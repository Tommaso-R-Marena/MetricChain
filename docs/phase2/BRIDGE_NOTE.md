# Phase II — overlap, bridges and oracle models: relations with the certified-MBAR division

*Theoretical Research Division, branch `research/phase2-foundations`, 2026-11-28.  Written after the
research owner's collaboration update of that day ("Certified Statistical Thermodynamics"), which asks
this division to stay informed about the new division `research/phase2-certified-mbar` and to look for
mathematically substantive relations between its findings and ours — without assuming that the oracle
models are equivalent.*

**Status.**  Everything here is the work of one AI session.  **No referee has read it** (the two
adversarial reviews of Phase II predate it).  Proofs are on paper; the deterministic steps are
machine-checked (`proofs/Frontiers/BridgeOverlap.lean`, 12 declarations, standard axioms only); every
numerical claim is reproduced by `experiments/phase2/p2_bridge.py` (output `out_p2_bridge.txt`) and by
harness test XXVIII.5 with 13 mutations, all caught.  Labels: **[V]** machine-checked, **[P]** paper
proof, **[K]** known, **[N]** numerical.

**What was read of the other division.**  Its branch at `003dad8` (opened 2026-11-28 05:23 UTC) contains
a provenance file and an imported package; of the package we read `README.md`, `FABLE_TASK.md`,
`results/EXECUTION_NOTES.md` and `proofs/MAIN_RESULTS.md` (sections A–G) in full.  We did not unpack the
archives, did not read or run its code, and did not review its proofs: §6 says exactly what we checked
of its statements (A1, A2 numerically) and what we only relate to.  Its results are quoted with its
labels (A1, A2, B3, C2, D1, D2, E3, G1).  Ours carry the letters F and J, which neither it nor the
Phase II report uses.

---

## 0. Results at a glance

| | statement | status |
|---|---|---|
| **Theorem F** | every member of the cube class overlaps the reference: `E_π min(w/A, s) ≥ min(½, s(V(n, r_s) + 1)/2ⁿ)`; exponent `KL(ρ₀ − σ/u‖p_u)` for `s = e^{σn}`, attained by the cone; at `s = 1`: `1 − TV(π, μ_w) ≥ e^{−nh − O(log n)}` | [P] from Lemma 11.43(b) of the archive; dichotomy [V]; [N] |
| **Corollary F1** | **samples substitute for adaptivity**: with `e^{ν₁n}` samples of the ensemble, `e^{(θ_na(ν₁)+o(1))n}` *non-adaptive* evaluations give `ln A` to bounded accuracy on the whole class — `a` at `ν₁ = 0`, `h` at `ν₁ = h`, `0` at `ν₁ = ln cosh(u/2)`; explicit constants | [P]; identities [V]; simulated [N] |
| **Proposition F2** | drawing one approximate sample of the ensemble costs at least `e^{n(h − o(1))}` evaluations | [P] |
| **Proposition F3** | a change of `ln A` cannot be hidden from samples: weights that agree off `D` have ensembles at distance `≥ μ₀(Dᶜ)(1 − A₀/A₁)` | [V] |
| **Theorem J** | observables that are functions of the *energy*, at tolerance `e^{−γn}`: the cost has exponent between `θ_hint(γ)` and `min(h, θ_na(γ))`; both vanish at `γ* = ln cosh(u/2)`, above which a bounded number of evaluations suffices — a sharp threshold | [P]; arithmetic [V]; [N] |
| §6.2 | the MBAR division's variance (its A1) in dual form: `V_c(s) = max_a (Σ c_k E_k a)²/Σ s_k Var_k(a) = bᵀM(s)⁺b` with `M(s)` *linear* in `s` — allocation is a `c`-optimal design problem | [P] given its A1; [N] on 300 instances |
| §6.3 | with correlated samples of unequal correlation times the variance of MBAR on the raw samples is **not convex** in the allocation (counterexample, simulated); with effective counts it is | [N] counterexample; [P] |
| §4, §6.4 | the oracle models are not equivalent, in either direction (two counterexamples) | [P] |

---

## 1. Three ways to learn about an ensemble, and a dictionary

Setting and notation of `PHASE2_REPORT.md` §1: `X = {0,1}ⁿ`, `π` uniform, `𝒲_u` the admissible weights
(`w(x) ≤ e^{u d(x,y)}w(y)`), `A(w) = E_π w`, `μ_w = wπ/A(w)`, `g = w/A` the density of the ensemble,
`m_r = 2^{−n}Σ_{j<r} C(n,j)(e^{u(r−j)} − 1)` the excess mass of a dip of radius `r`,
`V(n,k) = Σ_{j≤k} C(n,j)`; `p_u = 1/(1+e^u)`, `a = KL(p_u‖½)`, `ρ₀ = p_u + a/u`, `h = KL(ρ₀‖½) = KL(ρ₀‖p_u)`.
From the archive (theory report, Theorems 11.44, 11.45, 11.25, 11.54): at an accuracy `ε₁n` the
non-adaptive exponent is `θ_na(ε₁) = min{KL(ρ‖½) : KL(ρ‖p_u) ≤ ε₁}` and the adaptive one
`θ_hint(ε₁) = KL(ρ₀ + ε₁/u‖½)`; `θ_na(0) = a`, `θ_hint(0) = h`, and both vanish at
`ε₁ = ln cosh(u/2) = KL(½‖p_u)`.

An algorithm can learn about `μ_w` in three ways, which the owner's note asks us to keep apart:

* **(E) energy values**: it chooses a point and is told `w` there (the archive; exponent `h`
  adaptively, `a` non-adaptively);
* **(S) samples**: it is given points drawn from `μ_w` (Theorem E of the report); in the MBAR division's
  model every sample comes with the values of all energies at it, so here: a sample `Y` with `w(Y)`;
