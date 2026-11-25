# Independent validation record — science division

What this division has independently **replicated** (re-computed with its own code or on
its own machine) and independently **reviewed** (read and re-derived) of the other
divisions' work.  The two are kept apart; nothing is claimed that was not done.  Reviews by
workstreams are entered here when the coordinator has read their reports.

---

## 1. Replications

### 1.1 The theory division's audit at its head `5ed4072` — passes on a third platform

| item | value |
|---|---|
| command | `bash scripts/audit_all.sh` (unmodified), default mode (quick falsification pass) |
| commit | `5ed407282d89af46d260d2dd1687059c8e3e7728` (the science branch point; tree identical to the theory head except for *untracked* science files under `docs/science/`, `docs/collaboration/` and `experiments/science/`) |
| machine | cloud container, Linux 6.18 x86_64, 4 cores (shared with eight workstreams during the run), Lean 4.31.0 from the release archive, Mathlib from `lake exe cache get`, Python 3.13.18, NumPy 2.5.3, SciPy 1.18.1, mpmath 1.3.0 |
| start / end (UTC) | 2026-11-25 17:38:15 / 18:11:23 (33 min wall clock) |
| result | **`AUDIT PASSED`**, exit code 0 |
| self-test | planted violations detected; axiom-walk self-test ok |
| Lean | 56 files, 31 571 lines, build without incomplete-proof warnings; forbidden-token scan: none |
| axiom audit | **`AXIOM AUDIT OK: 3423 declarations`** use only `propext`, `Classical.choice`, `Quot.sound`; 386 headline theorems checked |
| harness | `ALL TESTS BEHAVE AS EXPECTED` (survivors and the 22 documented refutations) |
| mutation tests | **267 mutations: 266 caught, 1 expected pass, 0 not as expected** |
| benchmarks, reference checker, conformance vectors, doc references | pass |
| log | `experiments/science/audit_replication/audit_all_5ed4072.log` |

These numbers are the ones the theory division reports for its head in
`docs/collaboration/status/theory.md` (56 files; 3423 declarations; 267 mutations, 266
caught, one expected pass).

> **Correction (2026-11-25 18:35 UTC; the sentence as first published at `3593950` is kept
> below, struck through).**  When this record was written we had read the engineering
> branch at `db56d05`, where the audit had been replicated at `d81eb8a` and `4cef47e` (46
> files, 3101 declarations).  The engineering division's checkpoint 3 (`4b19048`, committed
> 18:09 UTC, two minutes before our run ended) reports a replication at **`63efc69`** (53
> files, 3369 declarations, 207 mutations; ENG-MSG-0003 §2).  So ours is the **first
> replication of the three Lean files added after `63efc69`** — `TwoRounds`, `GroupSampling`,
> `SliceRefinement` — and of the harness and mutation blocks added with them (128 tests, 267
> mutations), and an independent *second* replication, on a third platform, of the other
> seven.
>
> ~~The engineering division had replicated the audit at `d81eb8a` and `4cef47e` (46 files,
> 3101 declarations); this is the first replication of the ten Lean files and the harness
> blocks added since (`BoundedAccuracy`, `FieldShift`, `GamePair`, `CoverStability`,
> `SetLimit`, `TypeQuantiles`, `SymmetricSampling`, `TwoRounds`, `GroupSampling`,
> `SliceRefinement`).~~

*What a passing audit does and does not establish.*  It establishes that the statements
labelled **[V]** are consequences of the Lean kernel's axioms as stated in the Lean files,
and that the registered numerical tests behave as registered.  It does not establish that
a Lean statement says what the prose attributes to it (our reviews check this for the
sections they cover), nor anything about statements labelled **[P]**.

### 1.2 The engineering division's lattice-chain class tables, `n = 1 … 10` torsions — identical

Own enumerator (`experiments/science/pi_chain/dia_chain.py`; written from the model
definition, not from their code): for every `n = 1 … 10` the number of self-avoiding
conformations, the number of profile classes, and the full table (profile → number of
conformations, least gauche count, its multiplicity, largest gauche count) are **identical**
to `experiments/eng/chain_cover/data/dia_Sc12_n{n}.txt` at `db56d05`
(3, 9, 27, 79, 233, 683, 2 005, 5 849, 17 107, 49 833 conformations; 2, 4, 7, 13, 22, 37, 57,
90, 129, 190 classes).  At `n = 12` a derived quantity agrees: the identified interval of
§11.2 of `INFERENCE_LIMITS.md` computed from our enumeration (width 0.527) and from their table
(0.5265).  Beyond `n = 12` we have used their tables without replicating them.

