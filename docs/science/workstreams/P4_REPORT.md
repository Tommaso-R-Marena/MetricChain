# Workstream P4 (science division) — the theory division's share certificates and third-order pair form on our real instances; review of Theorem 11.18a and Propositions 11.18b, 11.18c

Report of an independent workstream of the Scientific Discovery, Translation & Independent
Validation Division.  Branch `research/scientific-translation`.  Written 2026-11-26, 01:53–02:40 UTC.
Scripts, logs, outputs and running notes: `experiments/science/ws_P4/` (`NOTES.md`).
Object of the review: theory report §11.7 at the theory commit `24a3c27` (read-only export),
`THY-RES-0009` §1 and §7, `proofs/Frontiers/ThirdOrderModel.lean`, `ShareCertificates.lean`.
Data: the enumerated grids of workstream P2 (`experiments/science/ws_P2/data/fb_*.npz`, read-only).

Labels as in `COMMON.md`: **[V]** machine-checked by the theory division (Lean name given; I read
the statement and compiled a copy, §3.6), **[P]** paper proof (theirs, re-derived by me, or mine —
said each time), **[N]** numerical evidence on random instances, **[M]** measured on P2's
enumerated instances (exact over the enumerated finite domain), **[K]** known, **[H]** heuristic.
Three kinds of checking are kept apart throughout: **review** (I re-derived the statement from
its hypotheses), **replication** (I re-computed with my own code), **re-run** (I ran their code).
Units: kcal/mol; `k_BT = 0.596161`; free energies in nats.

**What kind of numbers these are.**  Fixed synthetic peptides (homopolymers of Ser, Val, Leu,
Phe, Lys and the one patterned sequence of P2), rigid ideal backbones, P2's rotamer grid; no new
sequence, nothing optimised over sequences.  Every class constant is P2's *measured* constant —
an exact maximum over an enumerated domain, a lower bound for any larger domain, **not a
certified constant**.  A "certificate" below is a certificate *given those constants*.

---

## 0. How far I got

| item of the brief | state |
|---|---|
| 1. share certificate of Proposition 11.18b(d) on all instances of P2 | **done, completely** (908 analyses; §2.1, §3.1) |
| 2. site form against pair form of Theorem 11.18a on P2's measured `c_T`; mixed allocations by LP; soundness at every state | **done** (136 instances; §2.2, §3.2, §3.9) |
| 3. review of Theorem 11.18a (a)–(d), Proposition 11.18b (a)–(d), Proposition 11.18c (a)–(c) | **done** for every part (§1.2, §2.3–2.5); Lean copies compiled (§3.6); their harness blocks re-run (§3.5) |
| 4. pair form at order `m` for P3's certified sandwich | **done**: statement and 11 enumerated runs with P3's certified constants, floor side only (§2.6, §3.7) |

Not done: see §4.

---

## 1. Verdicts

### 1.1 The three answers asked for

