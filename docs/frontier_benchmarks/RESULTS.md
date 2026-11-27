# Results

*Frontier Benchmarking division.  Version 1, 2026-11-27 (UTC).  Read `NEGATIVE_RESULTS.md`
with this file.  Every table below is generated from stored result files by
`experiments/frontier/make_tables.py` (`--verify docs/frontier_benchmarks/RESULTS.md` checks
that the tables in this document are the generated ones).*

**Nothing in this file is validation.**  §§1–2 are exploratory pilots (assessment class
A-EXP, evidence stage *development*) run by this division on its own machine to find out
which evaluations are worth requesting; they informed the protocols and therefore cannot test
them.  §3 is about our own instruments.  §4 is a freeze whose outcome is not yet known.

## 1. Pilot of FB-P-01 — a certified optimum against toulbar2 on public fixed-sequence instances

**Setting.**  The structural-biology division's certified minimum-energy producer and
checker (`metricchain_sb.gmec`, `mincheck`) at its release `1756529`, run unmodified from a
detached copy, against toulbar2 1.4.0.3 (`pytoulbar2`, default settings).  Identical integer
tables for both.  One process each on a shared four-core machine on which other jobs were
running: wall times are indicative to within about a factor of two.  Budget 300 s per method
and instance.  A toulbar2 result counts as "optimum (claimed)" only if the solver's own
global lower bound had reached its best value before the limit.

**Instances.**  The ten `pdb*` instances of the "ProteinFolding" category of the 2011
Probabilistic Inference Challenge as hosted in INRAE's EvalGM repository (weighted-CSP
format; 337–1,972 residues, at most 81 rotamers per residue, integer costs).  They are
fixed-sequence side-chain-placement tables.  **Excluded:** the eleven instances of the same
category with 33–40 variables and domains up to 350–503 — consistent with design instances,
outside the charter; only their headers were read.  SHA-256 of each instance file is in the
stored rows.  We know nothing about the energy function behind these tables beyond its date.

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

Summary (generated):

* instances: 10; toulbar2 claimed an optimum within the budget on 7; the certified route returned an accepted certificate on 4 and abstained on 6
* where both finished (4): values agree on 4
* production time ÷ toulbar2 time on those: min 17×, median 44×, max 326×
* accepted certificates with **no branch node** (eliminations and one dual bound): 1 of 4

**What the pilot shows, by dimension.**

* **D9 (guarantees).**  Wherever both methods finished, the certified value equals
  toulbar2's.  Each accepted certificate covered the full state space, was written to a
  file, reloaded from text and accepted again.  This is the first run of the certified route
  on instances its authors did not build.
* **D3 (efficiency).**  The certified route is slower than toulbar2 by the factors in the
  table and returns nothing within the budget on instances that toulbar2 finishes in
  seconds.  It is a Python prototype a few hours old against a mature solver; the pilot
  cannot say how much of the gap is intrinsic.
* **D10 (recognising insufficient evidence).**  When it could not finish, the certified
  route abstained; it never returned an unproved value.  on three instances toulbar2
  returned its best value at the limit with a gap of 3–7 % to its own lower bound, through an
  interface that does not distinguish that case unless the caller compares the two numbers —
  our own first run mislabelled it (N-10).
* **Structure of the certificates.**  Thousands of eliminations and few dual bounds; little
  or no branching (the node counts in the table).  This is the stratum on which a kernel
  certificate is, in substance, an exact dual of the linear relaxation with an elimination
  trace (question T-1).
* **Not shown:** anything about proteins; any comparison with the certified incumbents
  (proof logging with a verified checker; exact rational duals), which nobody has run.

**Superseded first run.**  At the software division's founding commit `720e0ec` (four
instances before it was stopped): the same agreements and abstentions, and certificates that
could not be serialised.  Rows kept in
`experiments/frontier/exploratory_gmec/results/scp10_at_720e0ec_partial.jsonl`; not used
above.

## 2. Pilot of FB-P-04 — independent recomputation of planted identification controls, and two baselines

**Setting.**  The ensemble division's `controls_v1.json` at `2d2054d` (SHA-256
`48f095b1…8a4e`); the nine controls on a finite space with data linear in the ensemble.  (1)
*Replication* by code written here from the definitions: published data recomputed in exact
rational arithmetic; published certificates checked exactly; verdicts re-derived by a linear
programme plus an exact rank test; intervals recomputed.  (2) *Baselines* on the same data
from a uniform prior over the stated space: maximum-entropy reweighting and non-negative
least squares — **our own few-line implementations of the published algorithms, not the
established packages**.  "Distance to planted" is total variation.

