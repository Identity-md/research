# EmberEvo（EMVO）第二輪 Token Report｜R2 v1.1

**截至 2026-10-07，UTC。** 本報告只評估 Ethereum mainnet 官方標準 `evm_project` 發行方向及日後 Genesis 付款相容性；屬公開只讀研究與隔離測試，並非合約審計、發幣認證或金融批准。證據用語：**Owner 決策**是產品要求；**觀察**是指定時間的 HTTP／鏈資料；**TEAM**是提交者測量；**本輪實測**只對其運行環境有效；**推論**與**未知**另標。

## 執行摘要

Owner 後續明定首發總供應 **86% Pool／10% Swarm／4% 指定錢包**，以及 Paid Genesis 以精確 EMVO 轉入 `0x1C651928150DADDDA9C2C040a9D4901d862f8eC4` 並在同筆交易 mint NFT；無必要燃燒、日後強制燃燒、backing 或贖回。該地址格式與意向已知，**控制權、實際 payer、最終部署收款人尚未證明**。[最新決策][S05]取代[R1][S03]的 burn 前提與 88/10/2 選擇；不把 R1 的 `NOT_RUN` 改寫為技術通過。Owner 可持有、轉讓、出售或自行兌換收到的 4% 與 Mint 款，分帳只追溯資產來源，無強制 World 預算、Safe、vesting 或 AI 金融權限。

此輪可確認免費 Check 曾接受明示 86/10/4，並取得一個同 Factory 標準 `evm_project` 的 QOBS Token runtime 與一個 `custom_token` 混合幣種 fee claim。**兩者均非 EMVO／其 IMD 池**。最重要的 L 缺口是選定路線的有效 policy／fee 實作、完整 Factory／LP／collector／distributor 控制權、IMD-only 實收、及 exact Quote。公開 `evm_project` policy v18 的 `feeTiers=[500,3000,10000]`，而今日文件與樣本 `LaunchFees.poolFee()` 顯示 12500；不能用最高編號的 `univ4_hook` v29 代替 v18，也不能忽略此差異。[政策][POL][文件][DOC][只讀結果][RPC]

## R1 發現逐項處置

| ID／R1 出處 | 現行要求與新證據 | 狀態 | 證據等級 | Test | Severity | Gate | 最小結案／責任 |
|---|---|---|---|---|---|---|---|
| F-01 §4：true burn 無模板證據 | Owner 改精確 EMVO 收款；QOBS Token source 僅繼承 ERC20。 | **SUPERSEDED_BY_OWNER_DECISION**（burn 前提） | `SOURCE_INSPECTED`＋`SIMULATED` | 樣本 PASS；EMVO／Final Genesis `NOT_RUN` | 原 CRITICAL 已失效；付款待證 | L/G | 工程核實選定 Token 與真實 EMVO；Gate G 審原子付款，不稱 burn PASS。[S03][S05][TOK] |
| F-02 §4：UI88 與政策 80/10/10 未對帳 | 明示 8600 的免費 Check HTTP200、`judged=true`、零 blockers；回覆寫 86%，但 access/dependencies 仍 assumed/unknown。 | **PARTLY_CORRECTED** | `OBSERVED_HTTP` | allocation event `NOT_RUN` | HIGH | Q/L/V | IMD 給 v18 選用規則、分母、default/override、分配合約；Owner 對 exact plan 對帳。[CHK][DOC] |
| F-03 §4/§6：policy `owners.*` 同址 | v18 HTTP 同址；QOBS 樣本由該址呼叫 Factory。Token／Factory `owner()` revert，Factory `fees()`、Fees getter 局部可讀。 | **OPEN_EVIDENCE_GAP** | HTTP＋樣本 `OBSERVED_ONCHAIN` | 全面權限 `NOT_RUN` | HIGH | L/V | IMD 提供全部 source、ABI、selector、proxy/admin、LP／Merkle 權限；Owner 判斷控制模型。[POL][RPC] |
| F-04 §5：IMD-only 未證 | launch737 同 Factory 的 `custom_token` claim 之 ERC20 `Transfer` 實收 IMD 與 ZTO，各 80% requester／20% network。 | **OPEN_EVIDENCE_GAP** | 單例 `OBSERVED_ONCHAIN` | 標準 EMVO `NOT_RUN` | HIGH | L/V | IMD 給同版 `evm_project` IMD 池雙向 swap、accrual、claim／conversion trace；混幣需 Owner 另決。[FEE] |
| F-05 §4：kind 未釘 | capabilities 開放 chain1／`imd`／`evm_project`；v18 對應此 kind，v29 是 `univ4_hook`；Check 輸入是 `evm_project`。 | **PARTLY_CORRECTED** | `OBSERVED_HTTP` | Quote `NOT_RUN` | MEDIUM | Q/L | Q 明示 kind；IMD 確認真正套用的 policy／Factory，避免自訂 Token／Hook。[CAP][POL][CHK] |
| F-06 §4：policy 漂移 | v18、v19、v29 並存；Docs 說 Quote pin policy version，Check 不保價。 | **OPEN_EVIDENCE_GAP** | `OBSERVED_HTTP` | pin/expiry `NOT_RUN` | MEDIUM | Q/L | exact Quote 比 `inputHash`、`policyVersion`、有效期、code 版本；Owner 批准差異。[DOC] |
| F-07 §4：鏈與 pair 預設 | API `defaultChainId=11155111`、`pairWith=eth` 預設；Check 明示 1／`imd`；R1 曾把 launch 欄混入 Report input。 | **PARTLY_CORRECTED** | `OBSERVED_HTTP` | 部署 `NOT_RUN` | MEDIUM | Q/V | Q 核 chain1、IMD address／decimals、PoolKey；Report 不送 launch 參數。[CAP][CHK] |
| F-08 §4：款項／gas 未清 | capabilities 列 `launch.open` 0.5 IMD、主網、18 decimals、TTL600s；Docs 說 server 支付該 x402 gas。 | **OPEN_EVIDENCE_GAP** | `OBSERVED_HTTP` | Quote／支付 `NOT_RUN` | MEDIUM | L | Owner 核 exact payment、spender、nonce、deadline、額外 gas 及原單狀態。[CAP][DOC] |
| F-09 §4：Swarm lock 推論 | v18 有 `contributorLockSeconds=3600`；Swarm 10% 經 Merkle claims。欄位範圍未知；Owner 4% 無新增 lock。 | **OPEN_EVIDENCE_GAP** | `OBSERVED_HTTP` | claim `NOT_RUN` | LOW | Q/V | IMD 提供 distributor source、root/claim/lock 設定與樣本；文案區分 4% 與 Swarm。[POL][DOC] |

