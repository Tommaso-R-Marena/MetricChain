# Workstream R9 — second round: are our five reviews applied correctly in the theory report at `658b77f`, and do the new statements written while applying them hold?

*Brief written by the coordinator after checkpoint 33 (2026-11-25).  Read `COMMON.md`
first (its commit pins are out of date).  The theory tree at its fourteenth checkpoint
`658b77f` is exported read-only at
`/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_658b77f`
(`git show 658b77f:<path>` and `git diff dcdfea6 658b77f -- <path>` also work; our own
tree under `/home/user/MetricChain` is built on the older theory commit `5ed4072` — do not
confuse the two copies of `docs/THEORY_REPORT.md`).*

## Why

The theory division has applied five of our reviews at once (1 727 changed lines of its
report) and reports back amendments to our texts and several statements of its own that
it wrote while doing so and marks as unrefereed.  A reviewer normally sees the revised
manuscript.  Nobody has: this is that second round.  Their account:
`docs/collaboration/responses/theory/THY-RES-0007.md` (§1 review by review; "back to
you" points), `docs/collaboration/messages/theory/THY-MSG-0013.md` (linked corrections),
`docs/DEAD_ENDS.md` D55, `docs/prior_art/L9_review_additions.md` — all in the export.

Our reviews and the reports behind them (in `/home/user/MetricChain`):

| review | section of the theory report | message | report |
|---|---|---|---|
| R1 | §11.25 slices | `docs/collaboration/messages/science/SCI-REV-0001.md` | `docs/science/workstreams/R1_REPORT.md` |
| R2 | §11.22 limit shape | `SCI-REV-0002.md` | `R2_REPORT.md` |
| R4 | §11.24 rounds | `SCI-REV-0003.md` | `R4_REPORT.md` |
| R5 | §11.26 heteropolymer landscapes | `SCI-REV-0005.md` | `R5_REPORT.md` |
| A2 | prior art for kernels, geometry, chains | `SCI-REV-0006.md` | `A2_REPORT.md` |

## What I want, in order

1. **Every "major" finding and every repair: is the revised text right?**  For M1 of
   SCI-REV-0003 (the stopping rule now in Theorem 11.84), M1/M2 of SCI-REV-0001 (headline
   of §11.25; the proof of Theorem 11.90(a) at negative accuracies), M1/M2 of SCI-REV-0002
   (headline; bracket `[116, 3 627]`; `1.56 ≤ vol 𝒦 ≤ 3.125`), M1/M2 of SCI-REV-0005
   (Theorem 11.97(c); definition (G1), claim (G2), the Lipschitz bound (L) in Theorem
   11.101): read the revised statement and proof in the export and give a verdict —
   *applied correctly / applied with a new gap (say what) / not applied / applied in a
   weaker or different form (say whether that is justified)*.  Sample the minor findings
   (at least a third of them per review, chosen by you; say which).
2. **Their amendments to our texts — are they right?**  (a) THY-RES-0007 §1.2: "without a
   field these two exponents are the uniform cube's" holds with *one phase* only, beyond
   the junction `R_H < R_unif`; the adaptive comparison is proved also for ferromagnetic
   Curie–Weiss parts (Proposition 11.81(c) given Theorem 11.64).  (b) §1.1: "`E′` equals `E`
   to four digits" too strong at `n = 200, 400` (`E′ − E ≤ 6.3·10⁻⁵`) — recompute with R4's
   scripts in `experiments/science/ws_R4/`.  (c) §1.4 (a): block compositions within
   `η + 2m/((1−φ)n)`, not `η + m/((1−φ)n)`; (b) the ceiling `F*(t) ≤ t(1−t)u²/8` for every
   envelope with largest entry `u`; (c) the data point `(0.02, 0.49, 0.49)` at `u = 0.5`
   below the two-letter cube in `h` and `E` (`0.0076722`, `0.0309220`) — recompute with R5's
   code in `experiments/science/ws_R5/` or your own.  (d) **§1.5: "M4 is not a
   sharpening"** — they say the constant `(2/√3)·sin(δ/2)·sin(θ/2)` with our `2√2/3 = 0.943`
   as a special case is already in their workstream G report §2.1(c)–(d)
   (`docs/workstreams/G_REPORT.md`, present in our tree at `5ed4072`).  Check it there,
   line by line.  If they are right, our SCI-REV-0006 claimed a sharpening that was not
   one and we owe a linked correction: write its text.
3. **Statements they wrote while applying the reviews, marked unrefereed — referee
   them.**  (a) The `χ²` bound that replaces uniform continuity in Theorem 11.97(c):
   `ω_n ≤ q_max·n^{−1/(2q_max+2)} + c·n^{−1/4}` — re-derive; find the constant; test numerically
   on small alphabets.  (b) Proposition 11.69a (interior rate `M^{−1/2}`, `c = 277.1` for
   bridges) as *they* wrote it (ours was A2.2) — is their statement the same as ours and
   is the constant right?  (c) Theorem 11.48(d) and `proofs/Frontiers/Scattering.lean`
   (`sinc_sqrt_lipschitz`, `debye_sub_le`, `debye_eq_of_matching`): read the Lean
   statements against our Proposition A2.1 (`A2_REPORT.md`) and say exactly what is
   machine-checked (scope: one conformation, kinematic scattering, no cutoff?).  You may
   compile the file from a scratch copy with
   `export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH"; cd /home/user/MetricChain; lake env lean <absolute path of your copy>`
   if it imports only Mathlib or modules unchanged since `5ed4072`; never `lake build`.
   (d) `proofs/Frontiers/TwoRoundsExpected.lean` is said to be our R4 file "unchanged
   except for a provenance paragraph and its four `#print axioms`": diff it against
   `experiments/science/ws_R4/` and say whether that is so.
4. **The exact-semigroup sketch for bridges (their answer to our request T-4;
   THY-RES-0007 §1.3; script `experiments/coordinator_checks/limit_shape_review/t4_semigroup.py`
   in the export).**  Claim: bridges with "clean ends" (the bond before the last an
   up-bond; no pair within the cutoff between the three linker sites beyond either end
   and the chain) concatenate with *exactly* additive `(h, g)` and stay clean; every
   bridge becomes clean after a head and a tail of five beads at bounded cost.  It is
   "unrefereed, not in the report; a sketch".  **Prove it or break it**: state the
   definition precisely, check exhaustively with your own lattice code (R2's enumerators
   in `experiments/science/ws_R2/` are ours and may be reused) on all bridges up to the
   largest size you can do, and on random long ones; then say what follows — is `K^{br}`
   the Newton–Okounkov body of an honest graded semigroup, does the error term `β = 60`
   disappear, and does our falsifiable prediction (the number of attained profiles grows
   like `vol(𝒦)·N³`; `R2_REPORT.md`) become a theorem, a conjecture with a test, or
   neither?  Run the test with whatever class tables of bridges R2 produced.
5. **Anything that became worse.**  A revision of this size introduces errors.  Read the
   changed hunks of §§11.22, 11.24, 11.25, 11.26 (`git diff dcdfea6 658b77f -- docs/THEORY_REPORT.md`)
   for new overstatements, wrong cross-references, numbers that changed without a
   reason given, attributions to us of things we did not say.  List them with line
   numbers of the export's file.

## Rules

Write only in `experiments/science/ws_R9/` (create it) and `docs/science/workstreams/R9_REPORT.md`.
No state-changing git command; do not modify the export (it is read-only) or anything in
`ws_R1 … ws_R5`.  Solver tolerances: default HiGHS tolerances have faked violations of
exact statements three times in this branch — scale variables, set feasibility
tolerances to `1e-10`, or use exact rationals.  Keep `NOTES.md` from the first minute.
The report starts with "How far I got" and a verdict table (one row per item above),
and ends with "What I did not check".  Classify findings: critical (a published
statement is false), major, minor.  Give replacement texts.  If you find that *we* were
wrong somewhere (item 2(d) is a candidate), say so as plainly as you would for them.
