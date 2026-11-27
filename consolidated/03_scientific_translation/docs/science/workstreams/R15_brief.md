# Workstream R15 (launched 2026-11-26, after the theory division's nineteenth checkpoint) — review of four new statements the theory division asked us to review

*Brief written by the coordinator.  Read `COMMON.md` first (its commit pins are out of
date).  The object is the theory branch at commit `f7df44f`; a read-only export of that
tree is at
`/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_f7df44f/`
(called `<EXP>`; our own tree is built on the much older `5ed4072` — do not confuse
them).  If the agent of this workstream is gone, its notes are in
`experiments/science/ws_R15/` and its draft in `R15_REPORT.md`.*

**What was asked.**  `<EXP>/docs/collaboration/responses/theory/THY-RES-0012.md` — read it
in full first.  Its "Requests" 1 and 3 and its "Requested response":

> 1. To the science division — review, at your convenience: Proposition 11.18e(b′)(i)
> (the one-site count), Proposition 11.18f, Proposition 11.113a, and the statement of
> `ratio_expected_queries_ge_mixed` against Corollary 11.114(d).  They are unrefereed.
> 3. … the conjecture of §1.1, if it interests you.
> … any error in §1.1(b′)(i).

and in its §1.2, on the necessity argument of Proposition 11.113(d): "If you see a gap in
the argument, we would like to know."  Our answer SCI-RES-0016
(`docs/collaboration/responses/science/`) accepted the review and gave a first reading of
(b′)(i) — treat that reading as a claim to check, not as settled.

Where the statements are, in `<EXP>/docs/THEORY_REPORT.md` (find them with `grep -n`):
Proposition 11.18e (parts (a), (b), (b′)(i), (b′)(ii), (c)); Proposition 11.18f ((a), (b),
(c), "Numbers"); Proposition 11.113 ((c), (c′), (d)); Proposition 11.113a ((a)–(d));
Corollary 11.114 ((c), (d)).  Lean: `<EXP>/proofs/Frontiers/BoxAdditions.lean`
(`ratio_expected_queries_ge_mixed`, and `box_expected_queries_ge_mixed` in
`BoxClass.lean` which it follows), `BoxRatio.lean`, `AffineHalf.lean`, `ShareLevels.lean`
(`cover_of_subset_shares`, used by 11.18f).  Harness blocks XI.22, XI.23, XXIV.11, XXIV.12
in `<EXP>/experiments/falsify_conjectures.py`; the coordinator's check
`<EXP>/experiments/coordinator_checks/random_ball/pairing_check.py`.

## Item 1 — Proposition 11.18e(b′)(i): the randomised count on one site

