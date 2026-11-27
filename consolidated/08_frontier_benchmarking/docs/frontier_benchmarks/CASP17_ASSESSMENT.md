# CASP17: what is feasible, what is not, and what was done instead

*Frontier Benchmarking division.  Version 1, 2026-11-26 23:10 UTC.  Everything stated about
CASP17 was read from the official site (`https://predictioncenter.org/casp17/` and pages
linked from it) between 22:37 and 23:02 UTC on 2026-11-26 unless a line says otherwise; the
record of what was public at that time is freeze **FRONTIER-FRZ-0001**
(`experiments/frontier/freezes/FRONTIER-FRZ-0001_casp17_public_state/`, manifest SHA-256
`899f916e…0d29`, time-stamped by four unrelated authorities at 2026-11-26T23:03:21–23Z).*

> **Version 2 note, 2026-11-26 23:50 UTC.**  §4.2 and reason 1 of §4.3 describe the software
> division's founding commit `720e0ec`.  By 23:30 UTC that branch (`1756529`) had a molecular
> layer: structure input, a rotamer rule and energy tables exist.  **The determination of §1
> is unchanged**, for the reason the software division itself gives (STRUCTBIO-MSG-0002 §3):
> its software needs a backbone as input; before a reference is public there is no backbone
> to give it, and after it is public nothing is blind.  The science division concurs
> (SCI-MSG-0035 §3).  What the new layer changes is §6: opportunity R-2 is no longer gated on
> a missing layer but on a method freeze and a run (protocol FB-P-02; sealed held-out list
> FRONTIER-FRZ-0002).  The original text below is kept as written.

**MetricChain is not, and has never been, a participant of CASP17.  Nothing in this file is an
official result, an official ranking, or a submission, and none may be presented as one.**

## 1. Determination

**No MetricChain implementation is mature enough for any CASP17 evaluation that could be
frozen before the official results are released on 2026-11-29.  No MetricChain prediction has
been or will be produced for that date.**  The reasons are in §4.  What a proportionate,
defensible use of the window looks like is in §5; the retrospective opportunities that open
after the release, with their prerequisites, are in §6.

## 2. Facts from the official source

| item | what the site says | where |
|---|---|---|
| categories of CASP17 | immune complexes (antibody–antigen, nanobody–antigen, T-cell receptor complexes); organic ligand–protein complexes; nucleic acids and complexes; conformational ensembles (discrete alternative conformations, **and** targets assessed by agreement with low-resolution data: cryo-tomography, SAXS, NMR RDC and chemical shifts, FRET, cross-linking); difficult protein structures and complexes (membrane proteins, weak evolutionary information, more than 1,000 residues); accuracy estimation | index page, "Modeling categories" |
| target release | first week 27 April – 1 May 2026; last date 31 July | index page, "Timetable" |
| end of the modelling season | 31 August 2026 | same |
| submission rule | "All predictions must be received and accepted before 9am PDT on the corresponding expiration date"; submissions only through the web form or the server API | Q&A page; index page |
| results | "Results will be posted on Sunday, November 29" (message of 2026-11-25); "The results of numerical evaluations will be posted two days ahead of the conference" (2026-11-18) | message board |
| results page today | "No results available yet or you don't have permissions to retrieve them." | `results.cgi`, 23:02 UTC |
| conference | Rome, 1–5 December 2026 | index page |
| assessors | immune complexes D. Zyla; difficult monomers and complexes R. Keegan; ligands J. Durairaj; RNA M. Szachniuk, M. Antczak, E. Westhof; ensembles a team led by G. Montelione | index page |
| terms of use of the data | Creative Commons Attribution 4.0 | footer link |

The founding directive's statements — season ended 31 August; announcement on 25 November
that results appear on 29 November — are confirmed by the site.

## 3. What is public, target by target

From the target list (CSV export, copied into FRZ-0001) joined with the RCSB PDB entry records
(`targets_classified.csv` in the freeze):

