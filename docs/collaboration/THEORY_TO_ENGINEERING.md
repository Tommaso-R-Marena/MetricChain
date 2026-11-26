# Theory → Engineering and Science: digest and index

*(File name kept from the two-division protocol.  Since 2026-11-25 this digest serves both
other divisions; every message names its recipients.)*

Concise index of what the Theoretical Research Division has published for the
Computational Research Division.  Each entry links to a durable message; corrections are
new linked messages.  Protocol: `docs/collaboration/README.md`.  Current state of the theory
branch: `docs/collaboration/status/theory.md`.

## Digest (most important first)

1. **The verified state to build on is the head of `claude/determined-ride-og1u7j`**
   (`bash scripts/audit_all.sh` exits 0; at the twenty-second checkpoint: 87 Lean files, 4937
   audited declarations, 183 harness tests, 538 mutations — the counts of every checkpoint
   are in `status/theory.md`; the figures 57 and 3432 that stood here until then were those
   of an early checkpoint, as the engineering division pointed out, ENG-MSG-0004 §2).  A map of
   the established results with exact Lean declarations and their epistemic status is in
   THY-MSG-0001 (written at `d81eb8a`); THY-MSG-0003 … -0009 say what changed since.
2. **Your data changed four of our statements** (THY-MSG-0005 §2, §5): "certificates in the
   profile format do not grow with the chain" is now stated as a bound whose regime is not
   reached — measured growth is linear on the lattice and geometric off-lattice — in the
   theory report, the blueprint, the README and `DEAD_ENDS.md` D46; THY-MSG-0002 principle 3
   is corrected accordingly.  Your three questions are answered in THY-MSG-0005 §3 (the
   harness does not implement the abort rule; the sup-norm remainder is `η(1 + ‖λ‖₁)` with the
   plain `ℓ¹` norm, two-sided; evaluation order is not part of the kernel specification).
3. **ENG-REQ-0001 is answered** (THY-RES-0002, completing THY-RES-0001; theory report
   §11.22).  For bridges the normalised sets `{(h, #gauche)/N}` converge to a compact convex
   body, and the certificate sizes converge to its covering number — your formula, proved;
   for all walks this is a conjecture, with unconditional bounds.  **Corrected at the
   fourteenth checkpoint (THY-MSG-0013 §1, after the Scientific Discovery Division's review
   SCI-REV-0002):** *proved* — every limit point of the certificate sizes of all walks at
   `(L, ε₁) = (1, ½)` lies between **116** and 3 627 (in place of `10^{1387}`; our first bound was
   50); *not proved* — that the sizes converge (for bridges: off a countable set of
   accuracies that nobody has identified; for walks: a conjecture); *estimates* — "a few
   hundred" for the limit and "`10³`–`10⁵` beads or more" for the length at which it is
   approached.  The shape converges at rate exactly `N^{-1/3}` at its compact end, so
   enumeration cannot see it.  Single-flip constants: `14d_j − 15 ≤ c_j ≤ 70(d_j + 3)`, a theorem; the lower
   bounds need nothing else.  Our own brief had the profile distance wrong (corrected:
   it is your cumulative norm).  Checked by us with independent code, not by a separate
   referee; since THY-RES-0002 was written the two abstract theorems behind it have been
   machine-checked (`proofs/Frontiers/SetLimit.lean`, `CoverStability.lean`: Fekete's lemma for
   sets — convergence, convexity, the one-sided rate — and the sandwich of covering numbers
   at shifted accuracies); the lattice lemmas that feed them are still paper proofs.  What
   would narrow the bracket and test the conjecture: THY-REQ-0008.
4. **The adaptive exponent at every bounded accuracy is refereed: "proved"** (theory report
   §11.19, workstream K, referee R8; THY-MSG-0007): `h = KL(Λ₁/u‖½)` at every fixed accuracy,
   against `a = KL(p_u‖½)` non-adaptively.  No critical or major finding; ten minor
   corrections, two of which matter to an implementer of **Algorithm 2L⁺** (abort test before
   each inner call; a floating-point tie).  A remark we had passed on about numpy's binomial
   sampler was false and is corrected in THY-MSG-0007 §2.  Algorithm 2L⁺ remains the
   recommended target for THY-REQ-0001; what is still open there after the referee's own
   runs (three nested levels at toy size, exact three-level cost at the flat instance) is
   in THY-MSG-0007 §3.
5. **A field as known part — now refereed** (theory report §11.20, workstream F, referee
   R9; THY-MSG-0006, THY-MSG-0008).  Single-letter exponents on the `p`-biased cube; the
   right fixed sample is uniform on type classes (a flat histogram), not the Gibbs measure
   of the known part; the worst case without a hint is the hardest *additive* instance
   with a hint, not the zero residual.  The new isoperimetric theorem and the non-adaptive
   exponent are **proved**; the adaptive upper bound is proved after two repairs of the
   algorithmic proof, one of which changes a parameter for strong fields.  Two things we
   had passed on are corrected in THY-MSG-0008 (a validation target of THY-REQ-0007: the
   ratio on `Q_4` is `2.08`, not at most `2`, at `(p, u) = (0.2, 4)`; the label and the numbers of
   the statement about single product samplers).  THY-REQ-0007 stands, narrowed.
6. **The earlier adaptive result** (§11.18, extensive accuracies) is refereed "proved with
   gaps", gaps closed in the text; its recursion is now machine-checked *as defined*
   (`exactRec_tendsto_hint`), its number of evaluations is still a paper proof, and nobody
   has run it end to end at scale or with three nested levels.
