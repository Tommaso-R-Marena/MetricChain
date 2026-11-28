# Division 9 — cross-divisional mathematical synthesis

*Written by the coordinating AI session of Division 9; revised after the internal review
(`REVIEW_A.md`: S2's proof completed for two states, S4(ii) withdrawn and replaced, three wordings
weakened, two numbers corrected).  Statements of other divisions are imported with
their branch, commit and status and are **not re-verified here** unless said; a statement of this note
that depends on one of them is conditional on it.  Labels as in `MATHEMATICS.md`.  Numerical checks:
`experiments/mbar/bench/check_synthesis.py` → `results/synthesis_checks.json`.*

Branches read (heads on 2026-11-28 05:23 UTC): `research/phase2-foundations` `d3b13a2`,
`research/phase2-adaptive-hierarchy` `c66a401`, `research/phase2-certified-inference` `1bb0dcc`;
archive `fe9f58c`.  Only the documents named below were read, and of those only the cited sections.
Second read (08:53 UTC, heads `3daa07d`, `3e3e7d9`, `2d0255f`): the messages addressed to this division
— THY-MSG-0024, THY-MSG-0025, HIE-MSG-0003, ENG-MSG-0011, ENG-RES-0021 — in full, and nothing else of
those branches (not the bridge note, not `MBAR_INTEGRATION.md`); what they change is in §S8.

## S0. The two experiments

| | MetricChain (theory, foundations, hierarchy) | this division |
|---|---|---|
| unknown | a `u`-Lipschitz energy `ψ` on the cube `{0,1}ⁿ` (a class of energies) | the base measure seen through the energies (energies known) |
| access | evaluations of `ψ` at chosen points (+ observables, + samples of the target ensemble in Theorem E) | independent equilibrium samples of `K` chosen states, energies of all states at the sampled points |
| cost | number of evaluations; exponents `a` (fixed sample), `h` (adaptive) | number of samples; the constant `V_c(s)` |
| guarantee | deterministic class, probability over the algorithm | probability over the samples, given equilibrium |

The two models do **not** coincide, and no statement below identifies them.  What connects them is one
question: *what does a sampler buy?*

## S1. Overlap geometry and information complexity: a thermodynamic-length bound, and "sampling is the bottleneck"

**Proposition S1 (path bound)** [P; N].  Let `k_0, k_1, …, k_L` be distinct states with
`P_{k_{j+1}} ≪ P_{k_j}`, and `c = e_{k_0} − e_{k_L}`.  (A sequence with repetitions contains such a path
made of some of its own steps, so the bounds hold for it too.)  Then for every allocation `s`

    V_c(s) ≤ Σ_{j<L} χ²(P_{k_{j+1}} ‖ P_{k_j}) / s_{k_j} ,     and
    V*_c(B) ≤ (1/B) ( Σ_{j<L} √(a_{k_j} χ²(P_{k_{j+1}} ‖ P_{k_j})) )² .

*Proof.*  The tuple `r_{k_j} = p_{k_{j+1}}/p_{k_j} − 1` (`j < L`), `r_k = 0` otherwise, lies in the affine set
`F_c` of Theorem A1: `E_{k_j} r_{k_j} = 0`, and `Σ_k p_k r_k = Σ_j (p_{k_{j+1}} − p_{k_j}) = p_{k_L} − p_{k_0} = −Σ_k c_k p_k` — the
telescoping sum *is* the feasibility condition.  Its objective is the right-hand side; A1 and A5.  ∎

The tuple is the influence function of stepwise exponential averaging (free-energy perturbation along
the path).  The second bound is a non-asymptotic form of the "thermodynamic length" rule [K: Crooks
2007; Shenfeld et al. 2009]: the optimally allocated multistate estimator is never worse than the
squared sum of the χ-distances of the steps.  Checked on 300 random models (`V/bound ≤ 0.94`,
`V*/length² ≤ 1.00`).

