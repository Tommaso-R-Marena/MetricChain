# Inference limits: what models, energy evaluations and measurements jointly determine

*Science division, coordinator's research thread.  **Version 3** (checkpoint 18, 2026-11-25):
version 2 with the corrections of its referee (workstream R3,
`docs/science/workstreams/R3_REPORT.md`: no numbered statement false; eight major findings,
all about sentences that said more than the theorems; replacement texts N1–N13 applied
here and listed in §14).  Results obtained after version 2 are in
`INFERENCE_LIMITS_ADDENDA.md` (A1–A11) and summarised in §14.  Theory commit referred to:
`5ed4072` (some statements now also cite `89ac710`).  Scripts: `experiments/science/pi_inference/`,
`experiments/science/pi_chain/`.*

Labels: **[V]** machine-checked · **[P]** paper proof given here · **[K]** known, cited ·
**[N]** numerical only · **[C]** conjecture · **[H]** heuristic / physical argument.
Prior art: workstream M (`workstreams/SM_REPORT.md`; SCI-MSG-0002, -0003) and the referee's
§6.  **Textbook in other words:** Lemma 1 (a linear code is an orthogonal array), Theorem
2(a,b) (noisy codewords), Theorem 3 (Rao's bound and the moment method under `k`-wise
independence), Theorem 5 (Gibbs–Bogoliubov), Propositions 6 and 9, §8 (generalised moment
problem; maximum occurrence; divergence-ball duals), Theorem 8(a,b) (extent of
falsification).  **Short and not found in print:** Theorem 4 with its relatives (addenda
A1, A8, A10), Proposition 5b, the cancellation of the feature part in Theorem 7, addendum
A11.  "Not found" is not a claim of novelty.

---

## 0. The question

The theory division's query model has one kind of information about the unknown residual
`g`: its value at chosen configurations.  A scientist has others.  We ask what each kind
determines.

Throughout: `X` a finite configuration space, `f` the known part, `μ₀ ∝ e^{−βf}` its Gibbs
measure, `μ_g ∝ μ₀ e^{−βg}` the true ensemble, `Z_g = Σ_x e^{−β(f+g)(x)}`.

