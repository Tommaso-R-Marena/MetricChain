# Diagnostics of the certified minimum-energy route (class A-EXP, development instances)

Why the structural-biology division's certified producer abstains on public instances that an
uncertified solver closes in seconds.  Results and their reading: `docs/frontier_benchmarks/RESULTS.md` §6.

Inputs (outside the tree; URLs and checksums in `docs/frontier_benchmarks/DATA_PROVENANCE.md`):
`INST` = a directory with the ten fixed-sequence `pdb*.wcsp.xz` instances; `SB` = the `src/`
directory of a detached copy of the evaluated commit (`git archive <commit> | tar -x`), here
`d61fc53` whose solver files equal those of the pilot's release `1756529`;
`PILOT` = `experiments/frontier/exploratory_gmec/results/scp10_at_1756529.jsonl`.

    export PYTHONPATH=src
    D=experiments/frontier/diagnostics
    python $D/diagnose_gmec.py $INST $SB $PILOT $D/results/root_all.json   --mode root --jobs 2
    python $D/diagnose_gmec.py $INST $SB $PILOT $D/results/eps_abst.json   --mode eps --jobs 1 --budget 200 --only pdb1kwh pdb1fmj pdb1jmx
    python $D/diagnose_gmec.py $INST $SB $PILOT $D/results/profile_kwh.json --mode profile --jobs 1 --budget 150 --only pdb1kwh
    python $D/diagnose_gmec.py $INST $SB $PILOT $D/results/nodes_abst.json --mode nodes --jobs 3 --budget 900 --only pdb1kwh pdb1fmj pdb1jmx
    python $D/toulbar2_ablation.py $INST $D/results/toulbar2_ablation.jsonl --budget 60
    python experiments/frontier/make_tables.py --verify docs/frontier_benchmarks/RESULTS.md

Notes for whoever repeats this.

* The runs shared a four-core machine; seconds are indicative, node counts and bounds are not
  affected by load.  One run per cell.
* `toulbar2_ablation.jsonl` was written by three invocations appending to one file: the first
  was stopped inside the fourth instance (an instance nobody closes, where every row is a
  time-out) and the remaining instances were run with `--only`; for the two largest open
  instances only the root bounds and the default configuration were run.  The file is as
  written; no row was edited or removed.
* Written and **not run**: `--mode oracle` (the producer handed toulbar2's solution as its
  starting point).  At the root the producer's own decoding already finds the optimum on one
  of the three abstaining instances, so little was expected of it.
* Dropped: toulbar2 with virtual arc consistency (`vac=1`) did not return within the wall
  limit through the Python binding, even on the smallest instance.
* The producer's functions `dead_end_elimination` and `_Dual.sweep` are wrapped with counters
  in `--mode nodes`; nothing else of the evaluated software is touched.
