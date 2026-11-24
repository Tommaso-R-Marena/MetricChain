# MetricChain — Engineering Blueprint

Self-contained specification for a team that will **implement and benchmark** the systems whose
correctness is established in `proofs/` and explained in `THEORY_REPORT.md`.  Nothing here has to
be re-derived; every rule cites the machine-checked statement that makes it sound.

Contents: 1 trust model · 2 objects · 3 numeric semantics · 4 certificate schemas ·
5 verification algorithms and their cost · 6 producer algorithms (untrusted) ·
7 envelope-exporting equivariant residuals · 8 geometry certificates · 9 limits and impossibility
boundaries · 10 task mapping · 11 conformance tests.

---

## 1. Trust model

```
 untrusted                                   trusted (small, verified)
┌───────────────────────────┐   certificate  ┌──────────────────────────────┐
│ solver / sampler / network│ ─────────────▶ │ checker: exact rational       │──▶ accept + bound
│ (floats, heuristics, GPUs)│   (rationals)  │ comparisons only              │    / reject
└───────────────────────────┘                └──────────────────────────────┘
```

* The checker performs **only** rational additions, multiplications and comparisons.  It never
  minimises, searches, or evaluates a transcendental function.
* A reference checker exists as Lean definitions (`verify`, `verifyR`, `zverify`) with soundness
  theorems; any re-implementation must agree with it on the conformance vectors of §11.
* Guarantees are relative to the *published instance* (tables of rationals) and, for residual
  problems, to the *published envelope and anchor values*.  The correspondence between the
  published tables and a physical force field is the producer's obligation and is discharged by
  outward rounding (§3).

---

## 2. Objects

| object | definition | Lean |
|---|---|---|
| instance `I` | `n` sites, `k` states; `h[i][a] ∈ ℚ`; `J[i][j][a][b] ∈ ℚ` for ordered pairs `i ≠ j` (an unordered interaction may be stored in one orientation or split between both) | `PairInstance` |
| energy | `E(x) = Σ_i h[i][x_i] + Σ_{i≠j} J[i][j][x_i][x_j]` | `PairInstance.energy` |
| domains `D` | list of surviving states per site; box `∏ D` | `Dom`, `InBox` |
| envelope constants | `c[i] ≥ 0`: changing site `i` alone changes the residual by at most `c[i]` | `RProblem.c`, `ResidualClass` |
| anchors | evaluated pairs `(x, Δ(x))` | `RProblem.anchors` |
| weight instance | `w[i][a] ≥ 0`, `W[i][j][a][b] ≥ 0` (rational Boltzmann factors) | `WInstance` |
| partition sum | `Z(D) = Σ_{x∈∏D} ∏_i w[i][x_i] ∏_{i≠j} W[i][j][x_i][x_j]` | `WInstance.Z` |

**States.**  A state of site `i` is a pair (basin label, voxel of the torsion box).  Voxels are
boxes in the rational chart coordinates of §3.3.  For partition functions the one-body factor of
a voxel state includes its volume (§6.3).

**General envelopes.**  The theory holds for any envelope `d` (zero diagonal, triangle
inequality).  The kernels implement the site-additive bounded-difference envelope
`d(x,y) = Σ_i c[i]·[x_i ≠ y_i]`; a table envelope `δ_i(a,b)` must first be replaced by its
shortest-path closure (Floyd–Warshall per site, `O(k³)`), and may be used in the producer's
pruning tests (§6.2) even though the reference kernel checks the uniform constants `c[i]`.

---

## 3. Numeric semantics

### 3.1 Rationals in certificates

Every number in a certificate is an exact rational, serialised as a decimal integer string or
`"p/q"` in lowest terms (`q > 0`).  Dyadic rationals (`q = 2^m`) are recommended: they are exactly
representable from IEEE-754 doubles and keep denominators bounded.

### 3.2 Outward rounding protocol for floating-point producers

`roundDown_p(q) = ⌊q·2^p⌋ / 2^p ≤ q ≤ ⌈q·2^p⌉ / 2^p = roundUp_p(q)`, with
`roundUp_p(q) − roundDown_p(q) ≤ 2^{−p}` (`roundDown_le`, `le_roundUp`,
`roundUp_sub_roundDown_le`).  An interval `[lo, hi]` is rounded outward to
`[roundDown_p(lo), roundUp_p(hi)]`, widening by at most `2·2^{−p}` (`outward_width_le`).