**Corollary S1′ (tempering ladder on the cube class)** [P; N].  Let `ψ` have oscillation at most `Ω`
(for a `u`-Lipschitz `ψ` on `{0,1}ⁿ`: `Ω ≤ un`), `K′ = ⌈Ω⌉`, and states `q_j = e^{−(j/K′)ψ}`, `j = 0, …, K′`,
over any reference.  For each step the density ratio `p_{j+1}/p_j` has `sup/inf ≤ e` (the oscillation
of `ψ/K′` is at most 1), hence `χ² ≤ (e−1)²/(4e) < 0.272` (Bhatia–Davis), and for the free energy
`ln E_π e^{−ψ}`

    V*_c ≤ V_c(uniform on the K′ sampled states j < K′) ≤ 0.272 · K′² .

So with exact samplers of the tempered ensembles, `0.272⌈un⌉²(1.96/ε)²` samples give accuracy `ε`
asymptotically; on 27 random Lipschitz energies on cubes of 8–12 sites the exact `V_c` is 5–14 % of
the bound.  *Certification.*  In this design the target state `K′` is not sampled, and the region of
Theorem B2 constrains only states that occur as labels: to certify the free energy with B2 the target
must be sampled as well (uniform allocation on all `K′ + 1` states: the same argument gives
`V_c ≤ 0.272·K′(K′+1)`), and the width of the region is then 2–3 times the asymptotic one in our
benchmarks, with no proved bound (`MATHEMATICS.md` §B2).  The fully proved finite-sample statement
on this class is the elementary one used in S1″.

**Corollary S1″ (a query lower bound for sampling)** [P, conditional on the theory division's Theorem
11.25, lower bound [V] in its tree, not re-verified here].  Theorem 11.25 states that every randomised
algorithm returning a bracket of ratio `e^ε` with probability `1 − δ` for `A(ψ) = 2^{−n}Σ_x e^{−ψ(x)}` on the
class of `u`-Lipschitz `ψ` makes at least `exp(n·h(u) − o(n))` evaluations.  Consequently: **any
algorithm that, from evaluations of `ψ`, outputs `n₁ = ⌈8(e−1)²K′² ln(4K′/δ)/ε²⌉` points for each tempered
ensemble `μ_{jψ/K′}`, `j < K′ = ⌈un⌉`, whose joint law is within total variation `δ/2` of independent exact
draws, makes at least `exp(n·h(u) − o(n))` evaluations on some instance.**

*Proof.*  From such a sample, `ln A = Σ_j ln E_j e^{−ψ/K′}`, and each factor is the mean of a positive
variable whose values lie in an interval `[a, ea]` with mean `≥ a`: by Hoeffding the relative error of
the sample mean exceeds `η` with probability at most `2exp(−2n₁η²/(e−1)²)`; with `η = ε/(4K′)` all `K′`
factors are within `η` except with probability `δ/2`, and the logarithm of the product is within
`2K′η = ε/2`.  This uses `K′n₁` further evaluations (polynomial).  The result is a bracket of ratio `e^ε`
with probability `1 − δ`; apply Theorem 11.25.  ∎

*What this says.*  On the programme's own class the exponent `h` is not a cost of *estimation*: given
equilibrium samples of a tempering ladder, a certified free energy costs polynomially many samples.
The exponential cost of the query model is the cost of *producing* those samples from evaluations.
This is the classical reduction of counting to sampling (Jerrum–Valiant–Vazirani; Štefankovič–
Vempala–Vigoda) placed on the cube class; it complements two statements already in the programme:
the science division's remark that "with samples of pinned ensembles the problem is polynomial"
(addendum A7, quoted in the foundations report §6), and the foundations division's Theorem E, where
samples of the *target ensemble alone* still leave an exponent `ν* ≈ 0.40·h` (`PHASE2_REPORT.md` §6;
[P], refereed internally).  Read together: **samples of the target alone do not remove the exponent;
samples along a path of ensembles do.**  The quantity that measures "along a path" is the
thermodynamic length `Σ_j √χ²_j` of S1 — in MBAR terms the effective resistance of the overlap graph.

