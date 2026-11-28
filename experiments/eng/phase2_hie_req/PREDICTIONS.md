# Predictions and pass/fail criteria (written before any computation)

Written 2026-11-28 02:51 UTC (`date -u`), before any script of this directory was run.
Source of the criteria: HIE-REQ-0001 (branch `research/phase2-adaptive-hierarchy`, commit `0ec16b8`),
`docs/collaboration/requests/hierarchy/HIE-REQ-0001.md`, Q1 and Q2.  Q3 is not done (coordinator's decision).

## Q1 — Lemma B as a falsification test

Quantity per case: `V = max_y [ ν*(y) − nφ_P h + min{t_T(y), Θ − n(1−φ_P)h} ]`, where `ν* = G − t` and `G = −F`
is the pointwise largest `−F` under admissibility, (H1), (H2) and `ν ≤ 0` on `V_∅(Θ)`.

* **Lemma criterion (pass/fail):** `V ≤ m(u + 5 ln(n+1))` in every case.  One case above it refutes Lemma B as
  stated (to be re-checked by an independent LP / Dijkstra before reporting).
* **Their expectation (not a lemma criterion, checked and reported separately):** `V ≲ 5` nats in every case;
  and, for `Θ ≥ 1.1nh`, `max over {y : t_T(y) > Θ}` of the same bracket `≤ 0.01` nats.
* **My prediction:** all cases pass the lemma criterion with a wide margin (allowance ~90–115 nats); the
  largest `V` is about `+5` (u = 4, Θ = nh), matching their stored `+4.952`; my per-case numbers agree with
  their stored `viol` column to rounding (≤ 1e-3) if I read the definitions as they did.
* **Cross-checks:** min-plus fixed point = Dijkstra (independent code) to 1e-9 on moderate grids;
  = HiGHS LP optimum (constraints enumerated pairwise, no shared class code) to 1e-6 on tiny grids.
* **Negative controls (must fail):** dropping (H2), and dropping both (H1),(H2), should produce `V` above
  the allowance on suitable (larger-`n_T`) cases; at least the sharp 0.01 bound for hidden types must be
  violated when (H2) is dropped.  If a negative control does not violate, the pass is less informative and
  this will be said.

## Q2 — Algorithm R3 on real cubes

* (a) Every revealing point's candidate is `s^j` or its antipode: **no exception allowed**.
* (b) Mean of `Â` over repeated runs within 3 standard errors of `A(ψ)` in **≥ 95 %** of (instance, M) tests.
* (c) When all blocks are revealed (S₂ = [m]), `Â = A(ψ)` exactly (to floating-point rounding, relative
  1e-12): **no exception allowed**.
* Mutation (shell weights `P_j(a_j)` → uniform `1/(n_j+1)`): must show a bias — predicted: |z| > 3 in most
  tests, and a deterministic error whenever all blocks are revealed.
* My prediction: (a), (b), (c) pass; the mutation is caught.