1. **Of the 13 instance analyses of `g_GB` in which P2's row-sum condition fails and the exact
   second-order criterion holds, the share certificate of Proposition 11.18b(d) certifies 11.**
   It fails in two — Phe₄ on the helix and LKSE:2 on the helix, both at τ = 0.60 — in each case at
   a single pair of sites, by 0.036 and 0.034 kcal/mol.  The row-sum condition for the deficits
   (the split in halves) holds in 2 of the 13.  Over all 110 analyses of `g_GB` in which the
   criterion holds the certificate exists in 106 (the two others: Ser₂ on the strand at both
   thresholds, where P2's plain row-sum condition holds).  In the 61 polar and charged analyses in
   which the star fails no split exists — as soundness requires; the densest set of sites is
   over-dense by 2.7 to 274 kcal/mol.  For those peptides the relevant test is the third-order
   analogue (Proposition 11.18b(c)): of the 47 polar and charged instances in which the reference
   minimises the pair-form lower model, a split of the deficits exists in **25** (Ser on strand
   and PPII: 18 of 18; Ser on the helix: 0 of 9; Lys: 6 of 9; LKSE: 1 of 11).  [M]
2. **The pair form of the third-order lower model is tighter than the site form on the real
   constants** — pointwise at every state of all 136 instances, as it must be.  In numbers: the
   reference minimises the pair-form model in 132 instances against 113 for the site form (the
   exact three-body envelope: 133); `ln Z(model) − ln Z(E)` is smaller by a median factor **6.8**
   (range 1.0–137; Ser 1.8, LKSE 3.7, Lys 4.7, Phe 7.9, Leu 40, Val 41), medians `2.9·10⁻³` nats
   (pair) against `2.0·10⁻²` (site) and `2.6·10⁻⁴` (envelope); the largest gap `max(E − m)` is the
   **same** for the two forms in 129 of 136 instances (both penalties equal `Σ c_T` where every
   site is changed, and that is where the largest gap is).  An LP over shares gains little for
   the minimum (it changes the verdict in one instance, LKSE:6 on PPII) and a factor 0.82 in the
   median for `ln Z`; site shares are never useful (Lemma P4.2).  One LP over pair shares and
   state-dependent shares together finds, from the ball data alone, a certificate checked by
   additions in 133 of 136 instances — every instance in which the exact envelope certifies.  [M]
3. **Review**: table §1.2.  Two statements need a repair, both in Proposition 11.18c: (a) claims
   Proposition 11.18b for reset-closed domains, and its completeness part (b) is false there
   (counterexample with two sites); and the closing sentence about our measurement ("what the
   pruning discards is the set that (c) is about") does not describe P2's domains.  Everything
   else is correct; three sentences should be reworded ("at a single triple both are exact",
   "at the same cost", and the reasons given for "not necessary" in 11.18b(d)).

### 1.2 Review verdicts, part by part

| statement | verdict | what I did |
|---|---|---|
| Thm 11.18a (a) `I₂g` is pairwise | **correct** | review; replication (120 random instances, exact on the ball to `4·10⁻¹⁵`); Lean `anchoredInterp_three` read, copy compiled |
| Thm 11.18a (b) covering ⇒ pairwise lower bound; kernel soundness | **correct** | review; Lean `thirdOrder_pairwise_lower`, `verify_sound_thirdOrder` read against the wording, copy compiled; replication: `m ≤ E` at every state of 1 023 (instance, model) pairs on P2's grids, smallest `E − m` = `−1.1·10⁻¹³` |
| Thm 11.18a (c) site form, pair form, "the pair form is the tighter one" | **correct with a repair (wording)** | review; replication (136 real instances, 6 000 random states).  "At a single triple both are exact" holds only at configurations in which all three sites are changed (that is what `thirdOrder_witness` states); "at the same cost" (THY-RES-0009) is true of evaluations, not of the interaction graph (§2.3) |
| Thm 11.18a (d) neither is the exact envelope; best shares by LP | **correct** | review; attainment replicated by an LP over the class (28 points, error `2·10⁻¹⁵`); remarks: pair shares dominate mixed shares (Lemma P4.2); share-based coverings are a proper subset of the coverings of (b) (Example P4.3) |
| Prop 11.18b (a) soundness of shares; row-sum condition | **correct** | review; Lean `secondOrder_certified_of_shares`, `_of_rowSum` read, copy compiled; replication on 908 real analyses (no instance with shares and a failing criterion) |
| Prop 11.18b (b) completeness for an additive known part, "for every alphabet size" | **correct** (on product domains) | review (max-flow argument re-derived, single-state sites and ties included); replication: criterion ⇔ no over-dense set ⇔ flow in 1 500 random instances with 1–4 states per site, 135 exact ties.  Citations (Hakimi, Goldberg, Picard) not checked |
| Prop 11.18b (c) third order: deficits; shares among three sites ⇔ no set over-dense w.r.t. triples; exact when pair terms vanish | **correct** | review; replication (400 random instances: enumeration ⇔ over-dense test ⇔ LP) |
| Prop 11.18b (d) deficits of a pairwise known part: sufficient, not necessary | **correct**; the stated reasons for non-necessity are incomplete | review; replication (600 random + 908 real analyses).  The reason that occurs on our instances is a third one (one pair suffices; §2.4).  Instances asked for: Phe₄/H, LKSE:2/H, Ser₂/E for `g_GB`; 55 analyses of the exactly additive `g_99`, where `c_ij ≡ 0` |
| Prop 11.18c (a) "on a reset-closed domain nothing changes" | **correct with a repair** — wrong as stated for Proposition 11.18b(b) | review: true for Theorems 11.16, 11.17, 11.18, 11.18a and for the sound directions of 11.18b; the "iff" of 11.18b(b) fails on a reset-closed domain that is not a product (Counterexample P4.4, checked by LP).  Replication: remainder bounds on 60 random non-product domains (orders 2, 3) and on P2's real ones (order 2: 80 domains; order 3: 34), no violation |
| Prop 11.18c (b) `D′` is the largest reset-closed part; products are reset-closed | **correct**; the sentence applying it to our measurement is **wrong as a description** | review; replication (60 random domains: formula = brute force).  P2's pruned product equals `D′(x₀)` in 6 of 40 non-product analyses (§2.5) |
| Prop 11.18c (c) connectivity is not the condition; `{00, 01, 11}` | **correct**, and more is true (Proposition P4.5) | review; replication (LP unbounded at 41 of 41 points of `D ∖ D′`) |
| frequencies quoted in 11.18b and 11.18c | reproduced | re-run of their harness blocks XI.16–XI.18 in full mode (§3.5) |

---

## 2. Precise statements

Setting and notation as in theory report §11.7: sites `i`, states `x_i`, reference `x₀`, `S(x)` the
set of changed sites, `E = f + g`; `A_i(a) := E(x₀^{i→a}) − E(x₀)`, `Δ_i := min_{a≠x₀_i} A_i(a)`
(`+∞` for a site with one state); `T_ij`, `D_ij` the second mixed differences at `x₀` of `f` and of
`g`; `g_star` the star part, `I₂g` the interpolant of order two.

### 2.1 Item 1 — the share certificate of Proposition 11.18b(d) on P2's instances [M]

**What was run, exactly.**  For every instance analysis for which P2 wrote an output file
(184 files with at least two sites; residuals `g_GB`, `coul + g_GB`, `g_03`, `g_ipq`, `g_99`:
908 (instance, residual) analyses), on P2's pruned clash-free product `X′`:

* **Constants**: P2's enumerated class constants `c_ij(g)` = the exact maximum over *all*
  rectangles of `X′` of the second mixed difference of `g` (measured, not certified).  I
  recomputed them with a different algorithm (`p4lib.c2_matrix`); they coincide with the matrices
  P2 stored in all 908 analyses (largest difference 0.0).
* **Reference**: `x₀ = argmin E` over `X′` (P2's "argmin E"); known part `f` = ff14SB vacuum energy.
* **Deficits** `w_ij := max_{a≠x₀_i, b≠x₀_j} [c_ij − T_ij(a, b)]₊`, loads at most `Δ_i`.
* **Existence of shares**: maximum flow in the network source → pairs (`w_ij`) → their two
  sites → sink (`Δ_i`), my own Edmonds–Karp in exact rational arithmetic on the floating-point
  inputs.  Every certificate returned was re-verified by additions and comparisons only
  (`s ≥ 0`, `s_ij + s_ji ≥ w_ij`, `Σ_j s_ij ≤ Δ_i`, exact arithmetic); every refusal comes with an
  over-dense set `S` (`Σ_{i<j∈S} w_ij > Σ_{i∈S} Δ_i`, verified exactly) and agrees with brute force
  over all sets of sites (up to `2¹⁶`).
* **Exact criterion**: `x₀` minimises `L = f + g_star − Σ_{i<j changed} c_ij` over `X′`, by my
  enumeration; it agrees with P2's stored flag in all 908 analyses (as does P2's plain row-sum
  flag `½Σ_j c_ij ≤ Δ_i`).

**The 13.**  P2's output directory holds 184 analyses of `g_GB` with at least two sites (P2's
count of 181 leaves out three Ser₅ analyses at τ = 0.80; in all three the criterion fails): the
criterion holds in 110, P2's plain row-sum condition in 97 of them and in no other, which leaves
the 13 below.

**Headline table** (`g_GB`; "margin" = `min_{x≠x₀} L(x) − L(x₀)`; all energies kcal/mol):

| instance (τ) | states per site in `X′` | `min_i Δ_i` | margin of the exact criterion | row-sum condition, plain `c` (P2) | row-sum condition for the deficits | **share certificate 11.18b(d)** | if not: over-dense set, excess | state-dependent shares (§2.4) |
|---|---|---|---|---|---|---|---|---|
| Phe₂ / PPII (.70) | 2, 2 | 0.0673 | 0.0673 | fails | fails | **yes** | | |
| Phe₃ / PPII (.70) | 2, 2, 2 | 0.0079 | 0.0079 | fails | fails | **yes** | | |
| Phe₄ / strand (.60) | 4, 3, 3, 4 | 0.0430 | 0.0430 | fails | fails | **yes** | | |
| Phe₄ / helix (.60) | 5, 5, 4, 3 | 0.3784 | 0.0970 | fails | fails | **no** | sites {1, 2}: `w₁₂ = 1.113 > Δ₁ + Δ₂ = 1.077`, excess 0.036 | yes (slack 0.049) |
| Phe₄ / PPII (.70) | 1, 2, 2, 2 | 0.0379 | 0.0379 | fails | fails | **yes** | | |
| Phe₅ / strand (.60) | 4, 3, 1, 4, 4 | 0.0328 | 0.0328 | fails | fails | **yes** | | |
| Phe₅ / helix (.60) | 5, 5, 4, 3, 2 | 0.4436 | 0.2122 | fails | fails | **yes** | | |
| Phe₆ / strand (.60) | 4, 3, 1, 2, 4, 4 | 0.0412 | 0.0412 | fails | fails | **yes** | | |
| Phe₇ / strand (.60) | 4, 3, 1, 2, 2, 4, 4 | 0.0445 | 0.0445 | fails | fails | **yes** | | |
| Leu₁₄ / helix (.60) | 2 (14 sites) | 0.5266 | 0.5266 | fails | holds | **yes** | | |
| Leu₁₆ / helix (.60) | 2 (16 sites) | 0.5209 | 0.5209 | fails | holds | **yes** | | |
| Leu₅ / helix (.60) | 2 (5 sites) | 0.0007 | 0.0007 | fails | fails | **yes** | | |
| LKSE:2 / helix (.60) | 2, 31 | 0.4250 | 0.2877 | fails | fails | **no** | sites {1, 2}: `w₁₂ = 1.359 > 1.325`, excess 0.034 | yes (slack 0.144) |

**⇒ 11 of 13 certified; 2 of 13 by the split in halves.**  (P2's own state-wise variant of the
row-sum condition — the margin `rowsum_pairwise_margin` of its outputs, halves of
`max_b [c_ij − T_ij(a, b)]₊` charged to the state `a` — is nonnegative in the same two, Leu₁₄ and
Leu₁₆ on the helix.)

*Caveat on four of the thirteen (found in §2.5, not a property of the certificate).*  For Phe₄,
Phe₅, Phe₆, Phe₇ on the strand at τ = 0.60 the minimum of `E` over P2's pair-clash-free domain
`X_τ` is **not** in the pruned product `X′`: it lies 1.92, 10.45, 11.90, 13.20 kcal/mol below the
minimum that the star certifies on `X′`.

**All instances** (counts of analyses; "shares" = certificate of 11.18b(d) with deficits):

| residual | analyses | criterion holds | plain row-sum (`c`), P2's | row-sum for the deficits | shares | criterion holds, no shares | shares exist, criterion fails |
|---|---|---|---|---|---|---|---|
| `g_GB` | 184 | 110 | 97 | 91 | 106 | 4 | 0 |
| `coul + g_GB` | 180 | 145 | 132 | 112 | 119 | 26 | 0 |
| `g_03` | 184 | 156 | 119 | 84 | 120 | 36 | 0 |
| `g_ipq` | 180 | 155 | 145 | 109 | 126 | 29 | 0 |
| `g_99` (exactly additive, `c_ij ≤ 8·10⁻¹⁰`) | 180 | 180 | 180 | 103 | 125 | 55 | 0 |

`g_GB` by family (analyses / criterion / shares): Val 47 / 47 / 47; Leu 33 / 33 / 33; Phe 38 / 25 / 24;
Ser 33 / 2 / 0; Lys 18 / 0 / 0; LKSE 15 / 3 / 2.

*Readings.*
(i) For `g_GB` the certificate is nearly as good as the criterion (106 of 110), and the flow
matters: the split in halves certifies 91.
(ii) It is a statement about the *pair of* (known part, class), not about the class alone.
For `g_99` the constants vanish, the lower model is the energy itself, and the certificate
still fails in 55 of 180 analyses: the deficits are then the negative pair terms of the known
part, `w_ij = max[−T_ij]₊`, taken at the worst pair of states and charged against the cheapest
states (§2.4).  For `coul + g_GB`, `g_03` and `g_ipq` it certifies 82, 77 and 81 % of the
instances in which the criterion holds.
(iii) *P2's plain row-sum condition is not sufficient for a pairwise known part, on real
instances*: it holds while the criterion fails in 6 analyses of `g_03` (LKSE:4 and LKSE:5 on the
strand, Ser₂ and Ser₃ on the helix at both thresholds) and one of `g_ipq` (LKSE:6 on the helix);
never for `g_GB`.  The deficit version (the one that is a theorem) holds in no analysis in which
the criterion fails.  P2 said the plain condition is "a theorem only for an additive known
part"; this is the measurement that it is in fact violated as an implication.
(iv) *The polar and charged instances where the star fails* (Ser 31, Lys 18, LKSE 12 analyses;
one line per instance in `logs/p4_01b_tables.log`, table T3; all 908 rows in
`out/p4_01_shares.json`): no split exists in any of them, necessarily.  The excess of the densest set is 2.7–4.1
(Ser₂), 5–49 (Ser₃…₆), 14–274 (Lys), 6–230 (LKSE) kcal/mol — the "quadratic law" in the
form of a density.  The third-order test for these peptides is in §2.2 (Table 9 there).
(v) *A variant, not P2's constants* [M]: the proof of Theorem 11.16 visits only rectangles in
which one state of each site is the reference state.  With those "anchored" constants (smaller,
also valid at this `x₀`; `L ≤ E` checked at every state, smallest `E − L = −1.1·10⁻¹³`) the
criterion holds in 116 instead of 110 analyses of `g_GB` and shares exist in 114.

### 2.2 Item 2 — site form, pair form, mixed allocations, on P2's measured third-order constants [M]

**What was run.**  `g_GB`; all 136 instances with at least three sites that have more than one
state (3 to 16 sites; 21 of them beyond the eight sites to which P2 evaluated the ball);
`x₀ = argmin E` over `X′`; `c_T` = P2's measured third-order class constants (maxima over all
boxes of `X′`), recomputed with my routine and identical to P2's stored values (115 instances
with stored triples; `c3max`, `c3sum` in all).  Models `m = f + I₂g − penalty(S(x))`:

