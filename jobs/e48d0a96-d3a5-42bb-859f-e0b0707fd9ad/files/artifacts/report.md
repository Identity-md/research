# IMD Ember World 錢包登入與屋主功能重測（World only）

**時間：**2026-09-29 15:00–15:12 UTC。**判定：**在本次可重現的範圍內，連線與登入只要求 `eth_requestAccounts` 及一則 SIWE `personal_sign`，沒有發現要求轉帳、授權 NFT／token、交易或讓 EOA 未經其簽章取得 session 的路徑。屋主資料由 session 地址的 mainnet `ownerOf` 查核；「進入我的家」的公開閘門只接受該地址自己的房屋。這些是限定版本與測試環境的觀察，**不能回答「網站安全」的概括問題**。P1 的簽名轉送仍可取得七天 session；寬鬆 ERC-1271 合約仍可讓任意簽章代表該合約；正式 Worker、D1 與邊緣設定無法從公開 GET 驗證。新觀察到的過期 session「搬家」閘門問題只寫本機畫面狀態，沒有伺服器寫入或資產操作。

標記：**〖實測〗**我執行的命令／探針；**〖源碼〗**指定 commit 的可讀程式；**〖推論〗**由前兩者導出；**〖團隊聲稱〗**部署或私人原始碼資訊；**〖未知〗**本輪無法觀察。此文件是有限重測紀錄，不是 audit certificate、認證或背書。文中 `source/...:行號` 均指 [公開快照 b6e986be6d1c85a720a3b8231feb3adf1ab2b780](https://github.com/tungweb3/imd-ember-world-review/tree/b6e986be6d1c85a720a3b8231feb3adf1ab2b780)。先前判定以 [Swarm 原報告](https://github.com/Identity-md/research/blob/main/jobs/4bd31cfb-1151-497f-9b27-40e668dea372/files/artifacts/report.md) 為準；快照文件的修復狀態只當待查主張。

## 範圍與版本

〖實測〗以 `git checkout b6e986be6d1c85a720a3b8231feb3adf1ab2b780` 固定快照，`c2a8c33d2c3b1f643bb8c369527d56e51f88e9e5..HEAD` 恰有一個 commit；`sha256sum -c SHA256SUMS` 為 **97 OK、0 failed**。對象是 `https://imdember.com` 的 World 登入、session、logout、限額、mainnet `0x0000ec93127baa929e58e97dd0095a2bfb38ec1d` 席位 `ownerOf`、一錢包一房及按計入席位決定大小的產品規則、屋主的 My home／搬家／Enter、標頭與依賴。沒有在正式站 POST、登入、掃描、簽真實錢包或送交易。

| 對象 | 版本／SHA-256 | 證據性質 |
|---|---|---|
| 先前審查 | repo `c2a8c33`，Worker `beac62be-27ff-40cd-9dc4-3cbbdc6add4b`，bundle `4ec73351afbcc9af133fd487d7e2d33c1df6713bfa1aced881f412d38e0eccf3` | 原報告；本輪沒有重跑舊版 |
| 本輪快照 | repo `b6e986be6d1c85a720a3b8231feb3adf1ab2b780` | 〖實測〗git checkout |
| 私人來源／Worker ID | `2da46cdafcf8ad3fb3571ea0273ecc5d1ab5be1d`／`50c688c9-1bcf-4b68-a0ab-b7a9dc6ec82f` | 〖團隊聲稱〗私人 repo 與 Cloudflare 執行狀態不可讀 |
| 從 `source/` 重建 Worker | `14584fe4df57e7505fc38e57a3b8b99590d948051cbc3a52b3d5a9ea969ff5e4`，264,561 bytes | 〖實測〗與預期值、`manifests/deploy-record-SHA256SUMS.txt` 相同；後者的部署來源仍是團隊紀錄 |
| 正式 `/` | `7f0f9d5409db78799bb61ba1573d780cc8ecb815f4e60c4f0c8ba7317ce7a75c` | 〖實測〗730 bytes |
| 正式 [`index-Bj4ribmm.js`](https://imdember.com/assets/index-Bj4ribmm.js) | `70742ed409b55a400cb8439c3cb5e4bac719f8a4763083c77764d3a7283ef528` | 〖實測〗1,344,457 bytes |
| 正式 [`InteriorView-Xan3ABOQ.js`](https://imdember.com/assets/InteriorView-Xan3ABOQ.js) | `fbd4e640ac1718781f8980c3671282abfa4893fbc3b05cd672831912ff1770b0` | 〖實測〗92,999 bytes |
| 正式 [`index-5qjaKexX.css`](https://imdember.com/assets/index-5qjaKexX.css) | `adaf06955abcaff313a964c753508d8be821d381bd4bf951d67e95ec08202233` | 〖實測〗54,966 bytes |

## F-1 至 F-8：前次發現的重測

下表狀態評的是**公開快照與相符的正式前端檔案**；正式執行的 Worker 另列為未驗證，不把快照的修復自動當成正式後端的事實。

| 發現、原嚴重度 | 團隊主張 | 本輪判定與證據 | 殘餘風險 |
|---|---|---|---|
| **F-1** Medium shared-boundary；World Low | 頁面逐行檢查 SIWE、簽名前與錢包視窗中提示、statement 明列 token／NFT approvals | **部分改善；relay 未修復。** 〖源碼＋實測〗`source/src/world/siwe.ts:6,17-35` 比對 11 行、domain、URI、chain 1、帳號、nonce、時間與完整 statement；`auth.ts:201-207` 檢查通過才 `personal_sign`。`walletView.ts:39-51`、`WalletPanel.tsx:89-91,109` 顯示簽名前摘要與請求來源警語；正式 JS 含新 statement、摘要及一個 `personal_sign`。頁面錯誤訊息測試通過。P1：獨立請求者取得真實 challenge、合成受害錢包簽名後，用自己的 flow cookie verify **200、`signedIn:true`**。 | 釣魚頁不執行本站檢查；真正阻隔是錢包對 EIP-4361 domain 與請求 origin 的檢查、警告或拒絕，以及玩家核對網址列。真實錢包的提示行為未測。本站 origin 被注入腳本時，頁面檢查亦不能阻止其直接呼叫 provider。 |
| **F-2** Low／Info | 記錄 `wallet_type`／`verification_method`；ERC-1271 不可用時拒絕；欄位不授權 | **欄位與 fail-closed 修復；錯誤分類僅部分符合主張。** `migrations/0003_sign_in_layers.sql:7-13`；`server/auth.ts:252-275,341-376`；session 回應 `:378-382` 不含欄位。〖實測〗EOA 寫 `EOA/ECDSA`、合約寫 `CONTRACT/ERC1271`；無 key、HTTP／網路錯誤為 503，限額拒絕／拋錯為 429，缺綁定為 503，皆無新 session。**已知合約的 `eth_call` 回 JSON-RPC error 時為 401**，詳 W-3。寬鬆假合約對任意簽章回 magic word，verify **200**、`/api/me/home` `eligible:1`；所有權仍由 `server/ownership.ts:50-67,194-202` 的 `ownerOf` 查。 | 合約自己定義有效簽章；持有席位的寬鬆合約可讓任意人取得它的 World 屋主視圖。標記僅供稽核，沒有改變這件事。 |
| **F-3** Low，可用性 | 先 no-code cache／已知智慧錢包，再 claim、`chain:code`、`eth_getCode`、每網段及每合約份額、`chain:erc1271` 或 `:known`、一次 `eth_call` | **舊 P3 修復；殘餘如述。** `server/auth.ts:98-136,222-275,341-358`；`worker/app.ts:61-86`。P3：7 個 /24 共 21 個 EOA 垃圾簽章皆 401，`chain:erc1271` 計數 **0**，隨後合法合約登入 200。以 7 個 /24、11 個假合約共 21 次查核，首次智慧錢包登入 429；對同一合約兩次垃圾查核後第三次 429，`reason:address`。 | 這些是 node:sqlite 與精確 mock limiter 的門檻；[Cloudflare rate limiter 文件](https://developers.cloudflare.com/workers/runtime-apis/bindings/rate-limit/)說明每據點且 eventually consistent，正式流量中的「至少 7／10、每分鐘 2 次」不能當硬保證。18 個 /24 可佔滿 `chain:code` 的理論門檻仍在。 |
| **F-4** Low | `POST /api/auth/logout-all` 撤銷同地址所有 session／open challenge；兩種登出按鈕 | **修復，傳播限制如述。** `server/auth.ts:278-286,384-407,439-443`；`walletView.ts:53-72`、`WalletPanel.tsx:93-96,149-153`。P5：兩瀏覽器同地址；單裝置 logout 204 後另一個仍 `signedIn:true`；重新登入後 logout-all 200，另一個下一次 session GET 為 `false`。無效、已撤銷、過期 cookie 的 401、其他地址不受影響、Origin/JSON 規則與不限流由本機測試通過。 | 其他裝置要到下一次請求才得知撤銷；持有已失效 cookie 者不能代地址撤銷其他裝置。撤銷之前 bearer cookie 仍有效。 |
| **F-5** Low，可用性 | L1–L5、每 `(address,network)` 冷卻、challenge／verify 分鍵、surge 與拒絕紀錄 | **分層已實作；全站閥門殘餘如述；log「無 IP」措辭不精確。** `server/auth.ts:98-113,290-315,412-443`，`worker/app.ts:55-75`。P4：同一 6 秒窗由 20 個 /24 各發 3 個 challenge，共 60 個 200，另一網段得 429 `SIGN_IN_BUSY`；F-5 單元測試涵蓋冷卻、獨立 limiter key、surge 與拒絕紀錄。 | 約 20 個 /24 持續滿額仍可暫停新登入；正式 WAF 規則及採樣率為團隊聲稱。log 有 `/24` 或 `/48` 網段前綴，詳見新觀察 W-2。 |
| **F-6** Info | wrangler 升至 4.143.0，當時 `npm audit` 為 0 | **部分；目前「0」不成立。** 〖實測〗`npm audit --json` 為 **3 moderate**：`undici` 的 [GHSA-3wwx-pv8p-q78v](https://github.com/advisories/GHSA-3wwx-pv8p-q78v) 經 `miniflare`／`wrangler`；`npm audit --omit=dev` 為 **0**。`source/src/world/reviewRecord.ts:39-40` 的網站審查紀錄仍寫 0；`DEPENDENCIES.md:39-47` 已承認新 advisory。 | 目前觀察為建置／本機開發工具鏈，不在本次重建的 Worker 依賴集合；不能把目前完整 audit 說成 0。 |
| **F-7(a)–(e)** Info | (a) 隨 F-1 修；(b)–(e) 接受原設計 | **(a) 修復；(b)–(e) 殘餘如述。** (a) `siwe.ts:17-25`、`auth.ts:201-207`；(b) `server/auth.ts:459-467`，跨站頂層 GET 可耗 session 自己的 home 桶及 `chain:index`，回應受 same-origin 限制；(c) 正式四個靜態回應 CSP 仍有 `style-src 'unsafe-inline'`；(d) `worker/app.ts:70-81` 的 loopback 例外只看請求 URL，`wrangler.jsonc:35-36` 宣告 workers.dev／preview 關閉；(e) `auth.ts:243-246` 鎖錢包時留 session。 | (d) 外部是否真無其他入口不可獨立驗證；(e) session 是 bearer cookie，不隨錢包鎖定撤銷。 |
| **F-8** Info，shared-boundary | World 未變；未來 Mint 同 origin 另審 | **殘餘如述。** `source/public/_headers:18-24` 套用靜態頁；`server/auth.ts:198-200` 的 `__Host-` cookie 為 `Path=/`；同 origin 的 storage 與錢包連線授權自然共用。 | 未來 Mint 若沿用這個 session，受 F-1／F-2 及共用 CSP 影響；Mint 本身未審。 |

## 變更程式碼的交叉檢查與新觀察

**授權與預算。** 〖源碼＋實測〗challenge 只能以服務端產生的 nonce／訊息及新 flow cookie 建立（`server/auth.ts:290-314`）；verify 驗 flow、時間、儲存的 SIWE 與簽章（`:316-358`），session 只在消耗 challenge 的 batch 中寫入（`:359-376`），DB 只存 token SHA-256（`:278-286`）。`INSERT_CHALLENGE` 把 L1、L2、L5 計數與插入放在一個 SQL statement（`:105-108`）；`CLAIM_ERC1271` 與 `BURN_UNCLAIMED` 同批執行（`:119-120,136,343-346`）；`CLAIM_CONTRACT` 把網段及合約地址兩個份額與 `called_at` 放在同一 UPDATE（`:124-126,348-353`）。〖實測〗node:sqlite adapter 的 batch 以 BEGIN／COMMIT、錯誤時 ROLLBACK（`source/tests/d1-sqlite.mjs:23-27`），併發 verify 一個 nonce 只有一次鏈讀；0003 前部署時 verify 503、零 session，套 migration 後可登入。 [Cloudflare D1 `batch()` 文件](https://developers.cloudflare.com/d1/worker-api/d1-database/)亦聲明 batch 以 transaction 執行、失敗 rollback。這支持 SQL 的原子設計，不能證明正式 D1 的 schema 或負載行為。

分層數值由 `server/auth.ts:98-101,105-136`、`worker/app.ts:61-75` 及 `wrangler.jsonc` 核對：L1 每 `/24`（IPv6 `/48`）challenge 30／分、code claim 10／分、contract check 3／分；L2 同地址同網段 challenge 5／分、同合約跨網段查核 2／分，某地址第 20 個 challenge 起每次記 surge 而不封鎖；L3 每 challenge 只可用一次；L4 每據點 challenge 與 verify 各 20／分、`chain:code` 180／分、`chain:erc1271` 與 `:known` 各 20／分；L5 全站 challenge 60／6 秒。`AUTH_LIMITER` 的 challenge 與 `verify:` key 分開。〖實測〗F-5 測試與 P4 符合這些本機限制；正式邊緣的近似計數及 WAF 並未實測。

〖實測〗`EXPLAIN QUERY PLAN` 顯示 INSERT 的 net／address／issued 計數各走 `login_challenges_net`／`login_challenges_address`／`login_challenges_issued`；合約份額走 `login_challenges_called_net` 與 `_address`；`KNOWN_ERC1271` 走部分索引 `sessions_erc1271`，logout-all 走 `sessions_live`。0003 的兩個 nullable session 欄位、一個 nullable challenge 欄位與索引均為 additive（`migrations/0003_sign_in_layers.sql:7-22`）；舊 session 的 NULL 不授權。已知合約查詢在 claim 前、只讀 `verification_method='ERC1271'`；它連已撤銷但尚未清理的歷史 session 也算「已知」，只影響限額與省略 code read，不直接授權（`server/auth.ts:129-135,256-269`）。60 秒 no-code cache 在 isolate 內且先於查詢已知合約（`:222-226,256-268`）；新部署的合約／7702 delegation 在同一 isolate 可能等到 cache 到期，這是已載明的可用性代價。每合約兩次查核可花掉該合約他人的當分鐘份額；這是 F-3 已明說的殘餘。未重現無簽章取得 EOA session、以一個地址撤銷另一地址 session、已撤銷 cookie 重新生效、或對**另一地址的房屋**取得正常 Enter 的路徑；撤銷／轉手後的暫時過期畫面另見下文。

### 已確認的 World 問題／觀察

**W-1｜Info｜過期 session 可繼續做本機「搬家」。** `source/src/world/auth.ts:49-61` 的 `statusOf`／`ownerAddress` 不比較 `expiresAt`；`source/src/world/moves.ts:45-50,64-70` 的 `moveGate` 與 `commitMove` 依該狀態寫 localStorage。〖實測重現〗用一個 `expiresAt=now-1`、仍保留前次 `eligible:1` home 的 AuthState：`statusOf=owner`、`moveGate=ok`、`commitMove` 寫入 1 筆；同狀態的 `enterGate=expired`（`homeEntry.ts:11-17`）。另一裝置 logout-all 後，本頁在下一次伺服器讀取前也可能保留舊 owner UI；尚未到期的本機 session 在那段時間甚至可通過 Enter 閘門，因閘門沒有即時撤銷訊號。這不代表伺服器 session 恢復。未證明此問題由本 commit 引入。影響只在該瀏覽器的房屋位置／屋主 UI；移動沒有伺服器寫入，正式 `/api/me/home` 會按 cookie 的 revoked／expiry 拒絕。建議 UI 的 owner／move 狀態也比較本機時鐘，並在可見時重讀伺服器；這不是即時撤銷的替代品。

**W-2｜Info｜拒絕 log 的「無 IP」主張須精確表述。** `source/worker/app.ts:55-58,90-91` 從 `cf-connecting-ip` 產生 IPv4 `/24`、IPv6 `/48` 網段鍵；`source/server/auth.ts:313,414-426` 把 `net` 寫進每個拒絕／surge JSON，surge 另有地址前 6 字元 `addr`。〖實測〗拒絕行例如 `{"evt":"auth_refused","route":"/api/auth/verify","status":429,"error":"CHAIN_BUSY","reason":"address","walletType":"CONTRACT","colo":null,"net":"net:192.0.4.0/24"}`。無完整客戶端 IP、完整地址、cookie、token、簽章、nonce 或訊息；但 `/24` 是 IP 衍生的網段資訊，不能字面上說「無 IP 資訊」。這是紀錄最小化／文件精確性問題，未發現授權影響。

**W-3｜Info｜已知 ERC-1271 合約的 JSON-RPC error 被報成壞簽章。** `source/server/ownership.ts:35-48` 會把 JSON-RPC `error` 傳回；`source/server/auth.ts:270-274` 在 `eth_call` 有 `error` 時回 `invalid`，`auth.ts:354-358` 因此回 401 `SIGNATURE_INVALID` 並作廢 challenge。〖實測重現〗先讓假合約正常登入一次（200，進入 known path），一分鐘後讓 fake RPC 對 `eth_call` 回 `{error:{code:-32000}}`；同合約有效簽章的新 verify 回 **401**、無新 session，而非團隊所稱節點出錯時的 503。revert 也可能合理表示無效簽章；此處無法區分它與節點故障。影響是誤導使用者及監控、要求另取 challenge；**沒有 fail-open**。

**Enter 與所有權檢查。** `source/src/world/homeEntry.ts:11-27` 的 `enterGate` 要求 owner mode、尚未到期的 session、與 session 同地址的 `/api/me/home` 結果及同地址的房屋；`enterableHome` 只找該房，其他地址的房屋無 Enter。〖實測〗三個 `group 5` 授權測試全部通過，含使用真 handler 登入後撤銷 session、home GET 401 時關門。`server/auth.ts:462-466` 只用 session 地址，忽略任意查詢地址；`server/ownership.ts:50-67,155-177,194-202` 先從公開名冊／Alchemy 找候選，再以 mainnet `ownerOf` 證明。但 `ownerOf` 證明有 30 秒 cache（`ownership.ts:19-26`），owner 頁每 60 秒可見時重讀、429 時舊 home 的保留門檻為 3 分鐘；分頁隱藏未重讀時可更久（`src/world/auth.ts:84-87,152-169,268-276`）；轉手或遠端撤銷到下次成功重讀前，本機仍可能顯示舊屋主及其 Enter，並非實時的目前所有權證明。**一錢包一房、按計入席位定大小**是產品規則。`homeEntry.ts:48-53` 允許正式 URL 用 `?debug=1&interior=...` 看 mock preview；它不建立 owner session 或 Enter 權限。房屋擺放、完整 WorldApp 接線及 interior rendering 原始碼被保留；只能從正式 bundle 靜態檢查，不能宣稱完整瀏覽器行為已驗證。

### Shared-boundary 問題

**S-1｜Medium（對目前 World 為 Low）｜F-1 relay 仍在。** 本機 P1 的攻擊者必須取得受害者對真實 SIWE 文字的簽章；目前 World session 只導向唯讀查詢及本機效果。簽名的 domain 文字本身無法證明請求來自該 domain，玩家須看網址列與錢包的 request-origin 警告。日後同 origin 的 Mint 若把此 session 當成 Mint 授權，影響會不同；此為風險推論，Mint 未受測。

**S-2｜Info｜F-8 同 origin 邊界未變。** World 的 cookie、CSP、storage、錢包「已連線網站」授權會被未來同 origin 頁面共用；本輪未發現已上線的 Mint 交易或授權入口。這是架構邊界，不能由 World 的本機測試替未來 Mint 背書。

### 尚未驗證的項目

**U-1｜未定｜正式後端與邊緣。** Worker ID `50c688c9-...`、私有來源 commit、正式 Worker 程式與 secret、D1 已套用 0003、四個 limiter 綁定與命名空間、WAF `/api/` 每 IP 10 秒 20 次、Workers Logs 採樣率 0.2 均來自團隊文件／配置；公開 GET 不足以證實實際設定。`GET /api/auth/session` 200 `{"signedIn":false}` 只證明該讀路由當時可用；若實際執行的確是此 bundle，才可間接推斷其所需的 API limiter 存在。

**U-2｜未定｜被保留檔案與真實錢包。** 沒有完整 `WorldApp.tsx`、房屋幾何、interior rendering 原始碼或瀏覽器 E2E；沒有測 MetaMask、Rabby、Coinbase、Safe 的實際提示與 EIP-4361 domain 警告。三個預期失敗的測試正是被保留幾何／mockSeats 所致，不能替它們宣稱通過。正式 NFT RPC、ownerOf 資料與真實 D1 session 亦未讀取。

### Genesis Mint 上線前待辦（範圍外）

**G-1｜未定｜**持有人說未來 Mint 是 `imdember.com` 同 origin 子頁、使用這個 session，並會另審；本輪不能驗證。Mint 不應僅以 World 的「access your home」SIWE session 視為鑄造授權，須由 Mint 專項設計與審查決定明確的確認流程。**G-2｜未定｜**重新評估 ERC-1271 寬鬆合約及 P1 relay 對 Mint 資格的影響。**G-3｜未定｜**若 Mint 需放寬 CSP 或讀取共用 cookie，須按該頁及合約另行檢視。World 的本版沒有 Mint 路由、簽名服務或鏈上交易呼叫（`source/worker/app.ts:85-95` 與正式 JS 方法計數）；不能由此推斷未來 Mint 的安全性。

## 正式檔案的錢包方法與標頭

〖實測〗在 SHA-256 如上的主 JS 中，`.request(` **3** 次，對應 `eth_accounts`、`eth_requestAccounts`、`personal_sign` 各 **1**；`accountsChanged` **2** 次（註冊／移除）。InteriorView chunk 的 `.request(` **3** 次為繪製迴圈 `this.request()`，上述錢包方法皆 **0**。兩檔合計找不到 `eth_sendTransaction`、`eth_sendRawTransaction`、`eth_signTransaction`、`eth_signTypedData`、`signTypedData`、`eth_sign`、Permit／Permit2、`setApprovalForAll`、交易 selector `0x095ea7b3`／`0xa22cb465`／`0xd505accf`、`wallet_sendCalls`、`wallet_grantPermissions`、`wallet_requestPermissions`、切鏈／加鏈或 `eth_chainId`／`chainChanged`。主 JS 的 `approve` **2** 次只在「未核准連線」與簽名前說明文字，沒有 approve 呼叫。主 JS `import(` **1** 次指向此 interior chunk。靜態字串計數有執行期拼接的理論限制；公開 `auth.ts:119,188,207` 三個 provider 呼叫點都是字面方法名，且 live JS 的三個呼叫點可對照。

〖實測〗正式 `/`、JS、chunk、CSS 各 GET 一次均 200；四個靜態回應都有 `Strict-Transport-Security: max-age=31536000; includeSubDomains`、`X-Content-Type-Options: nosniff`、`X-Frame-Options: DENY`、`Referrer-Policy: strict-origin-when-cross-origin`、`Permissions-Policy: camera=(), microphone=(), geolocation=()`，及與 `source/public/_headers:18-24` 相符的 CSP（`script-src 'self'`、`frame-ancestors 'none'`，仍有 `style-src 'unsafe-inline'`）。未帶 cookie 的 `GET /api/auth/session` 為 200、`{"signedIn":false}`、`Cache-Control: no-store`、API CSP `default-src 'none'; frame-ancestors 'none'`、`Cross-Origin-Resource-Policy: same-origin`。沒有用正式站 POST 驗 cookie、Origin 或 rate limiter。

## 部署對照判定：**partial**

〖實測〗只用公開 `source/`、lockfile 與 `wrangler deploy --dry-run` 重建 Worker 的 264,561 bytes／SHA-256 與預期及團隊 manifest 逐位元組相同；四個正式靜態檔各一次 GET 的 SHA-256 與宣告相同，標頭吻合。前端其餘 65 個靜態檔未下載；因被保留程式，未獨立重建完整前端。〖未知〗無法下載 Cloudflare 正在執行的 Worker 或讀取其 secret、D1 schema、limiter、WAF；團隊部署紀錄與 manifest 是證據材料，不能單憑它們證明遠端狀態。因此不用 `verified`，也不是 `unverified`（已有可重現的 bundle 與 live 靜態檔對照）。

## 執行命令與結果摘錄

本機 Node **v24.21.0**、npm **11.19.0**（團隊快照使用 v24.19.0／11.17.0）。測試把 `source/` 複製成獨立 git repo，`git init/add/commit` 後執行；只在副本複製 `TESTS/stubs/{households,layout}.ts`，合成金鑰只在記憶體內，RPC 為 fixture。以下為實際執行且與判定有關的輸出；省略測試流水、合成地址及任何 owner log。

```text
git clone https://github.com/tungweb3/imd-ember-world-review.git /tmp/imd-ret
git -C /tmp/imd-ret checkout b6e986be6d1c85a720a3b8231feb3adf1ab2b780
git -C /tmp/imd-ret rev-parse HEAD         -> b6e986be6d1c85a720a3b8231feb3adf1ab2b780
(cd /tmp/imd-ret && sha256sum -c SHA256SUMS)
                                           -> exit 0; 97 OK
cp -r /tmp/imd-ret/source /tmp/imd-source-test; cd /tmp/imd-source-test
git init -q; git add -A; git -c user.name=r -c user.email=r commit -qm snapshot
npm_config_cache=/tmp/imd-npm-cache npm ci --no-audit --no-fund
                                             -> added 79 packages
mkdir -p dist; printf '<!doctype html>\n' > dist/index.html
XDG_CONFIG_HOME=/tmp/imd-xdg WRANGLER_SEND_METRICS=false npm_config_cache=/tmp/imd-npm-cache npx wrangler deploy --dry-run --outdir /tmp/imd-worker-rebuild
sha256sum /tmp/imd-worker-rebuild/index.js -> 14584fe4df57e7505fc38e57a3b8b99590d948051cbc3a52b3d5a9ea969ff5e4
wc -c /tmp/imd-worker-rebuild/index.js    -> 264561
npm_config_cache=/tmp/imd-npm-cache npm audit --json
                                           -> exit 1; 3 moderate: miniflare, undici, wrangler
npm_config_cache=/tmp/imd-npm-cache npm audit --omit=dev --json
                                           -> 0 vulnerabilities
cp /tmp/imd-ret/TESTS/stubs/households.ts src/world/households.ts
cp /tmp/imd-ret/TESTS/stubs/layout.ts src/world/layout.ts
npm test                                   -> exit 1; tests 141, pass 138, fail 3
node --test --test-name-pattern='group 5' tests/home-entry.test.mjs
                                           -> tests 3, pass 3, fail 0
node tests/zz-retest-probes.mjs             -> P1 200 / session true; P3 EOA junk 401, smart 200;
                                              P3 residual first-time 429, one-contract third 429;
                                              P4 first 60 200, fresh 429; P5 logout 204 still true,
                                              logout-all 200 then false
node --input-type=module - [W-3 的 inline fake RPC probe]
                                           -> first 200; next eth_call RPC error: 401 SIGNATURE_INVALID, sessions 1
cp /tmp/imd-ret/TESTS/probes/keyed-reads-probe.mjs tests/zz-keyed-probe.mjs
node tests/zz-keyed-probe.mjs              -> EOA bad verify: first 401, four repeats 409, one eth_getCode;
                                              next challenge hits no-code cache: zero chain calls;
                                              contract bad verify: one eth_getCode + one eth_call;
                                              chain:code refusal: 429, zero chain calls;
                                              missing AUTH_LIMITER: production URL 503;
                                              every limiter refusing: logout-all 200, logout 204
```

P1/P3/P4/P5 是本輪在暫存副本撰寫的等價探針；`zz-keyed-probe.mjs` 複製自快照的 `TESTS/probes/keyed-reads-probe.mjs` 並由我重跑，兩者都沒有提交到目標 repo。其環境是 `source/tests/wallet-harness.mjs` 的真 Worker handler、`node:sqlite`、三個 migration、假鏈和記憶體合成 key。`npm test` 的三個失敗是兩個 `HOUSE_FOOTPRINT` 幾何需求與一個缺少 `interior/mockSeats.ts`；不是授權 `group 5` 測試。正式站只執行 `curl -fsS --dump-header` 的 **五個低頻 GET**：`/`、兩個 JS、CSS、`/api/auth/session`，各一次；`sha256sum` 四個靜態檔結果如版本表。
