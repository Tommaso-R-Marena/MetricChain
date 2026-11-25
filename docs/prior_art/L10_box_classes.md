# L10 — Prior art for sup-norm (box) classes around a sampleable known part (theory report §11.30)

Written at the fifteenth checkpoint of cycle 10 (25 November 2026) by the theory division.
**Reading level: three web searches, results read as search summaries and abstract-level
snippets; no full text was opened.**  Each row says what the summary supports and what in our
text rests on memory.  A review of this section, with a proper search, has been requested from
the Scientific Discovery Division (THY-RES-0007 §6, THY-RES-0008).

| source | what the record or summary says | used in §11.30 for | what rests on memory |
|---|---|---|---|
| R. W. Zwanzig, J. Chem. Phys. 22 (1954) 1420 (already in `L1`, read at abstract level there) | free-energy perturbation: `ΔF = −ln⟨e^{−ΔU}⟩₀` | the identity `ln Z − ln Z₀ = ln E_π e^{−r}` | nothing beyond the identity |
| C. Jarzynski, *Rare events and the convergence of exponentially averaged work values*, arXiv:cond-mat/0603185 (2006) | exponential averages are dominated by rare realisations; a forward/reverse duality gives the number of realisations needed for convergence; the direction with the larger mean work needs fewer | the contrast "convergence of an estimator at one instance" against "a certificate against a class" | the journal reference (Phys. Rev. E 73, 046105) and the form "exponential of the dissipation of the reverse process" |
| S. Chatterjee, P. Diaconis, *The sample size required in importance sampling* (2018) (see `L9`: read by the science division) | sample size `e^{KL}` | the same contrast | — |
| P. Dagum, R. Karp, M. Luby, S. Ross, *An optimal algorithm for Monte Carlo estimation*, SIAM J. Comput. 29(5) (2000) 1484–1496, doi 10.1137/S0097539797315306 | an `(ε, δ)`-approximation algorithm for the mean of a `[0,1]`-valued variable from independent samples whose expected number of experiments is optimal up to a constant factor for every variable | the sampling model whose zero-variance rate `1/(εμ)` is the rate of Theorem 11.110(e) | the displayed rate `max(σ², εμ)·ln(1/δ)/(ε²μ²)` |
| a note on the above: arXiv:0711.2801 (*Inverse sampling for nonasymptotic sequential estimation of bounded variable means*) | states that the proof of the stopping-rule theorem of Dagum et al. has a significant gap | recorded as a caveat; **we do not use that theorem** | — |
| A. Maurer, M. Pontil, *Empirical Bernstein bounds and sample variance penalization*, COLT 2009, arXiv:0907.3740, Theorem 4 | with probability at least `1 − δ`: mean `≤` sample mean `+ √(2V_n ln(2/δ)/n) + 7 ln(2/δ)/(3(n−1))` for `[0,1]`-valued variables, `V_n` the sample variance; derived by a union bound of a Bennett-type inequality and a tail bound for the sample variance | the instance-wise bracket "without a hint" (two-sided: `ln(4/δ)`; scaled by the range `e^{ρ₋} − e^{−ρ₊}`) | nothing; the constants are those of the summary, and the coverage is tested by simulation (harness XXIV.5) |
| W. Hoeffding (1963), the lemma on the moment generating function of a bounded variable | `ln E e^{s(X − EX)} ≤ s²w²/8` | the bound `L(w) ≤ w²/8`; the sample size for the Gibbs–Bogoliubov side | the sharp two-point form `L(w)` is derived in the text and tested (harness XXIV.1) |

**What we did not find and did not look for properly:** a statement of the *certification*
cost for a class of remainders given by pointwise bounds — matching upper and lower bounds
`Θ((Z(lo)/Z(r) − 1)/ε)` for algorithms that know the reference measure and choose their
points.  We expect the upper bound to be folklore in the Monte Carlo literature (it is a
Bernoulli estimation problem in disguise) and the lower bound to be an instance of standard
packing arguments.  "Not found in three searches at summary level" is all that is claimed.

*Other terms of comparison in the molecular-simulation literature* (search summaries only):
variance-based convergence criteria for exponential averaging (Wang, Sun, arXiv:1803.03123)
and Kofke's bias measure are diagnostics for an estimator on sampled data; neither is a
guarantee against unsampled configurations, which is the point of the floor in Theorem
11.110 and of the documented refutation DEAD.28.
