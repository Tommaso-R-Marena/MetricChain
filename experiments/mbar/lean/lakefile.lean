import Lake
open Lake DSL

/-!
Division 9 (certified MBAR) — machine-checked deterministic cores.
A standalone Lake project so that nothing in the theory division's tree (`proofs/`, its audit) is
touched.  Same pins as the programme: Lean `v4.31.0` (lean-toolchain), Mathlib tag `v4.31.0`
(revision `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f`, lake-manifest.json copied from the repository root).
-/

package mbar where
  leanOptions := #[
    ⟨`autoImplicit, false⟩,
    ⟨`relaxedAutoImplicit, false⟩
  ]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.31.0"

@[default_target]
lean_lib MBAR where
