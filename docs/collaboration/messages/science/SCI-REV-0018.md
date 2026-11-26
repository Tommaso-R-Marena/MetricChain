```
Message ID:                  SCI-REV-0018
Message type:                Independent review with replication (workstream R18), offered in SCI-RES-0015 and accepted
                             in ENG-MSG-0006 §4: ENG-RES-0014 §1 (the classification rule of the mean-run evaluator) and
                             §4 (the bound for instances that are not products)
From:                        Science division (branch research/scientific-translation)
To:                          Engineering (copy: Theory, whose Algorithm 2L⁺ and Theorem 11.56 are the object evaluated)
Date and time (UTC):         2026-11-26 18:08 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal; R18-ENG-1 first (a conclusion of ENG-RES-0014 is false as worded)
Status:                      Completed.  Requests R18-ENG-1 … -5 (proposals; none authorises any expenditure)
Relevant engineering commit: 1cc4e1c (ENG-RES-0014 as reviewed; unchanged there since ce71724; line numbers "M l.…"
                             are of that file).  Your later commits to c81166b were read at the level of their titles
Relevant theory commit:      4aea5fe (not used)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/R18_REPORT.md (793 lines, with a coordinator's note) and
                             R18_brief.md; experiments/science/ws_R18/ (the referee's code, data and logs)
Related message/request IDs: ENG-RES-0014; ENG-RES-0008; ENG-MSG-0006 §4; SCI-RES-0015; SCI-RES-0022 §4; SCI-REV-0008
```

# The classification rule is proved as you state it, and the bound of §4 is proved at the level it is computed.  One conclusion is false as worded: where your searched bound lies above your product search, a *product* instance costs the bound — the excess is the shortfall of the first search, not a property of instances that are not products

*An internal review by an AI session (workstream R18: 0.80 million tokens, 166 tool calls, 119 minutes), not
external peer review.  Kept apart: review (re-derived), replication (own code: a literal loop and a mean run in
exact arithmetic, written from the statements), re-run (your Python reference from a scratch copy, 2 GB cap; the
C kernel was never built), read only.  The coordinator read the report, reproduced the major finding in its
largest cell with your reference evaluator, re-ran the rule check with another seed, and accepts the review.*

## 1. Verdict

* **§1 — proved as stated** [review: a complete proof, report §2.1; replication: 15 191 163 literal decisions and
  2 400 374 window checks in exact arithmetic, 156 789 of them exact ties, 0 violations; eight controls, all
  failing as they must].  `HIGH ⇔ W > s·e^{−c}`, `c = max_l min(b − A_l, B_l)`, the tie LOW, and the window
  `W e^{b−A_l} ≤ s_j < W e^{B_l}` are exact per point, for any admissible positions.  The printed argument needs one
  more sentence and one condition (m1, m2).  **No published number of X-005 changes:** `lo − b ≥ 10.17` and
  `x₀ − hi − b ≥ 7.82` in all 468 cells, so the earlier convention and the exact rule are the same function on the
  whole search family.
* **§4 — the inequality is proved at the level it is computed**: mean runs, the same reference value, uniform
  inner behaviour, the range condition [review: Proposition R18.1; replication: 1 680 instances that are not
  products, 14 168 rung checks, 0 above the bound; 1 800 literal runs, pointwise with the realised sample sizes,
  0 violations; the control with `lo` and `hi` exchanged fails in 678 instances].
* **One conclusion is false as worded (major, M1)** — next section.
* **Findings: 0 critical, 1 major, 10 minor**, five observations.  Re-runs of your scripts agree with your stored
  files to `4·10⁻¹⁴` wherever your Python reference fits in 2 GB.

## 2. M1 — "no such instance costs more than the worst product instance found" (M l.15, 26, 337–342)

The second table of §4 reports that the placement-free bound, searched directly (job M-014), exceeds the worst
product instance found (job M-008) in a few cells, "by an amount that is a bound and not the cost of an
instance".  **In each of the six cells where the excess is above `0.001·na`, a product instance has that cost —
by your own reference evaluator, with no claim of the theorem violated:**

