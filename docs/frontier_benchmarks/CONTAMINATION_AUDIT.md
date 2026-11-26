# Contamination audit

*Frontier Benchmarking division.  Version 1, 2026-11-26.  "Contamination" here means any path
by which the answer, or information correlated with it, can reach a method or its evaluator
before the comparison.  The audit never concludes that leakage "has been eliminated"; it
concludes, per path, **controlled**, **not controlled**, or **unknown**, and says on what
evidence.*

## 1. The paths

| # | path | typical carrier | how it is controlled here |
|---|---|---|---|
| L1 | the reference is in a learned method's **training data** | structures or measurements released before the training cut-off | targets must post-date every compared model's declared cut-off; the cut-off and its source are recorded per model (§2) |
| L2 | data **similar** to the reference are in the training data | homologues, same pocket, same ligand class | similarity filtering against the training set, at the level of the whole complex; a min-chain identity filter is known to leak |
| L3 | the reference shaped a method's **parameters or defaults** without any training | rotamer libraries and statistical potentials built from the PDB; force-field refits; regularisation defaults tuned on standard systems | recorded per baseline; a rotamer library built from a later PDB snapshot than the test structures is flagged |
| L4 | the **developer** has seen the test cases | benchmark built by the method's authors; instances chosen after results | development and held-out sets separated; held-out lists prospective or committed (`ASSESSMENT_PROTOCOLS.md` §3); selection rules fixed before results |
| L5 | **other parties' predictions** of the same targets are public | the CASP prediction archive | a method evaluated on such targets must not read the archive, and this can be asserted but rarely proved; the class is capped accordingly |
| L6 | the **evaluator** saw the reference before fixing the protocol | choosing metrics, thresholds or exclusions that favour an outcome | protocol frozen (hash, time-stamp) before execution; our own exposure logged in §4 |
| L7 | the **developing agent's own knowledge** | an AI system writing or tuning software knows public structures and results up to its knowledge cut-off | the model and its cut-off are recorded in every freeze manifest of agent-built software; see §3 |
| L8 | **wrong metadata** | release dates wrong in a curated dataset | dates are taken from the primary archive, not from a derived dataset |
| L9 | **metric leakage** | a method receives ground-truth geometry as input (reported for one side-chain packer) | inputs are regenerated from sequence and backbone only; idealised bond geometry |

## 2. Training cut-offs against benchmark dates

Declared cut-offs as collected by the literature assessments (read level in brackets; "not
verified" means exactly that).

| model family | declared cut-off | source level |
|---|---|---|
| AlphaFold 3; Protenix v0.5 / v1-default / v2; a 2026 language-model co-folding release | 2021-09-30 (September 2021) | FT / OP |
| Chai-1 | 2021-09-30 | MEM — not verified |
| Boltz-2; RoseTTAFold 3 | after 2023-01-13 (exact dates not verified) | OP (a benchmark's flag) |
| one Protenix v1 variant | 2025-06-30 | OP |
| OpenFold3 shipped weights | June 2025 | SN — not verified |
| learned side-chain packers (FlowPacker; PIPPack; others) | 2023-07-28; August 2020; "BC40" for others | FT, SELF; others not verified at source |

| benchmark | reference dates | clean for cut-offs up to | not clean for |
|---|---|---|---|
| static post-2021 sets | after 2021-09-30 | 2021-09-30 | anything trained later |
| a low-homology all-atom set | filtered against PDB before 2023-01-13 | early 2023 | models with later cut-offs (flagged by the benchmark itself) |
| CASP16 targets (2024) | mid-2024 | mid-2024 | June-2025 models |
| **CASP17 targets (2026)** | released to predictors April–July 2026; references mostly unreleased on 2026-11-26 | every cut-off in the table (L1) | — but see L5 and L7 |
| PDB entries released after a method's freeze | by construction | everything | — |

Consequence: for learned baselines with 2025 cut-offs, the only clean public structural
references are CASP17-era or later.  For non-learned baselines L1 does not apply; L3 does.

## 3. MetricChain's own exposure

* **No learned component exists** on any branch read; L1 and L2 do not apply to MetricChain's
  methods as they stand.  If a learned potential or a fitted rotamer library enters the
  software, its data snapshot becomes a cut-off and is recorded.
* **L3 applies to anything molecular.**  The force fields used by the science division were
  parameterised on data that include the kinds of systems any test would use; a rotamer
  library is a summary of the PDB.  These are properties of the model class, stated in every
  protocol's field 16.
* **L7 is real and cannot be audited from outside.**  The software and the protocols are
  written by AI sessions; the model of the session that founded this division declares a
  knowledge cut-off of **June 2026**.  CASP17 sequences were published from 27 April 2026 and
  four reference entries (designed RNAs) were released on 2026-05-27, so some CASP17 material
  lies inside that cut-off; most reference structures were released later (2026-06-17 to
  2026-10-07) or not yet.  We do not claim that an agent-built method evaluated on CASP17
  targets is uncontaminated by this path; for targets released before the developing model's
  cut-off the status is **unknown**, after it **controlled** with respect to L7 only.
* **L4 has already occurred once, deliberately.**  The ten public side-chain instances of
  FB-P-01 were run by us in a pilot and will be reported to the software division: they are
  development instances from now on and can never serve as held-out evidence.

## 4. Audit of our own freezes and runs

| item | what we had seen when it was fixed | paths | verdict |
|---|---|---|---|
| FRONTIER-FRZ-0001 (public state of CASP17) | contains no prediction | — | not applicable |
| CASP17 determination (`CASP17_ASSESSMENT.md`) | official pages; no result existed | L6: none possible | controlled |
| FB-P-01 pilot (`RESULTS.md` §1) | protocol written **after** the first instance was run (the pilot informed it) | L6 **not controlled** — which is why the pilot is class A-EXP and its numbers are never reported as validation | exploratory only |
| FB-P-02 expectations E1–E3 | fixed before any software exists; informed by published results on *other* data | L6 controlled for our side | — |
| blind test of our scoring tools (FB-P-10), when frozen | references public (PDB); official per-model scores not public | L6 controlled for the official numbers only: class A-PLB | recorded at freeze time |

## 5. Rules of wording

* "No evidence of leakage was found by the following checks: …" is allowed.  "Leakage was
  eliminated" is not, unless the reference demonstrably did not exist when the prediction was
  frozen.
* The time of prediction and the time at which reference information became available are
  two facts with two pieces of evidence: a time-stamp token for the first; an archive's
  release record (or its absence, with the caveat of `CASP17_ASSESSMENT.md` §3) for the
  second.
* A class is never upgraded after the fact, and an evaluation whose separation cannot be
  established is class A-UNK, reported as such.