* **(O) averaged observations**: it is told `E_{μ_w}φ` within a tolerance — for functions `φ` of the
  *position* fixed in advance (Theorems A, A′, B of the report), or, new in §5, for functions of the
  *energy*.

**Dictionary.**  The MBAR division studies `K` states `p_k = q_k/Z_k` on a common measure space, with
independent samples from each state and all `q_j` evaluated at every sample; the unknowns are the `Z_k`.
Our problem is its case `K = 2`, `p₀ = π` (`Z₀ = 1`), `p₁ = μ_w`, `q₁/q₀ = w`, `f*₁ − f*₀ = −ln A(w)` — with one
difference of substance (§4): there the *base measure* is unknown and the weight functions are known;
here the base measure `π` is known and the weight is unknown but structured.  For two states its
Laplacian is `ℓ(s)·[[1,−1],[−1,1]]` with

    ℓ(s) = s₀s₁ ∫ p₀p₁/(s₀p₀ + s₁p₁),        ½·∫min(s₀p₀, s₁p₁)  ≤  ℓ(s)  ≤  ∫min(s₀p₀, s₁p₁)

(`harmonic_between_min` [V]), its effective resistance is `R = 1/ℓ(s)` and its variance
`V_c(s) = 1/ℓ(s) − 1/s₀ − 1/s₁`.  At `s = (½, ½)`: `ℓ = ¼(1 − Δ/2)` with `Δ = ∫(p₀−p₁)²/(p₀+p₁)` the
triangular discrimination, and `Ω/4 ≤ ℓ ≤ Ω/2` with `Ω = ∫min(p₀,p₁) = 1 − TV(p₀,p₁)`, with equality on
the left for identical states.  For `p₀ = π`, `p₁ = μ_w`:

    ∫min(s₀π, s₁μ_w) = s₁·Ω_{s₀/s₁}(w),        Ω_s(w) := E_π min(g, s).

So the conductance of the two-state problem *is* the truncated mean `Ω_s`, up to a factor two; the
quantity "overlap" of the bridge-sampling literature is `Ω₁`.  For `n` independent sites the exponential
rate of `Ω₁` is the Chernoff information of the site laws [K]; `h` is that number for `Bernoulli(½)`
against `Bernoulli(p_u)` (report §1).  What was missing is a statement about the *whole class*.

---

## 2. Theorem F: every ensemble of the class overlaps the reference

