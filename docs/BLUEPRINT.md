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
* A reference checker exists as Lean definitions with soundness theorems: `verify` for
  minimisation, `verifyITop` for residual problems (interval anchor data; `verifyRTop` and
  `verifyRLowerTop` are its special cases for exact and for lower-only values), `zverifyTop` for
  partition sums.  The `…Top` entry points check the side conditions of the soundness theorems
  themselves (consistency of the residual data, nonnegative factors) before running the rule
  checkers `verifyR`, `zverify`; a re-implementation must do the same and must agree with the
  Lean kernels on the conformance vectors of §11.
* **Well-formedness is part of the check.**  In Lean, sites and states are elements of `Fin n`
  and `Fin k`, so an out-of-range index cannot be written down.  A file format can express one;
  a checker must therefore reject any file in which a site index is outside `[0, n)`, a state is
  outside `[0, k)` (in domains, anchors, witnesses or certificate nodes), a table has the wrong
  shape, or a domain repeats a state — *before* interpreting it (`validate` in the reference
  checker; conformance vectors `residual_bad_anchor_reject`, `partition_bad_domain_reject`).
* **The file format is strict, so that a file has one reading.**  A rational is a JSON integer or
  a string `-?digits` or `-?digits/digits` in canonical ASCII form (no `+`, spaces, leading
  zeros, decimals or exponents; nonzero denominator).  Table keys are `"i,j"` and `"j"` with
  canonical naturals.  Unknown fields and duplicate keys are errors (a duplicate would silently
  shadow a table; an unknown field may be a misspelt or obsolete one whose intent would be
  ignored — vector `residual_unknown_field_reject`).  A checker must never crash on a file: every
  malformed, ambiguous or over-sized input is a *rejection*, and the command-line status is
  zero only for an accepted certificate.
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
| anchors | interval evaluations `(x, lo, hi)`: `lo ≤ Δ(x) ≤ hi`, the upper value optional; an exactly known value is `lo = hi`, a floating-point evaluation is `[fl − err, fl + err]` | `IProblem.anchors`, `IAnchor`, `ResidualIntervalClass` |
| consistency | `c ≥ 0` and `lo_p − hi_q ≤ Σ_i c[i]·[x_p,i ≠ x_q,i]` for all ordered pairs of anchors of which the second has an upper value — equivalent to the existence of a residual with these data | `IProblem.Consistent`, `IProblem.consistent_iff_nonempty` |
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
| envelope constant `c[i]` of a residual | certified bound, rounded up | up |
| anchor lower value `lo` | `roundDown_p(fl(Δ(x)) − err)` | down |
| anchor upper value `hi` | `roundUp_p(fl(Δ(x)) + err)` | up |
| anchor `value` (shorthand for `lo = hi`) | the exact rational value of the residual — only for residuals that are exactly rational, e.g. table-based many-body terms; never for floating-point evaluations | — |
| dual variables (messages `m`) | any rounding (nearest dyadic) | soundness does not depend on them |
| claimed bounds `u, p, ℓ` (tropical) and `lo` (partition) | recomputed **in exact rational arithmetic** from the rounded duals and the published tables, or float value minus accumulated error, rounded down | down |
| claimed bounds `hi`, ratios `q₀, q_j` (partition) | exact recomputation, or float plus error, rounded up | up |

`err(e)` is a rigorous bound on the floating-point evaluation error of the table entry (interval
arithmetic or a running error bound).  Soundness of the protocol for real-valued energies is
`verify_sound_real` / `verifyR_sound_real` (lower instance ⇒ bound on the true energy) and
`Z_encloses_partitionFn` (lower/upper weight instances ⇒ enclosure of the true partition
function); the weight instances themselves are the computable functions
`WInstance.lowerOfIntervals` / `WInstance.upperOfIntervals` of the interval energy tables, and
`certified_partition_of_intervals` is the end-to-end statement (interval tables + two accepted
certificates ⇒ rational enclosure of the real partition function).  Because the checker re-verifies every inequality exactly,
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

`"instance": {"h":…, "J":…, "c": [q × n], "anchors": [A, …]}` where each anchor `A` is either
`{"x": [...], "lo": q, "hi": q}` (interval evaluation; `"hi"` may be omitted) or
`{"x": [...], "value": q}` (shorthand for `lo = hi = value`).  There is no default reading of a
bare number: a producer that evaluates the residual in floating point must publish `lo` and
`hi`.

File-level check, performed before any node is examined (`verifyITop`):

    c[i] ≥ 0 for all i,   and   lo_p − hi_q ≤ Σ_i c[i]·[x_p,i ≠ x_q,i]
    for every ordered pair of anchors (p, q) such that q has an upper value (p = q included).

This is exactly the condition that some residual with bounded differences `c` takes a value in
every published interval (`IProblem.consistent_iff_nonempty`).  A legitimate producer always
passes it — the true residual is a witness — whereas incompatible evaluations are rejected even
when they have been rounded (conformance vector `residual_interval_inconsistent_reject`).
Without the check every claim about inconsistent data would be vacuous: the rule checker alone
accepts `L = 41/4` on the vector `residual_inconsistent_reject`, whose pairwise minimum is `1`.

Consequences of acceptance (`verifyITop_sound`): for every residual `g` with bounded differences
`c` and `lo_p ≤ g(x_p) ≤ hi_p` at the anchors, `L ≤ E(x) + g(x)` on the box; and for every anchor
inside the box that has an upper value, `E(x_p) + hi_p` is an upper bound on the optimum, so the
optimum lies in `[L, min_p (E(x_p) + hi_p)]`.  Anchors without an upper value contribute to the
lower bound only; if *no* anchor has one, only `c ≥ 0` can be checked and no upper bound is
reported (vector `residual_lower_only`) — avoid this unless upper evaluations are unavailable.