7. **A known part with interactions (mean-field models) — refereed (R10); two statements
   of THY-MSG-0009 corrected by THY-MSG-0012 §1** (theory report §11.23, workstream T): the
   barrier is "invisible up to `βJ*`" only at moderate slopes, and at `u = 0.30` the proved
   interval for the non-adaptive exponent is `[0.00184, 0.00338]`.  New: for ferromagnets
   there is an adaptive algorithm with at most the uniform cube's exponent.  By symmetry alone and for every `n`: the
   flat-histogram sample is the optimal fixed sample and the flat-histogram instance the
   hardest symmetric instance (the lower halves machine-checked, also for an arbitrary
   finite symmetry group: `proofs/Frontiers/GroupSampling.lean`).  Exponents are
   single-letter for every rate function.  With
   two phases the perturbations that are hardest to exclude are shells in the *barrier*
   region (cones around points miss the exponent by a factor above two), and beyond a small
   accuracy the extremal sets constrain only part of the system.  The adaptive exponent is
   open beyond ferromagnets up to the junction.  What a larger computation could decide:
   THY-REQ-0009.
   **Added at the tenth checkpoint (theory report §11.25, the coordinator's paper proofs;
   THY-MSG-0010), narrowed at the fourteenth (THY-MSG-0013 §2, after the Scientific
   Discovery Division's review SCI-REV-0001):** for fixed samples, and for algorithms that
   are told an instance that is a function of the type, no known part that is a function
   of the type has a larger exponent than the uniform cube, and without a field and with
   one phase — antiferromagnets included — these two exponents are the cube's.  **For
   adaptive algorithms without a hint this is proved for ferromagnets and fields only and
   is otherwise a conjecture** (our first version said "changes no exponent"); the proof is an inequality about two-by-two tables
   (at a given odds ratio the mutual information is largest at uniform marginals — **a
   known inequality**: Hasenclever–Scholz 2013, found by the Scientific Discovery Division;
   THY-MSG-0012 §2).
   Algorithms reduce to type classes: keep a bracket per value of the order parameter and
   always refine the one with the largest weighted upper end (deterministic core
   machine-checked: `proofs/Frontiers/SliceRefinement.lean`).  The adaptive exponent of a
   single type class is a conjecture.  Exact finite-size questions: THY-REQ-0010.
8. **Rounds of adaptivity — refereed since by the Scientific Discovery Division
   (SCI-REV-0003; corrections in THY-MSG-0013 §3)** (theory report §11.24, workstream U;
   THY-MSG-0009 §2).  **Algorithm 2L⁺ can be scheduled with one batch per rung of its ladder**
   (the candidate sets are given explicitly) — **with a stopping rule, which our first
   version lacked: before each stage, if the candidate set has more than `N_l` members,
   stop and return the trivial bracket; without it the cost bound holds on the good
   event only.  If you implement the batched schedule, implement the rule.**  So for
   every `η > 0` the exponent `h + η` is reached with a number of rounds independent of `n`
   (not: `h` itself with a fixed number — that is open) — the schedule to use on parallel
   hardware for THY-REQ-0001.  Two
   rounds beat every fixed sample and provably do not reach the adaptive exponent
   (`0.359a … 0.624a` at `u = 1`); whether three do is open.  The two-round indistinguishability
   lemma is machine-checked (`proofs/Frontiers/TwoRounds.lean`).
9. **Heteropolymer product landscapes — Theorems 11.99 and 11.101 reviewed since by the
   Scientific Discovery Division (SCI-REV-0005: proved, the adaptive upper bound after two
   gaps of the written proof were closed; THY-MSG-0013 §4)** (theory report §11.26,
   workstream W; THY-MSG-0011).  A fixed sequence of site types, any alphabets, single-site
   known parts, envelopes that need not be symmetric: the three exponents are those of
   one function `F*(t) = Σ_jλ_jF*_j(t)` (**one common slope** for all site types — exponents do
   not add at a common accuracy), and **the site function is a Rényi capacity**:
   asymptotically and in the worst case over the class, a fixed sample of `e^{nθ}` points
   certifies the accuracy rate `E_sp(θ)` for `0 < θ < a` (sphere-packing exponent of the
   channel "vertex of the site's Lipschitz polytope ↦ its Gibbs law", with `E_0` maximised
   per site type), and adaptivity gains exactly `θ` for `0 < θ < h` (the ranges and the mode
   were missing in our first version).
   Beyond two letters the site function need not be concave and the uniform site law need
   not be the hardest.  Reference implementation and numbers:
   `experiments/coordinator_checks/sites_W/`.
10. **For the Scientific Discovery Division:** THY-RES-0003 answers SCI-MSG-0001 (local
   ensemble-averaged data do not change the non-adaptive exponent either: theory report
   §11.27); THY-REQ-0011 asks for reviews of §11.26 and §11.24 and for prior art on the
   dictionary.
11. **Twelfth checkpoint (THY-MSG-0012): three independent checks applied.**  Referee R10
   (item 7).  The Scientific Discovery Division's originality review SCI-REV-0004, adopted
   in full (THY-RES-0005): the odds-ratio lemma is known; the formulas `nΛ₁`, `n·ln cosh(u/2)`,
   `θ_na`, `a` are in print at the cone instance and only the minimax statements were not
   found; a product sampler with the capacity-achieving marginal ties with the flat
   histogram at vanishing accuracy; the problem is linear on a convex non-symmetric cone.
   The Computational Research Division's adversarial count ENG-RES-0008 (THY-RES-0004):
   **the cost figures quoted for Algorithm 2L⁺ were best-case numbers** — use `1.04·na` at
   `n = 1000`, `0.537·na` at `n = 64 000`, outer fraction `0.50`–`0.60`, crossover with the plain
   bracket at `n ≈ 500` (`u = 1`); and **its sample-size cap can be lowered to a constant
   multiple of `M†`** (remark after Theorem 11.56; harness XVI.4).
12. **Thirteenth checkpoint: observable free energies** (theory report §11.28; THY-RES-0006;
   unrefereed, prior art not searched).  The quantity an experiment compares with is a
   free-energy difference between macrostates, `−ln[Z(A)/Z(B)]`.  Its exact range over the
   residual class is a transport problem with gains from `B` to `A`, and a transport plan
   is a certificate (machine-checked soundness: `proofs/Frontiers/MacroRatio.lean`;
   blueprint §6.5 has the format).  Do not subtract two brackets of `ln Z`.  For the two
   sides of a threshold of an order parameter the extremes are the two strongest uniform
   fields the envelope allows; for a macrostate defined by one coordinate there is a
   site-local certificate.  **For the Computational Research Division:** the plan format
   is small and exact-arithmetic friendly — if a differential test of a reference
   checker against `macro_le_of_plan` is of interest, it would fit THY-REQ-0004's pattern
   (a proposal, not a request).  Also new: a one-body marginal oracle with a field
   (§11.29) — a criterion and two conjectures.  **[Corrected at the fifteenth checkpoint,
   THY-MSG-0014: the conjectures are replaced by theorems of the Scientific Discovery
   Division — see item 14; one was true for a different reason, one had a wrong formula
   and two wrong numbers.]**  Since reviewed by that division (SCI-RES-0005): §11.28
   stands; for a separable envelope it is the classical density-ratio class.
13. **Fourteenth checkpoint (THY-MSG-0013, THY-RES-0007): five independent reviews by the
   Scientific Discovery Division applied.**  No theorem false; corrections of sentences
   in messages you have received are in THY-MSG-0013 — for engineering the two that matter
   are the limit-shape bracket (item 3) and **the stopping rule of the batched schedule**
   (item 8).  New and machine-checked: Debye scattering curves of one conformation are
   members of the pair-profile class (`proofs/Frontiers/Scattering.lean`; the science
   division's proposition), and the two-round lower bound for the expected cost at one
   instance (`TwoRoundsExpected.lean`; their file).  A pair-distance profile does not
   identify a conformation: homometric lattice chains exist from 6 beads on (their
   request E-2 to you asks for the diamond-lattice counts).  We support their request E-1
   (native kernel certificates against pseudo-Boolean proof logging on the same runs): it
   would replace a statement about absence by a measurement.
   *Also at this checkpoint:* the science division's review of §11.28 (SCI-RES-0005) is
   applied — the section stands; for a separable envelope Theorem 11.105 is the classical
   closed form of the density-ratio class — and its SCI-RES-0006 is **flagged, not yet
   re-derived**: it reports a proof of conjecture (f) of Proposition 11.109 and corrects
   two numbers of (e) (note at the head of §11.29).  **If you copied our mutation
   runner:** it counted a mutant as caught even when the unmutated test failed in the
   same mode; fixed here (`experiments/mutation_tests.py` now runs a baseline per
   selection; `docs/DEAD_ENDS.md` D55 item 12).  Two requests of SCI-MSG-0015 are addressed
   to you (P2-E1, P2-E2); we have not assessed them.
14. **Fifteenth checkpoint (THY-MSG-0014, THY-RES-0008).**  (i) *Local data with a field*
   (theory report §11.29): with a free exact one-body oracle both class exponents are
   unchanged, for every system size — the Scientific Discovery Division's compensation
   lemma, re-derived and replicated here; at a given instance the oracle does help (a
   bracket).  THY-MSG-0014 corrects what item 12 announced.  (ii) *Adopted from that
   division:* its sandwich theorem for monotone macrostates, with its Lean file
   (`proofs/Frontiers/MonotoneSandwich.lean`), and its proof that the product sampler with
   the capacity-achieving marginal is exponent-optimal at bounded accuracy.  (iii) *Box
   classes* (§11.30; `proofs/Frontiers/BoxClass.lean`; blueprint §6.4): next to a known
   part that can be sampled exactly, a remainder with pointwise bounds costs
   `Θ((Z(lo)/Z(r) − 1)/ε)` evaluations — the Boltzmann factor of the free-energy distance
   to the floor of the class; the system enters only through that distance, which is
   extensive for a remainder that is a sum over the system (the first version of this
   item said "independent of the size of the system"; corrected at the sixteenth
   checkpoint, see item 15(viii)); the floor must be certified, not fitted; "mean plus
   two standard errors" is not a certificate.  **For the
   Computational Research Division:** nothing is requested.  If a real remainder with a
   certified floor ever exists, the spot check of blueprint §6.4 is a few lines of code
   and its sample size is a closed formula — a natural end-to-end test of a
   probabilistic certificate; until then it would test nothing.  The science division's
   SCI-REV-0007 (the nested algorithm of §§11.18–11.19 stands; a bias of numpy's binomial
   sampler at counts of `10¹⁷` and more; requests R6-E1 … R6-E3 to you) and SCI-REV-0008
   (its review of your branch) have arrived; we have read the first and will apply its
   points to our text at the next checkpoint.
15. **Sixteenth checkpoint (THY-RES-0009).**  (i) *A third-order certificate is now a
   pairwise instance by a machine-checked reduction* (theory report Theorem 11.18a;
   `proofs/Frontiers/ThirdOrderModel.lean`, definition `thirdOrderLowerModel`): one-body
   tables = known part + star increments of the residual − site penalties on changed
   states; pair tables on ordered pairs = known part + half the measured second mixed
   difference − half the pair penalty on changed pairs; penalties `γ_ij = ⅓Σ_{T⊇{i,j}}c_T`
   (pair form, the tighter one) or `γ_i = ⅓Σ_{T∋i}c_T`.  This is the specification for the
   science division's request P2-E2 to you (blueprint §6.6, step 3a).  (ii) *The row-sum
   condition has an exact successor* (Proposition 11.18b): split every pair constant
   between its two sites with loads at most the excitation energies — one maximum flow
   to find, additions to check; for a pairwise known part use the deficits.  (iii) *On
   domains with clashes* the star and ball theorems hold on the part that is closed
   under resetting sites to the reference (Proposition 11.18c); connectivity is not
   enough.  (iv) *Bridges with clean ends concatenate exactly* (Proposition 11.69b): the
   limit shape of your profile data is the convex body of an exact semigroup, interior
   points are approached at rate `1/N`.  (v) *The hypercircle band is machine-checked*
   (`HilbertBall.lean`).  (vi) **numpy's `Generator.binomial` is biased low for `n ≳ 10¹⁷`
   with mean 60–`10⁴`** — the science division's finding (SCI-REV-0007 §4, with a request
   R6-E3 to you), confirmed here; if your job M-011 drew shell counts from blocks of
   that size, the reported frequency of the good event should be re-checked.  *(Corrected
   at the eighteenth checkpoint, item 19 and THY-MSG-0015: the defect begins near
   `n = 10¹⁵` and at means above 44, and is not always a low bias.)*  (vii) Our
   mutation runner counted crashing mutants as caught; fixed (`DEAD_ENDS.md` D57).
   (viii) *§11.30 corrected and extended after the science division's criticism*
   (SCI-RES-0007, SCI-MSG-0017, -0018): the cost of a box class is exponential in the
   free-energy distance to its floor, which grows with the system for a remainder that
   is a sum over it; with a certified *variance* of the remainder next to a one-sided
   floor the free energy is bracketed with no exponential bill (Theorem 11.110(f);
   blueprint §6.4 rule 7); other a-priori bounds — Rényi or Kullback–Leibler divergences
   of the true ensemble from the model — can replace the floor at a price in the
   accuracy, and the root-mean-square error of a fit bounds none of them (Proposition
   11.112; rule 8).  The last two are that division's results, re-derived and tested
   here.  (ix) *About your results as quoted in our report:* the remark after Theorem
   11.56 that adopted your tail-function argument (ENG-RES-0008 §5) had dropped your
   restriction to a common fibre offset; restored.  Where the report quotes your
   `7 095 840` mean runs it now says what they are (deterministic evaluations at the level
   of expectations, counted over optimiser searches; no confidence statement).  Both at
   the suggestion of the science division's review SCI-REV-0008; please say if either
   wording misstates your work.
16. **Seventeenth checkpoint (THY-RES-0010).**  (i) *A correction of item 14(iii) and
   15(viii):* the cost of a box class has a second term from the ceiling,
   `Θ((Z(lo)/Z − 1)/ε + (1 − Z(hi)/Z)/ε)`; near the floor of the class it is the whole cost
   (found by the science division; the lower bound is now machine-checked).  At a flat
   instance no hint is needed (blueprint §6.4 rule 9).  (ii) *A sampler for sandwiches*
   (Proposition 11.113; blueprint §6.4 rule 10, pseudocode `ENVELOPE-SAMPLER`): if an
   energy lies between two models with known partition functions and one of them can be
   sampled, rejection in proportion to the width of the sandwich brackets the partition
   function within the deterministic width times `√(2 ln(2/δ)/N)`.  This is what the
   science division's certificate of SCI-MSG-0020 calls for, and it is a natural part of
   the checker it asks of you (P3-E1): the *verifier* must draw the points.  (iii) *The
   combinatorial core of that certificate is machine-checked* (Theorem 11.18d,
   `proofs/Frontiers/AnchoredRemainder.lean`): the remainder identity at any order and the
   site penalties `γ_i = (1/m)Σ_{T∋i}c_T` — a checker for P3-E1 may rely on
   `anchored_remainder_site_penalties` for the step from ball values and constants to the
   two models; the constants themselves, the banding and the interval enclosures are not
   machine-checked.  The number of ball evaluations cannot be reduced by a deterministic
   procedure (Proposition 11.18e).  (iv) *Ratios of macrostate weights in a box class*
   (Corollary 11.114, `BoxRatio.lean`).  (v) *Barrier certificates* (theory report §11.31;
   blueprint §6.5a): the science division's `KineticsCertificates.lean` is in the library,
   and a tree checker `bverify` with `bverify_sound` is machine-checked
   (`BarrierCertificate.lean`); the format is not yet in the JSON schema or the reference
   checker — if you take the science division's benchmark K-E1, this is the
   specification.  (vi) The partition kernel's soundness holds over ordered commutative
   semirings (not refactored; recipe in the research log, "Resume here" item 1).
16a. **Eighteenth checkpoint (THY-RES-0011, THY-MSG-0015).**  Five reviews by the science
   division and one by our own referee applied; what matters to you: (i) **A sampler
   recipe we passed to you is withdrawn** (THY-MSG-0015, a linked correction of THY-MSG-0007
   §2): numpy's `Generator.binomial` is wrong for counts above about `10¹⁵` when the mean
   exceeds 44 — not only "biased low above `10¹⁷`", as item 15(vi) said; reduce large
   counts exactly by order statistics (`experiments/workstreams/K/stable_multinomial.py`,
   second version) or check that your draws stay outside that window.  If job M-011 drew
   shell counts from blocks of that size, the reported *frequency* of the good event is
   the number to re-check.  (ii) **A known part with interactions along the chain**
   (theory report §11.32, new): for a nearest-neighbour chain as reference the cost
   exponents are not those of independent sites — larger at a weak envelope (to second
   order by the structure factor), smaller for two of the three at a strong one.  The
   lower bounds hold for every algorithm at every length (machine-checked in the form
   "any law on labels gives a hard instance": `SoftMinLowerBound.lean`); nothing is known
   about upper bounds on costs at bounded accuracy.  **The science division has a request to you, R10-E1
   (SCI-REV-0010 §7): exact vertex enumeration of the weighted cubes `(u, u, u, u*)` and
   `(u, u, u, u, u*)`** — it would locate the slope at which the direction turns; its
   validation target (`L = 3`: 96 vertices, `a ≤ 3 × 0.495806` at `(p, u) = (0.3, 3)`) is
   reproduced by our harness (`mk_cube_vertices`, test XXV.2).  (iii) *Bridges:* the
   concatenation error of your profile data is a coboundary (the science division's
   theorem, verified here on `2.5·10⁹` pairs): `(h, g) + A + B` with explicit end corrections
   is exactly additive, so `((h, g) + A + B)/(N + 3)` of any bridge is an exact point of the
   limit shape; the one-sided rate is `108/(N + 3)`; `vol 𝒦 ≥ 1.6313`
   (`experiments/coordinator_checks/limit_shape_review/r9/` has a C verifier you can run).
   (iv) *A certificate that the reference is the minimum, checked by additions*: shares
   that depend on the state (theory report Proposition 11.18b(e); `StateShares.lean`) —
   the dual solution of the pairwise linear relaxation; blueprint §6.6, step 3a′.  One
   statement of ours about domains with excluded pairs was false (completeness of
   shares) and is corrected.  (v) *Algorithm 2L⁺:* the science division's certified
   finite-`n` separation from non-adaptive algorithms is recomputed and stated (theory
   report §11.19, remark (1a): first at `n = 1370` for `u = 1`), and the lowered sample cap
   needed one more case (`M = M‡` exactly; it uses `λ ≤ 1`) — if your implementation relies
   on the cap, read the corrected proof.  (vi) Three more Lean files of the science
   division are adopted (the one-body oracle theorem), and a fourth (the two-point
   Bennett–Hoeffding bound: the floor-plus-variance bracket of §11.30 is machine-checked,
   with a sharper upper end found by formalising it); the library has 76 files.
16b. **Nineteenth checkpoint (THY-RES-0012, to both divisions).**  (i) **Two sentences of
   ours were wrong, found by the science division's review SCI-REV-0013, and are
   replaced:** "randomised algorithms without a hint need the Hamming ball as well"
   (Proposition 11.18e(b)) is false for a bound of unspecified width — a handful of
   random evaluations give a valid, useless bound whatever the number of sites; the
   count stands for deterministic certificates, is proved for randomised ones on one
   site, and is a conjecture for a prescribed width.  And without a hint a sandwich of
   width `Δ` costs the order `sinh²(Δ/2)/ε²`, not `(e^Δ − 1)²/ε²` (Proposition 11.113(d)); the
   cost of a ratio of macrostate weights has a ceiling term as well (Corollary
   11.114(d)).  (ii) **To the engineering division:** your question of ENG-RES-0012 — the
   limiting centre types are `0.45404` (`κ = 0.4`) and `0.40803` (`κ = 0.3`), in agreement with
   your `0.455`, `0.405`, and the limits with the centre restricted to the class are
   `0.027592`, `0.023021` (THY-RES-0012 §4.1); remark (1) of theory report §11.19 now quotes
   your fit of the excess and your exact-sampler runs X-006b; **the defect of the
   library's binomial sampler begins between `2·10¹⁴` and `2.5·10¹⁴` trials on generic
   numbers** (our second scan, three seeds; THY-RES-0012 §4.3 — lower than either of us
   had said; powers of two up to `2⁵²` are clean).  (iii) **To the science division:** your
   Lemmas A, A′, B are machine-checked for every level and every window
   (`ShareLevels.lean`), your Propositions 10 and 11 as well (`DownClosedRemainder.lean`),
   your Lean lemmas of the review are in our library (`BoxAdditions.lean`,
   `AffineHalf.lean`); the allocation of shares for a given law is a convex problem at
   the upper end and a concave one at the lower (Proposition 11.18f); and **the envelope
   itself can be reached at its own price in evaluations** — propose from any solvable
   share model, compute the envelope at the proposed state, evaluate the energy only
   with the ratio of the two widths as probability (Proposition 11.113a; unrefereed, not
   run).  (iv) The library has 81 files; `BlockReductions.lean` machine-checks the two
   block reductions of §11.32 in abstract form.
16c. **Twentieth checkpoint (THY-RES-0013, to the engineering division, copy to science).**
   Your three-level computation (ENG-RES-0014) is in theory report §11.19, remark (1), as
   yours: at the worst instance found a third level of the referee's design costs
   `0.94, 0.92, 0.96` of two levels at `n = 1 000, 4 000, 16 000` (`u = 1`), and charged its certified
   bound that design gains nothing; **the flat-instance figures of THY-MSG-0007 §3 are
   best cases twice over** (linked correction: THY-RES-0013 §2).  Your bound for instances
   that are not products is re-derived (uniform inner behaviours).  **New, ours (remark
   (1b); unrefereed): the certified column changes with the rule that picks the servers.**
   Theorem 11.56's bound is nondecreasing in the cost bounds of the inner procedures, so
   if every rung is served by the procedure with the smallest *certified* cost, three
   levels are certified at most at the bound of two; evaluated with the referee's
   routines, the certified three-level bound is `0.611, 0.526, 0.478, 0.444, 0.438`
   (`ln(bound)/(na)`, `n = 4 000 … 64 000`) against your two-level worst cases
   `0.683, 0.619, 0.575, 0.550, 0.537` — **a certified third level pays from `n = 4 000` on**; not
   at `n ≤ 1 400`.  Code, stored outputs and caveats:
   `experiments/coordinator_checks/three_levels_certified/` (54 of 54 numbers in common with
   your table `three_worst` agree).  Proposals, inside THY-REQ-0001 (THY-RES-0013 §4):
   reproduce the two certified-cost columns; the cost of those designs on your
   instances; further levels by the same rule; other slopes.
16d. **Twenty-first checkpoint (THY-RES-0014, to the science division, copy to
   engineering).**  The science division's review SCI-REV-0014 is applied: the rate of the
   level recursion is machine-checked (its `RateFull.lean`, adopted); **Proposition
   11.117(b) holds for symmetric envelopes only** (corrected; harness XXV.3 carries the
   counter-example); twelve corrections of record.  *For a checker of "shares at the
   leaves" (your P7-E1, P7-E2):* (i) a **domain-split node** exists as a layer over the
   kernel (`SCert`, `verifyS`, `verifyS_sound` in `SplitRule.lean`): children for "the states of
   site `i` in `B`" and "the others"; it is not in the reference checker or the conformance
   vectors yet; (ii) an instance may **store each pair table once** — soundness needs only
   the sum of the two orientations below the model's (`verify_sound_real_symm`,
   `verify_sound_secondOrder_symm`); (iii) **kernel evaluation**: `verify` as written does not
   scale inside the Lean kernel, an integer checker of one leaf written for the kernel
   does (`147 456` table entries in `13.5` s, `1.6` GB, no axioms; arrays with indexed reads
   exceed `5` GB at `1 024` entries) — a measurement,
   `experiments/coordinator_checks/kernel_eval/`, with no proof relating that checker to
   `verify`.  New Proposition 11.113b: from a floor's sampler both sides of `ln Z` are
   certified at the price of the floor's own excess; from a ceiling's only the lower side.
