# Workstream D — free-energy estimation in statistical mechanics; other observables; continuous spaces; structured classes

Directory: `<session scratch>/ws/D/`
(all scripts `s*.py`, outputs `out/*.txt`, scratch Lean files `lean/*.lean` and the literature
extract `lit/` referred to below are in this directory).  Nothing in the repository was
modified; it was read at the state of 2026-11-24 ≈19:15 UTC and again ≈21:00 UTC (it was being
edited by others in between).

Status labels.  **[K]** known (cited); **[R]** routine consequence of known tools; **[N]**
apparently new (not found in the searches of §4); **[P]** paper proof by me, not refereed;
**[V\*]** machine-checked in a scratch file of this directory (`lake env lean`, standard axioms
only; not part of the repository); **[num]** numerical evidence only.

**Overlap with workstream A (seen only at ≈21:00 UTC, after my own derivations were
finished).**  Sections 2.1–2.3 (generalised dips, failure of the single-dip conjecture for sites
with more than two states, the game-value threshold with the two-reference verifier) were
obtained here independently and coincide with workstream A's generalised dips and its Theorem B
as quoted in `docs/THEORY_REPORT.md` (revision ≈21:00).  They are *independent confirmations*,
not new results of this workstream; my own code reproduces every number quoted there from A
(`s12`, `s07`, `s10`).  What this workstream adds to that part is listed at the end of §2.3.
Everything in §§2.4–2.6 (continuous spaces, other observables, structured classes) and the
positioning of §4 is specific to this workstream.

---

## 1. Verdicts

