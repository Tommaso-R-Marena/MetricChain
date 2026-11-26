# Assumption audit and hierarchy of generality (living file of the science division)

*Opened 2026-11-26 (checkpoint 47) on the research owner's supplementary directive "Mathematical Generality, Physical
Relevance, and Foundational Breakthroughs" (its text, verbatim: `docs/collaboration/messages/science/SCI-MSG-0029.md`
§1).  The directive's section 2 asks, for every major theorem, which assumptions are essential, which belong to the
proof, which are conveniences, which can be weakened to a quantitative condition, which change the complexity when
removed, and which make the statement false when removed; and its section 6 gives this division the task of
assessing "the assumptions, mathematical limitations, and potential relevance of theoretical results, identifying
gaps that require further mathematical investigation".  This file is where that assessment lives.  It is rewritten
in place as entries are added; consequential changes of a classification are announced by a message.*

***Refereed.***  *Part A at the state of commit `0930440` (A1–A9, Propositions AA.1, AA.2, the measure-space form of
A17.19, level H2′) was reviewed adversarially by workstream R19 on 2026-11-26 (`docs/science/workstreams/R19_REPORT.md`,
§5; an internal review by an AI session, not external peer review): of 27 classified rows 19 confirmed, 5 weakened
or reworded, 3 rejected as written; four major findings (M1–M4) and fifteen minor ones.  Every change made on that
review is marked **[R19 …]** in place and listed in §6; it is announced in SCI-MSG-0030.  Not refereed: A10 and
Proposition AA.3, Parts B–D except H2′.*

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
| the ceiling is **finite** on all of the space | **T** | `E ≤ m₊` is needed only where `m₊ < ∞`: `ln Z(E) ≥ ln ∫_{m₊<∞} e^{−βm₊}dν`; the lower end survives restriction to one mode (same example) [P, one line; X].  *The two ends are not symmetric:* a lower bound of `Z` needs no knowledge of the rest of the space, an upper bound needs all of it — the place where "an ensemble not concentrated near one reference", "several modes" enter this line is the **floor**.  **[R19 M2]** *This row read "the ceiling holds on all of the space: **T**", which was wrong as worded: what can be dropped is finiteness, not validity — next row* |
| `E ≤ m₊` wherever `m₊` is finite | **F** | a *finite* model that is a ceiling on one mode only gives a "lower end" of 2.72 against `ln Z = 0.88` on the ten-state example; control, a finite ceiling valid everywhere: 0.45 [X, R19: `ws_R19/r19_audit_tests.py` S7].  A restricted ceiling is computable only if the region is tractable for the model class: a sub-product of the alphabets is, a Hamming ball is not band-limited **[R19 M2, new row]** |
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
| `g` is the generalised-Born term of one force field (GBn2) | **C**, replaceable by a structural condition — see A3′ | [P] by reading P9's proof of Lemma T′ and Theorem R (`workstreams/P9_REPORT.md` §1): the functional form enters through three facts only.  **[R19 M3]** the structural condition as we first stated and proved it (AA.1, AA.2) excludes hosts — and GBn2 has hosts; the statement that covers our own instance is AA.1′ below |
| `m ≥ 3` | **Q** | `m > h` (`h` hosts per term) for an envelope built from derivative bounds: the proof uses it twice — step (b) of Theorem R (a host outside `T` at the anchor: `h ≤ m`) and Lemma T′, which needs a non-host site in every `T` (`h ≤ m − 1`).  `h ≤ m` suffices for the identity and for abstract constants [V, theirs: `anchored_remainder_bound_hosts`], but at `h = m` the table of `T = ` (the hosts) is the hosts' mixed difference times `sup abs(φ)` and does not vanish with the displacement: two hosts, `m = 2`, all additive increments zero — remainder 0.80 at order 2, `6·10⁻¹⁷` at order 3 [X, R19 S7].  **[R19 m2]** *This row read "**T** / **Q** — used once …; the general condition is … hosts per term at most `m`"* |
| the tables are computed without error | see A9 | — |

