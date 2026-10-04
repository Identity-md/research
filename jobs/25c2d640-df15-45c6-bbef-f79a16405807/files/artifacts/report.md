# IMD Ember World — R7 修復後複核

日期：2026-10-04 UTC。審查對象是 TypeScript Cloudflare Worker／React World／Auth／Member M1 的公開子集。

**裁決：Audit #1–#4 四個 Low 與 Info #5 名稱快取反例，在固定 R7 公開來源及本機合成環境中均已修復。** 本次獨立執行公開 11 檔 **386/386**，另有會員／discovery 回歸 **63 通過、3 個整檔載入失敗**，以及本次撰寫的補充控制 **9/9**。相同安全期待在公開 parent 重現失敗，沒有為了讓 parent 通過而放寬條件。這支持特定反例的 **fixed locally**，不支持完整系統、部署、真錢包或資金安全認證。

第五輪的廣義 **LOW-1／LOW-2 仍保留 partly**：本次關閉其第六輪具體反例，但跨 cookie 授權、晚到 cookie-clear、無期限 Auth 讀取與程序終止仍有限制。**LOW-3／LOW-4 保持 fixed locally**。未在已執行範圍發現另一個新的、可重現的 Critical／High／Medium／Low 缺陷；未執行與 withheld 範圍不能據此排除任何嚴重度。Completed／accepted 只代表交付，不代表批准或無漏洞。

**版本、來源與證據層級**

| 身分 | 固定值／本次可確認範圍 |
|---|---|
| PIN | `c4f451b015abdaced6c35a717b29f5bb1cb351c0`；下列 R7 程式連結均固定此 commit |
| Before | 公開 parent `445747d6a4d4fb6fa4eaa9c67b74e3e2bd9c1703`；取得公開 tar archive，未取得私有 Git 歷史 |
| Auth 修復 | `ff6bed81afe69fddfc006d9ec8e96e3e6448ecc7`，R7 團隊標示的來源 |
| 部署來源 | `e48a94f8951938f889fa3aa963c0a3e9e1df9dfd`，R7 團隊標示的來源；不是本次直接讀取的正式 Worker |
| 公開完整性實測 | 111 個 source SHA-256 全部吻合；整包 `SHA256SUMS` 190 項零不符 |
| 公開／私有對應 | manifest 記 95 exact＋16 redacted、57 mask lines；本次只驗公開 bytes。被遮罩原件指紋未提供，無法獨立驗私有原件，也不能由公開 hash 證明兩個私有 commit 的 supplied scope 相同 |