*For the foundations division (question).*  Theorem E's remark (3) asks whether samples can beat
`e^{nh}` on the whole class.  S1′ answers it for samples of a tempering ladder (polynomial); is there
an intermediate statement — an exponent `ν(L)` for samples of `L` tempered ensembles, decreasing from
`ν*`-type behaviour at `L = 1` to 0 at `L = ⌈un⌉`?  The path bound gives the upper side for free:
`χ²` of a step of the ladder with `L` rungs is at most `(e^{un/L} − 1)²/(4e^{un/L})`, i.e. a cost
`≈ L·e^{un/L}/4` — exponential in `n/L`.

## S2. Effective resistance and adaptive computation: where adaptivity matters

**Imported** (theory division, consolidated archive `01_theory`, Theorems 11.52–11.54; status there:
lower bounds [V], algorithms [P]): on the cube class the adaptive exponent equals the hinted exponent
`h`, strictly below the non-adaptive exponent `a`; with two rounds the exponent is strictly between
(Theorem 11.86); the hierarchy division conjectures that three rounds reach `h` (Conjecture H5; proved
on block-radial classes, Theorem H1).

**This division** (Theorems A5, A6, C2; Proposition S2 below).  In the multistate sampling experiment:

1. the best fixed allocation has variance `V*_c(B)`, the squared Elfving gauge of the contrast (A5);
2. no adaptive strategy, with any number of rounds, beats `V*_c(B)` by more than a universal constant
   factor, locally at every instance and for budgets above a threshold (C2);
3. **Proposition S2 (one round)** [P; N].  Over all `K`-state instances, an allocation fixed in advance
   has worst-case efficiency `min_k s_k`; uniform allocation attains the optimum `1/K`.
   *Proof.*  Upper bound: `V(u) ≤ max_k(s*_k/u_k)V(s*) ≤ K·V(s*)` by monotonicity and homogeneity.  Lower
   bound, `K ≥ 3`: the *bridge instance* — `P_a` uniform on a block `A`, `P_b` uniform on `B`, `P_m` uniform
   on `A ∪ B`, the other states copies of `P_a`: samples of every state except `m` are constant in the
   energies and carry no information about `f_b − f_a`, so `V(s) = 4/s_m` and the efficiency of `s` is
   exactly `s_m`; the adversary chooses which state is the bridge.  `K = 2` (the bridge instance needs
   three states; pointed out by the referee): `P_1` uniform on `A`, `P_2` uniform on `A ∪ B`, contrast
   `f_2 − f_1`; samples of state 1 are constant in the energies, the efficiency of `s` is exactly `s_2`,
   and the adversary chooses which of the two states is the larger one.  ∎  (Checked: `K = 3, 4, 6`
   and the two-state instance, efficiency equal to the stated value to `10⁻⁹` or better.)
4. two rounds (a pilot and one adapted round) reach `V*_c(B)(1 + o(1))` on every fixed instance
   [C: standard for sequential designs, not proved here; consistent with the benchmark, where the
   two-stage rule matches the oracle allocation within noise in 6 of 8 systems].

So the round hierarchy of the sampling experiment is: **one round loses a factor up to `K` (proved);
no number of rounds gains more than a universal constant factor over the best fixed allocation
(proved: C2, two-point, local); that a single adaptive round already recovers the optimum at leading
order is a conjecture supported by the benchmark** — a multiplicative gap, against an exponential gap
in the query model whose closure after three rounds is the hierarchy division's open conjecture.  The structural parallel is exact in one respect: in both models
the value of adaptivity is the value of a *hint about the design* (theory: "adaptive = hinted";
here: "adaptive ≈ oracle allocation", up to a constant), and in both the lower bound is proved by exhibiting one
perturbation that is hard for every design simultaneously (here: the Elfving dual direction `h°` of
C2, whose variance per unit cost is small in *every* state).

*For the hierarchy division (question).*  Is there a class of instances on which the relaxation lemma
(your Lemma B) is the query-model counterpart of the equivalence theorem A6 — i.e. a statement that
the invisible mass after round two is controlled *in every direction at once*?  If so, a three-round
upper bound on general `L_u` might be approached through a minimax (Sion) argument of the kind used in
A5 rather than through families.

## S3. Certified energy envelopes and finite-sample statistical uncertainty

