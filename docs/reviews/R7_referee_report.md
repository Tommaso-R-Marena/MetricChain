# R7 — Referee report on the draft of theory report §11.18 ("Adaptivity replaces the hint")

Objects reviewed: `sec1118.md` (Theorems 11.51–11.54 and the five remarks), `HintRecursion.lean`,
and, as context, `docs/THEORY_REPORT.md` §11.16 and Theorem 11.25, `docs/workstreams/H_REPORT.md`,
`docs/reviews/R5_referee_report.md`.  While I was working the coordinator sent one correction to
Theorem 11.52 (no closure while `r = n_o`; `F2` restricted to `r ≤ n_o − 1`; `r†` capped at `n_o − 1`).
I had found the same gap independently before the notice arrived (§2, C1; `demo_q1.py`,
`out/demo_q1.txt`); from that point on "the algorithm" below is the corrected one, and every
re-derivation and test was repeated for it.

Everything here is my own work in `scratchpad/referee7/` (scripts at the top level, logs in `out/`,
Lean scratch copies in `lean/`).  Nothing under `/home/user/MetricChain` was modified, no state-changing
git command was run, `lake build` was not run, the authors' scripts were not run and their harness was
not read.  I did not delegate.

## 0. Summary

**Verdict on Theorem 11.54 as stated: proved with gaps.**  I believe the statement is true, I could
not break it, and the chain 11.25(a) + 11.44/11.46 + 11.52 + 11.53 ⇒ 11.54 is sound once the following
is written into the section: (i) the closure rule of Theorem 11.52 as corrected by the coordinator
(as drafted the algorithm returns a false bracket with probability one for part of the parameter
range — C1); (ii) an abort rule, so that the cost bound holds always and not only on the good event
(M1); (iii) the induction over levels, which the draft compresses into one parenthesis and which
needs a left limit in the accuracy and a ladder defined relative to the inner dimension (M2).  I
closed (ii) and (iii) on paper (§3.9, §5).  The machine-checked part is what it says it is — the
analysis of the recursion for an abstract pair of functions; that the cube functions satisfy its
hypotheses is paper calculus, which I re-derived by hand and checked numerically (M3).

What I did, in one paragraph.  Theorem 11.52: re-derived every line (good event and its probability,
validity, width, termination, `M ≤ 8Je²M†`, the count of points near a level, the cost sum and its
exponent); found the `r = n_o` gap; found no other error in the accounting.  Evaluated the corrected
algorithm *in expectation* with exact binomial arithmetic on 30 radial outer profiles (plus adversarial
search over profiles) at `n = 10³ … 10⁶`: no instance exceeds the explicit finite-`n` bound of the proof,
and `n⁻¹ ln(cost) − τ` shrinks from `+0.029` (`n = 10³`) to `+0.0002` (`n = 10⁶`; ratio to `τ` 1.006).
Simulated the outer loop with an adversarial inner oracle in about 17 000 runs (`n_o ≤ 16` exhaustive
outer cubes, radial and non-radial; `n_o = 150–240` radial to reach the "negligible" branch): with the
corrected rule no invalid bracket, no violation of the width, termination, count or `M`-bounds; with
the rule of the draft 2 940 of 2 940 runs in the bad parameter range return an upper end below `A`.
Theorem 11.53: compiled the Lean file (axioms `propext`, `Classical.choice`, `Quot.sound` only),
verified by hand every field of `HintPair` for the cube and the "≥" half of (b), iterated the
recursion with my own code: `T_k ≥ θ_hint` always, and the excess of `T_64` over `θ_hint` is
`2.7 %, 1.4 %, 0.7 %, 0.4 %, 0.2 %` on grids of `150 … 2400` points with a conservative (step)
interpolation and `≤ 0.06 %` with linear interpolation — a discretisation artefact, as the draft says.
Theorem 11.51: proof re-derived; algorithm run on the full cube for `n ≤ 14` (19 200 runs: 13 283 exact
outputs all correct, 5 917 brackets with one miss, within the allowed rate).

## 1. Verdict per statement

| statement | verdict | how checked |
|---|---|---|
| **11.51(a)** non-adaptive exponent `θ_na` on `R_u` | correct | cone and flattened cone are radial; relies on Thm 11.44/11.45 (refereed in R5, not re-refereed) |
| **11.51(b)** lower bound | correct | Thm 11.25(a) uses only the zero function and dips, which are radial; convention `(ε/2, δ)` checked |
| **11.51(b)** upper bound and its proof | correct for `n` large at fixed `δ`; two omissions (m4) | re-derived; `radial_check.py`: full cube `n ≤ 14`, 19 200 runs; bracket checked on 22 752 extremal-cap profiles (`n ≤ 80`), 0 violations; alternating-sum bound attained with equality; `k* − r_ε ∈ {−1,…,5}` for `n = 10³…10⁵` |
| remarks after 11.51 (promise is trusted; 2-periodic profile) | correct | read; the profile `(u/2)(−1)^j` depends on `s` only through a sign |
| definition of bracket procedure / exponent function | adequate after three small repairs (M1, M2, m5) | used it to redo the induction of 11.54 (§5) |
| "two families at hand" (`2ud` with one query; two-sample bracket has exponent function `θ_na`) | correct, also at and above `ε*` and for failure `e^{−cd}` | re-derived from Prop. 11.46 / H Lemma 2.4; there the tail lemma is legitimate at `r = d` because the threshold is a sampled value |
| **11.52** (F1), (F3) | correct | one-line proofs redone |
| **11.52** (F2) as drafted | **false at `r = n_o`** (C1); correct in the coordinator's corrected form | counterexample `W ≡` const; Lemma 11.43(b) needs `D ≠ X` |
| **11.52** good event, Chernoff constants, union bounds | correct (`K` is larger than needed); needs a deterministic set of potential inner calls (m9) | (V2) fails with prob. `≤ e^{−K/4}`, (V3) `≤ e^{−K/12}`; thresholds depend on the reference point only; `M ≤ 4K·2^{n_o}` holds deterministically |
| **11.52** validity of both ends | lower end correct; upper end **wrong as drafted** when the test closes with `q = 1`, correct with the correction | re-derived; simulation (§4.2) |
| **11.52** width `≤ gn + ln(4eJ+3)` | correct | re-derived; 0 violations in ≈ 17 000 simulated runs (closest: 0.013 below the bound) |
| **11.52** termination within `J` levels | correct | re-derived (level `≤ ⌈2un + b + n_o ln 2⌉ + 1`); 0 violations |
| **11.52** `M ≤ 8Je²M†`, `M† = e^{nφθ_na((g−β)/φ)+o(n)}` | correct (with `r†` capped) | re-derived incl. level 0, `q = 1`, `r = 0`, `2^{n_o}q < 1`, levels above `max W`; exact evaluation `n ≤ 10⁶`: `max ln(M/(8Je²M†)) ≤ −11.9` |
| **11.52** count of points near a level ("the two factors `e^b` cancel") | correct | re-derived with attention to which `ℓ` enters; exact: `max ln[2M_j^neg p(s_je^{−x})/(16KJe²e^x)] ≤ −1.4` over all instances, i.e. the bound is nearly attained and never exceeded |
| **11.52** cost sum, exponent `τ + 2η₀`, "pointwise exponent function suffices" | exponent correct; the statement "for every member of `L_u`, at most …" holds only on the good event unless an abort rule is added (M1); pointwise definition suffices if the ladder is fixed relative to `n_i` (M2) | re-derived; exact in-expectation evaluation (§4.1) |
| **11.52** "so … so is (up to an arbitrarily small loss) `R[T]`" | correct in the form `T′(ξ) ≤ R[T](ξ⁻) + η` | §5 |
| "What the algorithm does" | accurate | — |
| **11.53(a)** identity; (11.18.1); `θ_na(h) = h` | correct | by hand (§3.10); `klBin_shift` compiled; numerics to `4·10⁻¹⁶`, `u ∈ {0.1,…,8}` |
| **11.53(b)** `R[θ_hint] ≤ θ_hint` | correct | `step_from_hint_le` compiled + `HintPair` for the cube by hand |
| **11.53(b)** `R[θ_hint] ≥ θ_hint` **[P]** | correct, including `ρ_i = ½` and `(g−β)/φ ≥ ε*` | by hand; 120 000 random `(φ, β, g)`: min of `sup_γ − θ_hint(g)` is `+6·10⁻¹²` |
| **11.53(c)** | correct; prose says "bounded", Lean has `T ≤ a` (the general form also compiles) | Lean compiled; variant `lean/HintRecursionVariant.lean` |
| **11.53(d)** | correct for the cube, given `HintPair` (paper) and the trivial instantiation (paper) | Lean compiled; own iteration of the recursion |
| "holds for `gaussPair`" | correct | Lean compiled |
| **11.54** lower bound | correct | same accuracy convention on both sides; `ln(lower)/n → θ_hint` numerically (`0.02361` vs `0.02356` at `n = 10⁵`, `u = 1`, `ε₁ = 0.1ε*`) |
| **11.54** upper bound | **proved with gaps** (C1 corrected; M1, M2, M3) | §5 |
| remark (1) | exponent statement accurate; the sentence about the `n = 32` simulation overstates (m2); `T₂(0+) ≈ 0.51a` etc. are slightly high (m2) | H_REPORT §3; own recursion |
| remark (2) | accurate | — |
| remark (3) | not checked (a claim about other spaces) | — |
| remark (4) | **contradicts Theorem 11.54** at the exponential scale (m1) | logic |
| remark (5) | incomplete on prior art (M4) | §6 |

