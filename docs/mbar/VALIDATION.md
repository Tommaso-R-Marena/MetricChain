# Division 9 — practical validation

*All numbers are in `VALIDATION_TABLES.md`, generated from `experiments/mbar/results/` by
`bench/make_tables.py` (tables T1–T10).  This file says what was run, what it shows, and what it does
not show.  Everything except §6 is on synthetic systems with exact independent samplers and exactly
known free energies; §6 is a public data set without ground truth.  **All of it is development
evidence: no protocol was frozen in advance, and two variants in §3 were added after seeing results
(marked post hoc).**  Machine: 4 cores, local; no Modal job, no external computation.*

## 1. Correctness of the code against independent references

| check | result | where |
|---|---|---|
| four mathematically independent routes to the variance (closed form; stable formula A3; `J × J` dual; constrained least squares without the Laplacian) | agree to `3·10⁻¹²` on 400 random models | `tests/test_population.py` |
| gradient `−Var_k(z)` against finite differences | relative error `2·10⁻⁸` | same |
| convexity of `V`, concavity and superadditivity of `1/V`, monotonicity | no violation above `3·10⁻¹⁵` in 600 random pairs | same |
| optimal allocation: multiplicative iteration against two conic programmes (group norm; dual) | agree to `2.4·10⁻⁷`, 40 models with random costs | same |
| MBAR solver against PyMBAR 4.0.3 | `4·10⁻¹³` (harmonic test), `4·10⁻¹¹`–`4·10⁻⁷` (public data) | `tests/test_certificates.py`, T8 |
| plug-in variance (Theorem A3 on the fitted distributions) against PyMBAR's standard errors | 13 digits | `RESEARCH_LOG.md`, cycle 1 |
| e-value identity `E = exp(−N·KL(s‖a))` and `E ≤ 1` for arbitrary predictors and tilts | exact enumeration of all samples on small models: identity to `2·10⁻¹⁵`, `max E = 0.9999992` | `tests/test_certificates.py` |
| lower-bound construction, adaptive information bound, correlated-sampling statements | T9 | `bench/check_lower_bounds_and_chains.py` |

The handoff's reference implementation was run unchanged as a baseline (C1, C2) and its own test
suite was not modified.

## 2. Confidence statements (T1)

Eleven regimes (discrete four-state models with overlap 0.05 and 0.35; harmonic ladders with 2, 5, 10
states; 100 to 10 000 samples per state), 200 repetitions each, six methods on the same samples.

* **Likelihood-ratio region (B2), 8 batches:** covered the true contrast, and all free energies
  jointly, in 2200 of 2200 repetitions; never abstained; median width 2.05–3.05 times the width of
  `±1.96·se`.  The 2-batch (split) version is 7–28 % wider.  Median time 0.01–0.43 s per region.
* **Handoff C1:** `+∞` in every repetition of 4 regimes; 1.4–5.8 times wider than LR8 in the others.
* **Handoff C2** (pilot = first half): always finite, 2.4–8.3 times wider than LR8.
* **Asymptotic interval:** coverage 0.940–0.975.  **Bootstrap** (40 repetitions): 0.925–1.000.
  On these well-behaved systems the uncertified intervals are fine; the certified region costs a
  factor 2–3 in width and buys a guarantee that does not depend on `N` being large enough.

What this does not show: behaviour for `K ≫ 10` (see §6: the ratio grows to 5–7 at `K = 26`), and
anything about correlated samples (§5).

*Rerun after two corrections of the interval code* (`DEAD_ENDS.md` E7: unconverged profile solves are
now counted as inside the region; a batch is never dropped on its own data): the whole benchmark was
repeated with the corrected code (`results/certificates_coverage_v2.json`); coverage, numbers of finite
intervals and median widths of LR8 and LR2 are identical in all eleven regimes, i.e. neither hole was
exercised by the stored runs.

## 3. Pilot-based allocation: actual errors at matched cost (T2, T3)

Eight systems; total budget 3000 × mean cost; 2000 independent replicates per system and method;
every method ends with the same estimator (MBAR on all its samples).  The comparison is of the
mean-square error of the final estimate, not of population variances.  Baselines: equal counts
(identical to standard PyMBAR practice; the solvers agree to `10⁻¹³`), equal cost, the one-step
Neyman rule that is correct for EMUS, the earlier programme's resistance criterion, and the oracle
design computed from the true distributions (unattainable reference).

| system | what it is | oracle (predicted) | two-stage rule, measured | verdict |
|---|---|---|---|---|
| bottleneck | six states, one weak link | 0.764 | 0.758 [0.70, 0.82] | gain realised (24 %) |
| widths | five states of different widths | 0.914 | 0.896 [0.82, 0.98] | small gain (10 %), just significant |
| costly ends | end states 20× more expensive | 0.129 | 0.166 [0.15, 0.18] | 6× against equal counts; 9 % against equal cost |
| costly middle | middle state 20× more expensive | 0.199 | 0.292 [0.27, 0.32] | 3.4× against equal counts; short of the oracle |
| homogeneous | well-designed ladder (control) | 0.942 | 0.920 [0.85, 1.01] | no detectable gain; no loss |
| Dirichlet 0 / 1 / 2 | random 12-point models | 0.459 / 0.673 / 0.960 | 0.480 / 0.706 / 0.888 | gains realised where predicted |

Findings.
1. **The plug-in design from a 20 % pilot realises the gain the theory predicts, where there is one**,
   and does no harm where there is none (the safeguard).  Two-stage and four-stage rules are
   indistinguishable.
2. **It beats the one-step Neyman rule in every system with a real gain, and the resistance criterion
   in most** (`DEAD_ENDS.md` N9, N10).