**Theorem F [P; the dichotomy is `overlap_ge_of_tail_bound` [V]; the tail inequality is Lemma
11.43(b) of the archive, [P] + Harper's theorem [K]].**  Let `w ∈ 𝒲_u`, `s > 0`, and
`r_s := max{r ∈ {0,…,n−1} : s·m_{r+1} ≤ ½}` (`r_s := −1`, `V(n,−1) := 0`, if there is no such `r`).  Then

    Ω_s(w) = E_π min(w/A(w), s)  ≥  min( ½ ,  s·(V(n, r_s) + 1)/2ⁿ ).

*Proof.*  Let `D = {g > s}`.  First, `Ω_s = 1 − E_π(g − s)₊` (`sum_min_eq_sub_tail`) and
`Ω_s ≥ s·|D|/2ⁿ` (`card_superlevel_mul_le_sum_min`).  If `|D| ≤ V(n, r_s)`: either `D = ∅` and `Ω_s = 1`, or
`r_s ≥ 0`, `∅ ≠ D ≠ X` (as `V(n, r_s) < 2ⁿ`), and Lemma 11.43(b) applies to the level set of the admissible
weight `g` — *the mass above a threshold is at most the excess of a dip on a ball of the size of the
super-level set*, `E_π(g − s)₊ ≤ s·m_{r_s+1}` — so `Ω_s ≥ 1 − ½`.  Otherwise `|D| ≥ V(n,r_s) + 1`.  ∎

**Sharpness and exponents.**  (i) For the cone `w = e^{−u|x|}` and `s = e^{σn}` with
`−ln cosh(u/2) ≤ σ ≤ a`: `{g ≥ s} = {|x| ≤ κn}`, `κ = ρ₀ − σ/u ∈ [p_u, ½]`, and by the Chernoff bound for
the two binomial tails and the identity `KL(κ‖p_u) = KL(κ‖½) + u(κ − ρ₀)`,

    Ω_s(cone) = s·π(|x| ≤ κn) + μ(|x| > κn)  ≤  2·e^{−n KL(κ‖p_u)} ;        Ω₁(cone) ≤ 2e^{−nh}.

(ii) The bound of the theorem has the same exponent: `n^{−1}ln m_r → u(ρ − ρ₀)` gives `r_s/n → κ` and
`n^{−1}ln[s·V(n,r_s)/2ⁿ] → σ − KL(κ‖½) = −KL(κ‖p_u)` ([N]: at `n = 20 000` the two agree to `4·10⁻⁴`; at
`n = 8…14` the cone's overlap is 3.4 to 7.9 times the bound).  Hence, for `−ln cosh(u/2) < σ < a`,

    lim −n^{−1} ln inf_{w ∈ 𝒲_u} Ω_{e^{σn}}(w)  =  KL(ρ₀ − σ/u ‖ p_u),        and at σ = 0:   h.

(iii) The cap `½` is needed: for small `un` every radius satisfies `s·m_{r+1} ≤ ½` near `s = 1`, the
second term is `1`, and `Ω₁ = 1 − E(g−1)₊ < 1` for every non-constant member (found by a mutation of the
harness test, which a first choice of instances did not catch).

**Corollary (effective resistance of the class).**  For two states `π, μ_w` with weights `s`:
`R(s) = 1/ℓ(s) ≤ 2/(s₁Ω_{s₀/s₁}(w))`.  At equal weights `sup_{w ∈ 𝒲_u} R = e^{nh + O(log n)}`: at most
`4·max(2, 2ⁿ/(V(n,r₁)+1))` on the class, at least `e^{nh}` at the cone.  **The adaptive query exponent of
the class equals the exponent of its largest two-state effective resistance** — a third reading of
`h`, next to "hinted exponent" and "Chernoff information".  The same combinatorial number carries
both: Theorem 11.25 gives `E|Q| ≥ (1−2δ)2ⁿ/V(n,k)` for an accuracy below `ln(1 + m_{k+1})`, and Theorem F
gives `1/Ω₁ ≤ 2ⁿ/(V(n,k)+1)` at the largest `k` with `m_{k+1} ≤ ½`.

---

## 3. Corollary F1: the bridge, and samples in place of adaptivity

For every threshold `θ > 0` (`bridge_identity` [V]):

    A(w)  =  E_π[min(w, θ)] / E_{μ_w}[min(1, θ/w)] ,

a ratio of two means of variables with values in `[0, θ]` and `[0, 1]`.  With `θ = sA` the two means are
`A·Ω_s` and `Ω_s`: both are the overlap.  (The MBAR division's C2 uses the same identity with the
logistic function in place of the minimum, for any pilot value; the two differ by a factor at most 2.)

**Estimator.**  Input: `N₀` independent uniform points `X_i`, `N₁` independent samples `Y_j` of `μ_w`, the
values of `w` at these points and at one fixed point `x⁰`.  Let `s* = N₀/N₁`, `K₀ = ⌈un + |ln s*|⌉ + 1`,
`θ_k = w(x⁰)e^k` for `|k| ≤ K₀`, and

    S^a_k = Σ_i min(w(X_i)/θ_k, 1),     S^b_k = Σ_j min(1, θ_k/w(Y_j)),
    k̂ = argmax_k min(S^a_k, S^b_k),     Â = θ_k̂ · (S^a_k̂/N₀)/(S^b_k̂/N₁).

It is non-adaptive in the sense of the report: the evaluation points depend on the seed and on the
samples, not on evaluated values.

**Corollary F1 [P; last step `ratio_within` [V]].**  Let `0 < ε ≤ 1`, `0 < δ < 1`.  If

    min( N₁/2 ,  N₀·(V(n, r_{s*}) + 1)/2ⁿ )  ≥  54e·ε^{−2}·ln(4(2K₀ + 1)/δ),

then `|ln Â − ln A(w)| ≤ ε` with probability at least `1 − δ`, for every `w ∈ 𝒲_u`.  In particular
`N₀ = N₁ = N` with `N ≥ 54e·ε^{−2}ln(4(2K₀+1)/δ)·max(2, 2ⁿ/(V(n,r₁)+1)) = e^{nh + O(log n)}`.  In exponents:
`N₁ = e^{ν₁n}` samples and `N₀ = e^{ν₀n}` evaluations suffice whenever `ν₀ > θ_na(ν₁)`,

    (ν₁, ν₀) above the curve { (KL(ρ‖p_u), KL(ρ‖½)) : p_u ≤ ρ ≤ ½ },

which runs from `(0, a)` through `(h, h)` to `(ln cosh(u/2), 0)`.

*Proof.*  `|ln(A/w(x⁰))| ≤ un` by admissibility, so some `|k*| ≤ K₀` has `s_{k*} := θ_{k*}/A ∈ [s*, e·s*)`.
The means are `E S^a_k = N₀Ω_{s_k}/s_k` and `E S^b_k = N₁Ω_{s_k}`, and `A = θ_k·(E S^a_k/N₀)/(E S^b_k/N₁)` for
every `k`.  At `k*` both means are at least `Λ := N₁Ω_{s*}/e` (`Ω_s` is nondecreasing and `Ω_s/s`
nonincreasing in `s`), and `Λ ≥ e^{−1}min(N₁/2, N₀(V(n,r_{s*})+1)/2ⁿ)` by Theorem F.  Let `η = ε/3`,
`M₀ = (1−η)Λ/(1+η) ≥ Λ/2`.  By the multiplicative Chernoff bounds for sums of independent variables in
`[0,1]` [K], outside an event of probability `4(2K₀+1)e^{−η²M₀/3} ≤ δ` every one of the `2(2K₀+1)` sums is
within a factor `1 ± η` of its mean if that mean is at least `M₀`, and below `(1+η)M₀` otherwise.  Then
both sums at `k*` are at least `(1−η)Λ = (1+η)M₀`, so the same holds at `k̂`, so both means at `k̂` are at
least `M₀` and both sums are within `1 ± η`; `Â/A ∈ [(1−η)/(1+η), (1+η)/(1−η)]` and `ln((1+η)/(1−η)) ≤ 3η`.
For the exponents let `ρ* = ρ₀ − (ν₀ − ν₁)/u`, so that `r_{s*}/n → ρ*` when `p_u ≤ ρ* ≤ ½`, and let `ρ₁` be the
point of the curve above `ν₁`.  Since `KL(ρ‖½) − KL(ρ‖p_u) = u(ρ₀ − ρ)`, the hypothesis `ν₀ > θ_na(ν₁)` is `ρ* < ρ₁`,
and then `ν₀ − KL(ρ*‖½) = KL(ρ₁‖p_u) − KL(ρ*‖p_u) > 0`, which is the condition on `N₀`.  For `ρ* < p_u` the radius
`r_{s*}` lies where `m_r` has the exponent `−KL(ρ‖½)` and the condition on `N₀` reduces to `ν₁ > 0`; for `ρ* > ½` the
ball is more than half of the cube.  ∎

**Remarks.**  (1) *What it changes in the report.*  Without samples, non-adaptive algorithms need
`e^{na}` evaluations (Theorem 11.45) and adaptive ones `e^{nh}`.  With `e^{nh}` samples, *non-adaptive*
evaluation at the samples and at as many uniform points reaches `e^{nh}`: on the class, a supply of
samples is worth what adaptivity is worth.  Remark (3) after Theorem E said that the bridge identity
costs `1/μ_w(w ≤ A)` samples "which at the cone is again `e^{nh}`"; Theorem F shows that the cone is the
worst case.  **It does not beat `e^{nh}`**: whether samples can is still open (Theorem E: at least
`e^{0.40·hn}`).

(2) *One curve, three resources.*  `θ_na` is the trade-off between the two error exponents of testing
`Bernoulli(½)ⁿ` against `Bernoulli(p_u)ⁿ` (Hoeffding 1965; Blahut 1974) [K].  The archive found it as the
cost of plain Monte Carlo at an *accuracy* `ε₁n`; here it is the cost at bounded accuracy with `e^{ν₁n}`
*samples*; in §5 it is the cost with a *tolerance* `e^{−γn}` on observables of the energy.  In all three
the algorithm may ignore the part of the ensemble of mass `e^{−n·(\cdot)}`: because the accuracy allows
it, because the samples do not see it, because the tolerance hides it.

(3) *Simulation* ([N], `p2_bridge.py` B4; cubes of 14, 16, 18 sites with slopes 1, 4, 6; 14 instances —
cones, dips, maxima of 40 dips, regularised random energies — with overlaps from `0.64` down to
`7·10⁻⁴`): at `N = 30/(ε²Ω₁)` no error beyond `ε = ½` on any instance (300 runs each; 60 for the two with
`N > 10⁵`); at `N = 3/(ε²Ω₁)` between 0.3 and 20 %; at `N = 0.3/(ε²Ω₁)` 31 to 68 %.  The scale `1/Ω₁` is right
for this estimator; the constant `54e` of the corollary is not optimised (it gives `N = 46 550` at
`n = 14`, `u = 1`, `ε = ½`, `δ = 0.1`, where a few hundred suffice).

(4) *Not claimed.*  A lower bound for algorithms with samples in general.  The cone, on which the
bridge needs `e^{nh}`, is trivial for an algorithm that may explore (§4).  The MBAR division's B3
states that the maximum-likelihood estimator itself reaches bounded accuracy with `N ≳ R·log` samples;
with the corollary of §2 that is the same sample size, by another estimator; we have not checked B3.

(5) *When a sample has a price.*  If one sample costs as much as `e^{κn}` evaluations, the balanced
bridge costs `e^{n·b(κ)}` with `b(κ) = min_ρ max(KL(ρ‖½), KL(ρ‖p_u) + κ) = KL(ρ₀ − κ/u‖½)` for
`−ln cosh(u/2) ≤ κ ≤ a` — the optimum equalises the two exponents, the large-deviation form of the
MBAR division's condition "`Var_k(z)/a_k` constant" (its A2).  `b(0) = h`; `b(κ) = a` from `κ = a` on
(no samples); and `b(κ) = θ_hint(−κ)`, the adaptive exponent function continued to negative accuracies.
With the price of Proposition F2, `κ = h`: `b(h) = 0.0452 > h = 0.0291` at `u = 1` — to produce samples by
evaluations and bridge them is worse than to integrate adaptively, as it must be.

---

## 4. What a sample costs, what it sees, and why the models are not equivalent

**Proposition F2 (sampling) [P].**  Let an algorithm evaluate `w` adaptively and output a point whose
law is within total variation `κ < 1` of `μ_w`, for every `w ∈ 𝒲_u`.  Then for every `r ≥ 1`

    E|Q(1)|  ≥  ( m_r/(1+m_r) − κ )·2ⁿ/V(n, r−1) − 1

at the constant weight; with `r` the least radius such that `m_r ≥ (1+κ)/(1−κ)`:
`n^{−1}ln E|Q(1)| ≥ h − o(1)`.

*Proof.*  Fix the seed, let `Q` be the points evaluated on `w ≡ 1` and `y` the output there.  If
`Q ∩ B(c, r−1) = ∅` the run on the dip `w_{c,r}` is the same run and outputs `y`.  Its output must lie in
`B(c, r−1)` with probability at least `μ_{w_{c,r}}(B(c,r−1)) − κ ≥ m_r/(1+m_r) − κ`.  Averaged over a
uniform `c`: `P(Q ∩ B(c,r−1) ≠ ∅) ≤ E|Q|·V(n,r−1)/2ⁿ` and `P(y ∈ B(c,r−1)) = V(n,r−1)/2ⁿ` (every point
lies in exactly `V(n,r−1)` balls).  ∎

So `e^{nh}` is at once the price of one sample (F2, from below), the number of samples that makes
evaluation non-adaptive (F1), and the price of the integral without samples (archive).  With samples of
`⌈un⌉ + 1` tempered ensembles given for free the problem is polynomial for every weight with
`max w/min w ≤ e^{un}`: adjacent ensembles `∝ w^{j/⌈un⌉}π` have density ratios in `[e^{−1}, e]`, hence
Bhattacharyya coefficients at least `e^{−1/2}`, hence (§6.5) conductances at least `e^{−1}/K²` at equal
weights and a resistance of the ladder of at most `e·K³`, `K = ⌈un⌉ + 1`; independently of any statement
about MBAR, the telescoping product of the `⌈un⌉` ratios of adjacent partition functions, each a mean
of a variable whose values lie within a factor `e`, needs polynomially many samples [K].  **The whole
exponential cost of the certified problem is the cost of producing samples.**  An upper bound for
sampling was not examined.

**Proposition F3 (`tv_ge_of_agree_off` [V]).**  If `w₀, w₁ > 0` agree off `D` and `A₀ ≤ A₁`, then
`TV(μ_{w₀}, μ_{w₁}) ≥ μ_{w₀}(Dᶜ)·(1 − A₀/A₁)`.

Every lower bound of the archive and of the report for evaluations and for averaged observations of the
position (Theorems 11.25, 11.45, A, A′, B) uses pairs of weights that agree off a set `D` which carries
little of one of the two ensembles, and whose partition functions differ by a constant factor.  By F3
the two ensembles are then at a constant distance: **no such pair is hard for samples.**  What survives
against samples is the birthday mechanism of Theorem E (the *number* of basins), not hiding.

**The models are not equivalent, in either direction.**

1. *Evaluations or averaged observations do not bound samples.*  The dip `w_{c,r}` with `m_r ≈ 1` costs
   `e^{nh}` evaluations to tell from the constant weight, with or without means of observables of the
   position at a tolerance `e^{−o(n)}` (Theorem A).  One sample of its ensemble lands in the dip with
   probability about ½, and `n + 1` evaluations around it determine the centre and the radius.
2. *Sample lower bounds do not bound evaluations.*  The MBAR division's D1 shows an error of at least
   `(1/16)√(R_c/N)` on a family in which the densities `q_k` are fixed indicators of regions and the two
   instances differ in the *volumes of the regions* — in the base measure — by relative amounts of
   order `√(R_c/N)`.  With a known base measure there is nothing to estimate: `Z_k` is the sum of the
   known volumes on which `q_k = 1`.  Its D2 says so itself and restores the bound by hiding the
   assignment of cells to regions under a random permutation: by making the base measure unknown.  In
   our model the pair (`π`, cone) has `R = e^{nh+O(log n)}` (§2), and an algorithm that knows it faces a
   cone obtains `ln A` *exactly* from `n + 1` evaluations — a point and its neighbours give the centre and
   the height — with no sample at all.  **Instance by instance, `N ≳ R` is a law of the model in which
   the density of states is unknown; it is not a law of ours.**  That the *largest* resistance of the
   class and its adaptive cost have the same exponent (§2) is a statement about the class, and the
   cost comes from another mechanism: finding a dip, not resolving an overlap.

The two programmes are the two halves of one problem — "compute `ln ∫ w dπ` when the pair `(π, w)` is
partly known": there `w` is known along the samples and `π` is not; here `π` is known and `w` is known
only where it is evaluated, but belongs to a class with geometry.

---

## 5. Theorem J: observables that are functions of the energy

Theorems A and A′ of the report are about observables `φ(x)` of the position, fixed in advance.
Experiments also deliver functions of the *energy* — calorimetry, energy histograms, densities of
states.  The bridge identity makes them powerful: `E_{μ_w}[min(1, θ/w)]` is one.

**Model (EO).**  At any time the algorithm may submit a measurable `F : (0,∞) → [−1, 1]` — depending on
its seed, on earlier answers and on evaluated values — and receives a number within `τ` of
`E_{μ_w}[F(w(X))]`.  Any number of such queries; the oracle is adversarial within the tolerance.

**Theorem J [P; the arithmetic of (a) is `one_two_dips_gap`, `mixture_mean_diff_le` [V]].**
(a) *Lower bound.*  Let `r ≥ 1` with `2(r−1) < n` and `1/(1 + 2m_r) ≤ τ`, and let
`ε < ln((1+2m_r)/(1+m_r))`.  Every randomised algorithm that is `(ε/2, δ)`-correct on `𝒲_u` with the oracle
(EO) at tolerance `τ` satisfies, for a dip `w_{c,r}` with a uniformly random centre and every `k ≥ 0`,
`P(|Q| > k) ≥ 1 − 2δ − 2k·V(n,r−1)/2ⁿ`; hence `E|Q| ≥ (1−2δ)²·2ⁿ/(4V(n,r−1)) − ½` on some instance.

(b) *Upper bound.*  Let `s* > 0`, `ω* = min(½, s*(V(n,r_{s*})+1)/2ⁿ)`, `0 < ε ≤ 1`, `K₀ = ⌈un + |ln s*|⌉ + 1`.  If
`τ ≤ εω*/(3 + 2ε)`, then `2K₀ + 1` queries (EO) — the functions `min(1, θ_k/w)`, `θ_k = w(x⁰)e^k` — and
`N₀ ≥ 54e·s*·ε^{−2}ln(2(2K₀+1)/δ)/ω*` evaluations at independent uniform points (and one at the fixed point
`x⁰`) give `ln A` within `ε` with probability `1 − δ`, on the whole class.

(c) *Exponents.*  For `τ = e^{−γn}` and a bounded accuracy `ε < ln 2`, the least number of evaluations
`N(γ)` satisfies

    θ_hint(γ) − o(1)  ≤  n^{−1} ln N(γ)  ≤  min( h, θ_na(γ) ) + o(1)        (0 ≤ γ < γ* := ln cosh(u/2)),

and for `τ ≤ ε·e^{−u}e^{−nγ*}/(4(3+2ε))` already `108e·ε^{−2}ln(2(2K₀+1)/δ)` evaluations suffice.  Both
bounds equal `h` at `γ = 0` and tend to `0` at `γ*`: **`γ* = KL(½‖p_u)` is the exact threshold between
exponential and polynomial cost.**  At `u = 1` (`γ* = 0.1201`): `[0.0163, 0.0283]` at `γ = 0.03`,
`[0.0072, 0.0098]` at `0.06`, `[0.0018, 0.0021]` at `0.09`.  (At `γ = 0`, a constant tolerance `τ`, the accuracy in
(a) is `ε < ln(2/(1+τ))`; the last statement assumes `m_{⌊n/2⌋+1} ≥ ½`, true for large `n`.)

*Proof.*  (a) Let `c` be uniform, `c̄` its antipode, `w₀ = w_{c,r}` and `w₁ = max(w_{c,r}, w_{c̄,r})`.  The two
balls are disjoint, so `A(w₀) = 1 + m_r`, `A(w₁) = 1 + 2m_r`, and with `v = V(n,r−1)/2ⁿ` and `Γ̄` the law of the
weight inside a dip under its own ensemble (the same for both dips, and independent of `c`), the laws
of the weight under the two ensembles are

    P₀ = [(1−v)δ₁ + (m_r+v)Γ̄]/(1+m_r),        P₁ = [(1−2v)δ₁ + 2(m_r+v)Γ̄]/(1+2m_r) :

mixtures of the same two components whose weights differ by `(m_r+v)/((1+m_r)(1+2m_r)) ≤ 1/(1+2m_r) ≤ τ`.
So for every `F` the two means differ by at most `2τ`, and the oracle may answer both instances with
their midpoint — a function of `F` alone.  Run the algorithm with these answers and the value 1 at
every evaluation: this *reference process* does not depend on `c`, so each of its first `k` evaluation
points lies in one of the two balls with probability at most `2v`.  If none does and the process stops
within `k` evaluations, the runs on `w₀` and on `w₁` are that process and return the same number, which
cannot be within `ε/2` of both `ln A`: probability at most `2δ`.  If none does and it does not stop, the
run on `w₀` makes more than `k` evaluations.  Sum over `k < (1−2δ)/(2v)`.
(b) As Corollary F1, with the answers `o_k` in place of the sums `S^b_k/N₁`: accept `k` if
`o_k ≥ ω* − τ` and `S^a_k ≥ (1−η)N₀ω*/(e s*)`, `η = ε/3`.  The index `k*` is accepted; every accepted `k` has
`E_{μ}min(1, θ_k/w) ≥ ω* − 2τ`, so the answer is within a factor `1 ± τ/(ω*−2τ)`, and `τ/(ω* − 2τ) ≤ η`.
(c) In (a), `m_r ≈ e^{γn}/2` gives `r/n → ρ₀ + γ/u`, which is below ½ exactly when `γ < γ*`, and
`2ⁿ/V(n,r−1) = e^{n KL(ρ₀+γ/u‖½) + o(n)}`.  In (b) take `s* = e^{σn}` with `KL(ρ₀ − σ/u‖p_u) = γ`; for the last
statement `s* = 1/(2m_{⌊n/2⌋+1})`, where `ω* ≥ s*/2` and `m_r ≤ e^{u(r − ρ₀n)}`.  ∎

**Remarks.**  (1) *Energy against position.*  For observables of the position the report has, at
tolerance `e^{−γn}`, a lower bound `h̄(2γ)` that vanishes at `γ = a/2` and an upper bound
`(1 − γ/ln 2)h` that is positive up to `γ = ln 2` — the main open problem of the report.  For observables of
the energy the gap closes at both ends and the threshold is known.

(2) *`γ`, not `2γ`.*  A tolerance `e^{−γn}` on an observable of the energy is worth `e^{γn}` samples
(the curve `θ_na` in both cases), not `e^{2γn}`.  Hiding from observables of the position works with many
dips of tiny mass, and the tolerance is compared with a standard deviation (Hoeffding, bounded
differences: `2γ`).  Here it is compared with a *mean* — an overlap — as in the multiplicative
Chernoff bound.  This is the distinction the MBAR division uses when it replaces Hoeffding intervals
by Kullback–Leibler intervals for small overlap probabilities (its C2).

(3) *At a constant tolerance nothing is gained* in the worst case (`θ_hint(0) = h`), whatever functions of
the energy are observed — the analogue, for the whole law of the energy at a positive tolerance, of
the science division's statement for the mean energy (its Proposition 5b, in the table of report §7),
by a pair of one dip against two.  With the *exact* law of the energy the problem is trivial:
`E_μ[1/w] = 1/A`.

(4) *Not settled.*  For `0 < γ < γ*` the two bounds differ; the upper bound uses the oracle with
*non-adaptive* evaluations.  Whether adaptive evaluations of the truncated weight `min(w, θ)` — whose
supremum is at most `e^{n(σ+γ)}` times its mean — reach `θ_hint(γ)` is the natural question.

---

## 6. On the statements of the MBAR division

What follows is offered to that division as statements, proofs and one counterexample
(THY-MSG-0024).  We reviewed none of its proofs.

### 6.1 Its A1 and A2, checked numerically as stated

On 300 random finite instances (`2 ≤ K ≤ 5` states, supports of 3 to 13 points, weights `s` off the
simplex as well): `Σ_k s_k Var_k(z) = cᵀL(s)⁺c − Σ_k c_k²/s_k` to `10⁻¹²`; `∂V_c/∂s_k = −Var_k(z)` by central
differences to `10⁻⁷`; midpoint convexity without exception (`p2_bridge.py` B8).  This confirms the
statements on small instances, not the proofs, and says nothing about continuous supports.

### 6.2 The dual (Cramér–Rao) form, and allocation as optimal design

**Proposition [P, given the primal representation and the minimiser of its A1; [N] in finite
support].**  For `c ⊥ 1` and positive weights `s`,

    V_c(s)  =  max_a  (Σ_k c_k E_k a)² / Σ_k s_k Var_k(a) ,

over bounded measurable `a` with a positive denominator; when `V_c(s) > 0` the maximum is attained at
`a = z`.  On a finite support: `V_c(s) = bᵀM(s)⁺b`, `b = Σ_k c_k p_k`, `M(s) = Σ_k s_k(diag p_k − p_k p_kᵀ)`.

*Proof.*  Let `r ∈ F_c` (its feasible set: `E_k r_k = 0`, `Σ_k p_k r_k = −Σ_k c_k p_k`).  For bounded `a`:
`−Σ_k c_k E_k a = Σ_k E_k[r_k a] = Σ_k E_k[r_k(a − E_k a)] ≤ Σ_k ‖r_k‖_k sd_k(a)
≤ (Σ_k ‖r_k‖²_k/s_k)^{1/2}(Σ_k s_k Var_k a)^{1/2}`, so the quotient is at most `Σ_k ‖r_k‖²_k/s_k`, whose minimum
over `F_c` is `V_c(s)` by A1.  At `a = z`, with its minimiser `r_k* = s_k(μ_k − z)`:
`Σ_k E_k[r_k* z] = −Σ_k s_k Var_k(z) = −V_c(s)`, so the quotient is `V_c²/V_c`.  ∎

What it gives.  (i) *Convexity in one line*: for each `a` the function `s ↦ B_a²/Σ_k s_k v_k(a)` is convex
on the positive orthant, and a supremum of convex functions is convex.  (ii) *Optimal design.*  `M(s)` is
**linear** in `s` — it is the information operator of the model in which the base measure is the
parameter, and `diag p_k − p_k p_kᵀ` is the covariance of the indicator vector under state `k`.  So
"minimise `V_c(s)` under `Σ a_k s_k = B`" is the `c`-optimal design problem of the statistical literature
for the vector `b` and the elementary information matrices `M_k` (Elfving 1952; the equivalence
theorems of Kiefer and Wolfowitz; Pukelsheim's monograph) [K as a class of problems]; its A2 —
`Var_k(z)/a_k` constant on the support of the optimum, `z = M⁺b` — is the equivalence theorem of that
problem, and its group-norm programme E2 has the form of Elfving's representation of the optimal value
as a gauge.  This is where a precedent for A1/A2 is most likely to be found.  A search of ours (three
queries; summaries of a search engine only, no paper opened) reports that the abstract of Gill, Vardi
and Wellner (1988) announces a final section on design issues and lists Neyman allocation among its
keywords, that the original MBAR paper sets the choice of states aside, and found no statement of
convexity of the multistate variance in the sampling fractions.  That section should be read before
any claim of novelty for A1.
(iii) *Every observable bounds the variance from below*: `V_c(s) ≥ (Σ_k c_k E_k a)²/Σ_k s_k Var_k(a)`; for
two states and `a = 1_T`: `V ≥ (p₁(T) − p₀(T))²/(s₀p₀(T)(1−p₀(T)) + s₁p₁(T)(1−p₁(T)))`.  An observable whose
means under two states differ by many of its standard deviations certifies a poor overlap — the
statistical counterpart of "an observable that separates the states" in our Theorems A–C.

### 6.3 Correlated samples: convexity fails for the raw estimator, and what replaces it

Let the samples of state `k` be a stationary chain with long-run variance functional `σ_k²(·)`, the
chains independent.  Linearising the MBAR equations (the delta method; we state no regularity
conditions — in the example below the space is finite and the chains are geometrically ergodic),
`N·Var(cᵀf̂) → Σ_k s_k σ_k²(z_s)`, with `z_s` the function of its A1 at the allocation `s` (a per-state decomposition of the asymptotic variance of MBAR
with correlated data is in print — "Understanding the sources of error in MBAR through asymptotic
analysis", arXiv:2203.01227, the paper the handoff cites as Li et al. 2023; we know it from a search
summary and did not open it).  For lazy chains — stay with probability `λ_k`, else a fresh draw — `σ_k² = C_k Var_k` with
`C_k = (1+λ_k)/(1−λ_k)`, and the variance is `F(s) = Σ_k C_k s_k Var_k(z_s)`.

**Counterexample [N; simulated].**  `K = 3` states on four points,

    p₁ = (0.0344, 0.8010, 0.1182, 0.0463),  p₂ = (0.4817, 0.3260, 0.1709, 0.0215),  p₃ = (0.2941, 0.0319, 0.2172, 0.4568)

(each renormalised), `C = (1.706, 135.105, 1.053)`, `c = e₂ − e₁`, `s = (0.2047, 0.0295, 0.7658)`,
`t = (0.2387, 0.6463, 0.1149)`:

| allocation | `F` (formula) | simulated `N·Var`, raw MBAR | with weights `1/C_k`: `V_c(s/C)` | simulated |
|---|---|---|---|---|
| `s` | 69.00 | 68.4 ± 3.1 | 6.15 | 6.50 ± 0.29 |
| `(s+t)/2` | 183.78 | 170.8 ± 7.6 | 7.90 | 7.61 ± 0.34 |
| `t` | 163.95 | 153.3 ± 6.9 | 13.04 | 13.55 ± 0.61 |

(`p2_bridge.py` B9: `N = 6·10⁵`, 1 000 replicates per allocation; the estimate is the Newton solution of
the MBAR equations on the occupation counts of simulated chains; the errors are one standard error of
a variance estimated from 1 000 values.  Two earlier runs with other seeds gave `180.3 ± 8.1` and
`181.4 ± 4.1` (4 000 replicates) at the midpoint.)  `F` at the midpoint exceeds **both** endpoints: the
variance of MBAR on the raw samples is not convex, not even quasi-convex, in the allocation; simulated
excess over the mean of the endpoints `60 ± 9` against `67.3` by the formula.  A random search (B8c)
finds such instances readily once the `C_k` differ by a large factor.

**What replaces it [P].**  (i) Run the same equations with the *effective* fractions `s_k/C_k`, each
sample of state `k` weighted by `1/C_k`: then `N·Var → V_c(s₁/C₁, …, s_K/C_K)`, which is convex in `s` by A1,
and A2 holds with the costs `a_kC_k`.  It is the minimum of `Σ_k C_k‖r_k‖²_k/s_k` over the feasible set `F_c`
of A1, so no estimator whose influence functions lie in `F_c` does better on lazy chains.  In the
instance above it is 11 to 23 times smaller than the variance of the raw estimator.  (ii) For general
chains `min_{r ∈ F_c} Σ_k σ_k²(r_k)/s_k` is convex in `s` by the perspective argument of A1 verbatim, since
`σ_k²` is a nonnegative quadratic form; whether an estimator attains it we did not examine.  So an
"optimal allocation for correlated samples" (its task 5) is a convex problem for the *weighted*
estimator and not for the raw one, and "replace `N` by an effective `N`" is right exactly when the
estimator is changed with it.

### 6.4 Where its minimax bound lives

§4, item 2: D1 varies the base measure with the densities fixed, and D2 hides the base measure.  A
bound of that kind for our class would have to hide *volume* from an algorithm that knows the
geometry; Theorem E of the report does it with the number of basins (birthday bound) and reaches
`0.40·h`.  The two-point family of D1 and our dips are the two elementary ways in which two instances
can be close for an observer: a small relative change everywhere (statistical), a large change in a
place that is hard to find (computational).

### 6.5 Conductances from pairwise affinities

For any `K` states, positive weights `s` and `i ≠ j` (`sq_sum_sqrt_mul_le`, `harmonic_between_min` [V]; [N]):

    s_i s_j·BC_{ij}² / Σ_k s_k   ≤   −L_{ij}(s) = s_i s_j ∫ p_i p_j/m_s   ≤   ∫ min(s_i p_i, s_j p_j),

`BC_{ij} = ∫√(p_i p_j)` the Bhattacharyya coefficient — a lower bound that does not involve the other
states.  By Rayleigh monotonicity [K] every effective resistance of `L(s)` is at most that of the
network with conductances `s_i s_j BC_{ij}²/Σs`.  For a smooth family `BC ≈ 1 − ds²/8` in the Fisher–Rao
metric, which is the bridge between its resistances and information geometry, and gives the known
rule of a number of rungs proportional to the Fisher–Rao length of the path [K].  (The harness found
that the factor `1/Σ_k s_k` is needed off the simplex.)

### 6.6 Its composition E3 and what the archive has of that kind

E3 adds a uniform bound `|ũ_k − u_k| ≤ ε_k` to a statistical radius, and notes that MetricChain is not
assumed to supply such bounds.  With a sup-norm bound alone E3 is sharp.  The archive has two sharper
compositions, both machine-checked, for the case where the *mean* of the remainder `r = u − ũ` under the
sampled ensemble is also measured: `−E r ≤ ln(Z/Z̃) ≤ −E r + L(w)` with `L(w) ≤ w²/8` the largest Jensen gap
of a variable of range `w = 2ε` (theory report, Theorem 11.110(a), `jensen_bracket`; with a variance,
`bennett_bracket` in `BoxBennett.lean`), and its sampled form with an explicit failure probability
(`sampled_free_energy_sandwich`, row G10).  They replace an interval of length `2ε` by one of length
`ε²/2` around a measured mean.  They are statements about a finite configuration space with a known
reference measure and a remainder bounded on all of it; they do not certify any molecular system.

---

## 7. Ingredients of a common theory, and what is missing

1. **One trade-off curve.**  For the reference and the extremal ensemble of the class, the
   Neyman–Pearson curve `θ_na` governs the accuracy rate (archive), the number of samples (F1) and the
   precision of energy observables (J); its balanced point `h` governs adaptive evaluation (archive),
   the overlap and the effective resistance (F), and the price of a sample (F2).
2. **Two regimes of concentration.**  Additive (position observables, hiding, `2γ`) and multiplicative
   (energy observables, samples, overlaps, `γ`).
3. **Which half is unknown.**  A common model would have a class of base measures *and* a class of
   energies, with evaluations, samples and observations as resources.  Its lower bounds would combine
   three mechanisms: a change that is hard to find (ours), a volume that is hard to count (Theorem E,
   its D2), a small change everywhere (its D1).
4. **Allocation.**  Its convex allocation problem and our equalisation of exponents are the same
   principle at two scales (§3, remark 5; §6.2).

**Missing.**  A lower bound for samples above `0.40·h`, or an algorithm below `h`; the adaptive cost with
energy observables for `0 < γ < γ*`; an upper bound for sampling; Theorem F for references other than
the uniform cube (the tail lemma is isoperimetric; workstream I of the archive has the product case
by induction) and for consecutive tempered ensembles, where it would give the worst-case number of
rungs.  Two scalings coincide and we do not know whether it means anything: the exponent of `k` nested
levels is `h + c/k²` (Theorem 11.53b), and a ladder of `k` rungs of Fisher–Rao length `D` has adjacent
Chernoff exponents `nD²/(8k²)`.

---

## 8. Verification

| item | status |
|---|---|
| `proofs/Frontiers/BridgeOverlap.lean` | 12 declarations; `bridge_identity`, `overlap_ge_of_tail_bound`, `tv_ge_of_agree_off`, `one_two_dips_gap`, `mixture_mean_diff_le`, `ratio_within`, `harmonic_between_min`, `sq_sum_sqrt_mul_le` listed in `AxiomAudit.lean`; no `sorry`; `propext`, `Classical.choice`, `Quot.sound` only |
| `experiments/phase2/p2_bridge.py` | 11 checks pass (`out_p2_bridge.txt`): Theorem F and the tail inequality on 10 912 (member, level) pairs, `n ≤ 12`; exponents at `n = 2 000, 20 000`; identities; the estimator on 14 instances; F2, F3; the pair of Theorem J; A1/A2 and the dual form on 300 instances; a failure of convexity with correlated samples found by search (B8c, reported as information) and one such instance simulated (B9) |
| harness XXVIII.5 | survives in both modes; 13 mutations, all caught (the block XXVIII: 40 of 40) |
| not machine-checked | Lemma 11.43(b) (Harper), the Chernoff bounds, the coupling arguments of F2 and J(a), all exponents |
| review | **none** |

Reproduction: `python3 experiments/phase2/p2_bridge.py` (about three minutes); `python3
experiments/falsify_conjectures.py --only XXVIII.5`; `python3 experiments/mutation_tests.py XXVIII`;
`lake env lean proofs/Frontiers/BridgeOverlap.lean`.
