# L7 — Query complexity: prior art for theory report §11.10

Scope: the method and the nearest published statements for the bounds on *algorithms* (as
opposed to certificates) of theory report §11.10.  Four web searches were run on 2026-11-24;
results are search-engine summaries unless marked otherwise.  Nothing here was read in the
primary source during this cycle; statements quoted from memory are marked.

| # | claim of §11.10 | status | source |
|---|---|---|---|
| Q1 | A deterministic algorithm that is `ε/2`-correct must distinguish every pair of class members whose values differ by more than `ε` (Theorem 11.22(a)) | KNOWN: the radius-of-information argument for adaptive information | Traub–Wasilkowski–Woźniakowski, *Information-Based Complexity* (1988) [from memory] |
| Q2 | Randomised algorithms: every sensitive alternative is detected with probability `1 − 2δ`; expected queries are at least `(1 − 2δ)` times a fractional packing of sensitive blocks (Theorem 11.22(b,c)) | KNOWN METHOD: fractional block sensitivity = fractional certificate complexity is a lower bound on randomised query complexity of Boolean functions | Aaronson, "Quantum certificate complexity" (2003; randomised certificate complexity `RC`); Tal (2013) and Gilmer–Saks–Srinivasan (2016) (fractional block sensitivity, equal to fractional certificate complexity by LP duality); Kulkarni–Tal, "On fractional block sensitivity", Chicago J. Theor. Comput. Sci. 2016:8 — search summary: "It is a randomized lower bound on query complexity"; `fbs = Θ(RC)` |
| Q3 | Instance-wise deterministic complexity of certified minimisation equals the smallest certificate (Theorem 11.23(a)) | KNOWN in `ℝ^d` for `f ≡ 0`: the "best possible algorithm" `n_B` (Hansen–Jaumard–Lu 1991) and the lower bound for certified algorithms (Bachoc–Cesari–Gerchinovitz 2021, "relies on a local worst-case analysis"); the exact iff with a known part on a finite quasi-metric space is a restatement | see `L4`, K1 and K3 |
| Q4 | Randomised algorithms pay the covering price instance by instance (Theorem 11.23(b)) | NO MATCH FOUND for an instance-dependent statement.  Worst-case statements ("randomisation does not help for global optimisation over Lipschitz classes") are classical | Nemirovski–Yudin (1983), Novak (1988) [from memory; the search did not retrieve a primary statement — NOT RE-VERIFIED] |
| Q5 | Soft-gap radius, randomised exponent and accuracy threshold for `ln Z` (Theorems 11.24–11.25) | NO MATCH FOUND.  Nearest: query lower bounds for normalising constants of log-concave densities by hiding a perturbation in one of many cells ("making one query to `f` can reveal the type of at most one cell") | Ge–Lee–Lu, "Estimating normalizing constants for log-concave distributions: algorithms and lower bounds", STOC 2020, arXiv:1911.03043 (search summary) |
| Q6 | Extremal sets on the cube are Hamming balls (Theorem 11.25(c)) | KNOWN: vertex-isoperimetric theorem | Harper, "Optimal numberings and isoperimetric problems on graphs", J. Combin. Theory 1 (1966) [from memory] |
| Q7 | Sample size of importance sampling `≈ e^{KL}` (remark after Theorem 11.25) | KNOWN | Chatterjee–Diaconis, "The sample size required in importance sampling", Ann. Appl. Probab. 28 (2018) [from memory] |

## Search log

1. `fractional block sensitivity fractional certificate complexity randomized query complexity
   lower bound Tal Aaronson randomized certificate complexity` — confirmed Q2 (summaries of
   Kulkarni–Tal and of later papers citing Tal and Gilmer–Saks–Srinivasan).
2. `randomized algorithms global optimization Lipschitz functions lower bound randomization does
   not help Novak "Deterministic and Stochastic Error Bounds"` — did not retrieve Novak's
   statement; returned Malherbe–Vayatis (LIPO) and convex-optimisation lower bounds.  Q4's
   classical half therefore rests on memory.
3. `Bachoc Cesari Gerchinovitz instance-dependent bounds zeroth-order Lipschitz optimization
   error certificates lower bound certified algorithms randomized` — abstract-level summary;
   nothing on randomised algorithms.
4. `query complexity lower bound estimating normalizing constant partition function black-box
   oracle Ge Lee Lu "normalizing constants" lower bound` — Q5.

## What should be checked by a specialist

* Whether an instance-dependent lower bound for *randomised* certified Lipschitz optimisation is
  in the bandit / zeroth-order literature after 2021.
* Whether the threshold phenomenon of Theorem 11.25 (cost of estimating `ln E e^{−βg}` over a
  Lipschitz class on the cube as a function of the accuracy) is known in the literature on
  Monte-Carlo integration of unbounded or exponential functionals (information-based
  complexity; "integration of exponential functionals").
* Asymptotic isoperimetric inequalities on product spaces at the large-deviation scale
  (Ahlswede–Gács–Körner blowing-up; Ahlswede–Zhang; Alon–Boppana–Spencer) as the tool for the
  conjecture of theory report §12, item 2(b).
