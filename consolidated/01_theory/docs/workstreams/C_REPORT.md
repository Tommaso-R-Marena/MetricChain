# Workstream C — other representations of the certification geometry
*Reduced costs / Johnson / A\*, discrete weak KAM and tropical spectral theory, optimal transport,
tight spans, Funk geometry.  A dictionary with consequences.*

Directory: `<session scratch>/ws/C/`
(scripts `lib.py`, `t*.py`; outputs `out_*.txt`; the Lean scratch file `NormalForm.lean`; four
downloaded papers in `refs_*/`).  Nothing in `/home/user/MetricChain` was modified.

Notation as in `COMMON.md`: `X` finite, envelope `d`, known part `f`, residual `g ∈ Lip(d) :=
{g : g(x) − g(y) ≤ d(x,y)}`, `E = f + g`, `E* = min E`, slack `s(a,y) = d(a,y) − g(a) + g(y)`,
McShane envelopes `L_A`, `U_A`.  Additional notation used throughout:

* `d^φ(a,y) := d(a,y) + φ(a) − φ(y)` — the **reduced cost** of `d` under a potential `φ`
  (Johnson reweighting; Goldberg–Harrelson write `ℓ_π`).
* `f^d(y) := min_x [f(x) + d(x,y)]` — Pasch–Hausdorff envelope (theory report §2.3), the min-plus
  product `f ⊗ d`; contact set `{f = f^d}`.
* `σ_f := d^f` (signed), `σ := d^{f^d}` (nonnegative), `E^d := f^d + g`, `gap^d := E^d − E*`.
* point width `w_pt(A) = min_A E − min(f + L_A)`, value width `w_val(A) = min(f+U_A) − min(f+L_A)`.

Status tags: **[K]** known (cited), **[R]** routine, **[N]** apparently new for the certification
problem, **[V]** core machine-checked in `NormalForm.lean`, **[T: script]** tested numerically.

---

## 1. Verdicts (one paragraph)

All three suspected identifications are real, but they import theorems very unevenly.
**(1) Reduced costs / A\*:** literally the same objects — the slack is the reduced cost of `d` under
the perfect potential, the lower McShane envelope is the landmark (ALT) heuristic, envelope
propagation is pathmax, best-first search is AESA with the `D_∞` ordering ("A\* that turns every
expanded node into a landmark"), and Johnson's algorithm applied to the signed envelope
`σ_f = d^f` is the Pasch–Hausdorff regularisation of the known part.  Consequences: a
**normal-form theorem** — *a known part is exactly the gradient part of an asymmetric envelope*,
so every instance `(d, f, g)` is an instance with `f ≡ 0` (Theorem C1; the exchange lemma,
sharpness, D30 and "gaps are not Lipschitz" become one-liners); the **Dechter–Pearl
classification** transfers with Dechter–Pearl's own proof — best-first search is *type-3
optimal* (not strictly dominated), *no* algorithm is type-2 optimal, i.e. certification sits
exactly in the "admissible but inconsistent heuristic" cell of their table, and the hub is their
node `J₂` (Theorem C3); and a **second resource-augmentation bound, in centre form**, that needs
no `κ < 1` (Theorem C4, core machine-checked).  The A\* theory does **not** give a count bound
stronger than Theorem 11.11, and the normal form shows why: a known part makes the geometry
asymmetric, and then even the one-dimensional theorem of Hansen–Jaumard–Lu fails — on the line
with a known part best-first search uses `≈ log₂(1/η)` (zero residual) or `≈ 1.3/η` (extremal
residual) evaluations against a certificate of two (Proposition C5).  (An exploratory rule that
selects by elimination power under the central interpolant finds these hubs and needs 55–72 %
of the evaluations of best-first search on additive product landscapes; no theorem.)  **(2) Weak KAM /
tropical:** literal but *degenerate* for the envelope itself (critical value 0, Aubry set =
everything, every admissible function is a weak KAM solution); it has content in three places —
after conditioning (determined set = static class of the data node; the minimal exact
uniqueness set is the set of sources and sinks of the calibration order, C6), for asymmetry
(irreducible asymmetry = maximum cycle mean of the antisymmetric part, C1(e)), and for chains
(sharpness threshold = minimum cycle ratio; for the Ising chain `c* = 2h` independent of `J`,
C7).  Tropical *linearity* of `g ↦ min(f+g)` is the exact reason why single dips are extremal at
zero temperature, and non-idempotency is the reason they are not at finite temperature (C8).
**(3) Optimal transport, tight spans, Funk:** identities only (slack = Kantorovich duality gap =
twice a Gromov product = tropical Funk distance between one-point envelopes; `κ` and the
quasi-symmetry constant are Funk distances in the polytrope); the tight span is a *different*
(dual) tropical polytope, not the admissible class; no new theorem.  **Prior art found that the
repository does not cite:** Hetland (2020) proves, for metric nearest-neighbour search, that the
optimal number of distance computations is a directed minimum dominating set, with the same
0/1/2-distance hardness gadget as Theorem 11.10 and the same adversary argument as Theorem
11.23(a); Mustăţa (2009) has a Shubert-type method on quasi-metric spaces.

---

## 2. Statements, proofs, counterexamples

### 2.1 Normal forms: a known part is an asymmetric envelope

**Theorem C1 (gauge and normal forms) [N; V for the algebraic core; T: `t1`, `t2`, `t10`].**

(a) *Gauge.*  For every `φ : X → ℝ`: `d^φ` is an envelope (no sign condition), `Lip(d^φ) = φ +
Lip(d)`, the slack of `φ + g` for `d^φ` equals the slack of `g` for `d`, and
`L_A^{d^φ}[φ+g] = φ + L_A^d[g]`, `U_A^{d^φ}[φ+g] = φ + U_A^d[g]`.  Hence the instances `(d, f, g)`
and `(d^φ, f − φ, g + φ)` have the same energies, the same slack, the same evaluations up to the
known shift `φ(a)`, and the same certified bounds for every evaluated set.  Two gauges are
canonical: `φ = −g` gives `(s, E, 0)` (the unknown residual is absorbed: *every instance is a
zero-residual instance in its own slack geometry*, and `Lip(s) = Lip(d) − g`), and `φ = f` gives
`(σ_f, 0, E)`.

(b) *Signed normal form.*  `(d, f, g) ≅ (σ_f, 0, E)` for **all** notions: point, value and
configuration certificates, covers, best-first trajectories.  `σ_f(a,y) = sup_{g' ∈ Lip(d)}
[(f+g')(a) − (f+g')(y)]` is the pairwise worst-case regret (for `A = ∅` this is the quantity of
theory report Theorem 11.2); it is negative exactly when `a` strictly dominates `y` (a
dead-end-elimination pair).  So in the report's own formal framework (`IsEnvelope` does not ask
for nonnegativity) "`f ≡ 0`" is without loss of generality.

(c) *Regularisation = Johnson's algorithm.*  Johnson's potential of the signed matrix `σ_f` is
`m(y) := min_x σ_f(x,y) = f^d(y) − f(y) ≤ 0`, and `σ = (σ_f)^m = d^{f^d} ≥ 0` is a quasi-metric.
For every `g' ∈ Lip(d)`: `min(f+g') = min(f^d+g')`.  For every evaluated set `A`:

    w_val^{(d,f,g)}(A) = w_pt^{(σ,0,E^d)}(A) = w_val^{(σ,0,E^d)}(A),

so `N_value(d,f,g) = N_point(σ,0,E^d)`: value certificates *are* point certificates of the
regularised instance, and in normal form the two notions coincide.  The covering relations
coincide in three forms,

    ∀y ∃a∈A: s(a,y) ≤ gap(y)+ε   ⟺   ∀y ∃a∈A: s(a,y) ≤ gap^d(y)+ε   ⟺   ∀y ∃a∈A: σ(a,y) ≤ gap^d(a)+ε

