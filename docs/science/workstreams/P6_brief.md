# Workstream P6 (launched after checkpoint 43, 2026-11-26) — pair penalties in the certified sandwich: does a lower order suffice at twenty residues, and how far does the certificate reach?

> **Finished 2026-11-26: report `P6_REPORT.md`, published as SCI-MSG-0025.**  The brief below is kept as launched.

*Brief written by the coordinator.  Read `COMMON.md` first (its commit pins are out of
date: the theory branch is at `24a3c27`, a read-only export of it is in the session
scratchpad under `thy_ro_24a3c27/`), then `P3_REPORT.md` in full, then `P4_REPORT.md` §2.6
and §6 item 2.  If the agent of this workstream is gone, its notes and draft are in
`experiments/science/ws_P6/` and `P6_REPORT.md`.*

## Why

Workstream P3 certified `ln Z` of Ace-Val₂₀-NMe on a polyproline backbone (`3.49·10⁹`
rotamer assignments) with **no sampling**: `[518.2332, 518.2937]` from 87 441 evaluations
of the GBn2 term (order `m = 5`: values on the Hamming ball of radius 4 about an anchor,
a certified bound on the tail, a sandwich `m₋ ≤ E ≤ m₊` of banded pairwise models solved
by transfer matrices).  At `m = 4` (9 921 evaluations) the bracket is `[517.4843, 519.2199]`
— too wide to be useful.  P3 distributed each certified tail constant `ĉ_T` (`|T| = m`)
equally over the **sites** of `T`: `γ_i = (1/m) Σ_{T∋i} ĉ_T`.

The theory division then proved (Theorem 11.18a, for `m = 3`, machine-checked) that
distributing over the **pairs** of `T` is pointwise tighter, and our workstream P4 stated
the order-`m` version with a *banded* variant that keeps the models exactly solvable
(Proposition P4.6) and measured on enumerated grids, with P3's own certified constants,
**cost numbers falling from 16.4 to 0.064 at `m = 3` and from 0.0081 to 0.000087 at
`m = 4`** (Val₆ on the strand; floor side only; subsets enumerated explicitly, which is
affordable only for small `n`).  Nobody has applied it to the twenty-residue instance:
that needs the pair sums `Γ_ij = Σ_{T⊇{i,j}} ĉ_T` without enumerating subsets — from P3's
closed-form generating functions with two sites excluded
(`Σ_{T⊇{i,j}} ĉ_T = Γ − Γ^{(−i)} − Γ^{(−j)} + Γ^{(−i,−j)}`; P3's code has the one-site
exclusion).

## The questions, in this order

1. **Pair sums without enumeration.**  Derive and implement `Γ_ij` at order `m` from P3's
   generating functions (`gfbound.py`); validate against explicit enumeration of subsets
   on every small instance where that is affordable (they must agree to rounding;
   report the largest difference).  If the two-site exclusion is not available in closed
   form for P3's bound (its Proposition 4 uses elementary symmetric and Bell polynomials
   of per-site quantities — check which quantities are per-site), say exactly why and
   what replaces it (e.g. an upper bound on `Γ_ij` that is still valid, with proof).
2. **The banded pair form for both sides of the sandwich.**  Floor and ceiling:
   `m_∓ = f + I_{m−1}g ∓ penalty`, penalty = pair shares inside the band, the share of
   every out-of-band pair in halves to its two sites (P4.6(iii)).  Write the covering
   statement with its proof for both signs (it is the same inequality), including the
   interplay with P3's own band reductions of the pair terms (P4 did not apply those —
   P3's run does; read P3's Theorem 5 and its code path in `run_floor.py` and make sure
   the combined model is still a valid sandwich: this is the step where an error would
   be silent).
