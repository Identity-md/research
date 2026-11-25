# L-meta-2582 — a read-2 circuit at minimum size

**L-meta-2582 remains open in these results.** All four inputs report `missing_lemma`. None supplies a Lean proof of the unconditional theorem or a counterexample. The results contain no record of another holder checking a completed proof and no contributor pull request to `open-goat/pequalnp-proofs`. Each Lean check below is attributed to the result that reports it. [Angle 1], [Angle 2], [Angle 3], [Angle 4]

## The theorem and the checked reduction

Let `I p l` mean that point `p` lies on line `l` in the projective plane of the step, with order `q ≥ 2` and `N = q² + q + 1`. The function `F` accepts an input exactly when it selects both endpoints of some incidence. For every binary AND/OR circuit `C` computing `F`, the goal asks for a binary AND/OR circuit `D` computing `F` with `D.size ≤ C.size` and `IsReadK (N+N) D 2`. Equivalently, some minimum-size circuit for `F` must be read-2. [Angle 1], [Angle 3], [Angle 4]

Angles 1 and 2 report checking in Lean 4.36.0 that the prime implicants of any circuit computing `F` are exactly the sets `{Fin.castAdd N p, Fin.natAdd N l}` for incident `p,l`. Each such pair suffices to make `F` true, either singleton fails, and every accepting input contains such a pair. Angle 1 also checked that `ReadK.setList` lists its wires as `[p.val, N + l.val]`. Thus read-2 asks for one accepting proof tree per incident pair in which each endpoint is read at most twice. Different pairs may use different trees. [Angle 1], [Angle 2], [Angle 3], [Angle 4]

The remaining obligation can be stated precisely in either of two ways.

- **Minimum size (`Hcut`).** Given a least-size `IsAO2` circuit for `F`, produce an `IsAO2` circuit for `F` of the same size that passes `readsAtMost` at 2 on every incident pair. Angles 1 and 3 report checking the reduction to a least circuit by minimizing gate count with `Nat.find`. [Angle 1], [Angle 3]
- **Descent (`MOVE`).** Define `bad(D)` as the number of incidences failing that test. Angle 2 checked that read-2 is equivalent to `bad(D) = 0`. It also checked that the theorem follows if every failing circuit can be replaced by one computing the same function, still `IsAO2`, with fewer gates or with the same number of gates and fewer bad pairs. Induction on size and then on `bad` closes the proof *assuming* this replacement. Constructing the replacement is the missing step. [Angle 2]

## What the star construction settles

For each line, OR together its `q+1` points using `q` gates, then AND that result with the line input. Joining all line outputs takes another `N−1` OR gates, giving `N*(q+2)−1` gates in total. For an incident pair, the branch for its line can choose its point and read each endpoint once. Angle 3 states the general Lean construction as lemma A and reports that it was not formalized. Its checked reduction shows that, given A, the only outstanding case is a least circuit `C` with `C.size + 1 < N*(q+2)`. A matching lower bound on all circuits for `F` would suffice. The theorem also allows a smaller read-2 circuit if one exists. [Angle 1], [Angle 2], [Angle 3], [Angle 4]

For the Fano plane (`q = 2`, `N = 7`), Angles 1 and 4 report Lean evaluations on all **16,384 inputs** and all **21 incidences**. The 27-gate star circuit computes `F` and is read-1. It therefore witnesses the conclusion for every Fano circuit of size at least 27. Two distinct 29-gate circuits show why returning the given circuit can fail. Replacing point input `x₀` by `(x₀ ∧ x₀) ∧ x₀` fails the read-2 test on its three incidences and passes at 3. Duplicating one line's AND output by squaring it twice fails at 2 on that line's pairs and passes at 4. Both still compute `F`, and the 27-gate circuit witnesses the theorem for both. [Angle 1], [Angle 4]

## Why the replacement is still open

The proposed proof rearranges a least circuit into an OR of blocks `u ∧ v`, each of which accepts only inputs satisfying `F`. A monotone replacement circuit computes `F` if it still has this upper bound and accepts the input consisting of each incident pair alone. For a block accepting just one incident pair, the proposed move redirects its final gate to AND the two endpoints. For a block accepting several pairs, the cost argument must account for gates shared with other blocks. One proposed sufficient inequality is that the number of gates exclusive to the block covers the cost of stars for the pairs accepted only by that block. [Angle 1], [Angle 2], [Angle 4]

Angle 3 observes that two points on two common lines are impossible, which forces a star when the two operands accept the corresponding singleton inputs. This leaves cases where an operand itself needs both endpoints. Angle 4 proposes proving that, after rearrangement, each operand has a tree reading each endpoint at most once, giving the block a bound of two. The results leave both the general rearrangement and the argument for the remaining blocks unproved in Lean. [Angle 1], [Angle 2], [Angle 3], [Angle 4]

Angle 2 checked the obstacle on an eight-input block. On all 256 inputs its output implies the incidence function. It accepts just one of six incident pairs, and each of its four factors is necessary to keep it below the function. That pair fails the read test at 2 and passes at 3. Repointing the last AND directly to its endpoints keeps the gate count and passes at 1. This verifies the move for that block. A separate majority-shaped block passes at 2 and fails at 1. Angle 3 also reports a two-point, two-line toy instance where duplicating a point read changes a read-1 star into a circuit that fails at 2 while computing the same function. [Angle 2], [Angle 3]

Angle 4's SAT search found an eight-gate read-1 optimum for the order-1 triangle, outside the hypothesis `q ≥ 2`. It reports star-cover optima on the four- and five-edge paths, two Fano lines, a three-arm spider and a six-cycle with a pendant edge. The ten-gate searches for an eight-cycle and for three Fano lines were inconclusive, with eleven-gate circuits found for each. The **26-gate Fano search was also inconclusive**. The finite results therefore leave even the minimum Fano gate count undetermined. [Angle 4]

[Angle 1]: ../items/angle-1/result.json
[Angle 2]: ../items/angle-2/result.json
[Angle 3]: ../items/angle-3/result.json
[Angle 4]: ../items/angle-4/result.json
