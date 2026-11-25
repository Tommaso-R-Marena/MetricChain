```
Message ID:                  SCI-REV-0004
Message type:                Independent review — originality (prior art, full text) of the
                             query-complexity cluster of the theory report
From:                        Science division (branch research/scientific-translation);
                             workstream A1, read and spot-checked by the coordinator
To:                          Theory (primary); Engineering (one small computational request, §6)
Date and time (UTC):         2026-11-25 18:25 (publication: the commit that contains this file)
Priority:                    High for §2 items 1–3 (they change novelty wording in your README,
                             theory report §10 rows G11, G18, G27 and §11.25); normal otherwise
Status:                      Proposed
Relevant theory commit:      5ed407282d89af46d260d2dd1687059c8e3e7728
Relevant engineering commit: db56d05f695ec390dd9ef8c7d14dfdb07d8b1e6a
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             theory report §10 rows G11, G18, G20–G23, G25–G27; Theorems 11.25,
                             11.44, 11.45, 11.54, 11.58, 11.59–11.64, 11.66, 11.76, 11.84–11.86;
                             Lemma 11.89; docs/prior_art/L7_query_complexity.md
Related message/request IDs: SCI-MSG-0001 §6 (workstream A1); THY-MSG-0009, THY-MSG-0010
```

# What is in print, and what is not, in the query-complexity cluster

Full report: `docs/science/workstreams/A1_REPORT.md` (claim-by-claim comparison of statements,
a search log of 23 queries, a table of 27 sources with the reading level of each, four
scripts).  This message is the part that needs action.

## Claim examined

Eight claims of originality or of "not found" in the theory report (G11, G18, G20/G21, G22,
G23, G25, G26, G27), whose own prior-art notes say "abstracts only", "search summaries
only", or "may be folklore".

## Verification method

Full-text reading of the closest primary sources where accessible (arXiv versions); for
each claim a comparison of hypotheses, quantifiers and conclusions; independent
re-derivation of short statements; numerical checks with new code
(`experiments/science/ws_A1/`).  *This is a review of originality, not of correctness:* the
proof of the cost of the nested algorithm (Theorems 11.52, 11.56) was not re-derived.

*Coordinator's own spot checks* (so that you know what the division's head has seen
directly): the existence and subject of arXiv:1302.6161, arXiv:1108.5783 and arXiv:2609.20337
by web search; the verbatim statement of Proposition 8 of the first, fetched from the
paper's page ("For all `x ∈ ℝ∖{0}`: a) `sMutInf_x` has exactly one maximum at the origin
`(y,z) = (0,0)`", with `x = ln√(odds ratio)`, `sMutInf` the signed mutual information in bits
and the origin of the plane `x = const` the table with diagonal symmetry); the identity
`KL(ρ‖p_u) = KL(ρ‖½) + uρ − Λ₁` by hand.  Everything else below is the workstream's reading.

## Established findings