| node | fields | check | Lean |
|---|---|---|---|
| `anchor` | `index`, `cert` (a `min` node) | check `cert` against the *anchored* instance `h'_i(s) = h_i(s) − c_i·[s ≠ x^a_i]`, `J' = J`, with bound `L − value_a` | `PairInstance.anchored`, `residual_ge_anchor` |
| `branch` | as above | as above | `verifyR` |
| `prune` | as above | as above with margin `c_i` instead of `0` (differential DEE) | `PruneOK … (P.c i)` |

The nodes are checked against the *lower* values `lo_a` (written `value_a` in the table):
accepted ⇒ for **every** residual `g` with single-site variation `≤ c_i` and `g(x^a) ≥ lo_a`,
`L ≤ E(x) + g(x)` on the box (`verifyR_sound_lower`).

### 4.3 `kind = "partition"` — two-sided bound on a partition sum (`ZCert`, `zverify`)

`"instance": {"w": [[q]], "W": {...}}` with all entries `≥ 0` — a file-level check: an instance
with a negative factor is rejected whatever the certificate (`zverifyTop`; without the check the
rule checker can return an interval that misses `Z`, `negativeW_unguarded`).  The checker
*returns* an interval `[lo, hi]`; `"claim": {"lo": q, "hi": q}` must contain it.

| node | fields | returns | Lean |
|---|---|---|---|
| `leaf` | `lo{i,j}`, `hi{i,j}` | check `0 ≤ lo_ij ≤ W_ij(a,b) ≤ hi_ij` on `D`; return `S·∏ lo`, `S·∏ hi`, `S = ∏_i Σ_{a∈D_i} w_i(a)` | `LeafZOK`, `zleaf_sound` |
| `branch` | `site`, `children` | sum of the children's intervals over the *distinct* states of `D_site` | `Z_branch`, `foldr_addIv_sound` |
| `prune` | `site i`, `remove r`, `dominator t`, `q0`, `q{j}`, `rest` | check `t∈D_i`, `t≠r`, `q0 ≥ 0`, `w_i(r) ≤ q0·w_i(t)`, `q_j ≥ 0`, `∀s∈D_j: W_ij(r,s)W_ji(s,r) ≤ q_j·W_ij(t,s)W_ji(s,t)`; with `[lo', hi']` from `rest` on `D∖r` return `[lo', (1 + q0 ∏_j q_j)·hi']` | `PruneZOK`, `zprune_sound` |

Accepted ⇒ `lo ≤ Z(D) ≤ hi` exactly (`zverifyTop_sound`).  To bound a *real* partition function,
publish two weight instances `I⁻ ≤ true factors ≤ I⁺` and two certificates; then
`lo(I⁻) ≤ Z_true ≤ hi(I⁺)` (`Z_encloses_partitionFn`; for continuous integrals over product
voxels `certified_torsion_partition`, §6.3).

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

`verifyR` and `zverify` have the same shape (§4.2, §4.3); their top-level wrappers first perform
the file-level checks of §4.2 / §4.3.

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
Lower bound on the number of oracle calls of a procedure of *this form* (incumbent = best
evaluated anchor, bound = McShane lower envelope): every configuration with energy gap below
`(1−κ) c_min − ε` must be evaluated (`anchor_card_lower_bound`), where `κ` is the residual's true
variation relative to the published constants.  This is not a bound for arbitrary certificates —
a candidate that is separated from a state by the white-box part alone needs no evaluation there
(theory report §2.4, correction) — and it is only the first layer of the covering bound: the
exact statement is that the evaluated set must *cover* every configuration `y` within slack
radius `gap(y) + ε` (theory report §11.2), which gives the a-priori estimates of §6.6 below.

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

Guarantee: `lo(I⁻) ≤ ∫ e^{−βE} ≤ hi(I⁺)`, the integral being over the union of the product
voxels of the box with respect to the product of the per-torsion measures
(`certified_torsion_partition_top`: its hypotheses are exactly the entrywise inequalities
produced above — table enclosures of the one-body and pair energies on the cells of the box,
cell measures, and outward-rounded Boltzmann factors — plus measurability; nonnegativity of the
factors is checked by the kernel `zverifyTop`, and cells removed from the domains need no energy
enclosure).
Cells of one site must be pairwise disjoint (half-open intervals in the chart coordinate).  For
a cell `[t₁, t₂)` of a rational chart the angular measure is `2(arctan t₂ − arctan t₁)`; use the
rational enclosure `(t₂−t₁)·2/(1+T²) ≤ vol ≤ 2(t₂−t₁)`, `T ≥ max(|t₁|,|t₂|)`
(`two_arctan_sub_bounds`, `chartArc_onebody_brackets`).  The upper bound `2(t₂−t₁)` does **not**
tighten when a cell is subdivided (it overestimates by up to the factor `1 + T²`); for cells on
one side of the chart origin use `(t₂−t₁)·2/(1+t₂²) ≤ vol ≤ (t₂−t₁)·2/(1+t₁²)` (for
`0 ≤ t₁ ≤ t₂`; mirrored for `t₁ ≤ t₂ ≤ 0`), whose relative width `(1+t₂²)/(1+t₁²)` tends to `1`
(`chartArc_onebody_brackets_pos`, `chartArc_onebody_brackets_neg`) — so split every chart at
`t = 0`.  Only the base chart is formalized; cells of the rotated charts are translates by
multiples of `π/2` and have the same measures.  Unlike the minimised-voxel
surrogate of `K*`-type algorithms the bound contains the voxel volumes, i.e. the conformational
entropy inside each voxel.  Refining voxels tightens `[e_lo, e_hi]`.

