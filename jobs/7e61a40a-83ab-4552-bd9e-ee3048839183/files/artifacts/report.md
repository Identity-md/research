# IMD Ember World 第九次結案與發布證據報告

截至 2026-10-05；僅 World／Member M1。**指定三 Low、兩 Info 的來源反例，於本次公開位元組及有界離線測量內均已關閉；完整發布準備仍為 UNKNOWN。** 此為本次 REVIEWER 的技術判斷，不是另一次官方 Audit 工作完成宣告。TEAM 原有狀態仍是 `TEAM_PASS_EXTERNAL_REVIEW_PENDING`。[五項對應][matrix]、[本次測試](evidence/retry-3.log)、[artifact 實測](evidence/retry-4.log)。

| 判定對象 | 結果 | 依據、阻擋與界線 |
|---|---|---|
| SOURCE-CLOSURE：指定五項 | **PASS（有界）** | 613/613 公開測試、真實檔案控制與保存後 replay 通過；未見仍成立的指定反例。不是所有可能狀態均安全。 |
| RELEASE-READINESS：完整發布 | **UNKNOWN** | TEAM 建置、上傳、記錄持久化及讀回有對應證據；私有完整建置與認證後正式環境門檻未獨立測量，不能給無條件 PASS。 |
| 公開完整前端編譯 | **BLOCKED（輸入缺件）** | 刻意移除完整前端，不能把未執行編譯算成通過；此限制不否定五項局部結案。[範圍][readme] |

本次固定公開 pin 為 `347268a7ecae700088547c2402db9a3eb07a6fd2`，前版為 `88c130283efc45260f9e00da8d2d3055c38483bd`；私有來源 provenance 為 `8c3b60171a22b3ce71854f12282e629bbf5ca06f`，不是公開 checkout URL。系統是非官方 TypeScript Cloudflare Worker／React SIWE，**沒有 Solidity**；M1 會持久寫入 profile。審查含 Auth／server authority、ownership／index／budget／freshness 及 artifact／runner；排除 Genesis／Mint、Ember Coin、Fren Pet、完整 3D／scene／media／avatar／selfie 與私有備份。[輸入][inputs]

最新版 Audit8 於 `2026-10-04T19:26:33.961Z` 完成、`19:26:58Z` 發布；較早 Report8 於 `19:13:53.530Z` 完成。兩份原文均已下載核對 SHA256，因此採時間較晚的 Audit8 實際反例作起點，不以較早結案表取代。下表 NEW／REOPENED 描述相對既往修補的因果關係，PASS 描述本候選的結果；沒有僅按標題判為 DUPLICATE、SUPERSEDED 或 ALREADY_FIXED。[Audit8][audit]、[Report8][priorreport]、[核對](evidence/provenance-check.json)

| Audit8 finding／沿革 | 影響與本候選結案理由 | 判定／證據 |
|---|---|---|
| 1 Low：post-D1 expiry；NEW | proof 在 29999ms 有效，但等待後可過期而仍給 owner。現在所有 enrichment／lane await 之後重查嚴格 proof age；到 30000ms 回 503，不重訂 checkedAt。倒退、NaN、Infinity、拒絕／失敗 lane 均 fail closed，下一次可 latest recovery。 | PASS；[ownership][ownership]、[案例][owntest] |
| 2 Low：locked wallet 首次事件；REOPENED | cookie A 不是已觀察 wallet A。首次 B 保留 session、零清理／提示；真正 A→B、A→lock→B 及 explicit grant 後切換仍有 address 清理。observedAccount 跨 lock 保留，但生命週期重設。 | PASS；[Auth][auth]、[實際 rows／controls][authtest] |
| 3 Low：slow fresh overlap；REOPENED | 二十個早到同 context waiter 共享一個 admission，四頁各 7475／7500ms 均只一 cycle／proof／epoch。不同 roster、fresh intent、晚到及失敗控制仍重評估；不延長 producer timestamp。 | PASS；[flight 條件][ownership]、[慢速與反向控制][owntest] |
| 4 Info：dangling final symlink；REOPENED | 原本 existsSync 看漏缺目標連結而越界寫檔；改 lstat、exclusive sibling temp、fsync、父節點／target 重查及 rename。真實連結、替換與 hardlink alias 均有控制。 | PASS；[artifact][artifact]、[13 項實測](evidence/retry-4.log) |
| 5 Info：一般絕對路徑外洩；REOPENED | 原本只遮部分根目錄；現在巢狀診斷、空格／括號及 Windows 變體保存後遮蔽，URL、relative path、nonce／事件及非空 replay 保留。 | PASS；[sanitizer][artifact]、[保存／重播驗證][verifier] |

