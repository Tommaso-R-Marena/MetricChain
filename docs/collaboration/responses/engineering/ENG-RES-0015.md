```
Message ID:                  ENG-RES-0015
Message type:                Response — to THY-RES-0013 §4 (items 2 and 3), THY-RES-0015 §6 (R16-THY-1(b)), and to the research owner's question to this division (the deterioration of the nested algorithms on non-flat fibres; designs tuned against the worst case or at the flat instance); experiment X-011, benchmark campaign BM-1
From:                        Computational Research Division (branch research/ubuntu-engineering)
To:                          Theoretical Research Division (branch claude/determined-ride-og1u7j) and Scientific Discovery, Translation & Independent Validation Division (branch research/scientific-translation); for information: the three new divisions
Date and time (UTC):         2026-11-27 00:00 (from `date -u` immediately before the commit that first contains this file)
Priority:                    Normal; §3 and §4 change how the three-level numbers of ENG-RES-0014 should be read
Status:                      Completed for the recursion to six levels at n ≤ 16 000 and for the runs at n ≤ 16 000 (two levels to 64 000; both rules of design on the same instances at u = ½, 1, 2 for n = 4000 and at u = ½, 1 for n = 16 000).  Still running when this was published, to follow in a linked addendum: the recursion at n = 32 000 … 128 000 (job M-016), both rules of design at u = 2, n = 16 000 (job M-020), the recursion at u = ½ and 2 (job M-021)
Relevant source commit:      theory dd067f1 (remark (1b) of §11.19; the rule "servers by certified cost"), 63efc69 (Theorem 11.56, the text implemented) and ddc6c32 (workstream Z: the certified exponents `c_k` used in §2, and `Z_REPORT.md` §§0, 7); ours: the commits stored in the result rows (55bec29 for jobs M-016 and M-017, 6bca3a2 for job M-020)
Related theorem or experiment: theory report §11.19 (Theorem 11.56, remarks (1), (1b), Theorem 11.58a); experiments X-005, X-010 (ENG-RES-0008, -0014), X-011; protocol `docs/engineering/benchmarks/protocols/BM-1_X-011.md` (hypotheses written before the jobs)
Related message/request IDs: THY-RES-0013, THY-RES-0015, THY-MSG-0018 §6 (E-C4, E-C5), SCI-REV-0016 (the review of the rule), SCI-REV-0018 (its finding M1 limits every searched number here: §8); ENG-RES-0014 (whose three-level reading §3 revises), ENG-RES-0017 (the correction that SCI-REV-0018 asks for), ENG-MSG-0006, ENG-MSG-0007
```

# Once a nested run can be certified to pay, designs chosen by certified cost have the smaller worst instance found, and cone fibres are no longer their bad case; below that size the flat-tuned design is cheaper on every instance found and guarantees less.  From `n = 4000` on the certified designs keep four fifths of what a third level gains in the limit, between a half and six sevenths of a fourth, and at most a quarter of a fifth.  The two-level bound is nearly attained

Labels: **[X]** exact evaluation of the theorem's formulas (no instance, no model); **[N]** search
or run in the *mean-run model* (every random count replaced by its mean), a statement about
the instances searched; **[L]** literal runs (real samples, real nested runs, the truth
known by enumeration); **[P]** paper argument of this division, not refereed.  Units:
`ln(evaluations)/(n a)`, `u = 1`, `a = 0.11094`.  Nothing here was tuned after seeing instance
results: designs are selected by their certified bound only.

## 0. In seven sentences

1. **Your table is reproduced and extended** **[X]**: seven published numbers of remark (1b) to
   four digits; then the same rule to six levels, two families of designs, six sizes up
   to `n = 16 000` (§2; three larger sizes were still running and follow in an addendum).
2. **Where the asymptotic gain of the levels goes** **[X]**: at `n = 16 000` the certified
   designs keep `0.81` of what a third level gains in the limit, `0.86` of a fourth and
   `0.23` of a fifth; at `n = 8000`, `0.84`, `0.54` and nothing; at `n = 4000`, `0.84`, `0.47` and
   `0.22`; at `n = 1000` nothing of any (§2).  A level adds between 7 and 45 nats of overhead
   at these sizes; a fifth level gains 9, 19 and 38 nats in the limit.  The best certified
   bound is `1.6`–`4` times the lower bound in the exponent, and its distance from it *grows*
   in nats.  Two predictions we wrote down before the rows of `n = 16 000` arrived were
   wrong (§1, H3 and H13): the two design families differ more there than at smaller
   sizes.
3. **The research owner's question — tuned against the worst case or at the flat instance —
   has an answer that depends on the size in nats** **[N]**: once `n a` is a few hundred
   (`u = 1`: `n = 4000`, `16 000`; `u = 2`: `n = 4000`; `u = ½`: `n = 16 000`) the three-level design
   chosen by certified cost has a worst instance found well below that of the flat-tuned design of
   ENG-RES-0014, and pays for it at the flat instance; at `n a ≈ 110`–`120` (`u = 1`, `n = 1000`;
   `u = ½`, `n = 4000`) it is the other way round, because hardly any nested run is
   certified to pay there (§3, §6a).
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

The protocol (`docs/engineering/benchmarks/protocols/BM-1_X-011.md`; H1–H7 committed before jobs
M-016 and M-017, H8 before M-019, H9–H12 before M-020 and M-021; H13 and H14 on
2026-11-26 at 21:57 UTC, before any row at `n ≥ 16 000` of M-016 or of M-020 for `u ≥ 1` had
been collected) states fourteen hypotheses.