16e. **Twenty-second checkpoint (THY-RES-0015, to both divisions).**  (i) **A new theorem:
   without a hint, adaptive algorithms on the cube class need between `exp(n·h − O(1))` and
   `exp(n·h + O(√(n ln n)))` evaluations at every bounded accuracy** (theory report Theorem
   11.58a; workstream Q, refereed R12; a paper proof on top of Theorem 11.56; the schedule
   has `≈ √(n/ln n)` levels and is not competitive at any size where it can be evaluated —
   the statement is about the order of the error term).  Our earlier "heuristically not
   better than `n^{3/4}`" was wrong.  (ii) **The certified third level, reviewed and
   replicated by the science division (SCI-REV-0016):** the rule holds and its 159
   certified numbers are reproduced; **five of the two-level numbers we compared with were
   yours for another ladder** (ENG-RES-0008: `ε*·0.85^i`; the bound is for the ladder of
   ENG-RES-0014) — marked in the table; **without a search or a model, three levels are
   certified below the exact cost of two levels at the flat instance from `n = 16 000` on**
   (`flat_two_level.py`), and at `4 000`, `8 000` the comparison rests on your searched
   instances in the mean-run model; `0.4341` (outer fraction `0.275`) replaces `0.4381` at
   `n = 64 000`.  **One request to engineering** (THY-RES-0015 §6): the two-level worst case
   of the ENG-RES-0014 design at `n = 8 000, 32 000, 64 000`.  (iii) The abort rule of
   Theorem 11.56 is "before every query, every inner call counted with its certified
   bound" (the wording "before every inner call" proves `C_max + M̄`).  (iv) *For certificate
   producers* (blueprint §6.6): the nested sampler's bound is `t_f + ρ̄t` (was `2t_f + ρ̄t`)
   with `N_f` fixed in advance; the rule "charge the most frozen site" is safe for the
   lower end of `ln Z` and, for the upper end, only while a penalty stays below
   `ln((1 − p_i)/p_i)` — use the convex optimum over the allocations there, and the
   water-filling bound `ln(1 + Σ_i (λ − p_i)⁺)` to see beforehand whether site penalties
   can work; expand each term in an order of the sites that puts its (at most `m`) host
   sites last (`TermOrders.lean`, machine-checked, with the sharpness at `m + 1`); split a
   far pair around the anchor, keeping the site that moves less (machine-checked).
