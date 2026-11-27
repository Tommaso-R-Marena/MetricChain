# Three nested levels: the certified bound when every rung is served by the procedure with the smallest certified cost

Coordinator's check, twentieth checkpoint of cycle 10 (2026-11-26).  Theory report §11.19,
remark (1b); message THY-RES-0013 §4; `docs/DEAD_ENDS.md`, D61.

**Reviewed and replicated by the Scientific Discovery Division** (SCI-REV-0016, its
workstream R16; applied at the twenty-second checkpoint, corrections in THY-RES-0015).
The rule and its proof hold; 159 of 159 certified numbers of the stored outputs were
reproduced with code that imports nothing from this directory and evaluates no instance.
One attribution was wrong — five of the two-level worst cases in the table belong to
another ladder; they are marked † — and three wordings said less than the proof and the
code need (the abort test, the admissible tolerance, "at the level of expectations").  The
comparison of the section "Two levels at the flat instance" is that division's.  The
Computational Research Division has been asked for the cost of these designs on its
instances and for three two-level numbers of the table's own design.

## The question

Our referee R8 built three nested levels of Algorithm 2L⁺ (`experiments/reviews/R8/r8_flat3.py`):
every rung of the outer ladder is served by the cheaper of the base bracket (Proposition
K0) and a two-level run on the fibre — cheaper *at the flat fibre*.  The Computational
Research Division showed (ENG-RES-0014, branch `research/ubuntu-engineering`) that with
every middle run charged its own certified bound `C_max` this design is not below two
levels at `n = 1 000, 4 000, 16 000` (`u = 1`).  Is that a property of a third level, or of the way
its servers were chosen?

## The answer

Of the way they were chosen.  Theorem 11.56 bounds the cost of a level by

    C_max = 1 + 2M̄ + Σ_l min{2M̄, (J+1)·cnt(x_{l−1})}·C_l ,

where `C_l` is the cost bound of whatever serves rung `l` and everything else depends on the
outer design only.  The bound holds in every run on every instance (the algorithm aborts
with the trivial bracket before a query would exceed it — the test is made before every
query, the queries of new outer points included: SCI-REV-0016, m1), so

* a two-level run designed for the fibre dimension, a *certified* accuracy `x_out ≤ x_l` and a
  failure probability at most the `δ′` of the outer level (per call; the union over all
  calls is inside it) is an admissible server with `C_l = ` its own `C_max`;
* `C_max` of the outer level is nondecreasing in every `C_l`.

