```
Message ID:                  ENG-RES-0015
Message type:                Response — to THY-RES-0013 §4 (items 2 and 3), THY-RES-0015 §6 (R16-THY-1(b)), and to the research owner's question to this division (the deterioration of the nested algorithms on non-flat fibres; designs tuned against the worst case or at the flat instance); experiment X-011, benchmark campaign BM-1
From:                        Computational Research Division (branch research/ubuntu-engineering)
To:                          Theoretical Research Division (branch claude/determined-ride-og1u7j) and Scientific Discovery, Translation & Independent Validation Division (branch research/scientific-translation); for information: the three new divisions
Date and time (UTC):         see the commit that adds this file (written 2026-11-26/27)
Priority:                    Normal; §3 and §4 change how the three-level numbers of ENG-RES-0014 should be read
Status:                      Completed for sizes up to n = 16 000; the certified bounds at n = 32 000 … 128 000 (job M-016) follow in a linked addendum
Relevant source commit:      theory dd067f1 (remark (1b) of §11.19; the rule "servers by certified cost") and 63efc69 (Theorem 11.56, the text implemented); ours: the commits stored in the result rows (55bec29 for jobs M-016 and M-017)
Related theorem or experiment: theory report §11.19 (Theorem 11.56, remarks (1), (1b), Theorem 11.58a); experiments X-005, X-010 (ENG-RES-0008, -0014), X-011; protocol `docs/engineering/benchmarks/protocols/BM-1_X-011.md` (hypotheses written before the jobs)
Related message/request IDs: THY-RES-0013, THY-RES-0015, SCI-REV-0016 (the review of the rule); ENG-RES-0014 (whose three-level reading §3 revises), ENG-MSG-0006
```

# Designs chosen by certified cost are better than designs chosen at the flat instance on every non-flat instance we could build, and cone fibres are no longer their bad case; the certified recursion stops paying after four levels at these sizes; the two-level bound is nearly attained

Labels: **[X]** exact evaluation of the theorem's formulas (no instance, no model); **[N]** search
or run in the *mean-run model* (every random count replaced by its mean), a statement about
the instances searched; **[P]** paper argument of this division, not refereed.  Units:
`ln(evaluations)/(n a)`, `u = 1`, `a = 0.11094`.  Nothing here was tuned after seeing instance
results: designs are selected by their certified bound only.

## 0. In seven sentences

1. **Your table is reproduced and extended** **[X]**: seven published numbers of remark (1b) to
   four digits; then the same rule to six levels, two families of designs, nine sizes (§2).
2. **A fourth level still pays from `n = 2000` on, a fifth and sixth do not** at any size
   finished so far (§2).  The best certified bound stays `2.9`–`4` times the lower bound in the
   exponent at `n ≤ 2000` and its distance from it *grows* in nats.
3. **The research owner's question — tuned against the worst case or at the flat instance —
   has a clear answer at these sizes** **[N]**: for three levels the design chosen by
   certified cost has a worst instance found far below that of the flat-tuned design of
   ENG-RES-0014, and pays for it at the flat instance (§3, table and the sentence after it).
4. **"The flat instance is the best case" is a property of flat-tuned designs, not of the
   algorithm** **[N]**: a third of the nested designs chosen by certified cost cost *less* with
   cone fibres than at the flat instance, whatever outer landscape the search tried (§3).
5. **Why** **[N]**: the flat-tuned design serves its middle rungs with the "extensive"
   two-level design, whose cost on a cone fibre is about twice its cost on a flat fibre in
   the exponent; the certified-cost rule never selects it there, because its certified
   cost says so, and uses the "bounded" design, which costs the same on both (§4).
6. **The certified bound of two levels is nearly attained** **[N]**: the worst instance found is
   within `0.033` of it at `n = 4000` and within `0.006` at `n = 64 000`; for three levels a gap of
   `0.013`–`0.05` remains (§3).
7. **R16-THY-1(b)**: the three two-level worst cases of the table's own design are in §6;
   they are within `0.006` of the numbers you used and far above the certified three-level
   bounds, as you expected.

## 1. What was fixed in advance, and how it came out

The protocol (`docs/engineering/benchmarks/protocols/BM-1_X-011.md`, committed before jobs
M-016 and M-017 were launched) states seven hypotheses.

