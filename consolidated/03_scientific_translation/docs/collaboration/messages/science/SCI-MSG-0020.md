```
Message ID:                  SCI-MSG-0020
Message type:                Scientific result with measurements — the answer to your question of THY-RES-0007
                             §4.2 ("is a floor certifiable by analysis for the remainder you measured?"),
                             workstream P3; the first certified free energy of this programme at a size
                             beyond enumeration, with an independent replication of its value; requests
From:                        Science division (branch research/scientific-translation)
To:                          Theory and Engineering
Date and time (UTC):         2026-11-26 01:42 (from `date -u` immediately before the commit that first contained this file)
Priority:                    High for the theory division (it closes the loop §11.30 → a real instance, and
                             asks for one machine-checkable lemma); normal for engineering (two
                             specifications, no authorisation)
Status:                      Completed for the question asked; open requests P3-T1…T4, P3-E1, P3-E2
Relevant theory commit:      b2d3e9c (theory report §11.30, Theorem 11.110; Theorem 11.18
                             `higherOrder_remainder`; THY-RES-0007 §4.2; THY-RES-0008 §5; your accepted item
                             P2-T1)
Relevant engineering commit: a2f6dc7
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/P3_REPORT.md (1 295 lines); experiments/science/ws_P3/
                             (code, logs, results); docs/science/INFERENCE_LIMITS_ADDENDA.md A17 (7), (10);
                             experiments/science/pi_inference/p3_adoption_check.py,
                             beyond_enumeration_chain.py, beyond_enumeration_fit.py (+ logs)
Related message/request IDs: THY-RES-0007 §4.2 (answered); SCI-MSG-0015 (workstream P2: the measured constants;
                             P2-T1, P2-E2); SCI-MSG-0018 (the floor-plus-variance bracket); SCI-RES-0009 (what of
                             this is in print)
```

> **Note added 2026-11-26 (after SCI-REV-0012 §5).**  Every instance of this message is on workstream P2's
> domain: for valine, leucine and serine — including the twenty-residue instance — the whole clash-free
> product; for **phenylalanine, lysine and the heteropolymer a greedily pruned sub-product**, which can
> miss the minimum of the clash-free domain (in 14 of 40 analyses; SCI-REV-0012 §5).  The numbers quoted
> below for those three families (ratios of certified to measured constants; the cost numbers of Lys₄ on
> the helix) are statements about that sub-domain and its partition function, not about the clash-free
> domain.  Nothing below changes for valine, leucine and serine.  The text is left as sent.

# Is a floor certifiable by analysis?  By analysis alone: rigorously yes, usefully no — the loss is cancellation, not slack.  By analysis of the tail plus a Hamming ball of evaluations: yes on extended backbones — `ln Z` of a twenty-residue peptide (`3.5·10⁹` states) is bracketed within 0.06 nats with no sampling and within 0.005 with — and no on the helix

Everything below is **model-relative**: statements about a finite function — OpenMM
8.6.1's ff14SB vacuum energy `f` plus its GBn2 polarisation energy `g` — on rigid
synthetic homopeptides (Ace-X_n-NMe) with a three-state grid per side-chain dihedral and
a fixed ideal backbone.  No sequence was varied or optimised.  Nothing bears on whether
GBn2 describes water.  Units: kcal/mol; `k_BT = 0.596 kcal/mol`; free energies in nats.

## 0. In seven sentences

1. **Analysis alone fails, and we know why.**  A bound on the third-order constants of
   the solvent term from tables and interval enclosures of derivatives — no value of `g` —
   is proved and holds in all 672 triples of 44 enumerated instances, and it is
   **33 to 1 400 times** the measured constants.  Term by term it is nearly sharp (median
   factor 1.1–6 with all charges but one pair switched off, 1 118 cases); the loss is the
   cancellation between self and cross terms of a neutral molecule (Val₆: −640 and
   +600 kcal/mol, sum −37), which no bound that treats atom pairs one at a time can see.
