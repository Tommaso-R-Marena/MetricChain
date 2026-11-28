# Certified inference from multistate samples — compositions with free-energy estimation

*Computational Research Division, Phase II, addendum under the research owner's directive D-12
(`../DIRECTIVES.md`), 2026-11-28.  Written after `FINAL_REPORT.md`; it changes nothing there.  Epistemic
labels as in `docs/collaboration/README.md`.  **Every statement below is a paper proof of this division,
unrefereed** unless a different status is given; the numerical checks are named with each statement.
Software: `src/metricchain_eng/certinf/multistate.py`; tests `tests/eng/test_certinf_multistate.py`;
experiments `experiments/eng/phase2_mbar/` (predictions written before the runs: `PREDICTIONS.md` there).*

## 0. What this note establishes, in plain words

The directive asks whether the work of the new division on multistate free-energy estimation
("certified MBAR") composes with our certified ensemble inference, in substance and not in name.  That
division had, when this was written, imported a package of proposed theorems and had no result of its
own yet.  So this note does what can be done from our side: it states the compositions precisely, proves
them, tests them on models where everything is known exactly, and says what each needs from a
free-energy certificate.

1. **Uncertainty of the free energies acts exactly like an energy envelope (Theorem M1).**  Our
   certificates need the sign of one expectation under the target state.  With draws from several
   states that expectation is taken under the sampling mixture, weighted by the density ratio of the
   target against the mixture, which depends on the unknown free energies.  If those are enclosed in
   intervals, the ratio is enclosed pointwise between two computable functions, and the whole
   construction of Theorem 5.1 goes through with the envelope enlarged by that enclosure.  The levels
   add.  Where the target state dominates the mixture the enclosure is tight whatever the intervals.
2. **It turns multistate data into certified statements about rare regions, and the quality of the
   free-energy region decides how good they are.**  Measured on enumerable models, for an event of
   probability `9.4·10⁻⁷`: with bridge intervals summed along the ladder of windows the certified upper
   bound is ×5.9 the exact value at 40 000 draws and ×2.2 at 200 000; with the likelihood-ratio region
   that the MBAR division published during this cycle (its Theorem B1; re-derived, implemented and tested
   by us) it is ×1.5 and ×1.2; from the same number of draws of the target state alone it is ×333 and ×67
   (§8).  **It does not help for common observables** (the draws spent on other states are lost), and it
   fails for events on which the density ratio of the target against the mixture is very uneven (§4).
3. **A shared energy error largely cancels between overlapping states (Proposition M2).**  If two states
   carry the same error of size at most `ε`, their free-energy difference moves by at most
   `ln(1 + (e^{2ε} − 1)·TV)`, where `TV` is their total-variation distance — not by `2ε`.  For small `ε`
   this is `2ε·TV`, and it is sharp to first order.  For the usual overlap of adjacent windows the gain is
   a factor of about 0.6; for distant states there is none.
4. **Without free energies, states cannot cooperate in a certificate (Proposition M3).**  A sign test
   can pool states without any normalising constant, but then it is never better than the best single
   state.  The mixture form of Theorem M1 is the one in which a state that sees the rare region and a
   state that sees the bulk help each other, and its price is the free-energy intervals.
5. **Limits.**  Synthetic enumerable models with exact, independent draws.  Nothing here concerns a
   molecule, a force field or a correlated trajectory.  The bound that the certificate needs on the
   density ratio over the event must come from analysis of the bias functions; here it comes from
   enumeration.  One pre-registered design choice of ours (how to pick the windows to pool) performed
   badly and is reported as such; one defect of our own implementation of the likelihood-ratio region was
   found during the cycle, because the certificate refused its output, and repaired (§8.2).

## 1. Setting

States `j = 1, …, K` on a common measure space `(X, μ)`: unnormalised densities `q_j ≥ 0`,
`0 < Z_j = ∫ q_j dμ < ∞`, `p_j = q_j / Z_j`, `f*_j = −ln Z_j` (the notation of the MBAR package).  The
sample is stratified: `n_j` independent draws of `p_j`, `N = Σ n_j`, `s_j = n_j / N`; `m = Σ_j s_j p_j` is
the sampling mixture.  The target state `k` has `s_k > 0`.

Around the target, the class of `CERTIFIED_INFERENCE.md` §1 with envelopes proportional to `q_k`:
`P_k(λ, υ) = { p : dp ∝ w dμ, λ q_k ≤ w ≤ υ q_k }` for bounded measurable `0 ≤ λ ≤ υ`.  An error
`d(x) ∈ [−ε, ε]` of the reduced energy of the target is `λ = e^{−ε}`, `υ = e^{ε}`, envelope ratio
`Γ = e^{2ε}`; `λ = υ = 1` is the model itself.  Measured averages `E_p φ ∈ R` (`R` compact convex with
support function `h_R`), target `f`, score `s_{τ,η} = f − τ − η·φ + h_R(η)`, and `s⁰ = s_{0,η}`.
`V⁺ = sup{ E_p f : p ∈ P_k(λ, υ), E_p φ ∈ R }`.

*Weak duality (Theorem 4.1(a) of the main note), in one line.*  Put
`Ψ_k(τ, η) = ∫ q_k [υ (s_{τ,η})₊ − λ (s_{τ,η})₋] dμ`.  If `Ψ_k(τ, η) ≤ 0` then `V⁺ ≤ τ`: for `p` in the class
with weight `w`, `∫ w s ≤ ∫ [υ q_k s₊ − λ q_k s₋] ≤ 0`, so `E_p f ≤ τ + η·E_p φ − h_R(η) ≤ τ`.  Hence
`τ < V⁺` implies `Ψ_k(τ, η) > 0`, and by continuity `Ψ_k(V⁺, η) ≥ 0`.

## 2. Theorem M1: uncertainty of the free energies is an envelope