## 2. Errors and gaps

### CRITICAL (as drafted; repaired by the coordinator's correction)

**C1. The closure test applies the tail lemma to the whole outer cube.**
Place: (F2) ("if `p(s) ≤ |B(n_o, r)|/2^{n_o}` then `E(W − s)₊ ≤ s·2^{−n_o}E_r(n_o)`"), the closure test
("`r` the least radius with `|B(n_o, r)| ≥ 2^{n_o}q`"), and "Validity".  The first two passes of every
level have `M ≤ 2K`, hence `q = 1` and `r = n_o` whatever `N` is.  Lemma 11.43(b) needs a point outside
`{W > s}`; for `r = n_o` and `{W > s_j} = Q_o` (F2) is false (`W ≡ c·s`, `c` large).
Counterexample to the algorithm as drafted: `ψ ≡ 0`.  Then `s₀ = e^{−un}`, `W ≡ s₀e^{un}`; at level 0,
`M = K`: all points are high, `q = 1`, `ℓ = s₀`, `tail = s₀(e^{u(n_o+1) − Λ₁n_o} − 1)`.  If
`(u − Λ₁)n_o + u ≤ ln(1 + e^{gn})` — i.e. for every `φ < g/(u − Λ₁)` and `n` large — the test passes and the
algorithm returns `[s₀, s₀e^{(u−Λ₁)n_o+u}]`, whose upper end is below `A = s₀e^{un}` by the factor
`e^{un_i + Λ₁n_o − u}`: a false bracket with probability one, on every instance (the first test of level 0
does not depend on the instance).  `demo_q1.py`: `u = 1`, `n = 64`, `n_o = 6`, `g = 0.1`: returned
`ln(up/s₀) = 4.72`, truth `64.0`.  Since a closure with `r = n_o` requires `e^{(u−Λ₁)n_o+u} − 1 ≤ e^{G}ℓ/s_j ≤ e^{G}`,
the defect is confined to `φ(u − Λ₁) ≲ g`; outside that range the drafted algorithm is unaffected.
The same gap is in H_REPORT §2.6.  The workstream's simulation could not see it: the simulated
variant "tests closure only when a level is left as negligible".
Status: the coordinator's correction (no closure while `r = n_o`; (F2) for `r ≤ n_o − 1`; `r†` capped at
`n_o − 1`) is right and sufficient.  I re-derived the proof with it: `|{W > s_j}| ≤ 2^{n_o}q ≤ |B(n_o, r)| < 2^{n_o}`
gives `D ≠ Q_o`; a level that is left has `r = n_o` or `Γ̃(r) > e^{G−b}/4`, in both cases `r > r†`, so
`q_j > 2K/M†` with `M† > 2K`; termination is unchanged (`tail = 0` once `M > 2K·2^{n_o}`); `M†` changes by
a factor `≤ 2`.  My own variant, "no closure while `q = 1`", is also valid (`q < 1` already gives
`D ≠ Q_o`) and behaved identically in the tests.
Remark on the coordinator's note that "the three parameter choices used in the convergence proof are
not affected, because there `φ(u − Λ₁) > g`": true for choices (i) and (iii); choice (ii) is used in
the Lean proof (`lemS`, `hkey`, via `StepLE.of_macro` with `β = g/2`) for a fixed `φ` and **every** `g > 0`,
including `g ≥ φ(u − Λ₁)`.  This is harmless after the correction (Theorem 11.52 then holds for all
`φ`), and it could also be avoided by monotonicity of `T`; but the sentence is not accurate as it stands.

### MAJOR

