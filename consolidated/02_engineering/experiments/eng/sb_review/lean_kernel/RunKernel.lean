/-
Executing the machine-checked kernel `MetricChain.verify` (theory division, `proofs/CertificateAlgebra.lean`,
soundness theorem `verify_sound`) on an instance and a certificate read from a file of integers.

Written by the Computational Research Division for its review of the structural-biology division's certificates
(experiment X-017).

*What is proved here.*  One statement: `verifyM_eq`, that the function `verifyM` defined below returns the same
value as the kernel `verify` on every input.  `verifyM` is the kernel with one change that does not alter its value:
after every elimination and every branching step the domains are copied into an array.  The kernel itself keeps
them as nested function updates, and as compiled by Lean each lookup re-evaluates the update below it, so the cost
of `verify` doubles with every elimination in a chain (measured: see the experiment's report); a certificate with
344 eliminations cannot be run through it.  By `verifyM_eq` and `verify_sound`, `verifyM c I D L = true` implies
`L ≤ I.energy x` for every configuration `x` of the box.

*What is not proved.*  The reader below (a mistake in it would make the kernel check another instance than the one
intended) and the faithfulness of Lean's interpreter in executing `verifyM` (execution is not a proof term).  What
makes the reader checkable is printed at the end: digests of the instance *as the kernel sees it* (through `I.h`
and `I.J`, over every index, padding included), which the Python side recomputes from the published tables; the
energy of the witness computed by the kernel's own `PairInstance.energy`; and the verdicts for the claimed bound
and for the claimed bound plus one unit.

    lake env lean --run experiments/eng/sb_review/lean_kernel/RunKernel.lean TOKENS [full] [plain]

`full`: the digest of the pair tables runs over all `n·n·k·k` indices (otherwise over the unary tables only).
`plain`: the kernel `verify` itself is also executed and timed (feasible for short chains only).

Input: whitespace-separated decimal integers (written by `export_for_kernel.py`):

    n k den L                         L/den is the claimed bound; every rational below is a numerator over den
    k_0 … k_{n-1}                     number of states of every site (k = their maximum; the rest is padding)
    h                                 for every site, its k_i integers
    P, then P × (i j, k_i·k_j integers)   the stored pair tables, i < j, row index = state of i
    for every site: c, then c states  the root domains
    w_0 … w_{n-1}                     the witness
    the certificate in preorder:
      0  u (n)  p (n·n)  M  M × (i j, k integers)     leaf: bounds u_i, p_ij and message vectors m_ij(·)
      1  i  c  c × (a, subtree)                          branch on site i
      2  i r t  ℓ (n)  subtree                           elimination of state r of site i, dominated by t
-/
import proofs.CertificateAlgebra

open MetricChain

namespace SBKernel

/-! ### The kernel with memoised domains, and the proof that it is the kernel -/

/-- The values of a function on `Fin n`, as an array of length `n`. -/
structure Memo (n : ℕ) (α : Type) where
  arr : Array α
  size_eq : arr.size = n

def Memo.of {n : ℕ} {α : Type} (f : Fin n → α) : Memo n α := ⟨Array.ofFn f, Array.size_ofFn⟩

def Memo.get {n : ℕ} {α : Type} (m : Memo n α) (i : Fin n) : α :=
  m.arr[i.val]'(by rw [m.size_eq]; exact i.isLt)

theorem Memo.get_of {n : ℕ} {α : Type} (f : Fin n → α) : (Memo.of f).get = f := by
  funext i
  simp [Memo.get, Memo.of]

/-- `verify` with the domains copied into an array after every step (the copy is evaluated once, when the
recursive call is made, because `Memo.of …` is a value and not a function). -/
def verifyM {n k : ℕ} : Cert n k → PairInstance n k → Dom n k → ℚ → Bool
  | .leaf u p m, I, D, L => decide (LeafOK I D L u p m)
  | .branch i ch, I, D, L => (D i).all fun a => verifyM (ch a) I (Memo.of (D.fix i a)).get L
  | .prune i r t ℓ rest, I, D, L =>
      decide (PruneOK I D i r t ℓ 0) && verifyM rest I (Memo.of (D.remove i r)).get L
  | .sum I₁ I₂ L₁ L₂ c₁ c₂, I, D, L =>
      decide (SumOK I I₁ I₂ D L L₁ L₂) && verifyM c₁ I₁ D L₁ && verifyM c₂ I₂ D L₂

/-- The memoised kernel is the kernel. -/
theorem verifyM_eq {n k : ℕ} : ∀ (c : Cert n k) (I : PairInstance n k) (D : Dom n k) (L : ℚ),
    verifyM c I D L = verify c I D L := by
  intro c
  induction c with
  | leaf u p m => intro I D L; simp [verifyM, verify]
  | branch i ch ih => intro I D L; simp [verifyM, verify, Memo.get_of, ih]
  | prune i r t ℓ rest ih => intro I D L; simp [verifyM, verify, Memo.get_of, ih]
  | sum I₁ I₂ L₁ L₂ c₁ c₂ ih₁ ih₂ => intro I D L; simp [verifyM, verify, ih₁, ih₂]

/-- Hence acceptance by the memoised kernel has the meaning of the theory division's soundness theorem. -/
theorem verifyM_sound {n k : ℕ} (c : Cert n k) (I : PairInstance n k) (D : Dom n k) (L : ℚ)
    (h : verifyM c I D L = true) : ∀ x, InBox D x → L ≤ I.energy x :=
  verify_sound c I D L (by rw [← verifyM_eq]; exact h)

/-! ### Reading the input -/

/-- Decimal integers separated by spaces and newlines; anything else is an error. -/
def tokenize (bytes : ByteArray) : Except String (Array Int) := Id.run do
  let mut out : Array Int := Array.mkEmpty (bytes.size / 4)
  let mut cur : Nat := 0
  let mut neg := false
  let mut digits := false
  let mut err : Option String := none
  for idx in [0:bytes.size] do
    let b := bytes.get! idx
    if 48 ≤ b && b ≤ 57 then
      cur := cur * 10 + (b.toNat - 48)
      digits := true
    else if b == 45 then
      if digits || neg then err := some s!"misplaced minus sign at byte {idx}"
      neg := true
    else if b == 32 || b == 10 then
      if digits then
        out := out.push (if neg then -(cur : Int) else (cur : Int))
      else if neg then err := some s!"a minus sign without digits at byte {idx}"
      cur := 0
      neg := false
      digits := false
    else
      err := some s!"unexpected byte {b} at position {idx}"
  if digits then out := out.push (if neg then -(cur : Int) else (cur : Int))
  match err with
  | some e => return .error e
  | none => return .ok out

abbrev P := ReaderT (Array Int) (StateT Nat (Except String))

def next : P Int := do
  let toks ← read
  let pos ← get
  if h : pos < toks.size then
    set (pos + 1)
    pure toks[pos]
  else
    throw s!"unexpected end of input at token {pos}"

def nextBelow (b : Nat) (what : String) : P (Fin b) := do
  let v ← next
  if v < 0 then throw s!"{what}: negative value {v}"
  if h : v.toNat < b then pure ⟨v.toNat, h⟩ else throw s!"{what}: {v} is not below {b}"

def nextMany (m : Nat) : P (Array Int) := do
  let mut out : Array Int := Array.mkEmpty m
  for _ in [0:m] do
    out := out.push (← next)
  pure out

def q (num : Int) (den : Nat) : ℚ := (num : ℚ) / (den : ℚ)

/-- A certificate that proves nothing useful; stands for children that the file does not give. -/
def dummy (n k : ℕ) : Cert n k := .leaf (fun _ => 0) (fun _ _ => 0) (fun _ _ _ => 0)

instance (n k : ℕ) : Inhabited (Cert n k) := ⟨dummy n k⟩

partial def parseCert (n k den : ℕ) : P (Cert n k) := do
  let tag ← next
  if tag == 0 then
    let u ← nextMany n
    let p ← nextMany (n * n)
    let mcount ← nextBelow (n * n + 1) "number of message vectors"
    let mut midx : Array Nat := Array.replicate (n * n) 0
    let mut mvecs : Array (Array Int) := #[]
    for _ in [0:mcount.val] do
      let i ← nextBelow n "message site"
      let j ← nextBelow n "message neighbour"
      let v ← nextMany k
      if midx.getD (i.val * n + j.val) 0 ≠ 0 then throw s!"two message vectors for the pair ({i}, {j})"
      midx := midx.set! (i.val * n + j.val) (mvecs.size + 1)
      mvecs := mvecs.push v
    pure (.leaf (fun i => q (u.getD i.val 0) den) (fun i j => q (p.getD (i.val * n + j.val) 0) den)
      (fun i j a =>
        let s := midx.getD (i.val * n + j.val) 0
        if s = 0 then 0 else q ((mvecs.getD (s - 1) #[]).getD a.val 0) den))
  else if tag == 1 then
    let i ← nextBelow n "branch site"
    let c ← nextBelow (k + 1) "number of children"
    let mut ch : Array (Option (Cert n k)) := Array.replicate k none
    for _ in [0:c.val] do
      let a ← nextBelow k "child state"
      let sub ← parseCert n k den
      ch := ch.set! a.val (some sub)
    pure (.branch i (fun a => (ch.getD a.val none).getD (dummy n k)))
  else if tag == 2 then
    let i ← nextBelow n "site of an elimination"
    let r ← nextBelow k "eliminated state"
    let t ← nextBelow k "dominating state"
    let l ← nextMany n
    let rest ← parseCert n k den
    pure (.prune i r t (fun j => q (l.getD j.val 0) den) rest)
  else
    throw s!"unknown node tag {tag}"

structure Problem where
  n : ℕ
  k : ℕ
  den : ℕ
  L : Int
  I : PairInstance n k
  D : Dom n k
  w : Config n k
  cert : Cert n k
  nodes : ℕ

def parseProblem : P Problem := do
  let n ← next
  let k ← next
  let den ← next
  let L ← next
  if n ≤ 0 ∨ k ≤ 0 ∨ den ≤ 0 then throw "n, k and den must be positive"
  let n := n.toNat
  let k := k.toNat
  let den := den.toNat
  let mut sizes : Array Nat := #[]
  for _ in [0:n] do
    let s ← nextBelow (k + 1) "number of states"
    sizes := sizes.push s.val
  let mut hArr : Array (Array Int) := #[]
  for i in [0:n] do
    hArr := hArr.push (← nextMany (sizes.getD i 0))
  let np ← nextBelow (n * n + 1) "number of pair tables"
  let mut pidx : Array Nat := Array.replicate (n * n) 0
  let mut pcols : Array Nat := #[]
  let mut ptabs : Array (Array Int) := #[]
  for _ in [0:np.val] do
    let i ← nextBelow n "pair site"
    let j ← nextBelow n "pair site"
    if ¬ (i.val < j.val) then throw s!"a pair table must be given as i < j, got ({i}, {j})"
    if pidx.getD (i.val * n + j.val) 0 ≠ 0 then throw s!"two tables for the pair ({i}, {j})"
    let t ← nextMany (sizes.getD i.val 0 * sizes.getD j.val 0)
    pidx := pidx.set! (i.val * n + j.val) (ptabs.size + 1)
    pcols := pcols.push (sizes.getD j.val 0)
    ptabs := ptabs.push t
  let mut doms : Array (List (Fin k)) := #[]
  for _ in [0:n] do
    let c ← nextBelow (k + 1) "size of a domain"
    let mut d : List (Fin k) := []
    for _ in [0:c.val] do
      d := (← nextBelow k "state of a domain") :: d
    doms := doms.push d.reverse
  let mut wit : Array (Fin k) := #[]
  for _ in [0:n] do
    wit := wit.push (← nextBelow k "state of the witness")
  let start ← get
  let cert ← parseCert n k den
  let stop ← get
  let total := (← read).size
  if stop ≠ total then throw s!"{total - stop} tokens left after the certificate"
  if hk : 0 < k then
    let I : PairInstance n k :=
      { h := fun i a => ((hArr.getD i.val #[]).getD a.val 0 : Int)
        J := fun i j a b =>
          let s := pidx.getD (i.val * n + j.val) 0
          if s = 0 then 0
          else
            let cols := pcols.getD (s - 1) 0
            if b.val < cols then (((ptabs.getD (s - 1) #[]).getD (a.val * cols + b.val) 0 : Int) : ℚ) else 0 }
    pure { n := n, k := k, den := den, L := L, I := I, D := fun i => doms.getD i.val [],
           w := fun i => wit.getD i.val ⟨0, hk⟩, cert := cert, nodes := stop - start }
  else throw "k must be positive"

/-- A digest of the instance as the kernel sees it: every index, padding included.  The weights make a
misplaced or transposed entry visible; the modulus is the prime `2^61 - 1`. -/
def digest (pr : Problem) (full : Bool) : Int × Int × Nat := Id.run do
  let modulus : Int := 2305843009213693951
  let mut dh : Int := 0
  let mut dj : Int := 0
  let mut nonint : Nat := 0
  for i in List.finRange pr.n do
    for a in List.finRange pr.k do
      let v := pr.I.h i a
      if v.den ≠ 1 then nonint := nonint + 1
      dh := (dh + ((i.val * 131 + a.val + 1 : Nat) : Int) * v.num) % modulus
  if full then
    for i in List.finRange pr.n do
      for j in List.finRange pr.n do
        for a in List.finRange pr.k do
          for b in List.finRange pr.k do
            let v := pr.I.J i j a b
            if v.den ≠ 1 then nonint := nonint + 1
            if v.num ≠ 0 then
              dj := (dj + ((((i.val * 131 + j.val) * 131 + a.val) * 131 + b.val + 1 : Nat) : Int) * v.num) % modulus
  return (dh, dj, nonint)

end SBKernel

open SBKernel in
def runOne (path : String) (full plain : Bool) : IO Bool := do
  IO.println s!"file {path}"
  let bytes ← IO.FS.readBinFile path
  match tokenize bytes with
  | .error e =>
    IO.println s!"error tokens: {e}"
    return false
  | .ok toks =>
    match (parseProblem.run toks).run 0 with
    | .error e =>
      IO.println s!"error input: {e}"
      return false
    | .ok (pr, _) =>
      let L : ℚ := q pr.L pr.den
      IO.println s!"n {pr.n} k {pr.k} den {pr.den} tokens {toks.size} certificate_tokens {pr.nodes} size {pr.cert.size}"
      IO.println s!"claimed_bound {L.num}/{L.den}"
      let t0 ← IO.monoMsNow
      let ok := verifyM pr.cert pr.I pr.D L
      IO.println s!"verifyM_claimed_bound {ok}"
      let t1 ← IO.monoMsNow
      let above := verifyM pr.cert pr.I pr.D (L + q 1 pr.den)
      IO.println s!"verifyM_bound_plus_one_unit {above}"
      let t2 ← IO.monoMsNow
      IO.println s!"ms_verifyM {t1 - t0} ms_verifyM_plus_one {t2 - t1}"
      if plain then
        let p0 ← IO.monoMsNow
        let okPlain := verify pr.cert pr.I pr.D L
        IO.println s!"verify_claimed_bound {okPlain}"
        let p1 ← IO.monoMsNow
        IO.println s!"ms_verify {p1 - p0}"
      let t3 ← IO.monoMsNow
      let e := pr.I.energy pr.w
      let inBox := decide (∀ i, pr.w i ∈ pr.D i)
      IO.println s!"witness_in_box {inBox}"
      IO.println s!"witness_energy {e.num}/{e.den}"
      let (dh, dj, nonint) := digest pr full
      IO.println s!"digest_h {dh}"
      IO.println s!"digest_J {dj}"
      IO.println s!"non_integer_entries {nonint}"
      let t4 ← IO.monoMsNow
      IO.println s!"ms_rest {t4 - t3}"
      (← IO.getStdout).flush
      return ok

def main (args : List String) : IO UInt32 := do
  let flags := args.filter (fun a => a == "full" || a == "plain")
  let paths := args.filter (fun a => !(a == "full" || a == "plain"))
  if paths.isEmpty then
    IO.eprintln "usage: RunKernel [full] [plain] TOKENS..."
    return 2
  let mut all := true
  for path in paths do
    let ok ← runOne path (flags.contains "full") (flags.contains "plain")
    all := all && ok
  return (if all then 0 else 1)