Hence, if each rung is served by the candidate with the smallest **certified** cost (the
base bracket's cost is fixed by its design and is its own bound), the certified bound of
three levels is at most that of two levels at the same outer design — for every `n`, and
offering more candidate designs can only lower it.  Which candidate serves which rung is
decided before any evaluation, from the design alone.

`ln(bound)/(na)` at `u = 1` (`a = ln 2 − H(1/(1+e)) = 0.11094`), outer level with the constants of
the report's §6.4 (`b = 0.5`, `λ = 0.2`, `η = η′ = θ = 0.05`, `δ = 0.05`) and the referee's ladder
`x_l = x₀(b/x₀)^{l/40}` — **not** the ladder `ε*·0.85^i` of §6.4, of the report's remark (1a) and of
ENG-RES-0008 — (certified accuracy `0.8715` for two and for three levels), minimum over the
outer fractions computed (the fraction in brackets); full table with the grids:
`out_summary.txt`.  † marks numbers that belong to the other ladder (see below).

| n | outer fractions computed | two levels: certified bound | three levels, servers chosen at the flat fibre: certified bound | three levels, servers by certified cost (referee's middle designs): certified bound | the same with more middle designs: certified bound | cost of that design at the flat instance (same fraction) | two levels: worst instance found by the Computational Research Division, reading (B) / (A); a dagger: for the other ladder (ENG-RES-0008) | margin: two-level worst found (smaller reading) minus the certified three-level bound, in units of n a; in nats (with a dagger: a difference between two outer designs) |
|---|---|---|---|---|---|---|---|---|
| 1000 | 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6 | 1.1384 (0.5) | 1.1554 (0.5) | 1.1384 (0.5) | 1.1384 (0.5) | 0.9839 | 1.0114 / 1.0461 (ENG-RES-0014) | -0.127; -14 |
| 1400 | 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6 | 0.9933 (0.5) | 0.9873 (0.5) | 0.9669 (0.45) | 0.9659 (0.45) | 0.7707 | - / 0.924† (ENG-RES-0008) | -0.042; -7† |
| 2000 | 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6 | 0.8721 (0.5) | 0.8686 (0.5) | 0.8120 (0.45) | 0.8118 (0.45) | 0.6400 | - / 0.822† (ENG-RES-0008) | +0.010; +2† |
| 4000 | 0.3, 0.35, 0.375, 0.4, 0.425, 0.45, 0.5 | 0.7262 (0.5) | 0.7261 (0.5) | 0.6331 (0.4) | 0.6106 (0.375) | 0.5253 | 0.6829 / 0.6940 (ENG-RES-0014) | +0.072; +32 |
| 8000 | 0.25, 0.275, 0.3, 0.35, 0.4, 0.45, 0.5 | 0.6415 (0.5) | 0.6415 (0.5) | 0.5890 (0.4) | 0.5262 (0.3) | 0.4756 | - / 0.619† (ENG-RES-0008) | +0.093; +82† |
| 16000 | 0.25, 0.275, 0.3, 0.325, 0.35, 0.4, 0.45, 0.5 | 0.5899 (0.5) | 0.5899 (0.5) | 0.5500 (0.45) | 0.4782 (0.3) | 0.4237 | 0.5749 / 0.5753 (ENG-RES-0014) | +0.097; +172 |
| 32000 | 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5 | 0.5646 (0.5) | 0.5646 (0.5) | 0.5400 (0.45) | 0.4439 (0.25) | - | - / 0.550† (ENG-RES-0008) | +0.106; +377† |
| 64000 | 0.2, 0.25, 0.275, 0.45, 0.5 | 0.5407 (0.5) | 0.5407 (0.5) | 0.5325 (0.45) | 0.4341 (0.275) | - | - / 0.537† (ENG-RES-0008) | +0.103; +731† |

Reading it.

1. **Chosen at the flat fibre** (column 4; the division's certified column, reproduced):
   no gain over two levels, and at `n = 1 000` a loss.
2. **Chosen by certified cost among the referee's own two middle designs** (column 5):
   never above two levels; strictly below the certified bound of two levels from
   `n = 1 400` on.
3. **With more middle designs on offer** (column 6; the bounded-accuracy design at every
   accuracy, described after this list): below the **worst instance found for two levels**
   at every size from `n = 4 000` on (last column).  What that comparison is: at `n = 4 000`
   and `16 000` the two-level algorithm is the one of the same outer design, at every outer
   fraction of the division's grid (ENG-RES-0014; mean runs on searched instances; margins
   `0.07`, `0.10` in these units, factors `e^{32}`, `e^{172}`); at `n = 8 000, 32 000, 64 000` it is the
   two-level algorithm of ENG-RES-0008, which has the same constants and **another ladder**
   (inner rates `ε*·0.85^i`; certified two-level bound `0.639, 0.560, 0.542` where the design of
   this table has `0.6415, 0.5646, 0.5407`), with inner answers placed adversarially (margins
   `0.09, 0.11, 0.10`: differences between quantities of two designs).  Where both ladders
   were searched the two worst cases differ by at most `0.006`.  At `n = 2 000` the two numbers
   agree within the resolution of the grids; at `n ≤ 1 400` three levels are not certified
   below the two-level worst case.
4. **Without a search and without a model: from `n = 16 000` on** (next section).
5. From `n = 16 000` on the certified three-level bound is below `τ₂/a = 0.500`, the limit of
   the two-level exponent — a remark about a limit: at a finite `n` it bounds nothing (at the
   flat instance two levels cost `0.4998`, `0.4961` in these units at `n = 32 000`, `64 000`).

## Two levels at the flat instance: the comparison that needs no model (`flat_two_level.py`)

The Scientific Discovery Division's point (SCI-REV-0016, m3), recomputed here on a finer
scan.  The Computational Research Division's two-level numbers are costs of *mean runs*
(every random count replaced by its mean) on instances found by search: a model and a
search.  On the zero function neither is involved — a two-level run with base brackets
inside is deterministic, and its number of evaluations is exact (`r8_flat.flat_run`).

| `n` | certified three-level bound | two levels at the flat instance, exact: least over the outer fractions `0.30, 0.31, …, 0.85` (at) | least over the block sizes scanned within `±0.03n` of it | outer fractions at which two levels at the flat instance cost no more than the three-level bound | margin at the least favourable size found |
|---|---|---|---|---|---|
| 4 000 | 0.6106 | 0.5336 (0.63) | 0.5322 (every size) | 0.56 … 0.71 | −0.078; −35 nats |
| 8 000 | 0.5262 | 0.5110 (0.59) | 0.5080 (every 2nd) | 0.58 … 0.60 | −0.018; −16 nats |
| 16 000 | 0.4782 | 0.5027 (0.56) | 0.4991 (every 4th) | none | +0.021; +37 nats |
| 32 000 | 0.4439 | 0.4998 (0.54) | 0.4980 (every 8th) | none | +0.054; +192 nats |
| 64 000 | 0.4341 | 0.4961 (0.53) | 0.4954 (every 16th) | none | +0.061; +435 nats |

So at `n = 16 000, 32 000, 64 000`, at every outer block size scanned, the two-level algorithm
as built makes, in every run on the zero function, more evaluations than three levels
make in any run on any instance; at `n = 4 000` and `8 000` it does not (two levels with an
outer fraction near `0.6` are cheap at the zero function and expensive elsewhere), and
item 3 rests on searched instances in the mean-run model.  The exact cost is not smooth
in the block size: at `n = 4 000` neighbouring sizes differ by up to `0.005` (two nats).  The
division's own figures (grid of step `0.01`, replicated with its own engine up to
`n = 32 000`): `0.5336, 0.5110, 0.5027, 0.4998, 0.4961` — the same.

(At `n = 32 000` and `64 000` the column of the flat-chosen servers was computed at the outer
fractions `0.50` and `0.45, 0.50` only — its minimum at every smaller size is at `0.50` — and the
costs at the flat instance were not computed; at `n = 64 000` the last design was evaluated at
three outer fractions, `0.20`, `0.25` and `0.275` — the last added after the Scientific Discovery
Division found `0.4341` there with its own code; confirmed, `out_64000d.txt`.  The "more
middle designs": the bounded-accuracy design, `λ = η = η′ = θ = c = min(x/12, ⅓)`, offered at
every accuracy `x` — the referee offers it below `x = 8` only — with tolerance `x/2` or the
largest its accuracy allows — any `b` with `(2p_u)^d + e^b(e^c(1+c)/(1−c) + 2c) ≤ e^x`; the code takes
`b = x − ln(e^c(1+c)/(1−c) + 2c) − 10⁻⁶` — and with its own outer fraction found by descent from
`0.50` in steps of `0.05`.)

## Where the gain comes from (`out_terms_4000.txt`, `out_terms_16000.txt`)

`terms.py` prints, rung by rung, the cost of the base bracket, the best two-level
candidate with its certified bound and its cost at the flat fibre, and the term of `C_max`.

* *The referee's design, charged its bounds* (`n = 4 000`, `φ₁ = 0.40`, mode `cert`).  The eleven
  rungs of accuracy `10` to `97` are served by two-level runs of the "extensive" design (`λ = 1`,
  `η = ½`, `b = x/4`) that are cheap at the flat fibre and certified above the base bracket
  they replace: at accuracy `9.8` the run costs `e^{0.223na}` at the flat fibre, is certified at
  `e^{0.704na}`, and the base bracket costs `e^{0.512na}`.  The finest of these rungs carry the
  bound (`0.809` at that fraction).  The flat-instance advantage of the referee's table
  lives in exactly these rungs.
* *Chosen by certified cost, more designs* (`n = 16 000`, `φ₁ = 0.30`, fibres of dimension
  `11 200`, mode `searched`).  26 of 40 rungs are served by two-level runs: the bounded-accuracy
  design at accuracies `0.5` to `106` — with the largest tolerance its accuracy allows and an
  outer fraction that falls from `0.50` at the finest rungs to `0.30` — and the extensive
  design at accuracies `138` to `404`.  At the finest rung the base bracket would cost
  `e^{0.769na}`; the two-level run is certified at `e^{0.432na}` and costs `e^{0.416na}` at the flat
  fibre.  The bound (`0.478`) is carried by the coarse rungs near accuracy `500`, where the
  multiplier changes from the sample cap `2M̄` to the count.

So the certified gain and the flat-instance gain come from different rungs and different
middle designs.

## Files

| file | what |
|---|---|
| `cert3.py` | the computation.  Uses the referee's routines `r8_flat.flat_run`, `k0_plan_flat` (nothing re-implemented).  Modes: `flat` (the referee's design and columns), `cert` (the same servers, charged their `C_max`: the division's certified column), `tuned` (servers by certified cost among the referee's candidates), `searched` (the same with the added candidates), `tunedflat`, `searchedflat` (the exact cost of those two algorithms at the flat instance).  Usage in its header |
| `terms.py` | the terms of `C_max` and the server of every rung, for one size and one outer fraction |
| `summary.py` | collects `out_*.txt` into the table above; cross-checks against the division's table |
| `flat_two_level.py` → `out_flat_two_level.txt` | the exact cost of two levels at the flat instance over the outer fractions `0.30 … 0.85` and over the block sizes near the minimum, against the certified three-level bound |
| `out_small.txt` (`n = 1 000, 1 400, 2 000`), `out_4000.txt`, `out_8000*.txt`, `out_16000*.txt`, `out_32000*.txt`, `out_64000*.txt` | outputs of `cert3.py`; the command of each is the first line of the list below |
| `out_terms_4000.txt`, `out_terms_16000.txt` | outputs of `terms.py` |
| `out_summary.txt` | output of `summary.py` |

