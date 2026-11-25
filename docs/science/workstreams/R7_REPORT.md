# Workstream R7 — independent review and replication of the engineering division's results

Object reviewed: branch `research/ubuntu-engineering` at commit `a2f6dc781de05b642189a51d2ed88f94e8ed7026`
("`a2f6dc7`").  Every engineering file named below is cited by its path on that branch at that commit and
can be obtained with `git show a2f6dc7:<path>`.  My working copy of those files
(`experiments/science/ws_R7/eng_copy/`) is git-ignored and is not part of the science branch; it is
re-created by `experiments/science/ws_R7/make_eng_copy.sh`.  Everything of mine that is needed to
reproduce a number in this report is in `experiments/science/ws_R7/` (scripts `own_*.py`, `own_*.c`,
`x005_refit.py`, `x006_recount.py`, `check_*.py`, `rerun_engineering.sh`; outputs `out_*`, `rerun_logs/`;
the running log `NOTES.md`).

Three kinds of evidence are kept apart throughout:

* **REPLICATED** — recomputed with my own code, written from the model definition *before* I read the
  engineering implementation of that item (the order of events is in `NOTES.md`);
* **RE-RUN** — the engineering code at `a2f6dc7`, exported into a throw-away work tree outside the
  repository and executed here (`rerun_engineering.sh`);
* **READ** — read and checked for internal consistency (including recomputation from *their* stored
  files with my own code, which tests the document against the artifact, not the artifact).

Labels of COMMON rule 6: **[V]** machine-checked, **[P]** paper proof given here, **[K]** known and cited,
**[N]** numerical evidence only, **[C]** conjecture, **[H]** heuristic.  Nothing here was machine-checked.

*(This file is being written section by section while computations run; sections 1, 3.2–3.6 and 4–7
are appended as their results arrive.)*

---

## 2. Precise statements, with proofs or counterexamples

### 2.1 The "generic" chain is exactly decidable up to 14 torsions; the "exact ties" are identities

Model "gen" (theory `docs/workstreams/P_REPORT.md` §0): unit bonds `b_k = x_{k+1} − x_k`, bond angle
`θ = 111°`, torsions `180°, ±60°`.  Put `c := −cos θ = b_k·b_{k+1}` (`= cos 69° = 0.358368…`).

**Proposition G1 [P; checked numerically by integer-relation search at 50 digits].**  For every torsion
word and all beads `p < q`, the squared distance `s_pq = |x_q − x_p|²` is a polynomial in `c` with
**rational** coefficients, of degree at most `q − p − 1`.

*Proof.*  `s_pq = (q − p) + 2 Σ_{p ≤ k < l ≤ q−1} b_k·b_l`.  In the frame attached to bond `k`, `b_l` has
coordinates `T_{k+1}⋯T_l e₁` with `T_j = R_x(φ_j)R_z(π − θ)` (`R_z`: rotation by the angle between
consecutive bonds, entries `c, ±s, 0, 1` with `s = sin θ`; `R_x`: rotation by a torsion, entries
`1, 0, cos φ ∈ {−1, ½}, ± sin φ ∈ {0, ±√3/2}`).  So `b_k·b_l` is the `(1,1)` entry of a product of `l − k`
such matrices: a polynomial of total degree `≤ l − k` in `(c, s)` with coefficients in `ℚ(√3)`.
(i) *It is even in `s`.*  With `P = diag(1, −1, −1)`: `P R_z(α) P = R_z(−α)`, `P R_x(φ) P = R_x(φ)`,
`Pe₁ = e₁`; so replacing `s` by `−s` conjugates the product by `P` and leaves the `(1,1)` entry
unchanged.  Writing the entry as `A(c) + s·B(c)` (use `s² = 1 − c²`), evenness gives `B = 0`.
(ii) *Its coefficients are rational.*  With `M = diag(1, 1, −1)`: `M R_x(φ) M = R_x(−φ)`,
`M R_z(α) M = R_z(α)`, `Me₁ = e₁`; so the mirror image (all `φ_j → −φ_j`, i.e. `√3 → −√3` in the
expression) has the same entry.  Writing it as `A(c) + √3·B(c)` with `A, B ∈ ℚ[c]`, invariance gives
`B = 0`.  ∎

Examples found by PSLQ and consistent with the proof (`out_own_ties_detail.txt`): 1–4 pair, trans
`5 + 4c`, gauche `2 + 4c + 3c²`; 1–5 pair `tt`: `8 + 8c`; `g⁺g⁺`: `(7 + 7c + 9c² + 9c³)/2`; `tg`:
`5 + 8c + 3c²`.

**Proposition G2 [P, given K].**  `cos 69° = cos(2π·23/120)` is an algebraic number of degree
`φ(120)/2 = 16` (**[K]**, the degree of `cos(2πk/n)`; confirmed here by `sympy.minimal_polynomial`, which
returns `65536x¹⁶ − 262144x¹⁴ + … − 384x² + 1`).  Therefore, for a chain with `n ≤ 14` torsions
(`N − 2 = n + 1 ≤ 15`), at `θ = 111°` exactly:
(a) two squared distances are equal iff they are equal as polynomials in `c`; a non-constant squared
distance never equals a rational number — in particular never the hard-core bound `3` or the cutoff
`16`;
(b) for two conformations `x, y` the profile distance `D(x,y) = Σ_k |s̃^x_(k) − s̃^y_(k)|` (sorted truncated
squared distances; P_REPORT Proposition 2) is the value at `cos 69°` of one polynomial `Q_xy ∈ ℚ[c]` of
degree `≤ n + 1`, and the same polynomial gives `D(x,y; θ)` for all bond angles in a neighbourhood of
`111°`; `D(x,y)` is rational iff `Q_xy` is constant.