R1 的嚴重度只屬當時前提；本輪不能把「plain transfers」當無 burn 的證明。G-2 補救可納入原資格規則下被錯誤名單漏列的 tokenId，不能要求它原本就在錯名單；但 root 批准者與測試仍缺。I-G4 的 `UNDECLARED` 禁發在歷史 §71.2 已有文字，缺的是 validator 實作證據。[R1][HIST]

## 配額、路線與 Q 欄位草案

按今日文件 `poolBps` 是**總初始供應**的基點；Swarm 固定 10%，其餘 90% 才在 Pool 與 `remainderTo` 間分配。假設標準 1,000,000,000／18 實現，明示 8600／指定地址為 **860M／100M／40M**；UI 88/10/2 是舊預設文案，**880M／100M／20M**；省略欄位的有效結果仍未核定，政策 `liquidityBps=8000, treasuryBps=1000, contributorPoolBps=1000` 不能直接當成 80/10/10 發行結果。是否即時可轉讓須看實際分配與 vesting code；Owner 不批准另加鎖。[DOC][UI][POL][CHK]

**非執行 Q 清單**：`action=launch.open`、標準 `onchain=evm_project`、`chainId=1`、`pairWith=imd`、name/symbol、`economics.poolBps=8600`、`economics.remainderTo=0x1C651928150DADDDA9C2C040a9D4901d862f8eC4`；核對 1B／18、IMD 地址、default opening cap、paying wallet、policy kind/version、PoolKey、recipients 與 Check effective plan。`github`／`steps`／任何產物、額外專案合約欄位須先澄清：TEAM Check 曾帶 `github:true` 與 build/review steps，回覆計畫含建約與部署文字，零 blockers 只說這份描述可接受，**不保證只做標準 Token 或不產生附加物**。本 Report 本身無上述 launch 欄、無 request submission。[CHK][DOC]

**分母與預設的證據界線。** 公開文件同時用「九成給 requester」與「`poolBps` of the supply」描述分配，並明言 project/hook 可選填 `poolBps`、`remainderTo`。因此 8600 表示總供應的八成六，而不是九成之內再乘八成六；在十億供應假設下，剩餘四千萬與指定地址相連。這是**文件語意及數學推導**，尚非鏈上 `Transfer`、Merkle 根或 LP 頭寸之核算。Check 的 `facts.token_split` 雖寫八成六，仍未輸出分配交易、recipient balance 或本案 quote 的 calldata。若 UI 文案八成八是某一版預設，它不能覆蓋 Owner 的明示輸入；若 API 在該 policy 下另有 floor、cap 或 wallet 限制，也需由服務端給有效計畫而不能由我自行補欄位。[DOC][UI][CHK]

**版本可比性。** capabilities 告知某種 kind／pair 在某鏈開放，只說入口可用；policy 清單列多版，並未在本次資料中證明 quote 對該輸入最後選哪一版。樣本 launch884 的 Registry log 確認 kind `evm_project`、source commit 與 artifact，而其 `launch.json` 寫的 pairedCurrency 是原生 ETH，且 sample 88% 配額；這對 Token 模板來源有價值，對 EMVO/IMD 的初始池深度、發費幣種和 86% 分配沒有直接驗證力。把上述不同層級分開，才可以在 Q 準備欄位，同時保留 L 的實作風險。[DLOG][PLAN][POL]

## 權限矩陣：可觀察能力與未知控制