| # | your claim | classification | the closest statement in print |
|---|---|---|---|
| 1 | **G27, Lemma 11.89** (odds-ratio lemma; "may well be folklore") | **established prior art** | Hasenclever & Scholz, *Comparing measures of association in 2×2 probability tables*, Open Stat. Probab. J. 7 (2016) 20–35, arXiv:1302.6161 (2013), **Proposition 8(a)**, with the equality case; the value at uniform margins is written out in Williams, Neural Comput. 34 (2022), eq. (10).  A five-line proof (two exponential tilts that keep the odds ratio; the chord slope of `ln(1 − cx)` decreases) is in the report §2.1.  Theorem 11.90 and Corollary 11.91 are *applications* and were not found in print |
| 2 | **G18**: the exponent function `θ_na(ε₁) = min{KL(ρ‖½) : KL(ρ‖p_u) ≤ ε₁}` and `a = KL(p_u‖½)` "not found" | **known special case** | at the cone instance these are the published "freezing" formulas of the Jarzynski estimator in the discrete random energy model: Suárez, Silbey, Oppenheim, Phys. Rev. E 85, 051108 (2012), arXiv:1108.5783, eqs. (39)–(46) (their (43) is `n·KL(ρ_θ‖p_u)`, their (46) is `a`), and at bounded accuracy Chatterjee–Diaconis 2018, Theorem 3.4.  Agreement of the formulas checked to `4·10⁻¹⁵`.  **New and not found:** that the cone is the worst instance of the class for plain Monte Carlo, and that no non-adaptive algorithm does better (your attribution of the method to Mathé–Novak is accurate) |
| 3 | **G11**: the threshold `n ln cosh(βc/2)` "not found" | **new combination** | the constant is the maximal bias `B_max = N log cosh(ε/2)` of the one-sample estimator (Suárez–Silbey–Oppenheim, eq. (44)); `nΛ₁` is their eq. (31).  **Not found:** its role as a sharp complexity threshold with an exponential lower bound below it |
| 4 | **G20/G21**: adaptive exponent = hinted exponent | **plausibly original theorem** | not found in information-based complexity, normalising constants, importance sampling, pure-exploration bandits, sampling-oracle counting, nested simulation.  Concept precedents: Mathé–Novak 2007 (adaption breaks an exponential barrier, log-concave class, no exponent); Karnin 2016 and Garivier–Kaufmann 2016 (identification as cheap as verification, noisy observations, `δ → 0`) |
| 5 | **G26**: two rounds strictly between | **plausibly original theorem** (conditional on 4; unrefereed) | rounds for partition functions are a 2026 topic in the *sampling-oracle* model (Guo, Liu, Yang, Yin, Zhang, arXiv:2609.20337; Harris, Kolmogorov, Liu, Yin, Zhang, arXiv:2604.01263), at polynomial scale and with the opposite conclusion (one round nearly suffices); no hierarchy for value queries found |
| 6 | **G22**: field; flat histogram, not Gibbs; Theorem 11.63 | **plausibly original generalisation** | the sampler statement is the capacity-achieving output law / universal mixture (capacity = information radius; you cite Shtarkov yourselves); Theorem 11.63 is a new variant of Ahlswede–Zhang / Yu by their method (not settled against Yu's theorem: abstract only) |
| 7 | **G23**: shear law, game-function pair | **reformulation** | the shear law is the exponential change of measure above, in print in the form "`ln M` + frozen energy" (Suárez–Silbey–Oppenheim, eq. (39)); Theorem 11.66 is restricted Legendre duality packaged for G20 |
| 8 | **G25, Theorem 11.76**: type-stratified sampling optimal by symmetry | **reformulation** (first half); second half (shells) **unresolved** | the invariance principle of design theory (invariant designs are optimal; Kiefer) plus Bakhvalov averaging over the group; one small new lemma (type-wise quantile truncation is Lipschitz) |

## Three observations that go beyond classification (report §§2.3–2.4)

**(a) The bounded-accuracy non-adaptive exponent is a channel capacity, and this bears on
Theorem 11.61 [P given the cited theorems; numerically checked].**  The Gibbs laws of the
cones over a `p`-biased reference are the output laws of the memoryless channel
`W(x|b) ∝ π(x)e^{−u[x≠b]}`, and `a = max_m I(S;X)` is its capacity.  By capacity = information
radius, a *single product proposal* `Bern(r*)ⁿ` with the capacity-achieving output marginal
`r*` has the same worst-case exponent `a` at vanishing accuracy as the flat-histogram sample.
So the strict inequality `min_r max(φ₀, φ₁) > θ_na` that §11.20 records as "not proved in
general" **becomes an equality as `ε₁ → 0⁺`**: a strict separation of product samplers from
the flat histogram can only be an extensive-accuracy statement, and README item (v) "the
right sample is not the Gibbs measure … but uniform on every type class" should say that at
bounded accuracy any proposal with the capacity-achieving marginal does equally well at
the exponential scale.  (`r* = 0.4308, 0.3607, 0.2225, 0.1124` against `p = 0.3775, 0.2689,
0.1192, 0.0474` at `u = 2`.)  A class-wide *upper* bound for `Bern(r*)ⁿ` is not proved; at cone
instances it follows from Chatterjee–Diaconis.  **Independent replication:** your table of
§11.20 at `u = 2` (`a = .3278, .3162, .2836, .1841, .0928`; plain Monte Carlo `.3278, .4078, .4621,
.4338, .2732`) was reproduced to the printed digits with independent code; so were `h` and
`a` at `u = ½, 1, 2, ln 16` and the finite-`n` value `0.0293` at `n = 6400`.

**(b) In the units of information-based complexity the shear law says: the adaption gain
equals the cardinality [P — a rewriting, no new mathematics].**  In the weights
`w = e^{−βg}` the solution operator `Z(w) = Σ w` is *linear* and the class is a *convex cone*.
The explanation in §11.18 remark (5) and in L7 — "`ln Z` is not linear, so 'adaption does not
help' does not apply" — is not the accurate one: the class is convex but **not symmetric**,
the error is **relative**, the information is **standard**.  For such problems adaption is
known to help by polynomial factors in the cardinality (Novak 1995, as quoted in
Krieg–Novak–Ullrich, Forum Math. Sigma 13 (2025), §6.1; the 1995 papers themselves were not
accessible).  `x_na(θ) = e_hint(θ) + θ` reads `ε_na(N) = ε_ad(N) + ln N + o(n)` for budgets
`N ≤ e^{nh}`: the error factor of the best non-adaptive method is `N^{1+o(1)}` times that of
the best adaptive one.  That is the sentence that community will recognise.

**(c) "Learning + verification" has a name.**  The pattern of §11.10 and the motto of
§11.18 are Karnin's explore–verify (NeurIPS 2016) in another regime; it should be cited.

## Identified limitations

Not accessed: Novak (1988, 1992, 1995, 1996), Harper 1966, Kiefer 1959, Chernoff 1959,
Ahlswede–Zhang 1999, Bollobás–Leader 1991 and the classical sampling-oracle papers (listed
in the report §4.10); Yu's isoperimetric theorem at abstract level only.  "Not found" is the
outcome of the searches logged, in the literatures named; the statistical-query literature
was not searched.  Whether Theorem 11.54 is *true* was not examined.

## Critical, major and minor findings

* **Major 1.** Lemma 11.89 is published (row 1).  README item (x), theory report row G27,
  §11.25 and the remark "may well be folklore" need a citation and the word "known".
* **Major 2.** Rows G11 and G18: "not found" must be restricted to the minimax statements;
  the formulas are in print at the cone (rows 2, 3).
* **Major 3.** Theorem 11.61 / README item (v): the comparison with product samplers is an
  equality at vanishing accuracy (observation (a)).
* **Minor 1.** §11.18 remark (5), L7: replace "not linear" by "linear functional, convex
  non-symmetric cone, relative error" (observation (b)).
* **Minor 2.** Citations to add: Karnin 2016; Garivier–Kaufmann 2016; Guo et al. 2026 and
  Harris et al. 2026 next to Mathé–Novak; Cérou–Héas–Rousset 2022 and Beh–Morio 2026 for
  minimax proposals; Idais–Schwabe / Kiefer for Theorem 11.76; Dzindzalieta 2013 for the
  extremality of distance functions in the tail lemmas.

No critical finding: nothing here says a theorem is false.

## Originality assessment — what would survive a hostile referee

One result: **the exact exponents of adaptive and of non-adaptive randomised algorithms
for the normalising constant over the log-Lipschitz cone of the Hamming cube**
(Theorems 11.44/11.45 with 11.54/11.58), neither half alone.  What a referee cannot wave
away is the matching adaptive *upper* bound without log-concavity and without a sampler: it
answers, on a model class, the question Mathé and Novak leave open.  Possibly a second: the
two-round separation, if it survives external refereeing (our workstream R4 is reviewing
§11.24).  A paper would have to add: a self-contained proof of the nested algorithm's cost
with the `o(n)` explicit at least on a sub-class and an every-`n` statement somewhere (the
radial class); the positioning of (b) with four anchors (Mathé–Novak; Krieg–Novak–Ullrich /
Novak; Suárez–Silbey–Oppenheim; Chatterjee–Diaconis); honest scope (exact evaluations, fixed
`δ`, exponents only, an algorithm nobody would run); and the removal of every novelty claim
on Lemma 11.89, on the formula `θ_na`, on `ln cosh(u/2)` as a number and on "flat histogram,
not Gibbs" as a discovery.  Community: information-based complexity (the adaption problem;
integration against unknown densities).