**A3′. What the proof uses of `g` — the general class [P by reading; the statement without hosts is Proposition AA.1
below, elementary, with hosts Proposition AA.1′; tested by workstream R19 on synthetic energies that are not GBn2,
with controls: `G-1` discharged — see after AA.2].**  Each term `τ` of `g` is a smooth
function of (i) quantities fixed by the states of a bounded number of *host* sites and (ii) **statistics that are
additive over the remaining sites**, `I_p(x) = c + Σ_i C^p_i(x_i)`.  Nothing else is used.  So the envelope exists,
with the same proof, for every energy whose many-body part is a sum of terms `φ_c(κ(c) + Σ_{i∉H} a^c_i(x_i))`, `c = x_H`
the state of fewer than `m` host sites, each `φ_c` of class `C^m` on the convex hull of the values of its argument
(Proposition AA.1′).  **Without hosts** — terms `φ(u(x))`, `u(x) = c + Σ_i a_i(x_i) ∈ ℝ^r` — the bound is a product over
the sites (AA.1, AA.2): a function of a coordination number or of a total dipole is of this kind.  Implicit-solvent
terms through effective radii and embedding functions of a local density are additive only *for a fixed state of
the host* and belong to AA.1′.  **[R19 M3]** *Before the review this paragraph described the class with hosts and then
stated and proved the proposition without them, as "the general statement"; treating a host as one more additive
site makes Corollary AA.2 false (1 253, 2 630, 2 068 violations at `m = 2, 3, 4` on 200 random instances with one
host; R19 S8).*

> **Proposition AA.1 (mixed differences of a function of site-additive statistics) [P, elementary; in substance
> known — the mean-value form of a finite difference].**  Let `X = ΠX_i` (any sets), `a_i: X_i → ℝ^r`,
> `u(x) = c + Σ_i a_i(x_i)`, `φ ∈ C^m` on an open convex set containing `u(X)`, `T = {i_1, …, i_m}`, a context `z`
> with `z_T = x⁰_T`, states `y_T`, and `d_i = a_i(y_i) − a_i(x⁰_i)`.  Then
> `Δ_T(φ∘u)(z; y_T) = ∫_{[0,1]^m} D^mφ(u(z) + Σ_{i∈T} t_i d_i)[d_{i_1}, …, d_{i_m}] dt`, hence
> `|Δ_T(φ∘u)(z; y_T)| ≤ M_m·Π_{i∈T} ‖d_i‖`, `M_m` the supremum over the hull of the operator norm of `D^mφ` **induced by
> the norm used for the increments** (with Euclidean increments and the `ℓ¹` operator norm the bound fails:
> `φ = (u₁ + u₂)²/2`, two sites with increments `(1, 1)`: remainder 4, "bound" 2); for infinite `X_i`, `M_m` may be
> `+∞` **[R19 m14]**.
> *Proof.*  `h(t) = φ(u(z) + Σ_{i∈T} t_i d_i)` on the cube; its mixed difference over the cube is the integral of
> `∂^m h/∂t_{i_1}…∂t_{i_m} = D^mφ(·)[d_{i_1}, …, d_{i_m}]`; the points of evaluation are convex combinations of
> values of `u` at configurations.  ∎
>
> **Corollary AA.2 (the envelope is an elementary symmetric polynomial) [P].**  With the identity of A2, for every
> `x`: `|(φ∘u)(x) − I_{m−1}(φ∘u)(x)| ≤ M_m·e_m(δ_i(x_i): i ∈ S(x)) ≤ M_m·(Σ_{i∈S(x)} δ_i(x_i))^m / m!`, where
> `δ_i(x_i) = ‖a_i(x_i) − a_i(x⁰_i)‖` and `e_m` is the elementary symmetric polynomial of degree `m`.  The bound of
> **one host-free term** on a subset is a product over its sites (rank one): `Θ_T(x_T) = M_m·Π_{i∈T} δ_i(x_i)`; a sum
> of `P` terms has rank up to `P`, and neither the true mixed difference nor workstream P9's table of a subset (a sum
> over terms, blocks, host states and partitions) is a product **[R19, §5.1]**.
>
> **Proposition AA.1′ (terms with hosts) [P: workstream P9's Lemma T′ and step (b) of its Theorem R, which need
> `m > h`; N: R19 for `h = 1`] — [R19 M3], the referee's formulation.**  Let `τ(x) = φ_c(κ(c) + Σ_{i∉H} a^c_i(x_i))` with
> `c = x_H`, `|H| = h < m`, each `φ_c ∈ C^m` on an open convex set containing the values of its argument, and take an
> order of the sites with `H` last.  For `T ⊆ S(x)`, `|T| = m`:
> `|Δ_T τ(z^{T,x}; x_T)| ≤ Σ_{c ∈ 𝒞_x(T)} M^c_{m−|H∩T|}·Π_{i∈T∖H} δ^c_i(x_i)`, where `𝒞_x(T)` has `c_l = x⁰_l` for
> `l ∈ H∖T` and `c_l ∈ {x⁰_l, x_l}` for `l ∈ H∩T`, `δ^c_i(y) = ‖a^c_i(y) − a^c_i(x⁰_i)‖`, and `M^c_j` is the supremum
> over the hull, for host state `c`, of the operator norm of `D^jφ_c` induced by `‖·‖`.  The table of `T` is a sum of
> at most `2^h` products over the non-host sites of `T` — rank one only for `h = 0`.
>
> *Tests (R19, `ws_R19/r19_audit_tests.py`, no code of ours; re-run by the coordinator, output identical).*  AA.2 on
> 300 synthetic energies `Σ_p φ_p(c_p + Σ_i a_{p,i}(x_i))` (exponentials, sines, inverse powers, powers; 1–5 terms), every
> state, `m = 2 … 5`: **0 violations**, attained (ratio 1.000); controls: `M_m` halved — 8 540 to 15 082 violations;
> the derivative of order `m − 1` instead — 7 647 to 12 301; the derivative at the anchor's value only — 24 501 to
> 34 217.  AA.1′ with one host, 200 instances: 0 violations in 26 855, 26 855, 24 635 states, attained; control, one
> host state forgotten: 1 485, 2 651, 2 345 violations.

