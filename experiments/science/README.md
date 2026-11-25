# experiments/science — scripts of the science division

Everything here is the science division's own code (branch `research/scientific-translation`).
Nothing here modifies upstream files.

| directory | what | how to run |
|---|---|---|
| `pi_inference/` | checks for `docs/science/INFERENCE_LIMITS.md` §§1–6: `code_cone_check.py` (Theorem 2), `basin_bound_check.py` (Theorem 3), `maxent_stability_check.py` (Theorem 7), `calorimetric_twin_check.py`, `calorimetric_twin_exact.py` (Proposition 5b) | `python3 <script>`; seconds to a few minutes each |
| `pi_chain/` | diamond-lattice chains: own enumerator `dia_chain.py`; model-free identified sets `identified_sets.py`; the same up to 27 beads from the engineering tables `identified_from_eng_tables.py`; model + envelope class + data `envelope_identified.py`, `envelope_scaling.py` (§§9, 11) | see below |
| `audit_replication/` | log of `scripts/audit_all.sh` at theory head `5ed4072` on this machine | — |
| `ws_*/` | working directories of the independent workstreams (published with their reports) | see each report |

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
