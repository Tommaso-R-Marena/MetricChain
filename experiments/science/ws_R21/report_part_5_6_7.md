## 5. What the statements mean for measured data (Item 4)

*What Part II is.*  An exact, generic, point-conformer identifiability statement on the free configuration
space: `K` unknown frameworks and their populations are determined by `|E|` exact atomic laws.  *What it is not*:
a statement about anything known up to an error, about conformers with a width, about conformers that share a
rigid part, or about means.  Item by item (labels: [P] proved here or by them, [N] my numbers, [H] my reading):

1. **Laws versus moments versus means of nonlinear functions.**  E7 needs the whole law of every edge length,
   exactly; E8 needs the `2K` exact moments `E ℓ_e², …, E ℓ_e^{4K}` of every edge.  A *single* mean per edge of a
   function of the distance — the kind of number most averaged measurements deliver — is outside both.  On the
   free space such data identify no ensemble whenever all the functions are homogeneous of one degree `α` (the
   scaling argument of E1.3 with `E[R^α] = 1`; `α = −6` checked, T6(b)) **[P]**.  Through per-edge certificates,
   `K` conformers need a non-negative function with `K` double zeros in the span of the functions measured on each
   edge, hence at least `2K` independent functions per edge **[H]**.  A reader may *not* conclude that mean
   squared distances are useless for chains (M1): with fixed bond lengths they identify single conformations and,
   numerically, generic pairs once there are at least seven bonds in the plane (T6(d)).
2. **Exact laws versus laws with a band.**  Proposition B: the conclusion survives a band `τ` on every law when
   `τ` is below the chimera gap, and fails when a colouring and its complement are realised within `τ` (in
   between it depends on whether some switching component is realised within the band).  Measured gaps (T5,
   units: mean squared edge length = 4): see the table in §3.  A band of a few per cent of a distance is below the
   gap only for strongly over-determined graphs and very few conformers; as a rule of thumb **[H]**, with a
   relative band `τ` one needs `c ≳ |E| ln K / ln(1/τ)`, i.e. a number of measured pairs exceeding the degrees of
   freedom `dN − d(d+1)/2` by the factor `1/(1 − ln K / ln(1/τ))`, and nothing helps once `K τ ≳ 1`.  Already for
   one conformation a random framework on a minimally globally rigid graph can have a *near-flip*: in one of
   three random wheels a visibly different framework reproduces all eight squared lengths to `7.7·10⁻⁵` (T4b).
3. **One law per edge, measured on separate samples.**  This is exactly the model of E7 (marginals, no joint
   information), and the right one for pair-by-pair labelling.  What it hides: each sample carries its own labels,
   so the measured distance is between label positions with their own distribution — a conformer is then not a
   point in the space of measured lengths (item 4), and different edges are measured on chemically different
   molecules.
4. **Point conformers versus conformers that are distributions.**  Not covered; Proposition E8.1 is the
   statement in the other direction.  The mean distances of a basin are not the edge lengths of one
   configuration, so even the vocabulary (splice, chimera) presupposes width zero; with a width `σ` the relevant
   comparison is `σ` against the gap of item 2.  For moments the instability is quantified in §3 (T4): a spread
   `s` of a conformer changes the moments by `O(s²)`.
5. **Genericity versus conformers that share rigid domains.**  Mathematically the excluded tuples have measure
   zero.  Physically they are the rule for articulated chains: (i) every edge inside a rigid unit has the same
   length in all conformers — on the chain's configuration space these features are constant, i.e. loops of the
   matroid, which E5 excludes by hypothesis; (ii) conformers that differ by a few torsions share the lengths of
   all edges that do not span those torsions, so the tuple is non-generic for *every* graph containing such an
   edge; (iii) the conclusion then really can fail on a globally rigid graph (Example D2), and near such tuples
   the gap of item 2 is small.  For conformers that are the states of a few hinges the data are what one expects
   **[H]**: an edge spanning a set `S` of hinges has, generically, one atom per joint state of `S`, so its law is
   the marginal of the joint state distribution on `S` — the marginal problem of Part III — and a single edge
   spanning all hinges gives the whole joint distribution *if* its `2^{|S|}` atoms can be resolved.  So for such
   ensembles the question is which hinge sets are spanned and whether the atoms are resolvable; generic global
   rigidity of the graph is neither necessary nor sufficient.
6. **Genericity is a property of the unknown.**  It cannot be read off the data; but the data allow a finite
   a-posteriori test that replaces it (enumerate the splices of the observed atoms, test realisability and the
   uniqueness of the weights), at a cost exponential in `|E|`.
7. **Is anything stated more generally than the theorem?**  (a) The headline "ensemble rigidity = global
   rigidity" and the message's "every generic finite ensemble" omit *jointly*, *exact* and *point* (M2, M3).
   (b) "Mean squared distances determine nothing" (M1).  (c) §5 item 4 "is an ensemble theorem by Corollary E6"
   (m8).  (d) §5 item 2 "exactly the ensembles carried by the ground states" (m7).  (e) Lines 417–419 and 485–487
   (m2).  (f) §5 item 1 — "certificates produced for equilibrium problems are identification certificates; the gap
   […] is the stability constant" — is a statement about sharp minima on finite spaces; the certificate of Part II
   is not of that kind (M3(ii)), and the coordinator's note SCI-RES-0026 §2(c) already says why it cannot be on a
   manifold.