*What this changes in the reading of our results.*  (a) "Few side chains off the anchor" is not the condition of
the envelope; **a small total displacement of the additive statistics, `Σ_{i∈S(x)} δ_i(x_i)`, measured against the
curvature scale `M_m^{−1/m}`,** is.  Many sites may be off the anchor if each moves its statistic little.
(b) The mean of such an envelope under any band model is exactly computable although the envelope is not
band-limited (a transfer matrix with polynomial entries truncated at degree `m` extracts `⟨e_m(δ)⟩`) [P, standard;
implemented and checked by R19: 923 means against enumeration, `7·10⁻¹⁵`].  **[R19 m13]** *What that mean yields is a
first-order number or a Jensen lower end; a floor needs `Z(m − env)`, which no band model holds — without an
allocation of the envelope to tables (A4) it is not a certificate.*  (c) For few statistics the many-body term needs no expansion at all: see level H2′ of §3.

### A4. Allocation of a state-dependent bound to tables (workstream P9, Proposition P)

| assumption as used | class | evidence |
|---|---|---|
| chain, band, geometry | — (not used) | the statement is about weights and domination on finite index sets; machine-checked by the theory division since `3cf14b9` (`ResolvedPenalties.lean`: `resolved_allocation`, `resolved_allocation_max`, `reduction_step`, `resolved_remainder_bound`; alphabets arbitrary types; docstring and theorem list read by us) [V, theirs] |
| tables `c_{T,U} ≥ 0` | **F** without | two binary sites, `Φ_T = −1`, `c = max Φ = −1`: the allocation inequality reads `0 ≤ −1` [X, R19 S9]; it is the hypothesis `hc0` of the machine-checked statement [V, theirs: `resolved_allocation`] |
| non-negative bounds `Φ_T` | **T** — sufficient for `c ≥ 0`, not needed | the machine-checked statement assumes nothing about the signs of `Φ` and `γ` [V, theirs; docstring read by R19].  **[R19 m3]** *This row read "**E** for the enlargement steps of the proof … no counterexample constructed"* |

### A5. Tractable models: a band on a chain, exact by transfer matrix; reductions by maxima and minima

*Statement.*  Models whose terms all lie within `w + 1` consecutive sites have `ln Z` and window marginals exact
at cost `O(n·k^{w+1})`; a term that fits no window is replaced by its maximum (ceiling) or minimum (floor) over
the sites given up; a pair beyond the band is split around the anchor.

| assumption as used | class | evidence |
|---|---|---|
| the interaction graph is a chain with a band | **C** for validity (every step is a pointwise inequality); **X** for cost | exact partition functions of general pairwise models are hard, and bounded treewidth is the known tractable class with cost exponential in the width [K, **from memory — sources not examined in this session**; to be cited after examination].  The held-site passes of A7 are conditional marginals and exist on any tree decomposition [?: not written, not built — `G-3`] |
| the band is wide enough to hold what matters | **Q** | not needed since part (19): the slack of everything the band gives up is a known table and is taken back (A6); a band of 4 with the recovery is tighter than a band of 7 without [M, Lys₁₂: `6.9·10⁻⁴` against `7.3·10⁻³` nats; part (19), item 74] |
| finite alphabets (rotamers) | **[?]** (**[R19 m4]**: the row read "**X** / **[?]**"; class X needs the two complexities with their sources, and the row gives neither) | with a continuous site variable the transfer matrix becomes an integral operator; a certificate then needs a bound of the variation of every table over a cell and carries a quadrature allowance — not formulated here: `G-5` |