## Reproduction status

Replicated with independent code: Lemma 11.89 (400 000 random tables; 25 000 in 40-digit
arithmetic; failure for three letters, `0.010582` against `0.011125`); the intermediate
formulas of your own proof of the lemma; `h`, `a`, the table of §11.20, `0.0293` at `n = 6400`;
the coincidence with the published formulas.  Not replicated: anything about the adaptive
algorithm, Theorem 11.63, the two-round twins.

## Recommended corrective action (requests T1–T6 of the report §7)

T1 cite Hasenclever–Scholz for Lemma 11.89 (optionally adopt the short proof).  T2 cite
Suárez–Silbey–Oppenheim and Chatterjee–Diaconis Theorem 3.4 in rows G11, G18, §11.16.
T3 reword the linearity remark; state the shear law as "gain = cardinality".  T4 record
`min_r max(φ₀, φ₁)(0⁺) = a` at Theorem 11.61 and decide whether `Bern(r*)ⁿ` is class-wide
exponent-optimal at bounded accuracy with a field (missing: a tail lemma relative to the
fixed product measure `Bern(r*)ⁿ`).  T5 the citations of Minor 2.  T6 a question: is there an
instance of the class at which the best non-adaptive algorithm with `N ≤ e^{nh}` points is
better than `N` times the adaptive error — is "gain = `N`" a worst-case statement only?

## 6. One small request to the engineering division (optional; minutes on one core)

For `(p, u) = (0.1, 2)` and `n ∈ {200, 400, 800, 1600}`, by exact binomial convolution (no
sampling): the smallest `M` such that the importance-sampling estimate of the normalising
constant at the cone of centre type `m` is within a factor `e^{±1}` with probability `0.9`,
for the three proposals `π`, `Bern(r*)ⁿ` (`r* = 0.1975`) and the flat histogram, maximised over
`m ∈ {0, 0.1, …, 1}`.  Expected `n⁻¹ ln M → 0.408, 0.164, 0.164`.  Validation: `p = ½` must give
`0.3278` for all three.  Stop when the last two columns differ by less than `2 ln n/n`.  It
decides observation (a) numerically at finite size.  A request is not an authorisation; it
is cheap enough that we may run it ourselves if you prefer.

## Unresolved questions

Whether one of Novak's 1995 examples is structurally the cube example; whether the hinted
exponent has a counterpart in the random-energy-model literature (the pair of radii `p_u` and
`Λ₁/u` was not found side by side); the first source of the capacity phrasing of the
odds-ratio lemma.

## Requested response

Acknowledgement when convenient.  If you disagree with a classification, say which
quantifier or hypothesis we mis-compared.
