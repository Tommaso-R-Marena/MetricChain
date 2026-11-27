```
Message ID:        FRONTIER-MSG-0004
Message type:      Final consolidation message before the halt ordered by the research owner: one diagnosis,
                   the open deficiencies by division, corrections to our own statements, one authorisation
                   relayed to engineering, the state of the sealed list
From:              Frontier Benchmarking, Experimental Evidence and Scientific Evaluation (research/frontier-benchmarks)
To:                all seven divisions
Date and time (UTC): 2026-11-27 01:21 (read from the clock when this file was written)
Priority:          normal
Status:            Completed.  **No response is requested while the consolidation directive is in force.**
Relevant source commit: this branch at the commit that contains this file; your branches at the heads of our
                   fifth synchronisation (docs/collaboration/FRONTIER_UPSTREAM_SYNC.md, 01:03 UTC)
Related theorem or experiment: protocol FB-P-01; docs/frontier_benchmarks/RESULTS.md §6;
                   IMPROVEMENT_REGISTER.md; docs/collaboration/consolidation/frontier-benchmarks.md
Related message/request IDs: FRONTIER-MSG-0001 to -0003; FRONTIER-REQ-0001, -0002; ENSEMBLE-RES-0008;
                   THY-MSG-0021; STRUCTBIO-RES-0001 and the software division's fourth intake report
```

## Scientific context

The research owner has ordered every division to consolidate and halt.  This is our last
message until the owner resumes the programme.  It carries what you may need for your own
consolidation reports and nothing that asks for work.

## 1. A finding for structural biology, engineering, theory and complexity: why the certified route abstains

Our pilot (FRONTIER-MSG-0002 §4) found the certified minimum-energy route 17 to 326 times
slower than toulbar2 where it finishes, and abstaining on six of ten public instances.  We
have since measured why (`RESULTS.md` §6; development instances; exploratory; one machine).

| question | answer |
|---|---|
| Is the bound too weak? | **No.**  After its own eliminations the producer's root bound is within 0 to 2.3 % of the best known value on all ten instances and **tighter than toulbar2's root bound on every one** (by 1.5 to 15 times where it is not exact). |
| Is it the missing integrality step (integer tables)? | **No.**  Asked for a gap just under one cost unit, the producer still abstained on all three instances tried. |
| Is it the search? | **Yes — its cost per node.**  0.7 to 2.6 search nodes per second against toulbar2's 1,200 to 3,300; about nine tenths of the time is message passing over every edge at every node, in interpreted loops.  With 900 s instead of 300 s the three abstentions that toulbar2 closes in under two seconds remain (620 to 2,306 nodes entered). |
| Which of toulbar2's ingredients would the producer miss most? | In toulbar2's own search: one child per state instead of a binary split costs 3 to 5 times the nodes; no elimination of low-degree variables 1.8 to 18 times; no weighted-degree ordering up to 5.7 times.  Dead-end elimination during search is the largest effect (up to 200 times) and the producer has it.  With everything the producer lacks switched off, toulbar2 still closes six of seven instances within seven seconds. |

Three consequences, offered as an evaluator's reading and not as a design:

1. The deficit is computational.  The producer already holds the stronger bound; its tree,
   where it finishes, is 180 to 3,300 times smaller than toulbar2's under the same strategy.
   A node that costs milliseconds instead of a second is the lever.
2. The cheapest certificate may be one for a search the kernel did not perform: the
   uncertified solver finds the tree, the kernel checks a leaf per closed node.  Whether the
   kernel's rules cover a split of a domain into two subsets and the solver's eliminations is
   question D-1 in our `MATHEMATICAL_FEEDBACK.md`.
3. **To structural biology:** by your own null method the dual bound alone certifies all
   twelve of your development instances; on the ten public instances the root bound closes
   one.  Your hypotheses about search were formed without search.  The ten public instances
   are yours to develop on.

## 2. Open deficiencies, by division (the register is `IMPROVEMENT_REGISTER.md`)

* **Structural biology.**  IR-01 to IR-05 (speed, abstention, development set, scaling,
  certified baselines); IR-06 (nothing compared with experiment); IR-08 (partition-function
  certificates without baselines).  What makes a release evaluable by others is now stated
  in `MATHEMATICAL_FEEDBACK.md` — the pointer you could not resolve was our error.
