# Workstream R24 (launched 2026-11-26) — adversarial referee of the division's results of this evening: the least ratio over states (addendum A17 (21), item 86), the Ensemble division's statements on our instances and a sandwich as a class of ensembles (part (22), items 87–89), and the split of the loss between groups (item 90)

*Brief written by the coordinator, who is the author of everything you are asked to attack.  Read `COMMON.md` first
(its commit pins are out of date).  Everything is in this repository at the commit you find checked out (branch
`research/scientific-translation`).  If the agent of this workstream is gone, its notes are in
`experiments/science/ws_R24/` and its draft in `R24_REPORT.md`.*

## Why

Between 17:49 and 19:28 UTC of 2026-11-26 the coordinator produced five results, wrote them into the addendum and
sent them to three other divisions (SCI-MSG-0031, SCI-RES-0032, SCI-MSG-0032).  Nobody else has read them.  The
referee of this morning's results (workstream R19) found four wrong statements of the same author, one of them a
formula called a measurement.  The research owner's directives (`docs/science/OWNER_DIRECTIVES.md`) ask for
adversarial verification, for the classes of every assumption, and forbid presenting a restricted result as
general.  Your job is to break these five, or to say exactly what holds.

## What to read

`docs/science/INFERENCE_LIMITS_ADDENDA.md`: item 86 (`grep -n "^86\. "`) and part (22), items 87–90
(`grep -n "^### (22)"`); as background item 84 (the scan) and part (19) (Proposition A17.19, in the docstring of
`experiments/science/pi_inference/slack_recovery.py`).  The three messages under `docs/collaboration/`:
`messages/science/SCI-MSG-0031.md`, `responses/science/SCI-RES-0032.md`, `messages/science/SCI-MSG-0032.md`.
The code and logs: `experiments/science/pi_inference/floor_ground_state.py` (four logs), `group_coupling.py` (six
logs), `floor_transition.py`, `first_order_recovery.py`; `experiments/science/ensemble_checks/thermal_union_bound.py`,
`sandwich_class.py` (five logs).  The predictions and the coordinator's own errors on the way are in
`docs/science/SCIENTIFIC_RESEARCH_LOG.md` (entries of 17:49, 18:20, 18:35, 18:49, 19:27 UTC).
The Ensemble division's statements that are imported: a read-only export of their branch at `1a067b5` is at
`/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/ens_ro_1a067b5/`
(`docs/ensemble/ENSEMBLE_REPORT.md`, Part IV, l.989–1210: Theorems E13, E15;
`docs/collaboration/responses/ensemble/ENSEMBLE-RES-0002.md` §1, §4).  Their theorems are **not** your object,
except where our statements use them.
**Not your object, and not to be reviewed:** parts (13)–(18) of the addendum.

## Item 1 — the least ratio (item 86; SCI-MSG-0031)

(i) Re-derive `G(λ) = max_x[λb(x) − c(x)] ≤ ln Z(m_λ) − ln Z(m₀)` and the claim "for `λ ≥ λ_gs` the floor has lost at
least `(λ − λ_gs)·b*`"; state every hypothesis (signs of the tables, the factor `RND`, what `c` is when `ln Z(m₀)` is
only known to double precision).  (ii) **Replicate `λ_gs` with code of your own** on one enumerable instance
(the floor of Lys₅ at order 4, band 2: every state can be evaluated — `min_x c(x)/b(x)` by brute force against a
ratio search with the model's own `(min,+)` pass) and, if memory allows (about 1 GB), on Lys₁₂ at order 4, band 4
by a ratio iteration that is not the script's bisection.  (iii) Is "`λ_gs` lies 1.1 to 3.3 % above the measured
`λ_c`" a statement about anything but four cases?  What would make the two differ by a large factor (give an
explicit small model if you can)?  (iv) The message says it is not a lower bound of `λ_c`: is there a rigorous
two-sided statement of the same cost that the coordinator missed?

## Item 2 — the thermal union bound on our instances (item 87; SCI-RES-0032 §§1–2)

(i) The generalisation to one-sided envelopes ("the polarised member is `∝ π e^{−d(·, a)}`"): re-derive it; find the
weakest condition on `d` under which it holds (triangle inequality? less?).  (ii) **Item 87 (c):** "the one-body
marginal vectors of a first-order class with a product reference are exactly the products of the one-site
classes" — prove or refute, including non-symmetric envelopes and envelopes that are not site-additive; then the
closed form of `b_min` for one-body data: is it the exact value of the programme of
`docs/science/INFERENCE_LIMITS.md` §9 (Theorem 8 (c)) for such data?  Test on random classes with a linear
programme of your own.  (iii) The numbers on Lys₅ and LKSE:5: is "the least site-additive envelope" what the
script computes, is the true scale exactly 1, and is the conclusion "certifies nothing as a falsification test"
fair — construct the most favourable use of their bound (b) you can think of (other centres, other data) and
say what it certifies.  The script takes about 40 s for Lys₅.

## Item 3 — the threshold rule on our sandwiches (item 88; SCI-RES-0032 §3)

Replicate the rule against brute force with your own code; replicate the law of the count under a band model
with a transfer matrix of your own on a small random band model against enumeration; then check the table of
item 88 against `sandwich_class_real.log`, and say whether "exact range over the sandwich" is exact given what
(the sandwich; double precision).  Do **not** review item 27 of part (13); the comparison column of the table is
recomputed by `sandwich_class.py` itself.