Rules for a producer that computes in binary64:

| quantity | published value | direction |
|---|---|---|
| table entry of a **lower** instance (used for lower bounds on energy) | `roundDown_p(fl(e) − err(e))` | down |
| table entry of an **upper** instance (used to evaluate incumbents) | `roundUp_p(fl(e) + err(e))` | up |
| Boltzmann factor, lower / upper weight instance | `expLo`, `expHi` of the outward-rounded exponent (§3.4) | down / up |
| dual variables (messages `m`) | any rounding (nearest dyadic) | soundness does not depend on them |
| claimed bounds `u, p, ℓ` (tropical) and `lo` (partition) | recomputed **in exact rational arithmetic** from the rounded duals and the published tables, or float value minus accumulated error, rounded down | down |
| claimed bounds `hi`, ratios `q₀, q_j` (partition) | exact recomputation, or float plus error, rounded up | up |

`err(e)` is a rigorous bound on the floating-point evaluation error of the table entry (interval
arithmetic or a running error bound).  Because the checker re-verifies every inequality exactly,
a mistake in rounding can only cause rejection, never an unsound acceptance.  Precision loss per
leaf is at most `(n + P)·2^{−p}` for `P` listed pairs.

### 3.3 Rational charts of the torsion circle

Chart `q ∈ {0,1,2,3}` and parameter `t ∈ [−1/2, 1/2]` represent the unit vector
`quarterTurn_q((1−t²)/(1+t²), 2t/(1+t²))`, where the quarter turns are
`(a,b), (−b,a), (−a,−b), (b,−a)`.  Every torsion angle lies in at least one chart
(`circle_rational_atlas`); the charts overlap, which is harmless for lower bounds and must be
resolved by a disjoint choice of voxels for partition functions (use `|t| ≤ tan(π/8)`-type
boundaries enclosed between rationals, assigning the sliver to exactly one chart).  In chart
coordinates:

* `cos θ, sin θ` are rational in `t`; products of rotation matrices (forward kinematics) and
  squared inter-atomic distances are rational functions with denominators `∏ (1+t_i²) ∈ [1, 5/4]^M`;
* torsional terms `cos(nθ − γ)` are polynomials in `(cos θ, sin θ)`;
* 12-6 Lennard-Jones terms are rational in `r²` and require a certified bound `r² ≥ ρ > 0` on the
  voxel (the interval inverse `inv` needs a positive lower end);
* Coulomb terms need `√(r²)`: the producer supplies a rational `s` and the checker verifies
  `s² ≤ r²_lo` (lower bound on `r`) or `s² ≥ r²_hi`;
* the arc-length element is `dθ = 2 dt/(1+t²)`; voxel volumes are enclosed by rational bounds of
  this density.

Interval evaluation of these expressions over a voxel uses `QInterval` (`contains_add`,
`contains_mul`, `contains_sq`, `contains_inv`, `contains_circParam`).  Bond-geometry constants
(sines and cosines of bond angles) are irrational in general and enter as enclosing rational
intervals.

### 3.4 Certified exponential

For a rational `q` with `|q| ≤ 2^k` and `n ≥ 1`:

```
x      = q / 2^k
T      = Σ_{m<n} x^m / m!
err    = |x|^n · (n+1) / (n!·n)
expLo  = max(0, T − err)^(2^k)          expHi = (T + err)^(2^k)
```

`expLo ≤ exp(q) ≤ expHi` (`exp_enclosure`).  `n = 10`, `k = ⌈log₂|q|⌉` gives relative width
`≈ 3·10⁻⁵`; increase `n` for tighter factors.  `expLo > 0` needs `n ≥ 4` (`expLo_pos`).  For an
energy interval `[e_lo, e_hi]` and rational `β ≥ 0` the Boltzmann factor lies in
`[expLo(−β e_hi), expHi(−β e_lo)]` (`contains_boltzmann`).

---

## 4. Certificate schemas (JSON, format `metricchain-cert/1`)

Common envelope of every certificate file:

```json
{
  "format": "metricchain-cert/1",
  "kind": "min" | "residual" | "partition",
  "n": 3, "k": 2,
  "domains": [[0,1],[0,1],[0,1]],
  "instance": { ... },
  "claim": { ... },
  "certificate": { ...node... }
}
```

Sparse tables: `"J": {"0,1": [[..k..] × k], ...}` lists ordered pairs; unlisted pairs are `0`
(tropical) or `1` (weights).  Per-pair scalars use the same `"i,j"` keys, per-site scalars use
arrays of length `n` or objects keyed by site.

### 4.1 `kind = "min"` — lower bound on the minimum energy (`Cert`, `verify`)

`"instance": {"h": [[q]], "J": {...}}`, `"claim": {"lower_bound": q, "witness": [x_0..x_{n-1}]}`.

| node | fields | check (on the current domains `D`) | Lean |
|---|---|---|---|
| `leaf` | `u[i]`, `p{i,j}`, `m{i,j}[a]` | `∀i ∀a∈D_i: u_i ≤ h_i(a) + Σ_{j≠i} m_ij(a)`; `∀i≠j ∀a∈D_i ∀b∈D_j: 2 p_ij ≤ J_ij(a,b) + J_ji(b,a) − m_ij(a) − m_ji(b)`; `L ≤ Σ_i u_i + Σ_{i≠j} p_ij` | `LeafOK`, `leaf_sound` |
| `branch` | `site`, `children{state: node}` | every `a ∈ D_site` has a child; check it with `D_site := [a]` | `verify` |
| `prune` | `site i`, `remove r`, `dominator t`, `ell{j}`, `rest` | `t ∈ D_i`, `t ≠ r`; `∀j≠i ∀s∈D_j: ℓ_j ≤ J_ij(r,s)+J_ji(s,r)−J_ij(t,s)−J_ji(s,t)`; `0 ≤ h_i(r) − h_i(t) + Σ_{j≠i} ℓ_j`; continue with `r` removed from `D_i` | `PruneOK`, `prune_step` |
| `sum` | `parts: [{instance, bound, certificate} × 2]` | termwise on `D`: `h¹+h² ≤ h`, `J¹+J² ≤ J`; `L ≤ L₁ + L₂`; check each part against its own instance | `SumOK`, `sum_step` |

Accepted ⇒ `lower_bound ≤ E(x)` for all `x ∈ ∏ D` (`verify_sound`).  The checker additionally
evaluates `E(witness)` and reports the certified gap `E(witness) − lower_bound`
(`certified_optimum`).

`sum` covers independent components, tree/edge decompositions (dual decomposition) and
relaxations (drop nonnegative terms).  It is *necessary*: without it certificates for `m`
independent frustrated components need `≥ 2^m` leaves (§9).

### 4.2 `kind = "residual"` — energy with a non-decomposable residual (`RCert`, `verifyR`)

`"instance": {"h":…, "J":…, "c": [q × n], "anchors": [{"x": [...], "value": q}, ...]}`.

| node | fields | check | Lean |
|---|---|---|---|
| `anchor` | `index`, `cert` (a `min` node) | check `cert` against the *anchored* instance `h'_i(s) = h_i(s) − c_i·[s ≠ x^a_i]`, `J' = J`, with bound `L − value_a` | `PairInstance.anchored`, `residual_ge_anchor` |
| `branch` | as above | as above | `verifyR` |
| `prune` | as above | as above with margin `c_i` instead of `0` (differential DEE) | `PruneOK … (P.c i)` |

Accepted ⇒ for **every** residual `g` with single-site variation `≤ c_i` and the listed anchor
values, `L ≤ E(x) + g(x)` on the box (`verifyR_sound`); if anchor `a` lies in the box the true
optimum is in `[L, E(x^a) + value_a]` (`certified_gap`).

### 4.3 `kind = "partition"` — two-sided bound on a partition sum (`ZCert`, `zverify`)

`"instance": {"w": [[q]], "W": {...}}` with all entries `≥ 0`; the checker *returns* an interval
`[lo, hi]`; `"claim": {"lo": q, "hi": q}` must contain it.

