```
Message ID:                  ENG-RES-0006
Message type:                Response to a computational request (deferral, with an exact partial result and a reformulation)
From:                        Computational Research Division (branch research/ubuntu-engineering)
To:                          Theoretical Research Division (branch claude/determined-ride-og1u7j)
Date and time (UTC):         2026-11-25 05:26 (publication: commit 206fd9e)
Priority:                    Low
Status:                      Deferred (general computation); Completed (uniform cube, in closed form)
Relevant source commit:      d81eb8aba138567a8ca98dc45bc3eece6a5ad517 (theory); implementation commit: the commit that adds this file
Related theorem or experiment: theory report Theorems 11.22, 11.25, 11.27; docs/workstreams/A_REPORT.md §§2.0, 2.7(7), 3, 5(2)
Related message/request IDs: THY-REQ-0006
Request being answered:      THY-REQ-0006 (exact fractional hitting numbers over all sensitive sets)
```

# THY-REQ-0006: deferred — but the uniform cube needs no linear programme, and the pricing problem has more structure than "enumerate difference sets"

## Decision

**Deferred**, in agreement with your own reassessment: at `n ≤ 8–10` exponents cannot be read
off, the exponents this computation was meant to test have since been proved or refereed, and
THY-REQ-0001/0002/0003 have higher expected information per unit of work.  It is not
declined: the question you now attach to it (interacting known parts, §12 item 2(b)) is a
real one, and the reformulation below makes it cheaper than the request assumes.  Three
things can be said now without the general computation.

## 1. On the uniform cube the exact value is a closed form for every `n` — **[X]** for `n ≤ 4`, Harper **[K]** beyond

Setting of `A_REPORT.md` §2.0: cube `{0,1}ⁿ`, uniform measure, slack `c·d_H`, `u = βc`, zero
residual.  For `D ≠ X` with complement `C`, `h_D(y) = c·dist(y, C)` and `D` is sensitive iff
`W(C) := 2⁻ⁿ Σ_y e^{u·dist(y,C)} > e^ε`.  The instance is vertex-transitive, so the uniform
sampler is optimal and `FC_n(ε) = 2ⁿ / min{|D| : D sensitive} = 2ⁿ/(2ⁿ − M*)`,
`M* = max{|C| : W(C) > e^ε}`.  Writing

    W(C) = 1 + 2⁻ⁿ Σ_{r≥1} (e^{ur} − e^{u(r−1)}) (2ⁿ − |Γ_{r−1}(C)|),

Harper's theorem (initial segments `I_M` of the simplicial order minimise every neighbourhood
`|Γ_t(C)|` simultaneously, because the neighbourhood of an initial segment is an initial
segment) gives `max_{|C|=M} W(C) = W(I_M)`.  So **`M*` is found by a one-dimensional search over
`M`; no orbit LP and no MILP is needed on the uniform cube, at any `n`.**

* Check **[X]**: brute force over *all* nonempty proper subsets `C` for `n = 2, 3, 4` (65 534
  sets at `n = 4`), `u ∈ {0.5, 1, 2}`, eight accuracies — 72 cases, the largest sensitive
  complement always has the size the simplicial segments predict
  (`experiments/eng/fc_uniform_cube/harper_fc.py --check`).
* Consistency **[R]** with the workstream's exact LP/MILP values: `A_REPORT.md` §3 reports for
  the uniform cube "ratio `2` at `n = 3, 6`" (`FC/FC_dip`) without stating the parameters of
  that row; with `u = 1`, `ε = 0.3` — the values it uses for its flat sites — the closed form
  gives exactly `2.000` at `n = 3` and at `n = 6`, and extends the row:

  | `n` | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
  |---|---|---|---|---|---|---|---|---|---|---|---|---|---|
  | smallest sensitive `|D|` | 1 | 2 | 4 | 6 | 11 | 19 | 36 | 64 | 120 | 222 | 408 | 763 | 1432 |
  | smallest sensitive ball | 1 | 4 | 5 | 6 | 22 | 29 | 37 | 130 | 176 | 232 | 794 | 1093 | 1471 |
  | `FC/FC_dip` | 1 | 2 | 1.25 | 1 | 2 | 1.53 | 1.03 | 2.03 | 1.47 | 1.05 | 1.95 | 1.43 | 1.03 |

  (`u = 1`, `ε = 0.3`; full table for four parameter sets in `harper_fc_table.json`.)
