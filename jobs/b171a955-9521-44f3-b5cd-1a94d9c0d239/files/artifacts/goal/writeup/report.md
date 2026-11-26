# test staking

**[Open test staking on Sepolia](https://rawcdn.githack.com/identity-md-launches/launch-3422-workflow-frontend-stage-context/fb19e8784a80c9732519d411541cf6214d4e4481/dist/index.html)**. Choose **Open the page** if the host shows its external-content notice. This third-party mirror serves the published frontend from its exact Git commit. You can read gifts and get a buy quote before connecting a wallet.

Launch **3417** deployed the ERC-20 **test** (ticker **testAdam**, fixed supply **1,000,000,000**), a public gift vault and a seeded native ETH/testAdam Uniswap v4 pool on Ethereum Sepolia. Donor points measure how much testAdam a wallet has given. The contracts offer no staking yield. [Release workflow](https://api.imd.fun/workflows/b5426517-ab82-4ad1-af39-9ffa464422ef) · [Launch record](https://api.imd.fun/launches/2896cd7a-8746-400d-9809-5e342463e993)

## Buy, donate and claim

1. **Buy.** Connect a wallet on Ethereum Sepolia, chain **11155111**, with Sepolia ETH for the purchase and gas. In **Buy with ETH**, enter the ETH amount and review the estimated testAdam, minimum received, slippage and transaction deadline. The quote lasts 30 seconds. **Buy testAdam** simulates the payable router call before opening the wallet. Check the mined receipt for the transfer into your account.
2. **Donate.** In **Donate**, enter the amount of testAdam, approve the vault as spender and wait for the approval receipt. Then choose **Donate**. A donation of 1.5 testAdam creates one public gift of 1.5 and credits the donor 1.5 permanent, nontransferable points. A plain token transfer to the vault permanently locks those tokens and earns zero points.
3. **Claim.** Open **Gifts** from another wallet, select an open gift and confirm **Claim**. The first eligible transaction mined receives the whole gift. The donor address cannot claim it, a second claim reverts, and the donor keeps the points. A donor can control a second wallet, so the points measure gross donations. The vault receipt identifies the recipient in its `Claimed(giftId, claimer, amount)` event. [Vault source](https://github.com/identity-md-launches/launch-3417-workflow-contract-stage-context/blob/29cf2d87ebd12eba43c683766eb2fae4cd5e2811/src/DonationVault.sol)

## Market at finalized block 12,213,314

**26 November 2026, 01:31:00 UTC.** The values below cover one Sepolia pool. The hosted release displays price, active liquidity, FDV and volume. Its circulating-cap field always says “Unavailable”. The estimate below is reproducible from Sepolia balances, and the corrected export in this report displays it as balances and price change. [Finalized block](https://sepolia.etherscan.io/block/12213314) · [Published pool panel source](https://github.com/identity-md-launches/launch-3422-workflow-frontend-stage-context/blob/fb19e8784a80c9732519d411541cf6214d4e4481/web/src/App.tsx#L803-L888)

| Measure | Value at the block | Basis |
| --- | ---: | --- |
| Stored pool price | ≈0.00000002 ETH per testAdam | ETH is currency0, testAdam is currency1, both have 18 decimals. Price is `2^192 / sqrtPriceX96²`. |
| Active liquidity | 0 | Current tick 177284 was above the seeded position’s upper tick of 177240. |
| Fully diluted value | ≈20 ETH | Stored price × 1,000,000,000 minted testAdam. |
| Estimated circulating supply | 900,000,000 testAdam | The circulation rule below excludes 100,000,000 in the distributor and 0 permanently locked in the vault. |
| Estimated circulating market cap | **≈18 ETH** | Stored price × 900,000,000 testAdam. Both valuations describe the stored marginal price at a tick with zero active liquidity. |
| Pool swap volume | **0 ETH from 0 swaps** | Complete scan from initialization at block 12,212,785 (25 November, 23:42:48 UTC) through 12,213,314 inclusive. The pool was younger than 24 hours. |
| Gift vault | 0 gifts, 0 testAdam outstanding | `giftCount()` and `totalOutstanding()` at the same block. |

**Circulation rule used here.** Count all minted tokens except the launch Merkle distributor’s current balance and the permanently inaccessible portion of the vault balance. The latter is `balanceOf(vault) − totalOutstanding()`. Pool inventory, outstanding gifts and the unlocked launch recipient allocation count. This is an explicit release-specific estimate. The release supplies no official free-float policy. The launch record identifies the distributor, both the distributor and the vault return the deployed token from `token()`, and every balance in the calculation was read at the stated block. [Distributor](https://sepolia.etherscan.io/address/0x9b44adc47a9b850ab36954aacda9a51783a4ec1e) · [Launch allocation and contract roles](https://api.imd.fun/launches/2896cd7a-8746-400d-9809-5e342463e993) · [Sepolia read endpoint](https://ethereum-sepolia-rpc.publicnode.com)

**Buy check.** At the same block, 0.001 Sepolia ETH quoted **49,154.238270530270622382 testAdam**. With 0.5% slippage the minimum was 48,908.467079177619269270 testAdam. The hosted page passed the payable `execute` simulation and reached the wallet request for exactly 0.001 ETH. The test wallet declined it. This check produced no purchase receipt. [Buy implementation](https://github.com/identity-md-launches/launch-3422-workflow-frontend-stage-context/blob/fb19e8784a80c9732519d411541cf6214d4e4481/web/src/App.tsx#L421-L507)

## Deployment and source

| Sepolia component | Identifier |
| --- | --- |
| LaunchToken | [0x4cc136b358c28cd7107b22a8ef853b077a0b8ec9](https://sepolia.etherscan.io/address/0x4cc136b358c28cd7107b22a8ef853b077a0b8ec9) |
| DonationVault | [0xa241f03c041f964b37f63b874e81ac810a9739e3](https://sepolia.etherscan.io/address/0xa241f03c041f964b37f63b874e81ac810a9739e3) |
| PoolManager | `0xe03a1074c86cfedd5c142c4f04f1a1536e203543` |
| Pool ID | `0xf6b590d823083d9a9b7c10ceb9a990d06b9a1196e6a2dc002a1b1b915393d394` |
| Full PoolKey, in ABI order | `(0x0000000000000000000000000000000000000000, 0x4cc136b358c28cd7107b22a8ef853b077a0b8ec9, 12500, 60, 0xa0602cb30558d5dd17415b6268a4feea3a0ca000)` |
| StateView | `0xe1dd9c3fa50edb962e442f60dfbc432e24537e4c` |
| Quoter used by the site | `0x61b3f2011a92d183c7dbadbda940a7555ccf9227` |
| Universal Router used by the site | `0x3a9d48ab9751398bbfa63ad67599bb04e4bdf98b` |

One successful transaction deployed the token and vault, initialized the pool and added liquidity. The PoolManager’s `Initialize` and positive `ModifyLiquidity` logs have this pool ID, which equals `keccak256(abi.encode(PoolKey))`. The zero first currency is native ETH. The fee is 1.25%, tick spacing is 60 and the final key field is the initialization guard. The factory received the initial mint. At the snapshot the token returned `test`, `testAdam`, 18 decimals and `10^27` base units. The vault returned that token’s address, and the Quoter, Router and StateView each returned the listed PoolManager. [Deployment, initialization and funding receipt](https://sepolia.etherscan.io/tx/0x72562a80dff94d6c0c19aeadb1099c66ad3bc708bd3906422453bd273743d234) · [Deployment handoff](https://api.imd.fun/workflows/b5426517-ab82-4ad1-af39-9ffa464422ef)

| Code delivered | Repository and exact commit |
| --- | --- |
| Goal trunk reached by the contract waves | [identity-md-launches/goal-3416-create-token-sepolia-named](https://github.com/identity-md-launches/goal-3416-create-token-sepolia-named/tree/5e16ce53748597be091771df9beae3d54b9310cf) · `5e16ce53748597be091771df9beae3d54b9310cf` |
| Contracts release | [launch-3417-workflow-contract-stage-context](https://github.com/identity-md-launches/launch-3417-workflow-contract-stage-context/tree/29cf2d87ebd12eba43c683766eb2fae4cd5e2811) · `29cf2d87ebd12eba43c683766eb2fae4cd5e2811` |
| Published frontend, including build-ready source and static export | [launch-3422-workflow-frontend-stage-context](https://github.com/identity-md-launches/launch-3422-workflow-frontend-stage-context/tree/fb19e8784a80c9732519d411541cf6214d4e4481) · `fb19e8784a80c9732519d411541cf6214d4e4481` |

The release workflow completed at 01:47:55 UTC. It records `testadam.identitymd.eth` pointing to CID `bafybeih5bdqpqiawnsxdbwh3vk6fettfbkovkutzhbie4en25wkqjkmf44`. The Filebase copy is an **archive entry point**. In Chromium its HTTP 200 page blocked all three configured RPC origins with `default-src 'self'` and no `connect-src`. The separate hosted link at the top served the same deployment manifest and all 11 SHA-256-verified assets. With default browser security it showed the empty gift list, finalized block **12,213,497**, the pool data and a quote, with zero RPC policy violations. Browser JSON-RPC reads in these checks used the assigned Sepolia read transport. The primary public RPC also permitted JSON POST in its CORS preflight for the mirror’s origin. [IPFS archive](https://ipfs.filebase.io/ipfs/bafybeih5bdqpqiawnsxdbwh3vk6fettfbkovkutzhbie4en25wkqjkmf44/index.html) · [Published manifest](https://rawcdn.githack.com/identity-md-launches/launch-3422-workflow-frontend-stage-context/fb19e8784a80c9732519d411541cf6214d4e4481/dist/imd-deployment.json) · [Contracts job result](https://api.imd.fun/jobs/4887f394-12fb-4dab-92c6-4fc557466c7a/result) · [Frontend job result](https://api.imd.fun/jobs/d5876118-6af8-446e-bdab-3d64d9a6c326/result)

## Checks behind the release

All five work items were accepted. The integration wave exercised the merged trunk without changing its commit.

| Accepted result | Work and evidence |
| --- | --- |
| `contracts/launch-token` · `b01-launch-token` | Implemented the fixed-supply token. Eight token tests passed, including three fuzz tests at 1,024 runs each. |
| `contracts/donation-vault` · `b01-donation-vault` | Implemented allowance-based gifts, one-time claims and donor accounting. Sixteen tests passed with a mock token. |
| `trunk-integration-check/real-token-vault` · `b03-real-token-vault` | Built with solc 0.8.26. All 24 baseline and 10 real-pair integration tests passed, including 256 fuzz runs. Tests covered allowance failures, fractional and full-supply gifts, whole payouts, self/repeat-claim rejection, persistent points and direct transfers. The build reported three vault lint warnings. |
| `site-integration/buy-flow` · `b02-buy-flow` | Specified an exact-input v4 quote, slippage floor, deadline, router simulation and receipt checks. The table above gives the Quoter actually used by the released app. |
| `site-integration/market-metrics` · `b02-market-metrics` | Specified one finalized block for valuation and the sum of absolute ETH legs of distinct pool-specific Swap logs for volume. The scan starts at the later of initialization and the 24-hour cutoff. A missing interval makes volume unavailable. |

The frontend worker also exercised approve, donate, claim and buy on a Sepolia fork. The contracts ran on that fork with a mock wallet. The hosted checks here cover browser reads, a quote and a wallet preflight. A real-wallet transaction through the hosted page remains unverified. [Frontend validation log](https://github.com/identity-md-launches/launch-3422-workflow-frontend-stage-context/blob/fb19e8784a80c9732519d411541cf6214d4e4481/docs/VALIDATION.md)

## Corrected frontend included with this report

The hosted mirror runs the published commit. The following three corrections are delivered as a runnable export and a source patch in this report. Publishing them at the project’s ENS name would require a new frontend release.

| Published behavior reproduced | Correction and result in the included export |
| --- | --- |
| Pruning the token’s bytecode at block 6,106,657 caused zero log requests and unavailable volume, even though the complete event interval was accessible. | Read the PoolManager’s Initialize event at block 12,212,785 and verify its pool ID and launch transaction hash. With the old state read still failing, Chromium made one Initialize query and one Swap query and displayed **0 ETH, 0 swaps**. A failed Swap query still gave **Unavailable**. |
| At the review block FDV displayed 19.9999 ETH. Changing only the price to 0.00000004 ETH made FDV 40 ETH while circulating cap still said “Unavailable”. | Read the distributor and vault bindings, balances and outstanding gifts at the valuation block. The corrected panel displayed **17.9999 ETH** on 900,000,000 circulating testAdam. With the changed-price fixture it displayed **36 ETH** of cap and **40 ETH** of FDV. A failed distributor read withheld the cap and volume still loaded. |
| After a mocked 1.5 testAdam claim by B, switching to donor A showed “from you” alongside B’s payout and 6.5 balance. | Keep claim status by wallet **and** gift ID, including results hidden by the Open only filter. A saw the claimed gift without B’s receipt. B recovered its own receipt on switching back. On the published build, reload after switching wallets and use the receipt’s indexed `claimer` to identify the payee. |

The corrected source passed type checking, the production build, all nine frontend logic tests and export verification for all 11 assets. The executable export below contains those build bytes. The contract addresses, ABIs and PoolKey come from the published manifest.

### Run the corrected export without a frontend build

Download the pinned frontend repository using **Source archive** below. Extract it and save this report as `report.md` beside its `dist/` directory. Run the block below there with Python 3. It combines that release’s prebuilt assets with the binary patch in this report, verifies the input and output SHA-256 digests and creates a new `test-staking-reviewed/` directory. The reconstruction works offline. The running app uses Sepolia RPC for market reads and transactions. [Source archive at the frontend commit](https://codeload.github.com/identity-md-launches/launch-3422-workflow-frontend-stage-context/zip/fb19e8784a80c9732519d411541cf6214d4e4481)

<details>
<summary>Reconstruct the reviewed static site with Python 3</summary>

```sh
python3 - report.md dist <<'PY'
import base64
import bz2
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import zipfile

def checked(data, digest, label):
    if hashlib.sha256(data).hexdigest() != digest:
        raise SystemExit("SHA-256 mismatch for " + label)
    return data

report, dist = map(Path, sys.argv[1:])
manifest = checked((dist / "imd-deployment.json").read_bytes(),
    "d6e3a31e6a30060d1ba36cd43e81a70656aa603f4541ab1e42088db02b3b1648", "release manifest")
paths = [entry["path"] for entry in json.loads(manifest)["assets"]]
original = checked(b"".join((dist / p).read_bytes() for p in sorted(paths + ["imd-deployment.json"])),
    "1830507400e255d313f4f9736b16806026dc97aa7db8393f16090b13010feb98", "release export")
block = re.search(r"(?ms)^```base64\n(.*?)\n```$", report.read_text(encoding="utf-8"))
if block is None:
    raise SystemExit("The export patch block is missing from report.md")
patch = checked(base64.b64decode(block.group(1)),
    "3da28cf2408723d61e43410fcbfaf88584382f6f980e245d06049feab75f4266", "BSDIFF40 patch")

# BSDIFF40 uses signed-magnitude little-endian integers and three bzip2 streams.
def integer(octets):
    value = int.from_bytes(octets, "little")
    return -(value & ((1 << 63) - 1)) if value >> 63 else value

control_end = 32 + integer(patch[8:16])
difference_end = control_end + integer(patch[16:24])
control = bz2.decompress(patch[32:control_end])
difference = io.BytesIO(bz2.decompress(patch[control_end:difference_end]))
literal = io.BytesIO(bz2.decompress(patch[difference_end:]))
old = 0
rebuilt = bytearray()
for i in range(0, len(control), 24):
    count, extra, seek = (integer(control[j:j+8]) for j in (i, i+8, i+16))
    rebuilt.extend((a + b) & 255 for a, b in zip(original[old:old+count], difference.read(count)))
    rebuilt.extend(literal.read(extra))
    old += count + seek
checked(rebuilt, "c51f5fe7f570cf4d8d43f5de551502e0aaa6b4d3d4336ca8b35e9a06263cea07", "reviewed ZIP")
output = Path("test-staking-reviewed")
output.mkdir(exist_ok=False)
with zipfile.ZipFile(io.BytesIO(rebuilt)) as archive:
    archive.extractall(output)
print("Ready:", output / "index.html")
PY
```

</details>

Serve the resulting directory with `python3 -m http.server 8000 --bind 127.0.0.1 --directory test-staking-reviewed` and open `http://127.0.0.1:8000/`. To run the original published version locally, the same server command accepts `--directory dist`.

<details>
<summary>Source patch for frontend maintainers</summary>

Apply this unified diff from the root of frontend commit `fb19e8784a80c9732519d411541cf6214d4e4481`. With this report saved as `report.md`, the following commands extract the patch, apply it and rebuild the site with the release lockfile.

```sh
awk '/^```diff$/ {copy=1; next} copy && /^```$/ {exit} copy {print}' report.md > frontend-review.patch
git apply --check frontend-review.patch && git apply frontend-review.patch
(cd web && npm ci --legacy-peer-deps && npm run build && npm run verify && npm test)
```

```diff
diff --git a/web/src/App.tsx b/web/src/App.tsx
index 1ab5aa9..e13629c 100644
--- a/web/src/App.tsx
+++ b/web/src/App.tsx
@@ -108,16 +108,22 @@ function useTx(d: Deployment) {
 }
 
 /** Transaction slots keyed by id (gift claims), held by the list so a result outlives its row being filtered out. */
-function useTxMap(d: Deployment) {
+function useTxMap(d: Deployment, wallet?: Address) {
   const runner = useRunner(d);
-  const [map, setMap] = useState<Record<string, Tx>>({});
+  const account = wallet?.toLowerCase() ?? "";
+  const [accounts, setAccounts] = useState<Record<string, Record<string, Tx>>>({});
+  const map = accounts[account] ?? {};
   const get = (id: string) => map[id] ?? IDLE;
   return {
     map,
     get,
     busy: (id: string) => isBusy(get(id)),
     run: (id: string, label: string, params: RunParams, describe: (r: TransactionReceipt) => Outcome, opts?: RunOpts) =>
-      runner((u) => setMap((m) => ({ ...m, [id]: typeof u === "function" ? u(m[id] ?? IDLE) : u })), label, params, describe, opts),
+      runner((update) => setAccounts((all) => {
+        const mine = all[account] ?? {};
+        const tx = typeof update === "function" ? update(mine[id] ?? IDLE) : update;
+        return { ...all, [account]: { ...mine, [id]: tx } };
+      }), label, params, describe, opts),
   };
 }
 
@@ -653,7 +659,7 @@ function Gifts({ d, reads, wrongChain, openConnect }: PanelProps) {
   const list = useMemo(() => (gifts.data ?? []).filter((g) => !openOnly || !g.claimed), [gifts.data, openOnly]);
   const openCount = (gifts.data ?? []).filter((g) => !g.claimed).length;
   // Claim results live here, keyed by gift id, so Open only hiding a row that just became claimed keeps its receipt and link.
-  const claims = useTxMap(d);
+  const claims = useTxMap(d, address);
   const shownIds = new Set(list.map((g) => g.id.toString()));
   const hiddenResults = Object.entries(claims.map).filter(([id, t]) => t.phase !== "idle" && !shownIds.has(id));
   const claim = (g: Gift) => {
@@ -854,7 +860,13 @@ function PoolPanel({ d }: { d: Deployment }) {
           <div>
             <dt>Circulating market cap</dt>
             <dd>
-              Unavailable. <span className="muted">Supply basis unknown: the deployment handoff documents no locked or unreleased holders, so circulating supply cannot be verified.</span>
+              {p.circulatingSupply === undefined || !p.sqrtPriceX96
+                ? "Unavailable. The circulation inputs or pool price could not be verified."
+                : <>
+                    {fmt(p.circulatingSupply * p.ethPerToken / 10n ** 18n, 18, 4)} ETH
+                    <span className="muted"> at the stored price, from {fmt(p.circulatingSupply, 18, 4)} testAdam.</span>
+                  </>}
+              <span className="muted"> Estimate excludes the launch distributor balance and permanently locked direct vault transfers. Pool inventory and outstanding gifts count.</span>
             </dd>
           </div>
           <div>
diff --git a/web/src/pool.ts b/web/src/pool.ts
index e765d63..02df801 100644
--- a/web/src/pool.ts
+++ b/web/src/pool.ts
@@ -1,12 +1,40 @@
 // Pool panel data: one finalized block for price, liquidity and supply; a bounded, chunked Swap scan
 // for the trailing 24 hours. A scan with any failed chunk is reported as partial, never as a number.
-import type { Abi, Hex, PublicClient } from "viem";
+import { erc20Abi, parseAbi, type Abi, type Hex, type PublicClient } from "viem";
 import type { Deployment } from "./deployment";
 import { initializeEvent, poolIdOf, priceFromSqrt, stateViewAbi, swapEvent } from "./uniswap";
 
 export const DAY = 86_400n;
 export const CHUNK = 5_000n;
 
+// Sepolia launch 3417, from its release record and successful initialization receipt.
+const release = {
+  chainId: 11155111,
+  poolId: "0xf6b590d823083d9a9b7c10ceb9a990d06b9a1196e6a2dc002a1b1b915393d394",
+  block: 12212785n,
+  tx: "0x72562a80dff94d6c0c19aeadb1099c66ad3bc708bd3906422453bd273743d234",
+  distributor: "0x9b44adc47a9b850ab36954aacda9a51783a4ec1e",
+} as const;
+const bindingAbi = parseAbi(["function token() view returns (address)", "function totalOutstanding() view returns (uint256)"]);
+
+async function circulation(client: PublicClient, d: Deployment, blockNumber: bigint, supply: bigint) {
+  const token = d.token.address;
+  const vault = d.vault.address;
+  const balanceOf = (owner: typeof token) => client.readContract({
+    address: token, abi: erc20Abi, functionName: "balanceOf", args: [owner], blockNumber,
+  });
+  const boundToken = (address: typeof token) => client.readContract({
+    address, abi: bindingAbi, functionName: "token", blockNumber,
+  });
+  const [distributedToken, vaultToken, reserve, vaultBalance, outstanding] = await Promise.all([
+    boundToken(release.distributor), boundToken(vault), balanceOf(release.distributor), balanceOf(vault),
+    client.readContract({ address: vault, abi: bindingAbi, functionName: "totalOutstanding", blockNumber }),
+  ]);
+  if ([distributedToken, vaultToken].some(t => t.toLowerCase() !== token.toLowerCase()) || outstanding > vaultBalance) return;
+  const excluded = reserve + (vaultBalance - outstanding);
+  if (excluded <= supply) return supply - excluded;
+}
+
 export type PoolSnapshot = {
   poolId: Hex;
   block: bigint;
@@ -15,6 +43,7 @@ export type PoolSnapshot = {
   liquidity: bigint;
   /** Undefined when the token has no code at this block (a finalized block before launch). */
   totalSupply?: bigint;
+  circulatingSupply?: bigint;
   /** ETH per whole testAdam, scaled 1e18; 0 when the pool is not initialized at this block. */
   ethPerToken: bigint;
   /** FDV in wei: totalSupply * ethPerToken. Undefined without a supply. */
@@ -81,7 +110,11 @@ export async function loadPool(client: PublicClient, d: Deployment): Promise<Poo
   // ETH per testAdam: base = testAdam. Both 18 decimals here, but the formula keeps them explicit.
   const ethPerToken = priceFromSqrt(sqrtPriceX96, { baseIsCurrency0: !tokenIsCurrency1, dec0: 18, dec1: 18 });
   const fdvWei = totalSupply === undefined ? undefined : (totalSupply * ethPerToken) / 10n ** 18n;
-  const base = { poolId, block, timestamp: fin.timestamp, sqrtPriceX96, liquidity, totalSupply, ethPerToken, fdvWei };
+  const known = d.chain.id === release.chainId && poolId === release.poolId;
+  const circulatingSupply = known && totalSupply !== undefined && block >= release.block
+    ? await circulation(client, d, block, totalSupply).catch(() => undefined)
+    : undefined;
+  const base = { circulatingSupply, poolId, block, timestamp: fin.timestamp, sqrtPriceX96, liquidity, totalSupply, ethPerToken, fdvWei };
   const cutoff0 = fin.timestamp - DAY;
 
   // StateView proves the pool is uninitialized at this block. A pool cannot be uninitialized later, so no
@@ -104,11 +137,13 @@ export async function loadPool(client: PublicClient, d: Deployment): Promise<Poo
   let initBlock: bigint | undefined;
   let initError: string | undefined;
   try {
-    const tokenBlock = await firstCodeBlock(client, d.token.address, block);
-    for (let from = tokenBlock; from <= block && initBlock === undefined; from += CHUNK) {
-      const to = from + CHUNK - 1n > block ? block : from + CHUNK - 1n;
+    const first = known ? release.block : await firstCodeBlock(client, d.token.address, block);
+    const last = known ? release.block : block;
+    for (let from = first; from <= last && from <= block && initBlock === undefined; from += CHUNK) {
+      const to = from + CHUNK - 1n > last ? last : from + CHUNK - 1n;
       const logs = await getLogsRetry(() => client.getLogs({ address: pm, event: initializeEvent, args: { id: poolId }, fromBlock: from, toBlock: to }));
-      if (logs.length) initBlock = logs[0].blockNumber!;
+      const init = logs.find(log => !known || (log.blockNumber === release.block && log.transactionHash === release.tx));
+      initBlock = init?.blockNumber ?? undefined;
     }
   } catch (e) {
     initError = `The Initialize search did not complete (${(e as Error).message.slice(0, 80)}).`;
@@ -134,7 +169,7 @@ export async function loadPool(client: PublicClient, d: Deployment): Promise<Poo
       const cutBlock = await firstBlockAtOrAfter(client, cutoff, block);
       from = cutBlock > initBlock ? cutBlock : initBlock;
     } catch (e) {
-      return { poolId, block, timestamp: fin.timestamp, sqrtPriceX96, liquidity, totalSupply, ethPerToken, fdvWei, initBlock, volume: { status: "partial", fromBlock: initBlock, toBlock: block, reason: `Could not locate the block 24 hours back (${(e as Error).message.slice(0, 80)}).` } };
+      return { ...base, initBlock, volume: { status: "partial", fromBlock: initBlock, toBlock: block, reason: `Could not locate the block 24 hours back (${(e as Error).message.slice(0, 80)}).` } };
     }
     const all: Parameters<typeof sumEthLeg>[0] = [];
     let failed: string | undefined;
@@ -154,7 +189,7 @@ export async function loadPool(client: PublicClient, d: Deployment): Promise<Poo
     if (failed) volume = { status: "partial", fromBlock: from, toBlock: block, scannedTo, reason: failed };
     else volume = { status: "complete", ...sumEthLeg(all, ethIsCurrency0), fromBlock: from, toBlock: block, fromTime };
   }
-  return { poolId, block, timestamp: fin.timestamp, sqrtPriceX96, liquidity, totalSupply, ethPerToken, fdvWei, initBlock, volume };
+  return { ...base, initBlock, volume };
 }
 
 /**
```

</details>

<details>
<summary>Binary patch for the verified release export (BSDIFF40, Base64)</summary>

```base64
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
```

</details>
