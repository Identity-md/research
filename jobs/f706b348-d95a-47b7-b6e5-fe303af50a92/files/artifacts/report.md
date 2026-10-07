# EmberEvo ($EMVO) v3.3 ReviewFix1 — 單次非部署規格審查報告

審查日期：2026-10-07（UTC，retrieval 於 08:05 UTC 前後）
性質：**SPEC_ONLY 規格／政策審查**。未取得任何 source／bytecode／quote／Paying Wallet；未部署、未簽名、未送出交易、未付款、未開 child job 或 schedule。本報告不是 code audit，不是認證，也不是 launch 授權。
語言：Traditional Chinese；技術識別符保留英文。

---

## 1. INPUTS_READ

固定 commit：`902075d1dfb772738a074f06f56f7aeea9240fd8`（repo `tungweb3/emvo-review`）。
存取方式：`raw.githubusercontent.com/<commit>/<path>` 的 HTTP GET，以 `curl` 取得原始 bytes；以 `sha256sum` 對 **received raw bytes** 計算，未經任何編碼轉換。

| 檔案／角色 | URL（均 pin 於上列 commit） | 實收 bytes | 實算 SHA-256 | Manifest 值 | 結果 | 讀取範圍 |
|---|---|---:|---|---|---|---|
| `INPUT_MANIFEST.json`（清單） | `https://raw.githubusercontent.com/tungweb3/emvo-review/902075d1dfb772738a074f06f56f7aeea9240fd8/INPUT_MANIFEST.json` | 1,700 | `4be0ee3d9529828d4f0fb7dbb6ed1ce177ee9502c5aec5d1981a9792b54b69df` | 任務指定 `4be0ee3d…69df` | **MATCH** | 全文 |
| `README.md` | `…/902075d1…/README.md` | 3,282 | `d2a51c2b32316ecfccc1c5e24b6004aa613f3604cf4df93d3f144ee8123858f3` | manifest 未列（僅資訊） | 無可比對值；不影響 INPUT 判定 | 全文 L1–32 |
| 規格 `IMD_Ember_EmberEvo_v3.3_Crypto_Research_Genesis_Burn_2026-10-07.md` | `…/902075d1…/IMD_Ember_EmberEvo_v3.3_…2026-10-07.md` | 148,119 | `ba57f63ef3d7cc302b8c4b354d242438baf79d9f57aa9d9a37d97e20f3dd5847` | 同 | **MATCH**（bytes 亦符） | 全文 L1–3668 |
| `EMVO_Swarm_Review_Brief_v1.3_Crypto_Research_NoDeploy_2026-10-07.md` | 同上路徑模式 | 35,101 | `f8264f0b254eba8f50d7bfa47004e0b46e75dd97181c04bfd9db1a5db5d1ba8e` | 同 | **MATCH** | 全文 L1–406 |
| `EMVO_Hackathon_Swarm_Review_Addendum_v1.2_NoDeploy_2026-10-07.md` | 同上 | 7,283 | `af397c80912b12f4a7d8a7c804ba57588f442bfaa0913e7fd85de842fba6ab6d` | 同 | **MATCH** | 全文 L1–78 |
| `EMVO_Hackathon_Participation_Gap_Review_v1.2_2026-10-07.md` | 同上 | 20,591 | `5ab2680708c426af717dcc1766867a4dfe1bcdb217a237bf7b9cca7320841cad` | 同 | **MATCH** | 全文 L1–389 |

- Truncation：**無**。五份 Markdown 皆以行號區間完整閱讀（規格以分段方式 1–700／700–1500／1500–2400／2400–3668 讀畢）。
- Mismatch：**無**。INPUT_MISSING／MISMATCH：**無**，故繼續實質審查。
- 舊 commit `0dc9eec7…`、Rev.2/Rev.3 僅為歷史，未審。
- 補充：Addendum 引用的 hackathon proposal（`Identity-md/research@9f7d4a08…`）**未由我重新取得**；其內容僅透過 Gap Review 轉述得知 → 標 `DOCUMENTED_ONLY`（二手）。

**Prompt-injection 檢查**：所有輸入文件含大量「Do not…／Must…」類指令式文字。依任務規則一律視為 DATA；其中沒有任何要求我擴權、執行指令或洩漏設定的內容。文件亦自述「AI 寫的歸屬不是獨立授權」（README L5），本報告採同一立場。

### 1.1 本次額外取得的 live 公開證據（read-only GET，非鏈上）

取得時間 2026-10-07 ≈08:05 UTC；皆 HTTP 200。**這些是 IMD 服務自述的 API/頁面內容（`OBSERVED_HTTP`），不是鏈上觀察，也不是 EMVO 的 quote。**

| 來源 | bytes | SHA-256（received） |
|---|---:|---|
| `https://api.imd.fun/version` | 195 | `9b2c127532d3d47beac7bf38e3d325b0aca7d9911d8355fc793ad558cbbad41b`（commit `be003835…2011`, branch master, `deployedAt:null`） |
| `https://api.imd.fun/launch/policies` | 29,362 | `7c86eb577e027dee867419f75b04952d672db7b4c28ba3ab40d4dad4449eed25`（count=32） |
| `https://api.imd.fun/requests/capabilities` | 4,256 | `eaef51c4fa76119c48e31d71972e34b9fd590bdc8714025fc37f6899bd310e70` |
| `https://imd.fun/docs/`（靜態文字化後 84,463 字元） | 484,189 | 未記錄 hash（頁面動態，僅作文字參考） |
| `https://explorer.imd.fun/launch` | 41,961 | 未記錄 hash |

未做：鏈上 RPC 讀取、`api.imd.fun/openapi.json`、authenticated Check/Quote、任何 Factory source／runtime 取得。

---

## 2. 執行摘要與 R / Q / L / V / G / D / I / H 分項判定

