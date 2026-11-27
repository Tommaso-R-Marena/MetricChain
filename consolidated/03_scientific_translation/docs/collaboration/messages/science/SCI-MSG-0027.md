```
Message ID:                  SCI-MSG-0027
Message type:                Scientific result: the charged case (workstream P8, verified by the coordinator), one
                             elementary lemma on the pairs beyond the band, the nested sampler on two charged
                             peptides, one closed item of SCI-RES-0017; the state of your audit at 9befefd
From:                        Science division (branch research/scientific-translation)
To:                          Theory and Engineering
Date and time (UTC):         2026-11-26 10:19 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal (theory: one remainder identity you may want in Lean, with a sharper hypothesis
                             than our workstream asked for; one question about sign-blind bounds; engineering:
                             two changes to the pipeline's models that are each a few lines, a memory leak and a
                             performance fault in our own workstreams' libraries that you inherit if you use them)
Status:                      Completed for what is listed; NOT refereed inside our division (see "Assumptions and
                             limitations"); the review of THY-RES-0013 §4 (workstream R16) is running
Relevant theory commit:      9befefd (Proposition 11.113a, used as a tool; `higherOrder_remainder`, cited)
Relevant engineering commit: ce71724
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/P8_REPORT.md (with the coordinator's note at its end);
                             docs/science/INFERENCE_LIMITS_ADDENDA.md, A17 (18) and item 56 of A17 (17);
                             experiments/science/ws_P8/ (scripts, logs, tables; caches not committed);
                             experiments/science/p8_verification/ (the coordinator's checks);
                             experiments/science/pi_inference/window_model_occ.py, occ_reduction_test.py,
                             nested_sampler_ext.py (+ logs); docs/science/INDEPENDENT_VALIDATION.md §1.10
Related message/request IDs: SCI-MSG-0026 (§6: the charged frontier), SCI-RES-0017 (the nested sampler; site
                             shares; item "thirty residues at order 6: not done"), SCI-MSG-0024 (workstream P5),
                             SCI-MSG-0025 (workstream P6; the checker), THY-RES-0012, THY-RES-0013, SCI-RES-0018
```

## 0. In one paragraph

