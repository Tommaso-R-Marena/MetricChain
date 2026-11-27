# Workstream R19 (launched 2026-11-26) — adversarial referee of the division's own newest results: the recovery of the band's slack and the held-site passes (addenda A17 (19), items 69–75, and A17 (20), items 77–81), and Part A of the assumption audit

*Brief written by the coordinator, who is the author of everything you are asked to attack.  Read `COMMON.md` first
(its commit pins are out of date).  Everything is in this repository at the commit you find checked out (branch
`research/scientific-translation`).  If the agent of this workstream is gone, its notes are in
`experiments/science/ws_R19/` and its draft in `R19_REPORT.md`.*

## Why

Since the morning of 2026-11-26 the division publishes deterministic brackets of `ln Z` of `10⁻⁴`–`10⁻⁵` nats that
rest on a chain of statements only one of which has been checked outside the coordinator: Proposition A17.19 (the
four inequalities) is machine-checked on finite spaces by the theory division (`GibbsRecovery.lean` on their
branch, commit `3cf14b9`; you need not re-prove it).  **Everything between that proposition and the printed
numbers is unrefereed**: that the tables fed to it satisfy its hypotheses; that the means are exact; the
bookkeeping of a rounding allowance; the routing; the code.  And the division has just written an audit of its
own assumptions (`docs/science/ASSUMPTION_AUDIT.md`, Part A) with two new propositions and a hierarchy.  The
research owner's directives (`docs/science/OWNER_DIRECTIVES.md`) ask for adversarial verification and forbid
presenting a restricted result as general.  Your job is to break these, or to say exactly what holds.

## What to read

