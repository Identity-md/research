# Report11：六項來源阻斷的窄範圍閉合評估

**SOURCE-CLOSURE：PASS（有界）；RELEASE-READINESS：UNKNOWN。** 本次本地審查支持六項機制閉合，未見直接影響的 Auth、所有權、artifact 或 Member M1 不變量倒退。這是本文依來源比對、合成反例與反向控制作出的判斷，不是把 TEAM 大量通過紀錄轉為外部認證；也不是正式環境授權。矩陣的 CLOSED 僅適用於列出的機制及受控條件。

唯一評估對象為公開 pin `35ace952824ebf711fd9fa6cb7ea1cc83b75cd6a`，以前一公開 `c2f21a9ef9e1a093ed2c5808f8a99e4751fde643` 作比較。由精確 pin 的公開封存下載來源，不建立或修改 Git；146 個 manifest 檔案、根目錄 297 個 checksum 全部吻合。私有來源 `e20f6da…` 只是出處，不能代替公開身分；16 個歷史遮罩檔的私有原始位元組仍不可核對。[來源清單][manifest]

時間依目前文件：來源凍結為 2026-10-05 18:03:59.481888 UTC，即臺北 10 月 6 日 02:03:59；manifest 產生於 18:05:20.624250 UTC，TEAM 私有量測至 18:36:12.275094 UTC。本次本地重現於同日 UTC 晚間完成，使用 Node 24.21.0、鎖定 viem 2.56.9、真正 AuthClient／Worker 與遷移建立的 SQLite，未接觸正式端點或真實身分。[目前證據][team]

歷史分歧必須保留：[Audit10][audit] 在 15:59 UTC 判定 passive discovery 仍會遺失清理責任，原 Low3 只部分閉合，並追加三項 Info；[Report10][prior] 曾判原五項反例閉合，卻因非有限 lane 時鐘及 LOW2 等待競態判來源 BLOCKED。後者的原始閉合判斷不能否定前者後續重現。本次六列逐一處理兩份報告，沒有拿 Report9 或舊命名空間的 PASS 抵銷發現。

Auth 的關鍵是責任與公開身分分離：discovery 只處理目前生命週期 owner，較強撤銷原因不再降為 lock reconciliation；失敗的原 nonce 清理仍被保留。transport／503 不表示已撤銷，也不立即無限重試；既有 restart／stop 才再觸發。因果 fence 之後的 409 可以結束責任，但它是拒絕，舊 B 與替代 A 都可能仍 live。新生命週期 canonical PRESENT 可同時存在，舊 verify callback 不可安裝身分。[清理與生命週期][authflow]

另行編寫的同地址、同到期時間探針驗證了較新 session 不會被地址等值誤認為舊 session：原 nonce 在途期間沒有第二次派送；延遲 204 撤銷舊列，較新列保留，但 clear-cookie 仍可能清除共享 jar，之後 canonical ABSENT 是正確呈現。這個已知 cookie 邊界不是跨 session 撤銷，也不能聲稱瀏覽器 cookie 時序已獲認證。[伺服器 nonce 邊界][nonce]

所有權修正只移動評估時鐘，不更新生產者日期。257 席反例中仍有效的第 257 席保留，結果誠實 partial；拒絕 index 時則 limited。public assets 在 character I/O 後判定顯示資格，公共 roster 仍非 ownership proof。非有限時鐘阻止持久化 admission，既有有限 probe 保留原三十秒退避，不退款、不刷新；回復有限時鐘後可恢復。證明逾時仍 fail closed，不能藉延遲延長權威。[排名][ranking]、[顯示][display]、[lane][lane]

先前 R5／R8／v1.1、獨立 reference scheduler 與 M1 測試均保留；reference model、scheduler driver、Member 實作、M1 migration、lockfile 相對第十版位元組未變。LOW2 只把固定等待換為實際 logout 完成且通知到達，原斷言未刪。通過這些有界排程支持無回歸的推論，不是窮盡所有並行狀態。[測試等待][low2]、[獨立模型][oracle]

尚存限制包括受控本機根、未測 Windows 真實 junction、任意非引號自由文字的遮罩語法，以及遮罩後診斷 key 碰撞只留最後值。合成路徑不證明正式資料外洩。來源 PASS 若遇到上述機制的有效反例、原斷言失敗、評估器弱化或來源不吻合，就應改為 BLOCKED／UNKNOWN；未取得的發布證據本身不等於已證實來源缺陷。[artifact 邊界][store]