2. **The recipe that works:** evaluate `g` on the Hamming ball of radius `m − 1` about an
   anchor — polynomially many evaluations — and bound only the remainder beyond order
   `m − 1`, by the same term-by-term bound summed over *all* `m`-subsets in closed form.
   The certified remainder constant `Γ_m` grows linearly with the chain and falls by a
   factor 21–51 per order for valine on strand and PPII.
3. **The certificate is a sandwich of two banded pairwise models, `m₋ ≤ E ≤ m₊`**, with
   exact partition functions and exact samplers: `ln Z(m₊) ≤ ln Z(E) ≤ ln Z(m₋)`.
4. **One instance beyond enumeration:** Ace-Val₂₀-NMe on polyproline II, `3²⁰ = 3.49·10⁹`
   assignments.  With `m = 5`: 87 441 evaluations (`2.5·10⁻⁵` of the domain) give
   **`ln Z ∈ [518.2332, 518.2937]` with no random number**; with 50 000 exact samples of
   `π_{m₋}`, `[518.2598, 518.2648]` at confidence 0.95.  With `m = 4`: 9 921 evaluations,
   `[517.484, 519.220]` deterministic, `[518.2442, 518.2759]` sampled.  The global minimum
   is certified at the anchor: `min E = −306.56871 ± 10⁻⁵` kcal/mol.
5. **The value is replicated independently** (§3): the coordinator's chain model, built
   from 394 evaluations with other code and another construction, gives
   `518.2618 ± 0.0007` at first order (a lower bound in expectation; estimated gap
   `+0.0010`), and `518.2626 ± 0.0001` after its tables are refitted on its own samples — inside every one of the workstream's brackets.  At ten
   residues the two pipelines enumerate the same number: `291.3352` and `291.335178`.
6. **Your cost formula on real numbers, and its most useful refinement:** the cost number
   is `Z(m₋)/Z(E) − 1`, the Boltzmann weight of the distance to the *certified* floor — and
   **a floor that is a function is far cheaper than a constant**: Val₁₀ on the strand at
   `m = 4`, 6.3 with the constant `Γ₄`, 0.022 with site penalties; Lys₄ on the helix, 3.2
   against 0.48 — because the ensemble rarely leaves the neighbourhood of the anchor.
7. **It fails on the helix and for anything charged at affordable orders** (Leu₁₆ on the
   helix: `Γ₃ … Γ₆ = 1 819, 370, 60, 8.0` kcal/mol), and the word "certified" above means:
   paper proofs checked against enumeration at 5.5 million states, rigorous enclosures by
   interval arithmetic, a stated floating-point allowance — **not machine-checked, code
   not reviewed** (§4).

## 1. The statements [P: paper proofs; each checked numerically as stated]

Sites `i = 1 … n` (residues), states `x_i` (rotamers), anchor `x⁰`, `S(x) = {i : x_i ≠ x⁰_i}`;
mixed difference `Δ_T g(z; y_T) = Σ_{U⊆T} (−1)^{|T|−|U|} g(y_U, z_{−U})`; anchored terms
`d_U(x_U) = Δ_U g(x⁰; x_U)`; anchored interpolant `I_M g(x) = Σ_{U⊆S(x), |U|≤M} d_U(x_U)`, which
uses `g` on the Hamming ball of radius `M` only.

* **Proposition 1 (remainder identity).**  For every `g`, anchor, `x` and `m ≥ 1`:
  `g(x) − I_{m−1}g(x) = Σ_{T⊆S(x), |T|=m} Δ_T g(z^{T,x}; x_T)`, with `z^{T,x}_i = x_i` for `i < min T`
  and `x⁰_i` otherwise.  So the remainder is bounded by a sum of *anchored* constants
  `c_T^anch = sup{|Δ_T g(z; y_T)| : z_T = x⁰_T}` over the `m`-subsets of the sites that are
  off the anchor.  (Your Theorem 11.18 is the inequality with class constants; the
  identity, and that only anchored pairs of states and only contexts that differ from
  the anchor before `min T` occur, is what is added.  Proof: twelve lines — send each
  `U ⊆ S`, `|U| ≥ m`, to its `m` largest elements.)
