# Division 9 — prior art and novelty matrix

*Status: a bounded search by one AI subagent (about 46 web calls on 2026-11-28, nine failed), read and
edited by the coordinating AI session.  "Not found" below means **not found in this bounded search**;
it is not a claim of novelty.  Nothing here has been checked by a human expert.  Where the search could
read only an abstract or a search-result snippet this is said.  Sources not opened are listed in §4.*

## 1. Verdicts

| claim of this division (label in `MATHEMATICS.md`) | closest prior art | verdict |
|---|---|---|
| **A1** — variance as a minimum over an allocation-independent affine set; convexity in the allocation; gradient `−Var_k(z)` (handoff A1/A2) | Hahn & Then 2009: the two-state case, by a second-derivative computation, with the same envelope property and the same equal-variance optimality condition, cost-aware. Gill–Vardi–Wellner 1988: the information operator `Σ λ_i A_iᵀA_i` is linear in the sampling fractions. He & Owen 2014: joint convexity of the variance of mixture importance sampling with control variates (same perspective mechanism, known normalising constants; abstract only) | **known for `K = 2`; for general `K` it follows at once from known theory** (the dual formula, next row).  An explicit multistate statement was not found |
| **A2/A4** — dual formula `V = sup_h {2ℓ(h) − Σ s_k Var_k h}`; precision `1/V` concave and superadditive | the semiparametric bound is a supremum over one-dimensional submodels of (derivative)²/information, and information adds over independent samples; in design theory `(cᵀM⁻c)⁻¹ = min{hᵀMh : cᵀh = 1}` is concave (Pukelsheim; cited from memory, not re-opened) | **follows immediately from known theory**; not found stated for MBAR or the biased sampling model |
| **A5/A6** — Elfving-type identity for the optimal budgeted allocation; equivalence theorem; certified efficiency bound of any allocation; unsampled states | Bennett 1976 and Hahn & Then 2009 (`K = 2`: equal-variance condition, boundary cases, costs `β²/α² = c₀θ₁/(c₁θ₀)`); Gill–Vardi–Wellner 1988, **Problem 6.1 "Design questions"**: "if we have some control over the choice of the number of samples s, the sampling fractions λ_i or the biasing functions w_i, we may want to choose them to optimize some criteria such as the variance of an estimate", with two solved examples (Neyman allocation; enriched stratified sampling) and "Clearly there are a great variety of related optimization problems"; EMUS (Thiede et al. 2016; Dinner et al. 2020): Neyman-type allocation for an estimator whose influence functions do not depend on the allocation, "results pertain only to the EMUS method and not iterative EMUS or MBAR"; Xu 2019 (DiffNet): A/D/E-optimal allocation for *independent* pairwise measurements | **known in special cases; the general statement is the infinite-dimensional instance of Elfving / Kiefer–Wolfowitz c-optimality and follows from known theory with routine care; not found for the biased sampling model**, where the design question was posed in 1988 |
| **B1–B3** — the reverse-logistic likelihood ratio is an e-value under *stratified* sampling (`E = exp(−N·KL(s‖a))`); anytime-valid, allocation-adaptive confidence regions for free energies as sublevel sets of the MBAR objective | universal inference (Wasserman–Ramdas–Balakrishnan 2020; not re-opened): split or running-MLE likelihood ratios are e-values in any dominated model — this gives the **random-label** version immediately; Turner–Ly–Grünwald (k data streams with fixed group sizes, null "same source"; abstract); Turner–Grünwald (anytime-valid confidence sequences for odds ratios with fixed group sizes; snippet); Micaletto 2026 (finite-sample concentration for two-sample bridge sampling, no coverage guarantee, no e-values, no optional stopping) | the random-label version **follows immediately from universal inference**; the stratified identity and the application to free energies were **not found** (three targeted searches) |
| **C1–C2** — finite-sample two-point bound of order `√(V_c/N)` at every instance; no adaptive allocation beats the optimal static allocation by more than a universal constant factor (local) | Gill–Vardi–Wellner 1988 (asymptotic convolution theorem; the 1986 preprint: "A local asymptotic minimax lower bound can also be stated … but we forego this here"); Micaletto 2026 (lower bounds for the optimal bridge estimator in two-point families; "A minimax lower bound over all estimators that use both samples remains open"); Block & Shetty 2026 (proposal samples only); Armstrong 2022 (adaptive treatment assignment gives no first-order improvement over the optimised Neyman bound — a different model; snippet) | asymptotic local minimaxity at `V_c` is **known**; the finite-sample instance-wise statement and "adaptive ≈ static optimum up to a constant" for this model were **not found**; the techniques are standard.  A local bound does not settle Micaletto's uniform minimax question |