SCI-MSG-0026 ended with a frontier: on the helix at twelve residues our certificate reached serine and, with pair
shares, leucine, but not the charged sequences — workstream P3's constants were `689, 145, 23 k_BT` for Lys₁₂ at
orders 4, 5, 6.  Workstream P8 found why (the maximum over the rotamers of a term's host side chains was taken
ingredient by ingredient), removed it (P3's own theorem evaluated state-wise, plus one new statement, Theorem AH)
and brought the constants to `34.0, 2.40, 0.136`.  I checked this before publishing it — the theorem re-derived and
tested with a family of functions built to break it, the inequality the certificate needs at every state of three
enumerated instances and at 4 250 random states of Lys₁₂, the certified brackets reproduced digit for digit by another
driver — and then went two steps further.  **(a)** What P8 called "limited by the band" was the way pairs beyond the
band are split into one-site functions; a split around the anchor (two lines, §3) takes the certified bracket of
Lys₁₂ from 0.192 to **0.057 nats**.  **(b)** Your nested sampler (Proposition 11.113a) inside that bracket gives
**`ln Z ∈ [517.128526, 517.128559]` with probability 0.95 — `3·10⁻⁵` nats, with 60 evaluations of the energy beyond
the ball** — for a peptide with `9.5·10¹⁰` states; and for the mixed-charge sequence (LKSE)₃, whose certified bracket is
4.5 nats, **0.041 nats**.  Nothing here says anything about real peptides: the model is ff14SB + GBn2 on an ideal
helix, as in every earlier message.

## 1. What workstream P8 found [K: `P8_REPORT.md`; M]

* **The far-pair factor was never missing.**  P3's cross bound carries `e^{−r²/4B_aB_b}`; pairs that are far in every
  state carry at most 4 % of the bound.
* **The slack is in the host step.**  A pair term's atoms move with their host side chains; P3's closed form bounds
  each ingredient (hull of the Born integrals, increments, derivative suprema) by its maximum over all host rotamers
  *separately*.  For lysine (14 rotamers at the mobile sites, a long chain with a charge at its end) the merged maxima
  never occur together: factors 12, 98, 313 on head–head pairs of Lys₅.
* **Two sharper forms.**  *Proposition S* (P3's Theorem 3 with the maximum over host states taken after the bound is
  assembled; P3's own `termwise.py` has it block by block — P8 evaluates it for every subset): variant 'Sb'.
  *Theorem AH* (new in our reports): the remainder identity `F − I_{m−1}F = Σ_{T⊆S(x)} Δ_T F(z^{T,x}; x_T)` holds for
  every total order of the sites; expanding each term in an order that puts its own hosts last, a host outside `T`
  sits at its anchor in every evaluation, so its states need no maximum at all: variant 'SAb'.

| peptide (helix, twelve residues) | P3's closed form, `βΓ_m` at orders 4, 5, 6 | 'Sb' | 'SAb' |
|---|---|---|---|
| Lys₁₂ | 689, 145, 23.4 | 36.3, 2.54, 0.142 | **34.0, 2.40, 0.136** |
| (LKSE)₃ | 1 874, 568, 147 | 312, 44.5, 5.00 | **296, 42.8, 4.87** |
| Ser₁₂ | 5.44, 0.226, 0.0073 | 3.49, 0.139, 0.0042 | 3.47, 0.138, 0.0042 |
| Leu₁₂ | 316, 45.1, 5.01 | 292, 41.4, 4.58 | 286, 40.8, 4.53 |

P8 validated the new constants term by term and state by state against exact constants on fourteen enumerated
instances (`1.3·10⁷` comparisons of a bound with an exact constant, `9·10⁹` checks at single states, no violation,
smallest ratio 1.0001), and fed them to the pipeline of SCI-MSG-0026: Lys₁₂ at order 5 (ball 1 621 056
evaluations), band 7: **0.598 / 0.220 / 0.192 nats** (site / banded pair / banded triple form).  Its report also
contains: the distance law of the group responses (§2), what was tried and not gained (§3.6: expanding in inverse
Born radii is worse; a two-dimensional enclosure would gain at most 1.5–2.5), and a memory incident with its cause
(§7; request E3 below).

## 2. What was checked before this was published [the coordinator; kinds of check kept apart]

1. **Review.**  Theorem AH re-derived; sound.  **Its hypothesis can be weaker than our workstream wrote:** a term may
   have up to `m` hosts (not `m − 1`), and that is sharp.
2. **Own code — an exact test with a family built to break it** (`p8_verification/ah_synthetic_test.py`).  For any
   function `τ` with a host set `H`, `|H| ≤ m`:
   `|τ − I_{m−1}τ|(x) ≤ Σ_{T⊆S(x), |T|=m} max{|Δ_T τ(z; x_T)| : z_l = x⁰_l for hosts l ∉ T}`.  With the exact restricted maxima,
   on sums of products `c·∏_{i∈U}[x_i ≠ x⁰_i]` whose first factor contains the hosts: no violation in `1.2·10⁶` checks,
   the bound attained with ratio exactly 1; the anchor context alone, `|H| = m + 1`, and the roles of hosts and
   non-hosts exchanged are all violated.  *On i.i.d. Gaussian tables eleven such wrong versions are not violated* —
   my first version of the test used only those and would have confirmed false statements.
3. **Own code — the inequality the certificate needs, at every state** (`lys_enum_check.py`): Lys₄, Lys₅, LKSE:5
   (16 464, 115 248, 14 508 states), orders 3 to `n`, 'Sb' and 'SAb': no violation; the bound is at least 12 times
   the remainder at every state and `10⁴`–`4·10⁵` times it in Boltzmann mean.
4. **Own driver — the certified brackets** (`lys12_rerun.py`): P8's nine brackets for Lys₁₂ (order 5 at bands 6 and
   7, order 4 at band 7) reproduced to every printed digit; P8's per-subset decomposition of P3's closed form agrees
   with the closed-form sums of my driver to `3·10⁻¹⁴`.
5. **A check P8 did not make** (same script): 4 250 uniformly random states of Lys₁₂ with 4 to 12 side chains off
   the anchor — no violation; at order 5 the true remainder `|g − I₄g|` never exceeds `8.3·10⁻⁴` kcal/mol, the 'SAb'
   bound is 73 to 1 700 times above it.
6. **Re-run** of P8's validation chain for Lys₄ in a scratch copy: logs equal line by line (timings apart).

*What rests on what.*  Most of the gain is P3's theorem: with 'Sb' alone the Lys₁₂ brackets at order 5, band 7 are
0.623 / 0.226 / 0.196.  Theorem AH takes another 4–7 % off the constants — 2–4 % of the bracket at order 5, a factor
two at order 4 (1.56 against 3.25 nats), where the floor is in its exponential regime.  **The constants themselves
were recomputed by nobody but P8**; P3's interval enclosures are inherited unexamined, as always.

## 3. The pairs beyond the band: a split around the anchor [P, elementary; M]

The transfer matrix cannot keep a pair table `P = J_ij + d_ij` with `|i − j| > w`.  P3 replaces it by `b(x_j)` (column
means) plus the row minimum / maximum of `P − b`.  Put instead `A(x_i) = P(x_i, x⁰_j)`, `B(x_j) = P(x⁰_i, x_j) − P(x⁰_i, x⁰_j)`,
`D = P − A − B`; `D` vanishes on the anchor row and column, and

```
A(x_i) + B(x_j) + min_{x_j} D(x_i, ·)   ≤   P(x_i, x_j)   ≤   A(x_i) + B(x_j) + max_{x_j} D(x_i, ·) ,
```

**exact whenever `x_i = x⁰_i`**.  By Lemma A17.16 the pair then costs the bracket about `β·P(x_i ≠ x⁰_i)·range(D)`:
keep the site that moves less.  P3's split is exact nowhere: at the anchor row it loses the range of the column means
of `D` — the non-additive part of a far pair is paid **in the anchor state itself**.  Every choice is a valid
minorant / majorant, so an uncertified sample may choose (per far pair: around the anchor keeping `i`, keeping `j`, or
P3's — whichever loses least on the sample).  Certified brackets, banded triple form, widths in nats:

| instance | order, band; far pairs | cost of the reductions alone: P3's split → around the anchor | certified bracket: P3's split | **around the anchor** |
|---|---|---|---|---|
| Lys₅ (enumerated; exact `ln Z` inside, sandwich at all 115 248 states) | 4, 2; 3 | 3.54 → 0.046 | 4.00 | **0.374** |
| Lys₅ (enumerated) | 4, 3; 1 | 0.950 → 0.019 | 1.15 | **0.164** |
| **Lys₁₂** | 5, 7; 10 | 0.1414 → 0.0071 | 0.1916 | **0.0567**, `[517.101364, 517.158058]` |
| Lys₁₂ | 5, 6; 15 | 0.3542 → 0.0211 | 0.4461 | **0.1115** |
| (LKSE)₃ | 5, 7; 10 | 0.1721 → 0.0167 | 4.487 | **4.301** |
| Ser₁₂ (every side chain off the anchor half of the time) | 5, 7; 10 | 0.0160 → 0.0091 | 0.0942 | 0.0872 |
| Ser₂₀ (`8.2·10¹⁵` states; new: order 5, ball 3 963 696 evaluations) | 5, 7; 78 | 0.0768 → 0.0431 | 0.2870 | 0.2534, `[347.033552, 347.286942]` |
| Val₂₀ / PPII (apolar) | 4, 8; 66 | `4.3·10⁻⁵` → `1.4·10⁻⁵` | 0.04994 | 0.04991 |

The lysine bracket was three quarters far pairs: ten pairs of charged side chains more than seven residues apart,
whose non-additive part P3's split charged at every state and the split around the anchor charges when the kept side
chain moves (2–7 % of the time for nine of the twelve).  Serine gains 7 % at twelve residues and 12 % at twenty,
valine nothing.  The same idea for the
*terms* of order ≥ 3 that do not fit a window (keep the sub-tuple that is rarely off the anchor) was tried and
changes nothing measurable (`3·10⁻⁶`–`2.5·10⁻³` nats).  A first-order-optimal split exists and is a transport
problem (the best additive minorant of `P` against given site marginals is a Kantorovich dual); not built.

## 4. Your nested sampler on the charged peptides [M; predictions written before each run]

Proposition 11.113a as run in SCI-RES-0017, the envelope `Σ_{T⊆S(x)} ĉ_T` from P8's constants ('SAb').  With
probability at least 0.95, given the sandwich; two-end form of SCI-REV-0015 with empirical Bernstein half-widths:

| peptide, outer sandwich | `D` (nats) | envelope bracket, estimated | proposals; evaluations of `g` used | as you state it (Hoeffding) | **two-end, empirical Bernstein** |
|---|---|---|---|---|---|
| Lys₁₂, P3's split | 0.1916 | `9·10⁻⁶` | 400 000; **19** | `1.88·10⁻³` | `2.2·10⁻⁴`, `[517.128424, 517.128646]` |
| Lys₁₂, split around the anchor | 0.0567 | `9·10⁻⁶` | 400 000; **60** | `5.6·10⁻⁴` | **`3.3·10⁻⁵`, `[517.128526, 517.128559]`** |
| (LKSE)₃, P3's split | 4.487 | 1.23 | 400 000; 1 200 | 0.64 | **0.169**, `[655.522897, 655.691668]` |
| (LKSE)₃, split around the anchor | 4.301 | 1.23 | 4 000 000; 12 000 | 0.188 | **0.041**, `[655.592089, 655.632643]` |

* **Lysine.**  The inner sandwich pays only the envelope, whose bracket is `10⁻⁵` nats; `E_q ρ = 5·10⁻⁵`; the sampler
  asks for 19 (60) evaluations and the width is the proposal term.  Predicted before the run: `2·10⁻³` as stated,
  `1·10⁻³` two-end, `4·10⁻⁴` with empirical Bernstein if the standard deviation of `b` were 0.2 (it is 0.097).
* **The mixed-charge sequence.**  My guess for its envelope bracket was 0.1 nats; it is 1.23 — the envelope, the
  smallest valid penalty, delocalises as the floor does (nine side chains off the anchor among the proposals) — and
  the first run gave 0.17 nats where I had written 0.03–0.04.  The second run was predicted at 0.05 and gave 0.041.
  The plain sampler (Proposition 11.113) with the same evaluations: 1.18 and 0.18 nats (empirical Bernstein).
* **For your §11.113a text:** a sandwich 4.5 nats wide is usable when proposals are cheap — the criterion of
  SCI-REV-0015 (`2√(N/N_f) + ρ̄ < 0.878`) in a regime where the deterministic bracket no longer matters.

## 5. Thirty residues at order 6 — the item SCI-RES-0017 left open [M]

Ace-Leu₃₀-NMe on the helix (`1.07·10⁹` states), order 6 (ball 174 437), band 20, workstream P3's reduced models,
`βΓ₆ = 54.8`: equal site shares 0.730 nats; "most frozen first" at both ends 0.084; **Frank–Wolfe floor and
best-ordering ceiling `[866.910485, 866.921008]`, 0.0105 nats** (six Frank–Wolfe steps, duality gap `8.8·10⁻⁴`; the
a-priori bound of SCI-RES-0017 §3: no site allocation has a floor below `866.920625`).  At order 5 the best we had
was 0.070 nats, by intersecting two forms.  At most 0.0097 of the 0.0105 is the reduction of evaluated terms
(the penalty-free minorant is `866.920168`).  The split of §3 was not run here (leucine is apolar; valine gained
nothing).

## 6. Your head `9befefd`

Nothing that `audit_all.sh` builds or runs changed between `f7df44f` and `9befefd` (no file under `proofs/`,
`scripts/`, the lake files, or `experiments/` outside your new `three_levels_certified/`); the one audited input
that changed, the documents, passes `check_doc_refs.py` on an archive of `9befefd` here (2 811 declarations
indexed).  We did not re-run the full script at this head; the run at `f7df44f` (SCI-RES-0018 §2) stands for the
identical inputs.  The review of THY-RES-0013 §4 that we accepted is running (workstream R16) and will come as
SCI-REV-0016.

## 7. Requests (none is an authorisation to spend anything)

**To the theory division**

* **P8-T1 (the remainder identity with a term-dependent order).**  *Statement.*  `F = Σ_τ F_τ` on a finite product,
  anchor `x⁰`, for each `τ` a total order `≺_τ` of the sites.  Then for every `x`, `m ≥ 1`:
  `F(x) − I_{m−1}F(x) = Σ_τ Σ_{T⊆S(x), |T|=m} Δ_T F_τ(z^{T,x,τ}; x_T)`, `z^{T,x,τ}_i = x_i` if `i ≺_τ min T`, else `x⁰_i`.  If `≺_τ` puts a
  set `H_τ` of **at most `m`** sites last, every site of `H_τ ∖ T` is at its anchor in all evaluations; with `m + 1`
  sites this fails.  (Your `higherOrder_remainder` is the case of one order and class constants.)  *Validation.*
  `ws_P8/p8_10_order_identity.py` (62 400 checks of the identity); `p8_verification/ah_synthetic_test.py` (the
  consequence, with controls).  *Stopping condition.*  A Lean statement next to `higherOrder_remainder`, or a
  counterexample.
* **P8-T2 (the least sign-blind bound for a cluster with a net charge).**  Workstream P5's Theorem 9: the sign-blind
  class loses without bound on neutral clusters.  For lysine the measured loss is 3–7.  *Question.*  Is there a
  statement "`SB(Φ) ≤ C·(Σ|q|/|Σq|)²·Φ(g)`" for GB-type functions whose charges inside the range of the kernel are
  dominated by one sign?  *Validation case.*  Lys₅, `m = 4` (largest remainders: truth 0.0250, all charges positive
  0.111, best sign pattern found 0.127 kcal/mol; `ws_P8/out/sb_K5_H_0.70.json`).
* **A18-T1 (the split of §3 as a lemma).**  Two lines; if you keep a list of valid reductions of a term to fewer
  sites, this is the anchored one for pairs.  (We have not read your `BlockReductions.lean`; it may already be there.)

**To the engineering division**

* **P8-E2 (the state-wise constants inside the pipeline; a hybrid for long chains).**  For `n ≤ 12–16`: enumerate the
  subsets, `p8sr.BlockBound.total_T_blocks(m, T)['SAb']` (0.05–0.15 s per subset at 276 atoms).  Beyond: `Σ_T ĉ^{AH}_T` in
  closed form minus `ĉ^{AH}_T − ĉ^{SAb}_T` for the subsets inside a window.  *Stopping condition.*  One charged instance
  beyond twelve residues.
* **P8-E4 (penalties resolved by rotamer state).**  In the proof of Theorem AH the host states of a term are those of
  the state itself before the maximum is taken; a site or pair penalty that keeps the dependence on the host's
  rotamer is a table and fits the band models as they are.  *Why.*  §2, item 3: four to five orders of magnitude
  between what the ensemble pays and what a constant per subset charges.  *Stopping condition.*  A measured factor
  on Lys₁₂ at order 4, or a reason why the dependence is weak.
* **A18-E1 (the split of §3 in the models).**  `pi_inference/window_model_occ.py`, 100 lines; for workstream P3's
  reduced models the same effect is obtained by calling `build_band_models` with the far pairs zeroed and adding the
  split's one-site tables.  The certificate checker of SCI-MSG-0025 §8 needs no change in kind: a split is two
  one-site tables per far pair, checked entry-wise against `P`.
* **P8-E3 and A18-E2 (two faults in our own libraries that you inherit if you run them).**  `ws_P5/p5lib.anch_walk`
  leaves one full array per call in a reference cycle (11.7 GB in one of P8's runs; fix: `gc.collect()` after the
  call, as in `ws_P8/p8lib.py`).  `ws_P3/pwmodel.BandModel.sample` recomputes the transfer-matrix messages at every
  call (about an hour instead of 14 s for the proposals of §4 — the first run was stopped after sixteen minutes; fix: compute them once, as in
  `pi_inference/nested_sampler_ext.cached_sampler`).  Neither affects any number.

## Assumptions and limitations

* **Model-relative.**  ff14SB + GBn2, ideal helix, rotamer libraries pruned as in workstream P2, one anchor per
  instance.  Nothing here is a statement about a peptide in water.
* **Not refereed.**  Workstream P8's report, the coordinator's note in it, and addendum A17 (18) have had no referee
  inside our division; the referee of the preceding addenda (R14) was stopped by a platform safeguard before it
  produced anything (reported to the research owner), so A17 (13)–(18) are unrefereed except for Lemma A17.16 and
  the greedy lemma (machine-checked) and SCI-RES-0017 §2 (iii) (reviewed by R15).
* **The constants** 'Sb' / 'SAb' were computed by workstream P8's code only.  My checks are a review of the theorem,
  necessary conditions (every state of three small instances; 4 250 random states of the large one) and re-runs.
  P3's interval enclosures, table allowances and outward rounding are inherited.
* **The samples.**  Gibbs samples of the true ensemble are uncertified; they guide a choice between valid models
  (§3) and serve as states at which sandwiches are checked — no certified number depends on them.  The sampled
  brackets of §4 hold with probability 0.95 *given* the sandwich `m₋ ≤ E ≤ m₊` and the inner sandwich, i.e. given
  the constants; the sampling scheme is the one reviewed in SCI-REV-0015 (number of proposals fixed in advance).
* **One number disagrees with an estimate and is left standing:** P8's uncertified reweighting estimate for
  (LKSE)₃, `655.79 ± 0.09`, lies above both intervals of §4, 1.9 of its standard errors above their point estimates
  (`655.611`, `655.613`).
* **Prior art** outside our own reports was not searched for §3 (it is a one-line consequence of the anchored
  decomposition; no novelty is claimed) nor by P8 for Theorem AH ("not in workstreams P3, P5, P6" is all we say).

## Requested response

Theory: P8-T1 with the hypothesis `|H_τ| ≤ m` (a Lean statement or a counterexample); whether P8-T2 is a question you
want.  Engineering: whether A18-E1 and P8-E2 enter the pipeline, and — unchanged from SCI-MSG-0025 — the checker.
Neither request authorises any spending.
