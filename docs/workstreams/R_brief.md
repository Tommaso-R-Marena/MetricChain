# Workstream R — the rate of the level recursion: tangent lines, a saddle-node, `2π²`

*Brief written by the coordinator on 2026-11-26, after the twenty-second checkpoint of
cycle 10.  A paper-proof workstream with certified numerics; no Lean (a separate small
Lean task covers the two line lemmas of §2.2 and §2.6).*

## 1. Where we are

Theory report §11.18 (Theorems 11.52, 11.53 and the remark "a rate for the recursion"),
§11.19 remark (1).  The level recursion on exponent functions `T: (0, ∞) → [0, ∞)`:

    R[T](g) = inf_{0<φ<1, 0<β<g}  sup_{γ ≥ β} [ min(γ, μ) + (1 − φ)·T(γ/(1 − φ)) ],    μ = φ·θ_na((g − β)/φ),
    T_1 = θ_na,   T_{k+1} = min(T_k, R[T_k]),   τ_k = sup T_k = T_k(0+)

(in Lean: `BoundedAccuracy.exactRec`, index shifted by one).  The pair `(θ_na, θ_hint)`:

* **cube**, slope `u`: `κ(ρ) = KL(ρ‖½)`, `e(ρ) = KL(ρ‖p_u)`, `y(ρ) = uρ − Λ₁ = e(ρ) − κ(ρ)`,
  `p_u = 1/(1+e^u)`, `Λ₁ = ln(2/(1+e^{−u}))`; `θ_na(e(ρ)) = κ(ρ)` for `ρ ∈ [p_u, ½]` (zero from
  `ε* = e(½)` on), `θ_hint(y(ρ)) = κ(ρ)` for `ρ ∈ [ρ_h, ½]`, `ρ_h = Λ₁/u`, `h = κ(ρ_h)`, `a = κ(p_u)`;
* **Gaussian** (small-slope limit): `θ_na(e) = (1 − √e)²`, `θ_hint(y) = (1 − y)²/4`, `a = 1`, `h = ¼`,
  `ε* = 1`.

Known: `T_k ↓ θ_hint` **[V]**; `τ_k − h ≤ c₁/(k + c₂)` **[V]**; numerically `(τ_k − h)/a ≈ 0.65/k²` at
`u = 1` **[N]**.  Theorem 11.58a turns the rate `c₁/k` and a loss `O(ln n)` per level into
`ln N ≤ n·h + O(√(n ln n))`; a rate `C/k²` would give `n·h + O(n^{1/3}(ln n)^{2/3})`.

## 2. The coordinator's findings of 2026-11-26

Status: **§2.2 and §2.6 are proved below (short proofs; check them); the rest is
heuristic, with numerics that agree to three digits.**  Scripts and outputs:
`experiments/coordinator_checks/level_rate/` (read its `README.md`).

### 2.1 The window form

With `S(x) = x + T(x)`, `T` nonincreasing: for `μ ≥ β` the supremum over `γ` equals
`(1 − φ)·sup{S(x) : β/(1−φ) ≤ x ≤ μ/(1−φ)}`, and for `μ < β` it is `μ + (1−φ)T(β/(1−φ))`.  At accuracy
zero: `τ′ = inf_φ (1 − φ)·sup_{0 < x ≤ φa/(1−φ)} S(x)`.  If `S` is nondecreasing the supremum sits
at the upper end — the rung at which *all* outer points are refined — and with
`e = g/φ` (the outer accuracy rate, `β → 0`), `X = g·θ_na(e)/(e − g)`:

    T′(g) ≤ inf_{e > g} (1 − g/e)·S(X)  =  inf_{e>g} [ (g/e)·θ_na(e) + (1 − g/e)·T(X) ].        (2.1)

### 2.2 Lemma L (minorant lines propagate) — proved

*Let `θ_na ≥ 0`, `0 ≤ σ ≤ σ′`, and `T(x) ≥ B − σx` for all `x > 0`.  If
`B − (1 − σ)·θ_na(e) ≤ σ′·e` for every `e > 0`, then `R[T](g) ≥ B − σ′g` for every `g > 0`; hence
`min(T, R[T])(g) ≥ B − σ′g`.*

Proof.  Fix `φ, β` and let `e′ = (g − β)/φ > 0`, `μ = φθ_na(e′)`, `γ₀ = max(β, μ)`.  The bracket at
`γ₀` is `μ + (1−φ)T(γ₀/(1−φ)) ≥ μ + (1−φ)B − σγ₀`.  If `μ ≥ β` this is
`(1−φ)B + (1−σ)φθ_na(e′) ≥ (1−φ)B + φB − σ′φe′ = B − σ′(g − β) ≥ B − σ′g`.  If `μ < β` it is
`φθ_na(e′) + (1−φ)B − σβ ≥ (1−σ)φθ_na(e′) + (1−φ)B − σβ ≥ B − σ′(g−β) − σβ ≥ B − σ′g`.  ∎