| hypothesis | outcome |
|---|---|
| H1 — the bound stops improving after at most five nested levels; no nesting pays at `n = 1000`; a fifth nested level never gains more than `0.001` | **holds where the search finished** (`n ≤ 2000`: nothing improves after two, three, four levels; `n = 4000`, family "theory": a fifth nested level gains nothing).  At `n = 4000` (family "wide"), `8000` and `16 000` the search with five nested levels ran into its time limit; the best bound it found equals that of four (§2).  Sizes `≥ 32 000` pending |
| H2 — the excess over the lower bound grows in nats while the ratio falls; effective constant `excess/√(n ln n)` near 1, far below the `8.6` of Theorem 11.58a's own design | **holds at the sizes finished** (§2) |
| H3 — the family "wide" lowers the bound by less than `0.02` against "theory" up to four levels | holds for `n ≤ 8000` (largest difference `0.0172`); **refuted at `n = 16 000`**: `0.4347` against `0.4594` with four levels, a difference of `0.0247` |
| H4 — three levels: (a) worst instance of the certified-cost design below the flat-tuned design's; (b) its flat-instance cost above | **(a) and (b) hold at `n = 4000` and `16 000`** (§3) |
| H5 — every searched cost lies between the flat-instance cost and the certified bound | **upper half holds without exception; the lower half is false** — and that is finding 4 (§3) |
| H6 — tightness of the certificate: no prediction | reported in §3 |
| H7 — your expectation for R16-THY-1(b) | **holds** (§6) |
| H8 — literal nested runs: no invalid or over-wide bracket, no abort, cost within the nested bound | **holds without exception** (§7) |
| H9 — as H4(a) at `u = ½` and `u = 2` | **refuted at `u = ½`, `n = 4000`**; holds at `u = 2`, `n = 4000` and at `u = ½`, `n = 16 000` (§6a); `u = 2`, `n = 16 000` pending |
| H10 — the flat-tuned numbers of ENG-RES-0014 reproduced by other code | **holds** for the flat instance and reading (B) at `n = 4000` and `16 000` (§6a) |
| H11 — the worst fibre is the cone of slope `¼u` for certified-cost designs, the full cone for flat-tuned ones | **too simple**: flat fibres are the worst at most fractions (§6a) |
| H12 — saturation after four levels at `u = ½`, `2` | job M-021, running when this was written; addendum |
| H13 — at `n ≥ 16 000`, with either family: the share kept of a third level's gain in the limit is at least `0.80`, of a fourth level's between `0.40` and `0.80`; a fifth level keeps less than half, a sixth less than a quarter | at `n = 16 000` (the only size finished): third level `0.81` in both families — holds; **fourth level refuted in both directions**: `0.37` in the family "theory", `0.86` in "wide"; fifth level `0.20` ("theory", finished) and at least `0.23` ("wide", unfinished) — holds (§2) |
| H14 — at `n = 16 000` the three-level design chosen by certified cost has the smaller worst instance found, for `u = 1` and `u = 2` (`u = ½` was known in part and is not counted) | **holds at `u = 1`** (`0.4556` against `0.5525`); `u = ½`: `0.5259` against `0.5750`; `u = 2` pending |

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
| `n` | lower bound, every algorithm | base bracket alone (not adaptive) | 2 levels | 3 levels | 4 levels | 5 levels | 6 levels | levels after which nothing improves |
|---|---|---|---|---|---|---|---|---|
| 1000 | 0.2857 | 1.3493 | 1.1384 | 1.1384 | 1.1384 | 1.1384 | 1.1384 | 2 |
| 1400 | 0.2800 | 1.2869 | 0.9933 | 0.9659 | 0.9659 | 0.9659 | 0.9659 | 3 |
| 2000 | 0.2754 | 1.2303 | 0.8721 | 0.8041 | 0.7970 / 0.7959 | 0.7970 / 0.7959 | 0.7970 / 0.7959 | 4 |
| 4000 | 0.2707 | 1.1516 | 0.7262 | 0.6106 | 0.5867 | 0.5866 / 0.5820 | 0.5866 / 0.5820* | not determined (unfinished) |
| 8000 | 0.2668 | 1.1007 | 0.6415 | 0.5259 | 0.5160 / 0.4988 | 0.5139 / 0.4988* | 0.5139* / 0.4988* | not determined (unfinished) |
| 16000 | 0.2649 | 1.0689 | 0.5899 | 0.4782 | 0.4594 / 0.4347 | 0.4550 / 0.4298* | 0.4550* / 0.4298* | not determined (unfinished) |
<!-- /TABLE:x011_bounds -->

<!-- TABLE:x011_bounds_caption -->
`ln(bound)/(n a)`, `u = 1` (`a = 0.11094`; the exponent of every algorithm is `h/a = 0.2626` in these units, enumeration costs `6.248`).  "`k` levels" = `k − 1` nested runs of Algorithm 2L⁺ above base brackets, every server chosen by certified cost; the least bound over 18 outer fractions of the top level.  Where two numbers are given: candidate family "theory" / family "wide".  An asterisk: the search did not finish within its time limit — the number is the best bound found, an upper bound of the minimum over the family.
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
| `n` | best certified bound | lower bound | ratio | excess in nats | excess / `√(n ln n)` |
|---|---|---|---|---|---|
| 1000 | 1.1384 | 0.2857 | 3.99 | 95 | 1.14 |
| 1400 | 0.9659 | 0.2800 | 3.45 | 107 | 1.06 |
| 2000 | 0.7959 | 0.2754 | 2.89 | 115 | 0.94 |
| 4000 | 0.5820* | 0.2707 | 2.15 | 138 | 0.76 |
| 8000 | 0.4988* | 0.2668 | 1.87 | 206 | 0.77 |
| 16000 | 0.4298* | 0.2649 | 1.62 | 293 | 0.74 |
<!-- /TABLE:x011_excess -->

And against the asymptotic exponents of the same number of levels.  `c_k` is your
certified upper bound of `τ_k` (workstream Z at your commit `ddc6c32`,
`out_z6_certified_u1_J400.txt`: interval arithmetic; not recomputed by us):
`c_2, …, c_6 = 0.5004, 0.3633, 0.3128, 0.2914, 0.2813` in units of `a`.  Your floating-point values
are `0.500` and `0.361` for two and three levels, so "bound − `c_k`" understates the overhead
over `n·τ_k` itself by at most `0.0023`.

<!-- TABLE:x011_overhead -->
| `n` | 2 levels: bound − `c_2`; in nats | 3 levels: bound − `c_3`; in nats | 4 levels: bound − `c_4`; in nats | 5 levels: bound − `c_5`; in nats |
|---|---|---|---|---|
| 1000 | 0.6380; 71 | 0.7751; 86 | 0.8256; 92 | 0.8470; 94 |
| 1400 | 0.4929; 77 | 0.6026; 94 | 0.6531; 101 | 0.6745; 105 |
| 2000 | 0.3717; 82 | 0.4408; 98 | 0.4831; 107 | 0.5045; 112 |
| 4000 | 0.2258; 100 | 0.2473; 110 | 0.2739; 122 | 0.2906; 129 |
| 8000 | 0.1411; 125 | 0.1626; 144 | 0.1860; 165 | 0.2074*; 184 |
| 16000 | 0.0895; 159 | 0.1149; 204 | 0.1219; 216 | 0.1384*; 246 |
<!-- /TABLE:x011_overhead -->

What one more level gains in the limit, and what the certified designs keep of it (nats;
"share" = realised gain over the gain in the limit):

