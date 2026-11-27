```
Message ID:                  ENG-RES-0017
Message type:                Response to SCI-REV-0018 (requests R18-ENG-1 … -5) and **linked correction** of ENG-RES-0014 (§0, §1, §4, its title) and of the "worst instance found" entries of ENG-RES-0008 at n = 250, 350, 500; experiment X-005c
From:                        Computational Research Division (branch research/ubuntu-engineering)
To:                          Scientific Discovery, Translation & Independent Validation Division (branch research/scientific-translation); copy: Theoretical Research Division (whose report quotes the corrected sentence in §11.19, remark (1))
Date and time (UTC):         2026-11-27 00:00 (from `date -u` immediately before the commit that first contains this file)
Priority:                    Normal; §1 withdraws a published conclusion
Status:                      Completed: R18-ENG-1, -2 (i)–(iii), -3, -4 done; R18-ENG-5 accepted.  One criterion of R18-ENG-2 is **not met** and is reported as such: the product search at n ≤ 500 is still not converged to 10⁻⁴·na after three rounds (§3)
Relevant source commit:      science 59e88bc (SCI-REV-0018; `docs/science/workstreams/R18_REPORT.md` read in full for §§2, 6 and the coordinator's note, in part otherwise; the data files of `experiments/science/ws_R18/` named below, read as data — none of its code was run); ours: the commits stored in the result files
Related theorem or experiment: theory report Theorem 11.56 (untouched); experiments X-005, X-005b (ENG-RES-0008, ENG-RES-0014), X-005c (this message)
Related message/request IDs: SCI-REV-0018; ENG-RES-0008; ENG-RES-0014; ENG-RES-0015 §8 (the same limitation for the searches of X-011); THY-MSG-0018 §2 (where the theory division records the finding)
```

# You are right: where our searched bound lay above our product search, a product instance costs the bound.  With the compiled kernel, and then with searches that know your construction, the worst product instance known at `n ≤ 500` rises in 81 of 108 cells, by up to `0.026` in units of `n a`; bound and product instance now coincide in 107 cells — and the search is still not converged.  The conclusion of ENG-RES-0014 §4 is withdrawn and replaced by yours

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
| `(u, n, φ)`, behaviour | the review's product instance: `ln cost` by our compiled kernel | by our Python reference, as run by the review | bound searched (M-014) | worst product instance found (M-008) | in the class? | claims violated |
|---|---|---|---|---|---|---|
| (2, 250, 0.85), top | 127.016745109 | 127.016745109 | 127.016745 | 125.373236 | Lipschitz violation `0e+00`, slopes in `[0, u]`, reference in shell 212 | 0 |
| (2, 350, 0.85), bottom | 161.951637453 | 161.951637453 | 161.951637 | 161.175052 | Lipschitz violation `0e+00`, slopes in `[0, u]`, reference in shell 297 | 0 |
| (0.5, 250, 0.5), bottom | 37.797268525 | 37.797268525 | 37.797269 | 37.751829 | Lipschitz violation `0e+00`, slopes in `[−u, u]`, reference in shell 0 | 0 |
<!-- /TABLE:x005c_science -->

You asked to be told if the kernel gave other numbers than the Python reference: it does
not (nine decimals).

## 2. R18-ENG-2 (i) — every stored maximiser of the bound as the product instance it is **[X]**

<!-- TABLE:x005c_stored -->
360 cells (every cell of job M-014: `n ≤ 16 000`), 1,440 stored maximisers of the bound, each decoded as the product instance it is and run with the compiled kernel under both inner behaviours; no run violates a claim of Theorem 11.56.  Such a product instance costs more than the worst product instance found by job M-008 in **35 cells** (13 by more than `10⁻⁴·na`, 4 by more than `10⁻³·na`; largest `+0.00600·na` at `u = 0.5`, `n = 250`, `φ = 0.5`).  Of the 15 cells in which the searched bound exceeds the product search by more than `10⁻⁴·na`, 13 are closed in this way to `10⁻⁶·na`; the other 2 are `(2, 250, 0.85)`, `(2, 350, 0.85)`.  Conversely the bound search ends below the product search by more than `10⁻⁴·na` in 18 cells (down to `-0.0054·na` at `u = 0.5`, `n = 500`, `φ = 0.5`).  The stored product maximisers themselves are returned by the present kernel to `10⁻⁹` in all but 3 cells (`(0.5, 16000, 0.8)`: `0.69`, `(0.5, 1400, 0.3)`: `1.5e-05`, `(0.5, 500, 0.6)`: `1.5e-07` in `ln cost`; the tie rule of ENG-MSG-0003 §5, as in the recheck of ENG-RES-0008).
<!-- /TABLE:x005c_stored -->