**Theorem M1.**
*(a) Identity.*  With `W_k = p_k / m = e^{f*_k} q_k / Σ_j s_j e^{f*_j} q_j ≤ 1/s_k`: for every `g` with
`∫ q_k |g| < ∞`, `∫ q_k g dμ = Z_k E_m[W_k g]`, and the pooled sum of the stratified sample satisfies
`Σ_n E[W_k(x_n) g(x_n)] = N E_{p_k} g`.

*(b) Enclosure.*  For any centre `f⁰ ∈ ℝ^K` put `h = f* − f⁰`,
`W⁰ = e^{f⁰_k} q_k / Σ_j s_j e^{f⁰_j} q_j` and `ω_j = s_j e^{f⁰_j} q_j / Σ_r s_r e^{f⁰_r} q_r`.  Then

    W_k(x) = W⁰(x) ρ(x),        ρ(x) = 1 / Σ_j ω_j(x) e^{h_j − h_k}.

If `a_j ≤ h_j − h_k ≤ b_j` for every sampled `j` (`a_k = b_k = 0`), then
`ρ_lo := 1 / Σ_j ω_j e^{b_j} ≤ ρ ≤ 1 / Σ_j ω_j e^{a_j} =: ρ_hi` pointwise, and `W⁰ ρ_hi ≤ 1/s_k`.

*(c) Certificate.*  Split the draws into a pilot part and a validation part.  From the pilot alone fix:
the centre `f⁰`, the multipliers `η`, the start `τ_lo` of a bracket `[τ_lo, τ_hi]`, a number `B > 0` and bets
`λ_1, …, λ_R ∈ (0, 1/B)`.  From the validation part compute intervals `[a_j, b_j]` that contain all
`h_j − h_k` with probability at least `1 − α_f`, and with them

    L = W⁰ ρ_lo λ,     U = W⁰ ρ_hi υ,     z̄_τ = U (s⁰ − τ)₊ − L (τ − s⁰)₊.

Abstain if `sup_x U(x)(s⁰(x) − τ_lo)₊ > B`.  Otherwise return

    τ̂ = inf{ τ ∈ [τ_lo, τ_hi] : mean_r Π_n (1 − λ_r z̄_τ(x_n)) ≥ 1/δ }     (product over the validation draws),

or nothing if the set is empty.  Then **the probability that a value `τ̂ < V⁺` is returned is at most
`α_f + δ`.**

*Proof.*  (a) `m W_k = p_k`, and `Σ_n E[W_k g](x_n) = Σ_j n_j E_{p_j}[W_k g] = N ∫ m W_k g = N E_{p_k} g`.
(b) `W_k / W⁰ = e^{h_k} Σ_j s_j e^{f⁰_j} q_j / Σ_j s_j e^{f⁰_j + h_j} q_j = 1 / Σ_j ω_j e^{h_j − h_k}`; the
bounds follow because the `ω_j` are non-negative and sum to one; and
`W⁰ ρ_hi = e^{f⁰_k} q_k / Σ_j s_j e^{f⁰_j + a_j} q_j ≤ 1/s_k` since the term `j = k` alone is `s_k e^{f⁰_k} q_k`.
(c) Condition on the pilot.  Let `z_τ = W_k [υ (s⁰ − τ)₊ − λ (τ − s⁰)₊]`, so that by (a)
`Σ_n E z_τ(x_n) = N Ψ_k(τ, η) / Z_k`.  Let `E_f` be the event that the intervals hold; on it `z_τ ≤ z̄_τ`
pointwise by (b).  The wealth `W̄(τ) = mean_r Π_n (1 − λ_r z̄_τ(x_n))` is continuous and non-decreasing in
`τ`, because `z̄_τ` is non-increasing in `τ`.  Put `τ° = min(V⁺, τ_hi)`.  If a value `τ̂ < V⁺` is returned then
`τ̂ ≤ τ°`, hence `W̄(τ°) ≥ 1/δ`; and `Ψ_k(τ°, η) ≥ 0` by §1.  On `E_f`, when the procedure does not abstain,
`z_{τ°}(x) ≤ z̄_{τ°}(x) ≤ U(x)(s⁰(x) − τ_lo)₊ ≤ B` for every `x`.  Now either `sup_x z_{τ°}(x) ≤ B` — a
property of the truth and the pilot — or not.  If not, the event "`E_f` and no abstention" is empty.  If so,
`W(τ°) = mean_r Π_n (1 − λ_r z_{τ°}(x_n))` is a non-negative random variable with

    E W(τ°) = mean_r Π_n (1 − λ_r E z_{τ°}(x_n)) ≤ mean_r exp(−λ_r N Ψ_k(τ°, η)/Z_k) ≤ 1

(independent draws; `1 − y ≤ e^{−y}`), and on `E_f` without abstention `0 ≤ 1 − λ_r z̄ ≤ 1 − λ_r z` factor by
factor, so `W̄(τ°) ≤ W(τ°)`.  By Markov's inequality the probability of "`E_f`, no abstention, `W̄(τ°) ≥ 1/δ`"
is at most `δ`.  Adding `P(E_f^c) ≤ α_f` proves the claim.  ∎

**Remarks.**
1. *What is new relative to Theorem 5.1.*  With one state (`K = 1`) this is Theorem 5.1 with two
   improvements that the library's `certify_upper` does not have: a bracket that starts at a pilot value
   and a bound `B` on the *product* `U·(s⁰ − τ_lo)₊` rather than on `U` and the range separately.  For rare
   events the second is essential (§4).
2. *Sub-mixtures.*  The theorem holds for the pool of any subset of the sampled states that contains
   `k` (use only those draws and their proportions); the intervals may come from all states.  The pilot
   may choose the subset.
3. *Self-normalisation.*  Only differences `h_j − h_k` enter, and only through the convex combination
   `Σ_j ω_j(x) e^{h_j − h_k}`.  Where the target dominates the mixture (`ω_k(x) ≈ 1`) both `ρ_lo` and `ρ_hi` are
   close to one however wide the intervals are.  A statement about `E_{p_k} f` therefore pays for the free
   energies only where other states carry the sample.
