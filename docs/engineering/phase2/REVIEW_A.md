# REVIEW_A — adversarial review of `CERTIFIED_INFERENCE.md`

*Independent referee (a subagent of the Computational Research Division), 2026-11-28.  Object:
`docs/engineering/phase2/CERTIFIED_INFERENCE.md`.  The note was edited while the review was running:
Propositions 9.5 and 9.6, the new wording of §9.4 and the matching lines of §0, §10 and §12 were added
after the review had begun.  Sections 1–8 did not change.  Everything below refers to the text as it
stood at the end of the review (533 lines).*

*Method.  Every statement was re-derived before its proof was read.  Every statement was then attacked
numerically with code written for this review (`experiments/eng/phase2_review/`, outputs in `out/`),
which does not import the division's library: primal linear programmes over all weights (Charnes–Cooper),
threshold enumeration, exact Hausdorff distances by enumerating the vertices of the hyperplane
arrangement, Monte Carlo with up to 4·10⁵ repetitions.  Only after that was the library read
(`src/metricchain_eng/certinf/`), and tested against the same reference (`check_library*.py`).
Agreement between my code and the note is reported in one line; it is not evidence beyond the cases run.*

*Severity, as defined in the brief.  **Critical**: a false statement (with a counterexample) or an unsound
certificate.  **Major**: a gap in a proof, a missing hypothesis, or a conclusion the body does not
support.  **Minor**: wording, constants, typos.  Within a class the order is by consequence.*

## 1. Verdict per statement

| statement | verdict | finding |
|---|---|---|
| §1 setting | correct | `P(l,u)` is compact and convex for every envelope (also `l ≡ 0`), so `I` is a compact interval; `Γ` needs the convention `0/0 = 1` |
| Proposition 2.1 | correct | — |
| Theorem 2.2 | correct | constants re-derived; (H2) is not used by the statement |
| Proposition 2.3 | correct | the constant 2 is sharp (ratio 0.9995 attained) |
| Corollary 2.4 | correct | also needs (H1), (H5) through 2.3; holds for non-convex `R` (800 pieces, no violation) |
| table H1–H6 | correct with a repair | H6 is not an assumption and is never formulated; `§7.4` should read `§7.5` (m3, m4) |
| Proposition 2.5 | correct | the two sentences around it are not: "finite" fails at a tangency (cost `∝ √κ`), and the total excess can exceed `2κ(1+‖η‖₁)` (m2) |
| Theorem 3.1 | correct | not an improvement for `d ≤ 6` and large `ε` (m1) |
| Remark 3.2 | not checked | literature |
| Theorem 4.1(a) | correct | — |
| Theorem 4.1(b) | correct | the second sentence also holds for `l ≡ 0`, which the note uses but does not prove (M5); the infimum over `η` need not be attained (m9) |
| Theorem 4.1(c) | ill-posed; **false** under the reading in which the hypothesis `Ψ = 0` matters | M4 |
| Theorem 4.1(d) | correct | — |
| Theorem 4.1(e) | **false for `l ≡ 0`**; correct for `Z_l > 0` | C2 |
| Theorem 4.1(f) | correct | a restatement of the condition only |
| Theorem 5.1 | correct | the bound `δ` is attained (failure rates 0.046–0.049 at `δ = 0.05`); `B > 0` must be said (m5) |
| Proposition 5.2 | not proved (first order, as labelled); correct as an upper estimate | "≈" is "≲"; off by factors 3–270 when the bet is capped; `α` is measured from `τ*(η)` (M8) |
| §5.3 | arithmetic correct | compares a sufficient condition with a first-order estimate |
| Theorem 6.1(a), (b) | correct with a stated repair | all arithmetic verified; the access model must exclude evaluation of `l`, `u`, `w₀` (M2) |
| §6 consequence (iii), §0 item 4 | **not supported** as general statements | M1 |
| §7.1 | sound | "ball arithmetic" is not what the code does (M7) |
| §7.2 | sound | not implemented |
| §7.3 | ratio rule sound; total-variation rule correct with a repair | M6 |
| §7.4, §7.5 | sound | the gap-sampling code does not apply 7.4 (C1) |
| Proposition 8.1 | correct | — |
| Theorem 9.1 | correct | the compactness hypothesis is vacuous (m6) |
| Proposition 9.2 | correct | needs `u_i ≥ 0`; full support is not needed |
| Corollary 9.3 | correct | also for sites with more than two states |
| Proposition 9.5 | correct | binary sites, product reference |
| Proposition 9.6 | bound correct; **"equality for coordinatewise monotone `g`" false** for sites with more than two states | C3; "factor 1.4" is not a bound (m8) |
| §9.4 | values correct; last sentence false for the instance it is about | M1; a stronger statement holds (m7) |
| Proposition 9.4 | correct | `Q` must be stochastic on `{s > 0}`; the "limit" paragraph overstates (M1) |
| §0, §11 | several claims not supported | M1, M3, M7 |

## 2. Critical findings

