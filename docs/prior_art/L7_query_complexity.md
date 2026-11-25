# L7 — Query complexity: prior art for theory report §11.10

Scope: the method and the nearest published statements for the bounds on *algorithms* (as
opposed to certificates) of theory report §11.10.

How this note was made.  First version (cycle 8): four web searches on 2026-11-24, search-engine
summaries only.  The third referee (`reviews/R3`, M5) found that this could not support "no
match found" and that the closest literature was missing; the present version records what the
referee read (R3 §4a: Holzmüller–Bach, pp. 1–13 of the PDF; Bachoc–Cesari–Gerchinovitz through
an automatic summary; abstracts for Grossman–Komargodski–Naor) and what was re-checked for this
revision (the arXiv abstract pages of Holzmüller–Bach and of Hetland).  Everything else is
marked as unverified.

| # | claim of §11.10 | status | source |
|---|---|---|---|
| Q1 | A deterministic algorithm that is `ε/2`-correct must distinguish every pair of class members whose values differ by more than `ε` (Theorem 11.22(a,d)) | KNOWN: the radius-of-information argument for adaptive information | Traub–Wasilkowski–Woźniakowski, *Information-Based Complexity* (1988) [from memory] |
| Q2 | Randomised algorithms: every sensitive alternative is detected with probability `1 − 2δ`; expected queries are at least `(1 − 2δ)` times a fractional packing of sensitive blocks (Theorem 11.22(b,c)) | KNOWN METHOD: fractional block sensitivity = fractional certificate complexity is a lower bound on randomised query complexity of Boolean functions | Aaronson, "Quantum certificate complexity" (2003; randomised certificate complexity `RC`); Tal (2013) and Gilmer–Saks–Srinivasan (2016); Kulkarni–Tal, "On fractional block sensitivity", Chicago J. Theor. Comput. Sci. 2016:8 [search summaries; attributions agree with the referee's check] |
| Q3 | Instance-wise deterministic complexity of certified minimisation equals the smallest certificate (Theorem 11.23(a)); the cost notion "correct everywhere, charged on one instance, may be tailored to it" | KNOWN.  In `ℝ^d` for `f ≡ 0`: the "best possible algorithm" `n_B` (Hansen–Jaumard–Lu 1991) and the lower bound for certified algorithms (Bachoc–Cesari–Gerchinovitz 2021).  The notion itself is **instance complexity**: Grossman–Komargodski–Naor, "Instance complexity and unlabeled certificates in the decision tree model", ITCS 2020 (LIPIcs 151, paper 56) — an algorithm that receives a certificate, is correct on every input and is charged only when the certificate is right; deterministic and randomised trees; in the labelled case it is certificate complexity.  For metric search (symmetric metric, no known part, exact range queries) the characterisation of the best achievable query set as a minimum dominating set, with reductions in both directions, is Hetland, "Optimal metric search is equivalent to the minimum dominating set problem" (arXiv:2008.09607, 2020) — found by workstream C; it contains the hardness gadget of Theorem 11.10 and bears on Theorem 11.4 | see `L4`, K1 and K3; GKN: abstract read by the referee, not by us; Hetland: abstract re-checked for this revision, §§1–5 read by workstream C, full text read by the reviewer of workstream C |
| Q4 | Randomised algorithms pay the covering price instance by instance, and a hedged spot-check attains it (Theorem 11.23(b,c)) | NOT FOUND in this form.  Bachoc–Cesari–Gerchinovitz treat deterministic certified algorithms and name certification with a prescribed probability as an open direction [referee's reading of an automatic summary].  Worst-case statements ("randomisation does not improve the rate of global optimisation over Lipschitz classes") are classical | Nemirovski–Yudin (1983), Novak (1988); quoted as Theorem 7 "adapted from Novak (1988)" in Holzmüller–Bach (2025) [referee's reading of the PDF] |
| Q5 | For `ln Z`: randomisation helps only above an accuracy scale (Theorem 11.25) | KNOWN QUALITATIVELY for smoothness classes on `[0,1]^d` in the worst case: Holzmüller–Bach, "Convergence rates for non-log-concave sampling and log-partition estimation", JMLR 26(249):1–72, 2025 (arXiv:2303.03237).  Abstract (re-checked): "the optimal rates for sampling and log-partition computation are sometimes equal and sometimes faster than for optimization".  §2.2 (referee's reading): with *stochastic* evaluation points there is an "optimization regime", in which the deterministic rate cannot be improved (Proposition 9, by reduction to optimisation), and a "quadrature regime", in which Monte Carlo gains `n^{−1/2}` (Theorem 8); the lower bounds "place bumps with small support in regions that the algorithm does not query"; a lower bound for stochastic log-partition estimation outside the optimisation regime is stated as open | Theorem 11.25 is the corner of that picture in which the dimension grows and no approximation of the residual is affordable; the exact threshold `n ln cosh(βc/2)` and the accuracy diagram were not found there |
| Q6 | Soft-gap radius, three budgets, lower bound on the randomised exponent (Theorems 11.24, 11.26) | NOT FOUND.  Nearest: query lower bounds for normalising constants of log-concave densities by hiding a perturbation in one of many cells | Ge–Lee–Lu, "Estimating normalizing constants for log-concave distributions: algorithms and lower bounds", STOC 2020, arXiv:1911.03043 [search summary] |
| Q7 | Extremal sets on the cube are Hamming balls (Theorem 11.25(c)) | KNOWN: vertex-isoperimetric theorem | Harper, "Optimal numberings and isoperimetric problems on graphs", J. Combin. Theory 1 (1966) [from memory; the step used is checked exhaustively for `n ≤ 4` in harness XII.5] |
| Q8 | Sample size of importance sampling `≈ e^{KL}` (remark after Theorem 11.25; used only as a heuristic) | KNOWN | Chatterjee–Diaconis, "The sample size required in importance sampling", Ann. Appl. Probab. 28 (2018) [from memory] |
| Q9 | Isoperimetric exponents for two product measures; inherently typical subsets (the tools of workstream A for the exponent beyond the cube, theory report Theorem 11.27) | KNOWN TOOLS.  Referee R4 read Ahlswede–Zhang (1999) in full and, in Yu (arXiv:2205.07596), the definition of the exponent, Theorems 4, 5, 8, Assumption 3 and the proof; the attributions are accurate, and the lemma on inherently typical subsets used in the proof is a variant proved in the workstream report, not the statement of Ahlswede–Yang–Zhang (1997).  Used as a black box with a reference law that depends on the measure exponent of the set, the fixed-measure theorem gives a bound that coincides numerically with the game value on the examples computed; no proof of equality in general.  Uncited precedent for "sublevel sets of additive Lipschitz functions are extremal": Alon–Boppana–Spencer (1998) | no prior statement of the problem with a free second measure and a radius coupled to the measure of the set was found (six searches; then the search budget was exhausted) |

## Search log (first version)

1. `fractional block sensitivity fractional certificate complexity randomized query complexity
   lower bound Tal Aaronson randomized certificate complexity` — confirmed Q2 (summaries of
   Kulkarni–Tal and of later papers citing Tal and Gilmer–Saks–Srinivasan).
2. `randomized algorithms global optimization Lipschitz functions lower bound randomization does
   not help Novak "Deterministic and Stochastic Error Bounds"` — did not retrieve Novak's
   statement; returned Malherbe–Vayatis (LIPO) and convex-optimisation lower bounds.
3. `Bachoc Cesari Gerchinovitz instance-dependent bounds zeroth-order Lipschitz optimization
   error certificates lower bound certified algorithms randomized` — abstract-level summary;
   nothing on randomised algorithms.
4. `query complexity lower bound estimating normalizing constant partition function black-box
   oracle Ge Lee Lu "normalizing constants" lower bound` — Q6.

Not read by anyone in this project: Novak 1988, Nemirovski–Yudin 1983, Ge–Lee–Lu 2020, Harper
1966, Heinrich; the property-testing literature was not searched.

## What should be checked by a specialist

* Whether an instance-dependent lower bound for *randomised* certified Lipschitz optimisation is
  in the bandit / zeroth-order literature after 2021.
* Whether the threshold of Theorem 11.25 and the two-reference sandwich of §11.10 are known in
  the literature on Monte-Carlo integration of exponential functionals (information-based
  complexity), and how the open lower bound of Holzmüller–Bach relates to the instance-wise
  dip/pair technique.
* Hetland's paper against Theorems 11.5, 11.10 and 11.23(a).  The independent reviewer of
  workstream C read it in full (`reviews/R_C_review.md`): for `f ≡ 0`, symmetric `d` and exact
  range queries it contains the covering / dominating-set characterisation (of the type of
  Theorem 11.4), the identical 0/1/2-distance gadget of Theorem 11.10 with `(1−ε) ln n`
  inapproximability, and an informal adversary argument for Theorem 11.23(a).  Not there: the
  exchange lemma and the `+1` of Theorem 11.5, the accuracy `ε`, a known part, asymmetric
  envelopes, and the thermal theory; its function class also differs (it adds a Katětov
  constraint).  A specialist should confirm this reading.
* Asymptotic isoperimetric inequalities on product spaces at the large-deviation scale
  (Ahlswede–Gács–Körner blowing-up; Ahlswede–Zhang; Yu) as the tool for exponents beyond the
  cube.

## Addendum (cycle 10): algorithms without a hint (theory report §11.16)

Sources and who read what.  "R5" is the fifth referee (`reviews/R5_referee_report.md`, §4, with
its own search log of fifteen searches and nine page fetches).

| source | relevance | read by | depth |
|---|---|---|---|
| P. Mathé, E. Novak, *Simple Monte Carlo and the Metropolis algorithm*, J. Complexity 23 (2007); arXiv:math/0611285 | **closest prior art for Theorem 11.45**: lower bound for every non-adaptive Monte Carlo method on log-concave densities with a Lipschitz logarithm, by Bakhvalov's averaging over densities `exp(−α‖y − y_i‖)` with hidden centres and integrands supported near the centre (their Theorem 3); remark that one function value identifies the centre for an adaptive method; an adaptive Metropolis method of polynomial cost (Theorem 5); simple Monte Carlo optimal among all methods on the larger class `sup ρ/inf ρ ≤ C` (Theorems 1–2) | R5; the coordinator | R5: §§1–4.1 and §5 in full text, §4.2 skimmed; coordinator: abstract page only (title, authors, abstract: "adaptive methods are much better than nonadaptive ones … the curse of dimension (for nonadaptive methods) can be broken by adaption") |
| S. Chatterjee, P. Diaconis, *The sample size required in importance sampling*, Ann. Appl. Probab. 28 (2018) | the sample size `exp(KL(ν‖μ))` at one instance; Theorem 11.44 makes it a bound on the class at the exponential scale | R5 | abstract page; Theorem 1.1 and a summary of §3 through an automatic reading of the full text |
| L. H. Harper (1966), vertex-isoperimetric theorem | Lemma 11.43(b), (c) | nobody in this project | statement taken from secondary sources (Keevash–Long, *Stability for vertex isoperimetry in the cube*, introduction, automatic reading; a search summary of *Uniqueness in Harper's vertex-isoperimetric theorem*); the consequence used was checked exhaustively for `n ≤ 5` by R5 |
| D. Dzindzalieta, *Extremal Lipschitz functions in the deviation inequalities from the mean*, Electron. Commun. Probab. 18 (2013) | distance functions as extremal Lipschitz functions (precedent for "cones are extremal") | R5 | abstract |
| D. Krieg, E. Novak, M. Ullrich, *On the power of adaption and randomization* (2025); S. Heinrich, *Randomized complexity of parametric integration and the role of adaption I* (2024) | adaption versus non-adaption for **linear** problems on convex **symmetric** classes with absolute error.  (*Corrected at the twelfth checkpoint of cycle 10 after SCI-REV-0004:* this row said "`ln Z` is not linear, so neither 'adaption does not help' nor these gaps apply".  In the weights `w = e^{−ψ}` the functional `E_π w` is linear and the class is a convex cone; what makes those theorems inapplicable is that the class is not symmetric, the error is relative and the information is standard.  For such problems adaption is known to help polynomially in the cardinality — Novak 1995 as quoted in Krieg–Novak–Ullrich 2025, §6.1 — and the shear law of theory report §11.21 says "the adaption gain equals the cardinality" here.) | R5 | abstract pages |
| X. Cai, J. Scarlett, *Kernelized normalizing constant estimation* (AAAI 2024) | bounds for `∫e^{−λf}` over an RKHS ball; related to the open question of §12 item 2(d) | R5 | abstract |
| Dagum–Karp–Luby–Ross (2000); Kunsch–Novak–Rudolf (2019); Ionides (2008); Štefankovič–Vempala–Vigoda (2009) | stopping-rule Monte Carlo, varying cardinality, truncated importance sampling, adaptive cooling schedules | R5 | search summaries only |

Searches by R5 without a relevant hit: query complexity of the partition function of a
Lipschitz function on the Hamming cube (adaptive / non-adaptive); `Σ exp(−f)` over the Boolean
cube by value queries; Harper's theorem combined with Monte Carlo or importance sampling;
worst case of importance sampling over log-Lipschitz classes (this one led to Mathé–Novak).

Assessment (R5, accepted): the method of Theorem 11.45 is known and its hard family is
Mathé–Novak's; the exact non-adaptive exponent on the cube for `ln Z` with a matching
class-wide upper bound was not found; Theorem 11.44 is a routine combination.  The earlier
entry of this file "whether the threshold of Theorem 11.25 … [is] known in the literature on
Monte-Carlo integration of exponential functionals" remains open for a specialist.

## Addendum (cycle 10, second part): adaptive algorithms without a hint (theory report §11.18)

Searches by workstream H (25 Nov 2026); **[A]** = abstract or search-engine summary only,
**[S]** = machine summary of the full text, **[M]** = from memory, not re-checked.  Nobody in
this project has read any of these sources in full.

| topic | found | read | bearing on §11.18 |
|---|---|---|---|
| adaption versus non-adaption in information-based complexity | Novak, *On the power of adaption*; Novak, arXiv:2307.06787; Krieg–Novak–Ullrich, arXiv:2406.07108 | [A] | for linear problems on convex symmetric classes adaption does not help deterministically (Bakhvalov; Gal–Micchelli [M]) |
| randomised setting | Heinrich, *Randomized complexity of parametric integration and the role of adaption I* (J. Complexity 2024); Heinrich, arXiv:2401.14100; Kunsch–Novak–Wnuk, arXiv:2308.01705; Kunsch–Wnuk, arXiv:2410.23067 | [A] | adaption helps by polynomial factors in the number of evaluations (`n^{1/8}`, `n^{1/4}`, up to order `n` for vector-valued approximation); the present problem is nonlinear and the gain is exponential in the dimension |
| the method of the non-adaptive lower bound | Mathé–Novak (2007) | [S] (see the first addendum) | their adaptive upper bound uses log-concavity |
| normalising constants | Holzmüller–Bach, JMLR 26 (2025); Ge–Lee–Lu, STOC 2020 | [A] | smoothness classes on `[0,1]^d`, log-concave densities; not the exponential regime of a Lipschitz class in growing dimension |
| stability of Harper's inequality | Keevash–Long, arXiv:1807.09618; Przykucki–Roberts, arXiv:1808.02572 | [S] of the main theorems | stability at slack `1 + c/n`, resp. radius `≤ log n/(3 log log n)`: unusable here |
| nested simulation | Broadie–Du–Moallemi, Management Science 57 (2011); Giles–Haji-Ali, arXiv:1802.05016 | [A] | adaptive allocation of inner samples to outer scenarios near a threshold, mean-square analysis; the algorithmic relative of Theorem 11.52 |
| nested sampling, multilevel splitting, product estimators | Skilling (2006); Kahn–Harris; Cérou–Guyader; Huber–Schott | [M] | the layer-cake / level-set idea with a constrained sampler or mixing, which the query model does not provide |
| local search on the cube | Aldous (1983); Aaronson (2004); Zhang (2006) | [M] | hard instances are long level paths, which carry no mass under the oscillation constraint |

*Not found* (abstracts only — "not found", not "new"): a certified (worst-case, one-sided)
version of nested estimation; the use of an isoperimetric tail lemma to close a ladder of
levels; a recursion for worst-case exponents; a statement that adaption recovers exactly
the value of a-priori information (a hint) at the exponential scale.  The identity
`KL(ρ‖p_u) = KL(ρ‖½) + uρ − Λ₁` is an exponential change of measure and is certainly not new;
its use as the fixed-point equation of a recursion over levels was not found.

**Additions by referee R7** (`reviews/R7_referee_report.md`, §6; the referee read no full text):

| source | what it says, as far as read | read how |
|---|---|---|
| Mathé & Novak, *Simple Monte Carlo and the Metropolis algorithm*, J. Complexity 2007 (arXiv math/0611285) | "adaptive methods are much better than nonadaptive ones … the curse of dimension (for nonadaptive methods) can be broken by adaption", for integration against an unknown density that is log-concave with Lipschitz logarithm, by a Metropolis ball walk | abstract (quoted sentences); the body as described in R5 |
| Novak, *On the power of adaption*, J. Complexity 1996 | survey; the power of adaption depends critically on the a-priori knowledge | tool summary of the author's page |
| Sikorski (1982), zero finding; Traub–Wasilkowski–Woźniakowski | adaption exponentially better than non-adaption for a nonlinear problem; no gain for linear problems on convex balanced classes | search summary |
| Kunsch–Novak–Wnuk (arXiv 2308.01705) | gap `n^{1/2}(log n)^{−1/2}`; `√(log m)` against `log log m` in the dimension | abstract excerpts |
| nested sampling (Skilling 2006; Chopin–Robert; Fowlie et al. 2022), adaptive multilevel splitting (Cérou–Guyader et al.), Jerrum–Valiant–Vazirani 1986, Huber–Schott | error estimates asymptotic or heuristic, with a constrained sampler; counting through a split of coordinates / nested level sets with a sampler | search summaries, memory |

Consequence for the classification of Theorem 11.54: **the qualitative phenomenon — adaption
removes an exponential barrier of non-adaptive randomised methods for an
unnormalised-density problem — is known** (Mathé–Novak, for a log-concave class, with a
Markov chain).  Not found: exact exponents on a Hamming–Lipschitz class without concavity,
their coincidence with the hinted exponent, a certified one-sided nested algorithm without
a sampler, the recursion.


**Addendum at the fifth checkpoint of cycle 10** (coordinator; three generic searches on
2026-11-25, *search-engine summaries only — nothing below was opened or read*; recorded so
that a later reader knows what was and was not looked at for §§11.19–11.20):

| what was searched | what came back | bearing |
|---|---|---|
| query complexity of normalising constants for Lipschitz potentials, adaptive against non-adaptive, exponential in the dimension | (i) the *sampling-oracle* line for Gibbs partition functions — cooling schedules, where a query is a sample at a chosen temperature (Štefankovič–Vempala–Vigoda; Kolmogorov; a 2026 preprint "Optimal simulated annealing for partition function estimation", arXiv 2609.20337; another 2026 preprint with separate lower bounds for adaptive and for non-adaptive schedules, arXiv 2604.01263); (ii) quantum lower bounds (Chen–Nannicini, arXiv 2404.02414); (iii) Ge–Lee–Lu 2020 for strongly log-concave integrals | **a different model**: polynomial sample complexity with access to exact Gibbs samplers, where adaptivity of the *schedule* matters by logarithmic factors.  The present results are for value queries to the energy on a worst-case Lipschitz class, where the complexity is exponential and adaptivity changes the exponent.  The adaptive / non-adaptive distinction in that literature should be cited next to Mathé–Novak when §§11.16–11.20 are written up |
| flat-histogram / multicanonical sampling as a minimax-optimal proposal for worst-case estimation of a partition function | descriptions of the multicanonical ensemble (Berg–Neuhaus), Wang–Landau and stochastic-approximation variants (Liang), a 2024 preprint on optimal parameters (Shakirov, arXiv 2402.05653); one summary quotes "there is no rigorous theory for the convergence of the algorithms" | **not found**: a statement that a flat histogram in an order parameter is minimax-optimal among fixed samples for certified estimation over an uncertainty class (Theorem 11.61 in its toy setting).  One search; "not found at this depth", not "new" |
| isoperimetry for a type-uniform mixture on the cube; inherently typical subsets; two measures | only the edge-isoperimetric line of Kahn–Park and Durcik–Ivanisvili–Roos(–Xie) | nothing on the statement of Theorem 11.63; the relevant literature (Ahlswede–Zhang; Yu, arXiv:2205.07596) is the one the workstream and referee R9 were pointed to |


**Addendum at the twelfth checkpoint of cycle 10: what the Scientific Discovery Division found**
(SCI-REV-0004 on branch `research/scientific-translation`, `docs/collaboration/` and
`docs/science/workstreams/A1_REPORT.md` there: full-text reading where accessible, 23 logged
queries, 27 sources with reading levels, own numerical replications; "verified by us" below
means by the theory division, through a page fetch of the arXiv HTML versions on 2026-11-25).

| source | what it says | bearing on the theory report | verified by us |
|---|---|---|---|
| D. Hasenclever, M. Scholz, *Comparing measures of association in 2×2 probability tables*, arXiv:1302.6161 (2013); Open Stat. Probab. J. 7 (2016) | Proposition 8(a): in the coordinates `x = ln√(odds ratio)`, `y`, `z` (margins) the signed mutual information at fixed `x ≠ 0` has exactly one maximum, at `(y, z) = (0, 0)`, the table with uniform margins | **Lemma 11.89 is known** (§11.25, G27, README item (x) corrected) | statement of Proposition 8 and the parametrisation read in the full text (ar5iv rendering of v1); the proof, in an appendix, not read |
| A. Suárez, R. Silbey, I. Oppenheim, *Phase transition in the Jarzynski estimator of free energy differences*, Phys. Rev. E 85, 051108 (2012), arXiv:1108.5783 | bias of the exponential-average free-energy estimator from `M = e^{γN}` samples for `N` independent two-state units (discrete random energy model): `ΔF = N log(2/(1+e^{−ε}))` (eq. (31)), maximal bias `N log cosh(ε/2)`, a freezing transition in `γ` with closed formulas (eqs. (39)–(46)) | at the cone instance these are `nΛ₁`, the threshold `E` of §11.10, and `θ_na`, `a` of §11.16: **the formulas of G11 and G18 are in print at one instance**; not in print (two divisions' searches): the minimax statements | title, authors, subject, eq. (31) read; `N log cosh(ε/2)` derived from verbatim pieces (`B_max = ⟨W⟩ − ΔF`, `⟨W⟩ = Nε/2`); eqs. (39)–(46) in the division's reading only |
| S. Chatterjee, P. Diaconis, *The sample size required in importance sampling*, Ann. Appl. Probab. 2018 (arXiv:1511.01437) | sample size `e^{KL(target‖proposal)}` necessary and sufficient; Section 3: Gibbs measures (Theorem 3.4 in the division's reading) | bounded-accuracy sample size at the cone; product proposals at cone instances (Theorem 11.61) | abstract and section headings; Theorem 3.4 not read verbatim |
| Z. Karnin, *Verification based solution for structured MAB problems* (NeurIPS 2016); A. Garivier, E. Kaufmann, *Optimal best arm identification with fixed confidence* (COLT 2016) | explore–verify; identification asymptotically as cheap as verification (noisy observations, `δ → 0`) | concept precedent for "adaptive = hinted" (§11.18) | not opened |
| H. Guo, H. Liu, X. Yang, Y. Yin, Y. Zhang, *Optimal simulated annealing for partition function estimation*, arXiv:2609.20337; D. Harris, V. Kolmogorov, H. Liu, Y. Yin, Y. Zhang, *Near-optimal parallel approximate counting via sampling*, arXiv:2604.01263 | sampling-oracle model: non-adaptive annealing with `O(q log²h/ε²)` samples, two rounds of adaptivity with `O(q log h/ε²)`; lower bounds for general and non-adaptive algorithms | rounds for partition functions exist in another oracle model, at polynomial scale, with the opposite conclusion (§11.24) | abstracts |
| Novak (1995) as quoted in Krieg–Novak–Ullrich (2025), §6.1; Kiefer (1959), Idais–Schwabe (invariant designs); Beh–Morio (2026); Williams (2022), eq. (10) | adaption helps polynomially in the cardinality for convex non-symmetric classes; invariant designs are optimal; minimax proposals; the mutual information at uniform margins | §11.18 remark (5); Theorem 11.76; §11.20 | not opened |

The division's classification of the eight claims it examined is reproduced in theory
report §10 ("An independent assessment of originality").  Its unresolved questions: whether
one of Novak's 1995 examples is structurally the cube example; whether the hinted exponent
has a counterpart in the random-energy-model literature; the first source of the capacity
phrasing of the odds-ratio lemma.

