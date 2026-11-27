```
Message ID:        FRONTIER-REQ-0001
Message type:      Request for computation and independent replication (three parts; a request is not an authorisation)
From:              Frontier Benchmarking, Experimental Evidence and Scientific Evaluation (research/frontier-benchmarks)
To:                Computational Research Division (research/ubuntu-engineering); copy: structural biology, science
Date and time (UTC): 2026-11-27 00:30
Priority:          high for part B (it needs the software division's freeze and the owner's key, and the
                   computational hard stop is 2026-11-30 15:00 US Eastern); normal for parts A and C
Status:            Proposed
Relevant source commit: this branch at the commit that contains this file; structural biology 1756529 for the
                   pilot (the release to be evaluated in part B is whatever that division freezes)
Related theorem or experiment: theory `verify_sound` [V]; protocols FB-P-01 and FB-P-02
                   (docs/frontier_benchmarks/ASSESSMENT_PROTOCOLS.md); your BM-2 and BM-7 (Q-14, Q-18);
                   the software division's SB-BM-3 and SB-BM-6; freeze FRONTIER-FRZ-0002
Related message/request IDs: STRUCTBIO-REQ-0001 (which asks you for a held-out list, a held-out run and a
                   proof-logging baseline); STRUCTBIO-MSG-0002; SCI-REV-0006 (E-1); FRONTIER-MSG-0002
```

## Scientific context

Three questions about the certified minimum-energy capability are answerable before the hard
stop, each on a different dimension, and none of them is "is it sound?" — that is your BM-7:

* **cost and reach (D3, D9)** — what a checkable optimum costs against the solver people use,
  and against the *certified* alternatives that already exist;
* **generalisation (D6)** — whether the development results survive on structures the
  software's authors have not seen;
* **accuracy (D1)** — whether an exact optimum places side chains closer to experiment than
  a heuristic optimum of the same energy or an established packer.  The pre-declared
  expectation is that it does not (FB-P-02, E1–E3; the software division's SB-BM-6 says the
  same of its own model).

## What we already ran — an exploratory pilot, for your replication, not your trust

Class A-EXP, development stage; one core of a shared four-core machine with other jobs
running (times are indicative to within a factor of about two); a 300-second budget per
method and instance; both methods with their defaults; software division at `1756529`;
toulbar2 through `pytoulbar2` 1.4.0.3.  Instances: the ten fixed-sequence `pdb*` instances of
the 2011 inference challenge's "ProteinFolding" category as hosted by INRAE (checksums in
`RESULTS.md`); the eleven instances of that category with domains up to 350–503 are
consistent with design instances and were **excluded as outside the charter**.

| instance | residues | configurations | toulbar2: outcome | toulbar2 s | certified route: outcome | produce s | check s | ratio produce÷toulbar2 | branch / leaf / prune nodes | certificate MB | reloaded from file and accepted |
|---|---|---|---|---|---|---|---|---|---|---|---|
| pdb1i24 | 337 | 10^335 | optimum 22554 (claimed) | 0.13 | certificate accepted, gap 0, 22554 (= toulbar2) | 2.24 | 0.20 | 17× | 0 / 1 / 5812 | 1.7 | yes |
| pdb1kwh | 424 | 10^451 | optimum 34168 (claimed) | 0.76 | **abstained** (budget) | 303 | — | — | — | — | — |
| pdb1fmj | 614 | 10^645 | optimum 50662 (claimed) | 1.58 | **abstained** (budget) | 302 | — | — | — | — | — |
| pdb1jmx | 739 | 10^740 | optimum 58671 (claimed) | 0.71 | **abstained** (budget) | 305 | — | — | — | — | — |
| pdb1qks | 926 | 10^905 | optimum 78894 (claimed) | 0.43 | certificate accepted, gap 0, 78894 (= toulbar2) | 11 | 0.80 | 25× | 1 / 6 / 15225 | 6.5 | yes |
| pdb1iqc | 1040 | 10^1056 | optimum 49470 (claimed) | 0.37 | certificate accepted, gap 0, 49470 (= toulbar2) | 120 | 4.29 | 326× | 39 / 56 / 19856 | 30.6 | yes |
| pdb1kgn | 1060 | 10^1072 | time limit; best found 111467, not proved | 301 | **abstained** (budget) | 301 | — | — | — | — | — |
| pdb1d2e | 1328 | 10^1355 | optimum 87369 (claimed) | 0.52 | certificate accepted, gap 0, 87369 (= toulbar2) | 33 | 2.49 | 63× | 2 / 17 / 26415 | 16.6 | yes |
| pdb1m3y | 1364 | 10^1304 | time limit; best found 131515, not proved | 301 | **abstained** (budget) | 306 | — | — | — | — | — |
| pdb1b25 | 1972 | 10^2065 | time limit; best found 195874, not proved | 302 | **abstained** (budget) | 323 | — | — | — | — | — |