*Proof.*  (a) The difference of two distinct rational polynomials of degree `≤ 15` cannot vanish at an
algebraic number of degree 16.  (b) By (a) the only ties in the weak order of the finitely many values
`{s_pq(x)}, {s_pq(y)}, 16` at `111°` are between identical polynomials, so that order persists on a
neighbourhood; there the two sorted lists are fixed lists of polynomials and every `|·|` has a fixed sign
(or is identically zero).  Rationality of the value forces constancy, again by the degree.  ∎

**Corollary G3 (what this settles) [P + N].**  For `n ≤ 14`, every *equality* that a computation on
this model can meet — equal profiles (class identity), a pair exactly at the hard core or at the
cutoff, a profile distance exactly equal to a rational threshold `(gmin + ε)/L` — is a polynomial
identity in `c`, valid for an open interval of bond angles; it is not an accident of `111°`, and it is
reproduced by floating point to rounding error (`~10⁻¹³`).  Every *strict inequality* has the margin
measured in §3.1 (cover relation: `≥ 2.9·10⁻⁸` for `n ≤ 12`; distinct distance values: `≥ 5.4·10⁻⁶`; hard
core: `≥ 0.020`; cutoff: `≥ 0.035`), five orders of magnitude above rounding error.  **So the
floating-point results of the engineering division for the generic chain (label [X\*] there) are the
exact ones for `n ≤ 12`** — the margins are **[N]**, the dichotomy "identity or margin" is **[P]**.

**Proposition G4 (the five "exact ties" of ENG-RES-0007 §3) [P for one pair, by explicit polynomials;
N for all five: 60 digits at 111° and 30 digits at seven bond angles].**  At `n = 11` the five pairs
(centre, point) listed in §3.1 have `D ≡ 13` identically in `c`.  For the pair
`tt g⁺g⁺ t g⁻ tt g⁺ t g⁻` / `g⁺ t g⁺ ttt g⁺g⁺ t g⁻g⁻`, eleven of the 66 sorted positions differ; the
positive differences sum to `13/2 + P(c)` and the negative ones to `13/2 − P(c)` with
`P(c) = (21c − 3c² − 9c³)/2`, so `D = 13` for every bond angle at which the order of the 132 values is
the same as at `111°` (numerically: `D = 13.000…` to 30 digits at `110°, 110.5°, 111°, 111.5°, 112°,
113°, 115°`, and `D = 12.81…12.94` at `109°`, where the order has changed).