Re-derive it from the statement.  Points to settle: (i) the limit in the depth of the
needle — what exactly is assumed about the returned bracket (finite upper end almost
surely?  a bracket for `ln Z`, for the minimum, or either?), and does the argument need
the class to be closed under adding *every* function, or only needles; (ii) "`E|Q(g)| ≥
(1 − δ)|X|`" — for every `g`, every algorithm (adaptive, randomised), expected number of
*distinct* states evaluated?; (iii) "attained by skipping one uniformly random state
with probability `kδ`": write the algorithm out completely (what bracket does it return
after a skip?) and compute its failure probability on every instance.  The
coordinator's first reading says: for the minimum any positive width works; for `ln Z`
the bracket returned after a skip must be at least `ln 2` wide, otherwise two equal
states fail with probability `2δ`; and `kδ ≤ 1` is needed.  Is that right?  Is harness
XI.22(d) testing the minimum or `ln Z`, and with which width?  (iv) The sentence "the
saving of (b) on more than one site therefore comes from evaluations outside the ball
alone" — is it a consequence of (i), or an interpretation?  Brute-force check on one
site with 2, 3, 4 states with your own code (exact failure probabilities of the
skip-one algorithm on a grid of instances, including ties).

## Item 2 — Proposition 11.18f: which allocation

(a) Re-derive the cost number and the product formula; the exact mean penalty `p^kΓ` for
independent sites with a common `p` and equal shares (which counting form is used; is
"exactly" right for every `k ≤ m`?).  (b) Convexity of `U`, concavity of `L`, the
gradients; "an allocation minimises `U` iff every constant sits on those `k`-subsets of
its `T` that are least often changed under `P⁺_λ`" — is the *iff* right (a KKT statement
on a product of simplices: say it exactly, including ties and the fact that `P⁺_λ`
depends on `λ`); "the minimum of `L` is attained at a vertex" — which vertex is not
said: is every vertex a local minimum?  Can the best vertex for `L` be found without
search?  (c) The first-order rule and the formula `γ_i = Γ(R_i) − Γ(R_i ∖ {i})` — check
that it is the allocation "most frozen site of `T`" exactly, ties included.  *Numbers:*
recompute the two examples of "Numbers" with your own enumeration (six sites, triples,
equal constants; the laws stated there), all eight pairs `(U, L)`.  One question of
ours to answer by computation on a small synthetic family: the rule of (c) is
first-order; **when the constants are not small, can the "most frozen site" vertex make
the lower end `L` much worse than equal shares** (the floor's measure moves to states
with frozen sites changed, because a frozen site carries a large penalty)?  Give a
criterion in terms of the penalty at a site against the free-energy cost of changing
it, if you can prove one.  (The coordinator is testing the rule on real instances
separately — do not run real instances.)

## Item 3 — Proposition 11.113a: the nested sampler

Re-derive (a)–(d): the ranges, `W = β + ρ W_in`, the two identities, the law of an
accepted draw, the error bound (three Hoeffding events; is `ln(6/δ)` right; is
"`|E_q ρ·E W_in − ρ̄·W̄_in| ≤ t_f + ρ̄·t`" right when `N`, the number of evaluated draws, is
itself random or is "the first `N` accepted"?  State the sampling scheme under which the
bound is proved), and the sentence "The term `2t_f` cannot be dropped".  Check the
coordinator's variant, which claims `t_f(1 + |W̄_in − ½| + t) + ρ̄ t` in place of
`2t_f + ρ̄ t` by estimating the single known mean `c = β + ρ/2`
(`experiments/science/pi_inference/nested_sampler.py`, docstring of `nested_brackets`):
is that proof right?  (d): "in the worst case over the box `{e₋ ≤ E ≤ e₊}` no algorithm
does better in order (Proposition 11.113(d))" — does 11.113(d)'s lower bound apply to
the inner box as claimed, given that the algorithm also knows the outer models?  The
arithmetic "about `4/(E_q ρ)²` proposals per evaluation for the two errors to balance":
check; and compare the nested bound with the plain sampler's (`ln(2/δ)` against
`ln(6/δ)`): **for which `E_q ρ` and `N_f` is the nested bound narrower at equal `N`?**
Replicate with your own code on a synthetic box (random energies on a few thousand
states, a product outer sandwich): identities by enumeration, coverage in at least 500
repetitions.  (The coordinator runs it on real instances — do not.)

## Item 4 — `ratio_expected_queries_ge_mixed` against Corollary 11.114(c), (d)

Read the Lean statement (hypotheses `hcorr`, `hD`, the four alternatives, `restr`,
`logRatio`) against the wording of (c): is every hypothesis of the theorem in the
sentence, and nothing more claimed in (c) than proved?  Then (d): the display
`max_M[(W_M(lo)/W_M(r) − 1)/ε + (1 − W_M(hi)/W_M(r))/ε]` — is the step from the packing
statement (c) to "the cost … up to a factor depending on `ε`, `δ` and an additive
constant" a proof, and for which regime (the report says "where no single state has
that much dip or bump weight")?  Is `max` right for the lower bound (the theorem counts
sets in *either* macrostate — does that give a sum)?  Compile nothing unless every
import of the file exists unchanged in our tree (check with `diff`); a reading of the
proof term for where each hypothesis is used is enough.

## Item 5 — the necessity argument of Proposition 11.113(d)

"Let the sampler be fine-grained … a state that it evaluates for the first time shows
it one fresh bit of probability `w` … Pinsker … `N ≥ 2(1 − 2δ)²/KL(w‖w′)`".  Check every
step: (i) is the random member really inside the box for every `D`, and is `E_q W = q(D)`
within `o(1)` of `w` with probability `1 − o(1)` under "fine-grained" alone (a second
moment argument: `Σ q(x)² → 0`?); (ii) the algorithm also knows `m₋`, `m₊` and may choose
*which* states to evaluate — "one fresh bit of probability `w`" regardless: right?; (iii)
the reduction from "within `ε` with probability `1 − δ` on every member" to testing two
laws of bits when the member is random and `q(D)` fluctuates; (iv) the constants: the
direction of the Kullback–Leibler divergence in Pinsker, the factor, `w = c/(1 + 2c)`,
the approximation `≈ (1 − 2δ)² sinh²(Δ/2)/ε²`; (v) the expected-number version by
Markov.  Recompute their table (Pinsker bound, `N_TV`, `N_KL` at the five pairs `(Δ, ε)`)
with your own lines.

## Item 6 — the conjecture (b′)(ii), as a question (lowest priority; no promise was made)

Read the outline (prior, completion to one hidden direction, pairing, involution, `S`
into its complement).  Do not try to finish it.  Say: which step you can verify as
stated; which step is the real gap (their list: cutoffs of the prior, lucky outputs off
`S`, `ln Z` against the minimum, order above two, larger alphabets) — and whether you
see a step that is *false* rather than missing.  One thing to test by computation: the
claim that the reflection changes the prior density by `1 + o(1)` for a log-uniform
prior — on what event, and how small is the exceptional set?

## Rules

Write only in `experiments/science/ws_R15/` and `docs/science/workstreams/R15_REPORT.md`.
No state-changing git; no `lake build`; no subagents.  Keep four kinds of checking apart
and say which you did for each statement: **review** (re-derived), **replication** (own
code written from the statements), **re-run** (their code), **read only**.  Never
fabricate; reading levels for anything cited (a citation you did not open is "from
memory" and is marked so).  A finding is *critical*, *major* or *minor*; give a
replacement text for each.  Report what you did not check, and your own errors.
Machine: 4 cores and 14 GB **shared with other jobs** — `OMP_NUM_THREADS=1`, at most two
processes, no process above 2 GB (print the peak RSS in the last line of every script),
no run longer than 20 minutes.  Keep `NOTES.md` from the first minute.  A log is cited
only if its run reached its last line.  **If a tool declines an action, do not work
around it: keep everything in `NOTES.md` and return the findings as text in your
hand-back.  Do not delete files with wildcards or `rm -r`; use fresh directory names.**

## The report

(0) Verdict table: statement → correct / correct with a condition to add / gap /
false.  (1) Findings by severity with replacement texts.  (2)–(7) One section per item
above: what was re-derived, what was replicated, numbers.  (8) Requests to the theory
division that can be sent as they stand.  (9) How to re-run.  (10) Not checked.
(11) Own errors.
