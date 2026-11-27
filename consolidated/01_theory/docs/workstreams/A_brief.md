# Workstream A — the randomised exponent: an isoperimetric problem with two measures
Directory: <session scratch>/ws/A/

## Question
Decide (prove, refute, or delimit with strong evidence) the main open conjecture: on product
spaces `X = Sⁿ` with product Gibbs measure `πⁿ` and additive slack `s_n(x,y) = Σ_i s(x_i,y_i)`,
the randomised query complexity of `ln Z` at an additive instance has exponent exactly
`R^rand_β(ε₁) = max_P R(P; s, (E_P[Λ₁]+ε₁)/β)` — i.e. *single dips are the extremal sensitive
perturbations at the exponential scale*.

Exact combinatorial form.  A set `D ⊂ X` is *sensitive* at level `η` if
`E_π[e^{β h_D} − 1] ≥ η`, `h_D(y) = min_{x ∉ D} s(x,y)` (the largest admissible perturbation
supported in `D`).  `FC` = fractional hitting number of the sensitive sets
(= `1/max_q min_D q(D)`).  Proved: `FC ≥ FC_dip` (balls `{a : s(a,y) < c_y}` at critical depth),
and `FC ≤ E_π[e^{Λ}]·(1+η)/η`.  Level-set reformulation: for an admissible `h ≥ 0` the set
`{h > r}` has `π`-measure about `η e^{−βr}` for some `r`, and `supp h` contains its `r`-blow-up; so
the problem is: *minimal `q`-measure of the slack-`r`-neighbourhood of a set of `π`-measure
`e^{−βr}`*, minimised over `r`, maximised over the sampler `q`.

## Suggested lines (you choose)
1. Literature: asymptotic isoperimetry on product spaces at the large-deviation scale
   (Ahlswede–Gács–Körner blowing-up; Ahlswede–Zhang "Asymptotical isoperimetric problem";
   Alon–Boppana–Spencer; Bollobás–Leader for the biased cube; Marton; generalised Harper
   theorems for non-uniform measures / other alphabets).  Is the two-measure blow-up exponent a
   known single-letter formula?
2. Exact small-`n` computation with symmetry reduction (biased cube `f(x) = e|x|`; ternary
   alphabets): the optimal sampler is permutation-invariant; compute `FC` exactly for `n` as
   large as you can (orbit LPs, constraint generation with an ILP/greedy oracle for the
   adversary's best response) and compare the growth rate with `R^rand_β` and `U_β`.
3. A proof for the binary alphabet (biased cube, Hamming slack), or a counterexample family
   (unions of dips, cylinders, type-class slices, "weighted balls") whose exponent beats dips.
4. If the conjecture is false: the true single-letter formula, or the best bounds you can prove.