**Imported** (certified-inference division, `CERTIFIED_INFERENCE.md`, second version; [P], first
version refereed internally): Theorem 6.1(a) — with draws from the reference only, certifying an
ensemble average over the class of energies within an envelope of ratio `Γ` needs
`n ≥ Γ·ln(1/(4δ))/(72α²)` draws; Theorem 5.4 — draws from the extremal ensemble of the class make the
certificate independent of `Γ`.

**In the terms of this division** [P; N].  Reference-only sampling of a target ensemble is the
boundary point `s = e_ref` of Theorem A3: the variance is `∫ρ² dm`, a χ²-type divergence between the
target and the reference, and on the two-point instance of Theorem 6.1(a) (`π(1) = 1/Γ`, weights
`1, Γ`) it is asymptotic to `Γ/16` (computed: `V/Γ = 0.0635, 0.0627, 0.0626` at `Γ = 64, 256, 1024`).  Sampling the
target itself gives `Var_p(f) ≤ ¼`; and for the *free energy* of the target relative to the
reference, reference-only sampling costs `≈ Γ/4` while a ladder of `⌈ln Γ⌉` intermediate ensembles
costs at most `0.272⌈ln Γ⌉²` (S1′; on this instance the optimal ladder has `V ≤ 1.0` for all `Γ` up to
1024).  So **the cost `Γ` of the envelope ratio is the χ²-divergence between the sampled law and the
law the statement is about; a path of sampled ensembles replaces `Γ` by `(ln Γ)²`** — the same
phenomenon as Theorem 5.4, with a quantitative rate for paths, and with the caveat the certified-
inference division already records: the samplers of the intermediate ensembles must exist and be
exact (obstacle 3 of its final report).

**Composition** [V].  If the energies are known only within `|ũ_k − u_k| ≤ ε_k` uniformly on the support,
and the samples are equilibrium samples of the approximate system, then a statistical radius `r` for a
contrast of the approximate free energies gives the radius `r + Σ_k|c_k|ε_k` for the true ones
(`free_energy_envelope`, `contrast_composition`).  The same holds for consistent trapping
(`MATHEMATICS.md` B7): the missing mass `−log P_k(B)` plays the role of `ε_k`.  This is the only way a
sample-based certificate can speak about the true system, and it requires the envelope from outside
the samples.

## S4. Confidence regions as data regions for partial identification

**Imported**: certified-inference Theorem 4.1 — for ensembles `p` with weights within an envelope and
measured averages `E_p φ ∈ R`, the identified interval of `E_p f` is `inf_η T(η)` with
`T(η) = h_R(η) + max_p E_p[f − η·φ]`, `h_R` the support function of the data region `R`; soundness (a)
holds "with no assumption" for any `R` containing the true averages.  (The ensemble division's E17.2
gives the same interface through support functions; archive `04_ensemble_identifiability`.)

**Proposition S4** [P].  Let `R̂` be a random convex region *in the space of the averages* with
`P(E_p φ ∈ R̂) ≥ 1 − α`.  Then the interval of Theorem 4.1 computed with `R̂` contains `E_p f` with
probability at least `1 − α`.  What this division can supply:
(i) for `φ` bounded observables of a sampled state, the box of the intervals of `MATHEMATICS.md` B6
(levels added up);
(ii) for populations of macrostates or ratios of partition functions, a **box obtained from the region
`C` of B2 without any union bound**: `C` is simultaneous for all contrasts, so the intervals
`[inf_C cᵀf, sup_C cᵀf]` for any finite list of contrasts hold jointly at level `α`; exponentiating
gives a box for the corresponding ratios.

*Proof.*  Soundness of Theorem 4.1(a) on the event `{E_p φ ∈ R̂}`.  ∎

*Correction (found by the referee).*  The first version claimed that `C` itself can be passed as the
data region through its support function `sup_{f∈C} η·f`.  That is wrong as stated: `C` is convex in the
free energies, i.e. in *minus the logarithms* of ratios of populations; its image in the space of
averages is not convex in general, and its support function is a support function in the wrong
coordinates for the dual `T(η) = h_R(η) + max_p E_p[f − η·φ]`.  The box of (ii) is the valid form.  It
was sent in the wrong form in MBAR-MSG-0001 §4(b) and is corrected in MBAR-MSG-0002.  Not done:
running the certified-inference library on such a box.

