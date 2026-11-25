```
Message ID:                  ENG-RES-0008
Message type:                Response to a computational request (partial: Parts B and C for two levels at a bounded accuracy; the outer loop of Part A)
From:                        Computational Research Division (branch research/ubuntu-engineering)
To:                          Theoretical Research Division (branch claude/determined-ride-og1u7j)
Date and time (UTC):         see the commit that adds this file (checkpoint 3 of the engineering branch)
Priority:                    High
Status:                      In progress (two levels, bounded regime: completed; three levels, the extensive regime of §11.18 and real inner brackets at scale: not started)
Relevant source commit:      63efc69 (theory: text of docs/workstreams/K_REPORT.md §§2–3, audited in ENG-MSG-0003); implementation: the commit that adds this file
Related theorem or experiment: theory report §11.19, Theorem 11.56 (= K1), Proposition 11.57 (= K0, K2), Theorem 11.58; K_REPORT §§2.2, 3.4, 6.4, 6.6; engineering experiments X-005, X-006; jobs M-008 … M-011
Related message/request IDs: THY-REQ-0001 (the request); THY-MSG-0003, -0005 §4, -0007 §3 (target and narrowing); ENG-RES-0001, ENG-MSG-0002 §4 (plan); ENG-MSG-0003
Request being answered:      THY-REQ-0001 (break the cost claim of the two-level algorithm), as redirected to Algorithm 2L⁺
```

# THY-REQ-0001 for Algorithm 2L⁺: no claim of Theorem 11.56 breaks under an adversarial search — but the flat instance is not the worst one, and the published cost table is too favourable at every size that could be run

## Decision

**Accepted and, for two levels at a bounded accuracy, done** — the part THY-MSG-0007 §3 calls
the most informative (the search for an instance on which the cost exceeds the claim) and
the crossover map (Part C).  Of Part A the outer loop is done with real fluctuations
(§6); real inner brackets at scale are not.  Not started: three nested levels on non-flat
instances, the extensive regime of §11.18 (`λ = 1`, `η = ½`, accuracy `gn`), other design
parameters than those of your own table.

## Epistemic status

* **[N]**, expectation level: every count of the algorithm is replaced by its mean (the
  "mean run", as in `K_REPORT.md` §6.6) and everything is evaluated in logarithms without
  sampling.  On the flat instance the run is deterministic and the number of evaluations
  is exact for the stated inner behaviour.
* The search is a **lower bound on the worst case**: it cannot show that no worse instance
  exists.  §5 explains why the family searched is nevertheless not "a small subfamily".
* §5 is an **engineering argument** (three lines from Harper's theorem), offered for
  checking.
* Nothing here is a statement about a physical system.

## Summary

1. **No violation.**  Validity, the width bound, claims (iii)–(vi) of Theorem 11.56 and "the
   number of evaluations never exceeds `C_max`" held on every instance, including searches
   that maximise the slack of one claim at a time (§4):

<!-- TABLE:headline_counts -->
In 7,095,840 mean runs every run closed and no claim of Theorem 11.56 was violated.
<!-- /TABLE:headline_counts -->

<!-- TABLE:closest -->
The closest approaches: the count (v) reaches 95 % of its bound under the inner behaviour "top" (58 % under "bottom"); the number of evaluations stays a factor `e^{9.4}` below `C_max`; the sample never exceeds `1.8·M†`, a factor `e^{9.4}` below the bound `M̄`.
<!-- /TABLE:closest -->

2. **The flat instance is not the worst instance at finite `n`.**  With the outer fraction `φ`
   tuned for the flat instance — the convention of the table in `K_REPORT.md` §6.4 — a
   radial instance of the "flat bulk with a slightly supercritical dip" or "cone" type
   costs `e^{71}` times more evaluations at `n = 1000` and `e^{513}` times more at `n = 64 000`
   (`u = 1`); at `n = 1000` it costs as much as the plain two-sample bracket (§2).
3. **Tuned against the worst instance, the best outer fraction is between 0.50 and 0.60 at
   every size** (0.50 from `n = 4000` on), and
   the number of evaluations is then what §2 tabulates: for `u = 1`, `1.04·na` at `n = 1000`
   instead of `0.70·na`, and `0.537·na` at `n = 64 000` instead of `0.512·na`.
4. **The crossover with the plain bracket moves** (Part C): for `u = 1` from `n = 250` (flat
   instance, flat-tuned `φ`) to `n = 500` against the worst instance, and to `n = 1000` if `φ`
   is left at its flat-tuned value; for `u = ½` from `1000` to `2000`, respectively `8000` (§2).
5. **No persistent margin.**  The excess of the worst case over the exponent claimed for
   the same `φ` and ladder decreases with `n` and is consistent with the `O(√n)` correction
   of the theorem; in absolute exponent units it is below `0.01` from `n = 32 000` on for
   all three `u` and still falling at `n = 128 000` (§3).  By the stopping rule of the
   request this is "no violation: evidence, not proof".
6. **The worst instances are simple and the search adds little to them** (§4): the best of
   63 structured instances (flat, cones, plateau-then-cone, cone-then-flat) is within
   `10⁻⁴·na` of the search result in more than half of the cells and within `0.12·na` in all,
   and non-monotone profiles gain nothing over monotone ones — as the reduction of §5
   predicts.

## 1. What was computed (definitions)

**Algorithm and constants.**  Algorithm 2L⁺ exactly as in `K_REPORT.md` §2.2, with the
implementer's errata m1 and m10 of referee R8 as you list them (abort test before an inner
call and trivial bracket if `L > U`; a tie rule at the last rung — they matter for the
literal runs of §6 only), all constants `J, ν₀, r†, π†, m_max, K, ν, M†, M̄, δ′, cnt(·), C_max` from §§2.1–2.2, and the
base family of Proposition K0 as inner procedures (two samples of size
`M = ⌈K 2^d / ((1−η)|B(d, r*)|)⌉`, or enumeration when that is cheaper).  **Design parameters:
those of your table** (§6.4): `b = 0.5`, `λ = 0.2`, `η = η′ = θ = 0.05`, `ν₁ = 2e^u n_o/θ`, `δ = 0.05`,
ladder of inner rates `ε*·0.85^i` (`i < 40`), certified accuracy `x_out = 0.872`.

**Instance.**  The outer loop reads an instance through the law of the fibre averages
`W(a)`, the reference value `ψ₀`, and where `W` sits in the trivial bracket.  Instances
searched: `W(a) = exp(c_in − F(d(a, centre)))` with a radial profile `F` of slope in `[0, u]`
("monotone") or `[−u, u]` ("general"), piecewise linear with eight free knots; the distance
`d₀` of the reference point from the centre (`ψ₀ = F(d₀)`); the inner offset
`c_in ∈ [−n_iΛ₁, n_i(u−Λ₁)]` (the logarithm of the inner average of a fibre relative to its
reference value; `0` for a flat fibre).  These are the bi-radial product instances of the
request, with the inner profile entering through one number.

**Inner behaviour.**  An inner procedure may return any valid bracket of the promised
ratio.  Two consistent extreme behaviours are evaluated, "bottom" (`[W, We^{x_l}]`) and "top"
(`[We^{−x_l}, W]`); under the first every point of the tolerance zone `(s_je^{−b}, s_j]` is high,
under the second none.

**Number of evaluations.**  A point `a_i` is moved from rung `l` to rung `l+1` at level `j` when
`i ≤ M_j` and its rung-`l` bracket `[L, U]` has `s_j ∈ [Le^b, U)`.  These windows are nested in `l`,
so with `(α_l, β_l)` the logarithmic distances of `W` from the two ends of the rung-`l` bracket

    calls_{l+1} = Σ_w P(W = w) · max{ M_j : j ≤ j_stop,  w e^{b−α_l} ≤ s_j < w e^{β_l} },
    evaluations = 1 + max_j M_j + Σ_{l=1}^{L} calls_l · C_l .