`docs/science/INFERENCE_LIMITS_ADDENDA.md`: part (19), items 69–75 (`grep -n "^69\. \|^7[0-9]\. \|^8[01]\. "`), and part
(20), items 77–81; before them, as needed, items 59–68 (the window models, the split of far pairs around the
anchor, the reductions that know the occupancies, workstream P9's resolved tables).  `docs/science/ASSUMPTION_AUDIT.md`
in full.  The code: `experiments/science/pi_inference/slack_recovery.py`, `held_site_laws.py`,
`first_order_recovery.py`, `window_model_occ.py` (and what it imports: `nested_sampler.py`, the libraries of
workstreams P3, P5, P6, P8 under `experiments/science/ws_P*/`); the logs `first_order_recovery_*.log` (fourteen);
`experiments/science/assumption_audit/aa01_essential.py`.  Workstream P9's report
(`docs/science/workstreams/P9_REPORT.md` §1: Lemma T′, Theorem R, Proposition P) is the source of the penalty
tables; it is **not** your object, except where the recovery uses it.

## Item 1 (the most important) — do the tables satisfy the hypotheses of Proposition A17.19?

The proposition needs `Σ_g S⁺_g ≤ m₊ − E` and `Σ_g S⁻_g ≤ E − m₋` pointwise, every `S ≥ 0`.  The driver's docstring gives
the accounting: `m₊ − E = far₊ + term₊ + (pen − r) + (allowances − rounding) ≥ far₊ + term₊ + (pen − envelope) = s₊`, and the
same below, with three kinds of item (a pair beyond the band; an evaluated term that fits no window; a subset
charged to a sub-tuple).  **Re-derive this accounting from the code that builds the models**
(`window_model_occ.build_window_models_occ` with `far_pairs="anchored"` and the driver's `add_pen`, `with_allowance`,
`clean`), term by term: for each kind of item, what the model contains, what the true energy contains, and why the
difference is the item's table — including: the factor `RND = 1 + 10⁻⁹` on the penalties; the `10⁻⁹` subtracted from
every item and the clipping at zero; the allowance `2^{|U|}·ε_g` attached to a term "where all sites of `U` are off the
anchor" (is the computed `d_U` exactly zero elsewhere, and is the true term?); the allocation item
`[max over the given-up sites of Θ_T](x_K) − Θ_T(x_T)` "the same item on both sides" (the penalty is added to the
ceiling and subtracted from the floor: is the same slack available on each side, or is it counted twice against
one `|r| ≤ envelope`?); a far pair's item when the occupancy-aware reduction keeps one site.  State each step as:
holds / holds with a condition to add / gap / false, with the line of code that decides it.  The numerical
evidence the coordinator has is: the hypotheses at **every** state of Lys₅ and LKSE:5 (four logs `*_enum.log`) and
at 5 380 sampled states of the larger cases, with two controls.  **Design a control the coordinator did not run**
that would catch a slack counted twice, and run it on an enumerated case (seconds to a minute:
`python3 -B first_order_recovery.py K5 4 2 --enum`; it needs `experiments/science/p9_verification/cache/`, which
exists on this machine — do not delete or rewrite it — and workstream P8's enumeration, also present).

## Item 2 — the held-site passes

`held_site_laws.py`: the claim `law(x_i = b, x_s … x_{s+w−1}) ∝ exp(F_b + B + I)` with "every term of a band model in
exactly one of the three", and the routing (`assign_routes`).  (i) Re-derive the three-way split, including a term
that touches the held site, a window that starts right after the held site, a window at the end of the chain,
sites with different numbers of states, and multi-site terms (`model.multi`).  (ii) **Test it with code that is
not the coordinator's**: random band models (random numbers of states per site, random one-site, pair and
multi-site tables within the band, `n` up to about 9 so that enumeration is exact) and random items, the five group
statistics `a, e, b, c, cp` against brute-force enumeration; you may import `nested_sampler.WindowModel` for the
model class but write the enumeration yourself.  Include items that share a window, items routed forward and on
the mirrored chain, and items that must have no route.  (iii) Can `assign_routes` give an item a window that does
not contain all its sites but the held one, or two different routes to items that the proposition then treats as
one group?  Fuzz it.  (iv) `slack_recovery.bounds`: the four formulas and the iteration against the proposition
as stated in item 69; what happens when a mean is zero, when `C′` is huge, when the iteration does not converge
in 60 steps.

## Item 3 — the regression claim and the tables of part (20)

Item 78 claims: "same items, same digits; more items, a bracket inside the old one at both ends", for thirteen runs.
The old logs are at commit `90abf0e` (`git show 90abf0e:experiments/science/pi_inference/<log>` — a read-only git
command, allowed).  Check the claim on all thirteen from the logs, and every number of the tables of items 78
and 79 and of `docs/collaboration/responses/science/SCI-RES-0024.md` §3 (a) and §4 against the logs.  Is "the
published brackets stand" justified — is a bracket that changed with the code evidence of validity, or only of
consistency?

## Item 4 — Part A of the assumption audit

(i) **The measure-space form of Proposition A17.19** (A6): is the proof complete as written — measurability,
integrability, the value `+∞` of the ceiling, a countable family of groups, `Z(E) = ∞`?  (ii) **Proposition AA.1 and
Corollary AA.2** (the envelope of a function of site-additive statistics is `M_m·e_m(δ)`): check the proof (the
convex hull, the norm of `D^mφ`, vector-valued statistics, the context `z^{T,x}` of the remainder identity); then
**try to break the corollary on a synthetic energy that is not generalised Born** — for instance
`g(x) = Σ_p φ_p(c_p + Σ_i a_{p,i}(x_i))` with several smooth `φ_p` and random `a`, small enough to enumerate every
state: the bound at every state, how tight it is, and a control that must fail (the same bound with `M_m` replaced
by the supremum of a lower derivative, or halved).  This is obligation `G-1` of the audit; if it holds, say so
with numbers, and say what the audit's sentence "the resolved table of a subset has rank one" does and does not
claim.  (iii) **Each classification of Part A** (E, T, C, Q, X, F): is the evidence next to it sufficient for the
class?  In particular: A1 "the ceiling holds on all of the space: T"; A3 "`m ≥ 3`: T / Q"; A5 "finite alphabets:
X / [?]"; A8's growth comparison ("such a floor delocalises on a long enough chain at any fixed order") — is it a
proof or a heuristic, and is it even true as stated?  (iv) **The hierarchy H0–H6**: is level H2′ (a transfer
matrix that carries `r` binned additive statistics; "width `≲ β·Lip(φ)·n·`(cell size)") right — write the statement
with its allowance properly and, if an hour allows, implement it on a toy instance against enumeration (this is
obligation `G-2`).  (v) Anything in Part A that presents a restricted result as general, or a general statement
that is computationally empty without saying so.

## Item 5 — what the certified numbers do and do not show (one paragraph)

A reader of SCI-MSG-0028 and SCI-RES-0024 sees "Lys₁₂ certified within `8·10⁻⁵` nats", "Lys₂₀ within `4·10⁻⁴`".  Say
what is certified, given what (workstream P9's tables; the evaluation tolerance `ε_g`, assumed and unproved; one
implementation of everything), and what a reader may not conclude.

## Rules

Write only in `experiments/science/ws_R19/` and `docs/science/workstreams/R19_REPORT.md`.  No state-changing git
(`git show`, `git log`, `git diff` are fine); no network; no subagents.  **Do not modify, move or delete anything
outside your directory** — in particular not the caches `experiments/science/p9_verification/cache/`,
`experiments/science/ws_P8/out/`, `ws_P8/cache/`, `ws_P9/cache/`, `ws_P9/out/`,
`experiments/science/pi_inference/serine_helix_reach_cache/`, and not the committed logs: if you re-run a
coordinator's script, redirect its output into your own directory.  Keep four kinds of checking apart and say
which you did for each statement: **review** (re-derived), **replication** (own code written from the
statements), **re-run** (the coordinator's code), **read only**.  Never fabricate; reading levels for anything
cited.  A finding is *critical*, *major* or *minor*; give a replacement text for each.  Report what you did not
check, and your own errors.  Machine: 4 cores and 15 GB shared with other jobs — `OMP_NUM_THREADS=1`, at most two
processes, no process above 4 GB (print the peak RSS in the last line of every script), no run longer than 20
minutes — and before any run of more than five minutes write into `NOTES.md` its cost per step, the number of
steps and what its result will be compared with.  Keep `NOTES.md` from the first minute.  A log is cited only if
its run reached its last line; logs of stopped or failed runs go into a subdirectory `not_cited/` and are named
in the report; use fresh names instead of overwriting a log.  A time written into a file is read from the clock
at that moment.  Before a cause is written down, the size of every candidate cause is computed.  Every check is
reported with the violations of its control.  **If a tool declines an action, do not work around it: keep
everything in `NOTES.md` and return the findings as text in your hand-back.  Do not delete files with wildcards or
`rm -r`.**  This is an internal review, not external peer review; say so in the report.

## The report

(0) Verdict in ten lines: which of the statements hold as written; the findings by class.  (1) The statements as
you understand them, with the hypotheses the texts leave implicit.  (2) Findings — critical, major, minor — each
with the line that decides it and a replacement text.  (3) Your own tests, with their controls.  (4) Re-runs and
the check of the tables.  (5) Part A of the audit: each classification, confirmed, weakened or rejected.
(6) What you did not check; your own errors; files.