三 Low 曾分別影響過期權限、非預期撤銷及重複成本，均有來源結案阻擋性；Info 也是真實檔案寫入／洩漏反例，不能靠降低標籤消除。接受的剩餘 artifact 界線是**私有、受控本機根目錄**：portable Node 無 dirfd/openat 原子父路徑保障，不能推廣到敵手同步換祖先或 SMB/NFS；保守遮蔽亦可能吃掉路徑後同列文字，代價是診斷可讀性而非放任洩漏。[artifact 限制][artifactreceipt]

REVIEWER 使用 Linux x86_64、Node `v24.21.0`、npm `11.19.0`、真實鎖定 viem `2.56.9`。首次 npm 快取 EROFS 導致安裝失敗；保留後改用可寫快取，四個指定命令全部 exit 0。完整 23 檔 runner 為 613/613、fail／cancel／skip／todo 全零；其中 artifact 18/18，standalone verifier 13/13。未替換 crypto、Worker 或 SQLite，未選私有來源或省略失敗檔案。預設 scheduler artifact 輸出為 disabled。[命令與時間](evidence/retry-commands.json)、[環境與位元組](evidence/integrity.json)

TEAM 的 Node `24.19.0` 私有完整 1663/1663、私有 supported runner 613/613、fresh clean 私有 checkout 613/613、artifact 18/18 與兩次 verifier 13/13 是不同測量。本報告另行提供該 pin 公開位元組的直接 runner 結果。141 公開檔全部符合清單；125 exact、16 redacted／57 masked lines 的私有對應仍屬 TEAM 陳述。core 500 campaigns／428 digests 與 additional 90／54 身分分開，不能說成 590 unique proof cases 或窮盡狀態機。[清單][manifest]、[TEAM 收據][tests]

發布鏈採 privileged LOCAL 完整測試 gate，再由普通 USER 跑 TypeScript／Vite／Wrangler；**沒有呼叫 canonical `npm run deploy`**。TEAM 的 upload exit 0、deployment exit 0、verification match 與 record persisted 是四個分別成立的陳述。舊 canonical upload 0 後 overall 1 的 EPERM 仍是歷史失敗。新 Worker `06cbc8fe-112f-4a11-b84f-42907179afff` 的 316024 bytes 與 build 雜湊相符、100% traffic、7 bindings、7 migrations／0 pending，均只代表所列 TEAM 讀回時點。[建置／部署][build]

剩餘動作是獨立核驗私有完整 build 與認證 Cloudflare 對應、補受權的 cookie flags／ERC1271／登入與寫入測量，以及真實 browser／provider、WAF／limiter／upstream／跨 isolate concurrency／cron／process-death 驗證。匿名 session 的 signedIn:false、no-store、無 Set-Cookie 不能回答上述問題；本次只執行讀回 verifier 的零網路預設模式。未有新反例故不判來源 BLOCKED，但未知 release gates 不能算 PASS。完成、Low／Info、全綠測試均不構成背書、零漏洞或資金安全認證。[讀回][served]、[未測邊界][reviewer]

判定重點不是測試名稱相似，而是原本錯誤的授權來源是否被切斷。所有權案例先建立真正的測試登入，再讓既有 proof 在等待資料庫回應時跨越期限；修補後拒絕的是過期 owner 權限，不是刪除登入資料列。三個延遲控制的 session 建立／存活／撤銷均為 1/1/0，拒絕時 proof RPC 與 budget 各一，後續重新證明才增加第二次 RPC。這支持「到期拒絕且可恢復」，不支持「交易當下仍持有資產」或「整個請求全域原子化」的更強主張。[實際計數](evidence/retry-3.log)

錢包案例則檢查清理的責任是否來自真正觀察。首次解鎖與被動發現 B 時，原 cookie A 的存活列保留，沒有新增 challenge、verify、prompt 或 signed-out 廣播；真正切換才出現一次 address-conditional logout，且 challenge 的總數／已用／待用／失效維持 1/1/0/0。明確登入流程與尚未結束的驗證仍保留 nonce 責任，不能為避免首次事件誤撤銷而取消所有舊流程清理。新頁面與同 client 重啟控制，也防止舊觀察跨生命週期取得權力。[固定 Auth 測試][authtest]

慢速案例將第一頁阻擋到二十個等待者全部加入，再逐頁推進時鐘；修補後每組只四次 page fetch、一個 budget admission、一個 proof 與一個 epoch。完成時的有效證明可共享，但晚到、不同名單或不同 fresh 意圖不能借用這個豁免。這是降低特定已重疊請求群的成本，不是取消上游限額，也不是證明跨程序、跨資料中心只有一次工作。失敗分享與後續重試控制同樣必要，否則單看成功組的低 RPC 數可能掩蓋永遠不恢復的錯誤。[flight 反向控制][owntest]

證據歸屬有三層：本次直接測得的公開來源行為、TEAM 提供的私有完整來源與部署收據、以及兩者支持的有限推論。宣告的原始雜湊可固定文件身分，不能自行證明私有內容真實；本次沒有取得完整前端，因此不把 TEAM 的編譯成功寫成 REVIEWER 成功。原有私有測試的零失敗，與 Windows 普通權限曾因檔案連結失敗的收據，也必須同時保留。後一次具能力環境的成功只解除那次驗收阻礙，不會抹去先前結果。[收據與歷史失敗][tests]