World 並非全唯讀：M1 會持久化公開 profile；無 Solidity。完整前端輸入被保留，完整網站建置證據不可得，不能計為通過。Cloudflare、瀏覽器／provider／cookies、ERC-1271、M1 寫入授權、D1、WAF／limiter／upstream、process death／cross-isolate、部署身分均需另行發布證據。候選是來源審查包，沒有部署認證；completed、accepted、Low／Info 或高測試數量均不代表背書、零漏洞或資金安全。


本次證據分四層解讀。獨立事實是下載到的公開位元組、實際命令退出碼、測試斷言及查出的資料列；TEAM 主張是包內私有測量摘要，含成功與失敗歷史，即使附雜湊也不能替代原始收據。歷史是先前官方報告對第十版的判斷；推論則是這些有限排程足以支持此次窄範圍閉合。未知的發布條件不會被列為已通過，測試來源未改也不等於原評估器必然完備。

驗證重點是先讓弱基線失敗，再在相同斷言下讓修正版通過，並確認合法切換仍清理、被動觀察不取得新權限。資料庫效應與畫面效應分開記錄，nonce 一致性斷言不能變成撤銷授權；公共顯示資格也不能變成持有人證明。測試可證明列出的事件順序，不能證明網路永遠可達、失敗清理最終必成功或所有跨程序競態。若程序死亡，記憶體內責任可能消失，這需要獨立發布測試，不在本次有界來源結論內。

## 六列矩陣

以下重現皆為本次本地執行；TEAM 未公開原始 log 的部分另列附錄。

| ID／等級 | exact-pin 修正位置 | 重現與實際效果 | 修補／反向控制與判定 |
|---|---|---|---|
| A10-L1／Low | [`auth.ts:267,308`][authflow]、[`636–685`][authcleanup]；[`authLifecycle.ts:102–116`][lifecycle] | held B verify 已 commit → 首 nonce logout transport 失敗 → stop/restart、provider discovery C → late verify。六組有／無 discovery：原因維持 stop 或 context-switch；原 nonce logout 2，address logout 0。B cookie 得 204、B revoked；foreign A 得 409、A/B 均不撤銷。 | **CLOSED（有界）**。同生命週期真切換、lock→stop、目前 C→D（address logout 1、signed-out 1）、重複 transport／503、後續 restart/stop 重試均通過。canonical PRESENT 不釋放舊撤銷責任；額外同地址探針證實無在途重派及較新列保留。409 是 refusal，不是 revocation；延遲 clear-cookie 邊界保留。 |
| A10-I1／Info | [`ownership.ts:259–265`][ranking] | 257 席，1..256 在 sightings await 期間過 24h，257 未過期。延遲 1/2/5000ms：選入 257、eligible=1、size=s、256 席、partial；0ms 控制按 ID 取前 256、eligible=256。index read_at 不變。 | **CLOSED**。await 後一次取 rankingNow，每個排序比較共用。成功 index：index/budget/RPC=1/1/2；拒絕 index：0/1/2、limited。tie-break、256 cap、RPC/index/budget 上限未改，既有 proof TTL 控制通過。 |
| A10-I2／Info | [`auth.ts:733–736`][assetsroute]；[`ownership.ts:371–378`][display] | sightings 或 character 延遲 0/1/2/5000ms；first/next counts 都為 true/true/false/false。無延遲 24h−1／24h／24h+1 控制保持含邊界。presence、fetchedAt、lastOnlineAt 不更新。 | **CLOSED**。最後相關 await 後一次取 displayNow。兩次公共請求：無 character index/budget/RPC=0/0/0；有 character 僅既有 character index 1、assets limiter 1、RPC 0；seat index/lane/probe 均 0。不賦予公共 roster 所有權權威。 |
| A10-I3／Info | [`auth-artifacts.mjs:12–44`][mask] | 實際落盤讀回 nested/quoted/bare 的 `/api/auth/session private.log`、`… dir/file.ts`、`… (private)/x.ts` 都整段遮罩；8 條 route × 5 空白 × 3 suffix 亦通過。 | **CLOSED（語法有界）**。exact route/query/subroute、URL、relative ID、nonce/action/event 與 saved-trace replay 保留；實際 CLI／file symlink／directory alias／hardlink、輸入不覆寫、命名空間等原 19 組加 H-S5 共20/20。Linux directory symlink 不等同實測 Windows junction；不保證 hostile ancestor swap 或 SMB/NFS。 |
| R10-N1／Info | [`auth.ts:287–293`][probe]、[`760–777`][lane]；[`ownership.ts:354–362`][authority] | NaN／±Infinity／rollback 在 sightings、preflight、probe、limiter 後：503、無非有限 lane；預留前 probe 0，預留後有限 probe 1、不刷新。+10m/+60m 200 恢復，無 stuck lane。 | **CLOSED**。有限控制先 index 1/lane 1；無效時先 index 0/RPC 1/budget 1、limiter 至多1。累計恢復 index 2/RPC 3/budget 3。額外 +2→+5→+10→+8 rollback 不 admission，保留 +5 probe／30s，舊有限 proof 僅 limited；Infinity 則503。無 refund，producer dates 不變。 |
| R10-N2／Info／test reliability | [`auth-audit9.test.mjs:65–76`][low2] | 真 B→A 後等待所有 logout finished 且 signed-out 通知，保留 address assertion、204、B revoked/A live、單次通知、零 prompt 等全部原斷言。 | **CLOSED（重複次數有界）**。TEAM 50 targeted／10 full 的69-stage文件中有50／10對應逐筆紀錄，未公開 raw logs；本次獨立 targeted 50 次、full 2 次（結果見附錄）。沒有新增 sleep、增加 flush 或刪失敗／改 reference oracle。 |

