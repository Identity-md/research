# IMD Ember World — 第十次 Audit9 來源閉合審查報告（World／Member M1）

| 項目 | 值 |
|---|---|
| 候選公開 pin | https://github.com/tungweb3/imd-ember-world-review/tree/c2f21a9ef9e1a093ed2c5808f8a99e4751fde643 |
| 前一公開 pin（Audit9 審查對象） | `347268a7ecae700088547c2402db9a3eb07a6fd2` |
| 私有來源出處（不可公開檢出） | `a2e6aca828858730cfb6b60931abea20ba9b6ab6`；TEAM 測試投影 `59dfc4a90a52de181c1420f0babe6170c1dc08d7` |
| 控制性前次稽核 | Audit9，job `d76a2a79-7394-420a-99d2-df2ba6a23f45`，2026-10-05 04:30:23.485 UTC：https://github.com/Identity-md/research/blob/911652a2b1a7ab7be7d16bc37d97ab9376028fe6/jobs/d76a2a79-7394-420a-99d2-df2ba6a23f45/files/AUDIT.md |
| REVIEWER 環境 | Linux 6.8.0-124-generic，2 CPU，Node v24.21.0，npm 11.19.0，鎖定 viem 2.56.9；2026-10-05 |
| 審查性質 | 離線／本機合成測試；無正式環境呼叫、無真實錢包／簽章、無部署 |

---

## 一、執行摘要

**問題：**此候選版本是否在不重新打開先前 Auth／ownership／artifact 邊界的前提下，閉合 Audit9 的 3 項 Low＋2 項 Info 來源阻斷項，以及兩個相鄰反例（重啟早點擊、輸入父目錄 junction 別名）？

**結論：SOURCE-CLOSURE = BLOCKED（窄範圍、Info 級）；RELEASE-READINESS = UNKNOWN。**

REVIEWER 從公開 pin `c2f21a9…` 全新檢出，按指定四個指令執行。`npm ci --ignore-scripts` 與 `node scripts/review-tests.mjs --check` 皆 exit 0（25 個檔案、viem 2.56.9）；`node scripts/verify-artifact-closure.mjs` exit 0、19/19。143 個來源檔的 SHA-256 與 `manifests/submission10-published-source.json` 完全一致（127 exact／16 masked／57 遮罩行），五個修補檔均為 exact。以「同評估器」把新測試與新驗證器疊加到 `347268a` 的弱版本，REVIEWER 精確重現 TEAM 的校準數字：64 項中 40 通過／24 斷言失敗、驗證器 14/19、5 項 `ERR_ASSERTION`、exit 1、0 個 EPERM。這證明新測試並非空洞。

逐項審視原始碼與獨立探針：Low1（D1 等待後以即時時鐘判定 24h 資格與 lane）、Low2（同一 client 重啟後以第一個 fenced 回覆重設公開帳號）、Low3（舊 lifetime 的 retained owner 不再取得新 lifetime 的帳號切換授權）、Info4（`--minimize` 改走驗證過的 artifact writer）、Info5（路由前綴檔名不再繼承豁免）——Audit9 原始反例在本候選版皆不再成立，兩個相鄰反例亦已閉合，且未見 Auth／ownership／artifact 既有邊界被重新打開。

然而有兩項可歸因的問題，使 REVIEWER 無法給出 PASS：

1. **N2（Info，測試證據可靠性）**：指定的必要指令 `npm run test:review` 並非穩定 exit 0。REVIEWER 五次完整執行中有兩次為 659 項中 658 通過／1 失敗、exit 1，失敗的皆是正式回歸 `Audit9 LOW2 restart observing B followed by genuine B-to-A change…`（`tests/auth-audit9.test.mjs:69`，`undefined !== 204`）。單檔重跑 30 次失敗 8 次。根因是測試以固定 `flush(40)` 等待一個真實非同步的 logout 完成；改為等待完成後 40/40 通過。來源行為正確，但 TEAM 的「659/659、零失敗」在本環境不可穩定重現。
2. **N1（Info，Low1 相鄰、本次修補新使其可達）**：D1 讀取後若注入的即時時鐘為 `Infinity`，新的 `laneNow`（`server/ownership.ts:351-352`）使所有離線席位都「不計入」，因而進入 index lane。`server/auth.ts:759-769` 的 lane 沒有檢查時鐘是否有限，會把 `REAL Inf` 寫入 `index_lanes.at` 與 `index_lane_probes`。之後以正常有限時鐘在 +10 分鐘及 +60 分鐘發出的請求，該網路的 lane 始終無法再取得，持續回傳 `recheck:"limited"`。同樣的注入在 `347268a` 不會留下任何列；`NaN` 與有限時鐘對照則都能恢復。此問題不會產生錯誤的所有權授權（回應仍誠實標示 limited），而且正式環境的 `Date.now()` 一般為有限值。但任務明確要求驗證「rollback／NaN／Infinity 與之後的恢復」，此反向控制未完全成立。