| | count |
|---|---|
| target-list entries | 239 (T 62, H 92, R 52, M 14, E 14, W 2, L 2, A 1) |
| cancelled | 9 |
| name a PDB code whose entry RCSB reports as **released** | **19** (release dates 2026-05-27 to 2026-10-07) |
| name no PDB code | 211 |

* **The reference structures are not all confidential.**  Nineteen are in the PDB now —
  among them three 1.1–1.3 Å crystal structures of one 472-residue enzyme with different
  ligands (T2409, T2410, T2411; released 2026-09-16), eight antibody or T-cell-receptor
  complexes, four designed RNAs and a 1,142-residue ligand complex.
* **"No PDB code on the list" is not evidence of confidentiality.**  An entry may have been
  released without the list being updated; coordinates or figures may be public through a
  preprint (one target was cancelled for exactly that reason: "Canceled - preprint").  For
  those 211 targets the status is **unknown until checked individually**, not "blind".
* **All submitted predictions are public** — the download area holds the models of every
  group for the regular, multimer, ensemble, RNA, hybrid, ligand and accuracy-estimation
  targets (directory listings with sizes and dates are in the freeze).  The official
  reference files (`targets/`) and numerical results (`results/`) directories are empty.
* The ensemble targets (14 "E", one "A") are described on the list as: four variants of one
  1,269-residue trimer, two HIV-1 envelope complexes, five "NMR hidden states" proteins of
  92–139 residues, one "SAXS/DEER target", one "FRET hidden states", one "FRET/SAXS
  domain-linker-domain target", one "RNA ensemble".

## 4. Why no MetricChain evaluation is possible before the release

### 4.1 The classes of assessment, applied to today

| class (definitions: `docs/collaboration/README.md`, addendum) | available to MetricChain for CASP17? |
|---|---|
| **A-OPB** official prospective blind | **No, and never.**  The season closed on 31 August; MetricChain did not register or submit; late submissions are not accepted and none will be attempted. |
| **A-PRR** documented pre-reference-release | Only in principle, only for targets whose reference is shown — target by target — not to be public, and only with a caveat that cannot be removed: the predictions of roughly a hundred groups have been public since late August, so anything computed now can have been informed by them.  A method would have to take the sequence alone and be shown not to have read the archive. |
| **A-PLB** pre-leaderboard | Possible for the 19 targets with public references: numbers computed before the official tables exist.  This protects against tuning to the official ranking and against nothing else. |
| **A-RET** retrospective | Everything computed after 29 November. |

### 4.2 Maturity of what exists, category by category

Read at the pinned commits of `docs/collaboration/FRONTIER_UPSTREAM_SYNC.md`.

| CASP17 category | what MetricChain has | verdict |
|---|---|---|
| structure of proteins and complexes; immune complexes | no structure-prediction method of any kind.  The software of the structural-biology division (one commit, `720e0ec`, 2026-11-26 22:30 UTC) is a certified minimum-energy solver for **abstract pairwise tables**: it has no reader for sequences or coordinates, no rotamer library, no energy function; its instances are random integer tables | not applicable |
| ligand complexes; nucleic acids | nothing | not applicable |
| accuracy estimation | nothing.  A certificate of a model-relative bound is not an estimate of a model's accuracy against experiment | not applicable |
| conformational ensembles | mathematics, not a method: the ensemble division's exact linear programmes decide identifiability *relative to a stated finite candidate pool* and for data *linear in the ensemble*; the geometry division's demixing results use exact averaged squared distances with no noise guarantee.  There is no forward model for NMR, SAXS, FRET or DEER data on any branch, and no software that reads such data | no prediction possible; a retrospective analysis is conceivable (§6) |
| (not a CASP category) side-chain placement on given backbones | the certified solver above would need a molecular layer — coordinates, rotamers, an energy function, and the unproved step from real-valued energies to the integer tables it certifies | not built; see §4.3 |

### 4.3 Why nothing was rushed

The one route by which existing software could have touched CASP17 coordinates in three days
is repacking the side chains of public server models with the certified solver.  It was not
attempted, for three reasons that are independent of the deadline:

1. **The layer that would make it a statement about a protein does not exist** (rotamers,
   energies, structure input and output), and the science division has measured, for a
   comparable model, that the certified quantity is four to five orders of magnitude more
   precise than the energy model is accurate (its Lys₁₂ budget; `RESEARCH_INTAKE.md` §3).
2. **The independent literature predicts no gain**: a 2025 third-party assessment of packing
   methods found that repacking AlphaFold-generated backbones gives no significant
   improvement over the side chains those models already carry, and an older exact-optimum
   study found that the exact minimum of a standard energy function improved side-chain
   accuracy by less than 0.1 % over a heuristic one (`STATE_OF_THE_ART.md` §C; read levels
   given there).  A rushed implementation would most likely have produced an uninformative
   number that looked like a CASP result.
3. **Every model in the public archive is someone's prediction**; a repacked copy would be a
   derivative of a participant's work evaluated on that participant's backbone — neither a
   MetricChain prediction nor a fair comparison with anything.

The directive's instruction for this case is explicit: "record the limitation rather than
manufacturing predictions or rushing scientifically unjustified implementations."

## 5. What the window was used for

| action | status | class | what it is for |
|---|---|---|---|
| time-stamped snapshot of the public state of CASP17 (FRZ-0001) | **done**, 2026-11-26 23:03 UTC | n/a (no prediction) | so that later statements about what was public when rest on a record, not on memory |
| blind test of *our own scoring infrastructure*: scores computed by this division's tools for public CASP17 models against references already in the PDB, frozen before 29 November, compared afterwards with the official numbers | in preparation; registered in `PREDICTION_FREEZE_REGISTER.md` when frozen | **A-PLB**, evidence stage *development*; the object under test is the scoring code, **not** a MetricChain method | an evaluation division must know its instruments reproduce the community's before it scores anything with them; this is the only question about CASP17 that can be answered blind by 29 November |
| review of the official assessment when published | scheduled for after 2026-11-29 | — | `STATE_OF_THE_ART.md`; no CASP17 ranking is stated anywhere in this division's files until an official page states it |

## 6. Retrospective opportunities after the release, and what each needs first

None of these is started; each is gated on prerequisites owned by another division.  All
would be class **A-RET** at best.

| opportunity | scientific question | prerequisites (owner) | why it is worth the wait |
|---|---|---|---|
| **R-1  What could the ensemble data decide?**  For the CASP17 ensemble targets assessed against low-resolution data (NMR hidden states, SAXS/DEER, FRET) | Given the released data and their stated errors, which features of the submitted ensembles are *identified*, and is the official ranking of groups stable across the set of ensembles that fit the data equally well? | a forward model with a stated error for each data type; an identifiability statement for that forward model on a stated candidate pool; software that takes submitted ensembles as the pool (ensemble, geometry, structural biology); the experimental data, if and when CASP releases them | it is the one place where MetricChain's mathematics (partial identification, demixing limits) addresses a question the community is asking this year, and where a *negative* answer ("the data cannot rank these groups") would be a result |
| **R-2  Does a certified optimum change side-chain accuracy?**  On the high-resolution CASP17 references (for example the three 1.1–1.3 Å amidase structures) | For a fixed backbone and a stated energy model, how do the side chains of the certified minimum compare with experiment and with established packers, on native and on predicted backbones? | the molecular layer and the real-to-rational rounding bound (structural biology, science); protocol FB-P-02 with its pre-declared null expectation | a pre-registered test whose most likely outcome is "no accuracy gain; the gain is auditability" — worth stating with evidence rather than by citation |
| **R-3  Reading the official assessment** | Which methods does independent evidence place first in each category, and do the assessors report anything that bears on certificates, identifiability or calibration? | none | keeps the state-of-the-art register honest |

## 7. Coordination

Sent in FRONTIER-MSG-0001 (to all; flagged for structural biology, engineering and science):
the determination of §1 with its reasons, the invitation to contradict the maturity table of
§4.2 with evidence before 29 November, and the availability of the freeze tooling to every
division.  No division has been asked to produce anything for CASP17.