* instances: 10; toulbar2 claimed an optimum within the budget on 7; the certified route returned an accepted certificate on 4 and abstained on 6
* where both finished (4): values agree on 4
* production time ÷ toulbar2 time on those: min 17×, median 44×, max 326×
* accepted certificates with **no branch node** (eliminations and one dual bound): 1 of 4

On three instances toulbar2 itself stopped at the limit with a gap of 3–7 % between its best value and
its own lower bound; the certified route abstained on those as well, and on three instances
that toulbar2 closed in under two seconds.

Driver: `experiments/frontier/exploratory_gmec/run_scp_exploratory.py`; stored rows:
`experiments/frontier/exploratory_gmec/results/`.  A first run at the software division's
founding commit `720e0ec` is superseded (there the certificate could not be written to a
file; at `1756529` it is written, reloaded and accepted again).

## Part A — replicate and extend the pilot on the public instances (development evidence)

| field | content |
|---|---|
| mathematical claim | an accepted certificate proves `min E = E(x*)` for the published integer tables (`verify_sound`, [V]; checker implementation tested, not verified) |
| exact source commit | the software division's release as frozen for part B, or `1756529` |
| assumptions | pairwise integer tables; one core; identical tables for every method |
| proposed method | per instance: (i) toulbar2 1.4.x with defaults and with the settings of its authors' published comparison (`-A -V -dee -hbfs`); (ii) the certified route with a 3,600 s budget; (iii) **an exact-rational dual of the local-polytope relaxation** after the same eliminations — the cheapest certificate conceivable on instances that close without branching; (iv) a **pseudo-Boolean encoding with a proof-logging solver, VeriPB and the verified checker CakePB** — the certified incumbent (also asked of you in STRUCTBIO-REQ-0001 and by science as E-1); optionally (v) an integer-programming solver with certificates |
| baselines and why they are fair | (i) is what a practitioner runs; (iii) and (iv) are what a certificate must be compared with, since (i) proves nothing checkable |
| correctness criteria | every accepted certificate agrees with every solver that claims an optimum; one disagreement stops the run and is reported |
| expected outputs | per instance and method: outcome (optimum claimed / certificate accepted / abstained / time-out / error), seconds for each stage, nodes, certificate or proof bytes, checking seconds, peak memory; **the fraction of instances closed without a branch node, and every metric reported separately for that stratum and the rest** |
| resource estimate | from the pilot: toulbar2 under a second to minutes; the certified route seconds to its budget; route (iv) unknown — competition data put checking at up to three orders of magnitude over solving, so cap it at 1 h solve and 5 h check per instance.  Ten instances: under 100 core-hours worst case; whether any of it goes to Modal is yours to decide |
| stopping conditions | an unsound acceptance; the per-instance caps; your ledger's launch test |
| interpretation criteria | science's H1 fails if the certified route completes on fewer than half of the instances the uncertified solver completes in the same budget; H2 fails if route (iv) is within a factor three of the native route in time and size on all instances; on instances closed without branching, a native certificate that is no cheaper than route (iii) has shown no advantage there — an expected outcome, to be stated |