時間範圍亦有限制：source manifest 產生於 `2026-10-04T20:49:21.366210+00:00`，但沒有另列 freeze clock，故不能把產生時間冒充來源凍結時間。TEAM deployment 為 `2026-10-05T01:10:08.607Z` 至 `2026-10-05T01:10:28.002Z`，served readback 為 `2026-10-05T01:14:47.681Z` 至 `2026-10-05T01:14:55.834Z`。記錄已持久化的狀態與確切寫入時間是不同問題；後者仍未公開。Worker SHA256 為 `0d1c6176b09a73dac605c5f19a126c8b4ae4496fe659f1197a909e7f87c849e2`；讀回吻合只支持該時點，不能延伸成較晚 production 的保證。[manifest][manifest]、[發布時序][build]、[讀回][served]

發布讀回還應區分靜態資產與伺服器權限。TEAM 分別量了 HTML、主程式、樣式與 InteriorView 的原始位元組和安全標頭；它們支持所列建置產物曾被送出，卻不能證明所有私有模型、媒體或未測路由一致。匿名 session 回應只描述未登入請求，沒有建立認證 cookie，因此不可能從「沒有 Set-Cookie」推論登入後 cookie 屬性正確。同理，綁定與遷移狀態來自另外的 TEAM 認證讀回，不能由五個匿名端點反推出。[served 原始對應][served]、[設定對應][build]

若下一步需要無條件發布判定，應先明確補齊哪一個未知門檻，而不是再把同一套離線測試多跑幾次。完整編譯缺的是公開輸入；真實登入缺的是受權的認證行為證據；全域併發與程序死亡缺的是部署環境的故障條件。每類缺口都需要相應證據，不能相互抵換。若後續量到權限錯誤、跨流程誤撤銷或部署不符，即使仍標 Low，也應重新判為阻擋；目前沒有量到該等新反例，不代表已證明它們不可能發生。[未測項目][reviewer]

---

## 證據附錄 A：固定來源與測量身分

所有本報告的 GitHub 專案連結固定在同一公開 pin；Submission8 與更早 namespace 僅作歷史，不代表第九次現況。公開輸入已讀取 [README][readme]、[REVIEW_INPUTS][inputs]、[PRIOR_REVIEWS][priors]、FinalClosure 的 closure／test／artifact／build／served／reviewer 資料、[SERVED_EXPECTATIONS][expected] 與 [source manifest][manifest]。下載與本地靜態核對不等於查到私有 Git 或建置原始內容。

| 身分 | 精確識別與雜湊 |
|---|---|
| Audit8 原文 | job `7716c3f5-5d6c-4953-a643-141da678d051`；32883 bytes；SHA256 `8c9baaa6838e8b0137baa44282d1fcc2704834d68c92dafcd4426a882905bcfc`；[immutable original][audit] |
| Report8 原文 | job `38438c89-b34c-4d38-8ae8-027c9d175fb1`；51040 bytes；SHA256 `71c6f621342210c7f9abc6830babb20049dea8338e5492b9622a4783a6eed61f`；[immutable original][priorreport] |
| 鎖檔 | `9f86565e314090d5c399fd2998ecc5dd901746fb6dc7502470ec77dfd911b95b`；本次與 TEAM 相同 |
| artifact module | `69b9d2023fde69ec2b2b1719c721f0f99d5b0d7274aef5a548d75a96ec2fe2d7` |
| artifact verifier | `edec8bcbe3a257f0e58d40b509fbb48c19c1840935489195c5fd4f930083c195`（TEAM 收據；同 pin 程式） |

公開 manifest 141/141 的大小與 SHA256 已獨立核對，執行副本同樣 141/141 無差異。這只驗證公開內容與清單／副本一致，無法獨立驗證被遮蔽原文；不應將公開 redacted wrangler 指紋當私有原件指紋。[本次 integrity](evidence/integrity.json)

## 證據附錄 B：本次命令、完整失敗與環境

執行目錄為指定快照 `source/` 的逐位元組暫存副本 `/tmp/imd9-review/source`；沒有改測試或鎖檔。所有安裝均限暫存執行環境，交付報告與收據是普通檔案，不依賴日後網路或 node_modules 才能讀取。原始 stdout/stderr 合併保存於 evidence，不能把本報告自查當成第二位獨立審查者。

首次嘗試：`npm ci --ignore-scripts` exit 226（EROFS，預設 cache 唯讀）；`node scripts/review-tests.mjs --check` exit 1；`npm run test:review` exit 1，前置檢查失敗而未開始測試，**不是 0/0 PASS**；`node scripts/verify-artifact-closure.mjs` exit 1，13 assertions 中 12 pass／1 fail／0 skip，實際 saved replay 因 viem 不可用失敗。這批環境失敗完整保留：[命令](evidence/commands.json)、[安裝](evidence/1.log)、[preflight](evidence/2.log)、[runner](evidence/3.log)、[verifier](evidence/4.log)。