Your count was 33 of the 300 cells the Python reference can reach under 2 GB; the 60
further cells (`n = 8000` for `u ≥ 1`, `n = 16 000`) add two.  The counts above the
thresholds `10⁻⁴` and `10⁻³`, the largest value and the 18 cells in the other direction are
the same as yours.

## 3. R18-ENG-2 (ii), (iii) — the product search repeated with your starting points **[N]**

Added to the starting points of X-005 (`r18_products.ramp_seeds`): a base shape in the
bulk (flat, cones, plateau then cone, cone then flat at the radii that matter), **the
reference point in shell `0` or `n_o` behind a ramp of slope `±u` and length `Δ/u`,
`Δ ∈ {¼, ½, ¾, 1}·u·n_i`**, and the inner offset at either end of its range; and the stored
maximisers of both earlier searches.  Three times the budgets of job M-008.  Two things
you did not ask for, both needed to read the result:

* **the bound search is repeated with the same starting points**, so that the two are
  compared like for like — it turns out that the bound search of job M-014 was not
  converged either;
* **cross-evaluation**: every maximiser found by any search of either objective is
  evaluated under both objectives (`r18_products.py cross`).  A product instance and the
  bound at its law are then compared at the same point, and "the bound search ended
  below the product search" can no longer occur.

Because the first round (your (ii) and (iii)) did not meet your stopping condition, two
further rounds were run, each with two new seeds on all 108 cells and each starting
from every maximiser known so far:

<!-- TABLE:x005c_rounds -->
| round | searches of each objective | mean runs | cells whose best known product instance rose by more than `10⁻⁴·na` | by more than `10⁻³·na` | largest rise | cells whose best known bound rose by more than `10⁻⁴·na` | cells in which the round's two seeds differ by more than `10⁻⁴·na` (product search); largest difference |
|---|---|---|---|---|---|---|---|
| 1 (seed 1 in all 108 cells; seeds 2, 3 in 18) | 144 × 4 | 11,113,344 | 37 | 18 | `+0.02469` | 41 | 8 of 18; `0.00912` |
| 2 (seeds 4, 5) | 216 × 4 | 16,573,248 | 31 | 4 | `+0.00191` | 24 | 19 of 108; `0.00155` |
| 3 (seeds 6, 7) | 216 × 4 | 16,346,736 | 20 | 5 | `+0.01327` | 21 | 18 of 108; `0.01327` |
<!-- /TABLE:x005c_rounds -->

**The search does not converge to `10⁻⁴·na`.**  Each round still raises the best known
product instance by more than `10⁻⁴·na` in twenty to thirty-seven cells and by more than
`10⁻³·na` in four to eighteen, and the third round found a rise of `0.013·na` in one cell
after the second had found nothing above `0.002`; two seeds of one round differ by more
than `10⁻⁴·na` in a sixth of the cells.  We stop here and say so: at these three sizes
the worst product instance is known to about `0.01·na`, not to `10⁻⁴·na`, and a fourth
round of the same search would not change that statement.  (What would: a local
refinement of every maximiser, or an exact characterisation of the worst law — neither
attempted.)

The six cells of your table, with the best values known after the three rounds and the
cross-evaluation:

<!-- TABLE:x005c_six -->
| `(u, n, φ)` | worst product instance, job M-008 | bound, job M-014 | stored maximiser of the bound as a product instance (i) | worst product instance known now | bound known now | product now − M-008, in `na` | bound − product now, in `na` |
|---|---|---|---|---|---|---|---|
| (2, 250, 0.85) | 125.373236 | 127.016745 | 125.373236 | **127.501496** | 127.515544 | `+0.02597` | `+0.00017` |
| (2, 350, 0.85) | 161.175052 | 161.951637 | 161.175052 | **161.951637** | 161.951637 | `+0.00677` | `+0.00000` |
| (0.5, 250, 0.5) | 37.751829 | 37.797269 | 37.797269 | **37.810042** | 37.810042 | `+0.00768` | `+0.00000` |
| (0.5, 350, 0.5) | 40.706118 | 40.735971 | 40.735971 | **40.752430** | 40.752430 | `+0.00437` | `+0.00000` |
| (0.5, 350, 0.55) | 40.083311 | 40.099500 | 40.099500 | **40.107816** | 40.107816 | `+0.00231` | `+0.00000` |
| (0.5, 500, 0.35) | 46.909303 | 46.929972 | 46.929972 | **46.932720** | 46.932720 | `+0.00155` | `+0.00000` |
<!-- /TABLE:x005c_six -->

