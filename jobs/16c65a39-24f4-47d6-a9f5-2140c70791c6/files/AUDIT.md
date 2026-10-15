# Audit report

> Audit the contracts in gimogo/NTTW as they are.

| | |
|---|---|
| Repository | https://github.com/gimogo/NTTW.git |
| Commit | `d063100b315c1936202970da9fd7a24a25aa0a2b` |
| Job | `16c65a39-24f4-47d6-a9f5-2140c70791c6` |
| Judged | 2026-10-15 16:55 UTC |
| Findings | 2 medium · 7 low · 5 info |

Four agents audited the code as it is at `d063100`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: Reward payout is a push loop inside the only write entry point: one winner the token refuses to pay bricks stampNote forever

`contracts/IMDRetroWall.sol:550`

```
                        if (!PAYMENT_TOKEN.transfer(winner, share)) {
```

_processEpochReset is reachable only from stampNote and pays all ten leaderboard addresses by push with PAYMENT_TOKEN.transfer, reverting on a false return (lines 550-552) and bubbling any revert from the token. epochStartTime and the board are only updated inside the same call, so if a single transfer fails, every later stampNote from any address re-enters the same branch (line 261) and fails again. The contract is ownerless with no claim, skip or sweep function, so there is no recovery: the wall is permanently unusable and the whole weeklyRewardPool plus every future fee is locked. The live NOTES token on Robinhood Chain (0x03b76ccf...6173) was checked over RPC and is a plain ERC-20 with no blocklist or pause, so the current deployment is not exposed today; severity is medium because the constructor accepts any ERC-20 (README: 'Any standard ERC-20'), the Base Sepolia path is not pinned to that token, and the common USDC/USDT-style blocklist or pausable behaviour turns one blocked winner into a permanent denial of service for everyone. The hardhat test named 'reverts the whole stamp if a reward transfer fails' never constructs a failing transfer, so this path has no coverage. Merged from audit_permissions and audit_economics. Fix that keeps the economics: credit a failed share to an unclaimed[winner] mapping (try/catch or low-level call) with a permissionless claimReward(), or move fully to pull-based claims; the epoch bump and board clear must not depend on ten external transfers succeeding.

**Reproduction**

State: wall deployed with an 18-decimal ERC-20 whose transfer reverts for a blocked address (mock in the proof; USDC-style). alice stamps once (rank 1), bob stamps once (rank 2), weeklyRewardPool = 1000e18. The token issuer blocks alice. Warp 7 days + 1 s. carol calls stampNote('gm', '#FFF2A5', 3, 3, 0). Expected: carol's note is stamped, currentEpoch becomes 2, bob receives 150e18, alice's share is held or skipped. Actual: the call reverts inside _processEpochReset at the transfer to alice ('blocked'), getTotalNotes stays 2, currentEpoch stays 1, and every future stampNote from any caller reverts the same way. Reproduced: forge test --match-path test/scratch/BlockedWinnerBricksWall.t.sol fails on this code with 'blocked' and passes on a copy patched to credit the failed share to an unclaimed mapping.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Test.sol";
import {IMDRetroWall} from "contracts/IMDRetroWall.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