修復僅指定 `npm_config_cache=/tmp/imd9-review/npm-cache`，依相同順序重跑：

| 命令 | Exit | 實際數量／結果 | 秒（wall） | 原始結果 |
|---|---:|---|---:|---|
| `npm ci --ignore-scripts` | 0 | 79 packages installed；npm audit 0 vulnerabilities（非安全認證） | 26.267 | [log](evidence/retry-1.log) |
| `node scripts/review-tests.mjs --check` | 0 | Node v24.21.0／viem 2.56.9／23 files | 0.070 | [log](evidence/retry-2.log) |
| `npm run test:review` | 0 | 613 tests／613 pass／0 fail／0 cancelled／0 skipped／0 todo | 23.898 | [log](evidence/retry-3.log) |
| `node scripts/verify-artifact-closure.mjs` | 0 | 13 assertions／13 pass／0 fail／0 skip；無取消或 todo 案例（非 TAP 計數欄位） | 1.068 | [log](evidence/retry-4.log) |

613 的 TAP 報告 duration `23483.036931ms`；artifact suite 的 18 項包含在 613 中，不可再加算。真實 Linux filesystem 成功建立 dangling／existing file symlink、directory symlink、hardlink，且替換拒絕、outside 未建立、既有 sentinel／hardlink alias 不改變；不是只有 capability 探測通過就略過測試。verifier 的 saved trace 有 46 actions、10 Worker calls、11 DB comparisons，digest `93550e7acb3a1a47516f612b0f268ec8b8ffb51f7f8173a7d7e8b4937d4687e2`，保存前後 action／event、counts／projections／classification 一致。[實測 JSON](evidence/retry-4.log)

兩套 scheduler 的本次診斷均 `artifacts:"disabled"`；opt-in 僅准明確 `source/tmp` 子目錄、受限檔名，並先 sanitizer 再保存。verifier 的合成 root 也是本機暫存 fixture，未寫正式環境或第三方目錄。測試使用真實產品 AuthClient／Worker code 與 Node SQLite，但鏈、provider 與時間是離線 fixture，並不等於實際 Cloudflare D1 或敵意 wallet。[runner][runner]、[artifact][artifact]

## 證據附錄 C：五項因果、資料列與反向控制

**Low1。** [本次 TAP](evidence/retry-3.log) 記錄 initial checkedAt `1790596800000`。post-proof D1 延遲 0／1／2ms 對應 age 29999／30000／30001；status 200／503／503，只有第一項 eligible=1。session created/live/revoked 均 1/1/0，初次 index budget=1、owner proof RPC=1；過期回應沒有 owner fallback，後續 request eligible=0、RPC=2、checkedAt 至少增加 30000ms、budget 仍 1。嚴格條件是有限且非負的 elapsed `<30000`，同 block 或 copy warming 不得更新 epoch。測試另外覆蓋 await 後 rollback／NaN／Infinity、lane refused／admitted failure，再恢復 latest。[程式位置][ownership]、[固定測試][owntest]

歷史 Audit8 相同 D1 路徑在 30000／30001ms 仍 owner，session 1/1/0、challenge total/used/pending/invalidated=1/1/0/0，setup challenge/verify=1/1；本次對應案例的 TAP 直接列出 session／RPC／budget，challenge 計數並未在該診斷再列，故不偽稱新增逐列觀測。[Audit8][audit]。TEAM 同 evaluator vulnerable ownership baseline 12 cases 中 3 pass／9 fail、exit 1 是負校準，並非本次獨立 baseline 重跑。[對應][matrix]

**Low2。** Cookie A → locked `[]` → 首次 `accountsChanged([B])`，本次 before/after 的 session created/live/revoked 都是 1/1/0，challenge total/used/pending/invalidated 都是 1/1/0/0。追加 prompt／eth_requestAccounts／challenge／verify／logout／broadcast 全零；upstream calls 1→1（setup 的 index，事件不加 owner RPC）。discovery-first、same-account unlock、fresh-page、同 client restart 也保留；已觀察 A→B 或 A→lock→B 則 1/0/1、一次 `expectedAddress` 清理 HTTP 204、無 nonce 清理、一次 signed-out broadcast；challenge rows 不變。[本次 LOW2_EFFECTS](evidence/retry-3.log)、[11 模式與 explicit control][authtest]

explicit initial grant 建立可清理的觀察身分：一 prompt、一 eth_requestAccounts、一 challenge／verify，後續 genuine switch 只撤銷一次，沒有自動替 B 簽名。active／retained flow 的不同帳戶仍保有舊 nonce 責任；既有 old-A-nonce/new-A-row 控制與舊生命週期 guard 保留在 runner，不能將所有切換都當 passive 而免清理。TEAM targeted Auth baseline 7/12、5 fail；candidate 12/12 及 selected regression 544/544 是早期局部收據，本次以完整 613 判定。[Auth cleanup／lifecycle 測試][authtest]、[TEAM mapping][matrix]