This answers the remark of ENG-RES-0007 ("that sums of differences of squared distances of this
'generic' chain can be exact integers is itself a small observation; we did not pursue it"): the chain
is generic in its *angle* but its distances live in a 16-dimensional ℚ-vector space, and integer-valued
profile distances are frequent (§3.1: 17, 65, 208, 581, 1 566 pairs of classes at `n = 10 … 14`).

### 2.2 Fractional hitting numbers on the uniform cube (X-003): re-derivation

Setting (theory `docs/workstreams/A_REPORT.md` §2.0, uniform cube): `X = {0,1}ⁿ`, `π` uniform, slack
`u·d_H`; for a proper nonempty `D ⊂ X`, `h_D(y) = u·d_H(y, Dᶜ)`; `D` is *sensitive at level `ε`* iff
`ln E_π e^{h_D} > ε`; `FC_n(ε) = 1/max_q min_{D sensitive} q(D)`.

**Proposition H [P + K (Harper's vertex-isoperimetric theorem); derived by me before reading
ENG-RES-0006; the derivation there is the same].**
(H1) `FC_n(ε) = 2ⁿ / m*`, `m*` the least size of a sensitive set.  *Proof:* `q ↦ min_D q(D)` is concave
and invariant under the automorphism group of the cube (the family of sensitive sets is defined
metrically), which is vertex-transitive; averaging `q` over the group does not decrease the value and
gives the uniform distribution.
(H2) For every `m`, `max_{|D| = m} E e^{h_D}` is attained at the complement of the initial segment
`I_{2ⁿ−m}` of the simplicial order.  *Proof:* with `C = Dᶜ` and `N^j` the `j`-fold closed neighbourhood,
`Σ_y e^{u·d(y,C)} = e^{uJ}2ⁿ − Σ_{j=0}^{J−1}(e^{u(j+1)} − e^{uj})|N^j(C)|` (Abel summation, `J ≥` the largest
distance), decreasing in every `|N^j(C)|`; by Harper `|N(S)| ≥ |N(I_{|S|})|` and `N(I_k)` is an initial
segment, so all `|N^j(C)|` are minimised simultaneously by `C = I_{|C|}`.
(H3) These optimal sets are nested, so `F(m) := max_{|D|=m} E e^{h_D}` is nondecreasing and
`m* = min{m : ln F(m) > ε}` is found by bisection.  Consequently `1 ≤ FC/FC_dip < |B(k)|/|B(k−1)|`, `k` the
radius of the smallest sensitive ball (the Harper set of size `|B(k−1)|` *is* the ball, which is not
sensitive).  ∎

Checked: §3.3 (brute force over all subsets for `n ≤ 4`, including an LP that does *not* assume (H1)).

### 2.3 The reduction of outer landscapes to tail functions (ENG-RES-0008 §5): re-derivation, scope, and one addition

Let `g` be `u`-Lipschitz on `Q_m` (Hamming metric), `W = e^{−g}`, `m(t) = |{W > t}|`, and `∂(k)` the size of
the closed neighbourhood of the initial segment `I_k` of the simplicial order.

**Proposition T [P + K (Harper); re-derived; checked numerically in exact integer arithmetic, §3.4].**
(a) `m` is nonincreasing and right-continuous and `m(te^{−u}) ≥ ∂(m(t))` for all `t > 0`.
(b) Conversely, every nonincreasing right-continuous `m` with values in `{0,…,2^m}`, equal to `2^m` below
a positive threshold and to `0` above another, with `m(te^{−u}) ≥ ∂(m(t))` for all `t`, is the tail
function of a `u`-Lipschitz `g` whose super-level sets `{W > t}` are initial segments.
(c) The tail functions whose level sets are balls are those of monotone radial profiles with
increments in `[0, u]`.
*Proof.*  (a) If `x ∈ N({W > t})` then `W(x) ≥ W(y)e^{−u} > te^{−u}` for a neighbour (or `x` itself)
`y ∈ {W > t}`; so `N({W > t}) ⊆ {W > te^{−u}}`, and `|N(S)| ≥ ∂(|S|)` is Harper's theorem.  (b) Put
`S_t := I_{m(t)}` (nested, since `m` is nonincreasing) and `W(x) := sup{t : x ∈ S_t}`; `W > 0` by the lower
threshold, `{W > t} = S_t` by right-continuity.  For neighbours `x, y` and `t < W(y)`: `y ∈ S_t`, so
`x ∈ N(S_t) = I_{∂(m(t))} ⊆ I_{m(te^{−u})} = S_{te^{−u}}`, i.e. `W(x) > te^{−u}`; let `t ↑ W(y)`.  (c)
`∂(|B(r)|) = |B(r+1)|`.  ∎  **The engineering argument is correct as stated.**

**Addition T(d) (how far "up to partial shells" is) [P].**  For every admissible `m` let
`r(t) := max{r : |B(r)| ≤ m(t)}` (for `m(t) ≥ 1`) and `m_rad(t) := |B(r(t))|` (`0` if `m(t) = 0`).  Then
`m_rad` is the tail function of a monotone radial profile with increments in `[0, u]`, and

    m_rad(t)  ≤  m(t)  <  |B(r(t)+1)|  ≤  (m + 1)·m_rad(t).

*Proof.*  `∂` is nondecreasing (initial segments are nested), so
`m(te^{−u}) ≥ ∂(m(t)) ≥ ∂(|B(r(t))|) = |B(r(t)+1)|`, i.e. `r(te^{−u}) ≥ r(t) + 1` whenever `r(t) < m`: the
radius grows by at least one per factor `e^{−u}`, which is the condition "increments `≤ u`" for the
radial profile `F(d) = −ln sup{t : r(t) ≥ d}`.  `|B(r+1)|/|B(r)| ≤ 1 + C(m, r+1)/C(m, r) ≤ m + 1`.  ∎
So every tail probability of every `u`-Lipschitz landscape is within a factor `m + 1` of that of a
monotone radial one: negligible at the exponential scale, but **not** small compared with the
differences the engineering tables resolve (`ln(n_o+1)/(na) ≈ 0.06` at `n = 1000`, `u = 1`, against
"`0.002·na`").  No instance with a partial shell was evaluated by the engineering search (§5, §7).

**Scope T(e) (what the outer loop reads) [P, from the text of the algorithm].**  Step 1 of Algorithm 2L⁺
(theory `docs/workstreams/K_REPORT.md` §2.2) gives a new outer point `a` the trivial bracket
`[e^{−ψ(a,0)−un_i}, e^{−ψ(a,0)+un_i}]` after one query of `ψ(a, 0)`.  So the outer loop reads an instance
through the joint law of the pair `(W(a), ψ(a,0))` (and through what the inner procedures return), not
through the law of `W(a)` alone.  For product instances `ψ(a,b) = g(a) + F_i(b)` the second coordinate is
a function of the first and the reduction applies — and then it applies to the *distribution* of
literal runs with oracle inner behaviour, not only to mean runs, because the outer sample is i.i.d.
uniform.  For a general `u`-Lipschitz `ψ` the offset `t₀(a) = ψ(a,0) + un_i + ln W(a)` varies with `a`
within `[n_i(u − Λ₁), n_i(2u − Λ₁)]`, and the reduction says nothing.  ENG-RES-0008 §5 states this limit
("fibres that differ from point to point other than by their value at the reference"); the remark by
which the theory division adopted the argument (theory report at `40c5bd7`, after Theorem 11.56: "The
outer loop sees an instance only through the law of the fibre averages … the mean run on any instance
is the mean run on an instance whose outer level sets are initial segments") **drops it**.

### 2.4 What "no violation in 7 095 840 mean runs" is (X-005)

**Statement S1 [read from `src/metricchain_eng/twolevel/meanrun.py` and the stored results].**  A *mean
run* is one deterministic evaluation of Algorithm 2L⁺ on one instance (a discrete law of `W`, a reference
value `ψ₀`, one fibre offset `t₀`) and one inner behaviour ("bottom" or "top"), in which every random
count `#{i ≤ M : W(a_i) > s}` is replaced by its mean `M·P(W > s)`.  The number `7 095 840` is the sum of
the numbers of objective-function evaluations of 2 624 differential-evolution searches
(`5 144 256 + 1 568 160 + 383 424`, files `x005_cost.jsonl`, `x005_claims.jsonl`, `x005_converge.jsonl`;
recounted).  Hence "no violation in `7·10⁶` mean runs" is
* a statement about **expectations**: the inequalities of Theorem 11.56 hold along the trajectory that
  the algorithm follows when all counts sit at their means — which is how the deterministic part of
  the proof (accounting on the good event) is tested, not its probabilistic part;
* a **count of evaluated instances**, strongly dependent (populations of an optimiser converging, in
  468 cells `(u, n, φ)`), from one 19-parameter family of radial product instances — not a number of
  independent trials, and no confidence statement attaches to it;
* **not a statement about a tail.**  The only tail statement of the experiment is that of X-006
  (585 000 literal runs with oracle inner brackets at `n_o ≤ 300`, `n_i = 6`: zero failures, hence a
  failure frequency below `5.1·10⁻⁶` at 95 % *pooled over the 117 cases*, below `6.0·10⁻⁴` for each
  single case, `1.6·10⁻³` with a Bonferroni correction over the cases) — recounted in §3.5.
"Violation" means a slack above `10⁻⁷` in the logarithm (`Run.violations`, `tol = 1e-7`); the message
does not state this tolerance, and its table shows the validity slack `ln L − ln A` at
`+1.6·10⁻¹⁰` (rounding at an instance where `L = A`).

**Statement S2 (the trend) [N; refit of the stored data, §3.5].**  Over `n = 250 … 128 000` the excess of
the worst case found over the claimed exponent decays *faster* than `1/√n` at every size: effective
exponents `0.76, 0.68, 0.63` (`u = ½, 1, 2`; `0.71, 0.61, 0.56` for `n ≥ 4000`), and the column
"difference × √n" of the engineering table falls by factors `4.9, 2.9, 2.2` across the range.  A pure
law `A/√n` misfits by 24–45 % (rms, relative); `A/√n + B/n` fits to 3–4 %, `A/√n + B·ln n/n` equally
well, and a pure power `n^{−2/3}` fits `u = 1` to 8 %.  The data are *compatible with* an asymptote
`∝ 1/√n` reached from above with a `1/n` correction that is still as large as the leading term at
`n ≈ 6000, 1300, 440`; they neither establish nor exclude the exponent ½.  The sentence of ENG-RES-0008
§3 ("consistent with the `O(√n)` correction of the theorem") is accurate; the digest's "the excess
decays about like `1/√n`" (`docs/collaboration/ENGINEERING_TO_THEORY.md`, item 1) is not what the data
show.

---

## 3. Numerics: what was done, at which sizes, with what result, and how to re-run it

All runs: one core (`OMP_NUM_THREADS=1`), this machine (shared; load average 7–8 on 4 cores during the
work), Python 3.13, NumPy 2.5.3, SciPy 1.18.1 (HiGHS), mpmath 1.3.0, gcc 13.3; OR-Tools 9.15.6755
installed into a private directory outside the shared environment (for CP-SAT only).  No remote
resource was used and no Modal job was re-run.  From `experiments/science/ws_R7/`:

### 3.1 X-004 — the generic (off-lattice) chain (ENG-RES-0007 §3, ENG-RES-0009 §2): REPLICATED, no difference

Own code, written from P_REPORT §0, §2.1 and theory report Theorem 11.4 before any engineering file
on X-004 was opened: `own_gen.py` (enumeration breadth-first with prefix pruning, **no** symmetry
reduction; profile classes by *global* clustering of the occurring distance values with the gap
spectrum recorded), `own_cover.py` (cover relation `L·D ≤ gmin + ε`; greedy; LP; a tolerance-free
lower bound; MILP by HiGHS with exact re-check of the returned cover), `own_entropy.py` + `l1kern.c`,
`own_stats.py`, `own_hardcore.py`, `own_ties*.py`, `own_integer_distances*.py`, `own_angle_robust.py`.
The engineering implementation (`src/metricchain_eng/chains/generic_chain.py`, `generic_analysis.py`,
`profile_cover.py`, `experiments/eng/chain_cover/generic_entropy.py`) was read afterwards; it differs
in method (depth-first with mirror reduction; class key = distances rounded to 8 decimals; dominance
reductions before the integer programme) and agrees in every number:

| quantity (engineering source) | range | engineering | mine | verdict |
|---|---|---|---|---|
| conformations (ENG-RES-0007, -0009) | `n = 5…14` | 99, 239, 577, 1 393, 3 363, 8 115, 19 559, 47 141, 113 587, 273 623 | identical | REPLICATED |
| profile classes | `n = 5…14` | 30, 60, 136, 291, 639, 1 360, 2 908, 6 137, 13 012, 27 421 | identical | REPLICATED |
| cover table, 12 cells per `n` | `n = 5…9` (60 cells) | all proved optima | identical in all 60 (in 40 my LP certificate alone proves the optimum) | REPLICATED |
| cover table | `n = 10` (12 cells) | 319, 223, 255, `[209,211]`, `[119,123]`, 60 ; 13, 8, 10, 8, 5, 3 | identical, including the two open brackets with the same ends (240 s per cell on one core) | REPLICATED |
| cover table | `n = 11, 12` | 12 exact cells, 12 brackets | see below | (see below) |
| "nearest tie" column | `n = 5…12` | 5.2e-4, 2.7e-4, 1.2e-4, 1.8e-5, 4.5e-6, 3.2e-7, (ties), 2.9e-8 | 5.211e-4, 2.711e-4, 1.155e-4, 1.824e-5, 4.473e-6, 3.248e-7, (5 ties; nearest non-tie 1.273e-7), 2.929e-8 | REPLICATED |
| exact ties | `n = 5…12` | 5 at `n = 11` (`L = 1`, `ε = N/2`), none elsewhere | the same 5, none elsewhere | REPLICATED, and explained (§2.1) |
| hard-core margins at `n = 10` | | 0.078 above, 0.020 below | 0.078462, 0.020008 | REPLICATED |
| "classes never closer than 0.035" | `n ≤ 12` | 0.035 | 0.0353 (and 0.0075, 0.0072 at `n = 13, 14`) | REPLICATED |
| pairs within the cutoff per bead (three statistics) | `n = 5…12` | e.g. 2.58 / 2.46 / 4.23 at `n = 10` | identical | REPLICATED |
| distance entropy `σ(ρ)`, six radii | `n = 5…14` (60 numbers) | table of ENG-RES-0009 §2 | identical to the three printed decimals | REPLICATED |

Two things I expected to be weak points and that are not: (i) the column "max" of pairs per bead
equals (number of pairs)/N at every size — it is real (the conformation `(t g⁺g⁺)^k` keeps all pairs
within the cutoff up to 17 beads); (ii) the class key "round to 8 decimals" could split a class if a
value sat on a rounding boundary — my boundary-free clustering gives the same counts at every size.

*Ties and exactness.*  `own_ties.py 5 12`: the five ties at `n = 11`, re-evaluated at 60 digits from the
torsion words, have `D − 13 = O(10⁻⁶⁰)`.  In my float64 run all five come out slightly **above** 13
(`13.000000000000014 … 37`), in the engineering run one example is `12.999999999999998`: without the
tolerance `10⁻⁹` the two programmes would have decided these comparisons differently; with it both
count them as covered, which is the exact answer (§2.1, G4).  `own_angle_robust.py 5 12`: the set of
accepted torsion words and the partition into profile classes are unchanged when the bond angle is
moved by `−0.02°, −0.007°, +0.003°, +0.011°, +0.03°` — the equalities that define the classes are
identities (G2), not accidents.  Integer-valued profile distances (`own_integer_distances*.py`):

| `n` | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|
| unordered pairs of classes with `D ∈ ℤ` (to `10⁻⁹`) | 1 | 11 | 17 | 65 | 208 | 581 | 1 566 |
| exact ties of the `L = 1` cover relation, `ε = N/4` / `ε = N/2` | — | 0 / 0 | — | — / 5 | — | **4 / 253** | — |
| nearest non-tie over the six `L = 1` cells | 1.6e-3 | 4.5e-6 | 1.5e-5 | 2.4e-6 | 2.5e-6 | 5.0e-7 | **2.1e-8** |

("—": the accuracy is not an integer at that size, so no tie is possible; at `ε = 0` and `ε = 1`, which
are integers at every size, there is no tie for any `n ≤ 14`.)  **At 13 torsions — the
next size on the engineering division's list — 253 comparisons of one cell sit exactly on the
threshold, and at 14 torsions the nearest non-tie is within a factor 20 of the tolerance.**  The
floating-point treatment is at its limit there; §7 asks for exact arithmetic in `ℚ[c]`.

*Covers at `n = 11, 12`.*  (pending — filled in below if the runs complete.)

Re-run: `python3 own_gen.py 11`; `python3 own_cover_table.py 5 9 300`; `python3 own_cover_table.py 10 10 240`;
`python3 own_entropy.py 5 12`; `python3 own_entropy.py 13 14` (77 s for `n = 14`); `python3 own_stats.py 5 12`;
`python3 own_hardcore.py 2 12`; `python3 own_ties.py 5 12`; `python3 own_ties_structure.py`;
`python3 own_ties_detail.py`; `python3 own_integer_distances.py 5 12`; `python3 own_integer_distances_big.py 13 14`;
`python3 own_angle_robust.py 5 12` (build the kernel first: `gcc -O3 -march=native -fPIC -shared -o l1kern.so l1kern.c -lm`).
Outputs: `out_own_cover_n5_9.txt`, `out_own_cover_table_*.{txt,json}`, `out_own_entropy_*.json`,
`out_own_ties_*.{txt,json}`, `out_own_integer_distances*.{txt,json}`, `out_own_angle_robust.txt`.

RE-RUN of their code (reduced size): see §3.6.

### 3.2 X-002 — lattice chains: the published covers as certificates (ENG-RES-0002 §§1–2, 4, 6; ENG-RES-0007 §2)

Own code: `own_lattice_cert.py` (exact primal check; tolerance-free dual bound), `own_dia.c` +
`own_dia_compare.py` (own enumerator, written from the model definition before `dia_enum.c` was read),
`own_lattice_opt.py` (HiGHS and CP-SAT in my own formulation on the unreduced instance), `own_flip.c`
(brute-force single-flip constants), `own_lattice_nets.py`, `check_eng_res_0002_prose.py`.

**(a) Class tables** (`experiments/eng/chain_cover/data/dia_Sc12_n*.txt`; per class: pair counts, number of
conformations, fewest and most gauche torsions).  My enumerator gives **identical tables for
`n = 1 … 20`** (with the mirror reduction; without it for `n ≤ 9`), e.g. `n = 20`: 2 139 332 335
conformations, 2 328 classes (253 s here).  This re-does, with a third implementation, what workstream
R2 did up to 23 beads.  The tables for `n = 21 … 24` (Modal job M-002) — see the end of this
subsection.

**(b) Primal certificates.**  `results/lattice_Sc12.json` stores for each of the 288 cells
(`n = 1…24` × 12 settings) the cover itself (`centres_hist`).  With my own profile distance
(`5|ΔC₁| + 3|ΔC₂| + |ΔC₃|`, derived from the definition) and an exact integer cover relation:
**all 288 stored covers are covers of the stored class table and have the published size**
(`python3 own_lattice_cert.py primal`: 0 failures); class counts and conformation counts of the result
file equal those of the class tables in all 24 rows.

**(c) Dual bounds — which optima are certified, and by what.**  My lower bound solves the dual of the
covering LP in floating point, truncates the weights to integers and evaluates the largest centre
load in exact integer arithmetic on the *unreduced* matrix; it is valid whatever the LP solver did.

| | cells | what proves the published lower end |
|---|---|---|
| published single number, my certified bound equals it | **241** | stored cover (checked) + exact LP certificate: **an optimum with no reliance on any branch and bound** |
| published single number, LP certificate 1 or 2 below | 22 | branch and bound only: 18 cells at `n = 14…18` (`L = 1`, `ε ∈ {0, 1, N/20, N/10}`) and 4 cells at `n ≥ 19`: `(19, N/10)` 35, `(19, N/4)` 22, `(20, N/4)` 24, `(22, N/4)` 26 |
| published bracket `[a, b]` | 25 | `b`: stored cover (checked, 25/25).  `a`: equals my certified bound in 15 cells; in **10 cells it is one above it** and is the HiGHS branch-and-bound bound after 300 s |

For `n ≥ 19` my certified bound equals the stored `lower_certified` in all 72 cells, and my LP value
equals the stored `lp_bound` in all 288 (to its 6 printed decimals).  The ten brackets whose published
lower end is *not* the certified bound: `(19, ε=0)` `[52, 56]` (certified 51); `(19, ε=1)` and
`(19, N/20)` `[42, 44]` (41); `(20, ε=0)` `[57, 61]` (56); `(20, N/10)` `[37, 40]` (36); `(21, ε=1)` and
`(21, N/20)` `[50, 54]` (49); `(23, ε=0)` `[74, 83]` (73); `(23, ε=1)` and `(23, N/20)` `[60, 67]` (59).
ENG-RES-0002 §2 describes every bracket as "`a` a certified lower bound"; the table generator
(`make_tables.cover_cell`) prints `max(lower_certified, lower_solver)`.  **So "is each bracket what it
says?": the upper ends yes; fifteen lower ends yes; ten lower ends are solver-trusted bounds, one
above what is certified.**  (They are very probably true; they are not what the text says they are.)
As a consequence all 24 published covering numbers of the theory division (P_REPORT §3.3, `n = 5…12`)
are among the 241: reproduced *and* certified independently of any solver's search.

**(d) "Two solvers agree on every cover" / "proved by HiGHS and CP-SAT independently for `n ≤ 18`".**
Three of the 18 cells that rest on branch and bound, 1 core:

| cell (published; LP-certified) | HiGHS, my formulation, unreduced | CP-SAT, my formulation, unreduced, 1 worker, 120 s | their `min_cover_highs` on their reduced instance | their `min_cover_cpsat(workers=1)` on it, 240 s |
|---|---|---|---|---|
| `n = 14`, `L = 1`, `ε = 1` (25; 24) | optimal 25 (13 s) | cover 27, bound 6 | proves 25 (5 s) | cover 27, bound 7, not proved |
| `n = 15`, `L = 1`, `ε = 0` (33; 32) | optimal 33 (6 s) | cover 38, bound 6 | proves 33 (4 s) | cover 39, bound 8, not proved |
| `n = 16`, `L = 1`, `ε = 0` (38; 36) | optimal 38 (45 s) | cover 50, bound 7 | proves 38 (21 s) | cover 43, bound 7, not proved |

The published optima are confirmed by HiGHS in three settings (their stored run; my formulation on
the unreduced matrix; their function re-run here).  That CP-SAT proves them *independently* I could
not confirm: with one worker it neither finds the optimum nor gets a bound above 8 in the time I can
give it; the engineering runs used 8 workers on 4 cores without a time limit (job M-004).  More
important for the record: **the evidence for the sentence cannot be regenerated from the repository.**
The stored rows `n = 1…18` have `solvers = {highs: k, cpsat: k}` and lack the keys `lower_certified`,
`lower_solver`, `exact_certified`, which `lattice_analysis.analyse_table` writes at *every* commit of
the branch (`206fd9e`, `db56d05`, `a2f6dc7`): they were produced by a version of the code that was
never committed.  In the committed `covering_number_P` the loop over solvers ends as soon as one of
them has proved optimality, so CP-SAT is only a fallback; re-running `analyse_table` at `a2f6dc7` for
`n = 14` reproduces all twelve covering numbers and reports `solvers = {greedy, highs}` or `{greedy}` —
**CP-SAT is not called in any cell** (`out_rerun_lattice_solvers.txt`).  And the stored rows record,
per solver, only the size it found, not whether it proved it.

**(e) Single-flip constants** (ENG-RES-0002 §6, `results/lattice_Sc12_flip.json`).  Own brute force
(every self-avoiding conformation, every torsion, both other states; gauche states defined by the
sign of a triple product): `c^{sf}` **identical for `n = 3, 5, 8, 9, 10, 11, 12, 13`**
(`n = 13`: `53 89 98 113 132 132 130 | sym`, 44 s).  Not replicated: `n = 14, 15, 16` and the exhaustive
test that `c^{sf}` is a valid Hamming envelope (their mode B).  The derived table of ENG-RES-0009 §1
(36 pairs `(n, j)`, bounds of Proposition 11.74, no violation; least excess 21 … 73; largest ratio
0.136 … 0.286) follows from the stored constants (recomputed).

**(f) Prose and derived numbers of ENG-RES-0002 / -0007 §2**, recomputed from the class tables and the
result file (`check_eng_res_0002_prose.py`): the finite-size table (2.45 … 4.56; 6.64 … 13.56; 7/8 …
14/24), "four gauche torsions reach `‖N‖₁ = 166`", the sequence of conformations and classes for
`n = 13…24`, `N_cov/N² = 0.100, 0.093, 0.109, 0.110–0.126`, the effective exponent 4.3, "at most 8" at
`L = 1/5`, the `ε = N/2` sequence, the hand-typed table of ENG-RES-0007 §2: all consistent.  (One
rounding: `166/27 = 6.15`, printed as 6.1.)  The two-line proof that every trans/gauche pattern is
realised (restrict even bonds to `{a₀, a₂}` and odd bonds to `{a₁, a₃}`: every bond then has
`y`-component `+1`) is correct **[P, checked by reading]**.

**(g) Entropy brackets** (ENG-RES-0002 §4) and **class tables for `n = 21, 22`**: (pending — see the end
of §3.2 below if completed.)

Re-run: `gcc -O3 -march=native -o own_dia own_dia.c && python3 own_dia_compare.py 1 20`;
`python3 own_lattice_cert.py primal`; `python3 own_lattice_cert.py dual 1 18` and `… dual 19 24` (13 min);
`PYTHONPATH=<ortools> python3 own_lattice_opt.py 120 "14:L=1,eps=1" "15:L=1,eps=0" "16:L=1,eps=0"`;
`PYTHONPATH=<ortools> python3 rerun_eng_two_solvers.py <work tree> 240 "14:L=1,eps=1" …`;
`gcc -O3 -march=native -o own_flip own_flip.c && ./own_flip -n 13`; `python3 check_eng_res_0002_prose.py`.

### 3.3 X-003 — exact fractional hitting numbers on the uniform cube (ENG-RES-0006 §1): RE-DERIVED and REPLICATED, no difference

`own_harper.py` (written from A_REPORT §2.0 before ENG-RES-0006 and
`experiments/eng/fc_uniform_cube/harper_fc.py` were read).

* `python3 own_harper.py brute` — all `2^{2ⁿ} − 2` proper nonempty subsets for `n = 2, 3, 4` and 30
  parameter pairs (`u ∈ {¼, ½, 1, 2, 3}` × `ε ∈ {0.05, 0.1, 0.3, 0.5, 1, 2}`; 90 cases; the engineering
  check has 72 cases with other parameters).  In all 90: (i) the least size of a sensitive set equals
  the prediction from simplicial-order sets; (ii) the linear programme `max_q min_D q(D)` over **all**
  inclusion-minimal sensitive sets, solved without assuming the uniform sampler, equals `m*/2ⁿ`
  (largest deviation `5.6·10⁻¹⁶`) — a check of (H1) that the engineering script does not make;
  (iii) for **every** size `m` the true maximum of `Σ_y e^{u·d(y,Dᶜ)}` over `|D| = m` equals the value at
  the complement of the initial segment (relative deviation `≤ 6.7·10⁻¹⁶`) — (H2) in full, not only at
  the threshold size.  Smallest margin of a sensitivity comparison: `6.0·10⁻⁴` (no tolerance issue).
* `python3 own_harper.py table 14` — explicit simplicial-order sets, distances by breadth-first search,
  bisection over `m`; no closed-form shortcut.  **All 52 rows of
  `experiments/eng/fc_uniform_cube/harper_fc_table.json`** (four parameter sets × `n = 2…14`: smallest
  sensitive `|D|`, smallest sensitive ball, its radius) **are identical to mine**; e.g. `u = 1`,
  `ε = 0.3`: `1, 2, 4, 6, 11, 19, 36, 64, 120, 222, 408, 763, 1432`.
* RE-RUN of their script: `harper_fc.py --check` prints "72 cases, all agree"; `--nmax 14` regenerates
  the stored JSON **byte for byte** (`rerun_logs/harper_check.log`).

Outputs: `out_own_harper_brute.{txt,json}`, `out_own_harper_table.{txt,json}`.

### 3.4 The tail-function reduction (ENG-RES-0008 §5): numerical checks of Proposition T

`python3 own_tail.py` → `out_own_tail.txt` (exact integer arithmetic throughout).

| check | sizes | result |
|---|---|---|
| T0: Harper's theorem itself — `min_{|S|=k}|N(S)| = |N(I_k)|` for every `k`, by brute force over all subsets | `Q_2, Q_3, Q_4` | true |
| T0′: the closed neighbourhood of an initial segment is an initial segment | `Q_m`, `m ≤ 12`, every `k` | true |
| T1: claim (a) on random `u`-Lipschitz landscapes of three kinds (largest Lipschitz minorant of random data; sparse deep dips; multiples of `u`), on grids of 1, 7 and 1000 units per unit slope | `m = 3, 4, 6, 8, 10`; 150–3000 landscapes per block | `min_t [m(te^{−u}) − ∂(m(t))] = 0` in every block: never violated, and tight |
| T2: claim (b) — random admissible tail functions, the constructed landscape must be `u`-Lipschitz and have the prescribed tail function | `m = 3…10`; 27 900 constructions | 0 failures |
| T3: exhaustive converse — the set of level-size sequences `(|{h ≤ 0}|, |{h ≤ 1}|, …)` of **all** integer-valued 1-Lipschitz `h` with `min h = 0` against the set of **all** sequences with `k_{j+1} ≥ ∂(k_j)` | `Q_2`: 19 functions; `Q_3`: 495; `Q_4`: 197 547 | 5 = 5, 17 = 17, 86 = 86 sequences, the two sets equal |

### 3.5 X-005 / X-006 — the statistics and the claims (not the algorithm)

Read: ENG-RES-0008 in full, `src/metricchain_eng/twolevel/meanrun.py` (definition of the mean run and
of "violation"), `adversary.py`, `experiments/eng/twolevel/run_search.py`, `recheck.py`.  Recomputed
from the stored result files with my own code (`x005_refit.py`, `x006_recount.py`):

* **Table "trend" of ENG-RES-0008 §3** (39 rows): worst case found, best `φ` against it, claimed
  exponent, difference, difference × `√n` — rebuilt from `x005_cost.jsonl`; identical in every printed
  digit.  **Refit** (relative least squares; `out_x005_refit.json`):

  | law fitted to the excess | `u = ½` | `u = 1` | `u = 2` |
  |---|---|---|---|
  | `C·n^{−p}`, all 13 sizes: `p` (± s.e. of the log–log regression) | 0.758 ± 0.011 | 0.676 ± 0.012 | 0.626 ± 0.010 |
  | the same, `n ≥ 4000` (best `φ` fixed at 0.50) | 0.707 ± 0.017 | 0.612 ± 0.022 | 0.560 ± 0.008 |
  | local exponent between the last two sizes | 0.63 | 0.56 | 0.54 |
  | `A/√n`: rms relative misfit, all sizes / `n ≥ 4000` | 45 % / 23 % | 33 % / 13 % | 24 % / 7 % |
  | `A/√n + B/n` | 3.0 % / 0.6 % | 4.0 % / 3.0 % | 3.7 % / 1.3 % |
  | `A/√n + B·ln n/n` | 4.6 % / 1.9 % | 4.0 % / 3.7 % | 3.8 % / 1.3 % |
  | `A·n^{−2/3}` | 18 % / 6 % | 7.7 % / 8 % | 10 % / 12 % |
  | `A·n^{−3/4}` | 7.4 % / 6 % | 14 % / 16 % | 22 % / 22 % |

  (These are deterministic numbers, not noisy samples: the "errors" are search sub-optimality and the
  grids of `φ` and of the ladder, so the misfits are descriptive, and a formal goodness-of-fit test
  would be meaningless.)  Reading: Statement S2 of §2.4.
* **The search budget is not uniform in `n`, and the message does not say so.**  From the stored
  records: 4000 (monotone) / 2000 (general) evaluations per search for `n ≤ 32 000`, 2500 / 1250 at
  `n = 64 000`, 1500 / 750 at `n = 128 000` (`run_search.tasks`: "reduced at the two largest sizes so that
  a task stays near a quarter of an hour").  The gain of the search over the best of its 63 structured
  starting points falls from `0.11·na` (`n = 250`) to `0.003·na` (`n = 128 000`), and its median over the
  searches of a size is exactly `0` for every `n ≥ 1400`.  The convergence control (five times the
  budget, two more seeds) covers four cells, all at `u = 1`, `n ∈ {1000, 16 000}`.  So at the two largest
  sizes — the ones that carry "no persistent margin" and "still falling at `n = 128 000`" — the number
  called "worst instance found" is in effect "the worst of 63 hand-made instances", obtained with the
  smallest budget and without a convergence control.  That the hand-made instances are near-optimal
  there is plausible (the theory predicts that the instance matters less as `n` grows) but it is not
  shown by this experiment.
* **X-006** (`x006_sampled.jsonl`, 585 records): the table of ENG-RES-0008 §6 recounted — 117 cases ×
  5000 runs = 585 000 literal runs at the theorem's `K`, no failure of any kind; with `K` divided by
  4, 16, 64, 256 the good event fails in 82 / 14 668 / 29 408 / 31 698 of 39 000 runs (`u = ½`), etc.;
  every number of the table agrees.  "Below `5.1·10⁻⁶` at 95 %, pooled": `1 − 0.05^{1/585000} = 5.12·10⁻⁶`,
  correct, and correctly qualified as pooled; for a single case the bound is `6.0·10⁻⁴`.  At the
  theorem's `K` the literal runs' mean `ln(evaluations)` differs from the mean-run value by
  `−0.0006 … +0.0019`, and the extreme runs of a case by `−0.0035 … +0.018`: at these sizes the cost is
  essentially deterministic, which is what licenses the mean run as a proxy *there* (`n_o ≤ 300`,
  `n_i = 6`, oracle inner brackets) and nowhere else.
* **"The flat instance is not the worst one"** is a constructive claim: one instance with a larger
  mean-run cost at the same `φ` suffices, and the stored file contains one for 464 of the 468 cells.
  I checked that the instances are members of the class (radial outer profile with slopes in `[0, u]`
  resp. `[−u, u]`; inner offset within `[−n_iΛ₁, n_i(u − Λ₁)]`, the exact range of
  `ln E e^{−F_i} + F_i(ref)` over `u`-Lipschitz `F_i`; product form) and that the stored maximisers
  reproduce the stored costs when re-evaluated by the engineering code (§3.6).  Whether the mean-run
  cost is the cost of the algorithm of the theorem is the question of workstream R6, not examined
  here.

Re-run: `python3 x005_refit.py`; `python3 x006_recount.py`.
