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

## Second addendum (seventeenth checkpoint, 26 November 2026): what the Scientific Discovery Division's full-text search found

**Reading level: the division's, not ours.**  Its workstream A3 read 47 sources in the
passages that matter; its coordinator re-read twenty passages; the list of what could not
be accessed is in its message SCI-RES-0009 §4 and its report
`docs/science/workstreams/A3_REPORT.md` on its branch.  We repeated none of it.  Our own
contribution to this addendum is two search summaries (one query each) confirming that the
two records named first below exist with the stated titles, authors and identifiers.

| statement in §11.30 | in print, according to the division's reading | what it did not find |
|---|---|---|
| Theorem 11.110(a): the bracket with `L(w)` | W. Hoeffding, J. Amer. Statist. Assoc. 58 (1963) 13–30, Lemma 1 and (4.12)–(4.15): the bound with the mean known, of which ours is the maximum over the mean; `e^{L(w)}` is Specht's ratio (Specht 1960, through a secondary source); the same quantity as the "maxkl" of bounded-range mechanisms (Dong, Durfee, Rogers, arXiv:1909.13830) | nothing |
| (b): the range after evaluations, the mass a deterministic certificate needs | the stopping criterion of provable partition-function algorithms in computational protein design: Georgiev, Lilien, Donald, J. Comput. Chem. 29 (2008) 1527–1542, Proposition 3 (a function floor from pairwise lower bounds, no ceiling) — a literature about sequence design, cited here for the certificate scheme on one fixed state only | the ceiling term, the closed form of `q*`, the necessity half |
| (c)–(e): the hinted cost | the cost quantity: Liu, Fisher, Ihler, *Probabilistic variational bounds for graphical models* (NeurIPS 2015), weights bounded by an upper-bounding model; the rate `max(σ², εμ)·ln(2/δ)/(εμ)²` of Dagum, Karp, Luby, Ross (2000), read through restatements (its proof is reported incomplete in arXiv:0711.2801, whose author's own result implies the statement); the hint: Aaronson, arXiv:quant-ph/0210020, randomised certificate complexity; without a hint: Block and Shetty (below), Theorem 6; a linear dependence on a density-ratio bound: Mathé and Novak, arXiv:math/0611285 | **the instance-wise two-sided statement with a hint in the query model, with its sampler** |
| "without a hint": the empirical Bernstein bracket | Liu–Fisher–Ihler, Corollary 3.2, attributed there to Maurer and Pontil | nothing |
| (f): floor and variance | Hoeffding (1963), Theorem 3, inequality (2.8) with the extremal two-point law (2.10); the closed form (2.9) is Bennett's (1962); as a bound on the moment generating function: Fan, Grama, Liu, arXiv:1109.4359, Lemma 3.1; the lower bound with a ceiling: Liao and Berg, arXiv:1707.08644, Theorem 1 | its use as a certified second-order bound in free-energy perturbation (one possibly relevant paper, Decoster 2004, could not be opened) |
| Proposition 11.112: divergence balls | A. Block, A. Shetty, *Partition function estimation under bounded f-divergence*, arXiv:2602.23535 (26 February 2026; proceedings of COLT 2026): upper and lower bounds without a hint, in the sampling model; earlier for Rényi orders, for all randomised algorithms that use function values: R. Kunsch, E. Novak, D. Rudolf, arXiv:1805.08637, J. Complexity 53 (2019); mean estimation with heavy tails (Bubeck, Cesa-Bianchi, Lugosi, arXiv:1209.1727; Devroye, Lerasle, Lugosi, Oliveira, arXiv:1509.05845) | the reading as a verification cost; the statement that polynomial moments of the remainder do not suffice |
| (e) of the proposition: divergences from one-site oscillations | Cesar and Rogers, arXiv:2004.07223, Lemma 3.2 (bounded-range pairs); Bun and Steinke, arXiv:1605.02065, Lemma 2.2 (composition); for chains: Chazottes, Collet, Külske, Redig, arXiv:math/0503483; Kontorovich and Ramanan, Ann. Probab. 36 (2008) | the sharp form as stated (a direct corollary) |
| the asymmetry of the two sides; that an estimated variance certifies nothing | Grosse, Ghahramani, Adams, arXiv:1511.02543; Bahadur and Savage (1956, through a secondary source); Chatterjee and Diaconis, arXiv:1511.01437, Theorem 2.1 | a query-complexity statement of the asymmetry |

*Consequences drawn in the theory report:* the attributions in Theorem 11.110(a), (f) and
Proposition 11.112; the mean-dependent form of (a); the corrected two-sided statement (e);
the remark "what the hint buys"; the prior-art paragraph of §11.30, which now says that
every ingredient is in print and what was not found.  Not searched by anyone: the
statement for ratios (Corollary 11.114) and the sandwich sampler (Proposition 11.113) —
the latter is importance sampling in proportion to an envelope and is certainly classical
in the theory of randomised integration; we cite no source for it.