## S5. Geometric stress certificates and thermodynamic population estimates

The geometry division's criteria (archive `05_geometric_inference`, `ENSEMBLE_RIGIDITY.md`, Theorems
A–C; robust versions N0–N6, unreviewed) take as input ensemble *second moments* of inter-site
distances, exactly or within a tolerance.  For a molecular ensemble at a thermodynamic state `k` these
are expectations `E_k[d_ij²]` of bounded observables on a compact configuration space, and for an
ensemble of `M` metastable conformers the weights are populations `E_k[1_{A_m}]`.  This division
supplies, from multistate samples, simultaneous finite-sample intervals for finitely many such
expectations (B6) — the tolerance the robust criteria need — and the design theory says how to
allocate samples for them: the target measure of A3 is `ν = (d_ij² − E_k d_ij²)P_k`, and
`optimal_allocation(…, objective="max")` minimises the worst variance over the edges.  Nothing
specific to stress was proved here, and the geometry division's own verdict stands that its
quantitative guarantees are empty at realistic accuracy; the composition is recorded as an interface,
not as a result.

## S6. Sample allocation and experimentally relevant observables

The allocation theory is not tied to free-energy differences between sampled states: any smooth
functional of the base measure has a target measure `ν`, and Theorems A3–A8 apply — expectations at
sampled or unsampled states, populations, potentials of mean force between bins, sums and maxima of
several targets (A10).  On the public umbrella-sampling data (`VALIDATION.md` §6) the plug-in optimal
design for the free-energy difference between two rotamer wells *in the unbiased ensemble* puts 84 %
of the samples on the six umbrellas across the barrier and predicts the same precision from 37 % of
the samples; this is a plug-in estimate on one data set, not a demonstrated saving.

## S7. Summary of what is substantive and what is only an interface

| link | content | status |
|---|---|---|
| S1, S1′ | path/thermodynamic-length bound for MBAR; polynomial certified free energies on the cube class given ladder samplers | [P], [N] |
| S1″ | sampling the tempering ladder needs `e^{nh}` evaluations | [P], conditional on Theorem 11.25 |
| S2 | round hierarchy of allocation: `1/K` for one round; at most a constant factor for any number of rounds; contrast with the query model | (1)–(3) [P]; (4) [C] |
| S3 | the envelope-ratio cost is a χ²; paths give `(ln Γ)²` | [P], [N]; composition [V] |
| S4 | simultaneous boxes from the region of B2 as data regions (first form withdrawn) | [P], elementary; not run |
| S5 | intervals for second moments and populations | interface only |
| S6 | allocation for observables | theory [P]; one plug-in example |
| S8 | the exchange after our first message: independent replications of A1/A2 and B1 by two divisions; imported sharpenings (not quasi-convex; Bhattacharyya bounds; ladder exponent `Θ(1/L)`; shared errors; caps on unvisited regions; regime caveats); our answers on the shape of the region, joint levels, correlated draws, allocation for certificates | imported statements quoted with their status; inequalities checked numerically (T11); our answers [P] |

## S8. The exchange after our first message: what the other divisions sent, what we checked, what it changes

All three divisions wrote to this division while it worked (messages named in the header).  Their
statements are quoted with the status they give them; "checked" means the stated inequality or number
was recomputed by `experiments/mbar/bench/check_inbound.py` (`VALIDATION_TABLES.md` T11), not that a
proof of theirs was read.  Nobody refereed anybody's proofs in this exchange.

### S8.1 Independent replications of statements of this division

* **A1, A2, the dual form** — foundations (THY-MSG-0024 §2.3), own code, 300 random finite instances:
  `Σ_k s_k Var_k(z) = cᵀL^+c − Σc_k²/s_k` to `10⁻¹²`, the gradient to `10⁻⁷`, midpoint convexity without
  exception; the dual form derived by their own route before they saw ours, and credited to us.
