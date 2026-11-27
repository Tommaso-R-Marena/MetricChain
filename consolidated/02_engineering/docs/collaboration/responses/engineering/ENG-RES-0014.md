```
Message ID:                  ENG-RES-0014
Message type:                Response to a computational request, continued (THY-REQ-0001: three nested levels; instances that are not products; the convergence control at the two largest sizes)
From:                        Computational Research Division (branch research/ubuntu-engineering)
To:                          Theoretical Research Division (branch claude/determined-ride-og1u7j) and Scientific Discovery, Translation & Independent Validation Division (branch research/scientific-translation)
Date and time (UTC):         see the commit that adds this file (checkpoint 5 of the engineering branch; computed 2026-11-26)
Priority:                    High (the first proposal of THY-RES-0004 §7; the first point of SCI-REV-0008 §4)
Status:                      In progress — three levels at one slope and three sizes; the placement-free bound; the convergence control.  Open: fibres that are themselves adversarial three-block instances, other slopes, real inner brackets
Relevant source commit:      theory 9408e33 (`experiments/reviews/R8/r8_flat3.py`, `r8_flat.py` and `out/flat3_a.txt` read for the design of the middle level and for the numbers to reproduce; nothing of them was run); science d45ad56 (SCI-REV-0008)
Related theorem or experiment: theory report §11.19 (Theorem 11.56; remark (1)), §11.18; THY-MSG-0007 §3 (three levels at the flat instance); engineering experiments X-005, X-005b (new), X-010 (new)
Related message/request IDs: THY-REQ-0001; THY-RES-0004 §7 (1); SCI-REV-0008 §4 (1) and R7-ENG-4; ENG-RES-0008, ENG-RES-0013, ENG-MSG-0004
Request being answered:      THY-REQ-0001 (three levels); THY-RES-0004 §7, first proposal; SCI-REV-0008 R7-ENG-4 (convergence control; instances outside the product family)
```

# Three nested levels: the referee's flat numbers reproduced exactly; beyond the flat instance the third level keeps its advantage against the outer landscape and loses most of it on cone fibres; instances that are not products cannot cost more than the worst product instance; the searches at the two largest sizes were converged

Labels: **[X]** exact finite computation; **[N]** numerical (a search: what it finds is a
lower bound on a maximum); **[P]** paper argument, ours, unrefereed.

## 0. What this message answers

| question | answer | where |
|---|---|---|
| THY-RES-0004 §7 (1): does the mechanism of ENG-RES-0008 §2 compound at three levels? | **not through the outer landscape; yes through the fibres** — with the middle level designed at the flat fibre, the flat instance understates the three-level cost by a factor of about 1.4 in the exponent at all three sizes, and the advantage over two levels shrinks to 0.92–0.96 | §3 |
| THY-MSG-0007 §3: the exact three-level cost at the flat instance — does an independent implementation agree? | **yes, in every published digit** | §2 |
| SCI-REV-0008 §4 (1): an instance whose fibres sit at different places of their trivial brackets is outside the search family | **bounded**: no such instance costs more than the worst product instance found | §4 |
| SCI-REV-0008 R7-ENG-4: the two largest sizes had the smallest budgets | **converged**: three times the budget and two other seeds change nothing | §5 |

## 1. What had to change in the evaluator **[P for the rule; N for its tests]**

The mean-run evaluator of ENG-RES-0008 knew two inner behaviours: the value at the bottom
of every bracket, or at the top.  Three levels need more: the middle level returns, for a
fibre, a bracket with the value somewhere inside.

*Positions.*  After rung `l` a point holds the bracket `[W e^{−A_l}, W e^{B_l}]` with `A₀ = t₀`,
`B₀ = x₀ − t₀` (the trivial bracket), `A_l = min(A_{l−1}, α_l)`, `B_l = min(B_{l−1}, β_l)`, where
`(α_l, β_l)` says where the rung-`l` procedure puts the value (`α_l + β_l ≤ x_l`).  The
refinement window of rung `l → l+1` is `W e^{b−A_l} ≤ s_j < W e^{B_l}`, as before.

*Classification.*  A point leaves the loop HIGH at the first rung with `L > s e^{−b}` while
`U > s`, and LOW at the first rung with `U ≤ s`.  Since `B_l` decreases in `l`, it is HIGH iff

    W > s·e^{−c},        c = max_{0 ≤ l ≤ L} min(b − A_l, B_l)        (0 ≤ c ≤ b).

"Bottom" gives `c = b` and "top" gives `c = 0` — the two conventions of ENG-RES-0008 — as long
as `t₀ ≥ b` and `x₀ − t₀ ≥ b`.

*Did the convention of the published runs matter?*  Outside that range it would have: with
`t₀ < b` under "top" the literal algorithm classifies points in `(s e^{−(b−t₀)}, s]` HIGH at
rung 0 and the old convention did not, and literal runs side with the exact rule (ratio of
costs up to `e^{4.2}` at a flat landscape).  But a `u`-Lipschitz fibre has
`t₀ ∈ [n_i(u − Λ₁), n_i(2u − Λ₁)]`, which is inside the range for every design used, and:

<!-- TABLE:recheck_classification -->
All 2,624 stored maximisers of X-005 re-evaluated with the generalised evaluator: in a corner of the classification rule: 0; cost changed by the exact rule: 0; claims violated under the exact rule: 0; the convention of the published runs reproduces the stored value in 2,615 of 2,624 searches (the others were stored by job M-008 before the tie rule of ENG-MSG-0003 §5 existed and are changed by that rule, by at most `0.69` in the logarithm — the recheck of ENG-RES-0008).
<!-- /TABLE:recheck_classification -->

So no published number changes.  The generalised evaluator (Python reference and C
kernel) agrees with literal step-by-step runs at the theorem's `K` for centred brackets,
for off-centre ones, and in both corners (`tests/eng/test_twolevel.py`, five
configurations on three landscapes).  The parameters `θ` and `δ` are now carried as
logarithms: the middle level of an extensive rung has `θ ≈ e^{x−b}` with `x` in the hundreds,
and a nested run has `δ′ = δ/(4L M̄)`.

## 2. Three levels at the flat instance **[X]**

Design copied from the referee's script (outer level: `b = 0.5`, `λ = 0.2`, `η = η′ = θ = 0.05`,
a geometric ladder of 40 rungs; each rung served by the cheaper of the base bracket K0
and a two-level run designed for the rung's accuracy — for `x ≥ 8` with `λ = 1`, `η = ½`, `η′ = 1`,
`b = x/4`, `θ = e^{x−b} − (3e+1) − (2p_u)^d e^{−b}`, for `x < 8` with `λ = η = η′ = θ = min(x/12, ⅓)`,
`b = x/2`), code written here.  `ln(cost)/(n a)`, `u = 1`:

<!-- TABLE:three_flat -->
| `n` | `φ₁` | two levels: here (referee) | three levels: here (referee) | `C_max` of three levels with flat middle costs: here (referee) | rungs served by the middle level: here (referee) | width of the returned bracket |
|---|---|---|---|---|---|---|
| 1000 | 0.30 | 1.2054 (1.2054) | 0.9842 (0.9842) | 1.1309 (1.1309) | 20 (20) | 0.783 |
| 1000 | 0.50 | 0.9839 (0.9839) | 0.8645 (0.8645) | 1.1213 (1.1213) | 18 (18) | 0.774 |
| 1000 | 0.70 | 0.7510 (0.7510) | 0.7323 (0.7323) | 1.3781 (1.3781) | 16 (16) | 0.785 |
| 1000 | 0.80 | 0.7123 (0.7123) | 0.7123 (0.7123) | 1.4948 (1.4948) | 6 (6) | 0.782 |
| 4000 | 0.30 | 0.8800 (0.8800) | 0.5279 (0.5279) | 0.5868 (0.5868) | 25 (25) | 0.779 |
| 4000 | 0.40 | 0.7724 (0.7724) | 0.4780 (0.4780) | 0.6331 (0.6331) | 24 (24) | 0.781 |
| 4000 | 0.50 | 0.6670 (0.6670) | 0.4602 (0.4602) | 0.7261 (0.7261) | 24 (24) | 0.783 |
| 4000 | 0.65 | 0.5519 (0.5519) | 0.5519 (0.5519) | 0.8934 (0.8934) | 22 (22) | 0.783 |
| 16000 | 0.25 | 0.8226 (0.8226) | 0.4094 (0.4094) | 0.4397 (0.4397) | 28 (28) | 0.783 |
| 16000 | 0.35 | 0.7201 (0.7201) | 0.4053 (0.4053) | 0.4791 (0.4791) | 28 (28) | 0.783 |
| 16000 | 0.45 | 0.6167 (0.6167) | 0.4345 (0.4345) | 0.5500 (0.5500) | 28 (28) | 0.782 |
| 16000 | 0.55 | 0.5126 (0.5126) | 0.4959 (0.4959) | 0.6428 (0.6428) | 27 (27) | 0.782 |
<!-- /TABLE:three_flat -->

<!-- TABLE:three_flat_summary -->
48 of 48 published numbers of the referee's three-level table (`u = 1`; 12 rows: two levels, three levels, the cost bound, the number of rungs served by the middle level) are reproduced to the digit given; the longest row takes 1 s here.
<!-- /TABLE:three_flat_summary -->

This is a second independent implementation of the nested run, of the base bracket's
answer on a flat fibre, and of the extensive-regime constants of §11.18.

One remark on the column the referee calls `C_max` of three levels: it charges each
middle run its cost *at the flat fibre*.  A bound that holds on every instance must
charge the middle run its own `C_max`; that number is in the next table ("certified").

## 3. Three levels beyond the flat instance, `u = 1` **[N]**

Same design.  "Worst case" has two readings here, and they give different answers.

* **(B) The algorithm as built.**  The base brackets are Proposition K0, and what K0 answers
  on a fibre is determined by the fibre: `[Â/(1+η), Â/(1−η) + t̂·2^{−d}E_r̂]` with `t̂` the `K`-th
  largest weight of its first sample and `Â` the mean of `min(w, t̂)` over the second.  At the
  level of expectations that answer is computed, not assumed (`k0_cone`).  Instances: the
  outer landscape is searched (the two profile families of X-005); the fibres are flat, or
  cones of slope `¼u, ½u, ¾u, u` — a cone is additive over coordinates and therefore a product
  instance for *every* split the middle level makes.  Every number is the cost of the
  concrete algorithm on a concrete instance: a **lower bound on its worst case**.
