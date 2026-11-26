# Lean modules of the complexity division

Kept outside `proofs/` (which belongs to the Theoretical Research Division) and checked file by file
against the repository's pinned toolchain and Mathlib (`lean-toolchain`, `lake-manifest.json`):

```
source scripts/lean_env.sh        # or: export PATH="$HOME/.elan/bin:$PATH"
lake exe cache get                # once
lake env lean experiments/complexity/lean/StackPacking.lean     # no output = no error, no warning
lake env lean experiments/complexity/lean/JordanOrbit.lean
```

No file contains `sorry`, `admit`, an added axiom or native evaluation.  Axiom check (append
`#print axioms <name>` to a copy of the file): every theorem listed below depends on
`[propext, Classical.choice, Quot.sound]` only (checked 2026-11-26, Lean 4.31.0, Mathlib v4.31.0).

| file | declarations | what they are |
|---|---|---|
| `StackPacking.lean` | `Complexity.StackPacking.packing_of_all_stacked`, `exact_packing_of_all_stacked` | counting core of the bin-packing reduction (`docs/complexity/STRANDS_NN_HARDNESS.md`, Thm 1, step (d)): if every base of every item is paired with a template `G`, injectively, and consecutive bases of an item with adjacent positions, then the items pack into the blocks, exactly if the lengths sum to `m·B` |
| `JordanOrbit.lean` | `Complexity.JordanOrbit.weighted_fixed_point_formula`, `sum_jordan`, `jordan_zero`, `fix_iff_dvd_stab`, `stab_eq`, `sum_eq_fixed_one` | the orbit formula of `docs/complexity/STRANDS_ALGORITHM.md`, Lemma 2: for a permutation `ρ` of a finite set with `ρ^c = 1`, `Σ_x R(x)^k g(x) = Σ_{d∣c} J_k(d) Σ_{x : ρ^{c/d}x = x} g(x)`, `R(x)` the order of the stabiliser, `J_k` Jordan's totient with integer exponent |

What is **not** formalised: the model of secondary structures (polymer graph, faces, loops), hence neither
the statement "a structure with `M` stacks satisfies the hypotheses of `packing_of_all_stacked`" nor the
identification of physical structures with orbits; the NANUQ results; any complexity-theoretic statement.
