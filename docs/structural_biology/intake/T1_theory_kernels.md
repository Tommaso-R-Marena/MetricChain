# T1 — Theory division: certificate kernels and their Lean formalization

STRUCTBIO research intake, slice "implementable core". Reviewer: T1. Date 2026-11-26.

**Source.** Read-only worktree `scratchpad/wt/theory`, commit `eb88823c931953d6455f79c9d8089063abfb442b` (`git status` clean before and after). Abbreviations: `CA` = `proofs/CertificateAlgebra.lean`, `F/` = `proofs/Frontiers/`, `BP` = `docs/BLUEPRINT.md`, `TR` = `docs/THEORY_REPORT.md`, `RC` = `experiments/reference_checker.py`. `file:N` is a line number.

**Done.** Read in full: BP, CA, RC, the 16 JSON vectors, `proofs/Core/*`, `F/PartitionCertificate`, `VoxelEnclosure`, `SeparableVoxel`, `IntervalInstance`, `ShareCertificates`, `MacroRatio`, `LinearKernel`, the scripts, `AuditCommand.lean`; definitions and main statements (not proof bodies) of the other listed files; the kernel sections of TR; `experiments/coordinator_checks/kernel_eval/README.md`; `docs/collaboration/responses/theory/THY-RES-0014.md`. Ran RC `--selftest --quick` (passes, 0.35 s), RC on all 16 vectors (all as `EXPECTED`), and six small probes of my own (`intake/t1_scratch/`).

**Not done.** No `lake build`, no audit: no Lean toolchain is installed in this environment. Every **[V]** below is the repository's label, not re-verified by me. Repository's claim (`docs/RESEARCH_LOG.md:2765`): 90 Lean files build without warnings, 5051 declarations pass the axiom walk, `scripts/audit_all.sh` exits 0. My own scan of `proofs/` with the audit's forbidden-token regex: 0 hits.

---

## 1. Bottom line

1. **A small verified core exists [V].** Three kernels as computable Lean functions with soundness theorems: `verify` (lower bound on min energy), `verifyITop` (same under an unknown residual), `zverifyTop` (two-sided bound on a partition sum). Lean-only layers on top: `verifyS` (domain split), `zverify2Top` (cut + elimination), `verifyLTop` (linear residual), `bverify*` (barriers).
2. **Only the Python reference checker runs on external certificates today**, and only for the three elementary rule sets. It is declared untrusted (BP:1280) and is related to Lean by tests, not by proof. Lean has no executable target; `native_decide` is forbidden; kernel evaluation of `verify` as written is reported to exhaust 11.9 GB at 512 table entries (TR:2507).
3. **No certificate producer exists in this worktree** — pseudocode only (BP §6).
4. **GMEC + optimality certificate is the nearest implementable target** (one LP-dual leaf, DEE, shallow branching), but needs: a producer, a fast exact checker, an exactness convention (integrality or ε-gap), and format changes.
5. **Certified Z on real proteins is blocked by the rule set**, not by engineering: exact rules stop at treewidth 2 (general case [P]); the elementary rules are enumerative; JSON/RC lack cut/elim.
6. **Continuous side chains:** the measure-theoretic bridge is proved [V]; the input it needs — interval bounds of force-field terms over voxels — is explicitly not provided.
7. **Populations:** no theorem and no checker entry point; they follow from per-state enclosures by interval division (my inference, §4).

---

## 2. (A) The kernels

### 2.0 Objects shared by all kernels

* `PairInstance n k` (CA:68): `h : Fin n → Fin k → ℚ`, `J : Fin n → Fin n → Fin k → Fin k → ℚ`. Energy (CA:94): `E(x) = Σ_i h i (x i) + Σ_i Σ_{j≠i} J i j (x i) (x j)` — over **ordered** pairs; an unordered interaction is stored in one orientation or split (BP:58). Energies are exact rationals. `k` is uniform; per-site rotamer counts are expressed by `Dom n k := Fin n → List (Fin k)` (CA:78) and the box `InBox D x`.
* `WInstance n k` (`F/PartitionCertificate.lean:43`): rational weights `w`, `W`; `weight x = ∏_i w i (x i) · ∏_i ∏_{j≠i} W i j (x i)(x j)`; `Z D = Σ_{x ∈ box D} weight x`.
* Tables are Lean *functions*, not arrays (relevant for B).

### 2.1 K1 — minimum-energy lower bound (`Cert`, `verify`; CA:117–177)

Rules, checked on the current domains `D` for bound `L`:

| constructor | side conditions |
|---|---|
| `leaf u p m` (`LeafOK`, CA:127) | `∀i ∀a∈D_i: u_i ≤ h_i(a) + Σ_{j≠i} m_ij(a)`; `∀i≠j ∀a∈D_i,b∈D_j: 2·p_ij ≤ J_ij(a,b) + J_ji(b,a) − m_ij(a) − m_ji(b)`; `L ≤ Σ_i u_i + Σ_{i≠j} p_ij` (pairwise LP dual with the dual solution supplied) |
| `branch i children` | every `a ∈ D_i`: `verify (children a) I (D.fix i a) L` |
| `prune i r t ℓ rest` (`PruneOK`, CA:141, margin 0) | `t ∈ D_i`, `t ≠ r`; `∀j≠i ∀s∈D_j: ℓ_j ≤ J_ij(r,s)+J_ji(s,r)−J_ij(t,s)−J_ji(s,t)`; `0 ≤ h_i(r) − h_i(t) + Σ_{j≠i} ℓ_j`; continue on `D.remove i r` (Goldstein DEE) |
| `sum I₁ I₂ L₁ L₂ c₁ c₂` (`SumOK`, CA:153) | on `D`, termwise per ordered pair: `h¹+h² ≤ h`, `J¹+J² ≤ J`; `L ≤ L₁+L₂`; each part verified against its own instance |

