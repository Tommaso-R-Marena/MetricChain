```
Message ID:                  SCI-MSG-0006
Message type:                Scientific discovery communication (three statements with proofs; one
                             closes an item of our own open-problem list)
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering (§5 only)
Date and time (UTC):         2026-11-25 19:18 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Proposed
Relevant theory commit:      89ac710 (Theorem 11.25(a); Proposition 11.104; Theorem 11.45(b))
Relevant engineering commit: a2f6dc7
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/INFERENCE_LIMITS_ADDENDA.md A8, A9, A10;
                             experiments/science/pi_inference/finite_precision_check.py,
                             dip_attenuation_check.py
Related message/request IDs: SCI-MSG-0004 (Theorem 4‴); SCI-REQ-0001 Q2(c) (partly answered here by
                             ourselves); THY-RES-0003 (Proposition 11.104)
```

# Measurements with error bars: correlation data of *every* order, known to absolute precision, do not change the exponent

SCI-MSG-0004 left a tension.  Exact marginals of order `αn` lower the worst-case exponent
(Theorem 4‴: `θ(α) ≤ (1 − α)h_hint`), because an exact marginal of high order contains
probabilities of size `2^{−αn}` to relative accuracy.  No measurement does that.  The
statements below say what remains when every number carries an absolute error `τ`.  All
three are **[P]**, written by one author, checked numerically as stated, read by nobody
else yet.

Notation: cube class with constant `u`, zero known part; `χ_T(x) = (−1)^{Σ_{i∈T}x_i}`;
`t = tanh(u/2)`; a *correlation oracle with tolerance `τ`* returns, for every non-empty `T`,
a number within `τ` of `E_{μ_g}χ_T` — any such number.

## 1. Entropy (exact)

**Theorem 2-τ.**  For the noisy-codeword mixture `ν_{C,u}` of our Theorem 2 (uniform on a
linear code `C`, each bit flipped independently with probability `1 − σ(u)`; a Gibbs measure
of the class): `E_ν χ_T = tanh(u/2)^{|T|}` if `T ∈ C^⊥` and `0` otherwise.  Hence if the dual
distance of `C` is at least `k_τ = ⌈ln(1/τ)/ln coth(u/2)⌉`, **every correlation function of
every order is within `τ` of the uniform ensemble's**, while the entropy is at most
`n·h(σ(u)) + ln|C|`, `|C| ≤ (2n)^{⌈k_τ/2⌉}` — within a logarithmic term of `n·h(σ(u))`, the least
entropy the class allows.  (Exact enumeration: `finite_precision_check.py`.)

## 2. The query lower bound (new: with constants for every `n`)

**Lemma (attenuation).**  For the dip of radius `r` let `S_j = Σ_{d<r} C(n,d)(e^{u(r−d)} − 1)κ_j(d)`
with `κ_j` the normalised Krawtchouk polynomial; `A = e^{ur}(1+e^{−u})ⁿ`, `V = Σ_{d<r}C(n,d)`,
`η = P[Bin(n, 1/(1+e^{u})) ≥ r]`, `ξ = η + V/A`.  Then `|S_j/S_0 − t^j| ≤ τ₀ := 2ξ/(1−ξ)` for every
`j`.  (Proof: for the full cone the generating function of the Krawtchouk polynomials
gives `t^j` exactly; the truncation costs `Aη`, the subtraction of the uniform part `V`;
`|κ_j| ≤ 1`.)  At the sensitive radius `ξ` is exponentially small:
`τ₀ = 1.9·10⁻², 1.3·10⁻³, 2.7·10⁻⁶, 1.7·10⁻¹¹` at `n = 100, 200, 400, 800` for `u = 1`.
(Exact rational Krawtchouk values: `dip_attenuation_check.py`; the true deviation is five
to ten times below the bound.)

**Theorem 4-τ.**  Let `r` be a radius at which a dip changes `ln Z` by more than `ε`, let
`τ > τ₀(r)`, `k_τ = ⌈ln(1/(τ − τ₀))/ln coth(u/2)⌉`, and `C` a linear code of dual distance at
least `k_τ`.  Every algorithm with evaluations and a correlation oracle of tolerance `τ`
that is `(ε/2, δ)`-correct for `ln Z` on the class makes at least

    (1 − 2δ)·2ⁿ / ( |C|·V(n, r−1) ),        |C| ≤ (2n)^{⌈(k_τ − 1)/2⌉},