| node | fields | returns | Lean |
|---|---|---|---|
| `leaf` | `lo{i,j}`, `hi{i,j}` | check `0 ≤ lo_ij ≤ W_ij(a,b) ≤ hi_ij` on `D`; return `S·∏ lo`, `S·∏ hi`, `S = ∏_i Σ_{a∈D_i} w_i(a)` | `LeafZOK`, `zleaf_sound` |
| `branch` | `site`, `children` | sum of the children's intervals over the *distinct* states of `D_site` | `Z_branch`, `foldr_addIv_sound` |
| `prune` | `site i`, `remove r`, `dominator t`, `q0`, `q{j}`, `rest` | check `t∈D_i`, `t≠r`, `q0 ≥ 0`, `w_i(r) ≤ q0·w_i(t)`, `q_j ≥ 0`, `∀s∈D_j: W_ij(r,s)W_ji(s,r) ≤ q_j·W_ij(t,s)W_ji(s,t)`; with `[lo', hi']` from `rest` on `D∖r` return `[lo', (1 + q0 ∏_j q_j)·hi']` | `PruneZOK`, `zprune_sound` |

Accepted ⇒ `lo ≤ Z(D) ≤ hi` exactly (`zverify_sound`).  To bound a *real* partition function,
publish two weight instances `I⁻ ≤ true factors ≤ I⁺` and two certificates; then
`lo(I⁻) ≤ Z_true ≤ hi(I⁺)` (`Z_encloses_partitionFn`; for continuous integrals
`certified_voxel_partition`).

A compact binary encoding (canonical CBOR of the same tree, rationals as tagged integer pairs) is
recommended for large certificates; it carries no additional semantics.

---

## 5. Verification algorithm and cost

```
verify(node, I, D, L):
  case leaf:    return all three leaf inequalities hold on D
  case branch:  return all( verify(child[a], I, D[site := [a]], L) for a in D[site] )
  case prune:   return prune inequalities hold on D (margin 0) and
                       verify(rest, I, D[site := D[site] \ {r}], L)
  case sum:     return sum inequalities hold on D and
                       verify(c1, I1, D, L1) and verify(c2, I2, D, L2)
```

`verifyR` and `zverify` have the same shape (§4.2, §4.3).

Cost model (rational comparisons; `|D| = Σ_i |D_i|`, `‖D‖² = Σ_{i≠j} |D_i||D_j|` over listed
pairs):

| node | time | witness size |
|---|---|---|
| leaf | `O(|D|·deg + ‖D‖²)` | `n + P + Σ_{pairs}(|D_i| + |D_j|)` rationals |
| branch | `O(|D_site|)` + children | 1 site index |
| prune | `O(Σ_{j} |D_j|)` | `deg(i)` rationals |
| sum | `O(|D| + ‖D‖²)` + parts | two sub-instances (may be given as sparse differences) |

Total time = Σ over visited nodes; no node requires more than one pass over the instance tables
restricted to the current domains.  Implementation notes: (i) domains are immutable along a
root-to-leaf path except for one site per node — use persistent arrays or undo stacks;
(ii) rational comparisons of dyadics reduce to integer comparisons after one shift;
(iii) children of a branch node can be checked in parallel.

**Witness-size / checking-time trade-off.**  Supplying the dual solution (messages) makes every
leaf a linear-time check.  Omitting it shrinks the certificate but forces the checker to solve an
LP per leaf; delta-encoding messages along the tree is the intermediate point.  The kernel
specified here is the linear-time end.

---

## 6. Producer algorithms (untrusted; hardware-agnostic pseudocode)

### 6.1 Certified minimisation without residual

```
MINCERT(I, eps):
  D ← full domains;  U, witness ← any heuristic solution (local search, sampling)
  return NODE(I, D, U − eps)

NODE(I, D, L):
  repeat DEE: find (i, r, t) with Goldstein margin ≥ 0 on D → emit prune node, D ← D \ (i, r)
  split I on D into independent components (or a tree/edge decomposition) I = I₁ + I₂ + …
      if more than one part: allot L = Σ L_q and emit nested sum nodes of NODE(I_q, D, L_q)
  run a dual solver (TRW-S, MPLP, soft arc consistency) on (I, D) → messages m, bound b
  if b ≥ L: emit leaf(u, p, m) with u, p recomputed exactly from the rounded messages
  else: choose a site (largest dual gap / most fractional), emit branch over its states
```