The least admissible `σ′` is the **slope map**

    Σ_B(σ) = sup_{e>0} [B − (1 − σ)·θ_na(e)]/e ,      Σ_B(σ) − σ = sup_ρ [B − κ(ρ) − σ·y(ρ)]/e(ρ),

finite iff `B ≤ (1 − σ)·a` (*regular* lines).  With the concave function
`J(t) = min_ρ [κ(ρ) + t·y(ρ)]` — for the cube `J(t) = Λ(tu) − tΛ(u)`, `Λ(v) = ln(2/(1+e^{−v}))`; for
the Gaussian pair `J(t) = t − t²` —: `θ_hint(x) = sup_t [J(t) − tx]`, `h = max J = J(L_h)`,
`L_h = −θ_hint′(0)`, `J″(L_h) = −1/θ_hint″(0)`; the tangent lines of `θ_na` are
`(B, s)` with `B = (1+s)·J(s/(1+s))`; and `σ′ = Σ_B(σ)` is the solution of

    (1 − σ + σ′)·J( σ′/(1 − σ + σ′) ) = B.                                                   (2.2)

For the Gaussian pair this is the **Möbius map** `σ′ = B(1 − σ)/(1 − σ − B)`: fixed points
`(1 ± √(1 − 4B))/2`, parabolic at `B = h = ¼` (`σ = L_h = ½`), elliptic for `B > h` with rotation
angle `θ`, `2cos θ = (1 − 2B)/B`, i.e. `θ ≈ 4√(B − h)`.

**Consequence (lower bound for the recursion).**  Let `(B, s₀)` be a tangent line of
`θ_na` (convex) with `s₀ ≤ 1`, and `s_{j+1} = Σ_B(s_j)`.  If `s_j ≤ 1 − B/a` for all `j ≤ k − 2`, then
`T_k(x) ≥ B − s_{k−1}x` and **`τ_k ≥ B`**.

### 2.3 The saddle-node and the constant

For `B < h` the map `σ ↦ Σ_B(σ)` has a stable fixed point `σ_−(B) < L_h` (the tangent lines
of `θ_hint`: `J(σ_−) = B`) and an unstable one above `L_h`; they merge at `B = h`.  For
`B = h + δ` there is none: near `σ = L_h`

    Σ_B(σ) − σ  =  [δ + h − J(σ)]/e(ρ(σ)) (1 + o(1))  =  δ/h + (σ − L_h)²/(2·θ_hint″(0)·h) + … ,

the slope passes the bottleneck in `π·√(2θ_hint″(0)h²/δ)·(1 + o(1))` levels (the tangent
solution; the classical ghost of a saddle-node), and the lines of `θ_na` with `B` near `h`
start below it (`s₀ < L_h` because `θ_na > θ_hint`).  Hence the

**Conjecture R.**  `lim_k k²·(τ_k − h) = 2π²·h²·θ_hint″(0)` — for the cube
`2π²h²/(u²ρ_h(1 − ρ_h))` (`= 0.6412·a` at `u = 1`), for the Gaussian pair `π²/16`.

The lower half (`liminf ≥`) should follow rigorously from §2.2.  Numerically
(`iterate_exact.py`, interpolating grid, not one-sided): Gaussian pair
`k²(τ_k − h)/(π²/16) = 0.9960, 0.9982` at `k = 100, 160`; cube `u = 1`: `0.990` at `k = 55` and rising
like `1 − c/k`; the scaled profile `k²(T_k − θ_hint)(ζh/k)/(h²θ_hint″(0))` converges to the same
function `f(ζ)` for both pairs.

### 2.4 The same thing in primal variables (heuristic)