## 6. Novelty (Item 5): what I opened, what I did not

Reading levels.  **[tool]** = opened through a fetch tool that returns a model-written extraction of the page
(quotations in this report are as returned by that tool; I did not see the page itself); **[summary]** = search
result summary only; **[memory]** = not opened.

| statement | my class | basis |
|---|---|---|
| E1.3(a) | classical, trivial | — |
| E1.3(b) | elementary; correct on the free space; the general mechanism (affine images, conic at infinity) is the standard one of universal rigidity | Prop. A here; super stability / conic at infinity: Connelly; Gortler–Thurston arXiv 1001.0172; Connelly–Gortler–Theran arXiv 1605.07911 [summary] |
| E5(a) | elementary dimension count; a *formulation*.  The `K`-fold statement not found in print | their own proof; for two points it is the separator ⇔ product fact — Lemma 3.1 of Garamvölgyi–Gortler–Jordán [tool] in one direction; a search for the general statement about algebraic matroids of irreducible varieties returned no source |
| E5(b) | transfer of that Lemma 3.1 to polynomial maps, plus a local argument (as they say) | [tool] |
| E6 | elementary given E5(a) | — |
| E7 | **corollary** of Theorem 3.5 of Garamvölgyi–Gortler–Jordán 2022 (four lines); the reading — a finite mixture of frameworks identified from one law per edge — **not found** | [tool]: full text of that paper (Sections 4–5 included: nothing on several frameworks, pooled lengths or copies); Gortler–Theran–Thurston 2019 [tool, 100 of 112 k characters]: one configuration, unlabeled lengths, nothing on several |
| E8 | classical `2K`-moment certificate of a `K`-atomic measure applied per edge, plus E7; not found for frameworks | the per-edge fact is elementary (proof in one line); Lindsay 1989 / Gauss quadrature [summary via Wu–Yang arXiv 1807.07237, abstract page opened] |

Nearest neighbours found, and how they differ:
* **Unlabeled principal component analysis** (Yao–Peng–Tsakiris, arXiv 2101.09446 [tool]: Theorem 2 — a generic
  matrix of rank `r < min(m, n)` whose entries are permuted inside each column is the only matrix of rank `≤ r`
  compatible with the data, up to a row permutation).  Read with rows as points and columns as features, this is
  precisely "a generic *uniform* finite ensemble on an *unknown* generic linear subspace is determined by the
  multisets of its coordinates".  E6 is the version with a known variety, arbitrary weights and arbitrary
  competitor; neither contains the other (their ED4 says the same).
* **Unlabeled rigidity** (Boutin–Kemper [summary]; Gortler–Theran–Thurston [tool]; Garamvölgyi–Gortler–Jordán
  [tool]): one framework from an unlabeled set of lengths.  E7 is a *partially labelled* problem for `K` disjoint
  copies of `G` (each length labelled by its edge, not by its copy); the published theorems do not cover it
  (disjoint unions are not globally rigid), but the published proof of Theorem 3.5 uses the same device (M4).
* **Echo sorting / ghost rejection** (Dokmanić et al., PNAS 2013 [tool]; commentary [tool]): `K` unknown points,
  for each sensor the unlabeled set of distances to them; wrong combinations fail a distance-matrix rank test
  "with probability 1".  This is the no-chimera property for the feature map "distances to the sensors", with
  the genericity on the *sensors* and the points arbitrary — the opposite quantifier to E5(a), and the closest
  published statement in spirit that I found.
* **Joint conformational distributions from separately acquired distance distributions** (Hays–Boland–Kasson,
  arXiv 2010.15612 [tool]): the applied problem of E7; no uniqueness statement, the joint is supplied by
  simulation and a reference ensemble.
* **Sums of measurement maps and secant varieties** (Cruickshank–Mohammadi–Nixon–Tanigawa, arXiv 2305.18990
  [abstract page via tool]): the algebraic setting of Problem O5 and of the remark on `z ∈ (ℝ^{dK})^N` in M1.
* Not opened: turnpike/beltway surveys (Lemke–Skiena–Smith; arXiv 2402.03787) — one point set from pooled
  distances; heterogeneous multi-reference alignment (arXiv 1710.02590, 1707.00943) — mixtures from moments of
  invariants; discrete tomography (switching components); Rényi 1952 / Heppes 1956; Jackson–Jordán 2005.

