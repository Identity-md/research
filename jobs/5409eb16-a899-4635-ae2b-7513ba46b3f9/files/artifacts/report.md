# 20 significant cybersecurity incidents, hacks, and vulnerabilities from the last 60 days

**As of November 2, 2026. Reporting window: September 4–November 2, 2026, inclusive (60 calendar dates, UTC).**

This shortlist prioritizes reported financial loss, operational or personal harm, scale, active exploitation, and the importance of affected infrastructure. The order is editorial judgment, not a measured worldwide league table. A widely deployed vulnerability can merit inclusion even where no victim count is available.

**Date rule:** an incident qualifies through a public disclosure or substantial original investigation within the window. Some intrusions began earlier; their occurrence dates are stated separately. Thus this is a report of significant *recent disclosures and findings*, not a claim that every intrusion occurred in the last 60 days. Related bugs and their observed exploitation are grouped to avoid double counting.

**Evidence rule:** “confirmed” means explicitly reported by the affected organization or investigating researchers, not independently verified by this author. Attribution and AI involvement remain source assessments unless demonstrated. Affected installations, downloads, accounts, records, and compromised machines are different measures. “Unknown” means not established in the cited material; it does not mean zero. Financial amounts are USD unless otherwise stated. Sources were accessed November 2, 2026; links lead to the detailed notice or technical investigation and may subsequently change.

## At a glance

| # | Short name | Qualifying disclosure / investigation | Category |
|---|---|---|---|
| 1 | Binance hot-wallet theft | Oct 30; recovery update Nov 1 | Confirmed theft; investigation ongoing |
| 2 | PHP2Shell / PAN-OS exploit chain | Oct 21; campaign report Oct 26–29 | Exploited vulnerabilities |
| 3 | eMudhra intermediate-CA compromise | Oct 20 technical response | Cryptographic trust failure |
| 4 | LiteLLM 1.107.0 | Oct 21; post-mortem Oct 23 | Software supply-chain compromise |
| 5 | Railway secrets breach | Oct 21; preliminary report Oct 22 | Platform intrusion |
| 6 | Cursor marketplace backdoor | Oct 29; revised Oct 30 | Extension supply-chain compromise |
| 7 | French supermarket refrigeration sabotage | Oct 12; alert revised Oct 16 | Operational-technology intrusion |
| 8 | CAPCOM ID breach | Oct 22 | Customer-data breach |
| 9 | GMO Desktop Cloud trading compromise | Oct 21–22 | Hosted-server compromise |
| 10 | Quest Quanum LSM | Oct 22 SEC filing | Healthcare-system intrusion |
| 11 | TeamUpdraft / UpdraftCentral | Oct 19 onward | Vendor-to-customer intrusion |
| 12 | OVHcloud CLI release substitution | Oct 19 | Binary supply-chain compromise |
| 13 | UTA0565 Chrome–Windows zero-day chain | Sep 21 investigation | Targeted espionage |
| 14 | Kapibala / Red Heron campaign | Sep 21 investigation | Multi-product exploitation |
| 15 | VeloCloud Orchestrator takeover | Oct 22 advisory | Actively exploited privilege escalation |
| 16 | Brotli / Node.js decoder RCE | Oct 21 security release | Memory-corruption vulnerability |
| 17 | Cisco ASA / FTD VPN denial of service | Oct 28 advisory | Actively exploited availability flaw |
| 18 | Microsoft 365 passkey-lure intrusions | Sep 9 investigation | Identity and cloud compromise |
| 19 | CHOSEN BRICK | Sep 15 joint advisory | Targeted surveillance malware |
| 20 | Chainalysis internal-tools breach | Oct 30 notice | Customer-directory exposure |

The linked sources in each numbered entry support its date and factual fields. “Fix” includes containment and recovery where the incident has no installable software patch.

## 1. Binance hot-wallet theft

**Date / evidence:** Unauthorized withdrawals occurred around October 29, 20:05 UTC; Binance's October 30 update confirms the incident. Recovery update #4 is dated November 1.

