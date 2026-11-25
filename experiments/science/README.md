# experiments/science — scripts of the science division

Everything here is the science division's own code (branch `research/scientific-translation`).
Nothing here modifies upstream files.

| directory | what | how to run |
|---|---|---|
| `pi_inference/` | checks for `docs/science/INFERENCE_LIMITS.md` §§1–6: `code_cone_check.py` (Theorem 2), `basin_bound_check.py` (Theorem 3), `maxent_stability_check.py` (Theorem 7), `calorimetric_twin_check.py`, `calorimetric_twin_exact.py` (Proposition 5b) | `python3 <script>`; seconds to a few minutes each |
| `pi_chain/` | diamond-lattice chains: own enumerator `dia_chain.py`; model-free identified sets `identified_sets.py`; the same up to 27 beads from the engineering tables `identified_from_eng_tables.py`; model + envelope class + data `envelope_identified.py`, `envelope_scaling.py` (§§9, 11) | see below |
| `pi_inference/` (addenda) | checks for `docs/science/INFERENCE_LIMITS_ADDENDA.md`: `symmetrised_cone_check.py` (A1, Theorem 4′), `extensive_stability_check.py` (A2), `stability_sharpened_check.py` (A5), `vertex_channel_chain_rule_check.py` (replication of the theory division's `a = 0.294791`; chain-rule bound for several site types), `finite_precision_check.py` (A9: Theorem 2-τ, pinned ensembles), `dip_attenuation_check.py` (A10: attenuation lemma with exact rational Krawtchouk values, `n ≤ 800`; needs `mpmath`; about a minute), `monotone_ratio_check.py` (A11: robust macrostate ratios attained at fields for submodular known parts and monotone macrostates; exact linear programmes on 900 instances plus two controls; 15 seconds), `ordered_alphabet_ratio_check.py` (A13: the same on ordered multi-state sites; exact for path envelopes, a valid loose bound for discrete ones; 360 instances; 5 seconds), `helix_coil_robust_range.py` (A14: exact robust intervals of helix content and of local log odds on a Zimm–Bragg chain by transfer matrices; brute-force confirmation at `n = 10`; 8 seconds) | `python3 pi_inference/<script>.py` |
| `audit_replication/` | log of `scripts/audit_all.sh` at theory head `5ed4072` on this machine | — |
| `ws_*/` | working directories of the independent workstreams (published with their reports) | see each report |
| `ws_P/` | force-field pilot (`docs/science/workstreams/SP_REPORT.md`): needs `pip install openmm numexpr`; `verify_openmm_direct.py` is a four-second end-to-end check; the grid files (`data/`, 161 MB) are not tracked and are rebuilt by `enumerate_grid.py` | `SP_REPORT.md` §3.2 |
| `ws_K/` | kinetics (`docs/science/workstreams/SK_REPORT.md`): fifteen scripts `t*.py` and `KineticsCertificates.lean` (compile from the repository root with `lake env lean experiments/science/ws_K/KineticsCertificates.lean`; needs the Mathlib cache) | `SK_REPORT.md` §3 |

Requirements: Python 3 with NumPy and SciPy (HiGHS).  `pi_chain/cache/` (enumerations) is not
tracked and is rebuilt on demand.

The scripts that compare with, or use, the engineering division's exact class tables read
them from the directory in the environment variable `MC_ENG_DATA`.  To obtain it read-only:

```
git fetch origin research/ubuntu-engineering
git worktree add --detach /some/dir/eng_ro db56d05f695ec390dd9ef8c7d14dfdb07d8b1e6a
export MC_ENG_DATA=/some/dir/eng_ro/experiments/eng/chain_cover/data
python3 pi_chain/dia_chain.py 10                 # replication of the tables, n = 1..10 torsions
python3 pi_chain/identified_from_eng_tables.py   # identified intervals up to 27 beads
python3 pi_chain/identified_sets.py 8            # model-free identified sets, own enumeration
python3 pi_chain/envelope_identified.py 6        # model + envelope class + data, 9 beads
```