**Second-order voxels.**  If the producer has separable envelopes
`Σ_i φ_i(θ_i) ≤ E(θ) ≤ Σ_i ψ_i(θ_i)` on a product voxel (from a Taylor expansion with a diagonal
Hessian enclosure: `φ_i(t) = E(c)/M + g_i (t−c_i) + (m/2)(t−c_i)²`, `ψ_i` with `M` in place of
`m`), then `∏_i ∫ e^{−βψ_i} ≤ ∫_voxel e^{−βE} ≤ ∏_i ∫ e^{−βφ_i}` (`separable_voxel_bounds`), with
relative width `≤ exp(β Σ_i (M−m) h_i²/2)` (`separable_voxel_ratio`).  Each one-dimensional
integral is enclosed by a 1-D voxel sum with certified `exp` bounds, so the cost is
`M × (1-D resolution)` per voxel, and the voxel count for accuracy `1+ε` drops from `ε^{-d}`-type
to `ε^{-d/2}`-type scaling (with a dimension-dependent factor `d^{d/2}`; this is the rate of the
scalar-sandwich scheme, not an optimal rate — theory report §3.4).  The Hessian enclosure itself (interval arithmetic on second
derivatives) is the producer's obligation and is not covered by the Lean development.

**Decomposition rules (Lean kernel `zverify2`, `proofs/Frontiers/PartitionProduct.lean`).**  With
leaf / branch / thermal prune alone an exact enclosure needs full enumeration (`2ⁿ` leaves for a
two-state chain; theory report §3.4, limitation).  The extended certificate type `ZCert2` adds:

* `cut S p lo hi c₁ c₂` — split the sites into `S` and its complement; the checker verifies
  `0 ≤ lo_ij ≤ W_ij ≤ hi_ij` on the box for every ordered pair across the cut and returns
  `[Λ·l₁·l₂, Υ·h₁·h₂]` from the certificates of the two restricted instances
  (`Λ = ∏ lo`, `Υ = ∏ hi`).  Exact when the two parts do not interact.  Use it whenever the
  interaction graph (restricted to the current box) splits, or nearly splits.
* `elim1 i j p rest`, `elim2 i j l p rest` — sum out a site `i` that interacts only with `j`
  (resp. `j` and `l`) into a one-body factor of `j` (resp. a pair factor between `j` and `l`);
  exact.  A chain is certified by `n − 1` eliminations and one leaf — the transfer-matrix
  computation as a certificate (`chainCert`, `zverify2Top_chainCert`, machine-checked for every
  chain); trees, cycles and every interaction graph of treewidth at most two reduce in the same
  way (always eliminate a site of degree at most two) — machine-checked on the tree and ring
  instances evaluated by the kernel, a paper argument in general.

Producer order: eliminate while some site has at most two neighbours on the current box; cut
when the graph splits; branch (conditioning) to create sites of low degree; prune thermally; a
factorised leaf at the end.  The JSON format `metricchain-cert/1` and the reference checker do
not carry `cut`/`elim` nodes yet; the conformance vectors of §11 are unchanged.

### 6.4 Free energies with a residual

The width of the interval depends on the reference ensemble `μ₀`:

```
product reference  μ₀ = ⊗_i μ_i  (independent sites; e.g. one-body / mean-field reference):
    ln Z ∈ [ ln Z₀ − β⟨Δ⟩₀ ,  ln Z₀ − β⟨Δ⟩₀ + β² Σ_i c_i² / 8 ]        verified
    … with Σ_i ℓ(β c_i) ≤ β² Σ_i c_i²/8 in place of the last term       cited (Rio 2013), not verified
arbitrary reference  (e.g. μ₀ ∝ e^{−βE₀} with pairwise or tree-structured E₀):
    ln Z ∈ [ ln Z₀ − β⟨Δ⟩₀ ,  ln Z₀ − β⟨Δ⟩₀ + β² (Σ_i c_i)² / 8 ]      verified (Hoeffding, range ≤ Σ c_i)
```

(Lean: `bounded_differences_sandwich`, `bounded_differences_sandwich_any_reference`.)

