import Lake
open Lake DSL

/-!
MetricChain — machine-verified theory for fixed-sequence articulated SE(3) heteropolymer systems.
Lean sources live in `proofs/` (module prefix `proofs.`); Mathlib is pinned to a release tag.
-/

package metricchain where
  leanOptions := #[
    ⟨`autoImplicit, false⟩,
    ⟨`relaxedAutoImplicit, false⟩
  ]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.31.0"

@[default_target]
lean_lib MetricChain where
  srcDir := "."
  globs := #[.submodules `proofs]