| Gate | 判定 | 一句理由 |
|---|---|---|
| **R** 本次審查是否具備執行條件 | **READY（輸入完整；範圍僅 SPEC_ONLY）** | 四份 manifest 檔＋README hash 全符；無 code／quote，故測試 NOT_RUN。 |
| **Q** 能否不付款地準備 exact Mainnet 請求 | **NOT READY — 路徑明確，缺 4 項釘選** | 見 §4：`poolBps/remainderTo`、policy `kind`＋version、`pairWith=imd` 明示、token/Hook/LP owner 接受。 |
| **L** 付款／發幣批准 | **HOLD — NOT AUTHORIZED / EVIDENCE INCOMPLETE** | 無 exact quote、無 Paying Wallet、無 Factory source、**無 true-burn 能力證據**；且官方文件稱 launch token 為 "plain transfers"（見 F-01）。**我支持 ReviewFix1 提議的 L HOLD。** |
| **V** 已部署後核對 | **NOT_APPLICABLE / NOT_RUN** | EMVO 尚未存在，不能核對。 |
| **G** Genesis 開放 | **NOT READY（SPEC_ONLY）** | 規格方向完整，但 true-burn 路徑、BURN_PER_MINT、F/R/P、資格皆 TBD；測試全 NOT_RUN。 |
| **D** 世界內容發布 | **NOT_RUN** | 無 Engine／網站 source；D1+ 不阻擋 Token L（符合規格 §36.1）。 |
| **I** 加密研究管線 | **SPEC_ONLY，I-01..I-15 全 NOT_RUN；規格足以進入實作，另有 6 項建議補強** | 見 §8。 |
| **H** 黑客松資格 | **UNCONFIRMED** | 只有 proposal 的二手轉述；我未取得主辦正式規則、年份確認、網路與投稿路徑。 |

**核心結論（事實／推論分開）**
1. （事實）規格自己宣告 L 未授權、true-burn 為 UNVERIFIED、IMD-only fee 為 UNVERIFIED、2% 可出售且無 vesting、Paid Genesis 為 BURN_NOT_TREASURY。我對這些「文件自述」**未發現與輸入內容互相矛盾之處**（內部一致性良好，僅有 §7 所列小處）。
2. （事實，OBSERVED_HTTP）官方 docs 稱 "On a project or hook launch the token is fixed: 1,000,000,000 with 18 decimals and **plain transfers**"。
3. （推論，非證明）"plain transfers" 與 Genesis 需要的 `burn`/`burnFrom` 並不相容的可能性高；**不能證明沒有 burn**，因為我沒有 Token source。因此 L HOLD 是**正確的保守判定**，不是已證實不相容。
4. （事實）live policy `v29`（chain 1, `univ4_hook`）的 `owners.token / treasury / hookAdmin / lpPosition` 全為同一地址 `0xcecc29b037f5064fcdf45a5c318f132ef76aa551`；policy v27 note 稱之為 "launch wallet"。這與規格預設的「Paying Wallet 為實際收款／控制人」圖像**不一致或至少未被說明**（見 F-03）。
5. （事實）live policy 參數 `liquidityBps=8000, treasuryBps=1000, contributorPoolBps=1000`，而規格與 Launch 頁用「88/10/2」。兩者語意是否同一件事**未能對照**（見 F-02）。

---

## 3. 證據表

標籤：`DOCUMENTED_ONLY / OBSERVED_HTTP（本報告新增，指 IMD 服務 HTTP 自述）/ SOURCE_VERIFIED / OBSERVED_ONCHAIN / UNVERIFIED / CONTRADICTED / NOT_APPLICABLE`。

