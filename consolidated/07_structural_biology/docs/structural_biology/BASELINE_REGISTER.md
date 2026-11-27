# STRUCTBIO baseline register: datasets (G) and baseline tools (H)

- **Date:** 2026-11-26.
- **Status:** internal assessment by an AI analyst. Companion to `PRIOR_ART.md`, which defines the evidence labels: `[V]` verified online in this session; `[V-abs]` abstract or snippet only; `[repo]` verified by another MetricChain division; `[mem]` from memory, unverified.
- **Not done:** no tool listed here was installed or run for this register. "Usable now" means usable in principle with the stated licence and install route, not that it has been tested in this repository. The division does run pytoulbar2 1.4.0.3 (per the brief); PyPI shows 1.4.0.3, MIT `[V]`.

## G. Benchmark instance sets

### G1. Fixed-sequence pairwise side-chain models (in scope)

**G1.1 Yanover–Weiss side-chain positioning MRFs, Cost Function Library copy.** This is the primary candidate.

- **Location:** https://forge.inrae.fr/thomas.schiex/cost-function-library, path `real/protein/instances/uai/` `[V]`. The GitLab project was created 2018-09-25 and last active 2026-09-10 `[V]`.
- **Contents:** 240 files named `pdbXXXX.uai.xz`, for example `pdb1a1x.uai.xz` `[V]`.
- **Provenance:** the folder's `readme.txt` reads "Protein side-chain positioning problem as described in Yanover, Chen, and Yair Weiss. Approximate inference and protein-folding. NIPS 15 (2002), pages 1481-1488" `[V]`.
- **Format:** UAI `MARKOV`, one variable per residue with domain equal to the number of rotamers, unary and pairwise factors `[V]`. For example, `pdb1a1x` has 95 variables and 371 factors.
- **Factor values (important):** factors are stored as **Boltzmann-like weights with six decimal places**, floored at `0.000001` and normalised so that the maximum entry is 1 `[V]` (inspected `pdb1a1x`). Three consequences follow:
  - (a) The original energies, the energy function and the temperature are **not** recoverable exactly from the files.
  - (b) The tables *are* exact decimal rationals. On this set, Z is a sum of products of rationals and can be computed or certified **without any exp()**, which takes away much of C2's validated-exponential machinery.
  - (c) The 1e-6 floor truncates the energy, so a "certified" result is certified for the truncated model only.
- **Energy model:** described in the NIPS 2002 paper (SCWRL-type energy and rotamer library) `[mem]`; not read.
- **Licence:** **none stated** in the repository (no LICENSE file; the project licence field is null) `[V]`. Redistribution status is therefore unclear. Cite both the source and the repository, and do not re-host without permission.