**Low3。** 二十個在第一頁 gate 期間加入的 fresh requests，四頁每頁 7475ms 時 index cycles/page fetches/budget/proof RPC/epochs=1/4/1/1/1，elapsed=30030ms，checkedAt=`1791115229930`；7500ms 時同樣 1/4/1/1/1，elapsed=30130ms，checkedAt=`1791115230030`。兩者 20 個 eligible 都為 1。普通四頁 control=1/4/1/1/1；fresh 單頁 200ms control=1/1/1/1/1、elapsed=330ms、epoch=`1791115200230`。相較 Audit8 的兩個 slow fresh 20 cycles／80 pages／20 RPC／20 epochs，修補消除的是已加入同 context 的重複 admission，不是假設不存在上下游延遲。[本次診斷](evidence/retry-3.log)、[歷史反例][audit]

join 條件還包含 chain key、fetch、db identity、fresh/again、roster/ranking context 及 pending age；完成後仍檢查 proof TTL。changed roster、fresh intent、晚於 pending epoch deadline 必須重評估，失敗不蓋成功 epoch；相同失敗分享，後續 retry 可恢復。512 active-address cap 不得 evict 正在飛行者。直接 Ownership cohort 沒有 session／challenge rows，prompt／cleanup 等不適用且未產生；另一路 Worker/SQLite 20 route 測試保存 created/live=1/1，不能把 direct fixture 當 auth bypass 證明。限額只是本 isolate／有界 admission，不是 global RPC ceiling。[controls][owntest]

**Info4／Info5。** [實際 verifier][verifier] 用 lstat 確認 dangling entry 確實存在、target 不存在，write 拒絕且 outsideCreated=false；existing target bytes 保留，directory links／dangling parents／root links／getter 觸發 final-entry 或 parent substitution 拒絕，regular replacement 不改 hardlink alias。遮蔽涵蓋一般 POSIX、drive slash、UNC、rooted backslash、file URL、巢狀 key/value、空格／括號；保存後再讀 JSON 驗證，並保留 HTTP URL、relative path、protocol route、nonce alias 與事件順序。它不是任意字串的無損轉換，也不是受敵手操控根目錄的安全承諾。[saved-artifact suite][artifacttest]、[13/13](evidence/retry-4.log)

## 證據附錄 D：TEAM 與 REVIEWER 時間軸

下列 UTC 不混用 generatedAt、source-freeze、test completion、upload、persist 與 served readback。指定 record 名稱 `20261005T011008Z-8c3b601` 來自本任務提供的 TEAM 身分；公開 build receipt 用 manifest hash 對應記錄，未另列 record 持久化完成的精確時間。[BUILD_DEPLOYMENT][build]、[EXPECTATIONS][expected]

| 事件／來源 | 精確時間（UTC）與解讀 |
|---|---|
| Audit8 completion／publication | `2026-10-04T19:26:33.961Z`／`2026-10-04T19:26:58Z` |
| source manifest generatedAt | `2026-10-04T20:49:21.366210+00:00`；記載 clean committed source。[manifest][manifest] |
| source freeze | commit 精確固定；**獨立的 freeze clock timestamp 未在已讀公開收據列出，UNKNOWN**。不得把 manifest 產生時間當 commit／freeze 時間。 |
| TEAM 負 baseline verifier | `2026-10-05T01:06:58.721516+00:00` → `2026-10-05T01:06:59.264900+00:00`；expected exit 1 |
| TEAM artifact suite | `2026-10-05T01:06:59.322973+00:00` → `2026-10-05T01:07:00.054279+00:00` |
| TEAM standalone verifier | `2026-10-05T01:07:00.116799+00:00` → `2026-10-05T01:07:00.764437+00:00` |
| TEAM supported runner（private） | `2026-10-05T01:07:01.103622+00:00` → `2026-10-05T01:07:12.707405+00:00` |
| TEAM private full gate | `2026-10-05T01:07:12.773683+00:00` → `2026-10-05T01:08:43.839334+00:00` |
| TEAM clean private npm ci | `2026-10-05T01:08:43.898043+00:00` → `2026-10-05T01:08:56.378958+00:00` |
| TEAM clean private runner | `2026-10-05T01:08:56.674768+00:00` → `2026-10-05T01:09:06.783712+00:00` |
| TEAM clean verifier | `2026-10-05T01:09:06.843483+00:00` → `2026-10-05T01:09:07.408221+00:00` |
| TEAM staged deployment | `2026-10-05T01:10:08.607Z` → `2026-10-05T01:10:28.002Z` |
| TEAM TypeScript | `2026-10-05T01:10:09.010Z` → `2026-10-05T01:10:13.056Z`；exit 0 |
| TEAM Vite | `2026-10-05T01:10:13.443Z` → `2026-10-05T01:10:14.554Z`；exit 0 |
| TEAM Wrangler upload | `2026-10-05T01:10:14.998Z` → `2026-10-05T01:10:27.512Z`；exit 0 |
| expectations generatedAt | `2026-10-05T01:14:47.679Z`；預期值，不是觀測 |
| TEAM served readback | `2026-10-05T01:14:47.681Z` → `2026-10-05T01:14:55.834Z` |
| TEAM closure/test receipt capturedAt | `2026-10-05T01:21:28.261414+00:00` |
| REVIEWER `npm ci --ignore-scripts` | `2026-10-05T04:03:18.002114+00:00` → `2026-10-05T04:03:44.268854+00:00` |
| REVIEWER `node scripts/review-tests.mjs --check` | `2026-10-05T04:03:44.269660+00:00` → `2026-10-05T04:03:44.340113+00:00` |
| REVIEWER `npm run test:review` | `2026-10-05T04:03:44.340708+00:00` → `2026-10-05T04:04:08.238559+00:00` |
| REVIEWER `node scripts/verify-artifact-closure.mjs` | `2026-10-05T04:04:08.239179+00:00` → `2026-10-05T04:04:09.306818+00:00` |

