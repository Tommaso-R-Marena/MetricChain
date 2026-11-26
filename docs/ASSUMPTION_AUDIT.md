# Assumption audit and hierarchy of the theory

*Theoretical Research Division, 2026-11-26.  Written under the research owner's
supplementary directive of the same day ("Mathematical Generality, Physical Relevance, and
Foundational Breakthroughs"; relayed verbatim in
`docs/collaboration/messages/theory/THY-MSG-0016.md`): for every major theorem, say which
assumptions are essential, which are artefacts of the proof, which are conveniences,
which can be replaced by weaker quantitative conditions, whose removal changes the
complexity, and whose removal makes the result false; build the hierarchy from the most
tractable models to broader classes; "avoid presenting results for restricted models as
universal conclusions"; and identify general theorems whose guarantees are
computationally vacuous.*

This file is the synthesis.  The theorem-by-theorem tables are in four reports, which it
does not repeat:

| source | covers | size |
|---|---|---|
| `docs/audit/AA1_REPORT.md` | theory report §§2–6 and §§11.1–11.15: 71 numbered statements | 202 assumptions carrying 216 tags |
| `docs/audit/AA2_REPORT.md` | theory report §§11.16–11.32: 85 numbered statements | 297 tags (the report counts tags, not assumptions) |
| `docs/workstreams/N_REPORT.md` §6 | the nested adaptive algorithm (Theorems 11.52, 11.54, 11.56, 11.58), from an abstract form of the theorem | 25 rows |
| `docs/workstreams/R_REPORT.md` §9 | the rate of the level recursion | structural part against the one analytic hypothesis |

**Status.**  The two audits were made by independent internal readers (AI agents briefed
by the coordinator; internal reviews, not external peer review), each with its own
scripts (`experiments/audit/AA1`, `experiments/audit/AA2`: 15 scripts — seven and eight; an
earlier version of this file said 14).  The coordinator re-ran them — every output was
identical to the stored one; on a second run at the time of the corrections below, 14 are
identical again and the fifteenth, which cross-checks the Lean names cited in the theory
report, differs only through the report's later growth — and verified the one error of
substance that the audits found (Theorem 11.33(a), §7 below).  The
corrections to the theory report and the README are recorded item by item in
`docs/audit/APPLIED_CORRECTIONS.md`.  The table for the nested algorithm rests on workstream
N, which has since been refereed internally (`docs/workstreams/N_REVIEW.md`: the level theorem
correct as stated; six rows of its table reclassified — the counts below are the revised
ones); the rate theorem has been refereed internally in both halves (no error of
substance).
**The audit has itself been reviewed on a sample** by the Scientific Discovery Division
(its SCI-REV-0022 and `docs/science/workstreams/R23_REPORT.md` on its branch
`research/scientific-translation`, commit `88c9a90`: 32 of the 513 tags drawn by a rule fixed
in advance, all 15 scripts re-run, a third replicated with independent code; an internal
review by an AI session).  Its verdict, its corrections and what was done about them are
§1a below; the counts of §1 are the corrected ones.
Classifications are judgements with evidence attached; where the evidence is "not known"
the reports say so, and §8 collects those cases.  Line numbers in the two audit reports
and in the record of corrections refer to the theory report and the README as the audits
read them (commit `020e990`); the corrections made both files longer.

## 1. The categories, and the counts

Counts of tags (an assumption can carry two), after the corrections of §1a; in brackets
the counts as the audits delivered them, where different.