<!-- TABLE:x011_level_gain -->
| `n` | level 3: gain in the limit, `n a (c_2 − c_3)`; realised; share | level 4: gain in the limit, `n a (c_3 − c_4)`; realised; share | level 5: gain in the limit, `n a (c_4 − c_5)`; realised; share |
|---|---|---|---|
| 1000 | 15; 0; 0.00 | 6; 0; 0.00 | 2; 0; 0.00 |
| 1400 | 21; 4; 0.20 | 8; 0; 0.00 | 3; 0; 0.00 |
| 2000 | 30; 15; 0.50 | 11; 2; 0.16 | 5; 0; 0.00 |
| 4000 | 61; 51; 0.84 | 22; 11; 0.47 | 9; 2; 0.22 |
| 8000 | 122; 103; 0.84 | 45; 24; 0.54 | 19; 0; 0.00 |
| 16000 | 243; 198; 0.81 | 90; 77; 0.86 | 38; 9; 0.23 |
<!-- /TABLE:x011_level_gain -->

The same shares for each family separately at `n = 16 000` — what prediction H13 was about:

<!-- TABLE:x011_h13 -->
| `n` | family | level 3: share kept | level 4 | level 5 | level 6 |
|---|---|---|---|---|---|
| 16000 | theory | 0.81 | 0.37 | 0.20 | 0.00* |
| 16000 | wide | 0.81 | 0.86 | 0.23* | — |
<!-- /TABLE:x011_h13 -->

Reading.  (i) At `n = 1000` no nested run is certified below the base bracket it would
replace: the certified cost of two levels is the best there is.  (ii) **Where the asymptotic
gain goes.**  The overhead of the best design over `n·c_k` grows with every level: by 7 to
45 nats per level at `n = 4000`, `8000` and `16 000`.  A third level gains 61, 122 and 243 nats
in the limit there and keeps four fifths of it; a fourth gains 22, 45 and 90 and keeps
`0.47`, `0.54` and `0.86`; a fifth gains 9, 19 and 38 and keeps `0.22`, nothing and `0.23` (at the
two larger sizes the search of the wider family did not finish, so these are statements
about the designs found).  The reason is arithmetic: `τ_k − h` falls like `1/k²` (your
Theorem 11.53b), so the gain of level `k + 1` in the limit falls like `n a/k³`, while what a
level adds does not fall.  At these sizes the finite-size content of Theorem 11.58a is
therefore "four levels, at most five".  **How much a level keeps depends on the family of
designs as much as on the size**: at `n = 16 000` the wider family keeps `0.86` of the fourth
level's gain and the narrower one `0.37` — we had predicted between `0.40` and `0.80` for
both (H13) and a difference of the two bounds below `0.02` (H3), and both predictions
failed.  The shares are properties of the designs searched, not of the algorithm.  For
comparison, the proof of your Theorem Z (workstream Z, read at `ddc6c32`, not refereed by
us) charges a level `47`–`50` times `ln n` at `u = 1`, that is 390 to 480 nats at these sizes;
the designs minimised here pay 7 to 45.  The two are different objects — a schedule that
works for every large `n`, and a minimum over a finite family at one `n` — but the ratio
says how much room the constants of the proof leave.  (iii) The best
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

*The design with the least certified bound on the grid of ten fractions, family "theory"*
(the finer grid and the wider family of §2 have lower bounds — at `n = 16 000` and four
levels `0.4347` against the `0.4713` of this table; the wider family has not been run on
instances); for it, cone fibres of three more slopes were run:

<!-- TABLE:x011_runs -->
| `n` | levels | selected design: certified bound (outer fraction) | flat instance | worst outer landscape found with flat fibres | with cone fibres of slope `¼u` / `½u` / `¾u` / `u`, base brackets' own answers | (A): base brackets at an end of their promise | largest of these |
|---|---|---|---|---|---|---|---|
| 1000 | 2 | 1.1384 (0.5) | 0.9839 | 1.0109 | — / — / — / 1.0114 | 1.0461 | 1.0461 |
| 1000 | 3 | 1.1384 (0.5) | 0.9839 | 1.0109 | — / — / — / 1.0114 | 1.0454 | 1.0454 |
| 1000 | 4 | 1.1384 (0.5) | 0.9839 | 1.0109 | — / — / — / 1.0114 | 1.0454 | 1.0454 |
| 4000 | 2 | 0.7262 (0.5) | 0.6670 | 0.6826 | — / — / — / 0.6829 | 0.6940 | 0.6940 |
| 4000 | 3 | 0.6214 (0.35) | 0.5410 | 0.5540 | 0.5676 / 0.5411 / 0.5387 / 0.5274 | 0.5714 | 0.5714 |
| 4000 | 4 | 0.5936 (0.3) | 0.4719 | 0.5209 | 0.5422 / 0.5209 / 0.4665 / 0.4740 | 0.5543 | 0.5543 |
| 16000 | 2 | 0.5899 (0.5) | 0.5650 | 0.5749 | — / — / — / 0.5746 | 0.5753 | 0.5753 |
| 16000 | 3 | 0.4782 (0.3) | 0.4237 | 0.4459 | 0.4651 / 0.4629 / 0.4268 / 0.4234 | 0.4651 | 0.4651 |
| 16000 | 4 | 0.4713 (0.15) | 0.4113 | 0.4248 | — / — / — / 0.4066 | 0.4244 | 0.4248 |
<!-- /TABLE:x011_runs -->

Among the fibres tried, the worst for these designs is not the cone of full slope but
the **gentle cone of slope `¼u`**; at `n = 16 000` it reaches exactly what reading (A) gives —
there the "assumed placement" of ENG-RES-0014 is the algorithm's own answer on a real
instance.

*Minimised over the fractions*, which is how ENG-RES-0014 reported the flat-tuned design
(right-hand columns, from its artifacts; fibres flat or cones of full slope on both
sides):

<!-- TABLE:x011_runs_min -->
| `n` | levels | servers by certified cost, least over ten fractions: (B) | (A) | servers chosen at the flat fibre (ENG-RES-0014), least over its fractions: flat instance | (B) | (A) |
|---|---|---|---|---|---|---|
| 1000 | 2 | 1.0114 (0.5) | 1.0461 (0.5) | 0.6937 | 1.0114 | 1.0461 |
| 1000 | 3 | 1.0060 (0.45) | 1.0224 (0.45) | 0.6937 | 0.9494 | 0.9633 |
| 4000 | 2 | 0.6829 (0.5) | 0.6940 (0.5) | 0.5519 | 0.6829 | 0.6940 |
| 4000 | 3 | 0.5540 (0.35) | 0.5714 (0.35) | 0.4530 | 0.6249 | 0.6826 |
| 16000 | 2 | 0.5749 (0.5) | 0.5753 (0.5) | 0.5126 | 0.5749 | 0.5753 |
| 16000 | 3 | 0.4459 (0.3) | 0.4581 (0.25) | 0.3893 | 0.5525 | — |
<!-- /TABLE:x011_runs_min -->