* **env3**: `Σ_{T⊆S} c_T` — the exact envelope of Theorem 11.18, a three-body function;
* **site**: `Σ_{i∈S} γ_i`, `γ_i = ⅓Σ_{T∋i} c_T`;   **pair**: `Σ_{i<j∈S} γ_ij`, `γ_ij = ⅓Σ_{T⊇{i,j}} c_T`;
* **LP-A / LP-B / LZ**: pair shares `μ_{T,p} ≥ 0`, `Σ_{p⊂T} μ_{T,p} = 1`, chosen to maximise the
  margin / to minimise the largest gap (linear programmes, one row per changed set, §2.3) / to
  minimise `ln Z(m)` (convex; L-BFGS on a softmax parametrisation, "best found");
* **CV-A / CV-B**: the same objectives over *all* penalties `(γ_i, γ_ij)` satisfying the `2ⁿ`
  covering inequalities of Theorem 11.18a(b) (instances with at most 10 multi-state sites: 123).

**Soundness.**  `m ≤ E` at every state of every instance for every model: smallest value of
`E − m` over 1 023 (instance, model) pairs `−1.1·10⁻¹³` kcal/mol (rounding).  Pointwise order
`site ≤ pair ≤ env3` at every state of all 136 instances.

**(a) Does the reference minimise the lower model?**

| family | instances | env3 | pair | site | pair shares by LP-A | pair yes, site no | env3 yes, pair no |
|---|---|---|---|---|---|---|---|
| all | 136 | 133 | 132 | 113 | 120 of 123 | 19 | 1 |
| Ser | 27 | 27 | 27 | 23 | 27 of 27 | 4 | 0 |
| Lys | 12 | 9 | 9 | 8 | 9 of 12 | 1 | 0 |
| LKSE | 12 | 12 | 11 | 3 | 12 of 12 | 8 | 1 |
| Val | 32 | 32 | 32 | 32 | 28 of 28 | 0 | 0 |
| Leu | 30 | 30 | 30 | 29 | 21 of 21 | 1 | 0 |
| Phe | 23 | 23 | 23 | 18 | 23 of 23 | 5 | 0 |

The three instances in which not even the envelope certifies are P2's three (Lys₃ and Lys₄ on
the helix, Lys₄ on PPII, all at τ = 0.60: margins −0.137, −0.188, −6.72) — replication of P2's
Statement 5(c); beyond eight sites (Val₁₀, Val₁₂, Leu₁₀…₁₆, Phe₁₀ on the helix; 21 instances, new) the envelope and
both pairwise forms certify everywhere.  The pair form fails where the envelope succeeds once
(LKSE:6 on PPII, τ = 0.60: margin −0.054 against +0.010), and there the LP over pair shares
recovers the envelope's margin.  The 19 instances rescued by the pair form: Phe₃…Phe₇ on PPII
(.60), Lys₄ on the strand (.60; site −0.159, pair +0.623), Leu₅ on the helix, LKSE:4, 5 on all
three backbones and LKSE:6 on strand and helix (.60), Ser₃ on the helix (both thresholds), Ser₅
and Ser₆ on the helix (.60).  `margin(pair) − margin(site)`: 0.0003 to 0.94, median 0.012.

**(b) `ln Z(m) − ln Z(E)`, nats** (= `ln(1 + cost number)`; instances with a non-zero envelope value):

| family | instances | env3: median (max) | pair: median (max) | site: median (max) | site / pair: median (range) | pair / env3: median | LZ / pair: median (range) |
|---|---|---|---|---|---|---|---|
| all | 122 | `2.6·10⁻⁴` (14.5) | `2.9·10⁻³` (14.7) | `2.0·10⁻²` (15.3) | **6.8** (1.0–137) | 7.8 | 0.82 (0.00–1.00) |
| Ser | 27 | `5.7·10⁻³` (0.79) | `8.5·10⁻³` (1.16) | `1.3·10⁻²` (1.78) | 1.8 (1.5–4.1) | 1.7 | 0.92 (0.76–0.98) |
| Lys | 12 | `1.2·10⁻²` (14.5) | `5.1·10⁻²` (14.7) | 0.26 (15.3) | 4.7 (1.0–10.1) | 4.3 | 0.78 (0.39–0.99) |
| LKSE | 11 | `1.9·10⁻²` (0.15) | `8.6·10⁻²` (0.52) | 0.28 (1.78) | 3.7 (2.3–7.4) | 4.3 | 0.38 (0.09–0.71) |
| Val | 32 | `7.9·10⁻⁶` (`1.2·10⁻³`) | `8.4·10⁻⁵` (`8.2·10⁻³`) | `1.3·10⁻³` (`4.9·10⁻²`) | 41 (6.0–96) | 39 | 0.97 (0.74–1.00) |
| Leu | 19 | `9.5·10⁻⁶` (`1.6·10⁻⁵`) | `4.1·10⁻⁴` (`3.4·10⁻³`) | `1.5·10⁻²` (0.28) | 40 (11–82) | 40 | 1.00 (0.06–1.00) |
| Phe | 21 | `3.0·10⁻⁷` (`7.5·10⁻⁴`) | `8.5·10⁻³` (`1.5·10⁻²`) | `3.8·10⁻²` (0.14) | 7.9 (4.5–137) | `1.0·10⁴` | 0.04 (0.00–0.67) |

Cost number `Z(m)/Z(E) − 1` (all 136): median `8.2·10⁻⁵` / `2.3·10⁻³` / `1.6·10⁻²` for env3 / pair /
site; above 1 in 3 / 4 / 10 instances; below 0.01 in 112 / 98 / 58.  Why the factor is largest for
the apolar chains: their Gibbs weight sits on configurations with one or two changed sites,
where the site form charges `γ_i` per changed site, the pair form nothing for one and `γ_ij` for
two, the envelope nothing.

**(c) Largest gap `max_x (E − m)`**: the same for env3, pair and site (to `10⁻⁹`) in 129 of 136
instances.  Where every site is changed the three penalties coincide (`Σ_i γ_i = Σ_{i<j} γ_ij =
Σ_T c_T`), and that is where the largest gap is: a state of largest gap has every multi-state
site changed in 134 / 132 / 129 of the 136 instances for env3 / pair / site.  It is the wrong
quantity for comparing the forms.  (The seven exceptions are small Phe and Leu instances with gaps below 0.25.)

**(d) Does a mixed allocation do better still?**  For the minimum: hardly.  With equal thirds
the margin of the pair model already equals that of the three-body envelope in 134 of 136
instances (the binding configuration has one changed site, where neither charges anything);
optimal pair shares (LP-A) reach the envelope's margin in all 123 instances where the LP was
run, changing the value in two (Lys₄ on the helix, .60: −0.706 → −0.188, still negative; LKSE:6
on PPII, .60: −0.054 → +0.010, a certificate).  That equality is an observation, not a theorem
(`p4_03_review.py`, block A: three sites with two changed states each, each pair of sites cheap
in one combination of states only and the three combinations excluding one another, one triple
with `c = 1`: single, double and triple excitations at 1, 0.5 and 1.5; margin of the envelope
0.5, best margin over pair shares ⅙).  For the largest gap LP-B
improves on thirds in 1 of 123 instances (by `10⁻³`).  For `ln Z` the best shares found reduce
the excess of the equal split by the factor in the last column of the table (0.82 in the
median; 0.38 for LKSE, 0.04 for Phe — where one site has an excitation energy of 0.03–0.04, so
that the penalty on its pairs carries most of the excess [H]).  Optimising over all coverings instead of shares (CV-A)
never raised the margin (0 of 123), although coverings are a strictly larger set (Example P4.3).

