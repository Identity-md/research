# IMD Ember World（imdember.com）錢包連線與 SIWE 登入：審查報告（World-only）

> 本報告是一位外部 reviewer 在限定範圍內所做檢查的**紀錄**。它不是稽核、認證或安全保證，也不代表任何背書。
> 報告沒有宣稱網站「安全」，只寫出看到的證據、由證據推出的結論、還不確定的地方，以及沒有回答的問題。
>
> 標記說明：**【事實】** = 本 reviewer 親自執行或讀到、可重現的結果；**【推論】** = 由事實推出、未直接觀測的結論；
> **【團隊端】** = 只有專案方提供的說法或紀錄，本 reviewer 無法獨立驗證；**【未知】** = 沒有證據可判斷。

- 審查日期：2026-09-28（UTC，正式站請求時間 18:08:45Z–18:13:33Z）
- 審查者環境：Linux x64、Node v24.19.0（官方 tarball）、npm 11.17.0

---

## 0. 結論摘要（回答問題）

問題：「玩家在 https://imdember.com（Worker `imd-world` version `beac62be-27ff-40cd-9dc4-3cbbdc6add4b`，commit `0def8cb5…758d`）連上錢包並簽名登入，是否安全？」

在本輪能驗證的範圍內：

1. **錢包只被要求做三件事** 【事實】：`eth_accounts`（不跳提示）、`eth_requestAccounts`（連線提示），以及**唯一一個簽名** `personal_sign`，簽的是伺服器產生的 SIWE（EIP-4361）純文字訊息。正式 JS 與原始碼裡都沒有交易、typed data（EIP-712）、Permit／Permit2、`approve`、`setApprovalForAll`、`wallet_sendCalls` 批次呼叫、session key／`wallet_grantPermissions`、切鏈／加鏈（第 3 節）。所以就錢包提示而言，**這個網站沒有要求任何能直接轉移資產或授權花費的操作**。這一點在正式 bundle 上重新計數過。
2. **伺服器端 SIWE 驗證**：nonce 是一次性的，重放回 409；驗簽失敗會作廢 challenge；session 權杖是隨機值，資料庫只存雜湊；`__Host-` cookie 帶 HttpOnly、Secure、SameSite；POST 會檢查 Origin；limiter 在綁定缺失或丟例外時拒絕請求（fail closed）。以上都經本機測試確認【事實】。**沒有發現能讓攻擊者在不取得受害者簽章的情況下，以受害者地址登入的缺陷。**
3. **沒有發現 High 或 Critical 的問題。** 發現的是 Medium（shared-boundary）1 項、Low 4 項、Info 若干（第 5 節）。最值得注意的是 **F-1：SIWE 訊息可以被轉送（relay）**。攻擊者能從伺服器取得「以受害者地址登入 imdember.com」的真實訊息，再騙受害者在釣魚頁簽名，就能拿到 7 天 session。這是 SIWE 本身的限制，防線在錢包端的 domain 比對。目前 World 的 session 只給看得到、不寫伺服器的權限，所以對 World 的影響低。但它會直接影響之後放在同一個 origin、並沿用這個 session 的 Genesis Mint 頁面。
4. **部署對照判定：partial（部分驗證）**（第 6 節）。Worker bundle 我從 `source/` 重建，雜湊與預期的 `4ec73351…0eccf3` 逐位元組相同【事實】。正式站的 `index.html`、JS、CSS 雜湊也與快照宣告相同【事實】。但 Cloudflare 實際在跑的 Worker 程式、secret、D1 schema、limiter 綁定、WAF 規則都無法從外部驗證。

因此，本報告能支持的說法是：「在 commit 0def8cb、Worker bundle `4ec73351…`、前端 `index-BPJxeGls.js` 這個範圍裡，登入流程只要求一次純文字 SIWE 簽名，不要求任何交易或授權；伺服器驗證邏輯經本機重現，沒有找到繞過方法。」它**不能**支持「網站是安全的」這種概括說法（原因見第 8 節的未驗證事項）。

---

## 1. 範圍、版本與雜湊

| 項目 | 值 | 狀態 |
|---|---|---|
| 審查快照 repo | https://github.com/tungweb3/imd-ember-world-review @ `c2a8c33d2c3b1f643bb8c369527d56e51f88e9e5` | 【事實】已 checkout |
| 快照完整性 | `sha256sum -c SHA256SUMS`：全部 OK（0 行失敗） | 【事實】 |
| 快照 `source/` 對 0def8cb 的 blob | 46 個檔案的 `git hash-object --no-filters` 等於 `manifests/published-source-gitblobs.txt`；5 個不同（`wrangler.jsonc`、`DESIGN_W1_v001.md`、`collections.ts`、`moves.ts`、`0001_wallet_login.sql`），與 `REDACTIONS.md` 列出的遮蔽檔一致 | 【事實】（blob id 本身的來源是【團隊端】） |
| 來源 commit | `0def8cb5b80083d32545c59bc707fbbc92a4758d`（私人 repo） | 【團隊端】：reviewer 看不到私人 repo |
| Worker version | `beac62be-27ff-40cd-9dc4-3cbbdc6add4b` | 【團隊端】：外部無法查詢 |
| Worker bundle（重建） | `worker/index.js` 257,723 bytes，SHA-256 `4ec73351afbcc9af133fd487d7e2d33c1df6713bfa1aced881f412d38e0eccf3` | 【事實】重建值 = 預期值 = `manifests/deploy-record-SHA256SUMS.txt` |
| 正式 `https://imdember.com/` | 730 bytes，`49973696ecc3db3bdac2cf041d3f903b2b5f9bfe687f0895f2d0eb0aae357459` | 【事實】2026-09-28T18:08:46Z |
| 正式 `/assets/index-BPJxeGls.js` | 1,306,006 bytes，`3ba7f1e06d50d8a05f90bf23e7ccdbff0e6daf2717ce6e2cbe8e42319970277e` | 【事實】 |
| 正式 `/assets/index-BOzKL2IR.css` | 53,394 bytes，`83f3b7da4ac0845236cd609d89b17d3e30958ed99bbce5ded93f2ed26cafd804` | 【事實】 |
| 範圍外 | Genesis Mint（合約、mint 流程、signer、metadata／IPFS）；被保留的程式碼（3D、美術、音樂、房屋擺放、`WorldApp.tsx`）只透過公開 bundle 檢查 | — |