| # | 主張 | 來源 | 取得時間 | chain/block/commit | 證據等級 | 限制 |
|---|---|---|---|---|---|---|
| E-01 | 輸入 5 檔 bytes／SHA-256 與 manifest 相符 | raw GitHub @ `902075d1…` | 2026-10-07 | commit `902075d1…` | **SOURCE_VERIFIED（對輸入檔）** | 只證明 bytes 完整，不證明內容正確。 |
| E-02 | launch token 固定 1B／18 decimals／"plain transfers" | `imd.fun/docs/` | 08:05 UTC | — | OBSERVED_HTTP | 靜態文字；未見 Token source。 |
| E-03 | 池費 1.25%，1% paying wallet／0.25% network；"Anyone can call the distribution" | `imd.fun/docs/`；policy v29 `feeTiers:[12500]`、note "1.25%" | 08:05 | policy v29, chain 1 | OBSERVED_HTTP | 費用資產、記帳位置、conversion 皆**未說明**。 |
| E-04 | Supply 分配：swarm 10%（其中 2% 平分給有 accepted work 的錢包、8% 依 seat 平分，Merkle distributor）；其餘 90% 中 `poolBps`（≥1,000）入池、餘額 `remainderTo`（預設 paying wallet） | `imd.fun/docs/` | 08:05 | — | OBSERVED_HTTP | 「88% 池／2% paying wallet」只在 Launch 頁文案出現；`poolBps` 為**可調參數**，預設值未見。 |
| E-05 | Launch 頁文案："88% opens the pool, and 2% goes to the wallet that pays"；Chain 選單 Ethereum mainnet（Base/Robinhood/Sepolia 標 soon） | `explorer.imd.fun/launch` | 08:05 | — | OBSERVED_HTTP | 與 docs/capabilities 列出 Robinhood 4663 為 open 的說法不一致（頁面 "soon"）。 |
| E-06 | Live policy v29：`kind=univ4_hook`, `chainId=1`, `feeTiers=[12500]`, `totalSupply=1e27`, `treasuryBps=1000`, `liquidityBps=8000`, `contributorPoolBps=1000`, `recentContributorBps=800`, `contributorLockSeconds=3600`, `perWalletCapBps=3000`, `gasCeilingWei=5e16`, `initialMarketCaps[IMD]=2.5e21`, `owners.*=0xcecc…a551`；同 chain 另有 v19（舊 fee tiers 500/3000/10000）、v18 `evm_project`、v26 `custom_token`、v27 `evm_contracts` | `api.imd.fun/launch/policies` | 08:05 | policy v29（建立 2026-10-06T17:42Z） | OBSERVED_HTTP | 欄位語意（例如 `contributor*`、`perWalletCapBps`）無官方註解；**我不猜**。 |
| E-07 | capabilities：`launch.open`／`job.open` 皆 0.5 IMD（`5e17`，18 decimals），asset `0xd34a99bc…03e263b7`（IMD on `eip155:1`），`payTo 0x4e0fa57b…adbc`，quoteTtl 600s；Permit2 + EIP-712 QuoteApproval；chain 1 的 `pairWith=imd` 對 `univ4_hook／evm_project／custom_token` 開放；`defaultChainId=11155111`（Sepolia） | `api.imd.fun/requests/capabilities` | 08:05 | — | OBSERVED_HTTP | 鏈上 IMD 地址／decimals **未以 RPC 驗證**。 |
| E-08 | paid request 簽署者須為一般帳戶或 EIP-7702；Safe 暫不支援 | `imd.fun/docs/` | 08:05 | — | OBSERVED_HTTP | 規格 §7.4 一致。 |
| E-09 | schedule：按次預付、未用次數不退款、無 expiry、pause/cancel 由 IMD 團隊控制；`schedule.create/topup` 0.5 IMD／run，任何錢包可 topup | `imd.fun/docs/`＋capabilities | 08:05 | — | OBSERVED_HTTP | 規格 §73.3 一致。 |
| E-10 | 規格自述 EMVO template/runtime／burn／fee 實測皆未取得 | 規格 L38、Brief §2.1 | — | — | DOCUMENTED_ONLY | 與我觀察一致（我也未取得）。 |
| E-11 | Hackathon proposal 的日期、獎金、評分、資格條件 | Gap Review §1–2（二手） | — | `Identity-md/research@9f7d4a08…` | DOCUMENTED_ONLY（二手；proposal 非正式規則） | 我未重取原文，不可作 H 依據。 |

**「官方 template 是否具備 burn」** → **UNVERIFIED**（無 ABI/source/runtime）。

---

## 4. 發行範圍 blocker 與最小修正（Priorities 1、2）

嚴重度對象為「launch-scope」。類型：C=真實矛盾／M=缺證據／O=選配改善／F=未來功能。

