"""R7: inserts Section 1 (verdicts, verdict table, classified findings) into docs/science/workstreams/R7_REPORT.md,
filling the counts that depend on the last computations.  Usage:
    python3 insert_section1.py CERT UNCERT "<text for generic n=12>" "<text for n=22>" "<text for bracket ends>"
Idempotent: an existing Section 1 is replaced."""
import re
import sys
from pathlib import Path

REPORT = Path(__file__).resolve().parents[3] / "docs" / "science" / "workstreams" / "R7_REPORT.md"
CERT, UNCERT, GEN12, N22, BRK = sys.argv[1:6]
BB = int(CERT) - 241

SECTION = r"""## 1. Verdicts

**In one paragraph.**  I found **no wrong number** in the engineering division's results.  Every
quantity I recomputed with my own code — the generic chain (conformations and profile classes for
5–14 torsions, the covering numbers of 5–11 torsions, the tie analysis, 60 entropy numbers), the
lattice class tables for 1–22 torsions, the single-flip constants up to 14 torsions, the closed form
for the uniform-cube hitting numbers (all 52 stored rows) — is identical to theirs, and their stored
outputs regenerate bit for bit wherever I re-ran their code at reduced size.  All 288 published
lattice covers are valid certificates; of the 263 cells published as optima, **@CERT@ are certified
here without trusting any solver's search** (241 by an exact LP-duality certificate, @BB@ more by my
own branch and bound with an exact certificate at every pruned node) and @UNCERT@ remain optima by
HiGHS's branch and bound only; the other 25 cells are brackets.  The findings are about what the record
supports, not about values: (i) the sentence "two solvers agree on every cover / proved by HiGHS and
CP-SAT independently" rests on stored rows that no committed code produces — the committed driver
never runs the second solver on a cell the first one closes — and I could not reproduce a CP-SAT proof
with the one core I may use; (ii) ten lattice bracket ends and most generic ones are called
"certified" but are solver bounds, one to three above what is certified; (iii) "the excess decays
about like `1/√n`" is not what the X-005 data show (it decays faster; the exponent ½ is neither
established nor excluded), the search budget was cut at the two largest sizes without saying so, and
the `7·10⁶` "mean runs" are objective evaluations of an optimiser at the expectation level; (iv) the
off-lattice chain is *not* generic in the sense a floating-point treatment needs — its squared
distances are rational polynomials in `cos θ`, the "exact ties" are identities, and at 13 torsions
(the division's next size) one cell has 253 of them.  On the positive side the same structure shows
that the published off-lattice numbers are exact (covering numbers for `n ≤ 12`, class tables and
entropy numbers for `n ≤ 14`); the Harper reduction of ENG-RES-0008 §5
is correct as stated (re-derived, checked exhaustively on small cubes, and tested on a family with
non-ball level sets that the division had not tried: no claim violated, no worse instance); and the
total conformation counts of all 24 lattice tables, including the four produced on Modal, equal the
published series of diamond-lattice self-avoiding walks.

### 1.1 Verdict table

"Replicated" = own code written before reading theirs; "re-run" = their code executed here;
"read" = read, and where stated recomputed from their stored files with my own code.

| # | claim (source) | verdict | how | difference |
|---|---|---|---|---|
| 1 | generic chain: conformations and profile classes, `n = 5…14` (ENG-RES-0007 §3, -0009 §2) | **replicated** | `own_gen.py` | none |
| 2 | generic chain: 12-cell cover table, `n = 5…10` (72 cells incl. two open brackets) | **replicated** | `own_cover_table.py` | none (same two brackets, same ends) |
| 3 | generic chain: cover table, `n = 11` | 6 exact cells **replicated**; 6 brackets **consistent** | MILP (`L = 1/5`); own LP certificate + greedy (`L = 1`) | none in the values; 5 of the 6 lower ends are solver bounds, not certified ones |
| 4 | generic chain: cover table, `n = 12` | @GEN12@ |
| 5 | generic chain: "nearest tie"; five exact ties at `n = 11`, none elsewhere; classes `≥ 0.035` apart; hard-core margins | **replicated**, and explained | `own_ties*.py`; 60-digit re-evaluation | none |
| 6 | generic chain: distance entropy `σ(ρ)`, `n = 5…14`; pairs per bead | **replicated** | `own_entropy.py` | none (3 printed decimals) |
| 7 | generic-chain results carry the label "[X\*]" (floating point) | **strengthened**: exact (covers `n ≤ 12`; classes and entropy `n ≤ 14`) | Propositions G1–G3 | — |
| 8 | lattice class tables, `n = 1…22` (the tables of `n = 21, 22` were produced on Modal, job M-002) | **replicated** | `own_dia.c` | none (per class: count, fewest / most gauche) |
| 9 | lattice class tables, `n = 23, 24` (Modal job M-002) | totals **checked against the literature** (OEIS A001394 / 12, as for every `n ≤ 24`); @N22@ | `check_saw_counts_oeis.py` | none in the totals |
| 10 | the 288 lattice covers are covers of the stated sizes | **replicated** (certificates checked exactly) | `own_lattice_cert.py primal` | none |
| 11 | the 263 single lattice covering numbers are optima | **@CERT@ certified solver-independently**; @UNCERT@ **not** (HiGHS only; one of them re-solved by HiGHS in my own formulation) | exact LP certificate (241); `own_certified_bb.py` (@BB@) | none |
| 12 | "all 24 published covering numbers reproduced" | **replicated**, and certified | they are among the 241 | none |
| 13 | "two solvers agree on every cover"; "by HiGHS and CP-SAT independently for `n ≤ 18`" | **not reproducible from the repository; not confirmed** | re-run of the committed driver at `n = 14`: CP-SAT never called; CP-SAT with one worker on three cells: no proof | sentence vs record (finding M1) |
| 14 | lattice brackets, `n ≥ 19`: "`[certified lower bound, verified cover]`" | upper ends **replicated** (25 / 25); 15 certified lower ends **replicated**; 10 lower ends are solver bounds@BRK@ | `own_lattice_cert.py dual` | wording (finding m1) |
| 15 | lattice entropy table (ENG-RES-0002 §4), 50 cells | lower sides **replicated** where LP-certified (33 single values; all 10 bracket ends); upper sides **not checkable** (covers not stored); 7 values rest on branch and bound | `own_lattice_nets.py` | none |
| 16 | single-flip constants `c^{sf}` | `n = 3, 5, 8…14` **replicated**; `n = 15, 16` and the envelope-validity test **not examined** | `own_flip.c` | none |
| 17 | every trans/gauche pattern is realised (two-line proof) | **read**: proof correct | — | — |
| 18 | finite-size table and prose numbers of ENG-RES-0002, -0007 §2, -0009 §1 | **read**, recomputed from their stored tables | `check_eng_res_0002_prose.py` | three last-digit roundings |
| 19 | uniform-cube hitting numbers: closed form and table (ENG-RES-0006 §1) | **re-derived and replicated** (52 / 52 rows); their script **re-run**, byte-identical | `own_harper.py` | none |
| 20 | ENG-RES-0006 §2 (pricing as closure plus one budget row) | **not examined** (stated there as unimplemented analysis) | — | — |
| 21 | X-005: the generated tables of ENG-RES-0008 follow from the stored results | **re-run** (`make_tables --verify`); trend table rebuilt with own code | `x005_refit.py` | none |
| 22 | X-005: the stored search results are regenerated by the stated command | **re-run**: two cells bit-identical; all stored maximisers with `n ≤ 2000` re-evaluated | `rerun_engineering.sh … search`, `… recheck` | none |
| 23 | X-005: "no claim violated in 7 095 840 mean runs" | **read**: count and extremes agree with the stored files; what it means: Statement S1 | `check_record_numbers.py` | headline wording (m3) |
| 24 | X-005: "the excess decays about like `1/√n`" (digest) | **discrepancy with the data** (decays faster; Statement S2) | refit | finding m2 |
| 25 | X-005: "the flat instance is not the worst one" | **read + re-run**: the instances are in the class and the stored maximisers reproduce; correctness of the evaluator **not examined** (workstream R6) | — | none |
| 26 | X-005 §5: reduction of outer landscapes to tail functions (Harper) | **re-derived** [P] and checked numerically; scope note T(e); extra control on non-ball level sets **re-run** | `own_tail.py`, `rerun_eng_partial_shell.py` | none (correct as stated) |
| 27 | X-006: 585 000 literal runs without failure; "below `5.1·10⁻⁶` at 95 %, pooled" | **read**, recounted from the stored file; not re-run | `x006_recount.py` | none |
| 28 | X-001 (replication of the theory audit) | **not examined** | — | — |
| 29 | the tables of ENG-RES-0002, -0007, -0008, -0009 are generated from the artifacts | **re-run** (`make_tables --verify`, four documents) | | none |
| 30 | `python -m pytest tests/eng -q` | **re-run**: 128 passed | | — |

### 1.2 Findings, classified

**Critical** (a published result is wrong): **none found.**

**Major**

* **M1 — the two-solver validation cannot be regenerated, and what is stored does not show two
  proofs.**  *Where:* `docs/engineering/EXPERIMENT_REGISTER.md`, X-002, validation (vi);
  `docs/collaboration/responses/engineering/ENG-RES-0002.md` §1 ("Exactness"), §2 (note under the cover
  table), "Assumptions and limitations"; `docs/engineering/DEPENDENCY_MAP.md` ("minimum covers are
  optimal"); `src/metricchain_eng/chains/profile_cover.py`, `covering_number_P` (the loop over solvers);
  `experiments/eng/chain_cover/results/lattice_Sc12.json`, rows `n = 1…18`.  *What:* §3.2 (d).  *Effect
  on the numbers:* none that I could find — @CERT@ of the 263 values are certified here without any
  solver's search, and the sampled others agree with HiGHS in my own formulation.  *Effect on the
  claim:* "proved by two independent solvers" is, on the evidence in the repository, "proved by HiGHS;
  a second solver once found covers of the same size".
* **M2 — the floating-point treatment of the off-lattice chain is at its limit at the next size.**
  *Where:* `src/metricchain_eng/chains/generic_chain.py` (`ROUND_DECIMALS = 8`, `TOL = 1e-9`);
  ENG-RES-0007 §3–§4; the plan in `docs/engineering/RESEARCH_LOG.md` ("covers of the generic chain at 13
  and 14 torsions").  *What:* §2.1, §3.1 — exact ties are identities and become frequent (253 in one
  cell at 13 torsions), the nearest non-tie is `2·10⁻⁸` at 14 torsions, and the entropy table of
  ENG-RES-0009 already contains 305 exact ties (`n = 9, 10, 12, 13, 14`) that are reported nowhere —
  decided correctly only because the comparison carries a tolerance.  This is **not** a defect
  of any published number (those are exact, Corollary G3); it is a defect waiting in the announced
  continuation, with a clean remedy (request R7-ENG-3).

**Minor**

* **m1 — "certified lower bound" is said of bounds that are not.**  ENG-RES-0002 §2, ENG-RES-0007 §3,
  `docs/engineering/DEAD_ENDS.md` ED-3, the docstring of `generic_analysis`: ten lattice bracket ends
  (§3.2 (c)) and five of the six generic ones at each of 11 and 12 torsions are `max(certified, solver)`;
  `results/generic_Sc16.json` does not keep the two apart.  (For the entropy brackets the wording is
  accurate: all ten lower ends equal the certified bound.)
* **m2 — digest item 1** (`docs/collaboration/ENGINEERING_TO_THEORY.md`): "the excess decays about like
  `1/√n`"; see Statement S2.  The response itself (ENG-RES-0008 §3) is worded correctly.
* **m3 — ENG-RES-0008 does not state** the tolerance of "violation" (`10⁻⁷`), the search budgets per
  size (reduced at `n = 64 000` and `128 000`), or that the convergence control covers `u = 1`,
  `n ≤ 16 000` only; its headline number counts the objective evaluations of 2 624 searches.
* **m4 — provenance.**  `results/generic_Sc16_ties.json` has no generating script; the generic cover
  table has no stored covers and only a Modal entry point; stored result files carry no job id or
  commit (except the class tables for `n ≥ 21`); the ledger names a commit only for M-008 … M-011;
  ENG-RES-0007 cites ED-3 for job M-006.
* **m5 — three numbers computed from rounded table entries** (6.1 for 6.15; 0.014 for 0.0134; "rises
  by 0.2–0.3" of which one is 0.15).
* **m6 (for the theory division)** — the remark after Theorem 11.56 that adopts ENG-RES-0008 §5 drops
  the restriction to instances with a common fibre offset (T(e)); request R7-THY-1.

### 1.3 What is missing, and what a hostile referee would attack first (brief, item 6)

Claims with **no control or negative test** on the engineering branch: (a) the class *decomposition*
at 23–24 torsions — produced once, remotely, by one code; the 64-way merge is tested by equality with
a local run at `n = 14` only (now also: independent replications at `n = 21` and `22`@N22B@, and the
literature totals for all sizes); (b) the upper ends of the entropy brackets and of all generic brackets — the
covers are not stored; (c) in X-005: instances that are not of product form (one scalar offset serves
all fibres), level sets that are not balls (now: the cylinders of §3.7), other design parameters than
the one set used, and the search at the two largest sizes (smallest budget, no convergence control);
(d) in X-006: real inner brackets (stated by the division itself).
**I would attack, in this order:** (1) X-005 beyond product instances — an instance whose fibres sit
at different places of their trivial brackets is in the class, is outside the Harper reduction, and
nobody has evaluated one; (2) the two largest sizes of X-005, which carry "no persistent margin";
(3) the @UNCERT@ lattice optima that only HiGHS vouches for (`n = 16…19`, `ε ∈ {0, 1, N/20, N/10}`, and `(22, N/4)`);
(4) the class tables at 23–24 torsions.

---

"""

text = REPORT.read_text()
sec = (SECTION.replace("@CERT@", CERT).replace("@UNCERT@", UNCERT).replace("@BB@", str(BB)).replace("@GEN12@", GEN12)
       .replace("@N22@", N22).replace("@BRK@", BRK).replace("@N22B@", sys.argv[6] if len(sys.argv) > 6 else ""))
marker = "## 2. Precise statements, with proofs or counterexamples"
assert marker in text
if "## 1. Verdicts" in text:
    a = text.index("## 1. Verdicts"); b = text.index(marker)
    text = text[:a] + sec + text[b:]
else:
    text = text.replace(marker, sec + marker)
REPORT.write_text(text)
print("section 1 inserted;", len(text), "characters")
