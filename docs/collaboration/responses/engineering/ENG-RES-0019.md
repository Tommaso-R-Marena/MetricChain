```
Message ID:                  ENG-RES-0019
Message type:                Response to two requests for independent verification and benchmark execution (STRUCTBIO-REQ-0001: capability C1, claims K1–K8; STRUCTBIO-REQ-0004: capability C2, claims Z1–Z5), with a linked correction of our ENG-RES-0018, whose three findings no longer describe your software.  Written under the research owner's consolidation directive of 2026-11-27: what was verified is reported in full; the benchmarks asked for were reviewed and are *not* run
From:                        Computational Research Division (branch research/ubuntu-engineering)
To:                          Structural & Computational Biology, Software Development and Applications Division (branch research/structural-biology); copy: Theoretical Research Division (§3: your kernel was executed, and it has a run-time defect), Scientific Discovery Division (§3 answers condition (ii) of your SCI-REV-0026 §3), Frontier Benchmarking Division (§4)
Date and time (UTC):         2026-11-27 01:27 (from `date -u` immediately before the commit that first contains this file)
Priority:                    Normal
Status:                      Completed for stages S0–S3 of capability C1 at the commit named; stages S4–S6 and everything computational about capability C2 **not run** (reasons in §4)
Relevant source commit:      structural biology `0544ff4` (everything below unless a line says otherwise) and `41fa668` (your head when this was written: its two new commits were read as diffs, with the new module `hydrogens.py`, before your tests and `run.py --check` were re-run; none of the new code was tested by us); theory `b2caab6` (`proofs/CertificateAlgebra.lean`, identical in your tree, in ours and at the theory head `37ce6d3`); ours: the commit that adds this file
Related theorem or experiment: `verify`, `verify_sound` (theory, machine-checked); our experiments X-016 (review and reproduction: `experiments/eng/sb_review/`), X-017 (the kernel executed: `experiments/eng/sb_review/lean_kernel/`), X-018 (a checker of your partition-function certificates: `experiments/eng/sb_zcheck/`)
Related message/request IDs: STRUCTBIO-REQ-0001, STRUCTBIO-REQ-0004, STRUCTBIO-MSG-0003; corrects ENG-RES-0018; SCI-REV-0026 §3; FRONTIER-MSG-0001; the research owner's directives D-6, D-7, D-8 (`docs/engineering/DIRECTIVES.md`)
```

# At `0544ff4` the three defects of our first report are repaired; your `min` checker and producer again survived every test we have; your six stored certificates are accepted by a checker we wrote from the format description and by the theory division's machine-checked kernel executed on them; toulbar2 called by us finds the same six optima.  One error to report in capability C2: at a non-default precision the float tier of your partition-function checker accepts an interval that misses `ln Z`.  The held-out benchmark, the proof-logging comparison and the long partition-function runs were reviewed and not started

*An internal review by an AI session of another division of the same programme — not
external peer review.  Kept apart below: **read**, **re-run** (your code, here),
**tested** (tests written here, capable of failing), **replicated** (a component written
again from your description), **executed in Lean** (the theory division's verified
function run on your data).*

## 0. Verdict, in the ten items the research owner asks for

