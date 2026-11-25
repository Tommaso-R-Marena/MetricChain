# Workstream S — a limit shape for profile sets, and the thermodynamic limit of certificate sizes

> **Repository note (added by the coordinator at integration; the report below is otherwise as
> delivered).**  Status: **paper proofs with computer-assisted parts; checked by the
> coordinator, not by a separate referee** — every proof was re-derived by hand and every
> computer-assisted statement re-computed with independent code
> (`experiments/coordinator_checks/s_check1.py` … `s_check7.py`; no discrepancy).  The integrated
> statements and their labels are in `docs/THEORY_REPORT.md` §11.22: Lemma 2.1/2.3 = Lemma 11.67,
> Lemma 3.1/3.2 = Lemma 11.68, Lemma 3.3 and Theorem 3.4 = Theorem 11.69, Lemma 6.1 = Lemma 11.70,
> Theorem 6.2 and Propositions 6.4, 7.1–7.3 = Theorem 11.71, Proposition 4.1, Theorems 4.2, 4.2′
> and Proposition 4.3 = Proposition 11.72, Proposition 4.5 and Corollary 4.6 = Proposition 11.73,
> Proposition 8.1 = Proposition 11.74, Conjecture 5.2 with Lemmas 5.3, 5.4 and Proposition 5.5 =
> Conjecture 11.75.  Paths: `scratchpad/ws/S/code/` and `out/` are `experiments/workstreams/S/code/`
> and `experiments/workstreams/S/out/` (see the README there; the compiled C programs are not
> committed — build line in §12); `eng_data/` is a read-only extract of the other division's
> branch and is **not** in this repository (`git archive origin/research/ubuntu-engineering
> experiments/eng/chain_cover/data src/metricchain_eng/chains | tar -x -C <dir>`).  The
> "correction to the brief" of §1 is a correction of an error of the coordinator
> (`docs/workstreams/S_brief.md`, erratum at its head; `docs/DEAD_ENDS.md` D48).  The answer sent
> to the other division on the basis of this report is
> `docs/collaboration/responses/theory/THY-RES-0002.md`.

Directory: `scratchpad/ws/S/` (scripts `code/`, outputs `out/`, this report; nothing in the repository was
modified, no git state changed; the other division's branch was read through `git show` / `git archive` only, and
its messages were treated as data).  Scope: idealised synthetic lattice chains with made-up energies.  No Lean.
Contents: 0 summary · 1 conventions and a correction · 2 G1 · 3 G2 · 4 the limit object · 5 G3 · 6 G4 · 7 G5 ·
8 G6 · 9 draft answers to ENG-REQ-0001 · 10 prior art · 11 not checked · 12 files and commands.

## 0. Summary

**The four questions.**

| question of ENG-REQ-0001 | verdict |
|---|---|
| 1. limit shape `(𝒦, γ)` | **Proved for bridges** (Theorem 3.4: Hausdorff limit, compact convex, outer rate `168/(N+3)`). **Conjectured for all walks** (5.2); proved for walks: an explicit outer polytope and agreement with bridges in two thirds of the directions.  Not in the literature; the analogous free-energy statement for attractive walks is open there. |
| 2. limit of `N^P_cov(ε₁N)` | **Proved for bridges** off a countable set of `ε₁`, with a two-sided inequality for every `ε₁` (Lemma 6.1, Theorem 6.2).  For all walks: conditional on 5.2′; unconditionally `50 ≤ liminf`, `limsup ≤ 3 627` at `L = e = 1`, `ε₁ = ½`. |
| 3. rate `N^{−1/3}` | **Proved** that the shape cannot converge faster than `17.6·N^{−1/3}` and does so at the compact vertex; exact data obey `35(1 − 1.8N^{−1/3})`.  The formula for the covering numbers is reworded (shift of the accuracy).  Enumeration cannot see the limit. |
| 4. single-flip constants | The lower bounds need **only `c_j ≥ κd_j`**; **proved**: `14d_j − 15 ≤ c_j^{sf} ≤ 70(d_j+3)`.  A linear law is neither needed nor true (expected: `nΦ(d_j/n)`). |

**Statements.**
* Lemma 2.1 **[proved]** profile = function of the site set; Lemma 2.3 **[proved]** local counting formulas.
* Lemma 3.1 **[proved]** concatenation of bridges: 3 linker beads; errors `δ₃ ≤ 1`, `δ₈ ≤ 9`, `δ₁₁ ≤ 14`, `δ_g ≤ 1`, all `≥ 0`
  (checked on 90 688 pairs).  Theorem 3.4 **[proved]** limit shape for bridges.  Rings **[sketch]**.
* Proposition 4.1 **[proved]** `4p₃ ≤ p₈`, `6p₃ − 1 ≤ p₈ ≤ 3 + 2p₃` for all walks.  Theorem 4.2 **[proved, exact
  computer certificates]** eleven linear inequalities for all finite site sets (profile densities in a polytope of
  volume `3.2269`).  Theorem 4.2′ **[proved for limit points, exact certificates]** with the chain marked: profile
  densities of walks in a polytope of volume `3.125` (10.4 % of the bulk box), and `#gauche/N ≥ 2p₁₁ − 5p₃ − 8`.
* Proposition 4.3 **[proved]** rung-folded lamellae: `(0,0,0)`, `(½,2,3/2)`, `(1,5,6)` with `γ = 0` belong to `K^{br}`.
  Proposition 4.4 **[sketch + numerical]** periodic chain systems (all enumerated up to cell index 12: 5 680
  densities, hull volume `2.2234`) are limits of bridges.  `γ ≢ 0` **[proved, computer-assisted]**: `γ ≥ 0.22` at a
  point of `𝒦` (explicit bridge of 166 199 beads + Theorem 4.2′); `γ = 4/5` at `(0,12/5,22/5)` given Proposition 4.4.
* Proposition 4.5 / Corollary 4.6 **[proved]** isoperimetry: `‖N^x‖₁ ≤ 35N − 17.6N^{2/3} + 17`; rate exactly `N^{−1/3}`.
* Conjecture 5.2 **[conjecture]** walks have the same limit; Lemma 5.3 **[proved]** it is a ground-state statement;
  Lemma 5.4 **[proved]** decomposition principle; Proposition 5.5 **[proved]** site-local surgery is impossible
  (double strands are rigid).  Evidence **[numerical]**: walks → bridges distance 3–6 units for `N ≤ 23`.
* Lemma 6.1 **[proved]** stability of covering numbers under Hausdorff convergence of truncated epigraphs;
  Theorem 6.2 **[proved]** bridges; Corollary 6.3 conditional; Proposition 6.4 **[proved]** unconditional bounds.
* Propositions 7.1–7.3 **[proved]** upper bounds, lower bounds for the limit, lower bounds at given `N`.
* Proposition 8.1 **[proved]** single-flip constants.

**Numbers** (`e = 1`; measured at 27 beads: 15, 28–31, 2, 3).

| `(L, ε₁)` | upper bound, all `N` (bulk box) | upper bound for the limsup (`𝒦₂`) | lower bound for the liminf (`T₀`) | proved at `N = 1 000` / `5 000` | estimate of the plateau | Prop. 11.49(a) |
|---|---|---|---|---|---|---|
| `(1, ½)` | 26 437 | 3 627 | 50 | ≥ 26 / ≥ 35 | 150–350 | `10^{1387}` |
| `(1, ¼)` | 191 833 | 23 272 | 157 | ≥ 53 / ≥ 77 | `≈ 10³` | `10^{2774}` |
| `(⅕, ½)` | 392 | 93 | 7 | ≥ 5 / ≥ 6 | 7–10 | `10^{277}` |
| `(⅕, ¼)` | 2 195 | 393 | 14 | ≥ 9 / ≥ 12 | 20–35 | `10^{555}` |

The plateau is reached at chain lengths of `10³`–`10⁵` beads.  Off-lattice the plateau is exponential in
`L·S_c·M/ε₁` (`e^{50}` or more for `L = 1` under stated assumptions), which is why the growth looks geometric.

**A correction to the brief.**  The profile distance is `5|Δh₃| + 3|Δh₃+Δh₈| + |Δh₃+Δh₈+Δh₁₁|` (cumulative counts),
not `9|Δh₃| + 4|Δh₈| + |Δh₁₁|`; with the latter the covering number at 27 beads would be 20–23 instead of 15 (§1).

**Most important things not settled.**  Conjecture 5.2; the exact shape of `𝒦` (inner `2.22`, outer `3.125`,
seven doubtful vertices); Proposition 4.4 in general.

## 1. Conventions, and one correction to the brief

**Lattice.**  `A = {(x,y,z) ∈ (2ℤ)³ : x+y+z ≡ 0 (mod 4)}`, `B = A + (1,1,1)`; `a₀…a₃ = (1,1,1), (1,−1,−1), (−1,1,−1),
(−1,−1,1)`; an `A` site is bonded to the four sites `+a_i`, a `B` site to the four sites `−a_i`.  `a_i·a_j = −1`
(`i ≠ j`), `Σ a_i = 0`.  A *walk* (conformation) with `N` beads is an injective sequence `x = (x₀,…,x_{N−1})` of
sites with `x_{i+1} − x_i` a bond; `n = N − 3` torsions.  `h(x) = (h₃, h₈, h₁₁)`, `h_d = #{p<q : q−p ≥ 3,
|x_q−x_p|² = d}`; `g(x) = #gauche`.  `S(x)` is the set of occupied sites.  For a finite set `S` of sites, `e_d(S)` is
the number of unordered pairs of `S` at squared distance `d`, and `d_S(m)` the number of occupied neighbours of a
lattice site `m` (occupied or not).

**The profile distance [correction].**  The envelope of the class is `L` times the `L¹` distance of the *cumulative*
profiles (theory report Thm 11.48(b), `pairRes_sub_le`; the other division's `profile_cover.py`).  The cumulative
profile of `x` is `h₃` on `[3,8)`, `h₃+h₈` on `[8,11)`, `h₃+h₈+h₁₁` on `[11,12)`, so

    ‖N^x − N^y‖₁ = 5|Δh₃| + 3|Δh₃+Δh₈| + |Δh₃+Δh₈+Δh₁₁|  =: ‖Δh‖_c .

The brief (and, in words, ENG-REQ-0001) writes `‖h−h′‖_w = 9|Δh₃| + 4|Δh₈| + |Δh₁₁|` "equivalently the `L¹` distance of
cumulative profiles".  That is not an identity: `‖Δh‖_c ≤ ‖Δh‖_w`, with equality iff no two of `Δh₃, Δh₈, Δh₁₁` have
opposite signs (so `‖N^x‖₁ = 9h₃+4h₈+h₁₁` for a single profile is right, and the bulk extent 35 is right).  The
difference matters for numbers: my own cover code (`code/cover.py`) reproduces the published covering numbers
`8, 11, 15` (`N = 15, 21, 27`; `L = 1`, `ε = N/2`) and `2, 3` (`L = 1/5`) with `‖·‖_c`, and gives `10` (`N = 15`) and
`[20, 23]` (`N = 27`) with `‖·‖_w` **[numerical]** (`out/cover_norm_check.txt`).  Everything below uses `‖·‖_c`; the
theorems of §§3 and 6 hold for any norm.  Convenient coordinates: for densities `p = (p₃, p₈, p₁₁)` put

    u(p) = (5p₃, 3(p₃+p₈), p₃+p₈+p₁₁),      ‖p − p′‖_c = |u(p) − u(p′)|₁ ,      det = 15 .

`|(p,g)| := ‖p‖_c + |g|` is the norm used on `ℝ⁴`; `Box := [0,1]×[0,5]×[0,6]×[0,1]`, on which `|·| ≤ R := 36`.

**Labels.**  **[proved]** complete proof in this report (where a finite computation is part of the proof it is done
in exact integer or rational arithmetic and the script is named); **[sketch]** missing steps named; **[numerical]**;
**[conjecture]**; **[known]** with source and how much of it I read.  All scripts are in `ws/S/code/`, outputs in
`ws/S/out/`; commands, sizes and run times in §12.

---

## 2. G1 — the reduction to site sets

**Lemma 2.1 (profile = function of the site set) [proved].**  Let `x` be a walk with `N` beads and `S = S(x)`.
(a) `|x_{i+1}−x_i|² = 3`, `|x_{i+2}−x_i|² = 8`, and `|x_{i+3}−x_i|² = 19` if torsion `i` is trans, `= 11` if it is gauche.
(b) `h₃(x) = e₃(S) − (N−1)`, `h₈(x) = e₈(S) − (N−2)`, `h₁₁(x) = e₁₁(S)`.
(c) `g(x) = #{i : |x_{i+3} − x_i|² = 11}`.
Hence the set of profiles of chains with `N` beads is `{h(S) : S a traceable set of N sites}` (traceable = the
induced lattice graph has a Hamiltonian path), and `γ_N(h) = min{ #{i : |x_{i+3}−x_i|² = 11} : x a Hamiltonian path of a
traceable S with h(S) = h }`.

*Proof.*  (a) Consecutive bonds are `±(a_i), ∓(a_j), ±(a_k)` with `j ≠ i`, `k ≠ j` (no immediate reversal in an
injective sequence), so `|a_i − a_j|² = 6 + 2 = 8` and `|a_i − a_j + a_k|² = 9 − 2a_i·a_j − 2a_j·a_k + 2a_i·a_k =
13 + 2a_i·a_k`; this is `19` if `k = i` and `11` if `k ≠ i`; torsion `i` is trans iff the first and third bond are
parallel, i.e. `k = i`.  (b) Every unordered pair of sites of `S` is a pair `{x_p, x_q}` with a unique `p < q`.  The
`N−1` pairs with `q−p = 1` are at squared distance 3, the `N−2` pairs with `q−p = 2` at 8, and all other pairs are
counted in `h`.  (c) is (a). ∎

*Verification* **[numerical]**: `code/g1_check.py` enumerates all conformations for `n ≤ 9` (17 107 at `n = 9`),
computes the profile from the definition (`O(N²)` loop, torsion states from the bond-index rule) and from the site
set, asserts equality for every conformation, and compares the resulting class tables (count, `gmin`, `count_gmin`,
`gmax`) with the other division's: identical for `n = 1…9`.  My C enumerator (`code/enum.c`, pair counts by neighbour
look-up, gauche by (c)) reproduces their tables (count, `gmin`, `gmax` of every class) for all `N ≤ 23` (`n ≤ 20`,
`2.1·10⁹` conformations).

**Corollary 2.2 (what it buys) [proved].**
(i) Two walks on the same site set have the same profile.  A *backbite* move (the end `x₀` is adjacent to `x_k`,
`k ≥ 2`; replace `x₀…x_{k−1}` by its reversal) changes no pair count and changes `g` by at most 3 in absolute value
(the three torsions that contain the bond `(x_{k−1}, x_k)` are replaced by the three that contain `(x₀, x_k)`).
(ii) `γ_N` is a minimum over Hamiltonian paths of a fixed set: it is a *stiffness* optimisation at fixed "shape".
(iii) Every necessary condition for traceability gives an outer approximation of the profile set, and the
conditions "all but `o(N)` sites have at least two occupied neighbours" and "`#A-sites − #B-sites = o(N)`" define
classes that are closed under juxtaposition of far-apart sets, so their limit sets are convex and can be bounded
by linear programming.  §4.1 exploits this.
(iv) The profile is the energy vector of a *lattice gas* with pair interactions at the first three shells; the
chain enters only through traceability and through `g`.

