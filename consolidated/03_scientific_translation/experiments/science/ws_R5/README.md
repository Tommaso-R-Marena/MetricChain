# ws_R5 — review SCI-REV-0005 (theory report §11.26, Theorems 11.99 and 11.101)

Report: `docs/science/workstreams/R5_REPORT.md`.  Running log: `NOTES.md`.  Object under review: the theory branch at
`89ac710` (read-only checkout `thy_ro`; nothing of it is imported here).

Own implementation, written from the statements before the authors' code was read: `r5lib.py`.
Run every script from this directory with `python3 <script>`; stored outputs are in `out/` (same base name, `.txt`).

| script | what it checks |
|---|---|
| `t01_identity.py` | Theorem 11.99, first identity, by three routes (LP game + blind search over the Lipschitz polytope; primal Rényi programme; dual radius programme) |
| `t02_reference_numbers.py` | THY-MSG-0011 §1(c) and the worked-example table of §11.26 |
| `t03_dictionary.py` | cube = binary symmetric channel; sup_ρ[E_0(ρ) − ρθ] against S∘R̂⁻¹; fixed-composition forms (Gallager ≤ Csiszár–Körner ≤ E_sp) |
| `t04_beyond_two_letters.py`, `t04b_kink.py`, `t04c_split.py` | non-concave site function, hardest site law, groupings of letters, exact crossings e^u = k(k−1) |
| `t05_evaluation_lemma.py [n_random]` | the single-letter lemma V(μ,B;v) ≤ R̂(B − α(μ)) by a primal convex programme (one and two site types) |
| `t06_bruteforce_orientation.py` | brute force on 36 points, two site types, two asymmetric envelopes: the finite-n statements used by the transfer |
| `t07_misc.py`, `t07b_zero_threshold.py`, `t07c_rare_third_state.py` | grid of 171 site laws; a rare third state; asymmetric two-letter normal form; zero residual; Theorem 11.101(a) at n = 480 |
| `t08_binary_concavity.py [n_sites]` | concavity of the site function for random two-letter sites |
| `t09_lemma_Tprime.py` | Lemma 11.96 (inherently typical subsets with site types) by exact enumeration on 72 points |
| `lean_check/RenyiCentre_copy.lean` | verbatim copy of `proofs/Frontiers/RenyiCentre.lean` + `#print axioms`; `cd /home/user/MetricChain; lake env lean <absolute path>` |