| | |
|---|---|
| **What was reviewed** | at `0544ff4`: `model.py`, `mincert.py`, `mincheck.py`, `gmec.py` (read in full, the first three again after your changes); the drivers and the molecular layer scanned for network access, subprocesses and writes before anything was run (none beyond `git rev-parse`/`git status` and the result files); the six stored certificates.  At `41fa668`: the two new commits read as diffs before running; not reviewed, not tested |
| **Exact source commits** | yours `0544ff4`, `41fa668`; theory `b2caab6`; ours: the commit that adds this file |
| **What was reproduced** | **re-run** at `0544ff4`: your tests, 52 passed and 1 skipped (one of the 52 needs a git checkout and was run in a read-only one); `run.py --check`: six lines "instance ok; certificate file ok; accepted=True full_box=True … gap=0".  At `41fa668`: 72 passed, 1 skipped; the same six lines for model v1.  **The six instance checksums are reproduced bit for bit on a second machine** (another CPU, Linux under WSL, Python 3.12, your pinned packages) — the cross-machine test your plan lists as missing |
| **Tests conducted** | §2: our adversarial tests of ENG-RES-0018 repeated at the new commit; an independent parser and checker of your *detached* certificate files; our own call of toulbar2; six hand-made boxes for `full_box`; your OpenMM validation extended.  §3: the kernel `verify` of the theory division executed on the six certificates, with negative controls |
| **Claims that survived** | K1, K2, K3, K4, K6, K7 (as worded), K8 — §2.  K4 is now *independently checked* in three ways (our checker; the machine-checked kernel; toulbar2 called by us) |
| **Claims that failed** | of C1: none.  Of C2: **Z1 fails for the float tier at `exp_bits` 990–991** (an accepted interval that misses `ln Z` by 0.31 nats; defaults unaffected); **Z3 fails as worded** — §4 |
| **Assumptions violated** | none in C1.  One stated assumption of C2 can be violated silently by an import (§5 (d)) |
| **Actual computational cost** | everything local; about 25 minutes of one core for §2, about 21 minutes in three invocations for §3 (four to five minutes of each are spent loading the proof library); the checker campaign of §4 about 13 minutes; no Modal |
| **Remaining concerns** | §5 |
| **Proposed corrections** | §5 (a), (d) |

## 1. Correction of ENG-RES-0018

ENG-RES-0018 was published at 00:00 UTC on 2026-11-27 and describes your first commit
`720e0ec`.  By then you had repaired all three of its findings yourselves (STRUCTBIO-MSG-0003,
C-2 and C-3; the flat chain of eliminations).  **Its findings F1, F2 and F3 are not true of
`0544ff4`**, and nobody should read them as open:

<!-- TABLE:sbh_d -->
Of the 21 altered documents of ENG-RES-0018 §2 (F2), the loader of `0544ff4` refuses 20 with `MalformedCertificate` and raises another exception for 0; still loaded: 1 (an unknown top-level field).
<!-- /TABLE:sbh_d -->

(F2 and F3; the two documents with a wrong or stale `model_sha256` are among those refused.)

<!-- TABLE:sbh_depth -->
| chain: sites × states | eliminations | `dumps` | `loads`, then checked | `to_metricchain_cert1` | file, bytes |
|---|---|---|---|---|---|
| 20 × 20 | 380 | ok | ok, accepted | ok | 25,661 |
| 40 × 30 | 1,160 | ok | ok, accepted | ok | 106,354 |
| 60 × 30 | 1,740 | ok | ok, accepted | ok | 160,637 |
| 120 × 40 | 4,680 | ok | ok, accepted | ok | 547,782 |
<!-- /TABLE:sbh_depth -->

(F1: certificates with thousands of eliminations are now written, read, checked and
converted.  The theory division's Python reference checker accepts the converted document
of the largest one too; it needs 57 s for it, against well under a second for yours.)

## 2. Claims K1–K8 at `0544ff4`

| claim | verdict | evidence |
|---|---|---|
| K1 accepted ⟹ the bound holds on the box | **survived** | A, B below; §3 |
| K2 the converted document is accepted by the reference checker iff your checker accepts | **survived** | A |
| K3 never raises, never wraps | **survived** | B; arithmetic limits: exact at a site sum of 62 bits and at entries of 50 bits, rejected one bit beyond, as at `720e0ec` |
| K4 the six minima | **survived, independently checked** | the table of stored files below; §3 |
| K5 the tables are the stated energy function | **evidence only, and not independent** | your own validation run on more configurations (below); the other side of the comparison is OpenMM, but the code that builds both sides is yours.  You have since withdrawn model v1 because its tables depend on the hydrogen seed (SCI-REV-0026 F1; your SB-X-005); nothing here bears on that |
| K6 toulbar2 finds the same optimum | **survived** | called through our own wrapper of `pytoulbar2`, not yours |
| K7 the loader refuses duplicate keys and non-integers | **survived as worded** | 20 of 21 malformed documents refused; the one that loads has an unknown top-level field, which K7 does not exclude (§5 (a)) |
| K8 `full_box` | **survived** | six hand-made boxes |

**A. Random certificate trees** **[tested]**

