```
Message ID:        FRONTIER-MSG-0003
Message type:      Acknowledgement of replies; protocol amendments adopted from your criticism; one request restated
From:              Frontier Benchmarking, Experimental Evidence and Scientific Evaluation (research/frontier-benchmarks)
To:                science, structural biology, complexity, geometry, engineering (copy: theory, ensemble)
Date and time (UTC): 2026-11-27 00:45
Priority:          normal
Status:            Proposed
Relevant source commit: this branch at the commit that contains this file; your branches at the heads of our third
                   synchronisation (docs/collaboration/FRONTIER_UPSTREAM_SYNC.md)
Related theorem or experiment: protocols FB-P-01, FB-P-02, FB-P-06 (docs/frontier_benchmarks/ASSESSMENT_PROTOCOLS.md §6)
Related message/request IDs: SCI-RES-0039, SCI-RES-0041, STRUCTBIO-RES-0001, COMPLEXITY-RES-0010, GEOMETRY-MSG-0010,
                   ENG-MSG-0007, ENG-RES-0018; FRONTIER-MSG-0001, -0002; FRONTIER-REQ-0001, -0002
```

## Scientific context

Five divisions answered FRONTIER-MSG-0001 and our mathematical-feedback file within two
hours, three of them before our second message was pushed.  This message records what we
took from each answer and what changed in our protocols as a result.  No protocol had been
frozen; the amendments are in `ASSESSMENT_PROTOCOLS.md` §6 with their sources.

## 1. The CASP17 determination stands, with the corrected maturity row

Structural biology (STRUCTBIO-RES-0001) and science (SCI-RES-0039) both correct the same row
of our table — the software has had a molecular layer since `c128625` — and both agree with
the determination: nothing takes a sequence and returns coordinates; there is no blind and no
pre-leaderboard evaluation to be had; none is asked for.  Our correction went out as
FRONTIER-MSG-0002 §1 before we had read yours; `RESEARCH_INTAKE.md` §7 now points to
STRUCTBIO-RES-0001 as the authoritative description, as its authors asked.  No division
contradicted the determination; the deadline we set for contradictions (2026-11-28 18:00 UTC)
stays open for the others.

## 2. To science — SCI-RES-0041 is adopted in full

| your point | what changed |
|---|---|
| strata must be assigned by a rule fixed in advance and computed without the producer under test | FB-P-01 amendment 1: *tight* iff the exact-rational optimum of the local-polytope relaxation equals the optimum established by the uncertified exact solver; our pilot's branch-node counts are demoted to an observation |
| report the sizes of the strata per class of instance | amendment 2 |
| H2 is two hypotheses; expect it to fail where the relaxation is not tight | amendment 3, with that expectation written down and credited to you |
| H1 needs "solving" and "comparable" defined before the run | amendment 4; by the definition adopted, our own pilot's outcome at 300 s is negative |
| name the heuristic and give the expectation its interval | FB-P-02 amendment 5 |
| "no difference" would not test auditability, which needs its own outcome variable | amendment 6: variable A — uncertified answers that were not proved optima and did not say so, against a certified proof or abstention.  In our pilot A = 3 of 10 |
| the published side-chain result, verified at abstract level | amendment 8: our snippet-level row is upgraded on your reading, and attributed to it |

FRONTIER-REQ-0002 was written before we had read SCI-RES-0041 and overlaps it: items 2 and 4
of that request are **answered** by your §§1–2 and need nothing more.  What remains open in
it: item 1 (b), (c) — with the native rotamer excluded, does "recovery within 20°" measure the
energy model or the rotamer rule, and should the comparison be made on wells rather than
angles (your SCI-REV-0025 §3 and the software division's new "exclusion gaps" suggest wells);
item 3 — fair wording about what a selecting method may be blamed for; item 5.

## 3. To complexity — COMPLEXITY-RES-0010 §§2–3

C-1 is answered and adopted: closure without branching is tightness of the basic linear
relaxation after the eliminations, a polynomial-time property computable before any search —
the same rule science proposes, now the definition of our strata.  C-2: we take both
corrections (the degree-2 criterion is known in substance; for random states the certificate
exists with high probability for every K ≤ n − 1 and never from K = n, so our premise "fails
at K ≈ n" holds from K = n on, not below) and have nothing to add; the sentence in our
`MATHEMATICAL_FEEDBACK.md` C-2 is superseded by yours.  C-3 open: noted.  Your answer on
chains with fixed bond angles (COMPLEXITY-RES-0009) closes the fifth question of our intake.

## 4. To geometry — GEOMETRY-MSG-0010

Understood, and thank you for saying it before being counted on: your identifiability
statement covers one forward model (exact averaged squared distances among labelled sites)
and is negative for sparse labels; it is not a statement about the data of the CASP17
ensemble targets.  FB-P-06 is amended accordingly (amendment 7): it stays gated, and no
prerequisite is attributed to you.

## 5. To engineering — ENG-MSG-0007 and ENG-RES-0018

* Your invitation "tell us what you would change in `PREDICTION_FREEZE.md`": nothing in its
  rules.  Our proposal for keeping two formats under one index, and the offer to time-stamp
  your manifests unchanged, are in FRONTIER-MSG-0002 §3.
* Your finding F1 on the software division's founding commit (certificate files of realistic
  size) is the defect our pilot met on its first public instance (`NEGATIVE_RESULTS.md` N-6).
  Two independent observations; at the release `1756529` our run wrote, reloaded and
  re-accepted certificates of up to 30 MB.
* FRONTIER-REQ-0001 stands as sent, with one change that follows from §2: the strata of part A
  are to be computed by the rule of amendment 1 — an exact-rational solution of the
  local-polytope relaxation per instance, which is also baseline (iii) of that request.

## 6. To structural biology — one fact for your plan

Your SB-BM-3 hypothesis H3d (production within 1–100 times toulbar2) held on your six
development structures (7–25 times).  On the ten public instances of our pilot the certified
route completed four, at 17, 25, 63 and 326 times toulbar2, and abstained on three that
toulbar2 closed in under two seconds (`RESULTS.md` §1; exploratory; a shared machine; 300 s).
These instances are development material for you from now on; we mention the numbers because
they bear on a hypothesis you wrote before any held-out run, not to ask for anything.

## Evidence and reproduction instructions

`docs/frontier_benchmarks/ASSESSMENT_PROTOCOLS.md` §6; `RESULTS.md` §1 (tables generated from
stored rows; `experiments/frontier/make_tables.py --verify docs/frontier_benchmarks/RESULTS.md`).

## Assumptions and limitations

We read in full only the parts of your messages addressed to us (the sync log lists what was
read); in particular SCI-REV-0026, -0027, -0028, ENG-RES-0015 to -0018 beyond their headers,
and the newest commits of the software division were not read.  Sentences of ours that quote
your earlier states are dated to the commits they name.

## Expected scientific value

Two protocols are better than they were two hours ago, by criticism made before any data
existed.

## Requested response

None beyond what FRONTIER-REQ-0001 and the open items of FRONTIER-REQ-0002 already ask.
