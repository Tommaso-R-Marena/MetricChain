# Workstream S — scripts and outputs

Scripts and outputs of workstream S (a limit shape for profile sets of lattice chains; the
thermodynamic limit of certificate sizes), as delivered; the report is
`docs/workstreams/S_REPORT.md` (§12 lists every command with sizes, run times and outcomes),
the integrated statements are theory report §11.22.  They are **not** part of the audit
(`scripts/audit_all.sh`); they are kept so that the computer-assisted statements can be
re-run.  The coordinator's independent re-computation is in
`experiments/coordinator_checks/` (`s_check1.py` … `s_check7.py`).

Layout: `code/` (Python: numpy, scipy; three C programs), `out/` (stored outputs, including
the class tables of walks, bridges and half-space walks and of the periodic systems that
other scripts read).  The report's paths `ws/S/code`, `ws/S/out` are these two directories.

Build the C programs (not committed): from this directory

    gcc -O3 -march=native -o code/enum code/enum.c
    gcc -O3 -march=native -o code/pchain code/pchain.c
    gcc -O3 -march=native -o code/periodic code/periodic.c

Some scripts read the class tables of the Computational Research Division (their branch,
read-only).  Extract them once into a directory of your choice, here `DATA_ROOT`:

    git archive origin/research/ubuntu-engineering experiments/eng/chain_cover/data src/metricchain_eng/chains | tar -x -C DATA_ROOT

and pass `DATA_ROOT/experiments/eng/chain_cover/data` where a script asks for `DATA` or
`ENG_DATA_DIR` (`code/cover.py` expects it at `../eng_data/experiments/eng/chain_cover/data`
relative to `code/`, i.e. extract into `experiments/workstreams/S/eng_data` for that script;
that directory must not be committed).

| what | command (from this directory unless stated) | stored output |
|---|---|---|
| Lemma 2.1/2.3 (site sets, local counting), facts F1–F3, the strip of Proposition 5.5 | `python3 code/g1_check.py 9 DATA`; `cd code; python3 g1_local.py 11; python3 lattice_facts.py; python3 strip_check.py` | `out/g1_check.txt`, `out/g1_local.txt`, `out/lattice_facts.txt`, `out/strip_check.txt` |
| enumeration of walks, bridges, half-space walks | `code/run_enum.sh` | `out/walk_N*.txt`, `out/bridge_N*.txt`, `out/hsw_N*.txt`, `out/run_enum.log` |
| Lemma 3.1 (concatenation) | `cd code; python3 g2_concat.py 8 4000 1; python3 g2_concat.py 11 400 7` | `out/g2_concat.txt`, `out/g2_concat_N11.txt` |
| walks against bridges, nestedness, convexity | `python3 code/g3_compare.py out DATA` | `out/g3_compare.txt` |
| site-cluster programme and its exact certificates (Theorem 4.2) | `python3 code/cluster_lp.py 2000 1 out/lp_vertices_deg2.npy`; `cd code; python3 lp_exact.py ../out/lp_vertices_deg2.npy ../out/lp_exact.txt` | `out/cluster_lp_deg2.txt`, `out/lp_exact.txt` |
| path-cluster programme and its exact certificates (Theorem 4.2′) | `python3 code/cluster_lp4.py 1500 1500 out/lp4`; `cd code; python3 lp4_exact.py ../out/lp4_exact.txt ../out/lp4_vertices3.npy; python3 lp4_gamma_cert.py ../out/lp4_gamma_cert.txt` | `out/cluster_lp4*.txt`, `out/lp4_exact.txt`, `out/lp4_gamma_cert.txt` |
| lamellae (Proposition 4.3) | `cd code; python3 lamella.py; python3 rodpairs.py` | `out/lamella.txt`, `out/rodpairs.txt` |
| periodic site sets and periodic chain systems, cell index ≤ 12 | `code/periodic K 2` (`K = 1…12`); `code/pchain K` (`K ≤ 11`); `code/run_pchain12.sh`; hulls: `python3 code/periodic_hull.py out 12 out/lp_vertices_deg2.npy`, `python3 code/pchain_hull.py out 12 out/lp_vertices_deg2.npy` | `out/periodic_K*.txt`, `out/pchain_K*.txt`, `out/*hull*` |
| finite bridges from periodic systems; the bridge with 166 199 beads | `code/run_build.sh`; `cd code; python3 build.py "WITNESS" 128 128 128` (witness strings in `out/witnesses.txt`) | `out/build.txt`, `out/build_gauche_W128.txt` |
| covering numbers; the two norms | `python3 code/cover.py walk|bridge N Lnum Lden EPSnum EPSden [limit] [c|w]` | `out/cover_norm_check.txt`, `out/cover_bridge_vs_walk.txt` |
| bounds and estimates of the plateau; the surface law | `python3 code/g5_bounds.py out`; `cd code; python3 g5_finiteN.py ../out DATA; python3 g5_estimate.py ../out 12` | `out/g5_bounds.txt`, `out/g5_finiteN.txt`, `out/g5_estimate.txt` |
| lower bounds at given chain lengths (Proposition 7.3) | `cd code; python3 finite_packing.py 27 60 120 250 500 1000 2000; python3 finite_packing.py 5000` | `out/finite_packing.txt`, `out/finite_packing_5000.txt` |
| single-flip constants (Proposition 8.1) | `cd code; python3 g6_flip.py 43; python3 g6_flip_all.py 30` | `out/g6_flip.txt`, `out/g6_flip_all.txt` |

Every run is under ten minutes; the workstream ran them under `ulimit -v 2000000`, one
process at a time.  Re-run by the coordinator at integration: `lp_exact.py`, `lp4_exact.py`,
`lp4_gamma_cert.py` (outputs identical to the stored ones) and `build.py` at box side 128.