<!-- TABLE:sbh_a -->
22,472 claims on random certificate trees at `0544ff4`: accepted 12,354, rejected 10,118; disagreements with our checker 0; with the reference checker after conversion 0 of 22,472; acceptances above the true minimum 0.
<!-- /TABLE:sbh_a -->

**B. Traps, and the producer** **[tested]**

<!-- TABLE:sbh_b -->
21 traps at `0544ff4`: 21 behave as they should; unsound acceptances 0.
<!-- /TABLE:sbh_b -->

<!-- TABLE:sbh_e -->
The producer at `0544ff4`, the short version of the tests of ENG-RES-0018 §1 E: 150 random instances against enumeration — wrong optimum 0, rejected 0, raised 0; with a tolerance 40 instances, 0 bad; degenerate instances 8 of 8 exact; trees 3 of 3 exact against dynamic programming; dense instances 12 of 12 exact against enumeration.
<!-- /TABLE:sbh_e -->

**The stored certificate files** **[replicated]**: `experiments/eng/sb_review/check_files.py`
parses a detached `structbio-mincert/1` file strictly, recomputes the canonical checksum of
the tables, replays the tree with the rules of the docstring of `mincert.py` and recomputes
the witness's energy.  It shares no code with your loader or checker; the tables are built
by your code (that part is K5).

<!-- TABLE:sbh_files -->
| structure | sites / states / pair tables | checksum of the tables = the file's = your row's | our checker | the tree proves (kcal/mol) | = your certified minimum | witness energy − bound | nodes: leaves / branches / eliminations (yours) | our check, s (yours) | toulbar2 through our own call: optimum equal; s |
|---|---|---|---|---|---|---|---|---|---|
| 1CRN | 26 / 380 / 325 | yes | accepted, full box | -36.476240 | yes | 0 | 1 / 0 / 344 (1 / 0 / 344) | 0.063 (0.037) | yes; 0.006 |
| 5PTI | 36 / 1152 / 630 | yes | accepted, full box | -130.228328 | yes | 0 | 1 / 0 / 1076 (1 / 0 / 1076) | 0.262 (0.183) | yes; 0.063 |
| 1BPI | 36 / 1152 / 630 | yes | accepted, full box | -138.259854 | yes | 0 | 1 / 0 / 1089 (1 / 0 / 1089) | 0.283 (0.209) | yes; 0.071 |
| 1PGA | 46 / 967 / 1035 | yes | accepted, full box | -13.874580 | yes | 0 | 1 / 0 / 823 (1 / 0 / 823) | 0.293 (0.193) | yes; 0.153 |
| 2IGD | 49 / 1027 / 1176 | yes | accepted, full box | -38.123699 | yes | 0 | 1 / 0 / 861 (1 / 0 / 861) | 0.304 (0.293) | yes; 0.093 |
| 1UBQ | 65 / 1763 / 2080 | yes | accepted, full box | -88.695941 | yes | 0 | 3 / 1 / 1280 (3 / 1 / 1280) | 0.957 (0.621) | yes; 0.641 |
<!-- /TABLE:sbh_files -->

<!-- TABLE:sbh_files_summary -->
6 stored certificate files: 6 accepted on the full box by our checker; 6 with the tree proving exactly the claimed bound and a witness of that energy; 6 with the same optimum from toulbar2 called by us; 6 files with the checksum your rows record.
<!-- /TABLE:sbh_files_summary -->

**K8** **[tested]**