| ID | 類型 | 嚴重度 | Gate | 發現 | 最小修正 | 關閉證據 |
|---|---|---|---|---|---|---|
| **F-01** | M（高度可疑） | **CRITICAL for L** | L,G | true-burn 能力無證據；官方 docs 稱 launch token 為 "plain transfers"。**Launch 後 Token 無法升級補 burn**（規格 §52.1 也不允許擅自升級），故付款前後的不對稱代價大：若發行後才發現無 burn，Paid Genesis 無法依 Owner 已鎖定的決策實作。 | 維持 L HOLD（工程建議）。取得同 Factory/版本的 Token source 或 verified bytecode＋ABI，本地 fork 證明 (a) `burnFrom`+allowance 或 (b) `transferFrom`→Forge→`burn`，且 `totalSupply` 減少、Treasury 增加 0。若不支援：**Owner 另記一項決策**（不由 reviewer 選）。 | 綁定 Factory 地址＋runtime hash＋commit 的 `TEMPLATE_COMPATIBILITY: PASS` 與 Appendix H `exact_burn` 欄位；或 Owner 書面新決策記錄。 |
| **F-02** | M／可能 C | **HIGH** | Q,L | 分配數字來源不一：Launch 頁寫 88/2；docs 寫 `poolBps` 可調（≥1,000，上限 90%），預設未見；live policy 欄位為 `liquidityBps 8000 / treasuryBps 1000 / contributorPoolBps 1000`（80/10/10 型態）。規格寫「official default = 88/10/2」，Appendix C 又列 80/10/10 為「歷史、非現行」。我**無法判定**哪個是 v29 有效值，也無法判斷 `treasuryBps` 的收款人。 | Check 請求**明示**傳 `economics:{poolBps:8800, remainderTo:<Paying Wallet>}`（只在 docs 允許的欄位內；不得改 Owner 比例意圖），並以 Check 回傳的 effective plan 逐項對帳；差異交 Owner。 | Check 輸出（去敏）逐欄＝期望；`poolBps`／`remainderTo` 已寫入 input hash。 |
| **F-03** | M | **HIGH** | L,V,D | 控制權：policy v29 `owners.token/treasury/hookAdmin/lpPosition` 皆為 `0xcecc…a551`（官方稱 launch wallet）。規格 §7.1/§62.2 把這些列為 UNKNOWN，但沒有指出**官方 policy 已顯示這四個角色同址，且不是 Owner 的 Paying Wallet**。含義（推論）：Token owner、Hook admin、LP position、treasury 可能由 IMD 側地址持有；EMVO 是否能 mint/pause/改 hook/移 LP 取決於實作，**未驗證**。 | 規格 Appendix B 的 Authority Matrix 以此為起始事實；Q 前向 IMD 取得（或自行讀 source）：該 launch wallet 是否為多簽／合約、可執行的函式、是否可移轉；Owner 需知悉並接受「EMVO 的 Token/Hook/LP owner 非自己」這一前提。 | §6.2 矩陣各列由 UNKNOWN 變成附 `chainId+address+function selector+source commit` 的實據。 |
| **F-04** | M | **HIGH** | L | **IMD-only fee 無證據**；docs 僅說 "1% to the paying wallet and 0.25% to the network. Anyone can call the distribution"，未說費用資產、是否內部換幣、recipient 是否可變。Pair=IMD 不能推論 IMD-only。 | 規格已正確設為 Owner 待選、預設停在 L 前（§5.2–5.3）。最小補強：L checklist 加一欄「Owner 已書面接受／拒絕混合幣種收費」。 | Hook／collector／distributor source 的 fee accrual 與 `distribute` 路徑摘錄（附 commit），或 Owner 決策。 |
| **F-05** | M | **MEDIUM** | Q | 規格說「標準 token launch」，但 live policy 有 `univ4_hook`（IMD 自己的 Hook）與 `evm_project` 兩個 token kind；`custom_token` 是另一條。規格 §54「no custom v4 Hook」指**專案不自寫 Hook**，但 `univ4_hook` kind 本身就**含 IMD 的 Hook**，兩者容易被讀成矛盾。必須明定 `onchain` kind。 | 在 Q checklist 與 Appendix E 加 `policy_kind` 與 `policy_version`（現為 v29/chain 1/`univ4_hook`，會漂移）。 | Check/Quote 顯示的 kind＋version 與 Manifest 一致。 |
| **F-06** | M | **MEDIUM** | Q | Policy 版本漂移已實際發生：chain 1 `univ4_hook` 在 2026-10-05 為 v19（feeTiers 500/3000/10000），2026-10-06 17:42Z 變成 v29（只有 12500）。文件只說「1.25% 文件參考」。 | Quote 一律綁 `policy version`；若任何欄位在 Quote TTL（600 s）內或之間改變→作廢重做。 | 付款前比對 version/inputHash。 |
| **F-07** | M | **MEDIUM** | Q | `defaultChainId` 是 Sepolia（11155111）。若 `chainId` 漏填，會**靜默**發到 Sepolia；而 Launch 頁與 docs 對 Robinhood/Base 的 open/soon 說法不一致，規格自己已承認 UI 文案曾變。 | Check 請求必須顯式 `chainId:1`、`pairWith:"imd"`；`ipfs/github` 明確 false（本次非部署）。 | Check 回傳 effective plan 的 chainId=1。 |
| **F-08** | M | **MEDIUM** | L | 付款安全欄位（asset/amount/payTo/Permit2 spender/nonce/deadline）已逐項列於 Brief §5，規格 §59.3 亦列。live 值 `payTo=0x4e0f…adbc`、0.5 IMD、TTL 600 s 已取得，但**這是 `launch.open` 的請求費，不含 Token 發行額外 gas／服務費**（gasCeilingWei 5e16＝0.05 ETH 為 policy 上限，付費者歸屬未知）。 | 增列「gas 由誰付、上限多少」到 L checklist；Quote 的 `payTo` 須與 capabilities 的 payTo 相同，否則停止。 | Quote 與 capabilities 逐欄一致。 |
| **F-09** | C（輕微） | LOW | — | 規格 §2.2 說 IMD NFT／Genesis 皆 Mainnet，§1 O-02 同；無矛盾。但 `contributorLockSeconds=3600` 暗示 **Swarm 分配有 1 小時鎖**（推論，語意未證）。規格對「2% 無 vesting」成立與否不受影響，但「No additional vesting or lockup」是針對 Paying Wallet 2%。 | 對外揭露避免寫成「全部分配皆無鎖」。 | 公告文案審視。 |

### 4.1 針對「L HOLD」的專項評估（任務 Q）

**判定：HOLD 合理且應保留。** 理由（事實→推論）：

1. 事實：Owner 已鎖定 BURN_NOT_TREASURY；ERC-20 標準不含 burn（EIP-20）；Appendix C 明記 Owner 拒絕 Treasury 收款。
2. 事實：官方稱 token 固定為 "plain transfers"；規格亦承認無 source 證據。
3. 推論：Token 一旦 launch 即**不可逆**（不得升級／換幣是 Owner 決策的一部分）。因此「發了再說」使 G 路徑可能永久無法依 Owner 意圖實現。
4. HOLD 的**邊界**（我的建議，非 Owner 決策）：
   - HOLD **只**因「Owner 仍要求 true burn」而存在；若 Owner 之後另記決策改變路線（例如接受 permanent-consume 或延後 Paid Genesis 而先發 Token），HOLD 條件隨之改寫——但**這必須是 Owner 的新決策，reviewer 不能代選**。
   - 不應把 HOLD 擴大為「須完成 Genesis 最終合約」：規格 §12.1 也這樣說，我同意。
   - 不應以「ERC-20 `transferFrom` 到 dead address」或「收到 Owner 錢包」取代（§52.2 已禁止；我同意）。
5. 一項**規格自我矛盾風險**：manifest 稱 HOLD 是 "no new Owner approval"、規格 L3 稱「不取代尚待 Owner 確認的決策」，但 §59.3 把它放進 **L checklist** 的勾選項。→ 在 Owner 確認前，它是**工程建議 gate**，不是 Owner 決策；報告與 checklist 應維持此標示（現已標示，OK）。

---

## 5. Fee 方向／收款矩陣（Brief §7 格式）

所有「UNKNOWN」皆為**缺證據**，不是已證不存在。