## 緊湊證據附錄

### 身分、來源及歷史

- codeload 精確 pin 封存下載；不是可執行 `git rev-parse HEAD` 的 Git checkout，未推定私有 commit 身分。manifest SHA256 `4c82cd864ef99cede0ecdca6314d15a23e9eddb3446e85dcc123d958c7b7b2fc`，146/146；SHA256SUMS 297/297。146 包含130 exact、16歷史 masked、57遮罩行；checksum 證明公開位元組完整性，不證明行為。
- 官方 Audit10 SHA256 `37c079cf5da5ec71dabb16023372b0dd2b6e8adf645384e40ed239e2ef5dac3e`；Report10 `f12c235f7591eb0b09d11b4fd93062174ffec242a46211c8b19ec342a134c115`，與 LATEST_AUDIT_IDENTITY 相符。
- 第十版差異為13個來源檔（5執行／診斷、8測試／runner，其中3新增）。未變更 reference model／driver、M1／migration 或 dependency lock。全部 supported 28檔都執行；未替換私有來源、shim、global viem、複製 node_modules 或隱藏 skip。[runner][runner]

### 本次命令與失敗保留

| 命令（source/，除另註） | exit／總數、結果 |
|---|---|
| `npm ci --ignore-scripts` | 首次226，EROFS：預設 `/root/.npm` 快取唯讀；其後 prerequisite check exit1（local viem missing），當時 review 未啟動。環境失敗，不是來源斷言。 |
| `npm ci --ignore-scripts --cache /tmp/imd-npm-cache` | 0；79 packages、audited80；重試僅改快取，lock/source 未改。 |
| `node scripts/review-tests.mjs --check` | 0；Node v24.21.0／viem2.56.9／28檔。 |
| `npm run test:review` ×2 | 兩次皆0；各tests715/pass715/fail0/cancelled0/skipped0/todo0；約120.0s、93.1s。本次未重跑完整10次，不把TEAM10次當自己的量測。 |
| `node --test --test-reporter=tap tests/{auth-audit10,ownership-audit10,artifacts-audit10}.test.mjs`（實際逐檔列參數） | 0；56/56，fail/cancel/skip/todo 全0。 |
| `node scripts/verify-artifact-closure.mjs` | 0；20/20、failed/skipped0；Linux 實際 file/dir symlink，無 EPERM。 |
| `node --test --test-reporter=tap tests/auth-audit9.test.mjs` ×50 | 50次皆0；各tests11/pass11/fail0/cancelled0/skipped0/todo0，共550項。 |
| 額外 `node test/scratch/extra.mjs /tmp/imd-report11-candidate/source` | 0；2個同地址場景通過；基線 exit1，stop 被改為 lock-reconcile 的真正斷言失敗。 |
| 額外 `node reviewer-clock.mjs` | 首次1：自寫探針誤預期拒絕 index 也應 partial，實際 limited 是誠實結果；改為依 admitted/refused 分別 partial/limited 後0，未修改候選或原測試／oracle。兩次原始結果保留，不把首次失敗改寫成通過。 |