TEAM 原始歷史失敗沒有被刪除或更名：[原 pinned test receipt][tests]，亦附 [逐位元組副本](evidence/TEAM-TEST_RESULTS.json)。`e97847bef60aad79a95b0a587b099a921aaabc13` clean-review-admin 613 tests／612 pass／1 fail、exit 1：TEAM 說明為測試觀察早於 logout completion，最終改等完成且保留 assertion。相同最終 candidate 的 Windows medium identity full 1663／1660／3 fail，以及 clean 613／610／3 fail，均為真實 file symlink EPERM、exit 1、cancel／skip／todo 零；後來 privileged acceptance 是另一次執行，不使先前失敗消失。最終 TEAM 負 baseline artifact verifier 13 assertions／4 pass／9 fail／0 skip、exit 1 是預期負校準，不能改記成成功 exit 0。[artifact receipt][artifactreceipt]

## 證據附錄 E：source → build → record → upload → readback

推論鏈的強弱應分開：REVIEWER 核對的是 141 公開位元組與宣告 manifest；TEAM 另以 exact private source、鎖檔、privileged gate、normal USER build/upload 與 authenticated readback 宣告完整對應。本次沒有 private Git、完整前端／model／response／build bodies、owner secrets 或私有 DB，因此無法由 hash 收據獨立重建整條鏈。[來源限制][reviewer]

| 對應鍵 | 值與歸屬 |
|---|---|
| Worker main | 316024 bytes；SHA256 `0d1c6176b09a73dac605c5f19a126c8b4ae4496fe659f1197a909e7f87c849e2`；TEAM cloud raw-byte match=true |
| Worker／traffic | `06cbc8fe-112f-4a11-b84f-42907179afff`／100%；TEAM |
| deployment manifest | `f786dfab027cdd5feeac12071766d2becc403a8bf321b03a75187de81ff38b4b`；build receipt 與 expectations 同值 |
| staged receipt | `fb35016de876b43ae0d2f8731b91de2348944963b6c20c2814c351e59d4580fb` |
| dist tree | `2bbd66f127f65292875df92e65c2d1e8fc8b70cd88e2249baa3c7e0d2d1eaa68` |
| public redacted wrangler | `d31cf588020f457d66c710926551d01f199fa19d7fa1506522acd8b48011a6dd`；私有原件 fingerprint withheld，不能用這個 hash 自證 live config |
| public headers | `010ed5e5bec891e5a806b2d224ecc0d962fc585fa761c8a7285251e8ae03cc07` |
| runtime | TEAM Node v24.19.0／viem 2.56.9／TypeScript 5.9.3／Vite 8.3.1／Wrangler 4.143.0 |

以上值均來自 [build][build] 與 [expectations][expected]。七 bindings 是 ASSETS、DB、ALCHEMY_API_KEY、API_LIMITER、SEAT_LIMITER、AUTH_LIMITER、CHAIN_LIMITER；限額依序為 API 180/60s、SEAT 60/60s、AUTH 20/60s、CHAIN 20/60s。這是設定讀回，不是壓測。runtime compatibilityDate `2026-05-15`、cpuMs 50、assets routing match。七 applied migrations：`0001_wallet_login.sql`、`0002_sign_in_budgets.sql`、`0003_sign_in_layers.sql`、`0004_index_candidates.sql`、`0005_lanes_and_subnets.sql`、`0006_members.sql`、`0008_member_hardening.sql`；pending=0，不能自行補出 0007。[TEAM config／D1 readback][build]

