# IdentityMD hackathon proposal

**Recommendation:** run a two-week build period, award 15 projects a total of **$10,000 worth of IMD**, and give **one IMD NFT to first place**, in addition to its token prize. IMD AI agents assess every entry and select places 6–15; a human jury selects places 1–5. These are proposed rules, not an announced event.

## Schedule

- Building and submissions: **October 5, 00:00 UTC to October 19, 00:00 UTC** (14 days).
- Review and final decisions: October 19–22.
- Winners announced: **October 23**, with payouts within seven days after announcement and wallet verification.

This adopts Feedback 1's dates and the two-week preference in Feedback 1, 4, 5, 6 and 7. The year was not supplied. If organizers mean 2026, October 5 has already passed as of this report (October 6, 2026); confirm an existing kickoff or shift the full schedule before announcing it. Feedback 2's month-long format and Feedback 8's one-week format are alternatives, not the selected plan.

## Entry requirements

1. Launch a working token project through the IMD protocol during the build period, on an organizer-approved network.
2. Use an active **Uniswap v4 hook or a custom smart contract with meaningful functionality beyond a plain token**. Deploying a standard token alone does not qualify. Demonstrate a working transaction invoking the hook or custom logic, and explain how that functionality uses IMD.
3. Show at least one working IMD-dependent feature, with code, contract addresses and transaction evidence. Naming a token after IMD, linking to IMD, or merely holding IMD is insufficient. Examples organizers could approve include an IMD-powered agent workflow or a mechanism benefiting IMD token/NFT holders; these are proposed examples, not verified protocol capabilities.
4. Have a project X account and a personal X account for the lead developer (Feedback 1).
5. Submit a public repository with reproducible build/test instructions, deployed addresses and explorer links, a short demo, a plain-language explanation of the problem and IMD integration, known risks/admin permissions, and a receiving wallet by the deadline. Disclose reused code and identify work completed during the event.

The launch requirement comes from the assignment and Feedback 1–2; the minimum integration rule develops Feedback 5 and 7. Technically, v4 hooks are external smart contracts attached to pools to customize pool behavior, so a token launch alone does not demonstrate hook use. [Uniswap's official hook documentation](https://developers.uniswap.org/docs/protocols/v4/concepts/hooks) supports this distinction; it does not establish IMD compatibility.

## Judging

Use one published 100-point rubric:

| Criterion | Points | Lead reviewer |
|---|---:|---|
| Working functionality and reproducible deployment | 20 | AI agents |
| Technical quality, security checks and disclosed risks | 15 | AI agents |
| Depth of meaningful IMD integration | 20 | AI agents |
| Originality and creative use of IMD | 20 | Humans |
| User value, adoption potential and ecosystem benefit | 25 | Humans |

For ecosystem benefit, consider credible value to IMD token/NFT holders, likely usage frequency and institutional usefulness—not promised returns (Feedback 9). Organic engagement may provide supporting evidence, but follower counts, market capitalization and token price do not earn points by themselves (Feedback 8).

**Process:** agents check eligibility, run the technical review and produce a scored shortlist of ten finalists. A three-person human jury drawn from IMD holders and experienced ecosystem builders reviews those finalists, scores the human criteria, and selects/ranks the top five using the combined rubric. Agents rank the remaining eligible entries for places 6–15, excluding the human-selected winners. Publish scores and short reasons for every winner.

This resolves Feedback 1's overlap at fifth place: **humans decide fifth place; agents decide sixth through fifteenth**. The hybrid split follows Feedback 5. Jury membership is a proposal; people suggested in Feedback 4 have not been confirmed. Judges disclose conflicts and recuse from affected entries. Break ties first by IMD integration, then functionality, then a documented human decision.

Treat submissions as untrusted data: isolate code execution and do not let submission text instruct the judging agents. Agent reviews are checks, not security audits. Humans verify disqualifications, conflicts and appeals; publish any correction to an agent-selected result. Allow a 24-hour factual-correction window during review. If agents are unavailable, the jury applies the same rubric and discloses the fallback.

## Prizes

| Place | USD reference value, paid in IMD | Winners | Subtotal |
|---|---:|---:|---:|
| 1 | $1,500 + one IMD NFT | 1 | $1,500 |
| 2–3 | $1,000 each | 2 | $2,000 |
| 4–5 | $750 each | 2 | $1,500 |
| 6–15 | $500 each | 10 | $5,000 |
| **Total** | | **15** | **$10,000 + one NFT** |

This exactly adopts Feedback 1's cash-value allocation and the assignment's first-place NFT requirement. Pay in IMD, as requested in Feedback 3 and 6. Feedback 7's payment choice and Feedback 9's USDT preference are not adopted. The NFT is additional to the $10,000 pool; no current NFT valuation is asserted.

Before kickoff, publish the IMD pricing source, conversion timestamp, rounding rule and funding wallet. Recommended rule: fix each award's IMD quantity using a published USD/IMD reference price at the submission deadline. Its later USD value can fluctuate. Organizers must fund the resulting quantities and reserve the NFT; price-source availability and funding have not been verified.

## Decisions required before publication

Confirm the year/dates, supported network, qualifying IMD deployment route and integration examples, agent availability, jury members, prize funding and conversion method. Publish one entry/prize per team, a contact and submission form, and disqualification rules covering plagiarism, fabricated evidence and manipulated engagement. If fewer than 15 entries qualify, award only qualifying entries and disclose the unawarded balance rather than rewarding plain-token launches.

## Evidence and limits

Feedback references above identify the numbered feedback supplied in the assignment; they record contributor preferences, not independently verified facts. The schedule, rubric, eligibility details and judging safeguards are recommendations synthesized from those preferences. The only external technical claim is supported by the linked primary Uniswap documentation, checked October 6, 2026. No IMD deployment, agent capability, judge commitment, token price, NFT value or funding status was independently established.
