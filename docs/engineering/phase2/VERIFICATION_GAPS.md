# Workstream C — the verification gaps left by Phase I

*Computational Research Division, Phase II, 2026-11-28.  Items 1–3 were carried out by a subagent
(`experiments/eng/phase2_gaps/REPORT.md`, scripts and raw outputs beside it); the coordinator read its
tables, checked its stored outputs, and repeated the runs named below.  Items 4–5 are the coordinator's,
from a subagent's digest (`experiments/eng/phase2_digest/DIGEST.md`, Parts 2–3) checked against the
archive where stated.  Unfavourable findings are kept.*

## Summary

| gap recorded at the end of Phase I | now |
|---|---|
| the twelve later structural-biology certificates were never checked by engineering | **12 of 12 accepted** by engineering's two checkers and by the structural-biology (SB) division's repaired checker; **12 of 12 accepted by the memoised twin of the theory division's kernel**; negative controls refused |
| the float-tier exploit (finding F1) was found on old code; the repair was untested | **reproduced on the old code, refused by the repaired code**; a probe of the repair found no acceptance that misses the exact value |
| the memoised kernel had been run on six certificates only | run on all twelve later ones, 1.4 s to 196 s of checking, peak memory 4.9 GB on the largest |
| referee R29's concerns about certified constants were unanswered | **one correction of ours**: the constants `c_k` as quoted by engineering are rounded to nearest and three of five are not upper bounds as quoted; the file they come from is the run R29 did not check |
| "certified" was used for evaluations of cost formulas | classified below; **3 of 22 experiments are formula evaluations called certified** |

What is still not verified is listed at the end.

## 1. The twelve later certificates of the SB division

At its final head `a5cc106` the SB division has six certificates of its first energy model (the ones
engineering and the kernel had checked) and twelve of its later models, `certs/v2/` and `certs/v2-lib/`
(1CRN, 5PTI, 1BPI, 1PGA, 2IGD, 1UBQ in each).

* **All twelve are accepted** by engineering's `check_files.py`, by engineering's `indep_mincheck`
  (through an adapter, because that checker reads only the embedded format — so the two engineering
  checkers share one parser), and by SB's own repaired checker; in each the tree proves exactly the
  claimed bound, the witness has gap zero, the bound equals SB's stored row and the optimum of
  engineering's own toulbar2 call.  A claim raised by one unit and an altered table entry are refused by
  all three.
* **The energy tables are regenerated, not stored**: SB keeps no table files, so they were rebuilt with
  SB's builder (its molecular code is byte-identical between the commit engineering had reviewed and the
  final head).  Their checksum, computed by engineering's code, equals the one inside each certificate.
  So the certificates are checked against tables that do not come from the certificates — but **the
  physics that produces the tables is SB's code and was not verified by anyone** (SB's claim K5).
* Repeated by the coordinator: `check_files` on v2/1CRN and v2/2IGD and `indep_mincheck` on v2/1CRN and
  v2-lib/2IGD, from the exported tables — same checksums and verdicts.

Sizes and times: 323 to 2,428 eliminations; 0.03 to 4.2 s per check.

## 2. The floating-point exploit and its repair

Finding F1 of engineering's Phase I review (`experiments/eng/sb_zcheck/REPORT.md`): at `exp_bits` 990
and 991 the float tier of SB's partition-function checker accepted an interval 0.31 nats away from the
true `ln Z`.

* On the old code (`41fa668`) it reproduces exactly: accepted `[−677.0000000006, −676.9999958362]`
  against `−676.6867383125`.
* On the repaired code (`a5cc106`) it is refused: the parameter is now range-checked (16 to 512 in the
  float tier), and the faulty conversion itself was corrected.  Repeated by the coordinator.
* A probe of the repair (104 calls: the boundaries of the new range, neighbouring values, two families
  of energies) found **no acceptance that misses the exact value**.