Commands (run in this directory; times on four cores of the cloud container):

    python3 cert3.py 1000,1400,2000 0.30,0.35,0.40,0.45,0.50,0.55,0.60 flat,cert,tuned,tunedflat,searched,searchedflat > out_small.txt      # 4 min
    python3 cert3.py 4000 0.30,0.35,0.375,0.40,0.425,0.45,0.50 flat,cert,tuned,tunedflat,searched,searchedflat > out_4000.txt             # 3 min
    python3 cert3.py 8000 0.30,0.35,0.40,0.45,0.50 flat,cert,tuned,tunedflat,searched,searchedflat > out_8000.txt                          # 5 min
    python3 cert3.py 8000 0.25,0.275 flat,cert,tuned,tunedflat,searched,searchedflat > out_8000b.txt                                       # 2 min
    python3 cert3.py 16000 0.25,0.30,0.35,0.40,0.45,0.50 flat,cert,tuned,tunedflat,searched,searchedflat > out_16000.txt                   # 12 min
    python3 cert3.py 16000 0.275,0.325 tuned,searched > out_16000b.txt
    python3 cert3.py 32000 0.30,0.35,0.40,0.45 tuned,searched > out_32000.txt                                                             # 15 min
    python3 cert3.py 32000 0.25 tuned,searched > out_32000b.txt
    python3 cert3.py 32000 0.20 tuned,searched > out_32000c.txt
    python3 cert3.py 32000 0.50 cert,tuned > out_32000d.txt
    python3 cert3.py 64000 0.45,0.50 cert,tuned > out_64000.txt
    python3 cert3.py 64000 0.25 tuned,searched > out_64000b.txt
    python3 cert3.py 64000 0.20 tuned,searched > out_64000c.txt
    python3 cert3.py 64000 0.275 searched > out_64000d.txt                                                                                # 9 min
    python3 flat_two_level.py > out_flat_two_level.txt                                                                                    # 40 min
    python3 terms.py 4000 0.375 cert,tuned,searched > out_terms_4000.txt; python3 terms.py 4000 0.40 cert,tuned,searched >> out_terms_4000.txt
    python3 terms.py 16000 0.30 cert,tuned,searched > out_terms_16000.txt
    python3 summary.py > out_summary.txt

