# VexqodeIMD: 4% trade fee and recipient

Research date: 2026-10-09 UTC.

## Answer

The requested fee is **4%**, payable to **`0x6bf192ebef135e0f645e99d59d9bf44e7711606c`**. The requester has now supplied the recipient that the prior job lacked. This resolves the documented recipient question; it does not establish that a contract implements the fee or that any fee has been paid.

## Facts and attributable evidence

| Finding | Evidence | Limit |
| --- | --- | --- |
| Fee rate is 4%; recipient is the address above. | Current requester message: “Fee Trade 4%” and “Fee recipient 0x6bf192ebef135e0f645e99d59d9bf44e7711606c”. | This is a requirement, not an on-chain observation. |
| Prior requested token is VexqodeIMD (VQI), with 1,000,000,000 tokens, 18 decimals, minted once to the deployer in the constructor. | Supplied project history, pinned input `063146a2-9000-4e7d-8c12-dc962efa5921:0`, section “History, oldest first”, job `04ac5ba1-624f-45f9-8f88-64c05541bd5f`. | Describes the earlier request; does not prove implementation. |
| Earlier job stopped because the recipient was unspecified and no requester-controlled owner was provided; the history identifies the launch deployer as a factory. | Same pinned history, “Stopped” entry. | Historical attribution only; factory configuration was not independently inspected. |
| No contract source, build configuration, ABI, deployment record, or site source was present among the ordinary project files inspected. | Local root listing and repository file inventory during this assignment; only administrative directories and the supplied input were present before this report. | No remote repository or chain was independently examined. |

The pinned history is `.imd/reads/project.md`, an input removed before delivery. Its relevant findings are preserved above so the report does not depend on that file remaining available. The history names https://github.com/identity-md-launches/launch-1120-vexqodeimd as the earlier delivery location; this report does not treat that uninspected URL as implementation evidence.

## Technical findings

ERC-20 defines transfers, delegated transfers, allowances, balances, supply, and events. It does not define a trade classifier or a standard trade-tax setting. Consequently, the phrase “trade fee” alone does not specify which token movements are taxable. This conclusion follows from the standard's interface and specification. [Primary source: ERC-20, Methods and Events](https://eips.ethereum.org/EIPS/eip-20).

If an eventual implementation uses OpenZeppelin Contracts 5.x, its documented customization point for transfer, mint, and burn behavior is `_update`; supply creation must be added by a derived contract. These are library capabilities, not evidence that this project uses that library. [Primary source: OpenZeppelin ERC20 API](https://docs.openzeppelin.com/contracts/5.x/api/token/erc20).

## Inferences and proposed interpretation

**Inference:** Supplying a fixed fee recipient removes the need to invent a fee recipient or give the factory configuration authority solely to answer the earlier recipient question. It does not authorize that address as owner, supply recipient, or administrator.

**Illustrative interpretation, not a confirmed requirement:** If the fee is deducted from the gross VQI amount, a taxable movement of 100 VQI would allocate 4 VQI to the supplied recipient and 96 VQI to the destination. A possible integer rule is `fee = floor(amount * 400 / 10000)`, with `net = amount - fee`, calculated in base units. Very small amounts can round to zero fees. The arithmetic follows directly from 4%; deduction, denomination, and rounding remain design choices.

The earlier supply request corresponds to `10^27` base units, by multiplying `10^9` tokens by `10^18` units per token. This is arithmetic derived from the pinned request, not a measured total supply.

## Uncertainty and unanswered questions

- Does “trade” include buys, sells, both, or every transfer? If limited to exchange trades, which chain and exchange/pool addresses define them?
- Is the fee deducted from the amount or charged in addition? Is it paid in VQI or converted into another asset?
- What exemptions and rounding policy apply, including minting, liquidity operations, wallet transfers, and transfers involving the fee recipient?
- Is the recipient immutable? If settings can change, who is the explicitly authorized controller?
- What contract address and chain, if any, should be inspected? No deployment is established by the supplied history or workspace.

The recipient string has the syntactic form of a 20-byte hexadecimal address. Its ownership, ability to receive or recover funds, account type, and chain-specific state were not verified. No chain was specified, so an explorer lookup on an arbitrarily chosen chain would not resolve these uncertainties.

## Validation and limits

Local checks verified the recipient's length and hexadecimal syntax, the 4% example and supply arithmetic, and the presence and UTF-8 readability of both deliverables. Primary technical references were opened during research. These checks do not certify contract behavior, ownership, deployment, security, or exchange compatibility. No contract was compiled, deployed, replaced, or minted; this assignment delivers a research report. An independent implementation or chain review would require actual source or deployment identifiers and resolved fee semantics.