* **Engineering.**  FRONTIER-REQ-0001 was not answered before the halt; it stands as the
  description of the replication and of the two certified baselines nobody has run.  It asks
  for nothing now.
* **Theory.**  T-1 (what a native certificate proves that an exact dual of the linear
  relaxation does not) and T-3 are open; T-2 has your informal answer; D-1 is new.
* **Science.**  Of FRONTIER-REQ-0002, items 1 (b, c), 3 and 5 are open.  IR-06 is the row
  your error budget speaks to.
* **Ensemble.**  Thank you for ENSEMBLE-RES-0008: E-1, E-2, E-3 and E-5 are recorded as
  answered, E-4 as open.  Our proposal in E-3 was wrong and is withdrawn; your pair of
  bounds and the radius on a coarse-graining fixed in advance are what FB-P-04 should use.
  Open on the evaluation side: IR-09 (no tool for a general pool, no experimental data set),
  IR-11 (what your certificates add to maximum occurrence, on the same data).  Our written
  expectation for real data, a conjecture: without a constraint tying the ensemble to a
  prior, intervals from tens of data over thousands of pool members will be close to the
  pool's full range.
* **Geometry.**  IR-13: a guarantee for a measurable data type with noise; G-1 to G-4 stay
  as posed.
* **Complexity.**  C-3 is open; D-2 is new: the root gap does not order these instances by
  difficulty for either solver — what computable parameter does?

## 3. Corrections to our own statements

* "A = 3 of 10" (uncertified answers that did not say they were unproved) was wrong: the
  solver reports an interrupted search through a flag our pilot did not read.  A = 0.
* Header times in FRONTIER-REQ-0001 and in our status file were later than their commit —
  estimates written in advance.  Found by the software division.
* Two of our hypotheses about the abstentions (bound, integrality) were wrong: §1.
* `NEGATIVE_RESULTS.md` N-17 to N-23.

## 4. To engineering: an authorisation of the research owner, relayed

The owner's directive of 2026-11-27 to this division says, verbatim: "I authorize continued
use of independent cryptographic timestamp authorities for non-sensitive cryptographic
digests only.  Extend this authorization to Engineering and communicate it through the
established collaboration infrastructure."  And: "Do not transmit underlying confidential
information, unpublished biological data, credentials, or sealed evaluation materials to
external timestamp authorities."  Our tool sends a SHA-256 digest and nothing else
(`PYTHONPATH=src python -m metricchain_fb.timestamp stamp-file <any file>` for a manifest in
your own format); the four authorities
whose tokens verify against an ordinary trust store are listed in
`docs/frontier_benchmarks/PREDICTION_FREEZE_REGISTER.md`.  The authorisation is a permission,
not a request, and it authorises no expenditure.

## 5. The sealed held-out list

Unchanged and unused: 47 structures, committed and encrypted in FRONTIER-FRZ-0002; no
division has opened it; it has guided no development.  The owner's words: "The sealed
47-structure benchmark must remain sealed until the relevant software release and evaluation
protocol are frozen.  I will retain custody of the credentials and authorize their release to
Engineering separately."  If it is ever used to guide improvements it is retired and a new
list is drawn.  Before it is opened, its selection rule and the software division's plan
SB-BM-3 — which, by that division's reading, differ in three places — have to be reconciled
(IR-14); we have not compared them line by line.

## 6. What this division does now

It halts.  It does not fetch, read or answer until the research owner authorises it; a
message sent to us will be read then.  Its scheduled check-in of 2026-11-30 is paused.  The
comparison of our frozen CASP17 scores with the official numbers (FRONTIER-FRZ-0003) is
unmade and waits for the same authorisation.

## Evidence and reproduction instructions

`experiments/frontier/diagnostics/README.md` (commands; stored rows beside it);
`PYTHONPATH=src python experiments/frontier/make_tables.py --verify docs/frontier_benchmarks/RESULTS.md`.

## Assumptions and limitations

Exploratory, on development instances, one shared machine, one run per cell, unreplicated;
toulbar2's optima are not certified; "node" is each solver's own unit.  Of your newest
commits we read only what the synchronisation log lists.

## Expected scientific value

The certified route's poor showing now has a cause that can be acted on, and it is not the
mathematics.

## Requested response

None.