Soundness of the output is checked by `verify`; termination is by exhaustion of the finite box.
`sum` should be attempted at *every* node: fixing a site by branching frequently disconnects the
remaining interaction graph (for a chain, fixing one unit separates the two sides unless
long-range contacts link them).

### 6.2 Certified minimisation with a residual

Exact criteria (Theorems 2.3 and 2.6 of the theory report), with `d` the envelope, `L, U` the
McShane envelopes of the anchors:

* a configuration `x` may be discarded **iff** `∃y: E₀(x) > E₀(y) + d(y,x)` *or*
  `∃y: E₀(x) + L(x) > E₀(y) + U(y)`;
* an incumbent anchor `a` is certified optimal for *every* admissible residual without further
  evaluations iff `d(a,y) ≤ E₀(y) − E₀(a)` for all `y`.

```
RESCERT(I, c, residual_oracle, eps):
  anchors ← [(x₀, residual_oracle(x₀))] with x₀ ≈ argmin E₀
  loop:
    a* ← best anchor;  U ← E(a*) + value(a*)
    for each anchor a: I_a ← anchored instance (h'_i(s) = h_i(s) − c_i [s ≠ a_i])
    build an RCert for bound L = U − eps:
        differential DEE (margin ≥ c_i)                         → prune nodes
        branch; in each cell pick the anchor a maximising
            value(a) + lower bound of I_a on the cell           → anchor node + MINCERT on I_a
    if every cell closes: return certificate (gap ≤ eps)
    else: pick the cell with the smallest lower bound, evaluate the residual at its
          best configuration for I_a (a new anchor), repeat
```

Why this is the right loop: a cell is closed exactly when `min (E₀ + L) ≥ U − ε` on it, and the
only way to raise `L` is a new anchor inside or near the cell (`robust_min_bracket` is tight).
Lower bound on the number of oracle calls of *any* such procedure: every configuration with
energy gap below `(1−κ) c_min − ε` must be evaluated (`anchor_card_lower_bound`), where `κ` is
the residual's true variation relative to the published constants — so tightening `c` is worth
exactly as much as it shrinks that shell.

### 6.3 Certified partition functions

```
ZCERT(model, beta, D):
  for each site state (basin, voxel v): enclose the one-body energy on v → [e_lo, e_hi];
      volume bounds [vol_lo, vol_hi] from the density 2/(1+t²)
      w⁻ ← vol_lo · expLo(−β e_hi),   w⁺ ← vol_hi · expHi(−β e_lo)
  for each pair of states: enclose the pair energy on v × v' → W⁻, W⁺ likewise
  certificate for I⁻ and for I⁺ (same tree shape usually works):
      thermal DEE: prune r against t when the certified ratio ρ = q₀ ∏ q_j is small
          (budget: Σ ln(1 + ρ_k) ≤ ε_prune)
      branch on sites with the widest pair-factor ranges
      factorised leaf when ∏ hi_ij / ∏ lo_ij ≤ 1 + ε_leaf
  return [lo(I⁻), hi(I⁺)]
```

Guarantee: `lo(I⁻) ≤ ∫ e^{−βE} ≤ hi(I⁺)` (`certified_voxel_partition`).  Unlike the
minimised-voxel surrogate of `K*`-type algorithms the bound contains the voxel volumes, i.e. the
conformational entropy inside each voxel.  Refining voxels tightens `[e_lo, e_hi]`; the
second-order envelope of the theory report (§3.4, paper-level) reduces the voxel count from
`ε^{-d}`-type to `ε^{-d/2}`-type scaling and factorises into one-dimensional integrals.

For exact tree-structured references use transfer matrices instead of branching: the kernel's
`leaf` with `lo = hi = W` is exact on a fully fixed box, and a chain can be summed by `n` matrix
products outside the kernel; a tree-elimination rule is a natural extension of the certificate
algebra (not yet in the verified kernel).

### 6.4 Free energies with a residual

Given the reference ensemble `μ₀ ∝ e^{−βE₀}` (tree-structured: exact marginals by dynamic
programming):

```
ln Z ∈ [ ln Z₀ − β⟨Δ⟩₀ ,  ln Z₀ − β⟨Δ⟩₀ + Σ_i ℓ(β c_i) ]       (product reference; ℓ ≤ t²/8)
```