* **B1 and the region of B2** — engineering (ENG-MSG-0011 §4): re-derived in three lines, implemented
  and tested with their own code (coverage at the stated rate; every interval contains the truth whenever
  the region does; an independent optimiser reaches each bound to 0.2 %).  They hit, in their own
  implementation, the same kind of defect our referee found in ours (a Newton iteration running to a
  saturated point and passing a convergence test), caught by a guard of their certificate.
* **Failure of convexity for MBAR on correlated raw samples** (our A11) — foundations (§2.4), found
  independently, with a simulation (lazy chains, `N = 6·10⁵`, 1000 replicates: `68.4 ± 3.1`,
  `170.8 ± 7.6`, `153.3 ± 6.9` against the predicted 69.00, 183.78, 163.95), and the same repair as our
  A12(b)–(c) (`V_c(s/C)`; simulated `6.50 ± 0.29`, `7.61 ± 0.34`, `13.55 ± 0.61` against 6.15, 7.90, 13.04).
  **Their instance is stronger than ours: the value at the midpoint exceeds both end points, so the
  variance is not even quasi-convex.**  Reproduced with our code (T11).  It is the only simulation of
  MBAR under correlated sampling in this exchange, and it is theirs.

### S8.2 Imported statements that sharpen or bound ours

(a) *Bhattacharyya bounds* (THY-MSG-0024 §2.5; machine-checked in their tree; checked here):
`s_is_j·BC_{ij}²/Σ_k s_k ≤ −L_{ij}(s) ≤ ∫min(s_ip_i, s_jp_j)`.  By Rayleigh monotonicity every effective
resistance of `L(s)` is at most that of the network with conductances `s_is_jBC_{ij}²/Σs`, so
`V_c ≤ R_c ≤ R_c^{BC}`: a second explicit upper bound next to the path bound S1, finite whenever
consecutive states overlap at all (S1 needs absolute continuity and a finite `χ²`).

(b) *The exponent of a ladder with `L` rungs* (THY-MSG-0025 §2; the answer to question 5(a) of
MBAR-MSG-0001).  With an indicator `1_D` in our dual formula A2, for every allocation on the simplex,
`V_c(s) ≥ (f_L − f_0)²/max_k f_k(1 − f_k)`, `f_k = P_k(D)` (checked).  For a "dip" `D` of the cube class
they compute the exponent of the right-hand side: times `L` it is 0.038–0.048 for `L = 2, …, 16` at
`u = 1` (their exact binomial sums; not recomputed here).  With S1 (exponent at most `u/L`): **the
exponent of the end-to-end variance on an `L`-rung ladder is of order `1/L` from both sides; a bounded
number of rungs leaves an exponentially large variance on some member of the class whatever the
allocation, and the polynomial regime of S1′ needs of the order of `n` rungs.**  The constant is open
between about 0.045 and `u` (at `u = 1`).  For `L = 1` their Theorem F (Harper's theorem; not checked
here) gives the exact exponent `h` of the two-state resistance of the class — the exponent of adaptive
queries.  So in our experiment, with the reference and the target both sampled: *without intermediate
states the cost is `e^{nh}` samples on the worst member of the class; with a ladder of the order of `n`
states it is `O(n²)`.*

(c) *Shared errors* (ENG-MSG-0011, Proposition M2; checked).  When two states carry the *same* error
function `|d| ≤ ε` (windows of one potential), the free-energy difference moves by at most
`ln(1 + (e^{2ε} − 1)·TV(p_i, p_j))`, not `2ε`; the composition of S3 (`r + Σ_k|c_k|ε_k`, [V]) is sharp only
for unrelated errors or non-overlapping states.  From the foundations (§2.6; their archive, not
checked): if the mean of the remainder under the sampled ensemble is measured, the bracket has length
`ε²/2` instead of `2ε`.

(d) *Unvisited regions* (HIE-MSG-0003 §2.2–2.3; the half-space identity checked).  If the energy
difference is `L`-Lipschitz and at least `b` outside a region `S` of reference probability `Φ̄(t)`
(Gauss space, any dimension), then `∫_S e^{−ΔU}dγ ≤ e^{−b}·e^{L²/2 − Lt}·Φ̄(t − L)`, attained by a half-space;
the cube version has the threshold `e^{−nh}`.  This is an envelope *from outside the samples* of
exactly the kind our Proposition B7(b) says a certificate for the true system needs.  As they say, it
does not make the hypothesis observable.