| TEAM 匿名 URL（皆 HTTP 200） | 開始 UTC／raw bytes | SHA256 |
|---|---|---|
| `https://imdember.com/` | `2026-10-05T01:14:47.681Z`／2618 | `cc0e1cf85a60c2afb2fbee36847d69e18a5f5c058e6a1eca5b424654ee984265` |
| `https://imdember.com/assets/index-ClYR0IrS.js` | `2026-10-05T01:14:49.738Z`／1553842 | `71299ccf931e034ef5e7c9bba4d128ec2becac73418e5b47c23837202da31589` |
| `https://imdember.com/assets/index-Ym1X_eiK.css` | `2026-10-05T01:14:52.131Z`／68142 | `be70f6c11b0030c3401c1bce007e58a37cd6cb39e9adb9ffd5c6758582e6142a` |
| `https://imdember.com/assets/InteriorView-B8CZAtGZ.js` | `2026-10-05T01:14:53.807Z`／93242 | `287433410626b8171a5ff8ff2e071241e700971e59319d71f5d71229c915c473` |
| `https://imdember.com/api/auth/session` | `2026-10-05T01:14:55.637Z`／18 | `60483fbb3c01c4080583563e215e3ca4ab5ce4ff74f47cf36eadedd152572d2f` |

這是 [TEAM 當時讀回][served]，不是本次取得的新 production response。四個靜態 body 的 raw bytes/hash 與 build comparison 一致（HTML 2618、mainJS 1553842、CSS 68142、InteriorView 93242），同時 security headers match；HTML `public, max-age=0, must-revalidate`，assets `public, max-age=604800`，全無 Set-Cookie。靜態回應包含 `X-Content-Type-Options: nosniff`、`X-Frame-Options: DENY`、HSTS `max-age=31536000; includeSubDomains`、`Referrer-Policy: strict-origin-when-cross-origin`、`Permissions-Policy: camera=(), microphone=(), geolocation=()` 與下列 CSP：

```text
default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob: https://nft-cdn.alchemy.com; connect-src 'self' blob: https://api.dexscreener.com; object-src 'none'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'
```

匿名 `/api/auth/session`：`signedIn:false`、`Cache-Control: no-store`、無 Set-Cookie／Access-Control-Allow-Origin；`Cross-Origin-Resource-Policy: same-origin`、CSP `default-src 'none'; frame-ancestors 'none'`。這無法驗證登入 cookie 的 Secure／HttpOnly／SameSite 或真正簽名控制。[TEAM session receipt][served]

本次 `node Submission9/verify-served-readback.mjs` exit 0，只得 `VALIDATED_NO_NETWORK_REQUESTS`，不是 served PASS。[預設輸出](evidence/served-plan.json)。未使用 `--execute`。若後續獲准選擇既定可選測量，腳本僅五次 GET、相隔 1500ms、credentials omit、redirect error、每回應 8MiB／30s 上限、不 retry、不保存 body；HTML 的單一 managed analytics removal 是明確 qualified comparison，不能與 raw match 混寫。本次不以晚於 snapshot 的網頁狀態改寫 TEAM 舊時點。即使五個 GET 全綠，也不能識別 active Worker UUID／bindings／traffic／D1。[固定 verifier][servedverifier]

舊 known-good rollback source `bb7549e0a2576ba4da0ea7c4147c4aba1a7f577f`／Worker `cdd3ef36-ca81-439a-8798-a64e30cf01d3`／main hash `7fafc4c62af05efa33b9153a7aa7b094ac31b3a31a546429baa096c61435c66c` 是歷史保留身分，沒有本次 rollback 執行。其 canonical upload exit 0、overall exit 1（upload 後 local final-directory EPERM）與本次分階段 deployment 成功不可合併。[歷史 invocation][build]

## 證據附錄 F：尚待回答與行動

| 門檻 | 目前地位 | 必要動作／為何不能外推 |
|---|---|---|
| 五項指定反例 | REVIEWER 有界 PASS | 保留本 pin 回歸及負基線收據；來源改動後重評估，無現存指定 blocker。 |
| 完整 source/build reproducibility | 公開 checkout BLOCKED；私有對應 TEAM | 由有權取得私有完整輸入者核驗 freeze time、build inputs、record persistence 精確時間與 config；不要求公開秘密。 |
| upload／record／authenticated Cloudflare verification | TEAM 測量支持；REVIEWER UNKNOWN | 逐項核驗 Worker bytes、UUID／traffic、binding、migration 收據；不得以匿名 HTTP 代替。 |
| authenticated cookie／ERC1271／login truth／phishing 與 same-origin writes | UNKNOWN | 另行授權、隔離的真實環境與錢包測量；本次無 login、signature、write。 |
| browser／hostile provider／D1／process death | UNKNOWN | 真實 browser/device/provider matrix、D1 interleavings 與故障恢復證據；SQLite fixture 不能取代。 |
| WAF／limiter／upstream／global concurrency／cron | UNKNOWN | 另行有界計畫；本次沒有 stress、cron 或 authenticated production 操作。 |
| hostile artifact ancestors／SMB／NFS | 不在已接受的本機受控 root 假設 | 若產品需要該威脅模型，新增 OS 層保障與 race 測量；目前不宣稱解決。 |
| auxiliary native updater | REVIEW／sync/version 未量測 | Managed Cloudflare 與 filtered snapshot 不含 generic self-updater；與五項回歸分開。[TEAM disposition][reviewer] |