**M1. The cost bound is proved on the good event only; the definition and the induction need it always.**
Place: definition ("makes at most `C` queries to any `ψ ∈ L_u`"), Theorem 11.52 ("whose cost is, for every
member of `L_u`, at most …"), Theorem 11.54 ("least number of evaluations … in the worst case").  The
proof bounds the number of queries on (V1)–(V3).  Off the good event `M ≤ 4K·2^{n_o}` still holds, but
with invalid inner brackets the number of levels is not bounded by anything (a point with a wrong,
huge `L` stays "high"), and already `4K·2^{n_o}` points at accuracy `b` cost `e^{n(φ ln 2 + (1−φ)T(β/(1−φ)))}`,
which with a fixed `δ` destroys both the worst-case and the expected cost.  The draft dropped the
abort rule that H_REPORT has (there for the number of brackets only).
Fix (one sentence): the procedure stops and returns the trivial bracket `[s₀, s₀e^{2un}]` as soon as
its number of queries exceeds the explicit bound of the cost proof, or level `J + 1` is reached, or a
point is not classified at `x_last`; on the good event none of this happens, so the failure
probability is unchanged and the cost bound holds with certainty.  With it the lower bound (expected
number of queries at one instance) and the upper bound (deterministic) of Theorem 11.54 are consistent.

**M2. The induction of Theorem 11.54 is not written; as written it needs three repairs.**
Place: "by Theorem 11.52 and induction, for every `k` and `η > 0` there is a family with exponent function
at most `T_k + η` (finitely many parameter values at each level; `R[T + η] ≤ R[T] + η`)", and in the proof
of 11.52 "the inner accuracy `γn = (γ/(1−φ))n_i`".
(a) Theorem 11.52 produces, for fixed `(φ, β, g, η₀)`, procedures of accuracy `gn + ln(4eJ+3)`; a *family*
(one procedure for every `d, x, δ′`, cost nonincreasing in `x`) has to be assembled, and its exponent
function at `ξ` is bounded by `R[T](g)` for `g < ξ` only: `T′(ξ) ≤ R[T](ξ⁻) + η`.  Nothing shows that `T_k`
is continuous, so the induction hypothesis must be "`≤ T_k(ξ⁻) + η_k`", and the step needs the shift
inequality `R[T̃](g) ≤ R[T](g − ε) + ε + η` for `T̃ ≤ T(·⁻) + η` (§5).  This suffices for 11.54 because
`θ_hint` is continuous and `g < ε₁` is taken anyway.
(b) `n_i = n − ⌊φn⌋` is not `(1−φ)n`, so `γn/n_i` is not a fixed rate; with a pointwise exponent function
and a possibly discontinuous `T` the cost at accuracy `γn` is not controlled by `T(γ/(1−φ))`.  Fix: define
the ladder by fixed rates relative to the inner dimension, `x_l = ξ_l n_i`, `ξ_0 = 2u > … > ξ_last = β/(1−φ)`,
and put `b := x_last` (`= βn + O(1)`); then exactly finitely many rates occur and the exponent comes out
as `τ + η₀`.
(c) the cost must be monotone in `δ′` as well (the outer algorithm calls the inner one at
`δ′ = δ/(2^{n+6}n³)`, which is `e^{−c′n_i(1+o(1))}`, not `e^{−c n_i}`); this is free (a procedure for a smaller
failure probability is one for a larger) but should be in the definition.
None of this changes the result; all of it is routine; I carried it out in §5.

**M3. Machine-checked status of Theorem 11.53 at the level of the header.**
The header carries **[V]**.  Lean proves: the identity `klBin_shift`; for an abstract `HintPair`, the
three consequences of `StepLE`, `superSolution_le_hint`, `step_from_hint_le`, `iterates_lt_hint_add`; and
that the small-slope pair is a `HintPair`.  Not machine-checked: (11.18.1) for the cube (it involves
the inverse of `ρ ↦ KL(ρ‖p_u)` on `[p_u, ½]` and the choice of the root), every other field of `HintPair`
for the cube pair, the fact that `T_{k+1} = min(T_k, R[T_k])` satisfies the hypotheses of
`iterates_lt_hint_add`, and the half "≥" of (b).  The text below the theorem says most of this, and I
verified all of it by hand (§3.10) and numerically, so I regard the statements as correct; but by
the standard applied in R5 (M3 there) the tag should read "**[V]** for an abstract pair; **[P]** (+ numerics)
that the cube pair qualifies".  The file's own witnesses (`gaussPair`, the zero function) rule out
inconsistent hypotheses, which is what vacuity means here; they do not show that the cube is an
instance, and the zero function is a trivial super-solution.

**M4. Remark (5) understates the prior art on adaption.**
"… to help by polynomial factors in some randomised settings (Heinrich 2024; Kunsch–Novak–Wnuk 2024);
the problem here is nonlinear and the gain is exponential" invites the reading that exponential gains
from adaption are new.  They are not: Mathé–Novak 2007 — cited in §11.16 for the non-adaptive lower
bound — state in the abstract that "adaptive methods are much better than nonadaptive ones" and that
"the curse of dimension (for nonadaptive methods) can be broken by adaption", for integration with
respect to an unknown log-concave density with Lipschitz logarithm (the neighbouring problem);
Sikorski 1982 (zero finding) is the textbook example of an exponential gain in a nonlinear problem;
and the abstract of Kunsch–Novak–Wnuk has, besides the factor `n^{1/2}(log n)^{−1/2}`, a `√(log m)` against
`log log m` dependence on the dimension.  What I did not find in print: the exact exponents on a
Hamming–Lipschitz class without concavity, their coincidence with the hinted exponent, and the
recursion.  Fix: cite Mathé–Novak here as the precedent for "adaption breaks an exponential
non-adaptive barrier", and state the difference (no concavity, no Markov chain, exact exponent, a
matching lower bound).  How I read each source is in §6.

### MINOR

* **m1. Remark (4) contradicts the theorem.**  "whether some other instance is harder *with* a hint than
  the zero function is not known in general": at the exponential scale and extensive accuracy Theorem
  11.54 settles it — an algorithm without a hint is one with a hint, so every instance costs at most
  `e^{nθ_hint(ε₁)+o(n)}` with a hint.  (H_REPORT §2.9 says so: "it would follow from H3 + H4".)  What
  stays open is the instance-wise comparison below the exponential scale and at bounded accuracy.
* **m2. Remark (1).**  (a) The simulated algorithm was "a slightly earlier variant" (H_REPORT §3:
  tolerance 1 instead of `e^b`, no factor `J`, closure tested only at negligible levels), not the algorithm
  of Theorem 11.52; (b) of the "32 valid brackets" 20 are `[ℓ, +∞)` from runs stopped by the budget, and
  the comparison with plain Monte Carlo exists for three instances only; (c) the values are a little
  high: my upper bounds (conservative interpolation, `u = 1`) are `T₂(0+) ≤ 0.5006a`, `T₃(0+) ≤ 0.362a`,
  `T₄(0+) ≤ 0.3115a`; `h = 0.2626a`.  (`u = 2`: `T₂(0+) ≤ 0.5064a`; `u = ½`: `0.5001a`.)
* **m3. Bracket width off the good event.**  The definition allows a returned bracket to violate
  `U ≤ e^xL` with probability `δ′`; "classification ends at the latest at accuracy `x_last`" uses the width
  of the last bracket.  Either make the width part of the output format or let the abort rule of M1
  catch it.
* **m4. Theorem 11.51, proof of the upper bound.**  (a) "the two observed values" are not specified;
  with the value at the first sampled point and the common value of its neighbours (H_REPORT) this fails
  when that point lies within distance `r − 2` of the centre or its antipode, probability
  `2|B(n, r−2)|/2ⁿ`; (b) hence the display needs `4|B(n, r_ε − 2)|/2ⁿ ≤ δ`, which holds for fixed `δ`,
  extensive accuracy and `n` large, but not always (`n = 1000`, `u = 1`, `ε₁ = 0.9ε*`: `0.65`); (c) the union
  bound over shells is `(n − 2r + 1)δ/(2n)`, which is `≤ δ/2` for `r ≥ 1`.
* **m5. `x_last`.**  "`x_last ≤ b`" must be "`b − η₀n < x_last ≤ b`" (or `= b`), otherwise the cost display with
  "(or `x_last`)" is not bounded by `T(β/(1−φ))`.