For small accuracy and small defect `D_k = T_k − θ_hint`, (2.1) is a discrete Hopf–Lax
step: `D_{k+1}(g) ≈ min_X [(1 − g/h)·D_k(X) + q(X − g)²/(2g)]`, `q = h·θ_hint″(0)`, i.e.
`∂_k D = −x[D/h + (∂_x D)²/(2q)]`, with the similarity solution `D = (qh/k²)·f(kx/h)`,
`ζf′²/2 + ζf′ + (ζ − 2)f = 0`, selected by its passage through the folded saddle
`(ζ, f) = (3, 3/2)`: `f(0) = 2π²` (`ode_f0.py`: `19.7392088`).  In absolute variables a nest is a
path `G(s)` (accuracy of the level whose inner dimension is `s`), the excess exponent is the
Dirichlet energy `½θ_hint″(0)∫_0^n G′(s)² ds`, the number of levels is `h∫_0^n ds/G(s)`, and with
`W(ρ) = kG(ρn)/(hn)` the problem "minimise `∫_0^1 W′² dρ` subject to `∫_0^1 dρ/W = 1`,
`W(0) = W(1) = 0`" is radial Kepler motion `W″ = −c/W²` over one period: the optimal profile
is a cycloid and the minimum is `4π²` (virial theorem).  So: accuracies rise from the
base, peak when half of the coordinates are inside, and fall back to the bounded
accuracy at the top; every level's outer accuracy rate is close to `h`.

### 2.5 What the upper bound needs — and a trap

A *majorant* `M ≥ T_k` with `x + M(x)` nondecreasing gives `T_{k+1} ≤ (2.1)` with `S = S_M`.  If
`M` is convex with slopes in `[−1, 0]`, written as the envelope of its lines,
`(1 − g/e)S_M(X) = sup_lines [B − g·(B − (1−s)θ_na(e))/e]`: with a **common** `e` every line
`(B, s)` becomes the line `(B, [B − (1−s)θ_na(e)]/e)`.  By Sion's minimax theorem (the bracket is
affine in the line and quasi-convex in `e`) the infimum over `e` commutes with the
supremum over lines, so the majorant recursion is again the slope map, line by line —
as long as the image stays in the class.  It does not: (i) a line whose slope reaches
`[1 − B/a, 1]` can be dropped at accuracy zero (`τ′ ≤ sup_lines min(B, (1−s)a)`), but a line
may jump over this window to a slope `> 1`; then `S` is not monotone near zero, the
supremum of the window sits at its lower end, and the monotone hull
`hull(F)(x) = sup_{y≤x}(y + F(y)) − x` has to be taken (it creates a kink whose pencil of lines
re-enters the dynamics; at `k = 3` of the Gaussian pair this gives `τ₃ = 0.3573`, which is
what the grid recursion gives, while the naive line formula would give `⅓`: **the naive
formula is not an upper bound**); (ii) a line `B − sx` is a majorant only on a range.
**Single-line epochs** — a flat line `(B, 0)`, slope steps at the *optimal* outer rate until
it can be dropped, then a drop: the calculus of Theorem 11.58a with `e` optimised — give
only `B_k − h ≈ C/k` (`epochs.py`): the range of the line at the bottleneck is `O(√δ)`, the
drop per epoch of `δ^{−1/2}` levels is `δ^{3/2}`.  The `1/k²` law needs the lines with all
intercepts in `(h, τ]` to pass the bottleneck **in parallel**.  A finite family with
geometrically spaced intercepts (`O(log k)` lines) should give `C′/k²` with `C′` a constant
factor above the sharp constant.

### 2.6 Lemma M (majorant lines on a range, one step) — proved

*Let `T` be nonincreasing with `T(x) ≤ M(x)` for `0 < x ≤ R`, where `x + M(x)` is nondecreasing on
`(0, R]`.  Let `g > 0`, `0 < φ < 1`, `e = g/φ`, `θ_na` continuous at `e`, `μ = φθ_na(e) > 0` and
`X = μ/(1 − φ) ≤ R`.  Then `R[T](g) ≤ (1 − φ)·(X + M(X))`.*  (From `StepLE.of_limit`:
for `0 < γ ≤ μ`, `γ + (1−φ)T(γ/(1−φ)) ≤ (1−φ)S_M(γ/(1−φ)) ≤ (1−φ)S_M(X)`.)  For a line
`M(x) = B − σx`, `σ ≤ 1`: `T′(g) ≤ B − σ′g`, `σ′ = [B − (1 − σ)θ_na(e)]/e`, valid for `g ≤ R′ = Re/(θ_na(e) + R)`.

## 3. What to deliver

**A. The lower bound (must).**  From Lemma L, for the cube at every `u > 0` and for the
Gaussian pair: (A1) an explicit `c(u) > 0` with `τ_k − h ≥ c/k²` for all `k ≥ 2`; (A2)
`liminf_k k²(τ_k − h) ≥ 2π²h²θ_hint″(0)`; (A3) for the Gaussian pair the closed form that the
Möbius map gives (the exact lower bound `τ_k^{LB}` as a function of `k`).  Check Lemma L and
(2.2) first.  Everything that is used about the functions (convexity of `θ_na`, the
formula for `J`, the expansion at the bottleneck with an explicit remainder) proved, not
assumed.  Say exactly what the bound is a bound of: the recursion (the analysis), not
algorithms.

