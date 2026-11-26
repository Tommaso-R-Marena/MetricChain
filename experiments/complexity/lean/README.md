# Lean modules of the complexity division

Kept outside `proofs/` (which belongs to the Theoretical Research Division) and checked file by file
against the repository's pinned toolchain and Mathlib (`lean-toolchain`, `lake-manifest.json`):

```
source scripts/lean_env.sh        # or: export PATH="$HOME/.elan/bin:$PATH"
lake exe cache get                # once
lake env lean experiments/complexity/lean/StackPacking.lean     # no output = no error, no warning
lake env lean experiments/complexity/lean/JordanOrbit.lean
lake env lean experiments/complexity/lean/NanuqFinite.lean      # prints its axioms; about 3.5 min, peak ≈ 11 GB resident
lake env lean experiments/complexity/lean/FourPartition.lean    # prints its axioms; seconds
lake env lean experiments/complexity/lean/NanuqPattern.lean     # prints its axioms
lake env lean experiments/complexity/lean/ChainGadgets.lean     # prints its axioms; 8 s
```

No file contains `sorry`, `admit`, an added axiom or native evaluation (`native_decide`); the finite
checks of `NanuqFinite.lean` use `decide +kernel`, i.e. evaluation by the kernel.  Axiom check (append
`#print axioms <name>` to a copy of the file; `NanuqFinite.lean` prints them itself): every theorem listed
below depends on a subset of `[propext, Classical.choice, Quot.sound]` (checked 2026-11-26, Lean 4.31.0,
Mathlib v4.31.0; the theorems of `NanuqFinite.lean` on `propext` and, for three of them, `Quot.sound`).

| file | declarations | what they are |
|---|---|---|
| `StackPacking.lean` | `Complexity.StackPacking.packing_of_all_stacked`, `exact_packing_of_all_stacked` | counting core of the bin-packing reduction (`docs/complexity/STRANDS_NN_HARDNESS.md`, Thm 1, step (d)): if every base of every item is paired with a template `G`, injectively, and consecutive bases of an item with adjacent positions, then the items pack into the blocks, exactly if the lengths sum to `m·B` |
| `JordanOrbit.lean` | `Complexity.JordanOrbit.weighted_fixed_point_formula`, `sum_jordan`, `jordan_zero`, `fix_iff_dvd_stab`, `stab_eq`, `sum_eq_fixed_one` | the orbit formula of `docs/complexity/STRANDS_ALGORITHM.md`, Lemma 2: for a permutation `ρ` of a finite set with `ρ^c = 1`, `Σ_x R(x)^k g(x) = Σ_{d∣c} J_k(d) Σ_{x : ρ^{c/d}x = x} g(x)`, `R(x)` the order of the stabiliser, `J_k` Jordan's totient with integer exponent |

| `NanuqFinite.lean` | `Complexity.NanuqFinite.five_point_facts`, `decomposition_five`, `decomposition_six`, `tg6_length`, `tg6_globally_good`, `tg6_locally_good`, `locally_good_imp_globally_good_six`, `doubled_five_point_systems`, `C6_spec`, `closure_locally_good` (and `trees5_spec`, `trees6_spec`, `tg5_length`) | the finite facts of `docs/complexity/NANUQ_LOCAL_CRITERION.md`, recomputed in the kernel from definitions written in Lean (circular splits as bitmasks, binary trees as maximal compatible sets, tree-generated systems as unions of trees, the NANUQ metric and its split weights, the local terms `Φ5`, `Φ6`, `Ψ`): Lemma 4 for all 16 tree-generated systems on five points; Proposition 2 for all tree-generated systems on five and six points; there are 150 tree-generated systems on six points, 141 with a metric that is Kalmanson with exact support, 127 that are 6-locally good, and the latter are among the former; every five-point system with a doubled leaf is 6-locally good (Theorem 10(c)); the 108 systems of the list `C6` are pairwise distinct, tree-generated and 6-locally good (Lemma 8).  **The list `C6` is imported** from the Python enumeration of the substitution closure (`experiments/complexity/nanuq/export_lean_lists.py` checks that it is that closure); that it is the closure is not proved in Lean.  The metric on six points is evaluated in sixteen pieces (`facts_0 … facts_15`) and reassembled by proved lemmas, because a single kernel evaluation exceeds 10 GB |
| `NanuqPattern.lean` | `Complexity.NanuqPattern.phi6_neg_iff_pattern`, `kprime_six`, `seventeen` (with `tg6_length`) | Corollary 5′ of `docs/complexity/NANUQ_LOCAL_CRITERION.md` on six points: for all 150 tree-generated systems and all twelve placements, the six-leaf term `Φ6` is negative iff the system contains its three 3-splits and misses the 2-split `{z,w}`; 133 systems have no negative term (the class `𝒦′` on six points); 17 contain the three 3-splits and miss a 2-split, and these are exactly the ones with a negative term.  Self-contained (the definitions of `NanuqFinite.lean` are copied, since that file is not an importable module); about 30 s of CPU, a few minutes of wall time with the Mathlib import; axioms: `propext` |
| `FourPartition.lean` | `Complexity.FourPartition.four_sum`, `sum_good`, `size_bounds` (with `digits_zero`, `digit_equations`) | the arithmetic core of Garey and Johnson's reduction from 3-dimensional matching to 4-PARTITION with the sizes of `docs/complexity/STRANDS_NN_HARDNESS.md`, Appendix A, Lemma A2 (`r = 32q`, bin size `40r⁴ + 15`): four admissible items whose sizes add up to the bin size are one triple item with copies of exactly its three elements, all actual or all dummy; conversely such items fill a bin; every admissible item lies strictly between a fifth and a third of the bin size.  The 3DM instance, the packing and the equivalence of the two problems are not formalised |
| `ChainGadgets.lean` | `Complexity.ChainGadgets.right_angle_triangle`, `right_angle_triangle_eq`, `orthogonality_gadget`, `cyclic_core` | the two gadget inequalities of `docs/complexity/CHAIN_GEOMETRY_HARDNESS.md` over the reals, with square roots: `5√(25+24t) − 12t ≤ 25 − t²` on `[−1,1]` with equality only at `0` (§2a), and `√(25+24t) + √(25−24t) ≤ 10 − t²` on `[−1,1]` (§2); and the two-colouring step that ends the proof of Theorem 12′ of the NANUQ note.  Axioms: `propext`, `Classical.choice`, `Quot.sound` (the last theorem: `propext`, `Quot.sound`); checked 2026-11-26.  Nothing else of either note is formalised |

What is **not** formalised: the model of secondary structures (polymer graph, faces, loops), hence neither
the statement "a structure with `M` stacks satisfies the hypotheses of `packing_of_all_stacked`" nor the
identification of physical structures with orbits; phylogenetic networks and the general NANUQ statements
(Proposition 2 for all `n`, Theorem 4, Proposition 6, Lemmas A, B, Theorem 7 — only their finite inputs are
checked); any complexity-theoretic statement.