依據：[README.md:1](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/README.md#L1)、[manifests/r7-published-source.json:1](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/manifests/r7-published-source.json#L1)、[R7/PUBLIC_CONTENT.md:1](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/R7/PUBLIC_CONTENT.md#L1)；本次核對輸出 [provenance.txt](evidence/provenance.txt)。R7 聲稱上述 111 檔在 Auth 與 deployed commit **遮罩前相同**，這是團隊 provenance，不是本次公開 parent 與 R7 沒有差異。

原始第六輪 Audit 與 Report 皆已取得並核對，後續又固定至 `Identity-md/research` commit `5f3079ebbf0ff08865a0e8a1573839fa90be0b39` 再驗一次：

| 原件 | 本次 SHA-256；與 `R7/PRIOR_REVIEWS.md` 比對 |
|---|---|
| [Audit 原件](https://github.com/Identity-md/research/blob/5f3079ebbf0ff08865a0e8a1573839fa90be0b39/jobs/09062f1d-1a0b-49cb-af81-e55978798576/files/AUDIT.md#L46) | `5a905a34842b1f6a1fd003c923458f18fc0bfef1d6385b939c1e54f2404f394c`；相符 |
| [Report 原件](https://github.com/Identity-md/research/blob/5f3079ebbf0ff08865a0e8a1573839fa90be0b39/jobs/816968c0-8ff9-40a9-8e08-0e0bc4f2aef1/files/artifacts/report.md#L113) | `b5af10772e4a841682970bb570f758b40a4f755337f61592c00a7a8d3a69b122`；相符 |

對照 [R7/PRIOR_REVIEWS.md:1](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/R7/PRIOR_REVIEWS.md#L1) 與 [originals.json](evidence/originals.json)。**ReportR6-I1 與 Audit #2 是同一缺陷；Audit Info #6 是裁決矩陣，不是第六個 bug。** R5／R6／TESTS 的結果維持各自歷史版本，不拿來填補本次缺口。

以下「實測」指本次執行與保留的 raw logs；「碼讀／推論」指由指定程式得到的結論；「團隊記錄」不當成本次實測；「UNKNOWN」表示未建立足夠證據。測試沿用專案 evaluator 的部分，是獨立執行與檢視，不冒稱所有測試均由本次重新設計。

**方法與執行帳本**

Node `v24.21.0`，原生 TypeScript stripping、真 `createWorker`、公開 migrations SQL、`node:sqlite` D1 adapter。EOA keys／簽章只存在記憶體，實際簽 exact stored SIWE；provider、upstream、cookie jar、channel、clock、timer 與 headers/body gates 為合成 fixture。POST／PUT 全部在本機。無 private geometry／scene stub，未修改產品、legacy harness 或安全期待。

依 lockfile 下載 17 個必要套件，逐一驗 tarball integrity，使用普通目錄及 Node resolver hook；ESM/CJS 只轉套件路徑，不替換 handler／crypto／SQL。沒有 `npm ci`、`node_modules`、完整 Wrangler dependency junction。依賴普通檔案已封存 [runtime.tar.gz](evidence/runtime.tar.gz)，版本／integrity 在 [runtime.json](evidence/runtime.json)，包含 TypeScript 5.9.3、viem 2.56.9；SSR child 同樣繼承 loader。它不是 R7 記錄的 Node 24.19.0／完整 lock 安裝環境，也不是 Worker raw-byte rebuild 環境。

| 本次 run | pass／fail／skip；exit | 解讀 |
|---|---|---|
| `public386`，公開指定 11 檔 | **386／0／0；0** | 09:47:11.101–09:47:25.427 UTC；與記錄的公開 population 一致，無 scene stubs |
| `before-r7` 首次比較 | **65／22／0；1** | 混合 population：lifecycle 55 項確實選 parent，為 **33 pass／22 fail**；authority 32 項直接 import candidate，不能算 before |
| `before-server-cache` 修正比較方式 | **26／14／0；1** | 將 R7 authority/cache evaluator 原封不動複製至 parent `tests/`；32 authority＋8 cache。authority 23/32、cache 3/8 |
| 同 evaluator 的 R7 結果 | lifecycle **55/55**；server/cache **40/40** | 已包含於 386，不再相加；parent failure 是預期反例，非 R7 測試失敗 |
| `extra`，六檔回歸嘗試 | **63／3／0；1** | `member` 20＋`aud4-member-server` 24＋`aud4-discovery` 19 pass；`ownership`、`home-entry`、`wallet-client` 各因 withheld `households.ts` 無法載入，三個 runner failure 不等於跑過三個業務案例 |
| 本次獨立補充 `reviewer-candidate` | **9／0／0；0** | silent provider replacement、初次連線 event/reply、post-fence held body、獨立 expectedAddress cleanup |
| 同補充 evaluator `reviewer-baseline` | **7／2／0；1** | post-headers PRESENT／ABSENT 的 late-body 零清理期待在 parent 失敗 |

各 run cancelled／todo 均 0；未刪除失敗。完整命令、UTC、exit 見 [runs.json](evidence/runs.json)，原始 logs 見文末索引。`before-r7` 的 routing 誤差是本次方法修正，不能把 65/87 宣稱為完整 parent 結果；真正同源 before/after 是上列拆分結果。團隊私有 before/after 的 33/55→55/55、26/40→40/40 數字雖與本次吻合，證據來源仍分開。

公開 386 包含 79 項 `auth-lifecycle-model` 測試。碼讀其第 3 行直接 import 真 `AuthLifecycle`，因此是 controller invariants／64-seed scheduler 測試，**不是另一份完全獨立 reference implementation 的等價性證明**；parent 沒有該新增 controller，未捏造其 model before 結果。依據：[source/tests/auth-lifecycle-model.test.mjs:1](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/auth-lifecycle-model.test.mjs#L1)。

**四 Low＋cache 裁決矩陣**

「非阻斷」指這個局部反例沒有留下已重現的修復阻斷，也未證明資產／house 權限繞過；不是 production release approval。若要宣稱完整關閉廣義 LOW-1／LOW-2 或安全認證，文末 residual／UNKNOWN 仍阻斷該宣稱。

| 原始項目 | Parent → R7，同期待結果 | 裁決／阻斷性 |
|---|---|---|
| Audit #1 Low，46–68：accepted PRESENT＋held home＋stop＋late home | parent malformed 路徑撤掉已接受 session；R7 保持 live，direct-success 控制也保持 live | **fixed locally；非阻斷**，仍限 JS／合成 runtime |
| Audit #2 Low，70–93；ReportR6-I1，113–121：dead token＋exact nonce | parent 接受 expired/revoked，發 clear；R7 409、零 unauthorized rows/challenges/cookies；empty-token fallback 亦被拒 | **fixed locally；非阻斷**，不解 live-authorized late clear |
| Audit #3 Low，95–117：pre-commit read 錯放 cleanup owner | parent pre-commit ABSENT/PRESENT 釋責而 stop 無清理；R7 retain，stop 一次 cleanup，late body 不重開 | **fixed locally；非阻斷**；delivery best effort |
| Audit #4 Low，119–139：A preflight click 繼承至 B | parent B challenge＋1 prompt＋B session；R7 舊 click 零 challenge／prompt／verify，fresh click 可恢復 | **fixed locally；非阻斷**；真 provider 未驗 |
| Info #5，141–155：負 wall-clock cache age | parent 5/8 cache cases fail；R7 8/8，兩個入口都把負 age 視作過期 | **fixed locally；非阻斷**，presentation-only |
| Info #6，157–183 | 下列第五輪 Low 與 R5 矩陣 | 不是 bug，不計入修復數 |

**Audit #1：接受 PRESENT 後，舊 verify owner 不得再撤銷 session**

前提是 verify 已提交並安裝 cookie，但 2xx body 無法解析；recovery GET 成功讀到 PRESENT，之後 home read 被 hold。parent `auth.ts:419` 因 stop 改變 generation/lifetime 而再次用 closure nonce cleanup。影響是使用者已接受的登入遭意外撤銷，屬 availability／correctness，並非跨帳號授權。Parent 定位：[auth.ts:419](https://github.com/tungweb3/imd-ember-world-review/blob/445747d6a4d4fb6fa4eaa9c67b74e3e2bd9c1703/source/src/world/auth.ts#L419)。

實測順序為 GET ABSENT → challenge → `personal_sign` 一次 → verify 200/cookie → malformed body → GET PRESENT → hold home → stop → release home。Parent 在 late-home 後 created/live/revoked **1/0/1**、session cookie 消失；R7 為 **1/1/0**、cookie 保留，兩者 used/pending/invalidated **1/0/0**。R7 在 home await **之前** 已 `RELEASED`、retainedCount=0；stop 清 timer，late home 不新增 UI 通知／channel broadcast／timer arm。停止後保留的 state snapshot 不是仍掛載的 UI。

直接有效 verify body、stop/restart、舊 ABSENT/PRESENT 晚於新 accepted PRESENT、uncertain 後可信 PRESENT/ABSENT 都有控制。新實作 [source/src/world/auth.ts:272](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/auth.ts#L272)、[source/src/world/auth.ts:399](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/auth.ts#L399) 先終止 owner；[source/src/world/authLifecycle.ts:80](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/authLifecycle.ts#L80) 與 [source/src/world/auth.ts:476](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/auth.ts#L476) 使 late closure 沒有再取得 authority 的途徑。實測 [source/tests/auth-r7-lifecycle.test.mjs:15](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/auth-r7-lifecycle.test.mjs#L15)、[source/tests/auth-r7-lifecycle.test.mjs:90](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/auth-r7-lifecycle.test.mjs#L90)、[source/tests/auth-r7-lifecycle.test.mjs:287](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/auth-r7-lifecycle.test.mjs#L287)。

**不要把正常 context cleanup 誤判為 owner 復活。** 已完成 sign-in 後切換帳號，頁面可針對原顯示 session 另發 `expectedAddress`。本次補充控制實測一個 address assertion、零 nonce assertion、204，rows 1/0/1，但舊 verify owner 仍 RELEASED。新 B/A2 已取代 cookie 時，舊 nonce 沒有權力撤新 row，見 #2／#3 控制。Auth-only 案沒有 profile 操作，profile version／history／rename cooldown **N/A**。

**Audit #2／ReportR6-I1：nonce 是一致性 assertion，不是授權**

Parent [server/auth.ts:632](https://github.com/tungweb3/imd-ember-world-review/blob/445747d6a4d4fb6fa4eaa9c67b74e3e2bd9c1703/source/server/auth.ts#L632) 只以 token_hash＋nonce SELECT，dead token 仍可獲 204/cookie-clear。R7 [source/server/auth.ts:632](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/server/auth.ts#L632) 增加 `revoked_at IS NULL AND expires_at > now`；[source/server/auth.ts:640](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/server/auth.ts#L640) 用 `token !== null` 禁止「提供了空字串 token」轉成 pending-only authority。影響是未授權清理及晚到 clear 損害較新 browser context；未證明可撤掉另一 token 的 server row。

| 控制／實測 | R7 結果與 rows／cookie 語義 |
|---|---|
| expired exact nonce，original challenge retained/pruned，另一 B live＋pending | 409，零 Set-Cookie；created/live/revoked **2/1/0** 保持，expired1；used 為 2 或 pruned 後1，pending1、invalidated0 保持 |
| revoked exact nonce，同上 | 409；**2/1/1** 保持；原 challenge 保留／刪除均不賦予 dead authority |
| dead A response held → B 或同地址 A2 login＋pending → apply old headers | 409/no clear，較新 session/flow cookie identity、live row、pending challenge 均不變；這特別排除 dead-authorized late clear |
| newer B/A2 token＋old retained/pruned nonce | 409；**2/2/0**、pending1 保留；舊 A token 已遺失，不能期待此請求撤 A |
| live matching A＋exact nonce，B pending；原 challenge retained/pruned | 204，只清 A session cookie；**2/2/0→2/1/1**；B flow cookie／pending 保留且之後真的 verify 成功 |
| 無 session token＋original flow cookie＋exact pending/unexpired nonce | 204，只清 original flow；兩個 pending 中恰一個 invalidated，created0、pending1、invalidated1 |
| missing flow、newer flow、expired/pruned/used challenge | 409，rows/challenges/cookies 不變；不能僅靠 nonce 或任意 flow cookie |
| empty／forged／malformed／expired／revoked／live-other-nonce token＋本來可取消的 pending | 全部409；任何提供的 token 均禁止 pending-only fallback。Parent 的 empty token 控制也失敗，歸入同一 #2，不另算新 bug |
| 同時 expectedNonce＋expectedAddress | live／pending-only 均400，零變更 |
| expectedAddress fallback | 需 live cookie 地址相符，只選該 session 原始 flow；dead 401、mismatch409，不能以 address 單獨授權。live、missing/forged 與 pending 保護由 `auth-r5-authority` 補足 |
| 明確使用者 `/logout {}` | 保留 intentional current-cookie semantics：204，可撤當前 row、invalidated 當前 flow pending、清兩 cookies；不是自動 cleanup 的規則 |

本機 server-only fixture 的 `prompts=0` 是沒有 provider UI，setup 使用合成 EOA 簽章；不能解讀為真 wallet 沒有簽名。UI／knowledge／cleanup controller／timer／profile version **N/A**。測試含完整前後 row snapshot、cookie-preservation 判斷，而不只 status。證據：[source/tests/auth-r7-authority.test.mjs:35](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/auth-r7-authority.test.mjs#L35)、[source/tests/auth-r7-authority.test.mjs:45](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/auth-r7-authority.test.mjs#L45)、[source/tests/auth-r7-authority.test.mjs:102](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/auth-r7-authority.test.mjs#L102)、[source/tests/auth-r7-authority.test.mjs:128](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/auth-r7-authority.test.mjs#L128)、[source/server/auth.ts:651](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/server/auth.ts#L651)；[before-server-cache.tap](evidence/before-server-cache.tap)、[public386.tap](evidence/public386.tap)。

R4-01 的 `/logout-all` 是另一授權 gate：[source/server/auth.ts:680](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/server/auth.ts#L680) 先讀 live cookie，再在任何寫入前比較 expectedAddress；display A/cookie B 得409，A、B、challenge、cookies 不變。missing/dead authority401，client 不假報 all-device success，讀回失敗保留 UNKNOWN。`aud4-auth` 及原 auth 控制通過；live A 在兩 devices 的正控制則200/revoked2。此差異不能被 ordinary explicit logout 的語義抹平。

**Audit #3：fence 必須取 verify headers／transport 被觀察時的最新 read sequence**

反例必須保留順序：verify dispatch，尚未提交 → channel GET 在此時取得 ABSENT 但 hold → verify commit／cookie／headers 被觀察，body stall → 舊 GET 才到 → stop。只要求 read sequence 大於 VERIFY_START 不足，因為該 GET 仍可能先於 commit。

Parent 實測舊 ABSENT 使 knowledge=ABSENT，stop 時零 logout、rows **1/1/0**、cookie 還在；使用者畫面像 signed-out，但同瀏覽器 live session 仍能授權 M1。R7 此時 knowledge **UNKNOWN**、owner **RETAINED**，stop 在 body 仍未結束時一個 nonce logout 204，rows **1/0/1**、cookie 清除、owner **CONSUMED**。challenge used/pending/invalidated **1/0/0**，prompt1。舊 PRESENT 控制另有 setup B：R7 **2/2/0→2/1/1**，只撤 A，B row 仍 live。INVALID overlap／無 overlap 也各只有一個清理；parent 部分控制先清理成功，卻在 late body 又發一次，所以 22 個 lifecycle failure 不全是「stop 沒有清理」。

碼讀 [source/src/world/auth.ts:387](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/auth.ts#L387)／[source/src/world/auth.ts:404](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/auth.ts#L404) 在 response/transport observation 設 fence；[source/src/world/authLifecycle.ts:65](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/authLifecycle.ts#L65)、[source/src/world/authLifecycle.ts:70](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/authLifecycle.ts#L70) 要求 `readSeq > responseFence`。有效 post-fence PRESENT／ABSENT 終止 owner；invalid JSON/schema/status/transport 不能釋責。舊讀也受 generation／life／最新 readSeq 控制，不能覆蓋較新 accepted knowledge。

本次補充直接在 verify body 持續 hold 時啟動 post-headers GET：PRESENT 保持 rows1/1/0，ABSENT 正控制先由 fixture 明確 logout，rows1/0/1；兩者都 RELEASED，stop／late body 零自動 logout、零新 UI/timer/channel。Parent 同樣兩案在 late body 仍額外 cleanup，故 **7/9→9/9**。ABSENT 控制的 revoked row 是 fixture 外部 logout，不能算 controller 的副作用。[reviewer.test.mjs](evidence/reviewer.test.mjs)、[reviewer-candidate.txt](evidence/reviewer-candidate.txt)。

Early-refusal 控制尤其重要：第一次 cleanup 在 headers 前 dispatch，409 即使在 headers 後才完成也不能按完成時間算「post-fence attempt」。[source/src/world/authLifecycle.ts:86](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/authLifecycle.ts#L86) 捕捉 dispatch 時 `attemptObserved`；409 後同一 owner drain 第二次，序列 **409→204**、總 rows **2/1/1**、保留 B、prompt1，late body 無第三次。account→provider→stop／反序、重複 cancel 與 held cleanup 都只有一個 in-flight；RELEASED／CONSUMED 零可再行使的 cleanup authority。證據：[source/tests/auth-r7-lifecycle.test.mjs:43](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/auth-r7-lifecycle.test.mjs#L43)、[source/tests/auth-r7-lifecycle.test.mjs:223](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/auth-r7-lifecycle.test.mjs#L223)、[source/tests/auth-r7-lifecycle.test.mjs:255](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/auth-r7-lifecycle.test.mjs#L255)。

新 B/A2 cookie＋pending 控制：原 A uncertain → 新 session → pending → account/provider/stop → late read；R7 恰一個 original nonce cleanup **409**，created/live/revoked **2/2/0**，used2/pending1/invalidated0，兩 cookies identity 保留；pending 隨後可 verify，live3。這是正確的「拒絕跨 token 清理」，不是清理成功；CONSUMED 代表該 best-effort attempt 已終止，不代表 A row 必然撤銷。[source/tests/auth-r7-lifecycle.test.mjs:160](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/auth-r7-lifecycle.test.mjs#L160)。停止／restart 後舊 callback 不更新新 life 的 UI、hint、timer/channel；舊 channel listener 亦不發新 GET。Auth-only profile/version **N/A**。

**Audit #4：使用者 click 必須有固定 provider／account／generation／life**

實測 held initial GET → 帳號已是 A → A click → `accountsChanged(B)` → GET release。Parent 產生 B challenge、B `personal_sign` 1、verify1、rows **1/1/0**、used1、session cookie、signed-in broadcast 及 timer；不是使用者對 B 的新 click。錢包仍須批准簽章，所以不等於 signature bypass。

R7 [source/src/world/authLifecycle.ts:33](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/authLifecycle.ts#L33)／[source/src/world/authLifecycle.ts:39](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/authLifecycle.ts#L39) 固定 click lease；[source/src/world/auth.ts:327](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/auth.ts#L327)／[source/src/world/auth.ts:461](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/auth.ts#L461) 將 busy preflight 包含在取消判定。舊 click 結束時 challenge／verify／prompt／rows／used／pending／invalidated **全0**，session/flow cookies 都沒有。account/provider/lock/stop/restart 控制通過；明確 fresh click 在可信 read 後可建立一個新 flow，prompt1、row1 live、used1，正常 stop 不撤 accepted session。[source/tests/auth-r7-lifecycle.test.mjs:122](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/auth-r7-lifecycle.test.mjs#L122)。

same-account announcement 保留原 click，這不是帳號替換；held challenge 後切換零 prompt，held prompt 後切換允許已打開的 prompt 返回但零 verify。舊 channel 回呼受 life fence。另本次撰寫控制：不發 provider-change event 而換成另一 provider（不同或同地址），pending click 仍零 challenge／prompt；初次無 account 的 `eth_requestAccounts` 回覆必須與最新 event 一致，agree/repeat-agree 各允許一個 flow，disagree/lock 均零 verify。initial connect 的方法回覆是本次合成 wrapper，未把它的 connect call 數當真 UI 量測。碼讀 [source/src/world/auth.ts:240](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/auth.ts#L240)、[source/src/world/auth.ts:347](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/auth.ts#L347)、[source/src/world/auth.ts:466](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/auth.ts#L466)；實測 [reviewer-candidate.txt](evidence/reviewer-candidate.txt)。

這些控制沒有證明同一真 provider 靜默改帳號且不通知網站時，頁面必定得知；provider 說謊／真錢包 UX 屬 UNKNOWN。UNKNOWN 不能 prompt，invalid read 時 fresh click 先 GET；完整 positive/negative schema 見 R5 矩陣。此組未觸 Member，profile/version/cooldown **N/A**。

**Info #5：public-name cache 與 rename cooldown 分開判定**

[source/src/world/member.ts:195](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/member.ts#L195) 的 `publicName` 與 [source/src/world/member.ts:210](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/member.ts#L210) 的 `lookupName` 都要求 `now >= hit.at` 且 age<60000。不是將此快取改成 monotonic clock；是把負 age 視為失效。

同 evaluator 實測 parent cache **3 pass／5 fail**，R7 **8/8**：倒退1ms由 Name1 更新 Name2、GET1→2；連續倒退150000/100000/50000不固定舊名，GET合計4；age0及59999仍 hit，60000過期；pending 舊 request 不覆蓋較新 cache entry；負 age lookup 先等 **400ms** debounce，再刷新；delay 前 cancel 無 request/callback；fresh hit immediate、無 timer；503 refresh 得 null，不無限保留舊名。[source/tests/member-r7-cache.test.mjs:22](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/member-r7-cache.test.mjs#L22)。既有 `member-client` 的 late-response close 控制亦通過：停止 lookup 的 callback 不更新已關閉 panel。

此組 session created/live/revoked、challenge pending/used/invalidated、prompts 全0，cookie absent；Auth knowledge/owner、profile version／history／rename cooldown **N/A**，只有 public GET、快取及 callback。名稱從來不是 house／member write authority。rename cooldown 保留 serverTime＋monotonic elapsed 的原修補，不能因這個 wall-clock cache fix 宣稱又解了一次 LOW-4。

**保留第五輪四 Low 與 R5-01..09**

| 第五輪項目 | 第六輪原裁決 → 本次裁決 | 本次理由／界線 |
|---|---|---|
| LOW-1，R4-02/AUD4-06 | partly → **partly**（第六輪 #2 本機已修復） | nonce/live-token 與 B/A2/pending isolation 通過；lost A token、same-address renewal、live-authorized late Set-Cookie 邊界仍在 |
| LOW-2，R4-02/AUD4-06 | partly → **partly**（#1/#3 本機已修復） | accepted release／causal read fence／single cleanup owner 通過；still-running JS、offline/termination 及無 Auth deadline 不能承諾 |
| LOW-3，R4-02/AUD4-06/CORR-02 | fixed locally → **fixed locally** | strict schema、UNKNOWN 先讀、無重複 session/prompt 控制維持；真永久 stall 未 bounded |
| LOW-4，R4-08/AUD4-08 | fixed locally → **fixed locally** | monotonic estimate 只排程 server reconcile；不由裝置 wall time 解鎖；OS suspension 未實測 |

此矩陣不把 broad partly 與具體反例 fixed locally 混成矛盾，也不把 R5 九列計為九個新漏洞。歷史對應：[source/docs/security/R5_LOW_REMEDIATION.md:11](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/docs/security/R5_LOW_REMEDIATION.md#L11)。

| R5 控制 | 程式／測試 immutable file:line | 本次結果／裁決；殘留 |
|---|---|---|
| R5-01 account switch | [source/src/world/auth.ts:461](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/auth.ts#L461)；[source/tests/auth-r5.test.mjs:74](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/auth-r5.test.mjs#L74)；[source/tests/auth-r7-lifecycle.test.mjs:122](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/auth-r7-lifecycle.test.mjs#L122) | **fixed locally／非阻斷**：新 B/A2/pending 保留，held A click 取消；廣義 LOW-1仍 partly |
| R5-02 provider/newer context | [source/src/world/auth.ts:250](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/auth.ts#L250)；[source/tests/auth-r7-lifecycle.test.mjs:160](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/auth-r7-lifecycle.test.mjs#L160) | **fixed locally／非阻斷**：original nonce，不用共享 cookie 猜身分；silent/same-address provider 控制另見補充 |
| R5-03 teardown | [source/src/world/auth.ts:231](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/auth.ts#L231)；[source/tests/auth-r7-lifecycle.test.mjs:43](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/auth-r7-lifecycle.test.mjs#L43) | **fixed locally／非阻斷**：未決 owner stop 清理一次，終止 owner 不復活；程序終止保證 UNKNOWN |
| R5-04 malformed UNKNOWN | [source/src/world/auth.ts:264](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/auth.ts#L264)；[source/tests/auth-r5.test.mjs:239](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/auth-r5.test.mjs#L239) | **fixed locally／非阻斷**：invalid JSON/null/array/missing/wrong type、429/503/transport 全 UNKNOWN |
| R5-05 invalid positive schema | [source/src/world/auth.ts:268](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/auth.ts#L268)；[source/tests/auth-r5.test.mjs:214](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/auth-r5.test.mjs#L214) | **fixed locally／非阻斷**：true 必須 valid address＋positive safe-integer expiry；0、負、fractional、unsafe、NaN/Infinity wire 均不證 PRESENT |
| R5-06 GET before signing | [source/src/world/auth.ts:337](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/auth.ts#L337)；[source/tests/auth-r5.test.mjs:266](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/auth-r5.test.mjs#L266) | **fixed locally／非阻斷**：UNKNOWN 下一 click 先 GET；PRESENT 不再簽；ABSENT 才新 flow；Auth read deadline仍 open limit |
| R5-07 no duplicate session/prompt | [source/src/world/auth.ts:324](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/auth.ts#L324)；[source/tests/auth-r7-lifecycle.test.mjs:287](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/auth-r7-lifecycle.test.mjs#L287) | **fixed locally／非阻斷**：uncertain後多次壞讀仍 prompt1/live1/used1；成功讀 PRESENT 不增加，ABSENT 後新 click 才增加 |
| R5-08 backward clock | [source/src/world/member.ts:91](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/member.ts#L91)；[source/tests/member-r5.test.mjs:51](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/member-r5.test.mjs#L51) | **fixed locally／非阻斷**：wall 正負跳不改 monotonic elapsed；cache Info #5 另算；真 OS UNKNOWN |
| R5-09 timer/server reconcile | [source/src/world/member.ts:95](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/member.ts#L95)；[source/tests/member-r5.test.mjs:86](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/member-r5.test.mjs#L86) | **fixed locally／非阻斷**：deadline GET 決定 unlock，failed/invalid保持 cooling，60000ms 正 retry，舊account/life不得解鎖新 UI |

合法 ABSENT schema 僅 `signedIn===false`，`expired` 缺省或 boolean；合法 PRESENT 僅 `signedIn===true`＋40位 hex address＋正 safe integer `expiresAt`。字串 boolean、invalid address、壞 expiry、截斷 JSON 都不是 absence。wire `1e400` 解析 Infinity 也拒絕。這是對 server response 的 validation，不是任意 response 來源的權限認證。

Cooldown 實測：serverTime 與 monotonicNow 獨立於 Date.now；七日 deadline 到只發 GET，body hold 時仍 cooling，收到 server 已到期資料才 unlock，成功再 rename 才 profile v1→v2。failed 503/429/network/bad body 維持 cooling，59999ms 不重讀、60000ms retry；early timer／wall+30日不提前解鎖，late timer只 reconcile一次；switch／stop／舊同帳號 callback 不改新 view/timer。GET/timer 本身不加 profile version/history、不發 prompt、不創撤 session；為跨七日準備的 synthetic session renewal 不算 timer 副作用。[source/tests/member-r5.test.mjs:51](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/member-r5.test.mjs#L51)、[source/tests/member-r5.test.mjs:132](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/member-r5.test.mjs#L132)。模擬 callback 延後不等於實際 OS suspension 證明。

**其他 security／correctness／availability 回歸**

| 契約 | 本次證據及裁決 |
|---|---|
| Stored SIWE／Origin／nonce／replay／cookie | `auth.test` 重跑通過；server 依 stored message、challenge row／flow、簽章及 chain1 校驗，非任意 client message。[source/server/auth.ts:545](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/server/auth.ts#L545)、[source/tests/auth.test.mjs:37](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/auth.test.mjs#L37)。合成簽章不是實際 wallet 驗證 |
| R4-01 logout-all | 前述 live-cookie＋address guard 與無假 all-device-success；[source/tests/aud4-auth.test.mjs:32](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/aud4-auth.test.mjs#L32)。**fixed locally**，正式 D1 interleavings UNKNOWN |
| M1-R2／R4-06 version race | GET v0→save v1→late GET v0 不回退；GET2、late401/error、GET v2先於PUT v1、account switch 均通過。[source/src/world/member.ts:111](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/member.ts#L111)、[source/tests/member-r4.test.mjs:32](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/member-r4.test.mjs#L32)；**fixed locally** |
| R4-04／AUD4-05 五 attempt、no-op、idempotency | [source/migrations/0008_member_hardening.sql:4](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/migrations/0008_member_hardening.sql#L4) 原子 trigger＋成功 batch rollback；6/12/20 concurrent attempts 至多五 logical outcomes。same key同payload不加 slot/version/history/cooldown；異payload409；新ID同名no-op花slot不改profile；outcome race重讀 winner。[source/tests/aud4-member-server.test.mjs:170](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/aud4-member-server.test.mjs#L170)、[source/tests/aud4-member-server.test.mjs:203](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/aud4-member-server.test.mjs#L203)；本機 **fixed locally**，SQLite非正式D1證明 |
| R4-05 request/history retention | request一日、history180日是 deletion eligibility，非硬deadline；cron每表200、opportunistic10，未到期idempotency/current profile不動；backlog、缺schema、storage errors通過。[source/server/member.ts:28](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/server/member.ts#L28)、[source/tests/aud4-member-server.test.mjs:298](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/aud4-member-server.test.mjs#L298) |
| Discovery probe retention／cleanup | gate prune2、cron200、30秒scope backoff，與M1 schema清理獨立，無global probe-storage硬上限。[source/migrations/0008_member_hardening.sql:25](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/migrations/0008_member_hardening.sql#L25)、[source/tests/aud4-member-server.test.mjs:112](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/aud4-member-server.test.mjs#L112)；有界單次工作已驗，backlog／cron可用性未知 |
| R4-07 uncertain-save expiry | fetch＋body 15000ms deadline，一次exact ID/body retry；兩次未知後saving=false、per-wallet pending仍在，不能另起新logical rename猜結果；late body／switch/return控制通過。[source/src/world/member.ts:146](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/member.ts#L146)、[source/tests/member-r4.test.mjs:74](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/member-r4.test.mjs#L74)；不要把它當Auth有deadline |
| R4-03 smart-wallet write policy | [source/server/member.ts:33](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/server/member.ts#L33) 僅EOA AND ECDSA可持久寫入；CONTRACT/ERC1271/unknown403，login與existing profile read仍可用且不touch last_login。[source/tests/aud4-member-server.test.mjs:33](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/aud4-member-server.test.mjs#L33) 通過；**partly**，合法smart-wallet亦被限制，不是完整write authorization方案 |
| R4-09／AUD4-03／AUD3-02 | 80拒絕零admitted rows／index calls，另一colo可discovery；61並發上限60、12同scope只一次probe、fresh clock／缺schema／兩種denial模型通過。[source/tests/aud4-discovery.test.mjs:33](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/aud4-discovery.test.mjs#L33)、[source/tests/aud4-discovery.test.mjs:88](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/tests/aud4-discovery.test.mjs#L88)；**partly**，shared network、denial-counted local limiter、無global probe cap與backlog仍在 |
| R3-R1／N／ADV／Enter/Home | R7與補充覆蓋部分event/reply、stale read、cancel、no duplicate、late cleanup；完整 `wallet-client`／`ownership`／`home-entry` 因 withheld import 未載入。**完整重測 UNKNOWN**，未用stub或私有全套數字補齊 |
| AUD3 | auth.test 的AUD3-03、AUD3-08等保留通過；AUD3-06 dead nonce由#2修復，其他route dead-cookie拒絕控制保留。完整ownership部分UNKNOWN。**AUD3-05仍partly**（shared cookie／refresh/display窗口）；**AUD3-09仍review-limit**，不標fixed |

依據也包括 [source/docs/security/AUD4_REMEDIATION.md:11](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/docs/security/AUD4_REMEDIATION.md#L11)、[source/docs/security/AUD4_MEMBER_POLICY.md:17](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/docs/security/AUD4_MEMBER_POLICY.md#L17)、[source/docs/security/AUD4_DISCOVERY.md:37](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/docs/security/AUD4_DISCOVERY.md#L37) 及歷史 [source/docs/security/AUDIT_REMEDIATION_STATUS.md:1](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/docs/security/AUDIT_REMEDIATION_STATUS.md#L1)；文件的歷史通過數／部署描述不等於本次執行。保留這些未關閉項不是新增九個缺陷。

House authority 碼讀：[source/server/auth.ts:770](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/server/auth.ts#L770) 傳 authenticated session address，[source/server/ownership.ts:54](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/server/ownership.ts#L54) 執行 Ethereum mainnet ownerOf proof，再按 seat/activity eligibility；roster/index只是candidate，public name／publicMemberId不是權利。供應範圍內 provider calls 僅 `eth_accounts`、`eth_requestAccounts`、exact SIWE `personal_sign`（[source/src/world/auth.ts:243](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/auth.ts#L243)、[source/src/world/auth.ts:348](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/auth.ts#L348)、[source/src/world/auth.ts:380](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/src/world/auth.ts#L380)）；fixture 遇其他 wallet method 即失敗。後端 `eth_call` 是讀取，不是 wallet transaction。

不審查／不推論 Mint、Solidity、Coin E1／0007、rewards、transactions、approvals、Permit／Permit2、typed-data、batch、delegation 或 withheld 新功能；也未取回 models/textures/media、full WorldApp／scene／geometry。完整 house UI／Enter gate 因供應缺口不能認證。

**建置與部署對應：partial／team evidence**

本次沒有執行 tsc、Vite 或 Wrangler。以下是 R7 隨包保留的記錄，不冒充本次建置成功：

| R7 記錄 | 正確可得結論 |
|---|---|
| 公開 tsc `node node_modules/typescript/bin/tsc --noEmit`：exit2、16 diagnostics | 15 TS2307 withheld presentation/build imports＋1 derived TS7006；完整frontend未build。這不是global typecheck pass，也未證實產品新故障 |
| Worker首次 dry-run exit1 | sandbox ancestor-directory／entrypoint resolution失敗必須保留 |
| 同深度 dependency junction、compiler permission retry exit0 | raw **314508 bytes**，SHA-256 `afd82f506aceb57ca85ce44ff6c7e65146546d383ae2e2b2b7feca72bd23e92a`，記錄與team deployed Worker吻合；本次未獨立重建此bytes |
| 空 `dist/index.html` ASSETS fixture | 只滿足ASSETS validation，不是網站；無bundle normalization／rewrite。任意依賴realpath／checkout深度不能保證raw-byte一致 |
| 私有 Auth **1357/1357**、deployed full **1392/1392** | 兩種team population，含私有feature tests；不能取代本次386或稱為公開全套 |

依據：[R7/TEST_RESULTS.md:1](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/R7/TEST_RESULTS.md#L1)、[R7/PUBLIC_SOURCE_VALIDATION.json:1](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/R7/PUBLIC_SOURCE_VALIDATION.json#L1)、[R7/BUILD_EVIDENCE.md:1](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/R7/BUILD_EVIDENCE.md#L1)。本次 resolver/vendor layout 不具備上述same-depth junction，故 **Worker獨立raw-byte對應 UNKNOWN**；完整frontend缺件也不能自行補 geometry 來讓build變綠。

[R7/PRODUCTION_DEPLOYMENT.json:1](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/R7/PRODUCTION_DEPLOYMENT.json#L1) 團隊記 `20261004T031821Z-e48a94f`，完成 `2026-10-04T03:20:14.463Z`，Worker `6c505065-798d-4890-b7c7-0c6063d1ae9b`，deployment `49fd9f2d-271e-46e9-9f5b-a4c39fea9fe0`、traffic100%。五個 anonymous GET、四個static hashes、24 security headers、session200/`signedIn:false`/`no-store`/無Set-Cookie；三個anonymous functional viewports通過；無migration/config/header change。這些全部是 **team readback／smoke**。Bytes／GET吻合不能證明Auth wallet/concurrency、隱藏settings、未公開feature或正式D1/WAF/limiter/upstream。

本次對 `imdember.com` live GET **0次**；沒有authenticated request、真錢包連線／簽名、production POST/PUT、scan/fuzz/flood、D1 mutation、migration、deploy或messages，也沒有asset discovery/download。來源／套件下載只為公開pinned review與本機重現。故不產生本次production UTC/status/hash/header表，不能沿用團隊五GET冒充本次的兩GET額度。

**仍開放的限制與未答問題**

| 項目 | 狀態／影響及阻斷範圍 |
|---|---|
| A token被B取代 | **partly／設計權限界線**：old nonce沒有A token不能撤A；不能用修補擴大跨session權限。A仍live至其他有效logout／expiry |
| address-only same-wallet renewal | **partly**：address assertion區分不了A1/A2；uncertain verify應保留nonce。不能宣稱所有same-wallet cleanup都辨認renewal |
| live-authorized old Set-Cookie clear | **open residual／非本次新bug**：當伺服器處理時A仍有權的clear可能晚到而刪B browser cookie，B server row仍live；#2只阻止dead時才獲授權的clear |
| JS offline／process termination | **UNKNOWN／best effort**：one owner/one in-flight不保證網路送達或程序終止仍執行；阻斷「必撤銷」承諾 |
| Auth fetch/body永久stall | **open availability limit**：沒有新增bounded deadline；timeout rejection fixture不證明實際無限等待會結束；Member write15秒不可移植此結論 |
| 真provider/browser/OS／正式D1 races、cron、WAF、limiter、upstream | **UNKNOWN**：本機routes/SQL與event gates只證選定模型，不證正式runtime；阻斷全面部署／可用性認證 |
| withheld frontend／私有原件／未供應feature | **UNKNOWN／review limit**：不請求、不重建、不加stub；阻斷完整frontend與omitted-feature安全結論 |

應將後續驗收具體限定為真環境生命週期、跨tab transport、正式D1/cron/limiter與可重建部署證據；本任務沒有執行該等操作。低嚴重度標籤、測試數量、交付完成或 byte-match 都不會把上述 UNKNOWN 變成安全批准。

**證據索引與離線重現**

| ID | 證據 | 用途／限制 |
|---|---|---|
| E01 | [provenance.txt](evidence/provenance.txt)、[originals.json](evidence/originals.json) | 公開111／整包190雜湊與兩份原件fingerprints；不驗masked originals |
| E02 | [public386.tap](evidence/public386.tap) | 指定11檔原始輸出；每個R7 lifecycle/server/cache診斷有ordering、prompts、rows、cookie presence、knowledge／owner |
| E03 | [before-r7.tap](evidence/before-r7.tap) | 保留首次混合run；只其中55 lifecycle是parent，不誤算前32 candidate authority |
| E04 | [before-server-cache.tap](evidence/before-server-cache.tap) | 真parent同40 evaluator；14失敗（9 authority＋5 cache） |
| E05 | [extra.tap](evidence/extra.tap) | 額外63 pass及3 withheld import failures；無skip或scene stub |
| E06 | [reviewer.test.mjs](evidence/reviewer.test.mjs)、[reviewer-candidate.txt](evidence/reviewer-candidate.txt)、[reviewer-baseline.txt](evidence/reviewer-baseline.txt) | 本次新增9個控制，同檔跑兩版本；這兩份raw log是Node預設spec reporter，不偽稱TAP |
| E07 | [runs.json](evidence/runs.json)、[run.py](evidence/run.py) | 首輪實際command／UTC／exit；含routing誤差，不能只用run名稱判source |
| E08 | [runtime.json](evidence/runtime.json)、[loader.mjs](evidence/loader.mjs)、[prepare.py](evidence/prepare.py)、[runtime.tar.gz](evidence/runtime.tar.gz) | 17套件ordinary-file離線封存與最初取得／integrity校驗程式；重現不需要執行有network的prepare.py |
| E09 | [pinned-r7.tar.gz](evidence/pinned-r7.tar.gz)、[pinned-parent.tar.gz](evidence/pinned-parent.tar.gz) | 所用公開source archives，無私有內容／submodule；不含已安裝node_modules |
| E10 | [reproduce.py](evidence/reproduce.py)、[offline-replay.txt](evidence/offline-replay.txt)、[offline-runs.json](evidence/offline-runs.json)、[offline-counts.json](evidence/offline-counts.json)、[replay/](evidence/replay/) | 自封存檔離線重播，output在test/scratch；保留預期parent與withheld failures |
| E11 | [SHA256SUMS](evidence/SHA256SUMS) | 隨附evidence普通檔案雜湊；只證交付bytes，不證審查結論 |
| E12 | [source/docs/security/AUTH_STATE_MACHINE.md:1](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/source/docs/security/AUTH_STATE_MACHINE.md#L1)、[R7/AUTH_REMEDIATION.md:1](https://github.com/tungweb3/imd-ember-world-review/blob/c4f451b015abdaced6c35a717b29f5bb1cb351c0/R7/AUTH_REMEDIATION.md#L1) | 設計／團隊修補聲明，與本次實測分層 |

重現命令（需既有 Node24／Python3，不需網路）：`python3 artifacts/evidence/reproduce.py`。它展開封存依賴／公開source至 `test/scratch/r7-offline/`，不修改產品或補withheld檔；順序為public386、before-lifecycle、before-server-cache、extra、reviewer-candidate、reviewer-baseline，預期exit **0,1,1,1,0,1**。parent diagnostic getter原本不存在時記 legacy_NOT_AVAILABLE；缺少內部診斷不改 rows/prompt/cookie等外部期待。本次封存重播另驗交付可重現性，不將重跑案例加算為新的coverage。