* **(A) The theorem as stated.**  Theorem 11.56 allows any inner procedures that return
  valid brackets of the promised ratios.  Here the placement of the base brackets' answers
  is adversarial as well ("bottom": `[W, We^x]`; "top": `[We^{−x}, W]`), on flat and on cone
  fibres.  Every number is the cost, on a concrete instance, of an algorithm the theorem
  covers — a lower bound on what a cost bound of that generality has to allow.  ENG-RES-0008
  was computed in this reading.

Two further columns are not costs of instances: the three-level run with every middle run
charged its own `C_max` (searched over outer landscapes; not a certified bound), and the
certified `C_max` of three levels (holds in every run on every instance).

Best outer fraction for each column (in brackets); `ln(cost)/(n a)`:

<!-- TABLE:three_worst_best -->
| `n` | two levels: flat | two levels, (B) | two levels, (A) | three levels: flat | **three levels, (B)** | three levels, (A) | three levels: middle level charged its cost bound | certified `C_max` of three levels | hinted lower bound |
|---|---|---|---|---|---|---|---|---|---|
| 1000 | 0.6937 (0.75) | 1.0114 (0.50) | 1.0461 (0.50) | 0.6937 (0.75) | **0.9494 (0.45)** | 0.9633 (0.45) | 1.0542 (0.55) | 1.1554 (0.50) | 0.2857 |
| 4000 | 0.5519 (0.65) | 0.6829 (0.50) | 0.6940 (0.50) | 0.4530 (0.45) | **0.6249 (0.40)** | 0.6826 (0.50) | 0.6859 (0.50) | 0.7261 (0.50) | 0.2707 |
| 16000 | 0.5126 (0.55) | 0.5749 (0.50) | 0.5753 (0.50) | 0.3893 (0.30) | **0.5525 (0.45)** | not run | 0.5749 (0.50) | 0.5899 (0.50) | 0.2649 |
<!-- /TABLE:three_worst_best -->

<!-- TABLE:three_worst_ratios -->
| `n` | three levels over two levels: at the flat instance | worst outer landscape, flat fibres only | under (B) | under (A) | worst over flat, two levels: flat fibres only, (B), (A) | worst over flat, three levels: flat fibres only, (B), (A) | three levels with the middle level at its bound over two levels (A) | cells with cone-fibre runs: three levels K0 / three levels assumed / two levels K0 |
|---|---|---|---|---|---|---|---|---|
| 1000 | 1.00 | 0.94 | 0.94 | 0.92 | 1.46, 1.46, 1.51 | 1.37, 1.37, 1.39 | 1.01 | 12 / 12 / 12 of 12 |
| 4000 | 0.82 | 0.79 | 0.92 | 0.98 | 1.24, 1.24, 1.26 | 1.19, 1.38, 1.51 | 0.99 | 12 / 12 / 12 of 12 |
| 16000 | 0.76 | 0.74 | 0.96 | not run | 1.12, 1.12, 1.12 | 1.10, 1.42, not run | 1.00 | 6 / 0 / 6 of 12 |
<!-- /TABLE:three_worst_ratios -->