| 元件／樣本定位 | 讀到的權限線索 | 尚不能判定 |
|---|---|---|
| QOBS Token `0xAd455EE2800B314588B5178dF0dCBBC5dAD7E1c7`（chain1，launch884） | source commit `53c8e396…eea3` 的 `LaunchToken.sol` constructor 一次 mint 1B；ABI 僅 ERC20 典型方法；`totalSupply()` selector `0x18160ddd`、`decimals()` `0x313ce567`；runtime SHA-256 `34c88e…9062f`，block 26139425。 | 非 EMVO；未獨立重編 solc0.8.26/Cancun；ABI／`owner()` revert 不證 Factory、Hook 或其他合約無權。[TOK][ABI][RPC] |
| Factory `0xfF03410d0Fe5fa8f7F59F743de35E333D9857120`／policy | launch884 交易指向 Factory；`fees()` selector `0x9af1d35a`→`0x12c9E1007262AfAC205567457F5826a9416a3863`，Factory runtime `c0704d…f5d9a72`；v18 `owners` 同 `0xcecc29b037f5064fcdf45a5c318f132ef76aa551`。 | `owner()` selector `0x8da5cb5b` revert 非完整 ownerless 證明；setters、delegatecall/proxy、部署參數／收款改向與路線版本待 source。[DEP][RPC][POL] |
| LaunchFees `0x12c9E1007262AfAC205567457F5826a9416a3863`／collector | `owner()` `0x8da5cb5b`／`treasury()` `0x61d027b3`→`0x047F606fD5b2BaA5f5C6c4aB8958E45CB6B054B7`；`feeRecipient()` `0x46904840`→`0x3f252e859a277a86A3967c11D4E054B2f07a1F22`；`poolFee()` `0x089fe6aa`=12500，runtime `bc5792…973cc35`。 | 各地址角色非 Owner 錢包，fee beneficiary 不等於 admin；費率／recipient 可改性及 trigger／gas／conversion 未知。[RPC] |
| 官方 Hook、LP／position、Swarm distributor、任何 ProxyAdmin | 樣本 registry 另列 artifacts `0x380b9f1A53FFdb3725135E428d9765D382138BEB`、`0x44E8c4Cfa22626145065A33d5eC74fEdFe28c719`、`0x784FF9a3ac5d88A30bfff6F7f2a270161FBE6000`；未在此判定角色映射。 | 各實際合約的 selector、upgrade／pause／mint／rescue／withdraw／migration／root 更新、持有人及可轉移性均未完整核實。不能把 v29 hook 角色套到 v18 `evm_project`。[DEP][POL][DOC] |

鏈觀察固定 chain1 block **26139425**，Blockscout block hash `0x03089d7b…6d9`；launch884 tx 在 block **26139046**、hash `0xc088d2c9…63c4`。樣本與本案待發行實例之間只具路線線索，沒有 EMVO 的實際地址、代理實作或 runtime。[RPC][BLK][DEP]

**哪些權限還不能從 getter 推出。** QOBS `LaunchToken` source 沒寫 owner、pause、後續 mint 或 blacklist 入口，ABI 亦未列這些方法，這是對**該樣本 Token**較強的負面線索；但不能因 `owner()` 呼叫 revert，就推論 Factory 的部署授權、LaunchFees 的收款改向、LP 的退出或 Merkle root 管理都不存在。`fees.owner()` 顯示的地址屬 collector 合約權限線索，`feeRecipient()` 是網路收入目的地；兩者與 requester fee beneficiary、Owner 的 4% 地址及 API `payTo` 各有不同作用。若任何元件是 proxy，還需在同一 block 讀實作地址與管理槽，將 verified source 對上 runtime。這些證據目前未齊，故矩陣中的「未知」不是「已證有危險後門」，也不是「已證無管理權」。[TOK][ABI][RPC]

Owner 要能作有效選擇，應取得每項可執行能力的**函式簽章／selector、呼叫者限制、持有人、可轉讓條件、事件及實際位址**。尤其同一 `0xcecc…a551` 出現在 policy 的多個名稱欄，只說服務方聲稱將角色指向該址；地址是否仍控制該角色、是否為 EOA 或能經其他合約間接調權，需由部署資料與合約程式證明。費用受益權和管理權不能互換，也不能把「Owner 可賣 4%」誤寫成 Owner 可以移除官方 LP。[POL][DEP]

## 費用與收款資產

| 動作 | 費率／累積位置 | 分配、轉換、實收與 gas |
|---|---|---|
| IMD→EMVO 買入 | 文件說今日 factory 交易 1.25%，其中 1% payer／0.25% network；扣費基礎、資產、Hook/LP/collector 帳本未證。 | claim 函式／觸發條件、是否換幣、實際收款地址與幣種、rounding、zero-fee、失敗處理、gas payer 均**未知**。[DOC][POL] |
| EMVO→IMD 賣出 | 同上，方向可能改變累積資產，不能依 pair 名稱定論。 | 同上；需各方向 trace、重複 claim 與 recipient-change 測項。[DOC] |
| 一般 Token 轉帳 | QOBS 樣本 source 為標準 ERC20，無專案 transfer tax。 | 樣本本地精確轉帳可行；真 EMVO 仍 `NOT_RUN`，gas 由實際交易發送者按路徑負擔。[TOK][TEST] |
| 未來 Paid Genesis | `quantity ×` 凍結的 `MINT_PRICE_EMVO`，Token `transferFrom` 收至經確認地址；**無 burn**。 | 同筆 mint NFT 或全回滾；收的是 EMVO，不是 IMD 池費，且沒有自動換幣。價格、資格、F/R/P 仍 TBD。[S04][S05] |

