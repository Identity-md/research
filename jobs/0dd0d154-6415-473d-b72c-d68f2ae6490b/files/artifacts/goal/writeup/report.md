# L-meta-3566 · Vertex deletion in a binary monotone circuit

**The proof is open in all four results.** Each source record gives the status `missing_lemma`. None supplied a Lean 4 theorem for the posted step, an acceptance record from another holder checking that theorem, or a pull request by the proving contributor on `open-goat/pequalnp-proofs`. The shared mathematical gap is a gate lower bound for arbitrary binary AND/OR circuits. [A1](#a1) · [A2](#a2) · [A3](#a3) · [A4](#a4)

The public issue and PR search returned zero matches for the step ID. The repository tree at commit `c62fbcc7d8c3d7f5388a4f5ccb71b26bb9395272` also contained no path with `3566` in its name. These checks concern the identifier and filenames. The desk accepts a proof by checking the exact Lean statement against its pinned toolchain and Mathlib, with restricted imports, no proof holes, and only `propext`, `Classical.choice` and `Quot.sound` as axioms. The scratch Lean results below are attributed to the contributors. Their files and checker transcripts are absent from the four records. [Issue and PR search](https://api.github.com/search/issues?q=repo%3Aopen-goat%2Fpequalnp-proofs%20L-meta-3566) · [Inspected tree](https://api.github.com/repos/open-goat/pequalnp-proofs/git/trees/c62fbcc7d8c3d7f5388a4f5ccb71b26bb9395272?recursive=1) · [Desk checker requirements](https://github.com/open-goat/pequalnp-proofs/blob/c62fbcc7d8c3d7f5388a4f5ccb71b26bb9395272/README.md#what-the-checker-requires) · [A1](#a1) · [A2](#a2) · [A3](#a3) · [A4](#a4)

## The missing inequality

Write `m(G)` for the number of edges and `τ(G)` for the minimum vertex-cover size. The edge function is true when the selected vertices contain both ends of an edge. An AO2 circuit computes with binary AND and OR gates. For a bipartite, four-cycle-free graph with at least two edges, the step calls for a positive-degree vertex `z`. Deleting its incident edges gives the graph `H` on the same vertices. For every AO2 circuit `C` computing the edge function of `G`, there must be a circuit `D` computing the edge function of `H` with

```text
size(D) + degree(z) ≤ size(C)
size(D) + degree(z) + 1 ≤ size(C)   if τ(H) < τ(G).
```

The cover drops exactly when some minimum cover of `G` contains `z`. Removing `z` from that cover saves a vertex in `H`. In the other direction, adding `z` to a minimum cover of `H` covers `G`, so any drop is exactly one. A witness chosen using a least-size computing circuit works for every larger circuit of the same function. This preserves the requirement that the vertex work for every circuit. [A1](#a1) · [A2](#a2) · [A3](#a3) · [A4](#a4)

**Equivalent lower bound.** For every bipartite, four-cycle-free graph with an edge and every AO2 circuit `C` computing its edge function, the missing statement is

```text
m(G) + τ(G) ≤ size(C) + 1.
```

A2, A3 and A4 report proving the equivalence in scratch Lean. Their two directions explain exactly where a general proof would enter. [A2](#a2) · [A3](#a3) · [A4](#a4)

- **From the bound to deletion.** Choose an endpoint of one edge outside a second edge. Deleting there leaves the second edge in `H`. Assign each edge of `H` to one of its endpoints in a minimum cover. A centre with `k > 0` assigned edges uses `k − 1` OR gates on the neighbours and one AND gate with the centre. Combining the nonempty stars takes one fewer OR than the number of stars. Hence `size(D) + 1 ≤ m(H) + τ(H)`. Substituting `m(H) = m(G) − degree(z)` and applying the bound for `C` gives `size(D) + degree(z) + (τ(G) − τ(H)) ≤ size(C)`. This pays for both requested savings. [A2](#a2) · [A3](#a3) · [A4](#a4)
- **From deletion to the bound.** Induct on the number of edges. A single edge requires at least one gate. With at least two edges, apply the step. When an edge survives, the induction bound for `D` pays for `m(H) + τ(H)`, the degree saving pays for the deleted edges, and the bonus pays for a strict cover drop. If deletion removes all edges, `{z}` covers the nonempty graph, `m(G) = degree(z)`, and the degree saving alone gives the lower bound. [A2](#a2) · [A3](#a3) · [A4](#a4)

## What the restriction argument establishes

Setting `x_z = false` computes the edge function of `H`. Scan the gates in order, representing each old wire by false or a surviving wire. With a false operand an AND vanishes and an OR forwards its other operand. If `r(z,C)` counts distinct gate positions reading `z` directly, this gives `size(D) + r(z,C) ≤ size(C)`. Every positive-degree input has a reader, since toggling that input beside a single neighbour can change the output. The remaining issue is how to save the full degree and, when necessary, one further gate. [A1](#a1) · [A2](#a2) · [A3](#a3)

| Case | Saving established in the source |
| --- | --- |
| Leaf in no minimum cover | One direct reader suffices. The cover size stays fixed. Either of two leaves with a common neighbour qualifies. [A1](#a1) · [A2](#a2) · [A3](#a3) |
| Isolated edge with another edge surviving | Setting one endpoint true makes the other a singleton term. Then setting that endpoint false removes the edge. Each restriction saves a gate, giving the degree saving and the bonus. [A2](#a2) · [A4](#a4) |
| A gate on two distinct primary inputs | If one input is `z` with degree at least two, A1 forces a second direct reader by holding the gate fixed while toggling the edge function. [A1](#a1) |
| Every reader of `z` is an OR with a same-colour primary input or an AND with an opposite-colour primary input | For each neighbour, A3 exhibits an input where turning on `z` forces a first changing gate. The four-cycle exclusion prevents two neighbours charging the same OR partner. At an AND the partner has to be the neighbour itself. This pays the degree. Internal partners and the cover bonus remain open in this argument. [A3](#a3) |
| Fewer edges than nonisolated vertices | A4 reports the full deletion conclusion under this condition, which includes forests with edges. The degree sum gives more leaves than vertices of degree at least three. Shared neighbours and isolated edges give the cases above. Otherwise a leaf has a degree-two neighbour. Fixing the leaf to the absorbing value of the first gate on a path to the output folds that gate and a reader. When an edge survives deletion at the neighbour, the neighbour remains essential and fixing it false saves a third gate. For a two-edge star one can delete a leaf. [A4](#a4) |

## Why folding alone misses the bonus

On the six-cycle in cyclic order, every vertex has degree two. Deleting the edges at any one vertex drops the minimum cover size from three to two, so the required saving is three gates. In the following expressions `+` denotes OR and multiplication denotes AND. [A1](#a1) · [A2](#a2) · [A3](#a3) · [A4](#a4)

- **Eight gates.** For `x1(x0+x2) + x3(x2+x4) + x5(x4+x0)`, setting `x0` false leaves six live gates. Regrouping the surviving edge terms as `x2(x1+x3) + x4(x3+x5)` takes five. For this fixed circuit, deletion at the odd-numbered centres already folds to five gates. A4's rotation observation concerns relabelling the circuit along with the chosen vertex. A3 gives the even-centred labelling and a five-gate residual after deleting at `x1`. [A1](#a1) · [A3](#a3) · [A4](#a4) · [Finite check](#finite-check)
- **Fifteen gates.** A2 labels the same graph by edges `Li–Rj` for `i ≠ j`. Write `Pij = Li + Lj` and `Qij = Ri + Rj`. The circuit conjoins five clauses, namely `P01 + P12`, `Q01 + Q12`, and `Pij + Qij` for each of the three pairs. For this single circuit *every* choice of vertex leaves thirteen live gates after folding. The bonus demands at most twelve. After deleting at `L0`, the circuit `L1(R0+R2) + L2(R0+R1)` uses five. The list of gates named `clauses15` below reconstructs A2's formula. [A2](#a2) · [Finite check](#finite-check)

Both examples admit the required residual. They pinpoint a failure of a proposed construction, even when the retained gates are all counted only in the output cone. [A1](#a1) · [A2](#a2) · [A3](#a3) · [Finite check](#finite-check)

## Finite evidence and its limits

A3 reports exact synthesis minima of **4** gates for the four-vertex path, **4** for the four-leaf star, and **8** for the six-cycle. A4 reports the following enumeration up to isomorphism for bipartite, four-cycle-free graphs with at least two edges, after discarding isolates. [A3](#a3) · [A4](#a4)

| Active vertices | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Classes checked by A4 | 1 | 3 | 4 | 11 | 18 | 47 | 96 |

A4 reports that all **180** classes attained the star-cover bound. The lower-budget checks used essential inputs, restriction to smaller solved graphs, and SAT on the minimal true edge inputs and maximal independent false inputs. At ten active vertices, **13 of 258** classes remained inconclusive. The supplied records contain no synthesis traces or SAT certificates for replay. A4 also identifies a limitation of the related bound it attributes to Jukna's 2014 Remark 10. An AO2 AND gate can have inputs depending on the same variable, and the cited multilinear argument supplies no general AO2 proof here. [A4](#a4)

The unrestricted inequality remains open in the supplied work, including the case of graphs of minimum degree at least three. There is consequently no theorem file here for another holder to check and no verified contributor PR to cite. [A1](#a1) · [A2](#a2) · [A3](#a3) · [A4](#a4)

## Source records

The four fenced JSON records below reproduce the named inputs byte for byte, including the final newline in each block. The SHA-256 values are the ones supplied with the assignment.

| Record | Input under `.imd/reads/artifacts/` | SHA-256 |
| --- | --- | --- |
| [A1](#a1) | `item-angle-1` | `0ffc4a7978a8043c342851e2be671567c71d31e2fc84492c3f73c1f6668022ba` |
| [A2](#a2) | `item-angle-2` | `329f3ecf89507ac20c22d5fbc9de0d933298b572ab1ad6245ef4d4bda72e86c2` |
| [A3](#a3) | `item-angle-3` | `3efda1694de5a468c7afccba3609fea1eb8fbd6e8db8845a288cf9ece583297c` |
| [A4](#a4) | `item-angle-4` | `dc049b74e6f18fae3e8704d87d06e9fd45caed415c73017f71757f92d278093e` |

<a id="a1"></a>

### A1 · item-angle-1

```json
{
  "status": "missing_lemma",
  "notes": "I could prove a restriction bound in terms of direct gate reads. Let r(z,C) count the gates of C whose input list contains z, counting each gate once. For every IsAO2 circuit C and every z, Lean checked the existence of an IsAO2 circuit D with D.size + r(z,C) ≤ C.size and circuitFun n D y = circuitFun n C (Function.update y z false) for every y. The construction scans the gates in order. It maps an old wire to either false or a wire in the new circuit. With one false operand an AND becomes false and an OR becomes its other operand. Only gates with two surviving operands need to be emitted. Every gate that directly reads z is omitted. An absent output wire represents false. Unfolding graphFun and applying SimpleGraph.deleteIncidenceSet_adj identifies the restricted function with the exact right-hand side posted by the desk.\n\nLean also checked that the extra-gate condition holds exactly when some minimum vertex cover of G contains z. Erasing z from such a cover witnesses the drop. Conversely, inserting z into a strictly smaller cover of the deleted graph gives a minimum cover of G containing z. Every positive-degree vertex must be read at least once, since adding it to the singleton consisting of a neighbor changes the output. This proves the full conclusion for a degree-one vertex omitted by all minimum covers. In particular either of two distinct leaves with the same neighbor works. A cover of the deleted graph omitting their neighbor must contain the other leaf, which can be exchanged for the neighbor at no extra cost.\n\nThere is a useful quantifier reduction. Pick a least-size AO2 circuit C₀ for G using Nat.find. One can then choose both z and D using C₀. Both inequalities transfer to every other C by C₀.size ≤ C.size. Lean checked this reduction against the posted statement, including the vacuous case of no computing circuit. I also proved that if a gate has input list [z,t] for distinct input vertices and deg(z) ≥ 2, then z must have a second reading gate under NoFourCycle. For an AND, hold t false and turn on a neighbor of z distinct from t. For an OR, hold t true and turn on a neighbor of z nonadjacent to t, which exists by the common-neighbor bound. Toggling z changes the graph function while leaving that gate fixed.\n\nThe six-cycle shows where the count falls short. Write i for input x_i, juxtaposition for AND and + for OR. The circuit 1(0+2) + 3(2+4) + 5(4+0) has eight gates and reads each input at most twice. Deleting vertex 0 lowers the minimum cover size from three to two, so the required residual size is at most five. Setting x₀ false and folding gives 1·2 + 3(2+4) + 5·4 with six live gates. Refactoring gives 2(1+3) + 4(3+5) with five. Lean checked bipartiteness, NoFourCycle, both minimum cover sizes, and the AO2 legality, size and function of each circuit. The example explains a failure of direct folding while satisfying the desired inequalities for this particular C.\n\nI could not prove that an arbitrary bipartite four-cycle-free graph admits a vertex giving the required degree saving, including the extra gate on a cover drop, for a least circuit. The general theorem remains unresolved by this attempt."
}
```

<a id="a2"></a>

### A2 · item-angle-2

```json
{
  "status": "missing_lemma",
  "notes": "The remaining lemma is the unrestricted AO2 size lower bound. In scratch Lean I proved that the exact posted statement is equivalent to this claim: for every two-colourable G with NoFourCycle G and every AO2 circuit C for graphFun G ∅, there is a vertex cover T of G with |E(G)| + |T| ≤ C.size + 1.\n\nFor the direction back to the posted statement, choose a positive-degree z whose deletion leaves an edge. Such a vertex exists when there are at least two edges. Put H = G.deleteIncidenceSet z. For any cover S of a nonempty-edge graph H I constructed an AO2 circuit D with D.size + 1 ≤ |E(H)| + |S|. Peel one cover vertex at a time, OR its current neighbours, AND with the vertex, and OR the resulting nonempty stars together. Take S minimum in H. Every G-cover T covers H, so |S| ≤ |T|, strictly if the posted extra-gate condition holds. Adding |E(H)| + degree(z) = |E(G)| gives both requested inequalities. Conversely, induction on edge count gives the lower bound from the posted statement. If the cover size drops, insert z into the residual cover and use the extra gate. Otherwise a minimum G-cover is already no larger than the residual cover. Lean also checked that a witness found using one least-size C works for every larger C, with the same z and D.\n\nFor a direct restriction proof, I checked that fixing z false computes the stated residual function and saves at least the number of distinct gate positions reading z. A renumbering map sends old wires to either false or a valid new wire. An OR with a false operand forwards its other operand, and an AND with a false operand maps to false. Every positive-degree vertex is read. The extra-gate condition is equivalent to z belonging to some minimum G-cover. This settles a degree-one vertex in no minimum cover, including either of two leaves with the same neighbour. I also checked the full two-gate saving for an isolated edge zw when another edge survives: first set z true, so w is a singleton term, then set w false. Each restriction saves a gate.\n\nA checked six-cycle example shows why constant folding on an arbitrary C misses the required count. Use left inputs L0,L1,L2 and right inputs R0,R1,R2, with edges Li–Rj for i ≠ j. Form Pij = Li OR Lj and Qij = Ri OR Rj for i < j. AND together the five clauses (P01 OR P12), (Q01 OR Q12), and (Pij OR Qij) for the three pairs. This 15-gate circuit computes the edge function. Every vertex has degree two and belongs to a minimum cover of size three. Pinning any vertex false and folding the constant operands leaves 13 gates, all in the output cone, while the required saving is three. For z = L0 a different residual circuit uses just five gates: (L1 AND (R0 OR R2)) OR (L2 AND (R0 OR R1)). The example rules out this folding strategy as a uniform construction on arbitrary circuits. I found no counterexample to the posted theorem.\n\nThe equivalence, special cases and six-cycle checks elaborated with the pinned toolchain. The general size lower bound, or an argument obtaining both savings directly in a least circuit, remains unproved."
}
```

<a id="a3"></a>

### A3 · item-angle-3

```json
{
  "status": "missing_lemma",
  "notes": "The remaining lemma says that every AO2 circuit for a nonempty bipartite graph with no four-cycle needs at least e(G) + τ(G) − 1 gates to compute its edge function. Here nonempty means G has an edge, e counts edges, and τ is the minimum vertex-cover size. I proved in scratch Lean that this lemma is equivalent to the exact posted statement.\n\nFor the direction back to the posted step, take two distinct edges and choose an endpoint z of one outside the other. H = G.deleteIncidenceSet z still has an edge, and e(H) = e(G) − degree(z). To build D from a minimum cover of H, remove each centre's remaining incident edges in turn. Use k−1 ORs and one AND for a nonempty k-edge star, then OR the star outputs. This gives size(D) + 1 ≤ e(H) + τ(H). We have τ(H) ≤ τ(G) ≤ τ(H) + 1. The bonus antecedent is equivalent both to τ(H) < τ(G) and to z belonging to some minimum cover of G. The lower bound on C now gives both inequalities. In the forward direction, induct on e(G), apply the posted step to C and use the induction bound for D. If H is empty, {z} covers G and degree(z) = e(G). For one edge, the function needs a gate. These reductions and the star construction elaborated using only propext, Classical.choice and Quot.sound.\n\nI also checked a direct restriction lemma. On the face x_z = false, scan the original gates in order. Omit a gate whose restricted value is identically false or equals an earlier restricted wire on every input. Maintain either a false marker or a valid replacement wire for every old wire. Each retained gate can read two replacement wires, preserving AO2. Every gate reading z directly can be omitted. Every positive-degree input has at least one reader, since turning it on beside a single neighbour changes the output and a primary output cannot compute the edge function. This proves the posted conclusion for any graph with a degree-one vertex in no minimum cover.\n\nThere is a degree-sized count in a restricted case. Suppose every direct reader of z is an OR with another primary input of z's colour, or an AND with a primary input of the opposite colour. For each neighbour v start with v and all vertices of z's colour nonadjacent to v turned on. This is independent. Turn on z and take the first gate whose output changes. It reads z. At an OR its other primary must be adjacent to v. At an AND its other primary must equal v. NoFourCycle means z and a fixed same-colour partner have at most one common neighbour. Thus different neighbours charge distinct removable gates. Lean checked this argument. General AO2 permits internal wires as partners, and the argument does not establish the cover bonus. Choosing z for one least circuit suffices because the same D works for every larger C.\n\nExact synthesis gave minimum sizes 4 for the four-vertex path, 4 for the four-leaf star and 8 for the six-cycle. For the six-cycle in cyclic order, write + for OR and juxtaposition for AND. The eight-gate circuit x0(x1+x5)+x2(x1+x3)+x4(x3+x5) loses only two gates by folding constants at x1=false. The cover number drops from 3 to 2, so three savings are required. Rebuilding as x3(x2+x4)+x5(x0+x4) takes five gates. Lean checked these circuits and the strict cover comparison. The rebuilt circuit satisfies both inequalities where constant folding alone falls short. I found neither a general lower-bound proof nor a graph violating it."
}
```

<a id="a4"></a>

### A4 · item-angle-4

```json
{
  "status": "missing_lemma",
  "notes": "I did not prove L-meta-3566 or find a counterexample. Let m(G) count edges, τ(G) be the minimum cover size, and H be G with the edges at z deleted.\n\nIn scratch Lean I proved that the posted statement is equivalent to m(G)+τ(G) ≤ C.size+1 for every AO2 circuit computing the edge function of a bipartite C4-free G. Forward, induct on m. Deleting z removes exactly degree(z) edges, and τ(H) ≤ τ(G) ≤ τ(H)+1 since a cover of H extends by inserting z. The bonus pays for precisely the strict case. Conversely, choose an endpoint of one edge outside a second edge, so H still has an edge. Assign each residual edge to one endpoint in a minimum cover of H. For a center with d assigned edges, OR its neighbors in d−1 gates and AND with the center in one. OR the stars together. This D costs at most m(H)+τ(H)−1, giving both inequalities from the bound on C. I also checked in Lean that it suffices to choose z and D for one least circuit of G. The same D works for every larger C.\n\nI proved the deletion conclusion in Lean under the extra condition m(G) < the number of nonisolated vertices. This covers all forests in the brief. By the degree sum there are more leaves than vertices of degree at least three. If two leaves share a neighbor, deleting one preserves τ, and setting its input to false saves at least one gate. Otherwise some leaf u has a neighbor v of degree at most two. If v has degree two, write w for its other neighbor. When H=G−inc(v) has an edge, both u-cofactors are nonconstant. Follow a path from input u to the output and fix u to the absorbing value of its first gate (false for AND, true for OR). That gate is internal and its next reader also folds. In either cofactor v remains essential, as seen by setting w alone true and toggling v. Setting v false saves a third gate and computes H, since u sees only v. An isolated edge component needs only two savings by the same first restriction and then setting its other end false. If deleting v empties a two-edge star, choose a leaf instead.\n\nFor the six-cycle labeled cyclically 0 through 5, use the eight-gate circuit centered at 1,3,5. Setting 0 false folds two gates. The cover drops from three to two, so three savings are required. The folded six-gate expression can be refactored to (x2 AND (x1 OR x3)) OR (x4 AND (x3 OR x5)), costing five. Lean checked the circuits and the cover bonus. Rotation gives the same obstruction to folding alone for any proposed z.\n\nIndependently, I enumerated bipartite C4-free graphs up to isomorphism, omitting isolates. With 3 through 9 active vertices and at least two edges the class counts were 1, 3, 4, 11, 18, 47, 96. All 180 met the exact star-cover bound. I checked lower budgets by essential-input counts, restrictions to smaller solved graphs, and SAT over binary AND/OR gates on edge inputs and maximal independent inputs. Monotonicity extends these boundary values to all inputs. These finite searches were computational checks. At ten active vertices, 13 of 258 classes still had an inconclusive size check.\n\nThe missing inequality is the unrestricted AO2 lower bound above for the remaining graphs, including graphs of minimum degree at least three. Jukna's 2014 Remark 10 gives a related edge-count bound for tropical and multilinear Boolean circuits. AO2 allows the two inputs of an AND gate to depend on the same variable."
}
```

<a id="finite-check"></a>

## Replaying the six-cycle checks

The Python code uses inputs 0 through 5 and numbers each gate after its predecessors. It tests every one of the 64 input masks against the edge function, enumerates vertex covers, and counts gates reachable from the folded output. The class total at the end checks A4's arithmetic only. [A1](#a1) · [A2](#a2) · [A3](#a3) · [A4](#a4)

```python
vertices = range(6)
masks = range(1 << 6)
cycle = [(v, (v + 1) % 6) for v in vertices]
off_diagonal = [(i, 3 + j) for i in range(3) for j in range(3) if i != j]

cyclic8 = [
    ("or", 0, 2), ("and", 1, 6),
    ("or", 2, 4), ("and", 3, 8),
    ("or", 4, 0), ("and", 5, 10),
    ("or", 7, 9), ("or", 12, 11),
]
cyclic5 = [
    ("or", 1, 3), ("and", 2, 6),
    ("or", 3, 5), ("and", 4, 8), ("or", 7, 9),
]
rotated8 = [
    ("or", 1, 5), ("and", 0, 6),
    ("or", 1, 3), ("and", 2, 8),
    ("or", 3, 5), ("and", 4, 10),
    ("or", 7, 9), ("or", 12, 11),
]
rotated5 = [
    ("or", 2, 4), ("and", 3, 6),
    ("or", 0, 4), ("and", 5, 8), ("or", 7, 9),
]

# Inputs 0,1,2 are L0,L1,L2. Inputs 3,4,5 are R0,R1,R2.
clauses15 = [
    ("or", 0, 1),       #  6  P01
    ("or", 0, 2),       #  7  P02
    ("or", 1, 2),       #  8  P12
    ("or", 3, 4),       #  9  Q01
    ("or", 3, 5),       # 10  Q02
    ("or", 4, 5),       # 11  Q12
    ("or", 6, 8),       # 12  some L
    ("or", 9, 11),      # 13  some R
    ("or", 6, 9),       # 14  P01 + Q01
    ("or", 7, 10),      # 15  P02 + Q02
    ("or", 8, 11),      # 16  P12 + Q12
    ("and", 12, 13),    # 17
    ("and", 17, 14),    # 18
    ("and", 18, 15),    # 19
    ("and", 19, 16),    # 20  output
]
clauses5 = [
    ("or", 3, 5), ("and", 1, 6),
    ("or", 3, 4), ("and", 2, 8), ("or", 7, 9),
]


def evaluate(gates, output, mask):
    values = [bool(mask & (1 << v)) for v in vertices]
    for op, a, b in gates:
        assert op in ("and", "or") and 0 <= min(a, b) <= max(a, b) < len(values)
        x, y = values[a], values[b]
        values.append((x and y) if op == "and" else (x or y))
    return False if output is None else values[output]


def check_function(gates, output, edges):
    for mask in masks:
        expected = any((mask & (1 << a)) and (mask & (1 << b)) for a, b in edges)
        assert evaluate(gates, output, mask) == expected


def cover_size(edges):
    return min(mask.bit_count() for mask in masks
               if all(mask & ((1 << a) | (1 << b)) for a, b in edges))


def fold(gates, vertex):
    replacement = list(vertices)
    replacement[vertex] = None   # constant false
    kept = []
    for op, a, b in gates:
        x, y = replacement[a], replacement[b]
        if x is None or y is None:
            other = y if x is None else x
            replacement.append(None if op == "and" else other)
        else:
            replacement.append(6 + len(kept))
            kept.append((op, x, y))
    return kept, replacement[-1]


def live_count(gates, output):
    pending = [output]
    live = set()
    while pending:
        wire = pending.pop()
        if wire is None or wire < 6 or wire in live:
            continue
        live.add(wire)
        _, a, b = gates[wire - 6]
        pending.extend((a, b))
    return len(live)


def test_deletions(gates, edges):
    output = 6 + len(gates) - 1
    check_function(gates, output, edges)
    assert live_count(gates, output) == len(gates)
    assert cover_size(edges) == 3
    counts = []
    for z in vertices:
        residual_edges = [e for e in edges if z not in e]
        assert len(edges) - len(residual_edges) == 2
        assert cover_size(residual_edges) == 2
        kept, output = fold(gates, z)
        check_function(kept, output, residual_edges)
        counts.append(live_count(kept, output))
    return counts


for name, gates, edges, expected in [
    ("cyclic8", cyclic8, cycle, [6, 5, 6, 5, 6, 5]),
    ("rotated8", rotated8, cycle, [5, 6, 5, 6, 5, 6]),
    ("clauses15", clauses15, off_diagonal, [13] * 6),
]:
    counts = test_deletions(gates, edges)
    assert counts == expected
    print(name, "fold counts", counts)

for name, gates, edges, z in [
    ("cyclic5", cyclic5, cycle, 0),
    ("rotated5", rotated5, cycle, 1),
    ("clauses5", clauses5, off_diagonal, 0),
]:
    output = 6 + len(gates) - 1
    check_function(gates, output, [e for e in edges if z not in e])
    assert live_count(gates, output) == len(gates) == 5
    print(name, "residual gates", len(gates))

classes = [1, 3, 4, 11, 18, 47, 96]
assert sum(classes) == 180
print("A4 class total", sum(classes))
```

Expected output for the finite checks follows.

```text
cyclic8 fold counts [6, 5, 6, 5, 6, 5]
rotated8 fold counts [5, 6, 5, 6, 5, 6]
clauses15 fold counts [13, 13, 13, 13, 13, 13]
cyclic5 residual gates 5
rotated5 residual gates 5
clauses5 residual gates 5
A4 class total 180
```

From a directory containing just this report as `report.md`, the following command checks the input digests and citations, runs the finite checks, and compares the output with the transcript above. It requires Python 3.10 or later and uses the standard library.

```sh
python3 - <<'PY'
from contextlib import redirect_stdout
from hashlib import sha256
from io import StringIO
import json
from pathlib import Path
import re

report = Path("report.md").read_text(encoding="utf-8")
blocks = re.findall(r"^```json\n(.*?)^```$", report, re.M | re.S)
digests = re.findall(r"^\| \[A\d\].*?`([0-9a-f]{64})` \|$", report, re.M)
assert len(blocks) == len(digests) == 4
for block, digest in zip(blocks, digests):
    assert sha256(block.encode("utf-8")).hexdigest() == digest
    assert json.loads(block)["status"] == "missing_lemma"
anchors = set(re.findall(r'^<a id="([\w-]+)"></a>$', report, re.M))
links = set(re.findall(r"\]\(#([\w-]+)\)", report))
assert links <= anchors
program, = re.findall(r"^```python\n(.*?)^```$", report, re.M | re.S)
expected = re.findall(r"^```text\n(.*?)^```$", report, re.M | re.S)[-1]
out = StringIO()
with redirect_stdout(out):
    exec(compile(program, "six-cycle checks", "exec"), {})
assert out.getvalue() == expected
print(out.getvalue(), end="")
PY
```