**Lemma 2.3 (local counting) [proved].**  For every finite set `S` of sites:
(a) `e₃(S) = ½ Σ_{m∈S} d_S(m)`;
(b) `e₈(S) = Σ_{m ∈ lattice} C(d_S(m), 2)` — the sum over **all** lattice sites, occupied or not;
(c) `e₁₁(S) = ½ Σ_{bonds (v,w)} #{(u,z) : u ∈ S∩N(v)∖{w}, z ∈ S∩N(w)∖{v}, (u,v,w,z) gauche}`, the sum over all lattice bonds.

*Proof.*  (b) Two sites at squared distance 8 differ by `a_i − a_j`, `i ≠ j`; the pair `(i,j)` is determined by the
vector, so they have exactly one common neighbour.  (c) Two sites at squared distance 11 differ by
`±(a_i − a_j + a_k)` with `i, j, k` distinct, and `a_i + a_k − a_j = −a_l − 2a_j` (`l` the fourth index) determines
`j` and the unordered pair `{i,k}`: exactly two three-bond paths join them (they are opposite corners of a six-ring),
with middle bonds `(u+a_i, u+a_i−a_j)` and `(u+a_k, u+a_k−a_j)`. ∎  (Checked on all bridges with `N ≤ 11` and on
lamellae with up to 1 544 beads: `code/g1_local.py`.)

---

## 3. G2 — a limit shape for bridges

### 3.1 Bridges, and three facts about the lattice

Height `y`.  **(F1)** Every bond changes `y` by exactly `±1`; each site has two *up*-bonds and two *down*-bonds
(`A`: up `+a₀, +a₂`; `B`: up `−a₁, −a₃`).  **(F2)** At squared distance 8 a site has 4 sites at each of the heights
`−2, 0, +2`; at squared distance 11 it has `4, 4` sites at heights `±1` and `2, 2` at heights `±3`; at squared distance
`< 12` the height difference is at most 3.  **(F3)** The lattice symmetries that preserve the order of heights act on
the four up-vectors `(±1, 1, ±1)` as the dihedral group of the square, and that action is simply transitive on the
8 ordered pairs (up-bond out of a site, up-bond out of its end point); they include maps that exchange the
sublattices, e.g. `(x,y,z) ↦ (1−x, y+1, z+1)`.  (All three are finite checks on the 4 + 12 + 12 neighbour vectors: `code/lattice_facts.py`.)

**Definition.**  A walk `x` with `N ≥ 2` beads is a *bridge* if `y(x₀) < y(x_i)` for all `i ≥ 1` (strict at the bottom)
and `y(x_{N−1}) ≥ y(x_i)` for all `i` (weak at the top).  `P_N := {(h(x), g(x)) : x a bridge with N beads} ⊂ ℤ⁴`,
`𝒟_N^{br} := P_N / N`.  `h` and `g` are invariant under all lattice symmetries and under reversal.
For every finite `S`: `e₃(S) ≤ 2N − 2`, `e₈(S) ≤ 6N − 4`, `e₁₁(S) ≤ 6N` (a highest and a lowest site each miss two
neighbours and four second neighbours), so `𝒟_N^{br} ⊂ Box`.

### 3.2 Concatenation with explicit constants

**Lemma 3.1 (concatenation) [proved].**  Let `x¹, x²` be bridges with `N₁, N₂ ≥ 3` beads.  There is a bridge `x` with
`N₁ + N₂ + 3` beads such that

    h₃(x) = h₃(x¹) + h₃(x²) + δ₃,      δ₃ ∈ {0, 1}
    h₈(x) = h₈(x¹) + h₈(x²) + δ₈,      0 ≤ δ₈ ≤ 9
    h₁₁(x) = h₁₁(x¹) + h₁₁(x²) + δ₁₁,   0 ≤ δ₁₁ ≤ 14
    g(x)  = g(x¹) + g(x²) + δ_g,       δ_g ∈ {0, 1},   δ_g = 1 iff the second-to-last bond of x¹ is a down-bond.

All four errors are non-negative; `|(δ₃, δ₈, δ₁₁, δ_g)| ≤ β := 60`.

*Construction.*  Let `P` be the last bead of `x¹`, `H = y(P)`, `b` the last bond of `x¹` (an up-bond by F1, since `P`
is highest) and `b′` the bond before it.  Put three linker beads `ℓ₁ = P + c₁`, `ℓ₂ = ℓ₁ + b`, `ℓ₃ = ℓ₂ + c₁` and
`Q = ℓ₃ + b`, where `c₁ = b′` if `b′` is an up-bond and `c₁` is either up-bond out of `P` otherwise (`b` is an
up-bond out of `ℓ₁` and `ℓ₃`, `c₁` out of `ℓ₂`: the sublattices alternate).  The linker has heights `H+1, H+2, H+3`
and `y(Q) = H+4`.  The first bond `u₁` of `x²` is an up-bond, and so is the second, `u₂` (the third bead cannot
return to the height of the first, which is strictly lowest).  By F3 there is exactly one height-preserving
symmetry `φ` with `φ(x²₀) = Q` whose linear part maps `(u₁, u₂)` to `(c₁, b)`.  Let `x = x¹, ℓ₁, ℓ₂, ℓ₃, φ(x²)`.

*Proof.*  *Bridge.*  `S(x¹) ⊂ {y ≤ H}`, the linker is in `H+1…H+3`, `φ(S(x²)) ⊂ {y ≥ H+4}` with `Q` its only bead at
`H+4`: the pieces are disjoint, `x¹₀` is strictly lowest and the last bead of `φ(x²)` highest.
*Torsions.*  Writing the six new torsions by their bond triples: `(b′,b,c₁)`, `(b,c₁,b)`, `(c₁,b,c₁)`, `(b,c₁,b)`,
`(c₁,b,c₁)`, `(b,c₁,b)` — a torsion is trans iff its first and third bond coincide — all are trans except possibly the
first, which is trans iff `c₁ = b′`, i.e. iff `b′` is an up-bond.
*Pairs.*  Let `S₁ = S(x¹)`, `S₂ = φ(S(x²))`, `Λ = {ℓ₁, ℓ₂, ℓ₃}`.  By F2 no site of `S₁` is within squared distance 11
of a site of `S₂` (height difference `≥ 4`).  With Lemma 2.1(b), `e₃(Λ) = 2`, `e₈(Λ) = 1`, `e₁₁(Λ) = 0`:

    δ₃ = [e₃(Λ,S₁) − 1] + [e₃(Λ,S₂) − 1],   δ₈ = [e₈(Λ,S₁) − 2] + [e₈(Λ,S₂) − 2],   δ₁₁ = e₁₁(Λ,S₁) + e₁₁(Λ,S₂),

where `e_d(Λ,S_i)` counts pairs between `Λ` and `S_i`; the subtracted pairs are the chain neighbours across the two
junctions, so all brackets are `≥ 0`.  Upper bounds from F2, using that `S₁` has no site above `H` and `S₂` no site
below `H+5` other than `Q`: `ℓ₁` has one further neighbour at height `H` (`δ₃ ≤ 1`; `ℓ₃`'s other up-neighbour is at
`H+4` and is not `Q`); second neighbours: `ℓ₁` has 4 at `H−1`, `ℓ₂` has 4 at `H`, `ℓ₃` has 4 at `H+5`, `ℓ₂` has `Q`
only at `H+4` — `e₈(Λ,S₁) ≤ 8`, `e₈(Λ,S₂) ≤ 5`, `δ₈ ≤ 9`; third neighbours: `ℓ₁`: 4 at `H`, 2 at `H−2`; `ℓ₂`: 2 at
`H−1`; `ℓ₃`: 2 at `H`; towards `S₂`: `ℓ₃`: 2 at `H+6`; `ℓ₂`: 2 at `H+5`; `ℓ₁`: only `Q`, which is at squared
distance 19 because the torsion `(b, c₁, b)` is trans — `δ₁₁ ≤ 10 + 4`. ∎

**Lemma 3.2 (one more bead) [proved].**  For a bridge `x` with `N ≥ 3` beads, appending the bead `P + c₁` (`c₁` as
above) gives a bridge with `N+1` beads and `(h,g)` larger by a vector in `[0,1]×[0,3]×[0,6]×[0,1]`, of norm
`≤ β′ := 28`.  (Same counting for `ℓ₁` alone.)

*Numerical check of the constants* **[numerical]** (`code/g2_concat.py`): all bridges with `3 ≤ N ≤ 8` beads starting
on an `A` site (508 bridges; 61 312 ordered pairs — all pairs up to 4 000 per pair of sizes) and 29 376 sampled
pairs with `N ≤ 11`: for every pair all admissible concatenations (all eight symmetries, both `c₁`) were built from
coordinates, checked to be self-avoiding lattice walks and bridges with `N₁+N₂+3` beads, and recounted from scratch.
The smallest gauche excess is always `[b′ down]`, it is attained by the prescribed choice, and all errors lie in
the proved intervals; the observed maxima are `(δ₃, δ₈, δ₁₁, δ_g) = (0, 1, 3, 1)` for `N ≤ 8` and `(0, 2, 5, 1)` for
`N ≤ 11` — the proved constants `(1, 9, 14, 1)` are worst cases that need many beads near the top level.

### 3.3 The limit-shape theorem