---

## 2. 方法與限制

- 讀過的原始碼：`source/worker/{index,app}.ts`、`source/server/{auth,ownership,world-api,presence,chain-mock}.ts`、`source/src/world/{auth,wallet,WalletPanel,walletView,moves,links}.ts(x)`、`wrangler.jsonc`、`public/_headers`、兩個 migration、`package.json`。
- 在本機執行了原本的 112 項測試，另外寫了 7 個探測測試（`artifacts/probes/reviewer-probes.test.mjs`）。探測使用快照的 `tests/wallet-harness.mjs`：真正的 Worker handler、`node:sqlite` 跑真正的 migration、假的 Alchemy／IMD。金鑰每次執行時用 viem `generatePrivateKey()` 產生，只存在記憶體裡。
- 對正式站只發了 **6 個低頻 GET**：`/`、JS、CSS、`/api/auth/session`、`http://imdember.com/`、`https://www.imdember.com/`，每個之間間隔約 2 秒。沒有 POST、登入、fuzzing 或掃描，沒有使用真實錢包或簽章，也沒有改動目標。
- 沒有做瀏覽器測試，也沒有用真實錢包擴充功能做 E2E（第 8 節）。

---

## 3. 錢包方法清單（wallet-method inventory）

### 3.1 原始碼（`source/src/world/`）

| # | 呼叫 | 位置 | 何時 | 使用者提示 | 分類 |
|---|---|---|---|---|---|
| 1 | `eth_accounts` | `src/world/auth.ts:113` | 載入或換 provider 時（`bind`） | 無 | 唯讀：讀取已授權的帳號 |
| 2 | `eth_requestAccounts` | `src/world/auth.ts:182` | 使用者按「連接／簽名入住」，而且還沒有已知帳號時 | 連線請求 | 連線 |
| 3 | `personal_sign` params `[hexUtf8(message), account]` | `src/world/auth.ts:196` | 同一次點擊，在 `POST /api/auth/challenge` 之後 | 簽名請求（純文字 SIWE） | **SIWE 登入（EIP-191 personal message）** |
| 事件 | `accountsChanged`（`on`／`removeListener`） | `src/world/auth.ts:114` | 監聽 | 無 | 換帳號處理 |
| 事件 | EIP-6963 `eip6963:requestProvider`／`announceProvider` | `src/world/wallet.ts:58-59` | 載入時 | 無 | 錢包探索 |

- session 恢復（`restore()`，`auth.ts:129-145`）**不呼叫錢包**，只 `GET /api/auth/session`，接著 `GET /api/me/home`。
- 「我的家」、回家、搬家（`moves.ts:64-70`）**不呼叫錢包**：搬家只寫 localStorage。
- `chainChanged` 不監聽（`auth.ts:109-110` 註解說明理由），也不切鏈。

### 3.2 正式 bundle 重新計數（`index-BPJxeGls.js`，SHA-256 `3ba7f1e0…277e`）【事實】

```
.request(                    3   → .request({method:`eth_accounts`
                                   .request({method:`eth_requestAccounts`
                                   .request({method:`personal_sign`,params:[Wi(a),n]
eth_accounts 1 | eth_requestAccounts 1 | personal_sign 1 | eth_ (合計) 2* | wallet_ 0
eth_sign 0 | eth_signTypedData 0 | signTypedData 0 | eth_sendTransaction 0 | eth_sendRawTransaction 0
eth_signTransaction 0 | wallet_sendCalls 0 | wallet_grantPermissions 0 | wallet_requestPermissions 0
wallet_switchEthereumChain 0 | wallet_addEthereumChain 0 | wallet_watchAsset 0 | eth_chainId 0
Permit 0 | permit2 0 | setApprovalForAll 0 | approve 1（i18n 字串 "did not approve the connection"）
0x095ea7b3 (approve selector) 0 | 0xa22cb465 (setApprovalForAll selector) 0
sendAsync 0 | .on(`…`) 只有 .on(`accountsChanged`  | chainChanged 0
WebSocket 0 | EventSource 0 | import( 0 | eval( 0 | new Function 0 | document.cookie 0
viem 0 | noble 0 | abitype 0 （用戶端沒有打包加密／交易程式庫）
genesis 0 | ipfs 0 | tokenURI 0 | authorize 0 | mint（不分大小寫）12：three.js numIntersection 等與 mintcream、說明文字，沒有 Mint 程式
```
\* `eth_` 的 2 次就是 `eth_accounts` 和 `eth_requestAccounts`。`.send(` 的 11 次都是被保留的遊戲狀態機（`this.loop.send({type:\`board\`…})`），不是 EIP-1193。

