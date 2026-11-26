# Unresolved proof obligations and open problems — Ensemble division

## Obligations (things our statements still owe)

| # | obligation | affects | priority |
|---|---|---|---|
| OB1 | Internal adversarial review of every paper proof of the report (commissioned at checkpoint 1); apply its findings as linked corrections | all [P] | high |
| OB2 | Read Odlyzko (1988) in the original: exact leading term `4C(p,3)(¾)ⁿ`, range `p ≤ n − 10n/ln n`, error term | E10(c) | high |
| OB3 | Read Deza–Laurent (book, the section on neighbourliness) or Deza–Laurent–Poljak (1992): exact statement and hypotheses of 3-neighbourliness | E9(a) | medium |
| OB4 | Read Garamvölgyi–Gortler–Jordán (2022) Sections 4–5 and check that nothing there contains E5(a)/E7; read Gortler–Healy–Thurston for the exact genericity statement used in E7 | E7 | high |
| OB5 | Read Vitushkin–Henkin (or Khavinson's book) for the exact hypotheses (domain, smoothness, weights) | E8.1 | medium |
| OB6 | Bai–Yin: exact hypotheses (i.i.d. entries with finite fourth moment; almost-sure convergence) | E11 | low |
| OB7 | Machine-check candidates: E1(a) "only if" (needs a theorem of the alternative), E2(a) weak duality in the dual form, the Littlewood–Offord lemma of E10, E12(a) | — | medium |
| OB8 | The sources marked "memory" in `PRIOR_ART.md` | novelty classes | medium |
| OB9 | Run the programme's full audit (`scripts/audit_all.sh`) on this branch | verified state | high |

## Open problems

Listed with their statements in `ENSEMBLE_REPORT.md` §9: O1 (capacity of pair data), O2
(`k`-body data), O3 (conformers with common rigid parts), O4 (quantitative ensemble
rigidity), O5 (fewer moments), O6 (soft ensembles and adaptivity), O7 (finite temperature),
O8 (noise), and Conjecture C1 (the obstruction for densities).