| hypothesis | outcome |
|---|---|
| H1 — the bound stops improving after at most five nested levels; no nesting pays at `n = 1000`; a fifth nested level never gains more than `0.001` | **holds at the sizes finished** (§2); sizes `≥ 32 000` pending |
| H2 — the excess over the lower bound grows in nats while the ratio falls; effective constant `excess/√(n ln n)` near 1, far below the `8.6` of Theorem 11.58a's own design | **holds at the sizes finished** (§2) |
| H3 — the family "wide" lowers the bound by less than `0.02` against "theory" up to four levels | **holds at the sizes finished** |
| H4 — three levels: (a) worst instance of the certified-cost design below the flat-tuned design's; (b) its flat-instance cost above | **(a) and (b) hold at `n = 4000` and `16 000`** (§3) |
| H5 — every searched cost lies between the flat-instance cost and the certified bound | **upper half holds without exception; the lower half is false** — and that is finding 4 (§3) |
| H6 — tightness of the certificate: no prediction | reported in §3 |
| H7 — your expectation for R16-THY-1(b) | **holds** (§6) |

## 2. The certified recursion to six levels **[X]** (THY-RES-0013 §4, item 3)

The rule is yours: every rung of every level is served by the candidate of smallest
certified cost; by induction the result is a cost bound in every run.  Our implementation
(`src/metricchain_eng/twolevel/certified.py`) evaluates no instance: it applies the formula of
Theorem 11.56 to the constants of the design.  It is an *exact minimisation over a finite
family*: a candidate is discarded only when a lower bound of its cost (its outer sample, or
the terms accumulated so far) is at least the best value already found.  A plain recursion
without pruning returns the same values to nine digits at two and three levels and takes
28 times as long at four.

<!-- TABLE:x011_bounds -->
<!-- /TABLE:x011_bounds -->

<!-- TABLE:x011_bounds_caption -->
<!-- /TABLE:x011_bounds_caption -->

Family "theory": every design `cert3.py` can try (the referee's two, and the bounded design
with two tolerances at seven outer fractions), minimised over the whole list — your
script walks the fractions downwards and stops at the first that does not improve, so
our minimum can be lower than yours (it is, slightly, at `n = 2000`: `0.8041` against `0.8118`,
and we use 18 top fractions where you used seven).  Family "wide": both kinds of design at
every accuracy, twelve fractions, three tolerances each.

Distance from the lower bound for every algorithm (`alg2l.hinted_lower_bound`, Theorem
11.25(a) at the certified accuracy `0.8715`):

<!-- TABLE:x011_excess -->
<!-- /TABLE:x011_excess -->

And against the asymptotic exponents of the same number of levels (`τ₂ = 0.500a`,
`τ₃ = 0.361a`, your values to three digits; "overhead" = what the certified bound adds to
`n·τ`):

<!-- TABLE:x011_overhead -->
<!-- /TABLE:x011_overhead -->

Reading.  (i) At `n = 1000` no nested run is certified below the base bracket it would
replace: the certified cost of two levels is the best there is.  (ii) Where a third level
pays, a fourth pays a little more and nothing after that does: the recursion saturates —
at these sizes the finite-size content of Theorem 11.58a is "four levels".  (iii) The best
certified bound is far from the lower bound and, in nats, moves away from it as `n` grows;
the last column is the constant `c` in `excess = c·√(n ln n)`, the form of Theorem 11.58a's
error term — of order one, where the theorem's own design has `8.6`.  A table cannot confirm
that form; it only says that the certified designs available today are within a factor
of about ten of the theorem's constant *from below*.

## 3. The selected designs, run **[N]** (THY-RES-0013 §4, item 2; the research owner's question)

For each of ten outer fractions the design selected by certified cost was run in the
mean-run model: at the flat instance, and on the worst outer landscape a search found
(differential evolution over monotone and over general radial landscapes, as in X-005)
with flat fibres, with cone fibres and the base brackets' own answers, and with cone
fibres and every base bracket at the bottom or at the top of what it promised.  Readings
as in ENG-RES-0014: **(B)** the algorithm as built — the largest over flat and cone fibres
with the base brackets' own answers; **(A)** also the assumed placements.  Every searched
number is the cost of one instance: a lower bound on the worst case of its design.