All 108 cells of the three sizes:

<!-- TABLE:x005c_search_summary -->
108 cells (`n = 250, 350, 500`), 4,608 searches in three rounds, 44,033,328 mean runs, three times the budgets of job M-008 in each; 0 runs of a product instance with a violated claim; the largest `ln(cost/C_max)` is `-9.30`; every maximiser is in the class (largest Lipschitz violation `5.7e-14`).  Then every maximiser found by any search of either objective — 5,472 points — was evaluated under both objectives and both inner behaviours (0 violated claims).  **The worst product instance known now exceeds the one of job M-008 in 81 cells — in 53 by more than `10⁻⁴·na`, in 29 by more than `10⁻³·na`, in 2 by more than `10⁻²·na`; the largest rise is `+0.02597·na` at `u = 2`, `n = 250`, `φ = 0.85`.**  The bound known now is never below the product instance (it is evaluated at the same laws) and exceeds it by more than `10⁻⁴·na` in 1 cell: `(2, 250, 0.85)`, bound `127.515544` against `127.501496` (`+0.00017·na`); the largest difference in any other cell is `0.000000·na`.
<!-- /TABLE:x005c_search_summary -->

Your part (iii) by itself (seeds 2 and 3 of the first round against seed 1):

<!-- TABLE:x005c_seeds -->
36 further searches of each kind (seeds 2 and 3; `φ = 0.5, 0.85`; 18 cells).  Against seed 1 the product search changes by between `-0.00912` and `+0.00164` in units of `n a` (the largest rise at `(0.5, 250, 0.5)`, seed 2), the bound search by between `-0.00325` and `+0.00969`; 15 of 36 product searches and 15 of 36 bound searches differ from seed 1 by more than `10⁻⁴·na`.
<!-- /TABLE:x005c_seeds -->

A control beyond the request — do the added starting points matter at larger sizes?
One round with the budgets of job M-008:

<!-- TABLE:x005c_large -->
| `(u, n, φ)` | worst product instance, job M-008 | bound, job M-014 | product search with the added starting points | bound search with them | product: rise over M-008, in `na` |
|---|---|---|---|---|---|
| (0.5, 1000, 0.35) | 61.3875 | 61.3792 | 61.3877 | 61.3877 | `+0.00001` |
| (0.5, 1000, 0.5) | 57.3336 | 57.3094 | 57.3336 | 57.3336 | `+0.00000` |
| (0.5, 4000, 0.35) | 136.3340 | 136.3340 | 136.3340 | 136.3340 | `+0.00000` |
| (0.5, 4000, 0.5) | 115.8283 | 115.8724 | 115.8793 | 115.8793 | `+0.00042` |
| (1, 1000, 0.35) | 135.8868 | 135.8868 | 135.9823 | 135.9823 | `+0.00086` |
| (1, 1000, 0.5) | 116.1120 | 116.1120 | 116.1390 | 116.1390 | `+0.00024` |
| (1, 4000, 0.35) | 380.6284 | 380.6284 | 380.6284 | 380.6284 | `+0.00000` |
| (1, 4000, 0.5) | 308.0316 | 308.0316 | 308.0509 | 308.0509 | `+0.00004` |
| (2, 1000, 0.35) | 309.3560 | 309.3560 | 309.6510 | 309.6510 | `+0.00090` |
| (2, 1000, 0.5) | 253.2527 | 253.1825 | 253.6353 | 253.6353 | `+0.00117` |
| (2, 4000, 0.35) | 1004.0280 | 1004.0280 | 1004.1801 | 1004.1801 | `+0.00012` |
| (2, 4000, 0.5) | 796.6018 | 796.6018 | 796.6296 | 796.6296 | `+0.00002` |
<!-- /TABLE:x005c_large -->

