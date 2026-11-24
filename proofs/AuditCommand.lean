import Lean

/-!
# The axiom-audit command

`#audit_axioms root` walks every constant that is *defined in a module whose name starts with
`root`* (for this project: `proofs`) or in the file that invokes the command, and fails unless
each of them depends on no axiom other than `propext`, `Classical.choice`, `Quot.sound`.

The walk is by defining module, not by name: declarations outside the `MetricChain` namespace,
private declarations and compiler-generated auxiliary constants are all covered.  Anonymous
`example`s are not constants and cannot be seen by any such walk; the audit script therefore
forbids them in `proofs/` (every checked statement is a named declaration).
-/

open Lean Elab Command in
/-- Audit every constant defined in the modules `root.*` or in the current file: only the three
standard axioms are allowed. -/
elab "#audit_axioms " root:ident : command => do
  let env ← getEnv
  let pfx := root.getId
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count : Nat := 0
  let mut bad : Array (Name × Array Name) := #[]
  for (name, _) in env.constants.toList do
    let inProject : Bool := match env.getModuleIdxFor? name with
      | some idx => pfx.isPrefixOf (env.header.moduleNames[idx.toNat]!)
      | none => true
    if inProject then
      count := count + 1
      let axs ← Lean.collectAxioms name
      let extra := axs.filter fun a => !allowed.contains a
      unless extra.isEmpty do
        bad := bad.push (name, extra)
  if bad.isEmpty then
    logInfo m!"AXIOM AUDIT OK: {count} declarations of the modules `{pfx}.*` and of this file use only propext / Classical.choice / Quot.sound"
  else
    throwError "AXIOM AUDIT FAILED: {bad}"
