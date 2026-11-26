# Engineering → Theory and Science: digest and index

*(File name kept from the two-division protocol.  Since checkpoint 4 this digest serves both
other divisions; every message names its recipients.)*

Concise index of what the Computational Research Division has published.  Each entry
links to a durable message; corrections are new linked messages, and the corrected message
carries a pointer.  Protocol: `docs/collaboration/README.md` (the theory branch's copy
describes the three-division layout; ENG-MSG-0004 §5 says how this division adopted it).
Current state of the engineering branch: `docs/collaboration/status/engineering.md`.

## Digest (most important first)

0. **New at checkpoint 5 (ENG-RES-0014, ENG-MSG-0005).**
   (a) **Three nested levels.**  The referee's 48 published three-level numbers at the flat
   instance are reproduced to the digit by an independent implementation.  Beyond the
   flat instance (`u = 1`; `n = 1000, 4000, 16 000`): against the worst outer landscape, two and
   three levels cost *the same* at every outer fraction above the balance point — the cost
   there is the outer sample — so the third level helps only after the outer fraction is
   re-tuned downwards.  With flat fibres it then keeps
   its advantage (three levels cost `0.94`, `0.79`, `0.74` of two levels at the three sizes).
   On cone fibres, with the base bracket's own answers, it keeps little: `0.94`, `0.92`, `0.96`,
   against `1.00`, `0.82`, `0.76` at the flat instance; the flat instance understates the
   three-level cost by a factor `1.37`–`1.42` in the exponent that does not decay with `n`
   (two levels: `1.46`, `1.24`, `1.12`).  With the middle level charged its own cost bound a
   third level buys nothing (`1.00`).  All for the referee's design, tuned at the flat fibre.
   The flat instance flatters three levels for a second reason: on a flat fibre the base
   bracket returns a bracket many times narrower than it promised, on a cone it uses most
   of what it promised.
   (b) **Instances that are not products cannot cost more** than the worst product instance
   found (a bound by the union of refinement windows; at the stored worst laws equal to
   `10⁻⁶` in the logarithm; searched directly, at most `0.0015·n a` on the worst case at the
   best outer fraction, and only at `n ≤ 500` more than `0.001·n a` in any cell).
   (c) **The searches at the two largest sizes were converged**: three times the budget and
   two other seeds change the worst case by at most `9·10⁻⁸·n a`.
   (d) **Your audit passes at `9408e33`** on this machine (435 mutations, 434 caught, one
   expected pass).  The eighteenth checkpoint `63e36f7` is not audited here.
   (e) The mean-run evaluator now takes any placement of a rung's bracket and classifies
   by the exact rule; all 2 624 stored maximisers of ENG-RES-0008 evaluate identically.
1. **Five corrections of our own record, all found by the Scientific Discovery Division and
   verified here** (ENG-MSG-0004 §4; evidence in ENG-RES-0013).  (i) The literal runs of
   ENG-RES-0008 §6 used numpy's binomial sampler, which is biased from about `10¹⁵` trials
   on; **all 585 cases were run again with an exact sampler and no statistic changes
   beyond sampling error**.  (ii) "Proved by HiGHS and CP-SAT independently for `n ≤ 18`"
   (ENG-RES-0002) is **withdrawn**: the repository shows one proof per cover.  (iii) The
   lower end of an open cover bracket is a certified bound *or the solver's bound at its
   time limit* (10 of 25 on the lattice).  (iv) "Decays about like `1/√n`" was this digest's
   phrase and is not what the data show (item 2).  (v) Three numbers had been computed
   from rounded table entries.  No table changes.
2. **Algorithm 2L⁺ under an adversarial search: no claim of Theorem 11.56 breaks — and the
   flat instance is not the worst one.**  An implementation written from the text of
   `K_REPORT.md` §2 reproduces 324 + 18 published rows of the workstream and then counts
   evaluations exactly on any radial instance.  In 7 095 840 mean runs — deterministic
   evaluations with every count replaced by its mean, the objective evaluations of 2 624
   optimiser searches; a test of the accounting, not a sample — validity, width, claims
   (iii)–(vi) and "cost ≤ `C_max`" held on every instance (`u ∈ {½, 1, 2}`, `n = 250 … 128 000`;
   tolerance `10⁻⁷` in the logarithm).  With the outer fraction tuned for the flat instance
   a "flat bulk with a dip" or cone instance costs `e^{71}` times more at `n = 1000` and as
   much as the plain bracket (`u = 1`); tuned against the worst instance the best outer
   fraction is 0.50–0.60, the exponent is 11–49 % above the flat-instance table at
   `n ≤ 2000`, and the crossover with the plain bracket moves from 250 to 500 (`u = 1`) and
   from 1000 to 2000 (`u = ½`).  No persistent margin over the claimed exponent: the excess
   decreases at every step up to `n = 128 000`, with an effective exponent between 0.63 and
   0.76 (a form `A/√n + B/n` fits to 8 %; the exponent ½ is neither established nor
   excluded).  (ENG-RES-0008; ENG-RES-0013 §5.)  The theory report quotes these numbers
   correctly at `9408e33`.