with `ℓ(t) = (t − ln t − 1) + t/(e^t − 1) + ln(1 − e^{−t})` (Rio's function; the verified
statement has `β² Σ c_i²/8`).  `⟨Δ⟩₀` must itself be enclosed: exactly (enumeration of a small
cell), by anchors (`L ≤ Δ ≤ U` gives `⟨L⟩₀ ≤ ⟨Δ⟩₀ ≤ ⟨U⟩₀`, both computable by the transfer matrix
because `L, U` with one anchor are additive), or statistically (then the certificate is
probabilistic and outside the verified kernel).  Use the sandwich cell by cell inside the
partition-function branch-and-bound: within a cell the relevant constants are the cell-local
oscillations, and the gap is second order in the cell size.

### 6.5 Multi-state comparison

To certify `Z^{(0)} > max_k Z^{(k)}` keep an interval per state and refine the state whose
interval overlaps the leader's lower end most; stop when intervals separate.  Each interval is a
`partition` certificate; the comparison itself needs no further proof object.

---

## 7. Envelope-exporting equivariant residuals

A learned residual is admissible in this framework only if it ships with an envelope.

**Interface.**  `Δ_θ : configurations → ℝ` together with
(1) per-site constants `c_i` (or tables `δ_i(a,b)`, closed) valid on the declared domain, and
(2) an evaluation oracle used for anchors.

**Invariance.**  Build `Δ_θ` from SE(3)-invariant inputs — relative frames
`T_ij = T_i^{-1} T_j`, or distances plus signed volumes (pseudoscalars are required for
chirality; distances alone are reflection-invariant).  Invariance is by construction, so the
envelope can be stated on the quotient by rigid motions.

**From a Lipschitz certificate to an envelope.**  If `Δ_θ` is SE(3)-invariant and
`Λ`-Lipschitz in Cartesian coordinates (Frobenius norm; obtained by spectral normalisation or
certified bound propagation), then for all conformations

    |Δ_θ(X) − Δ_θ(Y)|  ≤  Λ · min_g ‖X − gY‖_F ,

because the residual does not change under `g`.  The superposition distance is a pseudo-metric,
hence an envelope.  For a torsion move it is bounded by the reduced-inertia chain rule (theory
report, Theorem 4.6): changing torsion `k` by `δ` costs at most `2√(2 I_red,k) |sin(δ/2)|`, so

    c_k  =  Λ · 2 √(Ī_k) ,      Ī_k ≥ min(I_A, I_B) on the domain      (≤ Λ · 2 √(2 I_red))

is a valid bounded-difference constant for torsion `k` (`residual_torsion_move`,
`IsTorsionMove.rigidWithin_min`; use `Ī_k = min(N_A, N_B)·ρ_max²` with `ρ_max` a bound on lever
arms if nothing better is known).  Voxel-level constants follow by
replacing `|sin(δ/2)|` with its maximum over the pair of voxels.

**From bound propagation to an envelope.**  Alternatively run interval or linear bound
propagation through the network with site `i` ranging over its domain and the other sites over
theirs, obtaining `δ_i(a,b)` directly; close the tables; export `c_i = max_{a,b} δ_i(a,b)`.

**What to optimise in training** (follows from Theorems 2.7 and 3.1): the certified constants
`c_i` — not merely the fit.  Halving `c_i` (i) shrinks the free-energy uncertainty by 4,
(ii) shrinks the energy shell that any optimality certificate must evaluate, (iii) enlarges the
set pruned by differential DEE.  Steep physical terms (sterics, electrostatics) belong in the
explicit part `E₀`.

---

## 8. Geometry certificates

### 8.1 Non-realizability of predicted squared distances in `ℝ³`

Input: hollow symmetric `D̂` (rational).  `Ĝ = −½ J D̂ J`, eigenvalues `λ_1 ≥ … ≥ λ_L`,
`T₂ = Σ_{k>3} λ_k²`, `τ = Σ_{k>3} λ_k`.  Then every configuration `Y` of `L` points in `ℝ³` has

    ‖D̂ − Δ(Y)‖_F²  ≥  4 T₂ + τ²             (`sstress_lower_bound`, r = 3).

