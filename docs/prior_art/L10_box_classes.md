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

## Addendum at the sixteenth checkpoint (26 November 2026): the two results adopted from the Scientific Discovery Division

**Reading level: none on our side.**  Nothing below was searched or opened by the theory
division; the attributions are from memory, ours and the science division's (its messages
SCI-RES-0007 §3(4), SCI-MSG-0018 say the same of their side), and the division's
full-text reading (its workstream A3) had not reported when this was written.

| statement in §11.30 | what it is | attribution, and its status |
|---|---|---|
| Theorem 11.110(f): `0 ≤ K ≤ W(b, σ²) ≤ (σ²/b²)(e^b − 1 − b)` for a variable bounded on one side with a variance bound, the two-point law extremal | the one-sided moment-generating-function bound behind Bennett's inequality | G. Bennett, J. Amer. Statist. Assoc. 57 (1962); W. Hoeffding (1963), the inequality for variables bounded above with given variance — **from memory; no source opened by either division**; the sharp form is tested numerically here (harness XXIV.6) |
| Proposition 11.112(a)–(c): detection in an `L^p` ball, the hinted cost `e^κ/ε^{p/(p−1)}`, the Chebyshev certificate for `p ≥ 2` | Hölder's, Minkowski's and Chebyshev's inequalities in the query model of this report | no source: elementary; whether the *statement* (certification cost against a Rényi-divergence bound, with a hint) is in the literature is not known to us — the division compares with the two terms of the stopping-rule theorem of Dagum, Karp, Luby and Ross, from memory |
| Proposition 11.112(d): a Kullback–Leibler bound costs `e^{κ/(1−e^{−ε})}` | data processing for the binary divergence | elementary; compare the `e^{KL}` sample-size rule of Chatterjee and Diaconis (row above), which is a statement about typical accuracy at an instance, in the opposite direction of the divergence — the division's remark |
| Proposition 11.112(e): `D_p ≤ p²Σc_i²/(8(p−1))` from one-site oscillations on a product measure | the bounded-differences bound on the moment generating function | McDiarmid (1989) — **from memory**; for a Markov-chain reference the division cites Marton and Kontorovich–Ramanan, **from memory, unverified** (its Proposition A17.8, which we have read and not otherwise checked) |
| the variance bound `¼Σc_i²` used in Theorem 11.110(f) | the Efron–Stein inequality with bounded differences | **from memory** |

No novelty is claimed for any row by either division.