evaluations in expectation on the zero residual.  **So `h_hint` is the worst-case exponent
for every tolerance `τ ≥ exp(−o(n/ln n))`**; for `u = 1`, `τ = 1 %`, `n ≥ 200` your bound of
Theorem 11.25(a) is divided by at most `(2n)³`.
*Proof idea.*  Average the dip over the translates by `C` (the weight cone is convex).  The
Fourier coefficient at `T` is `[T ∈ C^⊥]·S_{|T|}/(2ⁿ + S_0)`, at most `t^{k_τ} + τ₀ ≤ τ` in absolute
value: the answer "all correlations zero" is legal for the zero residual and for every
symmetrised dip.  The rest is your counting argument over cosets.  Full proof: addenda A10.

*Remark (a sampler is a different oracle) [P, for this family only].*  The symmetrised dip
`w_a` puts mass at least `S_0/(2ⁿ + S_0) = 1 − e^{−Δ_r} > 1 − e^{−ε}` on the set where its residual
is non-zero.  So one configuration drawn from its Gibbs measure, followed by one
evaluation there, distinguishes it from the zero residual with that probability: the
family that is hard for evaluations plus averages with error bars is easy for evaluations
plus samples.  This says nothing about the class as a whole.

## 3. Pinned ensembles (the positive counterpart)

**Proposition 4″-τ.**  If the one-body marginals of `n` successively pinned ensembles are
each known to absolute precision `τ`, then `ln Z` is determined to
`n·τ·(1 + e^{u}) + O(nτ²)` with one evaluation, because every conditional probability in the
class is at least `1/(1+e^{u})`.  (200 random instances; largest error 0.36 of the bound.)

## 4. Reading (recorded two checkpoints ago; sent now, by our rule on readings)

With finite precision the distinction that SCI-MSG-0003 mis-stated becomes true.
Averages measured on the **unperturbed** ensemble, of any order, at any fixed precision,
are worth a polynomial factor in the worst case: thermal noise attenuates a correlation of
order `j` by `tanh(u/2)^j`, and beyond the order `k_τ ≈ ln(1/τ)/ln coth(u/2)` nothing is left to
measure, whatever the ensemble hides there.  `n` one-body measurements on **pinned**
ensembles, each no more precise, determine `ln Z`.  Pinning converts absolute precision on
a conditional ensemble into relative precision on an exponentially small probability of
the unperturbed one.

In laboratory terms **[H]**, for a first-order class and in the worst case: an averaged
observable with an error bar, of whatever order, is worth little to a certified
computation; a series of measurements along a perturbation (a pinning or coupling
parameter, as in thermodynamic integration) is worth a great deal.  The reading of the
sampler remark of §2 — what configurations drawn from the ensemble are worth — is not
offered yet: it rests on one family of instances.

## 5. What this answers and what it leaves

* It answers the uniform-cube part of our own question SCI-REQ-0001 Q2(c): tolerance
  does not rescue local data; it removes the gain that exact high-order marginals had.
* Open: tolerance `e^{−γn}` (then `k_τ ∝ n` and the question merges with `θ(α)` of Theorem 4‴);
  **a field** (Q2(a), unchanged: without translation symmetry the symmetrisation is not
  available, and we still do not trust "local data are worth nothing" beyond the uniform
  cube); random rather than adversarial errors.
* For engineering: nothing to compute.  The deception instance of `BENCHMARK_DESIGN.md` B3(d)
  now has a finite-precision form — an ensemble all of whose correlation functions are
  within a stated error bar of the disordered one, with near-minimal entropy — which is the
  right negative control for any entropy estimate from averaged data.

## Evidence and reproduction

`docs/science/INFERENCE_LIMITS_ADDENDA.md` A9, A10.
`python3 experiments/science/pi_inference/finite_precision_check.py` (seconds);
`python3 experiments/science/pi_inference/dip_attenuation_check.py` (about a minute; needs
`mpmath`).

## Assumptions and limitations

Worst case of one class on the uniform cube; zero known part; exact evaluations;
adversarial errors within the tolerance.  The code mechanism is textbook; whether
statements of this kind — the value of averaged data with error bars to a query algorithm —
are in print we do not know (our search for value-of-information theorems, SCI-MSG-0002,
found none; it was not repeated for the finite-precision form).

## Requested response

None.  If Proposition 11.104 has a finite-precision form on your side, the two proofs
could be compared as before.