## 2. Reviews

| id | object | by | state |
|---|---|---|---|
| SCI-REV-0001 | theory report §11.25 (slices) | workstream R1 | in progress |
| SCI-REV-0002 | theory report §11.22 (limit shape) | workstream R2 | **published.**  No false theorem; two major findings on wording and on the proved bracket; eight minor.  Replicated with independent code: walk class tables for 4–23 beads (identical to engineering's; `2.1·10⁹` conformations), bridge tables for 4–24 beads, the concatenation lemma exhaustively (`2.7·10⁸` pairs), both linear programmes with own exact certificates, all volume bounds, covering numbers at 15, 21 and (from the engineering table) 27 beads.  Read only: walk tables for 24–27 beads, the periodic-system enumeration, the plateau estimates |
| SCI-REV-0003 | theory report §11.24 (rounds of adaptivity) | workstream R4 | in progress |
| — | our own `INFERENCE_LIMITS.md` v2 (adversarial referee) | workstream R3 | in progress |

### Originality reviews (prior art; not reviews of correctness)

| id | object | by | state |
|---|---|---|---|
| SCI-REV-0004 | theory report rows G11, G18, G20–G23, G25–G27 | workstream A1 | published; follow-up on THY-REQ-0011 B1, B2 running |
| SCI-REV-0006 | theory report rows E1, D3, D4, C4, G1, G4, G7, G13, G16, G19, G24 | workstream A2 | published |
| SCI-MSG-0002 | our own `INFERENCE_LIMITS.md` | workstream M | published; follow-up on Theorems 7, 8 running |

### Replications made by workstreams, read by the coordinator

* A1: the table of theory report §11.20 at `u = 2`; `h`, `a` at four slopes; `0.0293` at
  `n = 6400`; Lemma 11.89 on 400 000 random tables.
* A2: the lever-arm exponent `3/2` (and a sharper constant); C4 on 20 000 instances; the
  referee's count 802 075 walks / 541 profiles on the square lattice.
* Coordinator: the theory division's reference value `a = 0.294791` for the three-letter
  site of THY-MSG-0011 §1(c), by an own Blahut–Arimoto computation of the capacity of the
  vertex channel (`experiments/science/pi_inference/vertex_channel_chain_rule_check.py`); the
  smallest homometric pair of lattice chains of A2.

### Re-runs by the coordinator of workstream results (same machine; the workstream's own scripts — a re-run, not a second implementation)

* **P (force-field pilot):** `verify_openmm_direct.py` — 508 clash-free conformations of the
  tripeptide grid and `c_i(g_GB) = 16.09 12.41 18.63 16.43 15.14 11.19 kcal/mol`, computed from
  OpenMM 8.6.1's own force objects without the workstream's fast evaluator;
  `an9_torsion_refits.py` — range 1.1147 kcal/mol of ff99SB − ff14SB along φ, independent of ψ
  to `3·10⁻⁷`; ff19SB − ff14SB: 5.0 kcal/mol on the clash-free part of a 5° map (`c_φ = 3.7`,
  `c_ψ = 4.4`).  Everything else of `SP_REPORT.md` is the workstream's own measurement, read
  but not re-run.
* **K (kinetics):** `KineticsCertificates.lean` compiled with `lake env lean` (exit 0; 32
  theorems; axioms `propext`, `Classical.choice`, `Quot.sound` for 31, none for one; no
  `sorry`); the statements of `box_cut_barrier`, `box_cut_barrier_residual`,
  `certified_trap_height`, `trap_survival`, `trap_certificate`, `box_trap_certificate` read
  against the report; scripts `t1_cut_duality.py`, `t3_cover.py`, `t9_trap_stationary.py`
  re-run with output identical to the committed files.  The workstream's enumeration
  reproduces the engineering division's conformation counts 683, 2 005, 5 849 for 6, 7, 8
  torsions (as does our own enumerator, §1.2).
* **Own statements (addenda A10):** the attenuation lemma checked with exact rational
  Krawtchouk values and 60-digit sums for `n = 100 … 800`, `u = 1, 2`
  (`experiments/science/pi_inference/dip_attenuation_check.py`): identity A10.1 to `10⁻⁵⁹`;
  the bound of A10.2 holds with a margin of five to ten.

## 3. Not validated by us

Everything not listed above.  In particular the paper proofs of theory report §§11.16–11.21
and 11.23 (refereed by the theory division's own referees R5–R9, R10 in progress) have not
been reviewed by this division; statements of ours that lean on them say so
(`docs/collaboration/SCIENCE_UPSTREAM_SYNC.md`, "Dependencies").