| symbol | kind of information | idealisation of |
|---|---|---|
| **I1** | evaluations `g(a)` at chosen `a` | an expensive energy computation at a conformation (the theory division's "anchor") |
| **I2(Φ)** | expectations `E_{μ_g} φ`, `φ ∈ Φ` known functions | ensemble-averaged structural measurements; `Φ_k` = all functions of at most `k` coordinates = all marginals on at most `k` sites |
| **I3** | `U = E_{μ_g} g`, the mean of the *unknown* function in the true ensemble | a thermodynamic (calorimetric) measurement of the mean energy relative to the model's |

Targets: `ln(Z_g/Z_0)` (the theory division's), the entropy `S(μ_g)`, populations `μ_g(A)`,
averages `E_{μ_g} ψ`.  Classes for `g`: the **first-order class** `g(x) − g(y) ≤ d(x,y)`
(on the cube `{0,1}ⁿ` with `d = c·d_H`: single-flip differences at most `c`; `b := βc`), and
**linear classes** `g ∈ span{φ_1, …, φ_K}`.

Summary of this file, for the cube class with zero known part unless said otherwise:

| information | what it certifies | status |
|---|---|---|
| I2(`Φ_k`), **when the data are the uniform marginals** | **nothing about the entropy** beyond the a-priori range of the class, up to `⌊k/2⌋ ln(2n) + ln 2`: some class members with exactly these data have entropy within that distance of the class minimum (Theorem 2).  A statement about one data vector and about large `n` (it has content when `n(ln 2 − h(σ(b)))` exceeds `ln|C|`); other data can identify the entropy exactly | [P], enumerated; replicated by the referee on three further codes |
| I2(`Φ_k`) | **an upper bound `≈ t!/(n^t (1−2ρ)^{2t})`, `t = ⌊k/2⌋`, on the population of every basin** of radius `ρn` when the marginals are uniform (Theorem 3); attained up to constants; **no lower bound** — the data exclude dominance of one basin and identify no population | [P], enumerated; the bound is asymptotically exact among all measures [N, referee] |
| I1 + I2(`Φ_k`) | the lower bound for all algorithms at the zero residual is divided by at most `2(2n)^{⌊k/2⌋}`: **`θ_hint` unchanged** (Theorem 4); the non-adaptive exponent `θ_na` unchanged as well (addenda A1 = theory report Proposition 11.104 = referee's R5: three independent proofs).  Worst case over the class; on some instances (cones) the oracle is worth an exponential factor to a non-adaptive algorithm | [P] |
| I3 (+ polynomially many I1) | a bracket of `ln(Z_g/Z_0)` of width `J(μ₀, μ_g) + ε`; **at the zero residual — the hardest instance for I1 alone — the cost is `O(n b²/ε²)`** (Theorem 5) | [P]; the inequality is [K] |
| I1 + I3 | **at bounded accuracy (`ε < ½ ln 2`) the worst-case exponent is unchanged**: a visible basin can have a hidden twin with exactly the same mean energy (Proposition 5b).  At extensive accuracy: open | mechanism [P]; the root [N] in this file, **proved by the referee** (R6 of its report; the excess identity re-derived by the coordinator, the two end estimates read) |
| I2(Φ) + model + envelope class | data certify a **lower** bound on the envelope constant and on `KL(truth‖model)`: the bound on `KL(truth‖model)` with a certificate the kernels can check (two partition-function bounds, for pairwise `f` and `Φ`); the bound on the envelope constant with a flow certificate for which no structured family is known yet (Theorem 8, §8) | [P] |
| I2(Φ), `g ∈ span Φ` | everything (exponential-family identifiability; maximum-entropy refinement is exact) (Proposition 6) | [K] |
| I2(Φ), `g ∈ span Φ + r` | maximum-entropy refinement within `TV ≤ tanh(β·osc(r)/4)`, dimension-free, sharp for every value (Theorem 7) | [P], 3 900 random instances; sharp form found independently by workstream M's follow-up and by the referee |

---

## 1. Invariance under a code

**Lemma 1 [P].**  Let `C ⊆ F₂ⁿ` be a linear code whose dual `C^⊥` has minimum distance at least
`k + 1`.  Every probability measure `μ` on `F₂ⁿ` with `μ(x + a) = μ(x)` for all `a ∈ C` has uniform
marginals on every set `S` of at most `k` coordinates.

*Proof.*  `μ = Σ_{cosets} μ(e + C)·Unif(e + C)`, so it suffices to treat `Unif(e + C)`, and by
translation `Unif(C)`.  The projection `π_S : C → F₂^S` is linear.  If it were not onto there
would be `u ≠ 0` in `F₂^S` orthogonal to `π_S(C)`; padded with zeros, `u` is a non-zero word of
`C^⊥` of weight at most `|S| ≤ k`, a contradiction.  A linear surjection has fibres of equal
size.  ∎

(This is the statement that a linear code is an orthogonal array of strength `d^⊥ − 1`.)

**Codes.**  For `n′ = 2^m − 1` and `t ≥ 1` the binary primitive BCH code of designed distance
`2t + 1` has dimension at least `n′ − mt` and minimum distance at least `2t + 1` **[K]**; its dual
`C` has `|C| ≤ 2^{mt} = (n′+1)^t` and dual distance at least `2t + 1`.  Restricting `C` to any `n ≤ n′`
coordinates keeps the orthogonal-array property (a marginal of a marginal).  With
`m = ⌈log₂(n+1)⌉` and `t = ⌈k/2⌉`: **for every `n` and `k` there is a linear code `C` of length `n`,
dual distance `> k`, and `|C| ≤ (2n)^{⌈k/2⌉}`.**  For odd `k` the extended BCH code gives
`|C| ≤ 2(2n)^{⌊k/2⌋}` (referee, R3); by Rao's bound no code has fewer than `Σ_{j≤⌊k/2⌋} C(n,j)` words.
Restricting to `n` coordinates preserves the dual distance, not the minimum distance of `C`.

## 2. Uniform local data do not identify the entropy in a first-order class

**Theorem 2 (invisible order) [P].**  Cube class, zero known part, `b = βc > 0`,
`σ(b) = 1/(1 + e^{−b})`, `h` the binary entropy (nats).  Let `C` be as in Lemma 1 and

    ν_{C,b} = |C|⁻¹ Σ_{a ∈ C} P_a,        P_a = ⊗_i Bernoulli(x_i = a_i with probability σ(b)).

(a) `ν_{C,b} = μ_g` for some `g` of the class.
(b) Every marginal of `ν_{C,b}` on at most `k` coordinates is uniform.
(c) `n·h(σ(b)) ≤ S(ν_{C,b}) ≤ n·h(σ(b)) + ln|C|`.
(d) Every member of the class has `S(μ_g) ≥ n·h(σ(b))`.
(e) Consequently the set of entropies of class members all of whose `k`-body marginals are
    uniform contains `[n·h(σ(b)) + ⌈k/2⌉ ln(2n), n ln 2]`, while the whole class has entropies in
    `[n·h(σ(b)), n ln 2]`.

*Proof.*  (a) In the weights `w = dμ/d(uniform)` the class is the cone
`{w > 0 : w(x⁽ⁱ⁾) ≤ e^{b} w(x) for all x, i}` (theory report, remark after Theorem 11.12;
`admissible_iff_weights`).  A cone is convex; each `P_a` has `w(x⁽ⁱ⁾)/w(x) ∈ {e^{b}, e^{−b}}`.
(b) `ν_{C,b}(x + a′) = ν_{C,b}(x)` for `a′ ∈ C` because `P_a(x + a′) = P_{a+a′}(x)`; apply Lemma 1.
(c) Upper end: the entropy of a mixture is at most the entropy of the mixing law plus the
mean entropy of the components, and `S(P_a) = n·h(σ(b))`.  Lower end: (d).
(d) For `μ_g` in the class the conditional odds of `x_i` given all other coordinates are
`w(x^{i=1})/w(x^{i=0}) ∈ [e^{−b}, e^{b}]`, so the conditional law has entropy at least `h(σ(b))`, and
`S = Σ_i H(x_i | x_1 … x_{i−1}) ≥ Σ_i H(x_i | x_{−i}) ≥ n·h(σ(b))`.
(e) `b′ ↦ S(ν_{C,b′})` is continuous on `[0, b]`, equals `n ln 2` at `b′ = 0`, and `ν_{C,b′}` is in the
class and has uniform `k`-body marginals for every `b′ ≤ b`.  ∎

*Numerical check* (`code_cone_check.py`, exact enumeration): simplex codes `[7,3]`, `[15,4]`
(`k = 2`) and Reed–Muller codes `RM(1,3)`, `RM(1,4)` (`k = 3`), `b ∈ {0.5, 1, 2, 4}`, for the
variant `μ ∝ e^{−b·d_H(x,C)}`: all marginals of order `≤ k` uniform to `10⁻¹³`, order `k + 1` not
(deviations `10⁻³`–`10⁻¹`), entropies between the two ends of (c) in all sixteen cases.
*Two caveats of the referee.*  The statement "the entropies fill the a-priori range up to
`ln|C|`" is empty unless `n(ln 2 − h(σ(b))) > ln|C|`; of the sixteen cases, nine are in that
regime.  And the check is of the variant `e^{−b·d_H(x,C)}`, for which the upper end of (c) is
not proved above (it is: referee's R4, by Harris' inequality).  The referee also shows that
the price is sharp within mixtures of polarised basins: the least excess entropy over
`n·h(σ(b))` compatible with uniform `k`-body marginals is `⌊k/2⌋ ln n + O_k(1)` there (R2); for
the whole class this is open.

**Reading.**  `ν_{C,b}` is an equal mixture of polynomially many basins, each as ordered as
the class permits.  Every per-site and every `k`-site ensemble-averaged measurement returns
exactly what the uniform ensemble would.  Entropy per site is `h(σ(b))` instead of `ln 2`: for
`b = 2` (single-flip energy differences of at most `2 k_BT`), `0.365` against `0.693` nats.  The
order becomes visible only in an observable of order `d^⊥ ≥ k + 1` (a parity along a
minimum-weight word of `C^⊥`), or in a non-local one.

**What the class assumption does and does not do.**  Without any class the statement is
classical (there are `k`-wise independent distributions on `n^{O(k)}` points).  The content of
Theorem 2 is that the *physical-looking* constraint "flipping one site changes the energy
by at most `c`" does not help at all: the gap between the two ends is the whole a-priori
range.  The constraint that does help is the interaction **order** of the energy (§5).

## 3. What local data do certify: basin populations

**Theorem 3 (basin bound) [P].**  Let `μ` be *any* probability measure on `{0,1}ⁿ` with uniform
marginals on every set of at most `k` coordinates, and `t = ⌊k/2⌋`.  With the Krawtchouk
polynomials `K_j(d) = Σ_i (−1)^i C(d,i) C(n−d, j−i)`, let `F_t(d) = Σ_{j ≤ t} K_j(d)` and
`M_t = F_t(0) = Σ_{j ≤ t} C(n,j)`.  For every centre `a` and radius `r` with `F_t > 0` on `[0, r]`,

    μ( B(a, r) )  ≤  M_t / min_{d ≤ r} F_t(d)².

In particular `μ({a}) ≤ 1/M_t`, and for `r = ρn`, `ρ < ½`, `t` fixed, `n → ∞`:
`μ(B(a, ρn)) ≤ (1 + o(1))·t! / (n^t (1 − 2ρ)^{2t})`.

*Proof.*  With `χ_T(x) = (−1)^{Σ_{i∈T} x_i}` put `f(x) = Σ_{|T| ≤ t} χ_T(a) χ_T(x)`.  For `|T|, |T′| ≤ t`
the product `χ_T χ_{T′} = χ_{T △ T′}` depends on at most `2t ≤ k` coordinates, so
`E_μ χ_T χ_{T′} = [T = T′]`, whence `E_μ f² = M_t`.  Also `f(x) = F_t(d_H(x, a))`.  Markov:
`μ(B)·min_B f² ≤ E_μ f² = M_t`.  For the asymptotics, `K_j(d)/C(n,j) → (1 − 2d/n)^j`.  ∎

(The case `r = 0` is the weighted form of Rao's bound for orthogonal arrays **[K]**.)

**Attainment.**  For `ρ > 1 − σ(b)` the mixture `ν_{C,b}` of Theorem 2 gives
`ν(B(a, ρn)) ≥ (1 − o(1))/|C| ≥ (1 − o(1))·(2n)^{−⌈k/2⌉}` for `a ∈ C`.  So, with the extended code for odd
`k`, for every `k` the largest basin population compatible with disordered-looking `k`-body data
is `n^{−⌊k/2⌋}` up to a constant factor depending on `k` and `ρ`.  (The hypothesis `F_t > 0` restricts
`r` to `r < n/2 − O(√(tn))`; near `n/2` the plain moment bound is better.  The check below covers
`t = 1` and three centres per measure.)  *Numerical check* (`basin_bound_check.py`): identity
`E_μ f² = M_t` and the inequality on `C`-invariant measures (exponential weights and random
coset weights), all centres tried and all radii; attained/bound up to `0.995` (simplex code
`[15,4]`, where `|C| = M_1 = 16`).

**Reading.**  Disordered-looking local data *do* exclude one dominant folded basin, with a
bound that improves polynomially with the order of the data, and *do not* exclude a
mixture of `n^{⌊k/2⌋}` basins.  The population of every single basin is bounded **above** by
`≈ n^{−⌊k/2⌋}`, and up to a constant this is the largest value compatible with the data; it is
not bounded below (the uniform ensemble has the same data).  So the data exclude dominance
of one basin; they identify neither the populations nor the number of populated basins —
the entropy.  *(Version 2 said "populations of individual states are identified up to
polynomial factors".  That was false: only the upper end is polynomial.  Corrected after
the referee's M2; SCI-MSG-0008.)*  The largest weight a conformation can have in any ensemble reproducing averaged data
is the quantity computed numerically as "maximum occurrence" in the NMR literature
(to be compared in detail: workstream M); Theorem 3 is an analytic instance.

## 4. Two oracles: evaluations and local data

**Theorem 4 (a marginal oracle is worth at most a polynomial factor at the zero residual)
[P].**  Cube class, zero known part.  Consider a randomised algorithm that evaluates `g`
adaptively, *is given all marginals of `μ_g` on at most `k` sites exactly*, and outputs `ln Z_g`
within `ε` with probability at least `1 − δ` for every `g` of the class.  Suppose that for
some radius `r` the dip `g_a(x) = −c·(r − d_H(x, a))₊` has `ln Z_{g_a} − ln Z_0 > 2ε` (this does not
depend on `a`).  Then at `g ≡ 0`

    E[number of evaluations]  ≥  (1 − 2δ) · 2ⁿ / ( |C| · V(n, r) ),

`V(n, r) = |{x : d_H(x, 0) < r}|`, for every linear code `C` of dual distance `> k`; in particular
with `|C| ≤ (2n)^{⌈k/2⌉}`.

*Proof.*  Put `g_a^C(x) = −c·(r − d_H(x, a + C))₊`.  (i) It is in the class: the distance to a set
is 1-Lipschitz.  (ii) It is invariant under translation by `C`, hence so is `μ_{g_a^C}`, and by
Lemma 1 its `k`-body marginals are uniform — the oracle's answers at `g ≡ 0`.  (iii)
`g_a^C ≤ g_a ≤ 0`, so `ln Z_{g_a^C} ≥ ln Z_{g_a} > ln Z_0 + 2ε`.  (iv) `g_a^C` vanishes outside
`U_a = {x : d_H(x, a + C) < r}`, and `|U_a| ≤ |C|·V(n, r)`.  Run the algorithm at `g ≡ 0` and let `Q` be
the random set of evaluated points.  On `{Q ∩ U_a = ∅}` the run is identical at `g_a^C`; both
outputs cannot be within `ε` of targets more than `2ε` apart, so `P(Q ∩ U_a ≠ ∅) ≥ 1 − 2δ` for
every `a`.  For `a` uniform and independent of the run, `P(x ∈ U_a) = |U_0|/2ⁿ` for each fixed `x`, so
`1 − 2δ ≤ E|Q|·|C|·V(n,r)/2ⁿ`.  ∎

This is the indistinguishability argument of the theory division's Theorem 11.22 with a
symmetrised alternative.  (Convention: `ε` here is half the width `ε` of the theory report.)
Since `|C| = e^{o(n)}` whenever `k = o(n/ln n)`, **for accuracies with `ln(1/ε) = o(n)` below the
threshold, both exponents of the theory division's diagram for the cube — the non-adaptive
`θ_na` (Theorems 11.44–11.45) and the adaptive `θ_hint` (Theorems 11.54 and 11.58, paper
proofs) — are the same with and without free access to all `k`-body ensemble data,
`k = o(n/ln n)`.**  The adaptive half is Theorem 4 with their upper bound; the non-adaptive
half is addendum A1 (= their Proposition 11.104 = the referee's R5).  This is a worst-case
statement over the class: at a cone instance the one-body marginals reveal the centre,
and a non-adaptive algorithm with the oracle then needs one evaluation.

*Not proved here.*  (i) ~~The non-adaptive exponent~~ — proved: addendum A1.  (ii) A known
part that is not `C`-invariant (a field; any chain): **open, and the reason we do not
trust "local data are worth nothing" beyond the uniform cube.**  (iii) Tolerances: with
every correlation function known to absolute precision `τ ≥ e^{−o(n/ln n)}` the exponent is
still unchanged, for *all* orders (addendum A10); with exact marginals of order `αn` it does
drop (addendum A8).

## 5. A thermodynamic datum is a different kind of information

**Theorem 5 (two-sided perturbation bracket) [K for the inequalities; P for the reading].**
For every `g` (no class needed), with `U = E_{μ_g} g`:

    −β E_{μ₀} g  ≤  ln(Z_g/Z_0)  ≤  −β U,
    width = β(E_{μ₀} g − E_{μ_g} g) = KL(μ₀‖μ_g) + KL(μ_g‖μ₀) =: J(μ₀, μ_g).

If moreover `μ₀` is a product measure and `g` has single-site bounded differences `c_i`, then
`N` independent samples `x_1 … x_N` of `μ₀` give, with probability at least `1 − δ`,

    −β( N⁻¹ Σ_s g(x_s) + (Σ_i c_i² · ln(1/δ) / (2N))^{1/2} )  ≤  ln(Z_g/Z_0)  ≤  −β U.

*Proof.*  `Z_g/Z_0 = E_{μ₀} e^{−βg} ≥ e^{−βE_{μ₀}g}` and `Z_0/Z_g = E_{μ_g} e^{βg} ≥ e^{βU}` (Jensen; the
Gibbs–Bogoliubov inequality in both directions, standard in free-energy perturbation).  The
width identity: `KL(μ₀‖μ_g) = βE_{μ₀}g + ln(Z_g/Z_0)` and `KL(μ_g‖μ₀) = −βU − ln(Z_g/Z_0)`.  The
sampled form: McDiarmid's inequality for the mean of `N` i.i.d. copies of a function with
bounded differences (sub-Gaussian with variance proxy `Σc_i²/4`).  ∎

**Corollary (the hardest instance for evaluations alone is the easiest with a thermodynamic
datum) [P].**  Cube class, zero known part, at `g ≡ 0`: the oracle returns `U = 0`, all sampled
values are `0`, and `N = n b² ln(1/δ)/(2ε²)` evaluations certify `−ε ≤ ln(Z_g/Z_0) ≤ 0` with
probability `1 − δ`.  Without the datum every algorithm needs `e^{nθ_hint − o(n)}` evaluations
there for accuracies below the threshold `n ln cosh(b/2)` (theory report Theorem 11.25).

*Why.*  The exponential cost at the zero residual is the cost of excluding hidden
low-energy regions.  A hidden region that matters for `Z` is populated, and a populated
low-energy region lowers the mean energy: `U = 0` together with `ln(Z_g/Z_0) ≤ −βU` excludes
every dip at once.  Local structural data cannot do this (Theorem 4) because a symmetrised
family of dips leaves every `k`-body marginal untouched.

**Instance dependence.**  The bracket's width is `J(μ₀, μ_g) = β² ∫₀¹ Var_{μ_{sg}}(g) ds`: the
certificate is tight exactly when the model is good, and both ends are *measured*, so the
width is known a posteriori.  For a generic member of the class `J` is extensive; the
a-priori product-reference sandwich of theory report §3.2 has width `β²Σc_i²/8`.

*(Referee's N11, on the Corollary of Theorem 5.)*  The algorithm: compute the bracket;
return its midpoint if its width is at most `ε`; otherwise fall back on any class-correct
procedure.  It is correct on the whole class and costs `N` at `g ≡ 0`.  A tolerance `τ_U` on the
datum widens the bracket by `βτ_U`.

**Proposition 5b (at bounded accuracy the datum does not lower the worst-case exponent: a
visible basin can have a hidden twin) [mechanism P; the existence of the root: N in this
file (exact sums in floating point); proved in the referee's report, R6, by an excess
identity, a sign lemma and an overlap bound — the identity re-derived by the coordinator,
the estimates read].**  Cube class,
`u = βc`, `ρ₀ = ln(2/(1+e^{−u}))/u` (the radius at which a dip matters for `Z`; theory report
§11.10).  Fix `ρ₁ > ρ₀`, `r₁ = round(ρ₁n)`, a public centre `a₀`, and the base instance
`g₀ = −c·(r₁ − d_H(x, a₀))₊` — one visible basin that dominates `Z`.  For a hidden centre `a′` and
`s ∈ (−1, 1)` let `g′ = min(g₀, −c·(r₁ + s − d_H(x, a′))₊)`.  Adding a region whose *excess* mass has
mean energy `m` changes `U` to a weighted mean of `U` and `m`; when the visible basin dominates,
a twin of almost the same radius has `m ≈ U`, and by continuity in `s` there is `s*` with
**exactly** `E_{μ_{g′}} g′ = E_{μ_{g₀}} g₀`, while `ln Z_{g′} − ln Z_{g₀} ≈ ln 2`.  Since `g′ = g₀` outside
`B(a′, r₁ + 1)`, an algorithm with an exact I3 oracle and accuracy `ε < ½(ln Z_{g′} − ln Z_{g₀})` must
still evaluate `g` inside that ball for (almost) every `a′`:
`E[#evaluations] ≥ (1 − 2δ − o(1))·2ⁿ/V(n, r₁ + 1)` at `g₀`.  Letting `ρ₁ ↓ ρ₀`: **the worst-case
exponent with the thermodynamic oracle is at least `ln 2 − h(ρ₀)`, the hinted exponent at
bounded accuracy — the same as without the oracle.**  Only the hard instance has moved,
from "nothing is there" to "is the visible state the only one?".
*Numerical evidence* (`calorimetric_twin_check.py`, `calorimetric_twin_exact.py`; exact sums
over the joint law of the two distances, overlapping supports included): `u = 1`,
`ρ₀ = 0.3799`; for `n = 1000`, `ρ₁ = ρ₀ + 0.01` and hidden centres at distance `0.3n`, `0.45n`, `0.5n`:
`s* = −0.0049`, equal mean energies to `10⁻¹³`, `ln Z′ − ln Z₀ = 0.691`; for `n = 5000`,
`ρ₁ = ρ₀ + 0.002`: `s* = −0.039`, `ln Z′ − ln Z₀ = 0.674`, asymptotic exponent `ln 2 − h(ρ₁) = 0.0282`
(`0.0289` at `n = 5000` with the polynomial prefactor) against the hinted `0.0291`.  There is a
root as soon as the visible basin dominates by a factor of order `n` (`W ≥ 8r₁e^u·2ⁿ` suffices,
referee's R6.2); at `u = 1`, `ρ₁ = ρ₀ + 0.01` this is `n ≥ 400`, and there is none for `n ≤ 300`.
The statement is for accuracies `ε < ½(ln Z_{g′} − ln Z_{g₀}) ≈ ½ ln 2`; at extensive accuracy
equal-depth twins fall short of `θ_hint(ε₁)` ~~and the question is open~~ — **partly settled
in addendum A16 (checkpoint 26):** the datum alone gives `ln Z` within `n·KL(σ_u‖½)/2` (an
entropy bracket), which removes an exponential cost for accuracies between `KL(σ_u‖½)` and
`ln cosh(u/2) = KL(½‖σ_u)` per site; below, a twin that is as deep and exponentially wider (a
"plateau twin") gives a lower bound close to `θ_hint(ε₁)`; the exact exponent there is a
conjecture.  With any tolerance
on the datum the twin with `s = 0` already does: the exact root is the price of the exact
oracle, not of the phenomenon (referee's remark).  The referee's Corollary R6′ extends the
statement to both oracles together (`k`-body marginals and the mean energy).

**Reading.**  Calorimetry excludes hidden states *deeper* than what is seen (they would
lower the mean energy) and cannot exclude a hidden state *as deep as* what is seen.  With
local structural data added the twin must also reproduce the visible state's `k`-body
marginals; at maximal polarisation that is impossible (the product measure with
single-site probabilities `σ(u)` is the only member of the class with those one-body
marginals), below it we expect designs around `a₀` to supply twins **[C]**.

*Open.*  (i) ~~A proof of the root~~ (referee's R6; second reading done, addendum A12; a
machine check of its three finite inequalities is with workstream L2), and the exponent
at extensive accuracies below `KL(σ_u‖½)` per site (bracketed in addendum A16).  (ii) **Physical status of
the oracle [H]:** `E_{μ_g} g = E_{μ_g}(f+g) − E_{μ_g} f` is a calorimetric mean energy minus the
model energy averaged over the true ensemble; the second term is determined by `m`-body
marginals when `f` has interaction order `m`.  Neither is cleanly measurable for a solvated
macromolecule; temperature-dependent calorimetry (`∂ ln Z/∂β = −E_{μ}(f+g)`) is the realistic
form.  The theorem is about kinds of information, not about an instrument.

## 6. The positive side: when local data determine everything

**Proposition 6 (exponential-family identifiability) [K].**  Let `Φ = (φ_1, …, φ_K)` be functions on
`X`, `μ₀` of full support, `g = λ·Φ`.  Then `μ_g` is the unique minimiser of `KL(·‖μ₀)` among measures
with the same `Φ`-means (the I-projection; Csiszár 1975 **[from memory — to be verified by
workstream M]**), hence `μ_g` is determined by `μ₀` and `E_{μ_g}Φ`; and
`ln(Z_g/Z_0) = −β λ·E_{μ_g}Φ − KL(μ_g‖μ₀)` is determined as well when the constant function is not
in the class.  In particular, **in a linear class, exact I2(Φ) data replace all evaluations
of `g`**: zero queries of type I1 are needed for any Boltzmann average, where the theory
division's Proposition on linear classes needs rank-many evaluations (theory report §11.17).

For energies of interaction order at most `m` this says that the marginals on `m` sites
determine the ensemble, and the maximum-entropy refinement of the model is exact.

**The pair-distance-profile class is the class identified by scattering.**  The class of
theory report §11.17 — pair-additive residuals `g(x) = Σ_{pairs} u_{type}(r_{ij}(x))` with unknown
radial functions — is the linear span of the pair-distance histogram features (per pair of
types).  Their ensemble averages are the (partial) pair-distance distribution functions,
which is what small-angle scattering measures up to a linear transform **[K]** (the Debye
formula; resolution and form factors aside).  So within that class a complete scattering
measurement determines the ensemble (the finite-chain form of Henderson's theorem **[K]**),
and the class designed for cheap *computation* is at the same time the class of complete
*measurement*.

**Theorem 7 (stability of maximum-entropy refinement) [P].**  Let `X` be finite, `μ₀` of full
support, `μ ∝ μ₀ exp(−β(λ·Φ + r))` with `r` bounded, `ω = osc(r) = max r − min r`, and let `ν` be the I-projection of `μ₀` on
`{E Φ = E_μ Φ}` (the maximum-entropy refinement of the model against exact data).  Then

    (i)   KL(μ‖ν) + KL(ν‖μ) = β (E_ν r − E_μ r);
    (ii)  TV(μ, ν) ≤ tanh(βω/4);
    (iii) KL(μ‖ν) + KL(ν‖μ) ≤ βω·tanh(βω/4);
    (iv)  |E_μ ψ − E_ν ψ| ≤ osc(ψ)·tanh(βω/4) for every bounded ψ;
    (v)   0 ≤ KL(μ‖μ₀) − KL(ν‖μ₀) = KL(μ‖ν) ≤ βω·tanh(βω/4)      (and ≤ (βω)²/8: addendum A5),

independently of `|X|`, of the number and nature of the features, and of `μ₀`.

*Proof.*  `ν ∝ μ₀ e^{−βλ′·Φ}` for some `λ′`, so `ln(dμ/dν) = β(λ′ − λ)·Φ − βr + const`.  Then
`KL(μ‖ν) + KL(ν‖μ) = (E_μ − E_ν) ln(dμ/dν) = β(λ′−λ)·(E_μΦ − E_νΦ) − β(E_μ r − E_ν r)`, and the first
term vanishes because the means agree: (i).  `|E_ν r − E_μ r| ≤ ω·TV(μ,ν)`, and
`KL(μ‖ν) + KL(ν‖μ) ≥ 2·TV·ln((1+TV)/(1−TV))` (reduce to the two-cell partition `{μ > ν}`, `{μ ≤ ν}`
and minimise); so `ln((1+TV)/(1−TV)) ≤ βω/2`: (ii), then (iii), (iv).  (v) is the Pythagorean
identity for I-projections on linear families.  ∎  (Version 2 used Pinsker's inequality
and obtained `βω/4` and `(βω)²/4`, vacuous for `βω ≥ 4`.  The mechanism is Barron–Sheu 1991:
SCI-MSG-0003.)

Sharp for every `βω`: two points, no feature, `r = (0, ω)`, `μ₀ = (1, e^{βω/2})/(1+e^{βω/2})` give
`TV = tanh(βω/4)` and equality in (iii).  *Numerical check* (`maxent_stability_check.py`): 3 906
random instances (`|X| ≤ 39`, up to 6 features, `βω ∈ {0.05, …, 8}`), largest ratios
`TV/(βω/4) = 0.99989`, `J/((βω)²/4) = 0.99989`; identity (i) and Pythagoras to `10⁻⁷`.

**Reading.**  Maximum-entropy refinement is exactly as good as the span of the measured
observables is rich: its error is controlled by the part of the true correction *outside*
that span, not by the size of the system or of the correction itself.  Theorem 2 shows the
other side: a remainder with bounded differences `c` per site has `ω` up to `nc`, and then
nothing is controlled.

*Open.*  (i) An extensive version: if `ν` satisfies a transport–entropy inequality
`W₁(μ,ν) ≤ (2κ n KL(μ‖ν))^{1/2}` in the Hamming metric and `r` has bounded differences `c`, then
(i) gives `KL(μ‖ν) ≤ 2κ n (βc)²` — a per-site bound whose order `(βc)²` Theorem 2 shows to be
attained (`ln 2 − h(σ(b)) ≈ b²/8`) **[P sketch]**.  (ii) Local observables under a mixing
condition: is `|E_μψ − E_νψ|` bounded independently of `n` for `ψ` depending on `O(1)` sites when
`r` is a sum of local terms? **[C]**  (iii) Data with tolerance `τ`: (i) acquires the term
`β(λ′−λ)·(E_μΦ − E_νΦ)`, which is not dimension-free.

## 7. Free-energy differences between macrostates: a caution

The observable free energies are differences, `ln[Z_g(A)/Z_g(B)]`, not `ln(Z_g/Z_0)`.  The
theory division's exact robust interval for `Z_g` (`robust_partition_interval_exact`) rests on
monotonicity in `g`; a ratio is not monotone.  **The residual that maximises `Z_g(A)/Z_g(B)`
over an envelope class is in general not constant on `A`** **[P]**: `X = {x₁, x₂, y}`,
`A = {x₁, x₂}`, `B = {y}`, `d(x₁, y) = 1`, `d(x₂, y) = d(x₁, x₂) = 10` (symmetric; the triangle
inequality holds).  With `g ≡ 0` on `A` the best is `g(y) = 1`.  But `g(x₁) = 0`, `g(x₂) = −9`,
`g(y) = 1` is admissible and multiplies the weight of `x₂` by `e^{9β}`.  In the weights the
problem is a linear-fractional programme over the cone (theory report, remark after
Theorem 11.12), so it has an exact dual; a closed form of the kind of Theorem 11.12 for
ratios of macrostates is, as far as we have read, not in the theory report.  (For a
single state `B = {y}` the maximum has the closed form `Σ_{x∈A} e^{−β(f(x)−f(y)−d(y,x))}`, attained by
`g = −d(y,·)`; the open case is `|A|, |B| ≥ 2`.)  **A closed form does exist in one setting
(addendum A11):** binary sites, a submodular known part and monotone macrostates — there
the two extremal residuals are uniform fields, by Holley's inequality, and uncertainty
common to both macrostates cancels exactly.

## 8. Certified identified sets (framework; soundness only)

For data `E_μ Φ ∈ D` (`D` compact convex, e.g. a box of error bars) and a target `ψ`, the
*identified set* is the range of `E_μψ` over all ensembles consistent with what is known.
Three versions, each with a certificate whose soundness is one line:

* **Model-free [K: generalised moment problem].**  For every `λ`,
  `sup{E_μψ : E_μΦ ∈ D} ≤ h_D(λ) + max_x [ψ(x) − λ·Φ(x)]`, with equality at the infimum over `λ`
  (linear-programming duality; `h_D` the support function).  **The certificate is `λ` together
  with a certified upper bound on a maximum over `X`** — for `ψ, Φ` pairwise in the site
  variables, exactly what the verified `(min,+)` kernel checks.  The bound uses no energy
  model at all: it is a physical, not a model-relative, guarantee, as far as the forward
  models `Φ` and the error bars are.
* **Model within a divergence ball [K: Donsker–Varadhan].**  For every `λ` and `η > 0`,
  `sup{E_μψ : KL(μ‖μ₀) ≤ ρ, E_μΦ ∈ D} ≤ h_D(λ) + ηρ + η ln E_{μ₀} exp((ψ − λ·Φ)/η)`.  **The certificate
  is `(λ, η)` with a certified upper bound on a tilted partition function and a lower bound on
  `Z_0`** — two certificates of the verified `(+,×)` kernel.
* **Model within an envelope class [P].**  With `κ(x,y) = e^{βd(x,y)}`, data
  `m_k⁻ ≤ E_μφ_k ≤ m_k⁺`, multipliers `λ^± ≥ 0`, `Λ(z) = Σ_k λ_k⁺(φ_k(z) − m_k⁺) − λ_k⁻(φ_k(z) − m_k⁻)`,
  and a non-negative "flow" `F` on ordered pairs: if for every `z`

      (ψ(z) − t − Λ(z))·μ₀(z)  ≤  Σ_x F(x,z) − Σ_y κ(z,y) F(z,y),

  then `E_{μ_g}ψ ≤ t` for every admissible `g` consistent with the data.  (Multiply by
  `w(z) = e^{−βg(z)}` and sum: the right-hand side becomes `Σ F(x,y)(w(y) − κ(x,y)w(x)) ≤ 0`, and
  `Σ Λ μ₀ w ≤ 0` by the data.)  The dual object is a **flow with gains** — where minima over
  an envelope class dualise to shortest paths and transport, Boltzmann averages dualise to
  generalised flows.  *Open:* families of flows on product spaces for which the inequality
  can be checked by a pairwise kernel.  **For a ratio of two macrostate weights and no
  data the theory division has the sharp form (theory report §11.28 at `dcdfea6`, Theorem
  11.105; reviewed and replicated by us, SCI-RES-0005):** flows from `B` to `A` suffice, the
  certificate is exact, the optimum is a "closed pair", and for a macrostate defined by
  one coordinate a plan that moves that coordinate only gives a bound a pairwise kernel
  can check site by site (its Theorem 11.107).

Nothing in this section is deep; what is new to the programme is that its kernels are
dual-feasibility checkers for inference from *measurements*, and that the first version
needs no energy model.

## 9. Falsification: data certify a *lower* bound on model error

Envelope constants are inputs that nobody has certified (theory report §8).  Measurements
cannot certify an upper bound on them.  They can certify a lower bound.

**Definition.**  For a model `μ₀ ∝ e^{−βf}` and an envelope `d`, the *Lipschitz divergence* of an
ensemble `μ` from the model is the least `b ≥ 0` such that `μ = μ_g` with `g(x) − g(y) ≤ (b/β)·d(x,y)`:

    D_d(μ‖μ₀) = sup_{x ≠ y}  [ ln( μ(y) μ₀(x) / (μ(x) μ₀(y)) ) ]₊ / d(x, y).

The envelope class with constant `b` is the ball `{D_d(·‖μ₀) ≤ b}`; it is convex in `μ`
(a cone in the weights).  For data `E_μΦ ∈ D` put

    b_min(D) = inf{ D_d(μ‖μ₀) : E_μΦ ∈ D },        ρ_min(D) = inf{ KL(μ‖μ₀) : E_μΦ ∈ D }.

**Theorem 8 (falsification certificates) [P; duality K].**
(a) If the true ensemble is `μ_g` and the data are correct (`E_{μ_g}Φ ∈ D`), then the envelope
constant of `g` is at least `b_min(D)/β`, and `KL(μ_g‖μ₀) ≥ ρ_min(D)`.
(b) For every `λ`:  `ρ_min(D) ≥ −h_D(λ) − ln E_{μ₀} e^{−λ·Φ}`, `h_D(λ) = sup_{m∈D} λ·m`, with equality at
the supremum over `λ`.  **A certificate is `λ` with a certified upper bound on the partition
function of the tilted model `f + λ·Φ/β` and a certified lower bound on `Z_0`** — two outputs of
the verified `(+,×)` kernel.
(c) The data are inconsistent with the envelope class of constant `b` if there are `λ^± ≥ 0`
and a flow `F ≥ 0` with `(1 − Λ(z))·μ₀(z) ≤ Σ_x F(x,z) − Σ_y e^{b·d(z,y)} F(z,y)` for all `z` (notation of
§8); then `b_min(D) > b`.

*Proof.*  (a) is the definition.  (b) Donsker–Varadhan: `KL(μ‖μ₀) ≥ E_μ(−λ·Φ) − ln E_{μ₀}e^{−λ·Φ}`;
equality is maximum-entropy duality.  (c) is §8 with `ψ ≡ 1`, `t = 0`: it would give `1 ≤ 0`.  ∎

**Why this matters [H].**  When a simulated ensemble disagrees with experiment, the
disagreement is due to the model, to incomplete sampling, or to both, and current practice
cannot separate them: the reweighting statistics that quantify "how far the force field
must be moved" are computed from the same finite sample.  `ρ_min` and `b_min` are properties of
the model and the data alone.  A certified lower bound on either is a statement about model
error that no amount of additional sampling can change.  It requires `f` and `Φ` to be
decomposable in the configuration variables (§12).

*Numbers* (`envelope_scaling.py`; diamond-lattice chain, single-torsion moves between the
three torsion-angle states `(t, g⁺, g⁻)`; model = athermal, data = exact
averages under the truth `∝ e^{+ε·c₃}`, `c₃` the number of nearest-neighbour contacts;
"truth's constant" = its largest single-torsion energy change between self-avoiding
conformations, a lower bound on its envelope constant):

| beads | `ε` | truth's constant | `b_min` from `R_g²` | `b_min` from the three-shell profile |
|---|---|---|---|---|
| 8 | 0.25 / 0.5 / 1.0 | 0.25 / 0.5 / 1.0 | 0.068 / 0.150 / 0.360 | 0.220 / 0.438 / 0.866 |
| 9 | 0.25 / 0.5 / 1.0 | 0.5 / 1.0 / 2.0 | 0.079 / 0.176 / 0.436 | 0.240 / 0.482 / 0.952 |

The profile certifies between `0.87·ε` and `0.96·ε` at both sizes, while the truth's worst-case constant
doubles from 8 to 9 beads (one torsion flip can change two contacts: the lever arm of
theory report §11.14 in miniature).  The certified bound tracks the *typical* strength of
the missing interaction, not the worst-case constant **[N: two sizes, one family of
truths; at 10 beads `b_min/ε = 1.06–1.09` and the fraction of the truth's constant is
0.53–0.54, SCI-MSG-0002 §3]**.

## 10. A caloric curve determines `ln Z`

**Proposition 9 [K].**  Let `U(β) = E_{μ_β}(f+g)` be the mean energy at inverse temperature `β`.
`U` is non-increasing, `ln Z(β_m) − ln Z(β_0) = −∫ U dβ`, and for `β_0 < β_1 < … < β_m`

    −Σ_j (β_{j+1} − β_j) U(β_j)  ≤  ln Z(β_m) − ln Z(β_0)  ≤  −Σ_j (β_{j+1} − β_j) U(β_{j+1}),

of width at most `max_j(β_{j+1} − β_j)·(U(β_0) − U(β_m))`.  With `β_0 = 0`, `Z(0) = |X|`.  So `m` mean
energies certify `ln Z_β` within `β·osc(f+g)/m` **with no evaluation of `g`**; for an extensive
accuracy `ε₁n` a number of temperatures independent of `n` suffices.

This is thermodynamic integration.  It is recorded here because of what it says about
targets **[H]**: within the model's own configuration space the total `ln Z` is determined
by a caloric curve without any evaluation of `g` — provided the curve is known down to
`β = 0`, which no experiment provides (calorimetry reaches absolute entropies from the other
end, `T → 0`, and it measures the energy of all degrees of freedom, not `E_μ(f+g)`).  The
quantities for which a certificate would be scientifically new — the population of a
structural state, a contact probability, the entropy of a subsystem — are ratios of
restricted partition functions and conditional averages, for which the exact robust
theory is missing in general (§7; one setting solved in addendum A11); for one Boltzmann
average, the mean magnetisation on the cube, the theory division's Theorem 11.35 shows the
uncertifiable fraction to be larger than for `ln Z`.  *(Version 2 said in bold that "the
total `ln Z` is the one quantity of the programme that experiment delivers without any
model" and that "this is how absolute entropies are measured".  Both sentences claimed
more physics than Proposition 9 contains; withdrawn after the referee's M5.)*

## 11. Identified sets on the programme's lattice chain: numbers

Model: the diamond-lattice chain of theory report §11.17 (`n` torsions, `N = n + 3` beads;
profile = numbers of non-bonded pairs at squared distances 3, 8, 11).  Own enumerator
(`experiments/science/pi_chain/dia_chain.py`).

**Replication.**  For `n = 1 … 10` the conformation counts, class counts and complete class
tables agree exactly with the engineering division's tables at `db56d05`.

**11.1 Model-free, exact data** (`identified_sets.py`; exact linear programmes after
aggregation).  Width of the identified interval as a fraction of the a-priori range, 13
beads, truths athermal / stiff (`e^{−#gauche}`) / attractive (`e^{+c₃}`):

| data | gauche fraction | end-to-end `R²` | population of the most compact decile |
|---|---|---|---|
| `R_g²` | 0.76 / 0.73 / 0.72 | 0.41 / 0.45 / 0.37 | 0.79 / 0.57 / 0.89 |
| three-shell profile | 0.47 / 0.26 / 0.49 | 0.59 / 0.73 / 0.50 | 0.70 / 0.29 / 1.00 |
| full pair-distance histogram | 0.31 / 0.14 / 0.35 | 0.22 / 0.18 / 0.21 | 0.50 / 0.20 / 0.75 |

From 7 to 13 beads the entries grow or level off; none decreases towards zero.  The weight
of the all-trans conformation is identified exactly by the full histogram (it is the only
conformation with a pair at the largest distance): identification depends on whether the
target is in the span of the features, exactly as §6 says.

**11.2 Up to 27 beads, from the engineering tables** (`identified_from_eng_tables.py`).  The
tables give, for every profile class, the least and the largest number of gauche torsions,
which is all the linear programme needs.  Identified interval of the mean gauche fraction
given the exact athermal mean profile:

| beads | 7 | 9 | 11 | 13 | 15 | 17 | 19 | 21 | 23 | 25 | 27 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| lower end | 0.595 | 0.492 | 0.407 | 0.359 | 0.324 | 0.294 | 0.270 | 0.247 | 0.230 | 0.211 | 0.201 |
| upper end | 0.734 | 0.787 | 0.822 | 0.834 | 0.850 | 0.850 | 0.850 | 0.853 | 0.851 | 0.854 | 0.855 |
| width | 0.139 | 0.294 | 0.415 | 0.474 | 0.527 | 0.556 | 0.580 | 0.607 | 0.621 | 0.644 | 0.654 |

(the athermal value is `0.64–0.65`).  **At 27 beads an exact ensemble-averaged three-shell
profile leaves the mean gauche fraction undetermined over two thirds of its range, and the
interval is still widening — and decelerating** (increments of the width per two beads:
`0.155, 0.121, 0.059, 0.053, 0.029, 0.024, 0.027, 0.014, 0.023, 0.010`).

**11.3 The limit is a chord of the theory division's limit shape [P, given theory report
Theorem 11.69; for bridges].**  The model-free identified set of (mean profile, mean gauche count)`/N` over
ensembles of `N`-bead chains is the convex hull of `𝒟_N = {(h(x), g(x))/N}`.  For bridges,
`𝒟_N^{br} → K^{br}` in the Hausdorff metric with `K^{br}` compact and convex (Theorem 11.69), so the
hulls converge to `K^{br}` as well, and at every profile density `p` in the interior of the
projection `𝒦` the identified interval converges to the chord `[γ(p), γ⁺(p)]`,
`γ⁺(p) = max{g : (p,g) ∈ K^{br}}` (this uses that `𝒦` has interior points in `ℝ³`; four affinely
independent points of `K^{br}` are needed — asked of the theory division, R3-T2).  **For
bridges, the limit shape of §11.22 is the asymptotic model-free identified set at interior
profile densities.  For all walks — the ensembles of §§11.1–11.2 — the asymptotic
identified interval contains the chord `[γ(p), γ⁺(p)]` of `K^{br}` (bridges are walks), with
equality under Conjecture 11.75.**  Its lower boundary is the theory division's
least-gauche function, its upper boundary has not been computed.  *(Added at checkpoint
24, from the theory division's answer to our question Q3(c), THY-RES-0005 §3 — a
three-line lemma, checked by us: if the ball `B(p, r)` lies in the convex hull of the
normalised statistics of `N`-bead bridges, then `p` is the mean of exactly one Gibbs measure
with a three-shell pair energy and a stiffness term, and its coefficients are bounded by
`N⁻¹ ln #{bridges}/r ≤ ln 3/r`.  So every interior point of the limit shape is, for large
`N`, the exact mean of a Gibbs measure at finite temperature, uniformly in `N`; only boundary
points need diverging coefficients.)*  In exponential-family terms `K^{br}` is the
mean-parameter set of the family generated by the profile and the gauche count, and its
support function is the ground-state energy density of the corresponding energies.  For
unrestricted walks the same holds under Conjecture 11.75.  Whether the chord at the
athermal point is at least the 27-bead value `0.65` is **[C]** (the finite-size chords
increase at every size computed; the one-sided rate `168/(N+3)` of Theorem 11.69 is vacuous
at these sizes).

**11.4 With a model and its envelope class** (`envelope_identified.py`, `envelope_scaling.py`;
linear-fractional programmes in the weights with single-torsion constraints on all `3ⁿ`
torsion patterns).  Model = truth = athermal chain, envelope constant `b` per torsion; 9 beads:

| target (true value) | envelope `b = 1` only | profile only | both, `b = 1` | both, `b = 0.5` |
|---|---|---|---|---|
| gauche fraction (0.652) | [0.420, 0.825] | [0.492, 0.787] | [0.607, 0.701] | [0.629, 0.677] |
| end-to-end `R²` (46.0) | [31.0, 69.4] | [16.5, 77.6] | [38.2, 53.9] | [42.1, 49.9] |
| compact decile (0.111) | [0.019, 0.345] | [0.000, 0.409] | [0.042, 0.203] | [0.072, 0.156] |

Each kind of information is weak alone; together they are several times stronger than
either.  At 8 beads the corresponding widths are smaller (compact decile, both, `b = 1`:
0.089 against 0.161 at 9 beads; gauche fraction: 0.085 against 0.094).  Two sizes are not
a scaling law; but at fixed `b` the combined interval for a macrostate population must
eventually grow with the chain (a tilt of `b` per torsion can move an event of probability
`p₀` by a factor `e^{Θ(bn)}`), and programmes of this kind have `3ⁿ` variables — beyond about
10 beads they need the structured duals of §8.

## 12. Where the kernels can check such certificates

The certificates of §§8–9 are maxima and partition functions of `ψ − λ·Φ` and `f + λ·Φ/β`.  The
verified kernels handle pairwise (low-treewidth) functions of the configuration variables.
For a backbone in torsion space a pair distance depends on all torsions in between, so
profile-type features are *not* pairwise there.  They are pairwise (or single-site) in:
(i) **side-chain ensembles on a fixed backbone** — rotamers as variables; a pairwise force
field; scalar couplings and order parameters as single-site observables; inter-residue
distance-dependent observables (NOE-type) as pairwise ones **[H]**; (ii) lattice and
coarse-grained models whose features are local along the chain (transfer-matrix
structure).  The first is the physical arena in which the whole chain of reasoning —
model, class, measurement, certificate — could be closed on public fixed-sequence data.

## 13. Open problems arising here (state at version 3; the full list with owners is `OPEN_PROBLEMS.md`)

1. ~~`θ_na` with a `k`-body marginal oracle~~ — unchanged (addendum A1; theory report
   Proposition 11.104; referee's R5).
2. **Theorem 4 with a field, or any known part without a large translation symmetry.**
   ~~Open, and the most important limitation of §§2–4~~ **Settled for one-body data with a
   field (checkpoint 30; workstream F, `workstreams/SF_REPORT.md`; SCI-RES-0006):** neither
   class exponent changes, for every `n` — the hard instance is a two-component mixture
   built by a compensation lemma (add a multiple of an extreme additive instance to both
   members of a pair); at an additive instance the oracle strictly helps for `p ≠ ½`, and
   the instance-wise exponent is bracketed between explicit matched alternatives and a
   tilt inequality.  Open: the exact instance-wise exponent; exact marginals of order
   `≥ 3` with a field (order 2: an exact construction at `n = 13` and a sketch); known
   parts with interactions; chains.
3. The thermodynamic oracle I3 (§5): the root of the hidden twin is proved by the referee
   (R6; second reading done, A12).  **At extensive accuracy (addendum A16):** settled for
   `ε₁ ≥ a(u) = KL(σ_u‖½)` (the datum alone suffices; without it the cost is exponential up to
   `ln cosh(u/2) = KL(½‖σ_u)`); for `ε₁ < a(u)` the exponent lies between the plateau-twin
   bound `ln 2 − h(ρ₀ − σ_u + h⁻¹(h(σ_u)+ε₁))` and `θ_hint(ε₁)` — **open: which** (Conjecture A16.4:
   the lower one), i.e. a tail lemma with an energy constraint; and the instance-wise
   complexity with the datum.
4. The exchange rate between I1 and I2 in classes between linear and first-order.  Known
   now: exact marginals of order `αn` — exponent in `[h_hint − h(α), (1−α)h_hint]` (A8); every
   order at absolute precision `τ ≥ e^{−o(n/ln n)}` — nothing (A10); a linear-information class
   of order `m` — about `n^m` evaluations, and `m`-body data determine the ensemble
   (`ALTERNATIVE_FRAMEWORKS.md` §5).  Open: mixed classes `g = λ·Φ + r`.
5. Extensive and local versions of Theorem 7: the extensive version under a
   transport–entropy inequality is addendum A2; the local version is open.
6. Robust ratios of macrostate partition functions (§7): **solved for binary sites,
   submodular known parts and monotone macrostates (A11), on ordered alphabets (A13), and
   in general as a transport problem with gains by the theory division (theory report
   §11.28: duality, closed pairs, closed forms for exchangeable known parts and type
   macrostates, a single-letter limit; reviewed in SCI-RES-0005)**.  Open: the exact value
   for a pairwise known part and counting macrostates; a condition under which the
   maximal field is the optimal closed pair (common ground of A11 and Theorem 11.106);
   the range *given evaluations*; **the number of evaluations needed to certify a ratio**
   (theory report §12 item 11(a)); tractable flow families with data (§8) for §11.4
   beyond 10 beads.
7. Everything above for alphabets of size `k > 2` and for chains.
8. The upper boundary `γ⁺` of the limit shape and the chord at the athermal point (§11.3);
   class tables for bridges (requests R3-E1, R3-E2) to test how much Conjecture 11.75
   matters for identified sets.
9. Is `b_min ≈ ε` (§9) a theorem about contact residuals?  At 8, 9, 10 beads `b_min/ε` is
   0.87, 0.96, 1.07.
10. *(Referee.)*  Is the least excess entropy compatible with uniform `k`-body marginals
    `⌊k/2⌋ ln n + O(1)` in the whole class (proved within mixtures of polarised basins)?

## 14. What changed since version 2, and what the addenda contain

**Corrections after the referee (workstream R3; no numbered statement was false).**
N1 §0 row 1 and the title of §2 (the entropy statement is about the uniform data vector
and about large `n`); N2 §0 row "I1 + I3" (bounded accuracy only); N3 the reading after
Theorem 3 (**a false sentence withdrawn**: populations are bounded above, not identified);
N4 §0 row on Theorem 8 (what the kernels can check); N5 Proposition 5b (status, rounding,
the criterion for a root, the exponent quoted); N6 §10 (**a physical claim in bold
withdrawn**); N7 §11.3 (bridges against walks); N8 Theorem 7 (sharp form); N9 §4 (both
exponents; the worst case; convention); N10 codes for odd `k`; N11 the algorithm of the
Corollary of Theorem 5; N12, N13 small additions.  The same corrections for the messages
that quoted version 2 are in SCI-MSG-0008.

**Machine-checked (workstream L1; `experiments/science/ws_L1/`, eight files, 78 theorems,
standard axioms only; re-compiled by the coordinator).**  Lemma 1 (over any finite field);
Theorem 3 in Markov form; Theorems 4 and 4′ in full as corollaries of the theory
division's packing bounds (with the code for `k = 1` only — for `k ≥ 2` the code is a
hypothesis); Theorem 5's bracket and Proposition 9; Proposition 6; Theorem 7 (i)–(v) in the
Pinsker form of version 2, for `ν` given in exponential form; the soundness of the three
certificate formats of §8 and of Theorem 8(a)–(c) in the form "no member of the class is
consistent with the data"; Pinsker's inequality itself (absent from Mathlib).  **Not
machine-checked:** Theorem 2; the Krawtchouk form of Theorem 3; the sharp form of Theorem
7; Proposition 5b; every asymptotic statement; everything in the addenda.  Two things the
formalisation found: the theory division's `QueryAlgorithm` cannot represent an
oracle-assisted algorithm (repaired by indexing the algorithm by the oracle's answer; the
statements stand), and Theorem 8(c)'s strict form "`b_min(D) > b`" needs the data set `D` to be
closed.

**Addenda (`INFERENCE_LIMITS_ADDENDA.md`).**

| # | statement | status |
|---|---|---|
| A1 | Theorem 4′: the non-adaptive exponent is unchanged by a marginal oracle | [P]; = theory report Proposition 11.104 = referee's R5; machine-checked given a code |
| A2 | Theorem 7′: `KL ≤ 2κn(βc)²` under a transport–entropy inequality | [P]; machine-checked with the inequality as a hypothesis |
| A3 | Proposition 10: reduction of the robust ratio to a programme on one macrostate | [P] |
| A4 | three ways to compute identified sets under a model, a class and data | [P], [N] |
| A5 | Theorem 7 sharp: `KL ≤ w²/8`, `TV ≤ tanh(w/4)`, `J ≤ w·tanh(w/4)`; mechanism Barron–Sheu | [P], [K] |
| A6 | Theorem 8: "extent of falsification"; a sample-based estimate is biased upward | [K], [P] |
| A7 | pinned marginals — kept with its correction | corrected by A8 |
| A8 | Theorem 4‴: exact marginals of order `αn` — exponent in `[h_hint − h(α), (1−α)h_hint]` | [P] |
| A9 | Theorem 2-τ (exact) and Proposition 4″-τ (pinned ensembles with tolerance) | [P] |
| A10 | attenuation lemma; Theorem 4-τ: every order at tolerance `τ ≥ e^{−o(n/ln n)}` leaves `h_hint` unchanged | [P]; exact rational checks to `n = 800` |
| A11 | robust macrostate ratios attained at two fields (binary sites, submodular known part, monotone macrostates); cancellation of common uncertainty | [P] by Holley's inequality; 900 exact linear programmes and two controls |
| A12 | the oracle-invariance theorem assembled, parts (a)–(d), with who read what; the hidden-twin proof re-derived; the corollary with both oracles written out | [P]; cores machine-checked (L1) |
| A13 | the sandwich of A11 on ordered alphabets (step fields); exact when the envelope is additive along the order | [P]; 360 exact linear programmes |
| A14 | the robust range of the helix content of a Zimm–Bragg chain | [N], exact transfer matrices; reading [H] |
| A15 | what a scattering curve of finite range and precision determines, model-free (11–15 beads) | [N], exact linear programmes |
| A16 | a thermodynamic datum at extensive accuracy: the entropy bracket (the datum alone gives `ln Z` within `n·KL(σ_u‖½)/2`); the window in which it removes an exponential cost; the plateau twin (a lower bound below that accuracy); a conjecture for the exact exponent | [P], author only; exact sums to `n = 2000` |

**The theorem within reach (referee's §9) — written as one statement in addendum A12, and
sent as SCI-MSG-0011; its limit at extensive accuracy is addendum A16:** *oracle
invariance of the complexity diagram of the cube class* — free exact `k`-body marginals
(`k ln n = o(n)`) change neither the adaptive nor the non-adaptive exponent, and with the
mean residual energy given as well the adaptive exponent at bounded accuracy is still `h`,
although the zero residual then costs `O(nu²/ε²)`.  Every new ingredient is a finite
inequality with an elementary proof; every hard ingredient is in the theory report.
