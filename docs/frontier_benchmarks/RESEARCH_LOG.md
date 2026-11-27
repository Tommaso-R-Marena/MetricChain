# Research log of the Frontier Benchmarking division

*Chronological; times are UTC from the session machine's clock unless a time-stamp token is
cited.  "Resume here" is at the end.*

## 2026-11-26 — founding session

**22:35** Founding directive FB-D-1 received.  Repository inspected: seven branches, the
default being the theory branch; no `research/frontier-benchmarks` yet.  Read-only fetch of
all seven; heads pinned.

**22:37–22:39** Official CASP17 site read (index, message board, target list, Q&A, download
area).  Confirmed: season ended 31 August; results announced for Sunday 29 November; results
page empty; all predictions public; reference and results directories empty.  Scope
clarification FB-D-2 received at about 22:39: CASP17 is one opportunity inside a broader
programme and must not dominate it.

**22:40–22:50** Read directly: the software division's first commit (`720e0ec`: about 1,150
lines on abstract integer tables); engineering's benchmark master plan, readiness test and
results index; science's software-evaluation protocol and benchmark design.  Seven read-only
subagents dispatched (three for intake at pinned commits, four for literature), each with one
written deliverable and explicit read levels.

**22:50–22:55** Branch created at theory checkpoint `b2caab6` (rationale in the sync log);
protocol copy for eight divisions; owner-directive record.  First push accepted.