Consequences for how the results are presented: A1–A6 are presented as the *optimal-design theory of the
biased sampling model, written out* (the answer to Gill–Vardi–Wellner's Problem 6.1 for the variance of a
contrast), not as a new convexity phenomenon; the two-state case is credited to Bennett and to Hahn &
Then.  B1–B3 are presented as an application of e-values/universal inference with one new lemma (the
stratified identity).  C1–C2 are presented as explicit finite-sample forms of the classical local
asymptotic minimax bound.

## 2. What each source contains (as read)

1. **Hahn & Then, Phys. Rev. E 80, 031111 (2009), arXiv:0904.0625** (full text read).  Two states only.
   `M(α) = N·MSE = (1/(αβ))(1/U_α − 1) = θ₀/α + θ₁/β`, `θ_i = Var_i(p_α/p_i)`.  "Theorem. The
   asymptotic mean square error M(α) is convex in α."  Proof by a second derivative.  Envelope property
   `M′ = θ₁/β² − θ₀/α²`.  Interior optimum: equal variances of `(p₁−p₀)/(αp₀+βp₁)` under the two
   states; boundary criterion from the signs of `M′(0)`, `M′(1)`; with costs
   `β_o²/α_o² = c₀θ₁/(c₁θ₀)`, "a result Bennett was already aware of"; equal-cost allocation is within a
   factor 2.  A "dynamic strategy" (plug-in tracking of the optimum), no lower bound.
2. **Bennett 1976** (not opened; quoted through Meng & Wong 1996, full text read): "The best estimate of
   the free energy difference is usually obtained by dividing the available computer time approximately
   equally between the two ensembles; its efficiency (variance × computer time)⁻¹ is never less, and may
   be several orders of magnitude greater, than that obtained by sampling only one ensemble".
   Meng & Wong: equal allocation optimal for the geometric bridge; multi-density sections take sample
   sizes as given.
3. **Gill, Vardi & Wellner, Ann. Statist. 16 (1988)** (scan read in part).  Theorem 3.1: the NPMLE is
   asymptotically efficient; information operator linear in the fractions; Remark 3.1 and Problem 6.1 on
   design (quoted in §1).  Vardi 1985 not accessible.
4. **Kong et al. 2003; Tan 2004** (abstracts/snippets only).  Efficiency of the likelihood estimator for
   a fixed design; no allocation theorem surfaced.
5. **Shirts & Chodera 2008** (abstract).  Optimality of the estimator for given samples; nothing on allocation.
6. **Allocation literature.**  Xu 2019 (DiffNet; full text): independent measurements, classical A/D/E
   design on a graph Laplacian.  Yang et al. 2020 (snippet): which pairs to include.  OBAR (Sun–Wang–Zhang
   2017; abstract): adaptive allocation among windows ranked by the time derivative of the total BAR
   variance — heuristic.  EMUS (Dinner et al. 2020, first half): `variance = Σ_i (z_i²/κ_i)×(κ-free
   term)`, hence Neyman allocation.  Predescu et al. 2021 (Times Square sampling; full text searched):
   "The variance of the free energy estimate of interest typically depends strongly on how the total
   computational resources available for sampling are divided among the distributions", but "The
   specification of an optimal rung density γ is outside the intended scope of this paper"; credits AWH
   (Lindahl–Lidmar–Hess) with estimating an allocation that lowers the variance.  He & Owen 2014
   (abstract): joint convexity for mixture importance sampling with control variates.  Li–Tan–Chen 2013
   (snippet): a pilot stage to choose mixture proportions.  Roy & Evangelou (abstract): which proposals,
   not how many samples from each.  Density-ratio/case-control literature: no allocation result found.