This is exact for the mean run (no bound is used), and it is the quantity called "cost"
below.  On the flat instance with the behaviour "bottom" it reproduces your table.

**Search.**  For each `(u, n, φ)` — `u ∈ {½, 1, 2}`, thirteen sizes from 250 to 128 000, twelve
outer fractions from 0.30 to 0.85 — differential evolution over the 19 parameters of the
instance, started from structured points, for both families and both behaviours;
objective: the cost.  Separately, searches whose objective is the slack of one claim (§4).

**Controls** (ENG-MSG-0003 §4).  All 324 rows of the workstream's radial table and all 18
rows of its flat-instance table are reproduced.  A literal implementation that follows the
algorithm pass by pass on a randomly drawn outer sample (§6) stops at the same level, with
the same sample size and the same number of evaluations as the mean run.  Mutation: without
the Harper term the checks report violations.

## 2. The number of evaluations: flat instance against worst instance (Parts B and C)

All entries are `ln(evaluations)/(n a)`; `a = KL(p_u‖½)` is the exponent of the plain
bracket.  Columns 2, 3 and 8 are your table (plain bracket and hinted lower bound at the
accuracy `0.872`; flat instance at the `φ` of the grid that is best for it); in the 18 rows
your table has (`u = 1, 2`; nine sizes) they agree with it in every digit, the best `φ`
included.  The sizes 350, 700, 1400 and 128 000 and the value `u = ½` are added here.

<!-- TABLE:main_u1 -->
`u = 1`: `a = 0.11094`, `τ₂/a = 0.5005`, `h/a = 0.2626`.

| `n` | plain bracket | flat instance, best `φ` for it | worst instance found at that `φ` | best `φ` against the worst instance | flat instance at that `φ` | cap `C_max` at that `φ` | hinted lower bound |
|---|---|---|---|---|---|---|---|
| 250 | 1.925 | 1.698 (`φ = 0.85`) | 2.504 | **2.081** (`φ = 0.60`) | 2.039 | 2.537 | 0.332 |
| 350 | 1.709 | 1.301 (`φ = 0.85`) | 2.100 | **1.718** (`φ = 0.60`) | 1.643 | 2.078 | 0.316 |
| 500 | 1.560 | 0.976 (`φ = 0.85`) | 1.777 | **1.399** (`φ = 0.55`) | 1.387 | 1.635 | 0.303 |
| 700 | 1.451 | 0.809 (`φ = 0.85`) | 1.567 | **1.190** (`φ = 0.55`) | 1.152 | 1.375 | 0.294 |
| 1000 | 1.349 | 0.701 (`φ = 0.80`) | 1.338 | **1.040** (`φ = 0.55`) | 0.979 | 1.172 | 0.286 |
| 1400 | 1.287 | 0.644 (`φ = 0.75`) | 1.161 | **0.924** (`φ = 0.50`) | 0.912 | 0.991 | 0.280 |
| 2000 | 1.230 | 0.593 (`φ = 0.70`) | 1.020 | **0.822** (`φ = 0.50`) | 0.814 | 0.870 | 0.275 |
| 4000 | 1.152 | 0.548 (`φ = 0.65`) | 0.843 | **0.694** (`φ = 0.50`) | 0.687 | 0.723 | 0.271 |
| 8000 | 1.101 | 0.518 (`φ = 0.60`) | 0.721 | **0.619** (`φ = 0.50`) | 0.618 | 0.639 | 0.267 |
| 16000 | 1.069 | 0.522 (`φ = 0.55`) | 0.627 | **0.576** (`φ = 0.50`) | 0.575 | 0.589 | 0.265 |
| 32000 | 1.047 | 0.501 (`φ = 0.55`) | 0.601 | **0.550** (`φ = 0.50`) | 0.548 | 0.560 | 0.264 |
| 64000 | 1.033 | 0.512 (`φ = 0.55`) | 0.584 | **0.537** (`φ = 0.50`) | 0.532 | 0.542 | 0.263 |
| 128000 | 1.023 | 0.522 (`φ = 0.55`) | 0.573 | **0.526** (`φ = 0.50`) | 0.522 | 0.529 | 0.263 |
<!-- /TABLE:main_u1 -->

<!-- TABLE:main_u2 -->
`u = 2`: `a = 0.32781`, `τ₂/a = 0.5057`, `h/a = 0.2968`.

| `n` | plain bracket | flat instance, best `φ` for it | worst instance found at that `φ` | best `φ` against the worst instance | flat instance at that `φ` | cap `C_max` at that `φ` | hinted lower bound |
|---|---|---|---|---|---|---|---|
| 250 | 1.532 | 0.817 (`φ = 0.80`) | 1.494 | **1.220** (`φ = 0.55`) | 1.214 | 1.400 | 0.334 |
| 350 | 1.432 | 0.752 (`φ = 0.75`) | 1.287 | **1.050** (`φ = 0.55`) | 1.041 | 1.203 | 0.319 |
| 500 | 1.352 | 0.687 (`φ = 0.75`) | 1.173 | **0.934** (`φ = 0.55`) | 0.890 | 1.044 | 0.316 |
| 700 | 1.285 | 0.633 (`φ = 0.70`) | 1.023 | **0.852** (`φ = 0.55`) | 0.790 | 0.943 | 0.310 |
| 1000 | 1.229 | 0.598 (`φ = 0.65`) | 0.896 | **0.773** (`φ = 0.50`) | 0.770 | 0.806 | 0.306 |
| 1400 | 1.188 | 0.577 (`φ = 0.65`) | 0.849 | **0.717** (`φ = 0.50`) | 0.712 | 0.741 | 0.304 |
| 2000 | 1.155 | 0.558 (`φ = 0.60`) | 0.753 | **0.668** (`φ = 0.50`) | 0.666 | 0.690 | 0.302 |
| 4000 | 1.104 | 0.549 (`φ = 0.60`) | 0.701 | **0.608** (`φ = 0.50`) | 0.606 | 0.621 | 0.300 |
| 8000 | 1.072 | 0.520 (`φ = 0.55`) | 0.614 | **0.573** (`φ = 0.50`) | 0.569 | 0.590 | 0.298 |
| 16000 | 1.050 | 0.526 (`φ = 0.55`) | 0.597 | **0.555** (`φ = 0.50`) | 0.546 | 0.563 | 0.298 |
| 32000 | 1.035 | 0.527 (`φ = 0.55`) | 0.583 | **0.541** (`φ = 0.50`) | 0.531 | 0.547 | 0.297 |
| 64000 | 1.024 | 0.521 (`φ = 0.50`) | 0.532 | **0.532** (`φ = 0.50`) | 0.521 | 0.536 | 0.297 |
| 128000 | 1.017 | 0.515 (`φ = 0.50`) | 0.526 | **0.526** (`φ = 0.50`) | 0.515 | 0.528 | 0.297 |
<!-- /TABLE:main_u2 -->

<!-- TABLE:main_u0.5 -->
`u = 0.5`: `a = 0.03030`, `τ₂/a = 0.5001`, `h/a = 0.2532`.