| control | published verdict | recomputed here | published certificate checked exactly | maximum-entropy baseline: data misfit / distance to planted | least-squares baseline: data misfit / distance to planted |
|---|---|---|---|---|---|
| B1-01 | IDENTIFIED | IDENTIFIED | yes | 7e-06 / 0.00 | 3e-16 / 0.00 |
| B1-02 | IDENTIFIED | IDENTIFIED | yes | 2e-05 / 0.00 | 2e-16 / 0.00 |
| B2-01 | NOT_IDENTIFIED | NOT IDENTIFIED | — | 0e+00 / 0.50 | 3e-16 / 0.00 |
| B2-02 | NOT_IDENTIFIED | NOT IDENTIFIED | — | 2e-05 / 0.00 | 0e+00 / 0.50 |
| B2-03 | NOT_IDENTIFIED | NOT IDENTIFIED | — | 1e-05 / 0.50 | 4e-16 / 0.00 |
| B4-01 | IDENTIFIED | IDENTIFIED | yes | 1e-05 / 0.00 | 4e-16 / 0.00 |
| B5-01 | INTERVAL ['-3/10', '7/10'] | interval [-0.3, 0.7] | — | 8e-07 / — | 4e-16 / — |
| B5-02 | INTERVAL ['0', '7/20'] | interval [0.0, 0.35] | — | 8e-07 / — | 4e-16 / — |
| B5-03 | INTERVAL ['-2/5', '4/5'] | interval [-0.4, 0.8] | — | 8e-07 / — | 4e-16 / — |

**What the pilot shows.**

* **D8 (reproducibility), D5 (calibration).**  All nine verdicts, all published certificates
  and all three intervals are reproduced by independent code.  These controls had been
  "verified by their generator only".
* **D10.**  On the three planted NOT IDENTIFIED controls both baselines fit the data to
  rounding error and each returns a single ensemble; in three of the six baseline–instance
  pairs that ensemble is at distance 0.5 from the planted one, in the other three it
  coincides with it — and which baseline is "right" changes from instance to instance.
  Nothing in either baseline's output distinguishes the two situations.  A maximum-entropy
  method does not claim to identify — it selects; the point is that a user cannot tell from
  the output that a selection was made (wording under review: FRONTIER-REQ-0002 item 3).
* On the identified controls both baselines recover the planted ensemble (the
  maximum-entropy one to the accuracy of its regularisation).
* **Not shown:** anything about the established reweighting packages or about real data.

## 3. Conformance of our own scoring instruments

`src/metricchain_fb/scores.py` (RMSD, lDDT, GDT_TS/HA, TM-score for a fixed correspondence,
side-chain torsions and recovery), tested in `tests/frontier/test_scores.py`:

| control | planted answer | outcome |
|---|---|---|
| identity and rigid motion | RMSD 0, lDDT 1, GDT 100, TM-score 1 | as planted (three chains) |
| mirror image | lDDT exactly 1 (distances are preserved); RMSD, GDT, TM-score must see it | as planted — recorded as a blind spot of distance-based scores (N-12) |
| two rigid domains moved 200 Å apart | GDT at every cut-off = size of the larger domain; lDDT = fraction of intra-domain contacts | exact, for three splits |
| noise of known size | RMSD = σ√3 within 8 %; lDDT and GDT decrease monotonically | as planted |
| planted torsion and side-chain rotation | χ1 changes by exactly the applied angle, χ2 unchanged; recovery flips at the tolerance | as planted (after correcting the sign of our own planted torsion, N-11) |
| symmetric side-chain groups | a 180° flip of an aromatic ring or carboxylate is the same conformation | as planted |

Agreement with independent implementations: lDDT with `biotite` 2.0.0 on synthetic chains
(to 2·10⁻³) and on real CASP17 models (four decimals on the six models compared);
TM-score with TM-align (`tmtools` 0.3.0) to 0.02 on synthetic chains and four decimals on
real models; side-chain torsions with `biotite` on a 0.945 Å crystal structure (PDB 1CRN)
to 0.01°.  No independent GDT implementation was available to us; GDT rests on the planted
controls until the official CASP17 numbers arrive (§4).

## 4. Frozen, outcome pending: our scores of public CASP17 models (FRONTIER-FRZ-0003)

Class A-PLB.  Scores of every public model file of three CASP17 targets against the released
PDB references, frozen on 2026-11-26T23:58:17Z, before any official number existed.

| target (reference) | model files | groups | median GDT_TS | 10th–90th percentile GDT_TS | median GDT_HA | median lDDT (heavy atoms) | mean abs. difference of GDT_TS between reference chains A and B (max) |
|---|---|---|---|---|---|---|---|
| T2409 (PDB 30ZQ) | 387 | 82 | 99.31 | 89.23–99.79 | 94.19 | 0.931 | 0.28 (1.86) |
| T2410 (PDB 31GL) | 385 | 81 | 98.94 | 94.20–99.63 | 93.30 | 0.929 | 0.44 (1.75) |
| T2411 (PDB 30ZR) | 391 | 83 | 99.20 | 95.53–99.68 | 93.94 | 0.931 | 0.19 (0.69) |

The targets are three complexes of one 472-residue enzyme with different ligands; nearly all
models are within 1 Å.  The thresholds for agreement with the official numbers and the four
possible outcomes are fixed in the freeze's `COMPARISON_PLAN.md`.  **No outcome is claimed.**

## 5. Freezes made in the founding session

| id | content | attested (UTC) |
|---|---|---|
| FRONTIER-FRZ-0001 | public state of CASP17 before the results | 2026-11-26T23:03:21Z |
| FRONTIER-FRZ-0002 | sealed held-out list of 47 structures (commitment and encrypted list) | 2026-11-26T23:42:32Z |
| FRONTIER-FRZ-0003 | score tables of §4 with their comparison plan | 2026-11-26T23:58:17Z |

All three verify (`python -m metricchain_fb.freeze verify experiments/frontier/freezes`); each
carries tokens from four time-stamping authorities that verify against the system trust
store.