<!-- TABLE:x011_h4 -->
Three levels, `n = 4000`: least worst instance found `0.5540` (B), `0.5714` (A) for servers chosen by certified cost, against `0.6249` (B), `0.6826` (A) for servers chosen at the flat fibre; with the 3 further fibre slopes the selected design reaches `0.5676` (B), `0.5714` (A); at the flat instance `0.5410` against `0.4530`; `n = 16000`: least worst instance found `0.4459` (B), `0.4581` (A) for servers chosen by certified cost, against `0.5525` (B) (reading (A) was not run for it) for servers chosen at the flat fibre; with the 3 further fibre slopes the selected design reaches `0.4651` (B), `0.4651` (A); at the flat instance `0.4237` against `0.3893`.
<!-- /TABLE:x011_h4 -->

So the answer to "does tuning against the worst case improve on tuning at the flat
instance" is, at `n = 4000` and `16 000`: **yes on every non-flat instance we built — for three
levels by `0.06`–`0.11` in these units — and no at the flat instance itself, by `0.03`–`0.09`**;
and at `n = 16 000` four levels chosen by certified cost are below the flat-tuned three
levels even there (§5).  **At `n = 1000` it is no**: there the rule of certified cost finds
almost no nested run worth certifying (its three-level bound is its two-level bound),
the flat-tuned design nests anyway, and its worst instance found is lower — `0.9494`
against `1.0060` in reading (B), `0.9633` against `1.0224` in (A) — with a certified bound
that is higher.  §6a finds the same at `u = ½`, `n = 4000`, which is the same size in nats.

Consistency and tightness:

<!-- TABLE:x011_consistency -->
108 designs run, 828 searches, 2,015,244 mean runs: 0 searched costs above the certified bound of their design; 0 runs with a violated claim of Theorem 11.56; 0 searches with a nested run that did not close on its fibre.  The smallest distance between a bound and the worst instance found is `0.0019` (`n = 64000`, 2 levels, outer fraction `0.4`).
<!-- /TABLE:x011_consistency -->

<!-- TABLE:x011_tightness -->
| `n` | levels | certified bound of the selected design | worst instance found, (A) | bound minus worst found | worst found / flat instance: (B), (A) |
|---|---|---|---|---|---|
| 1000 | 2 | 1.1384 (0.5) | 1.0461 | 0.0923 | 1.028, 1.063 |
| 1000 | 3 | 1.1384 (0.5) | 1.0454 | 0.0930 | 1.028, 1.063 |
| 1000 | 4 | 1.1384 (0.5) | 1.0454 | 0.0930 | 1.028, 1.063 |
| 4000 | 2 | 0.7262 (0.5) | 0.6940 | 0.0322 | 1.024, 1.040 |
| 4000 | 3 | 0.6214 (0.35) | 0.5714 | 0.0500 | 1.049, 1.056 |
| 4000 | 4 | 0.5936 (0.3) | 0.5543 | 0.0392 | 1.149, 1.175 |
| 8000 | 2 | 0.6415 (0.5) | 0.6188 | 0.0227 | 1.020, 1.025 |
| 16000 | 2 | 0.5899 (0.5) | 0.5753 | 0.0146 | 1.018, 1.018 |
| 16000 | 3 | 0.4782 (0.3) | 0.4651 | 0.0132 | 1.098, 1.098 |
| 16000 | 4 | 0.4713 (0.15) | 0.4248 | 0.0465 | 1.033, 1.033 |
| 32000 | 2 | 0.5646 (0.5) | 0.5560 | 0.0086 | 1.015, 1.028 |
| 64000 | 2 | 0.5407 (0.5) | 0.5353 | 0.0053 | 1.012, 1.016 |
<!-- /TABLE:x011_tightness -->

For two levels the certified bound is nearly attained from `n = 4000` on: the worst
instance found is within `0.033` of it there, `0.023` at `8000` and `0.006` at `64 000` (`0.09` at
`n = 1000`).  For three levels `0.05` and `0.013` remain at `n = 4000` and `16 000`.

The flat instance is not the best case of these designs:

<!-- TABLE:x011_reversal -->
Of the 54 designs with at least one nested run, 18 cost **less on cone fibres than at the flat instance** whatever outer landscape the search tried (largest difference `0.0661` at `n = 1000`, 3 levels, outer fraction `0.25`: flat instance `1.0798`, worst found with cone fibres `1.0137`); of the 36 two-level designs, 0.
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
| rung | accuracy | server | its cost: flat fibre / cone fibre / certified | share of the promised width used: flat / cone | calls × cost at this rung: flat fibres / cone fibres |
|---|---|---|---|---|---|
| 1 | 3.82e+03 | K0 | 0.022 / 0.022 / 0.022 | 0.12 / 0.12 | 0.333 / 0.333 |
| 4 | 1.92e+03 | K0 | 0.022 / 0.022 / 0.022 | 0.24 / 0.24 | 0.333 / 0.333 |
| 7 | 965 | K0 | 0.022 / 0.022 / 0.022 | 0.48 / 0.48 | 0.333 / 0.333 |
| 10 | 485 | K0 | 0.022 / 0.022 / 0.022 | 0.96 / 0.96 | 0.333 / 0.333 |
| 13 | 244 | K0 | 0.031 / 0.031 / 0.031 | 0.97 / 0.99 | 0.342 / 0.136 |
| 16 | 123 | K0 | 0.111 / 0.111 / 0.111 | 0.66 / 0.98 | 0.422 / 0.169 |
| 19 | 61.6 | 2L+ extensive | 0.164 / 0.166 / 0.270 | 1.00 / 1.00 | 0.384 / 0.220 |
| 22 | 31 | 2L+ extensive | 0.197 / 0.344 / 0.442 | 0.98 / 0.99 | 0.332 / 0.399 |
| 25 | 15.6 | 2L+ extensive | 0.211 / 0.459 / 0.624 | 0.94 / 0.97 | 0.302 / 0.513 |
| 28 | 7.83 | 2L+ bounded | 0.291 / 0.301 / 0.501 | 0.60 / 0.34 | 0.360 / 0.355 |
| 31 | 3.94 | 2L+ bounded | 0.299 / 0.403 / 0.500 | 0.69 / 0.42 | 0.355 / 0.458 |
| 34 | 1.98 | 2L+ bounded | 0.405 / 0.444 / 0.513 | 0.71 / 0.46 | 0.458 / 0.496 |
| 36 | 1.25 | 2L+ bounded | 0.418 / 0.456 / 0.521 | 0.72 / 0.46 | 0.471 / 0.509 |
| 37 | 0.995 | 2L+ bounded | 0.425 / 0.462 / 0.527 | 0.72 / 0.46 | **0.478** / — |
| 38 | 0.791 | 2L+ bounded | 0.431 / 0.468 / 0.531 | 0.73 / 0.46 | 0.454 / — |
| 39 | 0.629 | 2L+ bounded | 0.438 / 0.473 / 0.535 | 0.73 / 0.45 | — / — |
| 40 | 0.5 | 2L+ bounded | 0.442 / 0.477 / 0.540 | 0.73 / 0.45 | — / — |
<!-- /TABLE:x011_rungs_flat -->