(client radius `gap(y)`; regularised client radius; **centre radius** `gap^d(a)` in the reduced
envelope), because `s(a,y) − gap^d(y) = σ(a,y) − gap^d(a)`.  Moreover `E^d ∈ Lip(σ)` and the
regularised gap is 1-Lipschitz for the slack: `gap^d(y) ≤ gap^d(x) + s(x,y)`.

(d) *Which quasi-metrics arise.*  If `d` is symmetric, `σ(a,y) − σ(y,a) = 2(f^d(a) − f^d(y))`: the
antisymmetric part of the reduced envelope is a gradient.  Conversely a quasi-metric `τ` is of
the form `d^φ` with `d` symmetric and `φ = φ^d` iff its antisymmetric part `α = (τ − τᵀ)/2` has
zero circulation on every triangle (Kolmogorov's criterion); then `d = (τ + τᵀ)/2`,
`φ(x) = α(x,o)`.  *"Symmetric envelope + known part" ≡ "reversible (gradient) quasi-metric, no
known part".*

(e) *Irreducible asymmetry.*  For an arbitrary quasi-metric `τ`,
`ι(τ) := min_φ max_{a,y} |α(a,y) − φ(a) + φ(y)|` equals the maximum cycle mean of `α` (a max-plus
eigenvalue); `ι = 0` iff (d) applies; and `Lip(τ) ⊆ φ* + Lip(τ_sym + ι·[a≠y])` for an optimal
`φ*`: every asymmetric envelope class is contained in a (symmetric envelope, known part) class
whose envelope is larger by `ι`.

*Proof.*  (a) is algebra: `(φ+g)(x) − (φ+g)(y) ≤ d(x,y) + φ(x) − φ(y)`; zero diagonal and triangle
inequality are preserved by telescoping; `max_a[(φ+g)(a) − d^φ(a,y)] = φ(y) + L_A(y)`.
(b) is (a) with `φ = f`; the supremum of `g'(a) − g'(y)` over `Lip(d)` is `d(a,y)` (attained by
`−d(a,·)`).  (c) `m(y) = min_x[d(x,y) + f(x)] − f(y)`; `(σ_f)^m = d^{f+m} = d^{f^d}`, nonnegative
because `f^d(y) ≤ f^d(a) + d(a,y)`.  If `f^d(y) = f(x) + d(x,y)` then `f^d(y) + g'(y) ≥ f(x) +
g'(x)` by admissibility, so `min(f^d+g') ≥ min(f+g')`, and `f^d ≤ f` gives the converse.
`min_x(f+U_A)(x) = min_{a∈A}[g(a) + min_x(f(x) + d(x,a))] = min_A E^d`, and `min(f+L_A) =
min(f^d+L_A)` (the lemma applied to `L_A ∈ Lip(d)`), while `f^d + L_A` is the lower envelope of
`E^d` for `σ` by (a); in normal form `min U_A = min_A E^d` because `σ ≥ 0`.  First covering
equivalence: `gap^d ≤ gap` gives ⇐; for ⇒ let `x` attain `gap^d(y) = min_x[gap(x) + s(x,y)]` and
let `a` cover `x`; then `s(a,y) ≤ s(a,x) + s(x,y) ≤ gap(x) + ε + s(x,y)`.  Second: the displayed
identity.  (d) `α(a,y) = f^d(a) − f^d(y)` for symmetric `d`; conversely zero triangle
circulation makes `α` a coboundary `φ(a) − φ(y)` on the complete graph, and `φ = φ^d` is
equivalent to `τ ≥ 0`.  (e) `min_φ max[α − δφ]` is the least `λ` for which `α − λ` has no
positive cycle, i.e. the maximum cycle mean (max-plus spectral theorem, **[K]**); `α` is
antisymmetric, so the maximum of the residual over ordered pairs is the maximum of its absolute
value. ∎

*What this buys (each a one-line consequence).*

1. **Exchange lemma** (theory report Theorem 11.5, `value_exchange`): a value certificate is a
   point certificate of the regularised instance; the exchange moves an anchor to a contact
   point (where `E = E^d`).
2. **Sharp minimum / dichotomy** (Theorems 2.4, 11.7): one evaluation at `x̂` is an exact value
   certificate iff `σ(x̂,·) ≡ 0`, i.e. `x̂` dominates every state (and an exact point certificate
   iff moreover `x̂` is a contact point, which is the criterion `σ_f(x̂,·) ≤ 0` of Theorem 11.7).  On a product, `σ = Σ_i σ_i` and
   `f^d = Σ_i min(φ_i, min φ_i + c_i)` (excitation energies truncated at the envelope constant);
   a two-state site has `σ_i(0,1) = (c−e)₊`, `σ_i(1,0) = c + min(e,c)`: the site is sharp iff
   leaving the ground state is free in the reduced envelope.  The exponent `R* = max_μ[h(μ) −
   h(ρμ)]` depends on the site only through the asymmetry ratio `q = σ(1,0)/σ(0,1) =
   (1+ρ)/(1−ρ)`: *asymmetry of the reduced envelope helps certification* (`R* = ln 2` at `q = 1`,
   `R* → 0` as `q → ∞`) — and hurts search (C4, C5).
3. **"Gaps are no longer Lipschitz, so the problem is priority k-centre with arbitrary radii"**
   (theory report §11.2) is avoidable: after the free replacement `f → f^d` the client radii
   `gap^d + ε` are 1-Lipschitz for the slack, and in centre form the radius function is
   `σ`-admissible — the classical picture of Lipschitz optimisation (an evaluation at `a`
   certifies the ball of radius `gap(a) + ε` around `a`) is universal.  The raw gap fails to be
   slack-Lipschitz exactly when `f ≠ f^d` (897 of 1200 random instances, `t1`).
4. **D30** (`f(x) = x` on `{0} ∪ {2^{−i}}`): `σ(a,y) = 2(a−y)₊`, going right is free, `σ(0,·) ≡ 0`:
   the pathology is an infinite quasi-symmetry constant of `σ`, nothing else.
5. **Asymmetric envelopes** are not an extra generality on top of known parts: gradient
   asymmetry *is* a known part; only the cyclic part (`ι > 0`) is new.
6. **Best-first search** with the rule `argmin(f + L_A)` only ever evaluates contact points and
   is a best-first search of the normal form with a particular tie-breaking (`t10`, 400
   instances); its first two queries do not depend on the instance (`t3`).

### 2.2 Dictionary I — reduced costs, A\*, landmarks, AESA

| certification | shortest paths / heuristic search | status |
|---|---|---|
| `g` admissible | potential `π` feasible / heuristic consistent (Goldberg–Harrelson §2) | literal |
| slack `s = d^{−g}` | reduced cost `ℓ_π(v,w) = ℓ(v,w) − π(v) + π(w)` for the perfect potential | literal |
| `slack_isEnvelope` | Johnson's lemma: reweighting commutes with shortest paths | literal |
| `L_A = max_a[g(a) − d(a,·)]`; `lowerEnv_admissible` | landmark (ALT / differential) heuristic `max_ℓ[dist(ℓ,t) − dist(ℓ,v)]`; G–H Lemma 2.1 "the maximum of feasible potentials is feasible" | literal for `g = dist(·,t)` |
| update `L_{A∪y} = max(L_A, g(y) − d(y,·))` | pathmax (Mérő 1984), bidirectional pathmax | literal |
| `f^d` (regularised known part) | cost-so-far `g*(v)` from a super-source with arc lengths `f` | literal |
| `f^d + L_A` (certified lower bound) | A\* evaluation function `g* + h` | literal |
| `E^d = f^d + g`, `gap^d` | length of the shortest solution through `v`; its detour | literal |
| uncovered set `{s(A,y) > gap^d(y)}` | nodes surely expanded by A\* with landmark set `A` | literal (C2) |
| exact cover; `N_cov` | perfect landmark set for the query; least number of landmarks | literal (C2) |
| best-first search (Piyavskii–Shubert) | "A\* that inserts every expanded node as a landmark"; AESA with the `D_∞` ordering (Vidal 1986; Figueroa et al. 2009 §3.1) | literal for `f ≡ 0`, `g` a distance function |
| dip at `y` (Theorems 11.22–23) | Dechter–Pearl's goal appended to an unexpanded node (their Fig. 5) | same argument; A\*'s detection sets are singletons |
| certificates = hitting sets of detection sets | must-expand pairs, minimum vertex cover, NBS ≤ 2·VC (Eckerle et al. 2017; Chen et al. 2017) | same structure; sets of size 2 there, unbounded here |
| hub (D26) | node `J₂` of Dechter–Pearl Fig. 6a: a node A\* never expands whose value lets `B` skip others | same phenomenon |
| — | the A\* *algorithm* (an expansion reveals arcs) | **analogy only**: an expansion is not an evaluation of `g` |

**Theorem C2 (A\* with landmarks is a certification instance) [K+R; T: `t4`].**  Let `(V, ℓ ≥ 0)`
be a digraph with shortest-path quasi-metric `d`, target `t`, start costs `f` (a super-source),
`g = d(·,t) ∈ Lip(d)`, so that `C* = min(f+g)`.  For a landmark set `A` the heuristic `h_A = L_A`
is consistent with `h_A(t) = 0`, and A\* (any tie-breaking) expands every node of
`{v : f^d(v) + L_A(v) < C*} = {v : s(A,v) > gap^d(v)}` — the set **not covered** by `A` — and no
node with `f^d + L_A > C*`.  So `A` is an exact cover of the instance `(d, f, d(·,t))` iff A\*
expands only tie nodes, and `N_cov` is the least number of landmarks that makes the heuristic
perfect for the query.  The lower bound `f^d + L_A` that best-first certification minimises is
A\*'s `f`-value: best-first search evaluates the node that A\* would expand next and then uses it
as a new landmark.  (553 random digraphs with integer lengths, A\* run on the sparse graph:
must-expand set = uncovered set in every case.)

**Theorem C3 (where certification sits in the Dechter–Pearl hierarchy) [N — a transfer; T: `t3`, `t13`].**
Call a deterministic algorithm *correct* if it is `ε/2`-correct on the whole class (theory report
§11.10); its evaluated set is then a value `ε`-certificate.  Let `BF*` be best-first search in
normal form with the value stopping rule: first query a `σ`-centre (a minimiser of the one-point
width `w₁(x) = max_y σ(x,y)`, the minimax-regret point), then always a minimiser of `f^d + L_A`,
stopping as soon as the evaluated set is a value certificate (any deterministic tie-breaking).
Dominance is inclusion of evaluated sets, as in Dechter–Pearl §4.2.

(i) *(their Theorem 8, with singleton detection sets.)*  Every correct algorithm evaluates every
forced point (a point covered only by itself); so does `BF*`.  On random instances 66 % of the
evaluations of best-first search are forced.

(ii) *(their Theorem 10 / Corollary 3.)*  **`BF*` is type-3 optimal**: if a correct algorithm `B`
skips, on some instance, a point that `BF*` evaluates, then there is an instance on which `B`
evaluates a point that `BF*` skips.  No correct algorithm strictly dominates `BF*`.

(iii) *(their Corollary 4.)*  **In general no correct algorithm is type-2 optimal**: there are
spaces (already the equilateral triangle with `f ≡ 0`) on which, for every correct algorithm,
some instance lets another correct algorithm evaluate a proper subset of its points.  `BF*` is
not type-2 optimal even generically: in 15 % of random instances a proper subset of the points
evaluated by best-first search is already a certificate.  (On a space where one evaluation
always certifies — all sites sharp — the statement is of course false.)

So the exact counterpart of "A\* is optimal" is false, the strongest type of optimality that
exists is type 3, and it is attained by best-first search — the row "admissible `h`" of
Dechter–Pearl's Figure 9 (*A\*\* is 3-optimal, no 2-optimal exists*), with the McShane lower
envelope in the role of A\*\*'s path-max evaluation function.

*Proof.*  (i) Theory report Theorems 11.6(a) / 11.22(a).  (ii) Let `y₁, …, y_K` be the sequence
of `BF*` on `g`, `Q` the set evaluated by `B` on `g`, and `j` the first index with `y_j ∉ Q`.
*Case `j ≥ 2`.*  `A = {y₁,…,y_{j−1}} ⊆ Q` is not a value certificate (a property of the values on
`A` only).  Let `g' = L_A`, the lower envelope of these values: `g' ∈ Lip(d)` and `g' = g` on
`A`.  On `g'`, `BF*` repeats `y₁,…,y_j` (same history), and at `y_j` it finds
`E'^d(y_j) = (f^d + L_A)(y_j)`, the lower bound itself, so the certificate closes: its evaluated
set on `g'` is `A ∪ {y_j}`.  On `g`, `B` must leave `A` (subsets of `A` are not certificates); let
`z` be its first query outside `A`.  All earlier queries were in `A`, where `g' = g`, so `B`
makes the same query `z` on `g'`, and `z ≠ y_j` because `y_j ∉ Q`.  Thus on `g'` the algorithm `B`
evaluates `z ∉ A ∪ {y_j}`.  *Case `j = 1`.*  If the centre `x₁` alone is a certificate, `BF*`
evaluates `{x₁}` on every instance, and `B`'s first query is another point.  Otherwise no single
point is a certificate (one-point widths do not depend on the instance, and `x₁` minimises
them); the second query `x₂` of `BF*` is instance-independent, and on `g'_v = v − d(x₁,·)` its
evaluated set is `{x₁, x₂}`.  If `B`'s first query `z₁ ∉ {x₁,x₂}` we are done; if `z₁ = x₂`, choose
`v` with `g'_v(x₂) = g(x₂)`: `B`'s second query on `g'_v` is the one it made on `g`, which is
neither `x₂` nor `x₁`.  (iii) Equilateral triangle `X = {a,b,c}`, `d ≡ 1` off the diagonal,
`f ≡ 0`, `ε < 1/2`, `E = (1/2, 0, 1)`: the value certificates are `{b,c}` and `X` (`{a,b}`, `{a,c}`
have width `1/2`).  An algorithm whose (instance-independent) first query is `a` evaluates all
of `X` here, a proper superset of the certificate `{b,c}` used by the correct algorithm
"evaluate `b`, `c`; continue only if the certificate is open"; by symmetry every first query is
wrong for some instance.  For `BF*` itself: `X = {x*, y, h}`, `f ≡ 0`,
`σ(x*,y) = 5, σ(x*,h) = 4.5, σ(y,x*) = 1, σ(y,h) = 2, σ(h,x*) = 3, σ(h,y) = 2`, `E = (0,1,3)`,
`ε = 0`: `BF*` evaluates `y, h, x*`, while `{x*, h}` is a certificate (`h` covers `y` at zero
slack). ∎

*Reading.*  (1) The proof of (ii) is Dechter–Pearl's proof of their Theorem 10 — "append a goal
to the node the algorithm is about to expand, at a cost equal to its current `f`-value" is the
optimistic instance `g' = L_A` — and it needs the *propagated* lower bound, exactly as theirs
needs A\*\*'s path-max.  (2) Why not more: Dechter–Pearl's strong optimality needs information to
be local (expanding `n` is the only way to learn about `n`) and the prior to be consistent
(nothing propagates).  An envelope makes information non-local by design, so certification is
always in their "inconsistent" regime, where they already show that an algorithm can skip many
nodes by first expanding a node that A\* never expands, "relying on the admissibility of `h`"
(their Fig. 6a).  That node is the hub.  (3) Bidirectional search is the intermediate case:
detection sets are pairs, the instance optimum is a minimum vertex cover, and NBS is within the
factor 2 = size of a detection set, which is unavoidable (Chen et al. 2017, abstract).  In
certification the detection sets `{a : s(a,y) < gap(y)+ε}` are unbounded, and the hub family
(`min(M,N)+1` against `N_cov = 2`) is the corresponding lower bound.  A second, independent
obstruction is the tie plateau ("needle in a haystack"): many points whose lower bound is within
`ε` of `E*`, one of which is the minimiser — Dechter–Pearl's "pathological instances".
(4) Type 3 is a weak notion (it only says "not strictly dominated"); I state it because it is
exactly what Dechter–Pearl's theory yields here, not because it is a performance guarantee.

### 2.3 What search can achieve: a second bound, and where it fails

**Theorem C4 (best-first search, centre form) [N as stated, R in method; V core; T: `t9`].**  Let
`ρ ≥ 1` be the quasi-symmetry constant of the reduced envelope, `σ(x,y) ≤ ρ σ(y,x)` (it depends
on the known data `(d, f)` only; for symmetric `d` and `f^d` `λ`-Lipschitz, `ρ = (1+λ)/(1−λ)`).
For **every** admissible residual `g` (`κ = 1` allowed) and every `ε ≥ 0`, best-first search
started at a contact point makes at most `|C|` evaluations for every set `C` such that

    ∀y ∃c ∈ C:  σ(c,y) ≤ θ (gap^d(c) + ε),      θ = 1/(2ρ+3)

(`|C| + 1` for an arbitrary first point).  For `f ≡ 0` and symmetric `d` this reads: at most as
many evaluations as the smallest covering of `X` by balls `B_d(c, (gap(c)+ε)/5)`; for symmetric
`d` in general `θ = (1−λ)/(5−λ)`.

*Proof.*  In normal form the evaluated points satisfy, for `j < k`,
(a) `σ(y_j,y_k) > ε` and (b) `σ(y_j,y_k) ≥ gap^d(y_j)`: the lower bound at `y_k` when it is
chosen is at least `E^d(y_j) − σ(y_j,y_k)`, it is `< UB − ε ≤ E^d(y_j) − ε` because the search has
not stopped, and it is `≤ E*`.  Suppose `y_j, y_k` lie in the ball of the same `c`, and put
`r = θ(gap^d(c)+ε)`.  Then `σ(y_j,y_k) ≤ σ(y_j,c) + σ(c,y_k) ≤ (ρ+1) r`, and `gap^d(y_j) ≥
gap^d(c) − r`.  With (a): `(ρ+1) r > ε`; with (b): `(ρ+2) r ≥ gap^d(c)`.  Adding,
`(2ρ+3) r > gap^d(c) + ε ≥ (2ρ+3) r`, a contradiction.  So `k ↦ c(y_k)` is injective. ∎
(`NormalForm.lean`, `not_cocovered_centre`.)

*Comparison with Theorem 11.11* (`|C|+1` for covers with client radii `θ'(gap(y)+ε/6)`,
`θ' = (1−κ)/(4(1+κ))`, `g` `κ`-Lipschitz, `f` arbitrary).  The two are dual and incomparable:
11.11 restricts the *unknown* residual and degenerates as `κ → 1`; C4 restricts the *known* part
and degenerates as `λ → 1`; C4 has no `+1` (a shrunk centre cover contains an `ε`-minimiser).  On
60-point line instances (`t9c`; means over 25 instances; best-first search itself used 11–15
evaluations):

| `κ` | `λ` | `N_cov` | C4 bound | 11.11 bound |
|---|---|---|---|---|
| 0.5 | 0 | 10.8 | **32.4** | 42.8 |
| 0.9 | 0 | 8.0 | **29.4** | 47.7 |
| 0.99 | 0 | 7.5 | **29.2** | 50.7 |
| 0 | 0.5 | 11.9 | 38.3 | **32.9** |
| 0 | 0.9 | 8.9 | 41.0 | **28.9** |
| 0.5 | 0.5 | 9.4 | **32.8** | 38.0 |

Both are far from the truth (constants not tight: no violation of C4 at `2θ` in 2500 random
instances, violations at `3θ`), and both are vacuous on small random metric spaces, where the
shrunk covers are everything (`t9b`).  On the binary product family (below) both are weak:
exponent `0.534` for C4 and `0.475` for 11.11 at `ρ = 1/2`, against `0.355` from a direct packing
argument.

**Proposition C5 (no constant factor on the line once there is a known part) [N; T: `t5d`, `t5`,
`t5e`].**  Points `x* = −D`, `c = 0`, `t_j = jh` (`j ≤ M`, `Mh = L_e = 0.98 G/η`, `h = D/8`),
`d = |x−y|`, `ε = 0.01 G`.
*Family A (zero residual):* `f(x*) = 0`, `f(0) = G`, `f(t) = G + (1−η)t`, `g ≡ 0`, `D = 1.5G`.
*Family B (extremal residual):* `f(x*) = D`, `f(0) = G`, `f(t) = G + (1−η)t`, `g = −|x|`, `D = 0.75G`.
In both `f = f^d`, `{x*, c}` is a point certificate (`N_point = 2`), and best-first search
(started at `argmin f = x*`) makes

| `η` | 0.2 | 0.1 | 0.05 | 0.025 | 0.0125 | 0.00625 |
|---|---|---|---|---|---|---|
| A: `K` | 4 | 5 | 6 | 6 | 7 | 8 |
| B: `K` | 8 | 15 | 28 | 54 | 106 | 211 |

evaluations: `K = log₂(1/η) + O(1)` for A and `K ≈ 1.3/η` for B.  *Mechanism.*  In normal form
the half-line right of `c` has rightward cost density `η` and leftward density `2−η`: the hub `c`
almost dominates everything to its right (`σ(c,t) = ηt ≤ gap^d(c)`), but the lower bound is lowest
at the far end, so the search starts there and walks back towards `c` — in A the lower bound
`max(G − D − ηt, G + (2−η)t − p)` left of the last evaluated point `p` is minimal at `t ≈ (p−D)/2`,
so the distance to `c` is halved at every step; in B the same computation gives steps of length
`D`.  *Consequences.*  (1) The one-dimensional theorem `n_PY ≤ 4 n_B + 1` of Hansen–Jaumard–Lu
does not survive a known part.  D30 showed only that the *comparison class* of Theorem 11.11
degenerates on the line; here the *algorithm* does, already for `g ≡ 0`.  (Control, `t5e`: with
`f ≡ 0` on the line, random and hill-climbing search never exceeded `K = 4 N_cov + 1`.)  (2) Both
theorems are consistent with this (`t11`): for A, the shrunk client covers of 11.11 have 6, 6, 8, 9
points for `η = 0.2, …, 0.025`; for B, `κ = 1` and `λ = 1−η`, so 11.11 does not apply and C4 allows
`≈ 6.7/η`.  (3) Even on the line a hub
exists as soon as the residual is extremal: the apex of a tent `g = −|x−p|` covers everything at
zero slack (hill-climbing over instances with a known part found `N_cov = 1`, `K = 8`).

**Best-first search on the binary product landscape [T: `t6`, `t6b`–`t6e`].**
`X = {0,1}ⁿ`, `f = e|x|`, `d = c·`Hamming, `g ≡ 0`, `ρ = e/c`, `ε = 0`; `a` covers `y` iff
`d_H(a,y) ≤ ρ|y|`.  Evaluations of best-first search (random tie-breaking) against the greedy
cover computed with full knowledge of `g` (Walsh–Hadamard convolutions) and the layer lower bound
`max_μ L_μ ≤ N_frac`:

| `ρ = 1/2`, `n` | 10 | 12 | 14 | 16 | 18 | 20 | 22 |
|---|---|---|---|---|---|---|---|
| best-first `K` | 71–78 | 148 | 251 | 482 | 869 | 1617 | 2828 |
| greedy cover | 53 | 105 | 191 | 336 | 596 | – | – |
| lower bound | 15 | 22 | 36.4 | 56 | 81.6 | 138.4 | 209 |
| `e^{nR*}` | 6.6 | 9.6 | 14.0 | 20.3 | 29.6 | 43.1 | 62.8 |

(`ρ = 1/4`: `K = 419, 972, 2580, 6799` against greedy `283, 681, 1703, –` for `n = 10…16`;
`ρ = 3/4`: `K = 48, 81, 116, 183, 245, 371` for `n = 10…20` against greedy `21, 31, 43, 65` for
`n = 10…16`; exact `N_cov = 6, 13, 23` (ILP) for `n = 4, 6, 8` at `ρ = 1/2`, where
`K = 12, 19, 36–52`; index-order tie-breaking is worse: `K = 756` at `n = 16`.)  So for `n ≤ 22`
best-first search is within a factor `1.3–1.5` (`ρ ≤ 1/2`) to `2.3–2.8` (`ρ = 3/4`, slowly growing)
of a cover built with knowledge of the residual.  Best-first search and the greedy cover both
grow at about `0.3` nats per site in this range, the lower bound at `0.22`, and `R* = 0.188`: the
asymptotic regime is not visible.  *Rigorous bracket for the exponent of best-first search*
**[R]**: its points in the layer `|y| = μn` form a constant-weight code of minimum distance
`≥ ρμn` (separation (b)), so by sphere packing inside the layer

    R*  ≤  exponent(best-first)  ≤  max_μ [h(μ) − μ h(ρ/4) − (1−μ) h(ρμ/(4(1−μ)))]

= `[0.188, 0.355]` at `ρ = 1/2` (`[0.351, 0.476]` at `1/4`, `[0.080, 0.270]` at `3/4`).  Whether
best-first search attains `R*` is open, and it is a question about greedy codes: its evaluated
set is a maximal "one-sided packing" (`d_H(y_j,y_k) > ρ|y_k|` for `j<k`), and the asymptotic size
of greedy maximal codes is not known even for the cube.  (An in-layer Gilbert–Varshamov count
would give `0.207 > R*`, but lower layers also cover; I could not make that computation
rigorous.)

**Exploratory: selection by elimination power [T: `t12`, `t12b`; no theorem].**  Hetland's "oracle
AESA" selects the pivot that eliminates most; without an oracle one can plug in a model.  Rule
*CC* ("central cover"): pretend that the residual is the centre `(L_A + U_A)/2` of the consistent
set, evaluate the point whose ball for that model (with `E*` replaced by the incumbent) contains
the most uncertified points, and re-plan after every evaluation; it stops when the certificate
closes, so it is a correct algorithm.  (Using the *upper* end `U_A` instead of the centre is
useless: every point could be a hub, all scores tie, and the rule degenerates to best-first.)
Mean numbers of evaluations:

| family | best-first | CC | alternating the two | `N_cov` |
|---|---|---|---|---|
| hub family, `N` = 20 shallow, `M` = 1 / 5 / 40 hubs | 21 / 21 / 21 | **2 / 7** / 42 | – | 2 |
| line family A (C5), `η` = 0.1 … 0.00625 | 5 … 8 | **2** | – | 2 |
| line family B (C5), `η` = 0.1 … 0.00625 | 15 … 211 | **3** | – | 1 |
| `{0,1}⁸`, additive `f`, additive `g`, `κ` = 0 / 0.5 / 1 | 45.4 / 41.0 / 33.9 | **25.0 / 26.3 / 28.6** | 28.4 / 28.3 / 29.1 | 20.3 / 20.0 / 19.9 |
| `{0,1}¹⁰`, same | 66.0 / 62.5 / 68.7 | **45.3 / 44.8 / 63.2** | 50.0 / 47.7 / 62.3 | – |
| line, 60 points, `(κ,λ)` = (0.5, 0) / (0, 0.5) / (1, 0.9) | **14.2 / 14.9 / 9.0** | 14.7 / 20.6 / 11.7 | 14.2 / 14.3 / 9.2 | 10.9 / 11.9 / 5.8 |
| grid 8×8, `(κ,λ)` = (0.5, 0) / (1, 0) / (0.5, 0.5) | **25.8 / 16.6 / 19.7** | 28.5 / 20.6 / 26.1 | 24.7 / 17.6 / 19.2 | 17.3 / 8.0 / 13.9 |
| random metric spaces, `\|X\| ≤ 12` | 4.03 | 4.05 | – | 3.50 (`N_value`) |

So the rule finds the hubs of C5 and, on additive product landscapes, uses 55–72 % of the
evaluations of best-first search for `κ ≤ 0.5` (84–92 % for `κ = 1`), within a factor 1.25–1.45 of
`N_cov` at `n = 8`, where best-first is at 1.7–2.2.  It pays `M + 2` on the hub family (bad when
hubs outnumber shallow states — no algorithm avoids `min(M,N)+1`), and it is *worse* than
best-first on unstructured line and grid instances; alternating the two rules stayed within
about 15 % of the better one in these tests.
On the zero-residual product landscape the centre of the bracket is the truth (the envelope is
symmetric and `g ≡ 0`), so there CC is the greedy cover; the gain persists for `κ = 0.5`.  This is
evidence that optimism is the wrong selection principle on product landscapes, not a result.

### 2.4 Dictionary II — discrete weak KAM, Aubry–Mather, tropical spectral theory

With the cost `c(y,x) := d(x,y)` and the Lax–Oleinik operators `T⁻u(x) = min_y[u(y) + c(y,x)]`,
`T⁺u(y) = max_a[u(a) − c(y,a)]`:

| certification | weak KAM / max-plus | status |
|---|---|---|
| admissible `g` | dominated function (critical sub-solution); eigenvector of the Kleene star | literal |
| — | critical value `0` (zero diagonal), Mañé potential = Peierls barrier = `d`, **Aubry set = X**, every sub-solution is a weak KAM solution of both signs | literal, **degenerate** |
| `κ < 1` | strict sub-solution (Zavidovique) | literal |
| zero-slack pair `s(a,y) = 0` | calibrated pair; tropical type / covector of `g` (Develin–Sturmfels); tight graph (Gordon–Petrov) | literal |
| `U_A`, `L_A` | `T⁻`, `T⁺` applied to the data (Hopf–Lax); min-plus / max-plus combinations of Kleene-star columns | literal |
| `U_A − L_A = s(·,A) + s(A,·)` | barrier of the conjugate pair `(U_A, L_A)`; shortest cycle through `x` and the data node in the conditional envelope `D_A` | literal (C6) |
| determined set `{U_A = L_A}` | static class of the data node = Aubry set of the conditioned system | literal (C6) |
| irreducible asymmetry `ι` (C1e) | maximum cycle mean = critical value of the antisymmetric part | literal |
| sharpness threshold of a chain (C7) | minimum cycle ratio = generalised tropical eigenvalue | literal |
| `g ↦ min(f+g)` | tropical linear functional with representing vector `f` (C8) | literal |
| every admissible `g` is a min-plus combination of the columns `d(·,x)` | max-plus Martin / horofunction representation (Akian–Gaubert–Walsh) | literal, trivial for finite `X` |

**Proposition C6 (calibration order; exact uniqueness sets) [R, K in substance; T: `t2`, `t10`].**
`a ⪯_g y :⟺ s(a,y) = 0` is a preorder (a partial order if `d(x,y) + d(y,x) > 0` for `x ≠ y`).
(i) `L_A = g` exactly on the down-set `{y : ∃a∈A, a ⪯ y}` and `U_A = g` exactly on the up-set
`{y : ∃a∈A, y ⪯ a}`: *an evaluation determines the residual downstream of it* (downstream = along
steepest descent of `g`) — the geometric content of "high points are hubs, and best-first search
climbs from the wrong end".  (ii) `g` is the only admissible function with the values `g|_A` iff
`A ⊇ Min(⪯_g) ∪ Max(⪯_g)`; this is the unique minimal uniqueness set, the unique minimal exact
(`ε = 0`) certificate of `ln Z` at every `β > 0`, and the minimal set that certifies every
topical functional exactly.  It is all of `X` iff no envelope inequality is tight (`κ < 1`),
which is `exact_free_energy_certificate_eq_univ`.  (iii) For the minimum at `ε = 0`: every
minimiser must have an evaluated point upstream of it; if `κ < 1` every minimiser is forced.
(iv) After conditioning on `A` the uncertainty width `U_A(x) − L_A(x)` is the length of the
shortest cycle through `x` and the data node in `D_A`; it vanishes exactly on the determined
set, which is therefore the static class of the data node: the conditioned system has a
non-trivial Aubry set although `d` does not.  *Proof.*  `L_A(y) = g(y) − s(A,y)`, `U_A(y) = g(y) +
s(y,A)`; a finite poset has a minimal element below and a maximal element above every point. ∎
(Checked exhaustively over all `A` on 400 instances.)

**Proposition C7 (sharpness threshold of a chain = minimum cycle ratio) [R; overlaps workstream B;
T: `t7`].**  Ring of `n` sites, `f(x) = Σ_i φ(x_i) + ψ(x_i,x_{i+1})`, envelope `c·`Hamming, and
suppose the uniform configuration `0ⁿ` is a ground state for every `n` (the loop at `0` is a
minimum-mean cycle of `w = ψ + φ`).  With `W(a,b) = w(a,b) − w(0,0)` and `T(a,b) = [b ≠ 0]`:
the single evaluation at `0ⁿ` is an exact certificate (Theorem 11.7) iff

    c ≤ c*(n) := min over closed walks of length n, not identically 0, of W/T,   and   inf_n c*(n) = c*,

`c*` the minimum cycle ratio of `(W,T)` over elementary cycles with `T > 0`, equivalently the
largest `λ` for which `u(b) − u(a) ≤ W(a,b) − λT(a,b)` has a solution `u` (a tropical
eigenvector); `c*(n) = c*` whenever `n` is a multiple of the length of an optimal cycle.
*Example:* Ising ring, `ψ = −J s s'`, `φ = −h s`, `J, h > 0`: `c* = 2h` for every `J` (the optimal
cycle is the loop at `−`: an all-minus domain), while a single flip costs `4J + 2h`.
*Reading:* with interactions the envelope constant must be below the energy *per excited site* of
the cheapest competing periodic phase, not below single-site excitation energies; a strong
coupling does not make a chain sharp.  (267 random instances with `k ≤ 3` states and `n ≤ 7`:
`c*(n) ≥ c*` always, equality in 1280 of 1340 cases; 4020 certificate checks.)  *Proof.*  The
sharp-minimum condition `c·d_H(0ⁿ,y) ≤ f(y) − f(0ⁿ)` reads `W(y) ≥ c·T(y)` for the closed walk
`y`; closed walks decompose into elementary cycles. ∎

**Proposition C8 (tropical linearity is why single dips are extremal) [R; T: `t2`, `t8`].**
(i) The functionals that are min-plus linear (`Φ(min(h,h')) = min(Φh, Φh')`, `Φ(h+c) = Φh + c`)
are exactly `Φ(h) = min_x[w(x) + h(x)]` **[K]**: *minimisation with a known part is the general
tropical linear functional*, and the known part is its representing vector.  (ii) For every `A`,
with `δ_y^A := min(g, L_A(y) + d(·,y))` the deepest single dip at `y` consistent with the data,
`L_A = min_y δ_y^A` pointwise.  Hence for tropical linear `Φ`, `Φ(L_A) = min_y Φ(δ_y^A)`: the
worst consistent residual is a single dip, and "certificates are coverings" follows.
(iii) At finite temperature `Z(f+·)` is linear over the *deformed* semiring `(⊕_β, +)`, but `L_A`
is the `⊕_∞`-sum of the dips, not their `⊕_β`-sum:

    max_y [Z(f+δ_y^A) − Z]  ≤  Z(f+L_A) − Z  ≤  Σ_y [Z(f+δ_y^A) − Z],

both inequalities strict in general (the single-dip value of the soft-min differs from the true
one in 442 of 600 random instances; ratios up to 3.2 on eight points).  The sum on the right has
up to `|X|` terms; on a type class of a product space that is a factor `e^{nH(P)}`.  This
counting factor is the origin of the entropy term in the deterministic budget
`KL(P‖π) = E_P[−ln π] − H(P)` of §11.10 (the lower envelope dips at all points of a type class at
once) and the reason single dips can fail to be extremal at the exponential scale (D34).
*Idempotency (`Σ = max`) is the property that makes the zero-temperature theory a covering
theory.*

### 2.5 Dictionary III — optimal transport, tight spans, Funk geometry

All of the following are identities **[R; T: `t2`, `t8`, `t10`]**; none produced a new theorem.

* **Kantorovich.**  For any coupling `γ` of `(μ, ν)`: `⟨γ, s⟩ = ⟨γ, d⟩ − μ(g) + ν(g)`; hence
  `W_s(μ,ν) = W_d(μ,ν) − μ(g) + ν(g)` — *transport cost in the slack is the duality gap of `g` as a
  Kantorovich potential*, zero iff `g` is optimal for `(μ,ν)`.  Theorem 11.13(a) says that a
  free-energy certificate is a quantiser of the Gibbs measure in `W_s`.
* **Gromov product / horofunctions.**  If `g = d(·,t)` (or a Busemann-type limit; every
  admissible `g` is one after adding a constant), `s(a,y) = d(a,y) + d(y,t) − d(a,t)` is twice the
  Gromov product of `a` and `t` based at `y`; on a tree, `s(a,y) = 2·dist(y, path[a,t])`: an
  evaluation covers a tubular neighbourhood of its descent path.
* **Tropical Funk metric.**  With `δ(h,h') = max(h−h')`: `g(x) = δ(g, d(·,x))` (Yoneda), and
  `s(a,y) = δ(U_y, U_a)` where `U_a = g(a) + d(·,a)` is the one-point upper envelope: *`(X,s)`
  embeds isometrically, by `a ↦ U_a`, into the admissible class with the tropical Funk metric* —
  and `U_y` is the landscape in the definition of the soft gap.
* **Topical functionals.**  Every monotone, additively homogeneous `Φ` (min, max, order
  statistics, free energies at any `β`, CVaR) is `δ`-nonexpansive (Crandall–Tartar), so
  `Φ(f+L_A) ≤ Φ(f+g) ≤ Φ(f+U_A)` with width `≤ max_x[s(x,A) + s(A,x)]`, and `A` certifies *all*
  topical functionals to `ε` iff `max_x[s(x,A) + s(A,x)] ≤ ε`.  One-line proofs of two facts of
  §11.10: `Λ(y) − Λ(y') ≤ β s(y',y)` (because `U_y − U_{y'} ≤ s(y',y)`), and `Λ(y)/β = E^{d,β}(y) −
  F`, where `E^{d,β} = f^{d,β} + g` with the *soft* Pasch–Hausdorff envelope
  `f^{d,β}(y) = −β⁻¹ ln Σ_a e^{−β(f(a)+d(a,y))}`: **the soft gap is the gap of the thermally
  regularised energy above the free energy**; `E^{d,β}` is admissible for the thermal reduced
  envelope `σ_β = d^{f^{d,β}} ≥ 0`, and the dip lower bound of Theorem 11.24 is the centre-radius
  covering problem with balls `B_{σ_β}(a, E^{d,β}(a) − F + ε/β)` — the same form as at zero
  temperature with `(σ, E^d, E*)` replaced by `(σ_β, E^{d,β}, F)`.  (There is no exact
  finite-temperature normal form: `Z(f^{d,β}+g) ≠ Z(f+g)`.)
* **Funk metric of the polytrope as a convex body.**  Its facet functionals evaluated at `g` are
  the slacks, so `F(g,h) = ln max s_g/s_h`.  Then `F(0,g) = −ln(1−κ(g))` — *`κ`-Lipschitz
  residuals are a Funk ball around the zero residual* — and for symmetric `d` the quasi-symmetry
  constant of the slack in Theorem 11.11 is `e^{F(g,−g)}`.
* **Tight span — only a neighbour.**  The admissible class modulo constants is the min-plus span
  of the columns of `+d` (the polytrope, full-dimensional).  Isbell's tight span is built from
  the tropical polytope generated by `−d` (Develin–Sturmfels; for directed distances
  Hirai–Koichi; as an Isbell completion, Willerton — all three known to me from abstracts and
  summaries only), a different object; it is not translation invariant, while everything in the
  certification problem is.  The tight span would become relevant only if residuals were known
  to be Katětov functions (`g(x) + g(y) ≥ d(x,y)`, the nearest-neighbour-search class of
  AESA/Hetland), which is a certification problem on a doubled space with a signed envelope.

### 2.6 What is only analogy (plainly)

1. The A\* *algorithm* is not best-first certification: an expansion reveals arcs, an evaluation
   reveals a potential value.  What is shared is the potential theory, the adversary and the
   optimality hierarchy.
2. Weak KAM / Aubry–Mather theory of the envelope is the trivial case of that theory; statements
   about Aubry sets, Peierls barriers and static classes of `d` itself are vacuous.  Tropical
   rank is an invariant of `d`, not of the instance, and says nothing about certificates.
3. Optimal transport contributes vocabulary (duality gap, quantisation) and no theorem.
4. Tight spans / injective hulls: neighbouring object, not the admissible class.
5. The "NBS analogue" (evaluate all possible coverers of the most optimistic point; cost at most
   the coverage ambiguity times `N_cov`, plus the search for an upper bound) is a heuristic
   remark; I did not prove a clean statement, because the tie plateau is not controlled by
   `N_cov`.

---

## 3. Numerics (own code; `python3 <script>` in the directory)

| script | what | size | result |
|---|---|---|---|
| `t1_normal_form.py` | C1(a)–(c): widths, covers, `N_cov`/`N_value`/`N_point`, trajectories | 1200 instances, `\|X\| ≤ 7`, all subsets | all identities hold (max error `2·10⁻¹⁵`); raw gap not slack-Lipschitz in 897 = number with `f ≠ f^d`; raw and regularised trajectories differ (ties) in 46 |
| `t10_extras.py` | signed normal form, Johnson potential, contact points, Funk identities, uniqueness sets (exhaustive), product formula for `f^d` | 400 instances, 18 056 subsets | all hold |
| `t2_identities.py` | slack of a slack, Funk, Kantorovich (LP), calibration order, barrier, Kolmogorov, cycle mean (Karp vs LP), single dips, trees | 600 instances + 9206 tree triples | all hold; soft-min not dip-determined in 442/600 |
| `t3_dechter_pearl.py` | C3: type-3 construction, proper sub-certificates, triangle, explicit instances | 1200 instances, 2526 constructions | construction always works; proper sub-certificate in 185/1200; forced fraction 0.66; mean `K = 3.1` against `N_value = 2.8` |
| `t13_type3_adversaries.py` | C3(ii) against four concrete correct competitors (fixed priority, worst-first, upper-envelope-first, rule CC) | 12 000 (instance, competitor) pairs | in all 2318 cases where the competitor skips a `BF*` point, the instance of the proof makes it evaluate a point `BF*` skips (644 times case `j = 1`); the competitor's set is a proper subset of `BF*`'s in 278 cases |
| `t4_astar_alt.py` | C2: A\* on sparse digraphs against the uncovered set | 553 digraphs, 8–29 nodes | identical in every case |
| `t5_line.py`, `t5b_inspect.py`, `t5c_line_adversary.py` | line with a known part, random and hill-climbing | 6000 random instances, `\|X\| ≤ 60` | `K/N_cov` up to 8 (`N_cov = 1`, `N_point = 2`) |
| `t5d_line_family.py` | C5 families A, B | `\|X\|` up to 1674 | table in §2.3 |
| `t5e_line_f0.py` | control `f ≡ 0` | 3000 random + 8 hill-climbs | `K ≤ 4N_cov + 1` never violated |
| `t6_ps_product.py`, `t6b`–`t6e` | best-first on `{0,1}ⁿ`, greedy cover (WHT), ILP, exponents | `n ≤ 22` (`4·10⁶` states) | tables in §2.3 |
| `t12_coverage_first.py`, `t12b_central_cover.py` | elimination-power selection (exploratory) | 600 random instances; hub family; C5 families; 280 line, 160 grid, 54 product instances (`n = 8, 10`) | table in §2.3 |
| `t7_chain_sharpness.py` | C7 | 267 chains, rings `n ≤ 7`, 4020 certificate checks | holds; Ising `c* = 2h` |
| `t8_topical.py` | topical bounds, `Λ` Lipschitz, soft gap = `E^{d,β} − F`, idempotency defect | 800 instances | all hold |
| `t11_checks.py` | C1(e) inclusion; shrunk covers for the families of C5 | 200 quasi-metrics; `η ≥ 0.025` | holds; family A: shrunk client covers 6, 6, 8, 9 (`K` = 4, 5, 6, 6); family B: centre-form covers 35, 68, 134, 266 `≈ 6.7/η` (`K` = 8, 15, 28, 54) |
| `t9_centre_form.py`, `t9b_compare.py`, `t9c_compare_line.py` | C4 | 2515 instances (`\|X\| ≤ 11`), 225 line instances (`\|X\| = 60`) | no violation; equality in 251; violated at `3θ` (31) and `5θ` (401), never at `2θ` |
| `NormalForm.lean` | gauge lemma, slack invariance, slack of a slack, nonnegativity, regularisation, client = centre, gap Lipschitz, centre-form separation | 10 theorems, self-contained (`import Mathlib`) | compiles without errors or warnings (`lake env lean`, 22 s) |

Negative numerical findings: the centre-form and client-form bounds are both vacuous on small
random metric spaces (`t9b`); the exponent of best-first search on products cannot be read off
at `n ≤ 22`; hill-climbing alone did not find unbounded ratios on the line (the explicit
families did); a first version of the Funk identity had the wrong orientation
(`max_z[L_a − L_y] = s(y,a)`, not `s(a,y)`) and was caught by the test.

---

## 4. Prior art and search log

*Read in full or in the relevant part.*
* R. Dechter, J. Pearl, "Generalized best-first search strategies and the optimality of A\*",
  J. ACM 32 (1985) 505–536 — §4 read in full (PDF from the first author's page, text layer):
  dominance and the four optimality types (§4.2), Theorem 8 with the appended goal (Fig. 5),
  Fig. 6a/6b, Theorems 9–10, Corollaries 3–4, summary table (Fig. 9).
* K. Figueroa, E. Chávez, G. Navarro, R. Paredes, "Speeding up spatial approximation search in
  metric spaces", ACM J. Exp. Algorithmics 14 (2009) — §§1–3.1 read: AESA (Vidal 1986) eliminates
  with `D_∞(q,u) = max_p |d(u,p) − d(p,q)|` and selects the next pivot by the sum `D₁` of the lower
  bounds; `D_∞` is the other standard ordering; iAESA selects differently and needs as few as
  60 % of AESA's distance computations (so the optimistic rule is not the best in practice
  either).
* A. Goldberg, C. Harrelson, "Computing the shortest path: A\* search meets graph theory", SODA
  2005 — §§2, 5, 7 (text search of the PDF): reduced costs, feasibility, "A\* search is
  equivalent to Dijkstra's algorithm on the graph with length function `ℓ_{π_t}`", Lemma 2.1,
  landmark bounds, landmarks "behind" the destination.
* M. L. Hetland, "Optimal metric search is equivalent to the minimum dominating set problem",
  arXiv:2008.09607 (2020; DOI 10.1007/978-3-030-60936-8_9) — §§1–5 read (PDF text, kept in
  `refs_hetland/`).  §2 "Pivoting is, of course, optimal": the bracket
  `max_p |δ(q,p) − δ(p,x)| ≤ δ(q,x) ≤ min_p δ(q,p) + δ(p,x)`, Lemma 1 (both ends are attained by
  metrics), Corollaries 1–2 ("No search method can resolve a metric range [kNN] query with fewer
  distance computations than pivoting", by an adversary).  §3: eliminations by different pivots
  do not interact, so the least number of distance computations is the domination number of a
  directed *elimination graph* (Proposition 1); "in order to guarantee using at most `γ(G)`
  distance computations, you would need to somehow determine `G`".  §4, Theorem 1: reduction from
  dominating set with distances 0 / 1 / 2 and the query at distance 2 from everything (`k`-NN:
  one extra object at distance `r < 1` from the query), hence no approximation within
  `(1−ε) ln n`.  §5: greedy selection by elimination power is the best feasible strategy; AESA
  selects by closeness to the query instead, although "a pivot that is far away might be able to
  eliminate an entire nearby cluster" (the hub).  **This is the covering characterisation (G1),
  the hardness gadget (G5, Theorem 11.10), the exactness of the bracket (Theorem 2.5) and the
  instance-wise optimality of certificates (Theorem 11.23(a)) for `f ≡ 0`, symmetric `d` and the
  Katětov class, in the similarity-search literature.**  Not there: the slack quasi-metric, a
  known part, asymmetry, exponents, randomised bounds, the `+1` analysis.

*Abstracts / search summaries only.*
* J. Chen, R. Holte, S. Zilles, N. Sturtevant, "Front-to-end bidirectional heuristic search with
  near-optimal node expansions", arXiv:1703.03868 (IJCAI 2017); J. Eckerle et al., ICAPS 2017 —
  surely-expanded pairs, vertex-cover lower bound, NBS ≤ 2·VC, no admissible front-to-end
  algorithm better than 2·VC in the worst case.
* A. Felner, U. Zahavi, R. Holte, J. Schaeffer, N. Sturtevant, Z. Zhang, "Inconsistent
  heuristics in theory and practice", Artif. Intell. 175 (2011) — pathmax (Mérő 1984), BPMX.
* R. Bauer et al., "Preprocessing speed-up techniques is hard" (2010) — NP-hardness of landmark
  selection for ALT (secondary sources only).
* H. Hirai, S. Koichi, "On tight spans and tropical polytopes for directed distances", Ann.
  Comb. 16 (2012) 543–569; S. Willerton, "Tight spans, Isbell completions and semi-tropical
  modules", Theory Appl. Categ. 28 (2013) 696–732, arXiv:1302.4370.
* M. Zavidovique, "Strict sub-solutions and Mañé potential in discrete weak KAM theory",
  arXiv:0905.0615; E. Garibaldi, Ph. Thieullen, "Minimizing orbits in the discrete Aubry–Mather
  model"; M. Akian, S. Gaubert, C. Walsh, "The max-plus Martin boundary", Doc. Math. 14 (2009)
  195–240.
* C. Mustăţa, "On the approximation of the global extremum of a semi-Lipschitz function",
  Mediterr. J. Math. 6 (2009) 169–180: a Shubert-type sequential method on quasi-metric spaces —
  the best-first algorithm for asymmetric envelopes is in print (the repository's `prior_art/L4`
  lists "any treatment of asymmetric envelopes in certified Lipschitz optimisation" as not
  found); no certificates or complexity there as far as the summary shows.

*Cited from memory, not re-verified:* Johnson (1977); Karp (1978, minimum mean cycle);
Dantzig–Blattner–Rao (1967) and Lawler (1976, minimum cycle ratio); Kolmogorov's reversibility
criterion; Crandall–Tartar (1980) and Gunawardena–Keane (topical maps); Bernard–Buffoni (weak
KAM pairs and Kantorovich duality); Butkovič, *Max-linear Systems* (2010); Develin–Sturmfels
(2004); Isbell (1964), Dress (1984); Lawvere (1973); Vidal Ruiz (1986); Mérő (1984);
Hansen–Jaumard–Lu (1991, through the repository's `prior_art/L4`).

*Searches run* (web search): (1) Dechter–Pearl, optimality of A\*; (2) Eckerle et al., must-expand
pairs / NBS; (3) AESA pivot selection and optimality; (4) lower bounds on distance computations /
certificates for nearest-neighbour search [found Hetland]; (5) ALT landmarks, hardness of
landmark selection; (6) discrete weak KAM, Aubry set, Kleene star; (7) pathmax / BPMX; (8) tight
span, tropical polytope, directed tight span; (9) Willerton; (10) topical functions,
Crandall–Tartar, Funk; (11) Piyavskii–Shubert on quasi-metric / semi-Lipschitz spaces [found
Mustăţa]; (12) "grey-box" Lipschitz optimisation with a known additive part [nothing relevant];
(13) Bernard–Buffoni, Akian–Gaubert–Walsh.  One wrong arXiv number was tried for Willerton and
discarded.  *Not found:* the statement that a known additive part is the gradient part of an
asymmetric envelope (C1); a Dechter–Pearl-type classification for certified Lipschitz
optimisation (C3); the centre-form bound in a quasi-metric space (C4; for `f ≡ 0` and symmetric
`d` it is the folklore packing argument of Bouttier et al. / Bachoc et al. in dimension-free
form).  These searches were short; absence is weak evidence.

---

## 5. Not settled

1. The exponent of best-first search on product landscapes (bracket `[0.188, 0.355]` at `ρ = 1/2`).
2. On the line with a known part: is there a bound `K ≤ C(ρ_σ)·N_cov` with `C` logarithmic in the
   quasi-symmetry constant when `κ < 1` (family A suggests a logarithm; family B shows that with
   `κ = 1` it is at least linear)?
3. Tight constants in C4 (`θ = 1/(2ρ+3)`; no violation at `2θ`), and a common generalisation of
   C4 and Theorem 11.11.
4. The converse of C8(i)–(ii): is every topical functional whose certificates are determined by
   single dips on all instances tropical linear?  (Expected; not proved.)
5. A clean statement for the "evaluate all possible coverers" algorithm (the analogue of NBS), and
   any guarantee for the rule CC of §2.3 or for its alternation with best-first search.
6. Whether the type-3 statement can be upgraded to a quantitative one on an instance class that
   plays the role of Dechter–Pearl's consistent, non-pathological instances (information local:
   every best-first point forced).  I found no natural such class other than trivial ones.
7. C7 for open chains (boundary excursions have one domain wall), non-uniform ground states and
   site-dependent constants (a non-autonomous min-plus product); the exponent above the
   threshold is workstream B's question.
8. I did not read the full texts of the bidirectional-search papers (abstracts only), nor Vidal's
   original AESA paper (described through Figueroa et al. and Hetland).

---

## 6. Three most promising next steps

1. **Rewrite §11 in normal form** (and add the lemmas of `NormalForm.lean` to the development):
   state the covering theorem, the exchange lemma, the dichotomy and both best-first bounds for
   `f ≡ 0` with a possibly asymmetric (signed, then Johnson-normalised) envelope.  This removes
   the point/value distinction, turns "known part" and "asymmetric envelope" into one feature,
   explains D30, and positions the cluster against Hetland (2020), AESA and landmark heuristics —
   literatures with which the repository has not yet been compared, and where G1, G5 and
   11.23(a) are partly in print.
2. **Search beyond optimism.**  C3 and C5 say that optimism alone is only type-3 optimal and can
   be arbitrarily bad; the normal form and Hetland's elimination graph say what is missing:
   *dominance / elimination power*.  The exploratory rule CC of §2.3 (greedy cover for the central
   interpolant, re-planned after each evaluation — "learn-then-cover" without any structural
   assumption) already beats best-first search on additive product landscapes and on the families
   of C5, and loses on unstructured instances.  Worth doing: a guarantee for the alternation of
   the two rules (e.g. in terms of `ρ_σ`, logarithmic rather than linear), its exponent on product
   landscapes against `R*`, and the exponent of best-first search itself (a greedy-code question;
   simulation with symmetry reduction beyond `n = 22`).
3. **Chains through the tropical normal form.**  C7 gives the sharpness threshold as a minimum
   cycle ratio; the same eigenvector `u` gives reduced pair energies `W − c*T − δu ≥ 0`, so the
   gap of a chain is a sum of nonnegative local terms vanishing on the Aubry graph.  With
   workstream B: use this as the "credit" in a Markov-type covering argument for the exponent
   above the threshold, and extend C7 to open boundaries and heterogeneous sites.