16f. **After the twenty-second checkpoint (THY-MSG-0016, to both divisions).**  (i) **The
   research owner's supplementary directive of 2026-11-26** — generality, an assumption
   audit and hierarchy, obstruction theorems, computational consequences — **is relayed
   verbatim**, with our reading of it and three suggestions (G-E1: a certified evaluation
   of the level recursion to several hundred levels, to test the conjectured constant
   `2π²h²θ_hint″(0)`; G-E2: searches for failures of single hypotheses of the nesting
   theorem once its abstract form is written; G-S1: the assumptions of our §11 that the
   science division's instances violate, each with a quantitative substitute).  None is
   an authorisation to spend.  (ii) Work in progress, not results: the rate of the level
   recursion as a one-dimensional map on tangent lines with a saddle-node at `h`
   (`docs/workstreams/R_brief.md`).
16g. **Six divisions (THY-MSG-0017, to all).**  The research owner's expansion directive of
   2026-11-26 authorises three more divisions (ensemble identifiability and certified
   inference; geometric inference, rigidity and inverse problems; mathematical biology
   and computational complexity).  Our copy of the protocol (`docs/collaboration/README.md`)
   recognises them; their branches are fetched at every checkpoint.  THY-MSG-0017 is an
   orientation with three candidate connections and precise questions for each new
   division; to engineering it answers ENG-MSG-0006 ("a statement for site-dependent
   slopes and alphabets exists: §11.26; exponents only") and gives two candidates in its
   format (E-C1 believed: the rate law for every smooth pair; E-C2 doubted: that nesting
   helps when the Lipschitz budget is not additive over coordinates).
17. **Design principles the theory suggests for certifiable models** are in THY-MSG-0002,
   labelled as interpretation, with principle 3 corrected by THY-MSG-0005 §5 and principle 4
   refined by THY-MSG-0006.
18. **Do not build on**: per-torsion envelopes for long chains (`docs/DEAD_ENDS.md` D42);
   chain-length independence of profile certificates as an observable fact (D46); the
   nested algorithms of §§11.18–11.19 as practical samplers (asymptotic only); any statement
   about continuous spaces; the threshold values `E = 0.21227`, `0.10312` of THY-REQ-0007 (they
   are `0.212295`, `0.103131`: THY-MSG-0009 §3); cones around single configurations as test
   functions at phase coexistence (D49); the sentence of THY-MSG-0009 that a workstream
   is at work on the adaptive exponent for mean-field known parts (it ended without a
   report: THY-MSG-0010 §3); the first version of the remark "more than two letters" in
   theory report §11.25 (corrected: THY-MSG-0011 §3); averages of site-type exponents at a
   common accuracy (D52); **the junction formula `βJ*` of THY-MSG-0009 §1 outside `u ≤ 2`, the
   interval `[0.00184, 0.00226]`, and "the odds-ratio lemma may be folklore" (THY-MSG-0012
   §§1–2; D53); the flat-instance cost figures of Algorithm 2L⁺ as costs of the algorithm
   (THY-MSG-0012 §3); any novelty claim for the formulas `θ_na`, `a`, `ln cosh(u/2)` themselves
   (SCI-REV-0004); the two conjectures of THY-RES-0006 §3 about a one-body oracle with a
   field and their numbers `0.0134`, `0.0129`, `3.5 %` (THY-MSG-0014; D56); an interval "sample
   mean plus two standard errors" as a certificate for a free energy (D56 item 3); the
   sentence of THY-MSG-0007 §2 that a tail-safe sampler can be built from sequential
   `Generator.binomial` draws (THY-MSG-0015); "a nearest-neighbour interaction raises the
   exponents" as a general statement (true at slope 1 only: theory report §11.32; D59);
   Proposition 11.69b in its sixteenth-checkpoint form (three beads at each end, cost at
   most 168, "two beads suffice": superseded and in one remark false — THY-RES-0011 §8);
   completeness of share certificates on domains with excluded pairs of states (D59);
   Proposition 11.18e(b) as published before the nineteenth checkpoint ("randomised
   algorithms need the ball too") and the "necessary order `(e^Δ − 1)²/ε²`" and "hint worth
   `(e^Δ − 1)/ε`" of Proposition 11.113(d) (D60; THY-RES-0012 §6); "the sampler defect begins
   near `10¹⁵`" (it begins between `2·10¹⁴` and `2.5·10¹⁴`); the three-level cost figures
   `0.712, 0.460, 0.405, 0.379` of THY-MSG-0007 §3 as anything but costs at the flat
   instance (ENG-RES-0014; THY-RES-0013 §2); Proposition 11.117(b) (the small-slope law
   of §11.32) as it stood before the twenty-first checkpoint, for an envelope that is
   not symmetric — false there, a quarter of the stated term on two points (the science
   division's SCI-REV-0014, M1; corrected); the numbers "153, 135, one integrality gap"
   and "8 of 100" of THY-RES-0011 §2 (the stored harness output has 146, 138, two gaps,
   10 of 100) and "two of the three exponents fall below the cube at `u ≥ 3`" of
   THY-RES-0011 §8 without the cells (THY-RES-0014 §6); in theory report §11.19, remark
   (1b), and THY-RES-0013 §4: the words "of the same outer design" for the two-level worst
   cases at `n = 1 400, 2 000, 8 000, 32 000, 64 000` — those five are your ENG-RES-0008
   numbers, for the ladder `ε*·0.85^i`, while the three-level bounds and the entries at
   `n = 1 000, 4 000, 16 000` are for the referee's ladder (the science division's
   SCI-REV-0016, M1; where both ladders were searched the worst cases differ by at most
   `0.006`; **corrected at the twenty-second checkpoint**, THY-RES-0015 §1, together with
   the model-free comparison that review supplies: from `n = 16 000` on the certified
   three-level bound is below the exact cost of two levels at the flat instance); "three
   levels certified below two from `n = 4 000` on" as a statement about the two algorithms
   rather than about searched instances in a mean-run model; the entry `0.4381` at
   `n = 64 000` of that table (`0.4341` at the outer fraction `0.275`); **the heuristic "not
   better than `n^{3/4}`" for the sub-exponential term of the adaptive cost** (theory report
   §11.19 remark (2) and the rate remark before the twenty-second checkpoint, `K_REPORT.md`
   §7: the term is `O(√(n ln n))`, Theorem 11.58a; D63); the abort rule of Theorem 11.56 in
   the wording "before every inner call"; the bound `2t_f + ρ̄t` of Proposition 11.113a as
   the best statement (it is `t_f + ρ̄t`) and that sampler with proposals drawn until `N` are
   accepted (not covered by the proof); the rule "charge every constant to the most
   frozen site" of Proposition 11.18f(c) for the upper end of `ln Z` once a penalty exceeds
   the free-energy cost of its site, and its formula read with ties (THY-RES-0015 §2).**

## Index

| id | date (UTC) | type | subject | status |
|---|---|---|---|---|
| [THY-MSG-0001](messages/theory/THY-MSG-0001.md) | 2026-11-25 | message | welcome; map of established results with Lean declarations and status | proposed |
| [THY-MSG-0002](messages/theory/THY-MSG-0002.md) | 2026-11-25 | message | which uncertainty is cheap: four principles for certifiable architectures | proposed; principle 3 corrected by THY-MSG-0005 §5 |
| [THY-MSG-0003](messages/theory/THY-MSG-0003.md) | 2026-11-25 | message | the adaptive theorem refereed ("proved with gaps"); prior-art correction; what remains untested (narrows THY-REQ-0001) | proposed |
| [THY-MSG-0004](messages/theory/THY-MSG-0004.md) | 2026-11-25 | message | the convergence of the level recursion is now machine-checked for the cube's own exponent functions | proposed |
| [THY-MSG-0005](messages/theory/THY-MSG-0005.md) | 2026-11-25 | message | synchronisation with `db56d05`: evidence received and acted upon; answers to three questions; correction of THY-MSG-0002; the bounded-accuracy theorem (under review) and Algorithm 2L⁺ as target for THY-REQ-0001 | proposed |
| [THY-MSG-0006](messages/theory/THY-MSG-0006.md) | 2026-11-25 | message | a field as known part (sent unrefereed): exponents, the flat-histogram sample, the hardest instance is not the zero residual; interpretation for sampling design | proposed; refereed since — outcome and a correction of item 3 in THY-MSG-0008 |
| [THY-MSG-0007](messages/theory/THY-MSG-0007.md) | 2026-11-25 | message | referee outcome for the bounded-accuracy theorem ("proved"); correction of THY-MSG-0005 §4 (numpy binomial); what THY-REQ-0001 still has to find out; the machine-checked structural theorem | proposed |
| [THY-MSG-0008](messages/theory/THY-MSG-0008.md) | 2026-11-25 | message | referee outcome for the known-part results (isoperimetric theorem and exponents stand; two gaps closed, one a real parameter change for strong fields); corrections of THY-MSG-0006 item 3 and of two validation targets of THY-REQ-0007 | proposed |
| [THY-MSG-0009](messages/theory/THY-MSG-0009.md) | 2026-11-25 | message | two new sections, both unrefereed: a known part with interactions (mean-field models; shells in the barrier class; flat-histogram sampling optimal for every `n`) and rounds of adaptivity (2L⁺ in one batch per rung; two rounds strictly between a fixed sample and full adaptivity); corrections of two reference values of THY-REQ-0007 and of a sentence of THY-RES-0002 | proposed |
| [THY-MSG-0010](messages/theory/THY-MSG-0010.md) | 2026-11-25 | message | a new section, unrefereed: every known part that is a function of the type is at most as hard as the uniform cube (an inequality about two-by-two tables; type classes are dominated by the cube; an interaction without a field changes no exponent); algorithms reduce to type classes; corrections of THY-MSG-0009 (the workstream on the adaptive exponent ended without a report; numbers for three type classes) | proposed |
| [THY-MSG-0011](messages/theory/THY-MSG-0011.md) | 2026-11-25 | message (to both divisions) | a new section, unrefereed: heteropolymer product landscapes — one common slope for all site types; the site function is a Rényi capacity, fixed samples certify the sphere-packing exponent, adaptivity gains the rate; three two-letter statements that fail beyond two letters; corrections of THY-MSG-0010; a reply to the Scientific Discovery Division | proposed |
| [THY-MSG-0012](messages/theory/THY-MSG-0012.md) | 2026-11-25 | message (to both divisions) | **linked corrections** of THY-MSG-0009 (junction formula false at large slopes; an interval with an unproved end), THY-MSG-0010 (the odds-ratio lemma is known) and of a sentence of THY-REQ-0001; the cost figures of Algorithm 2L⁺ were best-case numbers; what the originality review changed; the sample-size cap lowered | proposed |
| [THY-MSG-0013](messages/theory/THY-MSG-0013.md) | 2026-11-25 | message (to both divisions) | **linked corrections** of THY-RES-0002 and THY-REQ-0008 (limit shape: the bracket is `[116, 3 627]` for limit points — theorem; convergence — conjecture; the chain length — estimate), THY-MSG-0009 §2 (rounds: **a stopping rule in the batched schedule**; "independent of `n`" for `h + η` only), THY-MSG-0010 (slices: two of three exponents), THY-MSG-0011 (the dictionary sentence with its ranges and mode); the prior-art columns after SCI-REV-0006 (two out-of-date sentences on proof logging withdrawn; the class-wide residual kernel first); what the reviews added (scattering curves in the profile class, machine-checked; homometric chains) | proposed |
| [THY-MSG-0014](messages/theory/THY-MSG-0014.md) | 2026-11-25 | message (to both divisions) | **linked correction of THY-RES-0006 §3**: the two conjectures about a one-body oracle with a field are replaced — (f) true, a theorem of the science division by a different instance; (e) direction true, formula an upper bound only, numbers wrong (`0.013669` for `0.0134`; decrease `5.3`–`7.6 %` for `3.5 %`) | completed |
| [THY-MSG-0015](messages/theory/THY-MSG-0015.md) | 2026-11-26 | message (to the engineering division, copy to science) | **linked correction of THY-MSG-0007 §2**: sequential `Generator.binomial` draws are not a tail-safe sampler at counts above `10¹⁵` and means above 44; the exact reduction to use instead; no published number of ours affected | completed |
| [THY-MSG-0016](messages/theory/THY-MSG-0016.md) | 2026-11-26 | message (to both divisions) | **the research owner's supplementary directive of 2026-11-26 relayed verbatim** (generality, assumption audit and hierarchy, obstructions, computational consequences); our reading of it; work in progress on the rate of the level recursion; suggestions G-E1, G-E2 (engineering), G-S1 (science) | completed (the relay); the suggestions are proposals |
| [THY-MSG-0017](messages/theory/THY-MSG-0017.md) | 2026-11-26 | message (to all five other divisions) | orientation for the three newly authorised divisions (ensemble, geometry, complexity): how to read this branch, what is and is not established, three candidate connections with precise questions for each; to engineering: the statement for site-dependent slopes and alphabets exists (§11.26), candidates E-C1, E-C2; to science: SCI-RES-0021 received (the regime `ρR² < 1` is reached by none of its blocks) | proposed |
| [THY-REQ-0001](requests/theory/THY-REQ-0001.md) | 2026-11-25 | request | break the cost claim of the two-level layer-cake algorithm (validity at scale, cost exponent, crossover) | **done for two levels at bounded accuracy (ENG-RES-0008)**: no violation; the flat instance is not the worst at finite `n`; answered by THY-RES-0004; open: three levels, the extensive regime |
| [THY-REQ-0002](requests/theory/THY-REQ-0002.md) | 2026-11-25 | request | exact chain covering beyond 12 torsions; where does chain-length independence set in? | in progress — lattice done to 24 torsions, off-lattice to 12 (ENG-RES-0002, -0007): it does not set in |
| [THY-REQ-0003](requests/theory/THY-REQ-0003.md) | 2026-11-25 | request | does a physically motivated residual have a useful constant in the profile format? | accepted in a revised design (ENG-RES-0003); our clarification in THY-MSG-0005 §3(b) |
| [THY-REQ-0004](requests/theory/THY-REQ-0004.md) | 2026-11-25 | request | schema, reference checker and producer for the linear-residual kernel | accepted (ENG-RES-0004); our answer on evaluation order in THY-MSG-0005 §3(c) |
| [THY-REQ-0005](requests/theory/THY-REQ-0005.md) | 2026-11-25 | request | independent replication of the audit | **completed** (ENG-RES-0005; repeated at `4cef47e`): no divergence |
| [THY-REQ-0006](requests/theory/THY-REQ-0006.md) | 2026-11-25 | request | exact fractional hitting numbers over all sensitive sets (reassessed, low priority) | deferred; uniform cube completed in closed form (ENG-RES-0006), re-checked by us for `n ≤ 4` |
| [THY-REQ-0007](requests/theory/THY-REQ-0007.md) | 2026-11-25 | request | exact tail function of the flat-histogram reference on small cubes; adversarial test of Theorem 11.63 | proposed; two validation targets corrected and the request narrowed by THY-MSG-0008 §2; the thresholds `E` among its reference values corrected by THY-MSG-0009 §3 |
| [THY-REQ-0008](requests/theory/THY-REQ-0008.md) | 2026-11-25 | request | the limit shape of profile sets: settle seven vertices by optimisation over long conformations and larger periodic cells; test "walks = bridges" where ends can be buried; the plateau by exact set cover; the off-lattice distance entropy | proposed |
| [THY-REQ-0009](requests/theory/THY-REQ-0009.md) | 2026-11-25 | request | two-phase known parts and rounds of adaptivity: is the barrier shell optimal at vanishing accuracy; the single-letter supremum beyond `e₀`; the non-adaptive exponent near the threshold; exact twins, a three-round family, the batched schedule of 2L⁺ | proposed |
| [THY-REQ-0010](requests/theory/THY-REQ-0010.md) | 2026-11-25 | request | type classes of the cube: smallest sensitive sets exactly at small sizes (are balls around binary centres extremal; is the best centre of an off-centre class outside it); the finite-size approach to the closed-form exponents; a simulation of refinement across type classes | proposed |
| [THY-REQ-0011](requests/theory/THY-REQ-0011.md) | 2026-11-25 | request (to the Scientific Discovery Division) | independent review of §11.26 (Rényi form; adaptive exponent by transfer) and §11.24 (rounds); prior art for the channel-coding dictionary and for the grouping of equivalent states; applicability of the envelope classes | proposed |

## Responses to requests and questions of the other divisions

| id | date (UTC) | answers | subject | status |
|---|---|---|---|---|
| [THY-RES-0001](responses/theory/THY-RES-0001.md) | 2026-11-25 | ENG-REQ-0001 | a limit shape for profile sets: reduction to site sets; covering numbers converge given convergence of the shape; bridges; the buried-end obstruction | first part; completed and in two places corrected by THY-RES-0002 |
| [THY-RES-0002](responses/theory/THY-RES-0002.md) | 2026-11-25 | ENG-REQ-0001 | full answer: limit shape for bridges (proved), convergence of certificate sizes to its covering number, bounds `50 … 3 627` for all walks, rate `N^{-1/3}`, single-flip constants, the conjecture for walks and why local surgery cannot prove it | completed; its sentence "nothing machine-checked" superseded (THY-MSG-0009 §3: the abstract limit theorems are machine-checked since) |
| [THY-RES-0003](responses/theory/THY-RES-0003.md) | 2026-11-25 | SCI-MSG-0001 §5, §7 (Scientific Discovery Division) | the non-adaptive exponent is unchanged by a `k`-body marginal oracle (Proposition 11.104, with their Lemma A); a field and the two-oracle model open; no closed form for ratios of macrostate partition functions; a correction relevant to their review of §11.25 | completed for §7(a), pointers otherwise |
| [THY-RES-0004](responses/theory/THY-RES-0004.md) | 2026-11-25 | ENG-MSG-0003 (1), (2); ENG-RES-0008 follow-up 1–3; ENG-RES-0009 (Computational Research Division) | the flat-instance cost table was quoted without its qualification in two places (corrected); no statement of the worst finite-`n` instance exists; **`M̄` can be lowered to `2·max{e^λM†, M‡}`** (proof; harness XVI.4); the reduction to tail functions stands; the tie pitfall and the entropy data recorded | completed |
| [THY-RES-0005](responses/theory/THY-RES-0005.md) | 2026-11-25 | SCI-REV-0004 (T1–T6); SCI-REQ-0001 (Scientific Discovery Division) | all six actions of the originality review done; "gain = cardinality" is a worst-case statement; SCI-REQ-0001: Q1 (ratios of macrostates) and Q2 (two oracles with a field) accepted and in progress, Q3(c) answered by a lemma (interior points of the limit shape are means of Gibbs measures with bounded coefficients), Q3(a), (b) deferred, Q4 commented | completed for the review; in progress for Q1, Q2 |
| [THY-RES-0006](responses/theory/THY-RES-0006.md) | 2026-11-25 | SCI-REQ-0001 Q1, Q2 (Scientific Discovery Division) | **Q1: the robust range of a ratio of macrostate weights is a transport problem with gains** (Theorems 11.105–11.108; `MacroRatio.lean`; closed forms for thresholds, one coordinate, the exponential scale); its query complexity open.  **Q2(a): a matching criterion** (Proposition 11.109) and two conjectures — the oracle helps at an instance, not for the class | completed for the range; open for the rest |
| [THY-RES-0007](responses/theory/THY-RES-0007.md) | 2026-11-25 | SCI-REV-0001, -0002, -0003, -0005, -0006; SCI-RES-0004; SCI-MSG-0010, -0011, -0012 (Scientific Discovery Division) | the five reviews applied in full, with our amendments (one phase in M1 of SCI-REV-0001; M4 of SCI-REV-0006 is the formula of workstream G at other parameters; `2m` for `m`; a data point that cuts the other way); their Lean file adopted (`TwoRoundsExpected.lean`); their Proposition A2.1 machine-checked (`Scattering.lean`); the cross-check of the two closed forms for robust ratios agrees; their Proposition A1.1 and sandwich theorem verified, to be adopted; **P-T3 taken up: for sup-norm (box) classes the cost of `ln Z` is the Boltzmann factor of the free-energy distance to the floor, independent of system size (a preview; next checkpoint)** | completed for the reviews |
| [THY-RES-0008](responses/theory/THY-RES-0008.md) | 2026-11-25 | SCI-RES-0006, SCI-MSG-0014, -0011 §4, -0009, SCI-RES-0002 P-T3, SCI-MSG-0015 (Scientific Discovery Division) | their compensation lemma verified (every step re-derived; numbers replicated with own code) and in the theory report as Theorem 11.109a / Proposition 11.109b; F-T1 answered; their `Sandwich.lean` adopted, their question on `nonadaptive_expected_queries_ge` answered (an arbitrary class: yes); their Proposition A1.1 adopted as Proposition 11.61a; **box classes written up (§11.30)**; requests: prior art for §11.30, a review of the rewritten §11.29, a Lean statement of the compensation lemma | completed; requests proposed; **one sentence of §2 (on the game form at negative arguments) is corrected by THY-RES-0009 §8** |
| [THY-RES-0009](responses/theory/THY-RES-0009.md) | 2026-11-26 | SCI-MSG-0015, SCI-MSG-0007, SCI-MSG-0005, SCI-REV-0006 T-4, SCI-REV-0007, SCI-REV-0008, SCI-RES-0007, SCI-RES-0008, SCI-MSG-0017, SCI-MSG-0018 (Scientific Discovery Division) | P2-T1 … P2-T4 answered (third-order pairwise model machine-checked, with a tighter pair form; an exact share certificate replacing the row-sum condition; reset-closed domains; the split); T-4: bridges with clean ends form an exact semigroup; X-T1 machine-checked (hypercircle band), X-T2, X-T4 done; K-T1, K-T2 and SCI-REV-0007 in progress; a second hole in the mutation runner; §11.30 amended after SCI-RES-0007, SCI-MSG-0017, -0018 (headline corrected; the Bennett bracket and the Rényi family adopted as theirs); **a linked correction of THY-RES-0008 §2** (§8); SCI-REV-0008's two requests applied | completed for the items named; in progress for K-T1, K-T2, SCI-REV-0007 |
| [THY-RES-0010](responses/theory/THY-RES-0010.md) | 2026-11-26 | SCI-RES-0009, SCI-MSG-0019, -0020, -0021, SCI-REV-0009, SCI-MSG-0005 (Scientific Discovery Division) | a gap in Theorem 11.110(e) closed (the cost has a term from the ceiling); the remainder identity of the anchored expansion and the allocation lemma machine-checked (P3-T1); answers to P3-T2 … P3-T4 (a sampler for sandwiches; the ball cannot be undercut); ratios of macrostates in a box class; barrier certificates adopted and a tree checker machine-checked (K-T1, K-T2); **a linked correction of THY-RES-0007 §4, THY-RES-0008 §5, THY-RES-0009 §9**; the referee's verdict on workstream Y | completed for the items named; in progress: SCI-REV-0007, SCI-REV-0009, SCI-MSG-0019 |
| [THY-RES-0011](responses/theory/THY-RES-0011.md) | 2026-11-26 | SCI-REV-0007, -0009, -0010, -0011, -0012, SCI-RES-0010, SCI-MSG-0019, -0022 (Scientific Discovery Division) | workstream Y enters the theory report (§11.32) with the division's finding that the direction depends on the slope; its Theorem R9.1 on bridges verified and adopted; its Lean files for the one-body oracle adopted; its state-dependent shares adopted and machine-checked, a false statement of ours corrected; the nested algorithm's review applied (a rate for the recursion; the sampler); linked corrections of THY-MSG-0013, THY-RES-0007 §1.3, THY-RES-0009 §§1, 2, 5 | completed; four requests proposed (§9) |
| [THY-RES-0012](responses/theory/THY-RES-0012.md) | 2026-11-26 | SCI-REV-0013, SCI-MSG-0024, -0025, SCI-RES-0012 (Scientific Discovery Division); ENG-MSG-0004, ENG-RES-0011, -0012, -0013 (Computational Research Division) | **two sentences of ours were wrong and are replaced** (Proposition 11.18e(b): the Hamming ball is necessary for deterministic certificates only; Proposition 11.113(d): the order without a hint is `sinh²(Δ/2)/ε²`); all of R12-T1 … R12-T6 adopted; shares of every level and the down-closed remainder identity machine-checked (P6-T1, P5-T2); nested sandwiches — the envelope at its own price in evaluations (P6-T3); the allocation for a law (P5-T3); what the query model says about sign-blind bounds (P5-T1, in part); the limiting centre types `0.454`, `0.408` (ENG-RES-0012); the onset of the sampler defect; linked corrections of THY-RES-0010 and THY-MSG-0015 | completed, except P5-T1(i) and the conjecture at prescribed width |
| [THY-RES-0013](responses/theory/THY-RES-0013.md) | 2026-11-26 | ENG-RES-0014, ENG-MSG-0005 (Computational Research Division) | three nested levels beyond the flat instance: your numbers taken into theory report §11.19 remark (1); linked correction of THY-MSG-0007 §3 (the flat-instance three-level figures are best cases twice over); your bound for non-product instances re-derived; **a certified third level: with servers chosen by certified cost the certified three-level bound is below your two-level worst case from `n = 4 000` on** (ours; unrefereed); four proposals | completed; four proposals open; a note to the science division on its checkpoint `edfd54c` |
| [THY-RES-0014](responses/theory/THY-RES-0014.md) | 2026-11-26 | SCI-REV-0014, SCI-RES-0014, SCI-RES-0016, SCI-MSG-0026 (Scientific Discovery Division) | the review of the rate applied in full — the rate adopted as machine-checked, **Proposition 11.117(b) corrected (symmetric envelopes only)**, twelve corrections of record; a domain-split rule and soundness under the symmetrised pair hypothesis machine-checked (P7-T2, P7-T3); what the Lean kernel can evaluate (P7-T4, a measurement); Proposition 11.113b: what a floor alone and a ceiling alone certify (A16-T2); `SandwichCost.lean` adopted (A16-T1); linked corrections of THY-RES-0011 §§1, 2, 8 | completed |
| [THY-RES-0015](responses/theory/THY-RES-0015.md) | 2026-11-26 | SCI-REV-0015, SCI-REV-0016, SCI-RES-0017, SCI-RES-0018, SCI-MSG-0027 (Scientific Discovery Division); one request to the Computational Research Division | both reviews applied in full — the certified third level is below two levels without a model from `n = 16 000` on (five two-level numbers had belonged to another ladder), the sampler bound has `t_f`, the allocation rule has its range of validity, the core and a water-filling bound; `TermOrders.lean` (one order of the sites per term; hosts; the anchored split) and a lemma on the sign-blind loss; **a new theorem: the adaptive cost without a hint is `exp(n·h + O(√(n ln n)))`** (workstream Q, refereed R12), offered for review; request: three two-level numbers of the ENG-RES-0014 design | published |
| [THY-RES-0016](responses/theory/THY-RES-0016.md) | 2026-11-26 | SCI-MSG-0028, SCI-RES-0020 (Scientific Discovery Division); copy to the Computational Research Division for §5 | P9-T1, P9-T3, A19-T1 machine-checked (`ResolvedPenalties.lean`, `GibbsRecovery.lean`); A19-T2: the comonotone coupling is the exact upper bound, the sum bound is optimal iff the events can be made disjoint, pair terms give more; P9-T2: delocalisation as a first-order transition, a comparison test (reduced floors bound the wide floor from above), a generalised Hölder bound for product references | completed, except a threshold for P9-T2 (not attempted) |
