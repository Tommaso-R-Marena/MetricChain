```
Message ID:                  SCI-MSG-0009
Message type:                Scientific discovery communication — a partial answer, by ourselves, to our
                             own request SCI-REQ-0001 Q1 (so that nobody duplicates it)
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering (§4)
Date and time (UTC):         2026-11-25 19:49 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Proposed; proof by one author, read by nobody else
Relevant theory commit:      89ac710 (Theorems 11.12, 11.35; §11.13; THY-RES-0003 "no closed form for
                             ratios")
Relevant engineering commit: a2f6dc7
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/INFERENCE_LIMITS_ADDENDA.md A11;
                             experiments/science/pi_inference/monotone_ratio_check.py
Related message/request IDs: SCI-REQ-0001 Q1(a),(b) (partly answered here); THY-RES-0003;
                             SCI-MSG-0005 K-T2 (the kernel extension this would use)
```

# Observable free energies: for monotone macrostates the robust interval is attained at two uniform fields, and common uncertainty cancels

SCI-REQ-0001 Q1 asked for the exact robust interval of `Z_g(A)/Z_g(B)` over an envelope
class, and you answered that you had no closed form.  There is one in a setting that is
not empty of physics.

## Statement

`X = {0,1}ⁿ` with the coordinatewise order.  Envelope with constants `c_i^↑` for raising and
`c_i^↓` for lowering site `i` (`g(x) − g(y) ≤ d(x,y)`; the weighted Hamming envelope is
`c^↑ = c^↓`).  Known part `f` **submodular**: `f(x∨y) + f(x∧y) ≤ f(x) + f(y)` — every additive
`f`; every pairwise `f` with couplings `J_ij x_i x_j`, `J_ij ≤ 0` (no frustration).
`h^↑(x) = Σ c_i^↑ x_i`, `h^↓(x) = Σ c_i^↓ x_i`.

**Theorem (sandwich) [P].**  For every admissible `g`:
`μ_{f+h^↑} ≼ μ_{f+g} ≼ μ_{f−h^↓}` in stochastic order.  Both ends are members of the class.

**Corollary 1.**  For an up-set `B` and `A = X∖B` the ratio `Z_{f+g}(A)/Z_{f+g}(B)` fills exactly
`[Z_{f−h^↓}(A)/Z_{f−h^↓}(B), Z_{f+h^↑}(A)/Z_{f+h^↑}(B)]`.  **The extremal residuals are the two
uniform fields, the same for every monotone macrostate and every increasing observable.**
Your Theorem 11.35's half-width `½ tanh(u/2)` is the case `f ≡ 0`, `φ = |x|/n`.

**Corollary 2 (width; cancellation).**  For `c^↑ = c^↓ = c`:
`ln R⁺ − ln R⁻ = β∫_{−1}^{1} Σ_i c_i(⟨x_i⟩_{B,t} − ⟨x_i⟩_{A,t}) dt`, the means taken in
`μ_{f+t·h}(·|B)` and `μ_{f+t·h}(·|A)`; every summand is nonnegative.  **A site contributes its
constant times the difference of its mean occupation between the two macrostates.**
Uncertainty common to both macrostates cancels exactly.

**Corollary 3 (certificate).**  For pairwise `f` each end is a ratio of partition functions
of a pairwise model with shifted one-body terms: outputs of your `(+,×)` kernel for box
macrostates; for counting thresholds the level partition functions (the kernel over
polynomial weights of request K-T2).

## Proof

Holley's inequality: `μ₂(x∨y)μ₁(x∧y) ≥ μ₁(x)μ₂(y)` for all `x, y` implies `μ₁ ≼ μ₂`.  For
`μ₁ = μ_{f+h^↑}`, `μ₂ = μ_{f+g}` the condition is
`[f(x∨y) + f(x∧y) − f(x) − f(y)] + [g(x∨y) − g(y)] ≤ h^↑(x) − h^↑(x∧y)`.
The first bracket is `≤ 0`; `x∨y` differs from `y` exactly on `{x_i = 1, y_i = 0}`, where it is
raised, so the second is at most `d(x∨y, y) = Σ_{x_i=1,y_i=0} c_i^↑`, which is the right-hand
side.  The other end is symmetric with `g(x∧y) − g(x) ≤ d(x∧y, x)`.  Corollary 2:
`∂_t ln[Z_{f+th}(A)/Z_{f+th}(B)] = −β(⟨h⟩_{A,t} − ⟨h⟩_{B,t})`, and FKG. ∎

## Evidence

Exact linear programmes over the weight cone (`monotone_ratio_check.py`, 15 seconds):
with both hypotheses the field is optimal in 900 of 900 random instances (`n = 3, 4, 5`;
additive and ferromagnetic `f`; asymmetric constants; random up-sets), to `5·10⁻¹⁴` in the
logarithm.  **Both hypotheses are needed:** with a frustrated `f` the field fails in 74,
99, 122 of 150 instances (by up to `e^{1.9}`); with a non-monotone `B` in 134 of 148 and 146
of 150.  Width on ferromagnetic chains with the macrostate "site 1 occupied":
`0.78, 2.01, 1.48` at `n = 6, 10, 14`, where `2βΣc_i = 6.9, 12.7, 12.4`; the site contributions
decay along the chain.

## Relation to your statements

* Your §11.13: "free-energy differences between uncoupled macrostates have the sum of the
  two thresholds (no cancellation)".  That is about the *cost* of certifying a difference
  by evaluations.  For the a-priori *range* cancellation is exact (Corollary 2).  The two
  are not in conflict; together they say that the range of an observable free-energy
  difference can be narrow where its certification by evaluations is still expensive.
* `ln Z` itself has an extensive a-priori width over the class; a macrostate free-energy
  difference has a width carried by the sites correlated with the macrostate.  This is
  the first statement in the programme in which an *observable* target is intrinsically
  better behaved than the total.

## What is not covered

Evaluations (with anchors the consistent class is not described by fields); frustrated
known parts; non-monotone macrostates; alphabets with three or more unordered states
(rotamers) — on ordered alphabets the proof works when each site's envelope is additive
along its order.  For those the linear-fractional programme of our addendum A3 remains,
and Q1 stays open.

## Originality

Holley's inequality (1974) and the monotonicity of Gibbs measures in a field are
textbook.  That an *arbitrary* perturbation with bounded single-site differences is
sandwiched between the two fields is a two-line application; one search did not find it
stated, and we expect it to be folklore in statistical mechanics.  Its use for the robust
range of an observable free-energy difference over an uncertainty class was not found in
your branch nor in that search.  Nothing more is claimed.

## For engineering

Nothing to compute now.  If K-T2 (level partition functions from one chain certificate)
is taken up, Corollary 3 turns it into certified robust intervals for threshold
macrostates of ferromagnetic chain models at once.

## Requested response

Theory: is the sandwich already in your notes under another name?  And Q1 for a
frustrated known part — is the extremal residual of the linear-fractional programme
describable (our controls show it is not a field)?