所有「PASS」都應帶著對象、來源與時間閱讀。本文不執行 deployment、transaction、approval、mint、payment、wallet signature 或私有資料庫存取；沒有用交付檔案結構檢查替代行為證據。

[matrix]: https://github.com/tungweb3/imd-ember-world-review/blob/347268a7ecae700088547c2402db9a3eb07a6fd2/Submission9/FinalClosure/CLOSURE_MATRIX.md
[readme]: https://github.com/tungweb3/imd-ember-world-review/blob/347268a7ecae700088547c2402db9a3eb07a6fd2/Submission9/README.md
[inputs]: https://github.com/tungweb3/imd-ember-world-review/blob/347268a7ecae700088547c2402db9a3eb07a6fd2/Submission9/REVIEW_INPUTS.md
[priors]: https://github.com/tungweb3/imd-ember-world-review/blob/347268a7ecae700088547c2402db9a3eb07a6fd2/Submission9/PRIOR_REVIEWS.md
[ownership]: https://github.com/tungweb3/imd-ember-world-review/blob/347268a7ecae700088547c2402db9a3eb07a6fd2/source/server/ownership.ts#L225
[owntest]: https://github.com/tungweb3/imd-ember-world-review/blob/347268a7ecae700088547c2402db9a3eb07a6fd2/source/tests/ownership-audit8.test.mjs
[auth]: https://github.com/tungweb3/imd-ember-world-review/blob/347268a7ecae700088547c2402db9a3eb07a6fd2/source/src/world/auth.ts#L580
[authtest]: https://github.com/tungweb3/imd-ember-world-review/blob/347268a7ecae700088547c2402db9a3eb07a6fd2/source/tests/auth-audit8.test.mjs
[artifact]: https://github.com/tungweb3/imd-ember-world-review/blob/347268a7ecae700088547c2402db9a3eb07a6fd2/source/tests/auth-artifacts.mjs
[artifacttest]: https://github.com/tungweb3/imd-ember-world-review/blob/347268a7ecae700088547c2402db9a3eb07a6fd2/source/tests/auth-artifacts.test.mjs
[verifier]: https://github.com/tungweb3/imd-ember-world-review/blob/347268a7ecae700088547c2402db9a3eb07a6fd2/source/scripts/verify-artifact-closure.mjs
[runner]: https://github.com/tungweb3/imd-ember-world-review/blob/347268a7ecae700088547c2402db9a3eb07a6fd2/source/scripts/review-tests.mjs
[artifactreceipt]: https://github.com/tungweb3/imd-ember-world-review/blob/347268a7ecae700088547c2402db9a3eb07a6fd2/Submission9/FinalClosure/ARTIFACT_CLOSURE.json
[manifest]: https://github.com/tungweb3/imd-ember-world-review/blob/347268a7ecae700088547c2402db9a3eb07a6fd2/manifests/submission9-published-source.json
[tests]: https://github.com/tungweb3/imd-ember-world-review/blob/347268a7ecae700088547c2402db9a3eb07a6fd2/Submission9/FinalClosure/TEST_RESULTS.json
[build]: https://github.com/tungweb3/imd-ember-world-review/blob/347268a7ecae700088547c2402db9a3eb07a6fd2/Submission9/FinalClosure/BUILD_DEPLOYMENT.json
[served]: https://github.com/tungweb3/imd-ember-world-review/blob/347268a7ecae700088547c2402db9a3eb07a6fd2/Submission9/FinalClosure/SERVED_READBACK.json
[reviewer]: https://github.com/tungweb3/imd-ember-world-review/blob/347268a7ecae700088547c2402db9a3eb07a6fd2/Submission9/FinalClosure/REVIEWER_EVIDENCE.json
[expected]: https://github.com/tungweb3/imd-ember-world-review/blob/347268a7ecae700088547c2402db9a3eb07a6fd2/Submission9/SERVED_EXPECTATIONS.json
[servedverifier]: https://github.com/tungweb3/imd-ember-world-review/blob/347268a7ecae700088547c2402db9a3eb07a6fd2/Submission9/verify-served-readback.mjs
[audit]: https://github.com/Identity-md/research/blob/d7f6e26bf449d9c5ea3a1ecb6557ca3adbd23632/jobs/7716c3f5-5d6c-4953-a643-141da678d051/files/AUDIT.md
[priorreport]: https://github.com/Identity-md/research/blob/cdadc2923c04e905212f1f203b40aaf38cb65508/jobs/38438c89-b34c-4d38-8ae8-027c9d175fb1/files/artifacts/report.md