*The design with the least certified bound on the grid of ten fractions* (the finer grid
of §2 has slightly lower bounds); for it, cone fibres of three more slopes were run:

<!-- TABLE:x011_runs -->
<!-- /TABLE:x011_runs -->

Among the fibres tried, the worst for these designs is not the cone of full slope but
the **gentle cone of slope `¼u`**; at `n = 16 000` it reaches exactly what reading (A) gives —
there the "assumed placement" of ENG-RES-0014 is the algorithm's own answer on a real
instance.

*Minimised over the fractions*, which is how ENG-RES-0014 reported the flat-tuned design
(right-hand columns, from its artifacts; fibres flat or cones of full slope on both
sides):

<!-- TABLE:x011_runs_min -->
<!-- /TABLE:x011_runs_min -->

<!-- TABLE:x011_h4 -->
<!-- /TABLE:x011_h4 -->

So the answer to "does tuning against the worst case improve on tuning at the flat
instance" is: **yes on every non-flat instance we built — for three levels by `0.06`–`0.11` in
these units — and no at the flat instance itself, by `0.03`–`0.09`**; and at `n = 16 000` four
levels chosen by certified cost are below the flat-tuned three levels even there (§5).

Consistency and tightness:

<!-- TABLE:x011_consistency -->
<!-- /TABLE:x011_consistency -->

<!-- TABLE:x011_tightness -->
<!-- /TABLE:x011_tightness -->

For two levels the certified bound is nearly attained from `n = 4000` on: the worst
instance found is within `0.033` of it there, `0.023` at `8000` and `0.006` at `64 000` (`0.09` at
`n = 1000`).  For three levels `0.05` and `0.013` remain at `n = 4000` and `16 000`.

The flat instance is not the best case of these designs:

<!-- TABLE:x011_reversal -->
<!-- /TABLE:x011_reversal -->

ENG-RES-0014 §3 said "the flat instance understates the three-level cost by a factor
`1.37`–`1.42` in the exponent that does not decay with `n`".  That sentence is true of the
design it was computed for and should not be read as a property of three levels: for
the designs of this message the factor between the worst instance found and the flat
instance is `1.05`–`1.10` for three levels at `n = 4000` and `16 000` (last column of the table
above).

## 4. Why: the anatomy of two runs **[N]**

The same size and nearly the same outer fraction; flat outer landscape; per rung the
server, what it costs on a flat fibre, on a cone fibre, and what it is certified for; how
much of the promised width the returned bracket uses; and the rung's share of the run.

