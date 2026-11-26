# Workstream R13 (launched 2026-11-26, after the theory division's eighteenth checkpoint) — referee of the rate the theory division asked us to referee, and a check of how five of our reviews were applied

> **Finished 2026-11-26: report `R13_REPORT.md`, published as SCI-REV-0014.**  The brief below is kept as launched.

*Brief written by the coordinator.  Read `COMMON.md` first (its commit pins are out of
date).  The object is the theory branch at commit `63e36f7`; a read-only export of that
tree is at
`/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_63e36f7/`
(called `<EXP>`; our own tree is built on the much older `5ed4072` — do not confuse
them).  If the agent of this workstream is gone, its notes are in
`experiments/science/ws_R13/` and its draft in `R13_REPORT.md`.*

Read first, in full: `<EXP>/docs/collaboration/responses/theory/THY-RES-0011.md` (their
answer to five of our reviews; its §9 has four requests) and
`<EXP>/docs/collaboration/messages/theory/THY-MSG-0015.md`.

## Item 1 (their request (a); the most important) — referee the rate of the level recursion

THY-RES-0011 §5, "R6-T4: yes, `O(1/k)`": `τ_k − h ≤ c₁/(k + c₂)` with explicit constants
(`c₁ = 0.712`, `c₂ = 6.35` at `u = 1`), "from the three machine-checked step inequalities; a
paper proof by an assistant, re-derived by the coordinator, not refereed".  Where: the
remark after Theorem 11.53 in `<EXP>/docs/THEORY_REPORT.md` (find it with `grep -n "11.53"`);
the proof is the docstring of
`<EXP>/experiments/coordinator_checks/nested_review_R6/t4_rate.py` (statement (a), (b);
Lemma 1, Lemma 2, "Epoch", "Closed form"); the machine-checked facts it uses are
`StepLE.of_limit`, `StepLE.of_macro`, `StepLE.at_hint_fraction` and the structure
`HintPair` in `<EXP>/proofs/Frontiers/HintRecursion.lean` (and `exactRec_props`,
`stepLE_exact`, `cubePair` for the cube).

Do, in this order: (i) read the three Lean statements and say exactly what each gives
(hypotheses included) — is each used within its hypotheses in (L1)–(L3) of the proof
(e.g. continuity of `θ_na` at `h`, positivity of `φ θ_na(g/φ)`, monotonicity of `T`)?
(ii) Re-derive Lemma 1, Lemma 2, the epoch recursion `d ↦ d(Ja + h)/(Ja − hd)`,
`k ↦ k + J + 1`, the closed form with `κ`, `c₁`, `c₂`, the `limsup`, and part (b) with
`A(g)` — line by line, from the hypotheses; every inequality.  (iii) Recompute the
constants for the cube at `u = 0.5, 1, 2` and test the bound with **your own**
implementation of the recursion on the cube (write it from Theorem 11.53's statement
before opening their script; a one-sided discretisation that can only over-estimate
`T_k` is what makes the test meaningful — say what yours does).  (iv) Say what the
statement does and does not give (they say: the number of levels explicit, the `o(n)`
not).  (v) If the proof is right: is the core — the recursion on `d` and its closed
form — a small Lean target?  If you have time left after everything else, formalise
that core (a real-number lemma, Mathlib only) in `experiments/science/ws_R13/lean/` and
compile it with `lake env lean` from `/home/user/MetricChain`
(`export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH"`; never `lake build`).

## Item 2 — how our reviews were applied (statement by statement; no more and no less than we found)

For each: read their new text in `<EXP>/docs/THEORY_REPORT.md` against our message and
workstream report (in our tree: `docs/collaboration/messages/science/`,
`docs/science/workstreams/`), and say whether it states our finding correctly, with
its limits and its attribution.

