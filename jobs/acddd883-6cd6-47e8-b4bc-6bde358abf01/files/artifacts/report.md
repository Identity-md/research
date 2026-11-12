# Cybersecurity incidents and vulnerabilities: two priority lists

**Research cut-off: 12 November 2026.** This report contains **20 general entries** and **20 web-application entries**. Dates and conclusions reflect the public sources accessed on that date.

## Scope and how to read this report

- **List A — last 60 calendar days:** 14 September–12 November 2026, inclusive.
- **List B — six months:** 12 May–12 November 2026. Web applications include their HTTP APIs, identity flows, server frameworks, and web administration interfaces. One cloud-platform case explicitly requires a broader assessment than a conventional website test.
- An entry qualifies through an incident/disclosure in the window or a **new authoritative exploitation notice** in it. Older initial disclosures are stated explicitly. A recent article about an otherwise unchanged old issue does not qualify.
- “Top” means an editorial priority shortlist, ordered broadly by observed exploitation/harm, reach, and severity. It is **not a statistically established global top 20**, or a ranking of financial losses. Public reporting is incomplete. Linked exploit chains count as one entry; different weaknesses in the same product are separate only where their mechanism and testing differ.
- **Exploited** means a named primary source reports successful exploitation or CISA lists the flaw in its Known Exploited Vulnerabilities (KEV) catalog. **Vendor-reported incident** means the affected organization acknowledges intrusion; that is not independent confirmation of every assertion. **Disclosed vulnerability** means technical exposure is established, but the sources cited here do not establish malicious exploitation.
- “Affected systems” identifies vulnerable products/configurations. **It does not mean every installation was compromised.** Counts of records, accounts, workspaces, and machines are not interchangeable. “Not disclosed” means unavailable in the cited evidence, not zero.
- Each source link leads to the available technical advisory or incident account. Where there is no completed postmortem, that limitation is stated. Versions listed are fixes for the named issue, not assurances that they fix all subsequent vulnerabilities; choose the latest supported release incorporating them.

