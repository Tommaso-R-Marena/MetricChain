# Dead ends and refuted statements — science division

*Everything of ours that turned out false, vacuous or misleading, and every negative
result that closes an obvious route, in one place.  Written 2026-11-25 (checkpoint 20).
The theory division keeps the same kind of file (`docs/DEAD_ENDS.md`, D1–D52); numbering
here is `SD`.  Each entry: what was claimed, what is true, how it was found, where it was
corrected.*

## A. False or overstated sentences of ours that were published

| # | claimed | true | found by | corrected in |
|---|---|---|---|---|
| SD1 | "Populations of single states are identified up to polynomial factors" (SCI-MSG-0001 §4; note v2, reading after Theorem 3) | only the *upper* end is polynomial; populations are not bounded below and not identified; the data exclude dominance | referee R3 (M2) | SCI-MSG-0008 §1(a); note v3 |
| SD2 | "A caloric curve determines `ln Z` without any model … this is how absolute entropies are measured" (SCI-REQ-0001 Q1; note v2 §10, in bold) | Proposition 9 needs the curve down to `β = 0` on the model's configuration space; calorimetry works from `T → 0` and measures all degrees of freedom | referee R3 (M5) | SCI-MSG-0008 §1(b); note v3 |
| SD3 | pinned one-body marginals are "a third kind of local data … not the order of the observable" (SCI-MSG-0003 §3) | with exact oracles a conditional marginal is a ratio of higher-order marginals; the right statement is a trade-off in the order (Theorem 4‴), and a real distinction appears only with finite precision (addenda A9, A10) | the coordinator, trying to prove a trade-off | SCI-MSG-0004; addenda A7 (kept with a note), A8 |
| SD4 | the adaptive upper bound "answers, on a model class, the question Mathé and Novak leave open" (SCI-REV-0004) | they pose no such question | workstream A1's final report | SCI-RES-0003 §4 |
| SD5 | "in a first-order class" local data are worth a polynomial factor (SCI-MSG-0001 §4 heading; digest 2) | proved for the cube with zero known part, in the worst case; at a cone instance the oracle is worth an exponential factor to a non-adaptive algorithm | referee R3 (M6) | SCI-MSG-0008 §2 |
| SD6 | Theorem 2 read as "local data certify nothing about the entropy" | existential, for the uniform data vector, with content only when `n(ln 2 − h(σ))` exceeds the logarithm of the code size (9 of our 16 numerical cases) | referee R3 (M1) | SCI-MSG-0008 §2; note v3 |
| SD7 | "the worst-case exponent is unchanged" by a mean-energy datum | at bounded accuracy only | referee R3 (M3) | SCI-MSG-0008 §2 |
| SD8 | "the limit shape is the asymptotic model-free identified set", next to numbers for walks | proved for bridges at interior profile densities; for walks an inclusion, equality under Conjecture 11.75 | referee R3 (M4) | SCI-MSG-0008 §2 |
| SD9 | falsification numbers "0.87–0.96 of the strength of the missing interaction" | `b_min` was compared with `ε`, not with the truth's own envelope constant, of which it is about half at 9–10 beads | the coordinator, at the next size | SCI-MSG-0002 §3 |
| SD10 | "first replication of ten Lean files since `4cef47e`" | engineering had replicated `63efc69`; first for three files, second for seven | reading engineering's checkpoint 3 | `INDEPENDENT_VALIDATION.md` §1.1 |
| SD35 | Proposition A1.2 as sent in SCI-RES-0003: site envelopes "`d_j ≥ 0` with the triangle inequality"; item 1 "the vertices of the site's Lipschitz polytope" | the proof uses a zero diagonal (not listed; item 2 is false without it) and never the triangle inequality; the Lipschitz class is invariant under adding constants and has no extreme points — the statement is for the class normalised at a base point.  The conclusion stands for quasi-metric envelopes | the formalisation (workstream L2; machine-checked counterexample) | SCI-MSG-0014 §2; marked in SCI-RES-0003 |
| SD36 | "The one-body oracle does not lower the class exponents with a field **because the hardest instance is self-consistent**" — Augustin's fixed point `Q* = Σ M*V_φ`, with `V_φ` "the type that carries the mass of a hidden dip" (SCI-RES-0004 §4; `F_brief.md`) | the statement is true, the reason false: the mass of a dip sits on the cone law `MW` (`V_φ` is its rim), and `M*W ≠ Q*` for `p ≠ ½` (gap `0.006 … 0.21`); with additive bases and forced centre types 13–100 % of `R^max` is lost.  The actual mechanism is compensation — add a multiple of an extreme additive instance to both members of a pair | workstream F (`SF_REPORT.md` §2.4) | SCI-RES-0006 §4; marked in SCI-RES-0004 |

*What they have in common.*  None was a wrong proof.  Each was a sentence of
interpretation — a scope, a quantifier, a physical gloss, an attribution — written in the
same step as a correct result.  Rules adopted in consequence are listed in
`RESEARCH_SYNTHESIS.md` §4.

## B. Errors of record-keeping

| # | what | corrected |
|---|---|---|
| SD11 | the sync log listed three fetches that had not been run | sync log, checkpoint 6 |
| SD12 | a commit message (`23cbee9`) named an upstream head read before the fetch returned | sync log |
| SD13 | headers of six messages carried estimated times, up to 35 minutes ahead of the clock; two headings of the research log likewise | checkpoint 11; cycle 9 of the log |
| SD14 | a workstream's report was committed and quoted before the workstream had finished (it then proved what the quotation said was unproved) | SCI-RES-0001 §2; policy "snapshots are not statements" |

