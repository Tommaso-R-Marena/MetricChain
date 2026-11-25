# Workstream K — scripts and outputs

Scripts and outputs of workstream K (adaptive algorithms without a hint at a bounded
accuracy), as delivered; the report is `docs/workstreams/K_REPORT.md` (§6 describes every
script, its sizes, runtime and outcome), the integrated statements are theory report §11.19.
They are **not** part of the audit (`scripts/audit_all.sh`); they are kept so that the
numerical claims of the report can be re-run.

Run from this directory, numpy only, e.g. `ulimit -v 4000000; python3 recursion_bounded.py`.

| script | what it checks (report section) | runtime | stored output |
|---|---|---|---|
| `test_klib.py` | shared log-tables against brute force, `n ≤ 30` | seconds | — |
| `check_tail_lemmas.py` | both tail lemmas at every threshold of 408 Lipschitz functions on `Q_4 … Q_10` (§6) | < 1 s | `out_check_tail_lemmas.txt` |
| `recursion_bounded.py` | the level recursion including accuracy zero, 40 levels, `u = ½, 1, 2` (§6.1) | 152 s | `out_recursion_bounded.txt` |
| `sim_outer_loop.py` | outer loop of Algorithm 2L⁺ with a simulated adversarial inner oracle and the constants of the theorem; every claim of Theorem K1; five mutations (§6.2) | 4 min | `out_sim_outer_loop.txt`, `out_sim_outer_loop_seed777.txt` |
| `closure_window.py` | Lemma K.4 on tables `n ≤ 12 800`; the closure window (§6.3) | 2 s | `out_closure_window.txt` |
| `flat_cost_bounded.py`, `crosscheck_flat.py` | exact cost at the flat instance, `n ≤ 64 000` (§6.4) | 49 s | `out_flat_cost_bounded.txt`, `out_crosscheck_flat.txt` |
| `e2e_small.py` | the whole algorithm with real inner two-sample brackets on `Q_12`–`Q_14` (§6.5) | 5 min | `out_e2e_small.txt` |
| `radial_trajectory.py` | outer loop in expectation on radial and additive landscapes, `n_o ≤ 16 000` (§6.6) | 145 s | `out_radial_trajectory.txt` |
| `sim_grouped.py`, `stable_multinomial.py` | outer loop in the bounded regime with exact samples of up to `4.6·10^{18}` points (§6.8) | 5 min | `out_sim_grouped.txt`, `out_stable_multinomial.txt` |

The Lean files of §6.7 are merged into `proofs/Frontiers/BoundedAccuracy.lean`.