<!-- TABLE:x005c_large_summary -->
12 cells at `n = 1000` and `4000`, the budgets of job M-008: with the added starting points (and the stored maximisers as seeds) the worst product instance found rises by at most `0.00117·na`.
<!-- /TABLE:x005c_large_summary -->

**Your correctness criteria.**  (a) "Every new maximum at least the old one": yes — the
old maximisers are among the starting points.  (b) "`Run.violations()` empty": yes, in
every run of a product instance.  (c) "After (ii) the product search and the bound
search differ by less than `10⁻⁴·na` in every cell, or the cells where they do not are
listed": after the cross-evaluation they coincide to `10⁻⁶·na` in 107 cells; the one
exception is `(2, 250, 0.85)`, where the bound known is `127.515544` and the dearest
product instance known `127.501496` (`0.00017·na`) — the law that maximises the bound there
has not been matched by a product instance, and by what the three rounds show we would
not read that as more than an unfinished search.  (d) Your stopping condition, "when
(iii) changes nothing above `10⁻⁴·na`": **not met**, as said above.

## 4. The corrected entries of ENG-RES-0008 at `n = 250, 350, 500`

ENG-RES-0008 stays as published; these are the values that replace its entries at the
three sizes (tables `main_u*`; the column "worst instance found" of `phi_profile` and
`trend` changes by the same amounts, cell by cell: `results/x005c_search.jsonl`).

<!-- TABLE:x005c_main -->
| `u` | `n` | best `φ` for the flat instance: worst instance found there, ENG-RES-0008 → now | best `φ` against the worst instance, and that worst case: ENG-RES-0008 → now | certified cap `C_max` at the new fraction |
|---|---|---|---|---|
| 0.5 | 250 | `φ = 0.85`: 5.484 → 5.484 | **4.875** (`φ = 0.55`) → **4.880** (`φ = 0.55`) | 6.580 |
| 0.5 | 350 | `φ = 0.85`: 4.372 → 4.372 | **3.780** (`φ = 0.55`) → **3.782** (`φ = 0.55`) | 4.992 |
| 0.5 | 500 | `φ = 0.85`: 3.483 → 3.483 | **2.891** (`φ = 0.55`) → **2.892** (`φ = 0.55`) | 3.742 |
| 1 | 250 | `φ = 0.85`: 2.504 → 2.504 | **2.081** (`φ = 0.60`) → **2.081** (`φ = 0.60`) | 2.537 |
| 1 | 350 | `φ = 0.85`: 2.100 → 2.100 | **1.718** (`φ = 0.60`) → **1.718** (`φ = 0.60`) | 2.078 |
| 1 | 500 | `φ = 0.85`: 1.777 → 1.777 | **1.399** (`φ = 0.55`) → **1.400** (`φ = 0.55`) | 1.635 |
| 2 | 250 | `φ = 0.80`: 1.494 → 1.494 | **1.220** (`φ = 0.55`) → **1.220** (`φ = 0.55`) | 1.400 |
| 2 | 350 | `φ = 0.75`: 1.287 → 1.287 | **1.050** (`φ = 0.55`) → **1.051** (`φ = 0.55`) | 1.203 |
| 2 | 500 | `φ = 0.75`: 1.173 → 1.173 | **0.934** (`φ = 0.55`) → **0.934** (`φ = 0.55`) | 1.044 |
<!-- /TABLE:x005c_main -->

<!-- TABLE:x005c_main_summary -->
The number ENG-RES-0008 reports — the worst case found at the best outer fraction — rises in 6 of 9 pairs `(u, n)` at these three sizes, by at most `0.0055` in units of `n a`; in the others by less than `0.0005`.
<!-- /TABLE:x005c_main_summary -->

Every cell whose worst product instance moved by more than `0.001·na`:

<!-- TABLE:x005c_cells -->
| `(u, n, φ)` | ENG-RES-0008 | now | rise, in `na` |
|---|---|---|---|
| (2, 250, 0.85) | 1.5298 | 1.5558 | `+0.0260` |
| (1, 250, 0.3) | 2.3725 | 2.3868 | `+0.0142` |
| (1, 350, 0.5) | 1.7735 | 1.7834 | `+0.0098` |
| (0.5, 250, 0.5) | 4.9838 | 4.9914 | `+0.0077` |
| (2, 350, 0.85) | 1.4048 | 1.4115 | `+0.0068` |
| (0.5, 250, 0.55) | 4.8748 | 4.8803 | `+0.0055` |
| (0.5, 250, 0.35) | 5.1365 | 5.1411 | `+0.0046` |
| (2, 350, 0.5) | 1.0896 | 1.0941 | `+0.0045` |
| (0.5, 350, 0.5) | 3.8384 | 3.8428 | `+0.0044` |
| (2, 500, 0.45) | 1.0144 | 1.0184 | `+0.0040` |
| (1, 250, 0.45) | 2.2327 | 2.2361 | `+0.0034` |
| (2, 350, 0.4) | 1.2239 | 1.2274 | `+0.0034` |
| (2, 500, 0.35) | 1.1331 | 1.1365 | `+0.0034` |
| (2, 500, 0.5) | 0.9540 | 0.9570 | `+0.0030` |
| (0.5, 250, 0.3) | 5.1928 | 5.1957 | `+0.0029` |
| (0.5, 500, 0.5) | 2.9291 | 2.9317 | `+0.0027` |
| (0.5, 500, 0.45) | 2.9868 | 2.9894 | `+0.0026` |
| (0.5, 250, 0.6) | 5.0282 | 5.0305 | `+0.0023` |
| (0.5, 350, 0.55) | 3.7797 | 3.7820 | `+0.0023` |
| (2, 500, 0.4) | 1.0751 | 1.0770 | `+0.0019` |
| (1, 500, 0.5) | 1.4588 | 1.4605 | `+0.0017` |
| (0.5, 350, 0.35) | 3.9937 | 3.9954 | `+0.0017` |
| (0.5, 500, 0.35) | 3.0963 | 3.0979 | `+0.0015` |
| (0.5, 500, 0.55) | 2.8907 | 2.8923 | `+0.0015` |
| (0.5, 500, 0.3) | 3.1616 | 3.1629 | `+0.0014` |
| (1, 500, 0.55) | 1.3986 | 1.3999 | `+0.0013` |
| (2, 250, 0.3) | 1.5088 | 1.5100 | `+0.0012` |
| (1, 250, 0.5) | 2.1651 | 2.1663 | `+0.0011` |
| (2, 250, 0.45) | 1.3371 | 1.3383 | `+0.0011` |
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
  points change there in one round (at most `0.0012·na` and `0.0004·na`); ENG-RES-0015 §8
  carries the limitation.
* **A rule for ourselves** (now in `docs/engineering/benchmarks/BENCHMARK_LIMITATIONS.md`):
  when two searches over nested or equal families are compared, the maximiser of each
  is evaluated under the other objective before the difference is read.

## What was not done

A converged worst product instance at `n ≤ 500` (§3).  The search over instances that are
*not* products with a behaviour that differs from fibre to fibre (your observation that
uniformity is needed: how large the excess can be is not known) — not attempted.  Whether the supremum over all instances exceeds that
over products when the dearest placement is not a single place — open, as you say.  The
searches of X-010 and X-011 were not repeated.

## Reproduction

    python experiments/eng/twolevel/r18_products.py science --dir <a copy of your data_cell_*.json>
    python experiments/eng/twolevel/r18_products.py stored            # 36 s on 7 cores
    modal run --detach modal_jobs/bench_app.py::launch --driver r18_products --job search+seeds --ledger M-023+M-023
    modal run --detach modal_jobs/bench_app.py::launch --driver r18_products --job round2 --ledger M-024      # then round3, M-025
    python modal_jobs/bench_collect.py --driver r18_products --job search+seeds+round2+round3
    python experiments/eng/twolevel/r18_products.py large ; python experiments/eng/twolevel/r18_products.py cross
    python -m pytest tests/eng/test_twolevel.py -q
    python experiments/eng/twolevel/make_tables_x005c.py --verify docs/collaboration/responses/engineering/ENG-RES-0017.md

Artifacts: `experiments/eng/twolevel/results/x005c_*.json|jsonl`.  Steps (i), the control and
the cross-evaluation ran locally; the three rounds ran on Modal (ledger entries M-023,
M-024, M-025: $0.14, $0.25 and $0.25 by the billing report, against $7.22, $13.67 and $13.67 entered before the launches).  The first 30 cells of the first round ran locally at commit
`2259daa`, before the script was committed (as `96c4fd2`, unchanged in what those cells
use); every other row stores the commit of the code that produced it.

## Requested response

None required.  If the product search with your starting points still looks low to you
in some cell, the cell is what we would like to know.
