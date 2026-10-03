# IMD Ember World 第六次技術報告：四個 Low 修補與剩餘邊界

日期：2026-10-04（Europe/Berlin）；本次本機檢查在 2026-10-03 UTC 執行。範圍為非官方 TypeScript Cloudflare Worker／React World、Auth、Member M1 的安全、正確性與可用性。M1 持久保存公開 profile，不能稱整個 World 唯讀。沒有 Solidity 或新合約，也沒有金融研究。

**裁決：第五 Audit 的四個原始 Low 反例均在公開固定版本受到本機修補；不能據此宣告完整關閉所有相關要求。** 本次重跑新 96 案與既有 116 案，共 212/212 通過；把主要反例套到公開 parent，四個 Auth 探測與一個倒退時鐘探測全部失敗，具備 before/after 證據。另有本次獨立發現 **R6-I1（Info、開放）**：nonce 路徑接受仍可匹配資料列的 expired/revoked token，與「所有 dead authority 均零變更」的廣義條件不一致。它不等於可撤銷新 B session；四個原 Low 的修補與這項擴充邊界分開裁決。

完整私有來源、真瀏覽器／錢包、production 併發與 withheld presentation 未經本次驗證；R4-03、R4-09、AUD3-05 的 partly 及 AUD3-09 review-limit 均保留。沒有以 Low、測試通過或 Completed/accepted 推導認證、部署批准、零漏洞或資金安全。

## 證據身分與原件取得

**實測**表示本次親自執行；**碼讀**表示檢查固定原始碼／測試；**團隊**表示附帶紀錄而非本次執行；**推論**是有前提的結論；**未知**表示未取得／未執行。重跑團隊撰寫的測試不會使其成為獨立設計的測試；R6-I1 則由本次另寫探測。