Statement (CA:308): `theorem verify_sound : ∀ (c : Cert n k) (I : PairInstance n k) (D : Dom n k) (L : ℚ), verify c I D L = true → ∀ x, InBox D x → L ≤ I.energy x`. With a witness `w ∈ box`: `certified_optimum` (CA:342). For a real model with `I ≤ M` entrywise: `verify_sound_real` (CA:960) gives `(L:ℝ) ≤ M.energy x`; pair tables stored once: `verify_sound_real_symm`.

*Split layer* (`F/SplitRule.lean:165–198`): `SCert = base (c : Cert) | split i B c₁ c₂`; `verifyS_sound` has the same conclusion. A `split` may stand above kernel certificates, **not** below `branch`/`prune`/`sum` (BP:209). No added proving power (`split_leaves_iff_branch`); it saves checks.

Known incompleteness: one leaf cannot certify the frustrated triangle (`triangle_no_leaf_certificate`); without `sum`, `m` independent frustrated triangles need exactly `2^m` leaves (`sumFree_exponential`, `F/ProofComplexity.lean`).

### 2.2 K2 — residual/envelope kernel (`RCert`, `verifyR`, `verifyITop`; CA:354–942)

Instance `IProblem` (CA:727): `base : PairInstance`, envelope constants `c : Fin n → ℚ`, anchors `IAnchor = (x, lo, hi?)`. Class `ResidualIntervalClass` (CA:743): `g : Config → ℝ` with `g(x[i↦s]) − g(x) ≤ c_i` and `lo_p ≤ g(x_p) ≤ hi_p`.

Rules: `anchor idx cert` — run `verify cert` on the anchored instance `h'_i(s) = h_i(s) − c_i·[s ≠ x^a_i]` for the bound `L − lo_a`; `branch`; `prune` with margin `c_i` (differential DEE). File-level check `IProblem.Consistent` (CA:756): `c ≥ 0` and `lo_p − hi_q ≤ Σ_i c_i[x_p,i ≠ x_q,i]` for all ordered anchor pairs with `hi_q` — exactly non-emptiness of the class (`IProblem.consistent_iff_nonempty`).

Statement (CA:879): `verifyITop c P D L = true → (∃ g, ResidualIntervalClass P g) ∧ ∀ g, ResidualIntervalClass P g → (∀ x, InBox D x → (L:ℝ) ≤ (P.base.energy x:ℝ) + g x) ∧ ∀ p ∈ P.anchors, ∀ h ∈ p.hi, (P.base.energy p.x:ℝ) + g p.x ≤ ((P.base.energy p.x + h : ℚ):ℝ)`.

The envelope constants are hypotheses: "none are certified here for a concrete residual" (BP:750).

### 2.3 K3 — partition-function kernel (`ZCert`, `zverify`, `zverifyTop`; `F/PartitionCertificate.lean:161–457`)

The checker *returns* an interval `Option (ℚ × ℚ)`:

| constructor | check / returned interval |
|---|---|
| `leaf lo hi` (`LeafZOK`) | `∀i≠j: 0 ≤ lo_ij` and `lo_ij ≤ W_ij(a,b) ≤ hi_ij` on `D`; returns `(S·∏lo, S·∏hi)`, `S = ∏_i Σ_{a∈D_i} w_i(a)` |
| `branch i children` | sum of the children's intervals over the distinct states of `D_i` |
| `prune i r t q₀ q rest` (`PruneZOK`) | `t∈D_i`, `t≠r`, `q₀ ≥ 0`, `w_i(r) ≤ q₀ w_i(t)`, `q_j ≥ 0`, `∀s∈D_j: W_ij(r,s)W_ji(s,r) ≤ q_j W_ij(t,s)W_ji(s,t)`; from `(lo',hi')` of `rest` on `D∖r` returns `(lo', (1 + q₀∏_j q_j)·hi')` |

Top level rejects any negative factor. Statement (:456): `zverifyTop c I D = some (lo, hi) → lo ≤ I.Z D ∧ I.Z D ≤ hi` (no side condition).

**Extension K3′** (`ZCert2`, `zverify2`, `F/PartitionProduct.lean:816–856`): `base (c : ZCert)`, `branch`, and

* `cut S p lo hi c₁ c₂` (`CutOK`): pin `p_i ∈ D_i`; for every ordered pair across `S | Sᶜ`: `0 ≤ lo_ij ≤ W_ij ≤ hi_ij` on `D`; children on the restricted instances over pinned boxes; requires `l₁, l₂ ≥ 0`; returns `(Λ·l₁·l₂, Υ·h₁·h₂)`.
* `elim1 i j p rest` (`Elim1OK`): `i ≠ j` and `W_im = 1 = W_mi` on `D` for all `m ∉ {i,j}`; continue with `w'_j(b) = w_j(b)·Σ_{a∈D_i} w_i(a) W_ij(a,b) W_ji(b,a)`.
* `elim2 i j l p rest`: the same with two neighbours; the sum is absorbed into `W'_jl`.

Statement (:938): `zverify2Top c I D = some (lo, hi) → lo ≤ I.Z D ∧ I.Z D ≤ hi`.

Structural restriction (my inference from the inductive type): thermal `prune` exists only inside `base`, so **pruning cannot precede a cut or an elimination**.

### 2.4 K4 — linear/profile kernel (`LCert`, `verifyL`, `verifyLTop`; `F/LinearKernel.lean`)

Instance `LProblem n k p` (:83): `base`, `p` pairwise feature tables with entries ≥ 0, rational coefficient box `[lo, hi]`, exact anchors. Rules (:118–144): `leaf lam m c` — `verify c (base + Σ_α lo_α F_α) D m` and `L ≤ m + Σ_i λ_i v_i − Σ_α max(lo_α c_α, hi_α c_α)`, `c_α = Σ_i λ_i F_α(a_i)`; `split α mid l r` — bisect the box. Statement (:251): `verifyLTop c P D L = true → ∀ θ, LinResidualClass P θ → ∀ x, InBox D x → (L:ℝ) ≤ (P.base.energy x) + Σ_α θ_α·(P.feat α).energy x`. No built-in non-emptiness check of the class (my reading; the example proves it separately). [V], "not refereed" (TR:4654). Lean only: "There is no JSON schema for this kind yet" (BP:1126).