### A6. Recovery of the known slack (Proposition A17.19)

*Statement.*  For non-negative `S⁺_g`, `S⁻_g` with `Σ_g S⁺_g ≤ m₊ − E`, `Σ_g S⁻_g ≤ E − m₋`, and means `⟨·⟩` under the
ceiling: (LJ) `ln Z(E) ≥ ln Z(m₊) + βΣ⟨S⁺_g⟩`; (LP) `≥ ln Z(m₊) + ln(1 + Σ⟨e^{βS⁺_g} − 1⟩)`; (UE), (UP) upper ends by
a monotone iteration with `C = Σ⟨S⁻_g e^{βS⁺_g}⟩`, `C′ = Σ⟨(e^{βS⁻_g} − 1)e^{βS⁺_g}⟩`.

| assumption as used | class | evidence |
|---|---|---|
| the space is finite | **T** | **the proof uses nothing but Jensen's inequality, `Π(1 + y_g) ≥ 1 + Σy_g` for `y_g ≥ 0`, and a change of measure; it is written below for any σ-finite measure space** [P].  The finite form is machine-checked by the theory division since `3cf14b9` (`GibbsRecovery.lean`: `lower_jensen`, `lower_product`, `upper_jensen`, `upper_product`, the two iterations; statements read by us, hypotheses as ours — (LJ) without sign conditions) [V, theirs; their audit at that head is being repeated here] |
| every group slack is non-negative | **F** for (LP), (UE), (UP); **T** for (LJ) | `aa01_essential.py` (2): two groups whose slacks cancel pointwise satisfy the hypothesis on the sum, and (LP) as a formula exceeds the exact `ln Z` by `ln 1.25`; (LJ), which is Jensen, holds for any real `s₊ ≤ m₊ − E`; control: the same slack as one non-negative group, where (LP) is attained [X].  **[R19 m5]** the runs for (UP) and (UE), which were missing: (UP) with the same two groups as minus-slacks: limit `0.4055 < ln Z = 0.6931`; (UE) with a negative minus-group paired with a positive plus-group: first iterate `−0.804`; with a negative plus-group: `−0.421`; controls hold.  Signed minus-groups alone do not break (UE) when every `S⁺_g` is zero: the failure needs the pairing |
| the laws of the group slacks under the ceiling are known exactly | **Q** | any lower bounds of `⟨S⁺_g⟩`, `⟨e^{βS⁺_g} − 1⟩`, `C`, `C′` keep all four inequalities; estimates from samples turn them into statements with a confidence level, a different kind of certificate |
| which items form a group | **C** for validity, **Q** for tightness | any partition is valid; items whose slack occurs at the same states must share a group or their cross terms are lost [M: 0.0083 against 0.0029 nats on Lys₅ at band 2, part (19) item 70] |
| nothing is assumed about the joint law of different groups | the price is a loss of order `D²` (`D` the width of the sandwich) between groups | **[R19 M1]** *This row read "a loss of about `D²/4` … [M]".  That was a formula, not a measurement, and it is not a bound.*  Measured (loss := corrected width − width with the same routed items put back exactly): 2.24, 0.16, 0.06, 0.07 times `D²/4` on the four enumerated instances (our own logs, by enumeration); **2.09 and 1.54 times at Lys₁₂, order 4, bands 4 and 7 — two thirds and a quarter of those brackets** (R19 §3.4, exact first order and `10⁶` samples; the band-4 number re-run by the coordinator with another seed: 2.084 ± 0.003); up to 13 times on random sandwiches.  Not measured for Lys₁₂ at order 5 or for Lys₂₀.  Slacks of different groups that occur at the same states lose their cross terms entirely.  The theory division's THY-RES-0016 §4 answers A19-T2: from the group laws alone the product inequality cannot be improved when the events overlap |
| the ceiling is a band model | **C** | the proposition holds for any model; exact means need a model whose conditional marginals are computable |