Search log (2026-11-26; all queries generic; none contains a name, file or text of this programme):
(1) "Globally rigid graphs are fully reconstructible" Garamvölgyi Gortler Jordán arXiv; (2) Gortler Healy Thurston
"Characterizing generic global rigidity" arXiv generic frameworks globally rigid or none; (3) identifiability of a
mixture of point configurations from pairwise distance distributions rigidity theory; (4) unassigned distance
geometry problem multiple conformations mixture of structures unlabeled distances uniqueness; (5) multiple source
localization unlabeled distance measurements ghost sources uniqueness generic "data association" algebraic
rigidity; (6) echo sorting Euclidean distance matrix rank test unlabeled echoes "with probability 1" room shape
microphones theorem; (7) "unlabeled principal component analysis" Yao Peng Tsakiris theorem generic matrix
permuting entries each column rank unique up to row permutation; (8) conformational ensemble from DEER distance
distributions uniqueness identifiability "distance distributions" mixture of conformers non-uniqueness theorem;
(9) turnpike problem beltway problem reconstruct point set from multiset of pairwise distances generic uniqueness
homometric sets survey; (10) heterogeneous multi-reference alignment mixture of K signals generic identifiability
from invariant moments "estimation under group actions" orbits; (11) marginal pairwise distance distributions do
not determine joint conformational ensemble correlations between distances "three spin" OR "multi-spin" DEER
correlated distance distributions; (12) discrete tomography switching components finite point set determined by
X-rays coordinate projections on algebraic variety Rényi Heppes generalization; (13) algebraic matroid of an
irreducible variety connected if and only if variety is not a product of coordinate projections direct sum;
(14) reconstructing several point configurations simultaneously from mixed pairwise distances "partially
labeled" distances generic rigidity matroid connected [extended mode]; (15) "k-atomic" distribution uniquely
determined by its first 2k-1 moments among k-atomic distributions; first 2k moments among all distributions;
Gauss quadrature moment matching mixtures Lindsay; (16) "universally rigid" framework positive semidefinite stress
matrix "conic at infinity" affine motions super stable Connelly theorem; (17) "mixture of frameworks" OR
"ensemble of frameworks" rigidity "edge length distributions" identifiability global rigidity; (18) secant
variety of measurement variety Cayley-Menger identifiability mixture of Euclidean distance matrices sum of K
distance matrices generic uniqueness.  No search returned a theorem on mixtures of frameworks from per-edge
laws.  **"Not found" is the result of eighteen searches in one session, not a proof of novelty**; in particular
the localisation and array-processing literatures (data association, pairing in multidimensional harmonic
retrieval) were only touched.

## 7. Requests to the Ensemble division (can be sent as they stand)

1. **E1.3.**  State the configuration space in Corollary E1.3(b) and in the message ("on the free configuration
   space `(ℝ^d)^N`"), delete "determine nothing", and check Proposition A of this report (fixed lengths on a set
   of pairs whose directions are not on a conic at infinity ⇒ every affinely spanning conformation is determined
   by the mean squared distances of all pairs, with certificate `‖P^⊥ b(p)‖²`).  If you agree, Part III is its
   case `d = 1`, and the question "how many conformers do mean squared distances resolve on a chain with fixed
   bond lengths in `ℝ^d`" is the `d`-dimensional version of your Problem O1; T6(d) of this report is a first
   numerical data point (two conformers, plane: identified from seven bonds on).
2. **"Generic".**  Write "jointly generic" wherever E7/E8 are quoted without the definition (message, summary
   table, §5), and add Examples D1 and D2 as the non-generic cases with a failing conclusion.  Withdraw, or
   label as a question, "the relevant matroid is then a contraction" in §8: Example D2 is a generically globally
   rigid graph on which two conformers sharing a triangle are not determined.
3. **Stability.**  Add Proposition B (or your own version) after E7 and define the chimera gap and the switching
   gap in O4; report the gap of your own numerical examples.  For E8, state that the certificate is not sharp
   and that the bridge of §5 item 1 does not apply to Part II.
4. **Novelty labels.**  In `THEOREM_REGISTER.md`: E5(a) "elementary; formulation", E7 "corollary of the cited
   2022 theorem; reading not found", E8 "classical per-edge certificate plus E7"; mention that the published
   proof of the cited Theorem 3.5 splices `p` and `2p` along a separator.  Rephrase the headline as an
   implication.
5. **A sharper positive statement you already have.**  State E6 for rigidity: *on any graph with connected
   `d`-dimensional rigidity matroid, a jointly generic finite ensemble is determined up to replacing each conformer
   by an equivalent framework*; E7 is the globally rigid case, and for `d ≥ 2` the class is strictly larger (two
   `K_4` glued along an edge).  Add the full dichotomy: not generically globally rigid ⇒ no generic finite
   ensemble is determined.
6. **E5 on varieties.**  State E5/E6 for a rational map on an irreducible real variety (the proof is unchanged)
   before §5 item 4 uses it for torsion angles; say that "generic" then refers to that variety.
7. **Counts.**  In E8 and O5: redundant edges need no moments; `2K − 1` moments per edge suffice among ensembles
   with at most `K` conformers; for one conformation of a framework with a positive semidefinite stress matrix of
   maximal rank, `|E| + d(d+1)/2` means suffice (Proposition C here).
8. **Your numerical checks** — see §4 of this report for what the re-run showed.