### 2.5 K5 — share/leaf certificates and higher-order lower models

These are **theorems over ℝ, not executable kernels** (no `Bool` checker in Lean):

* `secondOrder_certified_of_shares`, `…_of_rowSum` (`F/ShareCertificates.lean:69, 104`); `secondOrder_certified_of_state_shares` (`F/StateShares.lean:105`): shares `s_ik(a) ≥ 0` with `c_ik − (T_ik(a,b)+T_ki(b,a)) ≤ s_ik(a)+s_ki(b)` for changed states and `Σ_{k≠i} s_ik(a) ≤` single-site excitation energy ⇒ the reference `x₀` minimises `M.energy + g′` for every `g′` in `SecondOrderClass g c x₀`. Checker cost `O(n²k²)` additions (BP:792). With `c = 0`, `g = 0` this certifies that `x₀` is the GMEC of the pairwise model itself (my inference); shares exist exactly when the pairwise LP relaxation is solved by `x₀` (LP duality, "not formalised here", `F/StateShares.lean` header).
* `verify_sound_secondOrder`, `verify_sound_thirdOrder` (`F/ThirdOrderModel.lean:272`), `F/ShareLevels.lean`: many-body residuals with certified mixed-difference constants reduce to pairwise lower models that K1 certifies.

Limits: complete only for the pairwise LP relaxation; "On a domain with excluded pairs of states the certificate remains sound, but its absence proves nothing" (BP:798).

### 2.6 K6 — macro-ratio and barrier certificates

* **Macro ratio** (`F/MacroRatio.lean:30`, `macro_le_of_plan`): a transport plan `ψ ≥ 0` from `B` to `A` with `Σ_{y∈A} e^{d(z,y)}ψ(z,y) ≤ λ·w(z)` and `Σ_{z∈B} ψ(z,y) ≥ w(y)` gives `Z_g(A) ≤ λ·Z_g(B)` for every residual with `g(z) − g(y) ≤ d(z,y)`. A theorem over ℝ, no checker; "it is a design note" (BP:631); the plan is as large as the two macrostates.
* **Barriers** (`F/BarrierCertificate.lean`; `CutTree` :295 with nodes `inside | wall w | outside | branch | split`; `bverify` :592): accept iff (1) every wall certificate is accepted by K1 for `L`, (2) no inside box is adjacent to an outside box, (3) `a` inside, `b` not. Statement (:631): `bverify c I a b L = true → ∀ walk p of single-site moves from a to b, ∃ j ≤ m, L ≤ I.energy (p j)`. Variants `bverifyRTop_sound`, `bverifyOn_sound`. [V], not refereed (TR:11689); Lean only.

### 2.7 K7 — other verified components

* **Numeric layer** (`proofs/Core/Rounding.lean`): `roundDown/roundUp` (fixed-point grid `2⁻ᵖ`), `QInterval` (add, neg, sub, mul, scale, sq, inv, div, outward, hull, inter, sum), `expLo/expHi` with `exp_enclosure` (:466), `contains_boltzmann` (:580), circle charts. No `sqrt`, no kinematics, no force-field term (grep).
* **Interval → Z** (`F/IntervalInstance.lean`): computable `WInstance.lowerOfIntervals/upperOfIntervals`; `certified_partition_of_intervals` (:70).
* **Observables under pruning** (`F/Dominance.lean:162`, `boltzmannAvg_prune_error`): discarding a set that carries at most a fraction `ρ` of the survivors' weight changes any Boltzmann average bounded by `B` by at most `2Bρ`.
* **Probabilistic certificates** (`SampledSandwich`, `BoxClass`) and **geometry** (`Realizability`, `Holonomy`, `TorsionRMSD`): theorems only, no kernel (BP:515, BP:1162).

### 2.8 (iv) Trusted inputs and trusted code base

* Theorems: Lean 4.31.0 kernel + Mathlib v4.31.0, axioms `propext`, `Classical.choice`, `Quot.sound` only (`scripts/audit_all.sh:25` forbids `sorry`, `admit`, `native_decide`, `+native`, `bv_decide`, `implemented_by`, `unsafe`, anonymous `example`).
* A concrete acceptance: either Lean kernel reduction (`decide +kernel`; toy sizes only) or a re-implementation whose *specification* is the Lean function — "trusted as an implementation, not as a proof" (THY-RES-0014 §4).
* Trusted inputs: the published tables and domains; for K2 the constants `c` and anchor intervals; for K3 the weight tables. "The correspondence between the published tables and a physical force field is the producer's obligation" (BP:48). The certificate itself is untrusted.

### 2.9 (v) Arithmetic

Exact rationals everywhere; the checker "never minimises, searches, or evaluates a transcendental function" (BP:24). Floats are allowed upstream only, via directed rounding (BP §3.2): lower-instance entries down, upper-instance entries up, claimed bounds recomputed exactly. **Boltzmann factors are never computed by K3**: the instance is already in the weight domain. For a rational exponent `q = −βE`, `|q| ≤ 2^K`, `N ≥ 1`: `x = q/2^K`, `T = Σ_{m<N} x^m/m!`, `err = |x|^N (N+1)/(N!·N)`, `expLo = max(0, T−err)^(2^K)`, `expHi = (T+err)^(2^K)`; `expLo > 0` is guaranteed for `N ≥ 4` (`expLo_pos`).

### 2.10 (vi) Checking cost (BP §5; TR §6.2)

With `|D| = Σ_i |D_i|` and `‖D‖² = Σ_{i≠j} |D_i||D_j|` over listed pairs:

* K1: leaf `O(|D|·deg + ‖D‖²)`; prune `O(Σ_j |D_j|)`; branch `O(|D_i|)` + children; sum `O(|D| + ‖D‖²)` + parts. Total = Σ over visited nodes. Witness per leaf: `n + P + Σ_pairs(|D_i|+|D_j|)` rationals (dense Lean count `Cert.dataSize`: `1+n+n²+n²k`); a `sum` node embeds two instances.
* K2: K1 plus `O(A²·n)` for `A` anchors.
* K3: same shape as K1 in comparisons; products cause bit growth. K3′: `elim1` `O(nk²)`, `elim2` `O(nk² + k³)` *if tabulated* — "In Lean the new instances are closures, not tables" (`F/PartitionProduct.lean:114`).
* Barrier: one adjacency test per (inside, outside) leaf pair; "no verified statement on certificate size, and none can be polynomial in general" (BP:657).

### 2.11 (vii) JSON schema accepted by `RC` (format `metricchain-cert/1`)

Top level (`validate`, RC:283): `format` (exact string), `kind ∈ {min, residual, partition}`, `n`, `k` (JSON ints), `domains` (n duplicate-free lists) ↔ `Dom n k`, `instance`, `claim`, `certificate`. Unknown fields, duplicate keys, out-of-range indices are rejections. Rational = JSON int or string `-?digits(/digits)?`, ≤ 100 000 characters (RC:53–71).

| kind | fields → Lean |
|---|---|
| `min` | `instance.h` n×k → `PairInstance.h`; `instance.J` `{"i,j": k×k}`, unlisted = 0 → `.J`; `claim.lower_bound` → `L`; `claim.witness` (optional). Nodes: `leaf{u[n], p{"i,j"}, m{"i,j":[k]}}`, `branch{site, children{"a":node}}` (children only for `a ∈ D_site`; Lean needs all `k`), `prune{site, remove, dominator, ell{"j"}, rest}`, `sum{parts:[{instance{h,J}, bound, certificate}×2]}` → `Cert` |
| `residual` | adds `instance.c[n]`, `instance.anchors[{x, lo, hi?} or {x, value}]` → `IProblem`; nodes `anchor{index, cert}`, `branch`, `prune` → `RCert`; entry point `verifyITop`; output adds `upper_bound` |
| `partition` | `instance.w` n×k, `instance.W` `{"i,j"}` (unlisted = 1) → `WInstance`; `claim.lo/hi` optional, must contain the returned interval; nodes `leaf{lo{"i,j"}, hi{"i,j"}}`, `branch`, `prune{site, remove, dominator, q0, q{"j"}, rest}` → `ZCert`; entry point `zverifyTop` |

**Not in the schema:** `split`, `cut`/`elim1`/`elim2`, `LCert`, barrier trees, any energy/β/`exp` parameter (the partition file carries weights only), per-site `k`. Discrepancies I observed between BP and RC (benign): lowest terms is not enforced (`"2/4"` parses); "sparse differences" for `sum` parts (BP:303) is not implemented (`h` must be full); CBOR (BP:275) exists nowhere.

### 2.12 (viii) Producers

**None in this worktree.** What exists: hand-built vectors (n ≤ 3, k ≤ 2); fuzz generators inside RC (`rand_cert`, `zcert`; n ≤ 4, k ≤ 3; RC:824); `leaf_rule_best_bound` (`experiments/falsify_conjectures.py:1507`: dense SciPy LP, returns a bound, emits no certificate); pseudocode in BP §6 (`MINCERT`, `RESCERT`, `ZCERT`, `STARCERT`). The kernel type will change only "when a producer exists" (BP:211). Reported elsewhere, not in this worktree and not read by me: the Scientific Discovery Division's exact integer certificates (2⁻⁴⁰ kcal/mol) on its enumerated instances, label **[M]** (TR:2476–2486). The file lists of the other branches show `src/metricchain_eng/leafcert/` (engineering) and `experiments/science/pi_inference/certified_populations.py` (science) — other reviewers' slices.

---

## 3. (B) Executability; relation of `RC` to Lean

