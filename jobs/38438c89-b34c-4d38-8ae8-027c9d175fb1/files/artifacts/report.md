# IMD Ember World：第八次 Swarm／Audit7 閉合與發布就緒覆核

## 主報告（2026-10-05 釘選快照截止）

**尚未八項全閉合。**本次獨立離線結果支持六項 Low 與第七項 Info 判為 `fixed locally`；第八項 Info 為 `partial`，找到 opt-in 輸出逃逸與路徑遮罩缺口。**SOURCE-CLOSURE：BLOCKED（第八項完整閉合要求）；RELEASE-READINESS：UNKNOWN／不得宣告就緒**，另須先修復來源缺口。這是有限覆核，並非承諾通過、認證、零漏洞或資金安全結論。[八項原申報][M]、[本次反例](#附錄二第八項未閉合反例)。

對象僅為公開 `88c130283efc45260f9e00da8d2d3055c38483bd`，比較 `7215c5d89a96bc79113a85766c04868d54393f3c`；私有凍結來源標示 `bb7549e0a2576ba4da0ea7c4147c4aba1a7f577f`。下載後獨立核對公開 manifest 的 140 個檔案，零雜湊差異；124 exact、16 保留遮罩、57 masked lines 的私有對應則仍屬 TEAM provenance。沒有私有歷史與完整前端，不能把公開核對改稱私有原件驗證。[manifest][P]

本案是非官方 TypeScript Cloudflare Worker／React SIWE，沒有 Solidity。永久公開名稱具有寫入路徑，World 並非完全唯讀；審查集中 Auth／provider／server authority、ownership proof／index／budget、freshness／numbers，排除 Genesis、Mint、經濟、場景、影音與其他視覺功能。沒有 live site/API 請求、真實錢包簽名、資產操作或部署。[範圍][R]、[伺服器邊界][B]

八列 TEAM 初始狀態一律是 `INDEPENDENT_PENDING`，下表才是本次有界裁決；基線欄指同 evaluator 的局部對照，非完整舊版重跑。詳細指令、行號與實際 rows/counts 見附錄。[政策][C]

| 項／嚴重度 | 先前行為；政策與修補／測試路徑 | 基線控制 → 候選證據 | 裁決、阻斷理由與保留限制 |
|---|---|---|---|
| 1 Low | 被動 discovery 撤 session；`auth.ts`／`wallet.ts` 分開 selection，`auth-audit8` | 舊物件／首次發現反例失敗 → session `1/1/0`，零 prompt／cleanup | fixed locally；無此來源阻斷。主動選擇與已觀測帳戶變更仍清舊 context；真擴充功能未知。[A] |
| 2 Low | 重疊 home 重複 index／budget；`ownership.ts` 使用 live clock，`ownership-audit8` | 舊版放大 → ordinary20、fresh20 各 index／admission／proof `1/1/1` | fixed locally；refused 維持 limited，expiry 重證。單 isolate 合併不等於全球 RPC 上限。[O] |
| 3 Low | lock503 後同帳戶 unlock 撤 committed row；`auth.ts` 維持 reconcile-only，`auth-audit8` | 舊兩模式失敗 → live1、cleanup0、owner RELEASED，後 stop 不撤 | fixed locally；真正帳戶／provider／lifetime 改變仍 fenced。停止頁面／程序死亡責任有限。[A] |
| 4 Low | 普通 read 丟有效 signature；`auth.ts` 保留 own preflight，`auth-audit8` | 舊 ABSENT verify0 → prompt／challenge／verify `1/1/1` | fixed locally；PRESENT／UNKNOWN／context／expiry 仍阻擋；GET 非跨頁原子鎖。[A] |
| 5 Low | 獨立 proof 意圖繼承失敗；`ownership.ts` settlement 後重評，`ownership-audit8` | 舊 changed-roster／fresh 失敗 → 503 後200，index1／budget1／RPC2 | fixed locally；同 cohort 共用失敗、後 retry 恢復；512 active cap 無 live eviction，仍非全域容量。[O] |
| 6 Low | 小 remote skew 進 failure ladder；`freshness.ts`／`cadence.ts`／`market.ts`，`clock-skew-audit8` | 舊報告重現 → 60000ms inclusive；60001／NaN／Infinity 拒絕 | fixed locally／policy decision；僅公共顯示容差，authority 嚴格 age／TTL，合法負變動保留。[F] |
| 7 Info | warm 改 producer stamp；`gateway.ts` 保留 fetchedAt，`clock-skew-audit8` | 舊 `Math.min` → 原 timestamp 與 source lineage 留存、exact TTL refresh | fixed locally；非阻斷。容許 remote skew 不延長 proof/session authority，實際 isolate skew 未測。[G] |
| 8 Info | 預設 sibling artifacts／機器路徑；`auth-artifacts.mjs`／runner，artifact／runner tests | 舊公開紀錄 → default0、23檔真 viem；新增懸空 symlink 可逃逸、`/root/...` 未遮罩 | partial；阻斷完整 SOURCE-CLOSURE。僅 opt-in、本地檔案控制，未發現 wallet 權限提升；詳附錄。[H] |

授權底線仍是 authenticated address 的 `ownerOf`，index、roster、D1、名稱及 memberID 只提供候選。checkedAt 固定 30 秒，same-block delta 不續 deadline，256 attempted IDs 包含失敗；lane 等待後以新 clock 判斷，過期需 latest block，unavailable／limited 不能當 complete-empty。本次 refused-budget、held RPC 到期及 sold-seat 控制通過；未發現新的 scoped authority、cross-revoke、無界 RPC 或 methods／headers 擴張。[O]、[既有控制][V]、[邊界][B]

清理仍須每事件一個 primary CleanupPlan；displayed expectedAddress 與 retained expectedNonce 責任不同，terminal owner 不復活。完整套件保留十一事件矩陣與 old-A-nonce／new-A-row、lock503／later-valid、passive provider、ordinary-read-during-prompt 控制。計畫、重試、有效撤銷不可混計；dispatch、Worker commit、Set-Cookie、fetch visibility、body delivery 亦分離，晚 header 仍可能影響 cookie，但不得跨撤新 row。[事件矩陣][E]、[nonce／lock控制][N]

Node `v24.21.0`、真鎖定 `viem 2.56.9` 的新執行為 23 檔、574/574、exit0、零 skip；core500／428 distinct 與 additional90／54 distinct 均本次另有指令與雜湊。原公開574、core500、additional90是 inherited executions，140 raw inputs／evaluator 未變不代表重跑；500 與90不是590個唯一排列，calibration 不是 seeds。第一次 npm cache 唯讀失敗與基線 selector／未完成廣泛對照均保留，沒有 shim 或略去候選失敗。[繼承紀錄][T]、[runner][R]、[本次證據](reviewer-evidence.json)

發布證據只支持 TEAM 在當時測得 Worker `cdd3ef36-ca81-439a-8798-a64e30cf01d3`、traffic100%、bindings／七 migrations、指定資產與 headers 相符；私有1606/1606、TypeScript、Vite及 Wrangler upload0 皆為成功子步驟。record `20261004T180257Z-bb7549e` 最後本地 rename EPERM，**整體 exit1** 必須保留。未變 pending record 復原與 upload／HTTP 對應另行核對，不是測試失敗，也不能改寫成 overall0或公開完整前端編譯成功。[部署收據][D]

先前 Report 的「fixed locally」與 Audit 的新反例不同，捕獲 originals 雜湊已獨立相符；兩者是比較證據，不替此候選背書。[先前原件][PR] 本次剩餘工作是封閉懸空 symlink／遮罩缺口並重跑反例，以及在授權且可取得環境時另做部署、瀏覽器與操作關卡。外部 readback 本次全是 TEAM 測量；WAF、D1 內部交錯、多 isolate、hostile-wallet、程序死亡與 withheld visuals 仍 unknown。有界可用性犧牲與 Info 不直接表示資金危險，也不能以 Low／Completed／accepted 消除未知；時間點 byte equality 不是永久全站 parity。[部署限制][D]、[runner限制][R]

第一項的政策選擇有具體後果：第一次發現錢包時，瀏覽器既有登入地址可能與錢包回報地址不同；這不是已建立錢包身份的變更，因此不能只憑被動發現撤銷登入。測試實際保留一筆有效登入資料列，同時顯示不同的錢包帳戶，沒有自動簽名或新增登入。另一方面，使用者明確選擇另一個錢包，即使地址相同，仍是新的操作意圖；已觀測帳戶改變也須清除舊上下文。這些相反控制都存在，不能只測「保留登入」便宣稱所有切換安全。[A]

第三項須看伺服器已提交的資料，而不是客戶端是否收到可解析回覆。注入的損壞驗證本文不會回滾已提交登入，也不會抹掉已處理的回應標頭；鎖定後首次查詢失敗，只能留下待釐清責任。本次在同一帳戶解鎖後讀到正式登入狀態，釋放責任，稍後停止也沒有撤銷。相反，解鎖到另一帳戶會使用舊流程的條件式責任清理，不能替新帳戶自動登入。晚到的舊回覆不能把已釋放責任改回有效，這是資料列與責任狀態共同支持的判斷。[A]、[N]

第四項的修復不是取消每次點擊前的查詢。候選仍先取得該次點擊自己的正式回覆；簽名等待期間，另一次普通查詢回報「未登入」，只更新回覆排序，不單憑序號增加丟掉簽名。本次反向控制還包含先看見已登入或未知、之後再回到未登入；這不能恢復先前已失效的簽名資格。挑戰壽命從請求派送開始計算，包含網路和提示等待；恰好五分鐘、時間倒退或非有限時間都停止驗證。伺服器的 nonce 截止與原本裝置時鐘容差仍各自保留。[A]、[C]

第二、五項的成本與授權也須分看。索引讀取完成時間若晚於另一請求的起始時間，使用後者會把有效索引誤判為未來資料，導致同批讀取重複支付預算。本次推進時鐘的兩批測試各自只讀一次索引；預算拒絕控制則沒有偷渡索引讀取。前一證明失敗時，完全相同的等待者共同收到有限失敗，獨立名冊或重新發現意圖則在前者結束後重新判斷；後續成功不是把失敗資料補上一個新時間戳。被限流、未能完成候選集合與確實完整的空集合因此保留不同結果。[O]、[V]

第六、七項接受的時鐘容差只改變公共資料顯示與輪詢分類，不授權身份、名稱寫入或房屋權限。暖拷貝保留生產者時間，使讀者能看見資料來源與年齡；不能以接收時間重新包裝成新證據。合法負市場變動有意保留，而價格、樓地板數值、換算率與衍生乘積的非有限值會拒絕或移除。這些測試支持指定數值入口，並不等於完成市場機制、視覺效果或實際交易的審查。[F]、[G]、[V]

第八項的新增反例不需要競態或真實帳號：先建立允許名稱的懸空符號連結，再要求輸出，目標尚不存在使存在性檢查略過連結檢查，最後普通寫檔跟隨連結。另一反例只是合成錯誤訊息中的本機絕對路徑。影響條件是啟用輸出且本機檔案可被布置，故維持資訊級；未證明遠端攻擊者能控制檔案，也未發現登入資料外洩。然而任務明定拒絕逃逸與遮罩機器路徑，不能把預設不寫檔的成功延伸為選用模式完整安全。修復應增加這兩種負控制，再保留可重播的動作與別名。[H]、[反例](#附錄二第八項未閉合反例)


---

## 證據附錄（不計主報告字數）

### 附錄一：取得、指令、歸屬與失敗收據

本次以 GitHub codeload GET 取得兩個 exact public commit 的乾淨 archive（未取得私有 Git history）。此 archive extraction 是新來源樹，並非含 `.git` 的 clone；版本由 URL 固定，manifest 再逐檔核對。安裝與執行全部位於 `/tmp` 的外部工作副本，提交的靜態報告不需要 Node、網路或第三方依賴，也未修改本 repository 的 node_modules／環境設定。下載的是 lockfile 所指定的真實套件，没有 stub、shim、手動 fixture patch 或私人 selector 混入 candidate command。測試附加檔及 opt-in tmp 不列為 140 source inputs；核對 inputs 仍零差異。

```sh
# archive: https://codeload.github.com/tungweb3/imd-ember-world-review/tar.gz/88c130283efc45260f9e00da8d2d3055c38483bd
# baseline: https://codeload.github.com/tungweb3/imd-ember-world-review/tar.gz/7215c5d89a96bc79113a85766c04868d54393f3c
cd /tmp/imd-r8-review/source
node --version
npm ci --ignore-scripts
# initial exit226: npm EROFS, /root/.npm cache read-only; downstream commands not run
npm_config_cache=/tmp/r8-npm-cache npm ci --ignore-scripts
npm run test:review -- --check
npm run test:review
# exits 0 / 0 / 0; Node v24.21.0; viem2.56.9; 23 files; 574/574
AUTH_REFERENCE_ARTIFACT_DIR=tmp/reviewer-r8 node --test --test-reporter=tap tests/auth-reference-scheduler.test.mjs tests/auth-audit8-causal.test.mjs
# exit0; 30/30 test cases; optional evidence inspection, not 30 new seeds
node scripts/replay-auth-trace.mjs --replay tmp/reviewer-r8/fixed-0-lost-hint.json
node scripts/replay-auth-trace.mjs --replay tmp/reviewer-r8/fixed-2-audit-hint-while-prompt.json
# both exit0; full explicit actions; no random re-selection
```

Supported runner 用 `node --test --test-reporter=tap --test-concurrency=3`，保留所有23檔；會刪除每個 `_SOURCE` 與 `NODE_OPTIONS`，檢查 Node24、local viem 與 lockfile 的一致性。測试中的純 oracle calibration 故意拒絕 UNKNOWN prompt、缺少 own preflight、duplicate prompt/hint、terminal nonce revival、stale projection、dead-cookie fallback 及 empty replay，不是 production failure 或 skip。[runner][R]、[純模型測試][Q]

下列基線實驗有意在 supported runner 外進行。`baseline` 指向前一 public snapshot 的 source，套件解析使用相同真實 lock 安裝。Auth fixtures 由候選 evaluator 載入舊 AuthClient／Worker／harness；WalletRegistry 仍由 evaluator 的候選 import 提供，故這是**局部 source substitution 控制**，不能聲稱全舊版端到端執行。ownership evaluator 的 `AUDIT8_SOURCE` 則載入舊 ownership／market／harness。

```sh
AUTH_R7_SOURCE=/tmp/imd-r7-review/source AUDIT8_SOURCE=/tmp/imd-r7-review/source node --test --test-reporter=tap tests/auth-audit8.test.mjs tests/ownership-audit8.test.mjs
# exit1: Auth fixture path guard rejects that spelling (not product failure).
# Ownership completed: 10 cases; 2 pass / 8 fail; no skips.
AUTH_R7_SOURCE=../baseline AUDIT8_SOURCE=../baseline node --test --test-reporter=tap tests/auth-audit8.test.mjs tests/ownership-audit8.test.mjs
# broad before-fix comparison did not finish; interrupted with Ctrl-C, exit130; no aggregate pass claim.
AUTH_R7_SOURCE=../baseline timeout 15s node --test --test-reporter=tap --test-name-pattern='passive same-address-object|passive first provider|held-verify lock503|invalid-verify-body lock503|ordinary canonical ABSENT ' tests/auth-audit8.test.mjs
# completes before timeout: exit1; 0 pass / 5 fail / 0 skip; expected before-fix policy counterexamples.
node artifacts/reproduce-clock-control.mjs /tmp/imd-r7-review/source
node artifacts/reproduce-clock-control.mjs /tmp/imd-r8-review/source
# run these two from repository root; both exit0, measurements below.
```

Clock control 首次用了 `source(..., shared)` 的錯誤參數入口，沒有進 warm path；該輸出不採作 warm closure 證據。修正為 `snapshot(undefined, shared)` 後，舊版 `remotePlus1:false, warmTimestamp:1000000`；候選 `remotePlus1:true, warmTimestamp:1059000`，producer `1059000`、local `1000000`。原錯誤與修正版 raw log hashes 均保留。候選的正式 clock tests 另驗證 exact skew／TTL 與 polling failure ladder，不依賴這個小 probe。[F]、[G]

原 TEAM public574／core500／additional90 是 `f94d2aa6a5c451eefbbfc8452bf70a56c11b284f` 的 inherited executions，candidate lineage receipt `2b55f450964b25e2a3d0df8c061c0daf6205dc201a51701d83f45dae0d52a331`；本次新 reviewer 執行的 commands、counts、exit 及 raw stdout hashes 在下表。[T]、[TEAM scheduler][S]

| 新 reviewer campaign | cases/seeds | distinct digests | Worker／SQLite／cookie／projection comparisons |
|---|---|---|---|
| default all23 | 574/574 test cases；fail0/cancel0/skip0/todo0 | 非排列計数 | 以下兩 campaign 是其中的 checks，不能與574加總 |
| core | 500/500 seeds | 428 | 3572 / 5477 / 3649 / 3402；38 pre-header failures |
| additional | 90/90 schedules；三 kernel 各30 | 54 | 646 / 1006 / 676 / 660；0 pre-header failures |
| opt-in inspection | 30/30 test cases | 再產生相同500與90 campaigns；非新增唯一覆蓋 | 完整 traces 另交付於 `traces/` |

CLI core seed0 replay digest `93550e7acb3a1a47516f612b0f268ec8b8ffb51f7f8173a7d7e8b4937d4687e2`，additional seed2 digest `b50d04c6f0d918b67876467885e645b5215ad0fcbe5cd7f7795292c44894f77a` 與保存 trace 一致。Replay 的 checkpoint comparison 次數較 seed execution 少，實際 action、final rows 與 digest 相符；不混報其 metrics。測試內另有原完整動作重播、empty replay拒絕與純模型負控制；本次沒有 product-failure trace 的刪除最小化執行，也沒有聲稱最小反例證明。[replay code][J]

### 附錄二：第八項未閉合反例

**R8-INFO-ARTIFACT-01：懸空 output symlink 未拒絕（Info，partial／SOURCE-CLOSURE blocker）。**Pinned [`auth-artifacts.mjs` L28-L32][H] 以 `existsSync(path)` 才決定是否 lstat；懸空 symlink 的目標不存在時回 false，随后 `writeFileSync` 跟隨連結。這是確定性失敗，不需要 TOCTOU。已存在、非懸空的 directory symlink 控制有通過；不足以覆蓋 output 懸空連結。

```sh
node artifacts/reproduce-artifact-gap.mjs /tmp/imd-r8-review/source
# exit0 = probe成功完成；以下是 policy violation 的量測，不是 closure pass：
# {"case":"dangling-output-symlink","targetExistedBefore":false,"writeReturned":true,
#  "outsideAllowedTreeCreated":true,"body":{"proof":"offline-fixture"}}
```

Probe 在一個全新 synthetic sourceDir 下建立 `tmp/replay/core500-RESULT.json` symlink，指向同 fixture 根部 `outside-source-tmp.json`（在 source/tmp 外）；沒有碰真實專案檔、既存資料或 credentials。建立 store 與 write 都成功。實際 scheduler RESULT 也使用同一 store/write 路徑，故推論 opt-in scheduler 輸出可有相同逃逸；沒有實測任意真實受保護系統檔。修復方向為對目錄項本身檢查而非只檢查目標存在性，寫入時拒絕 symlink／非regular file，並評估 check/use 間的變更；需加入 dangling output、既有非regular、junction及 replay 保留控制。未執行 Windows junction，不能把 POSIX reproducer 冒充跨平台驗證。

**R8-INFO-ARTIFACT-02：遮罩不是完整本機路徑政策（Info，同列）。**Pinned [`auth-artifacts.mjs` L10][H] 只匹配 drive-letter、`/Users/`、`/home/`、`/tmp/`。`sanitizeArtifact('failure at /root/reviewer/private/project.ts')` 原樣返回。字串是合成測試資料，不是本機配置披露；`sourceRoot` 等特定 keys 確有刪除，但 nested error message 的 `/root/` 未被涵蓋。修復應保持 relative input paths、actions、nonce aliases 可重播，同時遮罩其他絕對本機路徑；不要把 URL 誤當檔案路徑。未測出的其他路徑格式不作確定外洩結論。

Default scheduler artifact disabled 已通過，source inputs unchanged；本地允許的 opt-in 失敗不意味任何遠端錢包 authority 漏洞。因此 Info impact 限於 reviewer 機器檔案與可能的私有路徑證據 hygiene。它仍是任務明确 invariant 的失敗，不能宣稱八項全閉合。這兩個新增控制揭露了補丁的未覆蓋分支；不是把已知舊預設外寫問題原樣重報。[artifact tests][AT]

### 附錄三：八列直接 rows／counts 與控制界線

資料記號：`S=created/live/revoked`；`C=total/used/pending/invalidated`；`P/Q/V/L/H`=本頁 actual personal_sign／challenge dispatch／verify dispatch／cleanup dispatch／hint emission。已先用 fixture browser 登入的 seed setup 不計入本頁 P/Q/V，但資料列會含該 setup；故不得把 row1與本頁verify0視為矛盾。`pending` 是 SQL used_at/invalidated_at 的分類；時鐘到期可能仍保留未使用 row，不能說它仍可 verify。

全26個 Auth diagnostics（含 request order、Set-Cookie count、visibleStatus、plans、owner）與67個 ownership diagnostics 存於 [reviewer-evidence.json](reviewer-evidence.json)。以下列出重點；其餘反向控制已在同23檔命令執行，非僅 test 名稱閱讀。

| 控制／事件順序 | 實際 S；C | P/Q/V/L；其他觀測 |
|---|---|---|
| `late-announcement` | 1/1/0；1/1/0/0 | 0/0/0/0；owner `none`；cleanup `[]` |
| `second-wallet` | 1/1/0；1/1/0/0 | 0/0/0/0；owner `none`；cleanup `[]` |
| `same-address-object` | 1/1/0；1/1/0/0 | 0/0/0/0；owner `none`；cleanup `[]` |
| `same-address` | 2/1/1；2/2/0/0 | 1/1/1/1；owner `RELEASED`；cleanup `[{"nonce":false,"address":true,"status":204}]` |
| `different-address` | 2/1/1；2/2/0/0 | 1/1/1/1；owner `RELEASED`；cleanup `[{"nonce":false,"address":true,"status":204}]` |
| `late first provider without prior wallet account` | 1/1/0；1/1/0/0 | 0/0/0/0；owner `none`；cleanup `[]` |
| `accountsChanged` | 1/0/1；1/1/0/0 | 0/0/0/1；owner `none`；cleanup `[{"nonce":false,"address":true,"status":204}]` |
| `passive-different-account` | 1/0/1；1/1/0/0 | 0/0/0/1；owner `none`；cleanup `[{"nonce":false,"address":true,"status":204}]` |
| `held-verify` | 1/1/0；1/1/0/0 | 1/1/1/0；owner `RELEASED`；cleanup `[]` |
| `invalid-verify-body` | 1/1/0；1/1/0/0 | 1/1/1/0；owner `RELEASED`；cleanup `[]` |
| `stale lock callback/newer accepted generation` | 2/2/0；2/2/0/0 | 1/1/1/0；owner `RELEASED`；cleanup `[]` |
| `different account unlock` | 1/0/1；1/1/0/0 | 1/1/1/1；owner `CONSUMED`；cleanup `[{"nonce":true,"address":false,"status":204}]` |
| `held signature/ABSENT` | 1/1/0；1/1/0/0 | 1/1/1/0；owner `RELEASED`；cleanup `[]` |
| `held signature/PRESENT-same` | 1/1/0；2/1/0/1 | 1/1/0/0；owner `none`；cleanup `[]` |
| `held signature/PRESENT-other` | 1/1/0；2/1/0/1 | 1/1/0/0；owner `none`；cleanup `[]` |
| `held signature/UNKNOWN` | 0/0/0；1/0/1/0 | 1/1/0/0；owner `none`；cleanup `[]` |
| `held signature/UNKNOWN-then-ABSENT` | 0/0/0；1/0/1/0 | 1/1/0/0；owner `none`；cleanup `[]` |
| `held signature/PRESENT-then-ABSENT` | 1/0/1；2/1/0/1 | 1/1/0/0；owner `none`；cleanup `[]` |
| `held signature/expired` | 0/0/0；1/0/1/0 | 1/1/0/0；owner `none`；cleanup `[]` |
| `held signature/exact-deadline` | 0/0/0；1/0/1/0 | 1/1/0/0；owner `none`；cleanup `[]` |
| `held signature/clock-rollback` | 0/0/0；1/0/1/0 | 1/1/0/0；owner `none`；cleanup `[]` |
| `held signature/invalid-clock` | 0/0/0；1/0/1/0 | 1/1/0/0；owner `none`；cleanup `[]` |
| `held signature/account-switch` | 0/0/0；1/0/1/0 | 1/1/0/0；owner `none`；cleanup `[]` |
| `repeated ordinary ABSENT` | 1/1/0；1/1/0/0 | 1/1/1/0；owner `RELEASED`；cleanup `[]` |
| `held old-cookie ordinary read/sibling accepted` | 1/1/0；2/1/0/1 | 1/1/0/0；owner `none`；cleanup `[]` |
| `ordinary ABSENT supersedes one same-click recheck` | 1/1/0；1/1/0/0 | 1/1/1/0；owner `RELEASED`；cleanup `[]` |

Hints 不在原 `record()` diagnostic 中直接輸出，故該表不填假0；下列補充腳本量測 hint 與 actual per-row fields。Auth trace 的 individual index/budget/RPC 未全部印出，不能推論為0；ownership獨立量測如下。每 event 的 plan list 与真正 POST 是不同資料，RETAINED→RELEASED 是釋責而非撤銷。鎖後查詢失敗時 `RETAINED`、same-account unlock canonical PRESENT後 `RELEASED`、later stop plan `none`，实际 revocation0。

```sh
node artifacts/reproduce-rows.mjs /tmp/imd-r8-review/source
# exit0；使用原真實 AuthClient／Worker／SQLite harness，synthetic keys only
```

這個補充 passive probe 是同一 bound provider 的被動通知；替換物件／first／late／reannounced provider 由上表正式 tests與WalletRegistry source補足。會隨機生成測試地址，但下列保持所量測地址、時間、關係；nonce 轉成對應 `N1` 別名，不公布合成 bearer token。

**passive provider / accepted**

```json
{
  "label": "passive provider / accepted",
  "sessions": [
    {
      "nonce": "N1",
      "address": "0x42ab92abc290202f7b3b12fb85768ed7f564fd9d",
      "expires_at": 1791201600000,
      "revoked_at": null,
      "alias": "S1"
    }
  ],
  "challenges": [
    {
      "nonce": "N1",
      "used_at": 1790596800000,
      "invalidated_at": null
    }
  ],
  "counts": {
    "created": 1,
    "live": 1,
    "revoked": 0,
    "challenges": 1,
    "used": 1,
    "pending": 0,
    "invalidated": 0
  },
  "prompts": 0,
  "challenge": 0,
  "verify": 0,
  "cleanup": [],
  "hints": 0,
  "plans": []
}
```

**lock503 / before unlock**

```json
{
  "label": "lock503 / before unlock",
  "sessions": [
    {
      "nonce": "N1",
      "address": "0x6af6ca319213b924e4b94a1de96a6e502a09aa74",
      "expires_at": 1791201600000,
      "revoked_at": null,
      "alias": "S1"
    }
  ],
  "challenges": [
    {
      "nonce": "N1",
      "used_at": 1790596800000,
      "invalidated_at": null
    }
  ],
  "counts": {
    "created": 1,
    "live": 1,
    "revoked": 0,
    "challenges": 1,
    "used": 1,
    "pending": 0,
    "invalidated": 0
  },
  "prompts": 1,
  "challenge": 1,
  "verify": 1,
  "cleanup": [],
  "hints": 0,
  "plans": [
    {
      "eventId": 1,
      "reason": "lock",
      "kind": "reconcile",
      "flowId": 1
    }
  ],
  "owner": "RETAINED"
}
```

**same-account unlock / canonical release**

```json
{
  "label": "same-account unlock / canonical release",
  "sessions": [
    {
      "nonce": "N1",
      "address": "0x6af6ca319213b924e4b94a1de96a6e502a09aa74",
      "expires_at": 1791201600000,
      "revoked_at": null,
      "alias": "S1"
    }
  ],
  "challenges": [
    {
      "nonce": "N1",
      "used_at": 1790596800000,
      "invalidated_at": null
    }
  ],
  "counts": {
    "created": 1,
    "live": 1,
    "revoked": 0,
    "challenges": 1,
    "used": 1,
    "pending": 0,
    "invalidated": 0
  },
  "prompts": 1,
  "challenge": 1,
  "verify": 1,
  "cleanup": [],
  "hints": 1,
  "plans": [
    {
      "eventId": 1,
      "reason": "lock",
      "kind": "reconcile",
      "flowId": 1
    }
  ],
  "owner": "RELEASED"
}
```

**later stop**

```json
{
  "label": "later stop",
  "sessions": [
    {
      "nonce": "N1",
      "address": "0x6af6ca319213b924e4b94a1de96a6e502a09aa74",
      "expires_at": 1791201600000,
      "revoked_at": null,
      "alias": "S1"
    }
  ],
  "challenges": [
    {
      "nonce": "N1",
      "used_at": 1790596800000,
      "invalidated_at": null
    }
  ],
  "counts": {
    "created": 1,
    "live": 1,
    "revoked": 0,
    "challenges": 1,
    "used": 1,
    "pending": 0,
    "invalidated": 0
  },
  "prompts": 1,
  "challenge": 1,
  "verify": 1,
  "cleanup": [],
  "hints": 1,
  "plans": [
    {
      "eventId": 1,
      "reason": "lock",
      "kind": "reconcile",
      "flowId": 1
    },
    {
      "eventId": 2,
      "reason": "stop",
      "kind": "none"
    }
  ],
  "owner": "RELEASED"
}
```

**ordinary ABSENT during prompt**

```json
{
  "label": "ordinary ABSENT during prompt",
  "sessions": [
    {
      "nonce": "N1",
      "address": "0x6e574c9d8e12c999ee117b813d7a9e558fb6d086",
      "expires_at": 1791201600000,
      "revoked_at": null,
      "alias": "S1"
    }
  ],
  "challenges": [
    {
      "nonce": "N1",
      "used_at": 1790596800000,
      "invalidated_at": null
    }
  ],
  "counts": {
    "created": 1,
    "live": 1,
    "revoked": 0,
    "challenges": 1,
    "used": 1,
    "pending": 0,
    "invalidated": 0
  },
  "prompts": 1,
  "challenge": 1,
  "verify": 1,
  "cleanup": [],
  "hints": 1,
  "plans": [],
  "owner": "RELEASED"
}
```


ownership 控制沿用真 viem ABI／Multicall encode/decode，Worker route over actual SQLite；fixture upstream／clock為注入，沒有 live RPC。以下 index／budget／RPC 都是該 fixture campaign 的實測，RPC 指該測試所計 proof calls，不能等同所有整站 fetch。

| 控制 | 實際結果與計數 | 授權／成本解讀 |
|---|---|---|
| ordinary20，fresh20（各自一批） | 各 budget1/index1/RPC1；20個eligible1、single checkedAt；live advancing | 誤用舊 request-start clock 的重複 admission 已修 |
| Worker／SQLite due-index20 | delta budget1/index1/RPC1；20個HTTP200／eligible1；sessions1/live1 | 預先sign-in/first home成本由before/after分開，非全流程僅一RPC |
| changed-roster / fresh-intent queued after failure | first OWNERSHIP_UNAVAILABLE；second eligible2/1；budget1/index1/RPC2 | distinct意圖重評，不把 index當 proof |
| twenty identical failing callers |20 unavailable；later eligible1；budget1/index1/RPC2 total | 失敗cohort不 stamp新 epoch，後續retry不放大 index |
| Worker queued fresh after failed cold proof | HTTP503/200；budget1/index1/RPC2；sessions1/live1 | 503不是已完整證明空集合 |
| held RPC across30s deadline／sold seat | first unavailable，second eligible0；budget1/index1/RPC2；tags latest/latest | expired epoch不能續用；後者真的latest重證 |
|512active address cap |512 complete／1unavailable；budget512/index512/RPC512；settled後第513可retry | active flights不evict；cap為isolate，非全球 |
|refused fresh x20，保留一席已證明候選 | asks1/index0/ethCalls1；20個eligible1；20個limited，同checkedAt | 拒絕讀index不授 index權限或更新proof deadline |
|refused empty x20 | asks1/index0/ethCalls0；20個eligible0、limited | complete-empty與limited分離 |
|failed delta cap／same-block | checkedCandidates256、recheck partial；failed IDs佔attempt cap；delta tag固定block | Deadline不renew；到期後可latest重證 |

精確 before/after、tags、ids、budget、lane、recheck 都在 evidence JSON 的 ownershipDiagnostics；上述是每個實測campaign範圍內的概括。[O]、[V] 公共 headers、lockfile、server/auth、worker/app、七 migration 與舊版 public bytes 另外比較，無 public byte差異；redacted originals是否真的未改仍只能採TEAM summary。[B]

### 附錄四：十一事件矩陣與附加控制

`source/R8_FINAL_CLOSURE.md` 只採 **Required fixed ordering matrix** 的 case list。該文件其它日期、版本、私有1528/500數據屬歷史，不能改標第八候選的新執行。[E] 以下前五／後三有新 opt-in fixed traces；其餘有此次all23 suite的exact tests與計數。全部不是只以文件打勾。

| 必留事件 case | 本次 executable／實測界線 |
|---|---|
| PRESENT，held home，account switch | fixed-1-held-home-account；S1/0/1，C1/1/0/0，expectedAddress primary |
| PRESENT，held home，provider switch | fixed-2-held-home-provider；S1/0/1，C1/1/0/0；選擇為真正intent |
| slow valid verify body，sibling stale ABSENT | fixed-10-slow-body-sibling；S1/1/0；sibling自己的preflight觀測PRESENT，零sibling prompt |
| displayed session＋pending nonce，switch | fixed-3-displayed-pending；S1/0/1，C2/1/0/1；primary不是競爭pending nonce POST |
| stop，cleanup in flight，restart | fixed-4-restart-cleanup；S2/1/1，C2/2/0/0；late清理不能撤新row |
| fresh=1 refused index budget x20 | ownership-v11與ownership-market-r8；asks1/index0/proof1，limited與原deadline |
| backward clock，sold seat | auth-r8／ownership-v11；舊ownership不被回跳維持，重新ownerOf與latest控制 |
| backward clock，revoked session | fixed-9-backward-revoked與auth-r8；S1/0/1，不恢復舊session |
| lock，no active click | fixed-5-lock-idle；S1/1/0，stop仍preserve |
| lock，active click | fixed-6-lock-active；S0/0/0、C1/0/1/0；晚signature不verify；post-verify variant在core另行覆蓋 |
| missed signed-in hint | fixed-0-lost-hint；在後續explicit logout前，sibling own GET讀PRESENT、零prompt；final revoked由explicit intent造成 |
| extra old-A-nonce／new-A-row | auth-v11 L120+與auth-r7-authority；same-address／same-expiry不把舊nonce認成新row |
| extra lock503／later-valid | auth-v11 L98+；first503保責，later PRESENT釋放，stop零logout |
| extra passive provider | auth-audit8與fixed-0-audit-passive-discovery；零被動cleanup |
| extra ordinary read during prompt | auth-audit8與fixed-2-audit-hint-while-prompt；同一signature完成，S1/1/0 |

以下是**整條 fixed trace**的final rows與實際派送／提示，不是某個checkpoint的數字。`prompt`以final projection累計，不能把 `prompt` action與provider completion event重複算；cleanup204也不代表每個planned/retried request都造成一次有效撤銷。Traces的 worker-result/checkpoint 保留每階段 SQL counts、dispatch captured cookies／body nonce aliases、headers／expose／body，供重播查看。Auth trace中未逐項列RPC/budget者保持未量測，不補0。

| trace | S | C | actual prompt／challenge dispatch／verify dispatch／cleanup dispatch／hint emitted | replayable trace |
|---|---|---|---|---|
| passive-discovery | 1/1/0 | 1/1/0/0 | 1/1/1/0/1 | [fixed-0-audit-passive-discovery.json](traces/fixed-0-audit-passive-discovery.json) |
| lost-hint | 1/0/1 | 1/1/0/0 | 1/1/1/1/2 | [fixed-0-lost-hint.json](traces/fixed-0-lost-hint.json) |
| lock-503-same-unlock | 1/1/0 | 1/1/0/0 | 1/1/1/0/1 | [fixed-1-audit-lock-503-same-unlock.json](traces/fixed-1-audit-lock-503-same-unlock.json) |
| held-home-account | 1/0/1 | 1/1/0/0 | 1/1/1/1/2 | [fixed-1-held-home-account.json](traces/fixed-1-held-home-account.json) |
| slow-body-sibling | 1/1/0 | 1/1/0/0 | 1/1/1/0/1 | [fixed-10-slow-body-sibling.json](traces/fixed-10-slow-body-sibling.json) |
| pre-header-failure | 0/0/0 | 0/0/0/0 | 0/0/0/0/0 | [fixed-11-pre-header-failure.json](traces/fixed-11-pre-header-failure.json) |
| stopped-late-headers | 1/0/1 | 1/1/0/0 | 1/1/1/2/0 | [fixed-12-stopped-late-headers.json](traces/fixed-12-stopped-late-headers.json) |
| hint-while-prompt | 1/1/0 | 1/1/0/0 | 1/1/1/0/1 | [fixed-2-audit-hint-while-prompt.json](traces/fixed-2-audit-hint-while-prompt.json) |
| held-home-provider | 1/0/1 | 1/1/0/0 | 1/1/1/1/1 | [fixed-2-held-home-provider.json](traces/fixed-2-held-home-provider.json) |
| displayed-pending | 1/0/1 | 2/1/0/1 | 1/2/1/1/2 | [fixed-3-displayed-pending.json](traces/fixed-3-displayed-pending.json) |
| restart-cleanup | 2/1/1 | 2/2/0/0 | 2/2/2/1/1 | [fixed-4-restart-cleanup.json](traces/fixed-4-restart-cleanup.json) |
| lock-idle | 1/1/0 | 1/1/0/0 | 1/1/1/0/1 | [fixed-5-lock-idle.json](traces/fixed-5-lock-idle.json) |
| lock-active | 0/0/0 | 1/0/1/0 | 1/1/0/0/0 | [fixed-6-lock-active.json](traces/fixed-6-lock-active.json) |
| unknown-preflight | 0/0/0 | 0/0/0/0 | 0/0/0/0/0 | [fixed-7-unknown-preflight.json](traces/fixed-7-unknown-preflight.json) |
| cancel-preflight | 0/0/0 | 0/0/0/0 | 0/0/0/0/0 | [fixed-8-cancel-preflight.json](traces/fixed-8-cancel-preflight.json) |
| backward-revoked | 1/0/1 | 1/1/0/0 | 1/1/1/0/1 | [fixed-9-backward-revoked.json](traces/fixed-9-backward-revoked.json) |

**效果分層例子：**補充 lock503 probe 的plans只有lock/reconcile，不是logout；解鎖後沒有POST，Worker committed row仍live1；later stop新增none。explicit same-address provider selection則一個displayed-session primary、一次expectedAddress logout204，setup row1 revoked，再以新click建立row2，故created2/live1/revoked1。fixed restart trace含conditioned cleanup in flight與不同帳戶的新登入，final只有舊row revoked；header到達順序能改cookie visibility，不能把它當DB commit順序。受注入503/429拒絕的planned/retried責任以trace actions/events與result counts核算，不概括為「每一計畫等於一次撤銷」。[A]、[N]、[Q]

### 附錄五：前後 provenance、部署及待辦

兩個原始URL是mutable main，下載時hash與 `PRIOR_REVIEWS.md` 的捕獲hash完全相符；若之後main變更應回到這兩個hash比較。Audit 的新六Low／兩Info不是 Report 舊R8 v1.1八項的同一名稱集合；本次主表跟隨Submission8 Audit7 matrix，舊R8矩陣只維持控制，避免偷換閉合問題。

| 原件 | captured SHA-256（本次GET相同） | bytes／lines | 原判斷 |
|---|---|---|---|
| [Audit original](https://github.com/Identity-md/research/blob/main/jobs/4e150a3c-3ee4-4856-972e-db5db4f4d3fc/files/AUDIT.md) | `93ddeba22bd0dbcbff5a83f65bc48e9a373c7c2b8c3f6a848920a5fc7fa939a0` |47511／288| 六Low新反例；timestamp Info accepted limit；artifact Info open hygiene，當時非blocker |
| [Report original](https://github.com/Identity-md/research/blob/main/jobs/a31f9d4e-694e-416c-8462-e992c7b51267/files/artifacts/report.md) | `5d3a4ba07a38bc750949d6eca55f23bb15ddab6250d2269546d6d7fd49fa8de4` |27192／136| 既有R8 v1.1六Low與兩Info fixed locally；當時candidate未部署，release blocked |

不把 prior `Completed/accepted` 當來源安全承諾，也不抹掉彼此不同的觀測範圍。這次新增artifact反例的blocking含義是**任務要求未達到**，不是把Info自動升成wallet authority High。

TEAM 部署證據屬本快照內的時間點量測，未對production做任何本次live請求。記錄ID由assignment／TEAM deployment metadata標示；最新canonical raw logs、recovered pending directory與Cloudflare原始回讀body不在公開包，不能獨立重驗其操作細節。公开summary說明最後rename失敗、containment內恢復且沒有第二次部署；「未變pending record復原」保留為TEAM recovery敘述，而非本次親見。[D]、[T]

| TEAM measurement／receipt | 值及保留判斷 |
|---|---|
| source／Worker／record | `bb7549e0a2576ba4da0ea7c4147c4aba1a7f577f`／`cdd3ef36-ca81-439a-8798-a64e30cf01d3`／`20261004T180257Z-bb7549e` |
| overall canonical invocation | **exit1**；Windows EPERM at final local record rename，Wrangler upload exit0；不是tests failed、不是overall0 |
| canonical stdout／stderr | `a67f35b1e91c78eeff1a3a049611153355e60d473d3d0f828ab65a31ab230cab`／`85feb5a37577b175a34d354487c46b3209eea03700db4253904ceb6d34678175` |
| deploy manifest | `9f9fa82ce11c380fdb26ae6b63e6eaf497fba6340e1d16c0da7a88f7b66d119f` |
| deployed Worker raw bytes |315781 bytes；SHA256 `7fafc4c62af05efa33b9153a7aa7b094ac31b3a31a546429baa096c61435c66c`；TEAM Cloudflare readback matches |
| TEAM HTML | `dfe6fa0f3431ff9ca0128b81e5a1a135ae7d4a6ea8d5fcb4849e70e26eaac053` build/served equal；2618bytes |
| TEAM main JS | `2c1894a2c1fd21d757ea62af069dff983f505351620911a0af2a3438b72e3d21` build/served equal；1553557bytes |
| TEAM CSS | `be70f6c11b0030c3401c1bce007e58a37cd6cb39e9adb9ffd5c6758582e6142a` build/served equal；68142bytes |
| TEAM InteriorView JS | `51c60e2905075e4191190f77a0aa2af25d072ddaebebafa66c4bfb9d15d400a2` build/served equal；93242bytes；不代表source公開審查 |
| TEAM remote config |100%traffic；bindingsMatch true；pendingMigrations0；7migration rows，readOnlyCommands exit0，rowsWritten0；listed headersMatch true |
| readback receipt hashes | HTTP `904ef47a9c92b858d3bae8672beb5d8da090c7ea3734e756472d386e9ab53a4d`；Cloud `515621552b70def1d38e8bccbdfdbfbd6ad45603a1ad502f31efda2ed2b83718` |
| migrations receipt | `fed7c9b25c5e31168e3525ba7c26572352babc51c4c234b03f5c0439da631a2e`，captured2026-10-04T18:30:45.241Z |
| rollback observation |source `f94d2aa6a5c451eefbbfc8452bf70a56c11b284f`，version `e0a0c39c-0907-4588-984a-e53cd3a037e4`，record `20261004T172900Z-f94d2aa`；TEAM metadata，沒有本次rollback演練 |

歷史packages的HTML analytics mismatch保持歷史狀態；新TEAM summary為上述指定assets raw equality，沒有新增measured mismatch，但不能推及所有資產、時間、request variants或永遠parity。私有完整build與1606/1606是TEAM觀測；公開刻意濾出的前端缺失不適合宣稱全frontend tsc/Vite成功，也未為本次重跑完整frontend。

剩餘工作／bounded accepted limits：

- **SOURCE-CLOSURE：**修復第八項兩反例、補上拒絕與sanitized replay控制，重跑真locked viem/all23及新反例。六Low與第七Info的local fixed不擴張至未供應來源。
- **RELEASE-READINESS：**先達來源閉合，再取得具可核對時間點與完整freeze映射的独立部署/config/headers證據；目前raw回讀與private build不可取得，維持unknown，不要求owner credentials／private DB access。canonical非零收據需保持，操作恢復可靠性仍可補可重現本地檢查。
- **accepted limits：**GET不是global lock；相同地址proof lane與512 cap不是global RPC ceiling；失敗／refusal／deadline fail-closed會犧牲availability。Late cookie-clear、stopped/crashed pages、Auth transport沒有新增deadline、cross-isolate與實體wallet/browser仍有限或未知，不宣告不存在。
- **模型界線：**real client/Worker/SQLite plus pure oracle/injected deliveries會檢查因果序與SQL rows，但每個Worker/SQL body是一個scheduler step，不窮舉D1 transaction interleavings。Browser cookie政策、hostile extensions、process death、WAF、Cloudflare multi-isolate與real-money coverage未建立；withheld scene/media/source的build或served-byte比對不等於review。

### 附錄六：輸入與 evaluator hash 收據

[reviewer-evidence.json](reviewer-evidence.json) 保存全部140個獨立核算的 source SHA256、manifest零差異、raw command log hashes、26 Auth diagnostics、67 ownership diagnostics、per-row probes与exit codes。兩個campaign完整evaluator/input maps、500與90各seed digests分別保存：[core500-RESULT.json](core500-RESULT.json)、[audit8-90-RESULT.json](audit8-90-RESULT.json)。這些是本次產生，沒有挪用TEAM execution timestamps。raw logs未全體交付，以免把臨時機器路徑寫進主報告；以下hash釘住量測，結構化摘錄與可重播動作提供可讀證據。

| 本次 raw log | SHA-256 |
|---|---|
| `install` | `c56baa8fcabbfd0b6419defa99b8f8c824a3441936ac1174dbadcd6558a4cd39` |
| `install-retry` | `67eccdcd82a7eab94171e27d68aba86929472f280d0b64d08d27a9a4a49f4fa6` |
| `check` | `d7c62854077938dd3388d0e043d44e228a9e9e624a02191fb29b55ba8ebaca46` |
| `test` | `e60908e7f6f9aff3d7a13c742f03a94acad3d748e8b45e36ef2957ac91649804` |
| `baseline` | `a7f49ff3283987a28f62b9d342758685fe0e6f2bf947c16030c58b6d4c47dc6a` |
| `baseline-retry` | `19a7566ef416bbc4060d867b4e18e088ccc500836b8f00e817f0ce074040782f` |
| `baseline-auth-targeted` | `9ec08c02d375d3da935bcf4b0dad7b036478bb85b061dccad42f4e844b66c81c` |
| `optin` | `17923155f3793a5997ff1c406a3402749247854a8bb31c321e63e0f35e912a3c` |
| `replay-core` | `1ac0af3f0c5cd46d058ab91b6bac07252762b91f375ea920006000d6a65ef594` |
| `replay-audit` | `dcde73c1a6daa92b6e3cdefb88d85f7010383ebb7c82f88b7f06a737c25115db` |
| `rows` | `f2c6a818affdf5381ebb807c536367b012c145f834f2d43c40e91d40503f0660` |
| `artifact-probe` | `cf9727391f6938a563373832355fb7c6d6f39c0f98a3128520e65bc974d8fc7a` |
| `clock-baseline` | `6bfa70e950fdd8fbeaceb0621405f2f33ea951e7d784c0177bdc12ecbf46e0f4` |
| `clock-candidate` | `34ae9b994aef895fb20cb24800a7dc8143e2bc17d029d44abbd082f538fb3006` |
| `clock-baseline-retry` | `6bfa70e950fdd8fbeaceb0621405f2f33ea951e7d784c0177bdc12ecbf46e0f4` |
| `clock-candidate-retry` | `7c41d610bf7f378c8155bde0a55d1c6638a4ba561764073291451d35612daac7` |
| `rows-stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

核心與additional evaluator（獨立核算，保留 exact bytes）：

| path | SHA-256 |
|---|---|
| `source/tests/auth-artifacts.mjs` | `e5c12899484497d9429573bfca710ee88b3407b2e524fc9d28eec16f8698c8e3` |
| `source/tests/auth-audit8-causal.test.mjs` | `6d7481a527083ab01e4dbd1bd83860f2483f656f01a51ef4aadb2243d8d85ba3` |
| `source/tests/auth-audit8-causes.mjs` | `9fe8626e78ca1ecaa7df0794bf18fbf2c689b464ed359b996d218c9699995ed1` |
| `source/tests/auth-audit8-reference.mjs` | `2b85a7d62c4799282f03dc3f67e146b98d85cf7f09f603cb1b392c46bebc8d2a` |
| `source/tests/auth-reference-model.mjs` | `6c3259353fee927da1f759e8ce017e27cb03e7d81b3d124dcb4db21c8eaf942a` |
| `source/tests/auth-reference-scheduler.test.mjs` | `48a5eedc1c1c15113e3e2e4b7c92c8053416eb68e999654e03e1f75f0579e5ad` |
| `source/tests/auth-scheduler-driver.mjs` | `fbee8522512226a6c2cb41104126815c68ceaacf0a094f1b4bc3160f6ffe58e5` |

Pinned citation index：以下全部指向 exact public snapshot，不指向較晚 main。

[M]: https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/Submission8/CLOSURE_MATRIX.md
[P]: https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/manifests/submission8-published-source.json
[R]: https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/source/docs/security/AUDIT8_REVIEW_RUNNER.md
[B]: https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/Submission8/BOUNDARY_CHECK.json
[C]: https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/source/docs/security/AUDIT8_CLOSURE.md
[A]: https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/source/tests/auth-audit8.test.mjs
[O]: https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/source/tests/ownership-audit8.test.mjs
[F]: https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/source/tests/clock-skew-audit8.test.mjs
[G]: https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/source/server/gateway.ts#L248-L265
[H]: https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/source/tests/auth-artifacts.mjs#L6-L32
[V]: https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/source/tests/ownership-v11.test.mjs
[E]: https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/source/R8_FINAL_CLOSURE.md#L33-L48
[N]: https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/source/tests/auth-v11.test.mjs#L98-L142
[T]: https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/Submission8/TEST_RESULTS.json
[D]: https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/Submission8/BUILD_DEPLOYMENT.json
[PR]: https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/Submission8/PRIOR_REVIEWS.md
[Q]: https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/source/tests/auth-reference-scheduler.test.mjs
[S]: https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/Submission8/REFERENCE_SCHEDULER.json
[J]: https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/source/scripts/replay-auth-trace.mjs
[AT]: https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/source/tests/auth-artifacts.test.mjs

### 附錄七：修補定位與基線實際反向數據

| Audit7列 | pinned policy／patch位置 | 同候選正式evaluator |
|---|---|---|
|1|[auth.ts L274-L312](https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/source/src/world/auth.ts#L274-L312)、[wallet.ts L44-L89](https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/source/src/world/wallet.ts#L44-L89)、[WalletPanel.tsx](https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/source/src/world/WalletPanel.tsx)|auth-audit8／causal|
|2|[ownership.ts L253-L287](https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/source/server/ownership.ts#L253-L287)|ownership-audit8 ordinary20/fresh20／Worker20|
|3|[auth.ts L581-L595](https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/source/src/world/auth.ts#L581-L595)|auth-audit8 lock503／same-unlock／stale callback|
|4|[auth.ts L440-L505](https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/source/src/world/auth.ts#L440-L505)|auth-audit8 held-signature boundary matrix|
|5|[ownership.ts L223-L316](https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/source/server/ownership.ts#L223-L316)|ownership-audit8 distinct／identical／expiry／cap；ownership-v11 delta/cap|
|6|[freshness.ts L1-L23](https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/source/src/shared/freshness.ts#L1-L23)、[cadence.ts](https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/source/src/world/cadence.ts)、[market.ts L66-L115](https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/source/src/world/market.ts#L66-L115)|clock-skew-audit8／freshness-v11／ownership-market-r8|
|7|[gateway.ts L234-L265](https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/source/server/gateway.ts#L234-L265)|clock-skew-audit8 warm lifetime controls；gateway.test是TEAM/full source測試路徑，**不在公開23檔fresh run**|
|8|[auth-artifacts.mjs L6-L32][H]、[review-tests.mjs L6-L36](https://github.com/tungweb3/imd-ember-world-review/blob/88c130283efc45260f9e00da8d2d3055c38483bd/source/scripts/review-tests.mjs#L6-L36)、[replay-auth-trace.mjs][J]|artifact／runner／core/additional；new local dangling+root-path probes|

基線取得的**實際**數據補足主表（未把未完成廣泛實驗當通過）：

| 控制 | previous public量測 | candidate量測 |
|---|---|---|
|ordinary20與fresh20，各自一批|各budget20/index20/RPC1，eligible仍20個1|各1/1/1；修的是索引/預算放大，而非先前取得20次proof|
|Worker due-index20|before1/1/1→after21/21/2，delta20/20/1；sessions1/live1|delta1/1/1；sessions1/live1|
|changed-roster與fresh-intent queue|first與second均OWNERSHIP_UNAVAILABLE，index1/budget1/RPC1|first503後second成功，RPC2；eligible2／1|
|held RPC expiry／sold seat|first與second均unavailable，只1RPC/latest|firstunavailable，secondeligible0、2RPC/latest/latest|
|active address capacity|513complete/0unavailable，513RPC|512complete/1unavailable，512RPC，settle後retry|
|passive same-address-object／first discovery|各S1/0/1；P/Q/V=0/0/0；expectedAddress cleanup204一次|各S1/1/0；零cleanup；first mismatch仍保留cookie session|
|lock503 held-verify，same-account unlock|S1/0/1；P/Q/V=1/1/1；expectedNonce cleanup204|S1/1/0；cleanup0、valid canonical釋放責任|
|lock503 invalid verify body|測到一次nonce cleanup dispatch時S仍1/1/0，status尚未完成；不要誤報已撤銷|cleanup0，S1/1/0；後stop不撤|
|ordinary ABSENT during prompt|S0/0/0；C1/0/1/0；prompt1/challenge1/verify0|S1/1/0；C1/1/0/0；1/1/1|
|remote plus1ms／warm producer ahead59000ms|false／stamp1000000|true／stamp1059000；同producer1059000|

這些對照不等同舊版本重新完成all-suite。20 identical failure+later retry本來就通過；候選保留該控制，不宣稱每個baseline test都失敗。初次path guard failure與後來Ctrl-C130不作產品缺陷；targeted五個policy反例與ownership十個controls則有完成收據與實際數據，位於evidence的baseline欄。