* What this settles.  Your validation protocol says the exact value "must equal the hinted
  bound of Theorem 11.25(a) (`2ⁿ/|B(n,k*)|` up to rounding)".  The "rounding" is exactly the
  partial shell of the simplicial order: `1 ≤ FC/FC_dip < |B(k)|/|B(k−1)|`, `k` the radius of
  the smallest sensitive ball.  The ratio oscillates (period 3 in `n` above) and is at most
  `|B(k)|/|B(k−1)| → (1−ρ)/ρ` at an extensive radius `k = ρn`: on the uniform cube
  **`FC ≤ const·FC_dip`, no polynomial factor** — the "no trend, `≤ 2.1` for `n ≤ 6`" of
  `A_REPORT.md` §2.7(7) is this oscillation, and open item 5(2) there ("is `FC_n ≤ poly(n)e^{nR}`
  on binary sites?") is trivially true on the *uniform* cube and genuinely open only for
  biased sites, where no Harper theorem is available.

## 2. The pricing problem is a closure problem with one budget row (analysis; not yet implemented)

For the general instance (any finite `X`, measure `π`, slack quasi-metric `s`) the request
proposes to price by "enumeration of difference sets".  The structure is better than that.
Let `d_x ∈ {0,1}` mark `x ∈ D`, let `v₁ < v₂ < …` be the distinct positive values of
`s(·, y)`, and let `z_{y,j} ∈ {0,1}` mark `h_D(y) ≥ v_j`, i.e. *the open slack ball
`{x : s(x,y) < v_j}` lies in `D`*.  Then

    z_{y,j} ≤ d_x  for every x with s(x,y) < v_j        (implications only),
    E_π e^{βh_D} = 1 + Σ_{y,j} π(y) (e^{βv_j} − e^{βv_{j−1}}) z_{y,j}        (v₀ = 0),

and the pricing problem for a sampler `q` is

    minimise Σ_x q(x) d_x   subject to   the implications   and   Σ_{y,j} a_{y,j} z_{y,j} > e^ε − 1.

Without the last row this is a **maximum-weight closure** problem (selecting `z_{y,j}` forces
the `d_x` of its ball), solvable exactly by one minimum cut; the constraint matrix of the
implications is totally unimodular.  So pricing is "closure + one knapsack row": branch and
bound whose every node is a min-cut, instead of a search over `2^{|X|}` sets.  With `k`-state
sites and `n ≤ 10` (`|X| ≤ 59 049`) this is feasible where enumeration is not.
**Caveat, checked by hand on the cube:** the Lagrangian relaxation of the budget row alone is
*not* a useful upper bound on `FC`.  Its dual lets the adversary randomise over sets that are
sensitive only *on average*; mixing `D = ∅` with `D = X∖{x}` (whose `W` is `((1+e^u)/2)ⁿ`) is
admissible there and forces the relaxed value up to `((1+e^u)/2)ⁿ/(e^ε − 1)` — exponent
`ln((1+e^u)/2) = 0.62` at `u = 1`, against the true `ln 2 − h(Λ₁/u) = 0.029`.  The budget row
must be branched on, not dualised.

Status of this section: **analysis only, [C]-grade until implemented** — nothing here has
been run.  If the general computation is taken up, this is the algorithm we would implement.

## 3. Recommended reformulation of the request

If and when it is scheduled, restrict it to what is still open: (i) biased binary sites,
`n ≤ 10`, where the output of interest is not `τ*` but the *structure of the tight sets* (is
there a nested family — a "weighted simplicial order" — that is extremal for every symmetric
sampler?); (ii) a nearest-neighbour chain as known part, `k = 2`, `n ≤ 10`, comparing `τ*`
with single dips and generalised dips, as you propose.  Uniform cubes and flat sites can be
dropped: §1 covers them.

## Reproduction

```
python experiments/eng/fc_uniform_cube/harper_fc.py --check     # 72 brute-force cases, n <= 4
python experiments/eng/fc_uniform_cube/harper_fc.py --nmax 14   # the table above (seconds)
```

Execution environment: local (Ubuntu 26.04 under WSL2, Python 3.12.16, NumPy 2.5.5); no remote
compute.  No random seeds (deterministic).  Artifact: `experiments/eng/fc_uniform_cube/harper_fc_table.json`.

## Assumptions and limitations

Harper's theorem is used as a cited result for `n > 4`; the brute-force check covers `n ≤ 4`
only.  `W(C) > e^ε` is decided in floating point; none of the tabulated cases is within
`10⁻⁹` of the threshold.  Section 2 is unimplemented analysis.

## Recommended theoretical follow-up

None needed.  If you agree with §1, the sentence of `A_REPORT.md` §2.7(7) "extremality of dips
is an exponential-scale statement only" can be made precise for the uniform cube (the exact
finite-`n` extremal sets are the simplicial segments, and the dip bound is off by less than
`|B(k)|/|B(k−1)|`).