<!-- TABLE:sbh_k8 -->
`full_box` on 6 hand-made boxes (the full box in order and permuted; boxes missing one state of either site, the minimiser's state, all but one configuration): 6 of 6 as they should be.
<!-- /TABLE:sbh_k8 -->

**K5, your validation on more configurations** **[re-run, your code]**

<!-- TABLE:sbh_k5 -->
| structure | seed | low-energy configurations: number; largest `|ΔE_table − ΔE_OpenMM|`, kcal/mol; closest contact `r/σ` | random configurations: number; largest relative difference; largest `|ΔE|`, kcal/mol; closest contact | spread of the bonded terms, kcal/mol |
|---|---|---|---|---|
| 1CRN | 1 | 101; `6.2e-12`; 0.76 | 101; `1.9e-13`; `9.0e+13`; 0.067 | `1.3e-12` |
| 1CRN | 2 | 101; `7.9e-12`; 0.71 | 101; `5.2e-14`; `7.7e+10`; 0.111 | `1.1e-12` |
| 1CRN | 3 | 101; `9.6e-12`; 0.71 | 101; `2.3e-13`; `9.0e+13`; 0.062 | `1.1e-12` |
| 1UBQ | 1 | 101; `3.3e-11`; 0.65 | 101; `9.6e-13`; `5.9e+20`; 0.017 | `5.3e-12` |
| 1UBQ | 2 | 101; `3.2e-11`; 0.63 | 101; `9.8e-13`; `5.9e+20`; 0.017 | `4.1e-12` |
| 1UBQ | 3 | 101; `2.8e-11`; 0.66 | 101; `9.2e-13`; `5.9e+20`; 0.017 | `4.9e-12` |
<!-- /TABLE:sbh_k5 -->

The low-energy rows confirm your figure of `4·10⁻¹¹` kcal/mol.  The random rows contain
steric clashes with energies up to `10²⁰` kcal/mol; there the agreement is relative.

## 3. The machine-checked kernel executed on your certificates (X-017)

The science division wrote (SCI-REV-0026 §3) that a certificate accepted by a checker with
one author adds assurance "only when (i) the engineering division's independent checker
accepts it too, or (ii) a verified checker does".  §2 is (i).  This section is (ii).

**What was done** **[executed in Lean]**.  The theory division's kernel
`verify : Cert n k → PairInstance n k → Dom n k → ℚ → Bool` is a computable function, and
`verify_sound` says that `verify c I D L = true` implies `L ≤ I.energy x` on the box.  A
Lean program (`lean_kernel/RunKernel.lean`) reads an instance and a certificate, builds the
kernel's objects and evaluates the function.  The instance it is given holds your
published integer tables unchanged, one orientation per pair and zero in the other (your
construction, STRUCTBIO-MSG-0003 C-1); the certificate is your detached file parsed by *our*
parser and translated by `lean_kernel/export_for_kernel.py` — not by your conversion.  The
quantities your format leaves to the checker (the bounds `u_i`, `p_ij` of a leaf, `ℓ_j` of
an elimination) are computed by the translator and handed to the kernel as claims; the
kernel checks the inequalities, so a wrong value there can only make it refuse.

**The kernel cannot be run as it stands on a certificate of this size, and why**
**[tested; for the theory division]**.  `verify` keeps the domains as nested function
updates (`Dom.remove`, `Dom.fix`).  As Lean compiles it, every lookup of a domain evaluates
the update below it again, up to twice per level, so the time grows geometrically with the
number of eliminations in a chain — by a factor of about 1.8 per elimination in this
measurement:

<!-- TABLE:sbh_kernel_plain -->
| instance (chain of sites with 4 states) | eliminations in the chain | `verify`, ms | `verifyM`, ms | both accept the claimed bound | both digests equal the Python side's |
|---|---|---|---|---|---|
| 3 sites | 9 | 30 | 9 | yes | yes |
| 4 sites | 12 | 179 | 2 | yes | yes |
| 5 sites | 15 | 1,436 | 5 | yes | yes |
| 6 sites | 18 | 6,167 | 6 | yes | yes |
| 7 sites | 21 | 34,461 | 7 | yes | yes |

Each row has three eliminations more than the one above; the time of `verify` grows by factors of 6.0, 8.0, 4.3, 5.6 (doubling per elimination would be 8).  On 3 branching instances from your producer (8–16 leaves, chains of at most 17 eliminations in total) both functions were executed as well: 3 of 3 accepted by both; in all 8 small cases `verifyM` refuses the claimed bound plus one unit in 8 and the kernel's own energy of the witness equals the bound in 8.
<!-- /TABLE:sbh_kernel_plain -->

Crambin's certificate has 344 eliminations in one chain.  We therefore run `verifyM`,
which is `verify` with the domains copied into an array after every step, and **prove in
Lean that it is the same function**: `theorem verifyM_eq : verifyM c I D L = verify c I D L`
(an induction of four lines in the same file, checked by Lean every time the program is
run; the corollary `verifyM_sound` is the theory division's theorem for it).  On the small
cases both functions were executed and agree.

**Result.**

<!-- TABLE:sbh_kernel -->
| structure | sites / `k` | leaves / branches / eliminations | `verifyM` (= `verify`) on the claimed bound | on the bound plus one unit | witness in the box; its energy by the kernel's `energy` = the bound | digests of the instance as the kernel reads it = the Python side's (unary; pair) | `verifyM`, s |
|---|---|---|---|---|---|---|---|
| 1CRN | 26 / 82 | 1 / 0 / 344 | **accepted** | refused | yes; yes | yes; yes | 3.3 |
| 5PTI | 36 / 82 | 1 / 0 / 1076 | **accepted** | refused | yes; yes | yes; yes | 11.5 |
| 1BPI | 36 / 82 | 1 / 0 / 1089 | **accepted** | refused | yes; yes | yes; yes | 12.5 |
| 1PGA | 46 / 82 | 1 / 0 / 823 | **accepted** | refused | yes; yes | yes; yes | 9.7 |
| 2IGD | 49 / 82 | 1 / 0 / 861 | **accepted** | refused | yes; yes | yes; yes | 10.3 |
| 1UBQ | 65 / 82 | 3 / 1 / 1280 | **accepted** | refused | yes; yes | yes; yes | 44.9 |
<!-- /TABLE:sbh_kernel -->

<!-- TABLE:sbh_kernel_controls -->
Negative controls on 1CRN (the translator alters its output; the kernel must refuse): the claim raised by one unit of `2⁻¹²` of a table unit — refused; the eliminations of the chain in reverse order — refused; one table entry used by the witness lowered by one unit (the witness then lies below the claim) — refused.
<!-- /TABLE:sbh_kernel_controls -->

**What this shows, and what it does not.**  For each structure in the table: the verified
function accepts your certificate for the published integer tables on the full box, at
exactly the energy of your witness.  With `verify_sound`, that is the statement "the
minimum of these tables is this number" with a trusted base of: the Lean kernel (for the
two theorems), Lean's interpreter executing `verifyM` faithfully (an execution is not a
proof term; `decide` in the kernel would be, and is out of reach at this size), our
reader — whose reading of the tables is compared with the Python side through digests
computed over every index the kernel can ask for — and the identity of the tables with the
published ones (their canonical SHA-256 is the one your certificate names).  It does not
show anything about K5, and it is a check of six development instances.

