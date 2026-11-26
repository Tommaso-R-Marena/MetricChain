# Code of the internal adversarial reviews

These directories contain the programs written by the two internal referee agents (see
`docs/collaboration/messages/complexity/COMPLEXITY-REV-0001.md` and `-0002.md`).  They were written without
access to, and import nothing from, the division's own programs in `experiments/complexity/strands/` and
`experiments/complexity/nanuq/`; they are kept here unchanged as independent evidence.

| directory | reviews | entry point |
|---|---|---|
| `rev1_strands/` | `docs/complexity/STRANDS_NN_HARDNESS.md` | `run_all.sh` (needs `g++`; `fragility_real.py` additionally needs the five ViennaRNA parameter files `rna_turner2004.par`, `rna_turner1999.par`, `rna_andronescu2007.par`, `dna_mathews2004.par`, `dna_mathews1999.par` from the `misc/` directory of the ViennaRNA repository in a sibling directory `review1_params/`; they are third-party files and are not redistributed here) |
| `rev2_nanuq/` | `docs/complexity/NANUQ_LOCAL_CRITERION.md` | the `t*.py` scripts (libraries `rnet.py`, `gen.py`, `css.py`, `quarnet.py`); several scripts read the pickled network batches written by `t3b_random.py` / `t3b_random_big.py`, which are not stored (regenerate them first); logs of the referee's runs are in `rev2_nanuq/out/` |

Not stored: compiled binaries, caches of enumeration results (2.8 GB), pickled network batches, downloaded PDFs.
`rev1_strands/StackPackingCheck.lean` is the referee's scratch copy of `experiments/complexity/lean/StackPacking.lean`.

An internal AI review is not independent academic peer review.