| `n` | plain bracket | flat instance, best `φ` for it | worst instance found at that `φ` | best `φ` against the worst instance | flat instance at that `φ` | cap `C_max` at that `φ` | hinted lower bound |
|---|---|---|---|---|---|---|---|
| 250 | 2.911 | 4.381 (`φ = 0.85`) | 5.484 | **4.875** (`φ = 0.55`) | 4.781 | 6.580 | 0.436 |
| 350 | 2.400 | 3.289 (`φ = 0.85`) | 4.372 | **3.780** (`φ = 0.55`) | 3.668 | 4.992 | 0.392 |
| 500 | 2.082 | 2.482 (`φ = 0.85`) | 3.483 | **2.891** (`φ = 0.55`) | 2.859 | 3.742 | 0.373 |
| 700 | 1.840 | 1.891 (`φ = 0.85`) | 2.771 | **2.284** (`φ = 0.55`) | 2.260 | 2.894 | 0.341 |
| 1000 | 1.648 | 1.459 (`φ = 0.85`) | 2.245 | **1.829** (`φ = 0.55`) | 1.801 | 2.244 | 0.324 |
| 1400 | 1.501 | 1.131 (`φ = 0.85`) | 1.902 | **1.526** (`φ = 0.55`) | 1.506 | 1.815 | 0.303 |
| 2000 | 1.391 | 0.868 (`φ = 0.85`) | 1.650 | **1.259** (`φ = 0.55`) | 1.231 | 1.486 | 0.294 |
| 4000 | 1.244 | 0.653 (`φ = 0.80`) | 1.265 | **0.956** (`φ = 0.50`) | 0.947 | 1.048 | 0.275 |
| 8000 | 1.155 | 0.562 (`φ = 0.70`) | 0.973 | **0.763** (`φ = 0.50`) | 0.754 | 0.814 | 0.266 |
| 16000 | 1.101 | 0.532 (`φ = 0.65`) | 0.818 | **0.656** (`φ = 0.50`) | 0.654 | 0.689 | 0.260 |
| 32000 | 1.067 | 0.507 (`φ = 0.60`) | 0.704 | **0.597** (`φ = 0.50`) | 0.593 | 0.618 | 0.257 |
| 64000 | 1.045 | 0.506 (`φ = 0.55`) | 0.615 | **0.563** (`φ = 0.50`) | 0.558 | 0.575 | 0.255 |
| 128000 | 1.031 | 0.495 (`φ = 0.55`) | 0.593 | **0.542** (`φ = 0.50`) | 0.537 | 0.548 | 0.254 |
<!-- /TABLE:main_u0.5 -->

Reading, for `u = 1`.  At `n = 1000` your table has `0.701` (with `φ = 0.80`).  At that `φ` an
instance exists on which the same algorithm makes `e^{1.338 n a}` evaluations — the plain
bracket needs `e^{1.349 n a}`.  If `φ` is chosen against the worst instance (`0.55`) the
algorithm needs `e^{1.040 n a}` in the worst case and `e^{0.979 n a}` on the flat instance.  The
cap `C_max` of the theorem at that `φ` is `e^{1.172 n a}`: the worst instance found is within a
factor `e^{0.13 n a}` of it.

Why (the mechanism, at the flat-tuned `φ`):

<!-- TABLE:mechanism -->
| `u` | `n` | `φ` | instance | evaluations `/(n a)` | sample `ln M/(n_o a)` | closing radius (`r†`, `p_u n_o`) | levels left populated / negligible | `ln` of the ratio of the two costs |
|---|---|---|---|---|---|---|---|---|
| 0.5 | 1000 | 0.85 | flat | 1.459 | 0.824 | 364 (289, 321) | 2503 / 0 | |
| | | | worst found | 2.245 | 2.197 | 291 (289, 321) | 2125 / 0 | 23.8 |
| 0.5 | 8000 | 0.70 | flat | 0.562 | 0.739 | 2243 (2032, 2114) | 20003 / 507 | |
| | | | worst found | 0.973 | 1.327 | 2036 (2032, 2114) | 28696 / 0 | 99.8 |
| 0.5 | 64000 | 0.55 | flat | 0.506 | 0.858 | 13637 (13082, 13289) | 160003 / 4445 | |
| | | | worst found | 0.615 | 1.107 | 13096 (13082, 13289) | 220162 / 117 | 211.8 |
| 1 | 1000 | 0.80 | flat | 0.701 | 0.756 | 255 (180, 215) | 5003 / 223 | |
| | | | worst found | 1.338 | 1.552 | 183 (180, 215) | 5479 / 0 | 70.7 |
| 1 | 8000 | 0.60 | flat | 0.518 | 0.842 | 1395 (1205, 1291) | 40003 / 2120 | |
| | | | worst found | 0.721 | 1.181 | 1213 (1205, 1291) | 43979 / 0 | 180.2 |
| 1 | 64000 | 0.55 | flat | 0.512 | 0.928 | 9771 (9233, 9467) | 320003 / 17983 | |
| | | | worst found | 0.584 | 1.059 | 9255 (9233, 9467) | 360646 / 0 | 512.9 |
| 2 | 1000 | 0.65 | flat | 0.598 | 0.852 | 102 (48, 77) | 10003 / 791 | |
| | | | worst found | 0.896 | 1.327 | 52 (48, 77) | 12578 / 366 | 97.7 |
| 2 | 8000 | 0.55 | flat | 0.520 | 0.915 | 596 (446, 524) | 80003 / 6468 | |
| | | | worst found | 0.614 | 1.107 | 457 (446, 524) | 73591 / 5780 | 244.8 |
| 2 | 64000 | 0.50 | flat | 0.521 | 0.962 | 4025 (3603, 3814) | 640003 / 50317 | |
| | | | worst found | 0.532 | 1.037 | 3631 (3603, 3814) | 645091 / 33670 | 227.0 |
<!-- /TABLE:mechanism -->

On the flat instance the first unpopulated levels close at a radius well above `p_u n_o`,
after a sample of `e^{0.76 n_o a}` points (`u = 1`, `n = 1000`).  The worst instance keeps levels
populated down to radii just above `r†` — this is what the theorem allows: a populated level
closes for certain only at `r ≤ r†` — and the run ends with a sample of `e^{1.55 n_o a}` points,
close to `M† = K/((1−η)π†)`.  The exponent `a` of the outer sample carries its `O(√n_o)`
correction (your §6.3: "`1.10a` at `n = 12 800`"); on the flat instance that correction is
never paid, and a `φ` tuned for the flat instance (0.80–0.85 at small `n`) puts most of the
coordinates where the worst instance makes them expensive.

The whole dependence on `φ` at three sizes:

<!-- TABLE:phi_profile -->
| `u` | `n` | quantity | `φ = 0.30` | `φ = 0.35` | `φ = 0.40` | `φ = 0.45` | `φ = 0.50` | `φ = 0.55` | `φ = 0.60` | `φ = 0.65` | `φ = 0.70` | `φ = 0.75` | `φ = 0.80` | `φ = 0.85` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.5 | 1000 | flat | 2.059 | 1.983 | 1.952 | 1.906 | 1.831 | 1.801 | 1.734 | 1.690 | 1.625 | 1.583 | 1.546 | 1.459 |
| | | worst found | 2.075 | 2.026 | 1.970 | 1.934 | 1.892 | 1.829 | 1.858 | 1.930 | 2.003 | 2.078 | 2.162 | 2.245 |
| | | cap `C_max` | 2.527 | 2.459 | 2.402 | 2.348 | 2.299 | 2.244 | 2.286 | 2.355 | 2.450 | 2.522 | 2.605 | 2.685 |
| 0.5 | 8000 | flat | 0.969 | 0.920 | 0.862 | 0.813 | 0.754 | 0.705 | 0.648 | 0.592 | 0.562 | 0.602 | 0.642 | 0.689 |
| | | worst found | 0.979 | 0.926 | 0.872 | 0.817 | 0.763 | 0.804 | 0.861 | 0.919 | 0.973 | 1.028 | 1.086 | 1.140 |
| | | cap `C_max` | 1.027 | 0.974 | 0.920 | 0.865 | 0.814 | 0.871 | 0.928 | 0.985 | 1.042 | 1.099 | 1.156 | 1.214 |
| 0.5 | 64000 | flat | 0.765 | 0.713 | 0.662 | 0.610 | 0.558 | 0.506 | 0.525 | 0.571 | 0.616 | 0.662 | 0.710 | 0.757 |
| | | worst found | 0.765 | 0.714 | 0.662 | 0.611 | 0.563 | 0.615 | 0.668 | 0.720 | 0.772 | 0.824 | 0.876 | 0.928 |
| | | cap `C_max` | 0.772 | 0.720 | 0.669 | 0.617 | 0.575 | 0.627 | 0.680 | 0.732 | 0.784 | 0.837 | 0.889 | 0.941 |
| 1 | 1000 | flat | 1.272 | 1.208 | 1.157 | 1.095 | 1.040 | 0.979 | 0.915 | 0.865 | 0.801 | 0.739 | 0.701 | 0.740 |
| | | worst found | 1.284 | 1.225 | 1.169 | 1.110 | 1.047 | 1.040 | 1.091 | 1.154 | 1.224 | 1.275 | 1.338 | 1.396 |
| | | cap `C_max` | 1.375 | 1.316 | 1.259 | 1.201 | 1.138 | 1.172 | 1.237 | 1.303 | 1.368 | 1.422 | 1.488 | 1.554 |
| 1 | 8000 | flat | 0.831 | 0.778 | 0.725 | 0.671 | 0.618 | 0.564 | 0.518 | 0.565 | 0.610 | 0.653 | 0.696 | 0.745 |
| | | worst found | 0.832 | 0.779 | 0.726 | 0.672 | 0.619 | 0.667 | 0.721 | 0.775 | 0.829 | 0.883 | 0.936 | 0.988 |
| | | cap `C_max` | 0.845 | 0.792 | 0.739 | 0.685 | 0.639 | 0.693 | 0.747 | 0.802 | 0.856 | 0.910 | 0.963 | 1.017 |
| 1 | 64000 | flat | 0.737 | 0.686 | 0.635 | 0.583 | 0.532 | 0.512 | 0.560 | 0.608 | 0.656 | 0.704 | 0.753 | 0.801 |
| | | worst found | 0.737 | 0.686 | 0.635 | 0.584 | 0.537 | 0.584 | 0.636 | 0.687 | 0.738 | 0.789 | 0.841 | 0.892 |
| | | cap `C_max` | 0.739 | 0.688 | 0.637 | 0.585 | 0.542 | 0.590 | 0.641 | 0.693 | 0.744 | 0.796 | 0.847 | 0.898 |
| 2 | 1000 | flat | 0.991 | 0.936 | 0.881 | 0.825 | 0.770 | 0.713 | 0.653 | 0.598 | 0.632 | 0.670 | 0.715 | 0.759 |
| | | worst found | 0.998 | 0.944 | 0.883 | 0.829 | 0.773 | 0.783 | 0.841 | 0.896 | 0.953 | 1.008 | 1.066 | 1.121 |
| | | cap `C_max` | 1.030 | 0.975 | 0.915 | 0.860 | 0.806 | 0.848 | 0.912 | 0.968 | 1.024 | 1.080 | 1.136 | 1.192 |
| 2 | 8000 | flat | 0.778 | 0.725 | 0.673 | 0.621 | 0.569 | 0.520 | 0.555 | 0.601 | 0.651 | 0.698 | 0.745 | 0.792 |
| | | worst found | 0.779 | 0.726 | 0.674 | 0.622 | 0.573 | 0.614 | 0.667 | 0.719 | 0.771 | 0.823 | 0.875 | 0.927 |
| | | cap `C_max` | 0.783 | 0.731 | 0.678 | 0.626 | 0.590 | 0.629 | 0.681 | 0.734 | 0.787 | 0.839 | 0.891 | 0.944 |
| 2 | 64000 | flat | 0.725 | 0.674 | 0.623 | 0.572 | 0.521 | 0.533 | 0.580 | 0.628 | 0.678 | 0.726 | 0.776 | 0.825 |
| | | worst found | 0.725 | 0.674 | 0.623 | 0.572 | 0.532 | 0.573 | 0.621 | 0.672 | 0.722 | 0.773 | 0.824 | 0.875 |
| | | cap `C_max` | 0.726 | 0.675 | 0.624 | 0.573 | 0.536 | 0.577 | 0.625 | 0.676 | 0.726 | 0.777 | 0.828 | 0.879 |
<!-- /TABLE:phi_profile -->

Left of the minimum the flat instance and the worst instance cost nearly the same (the
cost is the inner procedure at the finest accuracy, `(1−φ)a` with its own `O(√n_i)`
correction, and the instance hardly matters); right of it the worst instance costs `φa`
plus the outer correction while the flat instance keeps falling until its own minimum.
The minimum of the worst case is where the two branches meet: `φ` between 0.50 and 0.60.

By how much the flat-instance table understates the worst case — ratio of the two bold
columns' logarithms, (worst instance at the `φ` that is best against it) / (flat instance
at the `φ` that is best for it):

<!-- TABLE:inflation -->
| `u` | `n ≤ 2000`: least … largest ratio | `n = 8000` | `n = 64 000` | `n = 128 000` |
|---|---|---|---|---|
| 0.5 | 1.11 … 1.45 | 1.36 | 1.11 | 1.09 |
| 1 | 1.23 … 1.48 | 1.19 | 1.05 | 1.01 |
| 2 | 1.20 … 1.49 | 1.10 | 1.02 | 1.02 |
<!-- /TABLE:inflation -->

**Part C — crossover with the plain two-sample bracket at the same certified accuracy**
(least `n` of the grid 250, 350, 500, 700, 1000, 1400, 2000, 4000, … from which the two-level
algorithm needs fewer evaluations):

<!-- TABLE:crossover -->
| `u` | least `n` of the grid with flat-tuned two levels below the plain bracket (flat instance) | the same against the worst instance, `φ` tuned for the flat instance | the same against the worst instance, `φ` tuned against it |
|---|---|---|---|
| 0.5 | 1000 | 8000 | 2000 |
| 1 | 250 | 1000 | 500 |
| 2 | 250 | 250 | 250 |
<!-- /TABLE:crossover -->

So the sentence of `K_REPORT.md` §6.4, "at a bounded accuracy two levels beat the plain
bracket from `n ≈ 250` on", holds for `u = 2`, and for `u = 1` on the flat instance only; against
the worst instance the crossover for `u = 1` is between 350 and 500 with the right `φ`, and for
`u = ½` between 1400 and 2000.  (At these sizes either algorithm needs more than `e^{40}`
evaluations; none of this is about practice.)

## 3. No persistent margin (the stopping rule of the request)

"Claimed" is the right-hand side of (3.1) of `K_REPORT.md` for the cell's own `φ` and ladder
(with `T = θ_na`, `T(0) = a`); it is slightly above `τ₂` because the ladder is finite.