7. **Micaletto 2026, arXiv:2610.17403** (abstract and most of the HTML).  Two-sample optimal bridge only:
   concentration `P(|Δ| ≥ t) ≤ 2exp{−N H κ(t)}` without moment conditions; Berry–Esseen
   `3.1/√n_eff`; lower bounds for the optimal bridge estimator in two-point families.  No finite-sample
   coverage guarantee, no e-values.  "multiple bridge sampling and MBAR" listed as an extension.
   **Block & Shetty 2026, arXiv:2602.23535** (abstract): partition-function estimation from proposal
   samples and density-ratio evaluations, with matching lower bounds.
8. **Li, Van Koten, Dinner, Thiede 2023 (PMC10845960)**: central limit theorem for MBAR with Markov-chain
   samples; the variance "takes the form of a sum of contributions from all states"; fractions fixed;
   "We leave a systematic procedure for using the error estimator to refine the sampling for future work."
9. **E-values.**  See §1 row B.  Nearest relatives named from memory and not verified: Markov-inequality
   bounds on unbiased exponential averages (Jarzynski; bidirectional Monte Carlo); classifier two-sample
   e-processes.
10. **Elfving / equivalence theorems in semiparametric multi-sample models**: nothing found; nearest:
    two-phase designs minimising a semiparametric efficiency bound (Wang et al., arXiv:2312.10596).

## 3. What a specialist should be asked

* Is the convexity of the efficiency bound of the biased sampling model in the sampling fractions, with
  its equivalence theorem, written anywhere between 1988 and now (design of case-control / multi-phase /
  choice-based samples is the most likely place)?
* Is the stratified e-value identity `E = exp(−N·KL(s‖a))` in the safe-testing literature on fixed group
  sizes (Turner–Ly–Grünwald and successors)?
* Does Tan's 2004 paper, or Kong et al. 2003 (not opened here), state an optimal-allocation result?

## 4. Sources the search could not open

Bennett 1976; Vardi 1985; full texts of Kong et al. 2003, Tan 2004, Li–Tan–Chen 2013, He & Owen 2014,
OBAR, Yang et al. 2020; Thiede et al. 2016; Doss & Tan 2014; Roy–Tan–Flegal 2018; the Sbert/Havran
multiple-importance-sampling papers; Wasserman et al. 2020 and Grünwald–de Heide–Koolen (cited from
memory); Elfving, Kiefer–Wolfowitz, Pukelsheim (cited from memory); the second half of Dinner et al. 2020.

## 5. Links

Hahn & Then <https://arxiv.org/abs/0904.0625> · Meng & Wong <https://www3.stat.sinica.edu.tw/statistica/oldpdf/A6n43.pdf> ·
Gill–Vardi–Wellner <https://sites.stat.washington.edu/jaw/JAW-papers/jaw-gill-vardi-88AS.pdf> ·
Gill & Wellner preprint <https://ir.cwi.nl/pub/6253/6253D.pdf> · Shirts & Chodera <https://arxiv.org/abs/0801.1426> ·
Xu <https://arxiv.org/abs/1906.08599> · Dinner et al. <https://arxiv.org/abs/1705.08445> ·
Predescu et al. <https://arxiv.org/abs/2112.05109> · He & Owen <https://arxiv.org/abs/1411.3954> ·
Roy & Evangelou <https://arxiv.org/abs/1805.00829> · Micaletto <https://arxiv.org/abs/2610.17403> ·
Block & Shetty <https://arxiv.org/abs/2602.23535> · Li et al. <https://pmc.ncbi.nlm.nih.gov/articles/PMC10845960/> ·
Turner–Ly–Grünwald <https://arxiv.org/abs/2106.02693> · Turner–Grünwald <https://arxiv.org/abs/2203.09785> ·
Armstrong <https://arxiv.org/abs/2205.02726> · Wang et al. <https://arxiv.org/abs/2312.10596>
