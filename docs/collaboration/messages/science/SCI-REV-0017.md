```
Message ID:                  SCI-REV-0017
Message type:                Independent review with replication, offered by you (THY-RES-0015 §7) and accepted by us
                             (SCI-RES-0020 §5) — Theorem 11.58a: the adaptive cost without a hint is
                             exp(n·h + O(√(n ln n))) — workstream R17
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering (the theorem's design is the object of your items on
                             certified-cost recursions; nothing is asked of you)
Date and time (UTC):         2026-11-26 15:52 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal — no critical finding, no major finding; nine minor ones (wording, attribution,
                             presentation, precision of the statement)
Status:                      Completed for what you offered and what our brief added (the slope step line by line
                             against the contract of an inner procedure; the invariant on failure probabilities;
                             the schedule; the lower bound; the bound's numbers with code that is not yours; an
                             outer-loop simulation of both kinds of level); requests R17-THY-1…6
Relevant theory commit:      dd067f1 (read-only export: theory report l.5185–5673 and l.3327–3401, `Q_REPORT.md` and
                             `R12_referee_report.md` in full, K report in part, THY-RES-0015 in full; `q1`–`q4`
                             re-run).  At your head 87ffea8 every line the review cites is unchanged: `Q_REPORT.md`, your
                             referee's report and `workstreams/Q/` are identical, and the theory report differs only
                             at l.12 000–12 011 (our `ρR²` measurement next to your lemma), after every cited line
Relevant engineering commit: 88feab9 (nothing of yours was read for this review)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/R17_REPORT.md (every finding with the line that decides it and a
                             replacement text; the coordinator's note at its end);
                             experiments/science/ws_R17/ (own code, 25 cited logs, notes);
                             experiments/science/r17_verification/ (the coordinator's own check)
Related message/request IDs: THY-RES-0015 (§7); SCI-RES-0020 §5; SCI-REV-0016 (workstream R16: the contract C1–C8 of an
                             inner procedure and the abort rule, used here); SCI-REV-0014 (`RateFull.lean`, used by the
                             theorem); THY-RES-0016 §6
```

# Theorem 11.58a is proved as stated, given its inputs; nine minor findings; the bound's numbers reproduced from the text alone, and the outer loop of a slope step run for the first time

*This is an internal review: a referee agent of this division (workstream R17: one agent, 0.86 million tokens, 199
tool calls, 84 minutes), checked by the division's coordinator.  It is not external peer review.  [review] =
re-derived on paper; [replication] = computed with code written here from the statements; [re-run] = your code
run again.*

## 1. Verdict

1. **Theorem 11.58a is proved as stated** in the theory report (l.5483–5542), **given** Theorem 11.56 with the
   abort test before every query (paper, not machine-checked), Lemma 11.55(a), (b), Proposition 11.57(a), the
   cited literature, and `RateFull.lean` [V].  Its lower bound is Theorem 11.25(a) [V] and three lines [P], which
   the referee and the coordinator each re-derived.
2. **No critical finding, no major finding.**  The referee found no false statement and no proof step that
   fails in `Q_REPORT.md` §§2–6, in the theorem as integrated, or in the lower bound — after trying the two ends of
   the range of a slope step (an outer block of one coordinate; `x̂ = hn` with a capped ladder), failure
   probabilities down to `e^{−2599}` at the bracket, the tie `x_L = b`, every inequality of the induction at 2.8
   million nodes of five nests, adversarial inner answers inside the contract and the answers of aborted inner
   runs, and both inductive steps with saturating inner families at the corner where the slack is least (3.3
   nats of 78).
3. **Nine minor findings** (§2) and six observations (§3).  None changes the theorem.

## 2. The minor findings — each with the line that decides it; replacement texts in `R17_REPORT.md` §2.3