**Description and detail:** Attackers compromised hot wallets. An initial theory involved a DevOps laptop reaching a service container, but Binance subsequently found additional breach points. The laptop explanation is provisional, not a completed root-cause analysis.

**Compromised machines / systems:** Hot-wallet withdrawal infrastructure; a laptop is suspected. Host count and complete attack path remain unknown. Binance reports no evidence of leaked wallet private keys.

**Impact:** Approximately **$6.3 billion in token assets stolen**, according to Binance. Its initial update reported about $3 billion frozen. Frozen assets are not necessarily recovered, and replenishment with company assets is a separate measure.

**Fix / status:** Affected authorization revoked, withdrawals temporarily suspended, security reviews and tracing initiated. November 1 update announced phased withdrawal restoration and approximately 95% replenishment; deposits remained operational. These are company statements, not an independent reserves audit.

**Unknown / post-mortem:** Full root cause, final net loss and recovery; technical post-mortem still promised in these notices. Sources: [Binance update #2](https://www.binance.com/en/support/announcement/detail/d3306d9dca5243548c813b605e1d1751), [initial update](https://www.binance.com/en-GB/support/announcement/security-incident-update-2026-10-30-c5a8729a97ac486d963784d96c5642d7), [November 1 recovery update](https://www.binance.com/en-GB/support/announcement/security-incident-recovery-update-4-withdrawals-resume-in-phases-2026-11-01-73911fb819b240f88b88256bdd318eda).

## 2. PHP2Shell and the PAN-OS / Fragnesia chain

**Date / evidence:** PHP patches October 21; Dream reported its October 25 discovery on October 26, updated October 29. Unit 42 independently verified the recovered tooling and results.

**Description and detail:** CVE-2026-109618 and CVE-2026-109619 enable unauthenticated code execution through PHP memory/state corruption. Attackers chained them with Linux privilege escalation CVE-2026-46300 (“Fragnesia”) against exposed PAN-OS management servers, then pursued credentials and Active Directory access.

**Compromised machines / impact:** Dream reports **25 firewall/management servers** across the US, Japan, Taiwan and South Korea, including three in a US government-affiliated environment. Credential extraction and persistent access are reported; financial loss and full downstream compromise are unknown.

**Fix:** PHP 8.2.35, 8.3.36, 8.4.27 or 8.5.12; use distribution backports where appropriate. For appliances, apply the vendor's PAN-OS hotfix, not an independently replaced PHP runtime, and remove public management access. The appliance advisory supplies branch-specific versions.

**Uncertainty / technical reports:** Chinese nexus and AI-assisted development are assessments; finding AI tools does not prove they authored the exploit. Unit 42 retracted a separate October 23 PHP2Shell attribution before confirming this campaign. Sources: [PHP advisory](https://www.php.net/archive/2026.php), [Dream investigation](https://dreamgroup.com/blog/chained-php2shell-exploit-roots-25-servers), [Unit 42 verification and correction](https://unit42.paloaltonetworks.com/cve-2026-109618-cve-2026-109619/), [PAN-OS fixes](https://security.paloaltonetworks.com/CVE-2026-109618).

## 3. eMudhra intermediate certificate-authority compromise

**Date / evidence:** Cloudflare's October 20 response says it learned of the issue October 19, approximately 17:00 UTC.

**Description and detail:** Weak private keys associated with **eight eMudhra intermediate certificates** made certificate forgery possible. An attacker could impersonate arbitrary domains to a client still trusting those intermediates. This compromises authentication, not TLS encryption algorithms themselves.

**Compromised machines / systems:** Certificate-signing keys and the trust paths that accept them; no count of successfully intercepted endpoints is established. A trusting browser or server is exposed, not automatically compromised.

**Impact:** Potential traffic interception or alteration across many software stacks. Cloudflare says its review found no active exploitation on its services. No verified financial-loss total is available in that report.

**Fix:** Update trust stores and bundled verifiers, redeploy affected images and restart services as needed. Cloudflare lists cloudflared **2026.10.2** and platform-specific WARP/client updates. Test the actual application's certificate-validation path; a browser test does not validate a separate service.

**Unknown / detailed response:** Wider exploitation and victim counts remain unknown. The cited response is Cloudflare's operational account, not a complete eMudhra root-cause post-mortem. Source: [Cloudflare technical response and remediation matrix, October 20](https://blog.cloudflare.com/emudhra-certificate-compromise).

## 4. LiteLLM 1.107.0 supply-chain compromise

**Date / evidence:** Malicious release October 21; vendor's canonical attack-chain report October 23.

**Description and detail:** A previously published, unrevoked administrative key enabled Agent Platform access on October 10. Attackers extracted an organization-owner GitHub token, acquired additional maintainer tokens, changed release workflows and published poisoned wheels and containers. Python startup hooks ran a credential stealer without requiring an explicit LiteLLM import.

**Compromised machines / systems:** Maintainer identities and release infrastructure; downstream environments running affected 1.107.0 artifacts or floating container tags during the incident. Wiz reports approximately **49,000 downloads**, which is not a count of infected machines.

**Impact:** Cloud, developer and AI credentials exposed; Wiz observed subsequent use of stolen AWS credentials. Total downstream victims and financial loss are unknown.

**Fix:** Replace poisoned environments with verified clean artifacts, remove startup-hook persistence and rotate accessible secrets. The vendor rotated its image-signing key; first releases using the new key included **1.106.3** on October 24.

**Post-mortem / uncertainty:** Use the canonical report: it supersedes early theories about tokens in gateway logs. Sources: [vendor attack-chain post-mortem](https://docs.litellm.ai/blog/security-incident-oct-21-2026-attack-chain), [affected artifacts and cleanup](https://docs.litellm.ai/blog/security-incident-oct-21-2026), [Wiz payload and observed abuse](https://www.wiz.io/blog/litellm-compromised-steals-credentials).

## 5. Railway customer-secrets breach

**Date / evidence:** Public disclosure October 21; preliminary report dated October 22. Railway places the intrusion between October 20, 13:58 UTC and October 22, 03:32 UTC.

**Description and detail:** Attackers reached internal systems, queried encrypted environment variables and obtained CI credentials that enabled decryption of a subset. Railway assesses that obtaining AI-provider keys was an objective; claims about the attacker's models and compute are its assessment.

**Compromised machines / systems:** Internal platform and CI systems and customer-secret storage. Public reporting does not give a compromised-host or customer total. Envelope encryption and available logs prevent exact identification of every decrypted key.

**Impact:** Secret exposure plus disrupted builds, deployments, dashboard/API access and support tooling. No aggregate monetary loss is established.

**Fix:** Railway restricted and rebuilt internal systems, rotated credentials and invalidated access. Customers should rotate stored sensitive credentials at their issuers, revoke old credentials and redeploy. The status page says builds, API and dashboard were restored October 23; it cautions that absence of a higher-risk notification does not establish safety.

**Unknown / post-mortem:** Specific exploit details and final scope remain withheld or unresolved. Sources: [preliminary incident report](https://blog.railway.com/p/preliminary-report-october-security-incident), [status and customer remediation](https://status.railway.com/incident/QH8L8B3E).

## 6. Backdoored Claude Code extension in Cursor's marketplace

**Date / evidence:** Cursor notice October 29, revised October 30. Distribution window approximately 02:27–13:35 Pacific Time on October 29.

**Description and detail:** Tampered **Anthropic.claude-code 2.1.312 and 2.1.313** packages collected host information and attempted an SSH backdoor, reverse tunnel and persistence. Cursor says Anthropic did not develop the malicious builds.

**Compromised machines / systems:** Windows/macOS endpoints that installed the tampered packages from Cursor's marketplace. Exact compromised-machine count is not given in the cited notice. Version number alone cannot distinguish legitimate and substituted builds; Cursor provides hashes.

**Impact:** Host metadata sent, attacker SSH key planted and persistence installed. Cursor says errors and lack of administrator rights usually prevented enabling SSH and attacker login. That does not negate the other payload effects. Financial loss is unknown.

**Fix:** Malicious packages removed, marketplace rebuilt and attacker server taken down. Isolate affected hosts; remove keys, persistence and tunnels; assess rebuilding; rotate accessible credentials from a trusted device. Uninstalling alone is insufficient.

**Unknown / technical notice:** Marketplace entry method and subsequent attacker access remain unresolved. Source: [Cursor's revised security notice, hashes and cleanup procedures](https://cursor.com/blog/claude-code-extension-security-notice).

## 7. French supermarket refrigeration-controller sabotage

**Date / evidence:** Attacks reported October 11–12; CERT-FR alert October 12, revised October 16.

**Description and detail:** Intruders manipulated remotely managed refrigeration systems. CERT-FR confirms numerous controller compromises; reporting describes altered defrost/temperature settings and resulting food-stock disruption.

**Compromised machines / systems:** **Danfoss AK-SM and AK-SC, Copeland xweb and Dixell xweb** controllers. The official alert does not quantify compromised units. Store counts in coverage should not be equated with controller counts.

**Impact:** Spoiled/discarded food and restocking disruption reported by AP. The cited sources do not establish a total financial loss or injury count.

**Fix:** Remove internet exposure, inspect configurations, restore compromised devices as instructed, update firmware and change default passwords. Reconnect management through a secured VPN/protected network. CERT-FR specifically recommends Strict security mode for Danfoss equipment. Emergency source-IP filtering is temporary protection.

**Unknown / technical account:** No complete public post-mortem or demonstrated common CVE is supplied by the official alert; do not assume every controller was breached through the same flaw. Sources: [CERT-FR alert and recovery guidance](https://cert.cyber.gouv.fr/alerte/CERTFR-2026-ALE-012/?nocache=20261014a), [AP reporting, October 14](https://apnews.com/article/81c2d5721f4df77f601f71741ef7c291).

## 8. CAPCOM ID customer-data breach

**Date / evidence:** Unauthorized access detected October 19; Capcom disclosed findings October 22.

**Description and detail:** An external party accessed the shared account service used for Capcom web services and some online games. The company found customer-data leakage and unauthorized password changes, and says it completed emergency countermeasures.

**Compromised machines / systems:** CAPCOM ID service; host count unknown. **11,774,247 records** contained email addresses and account metadata, including creation/login information and last-login IP. Forty-three also contained birth date, gender, country/region and nickname; 196 accounts had passwords changed without authorization.

**Impact:** Large-scale personal-data exposure and account interference. Capcom says it did not confirm leakage of users' original passwords; credit cards were not included. It reports no interruption to game play. Monetary impact is not quantified.

**Fix:** Access blocked, affected passwords reset, emergency measures implemented and customer notification initiated. Customers should treat subsequent impersonation messages cautiously.

**Unknown / detailed notice:** Server-level exploit, final scope and full root cause remain unpublished in the notice. Source: [Capcom's English disclosure, October 22](https://www.capcom.co.jp/ir/english/news/html/e261022.html).

## 9. GMO Onamae.com Desktop Cloud trading-server compromise

**Date / evidence:** GMO confirmed malicious programs October 20; notices October 21 and 22.

**Description and detail:** Attackers installed malware in hosted desktop-server environments used for trading tools. Customer reports indicate unauthorized trading activity and possible theft of stored trading credentials and other files.

**Compromised machines / systems:** Some Desktop Cloud customer servers confirmed affected; **26,739 servers potentially affected** across all plans. This is an exposure estimate, not a verified infection total. Stored MT4/MT5 and brokerage credentials may have been viewed.

**Impact:** Unauthorized account operations reported; potential financial losses to traders, with no aggregate amount established. GMO says payment/card information is not stored on these service servers.

**Fix:** Change trading-tool, brokerage and other stored credentials from a device outside the affected service, disconnect sessions, inspect transaction histories, contact brokers about unauthorized trades and enable available two-factor authentication. These customer actions are containment, not a patch for the hosting breach.

**Unknown / detailed notice:** Entry vector, final infected-host count and final trading losses remain under investigation with an external security firm. Source: [GMO second report and urgent customer instructions, October 22](https://internet.gmo/en/news/article/247).

## 10. Quest Diagnostics Quanum LSM intrusion

**Date / evidence:** Quest learned of unauthorized access October 21 and filed an SEC Form 8-K dated October 22.

**Description and detail:** An unauthorized party reached Quanum LSM, used by certain clients to order tests and retrieve results. Quest says it believes some patient records were accessed; that qualification matters while scope is being investigated.

**Compromised machines / systems:** Quanum LSM application/system. The filing does not enumerate servers, accounts, patients or individual data fields.

**Impact:** Potential exposure of sensitive patient records. Quest reports no material disruption to business operations or patient service. Financial impact is not quantified; filing an 8-K does not by itself prove a quantified material loss.

**Fix:** Incident-response procedures, containment/remediation, external cybersecurity assistance and federal law-enforcement notification. No public customer-installable patch or CVE is identified in the filing.

**Unknown / detailed disclosure:** Root cause, access duration, patient count and final data scope. The reviewed document is a corporate disclosure, not a forensic post-mortem. Source: [Quest SEC Form 8-K, Item 8.01](https://www.sec.gov/Archives/edgar/data/1022079/000094787126000941/ss6979200_8k.htm).

## 11. TeamUpdraft breach and UpdraftCentral key abuse

**Date / evidence:** Unauthorized access identified October 17–18; updates and remediation published October 19 onward.

**Description and detail:** TeamUpdraft says a compromised key enabled access to its website and believes its customer database was accessed. Stored UpdraftCentral connection keys were used to reach connected WordPress sites and install malicious plugins/create accounts. This is distinct from a vulnerability in the UpdraftPlus plugin code or a poisoned plugin download.

**Compromised machines / systems:** Vendor website/database and connected customer WordPress sites; totals unknown. Database contents included contact/billing data, password hashes, 2FA settings and service connection keys.

**Impact:** Customer-data exposure and downstream site backdoors. Financial loss and full extent of actions on sites are unknown. The vendor says self-hosted UpdraftCentral was unaffected.

**Fix:** **UpdraftPlus 1.26.13 / Premium 2.26.13 or later** revoke affected connections. Check/delete old keys, inspect all previously connected sites, remove malicious plugins/accounts, reset vendor login security and reauthorize storage as advised. Updating does not remove existing backdoors.

**Unknown / technical sources:** The vendor's AI-use suggestion is an inference, not demonstrated causation. Sources: [TeamUpdraft incident and remediation page](https://teamupdraft.com/blog/security-incident-october-2026/), [Patchstack's investigation of downstream backdoors](https://patchstack.com/articles/updraftcentral-key-compromise-wordpress-backdoors/).

## 12. OVHcloud CLI release-asset substitution

**Date / evidence:** October 19, approximately **12:47–14:21 UTC** (14:47–16:21 UTC+2 in the vendor timeline).

**Description and detail:** A hijacked developer account replaced release binaries for **v0.11.0–v0.15.0** with credential-stealing builds. OVHcloud attributes the account compromise to a malicious editor extension previously installed on a personal MacBook. Source code and the build chain were not affected.

**Compromised machines / systems:** Developer identity and downloadable assets; downstream hosts executing substituted binaries. OVHcloud reports approximately **250 downloads**, not 250 confirmed infected machines. Earlier downloads of the same version numbers are unaffected.

**Impact:** Malware targeted cloud credentials, SSH keys, container configuration and AI-assistant data. Final theft and financial loss are unquantified.

**Fix:** Malicious assets removed, account suspended, repositories audited and release immutability enabled. **v0.16.0** is the clean replacement. Identify suspect binaries by vendor hashes without executing them; investigate execution and rotate exposed credentials.

**Unknown / post-mortem:** Exact downstream infection and loss counts. The vendor supplies a technical timeline and root-cause discussion. Source: [OVHcloud advisory GHSA-862f-55f5-vmvw](https://github.com/ovh/ovhcloud-cli/security/advisories/GHSA-862f-55f5-vmvw).

## 13. UTA0565 fake-news-site Chrome–Windows exploit chain

**Date / evidence:** Volexity's September 21 investigation describes attacks September 3–4, including activity at the reporting-window boundary.

**Description and detail:** Phishing links led to cloned policy/news websites carrying a chain involving **Chrome CVE-2026-85046 / CVE-2026-87491 and Windows CVE-2026-85880**. It delivered CLEANGULP malware. Volexity connects the chain to a third actor it tracks as UTA0565, separate from two actors in its September 9 report.

**Compromised machines / systems:** Windows endpoints running vulnerable Chrome, including targets in Asian government and policy-related organizations. The report gives no global machine total.

**Impact:** Espionage access through a browser-to-OS compromise; monetary loss and total stolen-data volume unknown.

**Fix:** Install current Chrome and Windows security updates and investigate the published payload indicators. Windows September updates address CVE-2026-85880; the precise update depends on OS release. This report does not supply a single Chrome version that fixes every component of the chain.

**Uncertainty / technical report:** China linkage is Volexity's attribution assessment. “Zero-day” describes exploitation before available fixes, not current patch status. Sources: [Volexity September 21 technical investigation](https://www.volexity.com/blog/2026/09/21/mind-the-patch-gap-part-2-fake-websites-used-to-deploy-chrome-windows-0-day-exploits/), [NHS England's September Windows remediation advisory](https://digital.nhs.uk/cyber-alerts/2026/cc-4846).

## 14. Kapibala / Red Heron multi-product exploitation

**Date / evidence:** GreyNoise investigation September 21; underlying activity spans May–September. The major government theft occurred in July, so this entry qualifies by its recent investigation, not a recent intrusion date.

**Description and detail:** An actor exploited WordPress and other exposed systems, pivoting with stolen credentials into a government SQL database. Separately, it exploited **CVE-2026-7273** on Zyxel GS1900 switches to steal configuration and credential material.

**Compromised machines / systems:** GreyNoise reports **49 WordPress victim organizations across 29 countries** and **996 switches across 48 countries**. Organizations are not a machine count. Victim identities are largely withheld.

**Impact:** At least **18,566 government-related records**, including plaintext passwords and personal information, reportedly extracted; switch configuration and hashed root credentials stolen. No financial-loss total.

**Fix:** Apply product-specific updates, remove backdoors and rotate stolen credentials. Zyxel's linked matrix supplies model-specific GS1900 firmware fixes. A WordPress-only update does not remediate the separate switch exposures.

**Uncertainty / technical sources:** Chinese-speaking linkage and LLM-generated tooling are researcher assessments. Sources: [GreyNoise investigation and reconstructed timeline](https://www.greynoise.io/blog/open-season-on-kapibala-attacker-steals-government-records-wordpress-exploitation), [Zyxel vulnerability and patch matrix](https://www.zyxel.com/global/en/support/security-advisories/zyxel-security-advisory-for-stack-based-buffer-overflow-vulnerability-in-gs1900-series-switches-06-16-2026).

## 15. VeloCloud Orchestrator superuser takeover

**Date / evidence:** Arista advisory October 22; vendor explicitly confirms active exploitation.

**Description and detail:** **CVE-2026-114625**, an SQL-injection issue, allows any authenticated user to gain operator privileges and impersonate a local superuser operator. It exposes privileged internal functionality and can affect the orchestrator host and managed data.

**Compromised machines / systems:** Vulnerable VeloCloud Orchestrator deployments. Assessed affected branches are 5.2.x before **5.2.3.18**, 6.1.x before **6.1.3.10**, and 6.4.x before **6.4.2.12**. Hosted, including Dedicated, deployments were affected and patched. The vendor does not give a victim-host count; end-of-support releases were not assessed.

**Impact:** Potential compromise of confidentiality, integrity and availability in network-management infrastructure. Exploitation is confirmed, but individual victims, data losses and financial impact are not disclosed.

**Fix:** Upgrade to the matching fixed release or later supported fix. Hosted customers' patching was performed by the provider.

**Unknown / technical notice:** Initial credential acquisition, campaign scope and downstream consequences. Source: [Arista Security Advisory 0199, affected versions and solutions](https://www.arista.com/en/support/advisories-notices/security-advisory/24838-security-advisory-0199).

## 16. Brotli decoder / Node.js remote-code-execution vulnerability

**Date / evidence:** Node.js security release October 21.

**Description and detail:** **CVE-2026-111497** affects the bundled Brotli decoder. Malformed compressed input is incorrectly treated as awaiting more input, allowing bytes to overflow an eight-byte internal buffer. Applications decompressing attacker-controlled Brotli data through `node:zlib` can suffer memory corruption.

**Compromised machines / systems:** Vulnerable Node.js **22.x, 24.x and 26.x** deployments that exercise the decoder. This technical advisory identifies affected software, not a compromised-machine total. Reachability depends on application behavior; not every Node.js server exposes the decoding path.

**Impact:** Possible crashes, process-memory disclosure or remote code execution. The cited Node.js release does not quantify actual victims or financial losses, or establish exploitation in the wild.

**Fix:** Update to **22.23.4, 24.22.1 or 26.12.1**, respectively, or a later supported fixed release, and restart/redeploy affected processes. Other products bundling Brotli need their own vendor updates.

**Unknown / technical advisory:** Actual compromise at any particular organization cannot be inferred from a vulnerable dependency. Source: [Node.js October 21 security releases, Brotli section and release downloads](https://nodejs.org/en/blog/vulnerability/october-2026-security-releases).

## 17. Cisco ASA / FTD SSL VPN denial of service

**Date / evidence:** Cisco advisory October 28; PSIRT says it learned of active exploitation during October.

**Description and detail:** **CVE-2026-76418** permits an unauthenticated crafted SSL VPN request to cause a firewall reload. It involves logic errors where secondary authentication is configured on a tunnel group. This is an availability attack, not evidence of remote code execution or data theft.

**Compromised machines / systems:** ASA or FTD devices running vulnerable releases with the relevant reachable VPN/configuration combination. Cisco gives no victim-device count; an affected version alone does not establish a successful attack.

**Impact:** VPN/firewall service interruption from reloads. Downtime duration, financial cost and named victims remain undisclosed.

**Fix:** Branch-specific releases include **ASA 9.20.4.50 / 9.22.3.200** and **FTD 7.4.9 / 7.6.7**; use the full vendor matrix for other branches. Cisco describes temporary configuration mitigations but warns that removing secondary authentication lowers security. Prefer the fixed release.

**Unknown / technical notice:** Campaign identity, scale and downstream operational harm. Source: [Cisco advisory, prerequisites, fixed-release matrix and exploitation statement](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-asaftd-tunnel-dos-s6mgkb75).

## 18. Microsoft 365 passkey-themed identity intrusions

**Date / evidence:** Microsoft investigation September 9; activity observed since May, with September examples.

**Description and detail:** Fake helpdesk calls/messages used passkey or SSO enrollment as a lure for adversary-in-the-middle phishing or device-code authorization. Attackers obtained sessions, registered their own authentication methods and used Microsoft Graph to discover and collect cloud data. The lure does not demonstrate a cryptographic break of passkeys.

**Compromised machines / systems:** Microsoft 365/Entra identities and accessible SharePoint, OneDrive and Exchange resources. Microsoft gives no affected-user, tenant or endpoint total. Account compromise can occur without endpoint malware.

**Impact:** Observed high-volume document access/downloads and mailbox collection; some telemetry supports only possible access or suspected exfiltration. No aggregate financial loss is established.

**Fix:** Revoke sessions/refresh tokens, reset compromised credentials, remove attacker-enrolled factors and mailbox rules, and require secure authentication re-registration. Correlate identity events with Graph and cloud-workload logs; this is an identity-response problem without a single CVE patch.

**Uncertainty / technical report:** Microsoft associates initial access with multiple actor clusters; do not attribute every intrusion to one group. Source: [Microsoft investigation, evidence limits, hunting queries and remediation](https://www.microsoft.com/en-us/security/blog/2026/09/09/passkey-themed-social-engineering-leads-identity-cloud-compromise/).

## 19. CHOSEN BRICK surveillance of dissidents and journalists

**Date / evidence:** Joint NCSC/FBI/AIVD advisory published September 15; malware used since at least 2025.

**Description and detail:** Social engineering persuaded targets to run malicious files. The Windows malware supports screenshots, microphone capture, message/email theft and additional payload downloads, with Telegram and cloud storage used for communications/exfiltration. Registry Run keys provide persistence.

**Compromised machines / systems:** Personal and organizational Windows devices belonging to targeted individuals, including in the UK, US and Netherlands. No numerical infection total is published. The advisory says automated lateral movement has not been observed.

**Impact:** Surveillance and exposure of contacts and communications. Some victims' personal details appeared on pro-Iranian leak sites, increasing personal-safety risks. Financial loss is not quantified; capabilities such as wiping should not be read as proof they were exercised on every victim.

**Fix:** Investigate using the advisory's indicators, persistence locations and signatures; keep endpoint protection enabled, restrict untrusted software, update devices and use phishing-resistant MFA. No single vulnerability patch removes an established infection.

**Uncertainty / technical advisory:** Iranian-state linkage is the agencies' assessment; individual victims and full harm remain undisclosed. Source: [joint CHOSEN BRICK technical advisory](https://www.ncsc.gov.uk/news/iranian-cyber-targeting-of-dissidents-activists-and-journalists).

## 20. Chainalysis internal-tools and customer-directory breach

**Date / evidence:** October 30 notice says unauthorized activity was detected during October.

**Description and detail:** An external actor reached internal systems/tools through what Chainalysis describes as offensive agentic techniques. The company has not published the entry point, specific vulnerabilities or the degree of AI autonomy.

**Compromised machines / systems:** Unspecified internal systems and customer-directory records: user IDs, names, emails and organization-role labels. Numbers of hosts, users and organizations were still being determined.

**Impact:** Confirmed access to those customer records. Chainalysis says it found no evidence of access to investigation content, query/transaction results, cleartext passwords, MFA secrets or session tokens. That is an investigation finding to date, not proof that every possibility has been excluded. Financial loss is unknown.

**Fix:** Patching/hardening with external experts and broader platform review. Customers are advised to enable 2FA and watch unexpected reset requests/authentication prompts. No customer-installable version fix is specified.

**Unknown / detailed notice:** Full root cause and per-organization exposure; a technical post-mortem was not present in the reviewed notice. The company explicitly says this is unrelated to Binance. Source: [Chainalysis October 30 security notice and customer communication](https://www.chainalysis.com/blog/security-incident-october-30/).

## Reading the results responsibly

The strongest numerical claims here remain attributable reports: company estimates, vendor download statistics, or researcher reconstructions. They are not interchangeable and should not be summed. For example, downloaded malware does not establish execution, possible server exposure does not establish compromise, and replenishing stolen assets does not establish recovery from an attacker.

**Analyst inference:** These entries suggest that credential lifetime, release-channel integrity, exposed management interfaces and cloud-identity persistence deserve attention alongside patching. This is a qualitative pattern across this selected sample, not a prevalence estimate. AI branding alone does not establish a novel technique, autonomous operation or a shared campaign.

**Open questions:** Several victims have not published final root causes, machine inventories, data-access boundaries or audited net losses. Private notifications and later forensic findings may materially change this report. Entries are grouped by incident/campaign; the PHP campaign is not counted again as separate PHP, kernel and firewall incidents, and the other independent supply-chain breaches are not assumed to share an attacker.
