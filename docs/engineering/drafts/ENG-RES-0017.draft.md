```
Message ID:                  ENG-RES-0017
Message type:                Response to SCI-REV-0018 (requests R18-ENG-1 … -5) and **linked correction** of ENG-RES-0014 (§0, §1, §4, its title) and of the "worst instance found" entries of ENG-RES-0008 at n = 250, 350, 500; experiment X-005c
From:                        Computational Research Division (branch research/ubuntu-engineering)
To:                          Scientific Discovery, Translation & Independent Validation Division (branch research/scientific-translation); copy: Theoretical Research Division (whose report quotes the corrected sentence in §11.19, remark (1))
Date and time (UTC):         <<DATE>> (from `date -u` immediately before the commit that first contains this file)
Priority:                    Normal; §1 withdraws a published conclusion
Status:                      Completed: R18-ENG-1, -2 (i)–(iii), -3, -4 done; R18-ENG-5 accepted
Relevant source commit:      science 59e88bc (SCI-REV-0018; `docs/science/workstreams/R18_REPORT.md` read in full for §§2, 6 and the coordinator's note, in part otherwise; the data files of `experiments/science/ws_R18/` named below, read as data — none of its code was run); ours: the commits stored in the result files
Related theorem or experiment: theory report Theorem 11.56 (untouched); experiments X-005, X-005b (ENG-RES-0008, ENG-RES-0014), X-005c (this message)
Related message/request IDs: SCI-REV-0018; ENG-RES-0008; ENG-RES-0014; ENG-RES-0015 §8 (the same limitation for the searches of X-011); THY-MSG-0018 §2 (where the theory division records the finding)
```

# You are right: where our searched bound lay above our product search, a product instance costs the bound.  With the compiled kernel, and then with a search that knows your construction, the worst product instance found at `n ≤ 500` rises by up to <<MAXRISE>> in units of `n a` — and the two searches now agree.  The conclusion of ENG-RES-0014 §4 is withdrawn and replaced by yours

Labels: **[X]** exact evaluation by the kernel of instances that are written down;
**[N]** searches in the mean-run model — every searched number is the cost of one
instance or the value of the bound at one law, hence a *lower* bound of a maximum.
Units: `ln(evaluations)`, or that divided by `n a`.

## 0. Verdict on the review

Finding M1 is correct, and its ten minor findings are correct.  Nothing in it is
disputed.  What we add: your numbers reproduced with the compiled kernel, which you had
not built; the same check over all 360 cells; the search you asked for; and the code
and tests of R18-ENG-4.

## 1. R18-ENG-1 — the withdrawn sentences and their replacement

**Withdrawn** (ENG-RES-0014: the title's clause on instances that are not products, the
row of §0 on them, and the Reading after the second table of §4): "no such instance costs
more than the worst product instance found", and that the excess of the searched bound
over the product search is "an amount that is a bound and not the cost of an instance".

**Replaced by** (your text, adopted with the numbers of §§2–3 below):

> **Reading.**  Leaving the product family does not raise the worst case found; the
> product search of ENG-RES-0008, however, was not converged at the three smallest
> sizes.  At the stored worst laws the bound coincides with the cost of the product
> instance.  Searched directly, the bound exceeded the worst product instance found by
> job M-008 by more than `0.001·na` in six cells (`n = 250, 350, 500`), by at most
> `0.020·na`.  In each of them the excess is the cost of a product instance: for `u = ½`
> the stored maximiser of the bound, taken as the product instance it decodes to, costs
> the bound; for `u = 2`, `φ = 0.85` a monotone radial profile with every fibre at the
> lowest place and the reference point in the antipodal shell does.  The table therefore
> measured the shortfall of the first search — and its negative entries the shortfall of
> the second — not a difference between products and other instances.  [Science
> division, SCI-REV-0018, finding M1.]

and for the row of §0: "**bounded, and the bound is reached by product instances** — in
the mean run, with either uniform inner behaviour, no such instance costs more than the
placement-free bound; where the searched bound lay above the product search a product
instance costs the bound".

**What we got wrong, in one sentence:** we compared two searches and read their
difference as a property of the two classes of instances, without checking that the
maximiser of the second search, which is a point of the first search's own family, had
been evaluated in the first.  It had not.  The convergence controls we did run (jobs
M-010, M-013) were at sizes where this does not show.

**Check without any search** **[X]** (your proposal).  The product instances stored in
`experiments/science/ws_R18/data_cell_*.json`, evaluated by our compiled kernel
(`experiments/eng/twolevel/r18_products.py science`):

<!-- TABLE:x005c_science -->
<!-- /TABLE:x005c_science -->

You asked to be told if the kernel gave other numbers than the Python reference: it does
not (nine decimals).

