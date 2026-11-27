# Checks made when the review SCI-REV-0002 of §11.22 (the limit shape) was applied

Fourteenth checkpoint of cycle 10.  The Scientific Discovery Division reviewed theory report
§11.22 (its message SCI-REV-0002; the §11.22 items of SCI-REV-0006).  Before its findings
were written into the report they were checked by an assistant of the coordinator with
code written from the statements of the report (`mylat.py`: an own implementation of the
lattice, written from the *Setting* paragraph of §11.22, not from the harness and not from
workstream S); the coordinator re-ran the scripts marked ✔ below in this directory and
obtained the stored outputs (timing lines apart).  Run from this directory; pure
Python + numpy/scipy; every run under two minutes.

| script | what it checks | output |
|---|---|---|
| `n1_helix.py` ✔ | finding N1: the all-gauche `4₁` helix is a bridge for every `N` (checked for `N = 4 … 200` and up to 10 007 beads, two own counts, and with the harness helpers `ls_*`), with `h = (0, 0, N−3)`, `g = N−3`; so `(0, 0, 1; 1) ∈ K^{br}` | `out_n1_helix.txt` |
| `gen_witness.py`, `verify_witness.py` ✔ | the ten explicit bridges behind the lower bounds: regenerated with the builder of workstream S (`experiments/workstreams/S/code/build.py`, keys of `experiments/workstreams/S/out/witnesses.txt`: nine systems in a box of side 64, one in a box of side 128) and **verified from coordinates with `mylat.py` only** — lattice sites, bonds, self-avoidance, bridge property, `(h₃, h₈, h₁₁, g)` by two own counts.  The coordinate files `wit/*.npy` (4 MB) are not stored; `wit/verified.json` holds the verified counts | `out_gen_W64.txt`, `out_gen_W128.txt`, `out_verify_witness.txt` |
| `verify_packing.py` ✔ | finding M2/N3: the reviewer's four packings (`reviewer_packings/`, copied unchanged from `experiments/science/ws_R2/out/` on the branch `research/scientific-translation`) checked in exact rational arithmetic against a vertex list rebuilt from our own verified counts: weights nonnegative with sum one, and the pairwise condition `L‖p_k − p_l‖_c > e(g_k + g_l) + 2ε₁ + max(L, e)(d_k + d_l)` for all pairs — 116, 451, 8, 19 points at `(L, ε₁) = (1, ½), (1, ¼), (⅕, ½), (⅕, ¼)` | `out_verify_packing.txt` |
| `own_packing.py` | an independent greedy search of ours in the same hull, verified in the same way: 106, 413, 8, 19 points (usage: `own_packing.py L eps1 step G0`, parameters in the output) | `out_own_packing.txt` |
| `inner_volume.py` ✔ | finding M2/N2: the erosion of the hull of the four exact points and the ten bridge densities by `δ = 168/12 044`, in exact rationals: volume `1.5632` (hull `1.6317`) | `out_inner_volume.txt` |
| `misc_checks.py` ✔ | m4 (the three hand inequalities of Proposition 11.72(a) on all bridges with at most 14 beads), m5 (the volume ratios `26 437.0`, `3 626.5`, …), m6 (the tetrahedron of volume `1/12`; `K^{br}` has interior in `ℝ⁴`), the arithmetic of Bezdek's constant (`3.6653`, `4.618`; `k ≥ 0.689`), N4, a weak test of the reviewer's finite-`N` inequalities N5, the constant `c = 277.1` of Proposition 11.69a | `out_misc_checks.txt` |
| `concat_check.py` ✔, `concat_check2.py` ✔ | m1 and m3: the error of the concatenation of Lemma 11.68 is `A(x¹, c₁) + B(x²)` (57 025 real concatenations); exhaustive maxima of `A` and `B` over single bridges with at most 16 beads; the extension by `k ≤ 5` beads costs at most `(1, 6, 10; 1)` (52 420 extensions) (`concat_check.py 11 7 13` for the stored output) | `out_concat_check.txt`, `out_concat_check2.txt` |
| `t4_semigroup.py` ✔ | **now theory report Proposition 11.69b** (re-derived by the coordinator at the sixteenth checkpoint): bridges with "clean ends" concatenate with exactly additive `(h, g)` and stay clean (20 000 random pairs), and every bridge with at most 10 beads becomes clean after a head and a tail of five beads — a positive answer to request T-4 of SCI-REV-0006 (`K^{br}` is the convex body of an exact graded semigroup of lattice points) | `out_t4_semigroup.txt` |
| `t4_head_tail.py` ✔ | Proposition 11.69b(b): heads and tails of 1, 2, 3, 4 zigzag beads on every bridge with 3 to 10 beads — three (proved) and two (observed) always give a clean bridge, one does not; the largest change of `(h, g)` | `out_t4_head_tail.txt` |
| `t4_lattice_index.py` ✔ | Proposition 11.69b(c): the vectors `(h₃, h₈, h₁₁, g; M)` of the clean bridges with at most 10 beads generate all of `ℤ⁵` (integer row reduction; uses the lattice helpers of the harness) — no congruence obstruction in the interior of the limit shape | `out_t4_lattice_index.txt` |

What was **not** re-derived: the reviewer's finite-`N` certificates (N5) and its statement
"at least 100 with finite verified walks only"; Bezdek's theorem, Permuter–Weissman and
Kaveh–Khovanskii were not read by us (the report says whose reading each citation rests on).