| Case | Fee basis | Asset accrued | Accounting location | Distribution action | Actual recipient asset | Evidence（本報告） |
|---|---|---|---|---|---|---|
| IMD → EMVO（買入 EMVO） | 池 trade 的 1.25%（docs；基礎＝輸入端或輸出端 **UNKNOWN**） | UNKNOWN（IMD 或 EMVO） | UNKNOWN（Hook/collector/PoolManager） | docs: "Anyone can call the distribution"；函式／觸發者／gas 付款人 UNKNOWN | UNKNOWN（1%→paying wallet、0.25%→network 的**比例**為 OBSERVED_HTTP） | 無 source；NOT_RUN |
| EMVO → IMD（賣出 EMVO） | 同上 | UNKNOWN（EMVO 或 IMD） | UNKNOWN | 同上；是否內部 conversion UNKNOWN | UNKNOWN | 同上 |
| Wallet transfer | 無專案 transfer tax（規格期望；docs "plain transfers" 支持） | n/a | n/a | n/a | 精確收款數需實測（NOT_RUN） | docs OBSERVED_HTTP |
| Paid Genesis burn | frozen price × quantity（TBD） | EMVO，被 burn | 需 Token true-burn；`totalSupply` 減少 | 與 mint 同一交易 | Owner/Treasury 收 0；無 redemption | **SPEC_ONLY**，Token 能力 UNVERIFIED |

補充：
- 「paying wallet」收 1% 是**docs 文字**；policy v29 的 `owners.treasury=0xcecc…`，**兩者如何對應 UNKNOWN**（F-03）。
- 費用只適用官方池（規格 §4.4 正確），無 routing 強制。
- 規格 §6/§4.4 的「100 單位成交額→1 單位屬 paying wallet」算式：**與 docs 一致**（1.25% 內 1.00/0.25），不是「費用池的 1%」。✔

---

## 6. 權限矩陣（Appendix B 的補全與新增事實）

| 元件 | 已知（等級） | 未知／待證 | 風險判斷 |
|---|---|---|---|
| Launch Token | 1B／18／"plain transfers"（OBSERVED_HTTP）；policy `owners.token=0xcecc…` | mint/burn/pause/blacklist/upgrade 能力；是否 proxy | UNKNOWN；**burn 為 L 關鍵** |
| Factory／policy | policy 由 IMD API 發佈，版本漂移（v19→v29）；v27 `evm_contracts` 有 `factory 0xff03…7120`（僅 contracts-only，非 token launch） | token launch 的 Factory 地址、可更新性 | UNKNOWN；Quote 須 pin version |
| Hook（`univ4_hook`） | `hookAdmin=0xcecc…`（OBSERVED_HTTP） | 是否可改費率／收款人／pause | UNKNOWN；非 EMVO Owner |
| Fee collector／distributor | docs：anyone can call | recipient 是否可被重導、failed-transfer 處理、conversion | UNKNOWN |
| LP position controller | `lpPosition=0xcecc…` | 是否鎖定、可否 withdraw/migrate | UNKNOWN；**opening cap 2,500 IMD**（`initialMarketCaps[IMD]=2.5e21`，推論為 IMD 計價；單位語意待確認） |
| Swarm distributor | Merkle；2% 依 accepted work、8% 依 seat；`contributorLockSeconds=3600`（語意推論） | roots／rescue／expiry | UNKNOWN |
| Paying Wallet（Owner） | 簽署者須 EOA／EIP-7702；Safe 不支援 | 實際 fee recipient 是否＝此錢包、能否更換 | **Owner 未提供**；L 無法完成 |
| 未來 Genesis admin | 規格要求 set-once price、分離 open flags | 無 source | G：NOT_RUN |
| Research Collector／Publisher | 規格要求無 signer | 無實作 | I：NOT_RUN |
| 候選 ReleaseRegistry | CANDIDATE_ONLY；無資金、無 mint | 無 source | H：未批准 |

---

## 7. BURN_NOT_TREASURY：相容性、不變量與 G 專項（Priority 2）

**判定：SPEC_ONLY。無 source → 全部測試 NOT_RUN，絕無 PASS。**

### 7.1 規格不變量審視（§15.13 / Appendix H）

| 不變量 | 規格是否清楚 | 我的審查意見 |
|---|---|---|
| `true_burned_atomic == quantity × frozen_price_atomic` | ✔ | 加一條：價格＝0 或 quantity＝0 一律 revert（§12.3 已含 quantity=0；price>0 在 §13.2 `require p>0`）。 |
| Treasury/Paying Wallet 成本入帳 = 0 | ✔ | 需明確**含**「Forge 暫存餘額殘留 = 0」（Appendix H 有 `forge_cost_residue_atomic` ✔）。 |
| Mint 失敗全回滾 | ✔ | `_safeMint` 回呼重入已列（§15.10）。補：receiver 回呼中**再次呼叫 burn 路徑**。 |
| allowance／回傳值 | ✔（§15.12 "false/no-return ERC-20 行為明確處理"） | 這是 **ERC-20 interaction 相容性測試**，若 Token 不支援 burn 它就無意義；順序：先 F-01。 |
| totalSupply 減少 | ✔（§15.2） | 注意不要把「mint 抵銷」與同區塊其他交易混入（規格已提醒）。 |
| 無回收／rescue／upgrade／delegatecall | ✔ | 這條必須在 **Token（IMD 控制）** 與 **Forge（專案控制）** 兩邊都成立；目前 Token 端 owner 非 Owner（F-03）。 |
| 無 redemption／reissue | ✔ | 同上。 |

### 7.2 容量與資格
- F／R／P 隔離與 `MAX=F+R+P` 邏輯自洽（§9.2）。我檢查了邊界：若 R=0 且有效漏列超出 F，規格已說「停止、交 Owner」（§9.3）。✔
- `claimed[tokenId]` 共用於 normal/remediation，與 current-owner 檢查分離（§8.1、§8.3）。✔
- **缺口 G-1（MEDIUM，G）**：§8.1 說 claim 時 `IMD.ownerOf(tokenId)==msg.sender`，但沒指定 **IMD NFT 的 collection 地址／chain 驗證**如何綁入 Merkle leaf（§15.12 有「proof 綁 chain、collection、epoch」要求 ✔，建議在 §8.1 偽碼同步）。屬文件一致性，非漏洞。
- **缺口 G-2（MEDIUM，G）**：remediation 的「approver／Safe」在 §8.1A 提及 "Safe / authorized remediation approval"，但沒有說明**由誰授權 root／entitlement 的更新**、是否有 timelock／事件公告。建議最小規格：remediation 只能把已存在於「原公告資格快照」中的 tokenId 加入，且每次更新發事件並對應公開 evidence hash。
- **缺口 G-3（LOW）**：NFT burn 後 `totalSupply` 下降不得重開容量：規格已寫（§9.2）。✔ 建議測試明確以「累計 minted counter」而非 `totalSupply()`。