4. *Composition of the envelopes.*  The effective envelope ratio at `x` is
   `Γ(x) ρ_hi(x)/ρ_lo(x) ≤ Γ(x) e^{max_j b_j − min_j a_j}`: a deterministic energy error and the
   statistical uncertainty of the free energies multiply.  If only an oscillation bound `osc(h) ≤ r` is
   available, take `a_j = −r`, `b_j = r`.
5. *Levels.*  `α_f` (free energies) and `δ` (sign test) add; if the region `R` is itself a confidence
   region for measured averages, its level adds as well.  No independence between the three is needed.
6. *The lower end* `V⁻` is obtained by applying the theorem to `−f`.
7. *What the theorem does not need:* the estimator of the free energies need not be the multistate
   estimator, the centre `f⁰` need not be accurate (it affects the width of the intervals for `h`, not
   validity), and nothing is assumed about energies being bounded.  *What it needs:* independent draws of
   exactly the stated laws, exact evaluation of the `q_j` at the draws, and a valid `B`.

## 3. The free-energy intervals: two sources

### 3.1 Bridge intervals with sums along paths

The library computes them by the construction called C2 in the MBAR division's imported package (bounded
bridge averages, a Chernoff interval for each, shortest-path closure), in our own code.  We rely on two
facts and checked both:

* *Bridge identity.*  For any vector `a` and `w_l = e^{a_l} q_l / Σ_r e^{a_r} q_r ∈ [0, 1]`:
  `E_i[w_j] / E_j[w_i] = e^{a_j − a_i} Z_j / Z_i`, because both sides contain `∫ q_i q_j / Σ_r e^{a_r} q_r`.
  **[X]** at the population level on a finite model, to `10⁻¹²` for all pairs (unit test).
* *Chernoff–Hoeffding interval.*  For the average `y` of `n` independent `[0, 1]`-valued draws,
  `{μ : n·kl(y‖μ) ≤ t}` misses the mean with probability at most `2e^{−t}` (**[K]**, Hoeffding 1963,
  Theorem 1).  Coverage checked on non-Bernoulli draws (unit test).

With `|E|` pairs and `t = ln(4|E|/α_f)` all intervals hold together with probability `1 − α_f`, for a vector
`a` fixed independently of the draws used (here: from the pilot).  Differences along a path add, so the
width for a pair of distant states is the sum of the widths of the edges between them.  On the models of
§8 (six windows, total-variation distance 0.5–0.7 between neighbours) the measured half-width for the
farthest window is about `±1.7` at 2 857 validation draws per state and `±0.75` at 14 286.  This accumulation is what
limits Theorem M1 in practice; anything that tightens simultaneous free-energy regions on long chains
transfers to it one for one.  The other items of the package (C1, the B and D series, G1) are neither used
nor checked here.

### 3.2 The likelihood-ratio region (Theorem B1 of the certified-MBAR division)

*Source and status.*  Published on that division's branch at `12af33a`, while §8.1 was being written up: the
ratio of label likelihoods is an e-value under stratified sampling.  Its finite-support core is
machine-checked there (`MBAR.Model.stratified_evalue`, `lr_family_evalue`, `lr_region_coverage`; its axiom
log lists only `propext`, `Classical.choice`, `Quot.sound`).  We read the statements, not the proofs, and
did not rebuild the project; the argument below and the implementation (`lr_intervals`) are ours.  That
division's prior-art note credits universal inference (Wasserman, Ramdas and Balakrishnan) for the version
with random labels; we have not read that literature.

*Statement.*  With `π_j(f, x) = s_j e^{f_j} q_j(x) / Σ_r s_r e^{f_r} q_r(x)` and
`ℓ(f) = (1/N) Σ_n ln Σ_r s_r e^{f_r} q_r(x_n) − s·f`, for any `f′` fixed independently of the draws the set

    C_α = { f : ℓ(f) < ℓ(f′) + ln(1/α)/N }

contains `f*` with probability at least `1 − α`.  *Proof.*  `T = Π_n π_{y_n}(f′, x_n) / π_{y_n}(f*, x_n)`, `y_n` the
state of draw `n`, has `E T = Π_j b_j^{n_j}` with `b_j = E_{p_j}[π_j(f′)/π_j(f*)]`.  Since `π_j(f*) = s_j p_j / m`,
`Σ_j n_j b_j = N Σ_j ∫ m π_j(f′) = N`; by the weighted inequality between the geometric and the arithmetic
mean, `Π_j b_j^{n_j} ≤ 1`.  Markov's inequality, and `ln T = N(ℓ(f*) − ℓ(f′))`.  ∎

`ℓ` is convex, so `C_α` is convex and every difference `f_j − f_k` has a largest and a smallest value on it.
These are the `[a_j, b_j]` of Theorem M1, valid together at the single level `α`: no union over pairs, no
sums along paths.  Each end is computed from above by Lagrangian duality,
`max_C c·f ≤ μ·(ℓ(f′) + ln(1/α)/N − inf_f [ℓ(f) − (c/μ)·f])` for every `μ > 0`, so an inexact search over `μ`
only loosens it; the inner infimum is a floating-point computation (damped Newton with rejection of
anything it cannot vouch for).  Checks (unit tests): the region covers at the stated rate; whenever the
truth is in the region every interval contains it; no point of the region found by line searches exceeds
a bound; an independent constrained optimiser reaches each bound to within 0.2 %; a regression test for
the defect of §8.2.  The enclosing box of `C_α` discards the correlations between the `f_j`; using the
region itself in Theorem M1(b) would be tighter and was not done.

Measured half-width for the farthest window on the models of §8, at the same draws as §3.1: `0.31` and
`0.14` on R14, `0.25` and `0.11` on R10, against `1.75`, `0.78`, `1.63`, `0.71`.

## 4. Which events can be certified: the largest density ratio on the event

