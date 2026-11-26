# Three nested levels: the certified bound when every rung is served by the procedure with the smallest certified cost

Coordinator's check, twentieth checkpoint of cycle 10 (2026-11-26).  Theory report §11.19,
remark (1b); message THY-RES-0013 §4; `docs/DEAD_ENDS.md`, D61.  Nothing here is refereed;
the Computational Research Division has been asked to reproduce it with its own evaluator.

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
with the trivial bracket before a call would exceed it), so

* a two-level run designed for the fibre dimension, an accuracy at most `x_l` and the failure
  probability `δ′` of the outer level is an admissible server with `C_l = ` its own `C_max`;
* `C_max` of the outer level is nondecreasing in every `C_l`.

Hence, if each rung is served by the candidate with the smallest **certified** cost (the
base bracket's cost is fixed by its design and is its own bound), the certified bound of
three levels is at most that of two levels at the same outer design — for every `n`, and
offering more candidate designs can only lower it.  Which candidate serves which rung is
decided before any evaluation, from the design alone.

`ln(bound)/(na)` at `u = 1` (`a = ln 2 − H(1/(1+e)) = 0.11094`), outer level with the parameters of
the report's §6.4 (`b = 0.5`, `λ = 0.2`, `η = η′ = θ = 0.05`, `δ = 0.05`, 40 rungs; certified accuracy
`0.8715` for two and for three levels), minimum over the outer fractions computed (the
fraction in brackets); full table with the grids: `out_summary.txt`.

| n | outer fractions computed | two levels: certified bound | three levels, servers chosen at the flat fibre: certified bound | three levels, servers by certified cost (referee's middle designs): certified bound | the same with more middle designs: certified bound | cost of that design at the flat instance (same fraction) | two levels: worst instance found by the Computational Research Division, reading (B) / (A) | margin: two-level worst found (smaller reading) minus the certified three-level bound, in units of n a; in nats |
|---|---|---|---|---|---|---|---|---|
| 1000 | 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6 | 1.1384 (0.5) | 1.1554 (0.5) | 1.1384 (0.5) | 1.1384 (0.5) | 0.9839 | 1.0114 / 1.0461 (ENG-RES-0014) | -0.127; -14 |
| 1400 | 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6 | 0.9933 (0.5) | 0.9873 (0.5) | 0.9669 (0.45) | 0.9659 (0.45) | 0.7707 | - / 0.924 (ENG-RES-0008) | -0.042; -7 |
| 2000 | 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6 | 0.8721 (0.5) | 0.8686 (0.5) | 0.8120 (0.45) | 0.8118 (0.45) | 0.6400 | - / 0.822 (ENG-RES-0008) | +0.010; +2 |
| 4000 | 0.3, 0.35, 0.375, 0.4, 0.425, 0.45, 0.5 | 0.7262 (0.5) | 0.7261 (0.5) | 0.6331 (0.4) | 0.6106 (0.375) | 0.5253 | 0.6829 / 0.6940 (ENG-RES-0014) | +0.072; +32 |
| 8000 | 0.25, 0.275, 0.3, 0.35, 0.4, 0.45, 0.5 | 0.6415 (0.5) | 0.6415 (0.5) | 0.5890 (0.4) | 0.5262 (0.3) | 0.4756 | - / 0.619 (ENG-RES-0008) | +0.093; +82 |
| 16000 | 0.25, 0.275, 0.3, 0.325, 0.35, 0.4, 0.45, 0.5 | 0.5899 (0.5) | 0.5899 (0.5) | 0.5500 (0.45) | 0.4782 (0.3) | 0.4237 | 0.5749 / 0.5753 (ENG-RES-0014) | +0.097; +172 |
| 32000 | 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5 | 0.5646 (0.5) | 0.5646 (0.5) | 0.5400 (0.45) | 0.4439 (0.25) | - | - / 0.550 (ENG-RES-0008) | +0.106; +377 |
| 64000 | 0.2, 0.25, 0.45, 0.5 | 0.5407 (0.5) | 0.5407 (0.5) | 0.5325 (0.45) | 0.4381 (0.25) | - | - / 0.537 (ENG-RES-0008) | +0.099; +702 |

Reading it.

1. **Chosen at the flat fibre** (column 4; the division's certified column, reproduced):
   no gain over two levels, and at `n = 1 000` a loss.
2. **Chosen by certified cost among the referee's own two middle designs** (column 5):
   never above two levels; strictly below the certified bound of two levels from
   `n = 1 400` on.
3. **With more middle designs on offer** (column 6; the bounded-accuracy design at every
   accuracy, described after this list): below the **worst instance found for two levels** — an instance on
   which the two-level algorithm of the same outer design, at its best outer fraction,
   needs more evaluations than three levels need on any instance — at every size from
   `n = 4 000` on, by `0.07` to `0.11` in these units, a factor that grows from `e^{32}` at
   `n = 4 000` to `e^{702}` at `n = 64 000` (last column); at `n = 2 000` the two numbers agree within
   the resolution of the grids; at `n ≤ 1 400` three levels are not certified below the
   two-level worst case.
4. From `n = 16 000` on the certified three-level bound is below `τ₂/a = 0.500`, the limit that
   the two-level worst case approaches from above (`0.526` at `n = 128 000`, ENG-RES-0008).

(At `n = 32 000` and `64 000` the column of the flat-chosen servers was computed at the outer
fractions `0.50` and `0.45, 0.50` only — its minimum at every smaller size is at `0.50` — and the
costs at the flat instance were not computed; at `n = 64 000` the last design was evaluated at
two outer fractions, `0.20` and `0.25`.  The "more middle designs": the bounded-accuracy design,
`λ = η = η′ = θ = c = min(x/12, ⅓)`, offered at every accuracy `x` — the referee offers it below
`x = 8` only — with tolerance `x/2` or the largest its accuracy allows,
`b = x − ln(e^c(1+c)/(1−c) + 2c)`, and with its own outer fraction found by descent from `0.50` in
steps of `0.05`.)

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

* **The two-level side is not ours.**  The worst instances for two levels are the
  Computational Research Division's searches at the level of expectations (expected
  counts in place of random ones): a lower bound on the worst case of the two-level
  algorithm in that model, at the best outer fraction of a grid of step `0.05`.  Reading (B):
  the algorithm as built (the base brackets' own answers on cone fibres); reading (A): base
  brackets' answers placed adversarially — an algorithm the theorem covers.  The certified
  three-level bound holds for both.  Where only (A) is available (`n = 1 400, 2 000, 8 000,
  32 000, 64 000`; ENG-RES-0008) the comparison is with an algorithm the theorem covers, not
  with the algorithm as built; where both exist they differ by `0.035, 0.011, 0.0004`
  (`n = 1 000, 4 000, 16 000`).
* **One design family.**  "Two levels" means the outer design of §6.4 with the outer
  fraction free; a two-level design with another ladder or other constants has not been
  searched, and no lower bound for two-level algorithms as a class is known.
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
