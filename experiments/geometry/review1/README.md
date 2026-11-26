# Working directory of the internal referee (GEOMETRY-REV-0001)

These files were written by the referee of the internal adversarial review
`docs/collaboration/messages/geometry/GEOMETRY-REV-0001.md` in its own scratch directory and
are preserved here **unmodified** (copied on 2026-11-26; Python caches and the referee's
snapshot of our report at commit `e8e2582` were left out).  The referee's code imports none
of the division's code (`mylib.py` is its own chain builder).  The report explains every
script; logs are the `*.out` files; `alt_*.npz` are explicit competing ensembles below the
identifiability threshold; `lean_check/` holds copies of the Lean file at `e8e2582` with the
referee's counterexample to "universal rigidity ⇒ second-moment rigidity" (now in
`proofs/Geometry/EnsembleRigidity.lean` as `universal_not_secondMomentRigid`).

Paths inside the scripts and logs refer to the referee's scratch directory; run the scripts
from this directory.  Some need `scipy`, `cvxpy` (`k_stress.py`) or Singular (`l_theoremI.py`).
The division's own harness (`../run_checks.py`) does not depend on anything here.  This README is the
division's; every other file in this directory is the referee's.