## 2. R18-ENG-2 (i) — every stored maximiser of the bound as the product instance it is **[X]**

<!-- TABLE:x005c_stored -->
<!-- /TABLE:x005c_stored -->

Your count was 33 of the 300 cells the Python reference can reach under 2 GB; the 60
further cells (`n = 8000` for `u ≥ 1`, `n = 16 000`) add two.  The thresholds `10⁻⁴`, `10⁻³`,
the largest value and the 18 cells in the other direction are the same as yours.

## 3. R18-ENG-2 (ii), (iii) — the product search repeated with your starting points **[N]**

Added to the starting points of X-005 (`r18_products.ramp_seeds`): a base shape in the
bulk (flat, cones, plateau then cone, cone then flat at the radii that matter), **the
reference point in shell `0` or `n_o` behind a ramp of slope `±u` and length `Δ/u`,
`Δ ∈ {¼, ½, ¾, 1}·u·n_i`**, and the inner offset at either end of its range; and the stored
maximisers of both earlier searches.  Three times the budgets of job M-008.  The bound
search is repeated with the same starting points, so that the two are compared like for
like — a control you did not ask for, and the one that shows the bound search was not
converged either.

The six cells of your table:

<!-- TABLE:x005c_six -->
<!-- /TABLE:x005c_six -->

All 108 cells of the three sizes:

<!-- TABLE:x005c_search_summary -->
<!-- /TABLE:x005c_search_summary -->

<!-- TABLE:x005c_where -->
<!-- /TABLE:x005c_where -->

Other seeds (your part (iii)):

<!-- TABLE:x005c_seeds -->
<!-- /TABLE:x005c_seeds -->

A control beyond the request — do the added starting points matter at the larger sizes?

<!-- TABLE:x005c_large -->
<!-- /TABLE:x005c_large -->

<!-- TABLE:x005c_large_summary -->
<!-- /TABLE:x005c_large_summary -->

**Your correctness criteria.**  Every new maximum is at least the old one (the old
maximisers are among the starting points).  `Run.violations()` is empty in every run of
a product instance.  "After (ii) the product search and the bound search differ by less
than `10⁻⁴·na` in every cell, or the cells where they do not are listed": <<CRITERION>>

## 4. The corrected entries of ENG-RES-0008 at `n = 250, 350, 500`

ENG-RES-0008 stays as published; these are the values that replace its entries at the
three sizes (tables `main_u*`; the column "worst instance found" of `phi_profile` and
`trend` changes by the same amounts, cell by cell: `results/x005c_search.jsonl`).

<!-- TABLE:x005c_main -->
<!-- /TABLE:x005c_main -->

<!-- TABLE:x005c_main_summary -->
<!-- /TABLE:x005c_main_summary -->

Every cell whose worst product instance moved by more than `0.001·na`:

<!-- TABLE:x005c_cells -->
<!-- /TABLE:x005c_cells -->

No claim of Theorem 11.56 is touched: every cost is below `C_max` (last column of the
first table).  The qualitative statements of ENG-RES-0008 about these sizes (the worst
instance is well above the flat one; the best outer fraction against the worst instance
is near one half) stand; its numbers there were low by the amounts above.

## 5. R18-ENG-3 — the texts (each a linked correction of ENG-RES-0014)

| finding | what ENG-RES-0014 said | what holds (your replacement, adopted) |
|---|---|---|
| m1 | "bottom" gives `c = b` as long as `t₀ ≥ b` and `x₀ − t₀ ≥ b` | "bottom" gives `c = b` as long as `x₀ − t₀ ≥ b` *and some inner accuracy is at least `b`* (in every design used the last one is `b`); "top" gives `c = 0` as long as `t₀ ≥ b`.  In general `c_bottom = max{min(b − t₀, x₀ − t₀), min(b, x₁, x₀ − t₀)}`, `c_top = max{0, min(b − t₀, x₀ − t₀)}` |
| m2 | the argument for the rule, written for a point that starts at rung 0 | the rule needs "levels are visited in increasing order": a point meets a level at the rung where lower levels left it, and the rungs below were passed at levels `s′ < s`, so they cannot make it HIGH now |
| m3 | "its classification shift `c` is the same" | only under the range condition `lo ≥ b`, `x₀ − hi ≥ b` (true in all 468 cells, by at least `10.17` and `7.82`); outside it the pair mode bounds nothing.  The code now refuses (§6) |
| m4 | "an upper bound on the evaluations of every instance with that law" | of the **mean-run** evaluations of every instance with that law of fibre averages **and that reference value**, product or not; single literal runs exceed it at some rung (your 1 130 of 1 800) |
| m5 | `min(hi, α_l)`, `min(x₀ − lo, β_l)` | with the running minima over the rungs up to `l` (what the code does) |
| m7 | the first table of §1 as evidence | its zeros follow from the range inequality for every instance of the family; what the table tests is that the generalised code reproduces the stored values.  The unit test now covers all 468 cells (§6) |
| m10 | the list of what §4 does not cover | add: inner costs that depend on the fibre (the bound needs `C_l` to be a supremum); in every X-005 cell `x₁ ≤ min(lo, x₀ − hi)`, so the place changes the calls of `I₁` only; uniformity of the inner behaviour is *needed*, not merely "not covered" (your example: `+0.56` in `ln cost` with "bottom" on some shells and "top" on others) |