### C1. `certify_upper_gap` certifies while ignoring what was declared (code; unsound under non-default declarations)

*Location.*  `src/metricchain_eng/certinf/certify.py`, `certify_upper_gap`.

*Finding.*  The function takes a `Declared` and uses only `f_lo`, `f_hi`, `phi_lo`, `phi_hi`.  It ignores
`iid`, `beta`, `eps_tv`, `phi_err`, `f_err`, and it never checks the drawn values against the declared
ranges (the reference-sampling path does all of this).  `check_library.py`:

    Declared(iid=False)               -> 'certified', 0.430953     (plain declaration: 0.430953)
    Declared(eps_tv=0.2)              -> 'certified', 0.430953
    Declared(beta=3)                  -> 'certified', 0.430953
    Declared(f_err=0.1, phi_err=0.1)  -> 'certified', 0.430953
    declared f range violated         -> 'trivial', 0.2  (true V+ = 0.3824; the other path returns 'void')

With `f_err = 0.1` the reported bound is a bound for the *evaluated* target, not for the target: it can be
too small by 0.1.  With `iid=False` Theorem 5.1 does not apply and §7.3 says the prototype abstains.  With a
violated range `B` is not a bound and the bets are inadmissible.

*Scope.*  Only non-default declarations; the validation protocol's method M4 uses the default one, so its
runs are not affected.  It is still a certificate that contradicts §7.3–7.4.

*Repair.*  Same guards as `certify_upper`: abstain unless `d.iid`; enlarge the region by `phi_err`, add
`f_err`; return `void` if a drawn `f` or `φ` is outside the declared range; implement or refuse `beta`,
`eps_tv`; abstain when `G ≤ 0` (see K2).

### C2. Theorem 4.1(e) is false for `l ≡ 0`

*Statement.*  "`I = ∅` if and only if there is `η` with `Φ(η) = Σ[l t₊ − u t₋] > 0`."

*Counterexample* (`check_thm41.py`, `counterexample_e`).  `X = {0,1}`, `l ≡ 0`, `u ≡ 1`, `φ = (0,1)`,
`R = [2,3]`.  No ensemble has `E_pφ ∈ R`, so `I = ∅`; but `Φ(η) = −Σ u t₋ ≤ 0` for every `η` whenever
`l ≡ 0`.  With `l ≡ 10⁻³` on the same instance `sup Φ > 0`.

*Where the proof fails.*  "`Y = {M_φ/M_0 : M ∈ K}`" and "`min_{M∈K}(η·M_φ − h_R(η)M_0) > 0`" presuppose
`M_0 > 0` on `K`; for `l ≡ 0`, `0 ∈ K` and the minimum is `0`.  (An unbounded `R` is not a problem: `Y` is
compact, and a compact convex set is strictly separated from a disjoint closed convex set.)

*Consequence.*  The "if" direction, the one that certifies, is true, so nothing unsound follows.  But the
library's `find_inconsistency` and `certify_inconsistent` can never report inconsistency for a model-free
problem (`check_library.py`: `find_inconsistency → 0`, `certify_inconsistent → 'trivial'` on an instance
whose declared range of `φ` alone excludes `R`), while `interval()` does report it through the unbounded
dual.  Theorem 4.1 advertises (f), the model-free limit, in the same breath.

*Repair.*  State (e) for `P = P(l,u)`: `I = ∅` iff some `η` has `min_{p∈P} E_p t > 0`.  For `Z_l > 0` this is
`Φ(η) > 0`; for `l ≡ 0` it is `t > 0` on `supp u`.  For a sample this second form is not testable (an
unsampled configuration can have any `φ`), except deterministically from the declared range of `φ`.

### C3. Proposition 9.6: "equality holds … for coordinatewise monotone `g`" is false for sites with more than two states

*Statement.*  "In the setting of Proposition 9.2 …  Equality holds for additive `g` and for coordinatewise
monotone `g`."  Proposition 9.2 allows arbitrary finite sites.

*Counterexample* (`check_sec9b.py`, `check_library2.py`).  Two sites with three ordered states, site laws
`(0.0401, 0.5001, 0.4598)` and `(0.3815, 0.4694, 0.1491)`, slopes `(1.0038, 1.0722)`,
`g = 1{x₁ + x₂ ≥ 3}` (non-decreasing in each coordinate).  The supremum over the class is `0.632638`
(programme over the whole cone); `SEQ(g) = 0.671526`, and `0.634084` with the two sites in the other order;
the library's `sequential_upper` returns `0.671526`.  In a random search `SEQ` exceeded the exact value in
79 of 300 monotone instances.

*Where the proof fails.*  "For monotone `g` the maximising thresholds are those of `ν_+`": `ν_+` exists only
for binary sites.  With three states the maximising one-site threshold (up-weight the top state, or the top
two) depends on the values of `g(x_{<i}, ·)`, hence on `x_{<i}`; the extremal sequential ensemble is then not
in `𝒞_u`.