(e) *Regimes* (HIE-MSG-0003 §§1, 2.1, 2.4, 2.5).  Their model is ours with one **unsampled** target,
references that the experimenter designs and whose free energies are known, and one evaluation per
draw.  For such a target, in the exponential regime, the number of draws for a bounded accuracy at
fixed confidence has the exponent of the largest *relative entropy* `max KL(target ‖ reference)`
(`n·a(u)` on the cube; [K] in their archive), which is exponentially smaller than the second-moment
threshold `χ²`; a two-point argument in our oracle model gives the lower side in Gauss space (fewer
than about `L·e^{L²/2}` reference draws: no estimator is accurate to 0.23; the constants 0.473–0.599
recomputed).  **Consequence for how our statements must be read:** the variance of A3(c) for an
unsampled state, the sentence of S3 "the cost `Γ` of the envelope ratio is a `χ²`", and the bound C1
(which needs `N ≥ N₀`, of the order of the variance) are statements at the scale of the central limit
theorem.  They are not sample-complexity exponents for fixed-confidence guarantees at low overlap, and
there the answer is smaller than the variance suggests.  Likewise C2 (allocation among *given* states,
local, budget above a threshold) does not see what they prove when references may be redesigned
between stages: the number of stages changes the exponent (`a` to `h`).
*Effective resistance at low overlap* (their §2.6, elementary): with conductances `e^{−nc_e}`,
`(1/n)·ln R_{ab}` tends to the bottleneck cost of the best path; with (a) this is the overlap geometry of
our Laplacian in that regime.

(f) *A connection examined by them and rejected* (HIE-MSG-0003 §3.3): whether the `1/k²` law of their
nested levels is the thermodynamic-length law of a chain of bridging states (our S1).  Computed by
them: no (`c_*² = 0.0712` against 0.0294, 0.115, 0.0283 for the natural paths at `u = 1`).  The two laws
should not be identified; recorded here as their negative result about our S1.

### S8.3 Our region inside the certified-inference certificate (their Theorem M1, their measurements)

The box of our region bounds the density ratio of the target state against the sampling mixture
pointwise, which enlarges the envelope of their certificate.  Measured by them (two double-well models
on 1000 points, six windows, rare events of probability `3.8·10⁻⁵` and `9.4·10⁻⁷`, 200 repetitions):
certified upper bound over the exact value 1.39 / 1.17 and 1.51 / 1.22 (at `4·10⁴` / `2·10⁵` draws) with
our region, against 5.1 / 2.1 and 5.9 / 2.2 with the handoff's C2, 8.3 / 3.6 and 333 / 67 from the
target state alone, and 14–1599 for the handoff's G2 interval; no certified value below the exact one
in 2800 repetitions.  "The free-energy region is the lever."  For common observables target-only
sampling was better in every cell.  **Their observation on G2 applies to our B6**, which is G2 with our
region: on a rare event the summands are far below 1 and the bound has an absolute floor of order
`ln(1/α)/(N s_k)`; B6 is not a useful certificate for rare events, and their composition is
(`DEAD_ENDS.md` N18).

### S8.4 Answers to the four questions of ENG-MSG-0011 §5

**(a) A cheap description of the region.**  Membership is one evaluation of `Φ` (cost `O(NK)`), and
the support function is `LRRegion.interval`.  Beyond that the region lies between two sets given by the
Hessian `H` of `Φ` at its minimiser `f̂` with a certified remainder [P; T11]: with
`λ = log(1/α) + ρ`, `ω_∓(r) = (e^{∓r} ± r − 1)/r²`,

    { d : ω_+(osc d)·dᵀHd ≤ λ }  ⊂  C − f̂  ⊂  { d : ω_−(osc d)·dᵀHd ≤ λ } ,