**判定**【事實】：原始碼和正式 bundle 一致，錢包 RPC 只有上面 3 種，唯一會產生簽章的是 SIWE `personal_sign`。沒有 transaction、typed data、Permit／Permit2、approve、setApprovalForAll、batch call 或 session key。

【限制】靜態計數排除不了「方法名稱在執行期組字串」的寫法。不過全部 `.request(` 只有 3 處，而且方法名稱都是字面常數，這種寫法的可能性很低【推論】。

---

## 4. 各檢查項目的結果

### 4.1 SIWE 訊息與伺服器驗證（檢查項 2）

- **訊息完全由伺服器產生並存入 D1** 【事實】`server/auth.ts:175-186`。用戶端只能提供 `address`。探測 P1 的實際欄位：`domain imdember.com`、`URI https://imdember.com/`、`Version 1`、`Chain ID 1`、`Nonce` 32 hex（128-bit，`crypto.getRandomValues`）、`Issued At`、`Expiration Time` = +5 分鐘，statement 為 "Sign in to IMD Ember World to access your home for 7 days. This does not authorize asset transfers or transactions."
- **驗證**：`server/auth.ts:188-237`。從 D1 讀出原文重新 parse，比對 domain、uri、chainId、version、statement、issuedAt、expirationTime（`:208-211`）。先試 ECDSA（`recoverMessageAddress`），失敗才走 ERC-1271。ERC-1271 會先 `eth_getCode` 確認地址有程式碼，再以 `eth_call isValidSignature`，而且要求回傳**剛好是 32-byte 的 magic word**（`:143-155`，防止回聲合約）。ERC-6492 包裝的簽章會被拒（`:205`）。
- **一次性 nonce／重放**：消耗 challenge 與建立 session 在同一個 batch 內完成；`UPDATE … WHERE used_at IS NULL …` 加上 `sessions.nonce UNIQUE`，是兩道鎖（`:229-235`）。原本的測試「concurrent verifies of one signature create exactly one session」與「challenge lifetime: expired 410, replayed 409…」都通過【事實】。
- **失敗即作廢（burn）**：`:202-222`，400／401／429 `CHAIN_BUSY`／503 `VERIFY_UNAVAILABLE` 都會作廢 challenge。flow cookie 不符時回 403，**不會**作廢（`:195`），所以沒有這個 challenge flow cookie 的第三方沒辦法把別人的 challenge 燒掉【事實，讀碼】。
- **ERC-1271 每個 challenge 最多查一次**：`CLAIM_ERC1271` 用 `checked_at` 認領（`:65-67`、`:212-217`）。測試通過。
- **登入預算**：D1 內原子計數（`INSERT … SELECT … WHERE count<budget`，`:58-60`）：每個 /24（或 IPv6 /48）每分鐘 30 個，全站每 6 秒 60 個；ERC-1271 每個網段每分鐘 3 次，另外扣每個據點的 `CHAIN_LIMITER`。探測 P4 確認全站閥門會生效【事實】。
- **limiter fail closed**：`worker/app.ts:72`，正式網址缺綁定時丟 `LimiterMissing`，路由回 503。`server/auth.ts:125-128`：綁定丟例外時，`auth`、`home`、`chain` 拒絕，`api`、`seat` 放行。原本的測試「on imdember.com a missing … limiter binding makes exactly the routes that need it answer 503」通過【事實】。

### 4.2 Session、cookie、CSRF／Origin、登出、過期、換帳號、多分頁、晚到的回應（檢查項 3）

- **Cookie** 【事實】（`server/auth.ts:116`，原本的測試逐字檢查過）：`__Host-imd_session=<32 bytes base64url>; Path=/; Secure; HttpOnly; SameSite=Lax; Max-Age=604800`；`__Host-imd_flow` 用 `SameSite=Strict`、`Max-Age=300`。沒有 `Domain`。DB 只存 SHA-256（`:226`）。每次登入都發新權杖，沒有 session fixation。
- **過期**：從 challenge 簽發起算 7 天的絕對期限，不會延長（`:226`），到期時 `readSession` 回 `SESSION_EXPIRED`（`:165`）。
- **Origin**：三個 POST 都要求 `Origin` 是 `https://imdember.com`；loopback 只在請求 URL 本身是 loopback 時接受（`:98-106`、`:267-268`）。探測 P7：logout 在沒有 Origin、`https://evil.example`、`null`、`https://x.imdember.com`、`http://imdember.com` 的情況下都回 403，`text/plain` 回 400，session 仍然有效【事實】。回應沒有任何 `Access-Control-*` 標頭，所以跨站無法讀取【事實，正式站 `/api/auth/session` 回應標頭亦同】。
- **登入 CSRF**：flow cookie（Strict）綁定 challenge，而且每次都發新值，不採用用戶端帶來的值（`:173-186`）。
- **登出**：撤銷 session 與這個 flow 下所有未完成的 challenge，而且不受 rate limit（`:245-252`、`:269-270`）。**只撤銷這個瀏覽器的 session**，見 F-4。
- **換帳號／換 provider／多分頁／晚到的回應**（`src/world/auth.ts`）：每次點擊、換帳號、登出都會遞增 `gen`，舊世代的回應直接丟棄（`:175-210`）。舊流程如果晚到一個成功的 verify，會被 `revokeAbandoned()` 登出（`:201-204`、`:239`）。帳號 A 切到 B 時會關閉屋主模式並登出 A（`:228-236`）。多分頁用 `BroadcastChannel('imd-ember-auth')` 通知，收到訊息只會重新讀伺服器，不採信訊息內容（`:103`）。原本的測試涵蓋這些情境，全部通過【事實】。【限制】沒有在真實瀏覽器和錢包上測過。