| label | meaning (the directive's six categories, and one more) | AA1 | AA2 | N (25 rows; two labels possible) |
|---|---|---|---|---|
| E | essential to the result | 53 (52) | 63 | 4 |
| P | required only by the current proof technique — **see the note below the table** | 13 (16) | 59 (62) | 5 |
| C | introduced for computational or expository convenience | 27 (26) | 29 | 6 |
| Q | replaceable by a weaker quantitative condition (stated in the entry) | 39 | 29 (28) | 7 |
| X | removal changes the computational complexity (how, in the entry) | 14 (13) | 18 | 9 |
| F | removal makes the result false (counterexample in the entry) | 47 | 52 | 3 |
| ? | not known | 23 | 47 (45) | 9 |
| | all tags | 216 | 297 | |

*What the row P contains* (SCI-REV-0022, finding F3).  The audits used the tag for three
different things: (i) another proof of the statement without the assumption is on record
and named in the entry; (ii) the present proof uses the assumption at a named step and
nothing is known about the statement without it; (iii) an ingredient that is itself a
theorem (Harper's theorem, the binomial median) and not a hypothesis on the model.  Only
(i) supports "the statement survives".  The entries have not been re-sorted beyond the
sample; a reader should apply the rule of §1a.

A third of the classifications are either load-bearing in the strongest sense (F: about
one in five) or of unknown status (?: about one in seven); with E it is more than half;
fewer than one in six is a pure convenience.  (An earlier version said "half … are F or
?"; that was wrong arithmetic — SCI-REV-0022, g1.)  The theory is a theory of its models
much more than its summaries said — 47 sentences of the report and the README were found
to state more than is proved (§7).

**The label P is itself a claim** (a point of the Scientific Discovery Division's first
reading of this file, SCI-RES-0031 §2(b), taken as it stands).  "Required only by the
current proof" says that the statement survives without the assumption — a conjecture
unless the entry attaches another proof, a check or an argument.  The entries of the two
audit reports say what they attach; where an entry attaches nothing, read P as "believed
removable, not shown".  The research owner's sentence "Do not assume that these
generalizations are necessarily possible" applies to exactly this label.  That division's
sampled review has since put numbers on it:

## 1a. The sampled review of this audit (SCI-REV-0022), and what was done

| tag | sampled | stand | do not stand |
|---|---|---|---|
| F, false when removed | 10 | 8 — real counterexamples (two rebuilt with independent code, five more by the reviewer's own argument or computation) | 1 refutes a lemma of the proof, not the theorem; 1 shows vacuity, not falsity |
| P, needed only by the present proof | 12 | 6 | **2 are false when removed; 4 are "not known"** by a second tag on the same bullet |
| Q, replaceable by a weaker quantitative condition | 6 | 4 (one only after the reviewer stated and proved the condition) | 1 states no condition; 1 rests on a sketch quoted without its caveat |
| ?, not known | 4 | 3 | 1 is decided in part by our own report |

(Small samples: the reviewer's 95 per cent intervals for "stand" are 44–97, 21–79, 22–96 and
19–99 per cent.)  **The rule a reader can use, which matches our own reading of the two
reports:** an F of this audit can be trusted as "a counterexample exists"; a P is reliable
where the entry names the *other* theorem or proof that gives the statement without the
assumption — every such P in the sample stands — and where it names only the proof step,
read "not known".  Neither of the two false P and none of the four others had a proof or
a check behind it.  The three new counterexamples of §6 that the reviewer rebuilt are
correct; all five sampled citations of that division's reviews report them correctly.

*The two P that are false when removed* (both theorems are stated with the hypothesis, so
neither theorem is wrong — the audit's classification was):

* **Theorem 11.32, "the true residual is additive"** (AA1 entry E42): F, with a quantitative
  substitute — at a residual with second differences up to `κc`, `κ < 1`, the covering
  sandwich holds with the constants `(1 ∓ κ)c`; at the boundary of the class three
  evaluations certify where the sandwich says four (`n = 2`).  Replicated by the coordinator
  with code of its own (`experiments/coordinator_checks/sci_rev_0022/f1_check.py`: the
  counterexample at `n = 2, 3`; the substitute in 18 of 18 random instances; the original
  lower bound violated in 7 of 12 instances with `κ ∈ {0.5, 0.9}`).  Now a remark after the
  theorem, and qualifications in row G14, §11.7 and the README.
* **Theorem 11.116(e), stationarity and homogeneity** (AA2 entry 73): F for the existence of
  the limit — couplings on blocks of lengths `2^{j²}`, alternately those of `p = 0.3` and none,
  give limit points at least `0.0346` and at most `0.0291` per site; what holds without
  homogeneity is the bracket block by block.  The argument was read and checked given
  parts (a), (b) of the theorem and one number of AA2's script S3; now a remark in (e).

*The other corrections* (tags changed in place in the two reports, each marked there with
its old tag; listed in an appendix at the end of each report): AA1 — E15 and E25 `P ?` → `?`;
E14 `F` → `E` (the Lean example shows an empty class: without consistency the soundness
theorem is vacuously true, not false); E31 `Q` → `C`, `X` (no quantitative condition was
stated); E48: the weaker condition is now stated (the reviewer's droplet criterion with
site-dependent constants, proved in its report); E37: Harper's theorem marked as an
ingredient.  AA2 — entry 40 (`βJ ≥ 0` in Proposition 11.81(c)) and entry 56 (extensive
accuracy in Theorem 11.101) `P` → `?`; entry 15: the abort test before every query `F` → `Q`
(without it the proved bound is `C_max + M̄`; no violating run is known — that division's
SCI-REV-0016) and the binomial median marked as an ingredient; entry 11: the script
refutes fact (F2) of the proof, the failing certificate is workstream N's Proposition
N12, and the conclusion of the theorem without a product measure is "not known" (entry
13); entry 64 (exact oracle): `?` with a field, `Q` on the uniform cube with that division's
Theorem 4-τ; entry 13 and §§A.2, A.3: the sentence on interacting known parts (below);
entry 17 now cites SCI-REV-0017; entry 36 now names that division's bounded-accuracy bound
for product landscapes with site types (its Proposition A1.2; unrefereed here).

*An over-statement of ignorance* (finding F4).  "Whether 'adaptive = hinted' holds for any
interacting known part is open" contradicted our own Proposition 11.81(c): for the
Curie–Weiss known part without field at `0 ≤ βJ ≤ 1` the adaptive exponent without a hint is
determined and equals the hinted one, `R_H = R_unif` ([P]; part (c) is the workstream's
sketch with the referee's completion, checked by the coordinator and not refereed in
turn).  It is open in general; "adaptive = hinted" is not a property of product measures
alone.  Corrected in §2 (Level 3), §3(b) and §8 item 2.

*Not done.*  The other 481 tags are unreviewed.  Of the reviewer's coverage list, the
following were audited by nobody as statements: §§7–9 and 12 of the theory report;
nineteen rows of §10 by row (G18, G20–G22, G24, G26, G27, G29–G40); the Scientific
Discovery Division's Conjecture R10.3; and everything added to the report after the
audits (Theorems 11.53a, 11.53b, Lemma 11.58b – Theorem 11.58e — classified by the coordinator
alone in §6a —, §11.33, the remarks after
Theorems 11.32, 11.33 and in 11.116(e)).  Of its three questions (a product reference in
the adaptive upper bounds — the antiferromagnetic Curie–Weiss known part; a two-sided
tail estimate for the `p`-biased cube; site types growing with `n` and chains without
homogeneity) the third is taken up in part (the remark in Theorem 11.116(e)); the other
two are, in our judgement too, the right questions, and are in §8.

## 2. The hierarchy, from the most tractable model outwards

Each level names what holds there, with its label in the theory report — `[V]`
machine-checked, `[P]` paper proof, `[N]` numerical — and what is lost on the way to the
next.  Evidence in brackets: D-numbers are entries of `docs/DEAD_ENDS.md`; S-numbers are
scripts of the two audits (AA1: S1–S7; AA2: S1–S8).

```
LEVEL 0  THE UNIFORM CUBE, one slope, no known part, exact evaluations, worst case over the class
         complete at the exponential scale:
           fixed samples: exponent θ_na; plain Monte Carlo optimal            11.44 [P], 11.45 [V core]
           adaptive without a hint = hinted: θ_hint (extensive accuracy) 11.54; h (bounded) 11.58  [P]
           n·h − O(1) ≤ ln N ≤ n·h + O(n^(1/3) (ln n)^(2/3))                  11.58a(c), 11.58e [P]
           at an accuracy g·n:  ln N ≤ n·θ_hint(g) + O((ln n)²)               11.58e(g) [P]
           rounds of adaptivity; k-body marginal oracle changes no exponent   11.84–11.87, 11.104 [P]
           k nested levels: exponent h + (2π²h²θ_hint″(0) + o(1))/k²          Theorem 11.53b [P, refereed internally]
           certified upper bounds for that exponent at every k               11.58e(f) [P + interval arithmetic]
         the only level with an exact tail function (Harper) and a bounded-accuracy adaptive theorem
    |
    |  lost: exact isoperimetry (AA2 S1), every bounded-accuracy adaptive bound, the sub-exponential
    |        term, "the zero residual is the hardest instance"
    v
LEVEL 1  A FIELD (p-biased product measure), two letters                      11.59–11.65 [P]
         single-letter exponents; the right sample is flat in the type; isoperimetry only
         asymptotically (error 2·n^(−1/8))
    |
    |  lost from three letters on: "a field always helps", concavity of the site function,
    |        "the uniform site law is hardest"
    v
LEVEL 2  FINITELY MANY FIXED SITE TYPES, any finite alphabets, asymmetric site envelopes,
         single-site (product) known part                                      11.95–11.103 [P, by transfer]
         one-shot product bounds for ARBITRARY site types at every n            11.7, 11.8 [V]
         exponents as Rényi capacities; one common slope; exponents of types do not add
    |
    |  lost: the product measure — hence the independence of blocks on which every nested
    |        algorithm rests (AA2 S8), and the Σc_i² width of the sandwich (AA1 S2)
    v
LEVEL 3  EXCHANGEABLE KNOWN PARTS (functions of the type: mean-field)          11.76–11.82
         every-n statements by symmetry (stratified sample optimal up to a polynomial factor);
         single-letter hinted exponent for a convex rate function; not harder than the cube for
         two of three exponents (two letters); adaptive exponent: determined (= hinted = the cube's)
         for the ferromagnetic Curie–Weiss part without field, 0 ≤ βJ ≤ 1 (11.81(c) [P]), OPEN
         otherwise (antiferromagnets: nothing); two phases: searched values
    |
    |  lost: symmetry — hence the stratified sample, every unconditional upper bound, every
    |        formula; "ferromagnets are not harder than the cube" becomes false (AA2 S3)
    v
LEVEL 4  A NEAREST-NEIGHBOUR CHAIN AS KNOWN PART (one synthetic two-state model)  11.39–11.42, 11.116–11.117
         lower bounds for every algorithm at every n [V core]; exponents in numerical brackets;
         every upper bound conditional; no transfer-matrix formula (it is zero on a window: 11.41)
    |
    v
LEVEL 5  NO STRUCTURE: any set, any reference measure, any envelope
         the exact characterisations of §§2–6 and §§11.1–11.6, 11.12–11.14, 11.22–11.24, 11.26, 11.29 [V];
         lower bounds 11.43(a), 11.45(a), 11.62, 11.116(c); the abstract nesting theorem (validity
         on any probability space, given tail functions: theory report Theorem 11.118 [P, refereed internally])
         NOT available: any upper bound, without a hint, on the cost of any algorithm for a
         first-order class other than enumeration (with the instance as a hint: 11.22–11.26)
```

Side ladders, each with its own assumptions (none implied by a first-order envelope):

* **Other classes of ignorance.**  Linear in known features: rank-many evaluations
  (11.47 `[V]`, general) → a Hilbert ball: the spectrum (11.50a `[V]`) → second order with one
  reference, a product domain and weak coupling: a star of evaluations (11.16–11.18f) →
  dense second-order constants: a quadratic law, cost `2^{n − o(n)}`, at true residuals
  strictly inside the class in second order (11.31–11.32 with the remark after 11.32) → a box
  around a sampleable known part with a certified floor: the Boltzmann factor of one
  free-energy distance, *with the instance as a hint* (11.110).
* **Continuous variables.**  Voxel enclosures (product measure, pairwise energy; cost
  growing like `d^{d/2}` in the dimension `d` of a voxel) → the torus with zero known part
  (11.34) → Gauss space: with the *sum* metric an exact instance of the nesting theory,
  with the Euclidean metric an obstruction (§3, axis d).
* **Chain geometry.**  Torsion moves → RMSD → bounded-difference constants (4.6, 4.7 `[V]`)
  → constants that grow along the chain on every domain (11.36; AA1 S6) → the
  weighted-Hamming format is empty for long chains (11.37) → pair-distance profiles
  (11.48–11.49) → limit shapes for lattice bridges at the zero residual (11.69–11.71) →
  off-lattice: nothing.

## 3. The directive's axes of generalisation, one by one

For each: what is proved, what additional structure it needs, where an obstruction is
proved, and the computational reading.

**(a) Heterogeneous chains and non-uniform parameters.**
*Holds:* one-shot lower bounds and product bounds for arbitrary site types at every `n`
(`[V]`); all three exponents for finitely many fixed types, any alphabets, asymmetric
envelopes (§11.26, `[P]` by transfer; nothing at finite size, nothing simulated); a
continuum of slopes through `J = ∫ J_u dν` and, for the nested algorithm, the facts that no
split of the sites undercuts the hinted exponent and that the best outer block is *not*
proportional (it prefers steep sites; workstream N §3.2, numerical).
*Needs:* a fixed finite set of types as `n` grows; the combination of types is through a
common slope, not a common accuracy.
*Obstructions:* with one type per site the every-`n` optimality statement of the stratified
sample is empty (its polynomial factor is exponential; AA2 S7); with margins that shrink
like `1/n` "one evaluation or exponentially many" fails — every site non-sharp and the
covering number is `n + 1` exactly (AA1 S3); the exact tail lemma fails for site-dependent
slopes (weighted balls are not extremal; AA2 S1); from three letters on three comparison
statements fail (D-entries cited in AA2).
*Computational reading:* the polynomial factors of Theorems 11.76(a), 11.95 exceed the cost
they multiply for `n ≤ 50` on the cube and up to `n = 300` for twenty site types.

**(b) Correlated, dependent and strongly interacting variables.**
*Holds:* lower bounds for every algorithm with any known part (machine-checked cores);
mean-field known parts by symmetry (Level 3); a nearest-neighbour chain in brackets
(Level 4); the sandwich with a mixture of `K` product references at the same width with
`K` averages (new in AA1, S2(D)); the nested algorithm under a *class-relative bounded
influence* `ι` between blocks — dependence then costs slope, `u → u + ι` (workstream N,
Theorem N4).
*Needs:* a product reference or a bounded influence; symmetry with few orbits for every
every-`n` statement about fixed samples; an additive known part in Theorem 11.33(a).
*Obstructions:* the `Σc_i²` width of the sandwich fails for every correlation `ρ > 0`, not
only for perfect correlation (AA1 S2); additivity of the extremal residual fails for
dependent references (D25, D41); with interactions the fibre averages of a class member
change by `u(1 + c)` per outer flip, `c` up to 26 with two phases (AA2 S8), so the nested
algorithm's key fact is lost; with *unbounded* influence the nested algorithm returns a
**false certificate** (workstream N, Proposition N12: 80 of 80 runs; 120 of 120 in the
referee's reproduction) — the validity hypothesis that a dependent known part breaks
(the lower tail function, the a-priori bounds, the inner brackets and the sampling law
are validity hypotheses too);
"ferromagnets are never harder than the cube" is false for the nearest-neighbour
ferromagnet (`0.0346` against `0.0291` per site at `u = 1`; AA2 S3); Theorem 11.33(a) is false
for a pairwise known part of ferromagnetic blocks (§7).
*Open:* the adaptive exponent without a hint for interacting known parts in general — it
is determined for one family, the ferromagnetic Curie–Weiss part without field at
`0 ≤ βJ ≤ 1`, a positive mixture of field-tilted product measures (Proposition 11.81(c)); for
a known part that is not such a mixture (the antiferromagnetic Curie–Weiss part, where the
hinted exponent is the cube's) nothing is known.

**(c) Non-ideal and flexible geometry.**
*Holds:* the torsion-to-RMSD chain rule with inertia inputs (`[V]`); profile envelopes of
pair-additive residuals for any chain.
*Obstructions:* the verified first-order constants grow along the chain — at least like
`m^{3/2}` for extended arms, and at least like `m^{1/2}` on every domain because the inertia
of any arm of `m` bonds is at least `0.0267·m·b²` (new in AA1, S6) — which empties the
weighted-Hamming format (11.37; for the zero residual, an additive known part, a product
domain).
*Open:* excluded volume and flexible bond geometry in that no-go statement; everything
off-lattice in the limit-shape theory.

**(d) Continuous and hybrid spaces.**
*Holds:* voxel enclosures (`[V]`); the torus with zero known part; **Gauss space with the
sum metric** is an exact instance of the nesting theory at every dimension (exact tail
functions; the pair of exponent functions is the "Gaussian pair" of the rate theorem);
on Euclidean Gauss space the tail functions are exact and dimension-free, and the hinted
lower bound holds in high dimension with ball-shaped perturbations (workstream N,
Theorem N9, Proposition N11).
*Obstruction:* for Euclidean-Lipschitz functions on Gauss space, nesting over a fixed
split of the coordinates **gains nothing** — the level operator is the identity, and
every run of the algorithm draws at least `exp((L − √(2x))²/2)` outer points at a linear
instance (Proposition N10).  The dividing line is whether the envelope is additive over
independent parts, not whether the space is discrete.
*Open:* a known part on a continuous space; hybrid (basin, angle) sites; the adaptive
exponent on Euclidean Gauss space (between the hinted and the non-adaptive one); blocks
that are random subspaces.

**(e) Multimodal landscapes.**
*Holds:* mixtures of product references (above); barrier certificates (§11.31); box
classes around a sampleable known part.
*Obstructions:* with two phases the single-letter theory needs a convex rate function and
fails without it; the extremal perturbations are no longer cones; every two-phase
exponent in the report is a searched lower bound.

**(f) Long-range, many-body and non-decomposable interactions.**
*Holds:* second-order (and order-`m`) classes with one reference on a product domain under
weak coupling; linear classes; marginal oracles of order `k = o(n/ln n)` change no exponent.
*Obstructions:* dense second-order constants (the quadratic law, machine-checked
droplet); domains with exclusions, where the second-order class may contain every
function (11.18c); stars at several references do not combine (11.31(b)); a known part
that confines the ensemble to a code makes every bounded-accuracy algorithm exponential
at every coupling (AA1 S4).
*Open:* known parts with long-range or many-body interactions other than mean-field ones.

**(g), (j) High dimension and large systems: the accuracy scale.**
Every "bounded number of evaluations" statement (11.21, 11.25(b), 11.28, 11.34) is at an
*extensive* accuracy — `0.11` to `0.16` nats per site in the report's examples; every
exponent needs an accuracy that is `o(n)` and not exponentially small.  At a fixed
accuracy for a growing system the cost on a first-order class is exponential for every
algorithm (`n·h − O(1)` on the cube); what is polynomial there belongs to other classes
(linear; weakly coupled second order with an additive known part; a box with a small
free-energy distance to its floor).  Below Level 0 every upper bound is asymptotic with
proved error terms: for a field the term `2·n^{−1/8}` falls below the exponent itself only
from `n ≈ 4.9·10¹⁴` on at `u = 1` (exponent `0.0291`; from `10¹¹` on at `u = 2`, exponent `0.0839`),
and for two, three and four letters the term `q·n^{−1/(2q+2)}` falls below the fixed number
`0.05` only from `4·10⁹`, `1.7·10¹⁴`, `10¹⁹` on (AA2 S4, block H — two different criteria, which an
earlier version of this sentence ran together).

**(h) Ensembles not concentrated near one reference; (i) no symmetry, exchangeability,
homogeneity or product structure.**
What survives with no structure is Level 5: exact characterisations of certificates,
one-shot lower bounds, and the validity (not the cost) of the nested algorithm given
tail functions.  Costs at an instance are *verification* costs of an algorithm that is
handed the instance as a hint (without it `1/ε` becomes `e^w/ε²` in a box class); no single
algorithm attains the instance-wise costs (the hub family, D26, D37).
*A quantitative instance from another division* (Scientific Discovery Division,
SCI-RES-0031 §1 at its commit `32bcd7f`; its label [M], exact transfer-matrix values; not
recomputed here): a floor built around one reference state certifies `ln Z` up to a sharp
transition in the size `λ` of its penalty tables — below a critical size the floor's
ensemble is the reference state and first order is accurate, above it the chain is
displaced as a whole; the critical sizes are `15.3, 18.8, 1.32, 0.198` in its four cases
(the certificate is `λ = 1`), so
its order-4 floors are a factor 15–19 inside their own transition and one order-3 floor
is beyond it.  The position is, to first approximation, the least ratio of the cost of
a state to its penalty — an extremal quantity, which criteria built from means under
the reference bound from one side only.

## 4. The assumptions that matter most outside the models

1. **The class of ignorance itself** — the full first-order class, nothing more known (E for
   every lower bound; X when changed).  The exponential price is the price of this class.
2. **Independent sites / a product reference measure** (E, F, X): every exponent and
   threshold of §§11.4–11.10; every adaptive upper bound; the sandwich width.
3. **Additivity of the envelope over independent parts** (the sum metric): cost-only in the
   proof of the nested algorithm and yet the whole gain (workstream N, row 7).
4. **Bounded influence between blocks**, with a certified bound: among the validity
   hypotheses of the level theorem, the one that a dependent known part breaks — its
   failure yields false certificates, not a higher cost.
5. **The accuracy scale** (E, F): extensive for every bounded-cost statement.
6. **A hint, free computation, exact samples and certified a-priori constants** (X, E): the
   theorems count evaluations; slopes, floors, variances and per-pair constants are inputs
   that nothing in the repository certifies for a concrete residual (one paper
   certificate of another division excepted — and what that certificate is has since
   been stated by that division's own referee, SCI-MSG-0030 §4: constants bounded by a
   paper proof, arithmetic in double precision with stated margins, the evaluation
   tolerance assumed, one implementation).
7. **Symmetry with few orbits** for every every-`n` statement about fixed samples.
8. **Two letters** in the comparison theorems; **a function of the type** in "ferromagnets
   are not harder"; **one phase** in the single-letter formulas.
9. **Site types fixed as `n` grows and a margin bounded away from zero** for "one evaluation
   or exponentially many"; the exponent of a two-state site vanishes linearly in the
   margin (about `0.28·(c/e − 1)`).
10. **Smoothness and strict convexity of the non-adaptive exponent at its fixed point** for
    the `1/k²` law of nested levels: with a kink the rate is `1/k`, and the general `O(1/k)`
    bound is then sharp (`docs/workstreams/R_REPORT.md`, Proposition K).

## 5. General statements whose guarantees are computationally vacuous

The directive asks that these be named.

| statement | why it is vacuous as a cost guarantee | where |
|---|---|---|
| Theorem 11.33(a): polynomially many evaluations for `w ≤ 4` | about `n⁵ε⁻²`: `10¹⁰/ε²` at `n = 100`; above `2ⁿ` up to `n ≈ 22`–`40` | AA1, entry E43 |
| Theorem 11.33(b): exponential for `w > 4` | asymptotic at fixed `w`: at `w = 5` the bound is `e^{3.9}` for `n = 2000` | theory report, scope note of the theorem |
| the any-reference width `(Σc_i)²` of the sandwich | vacuous once `βΣc_i > 8` | AA1, hierarchy L1 |
| optimality "up to a polynomial factor" of stratified samples (11.76(a), 11.95) | the factor exceeds the cost for `n ≤ 50` (cube), `n ≤ 300` (twenty types); empty with one type per site | AA2 S7 |
| asymptotic isoperimetry behind Levels 1–2 | error terms `2n^{−1/8}`, `q·n^{−1/(2q+2)}`: below the exponent from `n ≈ 10¹¹` (`u = 2`) to `5·10¹⁴` (`u = 1`) on for a field; below `0.05` from `4·10⁹` on for two letters | AA2 S4 |
| cost bounds for profile certificates (11.49) | vacuous at extensive accuracy | AA2, overstatement 24 |
| voxel enclosures in dimension `d` | cost grows like `d^{d/2}` | AA1, hierarchy L5 |
| the abstract nesting theorem with a tail function that is valid but not sharp | ball-volume bound: exponent `0.197` for `0.029`; transport bound: the certified cap on the sample is `10^{14}`–`10^{24}` on the cubes of dimension 30 and 60 (runs may close much earlier, but below the threshold rate `u²/8` they do not close before the atom) | workstream N §4(e), corrected by its referee |
| the nested adaptive algorithm at bounded accuracy (11.56, 11.58, 11.58a) | the `O(√(n ln n))` term has explicit but large constants; the sizes at which a certified separation from plain Monte Carlo is reported are those of §11.19, remarks (1a), (1b); the schedule of Theorem 11.58a itself costs more than the non-adaptive bound `n·a` up to `n ≈ 2·10⁴` at `u = 1` (our referee R12: `2.1·10⁴`; the science division's SCI-REV-0017: `2.04·10⁴`) | theory report §11.19 |
| the rate theorem for `k` nested levels | asymptotic in `k`; exact lower bounds exist for the Gaussian pair; since Theorem 11.58e(f) there are certified *upper* bounds for the cube at every `k` computed (given two paper statements), which from `k = 3` on are not the exponents themselves | `docs/workstreams/R_REPORT.md` §12; theory report Theorem 11.58e |

## 6. New counterexamples and new positive facts found by the audits

Scripted, stored and re-run by the coordinator where a script is named; the positive
facts of the last bullet and the `n + 3` contradiction are arguments in the entries.  The
first, third and fourth were rebuilt by the Scientific Discovery Division with code of
its own before it opened ours (SCI-REV-0022 §1): correct.

* Every site non-sharp and yet `n + 1` evaluations suffice (two-state sites with margin
  below `1/n`; exhaustive for `n ≤ 12`, with a proof; that division's proof gives the exact
  condition for identical sites, a margin of at most `1/(n − 1)`) — AA1 S3.  It is a
  counterexample to the summary sentence "one evaluation or exponentially many", not to
  Theorem 11.9, whose hypothesis is finitely many site types fixed as `n` grows.
* The product width of the sandwich is violated for every correlation `ρ > 0`
  (two-site and `n`-site Markov references) — AA1 S2.
* Theorem 11.33(a) without an additive known part: a code landscape (an illustration:
  the extended Golay code, `n = 24`, `w = 4` — every algorithm with `ε < 10⁻³` makes
  `(1 − 2δ)·4096` evaluations, which at `n = 24` is still below the theorem's own polynomial
  `n⁵ε⁻²`; the refutation is the family — Gilbert–Varshamov codes: exponential at every
  `w > 0`), and a
  *pairwise* known part of ferromagnetic blocks (`exp(Θ(n^{1/3}))` at `w = 4`) — AA1 S4.
* With a `p`-biased measure Hamming balls are not extremal for the tail functional
  (ratio up to `2.08` on the 4-cube, all 65 534 subsets); with site-dependent slopes
  weighted balls are not extremal for 17 of 20 slope vectors — AA2 S1.
* The ratio duality of Theorem 11.105 overestimates without the triangle inequality
  (`10` against `2` on three states) and is exact after the shortest-path closure — AA2 S2.
* Degenerate regimes: for a failure probability close to one a single evaluation is
  correct on the whole class; a marginal oracle of order `k = n` gives the answer with one
  evaluation — AA2 S6.
* A class-correct procedure that costs `n + 3` on every cone (Theorem 11.45(d) of the
  report itself) contradicts the sentence "no procedure that is correct on a first-order
  class can be cheap on any of its subclasses" — AA1, AA2.
* Positive: a `K`-component sandwich for mixture references; the inertia bound
  `≥ 0.0267·m·b²` for any arm; a coNP-hardness reduction for dominance on domains with
  exclusions (AA1); the hypothesis (E) of the abstract limit theorem behind Theorem 11.69
  is redundant; a `K`-level lower bound valid for every failure probability below one
  (AA2).  These are recorded in the audit reports with their arguments and have **not**
  been refereed or integrated into the theory report.

## 6a. Added after the audits: the finite-`n` bounds of Lemma 11.58b – Theorem 11.58e

*The coordinator's classification (2026-11-26), in the same categories; not made by the
independent readers of the two audits, and subject to the lesson of §1a: every P below
names the statement or check that supports it.  Evidence in brackets.*

| statement | assumption | category | evidence |
|---|---|---|---|
| Lemma 11.58b (one level over a maximum of lines) | slopes in `[0, 1]` | F | with a slope above one the inequality fails; such a line has to be cut to slope one first (workstream Q2 §6.2, its referee §1.4) |
| | one line nonnegative at the dominant rung (a flat line, or a finite range) | F | negative control: violations up to `8 551` nats (Q2 referee); harness XVI.9(c) |
| | a common finite range of the lines | P | the same proof without it (Q2 referee, finding 1; confirmed by the referee of `Z_REPORT.md`): what is used is "nonincreasing with slope at least `−1`" |
| | the exact tail function of the uniform cube (Lemma 11.55(d)) | Q | used only as `ln(1/π†) ≤ n_o·θ_na(e) + O(ln n)`: a tail function sharp up to polynomial factors at every block size; known for the uniform cube only (§11.33; Level 0 of §2) |
| | the threshold `3(n_o + 1)e^{2u + e^u + n_oe}`, the ladder of step one, `λ = 1`, `η = ½` | C | constants of one proof; `ℓ₀` is attained up to a few nats (harness XVI.9: `0.26`) |
| Proposition 11.58c(b) (the chain) | a block with `m·B′ ≥ 𝒳 + P̄_cnt + ln 4` | F for "once" | with half the block every level adds the deficit (harness XVI.9(e): `57`–`73` nats over four to six levels) |
| | one tolerance parameter along the chain | C | the workstream's remark 5 |
| | a flat type of the family served at the coarse rung | ? | the chain is used on the flat majorant of a family with slopes (Theorem 11.58e(c)); whether a chain that uses the slopes loses less is not known |
| Theorem 11.58d | the epochs of the `O(1/k)` proof (one line per epoch) | P | replaced by convex families in Theorem 11.58e, with a better order |
| Theorem 11.58e (a)–(d) | **convexity of the family of lines** | F | for a non-convex family the line-by-line value is not a bound (`DEAD_ENDS.md` D64; harness XVI.7; the referee's controls) |
| | slopes capped at one | E for the accounting; C at the next level's zero accuracy | the shift of the accuracy by `X₀ ≈ ln n` costs `X₀` only because slopes are at most one; at vanishing accuracy the next level does not see steeper slopes (part (e): the slope-capped hull) |
| | the inner tolerance zero in the step | X for the exponents of finite depth | the recursion itself uses a positive tolerance and is strictly better from the third level on (`0.3612·a` against `0.3633·a`); same limit constant |
| | a chain after every level | C | a chain every `r` levels gives a smaller constant (the report's remark 3); without any chain the loss is `½k²·ln n` and the order is back to `√(n ln n)` (F for "no chain at all") |
| | `W₀ ≡ 0` and a flat base | E | the referee's repair of Lemma A1 |
| Theorem 11.58e (e) | (H1): the dual function has a twice differentiable maximum | X | with a kink at the fixed point the tops decrease like `1/k` (Theorem 11.53a(e)) and this method gives `O(√(n ln n))` again |
| | infinite slope of `θ_na` at zero | C | used for the description of the tops as "where the image becomes infinite"; for a finite slope the next top is `max_B min(B, (1 − W(B))a)` (the referee: by hand only) |
| | a restart near the fixed point; a range condition | P | the envelope sequence needs neither (Proposition A5 of the addendum, refereed) |
| Theorem 11.58e (f) | parts (a), (e) | E | the certified numbers are rigorous *given* those paper statements; the arithmetic is interval and exact |
| Theorem 11.58e (g) | `θ_na(e) → 0`; `J` differentiable below its maximiser | P | differentiability only names a subgradient — any supergradient does (the referee, §2.8) |
| | a fixed rate `g` | ? | the constant of the proof is of order `1/g²`; a statement uniform in `g`, or at accuracies between bounded and extensive, is not proved (numerically the defect is largest at accuracy zero for `k ≤ 60`) |
| all of 11.58b–e | the uniform cube, independent blocks | Q / E | as for Lemma 11.58b; with dependence see §11.33 (a certified class-relative influence, or a false certificate) |
| | free computation | X (not counted) | the design computes the curves and one minimisation per level |
| | effectiveness | — | `n₀`, `C′` and the rate at which the tops approach `h` are not produced by the proofs |

**Computationally:** the bound of Theorem 11.58e is, as a formula at `u = 1`, above the
non-adaptive cost at `n = 10⁴` and below every earlier bound from `n ≈ 3·10⁴` on; it describes
`k` nested levels and `k` chains of `≈ n/ln n` levels each, in a regime of the level theorem
that no simulation covers.  Evaluated exactly (certified costs, no run): two levels over
the real base at `n = 50 000` cost `e^{2818}` against `e^{5547}` non-adaptive.

## 7. Errors and overstatements found, and what was done

* **One error of substance.**  Theorem 11.33(a) (polynomially many evaluations for
  second-order classes below the Curie–Weiss coupling) was stated without the hypothesis
  of its source, "the known part is additive"; without it the statement is false (the
  counterexamples above).  The hypothesis was lost when the workstream's theorem was
  adopted — the failure mode recorded once before (D62).  Verified by the coordinator
  against the source and by re-running the audit's script; corrected.
* **Stale sentences** (seven in AA1, one in AA2): passages that an earlier or later section
  of the same report contradicts (a question called open that is answered twelve lines
  later; "under review" for a review that is reported; a statement that an operator is
  not in Lean when it is).  **Two numbers** of Theorem 11.38 quoted from a sharper formula
  than the one displayed.  **Status cells** of §0.3 that claimed more refereeing than the
  referees' scopes.
* **Overstatements:** 22 in AA1 (8 false as written, 10 with a hypothesis omitted in a
  summary, 4 of wording) and 25 in AA2 (5 major, 11 moderate, 9 mild).  Almost all are in
  the summaries (§0.3, §7, §10 of the report, and the README), almost none in the theorems.
  The worst: the sentence on subclasses quoted in §6; the unqualified dichotomy "one
  evaluation iff every site is sharp, otherwise exponential"; "a ferromagnetic interaction
  never makes the problem harder" (mean-field only); "the cost of certifying a free
  energy in a box class" (with a hint).
* No machine-checked statement was found false; 264 quoted numbers were recomputed from
  the printed formulas by the two audits and agree (apart from the two of Theorem 11.38);
  the 405 Lean names cited in the first part exist.
* Every item, with the old and the new sentence and the justification, is in
  `docs/audit/APPLIED_CORRECTIONS.md`.

## 8. What could not be classified — ranked by what hangs on it

1. **Exponents and thresholds at non-additive instances.**  Every single-letter result is
   at an additive (usually the zero) residual of a homogeneous system; only the one-shot
   bounds are general.  Everything the theory would say about a real residual hangs on
   this.  (Closed in part by sandwiches at interior instances: a residual that is
   `κ`-Lipschitz for the envelope leaves the envelope `(1 − κ)d` — machine-checked,
   `slack_ge_of_lipschitz` — and a residual with second differences up to `κc` leaves the
   second-order theory with the constants `(1 ∓ κ)c` — SCI-REV-0022, the remark after Theorem
   11.32.  The exponents then hold with changed constants; at the boundary of a class they
   fail.)
2. **The adaptive exponent without a hint for interacting known parts beyond one family** —
   it equals the hinted exponent for the ferromagnetic Curie–Weiss part without field at
   `0 ≤ βJ ≤ 1` (Proposition 11.81(c)), which is a positive mixture of product measures;
   whether "adaptive = hinted" holds for a known part with no product structure in any
   disguise is open.  *The smallest question* (the Scientific Discovery Division's,
   SCI-REV-0022 §5): the antiferromagnetic Curie–Weiss part without field, where the hinted
   exponent is the cube's — is there an adaptive algorithm without a hint at that
   exponent?  A first computation: the class-relative influence between an outer block and
   the rest as a function of the split, and whether it vanishes as the block shrinks
   (with Theorem 11.119 a bounded influence gives a valid nested algorithm at a larger
   slope; the question is whether that loss is real).
3. **A bounded-accuracy adaptive upper bound beyond the uniform cube** — it needs a
   two-sided tail estimate with polynomial precision, known for the uniform cube and
   Gauss space only (workstream N, rows 8–9).  *The smallest question* (same source): for
   the `p`-biased cube, a comparison `Ξ_H(q) ≤ θ·n^C·Θ_H(cq)` of the upper tail functional of
   Lemma 11.62 with its lower counterpart — the analogue of Lemma 11.55(b), (c); a first
   computation: both functionals over all subsets of the 4-cube.
4. **A lower bound for adaptive algorithms above the hinted one** — between `n·h + ½ ln n`
   (numerically) and the upper bound, which since this file was first written has gone
   from `n·h + O(√(n ln n))` to `n·h + O(n^{1/3}(ln n)^{2/3})` (Theorem 11.58e, §6a).  That analyses
   of nested algorithms through types cannot go below `n·h + Ω(n^{1/3})` is a heuristic, not
   a theorem (the referee of `Z_REPORT.md`, finding F4); whether any algorithm can is open.
5. **The class threshold and finite-temperature exponents with an interacting known
   part**; the exponents of Level 4 as costs.
6. **Upper bounds for genuinely heterogeneous sites** (a number of types growing with `n`).
7. **A known part on a continuous space; hybrid sites; Euclidean Gauss space.**
8. **Noisy evaluations and average-case correctness** — bounded errors give accuracy
   floors by a one-line argument; variance is not treated anywhere.
9. **Lower bounds for certificates that use the decomposition rules** ("the rules are
   needed" is proved; "they are enough" is not formulated).
10. Smaller ones, listed in the two reports (AA1 §6 items 6–10; AA2 §A.3 items 7–14).

## 9. How to use this file

A reader who wants to apply a theorem should (i) find its entry in the audit report that
covers its section and read the assumptions marked E and F; (ii) locate the model on the
ladder of §2 — if it is below Level 2, the statement is an exponent with asymptotic error
terms, at an extensive accuracy, at an additive instance; (iii) check §5 before reading a
"polynomial" or "optimal" as a cost.  A successor who wants to extend the theory should
start from §8, items 1–4, and from the two structural facts that the audits isolated:
additivity of the envelope over independent parts is what nesting exploits, and bounded
influence is what its validity needs.
