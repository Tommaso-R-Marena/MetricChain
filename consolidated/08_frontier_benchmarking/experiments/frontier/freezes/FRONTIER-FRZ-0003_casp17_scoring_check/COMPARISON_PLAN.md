# Blind check of our scoring code against the official CASP17 numbers — plan fixed before they exist

*Freeze FRONTIER-FRZ-0003, protocol FB-P-10.  Class **A-PLB** (pre-leaderboard): the reference
structures are public PDB entries; the official per-model scores are not public (results
announced for 2026-11-29; the results page said "No results available yet" on 2026-11-26,
freeze FRONTIER-FRZ-0001).  The object under test is this division's scoring code.  No
MetricChain method is involved; the models are the participants' own public predictions;
nothing here is an official CASP result.*

## What is frozen

`scores_T2409_vs_30ZQ.csv`, `scores_T2410_vs_31GL.csv`, `scores_T2411_vs_30ZR.csv`: for every
public model file of the three targets (one row per file), computed by
`experiments/frontier/casp17_scoring_check/score_models.py` with `src/metricchain_fb/scores.py`
at the commit named in the manifest:

| column | definition |
|---|---|
| `gdt_ts_A`, `gdt_ha_A`, `tm_A`, `lddt_ca_A` | CA-based scores against chain A of the PDB entry, over its observed residues (468 to 470 of the 472 target residues, depending on entry and chain; the column `ca_ref_*` gives the number) |
| `gdt_ts_B`, … | the same against chain B (the entry has two chains; the target is a monomer) |
| `lddt_heavy_A` | all-heavy-atom lDDT against chain A; no stereochemistry penalty, no relabelling of chemically equivalent atoms |
| `ca_common_*`, `heavy_atoms_common_A` | how much of the reference the model contains |

Checksums of the model archives and reference files are in the manifest.

## What will be compared, once the official numbers are published

Official per-model GDT_TS, GDT_HA and lDDT for T2409, T2410 and T2411, matched by model file
name, on the evaluation unit that corresponds to the whole target if one is published.

| criterion | threshold | kind |
|---|---|---|
| median absolute difference in GDT_TS | ≤ 0.5 | primary |
| 95th percentile of the absolute difference in GDT_TS | ≤ 2.0 | primary |
| median absolute difference in GDT_HA | ≤ 1.0 | primary |
| 95th percentile of the absolute difference in GDT_HA | ≤ 3.0 | primary |
| median absolute difference in lDDT (ours: heavy atoms, chain A) | ≤ 0.02 | primary |
| Spearman rank correlation over all models, each score | ≥ 0.95 | secondary (most models are near the ceiling: median GDT_TS above 99, so ranks among them are fragile) |
| fraction of models for which our GDT_TS exceeds the official one by more than 0.5 | ≤ 5 % | diagnostic: our search returns lower bounds, so a systematic excess means a different residue range or reference |

The comparison uses whichever of chain A or chain B the official reference corresponds to; if
that cannot be told, both are reported and the better-agreeing chain is named as such, not
silently chosen.

## Outcomes, fixed now

* **PASS** — every primary criterion holds on the matching evaluation unit.
* **EXPLAINED DIFFERENCE** — a primary criterion fails, and recomputation with a documented
  official definition (evaluation units or trimmed residues, a different reference chain,
  alternate locations, stereochemistry penalties or atom relabelling in the reference lDDT)
  restores it.  The explanation is demonstrated by the recomputation, not asserted.
* **FAIL** — an unexplained difference.  Then no score computed with this code is used in any
  reported result until the cause is found.
* **NOT ASSESSABLE** — the official numbers refer to units we cannot reconstruct.  This is
  reported as not assessable, never as passed.

## Known limits, stated in advance

* The three targets are easy (the same 472-residue enzyme with three ligands; nearly all
  models are within 1 Å): the check has little power to distinguish methods and is a check
  of *values*, not of discrimination.  No harder CASP17 target with a public reference is a
  monomer whose models we can score with CA-based tools; the complexes need interface scores
  this code does not have.
* Our GDT and TM-score use a heuristic superposition search, as the reference programs do,
  but not the same one.
* The official evaluation may exclude residues or use domains; that is the first thing to
  check.