### 4.3 屋主 API 只從 session 取地址；沒有 WebSocket（檢查項 4）

- `/api/me/home` 的地址只來自 `readSession`（`server/auth.ts:290-294`），查詢參數只讀 `fresh`。探測 P6：帶 `?address=<別人>&wallet=<別人>` 和 `x-address` 標頭，回傳的仍是 session 自己的地址（eligible 0），沒有 session 時回 401【事實】。
- `/api/wallet/:a/assets` 是公開的、未驗證的名冊資料（`source:'imd'`），不做需要金鑰的鏈上讀取，也不給屋主權利（`server/ownership.ts:207-214`）。
- WebSocket／EventSource／WebSocketPair：原始碼、重建的 Worker bundle、正式 JS 都是 0 次【事實】。

### 4.4 所有權（檢查項 5）

- 所有權的證明：以 Multicall3 `aggregate3` 對 `SEAT_COLLECTION = 0x0000ec93127baa929e58e97dd0095a2bfb38ec1d`（`src/world/market.ts:8`）做 `ownerOf`，第一個 call 用 `latest` 並取得區塊號，後續分塊都釘在同一個區塊（`server/ownership.ts:52-68`）。IMD 名冊與 Alchemy 索引只提供候選（`:161-179`）。原本的測試「forged candidates are rejected by ownerOf」通過【事實】。
- 轉手：證明快取 30 秒；已賣出的席位 30 秒內消失；新買的席位在 5 分鐘內出現（「Check again」是 30 秒）（`:19-23`）。測試「a sold seat drops within 30 s」通過。用戶端在重查持續失敗（非 503）時，最多還會保留屋主模式 3 分鐘（`src/world/auth.ts:81`、`:161-162`），影響只限本機畫面。
- 鏈上讀取失敗時回 503 `OWNERSHIP_UNAVAILABLE`，不會當成「一個都沒有」，也不快取（`ownership.ts:35-49`、`:139`）。測試通過。
- 一錢包一房、大小依計入的席位數（`ownership.ts:196-202`、`houseSize.ts`）：與產品規則相符，**不列為缺陷**。
- #361／#921：公開的 `server/`、`worker/` 程式沒有以席位編號給任何特權【事實，grep】。被保留檔案中的引用只能從 bundle 間接確認，屬展示用途【團隊端說明＋bundle 可見】。

### 4.5 重建與雜湊（檢查項 6）：見第 6 節。

### 4.6 依賴、動態模組、CSP／標頭、XSS（檢查項 7）

- 執行期依賴：`viem 2.56.9`、`@noble/curves 1.9.1`（只在 Worker 內）、`react`／`react-dom 19.2.6`、`three 0.186.1`，全部鎖定確切版本；lock 檔有 157 個 `integrity`。`npm audit --omit=dev`：**0 vulnerabilities**【事實】。
- dev／建置依賴：`npm audit` 回報 5 項（1 low、4 high），都在 `wrangler 4.92.0 → miniflare → undici／sharp` 與 `esbuild`（Windows dev server）。這些只在建置、本機開發時使用，不進 bundle（見 F-6）。
- 重建的 Worker bundle 只含 15 個專案檔與 `viem`、`abitype`、`@noble/hashes`、`@noble/curves`【事實，sourcemap】。
- 動態模組：正式 JS 的 `import(`、`eval(`、`new Function`、`Worker(`、`importScripts`、`srcdoc` 都是 0【事實】。
- CSP（正式站，`/`、JS、CSS 都相同，與 `public/_headers:24` 一致）【事實】：
  `default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob: https://nft-cdn.alchemy.com; connect-src 'self' blob: https://api.dexscreener.com; object-src 'none'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'`
  另有 `X-Frame-Options: DENY`、`nosniff`、`HSTS max-age=31536000; includeSubDomains`、Referrer-Policy、Permissions-Policy。API 回應帶 `default-src 'none'`、`CORP same-origin`、`no-store`。`http://imdember.com/` 與 `https://www.imdember.com/` 都 301 到 `https://imdember.com/`，不設 cookie【事實】。
- XSS：`innerHTML` 5 次、`dangerouslySetInnerHTML` 12 次，都在 React DOM 內部；`javascript:` 3 次是 React 的阻擋字串【事實，上下文 grep】。錢包圖示只接受 `data:image/*` 且 ≤64 kB，以 `<img>` 顯示（`wallet.ts:35-42`）。NFT 圖片只接受 `nft-cdn.alchemy.com`（`ownership.ts:97-104`、`WalletPanel.tsx:58`）。外部連結用 `rel=noreferrer`。沒有看到可注入 HTML 的路徑【推論，基於靜態檢查】。