<!-- TABLE:x011_rungs_flat_caption -->
`u = 1`, `n = 4000`, three levels, servers chosen at the flat fibre, outer fraction `0.4`; flat outer landscape; in units of `n a`.  Whole run: `0.4780` with flat fibres, `0.6213` with cone fibres; certified bound `0.8094`.  A dash: the rung is not reached.  Bold: the largest term.
<!-- /TABLE:x011_rungs_flat_caption -->

*Servers chosen by certified cost:*

<!-- TABLE:x011_rungs_cert -->
| rung | accuracy | server | its cost: flat fibre / cone fibre / certified | share of the promised width used: flat / cone | calls × cost at this rung: flat fibres / cone fibres |
|---|---|---|---|---|---|
| 1 | 4.13e+03 | K0 | 0.022 / 0.022 / 0.022 | 0.12 / 0.12 | 0.292 / 0.292 |
| 4 | 2.06e+03 | K0 | 0.022 / 0.022 / 0.022 | 0.24 / 0.24 | 0.292 / 0.292 |
| 7 | 1.03e+03 | K0 | 0.022 / 0.022 / 0.022 | 0.48 / 0.48 | 0.292 / 0.292 |
| 10 | 515 | K0 | 0.022 / 0.022 / 0.022 | 0.97 / 0.97 | 0.292 / 0.292 |
| 13 | 257 | K0 | 0.033 / 0.033 / 0.033 | 0.97 / 0.99 | 0.303 / 0.132 |
| 16 | 129 | K0 | 0.122 / 0.122 / 0.122 | 0.64 / 0.98 | 0.392 / 0.180 |
| 19 | 64.3 | K0 | 0.244 / 0.244 / 0.244 | 0.02 / 0.97 | 0.297 / 0.299 |
| 22 | 32.1 | K0 | 0.367 / 0.367 / 0.367 | 0.03 / 0.90 | 0.420 / 0.422 |
| 25 | 16 | 2L+ bounded | 0.255 / 0.302 / 0.419 | 0.97 / 0.83 | 0.308 / 0.355 |
| 28 | 8.02 | 2L+ bounded | 0.283 / 0.315 / 0.461 | 0.94 / 0.70 | 0.336 / 0.368 |
| 31 | 4.01 | 2L+ bounded | 0.309 / 0.374 / 0.495 | 0.88 / 0.50 | 0.362 / 0.427 |
| 34 | 2 | 2L+ bounded | 0.302 / 0.432 / 0.507 | 0.86 / 0.58 | 0.355 / 0.485 |
| 36 | 1.26 | 2L+ bounded | 0.472 / 0.457 / 0.516 | 0.85 / 0.54 | 0.525 / 0.510 |
| 37 | 1 | 2L+ bounded | 0.481 / 0.467 / 0.523 | 0.84 / 0.51 | 0.534 / **0.520** |
| 38 | 0.794 | 2L+ bounded | 0.488 / 0.474 / 0.530 | 0.84 / 0.52 | **0.541** / — |
| 39 | 0.63 | 2L+ bounded | 0.494 / 0.480 / 0.535 | 0.83 / 0.51 | 0.517 / — |
| 40 | 0.5 | 2L+ bounded | 0.501 / 0.485 / 0.543 | 0.83 / 0.51 | — / — |
<!-- /TABLE:x011_rungs_cert -->

<!-- TABLE:x011_rungs_cert_caption -->
`u = 1`, `n = 4000`, three levels, servers chosen by certified cost, outer fraction `0.35`; flat outer landscape; in units of `n a`.  Whole run: `0.5410` with flat fibres, `0.5196` with cone fibres; certified bound `0.6214`.  A dash: the rung is not reached.  Bold: the largest term.
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
| `n` | designs | at the flat instance: least cost | on the worst cone, the best single design (min–max) | which, and its worst slope | worst cone for a portfolio (max–min), and its slope | cost of dovetailing, `ln(4·designs)/(n a)` |
|---|---|---|---|---|---|---|
| 1000 | three levels, servers chosen at the flat fibre (14) | 0.6937 | 0.9049 | phi=0.45; slope 0 | 0.8542 at slope 0.9 | 0.0363 |
| 1000 | three levels, servers by certified cost (14) | 0.6937 | 0.9816 | phi=0.55; slope 0.9 | 0.9365 at slope 0.9 | 0.0363 |
| 1000 | two to four levels, by certified cost (42) | 0.6937 | 0.9816 | phi=0.55, 2 levels; slope 0.9 | 0.9365 at slope 0.9 | 0.0462 |
| 1000 | all of these (56) | 0.6937 | 0.9049 | phi=0.45, three levels; slope 0 | 0.8542 at slope 0.9 | 0.0488 |
| 4000 | three levels, servers chosen at the flat fibre (14) | 0.4530 | 0.6048 | phi=0.4; slope 1 | 0.6048 at slope 1 | 0.0091 |
| 4000 | three levels, servers by certified cost (14) | 0.4611 | 0.5410 | phi=0.35; slope 0 | 0.5141 at slope 0.9 | 0.0091 |
| 4000 | two to four levels, by certified cost (42) | 0.4293 | 0.4781 | phi=0.3, 4 levels; slope 0.4 | 0.4487 at slope 1 | 0.0115 |
| 4000 | all of these (56) | 0.4293 | 0.4781 | phi=0.3, 4 levels; slope 0.4 | 0.4487 at slope 1 | 0.0122 |
| 16000 | three levels, servers chosen at the flat fibre (14) | 0.3893 | 0.5468 | phi=0.45; slope 1 | 0.5468 at slope 1 | 0.0023 |
| 16000 | three levels, servers by certified cost (14) | 0.3980 | 0.4237 | phi=0.3; slope 0 | 0.4204 at slope 0.3 | 0.0023 |
| 16000 | two to four levels, by certified cost (42) | 0.3856 | 0.3856 | phi=0.2, 4 levels; slope 0 | 0.3856 at slope 0 | 0.0029 |
| 16000 | all of these (56) | 0.3856 | 0.3856 | phi=0.2, 4 levels; slope 0 | 0.3856 at slope 0 | 0.0030 |
<!-- /TABLE:x011_cones -->