with `ℓ(t) = (t − ln t − 1) + t/(e^t − 1) + ln(1 − e^{−t})` (Rio's function).  **Do not use the
`Σ c_i²` width with a correlated reference**: it is false there (two perfectly correlated sites,
`c = (1,1)`, `β = 1`: gap `0.434 > 0.25`; `correlated_reference_counterexample`, `DEAD_ENDS.md`
D14).  Intermediate widths for weakly
dependent references (`‖Γc‖²` with a Wasserstein/Dobrushin matrix `Γ`) are in the literature
(Kontorovich–Ramanan 2008) and are not part of the verified development.  `⟨Δ⟩₀` must itself be enclosed: exactly (enumeration of a small
cell), by anchors (`L ≤ Δ ≤ U` gives `⟨L⟩₀ ≤ ⟨Δ⟩₀ ≤ ⟨U⟩₀`, both computable by the transfer matrix
because `L, U` with one anchor are additive), or statistically (then the certificate is
probabilistic and outside the verified kernel).  Use the sandwich cell by cell inside the
partition-function branch-and-bound: within a cell the relevant constants are the cell-local
oscillations, and the gap is second order in the cell size.

### 6.5 Multi-state comparison

To certify `Z^{(0)} > max_k Z^{(k)}` keep an interval per state and refine the state whose
interval overlaps the leader's lower end most; stop when intervals separate.  Each interval is a
`partition` certificate; the comparison itself needs no further proof object.

### 6.6 What a residual certificate will cost, and the second-order alternative

The loop of §6.2 is the right loop for a first-order envelope, but theory report §11 shows that
its cost is dictated by the instance, not by the implementation.  Decide **before** running it.

**Step 1 — is the incumbent sharp?**  For a candidate `x̂` test the sharp-minimum condition
`d(x̂, y) ≤ E₀(y) − E₀(x̂) + ε` for all `y`, i.e. `min_y [E₀(y) − d(x̂,y)] ≥ E₀(x̂) − ε`: one
`min` certificate for the pairwise model `E₀ − Σ_i δ_i(x̂_i, ·)`.  If it holds, `x̂` is ε-optimal
for every admissible residual with **no** evaluation (`robust_certified_iff`), and the single
evaluation at `x̂` is a point certificate (`single_evaluation_certificate_iff`).  With evaluations
already made, the test is the same with the conditional envelope
(`robust_certified_with_anchors_iff`).

**Step 2 — if not, estimate the price.**  For every `t ≥ 0` any ε-certificate has

    #evaluations  ≥  e^{−tε} · Σ_y e^{−t·gap(y)} / ∏_i (1 + (k_i − 1) e^{−t(1−κ)c_i})

(`partition_bound_hamming`).  The numerator is a partition function of the landscape at inverse
temperature `t`; for planning, bound `gap(y) ≤ E₀(y) − E₀(x̂) + κ·d(y, x̂) + (UB − LB)` and compute
`e^{−t(UB−LB)} Σ_y e^{−t(E₀(y) − E₀(x̂) + κ d(y,x̂))}` — a pairwise partition function with shifted
one-body tables — by elimination (§6.3).  `κ` (the true variation of the residual relative to
the published constants) is a planning parameter, not something the kernel knows.  This is a
*lower bound* on the cost, valid for every algorithm (also randomised ones, with the factor
`1 − 2δ`: theory report §11.10).  On independent sites the exact exponent is
`max_t Σ_i max_v r_i(t; v)` (theory report Theorem 11.9): **one** slope `t` for all sites —
maximising site by site overshoots — and, for each site and `t`, the best weights `v` from a
small linear program; the Boltzmann weights used in the displayed bound are optimal only for
two-state sites with zero residual (`DEAD_ENDS.md` D31).  The count is one if every site is
sharp.  For free energies the corresponding deterministic floor is
`exp(H(π) − tε/β) / ∏_i (1 + (k_i−1) e^{−t(1−κ)c_i})` (`card_ge_entropy`): at least the
exponential of the entropy.  If the estimate is beyond budget, do **not** run §6.2; change the
information:

* *linear information* — a reference average of the residual and the sandwich of §6.4;
* *structure* — a second-order envelope with weak coupling (below);
* *accuracy* — an extensive tolerance;
* *a probabilistic guarantee* — Steps 4 and 5; but note the floor: randomisation does not help
  at every accuracy.  On the uniform cube class, below `n ln cosh(βc/2)` every randomised
  procedure is exponential in the worst case, i.e. for the zero model (theory report
  Theorem 11.25); for a model `ĝ` at hand, compute the single-site threshold of §6.6 Step 5.

**Step 3 — second-order envelopes.**  If the residual comes with certified bounds `c_ij` on its
mixed second differences, `n(k−1)+1` evaluations on the star of a reference configuration `x₀`
reduce the problem, without loss, to the pairwise kernel.  *Check the row-sum condition first*:
if `½ Σ_{j≠i} c_ij` is below the measured single-site excitation energies at every site, the
star at the minimiser certifies it.  With dense constants it does not, and no star-type data
will (the envelope's half-width grows with the square of the Hamming distance; theory report
§11.7, `DEAD_ENDS.md` D32) — the loop below then needs its fallback.

```
STARCERT(E0, residual oracle g, constants c_ij (symmetric, ≥ 0), eps):
  x0 ← best configuration known
  repeat
    evaluate g at x0 and at every single-site neighbour of x0         # 1 + Σ_i (k_i − 1) calls
    I⁻ ← pairwise instance:  h_i(s)    = E0.h_i(s) + [g(x0[i↦s]) − g(x0)]        (rounded down)
                             J_ij(a,b) = E0.J_ij(a,b) − (c_ij/2)·[a ≠ x0_i]·[b ≠ x0_j]
    (cert, L, y) ← MINCERT(I⁻)              # §6.1; y = minimiser found for I⁻
    if y = x0:  return (x0, cert)            # x0 is optimal for EVERY residual of the class
                                             # consistent with the star data
    evaluate g(y);  UB ← min(UB, E(y))
    if UB − (L + g(x0)) ≤ eps:  return (argmin, cert)
    x0' ← best evaluated configuration       # re-centre: the remainder grows like the number
                                             # of changed pairs, so stay near the incumbent
    if x0' = x0:                             # no progress: the same star would be evaluated again
        return FALLBACK                      # branch on a site (two smaller boxes, each with its
                                             # own star), or use first-order anchors (§6.2)
    x0 ← x0'
```

Without the fallback the loop does not terminate when the minimiser `y` of the lower model is
not better than `x0` and the gap exceeds `eps` (second referee, M3).

Guarantee: `L + g(x₀) ≤ E₀(x) + g(x)` for all `x` in the box (`verify_sound_secondOrder`); the
two pairwise models `E₀ + g_star ∓ Σ_{i<j changed} c_ij` are the exact lower and upper envelopes
of the class given the star data (`secondOrder_envelope_exact`), so no certificate using the
same evaluations can report a larger bound; the exit `y = x0` is exact
(`secondOrder_certified_minimizer_iff`).  After an evaluation at `y` the gap is at most twice
the pair remainder at `y`.  For partition functions use the same two pairwise models in the
weight domain (`Z(E₀ + g_star + R) ≤ Z ≤ Z(E₀ + g_star − R)`, both certified by §6.3).  The
constants `c_ij` are the producer's obligation; none are certified here for a concrete residual.

**Step 4 — a probabilistic guarantee instead (free energies).**  When a statement that holds
with probability `1 − δ` is acceptable, the free-energy difference between the target and a
*product* reference `μ₀` (e.g. the one-body part of `E₀`, whose `Z₀` is explicit) needs only
`N ≥ C ln(2/δ) / (2η²)` evaluations of the residual, `C = Σ_i c_i²`:

```
SAMPLED-SANDWICH(product reference p, residual oracle Δ, constants c_i, beta, eta, delta):
  N ← ceil( C · ln(2/delta) / (2 eta²) )
  the VERIFIER draws x⁽¹⁾ … x⁽ᴺ⁾ independently from p        # not the producer
  m̂ ← (1/N) Σ_k Δ(x⁽ᵏ⁾)                                     # N oracle calls
  return  ln(Z/Z₀) ∈ [ −β m̂ − |β| eta ,  −β m̂ + |β| eta + β² C / 8 ]
```

Guarantee: the interval contains `ln(Z/Z₀)` except on a set of sample tuples of probability at
most `δ` (`sampled_free_energy_sandwich_of_sample_size`).  Two cautions.  (i) The probability is
over the *sampler's* randomness: the statement is meaningless if the party that wants to
convince chooses the sample points, so the samples must be drawn by the verifier (or from a
committed seed); the verified kernels of this repository do not implement such a protocol.
(ii) The width `β²C/8` is extensive, as in §6.4; the statement is useful when `β c_i` is small or
after localisation.  For comparison, a deterministic certificate of the same accuracy from
pointwise evaluations needs exponentially many of them (theory report §11.6, §11.9).  The
guarantee presupposes exact sampling from `p`, exact evaluation of `Δ` and a known `Z₀`.

**Step 5 — spot-checking a claimed residual model (any functional).**  A producer may publish a
*model* `ĝ` of the residual (for instance the additive interpolant of a star, or a pairwise
fit) together with the value `Φ(E₀ + ĝ)` it implies.  The verifier draws `N` points from a
distribution `q` of its own choice, evaluates the residual there and compares:

```
SPOT-CHECK(model ĝ, residual oracle g, sampling distribution q, N, hedge η ∈ (0, ε)):
  the VERIFIER draws a⁽¹⁾ … a⁽ᴺ⁾ independently from q
  if g(a⁽ᵏ⁾) = ĝ(a⁽ᵏ⁾) for all k:  accept o = Φ(E₀ + ĝ) − ε/2 + η   (minimum)
                                           o = Φ(E₀ + ĝ) + ε/2 − η   (ln Z)
  else:                             reject (fall back to a deterministic procedure)
```

Guarantee (`hedgedSpotCheck_correct`): if every admissible residual whose value of `Φ` is
farther than `ε/2` from the accepted number `o` differs from `ĝ` on a set of `q`-probability at
least `p`, the accepted value is within `ε/2` except with probability `(1 − p)^N`.  The hedge
matters: without it (`o = Φ(E₀ + ĝ)`, `spotCheck_correct`) all alternatives at distance `ε/2` must
be detected, with it only those that move `Φ` by more than `ε − η` in the cheap direction or by
more than `η` in the other; the difference is a factor `e^{Θ(ε)}` in `N` for free energies and can
be unbounded for the minimum (`DEAD_ENDS.md` D36).  The work is in `p`.  For the minimum
(`min_hedgedSpotCheck_correct`), `p` is the least `q`-mass of the closed slack balls
`{a : s(a,y) ≤ gap(y) + ε − η}` and of the set of `η`-minimisers, all computable from `ĝ`
(harness XII.4, XII.7); no choice of `q` makes `N` smaller than `(1 − 2δ)` times the fractional
covering number (`expected_queries_ge`), so on non-sharp product landscapes spot-checking is
exponential too.  For free energies a
sampling distribution with a guarantee is available in closed form (`thermalSampler`,
`thermal_spotCheck_correct`): draw half of the samples from the Gibbs measure `π̂` of the model
and half with probability proportional to `π̂(z)·(e^{ε/2} e^{Λ(z)} − 1)`, where the soft gap
`Λ(z) = ln Z(E₀+ĝ) − ln Z(E₀ + ĝ(z) + d(·,z))` is a ratio of two partition functions of the
model (for a chain-structured `E₀` and an additive `ĝ`, two transfer-matrix computations per
`z`); then `N = ⌈2 ln(1/δ) E_π̂[e^{Λ}] / (1 − e^{−ε/2})⌉` samples suffice.  The number
`E_π̂[e^{Λ}]` is exponential in general — for the zero model on the cube `(2/(1+e^{−βc}))ⁿ`, still
exponentially smaller than the `2ⁿ` of every deterministic procedure there
(`cube_deterministic_lower_bound`).  This sampler is not optimal: for the zero model on the
cube uniform samples with the hedged output need only `2ⁿ/|B(k)|` of them, `k` the largest radius
whose dip changes `ln Z` by at most `ε − η` (theory report Theorem 11.25(c)), and for that model
no sampling distribution avoids an exponential number below the accuracy `n ln cosh(βc/2)`
(`cube_thermal_randomized_bound`, `cube_exact_dip_randomized`).  This is a statement about the
worst model, not about every model: `ĝ = c|x|` is determined by two evaluations.  For an
additive model, compute before sampling the single-site quantity
`γ(Q) = max_Φ [β E_Q Φ − Λ(Φ)]` (maximum over the vertices of the Lipschitz polytope of the
site): if the accuracy per site exceeds `min_Q γ(Q)`, a bounded number of samples from
`½π̂ + ½Q*ⁿ` suffices, whatever `n` (theory report Theorem 11.28; the tensorisation and the
hitting bound are machine-checked, `twoMeasureBound_pow`, `product_mass_ge`); below that
accuracy the cost is exponential in `n` (`genDip_expected_queries_ge`).  With no model at all,
for a class of identical sites: choose the reference law `Q*` that minimises the oscillation
`M(Q) − m(Q)` of the tilted site pressure `F_Q(ψ) = ln Σ_a e^{−β(f₁+ψ)} + βE_Qψ` over the admissible
site functions (a convex problem in one site), sample `Q*ⁿ`, and return the midpoint of
`[n m(Q*), n M(Q*)] − β·(sample mean of g)`; the accuracy `n(M − m)` is reached with a bounded
number of samples on every instance (`product_sandwich`), and no algorithm does better in the
worst case (Theorem 11.28(d)).  For two-state sites `Q*` is the Gibbs law tilted to the slope
at which the tangent of the pressure is parallel to its chord over `[−c, c]` (Theorem
11.28(e)).  Exact equality of values
is assumed; with numerical tolerances the comparison and the envelope must be widened
consistently.  No kernel for such transcripts is implemented here.

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

**From a Lipschitz certificate to an envelope.**  If `Δ_θ` is invariant under a group `G` of
rigid motions — `G = SE(3)` (proper motions) for chirality-sensitive residuals, or all of `E(3)`
— and `Λ`-Lipschitz in Cartesian coordinates (Frobenius norm; obtained by spectral normalisation
or certified bound propagation), then for all conformations

    |Δ_θ(X) − Δ_θ(Y)|  ≤  Λ · min_{g∈G} ‖X − gY‖_F ,

because the residual does not change under `g` (`invariant_lipschitz_of_rigidWithinIn`).  The
superposition distance is a pseudo-metric, hence an envelope.  For a torsion move the
superposition used in the proofs is a rotation about the torsion axis, so the reduced-inertia
bounds (theory report, Theorem 4.6) hold for every group `G` that contains those rotations.  The
verified statements are for such an abstract `G` (with a worked instance for a residual that is
not reflection-invariant, `signed_offset_residual_torsion_bound`); that the proper motions `SE(3)` form
such a group is immediate but `SE(3)` is not defined in the Lean development.  Consequently:
changing torsion `k` by `δ` costs at most `2√(min(I_A,I_B)) |sin(δ/2)| ≤ 2√(2 I_red,k) |sin(δ/2)|`,
so

    c_k  =  Λ · 2 √(Ī_k) ,      Ī_k ≥ min(I_A, I_B) for every conformation of the domain

is a valid bounded-difference constant for torsion `k` (`residual_torsion_move_min_in`; the
looser `Λ · 2√(2 Ī_k)` with `Ī_k ≥ I_red` is `residual_torsion_move_uniform`; use
`Ī_k = min(N_A, N_B)·ρ_max²` with `ρ_max` a bound on lever arms if nothing better is known).
Publishing constants `≥ c_k` (rounded up) and interval anchor data containing `Δ_θ` (lower
values rounded down, upper values rounded up) puts `Δ_θ` in the class for which the residual
kernel is sound (`residualIntervalClass_of_rigidWithinIn`, `verifyITop_sound_invariant`; a
worked instance is `interval_invariant_instance`).  Voxel-level constants follow
by replacing `|sin(δ/2)|` with its maximum over the pair of voxels.  The Lipschitz constant `Λ`
and the inertia bounds are the producer's obligations; they are hypotheses of the verified
statements, not conclusions.

**From bound propagation to an envelope.**  Alternatively run interval or linear bound
propagation through the network with site `i` ranging over its domain and the other sites over
theirs, obtaining `δ_i(a,b)` directly; close the tables; export `c_i = max_{a,b} δ_i(a,b)`.

**What to optimise in training** (follows from Theorems 2.7 and 3.1): the certified constants
`c_i` — not merely the fit.  Halving `c_i` (i) shrinks the free-energy uncertainty by 4,
(ii) shrinks the covering problem that an optimality certificate must solve (below the
sharp-minimum threshold `c_i ≤` single-site excitation energy one evaluation suffices; above it
the number of evaluations grows exponentially with the chain length, theory report §11.4),
(iii) enlarges the set pruned by differential DEE.  Steep physical terms (sterics, electrostatics) belong in the
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
with `σ₃(X)` the third singular value of the **centred** coordinate matrix (with an uncentred `X`
the inequality fails: a nearly planar molecule shifted along its normal gives RMSD `0.0348`
against a "bound" of `0.0076`; `reviews/R1`, item 10)
(harness-verified; cited, not formalized).  Frame-aligned errors: `RMSD ≤ min_i (L^{-1}Σ_j P_ij²)^{1/2}`.

---

## 9. Limits and impossibility boundaries (do not try to engineer around these)

| boundary | statement | source |
|---|---|---|
| gauge optimisation cannot help *single-site* pairwise DEE | the Goldstein value is the exact margin and gauge invariant; multi-site improving maps and bound-based pruning do depend on the gauge | `goldstein_isLeast`, `goldstein_gauge_invariant` |
| global bounds on the residual | exactly the energy window can be optimal; nothing inside it may be pruned | `energy_window_exact` |
| envelope + anchors | the set of possible values of `min(E₀+Δ)` and of `Z` is exactly the interval between the values at `E₀+L` and `E₀+U`; no tighter certificate exists | `robust_min_bracket`, `robust_partition_bracket`, `robust_min_interval_exact`, `robust_partition_interval_exact` |
| residual evaluations (incumbent = evaluated anchor) | at least the number of states with gap `< (1−κ)σ − ε`; in general the evaluated set must cover every `y` within slack radius `gap(y) + ε`, with LP-dual and rate–distortion lower bounds | `anchor_card_lower_bound`; `isCertificate_iff_cover`, `card_ge_of_weights`, `partition_bound` |
| first-order envelope + pointwise evaluations, independent sites | one evaluation if every site is sharp, otherwise exponentially many in the number of non-sharp sites (at least `(6/5)ⁿ` already for two-state sites with `c = 2e` and zero residual; machine-checked for identical sites with zero residual) | `product_single_certificate_iff`, `product_partition_bound`, `binary_certificate_exponential` |
| free-energy certificates from pointwise evaluations | at least `exp(entropy − tε/β)` divided by a slack-ball partition sum, even for sharp landscapes | `card_ge_entropy`, `thermal_exp_weights` |
| smallest certificate | NP-hard to find (contains minimum dominating set); best-first search is competitive only with covers at radii shrunk by `(1−κ)/(4(1+κ))` | `domCertificate_min_card`, `bestFirst_card_le`; `DEAD_ENDS.md` D26 |
| second-order envelope + star data | the pairwise sandwich is the exact envelope; nothing tighter exists with the same evaluations; its half-width is quadratic in the Hamming distance, so with dense constants even the whole radius-2 ball does not certify | `secondOrder_envelope_exact`; `DEAD_ENDS.md` D32 |
| partition kernel without decomposition rules | certificates with an *exact lower end* need one leaf per configuration on instances that are rigid *in the given representation* (`k^n` on chains, against one leaf with elimination); nothing is proved for approximate enclosures, and a gauge-trivial instance satisfies the hypothesis | `zverify2_elementary_exact_leaves`, `cut_rule_separation`, `chain_separation`, `ferroChain_separation`, `gauge_trivial_separation` |
| every algorithm that evaluates the residual, deterministic or randomised | the instance-wise deterministic cost equals the size of a value certificate; a randomised algorithm with error probability `δ` pays `(1 − 2δ)` times every fractional covering bound; for `ln Z` on the cube class, exponentially many evaluations at the zero residual below the accuracy `n ln cosh(βc/2)` (a worst-case statement), and `(1 − 2δ) 2ⁿ` for exact answers | `instance_query_complexity`, `expected_queries_ge_exp_weights_min`, `binary_randomized_exponential`, `thermal_expected_queries_ge`, `cube_thermal_randomized_bound`, `cube_exact_dip_randomized`, `cube_exact_randomized` |
| free energies on product landscapes beyond the cube | every slack-Lipschitz centre function gives a perturbation that must be detected; at an additive instance the cost is bounded above the single-site game value `min_Q max_Φ[βE_QΦ − Λ(Φ)]` per site and exponential below it; single dips underestimate both when sites have three or more states | `genDip_expected_queries_ge`, `twoMeasureBound_pow`, `product_mass_ge`; `DEAD_ENDS.md` D38 |
| pure dual certificates | incomplete: the frustrated triangle has LP bound 0, optimum 1 | `triangle_no_leaf_certificate` |
| certificates without `sum` | exactly `2^m` leaves on `m` independent frustrated triangles; `2m` with `sum`; the gap persists in total description length (at most `147 m³` against at least `2^m`, hence smaller for `m ≥ 21`) | `sumFree_exponential`, `sumFree_tight`, `sum_linear`, `sum_rule_separation_dataSize` |
| free-energy sandwich | product reference: constant `1/8` is optimal and the worst residual is additive two-level; the `Σ c_i²` width is false for correlated references; gap is extensive | `mcdiarmid_no_better_constant`, `exists_two_level_worst_residual`, `DEAD_ENDS.md` D14 |
| inconsistent residual data | every claim about them is vacuous; they must be rejected | `IProblem.consistent_iff_nonempty`, `inconsistentResidual_rejected`, `inconsistentInterval_rejected` |
| exact dominance with 3-body terms | factorises over blocks whenever the difference energy is block-separable (`exact_margin_of_block_separable`, verified in this abstract form); for 3-body terms the blocks are the connected components of the site's link graph (paper); cheap for chain-local terms; coNP-hard for unrestricted link graphs (paper) | theory report §2.2 |
| voxel quadrature | `O((βΔM·d/ε)^{d/2})` voxels with the scalar second-order sandwich; the exponent matches point-evaluation lower bounds for the class "only `mI ⪯ ∇²E ⪯ MI` known", but is not optimal for box-enclosure oracles on smoother energies | theory report §3.4 (paper + cited) |
| distances only | blind to chirality | §4.2 of the theory report |

---

## 10. Task mapping

| task | objects | certificate | guarantee |
|---|---|---|---|
| fixed-sequence conformational optimisation (rigid or voxelised) | `PairInstance` (lower instance) | `min` | `L ≤ min E`, gap to witness |
| …with a learned / many-body correction | `RProblem` | `residual` | `L ≤ min (E₀+Δ)` for every admissible `Δ`; gap to best anchor |
| partition function of one state | `WInstance` pair | `partition` ×2 | `lo ≤ Z ≤ hi` (continuous integral via voxels) |
| free-energy difference between macrostates | intervals per state | `partition` per state | interval for `ΔF`; sign certified when intervals separate |
| free energy with a residual | reference expectation + `c` | sandwich (§6.4) | `ln Z` interval of width `β²Σc_i²/8` (product reference) or `β²(Σc_i)²/8` (any reference) |
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
   `L = 1/8`; certified interval for the true optimum `[1/8, 7/8]`
   (`triangleResidual_verifiedTop`).
   3a. **Inconsistent exact values.**  Same `c`, anchors `(0,1,0) ↦ 0` and `(1,1,0) ↦ 10` given
   as `value` (Hamming distance 1, values differing by more than `1/4`); certificate: anchor 1 +
   exhaustive certificate, claim `L = 41/4`.  **Reject** (`inconsistentResidual_rejected`).
   3b. **Lower values only.**  The same two anchors given as `lo` without `hi`: **accept**
   `L = 41/4`, report no upper bound (`inconsistentResidual_lowerTop`, `verifyITop_ofLower`).
   3c. **Interval evaluation.**  Anchor `(0,1,0)` with `lo = −9/64`, `hi = −7/64`: accept
   `L = 7/64`, upper bound `57/64` (`triangleInterval_verified`).
   3d. **Rounded but incompatible intervals.**  `(0,1,0) ∈ [−1/64, 1/64]`,
   `(1,1,0) ∈ [639/64, 641/64]`: **reject** whatever the certificate
   (`inconsistentInterval_rejected`).
   3e. **Negative envelope constant.**  `c = (−10, 1/4, 1/4)`: reject whatever the certificate
   (`negativeEnvelope_rejected`).
   3f. **Malformed anchor.**  Anchor configuration `[7,7,7]` with `k = 2`: reject as malformed.
4. **Triangle, partition function.**  `w = 1`, `W[i][j][a][b] = 1/2` if `i<j` and `a=b`, else 1.
   Exhaustive certificate returns exactly `[13/4, 13/4]`; the single leaf with `lo = 1/2` on
   `i<j`, `hi = 1` returns `[1, 8]` (`triangleZ_exactTop`, `triangleZ_coarse`).
   4a. **Negative factor.**  `n = 2, k = 1`, `w = (−1, 1)`, `W = 2` on both ordered pairs: reject
   whatever the certificate (`negativeW_rejected`; the leaf `lo = 1, hi = 3` would otherwise
   return `(−1, −9)` although `Z = −4`).
   4b. **Malformed domain.**  `n = 1, k = 1`, domains `[[0, −1]]`: reject as malformed (a
   negative state would silently index from the end of a table in many languages).
5. **Rounding.**  `roundDown_4(1/3) = 5/16`; `2.7182 ≤ exp(1) ≤ 2.7183` from `expLo/expHi`.
6. **Realizability.**  Unit simplex on 5 points in `ℝ³`: bound `5·(5−4)/4 = 5/4`
   (`simplex_sstress_lower_bound`; a lower bound only — the optimum is ≈ 1.304).
7. **Torsion move.**  One static and one moving unit-mass atom at distance 1 from the axis,
   `φ = π`: `I_A = I_B = 1`, exact coaxial cost `2S − 2√(S² − 4) = 4 = 4·min(I_A,I_B)`.

**Reference implementation.**  `experiments/reference_checker.py` implements the three checkers
of §4–§5 on this JSON format in exact rational arithmetic (it is *not* trusted; the Lean kernels
are).  `--selftest` reproduces vectors 1–4b above — also stored as files in `experiments/certs/`,
together with two format vectors (`residual_unknown_field_reject`,
`min_noncanonical_rational_reject`) — runs 53 malformed, ambiguous or hostile inputs that must be
rejected without an exception (alias keys, non-canonical numbers, duplicate keys, wrong types,
30000-fold nesting), and fuzzes random, mostly invalid certificates against brute force: an accepted certificate must
never claim a bound above the true minimum (also with rounded-down anchor values), nor an
interval missing the true partition sum; interval anchors around the true values must be judged
consistent and corrupted ones inconsistent.

**Is the test suite itself any good?**  `experiments/mutation_tests.py` applies 104 small
mutations to a scratch copy of the falsification harness — each makes a tested claim false or
breaks the test's model of it — and requires every one to be caught (output stored in
`docs/mutation_output.txt`).  The audit script runs it, and starts with a self-test in which
planted violations (an incomplete proof, forbidden tokens) must be detected.  Use
it as the executable reading of the schema and as a regression oracle for faster checkers.

Synthetic stress tests and tightness benchmarks: `experiments/falsify_conjectures.py`
(counterexample search for every theorem) and `experiments/separation_benchmarks.py`
(B1–B11; numbers quoted in the theory report).