### 4.7 World／Mint 邊界（檢查項 8）

| 面向 | 目前狀態 | 依據 | 日後同 origin 的 Mint 子頁 |
|---|---|---|---|
| origin | 只有 `imdember.com`（`wrangler.jsonc:30` custom domain，`:33-34` workers_dev／preview 關閉） | 【事實】設定；workers.dev 回 404 為【團隊端】 | 同 origin → 共用 cookie、localStorage、錢包的 origin 授權 |
| cookie | `__Host-imd_session`／`__Host-imd_flow`，Path=/ | 【事實】 | Mint 頁面會自動帶上 World session（持有人說明） |
| bundle | 正式 JS 沒有 Mint 程式（genesis／ipfs／tokenURI／authorize 都是 0） | 【事實】 | 【未知】 |
| 路由 | Worker 只處理 `/api/{auth,me,wallet,world}/*`，其他路徑一律交給 ASSETS（`worker/app.ts:86-92`、`wrangler.jsonc:28`） | 【事實】程式；平台行為（例如 `/api/mint` 會得到 SPA index.html）為【推論】，沒有發請求驗證 | 【未知】 |
| 資料 | D1 `imd-world`：`login_challenges`、`sessions`、`seat_presence` | 【事實】migration；正式 schema【未知】 | 【未知】Mint 會如何讀 session |
| signer | Worker 沒有私鑰；`Env` 只有 ASSETS、4 個 limiter、`ALCHEMY_API_KEY`、DB、`CHAIN_MOCK_OWNERS`（`worker/app.ts:19-20`） | 【事實】程式；正式 secret 只有名稱是【團隊端】截圖 | 【未知】 |
| CSP／標頭 | `_headers` 的 `/*` 規則套用到所有靜態頁 | 【事實】 | Mint 如果要放寬 CSP（RPC、WalletConnect 等），World 也會一起被放寬【推論】 |

---

## 5. 發現（依類別分開）

嚴重度是 reviewer 依目前 World 的影響判定。目前 session 只提供唯讀的「我家」查詢與本機的屋主模式，**沒有任何伺服器端寫入或資產操作**，所以多數項目的影響都受限。

### 5.1 已確認的 World 問題（confirmed World issues）

#### F-2 【Low／Info】ERC-1271 合約若對任何簽章都回 magic value，任何人都能以該合約地址登入並取得屋主模式
- 證據：`server/auth.ts:143-155` 接受任何有程式碼、且回傳 32-byte magic word 的 `isValidSignature`。
- 重現：`artifacts/probes/reviewer-probes.test.mjs` P2。一個假合約持有 #361 並對任何雜湊回 `0x1626ba7e`；用 65 bytes 隨機簽章 verify → 200，`/api/me/home` 回 `eligible 1 size s`。
- 影響：這是 ERC-1271 本身的語意，由合約自己決定誰可以代表它簽名。受影響的是存放在「寬鬆」合約（例如某些金庫或 escrow）裡的席位，可被任何人標為「我家」。目前只有本機畫面效果。對日後的 Mint，見 G-2。
- 【推論】正式環境同樣成立，因為 bundle 相同。

#### F-3 【Low，可用性】少數 /24 網段就能用垃圾簽章耗盡單一據點的 `chain:erc1271` 預算，讓智慧錢包登入暫時回 429
- 證據：`server/auth.ts:146`、`:212-216`。任何非 ECDSA 簽章，即使對方是 EOA，都會先認領，並在 `eth_getCode` **之前**扣掉 `CHAIN_LIMITER`（`chain:erc1271`，每據點 20/分，`wrangler.jsonc:49`）；每個網段每分鐘 3 次（`:54`）。
- 重現：探測 P3。7 個 /24 各做 3 次「challenge → 隨機簽章 verify」，有 20 次扣到預算；接著一個合法智慧錢包 → `429 {"error":"CHAIN_BUSY"}`【事實，本機】。
- 影響：同一個 Cloudflare 據點的智慧錢包（Safe 等）使用者，在攻擊持續期間無法登入；ECDSA 錢包不受影響。這是預算設計的已知取捨（程式註解提到「per location」），但文件沒有量化「多少網段就能關閉」。正式站的邊緣 WAF（每 IP 10 秒 20 次）擋不住，因為每個 IP 只需要很低的速率【推論】。
- 建議：先 `eth_getCode`（這一步本身也要花 key），或者在 ECDSA 失敗而地址沒有 code 時直接 401、不扣 chain 預算。這需要權衡 keyed read 的成本，由專案方決定。

#### F-4 【Low】登出只撤銷目前瀏覽器的 session；沒有「登出所有裝置」，也沒有依地址撤銷
- 證據：`server/auth.ts:245-252` 只依 cookie 的 token_hash 撤銷；`sessions_address` 索引存在（`0001:14`），但沒有任何路由使用。
- 重現：探測 P5。同一地址在兩個瀏覽器各登入一次；B 登出（204）後，A 的 `/api/auth/session` 仍然 `signedIn:true`【事實，本機】。
- 影響：被竊的 session cookie（例如 F-1 的 relay）或遺留在公用電腦上的 session，最長有效 7 天，玩家沒有辦法主動撤銷。目前 World 的影響低；如果 Mint 沿用這個 session，影響會提高（G-1）。

