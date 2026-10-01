# IMD Ember World：audit 8c3aea2e 修正後有限重測

日期：2026-10-01 UTC。對象限 World 的 wallet connect、SIWE、session、logout／logout-all、limits、ownership、My home、move、Enter your home、headers、dependencies 與公開資料 shared cache。

## 回答玩家的問題

**本次不能對目前 live 網站給出肯定的使用判定。** 本機指定快照的原 N-1～N-7 重現案例都得到修正後的預期結果；N-5、N-6 的共享資源可用性問題仍只部分改善。另確認一個 Low 的登入競態 R-1：等待 `eth_requestAccounts` 時切換帳號，舊回應仍可覆寫新帳號、要求舊帳號簽名，並在取得該帳號有效簽章後登入。原 N-2 的 late challenge-body 漏洞已修正，但「切換後整個登入流程都不再 prompt／verify」不能無條件成立。

**在已檢查程式與本機案例中，沒有重現 EOA 無有效簽章登入、伺服器端復活 revoked session、無該地址 live session 卻 logout-all 該地址、或由未驗證候選直接取得別人房屋權限。** ERC-1271 仍以合約的回答為準；接受任意簽章的合約與取得真實簽章的 phishing relay 是已揭露殘餘，不能被前句排除。My home、move、Enter 是 session＋ownerOf 支持的本機體驗，不是資產交易授權。

部署對照為 **partial**：成功從公開來源重建指定 Worker hash，但本環境對五個獲准 production GET 全收到 HTTP 403，未取得 live index／JS／InteriorView／CSS 或 session JSON。因此 live wallet-method 重計數、live headers 與四個 live hash **cannot verify**；沒有把團隊舊輸出當成本次觀測。執行中的 Worker、D1 0005、secret、limiter、WAF 也沒有獨立證據。

這是有限重測紀錄，不是背書或認證。測試通過不證明不存在其他缺陷，尤其不涵蓋 withheld frontend 的完整接線、真實瀏覽器／錢包與 Genesis Mint。

## 證據類型、來源與版本

以下 **[重現]** 表示本次親自執行；**[碼讀]** 表示固定 commit 的原始碼檢查；**[推論]** 是由程式／局部測試推導；**[團隊]** 是尚未獨立確認的文件或部署聲明；**[未知]** 表示資料不足。後文的 fixed 都限於列出的情境與本機快照，不自動等於 production 已修正。

