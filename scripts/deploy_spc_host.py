"""Two-phase static-site cutover for the inspected OrioApp host only.

Run stage/activate through the existing authorized Ubuntu session. No IAM, DNS,
TLS key, database, API, wallet or package-management operation is implemented.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import tarfile
import tempfile
import time
import urllib.request

CONFIG = Path('/etc/nginx/sites-available/default')
OLD_ROOT = Path('/var/www/html/orio/build')
RELEASES = Path('/var/www/orio-spc/releases')
BACKUPS = Path('/var/backups/orio-spc')
SOURCE = 'https://raw.githubusercontent.com/wilkont/orio-website/'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def file_digest(path):
    with open(path, 'rb') as handle:
        return stream_digest(handle)


def stream_digest(handle):
    result = hashlib.sha256()
    for chunk in iter(lambda: handle.read(1024 * 1024), b''):
        result.update(chunk)
    return result.hexdigest()


def validate_manifest(manifest):
    if not isinstance(manifest, dict) or not re.fullmatch('[a-f0-9]{40}', manifest.get('commit', '')):
        raise ValueError('Invalid source commit')
    files = manifest.get('files')
    if not isinstance(files, dict) or not 1 <= len(files) <= 1000:
        raise ValueError('Invalid release file list')
    for name, checksum in files.items():
        p = PurePosixPath(name)
        if (p.is_absolute() or '..' in p.parts or str(p) != name or '\\' in name
                or not re.fullmatch('[A-Za-z0-9_./-]+', name)
                or not re.fullmatch('[a-f0-9]{64}', checksum)):
            raise ValueError('Invalid release file identity')
    if not {'index.html', 'app.mjs', 'fees.mjs', 'release.json'} <= files.keys():
        raise ValueError('Incomplete static release')
    return manifest


def render_config(original, candidate, manifest=None):
    """Refuse drift; preserve /api and the complete TLS/redirect configuration."""
    candidate_path = candidate.as_posix()
    if not re.fullmatch(r'/var/www/orio-spc/releases/[a-f0-9]{40}', candidate_path):
        raise ValueError('Unexpected candidate root')
    if not re.search(r'(?m)^[ \t]*server_name\s+orio\.io\s+www\.orio\.io\s*;', original):
        raise ValueError('Unexpected virtual host')
    manifest = manifest or {}
    previous = manifest.get('previousRoot')
    if previous is not None:
        if (not re.fullmatch(r'/var/www/orio-spc/releases/[a-f0-9]{40}', previous)
                or not re.fullmatch('[a-f0-9]{64}', manifest.get('expectedConfigSHA256', ''))
                or digest(original.encode()) != manifest['expectedConfigSHA256']):
            raise ValueError('Previous release or configuration fingerprint differs')
        root = 'root ' + previous + ';'
        if original.count(root) != 1:
            raise ValueError('Unexpected existing document root')
        if len(re.findall(r'(?m)^[ \t]*try_files \$uri \$uri/ =404;', original)) != 1:
            raise ValueError('Unexpected existing static routing')
        result = original.replace(root, 'root ' + candidate_path + ';', 1)
        if 'error_page 404 /404.html;' not in result:
            result = result.replace('try_files $uri $uri/ =404;', 'try_files $uri $uri/ =404;\n        error_page 404 /404.html;', 1)
        return result
    root = 'root /var/www/html/orio/build;'
    if original.count(root) != 1:
        raise ValueError('Unexpected existing document root')
    # The observed root location contains only the SPA fallback and comments.
    pattern = r'(?m)^[ \t]*location[ \t]+/[ \t]*\{([^{}]*)\}'
    matches = list(re.finditer(pattern, original))
    if len(matches) != 1:
        raise ValueError('Unexpected root location')
    body = re.sub(r'#[^\n]*', '', matches[0].group(1))
    if re.sub(r'\s+', ' ', body).strip() != 'try_files $uri /index.html;':
        raise ValueError('Unexpected root-location directives')
    if not re.search(r'(?m)^[ \t]*location[ \t]+/api[ \t]*\{', original):
        raise ValueError('Existing API location missing')
    csp = ("default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
           "img-src 'self' data:; connect-src 'none'; form-action 'none'; "
           "frame-ancestors 'none'; base-uri 'self'; object-src 'none'")
    location = ('location / {\n        try_files $uri $uri/ =404;\n'
                '        add_header X-Content-Type-Options nosniff always;\n'
                '        add_header Referrer-Policy strict-origin-when-cross-origin always;\n'
                '        add_header Cache-Control "no-cache" always;\n'
                '        add_header Content-Security-Policy "' + csp + '" always;\n    }')
    result = original[:matches[0].start()] + location + original[matches[0].end():]
    modules = ''.join('\n    location = /' + name + ' {\n'
                      '        types { application/javascript mjs; }\n'
                      '        add_header X-Content-Type-Options nosniff always;\n'
                      '        add_header Cache-Control "no-cache" always;\n    }\n'
                      for name in ['app.mjs', 'fees.mjs'])
    return result.replace(root, 'root ' + candidate_path + ';' + modules, 1)


def checked_directory(path, mode=0o755):
    """Never follow a pre-existing writable/symlink release or backup parent."""
    for part in [*reversed(path.parents), path]:
        if part.exists():
            info = part.lstat()
            if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
                raise ValueError('Unsafe directory component')
            if info.st_uid != 0 or info.st_mode & 0o022:
                raise ValueError('Directory is not exclusively administrator managed')
        else:
            part.mkdir(mode=mode)


def atomic_write(path, data, metadata):
    fd, temporary = tempfile.mkstemp(prefix='.orio-cutover-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, stat.S_IMODE(metadata.st_mode))
        os.chown(temporary, metadata.st_uid, metadata.st_gid)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def run(*args):
    # Operational output is limited to trusted nginx/curl tooling, never app env/logs.
    return subprocess.run(args, check=True, capture_output=True).stdout


def verify_candidate(candidate, manifest):
    found = {p.relative_to(candidate).as_posix() for p in candidate.rglob('*') if p.is_file()}
    if found != set(manifest['files']):
        raise ValueError('Candidate file membership differs')
    for name, checksum in manifest['files'].items():
        path = candidate / name
        if path.is_symlink() or file_digest(path) != checksum:
            raise ValueError('Candidate file verification failed')
    release = json.loads((candidate / 'release.json').read_text())
    if release.get('financialExecutionEnabled') is not False or release.get('pageCount') != sum(1 for name in manifest['files'] if name == 'index.html' or name.endswith('/index.html')):
        raise ValueError('Candidate publication state differs')


def stage(manifest):
    validate_manifest(manifest)
    old_root = Path(manifest.get('previousRoot', str(OLD_ROOT)))
    if CONFIG.is_symlink() or not CONFIG.is_file() or not old_root.is_dir():
        raise ValueError('Inspected configuration or site no longer exists')
    original = CONFIG.read_bytes()
    candidate = RELEASES / manifest['commit']
    render_config(original.decode(), candidate, manifest)  # Validate all routing assumptions before writes.
    old_files = sorted(p for p in old_root.rglob('*') if p.is_file())
    if any(p.is_symlink() for p in old_root.rglob('*')) or not old_files:
        raise ValueError('Legacy build contains links or no files')
    required = sum(p.stat().st_size for p in old_files) * 2 + 64 * 1024 * 1024
    if shutil.disk_usage('/').free < required:
        raise ValueError('Insufficient space for verified backup and release')
    checked_directory(BACKUPS, 0o700)
    backup = BACKUPS / (time.strftime('%Y%m%dT%H%M%SZ', time.gmtime()) + '-' + manifest['commit'][:12])
    backup.mkdir(mode=0o700)
    (backup / 'nginx-default.original').write_bytes(original)
    os.chmod(backup / 'nginx-default.original', 0o600)
    before = {p.relative_to(old_root).as_posix(): file_digest(p) for p in old_files}
    archive = backup / 'legacy-build.tar.gz'
    with tarfile.open(archive, 'w:gz') as handle:
        handle.add(old_root, arcname='legacy-build', recursive=True)
    os.chmod(archive, 0o600)
    restored = {}
    with tarfile.open(archive, 'r:gz') as handle:
        for entry in handle:
            if entry.isfile():
                stream = handle.extractfile(entry)
                restored[entry.name.removeprefix('legacy-build/')] = stream_digest(stream)
    after = {p.relative_to(old_root).as_posix(): file_digest(p) for p in old_root.rglob('*') if p.is_file()}
    if before != restored or before != after or CONFIG.read_bytes() != original:
        raise ValueError('Backup verification or configuration consistency failed')
    checked_directory(RELEASES)
    if candidate.exists():
        verify_candidate(candidate, manifest)
    else:
        staging = RELEASES / ('.staging-' + manifest['commit'])
        staging.mkdir(mode=0o755)  # Never overwrite a previous incomplete attempt.
        for name, checksum in manifest['files'].items():
            url = SOURCE + manifest['commit'] + '/public/spc-3/' + name
            with urllib.request.urlopen(url, timeout=20) as response:
                if response.geturl() != url:
                    raise ValueError('Unexpected source redirect')
                data = response.read(10 * 1024 * 1024 + 1)
            if len(data) > 10 * 1024 * 1024 or digest(data) != checksum:
                raise ValueError('Pinned download verification failed')
            destination = staging / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            destination.chmod(0o644)
        verify_candidate(staging, manifest)
        staging.rename(candidate)
    receipt = {'manifest': manifest, 'candidate': str(candidate), 'backup': str(backup),
               'originalConfigSHA256': digest(original), 'legacyArchiveSHA256': file_digest(archive),
               'legacyFileCount': len(before), 'financialExecutionEnabled': False,
               'deploymentHelperSHA256': file_digest(Path(__file__))}
    state = backup / 'stage.json'
    state.write_text(json.dumps(receipt, indent=2) + '\n')
    state.chmod(0o600)
    return {'status': 'STAGED_BACKUP_VERIFIED', 'state': str(state),
            'candidate': str(candidate), 'legacyFileCount': len(before),
            'legacyArchiveSHA256': receipt['legacyArchiveSHA256'], 'financialExecutionEnabled': False}


def verify_https(manifest):
    # Reload returns before new workers necessarily take the listener. Wait for
    # the pinned marker, rather than treating an old worker's response as success.
    for attempt in range(10):
        try:
            marker = run('curl', '--fail', '--silent', '--show-error', '--max-time', '5',
                         '--noproxy', '*', '--resolve', 'orio.io:443:127.0.0.1', 'https://orio.io/release.json')
            if digest(marker) == manifest['files']['release.json']:
                break
        except subprocess.CalledProcessError:
            pass
        time.sleep(0.2)
    else:
        raise ValueError('Pinned release marker did not become available')
    verified = 0
    for domain in ['orio.io', 'www.orio.io']:
        for name, checksum in manifest['files'].items():
            route = '/' if name == 'index.html' else '/' + name.removesuffix('index.html') if name.endswith('/index.html') else '/' + name
            response = run('curl', '--fail', '--silent', '--show-error', '--max-time', '15',
                           '--noproxy', '*', '--resolve', domain + ':443:127.0.0.1', '--dump-header', '-', 'https://' + domain + route)
            headers, separator, body = response.partition(b'\r\n\r\n')
            if not separator or digest(body) != checksum:
                raise ValueError('Served content differs from pinned release')
            mime = {'html': 'text/html', 'css': 'text/css', 'mjs': 'application/javascript',
                    'png': 'image/png', 'json': 'application/json', 'txt': 'text/plain', 'pdf': 'application/pdf', 'xml': '(?:application|text)/xml'}[name.rsplit('.', 1)[1]]
            if not re.search(r'^content-type:\s*' + mime + r'(?:;|\s|$)', headers.decode().lower(), re.M):
                raise ValueError('Served content type differs')
            verified += 1
    if '404.html' in manifest['files']:
        for domain in ['orio.io', 'www.orio.io']:
            response = run('curl', '--silent', '--show-error', '--max-time', '15',
                           '--noproxy', '*', '--resolve', domain + ':443:127.0.0.1',
                           '--write-out', '\n%{http_code}', 'https://' + domain + '/orio-missing-' + manifest['commit'])
            body, _, code = response.rpartition(b'\n')
            if code != b'404' or digest(body) != manifest['files']['404.html']:
                raise ValueError('Branded missing-page status differs')
    return verified


def perform_cutover(original, updated, metadata, verify):
    try:
        atomic_write(CONFIG, updated, metadata)
        run('nginx', '-t')
        run('systemctl', 'reload', 'nginx')
        return verify()
    except Exception as failure:
        atomic_write(CONFIG, original, metadata)
        run('nginx', '-t')
        run('systemctl', 'reload', 'nginx')
        raise RuntimeError('Candidate failed; original Nginx configuration restored and reloaded') from failure


def activate(state):
    state = Path(state)
    if (state.name != 'stage.json' or not state.resolve().is_relative_to(BACKUPS)
            or state.is_symlink() or state.stat().st_uid != 0 or state.stat().st_mode & 0o077):
        raise ValueError('Unsafe stage record')
    receipt = json.loads(state.read_text())
    manifest = validate_manifest(receipt['manifest'])
    candidate = RELEASES / manifest['commit']
    verify_candidate(candidate, manifest)
    if CONFIG.is_symlink() or digest(CONFIG.read_bytes()) != receipt['originalConfigSHA256']:
        raise ValueError('Nginx configuration changed after staging')
    original = (state.parent / 'nginx-default.original').read_bytes()
    if digest(original) != receipt['originalConfigSHA256']:
        raise ValueError('Configuration backup differs')
    if file_digest(state.parent / 'legacy-build.tar.gz') != receipt['legacyArchiveSHA256']:
        raise ValueError('Legacy archive differs')
    updated = render_config(original.decode(), candidate, manifest).encode()
    metadata = CONFIG.stat()
    count = perform_cutover(original, updated, metadata, lambda: verify_https(manifest))
    result = {'status': 'DEPLOYED_HTTPS_VERIFIED', 'sourceCommit': manifest['commit'],
              'verifiedHTTPSFiles': count, 'candidate': str(candidate), 'rollbackState': str(state),
              'activeConfigSHA256': digest(updated), 'financialExecutionEnabled': False,
              'apiAndTLSConfigurationPreserved': True}
    (state.parent / 'deployment.json').write_text(json.dumps(result, indent=2) + '\n')
    (state.parent / 'deployment.json').chmod(0o600)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', help='Pinned manifest JSON file')
    parser.add_argument('--activate', help='Previously verified root-owned stage record')
    args = parser.parse_args()
    if os.geteuid() != 0 or bool(args.stage) == bool(args.activate):
        parser.error('Use an authorized sudo session and exactly one phase')
    try:
        print(json.dumps(stage(json.loads(Path(args.stage).read_text())) if args.stage else activate(args.activate)))
    except Exception as failure:
        # Never emit raw Nginx configuration, request bodies or subprocess output.
        print(json.dumps({'status': 'BLOCKED', 'reason': str(failure) if isinstance(failure, (ValueError, RuntimeError)) else type(failure).__name__,
                          'financialExecutionEnabled': False}))
        raise SystemExit(1)
