# Workstream K — adaptive algorithms without a hint at a bounded accuracy

> **Repository note (added by the coordinator at integration; the report below is otherwise as
> delivered).**  Status: **paper proofs, refereed after integration (R8: "proved")** — see
> `docs/THEORY_REPORT.md` §11.19 for the integrated statements and their labels and
> `docs/reviews/R8_referee_report.md` for the referee report.  The scripts and outputs
> named in §6 are in `experiments/workstreams/K/` (run from that directory:
> `python3 <script>`, numpy only).  The four Lean files named in §6.7 (`KBounded.lean`,
> `KBoundedLink.lean`, `KBoundedCube.lean`, `KExactRecursion.lean`) were merged, with the theorem
> names unchanged, into `proofs/Frontiers/BoundedAccuracy.lean` (namespace
> `MetricChain.BoundedAccuracy`), where the coordinator added `exactRec_ge_hint` and
> `exactRec_tendsto_hint` (the exact recursion never undercuts, and converges to, the hinted
> exponent).  Theorem numbers of the theory report: K1 = 11.56, K.4 = Lemma 11.55, K0 =
> Proposition 11.57(a), K2 = Proposition 11.57(b), K3 = Theorem 11.58.

> **Errata after the referee report R8** (`docs/reviews/R8_referee_report.md`: verdict "proved",
> no critical or major finding).  The text below is unchanged; the following points of it
> are corrected in the theory report §11.19.  (m1) The abort test must be made *before* an
> inner call (otherwise the cost bound is `C_max + max_l C_l`), and off the good event the
> returned pair can have `L > U` (return the trivial bracket then).  (m2) In Theorem K2,
> "`T′(ξ) = T(ξ)` for `ξ > 0`" is not nonincreasing; read `T′(ξ) = min(T(ξ), T′(0))`.  (m3) The
> hypotheses `λ ≤ 1`, `η′ ≤ 1` of Theorem K1 are not used; claims (iii), (iv) hold for every run,
> not only on the good event.  (m5) "`Γ̃` is never below `4e^u(e^u−1)`" (§0, §3.2, §5) is false at
> `r = 0` and, by a fraction of a per cent, at finite `n`: `min_{r≥1} Γ̃(r) = 4e^u(e^u−1)(1−o(1))`.
> (m6) The remark in §6.8 that numpy's `binomial` returns `0` for `p < 10^{-16}` is false for the
> current generator interface; the remark on `multinomial` is true.  (m7) The non-adaptive
> lower bound at accuracies tending to zero needs the line given in the theory report's
> table.  (m8) The last sentence of Corollary K3′ presupposes that `lim ε_n/n` exists.
> (m9) Remark (2) after Theorem K3: the Lean theorems named there formalise Proposition
> K5(c); the iteration of Theorem K3 is `two_rung_bound`.  (m10) With `x_L = b` exactly, a
> floating-point tie can leave a point unclassified.  Labels: "[proved, given Theorem 11.25(a)
> and Theorem 11.53]" also rests on Harper's theorem, the binomial median, Chernoff–Hoeffding
> and the paper chain K1–K2; "deterministic core machine-checked" means four algebraic lemmas.

> **Errata after the Computational Research Division's checkpoint 3** (ENG-RES-0008 and
> ENG-MSG-0003 on branch `research/ubuntu-engineering`: exact counts of evaluations of
> Algorithm 2L⁺ under a search over instances and inner behaviours; all 324 rows of
> `out_radial_trajectory.txt` and all 18 rows of `out_flat_cost_bounded.txt` reproduced by an
> implementation written from §§2.1–2.3; no claim of Theorem K1 violated in more than seven
> million mean runs).  The text below is unchanged.  **(e1) §6.4, "what the algorithm
> costs", and the sentences that quote it (§0; §6.4 "two levels beat the plain bracket from
> `n ≈ 250`"; the Summary) are best-case numbers: the cost at the flat instance with the outer
> fraction `φ` tuned for the flat instance.**  The flat instance is not the worst instance
> at finite `n`: with the flat-tuned `φ` a radial instance "flat bulk with a slightly
> supercritical dip", or a cone, costs `e^{71}` times more at `n = 1000` and `e^{513}` times more
> at `n = 64 000` (`u = 1`); tuned against the worst instance the best `φ` is `0.50`–`0.60`, the cost
> is `1.04·na` at `n = 1000` and `0.537·na` at `n = 64 000` (instead of `0.70`, `0.512`), and the crossover
> with the plain bracket is at `n ≈ 500` (`u = 1`) and `n ≈ 2000` (`u = ½`).  The exponent `τ₂` is not
> affected.  **(e2) Two rows of `out_radial_trajectory.txt` depend on a floating-point tie**
> ("random walk 1" at `u = 1`, `n_o = 1000`, both variants): with ties treated exactly the
> closing radius is `311` (not `312`), there are `114` negligible levels (not `113`) and
> `ln M/(n_o a) = 0.7573` (not `0.7511`); the reference point's weight lies exactly on the level
> grid whenever its fibre is flat and `un/λ` is an integer, so the tie of (m10) is
> structural, not a rare coincidence.  **(e3) The cap `M̄` can be lowered** to
> `2·max{e^λM†, M‡}`, `M‡ = K/((1−η)·2^{−n_o}|B(n_o, r† − ⌈λ/u⌉)|)` — a constant multiple of `M†` (theory
> report §11.19, remark after Theorem 11.56; the division had observed `M ≤ 1.8·M†` in its
> runs).  **(e4)** For the outer loop radial instances are not "a small subfamily": by
> Harper's theorem the tail functions of all `u`-Lipschitz outer landscapes are those of
> landscapes whose level sets are initial segments of the simplicial order (the division's
> argument, same remark).

Independent report.  All scripts and outputs named below were produced in the workstream's
scratch directory (`python3 <script>`, numpy only, `ulimit -v 4000000`, each run under ten
minutes) and are reproduced in `experiments/workstreams/K/`.  Nothing in the repository was
modified by the workstream, no state-changing git command was run, nothing was delegated.  The
repository was read at commit `1bff191` (the brief) and re-read at `78ed930` after the coordinator
had integrated referee report R7 into §11.18 during this work; the statements below refer to the
corrected Theorem 11.52 (no closure at `r = n_o`, abort rule, ladder relative to the inner
dimension).  At the end of the work the repository was at `4cef47e` (`CubeHintPair.lean`: Theorem
11.53 machine-checked for the cube); the last Lean file below is compiled against it.

Status labels: **[proved]** complete proof in this report (paper proof, unrefereed; where a part is machine-checked or
simulated this is said); **[sketch]** missing steps named; **[numerical]**; **[conjecture]**; **[known]** taken from the
theory report or the literature (source given).

Notation (theory report §11.16/§11.18): `Q_n` the cube, `L_u(Q_n)` the `u`-Lipschitz `ψ`, `w = e^{−ψ}`, `A = 2^{−n} Σ_x w(x)`;
`p_u = 1/(1+e^u)`, `Λ₁ = ln(2/(1+e^{−u}))`, `ε* = ln cosh(u/2)`, `a = KL(p_u‖½) = Λ₁ − u p_u`, `h = KL(Λ₁/u‖½)`;
`θ_na(e) = min{KL(ρ‖½) : KL(ρ‖p_u) ≤ e}`, `θ_hint(e) = KL((Λ₁+e)/u‖½)` (both `0` from `ε*` on);
`B(m, r)` Hamming ball (`|B(m,−1)| = 0`), `E_r(m) = Σ_{j≤r} C(m,j)(e^{u(r+1−j)} − 1)`, `T_m(k) = Σ_j C(m,j) e^{−u(j−k)₊}`.

---

## 0. Verdicts in one page

**Conjecture K is true, in its strong form.**

> **Theorem K3 [proved, given Theorem 11.25(a) (the hinted lower bound) and Theorem 11.53 (convergence of the exact
> level recursion) of the theory report, both machine-checked in the repository].**  For every `u > 0`, every fixed
> accuracy `ε > 0` and every `0 < δ < ½`, the least number of evaluations with which a randomised adaptive algorithm
> without a hint is `(ε/2, δ)`-correct on all of `L_u(Q_n)`, in the worst case over the class, is
> `exp(n·h + o(n))`, `h = KL(Λ₁/u‖½)` — the hinted exponent, for *every* fixed `ε`, not only for large ones; and the
> same holds for every sequence `ε_n = o(n)` with `ln(1/ε_n) = o(n)` (Corollary K3′).

The proof is an algorithm.  It is the two-level layer-cake algorithm of Theorem 11.52 with four changes, each of which
costs only polynomial factors (Theorem K1, §2, explicit constants; change 1 is necessary for a bounded ratio, change 4
for a ratio arbitrarily close to `e^b` — the strong form —, and changes 2 and 3 are what makes the closure provable at a
bounded accuracy):

