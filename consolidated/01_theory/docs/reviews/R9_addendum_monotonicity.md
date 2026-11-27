> **Repository note.**  The addendum sent to referee R9 during its review (the coordinator's proof of
> Proposition 11.65(b), then unrefereed), as sent.  The referee's verdict: proved, with four presentational
> remarks, which are applied in theory report §11.20.

# Addendum for referee R9: a proof by the coordinator that the exponents decrease with the field

This replaces the numerical statement F10(b) of the report.  Notation: Theorem F2(b) of the report (cosh form): with the total field `x = θ + γ`, `C(x) = 2cosh(x/2)`, the game function is `F(γ,t) = ln[I_θ(θ+γ)/C(θ+γ)^t]`, `I_θ(x) = [sinh(t(θ+u−x)/2)·C(θ−u)^t + sinh(t(x−θ+u)/2)·C(θ+u)^t]/sinh(tu)`; `F*(t;θ) = max_{|γ|≤u} F(γ,t)`.  A numerical check of every step is in `experiments/coordinator_checks/field_monotone_proof_check.py` (do not rely on it; re-derive).

(b) *A field always helps, and the hardest residual always
works against it.*  For every `0 < t < 1` the function `θ ↦ F*(t; θ)` is even and strictly
decreasing on `[0, ∞)`, and its maximiser has `γ*·θ < 0` for `θ ≠ 0`.  Hence `R^max(e; θ)`, the class
threshold `E(θ)`, `θ_na(x; θ)` and `a(θ)` are nonincreasing in `|θ|`: the uniform cube is the
hardest case, for adaptive and for non-adaptive algorithms.  (The workstream had this as a
numerical observation on a grid of 121 fields, and `γ*θ < 0` to first order.)
*Proof of (b)* (every step checked numerically: `experiments/coordinator_checks/field_monotone_proof_check.py`).
Write `x = θ + γ` for the total field and, in the cosh form of Theorem 11.59(b),
`F(γ,t) = ln ρ_θ(θ+γ)` with `ρ_θ = I_θ/C^t`, where `I_θ` solves `I″ = (t/2)²I` on the window `[θ−u, θ+u]` and
equals `C^t` at its ends.  (i) Since `(C^t)″ = (t/4)C^t[1 − (1−t)tanh²(x/2)]`, the ratio satisfies

    ρ″ + t·tanh(x/2)·ρ′ + (t(1−t)/4)·sech²(x/2)·ρ = 0,        ρ = 1 at both ends,   ρ > 0.

At a critical point `ρ″ < 0`, so every critical point is a strict local maximum: there is
exactly one, `x* = θ + γ*`, and `F*(t; θ) = ln ρ_θ(x*)`.  (ii) Let `A_u ∈ (0, 1)` be the average of `tanh`
over `[(θ−u)/2, (θ+u)/2]`, `θ > 0`.  Then `∂_γF(0,t) = (t/2)[tanh(tuA_u/2)/tanh(tu/2) − tanh(θ/2)]`; the
quotient is increasing in `t` (convexity of `sinh`) and equals `tanh(θ/2)` at `t = 1`, so the
derivative is negative for `t < 1`, and by (i) `γ* < 0`.  (iii) `γ*` is a nondegenerate interior
maximum, so by the envelope theorem `dF*/dθ` is the partial derivative in `θ` at `γ*`; inserting
the first-order condition and `cosh a ± sinh a·tanh b = cosh(a ± b)/cosh b`, the inequality
`dF*/dθ ≤ 0` becomes

    ln cosh Q − ln cosh P  ≥  (1−t)·[ ln cosh((θ+u)/2) − ln cosh((θ−u)/2) ],
    P = (θ−u)/2 + t(u−γ*)/2,     Q = (θ+u)/2 − t(u+γ*)/2,

that is: *the average of `tanh` over `[P, Q]` is at least its average over
`[(θ−u)/2, (θ+u)/2]`*.  The first interval lies inside the second, has length `(1−t)u`, and its
centre `(θ − tγ*)/2` is to the right of `θ/2` because `γ* < 0`.  (iv) For an odd increasing
function `f` that is concave on `[0, ∞)` and `c ≥ 0`, the average of `f` over `[c−r, c+r]` is
nonincreasing in `r` (for `r ≤ c` by concavity; for `r > c` it is `(2r)^{-1}∫_{r−c}^{r+c} f`, whose
derivative has the sign of `r[f(r+c) − f(r−c)] − ∫_{r−c}^{r+c} f ≤ (r−c)f(r+c) − (r+c)f(r−c) ≤ 0`,
by the trapezoid bound for a concave function and because `f(x)/x` is nonincreasing).  So a
sub-interval with the same centre has at least the average of the whole interval, and
moving it to the right increases its average.  The statements about `R^max`, `E`, `θ_na` and `a`
follow because each is a pointwise nondecreasing functional of `F*`
(`θ_na(x) = sup_{τ<1}(F*(τ) − τx)/(1 − τ)`).  ∎