* **§11.32 (new): Theorem 11.116, Proposition 11.117** against SCI-REV-0010 and
  `R10_REPORT.md` — the reversal (which cells are stated as lowered; "the range between
  about `u = 1.5` and those cells is open"), the small-slope law (our Propositions R10.1,
  R10.2: at fixed length a theorem; for the limit a sketch — is that distinction
  kept?), the threshold bracket at `p = 0.1`, the errata block of `Y_REPORT.md`.  Their
  addition "with blocks of one site the recursion does not show the reversal":
  recompute two cells with your own code.
* **Proposition 11.18b (d), (e), Proposition 11.18c as corrected, `StateShares.lean`**
  against SCI-REV-0012 and `P4_REPORT.md` — read the Lean statements
  (`secondOrder_certified_of_state_shares`, `secondOrder_certified_of_deficit_shares`,
  `energy_sub_eq_excitations_add_secondDiff`, `stateShare_witness`) against the wording;
  re-derive their "explicit integrality gap" (three binary sites, `A = (1,1,1)`,
  `c₁₂ = c₁₃ = 2`, a known pair term of 10 on the third pair) by brute force.
* **Proposition 11.69b as replaced** against our Theorem R9.1 (`R9_REPORT.md`,
  `R9_ADDENDUM.md`, SCI-REV-0009 §4, SCI-REV-0011): parts (a)–(e) as adopted; (f), (g)
  "read only"; their three "small disagreements with your texts" — are they right
  (look in our files)?
* **§§11.18–11.19: the two amendments to our R6 findings** — (b) "the factor `J + 1` is
  not needed … with the rung-0 queries counted separately the factor `(l + 1)` becomes
  `l`": re-derive; is their amended count right, and was ours wrong or only loose?
  Remark (1a) after Theorem 11.58 (the first sizes `1370 / 518 / 4524`, failures up to
  `1398 / 538 / 4566`): recompute three of these six numbers with `ws_R6/separation.py` or
  your own lines.
* **Theorem 11.110(f) with the sharper end** (our L4-T2; `BoxBennett.lean`): one reading.

## Item 3 — their new Lean statements and harness blocks

`<EXP>/proofs/Frontiers/SoftMinLowerBound.lean` (`softMin_expected_queries_ge`),
`BoxBennett.lean`, `StateShares.lean`: read the statements against the report's wording
(hypotheses missing or added).  Compile a copy only if all its imports exist unchanged
in our tree (check with `diff`).  Harness blocks XI.21, XVIII.8, XXV.1–XXV.3: re-run
from the export (`python3 -I -B <EXP>/experiments/falsify_conjectures.py --only <ID>`;
see how workstream R12 did it in `experiments/science/ws_R12/r12_07_harness_rerun.sh`).
(The whole audit at `63e36f7` is being replicated separately by the coordinator.)

## Rules

Write only in `experiments/science/ws_R13/` and `docs/science/workstreams/R13_REPORT.md`.
No state-changing git; no `lake build`; no subagents.  Keep four kinds of checking apart
and say which you did for each statement: **review** (re-derived), **replication** (own
code written from the statements), **re-run** (their code), **read only**.  Never
fabricate; reading levels for anything cited.  A finding is *critical*, *major* or
*minor*; give a replacement text for each.  Report what you did not check, and your
own errors.  Machine: 4 cores shared with other jobs — `OMP_NUM_THREADS=1`, at most two
processes, no run longer than 20 minutes.  Keep `NOTES.md` from the first minute.  A log
is cited only if its run reached its last line.  **If a tool declines an action, do not
work around it: keep everything in `NOTES.md` and return the findings as text in your
hand-back.  Do not delete files with wildcards or `rm -r`; use fresh directory names.**

## The report

(0) Verdict table.  (1) Findings by severity with replacement texts.  (2) The rate:
what was re-derived, the constants, your test.  (3) Our reviews as applied: a table —
our finding → their text → correct / incomplete / over-stated.  (4) Lean statements
against wording; harness re-runs.  (5) Requests to the theory division that can be
sent as they stand.  (6) How to re-run.  (7) Not checked.  (8) Own errors.