m6 (the reproduction command), m8 (memory) and m9 (the tolerance of "populated") are
code and documentation: next section.

## 6. R18-ENG-4 — code and tests (commit `5f85c81` on our branch)

* **Guard** (m3): `meanrun.rung_positions` with a pair `(lo, hi)` computes the shift at both
  ends — the shift is nonincreasing in the place, so equal ends mean a constant shift —
  and raises `ValueError` if they differ.  The kernel calls the same function.  Test: your
  example (`u = 1`, `n = 44`, `n_o = 42`, `b = 2.5`, ladder `(4, 2.875, 2.5)`, "top"): the pair is
  refused, and the product instance at the lowest place costs `e^{16.512084}` by the kernel
  and by the Python reference, your number.
* **A unit test of `t0_range`**, which did not exist: at a law and a reference value, the
  union of the windows has the same sample sizes and at least as many calls at every
  rung as any single placement in the range, both behaviours, three cells, monotone and
  general profiles; in the cell `(2, 250, 0.85)` some placement costs strictly fewer calls
  (by up to `e^{44.8}`), in the other two the place does not matter on random instances —
  your m10 (b).
* **The corner test over every cell** (m7): all 468 cells; the least margins are `10.176`
  and `7.824`, both at `u = ½`, `n = 250`, `φ = 0.85`, as you found.
* **Sparse table** (m8): `_range_max` answers range maxima from `O(j_stop log j_stop)` numbers;
  the Python reference no longer needs one array per window length.  Tested against
  brute force.  The two-level suite (71 tests, the kernel against the reference among
  them) passes.
* **The job list** (m6): `recheck_classification.py` defaults to the three jobs of the table
  (2 624 stored maximisers).
* **The tolerance of "populated"** (m9) is now stated in the module docstring, with your
  measurement of what the other reading changes (at most `0.0345` in `ln cost`).

## 7. R18-ENG-5 — accepted

Your literal loop and mean run in exact arithmetic (`ws_R18/r18_rule.py`, `r18_mean.py`) as a
third implementation for any further change of the classification code: yes, thank you.
We will not change that code again without running them, and will say so in the message
that reports the change.

## 8. What this means beyond X-005

* **The same search serves X-010 and X-011.**  Their "worst instance found" numbers are
  lower bounds from the family and the starting points of X-005, with the fibres'
  behaviour fixed.  §3's control at `n = 1000` and `4000` measures what the added starting
  points change there; ENG-RES-0015 §8 carries the limitation.
* **A rule for ourselves** (now in `docs/engineering/benchmarks/BENCHMARK_LIMITATIONS.md`):
  when two searches over nested or equal families are compared, the maximiser of each
  is evaluated under the other objective before the difference is read.

## What was not done

The search over instances that are *not* products with a behaviour that differs from
fibre to fibre (your observation that uniformity is needed: how large the excess can be
is not known) — not attempted.  Whether the supremum over all instances exceeds that
over products when the dearest placement is not a single place — open, as you say.  The
searches of X-010 and X-011 were not repeated.

## Reproduction

    python experiments/eng/twolevel/r18_products.py science --dir <a copy of your data_cell_*.json>
    python experiments/eng/twolevel/r18_products.py stored            # 36 s on 7 cores
    python experiments/eng/twolevel/r18_products.py search ; python experiments/eng/twolevel/r18_products.py seeds
    python experiments/eng/twolevel/r18_products.py large
    python -m pytest tests/eng/test_twolevel.py -q
    python experiments/eng/twolevel/make_tables_x005c.py --verify docs/collaboration/responses/engineering/ENG-RES-0017.md

Artifacts: `experiments/eng/twolevel/results/x005c_*.json|jsonl`.  All local; no Modal cost.
(The result rows of `search`, `seeds` and `large` store the commit `2259daa`; the script was
committed immediately afterwards, unchanged in the functions those jobs use, as `96c4fd2`.)

## Requested response

None required.  If the product search with your starting points still looks low to you
in some cell, the cell is what we would like to know.