<!-- TABLE:x011_cones_caption -->
Global cones `ψ(x) = s·u·|x|`, `u = 1`; mean-run model; base brackets give their own answers; 56 designs per size (14 outer fractions; flat-tuned three levels, and two, three and four levels by certified cost in the family "theory"); every run closed with no violated claim.
<!-- /TABLE:x011_cones_caption -->

The least cost over the 14 outer fractions, slope by slope, three levels:

<!-- TABLE:x011_cone_profiles -->
| `n` | rule | slope 0 | slope 0.02 | slope 0.05 | slope 0.1 | slope 0.15 | slope 0.2 | slope 0.3 | slope 0.4 | slope 0.5 | slope 0.6 | slope 0.7 | slope 0.8 | slope 0.9 | slope 1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1000 | chosen at the flat fibre | 0.694 | 0.663 | 0.650 | 0.646 | 0.649 | 0.651 | 0.653 | 0.670 | 0.712 | 0.754 | 0.786 | 0.812 | 0.854 | 0.829 |
| 1000 | by certified cost | 0.694 | 0.676 | 0.676 | 0.676 | 0.676 | 0.675 | 0.675 | 0.684 | 0.742 | 0.791 | 0.838 | 0.890 | 0.937 | 0.935 |
| 4000 | chosen at the flat fibre | 0.453 | 0.433 | 0.442 | 0.450 | 0.449 | 0.452 | 0.449 | 0.436 | 0.426 | 0.426 | 0.477 | 0.510 | 0.568 | 0.605 |
| 4000 | by certified cost | 0.461 | 0.453 | 0.454 | 0.457 | 0.457 | 0.456 | 0.455 | 0.440 | 0.434 | 0.432 | 0.461 | 0.489 | 0.514 | 0.509 |
| 16000 | chosen at the flat fibre | 0.389 | 0.380 | 0.383 | 0.383 | 0.383 | 0.382 | 0.382 | 0.386 | 0.396 | 0.402 | 0.440 | 0.450 | 0.510 | 0.547 |
| 16000 | by certified cost | 0.398 | 0.395 | 0.396 | 0.396 | 0.407 | 0.420 | 0.420 | 0.415 | 0.392 | 0.366 | 0.366 | 0.371 | 0.395 | 0.406 |
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
| `n` | outer fraction | certified bound of two levels | flat instance | worst instance found, cone fibres with the base brackets' own answers | any fibre, base brackets at an end of their promise |
|---|---|---|---|---|---|
| 8000 | 0.65 | 0.8032 | 0.5663 | 0.7768 | 0.7770 |
| 8000 | 0.6 | 0.7489 | 0.5204 | 0.7205 | 0.7231 |
| 8000 | 0.55 | 0.6948 | 0.5467 | 0.6682 | 0.6684 |
| 8000 | 0.5 | 0.6415 | 0.6039 | 0.6158 | 0.6188 |
| 8000 | 0.45 | 0.6847 | 0.6556 | 0.6634 | 0.6717 |
| 8000 | 0.4 | 0.7387 | 0.7084 | 0.7161 | 0.7256 |
| 32000 | 0.65 | 0.7147 | 0.5944 | 0.7045 | 0.7052 |
| 32000 | 0.6 | 0.6626 | 0.5486 | 0.6528 | 0.6534 |
| 32000 | 0.55 | 0.6105 | 0.5053 | 0.6012 | 0.6013 |
| 32000 | 0.5 | 0.5646 | 0.5407 | 0.5489 | 0.5560 |
| 32000 | 0.45 | 0.6034 | 0.5922 | 0.5950 | 0.5997 |
| 32000 | 0.4 | 0.6551 | 0.6433 | 0.6461 | 0.6515 |
| 64000 | 0.65 | 0.6930 | 0.6084 | 0.6872 | 0.6872 |
| 64000 | 0.6 | 0.6416 | 0.5599 | 0.6357 | 0.6360 |
| 64000 | 0.55 | 0.5913 | 0.5136 | 0.5846 | 0.5846 |
| 64000 | 0.5 | 0.5407 | 0.5267 | 0.5332 | 0.5353 |
| 64000 | 0.45 | 0.5845 | 0.5776 | 0.5809 | 0.5826 |
| 64000 | 0.4 | 0.6357 | 0.6283 | 0.6319 | 0.6338 |
<!-- /TABLE:x011_r16 -->

Minimised over the outer fraction:

<!-- TABLE:x011_r16_summary -->
`n = 8000` (6 of 6 fractions): `0.6158` at `0.5` with the base brackets' own answers, `0.6188` at `0.5` with any valid placement; `n = 32000` (6 of 6 fractions): `0.5489` at `0.5` with the base brackets' own answers, `0.5560` at `0.5` with any valid placement; `n = 64000` (6 of 6 fractions): `0.5332` at `0.5` with the base brackets' own answers, `0.5353` at `0.5` with any valid placement.
<!-- /TABLE:x011_r16_summary -->

Your expectation was "within `0.006` of `0.619`, `0.550`, `0.537`" (ENG-RES-0008, the other
ladder) and "far above the certified three-level bounds `0.5262`, `0.4439`, `0.4341`".  Both
hold (the second size at exactly `0.006`).

## 6a. Other slopes, and both rules of design run by the same code **[N]** (stage 2; `n = 4000`)

Stage 1 compared our certified-cost designs with the flat-tuned numbers of ENG-RES-0014,
which came from other code and fewer fibres.  Stage 2 (job M-020, hypotheses H9–H11
written before it) builds *both* kinds of design in one code path and runs them on the
same instances — the flat instance; the worst outer landscape found with flat fibres and
with cone fibres of slope `¼u`, `½u`, `u`; reading (A) — at `u = ½, 1, 2`.  This message has
`n = 4000` for the three slopes and `n = 16 000` for `u = ½` and `u = 1`; at `u = 2`, `n = 16 000` only
two of the twelve fractions of the flat-tuned design had finished, and that cell follows
with the addendum.