launch737 的 `claimFees` 交易 `0xd751…7259`（block 26135240，hash `0x14d539…f29`）有 **12 logs**；以 ERC20 `Transfer` 的 token contract、from/to/value 重算，requester `0x7B8C…0479` 收 IMD 66.4319… 與 ZTO 2,839,361.822…（各約 80%），network `0x3f25…1f22` 收其餘約 20%。`FeesPaid` explorer decoded 欄名與 indexed 值對應不宜單獨採信；以 Transfer 為實收依據。這是 **custom_token、ZTO/IMD、同 Factory** 的一筆觀察；`evm_project` QOBS 樣本甚至以 ETH 配對，故未建立未來 EMVO/IMD 的同版費用路徑可比性。**IMD-only：尚未確立；也不能以此一例宣稱必混收。** Owner 尚未接受混幣。[FEE][DEP][PLAN]

**費率與到帳是兩個不同問題。** `poolFee()` 回傳 12500，若採 Uniswap 百萬分率通常相當於 1.25%，與文件宣傳一致；然而單一 getter 無法說明是買方輸入端扣、賣方輸出端扣，亦未回答 collector 從 PoolManager 提取時收到何種 token。launch737 的兩種 ERC20 實收足以反駁「凡是 IMD 配對都必然只到 IMD」這種普遍命題，卻不能推翻「未來某一標準 EMVO 池可能由另一 Hook／conversion 機制只付 IMD」。尤其 policy v18 費階與樣本 getter 不一致，須先確立實際路徑再做同版類比。不能把 Genesis 的 EMVO 售款混作官方 1% 池費，或把尚未 claim 的帳面值當可用 IMD。[DOC][POL][RPC][FEE]

可關閉此缺口的最低證據是：標準 `evm_project` 連接 IMD 的 PoolKey／Hook 與 collector source、兩個方向的既有 swap trace、對應的 fee accrual state 與 claim transaction，並以 `Transfer` 或餘額變化對照每個實收資產。還應包括少額取整、零額、重複分配、失敗 token transfer、誰能呼叫／支付 gas、recipients 是否能改，以及若有內部 swap，其最小輸出、路由與滑點保護。當前無此完整鏈條，因此此報告不試算 Owner 未來收入或建議自動換幣；若官方結果是混合幣種，應把幣種及操作成本交 Owner 另行決定。[HIST][DOC]

## Paid Genesis 相容性與獨立重跑

TEAM 公開 receipt 稱 fixture **10 TAP PASS**（9 子項＋父項），QOBS runtime／synthetic storage **4 checks PASS**。我讀了 test source，並在 `/tmp` 安裝指定主套件版本、獨立執行同兩個本機命令：fixture **10/10 PASS，0 FAIL，34.09 秒**；runtime **4/4 PASS，exit 0**，驗證植入 runtime 的 storage、收款地址、無 allowance 回滾、精確收款加 NFT 且 supply 不變。Node24、solc0.8.30、OpenZeppelin5.4、ethers6.15、Ganache7.9.2／Shanghai；本輪生成 lock SHA-256 `dd00dd14…e4477da1a3074` 與 TEAM lock `ea306a10…36c2b15` 不同，不能稱逐 byte 同環境。µWS native 模組未載入，Ganache 使用 JS fallback。[TEST][RUNTIME]

fixture 驗證正常收款、allowance／balance 不足、false／fake success、fee-on-transfer、第二次 ERC721 callback 拒收全回滾、重入、max allowance、no-return。runtime 重播把 launch884 code 植入本地帳戶並人工配置 balance/supply，非主網 fork；測試成本與 NFT probe 皆合成。Probe 刻意拒絕 payer=recipient，只是未決 self-payment 測試選項，**非 Owner 政策**。Free／有效 Remediation 的零 EMVO、同一 `claimed[tokenId]`、F/R/P、snapshot/root 權限、price freeze、recipient 改向、Final Genesis code 都 `NOT_RUN`。ERC-20 [標準][E20]只定介面，樣本與 mock PASS 不等於 EMVO 實例 PASS。[PROBE]

**付款設計需再驗收的細節。** 正常使用者必須事先授權正確 Token 與正確 spender；mint 函式核對開放狀態、數量、價格、Paid 容量和固定收款地址，然後以可處理 false／no-return 的方式拉取精確成本，再鑄造相同數量 NFT。任一步 revert 應連同本次付款、鑄造及計數一起回滾；先前獨立完成的 approve 與已花 gas 不會因此退還。收款地址不應由訪客提交的任意字串決定，但能否更改、誰能改及如何公告，仍待 Owner 決策。若付款人就是收款地址，一般「payer 減少／recipient 增加」的餘額斷言失效，應先定產品規則；不能從 probe 的拒絕自動沿用。成功付款不使 Token 總供應下降，不產生 NFT 換回 EMVO 的本金權利。[S04][S05][PROBE]

