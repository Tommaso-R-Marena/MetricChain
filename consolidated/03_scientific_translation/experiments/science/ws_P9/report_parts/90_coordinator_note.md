## Coordinator's note (2026-11-26, after the hand-back; everything above is the workstream's text, unchanged)

*Who writes here.*  The report above is workstream P9's.  I am the coordinator of the division.
Before publishing it (SCI-MSG-0028) I read it in full, went through §1 on paper, and checked
what is listed below with code that is not P9's (`experiments/science/p9_verification/`, every
log there ends with `ALL DONE`).  "Checked" never means refereed: **nothing in this report has
been read by an independent referee, and nothing in it is machine-checked.**

**N1.  The statements (§1) — re-derived, no gap found.**  Lemma T′ is P3's theorem with the
increments it is stated with; Theorem R is P8's Theorem AH with its last step left out — the
one point to verify is that a host `l ∉ T` sits at the anchor in the context `z^{T,x}`, and it
does: with the hosts last in the order, `T` (at least three sites, at most two hosts) has a
non-host element, which precedes `l`.  Proposition P stands on the two sentences its proof
prints in bold: the actual `x_T` is among the points of the maximum that defines `c_{T,U}(x_U)`,
and a table that is charged although `T ⊄ S(x)` only adds a non-negative term.

**N2.  The raw tables `Θ²_T` against exact remainders (my left sides, my states, my controls).**

| instance, order | what was compared | states | violations | smallest bound / exact | controls that must fail (violations) |
|---|---|---|---|---|---|
| Lys₄, Lys₅, LKSE:5, every order 3…n | `R ≤ B₂ ≤ B₁ ≤ B_SAb` at every state (`resolved_enum_check.py`) | 15 743 – 114 263 per row | 0 in all eight rows | 8.46 – 30.2 (Boltzmann mean of `B₂/R`: 255 – 880) | minimum in place of the value: 877 – 68 427; table reversed: 2 – 2 703 |
| Lys₁₂, 3 | every state with exactly 3 side chains off: exact anchored term against `Θ²_T(x_T)` (`resolved_check12.py`) | 92 525 | 0 | 9.02 | 14 334; 438 |
| Lys₁₂, 4 | the same with 4 | 1 524 690 | 0 | 8.25 | 630 395; 18 972 |
| (LKSE)₃, 3 | the same with 3 | 175 185 | 0 | 15.05 | 42 045; 2 819 |
| (LKSE)₃, 4 | the same with 4 | 3 290 515 | 0 | 8.26 | 1 853 296; 170 176 |
| Lys₁₂, (LKSE)₃, Ser₁₂, 5 | no ball of radius 5 exists: 2 000 uniformly random states each, and the Gibbs states with five or more side chains off | 2 000 + 0, 116, 812 | 0 | 17.7, 23.3, 8.9 | table reversed: 15, 20, 3 (weak) |

At order 5 the check is a necessary condition at states far from the ensemble; the per-entry
check that exists at orders 3 and 4 does not exist there.

**N3.  From the raw tables to the brackets, with a driver of mine (P9's request P9-E1, done:
`resolved_brackets.py`).**  The window-form tables and the triple sums, re-built from the raw
tables with my code, equal P9's stored ones entry for entry (largest deviation `0.0`) in all six
cases; "envelope ≤ tables" holds at 32 000 – 40 000 random states per case with **equality**
where the envelope is a single entry (window form), and fails with the minimum in place of the
maximum (15 393 – 27 020 violations) and with every twentieth table removed (119 – 10 560).
The brackets, digit for digit those of §4 and §5:

| instance, order (ball) | window form W | equal shares on triples T |
|---|---|---|
| Lys₁₂, 3 (3 841) | `[517.108870, 517.185731]` 0.07686 | `[516.827371, 517.659419]` 0.832 |
| Lys₁₂, 4 (96 366) | `[517.125649, 517.132996]` 0.007347 | `[517.075039, 517.186576]` 0.1115 |
| Lys₁₂, 5 (1 621 056) | `[517.125705, 517.132938]` 0.007233 | `[517.121336, 517.137333]` 0.016 |
| (LKSE)₃, 4 (181 268) | `[655.603013, 655.622116]` 0.0191 | `[655.203848, 656.350724]` 1.147 |
| (LKSE)₃, 5 (3 471 783) | `[655.604050, 655.621038]` 0.01699 | `[655.520038, 655.714657]` 0.1946 |
| Ser₁₂, 5 (481 506) | `[227.363089, 227.374782]` 0.01169 | `[227.357675, 227.380236]` 0.02256 |

The sandwich `m₋ ≤ E ≤ m₊` at 6 980 states of mine per case and form (Gibbs states of my seed,
exact samples of the floor **and of the ceiling**, uniformly random states, states with exactly
`m` and `m + 1` side chains off; new evaluations of the energy): no violation.  **How much that
last check can see** — the same states with the tables left out: 829 and 929 violations (Lys₁₂,
order 3), 18 (order 4), 92 ((LKSE)₃, order 4), and **none** for Lys₁₂ and (LKSE)₃ at order 5 and
for Ser₁₂; with tables a hundred times smaller 207, 4, 3 (window form) and never with tables ten
times smaller.  A table too small by a factor ten would pass the sandwich check at my states;
it would not pass N2.

**N4.  Not checked by me.**  The stage-1 tables (only stage 2 was compared with exact terms and
re-built); the forms S and B; the rows "joint maxima of stage 2 as constants" and "P8's
constants, my chains"; (LKSE)₃ at order 3 (no certificate there anyway); the gain tables of §3;
P3's interval enclosures and hulls, inherited by every certificate of the division.
*The sampler (§5.4).*  Run (B) — (LKSE)₃ from the order-4 ball — was repeated with a driver of
mine and another seed (`p9_verification/nested_resolved.py`, seed 2026113740 where the workstream
had 2026112740): as the theory division states the bound `[655.612563, 655.612815]` (above:
`[655.612562, 655.612814]`); two-end form with empirical Bernstein `[655.612658, 655.612720]`
(above: `[655.612657, 655.612719]`); 15 392 of 400 000 proposals accepted, 1 200 evaluated, none
outside either sandwich.  Run (A) was not repeated.  Run (C), which the workstream could not
make for memory, is in addendum A17 (19).

**N5.  What "certified" means in this report.**  A bracket of §4–§5 is the output of exact
transfer matrices on two models whose validity rests on a chain of paper proofs: P3's theorem
(workstream P3; its corollaries re-derived by workstreams P8 and P9, its bound tested on every
triple and four-body term that was enumerated; no independent referee), P8's Theorem AH
(re-derived and tested by me, not refereed), Theorem R and Proposition P above (N1; not
refereed), and on one implementation
of the stage-2 evaluation, tied to exact four-body and three-body terms by N2.  It is relative
to the GBn2 model function on rigid synthetic peptides.

**N6.  What is in the repository.**  Scripts, `NOTES.md`, the report parts, 60 logs (each ends
with `ALL DONE`) and 22 screen captures of chained runs (`logs/*.stdout`, not cited), the JSON
records, and `not_cited/` — 13 logs of failed or superseded runs,
kept under that name as the brief prescribed and named in §7; none of them is evidence.  **Not**
in the repository: `cache/` (0.52 GB) and `out/*.npz` (0.64 GB), regenerable arrays; the commands
are in §7 (`p9_03_tables.py … --keeptabs` writes the raw tables that my verification scripts
and the sampler driver read: 87 s and 378 s for Lys₁₂ at orders 4 and 5, twice four minutes
for (LKSE)₃ at order 5).

**N7.  What followed.**  The report's last line — the brackets are now the reductions of the
band, untouched — is where the coordinator went next: the slack of a reduction is a known
table, and a Gibbs–Bogoliubov argument with exact marginals of the ceiling model takes it
out of the bracket.  That is addendum A17 (19) of `docs/science/INFERENCE_LIMITS_ADDENDA.md`
(`pi_inference/slack_recovery.py`, `first_order_recovery.py`), not part of this workstream.
