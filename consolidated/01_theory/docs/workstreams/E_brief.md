# Workstream E — second-order classes: how many evaluations are really needed?
Directory: <session scratch>/ws/E/

## Setting
`X = ∏_i σ_i` (start with `{0,1}ⁿ`).  Second-order class: all `g` with
`|g(x^{i→a, j→b}) − g(x^{i→a}) − g(x^{j→b}) + g(x)| ≤ c_ij` for all `x`, `i ≠ j`, `a`, `b` (bounded mixed
second differences; `c ≡ 0` is the additive functions).  Known (theory report §11.7; Lean
`SecondOrderEnvelope.lean`, `HigherOrderEnvelope.lean`): with `g` evaluated on the star of `x₀`
(`x₀` and its single-site neighbours), the consistent residuals are exactly sandwiched by
`g_star ∓ Σ_{i<j changed} c_ij` (both extremes are class members).  Negative (second referee,
`DEAD_ENDS.md` D32): with dense constants `c_ij = c` the remainder is quadratic in the Hamming
distance; `−c·C(|x|−1, 2)` is in the class and vanishes on the whole radius-2 ball; an explicit
member vanishes on two opposite stars.

## Questions
* With dense constants and known part `f(x) = e|x|` (or general additive `f`), what is the least
  number of evaluations `N₂(n)` that certifies the minimiser / the minimum to within `ε`, for
  the *best* evaluation set?  Polynomial or exponential in `n`?  Give lower bounds (adversarial
  class members, "second-order dips", packing arguments) and upper bounds (designs: covering
  arrays, radius-`r` balls, random sets, Reed–Muller-type structures), and exact values for
  small `n` (the class is a polytope: given an evaluation set with data, the extreme values at
  a point are linear programs).
* The class is a neighbourhood of the affine (degree-1) functions — relate to local
  decoding/correction of low-degree functions, to polynomial interpolation on the cube, to
  designs; is there a clean characterisation of the evaluation sets that determine `g` up to
  `O(c)` everywhere (a "second-order covering" notion)?
* Sparse constants (`c_ij ≠ 0` only on a graph of bounded degree, e.g. a chain): what replaces
  the star?  Is the cost governed by the graph (treewidth, degree)?
* Order `m` in general, if the order-2 picture becomes clear.
Deliver exact small-`n` data, the best lower and upper bounds you can prove, and a conjecture
for the truth if they do not meet.