The number `B` must bound `U(x)(s⁰(x) − τ_lo)₊` over the whole configuration space.  For an indicator
`f = 1_A` without measured averages this is a bound on `υ·p_k/m` over the event `A`, inflated by the
enclosure.  In an application it has to come from analysis — the bias functions are known and are bounded
on `A` when `A` is a set of values of the biased coordinate — and a draw that exceeds it voids the
statement; in the experiments it is computed by enumeration from pilot quantities times a factor `c`
(twice the inflation that the pilot's own intervals predict), and the run abstains if the certified
envelope exceeds it anywhere.

*How large the sample must be (a heuristic, not a theorem; its only support is the three configurations
below).*  With bets capped at `1/B` the certified value satisfies roughly
`τ̂/(1 − τ̂) ≈ [E_m(U 1_A) + θ·B ln(1/δ)/N_v] / E_m(L 1_{A^c})` with `θ` of order one (`N_v` validation draws).
The first term is the exact answer inflated by the enclosure; the second is negligible when

    N_v · m(A)  ≳  c · ln(1/δ) · sup_A(p_k/m) / avg_A(p_k/m),        avg_A(p_k/m) = p_k(A)/m(A),

that is: the number of pooled draws that fall in the event must exceed `c ln(1/δ)` times the unevenness
of the density ratio on the event.  **This is a supremum, not a variance.**  Measured
(`experiments/eng/phase2_mbar/tail_event.py`; post hoc; Gaussian target, harmonic windows, `Γ = 3`, 18 000
draws, 60 repetitions, median of certified value over exact value; no wrong value and no abstention in any
configuration):

| event | states | `sup/avg` of `p_0/m` on the event | pooled, all states | target only |
|---|---|---|---|---|
| tail `x > 0.68` (`p_0 = 7.7·10⁻⁷`) | target + 5 windows | 383 | ×89 | ×909 |
| thin slice `0.68 < x ≤ 0.70` (`p_0 = 5.6·10⁻⁷`) | the same | 1.4 | ×8.6 | ×1252 |
| tail `x > 0.68` | two more windows covering the far tail | 9.6 | ×16 | ×909 |

Harmonic windows decay faster than the unbiased target beyond the last window, so on an event that
extends past the windows the ratio `p_0/m` grows without the event carrying any mass there.  The
asymptotic variance of the estimate is finite in the first row; the finite-sample certificate is poor.
A set of windows chosen for a certificate has to cover the *whole* event up to a moderate factor.

## 5. Proposition M2: an energy error shared by two states

**Proposition M2.**  Let two states have reduced energies `ũ_i + d` and `ũ_j + d` with the same unknown
`d : X → [−ε, ε]`, and let `p̃_i, p̃_j` be the laws of the model (`d = 0`).  Then

    | (f_j − f_i) − (f̃_j − f̃_i) |  ≤  ln( 1 + (e^{2ε} − 1)·TV(p̃_i, p̃_j) )  ≤  min( 2ε, (e^{2ε} − 1)·TV ).

The exact extreme values are attained at `d = ∓ε` on a level set of `p̃_j/p̃_i` and are computed by one sort
(`shared_error_extremes`).  To first order in `ε` the exact value and the bound both equal `2ε·TV`.

*Proof.*  `Z_i = Z̃_i E_{p̃_i} e^{−d}`, so the change of `f_j − f_i` is `−ln R`, `R = E_{p̃_j} e^{−d} / E_{p̃_i} e^{−d}`.
`E_{p̃_j} e^{−d} − E_{p̃_i} e^{−d} = ∫ (p̃_j − p̃_i) e^{−d} ≤ e^{ε} ∫ (p̃_j − p̃_i)₊ − e^{−ε} ∫ (p̃_j − p̃_i)₋ = (e^{ε} − e^{−ε})·TV`,
and `E_{p̃_i} e^{−d} ≥ e^{−ε}`; hence `R − 1 ≤ (e^{2ε} − 1)·TV`, and the same for `1/R` by symmetry.  `R` is a
ratio of two linear functions of `e^{−d}` on a box, so its extremes are at vertices, and for a fixed value of
the ratio the optimal vertex puts the large weight where `p̃_j/p̃_i` exceeds a threshold.  First order:
`−ln R = ∫ (p̃_j − p̃_i) d + O(ε²)`, maximal at `d = ε·sign(p̃_j − p̃_i)`.  ∎

**Corollary (from samples).**  Let `[l, u]` contain `f̃_j − f̃_i` with probability `1 − α_1` (bridge interval).
Since `1 − TV = E_{p̃_i} min(1, e^{f̃_j − f̃_i} q_j/q_i)` is non-decreasing in `f̃_j − f̃_i`, the average `y` of
`min(1, e^{l} q_j/q_i)` over the draws of state `i` gives `T̄ = 1 − (lower Chernoff end of y)`, and
`[l − β, u + β]` with `β = ln(1 + (e^{2ε} − 1)·T̄)` contains the true `f_j − f_i` with probability
`1 − α_1 − α_2`.  (`l` depends on the same draws; this is harmless because on the first event the average of
`min(1, e^{l} q_j/q_i)` is at most that of the fixed function with the true difference, and the Chernoff
lower end is monotone in the average.)

*Evidence* (`shared_error.py`).  **[X]** 400 random pairs on ten points, four values of `ε`: the closed form
equals the extreme over all `2¹⁰` sign patterns to `1.6·10⁻¹⁴`; no interior error exceeds it; the bound is
never violated; exact over bound: median 0.89, minimum 0.21.  **[X]** on the windows of model R10:

| pair | `TV` | `ε` | exact range of the change | bound | `2ε` |
|---|---|---|---|---|---|
| adjacent windows 1, 2 | 0.584 | 0.1 | `[−0.117, +0.117]` | 0.122 | 0.2 |
| | | 0.5 | `[−0.585, +0.578]` | 0.695 | 1.0 |
| | | 1.0 | `[−1.166, +1.138]` | 1.554 | 2.0 |
| windows 1, 3 | 0.915 | 0.5 | `[−0.916, +0.912]` | 0.945 | 1.0 |
| target and top window | 0.999 | 0.5 | `[−0.999, +0.999]` | 0.9995 | 1.0 |

**[S]** the corollary, with the error at its worst case: 0 misses in 500 repetitions at level 0.05 (2 000
draws per state, `ε = 0.5`); median width 1.97 against 2.45 for "bridge interval `± 2ε`" (bridge width 0.45,
certified `T̄ = 0.66` for a true 0.58).

*What it means and what it does not.*  The package's item E3 adds `ε_i + ε_j`, which is right when the two
errors are unrelated and is attained when the states do not overlap.  When the error is common — windows
of one potential with different biases, where the bias is known exactly and the error sits in the
potential — only the part of the error that the two states weigh differently survives.  The gain is the
factor `TV`: about 0.6 for neighbouring windows as usually spaced, nothing for distant states.  Along a
ladder the per-edge bounds add and can exceed the direct bound `2ε`; the smaller of the two is valid.
**For differences between disjoint regions of one state (a potential of mean force between two bins) the
full `2ε` is attained** (take `d = ∓ε` on the two bins): sharing does not help there.

## 6. Proposition M3: which sampling laws need free energies

**Proposition M3.**  Let `g = υ (s_{τ,η})₊ − λ (s_{τ,η})₋`, so `Ψ_k(τ, η) = ∫ q_k g`.
(i) *One state, no normaliser.*  If `q > 0` wherever `q_k g ≠ 0`, then `Ψ_k = Z_q E_q[(q_k/q) g]`: the sign
of `Ψ_k` is that of one expectation under `q`, whatever `Z_q` and `Z_k` are.  Theorem 5.1 is `q = q_k`;
Theorem 5.4 is `q` = the extremal weight.
(ii) *Several states, no normaliser.*  If each of the states `j ∈ J` satisfies (i) with `Y_j = (q_k/q_j) g ≤ B_j`,
the product `Π_j Π_{n ∈ j} (1 − λ_j Y_j(x_n))` with fixed `λ_j ∈ [0, 1/B_j)` is a valid test of `Ψ_k ≥ 0`.  Its
expected logarithm is `Σ_j n_j G_j(λ_j)` with `G_j(λ) = E_{p_j} ln(1 − λ Y_j)`: linear in the allocation.  Hence
at a given total cost it never exceeds what the best single state gives.
(iii) *States that cooperate.*  If no single state covers both signs of `g` usefully — one sees the event,
another the bulk — the mixture form of Theorem M1 combines them, and it needs the free-energy
differences between them.

*Proof.*  (i) `E_q[(q_k/q) g] = Z_q^{-1} ∫ q_k g`.  (ii) Each factor has expectation
`1 − λ_j Ψ_k/Z_j ≤ exp(−λ_j Ψ_k/Z_j) ≤ 1` when `Ψ_k ≥ 0`, the draws are independent, and the factors are
non-negative; Markov.  The expected logarithm is additive over independent draws.  (iii) is Theorem M1.  ∎

*Consequences.*  (a) Validity of a pooled sign test never needs a free energy; usefulness does, as soon
as the states are complementary.  A window that only visits the event contributes factors below one in
(ii) and is best given the bet zero.  (b) The allocation problem for a certificate is not the allocation
problem for an estimate: in (ii) the optimum is a vertex (all draws in one state), whereas the
asymptotic variance of a free-energy contrast is minimised in the interior (item A2 of the package, not
checked by us).  For the mixture form the objective is the growth rate of the test at the composed
envelope, which involves the widths of finite-sample free-energy intervals; we do not know its optimum.
(c) The extremal ensemble of Theorem 5.4 is the one state that sees both signs with the right weights;
its difficulty was the sampler.  As a Boltzmann state with reduced energy `ũ_k − ln υ` on `{s > 0}` and
`ũ_k − ln λ` elsewhere it can be one more state of a multistate simulation; with Theorem M1 its draws and
the reference's can be pooled.  Not tested here.

## 7. The seven sources of uncertainty, and where each enters

| source | where it enters these statements | covered by | not covered |
|---|---|---|---|
| deterministic computational error | evaluation of `q_j`, `f`, `φ` at the draws; the fit of the centre; root finding | the centre and the multipliers may be wrong without loss of validity; allowances for evaluation errors of `f`, `φ` and enclosures of population sums exist for one state (main note §7) | `multistate.py` is floating point without interval arithmetic; exact evaluation of the `q_j` is assumed |
| statistical sampling error | the levels `α_f` and `δ` | Theorem M1(c); intervals of §3 | — |
| nonequilibrium and mixing error | the hypothesis "independent draws of exactly `p_j`" | a law within a known density ratio or total-variation distance of `p_j` (main note §7.3), one state only | correlated trajectories, unconverged chains: the prototype abstains; a version for stationary chains with a known contraction would need an external inequality that we have not checked and a contraction bound that nobody certifies |
| energy-model approximation error | the envelope `(λ, υ)`; Proposition M2 when it is shared | exact when a uniform bound is proved; bounded-influence classes (main note §9) for extensive errors | a bound on selected configurations only |
| physical force-field error | formally the same envelope | conditional statements "if the error is at most `ε`" | **no bound is known**; no statement here is one about nature |
| experimental measurement error | the region `R` of the measured averages, with its own level | boxes, ellipsoids (correlated errors), sums of them | systematic errors of the forward model `φ` beyond a declared `phi_err` |
| ensemble identifiability limitation | the exact interval `[V⁻, V⁺]` itself | reported separately from the statistical excess `τ̂ − V⁺` | it cannot be reduced by sampling: only by more measured averages or a smaller class |

A certified value at `Γ = 1` from multistate draws is a statement about the *model state* `k`.  It is as
narrow as the sample allows and says nothing about the accuracy of the model.

## 8. Evidence for Theorem M1

### 8.1 First run: bridge intervals (as registered)

`experiments/eng/phase2_mbar/multistate_certificate.py`; design, methods and predictions in
`PREDICTIONS.md`, written before the first run; stored output `results/multistate_certificate.json` (all
values of all repetitions) and `.log`.  Two double-well models on 1 000 points with a ladder of six
harmonic windows from one well to the top of the barrier; the event `barrier` has probability
`3.786·10⁻⁵` (model R10) and `9.435·10⁻⁷` (model R14) under the target.  Level 0.05 for every method
(pooled: 0.02 for the free energies, 0.03 for the sign test); half of the draws for the pilot.  Total number
of draws `N`, equal for all methods of a row.  **[S]**, exact reference by enumeration.

* **T** — all draws from the target state; Theorem M1 with one state.
* **P-all**, **P-sel** — Theorem M1 with `N/7` draws per state: all states pooled; or the target and the
  windows that put at least a quarter of their pilot draws where the score is positive (as registered).
* **P-pilot** — *added after a smoke test, not covered by the predictions*: the pilot rehearses the
  certificate for three pools (target only, the registered selection, all) and takes the best.
* **G** — the interval of item G2 of the MBAR division's imported package, fed with the same free-energy
  intervals (indicators only).

Median of certified value / exact value `V⁺` (200 repetitions; 100 at `N = 2·10⁵`):

| event `barrier` | `Γ` | `N` | `V⁺` | T | P-all | P-sel | G | half-width of the free-energy interval used |
|---|---|---|---|---|---|---|---|---|
| R10 | 1 | 4·10⁴ | 3.79·10⁻⁵ | 8.3 | 5.5 | 5.1 | 57 | 1.63 |
| R10 | 1 | 2·10⁵ | 3.79·10⁻⁵ | 3.6 | 2.1 | 2.1 | 14 | 0.71 |
| R10 | 3 | 4·10⁴ | 1.14·10⁻⁴ | 11.6 | 5.5 | 5.1 | 57 | 1.61 |
| R10 | 3 | 2·10⁵ | 1.14·10⁻⁴ | 4.2 | 2.2 | 2.1 | 14 | 0.72 |
| R14 | 1 | 4·10⁴ | 9.44·10⁻⁷ | 333 | 6.4 | 5.9 | 1 599 | 1.75 |
| R14 | 1 | 2·10⁵ | 9.44·10⁻⁷ | 67 | 2.3 | 2.2 | 325 | 0.78 |
| R14 | 3 | 4·10⁴ | 2.83·10⁻⁶ | 333 | 6.3 | 5.9 | 1 594 | 1.75 |
| R14 | 3 | 2·10⁵ | 2.83·10⁻⁶ | 67 | 2.3 | 2.2 | 325 | 0.79 |

(P-pilot chose the registered selection in every repetition of these rows.  The ratio of P-sel is the
exponential of the half-width to within a few per cent — `e^{1.63} = 5.1`, `e^{0.71} = 2.0`, `e^{1.75} = 5.7`,
`e^{0.78} = 2.2`: the sign test itself adds almost nothing, the free-energy intervals are the whole excess.)

Median excess `τ̂ − V⁺` for the common observables on R10 (`right`: indicator of `x > 1/2`, `p_0 = 0.273`;
`position`: `f = x`); "trivial" means the method returned the upper end of the range in every repetition:

| observable | `Γ` | `N` | `V⁺` | T | P-all | P-sel | P-pilot (post hoc) | G |
|---|---|---|---|---|---|---|---|---|
| right | 1 | 4·10³ | 0.273 | 0.034 | trivial | trivial | 0.091 | trivial |
| right | 1 | 4·10⁴ | 0.273 | 0.011 | 0.067 | 0.034 | 0.029 | trivial |
| right | 3 | 4·10³ | 0.530 | 0.041 | trivial | trivial | 0.105 | trivial |
| right | 3 | 4·10⁴ | 0.530 | 0.013 | 0.093 | 0.053 | 0.033 | trivial |
| position | 1 | 4·10³ | 0.387 | 0.017 | trivial | trivial | 0.046 | — |
| position | 1 | 4·10⁴ | 0.387 | 0.0054 | 0.033 | 0.019 | 0.014 | — |
| position | 3 | 4·10³ | 0.513 | 0.021 | trivial | trivial in 139 of 200 | 0.055 | — |
| position | 3 | 4·10⁴ | 0.513 | 0.0066 | 0.045 | 0.027 | 0.017 | — |

(P-pilot chose "target only" in every repetition of the first six rows and in 139 and 181 of 200 in the
last two; its excess is about `√7` times T's, the price of having spent six sevenths of the draws on windows.)

**Outcome of the predictions.**

| | prediction | outcome |
|---|---|---|
| Q1 | no method certifies a value below `V⁺` in more than 5 % of the repetitions of a cell | **holds**: 0 wrong values in 2 800 repetitions for each of T, P-all, P-sel, P-pilot, and 0 in 2 000 for G.  (This shows soundness, not that the level is attained: the procedure is conservative.) |
| Q2 | R14: P-sel at most ×15 and ×4; T at least ×100 and ×25; P-sel better by at least 8 | **holds**: ×5.9 and ×2.2 against ×333 and ×67; better by 56 and by 30 |
| Q3 | R10: P-sel and T within a factor 3 of each other | **holds**: P-sel is better by 1.6 to 2.3 — certifying the ladder costs about as much as counting the event |
| Q4 | common observables: T best in all eight cells; P-sel's excess 1.5 to 5 times T's; P-all's at least 3 times | T is best in all eight (**holds**); P-all's excess is 6 to 7 times T's at `N = 4·10⁴` and it is trivial at `4·10³` (**holds**); **refuted for P-sel at `N = 4·10³`**: it returned the trivial bound in 739 of the 800 runs (every run of three cells, 139 of 200 in the fourth), because the registered rule selected windows near the top of the ladder, whose free-energy intervals are `±5` there; at `N = 4·10⁴` its excess is 3.3 to 4.1 times T's |
| Q5 | G at least 5 times worse than P-sel on R14; on `right` at `N = 4·10⁴` G returns at least `2V⁺` | **holds** on R14 (G is 146 to 272 times worse than P-sel, and about 5 times worse than T); on `right` G returned the trivial bound 1 in all four cells, which is `3.7 V⁺` at `Γ = 1` and `1.9 V⁺` at `Γ = 3` — the prediction as worded could not be met at `Γ = 3`, where `V⁺ > 1/2` |
| Q6 | at most 2 % abstentions | **holds**: none.  But "no abstention" is not "useful": P-all and P-sel returned the trivial bound in 800 and 739 of their 2 800 runs (all of them common observables at `N = 4·10³`) |
| Q7, Q8 | Proposition M2 (§5) | **hold** |

**What is shown.**  (i) Soundness of the composed certificate on these models.  (ii) For rare events
covered by the windows, relative accuracy at a cost set by the free-energy intervals of the ladder, where
target-only sampling is 30 to 56 times worse at equal numbers of draws; for an event of probability
`4·10⁻⁵` the gain shrinks to about two.  (iii) Composition with an energy envelope: the rows `Γ = 3` behave
like the rows `Γ = 1`.  (iv) A Chernoff interval that knows only that the weighted summands lie in `[0, 1]`
(G) is never relatively accurate for a rare event and is worse than counting; the bound on the density
ratio over the event is what makes the difference.

**What is not shown, and what went wrong.**  (i) Pooling does not help a common observable; with a poor
choice of pool it returns nothing.  Our registered selection rule was such a poor choice (also on the
thin-slice event of §4, where it selected no window at all and was ×8 254 the exact value); a pilot
rehearsal repairs it, and that repair was added after seeing the failure.  (ii) Every model is
one-dimensional and enumerable, the draws are exact and independent, the bound `B` comes from enumeration.
(iii) Only upper ends were run.  (iv) No measured averages (`η = 0`) in these runs: the theorem covers
them, the experiment does not.  (v) The intervals of §3 are conservative (union bound over 21 pairs, sums
along the path); the reported factors are what this particular free-energy certificate costs, not a
lower bound for any certificate.

### 8.2 Second run: the same draws with the likelihood-ratio region (post hoc)

Not covered by the predictions.  `multistate_certificate.py --lr` regenerates the draws of §8.1 (same
seeds, same order of random calls; the method P-sel, recomputed in this run through a different code path,
agrees with the first run to `1.9·10⁻⁸` in every repetition) and replaces the free-energy intervals by
those of §3.2, at the same level 0.02.  L-all and L-sel are P-all and P-sel with these intervals, L-pilot is
P-pilot.  Stored output: `results/multistate_certificate_lr.json`, `.log`.  Median of certified value /
exact value:

| event `barrier` | `Γ` | `N` | T | P-sel (§8.1) | L-all | L-sel | half-width of the interval used, §3.2 |
|---|---|---|---|---|---|---|---|
| R10 | 1 | 4·10⁴ | 8.29 | 5.13 | 1.44 | 1.39 | 0.25 |
| R10 | 1 | 2·10⁵ | 3.6 | 2.07 | 1.19 | 1.17 | 0.11 |
| R10 | 3 | 4·10⁴ | 11.6 | 5.07 | 1.43 | 1.39 | 0.24 |
| R10 | 3 | 2·10⁵ | 4.21 | 2.08 | 1.20 | 1.18 | 0.12 |
| R14 | 1 | 4·10⁴ | 333 | 5.93 | 1.57 | 1.51 | 0.31 |
| R14 | 1 | 2·10⁵ | 66.5 | 2.21 | 1.23 | 1.21 | 0.14 |
| R14 | 3 | 4·10⁴ | 333 | 5.85 | 1.55 | 1.50 | 0.31 |
| R14 | 3 | 2·10⁵ | 66.5 | 2.22 | 1.24 | 1.22 | 0.16 |

Median excess `τ̂ − V⁺` for the common observables:

| observable | `Γ` | `N` | T | L-all | L-sel | L-pilot |
|---|---|---|---|---|---|---|
| right | 1 | 4·10³ | 0.034 | 0.25 | 0.19 | 0.091 |
| right | 1 | 4·10⁴ | 0.011 | 0.041 | 0.03 | 0.029 |
| right | 3 | 4·10³ | 0.041 | 0.42 | 0.35 | 0.11 |
| right | 3 | 4·10⁴ | 0.013 | 0.047 | 0.035 | 0.033 |
| position | 1 | 4·10³ | 0.017 | 0.14 | 0.11 | 0.046 |
| position | 1 | 4·10⁴ | 0.0054 | 0.019 | 0.015 | 0.014 |
| position | 3 | 4·10³ | 0.021 | 0.2 | 0.17 | 0.054 |
| position | 3 | 4·10⁴ | 0.0066 | 0.024 | 0.018 | 0.017 |

No value below `V⁺`, no abstention, no trivial bound and no refusal in 2 800 repetitions of each of the
three methods.  L-pilot chose the registered selection in every repetition of the rare-event rows and
"target only" in every repetition of the common rows.

**What this shows.**  The free-energy region is the lever.  Replacing sums along paths by the
likelihood-ratio region takes the rare-event certificate from ×5.1–5.9 to ×1.4–1.5 at 4·10⁴ draws and
from ×2.1–2.2 to ×1.2 at 2·10⁵: for an event of probability `10⁻⁶` the certified bound is within 22 % of
the exact value, 55 to 220 times closer than target-only sampling at equal numbers of draws, and for the
event of probability `4·10⁻⁵`, where §8.1 gained only a factor two, it is 3 to 8 times closer.  With it,
pooling no longer returns trivial bounds for common observables at 4 000 draws; but target-only sampling
remains the best for them in all eight cells (the excess of L-all is 3.6 to 10 times that of T), as it
must when six sevenths of the draws go to windows.

**A defect of ours, found and repaired in this run.**  The first execution of this second run returned
"void" in 22 of 2 800 repetitions of L-all (two cells at 4 000 draws): the certificate refused envelopes
with `L > U`.  The cause was our first implementation of `lr_intervals`.  With few draws the search over
multipliers reached a nearly infeasible inner problem, the Newton iteration ran off to a saturated point
with a numerically singular Hessian, and a negative Newton decrement passed the convergence test; one
"upper bound" came out as `−2.9·10¹³`.  The refusal was a guard doing its work, but intervals wrong in a
less visible way cannot be excluded for that execution at 4 000 draws.  The inner solver now rejects steps
that are not descent directions, points far from its start and gradients that have not converged; the
search rejects any bound below a known point of the region; a regression test replays the failing draw.
The tables above are from the repaired execution; the first is kept as
`results/multistate_certificate_lr_run1_DEFECT.json` and `.log`.  Between the two, the rows at 4·10⁴ draws
are identical and those at 2·10⁵ differ in the second decimal (the repaired search is slightly more
conservative).

## 9. Relation to the MBAR division's package and first results

Read on its branch at `003dad8`, as proposals: `docs/mbar/PROVENANCE.md` and, in
`experiments/mbar/handoff/MBAR_strengthened/`, the files `FABLE_TASK.md`, `README.md`,
`results/EXECUTION_NOTES.md`, `proofs/MAIN_RESULTS.md`; and at `12af33a`: `docs/mbar/PRIOR_ART.md` (§§1–2),
the header and three theorem statements of `experiments/mbar/lean/MBAR/EValue.lean`, the end of its axiom
log and its coverage logs.  Its code was not run and not read; its Lean project was not rebuilt; the nested
archive was not opened.  The package itself says that its proofs are informal and unverified.

| item of the package | what it would give here if it is verified | status on our side |
|---|---|---|
| C2 (bridge intervals with closure) | the intervals `[a_j, b_j]` of Theorem M1 | the two facts it rests on re-derived and tested (§3); our own implementation is used |
| C1 (certificate from the score at any centre), C3 (valid at any stopping time) | other sources of `[a_j, b_j]`; C3 would let the free-energy level hold under optional stopping | not checked, not used |
| B1 (likelihood-ratio region; its own result, published at `12af33a`) | one convex region for all free energies: the intervals of Theorem M1 without a union over pairs and without sums along paths | **used**: re-derived (§3.2), implemented and tested by us, measured in §8.2 — the excess factor of the rare-event certificate falls from 5.9 to 1.5 and from 2.2 to 1.2.  Machine-checked by that division for finite support (statements read, project not rebuilt) |
| G2 (interval for a bounded observable) | the special case `Γ = 1` without measured averages | not checked as a theorem; implemented from its statement as the comparator G; see the observation below |
| E3 (energy error plus statistical error by the triangle inequality) | superseded for observables by Theorem M1 (which is exact in the envelope) and, for a shared error, by Proposition M2 | E3 itself is elementary and correct as far as it goes |
| G1 (stationary chains with a known contraction) | a version of Theorem M1 for correlated draws, in Hoeffding form | not derived, not checked; it would rest on an external inequality and on a contraction bound that nobody certifies |
| A1, A2, E2 (convexity of the asymptotic variance in the allocation) | nothing directly: the objective of a certificate is a growth rate, not that variance (§6) | not checked |
| B3–B5 (finite-sample bounds with population parameters), D1–D2 (lower bounds) | B: not usable in a certificate while the parameters are not observable; D: a floor for the width of `[a_j, b_j]`, hence for the excess of §8 | not checked |

*Three observations of a reader, offered to that division as proposals (ENG-MSG-0011).*
1. G2 bounds the pooled average of `π_k(f⁰, x) A(x)` as an average of summands in `[0, 1]`.  For a rare event
   those summands are at most the largest density ratio on the event, which is far below one; ignoring
   that leaves an absolute error of order `ln(1/α)/(N s_k)`, worse than counting (measured: ×325 to ×1 599
   against ×2.2 to ×5.9).  G2 also widens by the oscillation over *all* states, where only the states
   that carry the sample at `x` matter (Remark 3 to Theorem M1).
2. E3 treats the errors of two states as unrelated.  For windows of one potential they are the same
   function, and Proposition M2 applies.
3. For a certificate the relevant measure of overlap on an event is a supremum of a density ratio (§4),
   not an average; windows designed for a small variance can be useless for a certificate.

## 10. Limits, and what was not done

* **Unrefereed.**  Theorem M1 and Propositions M2 and M3 are paper proofs of one AI session, checked by
  unit tests and by the experiments above, not by a second reader.  The first version of the main note
  contained two false claims that only an independent review found; the same can be true here.
* One defect of our implementation was found only because the certificate refused its output (§8.2).  The
  numerical part of §3.2 needs an independent reader as much as the proofs do.
* One-dimensional enumerable models; exact independent draws; float arithmetic; upper ends only; no
  measured averages in the runs; two free-energy certificates (§3).
* The bound `B` is an analytic input that we obtained by enumeration.  For a physical system it has to be
  derived from the bias functions on the event; if it cannot be, the procedure must abstain.
* Not done: correlated draws; the extremal ensemble as an additional state (§6(c)); allocation for a
  certificate; the lower end of the interval in the runs; a search of the literature for Theorem M1 and
  Proposition M2 (multistate reweighting with bounded weights and sensitivity analysis with density-ratio
  bounds are both established fields; no novelty is claimed).
* No statement here is evidence about a molecule (§7).

## 11. Resources of this cycle

Local machine only: the first run took 22 minutes of wall time on seven processes, the second run 19 and,
repaired, 13 minutes; the other two scripts and the tests a few minutes.  Modal: nothing launched, no Modal command run; the ceiling of $25
for all four divisions is untouched.  No subagent was used.  Claude usage: the only meter available is
the account's usage counter, which the sessions of the other Phase II divisions share; they were running
during this cycle, so the counter's increase no longer bounds this division's spending in a useful way.
At 07:00 UTC that increase since the start of Phase II, all sessions together, stood at about $472 of the
$500 ceiling of directive D-11.  The division therefore stops at the end of this cycle and schedules no
further synchronisation until the research owner has decided how the ceiling is to be read.  The sealed held-out
material was not accessed.
