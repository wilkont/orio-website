// Publication copy reflects approved policy and observed evidence, not live reserve assertions.
export const pages = [
 ['launch-readiness','Launch readiness','Evidence for each part of a financial launch.',[
  ['What is live','The public informational website is live. This page distinguishes it from the unavailable financial services and identifies the evidence required before those services can open.'],
  ['What this matrix controls','This is a dated publication of engineering status, not a financial authorization mechanism. Editing a website file cannot enable signing, custody, account enrollment or real-money settlement.'],
  ['Accountable acceptance','The monetary economics are approved. External review is advisory. Actual implementation, custody/reserve arrangements, customer controls and release-specific acceptance remain required.'],
 ]],
 ['how-it-works','How ORIO works','Understand the flow of value.',[
  ['Purchase','The approved model charges a 1% conversion fee. With existing eligible holders, 20% of the collected fee goes to ORIO Company and the remainder appreciates eligible holdings before new tokens are minted. No extra ORIO is minted to distribute appreciation.'],
  ['Hold and send','Ordinary ORIO transfers have no additional protocol fee. Every on-chain action still carries a separately quoted, user-paid network fee. Company-managed execution is intended to remove the need for users to hold ETH.'],
  ['Redeem','A redemption batch uses a common opening price. Redeemed tokens do not receive appreciation from their own redemption. Full-supply redemption allocates the entire conversion fee to the company.'],
 ]],
 ['stable-progressive-currency','Stable Progressive Currency','A reference price, not a guaranteed peg.',[
  ['What progressive means','The monetary design allocates eligible conversion fees to remaining holders through the redemption price. This is an economic mechanism, not guaranteed interest, investment performance or protection against loss.'],
  ['Genesis','The original opening reference is $1 per ORIO. It is not a perpetual $1 promise. USDC must be valued using reserve controls; a dollar peg must not simply be assumed.'],
  ['Availability','Live purchases and redemptions are not available. Test-network connectivity and local execution evidence do not establish production readiness.'],
 ]],
 ['wallet','ORIO Wallet','Simple access requires careful recovery.',[
  ['Intended experience','The wallet is designed to show balances, complete transaction costs, authorization limits and reconciled receipts without requiring users to manage ETH. Consumer account enrollment is not open.'],
  ['Recovery candidate','Qualification contracts support multiple guardians, a quorum, a recovery delay, owner cancellation and execution freezing during a pending recovery. Consumer enrollment, notifications and recovery operations still require integration.'],
  ['Protect your credentials','Never give anyone a recovery phrase, private key or account password. This website does not request wallet connections or recovery secrets.'],
 ]],
 ['send-and-receive','Send and receive','The recipient receives the authorized amount.',[
  ['Protocol fee','An ordinary transfer of 100 ORIO delivers the authorized 100 ORIO to the recipient. No additional ORIO protocol transfer fee applies.'],
  ['Network fee','The sender separately authorizes the applicable network cost. If an ORIO-denominated gas charge is selected, it is a separate payment to the Gas Treasury, not an appreciation-generating redemption.'],
  ['Current availability','Live sending and receiving are not enabled on this website. Do not send assets to an address presented as an ORIO launch address unless an authenticated release explicitly publishes it.'],
 ]],
 ['convert','Convert','Know every cost before authorization.',[
  ['Purchase disclosure','The intended confirmation separates purchase amount, 1% conversion fee, network fee, token quantity, expiry and maximum authorized cost. Network costs must not reduce the monetary backing silently.'],
  ['Redemption disclosure','A redemption confirmation must show gross value, conversion fee, network charge and final proceeds. Any gas deduction from proceeds requires authorization.'],
  ['Not a live quote','The homepage fee explorer is illustrative approved-policy arithmetic. It does not accept funds, estimate actual network fees or execute conversions.'],
 ]],
 ['business','ORIO for businesses','Payments with explicit settlement.',[
  ['Merchant experience','Merchant payment and settlement flows are planned. Availability, supported jurisdictions, identity checks and commercial terms are not yet established.'],
  ['What a receipt must explain','A payment receipt must distinguish requested amount, asset, protocol fee, network charge, execution reference, refunds and settlement status. A database balance alone is not finalized ownership.'],
  ['No payment acceptance yet','This site does not provide live merchant checkout, settlement or business account enrollment.'],
 ]],
 ['developers','ORIO for developers','Build against documented boundaries.',[
  ['Source and evidence','The engineering repository contains the monetary engine, qualification contracts, immutable ledger, settlement adapters and tests. Public source publication is separate from deployed service availability.'],
  ['Exact units','Financial boundaries use canonical integer strings. ORIO has 18 decimal places and USDC has 6. Binary floating-point arithmetic is not used for settlement.'],
  ['API availability','There is no public authenticated financial API endpoint to use yet. Do not rely on legacy endpoints for the SPC 3 monetary protocol.'],
 ]],
 ['protocol','ORIO Protocol','Separate economics, custody and evidence.',[
  ['Execution','Qualification contracts include currency, monetary controller, reserve vault, redemption locks, master-asset registry and Gas Treasury paymaster candidates. They reject Base mainnet.'],
  ['Two ledgers','Ledger A records immutable balanced financial journals and entitlements. Ledger B records finalized on-chain ownership and execution. Reconciliation links the two and rejects duplicate external events.'],
  ['Failure behavior','Invalid, stale or conflicting evidence must pause the affected settlement rather than create unsupported balances. Accounting corrections use compensating entries.'],
 ]],
 ['economics','Monetary economics','The approved rules, made explicit.',[
  ['Ordinary conversions','Purchases and redemptions charge 1%. Company entitlement is rounded down from 20% of the collected fee and holders receive the remainder. Purchase appreciation occurs before minting; redeemed tokens are excluded from their own appreciation.'],
  ['Zero holders and full redemption','When supply is zero, the entire purchase fee goes to the company. Full-supply redemption also sends the entire fee to the company. There is no genesis or residual-supply escrow.'],
  ['Precision and residual supply','Minting and stablecoin payouts round down. The conversion fee rounds up to the settlement unit. Rounding residuals are explicit and segregated. Every positive remaining supply receives the ordinary holder share, even if tiny; unsafe precision must reject settlement.'],
  ['Reopening','A fully redeemed supply retains its last valid reference price. New issuance waits for reconciliation and does not automatically reset the reference to $1.'],
 ]],
 ['reserves','Reserve transparency','Unavailable data stays unavailable.',[
  ['Live financial data','Circulating supply, current redemption price, eligible reserve value, reserve coverage, composition and settled transaction statistics are not verified for a live SPC 3 deployment. They are unavailable, not zero.'],
  ['Asset separation','Customer redemption backing, company conversion revenue, Gas Treasury assets and rounding obligations must be recorded separately. Test results are not a reserve attestation.'],
  ['Addresses','No production SPC 3 contract or reserve address is published here. Mainnet deployment and custody qualification remain outstanding.'],
 ]],
 ['security','Security','Evidence before financial activation.',[
  ['Verified engineering checks','Local integration tests cover monetary conservation, replay protection, atomic journals, recovery behavior and gas separation. Provider checks verified a shared finalized Base Sepolia block and advertised EntryPoint support on November 14, 2026.'],
  ['Limits of that evidence','Test success does not prove live custody, legal qualification, market safety, deployed code identity or resilience to every attack. External review is advisory; actual security and operational acceptance remain required.'],
  ['Report concerns','Use the contact page to report a security concern. Do not include private keys, passwords or customer data. No bug bounty or response-time commitment is currently advertised.'],
 ]],
 ['governance','Governance','Changes need accountable authorization.',[
  ['Monetary policy','The founder-approved economics control implementation. Material economic changes require explicit authorization; an operator must not silently redirect holder allocations.'],
  ['Reserve changes','A master-asset replacement must preserve supply and holder balances, disclose losses, and not manufacture conversion fees or appreciation. Qualification code and accounting replay cover this boundary.'],
  ['Release acceptance','Legal, security, custody, financial and operational acceptance bind a specific release and deployment. One accountable owner may cover multiple roles; external review remains advisory. No public governance voting service is active.'],
 ]],
 ['docs','Documentation','Start with the model and its limits.',[
  ['Consumer guide','Read How ORIO Works, Pricing and Fees, Reserve Transparency and Risk Disclosures before evaluating the proposed financial experience. Website availability is not participant eligibility.'],
  ['Engineering guide','The linked source repository records the exact monetary model, contract candidates, dual-ledger integration and outstanding qualification. Production configuration must not reuse test keys or synthetic evidence.'],
  ['Availability','This documentation describes approved design and observed engineering progress. It does not announce a financial launch or provide a usable public financial API.'],
 ]],
 ['fees','Pricing and fees','Conversion and network fees are separate.',[
  ['Conversion fee','Purchases and redemptions carry the mandatory 1% conversion fee. Ordinary allocation is 20% company and 80% eligible holders before final asset-unit rounding. Zero-holder purchases and full-supply redemptions allocate the entire fee to the company.'],
  ['Network fee','Users pay the applicable network gas for purchases, redemptions, transfers and other authorized on-chain operations. The company Gas Treasury is intended to pay the network on their behalf. Gas does not create appreciation or conversion revenue.'],
  ['Limits and credits','A transaction must not exceed its authorized maximum gas charge without renewed consent. Unused estimates must be refunded or credited. Platform-caused failure charging needs an approved disclosed policy; no live fee schedule beyond the protocol rules is offered here.'],
 ]],
 ['stablecoins','Supported stablecoins','USDC is the initial master selection.',[
  ['Initial master','USDC is the initial Master Elected Stablecoin under the approved policy. This is a design selection, not a Circle partnership, endorsement or proof of reserves.'],
  ['Additional assets','No secondary stablecoins are announced as live supported assets. Approved secondary assets must be converted into the active master before minting is triggered.'],
  ['Peg and reserve risk','The system must not assume USDC is always worth one US dollar. Material depegging requires issuance restrictions and reserve-risk handling.'],
 ]],
 ['legal','Legal and compliance','Access depends on actual qualification.',[
  ['Informational website','This website explains an engineering project. It does not offer accounts, accept funds, establish merchant acceptance or announce a financial product launch.'],
  ['Eligibility','Supported countries, participant eligibility, licenses, identity verification and financial service terms are not established by viewing this site. Applicable legal and compliance readiness must be confirmed before activation.'],
  ['Documents','Website information, privacy information and risk disclosures are available below. Final financial service agreements are not yet offered for acceptance.'],
 ]],
 ['terms','Website terms','Information before participation.',[
  ['Scope','ORIO.IO Lab publishes information about ORIO-SPC 3.0. The site is informational and the fee explorer is a simulation. There is no financial account agreement or transaction authorization available here.'],
  ['Reliance and risk','Descriptions may change as engineering and qualification progress. This site does not promise appreciation, redemption liquidity, insurance, jurisdictional availability or guaranteed service. Review the stated evidence and limitations.'],
  ['Before financial use','Financial service terms, eligible jurisdictions and participant obligations must be published before enrollment. No financial terms are being accepted by viewing this page. Contact the project for questions about site content.'],
 ]],
 ['privacy','Privacy information','A website without wallet enrollment.',[
  ['Inputs','The fee explorer runs in the browser and does not send its input to an application service. This release has no registration, wallet-connection or payment form and requests no recovery secrets.'],
  ['Hosting and contact','A hosting provider may process ordinary request information such as IP address and browser metadata. Emailing the project shares your message and address with its mail systems. Do not send financial credentials or sensitive account data.'],
  ['Before enrollment','Detailed controller contact, retention, jurisdictional rights, identity-processing and account privacy information must be finalized before customer onboarding. This site does not claim that a future wallet has already met those requirements.'],
 ]],
 ['risks','Risk disclosures','Progress does not eliminate risk.',[
  ['Economic and asset risk','Activity-linked appreciation is not guaranteed. Stablecoins can depeg, reserves can be impaired and markets can lack liquidity. Positive residual supply can concentrate fee allocations. Tests do not eliminate strategic behavior or market risk.'],
  ['Technical and operational risk','Contracts, signing systems, providers, bridges, recovery procedures and networks can fail. Network fees can be charged on failed operations. Recovery and chain finality have delays and assumptions.'],
  ['Legal and participation risk','Eligibility and permitted services vary by jurisdiction. No live SPC 3 eligibility, custody arrangement, insurance or production reserve attestation is established here. Do not send funds in anticipation of a launch.'],
 ]],
 ['help','Help center','Answers without asking for secrets.',[
  ['Can I buy or redeem?','No. Live SPC 3 purchases and redemptions are not enabled. The explorer is illustrative arithmetic, not a quote or order.'],
  ['Do I need ETH?','The intended wallet abstracts ETH through a company-managed Gas Treasury. The user still pays the separately authorized network cost. This experience is not live yet.'],
  ['Is there an official launch address?','No production SPC 3 address is published on this site. Never send funds to an unverified address or share secrets with someone claiming to activate an account.'],
 ]],
 ['contact','Contact ORIO','Questions about the project.',[
  ['Project contact','The existing ORIO website identifies contact@orio.io as its contact address. Use email for general questions and security reports; delivery and response times are not guaranteed.'],
  ['Keep secrets private','Do not include passwords, private keys, seed phrases, payment credentials or identity documents in an unsolicited message. This site has no customer-verification upload workflow.'],
 ]],
 ['status','Status','A dated snapshot, not a live monitor.',[
  ['Financial services: not launched','Public wallet enrollment, purchases, redemptions, merchant checkout and production financial APIs are unavailable. No mainnet SPC 3 contracts are active through this release.'],
  ['Test-network checks: passed November 14, 2026','Account-owned Alchemy and Infura endpoints agreed on Base Sepolia finalized block 58794597 at 18:44:58 UTC. Pimlico advertised EntryPoint v0.8. This proves one-time read connectivity and capability reporting, not current uptime or contract admission.'],
  ['Engineering validation','181 local backend/database/execution integration tests, 39 contract tests and 4 credential-session security tests passed in the November 14 release preparation. Strict typechecking and packaged-service TLS, non-root and paused-state checks passed. These are local engineering results.'],
  ['Open work','Hosted workload and database upgrades, deployed custody, consumer authorization and recovery, complete gas attribution, production contracts and accountable release acceptance remain outstanding.'],
 ]],
 ['download','Download the app','No production app release yet.',[
  ['Availability','There is no official SPC 3 production app download or app-store listing linked by this release. Avoid unofficial downloads and requests for recovery secrets.'],
  ['What comes next','Verified release links, supported platforms, eligibility and account terms will be published after deployment and qualification. The current website provides documentation only.'],
 ]],
 ['sign-in','User sign in','Account access is not open.',[
  ['No SPC 3 sign-in service','Customer authentication has not been deployed for public financial use. This page does not collect a password or connect to a legacy wallet service.'],
  ['Stay informed','Read the status page for the dated engineering snapshot. Do not submit credentials to an unofficial page claiming early financial access.'],
 ]],
 ['register','User registration','Enrollment will follow qualification.',[
  ['Registration unavailable','There is no public SPC 3 customer enrollment or funds-acceptance flow in this release. Viewing ORIO.IO does not establish eligibility.'],
  ['Before enrollment','Qualified authentication, wallet recovery, privacy and service terms, participant checks and reserve/custody arrangements must be in place before accounts are offered.'],
 ]],
];