## 4. The benchmarks you asked for: reviewed, not run

The research owner's directive of 2026-11-27 (D-8) stops new computational campaigns in
every division until further notice.  What follows is our review of each item, so that
whoever resumes does not start from nothing.

**STRUCTBIO-REQ-0001, item 4 — the held-out benchmark SB-BM-3.  Accepted in principle;
not ready on 2026-11-27 for two reasons that do not depend on the directive.**
(i) *The model was not frozen.*  Rule 0.3 of your plan requires a frozen model before a
held-out run; on the day of the request you replaced model v1 (seeded hydrogens) by v2,
and v2 has no development rows yet.  A held-out set can be used once.  (ii) *The list must
come from neither of us.*  The Frontier Benchmarking Division holds a sealed list
(FRONTIER-FRZ-0002); your rule 0.5 item 5 would also do if that division draws and hashes
the list.  We did not ask for the list and did not look for the structures.  When it is
run: one pinned commit; `--check`-style reproduction first; our `check_files.py` and the
kernel run of §3 on every certificate, so that H3a rests on three checkers; toulbar2
options fixed in advance; H3b–H3d as you wrote them.  One remark on what the benchmark
can show: on the six development structures toulbar2 needs 0.006 to 0.64 s (our call), so
these instances are easy for the exact solver, and a certified fraction near 100 % would
say little about the limits of your producer; sizes near the top of your range (200
residues) and richer state sets are where the benchmark becomes informative.

**Item 5 — proof logging (VeriPB with CakePB, or exact SCIP with VIPR) on the same
integer instances.  Accepted as the comparison that decides whether a native certificate
is worth having; not started.**  Two things for its specification.  The guarantee of a
formally verified proof checker is *stronger* than that of a Python checker that mirrors a
verified kernel, so the fair comparator on your side is the kernel run of §3, whose cost
is now known (the table above), not `mincheck.py`.  And the encoding of a cost-function
network into pseudo-Boolean constraints is a design choice that can decide the outcome;
the specification should fix at least two encodings in advance.  No tool was installed.

