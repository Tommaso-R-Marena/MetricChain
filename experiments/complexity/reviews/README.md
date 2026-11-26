# Code of the internal adversarial reviews

These directories contain the programs written by the five internal referee agents (see
`docs/collaboration/messages/complexity/COMPLEXITY-REV-0001.md` to `-0005.md`).  They were written without
access to, and import nothing from, the division's own programs in `experiments/complexity/strands/` and
`experiments/complexity/nanuq/`; they are kept here unchanged as independent evidence.

| directory | reviews | entry point |
|---|---|---|
| `rev1_strands/` | `docs/complexity/STRANDS_NN_HARDNESS.md` | `run_all.sh` (needs `g++`; `fragility_real.py` additionally needs the five ViennaRNA parameter files `rna_turner2004.par`, `rna_turner1999.par`, `rna_andronescu2007.par`, `dna_mathews2004.par`, `dna_mathews1999.par` from the `misc/` directory of the ViennaRNA repository in a sibling directory `review1_params/`; they are third-party files and are not redistributed here) |
| `rev2_nanuq/` | `docs/complexity/NANUQ_LOCAL_CRITERION.md` | the `t*.py` scripts (libraries `rnet.py`, `gen.py`, `css.py`, `quarnet.py`); several scripts read the pickled network batches written by `t3b_random.py` / `t3b_random_big.py`, which are not stored (regenerate them first); logs of the referee's runs are in `rev2_nanuq/out/` |

| `rev3_strands_algorithm/` | `docs/complexity/STRANDS_ALGORITHM.md` and the additions to the hardness note (REV-0003) | `bf.py` (the referee's enumerator from the definitions, exact rationals), `bfmod.cpp` (the same in C++, weights modulo `2^61 − 1`; needs `g++`), `mydp.py` (the referee's own implementation of the algorithm, with letter-dependent weights), drivers `cmp*.py`, `val_cpp.py`, `complexity_*.py`, `api_edge*.py`; for the hardness note `hard_*.py`, `cor4_check.py`, `eth_*.py`; outputs of the referee's runs in `out/`.  The drivers import the division's `multiset_dp.py` from a copy (`author_copy/`, not stored: use `experiments/complexity/strands/`) |
| `rev4_ising_nanuq/` | `docs/complexity/ISING_GROUND_SETS.md` and the additions to the NANUQ note (REV-0004) | `ising_core.py`, `k4_table.py`, `k5_table.py`, `ising_tests*.py`, `referee_extras.py`, `anchor_c5*.py` (face numbers of the cut polytope on five nodes); `nanuq_core.py`, `nanuq_tests.py`, `nanuq_param.py`, `nanuq_mod_small.py`, `sharp_check*.py`, `compare_family.py`; logs `*.log`, `k5_results.json` |
| `rev5_nanuq_ising_strands/` | the statements added after the first four reviews: `NANUQ_LOCAL_CRITERION.md` Corollary 5′, §7.1, §7.2, Lemma 0; `ISING_GROUND_SETS.md` Corollary 5a, Propositions 12, 13, 13′, Theorem 14; `STRANDS_ALGORITHM.md` Proposition 5 (REV-0005) | libraries `mynet.py` (networks, switchings, the NANUQ metric from the definitions of the source paper), `mygen.py`, `myblob.py`, `mybuild.py`, `mysplits.py`, `mylemma0.py`, `ising_mine.py`, `strands_mine.py`; tests `t0_anchor.py` (Table 1(a) of the source, the network `N*`), `t1_exhaust.py`, `t1b_exhaust3.py` (exhaustive hybrid insertion, two and three hybrid nodes), `t2`–`t16` (six-point systems, Theorem 10′, structure of nested blobs, the table of Step 4, circular orders, random networks, seven- and eight-point systems, mutation test, closure, Corollary 14, any level, Lemma 8), `t20_ising.py`, `t21_thm14.py`, `t30_levels.py`; logs `*.log`; `authors_runs/` holds the outputs of our own programs as run by the referee |

Not stored: compiled binaries, caches of enumeration results (2.8 GB for the first review; `hard_cache.pkl`, 2 MB, for the third), pickled network batches, downloaded PDFs and texts of third-party papers, the referees' copies of our own files.
`rev1_strands/StackPackingCheck.lean` is the referee's scratch copy of `experiments/complexity/lean/StackPacking.lean`.

An internal AI review is not independent academic peer review.