**G1.2 PIC2011 / UAI competition instances.** The PIC2011 site (https://www.cs.huji.ac.il/project/PASCAL/) offers "All PR/MAR networks" and "All MPE networks" archives `[V-abs]`. The 2010 UAI approximate-inference evaluation listed a "Protein Folding" category with 21 instances `[V-abs]`. I did not confirm that these are the same Yanover–Weiss models, nor a licence. UAI 2014 benchmark PDFs are at ics.uci.edu/~dechter `[V-abs]`.

**G1.3 OpenGM "protein-folding".** 29 instances, "moderate size with sparse and full connectivity", pairwise potentials, "originally from [JEMF06, EG11]" (Structured Prediction Problem Archive, Swoboda et al., arXiv:2202.03574) `[V-abs]`. No licence was found for the datasets. That they derive from the Yanover–Weiss MRFs is `[mem]`.

The OpenGM **"protein-prediction"** set is, as I recall, a protein–protein *interaction* relational model (Jaimovich et al. 2006) and not side-chain packing `[mem]`. It is out of scope unless verified otherwise.

**G1.4 Structure-level packing test sets.** These are PDB IDs, not pairwise models; STRUCTBIO would have to build its own tables.

- **DB379** (SCWRL4 test set, reused by FASPR). Selected from the Uppsala Electron Density Server with ligands other than water removed, PISCES ≤ 30% identity, resolution ≤ 1.8 Å, R ≤ 20% `[V]`. IDs are in SCWRL4 Supplementary Data and FASPR Supplementary Table S6 `[V]`.
- **FASPR datasets** (native, I-TASSER models, 10 perturbed-backbone sets): "freely available" at https://zhanglab.ccmb.med.umich.edu/FASPR `[V]`.
- The underlying PDB coordinates are public (wwPDB, CC0) `[mem]`.

### G2. Design instances (out of scope; do not use as headline benchmarks)

- The CPD benchmark sets of Allouche et al. 2014 / Traoré et al. 2013 / Simoncini et al. 2015 (toulbar2 group).
- The OSPREY design examples.
- The K\* and binding-site systems of Viricel et al. CP 2016. Those are partition-function sub-problems of binding affinity; the authors "intend to make this benchmark ... available" `[V]`, and availability was not checked.

These have mutable positions, that is, sequence choice. Fixed-sequence sub-problems extracted from them would count as G1 only if regenerated with a single amino-acid identity per position, and they must be labelled as such.

## H. Baseline tools

| Tool | Version checked | Licence | What it guarantees | How to run on the *same* pairwise instance | Known limitations | Status |
|---|---|---|---|---|---|---|
| **toulbar2 / pytoulbar2** | pytoulbar2 1.4.0.3 (PyPI) `[V]`; docs 1.0.0 `[V]` | MIT `[V]` | Exact optimum for integer costs. Z\*ε (1+ε) bracket (Viricel et al. 2016, double precision) `[V]`. `-logz` on `.uai` input, no stated bound `[V]` | Reads `.uai`, `.cfn`, `.wcsp` directly `[V]`. Energies are scaled and rounded to integers `[mem]`, so STRUCTBIO must feed **the same integerised costs** to both sides | No proof output `[V]`. Floating point in counting. No marginal bounds | **Usable now.** Primary GMEC and Z baseline |
| **PB route:** RoundingSat + VeriPB + CakePB | not checked | RoundingSat MIT `[mem]`; VeriPB MIT `[mem]` | Checkable optimality proof; CakePB verified in HOL4 `[repo]` | Encode the CFN as PBO (one-hot rotamer variables, pair indicators) with integer costs | Encoding size grows with the number of pairs; overhead "within a factor of about 20" (Koops et al. 2025) `[V-abs]` | **Needs work.** Encoder must be written. Key comparator for C1 |
| **MIP route:** exact SCIP + VIPR | SCIP 10 `[repo]` | Apache 2.0 `[mem]` | Exact rational MIP optimum with VIPR certificate `[repo]` | Kingsford-style ILP from the same integer tables | Exact mode is slow; certificate size | **Needs work.** Second C1 comparator |
| **OSPREY 3** | not checked | GPL-2.0 `[V]` (repo LICENSE) | DEE/A* GMEC; K\*/BBK\*/MARK\* ε-brackets, in floating point, over minimised energies `[repo]` | Builds its own energies from PDB with AMBER-type terms `[mem]`. Feeding external pairwise tables needs custom code `[mem]` | Design-oriented. **PyPI "osprey" 1.1.0 is an unrelated MSMBuilder hyperparameter tool** `[V]` | **Needs work.** Only rigid, fixed-sequence mode is comparable |
| **Exact junction tree** (libDAI JTree) | not checked | BSD-2-clause `[V]` (dbtsai/libDAI mirror LICENSE) | Exact Z and marginals up to double rounding `[mem]` | Reads factor graphs. A UAI→`.fg` conversion is needed `[mem]` | Memory exponential in treewidth. Floating point | **Usable now** for low-treewidth instances. The reference for log Z and marginals |
| **BP / GBP / mean field** (libDAI; pgmpy) | pgmpy 1.1.2 (PyPI) `[V]` | libDAI BSD-2 `[V]`; pgmpy MIT `[V]` | None (approximate) | Same factor tables | No bounds | **Usable now** as an *uncertified* reference only |
| **Mooij–Kappen box propagation** | not checked | unknown | Rigorous marginal bounds in exact real arithmetic; implemented in floating point `[V-abs]` | Same factor graph | Code availability unverified (possibly in libDAI) `[mem]` | **Needs work.** Locate code. The only generic marginal-bound baseline found |
| **WMB / AND/OR anytime Z bounds** (Ihler group: Merlin, pyGMs; daoopt) | not checked | daoopt GPL per README `[V]`; Merlin and pyGMs unverified | Deterministic upper and/or lower bounds on Z, in floating point `[repo]` | Read `.uai` `[mem]` | Repository locations and licences unverified (IBM/merlin raw files returned 404) | **Needs work** |
| **SCWRL4** | not checked | Free non-profit/academic licence by request form; commercial licence separate `[V]` | None (heuristic; "not guaranteed to find the global minimum") `[V]` | **Cannot** take external pairwise tables; PDB in, PDB out | Own energy and library. Restricted redistribution | **Excluded** from same-instance comparisons. Allowed only for structure-level χ accuracy context |
| **FASPR** | not checked | MIT `[V]` | None (heuristic cuts and edge decomposition) `[V]` | PDB in, PDB out; own energy | Same as SCWRL4 | **Excluded** from same-instance comparisons. Structure-level context only |
| **Rosetta / PyRosetta packer** | not checked | Non-commercial licence; commercial and fee-for-service use needs a separate licence; conda mirrors at conda.rosettacommons.org `[V-abs]` | None (simulated annealing) `[mem]` | Can dump its own pair energies `[mem]`, but those are a different model | Licence restricts redistribution of outputs and derived code `[mem]` | **Excluded** for now (licence and model mismatch) |
| **OpenMM** | 8.6.1 (PyPI) `[V]` | Mostly MIT, some parts LGPL `[V]` | Force-field energy evaluation, no optimisation guarantee | Could *generate* rational pairwise tables from PDB plus a rotamer library (an STRUCTBIO pipeline step) | Not a solver | **Usable now** as an energy generator, not as a baseline |
| **Arb/FLINT** (python-flint) | python-flint 0.9.0 `[V]` | LGPL `[mem]` | Rigorous ball enclosures | Implementation dependency | Must appear in the trust base | **Usable now** (dependency) |
| **qFit 3** | not checked | Permissive Stanford/MIT-style `[V]` | None (experimental-data model building) | Not on pairwise instances | Different observable | Scientific comparator only (section D) |

### Recommended minimal fair baseline set

All baselines run on **the same pairwise instance, with the same integerised or rational tables**.

1. **GMEC (C1).**
   - toulbar2: time to the optimum, no proof.
   - The PB route (RoundingSat+VeriPB, checked by CakePB) and/or exact SCIP+VIPR: time to the optimum plus proof, then proof size and check time.
   - The C1 claim stands or falls on this three-way comparison.
2. **log Z (C2).**
   - Exact junction tree where treewidth permits (ground truth in double precision, re-checked in exact rationals on small instances).
   - toulbar2 Z\*ε at an ε that matches STRUCTBIO's enclosure width.
   - One WMB or AND/OR bounding code, if it can be installed.
   - On G1.1, also an exact rational sum, because no exponentials are involved there.
3. **Marginals (C2).**
   - Exact junction tree marginals (reference).
   - Mooij–Kappen bounds (the generic bounded competitor).
   - BP and mean field, labelled "uncertified".
4. **Ensemble identification (C3).** A floating-point LP (HiGHS or SciPy) computing the same ranges, plus MaxOcc-style weight bounds. The question is whether exact certificates change any reported conclusion.

### Additions of 2026-11-27 (after the science division's review SCI-REV-0026 §7)

1. **The null method for GMEC**: the exact-rational dual bound of the pairwise relaxation alone
   (no eliminations, no search).  In our format that is a certificate with a single leaf on
   the full box, so it needs no other software; the count "certified by the leaf alone" per
   instance is owed and not yet made.
2. **Search separated from certificate format**: translate *our own* derivation into the
   pseudo-Boolean proof format — a dead-end elimination is a redundance-based strengthening
   whose objective condition is the Goldstein inequality, a dual-bound leaf is a linear
   combination of the pair inequalities (the science division's reading of the published
   rules, from memory, untested) — and have the verified checker check it.  This also gives
   one real instance a check by a verified checker.  Not implemented; proposed to the
   engineering division with STRUCTBIO-REQ-0001.
3. **For line 2 of the budget (discretisation)**: the provable incumbent is dead-end
   elimination with continuous rotamers (MinDEE; iMinDEE in OSPREY).  As a solver comparison
   it remains excluded (a different optimisation problem); the measurement owed is SB-BM-7
   (rigid minimum against the per-well continuous minimum of the same energy).
4. **Certified baseline for C2**: rational bounds of each Boltzmann factor, then
   machine-checked weighted model counting (CPOG) twice — the count is monotone in every
   weight.  Not installed; proposed.
5. **Context for SB-BM-6**: learned packers (DLPacker, AttnPacker) next to FASPR, SCWRL4 and
   the Rosetta packer; none is a same-instance baseline.

## Comparisons that would be meaningless (avoid)

1. **Certified GMEC energy versus SCWRL4, FASPR or Rosetta energies or runtimes.** These use different energy functions, rotamer libraries and pruning. Even a comparison of χ accuracy against their published DB379 numbers (for example SCWRL4's 86% χ1 within 40° `[V-abs]`) compares models, not solvers.
2. **Design-instance results (G2) presented as fixed-sequence performance**, or the reverse.
3. **Certified versus uncertified at different accuracy.** Examples: STRUCTBIO's enclosure of width w against Z\*ε at a different ε, or against toulbar2 `-logz` without a stated bound. Runtimes must be compared at matched guarantee strength and width, and the certificate-check time must be reported separately.
4. **Exact rational results versus floating-point tools on different discretisations.** If toulbar2 rounds energies to integers, STRUCTBIO's certificate must be for the same rounded model, or the difference must be quantified.
5. **K\*/MARK\* brackets over continuously minimised energies versus rigid-rotamer enclosures.** These are different partition functions.
6. **BP or mean-field "accuracy" versus certified marginals without exact ground truth.**
7. **Agreement with NMR χ1 populations or qFit alternates presented as validation of the certificate.** That agreement tests the force field and the library.
8. **Temperature sweeps on G1.1.** The files encode a fixed, undocumented temperature in their weights.
9. **Cross-hardware or cross-time-limit runtime claims**, and any comparison against numbers taken from papers rather than re-run.