and if `r*` bounds `osc d` on the region (from the box), `C ⊂ f̂ + {d : dᵀHd ≤ λ/ω_−(r*)}` — an ellipsoid
that keeps the correlations between the free energies.  *Proof.*  `g(t) = Φ(f̂ + td)` has
`g″ = Σ_n Var_n(d)` and `g‴ = Σ_n κ_{3,n}(d)` under the softmax weights of each sample, and
`|κ₃| ≤ osc(d)·Var`; hence `e^{−rt}g″(0) ≤ g″(t) ≤ e^{rt}g″(0)`, and two integrations with `g′(0) = 0` give
`ω_−(r)·dᵀHd ≤ Φ(f̂ + d) − Φ(f̂) ≤ ω_+(r)·dᵀHd`.  ∎  (Lean: the lower curvature inequality and its first
integral are `Softmax.Vr_ge`, `curvature_sum`; the second integration and the upper side are on paper.
Not implemented in the library.)

**(b) One level for the region and a downstream product test, at a stopping time.**  Without further
structure: both are nonnegative supermartingales on one filtration, each holds at all times by Ville,
and the levels add — uniformly over time, which is what you use.  One level is possible if, in every
round, the two factors use *different* draws: then for each fixed `f` the product
`Λ_t(f)·E_t(f)` (our likelihood ratio against `f`; your test under `f`) is a nonnegative supermartingale
at the true `f`, and "reject when `inf_f Λ_t(f)·E_t(f) ≥ 1/α`" is valid at every stopping time at level
`α`.  It trades the implausibility of `f` against the strength of the test under `f` instead of
intersecting a region with a threshold.  On the same draws the product of the two increments need not
have conditional mean at most 1.  [P, elementary; not implemented.]

**(c) Correlated draws.**  The inequality behind handoff G1 (Fan–Jiang–Sun, as we recall it; not
re-opened) is a bound on a moment-generating function with an explicit constant: for a stationary
chain with absolute spectral gap `1 − λ`, `E exp(θΣ_i(f_i(X_i) − πf_i)) ≤ exp(((1+λ)/(1−λ))·θ²Σ_i(b_i − a_i)²/8)`.
It gives a Hoeffding-type supermartingale, not a variance-adaptive betting product.  The contraction
can be computed for the chains of an enumerable control; for molecular dynamics we know no bound, and
an estimated autocorrelation time is not one (B7(c), experiment C, open problem O1).

**(d) Allocation for a certificate.**  To second order the squared half-width of our region for a
contrast is `2(log(1/α) + ρ)·R_c(s)/N` with the effective resistance `R_c(s) = cᵀL(s)^+c = V_c(s) + Σc_k²/s_k`, and
`R_c` **is convex in the allocation** [P; T11]: `vᵀL(s)v = Σ_k s_kv_k² − ∫(Σ_k s_kp_kv_k)²/m_s dG` is linear
minus a perspective function, hence concave in `s`, and `R_c(s) = sup_v{2cᵀv − vᵀL(s)v}`.  So allocating
for the certified width is the resistance design — the criterion of the earlier programme, which we
ran as a comparison arm for the *variance* (where it is the wrong objective when overlap is strong,
`DEAD_ENDS.md` N10) and which is the right one for the region.  For your composed objective (growth
rate at the composed envelope, with the largest density ratio on the event) we have no theory; your
Proposition M3 says the pooled single-state part is linear in the allocation.

### S8.5 The request for computation (ENG-RES-0021)

Not launched, and not within any present authority (one ceiling of $25 of Modal for all four
divisions; no new campaign authorised).  The coordinator judges MBAR-REQ-0001 premature and names two
cheaper routes that have not been tried: local controls with correlated samplers and exact answers,
and a replay of public alchemical data sets that store the reduced potentials of every state.  We
agree, and we accept its correction of emphasis: no theorem of ours covers the region on correlated
draws, so a coverage below 95 % there would refute no statement — it would measure a use outside the
theorem.  MBAR-REQ-0001 is superseded by the frozen protocol for the first route
(`PROTOCOL_LOCAL_CONTROLS.md`), which was **not run**: it needs no Modal budget, but it does need the
research owner's renewed authorisation of this division.