*What is true.*  The inequality (sound in every case tried), equality for additive `g` at any number of
states, equality for monotone `g` on binary sites (agreement to 10⁻¹⁴ on 120 instances).  The docstring of
`sequential_upper` ("Exact for additive and for coordinatewise monotone functions") repeats the false part.

*Repair.*  "…and, for binary sites, for coordinatewise monotone `g`."

## 3. Major findings

### M1. The conclusions drawn from Theorem 6.1 ("a property of the class, not of the method"; "intrinsic"; "any sampled certificate over that box needs `e^{un}` draws") do not follow from it, and the last one is false

*Locations.*  §0 item 4; §6 consequence (iii); §9.4 ("by Theorem 6.1 any sampled certificate over that
box needs `e^{un}` draws"); Proposition 9.4, "limit" ("by Theorem 6.1 no sample can certify the remainder");
§11 ("the cost in `Γ` is intrinsic").

*Argument.*  Theorem 6.1 is a minimax statement for one sampling law: over all instances of ratio `Γ`,
procedures that see `n` draws from `π` (or `q`) need `n ≳ Γ/α²`.  It says nothing about a given instance,
and nothing about another sampling law.

(a) *Another sampling law.*  Fix a pilot `(τ₀, η)` and put `ω = U·1{s_{τ₀,η} > 0} + L·1{s_{τ₀,η} ≤ 0}`,
`p₀ ∝ π·ω`.  This is §5 verbatim with reference `p₀` and envelope `(L/ω, U/ω)` (only the unnormalised `ω` is
needed), so Theorem 5.1 applies.  At `τ₀` the tested variable is `ψ/ω = s`, bounded by `S`, and
`E_{p₀} s_{τ₀} = E_πψ_{τ₀}/E_πω ≤ −(τ₀ − τ*(η))`, because `∂_τ E_πψ_τ = −E_πω_τ` and `ω_τ ≥ ω_{τ₀}` for
`τ ≤ τ₀`.  The test costs about `2S² ln(1/δ)/α²` draws: no `Γ`.  `p₀` is the extremal ensemble itself, a
Boltzmann weight with a modified energy; it is exactly what Proposition 9.5 does for monotone scores
("no envelope ratio enters").  Measured (`check_thm61.py`, `tilted_law`), on the hard instance of Theorem
6.1(a), least `n` with median excess ≤ 0.05:

| `Γ` | 10 | 100 | 1 000 | 10 000 |
|---|---|---|---|---|
| draws from `π` | 2 240 | 19 456 | 221 184 | 2 031 616 |
| draws from `p₀` | 896 | 928 | 928 | 896 |

and on an 8-state instance with one observable and rare up-weighted states the first-order cost is
1 680 / 16 371 / 163 066 for `Γ = 10 / 100 / 1000` under `π` against 874 / 918 / 921 under `p₀`, with no
false certification in either.  §8 mentions the tilted proposal in one line and does not draw the
conclusion.  (Limits of this remark: an *exact* sampler of `p₀` built by rejection from `π` costs up to `Γ`
proposals per draw, in agreement with Theorem 6.1; and a pilot far below `τ*` loses the margin.  The point
is only that the cost belongs to the pair (class, sampling law).)

(b) *A given instance.*  §9.4's own instance (uniform cube, `f = x₁`, box of ratio `Γ = e^{un}`) has
`π(f = 1) = ½`, not `1/Γ`.  With reference draws, Theorem 5.1 with `τ_min = 1 − 2/(1+Γ)` certifies
`τ = V⁺ + ½(1 − V⁺)` with probability 0.98 from 200 draws and 1.00 from 400, for `un = 5, 10, 20, 30`
(`Γ` up to 10¹³), and never certifies `V⁺ − ½(1 − V⁺)` (`check_thm61.py`, `instance_94`).  That interval is
useless because it is within `e^{−un}` of the trivial one, not because certifying it is expensive.

*Repair.*  §0 item 4: "With draws from the reference or from the gap distribution, no method avoids a cost
proportional to `Γ` in the worst case over instances (Theorem 6.1); draws from the extremal tilt of the
reference avoid it.  Independently of sampling, the identified sets of a box class with an extensive
residual are nearly vacuous: that is the property of the class."  Delete the sentence of §9.4 and soften
the "limit" of Proposition 9.4 and consequence (iii) to worst-case statements about reference sampling.

### M2. Theorem 6.1: the access model must be stated; on the proof's instances one evaluation reveals the parameter

*Location.*  Theorem 6.1, "knows `f` and `Γ` and samples from the reference"; "(b) … given `b`, `G` and `Z_l`
exactly and samples from the gap distribution — S3's access model".

*Argument.*  The arithmetic is right throughout (`check_thm61.py`: both closed forms of `V⁺` against
threshold enumeration; `gap/(θ/6) ≥ 1.0000`; `χ²/(2θ²/Γ) ≤ 0.67`; in (b) `b = (1, 1/Γ)`, `G = Γ − 1`,
`Z_l = 1`, `q = π_t` for every `t`; `gap/(θ/48) ≥ 1.59`; `χ²/(θ²/Γ) ≤ 0.45`; grids over `Γ ∈ [4, 10⁷]`,
`θ ∈ (0,1]`).  But S3 is *given* the functions `l` and `u`.  In (b), `l(x) = π_t(x)`, so `l` at the state with
`f = 1` equals `t`: one evaluation gives `V⁺(t)` with no draw.  In (a), two evaluations of the unnormalised
reference give `a`.  The theorem is true for procedures whose only information about the instance is the `n`
draws with the values of `f`, `L`, `U` at them, and that has to be a hypothesis.

*Repair.*  Either say so, or replace each atom by a cell of many configurations of equal weight whose
cardinalities carry the parameter (then point evaluations of `l`, `u`, `w₀` are the same in both
instances, and `b`, `G`, `Z_l` are still fixed); the procedure may then evaluate anything at the drawn
points but cannot enumerate or sample uniformly.

### M3. "That removes the dimension from the sample bound altogether" (§0 item 3) is proved for validity only

*Argument.*  Theorem 5.1 bounds the probability of an invalid bound, for a given `η`.  The excess
`τ̂ − V⁺` depends on the `η` fitted on the training half and on `B`, which grows with `‖η‖₁`; no bound on the
excess in terms of `(n, m)` is stated or proved, and Proposition 5.2 assumes the optimal `η`.  Measured
(`check_dimension.py`; 300 states, `Γ = 3`, binding observations, independent implementation, 20
repetitions, no miss in any cell):

| `m` | excess at `n = 10³` | at `n = 10⁴` | at `n = 10⁵` | `‖η*‖₁` |
|---|---|---|---|---|
| 1 | 0.091 | 0.025 | 0.0072 | 0.00 |
| 20 | 0.120 | 0.029 | 0.0093 | 1.05 |
| 60 | 0.255 | 0.035 | 0.0111 | 2.51 |

*Repair.*  "Validity holds at every `m`; the excess depends on `m` through the fitted multipliers."  The
comparison of §5.3 ("free of `d`") needs the same qualification.

### M4. Theorem 4.1(c) is ill-posed, and false under the reading in which its hypothesis matters

*Statement.*  "At a pair `(τ, η)` with `Ψ = 0`, the weights `w = u` on `{s > 0}`, `w = l` on `{s < 0}`
(anything in between on `{s = 0}`) attain it."  If "it" is the maximum that defines `Ψ`, the sentence is
true at every `(τ, η)` and the hypothesis `Ψ = 0` is idle.  The title, the proof ("the case of equality in
(a)") and remark (iii) ("`p*` the extremal ensemble of (c)") say that it means: the ensemble is in the
identified set and has `E_p f = τ`.  Under that reading it is false.

*Counterexamples* (`check_thm41.py`, `counterexample_c`).  `l ≡ 1`, `u ≡ 3` on three states, `f = (0, ½, 1)`,
`φ = 1{x=2}`, `R = [0, ¼]`; `V⁺ = 0.53125`.
(i) `η = 0`, `τ = τ*(0) = 0.7`: `Ψ = 0`, the threshold ensemble has `E_pφ = 0.6 ∉ R`.
(ii) The optimal pair `η = 0.625`, `τ = V⁺`: the scores are `(−0.375, 0.125, 0)`, so state 2 is on `{s = 0}`.
With `w(2) = l(2)`: `E_p f = 0.5 ≠ V⁺`.  With `w(2) = u(2)`: `E_pφ = 0.4286 ∉ R`.  Exactly one value in
between attains `V⁺`.

*Repair.*  "Let `Ψ(τ, η) = 0` and `p = w/Σw ∈ P(l,u)`.  Then `E_pφ ∈ R` and `E_p f = τ` if and only if `w = u`
on `{s > 0}`, `w = l` on `{s < 0}`, and `η·E_pφ = h_R(η)` with `E_pφ ∈ R`.  Such a `p` exists if and only if
`τ = V⁺` and `η` is an optimal multiplier; the weights on `{s = 0}` are fixed by the last condition, not
free."  Generically `{s = 0}` holds `m + 1` configurations at the optimum, so this is the normal case.

### M5. Completeness for `l ≡ 0` is used and not proved

*Location.*  Theorem 4.1(b), "Hence, if `I ≠ ∅` and `Z_l > 0`, `V⁺ = inf{τ : ∃η, Ψ ≤ 0}`"; (f); the protocol's
family F6 and baseline B3 run the dual with `l ≡ 0`.

*Argument.*  The first sentence of (b) is right for every envelope (with `0·R = {0}`; verified at random
`τ`, 300 instances including `l ≡ 0`, to 4·10⁻¹⁵), and Sion's theorem is applied correctly: the function is
real-valued, convex and lower semicontinuous in `η` on the convex set `{h_R < ∞}`, which need not be closed.
The "Hence" uses strict monotonicity in `τ`, which fails for `Z_l = 0`, where `inf_η Ψ(τ, η) = 0` for every
`τ ≥ V⁺` and says nothing about the existence of `η`.  The conclusion is nevertheless true for `l ≡ 0`
(dual = primal to 10⁻⁹ on 180 model-free instances, 13 of them empty).

*Repair (one argument for every envelope, and for (e)).*  `P = P(l,u)` is compact and convex.  `Ψ(τ, η) ≤ 0` iff
`E_p s_{τ,η} ≤ 0` for all `p ∈ P` iff `τ ≥ T(η) := h_R(η) + max_{p∈P} E_p[f − η·φ]`.  By Sion on `P × {h_R < ∞}`,
`inf_η T(η) = max_{p∈P} inf_η [E_p f − η·E_pφ + h_R(η)] = max{E_p f : p ∈ P, E_pφ ∈ R} = V⁺` (`−∞` if empty).
No hypothesis on `Z_l`, no monotonicity.

### M6. §7.3, total variation: the rule as written breaks the argument of Theorem 5.1

*Statement.*  "add `ε_TV·(sup ψ − inf ψ)` to the tested expectation".

*Argument.*  The inequality `E_πψ ≤ E_{π'}ψ + ε_TV(sup ψ − inf ψ)` is right.  But `ψ` depends on `τ`, and
Theorem 5.1 needs every factor to be non-decreasing in `τ`.  With the shift evaluated at each `τ` the tested
function is not monotone (`check_sec7.py`: increases of 0.0036 per step of 0.005 in `τ`, e.g. with
`L = (0, 0.805)`), and `inf_x ψ_τ → −∞` as `τ → ∞`, so the shift is unbounded.

*Repair.*  One constant shift, a bound of `ε_TV·(sup ψ_τ − inf ψ_τ)` over a bounded bracket
`[τ_min, τ_max]` fixed in advance, with `τ̂` restricted to the bracket.  This is what `certify_upper` does
(constant in `τ`, bracket `[f_lo, f_hi]`), so the code is sound here and the note is not.  (An alternative
when `n·ε_TV < δ`: run the uncorrected test at level `δ − n·ε_TV`; `‖π'ⁿ − πⁿ‖_TV ≤ n·ε_TV`.)

### M7. Claims about evidence and about the prototype that nothing supports

* §5.3 "Measured: `RESULTS.md`" and §11 "Demonstrated (… numerics in `RESULTS.md`): … a sound interval is
  obtained with far fewer draws by Theorem 5.1; the cost in `Γ` is intrinsic".  `RESULTS.md` does not exist.
  The only support in the body for "far fewer draws" is the first-order Proposition 5.2 (M8), and
  "intrinsic" is M1.
* §7.1 "the prototype evaluates certificate sums in ball arithmetic and decides on the upper end".  The
  library has interval arithmetic in one place, the wealth of the validation sample, and only with
  `rigorous=True` (default `False`).  Every population sum (`core.py`: `psi`, `tau_root`, `interval`, lumped
  problems, `additive_interval`, `sequential_upper`) is plain floating point; the module docstring calls
  them "candidates".  The "exact" intervals of the protocol (M0, F4, F5) are therefore floating-point
  values.
* §7.2 (enclosures of `b`, `G`) is a rule on paper; no code implements it.
* The header says tests are in `tests/eng/test_certinf.py`; they pass (20 tests).  The test of Theorem 5.1
  accepts up to 20 misses in 120 at `δ = 0.1`.

### M8. Proposition 5.2 is an upper estimate, not an approximation

*Argument.*  Both ingredients hold under the stated normalisation `L ≡ 1`, `U ≡ Γ`: `E ψ² ≤ (Γ+1)S·E s₋ ≤
(Γ+1)S²` whenever `E ψ ≤ 0`, and `|μ| ≥ α` because `∂_τ E ψ ≤ −E_πL = −1` — with `α` the excess over the root
`τ*(η)` of the `η` in use, which is `V⁺` only for the optimal `η`.  They are bounds, so the display is
`n ≲ …`.  And the cap is not a correction: in `check_thm51.py` (part F) the uncapped formula is accurate
when the bet is free (simulated/predicted 1.04, 1.13) and too optimistic by factors 2.8, 22, 254, 267 when
`λ* > 1/B`, where the cost is `≈ B ln(1/δ)/|μ|`.  The library's mixture of 16 bets adds `ln 16` to
`ln(1/δ)`.

### K1–K4. Further mismatches between code and mathematics (major)

**K1. Non-finite numbers are reported as `'certified'`.**  `_smallest_tau` tests `log_wealth(hi) < target`;
a NaN fails every comparison, so the bisection runs and returns `hi`.  `check_library2.py`: one NaN in a
validation `f`, `φ` or `U` gives `status='certified', value=1.0` (the declared `f_hi`).
`Declared.violated_by` does not catch NaN.  The value is the trivial end, so no wrong bound, but the status
is wrong.  Repair: `if not (log_wealth(...) >= target): return None`, and reject non-finite samples.

**K2. `G = 0` is not handled.**  The directive asks for it explicitly; §7.5 treats it on paper.
`certify_upper_gap(b, 0.0, …)` divides by zero, emits two NumPy warnings and returns
`status='certified', value=f_hi` through K1; `s3_interval(b, 0.0, …)` with no draws raises `ValueError`.
Repair: abstain with a message.

**K3. The inconsistency certificate is blind in the model-free case** (C2), and `find_inconsistency` returns
`−∞` for `m = 0`.  `interval()` does detect emptiness there.

**K4. Model-free problems on an ellipsoid are not solved.**  For `l ≡ 0` and a region that is not a box,
`interval()` takes the descent route, whose gradient `tau_grad` is NaN (already recorded by the division in
`experiments/eng/certinf/bugs/tau_grad_nan_modelfree.py`).  Measured here (`check_library2.py`): on 15
instances with a disc the library's ends are worse than an independent dual minimisation by up to 0.254 on
a range of 2 — sound (never inside an inner primal bracket), but not the identified interval.  Any
baseline computed this way (the protocol's B3 on the family with an ellipsoid; also any model-free problem
with more than 20 000 points, which takes the same route) is wider than the truth, which biases H-F(iii) in
favour of the hypothesis.

What was found sound: `tau_root` (2 000 random problems against an independent exact root, incl. `l ≡ 0`,
`l = u`, ties, zero weights: 4·10⁻¹⁵); `interval()` on box regions (400 instances against the primal
programme: no unsound end, no wrong emptiness verdict, 3·10⁻¹⁵); the descent route on ellipsoids for
`l > 0` (within 10⁻⁷ of an independent multi-start minimum); `certify_upper` — the bound `big` is a valid `B` at
`τ_min = f_lo`, the bets `0.9·2^{−k}/B` are admissible and fixed in advance, the bisection returns the end at
which the wealth was verified, the total-variation shift is constant in `τ` and bounds the range over
`[f_lo, f_hi]`, `beta` is applied to `L`, `U` and `U_max`, the lower end is the negated problem with the
range negated and `f_err` on the right side; `certify_inconsistent` (false alarms 0.07 % at `δ = 5 %` on a
consistent region tangent to the reachable set); `s3_interval` (40/40 covered with either allowance;
`'inconsistent'` on a displaced region; abstains for `Z_l = 0`); `additive_interval` (6·10⁻¹³);
`rigorous=True` runs for boxes, ellipsoids and sums.  Simulated miss rates of `certify_upper` and
`certified_interval`: §6 below.

## 4. Minor findings

**m1. Theorem 3.1 is not uniformly better than S3's bound.**  At `δ = 0.05` it needs *more* draws for
`d = 2` unless `ε < 0.21`, `d = 3` unless `ε < 0.35`, `d = 4` unless `ε < 0.53`, `d = 6` unless `ε < 0.99`
(`check_sec2_sec3.py`).  §0 item 2 should say "for large `d` or small `ε`"; an implementation should take
the smaller of the two.  Both are loose by a factor of 4 to 7 against the simulated 95 % quantile.

**m2. The two sentences around Proposition 2.5.**  (i) "the total excess width of S3's interval over `I` is
up to `2κ(1 + ‖η⁺‖₁ ∨ ‖η⁻‖₁)`" is not an upper bound: the sampled body is itself displaced, so in the
coordinates of `K` the region is enlarged by up to `2κ` and the target by up to `2κ`.  A random search found
1.23 times the claimed value with both multipliers zero (`N = 5`, `L = 23`, `κ = 0.0341`, excess `0.0840`
against `0.0682`).  The bound that holds is `2κ(2 + ‖η⁺‖₁ + ‖η⁻‖₁)` (largest ratio found 0.62).
(ii) "costs at most `κ·inf‖η‖₁` over dual certificates, which is finite": when the region is tangent to the
reachable set no dual certificate exists at `τ = V⁺` and the cost is of order `√κ`
(`check_thm41.py`: 0.134·√κ for `κ = 10⁻³ … 10⁻⁵`).  (iii) "not `O(κ)` in general (next proposition)":
Proposition 2.5 is an upper bound and cannot show this; an instance does (`φ = ε'·f`: the enlargement costs
`κ/ε'`, 100κ for `ε' = 0.01`).

**m3.** "six assumptions": five (H1–H5).  H6 is "a regularity condition", never formulated, and concerns
the width.

**m4.** Table, row H4: "§7.4" should be "§7.5".

**m5. Theorem 5.1.**  `B > 0` is needed for `1/B` (if `sup ψ ≤ 0` at `τ_min` the claim is trivial).  The
case distinction "`τ° ≥ V⁺` or `τ° = τ_min`" is unnecessary: the set `{τ ≥ τ_min : E_πψ ≤ 0}` is closed, so
`E_πψ_{τ°} ≤ 0` and `τ° ≥ V⁺` always.  Worth stating: the bound is attained (`check_thm51.py`, part A:
failure rates 0.0459, 0.0487, 0.0493 at `δ = 0.05`, with `τ_min` just below `V⁺` and one bet near `1/B`), so
no data-dependent choice of `η`, `τ_min`, the bets or `B` can be tolerated; with `B` taken from the
certification sample the failure rate is 0.37–0.98 (part D1).  Monotonicity in `τ` verified on 300
configurations × 4 001 thresholds.

**m6. Theorem 9.1.**  "if the class is compact after normalisation (e.g. `E` strongly connected)":
`{r ≥ 0 : Σπr = 1}` is compact because `π > 0`, whatever `E` is; the duality holds on edge sets that are not
strongly connected (200 instances, 10⁻¹⁵).  The hypothesis matters only for the star with its extra node of
zero reference weight.  Farkas is used correctly (polyhedral cone, no closure needed); `r ≥ 0` is what turns
the equality into "≤".  Both alternatives agreed on 600 random graphs, including cycles with `∏C < 1`.

**m7. §9.4.**  The present wording of the statement about boxes is right (its last sentence, about Theorem
6.1, is M1).  More is true: *every* box class containing the
bounded-influence class has `V⁺(x₁) ≥ e^{un}/(1+e^{un})`.  Proof: a box with `α = ln(l/π)`, `β = ln(u/π)` contains
the class iff `β(x) − α(y) ≥ u·d(x,y)` for all `x, y`; then with `A = {x₁ = 1}` and `m(y) ∝ e^{α(y)}` on `A^c`,
`u(A)/l(A^c) ≥ Σ_{x∈A} max_y m(y)e^{u·d(x,y)} ≥ e^{un}Σ_{x∈A} m(x̄) = e^{un}`.  Checked by a linear programme
for `n ≤ 5` (`check_sec9.py`).

**m8. Proposition 9.6, "within a factor 1.4 of exact where it could be compared" (§0 item 5).**  A property
of the cases tried: 1.44 for parity on 8 sites, 1.43 for `1{S ≡ 0 mod 3}`, 1.84 for a random function of
`S` on 6 sites, 3.97 for a random target on at most 5 sites (`check_sec9b.py`).

**m9. Non-attainment.**  For a disc tangent to an edge of the reachable set (`Z_l > 0`), `inf_η τ*(η) = V⁺`
is not attained: the gap is `0.0044/k` along `η = (a, −k)` (`check_thm41.py`).  Theorem 4.1(b) is stated as
an infimum and is right; remark (iii) and Proposition 2.5 presuppose a minimiser; and for data near the
boundary of the reachable set `‖η‖`, `S` and `B` blow up, so the sampled certificate degrades.

**m10. §8.**  "a two-stage scheme (pilot, then tilted proposal with known density ratio) is sound by §7.3":
it is sound by §5 itself, with reference `π'` and envelope `(L/ω, U/ω)`, and needs only the unnormalised
ratio.  §7.3 with `β = sup ω/inf ω` would multiply the envelope ratio by `β²`.

**m11.** Propositions 9.2, 9.6 and Corollary 9.3 need `u_i ≥ 0` (otherwise the class is `{0}`).
Proposition 9.4 needs `Q(x, ·)` to be a probability for every `x` with `s(x) > 0`.

**m12. Code, efficiency only.**  The note's procedure chooses the bets "around the empirically log-optimal
one"; the code uses a fixed grid of 16.  `τ_min = f_lo` makes `B = U_max × (whole range)`; a `τ_min` taken
from the training half would reduce the cap term (in the instance of §9.4, from `Γ` to 2).
`solve_upper` does not lump repeated sample points: `s3_interval` took 45 s for 20 000 draws from 8 states,
against 0.02 s for one end after `lump()` (`check_library2.py`; the validation script lumps by itself).

## 5. What was verified and found correct, in one line each

Proposition 2.1 (support function against a programme over the weights, 2·10⁻¹⁵).  Theorem 2.2 and 3.1
(400 to 1 500 samples per cell, `d = 2, 3, 4`: no deviation above either bound; largest ratio to the bound of
Theorem 3.1: 0.36).  Proposition 2.3 (random extreme pairs: ≤ 0.57κ).  Corollary 2.4 (non-convex region).
Proposition 2.5 (the inequality, 200 instances).  Theorem 4.1(a), (b), (d) (primal programme = direct
minimisation of the root = dual programme, 1 080 instances, six kinds of degeneracy, `m = 0, 1, 2`,
≤ 10⁻⁹; soundness at more than 4 000 random certificates).  Theorem 5.1 (never above `δ`).  Theorem 6.1 (all
arithmetic).  §7.1–7.4 as inequalities (300 to 3 000 instances each); without the correction of §7.3 a
sampler off by a factor 2 gives failure rates 0.86–1.00.  Proposition 8.1.  Theorem 9.1.  Proposition 9.2
(and its failure for a correlated reference: 0.887 against 0.550).  Corollary 9.3 (77 instances with a
region, 2- and 3-state sites, ≤ 3·10⁻¹⁰).  Proposition 9.5.  Proposition 9.6 (the inequality).  §9.4
(values).  Proposition 9.4 (400 instances).  The archive passages cited in remark (i) to Theorem 4.1 and in §9
(item 89(d); Theorems 11.12 and 11.105; Proposition 11.113; E17.2; "special to single states") were located
in the archive; their content was not reviewed.

## 6. Simulated miss rates of the library (`check_library.py`)

No miss rate above `δ` was found in any configuration with a correct declaration.

| function | configuration | `δ` | miss rate | remark |
|---|---|---|---|---|
| `certify_upper` | two states, `Γ = 10`, `π(1) = 0.05`, `n = 60` / `600` (20 000 / 10 000 runs) | 0.05 | 0.0000 / 0.0003 | nothing certified at `n = 60` |
| `certify_upper` | `Γ = 1000`, `π(1) = 0.002`, `n = 1 500` / `15 000` (5 000 / 1 000 runs) | 0.05 | 0.0000 / 0.0000 | nothing certified at `n = 1 500` |
| `certify_upper` | `Γ = 100`, `π(1) = 0.0005`, declared range `[0.9, 1]`, `n = 12 800` (1 000 runs) | 0.05 | 0.0000 | |
| `certify_upper` | sampler at total-variation distance 0.02, declared `eps_tv = 0.02` (1 000 runs) | 0.05 | 0.0000 | 0.8430 when `eps_tv = 0` is declared |
| `certify_upper` | sampler off by the factor 1.5 on the rare state, declared `beta = 1.5` (1 000 runs) | 0.05 | 0.0000 | 1.0000 when `beta = 1` is declared |
| `certified_interval` | 6 states, `m = 1`, `Γ = 3`, `n = 500 + 500` (1 500 runs) | 0.10 | 0.0000 | median width 0.328, exact 0.214 |
| `certified_interval` | the same with `Γ = 30` | 0.10 | 0.0000 | median width 1.891 of a range of 2, exact 1.102 |
| `certify_upper_gap` | 8 states, `m = 1`, `Γ = 5`, `n = 500 + 500` (1 500 runs) | 0.05 | 0.0000 | median bound 0.427, exact 0.382 |
| `certify_inconsistent` | consistent region touching the reachable set, `n = 400 + 400` (1 500 runs) | 0.05 | 0.0007 (false alarms) | fires in 0.5 % at a displacement of 0.02, in 100 % at 0.2 |
| `s3_interval` | 8 states, `m = 1`, `Γ = 2`, `n = 5 000` (40 runs per allowance) | 0.05 | 0 / 40 | median width 0.69 (net), 0.65 (Theorem 3.1), exact 0.28 |

The certificate of the library is far from the limit of Theorem 5.1: with `τ_min = f_lo`, bets at most
`0.9/B` and a mixture of 16, the two-state instances that give failure rates of 0.046–0.049 with an
adversarial `τ_min` and a single bet give 0.0003 or less.

## 7. What I did not check

* §10 and Remark 3.2 (literature; no network), and the novelty judgements of §0 item 6.
* The archive's theorems beyond locating the cited passages; no Lean file was built or read.
* The validation protocol, its runs and baselines; `experiments/eng/phase2_seq/` (the twenty cases behind
  "1.13 to 1.40"); the Hoeffding and Bernstein variants `hoeffding_ucb`, `bernstein_ucb` beyond reading them.
* `metric.py` beyond `sequential_upper` and `additive_interval`; the stress observables;
  `product_joint_law`.
* Anything beyond finite `X` (the note assumes it), dependent draws, large instances, performance.
* The correctness of `mpmath`'s interval arithmetic; the `rigorous=True` path was read and run on three
  regions, not attacked.
* Ellipsoid regions against an exact primal: only against an independent dual minimisation and, for the
  tangent disc, a point region.
* Proposition 5.2 beyond one family of instances.

## 8. Scripts

All in `experiments/eng/phase2_review/`; each prints to standard output, stored in `out/<name>.txt`; fixed
seeds.  Run with the project's virtual environment from that directory, e.g. `python check_thm41.py`.

| script | covers | imports the library |
|---|---|---|
| `ref.py` | reference: primal programme, exact root of `Ψ`, dual minimisation, exact `d_H` | no |
| `check_sec2_sec3.py` | §2, §3 | no |
| `check_thm41.py` | Theorem 4.1, counterexamples C2, M4, tangency | no |
| `check_thm51.py` | Theorem 5.1, Proposition 5.2 | no |
| `check_thm61.py` | Theorem 6.1, the tilted law, the instance of §9.4 | no |
| `check_sec7.py` | §7 | no |
| `check_sec9.py`, `check_sec9b.py` | §8, §9, counterexample C3 | no |
| `check_dimension.py` | M3 | no |
| `check_library.py`, `check_library2.py` | the library against `ref.py` (C1, K1–K4) | yes |
