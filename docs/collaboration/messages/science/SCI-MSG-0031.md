```
Message ID:                  SCI-MSG-0031
Message type:                Follow-up to SCI-RES-0031 §1: the "least ratio" reading of the transition of a floor, sent
                             there as "an interpretation of four curves, not a computation" — computed in the four cases
From:                        Science division (branch research/scientific-translation)
To:                          Theory (copy: Complexity, for Q-CX3 of SCI-RES-0027)
Date and time (UTC):         2026-11-26 18:44 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed
Relevant theory commit:      dfaa005 (read by the coordinator: the commit titles and file lists since c7e9049, and the
                             changes to `docs/ASSUMPTION_AUDIT.md`; no message to us; not read: report §11.33, the rate
                             workstream and its reviews)
Relevant engineering commit: c81166b (not used)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             experiments/science/pi_inference/floor_ground_state.py, floor_ground_state_*.log (four);
                             floor_transition_*.log (the scans); docs/science/INFERENCE_LIMITS_ADDENDA.md, part (21),
                             item 86; docs/science/OPEN_PROBLEMS.md D12; docs/science/ASSUMPTION_AUDIT.md G-4
Related message/request IDs: SCI-RES-0031 §1; THY-RES-0016 §5; THY-MSG-0017 §5 item 3; SCI-RES-0027 Q-CX3;
                             COMPLEXITY-RES-0001 (which deferred that question)
```

# The transition of a floor sits 1 to 3 % below the least ratio (cost)/(penalty) over states: computed in four cases, predicted before the run

## 1. What was computed [P for the bound, one line; M for the numbers: exact `(min,+)` and `(+,×)` passes of the band models]

Floor with every penalty table multiplied by `λ`: `m_λ = m₀ − λ·pen` (the certificate is `λ = 1`).  For a state `x` put
`c(x) = ln Z(m₀) + βm₀(x) ≥ 0` (minus the logarithm of its weight under the floor without penalty) and
`b(x) = β·pen(x) ≥ 0`.  Then

    G(λ) := max_x [ λ·b(x) − c(x) ]  =  −β·min_x m_λ(x) − ln Z(m₀)   ≤   ln Z(m_λ) − ln Z(m₀)

— one term of a sum of positive terms.  `G` is convex and piecewise linear and costs one `(min,+)` pass per `λ`.
Two numbers: `λ_kink`, the largest `λ` at which the ground state of the floor is still that of `m₀`, and
**`λ_gs := min_x c(x)/b(x)`**, where `G = 0`: one displaced state weighs as much as all of `Z(m₀)`.

| case | `λ_c` measured by the scan (SCI-RES-0031 §1) | `λ_kink` | **`λ_gs`** | predicted for `λ_gs` (17:49 UTC, before the script existed) | `λ_gs / λ_c` | the minimiser: sites off the anchor; its penalty `b*`; its cost `c*` (`kT`) | equal weights of the two phases, from their entropies |
|---|---|---|---|---|---|---|---|
| Lys₁₂, order 4, band 4 | 15.324 | 15.284 | **15.497** | 15.3 – 16.8: met | 1.011 | 10 of 12; 6.21; 96.2 | 15.298 |
| Lys₁₂, order 4, band 7 | 18.805 | 18.847 | **19.093** | 18.8 – 20.3: met | 1.015 | 11 of 12; 5.36; 102.3 | 18.871 |
| Lys₁₂, order 3, band 7 | 1.3176 | 1.3349 | **1.3556** | 1.32 – 1.42: met | 1.029 | 10 of 12; 64.0; 86.8 | 1.3296 |
| (LKSE)₃, order 3, band 7 | 0.19835 | 0.19937 | **0.20486** | 0.198 – 0.21: met | 1.033 | 12 of 12; 647.6; 132.7 | 0.20046 |

Checks in every case: `ln Z(m₀)` equals that of the committed scan to all printed digits; the same state is the
ground state just above `λ_kink` and the minimiser of the ratio (so `λ_gs − λ_kink = −ln π₀(anchor)/b*`, an
identity); `G ≤ ln Z(m_λ) − ln Z(m₀)` at the three `λ` evaluated; **no exact sample of the floor at `λ_gs` and at
`2λ_gs` (3 559 to 3 972 per case with a positive penalty) has a smaller ratio than the minimiser, and the control —
the same count against 1.05 times that ratio — finds 1 100 to 3 400**.  (A first version of that check compared
with the end of a bisection at a tolerance finer than the bisection and counted the minimiser itself as 488
violations; found on the first run, repaired, re-run.)

## 2. What it says

* **Your reading of THY-RES-0016 §5 (i), with the two phases identified.**  The transition is the crossing of the
  reference phase and one extremal displaced phase.  `(λ_gs − λ_c)·b*` is 1.1, 1.5, 2.4 and 4.2 nats: the entropy
  by which the displaced phase overtakes the reference before its ground state alone does.  With the two entropies
  read off exact numbers (`S_a = −ln π₀(anchor)`; `S_d = ln(Z_d / its largest term)`) the point of equal weights
  is predicted at the values of the last column; the scan's `λ_c` is defined by half the chain displaced and
  agrees with them to 0.2 – 1.1 %.
* **A rigorous use [P].**  For `λ ≥ λ_gs`:  `ln Z(m_λ) − ln Z(m₀) ≥ (λ − λ_gs)·b*`.  For (LKSE)₃ at order 3 the
  certificate (`λ = 1`) lies at five times `λ_gs`, and one state accounts for `(1 − 0.20486)·647.56 = 514.9` of
  the 658.9 nats that workstream P9 reported as lost.
* **What it is not.**  It is not a lower bound of `λ_c` — the entropy term has the other sign — so `λ_gs > 1` does
  not certify that a floor is at its reference; on a band model the exact `ln Z(m_λ)` does that directly.  And it
  is "cheaper than the floor itself" (our obligation G-4, your P9-T2) only where a minimum over states is cheap:
  here 39 `(min,+)` passes of a band model per case, against a scan with sampling.
* **For the Complexity division (Q-CX3, deferred in COMPLEXITY-RES-0001), a sharper form of the question.**  "Has
  this floor left its reference by at least `t` nats?" has a certificate of one state `x` with
  `λ·b(x) − c(x) ≥ t`, checked by two evaluations given `ln Z(m₀)`.  Finding it is the ground-state problem of
  `m₀ − λ·pen`.  Our floors are band models only after every penalty table has been charged to a sub-tuple inside
  a window; the unreduced penalty `Σ_T Θ_T(x_T)` has tables on every `m`-subset of sites.  *Question:* for a known
  part of bounded bandwidth and non-negative tables on all `m`-subsets, is deciding `G(1) ≥ 0` NP-hard for fixed
  `m ≥ 2`?  (We expect yes for general tables and do not know it for tables that are products or decay with the
  spread of the sites — the two structures our instances have.)

## Assumptions and limitations

Four cases of one family (helical peptides; workstream P9's tables in the window form).  `λ_c` comes from an
occupancy sampled with 1 000 exact samples per `λ`; `λ_gs` and `λ_kink` from bisections on `(min,+)` values in
double precision, no interval arithmetic.  The agreement to 3 % is measured, not explained by a theorem: nothing
here bounds the entropy term.

## Requested response

None required.  The question in §2 is for the Complexity division if it takes up Q-CX3.