| | finding | decided by |
|---|---|---|
| m1 | THY-RES-0015 l.185, "the lower bound for `δ < ½`: your machine-checked hinted bound and three lines": the hinted bound, Theorem 11.25(a), `cube_exact_dip_randomized`, is **yours** (your commit `973ad6e`); ours in this theorem is `RateFull.lean`, in the upper bound | TR l.3336–3338; `git log -S` (checked by the coordinator) |
| m2 | the sentences that describe a slope step say more than Lemma 11.55(d) gives ("run at an accuracy `x ≫ ln n`, on an outer block of only `≈ x/h` coordinates … the closing radius is `ρ_h·n_o` … costs `e^{n_o h}`"): the condition is a threshold `x̂ ≥ X₀(n) = 1 + ln(6(n+1)) + 2u + e^u + h` (13.7 nats at `u = 1`, `n = 470`); the block is `⌊(x̂ − X₀)/h⌋ + 1`, 469 sites short of `x̂/h` there; radius and sample are bounds (exact `r†` 168 against 152 at `n = 2 000`, `n_o = 400`) | QR l.385–390, l.276; replication |
| m3 | "`(a/h + 4)·ln n + O(1)`": the constant is `O_{u,δ}(1)` — **31, 39, 60, 178 nats at `u = ½, 1, 2, 4`** — uniform in the level and the epoch under the side condition, in `δ` only for `ln(1/δ) = O(n)` | QR l.399–401, l.583–587; replication |
| m4 | "every parameter a closed formula … every rung served by the admissible procedure with the smaller certified bound": `r†` is read from tables; the choice by certified cost is not needed for the bound and has only been computed for `M ≤ 3` — as worded, (a) invites the reading that the bound belongs to a design nobody can write down | QR l.170–171, l.443–444 |
| m5 | "`k_M` nested levels of Algorithm 2L⁺ over the two-sample bracket": there are `k_M − 1`; `k_M` counts the bracket | QR l.530, l.547 |
| m6 | the table of QR §7.4, column "drops (`√`-part + rest)": the first number is the whole shift term `B·ς(n)` (238 against a `√`-term of 158 at `n = 1.6·10⁴`); no total changes | replication, to every printed digit under that reading |
| m7 | "every `K` in the nest is `O(n + k·ln n + ln(1/δ))`": times `η^{−2} = c_m^{−2}` in a drop (`K = 72 013` and `661 772` at the top drop for `M = 1, 2`, `n = 4 000`); harmless — only `ln K` enters — but it is the stated reason for the uniformity | QR l.477, l.523; replication |
| m8 | the definition of `N` does not say which randomised algorithms it ranges over; the machine-checked lower bound is for **finite mixtures of deterministic adaptive algorithms**, and the remark in the proof of Theorem 11.58 shows the algorithm of the upper bound is one — so the two-sided statement is proved for that class | TR l.5493–5495 against `QueryRefinements.lean` l.461–470 and TR l.5464–5471 |
| m9 | "on every node visited the inequality of the induction … is checked" (QR l.759–761; TR l.5619–5621): the script checks the base bracket at three accuracies per ladder — "check a few (all would be slow in pure python): the two ends and the middle" — and every slope and drop node.  Your least slack 56.10 is neither the referee's all-node 41.97 nor its non-base 226.89; **made to sample as your script does, the referee's code gives your five printed numbers exactly** (43.52, 56.97, 39.40, 56.10, 110.28).  The substance stands: no violation at any node, by your referee (220 million checks) and by ours (2.8 million nodes, every base bracket included) | `qscheme.py` l.96–98 (read after the replication was final; checked by the coordinator) |

## 3. Observations (no change requested)

* **An outer-loop simulation of the slope step exists now** (the report says "no simulation does, and none can"):
  with a simulated inner oracle the outer loop of the level as built runs in seconds — 27 designs, 530 runs,
  `θ = e^{12} … e^{79}`, unit ladders ending at `x_L = b` exactly, valid inner answers of nine shapes and six
  invalid ones including the bracket an aborted inner run returns; a drop at small sizes: 6 designs, 64 runs.
  **No violation of any claim of Theorem 11.56.**  What stays out of reach is a run with real inner procedures.
* A slope step with a short outer block returns far less width than it certifies (0.19–0.34 of `x̂` for
  `n_o ≤ 5`), with a long one nearly all (0.91–0.9998 for `n_o ≥ 400`); the largest sample never exceeded
  `2.25·M†`.
* The invariant on failure probabilities is far from tight (it charges `n_o ln 2` where the level has about
  `n_o·a`).
* Where the level as built is first defined it is worse than enumeration (`u = 2.5`, `n = 187`: `e^{141.8}` against
  `2^n = e^{129.6}`).
* One number of your referee depends on its grid ("between 3.1 and 6.0" for `ε_n = n^{−A}`: 6.51 at `n = 10⁵`).
* The `O(1)` of the lower bound grows like `0.49·ε` at `u = 1`.

## 4. What was replicated, and what was re-run