先讀 [README.md](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/README.md)，再檢查 SCOPE、SIWE、ROUTES、WALLET_METHODS、DATA_SCHEMA、OWNERSHIP_AND_HOMES、DEPLOYMENT_MATCH、DEPENDENCIES、TESTS/README、AUDIT_REMEDIATION_STATUS 與 MINT_BOUNDARY 的相關聲明及其程式／測試。原情境以 [audit 8c3aea2e 的 AUDIT.md](https://github.com/Identity-md/research/blob/main/jobs/8c3aea2e-26bc-4bff-bf5d-52d10f79ec9b/files/AUDIT.md) 為準；該報告的 N-1～N-6 為 Low，N-7 為 Info。

| 項目 | 本次確認或限制 |
|---|---|
| 公開 review repo | **[重現]** `8cad017fad58bac89d88fa72d530d3c56160009b`；下載的是這個 SHA 的 codeload archive，不以 branch 作為測試輸入 |
| Parent／提交數 | **[重現]** GitHub commits API 回報唯一 parent `ae1d41a30363ad04711083465501680469400d2f`；compare API `total_commits: 1`。依據：[固定 commit](https://github.com/tungweb3/imd-ember-world-review/commit/8cad017fad58bac89d88fa72d530d3c56160009b)、[compare](https://github.com/tungweb3/imd-ember-world-review/compare/ae1d41a30363ad04711083465501680469400d2f...8cad017fad58bac89d88fa72d530d3c56160009b) |
| Archive 完整性 | **[重現]** `SHA256SUMS` 的 115 個項目，0 mismatch。這是快照內部完整性，不是遠端部署認證 |
| Worker version／private source | **[團隊]** `imd-world`／`bbf24001-7eec-4f93-b312-a22e299ab275`，由 `2e4e830b367f651e3c880587c1a4b465d1bfcd91` 部署 |
| source/ 的來源 | **[團隊]** `f4272c513e2052fb0bea6d2e8512180256a60919`；相對部署來源只差兩份 docs、一份 test，另加一頁 evidence。沒有 private history，不能完整核實這個差異敘述 |
| Worker bundle | **[重現]** 280,605 bytes；SHA-256 `018df7b35117bf612cd9311a800de75964b07f9d74f2c2f1ae545b26894cf62c`，等於題目與 `manifests/deploy-record-SHA256SUMS.txt` |
| Node／npm | **[重現]** v24.21.0／11.19.0（團隊為 v24.19.0／11.17.0）；lockfile 未改。此環境差異未阻止 Worker byte-for-byte 重建 |
| D1 | **[重現]** 本機 `node:sqlite` 跑真 migrations 0001–0005，另測只到 0004；**[團隊]** production 0005 已在 deploy 前套用 |
| Ownership 合約 | **[碼讀]** Ethereum mainnet `0x0000ec93127baa929e58e97dd0095a2bfb38ec1d`；`server/ownership.ts:54-69` 用 Multicall3 的 ownerOf。鏈、索引、limiter 全以 fixture 代替，未查真錢包 |

未變更 target，也沒有 production POST、登入、掃描、fuzzing 或 exploit。所有簽章只由記憶體內隨機合成 key 產生，fixture 的 RPC 不出網。測試副本與 npm dependencies 在 repository 外的 `/tmp/imd-retest-src`；repository 的 `.git/`、`.github/`、`.env`、`node_modules/` 未修改。交付的 Markdown 不依賴任何執行期套件。

## N-1～N-7 判定

表中的位置均指上述固定 commit 的 `source/`，不是舊 audit 行號。測試不是只看名稱：已檢查相應 assertion、SQLite adapter 與 fixture 的作用範圍，並執行全部 43 項 N 測試。

| Finding／原嚴重度 | 團隊聲明 | 本次 verdict | 程式與本機情境證據 | 殘餘／限制 |
|---|---|---|---|---|
| N-1 Low | sessionReads 保留最新讀取；登入等 session 讀取 | **fixed（原情境）** | **[碼讀]** [src/world/auth.ts:187](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/src/world/auth.ts#L187)：gen＋sessionReads 在 fetch 後、json 後、catch 都檢查；不同 session／signed-out 增 homeGen，登入也作廢舊 home。**[重現]** `wallet-client.test.mjs:1010-1148`：R1 signed-out body 晚於 R2 signed-in，仍 owner／eligible=1；反向不復活；late 429／503／斷線、換帳號、logout 與舊 house read 都不覆寫新狀態；signIn 等新的 R2，無額外 signature | 最新讀取自己失敗仍 sessionKnown=false；持續發起讀取可令登入等待。這是文件已述的可用性取捨；並非伺服器 session 續期 |
| N-2 Low | challenge body 後核對 flow／wallet／account；取消後不 prompt／verify | **partly：原 audit 情境 fixed，較廣聲明有 R-1 例外** | **[碼讀]** [src/world/auth.ts:268](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/src/world/auth.ts#L268)、`:280-286`、teardown `:163`。**[重現]** `wallet-client.test.mjs:1150-1252` 與獨立 control：challenge body 被延遲，切換帳號／provider、logout、teardown 後 0 personal_sign、0 verify；已開 prompt 的 logout 後回覆也丟棄。但延遲 `eth_requestAccounts` 的 R-1 為 1 prompt＋1 verify | 網頁無法關閉已開的錢包 prompt。R-1 發生在 phase 尚為 idle 的連線 await，並非原 audit 的 challenge-body await；見下節，仍需有效簽章 |
| N-3 Low | cap 排序與計入使用相同 counts，包括 owner-bound 24 h sightings | **fixed（原情境）** | **[碼讀]** [server/ownership.ts:142](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/server/ownership.ts#L142)、`:228-245`、`:264-273`：registered 且 online 或 seen≥now−24h 優先，D1 查詢含 owner。**[重現]** `ownership.test.mjs:429-477`：0..254＋#1000 原有 256 候選；加入 #255 後仍保留一小時前見到的 #1000，256 個結果、eligible=1、size=s、partial；24h 恰好邊界、超時、別的 owner、sold token 與 persisted cut 均驗證 | >256 可計入候選仍只查 256；索引最多 5 頁。讀 sightings 失敗／無 DB 時排名退回 roster；這不保證故障時仍發現 #1000。真正 ownerOf 不符仍排除 |
| N-4 Low | pool／lane 分開記錄，先前 pool 不吃 retry lane | **fixed（0005 本機；同網段 residual as stated）** | **[碼讀]** [server/auth.ts:197](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/server/auth.ts#L197)、`:212-216`、`:492-497`；[migrations/0005_lanes_and_subnets.sql:11](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/migrations/0005_lanes_and_subnets.sql#L11)。**[重現]** `auth.test.mjs:599-662`：owner bad→外網 bad→owner good＝401,401,200；owner good→外網 bad→同 /24 第二裝置 good＝200,401,200；資料列 called_via＝pool,pool,lane；racing claim 只一個 lane | 同 /24 的兩次垃圾，或先佔 lane，仍可拒絕 owner；IPv6 同 /64 或同 /48 其他兩個 /64 類似。NULL called_via 按舊 lane 計。尚未套 0005 的舊情境仍 429，不能以 200 session GET 證明已修正 |
| N-5 Low | NET6_SCALE=2；/48 兩份，/64 一份 ERC-1271 share | **partly／residual as stated** | **[碼讀]** [worker/app.ts:62](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/worker/app.ts#L62)、`:74-85`、`:117-119`；[server/auth.ts:158](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/server/auth.ts#L158)、`:190-216`、`:477-487`。**[重現]** 四個不同 /64 的智慧錢包＝200,200,200,200；同 /64 只能 3 contract checks／10 code claims，從其他 IP verify 不搬移份額；換 host bits 無效；輪換 /64 仍在 /48 的 6／20／60 上限，IPv4 仍 3／10／30。`auth.test.mjs:664-763`、`worker.test.mjs:240` | 兩個以上 /64 可花掉共享 /48 的合約／code 額度；challenge 的 /64 限制是 per-colo，跨 colo 仍可吃 /48 總額。/64＝subscriber 是配置假設，不是已驗證的 ISP 分配事實；前 0005 challenge sub=NULL 只受 /48 總額 |
| N-6 Low | 主 index 被拒且無 counting seat 時有 discovery lane | **partly／residual as stated** | **[碼讀]** [server/auth.ts:234](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/server/auth.ts#L234)、`:617-625`；[server/ownership.ts:278](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/server/ownership.ts#L278)。先 D1 INDEX_LANE，再扣 chain:index:lane，未放行不讀；ownerOf 仍證明。**[重現]** `ownership.test.mjs:487-578`：原 audit 三分鐘、每分鐘單 IP 20 個合成 EOA 佔主池，新買家首分鐘仍找到 #361／Enter=ok，其後已保存候選仍 owner（limited）；20 外網耗盡 lane 的 residual、race、一網一 lane、全站 60/6s、第 61 個拒絕、下一窗恢復、上游錯誤不拿 lane 均通過 | 同網先取 lane、同 colo 20 個其他網段、或 global lane ceiling 仍拒絕；已有一席計入而新買其他席不拿 lane。缺 0005 無 lane。每個 index operation 可有 5 次 HTTP GET，見成本節；不是全站 Alchemy 帳戶額度保證 |
| N-7 Info | expired／revoked／signed-out 分開；session route 只有真過期加 expired:true | **fixed（原情境），文字 residual as stated** | **[碼讀]** [server/auth.ts:410](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/server/auth.ts#L410)、`:526-534`；[src/world/auth.ts:200](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/src/world/auth.ts#L200)、`:223-227`、`:307`；[src/world/walletView.ts:56](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/src/world/walletView.ts#L56)、WalletPanel.tsx:104-105。**[重現]** 真 handler 兩 browser logout-all 後第一頁 refreshHome：session=null、expired=false、ended=revoked；真 expiresAt、clock skew、local timer＝expired；本頁 logout＝signed-out；React server render 三種文案測試通過。forged／missing／revoked cookie 無 expired flag | cookie 已由瀏覽器刪掉且頁面時鐘落後，可能只顯示「已失效」。AUTH_REQUIRED 不辨識撤銷原因；不是「必定另一裝置登出」。無 browser E2E |

**0004 fallback 的實際結果：** `auth.test.mjs:732` 使用真 0001–0004 DB，帶 sub 的 INSERT 失敗後匹配 `SCHEMA_0004`、batch rollback，再用舊 SQL；IPv6 第 31 個 challenge＝429，N-4 retry＝429，四個 /64 登入＝200,200,200,429。加 0005 後第四個可登入。`ownership.test.mjs:571` 確認缺 index_lanes 回 limited 而非 503；`presence.test.mjs:68,100` 確認 migration additive 與 cron 兼容。這些結果支持 fallback 聲明，也說明不能靠普通成功回應驗證 production migration。

## 新發現：confirmed World issues

### R-1 — Low：連線帳號舊回應覆寫 accountsChanged，舊流程仍 prompt／verify

**證據：[重現＋碼讀]。** 位置 [src/world/auth.ts:254](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/src/world/auth.ts#L254)（`:256-258` await eth_requestAccounts，回來只檢查 gen，再 set account）、[src/world/auth.ts:314](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/src/world/auth.ts#L314)（`:317-318` 無 session 且 phase=idle 的 accountChanged 不增加 gen）。事件監聽會把 provider 的 accountsChanged 交給此方法（`:172`）。

前提：尚無 session、頁面 account=null，玩家點登入；`eth_requestAccounts` 的舊結果 A 延遲，在它抵達前 provider 發出 `accountsChanged([B])`。這是注入 provider 的時序模型；**未在真實 MetaMask 或其他 wallet 重現此事件順序**，也不需要假設攻擊者知道 A 私鑰。

實際流程：

1. 延遲 `eth_requestAccounts` promise；AuthClient 已在 signIn，但 phase 仍 idle。
2. 呼叫事件 handler `accountChanged(B)`，確認 state.account=B。
3. 放行舊 promise 的 `[A]`；gen 沒變，state.account 被設回 A。
4. 真 Worker 對 A 發出正常 SIWE challenge。N-2 新檢查看到 state.account=A，放行 personal_sign(A)。
5. fixture 以記憶體內 A key 簽這份 SIWE；真 verify=200、sessionForA=true，證明流程可送 verify。若玩家拒簽或 wallet 不允許 A 簽名，則不會有此 session。

本次輸出（沒有地址、key、signature 或 cookie）：

```json
{"prompts":1,"promptForOldA":true,"verify":1,"accountRevertedToA":true,"sessionForA":true,"status":"signedInNoHouse"}
```

預期應保留最新的帳號事件，或中止這次點擊，不能由舊連線結果把帳號倒退到 A。影響是錯帳號提示／登入與 UI 狀態混淆，**不是無簽章冒用、任意 payload 簽名或資產轉移**。相同控制測試在 challenge body 階段換 B 得到 prompts=0、verify=0，所以不推翻原 N-2 的具體修補。

這是本輪新確認的遺留 gap，不宣稱由本 commit 引入：parent `ae1d41a` 的 `auth.ts:228` 與 `:287` 已有同樣的 await／idle accountChanged 模式。A-3 原 house-response 修正仍有效，但不能概括為所有 wallet response 都會作廢。

建議：為 account read／connect 回應加入帳號事件序號或等效版本檢查，在 await 返回後核對 provider、最新帳號事件與流程；新增「idle connect pending→accountsChanged(B)→舊 A response」測試，並以實際支援的 wallet 驗證事件語意。此任務只交付重測，沒有更改 target code。

獨立重現程式附於 [reviewer-probe.mjs](reviewer-probe.mjs)；複製到指定 source 副本的 `tests/reviewer-probe.mjs` 後 `node tests/reviewer-probe.mjs`。它使用未修改 AuthClient、真 Worker、真 SQLite migrations、合成 keys；沒有 production 流量。控制案例與 pagination 案例也在同檔。

## Shared-boundary issues（既有，非本輪新漏洞）

- **F-1／S-1，Medium shared boundary：residual as stated。** [src/world/siwe.ts:16](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/src/world/siwe.ts#L16) 的逐行檢查及 [server/auth.ts:473](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/server/auth.ts#L473) 的 stored-message 檢查確實存在，相關測試通過。然而持有 flow cookie 的 server-side relay 若取得受害者對真 challenge 的真簽章，仍可 verify；本次沒有以 phishing 網頁或真 wallet 測試。Origin 檢查不是遠端腳本來源的身分證明；頁面檢查也不約束惡意 origin 的另一套程式。這不等於「不需要簽章」。
- **F-2，Low/Info：residual as stated。** [server/auth.ts:374](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/server/auth.ts#L374) 的 ECDSA first／code gate／exact magic-word ERC-1271 驗證、session 的 CONTRACT/ERC1271 標記均由測試確認；若合約本身接受任意 signature，登入也接受，並可取得該合約 ownerOf 證明的 read-only house view。沒有驗證 production 任一特定 smart wallet。
- **F-8／S-2，Info shared boundary：open。** [server/auth.ts:314](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/server/auth.ts#L314) 的 `__Host-`、Path=/、無 Domain 並不隔離同 origin 的不同頁面；HttpOnly 防止 JS 直接讀 token，不能阻止同源頁面帶 cookie 呼叫 API。未變更的 [docs/security/MINT_BOUNDARY.md:11](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/docs/security/MINT_BOUNDARY.md#L11) 把未來 Mint 的 session reuse 列為問題，未提供解答。

## 先前 A、W、F residual 的交叉檢查

下列本機測試均包含在 212 pass 內；未以團隊「fixed」字樣取代驗證。表中 status 對原 finding 判定，不宣稱超出測試範圍。

| 項目 | 本次判讀與依據 |
|---|---|
| A-1 Medium availability | **partly／residual as stated**。N-4 修正 pool/lane 混計。`auth.test.mjs:512,556,599,638,648` 通過：少數其他網段不擋 owner lane，同網垃圾仍擋；fixture 中 9 個 /24×3 wallets 可耗盡 lane，8 個／24 或 9 個×2 不足；IPv6 測試 5 個 /48、各兩個 /64×3 wallets 可耗盡。不是 edge 吞吐保證 |
| A-2 Low | **fixed 原 kept-index 問題，availability residual 保留**。[server/ownership.ts:164](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/server/ownership.ts#L164) 的 upsert 只覆寫 read_at 不較新的資料，DROP 也受時間限制；讀取地址來自 session；D1 只保存候選，ownerOf 重證。`ownership.test.mjs:242` 與 A-2 多 isolate／late write／sold-seat 測試通過，cron >8 天清除通過；新買 token 若兩來源都未見，或主池與 lane 均拒絕，仍找不到 |
| A-3 Low | **fixed 原 home-read 亂序情境**。auth.ts:214-231 的 gen＋homeGen 覆蓋 body 和 error，`wallet-client.test.mjs` A-3 測試通過。N-1 延伸 session-read 保護通過；R-1 是另一個尚存的 connect-response gap |
| A-4 Low | **fixed 原排序／partial 問題**。N-3 擴充至 24h owner-bound presence；cap 與 pages 截斷仍以 partial 表示，>256 不完整是 residual。`ownership.test.mjs` A-4／N-3、wallet-client A-4 全通過 |
| A-5 Low | **fixed 原舊分鐘計數問題，residual as stated**。[server/auth.ts:424](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/server/auth.ts#L424)、`:453` 在 readJson 後取時，contract 在 code read 後取時（`:491`），consume 再取時（`:510`）；slow-body 測試通過。readJson 無獨立 timeout；per-IP limiter 在 request 開始，不能據此保證無 slow-request 資源成本 |
| A-6 Low | **partly／residual as stated**。address challenge cooldown 已無，surge 只記錄；同網總額仍共享。auth A-6、N-5 通過；IPv4 兩 IP 可吃 30/min，IPv6 /48 60/min，/64 分配限制如 N-5 |
| A-7 Low | **partly／residual as stated**。[server/auth.ts:169](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/server/auth.ts#L169) 的全站 60/6s 中 20 留給過去一分鐘未要求的網段；A-7 測試顯示 20 busy networks 下新網段仍獲 challenge。14 /24（或 7 /48）的 regular-part 阻塞與另約 200 fresh networks/min 的成本是由 SQL 限額推導；本次未將全部組合重演成 production 負載 |
| A-8 Low | **fixed 原文案情境**。walletView 的 incomplete／limited 與 no-seat 分開；React server render 測試確認 refused chain check 不顯示「Checked on chain…no seat」。N-6 fallback 改動未破壞此 assertion |
| W-1 Info | **fixed 本機 expiry gate；remote revoke residual 保留**。statusOf、moveGate、enterAtPress 依當下 clock；expiry timer 與 visible re-read 測試通過。其他裝置 logout-all 仍待此頁下一次 session／home read 才得知；無 push，不可承諾即時清除每個畫面 |
| W-2 Info | **residual／wording as stated**。[server/auth.ts:563](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/server/auth.ts#L563) 的 refusal log 仍含 IP 推導 /24 或 /48 與 colo，surge 含地址前綴；不是完全沒有 IP-derived data。測試確認不寫完整 IP，N-5 新 sub／64 存 DB 不寫 log。本報告未讀 owner logs |
| W-3 Info | **fixed 原分類問題**。[server/auth.ts:394](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/server/auth.ts#L394)、`:405-407`：node error／transport 是 503，revert／EVM halt／wrong magic 是 401，均不建 session；auth 與 client W-3 測試通過 |
| F-1、F-2 | 見 shared-boundary 節；保留 phishing relay 與 permissive ERC-1271 殘餘 |
| F-3 Low availability | **partly／residual as stated**。code claim、no-code cache、contract／network／lane shares 有上限，EOA 正確 ECDSA 不花 RPC；probe 與 F-3／A-1／N-4／N-5 通過。多網段或同網鄰居仍可阻礙 smart-wallet sign-in；已知 smart-wallet pool 與 first-time pool 分開但都非無限 |
| F-4 Low | **fixed 原缺 logout-all 問題**。[server/auth.ts:549](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/server/auth.ts#L549) 只用 live session 的地址撤銷；`auth.test.mjs:223,242,269` 測試 revoked／expired／forged／無 cookie 不能結束別人 session、invalidate 未完成 challenge、其他地址不受影響。Worker limiter 拒絕時 logout-all 200／logout 204；edge WAF 仍可能在前面擋住，未測 production |
| F-5 Low availability | **partly／residual as stated**。challenge／verify 分鍵、fresh-network reserve、global emergency cap 仍在，A-5～A-7 的取捨仍在 |
| F-6 Info | **本次 audit 0，僅此時點與 lock**。package.json／lock 相對 parent 不變；undici=7.29.1 override 及兩個依賴測試通過。npm audit 全部與 omit=dev 都 0，不代表供應鏈或未來 advisory 已排除 |
| F-7 Info | **(a) fixed；(b)–(e) residual as stated，(b) 成本需連同新 lane 解讀**。SIWE 檢查通過；Lax cookie 可隨 cross-site top-level GET 觸發 `/api/me/home?fresh=1`，本次未跑真 browser，此路由沒有 Origin／Fetch-Metadata 拒絕，現在也可能消耗請求者網段的 index lane；CSP 仍允許 inline style；loopback exception 依 request URL；accountsChanged([]) 保留既有 session／owner（F-7e 測試通過）。這不是取消登入競態 R-1 的修正 |
| F-8 Info | **open／residual as stated**，見同源與 Mint 邊界 |

### 授權與 shared cache 的額外檢查

**[重現＋碼讀]** `auth.test.mjs:83,103,120,132,213,223,242,269,299,324` 覆蓋錯 key、改 message fields、Origin、flow cookie、nonce 過期／重送／supersede、並行 verify 只建一 session、logout、logout-all、絕對到期、猜 token。[server/auth.ts:514](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/server/auth.ts#L514) 的 batch 用一次 consume 與唯一 nonce 約束，沒有續期路徑；readSession 對 revoked_at 優先拒絕。

**[碼讀＋重現]** `/api/me/home` 的地址來自 readSession（[server/auth.ts:614](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/server/auth.ts#L614)、`:625`），不從 query 或 connected wallet 取；候選全經 [server/ownership.ts:258](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/server/ownership.ts#L258) ownerOf 篩選。`homeEntry.ts:11-18` 額外比 home.address 與 house.owner；`enterAtPress:30` 在按下時重查。三個 group 5 tests＝3/3 pass。move 只寫 localStorage（[src/world/moves.ts:64](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/src/world/moves.ts#L64)），不寫別人的伺服器房屋；一 wallet 一 house／大小依 counted seats 是題目指定產品規則。轉手仍存在 30s proof cache、頁面輪詢及短暫舊畫面窗口，不能把本機 Enter 視為即時鏈上 access control。withheld WorldApp／geometry／interior 實際接線未能從 live bundle 補查。

**[碼讀＋重現]** parent compare 顯示 gateway.ts／world-api.ts 未變。[worker/app.ts:51](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/worker/app.ts#L51) 用 origin＋固定 shared path＋SHARED_SHAPE＋source 作 cache key；[server/gateway.ts:194](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/server/gateway.ts#L194)、`:212-215` 只由固定上游成功讀取後放入選過的公開資料；`:247-258` 檢查 record version、shape、key、age 與新舊。[server/world-api.ts:48](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/server/world-api.ts#L48) 拒非 GET，未知 shared 路由＝404（`:65`）。worker shared-copy tests 通過。沒有找到讓普通 caller 用 body／query 寫入 shared snapshot 或將 session／Alchemy Authorization 存入 shared copy 的路徑；這不證明上游本身可信，也不涵蓋同 Cloudflare zone 的其他未公開程式。沒有 production cache poisoning 嘗試。

## Keyed reads probe 與可用性上限

**[重現]** 將原 `TESTS/probes/keyed-reads-probe.mjs` 原樣複製到 source 副本 tests/_probe.mjs，執行成功。輸出摘要（只有 fixture，不含 owner logs）：

```text
1) EOA bad verify: 401,409,409,409,409; same nonce right signature:409
   keyed reads=1 eth_getCode; next challenge same EOA bad signature:401, reads=0
1b) contract bad verify:401,409,409; keyed reads=2 (eth_getCode,eth_call)
1c) chain:code refused:429 CHAIN_BUSY; keyed reads=0
2) synthetic EOA sign-in:200; home:200; one getNFTsForOwner; chain:index
3) chain:index refused: home 200, recheck=-, seats=0; keyed reads=1
   keys: chain:index, chain:index:lane (plus API and session home limiter)
4) public wallet assets:200; keyed reads=0
5) missing AUTH_LIMITER production-shaped local request:503 LIMITER_UNAVAILABLE
   loopback:200; missing API_LIMITER world snapshot:503 limiter_unavailable
6) every binding refuses: logout-all=200; logout=204
```

相對上一輪，probe #3 不再是 0 upstream reads：有 lane 時增加一個 index operation，這是修正的刻意成本。N-6 的 local exact limiter／SQLite tests 證明普通主池 20 operations/min/colo，加 lane 20 operations/min/colo；lane 另受 /24 一次、/64 一次、/48 兩次與 global 60/6s 限制。D1 先 claim，主池／lane limiter fail closed。拒絕主池與 lane 後不會無限制繼續索引。

**計量限定：40 不是所有 upstream HTTP／RPC 的總上限。** `indexedNfts`（[server/ownership.ts:74](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/source/server/ownership.ts#L74)）每個 operation 最多 5 頁；本次另以 fixture `endlessPages=true` 實跑一個 lane，結果 **5 次 NFT HTTP GET，recheck=partial**。在理想精確 limiter 模型中，40 個獲准 index operations 的 HTTP 頁面數最多 200；跨 window 完成時間也不能直接當固定分鐘實際流量計算。每次 proof 最多 256 candidates、200/token per Multicall chunk，因此最多 2 RPC；lane fallback 可能先證舊候選，再重建新 proof，單次 home 可再付一輪 proof。已持有席位者可在既有 session/home limits 下重讀 proof，不必每次花 index key。public market floor 又有獨立 TTL／retry 路徑（world-api.ts:33-38），不在此 probe 的六項之內。

結論：**索引／lane 邏輯有界，沒有在本次重現出取消限流的 regression；不能把這些測試說成 Alchemy 帳戶全站用量或 billing plan 不會耗盡。** 真實 Cloudflare limiter 是 per-colo、非本機 exact fixture；多 colo、D1 實際計費、上游 quota、ISP 分配與 WAF 配置均未知。

## Wallet-method inventory：live 未能重計數

五個 production 請求均失敗，所以本節嚴格分兩層。**[重現＋碼讀]** 公開 auth.ts 的字面 method 呼叫各恰好 1：eth_accounts（`:171`）、eth_requestAccounts（`:256`）、personal_sign（`:278`）；後者 payload＝`[hexUtf8(checked SIWE message), account]`，不是 typed data／transaction。只註冊及移除 accountsChanged（`:172`）；WalletRegistry 的 EIP-6963 discovery 是頁面事件，不是額外 wallet RPC。原始碼檢查不等於完整 live frontend inventory。

下表數字全部是 **[團隊]** [WALLET_METHODS.md §3](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/WALLET_METHODS.md#3-正式檔案上的重新計數可自行驗證) 的待驗聲明，**本輪 live count 一律 unknown，不是 0**：

| 字串／呼叫類別 | 團隊 index JS 數 | 團隊 InteriorView 數 | 本輪 live |
|---|---:|---:|---|
| eth_accounts、eth_requestAccounts、personal_sign | 各 1 | 各 0 | unknown |
| `.request(` | 3，稱為上述 RPC | 3，稱為 render `this.request()` | unknown，未能檢查 call sites |
| accountsChanged | 2 | 0 | unknown |
| chainChanged、eth_chainId、switch／add chain | 各 0 | 各 0 | unknown |
| eth_sendTransaction／eth_sendRawTransaction／eth_signTransaction | 各 0 | 各 0 | unknown |
| eth_signTypedData／signTypedData／eth_sign | 各 0 | 各 0 | unknown |
| Permit／Permit2、setApprovalForAll、相關 selectors | 各 0 | 各 0 | unknown |
| approve（case-insensitive） | 2，稱為 UI 文字 | 0 | unknown，不能據數字視為 approve RPC |
| wallet_sendCalls／getCallsStatus／grantPermissions／requestPermissions／watchAsset | 各 0 | 各 0 | unknown |
| session key／委派 | 聲明沒有相關呼叫，未給獨立字串 count | 同左 | unknown |
| EIP-6963 requestProvider／announceProvider | 1／2 | 0／0 | unknown |
| import( | 1，稱為 InteriorView 動態載入 | 0 | unknown |
| WebSocket／EventSource／eval(／new Function／document.cookie／document.write／sendAsync | 各 0 | 各 0 | unknown |

即使能取 bundle，字串計數仍須搭配 call-site 檢查，不能單靠「未見名稱」排除動態組字串。這次未取得兩個實際檔案，沒有聲稱已排除 withheld 程式的交易、approval、batch、typed data、chain switch 或 session-key 呼叫。

## Deployment-match：partial

### Worker 來源重建已對上，遠端執行未對上

**[重現]** 使用 source/ 的獨立副本與鎖定依賴，建立空白 dist/index.html 供 assets path 存在，僅 dry-run；沒有部署。首次執行遇 wrangler 預設 config 路徑不可寫，改 `XDG_CONFIG_HOME=/tmp/imd-wrangler-config` 後成功。移除兩個測試 stubs 後再建一次仍得同 hash。sourcemap 的 16 個專案輸入為：

```text
worker/{index,app}.ts
server/{auth,ownership,presence,gateway,world-api,chain-mock}.ts
src/world/{links,status,model,cadence,market,collections,houseSize,siwe}.ts
```

沒有 households、layout、WorldApp 或 interior；第三方來源為 viem、abitype、@noble/curves、@noble/hashes。這證明公開來源能重現「團隊 manifest 所列 bundle」，**不能直接證明該 bundle 已上傳或正在處理 100% 流量**。[manifest](https://github.com/tungweb3/imd-ember-world-review/blob/8cad017fad58bac89d88fa72d530d3c56160009b/manifests/deploy-record-SHA256SUMS.txt) 本身仍是團隊提供。

### Live 一次性 GET 結果

以下時刻為本機 UTC request start；每次間隔約 3 秒，urllib.request.urlopen，每 URL 一次，無 Cookie、POST、重試、繞過或其他 production 路由。

| URL | 時刻 | 本次回應 | 成功 body／hash／security headers |
|---|---|---|---|
| https://imdember.com/ | 08:41:38.319804 | HTTPError 403 Forbidden | 未取得／未比對 |
| https://imdember.com/assets/index-C1BrxBtd.js | 08:41:41.418805 | HTTPError 403 Forbidden | 未取得／未比對 |
| https://imdember.com/assets/InteriorView-4LZmFcoq.js | 08:41:44.439335 | HTTPError 403 Forbidden | 未取得／未比對 |
| https://imdember.com/assets/index-B1zoY2Mz.css | 08:41:47.459899 | HTTPError 403 Forbidden | 未取得／未比對 |
| https://imdember.com/api/auth/session | 08:41:50.478594 | HTTPError 403 Forbidden | 未取得 JSON／未比對 |

抓取程式只在成功回應才保存 body／headers；遇 HTTPError 記錄 exception。因此沒有可用的 403 headers/body 證據可以判斷阻擋者，**不能斷言是網站 WAF，也不能斷言本站正常回應缺少 security headers**。沒有為了補 header 再發第六個 GET。

待比對的預期值如下，只核對其與 repo manifest／題目一致，**不是本次取得的 live hashes**：

| 檔案 | 預期 SHA-256 | 團隊 bytes | 本次 match |
|---|---|---:|---|
| index.html | `62af24a41f3825ffd8b8c68b8d2032205b58a82cbb92618fed599609163e49c9` | 2,634 | unverified |
| index-C1BrxBtd.js | `b6d39838089b2707778990485570b6069054bdea22298bc2062b41a17f198d3d` | 1,432,648 | unverified |
| InteriorView-4LZmFcoq.js | `5077095b0b0fee5b68ad02328bc5d2304de7822f90ed933f54780c8880041630` | 93,255 | unverified |
| index-B1zoY2Mz.css | `4d1e832e229e0ea91b5af4b907c915489babf94db21f015c8eb72bf1510e0b32` | 57,205 | unverified |
| Worker index.js（本機重建） | `018df7b35117bf612cd9311a800de75964b07f9d74f2c2f1ae545b26894cf62c` | 280,605 | verified 對 manifest；remote unverified |

**[碼讀＋本機 tests]** `public/_headers:18-24` 設定 static CSP 的 `script-src 'self'`、object-src/base-uri none、frame-ancestors none；style-src 仍 unsafe-inline；HSTS 一年含子域、DENY、nosniff、strict-origin-when-cross-origin、camera/microphone/geolocation=()。API_HEADERS（world-api.ts:11-15）為 no-store、CSP default-src none／frame-ancestors none、CORP same-origin、HSTS、nosniff、Referrer-Policy，無 CORS。相關 headers tests 全過。**本次沒有完成上述標頭與 live 回應的比較**。

分項判定：source→manifest Worker **verified**；live 四檔＋headers **unverified**；running Worker／D1／secrets／limiter／WAF **unverified**；整體 **partial**，且比團隊曾成功 fetch 四檔的 partial 少了一層獨立證據。團隊的 `bbf24001`、0005 applied、20 `/api/` requests/10s edge rule、private source diff、真 MetaMask 登入與 861 完整 tests 都仍為團隊端聲明。

## 本機 commands 與輸出紀錄

所有測試僅本機。以下是本次指令及結果摘要，省略毫秒耗時、terminal escape 與合成 refusal log；沒有讀取或附上 owner logs。`R=test/scratch/review` 是固定 SHA archive 解壓目錄；`S=/tmp/imd-retest-src` 是獨立 source 測試 repo。沒有執行正式 deploy。

### 取得與檢查

```sh
curl -fsSL 'https://api.github.com/repos/tungweb3/imd-ember-world-review/commits?per_page=5'
curl -fsSL https://codeload.github.com/tungweb3/imd-ember-world-review/tar.gz/8cad017fad58bac89d88fa72d530d3c56160009b
# tar 解到 test/scratch，排除 .git、.github、.env*、node_modules
curl -fsSL https://raw.githubusercontent.com/Identity-md/research/main/jobs/8c3aea2e-26bc-4bff-bf5d-52d10f79ec9b/files/AUDIT.md
curl -fsSL https://api.github.com/repos/tungweb3/imd-ember-world-review/compare/ae1d41a30363ad04711083465501680469400d2f...8cad017fad58bac89d88fa72d530d3c56160009b
curl -fsSL https://raw.githubusercontent.com/tungweb3/imd-ember-world-review/ae1d41a30363ad04711083465501680469400d2f/source/src/world/auth.ts
# Python hashlib 逐項核對 SHA256SUMS；rg／nl／sed／cat 檢查 docs、code、assertions
```

```text
latest: 8cad017fad58bac89d88fa72d530d3c56160009b
parents: [ae1d41a30363ad04711083465501680469400d2f]
compare total_commits: 1
SHA256SUMS: 115 entries, 0 mismatches
```

GitHub HTML 也以 web 工具讀取 repo 頁與原 audit 頁；沒有用 web 工具對 production 增加請求。上述 production 五次 GET 的完整時刻及錯誤在前表。

### 安裝、測試、重建

```sh
cp -R "$R/source/." "$S/"
git -C "$S" init -q
git -C "$S" add -A
git -C "$S" -c user.name=reviewer -c user.email=reviewer@example.invalid commit -qm snapshot
npm ci --prefix "$S" --no-audit --no-fund
# 首次失敗：npm error EROFS /root/.npm/_cacache/tmp/***；exit 226
npm ci --prefix "$S" --cache /tmp/imd-npm-cache --no-audit --no-fund
# 重跑 exit 0，lock 未修改
cp "$R/TESTS/stubs/households.ts" "$S/src/world/households.ts"
cp "$R/TESTS/stubs/layout.ts" "$S/src/world/layout.ts"
# 下列在 S 執行
npm test
node --test --test-name-pattern='^N-' tests/wallet-client.test.mjs tests/auth.test.mjs tests/ownership.test.mjs tests/presence.test.mjs tests/worker.test.mjs
node --test --test-name-pattern='group 5' tests/home-entry.test.mjs
# 複製原 probe 為 tests/_probe.mjs
node tests/_probe.mjs
npm audit --json --cache /tmp/imd-npm-cache
npm audit --omit=dev --json --cache /tmp/imd-npm-cache
node tests/reviewer-probe.mjs
```

| command／情境 | exit | 本次 output |
|---|---:|---|
| npm test，兩個原 stubs | 1 | tests 216；pass 212；fail 4；與 snapshot 數字一致 |
| N tests | 0 | tests 43；pass 43；fail 0 |
| group 5 | 0 | tests 3；pass 3；fail 0 |
| 原 keyed-reads probe | 0 | 六項結果如前節，#3 lane 有一次 keyed index read |
| npm audit 全部 | 0 | vulnerabilities={}；info/low/moderate/high/critical/total 均 0；dependencies prod=19, dev=141, total=159 |
| npm audit omit=dev | 0 | vulnerabilities={}；所有 severity 及 total 均 0 |
| reviewer-probe 最終版 | 0 | R-1 上述 JSON；original N-2 control prompts=0 verify=0；N-6 pagination 5 GETs，partial |
| npm test，移除兩 stubs | 1 | tests 111；pass 107；fail 4 |
| tsc --noEmit，無 stubs | 2 | 16 errors；缺 withheld modules／virtual:baked-terrain 與連帶 implicit-any |
| wrangler dry-run，修正暫存 config 路徑後 | 0 | 280,605 bytes，目標 SHA-256；移除 stubs 再建同值 |

四個完整 test failures 實查如下，不是把失敗忽略成 pass：

1. `deploy evidence from a real deploy record…`：`manifest.json has no valid commit`，`tests/deploy-evidence.test.mjs:54` 需要 private `132228c`；後面的 `3f661eb` 比對及同 test 後續 assertion 因此未執行。
2. `the door: the Enter offer appears within 1.8 m…`：stub 的 HOUSE_FOOTPRINT 明確丟出 withheld error。
3. `TEST-1: the render rules for the Enter action…`：同樣缺真正 geometry。
4. `group 8: the ?interior= preview…`：缺 `src/world/interior/mockSeats.ts`。

不加 stubs 時，三個測試檔因缺 households.ts 無法載入，另同一 private-history failure。stubs 只轉出公開 houseSize，geometry 讀取即 throw；沒有自行編造房屋幾何使測試過關。完整 frontend `npm run build` 未執行；tsc 已顯示快照不足以完成它。

Worker 實際建置指令：

```sh
mkdir -p dist
printf '<!doctype html>\n' > dist/index.html
# 首次未設 XDG_CONFIG_HOME，wrangler 無法建立 /root/.config/.wrangler，exit 1
XDG_CONFIG_HOME=/tmp/imd-wrangler-config WRANGLER_SEND_METRICS=false \
  npm_config_cache=/tmp/imd-npm-cache \
  ./node_modules/.bin/wrangler deploy --dry-run --outdir /tmp/imd-worker-rebuild
# 將兩個 stub 移到 /tmp，執行無 stub tests／tsc 後再重建至 /tmp/imd-worker-source-only
sha256sum /tmp/imd-worker-source-only/index.js
wc -c /tmp/imd-worker-source-only/index.js
```

```text
wrangler 4.143.0
Total Upload: 274.03 KiB / gzip: 70.57 KiB
API_LIMITER 180/60s; SEAT_LIMITER 60/60s; AUTH_LIMITER 20/60s; CHAIN_LIMITER 20/60s
--dry-run: exiting now.
018df7b35117bf612cd9311a800de75964b07f9d74f2c2f1ae545b26894cf62c
280605
```

dry-run 列出的 bindings 來自本機 config，不是遠端查詢。自寫 probe 的初版 control 因每次 provider() 建新物件而提早中止、top-level await 未完成（exit 13）；修正為同一 provider 物件後三個 assertion 情境均完成（exit 0）。R-1 的主重現前後相同；沒有改被測 AuthClient 或 handler。

## Unverified items 與 Genesis to-dos

### 未驗證項目（證據缺口，不冒充 confirmed 漏洞）

- **Live frontend inventory／hash／headers／session JSON：unknown**，原因是五次 403，不能將 repo 的 archived counts 充作 live recount。也因此無法從公開 bundle 補查 withheld WorldApp、interior、XSS sinks、動態 wallet methods 或 Enter 的 production 接線。
- **實際 running Worker、traffic split、secret 值、D1 schema／0005、limiter bindings、WAF rule：unknown。** 本機重建與 migration tests 不能代替 Cloudflare 控制面證據；未探測 edge 20/10s 門檻。
- **真錢包／瀏覽器：unknown。** R-1 的特定 provider 回應時序與 wallet UI 是否允許舊 A 簽名未實測；React server render 不是 browser E2E。沒有真實資產或合約行為驗證。
- **完整 frontend build、withheld geometry／house placement、private git history、完整 861 tests：unknown。** 三個 geometry／preview failures 與一個 history failure 仍是缺口。沒有驗證 private source 僅改 docs/test 的完整敘述。
- **正式 cache／upstream quota／成本與攻擊可達性：unknown。** 本機 exact limiter、fixture index／RPC 與真 Cloudflare 的差異已列出；沒有實際攻擊、ISP 分配或多 colo 流量證據。未發現普通 API caller 的資料污染路徑，不代表完整 XSS／supply-chain audit 已完成。

### World／Mint 邊界與 Genesis 待辦

**[碼讀]** parent compare 顯示 MINT_BOUNDARY.md 未變，account/world route handlers 沒有 Mint handler；此次 N 修正沒有加入 Mint API、server signer 或交易流程。公開 auth client 仍只 personal_sign 這份 SIWE。**[未知]** 因 live bundle 未取得，不能把「本機公開碼沒有 Mint」擴大成完整 live／withheld 前端的獨立確認。

**[團隊]** 未來 Genesis Mint 同 origin 並共用這個 session；其實作、合約與權限均在本輪範圍外，答案是 **unknown**。G-1～G-3／S-2 不是已關閉：

- G-1：須獨立定義 Mint 授權與每次使用者確認；7 天 World session 不是 Mint consent。
- G-2：須重新評估 relay SIWE、permissive ERC-1271，以及 Mint 當下 eligibility；World 的 ownerOf／24h presence／30s cache 是顯示規則。
- G-3／S-2：contract address、chain ID、transaction parameters、approval、Permit／Permit2、simulation、recipient、amount／quantity、replay、smart-wallet behavior、session reuse、same-origin cookie exposure、CSP／wallet RPC／storage 變更都待另外審查。沒有任何一項可用本次 World test pass 代答。

本報告證據僅支持上述固定快照的具體修正與殘餘判定；live 五個 GET 與 withheld／private／production 控制面未完成的驗證仍明確留白。

## 附錄：本次獨立 probe 完整程式

以下程式也隨報告保存，避免依賴 scratch 目錄。放在已安裝 lockfile 依賴的 source 副本 `tests/reviewer-probe.mjs`，執行 `node tests/reviewer-probe.mjs`。所有 HTTP 物件交給本機 handler，沒有網路 fetch。

```javascript
// Run after copying this file to tests/reviewer-probe.mjs in the pinned source snapshot.
// Local fixtures only; no production requests, real wallets, persisted keys or signatures.
import assert from 'node:assert/strict';
import {AuthClient,statusOf} from '../src/world/auth.ts';
import {setup,newAccount} from './wallet-harness.mjs';
const h=setup(),b=h.browser(undefined,undefined,'198.51.100.20');
const A=newAccount(),B=newAccount();
let resolveAccounts,startedResolve;
const started=new Promise(r=>startedResolve=r),requests=[],prompts=[];
const provider={request:async q=>{
 if(q.method==='eth_requestAccounts'){startedResolve();return new Promise(r=>resolveAccounts=r);}
 if(q.method==='eth_accounts')return [];
 if(q.method==='personal_sign'){prompts.push(q.params[1].toLowerCase());return A.signMessage({message:{raw:q.params[0]}});}
 throw new Error(q.method);
}};
const client=new AuthClient({provider:()=>provider,origin:'https://imdember.com',now:h.clock.now,
 hint:{get:()=>null,set:()=>{}},env:{set:()=>null,clear:()=>{},onVisible:()=>()=>{}},
 fetch:async(path,init={})=>{requests.push(path);return init.method==='POST'?b.post(path,JSON.parse(init.body)):b.get(path);}});
await client.restore();
const flow=client.signIn();await started;
client.accountChanged(B.address.toLowerCase());
assert.equal(client.state.account,B.address.toLowerCase());
resolveAccounts([A.address]);await flow;
const result={scenario:'accountsChanged(B) while eth_requestAccounts(A) response is held',prompts:prompts.length,promptForOldA:prompts[0]===A.address.toLowerCase(),verify:requests.filter(x=>x==='/api/auth/verify').length,accountRevertedToA:client.state.account===A.address.toLowerCase(),sessionForA:client.state.session?.address===A.address.toLowerCase(),status:statusOf(client.state,h.clock.now())};
assert.deepEqual(result,{scenario:result.scenario,prompts:1,promptForOldA:true,verify:1,accountRevertedToA:true,sessionForA:true,status:'signedInNoHouse'});
console.log(JSON.stringify(result,null,2));
// Control: a switch during the challenge body, the original N-2 scenario, is cancelled.
const c=setup(),browser=c.browser(undefined,undefined,'192.0.2.10');let release,bodyStarted;const pending=new Promise(r=>bodyStarted=r);let asked=0,verified=0;
const ctrlProvider={request:async()=>{asked++;return '0x12';}};
const ctrl=new AuthClient({provider:()=>ctrlProvider,origin:'https://imdember.com',now:c.clock.now,hint:{get:()=>null,set:()=>{}},env:{set:()=>null,clear:()=>{},onVisible:()=>()=>{}},fetch:async(path,init={})=>{
 if(path==='/api/auth/verify')verified++;
 const r=init.method==='POST'?await browser.post(path,JSON.parse(init.body)):await browser.get(path);
 if(path==='/api/auth/challenge'){const data=await r.json();return {ok:true,json:async()=>{bodyStarted();await new Promise(r=>release=r);return data;}};}
 return r;
}});
await ctrl.restore();ctrl.accountChanged(A.address.toLowerCase());const run=ctrl.signIn();await pending;ctrl.accountChanged(B.address.toLowerCase());release();await run;
assert.deepEqual([asked,verified],[0,0]);console.log('Original N-2 delayed challenge body control: prompts=0 verify=0');
// Counting the bound means index operations, not individual paginated HTTP reads.
const pages=setup();pages.chain.state.endlessPages=true;
pages.env.CHAIN_LIMITER={limit:async({key})=>({success:key!=='chain:index'})};
const pb=pages.browser(undefined,undefined,'198.51.100.80');await pb.signIn(newAccount());
const ph=await (await pb.get('/api/me/home?fresh=1')).json();
const pageReads=pages.chain.state.calls.filter(x=>x.url.includes('/nft/')).length;
assert.equal(pageReads,5);assert.equal(ph.recheck,'partial');
console.log('N-6 pagination control: one admitted lane operation = '+pageReads+' NFT HTTP GETs; recheck='+ph.recheck);
```
