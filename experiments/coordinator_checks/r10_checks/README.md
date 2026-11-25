# Coordinator's checks at the twelfth checkpoint of cycle 10

Three small scripts written while applying referee R10's report and answering the
Computational Research Division (run from the repository root, `python3 <script>`; each
loads the harness `experiments/falsify_conjectures.py` as a library where it needs its helpers).

| script | what it checks | outcome |
|---|---|---|
| `junction_m1_check.py` | referee R10, finding M1: at `u = 8`, `e = 0`, `βJ = 1 + 0.99(βJ* − 1) = 8.263` the constant exit at a well is feasible for the uniform cube's shell (closed form), the harness solver gives the value `0`, and the best symmetric shell on a coarse scan is `0.366 < R_unif = 0.3985`; controls at `u = 1, 2` (the value is the uniform cube's).  The second cell in the script uses `e_c = −Λ₁`, which is **not** the referee's `e_c = u·p_u − Λ₁`; its row is a different (also failing) cell and its scan runs into non-admissible shells — kept as run | confirms M1; became harness test DEAD.25 |
| `acone_check.py` | referee R10, finding m12: the mutual information of the Gibbs shell of a cone at `βJ = 1.5`, `u = 1`, all local minima of the cone functional | global shell `0.044351` at centre type `½`; the metastable branch has `0.044596` at `0.5025` — the `0.0446` of the first version |
| `sample_cap_check.py` | the remark after Theorem 11.56: every sample of Algorithm 2L⁺ is below `2·max{e^λM†, M‡}`; 1 363 completed runs on outer landscapes "plateau, then cone" | no violation; largest sample `0.91` of the cap (`3.7·M†`); a reduced version is harness test XVI.4 |