1. the lower end is the larger of the running bound `ℓ` and a layer-cake **sum** over the populated levels (step (1) of
   the coordinator's sketch — correct);
2. the running bound `ℓ` also contains, at every populated level, the **Harper lower bound** of the two-sided tail lemma
   11.43(c): if a fraction `p̲` of the fibres lies above `t`, then `A ≥ t·2^{−n_o}·T_{n_o}(k)` with `|B(n_o,k)| ≤ 2^{n_o} p̲`.  With it a
   populated level closes at *every* radius `r ≤ p_u n_o − O(√n_o)`, with a tail that is an arbitrarily small fraction of
   `ℓ`.  This replaces the "closure window" of step (2) of the sketch, which does not work as described;
3. the factor in the negligibility threshold is raised from `J` to `max(J, const·n_o/θ)`, so that an unpopulated level
   closes at every radius `r ≤ p_u n_o` (there the one-sided ratio `Γ̃(r)` is at most `2e^u n_o`, not `O(1)`; the factor `J`
   alone is of this order only when `θ ≳ e^u/u`);
4. Chernoff factors `1 ± η` instead of `2^{±1}`, a ladder ratio `e^λ` instead of `e`, and a reference bound that makes `s₀`
   exponentially small against `ℓ`.

The resulting bracket has ratio at most `e^b (e^λ(1+η)/(1−η) + η′ + θ) + (2p_u)^n`, where `b` is the accuracy of the inner
brackets and `λ, η, η′, θ` are free constants: **one level adds an arbitrarily small constant to the accuracy** (step (4)
of the sketch is too pessimistic), which is why the strong form holds.  The cost is governed by the same count as in
Theorem 11.52 (the two factors `e^b` cancel), and the exponent of the new level at a bounded accuracy is the natural
continuation of (11.18.2) to `g = β = 0`:

    R[T](0)  =  inf_{0<φ<1}  sup_{γ ≥ 0} [ min(γ, φ·a) + (1 − φ)·T(γ/(1 − φ)) ],        T(0) := the exponent at bounded accuracy

(Theorem K2 — step (3) of the sketch, correct).  For the limit only a two-rung ladder is needed:
`T′(0) ≤ max{ φa + (1−φ)T(ξ), (1−φ)(ξ + T(0)) }`; with `T(ξ) ≤ h + η` at one small extensive rate `ξ` — Proposition E,
§3.3: the extensive levels assembled from Theorem K1 and Theorem 11.53, without left limits — this contracts to `h`
(machine-checked as an abstract statement and for the exponent functions of the cube: `KBounded.lean`,
`KBoundedLink.lean`, `KBoundedCube.lean`).

**Verdicts on the five steps of the sketch** (details in §5): (1) correct; (2) wrong as a mechanism — with the layer-cake
lower end alone the closure test can succeed only for `G − b ≥ ln(16e^u(e^u−1))` and then only at radii below
`ρ₊(G−b)·n_o` with `ρ₊ < p_u`, populated levels never sit there (sketch and numerics), and the outer sample would get
the exponent `φ·KL(ρ₊‖½) > φa` — repaired by changes 2 and 3; (3) correct; (4) correct but too pessimistic (the loss per level can
be made arbitrarily small); (5) the conclusion is right, the reason given is not: the one-sided ratio `Γ(r) = E_r/|B(r−1)|`
is **not** bounded up to `p_u n` (it is `≈ c√n` there and never below `4e^u(e^u−1)`); the base bracket has a bounded ratio
at exponent `a` because of the *two-sided* lemma 11.43(c) (Proposition K0).

**Numerical checks** (§6): (i) the recursion with the point `g = 0` (`τ_k/a = 0.5006, 0.361, 0.311, 0.290, 0.280, …, 0.2631`
for `k = 2, 3, 4, 5, 6, …, 40` at `u = 1`, against `h/a = 0.2627`; never below `h`; rigorous one-sided evaluation
`τ_40 ≤ 1.027 h`); (ii) the outer loop of the new algorithm with a simulated adversarial inner oracle and the constants
of the theorem: 394 runs, every inequality of the proof checked on every run, no violation, five mutations all
detected; the same at medium size in the bounded regime (radial outer landscapes, `n_o ≤ 600`, exact samples of up to
`4.6·10^{18}` outer points, 1325 runs, 864 levels left as negligible, no violation: §6.8); and — not asked for — the
complete two-level algorithm with *real* inner two-sample brackets on cubes `Q_12`–`Q_14`, no invalid bracket (§6.5); (iii) the closure window and the two ratios `Γ̃`, `Γ″` for `n ≤ 10⁵`; (iv) the
exact cost of the algorithm at the flat instance for `n ≤ 64 000`, never below the hinted lower bound, and the outer
loop in expectation on 17 radial and 5 additive outer landscapes up to `n_o = 16 000` (§6.4, §6.6).

**Lower bounds above `h`:** there are none at the exponential scale, at any fixed accuracy — that is the theorem.  What
is left open is below the exponential scale (§7).

---

## 1. Inputs

### 1.1 Known facts used

* **(H) Harper's vertex-isoperimetric theorem [known].**  If `S ⊆ Q_m` and `|S| ≥ |B(m,k)|`, then the closed neighbourhood
  `N(S)` has `|N(S)| ≥ |B(m,k+1)|` (Harper 1966; in this form e.g. Frankl–Füredi 1981; quoted from memory, as in the
  theory report).
* **(C) Chernoff bounds [known].**  For `X ~ Bin(M, p)`, `μ = Mp`, `0 < η ≤ 1`: `P(X ≤ (1−η)μ) ≤ e^{−η²μ/2}`,
  `P(X ≥ (1+η)μ) ≤ e^{−η²μ/3}`; and `P(X ≥ t)` is nondecreasing in `p`.
* **(Ho) Hoeffding [known].**  `P(Bin(m,p) ≤ mp − t) ≤ e^{−2t²/m}`.
* **(Me) Median of the binomial law [known]** (Kaas–Buhrman 1980, from memory): `P(Bin(m,p) ≥ k) ≥ ½` for every integer
  `k ≤ mp`.
* **(LB) Theorem 11.25(a) [known; machine-checked in the repository].**  An `(ε/2, δ)`-correct algorithm makes at least
  `(1 − 2δ)·2ⁿ/|B(n, k*(ε))|` evaluations in expectation at the zero function, `k*(ε)` the least `k` with
  `2^{−n}E_k(n) > e^ε − 1`; for fixed `ε` (indeed for `ε_n = o(n)`, `ln(1/ε_n) = o(n)`) the exponent is `h` (Theorem 11.25(d)).
* **(R) Theorem 11.53: the exact recursion converges [known; machine-checked: the repository's
  `cube_iterates_lt_hint_add` (commit `4cef47e`) together with `exactRec_reaches_hint` of `KExactRecursion.lean` here].**
  Let `T₁ := θ_na` and `T_{k+1}(g) := min(T_k(g), R[T_k](g))` on `(0,∞)`,
  `R[T](g) := inf_{0<φ<1, 0<β<g} sup_{γ≥β}[min(γ, φθ_na((g−β)/φ)) + (1−φ)T(γ/(1−φ))]` (11.18.2).  Then for every
  `g ∈ (0, ε*)` and `η > 0` there is `k` with `T_k(g) < θ_hint(g) + η`.  (The repository's theorem is about any sequence
  with the step inequality, `T_{k+1} ≤ T_k`, `T_k` nonincreasing, nonnegative, `T₁` bounded.  `KExactRecursion.lean` defines
  this very sequence — the infimum of the suprema as the infimum of all upper bounds — and proves those hypotheses:
  `R[T]` is nonincreasing in `g` because every `(φ, β)` admissible for `g` is admissible for `g′ ≥ g` with a smaller
  bracket.  So no hypothesis about the sequence is left.)
* **(E) Extensive accuracies [proved in §3.3, Proposition E, from Theorem K1 and (R); the statement is that of
  Theorem 11.54 of the theory report].**  For every `ξ ∈ (0, ε*)` and `η > 0` there is a family of bracket procedures
  (definition below) whose exponent function satisfies `T(ξ) ≤ h + η`.  The assembly of the families over the levels is
  done in §3.3 without left limits (it asks for less than Theorem 11.54: an accuracy rate `g′ > g` at the exponent
  `T_k(g) + ζ`), so the induction of referee report R7, §5, is not an input of this report.

### 1.2 The two tail lemmas (Lemma 11.43(b),(c)) [known; proofs repeated because everything rests on them]

**Lemma K.1.**  Let `W : Q_m → (0,∞)` with `−ln W ∈ L_u(Q_m)` and `t > 0`.
(a) If `D = {W > t}` has `|D| ≤ |B(m,r)|` for some `r ≤ m − 1`, then `2^{−m} Σ_x (W(x) − t)₊ ≤ t·2^{−m}·E_r(m)`.
(b) If `S = {W ≥ t}` is nonempty and `|S| ≥ |B(m,k)|`, `k ≥ 0`, then `2^{−m} Σ_x min(W(x), t) ≥ t·2^{−m}·T_m(k)`.

*Proof.*  (a) If `D = ∅` there is nothing to prove; `D ≠ Q_m` because `|B(m,r)| < 2^m`.  For `x ∈ D` let `y ∉ D` be a nearest
point: `W(x) ≤ W(y)e^{u·d(x,y)} ≤ t·e^{u·dist(x,Dᶜ)}`.  With `D_i = {x : dist(x, Dᶜ) ≥ i}` (`D₁ = D`),
`Σ_{x∈D}(e^{u·dist(x,Dᶜ)} − 1) = Σ_{i≥1}(e^{ui} − e^{u(i−1)})|D_i|`.  `D_i` is the complement of the `(i−1)`-fold neighbourhood of
`Dᶜ`, and `|Dᶜ| ≥ 2^m − |B(m,r)| = |B(m, m−r−1)|`, so by (H) `|D_i| ≤ 2^m − |B(m, m−r+i−2)| = |B(m, r+1−i)|`, and
`Σ_{i≥1}(e^{ui} − e^{u(i−1)})|B(m, r+1−i)| = Σ_{j≤r} C(m,j)(e^{u(r+1−j)} − 1) = E_r(m)`.
(b) For every `x`, `min(W(x), t) ≥ t·e^{−u·dist(x,S)}` (for `x ∉ S` take a nearest `y ∈ S`).  `Σ_x e^{−u·dist(x,S)} =
Σ_{i≥0}(e^{−ui} − e^{−u(i+1)})|N^i(S)|` is nondecreasing in every `|N^i(S)|`, and `|N^i(S)| ≥ |B(m, k+i)|` by (H); for the ball the
sum is `T_m(k)`.  ∎

**Lemma K.2 (fibres) [known: facts (F1), (F2) of Theorem 11.52].**  For `ψ ∈ L_u(Q_n)` and `Q_n = Q_{n_o} × Q_{n_i}`: every fibre
`b ↦ ψ(a,b)` is in `L_u(Q_{n_i})`, and the fibre average `W(a) = 2^{−n_i} Σ_b e^{−ψ(a,b)}` has `−ln W ∈ L_u(Q_{n_o})`
(`W(a) ≤ e^{u·d(a,a′)} W(a′)` term by term).  `A = E_a W(a)`; write `p(s) = P_a(W(a) > s)`.

### 1.3 Bracket procedures and exponent functions

As in §11.18 (revised): a *bracket procedure* for dimension `d` with accuracy `x`, failure probability `δ′` and cost `C`
makes at most `C` queries to any `ψ ∈ L_u(Q_d)` — always — and returns `L ≤ U` with `L ≤ A(ψ) ≤ U` and `U ≤ e^x L` except
with probability `δ′`.  A *family* has one procedure for every `d ≥ 1`, `x > 0`, `0 < δ′ < 1`, with cost `C(d,x,δ′)`
nonincreasing in `x` and in `δ′`.  (Monotonicity is free: a procedure for `(x′, δ″)` with `x′ ≤ x`, `δ″ ≤ δ′` is one for
`(x, δ′)`; replace `C` by its monotone hull.)  We extend the exponent function to accuracy zero: a nonincreasing
`T : [0,∞) → [0,∞)` is an **exponent function** of the family if for every `c > 0`

    (E1)  limsup_d d^{−1} ln C(d, ξd, e^{−cd}) ≤ T(ξ)   for every ξ > 0,
    (E0)  limsup_d d^{−1} ln C(d, x,  e^{−cd}) ≤ T(0)   for every fixed x > 0.

`T(0)` is the exponent at *every* bounded accuracy.  A uniform version, used for accuracies that tend to zero:

    (E0′) limsup_d d^{−1} ln C(d, x_d, e^{−cd}) ≤ T(0)   for every sequence 0 < x_d ≤ 1 with ln(1/x_d) = o(d).

(E0′) contains (E0) (constant sequences; the cost is nonincreasing in `x`).  Enumerating the cube (`2^d` queries,
exact) is always available; the midpoint `½(ln L + ln U)` of a bracket of accuracy `ε` is an `(ε/2, δ′)`-correct output.

---

## 2. One more level, with explicit constants (Theorem K1)

### 2.1 Tables on the outer cube

Fix `u > 0`, the outer dimension `m = n_o ≥ 1`, and `0 < η ≤ ½`; put `c_η = (1−η)/(1+η)`.  For `0 ≤ r ≤ m`:

    Γ̃(0) = e^u − 1,     Γ̃(r) = E_r(m)/|B(m, r−1)|   (r ≥ 1)                — the one-sided ratio of Theorem 11.52;
    κ(r)  = the largest k ≥ 0 with |B(m,k)| ≤ max{1, c_η·|B(m, r−1)|};
    Γ″(r) = E_r(m)/T_m(κ(r))                                                 — the two-sided ratio.

For `θ > 0`, `ν₀ ≥ 1` let `r†` be the largest `r ∈ {0,…,m−1}` such that for every `0 ≤ r′ ≤ r`

    [N]  Γ̃(r′) ≤ θ(1−η)ν₀        and        [P]  min{ Γ̃(r′)/c_η , Γ″(r′) } ≤ θ ,

`r† = −1` if this fails at `r′ = 0`; and `π† = |B(m, r†)|/2^m` (`π† = 2^{−m−1}` if `r† = −1`).

### 2.2 Algorithm 2L⁺

*Parameters:* `n ≥ 2`, `1 ≤ n_o ≤ n−1`, `n_i = n − n_o`; `0 < λ ≤ 1` (ladder ratio `e^λ`), `0 < η ≤ ½` (Chernoff), `0 < η′ ≤ 1`
(share of the negligible levels), `θ > 0` (share of the tail), `ν₁ ≥ 1`, tolerance `b > 0`, failure probability `δ`; inner
accuracies `x₀ := 2u·n_i > x₁ > … > x_L`, `L ≥ 1`, `x_L ≤ b`; inner bracket procedures `I_1, …, I_L` for dimension `n_i`, `I_l` with
accuracy `x_l`, failure probability `δ′` and cost `C_l`.

*Constants* (all computable from the parameters):

    J     = ⌈(2un + b + n_o ln 2)/λ⌉                     ν₀ = (1−η)^{−1}·max{ (J+1)(e^λ − 1)/η′ , ν₁ }
    m_max = ⌈log₂( 2(1+η)e^λ ν₀ / ((1−η)π†) )⌉           K  = ⌈ 3(1+η)η^{−2} · ln( 2(J+1)(m_max+1)(L+2)/δ ) ⌉
    ν     = K·ν₀        M† = K/((1−η)π†)        M̄ = 2(1+η)e^λ ν₀ M†        δ′ = δ/(4L·M̄)
    cnt(x) = max{ K , 2(1+η)²(1−η)^{−1} e^λ ν e^x }        C_max = 1 + 2M̄ + Σ_{l=1}^{L} min{ 2M̄ , (J+1)·cnt(x_{l−1}) }·C_l .

*The algorithm.*
0. One query at the reference point: `ψ₀ = ψ(0ⁿ)`.  Levels `s_j = s₀e^{jλ}`, `s₀ = e^{−ψ₀−un}` (so `s₀ ≤ W ≤ s₀e^{2un}`).
   Running lower bound `ℓ := e^{−ψ₀}((1+e^{−u})/2)^n`; `Σ := 0`.
1. Outer points `a₁, a₂, …` independent uniform in `Q_{n_o}`, drawn when first needed.  A new point gets the trivial
   bracket `[e^{−ψ(a,0)−un_i}, e^{−ψ(a,0)+un_i}]` (one query; ratio `e^{x₀}`) and rung `0`.  Brackets are only ever refined:
   *to classify `a_i` at level `j`*, while `U_i > s_j` and `L_i ≤ s_je^{−b}` move `a_i` to the next rung `l`, call `I_l` on its fibre
   and intersect; then `a_i` is **low** if `U_i ≤ s_j` and **high** otherwise (then `L_i > s_je^{−b}`).
2. For `j = 0, 1, …, J`:  `M := K`;  repeat
   (a) classify `a₁,…,a_M` at level `j`; `N := #high`; `q := min{1, max(N,K)/((1−η)M)}`;
   (b) if `N ≥ K` (*populated*): `p̲ := N/((1+η)M)`, `k :=` the largest `k ≥ 0` with `|B(n_o,k)| ≤ max{1, 2^{n_o}p̲}`,
       `ℓ := max{ ℓ , s_je^{−b}p̲ , s_je^{−b}·2^{−n_o}T_{n_o}(k) }`;
   (c) *closure test:* `tail := 0` if `2^{n_o}q < 1`; otherwise let `r` be the least radius with `|B(n_o,r)| ≥ 2^{n_o}q` and
       `tail := s_j·2^{−n_o}E_r(n_o)` if `r ≤ n_o − 1`, `tail := +∞` if `r = n_o`.  If `tail ≤ θe^bℓ`: **stop** and return

           L = max{ ℓ , Σ + [N ≥ K]·(1−e^{−λ})e^{−b}s_jp̲ },        U = s₀ + Σ_{i<j}(s_{i+1} − s_i)·q_i + tail;

   (d) else if `N ≥ K`: `q_j := q`, `p̲_j := p̲`, `Σ := Σ + (1−e^{−λ})e^{−b}s_jp̲`, next level;
   (e) else if `M ≥ M_j^neg := ν·s_j/(ℓe^b)` (*negligible*): `q_j := q`, next level;
   (f) else `M := 2M`.
3. *Abort* (return the trivial bracket `[s₀, s₀e^{2un}]`) if a point is still unclassified at rung `L`, if `M` would
   exceed `K·2^{m_max}`, if level `J` is left, or if the number of queries exceeds `C_max`.

In (e) `ℓ` is the value at the entry of level `j` (it changes within a level only at a pass with `N ≥ K`, which ends
the level).  Differences from Theorem 11.52: the lower end (the sum `Σ`, the third term in (b), the initial value of
`ℓ`), the factors `1 ± η` and `e^λ`, and `ν₁` in the negligibility threshold; with `λ = 1`, `η = ½`, `ν₁ = 1`, `η′ = 1`, without
`Σ` and without the third term of (b) it is that algorithm up to constants.

### 2.3 Statement

**Theorem K1 [proved; deterministic core machine-checked (`KBounded.lean`); every step checked in simulation (§6.2)].**
With the parameters and constants of §2.2, and inner procedures `I_l` of accuracy `x_l`, failure probability at most
`δ′` and cost `C_l`, Algorithm 2L⁺ is a bracket procedure for dimension `n` with

    accuracy   x_out = ln[ (2p_u)^n + e^b·( e^λ(1+η)/(1−η) + η′ + θ ) ],      failure probability δ,      cost C_max.

More precisely there is an event `𝒢` of probability at least `1 − δ` on which, for every `ψ ∈ L_u(Q_n)`:
(i) no abort occurs and the algorithm stops at a level `j ≤ J`;
(ii) `L ≤ A ≤ U`, and every certificate is true: `p(s_i) ≤ q_i` at every level, `p(s_ie^{−b}) ≥ p̲_i` at every populated one,
     `ℓ ≤ A` throughout;
(iii) every level that is left without stopping has closing radius `r(q_j) > r†`, i.e. `q_j > π†`;
(iv) every sample size satisfies `M ≤ max{K, 2M_j^neg}` and `M_j^neg ≤ (1+η)e^λν₀M†`, hence `M ≤ M̄`;
(v) for every level `j` that is reached and every `x > 0`:  `M_j^neg·p(s_je^{−x}) ≤ (1+η)(1−η)^{−1}e^λ·ν·e^x`
    (**the count**; the two factors `e^b` cancel), and for `x ∈ {x₀,…,x_{L−1}}` at most `cnt(x)` of the points used at level `j`
    have `W > s_je^{−x}`;
(vi) at most `min{M̄, cnt(x_{l−1})}` calls of `I_l` are made during one level, so the number of queries is at most
     `1 + M̄ + Σ_l min{M̄, (J+1)cnt(x_{l−1})}·C_l ≤ C_max`.
The inequality `U ≤ e^{x_out}L` holds whenever the algorithm stops through the closure test, on or off `𝒢`.

The whole dependence on the instance class is in (iii): everything is polynomial in `n` except `1/π†`, the size of the
outer sample, and `e^{x_{l−1}}·C_l`, the price of the points within a factor `e^{x_{l−1}}` of a level.

### 2.4 Proof

Write `X_t(M) = #{i ≤ M : W(a_i) > t} ~ Bin(M, p(t))` and `ℳ = {K2^m : 0 ≤ m ≤ m_max}`.

**The good event.**  `𝒢 = (V1) ∩ (V2) ∩ (V3)`:
(V1) every *potential* inner call — a pair `(i, l)`, `i ≤ K2^{m_max}`, `1 ≤ l ≤ L`, each with its own randomness drawn in
     advance — returns a valid bracket of ratio at most `e^{x_l}`;
(V2) for all `0 ≤ j ≤ J`, `M ∈ ℳ`:  `M·p(s_j) ≤ K/(1−η)`  or  `X_{s_j}(M) ≥ (1−η)M·p(s_j)`;
(V3) for all `0 ≤ j ≤ J`, `M ∈ ℳ` and `t ∈ {s_je^{−b}} ∪ {s_je^{−x_l} : 0 ≤ l ≤ L−1}`:  `X_t(M) < K`  or  `X_t(M) ≤ (1+η)M·p(t)`.
The levels are functions of `ψ₀` alone and the list `a₁, a₂, …` is not influenced by inner results, so (V2), (V3) are
statements about binomial variables at fixed thresholds.  (V2): if `μ = Mp > K/(1−η)` then
`P(X < (1−η)μ) ≤ e^{−η²μ/2} ≤ e^{−η²K/2}`.  (V3): if `μ ≥ K/(1+η)`, `P(X > (1+η)μ) ≤ e^{−η²μ/3} ≤ e^{−η²K/(3(1+η))}`; if
`μ < K/(1+η)`, by monotonicity in `p`, `P(X ≥ K) ≤ P(Bin(M, K/((1+η)M)) ≥ K) ≤ e^{−η²K/(3(1+η))}`.  There are
`(J+1)(m_max+1)(L+2)` events; by the choice of `K` their total probability is at most `δ/2`.  (V1) fails with
probability at most `L·K2^{m_max}·δ′ < 2L·M̄·δ′ = δ/2` (`K2^{m_max} < 2M̄` by the definition of `m_max`).  So `P(𝒢) ≥ 1 − δ`.
From here on `𝒢` is assumed; the abort rule guarantees that only sizes `M ∈ ℳ` occur, and Step 6 shows that the rule
is never used.

**Step 1 (classification).**  A point at rung `L` has a bracket of ratio `≤ e^{x_L} ≤ e^b`; if `U > s_j` then
`L ≥ Ue^{−x_L} > s_je^{−b}`: classification ends at rung `L` at the latest (no abort of the first kind).  A point with
`W > s_j` is never low (`U ≥ W`), and a high point has `W ≥ L > s_je^{−b}`.  Hence at every pass

    X_{s_j}(M)  ≤  N  ≤  X_{s_je^{−b}}(M).                                                              (2.1)

**Step 2 (certificates).**  *`p(s_j) ≤ q`:* if `Mp(s_j) ≤ K/(1−η)` then `p(s_j) ≤ K/((1−η)M) ≤ q` (or `q = 1`); otherwise (V2)
and (2.1) give `N ≥ (1−η)Mp(s_j)`.  *If `N ≥ K` then `p(s_je^{−b}) ≥ p̲`:* by (2.1) `X_{s_je^{−b}}(M) ≥ N ≥ K`, so (V3) gives
`N ≤ (1+η)M·p(s_je^{−b})`.  *`ℓ ≤ A`:* initially because `w(x) ≥ e^{−ψ₀−u|x|}`, so `A ≥ e^{−ψ₀}·2^{−n}Σ_j C(n,j)e^{−uj}`; the update
`s_je^{−b}p̲ ≤ t·p(t) ≤ A` (`t = s_je^{−b}`, Markov); and for the third term, `S = {W ≥ t} ⊇ {W > t}` is nonempty with
`|S| ≥ 2^{n_o}p(t) ≥ 2^{n_o}p̲`, so `|S| ≥ |B(n_o,k)|` and Lemma K.1(b) gives `A ≥ E min(W,t) ≥ t·2^{−n_o}T_{n_o}(k)`.

**Step 3 (validity).**  `A = ∫₀^∞ p(s)ds`.  *Upper end:* `∫₀^{s₀}p ≤ s₀`; `∫_{s_i}^{s_{i+1}}p ≤ (s_{i+1} − s_i)p(s_i) ≤ (s_{i+1} − s_i)q_i`;
`∫_{s_j}^∞ p = E(W − s_j)₊ ≤ tail`: if `2^{n_o}q < 1` then `p(s_j) ≤ q` forces `{W > s_j} = ∅`; otherwise
`|{W > s_j}| ≤ 2^{n_o}q ≤ |B(n_o,r)|` with `r ≤ n_o − 1`, and Lemma K.1(a) applies to `W` (Lemma K.2).  *Lower end:* with
`t_i := s_ie^{−b}` (`t_{−1} := s₀e^{−λ−b}`) the intervals `(t_{i−1}, t_i]` are disjoint and `p` is nonincreasing, so for the set `P`
of populated levels

    A ≥ Σ_{i∈P} (t_i − t_{i−1})·p(t_i) ≥ Σ_{i∈P} (1 − e^{−λ})e^{−b}s_i·p̲_i                                   (2.2)

(`certified_lower_sum_le_mean`), which is `Σ` (with the current level, if it is populated).  With `ℓ ≤ A`: `L ≤ A ≤ U`.

**Step 4 (width; no probability involved).**  Let the algorithm stop at level `j`.
* `s₀ = (2p_u)^n·e^{−ψ₀}((1+e^{−u})/2)^n ≤ (2p_u)^n·L`.
* Populated levels `i < j`: `q_i ≤ N_i/((1−η)M_i) = p̲_i/c_η`, so with `e^λ − 1 = e^{λ+b}(1−e^{−λ})e^{−b}`:
  `Σ_{i∈P}(s_{i+1} − s_i)q_i = (e^λ − 1)Σ_{i∈P} s_iq_i ≤ c_η^{−1}e^{λ+b}·Σ ≤ c_η^{−1}e^{λ+b}·L` (`populated_part_le`).
* Negligible levels `i < j`: `q_i ≤ K/((1−η)M_i)` and `M_i ≥ ν s_i/(ℓ_ie^b)` (`ℓ_i` the value at that time, `≤` the final `ℓ`),
  so `(s_{i+1} − s_i)q_i ≤ (e^λ − 1)e^bℓ/((1−η)ν₀) ≤ η′e^bℓ/(J+1)`; there are at most `J+1` levels: together `≤ η′e^bL`.
* `tail ≤ θe^bℓ ≤ θe^bL`.
So `U ≤ [(2p_u)^n + e^b(e^λ/c_η + η′ + θ)]·L` (`width_le`).

**Step 5 (closing radius — claim (iii)).**  Let level `j` be left at a pass with `(M, N, q)`, so the test failed:
`2^{n_o}q ≥ 1` and `tail > θe^bℓ`.  If `r = n_o` then `r > r†` trivially; let `r ≤ n_o − 1`.  By the minimality of `r`,
`2^{n_o}q > |B(n_o, r−1)|` for `r ≥ 1`, and `2^{n_o}q = 1` for `r = 0`; in both cases

    tail = s_j·2^{−n_o}E_r(n_o) ≤ s_j·q·Γ̃(r).                                                              (2.3)

*Negligible:* `q ≤ K/((1−η)M)` and `M ≥ ν s_j/(ℓe^b)`, so `s_jq ≤ e^bℓ/((1−η)ν₀)` and `tail ≤ e^bℓ·Γ̃(r)/((1−η)ν₀)`; the test
failed, so `Γ̃(r) > θ(1−η)ν₀`: [N] fails at `r`.  *Populated:* `q < 1` (as `r < n_o`), so `q = p̲/c_η` and, by step (b),
`ℓ ≥ s_je^{−b}p̲`, whence `tail ≤ (Γ̃(r)/c_η)·e^bℓ`; moreover `max{1, 2^{n_o}p̲} ≥ max{1, c_η|B(n_o, r−1)|}`, so the radius `k` of
step (b) is at least `κ(r)`, `T_{n_o}(k) ≥ T_{n_o}(κ(r))` (`T` is nondecreasing in `k`), and `ℓ ≥ s_je^{−b}2^{−n_o}T_{n_o}(κ(r))` gives
`tail ≤ Γ″(r)·e^bℓ`.  The test failed, so `min{Γ̃(r)/c_η, Γ″(r)} > θ`: [P] fails at `r`.  In either case `r > r†` by the
definition of `r†`, i.e. `2^{n_o}q > |B(n_o, r†)|` (for `r† = −1`: `2^{n_o}q ≥ 1 > ½`).  So `q_j > π†`.

**Step 6 (sample sizes — claim (iv)).**  `M` is doubled only while `M < M_j^neg`, so the last size of level `j` is `K` or
less than `2M_j^neg`.  A negligible level that is left has `π† < q_j ≤ K/((1−η)M_j)`, i.e. `M_j < M†`.  Bound on `M_j^neg`,
with `ℓ_j` the value of `ℓ` at the entry of level `j`: `M₀^neg = ν s₀/(ℓ₀e^b) ≤ ν(2p_u)^n < ν ≤ ν₀M†` (as `M† ≥ K`).  For
`j ≥ 1`: if level `j−1` was negligible, `M_j^neg ≤ e^λM_{j−1}^neg ≤ e^λM_{j−1} < e^λM†` (`ℓ` is nondecreasing); if it was
populated, `ℓ_j ≥ s_{j−1}e^{−b}p̲_{j−1} ≥ c_η s_{j−1}e^{−b}q_{j−1}` and `q_{j−1} > π†`, so
`M_j^neg = νe^λs_{j−1}/(ℓ_je^b) < νe^λ/(c_ηπ†) = (1+η)e^λν₀M†`.  Hence `M_j^neg ≤ (1+η)e^λν₀M†` and every size is at most
`M̄ = 2(1+η)e^λν₀M† ≤ K2^{m_max}`: no abort of the second kind.

**Step 7 (the count — claim (v)).**  Let level `j` be reached and `x > 0`.  If `s_je^{−x} < s₀`:
`M_j^neg·p ≤ ν s_j/(ℓ_je^b) ≤ ν s_j/s₀ < νe^x` (`ℓ_j ≥ s₀`).  Otherwise let `i` be the largest index with `s_i ≤ s_je^{−x}`; then
`i < j` and `s_i > s_je^{−x−λ}`.  Level `i` was left as populated — then `s_iq_i ≤ s_ip̲_i/c_η ≤ e^bℓ_j/c_η` by the update of `ℓ` —
or as negligible — then `s_iq_i ≤ e^bℓ_j/((1−η)ν₀) ≤ e^bℓ_j`.  So

    M_j^neg·p(s_je^{−x}) ≤ (ν s_j/(ℓ_je^b))·q_i ≤ (ν s_j/(ℓ_je^b))·(e^bℓ_j/(c_η s_i)) < c_η^{−1}e^λ·ν·e^x

(`close_points_bound'`): the tolerance of "high" and the tolerance of "negligible" are the same `b`, and they
cancel; any valid `ℓ` may be used, because it enters the threshold and the certificates in the same way.  For
`x ∈ {x₀,…,x_{L−1}}` and the last size `M_j` of the level (all points classified during level `j` are among the first
`M_j`): if `M_j = K` the number of them with `W > s_je^{−x}` is at most `K`; otherwise `M_j < 2M_j^neg` (Step 6) and (V3)
gives `X_{s_je^{−x}}(M_j) ≤ max{K−1, (1+η)M_jp} ≤ max{K, 2(1+η)M_j^neg p}`.  In both cases the number is at most `cnt(x)`.

**Step 8 (cost — claim (vi)).**  A call of `I_l` for `a_i` during level `j` is made only if `a_i` is unclassified at level `j`
at rung `l−1`: `U_i > s_j` and `U_i ≤ e^{x_{l−1}}L_i ≤ e^{x_{l−1}}W(a_i)`, so `W(a_i) > s_je^{−x_{l−1}}`.  With Step 7 at most
`min{M_j, cnt(x_{l−1})}` such calls occur at level `j`; each point is called at most once per rung in the whole run, and
there are at most `J+1` levels.  Adding the reference query and one query per sampled point gives (vi).

**Step 9 (termination — claim (i)).**  On `𝒢`, `ℓ ≤ A < s₀e^{2un}` (the reference point itself has weight `s₀e^{un}`).  At
level `J`: `s_Je^{−b} ≥ s₀e^{2un}·2^{n_o} ≥ max W`, so nothing is high, and
`M_J^neg = ν s_J/(ℓe^b) > ν s_J/(s₀e^{2un+b}) ≥ ν2^{n_o} ≥ K2^{n_o}/(1−η)` (`ν₀ ≥ ν₁/(1−η) ≥ 1/(1−η)`).  A pass with `M ≥ M_J^neg` has
`q = K/((1−η)M) < 2^{−n_o}`, so its tail is zero and the test (c) stops the algorithm before (e) is reached; the
passes with `M < M_J^neg` stop or double, and the doubling stays below `M̄` by Step 6.  So the algorithm stops at a
level `≤ J`, and by Steps 1, 6, 8 no abort occurs.  Off `𝒢` the abort rule keeps the cost below `C_max`.  ∎

### 2.5 What each change is for

| change | needed for | without it |
|---|---|---|
| sum `Σ` in the lower end | populated part of the width `O(1)` | a factor `J = O(n)` in the ratio (mutation `maxform`: 18 of 143 runs violate the width bound) |
| `ℓ` starts at `e^{−ψ₀}((1+e^{−u})/2)^n` | `s₀ ≤ (2p_u)^n L` | `s₀ ≤ ℓ` only: an additive `1` in the ratio |
| Harper term in (b) | closure at populated levels at every `r ≤ r₊` (Lemma K.4) | populated levels are left with `r ≤ r†` (mutation `noharper`) and the run closes only at a later, larger sample |
| `ν₁` in `ν₀` | closure at unpopulated levels at every `r ≤ p_un_o`, where `Γ̃ ≤ 2e^un_o` | closure needs `Γ̃(r) ≤ θ(J+1)(e^λ−1)/η′`: a window of radii |
| `1 ± η`, `e^λ` | loss per level `λ + ln((1+η)/(1−η)) + ln(1 + η′ + θ)` | `≈ 1 + ln 4` per level |
| the same `b` in "high" and in `M^neg` (as in Theorem 11.52) | the count (v) | mutation `neg_tol`: the count is violated |

---

## 3. Exponents

### 3.1 The closing radius at a bounded accuracy

**Lemma K.4 [proved; all four inequalities checked on tables for `m ≤ 12 800`, §6.3].**  Let `m ≥ 1`, `0 < η ≤ ½`,
`c_η = (1−η)/(1+η)`, `m₀ := ⌈u^{−1} ln(1/c_η)⌉`, and `Γ̃, κ, Γ″, r†, π†` as in §2.1 on `Q_m`.
(a) `Γ̃(r) ≤ 2e^u·m` for `0 ≤ r ≤ p_u(m+1)`.
(b) `κ(r) ≥ r − 1 − m₀` for `1 ≤ r ≤ p_u(m+1) + 1`, and for `0 ≤ r ≤ p_u m`

        Γ″(r) ≤ 2e^{u(m₀+2)}·P(Bin(m, p_u) ≤ r) ≤ 2e^{u(m₀+2)}·exp(−2(p_u m − r)²/m).

(c) If `0 < θ ≤ 2e^{u(m₀+2)}` and `ν₀ ≥ 2e^u m/(θ(1−η))`, then `r† ≥ r₊ := ⌊p_u m − √((m/2)·ln(2e^{u(m₀+2)}/θ))⌋`, provided `r₊ ≥ 0`.
(d) If moreover `r₊ ≥ p_u m/2`:  `ln(1/π†) ≤ m·a + (u + ln 4)·(1 + √((m/2)·ln(2e^{u(m₀+2)}/θ))) + ln(m+1)`.

*Proof.*  The ratio `|B(m,i−1)|/|B(m,i)|` is at most `C(m,i−1)/C(m,i) = i/(m−i+1)` (compare term by term), which is `≤ e^{−u}` iff
`i ≤ p_u(m+1)`.  (a) `Γ̃(0) = e^u − 1`.  For `1 ≤ r ≤ p_u(m+1)` put `y = r/(m−r+1) ≤ e^{−u}`; `C(m, r−i) ≤ C(m,r)y^i`, so
`E_r ≤ Σ_{i=0}^{r} C(m,r−i)e^{u(i+1)} ≤ C(m,r)e^u Σ_{i≤r}(ye^u)^i ≤ (r+1)e^u C(m,r)`, and `|B(m,r−1)| ≥ C(m,r−1) = C(m,r)·r/(m−r+1)`;
hence `Γ̃(r) ≤ e^u(r+1)(m−r+1)/r ≤ 2e^u m`.
(b) For `1 ≤ r−1 ≤ p_u(m+1)` and `0 ≤ j ≤ r−1`: `|B(m, r−1−j)| ≤ e^{−uj}|B(m, r−1)|`; with `j = m₀` (if `m₀ ≤ r−1`) this is
`≤ c_η|B(m,r−1)|`, so `κ(r) ≥ r−1−m₀`; and `κ(r) ≥ 0` always.  Next, `C(m,j)e^{−uj} = (1+e^{−u})^m·P(Bin(m,p_u) = j)`, so
`E_r ≤ e^{u(r+1)}Σ_{j≤r}C(m,j)e^{−uj} = e^{u(r+1)}(1+e^{−u})^m P(Bin ≤ r)` and
`T_m(k) ≥ e^{uk}Σ_{j≥k}C(m,j)e^{−uj} = e^{uk}(1+e^{−u})^m P(Bin ≥ k)`.  For `r ≤ p_u m`: `k = κ(r) ≤ r ≤ p_u m`, so `P(Bin ≥ k) ≥ ½`
by (Me), and `r + 1 − κ(r) ≤ m₀ + 2`; the last inequality is (Ho).
(c) For `0 ≤ r′ ≤ r₊`: `p_u m − r′ ≥ √((m/2)ln(2e^{u(m₀+2)}/θ))`, so `Γ″(r′) ≤ θ` by (b): [P] holds; and `Γ̃(r′) ≤ 2e^u m ≤ θ(1−η)ν₀` by
(a): [N] holds; `r₊ ≤ m − 1`.
(d) `π† ≥ |B(m,r₊)|/2^m ≥ C(m,r₊)2^{−m} ≥ (m+1)^{−1}exp(−m·KL(ρ₊‖½))`, `ρ₊ = r₊/m ∈ [p_u/2, p_u]`; `KL(·‖½)` is convex with
derivative `−ln((1−ρ)/ρ)`, so `KL(ρ₊‖½) ≤ a + (p_u − ρ₊)ln((1−ρ₊)/ρ₊) ≤ a + (p_u − ρ₊)ln(2/p_u)`, and `ln(2/p_u) = ln(2(1+e^u)) ≤ u + ln 4`,
`m(p_u − ρ₊) ≤ 1 + √(…)`.  ∎

So at a bounded accuracy the outer sample of Theorem K1 has size `M̄ = poly(n)·e^{n_o a + O(√n_o)}`: the exponent `φa`.

### 3.2 The base family at a bounded accuracy (step (5) of the sketch)

**Proposition K0 [proved; coverage and width simulated, §6.5 part A].**  Let `ψ ∈ L_u(Q_d)`, `0 < η ≤ ½`, `K ≥ 1`,
`M ≥ K/(1−η)`, `q₊ = K/((1−η)M)`, and suppose `2^d q₊ < 1` or the least radius `r̂` with `|B(d,r̂)| ≥ 2^d q₊` is `≤ d − 1`.  Draw
two independent uniform samples of size `M`; let `t̂` be the `K`-th largest weight in the first and `Â` the mean of
`min(w, t̂)` over the second.  Then, outside an event of probability `4e^{−η²K/(3(1+η))}`,

    L := Â/(1+η)  ≤  A  ≤  U := Â/(1−η) + t̂·2^{−d}E_r̂(d),        U/L ≤ ((1+η)/(1−η))·(1 + Γ″_d(r̂))

(the tail term and `Γ″` are absent if `2^d q₊ < 1`).  Consequently the family "`η = min(½, tanh(x/4))`,
`K = ⌈3(1+η)η^{−2} ln(4/δ′)⌉`, `r*` the largest radius `≤ d−1` with `ln(1 + Γ″_d(r′)) ≤ x − ln((1+η)/(1−η))` for all `r′ ≤ r*`,
`M = ⌈K2^d/((1−η)|B(d,r*)|)⌉`; enumeration if no radius qualifies" has the exponent function `T₁(ξ) = θ_na(ξ)` for `ξ > 0`
(**[known]**: Theorem 11.44 / Proposition 11.46; here because `Γ″(r) ≤ (d+1)c_η^{−1}Γ̃(r) ≤ poly(d)·e^{d·KL((r−1)/d‖p_u)}`) and
**`T₁(0) = a`: cost `exp(d·a + O(√d))` at every fixed accuracy**.

*Proof.*  Three events.  (1) `P(w > t̂) ≤ q₊`: let `t⁺ = inf{s : P(w > s) ≤ q₊}`, so `P(w > t⁺) ≤ q₊ ≤ P(w ≥ t⁺)`; the number of
first-sample points with `w ≥ t⁺` is binomial with mean `≥ K/(1−η)`, hence `≥ K` except with probability `e^{−η²K/2}`, and
then `t̂ ≥ t⁺`.  (2) `P(w ≥ t̂) ≥ q₋ := K/((1+η)M)`: let `t⁻ = inf{s : P(w > s) ≤ q₋}`; the number of first-sample points with
`w > t⁻` is binomial with mean `≤ K/(1+η)`, hence `< K` except with probability `e^{−η²K/(3(1+η))}`, and then `t̂ ≤ t⁻`,
`P(w ≥ t̂) ≥ P(w ≥ t⁻) ≥ q₋`.  (3) Given the first sample, `min(w,t̂)/t̂ ∈ [0,1]` has `M`·mean `≥ Mq₋ = K/(1+η)`; the relative
error of `Â` exceeds `η` with probability `≤ 2e^{−η²K/(3(1+η))}`.  On the three events: `L ≤ E min(w,t̂) ≤ A`;
`A = E min(w,t̂) + E(w−t̂)₊ ≤ Â/(1−η) + t̂2^{−d}E_r̂` by Lemma K.1(a) (`|{w > t̂}| ≤ 2^d q₊ ≤ |B(d,r̂)|`); and by Lemma K.1(b) with
`S = {w ≥ t̂}`, `|S| ≥ max{1, 2^d q₋} ≥ |B(d, κ(r̂))|` (because `2^d q₋ = c_η2^d q₊ > c_η|B(d, r̂−1)|`),
`E min(w,t̂) ≥ t̂2^{−d}T_d(κ(r̂))`, so `t̂2^{−d}E_r̂ ≤ Γ″(r̂)·E min(w,t̂) ≤ Γ″(r̂)Â/(1−η)`.  Family: `ln((1+η)/(1−η)) ≤ x/2`, `r̂ ≤ r*`, so
the ratio is at most `e^x`; for fixed `x` and large `d`, Lemma K.4(b) gives `r* ≥ ⌊p_u d − √((d/2)ln(2e^{u(m₀+2)}/(e^{x/2}−1)))⌋`
and, as in K.4(d), `2M ≤ poly(d)·e^{d·a + O(√d)}` for `δ′ = e^{−cd}`.  *Extensive accuracies* `x = ξd`: `η = ½`, `K = O(d)`,
`Γ″(r) ≤ 3(d+1)Γ̃(r)` (`T_d(k) ≥ |B(d,k)|` and `|B(d,κ(r))| > c_η|B(d,r−1)|/(d+1)`), so by (3.0) below and Lemma K.4(a), exactly as in
the proof of Corollary K1.b, `r* ≥ min{d−1, ⌊ρ‡d⌋}` with `KL(ρ‡‖p_u) = ξ − O(log d/d)`, and `2M ≤ poly(d)·e^{d·θ_na(ξ) + o(d)}`:
`T₁ = θ_na` on `(0,∞)`.  *Uniformly in the accuracy* (E0′): for `x ≤ 1`,
`η = tanh(x/4) ≥ x/5`, `K = O(x^{−2}(1 + cd))`, `m₀ ≤ ⌈1/(2u)⌉`, `e^{x/2} − 1 ≥ x/2`, so
`2M ≤ poly(d, 1/x)·exp(d·a + (u + ln 4)(1 + √((d/2)ln(4e^{u(m₀+2)}/x))))`, which is `e^{da + o(d)}` whenever `ln(1/x_d) = o(d)`.  ∎

The reason given in the sketch — "ratio `≤ 3 + 12Γ(r)`, bounded for `r ≤ p_u n + O(√n)`" — is not right: `Γ(r) = E_r/|B(r−1)|`
is `≥ 4e^u(e^u−1)(1−o(1))` for every `r`, `≈ (e^u−1)n/r` for small `r` and `≈ c(u)√n` at `r = p_u n` (§6.3); with it the
bracket would have a bounded ratio only for `r ≤ (p_u − const)n`, i.e. at an exponent above `a`.  The two-sided ratio
`Γ″` is what is bounded — and small — up to `p_u n − O(√n)`.

### 3.3 Extensive accuracies: Theorem 11.52 again, and the assembly over the levels

**Corollary K1.b [proved].**  Let the inner family have the exponent function `T` (E1).  Fix `0 < φ < 1`, rates
`2u = ξ₀ > ξ₁ > … > ξ_L > 0` and `G > (1−φ)ξ_L`, and take in Theorem K1: `n_o = ⌊φn⌋`, `x_l = ξ_l n_i`, `b = x_L`, `λ = 1`, `η = ½`,
`η′ = 1`, `ν₁ = 1`, `δ = e^{−cn}` and `θ := e^{Gn−b} − (3e+1) − (2p_u)^n e^{−b}` (positive for large `n`; enumerate the cube for the
other `n`).  Then the procedure has accuracy exactly `Gn` and

    limsup_n n^{−1} ln C_max ≤ max{ μ , max_{1≤l≤L} [ min(μ, (1−φ)ξ_{l−1}) + (1−φ)T(ξ_l) ] },      μ = φ·θ_na((G − (1−φ)ξ_L)/φ).

With `G = g`, `ξ_L = β/(1−φ)` and a fine ladder the right-hand side is `sup_{γ≥β}[min(γ, μ) + (1−φ)T(γ/(1−φ))]` up to the
rounding of the ladder: (11.18.2), with accuracy exactly `gn` (Theorem 11.52: `gn + O(log n)`).
*Proof.*  Accuracy: `(2p_u)^n + e^b(3e + 1 + θ) = e^{Gn}` by the choice of `θ` (`e^λ(1+η)/(1−η) = 3e`, `η′ = 1`).  As
`(1−φ)n ≤ n_i < (1−φ)n + 1`, `Gn − b = (G − (1−φ)ξ_L)n − O(1) → ∞` and `ln θ = Gn − b − o(1)`.  For `r ≥ 1`,
`E_r(m) ≤ e^{u(r+1)}(1+e^{−u})^m` and `|B(m,r−1)| ≥ (m+1)^{−1}e^{m·H((r−1)/m)}` (`H` the entropy) give

    Γ̃(r) ≤ (m+1)e^{2u}·exp(m·KL((r−1)/m‖p_u))                      (uρ + ln(1+e^{−u}) − H(ρ) = KL(ρ‖p_u)).        (3.0)

[P] holds at `r′` as soon as `3Γ̃(r′) ≤ θ` (`c_η = ⅓`), and then [N] holds too (`(1−η)ν₀ ≥ 1`).  Put `m = n_o` and
`e_n := (ln θ − ln(3(n_o+1)e^{2u}))/n_o → e_∞ := (G − (1−φ)ξ_L)/φ > 0`; let `[ρ₋, ρ‡]` be the interval on which `KL(·‖p_u) ≤ e_n`
(`ρ₋ < p_u < ρ‡ ≤ 1`).  For large `n`, `3Γ̃(r′) ≤ θ` holds for `r′ = 0`, for every `r′ ≥ 1` with `(r′−1)/n_o ∈ [ρ₋, ρ‡]` by (3.0), and
for every `r′ ≥ 1` with `(r′−1)/n_o < ρ₋` by Lemma K.4(a) (then `r′ < ρ₋n_o + 1 ≤ p_u(n_o+1)` and `6e^u n_o ≤ θ`).  So
`r† ≥ min{n_o − 1, ⌊ρ‡n_o⌋}`.  If `ρ‡ ≥ ½` then `π† ≥ ½`; otherwise `π† ≥ C(n_o, ⌊ρ‡n_o⌋)2^{−n_o}` and
`ln(1/π†) ≤ n_o·KL(ρ‡‖½) + ln(n_o+1) + u + ln 4 = n_o·θ_na(e_n) + O(log n)`.  `θ_na` is continuous and `M̄ = poly(n)/π†`, so
`limsup n^{−1}ln M̄ ≤ φθ_na(e_∞) = μ`.  The rest is claim (vi) with `cnt(x) = poly(n)e^x`, `n_i/n → 1 − φ`,
`δ′ = δ/(4LM̄) ≥ e^{−c′n_i}` (`c′ = (c+1)/(1−φ)`) and the monotonicity of the inner cost in `δ′`.  ∎

**Proposition E (assembly over the levels) [proved, given (R)].**  Let `T_k` be the exact recursion of (R).
(a) For every `k ≥ 1`, `g > 0`, `g′ > g` and `ζ > 0` there is a family with an exponent function `T_F` (E1) such that
    `T_F(g′) ≤ T_k(g) + ζ`.
(b) Statement (E): for every `ξ ∈ (0, ε*)` and `η > 0` there is a family with `T_F(ξ) ≤ h + η`.

*Proof.*  (a) By induction on `k`.  `k = 1`: the base family has the exponent function `θ_na` on `(0,∞)` (Proposition K0),
and `θ_na(g′) ≤ θ_na(g)`.  `k → k+1`: if `T_{k+1}(g) = T_k(g)` use the hypothesis.  Otherwise `T_{k+1}(g) = R[T_k](g)`; choose
`φ ∈ (0,1)` and `β ∈ (0,g)` with

    S := sup_{γ≥β} [ min(γ, μ) + (1−φ)T_k(γ/(1−φ)) ] ≤ T_{k+1}(g) + ζ/4,        μ := φθ_na((g−β)/φ);

`S ≥ μ` (let `γ → ∞`; `T_k ≥ 0`).  Put `y_L := min(β/(1−φ), u)` and choose rates `y_L < y_{L−1} < … < y_1 < 2u` with
`y_{l−1} − y_l ≤ ζ/4` (`2 ≤ l ≤ L`) and `2u − y_1 ≤ ζ/4`; choose `0 < ι ≤ min(ζ/4, g′ − g)` with `y_1 + ι < 2u`, and put
`ξ_l := y_l + ι` (`1 ≤ l ≤ L`), `ξ₀ := 2u`.  By the induction hypothesis there are families `F_1, …, F_L` with
`T_{F_l}(ξ_l) ≤ T_k(y_l) + ζ/4`; their pointwise cheapest `F*` has an exponent function `T*` with `T*(ξ_l) ≤ T_k(y_l) + ζ/4`
for every `l`.  Apply Corollary K1.b to `F*` with this `φ`, the rates `ξ_l` and `G := g′`: it is applicable, since
`(1−φ)ξ_L ≤ β + (1−φ)ι < g′`, and since `G − (1−φ)ξ_L ≥ g′ − β − ι ≥ g − β` its `μ` is at most the present one.  It gives
procedures of accuracy exactly `g′n` (a family: enumeration for smaller accuracies) with the exponent

    T_F(g′) ≤ max{ μ , max_{1≤l≤L} [ min(μ, (1−φ)ξ_{l−1}) + (1−φ)(T_k(y_l) + ζ/4) ] }.

For every `l ≥ 1`, `ξ_{l−1} ≤ y_l + ζ/4 + ι`; so with `γ_l := (1−φ)y_l` the `l`-th term is at most
`min(μ, γ_l) + (1−φ)T_k(γ_l/(1−φ)) + 3ζ/4`.  If `γ_l ≥ β` the first two summands are at most `S`.  If `γ_l < β` — possible
only when `y_L = u < β/(1−φ)` — then `y_l ≥ u > ε*`, so `T_k(y_l) ≤ θ_na(y_l) = 0` and they are at most `μ ≤ S`.  Hence
`T_F(g′) ≤ S + 3ζ/4 ≤ T_{k+1}(g) + ζ`.
(b) Put `g := ξ/2`.  By (R) there is `k` with `T_k(g) < θ_hint(g) + η/2 ≤ h + η/2` (`θ_hint` is nonincreasing, `θ_hint(0) = h`);
(a) with `g′ = ξ` and `ζ = η/2` gives the family.  ∎

*Remark.*  Theorem 11.54 of the theory report asks for more — one family per level with the exponent `T_k(g⁻) + η_k` at
every `g` — and needs the bookkeeping with left limits of R7, §5.  For the limit statement only (a) is needed: an
accuracy rate slightly above `g` at the exponent `T_k(g) + ζ`, with finitely many inner families per step; the shift `ι`
of the ladder pays for the fact that the inner families are only available slightly above their nominal rates.

### 3.4 One more level at a bounded accuracy

**Theorem K2 [proved].**  Let a family `F` have the exponent function `T` on `[0,∞)`.  Let `0 < φ < 1`, `L ≥ 1` and rates
`2u =: ξ₀ > ξ₁ > … > ξ_{L−1} > 0` (none if `L = 1`).  Then there is a family `F′` with an exponent function `T′` such that
`T′(ξ) = T(ξ)` for `ξ > 0` and

    T′(0) ≤ max{ φa ,  max_{1≤l≤L−1} [ min(φa, (1−φ)ξ_{l−1}) + (1−φ)T(ξ_l) ] ,  min(φa, (1−φ)ξ_{L−1}) + (1−φ)T(0) }.      (3.1)

If `T(0)` is an exponent of `F` in the uniform sense (E0′), then the right-hand side of (3.1) is one of `F′` in the
sense (E0′).  In particular:
(a) *two rungs* (`L = 2`, `ξ₁ = ξ`):  `T′(0) ≤ max{ φa + (1−φ)T(ξ) , (1−φ)(ξ + T(0)) }`;
(b) *fine ladder:* for every `ε′ > 0` there is a ladder with `T′(0) ≤ R_φ[T](0) + ε′`,
    `R_φ[T](0) := sup_{γ≥0} [ min(γ, φa) + (1−φ)T(γ/(1−φ)) ]` — the bracket of (11.18.2) at `g = β = 0`.

*Proof.*  Fix a target accuracy `x > 0`, `c > 0`, `δ = e^{−cn}`.  Parameters of Algorithm 2L⁺ in dimension `n`:
`n_o = ⌊φn⌋`, `b = x/2`, `λ = η = η′ = θ = c₀ := min(x/12, ⅓)`, `ν₁ = 2e^u n_o/θ`, ladder `x_l = ξ_l n_i` (`1 ≤ l ≤ L−1`), `x_L = b`, inner
procedures `I_l = F(n_i, x_l, δ′)`.  *Accuracy:* `ln(e^λ(1+η)/(1−η) + η′ + θ + (2p_u)^n e^{−b}) ≤ c₀ + 2.25c₀ + 2c₀ + (2p_u)^n e^{−b} ≤ x/2`
for `n ≥ n₀(x,u)` (`ln((1+c₀)/(1−c₀)) ≤ 2c₀/(1−c₀²) ≤ 2.25c₀`), so `x_out ≤ b + x/2 = x`.  For `n` below the size at which
this, `1 ≤ n_o ≤ n−1`, `x_{L−1} > b` and the hypotheses of Lemma K.4(c),(d) hold, the procedure enumerates the cube.
`F′(n, x, δ)` is the cheaper of `F(n, x, δ)` and this procedure (monotone hull); so `T′ ≤ T` on `(0,∞)`.
*Cost.*  `J = O(n)`, `ν₀ = O(n)`, `m_max = O(n)` (`π† ≥ 2^{−n_o−1}`), `K = O(n)`, `ν = O(n²)`, `cnt(y) = O(n²)e^y`, and by Lemma K.4(d)
`ln M̄ ≤ n_o a + O(√n)`.  `ln(1/δ′) = cn + ln(4L·M̄) ≤ c′n_i` with `c′ = (c+1)/(1−φ)`, so `C_l ≤ C_F(n_i, x_l, e^{−c′n_i})`.  By
Theorem K1, `C_max = 1 + 2M̄ + Σ_l min{2M̄, (J+1)cnt(x_{l−1})}·C_l`, and with `n_o/n → φ`, `n_i/n → 1−φ`, (E1) at the rates
`ξ₁,…,ξ_{L−1}` and (E0) at the accuracy `x/2`, the `l`-th term has the exponent in (3.1) (`x₀ = 2un_i` for `l = 1`).  Only
finitely many rates occur.  (a): bound `min(φa, ·) ≤ φa` in the first term and `min(φa, (1−φ)ξ) ≤ (1−φ)ξ` in the second.
(b): take `ξ_{l−1} − ξ_l ≤ ε′` and `ξ_{L−1} ≤ ε′`; with `γ_l = (1−φ)ξ_l` the `l`-th term is at most
`min(φa, γ_l) + (1−φ)T(γ_l/(1−φ)) + ε′`, the last one at most `(1−φ)T(0) + ε′` (the value at `γ = 0`), and
`φa ≤ R_φ[T](0)` (`γ → ∞`).
*Uniform version.*  Let `x_n ≤ 1` with `ln(1/x_n) = o(n)` and run the same construction with `x = x_n`: `c₀ = x_n/12`,
`m₀ ≤ ⌈ln 2/u⌉`, `J, ν₀ = O(n/x_n)`, `K = O(n/x_n²)`, `cnt(y) = poly(n, 1/x_n)e^y`, and by Lemma K.4(d)
`ln M̄ ≤ n_o a + (u + ln 4)(1 + √((n_o/2)·ln(24e^{u(m₀+2)}/x_n))) + O(ln(n/x_n)) = n_o a + o(n)` (its hypothesis `r₊ ≥ p_u n_o/2` holds
for large `n`); the accuracy is at most `x_n/2 + 0.4375x_n + (2p_u)^n ≤ x_n` once `(2p_u)^n ≤ x_n/16`.  The inner
bounded accuracy is `x_n/2` in dimension `n_i`; the map `n ↦ n_i` takes each value at most `⌈1/(1−φ)⌉ + 1` times, so
`x′_d := min{x_n/2 : n_i(n) = d}` has `ln(1/x′_d) = o(d)`, and (E0′) for `F` applies because the cost is nonincreasing in
the accuracy.  All other factors are `e^{o(n)}`, and the exponents of the terms are as before.  ∎

The loss of accuracy per level is `x − b = x/2` here only for convenience; any split `b = (1−ς)x` works.  **The tolerance
`b` equals the inner accuracy, and what the level adds is `ln(e^λ(1+η)/(1−η) + η′ + θ) + o(1)`, as small as one likes.**

---

## 4. The adaptive exponent at a bounded accuracy

**Theorem K3 [proved, given (LB) and (R)].**  For every `u > 0`, `ε > 0`, `0 < δ < ½`: the least worst-case number of
evaluations of a randomised adaptive algorithm without a hint that is `(ε/2, δ)`-correct on `L_u(Q_n)` is `exp(nh + o(n))`.
The same holds for the least worst-case *expected* number.

*Proof.*  Lower bound: (LB), an algorithm without a hint being one with a hint; the bound is on the expected number
at the zero function, hence on both quantities.  Upper bound.  Fix `0 < η < h`; put `φ := min(½, η/a)` and
`ξ := min(ε*/2, φη)`.  By Proposition E(b) there is a family with exponent function `≤ h + η` at `ξ`; let `G₀` be the pointwise cheaper
of it and of the base family (Proposition K0): its exponent function `T₀` has `T₀(ξ) ≤ h + η` and `t₀ := T₀(0) ≤ a`.  Let
`G_{m+1} := (G_m)′` by Theorem K2(a) with this `φ` and the single rate `ξ` (`ξ < 2u`).  Then `T_{m+1}(ξ) ≤ T_m(ξ) ≤ h + η` and

    t_{m+1} := T_{m+1}(0) ≤ max{ φa + (1−φ)(h+η) , (1−φ)(ξ + t_m) } ≤ max{ h + 2η , (1−φ)t_m + φη },

i.e. `t_{m+1} − η ≤ max{h + η, (1−φ)(t_m − η)}`, so `t_m ≤ η + max{h + η, (1−φ)^m a}` (`two_rung_bound`, machine-checked).
For `m ≥ ln(a/h)/φ`: `T_m(0) ≤ h + 2η`.
By (E0), for the given `ε` and `δ_n := min(δ, e^{−n})`, the procedure `G_m(n, ε, δ_n)` makes at most
`exp(n(h + 2η) + o(n))` evaluations on every `ψ ∈ L_u(Q_n)` and returns, with probability `≥ 1 − δ`, a bracket of ratio
`≤ e^ε` around `A`; the midpoint of its logarithms is `(ε/2, δ)`-correct.  `η` was arbitrary.  ∎

*Remarks.*  (1) The algorithm has `m ≈ ln(a/h)·a/η` nested bounded-accuracy levels on top of the extensive-accuracy
family of Proposition E at the single rate `ξ ≈ η²/a`, which itself has `k(ξ, η)` levels; each bounded level uses the
fraction `φ ≈ η/a` of the remaining coordinates for its outer sample.  Nothing here is an algorithm one would run
(§6.4).  (2) The contraction is machine-checked as an abstract statement: `bounded_iterates_lt` (`KBounded.lean`;
hypothesis: the extensive exponents converge pointwise to a function `≤ h`), `levels_reach_hint_at_zero`
(`KBoundedLink.lean`; the same with the hypothesis discharged by the repository's `iterates_lt_hint_add`, i.e. for any
`HintPair`), and `cube_levels_reach_hint_at_zero` (`KBoundedCube.lean`; for the functions `θ_na`, `θ_hint` of the cube, by
the repository's `cubePair`, with `θ_hint ≤ h` proved there as `cubeHint_le_cubeH`).  (3) Accuracy bookkeeping: `G_m` at accuracy `ε` calls `G_{m−1}` at the bounded accuracy `ε/2` (and at `ξn_i`),
…, `G₀` at `ε/2^m`; a fixed positive number, so (E0) applies at every level.

**Corollary K3′ (accuracies that depend on `n`).**
(i) **[proved]** If `ε_n ≥ ε₀ > 0` and `ε_n = o(n)`, the adaptive exponent without a hint at accuracy `ε_n` is `h`
(the cost is nonincreasing in the accuracy; lower bound: Theorem 11.25(d), third row).
(ii) **[proved, given (LB) and (R)]** If `ε_n → 0` with `ln(1/ε_n) = o(n)`, the exponent is still `h`.  The base family
satisfies (E0′) (Proposition K0), Theorem K2 preserves (E0′), so the families `G_m` of the proof of Theorem K3 have
`T_m(0) ≤ h + 2η` in the sense (E0′), and `G_m(n, ε_n, e^{−n})` costs `exp(n(h + 2η) + o(n))`; the lower bound is the third
row of the table of Theorem 11.25(d).  (Through the `m` levels the accuracies are `ε_n, ε_n/2, …, ε_n/2^m`, all with
logarithm `o(n)`.)
Together with Theorem 11.54 (whose upper bound also follows from Proposition E(a), (R) and the continuity of `θ_hint`:
`T_F(ξ) ≤ θ_hint(g) + η` for every `g < ξ`): **the adaptive exponent without a hint is `θ_hint(lim ε_n/n)` for every accuracy with
`ln(1/ε_n) = o(n)`, from sub-exponentially small to extensive**; for exponentially small accuracies (`ε = e^{−λn}`, rows 4–6
of the table of Theorem 11.25(d)) nothing is claimed.

**Proposition K5 (the recursion on `[0,∞)`) [(a), (b) proved; (c) machine-checked for the cube as a statement about
sequences `T_k`, `τ_k` with the listed properties; (d) numerical].**  Let `T₁ = θ_na` on `(0,∞)`, `T₁(0) = a`, and
`T_{k+1}(g) = min(T_k(g), R[T_k](g))`, with `R[T](g)` as in (11.18.2) for `g > 0` and `R[T](0) := inf_φ R_φ[T](0)`; `τ_k := T_k(0)`.
(a) For every `k ≥ 1` and `ε′ > 0` there is a family whose exponent at bounded accuracy (E0) is at most `τ_k + ε′`.
    Proof by induction: `τ₁ = a` is Proposition K0.  If `τ_{k+1} = τ_k` there is nothing to do; otherwise choose `φ` with
    `R_φ[T_k](0) ≤ τ_{k+1} + ε′/4`, rates `0 < y_{L−1} < … < y_1 < 2u` (`L ≥ 2`) with `y_{L−1} ≤ ε′/4`, gaps `≤ ε′/4` (also
    `2u − y_1 ≤ ε′/4`), `0 < ι ≤ ε′/4` with `y_1 + ι < 2u`, and `ξ_l := y_l + ι`.  Let `F_l` be families with
    `T_{F_l}(ξ_l) ≤ T_k(y_l) + ε′/4` (Proposition E(a)), `F_0` one with bounded exponent `≤ τ_k + ε′/4` (induction), and `F*`
    their pointwise cheapest.  Theorem K2, (3.1), for `F*`, `φ` and the rates `ξ_l` gives
    `T′(0) ≤ max{φa, max_{l≤L−1}[min(φa, (1−φ)ξ_{l−1}) + (1−φ)(T_k(y_l) + ε′/4)], min(φa, (1−φ)ξ_{L−1}) + (1−φ)(τ_k + ε′/4)}`.
    As `ξ_{l−1} ≤ y_l + ε′/2` and `ξ_{L−1} ≤ ε′/2`, the `l`-th term is at most the bracket of `R_φ[T_k](0)` at `γ = (1−φ)y_l`
    plus `3ε′/4`, the last one at most its value at `γ = 0` plus `3ε′/4`, and `φa ≤ R_φ[T_k](0)`: `T′(0) ≤ τ_{k+1} + ε′`.
(b) *The necessary condition of D45 holds at accuracy zero:* if `T ≥ θ_hint` on `(0,∞)` then `R_φ[T](0) ≥ h` for every `φ`;
    hence `τ_k ≥ h` for all `k`.  Proof: take `γ = φa`, `X = φa/(1−φ)`.  If `X < ε*`, `ρ_i := (Λ₁+X)/u` satisfies
    `φp_u + (1−φ)ρ_i = (φ(up_u + a) + (1−φ)Λ₁)/u = Λ₁/u` (as `up_u + a = Λ₁`), and by convexity of `KL(·‖½)`:
    `φa + (1−φ)θ_hint(X) = φKL(p_u‖½) + (1−φ)KL(ρ_i‖½) ≥ KL(Λ₁/u‖½) = h`.  If `X ≥ ε*`: `ρ̄ := φp_u + (1−φ)/2` has
    `uρ̄ = Λ₁ − φa + (1−φ)ε* ≤ Λ₁`, so `φa = φKL(p_u‖½) + (1−φ)KL(½‖½) ≥ KL(ρ̄‖½) ≥ h`.  The two-rung bound of Theorem
    K2(a) passes the same test for all `φ, ξ` (with `T(0) ≥ h`): if `(1−φ)ξ ≤ φa` its first term is `≥ h` by the same
    convexity argument, otherwise its second term exceeds `φa + (1−φ)h ≥ h`.  (Of course `τ_k ≥ h` also follows from
    (LB); the direct proof is the consistency test.)
(c) `τ_k → h`.  (`cube_levels_reach_hint_at_zero`: its hypotheses are those of `cube_iterates_lt_hint_add`,
    `T_k(x) ≤ τ_k` — true because `R[T](g) ≤ R[T](0)` — and the step at zero, which is the definition of `τ_{k+1}` since
    the supremum over `γ > φa` is attained at `γ = φa`.  For the extensive part the hypotheses are machine-checked
    (`KExactRecursion.lean`); `T_k ≤ τ_k` and the step at zero are on paper.)
(d) Values at `u = 1` (`h/a = 0.2627`): `τ_k/a = 0.5006, 0.3613, 0.3108, 0.2898, 0.2803, 0.2723, 0.2689, 0.2659, 0.2643, 0.2634,
    0.2631` for `k = 2, 3, 4, 5, 6, 8, 10, 14, 20, 30, 40`; `0 ≤ τ_k − T_k(10⁻⁶ε*) ≤ 0.001a` (continuity at zero); `(τ_k − h)/a ≈ 0.65/k²`; and
    `max_g (T_k − θ_hint)(g) = τ_k − h`: **the bounded accuracy is the point where the recursion converges most slowly.**
    Similar for `u = ½, 2` (§6.1).

---

## 5. The coordinator's sketch, step by step

**(1) Layer-cake sum for the lower end — correct [proved; machine-checked].**  `A ≥ Σ_{populated i}(t_i − t_{i−1})p(t_i)` with
`t_i = s_ie^{−b}` is a lower Riemann sum of `∫p`; with a ladder of ratio `e^λ` the factor is `1 − e^{−λ}` (the sketch's `1 − 1/e`),
and the populated part of the upper end is `c_η^{−1}e^{λ+b}` times the sum (`certified_lower_sum_le_mean`,
`populated_part_le`).  It is also necessary: with the maximum as lower end the ratio really is of order `J` when many
levels carry the same `s·p(s)` (profile `W(d) ∝ 1/|B(n_o,d)|`; mutation `maxform`).  One addition is needed that the sketch
does not mention: `s₀ ≤ ℓ` only gives an additive `1` in the ratio; the reference bound
`ℓ ≥ e^{−ψ₀}((1+e^{−u})/2)^n = (2p_u)^{−n}s₀` removes it.

**(2) The closure window — wrong as a mechanism; the question "does every level close inside it?" has the answer
no, and a different mechanism is needed [proved: Lemma K.4, Theorem K1(iii); numerical: §6.3].**
* The one-sided ratio is never `O(1)` uniformly: `Γ̃(r) → (e^u−1)/(y(1−ye^u))`, `y = ρ/(1−ρ)`, for `ρ < p_u` fixed, with
  minimum `4e^u(e^u−1)` at `ρ = 1/(2e^u+1)`; it is `≈ (e^u−1)n/r` for small `r` (as the sketch says), but also `≈ c(u)√n` at
  `r = p_un` (`c(1) ≈ 2.6`), and `e^{nKL(ρ‖p_u)}` above.  The test of the sketch, `Γ̃(r) ≤ e^{G−b}/4`, therefore has an empty
  window unless `G − b ≥ ln(16e^u(e^u−1))` (`2.84, 4.31, 6.63` for `u = ½, 1, 2`), and for larger `G − b` the limiting window is
  `ρ₋ ≤ ρ ≤ ρ₊` with **`ρ₊ < p_u`**: `KL(ρ₊‖½)/a = 1.090, 1.011, 1.0015` for `G − b = 6, 8, 10` at `u = 1`.  The outer sample would
  have the exponent `φ·KL(ρ₊(G−b)‖½) > φa`, which tends to `φa` only as `G − b → ∞`: by this route one could hope for the
  weak form of the conjecture at best.
* Worse, populated levels do not close in that window at all.  A populated level always has its closing radius
  within `O(√(n log n))` of `p_un_o` or above **[sketch]**: the lower levels have certified `ℓ ≥ A/poly(n)`, Lemma K.1(b)
  gives `A ≥ s_je^{−b}2^{−n_o}T_{n_o}(k)` with `T_{n_o}(k) ≥ ½e^{uk}(1+e^{−u})^{n_o}`, so `M_j^neg ≤ poly·2^{n_o}e^{−uk}(1+e^{−u})^{−n_o}`, while a
  populated level needs `M ≳ K2^{n_o}/|B(n_o,r)|`, `k = r − O(1)`; together `KL(r/n_o‖p_u) ≤ O(log n/n)`.  (In words: a level
  whose super-level set is a ball well inside radius `p_un_o` carries a negligible share of the mass of the cone above
  it, and is declared negligible before it is populated.)  At those radii `Γ̃ ≈ √n`, so with `G − b = O(1)` the test of
  the sketch fails at every populated level.  It succeeds later, at an unpopulated level, provided the factor in the
  negligibility threshold is at least of order `n_oe^{u−(G−b)}` (the factor `J` of Theorem 11.52 is, when `e^{G−b} ≳ e^u/u`):
  so the algorithm with the sum-form lower end *does* close with a bounded ratio after `e^{n_oa + O(√(n log n))}` outer
  points (§6.6, variant "plain", confirms both statements in expectation up to `n_o = 16 000`) — but a proof of this
  needs the two-sided tail lemma in the *analysis* anyway.
* The repair used here puts that lemma into the *algorithm*: the Harper term in step (b).  Then a populated level
  closes whenever `Γ″(r) ≤ θ`, which holds for every `r ≤ p_un_o − O(√n_o)` and any constant `θ > 0` — no window, and no
  constant lost in the accuracy; and an unpopulated level closes whenever `Γ̃(r) ≤ θ(1−η)ν₀`, which holds for every
  `r ≤ p_un_o` once `ν₀ ≥ 2e^un_o/(θ(1−η))` (Lemma K.4).  "The doubling of the sample size moves `r` through all radii" is
  not needed: the proof only uses the state at the moment a level is left.

**(3) The recursion at vanishing accuracy rate — correct [proved: Theorem K2, Proposition K5].**
`τ_{k+1} = min_φ max((1−φ)τ_k, sup_{0<x≤φa/(1−φ)}(1−φ)(x + T_k(x)))` is `R[T_k](0)`, the bracket of (11.18.2) at `g = β = 0` with
`T_k(0) = τ_k`; the first term is the price of the polynomially many points within a bounded factor of a level, each
of which needs an inner bracket of bounded accuracy.  It never goes below `h` (K5(b)) and tends to `h` (K5(c)).  For
the limit Step I of Theorem 11.53 is not needed in full: one extensive rung and the bound `T_k(ξ) ≤ h + η` suffice
(Theorem K3).  Numerically the excess `τ_k − h` is the largest excess `T_k − θ_hint` over all accuracies.

**(4) "Each level adds `O(1)` to the accuracy, so `k` levels give `≈ k·C(u)`" — true for the algorithm as sketched, but
not necessary [proved: Theorem K1, width].**  The tolerance `b` must be at least the inner accuracy, but nothing else
has to be lost: the ratio is `e^b(e^λ(1+η)/(1−η) + η′ + θ) + (2p_u)^n`, and `λ, η, η′, θ` are free (they cost factors
`1/λ, 1/η², 1/η′, 1/θ` in `J, K, ν₀`).  With `G > b` replaced by the Harper closure there is no constant `C(u)`.  Hence the
strong form.

**(5) The base family — conclusion correct, reason not [proved: Proposition K0].**  See §3.2: the bound `3 + 12Γ(r)` is
never below `3 + 48e^u(e^u−1)` and is not bounded up to `p_un`; the bounded ratio at exponent `a` comes from Lemma
11.43(c) (this is also how Theorem 11.44(ii) gets every fixed accuracy).

---

## 6. Numerical checks (own code; commands, sizes, outcomes)

All scripts are in this directory; `klib.py` holds the shared log-tables (`test_klib.py`: tables against brute force
for `n ≤ 30`, agreement to `10⁻⁹`).  Every run under `ulimit -v 4000000`, one at a time.  `python3 check_tail_lemmas.py`
(< 1 s): Lemma K.1(a),(b) at every threshold of 408 `u`-Lipschitz functions on `Q_4 … Q_10` (5102 thresholds), no
violation, both equality cases attained.

### 6.1 The recursion with the point `g = 0`  — `python3 recursion_bounded.py` → `out_recursion_bounded.txt` (152 s)

`T_k` on a grid `0 = g₀ < g₁ = 10⁻⁶ε* < … < ε*` (161 points; 241 in the one-sided mode); for each `g` a grid search over
`(φ, β)` (72 × 20 values, special values `g/(g+θ_hint(g))`, `g/h`, two local refinements); `sup_γ` exact for the
interpolant; at `g = 0` the formula `R[T](0)`; 40 levels; `u = ½, 1, 2`.  Two modes: piecewise-linear interpolation, and a
step function to the left (`T(g_i)` on `[g_i, g_{i+1})`), which makes every number a rigorous upper bound of the exact
recursion up to rounding (cf. D45, item 6: this mode stalls a few per cent above the limit).

| `u` | `h/a` | `τ_k/a`, `k = 2, 3, 4, 5, 6, 10, 20, 40` (linear) | `τ_40/h` linear / one-sided |
|---|---|---|---|
| ½ | 0.2532 | 0.5001, 0.3568, 0.3037, 0.2814, 0.2711, 0.2593, 0.2548, 0.2537 | 1.0017 / 1.026 |
| 1 | 0.2627 | 0.5006, 0.3613, 0.3108, 0.2898, 0.2803, 0.2689, 0.2643, 0.2631 | 1.0016 / 1.027 |
| 2 | 0.2968 | 0.5056, 0.3814, 0.3393, 0.3225, 0.3145, 0.3033, 0.2985, 0.2972 | 1.0016 / 1.024 |

Checked in every step: nonincreasing in `k` and in `g`; never below `θ_hint` (in particular `τ_k ≥ h`: the necessary
condition of D45); `τ₂` equal to the closed form `min_φ max((1−φ)a, φa + (1−φ)θ_na(φa/(1−φ)))` (`0.5001a, 0.5004a, 0.5056a`);
`0 ≤ τ_k − T_k(g₁) ≤ 0.001a`; the one-sided values above the linear ones.  All passed.  The minimising `φ` at `g = 0` falls
like `0.50, 0.28, 0.14, 0.068, 0.033, …, 10⁻⁴`: deep levels use small outer blocks, as in the proof of Theorem K3.

### 6.2 The outer loop with a simulated inner oracle  — `python3 sim_outer_loop.py` → `out_sim_outer_loop.txt` (4 min)

Algorithm 2L⁺ exactly as in §2.2 with **the constants of the theorem** (`K ≈ 230–950`, `ν`, `J`, `m_max` from the formulas,
`δ = 0.05`).  The fibre averages are exact; a call of the inner procedure at accuracy `x` returns a valid bracket of
ratio `e^x` placed by one of five rules (random; value at the top; value at the bottom; adversarial — keep the point
unclassified at the current level as long as a valid bracket allows, then make it high, resp. low).  Instances:
(i) 120 `u`-Lipschitz functions on the enumerated cube `Q_8 × Q_4` (McShane extensions of random data, mixtures,
truncated cones, regularised noise, cone, dip, flat); (ii) 240 radial outer landscapes `n_o ∈ {12,…,40}` with the exact
binomial law (flat, dip, cone, mesa, flattened bottom, random walk, "staircase" `W ∝ 1/|B(n_o,d)|`, alternating);
(iii) 80 runs aimed at the negligible branch (`u ∈ {1.5, 2}`, `n_o ∈ {36, 40, 44}`, `ν₁ = 1`, `θ` such that the first level
above a flat bulk cannot close).  Parameters at random: `λ ∈ [0.22, 1]`, `η ∈ {¼, ½}`, `η′ ∈ {0.1, 0.5, 1}`,
`θ ∈ {0.1, 0.5, 2, 20}`, `b ∈ {0.25, 0.5, 1, 3}`, `ν₁ ∈ {1, 2e^un_o/θ}`.  394 runs completed (46 skipped: more than `1.6·10⁷`
outer points).

On each run the good event (V2), (V3) is verified exactly on the realised sample (it held in all 394 runs), and
then **every claim of Theorem K1** is tested: C1 `L ≤ A ≤ U`; C2 the width bound and its three components; C3 every
certificate (`q_i ≥ p(s_i)`, `p̲_i ≤ p(s_ie^{−b})`, `ℓ ≤ A` at each update); C4 every level left has `r(q_j) > r†`;
C5 `M ≤ max(K, 2M^neg)`, `M^neg ≤ (1+η)e^λν₀M†`, `M ≤ M̄`; C6 the count `M_j^neg p(s_je^{−x}) ≤ c_η^{−1}e^λνe^x` and the sampled count
`≤ cnt(x)` for every rung; C7/C8 the number of calls per level and rung; termination within `J+1` levels.
**No violation.**  Widest bracket `ln(U/L) = 5.71` (a run with `b = 3`, `θ = 20`), smallest distance to the width bound
`0.074`; the count reaches `0.57` of its bound; `30 445` levels left as populated and `36` as negligible (in 10 runs);
closures: 52 with an empty tail (`2^{n_o}q < 1`), 55 at a populated level, 287 at an unpopulated one; 341 by the tail
lemma at a radius `≤ n_o − 2`, 118 at a radius `≤ r†`; largest sample `1.5·10⁷` points, largest `M/M† = 4.5`.
A second seed (`python3 sim_outer_loop.py seed 777` → `out_sim_outer_loop_seed777.txt`, 2 min 16 s): 394 runs, again
no violation; `31 970` populated and `47` negligible levels (12 runs); widest bracket `5.98`, `0.08` inside the bound.

*Power of the test* — five mutations, each detected by the check it should break: lower end without the sum
(`maxform`: width violated in 18 of 143 runs); no Harper term (`noharper`: levels left with `r ≤ r†` in 11 of 142);
tail lemma applied at `r = n_o` (`close_at_no`, the gap of D45 item 4: invalid bracket in 150 of 164); negligibility
threshold `νs/ℓ` without `e^{−b}` (`neg_tol`, a tolerance mismatch: count violated in 21 of 143); `q` without the factor
`1/(1−η)` (`q_plain`: false certificate in 41 of 150).

*What it does not exercise:* with the bounded-regime `ν₁` no level is ever left as negligible at these sizes (that
needs larger `n_o` and samples far beyond `10⁷` points; cf. R7, m9) — the 36 negligible levels all come from the runs
with `ν₁ = 1`; §6.8 fills this gap.  The cost of the inner procedure is not simulated (only the number of calls per
rung).

### 6.3 The closure window  — `python3 closure_window.py` → `out_closure_window.txt` (2 s)

Tables of `Γ̃`, `κ`, `Γ″`, `r†` for `n ∈ {50, …, 12 800}` (and `10⁵` for the window), `u ∈ {½, 1, 2}`, `η = ¼`:
* Lemma K.4(a): `max_{r ≤ p_u(n+1)} Γ̃(r)/(2e^un) ≤ 0.21, 0.34, 0.51` (`u = ½, 1, 2`) — below 1;
* `min_r Γ̃(r) → 4e^u(e^u−1)` (`18.672` at `n = 12 800` against `18.683`, `u = 1`), attained at `ρ → 1/(2e^u+1)`;
* `Γ̃(⌊p_un⌋)/√n = 0.63, 2.58, 19.1`: the one-sided ratio is unbounded at `p_un`;
* Lemma K.4(b): `max_{1≤r≤p_un} Γ″(r)/(2e^{u(m₀+2)}P(Bin ≤ r)) ≤ 0.94`, and `κ(r) ≥ r−1−m₀` throughout;
* Lemma K.4(c),(d): `r† ≥ r₊` in all 27 cases (e.g. `u = 1`, `n = 12 800`: `r† = 3313`, `r₊ = 3246`, `p_un = 3442`), and
  `n^{−1}ln(2ⁿ/|B(n,r†)|) = a·(1 + 1.2u/(a√n))` — the `O(√n)` correction of the outer sample is real (`1.10a` at `n = 12 800`);
* the window of the sketch (§5(2)): limit window and its values at `n = 6400`, `10⁵`.

### 6.4 What the algorithm costs at the flat instance  — `python3 flat_cost_bounded.py` → `out_flat_cost_bounded.txt` (49 s)

At `ψ ≡ 0` all fibre averages are equal, so the outer loop is deterministic once the inner behaviour is fixed; with
the inner bracket `[W, We^x]` (the worst valid behaviour above the bulk) plus `K` points at the finest accuracy, the
**exact** number of evaluations of Algorithm 2L⁺ with base brackets (Proposition K0) inside is computed in the log
domain, all constants from the formulas (`b = 0.5`, `λ = 0.2`, `η = η′ = θ = 0.05`: certified `ln(U/L) ≤ 0.872`; `δ = 0.05`;
geometric ladder of 40 inner rates; best `φ` of a grid).  `crosscheck_flat.py`: the closed-form trajectory agrees
with the simulated outer loop of §6.2 in 9 of 9 parameter sets (closing level, radius, sample size, numbers of
populated and negligible levels).

| `n` (`u = 1`) | two levels: `ln(cost)/(na)` | plain bracket, same accuracy | hinted lower bound | best `φ` |
|---|---|---|---|---|
| 250 | 1.698 | 1.925 | 0.332 | 0.85 |
| 1 000 | 0.701 | 1.349 | 0.286 | 0.80 |
| 4 000 | 0.548 | 1.152 | 0.271 | 0.65 |
| 16 000 | 0.522 | 1.069 | 0.265 | 0.55 |
| 64 000 | 0.512 | 1.033 | 0.263 | 0.55 |
| limit | `τ₂/a = 0.5006` | 1 | `h/a = 0.2627` | 0.50 |

(`u = 2`: `0.817, 0.598, 0.549, 0.526, 0.521` against `1.532, 1.229, 1.104, 1.050, 1.024` and `0.334 … 0.297`; limits `0.5057`, `1`,
`0.2968`.)  **No cost is below the hinted lower bound** (asserted for every `n`): the necessary condition holds at
finite `n` on the instance where it bites.  At a bounded accuracy two levels beat the plain bracket from `n ≈ 250`
on — where either needs more than `e^{45}` evaluations.  The values are not monotone in the last digits because of
the grids in `φ` and in the ladder.

### 6.5 End to end with real inner brackets  — `python3 e2e_small.py` → `out_e2e_small.txt` (5 min 8 s)

*Part A (Proposition K0).*  The base bracket on 24 Lipschitz functions of `Q_10` per parameter set, `u ∈ {½, 1, 2}`,
accuracies `0.6, 1, 2, 4`, `δ′ ∈ {0.3, 10⁻³}`, the two samples drawn exactly (multinomial counts): 17 280 brackets, none
invalid; the three events of the proof failed 3 times (bounds `0.29–0.30` per bracket for `δ′ = 0.3`: Chernoff is
loose); on the good event no bracket was wider than the certified `ln((1+η)/(1−η)) + ln(1+Γ″(r̂))`.
*Part B (the whole algorithm).*  Algorithm 2L⁺ on explicit `u`-Lipschitz functions of `Q_{n_o} × Q_{n_i}`,
`(n_o, n_i) ∈ {(6,6), (8,6), (6,8)}`, with the base bracket of Part A as the inner procedure on each fibre (own
randomness per call; enumeration of the fibre where no two-sample bracket of the requested accuracy exists on so
small a cube: 38 of 317 rungs), every constant from the formulas, `δ = 0.05`, `δ′ = δ/(4LM̄)`: **84 runs, `1.05·10⁷` real
inner brackets, every final bracket valid and within the width bound of Theorem K1** (widest `2.53`, smallest
slack `0.18`), no abort, the number of evaluations at most `0.33 %` of `C_max`.  At this size an inner bracket costs
more than enumerating its fibre; the run tests the logic of the complete pipeline with real randomness, not its
cost.  (Workstream H ran an earlier variant of the extensive algorithm end to end at `n = 32`, 12 of 32 runs closing
within its budget; R7 lists a run of the corrected algorithm with real inner brackets as not done.  Here every run
closes, because the constants are those of the proof and the cubes are small enough to exhaust.)

### 6.6 Radial and additive outer landscapes at large `n_o`, in expectation  — `python3 radial_trajectory.py` → `out_radial_trajectory.txt` (145 s)

The outer loop depends on the instance only through the law of `W` and on the inner oracle only through which
points of the tolerance zone it lets be high.  For 17 radial profiles (flat, cone, cone of slope `u/2`, anti-cone,
cones with a flattened bottom and mesas at three radii, dips at three radii around `Λ₁n_o/u`, the "staircase"
`W ∝ 1/|B(d)|`, three random walks, the 2-periodic profile), `u ∈ {½, 1, 2}`, `n_o ∈ {1000, 4000, 16 000}`, the run is
evaluated exactly with counts replaced by their means (binomial law in logarithms; the pass at which a level is
populated, negligible or closed in closed form), for the algorithm of Theorem K1 and for the variant without the
Harper term ("plain": the lower end of the sketch), with the constants of the theorem (`b = 0.5`, `λ = 0.5`, `η = ¼`,
`η′ = θ = 0.1`; certified `ln(U/L) ≤ 1.581`); 510 runs.  In addition 5 *non-radial* outer landscapes with an exactly known
law of `W`: additive ones, `−ln W(a) = Σ_i c_i a_i` with slopes `c_i ∈ {±u, ±u/2, 0}` in blocks (law by convolution of
binomial laws in the log domain, checked against enumeration), `n_o ∈ {1000, 4000}`: 120 runs.  **No violation** of
validity, of the width bound, of claim (iii) (every level left has `r(q_j) > r†`), of claim (iv) (`M_j^neg`, `M_j ≤ M̄`) or of
the count (v), in any of the 630 runs.  Three further readings:
* the closing sample: `max over profiles of ln M_last/(n_oa) = 1.43, 1.19, 1.08` for `n_o = 1000, 4000, 16 000` at `u = 1`
  (`1.92, 1.36, 1.16` at `u = ½`; `1.24, 1.11, 1.05` at `u = 2`): the exponent `a` of the outer sample with its `O(√n_o)`
  correction, on every profile; without the Harper term `1.54, 1.25, 1.12` — slightly more, same exponent;
* *populated levels sit at or above `p_un_o − O(√(n_o log n_o))`* (§5(2)): over all populated levels of all runs,
  `(r(q_j) − p_un_o)/√(n_o ln n_o) ≥ −0.40` with the Harper term and `≥ −0.52` without, at every size;
* most runs close at an *unpopulated* pass (277 of the 306 radial and 39 of the 60 additive runs listed), where the
  certified `q` is small enough; the others close at a populated level through the Harper term (or, in the plain
  variant, through the one-sided test with `θ = 0.1` once `r` is small).
A pitfall met on the way: computing the closing radius for `q = 1` in floating point returns a radius `< n_o` once
`ln|B(n_o,r)|` is indistinguishable from `n_o ln 2`, and the tail lemma applied there closes level 0 with an upper end
below the lower end — the gap of D45 item 4 again, in numerical guise; `q = 1` must be handled exactly (`klib.radius`).

### 6.7 Lean  — `lake env lean <file>` from the repository root (about 10 s each; `out_lean_*.txt`)

`KBounded.lean` (imports Mathlib only): `bounded_iterates_lt` (the contraction at accuracy zero), `two_rung_bound`
(the iteration in the proof of Theorem K3), `certified_lower_sum_le_mean` (sum form of the lower end, (2.2)),
`populated_part_le`, `close_points_bound'` (the count of Step 7), `width_le` (Step 4).  `KBoundedLink.lean` (imports the repository's `proofs.Frontiers.HintRecursion`):
`levels_reach_hint_at_zero`.  `KBoundedCube.lean` (imports the repository's `proofs.Frontiers.CubeHintPair`, commit
`4cef47e`): `cubeHint_le_cubeH`, `cube_levels_reach_hint_at_zero`.  `KExactRecursion.lean` (same import): the exact
recursion `T₁ = θ_na`, `T_{k+1} = min(T_k, R[T_k])` defined in Lean (`exactRec`), `stepLE_exact`, `Rstep_anti`,
`exactRec_props`, and `exactRec_reaches_hint`: statement (R) with no hypothesis about the sequence (5 s).  All compile without `sorry` (exit 0);
`#print axioms`: `propext, Classical.choice, Quot.sound`.  Do not run them under `ulimit -v` (Lean maps its libraries).
**Not formalised:** the algorithm, its events, the cost sum, Lemma K.1/K.4, Harper's theorem, Proposition E (the
assembly), and that the recursion *at accuracy zero* (`τ_k`) satisfies the hypotheses of `cube_levels_reach_hint_at_zero`
(Theorem K3 does not use that statement: its iteration is `two_rung_bound`).

### 6.8 The outer loop at medium size, bounded regime, real fluctuations  — `python3 sim_grouped.py` → `out_sim_grouped.txt` (4 min 51 s)

The same algorithm, constants and checks as in §6.2, in the regime of Theorem K2 (`ν₁ = 2e^u n_o/θ`), at sizes where
levels really are left as negligible and the ladder is closed by the tail lemma after `10⁸ … 10^{18}` outer points:
radial outer landscapes (the eight profiles of §6.2) with `(u, n_o) ∈ {½}×{300, 400, 600} ∪ {1}×{100, 150, 200} ∪
{2}×{36, 48, 60}`, `n_i = 4`, `b ∈ {0.25, 0.5, 1}`, `λ ∈ [0.45, 1]`, `η ∈ {¼, ½}`, `η′, θ ∈ {0.1, 0.5}`, `δ = 0.05`, the five oracle
rules.  The list `a₁, a₂, …` is sampled exactly but stored as counts per shell and per block of the doubling sequence
(python integers in the checks); all points of one (block, shell) group receive the same bracket — a valid, if
correlated, inner oracle — so each run is an exact run of the algorithm on a sample of up to `2^{62}` points.
1440 runs, 115 skipped (sample beyond `2^{62}`), **1325 completed: the good event (V2), (V3) held in all of them and no
claim of Theorem K1 was violated** (C1–C8 as in §6.2).  `358 790` levels left as populated, **`864` as negligible (in
115 runs)**; closures: 74 with an empty tail, 111 at a populated level, 1140 at an unpopulated one; 367 by the tail
lemma at a radius `≤ p_u n_o` and 140 at a radius `≤ r†`; 386 runs used more than `10^{12}` outer points, the largest
`4.6·10^{18}`; widest bracket `ln(U/L) = 3.13`, smallest distance to the width bound `0.016`; the count reaches `0.73` of its
bound, the negligible part `0.5 %` of its budget `η′e^bℓ`; largest `M/M† = 3.9`.
*Power at this size* (3 repetitions per case and profile): no Harper term — levels left with `r ≤ r†` or `M^neg` above
its bound in 27 of 191 runs; lower end without the sum — width violated in 81 of 200; `q` without `1/(1−η)` — false
certificate in 93 of 201; negligibility threshold without `e^{−b}` — count violated in 1 of 199 (weak here).
*A pitfall worth recording.*  numpy's `multinomial` is not usable at this size: it conditions sequentially on
`1 − p₁ − … − p_j`, which is rounding noise once the remaining mass is below `≈ 10^{−14}`, so with `n ≈ 2^{60}` the far-tail
cells — exactly the rare high levels — get wrong counts (cells of total mass `10^{−16}` receive no point instead of
`≈ 50`); and numpy's `binomial` returns `0` for `p < 10^{−16}` whatever `n`.  A first version of this run, with numpy's sampler,
showed the "good event" failing in 25 of 1345 runs (the conditional checks still passed).  `stable_multinomial.py`
(binary splitting over the cells sorted by probability, inversion with `log1p` for tiny conditional probabilities;
`python3 stable_multinomial.py` → `out_stable_multinomial.txt`, 3 s) samples the tail correctly: at `n = 2^{59}` and tail
masses `7·10^{−18} … 4·10^{−13}` the mean and variance of the tail counts agree with the exact values within sampling
error.  The smaller runs of §6.2 and §6.5 are not affected (cell probabilities `≥ 2^{−44}` and at most `1.6·10⁷` points).

---

## 7. The strong form, lower bounds, and what is open

**What the strong form needed** (item 4 of the brief): nothing beyond the weak form except the observation that the
tolerance `b` is the *only* quantity tied to the inner accuracy.  The three places where the two-level algorithm lost
constants — the factor `4e` between `q` and `p̲` (Chernoff and ladder), the gap `G − b` of the closure, the additive `1`
from `s₀` — are removed by `1 ± η` and `e^λ`, by the Harper closure, and by the reference bound.

**Lower bounds above `h` at a bounded accuracy** (item 5): by Theorem K3 there is none at the exponential scale, for
any fixed `ε > 0`; with (LB) the exponent is exactly `h`.  Consequences: (a) at the exponential scale a hint is worth
nothing to an adaptive algorithm at bounded accuracy either, and the zero function is the hardest instance with a
hint there too (remark (4) of §11.18 extends); (b) the complete picture for the cube class is

| accuracy | non-adaptive | adaptive without a hint = with a hint at the hardest instance |
|---|---|---|
| `ε₁n`, `ε₁ > ε*` | `0` | `0` |
| `ε₁n`, `0 < ε₁ < ε*` | `θ_na(ε₁)` | `θ_hint(ε₁)` (Theorem 11.54) |
| `o(n)`, bounded below | `a` | `h` (**Theorem K3**, Corollary K3′(i)) |
| `→ 0`, `ln(1/ε) = o(n)` | `a` (Proposition K0, (E0′); lower bound Theorem 11.45) | `h` (**Corollary K3′(ii)**) |
| `e^{−λn}` | not studied | open (hinted: rows 4–6 of Theorem 11.25(d)) |

**Open.**
1. *Below the exponential scale.*  With a hint the cost at the zero function is `2ⁿ/|B(n,k*)|` up to a polynomial
   factor.  Without a hint the present upper bound is `e^{nh + o(n)}` with an unquantified `o(n)`; heuristically it is
   not better than about `n^{3/4}` (each bounded level loses `e^{O(√n)}` — the outer sample needs `r ≤ p_un_o − Θ(√n_o)`,
   Lemma K.4(d) and §6.3 — and `η → 0` needs `≈ 1/η` levels; the `o(n)` of the extensive family is not quantified
   either).  Whether an adaptive algorithm without a hint can reach `e^{nh + O(√n)}`, or even `poly(n)·2ⁿ/|B(n,k*)|`, and
   whether there is a lower bound of the form `e^{nh + ω(log n)}`, is open.  On the flat instance itself no level is
   needed — the doubling two-sample bracket of Proposition 11.46 stops there at the hinted cost up to a polynomial
   factor **[known]** — so any such lower bound has to come from non-flat instances.
2. *Depth.*  For this family of algorithms depth is necessary: `τ_k > h` for every `k`, with `(τ_k − h)/a ≈ 0.65/k²`
   **[numerical]**.  Is there a lower bound for a natural restricted class (bounded number of nested levels, or a
   bounded number of rounds of adaptivity) that matches `τ_k`?  For two levels the flat instance with inner cones
   attains `τ₂` for *this* algorithm (R7), which is not a lower bound for others.
3. *Instance by instance* (remark (4) of §11.18): unchanged.
4. *Exponentially small accuracies* (`ε = e^{−λn}`): the hinted exponents of rows 4–6 of Theorem 11.25(d) are not known
   to be attained without a hint.
5. *Other spaces* (remark (3) of §11.18): the new ingredient, Lemma 11.43(c), is again Harper's theorem on a
   sub-cube, so nothing new is required beyond what Theorem 11.52 uses.

---

## 8. Prior art (search log)

Web searches on 25 Nov 2026 (generic queries, no project information); **everything below was read as
search-engine summaries only — no full text, no abstract page was opened.**

| query | what came back | bearing |
|---|---|---|
| adaptive versus non-adaptive Monte Carlo, normalising constant, Lipschitz log-density, query lower bound | Mathé–Novak 2007 (simple Monte Carlo vs. Metropolis; already in `L7`); Ge–Lee–Lu 2020; adaptive complexity of log-concave sampling (2024, parallel rounds) | nothing on a bounded-accuracy adaptive exponent |
| nested sampling, rigorous non-asymptotic error bound, layer-cake estimator, certified relative accuracy | Chopin–Robert 2010; Fowlie et al. 2022; two 2026 preprints on nested sampling (heuristic coverage bounds; quadrature-error bounds) | asymptotic or heuristic; assume a constrained sampler |
| Dagum–Karp–Luby–Ross, optimal Monte Carlo estimation, stopping rule | SIAM J. Comput. 2000: `(ε,δ)` relative-error estimation of the mean of a `[0,1]`-valued variable, instance-optimal number of samples | the classical relative-error problem for *exactly observed* samples; here each sample (a fibre average) is itself only bracketed, at a cost that depends on the bracket |
| partition function of a Lipschitz function on the Boolean cube, value queries, Harper | Barvinok (polynomials on the cube, computational), Chen–Nannicini 2024 (`1/ε²` lower bound) | not this problem |
| adaptive multilevel splitting, non-asymptotic worst-case relative error | Cérou–Guyader and co-authors: unbiasedness and asymptotic variance in the idealised case | no worst-case certificate |
| exceedance probability with interval-valued evaluations, refinement near a threshold | level-set estimation with Gaussian processes, threshold bandits | the idea "refine only near the level" is standard there; no connection to the present accounting found |

*Not found* (at this depth — "not found", not "new"): a relative-accuracy (bounded-ratio) certified estimator of a
mean from bracketed samples with a ladder of levels; the use of the *lower* isoperimetric bound (Lemma 11.43(c)) to
close such a ladder at constant relative accuracy.  The prior art recorded in `prior_art/L7` and in R7 §6 for the
extensive case applies unchanged.

---

## 9. What I did not check

* **(R)** Theorem 11.53 (convergence of the exact recursion) is taken from the repository (machine-checked there, for
  the cube since `4cef47e`; I compiled against it and added the Lean proof that the exact sequence satisfies its
  hypotheses, but did not audit the repository's proof beyond its statement and its axioms).  The assembly of the
  extensive levels is Proposition E of this report — a paper proof, not machine-checked and not simulated beyond
  one level; it does not use the left-limit induction of Theorem 11.54 / R7 §5, which I did not re-verify.
* **(LB)** Theorem 11.25(a), Harper's theorem, the Chernoff/Hoeffding bounds and the binomial median are quoted, not
  re-proved; (H) and (Me) from memory.
* Theorem K1 is a paper proof.  Machine-checked: the algebra of the width and of the count, the lower Riemann sum,
  the contraction.  Simulated: every claim, with a simulated inner oracle, on enumerated cubes and radial landscapes
  with `n_o ≤ 44` (§6.2) and on radial landscapes with `n_o ≤ 600` and samples up to `4.6·10^{18}` points (§6.8), and for
  `n ≤ 14` with real inner brackets (§6.5).  At large `n` the cost was evaluated exactly at the flat instance only
  (§6.4), and the outer loop in expectation on radial and additive outer landscapes only (§6.6; no inner costs
  there); no run with three nested levels; non-radial outer landscapes with real fluctuations only on `Q_8 × Q_4`.
* The statement about populated levels in §5(2) is a sketch (with numerics).  Corollary K3′(ii) is proved only as
  far as the uniform bookkeeping of §3.2 and §3.4 is right; it was not simulated separately.
* The numbers of §6.1 depend on grids; the one-sided mode is rigorous only up to floating point.
* Prior art: search summaries only.
* The repository changed twice during the work (R7 integrated; `CubeHintPair.lean` added); I re-read §11.18 and R7 at
  `78ed930`, read the statements of `CubeHintPair.lean` that I use at `4cef47e`, and did not re-read the harness, the
  benchmarks or workstream L's report.

## Appendix: files

`REPORT.md`; `klib.py`, `test_klib.py`, `check_tail_lemmas.py`; `closure_window.py`; `recursion_bounded.py`; `sim_outer_loop.py`;
`sim_grouped.py`, `stable_multinomial.py`; `flat_cost_bounded.py`, `crosscheck_flat.py`; `radial_trajectory.py`; `e2e_small.py`;
`KBounded.lean`, `KBoundedLink.lean`, `KExactRecursion.lean`,
`KBoundedCube.lean`; outputs `out_*.txt`, logs `log_*.txt` (the console output of the full runs, with timings).

---

## Summary (at most 40 lines)

1. RESULT.  **Conjecture K is true in its strong form.**  Theorem K3 [proved, given Thm 11.25(a) (hinted lower bound) and Thm
   11.53 (convergence of the exact level recursion), both machine-checked in the repository]: for every `u > 0`, every FIXED
   `ε > 0`, `0 < δ < ½` the adaptive exponent without a hint is exactly `h = KL(Λ₁/u‖½)`.  Tool, Theorem K1 [proved, explicit
   constants; paper proof, unrefereed]: Algorithm 2L⁺ = the two-level algorithm of Thm 11.52 with (a) lower end
   `max(ℓ, layer-cake SUM over populated levels)`, (b) the Harper lower bound of the two-sided tail lemma 11.43(c) added to `ℓ`
   at every populated level, (c) negligibility factor `≥ 2e^u n_o/θ`, (d) Chernoff `1±η`, ladder ratio `e^λ`,
   `ℓ₀ = e^{−ψ₀}((1+e^{−u})/2)^n`.  Bracket ratio `≤ e^b(e^λ(1+η)/(1−η) + η′ + θ) + (2p_u)^n`, `b` = inner accuracy: a level costs an
   ARBITRARILY SMALL constant of accuracy.  Cost `≤ 1 + 2M̄ + Σ_l min(2M̄, (J+1)cnt(x_{l−1}))·C_l`, `M̄ = poly·2^{n_o}/|B(n_o, r†)| =
   e^{φan + O(√n)}` (Lemma K.4), `cnt(x) = poly·e^x` (the two `e^b` cancel as in 11.52).  One more level at bounded accuracy (Thm
   K2): `R[T](0) = inf_φ sup_{γ≥0}[min(γ, φa) + (1−φ)T(γ/(1−φ))]`, i.e. (11.18.2) at `g = β = 0`; never below `h` (the test of D45),
   and `→ h`: `t′ ≤ max(φa + (1−φ)T(ξ), (1−φ)(ξ + t))` with `T(ξ) ≤ h + η` at one small extensive rate (Proposition E: the
   extensive levels assembled from Thm K1 without the left-limit induction of Thm 11.54 / R7 §5).
2. SKETCH.  (1) sum-form lower end: CORRECT (and necessary; add the reference bound for `s₀`).  (2) closure window: WRONG as a
   mechanism — `Γ̃ ≥ 4e^u(e^u−1)` everywhere and `≈ c√n` at `p_u n`; the window is empty unless `G−b ≥ ln(16e^u(e^u−1))`, its upper
   end is `ρ₊ < p_u` (outer exponent `φKL(ρ₊‖½) > φa`), and populated levels never sit in it (they sit within `O(√(n log n))` of
   `p_u n_o`: [sketch + numerical]); repaired by (b), (c): populated levels close at every `r ≤ p_u n_o − O(√n_o)`, unpopulated
   ones at every `r ≤ p_u n_o`.  (3) recursion: CORRECT.  (4) "`O(1)` per level": true of the sketched algorithm, NOT NECESSARY —
   hence the strong form.  (5) base family: conclusion right (exponent `a` at every fixed accuracy, Prop. K0), reason wrong
   (`3 + 12Γ(r)` is not bounded up to `p_u n`; the two-sided lemma 11.43(c) is what works).
3. NUMERICS (all pass; `ulimit -v 4000000`; each < 10 min).  `python3 recursion_bounded.py` (152 s): `T_k` on `[0, ε*]` incl. `g = 0`,
   40 levels, `u = ½, 1, 2`: `τ_k/a = 0.5006, 0.361, 0.311, 0.290, 0.280, …, 0.2631` (`u = 1`; `h/a = 0.2627`), never below `h`, rigorous
   one-sided value `τ_40 ≤ 1.027h`, `(τ_k − h)/a ≈ 0.65/k²`.  `python3 sim_outer_loop.py` (4 min): outer loop of 2L⁺, simulated
   adversarial inner oracle, constants of the theorem, 394 runs (`Q_8×Q_4` enumerated; radial `n_o ≤ 44`): no claim of Thm K1
   violated; 5 mutations all detected.  `python3 sim_grouped.py` (4 min 51 s): the same in the bounded regime at medium size
   (radial, `n_o ≤ 600`, exact samples up to `4.6·10^{18}` points): 1325 runs, 864 negligible levels, 0 violations, 4 mutations
   detected.  `python3 closure_window.py` (2 s): Lemma K.4 on tables `n ≤ 12 800`, the window.  `python3 flat_cost_bounded.py`
   (49 s): exact cost at the flat instance, accuracy 0.87: `ln(cost)/(na) = 1.70, 0.70, 0.55, 0.52, 0.51` at `n = 250 … 6.4·10⁴`
   (limit `τ₂/a = 0.5006`; plain bracket `1.93 … 1.03`; hinted lower bound `0.33 … 0.26`, never undercut).
   `python3 radial_trajectory.py` (145 s): outer loop in expectation, 17 radial + 5 additive landscapes, `n_o ≤ 16 000`, 630 runs,
   0 violations.  `python3 e2e_small.py` (5 min 8 s): the WHOLE two-level algorithm with real inner brackets on `Q_12`–`Q_14`:
   84 runs, `1.05·10⁷` inner brackets, all valid and within the width bound.  Lean (≤ 10 s each, standard axioms): `KBounded.lean`,
   `KBoundedLink.lean`, `KBoundedCube.lean`, `KExactRecursion.lean` — contraction at accuracy 0, exact recursion → `θ_hint`, width, count.
4. STRONG FORM / LOWER BOUNDS.  Nothing further is needed for every fixed `ε > 0` (Theorem K3); the same exponent holds for
   `ε_n → 0` with `ln(1/ε_n) = o(n)` (Cor. K3′).  There is NO lower bound above `h` at the exponential scale at any such accuracy.
5. OPEN: sub-exponential factors (`e^{nh+o(n)}`, `o(n)` unquantified, against `poly·2ⁿ/|B(n,k*)|` with a hint); whether a bounded
   number of levels or rounds reaches `h` (`τ_k > h` for all `k`); exponentially small accuracies; instance-by-instance comparison.
   NOT CHECKED: Thm 11.25(a), Thm 11.53, Harper, Chernoff/Hoeffding, the binomial median are quoted; Thm K1, Prop. E are paper
   proofs (machine-checked: the algebra and the contraction; simulated: every claim of K1, but only with a simulated oracle
   — `n_o ≤ 600` radial, `Q_8×Q_4` general — and end to end for `n ≤ 14`; large `n` only flat-exact and in expectation; no
   three-level run); "populated levels sit near `p_u n_o`" is a sketch; prior art from search summaries only.