#### F-5 【Low，可用性，已揭露】全站 challenge 閥門可被約 20 個 /24 持續關閉
- 證據：`server/auth.ts:25-36`、`:54-60`；`CHALLENGE_BUDGET_NETWORKS = 20`。
- 重現：探測 P4。一個 6 秒窗口內送 60 個 challenge 之後，新網段 → `429 SIGN_IN_BUSY`【事實，本機】。
- 影響：所有玩家暫時無法登入（不影響瀏覽）。程式註解已經說明這是「runaway valve」的取捨，所以列為已揭露。

#### F-6 【Info】dev／建置依賴有已知漏洞（undici、sharp、esbuild，經 wrangler／miniflare）
- 證據：本機 `npm audit`：1 low、4 high，都不是執行期依賴；`npm audit --omit=dev` 為 0。
- 影響：只影響建置機與本機開發環境（供應鏈），不影響部署出去的 bundle。部署 bundle 的雜湊可重現，降低了「建置機器被動手腳而沒人發現」的風險【推論】。

#### F-7 【Info】其他觀察
- a. 用戶端直接 `personal_sign` 伺服器回傳的訊息，不在本機檢查 domain、URI、statement（`src/world/auth.ts:194-196`）。在 HTTPS、同 origin 的前提下沒有直接風險，但也沒有縱深防護。之後同 origin 的頁面如果被 XSS，就能用這個流程要求簽任意文字【推論】。
- b. `GET /api/me/home?fresh=1` 可以被跨站的 top-level navigation 觸發（Lax cookie 會送出），但回應讀不到，只會消耗該 session 的 `home` 桶與每據點的 `chain:index`（`server/auth.ts:292-294`）。影響可以忽略。
- c. `style-src 'unsafe-inline'` 允許注入 inline style（CSS 注入）。沒有找到注入點。
- d. loopback 放行只看 `new URL(request.url).hostname`（`worker/app.ts:69`、`:78`）。在只有 custom domain、workers.dev 關閉的前提下，外部請求無法走到這條路【推論】。
- e. 錢包鎖定（`accountsChanged []`）時保留 session（`src/world/auth.ts:230`，設計如此），session 與錢包是否仍連線無關。

### 5.2 Shared-boundary 問題（World 與日後同 origin 的 Mint 共用）

#### F-1 【Medium（shared-boundary）；目前對 World 為 Low】SIWE 訊息可被轉送（relay／phishing），伺服器的 Origin 檢查只能防瀏覽器
- 證據：`server/auth.ts:98-106` 只檢查 `Origin` 標頭，非瀏覽器客戶端可以任意偽造；`challenge()` 接受任何地址（`:171-172`），並把 flow cookie 發給請求者（`:186`）。簽章沒有綁定到請求者的瀏覽器，只綁定到 nonce，以及持有 flow cookie 的人。
- 重現（本機，合成金鑰）：探測 P1。模擬「伺服器端腳本」偽造 `Origin: https://imdember.com`，取得受害者地址的 challenge；受害者（在釣魚頁上）對這段文字 `personal_sign`；腳本用自己的 flow cookie verify → `200 {"address":"0x2960…3C41","expiresAt":…}`，並取得 7 天 session【事實，本機】。
- 前提：受害者必須在 5 分鐘內，對一段寫著 `imdember.com wants you to sign in…` 的訊息簽名，而且要在**不是 imdember.com 的網站上**簽。符合 EIP-4361 的錢包（例如 MetaMask）會比對訊息 domain 與請求 origin，顯示警告或拒絕；不做這項檢查的錢包、或以 `window.ethereum` 注入的錢包，都依賴使用者自己判斷【推論；本輪沒有用真實錢包驗證各錢包的行為】。
- 影響：目前攻擊者拿到的是受害者地址的 World session，能看到的「我家」資訊本來就可從公開名冊推得，而且沒有伺服器寫入。**如果日後的 Mint 頁面把這個 session 當成「這個錢包同意 mint」或「白名單資格」的憑證，這就會變成實質風險**（G-1）。
- 這是 SIWE 的通用限制，不是實作錯誤；專案文件（SIWE.md 等）沒有提到。

#### F-8 【Info（shared-boundary）】同 origin 的 CSP、cookie、localStorage、錢包授權都共用
- `_headers` 的 `/*` 規則、`__Host-` cookie（Path=/）、以錢包的「已連線網站」為單位的授權，都是 origin 層級。Mint 子頁面上的任何 XSS 或放寬的 CSP，都等同作用在 World 上，反之亦然【推論】。

### 5.3 未驗證事項：見第 8 節。

### 5.4 Genesis Mint 上線前待辦（Genesis to-dos；本輪沒有檢視 Mint）