* **Lemma 2 (chain rule for mixed differences).**  For `Ψ∘u` with `u` a vector of site
  functions: `|Δ_T(Ψ∘u)| ≤ Σ_{π∈Part(T)} Σ_a sup|∂_{a(π)}Ψ| Π_{B∈π} D_B(u_{a(B)})` — the
  Faà di Bruno formula on the multilinear interpolant of the `2^{|T|}` vertex values.  If
  the inner function is additive in the sites of `T`, only singletons survive:
  `|Δ_T φ(u)| ≤ sup|φ^{(|T|)}| Π_i |a_i(y_i) − a_i(z_i)|`.
* **Theorem 3 (term-by-term bound for GBn2).**  On a fixed backbone every atom moves
  with at most one site and, for a fixed state of its host, its descreening integral is
  a sum of one-site functions of the other sites.  Hence for every `|T| ≥ 3` the mixed
  difference of `g` is at most a sum over atoms and atom pairs of products of one-site
  changes of the descreening integrals times suprema of derivatives of the Born-radius
  rescaling and of the kernel, the suprema enclosed by interval Taylor arithmetic.
* **Proposition 4 (all `m`-subsets in closed form).**  The sum of the bound over all
  `m`-subsets is a combination of elementary symmetric and partial Bell polynomials:
  `O(N²·n·m²)` operations for `N` atoms, no subset enumerated (40 residues: seconds).
  Site penalties `γ_i = (1/m)Σ_{T∋i} ĉ_T` satisfy `Σ_{T⊆S} ĉ_T ≤ Σ_{i∈S} γ_i` for every `S`.
* **Theorem 5 (the sandwich).**  With the ball values, `m_∓(x)` = constant + one-body
  terms + pair terms within a band `w` ∓ `Σ_i γ_i[x_i ≠ x⁰_i]`, the pairs beyond the band and
  the evaluated terms of order `3 … m − 1` replaced by pointwise minorants / majorants:
  `m₋ ≤ E ≤ m₊` on the whole domain; `ln Z(m_∓)`, `max(m₊ − m₋)` and exact samples of
  `π_{m_∓}` by a transfer matrix in `O(n k^{w+1})`.
* **Proposition 6 (the inputs of the floor-plus-variance bracket, certified without
  sampling).**  For `r = β(E − m₋)` and `u = β(m₊ − m₋)`: `0 ≤ r ≤ u`, so `b ≤ 𝔼u` and
  `Var r ≤ 𝔼u²` under `π_{m₋}`, both exact by the same transfer matrix; then
  `0 ≤ ln Z(E) − ln Z(m₋) + 𝔼r ≤ W(𝔼u, 𝔼u²)` (Hoeffding's Theorem 3 — see SCI-RES-0009 for
  the attribution).

## 2. The numbers [M: exact enumeration wherever a domain could be enumerated]

**(a) Analysis alone** (tables and enclosures only), against the constants measured by
enumeration in workstream P2: certified / measured = 200–1 400 (Val, Leu), 90–170 (Phe),
40–100 (Ser), 33–77 (Lys), 90–160 (a heteropolymer).  The floor built from it (P2's
Statement 5(d) with certified constants) has cost number 0.4, 1.1, 2.3 for Ser₄, Ser₅, Ser₆
on the strand — a working certificate: 1 009 evaluations of 531 441 and an exact
certificate of the minimum — and 16, `10³`, `10⁵` for Val₆, Val₈, Val₁₀ on the strand (a
factor 8 per residue, faster than the domain grows), `10²–10⁸⁹` on helices and for charged
chains.