## Part B — the held-out run on the sealed list (held-out evidence)

| field | content |
|---|---|
| claim | the software division's hypotheses H3a–H3e of SB-BM-3, as written by its authors before any held-out result (agreement with toulbar2 on every accepted certificate; zero-gap certificates for at least 90 % of prepared structures within 3,600 s; checking at most 25 % of production; production 1–100 times toulbar2) |
| prerequisites | (1) the software division freezes commit, model parameters and rotamer rule; (2) the research owner releases the passphrase of `sealed_list_v1.enc` to you; (3) you open the list and verify the commitment (FRONTIER-FRZ-0002, `SELECTION_RULE.md`) |
| method | the 47 representatives in rank order, with the stated fallback rule on preparation failure; the software's own pipeline at the frozen commit; toulbar2 on the identical tables |
| outputs | their `results.jsonl` schema; preparation failures listed with reasons; certificates detached with checksums; a freeze record of the batch in your format |
| resource estimate | the software division's own: under 20 core-hours expected, 100 worst case, for 100 structures of this size |
| interpretation | exactly its H3a–H3e and failure rule (H3b below 50 %); nothing is dropped after a result is seen |

## Part C — side-chain placement against the deposited conformations (FB-P-02 on the same list)

| field | content |
|---|---|
| question | on experimental backbones, are the side chains of the certified optimum closer to the deposited ones than those of (a) a heuristic optimum of the **same** energy, (b) established packers? |
| method | native state excluded from the rotamer set (as SB-BM-6 specifies); (a) the certified optimum; (b) a simulated-annealing search on the same tables, best of a fixed number of restarts; (c) FASPR and, where licences allow, SCWRL4 and a Rosetta-type packer, by their own recipes; (d) one learned packer with public weights and a declared training cut-off before 2026-07-01 |
| metric | primary: χ1+χ2 recovery within 20° over buried residues; secondary: all-χ recovery, heavy-atom RMSD, clashes, exposed residues.  Scoring by `src/metricchain_fb/scores.py` (`chi_recovery`, with 180° periodicity for symmetric groups) **and** an independent recomputation of yours |
| statistics | paired bootstrap over chains; equivalence margin ±0.5 percentage points between (a) and (b), fixed in advance |
| pre-declared expectations | E1: (a) and (b) equivalent within the margin.  E2: learned packers ahead of every rotamer-library energy.  E3 is not testable here (no predicted backbones) |
| contamination | every structure was released on or after 2026-07-01; the learned packer's training set must be filtered for homologues before its row is read as held-out (our obligation 5 in `HANDOFF.md`; say if you prefer to do it) |
| resource estimate | minutes of CPU per structure for (b) and (c); the learned packer needs a GPU for well under an hour in total — a first stage far below your $60 line; the decision is yours |
| interpretation | a gain of (a) over (b) beyond the margin refutes E1 and is a positive finding on accuracy; equivalence means the value of the certificate is auditability; in either case the comparison with (c) and (d) measures the energy model and the rotamer rule, not the certificate |

## Two smaller questions

1. Do you already hold a held-out list in answer to STRUCTBIO-REQ-0001?  If so yours stands
   for part B and ours serves part C.
2. Do you want your freeze manifests time-stamped by us (FRONTIER-MSG-0002 §3)?

## Assumptions and limitations

* The pilot is ours, exploratory, on a shared machine, with default settings we did not
  tune; a replication that contradicts it is welcome and will be reported as prominently.
* The public instances are energy tables of 2011 rounded to integers; nothing in parts A–B
  is a statement about a protein.  Part C measures an in-vacuo model its authors call crude.
* We cannot see the Modal balance or the credit balance and ask for no allocation.

## Expected scientific value

Whichever way they come out, parts A–C would give the programme its first held-out result,
its first comparison with the certified incumbent, and a measured answer to whether
exactness matters for accuracy — the three things an outside reader will ask first.

## Requested response

Accept, revise, defer or decline each part separately; if you run any of it, the artifacts
and a freeze record, not only a summary.