* **m6. Union bound over inner calls.**  "(V1) every inner bracket is valid" is a union over calls that
  are chosen adaptively.  It is legitimate because the set of potential calls is deterministic
  (`M ≤ 4K·2^{n_o}` always: at `M > 2K·2^{n_o}` the level is populated or the tail is zero) and each
  potential call can be given its own pre-drawn randomness; the count `4K·2^{n_o}·(2u/η₀ + 1)·δ′ ≤ δ/2`
  holds for `n ≥ n₀(η₀)`.  One sentence.
* **m7. 11.53(c).**  Prose: "nonincreasing and bounded"; Lean: `T x ≤ a`.  The general statement is true
  (`lean/HintRecursionVariant.lean` compiles with `∃ C, ∀ x > 0, T x ≤ C`).
* **m8. "Status" paragraph** refers to a concluding paragraph on what the referee did and did not
  confirm; the draft has none yet.
* **m9. A side remark for the text.**  At small size the "negligible" branch is never taken: in ≈ 14 000
  runs with `n_o ≤ 24` no level was left as negligible (closure always comes first because `4Je²` exceeds
  `2^{n_o}/|B(n_o, r)|` at the closing radius); it needs roughly `n_o·h ≳ ln(2Je²)`.  Any small-size
  simulation offered as evidence should say which branches it exercised.

I found **no error in the accounting of Theorem 11.52** beyond C1: the counts, the tolerance that
enters each of them, and the exponent `τ` are right.

## 3. Theorem 11.52 line by line (A.1, A.2)

Notation of the draft; `b = βn`, `G = gn`, `s_j = s₀e^j`.

**3.1 Good event.**  (V2): `X ~ Bin(M, p)`, `Mp ≥ 2K`: `P(X < Mp/2) ≤ e^{−Mp/8} ≤ e^{−K/4}`.  (V3): if `Mp′ ≥ K/4`,
`P(X > 2Mp′) ≤ e^{−Mp′/3} ≤ e^{−K/12}`; if `Mp′ < K/4`, domination by mean `K/4` gives `P(X > K/2) ≤ e^{−K/12}`.
With `K = ⌈24 ln X⌉`, `X = 2^{n+6}n³/δ`: `e^{−K/12} ≤ X^{−2}`.  Events: `(J+1)` levels × `(n_o+3)` values of `M` ×
`≤ J+2` values of `x` (for `x > j` the threshold is below `min W` and the statement is trivial) — `O(n³)`,
total `≪ δ`.  The thresholds `s_j`, `s_je^{−x}` are functions of the reference point only and the list
`a₁, a₂, …` is i.i.d. and not influenced by inner results, so these are Chernoff bounds for fixed
thresholds; the prefix `a₁..a_M` is determined by `M`.  (V1): see m6.  The constants are compatible with
`K`, with room.

**3.2 Classification.**  Ends at `x_last ≤ b` for any brackets of the promised width (after intersection
`L ≥ Ue^{−x_last}`).  If both `U ≤ s_j` and `L > s_je^{−b}` hold the label is ambiguous in the draft; either
choice is valid (I tested both).

**3.3 Validity.**  `N ≥ #{i ≤ M : W(a_i) > s_j}`; if `Mp(s_j) ≥ 2K`, (V2) gives `p ≤ 2N/M`; otherwise
`p < 2K/M`; so `p(s_j) ≤ q` at every pass.  If `N ≥ K`: `N ≤ #{W > s_je^{−b}} ≤ max(2Mp(s_je^{−b}), K/2)` and
`N > K/2`, so `p(s_je^{−b}) ≥ N/(2M)` and `ℓ ≤ A` by Markov.  (F3) holds for arbitrary `s₀` (pointwise:
`W ≤ s₀ + Σ_{i<j}(s_{i+1} − s_i)1{W > s_i} + (W − s_j)₊`).  Upper end: (F3) with `p(s_i) ≤ q_i`, and (F2) —
with the correction.

**3.4 Width.**  Populated: `s_{i+1}q_i ≤ e s_i·2N/M = 4e^{b+1}·s_ie^{−b}N/(2M) ≤ 4e^{b+1}ℓ`, also when `q_i = 1`.
Negligible: `q_i = min(1, 2K/M) ≤ 2K/M_i^neg`, so `s_{i+1}q_i ≤ e^bℓ/J`, also when `M_i^neg ≤ K` (then the
level lies so far below `ℓ` that `q = 1` is harmless).  `ℓ` is nondecreasing, so the bounds survive.

**3.5 Termination.**  Let `j₁ = ⌈2un + b⌉`; for `j ≥ j₁` nothing is high.  A level `j ≥ j₁` with
`M_j^neg > 2K·2^{n_o}` cannot be left as negligible before `M = 4K·2^{n_o}`, where `tail = 0`.  Since
`ℓ ≤ A ≤ s₀e^{2un}`, `M_j^neg > 2K·2^{n_o}` as soon as `j > 2un + b + n_o ln 2 − ln(Je)`.  So the closing level is at
most `⌈2un + b + n_o ln 2⌉ + 1 ≤ J`.

**3.6 `M ≤ 8Je²M†`.**  `2^{−n_o}E_r ≤ qΓ̃(r)` (minimality of `r`; for `r = 0` because `2^{n_o}q ≥ 1`).  A level
that is left has `r > r†` (C1), hence `q_j > 2K/M†`.  Negligible predecessor: `M_{j−1}^neg ≤ M_{j−1} < M†`
(if `q_{j−1} = 1` then `M_{j−1} ≤ 2K < M†`).  Populated predecessor: `ℓ ≥ s_{j−1}e^{−b}q_{j−1}/4`, so
`M_j^neg ≤ 8KJe²/q_{j−1} < 4Je²M†`.  Level 0: `M₀^neg ≤ 2KJe^{1−b}`.  `M` is doubled only while `M < M_j^neg`
(with the `ℓ` from before the level; `ℓ` changes within a level only at the pass that ends it).
Asymptotics of `M†`: `Γ̃(ρn_o)` has the exponent `0` below `p_u`, `KL(ρ‖p_u)` on `[p_u, ½]`, `uρ − Λ₁` above;
in the exact evaluation `ln(8Je²M†)/n − φθ_na((g−β)/φ)` is `0.0042, 0.00049, 0.000056` at `n = 10⁴, 10⁵, 10⁶`.

**3.7 The count.**  For `i < j`: `s_ip(s_i) ≤ s_iq_i ≤ 4e^bℓ_j^-`, where `ℓ_j^-` is `ℓ` at the start of level `j`.
For `x ≥ b`, `i` the largest index with `s_i ≤ s_je^{−x}` (if `x ≤ j`; otherwise `p = 1` and the claim follows
from `ℓ ≥ s₀`): `p(s_je^{−x}) ≤ p(s_i) ≤ 4e^bℓ_j^-·e^{x+1}/s_j`.  `M_j ≤ max(K, 2M_j^neg(ℓ_j^-))`.  The product is
free of `ℓ` and of `b`: `2M_j^neg p ≤ 16KJe²e^x`.  With (V3): at most `max(32KJe²e^x, 2K)` points.  This is
the step where the earlier versions went wrong; it is right.  On a cone it is the certified `ℓ`
(negligibility once `s·p(s)` has dropped below the maximum), not a slope, that keeps the count below
`e^x` beyond the peak of `s·p(s)`.