> **Proposition A17.19, measure-space form [P; the proof of part (19), item 69, read without finiteness].**
> Let `(Ω, ν)` be σ-finite, `β > 0`, `m₋ ≤ E ≤ m₊` measurable with values in `(−∞, +∞]`, `0 < Z(m₊)` and
> `Z(m₋) < ∞`; `S^±_g ≥ 0` measurable, `g` in a countable set, `Σ_g S⁺_g ≤ m₊ − E` and `Σ_g S⁻_g ≤ E − m₋` where the
> right-hand sides are defined.  Then (LJ), (LP), (UE), (UP) hold, with `⟨X⟩ = ∫X e^{−βm₊}dν / Z(m₊)`.
> *Proof.*  `Z(E)/Z(m₊) ≥ ⟨e^{β(m₊−E)}⟩` (with equality iff `m₊ < ∞` almost everywhere on `{E < ∞}`) `≥ ⟨e^{βΣ_g S⁺_g}⟩`, which is at least `e^{βΣ_g⟨S⁺_g⟩}` (Jensen; monotone
> convergence for the sum) and at least `1 + Σ_g⟨e^{βS⁺_g} − 1⟩` (the product inequality, termwise non-negative).
> For the upper ends write `⟨·⟩_E` for the mean under `e^{−βE}dν/Z(E)`:
> `Z(m₋)/Z(E) ≥ ⟨e^{β(E−m₋)}⟩_E ≥ 1 + Σ_g⟨e^{βS⁻_g} − 1⟩_E` and `≥ e^{βΣ_g⟨S⁻_g⟩_E}`; and for measurable `X ≥ 0` and
> each `g`, since `E ≤ m₊ − S⁺_g`, `⟨X⟩_E ≥ (Z(m₊)/Z(E))·⟨X e^{βS⁺_g}⟩ ≥ e^{ln Z(m₊) − u}⟨X e^{βS⁺_g}⟩` whenever
> `ln Z(E) ≤ u`.  If `u_t ≥ ln Z(E)` then `u_{t+1} ≥ ln Z(E)` by the last display, so every iterate from
> `u₀ = ln Z(m₋)` is an upper bound; the right-hand sides are non-decreasing in `u`, so the iterates decrease.  ∎
> **[R19 m1]** *Two `=` were `≥` (the mean under the ceiling sees only `{m₊ < ∞}`), and the last sentence gave
> monotonicity as the reason for the bound; the result stands.  The referee checked the rest: integrability of
> `e^{βs₊}` under the ceiling, countable sums, `Z(E) < ∞`; σ-finiteness is not used.*

### A7. Exact means by held-site passes (part (19), item 70)

| assumption as used | class | evidence |
|---|---|---|
| chain with a band; an item has all its sites but one inside one window of `w` sites | **C** | the law of (held site, window) is `exp(forward message with the site held + backward message + terms inside)`; tested against enumeration to `10⁻¹²` [X, Lys₅ at band 2].  Items with two sites at each end need two held sites — cost `k²` passes — not built |
| the chain is at most `2w` long (so that the window can be the last or the first `w` sites) | **C** — removed | a window anywhere on the chain: addendum A17 (20), item 77; `pi_inference/held_site_laws.py`, in the tree since `0930440`.  Replicated by R19: 3 000 random band models, 65 670 group statistics against its own enumeration, largest relative deviation `6.4·10⁻¹³`; all 56 groups of Lys₁₂ at band 4 and five at band 7 by a variable elimination that knows nothing of windows, `5.8·10⁻¹²`; controls fail as they must.  **[R19 m6]** *the row was out of date* |

### A8. Conditions for a *narrow* bracket (not for a valid one)

Every bracket of this line is valid whether or not these hold; they decide whether it is worth having.