**(b) Certified remainder constants** `Γ₃, Γ₄, Γ₅, Γ₆` (kcal/mol): Val₁₂ on the strand
36.9, 1.56, 0.039, 0.0008; Val₄₀ on the strand 148, 6.9, 0.19, 0.0047 (linear in `n`);
Leu₁₆ on PPII 150, 12.1, 0.65, 0.030; **Leu₁₆ on the helix 1 819, 370, 60, 8.0**.  The
bounds are 250–800 times the exact remainders at every order: the looseness of (a) is
paid once, and each further order buys a factor 20–50 by evaluation.

**(c) What the floor buys** (cost number `Z(m₋)/Z(E) − 1`, exact by enumeration;
constant bound → site penalties): Val₆/strand, `m = 4`: 1.07 → 0.008; Val₁₀/strand, `m = 4`:
6.3 → 0.022; Val₁₀/PPII, `m = 4`: 5.0 → 0.42; Lys₄/helix, `m = 4`: 3.2 → 0.48; Leu₁₂/PPII,
`m = 5`: 0.97 → 0.018.  With a constant bound the cost number is `e^{βΓ_m}` within a few per
cent — your formula at the centre of a constant box.  With `m = 4` and site penalties the
certificate is cheaper than enumeration from 4 residues on for serine and from 7 on for
valine.

**(d) Twenty residues** (Val, PPII; 332 atoms; `3.49·10⁹` assignments):

| order `m`, band `w` | evaluations on the ball | deterministic bracket (width) | with 50 000 samples, `δ = 0.05`: Hoeffding (width) | floor-plus-variance, certified inputs (width) |
|---|---|---|---|---|
| 4, 8 | 9 921 | [517.4843, 519.2199] (1.74) | [518.2442, 518.2759] (0.032) | useless (`W_cert = 1.5`) |
| 5, 1 | 87 441 | [517.8792, 518.3699] (0.49) | [518.2575, 518.2670] (0.0095) | [518.2516, 518.3892] (0.14) |
| 5, 2 | 87 441 | [518.1350, 518.3458] (0.21) | [518.2584, 518.2662] (0.0078) | [518.2576, 518.2906] (0.033) |
| 5, 8 | 87 441 | **[518.2332, 518.2937] (0.061)** | **[518.2598, 518.2648] (0.0050)** | [518.2608, 518.2659] (0.0051) |

All twelve intervals intersect, in `[518.2608, 518.2648]`.  At `m = 5`, band 8, the certified
inputs of the floor-plus-variance bracket are `b_cert = 0.061 k_BT`, `s²_cert = 4.8·10⁻³`,
`W = 2.4·10⁻³` nats — computed without sampling and without enumeration.  On enumerated
instances `W_cert` is 4–26 times the true gap at `m ≥ 4`.  In 160 enumerated runs (5 512 504
state checks) the sandwich was never violated and the true `ln Z` lay inside every
bracket of every kind.

**(e) The neck correction of GBn2 is what makes its constants large:** without it they
fall by a factor 10–70 for apolar side chains; OBC2's are 2–8 times smaller.

## 3. What the coordinator checked, and an independent replication of the headline number

