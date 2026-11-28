# Prior-art verification (web), items (1)-(5)

Bounded search, about 45 web searches and 12 page fetches. **How well each claim is verified** (every entry carries one tag):

- **[opened]**: I read the abstract or publisher/arXiv page (or the paper's HTML text) myself with a fetch tool.
- **[index]**: the bibliographic data (authors, title, venue, volume, pages, DOI) come from search-engine summaries of publisher or database records (Project Euclid, AMS, RePEc/IDEAS, dblp, PubMed, Econometric Society) that I did not open. The data agree across those records, but I did not read the text. Content claims tagged [index] are abstract-level only.
- **[unverified]**: recalled from background knowledge, or a detail the records did not show. Do not cite it without checking.

I quote no theorem numbers or constants unless I saw them on an opened page. I could not parse PDFs in this environment, so I read no full PDF text.

---

## A. Lift zonoids, zonoid trimming, moment bodies of bounded densities

1. **G. Koshevoy, K. Mosler, "Zonoid trimming for multivariate distributions", Ann. Statist. 25(5) (1997) 1998–2017.** [index] The paper builds trimmed regions and a data depth (zonoid depth) on the lift zonoid. It also gives a trimming transform that maps a distribution to one with a unique median.
   - [unverified, recalled] The α-trimmed region is D_α(μ) = { ∫ x g(x) dμ(x) : 0 ≤ g ≤ 1/α, ∫ g dμ = 1 }.
   - *Relation:* if that definition is right, D_α is exactly the set of **normalised** moments under a density-ratio class with l = 0 and u = μ/α. Item (1) in the normalised form (l = 0, constant u/ref ratio) is then contained here. Check the definition in the paper.
2. **G. Koshevoy, K. Mosler, "Lift zonoids, random convex hulls and the variability of random vectors", Bernoulli 4(3) (1998).** [index; pages unverified] The lift zonoid of X is the zonoid of the lifted vector (1, X) ∈ R^{d+1}. It determines the distribution of an integrable X uniquely, and inclusion of lift zonoids defines a variability order.
3. **M.-A. Diaye, G. A. Koshevoy, I. Molchanov, "Lift expectations of random sets", Statistics & Probability Letters (arXiv:1805.04757).** [opened] States the definition Ẑ_ξ = E[(0,0),(1,ξ)], the selection (Aumann) expectation of a random segment. It gives the support function h(u₀,u) = E(u₀ + ⟨ξ,u⟩)_+, the "stop-loss transform". It credits the concept to Koshevoy–Mosler (1998) and Mosler (2002), and the uniqueness result to Hardin (1981).
   - *Relation:* this is item (1)'s support function with l = 0 and u = 1. For general l, K = Σ l·v + Σ (u−l)·[0, v(x)], a translate of a (weighted) lift zonoid. The formula h_K(λ) = Σ[u(λ·v)_+ − l(λ·v)_−] follows in one line from this.
4. **K. Mosler, *Multivariate Dispersion, Central Regions and Depth: The Lift Zonoid Approach*, Springer Lecture Notes in Statistics 165 (2002).** [unverified bibliographic data, recalled]
   - Convergence of empirical regions: arXiv:1611.08721 ("Convergence of depths and depth-trimmed regions"; authors not recorded) [opened, Example 4.3]. Citing Mosler (2002), it says empirical zonoid regions converge **almost surely pointwise** to the population regions. This yields uniform convergence of the empirical zonoid depth and compact (and Hausdorff) convergence of trimmed regions for distributions with a density. **No rates** are stated.
   - It also cites Cascos and López-Díaz (2016), "On the uniform consistency of the zonoid depth", J. Multivariate Anal. [index; volume unverified].
   - In the literature I could reach, I found **no explicit finite-sample Hausdorff rate for the empirical lift zonoid**.
5. **E. D. Bolker, "A class of convex bodies", Trans. AMS 145 (1969) 323–345** (some citing works give 323–346). [index] This is the standard early reference on zonoids. Lyapunov's convexity theorem (A. A. Lyapunov, 1940) is [unverified]: I did not retrieve its record.
6. **Markov L-problem.** [index] Two monographs:
   - M. G. Krein, A. A. Nudelman, *The Markov Moment Problem and Extremal Problems*, AMS Transl. Math. Monographs 50 (DOI 10.1090/mmono/050). Its contents include the Chebyshev–Markov problem and "the abstract L-problem and duality principle".
   - N. I. Akhiezer, M. G. Krein, *Some Questions in the Theory of Moments*, AMS Transl. Math. Monographs 2 (1962). Chapter 1 is "The L-problem of moments".
   - Secondary sources (arXiv:1304.1716, found by search, not opened) state the content: moments of φ with 0 ≤ φ ≤ L; by L¹–L^∞ duality, extreme points of the feasible set are indicators χ_{p<γ} of polynomial sublevel sets.
   - *Relation:* this is the bang-bang structure of item (3) for l = 0, u = L·Lebesgue on an interval, with polynomial φ. Chapter or theorem numbers are [unverified].

**Verdict A:** Item (1) is classical. K is a Minkowski sum of segments, i.e. the Aumann expectation of a random segment, a translated lift zonoid. Its support function is the "stop-loss transform" formula. Koshevoy–Mosler's zonoid-trimmed regions are (recalled, not verified) the normalised version with l = 0, u ∝ ref. The extreme-point/bang-bang structure is the L-problem of moments.

## B. Approximating zonoids by zonotopes

1. **J. Bourgain, J. Lindenstrauss, V. Milman, "Approximation of zonoids by zonotopes", Acta Math. 162 (1989) 73–141, DOI 10.1007/BF02392835.** [index] Asks for the minimal number of segments N that approximate a zonoid in R^n within (1+ε) (multiplicative, Banach–Mazur-type). Their method is random sampling with a change of density. The exact form of their general bound is [unverified]: I could not open the paper.
2. **M. Talagrand, "Embedding subspaces of L₁ into ℓ₁^N", Proc. AMS 108 (1990) 363–369.** [index] The AMS abstract snippet says an n-dimensional subspace X ⊂ L₁ is (1+ε)-isomorphic to a subspace of ℓ₁^N once N ≥ C·K(X)²ε⁻²n. Here K(X) is a constant attached to X; its definition was cut off in the snippet [unverified]. Cohen–Peng [opened] attribute to Talagrand "samples of size O(d log d)" for ℓ₁.
3. **G. Schechtman, "Fine embeddings of finite-dimensional subspaces of L_p, 1 ≤ p < 2, into ℓ₁^m", Proc. AMS 94 (1985).** [index] An earlier, weaker result for L₁. The exact bound is [unverified].
4. **J. Matoušek, "Improved upper bounds for approximation by zonotopes", Acta Math. 177 (1996) 55–73, DOI 10.1007/BF02392598.** [index] A secondary source (arXiv:math/0608011) reports N(n,ε) = O(ε^{−2(n−1)/(n+2)}) for n ≥ 5. This is the fixed-dimension, small-ε regime of Hausdorff (multiplicative) approximation of the ball/zonoids.
5. **M. B. Cohen, R. Peng, "ℓ_p Row Sampling by Lewis Weights", arXiv:1412.0588 (STOC 2015).** [opened] Gives Theorem 1.1: O(d log d · ε⁻²) rows; Theorem 2.3: O(d log(d/ε) ε⁻²) with approximate Lewis weights. The guarantee is ‖SAx‖₁ ≈_{1+ε} ‖Ax‖₁ **for all x**, which is multiplicative. Sampling is proportional to **ℓ₁ Lewis weights**, not to row length. The STOC venue comes from a citing paper (arXiv:2207.08268); the arXiv page shows no journal-ref.
6. Related identification-side result: **A. Beresteanu, F. Molinari, "Asymptotic properties for a class of partially identified models", Econometrica 76(4) (2008) 763–814.** [index] The sample Minkowski average of set-valued variables converges in Hausdorff distance to the Aumann expectation, which is the identification region. Then √n·Hausdorff distance converges to the sup of a Gaussian process on the sphere, using support functions.

**Verdict B:**
- BLM, Talagrand and Cohen–Peng prove the **stronger, multiplicative** statement: h_Z(λ) within (1±ε)·h_K(λ) for all λ. They need **non-uniform (Lewis-weight) sampling** to get N ≈ d log d/ε².
- Item (2) is a weaker **additive ℓ∞/Hausdorff** guarantee with plain sampling q ∝ (u−l)·ref. It is the uniform law of large numbers for a Minkowski average of i.i.d. random segments: Artstein–Vitale-type SLLN [unverified bibliographic data], with rates in Beresteanu–Molinari.
- The class {x ↦ (λ·v(x))_+ : ‖λ‖ ≤ 1} is a d-parameter Lipschitz family, so either the net bound d·log(1/ε)/ε² or a Rademacher bound is routine empirical-process theory.
- The "log d" Rademacher version needs the ℓ1 dual geometry: sup over ‖λ‖₁ ≤ 1 for an ℓ∞ guarantee. This is a standard contraction argument.
- I found no paper stating item (2) verbatim. I judge it to be known under other names: "empirical approximation of zonoids", "Hausdorff convergence of Minkowski averages".

## C. Density-ratio classes and their extremal bounds

1. **L. DeRobertis, J. A. Hartigan, "Bayesian inference using intervals of measures", Ann. Statist. 9(2) (1981) 235–244, DOI 10.1214/aos/1176345391.** [index] Prior knowledge is an interval I(L,U) of σ-finite measures. The paper gives upper and lower posterior expectations and their strong consistency. The first author's name is spelled DeRobertis or De Robertis in different records.
   - *Relation:* this is exactly the class l ≤ w ≤ u. The sup of a ratio ∫fw/∫w over it is the bang-bang/threshold solution of item (3) **without** moment constraints.
2. **M. Lavine, "Sensitivity in Bayesian statistics: the prior and the likelihood", JASA 86 (1991) 396–399, DOI 10.1080/01621459.1991.10475055**, and **M. Lavine, "An approach to robust Bayesian analysis for multidimensional parameter spaces", JASA 86 (1991), DOI 10.1080/01621459.1991.10475056** (density-bounded classes). [index]
3. **L. Wasserman, M. Lavine, R. L. Wolpert, "Linearization of Bayesian robustness problems", J. Statist. Plann. Inference 37(3) (1993) 307–316, DOI 10.1016/0378-3758(93)90109-J.** [index] The abstract says a single nonlinear (ratio) optimisation becomes a family of linear ones, with prior constraints added sequentially.
   - *Relation:* this is the "smallest τ with sup Σ w(f−τ) ≤ 0" step of item (3) (Dinkelbach/Charnes–Cooper-type).
4. **L. Wasserman, "Invariance properties of density ratio priors", Ann. Statist. 20(4) (1992) 2177–2182, DOI 10.1214/aos/1176348912.** [index] A secondary source says it shows the density-ratio class is the only class closed under Bayesian updating and marginalisation [unverified content].
5. **J. Geweke, L. Petrella, "Prior density-ratio class robustness in econometrics", J. Bus. Econ. Statist. 16(4) (1998) 469–478, DOI 10.2307/1392615.** [index] Gives a fast generic method for **exact density-ratio bounds on posterior expectations computed from posterior-simulator output**.
   - *Relation:* the sample-based (Monte Carlo) version of the unconstrained problem in item (3). The records show no certificate or finite-sample guarantee.
6. **B. Betrò et al., generalized moment classes, Ann. Inst. Statist. Math. 58 (2006), DOI 10.1007/s10463-006-0046-8.** [index; title and coauthors unverified] Posterior bounds over priors with generalized moment constraints reduce to linear semi-infinite programming.
7. **J. O. Berger et al., "An overview of robust Bayesian analysis" (with discussion), TEST 3(1) (1994) 5–124, DOI 10.1007/BF02562676.** [index] I could not confirm its density-ratio content.
8. **G. B. Dantzig, A. Wald, "On the fundamental lemma of Neyman and Pearson", Ann. Math. Statist. 22(1) (1951) 87–93, DOI 10.1214/aoms/1177729695.** [index] Proves existence and a necessary and sufficient condition for the generalised NP problem: maximise ∫φ f₀ subject to ∫φ f_i = c_i, 0 ≤ φ ≤ 1. The optimum is φ = 1 where f₀ > Σ k_i f_i and 0 where it is below.
   - *Relation:* with w = l + (u−l)φ, item (3) with **equality** moment constraints is an instance of this. Box/ellipsoid moment sets R give the h_R(η) term by conjugacy. Lehmann–Romano's textbook statement is [unverified], not retrieved.

**Verdict C:** The bang-bang form of item (3) is classical:
- Generalised NP lemma / L-problem duality.
- DeRobertis–Hartigan for the unconstrained ratio.
- Lavine-type linearisation for the ratio (the τ-root).
- Moment-constrained robust-Bayes classes (Betrò) via semi-infinite LP.

I did not find a single source that states the **combined** form: density-ratio class plus normalised moments in a convex set R, with h_R(η) in the score. It is a direct consequence of the above.

## D. Marginal sensitivity model (MSM)

1. **Z. Tan, "A distributional approach for causal inference using propensity scores", JASA 101(476) (2006) 1619–1637, DOI 10.1198/016214506000000023.** [index] Introduces the MSM: the odds ratio of the true versus the nominal propensity is bounded by Γ. Equivalently, the inverse-propensity weights lie in a known interval [l(x), u(x)], which is a density-ratio class.
2. **Q. Zhao, D. S. Small, B. B. Bhattacharya, "Sensitivity analysis for inverse probability weighting estimators via the percentile bootstrap", JRSSB 81(4) (2019) 735–761.** [index] The bounds are **linear-fractional programs** over bounded weights, i.e. exactly the ratio Σwf/Σw with l ≤ w ≤ u. They are solved by sorting/thresholding. Uncertainty comes from the **percentile bootstrap**, which is asymptotic, via a generalized minimax inequality.
3. **J. Dorn, K. Guo, "Sharp sensitivity analysis for inverse propensity weighting via quantile balancing", JASA 118(544) (2023) 2645–2657, DOI 10.1080/01621459.2022.2069572, arXiv:2102.04543.** [opened arXiv page]
   - ZSB's interval is conservative even asymptotically.
   - Their sharp bounds impose the infinite family of balancing constraints implied by the observed distribution, i.e. conditional moment constraints. The resulting weights are thresholded at a conditional quantile ("quantile balancing").
   - Confidence intervals come from the ZSB bootstrap, which is asymptotic.
4. **J. Dorn, K. Guo, N. Kallus, "Doubly-valid/doubly-sharp sensitivity analysis for causal inference with unmeasured confounding", JASA 120(549) (2025) 331–342, DOI 10.1080/01621459.2024.2335588, arXiv:2112.11449.** [index] Gives DML-type estimators of the sharp bounds and Wald CIs that remain valid but conservative under misspecification. These are asymptotic.
5. Related:
   - K. Ishikawa, N. He, T. Kanamori, "A convex framework for confounding robust inference", arXiv:2309.12450, extending PMLR v206 (2023). [opened] Sharp bounds by convex programming and strong duality; the estimator written as ERM; guarantees via M-estimation. The abstract does not say whether they are finite-sample.
   - X. Nie, G. Imbens, S. Wager, "Covariate balancing sensitivity analysis for extrapolating randomized trials across locations", arXiv:2112.04723. [opened] Tighten the bounds from the optimisation by **balancing covariate moments**, i.e. bounded weights plus moment constraints. Abstract-level only.
   - Y. Jin, Z. Ren, E. J. Candès, arXiv:2111.12161. [opened] Robust conformal prediction sets under the MSM: **finite-sample marginal coverage** when the propensity is known, approximate when it is estimated. Prediction of individual outcomes, not sharp bounds on averages.
   - M. Yin, C. Shi, Y. Wang, D. Blei, arXiv:2112.03493 (JASA 2022). [index] Conformal sensitivity analysis with finite-sample guarantees for individual treatment effects.

**Verdict D:** The MSM optimisation is the **same mathematical object** as item (3): a ratio under l ≤ w ≤ u, thresholding, and balancing/moment constraints (Dorn–Guo, Nie–Imbens–Wager). The only setting difference is that the weights act on an empirical sample rather than on a known reference model.
- The inference there is **asymptotic** (bootstrap, Wald).
- The finite-sample-valid MSM work I found is conformal and about individual outcomes, not about sharp bounds on population averages.
- I did not find a finite-sample certificate of the item-(4) kind (a fixed dual pair checked by one Hoeffding/empirical-Bernstein test) in the MSM literature. That absence is limited to the reach of this search.

## E. Certifying stochastic-programme bounds with a validation sample

1. **W.-K. Mak, D. P. Morton, R. K. Wood, "Monte Carlo bounding techniques for determining solution quality in stochastic programs", Oper. Res. Lett. 24 (1999) 47–56, DOI 10.1016/S0167-6377(98)00054-6.** [index] Two parts:
   - The SAA optimal value gives a statistical lower bound (minimisation) that is monotone in the sample size.
   - A **fixed candidate solution evaluated on an independent sample** gives the other bound, and the two together give one-sided CIs on the optimality gap. These rest on the CLT/t-intervals.
2. **G. Bayraksan, D. P. Morton, "Assessing solution quality in stochastic programs", Math. Program. 108 (2006) 495–514, DOI 10.1007/s10107-006-0720-x.** [index] Single- and two-replication procedures for gap CIs. These are asymptotically valid; single-replication coverage can be low at small n.
3. **A. Shapiro, D. Dentcheva, A. Ruszczyński, *Lectures on Stochastic Programming* (SIAM).** [unverified edition and pages; not retrieved]
4. Related:
   - P. W. Glynn, G. Infanger, "Simulation-based confidence bounds for two-stage stochastic programs", Math. Program. (2013). [index; title unverified]
   - Chu, Hunter, Pasupathy, primal–dual resampling, Optimization Online 2025. [index; title unverified] Builds statistical upper and lower bounds at a candidate primal–dual pair.
   - Daryalal, Bodur, Luedtke, arXiv:2001.00761. [opened] Uses **deterministic** Lagrangian relaxation bounds. The page does not support the claim, from a search-engine summary, that it gives statistically valid out-of-sample dual bounds.
5. **Concentration inequalities.**
   - A. Maurer, M. Pontil, "Empirical Bernstein bounds and sample variance penalization", COLT 2009, arXiv:0907.3740. [index]
   - J.-Y. Audibert, R. Munos, Cs. Szepesvári, "Exploration–exploitation tradeoff using variance estimates in multi-armed bandits", Theor. Comput. Sci. 410(19) (2009) 1876–1902, DOI 10.1016/j.tcs.2009.01.016. [index]
   - I. Waudby-Smith, A. Ramdas, "Estimating means of bounded random variables by betting", JRSSB 86(1) (2024) 1–27 (RSS discussion paper), arXiv:2010.09686. [index] The DOI is probably 10.1093/jrsssb/qkad009 [unverified: records conflict with the discussion DOIs].

**Verdict E:** The **pattern** of item (4) is standard in SAA validation:
- Fix a candidate found on one sample.
- Estimate a single expectation on an independent sample.
- Get a one-function confidence bound with no uniformity over the decision space.

Mak–Morton–Wood use CLT intervals. Swapping in Hoeffding, empirical-Bernstein or betting CIs for finite-sample validity is a routine strengthening.

Applying the pattern to a **dual feasibility test** E[U s₊ − L s₋] ≤ 0 is a direct instance of weak duality plus that recipe. I did not find that specific test stated anywhere.

## F. DRO with likelihood-ratio / φ-divergence sets plus moments

1. **A. Ben-Tal, D. den Hertog, A. De Waegenaere, B. Melenberg, G. Rennen, "Robust solutions of optimization problems affected by uncertain probabilities", Manag. Sci. 59(2) (2013) 341–357, DOI 10.1287/mnsc.1120.1641.** [index] Robust linear optimisation over φ-divergence balls, which arise as confidence sets; tractable robust counterparts.
2. **J. C. Duchi, H. Namkoong, "Learning models with uniform performance via distributionally robust optimization", Ann. Statist. 49(3) (2021) 1378–1406, DOI 10.1214/20-AOS2004.** [index] Worst case over D_f(Q‖P) ≤ ρ. Bounded-likelihood-ratio balls (f = indicator of [0, 1/α]) give the CVaR. The CVaR link is stated in related papers of the same group [index]; I did not confirm it in this paper.
3. **Z. Wang, P. W. Glynn, Y. Ye, "Likelihood robust optimization for data-driven problems", Comput. Manag. Sci. 13(2) (2016) 241–261, DOI 10.1007/s10287-015-0240-3, arXiv:1307.6279.** [index] The ambiguity set contains the distributions under which the data reach a likelihood level.
4. **A. Shapiro, "Distributionally robust stochastic programming", SIAM J. Optim. 27(4) (2017) 2258–2275.** [index] Reference measure plus an ambiguity set: φ-divergence, Wasserstein, moment constraints, and links to coherent risk measures.
5. **R. T. Rockafellar, S. Uryasev, "Optimization of conditional value-at-risk", J. Risk 2 (2000) 21–41/42.** [index; issue number inconsistent across records]
   - The dual representation CVaR_α(Z) = sup{E_Q Z : 0 ≤ dQ/dP ≤ 1/α} = min_β {β + α⁻¹E(Z−β)₊} is stated in several sources the search found (e.g. arXiv:1502.06155, not opened). Mind the α versus 1−α convention.
   - *Relation:* the general density-ratio-class sup in item (3) is a two-sided generalisation of that formula. With w ∈ [l,u] and no moment constraints, sup Σ w(f−τ) = Σ[u(f−τ)₊ − l(f−τ)₋]. The τ-root of this is a "CVaR-type" (Rockafellar–Uryasev) formula with general bounds.
6. Bertsimas et al., "Distributionally robust causal inference with observational data", arXiv:2210.08326. [index] Reported to contain the MSM as a special case.

**Verdict F:** Bounded-likelihood-ratio ambiguity sets (the CVaR envelope), φ-divergence sets, and their combination with moment constraints are standard DRO. Item (3) is, in DRO language, a **likelihood-ratio-box ambiguity set with moment constraints** and a fractional (normalised) objective.

## G. Model-form UQ in statistical mechanics

1. **P. Dupuis, M. A. Katsoulakis, Y. Pantazis, P. Plecháč, "Path-space information bounds for uncertainty quantification and sensitivity analysis of stochastic dynamics", SIAM/ASA J. UQ (2016), DOI 10.1137/15M1025645, arXiv:1503.05136.** [index] Bounds on observables through relative entropy rate and path-space Fisher information.
2. **M. A. Katsoulakis, L. Rey-Bellet, J. Wang, "Scalable information inequalities for uncertainty quantification", J. Comput. Phys. 336 (2017) 513–545, arXiv:1605.04184.** [index] Goal-oriented variational bounds: |E_Q f − E_P f| is controlled by KL(Q‖P) and the cumulant generating function of f under P. Applied to **phase diagrams of statistical-mechanics (lattice) models**.
3. **K. Gourgoulias, M. A. Katsoulakis, L. Rey-Bellet, J. Wang, "How biased is your model? Concentration inequalities, information and model bias", IEEE Trans. Inf. Theory 66(5) (2020), arXiv:1706.10260.** [index] Computable bias bounds via KL plus Bennett/Hoeffding-type concentration, and confidence bands valid for any amount of data.

**Relation:** for Gibbs measures with |E − E₀| ≤ δ pointwise, the density ratio dP/dP₀ lies in [e^{−2βδ}, e^{2βδ}] after normalisation. The unnormalised weights e^{−βE} lie in [e^{−β(E₀+δ)}, e^{−β(E₀−δ)}]. This is exactly item (1)'s class.
- The Katsoulakis et al. bounds use a **KL ball** (via the Donsker–Varadhan variational formula), a different ambiguity set.
- They do not use experimental moment constraints.
- A KL/Rényi bound implied by a pointwise energy bound is looser than the exact density-ratio bound of item (3).

I did not find work that computes the exact sup and inf of a Gibbs average under a pointwise energy envelope combined with measured ensemble averages. Searches for "rigorous"/"certified" free-energy-perturbation bounds turned up nothing relevant.

## H. Ensemble reweighting against experimental averages

1. **J. W. Pitera, J. D. Chodera, "On the use of experimental observations to bias simulated ensembles", J. Chem. Theory Comput. 8 (2012) 3445–, DOI 10.1021/ct300112v.** [opened: Chodera lab page] Maximum-entropy biasing; a linear restraint gives the minimally biased ensemble.
2. **B. Roux, J. Weare, "On the statistical equivalence of restrained-ensemble simulations with the maximum entropy method", J. Chem. Phys. 138(8) (2013) 084107, DOI 10.1063/1.4792208.** [index]
3. **G. Hummer, J. Köfinger, "Bayesian ensemble refinement by replica simulations and reweighting", J. Chem. Phys. 143(24) (2015) 243150 (BioEn), arXiv:1509.04447.** [index] For discrete configurations the optimum equals EROS (maximum entropy).
4. **S. Bottaro, T. Bengtsen, K. Lindorff-Larsen, "Integrating molecular simulation and experimental data: a Bayesian/maximum entropy reweighting approach" (BME).** [index] bioRxiv 10.1101/457952. Probably also Methods Mol. Biol. (2020), DOI 10.1007/978-1-0716-0270-6_15 [unverified: the Springer page redirected to login].
5. **M. Bonomi, C. Camilloni, A. Cavalli, M. Vendruscolo, "Metainference: a Bayesian inference method for heterogeneous systems", Sci. Adv. 2(1) (2016) e1501177, DOI 10.1126/sciadv.1501177.** [index]
6. **I. Bertini et al., "Conformational space of flexible biological macromolecules from average data", J. Am. Chem. Soc. 132 (2010) 13553–13558, DOI 10.1021/ja1063923** ("maximum occurrence", MaxOcc). [index; full author list not retrieved]
   - The **largest population a given conformation can have while the ensemble still reproduces the measured averages**, applied to calmodulin (SAXS plus paramagnetic NMR).
   - **This is the closest structural-biology precedent for an identified-set statement.** It is an extremal (LP-type) bound over all ensembles compatible with the averages, with only nonnegativity (no energy envelope).
   - It bounds the weight of a conformation, not a general second observable.
7. A recent Bayesian treatment of non-uniqueness: "Bayesian sampling of structural ensembles: the role of ensemble-counting measures", arXiv:2606.18495. [index] Bayesian posterior over maximum-entropy ensembles (BELT), where the choice of measure matters. This is distributional, not set-valued.

**Verdict H:** The mainstream methods (maximum entropy, BioEn, BME, metainference, EROS) return a **single** reweighted ensemble or a posterior over ensembles. MaxOcc is a set-valued extremal quantity, but without a reference-energy envelope, for population weights only, and without sampling certificates.
- I found **no method that reports a guaranteed outer interval (identified set) for an unmeasured ensemble average** under a reference-energy envelope plus experimental averages.
- I found no use of Manski-style partial identification language in this field.

## I. Direct searches for the combination

- "partial identification" + ensemble averages/molecular simulation: no relevant hit.
- Density-ratio class + generalized moment constraints + LFP: separate pieces only (Betrò LSIP; Geweke–Petrella).
- Zonoid/zonotope + identified set: the econometric random-set literature has identified sets that are Aumann expectations of random sets, i.e. zonoid-type for random segments:
  - Beresteanu–Molinari (2008);
  - Beresteanu, Molchanov, Molinari, "Partial identification using random set theory", J. Econometrics 166(1) (2012) 17–32 [index];
  - C. Bontemps, T. Magnac, E. Maurin, "Set identified linear models", Econometrica 80(3) (2012) 1129–1155, DOI 10.3982/ECTA7637 [index]. Identified set and support-function tests for linear moments with an unknown bounded function. The records do not say "zonotope", although the set is a linear image of an interval box.
- Cortes-Gomez, Dulce, Patino, Wilder, "Statistical inference under constrained selection bias", arXiv:2306.03302. [opened] Gives high-probability bounds on a target estimand under distribution shift constrained by known target moments. This is a close cousin of items (3)–(4) in ML; the exact ambiguity set is not given in the abstract.
- "Random zonotope" + moment set: nothing beyond the zonotope-vertex sampling paper arXiv:1602.06620 [index], which is unrelated.

---

## Assessment

**(i) Textbook / classical**
- **Item (1).** The moment set of a density-ratio (interval-of-measures) class is a translate of a weighted lift zonoid: the Aumann expectation of a random segment [l v, u v]. Its support function is the stop-loss formula. The continuous case is a zonoid (Lyapunov/Bolker); the finite case is a zonotope. Koshevoy–Mosler and Mosler 2002 contain the l = 0 case (and, as recalled, the normalised trimmed-region version). The general (l, u) case is a translation. Nothing new.
- **Item (3), the bang-bang and τ-root structure.** This is the generalised Neyman–Pearson lemma (Dantzig–Wald 1951), the Markov L-problem (Akhiezer–Krein; Krein–Nudelman), and DeRobertis–Hartigan upper posterior expectations with Lavine/Wasserman linearisation of the ratio. Moment constraints enter as Lagrange multipliers. A convex set R gives the support-function term h_R(η) by standard conjugate duality. The precise combined statement (normalised moments in a box/ellipsoid) was not found verbatim but is a routine corollary.

**(ii) Known in a neighbouring field under another name**
- **Item (2).** This is Hausdorff convergence of Minkowski averages of random segments, i.e. the random-set LLN/CLT (Beresteanu–Molinari 2008 give √n rates through support functions). The zonotope-approximation literature (BLM 1989, Talagrand 1990, Cohen–Peng 2015) proves a stronger multiplicative guarantee with Lewis-weight sampling and about d log d/ε² segments.
  - The additive ℓ∞ version with sampling proportional to (u−l) is weaker and follows from standard empirical-process bounds.
  - The two rates quoted in item (2) are routine; the net bound is "d log(1/ε)/ε²" and the "log d" Rademacher bound is for ℓ1-bounded directions.
  - No explicit finite-sample rate for empirical lift zonoids was found in the zonoid-depth literature, which proves only almost-sure convergence.
- **Item (3) as a whole, in applied form.** This is the MSM sharp-bound problem in causal inference (Tan 2006; ZSB 2019: linear-fractional programs over bounded weights; Dorn–Guo: thresholding plus balancing (moment) constraints) and the CVaR/likelihood-ratio-box DRO problem.
- **Item (4), the pattern.** A fixed candidate plus an independent validation sample plus a one-function confidence bound is Mak–Morton–Wood (1999) / Bayraksan–Morton (2006) SAA validation, with CLT intervals there. Substituting Hoeffding, empirical-Bernstein (Maurer–Pontil; Audibert–Munos–Szepesvári) or betting CIs (Waudby-Smith–Ramdas) is routine.
  - The specific use is not found: checking a **dual pair's feasibility inequality** E[U s₊ − L s₋] ≤ 0 to certify a sharp density-ratio bound under moment constraints, giving finite-sample validity without dimension dependence.
  - The MSM literature uses bootstrap/asymptotic inference for its sharp bounds. The finite-sample MSM work found is conformal and about individual outcomes.
  - So item (4) is best described as a **known recipe applied to a new target**. It is modest but not stated in the sources found.

**(iii) Not found**
- **Item (5).** Pointwise energy envelope around a tractable reference → Boltzmann weights in a density-ratio class → combined with experimental ensemble averages → guaranteed outer interval for another ensemble average, or an inconsistency certificate.
  - Nearest neighbours: Bertini et al. 2010 "maximum occurrence" (extremal populations compatible with averaged data, no energy envelope, no second observable); Katsoulakis–Rey-Bellet et al. (KL-ball bounds on Gibbs observables, no experimental constraints); maximum-entropy/Bayesian reweighting (point or posterior ensembles, not identified sets).
  - The **combination** (density-ratio class from an energy envelope + experimental moment constraints + identified interval + sample-based certificate) was not found in any of the fields searched, within the limits of this search.

Caveats: about 45 searches, and no full PDF could be parsed. "Not found" means not found by these searches. Several [index] items need a direct look before citing exact statements: Koshevoy–Mosler's trimmed-region definition, BLM's and Talagrand's exact bounds, and Lehmann–Romano.

## Searches run (generic terms only)

1. Koshevoy Mosler lift zonoid zonoid trimming
2. Bourgain Lindenstrauss Milman approximation of zonoids by zonotopes Acta Mathematica 1989
3. DeRobertis Hartigan 1981 Bayesian inference using intervals of measures
4. Dorn Guo sharp sensitivity analysis inverse propensity weighting quantile balancing
5. Zhao Small Bhattacharya sensitivity analysis IPW percentile bootstrap JRSSB 2019
6. empirical lift zonoid uniform convergence Hausdorff rate zonoid trimmed regions consistency
7. Markov L-problem of moments densities bounded between 0 and L Krein Nudelman
8. Bolker "a class of convex bodies" zonoids Trans AMS 1969
9. Cohen Peng "Lp row sampling by Lewis weights"
10. Lavine 1991 sensitivity in Bayesian statistics density bounded class
11. Wasserman 1992 invariance properties of density ratio priors
12. Dantzig Wald 1951 fundamental lemma of Neyman and Pearson
13. Dorn Guo Kallus doubly-valid doubly-sharp sensitivity analysis
14. marginal sensitivity model finite-sample valid confidence bounds conformal
15. Tan 2006 distributional approach causal inference propensity scores
16. marginal sensitivity model moment constraints covariate balance sharp bounds linear program
17. Mak Morton Wood 1999 Monte Carlo bounding techniques stochastic programs
18. Bayraksan Morton assessing solution quality in stochastic programs
19. Maurer Pontil empirical Bernstein bounds sample variance penalization
20. Waudby-Smith Ramdas estimating means of bounded random variables by betting
21. (same) JRSSB volume/DOI check
22. Audibert Munos Szepesvári variance estimates multi-armed bandits
23. stochastic programming Lagrangian dual bound independent sample confidence interval dual certificate
24. Wang Glynn Ye likelihood robust optimization
25. Ben-Tal et al. robust solutions uncertain probabilities 2013
26. CVaR dual representation densities bounded by 1/alpha risk envelope
27. Dupuis Katsoulakis Pantazis Plecháč path-space information bounds
28. Gourgoulias Katsoulakis Rey-Bellet Wang how biased is your model
29. bounds on ensemble averages under pointwise bounded energy error / rigorous FEP bound
30. Katsoulakis Rey-Bellet Wang scalable information inequalities phase diagrams
31. Hummer Köfinger Bayesian ensemble refinement BioEn
32. Bottaro Bengtsen Lindorff-Larsen Bayesian/maximum entropy reweighting
33. ensemble reweighting bounds on unobserved observable non-uniqueness linear programming (extended)
34. Bertini Luchinat maximum occurrence conformations from average data
35. Bayesian sampling of structural ensembles ensemble-counting measures
36. Pitera Chodera use of experimental observations to bias simulated ensembles
37. Roux Weare restrained-ensemble maximum entropy equivalence
38. Bonomi Camilloni Cavalli Vendruscolo metainference
39. "partial identification" ensemble averages molecular simulation identified set reweighting
40. robust Bayesian density ratio class generalized moment constraints LFP
41. Lavine Wasserman Wolpert linearization of Bayesian robustness problems
42. Geweke Petrella prior density-ratio class robustness econometrics
43. Bontemps Magnac Maurin set identified linear models
44. Beresteanu Molinari asymptotic properties partially identified models
45. Talagrand embedding subspaces of L1 into l1^N
46. Matoušek improved upper bounds approximation by zonotopes
47. Akhiezer Krein some questions in the theory of moments L-problem
48. Berger 1994 overview of robust Bayesian analysis
49. Shapiro 2017 distributionally robust stochastic programming
50. Rockafellar Uryasev optimization of conditional value-at-risk
51. zonoid identified set partial identification random zonotope moment set
52. Duchi Namkoong uniform performance DRO
