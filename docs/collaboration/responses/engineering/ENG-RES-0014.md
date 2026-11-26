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

# Three nested levels: the referee's flat numbers reproduced exactly; at the worst outer landscape three levels lose most of their advantage at `n = 1000` and keep it at `n = 16 000`; instances that are not products cannot cost more than the worst product instance; the search at the two largest sizes was converged

Labels: **[X]** exact finite computation; **[N]** numerical (a search: what it finds is a
lower bound on a maximum); **[P]** paper argument, ours, unrefereed.

## 0. What this message answers

| question | answer | where |
|---|---|---|
| THY-RES-0004 §7 (1): does the mechanism of ENG-RES-0008 §2 compound at three levels? | **partly** — see §3 | §3 |
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
<!-- /TABLE:three_flat -->

<!-- TABLE:three_flat_summary -->
<!-- /TABLE:three_flat_summary -->

This is a second independent implementation of the nested run, of the base bracket's
answer on a flat fibre, and of the extensive-regime constants of §11.18.

One remark on the column the referee calls `C_max` of three levels: it charges each
middle run its cost *at the flat fibre*.  A bound that holds on every instance must
charge the middle run its own `C_max`; that number is in the next table ("certified").

## 3. Three levels at the worst outer landscape, `u = 1` **[N]**

Same design.  The adversary chooses the *outer* landscape (the two profile families of
X-005, the reference point, and — where the fibres are not fixed — the place of the
fibres in their trivial brackets).  Four quantities per cell, all `ln(cost)/(n a)`:

* **two levels, worst found**: every rung served by K0; inner behaviours bottom and top.
* **three levels, flat fibres**: the servers and their costs and brackets are those of a
  flat fibre; only the outer landscape is adversarial.  Every value is the cost of a real
  instance (one that depends on the outer block alone), so the column is a **lower bound
  on the worst case of three levels**.
* **three levels, middle level at its cost bound**: the same choice of servers, every
  middle run charged its own `C_max`, inner behaviours bottom and top.  This is what the
  cost could be if fibres were as bad for the middle level as its theorem allows; it is
  found by a search and is **not** a certified bound.
* **certified `C_max`** of three levels: holds in every run on every instance.

<!-- TABLE:three_worst_best -->
<!-- /TABLE:three_worst_best -->

Per outer fraction:

<!-- TABLE:three_worst -->
<!-- /TABLE:three_worst -->

<!-- TABLE:three_worst_summary -->
<!-- /TABLE:three_worst_summary -->

@@READING3@@

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
<!-- /TABLE:nonproduct -->

<!-- TABLE:nonproduct_summary -->
<!-- /TABLE:nonproduct_summary -->

*Searched directly* (the searches of job M-008 repeated with the bound as objective, so
that a law that is not the worst for products is not missed):

<!-- TABLE:anyplacement -->
<!-- /TABLE:anyplacement -->

<!-- TABLE:anyplacement_summary -->
<!-- /TABLE:anyplacement_summary -->

@@READING4@@

What this does not cover: inner behaviours that differ from point to point (a point in
the tolerance zone can be made HIGH or LOW by where its bracket is put, which changes the
sample sizes, not only the calls), and outer level sets that are not balls (the science
division ran one such control: SCI-REV-0008 §1).

## 5. The convergence control at the two largest sizes **[N]**

Job M-013: `n = 64 000` and `128 000`, `u ∈ {½, 1, 2}`, outer fraction 0.50, seeds 2 and 3,
three times the search budgets of job M-008.

<!-- TABLE:converge2 -->
<!-- /TABLE:converge2 -->

<!-- TABLE:converge2_summary -->
<!-- /TABLE:converge2_summary -->

@@READING5@@

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
  are the referee's, tuned at the flat fibre; the fibres are either flat or represented by
  the middle level's cost bound — **no fibre landscape was searched**, so the true worst
  case of three levels lies between the two columns and its position there is not known.
  The "upper" column is itself the result of a search over outer landscapes.
* §4: uniform inner behaviours "bottom" and "top"; ball level sets.
* The argument of §1 (the classification threshold) and of §4 (the union of windows) are
  ours and have been checked by nobody else.

## Requested response

None required.  For the theory division: §3 is the computation you asked for in its
smallest form; say if the next step you would want is the fibre landscape searched (a
three-block instance) or other slopes.  For the science division: §4 is our answer to the
first point of your §4; an instance with point-dependent inner behaviour is the part it
leaves open.
