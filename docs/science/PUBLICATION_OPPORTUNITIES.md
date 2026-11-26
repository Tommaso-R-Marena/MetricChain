# Publication-level assessment

*Science division.  Version 2 (2026-11-25; version 1 at checkpoint 13).  An assessment for the research owner of which
results in the three branches are mature, which are provisional, and what each would need
before anyone could defend it in public.  Nothing here is a recommendation to submit; no
manuscript, preprint or external contact is proposed.  Verdicts marked "pending" wait for a
review of ours that is still running; they will be updated, not silently replaced.*

Sources of every judgment: `docs/science/workstreams/A1_REPORT.md` (SCI-REV-0004),
`A2_REPORT.md` (SCI-REV-0006), `SM_REPORT.md` (SCI-MSG-0002), the engineering division's
ENG-RES-0008, the theory division's own §10 and §12, and the coordinator's reading.

## 0. Summary table

| # | candidate | precise claim | verification | originality after our searches | maturity |
|---|---|---|---|---|---|
| P1 | **Adaption on a cone** (theory: Theorems 11.44/11.45 with 11.54/11.58) | exact exponents of adaptive (`= hinted`) and non-adaptive randomised algorithms for the normalising constant over the log-Lipschitz class of the Hamming cube; "adaption gains the cardinality" | lower bounds machine-checked; adaptive upper bound a paper proof refereed twice internally (R7, R8); engineering: no violation in 7·10⁶ adversarial mean runs (two levels, bounded accuracy, expectation level); **reviewed by us at checkpoint 32 (workstream R6, SCI-REV-0007): the cost accounting stands — re-derived from scratch with identical constants, independent implementation, 4 075 literal runs without a violation; eight minor points; nothing in the count is machine-checked** | the pair of exponents and their coincidence **not found** (A1, full text of the closest sources); the formulas are in print at the cone (Suárez–Silbey–Oppenheim 2012; Chatterjee–Diaconis 2018); method of the non-adaptive bound is Mathé–Novak's | **the strongest candidate; no longer provisional on the point we could check** — its remaining weaknesses are the ones a hostile referee would name: no machine check of the count, exponent `h` only as a limit of families of growing depth with no rate, nothing executed at three levels |
| P2 | Several site types, any alphabet: the channel-coding dictionary (theory §11.26) | site function = Rényi capacity of a vertex channel; non-adaptive exponent = inverse sphere-packing exponent; adaptivity gains the sampling rate | a workstream's paper proofs, upper bounds "by transfer"; two steps machine-checked; **our review R5 running**; one reference number replicated by us (`a = 0.294791`); at bounded accuracy a class-wide upper bound for every `n` now exists (Proposition A1.2, ours, unreviewed) | **the dictionary is a reformulation** (SCI-RES-0003): identities classical; mechanism in print three times (random-code glassy phase, Jarzynski bias, Hoeffding trade-off); the adaptive half has a precedent as a principle (confirmation phase: Chernoff, Burnashev, Yamamoto–Itoh; noisy search) but no formula in print | **reviewed (SCI-REV-0005): Theorem 11.99 proved; 11.101(a) proved; 11.101(b) true, two gaps in its written proof closed by our reviewer; never simulated**; as a *presentation* of P1 it is valuable and must cite the above |
| P3 | Rounds of adaptivity (theory §11.24) | two rounds lie strictly between a fixed sample and full adaptivity | **reviewed by us (SCI-REV-0003): the lower bound is correct**, every step re-derived, all numbers replicated; one displayed claim of the upper bound false as stated, repaired by one line; abstract lemma machine-checked, and now also in expected-cost form at one named instance | not found (A1; R4 at abstract level); round hierarchies and the coupling device are standard; the separating mechanism (dilution, not a chain of hidden pieces) is the distinctive point | **a theorem that stands**, conditional on P1 for the reading "does not reach the adaptive exponent"; asymptotic only — no finite-size separation is shown |
| P4 | Verified certificate kernels (theory §6; Lean) | soundness of three kernels; in particular one certificate valid for *every* residual of an envelope class consistent with interval anchor data | machine-checked; audit replicated at four heads by two divisions on independent machines | no proof logging for cost-function networks / MAP found; the class-wide kernel has no counterpart found; the pairwise kernel competes with verified pseudo-Boolean proof checking, now also importable into Lean 4 (A2; coordinator) | mature as a formalisation; its *advantage* unmeasured |
| P5 | Certification geometry (theory §§11.1–11.9) | certificates are coverings in a slack quasi-metric; a dichotomy and a rate–distortion exponent on product landscapes; finite-temperature counterpart | cores machine-checked; refereed internally (R2: "a coherent note, not a theorem-driven paper") | G4 plausibly original (an application of type covering); G1, G13 reformulations of named objects; G7's formula is an example in Merhav 2011 | mature as a note |
| P6 | Limit shape of profile sets of lattice chains (theory §11.22) | convex limit body for bridges; certificate sizes converge to its covering number; proved bracket `[116, 3 627]` (the report's `[50, 3 627]` is weaker than its own tools give) | abstract theorems machine-checked; lattice lemmas paper proofs; **reviewed by us (SCI-REV-0002): no false theorem**; tables replicated for 4–23 beads | "Fekete for sets" is the approximate-semigroup form of the Newton–Okounkov body; the lattice application plausibly original (A2) | mature as mathematics once the headline separates theorem, conjecture and estimate |
| P7 | **What local and thermodynamic data are worth to certification** (science; theory's Proposition 11.104) | on the cube class, free exact knowledge of all `k`-body marginals changes neither the adaptive nor the non-adaptive exponent; a mean-energy datum makes the zero residual easy and leaves the worst-case exponent unchanged | paper proofs by one author, enumerated; the non-adaptive half proved independently by the theory division; hidden-twin root numerical; **our referee R3 and formalisation L1 running** | value-of-information theorems of this kind not found (M); the code mechanism is known | provisional; a short note at best unless the field case is settled |
| P8 | Certified inference from averaged data (science) | identified sets under a model, an envelope class and data as linear-fractional programmes with flow duals; data certify a *lower* bound on model error; numbers on lattice chains | soundness proofs elementary; exact linear programmes to 10 beads (27 for one target) | the model-free and divergence-ball versions are **known** (moment problem; maximum occurrence; Christensen–Connault); the envelope-class version, guaranteed numbers and the lower-bound-on-model-error reading not found (M; follow-up running) | not a mathematics paper; a methods contribution only with a physical instance |
| P9 | Non-identifiability statements (science; A2) | (a) in a Gibbs class with bounded energy differences uniform `k`-body marginals are compatible with the whole a-priori entropy interval; (b) lattice chains are not identifiable from complete distance distributions; (c) Debye intensities lie in the profile class with constant `q²/6` | (a) paper proof, enumerated; (b) exhaustive enumeration; (c) proved, checked | (a) an observation with textbook ingredients, the Gibbs-class statement not found; (b), (c) simple, apparently not written down for chains | supporting material |
| P10 | **Which class do real residuals live in** (science; workstream P) | exact per-torsion and second-order constants, fit remainders in five classes, sharpness and certificate sizes for an implicit-solvent term and four force-field differences on alanine peptides; "exactly cheap inside one lineage, far from cheap for a solvent term; close to pair-additive in RMS, not in sup norm" | exact enumeration on grids; OpenMM as ground truth, re-implementation agreeing to `5·10⁻¹²`; two numbers re-run by the coordinator; **not independently replicated** | that GB is not pairwise and that an expansion in Born radii repairs most of it is known (Archontis–Simonson 2005); sup-norm per-torsion constants, their growth with length and the sup/RMS gap were not found in a thin search (six abstract queries) | a pilot; the empirical keystone of any applied paper; needs side chains, a relaxed geometry and the fixed-backbone case |
| P11 | **Certified kinetics** (science; workstream K) | cut certificates for barriers and escape rates on the existing kernels; exact robust interval of a barrier height; trap bound for every stationary local dynamics; PSPACE obstruction on chains; vacuity of multiplier relaxations | 32 Lean theorems (box case), re-compiled by the coordinator; exhaustive numerics on tiny systems | classical variational principles relabelled (Edmonds–Fulkerson; Aldous–Fill; Dirichlet/Thomson); no certified or machine-checked barrier or rate bound found in twenty searches, several at snippet level | a capability note, not a mathematics paper; needs one physical instance (a certified relaxed torsion scan) |
| P12 | **Polytope against ellipsoid: where the exponential price comes from** (science; workstream X) | certificate iff power function below gap; two-sided design bound on the cube; polynomial iff bounded order, exponent `h(α)`; `ln Z` cheaper than `min`; no free hedging; LP-funnel slope; head-to-head numerics | paper proofs by one author, each tested numerically; four arguments re-derived by the coordinator; nothing machine-checked | nearly every ingredient known (hypercircle; fractional-factorial posteriors; finite-order weights; kernelised optimism); the assembly next to a known part with matching lower bounds was not found — at the level of abstracts and snippets | a perspective with theorems; its value is the *positioning* of P1–P5 inside tractability theory and the recommendation it supports; not a stand-alone mathematics paper |
| P13 | **Robust range of an observable free-energy difference** (science; addendum A11) | over an envelope class with a submodular known part on binary sites the Gibbs measure is sandwiched in stochastic order between two uniform fields; macrostate ratios attained there; exact cancellation of common uncertainty | paper proof by one author (two lines from Holley's inequality); 900 exact linear programmes and two controls; unrefereed, not machine-checked (Mathlib contains Holley's inequality) | Holley and field monotonicity are textbook; the sandwich for arbitrary bounded-difference perturbations and its use for robust ranges not found in one search; probably folklore | a lemma; its value is that it makes an *observable* target tractable and local — the first positive robust statement about a measurable quantity in the programme |

## 1. P1 in detail — the one result that would survive a hostile referee

1. **Claim.**  For `(ε/2, δ)`-correct randomised algorithms that evaluate a `u`-Lipschitz
   function on `{0,1}ⁿ` and return `ln Σ e^{−g}`: worst-case cost `exp(n·KL((Λ₁+ε₁)/u‖½) + o(n))` for
   adaptive algorithms, `exp(n·θ_na(ε₁) + o(n))` for non-adaptive ones, at extensive
   accuracies and (with `h`, `a`) at every bounded accuracy.
2. **Verification.**  Lower bounds: Lean.  Non-adaptive upper bound: paper proof through
   Harper's theorem — and now, at bounded accuracy, a second proof without it for every `n`
   (workstream A1's Proposition A1.1: chain rule, convexity, Azuma), which also covers a
   field.  Adaptive upper bound: a nested algorithm whose cost is a paper proof with a
   history of five repaired accountings (`DEAD_ENDS.md` D45), refereed twice by the theory
   division's own referees.  Independent evidence: engineering's X-005.  **No review by
   this division.**
3. **Literature.**  SCI-REV-0004.  Anchors: Mathé–Novak 2007; Krieg–Novak–Ullrich 2025 and
   Novak 1995 (size of adaption gains on convex non-symmetric classes); Suárez–Silbey–
   Oppenheim 2012; Chatterjee–Diaconis 2018; Karnin 2016 for "verification vs search".
4. **Originality.**  The coincidence "adaptive = hinted" with exact exponents and the
   matching adaptive upper bound *without log-concavity and without a sampler*.
5. **Computational implications.**  None at accessible sizes: the nested algorithm beats
   the plain bracket only from `n ≈ 500–2000` against the worst instance (ENG-RES-0008).
6. **Scientific applicability.**  A statement about an idealised class; it says what
   evaluations cannot do, and (with P7) what local measurements cannot add.
7. **Limitations.**  Exponents only; exact evaluations; fixed `δ`; one Lipschitz constant;
   unquantified `o(n)`.
8. **Independent validation.**  Audit replicated (Lean parts); engineering's adversarial
   search; our replication of the tables of §11.20 and of `h`, `a`; nobody outside the theory
   division has re-derived the cost of the nested algorithm.
9. **Stands alone?**  Yes: it is a theorem of information-based complexity independent of
   molecules.
10. **Needed.**  A self-contained proof of the nested algorithm's cost with the `o(n)`
    explicit on a sub-class and an every-`n` statement somewhere (the radial class); the
    positioning "linear functional, convex non-symmetric cone, relative error, gain =
    cardinality"; removal of novelty claims on the formulas; an external reader for the
    cost proof.  **The single most valuable investment in the whole programme, if a
    publication is wanted, is an independent line-by-line check of Theorems 11.52/11.56.**

## 2. P7 in detail — ours, judged by the same standard

1. **Claim.**  Theorems 4, 4′ (= theory's Proposition 11.104), 5 and Proposition 5b of
   `INFERENCE_LIMITS.md`.
2. **Verification.**  One author; exact enumeration for the code facts; exact arithmetic
   for the hidden twin (the root is found numerically, not proved); the non-adaptive half
   derived twice independently.  Referee and Lean formalisation running.
3. **Literature.**  SCI-MSG-0002.  The mechanism (codes of dual distance `> k`) is textbook.
4. **Originality.**  A query model with two oracles and theorems about what the second is
   worth were not found.  The proofs are short.
5. **Implications.**  None computational.
6. **Applicability.**  The uniform cube is symmetric; the result may owe everything to
   that symmetry (with a field a marginal oracle may strictly lower the exponent:
   SCI-REQ-0001 Q2).  Until the field case is settled, "local data are worth nothing" is a
   statement about one model.
7. **Limitations.**  Exact marginals; zero known part; exponents.
8. **Validation.**  The theory division's independent derivation of one half.
9. **Stands alone?**  As a remark inside P1's paper, yes.  As a paper, no.
10. **Needed.**  The field case; a proof of the hidden-twin root; the exchange rate
    between evaluations and expectations in classes between linear and first-order.

## 3. What is *not* a publication, and why

* **The identified-set framework (P8)** is known mathematics under four names.  Its value
  for the programme is as an *interface*: it is what turns the kernels into checkers of
  statements about measurements.  It becomes a contribution only with one physical
  instance carried through — a fixed-backbone side-chain ensemble with public averaged
  data, a certified range and a certified lower bound on model error — and with the
  comparison against maximum occurrence as practised (`BENCHMARK_DESIGN.md`, B3, B4).
* **Theorem 2 (invisible order)** is an observation.  Its use is as a deception instance
  for benchmarks and as the reason why entropy inference from local data must state its
  assumption on interaction order.
* **The exponent refinements beyond P1–P3** (mean-field known parts, type classes,
  several site types) are extensions whose publication value depends entirely on P1
  standing.

## 4. Ranking for further investment (justified, not mandatory; revised at checkpoint 15)

1. An external-quality check of the adaptive upper bound (P1, item 10).
2. **The class constants where the theory's known part exists: rotamer variables on a
   fixed backbone** (P10; request P-E1).  The pilot showed that in backbone torsions a
   solvent term is out of reach of every per-site format; whether the second-order
   interface has a real instance is decided by this one measurement, at a cost of
   CPU-minutes.
3. A class with known features and a certified remainder for a real many-body term, and
   a certified typical-norm remainder (`OPEN_PROBLEMS.md` D4, D5; requests P-T2, P-T3): the
   pilot's sup/RMS gap of 4–8 and its Jensen gap of 2–3 nats against a class bound of
   71–178 say that worst-case first-order classes are the wrong price for this physics.
4. The physical instance for P8 (a certified range and a certified lower bound on model
   error from averaged data), now with P10's constants as inputs.
5. The field case of P7 and the robust interval of a ratio (SCI-REQ-0001 Q1, Q2): both
   change what the theory is *about* (measurable targets; non-symmetric models).
6. The native-versus-pseudo-Boolean measurement for P4 (SCI-REV-0006, E-1).
7. Completing the reviews of P2, P3 (running); P6 is reviewed (SCI-REV-0002: no false
   theorem; the headline must separate theorem, conjecture and estimate).
8. One certified relaxed torsion scan (P11).

Lower: further exponents on symmetric models at `βc ∼ 1` — the pilot found no physical
residual in that regime except torsion refits, for which the class is linear and the
exponent irrelevant; constants in the limit shape.

## 5. Changes since version 1

* P6: verdict no longer pending (SCI-REV-0002).
* P7: the finite-precision form is proved (Theorem 4-τ, addenda A10; SCI-MSG-0006), which
  removes the objection "exact marginals are unphysical" from one side: with error bars
  the statement gets *stronger* (all orders, not only bounded order).  Still a remark
  inside P1's paper unless the field case is settled.
* P10, P11 added.  The ranking of §4 moved the physical measurements above further theory
  on the cube.
* *Checkpoint 19:* the last two reviews are in.  **Summary of the four reviews of the
  theory division's newest sections (§§11.22, 11.24, 11.25, 11.26; more than twenty
  numbered statements): no theorem false.**  One displayed claim false as stated with a one-line
  repair; one proof step missing and supplied; two gaps in a written proof closed; one
  proved bracket improvable with the section's own tools; and in *every* section a
  headline that says more than its theorems (for §11.25 materially: two of three
  exponents).  For a publication on P1–P3 this is the pattern a hostile referee would
  attack first; the mathematics underneath held everywhere we looked.  What nobody has
  re-derived remains the cost of the nested adaptive algorithm (Theorems 11.52, 11.56) —
  still the single most valuable check.
* *Checkpoint 32:* **P1's cost proof has been reviewed from outside** (workstream R6;
  SCI-REV-0007).  Verdict: it stands.  The accounting, written before the authors' was
  read, reproduces theirs constant by constant; none of the five retracted accountings
  recurs; an independent implementation reproduces the engineering division's numbers
  to every published digit.  Two things the review adds that a paper should use: **a
  certified finite-`n` separation** — two levels with base brackets, explicit for every
  `n`, cheaper than the non-adaptive *lower* bound from `n = 1400` on at `u = 1` (the
  coordinator recomputed the lower-bound columns: identical) — and the honest wording
  of the headline: "*at the exponential scale* adaptivity recovers the hinted exponent".
  And one thing every harness should fix: numpy's binomial sampler is biased at block
  sizes of `10¹⁷` and more (confirmed independently).
* *Checkpoint 31:* **P10 has its second half** (workstream P2; SCI-MSG-0015).  In residue
  rotamer variables on a fixed backbone the known part is exactly pairwise, the solvent
  term is pairwise to hundredths of a kcal/mol for neutral side chains, the
  second-order interface has real instances for apolar side chains only, and the
  third-order interface for all enumerated ones.  With the pilot this is a complete
  empirical statement — *which class a real solvent residual lives in, in two sets of
  variables, with exact constants* — and the first evidence that an interface of the
  theory has a physical instance.  What a referee would ask: a buried environment
  (requested, P2-E1), relaxed geometry and a rotamer library, an a-priori bound on the
  third-order constants (the route is sketched in the report), and a full-text reading
  of the pairwise-GB literature (ours is at abstract level).  Still one group's
  measurement with the coordinator's re-run of one end-to-end check.
* *Checkpoint 30:* **P7 has its field case** (workstream F; SCI-RES-0006).  With a field a
  free exact one-body oracle changes neither class exponent, for every `n` (compensation
  lemma; two-component hard instance), and at an instance it helps by a bracketed
  amount.  The limitation "until the field case is settled, 'local data are worth
  nothing' is a statement about a symmetric model" (below) is lifted for one-body data;
  it stands for higher orders with a field (order 2: exact at `n = 13`, sketch beyond),
  and the result has one author, one partial second reader and no machine check.  The
  theory division's Proposition 11.109 (criterion; two conjectures) appeared the same
  afternoon; ours proves its conjecture (f) and corrects two numbers of (e) — a joint
  statement is the natural form.
* *Checkpoint 26:* **P7's statement becomes two-sided** (addendum A16; author only).  For
  local data the invariance stands at every accuracy examined; for a mean-energy datum
  it is a bounded-accuracy statement: `ln Z = S − βU` turns the problem into an entropy
  problem, the class confines the entropy to `[n·h(σ_u), n ln 2]`, and so the datum is worth
  nothing at bounded accuracy, everything beyond `KL(σ_u‖½)` nats per site (where the cost
  without it is still exponential up to `KL(½‖σ_u)`), and — if Conjecture A16.4 holds —
  something at every extensive accuracy in between.  "What a kind of data is worth, as a
  function of the accuracy asked" is a better theorem than invariance alone; it needs a
  second reader and the upper bound of the conjecture before it is claimed.
* *Checkpoint 18:* **P7 has been refereed and partly machine-checked** (R3: no false
  theorem; eight overstated or false sentences corrected in SCI-MSG-0008; L1: 78 Lean
  theorems for the short cores).  The referee names the statement P7 should become — the
  *oracle-invariance theorem* for the cube class (local data of bounded order change
  neither exponent; a mean-energy datum changes the hardest instance, not the exponent
  at bounded accuracy) — and judges it within reach: every new ingredient is a finite
  inequality, every hard ingredient is in the theory report.  P7 remains a companion of
  P1, not a paper of its own, and still owes the field case.  P13 added.
* *Checkpoint 17:* P12 added.  Together P10 (measurements) and P12 (theory) make one
  argument that none of the three branches had a day ago: *the first-order class is
  exponentially expensive by its geometry; a real solvent term is not in it at any useful
  constant; it is near a linear-information class in typical norm; and no data can certify
  that it is.*  If the programme wants an applied paper, that argument — with the
  fixed-backbone measurement added — is its spine, and P4's kernels are its instruments.
* *Checkpoint 16:* P3 reviewed (SCI-REV-0003) — the second result, after P1, that we
  would expect to survive a hostile referee, with the caveat that its meaning depends on
  P1.  P2's originality settled as "reformulation" (SCI-RES-0003); a paper on P1 must be
  positioned against the confirmation phase of sequential design and feedback coding —
  the first objection an information theorist will raise.
* *Checkpoint 34:* **the theory division applied five of our reviews** (its fourteenth
  checkpoint) — the pattern "no theorem false; headlines narrowed" is now in its text,
  with one of our own items withdrawn (a lever-arm constant we called sharper was
  theirs).  A second-round review of the revised sections is running (R9).  **A new
  candidate, small:** the certification cost of a free energy against a sampleable
  model as a function of *which divergence between truth and model is bounded a priori*
  (the theory division's floor theorem at one end, our addendum A17 for the family).
  Its value is conceptual — it says what a "certified surrogate" must mean, and that a
  root-mean-square error is not it — and it is probably a recombination of known
  estimation bounds (classification pending, A3).  It becomes a result with physical
  content only if a floor or a chi-square bound can be *proved* for a real energy term
  (P3).  Judged by the standard of §1: not a paper on its own; a section of P1's paper
  or of a methods note with the P2/P3 measurements.
* *Checkpoint 35:* **our own candidate on thermodynamic data (addendum A16) has been
  refereed internally.**  It stands, with its strongest sentence weakened: the cost at
  the visible basin is determined up to a constant and two units of the radius in a
  quantile sense, not "exactly".  For a publication the honest shape is: (i) the entropy
  bracket and the window in which a calorimetric datum removes an exponential cost —
  elementary, and partly a known bound under another name (Santha–Vazirani sources);
  (ii) the plateau twin and the isoperimetric lemma with an energy constraint — short,
  not found in print in three searches at snippet level, machine-checked in its
  algebraic core; (iii) a conjecture that survived a serious attempt at refutation and
  is open on a named interval.  This is a section of a paper on what data are worth
  (P7), not a paper.  What would lift it: the lemma for a general reference instance,
  or an algorithm with the datum below `a(u)` on the whole class.
* *Checkpoint 38:* **P6 (the limit shape) has become a better paper.**  The second-round
  review proved that the concatenation error of bridges is a coboundary (Theorem R9.1,
  SCI-REV-0009): the limit shape is the Newton–Okounkov convex set of an *exact* graded
  semigroup, every explicit bridge gives an exact point of it, the number of attained
  profiles is asymptotically its volume, and interior lattice points are eventually
  all attained.  That replaces "Fekete's lemma for sets with a bounded error" — a
  special case of known theory, as our first round said — by a statement with content
  specific to the object, and it improves two numbers with data already in the
  repository (`vol 𝒦 ≥ 1.63`; packings with zero radii).  Still missing for a
  publication: the routing lemma behind the larger inner volume; whether `ε₁ = ½` is an
  exceptional accuracy; an effective saturation constant; the theory division's
  verification of the theorem.  **P10 (which class real residuals live in) has also
  moved:** with addendum A17 (6)–(10) it now has a quantitative conclusion — in rotamer
  variables the solvent term is a small perturbation of a chain model in the sense that
  matters for certification, and a free energy at fifty residues follows from about a
  thousand to a hundred thousand evaluations with a bracket that needs two proved
  numbers.  As a methods note with the P/P2 measurements this is the most physical
  thing the programme has; what it lacks is the proof of those two numbers (P3) and a
  buried, non-homopeptide instance.
* *Checkpoint 39:* **the prior-art search removes a candidate and sharpens another.**
  Addendum A17 as a *theory* note is not a publication: its cost table is the main
  result of a preprint of February 2026 (Block and Shetty, arXiv:2602.23535), its
  bracket is Hoeffding's Theorem 3, its chain version is in print since 2006
  (SCI-RES-0009; `DEAD_ENDS.md` SD43).  The same holds, piece by piece, for the theory
  division's §11.30 — except its hinted cost as a statement of query complexity, which
  was not found.  **What survives for P10 is exactly the part that was always the
  physical one:** which row of a known table real remainders are in, measured — and the
  recipe that follows (a chain model, a sampled mean, Hoeffding's Theorem 3 with two
  certified numbers).  A methods note would have to *cite* the table, not derive it,
  and would stand on the measurements and on a certified instance (workstream P3
  reports one at twenty residues; unread when this was written).  One sentence to
  check before any such note: whether the use of Hoeffding's Theorem 3 as a second-order
  certificate for free-energy perturbation is in Decoster (J. Phys. A 37 (2004) 9051),
  which could not be opened.  **P7 (the field theorems) gained a formal core:** Lemmas
  0–3 and Theorem A are machine-checked (SCI-MSG-0019).
* *Checkpoint 40:* **P10 now has what it lacked — a certified instance — and a sharper
  open problem.**  Workstream P3 certifies `ln Z` of a twenty-residue apolar peptide on
  an extended backbone to 0.06 nats without sampling (0.005 with), from `10⁵` energy
  evaluations among `3.5·10⁹` states, and the coordinator's independent chain-model
  estimate falls inside the bracket to `10⁻⁴` nats (SCI-MSG-0020; addendum A17 (10)).  With
  P and P2 this is a complete arc: which class a real solvent term lives in (measured),
  what certification by reweighting would cost (measured), a certificate at a size
  beyond enumeration (proved on paper, replicated), and where it stops (the helix:
  cancellation that pair-by-pair bounds cannot see).  As a methods note this is the most
  defensible thing in the division's record *as measurement and construction*; its
  theory is cited, not claimed (SCI-RES-0009).  Before any external use: a machine check
  of the remainder identity and a stand-alone checker of the certificate (requests
  P3-T1, P3-E1); a proper prior-art search for the combination "evaluated low orders +
  a term-by-term tail in closed form" (six abstract-level queries so far); the sentence
  on Decoster (2004); and at least one instance that is not an exposed homopeptide.
  The charter's rule stands: no manuscript or external representation without the
  owner's authorisation.

*Note at checkpoint 43 (workstream R10; SCI-REV-0010).*  The theory division's workstream
Y would be the first treatment of the query-complexity exponents with an interacting
known part.  As a publication it now has a referee's answer to the obvious question
("is this a general effect?"): no — raised at small and moderate slopes, by the structure
factor at small ones (a theorem at second order), lowered at large slopes for the two
cost exponents, raised for the threshold throughout.  A paper that states the map is
stronger than one that states the headline; a paper that states the headline alone
would be corrected by its first reader with their own Proposition F.  What a hostile
referee would still ask: the crossover slope; a proof of the large-slope expansion; the
small-slope law for the infinite chain (the lower side is a sketch); controlled
rounding for the "certified" numerical brackets; a model with more than two states or a
field; and the prior art, which neither division has searched beyond snippets
(Rényi divergence rates of Markov sources; moment Lyapunov exponents; homomorphisms of
the cube to `ℤ`).  The small-slope law and the reversal are R10's; the charter's rule
stands: no manuscript or external representation without the owner's authorisation.


*Note after the fifth wave (2026-11-26; SCI-MSG-0024, SCI-MSG-0025, SCI-REV-0013,
SCI-RES-0012, SCI-RES-0013; addenda A17 (13), (14)).*  **The certified-free-energy arc
(P10 with workstreams P2–P6) is now the division's most complete piece of work, and
still not externally defensible; what separates the two is a short, known list.**

*What it gained in this stretch.*  (1) Scale and economy in the regime it is for:
order 4 suffices at twenty residues (9 921 evaluations among `3.5·10⁹` assignments, no
sampling, 0.055 nats), thirty residues are certified (0.0017 nats on the strand).
(2) A negative theorem with numbers on real instances: no bound that uses the charges
only through their magnitudes can come within a factor 16–153 of the true remainder on
the leucine helix at orders 3–5 — "our tail bound is loose in compact geometries" is a
result, not an apology.  (3) The frozen helix certified at thirty residues (0.033
nats) by the *form* of the certificate.  (4) Observables: a sandwich bounds every
population sharply and at no further cost — the usual objection "nobody measures
`ln Z`" no longer applies.  (5) The theory division's sandwich sampler turns the
deterministic certificate into a statistical one with an a-priori width, which it
attains on our instance.  (6) The logical skeleton is machine-checked twice.

*What a hostile referee would ask, in the order we would fix it.*
(i) **No independent program has checked the arithmetic chain** — the closed-form sums,
the covering inequalities, the transfer matrices.  The stand-alone checker (request
P6-E1; the engineering division has accepted it in principle) and the share lemmas in
Lean (P6-T1) come before any external use.
(ii) **Every certified instance is an exposed or a frozen homopeptide** on an ideal
backbone with a three-state grid per dihedral.  A compact ensemble with real
side-chain entropy is where the certificate may fail, and it has not been run
(`OPEN_PROBLEMS.md` D6, D9).  One such instance, certified or shown out of reach with
the reason, is worth more than another ten residues of valine.
(iii) **The certified constants are one workstream's paper proofs** (P3's Theorem 3 with
interval enclosures), never reviewed outside it; two floating-point allowances are
allowances.
(iv) **Prior art has been searched at abstract level only.**  The nearest neighbours
recorded by workstreams P2 and P5 are: provable ε-approximations of partition
functions for pairwise energy bounds in computational protein design (Jou, Holt,
Lowegard & Donald, *J. Comput. Biol.* 27:550 (2020), doi:10.1089/cmb.2019.0315),
tuple expansions for non-pairwise energies fitted, not bounded (Hallen, Jou & Donald,
*J. Comput. Biol.* 24:536 (2017), doi:10.1089/cmb.2016.0136), and pairwise
decompositions of generalized-Born energies whose error is assessed numerically
(Gaillard & Simonson, *J. Comput. Chem.* 35:1371 (2014), doi:10.1002/jcc.23637;
*J. Chem. Theory Comput.* 13:4932 (2017), doi:10.1021/acs.jctc.7b00202) — all at the
level of abstracts.  What we did not find there is a *certified* bound on the many-body
remainder of a GB term; that is a statement about five to ten queries, not about a
literature.  A proper comparison with the provable-partition-function line is the
second thing to do.
(v) **Model-relative.**  Nothing says GBn2 describes water; the populations are those
of a rotamer model.  A methods note can say so in its title.

*Verdict.*  Mature as measurement and construction inside the programme; one checker,
one hard instance and one literature comparison away from something a careful outsider
could try to break.  For the theory division's side of the same arc (§11.7, §11.30):
our review R12 found two sentences to replace and no theorem false (SCI-REV-0013).
The charter's rule stands: no manuscript or external representation without the
owner's authorisation.

*Note after addendum A17 (17) (2026-11-26; SCI-RES-0017).*  **The arc gained a
second mode — a probabilistic certificate — and an optimisation with a clean
structure; neither is externally defensible yet.**  (1) With the theory division's
nested sampler the order-5 ball of the serine helix gives `ln Z` within `5·10⁻⁴` nats
at probability 0.95: the headline instance of the last note with 25 times less
width and a ninth of the evaluations.  For a paper this is the natural "practical"
half of the method, and it is a joint result: the sampler and its bound are theirs,
the instance, the inner sandwich and two refinements ours.  (2) "Which shares" has
an answer that reads well outside the programme: the valid site penalties are the
core of a convex game, equal shares are its Shapley value, and the best bound is a
convex programme with a sort as oracle.  *Prior art to check before any claim:*
optimising a split to tighten a bound on `ln Z` is standard in variational inference
(tree-reweighted bounds, Wainwright–Jaakkola–Willsky; weighted mini-bucket,
Liu–Ihler — both confirmed bibliographically, neither opened); whether a core /
greedy structure for a *remainder* allocation appears there or in the dead-end
elimination and K\* literature has not been searched.  (3) *What is still missing* is
what the last note listed, unchanged: a referee (addenda A17 (13)–(17) are
unrefereed inside the division), a checker, a second force field, and an instance
that is not a homopolymer on an ideal backbone.

*Note after addendum A17 (16) and workstreams R13, P7 (2026-11-26; SCI-MSG-0026,
SCI-REV-0014, SCI-RES-0014).*  **The certified-free-energy arc gained its hard
instance and lost its excuse; it is still not externally defensible, and one item of
the list above got longer.**

*Gained.*  (1) The "hard instance" the last note asked for exists: a compact ensemble
that is not frozen — serine on a twelve-residue helix, `4.9·10⁹` assignments, more than
half of the side chains off the anchor — bracketed within 0.077 nats at order 5 and
0.012 at order 6 without sampling.  (2) A reason, not a recipe: the cost of a sandwich
is its mean band under the true ensemble (an elementary lemma), which explains every
earlier success and failure of the arc in one line — shares gain a factor `1/p` per
level, so they decide for frozen ensembles only — and lets a certificate be costed
before it is paid for; with its limit found by breaking it (a floor can delocalise, a
ceiling cannot).  (3) A boundary that can be stated to an outsider: on a helix at
twelve residues, neutral side chains are in reach and charged ones are not at any
affordable order.  "Works for neutral, fails for charged, here is why" is a more
publishable sentence than "works on our instances".  (4) On the theory division's
side, with our workstreams: the rate of their level recursion is machine-checked
(R13), and "shares at the leaves" certificates are terms of their own checker's
language, with thirteen real ones accepted (P7).

*What a hostile referee would ask now.*  Items (i)–(v) of the last note stand.  New:
(vi) **the newest results have been read by nobody but their author** — the lemma, the
window models and the twelve-residue numbers; an internal referee was launched and
was stopped by a platform safeguard before it began (`RESEARCH_SYNTHESIS.md` §0).
This comes before everything else for those results.  (vii) The window model
enlarges the model class of the certificate; the stand-alone checker's specification
gains a table type (A16-E1), and the floating-point allowances were computed for the
pairwise models — whether they cover the larger number of exact terms has not been
examined.  (viii) "Charged is out of reach" is a statement about workstream P3's
constants, not about nature: the true many-body terms of lysine are twenty times
serine's, not a thousand; workstream P8 is to say which lever exists.

*Verdict.*  The arc now has a result (1), a mechanism (2) and a boundary (3) — the
three things a methods note needs — and its newest third is unrefereed.  No manuscript
or external representation without the owner's authorisation.
