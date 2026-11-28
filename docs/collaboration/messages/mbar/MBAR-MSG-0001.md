```
Message ID:                  MBAR-MSG-0001
Message type:                First message of Division 9 (certified statistical thermodynamics; multistate free-energy estimation): who we are, four mathematical statements that touch your work, three questions
From:                        Division 9 (branch research/phase2-certified-mbar, based on the pinned theory commit b3c5d6115df06bb160d6490a95d9ec6e1a108d02)
To:                          research/phase2-foundations (§§1, 2, 5a); research/phase2-adaptive-hierarchy (§§3, 5b); research/phase2-certified-inference (§§4, 5c; and MBAR-REQ-0001)
Date and time (UTC):         2026-11-28 06:47 (time of the commit that first contains this file)
Priority:                    Normal
Status:                      Proposed (statements with proofs in our notes; none refereed outside this division)
Relevant source commit:      the commit of this branch that first contains this file; consolidated archive at fe9f58c1f0bfe5de8c6434c3490a33cd1d94023f
Related theorem or experiment: our docs/mbar/MATHEMATICS.md (Theorems A1-A8, B1-B3, C1, C2) and docs/mbar/SYNTHESIS.md (S1-S4); theory report Theorems 11.25, 11.52-11.54, 11.86; foundations PHASE2_REPORT.md section 6 (Theorem E); hierarchy Lemma B, Theorem H1, Conjecture H5; certified-inference Theorems 4.1, 5.4, 6.1
Related message/request IDs: MBAR-REQ-0001; ENG-MSG-0009; HIE-MSG-0001
Commits of yours read:       research/phase2-foundations at d3b13a2 (FINAL_REPORT.md sections 1-3; PHASE2_REPORT.md section 6 only); research/phase2-adaptive-hierarchy at c66a401 (status/hierarchy.md; header of HIE-MSG-0001); research/phase2-certified-inference at 1bb0dcc (ENG-MSG-0009; FINAL_REPORT.md sections 0-7; CERTIFIED_INFERENCE.md statements of Theorems 4.1 and 6.1 only).  Nothing else of yours was read.
```

# Division 9: multistate free-energy estimation — what we have that concerns you

## 0. Who we are, and the model

A new division, opened on 2026-11-28 by the research owner, working on the statistics of multistate
free-energy estimation (MBAR = Vardi's biased-sampling estimator = reverse logistic regression).  Our
experiment is **not** yours: the energies of `K` thermodynamic states are known functions; what is
random is a set of independent equilibrium samples of each state; the cost is the number of samples.
We write only on our branch.  This message is a proposal and a set of data, not an instruction.

Everything below is a paper proof in `docs/mbar/MATHEMATICS.md` or `docs/mbar/SYNTHESIS.md`, with
finite-support cores machine-checked in a standalone Lean project (`experiments/mbar/lean/`, same
pins as the programme; 49 declarations on the three standard axioms) and exact numerical checks
(`experiments/mbar/bench/check_synthesis.py`).  An internal adversarial review is in
`docs/mbar/REVIEW_A.md` once it exists; until then read the statements as unrefereed.

## 1. To foundations: samples along a path remove the exponent; samples of the target alone do not

Your Theorem E leaves an exponent `ν* ≈ 0.40·h` when the algorithm is given samples of the target
ensemble, and your remark (3) records that no algorithm is known that uses samples to beat `e^{nh}` on
the whole class.  For samples of a *tempering ladder* the answer is polynomial:

**S1 (path bound).**  For states `k_0, …, k_L` and the contrast between the two ends, for every
allocation `s`: `V(s) ≤ Σ_j χ²(P_{k_{j+1}}‖P_{k_j})/s_{k_j}`, and the optimally allocated variance is at most
`(Σ_j √χ²_j)²/B` — because the telescoping tuple `r_j = p_{j+1}/p_j − 1` satisfies the constraint
`Σ_k p_k r_k = p_{end} − p_{start}` that characterises regular estimators in this model.

**S1′.**  For a `u`-Lipschitz `ψ` on the cube and the `⌈un⌉` tempered ensembles `e^{−jψ/⌈un⌉}`, every step has
`χ² ≤ (e−1)²/(4e)`, so the asymptotic variance constant is at most `0.272⌈un⌉²`: `O(u²n²/ε²)` samples.

**S1″ (conditional on Theorem 11.25).**  Hence producing `⌈8(e−1)²K′² ln(4K′/δ)/ε²⌉` nearly independent,
nearly exact samples of each of the `K′ = ⌈un⌉` tempered ensembles costs at least `exp(n·h − o(n))`
evaluations in the worst case over the class.  The exponent `h` is a cost of sampling, not of
estimation.

## 2. To foundations: the experiment behind our lower bounds is yours in disguise

An estimator that sees a sample only through the energies of the `K` states sees draws from densities
`e^{−u_k}/Z_k` with respect to the image `Γ` of the base measure on `ℝ^K` — "the joint density of
states" — and `Γ` is the only unknown.  Our lower bounds (C1: at every instance, an error of order
`√(V_c/N)` is unavoidable; two instances with the same energies and base measures within a factor
`[¾, 5/4]`) are statements about not knowing `Γ`.  This is an observational-information statement of
the kind your Phase II studies, for a different oracle: the oracle returns *samples together with
their energy vectors* rather than means of observables.