真實 Gate G 還需要 Free 與有效 Remediation 共用 `claimed[tokenId]`、驗證 IMD NFT 當前持有人、鏈及 collection 綁定；F、R、P 三種累計計數必須分開，NFT 被 burn 不能重開名額。若原資格快照漏列而 tokenId 仍可按凍結的規則及窗口證明符合，補救可以修正名單，但更新 root 的批准者、證據 hash、公告與剩餘 R 容量都要可追溯。這些測項尚未因局部 Paid probe 的通過而完成。[HIST][S02]

## 最小修正、關卡與待取證

只需對有效規格／將來 Q 清單作局部修正：把 Paid `BURN_NOT_TREASURY`、`BURN_PER_MINT` 與 burn 不變量改成 `PAYMENT_TO_PAYING_WALLET`、待定 `MINT_PRICE_EMVO`、精確 EMVO 收款與同筆 Mint；Free／Remediation 保持零收費及原資格，付款與池費及 4% 配額分帳；把 88/10/2 標為歷史 UI、明示 86/10/4；L 刪除 burn 能力前提但保留付款、權限、費用、Quote 驗證。G 須測原規則漏列的有效 tokenId、current owner、共用 claimed、累計供應、退款／callback，並決定 self-payment 與 recipient 可變性。這是修正清單，未改母規格。[HIST][S04][S05]

**付款與 Quote 的不同效力。** 本次免費 Check 沒有保留價格、建立訂單或接受 Owner 的金融同意。公開 capabilities 只列 `launch.open` 當下單位請求費：主網 IMD、原子量 `500000000000000000`、18 decimals、`payTo=0x4e0fa57bde726079356537e2f34d671e9f41adbc`、TTL 600 秒；這個 `payTo` 是 IMD 服務收款人，絕不可填成 EMVO 4% 地址或 Genesis 收款地址。真正 Quote 還須綁 action、原輸入雜湊、policy version、issued/expires 時間及具體付款條款；付款前逐欄對照 Owner 批准的版本、token／網路／金額／spender／nonce／deadline、簽章 domain 與收款位址。若目標輸入或重要權限變更，應重新提交給 Owner 判斷；若只是無關的 catalog 項目更新，不能武斷聲稱仍有效的 pinned Quote 已改。此次沒有建立 Quote，因此上述都是**驗收清單而非已核對結果**。[CAP][API][DOC]

**重試與 gas 的責任邊界。** 文件描述同一 `requestKey` 加同一 input 可重取原 Quote，而改 input 用同 key 會衝突；訂單狀態可讀，付款與 admission 狀態分離。因 UI 超時而再次送出前，操作人應先查原 order、付款交易和是否已產生 launch，避免建立第二筆付費工作或重複發行。文件所說「server wallet pays gas」只涵蓋該 x402 收款流程，並非替 Owner 未來的 ERC20 授權、Genesis Mint、主動 claim 或 token 交易付 gas 的保證。`gasCeilingWei` 是 policy 欄位，不能當已實付金額或總成本；服務部署 gas 由誰出、失敗交易的費用及任何額外服務費仍須 IMD 的具體條款或 Quote 證明。不同資產餘額及未到帳 fee 應分列，不能以預期 IMD 池費抵銷已承諾的付款。[DOC][CAP][POL]

**各 Gate 的證據不能互相借用。** R 只說這份資料包完整且問題可研究；Q 只說有不付款的欄位草案；L 需要足以讓 Owner 審核的一筆實際訂單及可接受的合約權限／費用模型。即使 L 將來獲 Owner 獨立批准，V 仍要核對真正部署位址、代碼雜湊、完整 PoolKey／PoolId、配額事件與第一筆實收，不能把 sample 884 地址寫進 EMVO manifest。G 又需要最終 Genesis source、價格／資格／容量、完整測試與單獨批准；本報告沒有供應最終合約。這樣區分也避免把「同 Factory 觀察」當作同版／同路線證明，或把 TEAM 的 receipt 計成外部多席位審查。[S01][S05][HIST]

目前最值得先完成的免費工作是製作一張由 IMD 可逐欄答覆的對照表：輸入欄、Check 判定、實際選定 policy、Factory 參數、部署事件、每個接收地址與後續權限各占一欄，沒有資料的欄位保留空值。這能檢查「Owner 意圖」是否一路傳到部署，而不用先支付發幣費或試做交易。若官方只提供文件說法而不提供足以核對的 source 或同版交易，就應明示這是商業／技術風險供 Owner 決定，不能把缺證據寫成已證不安全，更不能因無法完成某項鏈上實測而把已取得的免費 Check、樣本 runtime 和局部 Getter 一併忽略。反過來，這些局部材料也不能成為建議直接付款的理由。最終若服務生成的合約或 policy 與預審模板不同，仍應逐項比對，留下差異、責任人與可回溯時間點。[S01][S05][DOC]

報告中的數量是以官方標準供應作條件計算；鏈上沒有本案的 allocation receipt。報告中的錢包是指定用途地址，不是經過挑戰簽名的控制證明。報告中的測試是隔離執行結果，不是對將來發行交易的保證。三種證據各自要在正確階段補齊，任何一種都不能由另一種代替。[S05][CHK][TEST]