The inequality is due to Sonthalia, Van Buskirk, Raichel and Gilbert (NeurIPS 2021); their
Algorithm 2 computes the sign-constrained relaxation exactly in `O(L³)` and is at least as strong
— use it on the producer side and the closed form above as the checker-side certificate.  The
bound is not tight in general (unit simplex, `L = 5`: bound `1.25`, optimum `≈ 1.304`).

Checker-side numerics: the theorem is about exact eigenvalues.  Use verified eigenvalue
enclosures `[λ_k⁻, λ_k⁺]` (e.g. Gershgorin discs of `Q^{-1} Ĝ Q` for an approximate eigenbasis
`Q`, in rational or interval arithmetic) and evaluate the right-hand side by interval arithmetic:
`T₂ ≥ Σ_{k>3} dist(0, [λ_k⁻, λ_k⁺])²` and `τ ∈ tr Ĝ − Σ_{k≤3} [λ_k⁻, λ_k⁺]` (the trace is an exact
rational).  The enclosure step is standard verified numerics and is **not** part of the Lean
development.  Interpretation: `4T₂` detects genuinely higher-dimensional or indefinite structure;
`τ²` detects additive-constant and scale bias and dominates by a factor `Θ(√L)` in that regime.
Conformance example (exact, verified): the unit simplex on `L` points gives `L(L−4)/4`.

### 8.2 Frame-graph screening by holonomy

For every cycle of a cycle basis with measured relative transforms `(R̂_k, t̂_k)`:
`θ_hol = angle(R̂_0 ⋯ R̂_{m−1})` lower-bounds the sum of rotational edge errors (and
`θ_hol²/m` the sum of their squares); `t_hol = Σ_k R̂_0⋯R̂_{k−1} t̂_k` satisfies
`‖t_hol‖ ≤ Σ_k ε_k + Σ_k (Σ_{l<k} ρ_l)‖t̂_k‖` for the translational errors `ε_k` and rotational
errors `ρ_l` (operator norm) of any consistent frame assignment (`Holonomy.lean`).  A cycle
whose holonomy exceeds what the claimed per-edge accuracies allow refutes those claims.

### 8.3 From torsion certificates to RMSD

Given per-torsion error bounds `|δ_k| ≤ ε_k` and inertia bounds `Ī_k ≥ min(I_A, I_B)_k` over
the path of intermediate conformations (`I_A, I_B`: moments of inertia of the two sides about
bond `k`): `RMSD ≤ N^{-1/2} Σ_k 2√(Ī_k) sin(min(ε_k, π)/2)` (`rigidWithin_torsion_chain`,
`IsTorsionMove.rigidWithin_min`).  Per move the exact coaxial cost is
`2S − 2√(S² − 4 I_A I_B sin²(δ/2))`, between `4 I_red sin²` and `4 min(I_A,I_B) sin²`.
Worst-case (`ℓ¹`); for independent errors expect `√m` slack.

### 8.4 Distance error versus RMSD

`dRMSD ≤ √2·RMSD`; and `RMSD_{with reflections} ≤ ‖Δ(X) − Δ(Y)‖_F / (√(8(√2−1)) · √L · σ₃(X))`
(harness-verified; cited, not formalized).  Frame-aligned errors: `RMSD ≤ min_i (L^{-1}Σ_j P_ij²)^{1/2}`.

---

## 9. Limits and impossibility boundaries (do not try to engineer around these)

| boundary | statement | source |
|---|---|---|
| gauge optimisation cannot help pairwise DEE | the Goldstein value is the exact margin and gauge invariant | `goldstein_isLeast`, `goldstein_gauge_invariant` |
| global bounds on the residual | exactly the energy window can be optimal; nothing inside it may be pruned | `energy_window_exact` |
| envelope + anchors | the certified interval for `min(E₀+Δ)` and `Z` is exactly `[E₀+L, E₀+U]`; no tighter certificate exists | `robust_min_bracket`, `robust_partition_bracket` |
| residual evaluations | at least the number of states with gap `< (1−κ)σ − ε` | `anchor_card_lower_bound` |
| pure dual certificates | incomplete: the frustrated triangle has LP bound 0, optimum 1 | `triangle_no_leaf_certificate` |
| certificates without `sum` | exactly `2^m` leaves on `m` independent frustrated triangles; `2m` with `sum` | `sumFree_exponential`, `sumFree_tight`, `sum_linear` |
| free-energy sandwich | constant `1/8` is optimal; the worst residual is additive two-level; gap is extensive | `mcdiarmid_no_better_constant`, `exists_two_level_worst_residual` |
| exact dominance with 3-body terms | coNP-hard in general; polynomial when the link graph of the site has bounded treewidth (chain-local terms) | theory report §2.2 (paper) |
| voxel quadrature | `Θ((βΔM/ε)^{d/2})` voxels with second-order information; rate not improvable | theory report §3.4 (paper + cited) |
| distances only | blind to chirality | §4.2 of the theory report |