**22:55–23:03** Decision: time-stamp evidence by RFC 3161 tokens from several unrelated public
authorities (eleven probed with a contentless file; four adopted whose tokens verify against
the machine's ordinary trust store).  Only digests are sent.  Freeze tooling written with 43
tests, most of them planted violations.  **Freeze FRONTIER-FRZ-0001** (public state of CASP17):
attested 23:03:21.  RCSB confirms 19 of 239 target-list entries have released PDB entries.

**23:05–23:15** CASP17 determination written: nothing mature enough for an evaluation before
the release; no prediction produced.  All seven subagent reports received and read in full
(two intake reports by section).  They are committed as delivered, with their read levels.

**23:10–23:17** Decision: ground the first protocol in a pilot.  The public "ProteinFolding"
instances of the 2011 inference challenge (INRAE mirror) were inspected: **10 fixed-sequence
instances** (domains ≤ 81) and **11 with domains up to 350–503, consistent with design
instances — excluded as outside the charter** (the literature assessment had described the
whole category as fixed-sequence).  toulbar2 1.4.0.3 installed.  First run on the smallest
instance: both methods agree; the certificate has no branch node; the serialiser of the
software division's first commit fails on it (recursion).

**23:17–23:36** Assessment protocols, benchmark registry, state-of-the-art register,
contamination audit and mathematical feedback written.  Scoring code (RMSD, lDDT, GDT,
TM-score, side-chain torsions) written with planted-answer tests; one test failed — a sign
error in the *test's* planted torsion, shown by agreement of the code with an independent
library on a crystal structure; corrected and recorded.  Second pilot: nine planted
identification controls of the ensemble division recomputed independently (all replicate);
two reweighting baselines run on them.

**23:36** Second read-only synchronisation: every branch had moved.  The software division
now has a molecular layer and a toulbar2 baseline, has written to us (STRUCTBIO-MSG-0002) and
asks that another division fix and hash a held-out list it does not see; science has written
to us (SCI-MSG-0035); engineering has recorded a directive about us and its own freeze
procedure.  **Our first intake and FRONTIER-MSG-0001 were partly out of date when pushed.**
Decisions: stop the pilot on the stale commit and rerun on the current release `1756529`;
issue linked corrections (FRONTIER-MSG-0002 §1) instead of rewriting.

**23:40–23:43** Held-out list v1 built from the PDB by the software division's proposed rule
plus a release date on or after 2026-07-01 and a secret ordering salt: 150 candidates, 47
representatives.  **Freeze FRONTIER-FRZ-0002** (commitment and encrypted list; passphrase and
commitment salt with the research owner): attested 23:42:32.

**23:44 →** Public CASP17 models of three targets with released references scored with our
code (to be frozen as FRONTIER-FRZ-0003 before the official numbers); pilot rerun on the
software division's current release; results, negative results, synthesis and handoff
written; FRONTIER-MSG-0002, FRONTIER-REQ-0001 (engineering), FRONTIER-REQ-0002 (science).

**23:58** **Freeze FRONTIER-FRZ-0003** (scores of 1,163 public CASP17 model files, with the
comparison plan): attested 23:58:17.

## 2026-11-27

**00:04** One check-in scheduled for 2026-11-30 05:00 UTC (CASP17 results, replies); nothing
else runs between sessions.

**00:23** Pilot on the software division's release `1756529` complete: toulbar2 claims an
optimum on 7 of 10 instances within 300 s; the certified route returns an accepted
certificate on 4 (all equal to toulbar2; 17–326 times slower) and abstains on 6, three of
which toulbar2 closed in under two seconds.

**00:30–00:45** Results, negative results, synthesis, handoff; FRONTIER-MSG-0002,
FRONTIER-REQ-0001, FRONTIER-REQ-0002; checkpoint 2 pushed.

**00:26–00:50** Third synchronisation: five divisions had replied.  No contradiction of the
CASP17 determination; two explicit agreements.  Science's and complexity's criticism adopted
as protocol version 1.1 (strata by tightness of the exact linear relaxation computed in
advance; H2 split; H1 defined; heuristic named; an auditability variable).  FRONTIER-MSG-0003;
checkpoint 3 pushed.

**00:40** Owner directives FB-D-3 and FB-D-4 received: continuation approved; a continuous
improvement loop across the divisions; benchmarks beyond CASP17; "investigate why it performs
poorly".

**00:43–00:58** Fourth synchronisation (two branches had moved).  Decision: diagnose the
certified route before writing to anyone.  Read the producer's bound and search code at the
software division's head (solver files identical to the evaluated release).  Three
hypotheses: weak bound, missing integrality step, slow search.  Root diagnostics on all ten
public instances; the producer asked for a gap just under one cost unit; a profile.  Two
public repositories fetched for planned evaluations (an established side-chain packer; a
maximum-entropy reweighting package with data) — **never used**.

**00:58–01:03** toulbar2's ingredients switched off one at a time.  Learnt on the way: in
depth-first mode its reported dual bound stays at the root value after a completed search, so
"proved" must be read from its `limited` flag — which also means our pilot's "A = 3 of 10"
was wrong (N-19).

**01:00** **Owner directive FB-D-5: controlled consolidation and halt**, with a clarification
asking for an orderly wind-down.  Decisions: let the two bounded diagnostic runs under way
finish (local, minutes; they complete the one investigation in progress) and add one
900-second node count on the three abstaining instances; start nothing else — the planned
evaluations, the subagent investigations and the per-division requests are cancelled and
written up as recommendations; the ablation was cut to its informative rows to end sooner.

**01:03** Fifth and last synchronisation.  The ensemble division had answered our questions
(four of five with propositions; one of our proposals was wrong).  The software division's
intake had found two defects in our records (a dead cross-reference, header times later than
commits); both corrected and recorded.

**01:18** All runs finished.  Result: the bound is not the cause (the producer's is tighter
than toulbar2's on all ten instances); integrality is not the cause; the node rate is — and
900 s do not remove the three abstentions.

**01:20 →** `RESULTS.md` §6 composed from stored rows; negative results N-17 to N-23;
improvement register; benchmark readiness; the consolidation report; FRONTIER-MSG-0004;
handoff.  Verification, commit, push.  The scheduled check-in paused.  **Halt.**

## Decisions and their reasons (for a successor who disagrees)

| decision | reason | what would change it |
|---|---|---|
| no CASP17 prediction of any kind | no method takes a sequence; a repacked public model would be a derivative of a participant's entry; the software division and science independently say the same | a backbone-predicting component with a documented training cut-off |
| RFC 3161 tokens from four authorities | the directive lists independent timestamp evidence; a commit date is written by the committer | an instruction from the owner to use, or not to use, a named service |
| subagent reports committed as delivered | their read levels are part of the evidence; rewriting them would hide what was and was not read | — |
| design instances excluded even "as pure optimisation" | their solutions are designed sequences; the same solver questions are answered by fixed-sequence and synthetic instances | an explicit authorisation from the owner |
| held-out list sealed rather than published | every branch is readable by every division; the software division asked not to see it | — |
| pilots labelled A-EXP and never called validation | the first protocol was written after its first instance was run | — |
| our own two-line baselines in the identification pilot | to learn whether the full comparison is worth requesting; the request names the established packages | — |

## Resume here

**The division is halted by owner directive FB-D-5.  Do nothing below without the research
owner's explicit authorisation.**  When it is given:

1. Read `HANDOFF.md` §§2, 5 and `docs/collaboration/consolidation/frontier-benchmarks.md` §E.
2. **The one obligation with a date behind it:** compare FRONTIER-FRZ-0003 with the official
   CASP17 numbers by the plan in
   `experiments/frontier/freezes/FRONTIER-FRZ-0003_casp17_scoring_check/COMPARISON_PLAN.md`;
   record PASS / EXPLAINED DIFFERENCE / FAIL / NOT ASSESSABLE in `RESULTS.md` §4.
3. One read-only fetch of the seven branches; record it in the synchronisation log; answer
   only what is addressed to this division.
4. Then whichever of the three recommended actions the owner chooses (report §E).  Before any
   protocol is frozen, re-verify at the source every baseline version and every literature
   row it relies on.