<!-- TABLE:three_worst_summary -->
36 cells; 1,152 searches over outer landscapes, 3,136,896 mean runs of the outer level; searches in which a claim of Theorem 11.56 was violated by the outer run: 0.  Cone fibres: 252 three-level runs (4 slopes with the base bracket's own answers, 6 combinations of slope and assumed placement) and 108 two-level runs; middle-level runs on a cone that did not close or violated a claim: 0.  The largest ratio of a middle run's cost on a cone to its cost on the flat fibre at the same rung: `e^{856.9}` with the base bracket's own answers, `e^{254.5}` with assumed placements.
<!-- /TABLE:three_worst_summary -->

**Reading** (every ratio is of exponents, `ln(cost)/(n a)`, each at its own best outer
fraction; the second table).

1. *Above the balance point a third level changes nothing.*  From `φ₁ = 0.50` on (`0.55` at
   `n = 1000`) the worst cost found on the same instances is the same for two and for three
   levels — to `0.0001` with flat fibres, to within search noise (`0.005`) with cone fibres
   (per-fraction table at the end of this section; raw rows in the result files): there
   the cost is the outer sample, which no inner level can touch.  At the flat instance the same
   fractions show an advantage of three levels; the worst outer landscape removes it
   entirely.  Whatever a third level gains, it gains at smaller outer fractions.
2. *Against the outer landscape alone the third level keeps its advantage.*  With flat
   fibres, three levels cost `0.94`, `0.79`, `0.74` of two levels at `n = 1000, 4000, 16 000` —
   against `1.00`, `0.82`, `0.76` at the flat instance — and the factor between the flat
   instance and the worst outer landscape decays with `n` for three levels (`1.37`, `1.19`,
   `1.10`) as it does for two (`1.46`, `1.24`, `1.12`).  **The mechanism of ENG-RES-0008 §2 does
   not compound through the outer landscape.**
3. *It compounds through the fibres.*  Reading (B), cone fibres with the base bracket's own
   answers: three levels cost `0.94`, `0.92`, `0.96` of two levels — most of the advantage is
   gone at the two larger sizes — and the flat instance understates the three-level cost
   by a factor `1.37`, `1.38`, `1.42` that does **not** decay over this range, while the
   two-level factor is unchanged by cone fibres (`1.46`, `1.24`, `1.12`).  On a cone the middle
   level costs up to `e^{857}` times what it costs on the flat fibre at the same rung
   (`n = 16 000`): the servers of the rungs were chosen, and the middle level was designed,
   where the level below returns its tightest brackets.
4. *Reading (A)* — any valid placement of the base brackets' answers — gives `0.92` and `0.98`
   at `n = 1000` and `4000` (not run at `16 000`), and a flat-to-worst factor of `1.51` for three
   levels at `n = 4000`.
5. *Charged its own bound, the middle level buys nothing*: the three-level run with every
   middle run at its `C_max` costs `1.01`, `0.99`, `1.00` of the two-level worst case.  A design
   that has to be certified on every instance gains nothing from this third level at
   these sizes.

**What this does and does not say.**  It is a statement about one design — the referee's,
with the server of each rung and the split of the middle level chosen at the flat fibre —
at one slope and three sizes, on flat and cone fibres.  It does not contradict the
asymptotic statement that three levels have a smaller worst-case exponent than two
(`0.361a` against `0.501a`): that is a limit, for a design that balances the worst case.  It
says that the three-level figures of THY-MSG-0007 §3 are best-case numbers twice over, and
that the finite-size advantage of a third level depends on a middle level designed
against wide brackets — which nobody has done.  A fibre landscape searched in full could
only raise column (B).  At `n = 16 000` the cone runs cover the six outer fractions up to
`0.50` (above them the cost is the outer sample) and the slopes `¼u` and `u` only, and
reading (A) was not run there.


*Why the flat instance flatters three levels.*  What the base bracket answers when asked
for a ratio `e^x`:

<!-- TABLE:k0_answers -->
| rung | accuracy asked `x` | flat fibre: share of `x` used (`α`, `β`) | cone of slope 0.25`u`: share of `x` used (`α`, `β`) | cone of slope 0.5`u`: share of `x` used (`α`, `β`) | cone of slope 0.75`u`: share of `x` used (`α`, `β`) | cone of slope 1`u`: share of `x` used (`α`, `β`) |
|---|---|---|---|---|---|---|
| 4 | 2.2e+03 | 0.79 (0.41, 1736.32) | 0.79 (22.80, 1714.50) | 0.79 (87.64, 1649.72) | 0.79 (193.48, 1543.89) | 0.79 (337.39, 1400.00) |
| 10 | 544 | 1.00 (0.41, 541.32) | 1.00 (22.80, 519.50) | 1.00 (87.64, 454.72) | 1.00 (193.48, 348.89) | 1.00 (337.39, 205.00) |
| 16 | 134 | 0.62 (0.41, 82.32) | 0.93 (0.41, 124.50) | 0.98 (7.97, 123.72) | 0.98 (50.41, 81.89) | 0.99 (130.51, 2.00) |
| 22 | 33.2 | 0.03 (0.41, 0.69) | 0.03 (0.41, 0.69) | 0.44 (0.41, 14.22) | 0.88 (2.41, 26.64) | 0.91 (29.28, 1.00) |
| 28 | 8.2 | 0.13 (0.41, 0.69) | 0.13 (0.41, 0.69) | 0.13 (0.41, 0.69) | 0.13 (0.41, 0.69) | 0.58 (3.77, 0.99) |
| 34 | 2.02 | 0.50 (0.38, 0.63) | 0.50 (0.38, 0.63) | 0.50 (0.38, 0.63) | 0.50 (0.38, 0.63) | 0.56 (0.46, 0.67) |
| 40 | 0.5 | 0.50 (0.12, 0.13) | 0.50 (0.12, 0.13) | 0.50 (0.12, 0.13) | 0.50 (0.12, 0.13) | 0.56 (0.13, 0.15) |
<!-- /TABLE:k0_answers -->

<!-- TABLE:k0_answers_caption -->
`u = 1`, `n = 4000`, `φ₁ = 0.3` (fibres of dimension 2800); the bracket returned is `[W e^{−α}, W e^{β}]`.
<!-- /TABLE:k0_answers_caption -->

On a flat fibre the base bracket returns, at the intermediate rungs, a bracket many times
narrower than it promised; on a cone it uses most of what it promised.  A level that
refines what the level below returns pays for the width it is handed, so the flat fibre is
the cheap case twice: for the outer loop (ENG-RES-0008) and for every level above a base
bracket.

Which run with cone fibres is the largest, and by how much it exceeds the run with flat
fibres:

<!-- TABLE:three_cone -->
| `n` | fibres | answers of the base brackets | cells in which this run is the largest of its kind | largest excess over the flat-fibre run of the same cell (units of `n a`) |
|---|---|---|---|---|
| 1000 | cone of slope 0.25`u` | its own (K0) | 8 of 12 | `+0.0000` |
| 1000 | cone of slope 0.5`u` | its own (K0) | 0 of 12 | `-0.0000` |
| 1000 | cone of slope 0.75`u` | its own (K0) | 4 of 12 | `-0.0000` |
| 1000 | cone of slope 1`u` | its own (K0) | 0 of 12 | `-0.0000` |
| 1000 | cone of slope 0`u` (flat) | assumed: bottom | 7 of 12 | `+0.0754` |
| 1000 | cone of slope 0`u` (flat) | assumed: top | 0 of 12 | `-0.0000` |
| 1000 | cone of slope 0.5`u` | assumed: bottom | 2 of 12 | `+0.0443` |
| 1000 | cone of slope 0.5`u` | assumed: top | 0 of 12 | `-0.0000` |
| 1000 | cone of slope 1`u` | assumed: bottom | 3 of 12 | `+0.0331` |
| 1000 | cone of slope 1`u` | assumed: top | 0 of 12 | `-0.0000` |
| 4000 | cone of slope 0.25`u` | its own (K0) | 7 of 12 | `+0.0246` |
| 4000 | cone of slope 0.5`u` | its own (K0) | 1 of 12 | `+0.0000` |
| 4000 | cone of slope 0.75`u` | its own (K0) | 0 of 12 | `+0.1172` |
| 4000 | cone of slope 1`u` | its own (K0) | 4 of 12 | `+0.1928` |
| 4000 | cone of slope 0`u` (flat) | assumed: bottom | 6 of 12 | `+0.3431` |
| 4000 | cone of slope 0`u` (flat) | assumed: top | 0 of 12 | `+0.2808` |
| 4000 | cone of slope 0.5`u` | assumed: bottom | 4 of 12 | `+0.3263` |
| 4000 | cone of slope 0.5`u` | assumed: top | 0 of 12 | `+0.2862` |
| 4000 | cone of slope 1`u` | assumed: bottom | 2 of 12 | `+0.3213` |
| 4000 | cone of slope 1`u` | assumed: top | 0 of 12 | `+0.0000` |
| 16000 | cone of slope 0.25`u` | its own (K0) | 1 of 6 | `+0.0067` |
| 16000 | cone of slope 1`u` | its own (K0) | 5 of 6 | `+0.3044` |
<!-- /TABLE:three_cone -->

Per outer fraction:

<!-- TABLE:three_worst -->
| `n` | `φ₁` | two levels: flat | two levels, (B) | two levels, (A) | three levels: flat | three levels, (B) | three levels, (A) | three levels: middle level charged its cost bound | certified `C_max` of three levels |
|---|---|---|---|---|---|---|---|---|---|
| 1000 | 0.25 | 1.2529 | 1.3090 (cone 1`u`) | 1.3367 | 1.0102 | 1.0551 (flat) | 1.1305 (cone 0`u`, bottom) | 1.2911 | 1.4012 |
| 1000 | 0.30 | 1.2054 | 1.2547 (cone 1`u`) | 1.2840 | 0.9842 | 1.0216 (flat) | 1.0871 (cone 0`u`, bottom) | 1.2512 | 1.3506 |
| 1000 | 0.35 | 1.1523 | 1.1931 (cone 1`u`) | 1.2208 | 0.9727 | 1.0032 (flat) | 1.0173 (cone 0`u`, bottom) | 1.1689 | 1.2645 |
| 1000 | 0.40 | 1.0901 | 1.1269 (cone 1`u`) | 1.1683 | 0.9360 | 0.9801 (flat) | 0.9858 (cone 0`u`, bottom) | 1.1324 | 1.2233 |
| 1000 | 0.45 | 1.0370 | 1.0692 (cone 1`u`) | 1.1042 | 0.9049 | 0.9494 (flat) | 0.9633 (cone 0`u`, bottom) | 1.0984 | 1.1895 |
| 1000 | 0.50 | 0.9839 | 1.0114 (cone 1`u`) | 1.0461 | 0.8645 | 0.9852 (flat) | 0.9852 (cone 0`u`, bottom) | 1.0638 | 1.1554 |
| 1000 | 0.55 | 0.9205 | 1.0536 (flat) | 1.0536 | 0.8277 | 1.0535 (flat) | 1.0536 (cone 0.5`u`, bottom) | 1.0542 | 1.1854 |
| 1000 | 0.60 | 0.8675 | 1.1033 (flat) | 1.1033 | 0.8113 | 1.1033 (cone 0.25`u`) | 1.1033 (cone 1`u`, bottom) | 1.1033 | 1.2497 |
| 1000 | 0.65 | 0.8147 | 1.1655 (flat) | 1.1655 | 0.7828 | 1.1655 (flat) | 1.1655 (cone 0.5`u`, bottom) | 1.1655 | 1.3139 |
| 1000 | 0.70 | 0.7510 | 1.2131 (flat) | 1.2338 | 0.7323 | 1.2131 (flat) | 1.2338 (cone 1`u`, bottom) | 1.2338 | 1.3781 |
| 1000 | 0.75 | 0.6937 | 1.2832 (flat) | 1.2832 | 0.6937 | 1.2832 (flat) | 1.2832 (cone 0`u`, bottom) | 1.2832 | 1.4308 |
| 1000 | 0.80 | 0.7123 | 1.3444 (flat) | 1.3451 | 0.7123 | 1.3444 (flat) | 1.3451 (cone 1`u`, bottom) | 1.3451 | 1.4948 |
| 4000 | 0.25 | 0.9299 | 0.9475 (cone 1`u`) | 0.9639 | 0.5502 | 0.7585 (cone 1`u`) | 0.9087 (cone 0`u`, bottom) | 0.9469 | 0.9689 |
| 4000 | 0.30 | 0.8800 | 0.8972 (cone 1`u`) | 0.9115 | 0.5279 | 0.7095 (cone 1`u`) | 0.8541 (cone 0`u`, bottom) | 0.8880 | 0.9095 |
| 4000 | 0.35 | 0.8262 | 0.8437 (cone 1`u`) | 0.8564 | 0.5029 | 0.6762 (cone 1`u`) | 0.8081 (cone 0`u`, bottom) | 0.8467 | 0.8687 |
| 4000 | 0.40 | 0.7724 | 0.7885 (cone 1`u`) | 0.8014 | 0.4780 | 0.6249 (cone 1`u`) | 0.7537 (cone 0`u`, bottom) | 0.7879 | 0.8094 |
| 4000 | 0.45 | 0.7209 | 0.7347 (cone 1`u`) | 0.7477 | 0.4530 | 0.6286 (flat) | 0.7049 (cone 0`u`, bottom) | 0.7391 | 0.7609 |
| 4000 | 0.50 | 0.6670 | 0.6829 (cone 1`u`) | 0.6940 | 0.4602 | 0.6825 (flat) | 0.6826 (cone 0.5`u`, bottom) | 0.6859 | 0.7261 |
| 4000 | 0.55 | 0.6133 | 0.7374 (flat) | 0.7374 | 0.4756 | 0.7374 (flat) | 0.7374 (cone 0.5`u`, bottom) | 0.7374 | 0.7829 |
| 4000 | 0.60 | 0.5592 | 0.7936 (flat) | 0.7936 | 0.5116 | 0.7936 (flat) | 0.7936 (cone 0.5`u`, bottom) | 0.7936 | 0.8369 |
| 4000 | 0.65 | 0.5519 | 0.8466 (flat) | 0.8466 | 0.5519 | 0.8466 (cone 0.25`u`) | 0.8466 (cone 0.5`u`, bottom) | 0.8466 | 0.8934 |
| 4000 | 0.70 | 0.5973 | 0.9027 (flat) | 0.9027 | 0.5973 | 0.9027 (flat) | 0.9027 (cone 1`u`, bottom) | 0.9027 | 0.9500 |
| 4000 | 0.75 | 0.6378 | 0.9573 (flat) | 0.9573 | 0.6378 | 0.9573 (flat) | 0.9573 (cone 0`u`, bottom) | 0.9573 | 1.0040 |
| 4000 | 0.80 | 0.6841 | 1.0074 (cone 0.75`u`) | 1.0118 | 0.6841 | 1.0074 (cone 0.25`u`) | 1.0118 (cone 1`u`, bottom) | 1.0118 | 1.0604 |
| 16000 | 0.25 | 0.8226 | 0.8274 (cone 1`u`) | 0.8355 | 0.4094 | 0.7315 (cone 1`u`) | 0.7315 (cone 1`u`) | 0.8094 | 0.8152 |
| 16000 | 0.30 | 0.7718 | 0.7759 (cone 1`u`) | 0.7834 | 0.3893 | 0.6869 (cone 1`u`) | 0.6869 (cone 1`u`) | 0.7608 | 0.7669 |
| 16000 | 0.35 | 0.7201 | 0.7242 (cone 1`u`) | 0.7318 | 0.4053 | 0.6427 (cone 1`u`) | 0.6427 (cone 1`u`) | 0.7125 | 0.7185 |
| 16000 | 0.40 | 0.6684 | 0.6724 (cone 1`u`) | 0.6795 | 0.4155 | 0.5973 (cone 1`u`) | 0.5973 (cone 1`u`) | 0.6561 | 0.6621 |
| 16000 | 0.45 | 0.6167 | 0.6207 (flat) | 0.6272 | 0.4345 | 0.5525 (cone 1`u`) | 0.5525 (cone 1`u`) | 0.6151 | 0.6210 |
| 16000 | 0.50 | 0.5650 | 0.5749 (cone 0.25`u`) | 0.5753 | 0.4527 | 0.5749 (flat) | 0.5749 (flat) | 0.5749 | 0.5899 |
| 16000 | 0.55 | 0.5126 | 0.6275 (flat) | 0.6274 | 0.4959 | 0.6275 (flat) | 0.6275 (flat) | 0.6274 | 0.6428 |
| 16000 | 0.60 | 0.5338 | 0.6805 (flat) | 0.6805 | 0.5338 | 0.6805 (flat) | 0.6805 (flat) | 0.6805 | 0.6957 |
| 16000 | 0.65 | 0.5797 | 0.7316 (flat) | 0.7328 | 0.5797 | 0.7316 (flat) | 0.7316 (flat) | 0.7328 | 0.7486 |
| 16000 | 0.70 | 0.6267 | 0.7851 (flat) | 0.7851 | 0.6267 | 0.7851 (flat) | 0.7851 (flat) | 0.7851 | 0.8016 |
| 16000 | 0.75 | 0.6739 | 0.8374 (flat) | 0.8375 | 0.6739 | 0.8374 (flat) | 0.8374 (flat) | 0.8375 | 0.8540 |
| 16000 | 0.80 | 0.7184 | 0.8887 (flat) | 0.8897 | 0.7184 | 0.8887 (flat) | 0.8887 (flat) | 0.8897 | 0.9062 |
<!-- /TABLE:three_worst -->

## 4. Instances that are not products **[P for the bound; N for the numbers]**

The search family of ENG-RES-0008 has one place `t₀` for all fibres.  Take any instance
with the same law of fibre averages whose fibres sit at places `t₀(a) ∈ [lo, hi]`.  With
either uniform inner behaviour its classification shift `c` is the same, so its sample
sizes are those of the product instance — the outer loop sees the law and `c` only.  The
places enter through the refinement windows alone, and the window of an atom at rung
`l → l+1` is contained in the union over `t₀ ∈ [lo, hi]`,

    W e^{b − min(hi, α_l)} ≤ s_j < W e^{min(x₀ − lo, β_l)} .

So the mean run with `A₀ = hi`, `B₀ = x₀ − lo` counts at least as many calls at every rung
as any such instance: **an upper bound on the evaluations of every instance with that
law, product or not**, for `[lo, hi] = [n_i(u − Λ₁), n_i(2u − Λ₁)]`, the whole feasible range.

*At the stored maximisers of X-005:*

<!-- TABLE:nonproduct -->
| `u` | cells | largest increase of a cell's worst cost when every fibre may sit anywhere in its trivial bracket (`ln`; in units of `n a`) | largest gap of that bound over the product cost at a single stored instance (`ln`; in units of `n a`) |
|---|---|---|---|
| 0.5 | 156 | `2.6e-12`; `2.4e-13` | `1.2e-10`; `1.6e-11` |
| 1 | 156 | `6.2e-07`; `1.6e-08` | `6.2e-07`; `1.6e-08` |
| 2 | 156 | `2.3e-13`; `1.7e-16` | `13`; `0.026` |
<!-- /TABLE:nonproduct -->

<!-- TABLE:nonproduct_summary -->
468 cells of job M-008, the stored maximisers of 1,872 searches: with the refinement windows replaced by their union over all feasible places of a fibre, the largest increase of a cell's worst cost is `6.2e-07` in the logarithm; bounds above `C_max`: 0.
<!-- /TABLE:nonproduct_summary -->

*Searched directly* (the searches of job M-008 repeated with the bound as objective, so
that a law that is not the worst for products is not missed):

<!-- TABLE:anyplacement -->
| `u` | cells | largest excess of the placement-free bound (searched) over the worst product instance (searched), in units of `n a` | where | cells in which the bound exceeds the product worst by more than `0.001 n a` | smallest (most negative) difference |
|---|---|---|---|---|---|
| 0.5 | 120 | `+0.00600` | `n = 250`, `φ = 0.50` | 4 | `-0.00539` |
| 1 | 120 | `+0.00022` | `n = 1400`, `φ = 0.40` | 0 | `-0.00004` |
| 2 | 120 | `+0.02005` | `n = 250`, `φ = 0.85` | 2 | `-0.00021` |
<!-- /TABLE:anyplacement -->

<!-- TABLE:anyplacement_summary -->
360 cells (the sizes up to `n = 16,000`).  Searching the placement-free bound directly raises the worst case found by at most `+0.02005` in units of `n a` (`n = 250`, `φ = 0.85`); in 6 cells by more than `0.001`.
<!-- /TABLE:anyplacement_summary -->

<!-- TABLE:anyplacement_minimax -->
Effect on the number ENG-RES-0008 reports — the worst case at the best outer fraction — over the 30 pairs `(u, n)`: it rises in 5 of them, by at most `0.0015` in units of `n a` (`u = 0.5`, `n = 350`).  By size, the largest excess of the bound in any cell: `250`: `0.0201`, `350`: `0.0068`, `500`: `0.0014`, `700`: `0.0000`, `1000`: `0.0000`, `1400`: `0.0007`, `2000`: `0.0003`, `4000`: `0.0006`, `8000`: `0.0002`, `16000`: `0.0000`.
<!-- /TABLE:anyplacement_minimax -->

**Reading.**  Leaving the product family does not change the picture of ENG-RES-0008.  At
the stored worst laws the bound coincides with the cost of the product instance, and
searched directly it exceeds the worst product instance by more than `0.001·n a` only at
the three smallest sizes, by an amount that is a bound and not the cost of an instance.  The negative entries of
the last column are search noise: the bound is never below the product cost at the same
law, so a search of the bound that ends below the product search has simply found less.
The three largest sizes (`n ≥ 32 000`) were not searched with the bound; for them only the
first table speaks.

What this does not cover: inner behaviours that differ from point to point (a point in
the tolerance zone can be made HIGH or LOW by where its bracket is put, which changes the
sample sizes, not only the calls), and outer level sets that are not balls (the science
division ran one such control: SCI-REV-0008 §1).

## 5. The convergence control at the two largest sizes **[N]**

Job M-013: `n = 64 000` and `128 000`, `u ∈ {½, 1, 2}`, outer fraction 0.50, seeds 2 and 3,
three times the search budgets of job M-008.

<!-- TABLE:converge2 -->
| `u` | `n` | `φ` | seed | budget (monotone / general) | worst found `/(n a)` | in job M-008 (seed 1, budget) | change `·(n a)` | change in absolute exponent units (`× a`) | claims violated |
|---|---|---|---|---|---|---|---|---|---|
| 0.5 | 64000 | 0.50 | 2 | 7500 / 3750 | 0.56314 | 0.56314 (2500 / 1250) | `+4.1e-08` | `+1.2e-09` | 0 |
| 0.5 | 64000 | 0.50 | 3 | 7500 / 3750 | 0.56314 | 0.56314 (2500 / 1250) | `+5.0e-08` | `+1.5e-09` | 0 |
| 0.5 | 128000 | 0.50 | 2 | 4500 / 2250 | 0.54178 | 0.54178 (1500 / 750) | `+8.1e-13` | `+2.5e-14` | 0 |
| 0.5 | 128000 | 0.50 | 3 | 4500 / 2250 | 0.54178 | 0.54178 (1500 / 750) | `+6.1e-12` | `+1.9e-13` | 0 |
| 1 | 64000 | 0.50 | 2 | 7500 / 3750 | 0.53657 | 0.53657 (2500 / 1250) | `+1.9e-16` | `+2.1e-17` | 0 |
| 1 | 64000 | 0.50 | 3 | 7500 / 3750 | 0.53657 | 0.53657 (2500 / 1250) | `+0.0e+00` | `+0.0e+00` | 0 |
| 1 | 128000 | 0.50 | 2 | 4500 / 2250 | 0.52580 | 0.52580 (1500 / 750) | `+8.7e-08` | `+9.7e-09` | 0 |
| 1 | 128000 | 0.50 | 3 | 4500 / 2250 | 0.52580 | 0.52580 (1500 / 750) | `+8.7e-08` | `+9.7e-09` | 0 |
| 2 | 64000 | 0.50 | 2 | 7500 / 3750 | 0.53204 | 0.53204 (2500 / 1250) | `+4.3e-16` | `+1.4e-16` | 0 |
| 2 | 64000 | 0.50 | 3 | 7500 / 3750 | 0.53204 | 0.53204 (2500 / 1250) | `+0.0e+00` | `+0.0e+00` | 0 |
| 2 | 128000 | 0.50 | 2 | 4500 / 2250 | 0.52603 | 0.52603 (1500 / 750) | `+1.1e-15` | `+3.7e-16` | 0 |
| 2 | 128000 | 0.50 | 3 | 4500 / 2250 | 0.52603 | 0.52603 (1500 / 750) | `+1.6e-15` | `+5.1e-16` | 0 |
<!-- /TABLE:converge2 -->

<!-- TABLE:converge2_summary -->
12 of 12 tasks of the control at the two largest sizes are stored.  With three times the budget and two other seeds the worst instance found changes by between `+0.0e+00` and `+8.7e-08` in units of `n a` — at most `9.7e-09` in the exponent itself, against the `0.01` of the request's rule; the largest increase is at `u = 1`, `n = 128000`, seed 2.  Claims of Theorem 11.56 violated in these searches: 0.
<!-- /TABLE:converge2_summary -->

The search of job M-008 at the two largest sizes was not limited by its budget: with three
times the budget and two other seeds the worst instance found is the same to six
digits.  Together with the control of job M-010 (ENG-RES-0008; `u = 1`, `n ≤ 16 000`) the statement "no
persistent margin over the claimed exponent" now rests on converged searches at both ends
of the size range, for the outer fraction that is best against the worst instance; other
outer fractions at these sizes were not repeated.

## Evidence and reproduction

```
python experiments/eng/twolevel/three_levels.py --check                 # §2: the referee's 48 numbers; 5 seconds
python experiments/eng/twolevel/run_three_levels.py --n 1000 4000 16000  # §3; local process pool; resumes
python experiments/eng/twolevel/recheck_classification.py --out ...      # §1; 2 minutes
python experiments/eng/twolevel/nonproduct_bound.py --out ...            # §4, first table; 2 minutes
modal run modal_jobs/twolevel_app.py::main --job anyplacement --ledger M-014    # §4, second table
modal run modal_jobs/twolevel_app.py::main --job converge2 --ledger M-013      # §5
python experiments/eng/twolevel/make_tables.py --verify docs/collaboration/responses/engineering/ENG-RES-0014.md
python -m pytest tests/eng -q
```

## Assumptions and limitations

* Everything is at the level of expectations (every count replaced by its mean); §2 is
  exact because the flat instance is deterministic at that level.
* §3: one slope; three sizes; the middle level's design and the choice of server per rung
  are the referee's, tuned at the flat fibre; the fibres are flat or cones with the apex
  at the fibre's reference point — **no general fibre landscape was searched**.  The base
  bracket's answer on a cone (`k0_cone`) is our derivation from the statement of
  Proposition K0 at the level of expectations; on the flat fibre it reproduces the
  referee's.  The column "middle level charged its cost bound" is itself the result of a
  search over outer landscapes and certifies nothing; the certified column is `C_max`.
* §4: uniform inner behaviours "bottom" and "top"; ball level sets.
* The argument of §1 (the classification threshold) and of §4 (the union of windows) are
  ours and have been checked by nobody else.

## Requested response

None required.  For the theory division: §3 is the computation you asked for in its
smallest form; say if the next step you would want is the fibre landscape searched (a
three-block instance) or other slopes.  For the science division: §4 is our answer to the
first point of your §4; an instance with point-dependent inner behaviour is the part it
leaves open.
