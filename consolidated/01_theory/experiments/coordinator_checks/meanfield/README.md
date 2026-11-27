# Mean-field known parts — the coordinator's exploration (not a result)

Exploratory type-level computations made on 2026-11-25 before commissioning workstream T
(`docs/workstreams/T_brief.md`): what happens to the theory of theory report §11.20 when the
known part is a function of the type, `f(x) = n·φ(|x|/n)` (Curie–Weiss), instead of a field?
**Coarse grids (errors of several per cent), no proofs, not part of the audit, quoted
nowhere as a result.**  They are kept because the brief of the workstream refers to them.

| file | what it computes |
|---|---|
| `mf_lib.py` | rate function `I` of the type, its largest `u`-Lipschitz minorant `v`, the profile fields around a centre of type `m`; the cone formulas (`θ_na`, `R_H`, `R_0`); the dip exponent of a symmetric instance from its variational definition (a weighted `ℓ¹` distance transform) |
| `mf_test_field.py` | control: the field `p = 0.1`, `u = 2` (known values of §11.20 reproduced to the grid error) |
| `mf_cw.py` → `out_cw_pair_identity.txt` | Curie–Weiss: the pair identity `θ_na(e + R_H(e)) = R_H(e)` with the cone formulas, one phase and two phases |
| `mf_cw2.py` → `out_cw2_two_phase.txt` | two phases: dip exponent of the flat-histogram instance from its definition (`0.025`) against the cone formula (`0.011`) and against additive instances (`0.009`) |
| `mf_refine.py` → `out_refine_twophase.txt` | convergence check of the two-phase numbers on grids of 401, 801, 1601 points: the dip exponent of the flat-histogram instance at accuracies `−0.01, 0, 0.01` is `0.0309, 0.0252, 0.0200`, and the shell-cone non-adaptive exponent satisfies the pair identity with it to three or four digits (cone value: off by a factor ten) |
| `mf_shell.py` → `out_shell_*.txt` | non-adaptive exponent from cones around shells against the dip exponent of the flat-histogram instance: equal to the cone value for the field and for one phase; for two phases the shell value restores the pair identity that the cone value violates by a factor ten |

Observations (to be confirmed or refuted by the workstream): for a convex rate function
everything of §11.20 seems to carry over; for a two-phase known part single cones are not
extremal, the hardest instance appears to be the flat-histogram (multicanonical) one, and
the extremal perturbations sit on a shell of configurations in the barrier type class.