**Common exploitation reference:** the [CISA-maintained KEV CSV](https://raw.githubusercontent.com/cisagov/kev-data/main/known_exploited_vulnerabilities.csv), checked at catalog version **2026.11.10**, supplies the KEV dates below. A KEV date establishes recognition of exploitation, not the attack's start, victim count, or loss. The CISA website itself returned HTTP 403 during research; its official GitHub data was accessible.

## List A — 20 significant general incidents / hacks / vulnerabilities

### A1. PHP2Shell — PHP request-state memory corruption

**Date/status:** disclosed 21 October; exploited, KEV 26 October. **Description/detail:** CVE-2026-109618 concerns out-of-memory cleanup of incompletely initialized data; CVE-2026-109619 concerns request state surviving its backing memory. Both can enable unauthenticated remote code execution (RCE). **Systems:** vulnerable PHP web workers; exact compromised-host count not disclosed. **Fix:** PHP 8.5.12, 8.4.27, 8.3.36, 8.2.35, or verified vendor backports; deploy/restart affected workers. Partial mitigations are not complete fixes. **Impact:** potential server takeover; attributable aggregate losses unavailable. **Technical account:** [PHP's security notice and releases](https://www.php.net/archive/2026.php).

### A2. Ivanti Connect Secure zero-day chain

**Date/status:** Volexity observed compromise in early October and published 13 October; exploited. **Description/detail:** CVE-2026-104935 combines authentication bypass and command execution; additional flaws enabled root access. **Systems:** an observed appliance was fully patched at the time, on 22.8R2.4; wider victim count unknown. **Impact:** attackers targeted Active Directory secrets, LAPS passwords and BitLocker recovery keys, and erased logs. **Fix:** apply Ivanti's current chain fixes; investigate memory and network evidence, since the integrity checker may miss compromise. Exact current fixed-build mapping could not be independently read from Ivanti's blocked portal. **Investigator account:** [Volexity's reconstruction](https://www.volexity.com/blog/2026/10/13/a-series-of-unauthenticated-events-chained-exploitation-of-ivanti-connect-secure-zero-days/).

### A3. Plex Media Server — SSRF-to-code-execution chain

**Date/status:** public proof of concept 16 October; Plex's exploitation update 19 October. **Description/detail:** CVE-2026-96652/96654/96655/96656 combine server-side request forgery (SSRF), internal-function access, owner-token disclosure and codec-directory file writing. **Systems:** internet-facing Plex servers before 1.43.3.10861; compromised count not given. **Impact:** Plex reports widespread exploitation installing miners and proxy software; no quantified losses. **Fix:** upgrade to 1.43.3.10861 or later; investigate and rebuild if compromise cannot be ruled out, invalidate sessions and change the account password. **Technical/remediation account:** [Plex's announcement](https://forums.plex.tv/t/important-security-update-for-plex-media-server-v1-43-2-and-earlier/942319/3).

### A4. Zeabur — cloud credentials and customer-host compromise

**Date/status:** activity 14–15 October; report 19 October; vendor-reported incident. **Description/detail:** stolen cloud/admin credentials enabled internal-network and database access. Initial credential acquisition remains unconfirmed. **Systems/impact:** Zeabur confirms root sign-ins to **101 GCP servers**, **3,218,965 environment-variable records** read, and **321,810 accounts** in the accessed database. These are different measures. Monetary loss is not quantified. **Fix:** vendor revoked keys, restricted networks and removed backup-secret exposure; customers should rotate exposed secrets and rebuild compromised hosts. **Account:** [preliminary report with confirmed versus assessed findings](https://zeabur.com/blogs/october-2026-security-incident).

### A5. Railway — internal access and environment-secret exposure

**Date/status:** activity 20–22 October; initial disclosure 21 October; preliminary report 22 October. **Description/detail:** vendor describes privilege escalation across internal systems and exposure of encrypted secrets, some potentially decrypted. Exploit mechanics remain undisclosed. **Systems/impact:** vendor estimates at most **1.85% of workspaces**, approximately **100,000**, had some variables potentially compromised; upstream resets affected more users. Builds and other services were interrupted. Machine count and losses unknown. **Fix:** rotate stored variables and API tokens; Railway restricted access and remediated identified paths. **Account:** [Railway's preliminary report and updates](https://blog.railway.com/p/preliminary-report-october-security-incident).

### A6. LiteLLM 1.107.0 — malicious release artifacts

**Date/status:** 21 October; vendor-confirmed supply-chain incident. **Description/detail:** a leaked, unrevoked Agent Platform admin key led to theft of an organization-owner OAuth token and release-workflow changes. Compromised publishing produced credential-stealing artifacts; the official source tag was clean. **Systems:** hosts installing/running affected PyPI wheels or container images, including floating tags during the affected interval; actual host count unknown. **Impact:** credential theft and remote tooling; aggregate losses undisclosed. **Fix:** remove affected artifacts, rebuild cleanly, rotate accessible credentials and verify image digests/signing-key changes. **Accounts:** [artifact windows and remediation](https://docs.litellm.ai/blog/security-incident-oct-21-2026); [vendor's canonical attack-chain account](https://docs.litellm.ai/blog/security-incident-oct-21-2026-attack-chain). The original live account contains superseded assumptions.

### A7. PingCAP / TiDB Cloud — stolen service-account access

**Date/status:** intrusion 9 September–7 October; disclosed 19 October, within this window. **Description/detail:** vendor says stolen service-account credentials enabled copying internal data and source code. **Systems/impact:** exported records included customer/account associations, SQL-editor text, commercial information and encrypted API-key values. Customer-specific scope and machine count remain unresolved. PingCAP reports no evidence that data stored in TiDB was impacted; this does not negate the internal-data exposure. **Fix:** identified credentials invalidated and access paths blocked by 14 October; four externally reported vulnerabilities were fixed and retested. **Account:** [PingCAP's ongoing incident report](https://www.pingcap.com/trust-hub/security/security-update-october-2026/).

### A8. Collabora built-in CODE server — command injection

**Date/status:** advisory 14 October; exploited, KEV 23 October. **Description/detail:** CVE-2026-110447 permits unauthenticated OS commands through `proxy.php` **while the built-in CODE server is not running**, including restart/crash windows. **Systems:** Nextcloud's `richdocumentscode` app before 26.4.303; standalone Collabora Online is unaffected. Actual victim count unknown. **Fix:** update the app to 26.4.303 or later, or remove it; merely disabling it is insufficient. EOL Nextcloud installations need upgrade or app removal. **Impact:** execution as the web-server user; loss totals unavailable. **Technical advisory:** [Collabora GHSA-g3vx-3m76-fghh](https://github.com/CollaboraOnline/online/security/advisories/GHSA-g3vx-3m76-fghh).

### A9. Brotli / Node.js — decoder memory corruption

**Date/status:** Node.js security release 21 October; Brotli flaw exploited, KEV 27 October. **Description/detail:** CVE-2026-111497 allows malformed compressed input to overrun an internal streaming-decoder buffer. **Systems:** applications decompressing attacker-controlled Brotli data; Node.js 22.x/24.x/26.x included vulnerable code. No disclosed compromised-host count. **Fix:** Node.js 22.23.4, 24.22.1, 26.12.1 or later supported fixes; other consumers should update their bundled Brotli. **Impact:** crash, memory disclosure or possible RCE; no aggregate financial figure. KEV exploitation of the component does not prove every Node.js deployment was attacked. **Technical account:** [Node.js advisory](https://nodejs.org/en/blog/vulnerability/october-2026-security-releases).

### A10. GPUStack — trusted-loopback authentication bypass

**Date/status:** original advisory 31 July; newly recognized exploitation, KEV 9 November. **Description/detail:** CVE-2026-102895 promotes loopback-looking requests to administrator, including requests through a local reverse proxy or forged real-IP header. **Systems:** GPUStack before 2.2.0; vendor documents exploitation of 2.1.1 with reverse-shell backends. Victim count unknown. **Fix:** 2.2.0 fixes this issue; use 2.2.2 or newer also for A15. Revoke suspicious admin keys and inspect workers. **Impact:** administrator access, exposed provider secrets and worker code execution; losses unquantified. **Technical account:** [GPUStack advisory](https://github.com/advisories/GHSA-gj9m-f8ph-pmhr).

### A11. IBM Aspera Faspex — authorization bypass

**Date/status:** IBM bulletin 7 November; exploited, KEV 9 November. **Description/detail:** CVE-2026-123218 allows a crafted application message to bypass authorization and grant administrative privileges. **Systems:** Faspex 5.0.0–5.0.19; actual victim/host counts not published. **Fix:** 5.0.19 PL1; verify `faspex-core` image 5.0.19, build `1ce4b13`, Fix Pack 1. IBM lists no workaround. **Impact:** administrative takeover; financial loss unknown. **Uncertainty:** IBM's prose requires an authorized user, but its CVSS vector says PR:N; this report conservatively retains the prose's authentication requirement. **Technical bulletin:** [IBM's remediation instructions](https://www.ibm.com/support/pages/node/7295921).

### A12. Cisco ASA / FTD — SSL VPN denial of service

**Date/status:** advisory 28 October; exploited, KEV 29 October. **Description/detail:** CVE-2026-76418 lets unauthenticated input in the Remote Access SSL VPN path crash/reload affected devices. **Systems:** ASA/FTD with the advisory's secondary-authentication/tunnel-group conditions; victim count unknown. **Fix:** branch-specific releases, e.g. ASA 9.24.1.27 or FTD 7.6.7; consult the full table. Disabling secondary authentication can reduce exposure but lowers security and is not a preferred permanent fix. **Impact:** availability loss, not demonstrated data theft or RCE; outage costs unpublished. **Technical advisory:** [Cisco's configuration checks and fixes](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-asaftd-tunnel-dos-s6mgkb75).

### A13. Cisco BroadWorks — XML external entity file disclosure

**Date/status:** disclosed 19 August; qualifies through KEV addition **10 November**. **Description/detail:** CVE-2026-20320 permits unauthenticated crafted OCI-P XML to resolve external entities and read files as the BroadWorks user. **Systems:** affected Application Delivery Platform, Application Server, Profile Server and Xtended Services Platform components before RI.2026.07; compromised count unknown. **Fix:** RI.2026.07 or applicable later release; no vendor workaround. **Impact:** sensitive-file/configuration disclosure; no loss figure. **Evidence timing:** Cisco's original advisory says no known malicious use, whereas the later KEV listing establishes subsequent exploitation recognition. **Technical advisory:** [Cisco BroadWorks bulletin](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-bworks-xxe-uwUd7CEt).

### A14. eMudhra — weak intermediate-CA private keys

**Date/status:** reported to Google 17 October; Google published 20 October, updated 4 November. **Description/detail:** insufficient randomness made private keys for **eight subordinate CA certificates** recoverable. **Systems:** vulnerable trust chains in clients lacking protective distrust updates, rather than a published count of hacked endpoints. **Fix:** Google blocked affected keys through CRLSet/Play Services; ensure clients and trust stores receive vendor protections. **Impact:** possible HTTPS impersonation. Google found no CT-logged certificates chaining to the six TLS intermediates before blocking, limiting demonstrated impact against CT-enforcing clients. Actual fraudulent use and financial loss are not established. **Account:** [Google's technical response](https://blog.google/security/protecting-chrome-and-android-users-from-compromised-emudhra-intermediate-ca-certificates/).

### A15. GPUStack — unverified SAML response

**Date/status:** advisory originally 30 September; indexed/reviewed 10 November; disclosed vulnerability. **Description/detail:** CVE-2026-102894 issues sessions from posted SAML identities without required validation, even when SAML is not configured. **Systems:** GPUStack >=0.7.1 and <2.2.2 with reachable callback. No confirmed malicious victim count. **Fix:** 2.2.2 validates responses and gates inactive-provider routes; block callback access pending upgrade. Disabling SAML alone is insufficient. **Impact:** possible arbitrary-user/admin takeover and replay; no reported loss. This is distinct from A10. **Technical advisory:** [GPUStack SAML findings and patch](https://github.com/advisories/GHSA-62m9-f875-rqw6).

### A16. GitLab / Ruby — regular-expression compiler RCE

**Date/status:** critical patch 21 October; disclosed vulnerability. **Description/detail:** CVE-2026-110264 is an integer overflow compiling crafted regular expressions, potentially allowing unauthenticated server code execution. **Systems:** vulnerable GitLab CE/EE branches from 7.0; successful malicious compromises are not established by this advisory. **Fix:** 18.11.13, 19.0.10, 19.1.9, 19.2.9, 19.3.6, 19.4.3, 19.5.1 or subsequent supported fixes. Custom-runtime installations also need Ruby 3.3.13/3.4.12/4.0.9 or later applicable fixes. **Impact:** potential code/repository/secret compromise; losses unknown. **Technical disclosure:** [GitLab's critical release](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-5-1-released/); detection guidance is not proof of successful exploitation.

### A17. React Server Components — conditional unauthenticated RCE

**Date/status:** maintainer publication 14 October; database publication/update 10 November. **Description/detail:** CVE-2026-126187 permits crafted payloads to produce RCE in rare response paths combining multiple typed arrays and attacker-controlled values. **Systems:** vulnerable React 19 server transport packages (`react-server-dom-webpack`, `-parcel`, `-turbopack`); client-only apps without RSC support are unaffected. **Fix:** 19.0.9, 19.1.10, 19.2.9 or 19.3.1 on the respective branch. **Impact:** potential server execution; no malicious exploitation, victim count or monetary loss established in the cited advisory. **Technical disclosure:** [React's advisory record and maintainer references](https://github.com/advisories/GHSA-xqc2-xf4c-x3h3).

### A18. Kubeflow Pipelines — shared-upload authorization omission

**Date/status:** maintainer publication 28 October; database publication 9 November; disclosed vulnerability. **Description/detail:** CVE-2026-77596 skips authorization for HTTP pipeline uploads with an empty namespace, allowing shared-pipeline creation/version injection. **Systems:** multi-user Pipelines through 2.17.3; low-privilege tenants, or unauthenticated callers where directly reachable. **Fix:** deploy 2.18.0 with matching manifests; review already uploaded versions and recurring runs. **Impact:** malicious workloads may execute when other tenants consume altered pipelines; actual compromised machines and loss unknown. **Technical disclosure:** [Kubeflow advisory](https://github.com/advisories/GHSA-rjr3-43j3-4q8g). Its body retains draft-publication wording despite public database metadata; release guidance is explicit.

### A19. Mongoose — query-selector injection in counts

**Date/status:** maintainer publication 2 November; database publication 10 November; disclosed vulnerability. **Description/detail:** CVE-2026-125120 leaves `countDocuments()` queries outside `sanitizeFilter` protection. **Systems:** Mongoose applications accepting user-influenced filters on affected major lines; no identified compromised machines. **Fix:** 6.13.11, 7.8.12, 8.24.3 or 9.9.2 respectively. **Impact:** potential query manipulation/information exposure depends on application use; the advisory does not establish RCE or a real-world loss total. **Technical advisory:** [Mongoose's patched ranges and workaround](https://github.com/advisories/GHSA-pcrw-h46h-c93h).

### A20. Tor relay hosts — unauthorized SSH interception

**Date/status:** Tor Project notice 5 October; operator-reported compromises under investigation. **Description/detail:** attackers changed Linux relay configurations, including converting non-exits to exits, to intercept SSH connections. Initial host-entry mechanism remains unknown; the notice does not establish a flaw in the Tor protocol itself. **Systems:** some Linux relay hosts; count unpublished. **Fix:** reject malicious relays, preserve evidence, reinstall compromised hosts, generate new relay identities and rotate host credentials. **Impact:** SSH interception and stolen host-key/credential risk; financial loss unreported. **Incident notice:** [Tor Project's operator warning and recovery guidance](https://forum.torproject.org/t/tor-relays-security-incident-affecting-some-relay-operators/22231).

## List B — 20 web-application cases in the last six months

**Interpretation:** “Could have been avoided with pentesting” is a **counterfactual inference**, not a verified historical fact. Every **Test opportunity** below is the report author's assessment. Prevention also requires fixing findings before exposure and retesting. Ordinary black-box scans are less likely to find runtime memory bugs than authenticated manual testing, code review, fuzzing, and dependency assessment. No claim is made that these organizations failed to commission testing.

Overlap with List A is intentional: the lists answer different questions. Cross-references identify overlap, and every entry still gives its own status, affected systems, impact and remediation. For entries marked disclosed vulnerability, no actual compromised-machine count or financial loss is established by the linked sources.

### B1. PHP2Shell (A1)

**Window/status:** 21 October disclosure; exploited. **Web detail/systems:** PHP worker request cleanup/state reuse can permit unauthenticated RCE across requests. **Fix:** 8.5.12/8.4.27/8.3.36/8.2.35 or verified backport. **Impact/machines:** server takeover possible; victim count and losses undisclosed. **Test opportunity — limited for routine pentests:** source-assisted request-parser fuzzing and memory-failure testing could discover it; after disclosure, dependency verification could identify exposure. No assurance a standard website assessment would find a zero-day. **Technical source:** [PHP notice](https://www.php.net/archive/2026.php).

### B2. Ivanti HTTPS authentication chain (A2)

**Window/status:** early October compromise, 13 October report; exploited. **Web detail/systems:** VPN web requests crossed authentication and command-execution boundaries, then enabled privilege escalation on appliances. **Fix:** current Ivanti chain patches, plus forensic investigation. **Impact/machines:** AD-secret targeting observed; total victims/losses undisclosed. **Test opportunity — specialized:** source-assisted testing of request-routing/header trust and unauthenticated CGI reachability could expose the entry path; a complete chain required deeper appliance research. **Investigator account:** [Volexity](https://www.volexity.com/blog/2026/10/13/a-series-of-unauthenticated-events-chained-exploitation-of-ivanti-connect-secure-zero-days/). Current exact fixed-build mapping remains unverified here.

### B3. Plex SSRF/token/file-write chain (A3)

**Window/status:** October; exploited widely according to Plex. **Web detail/systems:** internet-facing media-server endpoints reached privileged internal functions and exposed an owner token, enabling codec-directory writes. **Fix:** 1.43.3.10861 or later; rebuild and revoke sessions if compromised. **Impact/machines:** miners and traffic proxies observed; count and financial costs unknown. **Test opportunity — strong:** test unauthenticated HTTP endpoints for loopback SSRF, authorization of internal APIs, token leakage and dangerous configuration/file-write chaining. **Technical account:** [Plex advisory](https://forums.plex.tv/t/important-security-update-for-plex-media-server-v1-43-2-and-earlier/942319/3).

### B4. Collabora proxy command injection (A8)

**Window/status:** 14 October advisory; exploited. **Web detail/systems:** Nextcloud's built-in CODE proxy before 26.4.303 permits OS commands when CODE is stopped; standalone servers excluded. **Fix:** update to 26.4.303+ or remove the app. **Impact/machines:** web-user execution; victim count/losses unknown. **Test opportunity — strong with lifecycle coverage:** exercise the proxy unauthenticated during startup, crash and restart, then review shell-command construction. Testing only a healthy running server could miss the precondition. **Technical advisory:** [Collabora](https://github.com/CollaboraOnline/online/security/advisories/GHSA-g3vx-3m76-fghh).

### B5. GPUStack loopback admin bypass (A10)

**Window/status:** disclosed 31 July; KEV 9 November; exploited. **Web detail/systems:** before 2.2.0, same-host proxy topology or real-IP-header spoofing can turn anonymous API requests into admin requests. **Fix:** at least 2.2.0 for this issue; use 2.2.2+ for the separate SAML issue. **Impact/machines:** worker RCE/reverse shells reported on 2.1.1; count/loss unknown. **Test opportunity — strong:** test externally through the actual reverse proxy and vary client-IP trust inputs; verify every admin API requires authentication. **Technical account:** [GPUStack](https://github.com/advisories/GHSA-gj9m-f8ph-pmhr).

### B6. IBM Faspex privilege escalation (A11)

**Window/status:** 7 November bulletin; KEV 9 November; exploited. **Web detail/systems:** crafted messages bypass application authorization in 5.0.0–5.0.19. **Fix:** 5.0.19 PL1, verified container build. **Impact/machines:** full administrative privileges; victims/losses not disclosed. **Test opportunity — strong:** use ordinary and privileged accounts to compare message/API authorization and reject privilege-changing fields. **Technical bulletin:** [IBM](https://www.ibm.com/support/pages/node/7295921). Its prose/vector disagree about required authentication; do not rely on the score to infer that precondition.

### B7. SharePoint deserialization / authentication-bypass series

**Window/status:** July exploitation notice and patches; exploited. **Detail:** CVE-2026-50522 and related flaws include unsafe deserialization and missing authentication; the published authentication requirement for 50522 is disputed by observed exploitation reports. **Systems:** on-premises Subscription Edition, Server 2019 and Enterprise Server 2016; no machine count/loss total established here. **Fix:** applicable Microsoft security updates, credential rotation and compromise assessment; reconsider direct internet exposure. **Test opportunity — specialized:** source-assisted deserialization and unauthenticated-endpoint chain testing; known-flaw verification after disclosure. **Account:** [CERT-EU's 23 July advisory with Microsoft references](https://cert.europa.eu/publications/security-advisories/2026-009). No claim that every related CVE was first disclosed within this window.

### B8. Oracle PeopleSoft PeopleTools RCE

**Window/status:** Oracle alert 10 June; disclosed vulnerability in this source. **Detail:** CVE-2026-35273 affects Updates Environment Management over HTTP and can allow unauthenticated RCE. **Systems:** PeopleTools 8.61/8.62; earlier unsupported versions were not tested by Oracle. Confirmed malicious hosts/losses are not quantified by this alert. **Fix:** apply the alert's PeopleSoft patch/mitigation instructions; detailed availability document requires Oracle Support access. **Test opportunity — moderate:** inspect exposed management routes, authenticate every privileged operation, review component versions and validate known-flaw remediation. Discovery of the original RCE would require deeper testing. **Technical alert:** [Oracle](https://www.oracle.com/security-alerts/alert-cve-2026-35273.html).

### B9. Atlassian Data Center arbitrary file access

**Window/status:** 5 October disclosure; exploitation recognized 15 October. **Detail:** CVE-2026-21589 lets an unauthenticated user read known-path files within the web root, without directory enumeration. **Systems:** affected Jira, Confluence, Bitbucket, Bamboo, Crowd, Crucible and Fisheye; breached-machine count/loss unknown. **Fix:** product-specific patched releases, e.g. Jira 10.3.26, Confluence 10.2.19, Bitbucket 10.5.1. **Test opportunity — strong:** test resource-path normalization and unauthenticated access to sensitive known-path configuration files. **Sources:** [Atlassian's full affected/fixed table](https://confluence.atlassian.com/security/cve-2026-21589-arbitrary-file-access-vulnerability-impacts-multiple-products-1870495748.html), [Canada's later exploitation notice](https://www.cyber.gc.ca/en/alerts-advisories/atlassian-security-advisory-av26-1002). Cloud was patched; vendor found no Cloud exploitation evidence.

### B10. Adobe Commerce / Magento incorrect authorization

**Window/status:** 11 August bulletin; KEV 24 September; exploited. **Detail:** CVE-2026-71362 enables unauthenticated privilege escalation without user interaction. **Systems:** affected Commerce/Magento branches in APSB26-92, including July 2026 builds; actual compromised stores and losses undisclosed. **Fix:** corresponding August 2026 security builds or later supported releases; follow the product/branch table. **Test opportunity — strong:** compare anonymous/customer/admin access across sensitive application resources and APIs. **Technical bulletin:** [Adobe APSB26-92](https://www.adobe.com/trust/security/products/commerce/apsb26-92.html). Its original no-known-exploitation statement predates the KEV notice; do not treat it as current evidence of no attacks.

### B11. WSO2 API platform JWT authentication bypass

**Window/status:** initially disclosed **3 May, outside the six-month window**; included for new KEV exploitation recognition **24 September**. **Detail:** vendor describes CVE-2026-5430 as acceptance of tokens using unsupported signing algorithms, enabling account/admin takeover. **Systems:** API Manager 4.1–4.6 and listed Control Plane/Traffic Manager/Universal Gateway versions. Counts/losses undisclosed. **Fix:** vendor public patches or branch-specific U2 levels, e.g. API Manager 4.6.0 level 21. **Test opportunity — strong:** reject unsupported algorithms and invalid JWT signatures across privileged routes. **Technical advisory:** [WSO2](https://security.docs.wso2.com/en/latest/security-announcements/security-advisories/2026/WSO2-2026-5328/). KEV's path-traversal description conflicts with the vendor's JWT description; mechanism follows the vendor, exploitation status follows KEV.

### B12. GPUStack SAML account takeover (A15)

**Window/status:** 30 September publication; disclosed vulnerability. **Detail/systems:** >=0.7.1, <2.2.2 accepts unverified SAML identities and replay at the callback, including with SAML disabled. **Fix:** 2.2.2+; temporarily block callback access. **Impact/machines:** potential existing-admin impersonation; confirmed malicious victims/losses not established. **Test opportunity — strong:** submit unsigned, invalid-signature, expired and replayed assertions; test callback reachability with the provider disabled. **Technical advisory:** [GPUStack SAML account](https://github.com/advisories/GHSA-62m9-f875-rqw6).

### B13. Pocket ID stale email-verification token

**Window/status:** maintainer publication 29 July; database update 9 November; disclosed vulnerability. **Detail:** CVE-2026-115770 lets an ordinary user obtain a verification token, change email, then verify the new address using the old token. **Systems:** backend before `0.0.0-20260727180059-43aaccd5bfac`; downstream takeover requires email-based linking and other advisory preconditions. **Fix:** that backend revision or later; bind tokens to addresses and invalidate on change. **Impact/machines:** false verified-email claims and possible cross-app takeover; no observed victim/loss count. **Test opportunity — strong:** test account lifecycle transitions and relying-party linking, not just login. **Technical account:** [Pocket ID advisory](https://github.com/advisories/GHSA-rm8c-2cv8-jwf6).

### B14. Kubeflow shared-pipeline upload bypass (A18)

**Window/status:** 28 October publication; disclosed vulnerability. **Detail/systems:** Pipelines through 2.17.3 skips authorization for empty-namespace HTTP uploads; hostile shared versions can be consumed by other tenants. **Fix:** 2.18.0, matching manifests, and review existing pipeline versions/schedules. **Impact/machines:** possible execution of attacker-selected workloads; actual victims/loss unknown. **Test opportunity — strong:** compare low-privilege HTTP and gRPC writes; test omitted, empty and unauthorized namespaces, creation and version replacement. **Technical advisory:** [Kubeflow](https://github.com/advisories/GHSA-rjr3-43j3-4q8g).

### B15. Mongoose count-query injection (A19)

**Window/status:** 2 November publication; disclosed vulnerability. **Detail/systems:** unsanitized `countDocuments()` in affected Mongoose versions exposes apps using attacker-influenced count filters. **Fix:** 6.13.11/7.8.12/8.24.3/9.9.2 by branch. **Impact/machines:** possible query manipulation and count-based data inference; no established malicious-host count or loss. **Test opportunity — strong when reachable:** inject query operators into pagination/count APIs and compare count versus retrieval behavior under tenant restrictions. Impact is conditional on how the application builds queries. **Technical advisory:** [Mongoose](https://github.com/advisories/GHSA-pcrw-h46h-c93h).

### B16. GitLab regular-expression RCE (A16)

**Window/status:** 21 October; disclosed vulnerability. **Detail/systems:** CVE-2026-110264 reaches the Ruby regex compiler from vulnerable GitLab CE/EE paths and may allow unauthenticated execution. **Fix:** the critical GitLab builds in A16 or newer, plus patched Ruby for custom runtimes. **Impact/machines:** potential server/repository compromise; successful malicious victims/losses not established. **Test opportunity — limited for routine pentests:** source-assisted regex fuzzing and native crash analysis; dependency checks after disclosure. **Technical release:** [GitLab](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-5-1-released/).

### B17. React Server Components payload handling (A17)

**Window/status:** 14 October maintainer publication; disclosed vulnerability. **Detail/systems:** CVE-2026-126187 affects rare multiple-typed-array response paths in React 19 RSC transport packages; client-only apps excluded. **Fix:** 19.0.9/19.1.10/19.2.9/19.3.1 by branch and redeploy server code. **Impact/machines:** potential RCE; no proven malicious victim/loss count. **Test opportunity — specialized:** source-assisted serialization/deserialization fuzzing and malicious-value tests in actual RSC flows; ordinary browser-only scans may miss it. **Technical advisory:** [React record](https://github.com/advisories/GHSA-xqc2-xf4c-x3h3).

### B18. GitLab Group SAML identity authorization

**Window/status:** patched 10 June; disclosed vulnerability. **Detail:** CVE-2026-6552 permits a group Owner to take over another group member's account under the advisory's conditions. **Systems:** GitLab EE 15.5 onward on affected branches; actual victims/losses not established. **Fix:** 18.10.8/18.11.5/19.0.2 or later supported fixes. **Impact:** account takeover across the intended identity boundary. **Test opportunity — strong:** test one user's ability to alter another's SAML identity, separating group administration from ownership of personal accounts. **Technical disclosure:** [GitLab June release](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-0-2-released/).

### B19. GitLab Analytics Dashboard XSS

**Window/status:** patched 10 June; disclosed vulnerability. **Detail:** CVE-2026-10087 allows a developer-role user to execute client-side code as a targeted user through insufficient dashboard input sanitization; victim interaction is required. **Systems:** GitLab EE from 17.1 on affected branches; actual compromised users/machines and losses not disclosed. **Fix:** 18.10.8/18.11.5/19.0.2 or later supported fixes. **Test opportunity — strong:** test dashboard inputs and rendering with harmless script-execution markers across developer/viewer roles. **Technical disclosure:** [GitLab June release](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-0-2-released/). This browser-code issue is distinct from B18's identity authorization defect.

### B20. Zeabur platform/admin trust boundaries (A4)

**Window/status:** October; vendor-reported incident. **Detail/systems:** internet-reachable administration, long-lived tokens and internal-network/database trust amplified stolen credentials. **Fix:** vendor restricted interfaces, revoked keys and corrected backup-secret exposure; rotate customer secrets and rebuild compromised hosts. **Impact:** 101 confirmed GCP root sign-ins and millions of variable records accessed; total losses unknown. **Test opportunity — broader scope required:** a web/API assessment extended to cloud IAM and assumed-compromise segmentation could reveal the amplification paths. A normal website pentest cannot be credited with preventing the unconfirmed initial credential theft. **Preliminary account:** [Zeabur](https://zeabur.com/blogs/october-2026-security-incident).

## Evidence limits and unanswered questions

The most actionable distinction is between established exploitation and serious but as-yet unproven malicious use. Do not total the exposure figures across these entries: a leaked secret may belong to a workspace, a single machine may run several affected products, and the lists deliberately overlap.

Most cited sources do not publish aggregate financial losses or complete victim inventories. This report therefore does not estimate them from severity scores, exposed installations, attacker claims or record counts. Company incident reports remain self-reported and several are preliminary. Negative findings such as “no evidence” describe the reviewed evidence, not proof that all possible compromise has been excluded.

Unresolved points include the original credential-acquisition path at Zeabur, exact decrypted-secret scope at Railway, customer-specific exposure at PingCAP, initial host-entry method for the Tor relays, current Ivanti fixed-build mapping, IBM's authentication/vector inconsistency, and the WSO2 vendor/KEV mechanism mismatch. Broader public sources may contain later answers; none is assumed here.

For vulnerability-only entries, the linked advisory is the available technical disclosure, not an incident postmortem. Penetration-test opportunities are reasoned possibilities based on the documented defect. They neither prove a test would have found it nor establish that a particular breach would certainly have been prevented.