**3.8 Cost.**  A point at gap `G_a ≥ 0` is classified at the first rung `x_l ≤ max(G_a, b)`; a point above
the level at the first rung `x_l < b + |G_a|`.  Points whose last rung at level `j` is `l ≥ 1` have
`W > s_je^{−x_{l−1}}`; their number is at most `min(8Je²M†, 32KJe³e^{x_{l−1}} + 4K)` (one factor `e` for rounding
`x_{l−1}` up into `b + ℕ`); each costs at most `(l+1)·C(n_i, x_l, δ′)` because cost is nonincreasing in the
accuracy.  The exponent of the sum is `max_l [min(μ, x_{l−1}/n) + (1−φ)T(x_l/n_i)] ≤ τ + η₀`.  The bound is
attained (up to `o(n)`) by "outer flat × worst inner", e.g. `ψ(a,b) = u·d(b, s_i)` or the non-product
`u·d(b, ι(a))`, so `τ` is the exponent of this algorithm, not only a bound.

**3.9 What the generalisation from H2 loses (A.2).**  Nothing in the validity argument.  In the cost:
H2 doubles the inner effort with a deterministic width, the draft walks a ladder — the price is the
additive `η₀` and the factor `O(1/η₀)`, both accounted for.  What is needed from the inner family:
(i) a deterministic cost bound per call (definition); (ii) the width on the good event (m3);
(iii) cost nonincreasing in `x` and in `δ′`; (iv) `T` nonincreasing; (v) finitely many rates relative to
`n_i` (M2b).  The abort rule of H2 has to be kept and extended to the cost (M1).  The definition is
adequate for the induction with these additions; accuracy `gn + O(log n)` and failure `e^{−cn}` (`K = O(n)`)
cause no difficulty, and `n ↦ n − ⌊φn⌋` is onto, though only `n_i → ∞` is used.

**3.10 The identity and the cube pair (B.1, B.3).**  `−ρ ln p_u − (1−ρ)ln(1−p_u) = ln(1+e^{−u}) + uρ`, so
`KL(ρ‖p_u) = KL(ρ‖½) + uρ − Λ₁`.  `Λ₁ − up_u = KL(p_u‖½) = a > 0` and `Λ₁ + ε* = u/2`, so
`ρ_h(e) = (Λ₁+e)/u ∈ (p_u, ½]` for `0 ≤ e ≤ ε*`; `KL(·‖p_u)` is increasing and `KL(·‖½)` decreasing on
`[p_u, ½]`, so the minimiser in `θ_na(x)` is the root of `KL(ρ‖p_u) = x` in `[p_u, ½]`; at `ρ_h(e)`,
`KL = θ_hint(e) + e ≤ ε*`: (11.18.1).  `HintPair` with `a`, `h`, `E = ε*`: `θ_na ≤ a` (nonincreasing, limit `a`
at `0+`); continuous on `(0, ∞)` (inverse of a continuous strictly increasing function, value `0` at and
beyond `ε*`); `θ_na(h) = h`; `d/de[e + θ_hint(e)] = 1 + u⁻¹ln(ρ/(1−ρ)) ≥ 0` iff `ρ ≥ p_u`; the same derivative
gives `θ_hint(e) ≥ h − e` (`L = 1`); `θ_hint > 0` on `(0, ε*)`.  The sequence `T_k`: `R[T]` is finite for bounded
`T`, nonnegative, nonincreasing in `g` (a pair `(φ, β)` admissible for `g` is admissible for `g′ > g` and
`θ_na` is nonincreasing); `T₁ = θ_na ≤ a`.  So every hypothesis of `iterates_lt_hint_add` holds.
`StepLE θna T T′` is a faithful statement of `T′ ≤ R[T]`: all `g`, `0 < β < g`, `0 < φ < 1`, every upper
bound `B` of the bracket over all `γ ≥ β`; no hidden restriction (in particular `g` is not confined to
`(0, E)`, which is what makes `StepLE.of_macro` usable).

## 4. Numerical work

All runs: `ulimit -v 4000000`, one or two processes at a time, each under ten minutes except
`check_identities.py` (5.5 min) and the first, discarded, recursion batch.

### 4.1 Exact in-expectation cost of the two-level algorithm (A.3)

`skeleton.py` (model), `skel_runs.py`, `skel_adversarial.py`, `skel_T2.py`.
*Model.*  The run of the outer loop depends on the instance only through the law of `W(a)` and through
the inner oracle; the product structure and the inner shapes enter only through the inner cost, which
I set to the worst case of the family, `exp(n_iT(x/n_i))` with `T = θ_na` (attained by the two-sample
bracket on inner cones).  Hence "outer profile × inner cone" is the binding product family, and the
non-product instance `u·d(b, ι(a))` (constant `W`, moving inner centres) is identical to "outer flat".
For a radial outer profile the law of `W` is binomial and everything is computed in the log domain:
`K`, `J`, the ladder (`η₀n` steps), `p(s)`, for every level the pass at which it is populated, negligible
or closes (corrected rule), `ℓ`, `q_j`, the bracket, and the cost `M_j·E[cumulative ladder cost]` where the
needed accuracy is the worst one a valid oracle can force (`max(G,b)` below the level, `b + |G|` above).
Counts are replaced by expectations, `N = M·P(W > s_je^{−b(1−θ)})`, `θ ∈ {0, ½, 1}` (which of the points in
the tolerance zone the oracle lets be "high").  "sum over levels" is the accounting of the proof;
"max over levels" is attained by an oracle that targets one level, so the true worst case lies between
the two.  For each run I also evaluate the two ingredients of the proof exactly (`M_j/(8Je²M†)` and
`2M_j^neg p(s_je^{−x})/(16KJe²e^x)`) and the explicit bound `B_n` of the cost proof.
*Profiles* (30): flat, cone, cone of slope `u/2`, anti-cone, flattened cones (5 radii), dips and bumps
(5 radii each, around `Λ₁n_o/u`), 2-periodic, a "critical" profile with slope `ln((n_o−d)/(d+1))` clipped
to `±u` (makes `s·p(s)` flat) and half of it, two cliffs, three random walks, three random
piecewise-linear profiles; a second position of `s₀` for flat and cone.
*Parameters:* A–F in `skel_runs.py`: the `T₂`-optimal `(φ, β)` at `g = 0.1, 0.25, 0.5 ε*` (`u = 1`) and
`0.25ε*` (`u = 2`), the hint fraction, and a generic choice.

