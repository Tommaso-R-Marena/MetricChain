# Workstream R9 — scripts and outputs of the second-round review of the theory report at `658b77f`

Report: `docs/science/workstreams/R9_REPORT.md`.  Running log: `NOTES.md`.  Everything here was
written by the reviewer of R9.  Three scripts use code of others, and say so in their headers:
`r9_Eprime.py` imports R4's `twins_exact.py`; `r9_witness_ends.py` imports the theory division's
`experiments/workstreams/S/code/build.py` (the generator of the explicit bridges);
`r9_packing_volume.py` and `r9_exact_packing.py` read R2's packing weights.  Nothing outside this
directory is written.  gcc; Python 3.13 with numpy, scipy, sympy.

Build: `mkdir -p bin out; gcc -O3 -march=native -o bin/r9_semi r9_semi.c; gcc -O3 -march=native -o bin/r9_cobound r9_cobound.c; gcc -O3 -march=native -w -o bin/r9_extremal r9_extremal.c`

| file | what it does | output |
|---|---|---|
| `r9_semi.c` | own enumerator of diamond-lattice bridges; clean-ends flags; cleaning by a head and a tail (eight combinations) verified from coordinates; class tables; all ordered pairs of clean bridges concatenated from coordinates | `out/semi_small.txt`, `out/semi_enum22.txt`, `out/semi_pairs13_part{0,1}.txt`, `out/r9_tab_N*.txt` |
| `r9_cobound.c` | (generated from `r9_semi.c`) all ordered pairs of arbitrary (bridge, `c₁`): the error of Lemma 11.68 is `A(x¹,c₁) + B(x²)`, the ends are inherited, `q̂ = (h,g) + A + B` is exactly additive | `out/cobound13_part{0,1}.txt` |
| `r9_lat.py` | own lattice module in Python (walks, bridges, profiles, `A`, `B`, concatenation, cleaning, samplers) | — |
| `r9_long.py` | long random bridges with dense ends; concatenations; self-concatenations; helix and rod | `out/long.txt` |
| `r9_certificate.py`, `r9_head2.py` | five clean bridges with determinant 1; head 2 + tail 3 realises `q̂` exactly | `out/certificate.txt`, `out/head2.txt` |
| `r9_extremal.c` (generated from `r9_semi.c`), `r9_extremal.py` | a 21-bead bridge with `A = (1,6,10;1)` and a 14-bead bridge with `B = (0,3,4)`; their real concatenation has the error vector `(1,9,14;1)`, norm 60 = `β` | `out/extremal_raw.txt`, `out/extremal.txt` |
| `r9_semigroup_analysis.py` | my tables against R2's; set-level closure; generated lattice; the `vol·N³` test (counts, hulls, holes) | `out/semigroup_analysis.txt` |
| `r9_witness_ends.py`, `r9_exact_packing.py`, `r9_inner_volume.py` | end corrections of the ten explicit bridges; R2's packings and the hull volume on exact vertices; inner volume without coordinates | `out/witness_ends*.txt`, `out/witness_ends_*.json`, `out/exact_packing.txt`, `out/inner_volume.txt` |
| `r9_packing_volume.py` | the packings 116 / 451 / 8 / 19 in exact rationals; volumes; the arithmetic of the revised §11.22 | `out/packing_volume.txt` |
| `r9_sites.py`, `r9_sites2.py`, `r9_chi2_check.py` | own site functions (`F*`, `h`, `E`, `a` with duality brackets): data points of Proposition 11.103(d); the ceiling; laws with weight ½; the `χ²` step of Theorem 11.97(c) | `out/sites.txt`, `out/sites2.txt`, `out/chi2_check.txt` |
| `r9_minor.py`, `r9_slices.py`, `r9_m1_input.py` | numbers attached to sampled minor findings; Theorem 11.90(a) at negative accuracies; the input law of an asymmetric channel | `out/minor.txt`, `out/slices.txt`, `out/m1_input.txt` |
| `r9_Eprime.py` | `E′` against `E` on the rows of the twins table (R4's code) | `out/Eprime.txt` |
| `r9_lever.py` | the lever-arm constants of item 2(d) | `out/lever.txt` |
| `r9_diffview.py`, `r9_numdiff.py` | compact word diff of the theory report `dcdfea6..658b77f` (read-only `git diff`) | stdout |
| `lean/` | scratch copies of `Scattering.lean` and `TwoRoundsExpected.lean` from the export with `#print axioms` appended; outputs of `lake env lean` | `lean/out_*.txt` |