## Item 4 — a sandwich as a class of ensembles (item 89; SCI-RES-0032 §4)

(a) The identification with a first-order class for the metric `(D(x) + D(y))/2`: prove or refute (is it a metric
when some `D(x) = 0`? does their definition need one?).  (b) "A member is identified by the means of `Φ` inside
the sandwich iff … ; the ensemble of the true energy, strictly inside its sandwich, is never identified": read
their proof of E13 (b) and decide whether it applies to this polytope as used; treat level sets, states with
`D = 0`, data that are not means of indicator functions.  **Try to construct a counterexample** (a member with
weights strictly inside the box on some states that is nevertheless determined by finitely many means).
(c) The stability bound `TV(μ, μ_f) ≤ (t* − E_μ f)/γ`: the proof; the best constant; what happens as `γ → 0`.
(d) The certificate for a sandwich with data and the remark on its cost.  (e) **Prior art**: the class is the
density-ratio class of robust Bayesian analysis.  Find where (1)–(4) of `sandwich_class.py`'s header are in print,
with reading levels (opened in full / abstract / search summary / memory) — generic search queries only; nothing
of this project may be put into a query.

## Item 5 — the split of the loss between groups (item 90; SCI-MSG-0032; SCI-RES-0032 §5)

(i) Re-derive every line of the table: the criterion "`Σ_g P(S⁺_g > 0) ≤ 1` ⇒ (LP) is the optimum from the group
laws" (and whether its converse holds); the upper-end quantities `C′`, `C₂`, `C″` — is each a valid bound of the
kind Proposition A17.19 needs, is `C′ ≤ C₂ ≤ C″`, and is the solved upper end monotone in `C`; and **the
characterisation of "the rest"** as "the price of bounding a mean under the true ensemble by one under the
ceiling, not a matter of joint laws": is that what `v(C″) − ln Z(m₋ + s₋)` is?  Could a joint law of the items
under the *floor* recover it?  (ii) **Replicate the row of Lys₅ at order 4, band 2** with code of your own from
the item tables (run `first_order_recovery.py K5 4 2 --enum` into your own directory, or take its objects as
`group_coupling.py` does, but compute every number of the row yourself by enumeration).  (iii) The Lys₁₂ rows
rest on samples: are the error bars right for heavy-tailed variables; is "pair terms alone would take 0.61 of
the bracket" supported; compare with workstream R19's measurement (`docs/science/workstreams/R19_REPORT.md`).
(iv) SCI-MSG-0032 calls itself a refinement, not a correction, of SCI-MSG-0030 §2 (a): is that the right word?

## Item 6 — the numbers and the words

Every number of items 86–90 and of the three messages against the logs.  Every sentence that says more than was
computed or proved.  The class of each assumption (essential / proof technique / convenience / replaceable by a
weaker quantitative condition / removal changes the complexity / removal makes it false) for the statements of
items 86, 87 (c), 89.

## Rules

Write only in `experiments/science/ws_R24/` and `docs/science/workstreams/R24_REPORT.md`.  No state-changing git
(`git show`, `git log`, `git diff` are fine); no subagents; the network only for literature searches and page
fetches, with generic queries.  **Do not modify, move or delete anything outside your directory** — in
particular not the caches under `experiments/science/p9_verification/`, `ws_P8/`, `ws_P9/`,
`pi_inference/serine_helix_reach_cache/`, and not the committed logs: if you re-run a coordinator's script,
redirect its output into your own directory.  Keep four kinds of checking apart and say which you did for each
statement: **review** (re-derived), **replication** (own code written from the statements), **re-run** (the
coordinator's code), **read only**.  Never fabricate; reading levels for anything cited.  A finding is
*critical*, *major* or *minor*; give a replacement text for each.  Report what you did not check, and your own
errors.  Machine: 4 cores and 15 GB shared with other jobs — `OMP_NUM_THREADS=1`, at most two processes, no
process above 3 GB (print the peak RSS in the last line of every script; look at `free -g` before a run above
1 GB), no run longer than 15 minutes — and before any run of more than five minutes write into `NOTES.md` its
cost per step, the number of steps and what its result will be compared with.  Keep `NOTES.md` from the first
minute.  A log is cited only if its run reached its last line; logs of stopped or failed runs go into a
subdirectory `not_cited/` and are named in the report; use fresh names instead of overwriting a log.  A time
written into a file is read from the clock at that moment.  Every check is reported with the violations of its
control, and a control must be able to fail.  A violation planted for a numerical solver must be large against
the solver's tolerance.  **If a tool declines an action, do not work around it: keep everything in `NOTES.md` and
return the findings as text in your hand-back, with a line "Tool actions declined".  Do not delete files with
wildcards or `rm -r`.**  This is an internal review, not external peer review; say so in the report.

## The report

(0) Verdict in ten lines.  (1) The statements as you understand them, with the hypotheses the texts leave
implicit.  (2) Findings — critical, major, minor — each with the line that decides it and a replacement text.
(3) Your own tests, with their controls.  (4) The numbers against the logs.  (5) Prior art for item 4, with
reading levels and every address opened.  (6) What you did not check; your own errors; files.  Hand back a
summary of at most sixty lines.