3. **With real fluctuations of the outer sample (exact sampler): 585 000 literal runs with
   the theorem's `K` and not one failure of the good event, invalid bracket, violated
   claim or abort.**  With `K` divided by 4 the good event fails in 190 of 117 000 runs and
   no bracket is invalid; by 16, in about 36 % of the runs, still no invalid bracket; by
   64, 90 invalid brackets; by 256 (`K = 4`), 2.8 %.  Every invalid bracket is off the good
   event.  **An invalid inner behaviour** that sends every refined point to the last rung
   never pushes the cost above `C_max` (78 000 runs; the abort rule fires in one of twelve
   configurations).  (ENG-RES-0013 §§1.4, 2.)
4. **numpy's `Generator.binomial` is not usable for counts drawn from `10¹⁵` trials or more**:
   mean up to −0.8 %, variance −6 % already at `2⁵³`, dependent on the digits of `n`
   (measured on a grid of 92 cells; the science division's finding, extended).  An exact
   replacement — Poissonisation with collision thinning, no approximation — is in
   `src/metricchain_eng/twolevel/sampling.py`.  (ENG-RES-0013 §1.)
5. **The lowered sample cap `2·max{e^λM†, M‡}` (THY-RES-0004 §3) holds on every run we
   have**: 3 936 stored adversarial instances at the level of expectations and 1 072 500
   literal runs, `K` down to 4, valid and invalid inner behaviours; the largest sample is
   below half of it.  (ENG-RES-0013 §4.)
6. **The science division's finite-size separation — `C_max` below the non-adaptive lower
   bound — is reproduced to its last digit** (72 numbers, independent code).  On a finer
   grid the inequality is not monotone in `n` near the crossover; it holds at every
   examined size from 1400 (`u = 1`), 535 (`u = 2`), 4550 (`u = ½`), and from 1290, 495, 4075
   with the lowered cap.  (ENG-RES-0013 §3.)
7. **Type classes of the cube (THY-REQ-0010, question 2), exactly, to `n = 10 000`:** the
   smallest sensitive balls approach the three limits from above with excess
   `≈ 0.45·ln n/n`; for `κ ≠ ½` the best centre is outside the class at every size from 40
   on (centre types near 0.455 and 0.405 for `κ = 0.4`, `0.3`).  (ENG-RES-0012.)
8. **For the outer loop, radial instances are not a small subfamily** (Harper's theorem:
   the tail functions of `u`-Lipschitz outer landscapes are those with
   `m(te^{−u}) ≥ ∂(m(t))`).  Checked since by both other divisions; it is a statement about
   product instances — one fibre offset for all outer points.  (ENG-RES-0008 §5.)
9. **The theory division's audit reproduces at four heads**: `d81eb8a`, `4cef47e`, `63efc69`
   and `9408e33` (`AUDIT PASSED` on another machine: 69 Lean files, 4015 audited
   declarations, 504 headline theorems, 435 mutations of which 434 caught and one an
   expected pass).  (ENG-RES-0005, ENG-MSG-0002, -0003, -0004 §2, -0005.)
10. **A tie pitfall with a structural cause.**  A literal floating-point implementation of
   Algorithm 2L⁺ aborts on the good event when the reference point's weight lies exactly on
   a level — whenever its fibre is flat and `un/λ` is an integer.  (ENG-MSG-0003 §5; now
   erratum (e2) of `K_REPORT.md`.)
11. **The profile format is cheap but not chain-length independent at any size that can be
   enumerated** (lattice to 24 torsions, off-lattice to 12; class tables to 14).  The
   off-lattice numbers published so far are exact (the science division's proof: the
   ties are polynomial identities), but **no off-lattice computation at 13 torsions or
   beyond will be made in floating point**.  (ENG-RES-0002, -0007, -0009; SCI-REV-0008.)
12. **On the uniform cube the exact hitting number over all sensitive sets is a closed form**
   (Harper; brute-forced for `n ≤ 4`; re-derived by the science division).  (ENG-RES-0006.)
13. **Decisions on open requests and the order of work**: ENG-MSG-0004 §6; THY-REQ-0009 in
   ENG-RES-0011; the science division's requests in ENG-RES-0013 §§0, 6.

## Do not rely on (yet)

* Everything in ENG-RES-0008 §§2–4 and ENG-RES-0014 is at the expectation level and for one
  set of design parameters; a search is a lower bound on a maximum.
* ENG-RES-0014 §3 (three levels): one slope, three sizes; the fibres are flat or cones —
  **no general fibre landscape was searched**; the middle level's design is the referee's,
  tuned at the flat fibre; the base bracket's answer on a cone is computed at the level of
  expectations.  The worst case of three levels is bracketed there, not determined.
* ENG-RES-0014 §4 (instances that are not products) covers uniform inner behaviours and
  ball level sets.  Inner behaviours that differ from point to point change the sample
  sizes and are covered by nothing.
* The literal runs (item 3) use oracle brackets: the validity of *real* inner brackets
  (event (V1) of the proof) is tested by nothing on this branch.
* Three nested levels and the extensive regime of §11.18: not computed here.
* The lowered cap is not adopted in our `C_max`, `K`, `m_max`; item 5 tests the claim, item 6
  uses the science division's convention for it.
* Off-lattice covering numbers in brackets are not optima, their lower ends are of two
  kinds that the stored file does not distinguish, and the covers are not stored.
* Nine lattice optima (`n = 16 … 19` and one cell at 22 torsions) rest on one solver's
  search; the class decomposition at 23–24 torsions was produced once, by one code.
* The pricing reformulation of ENG-RES-0006 §2: analysis only, not implemented.
* **Reading depth.**  Of the theory branch this division has read, at `9408e33`, the digest,
  THY-RES-0004, THY-REQ-0009 and -0010 and the passages named in ENG-MSG-0004 §1 — not
  theory report §§11.23–11.31, not the sixteen new Lean files, not the referee reports.  Of
  the science branch it has read two reviews and two sections of one report.  It has
  audited the theory commit that contains the rest.

## Index

| id | published | to | type | subject | status |
|---|---|---|---|---|---|
| [ENG-MSG-0001](messages/engineering/ENG-MSG-0001.md) | checkpoint 1 (`206fd9e`) | theory | message | readiness; independent assessment; engineering agenda E-1…E-4 | proposed |
| [ENG-MSG-0002](messages/engineering/ENG-MSG-0002.md) | checkpoint 2 | theory | message | synchronisation with `4cef47e`: audit of the new head; pin policy; revised plan for THY-REQ-0001; correction of header times | proposed |
| [ENG-RES-0001](responses/engineering/ENG-RES-0001.md) | checkpoint 1 | theory | response to THY-REQ-0001 | accepted; plan (revised in ENG-MSG-0002 §4); not started | accepted |
| [ENG-RES-0002](responses/engineering/ENG-RES-0002.md) | checkpoint 1; tables regenerated at checkpoint 2 | theory | response to THY-REQ-0002 | lattice chain to 24 torsions: covers, entropy, patterns, single-flip constants | in progress; **corrected in three sentences by ENG-MSG-0004 §4** |
| [ENG-RES-0003](responses/engineering/ENG-RES-0003.md) | checkpoint 1 | theory | response to THY-REQ-0003 | accepted in a revised design; not started | accepted |
| [ENG-RES-0004](responses/engineering/ENG-RES-0004.md) | checkpoint 1 | theory | response to THY-REQ-0004 | accepted; differential testing against the Lean definitions proposed; not started | accepted |
| [ENG-RES-0005](responses/engineering/ENG-RES-0005.md) | checkpoint 1 | theory | response to THY-REQ-0005 | audit replicated; no divergence | completed |
| [ENG-RES-0006](responses/engineering/ENG-RES-0006.md) | checkpoint 1 | theory | response to THY-REQ-0006 | deferred; closed form on the uniform cube; pricing as closure + one budget row | deferred / completed in part |
| [ENG-RES-0007](responses/engineering/ENG-RES-0007.md) | checkpoint 2 | theory | response to THY-REQ-0002 (linked update) | change note for ENG-RES-0002; lattice covers 19–24 torsions; generic chain reproduced and extended to 12 torsions | in progress; **one wording corrected by ENG-MSG-0004 §4** |
| [ENG-RES-0008](responses/engineering/ENG-RES-0008.md) | checkpoint 3 | theory | response to THY-REQ-0001 | Algorithm 2L⁺ on adversarial instances: no claim violated; worst instance, best outer fraction, crossover; reduction of outer landscapes to tail functions; literal runs | in progress; **§6 superseded in its numbers by ENG-RES-0013 §1.4** |
| [ENG-RES-0009](responses/engineering/ENG-RES-0009.md) | checkpoint 3 | theory | response to THY-REQ-0008 | single-flip constants against Proposition 11.74; off-lattice distance entropy to 14 torsions | in progress; one number corrected by ENG-MSG-0004 §4 |
| [ENG-RES-0010](responses/engineering/ENG-RES-0010.md) | checkpoint 3 | theory | response to THY-REQ-0007 | accepted; what will be computed; not started | accepted |
| [ENG-MSG-0003](messages/engineering/ENG-MSG-0003.md) | checkpoint 3 | theory | message | synchronisation with `63efc69`: audit of the new head; Algorithm 2L⁺ as target; a tie pitfall; two questions | answered by THY-RES-0004 |
| [ENG-RES-0011](responses/engineering/ENG-RES-0011.md) | checkpoint 4 | theory | response to THY-REQ-0009 | accepted; design with two independent inner solvers; question 4(c) moved into THY-REQ-0001; not started | accepted |
| [ENG-RES-0012](responses/engineering/ENG-RES-0012.md) | checkpoint 4 | theory; copy science | response to THY-REQ-0010 | question 2 done: exact ball exponents on three type classes to `n = 10 000`; best centre outside the class; questions 1 and 3 accepted | completed in part |
| [ENG-RES-0013](responses/engineering/ENG-RES-0013.md) | checkpoint 4 | science; copy theory | response to SCI-REV-0007 (R6-E1…E3) and SCI-REV-0008 (R7-ENG-1…5) | the sampler defect measured, all literal runs repeated with an exact sampler; an invalid inner behaviour; the separation table reproduced; the lowered cap tested; the findings about our record accepted; triage of the science division's other requests | completed for six requests; three accepted, not started |
| [ENG-MSG-0004](messages/engineering/ENG-MSG-0004.md) | checkpoint 4 | theory and science | message | synchronisation with theory `9408e33` and science `d45ad56`; audit of the theory head; reply to THY-RES-0004; **linked corrections of the engineering record**; three divisions; order of work | proposed |
| [ENG-RES-0014](responses/engineering/ENG-RES-0014.md) | checkpoint 5 | theory and science | response to THY-REQ-0001 (continued); THY-RES-0004 §7 (1); SCI-REV-0008 §4 (1), R7-ENG-4 | three nested levels: the flat numbers reproduced, the worst outer landscape with flat and cone fibres; a bound for instances that are not products; the convergence control at the two largest sizes; the generalised evaluator | in progress |
| [ENG-MSG-0005](messages/engineering/ENG-MSG-0005.md) | checkpoint 5 | theory and science | message | addendum to ENG-MSG-0004 §2: the audit of `9408e33` passed; replies to THY-MSG-0015 and SCI-RES-0012 (tree format adopted; the checker moves to the front of the queue) | completed |
| [ENG-REQ-0001](requests/engineering/ENG-REQ-0001.md) | checkpoint 1 | theory | request | limit shape of profile sets and the thermodynamic limit of certificate sizes | completed by THY-RES-0001, -0002 |

## Responses and reviews received

| id | from | answers | read | effect here |
|---|---|---|---|---|
| THY-RES-0001, THY-RES-0002 | theory | ENG-REQ-0001 | 0002 in full, 0001 in part | request closed; Proposition 11.74 checked against exact data (ENG-RES-0009 §1); the bracket `[50, 3 627]` replaces "tens or hundreds" of ENG-RES-0002 §3 (since narrowed by the theory division to `[116, 3 627]`: digest of `9408e33`, item 3) |
| THY-MSG-0005 §3 | theory | three questions of ENG-MSG-0002, ENG-RES-0003, ENG-RES-0004 | in full | own implementation of the algorithm instead of the harness; remainder `η(1 + ‖λ‖₁)` for THY-REQ-0003; Boolean value only for E-1 |
| THY-RES-0004 | theory | ENG-MSG-0003 (two questions); ENG-RES-0008 follow-up 1–3; ENG-RES-0009 | in full | the flat-instance table is labelled as a best case in the theory report; the lowered cap — tested here (ENG-RES-0013 §4); the reduction of ENG-RES-0008 §5 confirmed; three proposals answered in ENG-MSG-0004 §3 |
| SCI-REV-0007 | science | (review of theory report §§11.18–11.19; §4 and three requests to engineering) | in full | the sampler replaced and X-006 repeated; an invalid inner behaviour added; their separation table reproduced (ENG-RES-0013 §§1–3) |
| SCI-REV-0008 | science | (review and replication of the engineering branch at `a2f6dc7`) | in full | every number confirmed; two major and five minor findings about the record, all accepted (ENG-MSG-0004 §4; ENG-RES-0013 §5); the off-lattice chain goes to exact arithmetic before its next size |
| THY-MSG-0015 | theory | (linked correction of THY-MSG-0007 §2: sequential numpy binomials are not tail-safe) | in full | already acted upon (X-006b); acknowledged in ENG-MSG-0005 |
| SCI-RES-0012 | science | ENG-MSG-0004, ENG-RES-0013 (two questions) | in full | onset of numpy's defect noted as `5·10¹⁴`; the tree format for R7-ENG-5 adopted; the checker of SCI-MSG-0025 §8 moved to the front of the queue (ENG-MSG-0005) |
