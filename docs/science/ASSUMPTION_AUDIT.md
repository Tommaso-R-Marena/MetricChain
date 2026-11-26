# Assumption audit and hierarchy of generality (living file of the science division)

*Opened 2026-11-26 (checkpoint 47) on the research owner's supplementary directive "Mathematical Generality, Physical
Relevance, and Foundational Breakthroughs" (its text, verbatim: `docs/collaboration/messages/science/SCI-MSG-0029.md`
§1).  The directive's section 2 asks, for every major theorem, which assumptions are essential, which belong to the
proof, which are conveniences, which can be weakened to a quantitative condition, which change the complexity when
removed, and which make the statement false when removed; and its section 6 gives this division the task of
assessing "the assumptions, mathematical limitations, and potential relevance of theoretical results, identifying
gaps that require further mathematical investigation".  This file is where that assessment lives.  It is rewritten
in place as entries are added; consequential changes of a classification are announced by a message.*

## 0. Method

**Classes** (the directive's six, with the letters used below):

| letter | class | what counts as evidence here |
|---|---|---|
| **E** | mathematically essential: the statement cannot be made, or is empty, without it | the place in the statement where it enters; where it is "empty without", an example |
| **T** | required only by the current proof (or by the way the statement is written down) | a proof without it, written here or cited to a file; or a machine-checked statement without it |
| **C** | introduced for computational convenience | what the general object is and what it costs |
| **Q** | replaceable by a weaker quantitative condition | the condition, and a number or an instance on each side of it |
| **X** | its removal changes the computational complexity | the two complexities, with the source of each |
| **F** | its removal makes the statement false | **a counterexample that has been run here**, with a control, or a machine-checked sharpness statement |

**Evidence tags:** **[V]** machine-checked (whose file, and whether we have read the statement); **[P]** proved on
paper (where); **[X]** exhaustive enumeration; **[M]** measured on instances; **[K]** known from the literature
— *"from memory" means the source was not examined in this session and the entry is to be re-examined before it is
relied on*; **[?]** not established.

**Rules.**  (1) No classification without evidence next to it; "we believe" is written as **[?]**.  (2) Class **F**
needs a counterexample that has been run, or a machine-checked statement; a plausible construction is **[?]**.
(3) A result for a restricted model is described with its restriction in the same sentence.  (4) A generalisation
that is valid but computationally empty is called so (the directive's section 4).  (5) Open proof obligations get a
number `G-n` in §4 and stay there until proved, refuted or handed over.

## 1. Part A — the certificate calculus of this division (addenda A17 (10)–(20))

The line of work that brackets `ln Z` of a solvated side-chain ensemble deterministically.  What its statements
actually use is less than what its instances are (peptides on a helix, rotamer libraries, an implicit solvent).

### A1. The sandwich

*Statement.*  If `m₋ ≤ E ≤ m₊` pointwise, then `ln Z(m₊) ≤ ln Z(E) ≤ ln Z(m₋)`.

| assumption as used | class | evidence, and what the general object is |
|---|---|---|
| the space is finite | **T** | monotonicity of the integral: holds on any σ-finite measure space `(Ω, ν)` with `Z(m) = ∫e^{−βm}dν`, `m₊` allowed the value `+∞` [P, one line] |
| the floor holds on **all** of the space | **F** for the upper end | `experiments/science/assumption_audit/aa01_essential.py` (3): two modes, a floor valid around one of them, the "upper end" is below the exact `ln Z`; repaired floor: holds [X] |
| the ceiling holds on all of the space | **T** | a ceiling may be `+∞` outside any region: the lower end survives restriction to one mode (same example) [X].  *The two ends are not symmetric:* a lower bound of `Z` needs no knowledge of the rest of the space, an upper bound needs all of it — the place where "an ensemble not concentrated near one reference", "several modes" enter this line is the **floor** |
| `Z(m₋)`, `Z(m₊)` exactly computable | **X** | this is the content of the certificate: see A5 |

### A2. The remainder identity

*Statement* (workstream P3; machine-checked by the theory division as `higherOrder_remainder`, and with one order
per term as `anchored_remainder_identity_orders`).  On a product space `X = ΠX_i` with an anchor `x⁰`, for every
total order of the sites, `F(x) − I_{m−1}F(x) = Σ_{T ⊆ S(x), |T| = m} Δ_T F(z^{T,x}; x_T)`: the error of the expansion
from the Hamming ball of radius `m − 1` is a sum of order-`m` mixed differences between anchor state and actual
state of the sites of `T`, in a context fixed by the order.

| assumption as used | class | evidence |
|---|---|---|
| a product structure ("sites") | **E** | it defines the objects of the statement |
| finite alphabets | **T** | the identity involves, for a given `x`, only the two states `x⁰_i`, `x_i` of each site; the theory division's Lean setting is, by its own description, a finite index type of sites with arbitrary alphabets with decidable equality [V, theirs; `TermOrders.lean`, `HigherOrderEnvelope.lean` — **statements not read by us**; description from their `LE_brief.md` at `8ff0667`] |
| one anchor, a configuration | **C** for the identity (any `x⁰`); for what it buys see A8 | — |
| one order of the sites for all terms | **T**, up to "a term has at most `m` hosts", which is **F** beyond | [V, theirs: `anchored_remainder_identity_orders`, `term_orders_sharp`; not read by us]; first seen as a gap by the coordinator's check of workstream P8 (SCI-MSG-0027) |

### A3. The envelope: a bound of the remainder, resolved by state

*Statement* (workstream P9, Theorem R; P8's Theorem AH and P3's Theorem 3 before it).
`|g(x) − I_{m−1}g(x)| ≤ Σ_{T ⊆ S(x), |T| = m} Θ_T(x_T)`, the table `Θ_T` uniform in the states of all other sites.

| assumption as used | class | evidence |
|---|---|---|
| **some** bound on the order-`m` mixed differences of `g` | **F** without | `aa01_essential.py` (1): two functions that agree on the whole ball of radius `m − 1` — every evaluation and every evaluated term the same — with `ln Z` apart by 0.009, 0.18, 3.4, 13.4 nats as one number grows; with a pointwise bound of the remainder in force, the sandwich contains both [X].  *No certificate from evaluations on a ball alone, for any ball smaller than the space* |
| `g` is the generalised-Born term of one force field (GBn2) | **C**, replaceable by a structural condition — see A3′ | [P] by reading P9's proof of Lemma T′ and Theorem R (`workstreams/P9_REPORT.md` §1): the functional form enters through three facts only |
| `m ≥ 3` | **T** / **Q** | used once, to place the (at most two) hosts of a term that are not in `T` at the anchor; the general condition is the one of A2 (hosts per term at most `m`) [P9's proof, step (b); V for the identity] |
| the tables are computed without error | see A9 | — |

**A3′. What the proof uses of `g` — the general class [P by reading; the general statement is Proposition AA.1
below, elementary; not yet tested on an instance that is not GBn2: `G-1`].**  Each term `τ` of `g` is a smooth
function of (i) quantities fixed by the states of a bounded number of *host* sites and (ii) **statistics that are
additive over the remaining sites**, `I_p(x) = c + Σ_i C^p_i(x_i)`.  Nothing else is used.  So the envelope exists,
with the same proof, for every energy whose many-body part is a sum of terms `φ(u(x))`, `u(x) = c + Σ_i a_i(x_i) ∈ ℝ^r`
with `φ` of class `C^m` on the convex hull of the values of `u` — which is the form of many non-decomposable
interactions (implicit-solvent terms through effective radii; embedding functions of a local density; a function
of a coordination number or of a total dipole).

> **Proposition AA.1 (mixed differences of a function of site-additive statistics) [P, elementary; in substance
> known — the mean-value form of a finite difference].**  Let `X = ΠX_i` (any sets), `a_i: X_i → ℝ^r`,
> `u(x) = c + Σ_i a_i(x_i)`, `φ ∈ C^m` on an open convex set containing `u(X)`, `T = {i_1, …, i_m}`, a context `z`
> with `z_T = x⁰_T`, states `y_T`, and `d_i = a_i(y_i) − a_i(x⁰_i)`.  Then
> `Δ_T(φ∘u)(z; y_T) = ∫_{[0,1]^m} D^mφ(u(z) + Σ_{i∈T} t_i d_i)[d_{i_1}, …, d_{i_m}] dt`, hence
> `|Δ_T(φ∘u)(z; y_T)| ≤ M_m·Π_{i∈T} ‖d_i‖`, `M_m` the supremum of the norm of `D^mφ` over the hull.
> *Proof.*  `h(t) = φ(u(z) + Σ_{i∈T} t_i d_i)` on the cube; its mixed difference over the cube is the integral of
> `∂^m h/∂t_{i_1}…∂t_{i_m} = D^mφ(·)[d_{i_1}, …, d_{i_m}]`; the points of evaluation are convex combinations of
> values of `u` at configurations.  ∎
>
> **Corollary AA.2 (the envelope is an elementary symmetric polynomial) [P].**  With the identity of A2, for every
> `x`: `|(φ∘u)(x) − I_{m−1}(φ∘u)(x)| ≤ M_m·e_m(δ_i(x_i): i ∈ S(x)) ≤ M_m·(Σ_{i∈S(x)} δ_i(x_i))^m / m!`, where
> `δ_i(x_i) = ‖a_i(x_i) − a_i(x⁰_i)‖` and `e_m` is the elementary symmetric polynomial of degree `m`.  The resolved
> table of a subset has rank one: `Θ_T(x_T) = M_m·Π_{i∈T} δ_i(x_i)`.

*What this changes in the reading of our results.*  (a) "Few side chains off the anchor" is not the condition of
the envelope; **a small total displacement of the additive statistics, `Σ_{i∈S(x)} δ_i(x_i)`, measured against the
curvature scale `M_m^{−1/m}`,** is.  Many sites may be off the anchor if each moves its statistic little.
(b) The mean of such an envelope under any band model is exactly computable although the envelope is not
band-limited (a transfer matrix with polynomial entries truncated at degree `m` extracts `⟨e_m(δ)⟩`) [P, standard;
not implemented: `G-1`].  (c) For few statistics the many-body term needs no expansion at all: see level H2′ of §3.

### A4. Allocation of a state-dependent bound to tables (workstream P9, Proposition P)

| assumption as used | class | evidence |
|---|---|---|
| chain, band, geometry | — (not used) | the statement is about weights and domination on finite index sets; machine-checked by the theory division since `3cf14b9` (`ResolvedPenalties.lean`: `resolved_allocation`, `resolved_allocation_max`, `reduction_step`, `resolved_remainder_bound`; alphabets arbitrary types; docstring and theorem list read by us) [V, theirs] |
| non-negative bounds `Φ_T` | **E** for the enlargement steps of the proof | [P, P9_REPORT §1]; no counterexample constructed: **[?]** whether a signed version has any use |

### A5. Tractable models: a band on a chain, exact by transfer matrix; reductions by maxima and minima

*Statement.*  Models whose terms all lie within `w + 1` consecutive sites have `ln Z` and window marginals exact
at cost `O(n·k^{w+1})`; a term that fits no window is replaced by its maximum (ceiling) or minimum (floor) over
the sites given up; a pair beyond the band is split around the anchor.

| assumption as used | class | evidence |
|---|---|---|
| the interaction graph is a chain with a band | **C** for validity (every step is a pointwise inequality); **X** for cost | exact partition functions of general pairwise models are hard, and bounded treewidth is the known tractable class with cost exponential in the width [K, **from memory — sources not examined in this session**; to be cited after examination].  The held-site passes of A7 are conditional marginals and exist on any tree decomposition [?: not written, not built — `G-3`] |
| the band is wide enough to hold what matters | **Q** | not needed since part (19): the slack of everything the band gives up is a known table and is taken back (A6); a band of 4 with the recovery is tighter than a band of 7 without [M, Lys₁₂: `6.9·10⁻⁴` against `7.3·10⁻³` nats; part (19), item 74] |
| finite alphabets (rotamers) | **X** / **[?]** | with a continuous site variable the transfer matrix becomes an integral operator; a certificate then needs a bound of the variation of every table over a cell and carries a quadrature allowance — not formulated here: `G-5` |

### A6. Recovery of the known slack (Proposition A17.19)

*Statement.*  For non-negative `S⁺_g`, `S⁻_g` with `Σ_g S⁺_g ≤ m₊ − E`, `Σ_g S⁻_g ≤ E − m₋`, and means `⟨·⟩` under the
ceiling: (LJ) `ln Z(E) ≥ ln Z(m₊) + βΣ⟨S⁺_g⟩`; (LP) `≥ ln Z(m₊) + ln(1 + Σ⟨e^{βS⁺_g} − 1⟩)`; (UE), (UP) upper ends by
a monotone iteration with `C = Σ⟨S⁻_g e^{βS⁺_g}⟩`, `C′ = Σ⟨(e^{βS⁻_g} − 1)e^{βS⁺_g}⟩`.

| assumption as used | class | evidence |
|---|---|---|
| the space is finite | **T** | **the proof uses nothing but Jensen's inequality, `Π(1 + y_g) ≥ 1 + Σy_g` for `y_g ≥ 0`, and a change of measure; it is written below for any σ-finite measure space** [P].  The finite form is machine-checked by the theory division since `3cf14b9` (`GibbsRecovery.lean`: `lower_jensen`, `lower_product`, `upper_jensen`, `upper_product`, the two iterations; statements read by us, hypotheses as ours — (LJ) without sign conditions) [V, theirs; their audit at that head is being repeated here] |
| every group slack is non-negative | **F** for (LP), (UE), (UP); **T** for (LJ) | `aa01_essential.py` (2): two groups whose slacks cancel pointwise satisfy the hypothesis on the sum, and (LP) as a formula exceeds the exact `ln Z` by `ln 1.25`; (LJ), which is Jensen, holds for any real `s₊ ≤ m₊ − E`; control: the same slack as one non-negative group, where (LP) is attained [X] |
| the laws of the group slacks under the ceiling are known exactly | **Q** | any lower bounds of `⟨S⁺_g⟩`, `⟨e^{βS⁺_g} − 1⟩`, `C`, `C′` keep all four inequalities; estimates from samples turn them into statements with a confidence level, a different kind of certificate |
| which items form a group | **C** for validity, **Q** for tightness | any partition is valid; items whose slack occurs at the same states must share a group or their cross terms are lost [M: 0.0083 against 0.0029 nats on Lys₅ at band 2, part (19) item 70] |
| nothing is assumed about the joint law of different groups | the price of this is a loss of about `D²/4` (`D` the width of the sandwich) | [M, part (19) item 73].  Whether the product inequality is the best possible from the group laws alone is our question A19-T2; the theory division has checks in progress (not yet a statement of theirs) |
| the ceiling is a band model | **C** | the proposition holds for any model; exact means need a model whose conditional marginals are computable |

> **Proposition A17.19, measure-space form [P; the proof of part (19), item 69, read without finiteness].**
> Let `(Ω, ν)` be σ-finite, `β > 0`, `m₋ ≤ E ≤ m₊` measurable with values in `(−∞, +∞]`, `0 < Z(m₊)` and
> `Z(m₋) < ∞`; `S^±_g ≥ 0` measurable, `g` in a countable set, `Σ_g S⁺_g ≤ m₊ − E` and `Σ_g S⁻_g ≤ E − m₋` where the
> right-hand sides are defined.  Then (LJ), (LP), (UE), (UP) hold, with `⟨X⟩ = ∫X e^{−βm₊}dν / Z(m₊)`.
> *Proof.*  `Z(E)/Z(m₊) = ⟨e^{β(m₊−E)}⟩ ≥ ⟨e^{βΣ_g S⁺_g}⟩`, which is at least `e^{βΣ_g⟨S⁺_g⟩}` (Jensen; monotone
> convergence for the sum) and at least `1 + Σ_g⟨e^{βS⁺_g} − 1⟩` (the product inequality, termwise non-negative).
> For the upper ends write `⟨·⟩_E` for the mean under `e^{−βE}dν/Z(E)`:
> `Z(m₋)/Z(E) = ⟨e^{β(E−m₋)}⟩_E ≥ 1 + Σ_g⟨e^{βS⁻_g} − 1⟩_E` and `≥ e^{βΣ_g⟨S⁻_g⟩_E}`; and for measurable `X ≥ 0` and
> each `g`, since `E ≤ m₊ − S⁺_g`, `⟨X⟩_E ≥ (Z(m₊)/Z(E))·⟨X e^{βS⁺_g}⟩ ≥ e^{ln Z(m₊) − u}⟨X e^{βS⁺_g}⟩` whenever
> `ln Z(E) ≤ u`.  Each right-hand side of (UE), (UP) is non-decreasing in `u`, so the iteration from
> `u₀ = ln Z(m₋)` stays above `ln Z(E)`.  ∎

### A7. Exact means by held-site passes (part (19), item 70)

| assumption as used | class | evidence |
|---|---|---|
| chain with a band; an item has all its sites but one inside one window of `w` sites | **C** | the law of (held site, window) is `exp(forward message with the site held + backward message + terms inside)`; tested against enumeration to `10⁻¹²` [X, Lys₅ at band 2].  Items with two sites at each end need two held sites — cost `k²` passes — not built |
| the chain is at most `2w` long (so that the window can be the last or the first `w` sites) | **C** — being removed | a window anywhere on the chain: built and tested against enumeration, regression runs in progress when this was written (research log, cycle 60; not yet in the addenda and its code not yet in the tree) |

### A8. Conditions for a *narrow* bracket (not for a valid one)

Every bracket of this line is valid whether or not these hold; they decide whether it is worth having.

| condition as it is usually said | class | what it is, quantitatively |
|---|---|---|
| "the ensemble is concentrated near one reference configuration" | **Q** | what enters is `β⟨Σ_{T⊆S(x)}Θ_T(x_T)⟩` under floor and ceiling.  Ser₁₂ has 6.3 of 12 side chains off the anchor on average and is certified within `1.8·10⁻³` nats at order 5; Lys₁₂ has 1.2 off and needs order 4 for `8·10⁻⁵` [M].  By A3′ the intrinsic quantity is the displacement of the additive statistics, not the Hamming distance |
| "the floor stays at the anchor" | **Q**, **criterion open** | the floor is the model minus the penalty; if the penalty grows faster with the number of displaced sites than the cost of displacing them, the floor's own Gibbs measure leaves the anchor and there is no certificate ((LKSE)₃ at order 3: a bracket of 658.9 nats, workstream P9; "about whether a floor delocalises" P9's own predictions were wrong five times of nine — question P9-T2 to the theory division, in progress there).  For an envelope `M_m·e_m(δ)` whose `M_m` does not decay with the spread of the sites, the penalty of `s` displaced sites grows like `s^m` and the cost at most linearly: **such a floor delocalises on a long enough chain at any fixed order** [P, a growth comparison; no rate function computed: `G-4`].  What saves the instances is that `Θ_T` is tiny for spread-out `T` |
| "the band holds what matters" | **Q** | see A5, A6 |

### A9. What every number of this line assumes and has not proved

| assumption | class | status |
|---|---|---|
| each value of `g` is computed within `ε_g = 10⁻⁷` kcal/mol | **E** (some bound is needed: a certificate cannot be more accurate than its evaluator) | **unproved** for the summation order of the evaluator used (workstream P3: an a-priori `3·10⁻⁸`; measured `2·10⁻¹²`); request A19-E2 to the engineering division |
| the instance: fixed backbone, a rotamer library, an implicit solvent, one force field | modelling choices, outside the mathematics | the statements above use only: a finite product space, a pairwise part, a many-body part of the class A3′ |

### A10. What the ball and the envelope allow at best: the box limit [added after the referee of Part A was launched; not in its brief]

> **Proposition AA.3 (the box limit) [P, two lines; X on three enumerated instances].**  Let all that is known of
> an energy `E` be a function `m₀` and a pointwise bound `|E − m₀| ≤ env` (in our certificates `m₀ = f + I_{m−1}g`, known
> from the ball, and `env` the resolved envelope).  Then (i) every interval that contains `ln Z(E)` for all `E`
> compatible with this knowledge contains `[ln Z(m₀ + env), ln Z(m₀ − env)]`; so no rule that uses this knowledge
> alone certifies `ln Z` more narrowly than
> `W* = ln Z(m₀ − env) − ln Z(m₀ + env) = ln⟨e^{β·env}⟩_{m₀} − ln⟨e^{−β·env}⟩_{m₀} = 2β⟨env⟩_{m₀} + O(β³)`
> (the even cumulants of `env` cancel); (ii) the sandwich of the two extreme members attains `W*`.
> *Proof.*  `m₀ + env` and `m₀ − env` are compatible; an interval valid for both contains both values.  ∎

The statement is trivial; what it buys is a **yardstick that separates the three things a certificate can lose**:
information (the box limit `W*`, which no computation with the same knowledge can beat), tractability (a band
model cannot hold `m₀ ± env`, so the sandwich has `D ≥ W*`), and the inequalities of the recovery.  By enumeration
(`experiments/science/assumption_audit/aa02_box_limit.py`; the certificate's numbers are those of the committed
logs of `first_order_recovery.py`):

| instance, order | box limit `W*` | `W*` over its first-order value `2β⟨env⟩` | sandwich `D` at band 2; 3 | `D / W*` | corrected bracket at band 2; 3 | corrected `/ W*` | envelope over remainder, pointwise: least; median |
|---|---|---|---|---|---|---|---|
| Lys₅, 4 | `4.389·10⁻⁵` | 1.000 | 0.0477; 0.0189 | 1 086; 431 | 0.00289; `6.44·10⁻⁵` | 65.7; **1.47** | 10.8; 373 |
| Lys₅, 5 | `7.98·10⁻⁹` | 1.000 | —; 0.0187 | —; `2.3·10⁶` | —; `7.1·10⁻⁶` | —; 890 | 12.5; 449 |
| LKSE:5, 4 | `8.459·10⁻⁵` | 1.000 | 0.2054; — | 2 428; — | 0.00156; — | 18.4; — | 17.0; 312 |

(The exact `ln Z` is inside every box, and every corrected bracket contains its box, as it must.)  What the table
says, classification by classification:

| statement | class | evidence |
|---|---|---|
| "a wide band is needed for a narrow bracket" | **C** — the band is a tractability device, not a limit of information | at order 4 and band 3 the recovered bracket is within a factor 1.47 of the box limit, where the plain sandwich is 431 times it [X] |
| "the envelope decides the width" | **E** for any rule that uses only the ball and the envelope (Proposition AA.3) | — |
| "the width is first-order in the envelope" | **Q** | `W* = 2β⟨env⟩` to three digits in all three rows [X]; the correction is of third order |
| "the envelope is the remainder" | **F** | the envelope exceeds the remainder at every state by a factor of at least 10.8 to 17.0 (median 312 to 449), and the exact `ln Z` sits within 1.2 per cent of the middle of the box [X].  **A control of ours could not fail for this reason**: halving every table violates nothing at any of the 115 248 states; the control now divides by 1 000 (79 657 violations).  What order 4 would gain most from is a tighter envelope, and the sign-blind bounds behind the tables cannot give it (finding S76) |
| "more order is always better" | **Q** | at order 5 the box limit (`8·10⁻⁹`) is far below what the certificate reaches (`7·10⁻⁶`): the limit there is the evaluation allowance `ε_g` (A9) and the inequalities, not information |

## 2. Part B — the theory division's theorems: not a second audit, an input to theirs and a review of it

*Changed on the day it was written.*  All three divisions received the directive directly, and the theory
division answered our question of SCI-MSG-0029 §3 before it was sent: it writes the audit of its own theorems
(`docs/ASSUMPTION_AUDIT.md` on its branch, by readers who did not write them; THY-MSG-0016 §3) and asks of us
(its suggestion G-S1) **the assumptions of its §11 that our instances violate, each with the quantitative
substitute we would consider meaningful**.  So this part holds, in order: (a) that list — first version in
SCI-RES-0023 §2, eight rows, reproduced in short below; (b) the same list against their theorem numbers
(**owed**: after a reading of their §11, or against the first version of their audit); (c) our review of their
audit when it exists.  The engineering division decides candidates of the form "proved under H, believed or
doubted under H′" on finite instances (ENG-MSG-0006 §2; agreed in SCI-RES-0022).

| # | assumed in their sharpest results (from our reviews; their audit's wording will replace this column) | our instances | substitute we would consider meaningful |
|---|---|---|---|
| 1 | product or exchangeable known part | a band model on a chain | exact oracle access to the known part (`Z`, window marginals, samples, conditional laws given a held site); or its correlation length — not yet computed |
| 2 | one slope, first-order (Hamming) envelope | an order-`m`, state-resolved, very heterogeneous envelope | a box class with a state-dependent box, described by the Gibbs mean of the box and its exponential moment, not by its supremum |
| 3 | binary letters | 3 to 14 letters, different per site | per-site alphabets and per-site probabilities of leaving the anchor |
| 4 | symmetric envelope, one hardest member | no symmetry; floor and ceiling differ | the cost of narrowing a box by further evaluations (their Propositions 11.113, 11.113a, 11.113b) |
| 5 | exponents as `n → ∞` | `n ≤ 30`, `10⁻²`–`10⁻⁵` nats | explicit constants at finite `n` |
| 6 | exact evaluations | a tolerance per evaluation, unproved | an evaluation allowance carried through the certificate |
| 7 | one reference instance | one anchor; a floor that can leave it | `ln⟨e^{β·env}⟩ = O(1)`; beyond it a cover by several anchors, with no cost statement yet |
| 8 | the algorithm only evaluates | white-box tables from the analytic form | a second oracle: a certified bound of an order-`m` mixed difference, resolved by state (class A3′) |

*Linked correction (SCI-RES-0025).*  SCI-RES-0023 §2 said of the box class of row 2 "lower bound: none that we
know".  There is one, theirs: Proposition 11.113 (d) — the order `sinh²(Δ/2)/ε²` of evaluations is necessary in the
worst case over `{m₋ ≤ E ≤ m₊}` for a fine-grained sampler — reviewed by us in SCI-REV-0013 and SCI-REV-0015.  Open,
as far as that proposition goes: the narrower box left by known slack whose ends are not tractable models; the
second oracle of row 8; a sampler that is not fine-grained; deterministic algorithms.

One structural remark that our review of their audit will test: functions of a Hamming weight, of a type, of a
block profile are functions of **site-additive statistics with equal weights** — the class A3′ with exchangeable
`a_i`.  The natural heterogeneous generalisation of results proved by the method of types is to unequal `a_i`,
with level sets of weighted sums in place of type classes; whether their exponents survive in that form, and at
what cost, is a question we will put precisely (`G-6`).

## 3. Part C — a hierarchy for certified `ln Z`, from tractable models outward

Each level names what is assumed of the energy, what a certificate costs, and what is known to fail beyond it.
**[P]** and **[M]** refer to entries above; **[K, from memory]** and **[?]** are to be examined or proved.

| level | the energy | certificate | cost | what stops it |
|---|---|---|---|---|
| H0 | a sum of one-site terms | exact product | `O(nk)` | — |
| H1 | pairwise on a chain or tree | exact, transfer matrix | `O(nk²)` | — |
| H2 | all terms within a band `w` (bounded treewidth) | exact | `O(nk^{w+1})` | the width: exact partition functions on general graphs are hard [K, from memory] |
| H2′ | H2 plus `φ(u(x))`, `u` a vector of `r` site-additive statistics, `φ` Lipschitz, otherwise arbitrary | exact up to a binning allowance: a transfer matrix that also carries the binned partial sums; floor and ceiling from the extreme values of `φ` on a cell | `O(nk^{w+1}B^r)` for `B` bins per statistic; width `≲ β·Lip(φ)·n·`(cell size) | `r`: exponential in the number of statistics — a parameter, not the size of the system [P in outline, standard dynamic programming; **not implemented, not tested: `G-2`**] |
| H3 | H2 plus a many-body part with a pointwise envelope of its order-`m` remainder (A3; class A3′ with any `r`) | sandwich from the ball of radius `m − 1` | `Σ_{s<m} C(n,s)(k−1)^s` evaluations, `C(n,m)` tables | the envelope: no certificate without it (A3, **F**); no width below the box limit `W* = 2β⟨envelope⟩ + O(β³)` with the same knowledge (A10, Proposition AA.3) |
| H4 | H3 with the slack of every reduction known as tables | sandwich + recovery (A6) | held-site passes: `k` transfer-matrix runs per held site | envelope; `D²/4` between groups; items that need two held sites |
| H5 | H3, sampled | a sampler inside the sandwich (the theory division's Propositions 11.113, 11.113a) | evaluations growing with the width of the sandwich | a statistical statement, not a deterministic one |
| H6 | no tractable floor (several modes; a floor that delocalises) | lower ends only (restriction, A1); an upper end needs a cover of the space | — | first-order information alone costs exponentially many evaluations (the theory division's lower bounds for first-order classes; our reviews SCI-REV-0001…0016) |

## 4. Part D — gaps and proof obligations

| id | what is missing | whose | status |
|---|---|---|---|
| `G-1` | Proposition AA.1 / Corollary AA.2 tested where they are not GBn2: a synthetic many-body energy `Σ_p φ(c_p + Σ_i a_{p,i}(x_i))` at every state, with a control; the polynomial transfer matrix for `⟨e_m(δ)⟩` | science (coordinator) | open |
| `G-2` | level H2′ stated with its allowance and implemented on a synthetic instance; comparison with H3 on the same instance (few statistics against many) | science | open |
| `G-3` | held-site passes on a tree decomposition (a graph that is not a chain) | science; a request to engineering if it grows | open |
| `G-4` | a criterion for a floor to stay localised, from quantities cheaper than the floor itself; the growth comparison of A8 made into a statement with a rate function | theory (our question P9-T2; in progress there) and science | open |
| `G-5` | a continuous site variable: what the tables must satisfy, the quadrature allowance, where it fails (a table that is not Lipschitz on a cell) | science | open |
| `G-6` | the theory division's exchangeable results with unequal site weights: which exponents survive | to be put to theory after Part B | open |
| `G-7` | Part B (b): the list of SCI-RES-0023 §2 against the theory division's theorem numbers; (c): a review of their audit when it exists | science | open |
| `G-8` | sources for the three **[K, from memory]** entries (hardness of general partition functions; treewidth; information-based complexity of smooth classes) examined and cited, or the entries removed | science | open |

## 5. Counterexamples run (index)

| script, log | what it shows | class supported |
|---|---|---|
| `experiments/science/assumption_audit/aa02_box_limit.py`, `aa02_box_limit_{K5_m4,K5_m5,LKSEc5_m4}.log` | the box limit `W*` by enumeration against the certificate's sandwich and corrected bracket; the envelope against the remainder at every state, with a control that fails (÷1000) and one that cannot (÷2) | A10 |
| `experiments/science/assumption_audit/aa01_essential.py`, `aa01_essential.log` | (1) no certificate from a ball alone; (2) (LP) fails with a negative group slack, (LJ) does not; (3) the floor must hold everywhere, the ceiling need not | A3 **F**; A6 **F** / **T**; A1 **F** / **T** |