完整全檔測試不是 full-site build。TEAM 私有full1765/1765、private build/typecheck與clean715/715不可獨立取得；原1764/1765／Git child128環境失敗仍在文件。TEAM的50／10穩定性紀錄只核對公開summary及時間／hash，raw receipt未公開，不能自行驗證其私有raw bytes；本次重跑是另外證據。Windows歷史file-symlink EPERM不能算拒絕通過，本次未執行Windows。

### 相同評估器弱基線

fresh 第十版公開封存單獨 `npm ci --ignore-scripts --cache /tmp/imd-npm-cache` exit0；只覆蓋候選的3新增測試、lifecycle model測試、verifier，產品模組不變。

```text
node --test --test-reporter=tap tests/auth-audit10.test.mjs tests/ownership-audit10.test.mjs tests/artifacts-audit10.test.mjs tests/auth-lifecycle-model.test.mjs
→ exit1，tests135 pass97 fail38 cancelled0 skipped0 todo0
node scripts/verify-artifact-closure.mjs
→ exit1，total20 passed19 failed1 skipped0；唯一H-S5斷言失敗
```

失敗涵蓋 retained原因／uncertain清理、非有限lane、257排名、assets等待及spaced路徑；無EPERM或setup failure，精確重現TEAM校準。這支持評估器可辨別弱基線；不是保證能找出所有缺陷。[TEAM校準][team]

### SQLite 與工作量

- L1 六組：prompt/connect/challenge/verify=1/0/1/1；nonce logout2、address0、signed-in0。stop-B session/home/index/budget/RPC/hint=4/0/1/1/0/2；stop-A=4/1/1/1/0/2；same-life switch=3/0/0/0/0/0。有／無 discovery相同。C→D address1、signed-out1；B nonce2。204只撤銷原B；409保留A/B列及cookie，challenge used_at/invalidated_at未變。
- 重複transport／503：stop、verify fence、restart、後續stop共4次同nonce嘗試；restore不追加重試；末次204或409。末態session6/home0/index1/RPC0，prompt1/connect0/challenge1/verify1、signed-in0。
- 額外同地址：兩列同expires_at但不同nonce；pending204僅原nonce派送1次，舊列revoked、新列NULL，共享cookie被clear後canonical ABSENT；repeated failure5次，最後409、兩列NULL。各prompt1/connect0/addresslogout0/index1/RPC0；外部合成登入另有challenge/verify各1。
- I1/I2/N1 auth與presence列逐次比對不變，無M1寫入；index read_at／sighting producer日期保留。N1查實際`index_lanes`／`index_lane_probes`數值，非靠JSON把Infinity顯成null猜測；已存在有限probe不退回、不刷新。R5/R8/v1.1 canonical-session與Member測試在全檔執行通過，SQLite仍只是D1合成介面，沒有生產D1一致性證明。

本地證據完成時間：2026-10-05T19:07:14.152796+00:00。以下為實際log SHA256，雜湊本身不授予獨立權威：

```text
imd-ci.log 990587fff9ae4cf632db3067bb88c402d0ecd4c3866c14221b366f8c01174a57
imd-check.log 8a8480e25a5b9efc8be8d9905374b3d54dd5ab688797c63f9c888cf6372097ea
imd-ci2.log 999885e44f07fffb644e7dc82289de97cc9e96a69d7d9a6bb93508cf52f09b00
imd-check2.log c6c029a382a3b79aaecd024f644437b86d0aa0f111190c5eb80cf951efbb82d3
imd-review.log 416b4c2d0e15d883c779ee154746a4ec535c8580f45f93e8ad889b1af2649e8b
imd-review2.log 6d15bf9a051eaaac652e3af3569576c2688d53e0a85da35ea2cd0ada805303f3
imd-verifier.log 8973dffa3286abc363bc95d9bb9c929caef604082ba00e1aa59b6d196bf85474
imd-targeted.log 8ad82ff589395ecda82150af525f6e230a51b9bef7ffbad8523fbb833d8cec69
imd-baseline-evaluator.log f2a8809a3cda939fc7fe83f04e2db28826676401df5ee2f0cbfa197c835b704a
imd-baseline-verifier.log bea7b19c43bbfefeae3c6465e8f836f8dd09d3becf4a921d87e3756859a10098
imd-extra.log 1ba2c76d05bb414961aeff5085819cd7be7a5e054bfd899b0a6ae3dbb147f545
imd-extra-baseline.log 87812d7ea0c0255e9d34532f3895f3205f56d215120dcd15ea38db6b95ed8e6f
imd-clock-extra.log 2f2e437ee1a63fce0d5194e73182e782760cfefe51f0a2216caaeed1f6fa37ac
imd-clock-extra2.log 30d2501644b1e8f3f2125c498c4cb55c74413b3e4523a74113dd059682383869
imd-low2-summary.json d6135dbc6d96a590eea2b2f4475afefc72a1cfed7116959c390cbd541d67f601
```