*Positioning.*  The qualitative picture — randomisation helps for `ln Z` only above an accuracy
scale; lower bounds by hiding a bump — is in print for smoothness classes in fixed dimension
(Holzmüller–Bach 2025, read in the primary source: their Proposition 9 is exactly "optimisation
lower bound minus the soft gap `d·ln(1+3B)`"), and the physics literature knows the *estimator
side* (Jarzynski 2006; Chatterjee–Diaconis 2018: cost `≈ e^{β·dissipated work}` of sampling the
dominant region).  I found no minimax or instance-wise statement of the threshold, of the soft
gap, or of the results below.  The soft gap has a physical reading but no standard name:
`Λ(y)/β` is the Zwanzig/Widom perturbation free energy of replacing the residual by its
pessimistic cone at `y`; the general object is the **pointwise dissipated work**
`βW_diss = ln(π_g/π_g̃)` of switching the instance `g` to an admissible competitor `g̃`, and the
lower bounds say: *every algorithm must probe, for every admissible competitor, a configuration
where that switch dissipates less than `ε/β`* (§2.1; machine-checked in scratch).
*Generalisations.*  (i) The accuracy threshold is the value of a zero-sum game — the verifier
chooses a sampling law `Q`, the adversary a competitor, payoff the mean dissipated work under
`Q`; its upper half holds on **every finite instance**, on product landscapes it tensorises and
is sharp, and on every *homogeneous* product space (cube, `k`-state sites, cycles, circles) it
equals the Laplace functional of the site and needs no hint (§2.2) [product part independently
also workstream A].  (ii) **Continuous spaces**: on a torus of `n` torsion angles with an
`ℓ₁`-geodesic-Lipschitz residual the threshold is exactly `Σ_i ln(sinh b_i/b_i)`,
`b_i = βL_iπ/2`; in fixed dimension `d` the cost is of order `(βL/ln βL)^d` (order known from
Holzmüller–Bach; here instance-wise with constants); for one global `ℓ₂` Lipschitz constant in
high dimension everything is dimension-free, `exp(Θ(β²L²))` (§2.4).  (iii) **Other
observables**: free-energy differences between uncoupled macrostates have threshold
`V_A + V_B` (no cancellation), and certifying a ranking is cheap iff the free-energy margin
exceeds the game value of the *loser*; Boltzmann averages are much harder than `ln Z`: for the
magnetisation on the cube every algorithm is exponential below a level that is more than `70 %` of the
a-priori half-range (through dips centred on *type classes*; single dips give only `O(u²)`), and a
bounded number of samples suffices above a level that is within `1 %` of that bound for
`βc ≥ 6` (§2.5).  (iv) **Structure and staged protocols**: on the first-order class staging
cannot help (it is an adaptive algorithm; the class is a lattice, which is exactly what makes
hidden perturbations possible).  For the class with dense mixed second differences `≤ c₂`,
`w = βc₂n`, there is **a sharp dichotomy at `w = 4`**: for `w ≤ 4` (Dobrushin uniqueness for the
whole class) star + annealed Glauber sampling estimates `ln Z` to any accuracy with
polynomially many evaluations; for `w > 4` every algorithm needs exponentially many evaluations
for accuracies below `n·f_CW(w)`, the Curie–Weiss free energy, because of parabolic "droplets"
(§2.6).
*Negative.*  Single dips are not extremal on product spaces with `≥ 3`-state sites
(independently of A); for Boltzmann averages they are not extremal even on the binary cube;
type-class dips do **not** improve the `ln Z` bounds on biased binary instances (33 parameter
sets) — consistent with A's claim that single dips are extremal for two-state sites; the generic
soft-gap sampler is exponentially wasteful in homogeneous high-dimensional spaces; for a
Boltzmann average nothing like the precision available for `ln Z` is reachable.

---

## 2. Statements, proofs, counterexamples

### 2.0 Conventions

`X` finite (or compact, §2.4); `E = f + g`; class `𝒢 = {g : g(x) − g(y) ≤ d(x,y)}`; slack
`s(a,y) = d(a,y) − g(a) + g(y)`; `π_g ∝ e^{−β(f+g)}`; `Z(g) = Σ e^{−β(f+g)}`.  As in the theory
report an algorithm is `(ε/2, δ)`-correct for `Φ` if `|output − Φ(g)| ≤ ε/2` with probability
`≥ 1−δ` on every member of the class; `ε` is a width.  For Boltzmann averages I write `η` for the
half-width.  `Q(g)` is the (random) set of points queried on the instance `g`.  I use the
detection principle of Theorem 11.22 and its pair version (`prob_query_ne_pair`,
`QueryRefinements.lean`, third referee): if `g₁, g₂ ∈ 𝒢` have `|Φ(g₁) − Φ(g₂)| > ε`, the run on `g`
hits `{g₁ ≠ g} ∪ {g₂ ≠ g}` with probability `≥ 1 − 2δ`.

### 2.1 Competitors, comparison dips, and the lattice property

`𝒢` is closed under pointwise minima, maxima and the addition of constants (a polytrope)
**[K]**.  This is the only property of the first-order class that the lower bounds use.

**Lemma 1 (comparison dips) [V\*, `lean/ComparisonDip.lean`; R].**  Let `g, g̃ ∈ 𝒢`, `C ∈ ℝ`,
`g' = min(g, g̃ − C)`.  Then `g' ∈ 𝒢`; `g'(a) = g(a)` wherever `g̃(a) − g(a) ≥ C`; and
`ln Z(g') ≥ βC + ln Z(g̃)` (`cmpDip_admissible`, `cmpDip_eq_of_le`, `log_sum_exp_cmpDip_ge`).
Hence, for `β ≥ 0`: if a randomised algorithm is `(ε/2, δ)`-correct for `ln Z` on `𝒢`, then on
every instance `g`, for every competitor `g̃ ∈ 𝒢` and every `C` with
`ln Z(g) − ln Z(g̃) + ε < βC`,

    P( ∃ a ∈ Q(g) : g̃(a) − g(a) < C )  ≥  1 − 2δ

(`thermal_prob_hit_competitor`; deterministic version `thermal_queries_hit_competitor`).

*Reading.*  Put `ℓ_g̃(a) := ln(π_g(a)/π_g̃(a)) = β(g̃(a) − g(a)) − [ln Z(g) − ln Z(g̃)]`.  With `C`
just above the bound the condition `g̃(a) − g(a) < C` is `ℓ_g̃(a) < ε`:

> **for every admissible competitor `g̃`, the queries on the instance `g` must hit the dominance
> set `S_ε(g̃) = {a : π_g̃(a) > e^{−ε}π_g(a)}` with probability `≥ 1 − 2δ`.**

In the language of work relations, `W = g̃ − g` is the work of switching `g → g̃`
instantaneously, `ΔF = −β⁻¹ln(Z(g̃)/Z(g))`, and `ℓ_g̃ = β(W − ΔF)` is `β` times the **dissipated
work** at the configuration `a` (Crooks).  `E_{π_g}ℓ_g̃ = KL(π_g‖π_g̃) ≥ 0` is the second law; the
dominance set consists of the configurations at which the switch dissipates less than `ε/β` —
the "dominant realisations" of the exponential average in Jarzynski (2006).

*Special cases.*  (a) `g̃ = U_y = g(y) + d(·,y)`: the dip of the theory report;
`ln Z(g) − ln Z(U_y) = Λ(y)`, `g̃ − g = s(·,y)`: Theorem 11.24(a,b).  (b) `g̃ = U_T`, the upper
McShane envelope of the values of `g` on a set `T`: the **set dip** `g − (C − s(·,T))₊`, with the
**set soft gap** `Λ(T) = ln Z(g) − ln Z(f+U_T) = −ln E_π e^{−βs(·,T)}` — the pessimistic
half-width of the certificate `T` (`Zlo_eq`); queries must reach within slack `(Λ(T)+ε)/β` of `T`
**[V\*, `lean/SetDip.lean`: `setDip_admissible`, `setDip_eq_sub`, `log_sum_exp_setDip_ge`,
`thermal_queries_cover_set`, `thermal_prob_cover_set`]**.  (c) On a product landscape,
`g̃ = g + Σ_iφ_i(x_i)` with `φ_i(a) − φ_i(b) ≤ s_i(a,b)`: the truncated additive tilt
`g − (C − Σ_iφ_i(x_i))₊` (the "generalised dip" of workstream A; note
`g + Φ ∈ 𝒢 ⇔ Φ(x) − Φ(y) ≤ s(x,y)`).

**Corollary 1' (packing form) [R].**  For any probability `P` on competitors and `ε' > ε`,
`(1 − 2δ) ≤ E|Q(g)| · max_a P_{g̃∼P}(ℓ_g̃(a) < ε')`, and for `t ≥ 0`
`(1−2δ) ≤ E|Q(g)| · e^{tε'} max_a E_{g̃∼P}e^{−tℓ_g̃(a)}`.

*Why other classes behave differently.*  Second-order and few-body classes are **not** closed
under minima, so a competitor cannot be spliced in locally; localised alternatives have to be
built by hand and may not exist (§2.6).

### 2.2 The threshold of an instance is a game value

For an instance `g` define

    K_g(Q) = max_{g̃ ∈ 𝒢} E_Q[ln π_g − ln π_g̃] = max_g̃ { βE_Q(g̃ − g) − [ln Z(g) − ln Z(g̃)] },
    V(g)  = min_Q K_g(Q) = max_P min_a E_{g̃∼P} ℓ_g̃(a),          J(g) = K_g(π_g) = max_g̃ KL(π_g‖π_g̃).

(`Q` ranges over probability vectors on `X`, `P` over finitely supported laws on `𝒢`; the payoff
is convex in `g̃` and invariant under constants, so the maximum is attained at vertices of the
polytrope and von Neumann's theorem applies.)  `0 ≤ V(g) ≤ J(g)`; `J` is the largest Jensen gap
relative to the instance's own ensemble.  In words: *the verifier chooses a sampling ensemble,
the adversary a competitor, and the payoff is the mean dissipated work.*

**Theorem 2 (upper half, every finite instance) [P; N in this generality].**  Let `g ∈ 𝒢` be
given as a hint, `S = max_{x,y}s(x,y)`, `Q*` a minimiser of `K_g`, `ε > V(g)`.  Draw
`N ≥ 4βS ln(1/δ)/(ε − V(g))` independent points from `½π_g + ½Q*` and evaluate the true residual
there; if all values agree with the hint return `ln Z(g) + V(g)/2`, otherwise evaluate
everything.  This algorithm is `(ε/2, δ)`-correct on all of `𝒢` and makes `N` evaluations on the
hint.

*Proof.*  Let `g' ∈ 𝒢`, `h = g − g'`, `D = {h ≠ 0}`.  If `D = X` the first sample detects.
Otherwise fix `x₀ ∉ D`; admissibility of `g'` gives `−s(x,x₀) ≤ h(x) ≤ s(x₀,x)`, so `|h| ≤ S`.
By the definition of `K_g(Q*)` with `g̃ = g'`:
`ln Z(g') − ln Z(g) ≤ βE_{Q*}h + V(g) ≤ βS·Q*(D) + V(g)`; by Jensen
`ln Z(g') − ln Z(g) = ln E_{π_g}e^{βh} ≥ βE_{π_g}h ≥ −βS·π_g(D)`.  Put `θ = (ε − V)/(2βS)`.  If
`π_g(D) ≤ θ` and `Q*(D) ≤ θ` the returned value is within `V/2 + βSθ = ε/2`; otherwise `D` has
probability `> θ/2` under the sampling law and is missed with probability `≤ (1−θ/2)^N ≤ δ`. ∎
(Checked exhaustively over all 1 680 supports of eight 2-site products and on 360 alternatives
on 14 heterogeneous binary sites: `s08` (C), `s08c`.)

**Theorem 3 (product landscapes) [P; independently workstream A, Theorem B].**  Let `X = ∏σ_i`,
`f, g` additive, `π_g = ⊗π_i`, `s = Σs_i`.  For site `i` let
`Φ_i = {φ : φ(a) − φ(b) ≤ s_i(a,b)}`, `Λ_i(φ) = −ln E_{π_i}e^{−βφ}`,
`K_i(Q) = max_{φ∈Φ_i}[βE_Qφ − Λ_i(φ)]`, `V_i = min_Q K_i(Q)`.
(a) *Two-reference inequality*: for every product law `Q = ⊗Q_i` and every `g' ∈ 𝒢`,
`ln Z(g') − ln Z(g) ≤ βE_Q(g − g') + Σ_iK_i(Q_i)`; hence `V(g) = Σ_iV_i`, attained by `Q* = ⊗Q_i*`.
(b) *Above the threshold*: for `ε > V(g)` Theorem 2 applies; for `n` identical sites and
`ε = nε₁`, `ε₁ > V₁`, the number of samples `4βs_max ln(1/δ)/(ε₁ − V₁)` does not depend on `n`.
(c) *Below the threshold*: for all `t ≥ 0` and laws `P_i` on `Φ_i`,

    ln E|Q(g)| ≥ ln(1−2δ) + Σ_i ρ_i(t,P_i) − tε/β ,     ρ_i(t,P) = −ln max_a E_{φ∼P} e^{−t(φ(a) − Λ_i(φ)/β)} ,

and `∂_tρ_i(0+, P_i*) = V_i/β`; for identical sites and `ε₁ < V₁` the cost is `≥ (1−2δ)e^{cn}`,
`c = c(ε₁) > 0`.  Maximising over `(t, P)` gives a single-letter exponent `R^tilt_β(ε₁)`
(`= R^gen_β` of workstream A) `≥ R^rand_β(ε₁)`.

*Proof.*  (a) Induction on the number of sites: for fixed `x' = (x_1..x_{n−1})` the function
`x_n ↦ h(x',x_n)` is slack-Lipschitz on site `n`, so
`E_{π_n}e^{βh(x',·)} ≤ e^{K_n(Q_n)}e^{βE_{Q_n}h(x',·)}`, and `x' ↦ E_{Q_n}h(x',·)` is slack-Lipschitz
on the first `n−1` sites.  (b) Theorem 2 with `S ≤ n s_max`.  (c) Corollary 1' with competitors
`g + Σφ_i(x_i)`, `φ_i ∼ P_i` independent: `ℓ(a) = Σ_i[βφ_i(a_i) − Λ_i(φ_i)]` is a sum of
independent terms. ∎
(Tensorisation checked by convex maximisation over all slack-Lipschitz `h` on 12 two-site
products: the maximum equals `K₁+K₂` to `10⁻¹⁵`, `s08` (B).  Game values and minimax equality on
60 random sites, `s08` (A).  Simulation against tilted dips at `n = 400`: `s08b`.)

For a two-state site `Φ_i` is a segment, `V_i` is the theory report's `ε₁^crit` (closed form
`½ln(1 + 2p(1−p)(cosh βc − 1))` for symmetric slack, reproduced), and the optimal `Q*` equalises
the two extreme competitors — it does not depend on the instance tilt (`s11`).  For `e/c = ½`,
`β = 1`: `V = 0.1137` at the zero residual, `sup_γV(γ) = 0.1138` over additive instances,
hint-free passive width `0.1225`.  So **the interval the theory report left open is cheap at
every additive instance** (star + Theorem 2: `n(k−1)+1+O(1)` evaluations, correct on the whole
class).  A biased example shows why the second reference is indispensable: for `u = 2`,
`βγ = 1` (`π = (0.73, 0.27)`, `Q* = (½,½)`, `V = 0.3137`) the most stealthy single dip of effect
`n(V+0.03)` has `Q*`-measure `e^{−0.2}` but `π`-measure `e^{−172}` at `n = 1600` (`s08` (D)).  The
hint-free worst case over non-additive instances remains open (§5).

**Corollary 4 (homogeneous product spaces; no hint) [P; N for general sites and for the
continuum].**  Let `(σ, d₁)` be a finite quasi-metric space, or a compact metric space, with a
transitive group of isometries, `μ₁` its invariant probability, `X = σⁿ`,
`d = Σ_ic_id₁(x_i,y_i)`, `f ≡ 0`, and

    J₁(u) = sup{ ln E_{μ₁}e^{−u(φ − E_{μ₁}φ)} : φ(a) − φ(b) ≤ d₁(a,b) }       (Laplace functional of the site).

(a) For `ε > Σ_iJ₁(βc_i)` the passive sandwich with
`N = O(β²Σ_ic_i²diam(σ)² ln(1/δ)/(ε − ΣJ₁)²)` uniform samples is `(ε/2,δ)`-correct on the whole
class.  (b) For every admissible site function `φ` and `t ≥ 0`, every `(ε/2,δ)`-correct
algorithm satisfies at every constant residual

    ln E|Q| ≥ ln(1−2δ) + Σ_i[ −ln E_{μ₁}e^{−tc_iφ} ] − (t/β)( Σ_i[ −ln E_{μ₁}e^{−βc_iφ} ] + ε ) ,

which is exponential in `n` for identical sites and `ε = nε₁`, `ε₁ < J₁(βc)`.  So **the
threshold is exactly `Σ_iJ₁(βc_i)`**; the extremal alternatives are truncations
`−(C − Σ_ic_iφ*(γ_ix_i))₊` of the additive Laplace-extremal function, moved by random
isometries `γ_i`.

*Proof.*  (a) Tensorisation of the Laplace functional for `ℓ₁`-sums (Alon–Boppana–Spencer;
Bobkov–Houdré–Tetali) and McDiarmid.  (b) Corollary 1' with the competitors
`g̃_γ = Σ_ic_iφ(γ_ix_i)`: for fixed `a`, `γ_ia_i` is `μ₁`-distributed, so the dominance set is
hit with probability `μ(Σc_iφ(x_i) < C) ≤ e^{tC}∏E e^{−tc_iφ}`; the derivative of the exponent at
`t = 0` is positive iff `ε₁ < βcEφ + ln E e^{−βcφ} = ln E e^{−βc(φ−Eφ)}`. ∎

| site | `J₁(u)` | extremal site function | single dips suffice? |
|---|---|---|---|
| two points (cube) | `ln cosh(u/2)` | `1[x ≠ y]` | yes (Theorem 11.25) |
| `k` points, discrete metric | `max_{1≤j<k} ln((j/k)e^{u(1−j/k)} + (1−j/k)e^{−uj/k})` | `1[x ∉ A]`, `|A| = j*` | iff `j* = 1` (true for `k ≤ 3`; false for `k ≥ 4` at small `u`) |
| cycle `ℤ_m`, `m` even | value of the triangle wave (all `±1` slope patterns enumerated, `m ≤ 20`) | distance to a point | yes [num] |
| circle of length `2π`, constant `L` | `ln(sinh b/b)`, `b = uπ/2`, `u = βL` | `|θ − θ₀|` | yes (Lemma 5) |

### 2.3 Single dips are not extremal (independent confirmation of workstream A)

Flat `k`-state sites, Hamming envelope, `u = βc`.  Single dips: sensitive at width `nε₁` iff the
radius exceeds `n(Λ_pt + ε₁)/u`, `Λ_pt = −ln(1/k + (1−1/k)e^{−u})`; exponent `D(ρ‖1 − 1/k)`.  Dips
centred on boxes `∏A_i`, `|A_i| = j`: the same with `1/k` replaced by `j/k`.  Own exact
computations (`s07`, `s07b`, `s10`, `s12`):

| site | exponent at `ε = o(n)`: single dips | all competitors | threshold: single dips | true (Cor. 4 / Thm 3) |
|---|---|---|---|---|
| flat 4-state, `u = 1` | `0.02841` | `0.02914` | `0.1074` | `0.1201` |
| flat 8-state, `u = 1` | `0.0194` | `0.0309` | — | — |
| flat 10-state, `u = 2` | `0.0891` | `0.1195` | `0.294` | `0.470` |
| flat 20-state, `u = 1` | `0.0093` | `0.0309` | `0.032` | `0.123` |
| energies `(0,0,2)`, `β = c = 1` | `0.0247` | `0.0290` | `0.0947` | `0.1197` |

Exact finite-`n` values converge to the single-letter exponents (`(ln N)/n = 0.02841` and
`0.02915` at `n = 10⁶`); at width `0.114n`, between the two thresholds, single dips give nothing
and box dips give `ln N ≥ 78` at `n = 10⁶`.  On `K₄×K₄` (all 65 534 supports, exact LP) box dips
give the exact fractional hitting number at every tested accuracy, single dips are off by up to
a factor `3.5`.  On 30 random non-uniform sites with 3–5 states the vertex game beats the
single-dip game in 25 (thresholds) and 16 (exponents at `ε₁ = 0`) cases; set-distance functions
alone are not enough in general (`V > V_set` in 41 of 60 random sites): general vertices
`min_b(c_b + s(·,b))` are needed.

*What this workstream adds to A's results as quoted in the theory report:*
(1) the competitor form (Lemma 1): one machine-checked lemma covering point, set and tilted dips
on arbitrary instances, with the likelihood-ratio / dissipated-work reading and the lattice
explanation;
(2) Theorem 2: the upper half of the threshold on *every finite instance*;
(3) Corollary 4: for homogeneous sites the threshold is the Laplace functional, no hint is
needed, and continuous sites are covered (§2.4);
(4) independent numerics with separate code.

*Negative result on the binary case.*  I tried to beat single dips for `ln Z` on biased binary
product instances with dips centred on two-group type classes (the family that *does* win for
Boltzmann averages, §2.5): no improvement of the exponent in 13 parameter sets at
`ε₁ ∈ {0, 0.05}` and no positive exponent above `V` in 20 further cases (`s06`, `s06b`).  This is
consistent with A's (unrefereed) claim that single dips are extremal for two-state sites.

### 2.4 Continuous configuration spaces

*Framework.*  `X` a compact metric space with a finite reference measure `μ₀`, `f` bounded
measurable, residuals with `g(x) − g(y) ≤ d(x,y)`, `Z(g) = ∫e^{−β(f+g)}dμ₀`; an algorithm
evaluates `g` at finitely many (random, adaptive) points.  Lemma 1, Corollary 1', Theorem 2 and
the detection-weight lemma are identities and inequalities between integrals and hold verbatim
(dips differ from `g` on open sets of positive measure); covering numbers become metric
entropies of slack balls **[R]**.  (Where a spot-check falls back to "evaluate everything", read:
any correct procedure, e.g. a deterministic certificate on a fine mesh; only the cost on the
hint is claimed.)

**Lemma 5 (circle) [P; R, probably classical].**  For `φ` `L`-Lipschitz on the circle of length
`2π` with uniform law and every convex `Ψ`, `EΨ(φ − Eφ) ≤ EΨ(Lπ(U − ½))`, `U` uniform on `[0,1]`;
in particular `ln E e^{−β(φ−Eφ)} ≤ ln(sinh b/b)`, `b = βLπ/2`, with equality for `φ = L|θ − θ₀|`.

*Proof.*  By the isoperimetric inequality on the circle (the `r`-enlargement of a proper closed
set gains at least `2r` in length) the quantile function `q` of `φ` on `(0,1)` satisfies
`0 ≤ q' ≤ Lπ`.  With `V` uniform, `X' = q(V) − Eq(V)` and `Y = Lπ(V − ½) = X' + D(V)`, where `D`
is nondecreasing and centred.  For convex `Ψ`, `EΨ(Y) ≥ EΨ(X') + E[Ψ'(X')D] ≥ EΨ(X')`, because
`Ψ'(X')` and `D` are nondecreasing functions of `V` (Chebyshev's association inequality).
`E e^{−2b(V−½)} = sinh b/b`. ∎
(Exhaustive check on `ℤ_m`, `m ≤ 20`: the triangle wave is the maximiser among all extreme
points, and its value converges to `ln(sinh b/b)`; `s04` (1).)

**Theorem 6 (torus of torsion angles, `ℓ₁` envelope) [P; N].**  Let `X = (ℝ/2πℤ)ⁿ`, `f ≡ 0`,
`𝒢 = {g : |g(x) − g(y)| ≤ Σ_iL_i|x_i − y_i|_{S¹}}`, `b_i = βL_iπ/2`, `J = Σ_i ln(sinh b_i/b_i)`,
`Λ₁(b) = ln(2b/(1 − e^{−2b}))`.
(a) For `ε > J`: `N = ⌈8Σ_ib_i² ln(2/δ)/(ε − J)²⌉` uniform random evaluations give `ln Z` within
`ε/2` with probability `1−δ` for every `g ∈ 𝒢`
(`ln Z ∈ [n ln 2π − βm̂ − βt, n ln 2π − βm̂ + βt + J]`, `m̂` the sample mean, `βt = (ε−J)/2`).
(b) For `ε < J`: every `(ε/2,δ)`-correct algorithm satisfies at every constant residual

    ln E|Q| ≥ ln(1−2δ) + sup_{λ≥0} [ Σ_iΛ₁(λb_i) − λ(Σ_iΛ₁(b_i) + ε) ] ,

which is positive iff `ε < J` and exponential in `n` for `ε = nε₁` below the mean of
`ln(sinh b_i/b_i)` (bounded `b_i`).  For equal `b_i = b` the exponent is
`E(ε₁;b) = sup_λ[Λ₁(λb) − λ(Λ₁(b)+ε₁)]`; `E(0;b) ≈ b²/24` and `J₁ ≈ b²/6` for small `b`;
`E(0;b) ≈ ln(2b/(e ln 2b))` for large `b`.

*Proof.*  (a) Lemma 5, tensorisation, McDiarmid with ranges `L_iπ`.  (b) Cone dips
`−(C − Σ_iL_i|x_i − y_i|)₊` (Corollary 4 with `φ` the distance to a point;
`E e^{−tL|θ|} = (1 − e^{−tLπ})/(tLπ)`, `Λ₁'(0) = 1`). ∎

| `b = βLπ/2` | `0.25` | `0.5` | `1` | `2` | `5` | `20` |
|---|---|---|---|---|---|---|
| threshold per angle `ln(sinh b/b)` | `0.0104` | `0.0413` | `0.1614` | `0.5952` | `2.697` | `16.31` |
| exponent `E(0;b)` | `0.0026` | `0.0103` | `0.0394` | `0.1366` | `0.4837` | `1.384` |

(For comparison the cube: threshold `ln cosh(u/2)`, exponent `≈ u²/32`; in both cases the
exponent at vanishing accuracy is one quarter of the threshold at weak coupling.)  The exact
volume bound from the `n`-fold convolution of `U[0,π]` approaches `nE` from above (`n ≤ 80`).  A
deterministic certificate at the same instance needs a mesh `≈ 4ε/(nβL)` per angle, i.e. about
`(nb/ε)ⁿ` evaluations.

**Proposition 7 (fixed dimension) [order K: Holzmüller–Bach 2025; constants R].**  Flat torus
`T^d` (or a compact `d`-manifold of volume `𝒱`) with geodesic distance,
`|g(x)−g(y)| ≤ L·dist`, `B = βL → ∞`, flat instance.  Then `e^{−Λ} = d!ω_d/(𝒱B^d)(1+o(1))`, i.e.
`Λ = d ln B + ln(𝒱/(d!ω_d)) + o(1)`, and

    (1−2δ) · 𝒱B^d / (ω_d(Λ+ε)^d)  ≤  E|Q|         (every algorithm; cone dips),

while with the hint a hedged spot-check with uniform samples needs `O(ln(1/δ)·𝒱/vol B(r))`
evaluations, `r ≈ (Λ+ε)/B` the least sensitive radius: the hinted cost at the flat instance is
`Θ(𝒱(B/(d ln B))^d/ω_d)` for `ε = O(1)`.  Uniform sampling is optimal by symmetry, and balls are
the smallest sensitive supports by Brunn–Minkowski (`D_t + tK ⊂ D` for the inner parallel sets
`D_t`, hence `∫_D(e^{B·dist(x,Dᶜ)} − 1) ≤` the same integral over the ball of equal volume)
**[P; for supports that lift to `ℝ^d`, i.e. `B` large]**.  The generic bound `E_πe^{Λ}` of Theorem
11.26 is larger by the factor `(Λ+ε)^d/d! ≈ (e ln B)^d`.  The order `(B/ln B)^d` of the
*worst-case* stochastic complexity is implicit in Holzmüller–Bach (their Theorem 8 with
`Bn^{−1/d} ≈ (d/2C)ln B`, and Proposition 9: error `≥ c·Bn^{−m/d} − d ln(1+3B)`, whose second term
is the soft gap of the flat instance).  New here: the instance-wise form and the constants.

**Remark 8 (one global `ℓ₂` constant in high dimension) [P/num].**  On `Tⁿ` with the Euclidean
geodesic metric (`B = βL` fixed, `n → ∞`) everything is dimension-free.  The largest Jensen gap
is at most `B²/2` (log-Sobolev constant `1` of the circle and Herbst's argument, **[K, from
memory]**) and at least `B²π²/24 = 0.411B²` (the additive function `Ln^{−1/2}Σ|x_i|`); the Jensen
gap of the distance function is only `B²π²/30 = 0.329B²`, so cone dips alone give a threshold
below the passive one — but the truncated additive competitor of Corollary 4 raises it to
`0.411B²`.  Below the threshold the bound is `exp(Θ((J − ε)²/B²))`: exponential in `B²`, not in
`n`.  Summary of the scaling in the dimension and in `βL`: `(βL/ln βL)^d` for fixed `d`;
`exp(n·E(ε₁;b))` with a sharp threshold for per-angle (`ℓ₁`) constants; `exp(Θ(β²L²))` for one
global `ℓ₂` constant.

### 2.5 Other observables

**Lemma 9 (soft gaps relative to a reference measure) [V\*, `lean/RefMeasure.lean`; R].**  For
positive weights `ν`, `β > 0`, `g, g' ∈ 𝒢`, `η ≥ 0`: if `Σνe^{β(g−g')} ≥ (1+η)Σν` then

    Σ_{z : g'(z) ≠ g(z)} ν(z)((1+η)e^{Λ_ν(z)} − 1) ≥ ηΣν ,       Λ_ν(z) = ln Σν − ln Σ_xν(x)e^{−βs(x,z)}

(`detection_weight_ref`: the repository's `detection_weight_ge` with the known part
`f = −β⁻¹ln ν − g`; the known part is a free parameter of that lemma).  By continuity it holds
for `ν` with zeros **[P]**; checked on 70 314 alternatives, including measures with zeros
(`s01`).  For a macrostate `S`, `Λ_S := Λ_{π(·|S)}` is the *restricted soft gap*
`ln Z_S(g) − ln Z_S(U_y)`.

**Proposition 10 (free-energy differences `Φ = ln Z_A − ln Z_B`, `A ∩ B = ∅`) [P; N].**
(a) A comparison dip with competitor `g̃` and constant `C` changes `Φ` by at least
`(βC − Λ_A(g̃))₊ − ln(1 + e^{βC − Λ_B(g̃)})`, `Λ_S(g̃) = ln Z_S(g) − ln Z_S(g̃)`.  In particular a
dip at `y` with `Λ_B(y) − Λ_A(y) > ε + M` is sensitive at depth
`(Λ_A(y) + ε − ln(1 − e^{−M}))/β`: where pinning at `y` shifts the log-odds of `A` against `B` by
more than `ε`, the radius is governed by the restricted soft gap of `A`.
(b) With the hint, sampling from `¼(π_A + π_B + w_A/W_A + w_B/W_B)`,
`w_S = π_S((1+η)e^{Λ_S} − 1)`, `η = e^{ε/4} − 1`, detects every alternative with `|ΔΦ| > ε/2` with
probability `≥ ¼min(η/W_A, η/W_B, 1 − e^{−ε/4})` per sample (Lemma 9).
(c) *Uncoupled macrostates* (`d = ∞` between `A` and `B`, each a product landscape): the
threshold of `Φ` is **exactly `V_A + V_B`** — exponential below (pair version of the detection
principle with a tilted dip in `A` and one in `B`), bounded cost above (Theorem 2 in each state,
output `Φ(g) + (V_A − V_B)/2`).  There is no cancellation of errors: for two cubes the threshold
is `2n ln cosh(u/2)`.
(d) *Ranking.*  To certify `Z_A > Z_B` at an instance with margin `Δ = Φ(g) > 0` one must exclude
hidden pockets in the **loser**: bumps in `A` are never stealthy (lowering `ln Z_A` by `a`
requires `π_A(D) ≥ 1 − e^{−a}`), dips in `B` are.  The certification is cheap (bounded number of
samples from `π_A`, `π_B`, `Q*_B`) iff `Δ > V_B`, and exponential for a product `B` if `Δ < V_B` by
an extensive margin.  For `K` macrostates the hinted cost is at most
`2ln(1/δ)[1/(1−e^{−Δ_min/2}) + Σ_{k≥2}W_k/η_k]`, `η_k = e^{Δ_k/2} − 1`: near-degenerate competitors
dominate.  (An answer, in the hinted model, to the stopping-rule question of theory report
§3.6.)
(e) The Gibbs probability of a single state costs exactly one evaluation more than `ln Z`; the
log-odds of a macrostate `S` is the case `A = S`, `B = Sᶜ`.
(Exact LPs on 40 small instances: the ordering `N_dip ≤ N_width ≤ N_inst ≤ 1/p_act ≤ 1/p_guar` is
never violated; the sampler is within a median factor `1.7` of the exact hitting number,
`s02`.)

**Proposition 11 (Boltzmann averages) [P; N].**  Let `0 ≤ O ≤ 1`, `μ = ⟨O⟩_g`, and let `g'` have
relative weight change `ψ = e^{β(g−g')} − 1`.  Then

    ⟨O⟩_{g'} − μ = E_π[(O − μ)ψ]/(1 + E_πψ) = (m/(1+m))(⟨O⟩_ν − μ)    for dips (ψ ≥ 0),

`m = Z'/Z − 1`, `ν ∝ πψ` the excess measure.  Consequently (a) a dip that changes `ln Z` by less
than `Δ` moves every average by less than `1 − e^{−Δ}`; (b) to be sensitive a dip must carry
mass *and* put it where `O` deviates from its mean; (c) *upper bound with a hint*: with the
charges `P = (O − μ − η)₊`, `N = (μ + η − O)₊`, the tilted measure `ν_P ∝ πP`,
`η_P = η/(2E_πP)`, every alternative with `⟨O⟩' > μ + η` differs from the hint on a set of
probability `≥ min(η/(2E_πN), η_P/((1+η_P)E_{ν_P}e^{Λ_{ν_P}} − 1))` under one of the two laws
`∝ πN`, `∝ ν_P((1+η_P)e^{Λ_{ν_P}} − 1)` (Lemma 9 for the charge-tilted measure), and
symmetrically for decreases: the cost is governed by the soft covering number of the part of
the ensemble where the observable exceeds its mean.  (Exact linear-fractional programs on 48
small instances: guarantee never violated; dips give the exact hitting number in only `13 %` of
them, `s02`.)

**Theorem 12 (magnetisation on the cube: averages are much harder than free energies)
[P; N].**  `X = {0,1}ⁿ`, `f ≡ 0`, `d = c·`Hamming, `u = βc`, `O(x) = |x|/n`, instance `g ≡ 0`
(`⟨O⟩ = ½`).  Over the class `⟨O⟩` ranges exactly over `[q, 1−q]`, `q = 1/(1+e^u)`; the a-priori
half-range is `H(u) = ½tanh(u/2)`.  Let an algorithm return `⟨O⟩` within `η` with probability
`1−δ` on the whole class.
(a) *Single dips.*  A dip of radius `(ρ₀+o(1))n` centred at `y`, `|y| = τn`, shifts `⟨O⟩` by
`(τ − ½)tanh(u/2)`, and its support has exponentially small density in every Hamming level iff
`τ < 1 − ρ₀`.  Hence the cost is exponential for
`η < (½ − ρ₀)tanh(u/2) = tanh(u/2)·ln cosh(u/2)/u` (`≈ u²/16`): the same fraction
`ln cosh(u/2)/u` of the a-priori width as for `ln Z`.
(b) *Dips centred on type classes do much better.*  Split the coordinates into two halves, let
`T*` be the configurations with fractions `1−q` and `a₀` of ones in the halves, and
`h = (R − d_H(x,T*))₊`.  If `½[h_b(q) + h_b(a₀)] + (u/2)(1−q−a₀) > ln 2` there is a depth `R` such
that the mass grows exponentially, the excess measure concentrates on `T*`, and the support has
exponentially small density in **every** level (no symmetric sampler finds it).  Hence the cost
is at least `½(1−2δ)e^{c(u,η)n}`, `c > 0`, for every

    η < ε_set(u) := ½(1 − q + a₀*(u)) − ½ ,    a₀* the root of  ½[h_b(q) + h_b(a₀)] + (u/2)(1−q−a₀) = ln 2 .

A linear program over all multi-group designs returns this two-group design.
(c) *Upper bound.*  For `η > η_up(u) := inf_{t>0}[ψ(t) + V(t)]/t − ½`, `ψ(t) = ln((1+e^t)/2)`,
`V(t) = ½ln(1 + 2p_t(1−p_t)(cosh u − 1))`, `p_t = e^t/(1+e^t)`, a bounded number of samples from a
mixture of three product measures (uniform and the game-optimal `Q*_{±t}` of the tilted measures
`Bern(p_{±t})ⁿ`) certifies `|⟨O⟩_{g'} − ½| ≤ η` for the hint `g ≡ 0`.

| `u = βc` | `0.1` | `0.5` | `1` | `2` | `3` | `4` | `6` | `8` |
|---|---|---|---|---|---|---|---|---|
| single dips: exponential for `η/H <` | `0.025` | `0.124` | `0.240` | `0.434` | `0.570` | `0.663` | `0.770` | `0.827` |
| type-class dips: exponential for `η/H <` | `0.707` | `0.710` | `0.716` | `0.740` | `0.769` | `0.798` | `0.844` | `0.874` |
| bounded cost for `η/H >` | `0.999` | `0.980` | `0.931` | `0.839` | `0.809` | `0.813` | `0.846` | `0.875` |

So for a Boltzmann average more than `70 %` of the a-priori half-range (the ratio `ε_set/H` is `1/√2` in the limit `u → 0` and increases with `u`, numerically) is out of reach of every
sub-exponential algorithm (for `ln Z` the corresponding fraction `ln cosh(u/2)/u` tends to `0` at
weak coupling); a threshold exists, it lies in the bracket of the last two rows, and the bracket
closes to within `1 %` for `u ≥ 6`.  For small `u` the bracket is `[H/√2, H]`.
*Where the gap comes from* **[num]**: `η_up(u)` coincides (to `10⁻⁵`, six values of `u`, `s09b`)
with the value of the design program of (b) *without* the constraint `a_g ∈ [q, 1−q]`.  So the
upper bound is the dual of the unconstrained design problem, and the whole bracket is the
effect of that constraint — an excess measure cannot sit at a type with more than a fraction
`1−q` of ones in a group, because the perturbation is Lipschitz and its mass spills over to
lower types.  A verifier analysis that accounts for this spill-over would put the threshold at
`ε_set(u)`.

*Proof sketch.*  (a), (b): counting by types.  For (b), with `R/n < F := (1−q−a₀)/2` (the
per-site distance from `T*` to the "diagonal" types `(κ,κ)`, which are the typical types of the
levels): mass exponent `½h_b(q) + ½h_b(a₀) − ln 2 + uR/n`; the support consists of types at
distance `< R/n` from `(1−q,a₀)`, none of which is typical for its level, so its density in level
`κ` is `≤ exp(−n·min_b[h_b(κ(b)) − ½h_b(b₁) − ½h_b(b₂)]) `; and since `1−q, a₀ ∈ [q,1−q]` the
function `b ↦ ½h_b(b₁)+½h_b(b₂) − u·dist(b,(1−q,a₀))` is maximal at `(1−q,a₀)`.  The lower bound is
the pair version of the detection principle applied to the alternative and its mirror image,
randomised over coordinate permutations: `E|Q| ≥ (1−2δ)/(2max_k density_k(supp))`.  (c):
`F(t) = ln E_πe^{βh + t|x|}` is convex with `F'(0) = n⟨O⟩_{g'}`, so
`n⟨O⟩' ≤ [F(t) − F(0)]/t`, `F(t) = nψ(t) + ln E_{π_t}e^{βh} ≤ nψ(t) + nV(t) + βE_{Q*_t}h`
(Theorem 3(a) at the tilted measure) and `F(0) ≥ βE_πh`; both means vanish up to `o(n)` when
nothing is detected. ∎
(Exact finite-`n` confirmation for `n ≤ 6400`: at `u = 2` the design `a₀ = 0.60` has
`ln(mass) = +295`, shift `0.238` (single-dip limit `0.165`, half-range `0.381`) and
`max_k ln density_k = −14.9` at `n = 6400`; the inequality in (c) was checked on 4 000 random
`(h,u,t,Q)` on the 4-cube.  `s03`, `s03b`, `s03c`, `s09`.)

### 2.6 Structured classes and staged protocols

**(i) First-order class: staging cannot help [R].**  Annealing in `β` or in a coupling
parameter, thermodynamic integration, Jarzynski/AIS and replica exchange are adaptive randomised
query algorithms; Theorems 11.23–11.25, Lemma 1 and Theorem 3(c) bound all of them.  In the
sampling-oracle model (free samples from the Gibbs measure at any chosen temperature) staging
reduces `e^{KL}` (one-shot importance sampling) to `Õ(q/ε²)` samples, `q` the log partition ratio
(Štefankovič–Vempala–Vigoda; Harris–Kolmogorov, with matching lower bounds).  The exponential
price in the query model is the price of *producing* those samples from an unknown landscape,
and Lemma 1 shows that it cannot be avoided on a lattice class.

**(ii) Few-body classes [R].**  If `g` is a sum of terms on at most `m` sites the class is a
linear space of dimension `D_m = Σ_{j≤m}C(n,j)(k−1)^j`; the anchored interpolant on a Hamming ball
of radius `m` (theory report Theorem 11.18) determines `g`, so `D_m` evaluations suffice for every
functional at every temperature — polynomial, non-adaptive, no staging.  (The computational cost
of evaluating `Z` afterwards is not counted in the query model.)

**(iii) Dense second-order classes: a sharp dichotomy.**  Let
`𝒢₂(c₂) = {g : {0,1}ⁿ → ℝ : |D_iD_jg(x)| ≤ c₂ for all x, i ≠ j}` (mixed second differences; no
first-order bound), `f` additive, `w = βc₂n`.

**Theorem 13 [P; N; the tools of (a) are K].**
(a) *`w ≤ 4`: polynomial, at every accuracy.*  If `α := (n−1)tanh(βc₂/4) < 1` (true whenever
`w ≤ 4`, with `1 − α ≥ 1/n`), the following staged algorithm is `(ε/2,δ)`-correct for `ln Z` on all
of `𝒢₂(c₂)` with `O(K³ε^{−2}ln(K/δ)·n ln(nK/ε)/(1−α))` evaluations, `K = ⌈wn⌉`: evaluate a star at
`x₀` (`n+1` points) and form the additive interpolant `g_star`; with `r = g − g_star`
(`β|r| ≤ wn/2` by Theorem 11.16) anneal along `E_λ = f + g_star + λr`, `λ_k = k/K`; sample each
`π_{λ_k}` by heat-bath Glauber dynamics (one new evaluation per step); return
`ln Z(f+g_star) + Σ_k ln mean(e^{−βr/K})`.
(b) *`w > 4`: exponential for every algorithm* (here `f ≡ 0`, instance `g ≡ 0`).  For `r ∈ ℕ` the **parabolic droplet**
`g_y(x) = −c₂T(r − d_H(x,y))`, `T(m) = m(m+1)/2` for `m ≥ 0` and `0` otherwise, belongs to
`𝒢₂(c₂)`, differs from `0` exactly on the open Hamming ball of radius `r`, and
`Z(g_y)/Z(0) = 2^{−n}Σ_kC(n,k)e^{βc₂T(r−k)}`.  Hence, if this ratio exceeds `e^{ε}`, every
`(ε/2,δ)`-correct algorithm on `𝒢₂(c₂)` has `E|Q(0)| ≥ (1−2δ)2ⁿ/|B(r−1)|`.  With `r = ρn`:
`n⁻¹ln(Z'/Z) → Ψ(w,ρ) = max_{κ≤ρ}[h_b(κ) − ln 2 + (w/2)(ρ−κ)²]₊`, and
`Ψ(w,½) = f_CW(w) := max_m[wm²/8 − I(m)]`, the Curie–Weiss free energy, which is positive iff
`w > 4`.  So for `w > 4` and every `ε₁ < f_CW(w)` (in particular `ε = o(n)`):

    n⁻¹ ln E|Q(0)| ≥ ln 2 − h_b(ρ*(w,ε₁)) − o(1) > 0 ,       ρ*(w,ε₁) = inf{ρ : Ψ(w,ρ) > ε₁} < ½ .

(c) *With a first-order bound as well* (`|D_ig| ≤ c₁`, `u = βc₁`): (a) is unchanged; in (b) the
slope of the droplet is capped at `c₁` and the lower bound holds below
`ε₁^crit(u,w) = max_x[∫₀^x min(u, ws)ds − (ln 2 − h_b(½ − x))]`, which vanishes iff `w ≤ 4` and
increases to the first-order threshold `ln cosh(u/2)` as `w → ∞`.

*Proof.*  (a) For `E_λ` the conditional law of `x_i` given the rest is Bernoulli with log-odds
`−βD_iE_λ`; changing `x_j` changes the log-odds by `βλ|D_iD_jg| ≤ βc₂`, hence the
total-variation influence is at most `tanh(βc₂/4)` (`f` and `g_star` are additive and drop out).
Path coupling (Dobrushin; Bubley–Dyer) gives `TV ≤ n(1 − (1−α)/n)^T`.  Each factor
`Z_{k+1}/Z_k = E_{π_k}e^{−βr/K}` has integrand in `[e^{−1/2}, e^{1/2}]`; Hoeffding and a union
bound over the `K` stages give the stated count.  (b) `D_iD_j` of a function `φ(d_H(x,y))` is
`±` a second difference of `φ`, and `φ(k) = c₂T(r−k)` has second differences in `{0, c₂}`;
detection requires a query in the support; average over `y`.  Finally
`ln 2 − h_b(½−x) = Σ_{j≥1}(2x)^{2j}/(2j(2j−1)) ≥ 2x²` with equality only at `0`, which gives
`Ψ(w,½) > 0 ⇔ w > 4`. ∎

| `w` | `4` | `5` | `6` | `8` | `12` |
|---|---|---|---|---|---|
| accuracy threshold `f_CW(w)` per site | `0` | `0.0359` | `0.1152` | `0.3265` | `0.8094` |
| exponent at `ε = o(n)` | `0` | `0.0010` | `0.0051` | `0.0196` | `0.0556` |

| `ε₁^crit(u,w)` | `w=4` | `5` | `6` | `8` | `16` | `64` | `∞` (`= ln cosh(u/2)`) |
|---|---|---|---|---|---|---|---|
| `u = 1` | `0` | `0.0201` | `0.0368` | `0.0576` | `0.0889` | `0.1123` | `0.1201` |
| `u = 2` | `0` | `0.0359` | `0.1004` | `0.1838` | `0.3088` | `0.4025` | `0.4338` |

*Remarks.*  The transition point is the Curie–Weiss critical coupling (`4βJ = w`), at which
Glauber dynamics for the Curie–Weiss model itself changes from `O(n log n)` to exponential mixing
(Levin–Luczak–Peres 2010) **[K]**.  The theorem says that the same point separates polynomial
from exponential *query* complexity for **every algorithm** on the whole class with that
second-order constant; the extremal members are one-sided Curie–Weiss droplets.  The
single-reference sandwich after the star only reaches width `n ln cosh(w/2)` even for `w < 4`, so
it is the staging that achieves the result; I did not prove that adaptivity is necessary.
Numerics (`s05`, `s05b`, `s05c`): droplets satisfy `max|D_iD_j|/c₂ = 1.000000` (brute force,
`n ≤ 10`); exact Glauber gaps are `≥ (1−α)/n` on 12 members of `𝒢₂` (`n = 8`); the annealed
estimator is accurate to `±0.02` on random members (`n = 12`, exact enumeration) and to `±0.06` at
`n = 4000`, `w = 3.5` (lumped chain, `1.5·10⁷` evaluations against `2^{4000}` states); for
`w = 6, 8, 12` it misses a planted droplet completely (errors `43.5`, `22.8`, `52.5` nats; support
measure `e^{−19}`…`e^{−50}`).

**(iv) Where structure enters.**

| class | closed under `min`? | localised admissible perturbation of depth `D` | query complexity of `ln Z` |
|---|---|---|---|
| first-order (Lipschitz) | yes (lattice) | cone / truncated tilt, radius `D/c` | threshold in **accuracy** (`V(g)`); exponential below it for every algorithm, staged or not |
| + dense second-order, `w = βc₂n` | no | parabolic droplet, radius `√(2D/c₂)` | threshold in **coupling / temperature**: polynomial iff `w ≤ 4` (staged), else exponential below `n f_CW(w)` |
| few-body of order `m` | no | none (a member vanishing on a ball of radius `m` vanishes) | `≤ D_m`: polynomial, non-adaptive |

### 2.7 Negative results and dead ends

1. *Single dips are not extremal for Boltzmann averages even on the binary cube* (Theorem 12:
   `O(u²)` against `Ω(u)`), and not for `ln Z` on sites with `≥ 3` states (§2.3).
2. *Type-class dips do not help for `ln Z` on biased binary instances* (`s06`, `s06b`).
3. *An annulus or a "code of shallow dips" is never better than a ball on the uniform cube*
   (hand computation, consistent with Harper): shallow perturbations have mass ≈ measure, so
   stealth forces extensive depth, and the support must contain a neighbourhood of the excess
   set.
4. *"Glassy" code instances (many deep wells) are not harder than the flat instance* for the dip
   bound.  I first estimated an exponent `≈ u/2`, forgetting that the slack ball of a well
   contains the whole well; the corrected radius is `≥ ρ₀n`.  (Withdrawn before it was written
   down anywhere else.)
5. *The generic soft-gap sampler is exponentially wasteful* at homogeneous instances: `u/2` per
   site against the true `≈ u²/32` on the cube; a factor `(e ln B)^d` in fixed dimension;
   `e^{Θ(B√n)}` against `e^{Θ(B²)}` for the `ℓ₂` torus.
6. *Mean-based hint-free procedures cannot beat the passive width*: adding a second reference
   `Q` costs the transport term `β(E_{π_f} − E_Q)g`, which cancels the gain.
7. *The convexity bound for averages is not tight at weak coupling* (`η_up/H → 1` as `u → 0`).
8. On discrete spaces balls are optimal supports only at ball sizes (cycle: arcs at every size,
   `s04b`) — a discreteness effect of at most the ratio of consecutive ball sizes.
9. A first version of the set-dip experiment used margins too small to see exponential decay at
   `n ≤ 3200` (rates are quadratic in the margin); the table of §2.5 uses larger margins.

---

## 3. Numerics

All scripts are plain Python (numpy/scipy), run from the directory; outputs are in `out/`;
none takes more than seven minutes.

| script | what | sizes | result |
|---|---|---|---|
| `s01_refmeasure_lemma.py` | Lemma 9 and dip bounds, exhaustive over supports + random alternatives | 400 instances, `|X| ≤ 9`, 70 314 alternatives | 0 violations; bound attained (min ratio `1.000000`) |
| `s02_observables_small.py` | exact LPs (Charnes–Cooper) for `⟨O⟩` and `ln Z_A − ln Z_B`: hitting numbers, dip bound, samplers | 24 + 20 instances, `|X| = 7, 8`, all supports | ordering never violated; sampler within a median factor `1.5–1.7` of exact |
| `s03_cube_magnetisation.py`, `s03b`, `s03c`, `s09`, `s09b` | magnetisation: single dips, type-class dips (exact type counts), LP over designs, exponent table, bracket, inequality check | `n ≤ 6400`; LP grid 401; 4 000 random checks on the 4-cube | Theorem 12 and its table |
| `s04_torus.py`, `s04b` | circle extremals (all slope patterns), tensorisation on `ℤ_m²`, exponents, exact volume bound, fixed-`d` numbers, optimal supports | `m ≤ 20`; `n ≤ 80`; all 65 534 supports of `ℤ₁₆`, `Q₄` and small tori | triangle wave extremal; no violation; arcs optimal at every size |
| `s05_second_order.py`, `s05b`, `s05c` | Theorem 13: droplet membership, `Ψ`, Dobrushin constants and exact gaps, annealed Glauber, planted droplets, two-parameter threshold | brute force `n ≤ 10`; exact `n = 12`; lumped chain `n ≤ 4000` | as stated in §2.6 |
| `s06_setdips_lnZ.py`, `s06b` | type-class dips against single dips for `ln Z`, biased binary sites | 13 + 20 parameter sets, type grid `420²` | no improvement |
| `s07_tilted_dips.py`, `s07b`, `s10`, `s12` | flat and random `k`-state sites: thresholds, exponents (dual LP), exact finite `n`, exact LP on `K₄×K₄`; cross-check of A's numbers | `k ≤ 20`, `n ≤ 10⁶`; 30 + 60 random sites | §2.3 table; all quoted numbers of A reproduced |
| `s08_game_threshold.py`, `s08b`, `s08c`, `s11` | game values, minimax, two-reference inequality, verifier bracket, simulation against tilted dips, two-state site over instances | 60 sites; 12 products; 1 680 supports; `n = 14` exact (360 alternatives); Monte Carlo `n = 400` | 0 violations; `V = J_sup` on flat sites; `V_point < V` for `k ≥ 4` |

Scratch Lean (each compiles with `lake env lean`; axioms `propext, Classical.choice,
Quot.sound`): `lean/ComparisonDip.lean` (Lemma 1), `lean/SetDip.lean` (set dips and set soft
gaps), `lean/RefMeasure.lean` (Lemma 9 for positive weights).

---

## 4. Prior art and positioning

### 4.1 Does the soft gap have a physical name?

No standard one, but several readings **[K for the identities]**:
* `e^{−Λ(y)} = ⟨e^{−βs(·,y)}⟩_π` is a Zwanzig (1954) free-energy-perturbation average with the
  slack as perturbation; `Λ(y)/β = F[f+U_y] − F[f+g]` is the reversible work of replacing the
  residual by its pessimistic cone anchored at `y` — formally a Widom (1963) insertion formula
  for the constraint "pinned at `y`".  `Λ(y) = min_Q[βE_Qs(·,y) + KL(Q‖π)]` (Gibbs variational
  principle): an entropy-regularised distance from the ensemble to `y`; as `β → ∞` it becomes the
  gap.
* With the pinned ensemble `π_y ∝ πe^{−βs(·,y)}`: `βE_{π_y}s ≤ Λ(y) ≤ βE_πs`, and
  `βE_πs − Λ = KL(π‖π_y)` is the dissipated work of the instantaneous switch (Crooks; the overlap
  measures of Wu–Kofke are these relative entropies).  The general object is `ℓ_g̃ = βW_diss`
  (§2.1).
* `E_πe^{Λ} = Σ_yπ(y)/π(`soft ball at `y)`: a soft form of the covering integral
  `∫dπ(x)/π(B(x,r))` of metric-entropy theory.
* At a flat instance in `ℝ^d`, `Λ ≈ d ln(βL)` is the "optimisation–log-partition gap" of
  Holzmüller–Bach, Lemma 3 (`|M_f − εL_{f/ε}| ≤ εd ln(1 + 3d^{−1/2}|f|₁/ε)`).

### 4.2 Is the threshold phenomenon known?

* **Holzmüller & Bach, JMLR 26 (2025)** [read: full text of §§1–2 and the proofs of Theorem 8
  and Proposition 9; extract in `lit/txt/hb.txt`].  Classes `‖f‖_{C^m} ≤ B` on `[0,1]^d`, `n`
  evaluations, constants depending on `(m,d)` not tracked.  Deterministic: `Θ(Bn^{−m/d})`.
  Stochastic: upper bound `min{Bn^{−m/d}, e^{CBn^{−m/d}}Bn^{−1/2−m/d}}`, lower bound
  `Ω(Bn^{−m/d}) − d ln(1+3B)` by reduction to optimisation; an "optimisation regime" and a
  "quadrature regime"; a lower bound outside the optimisation regime is stated as open.  So the
  two-regime picture and the bump technique are known for fixed `d`; the exact high-dimensional
  threshold, the instance-wise form and the role of the Jensen gap / game value are not there.
  (The third referee reached the same conclusion independently, `reviews/R3`, M5.)
* **Jarzynski, PRE 73, 046105 (2006)** [abstract read; the formula from memory]: the exponential
  work average is dominated by realisations typical of the reverse process; the number of
  realisations needed is `≈ exp(β·dissipated work of the reverse process)`.
  **Chatterjee–Diaconis (2018)** [search summary]: importance sampling needs
  `≈ e^{KL(target‖proposal)}` samples, with a cut-off.  **Zuckerman–Woolf (2002),
  Gore–Ritort–Bustamante (2003), Wu–Kofke (2005), Hahn–Then (2009), Suárez et al. (2012, "phase
  transition in the Jarzynski estimator")** [titles and summaries only]: bias and convergence
  of exponential averaging for a *given* pair of systems and a *given* estimator.  None is a
  lower bound over algorithms or a statement over a class of energy functions.  Lemma 1 is the
  minimax counterpart: the dominant region of *every* admissible competitor must be visited by
  *every* algorithm.
* **Bennett (1976), Shirts et al. (2003), Meng–Wong (1996)**: BAR / bridge sampling is the
  minimum-variance (maximum-likelihood) estimator given samples from both states; **Shenfeld et
  al. (2009)**: variance bounds in terms of thermodynamic length for staged protocols
  [summaries].  These are efficiency statements in the *sampling-oracle* model, as are the tight
  sample-complexity results of **Štefankovič–Vempala–Vigoda (2009)** and **Harris–Kolmogorov
  (2025)** (`Õ(q/ε²)` samples, optimal) [abstracts].
* **Ge–Lee–Lu (STOC 2020)** [abstract]: `d^{1−o(1)}/ε^{2−o(1)}` queries are necessary for
  well-conditioned log-concave targets.  **He–Zhang (COLT 2025)** [search summary]:
  `(LM/(dε))^{Θ(d)}` queries for sampling from `L`-log-smooth targets — the same `B^d`-type scaling
  as Proposition 7.  **Guo–Tao–Chen (ICLR 2026)** [abstract]: upper bounds for Jarzynski/AIS in
  terms of the action of the interpolating path; no lower bounds.
* **Instance complexity with a hint**: Grossman–Komargodski–Naor (ITCS 2020) and Aaronson's
  randomised certificate complexity — as recorded in `prior_art/L7` and `reviews/R3`; the
  verifier of Theorem 2 is a hedged spot-check in that model.

### 4.3 Tools

Laplace functional of product spaces and its additive extremals: Alon–Boppana–Spencer (1998),
Bobkov–Houdré–Tetali (2006) **[K; search summary; primary not read]**.  Dobrushin uniqueness and
path coupling (Dobrushin 1968; Bubley–Dyer 1997; Hayes 2006) **[K, from memory]**.  Curie–Weiss
Glauber dynamics: Levin–Luczak–Peres (PTRF 2010) **[K; search summary]**.  Asymptotic
isoperimetry on product spaces with auxiliary variables: Ahlswede–Zhang (1999), Yu
(arXiv:2205.07596) **[abstracts]** — the natural tools for the open exponent questions; the
two-group designs of Theorem 12 are instances of such time-sharing.  Vertex isoperimetry: Harper
(1966); Bollobás–Leader (discrete torus of even side length, `ℓ₁` balls) **[K, from memory and a
secondary source, not verified in the primary]** — would give extremality of cone dips on `ℓ₁`
tori with equal constants; not used in any proof here.  Kunisky (SODA 2024),
Eldan–Koehler–Zeitouni (2020): computational optimality of Glauber dynamics for Ising models at
spectral norm `1` — a white-box counterpart of Theorem 13 **[summaries]**.  I found no
query-model statement for classes defined by second-order differences (two searches).

### 4.4 Known / new

| # | statement | status |
|---|---|---|
| 1 | Two regimes for stochastic log-partition estimation; bump lower bounds; order `(B/ln B)^d` | **K** (Holzmüller–Bach 2025) |
| 2 | `N ≈ e^{βW_diss}` for exponential averaging; `e^{KL}` for importance sampling | **K** (Jarzynski 2006; Chatterjee–Diaconis 2018) |
| 3 | Lemma 1 (comparison dips; dominance sets; dissipated-work reading) | lemma **R**, machine-checked here; formulation **N**; an equivalent family appears in workstream A |
| 4 | Theorem 2 (upper half of the threshold on every finite instance) | **N** (product case independently workstream A) |
| 5 | Theorem 3 and §2.3 (products; failure of single dips for `≥ 3` states) | independent confirmation of workstream A |
| 6 | Corollary 4 (homogeneous products: threshold = Laplace functional, hint-free) | **N** |
| 7 | Lemma 5 (circle) | **R**, probably classical |
| 8 | Theorem 6 (torus threshold `Σ ln(sinh b_i/b_i)`) | **N** |
| 9 | Proposition 7 (fixed `d`) | order **K**; instance-wise constants and the Brunn–Minkowski remark **R** |
| 10 | Lemma 9 (reference-measure soft gaps) | **R**, machine-checked here |
| 11 | Proposition 10 (free-energy differences; threshold `V_A+V_B`; ranking rule) | **N** (corollaries) |
| 12 | Proposition 11, Theorem 12 (Boltzmann averages; type-class dips; bracket) | **N** |
| 13 | Theorem 13 (dense second-order dichotomy at `w = 4`) | **N**; upper half by known tools; the Glauber transition of the Curie–Weiss model itself **K** |
| 14 | "Staging cannot help on a lattice class; its gain is in producing samples" | **R** |

### 4.5 Relation to the third referee's list (`reviews/R3`, §4)

Item 3 ("beyond the cube: is the worst-case threshold of a product class its largest Jensen
gap?"): yes for every homogeneous site (Corollary 4), with truncated additive competitors
instead of dips; instance by instance the threshold is the game value `V(g)`, which is strictly
below the Jensen gap in general (Theorems 2–3); the hint-free worst case of non-homogeneous
classes is still open.  Item 4 (two-measure isoperimetry): the threshold part is exactly a
two-measure statement (`π` and `Q*`) and is proved; the exponent part is workstream A's.  Item 5
(bridge to Holzmüller–Bach): Proposition 7 and Theorem 6 are the instance-wise and the
high-dimensional counterparts; their open problem (quadrature regime) is not touched.

### 4.6 Search log (2026-11-24; web search unless noted)

1. `Holzmüller Bach "Convergence rates for non-log-concave sampling and log-partition estimation" …` → arXiv and JMLR; **PDF fetched and read** (pp. 1–13 and the proofs of Thm 8 / Prop 9).
2. `Ge Lee Lu "Estimating normalizing constants for log-concave distributions…" query lower bound` → abstract page fetched (tool summary).
3. `query complexity lower bound estimating normalizing constant non-log-concave … annealed importance sampling Jarzynski` → Guo–Tao–Chen (abstract fetched), He–Zhang (summary).
4. `He Zhang "On the query complexity of sampling from non-log-concave distributions"` → summary.
5. `Jarzynski "Rare events and the convergence of exponentially averaged work values"` → abstract page fetched.
6. `Harris Kolmogorov "Parameter estimation for Gibbs distributions" lower bound` → abstract page fetched.
7. `minimax lower bound free energy difference estimation Bennett acceptance ratio …` → no minimax result found; BAR optimality and a thermodynamic-length variance bound (summaries).
8. `Chatterjee Diaconis "The sample size required in importance sampling"` → summary.
9. `Kunisky "Optimality of Glauber dynamics…"` → summary.
10. `Shenfeld … "Minimizing thermodynamic length…"` → summary.
11. `Dobrushin uniqueness condition general Hamiltonian black-box oracle … "value oracle"` → nothing on query lower bounds.
12. `"Phase transition in the Jarzynski estimator of free energy differences"` → summary.
13. `Bobkov Houdré Tetali "The subgaussian constant and concentration inequalities"` → summary.
14. `query complexity sampling Gibbs distribution hypercube "value oracle" … second-order … Dobrushin lower bound` → nothing relevant.
15. `Bollobás Leader "An isoperimetric inequality on the discrete torus"` → secondary source only.
16. `Levin Luczak Peres "Glauber dynamics for the mean-field Ising model…"` → summary.
17. `vertex-isoperimetric problem Hamming graph K_k^n …` → inconclusive.
18. `Ahlswede Zhang "Asymptotical isoperimetric problem"` → summary; Yu arXiv:2205.07596 abstract fetched.
19. `Wu Kofke "Phase-space overlap measures" …; Hahn Then` → summary of Wu–Kofke only.
20. `Štefankovič Vempala Vigoda "Adaptive simulated annealing…"` → summary.

Not read in the primary source: Novak (1988), Bobkov–Houdré–Tetali, Bollobás–Leader,
Levin–Luczak–Peres, Jarzynski (2006) beyond the abstract, the chemistry papers of item 19;
Zwanzig, Widom, Bennett, Crooks, Dobrushin, Bubley–Dyer are cited from memory.

---

## 5. What is not settled

1. **Boltzmann averages**: the exact threshold between `ε_set(u)` and `η_up(u)` (a gap
   `[0.707, 1]·H` at weak coupling).  Conjecture: `ε_set` is the truth.  The two bounds are the
   same design program with and without the constraint `a_g ∈ [q,1−q]` (`s09b`), so what is
   missing is an upper bound that uses the spill-over of a Lipschitz perturbation to lower
   types (and, for the lower bound, a proof that type classes are extremal: exponential-scale
   isoperimetry on Hamming slices with time-sharing).  Non-additive
   observables, response functions (`⟨E⟩`, heat capacity) and coupled macrostates (shared
   residual, where errors do cancel) were not treated.
2. **Second-order classes**: the cost for `w > 4` at accuracies above `nf_CW(w)`; whether
   adaptivity is necessary for `w ≤ 4`; non-homogeneous constants `c_ij` (Dobrushin gives the
   polynomial side under `max_iβΣ_jc_ij/4 < 1`; the droplet side needs a dense block); `k`-state
   sites; the continuous analogue (bounded mixed second derivatives on a torus) and its relation
   to the smoothness classes `m ≥ 2` of Holzmüller–Bach.  Possible overlap with workstream E
   (not seen).
3. **Hint-free worst case on non-homogeneous classes** (third referee, §4 item 3): the
   instance-wise threshold is `V(g)`; the minimax threshold over all (non-additive) instances lies
   between `sup_gV(g)` and the passive width (`0.1138` and `0.1225` per site in the two-state
   example) and needs a multi-instance lower bound or an algorithm that is not mean-based.
4. **Exponents below the threshold on continuous products**: is the cone-dip exponent
   `E(ε₁;b)` of the torus exact?  (It would follow from an `ℓ₁`-torus analogue of Harper's
   theorem; workstream A's method for finite alphabets may extend.)
5. One global `ℓ₂` constant: the exact dimension-free threshold in `[0.411, 0.5]·β²L²` (the
   extremal Lipschitz function for the Laplace functional of the flat torus) and matching
   bounds.
6. The paper proofs of Theorems 2, 3, 6, 12, 13 and Propositions 10, 11 are unrefereed; only
   Lemmas 1 and 9 and the set-dip lemmas are machine-checked, in scratch files that are not
   integrated.  In Theorem 12 parts (a), (b) are proof sketches (type counting) supported by
   exact finite-`n` computations.
7. Lower bounds in the quadrature regime (Holzmüller–Bach's open problem) were not attempted.

## 6. The three most promising next steps

1. **Make Theorem 13 a theorem of the program.**  Machine-check the droplet half (the repository
   already has mixed differences in `SecondOrderEnvelope.lean`; the statement is
   `E|Q| ≥ (1−2δ)2ⁿ/|B(r−1)|` plus a membership lemma), write the Dobrushin half with explicit
   constants, extend to heterogeneous `c_ij` and `k`-state sites, and determine the regime
   `w > 4` above `f_CW`.  It gives the program a *temperature* threshold with matching sides for a
   structured class — the first positive result for staged protocols — and a precise criterion
   for when a second-order interface is worth certifying: `βΣ_jc_ij < 4`.
2. **State the first-order theory in competitor form.**  Lemma 1, the game `V(g)` and Theorem 2
   fit on one page, hold on arbitrary instances, are half machine-checked, and connect to the
   physics literature through dissipated work.  Then prove the corresponding *exponent*
   statement on tori and settle the Boltzmann-average threshold (§5, item 1) with the
   two-measure isoperimetric tools of Ahlswede–Zhang and Yu.  This also makes the continuous
   theorem (Theorem 6) the headline for torsion-angle models.
3. **Free-energy differences with shared residuals.**  Proposition 10 shows that uncoupled states
   have no cancellation (`V_A + V_B`) and that a ranking depends only on the loser.  The relevant
   next case is two macrostates whose residuals are coupled through the envelope
   (`d(x,Tx) ≤ κ` for a matching `T`): then `Φ` reduces to a Boltzmann average of a known function
   under an unknown ensemble plus `O(βκ)`, i.e. to questions of the type of Theorem 12.  A
   threshold theorem for this "relative free energy" problem would be the statement closest to
   the practice of free-energy calculations (relative versus absolute free energies).