/// @dev A plain ERC-20 (no transfer hooks, 18 decimals, returns bool) with a
///      USDC-style blocklist: transfers to/from a blocked address revert.
///      Everything else is standard.
contract BlocklistToken {
    string public name = "Blocklist Notes";
    string public symbol = "bNOTES";
    uint8 public decimals = 18;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    mapping(address => bool) public blocked;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    function setBlocked(address a, bool b) external {
        blocked[a] = b;
    }

    function mint(address to, uint256 amount) external {
        balanceOf[to] += amount;
        totalSupply += amount;
        emit Transfer(address(0), to, amount);
    }

    function approve(address spender, uint256 amount) external returns (bool) {
        allowance[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    function transfer(address to, uint256 amount) external returns (bool) {
        _move(msg.sender, to, amount);
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) external returns (bool) {
        uint256 allowed = allowance[from][msg.sender];
        require(allowed >= amount, "allowance");
        if (allowed != type(uint256).max) allowance[from][msg.sender] = allowed - amount;
        _move(from, to, amount);
        return true;
    }

    function _move(address from, address to, uint256 amount) internal {
        require(!blocked[from] && !blocked[to], "blocked");
        require(balanceOf[from] >= amount, "balance");
        balanceOf[from] -= amount;
        balanceOf[to] += amount;
        emit Transfer(from, to, amount);
    }
}

/// @title One blocked winner permanently bricks stampNote
/// @notice `_processEpochReset` pushes every winner's reward with a
///         `transfer` that must succeed, and it runs at the top of every
///         `stampNote` once the 7-day boundary has passed. If the payment
///         token refuses a transfer to a single leaderboard address, every
///         future stamp reverts with `RewardTransferFailed`, the epoch can
///         never advance, and the wall (ownerless, no other write path) is
///         dead forever. Expected: an unrelated user can still stamp after
///         the boundary and the other winners / the pool are unaffected.
contract BlockedWinnerBricksWallTest is Test {
    IMDRetroWall wall;
    BlocklistToken token;

    address alice = makeAddr("alice");
    address bob = makeAddr("bob");
    address carol = makeAddr("carol");

    string constant CONTENT = "gm";
    string constant COLOR = "#FFF2A5";

    function setUp() public {
        token = new BlocklistToken();
        wall = new IMDRetroWall(IERC20(address(token)));
        address[3] memory users = [alice, bob, carol];
        for (uint256 i = 0; i < users.length; i++) {
            token.mint(users[i], 1_000_000e18);
            vm.prank(users[i]);
            token.approve(address(wall), type(uint256).max);
        }
    }

    function test_blockedWinnerDoesNotBrickTheWall() public {
        // Epoch 1: alice is rank 1, bob rank 2. Pool = 2 * 500 = 1000 tokens.
        vm.prank(alice);
        wall.stampNote(CONTENT, COLOR, 1, 1, 0);
        vm.prank(bob);
        wall.stampNote(CONTENT, COLOR, 2, 2, 0);
        assertEq(wall.currentTopMinters(0), alice);
        assertEq(wall.weeklyRewardPool(), 1000e18);

        // The token issuer blocks alice (sanctions-style). Nothing the wall or
        // carol can do about it.
        token.setBlocked(alice, true);

        // Past the boundary: carol, who has nothing to do with alice, tries
        // to stamp. On the current code this reverts with
        // RewardTransferFailed(alice) and keeps reverting for every caller,
        // forever: the wall is bricked.
        vm.warp(block.timestamp + 7 days + 1);
        vm.prank(carol);
        wall.stampNote(CONTENT, COLOR, 3, 3, 0);

        // Expected after a fix (pull-based claims or skip-and-credit): the
        // stamp lands, the epoch advanced, and bob's 15% share is unaffected.
        assertEq(wall.getTotalNotes(), 3, "carol's note must be stamped");
        assertEq(wall.currentEpoch(), 2, "epoch must advance");
        assertEq(token.balanceOf(bob), 1_000_000e18 - 1000e18 + 150e18, "bob (rank 2) still gets 15%");
    }
}
```

### 2. Medium: tokenURI returns an unencoded data: URI; the raw '#' in every token name truncates the metadata for any URL-compliant consumer

`contracts/IMDRetroWall.sol:423`

```
        return string(abi.encodePacked("data:application/json,", json));
```

tokenURI concatenates 'data:application/json,' with raw JSON: no base64 and no percent-encoding. A non-base64 data URI is a URL (RFC 2397 / WHATWG URL): '#' starts the fragment and '%' begins a percent-escape. The header at line 371 hard-codes '"name":"IMD Note #<id>"' and the Color attribute carries the '#RRGGBB' string the frontend always sends, so every token's URI contains a raw '#' and standards-compliant consumers (browsers, fetch, new URL(), viem/ethers data-URI helpers, marketplace indexers) receive only '{"name":"IMD Note ' as the body, which is not valid JSON. A '%' in note content ('100% gm') is additionally percent-decoded into different text. The on-chain self-describing metadata, the headline feature of the ERC-721, is therefore unrenderable for all tokens. The hardhat test strips the prefix with String.replace and never runs the URI through a URL parser, which is why it passes. Merged from audit_permissions, audit_economics, audit_flow and audit_math. Fix: emit 'data:application/json;base64,' + Base64.encode(bytes(json)) (OpenZeppelin Base64 is in the vendored v5 library), or percent-encode '#', '%', '"', whitespace and non-ASCII bytes in the body.

**Reproduction**

Input: stampNote('100% gm', '#FFF2A5', 1, 1, 0) then tokenURI(0). Actual return (forge log): data:application/json,{"name":"IMD Note #0","description":...,{"trait_type":"Color","value":"#FFF2A5"},{"trait_type":"Content","value":"100% gm"},...}. Node 22: new URL(uri).pathname == 'application/json,{"name":"IMD Note ', new URL(uri).hash starts with '#0%22,%22description', and (await fetch(uri)).text() returns exactly '{"name":"IMD Note '; JSON.parse of it throws 'Unterminated string in JSON at position 18'. Expected: a URI whose body survives URL parsing and decodes to the full attributes JSON. Reproduced: forge test --match-path test/scratch/TokenURIDataUri.t.sol fails on this code with "raw '#' in data URI body" and passes on a copy that base64-encodes the body.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Test.sol";
import {IMDRetroWall} from "contracts/IMDRetroWall.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

/// Minimal standard ERC-20 (returns true, no hooks) so stampNote's fee pull works.
contract MockNotes {
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    function mint(address to, uint256 amount) external {
        balanceOf[to] += amount;
    }

    function approve(address spender, uint256 amount) external returns (bool) {
        allowance[msg.sender][spender] = amount;
        return true;
    }

    function transfer(address to, uint256 amount) external returns (bool) {
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) external returns (bool) {
        allowance[from][msg.sender] -= amount;
        balanceOf[from] -= amount;
        balanceOf[to] += amount;
        return true;
    }
}

/// tokenURI returns a `data:application/json,` URI whose body is neither
/// base64- nor percent-encoded. The fixed header `"name":"IMD Note #<id>"`
/// and the `#RRGGBB` color put a raw `#` into every URI, which any RFC 3986 /
/// WHATWG URL parser treats as the start of the fragment: the JSON body is
/// truncated and the metadata is unrenderable. A raw `%` in note content is
/// likewise mis-decoded. The test asserts the URI body is URL-safe (no raw
/// `#`, every `%` followed by two hex digits), which holds for either fix
/// (base64 body or percent-encoding) and fails on the code as it is.
contract TokenURIDataUriTest is Test {
    IMDRetroWall wall;
    MockNotes token;
    address alice = address(0xA11CE);

    function setUp() public {
        token = new MockNotes();
        wall = new IMDRetroWall(IERC20(address(token)));
        token.mint(alice, 1_000_000e18);
        vm.prank(alice);
        token.approve(address(wall), type(uint256).max);
    }

    function _isHex(bytes1 c) internal pure returns (bool) {
        return (c >= "0" && c <= "9") || (c >= "a" && c <= "f") || (c >= "A" && c <= "F");
    }

    function _assertUrlSafe(string memory uri) internal pure {
        bytes memory b = bytes(uri);
        bytes memory prefix = bytes("data:application/json");
        for (uint256 i = 0; i < prefix.length; i++) {
            assertEq(b[i], prefix[i], "unexpected scheme");
        }
        for (uint256 i = prefix.length; i < b.length; i++) {
            assertTrue(b[i] != "#", "raw '#' in data URI body: URL parsers truncate here");
            if (b[i] == "%") {
                assertTrue(i + 2 < b.length && _isHex(b[i + 1]) && _isHex(b[i + 2]), "raw '%' in data URI body");
            }
        }
    }

    function test_tokenURI_isUrlSafe_plainNote() public {
        vm.prank(alice);
        wall.stampNote("gm from the corkboard!", "#FFF2A5", 1, 1, 0);
        _assertUrlSafe(wall.tokenURI(0));
    }

    function test_tokenURI_isUrlSafe_percentInContent() public {
        vm.prank(alice);
        wall.stampNote("100% sure", "#FFF2A5", 1, 1, 0);
        _assertUrlSafe(wall.tokenURI(0));
    }
}
```

### 3. Low: Epoch settlement runs only inside a paid stampNote: a quiet wall never pays its last winners and the pool is stranded

`contracts/IMDRetroWall.sol:261`

```
        if (block.timestamp >= epochStartTime + EPOCH_DURATION) {
```

_processEpochReset is private and its only caller is stampNote, which pulls TOKEN_FEE (1000e18, 500e18 of it burned) from the caller. There is no permissionless settleEpoch() and no claim function, so once stamping stops the final epoch's winners are never paid and the balance sits in the ownerless contract with no exit. A winner who wants their payout must pay 1000 NOTES (500 burned) to trigger it, which is a net loss for every rank whose share is below 1000 NOTES (rank 1 needs a pool above ~3333 NOTES, rank 10 above 25000), and the trigger's own 500 NOTES then seed the next pool which has the same problem. During the gap timeUntilEpochEnd() reports 0 while currentEpoch, the board and weeklyRewardPool still describe the finished epoch. The README promises distribution 'enforced entirely on-chain, no off-chain payout runner', but it actually needs a new paying customer. Merged from audit_permissions, audit_economics and audit_math. Fix that preserves the economics: add an external settleEpoch() that reverts before the boundary and otherwise calls _processEpochReset(), keeping the lazy rollover in stampNote.

**Reproduction**

State: fresh wall at T; alice stamps once in epoch 1 (pool = 500e18, alice at rank 1, owed 150e18). Nobody stamps again. Warp T + 30 days. Expected: alice (or anyone) can settle epoch 1 at gas cost and alice receives 150e18. Actual (test/scratch/Explore.t.sol::test_settlement_requires_paid_stamp): timeUntilEpochEnd() == 0, currentEpoch() == 1, weeklyRewardPool() == 500e18, alice's balance unchanged; no function in the ABI moves the epoch or pays alice without a 1000e18 stampNote. When alice self-triggers she pays 1000e18, receives 150e18 (net -850e18 for that call) and the pool becomes 850e18, again uncollectable without another paid stamp.

### 4. Low: getNotes panics on offset + limit overflow instead of clamping the page

`contracts/IMDRetroWall.sol:330`

```
        uint256 end = offset + limit;
```

The NatSpec promises the slice [offset, min(offset + limit, total)) and the code clamps end to total, but offset + limit is computed in checked arithmetic before the clamp. Any caller that passes a very large limit (the natural 'everything from offset' request, e.g. type(uint256).max) with a non-zero offset gets Panic(0x11) instead of the clamped slice, while offset == 0 works, so the behaviour is inconsistent across offsets. No funds are at risk; it is a public read-API defect that breaks third-party readers and indexers. Merged from audit_flow and audit_math. Fix: uint256 end = limit > total - offset ? total : offset + limit;

**Reproduction**

State: three notes stamped. getNotes(0, type(uint256).max) returns 3 notes. getNotes(1, type(uint256).max): expected a 2-element page [note 1, note 2]; actual revert with panic 0x11 (arithmetic overflow). Reproduced: forge test --match-path test/scratch/GetNotesOverflow.t.sol fails on this code with 'panic: arithmetic underflow or overflow (0x11)' and passes on a copy with the clamp computed before the addition.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Test.sol";
import {IMDRetroWall} from "contracts/IMDRetroWall.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract MockNotes2 {
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    function mint(address to, uint256 amount) external {
        balanceOf[to] += amount;
    }

    function approve(address spender, uint256 amount) external returns (bool) {
        allowance[msg.sender][spender] = amount;
        return true;
    }

    function transfer(address to, uint256 amount) external returns (bool) {
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) external returns (bool) {
        allowance[from][msg.sender] -= amount;
        balanceOf[from] -= amount;
        balanceOf[to] += amount;
        return true;
    }
}

/// getNotes documents "Slice [offset, min(offset + limit, total))" and clamps
/// `end` to `total`, but computes `offset + limit` in checked arithmetic first,
/// so a large `limit` (a natural "give me everything from offset" request)
/// panics with 0x11 instead of returning the clamped slice.
contract GetNotesOverflowTest is Test {
    IMDRetroWall wall;
    MockNotes2 token;
    address alice = address(0xA11CE);

    function setUp() public {
        token = new MockNotes2();
        wall = new IMDRetroWall(IERC20(address(token)));
        token.mint(alice, 1_000_000e18);
        vm.startPrank(alice);
        token.approve(address(wall), type(uint256).max);
        wall.stampNote("one", "#FFF2A5", 1, 1, 0);
        wall.stampNote("two", "#FFF2A5", 2, 2, 0);
        wall.stampNote("three", "#FFF2A5", 3, 3, 0);
        vm.stopPrank();
    }

    function test_getNotes_largeLimitIsClamped() public view {
        IMDRetroWall.Note[] memory page = wall.getNotes(1, type(uint256).max);
        assertEq(page.length, 2);
        assertEq(page[0].id, 1);
        assertEq(page[1].id, 2);
    }
}
```

### 5. Low: Last-second sybil entries can take 100% of the weekly pool, including every honest stamper's contribution

`contracts/IMDRetroWall.sol:464`

```
            if (holder == address(0) || noteCountPerEpoch[currentEpoch][holder] < newCount) {
```

Rank is decided purely by per-epoch stamp count per msg.sender, the board (getCurrentTopMinters) and the boundary (timeUntilEpochEnd) are public, ties favour the earlier arrival, and ten addresses fill every paying slot. There is no per-address cap, no minimum participation, no sybil cost beyond the fee and no randomisation, so an actor who waits until the last second of the epoch knows the exact count needed per sybil (max honest count + 1) to out-rank every honest entry and collect 30+15+15+8+8+8+4+4+4+4 = 100% of the pool: the 500-NOTES pool share of every honest stamp plus any rolled-over remainder from quieter weeks. Profit condition for a full-board capture is 500*H > 10000*(c+1), with H honest stamps and c the highest honest count; for rank 1 alone 150*H > 850*(c+1). This is the agreed by-count design rather than a permission bypass, so it is recorded as a low-severity economic risk the requester should accept explicitly or redesign; any change (pro-rata by stamps, per-address cap, minimum distinct minters, fixed schedule) alters the stated economics and is a scoped decision. Merged from audit_economics, audit_flow and the audit_permissions trust-assumption note.

**Reproduction**

State: 100 distinct honest users each stampNote once in epoch 1 (pool = 50_000e18, every honest count = 1). At epochStartTime + 7 days - 1 s an attacker with 10 fresh addresses stamps twice from each (20_000e18 spent; pool = 60_000e18; board = the 10 sybils with count 2). At epochStartTime + 7 days the attacker stamps once more (1_000e18), which runs _processEpochReset. Expected under 'reward for the top stampers of the week': honest participation is rewarded. Actual (test/scratch/Explore.t.sol::test_snipe_full_board, logs 'spent: 21000', 'received: 60000'): the 10 sybils receive 60_000e18 in total for 21_000e18 spent, net +39_000e18; every honest user's balance stays at initial - 1_000e18.

### 6. Low: stampNote accepts '0xRRGGBB' colors that the frontend and metadata cannot render

`contracts/IMDRetroWall.sol:683`

```
        } else if (b.length == 8 && b[0] == "0" && b[1] == "x") {
```

_isValidHexColor accepts an alternate 8-byte '0xRRGGBB' form, but the stored string is used verbatim as a CSS color by the board (src/components/StickyNote.tsx line 94: background: note.color) and emitted verbatim in the tokenURI Color trait. '0xFFF2A5' is not a CSS color, so a note stamped with it renders with no paper background for every viewer, and marketplaces show a meaningless Color trait. The README and the Note.color comment (line 143) document '#RRGGBB' only, and the UI palette is not a guard because anyone can call the contract directly. The hardhat test 'accepts 0x-prefixed and uppercase hex colors' codifies the behaviour. From audit_flow. Fix: accept only the 7-byte '#RRGGBB' form, or normalise '0x' to '#' before storing.

**Reproduction**

Call stampNote('hi', '0xFFF2A5', 100, 100, 0) directly. Expected: InvalidColor revert, or a stored '#FFF2A5'. Actual (test/scratch/Explore.t.sol::test_0x_color_accepted): the call succeeds and getNote(0).color == '0xFFF2A5'; the board sets background: '0xFFF2A5', which CSS ignores, and tokenURI contains {"trait_type":"Color","value":"0xFFF2A5"}.

### 7. Low: Composer enforces 280 UTF-16 code units while the contract enforces 280 UTF-8 bytes; valid-looking notes revert on-chain after signing

`src/components/NoteComposer.tsx:96`

```
  const overLimit = trimmed.length > MAX_CONTENT_LENGTH;
```

The composer gates the stamp button and the counter on JavaScript String.length (UTF-16 code units) against MAX_CONTENT_LENGTH = 280 (src/lib/board.ts line 19), but stampNote checks bytes(_content).length > 280 (UTF-8 bytes, contracts/IMDRetroWall.sol line 268). Non-ASCII characters are 2 to 4 bytes each, so a note the UI shows as e.g. 200/280 can be 400 bytes; the UI submits it (after the approve step) and the paid transaction reverts with ContentTooLong, so the user sees an opaque error after signing. The README advertises '280 characters max', which the contract does not implement. Merged from audit_flow and audit_math. Fix: count new TextEncoder().encode(trimmed).length in the UI and state the limit as bytes (or document the byte limit in the contract NatSpec and README).

**Reproduction**

Input: 200 x 'é' (U+00E9). JS: 'é'.repeat(200).length == 200 <= 280, so overLimit is false, canStamp is true and the counter shows 200/280; TextEncoder gives 400 bytes. Contract: stampNote with that 400-byte content reverts ContentTooLong(400) (test/scratch/Explore.t.sol::test_utf8_bytes_vs_chars, expectRevert matched). Expected: the composer blocks or warns about anything the contract rejects. Same for 140 pushpin emoji: length 280, bytes 560.

### 8. Low: Content is not validated as UTF-8, so invalid bytes produce unparseable on-chain JSON metadata

`contracts/IMDRetroWall.sol:268`

```
        if (len > MAX_CONTENT_BYTES) revert ContentTooLong(len);
```

stampNote checks only the byte length of _content. _jsonEscape is documented as making 'any valid UTF-8 note' legal JSON, but nothing ensures the input is valid UTF-8: a lone 0xFF or an unterminated multi-byte sequence is stored, emitted in NoteCreated and copied byte-for-byte into the tokenURI JSON. JSON (RFC 8259) must be UTF-8, so that token's metadata fails to decode in strict decoders and the frontend's event decoding substitutes replacement characters. Only the author's own token is affected, which keeps this low. From audit_flow. Fix: validate UTF-8 on-chain (a byte walk over at most 280 bytes), or base64-encode the metadata and document content as opaque bytes.

**Reproduction**

Input: stampNote with content = the single byte 0xff and color '#FFF2A5'. Expected: revert (invalid UTF-8) or JSON-safe output. Actual (test/scratch/Explore.t.sol::test_invalid_utf8_accepted): the stamp succeeds and tokenURI(0) contains the raw 0xFF byte inside the Content value (forge prints it as a replacement character); decoding the body as UTF-8 JSON fails in strict decoders.

### 9. Low: @openzeppelin/contracts is imported but not declared, so a fresh clone cannot compile or test the contract

`contracts/IMDRetroWall.sol:4`

```
import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
```

The contract imports five OpenZeppelin files, but package.json lists no @openzeppelin/contracts and pnpm-lock.yaml contains no openzeppelin entry (hardhat-toolbox does not pull it in). The documented 'npm install && npm run compile / npm test' path therefore fails at import resolution and the hardhat suite never runs from a clean checkout. The code also requires the v5 API (_update(address,uint256,address) and _increaseBalance(address,uint128) overrides, ERC721Enumerable hooks), yet no major version is pinned anywhere, so the library revision the live deployment was built with is unrecorded. Merged from audit_flow and audit_math. Fix: add "@openzeppelin/contracts": "5.0.2" (or the exact version used for the deployment) to devDependencies and regenerate the lockfile.

**Reproduction**

State: checkout at d063100. grep -c openzeppelin pnpm-lock.yaml prints 0 and package.json has no @openzeppelin entry, while contracts/IMDRetroWall.sol lines 4-8 import @openzeppelin/contracts/... . Expected: npm install provides the import and npm run compile builds artifacts. Actual: hardhat fails at import resolution (HH404/HH411 'library @openzeppelin/contracts ... is not installed'). For this review the contract was compiled only by supplying OpenZeppelin v5.0.2 from outside the repository.

### 10. Info: Lazy rollover re-anchors the epoch to the triggering stamp, so epochs are not fixed 7-day weeks and view functions go stale after the boundary

`contracts/IMDRetroWall.sol:541`

```
        epochStartTime = block.timestamp;
```

NatSpec (line 126) says 'One epoch lasts exactly 7 days' and the README says 'Time is split into 7-day epochs', but the rollover sets epochStartTime to the triggering block's timestamp and bumps currentEpoch by exactly one regardless of how many weeks elapsed. An epoch therefore lasts 7 days plus the idle time until the next stamp, several missed weeks collapse into one settlement, and during the gap currentEpoch, getCurrentTopMinters, weeklyRewardPool and noteCountPerEpoch describe a finished epoch while timeUntilEpochEnd() returns 0. After the boundary the board is frozen (every stamp runs the reset first), so this cannot change winners; it is a documented-versus-actual mismatch for the frontend and for anyone timing stamps to a calendar week. Merged from audit_permissions, audit_economics and audit_flow. Fix if alignment is wanted: epochStartTime += EPOCH_DURATION * ((block.timestamp - epochStartTime) / EPOCH_DURATION) and advance currentEpoch by the same count, or document the lazy semantics.

**Reproduction**

State: deploy at T; alice stamps at T; nobody stamps until T + 20 days; alice stamps. Expected per NatSpec: boundaries at T+7d, T+14d, T+21d. Actual (test/scratch/Explore.t.sol::test_epoch_drift): currentEpoch() == 2, epochStartTime() == T + 20 days and timeUntilEpochEnd() == 7 days, so epoch 2 runs T+20d..T+27d; between T+7d and T+20d currentEpoch() == 1 while timeUntilEpochEnd() == 0.

### 11. Info: stampNote NatSpec states the burn and pool shares are 50 tokens; the constants are 500

`contracts/IMDRetroWall.sol:238`

```
     *           - `TOKEN_FEE_BURN_SHARE` (50 tokens) is pulled from
```

Lines 238-241 document TOKEN_FEE_BURN_SHARE and TOKEN_FEE_POOL_SHARE as '50 tokens', left over from an earlier fee schedule. The constants at lines 107-115 are 500e18 each (1000-token fee), which matches the README, the frontend and the live deployment. Stale documentation on the only paid path misleads integrators who read the ABI docs. From audit_flow. Fix: change both to 500.

**Reproduction**

Read lines 238-241 against lines 107-115: TOKEN_FEE = 1000e18, TOKEN_FEE_BURN_SHARE = TOKEN_FEE / 2 = 500e18, TOKEN_FEE_POOL_SHARE = 500e18; the comment says 50 tokens for each. Expected: NatSpec matches the constants.

### 12. Info: Tokens sent directly to the wall are untracked and permanently stranded (ownerless design, no sweep)

`contracts/IMDRetroWall.sol:165`

```
    uint256 public weeklyRewardPool;
```

weeklyRewardPool is an internal counter incremented only by stampNote; payouts are computed from the counter and PAYMENT_TOKEN.balanceOf(address(this)) is never read. Any NOTES transferred straight to the contract (a user confusing 'send 1000 NOTES' with approving, an airdrop, a tip) is excluded from every distribution and, with no owner, no sweep and no donate()/syncPool() function, can never leave. Nothing else is harmed because payouts are bounded by the counter. This is a consequence of the intended ownerless design and is recorded as a trust assumption; merged from audit_economics and audit_flow. If unwanted: a permissionless syncPool() folding the surplus into weeklyRewardPool, or documenting that direct transfers are burned.

**Reproduction**

State: alice calls PAYMENT_TOKEN.transfer(wall, 100e18), then stamps once; warp 7 days; alice stamps again (rollover pays alice 150e18). Expected (naive user): the 100e18 is in the pool or recoverable. Actual (test/scratch/Explore.t.sol::test_direct_transfer_stranded): balanceOf(wall) - weeklyRewardPool() == 100e18 after the rollover and no function in the ABI can move it.

### 13. Info: Hardhat test 'reverts the whole stamp if a reward transfer fails' never induces a failing transfer; the revert and brick path is untested

`test/IMDRetroWall.ts:593`

```
    it("reverts the whole stamp if a reward transfer fails", async function () {
```

The test's name claims coverage of the RewardTransferFailed path (contract lines 550-552), but its body (lines 598-609) only stamps alice and bob, warps, stamps carol with the always-succeeding mock, and asserts the epoch advanced; its own comment admits the failing case was not built. Deleting the revert check or making transfer return false would not fail this test. The TokenTransferFailed branches (lines 294-302) are likewise never reached through a false return, and _safeMint to a non-receiver contract, reentrancy from onERC721Received, a rollover whose trigger is itself a winner, and a settlement with no later stamp are untested. Merged from audit_economics and audit_flow. Fix: give the in-memory mock a blocked/returns-false flag and assert RewardTransferFailed with unchanged epoch, pool and board, plus the permanent failure on later stamps; or rename the test to what it checks.

**Reproduction**

Read test/IMDRetroWall.ts lines 593-610: no transfer is made to fail anywhere in the suite. Expected: a test with that name makes PAYMENT_TOKEN.transfer return false or revert and asserts RewardTransferFailed. Actual: the body performs a normal successful rollover and checks currentEpoch == epochBefore + 1.

### 14. Info: Trust assumptions of the ownerless design: PAYMENT_TOKEN is immutable and its decimals are not checked against the hardcoded 18-decimal fee

`contracts/IMDRetroWall.sol:226`

```
        PAYMENT_TOKEN = _paymentToken;
```

Entry-point inventory: the only project-defined state-changing function is stampNote (unrestricted); inherited ERC-721 approve/setApprovalForAll/transferFrom/safeTransferFrom are owner/operator-gated by OpenZeppelin v5; there is no receive, fallback, initializer, proxy, owner or role. The constructor pins PAYMENT_TOKEN and epochStartTime and only rejects address(0). TOKEN_FEE = 1000e18 and every share constant assume an 18-decimal, non-hooked, non-fee, non-blocklisting ERC-20 that returns a bool, as the NatSpec at lines 100-102 says, but nothing enforces decimals() == 18 or the other properties. The live NOTES token (chain 4663, 0x03b76ccf...6173) returns decimals() == 18 over RPC and exposes only the standard ERC-20 selectors, so the pinned deployment satisfies the assumption; this is recorded for any redeploy. Merged from audit_math and the audit_permissions inventory; no permission bypass was found. Suggested guard: require IERC20Metadata(_paymentToken).decimals() == 18 in the constructor, or derive TOKEN_FEE from decimals().

**Reproduction**

State: deploy IMDRetroWall with a 6-decimal ERC-20. stampNote then requires an allowance and balance of 1000e18 base units = 10^15 whole tokens, so every stamp reverts on transferFrom for any realistic holder. Expected per NatSpec: the constructor refuses a token whose decimals() != 18. Actual: the constructor only checks address(0) (lines 222-226).

---

Judge's submission `1ea05c56c2c97dde0383d1363062d86ea2aafb721fc478765e5805aa0f6561cc`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
