# Workstream A1 — prior art and originality of the query-complexity cluster

Read `docs/science/workstreams/COMMON.md` first.  Your directory:
`experiments/science/ws_A1/`; your report: `docs/science/workstreams/A1_REPORT.md`.

## Why this workstream exists

The theory division's strongest claims are about the **query complexity of estimating
`ln Z` (and certifying `min`) over a Lipschitz-type class of energy perturbations** (theory
report §10 rows G11, G12, G18–G23, G25–G27; §§11.10, 11.16–11.21, 11.23–11.25).  The division's
own novelty assessments for these rows say, again and again, "abstracts only", "search
summaries only", "not found in two searches", "may be folklore".  Before anyone invests in a
publication, an independent originality investigation with full-text reading is needed.  A
strong negative novelty finding is a success for this workstream.

## Claims to test (read the exact statements in the theory report before searching)

1. **G20/G21 — "adaptivity replaces the hint".**  On the class
   `{g : {0,1}ⁿ → ℝ, |g(x) − g(y)| ≤ c·d_H(x,y)}` (known part zero), for randomised algorithms
   that evaluate `g` and must output `ln Σ_x e^{−βg(x)}` within `ε` with probability `1−δ`
   for *every* class member: the worst-case exponent (in `n`) of **adaptive** algorithms is
   `θ_hint = KL((Λ₁+ε₁)/u ‖ ½)` — the same as for algorithms that are told the instance and
   only have to verify it — while **non-adaptive** ones have the strictly larger
   `θ_na = min{KL(ρ‖½) : KL(ρ‖p_u) ≤ ε₁}` (`u = βc`, `p_u = 1/(1+e^{u})` or its complement, `Λ₁`
   the single-site soft gap; Theorems 11.44, 11.45, 11.54, 11.58).
2. **G18** — Monte Carlo is exponent-optimal among non-adaptive algorithms on the cube class
   (method attributed to Mathé–Novak 2007).
3. **G22** — with a product (field) known part: the optimal fixed sample is uniform on type
   classes ("flat histogram"), not the Gibbs measure; hardest instance is additive, not zero;
   an asymptotic isoperimetric theorem for the type-uniform reference (Theorem 11.63).
4. **G23** — the "shear law" `x_na(θ) = e_hint(θ) + θ` and the game-function pair theorem.
5. **G25** — for exchangeable known parts, by symmetry alone, type-stratified sampling is
   optimal among fixed samples up to a polynomial factor, for every `n`; shells in the
   barrier class as extremal perturbations at phase coexistence.
6. **G26** — a round hierarchy: two rounds strictly between non-adaptive and fully adaptive.
7. **G27 / Lemma 11.89** — among pairs of binary random variables with a given odds ratio the
   mutual information is largest when both marginals are uniform (equivalently: among
   binary-input binary-output channels with a fixed odds ratio, the symmetric one has the
   largest capacity).  The report says this "may well be folklore".
8. **G11** — the accuracy threshold `ε = n ln cosh(βc/2)` on the cube class separating bounded
   from exponential randomised cost; the "soft gap".

## Literatures you must actually open (not exhaustive; find what we do not know)

* Information-based complexity of integration and of normalising constants: Novak;
  Mathé–Novak 2007 ("Simple Monte Carlo and the Metropolis algorithm"); Rudolf; Heinrich;
  Kunsch–Novak–Wnuk on adaption; Novak–Woźniakowski "Tractability of Multivariate Problems".
* Lower bounds for estimating log-partition functions / normalising constants from
  function or gradient queries: Holzmüller–Bach 2025 (the theory report's closest citation —
  read it in full and compare regimes: is `ln cosh` there? is the cube case a corollary?);
  Ge–Lee–Lu 2020; Chewi et al. on query complexity of sampling; "partition function
  estimation" with sampling oracles (Štefankovič–Vempala–Vigoda; Huber; Kolmogorov 2018;
  Harris–Kolmogorov) — different oracle, but check adaptive vs non-adaptive statements.
* Importance sampling sample size (Chatterjee–Diaconis 2018), nested sampling (Skilling),
  multilevel splitting / adaptive multilevel splitting (Cérou–Guyader; Bréhier et al.),
  flat-histogram methods (Berg–Neuhaus, Wang–Landau), their optimality theory.
* Query complexity of approximate counting / mean estimation with adaptivity:
  Canetti–Even–Goldreich lower bounds for sampling; Dagum–Karp–Luby–Ross optimal stopping;
  statistical-query lower bounds; "rounds of adaptivity" hierarchies (property testing,
  batched bandits, parallel optimisation).
* Isoperimetry on the cube with product and non-product measures (Harper; Bollobás–Leader;
  Ahlswede–Zhang; Lei Yu's work on isoperimetric exponents / "strong Brascamp–Lieb").
* For item 7: capacity of binary asymmetric channels at fixed odds ratio; "log-odds ratio"
  parametrisations; Fréchet-class / copula results on mutual information of 2×2 tables with
  fixed odds ratio (the odds ratio is the copula parameter of a 2×2 table — check the
  statistics literature on "maximum entropy / mutual information for given odds ratio",
  Plackett distributions, and the information-theory literature on "strong data-processing"
  constants of binary channels).  Try to *prove or find* the lemma independently; if it is a
  two-line consequence of a named inequality, say which.

## What to deliver

For each claim: the exact statement as the theory report has it (section, theorem number),
the closest prior statements you found with the reading level (full text / abstract /
snippet), a comparison of hypotheses, quantifiers and conclusions, and a classification into
exactly one of: (1) established prior art; (2) reformulation of a known result; (3) known
special case exists; (4) plausibly original generalisation; (5) new combination; (6)
plausibly original theorem; (9) unresolved.  Then: which one or two results of this cluster
would survive a hostile referee in information-based complexity or theoretical statistics as
*the* contribution of a paper, and what the paper would have to add.  Be concrete about
venues only in terms of community (IBC / sampling theory / information theory), not journal
prestige.
