# R3 — Independent referee report on the third research cycle (query complexity, §11.10)

Subject: (A) `docs/THEORY_REPORT.md` §11.10 (Theorems 11.22–11.25, the table of three budgets, "What is not
proved", "Prior art"), row G11 of §10, §12 as rewritten, `proofs/Frontiers/QueryLowerBound.lean` and its four
witnesses in `proofs/AxiomAudit.lean`; (B) the corrections demanded by the second referee (`reviews/R2`: C1, M1–M4,
m1–m17) against §§2.4, 8, 10–12, README "Status", `BLUEPRINT.md` §6.3, §6.6, §9, `DEAD_ENDS.md` D21, D22, D28–D34,
`RefereeLemmas.lean`; (C) harness tests `XII.1`–`XII.5`, `DEAD.10`–`DEAD.14`, mutation group `XII`, benchmark B10.
I had no part in the work.

**Repository state.**  The tree kept moving while I worked.

| time (UTC, 2026-11-24) | `git log --oneline \| head -1` | `git status --short \| wc -l` |
|---|---|---|
| 18:41 (start) | `e8ceeab Second referee report: correction of the finite-temperature exponent theorem` | 17 |
| 18:55 | `f1a6015 Cycle 8: referee corrections; query complexity of every algorithm` (the same 17 files, committed unchanged) | 0 |
| 19:27 | `6344bf9 Soft-gap bounds: randomised free-energy estimation bracketed from both sides` (new `SoftGapBounds.lean`, Theorem 11.26, harness `XII.6`) | 0 |
| 19:49 | `6344bf9` + uncommitted edits (Theorem 11.23(c), `min_spotCheck_correct`, "Without a hint") | 3 |
| 20:23 | `6344bf9` + further uncommitted edits ("No sharp regime at finite temperature", B10 check) | 4 |
| 20:33 (end) | `6344bf9` + uncommitted edits; untracked `proofs/Frontiers/QueryRefinements.lean`, `docs/workstreams/`, `docs/reviews/R3_referee_report.md` | 7 |

`QueryRefinements.lean` (20:30) collects the lemmas of Appendix A, and `docs/reviews/R3_referee_report.md` (20:31)
is a copy of an intermediate draft of this report; both were taken from my scratch directory by the authors
before the report was delivered.  I wrote nothing into the repository and have not reviewed either file; the
text below is the final one.

**Everything below refers to `f1a6015`** (identical to the tree I was given); line numbers are those of that
commit.  Theorem 11.26, `SoftGapBounds.lean`, `XII.6`, Theorem 11.23(c) and the later paragraphs appeared during
the review and are **not refereed**; §7 says how they bear on the findings.  Every sentence flagged under CRITICAL
and MAJOR was still present in the working tree at the end (M4: in a reworded form, see there).

**Method.**  (i) `QueryLowerBound.lean` read in full (statements and proofs) against the prose.  (ii) Five scratch
Lean files outside the repository, checked with `lake env lean` (no `lake build`): 44 cited declarations exist with
the stated types, 21 headline statements depend only on `propext`, `Classical.choice`, `Quot.sound`; seven lemmas
of my own are machine-checked (Appendix A).  (iii) Independent numerics, own code (§5): an **exact** linear
program for the instance-wise randomised query complexity, exhaustive search over all 16 430 adaptive decision
trees of a tiny class, exact ball counts on the cube up to `n = 6400`, Blahut–Arimoto (primal) computation of the
three exponents.  (iv) Literature: one primary PDF read (Holzmüller–Bach, JMLR 2025, pp. 1–13), abstracts and
summaries for the rest (§4a says exactly what).

## 0. Summary

* **No machine-checked statement is false.**  The Lean statements match the prose of Theorems 11.22–11.24 and
  11.25(a).  `QueryAlgorithm` is strictly more general than decision trees (machine-checked example, m1), which
  only strengthens the lower bounds; the upper-bound constructions are genuine two-round algorithms.
* **One paper statement is false as stated — the same error as R2-C1, re-committed in the new section.**
  Theorem 11.25(c) ("for `ε = o(n)` the bound (a) is attained at `g ≡ 0` up to a factor polynomial in `n`") and the
  sentence "exponent `ln 2 − h(ρ(ε₁))` … for `ε₁ = 0`" fail for accuracies that are exponentially small, in
  particular for `ε = 0`: there every randomised algorithm makes at least `(1 − 2δ) 2ⁿ` evaluations
  (machine-checked from the repository's own `expected_queries_ge_of_radius`, Appendix A.2), whereas (a) is
  `exp(n(ln 2 − h(ρ₀)))`.
* **The argument for 11.25(c) also fails for `ln n ≪ ε`**: the spot-check of Theorem 11.22(d) has to detect
  alternatives at level `ε/2`, the lower bound counts alternatives at level `ε`, and on the cube the two differ by
  `e^{Θ(ε)}` (measured: `e^{13}` at `ε = √n`, `e^{30}` at `ε = 0.06 n`, `n = 3200`).  For these accuracies the statement
  itself is true and can be repaired — and extended to extensive accuracies, where the report claims an exponent
  it does not prove —
  by a *hedged* spot-check (return `ln Z(0) + ε/2 − 1` instead of `ln Z(0)`; machine-checked lemma, A.3): then upper
  and lower bound agree within a constant factor for every `ε ≥ 2`.
* **Four further major points**: the cube threshold is quoted in four places as a statement about "the sandwich"
  in general; the README says the smallest certificate is "exactly the number of evaluations of the best algorithm
  that is correct on the whole class" (it is an instance-wise, hint-dependent statement; the report's own hub
  family refutes the literal reading); "on the cube class … exponentially small for every `q`" (blueprint Step 5)
  is false for models other than the zero residual (`ĝ = c|x|` is determined by two evaluations); and the prior-art
  paragraph misses the closest literature — Holzmüller–Bach §2.2 (optimisation regime versus quadrature regime for
  *stochastic* log-partition estimation; a paper the report cites elsewhere), Grossman–Komargodski–Naor 2020
  (instance complexity with a hint, deterministic and randomised), and the fact that Bachoc–Cesari–Gerchinovitz
  list randomised certified algorithms as an open direction.
* **R2 corrections**: all 22 items are applied (table in §3); two leave a residue (R2-M3 in §7 item 2 of the theory
  report; the error of R2-C1 recurs in Theorem 11.25(c)).
* **Verdict**: §11.10 turns the certificate bounds into instance-complexity bounds by a known three-line method;
  it does not change "a coherent note".  Theorem 11.25, once corrected, is the one statement with matching sides
  and an exact constant; §4 says what would make it a contribution.

## 1. Verdict per statement

| statement | correct? | depth | novelty | remark |
|---|---|---|---|---|
| Model (`QueryAlgorithm`, finite mixtures) | adequate for lower bounds | — | — | a `QueryAlgorithm` is a subcube partition with outputs (unambiguous certificates), strictly more than decision trees (A.1); finite mixtures only (m2) |
| 11.22(a) deterministic detection | correct | trivial | known (radius of information; certificate complexity) | Lean = prose |
| 11.22(b) randomised detection, `1 − 2δ` | correct | trivial (two-point union bound) | known method (Aaronson's `RC`; fractional block sensitivity) | holds verbatim for any *pair* of alternatives (A.4), which is strictly stronger |
| 11.22(c) packing bounds | correct | routine (weak LP duality) | known method | exhaustive search over all adaptive trees of a tiny class: bound respected and attained |
| 11.22(d) spot-check | correct | trivial | known (verification of a hint; "instance complexity", Grossman–Komargodski–Naor 2020) | `N` bounds the cost on the hint only (as the prose says): as soon as one sample disagrees the algorithm evaluates all of `X`; not the best converse: it must detect at level `ε/2` (M1) |
| "is the fractional hitting number … up to `ε` vs `ε/2`"; "the deterministic one is the integral hitting number" | loose | — | — | the `ε`/`ε/2` slack is exponential on the cube; deterministic complexity is `N_value`, not a hitting number at level `ε` (m6) |
| 11.23(a) certificate size = instance-wise deterministic complexity | correct | trivial | known in substance (Hansen–Jaumard–Lu `n_B`; Bachoc et al. `τ`; instance complexity = certificate complexity) | `IsValueCertificate` is the notion of the prose (width of `[min(f+L_A), min(f+U_A)]` at most `ε`); the quantifiers (correct on every admissible residual, counted on one instance, algorithm built from that instance) are stated in the theorem, G11 and §12, not in the README (M3) |
| 11.23(b) randomised covering price | correct | routine | apparently new in this form (finite quasi-metric, exact evaluations); answers a direction Bachoc et al. leave open | exact LP on 260 instances: never violated, attained in 4 |
| [P] "`1 − 2δ` attained under that hypothesis"; "`kδ/(k−1)`" | correct | trivial | — | on the uniform metric with `ε = d/2` the factor is attained even for the whole class (explicit mixture, §5) |
| Consequences (i) integrality gap | correct | trivial | — | — |
| Consequences (ii) learn-then-cover; "`R*` is the exponent of the query complexity on additive instances" | correct under the hypotheses of Thm 11.9 (additive known part, finitely many site types, `κ < 1`) | trivial | — | optimal only where the residual has no non-decomposable part; evaluations counted, not computation |
| Consequences (iii) hub family defeats randomised algorithms | correct | routine | — | the justification given is heuristic; rigorous argument in Appendix B: `max_j E\|Q(g_j)\| ≥ ((1−2δ)²/8) min(M,N)` |
| 11.24(a,b) soft-gap radius | correct | routine | new formulation | `softGap` sums over the first argument of `slack d g x y = d x y − g x + g y`, so `f x + g x + s(x,y) = (f + U_y)(x)`: it is the prose formula; signs and `β ≥ 0` / `β > 0` are right; a relaxation that is far from the exact dip criterion for `ε ≪ 1` (m5) |
| 11.24(c) queries form a free-energy certificate | correct | trivial | — | — |
| limit `β → ∞`, "equivalent family of covering constraints" | correct | routine | — | integral and fractional covering numbers coincide (triangle inequality of the slack) |
| table of three budgets; single-letter form of `R^rand_β` | correct as a lower bound | routine (tensorisation + Csiszár's dual) | new formulation | primal (Blahut–Arimoto) = dual to 4 digits; all quoted numbers reproduced; "exponent" is a lower bound only (m7) |
| 11.25(a) | correct **[V]** | routine (Chernoff ball count) | — | optimisation over `t, R` and "positive iff `ε₁ < ln cosh(u/2)`" verified |
| 11.25(b) | correct **[P]** | routine (Azuma–Hoeffding with the exact two-point constant) | known technique | `N ≥ 2u² ln(2/δ) / (n (ε₁ − ln cosh(u/2))²)` |
| 11.25(c) | **wrong as stated** (C1); argument incomplete for `ε ≫ ln n` (M1); correct for `n^{−O(1)} ≤ ε ≤ O(ln n)` | routine + Harper **[K]** | — | Harper step verified on all 65 534 supports of the 4-cube |
| "sharp threshold `n ln cosh(βc/2)`" | correct as a worst-case statement (lower bound at the zero residual only) | the one two-sided statement of the section; short | exact threshold apparently new; the regime dichotomy for stochastic log-partition estimation is known (Holzmüller–Bach §2.2) | on the same class `g = c\|x\|` costs two evaluations at every accuracy |
| hint-free sentence (`u²/32` vs `u²/8`) | lower end correct; upper end heuristic | — | **[K]** | m9 |
| "What is not proved": `ε₁^crit`, `0.1137` vs `0.1225`, D34 | formula and numbers correct | — | — | consequences of the conjecture overstated (m10) |
| "Prior art" paragraph, `prior_art/L7` | incomplete | — | — | M5 |

## 2. Errors and overstatements

### CRITICAL

**C1. Theorem 11.25(c) is false for exponentially small accuracies, in particular for `ε = 0`.**
Location: `THEORY_REPORT.md` 1972–1977 ("For `ε = o(n)` the bound (a) is attained at `g ≡ 0` up to a factor
polynomial in `n`"), 1979–1982 ("with exponent `ln 2 − h(ρ(ε₁))` at the zero residual (for `ε₁ = 0`: `0.0077, 0.029,
0.097, 0.156` …)"); repeated as "the true exponent `ln 2 − h(ρ₀)` of Theorem 11.25(c)" in the current text.

*Counter-statement (machine-checked, Appendix A.2).*  On the cube class with `c > 0`, `β ≥ 0`: if
`ε < ln(2ⁿ − 1 + e^{βc}) − ln 2ⁿ` (the effect of a dip of depth `c` supported on one point), every randomised
algorithm that is `(ε/2, δ)`-correct on the class has `E|Q(0)| ≥ (1 − 2δ) 2ⁿ` (`cube_small_accuracy_randomized`;
`cube_exact_randomized` for `ε = 0`, `β > 0`).  Proof: the dip differs from `0` at one point only and changes `ln Z`
by more than `ε`; apply `expected_queries_ge_of_radius` with unit weights.  The bound (a) at `ε = 0` is
`(1 − 2δ) exp(n(ln 2 − h(ρ₀)))`, `ρ₀ = ln(2/(1+e^{−u}))/u`, i.e. `e^{0.029 n}` for `u = 1`: off by `e^{n h(ρ₀)}`, not by a
polynomial.  Exact LP on the 3-cube (`u = 1`): `R_δ = 7.2` (`δ = 0.1`) at `ε = 0`, against `(1−2δ)·8 = 6.4` (exact
dips) and `0.87` (formula (a)).  The text's own count `2ⁿ/|B(r*)|` gives `2ⁿ` at `ε = 0` (`r* = 0`); the error is the
identification of that count with (a).

*What is true* (exact dip effects, log-domain, `n ≤ 6400`, `u = 1`; lower bound from Theorem 11.22(b,c), upper bound
spot-check + Harper).  With `Λ₁ = ln(2/(1+e^{−u}))`, `η* = 1/(1+e^{u})`, `λ_c = Λ₁ − uη* = ln 2 − h(η*)`, the exponent of
the instance-wise randomised complexity at the zero residual is

| accuracy | exponent | check (`n = 6400`, `u = 1`) |
|---|---|---|
| `ε = nε₁`, `0 ≤ ε₁ < ln cosh(u/2)` (for `ε₁ = 0`: `ε = o(n)` **and** `ln(1/ε) = o(n)`) | `ln 2 − h((Λ₁ + ε₁)/u)` | `0.0298` vs `0.0291` at `ε = 0.5` |
| `ε = e^{−λn}`, `0 < λ ≤ λ_c` | `ln 2 − h((Λ₁ − λ)/u)` | `λ = 0.02, 0.05, 0.1`: `0.0404, 0.0597, 0.1010` vs `0.0398, 0.0590, 0.1003` |
| `ε = e^{−λn}`, `λ_c ≤ λ ≤ ln 2` | `λ` | `λ = 0.3, 0.6, 0.69`: `0.3000, 0.5999, 0.6893` |
| `λ ≥ ln 2`, `ε = 0` | `ln 2` | **[V]** A.2 |

(Upper ends: uniform sampling and Harper's theorem; for `ε ≫ ln n` with the hedged output of M1.  The first row for
`ε₁ > 0` and the last three rows are not in the report.)

*Fix.*  State (c) for `ε_n = o(n)` and `ln(1/ε_n) = o(n)` (as in the corrected Theorem 11.15), say that the
soft-gap bound (a) is a relaxation that is not attained for exponentially small `ε`, and add the table above (the
lower bounds follow from `expected_queries_ge_of_radius` with the exact effect `ln E e^{u(k+1−H)₊}` of the dip on
`B(k)`; the soft-gap theorem cannot see this regime).  Add a `DEAD` entry and a harness test at `ε → 0`: `DEAD.10`
guards Theorem 11.15, nothing guards 11.25(c), and B10 uses `ε = 0.5` only.

### MAJOR

**M1. The argument for 11.25(c) loses `e^{Θ(ε)}`; the general "converse" of Theorem 11.22 is not tight.**
Locations: 1972–1977; 1847–1850 ("is the fractional hitting number … up to … the change from `ε` to `ε/2`");
1979–1982 (exponent claimed at `ε₁ > 0`).
The lower bound (a) concerns alternatives with `|Δ ln Z| > ε` (ball radius `≈ (nΛ₁ + ε)/u`), the spot-check of
11.22(d) must detect alternatives with `|Δ ln Z| > ε/2` (radius `≈ (nΛ₁ + ε/2)/u`).  The ball volumes differ by
`exp(ε ln((1−ρ)/ρ)/(2u))`.  Exact ball counts, `u = 1` (`ln UB − ln LB`, without `ln(1/δ)` and `1−2δ`):

| `n` | `ε = 2` | `ε = ln n` | `ε = √n` | `ε = 0.02n` | `ε = 0.06n` | `ε = 0.10n` |
|---|---|---|---|---|---|---|
| 200 | 1.0 | 1.8 | 2.6 | 1.5 | 2.6 | 2.9 |
| 800 | 1.0 | 1.9 | 5.9 | 4.0 | 8.1 | 8.6 |
| 3200 | 1.0 | 2.4 | 13.1 | 14.2 | 29.9 | 30.4 |
| 3200, hedged spot-check | 1.0 | 1.0 | 0.8 | 0.8 | 0.5 | 0.2 |

So "(a) is attained up to a factor polynomial in `n`" is justified by the text only for `ε = O(ln n)`, and the
closing sentence asserts an exponent at extensive accuracy (`ε₁ > 0`), where the text proves `ln 2 − h(ρ(ε₁))` from
below only and its own construction would give `ln 2 − h(ρ(ε₁/2))` from above (`0.0104` against `0.0197` at
`ε₁ = 0.048`, `n = 3200`).
*Fix (machine-checked general lemma `hedgedSpotCheck_correct`, A.3).*  Let the spot-check return a number `o`
instead of `Φ(g₀)`; it is `(ε/2, δ)`-correct as soon as every alternative with `|Φ(g) − o| > ε/2` is detected with
probability `p` per sample.  On the cube take `o = ln Z(0) + ε/2 − 1`: increases by more than `ε − 1` need support
`> |B(k*(ε−1) − 1)|` (Harper), decreases by more than `1` need support `≥ (1 − e^{−1}) 2ⁿ`.  Then

    (1 − 2δ) 2ⁿ/|B(k*(ε))|  ≤  min E|Q(0)|  ≤  ⌈ ln(1/δ) / min(|B(k*(ε−1) − 1)|/2ⁿ, 1 − 1/e) ⌉        (ε ≥ 2),

the two sides within a constant factor (last row of the table), also for `ε = nε₁`.  The same device removes
"`ε` vs `ε/2`" from the zero-temperature statement: with `o = E* − ε/2 + η` only closed balls of radius
`gap + ε − η` and the minimiser have to be hit.  In general the right lower bound is the *pair* version of
11.22(b) (A.4): for any two class members with `|Φ(g₁) − Φ(g₂)| > ε` the run on `g` must hit
`D(g₁) ∪ D(g₂)` with probability `1 − 2δ`; this is the fractional relaxation of "value certificate" and explains
the exact LP value on the 3-cube at `ε = 0.2` (`6.4 = (1−2δ)·8`, where the report's bound gives `3.2`).

**M2. "Below the accuracy of the sandwich every randomised algorithm is exponential" is not what Theorem 11.25
says.**  Locations: `THEORY_REPORT.md` 1636–1640 (§11.6), 1807–1809 (§11.9); `DEAD_ENDS.md` 556–559 (D28);
`BLUEPRINT.md` 496–497 (§6.6).  Three gaps.  (i) Theorem 11.25 is about the uniform cube with zero known part, and
its lower bound is at the zero residual.  (ii) The sandwich these sentences refer to (Theorem 11.21) has width
`β²Σc_i²/8`; the threshold is `n ln cosh(βc/2)`, strictly smaller (`0.120` against `0.125` per site at `u = 1`,
`0.754` against `0.961` at `u = ln 16`), and between the two 11.25(b) gives a *bounded* number of evaluations — the
sentence is false there.  (iii) For a product reference that is not uniform the proved exponential regime is
`ε₁ < ε₁^crit(g)`, which is below the exact passive width (`0.11367` at the zero residual, `0.11383` at the worst
additive instance `γ₁ = −0.037`, against `0.12246`, for `e/c = 1/2`, `β = 1`; at `β = 4`: `0.938`, `1.017`, `1.523`),
and the report itself calls the interval in between open (1998–2000).
*Fix.*  "On the uniform cube class, below `n ln cosh(βc/2)` every algorithm needs exponentially many evaluations on
the zero residual; for other product references this is proved below `ε₁^crit` only."

**M3. README: the equality "certificate size = number of evaluations of the best algorithm" lacks its
quantifiers.**  Location: `README.md` 92–93 ("the size of the smallest one is exactly the number of evaluations of
the best algorithm that is correct on the whole class"); 100–101 ("randomisation gains at most a factor `1 − 2δ`
against each covering bound").  The theorem (`instance_query_complexity`) is: for each instance `g` *separately*
there is an algorithm, built from `g` (`certificateAlgorithm d f g A hA` takes the residual as a parameter), that is
correct everywhere and cheap on `g`.  No single algorithm does this — the report's own hub family (§11.5:
`min(M,N)+1` against `N_cov = 2`; for randomised algorithms, Appendix B).  The second sentence is proved for the
*fractional* covering bounds (`N_frac`), not for `N_cov`.  (Blueprint §9 and row G11 say "instance-wise" and are
fine.)  *Fix.*  "…equals, instance by instance, the cost of the best algorithm that is correct on the whole class
*and may be tailored to that instance*; no algorithm achieves it on all instances"; "…against each LP-dual covering
bound".

**M4. Statements about "the cube class" that hold only at the zero residual.**  Locations: `BLUEPRINT.md` 580–582
("on the cube class with accuracy below `n ln cosh(βc/2)` it [the detection probability `p`] is exponentially small
for every `q`"; in the current tree: "no sampling distribution avoids an exponential number"); `BLUEPRINT.md` 709;
`README.md` 101–103; `THEORY_REPORT.md` 1979–1983.  *Counterexample.*  Model `ĝ(x) = c|x|`: the evaluations at
`0…0` and `1…1` give `L = U = ĝ` (both McShane envelopes equal `c|y|`), so every admissible alternative differs
from `ĝ` at one of these two points; with `q = ½(δ_{0…0} + δ_{1…1})`, `p = 1/2` for every `ε ≥ 0`, every `β` and every
`n` (3-cube: `N_det = 2` at `ε = 0.05, 0.2, 0.5`).  The dip bound itself vanishes at such instances
(`ε₁^crit → 0` as `γ₁ → ±c`).  The theorem is a worst-case statement; the blueprint sentence, which is about an
arbitrary published model `ĝ`, is false.  *Fix.*  Add "for the zero model" / "in the worst case over instances"
at each location.

**M5. Prior art: the closest literature is missing, and `prior_art/L7` cannot support "no match found".**
Locations: `THEORY_REPORT.md` 2004–2012, row G11 (1184), `prior_art/L7`.
* Holzmüller–Bach, *Convergence rates for non-log-concave sampling and log-partition estimation* (JMLR 26 (2025);
  arXiv:2303.03237) — cited by the report in §3.4 for another purpose.  §2.2: for algorithms with *stochastic*
  evaluation points the log-partition problem has an "optimization regime" (`Bn^{−m/d} ≫ 1`), where the
  deterministic rate cannot be improved (Proposition 9, by reduction to optimisation), and a "quadrature regime",
  where Monte Carlo gains `n^{−1/2}` (Theorem 8, approximation + importance sampling; Table 1); the lower bounds for
  deterministic points "place bumps with small support in regions that the algorithm does not query", the one
  for stochastic sampling uses "the classical approach of hiding a bump"; a lower bound for stochastic
  log-partition estimation outside the optimisation regime is stated as open.  That randomisation helps for `ln Z` only above an accuracy scale is
  therefore in print for smoothness classes on `[0,1]^d` (worst case, `n → ∞` at fixed `d`).  Theorem 11.25 is the
  corner of that picture in which no approximation is affordable (dimension `→ ∞`), with an exact threshold; the
  exact statement I did not find there.
* Grossman–Komargodski–Naor, *Instance complexity and unlabeled certificates in the decision tree model*
  (ITCS 2020): instance optimality measured against an algorithm that receives a certificate, is correct on every
  input and is charged only when the certificate is right; deterministic and randomised trees.  This is the
  notion of §11.10 ("given `g` as a hint"); in the labelled case it is certificate complexity.  Theorem 11.23(a)
  is its real-valued restatement.
* Bachoc–Cesari–Gerchinovitz (2021) treat deterministic certified algorithms only and list randomised
  certification with a prescribed probability as an open direction.  This is the natural positioning of Theorem
  11.23(b) and is not mentioned.
* `L7` records four web searches, no primary source, and the classical halves "from memory".  (Novak's statement
  that randomisation does not improve the rate of global optimisation is quoted as Theorem 7 "adapted from Novak
  (1988)" in Holzmüller–Bach; the `[K, cited from memory]` can cite that.)
*Fix.*  Rewrite the paragraph; change "the threshold: no match found" in row G11 to "exact threshold on the cube
not found; the two regimes are known for smoothness classes (Holzmüller–Bach 2025, §2.2)".

### MINOR

* **m1. `QueryAlgorithm` is not "an abstract deterministic adaptive algorithm" but something larger.**  The
  consistency axiom says exactly that the partial assignments `g|Q(g)` partition the function space into subcubes.
  `pathoAlg : QueryAlgorithm (Fin 3)` (A.1, the partition `01*, *01, 1*0, 000, 111` on sign bits) queries at least
  one point on every input but no point on all inputs, so it is no decision tree.  Harmless: lower bounds hold for
  the larger class, `certificateAlgorithm` and `spotCheck` are real algorithms, and the output cannot depend on
  unqueried values.  Say so in the docstring (1818–1821 is accurate: "the only property of decision trees that is
  used").
* **m2. Finite mixtures.**  The formal statements cover finite probability spaces; a randomised tree with fresh
  randomness at every node of a real-valued history is a continuum mixture.  The proof (pointwise in `ω`, then
  linearity) extends verbatim; the restriction is disclosed (2000–2001) but "every randomised algorithm"
  (README, G11) is formally "every finite mixture".
* **m3. Witnesses are degenerate.**  `binary_randomized_witness` and `cube_thermal_randomized_witness` use a
  one-point probability space, the full-evaluation algorithm, `δ = 0`, `ε = 0`; `spotCheck_witness` has `p = 1`,
  `N = 1`, `δ = 0`.  They show satisfiability, not that the randomised theorems say anything about a randomised
  algorithm.  A genuinely randomised witness on which `expected_queries_ge_packing` holds with *equality* is in
  A.5 (`packing_factor_attained`: full evaluation with probability `1 − 2δ`, two blind guesses).
* **m4. Redundant hypotheses.**  `hε0 : 0 ≤ ε` in `expected_queries_ge`, `…_exp_weights_min`,
  `binary_randomized_exponential` (if `ε < 0` then `δ ≥ 1` and the conclusion is trivial); `hP1` is used only as
  `∑ P ≤ 1`.  The strict inequality `ε < |ΔΦ|` cannot be relaxed (at equality the midpoint is a correct output).
  The limit argument `mul_exp_le_of_forall_gt` is correct.  `thermal_queries_strict_cover` is vacuous at
  `β = 0` (harmless); `thermal_queries_bracket` needs and has `β > 0`.
* **m5. The soft gap is a relaxation, and a poor one for small `ε`.**  `log_sum_exp_dip_ge` replaces `(c − s)₊` by
  `c − s`; the exact effect is larger by an additive term in `[0,1]` before the logarithm, so the soft-gap radius
  is tight only when `e^ε − 1 ≳ 1`.  3-cube, `u = 1`, `δ = 0.1`: soft-gap bound `1.6`, exact-dip bound `6.4`, truth
  `7.04` at `ε = 0.05`.  For `ε = 0`, `β > 0` and positive slack off the diagonal every algorithm makes
  `(1 − 2δ)|X|` evaluations on every instance (the randomised analogue of
  `exact_free_energy_certificate_eq_univ`); Theorem 11.24 should say this and state the exact version
  (`expected_queries_ge_of_radius` already allows it).
* **m6. "The deterministic one is the integral hitting number" (1850).**  Hitting every alternative at level `ε`
  only confines the consistent values to an interval of length `2ε`; the deterministic instance complexity is the
  integral hitting number of `{D : width of V(Dᶜ) > ε}` (= `N_value`).
* **m7. "Exponent" for a lower bound.**  Row G11 ("a third (randomised) exponent"), "Honest reading" (iv), the
  table (1943) and 1949–1952 call `R^rand_β` an exponent; it is a lower bound on one, known to be exact only on
  the cube at the zero residual in the accuracy range of C1.  The deterministic row of the table (1942) lacks the
  accuracy restriction of Theorem 11.15.
* **m8. "`2^{n(1−o(1))}` evaluations at every temperature" (1983)** holds for `ε = o(n)`; at `ε = nε₁` the cited
  bound gives `exp(n(ln 2 − h(ε₁/u)))`.
* **m9. Hint-free sentence (1983–1987, §12 2(d)).**  The lower end `u²/32` is proved (at the zero residual).  The
  upper end needs (i) that the additive cone maximises `KL(π_g‖uniform)` over the class (numerically true for
  `n = 4`, `u = 0.5, 1, 2`), (ii) the concentration hypothesis of Chatterjee–Diaconis, (iii) a correctness proof
  for the estimator on the whole class.  What follows from the report's own tools is `ln cosh u ≈ u²/2`
  (Chebyshev, second moment `≤ (cosh u)ⁿ`).  Mark the upper end as heuristic.
* **m10. "What is not proved" (1990–2001).**  `ε₁^crit = max_P min_a E_P[βs(a,·) − Λ₁]` is the right vanishing point
  and `0.1137`, `0.1225` are right.  But (i) the conjecture makes `R^rand_β(ε₁)` the exponent only together with a
  hedged converse (M1) and for accuracies that are not exponentially small (C1); (ii) `ε₁^crit` depends on the
  instance and the zero residual is not the worst additive one (`0.11383` at `γ₁ = −0.037`; in closed form
  `max_q { uq − ln(μ₀ + μ₁e^{−u(1−2q)}) + (1−q) ln(μ₀ + μ₁e^{−u}) + q ln(μ₁ + μ₀e^{−u}) }`); (iii) "In general `ε₁^crit` is
  below the passive width" is a theorem, not an observation: `Λ(b) ≥ β E_{μ₀} s(·,b) − W` by the sandwich applied to
  `g` and `U_b`.
* **m11. Hub family and randomised algorithms (1905–1906).**  "Each evaluation tests one" is not a proof — the
  instance-wise bound at `g_j` is `2(1−2δ)`.  The proof needs correctness on the all-bad instance (Appendix B).
* **m12. "`k` alternatives … `kδ/(k−1)`" (1890–1891)** is right only if the instance is one of the `k`; reworded
  correctly in `6344bf9`.
* **m13. Residue of R2-M3.**  `THEORY_REPORT.md` 1030–1037 (§7 item 2: "The kind of envelope matters more than its
  size … makes `n(k−1)+1` evaluations on a star sufficient for an exact reduction") has no weak-coupling
  qualifier; `RESEARCH_LOG.md` 374 ("The way out is the *order* of the envelope") is an older entry.
* **m14. §8 (1077–1078)** lists the product form of Theorem 11.24 as machine-checked; at `f1a6015` it was **[P]**
  outside the cube (supplied in `6344bf9` by `thermal_product_randomized`).
* **m15. Stale counts.**  `BLUEPRINT.md` 788 ("36 small mutations": 79 at `f1a6015`), 797 ("B1–B7": B1–B10).
* **m16. Harness** (details in §5a): `XII.5` title says "n = 3: all sets" (only ball sizes are enumerated);
  `XII.3` cannot distinguish `1 − 2δ` from `1 − δ`; `XII.2` models no adaptive and no hedged strategy.

## 3. The R2 corrections

| item | status | where (`f1a6015`) | remark |
|---|---|---|---|
| C1 Thm 11.15, exponentially small `ε` | applied correctly | statement 1561–1568, proof 1582–1595 (level `D_Q = max(0, KL/β − a_n)`), remark 1597–1605; G7 (1180); README 96–98; §8 1082–1083; §12 1(c'); D29; `exact_free_energy_certificate_eq_univ` + witness; `DEAD.10` | proof re-derived: classes with `D_Q > 0` contribute `≤ ε_n/4` to `Z_hi/Z − 1` and to the mass outside `A`; "`π(Aᶜ) ≤ ε/(1 − e^{−βs_min})`" checked.  **The same omission recurs in Theorem 11.25(c) (my C1)** |
| M1 doubling remark | applied correctly | 1484–1490; G6 (1179); §12 2(e); D30; `DEAD.11` | recomputed (`m = 4…16`: `m+1` forced points, best-first ≤ 2); "none would help" is too strong for `f ≡ 0`, which the next sentence leaves as a conjecture |
| M2 blueprint Step 2 | applied correctly | `BLUEPRINT.md` 473–491; report 1433–1448; §12 item 1; D31; `DEAD.12` | recomputed: `0.3764` / `0.2329`; `0.1882` / `0.1066`; `0.0252` / `0` |
| M3 "the way out" | applied correctly, small residue | §11.7 title, 1698–1713, 1715–1723; G8; README 105–106; §8 1091–1094; D28, D32; `STARCERT` fallback (`BLUEPRINT.md` 519–528); `DEAD.13` | members of the class re-verified for `n = 6…10`; residue m13 |
| M4 partition-kernel separation | applied as disclosure | 1753–1768; G9; `BLUEPRINT.md` 708; D22, D33; docstrings in `PartitionProduct.lean`; `gauge_trivial_separation` | the suggested redefinition of `Rigid` through the symmetrised factor is not carried out (listed as open) |
| m1 Thm 11.18 `[V]` | applied | 1682–1686; §8 1102 | — |
| m2 Thm 11.5 not sharp | applied | 1290–1311; D21; `RefereeLemmas.lean` (`value_exchange`, `config_exchange`, `card_exchange_le` type-checked) | docstring of `CertificateNotions.lean` still gives the weaker chain (true) |
| m3 LIPO attribution | applied | 1255–1257 | — |
| m4 `thermal_binary_single_tight` | applied | 1577–1580; docstring in `ProductRates.lean` | — |
| m5 G6 "augmentation necessary" | applied | G6 row; 1479–1482 | — |
| m6 Hansen–Jaumard–Lu | applied | 1494–1495 | — |
| m7 `δ_ν ≤ (k−1)/k` | applied | 2026–2027 | — |
| m8 contrast with linear information | applied; **new problem** | 1633–1636 | the two sentences added after it (1638–1640) are my M2 |
| m9 §2.4 bullets | applied | 357–364 | matches `anchor_necessary` (`hsep : ∀ a ∈ A, a ≠ y → σ ≤ d a y`) |
| m10 treewidth `[P]`; numerics | applied | README 79–80, 107–109; §8 1079–1082; 1749–1751 | — |
| m11 "otherwise exponentially many" | applied | README 94–95; `BLUEPRINT.md` 704; 1433–1436 | — |
| m12 checking a certificate is coNP-hard | applied | §8 1086–1090 | — |
| m13 D22 vs §11.8 | applied | D22; 1753–1754 | — |
| m14 planning bound factor | applied | `BLUEPRINT.md` 477–480 | inequality re-derived |
| m15 common slope in Thm 11.9 | applied | 1388–1390 | — |
| m16 Thm 11.21 conditions | applied | 1792–1794; `BLUEPRINT.md` 560 | — |
| m17 unequal sites | applied | 1409–1415 | allocation argument checked |

No sentence in README, blueprint §9 or D28 still makes a withdrawn claim, apart from m13.

## 4. Publication assessment

**Does §11.10 change the verdict "a coherent note, not a theorem-driven paper"?**  No.  Theorem 11.22 is the
indistinguishability argument plus a union bound; with LP duality it is the bound "fractional block sensitivity ≤
randomised query complexity" transplanted to real-valued classes.  Theorem 11.23(a) is the definition of a
certificate read as "instance complexity" (Grossman–Komargodski–Naor); 11.23(b) and 11.24 insert one explicit
family of alternatives (dips); the product forms are the tensorisation already used in §11.4.  The section does
make the note more complete — it answers both requests of R2 honestly, and the finding that randomisation is
worthless for the minimum (at most the integrality gap) while it has a threshold for `ln Z` is a clean message for
the certified-optimisation audience, where Bachoc–Cesari–Gerchinovitz explicitly leave the randomised case open.

**Theorem 11.25** is the only statement of the cluster with matching sides and an exact constant.  As it stands
it is too thin: one class (uniform cube, zero known part), lower bound at one instance, both halves textbook
(ball packing; Azuma with `cosh`), part (c) wrong at one end and unproved at the other, and the qualitative
phenomenon in print.  It would become a contribution through any of:

1. *A complete statement at the zero residual*: the phase diagram of C1 (extensive, sub-extensive and
   exponentially small accuracies) with the hedged converse of M1 — exponents determined on the whole range,
   lower bounds machine-checkable with the existing lemmas.
2. *The hint-free minimax problem on the cube class*: the exponent of the worst-case cost of algorithms that are
   given nothing (between `u²/32` and, heuristically, `u²/8`).  This is a tractability question for integrating
   `e^{−βg}` over a Lipschitz class in high dimension and needs a multi-instance lower bound (as in Appendix B),
   not the instance-wise method.
3. *Beyond the cube*: is the worst-case threshold of a product class its largest Jensen gap `W₁`?  The dip bound
   gives `sup_g ε₁^crit(g) < W₁` in the asymmetric example (`0.1138` < `0.1225`), D34 shows that unions of dips can
   matter, and the passive sandwich is optimal only among mean-based procedures.  A proof or a counterexample is a
   theorem either way.
4. *The conjecture of §12 2(b)* as a two-measure asymptotic isoperimetric inequality on product spaces (tools:
   blowing-up lemma, Marton's transportation method, Bollobás–Leader-type compressions).  It must be stated with a
   window (M1), for accuracies that are not exponentially small (C1), and per instance.
5. *A bridge to the open problem of Holzmüller–Bach* (a lower bound for stochastic log-partition estimation
   outside the optimisation regime): the dip/pair technique gives instance-wise randomised lower bounds; a version
   for smoothness classes would be read by that community.

For the conjecture alone, a proof for one non-uniform two-state site would already show that the method is not
tied to Harper's theorem.

### 4a. What I read

Holzmüller–Bach (arXiv:2303.03237v4 = JMLR 26, 2025): pp. 1–13 of the PDF (abstract, §1.1, §2 with Theorems 4, 6,
7, 8, 11, 12, Proposition 9, Table 1).  Bachoc–Cesari–Gerchinovitz (arXiv:2102.01977, ar5iv): through an automatic
summary of the first 100 000 characters (definition of a certified algorithm, Theorem 2, conclusion).
Grossman–Komargodski–Naor (LIPIcs.ITCS.2020.56) and Liu–Mande (arXiv:2309.15026): abstracts only.  Tal 2013,
Gilmer–Saks–Srinivasan, Kulkarni–Tal 2016, Aaronson (randomised certificate complexity), Chatterjee–Diaconis 2018:
search-engine summaries only (the attributions in 1851–1854 agree with them; `cjtcs.cs.uchicago.edu` was not
reachable).  Not read: Novak 1988, Nemirovski–Yudin 1983, Ge–Lee–Lu 2020, Harper 1966, Heinrich; no search of the
property-testing literature.

## 5. Independent numerical checks

All code is mine (scratch directory `referee3/py/`); nothing from `experiments/` was reused except to run a copy
of the harness for §5a.

| check | sizes | result |
|---|---|---|
| **Exact instance-wise randomised complexity `R_δ(g)` by LP** (a deterministic algorithm is dominated, for the cost at `g`, by "evaluate `Q(g)`; if the values agree return `output(g)`; else evaluate everything"; outputs on the finite set `{b ± ε/2 + jε}`) — minimum | 260 random integer quasi-metric instances, 4–6 points, `ε ∈ {0,1,2}`, `δ ∈ {.02,.1,.25,.4}` | `(1−2δ) N_frac ≤ R_δ ≤ N_value` always; `R_δ/((1−2δ)N_frac)`: min `1.000` (4 equalities), median `1.50`, max `6.0`; never below `(1−2δ) N_cov`; `δ → 0` gives `N_value` |
| reduction checked against **all** adaptive trees | OR on 3 points, 16 430 deterministic trees, 8 instances, 4 values of `δ` | LP over all trees = reduced LP = `(1−2δ)·`packing in every case |
| hand check | uniform metric, 2 points, `ε = 0`: `R_δ = 2(1−δ)`; `ε = d/2`: `R_δ = 2(1−2δ)` by the mixture {blind `δ`, two hedged singletons `δ` each, full `1−3δ`} | LP agrees; the factor `1−2δ` is attained for the whole class |
| integrality gap | 7-point instance with `N_cov = 3`, `N_frac = 2.5` | `R_δ = 2.8, 2.6, 2.0` at `δ = .05, .1, .25`: above `(1−2δ)N_cov` |
| `R_δ` for `ln Z` | 60 random 4-point instances | no violation of the soft-gap, exact-dip or general bound; soft-gap bound up to `6.2×` below `R_δ`, up to `4×` below the all-alternatives bound |
| D34 (uniform metric, `n = 8`, `β = 1`, `ε = 0.3`) | symmetric LP | hitting number `4`, dip bound `1` (as stated); `R_δ = 5.65, 4.80, 2.79, 1.53` at `δ = .05, .1, .25, .4` |
| 3-cube, `u = 1` | orbit-reduced LP | `ε = 0`: `R_δ = 7.2`; `ε = 0.2`: `6.4` (= pair bound; report's bound `3.2`); `ε = 1`: `2.01`; at `g = c\|x\|`: `N_det = 2` for all `ε` |
| cube, closed form vs exact ball counts (B10) | `u = 0.5, 1, 2, ln 16`; `n = 100…6400`, `ε = 0.5` | B10 values reproduced (`0.02336, 0.01308, 0.00935` …); `n = 6400`: `0.0082, 0.0298, 0.0980, 0.1570` against `0.0077, 0.0291, 0.0973, 0.1561` |
| cube, threshold | `u = 1` | `ρ(ε₁) < 1/2 ⇔ ε₁ < ln cosh(u/2) = 0.12011`; `(27/16)^m` and `0.2425 m` re-derived |
| cube, `ε` vs `ε/2`, hedging, small `ε` | `n ≤ 3200` resp. `6400` | tables in C1, M1 |
| three exponents, primal (Blahut–Arimoto over types) vs dual LP | two-state sites `e ∈ {0.5, 2}`, `c = 1`, 7 values of `β`; cube | `R^rand = 0.0275, 0.1541, 0.1882` vs `R_β = 0.6658, 0.4817, 0.2159` at `β = 1, 4, 40`; sharp site `0.0129`; cube `0.00767, 0.02914, 0.09728, 0.15614`; `ε₁^crit = 0.1137`, passive width `0.1225` |
| `R^rand_β ≤ R_β`, `R_β ≥ H(π)`, `ε₁^crit ≤ W₁` | 45 random two- and three-state sites with residuals × 5 temperatures | no violation (margins `≥ −6·10⁻⁵`, grid error) |
| D30, D31, D32 | as in the dead ends | reproduced |
| Harper step | all supports of the 3- and 4-cube, `u = 0.5, 1.5` | initial segments of the simplicial order maximise `Σ_{x∈D} e^{u dist(x,Dᶜ)}` at every size |
| hub family | `N = 4`, `M = 3` | `N_cov = 2` with a good hub, `5` without |
| additive cone maximises `KL(π_g‖uniform)` | `n = 4`, multi-start SLSQP | yes for `u = 0.5, 1, 2` |

### 5a. Harness

Run on a scratch copy of the `f1a6015` harness (quick mode): `XII.1`–`XII.5` survive, `DEAD.10`–`DEAD.14` are
refuted as documented.

* `XII.1` exercises its title (identities of the dip on random instances); `ε' = 0.25` only.
* `XII.2` tests the inequality that the proof establishes, on mixtures of *fixed* evaluated sets that return the
  hint's minimum, plus blind guesses.  It models neither adaptivity (harmless, by the reduction above) nor hedged
  outputs of a partial evaluation — the strategies that are optimal for the whole class.  It can detect a wrong
  constant (`M1`) or a wrong radius (`M2`); it could not detect a failure of the theorem.
* `XII.3`: the certificate half is a real exhaustive test.  The randomised half has no blind component, so
  `(1 − δ)·`packing `≤` cost holds in its family: **a copy with `1 − δ` in place of `1 − 2δ` survives** (full and
  quick mode).  It tests the detection radius, not the factor.
* `XII.4` exercises its title; `XII.5` enumerates ball sizes only (title: "n = 3: all sets").
* `DEAD.10`–`DEAD.13` recompute R2's counterexamples; `DEAD.14` hard-codes the dip side.  `DEAD.12`, `DEAD.13`
  have no mutation.  Nothing tests Theorem 11.25(c) outside `ε = 0.5`.
* B10 is correct and reproduced; its ball-count column uses a fixed `ε` and therefore hides both C1 and M1.

## 6. Not checked

* `lake build`, `scripts/audit_all.sh`, the harness in full mode, the mutation run.
* `SoftGapBounds.lean`, Theorem 11.26, `XII.6`, Theorem 11.23(c) / `min_spotCheck_correct`, "Without a hint",
  "No sharp regime at finite temperature", `QueryRefinements.lean` (all later than `f1a6015`) beyond the remarks
  of §7.
* The type covering lemma and Merhav's theorem behind the **[P]** upper bounds of Theorems 11.9 and 11.15; I
  checked the corrected proof of 11.15 for internal consistency only.
* Harper's theorem beyond `n = 4`; asymptotics beyond `n = 6400`.
* The upper ends of the phase diagram of C1 beyond the count `2ⁿ/|B|` (they rest on Harper).
* An instance with a large integrality gap (whether a randomised algorithm can beat `(1−2δ) N_cov`).
* `RESEARCH_LOG.md`; the first research phase; R1.

## 7. Changes made during the review

* `6344bf9`, Theorem 11.26 (not refereed).  Its spot-check is unhedged and its sample size carries `1/(1 − e^{−ε/2})`,
  consistent with C1.  The sentence "far from the true exponent `ln 2 − h(ρ₀)` of Theorem 11.25(c)" inherits C1 and
  M1.  The new README sentence (about `(2/(1+e^{−βc}))ⁿ` random against `2ⁿ` deterministic evaluations) compares two
  instance-wise costs at the zero residual, both with a hint; say so.
* Uncommitted Theorem 11.23(c): the bracket `(1−2δ) N_frac(ε) ≤ E|Q| ≤ ⌈ln(1/δ)(N_frac(ε/2) + 1)⌉` is correct, but
  "gains the integrality gap … and no more" and the docstring's "exactly the integrality gap" do not follow:
  `N_frac(ε/2)` can exceed `N_cov(ε)` without bound (uniform metric, `ε = 1.5 d`: `N_cov(ε) = N_value = 1`,
  `N_frac(ε/2) = n`).  With the hedged output of M1 the upper bound becomes `ln(1/δ)(N_frac^{open}(ε) + 1)`.
* Uncommitted closed form `ε₁^crit = ½ ln(1 + 2p(1−p)(cosh βc − 1))`: agrees with my value (`0.11367` at `p = 0.3775`,
  `βc = 1`).  It is the value at the zero residual, not the worst case over instances (m10).
* m12 is fixed in `6344bf9`; m14 is fixed by `thermal_product_randomized`.

## Appendix A. Referee lemmas, machine-checked

Scratch files `referee3/R3check2.lean` … `R3check5.lean` (outside the repository), checked with
`lake env lean <file>` from the repository root when written (18:54–20:20) and all four again at the end against
the then current build of `QueryLowerBound`; all depend on `propext`, `Classical.choice`, `Quot.sound` only.  All import `Mathlib` and
`proofs.Frontiers.QueryLowerBound`, and sit in `namespace MetricChain.Referee3` with `open Finset MetricChain`.

### A.1 A `QueryAlgorithm` that is not a decision tree

```lean
def pat : Bool → Bool → Bool → Finset (Fin 3)
  | false, true, _ => {0, 1}
  | _, false, true => {1, 2}
  | true, _, false => {0, 2}
  | _, _, _ => {0, 1, 2}

theorem pat_stable : ∀ b0 b1 b2 c0 c1 c2 : Bool,
    ((0 : Fin 3) ∈ pat b0 b1 b2 → c0 = b0) → ((1 : Fin 3) ∈ pat b0 b1 b2 → c1 = b1) →
    ((2 : Fin 3) ∈ pat b0 b1 b2 → c2 = b2) → pat c0 c1 c2 = pat b0 b1 b2 := by
  decide

open Classical in
noncomputable def sgn (g : Fin 3 → ℝ) (i : Fin 3) : Bool := decide (0 < g i)

theorem sgn_congr {g g' : Fin 3 → ℝ} {i : Fin 3} (h : g' i = g i) : sgn g' i = sgn g i := by
  unfold sgn
  rw [h]

noncomputable def pathoAlg : QueryAlgorithm (Fin 3) where
  queries := fun g => pat (sgn g 0) (sgn g 1) (sgn g 2)
  output := fun _ => 0
  consistent := by
    intro g g' h
    refine ⟨?_, rfl⟩
    exact pat_stable _ _ _ _ _ _ (fun h0 => sgn_congr (h 0 h0)) (fun h1 => sgn_congr (h 1 h1))
      (fun h2 => sgn_congr (h 2 h2))

theorem pat_nonempty : ∀ b0 b1 b2 : Bool, (pat b0 b1 b2).Nonempty := by
  decide

theorem pathoAlg_not_a_tree :
    (∀ g, (pathoAlg.queries g).Nonempty) ∧ ¬ ∃ a : Fin 3, ∀ g, a ∈ pathoAlg.queries g
```

(proof: evaluate the query set on the indicator functions of the points `2`, `0`, `1`, which gives `{1,2}`,
`{0,2}`, `{0,1}`; `fin_cases a <;> simp`.)

### A.2 Tiny accuracies on the cube (C1) — complete source

```lean
theorem hamEnv_ge_of_ne {n : ℕ} {c : ℝ} (hc : 0 ≤ c) {x y : Fin n → Bool} (h : x ≠ y) :
    c ≤ hamEnv (fun _ : Fin n => c) x y := by
  obtain ⟨i, hi⟩ := Function.ne_iff.mp h
  unfold hamEnv
  have hnn : ∀ j ∈ (univ : Finset (Fin n)), 0 ≤ (if x j = y j then (0 : ℝ) else c) := by
    intro j _
    split_ifs
    · exact le_rfl
    · exact hc
  have hsingle := Finset.single_le_sum hnn (mem_univ i)
  rw [if_neg hi] at hsingle
  exact hsingle

theorem cube_one_point_dip (n : ℕ) {β c : ℝ} (hc : 0 ≤ c) (y : Fin n → Bool) :
    ∑ x, Real.exp (-β * ((0 : ℝ) + dip (hamEnv fun _ : Fin n => c) (fun _ => 0) y c x)) =
      2 ^ n - 1 + Real.exp (β * c) := by
  have hd : IsEnvelope (hamEnv (σ := fun _ : Fin n => Bool) fun _ => c) :=
    hamEnv_isEnvelope fun _ => hc
  have hterm : ∀ x : Fin n → Bool,
      Real.exp (-β * ((0 : ℝ) + 0)) *
        Real.exp (β * max 0 (c - slack (hamEnv fun _ : Fin n => c) (fun _ => 0) x y)) =
          1 + (if x = y then Real.exp (β * c) - 1 else 0) := by
    intro x
    have hs : slack (hamEnv fun _ : Fin n => c) (fun _ => (0 : ℝ)) x y =
        hamEnv (fun _ : Fin n => c) x y := by
      unfold slack
      ring
    rw [hs]
    by_cases hxy : x = y
    · subst hxy
      rw [hd.self x, sub_zero, max_eq_right hc, if_pos rfl]
      simp
    · have hge := hamEnv_ge_of_ne hc hxy
      rw [if_neg hxy, max_eq_left (by linarith)]
      simp
  have h := sum_exp_dip β (hamEnv fun _ : Fin n => c) (fun _ : Fin n → Bool => (0 : ℝ))
    (fun _ => (0 : ℝ)) y c
  refine h.trans ?_
  rw [Finset.sum_congr rfl fun x _ => hterm x, Finset.sum_add_distrib, Finset.sum_ite_eq']
  simp
  ring

open Classical in
theorem cube_small_accuracy_randomized (n : ℕ) {Ω : Type*} [Fintype Ω]
    (alg : Ω → QueryAlgorithm (Fin n → Bool)) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω)
    (hP1 : ∑ ω, P ω = 1) {β c ε δ : ℝ} (hc : 0 < c)
    (hε : ε < Real.log (2 ^ n - 1 + Real.exp (β * c)) - Real.log (2 ^ n))
    (hcorr : ∀ g, Admissible (hamEnv fun _ : Fin n => c) g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output g -
        Real.log (∑ x, Real.exp (-β * ((0 : ℝ) + g x)))| ≤ ε / 2), P ω) :
    (1 - 2 * δ) * 2 ^ n ≤ ∑ ω, P ω * ((alg ω).queries fun _ => 0).card := by
  have hd : IsEnvelope (hamEnv (σ := fun _ : Fin n => Bool) fun _ => c) :=
    hamEnv_isEnvelope fun _ => hc.le
  have hadm := admissible_zero_hamEnv (n := n) (c := c) hc.le
  have hZ0 : ∑ _x : Fin n → Bool, Real.exp (-β * ((0 : ℝ) + 0)) = (2 : ℝ) ^ n := by
    simp
  have key := expected_queries_ge_of_radius
    (Φ := fun g : (Fin n → Bool) → ℝ => Real.log (∑ x, Real.exp (-β * ((0 : ℝ) + g x))))
    hd alg P hP hP1 hcorr hadm (fun _ => c)
    (fun y => by
      show ε < |Real.log (∑ x, Real.exp (-β * ((0 : ℝ) +
          dip (hamEnv fun _ : Fin n => c) (fun _ => 0) y c x))) -
        Real.log (∑ _x : Fin n → Bool, Real.exp (-β * ((0 : ℝ) + 0)))|
      rw [cube_one_point_dip n hc.le y, hZ0]
      exact lt_of_lt_of_le hε (le_abs_self _))
    (fun _ => (1 : ℝ)) (fun _ => zero_le_one) (B := 1)
    (fun a => by
      have hsub : univ.filter (fun y : Fin n → Bool =>
          slack (hamEnv fun _ : Fin n => c) (fun _ => (0 : ℝ)) a y < c) ⊆ {a} := by
        intro y hy
        have hlt := (Finset.mem_filter.mp hy).2
        have hs : slack (hamEnv fun _ : Fin n => c) (fun _ => (0 : ℝ)) a y =
            hamEnv (fun _ : Fin n => c) a y := by
          unfold slack
          ring
        rw [hs] at hlt
        by_contra hne
        have hne' : a ≠ y := fun h => hne (by rw [Finset.mem_singleton]; exact h.symm)
        have := hamEnv_ge_of_ne hc.le hne'
        linarith
      calc ∑ y ∈ univ.filter (fun y : Fin n → Bool =>
            slack (hamEnv fun _ : Fin n => c) (fun _ => (0 : ℝ)) a y < c), (1 : ℝ)
          ≤ ∑ y ∈ ({a} : Finset (Fin n → Bool)), (1 : ℝ) :=
            Finset.sum_le_sum_of_subset_of_nonneg hsub fun _ _ _ => zero_le_one
        _ = 1 := by simp)
  have hcard : ∑ _y : Fin n → Bool, (1 : ℝ) = (2 : ℝ) ^ n := by
    simp
  rw [hcard, mul_one] at key
  exact key

theorem cube_exact_randomized (n : ℕ) {Ω : Type*} [Fintype Ω]
    (alg : Ω → QueryAlgorithm (Fin n → Bool)) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω)
    (hP1 : ∑ ω, P ω = 1) {β c δ : ℝ} (hβ : 0 < β) (hc : 0 < c)
    (hcorr : ∀ g, Admissible (hamEnv fun _ : Fin n => c) g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output g -
        Real.log (∑ x, Real.exp (-β * ((0 : ℝ) + g x)))| ≤ (0 : ℝ) / 2), P ω) :
    (1 - 2 * δ) * 2 ^ n ≤ ∑ ω, P ω * ((alg ω).queries fun _ => 0).card := by
  refine cube_small_accuracy_randomized n alg P hP hP1 hc ?_ hcorr
  have h1 : (1 : ℝ) < Real.exp (β * c) := Real.one_lt_exp_iff.mpr (mul_pos hβ hc)
  have h2 : (0 : ℝ) < 2 ^ n := by positivity
  have := Real.log_lt_log h2 (show (2 : ℝ) ^ n < 2 ^ n - 1 + Real.exp (β * c) by linarith)
  linarith
```

### A.3 Hedged spot-check (M1)

```lean
open Classical in
noncomputable def hedgedSpotCheck (Φ : (X → ℝ) → ℝ) (g₀ : X → ℝ) (o : ℝ) {N : ℕ} (a : Fin N → X) :
    QueryAlgorithm X where
  queries := fun g => if ∀ k, g (a k) = g₀ (a k) then univ.image a else univ
  output := fun g => if ∀ k, g (a k) = g₀ (a k) then o else Φ g
  consistent := -- as for `spotCheck`

theorem hedgedSpotCheck_card_le (Φ : (X → ℝ) → ℝ) (g₀ : X → ℝ) (o : ℝ) {N : ℕ} (a : Fin N → X) :
    ((hedgedSpotCheck Φ g₀ o a).queries g₀).card ≤ N

theorem hedgedSpotCheck_correct (g₀ : X → ℝ) (o : ℝ) (N : ℕ) (q : X → ℝ) (hq : ∀ x, 0 ≤ q x)
    (hq1 : ∑ x, q x = 1) {ε δ p : ℝ} (hε : 0 ≤ ε) (hp1 : p ≤ 1)
    (hp : ∀ g, G g → ε / 2 < |Φ g - o| → p ≤ ∑ x ∈ univ.filter (fun x => g x ≠ g₀ x), q x)
    (hN : (1 - p) ^ N ≤ δ) (g : X → ℝ) (hg : G g) :
    1 - δ ≤ ∑ a ∈ univ.filter (fun a : Fin N → X =>
      |(hedgedSpotCheck Φ g₀ o a).output g - Φ g| ≤ ε / 2), ∏ k, q (a k)

theorem hedged_window_up {ε η Φg Φg₀ : ℝ} (h : ε / 2 < |Φg - (Φg₀ + ε / 2 - η)|) :
    ε - η < Φg - Φg₀ ∨ η < Φg₀ - Φg
```

The proofs of the first three are those of `spotCheck`, `spotCheck_card_le`, `spotCheck_correct` in
`QueryLowerBound.lean` with `Φ g₀` replaced by `o` (and `hclose : |Φ g - o| ≤ ε / 2`); the last is
`rcases lt_abs.mp h with h1 | h1 <;> [left; right] <;> linarith`.

### A.4 Pair version of the detection principle

```lean
theorem exists_query_ne_pair (alg : QueryAlgorithm X) {ε : ℝ}
    (hcorr : ∀ g, G g → |alg.output g - Φ g| ≤ ε / 2) (g : X → ℝ) {g₁ g₂ : X → ℝ}
    (h₁ : G g₁) (h₂ : G g₂) (hΦ : ε < |Φ g₁ - Φ g₂|) :
    ∃ a ∈ alg.queries g, g₁ a ≠ g a ∨ g₂ a ≠ g a

theorem prob_query_ne_pair (alg : Ω → QueryAlgorithm X) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω)
    (hP1 : ∑ ω, P ω = 1) {ε δ : ℝ}
    (hcorr : ∀ g, G g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output g - Φ g| ≤ ε / 2), P ω)
    (g : X → ℝ) {g₁ g₂ : X → ℝ} (h₁ : G g₁) (h₂ : G g₂) (hΦ : ε < |Φ g₁ - Φ g₂|) :
    1 - 2 * δ ≤ ∑ ω ∈ univ.filter
      (fun ω => ∃ a ∈ (alg ω).queries g, g₁ a ≠ g a ∨ g₂ a ≠ g a), P ω
```

(proofs: those of `exists_query_ne`, `prob_query_ne_ge` with the events "correct on `g₁`", "correct on `g₂`"; a run
that sees neither returns the same number on both.  `g` need not belong to the class.)  Consequence:
`E|Q(g)| ≥ (1 − 2δ) τ*`, `τ*` the fractional hitting number of `{D : width of V(Dᶜ) > ε}`, whose integral version is
`N_value`.  Checked against the exact LP on 120 instances (never violated, 8 equalities).

### A.5 The factor `1 − 2δ` is attained

`packing_factor_attained`: on the class `{0, 1}` of functions on a one-point space, `Φ g = g ()`, `ε = 1/2`,
`0 ≤ δ ≤ 1/2`, the mixture {full evaluation: `1 − 2δ`; blind `0`: `δ`; blind `1`: `δ`} is correct with probability
`1 − δ` on both members and makes `1 − 2δ` evaluations on `0` in expectation — equality in
`expected_queries_ge_packing` with a genuinely randomised algorithm.

## Appendix B. The hub family defeats randomised algorithms (proof)

Instances `g_j` (hub `j` good) and `g_∅` (all hubs at `−0.7`; admissible).  Algorithms are mixtures of decision
trees (the statement is about actual procedures; the abstract `QueryAlgorithm` has no query order).  For a tree
`ω` let `σ_ω` be its query sequence on `g_∅`, `T_ω` its length and `S_ω` the set of shallow states in it.  (1) On `g_∅` a dip of
depth `1.5 + ε'`, `ε < ε' < 0.2`, at a shallow state `y` is seen from `y` only (hubs have slack `1.7`), so by
`prob_query_ne_ge` each `y` is queried with probability `≥ 1 − 2δ`: `E|S_ω| ≥ (1−2δ)N`.  (2) `g_j` and `g_∅` differ
at hub `j` only, so the run on `g_j` follows `σ_ω` until hub `j` appears: `|Q_ω(g_j)| ≥ min(pos_j(ω), T_ω)`.  The hubs
occupy distinct positions, hence `M⁻¹ Σ_j |Q_ω(g_j)| ≥ M⁻¹ Σ_{i ≤ M} min(i, T_ω) ≥ min(T_ω, M)/2 ≥ min(|S_ω|, M)/2`.
(3) `P(|S_ω| ≥ (1−2δ)N/2) ≥ (1−2δ)/2`.  Therefore
`max_j E|Q(g_j)| ≥ ((1−2δ)/4) min((1−2δ)N/2, M) ≥ ((1−2δ)²/8) min(N, M)`, while `N_cov(g_j) = 2`.
