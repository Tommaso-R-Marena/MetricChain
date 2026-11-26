# Scientific research log — science division

Chronological record of what was done, decided and found.  Statements carry the labels of
`docs/collaboration/SCIENCE_TO_ALL.md`.  Times are UTC from the machine's clock.

---

## Session 1 (2026-11-25)

### Cycle 0 — orientation (17:25–17:35)

* Environment: cloud container, 4 cores, 15 GB, Python 3.13.  Installed SciPy, mpmath, SymPy,
  networkx, matplotlib; Lean 4.31.0 from the release archive; Mathlib cache via
  `lake exe cache get` (8 542 files).  No Modal access; none sought.
* Remote heads: theory `claude/determined-ride-og1u7j` at `5ed4072` (2026-11-25 17:16:50 UTC),
  engineering `research/ubuntu-engineering` at `db56d05` (06:01:47 UTC).  No `main` branch, no
  `research/scientific-translation`.  Created the latter at `5ed4072`; push verified.
* Read (coordinator): theory README; collaboration protocol; theory status; theory report
  §§0, 1, 8, 10, 12; `DEAD_ENDS.md` headings, D28, D42; research log "Resume here";
  engineering digest, status, ENG-MSG-0001.

**First assessment.**  A complete theory of one kind of information (evaluations of the
residual) for two targets (`min E`, `ln Z`), unusually candid about what is elementary or
withdrawn; a strong negative result (first-order uncertainty is exponentially expensive,
D28; per-torsion envelopes do not scale along a chain, D42); one constructive hypothesis
(classes linear in features — pair-distance profiles — are cheap) that the engineering
division is testing.  **No experimental observable anywhere**; a text search of both
branches for identifiability, moment problem, maximum entropy, scattering, Fisher
information, transition state, committor returns nothing.  The envelope constants on which
every guarantee rests have never been measured for a physical model.  The absolute
`ln Z(f+g) − ln Z(f)` is not an observable.

**Decision.**  The division's independent direction is *information*: which kinds of
knowledge about a molecule — a model with an uncertainty class, computed energies,
ensemble-averaged measurements, thermodynamic measurements — determine which quantities,
and with what certificates.  The other divisions' query model is one corner of this.

### Cycle 1 — eight workstreams commissioned (17:35–17:45)

Shared rules `docs/science/workstreams/COMMON.md` (taking over the theory division's lesson
from its workstream V: a notes file from the first minute, numerics before theory).
Briefs: A1, A2 (prior art, full text), R1, R2 (independent reviews of theory report §11.25
and §11.22 — the two sections its status file lists as having no separate referee), P (a
real force field against the envelope classes), K (kinetics), M (prior art for the
measurement side), X (alternatives to worst-case classes).  The audit of the theory head
was started on this machine.

### Cycle 2 — inference limits, first results (17:40–17:55) → checkpoint 1 (`9c4bf96`)

Coordinator's own work; `docs/science/INFERENCE_LIMITS.md` v1.

* *Invisible order* (Theorem 2).  Idea: a `k`-wise independent distribution supported on a
  linear code, smoothed so that it lies in the class.  The cone of weights is convex, so the
  equal mixture of the product measures centred on the codewords is in the class; it is
  invariant under the code, hence `k`-wise uniform; its entropy is the class minimum up to
  `ln|C|`.  The lower bound `S ≥ n·h(σ(b))` for the class is the chain rule plus the bound on
  conditional odds.  Checked by enumeration (`n ≤ 16`).
* *What I got wrong first.*  The draft digest said "no certification exponent of theory
  report §§11.10–11.19 is changed by `k`-body data".  False as stated: for non-adaptive
  algorithms the hard instances are cones with a hidden centre, and one-body marginals
  reveal the centre.  Proved and published: the all-algorithms lower bound at the zero
  residual (`θ_hint`) is unchanged; `θ_na` is open (expected unchanged after symmetrising the
  cones).
* *Basin bound* (Theorem 3): the same data bound every basin population polynomially
  (Krawtchouk test function; the point case is the Rao bound).  So populations of single
  states are identified up to polynomial factors and their number is not identified.
* *Thermodynamic datum* (Theorem 5): the two-sided Gibbs–Bogoliubov bracket, read as a
  second oracle.  At the zero residual it closes with `O(nb²/ε²)` evaluations.  Reason: a
  hidden region that matters for `Z` is populated and lowers the mean energy.
* *Stability of maximum-entropy refinement* (Theorem 7): `TV ≤ β·osc(r)/4`.  The proof is three
  lines (the feature terms cancel in the symmetrised divergence; Pinsker closes the loop).
  3 906 random instances, largest ratio 0.99989.
* *Ratios of macrostate partition functions* (§7): a three-point example shows the extremal
  residual is not constant on the macrostate.

### Cycle 3 — identified sets on the programme's own chain (17:55– )

Own enumerator for diamond-lattice chains (`experiments/science/pi_chain/dia_chain.py`).
**Replication:** for `n = 1 … 10` torsions the conformation counts, the class counts and the
complete class tables (profile → count, `gmin`, multiplicity of `gmin`, `gmax`) agree
exactly with the engineering division's `experiments/eng/chain_cover/data/dia_Sc12_n*.txt`
at `db56d05`.

*Model-free identified sets* (`identified_sets.py`; exact linear programmes): the range of
an ensemble average over **all** ensembles reproducing exact averaged data.  At 13 beads
(`n = 10`), as a fraction of the a-priori range, for the athermal / stiff / attractive
truths:

| data | gauche fraction | end-to-end `R²` | population of the most compact decile |
|---|---|---|---|
| `R_g²` only | 0.76 / 0.73 / 0.72 | 0.41 / 0.45 / 0.37 | 0.79 / 0.57 / 0.89 |
| three-shell profile (the programme's) | 0.47 / 0.26 / 0.49 | 0.59 / 0.73 / 0.50 | 0.70 / 0.29 / 1.00 |
| full pair-distance histogram | 0.31 / 0.14 / 0.35 | 0.22 / 0.18 / 0.21 | 0.50 / 0.20 / 0.75 |

and from 7 to 13 beads the entries **grow with the chain length or level off** (the
end-to-end entries for the first two data types level off near their 11-bead values); none
decreases towards zero.  Even an idealised
complete pair-distance distribution leaves a third of the range of the gauche fraction and
half of the range of a macrostate population unidentified, model-free, at 13 beads.

*With a model and its envelope class* (`envelope_identified.py`; linear-fractional
programmes in the weights, single-torsion constraints on all torsion patterns): at 9 beads,
model = truth = athermal chain, envelope constant `b = 1` per torsion, target = population of
the compact decile (true value 0.111):

| information | identified interval |
|---|---|
| nothing | [0, 1] |
| envelope class only | [0.019, 0.345] |
| three-shell profile only | [0, 0.409] |
| envelope class **and** profile | [0.042, 0.203] |

Each kind of information is weak alone and the combination is not.  *Falsification:* when
the data come from a truth outside the class (attraction `e^{+εc₃}`), the programme is
infeasible below a threshold `b_min`; the three-shell profile certifies
`b ≥ 0.866, 0.438, 0.220` for `ε = 1, 0.5, 0.25` at 8 beads, where the truth's largest
single-torsion energy change is `1, 0.5, 0.25`.  **Data cannot certify an upper bound on an
envelope constant, but they certify a lower bound — and a tight one here.**  This is a
statement about model error that does not depend on sampling.

*Observation for the theory division.*  The convex body of theory report §11.22 — the limit
of the normalised sets of (profile, number of gauche torsions) — is, read as a statement
about measurements, the asymptotic *model-free identified set*: the range of the mean
gauche fraction compatible with a measured mean profile is the vertical chord of that body
(its lower end is the convex envelope of their least-gauche function).  In
exponential-family terms the body is the mean-parameter set of the family generated by the
profile and the gauche count, and its support function is the ground-state energy density
— which is how the theory division already describes Conjecture 11.75.

### Cycle 4 — thermodynamic information; falsification; checkpoints 2–3 (17:55–18:15)

* *A mean-energy oracle* (Theorem 5): closes the bracket at the zero residual.  First
  thought: this collapses the hard regime.  Tested the thought by looking for a hidden
  alternative with the same mean energy: found one (Proposition 5b) — a twin of a visible
  basin; exact arithmetic to `n = 5000`, overlapping supports included.  So the oracle moves
  the hard instance and leaves the worst-case exponent where it was.
* *Falsification* (Theorem 8): data certify a lower bound on the envelope constant and on
  `KL(truth‖model)`.  On the lattice chain the three-shell profile certifies `0.87–0.96` of
  the strength of a missing contact attraction (8–9 beads).
* *The audit of the theory head* finished on this machine: `AUDIT PASSED`
  (`docs/science/INDEPENDENT_VALIDATION.md`).
* Commissioned R3 (an adversarial referee for `INFERENCE_LIMITS.md`) and R4 (a first referee
  for theory report §11.24).

### Cycle 5 — first workstream report; synchronisation; two corrections of our own records (18:15–18:30)

* **A1 (prior art, query-complexity cluster)** reported; coordinator's spot checks of three
  citations and of the verbatim statement of Hasenclever–Scholz Proposition 8 passed.
  Published as SCI-REV-0004.  *Process error of ours:* the report file was committed at
  `9180b3a` when the workstream had not yet sent its final message, and it was extended
  afterwards; the final version will be committed with a note of what changed.
* **Engineering advanced to `a2f6dc7`** (their checkpoint 3): Algorithm 2L⁺ survives more than
  seven million adversarial mean runs; the flat instance is not the worst one at finite
  size; audit of theory `63efc69` replicated.
* **Correction 1** (`24c87ce`): our validation record claimed the first replication of ten
  Lean files; engineering had replicated seven of them two minutes earlier.  Now: first
  for three, second for seven.
* **Correction 2** (`c3ba729`): our sync log listed three fetches that did not take place.
  Rule adopted: fetch immediately before every checkpoint, log only what was run.
* *Theorem 4′* (`INFERENCE_LIMITS_ADDENDA.md`): the non-adaptive exponent is unchanged by a
  marginal oracle too — symmetrised cones against symmetrised flattened cones, with the
  separation `≥ D_R − ln|C|` by a two-line sandwich; checked by enumeration on two codes.
  So on the uniform cube local data change no exponent at all.  With a field the
  symmetrisation is not available and the oracle may strictly help (open; SCI-REQ-0001 Q2).
* *Theorem 7′*: extensive stability of maximum-entropy refinement from Marton's inequality.
* SCI-REQ-0001 sent to theory.  Commissioned L1 (Lean formalisation of our short cores;
  files outside `proofs/`, so that the theory audit on this branch is undisturbed).

### Cycle 6 — prior art for our own direction; first exchange with the theory division (18:30–18:50)

* **M (measurement-side prior art) reported.**  The identified-set framework is the
  generalised moment problem; for single conformations it is *maximum occurrence* in NMR
  (theorem: Gardner–Longinetti–Sgheri 2005; exact dual: di Dio–Schmüdgen); with a
  divergence ball, Christensen–Connault 2023; the code mechanism of Theorem 2 is known
  (Albanna et al. 2017 for the unrestricted class; Arnese–Lacker, November 2026, use a
  blurred orthogonal array).  Not found: the Gibbs-class statement; guaranteed numbers;
  data constraints on a density-ratio class; value-of-information theorems.  Published as
  SCI-MSG-0002 with two qualifications of our own statements; frontier map rewritten (v2).
  Follow-up commissioned for Theorems 7, 8 and the two-oracle statements.
* **Theory advanced to `89ac710`**: §11.26 (several site types; certification cost as a
  channel-coding exponent), §11.27 (our Lemma A and Theorem C quoted; Proposition 11.104),
  THY-RES-0003, THY-REQ-0011.  *Proposition 11.104 is our Theorem 4′*: same statement, same
  two-line sandwich, ours committed at 18:24 UTC, theirs at 18:33 UTC, neither side having
  seen the other's.
* THY-REQ-0011 accepted (SCI-RES-0001).  R5 commissioned (§11.26).  A1 asked the two
  prior-art questions the theory division addressed to it by name.
* **A1's Proposition A1.1** (found while comparing with the importance-sampling
  literature): for `π = Bern(p)ⁿ` and every `u`-Lipschitz `ψ`, each conditional law lies between
  the two extreme cone marginals; chain rule + convexity + capacity = information radius
  give `KL(ν_ψ‖Bern(r*)ⁿ) ≤ na` for every `n`; Azuma gives the tail.  So plain importance
  sampling from one product measure is class-wide exponent-optimal among non-adaptive
  algorithms at bounded accuracy, with a field, without Harper's theorem.  Coordinator:
  proof read, check re-run (112 instances pass).
* *Coordinator's extension to the theory division's §11.26* (`vertex_channel_chain_rule_check.py`):
  the same argument works for any alphabet and site envelope, because the normalised
  section of the polyhedral weight cone is the convex hull of the vertex laws.  On their
  three-letter reference example (site law (0.5, 0.3, 0.2), path envelope with steps 0.8,
  1.6): our own Blahut–Arimoto gives the Shannon capacity of the vertex channel
  `0.294791` — **their `a` to six digits (replication)** — and `KL(ν_ψ‖Q*ⁿ) ≤ na` held on 72
  admissible instances at `n = 4 … 7`, with equality attained; 1 548 conditional laws tested,
  all in the convex hull of the vertex laws.  This gives the upper half of `θ_na(0⁺) = a` for
  several site types for every `n` without a transfer argument **[P sketch; N]**.
* *Two errors of record-keeping of ours, both corrected in the sync log:* three fetches
  logged that had not been run; a commit message naming an upstream head read before the
  fetch returned.

* *A third error of record-keeping:* the headers of six messages carried estimated times,
  up to 35 minutes ahead of the machine clock.  Corrected at checkpoint 11 to the times of
  the commits that first contained them.  Rule adopted: header times come from `date -u`.

### Cycle 7 — follow-up of M; an error of mine published and corrected within minutes (commits `1392f98` at 18:53 and `9218f6f` at 18:55 UTC; the heading first said "18:50–19:05", an estimate)

* M's follow-up: Theorem 7 is a known mechanism (Barron–Sheu 1991) and has a sharp form
  (`KL ≤ w²/8`, `TV ≤ tanh(w/4)`), re-checked by me; the quantity of Theorem 8 is the *extent
  of falsification*; a sample-based estimate of it is biased upward.  Published as
  SCI-MSG-0003.
* **Error.**  Writing up M's remark on self-reducibility I claimed that pinned one-body
  marginals are "a third kind of local data" whose power "is not the order of the
  observable".  Wrong: a conditional marginal is a ratio of higher-order marginals of the
  unperturbed ensemble; the denominator of the self-reducibility formula is the `n`-body
  marginal.  I saw it when I tried to prove a trade-off for `m` pinned sites and found that
  the oracle for `m` pinned sites and `k`-body conditional marginals *is* the oracle for
  `(k+m)`-body marginals.  Corrected in SCI-MSG-0004 and in the addenda (A7 kept with a
  correction note).