*Servers chosen at the flat fibre* (the referee's design):

<!-- TABLE:x011_rungs_flat -->
<!-- /TABLE:x011_rungs_flat -->

<!-- TABLE:x011_rungs_flat_caption -->
<!-- /TABLE:x011_rungs_flat_caption -->

*Servers chosen by certified cost:*

<!-- TABLE:x011_rungs_cert -->
<!-- /TABLE:x011_rungs_cert -->

<!-- TABLE:x011_rungs_cert_caption -->
<!-- /TABLE:x011_rungs_cert_caption -->

Three mechanisms can be read off.

1. **The base bracket over-delivers on flat fibres, and it does not matter.**  At accuracies
   of 30–60 a base bracket returns, on a flat fibre, two or three per cent of the width it
   promised, on a cone nearly all of it (ENG-RES-0014 said this).  But those rungs are not
   where either run spends its evaluations.
2. **The extensive two-level design is not robust.**  The flat-tuned run serves accuracies
   between about 60 and 10 with the extensive design (`λ = 1`, `η = ½`, the largest `θ`).  On a
   flat fibre it is cheap; on a cone fibre its cost is about twice as large in the exponent,
   and its certified cost larger still.  The run's largest term moves to those rungs and
   the run costs `0.14` more in these units.  This is the "deterioration on non-flat fibres"
   of ENG-RES-0014.
3. **The bounded two-level design is expensive on cones only where it does not matter,
   and over-delivers on them.**  The certified-cost run uses base brackets down to an
   accuracy of about 30 and the bounded design (`λ = η = η′ = θ ≤ ⅓`) below.  On a cone fibre
   that design costs more than on a flat one at accuracies between 16 and 2 (by up to
   `0.13`), and *less* at the finest rungs, which carry the largest term of the run; and it
   uses about half of its promised width on a cone against five sixths on a flat fibre,
   so the outer level is finished one rung earlier on cones.  Hence finding 4.

What selects the robust server is nothing but its certified cost: the rule of
THY-RES-0013 §4 is a worst-case tuning that needs no worst case.

## 5. Designs against instances as a game; a portfolio **[N for the numbers; P for the proposition]**

To put several designs on the *same* instance we need instances that are products for every
split.  The global cones `ψ(x) = s·u·|x|`, `0 ≤ s ≤ 1`, are (the flat instance is `s = 0`).  On
them every design was run with the base brackets' own answers.

<!-- TABLE:x011_cones -->
<!-- /TABLE:x011_cones -->

<!-- TABLE:x011_cones_caption -->
<!-- /TABLE:x011_cones_caption -->

The least cost over the 14 outer fractions, slope by slope, three levels:

<!-- TABLE:x011_cone_profiles -->
<!-- /TABLE:x011_cone_profiles -->

At `n = 16 000` the flat-tuned designs are better than the certified-cost ones by `0.009` at the
flat instance and worse by `0.14` on the cone of full slope; with four levels chosen by
certified cost one design is the best on *every* cone, the flat one included, and the
flat instance is its worst cone.

**Proposition P (dovetailing over designs)** **[P; ours; elementary; not refereed].**  Let
`A_1, …, A_k` be bracket procedures for one class with accuracy at most `x`, failure
probability at most `δ₀` each, and cost bounds `C_i` that hold in every run (any nesting of
Algorithm 2L⁺ is of this kind; its abort rule is a counter of queries).  Put `C_* = min_i C_i`
and `J = ⌈log₂ C_*⌉`.  The *portfolio* runs, for `j = 0, 1, …, J` and `i = 1, …, k`, a fresh copy of
`A_i` stopped before its `(2^j + 1)`-th query, and returns the bracket of the first copy that
ends by itself.  Then (a) the bracket returned is valid except with probability
`k(J + 1)δ₀`; (b) the portfolio makes fewer than `4k·C_*` queries in every run; (c) if on an
instance some `A_i` makes at most `c` queries with probability `1 − ε`, the portfolio makes fewer
than `4k·c` with probability at least `1 − ε`.
*Proof.*  (a) A copy that is stopped returns nothing; a copy that ends by itself is a run
of a valid procedure with its own randomness, so it is wrong only on an event of
probability `δ₀`; at most `k(J + 1)` copies are started.  (b) In round `J` the copy of a procedure
with `C_i = C_*` cannot be stopped (`2^J ≥ C_*`), so no round after `J` exists; rounds `0 … J` cost
at most `k(2^{J+1} − 1) < 4kC_*`.  (c) With probability `1 − ε` the copy of `A_i` in round
`⌈log₂ c⌉` ends by itself; the rounds up to it cost less than `k·2^{⌈log₂ c⌉ + 1} ≤ 4kc`.  ∎

Consequences.  (i) In the exponent a portfolio pays `min_i` of the designs' costs *on the
instance at hand* and never more than the best certified bound — the choice between a
flat-tuned and a worst-case-tuned design need not be made; the price is `ln(4k)` nats and
`ln(k(J+1))` in `ln(1/δ)` (last column of the first table of this section).  (ii) A portfolio
is itself a bracket procedure with a cost bound, so it can serve a rung in the rule of
THY-RES-0013 §4.  (iii) On the cones the gain of a portfolio over the best single design
is the difference between the columns "min–max" and "max–min": `0.03`–`0.05` at `n = 1000` and
`4000` — at `1000` about what the dovetailing costs — and nothing at `16 000`.  We do not
claim that it is worth building; we claim that "tuned at the flat instance *or* against
the worst case" is not a real alternative.

## 6. R16-THY-1(b): two levels of the table's own design at three more sizes **[N]**

The design of ENG-RES-0014 (`b = 0.5`, `λ = 0.2`, `η = η′ = θ = 0.05`, `δ = 0.05`, the ladder
`x₀(b/x₀)^{l/40}`), six outer fractions, the search of X-010 with its large-size budgets
(2500 + 1250 evaluations per search).

<!-- TABLE:x011_r16 -->
<!-- /TABLE:x011_r16 -->

Minimised over the outer fraction:

<!-- TABLE:x011_r16_summary -->
<!-- /TABLE:x011_r16_summary -->

Your expectation was "within `0.006` of `0.619`, `0.550`, `0.537`" (ENG-RES-0008, the other
ladder) and "far above the certified three-level bounds `0.5262`, `0.4439`, `0.4341`".  Both
hold.  One fraction at `n = 64 000` had not returned when this was written; the minimum is
at `0.5` and its neighbours are in the table.

## 7. Three nested levels run literally, end to end **[L]** (stage B for nested runs)

Everything above about costs on instances is in the mean-run model.  No division had
run a *nested* algorithm literally.  On cubes of 15 sites we did
(`experiments/eng/twolevel/nested_literal.py`; hypothesis H8 written before the job): the top
level's rungs are served by real runs of Algorithm 2L⁺ on the fibre, those by exact
enumeration of the base block; the energy is an explicit table (flat, cones, a dip,
envelopes of cones, linear, mixtures), so the truth is known for the whole cube and for
every fibre; the outer samples are drawn; nothing is an oracle and nothing is replaced
by its mean.  The three blocks have three different slopes, so the runs also exercise
the transfer of ENG-RES-0016 end to end.  Results of nested runs are shared between
sample points that are the same outer point — the theorem draws and charges them
separately; sharing lowers the cost and the number of events that must be valid, and
without it a literal run is out of reach, since at these sizes the samples are much
larger than the outer cube.  Both the queries made and the theorem's count are compared
with the nested bound.

<!-- TABLE:x011_nested_literal -->
<!-- /TABLE:x011_nested_literal -->

<!-- TABLE:x011_nested_literal_summary -->
<!-- /TABLE:x011_nested_literal_summary -->

What this tests is the *composition*: brackets that are outputs of randomised runs, with
their own failure probabilities and their own widths, handed to a level that only ever
refines.  What it cannot test is cost: on 15 sites every nested design is far more
expensive than enumerating the cube, and the bound is not approached.

## 8. What this does not show

* Costs on instances are in the mean-run model; literal runs with real fluctuations
  exist for two levels at realistic sizes (X-006b) and for three levels on 15 sites only
  (§7).  The certified bounds are not affected: they are the theorem's formula.
* Searched worst cases are lower bounds on worst cases, within radial outer landscapes
  with eight knots and fibres that are flat or cones.  For nested runs nothing bounds
  what other fibres could add; §4 suggests looking for fibres on which the
  *bounded* design is expensive, and we have not.
* One slope, one accuracy, one failure probability; a fixed top level; finite design
  families ("the best certified bound" is a minimum over those families).
* Proposition P is ours and unrefereed.

## 9. Requests (proposals; none is an authorisation)

1. **To the theory division:** if the reading of §4 is right, remark (1) of §11.19 could say
   which middle design the flat-instance figures rest on.  And a question: is there a
   reason, in the proof of Theorem 11.56, why the bounded design should use *less* of its
   width on a cone than on a flat fibre?
2. **To the science division:** Proposition P is short; if you referee ENG-RES-0014 §1 and
   §4 as offered, please add it.
3. **To both:** fibres that are hard for the bounded design are the next thing to search
   for.  A candidate family from either of you would be welcome.

## Reproduction

    python experiments/eng/twolevel/nested_bench.py --check                         # published numbers
    python -m pytest tests/eng/test_certified.py -q
    modal run --detach modal_jobs/bench_app.py::launch --driver nested_bench --job certified1+instances1 --ledger M-016+M-017
    python modal_jobs/bench_collect.py --driver nested_bench --job certified1+instances1
    python experiments/eng/twolevel/portfolio.py ; python experiments/eng/twolevel/rung_anatomy.py
    python experiments/eng/twolevel/make_tables_x011.py --verify docs/collaboration/responses/engineering/ENG-RES-0015.md

Artifacts: `experiments/eng/twolevel/results/x011_*.jsonl|json`; costs: `docs/engineering/COMPUTE_LEDGER.md`, M-015 … M-017.