### 7.3 Burn 實測表（Appendix H 欄位；全部 NOT_RUN）

| 檢查 | 狀態 | 原因 |
|---|---|---|
| `exact_burn` | **NOT_RUN** | 無 Token source／ABI／fork |
| `atomic_revert` | NOT_RUN | 無 Forge 實作 |
| `no_treasury_receipt` | NOT_RUN | 同上 |
| `no_recoverable_cost` | NOT_RUN | 同上 |
| `free_and_remediation_zero_cost` | NOT_RUN | 同上 |
| `capacity_and_claim_isolation` | NOT_RUN | 同上 |
| `no_redemption_or_reissue` | NOT_RUN | 同上 |
| `TEMPLATE_COMPATIBILITY / true_burn_template` | **BLOCKED** | 缺 Factory／Token 版本 source；這同時是 L HOLD 的直接原因 |

> 任何 generic mock ERC-20 的通過**不得**當作本表 PASS（規格 §15.13 亦如此要求）。

---

## 8. Gate I：研究平台（Priority 3、4）

### 8.1 I-01..I-15（規格 §75.2）狀態——全部 **NOT_RUN**（無實作）

| ID | 案例 | 我的 SPEC_REVIEW | 狀態 | 若實作需補 |
|---|---|---|---|---|
| I-01 | 同 ticker 不同鏈／合約 | 規格 §68.1：以 chain+address 識別；足夠 | NOT_RUN | fixture：同 symbol 兩鏈兩合約，價格來源不可交叉 |
| I-02 | 假 NFT collection 與官方同名 | §68.1 relation 需 evidence；足夠 | NOT_RUN | fixture：偽造 collection 宣稱 official |
| I-03 | 成交量／floor／bid 單位不同 | §68.2 要求單位、decimals；足夠 | NOT_RUN | 以 raw integer＋decimals 比對 |
| I-04 | Proxy 變更後舊審計仍引用 | §70.2 影響圖；足夠 | NOT_RUN | implementation 位址變動→NEEDS_RECHECK |
| I-05 | 來源 403／空值 | §74、§71.4；足夠 | NOT_RUN | UNAVAILABLE≠0 |
| I-06 | reorg／供應商更正 | §68.3 提到 finality 策略，但**未給 confirmation 深度或 reorg 偵測方法** | NOT_RUN | 規格補：每條鏈 finality 規則與撤回流程（建議，待 Owner/工程決定數值，不由我捏造） |
| I-07 | 外部 README 要求加分／付款 | §74.3 | NOT_RUN | 注入字串＋工具權限邊界測試 |
| I-08 | 重送／並行超額 | §73.2、§73.4 | NOT_RUN | 兩個併發請求只保留一筆 pending budget |
| I-09 | Genesis 轉手／多登入 | §72.2 帳本分離 | NOT_RUN | 轉手前後 ACL、額度不重置 |
| I-10 | 贊助方要求刪除負面結論 | §70.3、§74.1 | NOT_RUN | 更正流程留痕 |
| I-11 | Pet 台詞回流研究 | §27.6、§70.4 | NOT_RUN | 標記 fiction 的資料不得進 evidence store |
| I-12 | 舊 cache／撤回版本 | §71.4、§41.2 | NOT_RUN | 撤回版本 hash 黑名單 |
| I-13 | 模型擴 token／抓無限來源 | §73.4 | NOT_RUN | 硬上限與 stop |
| I-14 | 關網站即宣稱排程取消 | §73.3；**已被 live docs 佐證**：cancel 在 IMD 團隊（OBSERVED_HTTP） | NOT_RUN | UI 狀態必須反映服務端狀態 |
| I-15 | Burn 金額填為研究收入 | §51、§55.2 | NOT_RUN | 會計欄位型別隔離 |

### 8.2 建議補強（Gate I 缺口；非 launch blocker）

| ID | 類型 | 嚴重度 | 發現 | 最小修正 |
|---|---|---|---|---|
| I-G1 | M | MEDIUM | reorg／provider correction 沒有量化 finality（§68.3）。 | 規格加 per-chain `finality_policy`（Owner／工程選值）；I-06 測試以它為準。 |
| I-G2 | M | MEDIUM | 私人筆記的**刪除／匯出**（隱私法規）與 append-only 日誌的衝突僅一句話帶過（§70.3）。 | 規格加：私資料不入 append-only 公開日誌；僅存去敏 hash；保存期限由 Owner 決定。 |
| I-G3 | M | MEDIUM | 「額度轉手重領」只有原則（§72.2），未列威脅模型。 | 新增 I-16：同一 NFT 於短時間內 A→B→A 轉手或在兩個帳戶間 flip，不得重置／疊加額度；以「額度綁 service account＋period，而非 tokenId」為候選設計（待 Owner 定，不預設）。 |
| I-G4 | M | MEDIUM | 贊助／自家項目揭露有欄位（§71.2 `commercial.relationship`）但**無強制發布前非 UNDECLARED 的 validator**。 | 新增 I-17：`commercial.relationship=UNDECLARED` → 禁止 publish。 |
| I-G5 | O | LOW | 單位：§68.2 要求 raw integer＋decimals，但 `claims.json` 範本無數值欄位型別。 | 範本補 `amount_atomic:string`、`decimals:int`、`asset_ref`。 |
| I-G6 | M | LOW | Research ingestion 的 SSRF／下載防護引用 §33.1，但 Research 資料來源（任意網址、PDF、repo）比 Dream Room 更廣。 | 新增 I-18：Collector 使用 allowlist；測試 redirect→metadata host。 |

