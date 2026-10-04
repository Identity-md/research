# IMD Ember World — Submission7_R8Closure／R8 v1.1 閉合覆核

## 主報告（2026-10-04 pinned cutoff）

### 結論

**是，但僅限來源層、指定範圍與已供應的離線反例：此 exact candidate 足以把 R8 v1.1 的 LOW-1～LOW-6 與可處理的 INFO-1～INFO-2 判為 `fixed locally`；第九項 Info 是裁決矩陣，不是缺陷。**我未在 Auth／session lifecycle／server gates、ownership freshness、相關 cache／market 數值邊界找到新的可重現 scoped regression（任何嚴重度）。這個結論不預測 Swarm 接受、不建立 `WORLD_SECURITY_BASELINE_v1`，也不等於全產品、資金安全或零漏洞認證。

對象是公開快照 `7215c5d89a96bc79113a85766c04868d54393f3c` 所指向、manifest 宣稱對應私有來源 `8a22b51035c965b9df2fe010e3ac0a780581b0e2`、parent `f9a34cba0876306287b35aff0176e9dc38942624`。公開 manifest 有 128 個來源檔，其中 112 byte-exact、16 redacted；因此「公開 bytes 與私有 commit 完全相同」仍是團隊 provenance claim，而非我能由私有 Git 獨立證明的事實。[manifest](https://github.com/tungweb3/imd-ember-world-review/blob/7215c5d89a96bc79113a85766c04868d54393f3c/manifests/submission7-r8closure-published-source.json) [inventory](https://github.com/tungweb3/imd-ember-world-review/blob/7215c5d89a96bc79113a85766c04868d54393f3c/Submission7_R8Closure/PUBLIC_CONTENT.md)

### 八項裁決

| 項目 | 本次裁決 | 阻斷判斷 |
|---|---|---|
| LOW-1 accepted PRESENT／切換 | **fixed locally，Low** | PRESENT 在 home I/O 前釋責；切換仍以 displayed `expectedAddress` 作獨立清理，terminal nonce 不復活。非來源阻斷。 |
| LOW-2 sibling／每次 click receipt | **fixed locally，Low** | 每次 click 自己做 canonical GET；壞 schema、429、503 都 UNKNOWN/fail-closed；matching PRESENT 零新 prompt/challenge/verify，hint 只觸發重讀。非阻斷。 |
| LOW-3 pure cleanup plan | **fixed locally，Low** | 每 EVENT 一個 primary；displayed address 優先於 pending／retained nonce；同地址舊 nonce 與新 row 不被誤認為同一 session。非阻斷。 |
| LOW-4 stop／cleanup／restart | **fixed locally，Low** | detached completion 只要求現 lifetime canonical reread，不寫舊 UI；busy 時排隊，舊 cleanup 不能 cross-revoke 新 row。非阻斷。 |
| LOW-5 ownership epoch／成本 | **fixed locally，Low** | 只有 authenticated-address `ownerOf` 授權；proof 30 秒獨立於 index，完成時重看 clock，256 attempted-ID cap 包含 failed delta；limited/unavailable 不冒充 empty/not-owned。非阻斷。 |
| LOW-6 freshness／倒退時鐘 | **fixed locally，Low** | 共用條件為有限值、正 TTL、`0 <= age < TTL`；rollback、future、NaN、Infinity 與 exact expiry fail closed。非阻斷。 |
| INFO-1 wallet LOCK | **fixed locally，Info** | lock 取消 click；uncertain verify 只在 post-fence canonical read 後 reconcile，不自動撤 committed session；503 後有效 PRESENT 可釋責。非阻斷。 |
| INFO-2 market numbers | **fixed locally，Info** | 價格、floor 與乘積必須有限且有效；壞 optional 數值移除，合法負 change 保留。僅顯示面，非阻斷。 |

實作交叉點可見：PRESENT receipt 在 home await 前完成，[`auth.ts` L292-L312](https://github.com/tungweb3/imd-ember-world-review/blob/7215c5d89a96bc79113a85766c04868d54393f3c/source/src/world/auth.ts#L292-L312)；每次 click 的 own read 與 UNKNOWN gate 在 [L379-L393](https://github.com/tungweb3/imd-ember-world-review/blob/7215c5d89a96bc79113a85766c04868d54393f3c/source/src/world/auth.ts#L379-L393)；pure planner 的 displayed／owner／local-cancel 優先序在 [`authCleanup.ts` L14-L24](https://github.com/tungweb3/imd-ember-world-review/blob/7215c5d89a96bc79113a85766c04868d54393f3c/source/src/world/authCleanup.ts#L14-L24)；detached cleanup reread在 [`auth.ts` L195-L228](https://github.com/tungweb3/imd-ember-world-review/blob/7215c5d89a96bc79113a85766c04868d54393f3c/source/src/world/auth.ts#L195-L228)。ownership 的完成側 clock、舊 epoch、failed delta 與 cap 在 [`ownership.ts` L271-L296](https://github.com/tungweb3/imd-ember-world-review/blob/7215c5d89a96bc79113a85766c04868d54393f3c/source/server/ownership.ts#L271-L296)；數值邊界在 [`freshness.ts`](https://github.com/tungweb3/imd-ember-world-review/blob/7215c5d89a96bc79113a85766c04868d54393f3c/source/src/shared/freshness.ts) 及 [`market.ts` L66-L115](https://github.com/tungweb3/imd-ember-world-review/blob/7215c5d89a96bc79113a85766c04868d54393f3c/source/src/world/market.ts#L66-L115)。

### 裁決理由

LOW-1 的關鍵不是「舊 verify owner 永遠做清理」，而是責任要在接受有效 PRESENT 時終止，同時帳戶或 provider 切換仍須形成另一個 displayed-session 決策。候選先把 owner 標成 terminal，再於切換事件依畫面已驗證地址送條件式清理；慢 verify body、held home 與晚回覆不能再奪回責任。這同時避免兩個相反錯誤：既不遺留切換前 session，也不讓已釋放的舊 nonce 撤掉後來的 session。

LOW-2 要求的不是「曾經有過一個 GET」，而是目前這一次 click 擁有自己的有效收據。候選在等待前序工作後重新送 canonical GET，並把 click、generation、lifetime、read sequence 綁在一起；舊 ABSENT、先前 click 的 GET 或遺失的跨頁提示都不能授權 challenge。回覆格式錯誤、傳輸錯誤、429 或 503 均保持 UNKNOWN，因而不會進入簽名。若讀到同地址 PRESENT，則直接接受並丟棄提示性資料，不再建立 challenge、prompt 或第二個 session。

LOW-3 把「一次事件只能有一個主要決策」與「整個生命期只能有一次清理」分開。切換時若已有可信 displayed session，就選地址斷言；只有沒有 displayed session 且仍有 retained verify owner 時才選原 nonce；單純 pending click 僅在本地取消並等待 challenge 自然到期。不同事件或舊 owner 可各自完成既有責任。同地址、同到期時間只描述外觀，不能當 session identity，所以舊 A nonce 在途時，新顯示的 A row 仍由自己的地址清理處理。

LOW-4 的修正亦沒有讓舊生命期直接操作新畫面。舊 cleanup 完成只設置「需要重讀」訊號；目前 client 若忙於 click、離開流程或非 idle，便延後到安全點才讀共用 cookie。重啟不必無限等待舊網路請求，已接受的同步通知也先完成；最後由最新 canonical read 決定顯示。伺服器的 token、nonce、未撤銷及未到期條件仍界定可撤哪一列，舊流不能跨撤後建的列。

LOW-5 的 authority boundary 保持窄：索引、roster、D1、名字與會員識別只找候選，只有針對已驗證 session 地址的鏈上 `ownerOf` 才給 house eligibility。索引新鮮度與密碼學 proof epoch 分開；等待 discovery 或 lane 之後會再取實際時鐘，過期即以最新區塊重證，而非沿用請求開始時刻。正、負、revert 與失敗 delta 都綁原 30 秒 epoch；最多嘗試 256 個識別碼，失敗也佔額度，避免用不斷加入新候選繞過上限。

LOW-6 將多處各自判斷的新鮮度收斂成同一失敗關閉規則。時間、時間戳與 TTL 必須有限，TTL 必須為正，只有非負且嚴格小於 TTL 的 age 才命中；恰好到期、時鐘倒退、未定值與無限值都重讀或回 unavailable。held RPC 在完成時也再驗證，不能把未來或已過期證據裝進 cache。這保住 sold-seat、revoked-session、公開名稱、行情與 floor 的共同邊界，而沒有把視覺動畫時鐘誤當權限時鐘。

INFO-1 的 lock 是狀態協調問題，不是新的登出權限。尚未完成的 click 被取消；若 verify 可能已提交，owner 進入 reconciliation-only，先等 response/transport fence，再以因果上較新的有效 PRESENT 或 ABSENT 終止。第一次 canonical read 為 503 時責任保留，後來普通讀到 PRESENT 才釋放；停止 client 不會令已釋放 owner 復活。已接受的 server session 因此不會只因錢包自動鎖定而被撤銷。

INFO-2 在資料進入畫面前規範化 direct 與 Worker fallback。主美元價格須有限且為正；市值、流動性、成交量與筆數須有限且非負；變動率可為有限負數。ETH floor 與換算輸入、除法結果及乘積均須有限且為正，否則 USD 欄位缺席而不是 Infinity。遠端未來時間戳原樣保留供 freshness gate 拒絕，不能偷偷改寫成現在；有效的負漲跌仍保留，故不是以「全部負數都丟掉」換取表面通過。

回歸掃描另核對伺服器 authority、錢包方法、security headers 與來源邊界。沒有看到名稱、roster 或索引變成授權來源，也沒有新增 transaction、approval、permit、delegation 或 mint 方法；已記錄的方法仍是查詢帳戶、請求帳戶與經檢查的 SIWE 個人簽名。沒有發現會製造額外 prompt/session、讓 old flow cross-revoke、取消 keyed-RPC 上限或擴張 header/method 的變更。這是針對供應檔及固定案例的否定結果；被遮蔽前端、真瀏覽器排程、Cloudflare 內部並行與未部署環境仍不可由它推論。

來源閉合的阻斷門檻另外逐項套用：若仍有重大或中等嚴重度缺陷、Auth／ownership 不變量的低度缺陷、錯誤資料可授權、正常次序會產生非預期簽名或 session、舊流程能撤新 credential、以新 key 無界放大 RPC、錢包方法或安全 header 擴張，便不能判定通過。現有程式、固定矩陣與反向校準未顯示其中任何一項；因此八項可在本地來源層閉合。相反地，部署 bytes 與量測候選不符會直接推翻發布結論，而目前根本尚未量測，故只能把它列為 release gate，不能把未知寫成通過。

保留限制也有實際影響。跨頁 GET 只能提供當下 canonical knowledge，不能鎖住另一頁同時開始的合法 click；多 isolate、不同 colo、cache eviction 或重啟可能增加鏈上查詢；failed delta 在原 epoch 內不重試，節省成本但延遲剛買到座位的可見性；限流、上游失敗與嚴格 freshness 會顯示 unavailable。已授權的晚到 cookie-clear 可能清掉較新的瀏覽器 cookie，但伺服器條件必須阻止它撤掉較新 row。這些都有界且以可用性為代價，故作 accepted limit，而非另稱已修復。

### 證據權重與不確定性

我的量測是：公開 archive 的 `SHA256SUMS` 全通過；兩份 prior official originals 重新下載後分別吻合 `c15eb0…6215` 與 `5f6f3a…8955`；不需第三方套件的三檔測試 **96/96、exit 0**。完整 17 檔公開命令在此乾淨環境因未供應 `viem` 而為 **96 pass／14 runner load failures、exit 1**，不是候選 assertion failure，也不能冒充 518 重跑。未安裝依賴、未加 stub、無 skip。

團隊 receipt（不是我的量測）記錄 public filtered **518/518**、零 fail/skip/cancel/todo；public `tsc` **exit 2**（TS2307×14、TS7006×1，共 15 個 withheld frontend diagnostics）；Worker empty-ASSETS dry-run retry **exit 0**。私有完整專案 **1528 pass**、TypeScript/Vite exit 0 也只是團隊 claim，不能轉移到 asset-free public subset。[TEST_RESULTS.json](https://github.com/tungweb3/imd-ember-world-review/blob/7215c5d89a96bc79113a85766c04868d54393f3c/Submission7_R8Closure/TEST_RESULTS.json)

另一份團隊 evaluator receipt 使用真 AuthClient、Worker、migrations、SQLite，但 provider/upstream/browser／時鐘為 injected；記錄 **24 tests、500/500 schedules、428 digests、3572 Worker calls、5477 SQLite comparisons、3402 projections、38 pre-header failures**，且分離 dispatch cookie、commit、Set-Cookie、fetch exposure、body completion。pure model 無 production import；fixed/calibration 不是 seeds，有限 anchored traces 不是 exhaustive randomness。[REFERENCE_SCHEDULER.json](https://github.com/tungweb3/imd-ember-world-review/blob/7215c5d89a96bc79113a85766c04868d54393f3c/Submission7_R8Closure/REFERENCE_SCHEDULER.json) baseline `f9a34…` 的 seeds 0/3/19 被同 oracle 以 AUTH-I3／AUTH-I5／INFO-1 拒絕，是預期 negative control，不是 candidate failure 或 production exploit；36-trial bounded minimization 也不是 global-minimal claim。[COUNTEREXAMPLES.json](https://github.com/tungweb3/imd-ember-world-review/blob/7215c5d89a96bc79113a85766c04868d54393f3c/Submission7_R8Closure/COUNTEREXAMPLES.json)

### SOURCE-CLOSURE 與 RELEASE-READINESS

**SOURCE-CLOSURE：PASS（targeted／conditional）。**八項原反例具備政策、候選實作、正向控制與 parent negative control；未發現 Critical／High／Medium、Auth／ownership invariant Low、錯誤 authority、非預期 prompt/session、old-flow cross-revoke、無界 keyed-RPC、wallet method／security-header 擴張。M1 的 public-name 寫入是持久寫入，所以 World 不可描述為全唯讀；該寫入 authority 未因名稱／roster／D1 index 而擴張。

**RELEASE-READINESS：BLOCKED。**候選明載 `NOT_DEPLOYED`、production parity `NOT_CHECKED`；舊 production `f9a34…`／R5-R7 receipts 只能作歷史比較，不能替新候選背書。[DEPLOYMENT_STATUS.json](https://github.com/tungweb3/imd-ember-world-review/blob/7215c5d89a96bc79113a85766c04868d54393f3c/Submission7_R8Closure/DEPLOYMENT_STATUS.json) 發布前至少須：以 candidate build/deploy receipt 回讀 Worker version、traffic、bundle、bindings／migrations／headers並量測 production match；在完整資產樹重跑 tsc/Vite／全套；再作獨立 review。GET 不是跨 tab atomic lock、per-isolate cache 不是 global RPC cap、late cookie/process death 是 best effort、Auth fetch 無新 deadline、實體 OS wallet／Cloudflare binding／WAF／D1 internal interleavings 未窮舉。failed delta 等到原 epoch 到期、限流／index 拒絕與 fail-closed 會犧牲可用性；這些是有界 accepted limits，不是已消失的風險。

---

# 證據附錄（不計主報告字數）

## A. 完整閉合表

| finding | 先前行為 | policy／候選定位 | baseline negative control | candidate measurement | 限制 | state／severity／blocker |
|---|---|---|---|---|---|---|
| LOW-1 | terminal owner 令 switch 提早 return，PRESENT A 的 cookie/row 可留存 | acceptance 先於 home；switch 是獨立 event，以 displayed `expectedAddress`，不復活 RELEASED/CONSUMED nonce；[`auth.ts` L186-L228](https://github.com/tungweb3/imd-ember-world-review/blob/7215c5d89a96bc79113a85766c04868d54393f3c/source/src/world/auth.ts#L186-L228) | frozen parent seed/fixture 不能滿足 terminal-owner context cleanup | held-home account/provider kernels；row `1/0/1`、challenge `1 used/0 pending/0 invalidated` | late authorized cookie-clear 仍可能清較新 browser cookie，但不得 revoke 新 row | **fixed locally / Low / no source blocker** |
| LOW-2 | slow valid verify body 前的 PRESENT 未廣播；舊 ABSENT/hint 可導致第二 prompt/session | 每次 click 自己 GET；invalid/429/503=UNKNOWN；PRESENT suppress 全 sign flow，hint 只促 reread；[`auth.ts` L379-L445](https://github.com/tungweb3/imd-ember-world-review/blob/7215c5d89a96bc79113a85766c04868d54393f3c/source/src/world/auth.ts#L379-L445) | seed 0 AUTH-I3 拒絕 missing own-click preflight | slow-body-sibling `created/live/revoked=1/1/0`、challenge `1/1/0/0`；lost-hint 沒有第二 session | GET 不是全域鎖；兩個真正獨立 click 可同時讀 ABSENT | **fixed locally / Low / accepted concurrency limit** |
| LOW-3 | displayed session + pending nonce 的 switch 選 nonce，409 後未清 displayed row | `planCleanup` 是 pure one-primary per EVENT；displayed address > retained owner > local pending cancel；planned/effective/retry 分開由 lifecycle 記錄 | seed 3 AUTH-I5 拒絕 competing pending nonce cleanup | displayed-pending `1/0/1`；challenges `2/used1/pending0/invalidated1`；same-address test 保留舊 row直到其原 cleanup，另撤新 displayed row | 不宣稱整個 app lifetime 只有一次 cleanup；不同 event/owner 可各有一次 | **fixed locally / Low / no source blocker** |
| LOW-4 | stop 清理在途、restart 先顯示 PRESENT，舊 cleanup 完成後不重讀而留 stale UI | detached completion 只排當代 read；busy/phase/leaving gate；舊 callback 不直接寫 UI；[`auth.ts` L195-L228](https://github.com/tungweb3/imd-ember-world-review/blob/7215c5d89a96bc79113a85766c04868d54393f3c/source/src/world/auth.ts#L195-L228) | parent restart witness 保留 stale PRESENT | restart kernel `created/live/revoked=2/1/1`、challenge `2/2/0/0`，old cleanup 不撤 newer row | process death、離線、永遠 stalled fetch 仍 best effort | **fixed locally / Low / accepted availability limit** |
| LOW-5 | refused `fresh=1` 在 30 秒內反覆 budget + keyed RPC；discovery wait 可用過期 proof | proof epoch 30s；completion clock 重新判；delta 同 block/deadline；attempted cap 256 含 failed；queued caller重看 roster；[`ownership.ts` L246-L299](https://github.com/tungweb3/imd-ember-world-review/blob/7215c5d89a96bc79113a85766c04868d54393f3c/source/server/ownership.ts#L246-L299) | 同 evaluator 指向 f9：8 pass／20 expected failures | team ownership 139/139；x20 refused=budget1/index0/RPC1；index@0/proof@31/fresh@32=RPC2；sold/delayed/failed-delta controls | per-address/per-isolate，不是跨 colo/global RPC ceiling；first/expired proof failure受既有限流 | **fixed locally / Low / accepted bounded limit** |
| LOW-6 | negative age 令 home/session/name/market cache 過度新鮮，sold seat/revoked session UI延長 | `isFreshAge` 有限、正 TTL、exclusive bound；held completion也判 clock；[`freshness.ts` L3-L7](https://github.com/tungweb3/imd-ember-world-review/blob/7215c5d89a96bc79113a85766c04868d54393f3c/source/src/shared/freshness.ts#L3-L7) | freshness evaluator 對 f9：3 pass／6 expected failures | 我的 dependency-free freshness/name controls通過；team 51/51 scoped，含 backward sold/revoked | 真區域時鐘漂移／OS suspension 未量測 | **fixed locally / Low / no source blocker** |
| INFO-1 | LOCK 在 idle retained-owner 狀態自動 nonce logout，撤已 committed session | lock local-cancel click；retained uncertain owner只 reconcile；post-fence PRESENT/ABSENT才 release；[`auth.ts` L519-L557](https://github.com/tungweb3/imd-ember-world-review/blob/7215c5d89a96bc79113a85766c04868d54393f3c/source/src/world/auth.ts#L519-L557) | seed 19 INFO-1 拒絕 uncertain-lock auto logout | lock-idle `1/1/0`；lock-active precommit `0/0/0`、一個 pending challenge；503 後 PRESENT：零 logout、row仍 live | physical wallet lock/event timing injected，非真 OS wallet | **fixed locally / Info / no blocker** |
| INFO-2 | 極小 `priceNative` 可算出 Infinity floorUsd | direct/fallback runtime normalization；finite positive price/floor/product，optional非負、change可負；[`market.ts` L33-L50](https://github.com/tungweb3/imd-ember-world-review/blob/7215c5d89a96bc79113a85766c04868d54393f3c/source/src/world/market.ts#L33-L50), [L66-L115](https://github.com/tungweb3/imd-ember-world-review/blob/7215c5d89a96bc79113a85766c04868d54393f3c/source/src/world/market.ts#L66-L115) | f9 freshness numeric controls預期失敗 | 我的 freshness-v11 9項通過；overflow主價 unavailable、負 change保留、future floor hidden | 顯示資料；不涵蓋交易／經濟權限 | **fixed locally / Info / bounded display impact** |

## B. 固定矩陣與額外兩案

共同 receipt：team command 為 `node --test --test-reporter=tap --test-concurrency=3 … auth-r8 … auth-v11 … ownership-v11 … freshness-v11 … auth-reference-scheduler`，exit 0，source `8a22b510…`；Auth evaluator hashes：model `6c3259…942a`、driver `e0a854…a72`、scheduler `5cc24f…b8318`。所有 scheduler cases 都逐步比較 dispatch/captured cookie aliases、SQLite rows、Set-Cookie jar、client projection；表內 `S=l/r` 是 session live/revoked，`C=u/p/i` 是 challenge used/live-pending/invalidated。過期未用 challenge 不算 live pending authority。

| case；事件順序／context | expected = actual；計數與 authority |
|---|---|
| PRESENT／held home／account switch；A verify commit → post-fence PRESENT → home held → switch B | 一次 address cleanup；`S=0/1, C=1/0/0`，prompt1；A cookie alias清除，B無 challenge/verify；seed1 digest `da50de…5078` |
| PRESENT／held home／provider switch；同上但替換 provider | 同上 `S=0/1, C=1/0/0`，prompt1；terminal nonce不復活；seed2 `3d7a47…e4c3` |
| slow valid verify body／sibling stale ABSENT；commit+Set-Cookie → canonical PRESENT → hint → sibling click | sibling own GET見 PRESENT，零第二 prompt/challenge/verify；`S=1/0, C=1/0/0`；seed10 `b5bca2…7539` |
| displayed session／pending nonce／switch；T1 challenge held → T2建立 session → T1讀PRESENT→challenge body→switch | 只送 displayed-address primary、pending local cancel；`S=0/1, C=1/0/1`（2 rows）；prompt總1且T1=0；seed3 `156659…c80c` |
| stop／cleanup in flight／restart；uncertain verify → stop nonce cleanup held → restart/新session →舊完成 | current reread；舊流只撤自己的 row：`S=1/1, C=2/0/0`、used2；seed4 `e79db4…146c` |
| fresh=1 refused index ×20 | budget1、index0、RPC1；20 views limited；一個 proof epoch，未證新候選不授權；[`ownership-v11.test.mjs` L68-L73](https://github.com/tungweb3/imd-ember-world-review/blob/7215c5d89a96bc79113a85766c04868d54393f3c/source/tests/ownership-v11.test.mjs#L68-L73) |
| backward clock／sold seat | rollback cache miss；deadline前可重用，exact/after expiry latest-block reproves並拒 sold；Auth/ownership rows N/A、prompt/cookie/cleanup 0 |
| backward clock／revoked session | current GET/home reread，不延長 PRESENT；`S=0/1, C=1/0/0`、prompt1；seed9 `b9bde8…d6e` |
| idle LOCK | committed session保留，零 logout；`S=1/0, C=1/0/0`、prompt1；seed5 `a23977…0b75` |
| active-click LOCK | click取消，未 commit時 `S=0/0, C=0/1/0`、prompt0；uncertain commit則 post-fence reconcile、不 auto revoke；seed6 `fdf920…1f13` |
| missed／dropped signed-in hint | sibling明確 click 自己GET；無第二 prompt/session；最終顯式流程使 `S=0/1, C=1/0/0`、prompt總1；seed0 `93550e…87e2` |
| **額外：same-address old nonce／new row**；舊A cleanup held → restart → 新A row → switch C | address/expiry不當session identity；address cleanup撤新 displayed row，舊nonce request仍只負責舊row；nonce cleanup恰1、address cleanup恰1、prompt1；[`auth-v11.test.mjs` L120-L143](https://github.com/tungweb3/imd-ember-world-review/blob/7215c5d89a96bc79113a85766c04868d54393f3c/source/tests/auth-v11.test.mjs#L120-L143) |
| **額外：LOCK 503／later valid PRESENT**；malformed verify body → lock → first reconcile503 → ordinary current GET PRESENT → stop | first read不釋責；後讀RELEASED，stop零logout；`S=1/0`，prompt1；[`auth-v11.test.mjs` L98-L107](https://github.com/tungweb3/imd-ember-world-review/blob/7215c5d89a96bc79113a85766c04868d54393f3c/source/tests/auth-v11.test.mjs#L98-L107) |

Ownership 的另外 real-Worker/RPC controls：index@0/proof@31/fresh@32 共 RPC2；discovery跨 expiry與 60 秒 lane admission 都在當下用 `latest`；255既證＋2新候選只試一個，failed delta佔第256格直到原 deadline；等待中的新 roster取得自己的 pinned delta。`limited`／`unavailable` 均不等於 complete-empty 或 not-owned authority。[OWNERSHIP_FRESHNESS.md](https://github.com/tungweb3/imd-ember-world-review/blob/7215c5d89a96bc79113a85766c04868d54393f3c/source/OWNERSHIP_FRESHNESS.md)

## C. Authority、headers、wallet boundary

只有 authenticated session address 的 mainnet `ownerOf` 可給 home authority；roster、Alchemy/D1 index、public name、`publicMemberId` 只作 discovery/display。Server Auth、World API、headers、package-lock、migrations 對 parent 的團隊 boundary comparison 為 unchanged；wallet methods 前後均只有 `eth_accounts`、`eth_requestAccounts`、checked SIWE `personal_sign`（HTTP `POST` 是 API method，不是 wallet method）。我能在公開 bytes 靜態確認方法集合與 headers 檔，不能比較未供應的私有原檔、部署 bindings、WAF 或 live header。[BOUNDARY_CHECK.json](https://github.com/tungweb3/imd-ember-world-review/blob/7215c5d89a96bc79113a85766c04868d54393f3c/Submission7_R8Closure/BOUNDARY_CHECK.json) [WALLET_METHODS.md](https://github.com/tungweb3/imd-ember-world-review/blob/7215c5d89a96bc79113a85766c04868d54393f3c/WALLET_METHODS.md)

## D. 可重現命令、錯誤、排除與 provenance

我的命令與結果：

```text
curl -L <7215c5d...tar.gz>; tar -xzf ...
(repo root) sha256sum -c SHA256SUMS
=> 216/216 OK（SHA256SUMS 本身除外）

curl -L raw.../AUDIT.md | sha256sum
=> c15eb0cc7b0c696a1ffca5e62796c0ec83b05314296573a28529b07a3bc26215
curl -L raw.../artifacts/report.md | sha256sum
=> 5f6f3abc6f29e132561f70d246ac882916af7153f79d29ed6eb0ca0c95998955

(source) node --test --test-reporter=tap \
  tests/auth-lifecycle-model.test.mjs tests/freshness-v11.test.mjs tests/member-r7-cache.test.mjs
=> tests 96, pass 96, fail/skip/cancel/todo 0, exit 0, Node v24.21.0

(source) <TEST_RESULTS.json 的17檔 public filtered command>
=> tests 110, pass 96, fail 14, skip 0, exit 1
=> 14 個 test-file runner 都是 ERR_MODULE_NOT_FOUND: viem；沒有 assertion failure。
```

本環境未含 `node_modules`，依任務限制未建立／修改它，也未用 stub 或把 14 個載入錯誤改列 skip。因此我的 96/96 只覆蓋 pure lifecycle model、freshness/market 與 public-name cache；Auth real Worker/SQLite、ownership RPC controls 的 518、500 schedules 與 1528 數字均保留為 team receipts。public `tsc` 的 15 diagnostics 與缺 presentation assets 是真實 exclusion；Worker dry-run 使用空 ASSETS，只證 Worker bundle 可產生，不證網站 build 或 deployed-byte parity。

先前官方原文（mutable `main`，本次 bytes 已以題定 hash 核對）：[Audit](https://github.com/Identity-md/research/blob/main/jobs/2abde7c7-c84a-4a64-a693-f83754bccd91/files/AUDIT.md)、[Report](https://github.com/Identity-md/research/blob/main/jobs/25c2d640-df15-45c6-bbef-f79a16405807/files/artifacts/report.md)。R5/R6/R7 receipts 全是 historical；原報告中的 disagreements／unknowns（global locking、late cookie、process death、physical providers、production/WAF/D1 parity）均未被本報告抹除。

## E. 範圍與未做事項

本次是 unofficial TypeScript Cloudflare Worker／React SIWE，沒有 Solidity。排除完整 Genesis／Mint／Ember Coin／3D／avatar／selfie／無關功能稽核；沒有真 wallet/signature、production request、transaction、approval、permit、delegation、mint、bridge、deployment、付費 job 或 publication。所有 fixtures 是離線合成。完成／accepted 僅代表輸出完整；測試通過、Low／Info 標籤或本地閉合都不是 endorsement、完整產品證明或 fund-safety 保證。