| set (`u`; `g/ε*`; `φ`; `β`; `η₀`) | `τ` | `n` | largest `ln(cost)/n − τ` (ratio to `τ`) | `ln(B_n)/n − τ` | where |
|---|---|---|---|---|---|
| A (1; 0.10; 0.6327; 0.00127; 0.001) | 0.029556 | 10³ | +0.02903 (1.98) | +0.05556 | dip, `θ = 1` |
| | | 10⁴ | +0.00300 (1.10) | +0.00503 | random walk, `θ = 1` |
| | | 10⁵ | +0.00070 (1.024) | +0.00079 | piecewise slopes, `θ = 1` |
| | | 10⁶ | +0.00019 (1.006) | +0.00038 | bump, `θ = 1` |
| B (1; 0.25; 0.7779; 0.00071; 0.001) | 0.018093 | 10⁴ / 10⁵ | +0.00314 / +0.00085 (1.047) | +0.00472 / +0.00095 | random walk |
| C (1; 0.25; 0.6479; 0.0015; 0.001) | 0.027433 | 10⁴ | +0.00333 | +0.00457 | random walk |
| D (1; 0.10; 0.30; 0.003; 0.001) | 0.054486 | 10⁴ | +0.00363 | +0.00485 | random walk |
| E (2; 0.25; 0.7864; 0.00099; 0.002) | 0.058188 | 10⁴ / 10⁵ | +0.00409 / +0.00178 (1.031) | +0.00540 / +0.00187 | random walk / piecewise |
| F (1; 0.50; 0.9143; 0.00017; 0.0005) | 0.007419 | 10⁴ / 10⁵ | +0.00283 / +0.00059 (1.079) | +0.00508 / +0.00069 | random walk |

In every one of the ≈ 900 runs: the bracket is valid, closes within `J` levels and within the width
bound; `ln(M/(8Je²M†)) ≤ −11.9`; `ln(count ratio) ≤ −1.4`; and **the cost is below `B_n`** (closest:
`ln(cost/B_n) = −8.3` at `n = 10⁵`).  The theorem claims `τ + 2η₀ + o(1)`; from `n = 10⁵` on every value is
below `τ + η₀`.  Adversarial search (`skel_adversarial.py`, hill climbing over 10 slopes, 9 knots and a
2-periodic ripple, `n = 20 000`, 200–250 evaluations each): best `ln(cost)/n − τ = +0.0018` (A), `+0.0020`
(B), `+0.0029` (E), against `+0.0028, +0.0025, +0.0035` for `B_n` — the search gains about 4 % over flat and
cone and stays below the bound.  With `T = T₂` (third level; `skel_T2.py`, `n = 20 000`, `g = 0.1ε*`,
`τ[T₂] = 0.025408`): `+0.0023` (`η₀ = 0.001`), `+0.0015` (`η₀ = 0.0002`).
**No instance exceeds `τ` by more than the finite-`n` prefactor plus `η₀`; largest ratio to `τ` at the
largest size: 1.006.**  At `n = 10³` the polynomial factors (`K ≈ 1.7·10⁴`, `J ≈ 2.4·10³`, squared) are as large
as the exponent — which is why the brief asked for `n ≥ 10³–10⁴`, and why `10⁴` is still too small to
read `τ` off to better than 10 %.
Commands: `python3 skel_runs.py <A..F> <n> [few [levels]]` (`out/skeleton_n1000.txt`, `…10000…`,
`…100000…`, `…1000000…`), `python3 skel_adversarial.py <set> 20000 <evals> <seed>`
(`out/skeleton_adversarial.txt`), `python3 skel_T2.py 20000` (`out/skeleton_T2_eta0.txt`).  For `n ≥ 10⁵` the
cost is evaluated on 150–300 sampled levels plus the first and last 60, and the sum over levels is
bounded by (number of levels) × max.

### 4.2 Logic of the outer loop with a simulated inner oracle (A.4)

`two_level.py` (the loop, from the text of the draft, with the three closure rules), `logic_test.py`,
`demo_q1.py`.  The list `a₁, a₂, …` is sampled exactly (multinomial counts of the classes of outer
points with equal `W`, per dyadic block of indices); `W(a)` and `A` are exact; `K`, `J`, the ladder as in
the draft; `s₀ = e^{−ψ_ref − un}` with a random reference point and a random offset of the inner part.
Oracle strategies: a valid bracket `[We^{−θx}, We^{(1−θ)x}]` with `θ` random per group, or `0`, `½`, `1`; a
greedy adversary that delays classification at the current level as long as a valid bracket allows;
the same targeted at a random level.  Tie rule low/high at random.  Checked in every run: validity of
both ends; width `≤ G + ln(e^{−G} + 4Je^{b+1−G} + e^{b−G} + 1)`; closing level `≤ J`; the count bound for
every level and every `x ∈ b + ℕ`; the deterministic step `2M_j^neg p(s_je^{−x}) ≤ 16KJe²e^x` with the exact `p`;
`M ≤ 8Je²M†`; "classified as soon as the accuracy is `≤ max(G_a, b)`"; and whether (V2)/(V3) held.

| batch | runs | closure rule | invalid | other violations | remarks |
|---|---|---|---|---|---|
| radial, `n_o ∈ {8,…,24}`, 16 parameter sets, 22 profiles × 6 oracles × 5 | 10 470 | corrected (`r < n_o`) | 0 | 0 | max Markov ratio 0.43; max count/bound 0.004; 280 closures with `tail = 0` |
| same | 10 470 | "no closure while `q = 1`" | 0 | 0 | — |
| same | 10 470 | as drafted | 660 | 0 | all 660 in the one set with `(u−Λ₁)n_o + u ≤ G` |
| small outer block (`n_o ∈ {4, 6, 8, 10}`), 4 sets | 2 280 | as drafted | **2 280** | 0 | upper end below `A` in every run, closes at level 0 |
| same | 2 280 | corrected | 0 | 0 | — |
| non-radial exact `W` (`n_o = 12, 16`): min of cones, max of anti-cones, additive, cone + noise, plateau with hidden dips, i.i.d. noise | 2 016 | corrected | 0 | 0 | — |
| `K ∈ {4, 16, 64}` instead of ≈ 1000 | 3 960 | corrected | 0 | 0 | (V2)/(V3) failed in 53 runs, still no invalid bracket |
| radial, `n_o ∈ {150, 200, 240}`, `n = 300–400` | 396 (91 skipped: a block would exceed `2^{61}` points) | corrected | 0 | 0 | 2 577 levels left as **negligible**; max count/bound 0.14; max Markov ratio 0.28 |

(Two further medium-size sets, `u = 4, n_o = 80` and `u = 1, n_o = 600`, are in `out/logic_test_medium2.txt`.)
The observation of m9: with `n_o ≤ 24` no level is ever left as negligible.  Commands:
`python3 logic_test.py radial 5`, `… smallphi 5`, `… stress 5`, `… general 10 0,1,2`, `… general 10 3,4`,
`… medium 1` (`out/logic_test*.txt`); `python3 demo_q1.py` (`out/demo_q1.txt`).

### 4.3 The recursion (B.5)

`recursion.py u Nx Nphi Nbeta kmax mode`.  `T_k` on a geometric grid of `Nx` points in `(10⁻⁷ε*, ε*]`; `θ_na`
from a table (it is convex, so linear interpolation is an upper bound); for every grid point a grid
search over `(φ, β)` (fine in `ln φ` near 0, in `ln(1−φ)` near 1 and around the hint fraction) with three
zoom steps; `sup_γ` exactly for the interpolant.  Mode `step` (`T(y) :=` value at the grid point to the
left) makes every computed `T_k` a rigorous upper bound of the true `T_k`, up to floating point; mode
`linear` is a best estimate.

`u = 1`, entries `T_k/θ_na` (step mode, `Nx = 1200`), last row `θ_hint/θ_na`:

| `g/ε*` | 0+ | 0.016 | 0.062 | 0.25 | 0.49 | 0.81 |
|---|---|---|---|---|---|---|
| `k = 2` | 0.5006 | 0.5124 | 0.5413 | 0.6402 | 0.7538 | 0.9057 |
| `k = 3` | 0.3619 | 0.3990 | 0.4509 | 0.5909 | 0.7356 | 0.9047 |
| `k = 4` | 0.3115 | 0.3630 | 0.4248 | 0.5817 | 0.7339 | 0.9047 |
| `k = 6` | 0.2811 | 0.3433 | 0.4118 | 0.5785 | 0.7337 | 0.9047 |
| `k = 12` | 0.2678 | 0.3343 | 0.4067 | 0.5781 | 0.7337 | 0.9047 |
| `k = 64` | 0.2637 | 0.3323 | 0.4061 | 0.5781 | 0.7337 | 0.9047 |
| `k = 64`, linear | 0.2628 | 0.3313 | 0.4050 | 0.5770 | 0.7331 | 0.9046 |
| `θ_hint/θ_na` | 0.2626 | 0.3313 | 0.4050 | 0.5770 | 0.7331 | 0.9046 |

* `T_k ≥ θ_hint` on the whole grid for every `k`, in both modes (`min(T_k − θ_hint) ≥ +7·10⁻¹³`).
* Largest relative excess of `T_64` over `θ_hint` on `g ≤ 0.9ε*`, step mode: `2.71 %` (`Nx = 150`), `1.39 %`
  (300), `0.72 %` (600; the same with a twice finer parameter grid), `0.39 %` (1200), `0.23 %` (2400): it
  halves with the grid spacing.  Linear mode: `0.06 %` at `g → 0` (finite `k`), `0.00 %` for `g ≥ 0.016ε*`,
  at `Nx = 600` and `1200`.  `u = ½` and `u = 2` (`Nx = 600`): `0.74 %` and `0.65 %` (step), `0.06 %` (linear).
  So the 0–2 % residual of the workstream is discretisation — its interpolation, and, at
  `g ≳ 0.75ε*`, the parameter search: my first search, with a `φ`-grid that was coarse in `1 − φ`, left
  a spurious `0.4 %` at `g = 0.81ε*` that did not shrink with `Nx` (kept as
  `out/recursion_runs_v1_coarse_phi_search.txt`); the optimal `φ` there is `0.989`.
* At every reported accuracy the minimising `φ` has `φ(u − Λ₁)/g ≥ 5.3`, i.e. lies outside the range
  affected by C1.
Output: `out/recursion_runs.txt` (12 runs).  `check_identities.py` (`out/check_identities.txt`): identity,
(11.18.1), the fields of `HintPair`, "≥" and "≤" of 11.53(b), for `u ∈ {0.1, 0.5, 1, 2, 4, 8}`.

### 4.4 Lean (B.2)

`lake env lean lean/HintRecursionAx.lean` (the file plus `#print axioms` for nine theorems and three
`#check`s): exit 0, 15 s; every theorem depends on `[propext, Classical.choice, Quot.sound]` only; no
`sorry` (`out/lean_axioms.txt`).  `lean/HintRecursionVariant.lean`: `superSolution_le_hint` with the
hypothesis `∃ C, ∀ x > 0, T x ≤ C` — compiles, same axioms (`out/lean_variant.txt`).

### 4.5 Theorem 11.51 (D)

`python3 radial_check.py` (`out/radial_check.txt`, `out/radial_check_part3.txt`).  (1) The algorithm on the
full cube, `(n, u, δ) ∈ {(14,1,.05), (14,2,.05), (12,.5,.05), (10,1,.1)}`, eight families of radial profiles
(random walk, 2-periodic, 2-periodic with random or steepest caps, dip, cone, flattened cone, constant),
`M ∈ {60, 120, 300, 1200}`, 150 runs each: 19 200 runs; 13 283 ended in the exact branch, all with
`|output − ln A| < 10⁻⁹`; 5 917 in the bracket branch, the truth outside once (a dip, `r = 2`; allowed
rate there `0.025`); queries never above `(n+1)M + 2n + 1`.  (2) The deterministic bracket for
2-periodic profiles with the four extremal cap profiles (`A` is monotone in every cap value), all
`r < n/2`, `n ∈ {8, …, 80}`, `u ∈ {0.3, 1, 2, 4}`: 22 752 cases, no violation.  (3) `k*(ε) − r_ε` between `−1` and
`5` for `n = 10³, 10⁴, 10⁵`, `u ∈ {½, 1, 2}`, `ε₁/ε* ∈ {0.1, 0.5, 0.9}`; both sides of the display approach
`θ_hint` (`u = 1`, `ε₁ = 0.1ε*`, `n = 10⁵`: `0.02361` and `0.02376`, `θ_hint = 0.02356`).

## 5. Theorem 11.54: the chain of quantifiers (C)

Fix `u`, `ε₁ ∈ (0, ε*)`, `δ < ½`, `η > 0`.  Choose `g < ε₁` with `θ_hint(g) ≤ θ_hint(ε₁) + η` (continuity), then `k`
with `T_k(g) < θ_hint(g) + η` (11.53(d)), then the parameters of the `k − 1` levels, then `n → ∞`.

*Assembly.*  Let a family have the nonincreasing exponent function `T` (cost monotone in `x` and `δ′`).
For a tuple `p = (φ, β, g, η₀)` Theorem 11.52 (corrected, with abort, ladder in units of `n_i`) gives for
every `d` and `δ` a procedure of accuracy `gd + ln(4eJ_d + 3)` and cost `C_p(d, δ) ≤ exp(d(τ_p + η₀) + o(d))`
for `δ = e^{−cd}`, any `c` (the inner calls use the finitely many rates `ξ_l` and one sequence `δ′ ≥ e^{−c″n_i}`).
Enumerate a countable dense set of tuples; let the new procedure for `(d, x, δ′)` be the cheapest among
the old one and the first `d` tuples with `gd + ln(4eJ_d+3) ≤ x`.  Its cost is nonincreasing in `x`, and for
fixed `ξ` every tuple with `g < ξ` is eventually admissible: `T′(ξ) ≤ min(T(ξ), inf_{g<ξ} R[T](g)) + η₀`, i.e.
`T′ ≤ min(T, R[T])(·⁻) + η₀`.
*Shift.*  If `T̃ ≤ T(·⁻) + η` then `R[T̃](g) ≤ R[T](g − ε) + ε + η` for `0 < ε < g`: for `(φ, β′)` with `β′ < g − ε`
take `β = β′ + ε`; `μ` is the same; `T̃(γ/(1−φ)) ≤ T((γ−ε)/(1−φ)) + η`; substitute `γ′ = γ − ε`.
*Induction.*  `T̃₁ = θ_na`; if `T̃_k ≤ T_k(·⁻) + η_k` then `T̃_{k+1} ≤ min(T_k, R[T_k])(·⁻) + η_k + 2η₀ = T_{k+1}(·⁻) + η_{k+1}`.
So at accuracy `ε₁n` the level-`k` family costs `exp(n(T_k(g) + kη′) + o(n))` for every `g < ε₁`, and the
midpoint of a bracket of accuracy `ε₁n` is `(ε/2, δ)`-correct.  The `o(n)` at level `k + 1` consists of the
polynomial factors (`K = O(n + ln 1/δ)`, `J = O(n)`, `1/η₀`) and the finitely many `o(n_i)` of level `k`; no
uniformity over a continuum is needed.  The failure probability passed down is `δ/(2^{n+6}n³)` per
level, still `e^{−O(kn)}` at the bottom, so `K` stays `O(kn)`.
*Base.*  Two-sample bracket: `K = 24 ln(4/δ′) = O(d)`, width `≤ ln(3 + 12Γ_d(r̂))` on its good event, cost
`2M = 4K·2^d/|B(d, r̂)| = e^{dθ_na(ξ)+o(d)}` for `ξ < ε*` and `O(d)` for `ξ ≥ ε*` (the closing radius is
`≥ d/2`); the floor `ln 3` is irrelevant at extensive accuracy.
*Lower bound.*  Theorem 11.25(a): `E|Q(0)| ≥ (1 − 2δ)2ⁿ/|B(k*)|` for `(ε/2, δ)`-correct algorithms, `ε = ε₁n`,
`k*/n → (Λ₁ + ε₁)/u`; it bounds the expected cost at one instance, hence the worst-case expected and
the worst-case cost.  Same convention as the upper bound.  With M1 "worst case over the class" and
"number of evaluations" are consistent on both sides.