### 8.3 其他 Priority 3/4 檢視（SPEC_REVIEW）
- **Hall／fast page 共用資料**：§67.3、§29.3 ✔；建議僅有**單一 published pointer**，兩者讀同一 `manifest` hash（規格隱含，未明說）。
- **無虛構世界證據**：§27.6、§70.4 ✔。
- **Budget／idempotency／pending**：§73.2/73.4 ✔；與 live docs「Retries reuse the order and never charge twice」一致（OBSERVED_HTTP）。
- **Research vs Creation Mode**：§27.1 ✔。
- **無 auto-topup、無財務 signer**：規格 ✔；**注意**：capabilities 顯示 `schedule.topup` 可由**任何錢包**付款；因此「無 auto-topup」必須由**不給任何工具簽名／session 授權**來保證，不能靠 UI。規格 §56.3 已寫，維持。
- **停止控制**：E-09 佐證規格 §73.3：Owner 不能單方取消已付 schedule。A2（預付批次）因此應維持**不啟用**；我同意。

---

## 9. Genesis／World／Research 整合（與 L 分離）

- Genesis（Free＋Paid＋Remediation）、配件／Pets、Ecosystem Hall、IMD-anchored Dream Hall：規格全部保留，且 §36.1/§59.6/§63 明確「D1+ 不自動阻擋 Token L」。我同意。
- Research 範圍為 crypto token／NFT，不限 IMD／AI：§67.1 ✔。
- 服務／額度／finite batch 皆為 proposal，無價格、無啟用：✔（§73、§76）。
- 無 staking／yield／backing／自動交易／AI 財務權：§54、§56、§62.5 ✔；**未發現規格內有隱性違反**。

---

## 10. U0–U4、資料與虛構邊界、最小 I/D 驗收

- U0–U4（§56.1）：分類以「實際影響」為準 ✔。補一條（LOW）：**前端交易目標地址與 RPC 設定屬 U3/U4，不是 U1**（§56.1 已提「改前端地址…」，建議列入 D-T 測試：D-T11「更換 mint 合約地址的 JSON 變更被拒」）。
- 資料／虛構：單向引用 ✔。
- 最小 I 驗收（§75.1）：一個 Token＋NFT 項目、兩次快照、兩版研究含 diff、撤回行為；我認為足夠且不誇大。
- 最小 D 驗收：D-T01…D-T10 ✔；全部 NOT_RUN。

---

## 11. 同業比較（選配）

規格保留 CLAUS／HIVE 為 REFERENCE_ONLY；我**未重驗**（規格也宣告未重跑 S4–S15）。不採納 redemption／staking／proxy，不影響本次判定。

---

## 12. H：黑客松（與 Token 發行分離）

| 項目 | 狀態 | 說明 |
|---|---|---|
| 該 proposal 是否被採用／年份／起訖／網路／投稿路徑 | **UNCONFIRMED** | Gap Review 自承未取得正式規則。proposal 的 Oct 5–19（UTC）若屬 2026，今天（2026-10-07）已在期間內（推論；以 proposal 為前提）。 |
| 既有專案＋新工作是否合格 | UNCONFIRMED | 需 baseline commit 與主辦答覆。 |
| 標準 Token＋獨立產品合約是否合格、可否分次部署 | UNCONFIRMED | |
| DreamHallReleaseRegistry | CANDIDATE_ONLY | 無資金、不 mint、不改 EMVO；jobId 上鏈**不是**對 IMD accepted job 的密碼學驗證（Addendum L70 已聲明）。 |

**H gap matrix（精簡）**

| 需求 | 現有證據 | 缺 | 最小改動 | 批准者 |
|---|---|---|---|---|
| 可重現公開 repo＋固定 commit | 只有規格 repo | 應用程式原始碼 | 另建 submission repo（去敏） | Owner |
| 可運作自訂合約＋成功呼叫交易 | 無 | 合約、測試、部署、TX | 先取得主辦對網路與資格的書面答覆再實作 | Owner＋主辦 |
| IMD 依賴功能（真實 job） | 無 | 付費 job、artifact、review | Owner 手動批准一筆 job | Owner |
| 負面測試 | 清單存在 | 執行結果 | 於本地跑 | 工程 |
| X 帳號／收款錢包 | 無 | 全部 | 依最終規則 | Owner |

**兩個分離判定**：標準 Token 發行準備度 = **L HOLD**；黑客松提交準備度 = **NOT ESTABLISHED**。兩者互不替代。

**給主辦的問題**：已採用？年份／截止／網路？既有 World＋新模組？Token 與產品合約是否可分次部署、是否須同一 IMD job？「meaningful on-chain functionality」是否排除單純 hash/事件？（沿用 Gap Review §9，我未新增。）

---

## 13. PATCH_PLAN

類型：**OWNER**＝需 Owner 決策；**ENG**＝工程建議；**DOC**＝文件一致性。

