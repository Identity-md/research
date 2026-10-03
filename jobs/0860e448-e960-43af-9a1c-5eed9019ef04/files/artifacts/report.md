# IMD Ember World 第五次技術報告：R4／AUD4 與 Member M1

日期：2026-10-03 UTC。範圍僅限非官方 TypeScript Cloudflare Worker／React World、SIWE 與公開會員資料 M1；不含 Solidity、Genesis Mint、Coin E1／0007、check-in、獎勵、經濟或金融研究。

**結論：九個原問題的指定本機重現均受到修補約束；不構成整站安全或正式環境通過。** 七項判為「本機已修復（原情境）」；合約會員寫入政策與 discovery 整體可用性判為「部分處理」，其中原攻擊／錯誤路徑在本機已阻止。Report-only **M1-R2 獨立判為本機已修復**，沒有與 M1-R1 或 Audit #5 混算。未在本次已執行情境找到新增阻斷缺陷；正式 D1 執行、真實錢包／瀏覽器與未公開 UI 仍不足以批准上線或認證安全。

## 固定來源與證據層級

所有 `source/...:行` 均指 [固定提交 357668f37c75317f79ff2266795636597a707c04](https://github.com/tungweb3/imd-ember-world-review/tree/357668f37c75317f79ff2266795636597a707c04)，不是分支 HEAD。GitHub commit API 的父提交為 **6e307dea76e763936fc4ac86e54c9f5d558f58c4**，也就是已發表的第四輪基準；[commit.json](evidence/commit.json)、[integrity.json](evidence/integrity.json) 保存讀回與雜湊。本機核對 manifest 所列 **100／100 檔案 SHA-256 與大小相符**。16 masked＋84 exact 是公開 manifest 的分類；本機只能確認公開內容與該 manifest 一致，不能由此確認私有 blobs。

私有修補 `54410b2f8dece71bdb2fd999c94feea6454ecfcd` 的 provenance 是**團隊聲稱**；未取得私有歷史，不宣稱獨立比較過其 parent。舊 root 文件只作歷史，不以舊部署／測試數據取代 R5。已讀 README、R5/TEST_RESULTS、BUILD_EVIDENCE、PRODUCTION_D1、兩份前輪報告、AUD4_REMEDIATION、MEMBER_POLICY、DISCOVERY，並核對實作與測試。

本文標籤：**實測**＝本次親自執行；**碼讀**＝固定公開來源；**推論**＝由實作／測試導出的有限結論；**團隊**＝快照附帶的紀錄；**未知**＝未取得或未執行。團隊撰寫測試由本次重跑，仍不變成獨立設計；另附本次自寫 probes。

前輪 ID 可追溯至 [Audit f3e7cfc7 原文](https://github.com/tungweb3/imd-ember-world-review/blob/357668f37c75317f79ff2266795636597a707c04/R5/PRIOR_AUDIT_f3e7cfc7.md)（job `f3e7cfc7-0b43-473a-9c0f-6931cf278c56`）及 [Report 1dbe2282 原文](https://github.com/tungweb3/imd-ember-world-review/blob/357668f37c75317f79ff2266795636597a707c04/R5/PRIOR_REPORT_1dbe2282.md)（job `1dbe2282-d61a-42a8-9823-2b24e48d29c1`）。前者八項 Low；後者 M1-R1 Low 與 Audit #5 重疊，M1-R2 Info 為第九個唯一問題。

## 九列裁決矩陣

「阻斷」指本次原問題是否仍阻止接受該修補，不是部署批准。表中沒有任何「正式全通」含義。

| R4／既有 ID | 原等級／本輪阻斷 | 裁決 | 固定程式位置與主要證據 |
|---|---|---|---|
| R4-01／AUD4-01／Audit #1 | Low；原情境不阻斷 | **本機已修復** | [server/auth.ts:651](https://github.com/tungweb3/imd-ember-world-review/blob/357668f37c75317f79ff2266795636597a707c04/source/server/auth.ts#L651)、client auth:392,458；auth 組與 P1 |
| R4-02／AUD4-06／Audit #6 | Low；原情境不阻斷 | **本機已修復** | [client auth.ts:345](https://github.com/tungweb3/imd-ember-world-review/blob/357668f37c75317f79ff2266795636597a707c04/source/src/world/auth.ts#L345)、:365,435；server auth:617；auth 組與 P2 |
| R4-03／AUD4-02／Audit #2 | Low；原任意合約寫入已阻止，完整 smart-wallet 寫入仍不接受 | **部分處理：暫停持久寫入** | [server/member.ts:33](https://github.com/tungweb3/imd-ember-world-review/blob/357668f37c75317f79ff2266795636597a707c04/source/server/member.ts#L33)、:170,209；server 組與 P3 |
| R4-04／AUD4-05／Audit #5＋Report M1-R1 | Low；原情境不阻斷 | **本機已修復，兩 ID 一個修補** | [0008:4](https://github.com/tungweb3/imd-ember-world-review/blob/357668f37c75317f79ff2266795636597a707c04/source/migrations/0008_member_hardening.sql#L4)、member:234,252,272；36 組獨立競態、P4、no-op probe |
| R4-05／AUD4-04／Audit #4 | Low；原情境不阻斷 | **本機已修復；保留期非硬期限** | [member.ts:42](https://github.com/tungweb3/imd-ember-world-review/blob/357668f37c75317f79ff2266795636597a707c04/source/server/member.ts#L42)、worker/app:153；server 組與 P5 |
| R4-06／Report **M1-R2 ONLY** | Info；原情境不阻斷 | **本機已修復，獨立裁決** | [client member.ts:103](https://github.com/tungweb3/imd-ember-world-review/blob/357668f37c75317f79ff2266795636597a707c04/source/src/world/member.ts#L103)、:112,157；member-r4 四種排序與 P6 |
| R4-07／AUD4-07／Audit #7 | Low；原情境不阻斷 | **本機已修復** | [client member.ts:144](https://github.com/tungweb3/imd-ember-world-review/blob/357668f37c75317f79ff2266795636597a707c04/source/src/world/member.ts#L144)、:154；MemberPanel:87；member-r4 與 P7 |
| R4-08／AUD4-08／Audit #8 | Low；原情境不阻斷 | **本機已修復** | [client member.ts:96](https://github.com/tungweb3/imd-ember-world-review/blob/357668f37c75317f79ff2266795636597a707c04/source/src/world/member.ts#L96)、MemberPanel:105；member-r4、SSR 與 P8 |
| R4-09／AUD4-03／Audit #3／AUD3-02 | Low；原跨 colo 污染已阻止，可用性風險仍開放 | **部分處理；原重現本機已修復** | [server/auth.ts:735](https://github.com/tungweb3/imd-ember-world-review/blob/357668f37c75317f79ff2266795636597a707c04/source/server/auth.ts#L735)、:262,281；discovery 組與 P9 |

## 各項重現、影響與事件證據

下文測試 clock 的共同起點 **T=1790596800000（2026-09-28 12:00:00 UTC）**，不是執行當天牆鐘。獨立 P1–P8 的[程式](evidence/independent.mjs)與[事件輸出](evidence/independent.log)包含 DB 數目、客戶端狀態與提示數；P9 另列。所有簽章只在本機記憶體合成金鑰及假 provider 中生成，沒有真實錢包或正式簽章。

### R4-01：共享 cookie 與 logout-all 的帳號一致性

前提是頁面顯示 A，另一分頁把共享 cookie 換成 B。舊行為會撤銷 B 卻讓 A 以為所有裝置已登出，影響安全撤銷的正確性；不是任意匿名撤銷漏洞。

**碼讀＋實測：**先驗證 live cookie，後比對 expectedAddress；不相符回 **409 ACCOUNT_CONTEXT_CHANGED**，尚未進 revoke batch。團隊案例建立 A 兩個 session、B 一個及 B 的 pending challenge：409 後三個仍 live、challenge 未失效、零 Set-Cookie；匹配 A 時才撤銷 A 的兩個，B 保留。客戶端讀回 B 或在讀回 429／503 時維持未知，notice 不宣稱所有裝置成功登出。absent、forged、dead cookie 不因 expectedAddress 得到權限。

**獨立 P1：**A/B 各一 live session → B-cookie/A-body 409 → fixture 將到期時間設為過去 → A-cookie 401；DB revoked=0，409 Set-Cookie=0。這補測 expired cookie。prompts 為 N/A（route fixture 直接合成登入），本次操作不建 session。expectedAddress 是一致性條件而非授權。晚到的 browser cookie 清除仍不是這個 request-time 比較能阻止的事項。

### R4-02：verify 已提交但 body 不可信

前提是 verify 成功寫入 session/cookie，body 隨後遺失、截斷或不是合法 session；舊版誤認未登入而再開 personal_sign。

**實測：**truncated、malformed、invalid-fields、transport-after-commit 都先保留已套用 cookie，再破壞回應；client 轉未知並 GET session。成功讀回只保留一個 session、一次 personal_sign；失敗讀回不變成 signed-out，下一 click 先重讀。確認 absence 才容許新 challenge／prompt。P2 額外讓兩次讀回 503，第三次成功：事件為 challenge → personal_sign → verify → 三次 session read → home；prompts=1、created/live=1、revoked=0，最後 sessionKnown=true。

**清理邊界：**server auth:627 以 cookie session 的 nonce 比對 expectedNonce。套件重測涵蓋 account/provider 切換、teardown、晚到失敗、新 A 或 B session，以及「新 challenge 已建立但新 session 未建立」。較新 session nonce 不符時 409，不能撤銷／清 cookie；匹配 abandoned session 時只撤舊 session及原 flow，不使新 pending challenge／flow 失效。這些案例通過；pending challenge 保護不等同較新 session 保護，兩者都有斷言。

**未知：**真瀏覽器可在上述 request-time 比對後套用另一回應的 Set-Cookie；缺失 provider events 亦無法完全辨識。未做真 cookie jar／BroadcastChannel 整合或無限 auth body 的完整可用性驗證。

### R4-03：合約登入真值與 M1 持久寫入政策

前提為任意接受簽章的 ERC1271 合約；舊版可登入後改公開名、啟動七日 cooldown。影響是公開身分污染及改名可用性，不推導資產損失。

**碼讀＋實測：**只有 session 伺服器欄位同時 **EOA AND ECDSA** 可 bootstrap／PUT／GET 的 last_login touch。CONTRACT/ERC1271、未知或缺 metadata 一律 persistent write 403 CONTRACT_WRITE_NOT_ENABLED；既有 profile 可讀但 last_login 不動，無 member 時 GET 404。會員路由零 Set-Cookie，拒絕不建 profile/history/request。EOA 正常更新仍通過。

任意 magic-word fixture 可登入但 bootstrap 拒絕。P3 加入只接受指定測試簽章的合約 predicate，login=200、bootstrap=403、sessions=1、profile/request/history=0，驗證正常允許登入的 smart-wallet 也受限制；它不是完整真實合約實作。套件亦測已有合約／未知 metadata 的讀取不 touch。

**部分處理理由：**政策有效縮小持久寫入權，卻排除合法 smart-wallet 使用者；ERC1271 登入真值仍由合約決定，沒有建立每次寫入 intent 的合約授權。EOA 的同源惡意程式／真 SIWE phishing relay 風險不因此消失。

### R4-04：五次 recorded attempts 原子額度與 M1-R1

前提為同會員多個有效新 requestId 同時到達；舊 read-count 後 insert 可越過五次限制，增加儲存工作。Report M1-R1 與 Audit #5 是同一缺陷，不能多算一項。

**實測：**[36 組自寫競態](evidence/race-independent.mjs)、[輸出](evidence/race-independent.log)＝6／12／20 × 自然／受控排程 × success、reserved-name refusal、stale version、locked、cooldown、same-name no-op。受控排程先讓所有原 request lookup 回無記錄，再放行，不改 SQL 結果。每組只有五筆當分鐘 outcome，其餘 1／7／15 個回 429；success 組只一次 mutation/history，其他組零新增 mutation/history。no-op 五筆 ok、版本／cooldown 不動；所有會員回應零 cookie。

P4：T 保存 v1＋四個 no-op＝五筆；原 ID／原 payload 重試 200、不增加 row/version/history/cooldown；改 payload 409 IDEMPOTENCY_CONFLICT。T+59999 新操作 429；T+60000 新 no-op 200。此時**累積六筆**但滾動窗只一筆，v1、history=1、cooldown=T+604800000。不可把累積列數與當分鐘額度混淆。

[獨立 no-op／rename 探測](evidence/noop-independent.mjs)在 guarded INSERT 前暫停 no-op，再讓 rename v1→v2 提交；放行後 no-op 409 PROFILE_VERSION_CONFLICT，保留 AfterCat/v2、history=2，沒有把陳舊觀察記為成功（[結果](evidence/noop-independent.log)）。另有套件 moderation race。fallback refusal recording 若 quota 滿回429，storage failure回503；同-key並發 success/refusal winner、異 payload conflict 均通過。

**碼讀／推論：**0008 BEFORE INSERT trigger 執行原子新-key檢查；成功 outcome、claim、history、profile 在同 batch，錯誤一起回滾。SQLite RAISE(ABORT) 終止 statement，整 batch 回滾依 D1 batch 契約及本機 adapter；[SQLite 官方](https://www.sqlite.org/lang_createtrigger.html)、[D1 官方](https://developers.cloudflare.com/d1/worker-api/d1-database/)支持這個設計，並不替本次證明 production isolation。

五次限制只管會記錄的有效邏輯操作，不是全部 HTTP／格式錯誤／actor mismatch／未登入成本。IP 20/min limiter 獨立；bootstrap/GET 不用 rename attempt。request 到期並被清理後不保證舊 ID 永久冪等。所有競態由單程序 SQLite adapter 排程，非 production D1 concurrency。

### R4-05：過期拒絕紀錄清理

舊前提為一直拒絕／鎖定、永不成功改名的會員，outcome 持續累積。影響資料最小化、儲存與可用性。

**實測：**server 組涵蓋 expiry index、每表 cron 200／合格寫入 opportunistic 10、backlog 分輪排空、不刪 unexpired retry、不改 current profile。缺 0008／index、DB 不存在或錯誤皆有固定失敗訊息；不偷偷裝 schema，不輸出原始 SQL／秘密。P5 在恰好一日移除唯一拒絕記錄，profile v0／history0／session1 不動；再植入205筆過期 probe，移除 M1 trigger，獨立 probe cleanup 仍刪200留5。worker/app:153 與 :157 分別排程、各自捕捉錯誤。

一日 request、180日 history 是**可刪除時間**，不是硬刪除 deadline。每15分鐘200筆意味單表 cron 理論19,200筆／日，持續輸入超過排空或 cron 延誤仍可能長期 backlog。名字與錢包連結是公開資料；不應宣稱一日後全站不再保存名字。sessions/cookies/prompts 對 cleanup 為 N/A（沒有 auth／HTTP 寫 cookie），route fixture 的既有 session 保留。正式 cron 執行與吞吐未知。

### R4-06：Report-only M1-R2，舊 GET 不得覆蓋保存結果

前提為同身份 GET(v0) 先開始，SAVE(v1) 接受，舊 GET 最後到達；舊影響是 UI 回退到 needs_name/v0，**不是 DB 回滾**。

**實測＋碼讀：**load read sequence、帳號 generation、每 publicMemberId 的最高接受 version；成功 save 還增加 reads 使既有讀取過期。套件涵蓋 GET2 先於 GET1、舊401/stream錯誤、GET(v2) 先於 PUT(v1) reply、account switch。P6 真 handler 暫存 GET v0，save OrderProbe 完成後才釋放：client=1、DB=1、request=1、history=1；無新 prompt、session 或 cookie。

裁決獨立為本機已修復。換帳號後清版本表是 generation 邊界，不宣稱跨頁面持久的最高版本；未公開 WorldApp 是否正確建立／銷毀 client 仍未知。

### R4-07：不確定 PUT 的冪等恢復與表單釋放

前提為 PUT 實際提交，但 fetch／body 遺失、無效或永不完成。舊行為 saving 永遠 true；新實作把 **fetch＋body 共15秒**納入 deadline，一次自動重試保留原 ID 與 body。

套件實測 truncated／malformed、兩次遺失、endless success body、early401/429/503、wait例外、account switch／return。timeout 使用受控 timers，不是正式網路超時。兩次未知則 saving=false、pendingSave=true、讀回，禁止新名字，只准原操作重試；拒絕若在 outcome lookup 前發生，不證明原提交失敗。

P7 在先前 v1 後推進七日並重新建立 fixture session：commit v2 → 兩個 `{}` body → GET v2，但 pending仍true → synthetic logout/回同wallet → 不同名字不送PUT → 原 retry成功。自開始共四次 PUT（一次 v1、兩次 v2 嘗試、一次原 retry），v2、history=2；舊一日 outcome被prune，現存request=1。新 rename只一次歷史／cooldown；兩個 session是兩次 fixture login，其中一個到期，非save創建。沒有真wallet prompt；MemberClient不呼叫wallet。

pending保存在同一 client 的 per-wallet Map；整頁 reload／重新建立client或已清理outcome不在永久恢復保證內。瀏覽器晚 cookie、正式 UI lifecycle 與真持久離線恢復未知。

### R4-08：冷卻到期重新可用

前提為頁面載入時 nextNameChangeAt 非null，停留越過七日截止；舊UI仍disabled。

**實測：**serverTime 校準時間、timer到期更新 cooling 並 load；到期前／恰好到期／之後、browser clock快轉仍由server拒絕、teardown取消皆通過，React SSR也檢查disabled／recovery文案。P8 確認登出切換使timer jobs=0、之後stop無額外GET、client idle。沒有DB mutation、session建立／撤銷或簽章；P8只改synthetic auth source，沒有真的撤銷cookie。長背景分頁的browser timer節流可能延後刷新，不能許諾精準牆鐘到秒；伺服器仍是冷卻權威。

### R4-09：拒絕探索不占 admitted 全域容量

原前提是colo A limiter耗盡，四個有效session從80個/24各做20次探索，拒絕仍占全域60/6s，讓colo B買家不可發現席位。影響owner-mode／Enter可用性，不授予假owner權。

**碼讀：**bounded READY預檢 → 獨立 atomic probe → local limiter → fresh-clock atomic INDEX_LANE admission → index。預檢不是保留；只有最後原子保留授權工作。probe保留30秒，/24及/64各一、/48兩；admitted仍/24或/64每分鐘一、/48兩，全域60/6s。拒絕只有probe，不污染admitted ceiling；已admit而upstream失敗仍計費、不退還。

**實測：**套件兩種refusal-counted/free模型、61個競態放行只60筆／60個index operations、IPv4/IPv6網段並發、29,999/30,000ms邊界、slow limiter新時間、missing schema/index fail closed、舊released列、D1回覆不確定均通過。保留第一份ownerOf proof，D1不確定有row但無RETURNING/changes時不啟動index，也不refund。

[獨立P9](evidence/discovery-independent.mjs)改為四session round-robin、每250ms一次、**80次共20秒**：A refused後admitted=0、probe=80、indexCalls=0；切B後200、seat361／eligible1、admitted=1、probe=81、indexCalls=1；session始終5，探索新增session=0（[事件](evidence/discovery-independent.log)）。提示數N/A，五個登入是fixture準備，不是探索提示。

**仍開放：**本地denial-counted模型10個/24在三分鐘觀察期能維持阻擋，9個不足；free模型約60秒可恢復。probe沒有全域storage ceiling；每次opportunistic最多刪2、獨立cron最多200，不等於無限新網段不增加成本。共享/24、/48、真實influx／backlog／API與session限額仍有可用性取捨。[Cloudflare官方limiter](https://developers.cloudflare.com/workers/runtime-apis/bindings/rate-limit/)描述location-local、非精準計帳特性；本機兩模型不判定正式採哪一種。因此整體AUD3-02／R4-09仍部分處理。

## R3／AUD3、N／ADV、Enter／Home 與登入不變量

[focused 83／83](evidence/focused.log)、[N 43／43](evidence/n.log)、[Enter 3／3](evidence/enter.log)、[auth＋worker 83／83](evidence/auth-worker.log)均為本次實測；互相重疊，不加總成coverage比例。

| 舊項 | 本輪裁決與仍在的邊界 |
|---|---|
| R3-R1 | 原event/connect排序本機fixed。accountEvents＋generation在連線、challenge body、signature後核對；缺provider事件的陳舊帳號仍未知。 |
| AUD3-01 | 原lane失敗丟第一proof本機fixed；ownership:280–294保留第一proof/sightings，已送upstream成本不refund；第一proof本身不可得仍503。 |
| AUD3-02 | 原拒絕污染admitted本機fixed；整體availability partly，見R4-09。 |
| AUD3-03 | 未送ERC1271 eth_call的份額回收本機fixed；已送失敗照計、nonce不復活，共享network與refusal-counted可用性殘餘保留。 |
| AUD3-04 | 已確認登出後舊session/home讀回不復顯，本機fixed；client auth讀取序號護欄。 |
| AUD3-05 | **仍partly**。共享cookie不符的home關閉owner mode；session重讀失敗仍有顯示／刷新窗口。本次logout-all一致性修正不讓整項變fixed。 |
| AUD3-06 | dead/forged logout-all不清新cookie的原問題本機fixed；request比較後瀏覽器套用late Set-Cookie仍存在。 |
| AUD3-07 | expired／AUTH_REQUIRED／讀回失敗不假報其他裝置已登出，本機fixed；不能從缺cookie推斷確切原因。 |
| AUD3-08 | IPv4/IPv6/mapped/invalid解析本機fixed；worker/app:29起；不代表真WAF bypass曾可達或正式header完整性已驗。 |
| AUD3-09 | **review-limit record，未知而非bug已修復**。部署團隊證據縮小來源缺口，不消除下面production/browser限制。 |

N-1 session讀取序、N-2 flow切換不多簽、N-3候選優先序、N-4 pool/lane隔離、N-7到期分類保留本機fixed；N-5 IPv6共享與N-6新買家探索可用性仍partly。ADV等待／abandoned-flow與新請求隔離在focused組通過；不能從合成事件推導真wallet會如期送出事件。

**登入與authority：**server/auth:530–553重新驗 stored SIWE fields與row equality（domain/URI/chain1/nonce/address/time），校驗flow；ERC6492拒絕、ERC1271 code/magic/one-check-per-challenge、consume/session唯一性、token hash、revoke/expiry等測試通過。cookie是`__Host-`、Secure、HttpOnly、Path=/、無Domain；session SameSite=Lax、七日，flow Strict。readSession從cookie hash取有效身份及伺服器驗證metadata，名稱與publicMemberId不能授權另一個wallet。

房屋權限由**session address＋Ethereum mainnet ownerOf＋seat活動eligibility**；`server/ownership.ts:54,280`與`server/auth.ts:746`將受驗address傳入，index/roster只是候選。public names、publicMemberId或地圖資料不是權利來源。Enter/Home group5重測只允許session自己的屋、401撤銷後關gate；本機Move不發資產交易。候選cap256、index五頁、快取／刷新、轉手與失敗窗口仍可能partial；非完整所有權名單或即時撤權保證。

[方法靜態清冊](evidence/wallet-scan.txt)在公開程式只見 provider `eth_accounts`（client auth:205）、`eth_requestAccounts`（:307）、精確伺服器SIWE之`personal_sign`（:338，`siwe.ts`逐行gate）。沒有找到錢包transactions、approvals、Permit/Permit2、typed-data、delegated permissions、session keys或wallet batches的實作呼叫。這是公開程式與測試邊界內的陰性結果，不證明未公開bundle／動態注入行為；server eth_call為後端讀取，不是錢包送交易。

## 隱私、可用性與未消除的信任邊界

M1名字刻意對錢包地址公開查詢，可形成長期可連結社群身份；不等於官方身份或所有權證明。history雖無公開讀取API仍是儲存資料，180日只是cleanup eligibility；當前profile與名稱claims另有生命週期。限流log仍有network／colo，非「沒有IP衍生資料」；本次沒看production log保留或第三方資料處理。

同origin惡意程式可帶HttpOnly cookie發EOA profile寫入；SIWE逐行檢查不阻止取得真challenge簽章的phishing relay。F-1共享信任／F-8同源邊界保留開放；F-2合約登入真值仍存在，M1只限制其persistent write。不能把M1稱read-only，也不能把此次暫停smart-wallet writes稱完整合約authority方案。

availability仍依Cloudflare location、WAF、bindings、D1限額／cron吞吐、Alchemy/RPC/NFT-index與IMD上游。缺binding/schema大多fail closed保護正確性但會降低可用性；慢body/網路、真實費用與influx未量測。沒有production scans、fuzz、flood或寫入。

## 測試紀錄：本次、團隊與未執行不可混合

本次Node **v24.21.0**；未執行npm ci，避免寫入禁止的node_modules。依固定lock取得17個測試需要的套件，核對integrity，保存為普通`.tgz`；自訂Node resolve hook從scratch/vendor載入。這不是完整原樣npm安裝或供應鏈審查。子程序初始CJS path處理錯誤已修正，產品source未變。source archive、套件、重現腳本均隨附，可離線重跑。

| 本次執行 | run/pass/fail | 結果／限制 |
|---|---:|---|
| 初始aud4-auth單組 | 17/17/0 | [auth-initial.log](evidence/auth-initial.log) |
| 初跑Member＋AUD4 | 111/107/4 | [保留失敗](evidence/member-aud4-initial.log)：四個SSR child找不到react，屬本次loader問題 |
| 修正loader後Member＋AUD4 | **111/111/0** | [重跑](evidence/member-aud4.log)，涵蓋九修補／原M1 |
| 初跑focused | 83/73/10 | [保留失敗](evidence/focused-initial.log)：同loader影響渲染子程序 |
| 修正loader後focused | **83/83/0** | R3-R1/AUD3/ADV |
| N選集 | **43/43/0** | 本次命令選出的43，不冒稱團隊42原命令逐一相同 |
| Enter group5 | **3/3/0** | 無完整geometry驗證 |
| auth＋worker | **83/83/0** | 含stored SIWE/session/cookie/nonce/解析等 |
| 獨立P1–P8、P9 | **8＋1情境，斷言全過** | 自寫腳本非node:test case計數；具體事件見各log |
| 獨立quota矩陣＋no-op/rename | **36＋1情境，斷言全過** | 控制／自然排程、分鐘邊界另在P4 |

上述node:test組 cancelled/skipped/todo均0；pattern未選case不算已執行。[runs.json](evidence/runs.json)與[reruns.json](evidence/reruns.json)保存命令、UTC開始／結束與exit，重跑不刪除首次失敗。兩個公開throwing stubs只讓非幾何import可達，並未發明場景或完成browser proof。首次缺`python`改用`python3`、web fetch失敗改用immutable archive等工具準備不屬产品測試結果。

**團隊紀錄（本次未重跑全套）：**private **1087/1087**、tsc/frontend build pass；public no-stub **239/235/4**；FIRST with-stub **419/414/5**。失敗包括withheld geometry/preview/private history與首次presence timing；單獨timing **1/1**重跑不能抹除首次失敗。public tsc **16 diagnostics／exit2**，沒有完整public frontend build。團隊focused83/83、N42/42、Enter3/3、Member＋AUD4含M1-R2 111/111是另一批執行。詳細原始紀錄保存在附帶snapshot的R5/logs與[固定TEST_RESULTS](https://github.com/tungweb3/imd-ember-world-review/blob/357668f37c75317f79ff2266795636597a707c04/R5/TEST_RESULTS.md)。

本次未重跑public全套、tsc、frontend build、Wrangler Worker build或fresh workerd D1，也未執行private tests；不可把缺依賴／歷史失敗改報通過。本次主要獨立證據為公開handler/client／真migration SQL的SQLite測試與碼讀。

## 部署比較：團隊證據支持對應，獨立production裁決仍有限

[BUILD_EVIDENCE](https://github.com/tungweb3/imd-ember-world-review/blob/357668f37c75317f79ff2266795636597a707c04/R5/BUILD_EVIDENCE.md)記錄：public/private Worker均 **309594 bytes**，SHA-256 **c7d7c0fbe49ce601a187bafdf7480c40d64ceda7bcfde64b9aea3f63f809811c**。本次未取得bundle重建比對，此處是團隊build證據，不能寫成親自重建。

團隊記錄 `20261003T174551Z-54410b2`，部署來源54410b2，新Worker **e491cb71-60ec-4cfe-9db7-b88e52d78ce9**；開始17:45:51.193Z，完成17:48:17.618Z，post-deploy traffic查詢為100%。[PRODUCTION_D1](https://github.com/tungweb3/imd-ember-world-review/blob/357668f37c75317f79ff2266795636597a707c04/R5/PRODUCTION_D1.md)列0001–0006＋0008已套用、六個schema名稱/type/SQL讀回相符；**沒有0007**。這是團隊清理過的production證據，raw readback／備份未提供，本次沒有存取其帳戶。

團隊fresh local Wrangler D1 final0008五次接受、第六次trigger拒絕、再讀五筆；它不是production併發證據。schema存在也不證明route已在production承受上述競態、cron已執行或binding接到預期DB。

團隊LIVE_MATCH在 **2026-10-03T17:49:09.683Z–17:49:14.844Z** 的五個匿名GET均200：首頁、`/assets/index-CIkdCwRI.js`、`/assets/InteriorView-B7dudNwf.js`、`/assets/index-BZpalHf7.css`、`/api/auth/session`；四靜態hash、24項headers相符，session signedIn:false/no-store，無Set-Cookie。完整URL/hash/header在固定R5/LIVE_MATCH.json及deployment record。**本次選擇不做optional live GET，正式請求數0**；沒有登入、wallet、寫入、部署或DB操作。

舊`acdbb2bd`／`ddb10e2`只證明舊版本，不能用來證明本修補部署。新團隊紀錄比舊證據更相關，但匿名GET不測repaired authenticated routes，不涵蓋102個dist檔或完整WorldApp/browser。3D、textures、scenes、interiors、完整WorldApp與私有history withheld，因此即使Worker一致仍非完整前端可重現。

## 待回答與交付界線

仍需獨立production/runtime證據的問題包括：D1 batch/RETURNING與高並發實際排程、0008接線與錯誤包裝、cron backlog與限額、WAF/bindings/limiter拒絕計法、上游failure、真provider事件／cookie晚到，以及完整React/WorldApp lifecycle。這些是未知，不是本報告發現的可利用漏洞，也不因團隊宣稱部署而自動關閉。

離線重現包已在另一個空白scratch目錄以`--offline --smoke`路徑解包、驗證17個套件並執行no-op競態，exit0（[結果](evidence/offline-smoke.log)）；這只驗證隨附依賴足以執行該探測，並非再次重跑所有測試。

本報告與[證據／離線重現README](README.md)交付完成只代表輸出完整可檢查；Low／Info、fixed locally或Completed／accepted **均不是認證、批准、零漏洞宣告或資金安全證明**。