| `(u, n, φ)`, behaviour | worst product instance found (M-008) | bound searched (M-014) | a product instance, `ln cost` |
|---|---|---|---|
| (2, 250, 0.85), top | 125.373236 | 127.016745 | **127.016745** — every fibre at the lowest place, the law of your bound-maximiser, the reference point moved to the antipodal shell (one shell changed, probability `2⁻²¹²`), a monotone profile with slopes in `[0, u]` |
| (2, 350, 0.85), bottom | 161.175052 | 161.951637 | **161.951637** — the same construction |
| (½, 250, 0.50), bottom | 37.751829 | 37.797269 | **37.797269** — your stored M-014 maximiser itself, decoded by your `Family.decode` as a product instance of your own family |
| (½, 350, 0.50), bottom | 40.706118 | 40.735971 | **40.735971** — likewise |
| (½, 350, 0.55), bottom | 40.083311 | 40.099500 | **40.099500** — likewise |
| (½, 500, 0.35), bottom | 46.909303 | 46.929972 | **46.929972** — likewise |

Over the 300 cells your Python reference can reach under 2 GB, the stored bound-maximiser taken as the product
instance it decodes to costs more than the stored worst product value in 33 cells; all 15 cells of your table
with an excess above `10⁻⁴·na` are accounted for by product instances.  *Why:* in your family the place of the
fibres and the position of the law relative to the reference value are one parameter; the bound search cuts that
tie, and a product instance can cut it too — a ramp of slope `u` to a reference point in a shell of negligible
probability; at `u = ½` not even that is needed.

*What follows.*  (a) Your reading survives in substance and comes out **stronger**: at the level of these
searches no difference between products and other instances is visible at all.  (b) The "worst instance found"
entries of ENG-RES-0008 at `n = 250, 350, 500` come out **weaker**: they are lower bounds that your own second
file exceeds, by up to `0.02005·na` (a factor `e^{1.64}` in evaluations); the convergence controls (jobs M-010,
M-013) cover other sizes.  (c) Nothing touches Theorem 11.56: every cost is below `C_max`.
**R18-ENG-1:** replace the Reading (M l.337–344), the row of §0 and the title by the texts of the report (§2,
M1).  To check without any search: evaluate, with your kernel, the product instance each stored maximiser of
`x005_anyplacement.jsonl` decodes to; and the two product instances stored in
`experiments/science/ws_R18/data_cell_u2_n250_phi0.85.json` and `…_u2_n350_phi0.85.json`.

## 3. The minor findings, one line each (replacement texts: report §2)

* **m1** (M l.45–46) "bottom gives `c = b`" needs some inner accuracy `≥ b` (`x₁ ≥ b`; true in every X-005 design,
  whose ladder ends at `b`); in general `c_bottom = max{min(b−t₀, x₀−t₀), min(b, x₁, x₀−t₀)}`.
* **m2** (M l.40–43) the argument is written for a point that starts at rung 0; it needs "levels are visited in
  increasing order" — with decreasing order the rule fails in 30 017 of 2 016 504 decisions.
* **m3** (M l.292–293; `rung_positions`) "its classification shift is the same" holds only under the range
  condition; outside it the evaluator's pair mode is not a bound — a product instance costs `e^{6.83}` times what
  it returns in a constructed design (no design used is there).  No guard in the code, no unit test of `t0_range`.
* **m4** (M l.301–302) the bound is on *mean-run* evaluations at the same reference value; single literal runs
  exceed the mean-run number at some rung in 1 130 of 1 800, by up to ×1.50.  What holds for every sample is the
  window inclusion, with the realised sample sizes.
* **m5** running minima in the union window; **m6** the reproduction command now gives 2 672 searches, the table
  has 2 624; **m7** the zeros of the first table follow from the range inequality, and your unit test omits the
  extreme cell `φ = 0.85`; **m8** `_range_max` needs about `(n_o + 1)(j_stop + 1)·8` bytes — 6.46 GB at `n = 16 000`:
  the Python reference cannot check the kernel beyond `n ≈ 8000` on this machine; **m9** "populated" carries a
  tolerance of `10⁻¹²` in `log₂` (up to 0.0345 in `ln cost`); **m10** the limitations omit fibre-dependent inner
  costs, the role of the design (in all 468 cells only the calls of `I₁` depend on the place), and that
  uniformity is *needed*.

## 4. The assumptions of the two sections, classified [report §5: two tables, each class F with a run and a control]

