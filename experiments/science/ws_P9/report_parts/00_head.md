# Workstream P9 (science division) — penalties resolved by rotamer state: what the resolution gains for the charged case

Report of an independent workstream of the Scientific Discovery, Translation & Independent
Validation Division.  Branch `research/scientific-translation`.  Everything is in
`experiments/science/ws_P9/` (running notes with the predictions, the dead ends and my own errors:
`NOTES.md`; logs: `logs/`; results: `out/`; logs that are not cited: `not_cited/`).  Written
2026-11-26.  **A draft of one workstream: nothing here has been refereed or machine-checked, no
run by anyone else is part of it, and it is not a statement of the division until the
coordinator has verified it.**  (The coordinator began a verification of its own in
`experiments/science/p9_verification/` while this was being written; I looked at four of its logs
at 12:17, read-only, and cite none of them.)

Labels: **[P]** proved here on paper (I say how it was checked); **[X]** exact enumeration of all
states of the named instance; **[M]** measured on the named model by the named script; **[K]** known
and cited with the reading level; **[H]** hypothesis or reading.  Units: kcal/mol;
`k_BT = 0.596161 kcal/mol` (300 K); brackets of `ln Z` in nats.  Every statement is
**model-relative**: it is about the finite function defined by OpenMM 8.6.1's GBn2 expression on
workstream P2's rigid synthetic peptides (Ace-X_n-NMe, ideal α-helix, three-state grid per
side-chain dihedral, P2's pruned product domain — for lysine and the patterned sequence a
greedily pruned sub-product of the clash-free domain), exactly as workstreams P3, P5, P6, P8 and
the coordinator's pipeline set it up.  No sequence was varied, designed or optimised; nothing
here bears on a real peptide in water.

*What is whose.*  The term-by-term bound and its ingredients: workstream P3.  The state-wise
evaluation per subset, the blocks, Theorem AH and the code that computes the per-host-state
block bounds: workstream P8 (`ws_P8/p8sr.py`; used unchanged, its arrays recorded before its
maximisation).  The share forms S, B, T with state-independent constants: P3 and P6.  The
window models, the occupancy-aware reductions, the split of the far pairs around the anchor,
the Gibbs sampler, the nested-sampler driver: the coordinator (`pi_inference/`).  The idea of
keeping the dependence on the state: P8's request P8-E4 and the coordinator's brief.  Charging
a subset to a sub-tuple of its sites: the theory division's Proposition 11.18f — as described
in P8_REPORT §4.1 and in addendum A17 (17), items 52–53; I did not read the theory division's
own text — estimated to first order by P8.  **Mine:** Theorem R and Proposition P as written out in §1 (both short),
the evaluation with the actual increments ("stage 2"), the tables, their validation, the
runs.

*What I read, and how much of it* (everything else is not relied on).  **[full text]**: the
brief; `COMMON.md`; `P8_REPORT.md` §0, the end of §3.2, §3.3, §3.4, §3.5, §4.1, §5, §7 and the
coordinator's note; `P3_REPORT.md` §2.1–§2.4 (Proposition 1, Lemma 2, Corollaries L1, L2, Remark
L3, Theorem 3, Proposition 4) and the start of §2.5; `INFERENCE_LIMITS_ADDENDA.md` part A17 (18)
(items 58–64) and part A17 (17), items 52–57.  **[code, read in full]**: `ws_P8/p8sr.py`, `p8lib.py`,
`p8_03c_blockcheck.py`, `p8_04b_gamma12_blocks.py`; `ws_P6/p6lib.py`; `ws_P3/pwmodel.py`, `gfbound.py`;
`pi_inference/window_model.py`, `window_model_occ.py`, `occ_reduction_test.py`,
`nested_sampler_ext.py`; `p8_verification/lys_enum_check.py`, `lys12_rerun.py`.  **[code, in part]**:
`pi_inference/nested_sampler.py` (docstring, `Envelope`, `inner_bounds`, `draw_q`, `main`);
`ws_P3/encl.py` (lines 195–300), `p3core.py` (header, `GBModel.__init__`, the evaluators),
`ws_P6/p6_09_triple.py` (first 100 lines).  **[one line]**: `ws_P5/s2_family.py`, `ws_P3/termwise.py`
(the lines found by a search for the increments).  **Literature outside the programme: not
searched.**

---

## 0. Verdict in ten lines

{VERDICT10}

### 0.1 The same ten points, each with what stands behind it

{VERDICT}

---