| # | 來源章節 | 變更 | 理由 | 類型 | Gate | 關閉測試 |
|---|---|---|---|---|---|---|
| P-01 | §59.3 L checklist、Appendix E | 新增欄位 `policy_kind`、`policy_version`、`poolBps`、`remainderTo`、`gas_payer/gas_ceiling` | F-02/05/06/08 | ENG | Q/L | Check effective plan 與 Manifest 逐欄相符 |
| P-02 | §3.1、§59.2 | `chainId:1`、`pairWith:"imd"` 必須**出現在送出的 input**；`defaultChainId` 為 Sepolia 的警示 | F-07 | ENG | Q | Check 回傳 chainId=1 |
| P-03 | Appendix B | 以 policy v29 的 `owners.*` 為 Authority Matrix 起始事實；列出「Owner 非 Token/Hook/LP owner」風險 | F-03 | ENG／**OWNER 需知悉** | L/V | 每列附 address＋selector＋source commit |
| P-04 | §52.1／§59.3 | 保留 L HOLD；補一句「HOLD 解除只有兩條路：(a) 同版 Token 能力證據；(b) Owner 另記新決策」 | F-01 | ENG；(b)=**OWNER** | L | `TEMPLATE_COMPATIBILITY` 證據或決策記錄 |
| P-05 | §5.2、§59.3 | 加「Owner 對混合幣種收費的書面接受／拒絕」欄 | F-04 | **OWNER** | L | 決策記錄 |
| P-06 | §8.1A | 補 remediation 授權者、事件公告、與原公告快照的綁定；不增加 admin free mint | G-2 | ENG | G | 合約測試：非快照 tokenId 被拒 |
| P-07 | §8.1 | 偽碼加入 IMD collection address／chain 綁定與 leaf 編碼 | G-1 | DOC | G | proof 重放測試 |
| P-08 | §68.3／§75.2 | 加 `finality_policy` 與 I-06 判定標準 | I-G1 | ENG（數值＝**OWNER/工程**） | I | I-06 PASS |
| P-09 | §70.3 | 私資料不入 append-only 公開日誌；刪除／保存期限 | I-G2 | ENG／**OWNER（期限）** | I | 隱私測試 |
| P-10 | §75.2 | 新增 I-16（額度轉手 flip）、I-17（UNDECLARED 商業關係禁止發布）、I-18（SSRF）| I-G3/4/6 | ENG | I | 新測試 PASS |
| P-11 | §61.2 | 新增 D-T11（交易目標地址變更被拒） | §56.1 | ENG | D | 測試 PASS |
| P-12 | 規格 §1 與 Appendix A | **Decision ID 對齊不完整**：§1 只列 O-11..C-19，O-01..O-10 僅在 Appendix A；manifest 稱 "aligned across section 1 and Appendix A"。建議 §1 加註「O-01..O-10 見 Appendix A」。另 O-11 在 §1 為「本次 Owner 明確選擇」，在 Appendix A 為「本次再確認」，措辭統一。 | 文件一致性 | DOC | — | diff 檢查 |
| P-13 | §3.2 | 「88/10/2」標為 **Launch 頁文案**，加註 policy v29 欄位 80/10/10 型態與 `poolBps` 可調，待 Check 對帳 | F-02 | DOC | Q | 對帳完成 |
| P-14 | Brief §14 | 要求輸出檔名 `artifacts/emvo-prelaunch-review.md`，與本任務要求 `artifacts/report.md` 不同 → 以任務為準 | 交付契約 | DOC | R | — |

---

## 14. 待 Owner 提供的輸入、Q/L 精簡清單、後續檢查、限制

### 14.1 Pending Owner inputs
1. **決定性**：是否維持「必須 true burn」；若 Token 能力不支援，要走哪條（reviewer 不代選）。
2. Paying Wallet 地址（EOA／EIP-7702）；是否同為 fee recipient。
3. `poolBps`／`remainderTo` 明示值；`onchain` kind（`univ4_hook` 或 `evm_project`）。
4. 對「IMD-only 費用未證實」的立場（等待證據，或接受混合並手動處理）。
5. 接受（或拒絕）「Token／Hook／LP／treasury owner 為 IMD launch wallet」這一前提。
6. Genesis：BURN_PER_MINT、F/R/P、資格窗口、Free 期限（皆 TBD，不屬本次）。
7. 研究：coverage、finality、保存期限、provider/model、預算與停止方式（皆 TBD）。
8. H：向主辦取得書面規則。

### 14.2 Q 清單（不付款即可完成）
`[ ]` Check 請求含 `chainId:1`、`pairWith:"imd"`、`onchain` kind、`economics`；`[ ]` effective plan 與 Manifest 對帳；`[ ]` policy version／input hash 記錄；`[ ]` IMD 地址與 decimals 以 RPC 確認；`[ ]` Quote payTo/asset/amount 與 capabilities 一致。

### 14.3 L 清單（Owner 簽署前）
沿用規格 §59.3（16 項）＋P-01 新欄位；**其中 true-burn 項與 fee-asset 項目前皆為「未滿足」**。

### 14.4 Postlaunch（V）
實際 Token runtime／PoolKey／PoolId／allocation 事件／第一筆 distribution 的資產與收款人；與 Prelaunch Manifest 比對；Owner 另批准的小額實測。

### 14.5 限制與未回答問題
- **未執行**：任何 code 測試、fork、RPC 讀取、Check/Quote、payment、簽名、broadcast、swap、approve、schedule、child job。
- **未取得**：Factory／Token／Hook source；EMVO quote；Paying Wallet；hackathon 原文與主辦規則；GitHub `main` 現況；`openapi.json`。
- Live 證據為 IMD **自述 HTTP**，可隨時改變；本報告值僅代表 2026-10-07 ≈08:05 UTC。
- 我對 policy 欄位（`contributor*`、`perWalletCapBps`、`treasuryBps`）的語意**不作斷言**。
- 多個「Reviewer」非獨立：本報告為單一 agent，**沒有**多席位或獨立運行時的佐證。
- 未發現的問題不等於不存在；本報告不是 audit、認證或 GO。
- **最終**：**L = NOT AUTHORIZED**；R=READY（SPEC_ONLY）；Q=NOT READY（可補）；V=N/A；G/D/I=NOT_RUN；H=UNCONFIRMED。