3. **With unequal costs most of the gain is already obtained by equal cost per state**; the design
   adds 9 % (costly ends) and 9 % (costly middle).  The equal-count pilot and the equal-count
   safeguard waste budget on a costly state that the optimal design never samples.  *Post hoc
   variants* (T3): a cost-aware pilot (`PILOT2C`: 0.148 and 0.265) and, in addition, an equal-cost
   safeguard (`PILOT2CE`: 0.141 [0.13, 0.15] and 0.226 [0.21, 0.25], against the oracle's 0.124 and
   0.205 and the equal-cost rule's 0.182 and 0.321).  Because they were introduced after the first
   results they need an independent confirmation on a protocol frozen beforehand.
4. Optimal designs sit on the boundary: in "costly ends" the oracle design puts **all** samples on
   two cheap intermediate states and none on the two end states whose free-energy difference is the
   target, nor on the middle state.
5. Overhead: the allocation step (MBAR fit of the pilot + convex optimisation on the pooled pilot
   points) takes 0.01–0.09 s; no pilot fell back to uniform in 16 000 replicates.
6. The certified efficiency bound of the uniform allocation (computed from the true distributions) is
   0.49 for the bottleneck system where the true efficiency is 0.76: valid, not tight.

What this does not show: gains with a real sampler.  In molecular dynamics the cost per effective
sample depends on the state through the correlation time, which the pilot must estimate; that
experiment is proposed in MBAR-REQ-0001 and was not run.

## 4. Every round, adaptive allocation, optional halting (T5)

Twelve rounds of 400 samples; each round's allocation from the plug-in design of the earlier rounds;
region recomputed after every round; sampling "halts" when the interval is below a target width.
300 repetitions per overlap.  The truth left the region at some round in 0.0 % (overlap 0.35) and
1.7 % (overlap 0.05) of the repetitions — the guarantee is 5 % *simultaneously over all rounds*; at
the halting round the interval covered in every repetition.

## 5. When the assumptions fail (T6, T7)

* **A trapped sampler** (T6).  One umbrella of five confined to one well: MBAR's error in the affected
  free energy is 0.60 kT, and both the certified region and the asymptotic interval exclude the truth
  in *every* repetition — as they must, since their assumption is false.  The model check (B5) with a
  24-bin histogram predictor rejects in 37 % of the repetitions at 200 samples per state and in 100 %
  at 1000, with no false alarm in 600 repetitions under correct sampling.  With *all* umbrellas
  confined to the same well nothing rejects (0 of 600) and the error is 7.6 kT: consistent trapping
  is invisible (B7).
* **Correlated samples** (T7).  Stationary AR(1) samplers with contraction `φ`.  Treated as
  independent, the asymptotic interval covers in 36 % (`φ = 0.9`) of the repetitions; thinned by an
  *estimated* statistical inefficiency, in 83 %; thinned by the known integrated autocorrelation time,
  92 %; thinned until the remaining correlation is below 0.01, 97 %.  The likelihood-ratio region
  covered in 98.7–100 % in all four treatments; this reflects its width, and — for time-ordered
  batches — a regret that grows when earlier batches predict later ones badly; **it is not a
  guarantee for correlated data** (B7c gives the only guarantee: thinning under an assumed mixing
  rate).  At `φ = 0.99`, treated as independent, the region's *joint* coverage was 92.3 % — below
  nominal — and the asymptotic interval's 12 %; with the estimated inefficiency the asymptotic
  interval covered in 70 %, the region in 99 %; with certified thinning both were at or above 95 %.

## 6. Public data: umbrella sampling of a valine side-chain torsion (T8)

26 umbrellas, 501 snapshots each (`experiments/mbar/data/pymbar_umbrella/README.md`); no ground truth.

* Our solver and PyMBAR agree to `4·10⁻¹¹` kT on the decorrelated data.
* The joint region is finite in all three treatments of time correlation.  Its intervals are 4.6–7.1
  times wider than `±1.96·se`: with 25 nuisance directions the regret is 32–59 nats.  For adjacent
  umbrellas the sub-ladder restriction (Proposition B2′) gives 1.9–2.2 times the asymptotic width; for
  a pair 13 umbrellas apart it gives no improvement.
* The model check does not reject, and with this predictor it could not be expected to (N13).
* Design diagnostic (plug-in, not a certificate): for the free-energy difference between the trans
  and gauche⁻ rotamers in the *unbiased* ensemble, the plug-in optimal design concentrates 84 % of
  the samples on the six umbrellas between −165° and −90° and predicts the same precision from 37 %
  of the samples.  This is a prediction from one data set.  It is the kind of statement the
  proposed computational phase would test.

## 7. Summary against the directive's list of measurements

| measurement | where | result in one line |
|---|---|---|
| actual error and RMSE | T2, T3 | pilot-based design: MSE ratios 0.17–0.90 against equal counts where a gain is predicted; 0.92 (n.s.) on the control |
| coverage and width | T1 | certified region: 100 % coverage, 2.0–3.1× the asymptotic width (`K ≤ 10`); 4.6–7.1× at `K = 26` |
| abstention | T1, tests | region: none in 2200 repetitions with overlapping supports; `±∞` when supports are separated; C1 abstains in 4 of 11 regimes |
| effort for a given precision | T2 | equal to the MSE ratio (same estimator, same budget) |
| pilot and allocation overhead | T2 | 0.01–0.09 s per allocation; 20 % pilot |
| computational cost | T1 | region: 0.01–0.43 s for `N ≤ 40 000` (median); asymptotic: 0.002–0.07 s |
| weak overlap | T1 | region stays finite and valid at overlap 0.05 with 100 samples per state (width 2.9 kT); C1 infinite |
| correlated samples, missed regions | T6, T7 | no guarantee; trapping of one state detected by the model check; consistent trapping undetectable |