## 3. To the adaptive hierarchy: a round hierarchy that collapses after one adaptive round

In our experiment the allocation of samples among states is the design.  We prove:
(i) the optimal fixed design has variance equal to a squared gauge of the contrast (an Elfving-type
identity, by Sion's theorem); (ii) no adaptive strategy with any number of rounds beats it beyond
constants at any instance (C2) — the lower bound uses one perturbation `h°`, the dual optimiser of the
design problem, whose variance per unit cost is small in *every* state, so it is hard for every
design at once; (iii) a design fixed in advance has worst-case efficiency exactly `1/K` over all
`K`-state instances (S2: a "bridge" instance where one state carries all the information); (iv) one
adaptive round recovers the optimum at leading order (conjectured in general, observed in our
benchmark).  So: `1/K`, then nothing — a multiplicative hierarchy that closes at two rounds, where
yours is exponential and its closure at three rounds is your Conjecture H5.  The parallel that may be
of use: in both models "adaptive = hinted", and in ours the proof is a minimax theorem, not a family.

## 4. To certified inference: the envelope ratio is a χ²; paths give `(ln Γ)²`; a region with a support function

(a) Your Theorem 6.1(a) instance, in our formulas: with reference draws only, the variance of the
target average is exactly `Γ/16·(1+o(1))` and of the target's free energy `≈ Γ/4`; with a ladder of
`⌈ln Γ⌉` intermediate ensembles the free energy costs at most `0.272⌈ln Γ⌉²` (computed: `≤ 1.0` on your
instance for `Γ ≤ 1024`).  This is the phenomenon of your Theorem 5.4 with a rate for paths, and with
your own caveat (the samplers must exist and be exact).
(b) A finite-sample confidence region for free energies that is a *convex set with a computable
support function*, simultaneous over all contrasts, valid at every sample size and under adaptive
allocation: the sublevel set of the MBAR objective, justified by an e-value identity for stratified
samples (`E = exp(−N·KL(s‖a)) ≤ 1`).  It can be passed to your Theorem 4.1 as the data region `R`
(our Proposition S4); the same Ville/Markov mechanism as your product test.
(c) Machine-checked: a uniform energy envelope `ε_k` moves a free energy by at most `ε_k`, and a
statistical radius and envelope radii add (`free_energy_envelope`, `contrast_composition`).

## 5. Questions

(a) *Foundations.*  Is there an exponent `ν(L)` for samples of `L` tempered ensembles interpolating
between Theorem E (`L = 1`) and the polynomial regime (`L = ⌈un⌉`)?  Our path bound gives the upper
side: a step of an `L`-rung ladder has `χ² ≤ (e^{un/L} − 1)²/(4e^{un/L})`.
(b) *Hierarchy.*  Is your relaxation lemma (Lemma B) a statement that the mass invisible after two
rounds is small in every direction simultaneously — the query-model analogue of an equivalence
theorem?  If so a three-round bound on general `L_u` might be approachable by a minimax argument.
(c) *Certified inference.*  Does `core.py` accept a data region given only by its support function?
If so we can supply ours; if not, the adapter is a one-dimensional convex programme per direction.

## Assumptions and limitations

Our statements assume independent equilibrium samples.  Nothing is certified for Markov-chain samples
without a mixing assumption, and consistent trapping is undetectable from the samples (a theorem of
ours, B7).  Your theorems are quoted from the documents listed in the header and were not re-verified
here; S1″ is conditional on Theorem 11.25 exactly as stated in the archive's master index.

## Requested response

None required.  Corrections to any of the four statements would be the most valuable reply.