| Gate | 本輪判定 |
|---|---|
| **R** | **READY for bounded review**：必讀輸入完整，hash 全符；不是 full-spec audit。 |
| **Q** | **FIELD DRAFT ONLY**：可備上述非執行欄；免費 Check 不能替代 effective deployment plan／exact Quote，kind v18 與今日 fee 路徑仍需 IMD 回答。 |
| **L** | **NOT AUTHORIZED / EVIDENCE INCOMPLETE**：無 exact Quote、無 Owner 對實際費用資產／權限的確認，未證明付款人控制及部署收款人。Reviewer 無權批准。 |
| **V** | **NOT_RUN / INSTANCE NOT SUPPLIED**：未收到 EMVO address／deployment receipt；不能因此斷言鏈上絕無同名幣。 |
| **G** | **NOT_READY / Final Genesis NOT_SUPPLIED**：局部 probe 通過不覆蓋資格、容量及正式合約。 |

**D／I／H：NOT_REVIEWED_THIS_ROUND**，延續 R1 歷史限制，不升格通過。可免費準備欄位對帳與 source 清單；Owner 需提供可公開驗證的實際付款地址控制方式（不交私鑰／簽名）、對官方權限及可能混幣的明確立場，Genesis 價格／資格／F/R/P 則留 Gate G。向 IMD 精確請求：① chain1 `evm_project` 選用哪個 policy version、v18 feeTiers 與 12500 的關係及 default→8600 override 的 factory 計算；② 同版 Factory、LaunchFees、Hook、Proxy/implementation/admin、LP position、Merkle distributor 的 source commit、verified runtime、selector／角色／setter 與可撤流動性範圍；③ IMD/標準 Token 買賣各一筆可比交易及 claim trace、fee asset／轉換／rounding／recipient 變更／trigger／gas；④ quote 的 effective input、`inputHash`、`policyVersion`、expiry、付款欄及額外部署 gas 由誰支付。得到後仍須 Owner 對**那一筆** exact Quote 另行決定。[DOC][CAP][POL]

這些提問應要求 IMD 指明適用的鏈、合約位址、部署區塊與雜湊、source commit、編譯器和測試或交易編號；回答「目前官方標準」而無版本錨點，無法判定它是否覆蓋本案。若某項源碼不可公開，至少需可核對的 verified bytecode、ABI、唯讀狀態及已發生交易，並明列仍不能推斷的管理能力。Owner 的回答可以改變其願意承擔的風險，卻不能把缺失的技術證據改寫為測試通過。[S01][RPC]

未做任何 Quote／request submission、簽名、付款、approve、swap、fee claim、主網廣播、部署、網站、付費 child 或排程。此報告由一位 Reviewer 產出；TEAM 資料不能算獨立 Reviewer。下列附錄記錄可核對的來源與錯誤；hash 只證明取回 bytes，非行為認證。

## 附錄 A｜INPUTS_READ（附錄不計正文長度）

釘選 commit `c2b7b49515a0bce41f05743f7221c778434cd3b2`；全部以 HTTPS raw GET 存 `/tmp`，用 Python SHA-256 對原始 bytes 計算，UTF-8 全文讀取，無截斷。manifest 2,385 bytes，實算及預期同為 `12f3ca6bc675f578fe33d7926f6d737c07abcbde271cda2501002b9566835a33`。[manifest][MAN]

| 必讀檔／URL | 實收 bytes | 實算 SHA-256＝manifest | 閱讀覆蓋 |
|---|---:|---|---|
| [01 Brief][S01] | 24,612 | `46dd3126eb1cc1add1ecf887f69d44b59f105a4840e8590be9854fd3d6c0db89` | 全文 |
| [02 Scope][S02] | 12,808 | `69694d0d171725b76744b24e81028f074bd9aad18ffbfe07e0b130586a85bea1` | 全文 |
| [03 R1][S03] | 37,365 | `e399fdfb22e512448e855ca9aa2f2ca77536e4c95ecf6f600d220ec2e162937b` | 全文 |
| [04 決策][S04] | 7,331 | `31f962d92c450c91c37e7a7cdceb73ae24cb0d65f4946daeba2fcd3d69760355` | 全文 |
| [05 最新][S05] | 7,573 | `8cf8bfe6c1370a1dc6d305b147d6ab9885d9bc2037d01e431b609e5ebf0caf60` | 全文 |

[證據清單][INV] 10,297 bytes、SHA-256 `858f96880426b8ce8a83cabc9f28c5bd34005d87970072aff14dd410a976fcc6`；所列 48 個 evidence/reproduction 檔逐一 GET，48/48 bytes 與 SHA-256 相符。歷史規格只針對 §3–16、§51–59、§60–63、§71.2–71.3 閱讀，raw @ `902075d1dfb772738a074f06f56f7aeea9240fd8` 148,119 bytes、實算 `ba57f63ef3d7cc302b8c4b354d242438baf79d9f57aa9d9a37d97e20f3dd5847`；未宣稱全文重新審計。[HIST]

## 附錄 B｜ACQUISITION_LOG 與獨立測試（附錄不計正文長度）