**(e) The LP that matters: shares and certificate together, without enumeration**
(`p4_08_joint.py`).  The pair shares `μ_{T,p}` of the triples and the state-dependent shares
`s_ij(a)` of Proposition P4.1 enter the cover constraints linearly and together:
`s_ij(a) + s_ji(b) ≥ Σ_{T⊇{i,j}} c_T μ_{T,ij} − (T_ij + D_ij)(a, b)`, `Σ_j s_ij(a) ≤ A_i(a)`, `Σ_p μ_{T,p} = 1`.
One LP with `O(n²k + n³)` variables and `O(n²k²)` rows (at most 2 161 and 4 996 here), whose inputs
are the ball data and the constants only, therefore searches for a certificate checked by
additions.  Result: an **exactly verified certificate exists in 133 of the 136 instances —
precisely those in which the three-body envelope certifies** — against 132 with equal thirds
(the gain is LKSE:6 on PPII, exact slack 0.0102 = the envelope's margin).  Each accepted
solution was made exact (shares completed to at least one, pair penalties rounded up, state
shares repaired, loads compared in rational arithmetic) and the model was rebuilt on the grid
(`m ≤ E`, reference minimises: confirmed by enumeration in all 133).

**Selected instances** (those of P2's table 5(c) except Lys₃ on the strand, and three more: Leu₁₆/H, Val₁₂/P2, LKSE:6/E):

| instance | `X′` | `Σ c_T` / `max c_T` | margin env3 / pair / site | `ln Z(m) − ln Z(E)`: env3 / pair / site / LZ | cost number pair / site | shares 11.18b(c): pair / site |
|---|---|---|---|---|---|---|
| Ser₆, E (.70) | 531 441 | 0.022 / 0.0043 | 1.024 / 1.024 / 1.023 | `5.3·10⁻⁴` / `2.2·10⁻³` / `8.9·10⁻³` / `2.1·10⁻³` | `2.2·10⁻³` / `8.9·10⁻³` | yes / yes |
| Ser₆, P2 (.70) | 531 441 | 0.017 / 0.0027 | 0.420 / 0.420 / 0.418 | `8.5·10⁻³` / `1.3·10⁻²` / `1.9·10⁻²` / `1.2·10⁻²` | `1.3·10⁻²` / `1.9·10⁻²` | yes / yes |
| Ser₆, H (.70) | 104 976 | 0.230 / 0.054 | 0.127 / 0.127 / 0.104 | 0.068 / 0.12 / 0.21 / 0.095 | 0.13 / 0.24 | no / no |
| Ser₆, H (.60) | 531 441 | 1.75 / 0.20 | 0.127 / 0.127 / −0.272 | 0.79 / 1.2 / 1.8 / 1.0 | 2.2 / 4.9 | no / no |
| Val₈, E (.70) | 6 561 | 0.048 / 0.0059 | 2.468 / 2.468 / 2.465 | `1.1·10⁻⁷` / `8.8·10⁻⁶` / `8.1·10⁻⁴` / `8.8·10⁻⁶` | `8.8·10⁻⁶` / `8.1·10⁻⁴` | yes / yes |
| Leu₈, H (.60) | 256 | 1.23 / 0.069 | 0.619 / 0.619 / 0.478 | `1.1·10⁻⁵` / `2.4·10⁻³` / 0.11 / `1.4·10⁻⁴` | `2.4·10⁻³` / 0.12 | yes / yes |
| Leu₁₆, H (.60) | 65 536 | 7.45 / 0.086 | 0.521 / 0.521 / 0.205 | `1.5·10⁻⁵` / `3.4·10⁻³` / 0.28 / — | `3.4·10⁻³` / 0.33 | yes / yes |
| Val₁₂, P2 (.70) | 531 441 | 0.163 / 0.0064 | 0.886 / 0.886 / 0.870 | `1.2·10⁻³` / `8.2·10⁻³` / `4.9·10⁻²` / — | `8.2·10⁻³` / `5.1·10⁻²` | yes / yes |
| Phe₇, P2 (.60) | 112 500 | 1.01 / 0.088 | 0.032 / 0.032 / −0.055 | `5.9·10⁻⁴` / `1.1·10⁻²` / 0.14 / `1.4·10⁻³` | `1.1·10⁻²` / 0.15 | yes / no |
| Lys₄, H (.70) | 16 464 | 0.251 / 0.144 | 0.461 / 0.461 / 0.383 | `7.8·10⁻³` / `3.1·10⁻²` / 0.12 / `2.4·10⁻²` | `3.1·10⁻²` / 0.13 | yes / yes |
| Lys₄, E (.70) | 74 529 | 0.530 / 0.193 | 1.243 / 1.243 / 1.111 | `9.6·10⁻⁴` / `1.0·10⁻²` / 0.11 / `6.7·10⁻³` | `1.1·10⁻²` / 0.11 | yes / yes |
| Lys₄, P2 (.70) | 194 481 | 2.97 / 2.39 | 0.975 / 0.975 / 0.031 | 0.17 / 0.36 / 1.3 / 0.29 | 0.43 / 2.8 | no / no |
| Lys₄, E (.60) | 450 225 | 2.62 / 1.05 | 0.623 / 0.623 / −0.159 | 0.032 / 0.18 / 1.1 / 0.068 | 0.19 / 1.9 | no / no |
| Lys₄, H (.60) | 353 220 | 4.08 / 1.90 | −0.188 / −0.706 / −1.435 | 1.1 / 1.6 / 3.0 / 1.3 | 4.1 / 20 | no / no |
| Lys₄, P2 (.60) | 783 000 | 13.4 / 10.2 | −6.72 / −6.72 / −7.41 | 14.5 / 14.7 / 15.3 / 14.5 | `2.4·10⁶` / `4.4·10⁶` | no / no |
| LKSE:5, H (.60) | 14 508 | 1.53 / 0.46 | 0.037 / 0.037 / −0.250 | 0.049 / 0.20 / 0.79 / 0.080 | 0.23 / 1.2 | no / no |
| LKSE:6, H (.60) | 217 152 | 3.42 / 0.71 | 0.162 / 0.162 / −0.682 | 0.085 / 0.44 / 1.8 / 0.15 | 0.55 / 4.9 | no / no |
| LKSE:6, P2 (.60) | 622 728 | 2.20 / 0.45 | 0.010 / −0.054 / −0.747 | 0.15 / 0.52 / 1.5 / 0.19 | 0.69 / 3.6 | no / no |
| LKSE:6, E (.60) | 341 172 | 0.58 / 0.15 | 0.038 / 0.038 / −0.121 | 0.013 / 0.063 / 0.28 / 0.024 | 0.065 / 0.32 | no / no |

**Table 9 — the share certificates of Proposition 11.18b(c)/(d) on the third-order models**
(deficits `w_ij = max[γ_ij − T_ij − D_ij]₊`, loads at most `Δ_i − γ_i`; flow and exact verification
as in §2.1):

| family | instances | pair form: reference minimises | … shares exist | … split in halves | … state-dependent shares | site form: reference minimises | … shares exist | … state-dependent shares |
|---|---|---|---|---|---|---|---|---|
| all | 136 | 132 | 110 | 92 | 132 | 113 | 104 | 113 |
| Ser | 27 | 27 | 18 | 18 | 27 | 23 | 18 | 23 |
| Lys | 12 | 9 | 6 | 6 | 9 | 8 | 6 | 8 |
| LKSE | 12 | 11 | 1 | 1 | 11 | 3 | 1 | 3 |
| Val | 32 | 32 | 32 | 32 | 32 | 32 | 32 | 32 |
| Leu | 30 | 30 | 30 | 29 | 30 | 29 | 29 | 29 |
| Phe | 23 | 23 | 23 | 6 | 23 | 18 | 18 | 18 |

So for the polar and charged peptides — where the ball certifies and the star does not — the
split of the deficits of Proposition 11.18b(c) exists in 25 of the 47 instances in which the
pair model certifies: all of serine on strand and PPII, none of serine on the helix (9), 6 of 9
lysine, 1 of 11 LKSE.  The cause is not the penalties (`γ_ij ≤ 0.2` for Ser, ≤ 0.5 for LKSE,
≤ 4.2 for Lys) but `−(T_ij + D_ij)`: the second difference of the *full energy* at the reference
is strongly negative for some pairs of states (largest deficits 0.28–1.87 for Ser, 0.57–5.9 for
LKSE, up to 43.0 for Lys — two rotamers that are each expensive against the reference and much
less so together), while the loads are bounded by the *cheapest* excitations (0.003–1.2).  With
shares that may depend on the state (§2.4) all 132 are certified.

### 2.3 Theorem 11.18a — review

**(a), (b)** correct [V for them; review and replication here].  Re-derivation: `I₂g(x) =
Σ_{U⊆S(x), |U|≤2} (mixed difference of g at x₀ over U with targets x)`; a mixed difference with an
unchanged site vanishes, so the sum over all pairs equals the sum over changed pairs, and every
term depends on at most two states.  (b) is Theorem 11.18 at `m = 3` followed by the covering
inequality at `S = S(x)`.  The Lean statements say this and no more: `HigherDiffBound 3 g c` is
the bound over *all* boxes (all base points, all pairs of states) — the same constant P2
measured; `thirdOrderLowerModel` puts `pairIncrement/2 − γ₂/2·[both changed]` on ordered pairs,
`PairModel.energy` sums ordered pairs; `hcover` is required for every `Finset S`;
`verify_sound_thirdOrder` concludes `L + g(x₀) ≤ M.energy x + g x` on the box of the certificate.
No hypothesis of the report is missing in Lean and none is added (`thirdOrder_pairwise_lower`
does not even use `c_T ≥ 0`; the two rules of thirds do).

**(c)** correct; two sentences to repair.
(i) *"at a single triple both are exact (`thirdOrder_witness`)"*.  The witness is the equality
at the configuration `(1, 1, 1)`.  With one triple and one changed site the site form charges
`c_T/3`, with two changed sites the pair form charges `c_T/3`, and the envelope charges nothing
in either case; so neither form is the envelope even for a single triple.  Proposed wording:
"where all three sites of a triple are changed both forms charge exactly `c_T`".
(ii) *"There is a tighter one at the same cost"* (THY-RES-0009 §1).  The same number of
evaluations, yes.  Not the same interaction graph: the site form adds nothing to the pair
tables, the pair form adds a term on every pair that lies in a triple with `c_T > 0`.  Where
the lower model must stay banded or of small treewidth — the remark "lower models" of §11.30,
and P3's sandwich — the pair penalty of an out-of-band pair has to be charged to its two sites;
the result is still pointwise at least as tight as the site form (Proposition P4.6, §2.6).

**(d)** correct [P; attainment replicated by LP over the class].  Three additions.

**Lemma P4.2 [P, mine]** (*site shares are never useful*).  Let each triple `T` have
nonnegative shares `λ_{T,i}` (its sites) and `μ_{T,p}` (its pairs) adding up to one.  Moving a
site share `λ_{T,i}` to any pair `p ∋ i` of `T` leaves the covering valid and does not increase
the penalty at any set `S`: the charge of `T` at `S` changes by `−λ_{T,i}[i ∈ S][p ⊄ S] ≤ 0`.
So among share allocations the pure pair allocations are pointwise optimal, the equal split
`⅓` is one of them, and "the best shares" is a programme over `3·C(n,3)` pair shares.

*The size of that programme.*  The penalty depends on `x` only through `S(x)`.  With
`B(S) := min{(f + I₂g)(x) − (f + I₂g)(x₀) : S(x) = S}`, maximising the margin over pair shares is
the LP `max t : B(S) − Σ_{T⊆S} c_T − Σ_{T: |T∩S|=2} c_T μ_{T, T∩S} ≥ t` for all `S ≠ ∅` — `2ⁿ − 1` rows,
each right-hand side a pairwise minimisation.  "A linear programme for the producer" is
accurate; it is not of polynomial size in general.

**Example P4.3 [P, checked by brute force]** (*coverings are more than shares*).  Four sites,
`c_{012} = c_{013} = 1`, the other two triples 0.  The penalties `γ₀₁ = γ₂₃ = 1` (all others 0)
satisfy the covering inequality of (b) at all 16 sets.  They are not a sum of shares (the pair
{2, 3} lies in neither triple), and no share-based covering is below them at every set: the
penalties of the five two-site sets other than {2, 3} add up to 1 here, to exactly 2 for every
allocation of pair shares, and to at least 2 when site shares are used as well.  So `thirdOrder_pairwise_lower` [V] covers lower models that no triple-by-triple
check certifies; verifying such a covering takes the `2ⁿ` inequalities (or another certificate).
On our 123 instances this extra freedom never improved the margin (§2.2(d)).

### 2.4 Proposition 11.18b — review

**(a)** correct [V].  Lean: `hJ` (zero pair tables of the known part), symmetric `c`, shares
`s ≥ 0` with `c i k ≤ s i k + s k i` for `i ≠ k`, load `Σ_{k≠i} s i k ≤` every single-site excitation
energy of `M.energy + g` at `i`; conclusion for every `g′` of `SecondOrderClass g c x₀`.  This is
the report's sentence.  (`c ≥ 0` is needed only for the row-sum corollary, and is there.)

**(b)** correct [P; re-derived].  For an additive known part
`L(x) − L(x₀) = Σ_{i∈S} A_i(x_i) − Σ_{i<j∈S} c_ij`; on a product the minimum over the states with
changed set `S` is `Σ_{i∈S} Δ_i − Σ_{i<j∈S} c_ij` for every alphabet size (a site with one state is
in no `S`; `Δ_i = +∞` does that).  In the network source → pairs → sites → sink a finite cut is a
set `S` of sites together with the pairs inside it, of capacity `Σ_{all} c − Σ_{i<j∈S} c_ij +
Σ_{i∈S} Δ_i`; so all pair arcs can be saturated iff no `S` is over-dense.  Needs `c ≥ 0` (as
Theorem 11.17 does) and gives `Δ_i ≥ 0` from `S = {i}`.  **The sentence "the constants do not
depend on the states, so the worst state of a site is its cheapest one" uses that the cheapest
states of the sites of `S` can be chosen together — a product.**  On a reset-closed domain that
is not a product it fails (Counterexample P4.4).  Tested: 1 500 random instances with 1 to 4
states per site, integer data in half of them (135 exact ties, 221 instances with a negative
`Δ_i`): enumeration, over-dense test and flow agree in all.  The three citations are "from
memory" in the report; I did not check them.

**(c)** correct [P; replicated].  The identity behind the first sentence:
`L₃(x) − L₃(x₀) = Σ_{i∈S} [A_i(x_i) − γ_i] + Σ_{i<j∈S} [M^E_ij(x_i, x_j) − γ_ij]`, where
`M^E_ij = T_ij + D_ij` is the second difference of the *full energy* at the reference — which is
why the deficits of the third-order models are dominated by the measured pair structure of
`E` and not by the penalties (Table 9).  Triples: site shares with loads at most `Δ_i` ⇔ no set
over-dense w.r.t. the triples ⇔ `x₀` minimises `Σ A_i − Σ_{T⊆S} c_T` (400 random instances, all
agree); given attainment at `m = 3` (replicated by LP) this is the exact criterion when the
pair terms vanish, as stated.

**(d)** correct; its list of reasons for non-necessity is incomplete, and the missing reason
is the one that occurs in practice.

*Three mechanisms.*  (1) the worst states of different pairs need not be compatible
(theirs); (2) pair terms of the known part that help are discarded (theirs; e.g. three binary
sites, `A_i = 1`, `T₀₁ = T₁₂ = −1.8`, `T₀₂ = +10`, `c = 0`: margin 0.2, deficits 1.8, 1.8, 0, set
{0, 1, 2} over-dense by 0.6); (3) **within a single pair, the pair of states that realises the
deficit need not consist of the cheapest states of its two sites**: the certificate compares
`max_{a,b}[c_ij − T_ij(a, b)]₊` with `min_a A_i(a) + min_b A_j(b)`.  Two sites with three states,
`A = (0, 1, 5)` twice, `T(2, 2) = −4`, `c = 1`: margin 1, deficit 5 against `Δ₁ + Δ₂ = 2`.  **All
four analyses of `g_GB` in which the criterion holds and the certificate fails are of kind (3)
at one pair**: Phe₄/H (1.113 against 1.077), LKSE:2/H (1.359 against 1.325), Ser₂/E at both
thresholds (2.155 against 2.122, margin 0.686; `c₁₂ = 1.31`).  These are the instances the brief
asked for.

**Proposition P4.1 [P, mine; the mathematics is the linear-programming duality of pairwise
energy minimisation, which is known — K, from memory, unverified: Schlesinger's dual,
reparametrisations, soft arc consistency in cost-function networks].**  *State-dependent
shares.*  Let `s_ij(a) ≥ 0` be defined for every ordered pair of sites and every changed state
`a` of `i`, with

    s_ij(a) + s_ji(b) ≥ c_ij − T_ij(a, b)   (a ≠ x₀_i, b ≠ x₀_j),      Σ_{j≠i} s_ij(a) ≤ A_i(a)   (a ≠ x₀_i).

Then `x₀` minimises `L`.  (i) *Proof*: `L(x) − L(x₀) = Σ_{i∈S} [A_i(x_i) − Σ_{j∈S∖i} s_ij(x_i)] +
Σ_{i<j∈S} [T_ij − c_ij + s_ij(x_i) + s_ji(x_j)] ≥ 0`.  (ii) Constant shares `s_ij(a) = s_ij` are the
certificate of 11.18b(d), so this one is never weaker; it costs `O(n²k)` numbers, `O(n²k²)`
additions to check, and a linear programme (not a single flow) to find.  (iii) *Such shares
exist iff `x₀` is an optimal solution of the pairwise (local-polytope) linear relaxation of
`min L`*: they are exactly a dual solution complementary to `x₀` (messages normalised to zero at
the reference state; the constraint `s ≥ 0` is dual feasibility at the pairs "one state
changed, one not").  So the certificate is complete precisely when that relaxation is tight at
`x₀`; any certificate that redistributes pair terms onto the states of their sites reduces to
this one after normalisation.
*Tested* [N]: 300 random instances, "shares exist" = "relaxation attains its minimum at `x₀`"
in all (173; the criterion holds in 177, constant shares exist in 131).
*Measured* [M] (LP by HiGHS; each accepted certificate then repaired and verified in exact
arithmetic; smallest exact slack 0.0074 at second order, 0.0025 at third): state-dependent shares certify **all 13**, all 110
analyses of `g_GB` in which the criterion holds, all 145 of `coul + g_GB`, 155 of 155 for `g_ipq`,
154 of 156 for `g_03` (not: Ser₆ on the strand at both thresholds), 177 of 180 for `g_99`, and all
132 + 113 third-order models of Table 9.  The five failures are integrality gaps of the
relaxation.

### 2.5 Proposition 11.18c — review

**(a) "On a reset-closed domain nothing changes" — correct for the bounds, wrong for the
completeness part of Proposition 11.18b.**

*What is correct* [P; re-derived].  The telescoping proof of Theorem 11.16 uses, for `x` with
changed sites `i₁, …, i_m`, the rectangles with corners `y_{l−1}`, `y_l`, `y_{l−1}^{+i_k}`, `y_l^{+i_k}`
(`y_l` = `x` on `{i₁…i_l}`, reference elsewhere): resets of `x`, as stated.  The induction of
Theorem 11.18 goes through as well: `D_j h` is defined on `{z : (z, x_j) ∈ D}`, which is
reset-closed, and a box `B` there gives the box `B × {x₀_j, x_j} ⊆ D`; the interpolant has no
differences of order `m` over boxes inside `D` because each of its terms is a function of fewer
than `m` sites that is defined wherever it is needed (by reset-closedness).  The extremal
members `g_star ∓ Σ c_ij`, `I₂g ∓ Σ c_T` restricted to `D` belong to the class on `D`, so Theorem
11.17 (which the list in (a) omits) and the attainment in 11.18 hold on `D` too.  Hence all
*sound* directions carry over: 11.16, 11.17, 11.18, 11.18a(a)–(d), 11.18b(a), 11.18b(d), and
"shares ⇒ no over-dense set ⇒ `x₀` minimises `L` on `D`".
*Replication.*  60 random domains with pairwise exclusions: second- and third-order bounds at
all 889 points of `D′` with constants over boxes inside `D′` only (smaller than the product
constants in 55 of 60), no violation, equality attained at 73 and 62 points.  **Real domains**
[M]: for the 40 analyses of `g_GB` whose clash-free domain `X_τ` is not a product, the bound
`|g − g_star| ≤ Σ c_ij` with constants over the rectangles inside `D′` holds at every state of
`D′(x₀)` and of `D′(x*)` (80 domains of up to 898 619 states; smallest slack `−3.6·10⁻¹⁵`).

**Counterexample P4.4 [P; checked by enumeration, flow and an LP over the class]** (*the "iff"
of 11.18b(b) fails on a reset-closed domain that is not a product*).  Two sites with states
{0, 1, 2}, `x₀ = (0, 0)`, `D` = the product minus the pair of states `(1, 1)`.  `D` is reset-closed.
Additive known part with excitation energies `A₁ = A₂ = (0, 1, 10)`; zero star data for the
residual; class constant `c₁₂ = 3` (over the rectangles inside `D`).  The least member of the class
on `D` with these star data is `−3·[both changed]` (LP over the class at every point of `D`:
reproduced to 0.0), so `L − L(x₀)` on `D` is 1 or 10 at the four star points, `1 + 10 − 3 = 8` at
`(1, 2)` and `(2, 1)`, 17 at `(2, 2)`: **`x₀` minimises `E₀ + g′` for every member `g′`**.  But
`Δ₁ + Δ₂ = 2 < 3 = c₁₂`: the set {1, 2} is over-dense and no shares exist.  The two cheapest states
cannot be taken together.  *Repair*: in (a) replace "Proposition 11.18b" by "the sufficient
directions of Proposition 11.18b"; on a non-product `D` the exact criterion is the minimisation
of `L` over `D`, and the state-dependent shares of P4.1 (with the cover constraints imposed for
jointly admissible pairs of states only) are the natural certificate.

**(b) correct** [P; re-derived; replicated: on 60 random domains the formula for `D′` equals the
largest reset-closed part computed by brute force; `D` itself not reset-closed in 49].

*The sentence about our measurement.*  "In the division's measurement the theorems were applied
'on greedily pruned clash-free products' — covered by (b) — and what the pruning discards is the
set that (c) is about."  The first half is right: P2's `X′` is a product inside `X_τ` that
contains `x₀`.  The second half is not what P2's domains are.  Measured on the 40 analyses of
`g_GB` with a non-product `X_τ` (Phe 26, Lys 10, LKSE 4; `x₀` = P2's reference, `x*` = the
minimiser of `E` over `X_τ`):

* `X′ = D′(x₀)` in 6; `X′` is strictly smaller in 34 (`|X′|/|D′(x₀)|`: 0.44 to 1, median 0.79);
  `D′(x₀) = X_τ` — nothing of the kind (c) is about — in 16.  So the pruning mostly discards
  configurations that star and ball data at `x₀` *can* reach.
* It matters.  `x₀` is the minimiser of `E` over `D′(x₀)` in 28 of 40 and over `X_τ` in 26 of 40.
  In the other 14 the minimum over P2's own clash-free domain lies outside the pruned product,
  by 0.03 to 13.2 kcal/mol: Phe₄…Phe₈ on the strand at τ = 0.60 by 1.92, 10.45, 11.90, 13.20, 13.25
  (for Phe₅, Phe₆, Phe₇ I looked at the state: the uniform assignment "state 3 at every site",
  two-site clash score 0.93; the greedy rule removes that state at interior sites, presumably
  because it clashes with many states of the neighbours [H]), Phe₄ on the strand at 0.70 (1.92), Phe₅…Phe₇ on PPII at 0.70 (0.03, 1.47, 2.68), Lys₃,
  Lys₄ on the strand at 0.70 (0.74, 1.33), LKSE:4…6 on the strand (1.2–1.3).  In 9 of these 14 P2 reports
  the star as an exact certificate (on `X′`, where it is one); four of them are among the 13.
* *Third order on these domains* [M] (`p4_07_dprime3.py`; the 34 analyses with at least three
  sites that can change inside `D′(x*)`; constants over the boxes inside `D′(x*)`): the remainder
  bound of Theorem 11.18 and `m ≤ E` for the envelope, the pair form and the site form hold at
  every state of every domain (up to 898 619 states; smallest slack `−1.1·10⁻¹³`) — Proposition
  11.18c(a) for Theorems 11.18 and 11.18a on real non-product domains.  `x*` minimises the
  envelope and the pair-form model over `D′(x*)` in 30 of 34 (Phe 22 of 22, LKSE 4 of 4, Lys 4 of
  8), the site-form model in 22.  The four failures are poly-Lys at τ = 0.60: the three of P2 and
  **Lys₄ on the strand**, which the ball certifies on the pruned product (450 225 states,
  `max c_T` = 1.05, margin 0.62) and not on `D′(x*)` (698 896 states, `max c_T` = 3.78, margin
  −7.7): P2's "exact in all but three poly-Lys instances" is a statement about `X′`.
* *What (b) offers instead* [M]: choose the reference first, then the domain.  With `x*` and
  `D′(x*)` (21–100 % of `X_τ`, median 86 %) the star with constants over the rectangles inside
  `D′(x*)` certifies the true minimum of `X_τ` over `D′(x*)` in 13 of the 40 analyses, all Phe;
  for Phe₄…Phe₈ on the strand with margins of 1.97 kcal/mol (on `X′`: 0.03–0.04 for Phe₄…Phe₇
  and 0.62 for Phe₈, for a minimum that is 2–13 kcal/mol too high).  With P2's `x₀` the star certifies on `D′(x₀)` in 6
  of the 14 analyses in which it certifies on `X′`.

P2 stated the limitation in general terms (its Statement 9(iii): "a certificate over `X′` says
nothing about `X_τ ∖ X′`"); it does not report where the minimum over `X_τ` is, and its verdict that
one star is an exact certificate for poly-Phe on the strand is about a sub-domain that does not
contain that minimum.
This is a correction of emphasis for our own report, not of any number in it.

**(c) correct** [P], and the example is an instance of a general fact:

**Proposition P4.5 [P, mine; replicated by LP]** (*outside `D′` the class says nothing*).  Let
`D` be a product minus forbidden pairs of states, `x₀ ∈ D`, and `x ∈ D ∖ D′`.  For every function
`g` on `D`, every order `m ≥ 2` and all constants, the class of functions on `D` that have the
same mixed-difference bounds of order `m` as `g` and agree with `g` **at every point of `D′`**
contains members with arbitrarily low value at `x`.  *Proof.*  `x` has a changed state `a` at
some site `i` that clashes with the reference state of another site; no point of `D′` carries
`a` at `i`; so `φ(y) = t·[y_i = a]` vanishes on `D′`, is a function of one site (all mixed
differences of order ≥ 2 vanish), and `g + φ` takes the value `g(x) + t` at `x`. ∎  So "what star
and ball data at `x₀` can certify is the minimum over `D′`" is exact, and no amount of data
inside `D′` helps.  (LP check: 41 points of `D ∖ D′` in random domains, all values on `D′` fixed,
the constants of `g` itself: unbounded below at 41 of 41.)

### 2.6 Item 4 — the pair form at order `m` and P3's certified sandwich

**Proposition P4.6 [P, mine; checked at every state of the runs below].**  Let `ĉ_T ≥ 0`,
`|T| = m ≥ 2`, bound the remainder as in P3's Theorem 5: `|g − I_{m−1}g| ≤ Σ_{T⊆S(x)} ĉ_T`.
(i) Any nonnegative shares of each `ĉ_T` among its `m` sites and its `C(m, 2)` pairs that add up
to one give penalties `γ_i`, `γ_ij` with `Σ_{T⊆S} ĉ_T ≤ Σ_{i∈S} γ_i + Σ_{i<j∈S} γ_ij` for every `S`.
(ii) *Pair form*: `γ_ij = Σ_{T⊇{i,j}} ĉ_T / C(m, 2)`.  A subset with `t` changed sites is charged
`ĉ_T·t(t−1)/(m(m−1))` against `ĉ_T·t/m` in the site form `γ_i = (1/m)Σ_{T∋i} ĉ_T`: never more,
strictly less for `0 < t < m`.  (iii) *Banded pair form* for band width `w`: pairs of `T` with
`|i − j| ≤ w` keep their share as a pair penalty, the share of every other pair goes in halves
to its two sites.  The model then has pair terms of separation at most `w` only (P3's exact
transfer-matrix evaluation still applies), and the charge is pointwise between the pair form
and the site form: a changed site `i ∈ T` is charged at most `(m − 1)·½/C(m, 2) = 1/m`.
(More generally the shares may go to the `k`-subsets of `T`, with charge `C(t, k)/C(m, k)`,
decreasing in `k`; `k = m − 1` is the tightest that keeps the order of the model.)

**Runs** [M for the grids, P3's certified constants re-run].  Constants `ĉ_T` from P3's code,
unchanged (`gfbound.GFBound.total(m, T)`, anchored mode, at the anchor `x₀ = argmin E`; they sum
to P3's `Γ_m`, and my site penalties reproduce the vector P3 quotes for Val₆/E, `m = 4`:
largest `γ_i` = 0.0992, cost number 0.0081 against P3's "0.008"); `f`, `g_GB` on P2's grid;
floor `f + I_{m−1}g − penalty`, without P3's band reductions of the pair terms (the same for all
forms); `w = 2`.  `m ≤ E` at every state in every run; P3's certified remainder bound holds on
every grid.

| instance, `m` | `Γ_m = Σ ĉ_T` | `ln Z(floor) − ln Z(E)`: `m`-body envelope / **site form (P3)** / **pair form** / banded pair form | cost number: site → pair (banded) | reference minimises: site / pair |
|---|---|---|---|---|
| Val₆, E (.70), 3 | 12.96 | 0.0115 / **2.857** / **0.0623** / 0.146 | 16.4 → 0.064 (0.157) | no / yes |
| Val₆, E (.70), 4 | 0.432 | `1·10⁻⁸` / **0.00811** / **0.000087** / 0.00194 | 0.0081 → 0.000087 (0.0019) | yes / yes |
| Ser₄, E (.70), 3 | 0.729 | 0.029 / 0.350 / 0.097 / 0.113 | 0.42 → 0.10 (0.12) | yes / yes |
| Ser₆, E (.70), 3 | 2.26 | 0.105 / **1.192** / **0.352** / 0.483 | 2.29 → 0.42 (0.62) | yes / yes |
| Ser₆, E (.70), 4 | 0.0418 | 0.00026 / 0.0172 / 0.0042 / 0.0077 | 0.0174 → 0.0043 (0.0077) | yes / yes |
| Phe₄, E (.60), 3 | 8.73 | `1·10⁻⁶` / **2.939** / **0.0399** / 0.632 | 17.9 → 0.041 (0.88) | no / yes |
| Val₈, P2 (.70), 4 | 0.717 | 0.00088 / 0.226 / 0.0376 / 0.0859 | 0.25 → 0.038 (0.090) | yes / yes |
| Val₈, P2 (.70), 3 | 18.5 | 15.6 / 17.9 / 16.0 / 16.3 | all useless | no / no |
| Ser₆, H (.70), 3 | 17.0 | 24.82 / 24.92 / 24.83 / 24.84 | all useless | no / no |
| Lys₄, H (.70), 3 | 33.6 | 49.86 in all forms | all useless | no / no |
| Leu₈, H (.60), 3 | 356.6 | 525.7 in all forms | all useless | no / no |

**Answer: yes, where the sandwich works at all.**  With certified constants (at `m = 3` their sums are 74 to 422
times the measured sums `Σ c_T` of §2.2 for the eight instances) the penalty form decides between a useful and a useless
floor: for Val₆ and Phe₄ on the strand at `m = 3` the site form gives cost numbers of 16–18 and a
model that the reference does not minimise, the pair form 0.04–0.06 and a certificate; at
`m = 4` the pair form gains a factor 4–93, the banded form with `w = 2` a factor 2–4.  Where
`Γ_m` is large (helices, lysine at `m = 3`) no allocation helps: there even the `m`-body envelope
is useless, the loss is in the constants.  Only the floor was run; the ceiling
`f + I_{m−1}g + penalty` is the mirror image.

---

## 3. Numerics: what was run and how to re-run

All in `experiments/science/ws_P4/`; run from that directory with
`export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1`.  Python 3.13, numpy,
scipy (HiGHS), OpenMM (imported by P2's modules).  Every log named below reached its last line
(`DONE …`; followed by `exit 0` where the exit status was recorded).  `cache_p3/` holds copies of
P3's cached enclosure tables (§3.7).  P2's code is used only to read the grids and to rebuild `X′`
(`anlib.load_fb`, `restrict`, `residuals`; `an_main.pruned_product`, `subselect`); P3's code only in
§3.7; nothing was written into `ws_P2`, `ws_P3` or the theory export (checked by time stamps).

| § | command | time | log | output |
|---|---|---|---|---|
| 3.0 | `python3 -B p4_00_find13.py` | 1 s | `logs/p4_00_find13.log` | `out/p4_00_find13.json` — the 13, from P2's stored flags |
| 3.1 | `python3 -B p4_01_shares.py > logs/p4_01_shares.log`; `python3 -B p4_01b_tables.py > logs/p4_01b_tables.log` | 56 s | both | `out/p4_01_shares.json` (908 rows: deficits, shares, over-dense sets, margins) |
| 3.2 | `python3 -B p4_02_third.py > logs/p4_02_third.log`; `python3 -B p4_02b_tables.py > logs/p4_02b_tables.log` | 55 s | both | `out/p4_02_third.json` (136 rows) |
| 3.3 | `python3 -B p4_03_review.py > logs/p4_03_review.log` | 5 s | `logs/p4_03_review.log` | blocks A–G: random instances, brute force, small LPs; the examples and counterexamples of §2 |
| 3.4 | `python3 -B p4_04_domains.py > logs/p4_04_domains.log` | 20 s | `logs/p4_04_domains.log` | `out/p4_04_domains.json` (40 non-product domains) |
| 3.5 | `python3 -I -B <export>/experiments/falsify_conjectures.py --only XI.16` (and `XI.17`, `XI.18`), full mode | 3 s | `logs/p4_05_harness_rerun.log` | re-run of *their* harness |
| 3.6 | from `/home/user/MetricChain`: `lake env lean experiments/science/ws_P4/lean/P4_ThirdOrderModel_copy.lean` (and `P4_ShareCertificates_copy.lean`) | 14 s | `logs/p4_lean_copies.log` | — |
| 3.7 | `./run_p4_06.sh` (= `python3 -B p4_06_p3pair.py SEQ BB TAU M 2`, 11 runs) | 10 s | `logs/p4_06_*.log` | `out/p4_06_*.json` |
| 3.8 | `python3 -B p4_07_dprime3.py > logs/p4_07_dprime3.log` | 39 s | `logs/p4_07_dprime3.log` | `out/p4_07_dprime3.json` (third order on `D′(x*)`, 34 domains) |
| 3.9 | `python3 -B p4_08_joint.py > logs/p4_08_joint.log` (after 3.2) | 48 s | `logs/p4_08_joint.log` | `out/p4_08_joint.json` (joint LP, 136 instances) |

`p4lib.py` is the library (constants of order two and three by a range algorithm, also over
masked domains; tables at the reference; lower models; exact-rational flow, verifier, over-dense
witness, brute force; state-dependent shares by LP with exact verification).

**3.1** Replication checks inside the run: `c_ij` equal to P2's stored matrices (0.0); my
criterion flag and plain row-sum flag equal to P2's in 908 of 908; every flow certificate
verified exactly; every refusal has an exactly verified over-dense set and agrees with brute
force over subsets; "shares ⇒ criterion" asserted in every analysis.

**3.2** Replication checks: `c_T` equal to P2's stored values (0.0); the three instances in which
the envelope fails are P2's, with P2's values (`P2_ball_eps` 0.137, 0.188, 6.72).  LP-A, LP-B, CV-A,
CV-B, LZ are evaluated by rebuilding the model on the full grid and measuring soundness, margin,
`ln Z` and gap there (not from the LP's own value).  LP not run for the 13 instances with more
than 10 multi-state sites (Val₁₂, Leu₁₂…₁₆).

**3.5 Re-run of their harness** (their code, their seed): XI.16 `instances=50, configs=2542,
pair_tighter=50`; XI.17 `pair_yes=29, rowsum_yes=9, triple_yes=58, thirds_yes=19, pairwise_exact=41,
pairwise_cert=40, pairwise_rowsum=17`; XI.18 `instances=66, points=1226, not_reset_closed=43` — the
numbers printed in Propositions 11.18b and 11.18c.  For comparison, my own random pairwise
instances with 2 to 4 states per site and wider tables (block D): criterion 359 of 600, shares
326, split in halves 197; on P2's real instances §2.1.

**3.6 Lean.**  I did not run `lake build` and did not compile in the audit copy.  Copies of the
two files were placed in `ws_P4/lean/` and compiled with `lake env lean` from our tree (built at
the older theory commit).  `ThirdOrderModel.lean`: its imports (`Mathlib`,
`proofs.Frontiers.HigherOrderEnvelope`) **resolve against our tree** — `HigherOrderEnvelope.lean`
and `SecondOrderEnvelope.lean` are identical in our tree and in the export — and the text,
unmodified apart from `#print axioms` lines appended at its end, compiles (exit 0, no error or
warning).  `ShareCertificates.lean` imports
`proofs.Frontiers.ThirdOrderModel`, which **does not exist in our tree**; nothing of that module
is used in the file, so the copy has this one import line replaced by
`import proofs.Frontiers.HigherOrderEnvelope` and then compiles (exit 0).  `#print axioms`
(appended to both copies) reports `propext, Classical.choice, Quot.sound` for all eleven
headline declarations.  This is a check of these two files against the definitions they
import, not a replication of the theory division's audit.

---

## 4. What I did not check

* The **citations** in Proposition 11.18b(b) (Hakimi; Goldberg; Picard) and the attribution of
  P4.1 to the LP-duality literature: no literature was consulted in this workstream.
* **Proposition 11.69b** (also named in THY-RES-0009 §7.2): outside the brief.
* The theory division's **audit** as a whole, its mutation tests, and the Lean build of its tree.
* **Non-product domains**: on P2's real domains the star was run on `D′(x₀)` and `D′(x*)`, the
  third-order models on `D′(x*)` only; no share certificate was run on a non-product domain.
* **Exactness of the LPs.**  Flows and their verification are exact.  State-dependent shares
  and the joint programme of §2.2(e) come from a floating-point LP and are verified exactly after
  a repair; a rejection by the LP (5 analyses at second order) is a floating-point statement.
  (The three rejections in §2.2(e) are forced: there not even the envelope certifies.)  LP-A, LP-B, CV-A, CV-B are floating-point; their
  models were checked on the grid (largest covering violation of a CV solution `7·10⁻⁸`).  LZ is
  a best-found value, not a certified optimum.
* **Item 4**: the floor only; my anchor (`argmin E`), not P3's coordinate-descent anchor; P3's
  band reductions of the pair terms not applied; `m = 5` not run; 11 runs.
* **Upper models**, brackets `ln Z(L) − ln Z(U)`, and kernels: no certificate was fed to the
  theory division's tropical kernel.
* No new enumeration: everything rests on P2's stored grids (`ws_P2/data`, not under version
  control) and inherits P2's modelling choices and its caveats (measured constants, small
  exposed peptides, rigid geometry).
* The claim of §11.30 that Theorem 11.18a supplies sampleable lower models "on graphs of small
  treewidth" was not examined beyond the remark of §2.3(c)(ii).

---

## 5. Requests for the theory division (can be sent as they are)

**P4-T1 (Proposition 11.18c(a): restrict the claim).**  "Theorems 11.16, 11.18, 11.18a and
Proposition 11.18b hold for functions defined on `D` only" is false for the completeness part
of 11.18b(b).  Counterexample: two sites with states {0, 1, 2}, `x₀ = (0, 0)`, `D` = the product
minus the pair of states `(1, 1)` (reset-closed), additive known part with excitation energies
`(0, 1, 10)` at both sites, `c₁₂ = 3`: `x₀` minimises the exact envelope on `D` (which lies 1 or 10
above it at the four star points and 8, 8, 17 at the other three points), and `Δ₁ + Δ₂ = 2 < 3`,
so no shares exist.  Please replace "Proposition 11.18b" by its
sufficient directions ((a), (d), and "shares ⇒ no over-dense set ⇒ certified") and add Theorem
11.17 to the list, for which the extension does hold.

**P4-T2 (Proposition 11.18c, last sentence).**  "What the pruning discards is the set that (c)
is about" is not what our pruned products are.  Measured on the 40 analyses of `g_GB` with a
non-product clash-free domain: the pruned product equals `D′(x₀)` in 6; it is smaller in 34
(median 79 % of `D′(x₀)`); the minimum of the energy over `D′(x₀)` lies in the discarded part in
12, over the whole clash-free domain in 14 (by up to 13.2 kcal/mol).  Suggested text: "covered
by (b) as products; they are in general smaller than `D′`.  The largest reset-closed part at
the minimiser of the clash-free domain is the better choice: on it the star certifies in 13 of
these 40 analyses and the pair-form model of Theorem 11.18a in 30 of 34".

**P4-T3 (Proposition 11.18b(d): the third reason, and the state-dependent form).**  On our
instances the certificate fails although the criterion holds in 4 analyses of `g_GB` (2 of the
13), 26–55 analyses of the other residuals, and 22 of the 132 third-order pair models — in every
`g_GB` case at a single pair, because the deficit is taken at the worst pair of states and the
loads at the cheapest states.  Shares that depend on the state of the site that carries them
(Proposition P4.1) are sound by the same two lines, certify all of the `g_GB` and third-order
cases and all but 5 of the others (each accepted certificate verified exactly), and exist iff
the reference solves the pairwise linear relaxation of the lower model.  Requests:
(i) add the third mechanism to the sentence "They are not necessary: …"; (ii) state P4.1, with
whatever attribution to the LP-duality literature you can verify; (iii) machine-check its
soundness — the statement is `secondOrder_certified_of_shares` without `hJ`, with `s i k a` in
place of `s i k`, the cover hypothesis `c i k − T_ik(a, b) ≤ s i k a + s k i b` for changed `a`, `b`
(`T` the second difference of `M.energy` at `x₀`), and the load hypothesis with the single-site
excitation energy of `M.energy + g` (which for a pairwise `M` contains its pair terms with the
reference states).

**P4-T4 (Theorem 11.18a: wording, and two remarks).**  (i) "At a single triple both are exact"
→ "where all three sites of a triple are changed both forms charge exactly `c_T`".  (ii) "At the
same cost" (THY-RES-0009): the same evaluations; the pair form adds pair terms on every pair
inside a triple with `c_T > 0`, which matters where the lower model must stay banded (§11.30's
remark on lower models).  (iii) Among shares of a triple between its sites and pairs the pure
pair shares are pointwise optimal (Lemma P4.2).  (iv) The coverings of (b) are more than
shares: for four sites and `c_{012} = c_{013} = 1` the penalties `γ₀₁ = γ₂₃ = 1` cover every set
and are not dominated by any share allocation (Example P4.3); "a covering is checked triple by
triple" applies to shares only.

**P4-T5 (measured input for the sentences "How much is gained" and "Measured input").**
Second order, `g_GB`, 184 analyses: criterion 110, share certificate 106, split of the deficits in
halves 91; of the 13: 11.  Third order, 136 instances: reference minimises the envelope / pair
form / site form in 133 / 132 / 113; `ln Z(model) − ln Z(E)` medians `2.6·10⁻⁴` / `2.9·10⁻³` /
`2.0·10⁻²` nats; the pair form is tighter than the site form by a median factor 6.8 in that
quantity and not at all in the largest gap.  All with measured, not certified, constants.

## 6. For our own division

1. **P2's poly-Phe strands** (and nine other analyses): the star's "exact certificate" is for the
   pruned product; the minimum of the clash-free domain is elsewhere, 2–13 kcal/mol lower
   (§2.5).  A note next to P2's Statement 5(b) would prevent a misreading.  The protocol
   "minimiser first, then `D′`" repairs it: the star then certifies Phe on the strand, and the
   pair-form model of third order certifies all Phe and LKSE analyses and Lys at τ = 0.70 (30 of
   34), always as a minimum over `D′(x*)`, not over all of `X_τ`.
2. **P3's sandwich**: replace the site penalties by the banded pair form of Proposition P4.6 —
   no new evaluation, no new constant, the same transfer matrices; on Val₆ and Phe₄ on the
   strand it turns the analysis-only route at `m = 3` from useless (cost number 16–18) into
   usable (0.04–0.9 depending on the band).  P3's generating functions give `Γ_m` and `γ_i`
   without enumerating subsets; the pair sums `Σ_{T⊇{i,j}} ĉ_T = Γ − Γ^{(−i)} − Γ^{(−j)} + Γ^{(−i,−j)}`
   need evaluations with two sites excluded, `O(n²)` of them (P3's code has the one-site
   exclusion; I enumerated the subsets instead, which is affordable only for small `n`).
3. **The joint programme of §2.2(e)** is the form in which the third-order certificate should
   be handed to a checker: tables on the ball, constants, pair shares, state shares; `O(n²k²)`
   additions; no enumeration on either side.  What it still lacks is what everything here
   lacks: certified constants.

---

## Coordinator's note (2026-11-26, before publication as SCI-REV-0012)

1. **Read in full by the coordinator at `24a3c27`:** Proposition 11.18b and Proposition 11.18c of the theory
   report (lines 2238–2318) — the sentences quoted in §2.4, §2.5 and in requests P4-T1, P4-T2 are as printed
   there.  Theorem 11.18a was read at checkpoint 42; the two Lean files were not read by the coordinator.
2. **Recomputed with independent lines** (`experiments/science/pi_inference/p4_adoption_check.py`):
   Counter-example P4.4 by brute force (the domain is reset-closed; `−3·[both changed]` is in the class; the
   lower model lies 1, 10, 8, 8, 17 above its value at the reference; no shares; on the full product the
   criterion fails at `(1, 1)`); and the finding of §2.5 for Phe₄…Phe₈ on the strand at the threshold 0.60 from
   workstream P2's stored grids with P2's own domain functions: the minimum over the clash-free domain is
   not in the pruned product, by `1.92, 10.45, 11.90, 13.20, 13.25` kcal/mol, with the shapes of `X′` printed
   in §2.1.
3. **Re-run from a clean copy** (the scripts only, with links to `ws_P2`, `ws_P3`): `p4_00_find13`,
   `p4_01_shares`, `p4_01b_tables`, `p4_03_review`, `p4_04_domains` — 81 s, exit 0, empty error streams; logs
   identical to the cited ones apart from run-time fields and the appended `exit 0` lines.
4. **Both Lean copies re-compiled** with `lake env lean` (exit 0; 8 + 3 `#print axioms` lines, standard
   axioms only) and compared with the originals of the audit copy at `24a3c27` by `diff`: they differ in the
   appended axiom lines and, for `ShareCertificates`, in the one import line.
5. **Not re-run by the coordinator:** `p4_02`, `p4_02b`, `p4_06`, `p4_07`, `p4_08`; their harness blocks.
   **Not re-derived by the coordinator:** Lemma P4.2, Example P4.3, Propositions P4.1, P4.5, P4.6 (read;
   P4.1's two-line soundness argument and P4.6(ii) were followed).