## 6. Prior art (E)

Queries (web search, 25 Nov 2026; no personal or project information): power of adaption in the
randomised setting / Heinrich; adaptive versus non-adaptive Monte Carlo for unnormalised densities
with Lipschitz logarithm; nested sampling with rigorous or certified error bounds; multilevel
splitting with non-asymptotic guarantees or query lower bounds; nested sequential simulation;
Holzmüller–Bach; query complexity of the log-partition function of a Lipschitz function on the
Hamming cube; layer-cake / level-set estimation with adaptive–non-adaptive separation; Sikorski zero
finding; Kunsch–Novak–Wnuk; Jerrum–Valiant–Vazirani / tootsie-pop algorithm.

| source | what it says, as far as I read | how read |
|---|---|---|
| Mathé, Novak, *Simple Monte Carlo and the Metropolis algorithm* (J. Complexity 2007, arXiv math/0611285) | "adaptive methods are much better than nonadaptive ones … the curse of dimension (for nonadaptive methods) can be broken by adaption", for integration w.r.t. an unknown density (log-concave, Lipschitz logarithm), by a Metropolis ball walk | abstract (arXiv page, quoted sentences through a fetch tool); the body is described in R5, which I did not re-read in the source |
| Novak, *On the power of adaption* (J. Complexity 1996) | survey; "the power of adaption is critically dependent on our a priori knowledge concerning the problem" | author's web page, tool summary |
| Traub–Wasilkowski–Woźniakowski surveys; Sikorski 1982 | adaption exponentially better than non-adaption for zero finding; no gain for linear problems on convex balanced classes (Bakhvalov; Kiefer) | search summary only |
| Heinrich, *Randomized complexity of mean computation and the adaption problem* (arXiv 2401.14100) | adaptive/non-adaptive randomised gap of order `n^{1/4}` up to logs | abstract (tool summary of the arXiv page) |
| Kunsch, Novak, Wnuk (arXiv 2308.01705; J. Approx. Theory 2024 according to a search summary) | gap `n^{1/2}(log n)^{−1/2}`; non-adaptive `√(log m)` against adaptive `log log m` | abstract excerpts (tool) |
| Krieg, Novak, Ullrich, *On the power of adaption and randomization* (arXiv 2406.07108) | bounds on the maximal gain for linear problems | abstract (tool summary) |
| Holzmüller, Bach (JMLR 2025) | information-based complexity of log-partition estimation on smoothness classes in fixed dimension | search summary only |
| nested sampling: Skilling 2006; Chopin–Robert, *Properties of nested sampling*; Fowlie et al. 2022; Higson et al. | error estimates are asymptotic or heuristic and assume the constrained sampler | search summary only |
| adaptive multilevel splitting: Cérou–Guyader et al. (fluctuation analysis, CLT) | asymptotic normality; no worst-case certificate | search summary only |
| Broadie, Du, Moallemi (Management Science 2011) | inner samples allocated adaptively to scenarios near the threshold, sequential tests, mean-square criteria | search summary only |
| Jerrum–Valiant–Vazirani 1986; Huber–Schott (tootsie-pop) | counting through a split of coordinates / nested level sets, with a sampler | memory, and a search summary for the second |
| Chatterjee–Diaconis 2018 | sample size `e^{KL}` for importance sampling | memory |

*Assessment.*  Theorem 11.51: not found in print; elementary once stated.  The two-level algorithm:
its ingredients are known — the layer-cake/level-set decomposition (nested sampling, splitting),
effort concentrated near a threshold (nested sequential simulation), a split of the coordinates with
fibre partition functions (self-reducibility) — but a certified, worst-case, one-sided version without
a sampler, closed by an isoperimetric tail bound, was not found.  The identity of 11.53(a) is the
routine fact that `KL(ρ‖p) − KL(ρ‖q)` is affine in `ρ`; its use as `θ_na(e + θ_hint(e)) = θ_hint(e)` and the
recursion were not found.  Theorem 11.54 (exact adaptive exponent equal to the hinted one, against a
strictly larger non-adaptive exponent): not found; the qualitative phenomenon — adaption removes an
exponential barrier of non-adaptive randomised methods for an unnormalised-density problem — is in
Mathé–Novak 2007 for a log-concave class (M4).  **"Not found" is at the level of abstracts and search
summaries; I read no full text.**

## 7. What I did not check

* Lemma 11.43(b) (Harper), Theorems 11.25(a), 11.44, 11.45 and Proposition 11.46 beyond their
  statements and the points noted; I relied on R5 and on the labels of the theory report.
* The Lean proofs line by line: I read the statements, `StepLE`, `HintPair` and the structure of the
  three main proofs, compiled, and printed the axioms; I did not formalise `HintPair` for the cube.
* The real algorithm end to end: the inner procedure was simulated (A.4) or priced by its exponent
  function (A.3); there is no run with real inner two-sample brackets, and none with three nested
  levels.  The in-expectation evaluation replaces counts by expectations; fluctuations are covered
  by the simulation at small and medium size only.
* A.3 on non-radial outer profiles (I argued that only the law of `W` matters, and tested radial laws,
  random and optimised ones included); the actual inner cost on particular inner shapes.
* The uniformity of the `o(n)` terms through `k` levels, other than on paper (§5).
* Remark (3) (other spaces); `DEAD_ENDS.md` D45; `prior_art/L7_query_complexity.md`; harness XV.1; the
  authors' scripts (not run, not read).
* Prior art beyond abstracts and search summaries.
* Floating point: the "rigorous upper bounds" of §4.3 are rigorous up to rounding; no interval
  arithmetic was used.

## 8. Files (all in `scratchpad/referee7/`)

`rlib.py` (formulas, self-test) · `check_identities.py` · `recursion.py` · `two_level.py`, `logic_test.py`,
`demo_q1.py` · `skeleton.py`, `skel_runs.py`, `skel_adversarial.py`, `skel_T2.py` · `radial_check.py` ·
`lean/HintRecursionAx.lean`, `lean/HintRecursionVariant.lean` · outputs in `out/`.