**B. The upper bound.**  (B1, must) *Certified numerics*: the recursion
`M_{k+1} = hull(min(M_k, P[M_k]))`, `P[M](g) = inf_{e>g}(1 − g/e)S_M(X)`, `M_1 = hull(θ_na)`, with the
accuracy-zero rule, is an upper bound of the exact recursion by Lemma M (prove this
statement, including the accuracy-zero value and the role of the hull).  Evaluate it in
a one-sided way (every computed number an upper bound up to rounding: say how the
grid, the interpolation and the infimum over `e` are made one-sided) for the Gaussian
pair and the cube at `u ∈ {½, 1, 2}`, as far in `k` as the resolution allows (aim at
`k ≥ 200`); tabulate `τ_k^{LB} ≤ τ_k^{grid} ≤ τ_k^{UB}` and the three values of `k²(τ_k − h)` against
`2π²h²θ_hint″(0)`.  (B2, should) *A proof* of `τ_k − h ≤ C/k²` for all `k`, with an explicit `C`,
by explicit majorants — a finite family of lines in parallel as in §2.5, or the convex
dual dynamics with the hull, or anything else that works; every inequality of the
induction also checked numerically.  (B3, could) `limsup_k k²(τ_k − h) ≤ 2π²h²θ_hint″(0)`, which
with (A2) proves Conjecture R.  If (B2) resists, the deliverable is the precise
obstruction and the best rate you can prove (`o(1/k)`?).

**C. The schedule in a form usable at finite `n`** (should; no finite-`n` analysis — that is
workstream Q2, Part B).  For the majorants of (B2): which outer rates `e` are used and
are they bounded away from `0` and `ε*`; how many lines; the ranges; where drops occur and
how many; so that "`k` levels of the kinds {slope step at rate `e ∈ [e₀, e₁]` on a
max-of-lines type; drop}" is a complete description with `B_k − h ≤ C/k²`.

**D. "What is not proved"**, the weakest link, and anything in the theory report,
`K_REPORT.md`, `Q_REPORT.md` or this brief that you find wrong on the way — including in
§2: the heuristics may be wrong in detail (the role of the layer near zero accuracy in
particular), and the coordinator's numerics are not one-sided.

## 4. Rules

* Create only `docs/workstreams/R_REPORT.md` and files under `experiments/workstreams/R/`
  (scripts with stored outputs; commands in the report).  Do not edit any existing
  file.  Do not run `lake` or `scripts/audit_all.sh`.  No git command that changes state.
  Do not start further agents.
* Every statement labelled: proved here / quoted (from where, with its status) /
  numerical (one-sided or not) / heuristic / conjecture.
* One Python process at a time, under about 1.5 GB; other work shares the machine (4
  cores).  Foreground `sleep` is not available; wait with bounded loops if you must.

## 5. What to report back

At most 40 lines: the theorems proved (with constants), what is certified numerically
and to which `k`, the status of Conjecture R, the schedule of part C, the weakest link,
errors found elsewhere, files created.

## Errata (added by the coordinator; the text above is left as it was briefed)

* §2.2, found by the Lean task LD (2026-11-26): "`Σ_B(σ)` finite iff `B ≤ (1 − σ)·a`" must be
  strict — at `B = (1 − σ)a` the supremum is `+∞` (the slope of `θ_na` at `0` is infinite; for the
  Gaussian pair the Möbius map has its pole at `σ + B = 1`).  Accordingly the Consequence
  needs `s_j < 1 − B/a`.  It also uses `s_j ≤ s_{j+1}` (Lemma L needs `σ ≤ σ′`), which is automatic
  for `B ≥ h`; and its hypothesis "`s₀ ≤ 1`" is not needed.
* Lemma L, the iteration along the exact recursion, the Möbius map of the Gaussian pair
  with its minimality, two numerical witnesses (`T_2(0+) ≥ 3/8`, `T_3(0+) ≥ 3/10` for the Gaussian
  pair) and Lemma M with the line step at a general outer rate are machine-checked:
  `proofs/Frontiers/LineDynamics.lean` (`line_le_Rstep`, `lines_le_exactRec`, `le_sSup_exactRec`,
  `gauss_slope_map`, `gauss_slope_map_least`, `gauss_lines_le_exactRec`, `gauss_level_two_ge`,
  `gauss_level_three_ge`, `StepLE.monotoneS_step`, `StepLE.line_step`, `StepLE.line_step_rate`).