[manifest]: https://github.com/tungweb3/imd-ember-world-review/blob/35ace952824ebf711fd9fa6cb7ea1cc83b75cd6a/manifests/submission11-published-source.json
[team]: https://github.com/tungweb3/imd-ember-world-review/blob/35ace952824ebf711fd9fa6cb7ea1cc83b75cd6a/Submission11/FinalClosure/TEST_RESULTS.json
[authflow]: https://github.com/tungweb3/imd-ember-world-review/blob/35ace952824ebf711fd9fa6cb7ea1cc83b75cd6a/source/src/world/auth.ts#L267-L319
[lifecycle]: https://github.com/tungweb3/imd-ember-world-review/blob/35ace952824ebf711fd9fa6cb7ea1cc83b75cd6a/source/src/world/authLifecycle.ts#L102-L116
[nonce]: https://github.com/tungweb3/imd-ember-world-review/blob/35ace952824ebf711fd9fa6cb7ea1cc83b75cd6a/source/server/auth.ts#L627-L651
[ranking]: https://github.com/tungweb3/imd-ember-world-review/blob/35ace952824ebf711fd9fa6cb7ea1cc83b75cd6a/source/server/ownership.ts#L259-L265
[display]: https://github.com/tungweb3/imd-ember-world-review/blob/35ace952824ebf711fd9fa6cb7ea1cc83b75cd6a/source/server/ownership.ts#L371-L378
[lane]: https://github.com/tungweb3/imd-ember-world-review/blob/35ace952824ebf711fd9fa6cb7ea1cc83b75cd6a/source/server/auth.ts#L758-L777
[authority]: https://github.com/tungweb3/imd-ember-world-review/blob/35ace952824ebf711fd9fa6cb7ea1cc83b75cd6a/source/server/ownership.ts#L354-L364
[assetsroute]: https://github.com/tungweb3/imd-ember-world-review/blob/35ace952824ebf711fd9fa6cb7ea1cc83b75cd6a/source/server/auth.ts#L733-L736
[low2]: https://github.com/tungweb3/imd-ember-world-review/blob/35ace952824ebf711fd9fa6cb7ea1cc83b75cd6a/source/tests/auth-audit9.test.mjs#L65-L76
[oracle]: https://github.com/tungweb3/imd-ember-world-review/blob/35ace952824ebf711fd9fa6cb7ea1cc83b75cd6a/source/tests/auth-reference-model.mjs#L1
[store]: https://github.com/tungweb3/imd-ember-world-review/blob/35ace952824ebf711fd9fa6cb7ea1cc83b75cd6a/source/tests/auth-artifacts.mjs#L61-L112
[mask]: https://github.com/tungweb3/imd-ember-world-review/blob/35ace952824ebf711fd9fa6cb7ea1cc83b75cd6a/source/tests/auth-artifacts.mjs#L12-L44
[runner]: https://github.com/tungweb3/imd-ember-world-review/blob/35ace952824ebf711fd9fa6cb7ea1cc83b75cd6a/source/scripts/review-tests.mjs#L6-L38
[audit]: https://github.com/Identity-md/research/blob/d2bbc2713f0c15d7542bc8afa09bafc4bf12ef12/jobs/e817a62e-1b9f-4469-90d7-7a761579af81/files/AUDIT.md
[prior]: https://github.com/Identity-md/research/blob/7701ce0c6d860ba50616629d0a3a60e644135fe4/jobs/a3ec7191-f1ab-400e-bb5f-dfa858c6da65/files/artifacts/report.md
[authcleanup]: https://github.com/tungweb3/imd-ember-world-review/blob/35ace952824ebf711fd9fa6cb7ea1cc83b75cd6a/source/src/world/auth.ts#L636-L685
[probe]: https://github.com/tungweb3/imd-ember-world-review/blob/35ace952824ebf711fd9fa6cb7ea1cc83b75cd6a/source/server/auth.ts#L287-L293