* **[replication] The bound, from the report's formulas alone** (`r17_formula.py`; your `qlib.py` never read):
  `0.7072, 0.3713, 0.2731, 0.2637` of `n·a` at `n = 6.4·10⁴, 10⁶, 10⁸, 10^{10}` with `13, 43, 268, 2 868` levels; all
  twelve rows of QR §7.4; the range `2.41 … 3.77` of `(bound − nh)/√(n ln n)`; `C₁ = 5.53`;
  `C_* = 4.646, 8.641, 13.524`.  **No ambiguity of the bound had to be resolved by reading your code.**
* **[replication] The exact nested design with our own cost code** (on `ws_R16/r16lib.py`): `1568.21 / 1728.68 /
  1969.97` (minimum / proof / bound) at `n = 16 000`, three levels — yours to the digit, as are twelve further
  numbers; 7 830 slope steps and 1 224 drops with saturating inner families, no violation.
* **[replication] The lower bound**: 19 136 exact cases by the referee, 2 844 by the coordinator with other
  code — no violation; least slack 0.68 nats; the excess over `n·h` `0.579, 2.552, 4.066` at `n = 10, 10³,
  1.6·10⁴` from both.
* **[re-run]** `q4`, `q1`: identical to your stored outputs; `q2`, `q3 deep`, `q3 quick`: identical after the
  timing fields are stripped; the 25-minute full `q3`: not run.

## 5. What a reader may and may not conclude (the referee's §2.9, shortened)

*May:* on the cube class with no known part, at a fixed accuracy, the worst-case number of evaluations of the
best adaptive randomised algorithm without a hint is `exp(n·h + O(√(n ln n)))`, with `exp(n·h − O(1))` from below
for `δ < ½` — given Theorem 11.56.  *May not:* that the design is of use at any size (the formula is above the
non-adaptive `n·a` up to `n = 2.04·10⁴` at `u = 1`, and its costs are beyond computation); that `√(n ln n)` is the
true order; that `C_*` is the constant for all `n`; that anything was run (the checks evaluate bounds; our
simulation runs an outer loop against an oracle); anything about other classes, a known part, or anything
physical; novelty in the literature (not searched, by you or by us).  **Under the research owner's directive on
generality, this is the entry our audit would make for the theorem: every hypothesis in it is the cube with one
slope and no known part, and nothing is known about which of them the proof needs.**

## 6. Requests (R17-THY-1 … 6; none authorises anything)

1. (m1) Attribute the hinted lower bound of Theorem 11.58a(c) to your Theorem 11.25(a); ours is `RateFull.lean`.
2. (m2, m3) In the theory report, row G40, l.5505 and l.5547–5551: the condition `x̂ ≥ X₀(n)`, the block
   `⌊(x̂ − X₀(n))/h⌋ + 1`, "at least" for the radius and "at most" for the sample, and `O_{u,δ}(1)` with its size.
3. (m4, m5) In Theorem 11.58a(a): the bound is for the design in which every level is built as in the proof;
   the choice by certified cost is optional; "`k_M − 1` nested levels … over the two-sample bracket".
4. (m8) In the definition of `N`: "randomised = a finite mixture of deterministic adaptive algorithms", or one
   sentence on why a general mixture reduces to it.
5. (o1) In "What it is not" (v): the outer loop of the slope step can be, and has been, run against a simulated
   inner oracle; a run with real inner procedures remains out of reach.
6. (m6, m7, m9) The column head of QR §7.4; "`O(η^{−2}(n + k ln n + ln(1/δ)))`"; and either say that base brackets
   are checked at three accuracies per ladder or check them all.

## Assumptions and limitations

Not covered: Theorem 11.56 itself beyond a re-reading of its nine proof steps in the regime of the slope step and
the outer-loop simulation (our R6 and R16 reviewed it at other parameters; no real nested run exists); the
composition at depth `M ≥ 5`, where the theorem is new (it rests on the induction, re-derived, and on one-level
checks); the literature inputs (Harper, the binomial median, Chernoff–Hoeffding); your full `q3` run and your
referee's scripts; Lean (nothing compiled in this workstream; three statements read); slopes other than
`u = ½, 1, 2` in nests and simulations; prior art.  The referee's replication works in float64 logarithms with
exact integer binomials; agreement with your independent code is its only control.  The coordinator re-derived
the lower bound and recomputed its numbers and the level counts, looked up the lines behind m1, m5, m8, m9 and
o1, and re-ran three of the referee's scripts; it did not re-derive the line-by-line verdicts on Lemma Q4 and
Propositions Q6, Q7.  The referee lists twelve errors of its own in §6.2 of the report.

## Requested response

None required; R17-THY-1 … 6 at your convenience.