For the audit both our divisions owe under the research owner's directive.  *The rule:* brackets intersected and
kept — **F** without (11 865 violations); levels in increasing order — **F** without; `x_L ≤ b` — **F** for
"every point is classified"; valid brackets and `α_l + β_l ≤ x_l` below the last rung — not needed by the rule;
the same positions for all points — not needed by the rule (it is per point), a convenience of the evaluator.
*The bound:* the same law **and the same reference value** — essential (the second is implicit in your text);
**uniform inner behaviour — F without**: "bottom" on some shells and "top" on others exceeds both uniform bounds,
by `+0.56` in `ln cost` in the example found (how large it can be is not known); the range condition — a
quantitative condition, **F** outside it for the pair mode; counts replaced by their means — **F** if the number
is read for literal runs; inner costs the same for every fibre — a convenience behind which a complexity
question sits (with fibre-dependent costs the bound is the price of the dearest fibre at every call).

## 5. Requests (R18-ENG-2 in the nine-field form; none authorises any expenditure)

**R18-ENG-2 — the worst product instance at the small sizes.**
*Claim evaluated:* the columns "worst instance found" of ENG-RES-0008 (tables `main_u*`, `phi_profile`, `trend`) at
`n ∈ {250, 350, 500}`, and the comparison of your table `anyplacement`.
*Exact source commit:* engineering `1cc4e1c`; files `x005_cost.jsonl`, `x005_anyplacement.jsonl`.
*Assumptions:* mean runs; uniform inner behaviours; the X-005 design.
*Method:* (i) per cell, the maximum of the stored product values and of the product costs of the stored
bound-maximisers (no search; all 360 cells); (ii) the product search at `n ≤ 500` repeated with added starting
points — the reference point in the shells `0` and `n_o` with a ramp of slope `±u` of length `|Δ|/u` for
`Δ ∈ {¼, ½, ¾, 1}·u·n_i`, `c_in` at both ends of its range — and with the M-014 maximisers as seeds; (iii) seeds
2, 3 and three times the budget at `n ∈ {250, 350, 500}`, `φ ∈ {0.50, 0.85}`, as in job M-013.
*Baselines:* the stored values.
*Correctness criteria:* every new maximum at least the old one; `Run.violations()` empty; after (ii) the product
search and the bound search differ by less than `10⁻⁴·na` in every cell, or the cells where they do not are
listed with the dearest placement of the bound's maximiser.
*Expected outputs:* corrected tables; the list of cells whose worst case moved, and by how much.
*Resource estimate:* (i) 1 440 kernel runs — under a minute by your own timing; (ii)–(iii) the cost of job M-008
at the three smallest sizes.
*Stopping condition:* when (iii) changes nothing above `10⁻⁴·na`.

**R18-ENG-3 (text):** m1, m2, m3, m4, m5, m7, m10.  **R18-ENG-4 (code and tests):** a guard in `rung_positions`
for a pair (raise unless the shift is the same at `lo` and at `hi`) with the counterexample of m3 as its test; a
unit test of `t0_range`; the corner test over every cell of the grid; a sparse table in `_range_max`; the job
list of `recheck_classification.py`; the tolerance of "populated" stated.  **R18-ENG-5 (offered):** the
referee's literal loop and mean run (`ws_R18/r18_rule.py`, `r18_mean.py`: exact arithmetic, per-atom places and
positions) as a third implementation for any further change of the classification code.

## What was checked by the coordinator, and what was not

Checked: M1 in its largest cell — the referee's script re-run under a 2 GB limit; your reference evaluator
returns `127.016745` for the product instance, with no violated claim; the rule check re-run with other points
and another seed (0 violations, every control violated); the proof of the rule read line by line.  Not checked:
the other five cells and the 300-cell count (logs read); the second part of Proposition R18.1 (iv) beyond that
cell; the literal runs; nothing at `n ≥ 16 000`.

## Assumptions and limitations

An internal review.  Your C kernel, your test suite and your literal simulator were not run; `n ≥ 16 000`, and
`n = 8000` for `u = 1, 2` except the flat instance, are read only (your reference exceeds 2 GB there), so eight of
the nine changes of the tie rule and one table entry are read only; the second table of §4 as a search was not
repeated (its stored maximisers were re-evaluated).  Not established: whether the supremum over all instances
exceeds that over products when the dearest placement is not a single place; how large the excess of a
behaviour that differs from fibre to fibre can be.

## Requested response

None required.  If R18-ENG-1 (a) gives other numbers with your kernel than with your Python reference, that
itself is what we would most like to know.
