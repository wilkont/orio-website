# ORIO website release — November 14, 2026

## Completed public cutover

ORIO.IO and www.orio.io now serve this release from the existing OrioApp host. The original Dot preview's white/blue design, ORIO logo and circular USDC artwork were retained. All32 static files matched the pinned source on each domain:64 origin HTTPS checks and64 independent public HTTPS checks passed. Live browser checks confirmed the design and zero-holder fee calculation. Source and backup identities are in DEPLOYMENT_2026-11-14.json. The legacy API route and TLS configuration were preserved; no DNS, IAM, database or server-reboot change occurred. The authorized Ubuntu shell was logged out after verification.

All59 legacy static files were verified against the archived backup; the old build remains untouched. Six deployment tests cover drift, path restrictions, preservation, commented Nginx examples and rollback control flow. This is not a database recovery drill or a financial launch. The preparation/access limitations below are historical context, superseded for the website cutover by this completed record. Financial workload deployment and qualification remain outstanding.

This is a static informational website, not live financial software. It preserves the owner's existing white/blue branding and authentic ORIO logo. The earlier untracked public/spc-next design is preserved as found. No legacy PHP service or credential is executed.

## Source and verification

Build with `node scripts/build-spc.mjs`; verify with `node --test scripts/test-spc.mjs`. No package installation is required. The builder writes public/spc-3 with 26 pages and local assets. Its inputs are entirely tracked under site/ and scripts/. BigInt fee arithmetic follows approved six-decimal USDC rounding and the ordinary/zero-holder/full-redemption exceptions; it is explicitly not a live quote. Tests validate all internal page/anchor/asset destinations and 3,000 fee-allocation vectors. Browser checks confirmed the zero-holder example, lifecycle panel behavior and mobile/desktop presentation at390x844 and1440x900 with no observed horizontal overflow on the mobile homepage. Full assistive-technology and cross-browser certification is not claimed.

The public data snapshot is dated. No supply, reserve valuation, coverage, live price, contract address or production account availability is fabricated. Sign-in, registration, download and financial-action pages explain their actual unavailable status and collect no credentials. All visible navigation links work. There are no external font, analytics or executable dependencies in this static release.

## Deployment boundary

The current ORIO.IO apex still resolves to the legacy host52.14.199.108, associated in discovery with account710096437887/us-east-2. Platform target account720232346199 is separate. Do not assume a login to one grants deployment access to the other. AWS console reports all tabs signed out; owner sign-in has been requested. No authenticated SSH/SSM deployment session, current Nginx/Apache document root, current backup or atomic rollback has been verified.

The existing owner-private Sites publication is a review surface, not the ORIO.IO custom domain. Keep its audience private. Updating that publication does not establish a domain cutover. No paid host, new AWS resource, IAM expansion or DNS change is authorized implicitly by this document.

## Exact host cutover sequence once access is established

1. Verify account, instance identity and non-root deployer. Inspect only web-server virtual-host configuration and service status needed to locate the current site; do not dump environment files, customer data or legacy credentials.
2. Record the current source/release identity and web-server configuration. Create and verify a recoverable backup before changing the served document root. Existing evidence does not establish a backup.
3. Transfer only the contents of public/spc-3 into a new versioned static release directory outside existing application/data directories. Serve a staged path and verify every page, response MIME type, relative asset path, HTTPS certificate/hostname, no directory listing, security headers and mobile navigation.
4. Preserve TLS, mail/DNS, API routes and existing application data. If legacy financial endpoints are found, do not silently expose them as SPC3. Decide their explicit routing/maintenance behavior before switching the root.
5. Test the web-server configuration, then atomically switch only the accepted site root or release symlink. Recheck ORIO.IO and www over HTTPS with cache-busting and the release.json marker. Record exact server-side release identity and the public response.
6. If verification fails, atomically restore the prior root/configuration and test HTTPS again. Never roll back by deleting customer data or the database.

This plan uses the existing host without provisioning new resources. Actual existing-host access, backup storage and any incremental transfer costs must be established; no zero-cost guarantee for AWS is made. Do not change DNS merely to work around missing server access.