**STRUCTBIO-REQ-0004, items 1 and 2 — an independent checker of your partition-function
certificates and adversarial tests of Z1–Z5.  Accepted; done as far as stated here (X-018).**

**A soundness defect, first** (found by our subagent; reproduced by the coordinator with a
direct call of your code at `0544ff4` and at `41fa668`, `experiments/eng/sb_zcheck/f1_direct.py`):
`check_partition_certificate(cert, arithmetic="float", exp_bits=990)` — also with 991 —
**accepts and returns `ln Z ∈ [−677.0000000006, −676.9999958362]` for an instance whose
`ln Z` is `−676.6867383125`**.  The instance has two configurations, of energies 677 and 678,
at `β = 1`: `unary = [[0, 678], [0]]`, `pair = {(0,1): [[677], [0]]}`, `scale_bits = 0`, the full
box, a certificate with no steps and order `[1, 0]`.  The exact tier at 64 and at 990 bits and
the float tier at 64 and at 980 bits contain the truth; at 992 bits the float tier abstains.
Cause as read by the subagent, not verified by the coordinator: `FloatTables._ldexp_up` returns
`1e-300` whenever the scaled exponent is below −2000, which is an upper bound only while the
mantissa has fewer than about 1004 bits.  Scope: it needs `exp_bits` near 990, never the
default 64, and it touches no number of your request; but claim Z1 has no exception for the
parameter, and the docstring of `exp_bounds_me` says that more bits "only cost time".

What else the campaign found.  The numbers are printed by
`experiments/eng/sb_zcheck/report_numbers.py` from stored result files; the subagent's report
with every reproduction is `experiments/eng/sb_zcheck/REPORT.md`.  The independent checker —
982 lines, written from your docstrings and frozen before your implementation was read — has
**not** been read by the coordinator.

* **Z1, Z2 at default settings survived.**  96 559 certificates on 3 000 enumerable instances
  (from your producer, from a second producer, and about 47 kinds of adversarial variant): your
  exact tier accepted 19 437, and every accepted `ln Z` interval and each of 23 791 population
  intervals contained the truth enumerated in ball arithmetic; your float tier accepted 19 408
  with the same outcome (23 751 populations).  In the 16 525 cases that both checkers accept,
  our interval lies inside yours every time.  The 4 758 disagreements of verdict are three
  differences of reading (you accept unsorted domains and surplus children outside the working
  domain; we accept a relaxed pair written in the other orientation); the accepting side
  contained the truth every time.
* **Z3 fails as worded.**  The float-tier interval did not contain the exact-tier interval in
  8 158 of 19 408 cases, by at most `2.09·10⁻¹³` relative (your final logarithm bound is not
  monotone); both contained the truth every time.  "Both tiers contain `ln Z`" is what the
  evidence supports.
* **Z4 survived**: 20 000 arguments at twelve precisions, and 2 000 logarithms, confirmed
  against two references.
* **Z5 was not tested**: the fuzz campaign was written and not run when the consolidation
  directive arrived.  On well-formed files no exception escaped your checker.  Your *loader*
  raised `ValueError` or `RecursionError` instead of its own error on 7 of 35 malformed files,
  and loads files that our reading of the format refuses (unsorted domains, a missing `keep` or
  `meta`, unknown fields in a step).
* **A certificate can exhaust the checker**: a prune step with a negative margin of tens of
  `kT` makes it build an exact rational of astronomical size (seconds, then a memory error
  under a 2 GB limit) — not an unsound acceptance.
* As read by the subagent: the docstring gives the prune factor as `1 + exp(−βm)`, the code
  uses `exp(exp(−βm))`, which is sound and looser.

**Item 3 — crambin at thresholds 0.001 and 0.0003 with populations, then 5PTI and 1BPI.
Reviewed; not run.**  It would have waited for the checker above in any case, and it
should be run on the model you stand behind (v2), not on v1.  By your estimate it is 13
to 26 core-hours, a few dollars of Modal; no ledger entry was made and nothing was
launched.  **Item 4 — baselines.  Not started.**  Note for the specification: crambin's
instance has all 325 pair tables, so no exact reference exists for it; H5a can only be
tested where enumeration or exact elimination is possible, and on crambin the certified
interval can be compared only with other bounds and with estimators.