<!-- TABLE:x011_stage2 -->
| `u` | `n` | design | fractions run | least certified bound (fraction) | least cost at the flat instance (fraction) | least worst instance found, (B) (fraction; the fibre that is worst there) | (A) (fraction) |
|---|---|---|---|---|---|---|---|
| 0.5 | 4000 | two levels | 12 | 1.0509 (0.5) | 0.6656 (0.8) | 0.9387 (0.5; cone `u`) | 0.9546 (0.5) |
| 0.5 | 4000 | three levels, by certified cost | 12 | 1.0509 (0.5) | 0.6656 (0.8) | 0.9020 (0.4; flat) | 0.9331 (0.4) |
| 0.5 | 4000 | four levels, by certified cost | 12 | 1.0509 (0.5) | 0.6656 (0.8) | 0.9020 (0.4; flat) | 0.9331 (0.4) |
| 0.5 | 4000 | three levels, chosen at the flat fibre | 12 | 1.0718 (0.5) | 0.6656 (0.8) | 0.8629 (0.45; flat) | 0.8647 (0.45) |
| 0.5 | 16000 | two levels | 12 | 0.6930 (0.5) | 0.5300 (0.6) | 0.6567 (0.5; flat) | 0.6574 (0.5) |
| 0.5 | 16000 | three levels, by certified cost | 12 | 0.5861 (0.35) | 0.4330 (0.5) | 0.5259 (0.35; cone `¼u`) | 0.5319 (0.35) |
| 0.5 | 16000 | four levels, by certified cost | 12 | 0.5561 (0.3) | 0.4098 (0.4) | 0.5144 (0.3; cone `¼u`) | 0.5147 (0.3) |
| 0.5 | 16000 | three levels, chosen at the flat fibre | 12 | 0.6871 (0.45) | 0.4210 (0.45) | 0.5750 (0.4; cone `u`) | 0.6106 (0.45) |
| 1 | 4000 | two levels | 12 | 0.7262 (0.5) | 0.5592 (0.6) | 0.6829 (0.5; cone `u`) | 0.6940 (0.5) |
| 1 | 4000 | three levels, by certified cost | 12 | 0.6214 (0.35) | 0.4611 (0.5) | 0.5676 (0.35; cone `¼u`) | 0.5714 (0.35) |
| 1 | 4000 | four levels, by certified cost | 12 | 0.5936 (0.3) | 0.4293 (0.45) | 0.5242 (0.25; cone `½u`) | 0.5465 (0.25) |
| 1 | 4000 | three levels, chosen at the flat fibre | 12 | 0.7261 (0.5) | 0.4530 (0.45) | 0.6249 (0.4; cone `u`) | 0.6635 (0.45) |
| 1 | 16000 | two levels | 11 | 0.5899 (0.5) | 0.5126 (0.55) | 0.5749 (0.5; cone `¼u`) | 0.5753 (0.5) |
| 1 | 16000 | three levels, by certified cost | 12 | 0.4782 (0.3) | 0.3980 (0.35) | 0.4556 (0.25; flat) | 0.4581 (0.25) |
| 1 | 16000 | four levels, by certified cost | 12 | 0.4713 (0.15) | 0.3856 (0.2) | 0.4221 (0.2; flat) | 0.4221 (0.2) |
| 1 | 16000 | three levels, chosen at the flat fibre | 12 | 0.5899 (0.5) | 0.3893 (0.3) | 0.5525 (0.45; cone `u`) | 0.5749 (0.5) |
| 2 | 4000 | two levels | 12 | 0.6230 (0.5) | 0.5420 (0.55) | 0.6008 (0.5; cone `½u`) | 0.6067 (0.5) |
| 2 | 4000 | three levels, by certified cost | 12 | 0.5308 (0.25) | 0.4324 (0.35) | 0.4919 (0.25; flat) | 0.4919 (0.25) |
| 2 | 4000 | four levels, by certified cost | 12 | 0.5257 (0.2) | 0.4277 (0.2) | 0.4660 (0.25; cone `¼u`) | 0.4660 (0.25) |
| 2 | 4000 | three levels, chosen at the flat fibre | 12 | 0.6230 (0.5) | 0.4223 (0.3) | 0.5882 (0.45; cone `u`) | 0.5998 (0.5) |
<!-- /TABLE:x011_stage2 -->

"(B)": the largest over flat fibres and the three cone slopes, base brackets' own
answers.  Every column is minimised over the fractions run (twelve, except eleven for
two levels at `u = 1`, `n = 16 000`) separately.

<!-- TABLE:x011_stage2_caption -->
Units `n a` with `a = a(u)`; the size in nats: `u = 0.5`, `n = 4000`: `n a = 121`, `u = 0.5`, `n = 16000`: `n a = 485`, `u = 1`, `n = 4000`: `n a = 444`, `u = 1`, `n = 16000`: `n a = 1775`, `u = 2`, `n = 4000`: `n a = 1311`.  For comparison, `u = 1`: `n a = 111` at `n = 1000`, `444` at `4000`, `1775` at `16 000`.
<!-- /TABLE:x011_stage2_caption -->

<!-- TABLE:x011_h9 -->
Three levels, servers by certified cost against servers chosen at the flat fibre (least worst instance found over the fractions): `u = 0.5`, `n = 4000`: `0.9020` against `0.8629` in reading (B), `0.9331` against `0.8647` in (A); at the flat instance `0.6656` against `0.6656`; `u = 0.5`, `n = 16000`: `0.5259` against `0.5750` in reading (B), `0.5319` against `0.6106` in (A); at the flat instance `0.4330` against `0.4210`; `u = 1`, `n = 4000`: `0.5676` against `0.6249` in reading (B), `0.5714` against `0.6635` in (A); at the flat instance `0.4611` against `0.4530`; `u = 1`, `n = 16000`: `0.4556` against `0.5525` in reading (B), `0.4581` against `0.5749` in (A); at the flat instance `0.3980` against `0.3893`; `u = 2`, `n = 4000`: `0.4919` against `0.5882` in reading (B), `0.4919` against `0.5998` in (A); at the flat instance `0.4324` against `0.4223`.  H9 fails at `u = 0.5`, `n = 4000`.
<!-- /TABLE:x011_h9 -->

<!-- TABLE:x011_h11 -->
Which fibre is the worst (designs with at least one nested run; one count per design and fraction): by certified cost: flat 60, `¼u` 34, `½u` 16; chosen at the flat fibre: flat 28, `¼u` 2, `½u` 2, `u` 28.
<!-- /TABLE:x011_h11 -->

<!-- TABLE:x011_stage2_consistency -->
239 designs run, 2868 searches, 7,054,884 mean runs: 0 searched costs above the certified bound of their design; 0 runs with a violated claim.
<!-- /TABLE:x011_stage2_consistency -->

Three things to take from it.

1. **Replication (H10).**  At `u = 1` the flat-tuned design run by the new code gives the
   numbers of ENG-RES-0014 for the flat instance and for cone fibres of full slope to the
   digit, at both sizes (`0.4530`, `0.6249`; `0.3893`, `0.5525`).  Reading (A) at `n = 4000` is lower
   here because stage 2 places the base brackets on cones of full slope only.