全部 `source/...:line` 除明示 parent 外，均指 [PIN 445747d6a4d4fb6fa4eaa9c67b74e3e2bd9c1703](https://github.com/tungweb3/imd-ember-world-review/tree/445747d6a4d4fb6fa4eaa9c67b74e3e2bd9c1703)。GitHub commit API 與本機 [commit.json](evidence/commit.json) 確認 parent 為 `357668f37c75317f79ff2266795636597a707c04`。下載以 immutable commit 指定，不用 branch HEAD 作程式基準。

[公開 manifest](https://github.com/tungweb3/imd-ember-world-review/blob/445747d6a4d4fb6fa4eaa9c67b74e3e2bd9c1703/manifests/r6-published-source.json) 的 104 檔，本次逐檔 SHA-256／大小 **104/104 相符**（[integrity.json](evidence/integrity.json)）。88 exact、16 masked、57 mask lines 是 manifest 分類；16 檔的 `REDACTED` 標記文字序列與公開 parent 一致，字面標記共48行，不能把它當成全部57個遮罩位置。部分遮罩是欄位替代值；[parent-diff-index.json](evidence/parent-diff-index.json) 保存比較。公開內容相符不能獨立證明未公開的原始 blobs 或行保留比較。

完整來源 `1cc61b68b2dc14af83bf5178c9fe057452ba9b46`、private parent `54410b2f8dece71bdb2fd999c94feea6454ecfcd` 的對應為**團隊 provenance**；本次沒有私有 Git objects。3D、textures、scenes、完整 WorldApp／interior assets、私有歷史仍 withheld。已讀 README、R6/PRIOR_REVIEWS.md、TEST_RESULTS.md、BUILD_EVIDENCE.md、PRODUCTION_DEPLOYMENT.json、LIVE_MATCH.json、PUBLIC_SOURCE_VALIDATION.json 及四份指定 remediation／policy／discovery 文件；舊 R4/R5 記錄只作歷史。

依 [PRIOR_REVIEWS.md](https://github.com/tungweb3/imd-ember-world-review/blob/445747d6a4d4fb6fa4eaa9c67b74e3e2bd9c1703/R6/PRIOR_REVIEWS.md) 取得原件，而非僅採其摘要：

| 原件 | 取得入口與驗證 |
|---|---|
| Audit `e137990d-8dbc-4153-ae11-cada783827ea` | 指定 `files/artifacts/` API 404；web 工具入口不可取得。官方 [Explorer](https://explorer.imd.fun/jobs/e137990d-8dbc-4153-ae11-cada783827ea) HTTP 200，連到官方 [交付 README](https://github.com/Identity-md/research/blob/main/jobs/e137990d-8dbc-4153-ae11-cada783827ea/_identitymd/README.md)，再取得 [files/AUDIT.md](https://github.com/Identity-md/research/blob/main/jobs/e137990d-8dbc-4153-ae11-cada783827ea/files/AUDIT.md)。SHA-256 `93868411e170b03b349d7da7982293e96b8fceef6a36cfd32752c7284984aaab` 完全符合。 |
| Report `0860e448-e960-43af-9a1c-5eed9019ef04` | 官方 [files/artifacts/report.md](https://github.com/Identity-md/research/blob/main/jobs/0860e448-e960-43af-9a1c-5eed9019ef04/files/artifacts/report.md) HTTP 200；SHA-256 `920d7ff88e39d280dde9788bc6fce0d7940ff77c35645bccc0fdde1d14a9948d` 完全符合。 |

官方儲存入口用 main，但取得 bytes 受上列固定 SHA 驗證；保存於 [fifth-audit.md](evidence/fifth-audit.md)、[fifth-report.md](evidence/fifth-report.md)。第五 Report 的 aggregate 7 fixed／2 partly 沒有推翻 Audit 隨後提出的四個具體 Low。Audit 原本使用 Node22／SQL adapter 及 throwing crypto import shims 的合成 session fixture；本次則用 Node24、真實 EOA 測試金鑰簽 synthetic SIWE。兩者都不是 production wallet 證據。

## 四個 Low 的獨立關閉矩陣

「本機已修復」只涵蓋原反例及已列控制組；「阻斷」指能否接受該修補的技術主張，不是上線批准。

| 原 Low／prior ID | 原等級／影響 | 原問題裁決與阻斷 | 修補、測試、缺口 |
|---|---|---|---|
| LOW-1／R4-02／AUD4-06 | Low；錯清較新 session／challenge | **本機已修復（原反例）**；原誤撤銷不再阻斷。整體 dead-authority 零變更要求僅**部分滿足**，見 R6-I1。 | [source/src/world/auth.ts:184](https://github.com/tungweb3/imd-ember-world-review/blob/445747d6a4d4fb6fa4eaa9c67b74e3e2bd9c1703/source/src/world/auth.ts#L184)、[source/server/auth.ts:618](https://github.com/tungweb3/imd-ember-world-review/blob/445747d6a4d4fb6fa4eaa9c67b74e3e2bd9c1703/source/server/auth.ts#L618)；auth-r5:74,109；authority:57,77,98,116,124,144,165,179。2/2 live 新舊 session 保留；token 遺失的 A 不會被 nonce 撤銷。 |
| LOW-2／R4-02／AUD4-06 | Low；取消後遺留可寫 M1 的 session | **本機已修復（running JS）**；原 teardown 漏清理不再阻斷。 | [source/src/world/auth.ts:224](https://github.com/tungweb3/imd-ember-world-review/blob/445747d6a4d4fb6fa4eaa9c67b74e3e2bd9c1703/source/src/world/auth.ts#L224)、:412、:476；auth-r5:127,154,184,277,302。停止／重啟舊 callback 不更新新 UI。termination／offline 清理仍未知。 |
| LOW-3／R4-02／AUD4-06／CORR-02 | Low；誤判 absence、多簽多 session | **本機已修復**；原 schema 路徑不再阻斷。 | [source/src/world/auth.ts:84](https://github.com/tungweb3/imd-ember-world-review/blob/445747d6a4d4fb6fa4eaa9c67b74e3e2bd9c1703/source/src/world/auth.ts#L84)、:254、:328；auth-r5:214,239,266,277。UNKNOWN 下先 GET；auth fetch 無新增 bounded deadline。 |
| LOW-4／R4-08／AUD4-08 | Low；時鐘倒退延長 UI 冷卻 | **本機已修復（合成時鐘）**；原錯誤不再阻斷。 | [source/src/world/member.ts:91](https://github.com/tungweb3/imd-ember-world-review/blob/445747d6a4d4fb6fa4eaa9c67b74e3e2bd9c1703/source/src/world/member.ts#L91)、:95、:111；member-r5:51–178。monotonic 到期只觸發 GET，server 決定 unlock；真 OS／browser suspension 未驗。 |

### LOW-1：switch 必須持有原流程條件，不能借用目前共享 cookie

**前提／影響：**A verify 已提交、cookie 已套用，但回應 body 無效；recovery GET 被延後。另一分頁已將 jar 換成 B／新 A session 並取得新 pending challenge。此時帳號／provider 切換，parent 送 `{}` logout，撤掉新 session 與新 challenge，原 A 反而仍活著。屬 session 正確性與登入可用性，不是房屋／資產權限繞過。

**Before 實測：**公開 parent 在 T=1790596800000（2026-09-28T12:00:00Z 的 fixture clock），順序 `session GET → challenge → personal_sign → verify → held session GET → switch → logout {}`。account/provider 兩案皆 created/live/revoked=**2/1/1**，B pending 由1變0、invalidated由0變1；A 原 challenge 已 used，A session 未撤銷。session／flow cookie 均被清，client idle/null/unknown，舊流程提示1次。這是 request-time 問題，不需晚到清 cookie 才出現。[parent-probes.tap](evidence/parent-probes.tap)

**After 實測＋碼讀：**client 保留 flow nonce，automaticCleanup 優先送 `expectedNonce`；無 nonce 但有顯示的 session 才送 `expectedAddress`，兩者都無則不自動 logout。server 以 token hash＋nonce 定位原 session，不能只憑 nonce；新 B／同錢包新 A 的 nonce 不符回409，**2/2/0**、pending1、invalidated0，兩 cookie 保留。切換不新增提示（原 provider1、另一 provider0）；測試準備較新 session 用 harness 直接簽 synthetic SIWE，不混算成 UI prompt。

pending-only 控制：jar 仍是 A token、只有 B 新 challenge，匹配 A nonce 的清理為 **1/0/1**；只清 session cookie，保留 B flow cookie／pending challenge。隨後實際簽 B challenge 並走 verify 成功，變 **2/1/1**、pending0、invalidated0；不是只檢查一個未改欄位。原 A challenge 被 prune 也不能拿新 flow cookie 推導舊 flow。

stale A display → session read429 → switch C 的控制，用 `expectedAddress:A` 對 B cookie 回409，仍 **2/2/0**、pending1，無 cookies／rows 變更。address fallback 必須有 live matching cookie，只從該 session 原 challenge 取 flow；地址本身不是權限。但 address-only 無法分辨同錢包更新 session，因此不應宣稱完全隔離所有 same-address renewal。

[source/tests/auth-r5-authority.test.mjs:124](https://github.com/tungweb3/imd-ember-world-review/blob/445747d6a4d4fb6fa4eaa9c67b74e3e2bd9c1703/source/tests/auth-r5-authority.test.mjs#L124) 的 pending-only fallback 僅限 **NO token＋原 flow cookie＋exact pending/unexpired nonce**，只 invalidates 一個 challenge、只清 flow cookie、不建／撤 session。有任何 token 即禁止 fallback；missing/forged/newer flow、wrong nonce、expired/invalidated/pruned/used challenge 都不能落入成功分支。兩個 assertions 同時出現400；使用者明確 `/logout {}` 仍作用於目前 cookie。dead token 的 matching-session nonce 路徑另見 R6-I1，不能與「dead token 不得 fallback」混為一談。

晚完成／same address＋same expiry 控制 [source/tests/auth-r5.test.mjs:339](https://github.com/tungweb3/imd-ember-world-review/blob/445747d6a4d4fb6fa4eaa9c67b74e3e2bd9c1703/source/tests/auth-r5.test.mjs#L339)、:373 檢查清理後 readback，而不把 address/expiry tuple 當 session identity。先撤 A1、早到清 cookie，再建立 A2，舊 body 到達時只重新核對 cookie；A2 row 保留，最終真實 readback 決定 owner。無法 retroactively 收回已送出的 Set-Cookie；如果舊清除 header 最後到達，可刪新 cookie但不撤新 session row，讀回會移除 stale owner evidence。不能恢復「禁止所有後續 GET」或「一律撤新 session」的舊測試期待。

Auth 案沒有 M1 route，profile version/history/cooldown **N/A**；UI home evidence、sessionKnown、channel、timer 由 auth state/lifetime 控制，並不代表完整 React scene 已驗。

### LOW-2：UNKNOWN idle 仍有清理責任；停止不代表請求消失

**前提／影響：**verify 的 row/cookie 已提交，body 損壞；recovery 尚未可信，頁面 teardown。parent gen 改變後只 return，留下仍可作 EOA M1 寫入的 session 到 expiry／授權 logout。

**Before 實測：**T 固定，`GET → challenge → sign → verify → held GET → stop → release`，沒有 logout；created/live/revoked **1/1/0**、used challenge1、pending0、invalidated0，session cookie仍在。client idle/unknown/null，不多簽但不是安全清理。[parent-probes.tap](evidence/parent-probes.tap)

**After 實測：**同序列 stop 會 nonce-bound cleanup；matching A 為 **1/0/1**、session cookie清除、session GET signedIn:false，原 used challenge不改。新 B 先替換 A token／帶 pending challenge 時，則 **2/2/0**、pending1、invalidated0、B兩 cookie保留，因沒有 A token 就沒有撤 A 的權限。這項保留是必要保護，不應為追求「A永不殘留」改成撤 B。

責任保存在 flow.uncertain，跨越 verifying 到 **failed recovery → UNKNOWN idle**；account、provider、stop 三種事件都測 matching A／newer B。failed verify transport／malformed body 與 failed read 在 auth-r5:154、aud4-auth:70,97,126 覆蓋；definite non-OK verify 不當作已提交成功。

stop/restart 將 `life`、generation、讀取序號隔離；held body、舊 cleanup 的409以及 preflight late204 不得改新 subscriber、channel、expiry timer 或 hint（auth-r5:184,302）。正常讀到並接受 **PRESENT** 會清責任；其後正常 stop **不撤已接受 session**。可信 **ABSENT** 也清責任，下一 click 可開一個新 flow。這兩個控制避免修補變成每次離頁都登出。

UI stop 時同步歸 idle 與取消 timer 是預期；測試禁止的是停止後的舊非同步更新。提示維持1，不因 cleanup 新簽；沒有 member route，profile/version/cooldown **N/A**。清理是 still-running JS 的 best effort，process kill、offline、封包遺失不保證送達，也沒有新增 auth fetch deadline。

### LOW-3：只有兩種合法 session schema 能结束 UNKNOWN

**前提／影響：**verify 已存 session，而 recovery 回無效資料；parent 把某些 parsed JSON 當 absence，造成下一 click 再簽並留下第二個 session。

**Before 實測：**T 固定；verify body `{`、recovery `{}`。第一次之後 created/live/revoked **1/1/0**、prompts1，client 卻 sessionKnown=true/session=null。下一 click 直接 challenge／sign／verify，沒有先 session GET，變 **2/2/0**、prompts2，兩個 challenge used，新 cookie取代舊 cookie而舊 row仍live。

**After 判定：**只有 record `signedIn===false`（expired 缺省或 boolean）證明 ABSENT；或 `signedIn===true`＋有效40位十六進位地址＋正 safe-integer expiresAt 證明 PRESENT。這是格式正確性 gate，不把第三方傳入地址當伺服器授權。空物件、null、array、缺欄位、wrong signedIn/expired type、bad address、零／負／小數／unsafe expiry、NaN wire、±infinity、truncated JSON、429/503/network/timeout rejection 皆維持 UNKNOWN。NaN literal 是無效 JSON；`1e400` 雖是合法 JSON number literal，解析成 Infinity 也必須拒絕。

**實測結果：**[source/tests/auth-r5.test.mjs:239](https://github.com/tungweb3/imd-ember-world-review/blob/445747d6a4d4fb6fa4eaa9c67b74e3e2bd9c1703/source/tests/auth-r5.test.mjs#L239) 的表列案例，在第一次及下一 click 的 failed GET 期間均 **1/1/0**、prompts1；不發新 challenge、不多建session，原 used challenge1、pending0。恢復有效 PRESENT 後 GET/session＋home 可回復而不用 personal_sign；有效 ABSENT 才允許一個新 flow。有效 read 清除 retained uncertain responsibility；正常 stop不再自動撤 accepted session（:266、:277）。時間排序由 gate固定，不是依 real network 速度碰巧通過。

UI UNKNOWN 不是 signed-out 的證據，owner/home 的恢复只依可信讀回；無 M1操作，profile/version/history/cooldown **N/A**。timeout 案是注入 rejection，不是證明真 fetch/body 永久 stall 有 bounded waiting；這個可用性未知仍保留。

### LOW-4：單調 elapsed 只安排刷新；serverTime 才決定可改名

**前提／影響：**profile v1 有七日 nextNameChangeAt，client 的 Date.now 倒退。parent 的 serverTime＋wall delta 被 clamp/rearm，使 server 已到期仍不能改名；它不會繞過 server cooldown。

**Before 實測：**同一 member-r5:51 探測放到 parent：先 save v1；wall 往後三日，server獨立越過七日，monotonic/timer到達七日；預期增加一次 GET，實際不增加而重設 timer，探測失敗。原 Audit 更窄的 D−1000ms／倒退一天／timer+1000ms 案顯示同一原因；該具體1000ms數據是前輪原件，不冒稱本次重跑數據。

**After 實測：**timeBase={serverTime, performance.now()}，與 Date.now／legacy now injection分開。monotonic七日−1ms仍 cooling；+1ms恰好 GET。body held時仍鎖，接受 server `nextNameChangeAt:null` 後才 unlock；再 save成功為 **v2**。正向wall+30日與early timer不提前 GET/unlock；server仍拒絕 premature PUT，profile history維持1。

[source/tests/member-r5.test.mjs:86](https://github.com/tungweb3/imd-ember-world-review/blob/445747d6a4d4fb6fa4eaa9c67b74e3e2bd9c1703/source/tests/member-r5.test.mjs#L86) 分別 inject503、429、network、壞body，失敗保持 cooling，正 **60000ms** retry；59999ms不發第二次 GET，+1ms重新讀回成功才解除。server仍cooling會重新 anchor未來 deadline；晚九日 callback只 reconcile一次，不補發每個漏掉的interval。stop、switch、same-account refresh使舊run失效；held A response不能改B profile、timer或cooling（:132–166）。

計時／GET本身不創建或撤銷session，不簽名、不寫cookie、不增加profile version/history/request；測試準備用 synthetic login並在第六日續期以跨七日，這些 setup sessions不能算作timer副作用。成功新rename才增加version/history及新cooldown；Auth channel N/A，MemberClient只處理profile store與timer。無 real wallet prompt；不是實際 background tab、OS clock或suspension實驗。停止後callback零新GET，不代表終止瀏覽器仍能執行清理。

## R5-01..09 行為矩陣（不是九個漏洞）

以下測試 path 全部在 PIN 的 `source/tests/`；七檔最終212案包含這些斷言。共同缺口為 withheld full frontend／real wallet／production runtime。

| ID | 對應 Low | code file:line；test file:line | outcome／裁決／特定缺口 |
|---|---|---|---|
| R5-01 account switch | LOW-1 | auth.ts:184,464；auth-r5.test.mjs:74,109,154 | 新B/A2與pending保留，本機已修復原情境；A token遺失不能撤A；R6-I1另列。 |
| R5-02 provider switch | LOW-1 | auth.ts:244；auth-r5.test.mjs:74,154 | nonce-bound cleanup，409不改新jar，本機已修復；沒有assertion不自動logout。 |
| R5-03 teardown | LOW-2 | auth.ts:224,412,476；auth-r5.test.mjs:127,184,277,302 | matching A撤銷，新B保留，舊life無新UI/channel/timer/hint；本機已修復，delivery best effort。 |
| R5-04 malformed UNKNOWN | LOW-3 | auth.ts:254；auth-r5.test.mjs:214,239 | `{}`／null／array／壞JSON不證absence；本機已修復。 |
| R5-05 positive schema | LOW-3 | auth.ts:84–86,261；auth-r5.test.mjs:214,239 | 地址與positive safe integer expiry gate；本機已修復，不代表server response來源可被任意信任。 |
| R5-06 GET before sign | LOW-3 | auth.ts:328；auth-r5.test.mjs:239,266 | UNKNOWN點擊先GET，PRESENT不簽，ABSENT一flow；本機已修復，auth read無bounded deadline。 |
| R5-07 no duplicate | LOW-3／LOW-2 | auth.ts:321,398,412；auth-r5.test.mjs:239,277 | unknown prompts1/live1，恢復不增session；本機已修復；不同tab自行登入不算此流程重複提示。 |
| R5-08 backward clock | LOW-4 | member.ts:91–97；member-r5.test.mjs:51,63,168 | wall正負跳不改elapsed；本機已修復，真OS未知。 |
| R5-09 server reconcile | LOW-4 | member.ts:101–113；member-r5.test.mjs:74,86,110,120,132,148,160 | timer只GET；60s重試、stale隔離；本機已修復，實際suspension未知。 |

此表的 auth.ts／member.ts 指 `source/src/world/`；server 分支見四Low矩陣。原四Low裁決與行為分解不能相加成13個漏洞，也不能把九列pass當整體認證。

## R6-I1：matching nonce 的 dead token 仍可完成清理

**Info；開放；非資產／house authority阻斷，但阻止接受廣義「dead一律零rows/cookies」結論。** prior關聯 LOW-1／R4-02／AUD4-06；不是已證實的新增跨session撤銷漏洞。[source/server/auth.ts:632](https://github.com/tungweb3/imd-ember-world-review/blob/445747d6a4d4fb6fa4eaa9c67b74e3e2bd9c1703/source/server/auth.ts#L632) 的 SELECT只比 token_hash與nonce，沒有 expires_at／revoked_at predicate；:661 UPDATE與:664清cookie仍可執行。address分支:653則呼叫live readSession。

**本次獨立實測：**[dead-token-probe.mjs](evidence/dead-token-probe.mjs) 使用真Worker、SQLite migrations、合成EOA登入後，分別推進8日到expired，或將該row標revoked。送original nonce與matching dead cookie，expired回204／Set-Cookie1、revoked_at由null變1791288000000；revoked回204／Set-Cookie1、原revoked_at保持1790596799999。同條件改送expectedAddress兩案皆401、Set-Cookie0、row不變。live兩種assertion皆204正常清理。[六組輸出](evidence/dead-token-probe.jsonl)

每個獨立fixture建立session1／used challenge1／pending0／invalidated0；expired清理前created/live/revoked=1/0/0，後1/0/1；revoked前後1/0/1。清理無新signature/prompt/session，profile/version/cooldown與UI/channel/timer **N/A**（直接route探測）。沒有簽入第二帳號，故不宣稱這六組證明可影響B。程式匹配nonce保護仍阻擋dead token配另一nonce的pending-only fallback；原36 authority案測的是該種控制，沒有涵蓋matching dead nonce。

**影響推論：**目前較像重複清理的冪等語義與驗收契約不一致；到期session本來已無M1權限。它仍送出可晚到的cookie-clear，需保留既有transport race，但未證實新的權限提升或額外跨帳號資料修改。若要求dead也完全無副作用，需對nonce branch加入live條件並測matching expired/revoked；若維持冪等清理，應明示例外，不能宣稱所有dead都零cookies。本任務為review，未修改target程式或為了綠燈弱化assertion；探測斷言記錄實際行為，不是期望修補已通過的測試。

## 相關回歸與既有未關閉項

| 契約 | 本次證據與裁決 |
|---|---|
| R4-01／AUD4-01 | [source/server/auth.ts:672](https://github.com/tungweb3/imd-ember-world-review/blob/445747d6a4d4fb6fa4eaa9c67b74e3e2bd9c1703/source/server/auth.ts#L672)；aud4-auth:32,47,57。display A/cookie B在revocation前409 ACCOUNT_CONTEXT_CHANGED，無row/cookie改動；讀回失敗不假報all-device-success。matching、missing、forged、expired authority控制通過。與R6-I1不同，是logout-all的live授權。 |
| Stored SIWE／session | server/auth:545–553；auth.test:37,88,108,125,137等在既有116案內。exact stored SIWE欄位／row equality、Origin、nonce、flow、replay、cookie flags與簽章驗證實測通過；合成keys不代表真wallet。 |
| M1-R2（獨立於M1-R1） | member-r4:32,41,54,64；member.ts:111,119,155。舊GET v0→PUT v1→晚GET不回退；GET2、late401/error、v2先於PUT v1、switch均通過。本機已修復UI版本排序；不是DB rollback修補。 |
| Atomic五attempt／no-op／idempotency | [source/migrations/0008_member_hardening.sql:4](https://github.com/tungweb3/imd-ember-world-review/blob/445747d6a4d4fb6fa4eaa9c67b74e3e2bd9c1703/source/migrations/0008_member_hardening.sql#L4)、server/member.ts；aud4-member-server:170,195,203,214,226,236,244,274。6/12/20競態最多五logical outcome，成功batch與outcome回滾；同ID同payload不加version/history/cooldown，新ID同名no-op花slot不mutate。本次通過；SQLite adapter非production D1 isolation證明。 |
| Retention／probe cleanup | aud4-member-server:112,127,145,298,311。request一日／history180日是deletion eligibility；cron200/table、opportunistic10，probe2／cron200。缺schema與backlog控制通過，沒有硬刪除期限或無限吞吐保證。 |
| Uncertain-save | member-r4:74–151；member.ts:44,146。fetch＋body15秒deadline，一次exact ID/body retry；兩次未知釋放saving並保留per-wallet pending，不許新logical rename。通過；不把Member寫入deadline套用到Auth讀取。 |
| R4-03／AUD4-02 | server/member.ts:33；aud4-member-server:33,46。只有EOA AND ECDSA persistent write；CONTRACT/ERC1271/unknown寫403，login／existing profile read保留且不touch。**partly**：合法smart wallet也被限制，未解持久寫入授權政策。 |
| R4-09／AUD4-03、AUD3-02 | aud4-discovery 19案在額外63案內。80個拒絕不占admitted跨colo容量、原子probe／admission及61-race、fresh clock、缺schema控制通過。**partly**：refusal-counted本地limiter、共享network、probe無global storage ceiling及backlog仍有可用性風險。 |
| R3-R1／N／ADV／Enter/Home | 碼讀auth:232,321,464、homeEntry:11，並由新96案覆蓋部分switch、generation、no-duplicate及late-cleanup控制。完整wallet-client／ownership檔因withheld households.ts載入失敗，本次沒有重現全部舊項；**完整重測未知**，不能借私有1183冒充本次通過。 |
| AUD3 | auth.test中的AUD3-03、AUD3-08及新清理讀序控制可重跑；AUD3-01的完整ownership套件無法載入。**AUD3-05仍partly**（共享cookie／刷新／顯示窗口）；**AUD3-09仍review-limit**，不是已修好的漏洞。其他歷史fixed結論不自動升級成本次全驗。 |

額外server四檔嘗試結果為64 runner項：63 pass、1檔載入fail；其中 member20＋aud4-member-server24＋aud4-discovery19，ownership本體沒執行。授權、quota、profile版本、retention等code未因本輪Auth／clock修補改變；這是維持原契約的證據，非全部未知漏洞的排除。

**房屋授權碼讀：**[source/server/ownership.ts:54](https://github.com/tungweb3/imd-ember-world-review/blob/445747d6a4d4fb6fa4eaa9c67b74e3e2bd9c1703/source/server/ownership.ts#L54)、:280及server/auth傳入已認證address，依Ethereum mainnet ownerOf＋eligibility；roster/index是candidate，publicMemberId／名稱不是house authority。client provider calls在auth:237,344,379僅 `eth_accounts`、`eth_requestAccounts`、經siwe.ts逐行核對的exact server-SIWE `personal_sign`。公開程式範圍沒有新增 Mint、Solidity、E1／0007、rewards、transaction、approval、Permit／Permit2、typed-data、batching、delegation或session key能力。後端eth_call讀取不等於wallet交易；未公開UI不能由陰性字串搜尋保證。

## 執行記錄、失敗、shims 與未執行項

本次Node **v24.21.0**；沒有npm ci或寫node_modules。依PIN lock取得17個必要package，核對registry tarball integrity，展開成普通vendor檔並保存壓縮包。Node resolver hook只調整套件路徑與CJS解析，不替換crypto、handler或scene；SSR fixture原本用TypeScript transpileModule，仍使用它。使用真Worker/routes/migrations、node:sqlite D1-shaped adapter（batch transaction），真合成EOA簽SIWE；provider/upstream/timer/cookie jar均fixture。沒有scene import stubs。這不是原樣npm-ci／Wrangler layout。

| 本次 run | pass／fail／skip | exit／解釋 |
|---|---|---|
| 新3檔 | **96／0／0** | 0；Auth49＋authority36＋cooldown11，[new-tests.tap](evidence/new-tests.tap)。 |
| 公開parent主要5探測 | **0／5／0** | 1；預期before反例，四Auth＋backward clock；非新版本失敗。 |
| 既有4檔初跑 | **111／5／0** | 1；5個SSR child缺typescript等環境依賴；[首次紀錄](evidence/existing-tests.tap)。 |
| 補17套件並向child傳hook | **111／5／0** | 1；CJS nextResolve收到file URL找不到react；[第二次紀錄](evidence/existing-tests-retry.tap)。 |
| 改用絕對filesystem path後重跑 | **116／0／0** | 0；[最終紀錄](evidence/existing-tests-final.tap)。最終七檔96＋116＝212，兩組不重疊。 |
| 額外server回歸 | **63／1／0** | 1；ownership檔因withheld households.ts import失敗；[紀錄](evidence/server-regressions.tap)。其他63案成功，未冒稱64功能案例全跑。 |
| wallet-client focused嘗試 | **0／1／0** | 1；相同withheld import，整檔無法載入；[紀錄](evidence/wallet-withheld.tap)。pattern未選case不算skip／已執行。 |
| 獨立R6-I1 | 六情境斷言完成 | 0；不是node:test六個case；測的是實際語義而非修補通過。 |

各node:test run cancelled/todo均0。首次錯誤已診斷、修復loader並重跑；缺private presentation不能從公開來源修復而保持相同scope，因此保留blocked checks。另有工具準備失敗：官方Audit錯目錄／猜測檔名404、web不可取得，最後由官方README找到hash匹配原件；`python`不存在改用`python3`；不存在的global npm目錄未當作套件已安裝。沒有為取得成功而修改產品或抹去失敗。

本次**沒有**跑tsc、Vite frontend、Wrangler Worker rebuild、完整1183、production D1或live HTTP；本次production GET數 **0**，無登入／簽章／POST／PUT／scan／fuzz／flood／transaction／D1變更／deploy。上列POST/PUT都在本機synthetic fixture。沒有Solidity，Slither不適用。

**團隊紀錄另列，不與本次混算：**[R6/TEST_RESULTS](https://github.com/tungweb3/imd-ember-world-review/blob/445747d6a4d4fb6fa4eaa9c67b74e3e2bd9c1703/R6/TEST_RESULTS.md) 記私有local gate與formal deploy gate各 **1183/1183**、零skip，tsc/Vite pass；兩次同population不是2366 unique。早期dry-run exit1在tests/tsc/Vite已pass後因sandbox Wrangler ancestor path refusal；isolated retry exit0、**無upload**。formal deployment是另一次有upload的gate，不可倒寫dry-run為成功部署。

[PUBLIC_SOURCE_VALIDATION.json](https://github.com/tungweb3/imd-ember-world-review/blob/445747d6a4d4fb6fa4eaa9c67b74e3e2bd9c1703/R6/PUBLIC_SOURCE_VALIDATION.json) 記公開七檔212/212（96＋116），不是1183；public tsc **exit2／16 diagnostics**＝15 TS2307 withheld presentation imports＋1 derived TS7006。完整frontend withheld／未build。首Worker compile AccessDenied；deeper layout成功但 **314846B**，與目標差 **399B／133 relative labels**；第三次same-depth raw rebuild **314447B／SHA匹配**。fixture只有empty dist/index.html供ASSETS validation；**沒有normalize或rewrite bundle**。任意checkout/npm-ci layout不保證同bytes。本次沒有重建來獨立驗證團隊bundle比較。public failures、withheld fixtures與private1183分層保留；舊R5的239／419等歷史數字不充作本輪結果。

## 部署對應：部分團隊證據，不是 repaired-flow 證明

依固定 [BUILD_EVIDENCE](https://github.com/tungweb3/imd-ember-world-review/blob/445747d6a4d4fb6fa4eaa9c67b74e3e2bd9c1703/R6/BUILD_EVIDENCE.md)、[PRODUCTION_DEPLOYMENT.json](https://github.com/tungweb3/imd-ember-world-review/blob/445747d6a4d4fb6fa4eaa9c67b74e3e2bd9c1703/R6/PRODUCTION_DEPLOYMENT.json)，團隊部署source `1cc61b68b2dc14af83bf5178c9fe057452ba9b46`，record **20261003T214856Z-1cc61b6**，UTC21:48:56.252–21:50:27.782；Worker **5022cd62-6f1f-444c-af94-3b68ec359b94**，314447 bytes，SHA-256 **3977c6db6cbff23e9f6aec87092a236c603eac8bf64a7ce0c825d400dd1ad7dd**。traffic API記deployment `665f9e0a-8ae6-4a09-ac0d-e919d09fb60c`、100%到該版本。此為團隊allowlisted metadata，本次沒有查Cloudflare帳戶或取得raw bundle。

團隊 [LIVE_MATCH.json](https://github.com/tungweb3/imd-ember-world-review/blob/445747d6a4d4fb6fa4eaa9c67b74e3e2bd9c1703/R6/LIVE_MATCH.json) 的五GET在 **2026-10-03T21:51:47.506Z–21:52:11.967Z**，間隔至少5秒，**5/5 HTTP200**：

| route | bytes／SHA-256（團隊紀錄） |
|---|---|
| `/` | 2634／`3bcd74f4f4d29675d8a6db2e365830e9f4048cf95bc9c3ebb7b14a08146415df` |
| `/assets/index-COJsvXGn.js` | 1490500／`01650467076461ed932fa45b8c5a25aff670f327e3f49d92ceee592fef3a1eca` |
| `/assets/InteriorView-By3aPoX4.js` | 93242／`c5eec32a6b6b59cb299ad7e30f1eeec68962fbaac6113e16bd77b40f7fd34815` |
| `/assets/index-BZpalHf7.css` | 58227／`6799cd5de49639b854270820c090bf5983b22d7d81b58818b9a427e48c1152ec` |
| `/api/auth/session` | 18／`60483fbb3c01c4080583563e215e3ca4ab5ce4ff74f47cf36eadedd152572d2f`；signedIn:false、no-store |

四static hashes、每檔六項headers共 **24/24** 匹配；五回應無Set-Cookie。headers包括nosniff、strict-origin-when-cross-origin、permissions-policy、HSTS、DENY與CSP；精確值與各UTC見JSON，不把session不同header集合混入24項。

D1 pre/post選定metadata一致，migration **0001–0006＋0008**，沒有0007或新migration。這不是新production parallel-write測試，也不驗證cron throughput、binding實際指向或WAF/limiter accounting。舊R5部署屬歷史，不能代替此Worker。匿名GET／byte comparison只支持部分來源與公開回應對應，不能證明四個修補流程、UI/wallet UX或production D1 concurrency；102個private frontend檔也未全部抓取。

## 未回答問題與驗收界線

仍未知：real browser/OS wall correction與suspension、wallet/provider事件及UX、full WorldApp client lifetime、production D1 concurrency/RETURNING/bindings、WAF與limiter拒絕計法、upstream／跨network可用性、cron backlog與未公開內容。Auth讀取無新bounded deadline，永久stall仍可能阻塞；Member PUT的15秒保護不能抵銷此點。

已知限制不可刪：B替A token後nonce不能撤A，A可能活到授權logout或expiry；address-only不能區分same-wallet renewal；舊Set-Cookie清除晚到可能刪新cookie但不撤新row；teardown只在可執行JS時best effort；R4-03 policy、R4-09 availability、AUD3-05 partly、AUD3-09 review-limit維持。M1公開名稱可連結wallet，名稱不是官方身份／house authority；同源惡意程式及真SIWE relay信任邊界沒有因本輪修補消失。

交付含[證據與離線重現索引](README.md)。文件存在／hash／格式檢查只驗輸出完整性；本次評估提供可歸屬的本機證據與限制，不是另一位獨立reviewer的背書，也不是部署或資金安全批准。

## 交付大小修復補記（2026-10-04）

前次 upload 檢查因 source bundle 13,891,146 bytes 超過 8 MiB 而失敗，這是交付封裝失敗，不是產品行為失敗。此次只精簡離線測試依賴中的開發型別／maps／未使用 TypeScript CLI，保留 runtime、licenses、產品來源與全部既有證據；封存檔同步更新。原依賴下載 integrity 只證明當時取得的完整 tarball，不代表精簡樹。重現範圍與修復後驗證見 [README](README.md) 及 [bundle-check.json](evidence/bundle-check.json)。此處的重跑不增加獨立測試案例數，也不提升 production／private 證據強度。