**Lemma 3.3 (abstract) [proved; the argument is Fekete's lemma for sets].**  Let `(Q_M)_{M ≥ M₀}` be non-empty
subsets of a normed space `ℝ^d` with
(C) for `q₁ ∈ Q_{M₁}`, `q₂ ∈ Q_{M₂}` there is `q ∈ Q_{M₁+M₂}` with `|q − q₁ − q₂| ≤ β`;
(E) for `q ∈ Q_M` there is `q′ ∈ Q_{M+1}` with `|q′ − q| ≤ β′`;
(B) `|q| ≤ R·M` for `q ∈ Q_M`.
Then `E_M := Q_M / M` converges in the Hausdorff metric to a non-empty compact **convex** set `K`, and
(i) `E_M ⊂ K + B̄(β/M)` for every `M`;
(ii) `E_m ⊂ E_M + B̄(β/m + m(β′+R)/M)` for all `M ≥ m ≥ M₀`.

*Proof.*  (ii) Let `q ∈ Q_m`, `M = km + r`, `0 ≤ r < m`.  By (C), `k−1` times, there is `q_k ∈ Q_{km}` with
`|q_k − kq| ≤ (k−1)β`; by (E), `r` times, `q′ ∈ Q_M` with `|q′ − q_k| ≤ rβ′`.  Then
`|q′/M − q/m| ≤ |q′ − kq|/M + k|q|·(1/(km) − 1/M) ≤ ((k−1)β + rβ′)/M + |q| r/(mM) ≤ β/m + m(β′+R)/M`.
*Existence of the limit.*  Let `K₋` be the set of points `q` with `dist(q, E_M) → 0` and `K₊` the set of cluster
points of sequences `q_j ∈ E_{M_j}`, `M_j → ∞`; `K₋ ⊂ K₊`, both closed, `K₊ ≠ ∅` by (B).  Claim: every `q ∈ E_m` has
`dist(q, K₋) ≤ 2(β+β′+R)/m`.  Put `M₁ = m`, `M_{j+1} = M_j²`, `q₁ = q`, and choose by (ii) `q_{j+1} ∈ E_{M_{j+1}}`
with `|q_{j+1} − q_j| ≤ (β+β′+R)/M_j`.  The sequence converges to some `q*` with `|q* − q| ≤ 2(β+β′+R)/m`.  For
`M_j ≤ M < M_{j+1}`, (ii) applied to `q_{j−1} ∈ E_{√M_j}` gives `dist(q_{j−1}, E_M) ≤ (β+β′+R)/√M_j → 0`, so
`q* ∈ K₋`.  The claim gives `K₊ ⊂ K₋` (closedness), so `K := K₋ = K₊`, compact; `sup_{E_M} dist(·, K) → 0` by the
claim, and `sup_K dist(·, E_M) → 0` because these `1`-Lipschitz functions converge pointwise on a compact set.
(i) For `q ∈ Q_M` and every `k` there is `q_k ∈ Q_{kM}` with `|q_k/(kM) − q/M| < β/M`; let `k → ∞`.
*Convexity.*  Let `q, q′ ∈ K`, `q_m, q′_m ∈ E_m` with `q_m → q`, `q′_m → q′`, and integers `a, b ≥ 0`, `a+b ≥ 1`.
By (C) there is `q″ ∈ Q_{(a+b)m}` with `|q″ − am q_m − bm q′_m| ≤ (a+b−1)β`, so by (i)
`dist((a q_m + b q′_m)/(a+b), K) ≤ 2β/m`; let `m → ∞`, then use that `K` is closed and rational weights are dense. ∎

**Theorem 3.4 (limit shape for bridges) [proved].**  There is a compact convex set `K^{br} ⊂ Box ⊂ ℝ⁴` with
`d_H(𝒟_N^{br}, K^{br}) → 0`.  Every point of `𝒟_N^{br}` lies within `168/(N+3)` of `K^{br}` (norm `‖p‖_c + |g|`).
Consequently `𝒦 := π(K^{br}) ⊂ ℝ³` (profile densities) is compact convex, `γ(p) := min{g : (p,g) ∈ K^{br}}` is a
convex function `𝒦 → [0,1]`, and the truncated epigraphs `{(h/N, t) : γ^{br}_N(h)/N ≤ t ≤ 1}` converge in the
Hausdorff metric to `{(p,t) : p ∈ 𝒦, γ(p) ≤ t ≤ 1}`.

*Proof.*  `Q_M := P_{M−3}` (`M ≥ 6`) satisfies (C) by Lemma 3.1, (E) by Lemma 3.2 and (B) with `R = 36`.  Lemma 3.3
gives `K^{br}`; `𝒟_N^{br} = E_{N+3}·(N+3)/N`, and `|q/N − q/(N+3)| ≤ 3R/(N+3)`, so the limit is the same and the
distance of a point of `𝒟_N^{br}` to `K^{br}` is at most `(β + 3R)/(N+3) = 168/(N+3)`.  The epigraph statement follows
because `F ↦ F^↑ = {(p,t) : (p,g) ∈ F, g ≤ t ≤ 1}` is `1`-Lipschitz for `d_H`, and `(K^{br})^↑` is the epigraph of `γ`
(convex because `K^{br}` is). ∎

**What the argument gives about the rate.**  One-sided and asymmetric **[proved]**: finite sets never stick out of
the limit by more than `168/(N+3)`; the argument gives **no** rate for how fast they fill it (a super-additive
sequence can converge arbitrarily slowly from below).  §4.4 shows that the filling cannot be faster than
`const·N^{−1/3}`, and is exactly of that order at the compact vertex.

**Remarks.**  (1) The same proof with "weak at both ends" or with a different coordinate axis gives the same set
(axes are exchanged by lattice symmetries; a weak bridge becomes a bridge after one extra bond).  (2) `K^{br}` is the
support of the joint density function of `(h, g)` for bridges in the sense of Janse van Rensburg's theory of
supermultiplicative models; that theory would give in addition a concave entropy function on `K^{br}` — not needed
here.  The existence of such limits for concatenable classes is **[known]** in substance (§10); I did not find this
statement for this model.

### 3.4 Rings **[sketch]**

For self-avoiding polygons (`N` even; pairs at cyclic separation `≥ 3`) the classical concatenation works: let `t`
be the lexicographically largest site of `ω¹` in the order `(y, x, z)`.  Both neighbours of `t` in the ring are its
two down-neighbours; for the one, `t⁻`, reached by the down-bond with the larger `x`-component, the other
up-neighbour `t′` of `t⁻` is lexicographically larger than `t`, hence free, as is everything above height `y(t)`.
Symmetrically for the lexicographically smallest site of `ω²`.  Remove the bonds `(t, t⁻)` and its mirror in `ω²`,
place `ω²` above `ω¹` with a gap of `c₀` free levels, and join the four ends by two disjoint strands through the
gap.  This gives a ring with `N₁ + N₂ + c₁` sites and errors `O(1)` in every pair count and in `g` (all changes
are within a bounded distance of `t` and of the bottom site), hence, by Lemma 3.3 (with (E) replaced by "two more
sites": insert a kink in the top), a compact convex limit `K^{ring}`.  *Missing:* the explicit routing of the two
strands on this lattice (a finite case analysis over the local shapes at `t`), the values of `c₀, c₁` and of the
error constants, and a numerical check.  A ring minus one bond is a walk, so `K^{ring} ⊂ liminf 𝒟_N`; I could prove
neither `K^{ring} ⊂ K^{br}` nor the converse (both reductions need a return strand whose length is the span of the
object, which is `o(N)` only for compact shapes; §5).

---

## 4. What the limit object looks like: outer bounds for all walks, inner points from bridges

Lemma 2.1 turns the profile part of the question into a ground-state problem for a lattice gas, for which there is
a standard machinery (§10): linear programmes over the frequencies of local configurations give *outer* bounds
valid for **every** walk, periodic constructions give *inner* points.  Notation: `p = (p₃,p₈,p₁₁)` stands for
`(e₃/N − 1, e₈/N − 1, e₁₁/N)`; for a walk `h/N = p + (1/N, 2/N, 0)`.

### 4.1 Outer bounds valid for all walks

**Proposition 4.1 (the `(p₃,p₈)` plane, by hand) [proved].**  For every walk with `N` beads

    h₈ ≥ 4h₃ − 2,        h₈ ≥ 6h₃ − N − 4,        h₈ ≤ 2h₃ + 3N + 3,        h₃ ≥ 0.

So every limit point of `(h₃, h₈)/N` lies in the quadrilateral `conv{(0,0), (½,2), (1,5), (0,3)}` (area 7/4, against
5 for the bulk rectangle).

*Proof.*  By Lemma 2.3, `e₃ = ½Σ_{m∈S} d(m)` and `e₈ = Σ_{m∈S} C(d(m),2) + Σ_{m∉S} C(d(m),2)`.  For integers `0 ≤ d ≤ 4`,
`C(d,2) ≥ 2d − 3` and `C(d,2) ≥ 3d − 6`; summing over `S` and dropping the second sum, `e₈ ≥ 4e₃ − 3N` and
`e₈ ≥ 6e₃ − 6N`; insert `e₃ = h₃+N−1`, `e₈ = h₈+N−2`.  For the upper bound: `C(d,2) ≤ (5d−8)/2` for `d ∈ {2,3,4}` and
`≤ (5d−8)/2 + 3/2` for `d = 1` (at most two sites of a walk have `d = 1`, none has `d = 0`), and `C(d,2) ≤ 3d/2` for
`0 ≤ d ≤ 4`; with `Σ_{m∉S} d(m) = 4N − 2e₃` this gives `e₈ ≤ 5e₃ − 4N + 3 + 6N − 3e₃ = 2e₃ + 2N + 3`. ∎
Equality structures: all occupied sites of degree 2 and no vacant site with two occupied neighbours (isolated rod);
all of degree 3 (the buckled honeycomb layer = one row of rods); all of degree 4 (the full lattice); and, for the
upper bound, all occupied sites of degree 2 with every vacant site next to an occupied one having four occupied
neighbours (the crossed-rod "woodpile" `W₃` of §4.2).

**Theorem 4.2 (eleven inequalities for all finite sets; computer-assisted, exact arithmetic) [proved].**  Let `S` be
a finite set of `N` lattice sites, `n_E` of which have fewer than two occupied neighbours.  For each row `(c, b, M)`
of the table

    c₃(e₃ − N) + c₈(e₈ − N) + c₁₁ e₁₁  ≤  b·N + 2M·n_E .

| `c = (c₃, c₈, c₁₁)` | `b` | `M` | read as |
|---|---|---|---|
| `(−1, 0, 0)` | 0 | ½ | `p₃ ≥ 0` |
| `(4, −1, 0)` | 0 | 5 | `p₈ ≥ 4p₃` |
| `(6, −1, 0)` | 1 | 6 | `p₈ ≥ 6p₃ − 1` |
| `(−2, 1, 0)` | 3 | 2 | `p₈ ≤ 3 + 2p₃` |
| `(−1, 1, −1)` | 0 | 3 | `p₁₁ ≥ p₈ − p₃` |
| `(−1, 2, −1)` | 3 | 4 | `p₁₁ ≥ 2p₈ − p₃ − 3` |
| `(−4, 2, −1)` | 2 | 6 | `p₁₁ ≥ 2p₈ − 4p₃ − 2` |
| `(3, 4, −3)` | 5 | 6 | `3p₁₁ ≥ 3p₃ + 4p₈ − 5` |
| `(6, −2, 1)` | 2 | 6 | `p₁₁ ≤ 2 + 2p₈ − 6p₃` |
| `(0, −1, 2)` | 7 | 1 | `2p₁₁ ≤ 7 + p₈` |
| `(−3, 0, 2)` | 9 | 3 | `2p₁₁ ≤ 9 + 3p₃` |

In particular every walk with `N` beads satisfies `c·h ≤ bN + 4M + c₃ + 2c₈`, and every limit point of the profile
densities of walks (bridges, rings) lies in the polytope `𝒦₁ = {p : c·p ≤ b for the eleven rows}`, which has 12
vertices

    (0,0,0), (0,0,2), (0,1,4), (0,2,2), (0,2,9/2), (0,3,4), (0,3,9/2), (⅓,3,8/3), (⅓,11/3,4), (½,2,3/2), (½,2,3), (1,5,6)

and volume `3.2269`, i.e. 10.8 % of the bulk box (`48.40` in `u`-coordinates, against 450).

*Proof.*  Fix the 8-site cluster of a lattice bond `(v,w)`: `v`, `w`, the three other neighbours `u₁,u₂,u₃` of `v`
and `z₁,z₂,z₃` of `w`, labelled so that `(u_j, v, w, z_j)` is trans.  By Lemma 2.3,
`e₃ = Σ_bonds [v][w]`, `e₈ = Σ_bonds ¼(C(d_v,2) + C(d_w,2))` (every site is an end of four bonds),
`e₁₁ = ½ Σ_bonds Σ_{j≠k}[u_j][z_k]`, and `N = Σ_bonds ¼([v]+[w])`, where `d_v = [w]+Σ[u_j]`, `d_w = [v]+Σ[z_j]`.
Let `n(σ)` be the number of lattice bonds whose cluster has occupation pattern `σ ∈ {0,1}⁸`, averaged over the 48
point-group operations applied to `S` (the counts `e_d` are invariant), and `μ = n/(2N)`.  Then (1) `μ(v=1) = 1`;
(2) `μ` is invariant under the 12 symmetries of the cluster (permutations of the index `j`, exchange of the two
ends); (3) the marginal of `μ` on the star `(v; w,u₁,u₂,u₃)` is invariant under all permutations of the four
neighbours (the stabiliser of a site acts on its neighbours as the full symmetric group, and every bond at `v`
occurs as the distinguished one); and `e₃/N = 2μ(vw)`, `e₈/N = μ((C(d_v,2)+C(d_w,2))/2)`, `e₁₁/N = μ(Σ_{j≠k}u_jz_k)`.
Call a pattern *forbidden* if an occupied centre has fewer than two occupied neighbours; at most `4n_E` bonds have
a forbidden pattern, so `μ(forbidden) ≤ 2n_E/N`.  The script `code/lp_exact.py` groups the 256 patterns into 46
orbits (32 allowed), writes the six independent star relations of (3) as functions `r_k` with `μ(r_k) = 0`, and
verifies **with exact rational arithmetic**, for each row, integer multipliers `y₁…y₆, y₀` (printed in
`out/lp_exact.txt`) with

    c₃·2[v][w] + c₈·(C(d_v,2)+C(d_w,2))/2 + c₁₁ Σ_{j≠k}u_jz_k  −  Σ_k y_k r_k  −  y₀([v]+[w])/2   ≤  0   on every allowed orbit

(functions averaged over the orbit, which changes no `μ`-integral), `y₀ = b + c₃ + c₈`, and `≤ M` on the forbidden
orbits.  Integrating against `μ` gives
`c₃e₃/N + c₈e₈/N + c₁₁e₁₁/N ≤ y₀ + M·2n_E/N`.  The vertex list and the volume are those of the polytope cut out by
the eleven rows (numerically it coincides with the set of `p` attainable in the linear programme "(1)–(3), no mass
on forbidden patterns", `code/cluster_lp.py`; this is not needed). ∎
(The rows of Proposition 4.1 are among them.  The finite forms were also checked directly on all 9 188 bridges with
`N ≤ 11` and on six lamellae, `code/g1_local.py`; and all 20 075 periodic site sets with degrees `≥ 2` and cell
index `≤ 12` satisfy the eleven inequalities exactly, with equality attained, `code/check_inside.py`; and the
finite form with `n_E` holds on 1 800 random finite site sets of arbitrary degrees, `code/check_thm42_random.py`.)

**Theorem 4.2′ (path-cluster programme: the chain is used) [proved for limit points; exact certificates].**
Mark the bonds of the walk in the cluster: an occupied centre has exactly two marked bonds (true for all beads
but the two ends, whose `O(1/N)` mass disappears in the limit).  The empirical distribution of marked clusters
satisfies the analogues of (1)–(3) (340 configurations, 48 orbits, 7 independent star relations;
`code/cluster_lp4.py`), `p` is given by the same formulas, and the gauche density is
`q = 2μ(vw marked, the other marked bonds vu_j and wz_k with j ≠ k)`.  Every limit point `(p, q)` of `(h, g)/N` over
walks satisfies, with integer multipliers verified in exact arithmetic (`code/lp4_exact.py`,
`code/lp4_gamma_cert.py`):
(i) the twelve inequalities `c·p ≤ b` with `(c; b)` =
`(−1,0,0; 0)`, `(4,−1,0; 0)`, `(6,−1,0; 1)`, `(−2,1,0; 3)`, `(−1,1,−1; 0)`, `(−1,2,−1; 3)`, `(−3,2,−1; 2)`, `(−3,4,−3; 2)`,
`(3,4,−3; 5)`, `(6,−2,1; 2)`, `(0,−1,2; 7)`, `(−3,0,2; 9)`, which cut out a polytope `𝒦₂ ⊂ 𝒦₁` of volume `3.125`
(`46.88` in `u`-coordinates) with the 12 vertices
`(0,0,0), (0,0,2), (0,1,4), (0,2,2), (0,2,9/2), (0,3,4), (0,3,9/2), (½,2,3/2), (½,2,3), (½,7/2,7/2), (½,4,9/2), (1,5,6)`
(the vertex `(⅓,11/3,4)` of `𝒦₁` is attained by a periodic set with twice as many `A` as `B` sites, which no chain
can trace; the marks exclude it);
(ii) three lower bounds for the gauche density:

    q ≥ 2p₁₁ − 5p₃ − 8,        q ≥ 2p₁₁ − p₈ − 7,        q ≥ p₁₁ + p₈ − 4p₃ − 7 .

In words: more than four third-neighbour pairs per bead (plus 2.5 per contact) force gauche torsions.
*Numerical only* (floating-point LP, `code/cluster_lp4_zero.py`, `code/gamma_lp_points.py`): the set of profile
densities compatible with `q = 0` has volume `2.729` (13 vertices); `γ_LP(p) := min q` at fixed `p` equals `4/5` at
`(0,12/5,22/5)` and `5/7` at `(0,18/7,61/14)` — both given by the first inequality of (ii).

### 4.2 Inner points: explicit bridges

**Rods.**  The all-trans zigzag with bonds `+a₀, −a₁` ("rod", direction `(0,1,1)`) is a bridge for every `N`, with
`h = 0`, `g = 0`: `(0,0,0;0) ∈ K^{br}` **[proved]**.  The diamond lattice is the disjoint union of the parallel rods
`R_{m,q} = R₀ + m(2,2,0) + q(2,0,2)`; rod `R_{m,q}` consists of the sites `A_k = m(2,2,0)+q(2,0,2)+k(0,2,2)`,
`B_k = A_k + (1,1,1)`, and besides the rod bonds `A_k B_k`, `B_k A_{k+1}` there are *rungs* `B^{(m,q)}_k A^{(m+1,q)}_k`
and `B^{(m,q)}_k A^{(m,q+1)}_k`.  Two parallel rods have pairs inside the cutoff only at the eight offsets
`±(1,0), ±(0,1)` [type 1: `(1,4,3)` pairs at squared distances `(3,8,11)` per period], `±(1,−1)` [type 2: `(0,2,4)`],
`±(1,1)` [type 3: `(0,0,2)`] (`code/rodpairs.py`; all other rods are at squared distance `≥ 19`).

**Proposition 4.3 (rung-folded lamellae) [proved].**  For odd `M, Q` and `ℓ ≥ 2` there is a bridge `Λ(M,Q,ℓ)` whose
site set is the block of stems `{R_{m,q} : 0 ≤ m < M, 0 ≤ q < Q}`, each cut to `ℓ` periods (`±1` site at the ends),
traversed in snake order, consecutive stems being joined **by a single rung bond** (no linker sites); it has
`N = 2ℓMQ + O(MQ)` beads, `g ≤ 3(MQ−1)`, and

    h = ℓ·[ (2MQ − M − Q)(1,4,3) + (M−1)(Q−1)·((0,2,4) + (0,0,2)) ] + O(MQ) .

Hence `(½, 2, 3/2; 0) ∈ K^{br}` (`Q = 1`, `M, ℓ → ∞`: one row = the buckled honeycomb layer) and
`(1, 5, 6; 0) ∈ K^{br}` (`M, Q, ℓ → ∞`: the crystal), and by convexity the triangle

    T₀ = conv{(0,0,0), (½,2,3/2), (1,5,6)} × {0}  ⊂  K^{br},        so  γ = 0 on T₀.

With `M = Q ≈ ℓ ≈ N^{1/3}` the crystal vertex is approached at distance `O(N^{−1/3})`.

*Proof.*  The walk (`code/lamella.py`): rods in the order `q = 0, 1, …`, within row `q` in the direction `+m` for
even `q` and `−m` for odd `q`; stems alternately upwards and downwards; an upward stem ends at `B_{ℓ−1}` and jumps
to `A_{ℓ−1}` of the next rod if the next rod is `(m+1,q)` or `(m,q+1)`, and ends at `A_{ℓ−1}` and jumps to
`B_{ℓ−1}` of the next rod if that is `(m−1,q)`; downward stems likewise with `k = 0`; the first stem starts at
`A_{−1}`, the last (upward, because `MQ` is odd) ends at `B_ℓ`.  Stems lie on distinct rods, hence are disjoint;
jumps are rungs; so this is a self-avoiding walk.  Heights: `y = 2m + t` at position `t` (`t = 2k` for `A_k`, `2k+1`
for `B_k`) of rod `(m,q)`, so the first bead (`t = −2` on rod `(0,0)`) is strictly lowest and the last (`t = 2ℓ+1`
on rod `(M−1,Q−1)`) highest.  Only the torsions that contain a rung can be gauche.  Pair counts: by Lemma 2.1 they
depend on the block only; rods interact at the eight offsets, with the stated numbers per period of overlap, and
the sites within the cutoff of a stem end are `O(1)` per stem.  The numbers of rod pairs of types 1, 2, 3 in an
`M×Q` block are `2MQ−M−Q`, `(M−1)(Q−1)`, `(M−1)(Q−1)`. ∎
*Check* **[numerical]** (`out/lamella.txt`; every walk verified to be a self-avoiding bridge, profile from
coordinates): one row, `N = 16 580`: `(h/N, g/N) = (0.4864, 1.9493, 1.4668; 0.0116)`; crystal `25×25×26`,
`N = 31 880`: `(0.9215, 4.6088, 5.4768; 0.0587)`, with `(1 − h₃/N)·N^{1/3} = 2.40…2.49` for `N = 68…31 880`.

**Periodic chain systems (exhaustive for small cells).**  A *periodic chain system* is a set of bonds, invariant
under a sublattice `L′` of index `K` of the fcc lattice, in which every site has degree 0 or 2 and all components
are infinite chains.  `code/pchain.c` enumerates **all** of them for `K ≤ 12` (`1.23·10⁹` systems at `K = 12`) and
records, per cell, the exact site and pair counts and the smallest and largest number of gauche torsions; 5 680
distinct profile densities result.

| quantity (cell index `≤ K`) | `K = 4` | 6 | 8 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|
| volume of the hull of profile densities, chain systems | 1.861 | 2.056 | 2.078 | 2.125 | 2.129 | 2.223 |
| the same for all periodic site sets with all degrees `≥ 2` (`code/periodic.c`; includes ring packings) | 2.000 | 2.208 | 2.319 | 2.351 | 2.355 | 2.490 |
| zero-gauche (rod) systems only | 1.694 | 1.750 | 1.750 | 1.750 | 1.750 | 1.833 |

Vertices of the hull for `K ≤ 12` (exact densities; `g` = smallest gauche density found at that profile):

| `(p₃, p₈, p₁₁)` | `g` | structure |
|---|---|---|
| `(0,0,0)` | 0 | isolated rods |
| `(½,2,3/2)` | 0 | one row of rods, type-1 neighbours (honeycomb layer) |
| `(1,5,6)` | 0 (also 1: all-gauche `4₁` helices) | the full lattice |
| `(0,1,3)` | 0 | checkerboard of parallel rods (types 2 and 3 only) |
| `(0,1,1)` | 0 | rods, `K = 12` |
| `(0,3,4)` | 0 | woodpile `W₃`: planes `x ≡ 0 (mod 3)` empty, rods along `(0,1,−1)` and `(0,1,1)` in alternate slabs |
| `(½,2,5/2)` | 0 | rods |
| `(½,4,9/2)` | 0 | crossed rods (a vertex of `𝒦₂`: attained) |
| `(0,0,3/2)` | 1 | all-gauche chains with third-neighbour contacts only (`K = 12`) |
| `(0,12/5,22/5)` | 4/5 | `= 2p₁₁ − 5p₃ − 8` there: the gauche density is forced |
| `(0,18/7,61/14)` | 5/7 | `= 2p₁₁ − 5p₃ − 8` there |
| `(0,27/14,4)`, `(1/16,23/8,35/8)`, `(⅓,10/3,5)` | 6/7, 3/4, 2/3 | (lower bounds `γ_LP` = 0.07, 0.44, 0.33) |

**Proposition 4.4 (from periodic systems to bridges) [sketch + numerical].**  The density `(p; g)` of every periodic
chain system belongs to `K^{br}`.  *Sketch:* take the bonds of the system inside a box of side `W`; the strands end
on the surface, at mutual distances `O(1)`; link them through the free space outside the box by paths of bounded
length, and add two tails to make a bridge; the changes are `O(W²)` against `N ≍ W³`.  *Missing:* a routing lemma
that produces the `O(W²)` disjoint linkers for an arbitrary periodic pattern of strand ends (I have it only for
rung folds, Proposition 4.3).  *Numerical support* (`code/build.py`: box cut, greedy linking by breadth-first
search, tails; every output verified to be a self-avoiding bridge, counts from coordinates; `out/build.txt`):

| system (ideal `(p₃,p₈,p₁₁; g)`) | box 16 | 32 | 48 | 64 (`N`) |
|---|---|---|---|---|
| `W₃` `(0,3,4;0)` | `(0.04,1.86,2.83;0.34)` | `(0.03,2.39,3.41;0.20)` | `(0.02,2.60,3.63;0.14)` | `(0.017,2.69,3.72;0.105)` (22 351) |
| checkerboard `(0,1,3;0)` | `(0.09,1.03,2.27;0.33)` | `(0.06,1.06,2.63;0.22)` | `(0.05,1.05,2.75;0.16)` | `(0.037,1.05,2.81;0.12)` (17 796) |
| crossed rods `(½,4,9/2;0)` | `(0.40,2.72,3.30;0.30)` | `(0.45,3.34,3.92;0.18)` | `(0.45,3.49,4.08;0.13)` | `(0.458,3.61,4.18;0.10)` (27 144) |
| `(0,12/5,22/5;4/5)` | `(0.09,1.59,2.73;0.69)` | `(0.04,1.93,3.47;0.76)` | `(0.03,2.08,3.76;0.77)` | `(0.029,2.16,3.90;0.78)` (21 235) |
| `(⅓,5/3,3;⅔)` | `(0.27,1.39,2.33;0.62)` | `(0.29,1.50,2.62;0.65)` | `(0.30,1.54,2.74;0.66)` | `(0.308,1.57,2.80;0.66)` (16 238) |
| `(0,½,9/4;1)` | `(0.02,0.45,1.73;0.90)` | `(0.03,0.55,2.02;0.94)` | `(0.01,0.49,2.06;0.96)` | `(0.010,0.50,2.11;0.97)` (12 767) |

The deviations decrease like `1/W` (for `W₃`: `|p₈ − 3|·W = 18.2, 19.7, 19.4, 19.8`).  Each row entry is an actual
bridge and therefore, by Theorem 3.4, within `168/(N+3)` of `K^{br}` **[proved]** — e.g. `K^{br}` contains a point
within `0.0075` of `(0.0171, 2.6912, 3.7189; 0.1051)`.

### 4.3 The picture

* **`𝒦` (profile part) is a thin body.**  `2.2234 ≤ vol 𝒦` if Proposition 4.4 holds (rod part alone: `1.8333`), and
  `vol 𝒦 ≤ 3.125` **[proved]** (Theorem 4.2′; `≤ 3.2269` for all finite site sets): between 7.4 % and 10.4 % of the bulk
  box that Proposition 11.49(a) and the grid bounds use.  In `u`-coordinates: between `33.4` and `46.9`, with
  diameter 35.  The inner volumes still grow with the cell index (`+4 %` from 11 to 12): the true body is not
  determined.
* **Five vertices are settled** (outer bound = construction): `(0,0,0)`, `(½,2,3/2)`, `(1,5,6)` **[proved]**;
  `(0,3,4)`, `(½,4,9/2)` [construction: sketch + numerical].  Seven vertices of `𝒦₂` —
  `(0,0,2)`, `(0,1,4)`, `(0,2,2)`, `(0,2,9/2)`, `(0,3,9/2)`, `(½,2,3)`, `(½,7/2,7/2)` — are not attained by any chain
  system with cell index `≤ 12`; they are either artefacts of the one-bond cluster or need larger cells.
* **`γ` is not identically zero [proved, computer-assisted].**  `γ = 0` on `T₀` **[proved]** (and on the hull of the
  rod systems, given Proposition 4.4), but the `p₁₁`-rich part of `𝒦` can only be reached with gauche torsions.
  *Proof:* the bridge with `N = 166 199` beads built from the system `(0,12/5,22/5; 4/5)` in a box of side 128
  (`out/build_gauche_W128.txt`: `(h₃,h₈,h₁₁,g) = (1 717, 376 013, 687 789, 131 710)`, verified from coordinates) has
  `2h₁₁ − 5h₃ − 8N = 37 401 = 0.225N`; by Theorem 3.4 a point `(p*, g*)` of `K^{br}` lies within `0.00101` of its
  density, and `p ↦ 2p₁₁ − 5p₃` is 2-Lipschitz for `‖·‖_c`, so `2p₁₁* − 5p₃* − 8 ≥ 0.22`; by Theorem 4.2′(ii) every
  sequence of walks with profile density `→ p*` has gauche density `≥ 0.22`: `γ(p*) ≥ 0.22`. ∎  At the ideal point
  `(0,12/5,22/5)` bound and construction agree, `γ = 4/5` (given Proposition 4.4).  In the inner model (`K ≤ 12`),
  `γ > 0.02` on 16 % of the volume.
  So the limit object has the form asked for in question 1 — a convex body with a convex function on it — and the
  function is non-trivial.
* **Finite sizes are far from it.**  At 27 beads the exact profile set has hull volume `0.228` per `N³` — a tenth
  of the limit — and its lower boundary is far from convex (§5.4).

### 4.4 The rate at the compact end: a surface term, with proof

**Proposition 4.5 (isoperimetry) [proved].**  For every finite set `S` of `N` sites
`e₃(S) ≤ 2N − 2^{−2/3}N^{2/3}` and `e₈(S) ≤ 6N − 3N^{2/3}`.  Hence for every walk
`‖N^x‖₁ = 9h₃ + 4h₈ + h₁₁ ≤ 35N − 17.6·N^{2/3} + 17`, i.e. `max ‖N^x‖₁/N ≤ 35(1 − 0.50·N^{−1/3}) + 17/N`.

*Proof.*  For `f = 1,2,3` the bonds of types `a₀` and `a_f` partition the lattice into parallel rods; in fcc
coordinates (`A(n) = n₁(0,2,2)+n₂(2,0,2)+n₃(2,2,0)`, `B(n) = A(n)+(1,1,1)`) the rod through `A(n)` contains
`A(n+ke_f)`, `B(n+ke_f)`.  A rod that meets `S` carries at least two bonds between an occupied and a vacant site;
a boundary bond of type `a₀` lies on three of these rods, one of type `a_f` on one.  So the number `∂` of boundary
bonds satisfies `3∂ ≥ 2Σ_f ρ_f`, `ρ_f` = number of rods of family `f` meeting `S`.  Let `S_A` be the larger
sublattice part, `|S_A| ≥ N/2`; `ρ_f ≥ |π_f S_A|` (projection along `e_f`), and by the Loomis–Whitney inequality
`|S_A|² ≤ Π_f|π_fS_A|`, so `Σ_f ρ_f ≥ 3(N/2)^{2/3}` and `∂ ≥ 2(N/2)^{2/3}`; `e₃ = (4N − ∂)/2`.  For `e₈`: within one
sublattice the second neighbours are `±e_f, ±(e_f − e_{f′})`; every line in direction `e_f` that meets `S_A` has
two (site, vacant second neighbour) incidences, so `2e₈(S_A) ≤ 12|S_A| − 2Σ_f|π_fS_A| ≤ 12|S_A| − 6|S_A|^{2/3}`; the
same for `S_B`, and `x^{2/3}+y^{2/3} ≥ (x+y)^{2/3}`.  Last claim: Lemma 2.1(b) and `e₁₁ ≤ 6N`. ∎

**Corollary 4.6 (the convergence of the shape is exactly of order `N^{−1/3}` at the compact vertex) [proved].**
`(1,5,6;0) ∈ K^{br}` (Proposition 4.3), every point of `𝒟_N` (walks or bridges) is at `‖·‖_c`-distance
`≥ 17.6·N^{−1/3} − 17/N` from it, and the lamellae come within `O(N^{−1/3})`.  So
`d_H(𝒟_N^{br}, K^{br}) ≥ 17.6·N^{−1/3} − 17/N`, whereas the outer deviation is `≤ 168/(N+3)` (Theorem 3.4).

**The surface law is visible in the exact data [numerical]** (`out/g5_finiteN.txt`): with
`k_N := (1 − max‖N^x‖₁/(35N))·N^{1/3}`, the class tables give `k_N ∈ [1.71, 1.86]` for every `N` from 8 to 27
(`1.80` at 11, `1.79` at 15, `1.86` at 20, `1.84` at 27), and the bridges have the same maximum as the walks for all
`N ≤ 24` except `N = 17, 18`.  So

    max ‖N^x‖₁ / N  ≈  35·(1 − 1.8·N^{−1/3}),       bounds:  35(1 − 2.5 N^{−1/3})  [lamellae, computed to N = 31 880]  ≤  max  ≤  35(1 − 0.50 N^{−1/3}) + 17/N  [proved].

The finite-size table of ENG-RES-0002 (38 % of the bulk extent at 27 beads) is this law: `1 − 1.84/3 = 0.39`.
Half of the bulk extent needs `N ≈ 47`, 80 % needs `N ≈ 730`, 90 % needs `N ≈ 5 800`.

---

## 5. G3 — unrestricted walks

`𝒟_N := {(h(x), g(x))/N : x a walk with N beads}`; `F^↑ := {(p,t) : (p,g) ∈ F, g ≤ t ≤ 1}`.

### 5.1 Statement, and equivalent forms

**Fact 5.1 [proved].**  `K^{br} ⊂ liminf 𝒟_N` (bridges are walks), and every limit point `(p,q)` of `𝒟_N` has `p ∈ 𝒦₂ ⊂ 𝒦₁`
and `q ≥ max(0, 2p₁₁ − 5p₃ − 8)` (Theorems 4.2, 4.2′).

**Conjecture 5.2 [conjecture].**  `𝒟_N → K^{br}` in the Hausdorff metric.  **5.2′ (all that certificates need):**
`𝒟_N^↑ → (K^{br})^↑`, i.e. the profile sets of walks converge to `𝒦` and their lower boundaries to `γ` in the sense of
epigraphs.

**Lemma 5.3 (reformulation as a ground-state problem) [proved].**  Conjecture 5.2 holds iff for every `u ∈ ℝ⁴`

    limsup_N  max_{x walk, N beads}  u·(h(x), g(x)) / N   ≤   max_{q ∈ K^{br}} u·q ,

and 5.2′ holds iff this is true for all `u` with `u_g ≤ 0`.  In words: for every energy `E_u = −u₃h₃ − u₈h₈ − u₁₁h₁₁ −
u_g·#gauche` — a pair interaction on three shells plus a stiffness term — walks and bridges have the same
ground-state energy per bead (5.2′: for all such energies in which gauche torsions are not rewarded).

*Proof.*  `K^{br}` is compact and convex, so a point is outside it iff some linear functional separates it; with
Fact 5.1 this is the first claim.  For the second, `(K^{br})^↑` is compact convex with support function
`max_{K^{br}} u·q` for `u_g ≤ 0` and `max_{p∈𝒦} u_p·p + u_g` for `u_g > 0`, and the latter is the case `u_g = 0` of the
former. ∎

### 5.2 What is proved towards it

**(a) Directions settled by matching bounds [proved].**  If `u_g ≤ 0` and `(u₃,u₈,u₁₁)` lies in the normal cone of
`𝒦₁` at one of the vertices `(0,0,0)`, `(½,2,3/2)`, `(1,5,6)`, then the inequality of Lemma 5.3 holds: the left
side is at most `u_p·v` by Theorem 4.2 and `g ≥ 0`, and bridges attain `u_p·v` with `g/N → 0` (Proposition 4.3).
These three cones contain 67 % of the 2 026 directions used to compute `𝒦₁` (`c = (9d₁, 4d₂, d₃)` with `d` uniform
on the sphere, and the 26 lattice directions; 75 more directions, 71 % in all, belong to the vertex `(0,3,4)`, where
the construction is only sketched).  In particular: **the maximal number of contacts, of second- and of third-neighbour pairs per bead and the
maximum of `‖N^x‖₁/N` are the same for walks and bridges in the limit, and the lower boundary
`p₈ ≥ max(4p₃, 6p₃−1)` of the `(p₃,p₈)` projection is attained by bridges.**

**(b) The decomposition principle [proved].**  Convexity means that a walk need not be turned into *one* bridge.

*Lemma 5.4.*  Let `x` be a walk with `N` beads and `x¹,…,x^k` bridges with `N₁,…,N_k` beads such that
`|(h,g)(x) − Σ_i (h,g)(x^i)| ≤ η` and `|N − Σ_i N_i| ≤ η`.  Then `dist((h,g)(x)/N, K^{br}) ≤ (168k + 37η)/(N − η)`.

*Proof.*  By Theorem 3.4, `(h,g)(x^i) ∈ N_iK^{br} + B̄(168)`; `Σ_i N_iK^{br} = N′K^{br}` (`N′ = ΣN_i`) by convexity, so
`(h,g)(x) ∈ N′K^{br} + B̄(168k+η)`; and `|(h,g)(x)|·|1/N − 1/N′| ≤ 36η/N′`. ∎

So Conjecture 5.2 is equivalent to: *every walk has the same `(h, g)`, up to `o(N)`, as a family of `o(N)` bridges
with `N + o(N)` beads in total.*  The bridges need not be pieces of the walk.

**(c) Site-local surgery is impossible [proved].**  *Proposition 5.5.*  Let `S` contain two adjacent parallel rods
(type-1 neighbours, e.g. `R_{0,0}` and `R_{1,0}`) over the heights `2…2ℓ−1` and no other site at these heights (the
double strand of a hairpin; the rest of the walk — the fold above, any tail below — is arbitrary).  Then there is
no bridge with a bead below height 2 whose site set `S′` satisfies `|S′ Δ S| < (ℓ−3)/2`.

*Proof.*  In the two-rod strip the sites `A^{(0)}_k` and `B^{(1)}_k` have exactly two neighbours in the strip (their
rod neighbours; the rungs join `B^{(0)}_k` to `A^{(1)}_k`), and between the levels `2j` and `2j+1` the strip has
exactly two bonds, `A^{(0)}_jB^{(0)}_j` and `A^{(1)}_{j−1}B^{(1)}_{j−1}`.  If `S′` coincides with `S` on the four levels
`2j−1…2j+2` (`2 ≤ j ≤ ℓ−2`), then `A^{(0)}_j` and `B^{(1)}_{j−1}` are interior beads of the bridge (the first bead
is below, the last — a highest one — at height `≥ 2j+2`) with only two available neighbours, so both bonds are used and the bridge crosses from level `2j` to `2j+1` exactly twice; but a walk
that starts below these levels and ends at its highest bead crosses an odd number of times.  A site of `S′ΔS`
spoils at most two values of `j`. ∎  (The degrees, the bonds between consecutive levels, and — by brute force for
`ℓ ≤ 6` — the absence of a Hamiltonian path from a lowest to a highest site of the strip: `code/strip_check.py`.)

*Consequence.*  For the *unequal hairpin* (double strand of `N/4` beads per arm on top of a single strand of
`N/2`) no bridge has a site set within `o(N)` of it; yet its `(h,g)` is that of two bridges up to `O(1)` — a
three-stem lamella `Λ(3,1,·)` of `3N/8` beads and a rod of `5N/8` (the same number, `N/8` periods, of type-1
adjacency; two folds instead of one) — so Lemma 5.4 applies with `k = 2`.  Any proof of the conjecture must use
convexity in this non-local way; in particular the literal surgery lemma "change `o(N)` sites" is false, while
"change `(N, h, g)` by `o(N)`" is open.

### 5.3 The obstruction, precisely  **[sketch / heuristic accounting — nothing in this subsection is a theorem]**

Cut a walk by planes into slabs or boxes of size `W` with `O(N/W)` crossings (possible by averaging over the
offset), delete the `O(N/W)` sites near the cuts, and separate the pieces.  By Lemma 5.4 it remains to realise the
content of each piece — a *bundle* of `k` strands whose ends lie on the surface of the piece, plus at most two
buried walk ends at depth `≤ W` — by bridges of the same `(h,g)` up to an error that sums to `o(N)`.  Three
facts decide what is easy:

1. A bundle whose strand ends are close together (compact pieces: `k ≍ W²` ends on faces of area `W²`) can be
   chained into one path by `O(1)` linker sites per strand; replicating the bundle `m` times and chaining the
   copies removes the parity problem (an even number of crossing strands ends at the wrong face) at relative cost
   `1/m`.  This is the regime in which the coordinator's attempt (ii) works, and the lifting by slabs makes the
   depth of a buried end `≤ W` for every walk, not only for globules.
2. A bundle with few strands (`k = O(1)`) can be replicated with shifts of length `O(k²)`, again at small cost.
3. **The hard case is in between**: `1 ≪ k ≪ W²` strands that interact in the interior of the piece but whose ends
   are spread over its surface at mutual distance `≫ 1` ("bow-tie": a tight bundle that splays out).  Chaining
   them costs of the order of the piece size per strand — comparable with the content — and Proposition 5.5 shows
   that no cheap re-threading inside the bundle exists in general.  The remedy is to cut again where the bundle
   is tight, but a walk can be a bow-tie at every scale, and I have no bound on the total cost of a multi-scale
   decomposition.  (Crude accounting: within-piece linking costs `≲ W√k`, replication `≲ k·(kW)^{2/3}`, content
   `≥ k·w` for strands of at least `w` sites; the ratio is not small when `√W ≲ k ≲ W` and the strands are short.)

No counterexample is known to me: every structure I can describe that defeats the cutting argument (jacks,
hierarchical bundles of doubled strands) has a density that is attained by bridges for the trivial reason of
Lemma 5.4.  A counterexample would have to be a walk whose interactions cannot be redistributed among `o(N)`
bridges — i.e. whose every near-optimal realisation, for some energy `E_u`, has both ends inaccessible.

### 5.4 Evidence from exhaustive enumeration **[numerical]**

Own enumeration of all walks (`N ≤ 23`), bridges (`N ≤ 24`; `1.4·10⁹` at `N = 24`) and half-space walks (`N ≤ 22`),
with the full set of realised `(h, g)` per class; walks for `N ≤ 27` from the other division's tables.
`code/g3_compare.py` → `out/g3_compare.txt`.

| `N` | classes: walks / bridges | max `‖N‖₁/N`: walks / bridges | one-sided distance walks(`N`) → bridges(`N+k`), `k = 0, 1, 2, 3` (units of `‖·‖_c`) | the same for lower boundaries `(h, gmin)` | `N_cov` (`L=1`): `ε=N/2` walks / bridges; `ε=N/4` walks / bridges |
|---|---|---|---|---|---|
| 12 | 129 / 101 | 7.667 / 7.667 | 6, 4, 4, 3 | 8, 5, 5, 4 | 5 / 5; 8 / 7 |
| 15 | 356 / 280 | 9.600 / 9.600 | 6, 4, 3, 3 | 7, 7, 6, 6 | 8 / 6; 13 / 11 |
| 18 | 818 / 656 | 10.556 / 10.500 | 7, 6, 5, 5 | 10, 9, 10, 10 | 9 / 8; 16 / 14 |
| 21 | 1 594 / 1 328 | 11.619 / 11.619 | 5, 6, 5, 4 | 7, 7, 5, 7 | 11 / 10; 19 / 17 |
| 23 | 2 328 / 1 950 | 12.391 / 12.391 | 7, 5, –, – | 7, 7, –, – | 13 / 11; 24 / 20 |
| 24 | 2 753 / 2 350 | 12.833 / 12.833 | 12, –, –, – | 13, –, –, – | 13 / 11; [23,24] / 20 |

Readings.  (1) The distance from the profile set of walks to that of bridges with one more bead is 3–6 units for
every `N` from 11 to 23 and does not grow: per bead it falls from 0.5 to 0.22.  With the gauche count the
distance is 5–9 units.  This is what Conjecture 5.2 predicts when exposing an end costs `O(1)` beads — which is
all that can happen at sizes where no end is buried deeper than one layer, so the test has little power against
the mechanism of §5.3.  (2) The covering numbers of bridges (clients and centres bridges) equal those of walks
two to three beads shorter.  (3) Extremes coincide (same `k_N` in the surface law).  (4) *Nestedness:* 96–99 % of the
classes of `N` are classes of `N+1` (`N ≥ 11`), 94–98 % with `gmin` larger by at most one.  (5) *Convexity of the
profile set:* 90–92 % of the lattice points of the convex hull of the classes are classes (`N = 20…27`), and no
hull point is farther than 3–9 units (0.14–0.35 per bead) from a class.  (6) *Convexity of the lower boundary is
not visible:* the largest gap between `gmin(h)` and the lower convex envelope of `{(h, gmin)}` is `3.5, 3.5, 4.6,
6.3, 6.1, 7.2` torsions for `N = 12, 15, …, 27` — a constant `0.25…0.30` per bead.  At these sizes a fold costs as
much as a stem; the convexity of `γ` is a statement about `N ≫ 27`.

### 5.5 Literature **[known]**

* Interacting self-avoiding walks and polygons with a contact energy `β`: the limiting free energy exists for
  polygons for all `β` and is convex; for walks it is proved to exist, and to equal that of polygons, only for
  `β ≤ 0` (repulsive); for `β > 0` "little else has been proved rigorously", and equality is a conjecture supported
  by series and Monte Carlo (Tesi, Janse van Rensburg, Orlandini, Whittington, J. Phys. A 29 (1996) 2451; their
  "contact theorem": equality follows if polygons have on average at least as many contacts as walks).  *Read:*
  the abstract of the 1996 paper through search summaries only; the statement above from pp. 2–4 of
  Bennett-Wood, Enting, Gaunt, Guttmann, Leask, Owczarek, Whittington, J. Phys. A 31 (1998) 4725
  (arXiv:cond-mat/9803359), which I read in full text.  The coordinator's recollection is correct.
* Later: existence of the connective constant for *weakly* self-attracting walks (Ueltschi 2002, infinite range;
  Hammond–Helmuth, arXiv:1712.07673, bounded range, "even without knowing whether submultiplicativity holds") —
  abstracts.  A 2018 review (Carmona, Nguyen, Pétrélis, Torri, arXiv:1802.08745) still describes the free energy
  of the undirected model as established only for small interaction — search summary.  I found no proof for
  strong attraction, and none for a two-parameter (contacts, stiffness) density.
* The two-parameter model is the *semi-flexible* interacting walk (Bastolla–Grassberger 1997; coil, globule and
  crystalline/frozen phases) — search summaries; physics, no existence theorems found.
* Our question is weaker than the free-energy question: it concerns the *support* of the joint density of
  `(h, g)` (ground states, no entropy), so non-injective maps from walks to bridges are allowed (Lemma 5.4), which
  unfolding arguments for the free energy cannot use.  Unfolding itself destroys the pairs between the unfolded
  pieces and does not help.
* Supermultiplicativity ⇒ limits and concave density functions: Janse van Rensburg, *The Statistical Mechanics of
  Interacting Walks, Polygons, Animals and Vesicles* (chapter on density functions; table of contents only) and
  arXiv:1603.08553 (abstract).  Theorem 3.4 is the set-valued version of this for bridges.
* Maximal contacts / compact walks: for the cubic and fcc lattices exact contact bounds are used in the HP model
  (Backofen and others) — search summaries; a diamond-lattice enumeration of the HP model exists
  (arXiv:1204.3438) — title only.  The surface term `N^{(d−1)/d}` of collapsed polymers: Owczarek, Prellberg, Brak,
  Phys. Rev. Lett. 70 (1993) 951 — through later papers that quote it.

---

## 6. G4 — from a limit shape to a limit of certificate sizes

### 6.1 The abstract lemma

Let `(V, ‖·‖)` be a finite-dimensional normed space, `L, e > 0`, `π : V×ℝ → V` the projection.  For a non-empty
compact `F ⊂ V × [0, G]` and `ε ∈ ℝ` let

    N(F, ε) := min{ |A| : A ⊂ π(F) finite,  ∀(p,g) ∈ F ∃a ∈ A :  L‖a − p‖ ≤ e·g + ε }  ∈ ℕ ∪ {∞}

(centres are *internal*: profiles of the set itself).  Hausdorff distances are taken for
`ρ((p,g),(p′,g′)) = max(‖p−p′‖, |g−g′|)`.  `F^↑ = {(p,t) : (p,g) ∈ F, g ≤ t ≤ G}`.

**Lemma 6.1 [proved].**
(a) *Only the lower boundary matters:* `N(F, ε) = N(F^↑, ε)`; `F^↑` is the truncated epigraph of
`γ_F(p) = min{g : (p,g) ∈ F}` over `π(F)`.
(b) *Two-sided stability, for every `ε`:* if `F, F′` are compact with `d_H(F, F′) ≤ η`, then

    N(F′, ε + (2L+e)η)  ≤  N(F, ε)  ≤  N(F′, ε − (2L+e)η) .

(c) `ε ↦ N(F, ε)` is non-increasing, finite for `ε > 0`, and right-continuous; hence it has at most countably many
discontinuities.
(d) *Limit:* if `F_N` are compact and `d_H(F_N^↑, F^↑) → 0`, then for every `ε`

    N(F, ε)  ≤  liminf_N N(F_N, ε)  ≤  limsup_N N(F_N, ε)  ≤  N(F, ε−) := lim_{ε′↑ε} N(F, ε′),

so `lim_N N(F_N, ε) = N(F, ε)` for every `ε` outside the (at most countable) set of discontinuities of `N(F,·)`;
more precisely `N(F_N, ε) = N(F, ε)` as soon as `N(F,·)` is constant on `[ε − (2L+e)d_N, ε + (2L+e)d_N]`,
`d_N = d_H(F_N^↑, F^↑)`.
(e) The exceptional set can be non-empty and the limit can fail there: `V = ℝ`, `F = {(0,0),(1,0)}`,
`F_N = {(0,0),(1+1/N,0)}`, `ε = L`: `N(F, L) = 1`, `N(F_N, L) = 2`.

*Proof.*  (a) `π(F^↑) = π(F)`, `F ⊂ F^↑`, and a centre that covers `(p,g)` covers `(p,t)` for `t ≥ g`.
(b) Let `A ⊂ π(F)` be optimal for `(F, ε)`.  For `a ∈ A` choose `(a,g_a) ∈ F` and a point `(a′,·) ∈ F′` within `η` of
it; `a′ ∈ π(F′)`, `‖a′−a‖ ≤ η`.  Given `(p′,g′) ∈ F′` choose `(p,g) ∈ F` within `η` and `a ∈ A` covering it:
`L‖a′−p′‖ ≤ L(η + ‖a−p‖ + η) ≤ 2Lη + e·g + ε ≤ e·g′ + ε + (2L+e)η`.  So the `a′` cover `F′` at `ε + (2L+e)η`.
Exchange `F` and `F′` for the other inequality.
(c) Monotone: clear.  Finite: `π(F)` is compact; a maximal `ε/L`-separated subset of `π(F)` is finite and covers.
Right-continuous: if `k` centres suffice for every `ε′ > ε`, take a limit of the `k`-tuples as `ε′ ↓ ε` (compactness
of `π(F)^k`); for a fixed client the covering centre has a constant index along a subsequence, and the closed
condition passes to the limit.  A monotone map into `ℕ ∪ {∞}` has countably many jumps.
(d) Apply (b) to `F_N^↑, F^↑` and use (a), (c).  (e) is a direct check. ∎

**Which convergence is needed.**  Not the Hausdorff convergence of the whole sets `𝒮_N/N` (all gauche counts), and
not the convergence of the *graphs* of the lower boundaries — which fails already when one profile has an
atypically small `γ_N` — but **Hausdorff convergence of the truncated epigraphs**: convergence of the profile sets
(the domains) together with epi-convergence of `γ_N/N`.  Convergence of the whole sets implies it.

### 6.2 Certificates

`N^P_cov(ε₁N)` for chains with `N` beads is `N(𝒟_N, ε₁)` in `V = ℝ³` with `‖·‖_c`, clients and centres all walks;
`N^{P,br}_cov` is the same problem with clients and centres restricted to bridges.

**Theorem 6.2 (bridges) [proved].**  With `(𝒦, γ)` of Theorem 3.4 and
`N_∞(ε₁) := N(K^{br}, ε₁) = min{|A| : A ⊂ 𝒦, ∀p ∈ 𝒦 ∃a ∈ A : L‖a−p‖_c ≤ eγ(p) + ε₁}`:

    N_∞(ε₁) ≤ liminf_N N^{P,br}_cov(ε₁N) ≤ limsup_N N^{P,br}_cov(ε₁N) ≤ N_∞(ε₁−)        for every ε₁ > 0,

with equality throughout for all `ε₁` outside an at most countable set; and for all `N` and `ε₁`,
`N_∞(ε₁ + (2L+e)d_N) ≤ N^{P,br}_cov(ε₁N) ≤ N_∞(ε₁ − (2L+e)d_N)`, `d_N = d_H(𝒟_N^{br}, K^{br}) → 0`.
(Theorem 3.4 and Lemma 6.1.)  This is exactly the statement of question 2 of ENG-REQ-0001, for bridges.

**Rings [sketch]:** the same with `K^{ring}`, given §3.4.

**Corollary 6.3 (all walks, conditional) [proved from Conjecture 5.2′].**  If `𝒟_N^↑ → (K^{br})^↑`, then
`lim_N N^P_cov(ε₁N) = N_∞(ε₁)` off a countable set of `ε₁`, with the two-sided inequalities of Theorem 6.2.

**Proposition 6.4 (all walks, unconditional) [proved].**
(a) Every subsequence of `(𝒟_N^↑)` has a further subsequence that converges to a compact set `F*` with
`(K^{br})^↑ ⊂ F* ⊂ 𝒦₂ × [0,1]`, and along it `N^P_cov(ε₁N) → N(F*, ε₁)` off a countable set.  So the limit points of
the certificate sizes are covering numbers of such `F*`; the conjecture says `F*` is unique.
(b) *Lower bound.*  If `(p_i, g_i) ∈ K^{br}`, `i = 1…k`, satisfy `L‖p_i − p_j‖_c > e(g_i + g_j) + 2ε₁` pairwise, then
`liminf_N N^P_cov(ε₁N) ≥ k` (and the same for bridges).
(c) *Upper bound.*  For every `N`, `N^P_cov(ε₁N)` is at most the largest number of points of `𝒟_N`'s profile set with
pairwise `‖·‖_c`-distance `> ε₁/L`; hence `N^P_cov(ε₁N) ≤ vol(u(𝒦₁^{(N)}) + B₁(ε₁/2L)) / vol B₁(ε₁/2L)`, where `B₁` is the `ℓ¹` ball in `u`-coordinates and
`𝒦₁^{(N)}` is `𝒦₁` with every facet moved out by `(4M + c₃ + 2c₈)/N`; and `limsup_N N^P_cov(ε₁N)` is at most the same
expression with `𝒦₂` (Theorem 4.2′).

*Proof.*  (a) Blaschke selection in the compact box, Fact 5.1, Lemma 6.1(d).  (b) No centre covers two of the
clients (triangle inequality), the condition is open, and for large `N` there are walks within any `δ` of each
`(p_i, g_i)`; their classes have `γ_N/N ≤ g_i + δ`.  (c) A maximal `ε₁/L`-separated set of profiles is an internal
`ε₁/L`-net, and `e·γ ≥ 0`; balls of radius `ε₁/2L` around a separated set are disjoint; Theorems 4.2 and 4.2′ (the profile sets are within
`o(1)` of `𝒦₂`, and the volume of the enlarged polytope is continuous in the enlargement). ∎

---

## 7. G5 — numbers one can compute now

Throughout `e = 1`, `r := ε₁/L` (radius of a ball in `‖·‖_c` when the gauche credit is ignored), `B₁(ρ)` the `ℓ¹` ball
in `u`-coordinates, `vol B₁(ρ) = 4ρ³/3`.

### 7.1 (a) Chain-length-independent upper bounds

**Proposition 7.1 [proved].**  For every chain length `N`

    N^P_cov(ε₁N)  ≤  #(largest r-separated set of profiles)  ≤  vol(X + B₁(r/2)) / vol B₁(r/2)

for every convex set `X` that contains `u(h/N)` for all walks with `N` beads: (i) the image of the bulk box (all `N`);
(ii) the polytope `𝒦₁^{(N)}` of Theorem 4.2 (facets moved out by `(4M + c₃ + 2c₈)/N`).  On a lattice with `D` distances
below the cutoff the same argument gives `N^P_cov(ε₁N) ≤ D!·Π_k (W_k + r)/r^D`, `W_k` = cell width × largest
cumulative count per bead in cell `k`.  (Proposition 6.4(c); the Minkowski sum of a polytope and an `ℓ¹` ball is the
hull of the vertex sums, computed in `code/g5_bounds.py`, `code/g5_finiteN.py`.)

| `(L, ε₁)` | measured, 27 beads | Prop. 11.49(a) (`z = 24`) | theory report's volume bound `G ln(1+2zLS_c/ε₁)`, `G = 3` | bulk box, all `N` **[proved]** | `𝒦₁`, `N ≥ 100` **[proved]** | `𝒦₁`, `N ≥ 1000` **[proved]** | `𝒦₁`, `N → ∞` | `𝒦₂`, `N → ∞` (limsup) **[proved]** |
|---|---|---|---|---|---|---|---|---|
| `(1, ½)` | 15 | `10^{1387}` | `1.5·10⁹` | 26 437 | 4 673 | 3 809 | 3 719 | **3 627** |
| `(1, ¼)` | 28–31 | `10^{2774}` | `1.2·10¹⁰` | 191 833 | 30 526 | 24 555 | 23 936 | **23 272** |
| `(⅕, ½)` | 2 | `10^{277}` | `1.2·10⁷` | 392 | 111 | 96 | 94 | **93** |
| `(⅕, ¼)` | 3 | `10^{555}` | `9.9·10⁷` | 2 195 | 488 | 409 | 401 | **393** |

(A lattice of octahedra — the body-centred cubic lattice has `ℓ¹` covering radius ¾ of its cube edge — gives the
same numbers within 10 %: 4 086, 26 558, 98, 432 for `𝒦₁`; 3 984, 25 792, 96, 424 for `𝒦₂`.)  These bounds ignore the gauche credit and pay a factor
`2³` for internal centres (balls of radius `r/2`); without that factor the volume count for `𝒦₂` would be
`46.9/(4r³/3)·1.125 ≈ 320` at `r = ½`.  They are 47 to 800 times above the measured values and `10^{275}` to
`10^{2770}` times below Proposition 11.49(a).

### 7.2 (b) Inner approximations and lower bounds

*Exact densities of explicit periodic conformations:* the tables of §4.2 (rod `(0,0,0;0)`; one row of stems /
stacked hairpins `(½,2,3/2;0)`; lamellar crystal `(1,5,6;0)`, also realised by all-gauche `4₁` helices with `g = 1`;
checkerboard `(0,1,3;0)`; woodpile `(0,3,4;0)`; crossed rods `(½,4,9/2;0)`; gauche-rich packings up to
`(0,12/5,22/5; 4/5)`).

**Proposition 7.2 (lower bounds for the limit) [proved].**  For all walks (and for bridges)

    liminf_N N^P_cov(ε₁N)  ≥  max #{points of T₀ with pairwise ‖·‖_c-distance > 2r},

and explicit packings (greedy on a grid, verified pairwise; `code/g5_bounds.py`) give the middle column:

| `(L, ε₁)` | on the segment rod–crystal (length 35) | in `T₀` **[proved]** | in the hull of the nine rod vertices of §4.2 [sketch: needs Prop. 4.4] | measured, 27 beads |
|---|---|---|---|---|
| `(1, ½)` | 35 | **50** | 130 | 15 |
| `(1, ¼)` | 70 | **157** | 749 | 28–31 |
| `(⅕, ½)` | 7 | **7** | 8 | 2 |
| `(⅕, ¼)` | 14 | **14** | 18 | 3 |

(Proposition 6.4(b) with `g_i = 0`, Proposition 4.3.)  So the plateau is at least 3.3, 5, 3.5 and 4.7 times the
values measured at 27 beads.

**Proposition 7.3 (lower bounds at a given chain length, from explicit walks) [proved; exact counts from
coordinates].**  For each `N` below, `code/finite_packing.py` constructs lamellae `Λ(M,Q,ℓ)` prolonged by an all-trans
tail to exactly `N` beads, computes their exact `(h, g)`, and extracts walks with
`L‖h_i − h_j‖_c > g_i + g_j + 2ε₁N` pairwise; no evaluation covers two of them, so:

| `N` | 27 | 60 | 120 | 250 | 500 | 1 000 | 2 000 | 5 000 | `∞` (Prop. 7.2) |
|---|---|---|---|---|---|---|---|---|---|
| `N^P_cov(N/2)`, `L = 1`, at least | 3 | 6 | 10 | 17 | 22 | 26 | 31 | 35 | 50 |
| `N^P_cov(N/4)`, `L = 1`, at least | 4 | 11 | 19 | 31 | 43 | 53 | 64 | 77 | 157 |
| `N^P_cov(N/2)`, `L = ⅕`, at least | 1 | 2 | 3 | 4 | 5 | 5 | 6 | 6 | 7 |
| `N^P_cov(N/4)`, `L = ⅕`, at least | 2 | 3 | 5 | 6 | 8 | 9 | 10 | 12 | 14 |

(The family is one two-parameter family of crystals; at `N = 27` it gives 3 where the truth is 15.)  **The growth
seen up to 27 beads provably continues:** at 500 beads at least 22 and 43 evaluations are needed where 15 and
28–31 suffice at 27 beads, at 5 000 beads at least 35 and 77.

**Bracket for the plateau** (`N_∞` here stands for any limit point of `N^P_cov(ε₁N)`, walks or bridges; Proposition 6.4).

| `(L, ε₁)` | measured at 27 beads | `N_∞`: proved bracket | covering number of the inner model (`K ≤ 12` chain systems with their `γ`): packing … greedy cover [numerical estimate] |
|---|---|---|---|
| `(1, ½)` | 15 | `50 ≤ N_∞ ≤ 3 627` | 155 … 341 |
| `(1, ¼)` | 28–31 | `157 ≤ N_∞ ≤ 23 272` | 900 … 1 300 |
| `(⅕, ½)` | 2 | `7 ≤ N_∞ ≤ 93` | 6 … 9 |
| `(⅕, ¼)` | 3 | `14 ≤ N_∞ ≤ 393` | 19 … 35 |

(`code/g5_estimate.py`: the inner model is the hull of §4.2 with `γ` the lower envelope of the four-dimensional hull;
"packing" and "greedy cover" bracket the covering number of *that model* on a grid of step `r/3.2`; the true
`𝒦` is larger, the true `γ` smaller, both raising the numbers a little.  For `(1,¼)` the packing was computed on a
finer grid than the cover.)  My best estimate: **`N_∞ ≈ 150–350` for `(1, ½)`, of the order of `10³` for `(1, ¼)`,
`7–10` for `(⅕, ½)`, `20–35` for `(⅕, ¼)`** — ten to forty times the values at 27 beads for `L = 1`, three to ten times
for `L = ⅕`.  The other division's prediction "tens or hundreds" is confirmed: hundreds.

**At what chain length?**  Three effects, all `∝ N^{−1/3}`: (i) the extent, `35(1 − 1.8N^{−1/3})` (§4.4): 80 % at
`N ≈ 730`, 90 % at `N ≈ 5 800`; (ii) the gauche credit at the compact end, `g/N ≈ 1.9·N^{−1/3}` for lamellae (it is
`0.52` at 27 beads in the exact data, `0.06` at 31 880 beads), which enlarges the radii until `1.9N^{−1/3} ≪ ε₁`,
i.e. `N ≫ 55` for 100 % and `N ≈ 5·10⁴` for 10 % of `ε₁ = ½`; (iii) the thickness of the body.  With Proposition 7.3:
half of the proved plateau is reached at `N ≈ 10³`, 70 % at `N ≈ 5·10³`.  **Chain lengths of `10³`–`10⁵` beads**; no
enumeration reaches them.

### 7.3 (c) The off-lattice chain: why the growth is geometric

*What differs.*  On the lattice the profile is a point of `ℤ³`: the normalised profile set lives in three
dimensions for every `N`, a ball of radius `ε₁/L` occupies a fixed fraction of it, and the covering number is
bounded by a volume ratio (§7.1) and grows only because the set expands (§4.4).  Off-lattice the profile is a
non-decreasing function on `[0, S_c)`; the measured rank of the profile set is 51, 140, 226 at `n = 8, 10, 12`
(P_REPORT §3.5).  At resolution `r = ε₁/L` per bead a step of height `μ` (pairs per bead) can be told from the same
step shifted by `w` only if `μw ≳ r`, so the number of resolvable degrees of freedom is

    D_res ≈ (S_c − s_core)·M / r,        M = pairs per bead inside the cutoff,

and the classical entropy of monotone functions gives `ln N_∞ ≍ c·D_res` (`c ≤ 2 ln 2` by the grid construction of
P_REPORT §2.4; `c ≳ 0.1` for the full class of monotone functions; for chains `c` is unknown).  The plateau
exists — Proposition 11.49(a) — but it is exponential in `L·S_c·M/ε₁`, where on the lattice it is a polynomial of
degree 3 in `L/ε₁`.  **Geometric growth is what a set does while its effective dimension still grows linearly with
the chain length**: `ln N^P_cov ≈ c·D_res(N)` with `M = M_N` increasing (1.3 → 5.7 pairs per bead from 8 to 16 beads).

*When must it stop?*  **[proved, vacuous]**: beads whose indices differ by a multiple of 3 are pairwise at
distance `≥ √3`, so a bead has at most `3·(4 + √3/2)³/(√3/2)³ = 531` beads within the cutoff, `z ≤ 531`; Proposition
11.49(a) gives `ln N^P_cov(ε₁N) ≤ ln 4·⌈4·531·16·L/ε₁⌉ = 9.4·10⁴` (`L = 1`, `ε₁ = ½`) and `1.9·10⁴` (`L = ⅕`).  A growth
by a factor `≥ 1.3` per torsion from the measured value at `n = 12` must therefore stop before `n ≈ 3.6·10⁵`
(`L = 1`).  **[estimate, with assumptions]**: (A1) bulk coordination: stems of diameter `√3` with beads `0.82` apart
along the axis, hexagonally packed, give `0.47` beads per unit volume and `M ≈ 63` pairs per bead inside the
cutoff; (A2) `s_core = 3`; (A3) `c ∈ [0.03, 1]`, the lower value from the measured slope
(`d ln N_cov/dN ≈ 0.37` per bead while `M_N` grows by `≈ 0.5` per bead at `L = 1`, `ε₁ = ½`, i.e.
`ln N_cov ≈ 0.03·D_res(N)`).  Then `D_res ≈ 1 640` for `(1, ½)` and `330` for `(⅕, ½)`:

| | `ln N_∞` (A1–A3) | chain length at which the growth must have stopped: at the observed rate | at the largest possible rate (`≤ 2.41` per torsion, the growth of the number of conformations) |
|---|---|---|---|
| `L = 1`, `ε₁ = ½` | 50 … 1 600 | `n ≈ 130 … 4 400` (rate 1.45) | `n ≥ 55 … 1 800` |
| `L = ⅕`, `ε₁ = ½` | 10 … 330 | `n ≈ 60 … 3 000` (rate 1.1–1.2) | `n ≥ 11 … 370` |

and in any case not before the profile set has expanded (`M_N → M`: surface law, `N ≳ 10³`).  So for `L = 1` the
off-lattice plateau is `e^{50}` or more and is reached at chain lengths of hundreds to thousands of torsions; for
`L = ⅕` it may be as low as `10⁴`–`10⁵` evaluations at a few hundred torsions.

*Can the rate per torsion be predicted?*  Not from the theory as it stands.  What is true: (i) the rate is at most
the growth rate of the number of profile classes (2.14 per torsion measured, `≤ 2.41`); (ii) it is that rate
divided by the growth rate `e^{σ}` of the number of classes inside one slack ball, where
`σ(ρ) = lim n⁻¹ ln #{classes within profile distance ρN of a typical class}` — a large-deviation function of the
*distance distribution* that can be measured from the stored class tables (all pairwise distances exist for
`n ≤ 12`).  The measured rates (1.61 at `ε = 0`, 1.46 at `N/4`, 1.45 at `N/2` for `L = 1`; 1.23 and 1.10 for `L = ⅕`)
say `σ ≈ ln(2.14/1.45) = 0.39` at `L = 1` almost independently of `ε₁`, and `σ ≈ 0.6` at `L = ⅕`; a prediction
is the statement that `σ` measured at `n ≤ 12` extrapolates.  (iii) The rate must decrease with `N` — the entropy at
fixed relative resolution is bounded — so the second difference of `ln N^P_cov` in `n` must become negative; with
brackets as wide as `[109, 136]` at `n = 12` this is not yet decidable.  I did not compute `σ` (no off-lattice code
of my own).

---

## 8. G6 — the two smaller questions

### 8.1 Question 3: the rate

* **The shape converges with a surface correction of exact order `N^{−1/3}` at its compact end [proved]**
  (Corollary 4.6): `17.6·N^{−1/3} − 17/N ≤ d_H(𝒟_N^{br}, K^{br})`, the lamellae achieve `O(N^{−1/3})` there, and the
  exact data for `N ≤ 27` follow `max‖N^x‖₁/N = 35(1 − k_N N^{−1/3})` with `k_N = 1.8 ± 0.06` **[numerical]**.  The
  deviation is one-sided: finite sets stay inside the limit up to `168/(N+3)` **[proved, bridges]**.  Away from the
  compact end the rate depends on the structure: the rod vertex is exact for every `N`; one row of stems
  (`(½,2,3/2)`) is reached at rate `N^{−1/2}` (`M ≈ ℓ ≈ √(N/2)`: two free dimensions); every point that needs a
  three-dimensional crystal — in particular the whole upper part of `𝒦` — at rate `N^{−1/3}`.  That
  `d_H = O(N^{−1/3})` for the whole body is **[conjecture]** (it would follow from Proposition 4.4 with uniform
  constants and a description of the extreme points).
* **The formula in the question needs rewording.**  `N_∞(ε₁) − N^P_cov(ε₁N)` is an integer; for non-exceptional `ε₁`
  it is eventually zero (given Conjecture 5.2′).  The correct statement is Lemma 6.1(b):

      N_∞(ε₁ + 3d_N)  ≤  N^P_cov(ε₁N)  ≤  N_∞(ε₁ − 3d_N)        (L = e = 1),    d_N ≥ 17.6·N^{−1/3} − 17/N,

  i.e. *the covering number at chain length `N` is the limiting covering number at an accuracy shifted by a
  surface term*; and since the deviation is one-sided (the finite set is roughly a shrunken copy of the limit), one
  expects the finite-`N` number to be below the limit, as observed (not a theorem: covering numbers with internal
  centres are not monotone under inclusion).  Because `N_∞(ε₁) ≍ ε₁^{−3}·vol` for small `ε₁` and `≍ ε₁^{−1}`
  for large `ε₁` (thin body), a shift of `ε₁` by a fraction `θ` changes `N_∞` by a factor between `(1+θ)` and
  `(1+θ)³`; with `d_N ≈ 63·N^{−1/3}` in the worst direction (`35·1.8`), `3d_N < 0.1·ε₁` needs `N ≈ (1900/ε₁)³` —
  the guaranteed convergence is hopeless, the effective one is governed by `1.8N^{−1/3}` relative to 1 (§7.2).
* **What it implies for enumeration.**  Yes: enumeration cannot see the limit.  At 27 beads the profile set has
  39 % of its bulk extent and a tenth of its limiting volume; each further bead adds about 1 % of extent
  (`d/dN [1.8N^{−1/3}] = 0.007` at `N = 27`); 50 % of the extent needs 47 beads (`≈ 10²⁰` conformations).  The
  right computational objects are `(𝒦, γ)` (extreme points = ground states of three-shell lattice gases with a
  stiffness term) and constructed conformations at `N = 10²…10⁴` (Proposition 7.3).

### 8.2 Question 4: which property of the single-flip constants the lower bounds use

**Reading of the two theorems.**  Theorem 11.37 (= Theorem G3 of `G_REPORT.md` §2.3) assumes a product domain
`[k]ⁿ`, an additive known part, the envelope `Σ c_i[x_i ≠ y_i]`, and **`c_i ≥ c₀ m_i^γ`** with at most two sites per
value of `m_i`.  Its proof uses the constants in exactly one place: the denominator of the partition bound
(Theorem 11.6(c)) is `Π_i(1 + (k−1)e^{−tc_i}) ≤ exp((k−1)Σ_i e^{−tc_i})`, and `Σ_i e^{−tc_i} ≤ 2Σ_{m≥1} e^{−tc₀m^γ}`.
This is monotone in each `c_i`: **only lower bounds on the constants enter**, through the single number
`Σ_i e^{−tc_i}`.  No upper bound, no asymptotic law, no regularity of `j ↦ c_j` is used; with exact constants one
can simply evaluate `max_t [ln Z_X(t) − tε − (k−1)Σ_i e^{−tc_i}]`.  Theorem 6(c) of `P_REPORT.md` supplies the lower
bound for *every* valid envelope: `c_i ≥ L·c_i^{sf}` (the two conformations of a single flip must be separated by
at least their profile distance).  So the statement needed is

    c_j^{sf}  ≥  κ·d_j    for all j and all n, with one κ > 0,

the *lower* half of the "two-sided linear bounds" of ENG-RES-0002; the upper half and an asymptotically linear
law `c_j ~ κd_j` are not needed.  `κ` does not affect the leading term `n ln k` of the exponent, only the deficit
`C_{k,1}((G+ε)/(Lκ))^{1/2}`.  (For the *upper* bound `N_cov ≤ k^{n − n_sharp}` of the same theorem upper bounds on the
constants would be needed, but only at the `O(1)` sharp sites near the ends.)

Two caveats that are not about the constants: (i) the numerator.  On the self-avoiding domain `X` the bound reads
`ln N_cov ≥ ln Σ_{y∈X} e^{−t·gap(y)} − tε − (k−1)Σ_i e^{−tc_i}` (the denominator only decreases when `y` is restricted
to `X`); with "every trans/gauche pattern is realised" (ENG-RES-0002 §5) the numerator is `≥ (1+e^{−te})ⁿ`, with the
count of conformations `≈ μⁿ`, `μ ≈ 2.88`.  So on the self-avoiding chain the same optimisation over `t` gives growth `μ^{n−O(√n)}`,
`2 < μ < 3`, not `3^{n−O(√n)}` **[sketch]**.  (ii) The measured instances are already in the regime "every conformation is
needed" (R_P review, m1), where the statement is trivially true.

**The lower bound is a theorem; the two-sided bounds hold; the linear law is false.**

*Proposition 8.1 [proved; the finite part by computation].*  For the self-avoiding diamond chain with `S_c = 12`
and every torsion `j` with `d_j = min(j, n+1−j) ≥ 5`:   `14·d_j − 15 ≤ c_j^{sf} ≤ 70·(d_j + 3)`.

*Proof.*  Lower bound: the hairpin `t^a g⁺g⁻g⁺ t^b` (two adjacent stems joined by a rung; the fold word is read off
`Λ(3,1,·)`) and the conformation in which the middle fold torsion is set to trans.  Both are self-avoiding, the
flipped one consists of two straight rods leaving the hinge in different directions, so it has `O(1)` pairs
inside the cutoff, while the hairpin has `(1,4,3)` pairs per period of overlap (type-1 rods, §4.2), i.e. profile
norm 28 per two beads of the shorter arm.  Lengthening both arms by one period changes the two profiles by
exactly `(1,4,3)` and `0` once the arms are longer than the range of the hinge; `code/g6_flip_all.py` computes the
distance from coordinates for all `3 ≤ a, b ≤ 30` (784 hairpins): `−15 ≤ D − 14d ≤ −5`, with `D(a+2,b+2) = D(a,b)+28`
and `D(a,b+2) = D(a,b)` (`b ≥ a+6`) without exception for `a, b ≥ 5`; `code/g6_flip.py` goes to `a = b = 43` (`n = 89`).  Upper bound: a flip of torsion `j` moves one arm
rigidly; choose the shorter, with at most `d_j + 2` beads.  Only pairs (moved bead, fixed bead) change.  A moved
bead has two chain neighbours on its own side (all but one), hence at most 2, 10 and 12 partners of the other
side at squared distances 3, 8, 11, so each cumulative count changes by at most `2, 12, 24` per moved bead:
`‖Δ‖_c ≤ (5·2 + 3·12 + 24)(d_j + 3) = 70(d_j+3)`. ∎

The measured constants (`58, 108, 124, 141, 160, 170, 169, 170` for `d = 1…8` at `n = 16`) lie between the two.
*Why there is no linear law:* the arm of `d` beads can be surrounded by as many stems of the *other* arm as that
arm can supply — one if `d ≈ n/2` (hairpin: `14d`), up to eight if `d ≤ n/9` (`70d`: every bead of the moved stem
loses 2 + 10 + 12 partners).  So the natural scaling form is

    c_j^{sf} ≈ n·Φ(d_j/n),      Φ concave,  Φ(δ) ≈ 70δ for small δ,  Φ(½) ≥ 7     [conjecture],

a large first step, a slope that decreases from the ends to the centre, and a plateau at the centre — the shape
reported in ENG-RES-0002 §6.  `c_j/d_j` at `n = 16`: `58, 54, 41, 35, 32, 28, 24, 21`, decreasing as predicted.
An "asymptotically linear law" holds only at fixed `d/n`.

---

## 9. Draft answers to the four questions of ENG-REQ-0001

**Question 1 (limit shape).**  *Proved for bridges; conjectured for all walks; the corresponding free-energy
question is open in the literature, but this one is weaker.*
For bridges (first bead strictly lowest, last bead highest along a coordinate axis) the sets
`{(h, #gauche)/N}` converge in the Hausdorff metric to a compact convex `K^{br} ⊂ ℝ⁴`; so there are a compact convex
`𝒦 ⊂ ℝ³` and a convex `γ : 𝒦 → [0,1]` such that the truncated epigraphs of `γ_N/N` over the profile sets converge to
the epigraph of `γ` over `𝒦` (Theorem 3.4; the concatenation needs three linker beads and costs at most
`(1, 9, 14)` pairs and one gauche torsion).  For all walks: `K^{br} ⊂ liminf`, every limit point of the profile
densities lies in an explicit polytope `𝒦₂` (volume 10.4 % of the bulk box; twelve inequalities, exact
certificates), the gauche density is at least `2p₁₁ − 5p₃ − 8`, and walks and bridges have the same support function in the directions that belong to the three
proved vertices (rod, one row of stems, crystal) — about two thirds of all directions; equality of the limits
is Conjecture 5.2.  It is equivalent to "walks and bridges have the same ground-state energy per bead for every
three-shell pair energy with a stiffness term" (Lemma 5.3) and to "every walk has the `(h,g)` of `o(N)` bridges"
(Lemma 5.4); a surgery that changes `o(N)` *sites* is impossible (Proposition 5.5).  Known theory: for the
free energy of interacting walks existence is proved for polygons, and for walks only for repulsion and weak
attraction; the buried end is exactly the obstacle there.  The limit object is not the whole bulk box: it is a
thin body (`2.2 ≲ vol ≤ 3.125` of 30), with `γ = 0` on the part reached by folded all-trans stems (lamellae; at
least the triangle rod–row–crystal, proved) and `γ > 0` on the part rich in third-neighbour pairs (proved:
`γ ≥ 0.22` at an explicit point; `4/5` at `(0,12/5,22/5)`, where bound and construction agree).

**Question 2 (limit of certificate sizes).**  *Proved for bridges; for all walks conditional on Conjecture 5.2′,
with unconditional two-sided bounds.*  Lemma 6.1: if the truncated epigraphs converge, then
`N(F, ε₁) ≤ liminf ≤ limsup ≤ N(F, ε₁−)` for every `ε₁`, with equality off the countable set of jumps of `N(F,·)`, and
for every `N` and `ε₁` the two-sided inequality with slack `(2L+e)·d_H`.  For bridges this gives
`lim N^{P,br}_cov(ε₁N) = N_∞(ε₁)`, the covering number of `𝒦` with radii `eγ(p)+ε₁` and internal centres, exactly as
written in the request.  For all walks, unconditionally: `50 ≤ liminf` and `limsup ≤ 3 627` at `(L, ε₁) = (1, ½)`
(`157 … 23 272` at `(1,¼)`, `7 … 93` at `(⅕,½)`, `14 … 393` at `(⅕,¼)`), every limit point is the covering number of a
limit set between `K^{br}` and `𝒦₂×[0,1]`, and Proposition 11.49(a) (`10^{1387}`) is replaced by these numbers.  Best
estimate of the plateau: 150–350, `≈ 10³`, 7–10, 20–35.  One correction: the norm is the `L¹` norm of *cumulative*
counts, `5|Δh₃| + 3|Δh₃+Δh₈| + |Δh₃+Δh₈+Δh₁₁|`, not `9|Δh₃|+4|Δh₈|+|Δh₁₁|` (§1).

**Question 3 (rate).**  *Yes for the shape, with proof at the compact end; the formula for the covering numbers
must be reworded.*  `d_H ≥ 17.6·N^{−1/3}` (isoperimetric inequality) and the crystal is approached at that rate by
lamellae; the exact data follow `max‖N^x‖₁/N = 35(1 − 1.8N^{−1/3})` for all `N` from 8 to 27.  Finite sets stay inside
the limit up to `O(1/N)`.  `N^P_cov(ε₁N)` equals `N_∞` at an accuracy shifted by `(2L+e)d_N`; it is integer-valued, so
"`N_∞ − N_cov = Θ(N^{−1/3})`" is not the right form.  Consequence as anticipated: enumeration cannot see the limit
(39 % of the extent at 27 beads, 50 % at 47, 90 % at about 5 800); explicit walks show that at least 17, 26, 35
evaluations are needed at 250, 1 000, 5 000 beads (`L = 1`, `ε = N/2`).

**Question 4 (single-flip constants).**  *The one-sided linear lower bound, and it is now a theorem.*  The lower
bounds (Theorem 11.37 with Theorem 6(c)) use the constants only through `Σ_j e^{−tLc_j}`, which is monotone: they
need `c_j^{sf} ≥ κd_j` and nothing else.  Proposition 8.1: `14d_j − 15 ≤ c_j^{sf} ≤ 70(d_j+3)` for all `n` (hairpin; one
bead has at most 2, 10, 12 foreign partners).  An asymptotically linear law is neither needed nor true: the
expected form is `c_j ≈ nΦ(d_j/n)` with `Φ` concave.  What the extension to self-avoiding chains needs besides is
the numerator `Σ_{y∈X}e^{−t·gap(y)}`, i.e. the count of conformations (`μⁿ`, `μ ≈ 2.88`, in place of `3ⁿ`).

**Which finite-size quantities to compute next, and why.**

1. *Ground states instead of enumeration.*  For the seven unattained vertices of the outer polytopes
   (`(0,0,2)`, `(0,1,4)`, `(0,2,2)`, `(0,2,9/2)`, `(0,3,9/2)`, `(½,2,3)`, `(½,7/2,7/2)`) maximise `c·h` over
   conformations of `10²…10³` beads (annealing with end-moves and backbites) and over periodic chain systems
   with cell index 13–16 (`code/pchain.c` is exhaustive to 12 in 12 core-minutes; 13–14 need `10¹⁰`–`10¹¹`
   systems).  Each vertex is either attained (then it is settled) or not (then the outer bound must be improved).
   This closes the gap `2.22 … 3.125` in `vol 𝒦`, which is the main uncertainty of `N_∞`.
2. *A second-level linear programme* (two-shell cluster of 17 sites, or the six-ring), with exact dual
   certificates as in `code/lp_exact.py` / `code/lp4_exact.py` — the one-bond cluster leaves seven vertices open.
3. *The surface law* `35(1 − kN^{−1/3})`, `k ≈ 1.8`: extend `max ‖N^x‖₁/N` and `min{g : ‖N^x‖₁ ≥ (1−θ)·max}` to
   `N = 10³` by constructed conformations; it fixes the chain-length scale of the plateau.
4. *Bridges against walks*: class tables of bridges for `N = 25…27` (I have `N ≤ 24`), and — more informative —
   the one-sided distance between the best constructed walks and the best constructed bridges at `N = 10²…10³`,
   where ends can be buried; a persistent gap `≫ N^{2/3}` in some direction would refute Conjecture 5.2.
5. *Lower bounds at given `N`* by packings among constructed conformations (Proposition 7.3 uses one family;
   annealed sets will do better), and the covering number of the limit model itself by an exact set cover on a
   fine grid of `(𝒦, γ)` — my estimates (155 … 341 at `(1,½)`) come from a greedy cover.
6. *Single flips*: the scaling plot `c_j/n` against `d_j/n` for `n = 8…16` (collapse onto a concave `Φ`), and the
   check `c_j ≥ 14d_j − 15`.
7. *Off-lattice*: the distance-entropy function `σ(ρ)` of §7.3 from the stored tables (`n ≤ 12`), and the pairs
   per bead `M_N` — the two inputs of a growth-rate prediction.
8. Replace "weighted `ℓ¹` norm `9, 4, 1`" by the cumulative norm in the request and the brief.

---

## 10. Prior-art log

Search tool, generic queries only; what I could read is stated per item.

| # | query (abridged) | what I read | used for |
|---|---|---|---|
| 1 | Tesi, Janse van Rensburg, Orlandini, Whittington, "Interacting self-avoiding walks and polygons in three dimensions", limiting free energy | search summary of the abstract (J. Phys. A 29 (1996) 2451–2463): walks and polygons have the same limiting free energy for repulsive interactions | §5.5 |
| 2 | existence of limiting free energy, interacting SAW, attractive regime, walks versus polygons | **full text, pp. 1–4** of Bennett-Wood et al., arXiv:cond-mat/9803359 (J. Phys. A 31 (1998) 4725): `κ, κ°, κ_f` exist and are equal for `β ≤ 0` (Tesi et al., `d = 3`); for `β > 0` existence proved for polygons, "otherwise, little else has been proved rigorously"; conjecture (1.7); the contact theorem | §5.5; confirms the coordinator's recollection |
| 3 | Hammond, Helmuth, "Self-attracting self-avoiding walk" | arXiv:1712.07673 abstract (search summary): connective constant exists for weak self-attraction; Ueltschi 2002 for infinite range | §5.5 |
| 4 | same query as 2 | search summary of Carmona, Nguyen, Pétrélis, Torri, arXiv:1802.08745 (review): free energy of the undirected model established for small interaction only | §5.5 |
| 5 | Janse van Rensburg, density functions, supermultiplicative | arXiv:1603.08553 (abstract page): a two-variable supermultiplicative inequality implies a limit generalising Fekete's lemma; table of contents of the 2nd edition of his book (chapter "Density functions and free energies") | §3.3 remark; Theorem 3.4 is the set version |
| 6 | Owczarek, Prellberg, Brak, collapsed polymer, surface free energy `N^{(d−1)/d}` | search summaries of later papers quoting PRL 70 (1993) 951 (`Z ~ a^N b^{−N^{(d−1)/d}} N^{γ−1}`) | §4.4, §8.1 (the surface term is expected; here it is proved for the support) |
| 7 | maximum number of contacts of a self-avoiding walk, compact conformations, isoperimetric | search summaries (Backofen: layer bounds for cubic and fcc lattices in the HP model; arXiv:1204.3438, diamond-lattice HP enumeration — title) | §4.4: I did not find the diamond-lattice bound of Proposition 4.5 |
| 8 | ground states of lattice gases, cluster method, configuration polytope, Kanamori | search summaries: Kaburagi–Kanamori (1975, 1978), "method of geometric inequalities" / configurational polytope; Huang et al., arXiv:1606.07429 ("basic polytope method" = LP over cluster probabilities with compatibility equations, lower bounds for ground-state energies) | §4.1: Theorem 4.2 is this method applied to the three-shell lattice gas of Lemma 2.1; the application to chain profiles I did not find |
| 9 | Hamiltonian walks, compact polymers, diamond lattice, chain folding | search summaries (Jacobsen 2007 enumeration on square/cubic lattices; nothing for the diamond lattice or lamellae) | §4.2 |
| 10 | semiflexible interacting self-avoiding walk, stiffness and contacts, rigorous | search summaries (Bastolla–Grassberger 1997; Krawczyk–Owczarek–Prellberg; Bedini et al.): phase diagrams, no existence theorems | §5.5 |

Not found in print (after these searches; none is deep): the site-set reduction used as an LP relaxation for
profile sets; the eleven inequalities; the limit-shape statement for `(h, g)` of diamond-lattice bridges; the
stability lemma 6.1 for covering numbers with position-dependent radii (it is elementary); Proposition 8.1.

## 11. What I did not check

* **Conjecture 5.2 is open.**  Nothing is proved for walks beyond Fact 5.1, Theorem 4.2 and §5.2(a); the enumeration
  evidence (`N ≤ 24`) has no power against deeply buried ends.
* **Proposition 4.4 is a sketch.**  The inner hull of volume `2.2234` (and the rod hull `1.8333`, the vertices
  `(0,3,4)`, `(½,4,9/2)`, the values `γ = 4/5`, `5/7` as *attained*) rests on it; what is proved is `T₀` and the finite
  bridges of `out/build.txt` up to `168/(N+3)`.  The greedy builder may fail for other structures; it was run on nine.
* **The inner hull has not converged** in the cell index (`+4 %` from 11 to 12); `vol 𝒦`, the vertex list and the
  region `γ > 0` are lower estimates.  No stochastic search at large cells was done.
* **Linear programmes.**  The facets of `𝒦₁`, `𝒦₂` and the three gauche inequalities are certified in exact
  arithmetic; the *derivation* of the constraints (symmetrisation, star relations) is a paper argument checked
  against data (20 075 periodic sets, 5 680 chain systems, 9 188 bridges, 1 800 random sets, lamellae).  Theorem 4.2′
  is a statement about limit points: the `O(1/N)` constants for finite `N` were not computed.  Floating point
  only: the volume `2.729` of the zero-gauche LP set and the values of `γ_LP` away from the certified inequalities.
* **Rings**: §3.4 is a sketch without constants or numerics; `K^{ring}` versus `K^{br}` is open.
* **Connected site sets** (lattice animals) were not enumerated; the outer approximations use only the degree
  condition and, in the path-cluster programme, the chain marks.  The class tables for `N = 24…27` are the other
  division's (my enumeration confirms them up to `N = 23`).  The percentages "67 %" of §5.2(a) depend on which
  optimal vertex the LP solver returns in degenerate directions.
* **Lemma 3.1**: the upper constants `(1, 9, 14)` are proved but probably not attained (observed maxima `(0,2,5)` for
  `N ≤ 11`); I did not search for the worst case.
* **Packings and covers of §7** are greedy: the lower bounds are valid but not optimal; the "greedy cover" numbers
  are estimates on a grid, not bounds.  No exact set cover of the limit model was computed.
* **Finite-`N` upper bounds** use `𝒦₁^{(N)}`; I did not verify the enlargement `(4M + c₃ + 2c₈)/N` beyond the direct
  check of the finite inequalities on small walks.
* **Off-lattice chain (§7.3)**: no computation of my own; `M ≈ 63`, `c ∈ [0.03,1]` and the saturation lengths are
  estimates under stated assumptions; `σ(ρ)` was not measured.
* **Surface law**: `k_N ≈ 1.8` is an observation for `N ≤ 27`; the proved constants are `0.50` and (lamellae) `2.5`.
* **Proposition 8.1**: lower bound checked for arms up to 30 and extended by periodicity (verified, not written
  out as a formal induction); the scaling form `nΦ(d/n)` is a conjecture.  The remark that Theorem 11.37 gives
  `μ^{n−O(√n)}` on the self-avoiding domain is a sketch.
* **Literature**: of the primary sources only four pages of one paper were read in full; everything else is
  abstracts or search summaries.  I did not search the mathematical literature on limit shapes of ground states
  (Wulff-type results for lattice gases with connectivity constraints).
* Nothing was machine-checked in Lean.  Theorems of the theory report (11.37, 11.48, 11.49) and of `P_REPORT.md`
  were used as stated.

## 12. Files, commands, sizes, run times

All in `scratchpad/ws/S/`; `ulimit -v 2000000`, one process at a time, every run below ten minutes; no random
seeds except where given.  `DATA = eng_data/experiments/eng/chain_cover/data` (extracted with `git archive` from
`origin/research/ubuntu-engineering`; read-only use).  Build: `gcc -O3 -march=native -o code/X code/X.c`.
(Process discipline, for the record: every computing process ran alone and for less than four minutes; twice a
shell command chained several such processes for more than ten minutes in total, and a few text-editing
snippets of a few milliseconds were run while a long job was in the background.)

| command (from `ws/S/`) | what | size | time | outcome |
|---|---|---|---|---|
| `python3 code/g1_check.py 9 DATA` | Lemma 2.1, both definitions, class tables | `n ≤ 9`, 17 107 conformations | 2 s | identities hold for every conformation; tables identical to the other division's (`out/g1_check.txt`) |
| `code/run_enum.sh` (`code/enum walk\|bridge\|hsw N`) | own enumeration | walks `N ≤ 23` (`2.1·10⁹`), bridges `N ≤ 24` (`1.4·10⁹`), half-space walks `N ≤ 22` | 215 s, 145 s, 63 s for the largest | `out/{walk,bridge,hsw}_N*.txt`, log `out/run_enum.log` |
| `python3 code/g3_compare.py out DATA` | validation, extremes, distances, nestedness, convexity | all `N ≤ 27` | 7 s | walk tables identical for `N ≤ 23`; `out/g3_compare.txt` |
| `cd code; python3 g2_concat.py 8 4000 1`; `… 11 400 7` | Lemma 3.1 | 61 312 and 29 376 pairs | 116 s, 64 s | all checks pass; `out/g2_concat.txt`, `out/g2_concat_N11.txt` |
| `cd code; python3 g1_local.py 11`; `python3 lattice_facts.py`; `python3 strip_check.py` | Lemma 2.3, finite inequalities; facts F1–F3; Proposition 5.5 | 9 188 bridges, 6 lamellae | 4 s | hold; `out/g1_local.txt`, `out/lattice_facts.txt`, `out/strip_check.txt` |
| `python3 code/cluster_lp.py 2000 1 out/lp_vertices_deg2.npy` | site-cluster LP | 256 variables, 2 026 directions | 5 s | 12 vertices, volume 3.2269; `out/cluster_lp_deg2.txt` |
| `cd code; python3 lp_exact.py ../out/lp_vertices_deg2.npy ../out/lp_exact.txt` | exact certificates | 11 facets, 46 orbits | 1 s | all certified exactly |
| `python3 code/cluster_lp4.py 1500 1500 out/lp4`; `python3 code/cluster_lp4_zero.py 1500 out/lp4_zero_vertices.npy`; `cd code; python3 gamma_lp_points.py` | path-cluster LP (floating point) | 340 configurations | 12 s, 10 s, 1 s | volumes 3.125, 2.729; `γ_LP` values; `out/cluster_lp4*.txt`, `out/gamma_lp_points.txt` |
| `cd code; python3 lp4_exact.py ../out/lp4_exact.txt ../out/lp4_vertices3.npy`; `python3 lp4_gamma_cert.py ../out/lp4_gamma_cert.txt` | exact certificates for Theorem 4.2′ | 48 orbits, 12 facets, gauche inequalities | 1 s, 1 s | all certified exactly |
| `cd code; python3 build.py "WITNESS" 128 128 128` (witness of `(0,12/5,22/5)` in `out/witnesses.txt`) | the bridge used for `γ ≢ 0` | 166 199 beads | 37 s | `out/build_gauche_W128.txt` (and `W96`) |
| `code/periodic K 2`, `K = 1…12` | periodic site sets | 455 sublattices × `2²⁴` sets at `K = 12` | 220 s | `out/periodic_K*.txt`; hull: `python3 code/periodic_hull.py out 12 out/lp_vertices_deg2.npy` |
| `code/pchain K`, `K ≤ 11`; `code/run_pchain12.sh` | periodic chain systems | `1.3·10⁸` (`K = 11`), `1.23·10⁹` (`K = 12`, four parts) | 62 s; 4 × ≈ 170 s | `out/pchain_K*.txt`; hull: `python3 code/pchain_hull.py out 12 out/lp_vertices_deg2.npy` → `out/pchain_hull_K12.txt`, trend `out/pchain_hull_trend.txt` |
| `cd code; python3 check_inside.py ../out`; `python3 check_thm42_random.py` | consistency of outer bounds with all periodic structures; Theorem 4.2 on random finite sets | 20 075 + 5 680; 1 800 | 4 s, 1 s | no violation; `out/check_inside.txt`, `out/check_thm42_random.txt` |
| `cd code; python3 lamella.py`; `python3 rodpairs.py` | Proposition 4.3 | up to 31 880 beads | 1 s | `out/lamella.txt`, `out/rodpairs.txt` |
| `code/run_build.sh` | finite bridges from nine periodic systems | boxes 16…64, up to 27 144 beads | 90 s | all valid bridges; `out/build.txt` (witnesses: `out/witnesses.txt`) |
| `python3 code/cover.py walk\|bridge N Lnum Lden EPSnum EPSden [limit] [c\|w]` | covering numbers | up to 4 532 classes | ≤ 204 s | reproduces 8, 11, 15, 2, 3; `out/cover_norm_check.txt`, `out/cover_bridge_vs_walk.txt` |
| `python3 code/g5_bounds.py out`; `cd code; python3 g5_finiteN.py ../out ../DATA`; `python3 g5_estimate.py ../out 12` | bounds and estimates of §7, surface law | — | 69 s, 1 s, 28 s | `out/g5_bounds.txt`, `out/g5_finiteN.txt`, `out/g5_estimate.txt` |
| `cd code; python3 finite_packing.py 27 60 120 250 500 1000 2000`; `… 5000` | Proposition 7.3 | up to 6 196 explicit walks of 5 000 beads | 52 s; ≈ 4 min | `out/finite_packing.txt`, `out/finite_packing_5000.txt` |
| `cd code; python3 g6_flip.py 43`; `python3 g6_flip_all.py 30` | Proposition 8.1 | 784 hairpins | 1 s | `D − 14d ∈ [−15, −5]`; `out/g6_flip.txt`, `out/g6_flip_all.txt` |
