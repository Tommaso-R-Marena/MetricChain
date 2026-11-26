# Workstream P9 (launched 2026-11-26, after SCI-MSG-0027) — penalties resolved by rotamer state: the next lever for the charged case

*Brief written by the coordinator.  Read `COMMON.md` first (its commit pins are out of
date), then `P8_REPORT.md` §0, §3.3 (Lemma T, Proposition S, Theorem AH — the proof, one
page), §3.5, §4.1, §5 (request P8-E4) and the coordinator's note at its end, and
`docs/science/INFERENCE_LIMITS_ADDENDA.md` part A17 (18) (items 58–64).  If the agent of
this workstream is gone, its notes are in `experiments/science/ws_P9/` and its draft in
`P9_REPORT.md`.*

## Where we stand (numbers of 2026-11-26; re-derive what you use)

Workstream P8 brought the certified constants of the charged sequences down by taking
workstream P3's theorem state-wise and by expanding every term in an order with its own
hosts last (variant 'SAb').  With a split of the pairs beyond the band around the anchor
(`pi_inference/window_model_occ.py`) the pipeline certifies, triple form, band 7:

| peptide (helix, 12 residues) | order | `βΓ_m` ('SAb') | certified bracket (nats) | sampled, probability 0.95 |
|---|---|---|---|---|
| Lys₁₂ | 5 (ball 1 621 056) | 2.40 | 0.0567 | `3·10⁻⁵` |
| Lys₁₂ | 4 (ball 96 366) | 34.0 | 1.56 with P3's split (the split around the anchor at order 4: being run by the coordinator) | — |
| (LKSE)₃ | 5 (ball 3 471 783) | 42.8 | 4.30 | 0.041 (the envelope's own bracket is 1.23 nats) |

What is left is the constants.  They are **suprema over the rotamers of the sites of
`T`**, and the ensemble visits few of them: on enumerated Lys₅ the bound is `10⁴`–`4·10⁵`
times the Boltzmann mean of the true remainder (`p8_verification/lys_enum_check_K5.log`).

## The idea (P8's request P8-E4; nobody has done it)

In the proof of Theorem AH the host states of a term are those of the state `x` itself
(`u_l = x_l` for a host `l ∈ T`) **before** the maximum over `u` is taken.  The code has
the dependence in hand: `ws_P8/p8sr.py`, `BlockBound.total_T_blocks` builds, for every
block, the array `v` (one host) or `W` (two hosts) of block bounds **per host state** and
only then calls `_c1` / `_c2`, which take `v[a] + max_{b≠a} v[b]` (host in `T`) or the
four-term maximum.  Keep the function of `b` instead of its maximum.

**What to prove (short, but write it out).**  For every `x` and every `T ⊆ S(x)`,
`|T| = m`, let `Θ_T(x_T)` be the bound of §3.3 evaluated with the *actual* states of the
hosts in `T` (`u_l = x_l`), hosts outside `T` at the anchor (Theorem AH), and — first
stage — the non-host sites of `T` still through their maximal increments.  Then
`|g(x) − I_{m−1}g(x)| ≤ Σ_{T⊆S(x)} Θ_T(x_T)`, and for any weights `w_{T,i} ≥ 0`,
`Σ_{i∈T} w_{T,i} = 1`, the tables

```
c_{T,i}(b) := max{ Θ_T(x_T) : x_i = b },        γ_i(b) := Σ_{T∋i} w_{T,i} c_{T,i}(b)        (b ≠ x⁰_i)
```

are valid site penalties: `|g − I_{m−1}g|(x) ≤ Σ_{i∈S(x)} γ_i(x_i)`.  The same for pairs
`c_{T,ij}(b_i, b_j)` and triples: tables on two or three sites, which the band models
take as they are (`add_pair` for in-band pairs, `add_multi` for triples in a window; the
share chains of workstream P6 — Lemma A, A′ — for what is out of band or out of
window).  State what each table maximises over, and prove the chain you use.

## The questions, in this order

1. **The statement and its proof**, with the exact hypotheses (which sites are
   resolved, which are maximised; equal weights first).  Say explicitly why a table
   that depends on `x_i` is still a valid penalty for a set `T` that contains `i`
   (it is one line; it must be there).
2. **Validation by enumeration, before anything else is computed** — Lys₄, Lys₅,
   LKSE:5 on the helix (constants via P8's code path; the pattern of
   `p8_verification/lys_enum_check.py` for the left side): `|g − I_{m−1}g|(x) ≤ pen(x)`
   at **every** state, orders 3 to `n`, for each table form you build; and one
   deliberately wrong table that must fail (e.g. the minimum over `b` in place of the
   value at `b`): a check that cannot fail checks nothing (`DEAD_ENDS.md` SD59).
3. **How much does the resolution gain?**  For Lys₁₂ at orders 4 and 5 and (LKSE)₃ at
   order 5: the ratio, site by site, of the Boltzmann-typical penalty (on a Gibbs
   sample; the coordinator's sampler is `window_model_occ.gibbs_sample`) to the
   state-independent one, and of the maximum over `b` to it (must be ≤ 1, = 1 for
   the worst rotamer).  **Write a prediction of the certified brackets into your notes
   before you build the models**, with its reasoning.
4. **The certified brackets** with the resolved tables in the site, banded pair and
   banded triple forms, band 7, models built with `window_model_occ.build_window_models_occ`
   (zero penalties) plus your tables added to `lo.one[i]` / `up.one[i]`, `add_pair`,
   `add_multi` (see how `pi_inference/occ_reduction_test.py` builds models and checks
   them; workstream P6's floating-point allowances `L.fp_tables` must be kept — say
   how you add them).  Checks: the sandwich at Gibbs states and at exact samples of
   the floor (and at every state on Lys₅ at a narrow band, with the exact `ln Z`
   inside).  Stopping condition: the three brackets against the state-independent
   ones — `0.0567` (Lys₁₂, order 5), the order-4 number the coordinator gives you,
   `4.30` ((LKSE)₃) — or a reason why the dependence on the host's rotamer is weak.
5. **Second stage, if the first gains** — resolve the *non-host* sites of `T` too
   (their increments `δ_i` are maxima over the states of `i`; with the state of `i`
   fixed they are single values: look for them in workstream P3's `GFBound` per-state
   data), and/or unequal weights `w_{T,i}` (charge a subset to the site that is rarely
   off the anchor — addendum A17 (17), items 52–54, for the state-independent case).
6. **Stretch — a state-resolved envelope for the nested sampler.**  For (LKSE)₃ the
   sampler's cost is the envelope's own bracket (1.23 nats).  The fully resolved
   `Σ_{T⊆S(x)} Θ_T(x_T)` is a valid envelope; `pi_inference/nested_sampler_ext.py` shows
   how an envelope object is plugged in (`TableEnvelope.value`).  Estimate its cost per
   proposal before building it; run it only if 400 000 proposals fit in twenty
   minutes.

## Rules

Write only in `experiments/science/ws_P9/` and `docs/science/workstreams/P9_REPORT.md`
(import P3's, P5's, P6's, P8's and the coordinator's modules read-only; P8's `p8lib.py`
shows how to redirect caches so that nothing is written into another workstream's
directory; wrap `p5lib.anch_walk` with a garbage collection as P8 does).  No
state-changing git; no `lake build`; no subagents.  Label every statement **[V]**, **[P]**,
**[X]** (exact enumeration), **[M]** (measurement), **[N]**, **[H]**; a statement of validity
is [P] only with a written proof.  Never fabricate; reading levels for anything cited;
search workstreams P3, P5, P6, P8 before calling anything new, and say "not searched"
for the literature unless you searched.  Report what you did not check, and your own
errors.  Machine: 4 cores and 14 GB **shared with the coordinator's runs** —
`OMP_NUM_THREADS=1`, at most two processes, no process above 3 GB (the band-7 models of
Lys₁₂ need 2.5 GB: one such process at a time; print the peak RSS in the last line of
every script), no run longer than 20 minutes — **and before any run of more than five
minutes write into `NOTES.md` its cost per step, the number of steps, and what its
result will be compared with**.  The balls exist: `ws_P8/cache/ball_K12_H_0.70_M4_*.npz`,
`ball_LKSEc12_H_0.60_M4_*.npz` (read-only; the order-4 ball is a prefix).  Keep `NOTES.md`
from the first minute.  A log is cited only if its run reached its last line; logs of
stopped or failed runs go into a subdirectory `not_cited/` and are named in the report.
A time written into a file is read from the clock at that moment.  **If a tool
declines an action, do not work around it: keep everything in `NOTES.md` and return the
findings as text in your hand-back.  Do not delete files with wildcards or `rm -r`;
use fresh names.**

## The report

(0) Verdict in ten lines: what the resolution gains, in certified nats.  (1) The
statement(s) with proofs.  (2) Validation by enumeration, with the control that fails.
(3) The tables: what they look like (per site: penalty by rotamer against the
state-independent one).  (4) The brackets, with the prediction written before them.
(5) Second stage and stretch, or why not.  (6) Requests to the other divisions that
can be sent as they stand.  (7) How to re-run (one command per number).  (8) Not
settled, not checked, own errors.
