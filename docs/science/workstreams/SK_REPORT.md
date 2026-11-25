# SK_REPORT — Workstream K: certified kinetics — barriers, rates and the third semiring

Science division, independent workstream K.  Written 2026-11-25.  Everything below was produced in one
session; scripts, outputs, running notes and a machine-checked Lean file are in
`experiments/science/ws_K/` (`NOTES.md` is the chronological log).  Labels: **[V]** machine-checked
(Lean declaration named), **[P]** paper proof given here, **[K]** known and cited (reading level stated in
§4), **[N]** numerical evidence only, **[C]** conjecture, **[H]** heuristic.  "Independent replication"
is claimed nowhere: all numerics are my own code testing my own statements.

---

## 1. Verdicts

**In one paragraph.**  A lower bound on a minimax barrier is a cut, and a cut is certified by lower bounds
on the energy over the boxes of its wall; an upper bound on an escape rate is the same cut with the wall
*minimum* replaced by the wall *partition function* and the basin minimum by the basin partition function.
Both are exactly what the verified `(min,+)` and `(+,×)` kernels output, so soundness of "certified
kinetics" needs **no new kernel** — I machine-checked the composition (25 Lean theorems in one file on
top of `verify_sound` / `verifyR_sound`, including two kernel-evaluated instances and a discrete-time
kinetic-trap theorem that needs only stationarity, not reversibility).  Under an envelope class the
barrier height above a state has an **exact** robust interval, attained at the two cone residuals
`−d(a,·)` and `d(·,a)` (the coordinator's sketch 2 is true, with anchors too, and it is the same
one-line lemma that gives Theorems 2.3, 2.4 and 11.12 of the theory report); in the query model a
barrier certificate is a covering of *a separator* (lower bound) and of *a path* (upper bound).  The
limits are sharp and mostly negative: (i) the brief's "iff" for cuts is false as stated (corner cases;
repaired form = Edmonds–Fulkerson 1970); (ii) coordinate cuts certify nothing under unrestricted
single-site moves; (iii) Lagrangian (or Chernoff) relaxation of a counting constraint — the obvious way to
hand a reaction-coordinate cut to the pairwise kernel — **never** beats the trivial bound
`max(E(a),E(b))` (a quadratic penalty does, but unreliably); (iv) there is **no transfer matrix for barriers**: by a theorem of Wrochna (2014/2018)
the barrier threshold problem is PSPACE-complete already for a translation-invariant nearest-neighbour
chain with a fixed alphabet, the family on which minima and partition functions cost `O(nk²)`; (v) rate
bounds inherit a factor `exp(β × envelope distance between basin and wall)`, so first-order envelopes
certify rates only when that distance is `O(kT)`; (vi) a discrete barrier certificate is a statement
about the continuous potential-energy surface only on the voxel *face-adjacency* graph, not on the
programme's default Hamming graph.  Almost all the mathematics is classical (bottleneck duality,
Rayleigh/Dirichlet/Thomson/Nash-Williams, Kac, complete monotonicity, reconfiguration complexity); what
is new is the composition with certified kernels, the robust exact intervals, the covering
characterisation and the negative results.  "Certified kinetics" is therefore a **real but one-sided and
incomplete capability**: it certifies the direction that path-finding methods cannot ("no lower pathway
/ no faster escape through this surface exists"), for cuts with tractable walls.

**Status of the coordinator's sketches.**

| sketch | verdict |
|---|---|
| 1. barrier lower bounds are cut certificates; reduce to `(min,+)` on a constrained set | soundness true **[V]**; "iff" false as stated, true in the form `B(a,b) = max(E(a), max_S min_{∂⁺S} E)` **[K]** (Thm K1); the reduction is real but *incomplete in polynomial size* unless NP = PSPACE (Thm K4) |
| 1. which cuts stay decomposable | boxes (wall = `n` boxes) **[V]**; counting cuts with an exact counter — never with a linear multiplier, unreliably with a quadratic penalty **[P, N]**; coordinate cuts only on restricted site graphs **[P, N]** (Prop. K2, K3) |
| 2. robust interval for the height above `a` | true, exact, with anchors via the conditional envelope `D_A` **[P, N; both ends' soundness V]** (Thm K6); saddle energy in `[B_{f+L}, B_{f+U}]` exactly **[P, N]** |
| 2. query complexity; persistence | certificates are coverings of a separator and of a path **[P, N]** (Thm K7); position-dependent stability of the persistence of one minimum **[P, N]** (Cor. K6.2, K6.4) |
| 3(i) exit time from boundary/basin partition functions | true **[K]**; stronger: discrete-time survival bound for any stationary local kernel **[V]** (Thm K10) |
| 3(ii) gap ≤ `Q/(π(A)π(Aᶜ))` | true **[K, N]** |
| 3(iii) Dirichlet / Thomson as two-sided certificates | true **[K, N]**; Dirichlet side = cuts and level partition functions (kernel-checkable), Thomson side = mixtures of explicit paths (no partition function) (Prop. K11, K12) |
| 3(iv) envelope uncertainty of rates | exact for a single gateway, LP in general, closed-form sound bounds, factor `e^{β·d(basin,wall)}` **[P, N]** (Thm K14) |
| 4. physical meaning | barrier brackets transfer to the continuum on the face-adjacency graph **[P, N]** (Prop. K8); the trap bound holds for every local stationary dynamics **[V]**; continuum rates need a TST prefactor not available in the programme **[K/H]** (§2.9) |

---

## 2. Statements, proofs, counterexamples

### 2.1 Setting

`X` finite, `G = (X, ~)` a connected undirected **move graph**, `E : X → ℝ`.  A walk is a sequence
`x₀ ~ x₁ ~ … ~ x_m`.  The **barrier** is

    B_E(a,b) = min over walks a = x₀, …, x_m = b of  max_j E(x_j)        (endpoints included),

so `B_E(a,b) ≥ max(E(a),E(b))`; the **height** above `a` is `B_E(a,b) − E(a)`; the **depth** of `a` is
`min{B_E(a,b) − E(a) : E(b) < E(a)}` (`+∞` for a global minimiser) — for a strict local minimum this
is the persistence of the class born at `a` in 0-dimensional sublevel-set persistence (elder rule).
`∂⁺S = {y ∉ S : y ~ x for some x ∈ S}` is the outer boundary ("wall") of `S`.

On a product space `X = ∏_i D_i` two move graphs matter: the **Hamming graph** (unrestricted single-site
moves; the programme's default) and a **site-graph product** (site `i` moves along the edges of its own
graph `G_i`, e.g. a cycle of torsion voxels).  Envelope, admissible residual, anchors, McShane envelopes
`L, U`, conditional envelope `D_A`, slack `s` are those of the theory report (§1, §2.3, §11.1–11.2).
`E_g = f + g`.

### 2.2 Barriers: the `(min,max)` problem

**Theorem K1 (cut duality) [K — Edmonds–Fulkerson 1970; (a) is V: `cut_sound`].**
(a) If `a ∈ S`, `b ∉ S` and `E ≥ t` on `∂⁺S`, then `B_E(a,b) ≥ t`.
(b) `B_E(a,b) = max( E(a), max_{S ∋ a, S ∌ b} min_{∂⁺S} E )`; if `B_E(a,b) ≥ t > E(a)` the component
`S*` of `a` in `{E < t}` is a valid cut.  Symmetrically
`B_E(a,b) = max( E(b), max_S min_{∂⁻S} E )` with the inner boundary.
(c) The statement "`B(a,b) ≥ t` iff some `S ∋ a`, `S ∌ b` has `E ≥ t` on its boundary" is **false**
for either boundary convention.

*Proof.*  (a) A walk from `a` to `b` has a first vertex outside `S`; it lies in `∂⁺S`.  (b) `≥` is
(a) and the trivial bound.  Let `t = B(a,b) > E(a)` and `S*` as stated.  `b ∉ S*`, else some walk stays
below `t`; a vertex of `∂⁺S*` with `E < t` would belong to `S*`.  (c) Path graph `a — b`:
`E = (5, 0)`, `t = 5`: `B = 5`, the only admissible `S = {a}` has `∂⁺S = {b}`, `E(b) = 0`;
`E = (0, 5)`: the inner boundary of `S = {a}` is `{a}`, `E(a) = 0`. ∎

In the language of Edmonds–Fulkerson: the vertex sets of `a–b` paths form a clutter whose blocker is the
family of minimal vertex separators, `{a}` and `{b}` included; (b) is their bottleneck theorem.  The
corner cases of (c) are exactly `E(a) = B` or `E(b) = B`; for two local minima below `t` both
conventions give an "iff".  *Numerics T1:* (b) holds on 126/126 exhaustive instances; the unrepaired
"iff" fails on 43 (outer) and 54 (inner) of them.

**Proposition K2 (which cuts are checkable by the existing min-kernel) [P; (a) is V].**
Let `X = ∏ D_i`.
(a) *Box cuts.*  For a box `S = ∏ T_i`, `∂⁺S ⊆ ⋃_i W_i` with the `n` **wall boxes**
`W_i = {x : x_i ∉ T_i, x_j ∈ T_j (j ≠ i)}` (equality on the Hamming graph).  Hence `n` accepted
certificates `verify c_i I W_i L = true` certify that every walk of single-site moves leaving `S` visits
energy `≥ L` — **[V] `box_cut_barrier`**; kernel-evaluated instance **[V] `ferro_barrier`** (three
binary sites, bound `7/2` accepted and attained, bound `4` rejected).
(b) *Coordinate cuts.*  On the Hamming graph `∂⁺{x : x_i ∈ T} = {x : x_i ∉ T}`, the whole complement,
so the certified value is `≤ E(b)`: **coordinate cuts never beat the trivial bound under unrestricted
single-site moves.**  On a site-graph product `∂⁺{x_i ∈ T} = {x_i ∈ ∂⁺_{G_i} T}` is a box; for a cycle
of `k` torsion voxels this is the **certified relaxed scan**

    B(a,b) ≥ min over the two arcs of site i from a_i to b_i of  max_{s ∈ arc} m_i(s),   m_i(s) = min_{x : x_i = s} E(x),

`k` box minimisations (the familiar relaxed torsion scan, with the relaxation certified globally).
(c) *Counting cuts.*  Let `q = Σ_i q_i(x_i)` be integer valued and change by at most `Δ` per move.
For `S = {q < r}`: `∂⁺S ⊆ {r ≤ q < r + Δ}`.  For `q_I(x) = #{i ∈ I : x_i ≠ a_i}` the wall is exactly
the level set `{q_I = r}`; `r = 1` is the box cut that fixes the sites of `I`, `I` = all sites is a
Hamming sphere.  Hence `B(a,b) ≥ max_{1 ≤ r ≤ q_I(b)} min_{q_I = r} E`.  The level minima of a
chain-structured (path-width `w`) pairwise energy are computed exactly by a transfer matrix that carries
the counter, `O(n k^{w+1} R)` operations for all `R` levels at once (script T10; this is the chain
kernel run over tropical polynomials).  A statistic that is itself pairwise ("number of native
contacts" in a product encoding) needs the counter on a decomposition of the union of the interaction
graph and the support graph of `q`.
(d) *Decision-tree cuts.*  The general checkable format is §2.5.

*Proof.*  (a) a move out of the box changes one coordinate `i` to a value outside `T_i` and leaves the
others in their `T_j`.  (b), (c) are the same remark for the respective sets. ∎

**Proposition K3 (a multiplier cannot replace the counter) [P, N].**  Let `q : X → ℝ` be any
statistic and `q(a) < r ≤ q(b)`.  Then

    sup_λ min_x [ E(x) + λ (q(x) − r) ]  ≤  max(E(a), E(b)).

So handing `E + λq` to the pairwise kernel — the Lagrangian bound on `min_{q=r} E` — never certifies
more than the trivial barrier bound.  The same holds for slabs and, at finite temperature, for the
Chernoff bound `Z(q = r) ≤ e^{θr} Σ_x e^{−βE(x) − θq(x)}`: the certified free energy of the level never
exceeds the larger of the free energies of a level on the `a` side and a level on the `b` side.

*Proof.*  For `λ ≥ 0` evaluate at `x = a`: `E(a) + λ(q(a) − r) ≤ E(a)`.  For `λ < 0` evaluate at
`x = b`.  (The supremum is the lower convex envelope of the profile `j ↦ min_{q=j} E` at `r`, and a
barrier top is where the profile is not convex.)  The Chernoff statement is the same argument with
`θ ≷ 0`. ∎  *Numerics T4, T10:* over 151 traps the Lagrangian value was `≤` the trivial bound in every
case (mean certified fraction of the height: 0.00); for a 200-site chain `−155.11 <` trivial
`−154.68 <` true level minimum `−153.31`.

*Remark (a quadratic penalty rescues the leaf rule only partly) [P, N].*  `min_{q=r} E ≥ min_x [E(x) +
μ(q(x) − r)²]` for every `μ`, with equality for large `μ` — as an integer programme.  `(q − r)²` is a
dense pairwise term, so `E + μ(q − r)²` is still an instance of the existing kernel.  For binary sites
with `q` a Hamming distance the pairwise LP relaxation of the penalty alone (what a single `leaf` can
certify) is at most `r² − nr + n/2` (all one-site marginals `1/2`, all pairs anti-correlated), negative
for every `0 < r < n` once `n ≥ 3`: the leaf bound collapses to `−∞` as `μ` grows **[P]**.  For moderate
`μ` it can nevertheless be tight: with the best `μ ∈ {0.25, …, 6}` one leaf certified on average `0.42`
of the level height over 23 traps of random binary models (`n = 10`) — the exact level minimum in
`30 %` of them, nothing in `48 %` (T13) **[N]**.  So, unlike a linear multiplier, a quadratic penalty is
a usable but unreliable way to hand a counting cut to the unmodified kernel; an exact counter (or
branching) is needed for a guarantee.

**Theorem K4 (no transfer matrix for barriers) [K — Wrochna, Theorem 3; the reading as a statement
about barriers is a one-line reduction].**  There are a fixed finite alphabet `Σ` and a fixed relation
`R ⊆ Σ²` such that for the translation-invariant nearest-neighbour chain energy

    E(x) = Σ_{i=1}^{n−1} [ (x_i, x_{i+1}) ∉ R ]       on  Σⁿ,  Hamming graph,

deciding, given `n` and two configurations `a, b` of energy `0`, whether `B_E(a,b) = 0` is
PSPACE-complete.  For the same family `min E` and `Z_β` are computed by one `|Σ| × |Σ|` transfer matrix
(and by linear-size certificates of the verified kernels: tree-exact LP leaf; `zverify2Top_chainCert`).

*Proof.*  `B_E(a,b) = 0` iff `b` is reachable from `a` by changing one symbol at a time through words
all of whose consecutive pairs lie in `R` — Wrochna's `H`-Word Reachability, PSPACE-complete for a
suitable digraph `H = (Σ, R)`. ∎

*Consequences.*  (1) Unless P = PSPACE the barrier of a nearest-neighbour chain is not polynomial-time
computable: the elimination rule of §11.8 of the theory report has no `(min,max)` counterpart.
(2) PSPACE is closed under complement, so if every true statement "`B(a,b) ≥ 1`" on these chains had a
polynomial-size certificate checkable in polynomial time, then NP = PSPACE; in particular the complete
decision-tree certificates of §2.5 need super-polynomially many leaves on some chain instances unless
NP = PSPACE.  The same holds for upper-bound certificates: unless NP = PSPACE some optimal paths are
super-polynomially long.  (3) For pairwise Potts-type energies on general graphs (number of
monochromatic edges, `k ≥ 4` colours) the same threshold problem is PSPACE-complete and shortest
zero-energy paths can be exponentially long (Bonsma–Cereceda) **[K]**.
*What this does not say:* on these chains the barrier takes values in `{0, 1}` (a single domain-wall
sweep costs at most one violated bond), so the hardness is that of the **exact threshold**, not of the
order of magnitude of a rate; whether chain barriers can be *approximated* in polynomial time is open
(§5).  Hierarchy on the programme's best case: minima and partition functions polynomial, barriers
PSPACE-complete.

### 2.3 Barriers under an envelope class

**Lemma K5 (the pinned class is an order interval with attained ends) [P; V: `pinned_bounds`,
`neg_cone_admissible`, `cone_admissible`].**  For every admissible `g` and every `a, x`:
`−d(a,x) ≤ g(x) − g(a) ≤ d(x,a)`, and the functions `−d(a,·)`, `d(·,a)` are admissible and vanish at
`a`.  Consequently, for every functional `Φ` of the pinned energy `e_a = E_g − E_g(a)` that is monotone
in the pointwise order,

    min_g Φ = Φ(f − f(a) − d(a,·)),      max_g Φ = Φ(f − f(a) + d(·,a)),

and if `Φ` is continuous the set of values is the whole interval (the class is convex).  With evaluated
anchors `(A, v)` the same holds with `d` replaced by the conditional envelope
`D_A(x,y) = min(d(x,y), U(x) − L(y))`, the ends being attained **simultaneously in `x`** by

    g⁺ = min(U, L(a) + d(·,a)),        g⁻ = max(L, U(a) − d(a,·)).

*Proof.*  The two inequalities are admissibility for the pairs `(a,x)` and `(x,a)`; admissibility of
the cone residuals is the triangle inequality.  Anchors: `g(x) − g(a) ≤ D_A(x,a)` and `≥ −D_A(a,x)` for
every consistent `g` (theory report, Thm 11.1).  `g⁺` is a minimum of two admissible functions, equals
`v` on `A` because `L(a) + d(a',a) ≥ v(a')`, and `g⁺(x) − g⁺(a) = min(U(x) − L(a), d(x,a))` since
`g⁺(a) = L(a) ≤ U(a)`; `g⁻` symmetrically. ∎

*Instances of the lemma:* `Φ = min_x e_a(x) ≥ 0` gives the sharp-minimum and contact theorems (2.3,
2.4); `Φ = 1/Σ_y e^{−βe_a(y)}` gives thermal contact (11.12); the next theorem is the instance "one
semiring further".

**Theorem K6 (robust barrier height: exact interval) [P, N; soundness of both ends V:
`robust_cut_sound`, `robust_path_sound`, `neg_cone_pinned`, `cone_pinned`].**  Let
`H_g(a,b) = B_{f+g}(a,b) − (f+g)(a)`.  Over the admissible class

    { H_g(a,b) } = [ B_{f − d(a,·)}(a,b) − f(a) ,  B_{f + d(·,a)}(a,b) − f(a) ]        exactly,

the ends being attained at `g = −d(a,·)` and `g = d(·,a)`.  With anchors the interval is
`[B_{f − D_A(a,·)}(a,b) − f(a), B_{f + D_A(·,a)}(a,b) − f(a)]`, attained at `g⁻`, `g⁺`.  The saddle
energy itself ranges exactly over `[B_{f+L}(a,b), B_{f+U}(a,b)]`.  The depth of `a` has its smallest and
largest values at the same two residuals (its range need not be an interval: the value `+∞` occurs).

*Proof.*  `H_g = B_{e_a}(a,b)` is monotone and 1-Lipschitz in `e_a`; apply Lemma K5.  The saddle
energy is monotone in `g`, `L ≤ g ≤ U`, and `L, U` are consistent admissible residuals.  The depth is
`Φ(e) = min{B_e(a,b) : e(b) < 0}`; if `e ≤ e'` the minimum for `e` is over a larger set of smaller
numbers. ∎

*Numerics T2:* agreement to `2·10⁻¹⁶` with an **independent** exact optimisation over the polytope (one
LP per separator for the maximum, one LP per simple path for the minimum) on 16 tiny instances with
symmetric and asymmetric site-additive envelopes; no violation in 2880 (no anchors), 1920 (anchors),
1920 (saddle energy), 2880 (depth) sampled residuals.

*Corollary K6.1 (the robust lower end is a kernel query) [V: `box_cut_barrier_residual`,
`certified_trap_height`; kernel-evaluated: `ferroResidual_trap`].*  For a site-additive envelope
`f − d(a,·)` is the anchored instance `PairInstance.anchored` — the envelope is absorbed into the
one-body tables — so a cut certificate for the anchored instance certifies the height for **every**
residual of the class.  Machine-checked form: if `verifyR (certs i) P (wallBox D i) L = true` for the
`n` wall boxes of a box `D` and the walk starts at an evaluated anchor `(a, v)` in `D`, then for every
`g ∈ ResidualClass P` some configuration on the walk has true energy at least
`L − (E(a) + v)` above the true energy of `a` before the walk can leave `D`.

*Corollary K6.2 (position-dependent stability) [P, N].*  For an `f`-optimal path `P`
(`max_P f = B_f(a,b)`) and an `f`-optimal separator `C` (`min_C f = B_f(a,b)`; if `H_f = 0` the lower
bound below is trivial),

    H_f − max_{y ∈ C} d(a,y)  ≤  H_g(a,b)  ≤  H_f + max_{x ∈ P} d(x,a)     for every admissible g.

The stability theorem for persistence (Cohen-Steiner–Edelsbrunner–Harer) gives `± osc(g)`, i.e.
`± max_{x,y} d(x,y)` (`= Σ_i c_i` for weighted Hamming, extensive).  Here the upper error is paid along
one path and the lower error along one cut; the exact interval was `0.24` (median; range `0–0.85`) of
the sup-norm interval in T2, `[1.70, 4.40]` against `[1.10, 5.90]` for the deepest trap of an 8-torsion
chain (T7).

*Corollary K6.3 (kinetically sharp states) [P].*  A height `h` above `a` is certified with **no
evaluation of the residual** iff some separator `C` between `a` and `b` satisfies
`f(y) − f(a) − d(a,y) ≥ h` on `C`: the known landscape must rise around `a` faster than the envelope —
the kinetic analogue of the sharp-minimum theorem.

*Remark K6.4 (two reference points).*  For quantities that are not pinned at one state — the height
above the lowest point of a basin, the critical depth `max_{x,y}[B(x,y) − E(x) − E(y)] + min E` that
governs the low-temperature spectral gap — the upper end still decouples
(`max_g max_x = max_x max_g`), the lower end is a genuine min–max over the polytope and is not treated
here (§5).

**Theorem K7 (query model: barrier certificates are coverings of a separator and of a path) [P, N].**
Let `g` be the true residual, `E = f + g`, `B = B_E(p,q)`, and let `A` be evaluated.  The saddle
energies consistent with the evaluations are exactly `[LB(A), UB(A)] = [B_{E − s(A,·)}, B_{E + s(·,A)}]`
(Thm K6 with Thm 11.3 of the theory report), and

    LB(A) ≥ B − ε   ⇔   W_ε(A) := { y : s(A,y) ≤ E(y) − B + ε }  separates p from q,
    UB(A) ≤ B + ε   ⇔   V_ε(A) := { y : s(y,A) ≤ B + ε − E(y) }  contains a walk from p to q.

So a lower certificate covers **some separator**, each point with radius "its energy excess over the
saddle, plus ε"; an upper certificate covers **some path**, each point with radius "its energy deficit
below the saddle, plus ε".  (A minimum certificate must cover *every* point, with radius gap + ε:
theory report Thm 11.4.)

*Proof.*  `B_{E − s(A,·)} ≥ B − ε` iff every walk has a vertex with `E(y) − s(A,y) ≥ B − ε`, i.e. meets
`W_ε(A)`; `B_{E + s(·,A)} ≤ B + ε` iff some walk has all vertices with `E(y) + s(y,A) ≤ B + ε`. ∎

*Corollary K7.1 (lower bounds are expensive, upper bounds cheap) [P, N].*  On the `n`-cube with
`f(x) = φ(|x|)`, `φ` with a strict global maximum at layer `m`, uniform Hamming envelope `c`, true
residual `g = 0` (so the slack is `d` itself) and `ε < min(c, φ(m) − max_{j≠m} φ(j))`: every lower
certificate for the barrier between `0ⁿ` and `1ⁿ` contains the **whole transition layer**,
`N_low ≥ C(n,m)`, while `n + 1` evaluations along one monotone path are an exact upper certificate.
(The barrier is `φ(m)`; the covered set `W_ε(A)` lies in layer `m`; each of its points is within slack
`ε < c` of an evaluation, hence evaluated; a separator inside one layer is the whole layer, because
every point of the layer lies on a monotone path that meets the layer only there.)
*Numerics T3:* both equivalences without a mismatch in 1280 tests each; for `n = 4` no anchor set
smaller than the layer (6 points) is a lower certificate (exhaustive).

### 2.4 What a discrete barrier says about the continuous surface

**Proposition K8 (continuum bracket) [P, N].**  Let the configuration torus be covered by the closed
product voxels `V_x`, `x ∈ ∏[k_i]`, let `E_lo(x) ≤ inf_{V_x} E`, `E_hi(x) ≥ sup_{V_x} E`, and let
`G_face` be the **face-adjacency** graph (one torsion moves to a neighbouring arc).  For `p ∈ V_a`,
`q ∈ V_b` and `B_cont(p,q) = inf_γ max_t E(γ(t))` over continuous paths,

    B_{E_lo}^{G_face}(a,b)  ≤  B_cont(p,q)  ≤  B_{E_hi}^{G_face}(a,b).

Enlarging the move graph (e.g. to the Hamming graph on voxel labels) keeps the left inequality and
destroys the right one, and the left side then need not converge to `B_cont` under refinement (it does
not in T8).

*Proof.*  Upper: the union of two face-adjacent voxels is convex, so a discrete walk lifts to a
polygonal path through voxel centres on which `E ≤ E_hi`.  Lower: for a path `γ` the closed sets
`γ⁻¹(V_x)` cover `[0,1]`, so their intersection graph is connected; if `γ(t) ∈ V_x ∩ V_y`, the voxels
containing `γ(t)` form a product of one or two adjacent arcs per coordinate, are connected by face
moves, and all have `E_lo ≤ E(γ(t))`.  This gives a face-adjacent walk from `a` to `b` through voxels
with `E_lo ≤ max_t E(γ(t))`.  (No genericity or continuity of `E` is used.) ∎

*Numerics T8:* two- and three-torsion test potentials with Lipschitz enclosures: all brackets
(`k = 6 … 192` arcs) contain the fine reference bracket (`[1.0894, 1.1863]` from `k = 720` in 2-D); on
the Hamming graph the lower value stays far below (`−0.74` against `0.775` at `k = 96`): a torsion
"jumps" over its own barrier.  The certified relaxed scan of K2(b) coincides with the full discrete
lower bound for `k ≥ 24` in the 2-D example; in 3-D it is `0.24` below it at `k = 24` and `0.09` below
at `k = 48`.

**Consequence for the programme.**  Barrier certificates with the tables `E_lo` (the output of the voxel
enclosure, theory report §3.4) are statements about the potential-energy surface itself *provided the
checker uses the voxel adjacency graph*; with rotamer-like labels and unrestricted single-site moves
they bound only barriers between label combinations, and intra-site torsional barriers are invisible.

### 2.5 Barrier certificate: format, checker, soundness

    inductive BCert (n k)
      | inside                                  -- the current box lies in S
      | wall (c : Cert n k)                     -- the current box lies in the wall; c certifies L on it
      | outside                                 -- unconstrained
      | branch (i : Fin n) (children : Fin k → BCert n k)

`bverify c I a b L` accepts iff (1) every `wall` leaf satisfies `verify c I (box of the leaf) L = true`
(for a residual problem: `verifyR`); (2) no `inside` leaf box is adjacent to an `outside` leaf box —
two boxes `D, D'` are adjacent iff `#{i : D_i ∩ D'_i = ∅} ≤ 1` (on a site-graph product: … or the one
disjoint coordinate has a `G_i`-edge between the two domains); (3) the leaf containing `a` is `inside`,
the leaf containing `b` is not.  Cost: the kernel cost of the wall leaves plus `O(ℓ² n k)` for `ℓ`
leaves; the verifier never searches.

**Soundness statement (to formalise next to `verify_sound`).**  If `bverify` accepts, every walk from
`a` to `b` visits a configuration of energy at least `L`; with `verifyR` leaves and `a` an anchor:
for every residual of the class the height of the barrier above `a` is at least `L − (E(a) + v_a)`.
*Proof:* `S` = union of the `inside` leaves; a move from `S` to its complement cannot land in an
`outside` leaf by (2), hence lands in a `wall` leaf; `cut_sound` and `verify_sound`.  The special case
"`S` is a box" is **[V]** (`box_cut_barrier`, `box_cut_barrier_residual`, `certified_trap_height`); the
tree checker is specified, not formalised.

*Upper bounds* are walks: a list of configurations with one-site changes and a claimed bound on each
energy; under a residual each energy is bounded through the upper McShane envelope of the anchors
(`le_upperEnv`), or pinned at `a` through `f + d(·,a)` (**[V]** `robust_path_sound`).

*Completeness and size.*  The format is complete (full tree) but, by Theorem K4, not polynomially so.
Empirically (T11, small systems only) the wall of the *exact* cut of a trap was covered greedily by
`3–10` boxes for random pairwise models with `n ≤ 10` and by a median of `7 / 11 / 11` (max `9 / 22 /
26`, at most `3.2 n`) boxes for rotational-isomeric chains with `n = 6 / 7 / 8` torsions.

### 2.6 Rates

`P` (discrete time) or `Q` (continuous time) is a Markov dynamics on `X` with stationary law
`π ∝ e^{−βE}`; `Q(A,Aᶜ)` is the stationary probability flux out of `A` (equal to the flux in);
`k_TST(A) = Q(A,Aᶜ)/π(A)`; `τ` is the exit time of `A`.

**Theorem K10 (certified kinetic trap; stationarity suffices) [V: `trap_survival`,
`trap_certificate`, `trap_certificate_weighted`].**  Let `P` be a stochastic kernel on a finite set with
stationary weights `w ≥ 0` (not necessarily reversible or normalised) and `surv_T(x)` the probability
that the chain started at `x` spends its first `T` steps in `A`.  Then

    Σ_{x∈A} w(x) surv_T(x)  ≥  w(A) − T · Σ_{x∉A} Σ_{y∈A} w(x) P(x,y).

If moreover `Σ_{y∈A} P(x,y) ≤ κ(x)` for `x ∉ A`, `Σ_{x∉A} w(x) κ(x) ≤ U` and `0 < Lo ≤ w(A)`, then

    P_{π_A}( τ > T )  ≥  1 − T · U / Lo .

For a local kernel `κ` vanishes off the wall; for a sampler with uniform proposals among `deg`
single-site moves `κ(x) = deg_A(x)/deg`.  So **an upper bound on a (weighted) wall partition function
and a lower bound on a basin partition function certify a lower bound on survival, for every stationary
local dynamics** — the "free-energy well" argument, here with a machine-checked statement.
*Numerics T9:* Metropolis, heat-bath and a non-reversible single-site kernel with the same `π`: 30
cases, no violation; at `T = 0.5/k` the exact survival was `0.59–0.77` against the bound `0.50–0.60`.

**Reversible, continuous time [K — Aldous–Fill Ch. 3, Lemma 3.16 and Prop. 3.21; Rayleigh].**
`λ_A ≤ k_TST(A)` for the principal Dirichlet eigenvalue (indicator test function); the exit time from
the quasi-stationary law is exponential with rate `λ_A`; the exit time from `π_A` is completely
monotone with `P_{π_A}(τ > t) ≥ e^{−k_TST t}` and `E_{π_A} τ ≥ 1/k_TST`; and `1/k_TST` is *exactly* the
mean sojourn in `A` per entrance (Kac).  `k_TST` is the discrete transition-state-theory rate: it counts
every crossing of the dividing set, recrossings included.  The spectral gap satisfies
`gap ≤ Q(A,Aᶜ)/(π(A)π(Aᶜ))`.  For Metropolis rates `min(1, e^{−βΔE})` per neighbour and `A` a component
of a sublevel set, `Z·Q(A,Aᶜ) = Σ_{y∈∂⁺A} deg_A(y) e^{−βE(y)}` exactly; in general this is an upper
bound for every single-site dynamics with rates at most one per neighbour.

**Proposition K11 (Dirichlet certificates: shorting, series law) [K, N].**  For a partition of `X`
into classes with values `φ_I` (`1` on the class of `A`, `0` on that of `B`),
`cap(A,B) ≤ Σ_{I<J} C_{IJ} (φ_I − φ_J)²` with `C_{IJ}` the total conductance between the classes, and
upper bounds on the `C_{IJ}` suffice (Rayleigh monotonicity): a checker needs only arithmetic.  For the
levels of a statistic `q` that changes by at most one per move this is Nash-Williams' inequality
`cap ≤ [Σ_m 1/C_m]^{-1}`, and for `q_I` on the Hamming graph

    Z·C_m ≤ min( (m+1) Z_{m+1} , max_{q=m}(number of up-moves) · Z_m ),      Z_j = Σ_{q=j} e^{−βE},

so **level partition functions certify capacities**.  The same test functions give a multi-cut
improvement of the TST bound: for `A = {q < m*}` and every `m₀ < m*`,
`λ_A ≤ [Σ_{m=m₀}^{m*−1} 1/C_m]^{-1} / π(q ≤ m₀)`.
Mean transition times: `E_{ν}[τ_B] = Σ_y π(y) h_{A,B}(y)/cap(A,B) ≥ π(A)/cap(A,B)` for the reactive
entrance law `ν` on `A` (identity checked to `2·10⁻⁹` in 38 well-conditioned cases and to `5·10⁻⁶¹`
in 60-digit arithmetic where double precision fails).

**Proposition K12 (Thomson certificates: path mixtures, parallel law) [K, N].**  Every unit flow gives
`cap(a,b) ≥ 1/𝒟(ψ)`; a flow supported on `K` edge-disjoint walks gives `cap ≥ Σ_j 1/R_j`,
`R_j = Σ_{e ∈ γ_j} 1/c(e)` — only energies along the walks enter, no partition function — and
`E_a[τ_b] ≤ (1 − π(b)) 𝒟(ψ)`.  Flows built from the conductances of a reaction coordinate are valid
(divergence-free) only for exactly lumpable models.  One genuinely *product* flow is checkable **[P, N]**:
flip the `D` sites on which `a` and `b` differ in a uniformly random order; the flow through an edge
leaving level `m` of the spanned subcube is `1/(C(D,m)(D−m))`, and for Metropolis conductances

    cap(a,b)⁻¹ ≤ 𝒟(ψ) ≤ Z · Σ_{m<D} [C(D,m)(D−m)]⁻² [ (D−m) Z⁻_m + (m+1) Z⁻_{m+1} ],   Z⁻_j = Σ_{level j} e^{+βE},

a capacity **lower** bound from *negative-temperature* level partition functions (same kernel, sign of
`β` reversed).  *Numerics T12 (`n = 8`):* the flow is exact for a flat landscape and for Curie–Weiss
(the `Z⁻` form loses a factor `≤ 2`); on random pairwise landscapes it gives `0.43–0.59` of the capacity
at `β = 0.5` (one path: `0.07–0.09`) but `10⁻⁴–10⁻³` at `β = 2` (one path: `0.19–0.37`).  So product
flows are the Thomson certificate for entropic barriers, path mixtures for energetic ones.

**Proposition K13 (one cut, three semirings) [P].**  For `A` contained in `{E ≤ m_W}`,
`m_W = min_{∂⁺A} E`, `m_A = min_A E`, Metropolis rates:

    e^{−β(m_W − m_A)} / |A|  ≤  k_TST(A)  ≤  |E(A,Aᶜ)| · e^{−β(m_W − m_A)},

so `−β⁻¹ ln k_TST(A) = (m_W − m_A) + O(β⁻¹ ln(|A||E(A,Aᶜ)|))`: the rate certificate of a cut
tropicalises to its barrier certificate.  Dictionary: indicator test function ↔ cut; Nash-Williams over
disjoint cuts ↔ maximum over cuts; path flow ↔ path; parallel law ↔ minimum over paths; the
Dirichlet–Thomson duality becomes the bottleneck duality of Theorem K1.  The `(min,max)` algebra enters
only through the definition of `B`; the certificates live in `(min,+)` and `(+,×)`.

*Tightness against exact linear algebra (T5, T5b, T7; no inequality is violated in the 43 cases of T5):*

| quantity (exact / bound) | range observed | remark |
|---|---|---|
| `λ_A / k_TST(A)` | `0.24 – 1.00` | `A` = sublevel component of the trap |
| `E_{π_A}τ · k_TST` | `1.00 – 3.86` | survival bound holds on 61 times in every case |
| `gap / [Q/(π(A)π(Aᶜ))]` | `0.14 – 0.66` | `0.04 – 0.09` when `A` is not the slowest mode (chain, T7) |
| `cap(a,b)` / single cut | `0.014 – 0.67` | `0.28 – 0.67` at `β = 8` |
| `cap(a,b)` / Nash-Williams over levels of `q` | `1.000` Curie–Weiss, `0.965–0.999` Ising chain, down to `0.0007` on a random 3-state model | only as good as the coordinate |
| one path / `cap`, ≤ 8 disjoint paths / `cap` | `0.001–0.98`, `0.008–0.99` | `0.73–0.99` (8 paths) at `β = 8` |
| Curie–Weiss `n = 10 … 320`, `β = 1.3`: `λ_A/k_TST` | `0.283, 0.173, 0.109, 0.076, 0.058, 0.044` | recrossing, `≈ n^{−1/2}` |
| the same, multi-cut bound of K11 | `0.73 → 0.9998` | series law recovers the rate |

So at low temperature (`β = 8` here) the cut bound (Dirichlet) and a handful of paths (Thomson) bracket
a capacity within a factor `≈ 1.5–5`; at high temperature or for collective barriers a single cut loses the
recrossing factor and the levels of a good coordinate are needed.

### 2.7 Rates under an envelope class

Let `A` be chosen from the known part, `E_g = f + g`, and
`k(g) = Σ_{x∈A, y∉A, x~y} e^{−β max(E_g(x),E_g(y))} / Σ_{x∈A} e^{−βE_g(x)}`; write `n_y = deg_A(y)`.

**Theorem K14 (robust TST bounds) [P, N].**
(a) *Single gateway — exact.*  `π_g(y)/π_g(A)` ranges exactly over
`[ 1/Σ_{x∈A} e^{−β(f(x) − f(y) − d(y,x))} , 1/Σ_{x∈A} e^{−β(f(x) − f(y) + d(x,y))} ]`
(Lemma K5 pinned at `y`; thermal contact restricted to `A ∪ {y}`).
(b) *Sound closed forms.*  For every admissible `g`

    k(g) ≤ K_gate := Σ_{y∈∂⁺A} n_y / Σ_{x∈A} e^{−β(f(x) + d(x,y) − f(y))},
    k(g) ≤ K_a    := Σ_{edges} e^{−β max((f − d(a,·))(x), (f − d(a,·))(y))} / Σ_{x∈A} e^{−β(f + d(·,a))(x)},

both made of partition functions of anchored (one-body-shifted) instances, and more generally for every
"transport plan" `θ_y(·)` (a probability on `A` for each wall point)
`k(g) ≤ max_{x∈A} Σ_y n_y θ_y(x) e^{−β(f(y) − f(x) − d(x,y))}`; `K_gate` is the plan
`θ_y(x) ∝ e^{−β(f(x)+d(x,y))}`.
(c) *Sensitivity.*  `K_gate ≤ [Σ_y n_y e^{−βf(y)} / Z_f(A)] · exp(β max_{x∈A, y∈∂⁺A} d(x,y))`, and
`sup_g k(g) ≥ k(−d(a,·))`.
(d) *Exact value.*  `sup_g k(g)` is a linear program in the weights `w = e^{−βg}` over the cone
`w(y) ≤ e^{βd(x,y)} w(x)` (Charnes–Cooper), of the size of the state space.

*Proof.*  (b) `e^{−β max(E_g(x),E_g(y))} ≤ e^{−βE_g(y)}` and `E_g(x) − E_g(y) ≤ f(x) − f(y) + d(x,y)`;
for `K_a` pin numerator and denominator at `a` (Lemma K5).  Plans: `u = e^{−βE_g}` satisfies
`u_y ≤ e^{−β(f(y) − f(x) − d(x,y))} u_x`; average over `θ_y`, exchange sums, bound by the maximum.
(c) factor `e^{−βd(x,y)} ≥ e^{−β max d}` out of each denominator of `K_gate`. ∎

*Numerics T6 (LP, 33 cases, no violation):* the exact inflation `β⁻¹ ln(sup_g k / k(0))` was
`0.10–0.77` energy units for envelopes with `Σ c_i` between `0.5` and `3.6`, about one third (median
`0.36`) of the bound (c); `K_gate` overshoots by `0.02–0.5`, `K_a` by `0–1.0` energy units; in the
instance inspected the LP optimiser *was* the cone residual `−d(a,·)` at `β = 1, 2` (the same extremal
as for the barrier) **[N]**.

**Reading.**  A first-order envelope with constants `c_i` certifies `ln k` only up to
`β · (sum of the c_i over the sites that separate basin from wall)`; at one `kT` of uncertainty per
site a transition that moves five sites is uncertain by `e⁵`.  Evaluating the residual at the basin
minimum and at the gateways removes the leading term (replace `d` by `D_A`), at the price of the
covering of Theorem K7; the remaining entropy terms are quantizer problems (theory report Thm 11.13
applied to the wall and to the basin).

### 2.8 Rate certificate: format, checker, soundness

A rate certificate is a cut tree as in §2.5 whose `wall` leaves carry `ZCert`s for an **upper**
instance (weights rounded up) and whose selected `inside` leaves carry `ZCert`s for a **lower**
instance; the checker runs `zverifyTop` (or `zverify2Top`) on every leaf box, adds the upper ends of the
wall leaves (each multiplied by a bound `κ ≤ 1` on the entrance probability) into `U`, the lower ends of
the inside leaves into `Lo`, checks the adjacency condition (2) of §2.5 and outputs the rational `U/Lo`.

**Soundness statement.**  If the checker outputs `U/Lo`, then for every stochastic kernel that is
stationary for the Boltzmann weights and moves one site per step,
`P_{π_A}(τ > T) ≥ 1 − T·U/Lo` for all `T` (**[V]** `trap_certificate_weighted` + `zverifyTop_sound` +
`certified_partition_of_intervals`; the glue is not formalised), and for reversible continuous-time
dynamics with rates at most one per neighbour `λ_A ≤ U′/Lo` and `P_{π_A}(τ > t) ≥ e^{−tU′/Lo}` **[K]**,
where `U′` is the wall sum weighted by `deg_A(y)` instead of `κ(y)`.
Robust version: anchored upper/lower instances as in Theorem K14(b).  Level certificates (K11) need the
same kernel over polynomial weights (§7, request T2).  Rate *lower* bounds are path lists (K12) plus an
upper bound on `Z(A)`.

### 2.9 Which kinetic statement is physically meaningful?

1. **Barriers** are properties of the energy function and of a notion of adjacency, not of a
   dynamics.  By Proposition K8 a certified `[B_{E_lo}, B_{E_hi}]` on the voxel adjacency graph brackets
   the potential-energy barrier of the model surface: a *model-relative statement about the force
   field*, with the same status as the certified minimum.
2. **The trap bound** (Theorem K10) holds for every Markov dynamics that is stationary for the Gibbs
   measure and local on the chosen graph.  It is first of all a statement about **samplers**: a
   certificate that Metropolis or Glauber sampling with that move set cannot leave a region within `T`
   steps except with probability `T·U/Lo` — a certified diagnosis of non-equilibration that the
   programme can apply to its own Monte Carlo evidence.
3. **Physical rates** [K/H].  For classical Hamiltonian or underdamped Langevin dynamics the expected
   number of outward crossings of a dividing surface per unit time in equilibrium is the TST flux
   (surface partition function × mean normal velocity), and the same union bound gives
   `P(exit before t) ≤ t·k_TST`; variational TST is an upper bound on the classical reactive flux
   (Wigner; Vanden-Eijnden–Tal).  The configurational factor — surface partition function over basin
   partition function — is what the voxel kernel can enclose; the kinetic prefactor (mass metric in
   torsion space, cf. theory report §4.4) is not in the programme, and for overdamped dynamics the
   instantaneous flux is infinite and one needs the capacity instead.  The discrete Metropolis rate is
   **not** a physical rate; only its Arrhenius exponent (Prop. K13) is transferable.
4. **What must not be claimed:** that a certified discrete rate bounds an experimental rate; that a
   barrier certified on the Hamming graph of rotamer labels is a barrier of the molecule; that a rate
   bound survives per-site envelope uncertainties larger than `kT/(number of sites that move)`.

### 2.10 Assessment

*Relabelling or capability?*  As mathematics it is a relabelling of classical variational principles —
I found no theorem here that would surprise a specialist in metastability or combinatorial
optimisation, with the possible exceptions of the robust exact intervals (K6, K14a), the covering
characterisation (K7) and the vacuity of the multiplier relaxation (K3), all of which are short.  As a
*capability* it is real, because the classical principles are one-sided in exactly the way certified
kernels are: every other route to a barrier or a rate (nudged elastic band, string methods, transition
path sampling, Markov state models, discrete path sampling) produces paths, i.e. **upper** bounds on
barriers and **lower** bounds on rates along the pathways found; none can assert that no lower pathway
exists.  Cuts assert exactly that, and their soundness reduces to minima and partition functions over
boxes — the two things MetricChain certifies.  The capability is bounded by Theorem K4 (no completeness
in polynomial size, even on chains), by the quality of tractable cuts (T7: on small rotational-isomeric
chains box and counting cuts certified `55–77 %` of the trap depths on average, a global
contact-number coordinate `0 %`), and by the envelope factor of K14.

*The one experiment-facing statement.*  "For this force field (with these certified table enclosures),
**every** pathway that changes torsion `i` from the arc of conformer `a` to the arc of conformer `b`
crosses potential energy at least `L` above `a`" — a certified relaxed scan (K2b + K8) — and, with a
classical TST prefactor, "the classical exchange rate between the two conformers is at most
`ν e^{−ΔF‡_cert/kT}`".  A measured activation energy or exchange rate (dynamic NMR of hindered
rotations is the obvious test bed) *above* a certified upper bound would falsify the energy model
independently of any sampling; current practice cannot make a statement of that logical form.  This is
a proposal: no physical system has been treated here.

---

## 3. Numerics

All scripts are in `experiments/science/ws_K/`; run with `OMP_NUM_THREADS=1 python3 <script>` (the
machine was shared and oversubscribed; multi-threaded BLAS was an order of magnitude slower).  Outputs
are the `out_*.txt` files.  State spaces are enumerated exhaustively; floating point (not interval)
arithmetic except where stated.  Random instances: pairwise tables with Gaussian entries
(`scale_h = 0.5`, `scale_J = 1`), interaction graph a chain plus each longer-range pair with probability
1/4 ("chain+") or complete.

| script | what | sizes | result |
|---|---|---|---|
| `t1_cut_duality.py` | Thm K1 (exhaustive over all `S`), counterexamples, K2(a,b) | `N = 8…16`, 126 instances | formula 126/126; unrepaired iff fails 43/54; coordinate wall = complement 800/800; box wall = `n` boxes 186/186 |
| `t2_robust_barrier.py` | Thm K6, Lemma K5, Cor. K6.2 | `N ≤ 81`; LP check `N = 8, 9` | LP agreement `2e-16` (16 instances); 0 violations in 9600 samples; path- and cut-radius bounds 48/48 |
| `t3_cover.py` | Thm K7, Cor. K7.1 | `N ≤ 128` | 0 mismatches in 2 × 1280 tests; whole layer necessary (`n = 4` exhaustive) |
| `t4_cut_families.py` | certified fraction of trap depth: box / sphere / count / Lagrangian | binary `n = 10`, 3-state `n = 6`, 151 traps | box `0.89–0.99` (exact in `76–93 %`), count `0.91–1.00`, sphere `0.69–0.86`; Curie–Weiss: box `1.7` of `4.5`, count exact; Lagrangian `0.00`, never above trivial |
| `t5_rates.py` | K10 (reversible part), K11, K12 against exact eigenvalues, exit times, capacities | `N ≤ 1024`, 43 (system, β) cases | no violation; ranges in the table of §2.6; hitting-time identity `≤ 2e-9` in 38 cases, 5 cases ill-conditioned in double precision |
| `t5b_scaling_highprec.py` | the identity at 60 digits; Curie–Weiss lumped chain up to `n = 320` | — | defect `4.7e-61`; recrossing `≈ n^{-1/2}`; multi-cut ratio → `0.9998`; rows with `λ_A < 1e-10` not reported |
| `t6_robust_rates.py` | Thm K14: LP for `sup_g k(g)` vs closed forms and samples | `N = 256, 243`, 33 cases | no violation; inflation `0.10–0.77`; optimiser admissible and attains the LP value |
| `t7_chain.py` | rotational-isomeric chain on the diamond lattice, hard overlaps, `E = 0.5·#gauche − #contacts` | `n = 6, 7, 8` torsions; 683 / 2005 / 5849 states | box/count certify `1.00 / 0.55 / 0.77` of the depths (17 / 35 / 85 traps); global contact-number cut `0.00`; connected piece of the contact superlevel set `0.24 / 0.89 / 0.49`; `λ_A/k_TST = 0.75–0.87` |
| `t8_voxel_continuum.py` | Prop. K8, certified relaxed scan | 2 torsions up to `720²`, 3 torsions up to `96³` voxels | all brackets contain the reference bracket; the Hamming-graph lower bound stays far below at every resolution tested |
| `t9_trap_stationary.py` | Thm K10 for Metropolis, heat-bath, non-reversible kernels | `N = 256, 243`, 30 cases | no violation |
| `t10_counter_dp.py` | counting cuts at scale (transfer matrix with counter) | validation `n = 12`; `n = 200` | errors `4e-15`, `7e-15`; height bracket `[1.3758, 1.5178]` on `2²⁰⁰` states; Lagrangian below trivial |
| `t11_cut_size.py` | greedy number of wall boxes of exact cut certificates | as T4, T7 | median `≤ 1.6 n`, max `3.2 n` boxes |
| `t12_product_flow.py` | random-order (product) flow and its `Z⁻` bound against exact capacities | `N = 256`, 13 cases | no violation; exact when lumpable; useless at low temperature on rugged landscapes |
| `t13_penalty_lp.py` | linear multiplier, quadratic penalty (integer and pairwise-LP leaf) against exact level minima | binary `n = 10`, 8 + 23 traps | linear: below trivial always; quadratic integer → exact; quadratic LP leaf: mean `0.42`, exact `30 %`, nothing `48 %`; collapses for large `μ` |
| `KineticsCertificates.lean` | 25 theorems (listed below) | — | `lake env lean`: exit 0, no warnings; `#print axioms` of all 25: `[propext, Classical.choice, Quot.sound]` (`out_lean.txt`) |

**Machine-checked statements** (`experiments/science/ws_K/KineticsCertificates.lean`; imports
`proofs.CertificateAlgebra`; not part of the library; re-check with
`export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH"; cd /home/user/MetricChain; lake env lean experiments/science/ws_K/KineticsCertificates.lean`):
`exists_exit`, `cut_sound`, `pinned_bounds`, `neg_cone_admissible`, `cone_admissible`,
`robust_cut_sound`, `robust_path_sound`, `neg_cone_pinned`, `cone_pinned`, `mem_wallBox_of_exit`,
`box_cut_barrier`, `box_cut_barrier_residual`, `certified_trap_height`, `ferro_wall_verified`,
`ferro_wall_rejects`, `ferro_barrier`, `ferro_start`, `ferro_wall_attained`,
`ferroResidual_wall_verified`, `ferroResidual_trap` (the `ferro*_verified`, `_rejects`, `_start`,
`_attained` facts by `decide +kernel`, i.e. the checker is run inside Lean's kernel), `surv_nonneg`,
`surv_le_one`, `trap_survival`, `trap_certificate`, `trap_certificate_weighted`.
What is **not** machine-checked: the exactness (attainment and interval) part of K6 beyond the two
admissibility lemmas, K7, K8, the decision-tree checker of §2.5, the composition of K10 with the
Z-kernel, and every reversible/spectral statement.

**Caveats.**  (i) Every landscape is tiny (at most 5849 states, plus one 200-site chain treated by
dynamic programming); the fractions in T4, T7, T11 are not monotone in `n` and must not be
extrapolated.  (ii) The chain model of T7 is a toy (lattice, contact energy) and is not pairwise in the
torsion coordinates, so it tests theorems and cut families, not the kernels.  (iii) The non-reversible
kernels of T9 leave the boundary flux unchanged by construction, so that test exercises the theorem
weakly; the theorem itself is machine-checked.  (iv) In T5 the first run (kept as
`out_t5_partial_first_run.txt`) was killed for slowness, not for a failure.

**One cross-check against another division.**  The numbers of self-avoiding conformations found by my
enumeration in T7 for `n = 6, 7, 8` torsions — 683, 2005, 5849 — coincide with the engineering
division's counts for the same model and the same `n` (`PUBLISHED_CONFS` in
`experiments/eng/chain_cover/run_lattice.py` and the header `conformations=683` of
`data/dia_Sc12_n6.txt`, in their checkout at `db56d05`; their `dia_enum.c` defines the same chain: `n`
torsions, `n + 3` beads, first two bonds fixed, self-avoidance).  I read those files and did not run
their code.  This replicates those three counts with independent code; nothing else of theirs was
replicated.

---

## 4. Prior art

Reading levels: **[full]** = I read the stated pages; **[tool]** = the page was fetched and the
statements extracted by the fetch tool, not read raw by me; **[snippet]** = search-result summary only;
**[memory]** = from memory, unverified in this session.

| topic | source | level | relation to this report |
|---|---|---|---|
| bottleneck duality | J. Edmonds, D. R. Fulkerson, "Bottleneck extrema", J. Combin. Theory 8 (1970) 299–306 | [full, pp. 299–301] | Thm K1(b) is their theorem for the clutter of `a–b` paths; their introduction attributes the path/cut case (arcs) to Fulkerson, Pollack, Hu |
| reconfiguration on chains | M. Wrochna, "Reconfiguration in bounded bandwidth and treedepth", arXiv:1405.0847v1 (journal version J. Comput. Syst. Sci. 2018 [snippet]) | [full, pp. 1–8] | Theorem 3 (`H`-Word Reachability PSPACE-complete) is Thm K4; the paper itself remarks that existence and counting are trivial there; `k`-Coloring, Independent Set, Shortest Path reachability PSPACE-complete at bounded bandwidth; polynomial for bounded tree-depth |
| recolouring | P. Bonsma, L. Cereceda, Theoret. Comput. Sci. 410 (2009) 5215–5226 | [snippet] | PSPACE-complete for `k ≥ 4`, polynomial for `k = 3`, exponential distances |
| Boolean solution graphs | Gopalan, Kolaitis, Maneva, Papadimitriou (2009) | [memory] | context for binary models; I did not verify a pairwise-binary (Ising) hardness statement |
| barrier problem in RNA | Maňuch, Thachuk, Stacho, Condon, Natural Computing 10 (2011) 391–405 | [snippet] | NP-completeness of an energy barrier problem in a restricted move model |
| disconnectivity graphs, barrier trees | Becker, Karplus, J. Chem. Phys. 106 (1997) 1495; Flamm, Hofacker, Stadler, Wolfinger, Z. Phys. Chem. 216 (2002) 155; Wales, *Energy Landscapes* [memory] | [snippet] | exact merge trees by exhaustive enumeration / flooding, or from sampled stationary points (uncertified) |
| certified saddles in the continuum | Westerberg, Floudas, J. Chem. Phys. 110 (1999) 9259; Nerantzis, Adjiman, J. Glob. Optim. 67 (2017) 451–474; Lin, Stadtherr (2004) | [snippet] | deterministic enclosure of *all* stationary points / index-1 saddles by interval branch and bound: the existing route to a guaranteed barrier, in low dimension; cuts over voxel walls are a different certificate for the same quantity |
| persistence stability | Cohen-Steiner, Edelsbrunner, Harer, Discrete Comput. Geom. 37 (2007) 103–120 | [snippet] | sup-norm bound compared with in Cor. K6.2 |
| interval-valued fields | Günther, Salmon, Tierny, "Mandatory critical points of 2D uncertain scalar fields", Comput. Graph. Forum 33 (2014) 31–40 | [snippet] | critical points and merge trees forced by pointwise bounds `f⁻ ≤ f ≤ f⁺`: the interval analogue of "saddle energy in `[B_{f+L}, B_{f+U}]`"; I could not read the definitions (server error) |
| hitting times from stationarity | Aldous, Fill, *Reversible Markov chains and random walks on graphs*, Ch. 3 §3.5 (Lemma 3.16, Prop. 3.21) | [tool] | `π(Aᶜ)/Q(A,Aᶜ) = E_{ρ_A} T_A ≤ E_{π_{Aᶜ}} T_A ≤ 1/λ_A`; complete monotonicity; the lower bound `exp(f′(0)t/f(0))` — the reversible part of Thm K10 |
| free-energy wells | Ben Arous, Gheissari, Jagannath, "Algorithmic thresholds for tensor PCA", arXiv:1808.00921 | [snippet] | exit-time lower bound from the Gibbs measure restricted to a well: the union-bound argument formalised in `trap_survival` |
| potential theory of metastability | Bovier, Eckhoff, Gayrard, Klein, Commun. Math. Phys. 228 (2002) 219–255; Bovier, den Hollander, *Metastability* (2015) [memory]; Berman–Konsowa principle (den Hollander, Jansen, arXiv:1309.1305) | [snippet] | capacities, Dirichlet and Thomson/Berman–Konsowa principles, mean hitting-time formula (K11, K12); capacity `≍ e^{−β·barrier}` [memory] |
| Nash-Williams | Lyons, Peres, *Probability on Trees and Networks*, §2.5 | [snippet] | series law of K11 |
| spectral gap and critical depth | Holley, Kusuoka, Stroock, J. Funct. Anal. (1989); Hajek (1988) | [snippet for the citation; statement from memory] | gap `≍ e^{−βm}`; relevant to Remark K6.4 |
| variational TST | Wigner (1938) [memory]; Vanden-Eijnden, Tal, J. Chem. Phys. (2005) | [snippet] | TST frequency ≥ true frequency (recrossing); §2.9 |
| caution on VTST bounds | Phys. Rev. E 61, 2457 (2000), "Breakdown of the bounding properties of variational transition state theory and the Rayleigh quotient method" | [title only; abstract not accessible] | I could not read it; it may restrict the scope of item 3 of §2.9 |
| Markov state models | Noé, Nüske, Multiscale Model. Simul. (2013), arXiv:1211.7103; Webber et al., arXiv:2005.02248 | [snippet] | Rayleigh-quotient estimates of slow eigenvalues from data: the same variational direction, statistical not certified (my inference from the principle, not a quoted statement) |
| imprecise Markov chains | Krak, T'Joens, De Bock, ISIPTA 2019 (PMLR 103) | [snippet] | lower/upper expected hitting times for sets of chains; related to K14 but with interval transition probabilities, not an envelope on an energy |
| provable design | OSPREY 3.0, MARK*, BBK* (Donald lab) | [snippet] | provable minima and partition functions; no barrier or rate guarantee found |

**Search log** (web search unless stated; "nothing found" means nothing in that query, not that nothing
exists).  (1) Wrochna bounded bandwidth reconfiguration → paper; fetched and read pp. 1–8.
(2) Bonsma–Cereceda title → abstract-level summary.  (3) Edmonds–Fulkerson "Bottleneck extrema" →
scanned PDF; read pp. 299–301.  (4) Aldous–Fill hitting time lower bound from stationarity → book
chapter; two fetches of Ch. 3 §3.5.  (5) "free energy well" exit time lower bound → Ben Arous et al.
(6) Maňuch et al. energy barrier NP-complete → citation.  (7) Westerberg–Floudas all transition states →
citation; Nerantzis–Adjiman → citation.  (8) persistent homology with pointwise varying error bounds /
interval-valued functions / merge trees → no direct hit; follow-up: mandatory critical points → citation
(PDF server returned 503).  (9) BEGK low-lying spectra → citation.  (10) Berman–Konsowa → den
Hollander–Jansen.  (11) **extended search** "rigorous / certified / computer-assisted / verified upper
bound on a transition rate or lower bound on an energy barrier of a molecular potential energy
surface" → nothing relevant; one hit on the breakdown of VTST bounds (abstract inaccessible, 403).
(12) Vanden-Eijnden–Tal TST → meeting abstract.  (13) Flamm et al. barrier trees → citation.
(14) Noé–Nüske variational approach → citation.  (15) Becker–Karplus → citation.
(16) Holley–Kusuoka–Stroock → citation only.  (17) imprecise Markov chains hitting times → citation.
(18) Cohen-Steiner–Edelsbrunner–Harer → citation.  (19) Nash-Williams / Lyons–Peres → citation.
(20) provable guarantees for conformational transition barriers in protein design (OSPREY) → nothing
on kinetics.  Not searched: tropical / ultrametric limits of effective resistance; hardness of
barriers for binary pairwise (Ising) models; approximability of barriers; lower bounds on spectral
gaps by canonical paths as certificates.

**Classification.**

| item | class |
|---|---|
| K1 (cut duality), K10 reversible part, K11, K12, gap bound, Kac identity | **known** (classical) |
| K4 as a statement about barriers of chains; "no transfer matrix"; consequences for certificate sizes | **known theorem, new reading** (the reduction is one line; Wrochna's own remark already contrasts reachability with existence/counting) |
| K2 (wall of a box = `n` boxes; coordinate cuts trivial on the Hamming graph; certified relaxed scan), K8 (continuum bracket on the face-adjacency graph), K13 | **new combination** of elementary facts; I found no statement of them in this form, and each is short enough to be folklore |
| K3 (multiplier/Chernoff relaxation is vacuous at a barrier) | **possibly new as a stated lemma**; two-line proof, certainly known in spirit (a barrier top is a non-convex point of the profile) |
| K5–K6 (pinned extremal lemma; exact robust interval for barrier height, depth, saddle energy; with anchors) | **possibly new** in this form; elementary; subsumes Thm 2.3, 2.4, 11.12 of the theory report; the interval-valued-field literature (mandatory critical points) is the closest prior art I found and I could not read it |
| K7 (barrier certificates are coverings of a separator and of a path) and K7.1 | **possibly new**; the analogue of the covering theorem for minima |
| K14 (robust TST bounds: exact single gateway, transport-plan bounds, sensitivity factor) | **possibly new combination** (linear-fractional programming over the weight cone is standard; cf. imprecise Markov chains) |
| machine-checked composition with `verify_sound` / `verifyR_sound`; `trap_survival` | **new artefacts** |

---

## 5. What I did not settle

1. **Approximability on chains.**  Theorem K4 is about an exact threshold with barrier values in
   `{0,1}`.  Is the barrier of a nearest-neighbour chain approximable in polynomial time to additive
   error `ε·max|J|`?  Is the problem already hard for *binary* chains, or for chains with generic
   (non-degenerate) energies?  I did not look.
2. **Two-point robust quantities** (Remark K6.4): the exact robust range of the critical depth
   (spectral-gap exponent) and of the height above an unknown basin minimum.
3. **Exponent of the number of evaluations** needed to certify a barrier on product spaces (the
   analogue of `R*` of the theory report): only the example K7.1.
4. **Structure of the worst-case residual for rates** (K14d): when is `−d(a,·)` optimal?  Observed in
   one instance at two temperatures **[N]**; no theorem.
5. **Typical effectiveness and size of tractable cuts for long chains.**  All data are for `n ≤ 10`
   sites; the dependence on `n` in T7/T11 is not even monotone.
6. **Lower bounds on spectral gaps** (upper bounds on relaxation times): these need path systems
   (canonical paths) for *all* pairs; not treated beyond the remark that they are the Thomson side.
7. **Continuum rates**: the TST prefactor in torsion coordinates; the paper Phys. Rev. E 61, 2457 on
   failures of VTST bounds, which I could not read; overdamped dynamics (capacity instead of flux).
8. **Strictness in Remark K6.4** and the tightness of the transport-plan bounds of K14(b) (LP duality
   should give equality for the relaxed problem; not checked).
9. I did not verify the **journal versions** of Wrochna's and Bonsma–Cereceda's theorems, nor read
   Bovier–den Hollander for the exact form of the hitting-time identity (it was checked numerically).

---

## 6. The three most promising next steps

1. **A certified relaxed torsion scan on a real small molecule** (the experiment-facing statement of
   §2.10).  Needs interval tables `E_lo, E_hi` of a force field on torsion voxels with nearest-voxel
   adjacency; output: a certified bracket for a rotational barrier, to be compared with a measured
   activation energy.  This is the smallest end-to-end demonstration of a statement that sampling cannot
   make, and it exposes the real obstacle (the lever arm: the energy is not pairwise in torsions, so the
   wall minimisations need the profile/feature classes of theory report §11.17, not the pairwise
   kernel).
2. **Two kernel extensions that make the formats of §2.5 and §2.8 executable:** the decision-tree cut
   checker (`bverify`, pure combinatorics on boxes) and the Z-kernel over polynomial weights
   (`ℚ[z]` with the coefficientwise order), which turns one chain certificate into certified level
   partition functions and hence into Nash-Williams rate certificates; plus the tropical counterpart
   (an elimination rule in the min-kernel over min-plus polynomials) for counting cuts.
3. **The complexity frontier for chains:** approximability of the barrier of a nearest-neighbour chain
   and the query-complexity exponent of barrier certification on product spaces (Theorem K7 reduces it
   to a covering problem for separators).  Either a polynomial approximation scheme or a hardness of
   approximation would tell the programme whether "certified barriers for chain-structured known parts"
   is a tractable target at all.

---

## 7. Requests

### To the theory division

**T1 (formalise, small).**  Move the content of `experiments/science/ws_K/KineticsCertificates.lean`
into the library (it checks against `5ed4072` as it is) and add the decision-tree checker of §2.5:
`BCert`, `bverify`, and `bverify_sound : bverify c I a b L = true → ∀ walk of single-site moves from a
to b, ∃ j, L ≤ I.energy (p j)`; residual version on `verifyR`.  The only new lemma is "two boxes contain
a pair of configurations that differ in at most one site iff at most one coordinate has disjoint
domains".

**T2 (generalise the weight domain).**  Is `zverify2_sound` valid verbatim over an ordered commutative
semiring in place of `ℚ≥0`?  For `ℚ≥0[z]/(z^{R+1})` with the coefficientwise order this would give, from
one `chainCert`, certified brackets for all level partition functions `Z_r = [z^r] Z(z)` of a
site-additive statistic — the inputs of Proposition K11.  Same question for the tropical kernel with an
elimination rule over min-plus polynomials (level minima; Proposition K2(c)).  Proposition K3 shows that
a linear multiplier cannot replace this, and T13 that a quadratic penalty does so only unreliably.

**T3 (state and prove).**  Theorem K6 in full (exactness: the set of heights is the closed interval) and
Theorem K7, in the style of `CertificationGeometry.lean`; this needs a definition of `B` as a minimum
over walks on a finite graph.  Also the reversible continuous-time refinement of `trap_survival`
(`λ_A ≤ Q(A,Aᶜ)/π(A)` as a Rayleigh-quotient statement for a symmetric matrix).

**T4 (question).**  Remark K6.4: is the robust lower end of a two-point quantity (critical depth)
computable by a polynomial number of anchored barrier computations, or is it NP-hard on the polytope?

### To the engineering division

**E1 (benchmark; precise).**  *Motivation:* effectiveness of tractable cuts versus chain length.
*Formulation:* for rotational-isomeric chains on the diamond lattice with the energy of
`experiments/science/ws_K/t7_chain.py` (and for the profile-format known parts of `chain_cover`),
enumerate all feasible conformations for `n = 6 … 13` torsions; compute the exact merge tree under
single-torsion moves; for every local minimum with positive depth report (i) the depth, (ii) the best
box cut and the best counting cut `q_I` over all `I` (for `n > 10`: over `|I| ≤ 4` and `I` = all), (iii)
the greedy number of wall boxes of `t11_cut_size.py`.  *Inputs:* `n`, `e_g = 0.5`, `ε = 1`, `S_c = 8`.
*Expected output:* a table of the mean certified fraction and the box counts versus `n`.
*Validation:* reproduce `out_t7.txt` and `out_t11.txt` for `n = 6, 7, 8` (17 / 35 / 85 traps; fractions
`1.00 / 0.55 / 0.77`).  *Stopping condition:* `n = 13` (1 231 221 conformations by your `PUBLISHED_CONFS`) or 6 GB.
*Resources:* union–find merge tree is `O(N n)`; the subset loop is the cost — restrict `I` as stated.

**E2 (prototype).**  A producer for certified relaxed scans on a torsion-voxel model: given interval
tables on product voxels with nearest-voxel adjacency, a torsion `i` and two voxel arcs, output the `k`
profile values `m_i(s) = min_{x_i = s} E_lo` with their min-certificates and the bracket of Proposition
K8.  *Validation:* the test potentials of `t8_voxel_continuum.py` (2 and 3 torsions; reference bracket
`[1.0894, 1.1863]`).

**E3 (cut search).**  A heuristic that, given a trap and a path found by any path-finding method, grows
a box or decision-tree cut around the trap and reports the certified wall height and the number of wall
boxes — to measure how often "path found" and "cut certified" meet on instances beyond enumeration.