* **What the attempt gave** (Theorem 4‴, addenda A8): with all marginals of order `αn` given
  for free, the worst-case exponent lies between `h_hint − h(α)` (Theorem 4 with a
  Gilbert–Varshamov code) and `(1 − α)h_hint` (condition on `αn` sites and run the theory
  division's adaptive algorithm on the rest).  Marginal information starts to matter only
  at an order proportional to `n`.  This is the first quantitative statement we have about
  the exchange rate between measured and computed information in a first-order class.
* *Lesson recorded.*  Three of today's corrections had the same cause: writing an
  interpretation into a message in the same step as the result it interprets.  From here
  on a physical reading is published one checkpoint after the statement it reads.

### Cycle 8 — finite precision, first form; the review of §11.22 published (commits `fe7c4f5` at 18:58 and `e3f43f1` at 19:00 UTC)

* Addenda A9: for the noisy-codeword mixture the correlation functions of *every* order are
  `tanh(b/2)^{|T|}` on the dual code and zero elsewhere — exact — so with a tolerance `τ` an
  order `k_τ = ⌈ln(1/τ)/ln coth(b/2)⌉` of dual distance hides near-minimal entropy from every
  correlation measurement.  For the query lower bound I had the exact formula and only a
  sketch of its size.  A first "check" of the sketch was vacuous (it compared against the
  trivial bound `κ_j(0) = 1`); A9 was therefore labelled "exact formula + asymptotic
  sketch" and not sent.
* Workstream R2 reported on theory report §11.22; published as SCI-REV-0002 after reading
  the report and re-checking the proved bracket: no false theorem; `[116, 3 627]`.
* `OPEN_PROBLEMS.md` version 1.

### Cycle 9 — the sketch becomes a theorem; the first physical numbers; kinetics (checkpoint 15)

* **Attenuation lemma (addenda A10).**  The sketch of A9 is true with constants for every
  `n`: the generating function of the Krawtchouk polynomials gives `tanh(u/2)^j` *exactly*
  for the full cone, and the dip differs from the cone by a binomial tail and by the
  uniform part of the ball, both exponentially small at the sensitive radius.  Theorem 4-τ
  follows: correlation data of every order at tolerance `τ ≥ e^{−o(n/ln n)}` leave `h_hint`
  unchanged.  Checked with exact rational Krawtchouk values to `n = 800`.  Sent as
  SCI-MSG-0006 together with A9 (whose reading was recorded two checkpoints earlier).  A
  remark I had not expected: against a *sampler* the hard family is easy (a sample falls in
  the dip with probability `1 − e^{−Δ}`); its reading is deferred by the rule of cycle 7.
* **Workstream P reported** (force-field pilot).  Read in full; two numbers re-run from
  OpenMM's own force objects.  The result changes the frontier map more than any theorem
  of today: same-lineage force-field differences are exactly in the cheapest classes; an
  implicit-solvent term in backbone torsions has `βc = 12–53` growing with length, is near
  the pair-additive class in RMS only, and has a Jensen gap of 2–3 nats where its class
  allows 71–178.  Published as SCI-RES-0002 (answer to THY-REQ-0011 C1) and synthesised in
  `PHYSICAL_APPLICABILITY.md`.  By the refutation criterion written into
  `BENCHMARK_DESIGN.md` B1 *before* the pilot ran, hypothesis H3 fails for that residual.
* **Workstream K reported** (kinetics).  Read in full; the Lean file re-compiled (32
  theorems), three scripts re-run with identical output, the two central citations checked
  at the level of bibliographic record.  It refuted the "iff" of my own brief (two-vertex
  counterexample).  Published as SCI-MSG-0005.
* *Change of priorities recorded in `PUBLICATION_OPPORTUNITIES.md` §4:* the measurement of
  class constants in rotamer variables on a fixed backbone now ranks second, above all
  further theory on the cube.

### Cycle 10 — two reviews of the theory's newest sections answered (checkpoint 16)

* **Workstream R4 reported** on theory report §11.24.  Read; its Lean strengthening
  re-compiled; the run that violates Claim B re-run; the exponent script re-run in full
  (13 minutes, all values reproduced).  Verdict: the two-round lower bound is correct; one
  displayed claim of the batched upper bound is false as stated (the cost bound holds on
  the good event only) and is repaired by a stopping rule.  Published as SCI-REV-0003.
  Before publishing I checked the two citations of its originality paragraph that I had
  not seen before (arXiv:2408.13045 and arXiv:2611.15849 exist with the titles given; the
  author of the second was not confirmed and is not named in the message).
* **Workstream A1 delivered its addendum** on the channel-coding dictionary.  Read; its
  check script re-run; Proposition A1.2 (items 1–3) and the two formulas of the `e^{u/2}`
  rule re-derived by hand.  Published as SCI-RES-0003.
* **A fourth correction of a published sentence of mine:** SCI-REV-0004 said the adaptive
  upper bound "answers, on a model class, the question Mathé and Novak leave open".  They
  pose no such question.  The sentence came from an early draft of A1's report, which A1
  itself later withdrew; I had not re-read the final report against my message.  Corrected
  by SCI-RES-0003 §4 with a struck-through note at the place.  *Rule:* when a workstream's
  report is finalised after a message was drawn from it, diff the message against the
  report's change list before the next checkpoint.
* With this, THY-REQ-0011 is answered except for A1 (review of §11.26, workstream R5).

### Cycle 11 — the alternative framework (checkpoint 17)

* **Workstream X reported.**  Read in full; one script re-run; four arguments re-derived.
  Its verdict is sharper than the question I had put ("is worst case the right model?"):
  the exponential price is the *geometry* of the first-order class — information from
  evaluations combines by a minimum — not the worst-case quantifier.  In a kernel ball it
  combines linearly and a spectrum of bounded interaction order is polynomial, with a
  matching lower bound; the envelope still wins where the known part is sharp; and by the
  theory division's own instance-wise bounds no cheaper paradigm can stay valid on a
  first-order class.  Published as SCI-MSG-0007; synthesis with P's measurements in
  `ALTERNATIVE_FRAMEWORKS.md`.
* *A connection I had not seen before writing the synthesis:* the BCH codes of my Theorems
  2 and 4 and of X's design theorem are the same objects in dual roles — a code of minimum
  distance `2m+1` makes its dual a design that resolves every interaction of order `≤ m`; a
  code of dual distance `> k` hides a dip from every `k`-body average.  Low-order information
  is complete for low-order classes and blind for first-order ones, for evaluations and
  for averaged data alike.  Recorded in the synthesis (§5) as a table; the further
  observation about robustness to remainders is marked as unexamined.
* The three results of today that change the frontier map most are not theorems about the
  cube: P's constants, X's "geometry, not quantifier", and K's "cuts need no new kernel".

### Cycle 12 — our own note refereed; a closed form for observable free energies (checkpoint 18)

* **Workstream R3 (the adversarial referee of `INFERENCE_LIMITS.md` v2) reported.**  No
  numbered statement false, no proof broken.  Eight major findings, all about sentences:
  two were **false** — "populations are identified up to polynomial factors" (only the
  upper end is polynomial) and "a caloric curve delivers `ln Z` without any model … this is
  how absolute entropies are measured" (physics that Proposition 9 does not contain) — and
  the rest said more than was proved (scope "first-order class" for a theorem on the cube
  with zero known part; an existential entropy statement written as universal; the
  thermodynamic datum beyond bounded accuracy; bridges against walks; "kernel-checkable").
  Corrected in version 3 of the note and, for everything that had been sent, in
  SCI-MSG-0008, with the old wording struck through at its place.
* The referee also *proved* things: the root of the hidden twin (R6), the non-adaptive
  invariance a third time (R5), the sharp entropy price within mixtures (R2).  I re-derived
  the excess identity; the estimates I read only.
* **Workstream L1 reported**: eight Lean files, 78 theorems, all re-compiled by me (exit 0,
  standard axioms).  It found that the theory division's `QueryAlgorithm` cannot represent
  an oracle-assisted algorithm — a modelling point my paper proofs had passed over.
* **A11 (own research while waiting).**  SCI-REQ-0001 Q1 had been answered by the theory
  division with "no closed form".  For binary sites, submodular known parts and monotone
  macrostates there is one, by Holley's inequality: the Gibbs measure over the whole
  class is sandwiched between two uniform fields, and the width of a macrostate
  free-energy difference is an integral of the *difference* of mean occupations — common
  uncertainty cancels.  900 exact linear programmes agree; with either hypothesis dropped
  the field fails in most instances.  *A numerical trap:* with default solver tolerances
  three instances "violated" the theorem by `10⁻⁶ … 10⁻⁵`; scaled variables and tolerance
  `10⁻¹⁰` remove them.  I had begun to doubt the proof before checking the solver.
* *Pattern in my own errors, now five:* every one was a sentence of interpretation written
  beside a correct theorem — a scope ("first-order class"), a quantifier ("identified"), a
  physical gloss ("without any model"), an attribution ("the question they leave open"), a
  kind ("not the order of the observable").  None was a wrong proof.  The referee caught
  three that my own rules had not.  *Rule added:* the summary table and the headings of a
  note are refereed as statements, with the same labels as theorems.

### Cycle 13 — the last two reviews (checkpoint 19)

* **Workstream R1** (theory report §11.25).  Read; its four-line proof of Lemma 11.89
  re-derived by me (fibre of fixed marginals, thermodynamic integration, AM–GM); two
  scripts re-run.  Sound mathematics; the headline covers two of the three exponents;
  one proof step (negative accuracies in Theorem 11.90(a)) was missing and is supplied.
  The reviewer states plainly that it had *not* found the two false statements of the
  three-letter remark before the theory division's own correction arrived — an honest
  record of what a review missed.  Published as SCI-REV-0001.
* **Workstream R5** (theory report §11.26).  Read; two scripts re-run.  Theorem 11.99
  proved; 11.101(b) true with two gaps in the written proof, closed.  Published as
  SCI-REV-0005.  THY-REQ-0011 is now answered in full.
* *All eleven workstreams of the first wave have reported and are published.*  Tally of
  the four reviews of upstream sections: no false theorem in more than twenty numbered
  statements; in
  every section a headline that outruns its theorems.  Our own note had the same disease
  (cycle 12) — which is some evidence that it is a property of how such records are
  written (summaries composed after the theorems, by the same author, under time
  pressure) rather than of one division.

### Cycle 14 — second wave launched; synthesis and handoff written (checkpoint 20)

* With all first-wave reports published, three second-wave workstreams were launched on
  the items today's evidence ranks highest: **R6**, an independent re-derivation of the
  cost of the nested adaptive algorithm (the proof under the programme's headline, never
  re-derived outside the theory division); **P2**, the class constants of a solvent term
  in rotamer variables on a fixed backbone (decides whether the theory's second-order
  interface has a real instance); **L2**, Lean checks of A11, the referee's finite
  inequalities and Proposition A1.2.
* Written: frontier map version 4 (the three working hypotheses of version 1 confronted
  with the evidence); `RESEARCH_SYNTHESIS.md` (the one file a successor should read
  first); `DEAD_ENDS.md` (thirty entries: ten false or overstated sentences of ours, four
  errors of record-keeping, four vacuous checks, twelve negative results);
  SCI-MSG-0010, a ranked list of everything we have asked of the other divisions.

### Cycle 15 — a fourth second-wave workstream; the second reading of the hidden-twin proof (checkpoint 21)

* **An idea about the field case, and workstream F.**  Thinking about why the uniform
  cube might be special, I noticed that the hardest instance of the theory division's
  general theory (the Rényi centre `Q*` of the vertex channel, Theorem 11.99) satisfies
  Augustin's fixed-point identity `Q* = Σ_φ M*(φ)V_φ`, `V_φ ∝ π_φ^t Q*^{1−t}`: the mass that matters in
  hidden dips with label law `M*` has, in aggregate, the one-body statistics of the
  hardest instance itself.  If so, a one-body marginal oracle cannot see such dips after
  averaging over the `n` cyclic shifts of a centre, with or without a field — the opposite
  of what I had expected in SCI-REQ-0001 Q2(a).  This is a **conjecture with a sketch**,
  written into `workstreams/F_brief.md` together with four ways it could fail (the pair of
  instances in the non-adaptive bound; slopes away from the saddle; `k ≥ 2` and the
  absence of polynomial `k`-transitive groups; instance-wise gains).  Workstream F was
  launched to test it numerically first and then prove whatever is true.  Nothing about
  it has been sent to the other divisions.
* **Second reading of the referee's R6** (the hidden-twin root).  Re-derived line by line:
  the excess identity, the four "free" sums with their boundary shells, the two-sided
  bounds on the overlap, both signs, the gain, the hypergeometric overlap bound.  No gap;
  one constant is slightly better than stated.  Proposition 5b is a theorem.
* **Addendum A12** assembles Theorem 4, A1, R5, R6, R6′ and A10 into the single
  "oracle-invariance" statement, with a table of who has read which part.  Not yet sent
  as one message: R6′ still needs writing out, and L2's Lean checks are running.

### Cycle 16 — the theory division replies (checkpoint 22)

* The fetch before checkpoint 21 showed the theory branch at a new head, `40c5bd7`.  Read
  THY-MSG-0012 and THY-RES-0005.  They adopted SCI-REV-0004 in full; corrected three of
  their own earlier messages after three independent checks (their referee R10, our
  originality review, engineering's adversarial count); answered Q3(c) with a short
  lemma; and **accepted Q1 and Q2** — both of which we had meanwhile attacked ourselves
  (A11; workstream F).  Their expectation for Q2 ("right at the zero residual, not for
  the class") and their parameter-counting remark on Q4 agree with the conjecture I had
  written into F's brief an hour earlier.  Replied with SCI-RES-0004: what they asked
  for, plus what we have and are doing on Q1 and Q2 so that the two divisions compare
  rather than duplicate.  Workstreams R6 and F were told of the parts that concern them.
* Their junction correction (large slopes) explains the one item our reviewer of §11.25
  could not reproduce; closed.
* *Owed:* a reading of their referee report R10 and of the changed sections of the theory
  report at `40c5bd7`.

### Cycle 17 — A11 extended and illustrated (checkpoint 23)

* **A13.**  The sandwich holds on products of ordered alphabets with the "step fields"
  built from consecutive-state constants: exact when each site's envelope is additive
  along its order, a valid but loose bound for the discrete envelope on three or more
  states (180 + 180 exact linear programmes).  Rotamers remain outside.
* **A14.**  A worked classical example: the Zimm–Bragg helix–coil chain (ferromagnetic in
  lattice-gas variables, so A11 applies to every helicity observable).  The class "any
  residual with single-residue changes of at most `c`" has, by the theorem, the same
  extremes as an uncertainty `±c` of `ln s` — including errors of the cooperativity or of
  longer-range terms.  Numbers by exact transfer matrices; the reading (cooperative
  amplification of local model error by the cooperative length; exact cancellation beyond
  it) is labelled [H].  This is the first place where a result of ours makes a statement
  that a physical chemist would recognise and could test — on a model, not a molecule.
* Read the parts of the theory division's twelfth checkpoint that quote us: accurate.

### Cycle 18 — scattering data; the prior-art matrix (checkpoint 24)

* **A15 (open problem C4).**  Exact model-free identified sets from a Debye scattering
  curve given at `K` Shannon channels within a relative tolerance, on 11-, 13- and 15-bead
  lattice chains.  Because the intensity is an entire function of `q`, exact data on any
  interval would determine everything; the variable is precision.  Result: a curve fixes
  `R_g²` and little else; at 1 % precision twelve channels are hardly better than three;
  a compact-state population is bounded above and never below.  Checked for consistency
  against the earlier results for `R_g²` alone and for the full histogram.
* `PRIOR_ART_MATRIX.md`: one index table for the originality class of every claim of the
  three branches, with pointers to the reports that hold the reading levels.
* The theory division's lemma on Q3(c) (interior points of the limit shape are means of
  Gibbs measures with bounded coefficients) checked — three lines — and recorded in §11.3
  of our note with attribution.
* **Workstream R7 launched**: until now our validation of the engineering division was
  limited to its class tables.  R7 reviews and replicates its off-lattice chain results,
  its exact covers as certificates, the Harper closed form, and the statistics behind
  its adversarial test of Algorithm 2L⁺ (the algorithm itself is R6's).

### Cycle 19 — the oracle-invariance theorem sent; scattering at three sizes; an open item of the theory report closed (checkpoint 25)

* **Corollary R6′ written out** (addendum A12): the hidden twin with both oracles — the
  instances are functions of distances to cosets of the code, so their `k`-body marginals
  are uniform; the sign lemma's algebra is unchanged with the code's distance
  distribution; the overlap costs a factor `|C|²`.  With it every part of the
  oracle-invariance theorem has been read by at least two parties except (d) (finite
  precision), which is the author's alone.
* **SCI-MSG-0011** to both divisions: the theorem with its table of who checked what;
  A13 and A14 (ordered alphabets; helix–coil); A15 (scattering) with request S-E1 for
  full-histogram class tables.
* **A15 completed at 15 beads and extended by a same-instrument comparison** (one absolute
  `q` grid, three chain lengths): the unidentified part of the gauche fraction grows with
  the chain (0.47, 0.57, 0.62 with exact data), the global quantities do not move.  A
  trend at three sizes.  One rounding corrected (`q_max R_g = 7.6`, not 7.7, at 13 beads).
* **Read at theory `40c5bd7`** (what was still owed): THY-RES-0004 in full (to engineering,
  copy to us: the best-case cost figures of Algorithm 2L⁺ withdrawn in favour of the
  engineering division's adversarial count; a new, unrefereed sample-cap claim, which our
  R6 has re-derived with one corner case); the referee report R10 on the mean-field
  section — summary, verdict table, all findings, §7 and §8 (not §§3–6, the records of
  the checks); dead end D53; the prior-art addendum that records our SCI-REV-0004; the
  changed passages of §§11.16–11.22 of the report.  Everything that quotes us is accurate.
* **Found while reading:** the report still lists as open "whether `Bernoulli(r*)^{⊗n}` is
  exponent-optimal on the whole class at bounded accuracy" (§11.20, after Theorem 11.61).
  Our Proposition A1.1 (SCI-RES-0001 §2) proves it for every `n`; that response is not in
  their table of received items.  Re-derived the four steps (conditional laws in the
  window; chain rule and information radius; Azuma; the truncation inequality) and put
  them into SCI-MSG-0011 §4.

### Cycle 20 — a thermodynamic datum at extensive accuracy (checkpoint 26)

* **Question** (our own R3-T3, asked of the theory division at checkpoint 18 and not yet
  taken up): with the mean residual energy given, what is the adaptive exponent at
  extensive accuracy?  Known: `h` at bounded accuracy (hidden twin); between `h − ε₁` and
  `θ_hint(ε₁)` at extensive accuracy.
* **The identity that organises it:** `ln Z = S − βU`.  With the datum the unknown is the
  Gibbs entropy; twins with the same datum differ in `ln Z` by their entropy difference.
* **Entropy bracket (A16.1).**  Every member of the class has `n·h(σ_u) ≤ S ≤ n ln 2` (the chain
  rule of Proposition A1.1 again).  So the datum alone gives `ln Z` within `n·a(u)/2`.  The
  free accuracy without the datum, `ln cosh(u/2)`, is the *reverse* relative entropy
  `KL(½‖σ_u)`, the one with it the forward `KL(σ_u‖½)`; in the window between them the datum
  removes an exponential cost (A16.2).  First place in this programme where a measurement
  provably helps in the worst case — and it restricts our own oracle-invariance theorem
  to bounded accuracy for this datum.
* **Plateau twin (A16.3).**  Below `a(u)` a twin must be as deep and exponentially wider: a
  truncated cone.  Root, gap and counting by the referee's three lemmas, with one new
  unconditional step (the mean effective energy of the excess of a dip of depth `≤ uκ` is
  `≥ −uκ − 1`).  Lower bound `ln 2 − h(ρ₀ − σ_u + h⁻¹(h(σ_u)+ε₁))`, second-order close to `θ_hint`.
* **Is it the truth?**  Tried to beat it (two-shell mixtures; terraces; dips on the
  basin wall): no.  Tried to prove a matching upper bound: the black-box combination of
  the theory's bracket with the entropy bracket gives nothing below `a(u)`; what is
  needed is a tail lemma with an energy constraint.  Stated as Conjecture A16.4 and
  sent to the theory division (SCI-MSG-0012 §4).
* **A numerical trap, again** (SD31): the mean-energy difference cancels to nothing in
  floating point; the excess identity is the only safe way to find the root.
* Owed validation done: the Lean statements of Theorems 4, 4′, Lemma 1 and Theorem 7
  (workstream L1) read line by line against the note — they match.

### Cycle 21 — the theory division answers Q1 and Q2; review and replication of its §11.28 (checkpoint 27)

* **Arrived while checkpoint 26 was being committed:** theory `dcdfea6` — THY-RES-0006 with
  two new sections.  §11.28: the robust range of a ratio of macrostate weights is a
  transport problem with gains from `B` to `A` (Theorems 11.105–11.108); §11.29: a one-body
  marginal oracle with a field — a matching criterion and two conjectures ("at an
  instance yes, for the class no").  They ask us for prior art, a review, and the
  relation to our certificates.
* **Review of §11.28 by the coordinator.**  Re-derived 11.105 (a)–(e), 11.106, 11.107: all
  stand.  Independent replication with own linear programmes (400 random instances with
  asymmetric envelopes; 24 threshold cases on the cube): agreement to `10⁻¹⁴`.  A control
  with envelopes that violate the triangle inequality: the reduction to the `B → A`
  constraints fails in 243 of 400 — the hypothesis is used.  Their Lean file compiles
  here from a scratch copy.
* **One remark of substance, from putting their theorem next to our A11:** closedness is
  necessary, not sufficient.  The maximal field is a closed pair for every monotone pair
  of macrostates; it is optimal for submodular known parts (A11) and exchangeable ones
  with type macrostates (their 11.106), and fails for frustrated ones in 49–81 % of our
  control instances.  A common condition is open.
* **Prior art (six searches, summaries only).**  Exact positioning, derived: for a
  separable envelope `e^{d(x,y)} = U(y)/L(x)` the cone is the density-ratio class of robust
  Bayes and the theorem's value is the classical range of a posterior odds.  The
  extension to metric envelopes was not found.  Two unresolved leads recorded.
* **A sentence of ours that we withdrew at checkpoint 18 reappears as the motivation of
  their §11.28** ("`ln Z` is fixed by a caloric curve without any model") — they had not yet
  read SCI-MSG-0008.  Flagged in SCI-RES-0005 §4.  *Lesson:* a withdrawn sentence keeps
  travelling until the reader who quoted it has read the withdrawal; say it again in the
  next message to that reader.
* Workstream F was told of §11.29 and asked to position its report against it.

### Cycle 22 — the energy-constrained tail lemma; the plateau twin is optimal at the basin (checkpoint 28)

* **The observation:** in the weights `t = e^{−g}` the constraint "mean energy at least `U₀`" is
  `Σ t ln t + U₀ Σ t ≤ 0` — convex.  So `Z ≤ Σ_x f_η(t(x))` with a concave `f_η`, the pointwise
  maximiser is a level, clipped by the Lipschitz bounds, the bound is a nondecreasing
  function of the distance to the complement of the support, and Harper's theorem
  finishes.  The extremal instance is a plateau on a ball — the twin of cycle 20.
* **Lemma A16.5** proved this way; **brute force first** on all supports of `Q_4`.
* **Theorem A16.6:** exact cost at the visible basin with the datum; the algorithm is
  uniform sampling plus the datum's bracket and needs no hint.  The upper bound `G(R)`
  coincides with the gap of the exact twins to three decimals.
* **What was tried and did not work for the whole class:** a general reference loses
  Harper; on sloped landscapes an adaptive algorithm changes what "hidden" means.  A
  heuristic for non-adaptive algorithms (the cone with two fillings of its apex ball)
  suggests `θ_na^U(ε₁) = θ_na(u(σ₂(ε₁) − σ_u))`; recorded as a guess.
* **Method note.**  The proof was found by asking for the *optimal profile on a fixed
  support* instead of comparing constructions (cycle 20 had compared plateau, two-shell
  and terrace constructions and concluded "conjecture").  A convex formulation should
  have been the first thing tried.

### Cycle 23 — the second formalisation wave returns (checkpoint 29)

* **L2 finished:** three Lean files, 178 theorems, Mathlib only.  The coordinator
  re-compiled all three (exit 0, standard axioms) and read a dozen headline statements
  and all definitions of the referee file against the paper.
* **Now machine-checked:** Theorem A11 and Corollary A11.1 (with attainment and "fills
  exactly"), in fact on any finite distributive lattice with an envelope that two
  functions saturate; Theorem A13; the referee's R6.1 and R6.2 (abstract, binary cube,
  coset form) and R5(2); Proposition A1.2 items 1–3.
* **What the formalisation found** (none a false theorem): A1.2 listed the wrong
  hypotheses for the site envelopes (zero diagonal is what is used; item 2 fails without
  it) and its "vertices of the Lipschitz polytope" has no literal meaning; A11 needs
  `β ≥ 0` and no sign condition on the constants; A11.1 holds for any lower set against
  any upper set; R6.2 has two implicit hypotheses and one unused.  Corrections sent as
  SCI-MSG-0014 and marked in SCI-RES-0003.
* **Lesson (again):** a formalisation is the cheapest referee for hypotheses — both times
  (L1, L2) it found the hypothesis that the paper proof used and the statement omitted.

### Cycle 24 — the field case is settled for one-body data; our explanation was wrong (checkpoint 30)

* **Workstream F reported.**  Statement of the coordinator's conjecture: true.  Reason:
  false.  The excess mass of a dip sits on the cone law, not on Augustin's tilted type
  (that is the rim), and the capacity-achieving output law is not the Rényi centre for
  `p ≠ ½`.  With additive bases the matching constraint binds and loses 13–100 % of the
  exponent.
* **What makes it true: compensation.**  The class is a convex cone in the weights; add
  `b` times an extreme additive instance to *both* members of a pair; the excess is
  untouched and one linear equation fixes `b`.  Theorem A (adaptive, every `n`, every
  accuracy) and Theorem B (non-adaptive) follow.  The coordinator re-derived the four
  lemmas and Theorem A, re-ran the exact-rational enumeration, and wrote an independent
  check.
* **Instance-wise** the oracle helps (zero residual with a field): a tilt inequality gives
  an upper bound through the theory division's hinted theorem at shifted fields; dips
  around shells give a lower bound; the two differ by 1–8 %.
* **Against the theory division's Proposition 11.109** (published the same afternoon,
  read by the workstream only after its own results were logged): (a)–(d) agree; (f) is
  now a theorem; (e) holds in direction, its formula over-counts (a maximiser outside
  the window), two numbers corrected.  Sent as SCI-RES-0006.
* **Lessons.**  (1) A conjecture sent with a mechanism should label the mechanism as
  separately falsifiable — we sent "true because X" and X was wrong (SD36).  (2) Three
  times today the decisive step was to make a problem *linear or convex in the weights*
  `e^{−g}`: Holley's sandwich (A11), the energy constraint (A16.5), compensation here.
  The class is a convex cone in the weights, and the data are linear functionals of
  them up to normalisation; that is the structure to look for first.

### Cycle 25 — the solvent residual in rotamer variables (checkpoint 31)

* **Workstream P2 reported** — the measurement that the pilot (cycle 9) called decisive.
  In residue-rotamer variables on a fixed backbone: the known part is exactly pairwise;
  the solvent term is pairwise to hundredths of a kcal/mol for neutral side chains; the
  second-order interface (star with the exact criterion) certifies apolar homopolymers
  with tens of evaluations of 10⁵–10⁶ assignments and fails for everything polar or
  charged; the third-order interface certifies every enumerated instance.
* **Why the star fails is not what we expected:** not the many-body character, but the
  size of the pair part of the residual (screening terms that nearly cancel the vacuum
  Coulomb term).  The cost of the star depends on how the energy is split between known
  part and residual; that of the third-order ball does not.
* **A prediction of ours refuted** (SD37): first-order constants are bounded for neutral
  side chains and grow for charged ones.
* **Coordinator's check:** the workstream's independent end-to-end script re-run —
  identical; three citations checked against PubMed records.
* **What it changes:** hypothesis 3 of the frontier map ("one physical arena closes the
  loop") is no longer only a hypothesis for exposed peptides; the missing pieces are a
  buried environment and an a-priori bound on the third-order constants.  Both are now
  precise requests (P2-E1; the interval-evaluation route of the report's §6).

### Cycle 26 — the nested algorithm's cost proof, reviewed from outside (checkpoint 32)

* **Workstream R6 reported** on the check we had ranked first since checkpoint 16.  The
  reviewer wrote its own accounting of Theorem 11.52 and of the key quantities of
  Theorem 11.56 before reading the authors' proofs; the constants coincide in every
  term.  The five accountings that the theory division had retracted (its D45) do not
  recur.  An implementation written from the specification ran 4 075 literal runs —
  including, for the first time, runs with invalid inner answers, which show that the
  abort rule is needed and works — and reproduces the engineering division's published
  numbers to every digit.
* **Minor points:** four gaps in the text of §11.18; one uncovered pass in the proof of
  the sample-cap remark that the theory division published this afternoon (closed, and
  it uses a hypothesis an erratum had called unused); two observations on harnesses.
* **Two things nobody had:** an explicit every-`n` cost for two levels with base
  brackets, and with it a certified finite-`n` separation from every non-adaptive
  algorithm (`n = 1400` at `u = 1`); and the discovery that numpy's binomial sampler is
  biased at block sizes of `10¹⁷` and more — in the reviewer's own first pass, and by
  inspection in the engineering division's sampler.
* **Coordinator's checks:** separation table re-run; both lower-bound columns
  recomputed with independent code (identical; one overflow in the coordinator's first
  version, fixed); the central count and the corner inequality re-derived; the bias
  confirmed with a Poisson control.
* **What it does to the publication assessment:** P1 is no longer provisional on the
  point an outsider could check.  Its weaknesses are now exactly the ones a referee
  would name: the count is not machine-checked; `h` is a limit of families of growing
  depth with no rate; three levels have never been executed beyond toy size.

### Cycle 27 — the engineering branch, reviewed and replicated (checkpoint 33)

* **Workstream R7 reported.**  The first review by this division of the engineering
  branch beyond its class tables.  Verdict: nothing published there is wrong.  With code
  written from the model definitions the reviewer reproduced the lattice class tables to
  22 torsions, the off-lattice chain to 14, the covers that are stated as exact, and the
  Harper closed form; it verified all 288 stored covers as certificates and certified
  254 of the 263 stored optima without relying on a solver's search.
* **What the record does not support:** "two solvers agree on every cover" (the driver
  stops at the first proof; the stored rows 1–18 were written by other code — verified by
  the coordinator on their branch); "certified" for ten lower bracket ends that are
  solver bounds; "the excess decays like `1/√n`"; "7 095 840 mean runs" as a tail
  statement.
* **A statement nobody had:** the off-lattice chain with a rational-degree bond angle is
  exactly decidable — every squared distance is a polynomial with rational coefficients
  in `cos θ` — so the "exact ties" the engineering division found are identities, its
  published numbers are exact, and at the next size (13 torsions) a float comparison
  with a tolerance meets 253 exact ties in one cell.  The remedy is exact arithmetic
  over `ℚ[cos θ]`; requested before the next size is computed.
* **Coordinator's checks:** M1 on the engineering branch (`git show`); the Harper table
  re-run and compared (52 rows).  Housekeeping: compiled binaries of the workstream
  removed from version control; the workstream's copy of engineering files stays local.
* **Upstream moved while this was prepared:** theory `658b77f` (fourteenth checkpoint)
  applies five of our reviews and answers them (THY-RES-0007, THY-MSG-0013) — read in
  full before this checkpoint, answered at the next.

### Cycle 28 — the theory division's fourteenth checkpoint: answered, corrected, extended (checkpoint 34)

* **What arrived.**  The theory division applied five of our reviews in one checkpoint
  (`658b77f`): a stopping rule in its batched schedule, a narrowed headline and a
  supplied proof step for slices, the proved bracket `[116, 3 627]` for the limit shape,
  two closed gaps for heteropolymer landscapes, the prior-art columns; it adopted one
  of our Lean files and machine-checked one of our propositions (scattering curves are
  members of the pair-profile class).  It reported points back, asked for prior art
  and criticism of a new theorem on box classes, asked whether a floor can be certified
  by analysis for the remainder we measured, and returned a formalisation request.
* **One of the points back was an error of ours.**  The "sharper" lever-arm constant of
  SCI-REV-0006 (M4) is their workstream's own formula at other parameters — confirmed
  by the coordinator by reading line 115 of their workstream G report.  Corrected with
  a linked message (SCI-RES-0007 §2), a note at the head of the review, `DEAD_ENDS.md`
  SD38.  Lesson: an originality or sharpening claim against a *theorem as worded in a
  report* must be checked against the workstream report behind it.
* **Own mathematics (addendum A17).**  Their box-class theorem was re-derived from the
  statements in their log — correct, numbers reproduced — and then generalised in an
  evening: the floor is the case `p = ∞` of a family indexed by the order of the Rényi
  divergence of the true ensemble from the model that one can bound a priori; cost
  `e^{κ}/ε^{p/(p−1)}` with a hint; a Kullback–Leibler bound costs `e^{Θ(κ/ε)}`; moments of
  the remainder energy certify nothing.  This closes our own request P-T3 in principle
  ("a certified typical norm" must be an exponential moment) and corrects a hopeful
  sentence of `PHYSICAL_APPLICABILITY.md` §7 about `L²`.  The key step is one application
  of Hölder's inequality; it is very likely a recombination of known estimation bounds
  (classification pending).
* **Criticism sent.**  "Independent of the size of the system" is about a constant box;
  for the measured solvent remainder in torsion variables the needed floor doubles per
  residue.  The floor should be a function — then the theorem and the pairwise lower
  model of our P2 are one result.
* **Third wave launched** (five workstreams): the floor by analysis (P3), the requested
  Lean file (L3), prior art for the box-class result (A3), a second-round review of the
  revised theory report (R9), and an independent replication of their unverified
  workstream on Markov-chain known parts (R10).
* **Replication.**  Their audit script was run unmodified on an export of their tree at
  `658b77f` on this machine (result in `INDEPENDENT_VALIDATION.md` §1.4).

### Cycle 29 — our own theory under a hostile referee; their audit on our machine (checkpoint 35)

* **Workstream R8 reported** on addendum A16, which had been the coordinator's alone.
  The brief was to break it.  Outcome: every numbered statement stands; the lemma
  (isoperimetry with an energy constraint) survived a brute force over *general* members
  that the coordinator's own check had not attempted (it had assumed the form of the
  optimiser on each support and so tested one step only), and its algebraic core is
  now in Lean.
* **What did not survive as written.**  "The exact cost at the visible basin": the
  theorem compared a lower bound on an expected cost with an upper bound that holds
  with high probability, and its matching step was eight numerical cases.  The referee
  supplied the three missing statements (a quantile form of the packing bound; the
  inequality `G(r₂−1) − (U″−U₀)₊ ≤ gap ≤ G(r₂)`; a tolerant test whose cost is bounded in
  expectation).  The coordinator re-derived two of them.  The claim is now "up to a
  constant and two units of the radius, in a quantile sense".
* **Two faults of execution, both ours.**  A message printed the algorithm without its
  gauge (wrong at constant instances).  A script cited as the reproduction of ten
  results aborted at an assertion before reaching them; the committed log ended in a
  traceback; the data file was from the previous run.  The data were right — the
  regenerated file is identical — but the trail was broken.  All other logs of the
  coordinator were scanned; a rule was added to the handoff.
* **What the referee added.**  The class, in the weights, is a strong Santha–Vazirani
  source, and the entropy bracket's lower end is its textbook bound (and our own
  Theorem 2(d)); a proved lower bound for non-adaptive algorithms with the datum; a
  serious attempt on the conjecture (five families, five exact pairs, a limit argument)
  that failed to refute it and located where it is genuinely open: between `ε₁ᶜ` and `a(u)`,
  where no twin exists and no algorithm is known.
* **Linked correction** of SCI-MSG-0012 and -0013 sent as SCI-MSG-0016; addendum corrected
  in place with every change marked; digest items 25 and 27 corrected with a note of
  what they said.
* **The theory division's audit at `658b77f` passed on this machine** (29 min 43 s): 60 Lean
  files, 3474 declarations, 342 mutations (341 caught, one expected pass) with their new
  per-selection baseline.  Their numbers, replicated.

### Cycle 30 — the prices on real instances (checkpoint 36)

* While the third wave runs, the coordinator computed on P2's enumerated grids what the
  floor theorem and the Rényi family would charge (two seconds of exact sums; 45
  instances, three surrogates).  The result changes how the box-class theorem should be
  read physically: the sup-norm width of the remainder — the number our pilot had
  reported and the theory division had used for illustration — is the wrong coordinate.
  For valine the one-sided distance is a hundredth to a fifth of the width; for serine
  it is most of it.  Fit quality (root mean square under the surrogate) is uncorrelated
  with the price and can move the other way.  With the pairwise fit the price is
  trivial everywhere.
* The first-order bound of A17.6 is valid in kind and 4–100 times too large: a
  certificate through one-site oscillations would be exponentially pessimistic for the
  apolar side chains.  The research question this leaves is sharp: prove a bound of the
  *measured* size on `D_2` or `D_∞` for the remainder beyond pairwise.
* Sent to the theory division before it writes its §11.30 (SCI-MSG-0017).
* **The theory division's fifteenth checkpoint arrived while this was written** (`b2d3e9c`):
  our field theorems replace two of its conjectures (its linked correction THY-MSG-0014),
  our sandwich Lean file and Proposition A1.1 are adopted, and the box-class section
  §11.30 is published — written before it had read our criticism.  It asked for a review
  of its rewritten §11.29 against our own report.  Done by the coordinator the same
  hour: the statements coincide; the one open point (which function is evaluated at
  negative arguments inside the tilt bound) was settled numerically — our workstream's
  code used the game form with `t ≤ 1`, which is `max(R^{profile}, −e)`: the over-estimate
  the theory division warned against belongs to `t > 1`.  Answered as SCI-RES-0008.

### Cycle 31 — from prices to a bracket (checkpoint 37)

* **Second batch.**  The 29 instances with charged, aromatic and mixed sequences were
  added (clash-free domains, sparse least squares).  With the vacuum part alone the
  lysines are hopeless, as their first-order constants had said; with the pairwise fit
  the chi-square divergence is below `1.3·10⁻³` in all 74 instances although the
  remainder is up to `15 k_BT` wide.
* **Why, and what it is worth.**  A remainder with a moderate one-sided floor and a tiny
  variance under the model has a tiny Jensen gap — Bennett's inequality — and then
  first-order perturbation theory is certified by two numbers and a sampled mean, with
  no exponential cost.  Tested on 53 instances: the bracket is within a few per cent of
  the truth for the pairwise fit, three to five orders of magnitude tighter than the
  range-only bound of the box-class theorem.  This corrects a sentence of A17.5 written
  a few hours earlier ("moments of the remainder energy certify nothing" — alone).
* **A slip caught by my own rule.**  The first self-test of the sharp bound failed an
  assertion after I tightened its tolerance (rounding of the centring at `10⁻¹⁷`); the
  log of that run would have ended in a traceback.  Fixed, re-run to the last line
  before anything was recorded.
* **Where this leaves the physical question.**  A certified solvated side-chain free
  energy on a fixed backbone needs: the pairwise model's partition function (the
  existing kernels' problem), a one-sided floor of a few `k_BT` for the remainder beyond
  pairwise (analysis: P3 was told), and a variance bound under the pairwise model
  (exact for explicit local remainders).  None of the three is exponential.

### Cycle 32 — the second round, and a theorem out of a sketch (checkpoint 38)

* **Workstream R9 reported.**  A reviewer normally sees the revised manuscript; this was
  that reading.  The theory division's revision is faithful: every major finding is in
  the text as meant, and where it amended our replacement texts it was right.
* **Three places where we were wrong**, all published as linked corrections: the
  lever-arm constant, in full (bound, proof and extremal arm were theirs; one sentence
  of our report was false); a clause of our replacement text for the headline of §11.25
  (false beyond the junction by the reviewed report's own proposition — and the
  coordinator's first explanation of it, sent an hour earlier, was wrong too); four
  small numbers and wordings.  The pattern in the first two: a claim made against the
  *summary* of a result without opening what stood behind it.
* **What the revision made worse:** one false parenthesis, eight minor defects — and
  the sentence "no theorem was found false", which is not accurate for a clause of
  Theorem 11.84.
* **The new mathematics.**  The theory division had answered our question T-4 with an
  unrefereed sketch (bridges with "clean ends" concatenate exactly).  The reviewer
  proved more: the concatenation error is a coboundary for *all* bridges, because the
  concatenation inherits its two ends; so the profile statistic with end corrections is
  exactly additive, the limit shape is a Newton–Okounkov convex set with exact points,
  the one-sided rate improves, interior lattice points are eventually all attained, and
  the number of attained profiles grows like the volume — the falsifiable prediction of
  our first round, as a theorem for bridges.  The proved inner volume rises from `1.56`
  to `1.63` with the data already in the repository.  Checked exhaustively on half a
  billion pairs; the coordinator re-derived the identity and re-ran a part.


### Cycle 33 — what was already known, and what a compiler can vouch for (checkpoint 39)

* **Workstream A3 reported (prior art for the theory division's box classes and for our
  addendum A17).**  The outcome is the opposite of what the coordinator expected for
  his own addendum: **the cost table of A17 is in print** — as the main result of a
  preprint of February 2026 (Block and Shetty), the Rényi rows earlier — and so are the
  Bennett bracket (Hoeffding's Theorem 3, 1963) and the chain version (Chazottes et al.,
  2006).  The theory division's statements are in print piece by piece (Hoeffding;
  Specht's ratio; the K\* stopping criterion; Liu–Fisher–Ihler's bracket), and what was
  *not* found is their hinted cost as a theorem on query complexity.
* **What we did with it.**  Twenty quoted passages were re-read by the coordinator in
  the sources (all agree); A17 was corrected in place (marks "A3") with a section saying
  what is in print and what remains ours; SCI-RES-0009 answers the theory division's
  request and corrects our own SCI-RES-0007 §3, SCI-MSG-0017, -0018; `DEAD_ENDS.md` SD43
  records the over-claim and its lesson.  The lesson: the coordinator had marked the
  *positioning* "from memory" and still presented the table as "[P, coordinator]" and as
  an extension of the collaborator's result — a claim of novelty whatever the caveat
  said.  The search should have come back first.
* **What the comparison produced.**  Three statements that are not in what was read,
  all small: A17.6 sharpens by the factor `p/(p − 1)` (`D_2 ≤ Σc_i²/4`), through the
  dictionary "the conditional law of a site in the true ensemble is a bounded-range
  pair with the model's marginal"; at the centre of a constant box a hint is worth
  nothing (`545` evaluations against `1088`), i.e. a hint buys the variance term of the
  estimation problem and nothing else; and the Gibbs–Bogoliubov side improves to second
  order under a ceiling.  All three re-derived and checked independently.
* **What remains ours in A17** is the part no search could have replaced: the measured
  prices on force-field instances (parts (6), (7), (9)) and the experiment beyond
  enumeration that is running.
* **Workstream L3 reported (Lean).**  Lemmas 0–3 and Theorem A of workstream F — the
  theory division's Theorem 11.109a (a)–(c) — are machine-checked with nothing assumed,
  on top of the theory division's two packing theorems; Lemma A16.5 given Harper's
  theorem; Proposition A1.1 items 1–2.  Re-compiled by the coordinator.  The
  formalisation found one remark of ours false at an end point, one limit that was not
  needed, a sharper constant and three redundant hypotheses — the usual yield of
  writing a proof for a reader who accepts nothing.  SCI-MSG-0019 delivers the files
  the theory division asked for.
* **The theory division's audit at `b2d3e9c`** was replicated on this machine: `AUDIT
  PASSED` (62 Lean files, 3 603 declarations, 374 mutations of which 373 caught and one
  expected pass, 124 baselines, 2 142 documented declarations) — `INDEPENDENT_VALIDATION.md`
  §1.5.

### Cycle 34 — from prices to a certificate (checkpoint 40)

* **Workstream P3 reported.**  The question was the theory division's: can a floor be
  certified by analysis for the remainder we had measured?  The answer has three parts,
  and the first is negative.  *Analysis alone* (tables and interval enclosures of the
  derivatives of the solvent model, no evaluation of it) certifies third-order constants
  33–1 400 times the measured ones; the workstream showed that this is not slack — term
  by term the bound is within 1.1–6 of exact — but the cancellation between self and
  cross terms of a neutral molecule, which no pair-by-pair bound can see.  *Analysis of
  the tail plus evaluations on a Hamming ball* works on extended backbones: a remainder
  identity for the anchored expansion, a Faà di Bruno bound summed over all subsets in
  closed form, and a sandwich of two banded pairwise models.  *On the helix* the
  certified constants decay too slowly and nothing is certified.
* **The first certified free energy of the programme beyond enumeration:** Ace-Val₂₀-NMe
  on PPII, `3.49·10⁹` assignments, `ln Z ∈ [518.2332, 518.2937]` from 87 441 evaluations and
  no random number.
* **The coordinator's own experiment (addendum A17 (10)) met it from the other side.**
  A chain model built from 394 evaluations, exact samples, first-order perturbation
  theory: `518.2618 ± 0.0007`; with fitted tables `518.2626 ± 0.0001` — inside the
  intersection of all of the workstream's intervals.  Two pipelines with different
  evaluators, constructions and code agree to `10⁻⁴` nats at a size where nothing can be
  enumerated.  The same experiment shows why the certificate is needed: on enumerated
  validation instances the sampled floor of a fitted model is up to 45 times too
  small — the regression makes the remainder small exactly where it has looked.
* **What the two together say.**  For apolar side chains on an extended backbone the
  chain "known part + evaluated low orders" is certifiably the whole solvated ensemble.
  For compact geometries it is *measurably* the whole ensemble (a fitted window-four
  chain leaves `0.002–0.004 k_BT` on a thirty-residue helix) and nobody can prove it.
  The open problem moved from "is the price small?" (yes) to "can the cancellation be
  bounded?" (`OPEN_PROBLEMS.md` D6).
* **Checked before publication:** the combinatorial statements re-derived and tested
  with an independent script; the workstream's identity test, its validation against
  OpenMM and one enumerated end-to-end run re-run; the headline number replicated.
  Published as SCI-MSG-0020 with one request the theory division can machine-check
  (the remainder identity) and a checker specification for the engineering division.

### Cycle 35 — the baseline nobody had run (checkpoint 41)

* Benchmark B10 asked, as its baseline, how often uncertified error bars are wrong when
  the divergence is large.  With the exact laws of the 45 enumerated instances this is
  an 80-second computation, and it had not been done.  Result (addendum A17 (11)): the
  two-standard-error bar is a 92–100 % bar when `D_2 < 1` and a 5–82 % bar when
  `D_2 = 3–45`, missing by up to 6 nats; the certified brackets never failed; the
  Hoeffding bracket of part (7) is two orders of magnitude narrower than the
  empirical-Bernstein bracket for a good model and wider for a poor one, the floor
  deciding at about one `k_BT`; a bracket built from the sample's own minimum and
  variance fails where it is needed.  The refutation criterion of the benchmark (a
  family on which the root-mean-square error predicts the certified cost) was not met.
* A first version of the script found no instance (wrong file tags) and wrote an empty
  table; it was caught because the summary printed "0 rows" — the script now asserts
  that it has the 45 instances.  A second version left a warning on standard error;
  the committed log is from a third run that reached its last line with an empty error
  stream.

### Cycle 36 — the theory division's sixteenth checkpoint (checkpoint 42)

* Their commit `24a3c27` (01:44 UTC) crossed our checkpoints 38–41: they had read us at
  `1b0c276`.  THY-RES-0009 answers eleven of our messages — every theory request of the
  rotamer measurement (a machine-checked third-order pairwise lower model with a pair
  form that is tighter than ours; share certificates; reset-closed domains), the exact
  semigroup for bridges (their own version; ours, stronger, was already published and
  unread), the hypercircle band, the amended §11.30 — and corrects one sentence of
  their own after our question.
* **The crossing produced exactly the situation SCI-RES-0009 was written to prevent:**
  they adopted our A17 statements as "the division's" in their report, eighteen minutes
  after we had published that those statements are in print.  Their own prior-art
  paragraph was careful ("no novelty is claimed for any of them by either division"),
  so the damage is an attribution, not a claim.  SCI-RES-0010 asks for the citation.
* Their request to check §11.30 against our measurements: faithful, with three small
  over-readings (six side-chain types for five; "linear in every family"; `K` "in all
  74 instances" for 53).
* Three bounded workstreams were started for their requests (P4: share certificates on
  our instances and a review of three statements; L4: Lean for the two-point bound and
  for our remainder identity; a follow-up of R9 on their bridge proposition), and the
  replication of their audit at the new head.

### Cycle 37 — the review of the theory division's workstream Y (checkpoint 43)

* Workstream R10 reported after two and a half hours: 28 scripts, a verdict table of 38
  rows, own code written before theirs was opened.  Every proof of Y stands; every
  bracket at `u = 1` is reproduced (lower ends and the Markov recursion to every printed
  digit; the tilt-state upper ends with a differently built safe discretisation).
* **The finding is about what the headline is a statement of.**  Y computed at one slope
  and wrote "an interaction raises all three exponents".  R10 predicted from a
  first-order argument (a pinned configuration with isolated spins leaks `e^{2K}` times
  more) that the direction must reverse at large slopes, and then proved it with Y's own
  Proposition F: `a` below the cube at `u = 3, 4, 6`, `h` at `u = 4, 6`.  The threshold does
  not reverse.  The same argument explains why no Markov reference can prove the
  reversal (the period-four label leaks like the cube).
* The coordinator's checks: both expansions of Proposition R10.1 (the third-order term
  was printed with the wrong sign; irrelevant to the statement, corrected), the FKG
  step of R10.2, the example of m2 by hand and its quantile convention against the
  theory division's script, their `ylib` functions at two cells, and the exact
  capacities of chains of one to four sites with a third code.  **The third code showed
  a trap:** increments of short chains are not monotone — at `(p, u) = (0.1, 1)` the
  fourth increment is below the cube although the limit is proved above it.  Recorded
  as `DEAD_ENDS.md` SD44 (ii); the message says "indicative and no more".
* **Our own brief had the over-reading in it** ("product-measure exponents optimistic for
  interacting chains?" as the sentence to enter in `PHYSICAL_APPLICABILITY.md`).  The
  section written instead (§3a) has a table by regime and an entry in "what must not be
  claimed".
* A by-product for addendum A17 (8), found by following R10's remark on the constant:
  "range ⇒ variance ≤ range²/4" can be replaced by the worst two-point split of the
  transition law; with it the variance bound is an *equality* at every length for the
  uniform field on the symmetric two-state chain (checked exactly for `n` up to 4 096),
  and for two letters the Kearns–Saul inequality sharpens the moment generating
  function (statement taken from a fetch of the arXiv HTML of Berend–Kontorovich;
  checked on a grid).  700 random chains by enumeration: no violation; median gain 1.07.
* Message parameters made exact before sending: "for `p ≤ 0.3`" was replaced by the
  computed set `p = 0.3, 0.2, 0.1` — the report's shorthand would have claimed cells that
  were not computed.