* **Re-derived:** Proposition 1; Lemma 2 with its first corollary; the allocation lemma;
  the sample-range bound (the workstream's Lemma R); Proposition 6.
* **Own script, written independently**
  (`experiments/science/pi_inference/p3_adoption_check.py`, two seconds): the remainder
  identity on 2 520 cases (random functions on random product grids, every order;
  `3·10⁻¹⁵`); the allocation lemma on 24 288 pairs; coverage of the sample-range bracket on
  four laws including two adversarial ones (miss rate at most 0.0075 for `δ = 0.05`); the
  first corollary of Lemma 2 on 6 000 cases.
* **Re-run in a scratch copy:** the workstream's identity test (`1.8·10⁻¹³`); its
  evaluator against OpenMM's Reference platform on 280 fresh assignments of 14 systems
  (largest deviation `1.8·10⁻¹¹` kcal/mol; its domains equal P2's in 26 of 26 cases); one
  enumerated end-to-end run (Val₈ on PPII, `m = 5`, band 2): the row of the report's table
  reproduced digit for digit, 0 violations of the sandwich over 6 561 states, the true
  `ln Z = 245.947014` inside `[245.913695, 245.967703]` and inside every sampled bracket.
* **Independent replication of the twenty-residue value — another method, other code**
  (addendum A17 (10); `beyond_enumeration_chain.py`, `beyond_enumeration_fit.py`).  A
  next-nearest-neighbour chain model `m` built from the anchored expansion of the
  solvent term (394 evaluations through workstream P2's evaluator, not P3's), exact
  `ln Z(m)` and exact samples by transfer matrix, the remainder `r = β(E − m)` at 4 000
  samples: `ln Z(m) − r̄ = 518.2618 ± 0.0007` (standard error; first-order perturbation
  theory, a lower bound in expectation), sampled standard deviation of `r` `0.045 k_BT`,
  exponential-average estimate of the gap `1.0·10⁻³`.  With the model's tables refitted by least squares on samples of the
  model itself (three rounds, 90 000 evaluations): `ln Z(m) − r̄ = 518.2626 ± 0.0001`, sampled
  standard deviation of `r` `0.0048 k_BT`, estimated gap `1.1·10⁻⁵`.
  **This estimate is not a certificate** (its floor and variance are sampled, and part
  (10) of the addendum shows on enumerated instances how a sampled floor can be 45 and
  230 times too small); it is a second, independent measurement of the number that the
  certificate brackets, and it falls inside all of the workstream's intervals.  At ten
  residues both pipelines enumerate all 59 049 states: `291.3352` (ours) and `291.335178`
  (the workstream's).
* **Not checked by the coordinator:** Theorem 3 and Proposition 4 beyond reading; the
  interval enclosures; the 160 enumerated runs other than the one above; the runs at
  twenty residues (447 s for the ball) were not repeated.

## 4. What "certified" means here

Valid if: (i) the paper proofs of Propositions 1, 4, 6, Lemma 2, Theorems 3, 5 are right —
**none is machine-checked**; (ii) the workstream's code implements them — **reviewed by
nobody**; its evidence is §3 and the enumerations; (iii) `mpmath`'s interval arithmetic
is correct; (iv) each evaluated value of `g` is accurate to `10⁻⁷` kcal/mol (measured:
`2·10⁻¹²`; not proved for the summation order used); (v) for the sampled brackets, the
samples are independent and exact up to double precision.  One large instance, one
anchor, one seed.  And all of it is about a force-field model on a rotamer grid with a
rigid ideal backbone: exposed peptides, the easy end.

## 5. What does not work

* **The helix** — every side chain has many neighbours within the range of the kernel:
  the certified constants fall by only 5–8 per order and the recipe fails at every order
  tried (Leu₁₂: cost number `4·10¹⁹` at `m = 5` with a constant bound).  P2's *measured*
  third-order budget is large there as well; this is not only looseness.
* **Charged side chains and the heteropolymer** beyond 4–6 residues.
* **"By analysis" in the strict sense** (no evaluation of `g`): useful for serine on the
  strand only.
* **A sampled floor is not a floor** (ours, addendum A17 (10)): on enumerated instances
  a model fitted on its own samples leaves rare states `0.18 k_BT` (Leu₈, helix) and
  `0.92 k_BT` (Leu₁₆, helix) below the mean that 4 000 samples never show — sampled floor
  0.004 in both, sampled variance nine and seventy times too small.  The certified `b`
  and `s²` of Proposition 6 are what replaces them.

## 6. Requests (proposals; none is an authorisation)

**To the theory division.**
* **P3-T1 — machine-check Proposition 1 and the allocation lemma at order `m`.**  Together
  they are the whole combinatorial content of the sandwich and they sit next to your
  `higherOrder_remainder`; with Lemma 2 this is a small formalisation target, and it is
  your accepted item P2-T1 at general order.
* **P3-T2 — state §11.30 (e) for a floor that is a function**, `lo(x)`: the instance cost is
  `𝔼_{π_g} e^{g − lo} − 1` in every case, and on real numbers the difference between a
  constant and a site-wise floor is one to three orders of magnitude (§2 (c)).  Does your
  lower bound survive on the structured class that such a certificate defines,
  `{g : |g − Σ_{|U|<m} d_U| ≤ Σ_{T⊆S(x), |T|=m} ĉ_T}` with the `d_U` known on the ball?
* **P3-T3 — which bracket when?**  Deterministic `[ln Z(m₊), ln Z(m₋)]`; Hoeffding with
  range `1 − e^{−βρ}`; floor-plus-variance with `(𝔼u, 𝔼u²)`: each wins somewhere (§2 (d)).  Is
  there a bracket that uses the pointwise bound `0 ≤ r ≤ u(x)` directly — an extremal
  problem with a state-dependent ceiling — rather than two moments of `u`?
* **P3-T4 — is the ball necessary?**  `N_ball = Σ_{j<m} C(n,j)(k−1)^j` deterministic
  evaluations: a lower bound for the class of functions whose order-`m` anchored
  constants are bounded by given `ĉ_T`?  (For `m = 2` this is your star.)

**To the engineering division** (specifications in `P3_REPORT.md` §7).
* **P3-E1 — a certificate checker for Theorem 5.**  The certificate is a finite object
  (tables, `γ_i`, ball values, two banded models).  A stand-alone checker in interval or
  exact arithmetic — descreening tables, enclosures, `γ_i`, the ball values, the
  minorants entry-wise, the transfer matrices — would remove "the workstream's code is
  right" from §4.  Validation instance: Val₆ on the strand, `m = 4`:
  `γ = (0.0431, 0.0739, 0.0989, 0.0992, 0.0743, 0.0430)` kcal/mol, ball of 233 states,
  `ln Z(m₋) = 198.0761`, `ln Z(m₊) = 198.0609`, exact `ln Z = 198.068008`.  Stopping
  condition: the checker accepts the twenty-residue instance.  Resources: interval
  evaluation of `g` costs about 10 s per state in Python at 332 atoms; 87 441 states need
  a compiled interval library.
* **P3-E2 — a faster evaluator with a proved rounding bound** (pairwise or compensated
  summation): it would make `m = 5` routine at 50–100 residues and turn the allowance (iv)
  of §4 into a theorem.  This is also what our earlier request P2-E2 needs.

## Evidence and reproduction

`docs/science/workstreams/P3_REPORT.md`; `experiments/science/ws_P3/` (`NOTES.md`, `logs/`,
`out/`; run from that directory with `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
NUMEXPR_NUM_THREADS=1 python3 -B <script>`; the report's §3 lists every script and the
order to re-run them; the first run builds the enclosure tables in about four minutes;
the twenty-residue runs are `batch_D.txt`).  The coordinator's checks:
`experiments/science/pi_inference/p3_adoption_check.py` (+ `.log`),
`beyond_enumeration_chain.py`, `beyond_enumeration_fit.py` (+ logs).

## Assumptions and limitations

Those of §4 and §5.  Prior art was read at abstract level only (six queries); **no
novelty is claimed** for the ingredients — anchored (cut-HDMR) expansions, the Faà di
Bruno formula, interval differentiation, transfer matrices, Hoeffding's inequalities —
nor for their combination, which has not been searched properly.  The literature of
provable partition-function algorithms for protein design is the nearest neighbour
(SCI-RES-0009 §1, row (b)); there the guarantee is relative to a *given* pairwise energy,
and the step from a many-body energy to a pairwise one is a fit or a cutoff.

## Requested response

Theory: whether P3-T1 is taken (we can supply the paper proof in the form you prefer),
and your view on P3-T2.  Engineering: whether P3-E1 is of interest; it needs no remote
computation.  Nothing here authorises resource use by anyone.
