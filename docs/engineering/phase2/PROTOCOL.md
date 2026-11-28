# Validation protocol of Phase II (Workstream D) — committed before any validation run

*Written 2026-11-28 by the coordinator of the Computational Research Division, after the prototype's
unit tests passed and before any of the runs below.  Not edited afterwards except for the section
"Deviations".  The runs are carried out by a subagent; the coordinator reviews code and results.
Mathematics and notation: `CERTIFIED_INFERENCE.md`.  Library: `src/metricchain_eng/certinf/`.*

## 1. What is evaluated

The **identified interval** `I = [V⁻, V⁺]` of a target average over a class of ensembles compatible with
measured averages, and methods that bound it from samples.  Ground truth is always the exact interval
on an enumerated (or exactly lumped) space.  "Covers" means: the reported interval contains `I`.
Confidence `1 − δ` with `δ = 0.05` everywhere (each end at `δ/2`).

## 2. Instance families (all deterministic from the seeds stated in the code)

| | family | size | reference | measured `φ` (scaled to `[−1,1]`) | target `f` |
|---|---|---|---|---|---|
| F1 | Ising ring | 14 spins, 16 384 states | ring, coupling 0.4, field 0.1 | magnetisation; nearest-neighbour correlation | next-nearest-neighbour correlation; and `|magnetisation|` (not additive) |
| F2 | rotamer-like Potts | 7 sites × 4 states, 16 384 states | random one-body and pair energies | three one-site populations | one two-site population |
| F3 | lattice chain | self-avoiding walks of 7 steps on the cubic lattice, 81 390 conformations | contact energy −0.5 per non-bonded contact | three squared distances between beads (correlated errors: an ellipsoid) | the stress observable `tr(XᵀΩX)` of the lowest-energy conformation (geometry division's Theorem G); squared radius of gyration |
| F4 | large product | 100 binary sites (`2^100` states) | product, site biases in `[0.2, 0.8]` | ones in the first 50 sites; ones in the last 50 | fraction of ones in the first 20 sites; exact by level counts (Proposition 8.1) |
| F5 | bounded influence | cube, 8 and 12 sites (programme); 50 and 200 sites (Corollary 9.3) | product | two additive observables | additive; one spin; a two-spin product |
| F6 | model-free controls | the ensemble division's frozen instances with stored exact intervals (`controls_v1.json`, B5-01/02/03) | — | theirs | theirs: reproduce the stored intervals with `l ≡ 0` |

Envelopes: uniform half-width `ρ ∈ {0.2, 0.55, 1.15, 1.7, 2.3}` (`Γ = e^{2ρ} ≈ 1.5, 3, 10, 30, 100`); for
F1 also a state-dependent `ρ(x)`.  Data: the measured averages of a "true" ensemble
`p_true ∝ π·e^{−R}` with a fixed `R` inside the envelope, in a box of half-width 0.03 (F3: an ellipsoid
with correlated covariance of comparable size).  Sample sizes `n ∈ {10³, 10⁴, 10⁵}`; repetitions 200
(50 at `10⁵`).  The training part of a split is `min(n/2, 5000)` draws.

## 3. Methods

| | method | access |
|---|---|---|
| M0 | exact dual on the whole space (ground truth; cross-checked against the primal programme on F1, F2) | everything |
| M1 | S3 as proposed, covering-net allowance | exact `b`, `G`; draws from the gap distribution |
| M2 | S3 with the allowance of Theorem 3.1 | same |
| M3 | sampled dual certificate with the product test (Theorem 5.1), reference sampling | draws from the reference |
| M4 | the same test with gap sampling and exact `b`, `G` | as M1 |
| M5, M6 | M3 with Hoeffding, with empirical Bernstein, in place of the product test (a grid of 32 thresholds, union bound) | as M3 |
| B1 | plug-in sharp bounds on the sample with a percentile bootstrap (200 resamples) — the practice for the marginal sensitivity model | as M3 |
| B2 | maximum-entropy reweighting to the centre of the data: one ensemble, one number | as M3 |
| B3 | model-free linear programme on the sampled pool (`l ≡ 0`) | the pool |
| B4 | information bound: `E_p f − E_π f ≤ inf_c [ln E_π e^{c(f − E_π f)} + ρ²/2]/c`, exact on the space, no data | everything |
| B5 | the archive's bracket: the threshold rule without data (`m = 0`), exact | everything |

Matched resources: all sampled methods get the same number of draws; M1, M2, M4 additionally get `b`
and `G` exactly, which is recorded as an advantage, not hidden.

## 4. What is reported, per family × envelope × sample size × method

Coverage of `I`; coverage of the true value; median and 90th percentile of the width and of the excess
over `I` at each end; rate of trivial ends, abstentions and voids; wall time split into preprocessing
(exact `b`, `G`, or level counts), sampling, optimisation and certification; peak memory; for
inconsistency: detection rate against the displacement of the region, and false-alarm rate.
Sensitivity runs: (a) the true ensemble outside the declared envelope (true half-width `2ρ`);
(b) no observation, one observation, uninformative observations; (c) a region displaced by
`0.05 … 0.5` outside the reachable set.

## 5. Hypotheses, fixed now

* **H-A (S3 is sound).**  M1 and M2 cover in every repetition on F1–F3.  *Refuted by* one miss.
* **H-B (S3 is far from efficient).**  At every `n`, on F1–F3, for `Γ ≥ 3`: the median excess of M1 is at
  least 5 times that of M3, and M1's interval is trivial (the whole range) at `n = 10³` for `Γ ≥ 10`.
  *Refuted by* one cell where the ratio is below 5 while M3's interval is not trivial.
* **H-C (Theorem 5.1 is valid).**  The miss rate of each certified end of M3 and M4 is at most
  `δ/2 + 3√(δ/2·(1−δ/2)/reps)` in every cell.  *Refuted by* one cell above.
* **H-D (cost linear in `Γ`).**  On F1 at fixed target excess 0.05, the least `n` at which M3's median
  excess is below it grows like `Γ^γ` with `0.7 ≤ γ ≤ 1.3` over the five envelopes.
* **H-E (the product test beats the standard inequalities).**  At every cell where M3 is not trivial,
  median excess M3 ≤ M6 ≤ M5.
* **H-F (established practice).**  (i) B1's nominal 95 % interval misses an end of `I` more often than
  5 % in at least one cell at `n = 10³` with `Γ ≥ 10`.  (ii) B2's number lies inside `I` whenever the
  data are consistent, in at least 95 % of repetitions.  (iii) B3's interval on the pool is at least
  twice as wide as `I` for `Γ ≤ 10` on F1–F3.
* **H-G (what data add).**  B5's exact interval without data is at least 1.5 times as wide as `I` on
  F1–F3 for `Γ ≥ 3`; B4's is wider than B5's in every cell.
* **H-H (inconsistency).**  With the region displaced by at least 0.2 and `Γ ≤ 3`, M3's inconsistency
  certificate fires in at least 90 % of repetitions at `n = 10⁴`; with consistent data it fires in at
  most 5 %.
* **H-I (a wrong envelope is not detected by the interval).**  With the true half-width twice the
  declared one, the certified interval of M3 misses the true value in more than 10 % of repetitions in
  at least one cell; no prediction on how often the inconsistency certificate fires.
* **H-J (bounded influence).**  On F5 the formula of Corollary 9.3 equals the programme at 8 and 12
  sites to `10⁻⁶`; at 200 sites it runs in under 10 s; the box hull of the class gives an interval
  within `10⁻³` of the whole range from 20 sites on, for slope 0.5 per site.
* **H-K (exactness at scale).**  On F4 the exact interval by level counts takes under 60 s; M3 at
  `n = 10⁵` covers it with median excess below 0.05 for `Γ ≤ 3`.

Analysis fixed in advance: the tables of §4; no method is tuned on the outcome; the bets of the product
test, the split and the grid of M5/M6 are as coded before the runs.

## 6. What this cannot show

Everything is a statement about synthetic models with envelopes that hold by construction.  Nothing here
is evidence about a molecule, and no envelope between a force field and experiment is claimed.  The
sealed held-out list is not involved in any way.

## 7. Deviations

*(none at the time of writing — the entries below were added on 2026-11-28 after the runs; nothing above
this section was edited)*

Recorded after the runs.  The campaign's own list, with reasons, is `experiments/eng/certinf/REPORT.md`
§2 (D1–D16); outcomes and their reading are in `RESULTS.md`.

1. **Repetitions** (D1): 100 at `n = 10³` and `10⁴`, 30 at `10⁵`, instead of 200 and 50 — runtime.  The
   threshold of H-C is computed with the actual numbers.
2. **Baselines restricted** (D2, D3): the bootstrap B1 only at `n = 10³` on F1, F2 and one cell of F3; the
   pool programme B3 on F3 only for one target at `n = 10³`, `Γ ≤ 10` — runtime.
3. **Choices the protocol left open** (D5, D11, D12): the sizes and cells of the sensitivity runs; the
   state-dependent envelope of F1; the shape of the true residual; data regions centred at the exact
   averages of the true ensemble, with no simulated measurement noise.
4. **H-D** (D6): the least `n` was located by a separate sweep (ten sample sizes, 20 repetitions), because
   the grid's three sizes cannot locate it.
5. **Readings of criteria** fixed by the campaign before its tables (its §2): "excess" is the sum over
   both ends; envelope thresholds refer to the nominal ratios; the inconsistency certificate is one test
   at `δ = 0.05` (D9).
6. **The library changed during the campaign** (D16), at 02:35:33 UTC, in answer to the independent
   review: certificates unchanged for valid input; model-free problems on a region that is not a box are
   now solved correctly.  The grid ran before the change.  **The baseline B3 on F3 had been too wide —
   in favour of the hypotheses — and was recomputed on the same draws**; the superseded values are kept.
7. **The exact reference on F3** (D10) was not independently checked by the campaign; the coordinator
   verified it afterwards (`experiments/eng/phase2_coord_checks/`).
8. **Outside the protocol:** the supplementary experiments S1 (draws from the extremal ensemble) and S2
   (references that are not products) were designed after the review and after the first results were
   known.  They are reported as such in `RESULTS.md` §4 and decide no hypothesis.
9. **A count corrected by the coordinator:** H-F(i) is met in 8 of 10 cells, not 9 as the campaign's table
   says (one cell is at exactly 5 misses in 100).