3. **Validation by enumeration.**  On every enumerated instance P3 used: `m₋ ≤ E ≤ m₊` at
   **every** state for the site form (reproducing P3), the pair form and the banded pair
   form; counts of state checks and violations; bracket widths `ln Z(m₋) − ln Z(m₊)` for
   the three forms, per instance and order.  A single violation means the construction
   is wrong: stop, find it, keep the counter-example.
4. **Twenty residues.**  Ace-Val₂₀-NMe on PPII, P3's anchor and domain: the certified
   bracket for `m = 3, 4, 5` with the banded pair form next to P3's site form, with the
   number of evaluations of the solvent term for each.  Independent checks of the
   *value* (not of the certificate): the coordinator's uncertified estimates
   `518.2618 ± 0.0007` (anchored chain model) and `518.2626 ± 0.0001` (fitted chain model),
   addendum A17 (10).  Reuse P3's cached evaluations if they exist; do not repeat a long
   enumeration that is already on disk.
5. **How far does it reach?**  Only if 1–4 are done and a run is affordable within the
   machine rules below: the same certificate for valine on the strand or PPII at 30 and
   at 50 residues (`10^{14.3}` and `10^{23.9}` assignments) at the lowest order that gives a
   bracket below 0.1 nats, if any.  Independent estimates of the value: `743.1665` (Val₃₀,
   strand) and `1197.4086` (Val₅₀, strand), addendum A17 (10).  State the number of
   evaluations and the run time; if it is not affordable, say what it would cost.
6. **What it does not fix.**  Re-run one helix instance (Leu₈ or Leu₁₆) to confirm that
   no allocation helps where the constants are large (P4 found this at `m = 3`), so that
   the report does not suggest the compact case is solved — workstream P5 is on that.

## What is available (all read-only; import or copy, never edit)

`experiments/science/ws_P3/` (`p3core.py`, `encl.py`, `gfbound.py`, `run_floor.py`, its
caches and logs); `experiments/science/ws_P4/p4_06_p3pair.py` (the pair form with
enumerated subsets, floor side) and its logs; `experiments/science/ws_P2/` (grids,
geometry); `experiments/science/pi_inference/beyond_enumeration_*.py` (the coordinator's
chain models).  Theory division: `docs/THEORY_REPORT.md` §11.7 at `24a3c27` in the export
(Theorem 11.18a), `proofs/Frontiers/ThirdOrderModel.lean` there.

## Rules

As in the P3 and P5 briefs.  Write only in `experiments/science/ws_P6/` and
`docs/science/workstreams/P6_REPORT.md`.  No state-changing git; no `lake build`; no
subagents.  Model-relative statements only; the fixed synthetic homopeptides of P2/P3;
no sequence is varied or optimised; nothing target-specific; no experimental execution;
no cloud compute.  Every inequality claimed as a bound is checked against enumeration
at every state where the domain can be enumerated, with counts.  A log is cited only if
its run reached its last line; scripts that produce cited numbers run from a clean
state with one command, listed with run times.  Machine: 4 cores shared with two other
jobs — `OMP_NUM_THREADS=1`, at most two processes, no single run longer than 20 minutes
without a checkpoint.  Keep `NOTES.md` from the first minute.  Labels [P], [M], [N], [C],
[H], [K] with reading levels for anything cited.  Report your own errors.  A negative
result with its reason is a result.

## The report

(0) Verdict in five sentences.  (1) The statement of the banded pair sandwich with its
proof, and how `Γ_ij` is computed.  (2) Validation tables (state checks, violations,
largest and smallest ratio of bound to exact remainder).  (3) Bracket widths: site form
against pair forms, per instance and order.  (4) The twenty-residue table (`m = 3, 4, 5`;
evaluations; brackets; comparison with P3 and with the uncertified estimates).  (5) The
reach (30, 50 residues) or its cost.  (6) The helix control.  (7) What a checker would
need (the certificate's data and the additions it takes to verify).  (8) Requests to the
theory and engineering divisions that can be sent as they stand.  (9) How to re-run.
(10) What was not settled; what was not checked; own errors.