## C. Checks of ours that were vacuous or misleading

| # | what | lesson |
|---|---|---|
| SD15 | `finite_precision_check.py` reported "bound holds" against the trivial bound `κ_j(0) = 1` | a check must be able to fail; the real statement was proved later (A10) with a script that tests the identity to `10⁻⁵⁹` |
| SD16 | the numerical check of Theorem 2 tested a variant of the measure for which one part was not proved, and was empty in 9 of 16 cases | state the regime in which a statement has content before testing it |
| SD17 | **solver tolerances** — default HiGHS tolerances produced "violations" of exact statements three times in one day: 3 of 900 instances of A11 (`10⁻⁶ … 10⁻⁵`), workstream R5's first run (`10⁻⁹`), and, in the theory division's `wv_lib.py`, an upward bias of a blind maximisation | scale variables; tolerance `10⁻¹⁰`; check feasibility of the returned point before believing a counterexample |
| SD18 | the Pinsker form of Theorem 7 (`TV ≤ βω/4`) is vacuous for `βω ≥ 4` | the sharp form `tanh(βω/4)` was found three times independently |
| SD31 | `plateau_twin_check.py`, first version: the root of `U′ − U₀` was sought on the difference of two mean energies computed separately; the true difference is of relative size `e^{−Ω(n)}` and vanished in floating point — a false "no root" in four of ten cases and a wrong root radius in a fifth | compute the sign through the excess identity (mean effective energy of the excess mass minus `U₀`), term by term positive; the referee had said so for the equal twin (R3 report, on Proposition 5b) and the coordinator repeated the mistake on the next construction |

## D. Negative results that close a route

| # | route | result | where |
|---|---|---|---|
| SD19 | first-order (per-torsion) envelopes for a continuum-solvent term in backbone torsions | constants `12–53 k_BT` growing with length; no sharp site; certificates are a fixed fraction of the domain.  Hypothesis H3 of `BENCHMARK_DESIGN.md` fails for this residual by the criterion written before the measurement | SCI-RES-0002 |
| SD20 | "GB is nearly pairwise" as a basis for a certificate | true in RMS (0.1–0.5 kcal/mol), false in sup norm (up to 9 kcal/mol); freezing the Born radii is useless (RMS 5 kcal/mol) | SCI-RES-0002 |
| SD21 | a sup-norm remainder fitted on a sample as a bound | held-out maxima up to ten times the fitted ones | SCI-RES-0002 |
| SD22 | low-order averaged data as a substitute for evaluations in a first-order class | worth a polynomial factor at best — exactly for bounded order, and for every order at fixed precision | note v3; addenda A1, A10 |
| SD23 | a mean-energy datum as a certificate that nothing is hidden | excludes deeper hidden states, not a twin of the same depth | note v3 §5 |
| SD24 | cuts stated as an "iff" (our own brief for workstream K) | false in two-vertex examples; the correct form is Edmonds–Fulkerson's | SCI-MSG-0005 |
| SD25 | coordinate cuts under unrestricted single-site moves; Lagrangian or Chernoff relaxation of a counting cut | certify nothing beyond the trivial bound | SCI-MSG-0005 |
| SD26 | a transfer matrix for barriers of chains | the threshold problem is PSPACE-complete (Wrochna) | SCI-MSG-0005 |
| SD27 | "be Bayesian" as the remedy for worst-case cost | the price is the geometry of the class; a Bayesian certificate fails silently on a dip (coverage 9 %); no procedure correct on a first-order class is cheap on a subclass | SCI-MSG-0007 |
| SD28 | "polynomial iff the spectrum decays" for `ln Z` under a prior | false: a white tail self-averages in the annealed regime | SCI-MSG-0007 |
| SD29 | the uniform field as extremal residual for *every* macrostate ratio | false for frustrated known parts (49–81 % of random instances) and for non-monotone macrostates | addendum A11 |
| SD30 | identifying a chain from its complete distance distribution | homometric lattice chains from 6 beads on; 19 % of 9-bead site sets on the cubic lattice | SCI-REV-0006 |
| SD32 | equal-depth twins as the lower bound with a mean-energy datum at extensive accuracy (`h − ε₁`; SCI-MSG-0008 R3-T3) | superseded: a twin must have the visible state's energy and `ε₁n` more entropy, so it is as deep and wider (plateau twin); `h − ε₁` is void from `ε₁ = h` on, the plateau bound only near `a(u)` | addendum A16; SCI-MSG-0012 |
| SD33 | "the exponents are those of the class, not of the oracle" as a slogan for the mean-energy datum | true at bounded accuracy only: beyond `KL(σ_u‖½)` per site the datum alone gives the answer (entropy bracket), and without it the cost is exponential up to `KL(½‖σ_u)` | addendum A16; SCI-MSG-0012 §3 |
| SD34 | hiding the plateau twin on a visible terrace, or on the wall of the visible basin | terrace: never better than the flat background (twelve cases, exponential-scale formulas); wall: the simple dips have depth `O(1)`.  Evidence for Conjecture A16.4, not a proof | addendum A16 |
