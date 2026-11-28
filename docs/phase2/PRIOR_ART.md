# Phase II — prior art: a bounded search

*Theoretical Research Division, Phase II, 2026-11-28.  Five web-search queries in generic terms (no
project names, no private details) and one abstract page.  **Reading level: search-engine summaries, and
one abstract; no paper was opened.**  "Not found" below means *not found by this search*, nothing more.
The earlier sweeps of the programme (theory `docs/prior_art/L1–L10`, the science division's
`PRIOR_ART_MATRIX.md`) are not repeated.*

## 1. What was asked

| # | query (as sent) | aim |
|---|---|---|
| 1 | query complexity normalizing constant estimation lower bound "statistical query" oracle function evaluations partition function | Theorem A: is an observation (statistical-query) oracle added to evaluations treated anywhere? |
| 2 | lower bound estimating normalizing constant given samples from target distribution and density evaluations query complexity | Theorem E: samples of the ensemble plus evaluations |
| 3 | free energy estimation "moment constraints" OR "expectation values" side information oracle complexity lower bound Lipschitz hypercube integration adaptive | Theorems A, B: averaged data as side information |
| 4 | "statistical query" lower bound "partition function" OR "normalizing constant" estimation hardness oracle tolerance | Theorem A, tolerance model |
| 5 | partition function estimation given exact marginals OR "marginal oracle" query lower bound "k-wise independent" hidden perturbation hypercube | Theorem B: exact marginals, code-averaged hidden instances |

## 2. What came back

| source (as returned by the search) | what the summary says | relation to Phase II |
|---|---|---|
| Ge, Lee, Lu, *Estimating normalizing constants for log-concave distributions: algorithms and lower bounds* (arXiv 1911.03043; STOC 2020) | value/gradient queries of a strongly convex smooth potential on `ℝ^d`; an information-theoretic lower bound ("one query reveals the type of at most one cell"), `d^{1−o(1)}/ε^{2−o(1)}` queries insufficient | the same kind of hiding argument, for a log-concave class in `ℝ^d` with polynomial complexity; no observation oracle |
| Kolmogorov, *A faster approximation algorithm for the Gibbs partition function* (arXiv 1608.04223; COLT 2018); Harris, Kolmogorov, *Parameter estimation for Gibbs distributions* (arXiv 2007.10824) | the algorithm draws samples of Gibbs distributions at chosen temperatures; lower bound `Ω(q ε^{−2})` oracle calls, `q` the log-ratio of two partition functions | a *sampling* oracle at chosen temperatures and no evaluations of an unknown function: a different access model from Theorem E (samples at one temperature plus exact evaluations) |
| Guo, Liu, Yang, Yin, Zhang, *Optimal simulated annealing for partition function estimation* (arXiv 2609.20337, 17 Sep 2026; abstract read) | a non-adaptive simulated-annealing reduction for Gibbs partition functions; lower bounds for general and for non-adaptive algorithms; optimal over a broad range of parameters.  The access model is not stated in the abstract (by the search summary: temperature-indexed sampling oracles; lower bounds from two instances whose oracle outputs are close at every temperature) | the nearest recent work on *adaptive against non-adaptive* partition-function estimation, in the sampling-oracle model; not about evaluation oracles on a Lipschitz class, nor about averaged data |
| Block, Shetty (arXiv 2602.23535, 2026) | sample access to a proposal and an unnormalised density ratio; "integrated coverage" characterises the sample complexity of multiplicative estimation, with matching lower bounds | already known to the programme (its cost table of certified reweighting is theirs); a proposal-sampling model |
| Cai, Scarlett, *Kernelized normalizing constant estimation* (arXiv 2401.05716) | black-box queries of a function in a reproducing-kernel Hilbert space; bounds like those of Bayesian quadrature; noisy and noiseless cases differ | another function class; "noise" there is on evaluations, not an observation oracle |
| arXiv 2404.02414 (2024) | `Ω(1/ε²)` classical query lower bound and `Ω(1/ε)` quantum, by reduction from estimating a Hamming weight | accuracy dependence in a different model |
| arXiv 2210.06539 (quantum algorithms for log-concave sampling and normalizing constants); arXiv 2502.04575 (annealed importance sampling, oracle complexity without log-concavity, upper bounds); arXiv 2105.14163 (query complexity of sampling in one dimension) | as titled | background only |
| statistical-query literature | the search returned no statistical-query lower bound for partition functions or normalising constants; one hit on robust estimation for Ising models in the statistical-query model | Theorem A's setting — a statistical-query oracle *in addition to* exact evaluations of the unnormalised density — was not found |

## 3. Assessment (AI, summary level)

* **Not found:** a statement that averaged data with tolerance `τ` on `M` observables change the query
  complexity of a normalising constant by at most a factor `τ^{−2} ln M` (Theorem A); the exact exponent
  with the law of a block of sites (Theorem C); the collapse with all observables against the
  deterministic `τ·2ⁿ` (Proposition C′); a lower bound for samples at one temperature plus exact
  evaluations (Theorem E).
* **Found, and to be cited by anyone who writes this up:** the cell-hiding lower bound of Ge–Lee–Lu; the
  sampling-oracle line (Kolmogorov; Harris–Kolmogorov; Guo et al. 2026, which has an adaptive /
  non-adaptive distinction of its own); Block–Shetty.  From memory, not searched: statistical queries
  (Kearns 1998), `k`-wise independence and small-bias sets (Rao 1947; Alon–Babai–Itai 1986; Naor–Naor
  1993; Alon–Goldreich–Håstad–Peralta 1992), counting and sampling (Jerrum–Valiant–Vazirani 1986),
  support-size estimation (Raskhodnikova et al. 2009; Valiant–Valiant 2011), annealing for counting
  (Štefankovič–Vempala–Vigoda 2009; Huber 2015).
* **What this is worth.**  Five queries and one abstract.  Every ingredient of the Phase II proofs is
  classical (translation averaging, Hoeffding, random linear codes, the birthday bound); a specialist
  in information-based complexity or in statistical-query lower bounds may regard the statements as
  exercises.  Within the programme, part of Theorem B is the science division's (report §9).

## 4. Sources

* <https://arxiv.org/pdf/1911.03043>
* <https://arxiv.org/pdf/1608.04223>
* <https://arxiv.org/html/2007.10824v11>
* <https://arxiv.org/abs/2609.20337>
* <https://arxiv.org/abs/2602.23535>
* <https://arxiv.org/pdf/2401.05716v1.pdf>
* <https://arxiv.org/abs/2404.02414v1>
* <https://arxiv.org/pdf/2210.06539>
* <https://arxiv.org/pdf/2502.04575v2>
* <https://arxiv.org/pdf/2105.14163>