| 問題／讀取 URL 或方法 | UTC、狀態、bytes／SHA-256 或 block | 支持範圍／限制 |
|---|---|---|
| [官方 Docs][DOC]／[Launch UI][UI] | 10:42:04，HTTP200；484189／`df88e767bd682c01d1615f456dbcae21d80a4244c7a81bc6b9b5fa636489fdfe`、41502／`d9ed865ad2c420d148f1610f2239f5b51395fe466c6bcb8ef89a2ab71165595f` | 當時文案；UI 仍寫 88/10/2；非合約行為。 |
| [capabilities][CAP]／[policies][POL]／[version][VER]／[OpenAPI][API] | 10:42:04，均 HTTP200；4256／`eaef51c4fa76119c48e31d71972e34b9fd590bdc8714025fc37f6899bd310e70`、29362／`7c86eb577e027dee867419f75b04952d672db7b4c28ba3ab40d4dad4449eed25`、195／`9b2c127532d3d47beac7bf38e3d325b0aca7d9911d8355fc793ad558cbbad41b`、23132／`be142840c010710cb2a5b9e5c73e71d8e79ec4054c15661699d60bfa627be96a` | kind、公開條款與介面快照；無 Quote。 |
| [免費 Check request][CHQR]／[response][CHK]／[receipt][CHKC] | TEAM 09:56:26，POST `/requests/check` HTTP200；1307／`5393917e474d7f055d7c2dceed972b3064addf9293ddc3889ebd7f38160ef2c2`、2798／`80404d66d65680f66b26f6119d5fbe2b6e7e5741b318b6bb2d4e3000e3e17650` | 本輪未重送；只證當時該輸入的格式／描述可接受，沒有價格鎖定。 |
| [QOBS source][TOK]／[ABI][ABI]／[Blockscout token][BCT] | TEAM 08:46–08:48；372／`24bc1e23…19bc`、5715／`9578fcb4…8542`、8853／`2160e020…12c7e`；本輪 10:43:24 再取 Blockscout HTTP200 同 hash | source commit `53c8e396dfaf7add0d1d90dd2ea19c52206feea3`；runtime 相同，但未獨立重編官方 compiler。 |
| [launch884 tx][DEP]／[raw logs][DLOG]／[只讀 RPC receipt][RPC] | TEAM 08:48–08:50；tx block 26139046、hash `0xc088d2c99dee568e7f1fcf28585a409547b75747abcee47b9ff08e81cd5763c4`；read block 26139425／本輪 [block][BLK] hash `0x03089d7bd5c9532e08ae2f35b18ac236fa9d1337bb107696d4b8f19786ae06d9` | QOBS 樣本；本輪 `ethereum-rpc.publicnode.com` POST `eth_getBlockByNumber`／`eth_getCode` 得 HTTP403，改由 Blockscout GET；部分 TEAM getter 列只有 block number，不能反填每列 block hash。 |
| [launch737 claim logs][FEE]／[decoded summary][DEC] | TEAM 08:48；claim block 26135240／`0x14d53974406fd47f08bb8206312e7375be957b704250b683550cb8592668ff29`；本輪 10:43:24 再取 logs HTTP200、16401／`c3d3f023…f5fc` | `custom_token` 一例，非 EMVO 標準池。 |
| [TEAM fixture][TEAMF]／[TEAM runtime][TEAMR]、[repacked fixture][REPF]／[repacked runtime][REPR] | 原測 10／4 PASS；公開 receipt 的 SHA-256／脫敏限制見[清單][INV] | TEAM 自述，不算本輪獨立結果；原路徑被移除不等於重新執行。 |
| 本輪本機測試 `node --test --test-concurrency=1 tests/treasury-payment.test.mjs`／`node evidence/local-payment-runtime-test.mjs` | 10:44 左右，exit0、10/10 TAP，34.09秒；runtime exit0、4/4 PASS；主套件 Node24／solc0.8.30／OZ5.4／ethers6.15／Ganache7.9.2 | 從[測試 source][TEST]、[probe][PROBE]及[runtime script][RUNTIME]下載後在 `/tmp` 運行；synthetic、無鏈上廣播。 |

### 來源連結