* Of the other eight findings of that review: fixed F4, F7, F8 and the memory exhaustion of F3; partly
  fixed F5 (five lax loader cases remain); unchanged F2 (SB's claim Z3 is still false as worded, with
  no unsound interval), F3's looseness, F6, F9.  **New**: the repair refuses 15 certificates that
  engineering's checker accepts — a loss of completeness by design, not of soundness.

## 3. The memoised kernel

`verifyM` (engineering's `RunKernel.lean`), proved equal to the theory division's verified kernel
`verify` by `verifyM_eq`, **accepts all twelve later certificates** and refuses each with its bound
raised by one unit; the kernel's own witness energy equals the bound and the digests of the tables
match the Python side.  Checking takes 1.4 to 9.3 s on ten of them, 22 s on 2IGD (v2), 121 s and 196 s
on the two ubiquitin certificates; loading the proof library 1 to 1.5 minutes; peak memory 4.9 GB.

What this is: an evaluation by Lean's runtime of a function proved equal to the verified one — not a
proof term.  Trusted besides Lean's kernel: the runtime, engineering's reader and translator (checked
through digests and the kernel's own witness energy), and the identity of the tables.  The unmemoised
`verify` remains impractical (its time grows about 1.8-fold per elimination, ENG-MSG-0008 §2); the
theory division never read that report, and a compiled target in its tree is still missing.

## 4. Referee R29's concerns about numerical certificates, where they touch engineering

R29 is the science division's incomplete review of the theory division's Theorem 11.58e and of the
script that certifies the exponents `c_k` of nested levels (SCI-REV-0030).  Its findings, as the digest
quotes them: **F1 (major, "evidence, not numbers")** — the script's verdict cannot fail: "of 30
mutations, 2 are caught by the script …; 17 break a certificate and still end with 'ALL CHECKS PASS'",
among them one that prints `c₂` below `τ₂` as certified; F2–F4 minor (a proposition that does not
literally cover a cap line; the base case of the certified sequence; **printed numbers rounded to
nearest, not upwards**); F5–F7 concern Theorem 11.58e itself.  R29's own independent exact checker
confirmed the certified tops of the 80-level run at slope 1 and the 40-level runs at slopes ½ and 2 with
no violation.  **Unfinished: the 400-level run.**

Where this touches engineering — checked by the coordinator in the theory tree of the archive:

* Engineering's finite-size tables (ENG-RES-0015 §2; the addendum on the late rows) subtract the
  constants `c_2 … c_6` from its own bounds.  It took them from
  `out_z6_certified_u1_J400.txt` — **the 400-level run, the one R29 did not check** — whose values
  are `c_k/a = 0.500410019, 0.363300651, 0.312791457, 0.291376730, 0.281323057`.  (The shorter run
  that R29 did check gives the same values to seven decimals: `0.500410024, 0.363300653, 0.312791462,
  0.291376787, 0.281323250`.)
* **A correction.**  Engineering quoted them as `0.5004, 0.3633, 0.3128, 0.2914, 0.2813` and called
  them "certified upper bounds".  Rounded to nearest, **three of the five (`c_2`, `c_3`, `c_6`) are
  below the certified values, by at most `2.3·10⁻⁵`; as quoted they are not upper bounds.**  Affected
  text: ENG-RES-0015 §2, the comment in `experiments/eng/twolevel/make_tables_x011.py`, the addendum.
* **Effect on published numbers: none at the printed precision that changes a conclusion.**  The
  constants enter as `bound − c_k`, in units of `n·a`; an error of `2.3·10⁻⁵` is at most 0.33 nats at
  `n = 128 000`, against overheads of hundreds of nats, and can move a printed integer of nats by one.
  The shares of the hypothesis H13 are quotients of differences of the `c_k`; the addendum already
  carries a column for a rounding of `±5·10⁻⁵` per constant, which covers this, and its one verdict
  inside that margin (the share `0.5018`) was already reported as undecided.  The tables were **not**
  regenerated; this note is the correction of record, and ENG-MSG-0009 §3 tells the other divisions.
* Engineering's statement that the constants are certified rests on the theory division's script and,
  for the shorter runs, on R29's independent checker.  Engineering has not recomputed them.

## 5. Certified computation, and evaluation of cost formulas

The research owner asked for this distinction to be made.  Kinds: **K** a certificate about a concrete
instance accepted by a run of a machine-verified kernel; **C** accepted by an independent
exact-arithmetic or rigorous-arithmetic checker; **L** a literal run of an algorithm on concrete small
instances; **S** a simulation in a model of the algorithm, or a searched worst case; **F** evaluation or
minimisation of a published cost-bound *formula* — no algorithm is run on any instance; **E** exact
enumeration.  Main kind of each Phase I experiment (the digest's table quotes the register's words for
each):

| kind | experiments |
|---|---|
| K | X-017 (the kernel on SB certificates: Phase I six, now eighteen).  X-001 is a build of the theory division's proof library, not an instance certificate |
| C | X-012 (shares at the leaves), X-016 (SB `min` certificates), X-018 (SB partition-function certificates), X-019 (a certified maximum on the 4-torus) |
| L | X-006, X-006b (literal two-level runs, 8–16 sites, with oracle inner brackets), X-015; parts of X-011 (15 sites) and X-014 (11–16 sites) |
| S | X-005, X-005b, X-005c (searched worst cases in the mean-run model; X-005c not converged), X-010; parts of X-011 |
| **F** | **X-009** (crossover sizes), **X-011(a)** (the bound of nested runs to six levels, all sizes to 128 000, all slopes), **X-014(a)** (bounds on 75 mixtures) |
| E | X-002, X-003, X-004 (floating point), X-007, X-008, X-013 |

**Where engineering wrote "certified" for a result of kind F or S.**  X-009's title ("certified to
win"); throughout X-011 — "designed by certified cost", "the certified recursion to six levels", "best
certified bounds found", "no searched cost above a certified bound"; X-010 ("charged its certified
bound"); X-014 ("certified bounds on 75 mixtures", "a certified algorithm with finite-size constants" —
conditional, by the register's own words, on a proof transfer by one author); the comment on `C_UP`.

**What those words meant, and what they do not mean.**  In X-009, X-011 and X-014 "certified" refers to
the *theorem*: the number is the cost bound that Theorem 11.56 (a paper proof of the theory division,
refereed inside the programme) guarantees for a design, evaluated by engineering **in floating point,
without interval arithmetic** — as its consolidation report says in one sentence — and, in X-011,
minimised over finite families of designs by searches of which 20 of 33 at the larger sizes did not
finish.  No algorithm was run at those sizes; no instance was certified; no rounding was controlled.
The only results of engineering that are certified computations about concrete instances are those of
kinds K and C above.  For reading any engineering document of Phase I: **"certified bound" in the
context of nested or two-level algorithms means "evaluated formula of a paper theorem".**  The Phase I
documents on the original branch are not edited; this section is the correction of record, and the
Phase II documents use "certified" only for kinds K and C and for the statistical certificates of
`CERTIFIED_INFERENCE.md` §5, whose meaning is stated there.

## 6. Still not verified

* The physics behind the SB energy tables (K5), and the rounding of real energies to integers.
* The SB repair beyond what the reproducers touch; the fuzz campaign for claim Z5 and the
  rounding-mode experiment of Phase I were again not run.
* The 400-level run of the theory division's certified exponents (unchecked by anyone but its
  authors); a recomputation of the constants by engineering.
* Whether the X-011 formula evaluations survive interval arithmetic (expected to, at the printed
  precision; not done).
* Engineering's test `tests/eng/test_sb_zcheck.py::test_finding_f3…` asserts an acceptance that the
  repaired SB code now refuses on purpose; it passes against the code it was written for and fails
  against `a5cc106`.  Left as it is, with this note.