* `lakefile.lean` declares only `lean_lib`: **no `lean_exe`**. No `#eval`, no `def main` in `proofs/` (grep). The functions are computable, so `#eval verify …` is possible; the repository labels such runs **[M]** — "an execution of the function and not a theorem" (TR:2478).
* In-repo executions are `decide +kernel` (147 uses in 15 files); every concrete kernel instance has n ≤ 6, k ≤ 3.
* `native_decide` is forbidden by the audit (`scripts/audit_all.sh:25`).
* Scaling: "512 table entries exhausted 11.9 GB" for `verify` under `decide +kernel` (the science division's figure, TR:2507). An integer re-implementation of *one leaf check* reaches 147 456 entries in 13.5 s / 1.6 GB **[M]**, but "**No proof relates these checkers to `verify`**" (kernel_eval README §7); branch/prune/sum and restricted domains are not covered.
* The intended route (TR §12 item 7; open): "a compiled checker with a refinement proof".
* `RC` ↔ Lean: **tested, not proved.** (a) 12 vectors transcribe Lean theorems proved by `decide +kernel` (names in RC:10–13); the audit only checks that stored files equal RC's own dump (`audit_all.sh:140`). (b) 53 hostile inputs must be rejected. (c) Fuzz against brute force (n ≤ 4, k ≤ 3) checks *soundness of acceptance* and the anchor-consistency test; it never compares acceptance with Lean. (d) The harness mutation tests do not cover RC. (e) Coverage gap I found: **no vector and no fuzz case contains a `sum` node**, and no stored vector contains a partition `prune`; my three-case probe of `sum` behaved correctly. Referee R1 did not check RC (`docs/reviews/R1_referee_report.md:302`); later internal checks found crashes and misreadings, "No unsound acceptance was found" (`docs/DEAD_ENDS.md:392`).

---

## 4. (C) From a rational energy table to an enclosure of Z

1. **Inputs:** rational interval tables `[e_lo, e_hi]` (a point interval for an exact table), rational `β ≥ 0`, Taylor terms `N`, halvings `K` with `|β·e| ≤ 2^K` for **every** entry (hypotheses `hbh`, `hbJ`). BP:156: "`n = 10`, `k = ⌈log₂|q|⌉` gives relative width `≈ 3·10⁻⁵`".
2. **Weights:** `I⁻ = expLo(N,K,−β e_hi)`, `I⁺ = expHi(N,K,−β e_lo)` (`lowerOfIntervals/upperOfIntervals`). Even for exact rational `E`, `I⁻ ≠ I⁺`.
3. **Two certificates**, one per instance. `certified_partition_of_intervals` (`F/IntervalInstance.lean:70`) [V]: `zverifyTop clo I⁻ D = some (a,b)` and `zverifyTop chi I⁺ D = some (a',b')` ⇒ `a ≤ partitionFn β M.energy (boxFinset D) ≤ b'`. Kernel-run example: triangle at β = 1, `Z ∈ [2.3068, 2.3069]`.
4. **Rules:** factorised leaf (exact iff pair factors are constant on the box; producer rule "when `∏hi/∏lo ≤ 1+ε_leaf`", BP:389); branch (exact, one subtree per state; "on sites with the widest pair-factor ranges", BP:388); thermal DEE (upper end × `(1+ρ)`, lower end unchanged; budget `Σ ln(1+ρ_k) ≤ ε_prune`, BP:387); cut (exact for independent parts; otherwise loses `∏hi/∏lo` across the cut); elimination (exact).
5. **Exact graph classes:** every chain — `zverify2Top_chainCert` [V] (`m` eliminations, one leaf); tree and ring instances by kernel runs; "every interaction graph of treewidth at most two … a paper argument in general" (BP:437) **[P]**. Without cut/elim an exact lower end needs one leaf per configuration on rigid instances (`zverify2_elementary_exact_leaves`) — a statement about exact lower ends only (TR:3076).
6. **No named end-to-end theorem for `ZCert2`:** `certified_partition_of_intervals` and `certified_torsion_partition*` are stated for `ZCert`. Composition with `zverify2Top_sound` is immediate (my inference) but unwritten.
7. **Marginals/populations:** no kernel entry point and no theorem. BP only says intervals per macrostate separate or not ("the comparison itself needs no further proof object", BP:607). My inference: with per-state enclosures `[lo_a, hi_a]` (a root `branch` on site `i`), `P(x_i=a) ∈ [lo_a/(lo_a+Σ_{b≠a}hi_b), hi_a/(hi_a+Σ_{b≠a}lo_b)]`; for a real model take `lo` from `I⁻`, `hi` from `I⁺`. `zverify` returns only the root interval, so a checker must expose the children. The repository has one theorem of this ratio type (`box_trap_certificate`, `F/KineticsCertificates.lean:526`).

**My measurements (exp enclosure, re-implemented from the Lean definitions, conformance with `rounding_check_16/17`):** for a 20-bit dyadic energy and β ≈ 1.69 mol/kcal, `expLo(10, K_min, q)` has a ~5 400-bit numerator at 5 kcal/mol, ~24 000 bits at 20 kcal/mol, ~50 000 bits at 60 kcal/mol (relative width 3·10⁻⁸ … 2·10⁻⁵). Four extra halvings give 10⁵–9·10⁵ bits. Consequences: weights must be outward-rounded after `exp` (sound by `Z_encloses_partitionFn`, but that is no longer literally `lowerOfIntervals`: an unwritten two-line lemma, my inference); a single clash entry forces a large uniform `K`; RC rejects rationals above 100 000 characters.

---

## 5. (D) Continuous degrees of freedom

**Provided [V]:**

* `voxel_boltzmann_bounds` (`F/VoxelEnclosure.lean:33`): `vol(V)e^{−βE_hi} ≤ ∫_V e^{−βE} ≤ vol(V)e^{−βE_lo}` — the volume (entropy) factor that K*-type minimised-voxel surrogates drop.
* `pairwise_voxel_weight_bounds` (`F/VoxelBridge.lean:121`), any measurable space: voxel energy enclosed by two pairwise **table** models + factorised volume + bracketed factors ⇒ the instance weights bracket the voxel integral.
* `certified_torsion_partition_top` (:457): end to end for `E(θ) = Σ_i u_i(θ_i) + Σ_{i≠j} U_ij(θ_i,θ_j)` on `Fin n → ℝ` with product voxels — **one real coordinate per site**. Multi-χ residues fit only the abstract bridge, not this theorem (my reading).
* Chart-arc volume brackets (`chartArc_onebody_brackets_pos/_neg`); `separable_voxel_bounds`, `separable_voxel_ratio` (`F/SeparableVoxel.lean:47, 81`).

**Implementer must supply (hypotheses, never checked):** for every cell / pair of cells in the box, real tables `M_lo ≤ u_i, U_ij ≤ M_hi`; measurability; disjoint cells; volume and Boltzmann brackets; for second order, separable envelopes from a Hessian enclosure.

**Explicitly not provided:** "certifying envelope constants for a concrete learned residual, interval evaluation of force-field terms over voxels, and any claim of practical solver performance are outside the development" (`README.md:700`); the Taylor step is [P]; "Only the base chart is formalized" (BP:408); no `sqrt` enclosure (Coulomb), no kinematics, no Lennard-Jones term in Lean. Cost grows like `d^{d/2}` in the voxel dimension (`docs/ASSUMPTION_AUDIT.md:405`).

---

## 6. (E) Limitations and unsupported cases stated in BLUEPRINT.md

Trust and format
* "Guarantees are relative to the *published instance* … and, for residual problems, to the *published envelope and anchor values*." (:47)
* Well-formedness is part of the check; "A checker must never crash on a file" (:33–46).
* RC "is *not* trusted; the Lean kernels are" (:1280).
* Anchor `value` "only for residuals that are exactly rational …; never for floating-point evaluations" (:104); "There is no default reading of a bare number" (:224).
* Without the consistency check "every claim about inconsistent data would be vacuous" (:237); a negative factor makes the bare partition checker miss `Z` (:260).
* If no anchor has an upper value "no upper bound is reported … avoid this" (:244).

Rule sets
* Kernels implement only the site-additive envelope `Σ c_i[x_i≠y_i]`; table envelopes must be closed first (:71–75).
* `split`: "not yet in the reference checker or its conformance vectors"; not below `branch`/`prune`/`sum` (:202–211).
* `sum` "is *necessary*" (:199).
* "The JSON format `metricchain-cert/1` and the reference checker do not carry `cut`/`elim` nodes yet" (:443).
* Treewidth ≤ 2 in general: "a paper argument" (:439).
* Macro-ratio plans: "a design note" (:631). Barrier trees: "**not** yet part of the JSON schema or of the reference checker" (:660).
* Linear kernel: Lean only; "features with entries of both signs must be split" (:1127).

Numerics and geometry
* Overlapping charts "must be resolved by a disjoint choice of voxels for partition functions" (:126).
* Lennard-Jones needs a certified `r² ≥ ρ > 0` (:133); Coulomb needs a producer-supplied square-root witness (:135); bond-angle constants enter as intervals (:141).
* "`expLo > 0` needs `n ≥ 4`" (:157); cells of one site "must be pairwise disjoint" (:400).
* The volume bound `2(t₂−t₁)` "does **not** tighten when a cell is subdivided" (:403).
* "The Hessian enclosure itself … is the producer's obligation and is not covered by the Lean development." (:421)
* `SE(3)` "is not defined in the Lean development" (:1029); Lipschitz constant and inertia bounds "are hypotheses of the verified statements, not conclusions" (:1043).
* "**Warning: this route does not scale with chain length**" (:1046).
* Eigenvalue enclosures for §8.1 not in Lean (:1162); §8.4 "cited, not formalized" (:1191).

Residuals and free energies
* Envelope constants `c_i`, `c_ij`, `c_T` are "the producer's obligation"; "measured maxima over an enumerated domain are not certified bounds" (:750, :773).
* "**Do not use the `Σ c_i²` width with a correlated reference**: it is false there" (:460).
* Statistical estimates make a certificate "probabilistic and outside the verified kernel" (:468); such certificates "are **not** checked by any kernel of this repository" (:515); "The verifier, not the producer, must draw the points" (:558); "Sampling must be exact" (:510).
* Share certificates on domains with excluded state pairs: sound, but absence "proves nothing" (:798).
* "No kernel for such transcripts is implemented here." (:999)

Further caveats (producer side and scope)
* Rounding mistakes "can only cause rejection, never an unsound acceptance" (:117); the kernel is "the linear-time end" of the witness-size trade-off (:314).
* Producer loops: termination "by exhaustion of the finite box" (:336); `STARCERT` "does not terminate" without its fallback (:740); `κ` is "a planning parameter, not something the kernel knows" (:683).
* The second-order voxel rate is "not an optimal rate" (:421); Rio's sharper width is "cited …, not verified" (:453).
* A floor "must be **certified**"; "a constant fitted or observed on samples is not a floor" (:504–506); drawing proposals "*until* `N` are accepted is not covered" (:589); the sampled sandwich "presupposes exact sampling from `p`, exact evaluation of `Δ` and a known `Z₀`" (:885); "Exact equality of values is assumed" (:997).
* Third-order pairwise model "is a relaxation, not the exact envelope" (:771); the share-allocation rule is safe "for the lower end of `ln Z`" only up to a stated threshold (:828).
* "A learned residual is admissible in this framework only if it ships with an envelope." (:1005); the RMSD envelope route is "not yet a kernel" (:1058).
* Pair-profile format: the favourable regime "has not been reached at any size that could be enumerated" (:1099); it does not cover chirality, sequence-specific pairs, many-body terms, steep short-range terms (:1109–1113).
* The s-stress bound "is not tight in general" (:1156); the torsion→RMSD bound is "Worst-case (`ℓ¹`)" (:1183).

§9 "do not try to engineer around these": pure dual certificates are incomplete; certificates without `sum` are exponential; the partition kernel without decomposition rules needs `k^n` leaves for exact lower ends; the smallest certificate is NP-hard to find; first-order envelopes with point evaluations are exponential in the number of non-sharp sites; voxel quadrature `O((βΔM·d/ε)^{d/2})`; distances alone are blind to chirality.

---

## 7. (F) Obstacles for a real side-chain packing instance (50–300 residues, 3–80 rotamers, float tables)

Everything here is my assessment unless a source is cited.

1. **No producer.** Needed: a dual solver emitting messages (TRW-S/MPLP/soft arc consistency), exact recomputation of `u`, `p`, `ℓ`, DEE, component detection for `sum`, branching, an incumbent.
2. **Float → rational.** A binary64 is exactly a dyadic rational, so the table itself can be published without rounding; the statement is then about the table read as exact reals. A statement about the force field needs evaluation error bounds — none exist here.
3. **Exact optimality needs a convention.** K1 proves `L ≤ E(x)`. A float dual solver will not reach `L = E(x*)` exactly. Either accept a certified ε-gap, or use tables on a common grid (as integer-cost solvers do) plus an integrality step `E(x) ∈ 2⁻ᵖℤ ⇒ E(x) ≥ ⌈L⌉_grid` — trivial, but not in Lean.
4. **Certificate size.** One leaf carries messages for every ordered interacting pair: about `2P·k` rationals (P = 3 000, k = 30 → 1.8·10⁵). Fine for one leaf, prohibitive for 10⁴ leaves without delta encoding (BP:311 names the trade-off; nothing is implemented). Every `sum` node embeds two instances with full `h`. Uniform `k` forces `k×k` padding per pair.
5. **Checking time.** Measured: RC needs 6.0 s for one zero-message leaf at n = 60, k = 20 (1.4·10⁶ ordered-pair entries, ≈4 µs each) and loops over all `n(n−1)k²` entries regardless of sparsity. Extrapolated (not measured): ≈4 min per leaf at n = 200, k = 40. A compiled, sparse, integer checker is required.
6. **Deep nesting.** `prune` nests through `rest`. RC accepted chains of 12 000 nested prunes through the object API; my JSON serialisation of that depth already failed, and RC rejects 30 000 levels by design. A DEE-heavy run on 300 residues can exceed this.
7. **Treewidth (Z).** Exact rules stop at degree-2 elimination; packed cores have larger treewidth. Bounding weak pairs by `[lo,hi]` costs `β·Σ(pair-energy ranges)` in `ln Z`, extensive in the number of pairs. No higher-arity factor exists (`WInstance` is pairwise). Realistic near-term scope for Z: chains, low-treewidth abstractions, or K*-sized active sites by enumeration — where the factorised leaf is a weaker bound than an A*-style bound (it takes the max of each pair factor independently).
8. **Exp precision.** See §4: uniform `K`, 10⁴–10⁶-bit weights unless rounded; fixed-point `roundDown` loses small Boltzmann factors (shift energies by the incumbent energy first).
9. **Trust perimeter.** The file contains its own instance and domains. Probe: an empty domain makes RC accept `lower_bound = 10⁶` (a true statement about an empty box); a witness outside the box is silently ignored (no `certified_gap`). A consumer must bind the file to the intended energy table and full rotamer sets.
10. **Model fit.** Only one-body + two-body terms. Non-pairwise terms go to K2/K5, which need certified constants that nobody has produced. Continuous rotamers need §5's missing interval evaluation.
11. **Hard exclusions.** Forbidden pairs need a finite surrogate cost (sound for lower bounds) or weight 0 (allowed in K3).

---

## 8. Fifteen-field records

Common to all: (1) Theoretical Research Division unless noted; (2) commit `eb88823c931953d6455f79c9d8089063abfb442b`. "Mine" marks my own knowledge, not the repository's.

**R1 — Min-energy kernel K1 (leading candidate).** (3) TR §6.1 Master Soundness Theorem (row E1); Theorem 6.1. (4) `Cert`, `verify`, `verify_sound`, `certified_optimum`, `verify_sound_real`, `verify_sound_real_symm`. (5) Finite product domain; pairwise rational tables; real model bounded below entrywise (or by symmetrised sums). (6) [V]. (7) Referee R1 read the statements ("I found no false theorem", `R1_referee_report.md:31`), did not check the Lean build or RC. (8) 4 `min` vectors; RC fuzz (n ≤ 4, k ≤ 3); kernel runs n ≤ 6; harness VII.1; SCI-division instances [M]. (9) `triangle_no_leaf_certificate` (LP gap); `sumFree_exponential`; kernel evaluation does not scale [M]. (10) Proof that no rotamer assignment of the published table has energy below `L`; with a witness, the GMEC up to the gap. (11) Producer; exact dyadic/integer tables; compiled checker. (12) Auditable GMEC for fixed-backbone packing; independent check of an exact solver's optimum. (13) Repo: toulbar2 and OSPREY emit no checkable proofs; pseudo-Boolean proof logging (VeriPB/CakePB) covers the ingredients; which is cheaper "has not been measured" (TR:1057). Mine: toulbar2 (exact, integer costs, soft-consistency bounds), OSPREY DEE/A*, Rosetta packer (stochastic), SCWRL4/FASPR (heuristic), MPLP/TRW-S, ILP. (14) Empty box; box not the intended rotamer set; table not bounding the model; LP gap with a huge search tree. (15) **Partially** — kernel, schema and reference checker exist; producer, scalable checker, exactness convention and refinement proof are missing.

**R2 — Split layer.** (1) Theory, requested by Scientific Discovery (P7-T2). (3) TR Prop 11.18b(e) (i). (4) `SCert`, `verifyS`, `verifyS_sound`, `leafOK_mono`, `split_leaves_iff_branch`. (5) As R1. (6) [V]. (7) Written by a subagent under a brief, checked by the coordinator (THY-RES-0014); I found no referee report. (8) `splitTriangle_*` kernel runs; the requesting division measures a factor 3.8–6.7 fewer checks (TR:2497). (9) Cannot sit below `branch`/`prune`/`sum`. (10) Binary domain splitting. (11) Schema and checker extension. (12) Natural form of binary-branching search trees. (13) None named. (14) No power beyond `branch`. (15) **Partially** (Lean only).

**R3 — Numeric layer and interval→Z pipeline.** (3) TR §5 (row B1), §3.4. (4) `roundDown`, `roundUp`, `QInterval.*`, `expLo`, `expHi`, `exp_enclosure`, `contains_boltzmann`, `WInstance.lowerOfIntervals`, `certified_partition_of_intervals`. (5) `N ≥ 1`, `|q| ≤ 2^K`, rational β. (6) [V]. (7) R1 did not check `Rounding.lean` "beyond two spot checks". (8) `rounding_check_1…33`; `triangle_real_partition_enclosure`; my re-implementation reproduces checks 16/17. (9) None recorded; "verified interval libraries exist" (TR:67). (10) Rigorous Boltzmann-factor brackets. (11) Big-integer arithmetic; choice of `N`, `K`, rounding precision. (12) Library for any certified-Z tool. (13) Repo: LeanCert, girving/interval. Mine: MPFI/Arb. (14) Clash entries force a large uniform `K`; unrounded weights are too large to use. (15) **Yes** as a library; **partially** as a pipeline (rounded variant and `ZCert2` composition unwritten).

**R4 — Partition kernel K3 (elementary rules).** (3) TR §3.1, §3.4 (rows D1, D3). (4) `ZCert`, `zverify`, `zverifyTop_sound`, `zprune_sound`, `Z_encloses_partitionFn`, `thermal_dee`, `boltzmannAvg_prune_error`. (5) Nonnegative weights (checked). (6) [V]. (7) R1: sound but "too weak for the stated application" (`R1:38`). (8) 4 partition vectors; fuzz; harness I.5, I.6; benchmark B6 (n ≤ 6). (9) D22: exponential on chains; `negativeW_unguarded`. (10) Two-sided bound on Z of a rotamer box; with voxel weights, of a continuous integral. (11) Weight tables from R3; producer. (12) K*-style enumeration certificates for small active sites; population intervals (my inference). (13) Repo: no verified checker for deterministic two-sided bounds on a weighted sum was found (TR:60); K*/BBK*. Mine: toulbar2's ε-approximate log-Z mode, OSPREY MARK*, mini-bucket and tree-reweighted bounds. (14) Dense interaction graphs: leaves loose, enumeration exponential. (15) **Partially.**

**R5 — Extended partition kernel K3′ (cut, elimination).** (3) TR Theorems 11.19, 11.20 (row G9). (4) `ZCert2`, `zverify2`, `zverify2Top_sound`, `WInstance.Z_cut`, `Z_elim1`, `Z_elim2`, `chainCert`, `zverify2Top_chainCert`, `chain_separation`. (5) Nonnegative weights; eliminated site has ≤ 2 neighbours on the box. (6) [V] for soundness and every chain; [P] for treewidth ≤ 2 in general. (7) §§11.1–11.9 refereed by R2, with reservations M4 (D33). (8) Kernel runs: chain (6 sites), tree, ring; harness XI.12. (9) D33: separation concerns exact lower ends and a representation-dependent rigidity. (10) Transfer-matrix computation as a certificate. (11) JSON nodes, tabulating checker, elimination-order producer. (12) Exact Z for chain-like or series-parallel interaction graphs. (13) Mine: bucket/variable elimination, weighted model counters. (14) Treewidth > 2; prune cannot precede elimination. (15) **Partially/No** for real proteins (Lean only; treewidth limit).

**R6 — Residual kernel K2.** (3) TR §6.1; Theorems 2.3–2.6. (4) `RCert`, `verifyR`, `verifyITop`, `verifyITop_sound`, `IProblem.consistent_iff_nonempty`, `verifyR_sound_real`. (5) Residual with single-site bounded differences `c_i`; interval anchor data. (6) [V]. (7) R1 (statements); the underlying mathematics is classed "known in substance" (TR §0.2). (8) 8 residual vectors; fuzz. (9) D15 (vacuous on inconsistent data, repaired); D42 (per-torsion constants do not scale); cost exponential in non-sharp sites (BP §9). (10) GMEC bounds valid for every correction term in an envelope class. (11) Certified `c_i` — "none are certified here". (12) Non-pairwise terms (solvation, learned corrections) with guaranteed bounds. (13) Repo: iMinDEE is a special case. (14) `c_i` above the single-site excitation energies; uncertified constants. (15) **Partially** (kernel yes; no usable constants for any real term).

**R7 — Share certificates / higher-order lower models.** (1) Theory; statements proposed or requested by Scientific Discovery. (3) Theorem 11.18a; Prop 11.18b(a),(d),(e). (4) `secondOrder_certified_of_shares`, `…_of_rowSum`, `…_of_state_shares`, `…_of_deficit_shares`, `verify_sound_thirdOrder`, `cover_of_level_shares`. (5) Certified mixed-difference constants; product domain for completeness. (6) "(a) V; (b) P from K; (c) V for the covering, P for the rest; (d) V; (e) V for soundness, P for the duality; N for the frequencies; M for the division's instances" (TR:2356). (7) Reviewed by Scientific Discovery (SCI-REV-0012). (8) Harness XI.17, XI.21; division's instances [M]. (9) Integrality gaps; excluded state pairs (D59); dense constants (D32). (10) Reference rotamer assignment proved optimal by additions. (11) An `O(n²k²)` checker (to be written; no Lean `Bool` function); one LP for the producer. (12) Cheap one-shot GMEC certificate when the LP is tight. (13) Mine: this is LP-dual feasibility, as in MPLP/TRW-S certificates. (14) LP not tight at the reference. (15) **Partially.**

**R8 — Voxel enclosure, bridge, separable voxels.** (3) TR §3.4 (row D4). (4) `voxel_boltzmann_bounds`, `Z_encloses_voxel_integral`, `pairwise_voxel_weight_bounds`, `certified_torsion_partition_top`, `chartArc_onebody_brackets_pos`, `separable_voxel_bounds`. (5) Measurability; disjoint cells; voxelwise table enclosures. (6) [V]; Taylor step [P]. (7) R1 did not check measurability side conditions or chart brackets beyond spot checks. (8) `exact_witness`, `pair_witness`, `chart_witness`. (9) D18 (pipeline once assumed its key hypothesis; repaired). (10) Conformational entropy inside rotamer wells included in Z. (11) Verified interval evaluation of force-field terms — absent. (12) Continuous-rotamer free energies. (13) Repo: K* uses minimised-voxel surrogates. (14) High voxel dimension (`d^{d/2}`); steep terms. (15) **No** (missing prerequisite).

**R9 — Linear/profile kernel K4.** (3) Prop 11.50. (4) `LProblem`, `LCert`, `verifyL`, `verifyLTop_sound`. (5) Nonnegative pairwise features; coefficient box; exact anchors. (6) [V]; "not refereed". (7) None. (8) `contactTriangle_*`; harness XIV.3. (9) None recorded. (10) Bounds valid for every coefficient vector of a parametrised energy term. (11) Schema, checker, producer. (12) Force-field parameter uncertainty. (13) None named. (14) Wide coefficient boxes; inconsistent anchors (vacuous). (15) **No** for a first release.

**R10 — Barrier and macro-ratio certificates.** (1) Scientific Discovery (`KineticsCertificates.lean`) and Theory. (3) Theorems 11.115, 11.105. (4) `bverify`, `bverify_sound`, `bverifyRTop_sound`, `bverifyOn_sound`, `box_trap_certificate`, `macro_le_of_plan`. (5) Single-site (or site-graph) moves. (6) [V]; Theorem 11.105 partly [P]. (7) "Not refereed" (TR:11689); parts (c)–(e) reviewed by Scientific Discovery (SCI-REV-0013). (8) Kernel runs (`maze_barrier_exact`, …); no harness test. (9) Barrier decision PSPACE-complete (cited). (10) Lower bounds on rotamer-flip barriers; trap survival. (11) Schema, checker, producer. (12) Certified kinetic statements. (13) None named. (14) Certificate size unbounded in general. (15) **No** for a first release.