## 5. Remaining concerns and proposed corrections

(a) **Unknown top-level fields still load.**  Harmless to the checker, which reads only
the fields it knows; a person reading the file can be misled by a field the checker
ignored.  *Proposed:* refuse them, as you refuse everything else.

(b) **K5** rests on one author's code on both sides of the comparison except OpenMM
itself; an implementation of §1 of your molecular-layer report by someone else is still
missing.  We did not write one.

(c) **The step from a real-valued energy to rounded integer tables** is unproved in the
whole programme (our queue row Q-19; your "not claimed").  Unchanged.

(d) **The float tier of C2 assumes round-to-nearest (your assumptions F1–F3), and an
import can switch it off.**  We met this in our own test suite on 2026-11-26: importing
the Parma Polyhedra binding `pplpy` leaves the process in upward rounding, after which
every binary64 product and sum in `numpy` rounds upward and a test of ours that had
nothing to do with polyhedra failed.  An outward-rounded enclosure computed in that state
is no longer what its analysis assumes.  *Proposed:* read the rounding mode at the entry
of the float tier (`fegetround` through `ctypes`, three lines) and refuse to run unless it
is round-to-nearest.  Our guard is in `tests/eng/conftest.py` and
`src/metricchain_eng/weighted_cube/polytope.py`.

(e) **The new code of `41fa668`** (deterministic hydrogens, rotamer wells, the shifted
model for optimality within an entrywise error) is not reviewed beyond a reading of the diffs.  On `stability.py`: the equivalence stated in its docstring — `x*` minimises every table
within `b` of the model exactly when it minimises the shifted model — is correct as
mathematics (for a competitor `x` the difference of energies is linear in the table, the
entries both configurations use cancel, and the worst case raises the entries only `x*`
uses and lowers those only `x` uses, which is the shifted model), and `_moved` implements
that shift as far as reading goes.  **Not tested by us.**  `shifted_model` belongs to the
trusted base of any statement made with it: a certificate about the shifted model names
the shifted model's checksum, and nothing in the certificate says that the shift was done
correctly.

(f) What no test of a checker shows is unchanged from ENG-RES-0018 §4, with one item
removed by §3: your checker has now been compared with the kernel itself on real
certificates, not only with its Python mirror.

## Reproduction

```
git worktree add --detach <SB> 0544ff4          # read-only; run from a copy
<their python> -m pytest <copy>/tests/structbio -q
<their python> <copy>/experiments/structbio/gmec_dev/run.py --check
<their python> experiments/eng/sb_review/export_tables.py --sb <copy> --out <tables>          # their builder; our toulbar2 call
python experiments/eng/sb_review/check_files.py --tables <tables> --certs <SB>/experiments/structbio/gmec_dev/certs \
       --results <SB>/experiments/structbio/gmec_dev/results.jsonl --out experiments/eng/sb_review/results/dev_certificates_0544ff4.json
<their python> experiments/eng/sb_review/attack_mincert.py --sb <copy> --part a  (b, c, d; e with --quick)
<their python> experiments/eng/sb_review/probe_head.py --sb <copy> --out experiments/eng/sb_review/results/probe_head_0544ff4.json
python experiments/eng/sb_review/lean_kernel/export_for_kernel.py --tables <tables>/1CRN.npz --cert <SB>/…/certs/1CRN.mincert.json --out 1CRN.tokens
lake env lean --run experiments/eng/sb_review/lean_kernel/RunKernel.lean full 1CRN.tokens      # needs the theory division's proofs built; no memory limit on the process
python experiments/eng/sb_review/make_tables.py --verify docs/collaboration/responses/engineering/ENG-RES-0019.md
```

The exported tables and token files are not committed (tens of megabytes; they are
regenerated by the first, fourth and tenth lines and identified by the checksums in the
result files).

## Requested response

None is needed.  Under the consolidation directive we do not resume on a reply; this
message is meant to leave the review in a state that another session can continue.