[MAN]: https://raw.githubusercontent.com/tungweb3/emvo-review/c2b7b49515a0bce41f05743f7221c778434cd3b2/EMVO_R2_INPUT_MANIFEST.json
[S01]: https://raw.githubusercontent.com/tungweb3/emvo-review/c2b7b49515a0bce41f05743f7221c778434cd3b2/EMVO_R2_01_Token_Report_Brief_v1.1_2026-10-07.md
[S02]: https://raw.githubusercontent.com/tungweb3/emvo-review/c2b7b49515a0bce41f05743f7221c778434cd3b2/EMVO_R2_02_Active_Scope_and_Finding_Map_v1.1_2026-10-07.md
[S03]: https://raw.githubusercontent.com/tungweb3/emvo-review/c2b7b49515a0bce41f05743f7221c778434cd3b2/EMVO_R2_03_First_Report_UNCHANGED_2026-10-07.md
[S04]: https://raw.githubusercontent.com/tungweb3/emvo-review/c2b7b49515a0bce41f05743f7221c778434cd3b2/EMVO_R2_04_PaidMint_Decision_UNCHANGED_2026-10-07.md
[S05]: https://raw.githubusercontent.com/tungweb3/emvo-review/c2b7b49515a0bce41f05743f7221c778434cd3b2/EMVO_R2_05_Latest_Owner_Decisions_and_Evidence_v1.1_2026-10-07.md
[INV]: https://raw.githubusercontent.com/tungweb3/emvo-review/c2b7b49515a0bce41f05743f7221c778434cd3b2/EMVO_R2_EVIDENCE_MANIFEST.json
[HIST]: https://raw.githubusercontent.com/tungweb3/emvo-review/902075d1dfb772738a074f06f56f7aeea9240fd8/IMD_Ember_EmberEvo_v3.3_Crypto_Research_Genesis_Burn_2026-10-07.md
[DOC]: https://imd.fun/docs/
[UI]: https://explorer.imd.fun/launch
[CAP]: https://api.imd.fun/requests/capabilities
[POL]: https://api.imd.fun/launch/policies
[VER]: https://api.imd.fun/version
[API]: https://api.imd.fun/openapi.json
[CHQR]: https://raw.githubusercontent.com/tungweb3/emvo-review/c2b7b49515a0bce41f05743f7221c778434cd3b2/evidence/allocation4pct/check-standard-wallet4pct.request.json
[CHK]: https://raw.githubusercontent.com/tungweb3/emvo-review/c2b7b49515a0bce41f05743f7221c778434cd3b2/evidence/allocation4pct/check-standard-wallet4pct.response.json
[CHKC]: https://raw.githubusercontent.com/tungweb3/emvo-review/c2b7b49515a0bce41f05743f7221c778434cd3b2/evidence/allocation4pct/check-standard-wallet4pct.receipt.json
[TOK]: https://raw.githubusercontent.com/identity-md-launches/launch-884-workflow-contract-stage-context/53c8e396dfaf7add0d1d90dd2ea19c52206feea3/src/LaunchToken.sol
[ABI]: https://raw.githubusercontent.com/tungweb3/emvo-review/c2b7b49515a0bce41f05743f7221c778434cd3b2/evidence/public-observations/LaunchToken.abi.json
[BCT]: https://eth.blockscout.com/api/v2/smart-contracts/0xad455ee2800b314588b5178df0dcbbc5dad7e1c7
[DEP]: https://eth.blockscout.com/api/v2/transactions/0x89218c12e6d9833be66ed9672f6501a5e08e6829ebb6567cb1cf63ea3d348f2b
[DLOG]: https://raw.githubusercontent.com/tungweb3/emvo-review/c2b7b49515a0bce41f05743f7221c778434cd3b2/evidence/public-observations/deployment884-logs.json
[RPC]: https://raw.githubusercontent.com/tungweb3/emvo-review/c2b7b49515a0bce41f05743f7221c778434cd3b2/evidence/public-observations/rpc-result.json
[BLK]: https://eth.blockscout.com/api/v2/blocks/26139425
[FEE]: https://eth.blockscout.com/api/v2/transactions/0xd751270d5e5a49352c5151065f41e0d29d37de40b73f5c089f9002aa8c4e7259/logs
[DEC]: https://raw.githubusercontent.com/tungweb3/emvo-review/c2b7b49515a0bce41f05743f7221c778434cd3b2/evidence/public-observations/decoded-evidence.json
[PLAN]: https://raw.githubusercontent.com/tungweb3/emvo-review/c2b7b49515a0bce41f05743f7221c778434cd3b2/evidence/public-observations/launch.json
[TEAMF]: https://raw.githubusercontent.com/tungweb3/emvo-review/c2b7b49515a0bce41f05743f7221c778434cd3b2/evidence/team-measurements/treasury-payment-test.public-receipt.json
[TEAMR]: https://raw.githubusercontent.com/tungweb3/emvo-review/c2b7b49515a0bce41f05743f7221c778434cd3b2/evidence/team-measurements/local-payment-runtime-test.public-receipt.json
[REPF]: https://raw.githubusercontent.com/tungweb3/emvo-review/c2b7b49515a0bce41f05743f7221c778434cd3b2/evidence/team-measurements/repacked-fixture.receipt.json
[REPR]: https://raw.githubusercontent.com/tungweb3/emvo-review/c2b7b49515a0bce41f05743f7221c778434cd3b2/evidence/team-measurements/repacked-runtime.public-receipt.json
[TEST]: https://raw.githubusercontent.com/tungweb3/emvo-review/c2b7b49515a0bce41f05743f7221c778434cd3b2/reproduction/tests/treasury-payment.test.mjs
[PROBE]: https://raw.githubusercontent.com/tungweb3/emvo-review/c2b7b49515a0bce41f05743f7221c778434cd3b2/reproduction/contracts/test/GenesisTreasuryPaymentProbe.sol
[RUNTIME]: https://raw.githubusercontent.com/tungweb3/emvo-review/c2b7b49515a0bce41f05743f7221c778434cd3b2/reproduction/evidence/local-payment-runtime-test.mjs
[E20]: https://eips.ethereum.org/EIPS/eip-20