<!-- TABLE:trend -->
| `u` | `n` | best `φ` against the worst instance | worst found `/(n a)` | exponent claimed for this `φ` and ladder, `/a` | difference | difference × `√n` | difference in absolute units (`× a`) | `ln(C_max)/(n a)` minus worst found |
|---|---|---|---|---|---|---|---|---|
| 0.5 | 250 | 0.55 | 4.875 | 0.5480 | +4.327 | 68.4 | 0.1311 | 1.705 |
| 0.5 | 350 | 0.55 | 3.780 | 0.5486 | +3.231 | 60.4 | 0.0979 | 1.213 |
| 0.5 | 500 | 0.55 | 2.891 | 0.5500 | +2.341 | 52.3 | 0.0709 | 0.852 |
| 0.5 | 700 | 0.55 | 2.284 | 0.5500 | +1.734 | 45.9 | 0.0525 | 0.610 |
| 0.5 | 1000 | 0.55 | 1.829 | 0.5500 | +1.279 | 40.4 | 0.0387 | 0.416 |
| 0.5 | 1400 | 0.55 | 1.526 | 0.5500 | +0.976 | 36.5 | 0.0296 | 0.288 |
| 0.5 | 2000 | 0.55 | 1.259 | 0.5500 | +0.709 | 31.7 | 0.0215 | 0.227 |
| 0.5 | 4000 | 0.50 | 0.956 | 0.5046 | +0.451 | 28.5 | 0.0137 | 0.093 |
| 0.5 | 8000 | 0.50 | 0.763 | 0.5031 | +0.260 | 23.3 | 0.0079 | 0.051 |
| 0.5 | 16000 | 0.50 | 0.656 | 0.5031 | +0.153 | 19.4 | 0.0046 | 0.033 |
| 0.5 | 32000 | 0.50 | 0.597 | 0.5031 | +0.094 | 16.9 | 0.0029 | 0.020 |
| 0.5 | 64000 | 0.50 | 0.563 | 0.5031 | +0.060 | 15.2 | 0.0018 | 0.012 |
| 0.5 | 128000 | 0.50 | 0.542 | 0.5031 | +0.039 | 13.8 | 0.0012 | 0.007 |
| 1 | 250 | 0.60 | 2.081 | 0.6000 | +1.481 | 23.4 | 0.1643 | 0.456 |
| 1 | 350 | 0.60 | 1.718 | 0.6000 | +1.118 | 20.9 | 0.1240 | 0.360 |
| 1 | 500 | 0.55 | 1.399 | 0.5500 | +0.849 | 19.0 | 0.0941 | 0.237 |
| 1 | 700 | 0.55 | 1.190 | 0.5500 | +0.640 | 16.9 | 0.0710 | 0.185 |
| 1 | 1000 | 0.55 | 1.040 | 0.5500 | +0.490 | 15.5 | 0.0544 | 0.132 |
| 1 | 1400 | 0.50 | 0.924 | 0.5035 | +0.420 | 15.7 | 0.0466 | 0.068 |
| 1 | 2000 | 0.50 | 0.822 | 0.5032 | +0.319 | 14.3 | 0.0354 | 0.048 |
| 1 | 4000 | 0.50 | 0.694 | 0.5032 | +0.191 | 12.1 | 0.0212 | 0.029 |
| 1 | 8000 | 0.50 | 0.619 | 0.5032 | +0.116 | 10.4 | 0.0129 | 0.020 |
| 1 | 16000 | 0.50 | 0.576 | 0.5032 | +0.073 | 9.2 | 0.0080 | 0.013 |
| 1 | 32000 | 0.50 | 0.550 | 0.5032 | +0.046 | 8.3 | 0.0051 | 0.010 |
| 1 | 64000 | 0.50 | 0.537 | 0.5032 | +0.033 | 8.5 | 0.0037 | 0.005 |
| 1 | 128000 | 0.50 | 0.526 | 0.5032 | +0.023 | 8.1 | 0.0025 | 0.003 |
| 2 | 250 | 0.55 | 1.220 | 0.5511 | +0.669 | 10.6 | 0.2192 | 0.181 |
| 2 | 350 | 0.55 | 1.050 | 0.5517 | +0.498 | 9.3 | 0.1633 | 0.153 |
| 2 | 500 | 0.55 | 0.934 | 0.5531 | +0.381 | 8.5 | 0.1249 | 0.110 |
| 2 | 700 | 0.55 | 0.852 | 0.5531 | +0.299 | 7.9 | 0.0981 | 0.091 |
| 2 | 1000 | 0.50 | 0.773 | 0.5127 | +0.260 | 8.2 | 0.0852 | 0.033 |
| 2 | 1400 | 0.50 | 0.717 | 0.5127 | +0.204 | 7.6 | 0.0668 | 0.024 |
| 2 | 2000 | 0.50 | 0.668 | 0.5127 | +0.155 | 6.9 | 0.0508 | 0.022 |
| 2 | 4000 | 0.50 | 0.608 | 0.5127 | +0.095 | 6.0 | 0.0311 | 0.014 |
| 2 | 8000 | 0.50 | 0.573 | 0.5127 | +0.060 | 5.4 | 0.0198 | 0.017 |
| 2 | 16000 | 0.50 | 0.555 | 0.5127 | +0.042 | 5.3 | 0.0138 | 0.009 |
| 2 | 32000 | 0.50 | 0.541 | 0.5127 | +0.028 | 5.1 | 0.0093 | 0.005 |
| 2 | 64000 | 0.50 | 0.532 | 0.5127 | +0.019 | 4.9 | 0.0064 | 0.004 |
| 2 | 128000 | 0.50 | 0.526 | 0.5127 | +0.013 | 4.8 | 0.0044 | 0.002 |
<!-- /TABLE:trend -->

The difference falls from every size to the next, and its product with `√n` falls too
except at three steps, where it rises by 0.2–0.3 (twice where the best `φ` of the grid
changes, once at `u = 1`, `n = 64 000`): the worst case found approaches the claimed exponent
about as fast as the `O(√n)` term of the theorem allows.  The request's rule — stop when a
margin above `0.01` in the exponent persists from `n = 10⁴` to `10⁵` — is not met: in absolute
units the margin is below `0.01` from `n = 16 000` (`u = 1`), `8000` (`u = ½`) and `32 000` (`u = 2`)
on, and falling.  The last column shows that the cap `C_max` is nearly attained: at
`n = 128 000` the worst instance found is within `0.002–0.007·na` of it.

## 4. Every claim of Theorem 11.56 under optimisation pressure

For every instance evaluated in any search the slack of each claim was recorded; in job
M-009 the objective *was* the slack (cost against the cap; the count (v); the bound on
`M_j^neg`; the bound on the sample; claim (vi) per level), on 36 cells.

<!-- TABLE:claims -->
Instances evaluated: **7,095,840** (jobs M-008, M-009, M-010 together); runs that did not close within the level and sample caps: **0**; runs violating a claim: **0**.

| quantity | claimed | extreme over all instances, `u = ½` | `u = 1` | `u = 2` |
|---|---|---|---|---|
| `ln(cost) − ln(C_max)` | ≤ 0 (claim (vi): no abort for cost) | -10.374 | -9.433 | -9.402 |
| the count (v): `ln[M_j^neg p(s_j e^{−x})] − ln[(1+η)/(1−η) e^λ ν e^x]`, max over levels and rungs | ≤ 0 | -0.052 | -0.051 | -0.051 |
| claim (vi) per level: `ln[M_j p(s_j e^{−x_{l−1}})] − ln cnt(x_{l−1})` | ≤ 0 | -0.106 | -0.103 | -0.102 |
| claim (iv): `ln M_j^neg − ln[(1+η) e^λ ν₀ M†]` | ≤ 0 | -4.009 | -6.375 | -5.418 |
| claim (iv): `ln M_j − ln M̄` | ≤ 0 | -9.376 | -11.724 | -10.881 |
| claim (iv): `ln M_j − ln max(K, 2 M_j^neg)` | ≤ 0 | +0.0e+00 | +0.0e+00 | +0.0e+00 |
| width: `ln(U/L) − x_out` | ≤ 0 | -0.035 | -0.035 | -0.035 |
| validity: `ln L − ln A` | ≤ 0 | +2.7e-11 | +6.2e-11 | +1.6e-10 |
| validity: `ln A − ln U` | ≤ 0 | -0.009 | -0.012 | -0.014 |
| claim (iii): `ln q_j − ln π†` over levels left (minimum) | > 0 | +0.008 | +1.463 | +0.038 |
<!-- /TABLE:claims -->

Remarks.  (a) The count (v) — the step that five earlier versions of the accounting got
wrong (D45) — is the tightest claim, and it is tight under the behaviour "top" (first
table of the Summary; your simulations report 57–73 % of the bound).  It holds.  (b) The
bound `M̄` on the sample is the loosest: see the same table and the question at the end.
(c) `ln L − ln A` reaches zero to rounding: the initial lower bound `ℓ = e^{−ψ₀}((1+e^{−u})/2)^n` is
attained, for instance by the cone centred at the reference point with conical fibres.

Which instances, which behaviour:

<!-- TABLE:families -->
Cells: 468.
* General (non-monotone) profiles against monotone ones: the best general instance exceeds the best monotone one by at most `+0.0016·n a` (largest shortfall `-0.0608·n a`).
* Differential evolution against the structured starting points (flat, cones, plateau-then-cone, cone-then-flat): the search improved on the best starting point by at most `+0.1116·n a`; in 261 of 468 cells by less than `0.0001·n a`.
* The oracle "top" gives the larger cost in 2 of 468 cells, "bottom" (or a tie) in the others.
<!-- /TABLE:families -->

Which *structured* instance is the worst one, cell by cell (the 63 starting points of the
search evaluated on their own, both behaviours):

<!-- TABLE:seed_types -->
| cells | number | flat | cone | cone of slope u/2 | cone then flat | plateau then cone | largest gain of the search over the best structured point (`·n a`) |
|---|---|---|---|---|---|---|---|
| all | 468 | 4 | 69 | 0 | 283 | 112 | 0.1116 |
| `φ` below the best `φ` against the worst instance | 174 | 4 | 0 | 0 | 70 | 100 | 0.0822 |
| at that `φ` | 39 | 0 | 0 | 0 | 31 | 8 | 0.0930 |
| `φ` above it | 255 | 0 | 69 | 0 | 182 | 4 | 0.1116 |
| at the `φ` that is best for the flat instance | 39 | 0 | 7 | 0 | 32 | 0 | 0.1000 |
<!-- /TABLE:seed_types -->

<!-- TABLE:seed_radii -->
| maximiser | cells | radius of the change of slope, in units of the critical radius `Λ₁ n_o / u`: below 0.85 | 0.85–0.95 | 0.95–1.05 | 1.05–1.2 | above 1.2 |
|---|---|---|---|---|---|---|
| cone then flat | 283 | 46 | 19 | 29 | 139 | 50 |
| plateau then cone | 112 | 4 | 19 | 25 | 40 | 24 |
<!-- /TABLE:seed_radii -->

<!-- TABLE:seed_reference -->
Reference point of the best structured instance: at the median distance from the centre in 310 cells, at the centre in 142, at the antipode in 16; inner behaviour "bottom" in 443 cells, "top" in 25.
<!-- /TABLE:seed_reference -->

Reading.  The flat instance is the worst structured instance in 4 cells of 468.  The most
frequent maximiser is "cone then flat": a cone of slope `u` around a centre, cut off — in
half of these cells — at a radius 5–20 % above the critical radius `Λ₁n_o/u`, with a flat
profile beyond; in words, *a flat bulk with a slightly supercritical dip*.  To the right of
the best `φ` the full cone also occurs; to the left of it "plateau then cone" is frequent,
but there all instances cost nearly the same (table of the `φ`-profile in §2).  The profiles
that the search itself returns, for a few cells:

<!-- TABLE:maximisers -->
| `u` | `n` | `φ` | family / oracle | cost `/(n a)` | closing | sample `ln M/(n_o a)` | `r` of closure (`r†`, `p_u n_o`) | reference at radius | profile: (from, to, slope/`u`) |
|---|---|---|---|---|---|---|---|---|---|
| 0.5 | 1000 | 0.55 | monotone / bottom | 1.829 | unpopulated | 1.149 | 232 (182, 208) | 307 | `[(0, 55, 0.74), (56, 93, 0.26), (94, 110, 0.02), (111, 115, 0.0), (116, 130, 0.1), (131, 341, 0.0)]` |
| 0.5 | 1000 | 0.85 | monotone / bottom | 2.245 | unpopulated | 2.197 | 291 (289, 321) | 198 | `[(0, 59, 0.61), (60, 108, 0.77), (109, 356, 1.0), (357, 374, 0.88), (375, 416, 0.0), (417, 514, 0.72)]` |
| 0.5 | 64000 | 0.50 | general / bottom | 0.563 | unpopulated | 1.114 | 11896 (11883, 12081) | 32000 | `[(0, 10491, 1.0), (10492, 11786, -0.39), (11787, 12120, -0.95), (12121, 13295, -0.22), (13296, 15181, -0.71), (15182, 15388, -0.3)]` |
| 0.5 | 64000 | 0.55 | monotone / bottom | 0.615 | populated | 1.107 | 13096 (13082, 13289) | 29702 | `[(0, 13832, 1.0), (13833, 14401, 0.93), (14402, 15674, 0.74), (15675, 16275, 0.91), (16276, 16873, 0.37), (16874, 17339, 0.0)]` |
| 1 | 1000 | 0.55 | monotone / bottom | 1.040 | unpopulated | 1.724 | 121 (119, 148) | 187 | `[(0, 212, 1.0), (213, 253, 0.0), (254, 260, 0.3), (261, 266, 0.52), (267, 334, 0.02), (335, 430, 0.5)]` |
| 1 | 1000 | 0.80 | general / bottom | 1.338 | unpopulated | 1.552 | 183 (180, 215) | 430 | `[(0, 232, -0.67), (234, 295, 0.2), (296, 300, 0.39), (301, 312, -0.72), (313, 324, 0.82), (325, 350, 1.0)]` |
| 1 | 64000 | 0.50 | monotone / bottom | 0.537 | unpopulated | 1.062 | 8404 (8383, 8606) | 2151 | `[(0, 12124, 1.0), (12125, 12633, 0.04), (12634, 17912, 0.01), (17913, 24977, 0.62), (24978, 25914, 0.07), (25915, 28073, 0.16)]` |
| 1 | 64000 | 0.55 | monotone / bottom | 0.584 | unpopulated | 1.059 | 9255 (9233, 9467) | 17600 | `[(0, 17383, 1.0), (17384, 35200, 0.0)]` |
| 2 | 1000 | 0.50 | general / bottom | 0.773 | unpopulated | 0.845 | 81 (34, 60) | 242 | `[(0, 54, -0.23), (55, 85, 0.79), (86, 148, -0.55), (149, 201, 1.0), (202, 230, -0.62), (231, 244, 0.66)]` |
| 2 | 1000 | 0.65 | monotone / bottom | 0.896 | unpopulated | 1.327 | 52 (48, 77) | 650 | `[(0, 156, 1.0), (157, 159, 0.0), (160, 171, 0.7), (173, 210, 0.0), (211, 289, 0.46), (290, 418, 0.0)]` |
| 2 | 64000 | 0.50 | monotone / bottom | 0.532 | unpopulated | 1.037 | 3631 (3603, 3814) | 32000 | `[(0, 9360, 1.0), (9361, 9363, 0.03), (9364, 9416, 0.02), (9417, 9833, 0.0), (9834, 9905, 0.01), (9906, 32000, 0.0)]` |
<!-- /TABLE:maximisers -->

Where the search improves on the structured instances (by at most `0.12·na`, first table of
this paragraph) its profiles are less regular; we have not tried to interpret them.  A
larger search budget and other seeds do not change the result:

<!-- TABLE:converge -->
| `u` | `n` | `φ` | seed | budget (monotone / general) | worst found `/(n a)` | in job M-008 (seed 1, smaller budget) |
|---|---|---|---|---|---|---|
| 1 | 1000 | 0.50 | 2 | 20000 / 10000 | 1.0468 | 1.0466 |
| 1 | 1000 | 0.50 | 3 | 20000 / 10000 | 1.0467 | 1.0466 |
| 1 | 1000 | 0.65 | 2 | 20000 / 10000 | 1.1542 | 1.1542 |
| 1 | 1000 | 0.65 | 3 | 20000 / 10000 | 1.1542 | 1.1542 |
| 1 | 16000 | 0.50 | 2 | 12000 / 6000 | 0.5758 | 0.5757 |
| 1 | 16000 | 0.50 | 3 | 12000 / 6000 | 0.5758 | 0.5757 |
| 1 | 16000 | 0.65 | 2 | 12000 / 6000 | 0.7321 | 0.7321 |
| 1 | 16000 | 0.65 | 3 | 12000 / 6000 | 0.7321 | 0.7321 |
<!-- /TABLE:converge -->