- **G-1**：不要把目前的 World session 直接當成 mint 授權。目前的 SIWE statement 寫的是「access your home for 7 days. This does not authorize asset transfers or transactions」，使用者並沒有同意 mint。如果 Mint 需要伺服器端授權（authorize／finalize、配額、白名單），應要求**另一次、內容明確的簽名**，或至少在短時效、帶 Mint 專屬 statement／`Resources` 的 SIWE 之後才授權；同時處理 F-1 的 relay 風險（例如加 Request ID、Mint 專屬 nonce，並把鏈上交易的 `msg.sender` 當成最終依據）。
- **G-2**：Mint 的資格如果依賴 ERC-1271 登入，要考慮 F-2（寬鬆合約）與 ERC-6492（目前拒絕）。
- **G-3**：新增「撤銷此地址所有 session」的能力（F-4），並考慮為 Mint 另設較短的 session 期限。
- **G-4**：Mint 需要的 CSP 放寬（RPC endpoint、WalletConnect relay、IPFS gateway 等）應限定在 Mint 路徑（`_headers` 可依路徑設定），不要放寬 `/*`（F-8）。
- **G-5**：Mint 會帶進 `eth_sendTransaction`，可能還有 `wallet_switchEthereumChain`、typed data。錢包方法清單（第 3 節）要在 Mint 上線後重新計數；World 的 bundle 最好維持目前這 3 種方法。
- **G-6**：新增 `/api/mint*` 路由時，要一併更新 `run_worker_first`、Origin 檢查、limiter 綁定與 fail-closed 行為；確認 Mint 的 signer 私鑰不在 `imd-world` Worker 的 `Env` 中，或在另一個 Worker、有另外的權限隔離。
- **G-7**：Mint 審查時，需要重新確認 `sessions` 的讀取路徑，以及 D1 的共用範圍。

---

## 6. 部署對照判定：**partial（部分驗證）**

| 項目 | 判定 | 理由 |
|---|---|---|
| Worker bundle 由 `source/` 可重現 | **verified**【事實】 | 本機重建 `4ec73351…0eccf3`，257,723 bytes，等於預期值與 `deploy-record-SHA256SUMS.txt` |
| 「部署紀錄中的 bundle = 上傳的 bundle = Cloudflare 正在執行的程式」 | **unverified**【團隊端】 | 外部無法下載執行中的 Worker；version id `beac62be…` 無法查詢 |
| 正式 index.html／JS／CSS | **verified（與快照宣告的雜湊相同）**【事實】 | 3 個 SHA-256 都等於 `manifests/live-sha256.txt` 與 README 所列 |
| 前端 bundle 由原始碼重建 | **unverified** | 前端需要被保留的 `WorldApp.tsx` 等檔案，無法從快照建置；「重建 = 正式」只有【團隊端】證據。錢包相關檢查直接對正式 bytes 做，所以這一點不影響第 3 節的結論 |
| 安全標頭 | **verified（線上觀測）**【事實】 | 6 個標頭與 `_headers` 相同；API 標頭與 `API_HEADERS` 相同 |
| limiter／D1 綁定、secret、D1 schema（含 0002）、WAF 規則、其他 Worker／Pages | **unverified**【團隊端】 | 只有持有人提供的截圖或說明 |

整體為 **partial**：可重現的部分都相符，但決定實際行為的執行環境無法獨立確認。

---

## 7. 執行的指令與輸出（節錄；不含 owner logs）

```sh
# 取得快照
git clone https://github.com/tungweb3/imd-ember-world-review repo && cd repo
git checkout c2a8c33d2c3b1f643bb8c369527d56e51f88e9e5
sha256sum -c SHA256SUMS | grep -v ': OK$'            # 無輸出（全部 OK）
# 46 個檔案 git hash-object --no-filters == manifests/published-source-gitblobs.txt
#   → blob ok=46 diff=5（DIFF 為 5 個遮蔽檔）

# Node v24.19.0 / npm 11.17.0（官方 tarball）
cd source && npm ci
cp ../TESTS/stubs/households.ts src/world/households.ts && npm test; rm src/world/households.ts
#   ℹ tests 112  ℹ pass 112  ℹ fail 0

# Worker 重建
mkdir -p dist && printf '<!doctype html>\n' > dist/index.html
WRANGLER_SEND_METRICS=false npx wrangler deploy --dry-run --outdir ../../worker-rebuild
#   Total Upload: 251.68 KiB / gzip: 64.53 KiB；bindings: DB, API/SEAT/AUTH/CHAIN_LIMITER, ASSETS
sha256sum worker-rebuild/index.js
#   4ec73351afbcc9af133fd487d7e2d33c1df6713bfa1aced881f412d38e0eccf3  (257723 bytes)
grep 'worker/index.js' manifests/deploy-record-SHA256SUMS.txt
#   4ec73351afbcc9af133fd487d7e2d33c1df6713bfa1aced881f412d38e0eccf3  deploy-records/20260928T160119Z-0def8cb/worker/index.js
# 字串計數（重建 bundle）：SIGN_IN_BUSY 1, CHAIN_BUSY 1, LIMITER_UNAVAILABLE 1, limiter_unavailable 1,
#   chain:erc1271 1, chain:index 1, chain:assets 1, WebSocket 0, EventSource 0, WebSocketPair 0
# sourcemap 專案檔 15 個；第三方：abitype, viem, @noble/hashes, @noble/curves

# 正式站（6 個 GET，間隔約 2 秒，2026-09-28T18:08:45Z–18:13:33Z）
curl -sS -D index.headers -o index.html https://imdember.com/
curl -sS -D js.headers    -o index.js   https://imdember.com/assets/index-BPJxeGls.js
curl -sS -D css.headers   -o index.css  https://imdember.com/assets/index-BOzKL2IR.css
curl -sS -D session.headers -o session.json https://imdember.com/api/auth/session   # 200 {"signedIn":false}, no-store, 無 ACAO
sha256sum index.html index.js index.css
#   49973696ecc3db3bdac2cf041d3f903b2b5f9bfe687f0895f2d0eb0aae357459  index.html (730)
#   3ba7f1e06d50d8a05f90bf23e7ccdbff0e6daf2717ce6e2cbe8e42319970277e  index.js (1306006)
#   83f3b7da4ac0845236cd609d89b17d3e30958ed99bbce5ded93f2ed26cafd804  index.css (53394)
curl -sS -o /dev/null -D - http://imdember.com/        # HTTP/1.1 301, Location: https://imdember.com/
curl -sS -o /dev/null -D - https://www.imdember.com/   # HTTP/2 301, location: https://imdember.com/
# 錢包方法計數：見第 3.2 節（grep -oF <字串> index.js | wc -l）

# 依賴
npm audit --omit=dev    # found 0 vulnerabilities
npm audit               # 5 vulnerabilities (1 low, 4 high)：esbuild(low), miniflare, sharp, undici, wrangler（都是 dev）

# 本 reviewer 的探測（artifacts/probes/reviewer-probes.test.mjs，放進 source/tests/ 執行）
node --test tests/zz-reviewer-probes.test.mjs
#   P1 relay verify 200 {"address":"0x2960…3C41","expiresAt":1791201600000}
#   P2 verify 200 home eligible 1 size s
#   P3 attacker attempts that reached the limiter 20 -> legit smart wallet 429 {"error":"CHAIN_BUSY"}
#   P4 after 60 challenges in one slice, fresh network -> 429 {"error":"SIGN_IN_BUSY"} networks needed…: 20
#   P5 logout 204 other browser still signed in: true
#   P6 attacker home address 0x6a1B…2307 eligible 0
#   P7 logout statuses {"none":403,"evil":403,"nul":403,"sub":403,"http":403,"textPlain":400}
#   ℹ tests 7  ℹ pass 7
```

