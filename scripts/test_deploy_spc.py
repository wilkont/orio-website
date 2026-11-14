import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('deployment', Path(__file__).with_name('deploy_spc_host.py'))
deployment = importlib.util.module_from_spec(spec)
spec.loader.exec_module(deployment)

CONFIG = '''server {
 root /var/www/html/orio/build;
 index index.html;
 server_name orio.io www.orio.io;
 location / {
   # Original SPA fallback
   try_files $uri /index.html;
 }
 location /api {
   proxy_pass http://localhost:5000;
 }
 listen 443 ssl;
 ssl_certificate /existing/fullchain.pem;
 ssl_certificate_key /existing/privkey.pem;
}
server { listen 80; server_name orio.io www.orio.io; return 301 https://$host$request_uri; }
'''


class DeploymentGuards(unittest.TestCase):
    def test_commented_example_location_does_not_count_as_active_routing(self):
        example = '\n# server {\n#   location / {\n#     try_files $uri $uri/ =404;\n#   }\n# }\n'
        rendered = deployment.render_config(CONFIG + example, Path('/var/www/orio-spc/releases/' + 'a' * 40))
        self.assertIn(example, rendered)
        self.assertIn('root /var/www/orio-spc/releases/' + 'a' * 40 + ';', rendered)

    def test_failed_https_verification_restores_original_before_reload(self):
        writes, commands = [], []
        def verify():
            self.assertEqual(writes, [b'candidate'])
            raise ValueError('wrong served bytes')
        with patch.object(deployment, 'atomic_write', side_effect=lambda path, data, metadata: writes.append(data)), \
                patch.object(deployment, 'run', side_effect=lambda *args: commands.append(args)):
            with self.assertRaisesRegex(RuntimeError, 'original Nginx configuration restored'):
                deployment.perform_cutover(b'original', b'candidate', None, verify)
        self.assertEqual(writes, [b'candidate', b'original'])
        self.assertEqual(commands, [('nginx', '-t'), ('systemctl', 'reload', 'nginx')] * 2)

    def test_invalid_configuration_is_not_reloaded_as_candidate(self):
        writes, commands = [], []
        def command(*args):
            commands.append(args)
            if len(commands) == 1:
                raise ValueError('invalid candidate syntax')
        with patch.object(deployment, 'atomic_write', side_effect=lambda path, data, metadata: writes.append(data)), \
                patch.object(deployment, 'run', side_effect=command):
            with self.assertRaises(RuntimeError):
                deployment.perform_cutover(b'original', b'candidate', None, lambda: self.fail('Verification must not run'))
        self.assertEqual(writes, [b'candidate', b'original'])
        self.assertEqual(commands, [('nginx', '-t'), ('nginx', '-t'), ('systemctl', 'reload', 'nginx')])

    def test_root_switch_preserves_api_tls_and_redirect(self):
        candidate = Path('/var/www/orio-spc/releases/' + 'a' * 40)
        rendered = deployment.render_config(CONFIG, candidate)
        self.assertIn('root ' + candidate.as_posix() + ';', rendered)
        self.assertIn('location /api {\n   proxy_pass http://localhost:5000;\n }', rendered)
        for line in CONFIG.splitlines():
            if 'ssl_' in line or 'listen' in line or 'return 301' in line:
                self.assertIn(line, rendered)
        self.assertIn('types { application/javascript mjs; }', rendered)
        self.assertIn('try_files $uri $uri/ =404;', rendered)
        self.assertIn("connect-src 'none'", rendered)

    def test_configuration_drift_cannot_be_overwritten(self):
        for changed in [CONFIG.replace('/var/www/html/orio/build', '/another/site'),
                        CONFIG.replace('location / {', 'location / { proxy_pass http://another;'),
                        CONFIG.replace('location /api {', 'location /different-api {'),
                        CONFIG.replace('orio.io www.orio.io', 'another.example')]:
            with self.assertRaises(ValueError):
                deployment.render_config(changed, Path('/var/www/orio-spc/releases/' + 'a' * 40))
        with self.assertRaises(ValueError):
            deployment.render_config(CONFIG, Path('/tmp/release'))

    def test_manifest_rejects_traversal_foreign_paths_and_unpinned_files(self):
        files = {name: 'b' * 64 for name in ['index.html', 'app.mjs', 'fees.mjs', 'release.json']}
        deployment.validate_manifest({'commit': 'a' * 40, 'files': files})
        for invalid in ['../secrets', '/etc/nginx/nginx.conf', 'assets/../../x', 'a\\b', 'a//b']:
            with self.assertRaises(ValueError):
                deployment.validate_manifest({'commit': 'a' * 40, 'files': {**files, invalid: 'b' * 64}})
        with self.assertRaises(ValueError):
            deployment.validate_manifest({'commit': 'main', 'files': files})


if __name__ == '__main__':
    unittest.main()