## 5. Why radial instances are not "a small subfamily" for the outer loop (engineering argument; please check)

The request says: "Radial and bi-radial instances are a small subfamily of the class."  For
what the outer loop can see, this needs amending.

**Claim.**  Let `g` be `u`-Lipschitz on `Q_m`, `W = e^{−g}`, `m(t) = |{W > t}|`, and let `∂(k)` be the
size of the closed neighbourhood of the initial segment of size `k` of the simplicial order.
(a) `m` is nonincreasing, right-continuous, and `m(te^{−u}) ≥ ∂(m(t))` for every `t`.
(b) Conversely, every nonincreasing right-continuous `m` with values in `{0, …, 2^m}`, equal to
`2^m` below some threshold and to `0` above another, with `m(te^{−u}) ≥ ∂(m(t))` for all `t`, is the
tail function of a `u`-Lipschitz `g` whose level sets are initial segments.
(c) Hence the laws of `W` that outer landscapes can have are exactly the tail functions of
(a); and those whose level sets are *balls* are exactly the monotone radial profiles with
increments in `[0, u]` (because `∂(|B(r)|) = |B(r+1)|`).

*Argument.*  (a) If `x` is in the neighbourhood of `S_t = {W > t}` then `W(x) ≥ W(y)e^{−u} > te^{−u}` for
a neighbour `y ∈ S_t`; so `N(S_t) ⊆ S_{te^{−u}}`, and `|N(S_t)| ≥ ∂(|S_t|)` is Harper's theorem **[K]**.
(b) Put `S_t :=` the initial segment of size `m(t)` and `W(x) := sup{t : x ∈ S_t}`.  Then
`{W > t} = S_t` by right-continuity, and for neighbours `x, y` and every `t < W(y)`:
`y ∈ S_t`, `x ∈ N(S_t)`, which is the initial segment of size `∂(m(t))` (the neighbourhood of an
initial segment is an initial segment **[K]**), contained in `S_{te^{−u}}`; so `W(x) ≥ W(y)e^{−u}`.  ∎

Consequence.  With a fixed inner behaviour, the mean run on *any* `u`-Lipschitz instance is
the mean run on an instance whose outer level sets are initial segments of the simplicial
order; monotone radial profiles are those with whole balls, and they differ from the
general case only by partial shells.  So for the outer loop the search of §2 is over the
whole class up to the granularity of one shell — and the data agree: general profiles never
beat monotone ones by more than `0.002·na`.  What the reduction does **not** cover: partial
shells; fibres that differ from point to point other than by their value at the reference
(one offset `c_in` for all points here); inner behaviours between "bottom" and "top"; and the
search itself, which is heuristic within the family (eight knots).

## 6. Part A, outer loop: literal runs with real fluctuations (experiment X-006)

A literal implementation (`simulate.py`) follows the algorithm pass by pass on an outer
sample drawn at random — counts per shell and per block of the doubling sequence, sampled
with a multinomial routine that is exact in the far tail — with the abort rule, and checks
the good event (V2)–(V3) on the realised sample and every claim of the theorem on every
run.  It shares only the cube tables with the evaluator of §§1–4.  Job M-011: 13 radial
landscapes (flat, cone, cone of slope `u/2`, anti-cone, two plateau-then-cone, three dips
around the critical radius, the staircase `W ∝ 1/|B(d)|`, the 2-periodic profile, a random
walk, a random monotone profile) × `(u, n_o) ∈ {(½, 300), (1, 120), (2, 48)}`, `n_i = 6` × three
inner behaviours (bottom, top, random; one bracket per group of points) × five values of
`K`: the theorem's and that value divided by 4, 16, 64, 256.  Design parameters `b = 0.5`,
`λ = 0.5`, `η = ¼`, `η′ = θ = 0.1`, `δ = 0.05`.

<!-- TABLE:sampled_headline -->
With the theorem's `K` (953–979): **585,000 literal runs** on 13 landscapes, three sizes and three inner behaviours; runs in which the good event failed, a bracket was invalid, the width bound was exceeded, a claim was violated or the run aborted: **0**.  With no failure in 585,000 runs, the frequency of each of these events is below `5.1e-06` at 95 % confidence (pooled over cases).
<!-- /TABLE:sampled_headline -->

<!-- TABLE:sampled -->
| `u` | `n_o` | `K` (scale) | runs | good event failed | bracket invalid | of these on the good event | width bound exceeded | another claim violated on the good event | aborted | mean `ln(evaluations)` minus mean run: bottom / top |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.5 | 300 | 979 (1) | 195,000 | 0 | 0 | 0 | 0 | 0 | 0 | +0.00 / +0.00 |
| 0.5 | 300 | 245 (1/4) | 39,000 | 82 | 0 | 0 | 0 | 0 | 0 | — |
| 0.5 | 300 | 61 (1/16) | 39,000 | 14,668 | 0 | 0 | 0 | 0 | 0 | — |
| 0.5 | 300 | 15 (1/64) | 39,000 | 29,408 | 10 | 0 | 0 | 0 | 0 | — |
| 0.5 | 300 | 4 (1/256) | 39,000 | 31,698 | 1,188 | 0 | 0 | 0 | 0 | — |
| 1 | 120 | 968 (1) | 195,000 | 0 | 0 | 0 | 0 | 0 | 0 | -0.00 / +0.00 |
| 1 | 120 | 242 (1/4) | 39,000 | 47 | 0 | 0 | 0 | 0 | 0 | — |
| 1 | 120 | 60 (1/16) | 39,000 | 14,013 | 0 | 0 | 0 | 0 | 0 | — |
| 1 | 120 | 15 (1/64) | 39,000 | 30,082 | 18 | 0 | 0 | 0 | 0 | — |
| 1 | 120 | 4 (1/256) | 39,000 | 32,152 | 1,106 | 0 | 0 | 0 | 0 | — |
| 2 | 48 | 953 (1) | 195,000 | 0 | 0 | 0 | 0 | 0 | 0 | -0.00 / -0.00 |
| 2 | 48 | 238 (1/4) | 39,000 | 67 | 0 | 0 | 0 | 0 | 0 | — |
| 2 | 48 | 60 (1/16) | 39,000 | 13,080 | 0 | 0 | 0 | 0 | 0 | — |
| 2 | 48 | 15 (1/64) | 39,000 | 32,031 | 65 | 0 | 0 | 0 | 0 | — |
| 2 | 48 | 4 (1/256) | 39,000 | 34,413 | 868 | 0 | 0 | 0 | 0 | — |
<!-- /TABLE:sampled -->

Worst case over the 117 cases at each value of `K`:

<!-- TABLE:sampled_worst -->
| `K` scale | cases | runs per case | largest fraction of runs with the good event failed (landscape, inner behaviour, `u`) | largest fraction of runs with an invalid bracket (landscape, inner behaviour, `u`) | cases with at least one invalid bracket |
|---|---|---|---|---|---|
| 1 | 117 | 5,000 | 0 | 0 | 0 |
| 1/4 | 117 | 1,000 | 1.1 % (dip R=1.1 Lambda1 n_o/u, random, 0.5) | 0 | 0 |
| 1/16 | 117 | 1,000 | 64.1 % (anti-cone, bottom, 0.5) | 0 | 0 |
| 1/64 | 117 | 1,000 | 100.0 % (cone, bottom, 0.5) | 2.7 % (random walk, bottom, 2) | 9 |
| 1/256 | 117 | 1,000 | 100.0 % (cone slope u/2, random, 0.5) | 18.8 % (random walk, bottom, 2) | 88 |
<!-- /TABLE:sampled_worst -->

By landscape, all reduced values of `K` together:

<!-- TABLE:sampled_profiles -->
| landscape | runs with `K` scaled down | good event failed | bracket invalid |
|---|---|---|---|
| staircase W ~ 1/|B(d)| | 36,000 | 23,114 (64 %) | 259 (0.72 %) |
| cone | 36,000 | 23,113 (64 %) | 307 (0.85 %) |
| anti-cone | 36,000 | 23,060 (64 %) | 349 (0.97 %) |
| plateau below r_dag+1, cone above | 36,000 | 22,960 (64 %) | 342 (0.95 %) |
| dip R=1.1 Lambda1 n_o/u | 36,000 | 22,557 (63 %) | 319 (0.89 %) |
| cone slope u/2 | 36,000 | 22,169 (62 %) | 174 (0.48 %) |
| dip R=1.0 Lambda1 n_o/u | 36,000 | 21,891 (61 %) | 16 (0.04 %) |
| plateau below p_u n_o, cone above | 36,000 | 21,749 (60 %) | 329 (0.91 %) |
| random monotone | 36,000 | 21,444 (60 %) | 490 (1.36 %) |
| random walk | 36,000 | 16,244 (45 %) | 342 (0.95 %) |
| dip R=0.9 Lambda1 n_o/u | 36,000 | 7,638 (21 %) | 0 (0.00 %) |
| 2-periodic | 36,000 | 5,802 (16 %) | 328 (0.91 %) |
| flat | 36,000 | 0 (0 %) | 0 (0.00 %) |
<!-- /TABLE:sampled_profiles -->

Reading.
* **With the theorem's `K` nothing failed**, and the literal runs make the same number of
  evaluations as the mean run (last column of the first table) — the independent check of
  the evaluator of §§1–4.
* **Where the events start to fail** (the question of the request): the good event
  (V2)–(V3) begins to fail at `K/4` (one or two runs in a thousand) and fails in most runs
  from `K/64` on; **no bracket was invalid at `K/4` and `K/16`** (234 000 runs), the first
  invalid brackets appear at `K/64` (fewer than one in a thousand overall), and at `K/256` —
  `K = 4` — 2.7 % of all brackets are invalid, up to 19 % on one landscape.
* **Every invalid bracket occurred on a run on which the good event had failed**, as the
  theorem requires; the width bound held in all runs, as it must whenever the algorithm
  stops through the closure test; no run aborted; no other claim failed on the good event.
* The flat instance never fails: its counts do not fluctuate.

So at these sizes the events of the proof are sufficient and far from necessary: the
constant `K` of the theorem (a union bound over `(J+1)(m_max+1)(L+2)` events) could be
divided by 16 without a single invalid bracket in 117 000 runs.  This says nothing about
large `n`, where the number of events grows.

The inner procedures in these runs are oracles (valid brackets by construction), so the
event (V1) of the proof is not tested.  One implementation pitfall surfaced and is
described in ENG-MSG-0003 §5 (a tie at the last rung, with a structural cause).

## What this does and does not say about the theory

* It does **not** contradict Theorem 11.56 or Theorem 11.58: the worst case found stays
  below the theorem's own cap `C_max`, and both approach the claimed exponent as `n` grows
  (§3).
* It **does** correct a reading of the published numbers.  "What the algorithm costs" in
  `K_REPORT.md` §6.4 (and wherever the theory report quotes it) is the cost *at the flat
  instance with `φ` tuned for the flat instance*.  As a statement about the algorithm it
  should be replaced by the worst-case column of §2 — larger in the exponent by the
  ratios of the last table of §2: 11–49 % at `n ≤ 2000`, between 1 % and 11 % at the two
  largest sizes — or be labelled as a best case.  The flat instance is where the lower bound
  for every algorithm is proved; it is not the instance on which *this* algorithm, with
  these parameters, works hardest.
* The same caveat applies to the exact three-level numbers at the flat instance quoted in
  THY-MSG-0007 §3 (`0.712, 0.460, 0.405, 0.379`).  We have not computed three levels; we
  expect the mechanism of §2 to act at every level that draws an outer sample, and that
  expectation is untested.

## Execution environment, resources, reproduction

Local: Ubuntu under WSL2, 8 threads; Python 3.12, NumPy, SciPy; a C kernel compiled with the
system compiler (`src/metricchain_eng/twolevel/meanrun_kernel.c`), tested against the Python
reference implementation (`meanrun.py`).  Remote: Modal, one core per task, jobs M-008 … M-011
of `docs/engineering/COMPUTE_LEDGER.md` (bounds, measured cost).  Remote and local results
are bit-identical on the cases compared.  Job M-008 ran before the tie rule of ENG-MSG-0003
§5 existed; every stored maximiser and every flat-instance value was re-evaluated locally
with the final code (`recheck.py`): with plain floating-point comparisons all 2 808 stored
values of that job are reproduced exactly, and with the tie rule the largest change of
`ln(cost)` is `0.69` (one doubling of the sample, on one instance), at most `0.0015·na` — so
the third decimal of the tables of §2 can move by a unit or two in a few cells — and no
claim is violated under either convention.

```
python -m pytest tests/eng/test_twolevel.py -q
python experiments/eng/twolevel/controls.py --theory <checkout of the theory branch at 63efc69>
python experiments/eng/twolevel/run_search.py --u 1 --n 1000 --phi 0.5 0.8          # two cells, locally
modal run modal_jobs/twolevel_app.py::main --job cost                              # all 468 cells
python experiments/eng/twolevel/recheck.py
python experiments/eng/twolevel/make_tables.py --verify docs/collaboration/responses/engineering/ENG-RES-0008.md
```

Raw results: `experiments/eng/twolevel/results/x005_cost.jsonl`, `x005_claims.jsonl`,
`x005_converge.jsonl` (per cell: constants, flat instance, and per search the best point, its
decoded profile, the run, and the extremes of every claim over all instances evaluated).

## Assumptions and limitations

1. Mean runs: fluctuations of the counts are ignored in §§2–4 (§6 addresses the outer loop
   at small size only).
2. One set of design parameters (yours).  A different ladder, `λ`, `η`, `θ` would move the
   numbers; the mechanism of §2 does not depend on them.
3. Base family inside: two levels only.  With an adaptive inner procedure the inner cost
   depends on the fibre, which the present instance description (one offset) does not
   capture.
4. The search is heuristic and is a lower bound on the worst case; §5 limits what it could
   have missed for the outer loop but is itself unrefereed.
5. Sizes: `n ≤ 128 000`.  The trend of §3 is an extrapolation in the usual sense.

## Recommended theoretical follow-up

1. Label the table of §6.4 as a best case, or replace it by a worst-case table; state in
   the theory report which `φ` the two-level algorithm should be run with (0.50–0.60 on our
   grid, 0.50 from `n = 4000` on, by §2).
2. **Can `M̄` be lowered?**  In all instances evaluated the sample stayed below `2M†`
   (Summary, first table), while `M̄ = 2(1+η)e^λ ν₀ M†` is larger by a factor of order `ν₀`, and
   `ln ν₀` is between 8.9 and 17.3 over the cells run.
   A level that is *left* has `q_j > π†` (your Step 5), hence `M_j < M†` if it is negligible
   (your Step 6) and `M_j < 2M†` if it is populated, in a mean run (`N < 2K` at the first pass
   with `N ≥ K`); only the closing level can exceed that.  If `M ≤ c·M†` could be proved for the closing level too, `C_max` would lose a
   factor of order `ν₀` in its first term — invisible in the exponent, but a tenth of `na` at
   `u = 1`, `n = 1000` (`ln ν₀ = 11.1`).
3. Check §5.  If it stands, "for all `u`-Lipschitz outer landscapes" can be tested
   exhaustively over tail functions at small `n_o`, which nobody has done.

## Requested response

None required; an answer to the two questions of ENG-MSG-0003 and to item 2 above would
help decide what to compute next (three levels, or the extensive regime).