另有兩項不阻斷的觀察：重啟時初始回覆被扣住期間若明確登出，該回覆會被 gen fence 丟棄，公開帳號停在 `null`，屬保守 UI 失準；路徑遮罩對「數字緊鄰的 `/home/...`」與 `~/...` 不做遮罩，這是既有政策，不在路由前綴範圍內。

**解除阻斷的最小條件（推論）：**正式回歸改以 `until(()=>logouts(q).every(e=>e.finished))` 等待；在 `laneNow` 或 lane 內對非有限時鐘 fail-closed，不保留 lane；然後重新量測。

本報告不是認證、背書、零漏洞或資金安全證明。通過測試與 Low／Info 標籤皆不構成這類保證。

---

## 二、五項閉合矩陣（＋相鄰反例）

| Audit9 項目 | 等級 | 候選版修補位置（exact pin） | REVIEWER 獨立結果 | 判定 |
|---|---|---|---|---|
| **Low1** D1 等待後資格／lane 使用請求開始時間 | Low | [`server/ownership.ts:351`](https://github.com/tungweb3/imd-ember-world-review/blob/c2f21a9ef9e1a093ed2c5808f8a99e4751fde643/source/server/ownership.ts#L351)、[`:352`](https://github.com/tungweb3/imd-ember-world-review/blob/c2f21a9ef9e1a093ed2c5808f8a99e4751fde643/source/server/ownership.ts#L352)、[`:357-359`](https://github.com/tungweb3/imd-ember-world-review/blob/c2f21a9ef9e1a093ed2c5808f8a99e4751fde643/source/server/ownership.ts#L357-L359) | Audit9 原序重跑：延遲 0/1/2/5000ms，sighting 年齡分別為 86399999/86400000/86400001/86404999，first 與 next 都是 1/1/0/0；`checkedAt` 維持 t；index／budget／ownerOf 各 1；presence 列不變；exit 0。lane 三種變體、29999/30000/30001ms、rollback／NaN 均符合預期。**`Infinity`＋已准入 lane 會持久化 `Inf` 列，之後無法恢復（N1）** | **原始反例 CLOSED；Infinity 恢復子控制 PARTIAL（N1 OPEN, Info）** |
| **Low2** 重啟後保留前一 lifetime 帳號 | Low | [`src/world/auth.ts:264`](https://github.com/tungweb3/imd-ember-world-review/blob/c2f21a9ef9e1a093ed2c5808f8a99e4751fde643/source/src/world/auth.ts#L264)、[`:283`](https://github.com/tungweb3/imd-ember-world-review/blob/c2f21a9ef9e1a093ed2c5808f8a99e4751fde643/source/src/world/auth.ts#L283)、[`:284-285`](https://github.com/tungweb3/imd-ember-world-review/blob/c2f21a9ef9e1a093ed2c5808f8a99e4751fde643/source/src/world/auth.ts#L284-L285)、[`:293-297`](https://github.com/tungweb3/imd-ember-world-review/blob/c2f21a9ef9e1a093ed2c5808f8a99e4751fde643/source/src/world/auth.ts#L293-L297) | Audit9 原序：重啟後 account=B、session=A、`mismatch`、列不變；點擊後真實 B 授權與簽章，以 address 斷言 logout A（204）。locked：account=null／cookie A 保留／0 logout。相鄰早點擊（TEAM 測試）通過。B→A 清理正確，但其正式測試不穩定（N2） | **CLOSED（來源）；正式回歸 flaky（N2 OPEN, Info）** |
| **Low3** 舊 lifetime retained owner 撤銷新 lifetime 的 A | Low | [`src/world/auth.ts:595-599`](https://github.com/tungweb3/imd-ember-world-review/blob/c2f21a9ef9e1a093ed2c5808f8a99e4751fde643/source/src/world/auth.ts#L595-L599) | Audit9 原序：首次 accountsChanged(C) 後 A 的 `revoked_at=NULL`、0 個 address logout、`mismatch`；B 的 nonce 專屬清理稍後完成（B 被撤銷，204）；延遲的 clear-cookie 標頭清除共享 cookie，但 A 的 SQLite 列仍有效（屬已接受邊界）；C→D 由 TEAM 測試覆蓋 | **CLOSED** |
| **Info4** 重播 CLI `--minimize` 繞過 artifact store | Info | [`scripts/replay-auth-trace.mjs:16-24`](https://github.com/tungweb3/imd-ember-world-review/blob/c2f21a9ef9e1a093ed2c5808f8a99e4751fde643/source/scripts/replay-auth-trace.mjs#L16-L24)、[`:34`](https://github.com/tungweb3/imd-ember-world-review/blob/c2f21a9ef9e1a093ed2c5808f8a99e4751fde643/source/scripts/replay-auth-trace.mjs#L34)、[`:39`](https://github.com/tungweb3/imd-ember-world-review/blob/c2f21a9ef9e1a093ed2c5808f8a99e4751fde643/source/scripts/replay-auth-trace.mjs#L39) | 懸空 final link：`ARTIFACT_REJECTED`，外部目標未建立，link 仍在。目錄別名使輸出等於輸入、或別名輸入加真實輸出：都 `ARTIFACT_REJECTED`，輸入 20226 bytes 與雜湊不變。經別名讀入並另寫輸出：成功，輸出雜湊 `683ba5e0…`，兩個輸入視圖不變。hardlink、tmp 外路徑、命名空間外檔名、預設重播（不寫檔）皆正確 | **CLOSED（本機受控根假設下）** |
| **Info5** 路由前綴檔名未遮罩 | Info | [`tests/auth-artifacts.mjs:17`](https://github.com/tungweb3/imd-ember-world-review/blob/c2f21a9ef9e1a093ed2c5808f8a99e4751fde643/source/tests/auth-artifacts.mjs#L17) | 實際寫檔後讀回：18 種 quoted／bare／巢狀／key／後綴變體全部遮罩為 `[local-path]`；8 種 exact route／query／subroute／URL／相對 ID／動作字串原樣保留；trace 結構不變 | **CLOSED**（`2/home/…`、`~/…` 屬既有政策＝accepted-limit） |
| 相鄰：重啟早點擊 | — | `auth.ts:264`、`:285`（`g!==this.gen`） | TEAM 正式測試（different-account／locked）在全部 REVIEWER 執行中通過；P1 原序探針一致 | **CLOSED** |
| 相鄰：輸入父目錄 junction 別名 | — | `replay-auth-trace.mjs:16,19`＋store 父鏈驗證 [`auth-artifacts.mjs:64`](https://github.com/tungweb3/imd-ember-world-review/blob/c2f21a9ef9e1a093ed2c5808f8a99e4751fde643/source/tests/auth-artifacts.mjs#L64) | Linux 目錄 symlink 版本重現如上；未測真實 Windows junction | **CLOSED（Linux）；Windows junction 為 UNKNOWN** |

---

## 三、分離判定

### SOURCE-CLOSURE：**BLOCKED**（窄範圍，均為 Info 級）

- Audit9 五項原始反例與兩個相鄰反例：在 REVIEWER 重現中**皆已不成立**，也未觀察到已關閉的 Auth／ownership／artifact 邊界被重新打開。
- 阻斷理由：(a) **N2**：必要指令 `npm run test:review` 在 REVIEWER 環境為 2/5 次 exit 1，TEAM 所稱「正向執行 exit 0、零失敗」無法穩定重現。(b) **N1**：Low1 明列的 `Infinity` 與之後恢復的反向控制失敗，而且這條路徑是本次修補新使其可達。
- 這兩項都**不是**已證實的授權繞過、錯誤所有權授予、M1 未授權寫入或資金風險。若需方把 N2 視為純環境問題並接受 N1 為邊界，其餘證據會支持「有界閉合」；但依任務規則，REVIEWER 不推定 PASS。

### RELEASE-READINESS：**UNKNOWN**

此來源未部署（`BUILD_DEPLOYMENT.json`：`deploymentPerformedByThisSubmission:false`、`servedProductionVersion:null`）。以下項目皆未量測：正式 Cloudflare、瀏覽器／provider／cookie 旗標、ERC-1271、M1 寫入授權、D1 交錯、WAF／limiter、上游、程序死亡、跨 isolate。公開選集的 `tsc --noEmit` 為 exit 2（14×TS2307 缺少被保留的前端模組、1×TS7006），完整前端建置證據不可得，不能視為通過。

---

## 四、發現（依嚴重度排序；含相鄰案例）

### N1 — Info｜非有限即時時鐘會持久化 lane 保留，使該網路之後的 lane 無法恢復（OPEN）

- **位置**：[`server/ownership.ts:351-352`](https://github.com/tungweb3/imd-ember-world-review/blob/c2f21a9ef9e1a093ed2c5808f8a99e4751fde643/source/server/ownership.ts#L351-L352)（`laneNow` 未檢查有限值）；[`server/auth.ts:759-769`](https://github.com/tungweb3/imd-ember-world-review/blob/c2f21a9ef9e1a093ed2c5808f8a99e4751fde643/source/server/auth.ts#L759-L769)（`t=clock(deps)` 直接傳入 `reserveIndexProbe` 與 `INDEX_LANE`）；清理用的 [`server/presence.ts:51`](https://github.com/tungweb3/imd-ember-world-review/blob/c2f21a9ef9e1a093ed2c5808f8a99e4751fde643/source/server/presence.ts#L51) `DELETE FROM index_lanes WHERE at<?1` 永遠不會刪除 `Inf`（推論）。
- **事件順序**：登入（challenge／verify 各 1）→ 席位 7 離線、sighting 年齡 86399999ms → index 預算拒絕、lane 允許 → D1 sightings 讀取後時鐘設為 `Infinity` → `counts(...,Infinity)=false` → 呼叫 `req.lane()` → 寫入 probe 與 lane → `proof()` 因 `proofNow` 非有限而丟出 `OwnershipUnavailable`，被捕捉 → 最終回應 503 → 時鐘恢復為 t+600000、t+3600000。
- **預期**：非有限時鐘 fail-closed（503），不保留 lane；之後的有限時鐘請求可重新取得 lane。**實際**：`index_lanes(net:unknown,NULL,at=REAL Inf)`、`index_lane_probes(scope_key "net:unknown|", probed_at=Inf, expires_at=Inf)`；+10m 與 +60m 皆為 `200 recheck:"limited" eligible:0`。lane key 只有 1 次（對照組為 3 次）；index 0（對照組 3）；budget 3；ownerOf RPC 3。
- **對照**：同一腳本在 `347268a` 上 exit 0（無列，lane 2 次，可恢復）；候選版 NaN 與有限時鐘對照組都能恢復。
- **授權影響**：無錯誤授權，回應誠實標示 limited。影響限於該 network scope 的 lane 可用性。正式環境 `Date.now()` 一般有限，因此可達性屬 UNKNOWN／低（推論）。
- **TEAM 測試缺口**：[`tests/ownership-audit9.test.mjs:136-144`](https://github.com/tungweb3/imd-ember-world-review/blob/c2f21a9ef9e1a093ed2c5808f8a99e4751fde643/source/tests/ownership-audit9.test.mjs#L136-L144) 只斷言 status、index、rpc、budget，未斷言 lane key 次數、持久化列或之後的恢復。

### N2 — Info｜正式回歸 `Audit9 LOW2 restart observing B…` 不穩定，必要指令非確定性 exit 1（OPEN；測試證據，非產品行為）

- **位置**：[`tests/auth-audit9.test.mjs:65`](https://github.com/tungweb3/imd-ember-world-review/blob/c2f21a9ef9e1a093ed2c5808f8a99e4751fde643/source/tests/auth-audit9.test.mjs#L65)（`p.switchTo(A);await flush(40)`）；失敗於 [`:69`](https://github.com/tungweb3/imd-ember-world-review/blob/c2f21a9ef9e1a093ed2c5808f8a99e4751fde643/source/tests/auth-audit9.test.mjs#L69)。`flush` 定義見 `tests/auth-r7-fixtures.mjs:19-20`，即 40 次 `setImmediate`。
- **錯誤**：`Expected values to be strictly equal: undefined !== 204`（`ERR_ASSERTION`，`failureType: testCodeFailure`）。
- **失敗時的診斷**：client account=A、session=null、`known:false`。logout POST 已送出（`addressAssertion:true`、`nonceAssertion:false`），但尚未 finished。cleanupPlans 為 `[{1,stop,none},{2,account-switch,displayed-session}]`。SQLite 兩列皆 live（A `c94fa99d…`、B `ec917efc…`，`revoked_at NULL`）。計數：prompt 0／connect 0／challenge 0／verify 0／session 2／home 0／logout 1／index 2／rpc 0。
- **頻率**：完整 `npm run test:review` 5 次中 2 次 exit 1（658/659）；單檔 30 次中 8 次失敗。
- **來源行為**：改為等待 logout 完成的 40 次變體全部通過（B 撤銷、A 保留、1 次 signed-out 廣播、0 prompt）。其中 13/40 次在 `flush(40)` 當下 logout 尚未完成。**判斷為測試等待競態，非來源缺陷**（推論：Worker 的 WebCrypto／SQLite 非同步時間超過 40 個 macrotask）。
- **影響**：TEAM 的「supported 659/659、零失敗、exit 0」在 Linux／Node 24.21.0 不可穩定重現。TEAM 量測環境是 win32／Node v24.19.0，且只記錄單次執行，未提供重複執行資料。

### N3 — Info／accepted-limit｜重啟時初始回覆被扣住期間明確登出，公開帳號停在 null（不阻斷）

- [`auth.ts:285`](https://github.com/tungweb3/imd-ember-world-review/blob/c2f21a9ef9e1a093ed2c5808f8a99e4751fde643/source/src/world/auth.ts#L285) 的 `g!==this.gen` 會丟棄任何 gen 遞增之後才到的回覆，登出也包括在內。實測：錢包授權 B，最終 account=null、session=null、`visitor`；logout 1、廣播 1、prompt 0。方向保守（權限較少），只有 UI 失準，直到下一次 accountsChanged 或重新綁定才更新。

### N4 — accepted-limit｜路徑遮罩的既有前綴政策

- `2/home/user/secret.txt`、`err:2/home/u/x`、`~/secret/file.txt` 在候選版與 `347268a` 都不遮罩。原因是 lookbehind `(?<![A-Za-z0-9._~%+\\/-])` 把它們視為相對識別碼（[`auth-artifacts.mjs:9`](https://github.com/tungweb3/imd-ember-world-review/blob/c2f21a9ef9e1a093ed2c5808f8a99e4751fde643/source/tests/auth-artifacts.mjs#L9)）。這不屬於 Audit9 #5 的路由前綴範圍；合成檔名也不代表正式環境資料外洩。

### 已接受邊界（非發現）

- Low3 的延遲 clear-cookie：B 的 nonce 清理請求帶著 cookie B，於事後完成（`server/auth.ts:629-651` 以 token＋nonce 比對），其 `Set-Cookie` 清除了共享 jar 中後來寫入的 A cookie。A 的 SQLite 列仍為 `revoked_at NULL`，client 依 canonical `/api/auth/session` 顯示 `signedIn:false`，舊 callback 沒有把 B 安裝進新 UI。這與任務所述「分離 A 的 live 列與共享 cookie」一致。
- Info4 依賴本機受控根：不保證對抗性並行祖先替換，也不保證 SMB／NFS（驗證器 `limits` 亦如此聲明）。

---

## 五、證據分類

| 類別 | 內容 |
|---|---|
| **REVIEWER 重現** | 第六節 A–H 的全部指令、exit code、計數與探針；N1、N2、N3 |
| **TEAM 量測（未獨立重現）** | private full 1709/1709；fresh private 659/659；win32 能力批次 artifact 28/28；EPERM 歷史（一般 Windows 環境 23/28、14/19，各 5 項 EPERM）；`retryHistory[0]`（WinError267 cwd 錯誤後重試）；`tsc` 與私有建置 exit 0；批次完成於 2026-10-05T14:04:44.131075Z |
| **TEAM 量測（REVIEWER 已重現）** | 基線 64→40/24、驗證器 19→14/5、exit 1、無 EPERM；驗證器 19/19；公開 143 個檔案的雜湊 |
| **歷史** | Audit9 原文（35419 bytes，SHA256 `8b71346eaeb6b6abdb6e50f1290d3ceaf368eb1e28e32e138c4ad603a94bb0b0`，已核對）；Report9 的有界通過不推翻 Audit9；613/613、13/13 屬舊總數 |
| **推論** | N1 中 `Inf` 永不被 prune；N2 的時序根因；N1 在正式環境可達性低 |
| **不可得／UNKNOWN** | 私有 `a2e6aca…`／`59dfc4a…` 位元組（只能比對公開 manifest）；Windows 真實 junction／file-symlink；完整前端建置；正式環境的一切；外部 Swarm 結果 |

---

## 六、證據附錄

### A. 檢出與出處

```text
git clone https://github.com/tungweb3/imd-ember-world-review.git && git checkout c2f21a9ef9e1a093ed2c5808f8a99e4751fde643
c2f21a9… 2026-10-05 22:26:01 +0800 (=14:26:01 UTC) "Submission10 Audit9 source fixes and measured closure evidence"
parent 347268a7ecae700088547c2402db9a3eb07a6fd2
git diff --stat 347268a c2f21a9：30 files，source 變更：server/ownership.ts(10) src/world/auth.ts(21) scripts/replay-auth-trace.mjs(34)
  tests/auth-artifacts.mjs(4) scripts/verify-artifact-closure.mjs(109) scripts/review-tests.mjs(3)
  新增 tests/auth-audit9.test.mjs(203) tests/ownership-audit9.test.mjs(158)；其餘為文件／測試
```

時間軸：Audit9 於 04:30:23.485 UTC 完成 → 私有來源凍結 10:07:04 UTC（任務陳述）→ manifest `generatedAtUtc` 為 2026-10-05T10:17:18.719829Z → TEAM 批次完成 14:04:44 UTC → 公開 commit 14:26:01 UTC。公開 commit 晚於量測，與「僅文件／checksum 差異」的說法相容，但 REVIEWER 無法直接比對私有位元組。

Manifest 核對（REVIEWER）：
```text
sha256 manifests/submission10-published-source.json = 6e22edd28321251cff9ec4d9f9eb853eb23010433f3e8b28dfc4194de36eccc6（等於 SOURCE_MANIFEST.selectedManifestSha256）
checked 143 bad 0 missing 0；git ls-files source = 143，全部在 manifest 中
policy: exact 127 / redacted 16；preserved_mask_lines 合計 57
server/ownership.ts           exact 858cdfc9eec304e2c15b7f7b1ae66f846a9677c87a91c4333f56dd607abce207
src/world/auth.ts             exact 07afd30b8dcd8b1b1d74f3a8940f2f4d9a7037b06246911290ec8392f968275b
scripts/replay-auth-trace.mjs exact 7e36564374a25abe61b22b7a74c5705feb186f1a8b1e77f3859de0d3a157d408
tests/auth-artifacts.mjs      exact af7e838ffa6cbd835a118c1e62b085ed15d5d2475d4e7663ce23668503db0d50
scripts/verify-artifact-closure.mjs exact f2b1bcc991c2a0c85d0d3516ecdf82ca63d26b04701e6d6a85745a3cd70e6193
server/auth.ts 6077402849c4da2423b8cd00b8625afd4bb50aa0f5248a2566e6476d71057ead；server/presence.ts 61ea5ae25d38dd4572cc0d987fdc2746161dc77c7f8b23758c0f5745de0efe81
tests/auth-audit9.test.mjs b4badef8c93f48aba928ed4f93e559e768efccb6795d1ce12cd494aa2767e66a；tests/ownership-audit9.test.mjs 38ab56bdffa2ad7b85e656a7c7047b689ae3e4536f7326c0830d617090d91c66
```
被遮罩的 16 個檔案包括 `server/member.ts`（4 行）與 `migrations/0006_members.sql`（10 行）。五個修補檔皆為 exact。

### B. 必要指令（REVIEWER，source/）

```text
$ npm ci --ignore-scripts                    → exit 0（added 79 packages, audited 80；TEAM 記錄為 78 packages、--offline 安裝，差異未對帳，lock 相同）
$ node -e "require('viem/package.json').version" → 2.56.9
$ node scripts/review-tests.mjs --check      → exit 0
  REVIEW_PREREQUISITES {"node":"v24.21.0","viem":"2.56.9","testFiles":25}
$ npm run test:review   (#1) → exit 1  tests 659 pass 658 fail 1 cancelled 0 skipped 0 todo 0  duration_ms 65039
                          not ok 93 - Audit9 LOW2 restart observing B followed by genuine B-to-A change cleans displayed cookie B once
                          error: Expected values to be strictly equal: undefined !== 204  (tests/auth-audit9.test.mjs:69:12)
                        (#2) → exit 1  659/658/1，同一測試
                        (#3) (#4) (#5) → exit 0  659/659/0, cancelled 0 skipped 0 todo 0
$ node scripts/verify-artifact-closure.mjs   → exit 0
  {"status":"PASS","node":"v24.21.0","platform":"linux","artifactModuleSha256":"af7e838f…","replayCliSha256":"7e365643…",
   "assertions":{"total":19,"passed":19,"failed":0,"skipped":0}}
  limits: "Local filesystem; no NFS/SMB exclusivity claim." / "Node has no portable dirfd/openat … ancestry swaps remain outside the private fixture-root trust assumption."
```
沒有使用 shim、選擇器或替代模組，也沒有略過或刪除失敗測試。無 cancel／skip／todo。沒有重試被當作通過：所有執行皆如實記錄。

REVIEWER 本機 log 雜湊（未發布，含本機路徑）：review.log `43cd6e9a…`、review2.log `b9651225…`、verifier.log `4dc15748…`。

### C. 同評估器弱基線（REVIEWER）

做法：在 `347268a` 檢出上只覆蓋 `tests/auth-audit9.test.mjs`、`tests/ownership-audit9.test.mjs`、`tests/auth-artifacts.test.mjs`、`scripts/verify-artifact-closure.mjs`（取自 `c2f21a9`），產品實作保持不變；`package-lock.json` 與候選版相同。

```text
node --test ownership-audit9 auth-audit9 auth-artifacts → exit 1  tests 64 pass 40 fail 24 cancelled 0 skipped 0 todo 0；EPERM 0
  ownership-audit9 25: 17/8（Low1 2ms、5000ms、online、refused／failed／successful lane、second read、29999ms）
  auth-audit9      11:  3/8（LOW2 ×3 restart、B-to-A、LOW3 first-observation／current-switch、early-click ×2）
  auth-artifacts   28: 20/8（CLI dangling／existing／nonregular／parent alias／outside／input overwrite／input-dir alias；route-prefix）
verify-artifact-closure → exit 1  total 19 passed 14 failed 5 skipped 0，全部為 ERR_ASSERTION：
  H-C1 "CLI must not create a dangling link target true !== false"；H-C2；H-C3（EISDIR from writeFileSync）；
  H-C5 "the canonical replay input must survive an aliased input/output collision"；H-S4（/api/auth/session.log 等未遮罩）
```
結果與 TEAM `calibrationHistory.baselineFrozenEvaluator` 一致（64:40/24；19:14/5；`capabilityErrors: None`）。

### D. Low1 重現

Audit9 #1 腳本只改兩處：把中間斷言改為預期值、改用精簡輸出。腳本 SHA256 `20ac207fce47479af048f5f2ac1f928b901531abafe62e95a718a1a3d1fd32d0`，候選版 exit 0：
```text
delay 0    age 86399999 first 1 next 1 checkedAt 1790596800000 index1 budget1 rpc1 prompt0 logout0 hint0
delay 1    age 86400000 first 1 next 1
delay 2    age 86400001 first 0 next 0
delay 5000 age 86404999 first 0 next 0
seat_presence=(7,0x19e7e376e7c213b7e7e7e46cc70a5dd086daff2a,1790510400001,1790510400001) 不變
```

N1 重現（`repro-n1.mjs`，SHA256 `62b5361f9e20064ade2125160c232a742d1107a0a914e684e2e400cfeaf65ee8`，以 `node --input-type=module` 從 source/ 執行）：

```js
import assert from 'node:assert/strict';
import {setup,newAccount,fakeImd,fakeChain} from './tests/wallet-harness.mjs';
import {ONLINE_WINDOW_MS} from './server/ownership.ts';
const results=[];
for(const change of ['Infinity','finite+2ms']){
  const acct=newAccount(),a=acct.address.toLowerCase(),owners=[];owners[7]=a;
  const w=setup({chain:fakeChain({owners:{7:a}}),imd:fakeImd({seats:{7:'707'},owners,online:[]})}),b=w.browser();
  const keys=[];w.env.CHAIN_LIMITER={limit:async({key})=>{keys.push(key);return {success:key!=='chain:index'};}};
  assert.equal((await b.signIn(acct)).verify.status,200);
  const at=w.clock.now(),seen=at-ONLINE_WINDOW_MS+1;
  w.db.raw.prepare('INSERT INTO seat_presence(token_id,owner,last_online_at,updated_at) VALUES(7,?,?,?)').run(a,seen,seen);
  const prepare=w.db.prepare.bind(w.db);let once=true;
  w.db.prepare=sql=>{const wrap=s=>({...s,bind:(...x)=>wrap(s.bind(...x)),all:async()=>{const r=await s.all();
    if(once&&sql.startsWith('SELECT token_id,last_online_at')){once=false;if(change==='Infinity')w.clock.set(Infinity);else w.clock.advance(2);}return r;}});return wrap(prepare(sql));};
  const get=async()=>{const r=await b.get('/api/me/home');const body=await r.json();await Promise.all(w.kept);return {status:r.status,recheck:body.recheck,eligible:body.eligible,error:body.error};};
  const first=await get();
  const stored={lanes:w.db.raw.prepare('SELECT typeof(at) t,CAST(at AS TEXT) at FROM index_lanes').all(),
    probes:w.db.raw.prepare('SELECT CAST(probed_at AS TEXT) p,CAST(expires_at AS TEXT) e FROM index_lane_probes').all()};
  w.clock.set(at+600000);const later=await get();w.clock.set(at+3600000);const later60=await get();
  const r={change,first,stored,later10m:later,later60m:later60,laneKeys:keys.filter(k=>k==='chain:index:lane').length,
    index:w.chain.state.calls.filter(c=>!c.body).length,rpc:w.chain.state.calls.filter(c=>c.body).length};
  console.log(JSON.stringify(r));results.push(r);
}
assert.equal(results[1].later10m.recheck,undefined,'finite control recovers');
assert.equal(results[0].later10m.recheck,undefined,'a non-finite live clock must not persist a lane reservation that denies later finite-clock recovery');
```

```text
候選版 c2f21a9 → exit 1
{"change":"Infinity","first":{"status":503,"error":"OWNERSHIP_UNAVAILABLE"},"stored":{"lanes":[{"t":"real","at":"Inf"}],"probes":[{"p":"Inf","e":"Inf"}]},
 "later10m":{"status":200,"recheck":"limited","eligible":0},"later60m":{"status":200,"recheck":"limited","eligible":0},"laneKeys":1,"index":0,"rpc":3}
{"change":"finite+2ms","first":{"status":200,"eligible":0},"stored":{"lanes":[{"t":"integer","at":"1790596800002"}],…},"later10m":{"status":200,"eligible":0},…,"laneKeys":3,"index":3,"rpc":3}
AssertionError: a non-finite live clock must not persist a lane reservation … + 'limited' - undefined
基線 347268a → exit 0
{"change":"Infinity",…"stored":{"lanes":[],"probes":[]},"later10m":{"status":200,"eligible":0},…"laneKeys":2,"index":2}
{"change":"finite+2ms","first":{"status":200,"recheck":"limited","eligible":1},…}   ← 原始 Low1 缺陷（eligible 1）
```
同一組探針的補充結果：NaN＋admitted lane → lane 0、無列，之後可恢復。rollback → 503、lane 0。D1 延遲 +30001ms＋admitted lane → 200，新 ownerOf `checkedAt=1790596830001`（rpc 2、index 1，以 latest 重新證明，不是延長舊證明）。+30001ms＋refused lane → 503。整個過程 auth 列與 presence 列都不變。

### E. Low2／Low3 探針（REVIEWER，真實 AuthClient／Worker／node:sqlite）

```text
P1-B  (A 登入→觀察 A→stop→provider B→restart→點擊)
  restored: account 0x1563…5508(B) session 0x19e7…2a(A) status mismatch rowsSame true
  click: session B；logout [{nonceAssertion:false,addressAssertion:true,status:204}]；A revoked_at 1790596800000，B NULL
  counts: prompt1 connect0 challenge1 verify1 session4 home1 logout1 broadcast2 index2 rpc1
P1-locked: account null session A status owner rowsSame true；prompt/challenge/verify/logout/broadcast 0；session2 index1 rpc1
P2-firstC (B verify 已 commit 但回應被扣住；nonce-B 清理被扣住；stop；另一 context 寫入 cookie A；restart []；accountsChanged(C))
  mid: account C session A status mismatch addressLogouts 0 A_revoked null rowsSame true
  final: B revoked（nonce 清理 204），A revoked_at NULL；canonical {"signedIn":false}；client session null
  plans [{1,lock,reconcile,flow1},{2,stop,verify-owner,flow1}]
  counts: prompt1 challenge1 verify1 session4 home0 logout1 broadcast0 index1 rpc0
P2-noEvent: 除 account=null 外與上相同
P3 (held initial B → q.c.signOut() → release): account null session null status visitor；logout1 broadcast1 prompt0
```

### F. N2 不穩定測試

```text
for i in 1..20: node --test --test-reporter=tap tests/auth-audit9.test.mjs → 6/20 次失敗（另一輪 10 次中 2 次）；每次都是 not ok 4（檔內編號）
等待完成的變體（40 次；把 flush(40) 後改為 until(()=>logouts(q).length>0&&logouts(q).every(e=>e.finished))，其餘斷言相同）
  → tests 40 pass 40 fail 0；其中 13/40 次在 flush(40) 當下 {"n":1,"finished":false}
環境：nproc 2，loadavg 0.88 1.04 1.05
```

### G. Info4 CLI 探針（真實 Linux symlink／hardlink，根目錄在 source/tmp）

```text
輸入：runSeed(0)＋重複 worker 動作（47 actions），經 createArtifactStore 寫入；20226 bytes，sha256 b845e18c5a8df46deae199ec50556e30a4c418c8a35f0aef51c8ed6b32d40a93
C1 dangling final link → exit1 invariants [HARNESS-CAUSAL, ARTIFACT_REJECTED] "artifact output is not a regular file"；outsideCreated false；stillSymlink true
C2 alias/輸出=輸入 → exit1 [ARTIFACT_REJECTED] "artifact path cannot traverse a symlink or junction"；inputHashSame true
C3 alias 輸入、真實輸出=輸入 → exit1 [ARTIFACT_REJECTED] "minimized output must be separate from the replay input"；inputBytes 20226
C4 alias 輸入、另寫輸出 → exit1 [HARNESS-CAUSAL]（刻意的無效 trace）；minimized 為 regular file，sha256 683ba5e0d06c1c86ee74dbe1dfcc357010d271a72282d922e058550f594c2b2d（與 Audit9 #4 量測相同）；兩個輸入視圖雜湊不變
C5 hardlink 輸入作為輸出名稱 → rename 只替換目錄項；輸入雜湊不變；nlink 1
C6 source/scripts 下 → [ARTIFACT_REJECTED] "artifacts must use a child directory of source/tmp"；evil.json → [HARNESS-CAUSAL, ARTIFACT_REJECTED] "outside the scheduler namespace"
C7 預設重播（無 --minimize）→ exit1 [HARNESS-CAUSAL]；目錄內容不變（不寫檔）
```
說明：child 的 exit 1 本身既不證明拒絕，也不證明 Auth 漏洞。判定依據是 `ARTIFACT_REJECTED`、檔案存在與否，以及位元組與雜湊。觀察：命名空間檢查在最小化之後、寫入時才執行（C6 badName 先輸出 HARNESS-CAUSAL），結果仍為拒絕，屬效率而非安全問題。

### H. Info5 讀回探針

寫入 `core500-RESULT.json` 後讀回，檔案 1271 bytes，sha256 `6116d339cab0e56ea34d354f8dcac94c04e694194c57de6ef9fe3c21e8e04d50`：
```text
遮罩（皆為 [local-path]）：Cannot read /api/auth/session.log｜Error at /api/auth/verify.backup｜Error at /api/me/home.private.json｜
 "…/api/auth/session.log"｜'…/api/me/home.private.json'｜/api/auth/logout-all.json｜/api/me/home/refresh.bak｜/api/me/home?fresh=1.log｜
 /api/auth/session/../../etc/passwd｜/api/auth/session"/etc/x｜/api/auth/session;private.json｜/api/auth/session,private.json｜
 \api\auth\session.log｜file:///api/auth/session.log｜path=/api/auth/verify.backup｜x (/api/auth/session.log)｜NBSP 後綴｜JSON 內字串；物件 key 亦遮罩
保留：/api/auth/session｜GET /api/me/home?fresh=1 200｜/api/me/home/refresh｜route /api/auth/logout, then /api/auth/logout-all｜"/api/auth/challenge"｜
 https://example.com/root/project.ts｜tests/auth-artifacts.test.mjs｜nonce/action/tab 字串；trace 結構相同
未遮罩（既有政策，候選版與基線相同）：2/home/user/secret.txt｜~/secret/file.txt｜err:2/home/u/x
```

### I. 型別檢查（公開選集）

```text
node node_modules/typescript/bin/tsc --noEmit → exit 2；15 errors：14×TS2307（src/main.tsx 5、HomePanels 2、WalletPanel 1、homeEntry 2、walletView 1、vite.config.ts 3）、
1×TS7006 HomePanels.tsx(20,55)；五個修補檔 0 錯誤 → 完整前端建置證據 UNAVAILABLE，不計為通過
```

### J. TEAM 主張對照

| TEAM 主張 | REVIEWER 結果 |
|---|---|
| 25 supported files | 已重現（`testFiles:25`） |
| review 659/659、零失敗、exit 0 | **部分重現**：3/5 次成功；2/5 次 658/659 exit 1（N2） |
| verifier 19/19 | 已重現 |
| artifact 28/28 | 已重現（完整 runner 內；auth-artifacts 28 項於所有執行中通過） |
| fresh private 659/659、private full 1709/1709 | 不可得（私有） |
| 基線 64:40/24；verifier 19:14/5，exit 1，無 EPERM | 已重現 |
| EPERM／setup 重試史 | 僅文件；REVIEWER 在 Linux 上無 EPERM，Windows 能力未測 |

---

*REVIEWER 只做離線合成測試；所有身分、私鑰（`0x11…`、`0x22…`、`0x33…`、`0x44…`）皆為公開測試值。未呼叫正式端點，未使用真實錢包、簽章或資產，未部署。Accepted／completed 不等於背書或認證。*