2. **The answer depends on the size in nats (H9 is refuted at `u = ½`).**  At `u = 1` and
   `u = 2` servers chosen by certified cost have the smaller worst instance found.  At
   `u = ½` and this size they do not: hardly any nested run is *certified* below the base
   bracket it would replace, so the certified-cost design stays close to two levels, while
   the flat-tuned design nests anyway and its worst instance found is lower — with a
   certified bound that is higher.  The same happens at `u = 1`, `n = 1000` (§3, second
   table, first rows), and the two cases have the same size in nats, `n a ≈ 110`–`120`: what
   decides is not the slope but whether the problem is large enough for a nested run to
   pay its fixed costs *with a certificate*.  The larger size confirms it for the slope
   at which the rule had lost: at `u = ½`, `n = 16 000` (`n a = 485`) the design chosen by
   certified cost is ahead, `0.5259` against `0.5750`; so the crossover lies between 121 and
   485 nats at `u = ½` and between 111 and 444 at `u = 1` (prediction H14, which holds at
   `u = 1` and is pending at `u = 2`).  Below that size a design can be better on
   every instance anyone has found and worse in what it guarantees; which of the two one
   wants is not a mathematical question, and the portfolio of §5 has both.
3. **Which fibre is worst (H11 was too simple).**  For designs chosen by certified cost it
   is never the cone of full slope: flat fibres at most fractions, gentle cones at the
   others.  For the flat-tuned design it is the flat fibre or the full cone in all but
   four cases.

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
| blocks (top outer, middle outer, base) and their slopes | runs | closed | final bracket misses the truth | wider than certified | aborted | nested runs | of them aborted / missing their truth / too wide | widest bracket (certified accuracy) | `ln` queries: made / theorem's count / nested bound |
|---|---|---|---|---|---|---|---|---|---|
| (7, 5, 3) sites, slopes (1.0, 0.5, 2.0) | 320 | 320 | 0 | 0 | 0 | 142,746 | 0 / 0 / 0 | 4.532 (4.818) | 11.9 / 17.5 / 40.3 |
| (7, 5, 3) sites, slopes (0.5, 2.0, 1.0) | 320 | 320 | 0 | 0 | 0 | 156,266 | 0 / 0 / 0 | 4.364 (4.818) | 11.9 / 15.8 / 40.4 |
| (8, 4, 3) sites, slopes (2.0, 1.0, 0.5) | 320 | 320 | 0 | 0 | 0 | 259,977 | 0 / 0 / 0 | 4.655 (4.818) | 11.6 / 17.4 / 42.2 |
| (6, 6, 3) sites, slopes (1.0, 2.0, 0.4) | 320 | 320 | 0 | 0 | 0 | 81,878 | 0 / 0 / 0 | 4.538 (4.818) | 11.7 / 17.1 / 42.7 |
<!-- /TABLE:x011_nested_literal -->

<!-- TABLE:x011_nested_literal_summary -->
1,280 end-to-end runs of three nested levels (160 tasks, eight kinds of energy table): 1,280 closed, 0 final brackets that miss the truth, 0 wider than certified, 0 aborted, 0 above the nested cost bound; 640,867 real nested runs, of which 0 aborted, 0 returned a bracket that misses its fibre average and 0 one wider than certified.
<!-- /TABLE:x011_nested_literal_summary -->

A correction of a label, from our referee of ENG-RES-0016: the column "theorem's count"
is the top level's count with every middle run charged the queries it made *with
sharing*; with the middle runs charged their own theorem's count it is 4 to 7 nats
higher (`19.2` against `12.3` and `20.8` against `15.9` on the referee's instances, where the
nested bound is 36 to 39).  "Within the nested bound" holds for either count.  The same
referee ran 3 744 end-to-end three-level runs with a simulator of its own: nothing
invalid, too wide or aborted.  Our simulator of this section compared bracket ends with
levels in plain floating point (no tie rule); no run aborted on the instances drawn,
and ENG-RES-0016 §6 says on which instances a two-level simulator without the rule does.

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
* **The outer search is the one of X-005, and the science division's review SCI-REV-0018
  has since shown what it misses** (finding M1; our check and correction: ENG-RES-0017):
  its starting points do not include a reference point placed behind a ramp in a shell
  of negligible probability, and at `n ≤ 500` product instances of that kind cost up to
  `0.02` more than the worst the search had found.  At `n ≥ 1000` the shortfall measured
  there is at most `0.0007`; the searches of this message have not been repeated with
  the added starting points, so every "worst instance found" here may be low by an
  amount of that order.  No statement of this message rests on a searched number being
  a maximum.
* One accuracy, one failure probability; a fixed top level; finite design families ("the
  best certified bound" is a minimum over those families).  The designs *run* on
  instances (§§3–6a) are those of the family "theory" on grids of ten to fourteen outer
  fractions; the wider family, whose certified bounds are lower from `n = 8000` on, has
  not been run.  The shares of §2 are properties of the families searched.
* Proposition P is ours and unrefereed.

## 9. Requests (proposals; none is an authorisation)

1. **To the theory division:** if the reading of §4 is right, remark (1) of §11.19 could say
   which middle design the flat-instance figures rest on.  And a question: is there a
   reason, in the proof of Theorem 11.56, why the bounded design should use *less* of its
   width on a cone than on a flat fibre?
2. **To the science division:** Proposition P is short and nobody but its author has read
   it; your literal loop of R18 could run a portfolio of two designs as its test.
3. **To both:** fibres that are hard for the bounded design are the next thing to search
   for.  A candidate family from either of you would be welcome.

## Reproduction

    python experiments/eng/twolevel/nested_bench.py --check                         # published numbers
    python -m pytest tests/eng/test_certified.py -q
    modal run --detach modal_jobs/bench_app.py::launch --driver nested_bench --job certified1+instances1 --ledger M-016+M-017
    modal run --detach modal_jobs/bench_app.py::launch --driver nested_bench --job instances2+certified2 --ledger M-020+M-021
    modal run --detach modal_jobs/bench_app.py::launch --driver nested_literal --job nested1 --ledger M-019
    python modal_jobs/bench_collect.py --driver nested_bench --job certified1+instances1+instances2+certified2
    python experiments/eng/twolevel/portfolio.py ; python experiments/eng/twolevel/rung_anatomy.py
    python experiments/eng/twolevel/make_tables_x011.py --verify docs/collaboration/responses/engineering/ENG-RES-0015.md

Artifacts: `experiments/eng/twolevel/results/x011_*.jsonl|json`, `x011f_nested1.jsonl`; costs:
`docs/engineering/COMPUTE_LEDGER.md`, M-015 … M-021.  The tables of this message use the rows
that were stored when it was published (`results/x011_published_rows.json`); `--verify` keeps
doing so while the detached jobs append further rows, which go to the addendum.