---

## 10. Task mapping

| task | objects | certificate | guarantee |
|---|---|---|---|
| fixed-sequence conformational optimisation (rigid or voxelised) | `PairInstance` (lower instance) | `min` | `L ≤ min E`, gap to witness |
| …with a learned / many-body correction | `RProblem` | `residual` | `L ≤ min (E₀+Δ)` for every admissible `Δ`; gap to best anchor |
| partition function of one state | `WInstance` pair | `partition` ×2 | `lo ≤ Z ≤ hi` (continuous integral via voxels) |
| free-energy difference between macrostates | intervals per state | `partition` per state | interval for `ΔF`; sign certified when intervals separate |
| free energy with a residual | reference marginals + `c` | sandwich (§6.4) | `ln Z` interval of width `Σℓ(βc_i)` |
| screening predicted distance matrices | `D̂` | spectral bound (§8.1) | lower bound on 3-D realization error |
| screening predicted relative frames | cycle basis | holonomy (§8.2) | lower bound on synchronisation error |
| torsion-accuracy → global accuracy | torsion error bounds | reduced inertia (§8.3) | upper bound on RMSD |

---

## 11. Conformance tests

A re-implemented checker must reproduce the following kernel-evaluated facts
(`proofs/CertificateAlgebra.lean`, `proofs/Frontiers/PartitionCertificate.lean`):

1. **Triangle, optimum.**  `n=3, k=2`, `h=0`, `J[i][j][a][b] = 1` if `i<j` and `a=b`.
   Certificate: branch on site 0; for child `a` a leaf with `u = (0,1,0)`, `p = 0`,
   `m[1,0][s] = [s=a]`, `m[2,0][s] = [s=a]`, `m[1,2][s] = [s≠a]`, `m[2,1][s] = −[s=a]`.
   Accept for `L = 1`; reject for `L = 2`.  Witness `(0,1,0)` has energy 1.
2. **Biased triangle, DEE.**  As above with `h[0][0] = 3`.  Certificate: prune site 0 state 0
   by dominator 1 with `ℓ = (−1,−1,−1)`, then the leaf of test 1 with `a = 1`.  Accept for `L = 1`.
3. **Triangle with residual.**  `c = (1/4,1/4,1/4)`, anchor `x = (0,1,0)` with value `−1/8`.
   Certificate: anchor 0 + exhaustive certificate of the anchored instance.  Accept for
   `L = 1/8`; certified interval for the true optimum `[1/8, 7/8]`.
4. **Triangle, partition function.**  `w = 1`, `W[i][j][a][b] = 1/2` if `i<j` and `a=b`, else 1.
   Exhaustive certificate returns exactly `[13/4, 13/4]`; the single leaf with `lo = 1/2` on
   `i<j`, `hi = 1` returns `[1, 8]`.
5. **Rounding.**  `roundDown_4(1/3) = 5/16`; `2.7182 ≤ exp(1) ≤ 2.7183` from `expLo/expHi`.
6. **Realizability.**  Unit simplex on 5 points in `ℝ³`: bound `5·(5−4)/4 = 5/4`
   (`simplex_sstress_lower_bound`; a lower bound only — the optimum is ≈ 1.304).
7. **Torsion move.**  One static and one moving unit-mass atom at distance 1 from the axis,
   `φ = π`: `I_A = I_B = 1`, exact coaxial cost `2S − 2√(S² − 4) = 4 = 4·min(I_A,I_B)`.

Synthetic stress tests and tightness benchmarks: `experiments/falsify_conjectures.py`
(counterexample search for every theorem) and `experiments/separation_benchmarks.py`
(B1–B7; numbers quoted in the theory report).