## What is checked, and against what

* `flat` reproduces the referee's stored three-level table (`experiments/reviews/R8/out/`)
  and `cert` the division's certified column: `summary.py` compares the two-level cost at
  the flat instance, the three-level cost at the flat instance and the certified
  three-level bound with the division's per-fraction table (ENG-RES-0014, table
  `three_worst`) wherever the grids overlap — 54 of 54 numbers agree to the four digits given.
  The division's evaluator is an independent implementation.
* Assertions inside `cert3.py`, on every row: every candidate has certified accuracy at
  most the rung's; a flat-instance cost never exceeds the corresponding bound; the
  bracket returned at the flat instance is valid and within the certified accuracy;
  `searched ≤ tuned ≤` the two-level bound at the same outer fraction.
* `terms.py` recomputes `C_max` from its terms and asserts equality with `flat_run`'s.

## What is not shown

* **The two-level side of item 3 is not ours, and it is a model.**  The worst instances
  for two levels are the Computational Research Division's searches; their costs are
  costs of *mean runs* (every random count replaced by its mean — neither an expected
  number of evaluations nor the number of a run; the agreement with literal runs was
  measured at small outer blocks): a lower bound on the worst case of the two-level
  algorithm in that model, at the best outer fraction of a grid of step `0.05`.  A theorem
  for `n = 4 000` and `8 000` would need a lower bound, with positive probability, for the
  evaluations of the two-level algorithm at those instances (open).  Reading (B):
  the algorithm as built (the base brackets' own answers on cone fibres); reading (A): base
  brackets' answers placed adversarially — an algorithm the theorem covers.  The certified
  three-level bound holds for both.  Where only (A) is available (`n = 1 400, 2 000, 8 000,
  32 000, 64 000`; ENG-RES-0008) the comparison is with an algorithm the theorem covers, not
  with the algorithm as built; where both exist they differ by `0.035, 0.011, 0.0004`
  (`n = 1 000, 4 000, 16 000`).
* **One design family, and two ladders in one column.**  "Two levels" means the outer
  design of this directory with the outer fraction free; the entries marked † are for the
  same constants with the ladder `ε*·0.85^i` (ENG-RES-0008).  The two-level worst case of
  this directory's design at `n = 8 000, 32 000, 64 000` has not been searched (asked of the
  Computational Research Division), other constants have not been searched at all, and no
  lower bound for two-level algorithms as a class is known.
* **One slope** (`u = 1`).
* **No cost of the new designs on bad instances.**  For the designs of `tuned` and `searched`
  only the bound and the cost at the flat instance are computed; the bound is what the
  comparison needs, but how close the worst case comes to it is not known.
* **Not optimised.**  Outer fractions on a grid; the outer ladder (40 rungs) and constants
  untouched; a handful of middle designs; the lowered sample cap of the remark after
  Theorem 11.56 not used; four and more levels — the same rule gives a certified level
  recursion at finite `n` — not evaluated.
* **Nothing one would run.**  The certified three-level bound at `n = 4 000` is `e^{271}`
  evaluations.
