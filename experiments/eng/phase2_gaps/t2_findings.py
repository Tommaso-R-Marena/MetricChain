"""T2 (d): run engineering's reproducer of findings F1, F3, F4, F6 (``experiments/eng/sb_zcheck/findings_repro.py``,
unchanged) against a given SB worktree, writing its output under this directory instead of ``sb_zcheck/results``.

The adapter does exactly two things: it sets ``SB_CHECKOUT`` (read by ``sb_bridge.checkout()``) to the worktree, and it
rebinds the module global ``findings_repro.HERE`` so that ``main()`` writes ``<out>/results/findings.json`` (the
original writes into ``experiments/eng/sb_zcheck/results/``, which this task must not touch).  F2 (Z3 monotonicity)
and F7-F9 are not part of findings_repro.py; see t2_f2_f9.py.

    <python with python-flint> experiments/eng/phase2_gaps/t2_findings.py <sb-worktree> <out-dir>
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

SB, OUT = Path(sys.argv[1]), Path(sys.argv[2])
os.environ["SB_CHECKOUT"] = str(SB)
ZDIR = Path(__file__).resolve().parent.parent / "sb_zcheck"
sys.path.insert(0, str(ZDIR))
import findings_repro  # noqa: E402

(OUT / "results").mkdir(parents=True, exist_ok=True)
findings_repro.HERE = OUT
sys.exit(findings_repro.main())
