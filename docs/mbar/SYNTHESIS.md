# Division 9 — cross-divisional mathematical synthesis

*Written by the coordinating AI session of Division 9.  Statements of other divisions are imported with
their branch, commit and status and are **not re-verified here** unless said; a statement of this note
that depends on one of them is conditional on it.  Labels as in `MATHEMATICS.md`.  Numerical checks:
`experiments/mbar/bench/check_synthesis.py` → `results/synthesis_checks.json`.*

Branches read (heads on 2026-11-28 05:23 UTC): `research/phase2-foundations` `d3b13a2`,
`research/phase2-adaptive-hierarchy` `c66a401`, `research/phase2-certified-inference` `1bb0dcc`;
archive `fe9f58c`.  Only the documents named below were read, and of those only the cited sections.

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

**Proposition S1 (path bound)** [P; N].  Let `k_0, k_1, …, k_L` be any sequence of states with
`P_{k_{j+1}} ≪ P_{k_j}`, and `c = e_{k_0} − e_{k_L}`.  Then for every allocation `s`

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
over any reference.  Each step has density ratio with oscillation at most `e`, hence
`χ² ≤ (e−1)²/(4e) < 0.272` (Bhatia–Davis), and for the free energy `ln E_π e^{−ψ}`

    V*_c ≤ V_c(uniform on the K′ sampled states) ≤ 0.272 · K′² .

So with exact samplers of the tempered ensembles, `0.272⌈un⌉²(1.96/ε)²` samples give accuracy `ε`
asymptotically, and the region of Theorem B2 certifies it; on 27 random Lipschitz energies on cubes of
8–12 sites the exact `V_c` is 5–14 % of the bound.

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
2. no adaptive strategy, with any number of rounds, beats `V*_c(B)` beyond constants, at every instance
   (C2): "adaptive = oracle design";
3. **Proposition S2 (one round)** [P; N].  Over all `K`-state instances, an allocation fixed in advance
   has worst-case efficiency `min_k s_k`; uniform allocation attains the optimum `1/K`.
   *Proof.*  Upper bound: `V(u) ≤ max_k(s*_k/u_k)V(s*) ≤ K·V(s*)` by monotonicity and homogeneity.  Lower
   bound: the *bridge instance* — `P_a` uniform on a block `A`, `P_b` uniform on `B`, `P_m` uniform on `A ∪ B`,
   the other states copies of `P_a`: samples of every state except `m` are constant in the energies
   and carry no information about `f_b − f_a`, so `V(s) = 4/s_m` and the efficiency of `s` is exactly `s_m`;
   the adversary chooses which state is the bridge.  ∎  (Checked: efficiency `= s_m` to `10⁻¹⁵`.)
4. two rounds (a pilot and one adapted round) reach `V*_c(B)(1 + o(1))` on every fixed instance
   [C: standard for sequential designs, not proved here; consistent with the benchmark, where the
   two-stage rule matches the oracle allocation within noise in 6 of 8 systems].

So the round hierarchy of the sampling experiment is: **one round loses a factor up to `K`; two rounds
lose nothing at leading order; more rounds cannot gain** — a multiplicative gap that closes after one
adaptive round, against an exponential gap in the query model whose closure after three rounds is the
hierarchy division's open conjecture.  The structural parallel is exact in one respect: in both models
the value of adaptivity is the value of a *hint about the design* (theory: "adaptive = hinted";
here: "adaptive = oracle allocation"), and in both the lower bound is proved by exhibiting one
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
`1, Γ`) it equals `Γ/16·(1 + o(1))` exactly (computed: `V/Γ = 0.0625` at `Γ ≥ 64`).  Sampling the
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

**Proposition S4** [P].  Let `R̂` be a random convex region with `P(E_p φ ∈ R̂) ≥ 1 − α`.  Then the
interval of Theorem 4.1 computed with `R̂` contains `E_p f` with probability at least `1 − α`.
Two regions of this division qualify: (i) for `φ` bounded observables of a sampled state, the box of
the intervals of `MATHEMATICS.md` B6 (levels added up); (ii) for `φ` free-energy differences between
thermodynamic states (populations of macrostates are of this form, `−log` of a ratio), the
likelihood-ratio region `C` of B2 itself — convex, with support function
`h_C(η) = sup_{f∈C} η·f` computed by one convex programme per direction
(`LRRegion.interval`).

*Proof.*  Soundness of Theorem 4.1(a) on the event `{E_p φ ∈ R̂}`.  ∎

The statement is elementary; its content is the interface: a *simultaneous* region with a computable
support function is exactly what the dual of Theorem 4.1 consumes, and the region of B2 has both
properties without a union bound over observables.  Not done: running the certified-inference
library on such a region (its `core.py` accepts boxes and ellipsoids; a general support function
would need a small adapter) — proposed in MBAR-MSG-0001.

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
| S2 | round hierarchy of allocation: `1/K`, then nothing; contrast with the query model | (1)–(3) [P]; (4) [C] |
| S3 | the envelope-ratio cost is a χ²; paths give `(ln Γ)²` | [P], [N]; composition [V] |
| S4 | regions with support functions as data regions | [P], elementary; not run |
| S5 | intervals for second moments and populations | interface only |
| S6 | allocation for observables | theory [P]; one plug-in example |