完整探測輸出：`artifacts/probes/reviewer-probes-output.txt`。重現方式：把 `reviewer-probes.test.mjs` 複製到快照的 `source/tests/`，執行 `node --test tests/<檔名>`（需要先 `npm ci`；探測檔只 import `wallet-harness.mjs` 與 `server/auth.ts`）。

---

## 8. 無法驗證的事項（unverified／unknown）

1. Cloudflare 實際執行的 Worker 程式是否就是 `4ec73351…`（version `beac62be…`）【未驗證】。
2. 正式環境的 `ALCHEMY_API_KEY` 等 secret、4 個 rate limiter 綁定、D1 綁定與 schema（是否已套用 0002）【未驗證；團隊端截圖】。`/api/auth/session` 回 200，只是間接跡象。
3. 邊緣 WAF 規則（`/api/` 每 IP 10 秒 20 次）【未驗證；依限制不做實測】。
4. 前端 bundle 是否由 commit 0def8cb 建出【未驗證】。本輪只確認正式 bytes 與宣告的雜湊相同，並直接檢查了這些 bytes。
5. 真實瀏覽器與真實錢包（MetaMask、Rabby、Coinbase、Safe 等）的行為：提示畫面、EIP-4361 domain 比對（F-1 的前提）、EIP-6963 公告、MV2 inline 注入是否被 CSP 擋掉【未驗證；沒有 E2E】。
6. `api.imd.fun`（IMD 名冊）與 Alchemy 的正確性與可用性：只影響候選與「計入」的判定，所有權仍以 `ownerOf` 為準【未驗證】。
7. 被保留的原始碼（`WorldApp.tsx` 等）：只在正式 bundle 上看過錢包相關的呼叫點，沒有逐行審查 3D／UI 程式【部分】。
8. `www`／`imd.stickember.com` 以外的子網域，以及其他 Cloudflare Worker／Pages 是否存在【未知】。因為 HSTS 設了 includeSubDomains，子網域都必須是 HTTPS；但同一個 site 的子網域在 SameSite 意義上算 same-site，仍會帶 Lax cookie 發出 top-level GET（見 F-7b，影響可忽略）。
9. Genesis Mint 頁面的設計、路由、signer、合約、CSP【未知；範圍外】。

---

## 9. 事實／推論／未知 對照（摘要）

| 陳述 | 類型 |
|---|---|
| 正式 JS 只呼叫 `eth_accounts`、`eth_requestAccounts`、`personal_sign` | 事實（計數＋上下文） |
| 伺服器拒絕重放、驗簽失敗會燒掉 challenge、limiter fail closed | 事實（本機測試，同一份原始碼） |
| 正式站的伺服器行為與上面一致 | 推論（Worker bundle 可重現；執行中的版本屬團隊端證據） |
| SIWE relay 可取得 session（F-1） | 事實（本機）；在正式站能否成功取決於錢包的 domain 檢查：未知 |
| 目前 session 不給伺服器寫入權 | 事實（公開原始碼沒有寫入路由） |
| Mint 會沿用這個 session | 團隊端說明；影響為推論 |
| 正式 D1／limiter／secret 設定 | 未驗證 |