| condition as it is usually said | class | what it is, quantitatively |
|---|---|---|
| "the ensemble is concentrated near one reference configuration" | **Q** | what enters is `β⟨Σ_{T⊆S(x)}Θ_T(x_T)⟩` under floor and ceiling.  Ser₁₂ has 6.3 of 12 side chains off the anchor on average and is certified within `1.8·10⁻³` nats at order 5; Lys₁₂ has 1.2 off and needs order 4 for `8·10⁻⁵` [M].  By A3′ the intrinsic quantity is the displacement of the additive statistics, not the Hamming distance |
| "the floor stays at the anchor" | **Q**, **criterion open** | the floor is the model minus the penalty; if the penalty grows faster with the number of displaced sites than the cost of displacing them, the floor's own Gibbs measure leaves the anchor and there is no certificate ((LKSE)₃ at order 3: a bracket of 658.9 nats, workstream P9; "about whether a floor delocalises" P9's own predictions were wrong five times of nine — question P9-T2 to the theory division, in progress there).  For an envelope `M_m·e_m(δ)` with `M_m` and a positive fraction of the `δ_i` bounded below, the penalty of `s` displaced sites grows like `s^m`; everything else in the floor grows at most like `s^{max(2, m−1)}` when the tables are bounded (the pair part like `s²`, the evaluated terms of order `j < m` like `C(s, j)`).  So **for `m ≥ 3` such a floor leaves the anchor on a long enough chain** [H, a growth comparison; N: an exchangeable instance, R19 S6]; at `m = 2` it depends on the pair part (with a pair repulsion larger than the envelope constant the gap stays near one nat up to `n = 200`).  No rate function: `G-4`.  What saves the instances is that `Θ_T` is tiny for spread-out `T`.  **[R19 M4]** *This passage read "the cost [grows] at most linearly: such a floor delocalises on a long enough chain at any fixed order [P]".  The premise was false — the floor contains the interpolant `I_{m−1}g`, which grows like `s^{m−1}` (exponents 2.0 and 2.9–3.1 measured at `m = 3, 4`) — and the label [P] was not earned.  The same sentence went to the theory division in SCI-RES-0024 §3; corrected by SCI-MSG-0030.*  Measured since: the transition of four floors in the size of their tables (`OPEN_PROBLEMS.md` D12) |
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

**(b) The same rows against the sections of the theory report** [from its table of contents at `b2cf817` and from
our reviews of the sections named; **not a re-reading** — their audit decides what each theorem needs]:

| # | where their report already leaves the assumption | reviewed by us | what, to our knowledge, is still inside the assumption |
|---|---|---|---|
| 1 | §11.15 (chains as known parts), §11.20 (a field), §11.23 (a function of the type: mean-field models, one or two phases), §11.32 (a nearest-neighbour coupling along the chain); **§11.30 (remainders around a *sampleable* known part — the oracle form of row 1)** | §11.30 (SCI-REV-0013, -0015), §11.32 (SCI-REV-0010, -0014); §11.15, §11.20, §11.23 not reviewed by us | the adaptive theory (§§11.18–11.19, Theorem 11.58a): the cube with the uniform measure only ("elsewhere exponents only, by transfer", THY-MSG-0017 §2) |
| 2 | §11.12 (dense second-order classes), §11.13 (beyond first-order product classes), §11.17 (classes linear in features), **§11.30 (box classes: Theorem 11.110, Proposition 11.113 with its necessity part)** | §11.30 | envelopes of order `m ≥ 3` that vanish on a ball; boxes whose two ends are not tractable models (SCI-RES-0025 §1) |
| 3 | §11.26 (several site types, any alphabets) | §11.26 (SCI-REV-0005) | exponents only; a continuum of site parameters; alphabets that grow |
| 4 | §11.11 (the known part as the gradient part of an asymmetric envelope), §11.26, §11.28 | §11.28 (SCI-RES-0005) | — |
| 5 | Theorem 11.58a (an explicit error term), §11.30 (brackets at finite size), the certified tables of §11.19 | §11.19 (SCI-REV-0007, -0016, -0017), §11.30 | constants at `n ≤ 30`: our referee found the design of Theorem 11.58a above the non-adaptive cost up to `n = 2·10⁴` |
| 6 | Proposition 11.113, remark: an error of at most `e` in every evaluated energy moves `ln Z` by at most `e` | §11.30 | a query model with noisy evaluations elsewhere |
| 7 | §11.23 (two phases), §11.31 (barriers and traps: cut certificates) | — (not reviewed by us) | a floor that leaves its reference: THY-RES-0016 §5 (a mechanism, a one-sided test, no threshold) |
| 8 | §11.27, §11.29 (evaluations together with local ensemble-averaged data — our own earlier question) | answered there; reviewed in part | an oracle for certified mixed-difference bounds |

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
| H2′ | H2 plus `φ(u(x))`, `u` a vector of `r` site-additive statistics, `φ` Lipschitz, otherwise arbitrary | exact up to a binning allowance: a transfer matrix that also carries the binned partial sums; floor and ceiling from the extreme values of `φ` on a cell | `O(nk^{w+1}B^r)` for `B` grid values per statistic; width exactly `2β·Lip(φ)·ρ ≤ β·Lip(φ)·n·h` for grid step `h`, `ρ = Σ_i max_b abs(a_i(b) − ã_i(b))` the **accumulated** rounding (attained), and `B ≈ R/h + n` grows with `n` at fixed `h`: for a width `ε`, cost `O(nk^{w+1}(β·Lip·n·R/ε)^r)` | `r`: exponential in the number of statistics — a parameter, not the size of the system; **and necessarily so: the problem is W[1]-hard in `r`** (the Complexity division's COMPLEXITY-RES-0001: a reduction from unary bin packing with `r` bins, with `k = r` states per site and a threshold `φ` [P, theirs, re-derived by us; K for the hardness of unary bin packing, cited by them from memory]) [P, elementary; N: R19 S5, the exact `ln Z` inside in 480 of 480 for `r = 1`; with the allowance of one cell only, the truth is outside; `r ≥ 2` not tested] **[R19 m12]** |
| H3 | H2 plus a many-body part with a pointwise envelope of its order-`m` remainder (A3; class A3′ with any `r`) | sandwich from the ball of radius `m − 1` | `Σ_{s<m} C(n,s)(k−1)^s` evaluations, `C(n,m)` tables | the envelope: no certificate without it (A3, **F**); no width below the box limit `W* = 2β⟨envelope⟩ + O(β³)` with the same knowledge (A10, Proposition AA.3) |
| H4 | H3 with the slack of every reduction known as tables | sandwich + recovery (A6) | held-site passes: `k` transfer-matrix runs per held site | envelope; a loss of order `D²` between groups (measured between 0.06 and 2.2 times `D²/4`; no bound of that form: A6, **[R19 M1]**); items that need two held sites |
| H5 | H3, sampled | a sampler inside the sandwich (the theory division's Propositions 11.113, 11.113a) | evaluations growing with the width of the sandwich | a statistical statement, not a deterministic one |
| H6 | no tractable floor (several modes; a floor that delocalises) | lower ends only (restriction, A1); an upper end needs a cover of the space | — | first-order information alone costs exponentially many evaluations (the theory division's lower bounds for first-order classes; our reviews SCI-REV-0001…0016) |

## 4. Part D — gaps and proof obligations

| id | what is missing | whose | status |
|---|---|---|---|
| `G-1` | Proposition AA.1 / Corollary AA.2 tested where they are not GBn2: a synthetic many-body energy `Σ_p φ(c_p + Σ_i a_{p,i}(x_i))` at every state, with a control; the polynomial transfer matrix for `⟨e_m(δ)⟩` | science (workstream R19) | **done for the host-free class and for one host (AA.1′)** — 0 violations, attained, controls fail; the transfer matrix implemented (`7·10⁻¹⁵`).  Open: AA.1′ machine-checked, next to the theory division's `resolved_remainder_bound` |
| `G-2` | level H2′ stated with its allowance and implemented on a synthetic instance; comparison with H3 on the same instance (few statistics against many) | science (workstream R19) | **done for one statistic** (statement in §3, row H2′; on one nine-site instance with 6.1 of 9 sites off the anchor H2′ gives 0.74, 0.23, 0.046 nats with 65, 257, 1 025 grid values and no ball, against 7.6, 11.8, 7.2, 1.24, 0.21 nats for the H3 envelope at orders 2–6).  Open: `r ≥ 2` in an implementation.  Whether the exponent in `r` is necessary: **yes** (COMPLEXITY-RES-0001; `OPEN_PROBLEMS.md` D13) |
| `G-3` | held-site passes on a tree decomposition (a graph that is not a chain) | science; a request to engineering if it grows | open |
| `G-4` | a criterion for a floor to stay localised, from quantities cheaper than the floor itself; the growth comparison of A8 made into a statement with a rate function | theory (our question P9-T2; in progress there) and science | **partly answered** (2026-11-26): for band models the least ratio (cost)/(penalty) over states, by `(min,+)` passes, is within 1.1 – 3.3 % above the measured transition in four cases (addendum A17 (21), item 86; **[M]**, and **[P]** as a lower bound of the bracket lost beyond it); open: a bound on the entropy term (so that it becomes a criterion from below), models without band structure, a rate function |
| `G-5` | a continuous site variable: what the tables must satisfy, the quadrature allowance, where it fails (a table that is not Lipschitz on a cell) | science | open |
| `G-6` | the theory division's exchangeable results with unequal site weights: which exponents survive | to be put to theory after Part B | open |
| `G-7` | Part B (b): the list of SCI-RES-0023 §2 against the theory division's report — **done at the level of sections** (table (b) of Part B, from its table of contents and our reviews); theorem by theorem it is their audit's; (c): a review of their audit when it exists | science | (b) done in part; (c) open |
| `G-8` | sources for the two **[K, from memory]** entries (hardness of general partition functions; treewidth) examined and cited, or the entries removed.  **[R19 m4]** *the row counted three; the third topic it named occurs nowhere in this file* | science | open — the Complexity division answered with leads "all from memory (none opened in this session; please treat as leads, not as verified citations)" (COMPLEXITY-RES-0001: Jerrum–Sinclair 1993, Jaeger–Vertigan–Welsh 1990, Bulatov–Grohe 2005, Goldberg–Grohe–Jerrum–Thurley 2010, Barahona 1982; Lauritzen–Spiegelhalter 1988, Dechter 1999, Chandrasekaran–Srebro–Harsha 2008, Kwisthout–Bodlaender–van der Gaag 2010, Marx 2010): the two entries stay **[K, from memory]** until a source is opened |

## 5. Counterexamples run (index)

| script, log | what it shows | class supported |
|---|---|---|
| `experiments/science/assumption_audit/aa02_box_limit.py`, `aa02_box_limit_{K5_m4,K5_m5,LKSEc5_m4}.log` | the box limit `W*` by enumeration against the certificate's sandwich and corrected bracket; the envelope against the remainder at every state, with a control that fails (÷1000) and one that cannot (÷2) | A10 |
| `experiments/science/assumption_audit/aa01_essential.py`, `aa01_essential.log` | (1) no certificate from a ball alone; (2) (LP) fails with a negative group slack, (LJ) does not; (3) the floor must hold everywhere, the ceiling need not be finite everywhere | A3 **F**; A6 **F** / **T**; A1 **F** / **T** |
| `experiments/science/ws_R19/r19_audit_tests.py`, `r19_audit_tests_v3.log` (the referee's; no code of ours) | S1–S4: AA.1, AA.2 on synthetic energies with three controls, the norm, the identity, the polynomial transfer matrix; S5: H2′; S6: the growth comparison of A8; S7, S9: a finite ceiling valid on one mode only; `h = m`; signed tables; (UE), (UP) with negative slacks; S8: one host | A1 **F** (new row); A3 **Q**; A3′, AA.1′; A4 **F**; A6 **F**; A8; H2′ |

## 6. Changes made on the review of workstream R19 (2026-11-26; announced in SCI-MSG-0030)

| where | before | now | finding |
|---|---|---|---|
| A1, third row | "the ceiling holds on all of the space: **T**" | finiteness is **T**; `E ≤ m₊` where `m₊` is finite is **F** (new row, with a run) | M2 |
| A3′, AA.1, AA.2 | the class described with hosts, the proposition stated without, called "the general statement" | AA.1 is the host-free case; AA.1′ (with hosts) added; AA.2 fails if a host is treated as an additive site | M3 |
| A6, joint law | "a loss of about `D²/4` … [M]" | a loss of order `D²`; measured 0.06 to 2.2 times `D²/4`, 2.09 and 1.54 times at Lys₁₂; no bound of that form | M1 |
| A8, the floor | "cost at most linearly … at any fixed order [P]" | everything else grows like `s^{max(2, m−1)}`; true for `m ≥ 3`; [H] | M4 |
| A6, proof | two `=`; a wrong reason for the iterates | `≥`; induction | m1 |
| A3, `m ≥ 3` | **T** / **Q**, "used once" | **Q**: `m > h`, used twice; `h = m` fails for derivative bounds | m2 |
| A4, signs | `Φ_T ≥ 0`: **E** | `c_{T,U} ≥ 0`: **F** without; `Φ_T ≥ 0`: **T** | m3 |
| A5, alphabets; `G-8` | **X** / **[?]**; three entries from memory | **[?]**; two | m4 |
| A6, signs of the group slacks | a run for (LP) only | runs for (UE), (UP) supplied | m5 |
| A7, second row | "being removed" | removed; replicated | m6 |
| H2′ | "width `≲ β·Lip·n·`(cell size)" | the allowance is the accumulated rounding; `B` grows with `n` | m12 |
| A3′ (b) | "exactly computable" | …and not a floor | m13 |
| AA.1 | "the norm of `D^mφ`" | the operator norm induced by the norm of the increments | m14 |

Confirmed without change (19 rows): §5.2 of the referee's report.  Findings m7–m11 and m15 concern the addenda, a
message and the code, not this file: `INFERENCE_LIMITS_ADDENDA.md`, part (21), and SCI-MSG-0030.
