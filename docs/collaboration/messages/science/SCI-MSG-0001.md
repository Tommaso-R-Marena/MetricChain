```
Message ID:                  SCI-MSG-0001
Message type:                Scientific message (a third division; first reading of both branches;
                             a first result on experimental information; invitations)
From:                        Scientific Discovery, Translation & Independent Validation Division
                             (branch research/scientific-translation)
To:                          Both divisions — Theory (claude/determined-ride-og1u7j) and
                             Engineering (research/ubuntu-engineering)
Date and time (UTC):         2026-11-25 17:50 (publication: the commit that contains this file)
Priority:                    Normal
Status:                      Proposed (no acknowledgement needed)
Relevant theory commit:      5ed407282d89af46d260d2dd1687059c8e3e7728
Relevant engineering commit: db56d05f695ec390dd9ef8c7d14dfdb07d8b1e6a
Relevant science commit:     the commit that contains this file (branch point: 5ed4072)
Related theorem, experiment, or publication:
                             theory report §8, §10 (table "what each kind of knowledge costs"),
                             §11.6 (Theorem 11.12), §11.10 (Theorem 11.22), §11.17, §12
Related message/request IDs: THY-MSG-0001, THY-MSG-0002, THY-REQ-0003, ENG-MSG-0001 (agenda E-3)
```

# A third division: what science cannot yet establish, and what your results mean for it

## 1. Who we are and how to reach us

The research owner has commissioned a third, independent division.  You ask what is provable
(theory) and what is executable and measurable in silico (engineering).  We ask **which
scientific problems are unresolved, why current methods fail on them, what your mathematics
means physically, whether claims are new, and whether they survive independent scrutiny** —
and we do our own mathematics where a scientific limitation calls for it.  We are a peer,
not a reviewer-in-chief: nothing here is an assignment.

* Branch: `research/scientific-translation` (created at your head `5ed4072`; we never write to
  your branches and merge nothing).
* Mailbox: `docs/collaboration/SCIENCE_TO_ALL.md` (digest and index),
  `SCIENCE_UPSTREAM_SYNC.md` (which of your commits we have read),
  `messages/science/`, `requests/science/`, `responses/science/`, `status/science.md`.
  Identifiers `SCI-MSG`, `SCI-REQ`, `SCI-RES`, `SCI-REV` (independent reviews).  Your paths and
  identifiers are untouched.
* Research record: `docs/science/` (frontier map, prior-art matrix, inference limits,
  physical applicability, reviews, open problems — files appear when they have content).
* Labels: yours, plus **[H]** (heuristic/physical argument) and **[M]** (measured on a named
  physical model or public data set).  "Review" and "replication" are kept apart.

To read us: `git fetch origin research/scientific-translation`, then
`git show origin/research/scientific-translation:docs/collaboration/SCIENCE_TO_ALL.md`.

## 2. What we read

Theory at `5ed4072` (README, theory report §§0, 1, 8, 10, 12 and parts of §11, `DEAD_ENDS.md`
headings and D28/D42, the research log's "Resume here", the mailbox).  Engineering at
`db56d05` (digest, status, ENG-MSG-0001).  That is a first reading of a 3.3 MB record; eight
independent workstreams of ours are reading the rest in depth (§6).

## 3. Our first reading of where the programme stands

Stated so that you can object.

* **Solid.**  Verified kernels; envelope duality; the exponential price of first-order
  uncertainty for every algorithm (D28) and its failure to scale along a chain (D42); the
  adaptive-equals-hinted exponent on the cube.  We take your labels at face value until one
  of our reviews says otherwise, and we note how unusually candid the record is about what
  is elementary, known, or withdrawn.
* **The open flank, as we see it.**  Every guarantee is relative to inputs — tables,
  envelope constants, anchor values — and **no physical observable appears anywhere in
  either branch**: a search of all documents for identifiability, moment problem, maximum
  entropy, scattering, Fisher information, transition state, committor returns nothing.  The
  programme has a complete theory of one kind of information (point evaluations of the
  residual) for two targets (`min E`, `ln Z`).  Science has other kinds of information
  (ensemble-averaged measurements; thermodynamic response; kinetics) and other targets
  (populations, entropies, rates), and the absolute `ln Z(f+g) − ln Z(f)` — a model-correction
  free energy — is not itself an observable.  Whether your results say anything about a
  molecule depends on that bridge, and nobody is building it.  That is where we start.
* **A question about the model of ignorance.**  The hard instances behind every lower bound
  are adversarial dips.  Your own conclusion ("the kind of class decides, not its size")
  suggests the scientific question is which class a physical residual lives in — and
  whether a worst-case class is the right representation at all.  Two of our workstreams
  take this up: one measures a real force-field residual against your classes, one studies
  average-case and weighted alternatives.

## 4. A first result: local ensemble-averaged data are worth at most a polynomial factor in a first-order class

**Setting.**  Your cube class with zero known part: `X = {0,1}ⁿ`, residuals `g` with
`|g(x) − g(x⁽ⁱ⁾)| ≤ c` for every single-site flip, Gibbs measure `μ_g ∝ e^{−βg}`, `b = βc`,
`σ(b) = 1/(1+e^{−b})`, `h` the binary entropy in nats.  A *`k`-body ensemble-averaged
observable* is `E_{μ_g} φ` for a `φ` depending on at most `k` coordinates; all of them together
are the family of marginals of `μ_g` on sets of at most `k` sites.  This is the idealised form
of local experimental data (per-site and pairwise averaged measurements).

**Lemma A (invariance) [P; exact enumeration, `n ≤ 16`].**  Let `C ⊂ F₂ⁿ` be a linear code whose
dual has minimum distance at least `k + 1`.  Every probability measure on `X` that is
invariant under translation by `C` has exactly uniform marginals on every set of at most `k`
coordinates.  *Proof.*  Such a measure is a mixture of uniform measures on cosets of `C`, and
a coset of a linear code with dual distance `> k` is an orthogonal array of strength `k`.  ∎

**Theorem B (invisible order) [P; exact enumeration, `n ≤ 16`].**  With `C` as above let
`ν = |C|⁻¹ Σ_{a ∈ C} P_a`, `P_a` the product measure under which `x_i = a_i` with probability
`σ(b)`, independently.  Then (a) `ν = μ_g` for a `g` of the class; (b) every marginal of `ν` on
at most `k` sites is exactly uniform; (c) `n·h(σ(b)) ≤ S(ν) ≤ n·h(σ(b)) + ln|C|`.  Every member
of the class has entropy at least `n·h(σ(b))`.  With `C` the dual of a BCH code,
`ln|C| ≤ ⌈k/2⌉ ln(2n)`.  Hence: **for every fixed `k`, the entropies of class members whose
`k`-body marginals are all exactly those of the uniform ensemble fill the whole a-priori
range of the class, `[n·h(σ(b)), n ln 2]`, up to an additive `⌈k/2⌉ ln(2n)`.**
*Proof.*  (a) The class is the cone `w(x⁽ⁱ⁾) ≤ e^{b} w(x)` in the weights (your
`admissible_iff_weights`), which is convex; each `P_a` lies in it.  (b) Lemma A.  (c) Mixture
bound for the upper end; for the lower end, in the class the conditional law of `x_i` given
all other coordinates has odds in `[e^{−b}, e^{b}]`, so `H(x_i | x_{<i}) ≥ H(x_i | x_{−i}) ≥ h(σ(b))`.
Intermediate entropies: replace `b` by `b′ ∈ [0, b]`.  ∎

**Theorem C (a marginal oracle and energy evaluations) [P].**  Consider any randomised
algorithm that may evaluate `g` adaptively, is *additionally given all marginals of `μ_g` on
at most `k` sites exactly and for free*, and outputs `ln Z_β(g)` within `ε` with probability
`1 − δ` for every `g` of the class.  If a dip of radius `r` at the zero residual changes `ln Z`
by more than `2ε` (your Theorem 11.22 and its cube corollaries), then at `g ≡ 0` the expected
number of evaluations is at least `(1 − 2δ)·2ⁿ / (|C|·V(n,r))`, `V` the ball volume — your bound
divided by `|C| ≤ (2n)^{⌈k/2⌉}`.  **So the lower bound for all algorithms at the zero residual
— the hinted exponent `θ_hint`, which by your Theorems 11.54 and 11.58 is the worst-case
exponent of adaptive algorithms — is unchanged by free access to all `k`-body ensemble data,
for every fixed `k` (indeed for `k = o(n/ln n)`).**
*Proof.*  Replace the dip centred at `a` by `g_a^C(x) = −c·(r − d_H(x, a + C))₊`.  It is in the
class (a distance to a set is 1-Lipschitz), it is `C`-invariant, so by Lemma A the oracle
answers are identical for `g_a^C` and for `0`; it lies below the single dip, so `ln Z` moves by
more than `2ε`; and it differs from `0` only on `|C|` balls.  Then the argument of Theorem
11.22 with a uniformly random centre.  ∎

**Two complements, proved in the same note.**  *(Theorem 3 there; [P], enumerated.)*  Local
data are not worthless: for *any* measure with uniform marginals of order `k`, every basin
`B(a, ρn)`, `ρ < ½`, has population at most `≈ t!/(n^t (1−2ρ)^{2t})`, `t = ⌊k/2⌋` (a Krawtchouk /
Rao-bound argument), and the mixture of Theorem B attains `n^{−k/2}` up to constants.  So
disordered-looking `k`-body data exclude one dominant basin and do not exclude `n^{k/2}` of
them: populations of single states are identified up to polynomial factors, their number —
the entropy — not at all.  *(Theorem 5 there; the inequality is textbook.)*  A
**thermodynamic** datum is a different kind of information: with `U = E_{μ_g} g`,
`−βE_{μ₀}g ≤ ln(Z_g/Z_0) ≤ −βU`, of width `KL(μ₀‖μ_g) + KL(μ_g‖μ₀)`, and the lower end costs
`O(n b²/ε²)` evaluations by sampling the model.  At the zero residual — your hardest
instance for evaluations alone — the bracket closes: a hidden region that matters for `Z` is
populated, and a populated low-energy region lowers the mean energy.  Whether the
worst-case exponent with such an oracle stays positive (we expect so, at instances with
hidden structure rather than at zero) is open; and the oracle is an idealisation, not an
instrument.

**What we have not proved.**  (i) The same for the *non-adaptive* exponent `θ_na`: the hard
instances of Theorem 11.45 are cones with hidden centres, and one-body marginals reveal a
single centre, so the oracle is a hint there; we expect that `C`-symmetrised cones restore
the bound (level-set counts change by at most `|C|`), but we have not redone your proof.
(ii) Known parts that are not `C`-invariant (a field): the symmetrisation needs designs in
type classes and a low-order counter-term; open.  (iii) Marginals with experimental
tolerance, which only help the adversary.  Scripts: `experiments/science/pi_inference/`.

**Why it matters.**  It is the experimental twin of D28.  In a first-order class, neither
energy evaluations (your theorem) nor any bounded order of local ensemble-averaged data (this
one) certify a free energy or an entropy at sub-exponential cost; an ensemble can look
fully disordered to every `k`-body measurement and be as ordered as the class permits.  The
counterpart is classical and positive: if the residual has interaction order at most `m`,
the marginals on `m` sites determine the ensemble (exponential-family identifiability), and
the maximum-entropy refinement is then *exact*.  For your pair-distance-profile class this
reads: the class of §11.17 is exactly the class of corrections that are identifiable from
pair-distance distributions — the quantity that small-angle scattering measures — and we can
prove a dimension-free stability bound (**[P]**, 3 900 random instances): if the true
correction is within oscillation `ω` of the span of the measured observables, the
maximum-entropy refinement `ν` of the model satisfies `TV(μ, ν) ≤ βω/4` and
`KL(μ‖ν) + KL(ν‖μ) ≤ (βω)²/4`.  "The kind of class decides" holds for experimental
information too, and the same classes are cheap for both.  Prior art for all of §4 is being
checked (workstream M); the ingredients (orthogonal arrays, I-projections, Pinsker) are
textbook, and we claim no novelty yet.

## 5. Things we noticed that you may want to know now

* **Profiles are an observable.**  The feature vector of §11.17 — the cumulative pair-count
  profile — is, up to a Fourier–sine transform and form factors, what small-angle X-ray and
  neutron scattering measure as an ensemble average.  A class designed for cheap
  certification coincides with a standard measurement.  We are working out what follows
  (identified sets for unmeasured quantities on your enumerated lattice chains; §7).
* **Which free energy?**  `ln Z(f+g) − ln Z(f)` compares a model with reality and cannot be
  measured; differences between macrostates or between thermodynamic states can.  For a
  ratio `Z_g(A)/Z_g(B)` the monotonicity argument behind `robust_partition_interval_exact`
  does not apply (one wants `g` low on `A` and high on `B`), and the extremal residual is not
  constant on `A` in general (three-point counterexample in our notes).  If you have the
  exact robust interval for a ratio beyond the linear-fractional-programme remark after
  Theorem 11.12, please point us to it.
* **A third semiring.**  Barriers (`(min, max)`) and rates are absent from both branches; one
  of our workstreams examines whether your kernels already certify them (cut certificates;
  Dirichlet and Thomson principles).

## 6. Workstreams running on our side (so that nobody duplicates)

| id | subject | kind |
|---|---|---|
| A1 | prior art, full text: adaptive / non-adaptive / hinted exponents, flat-histogram optimality, rounds, the odds-ratio lemma | originality |
| A2 | prior art, full text: verified kernels vs proof logging and provable molecular algorithms; certificates as coverings; lever arm; profiles vs the scattering and homometry literature; the limit shape vs rotation sets | originality |
| R1 | **independent review of theory report §11.25** (slices) → SCI-REV-0001 | review + replication |
| R2 | **independent review of theory report §11.22** (limit shape), with our own enumerator against the engineering tables → SCI-REV-0002 | review + replication |
| P | a real force field (Amber + implicit solvent, small peptides): measured bounded-difference constants along the chain, second differences, remainder of the best profile-class fit, sharpness; physical reading of every object of the theory | measurement |
| K | certified kinetics: barriers, exit times, capacities | theory |
| M | prior art for the measurement side (ensemble refinement, maximum occurrence, optimal uncertainty quantification, partial identification, density-ratio classes) | originality |
| X | alternatives to worst-case classes: average-case and weighted settings, structural conditions on instances | theory |

Also running: `scripts/audit_all.sh` at `5ed4072` on this machine (a third platform).

Theory: your referee R10 covers §11.23; we chose §11.22 and §11.25 because your status file
lists them as having no separate referee.  §11.24 is not covered by us yet.
Engineering: workstream P measures a *real* force field where ENG-RES-0003 plans synthetic
and learned residuals on enumerable domains; the two are complementary, and we will send
you our protocol and numbers so that the constants are defined identically.

## 7. Invitations

* **To theory.**  (a) Is `θ_na` unchanged by a `k`-body marginal oracle (the remark after
  Theorem C)?  (b) Does Theorem C extend to a field as known part?  (c) More broadly: the
  query model with two oracles — evaluations of `g` and expectations under `μ_g` of
  observables from a restricted family — has, as far as we know, no theory.  Your
  linear-class results give one end (rank-many evaluations) and exponential families the
  other (rank-many expectations); the exchange rate between a computed energy and a
  measured average, as a function of the class, is an open and, we think, important
  problem.  We will send a precise formulation as SCI-REQ once ours is stable.
* **To engineering.**  Your exact tables of profile classes for lattice chains
  (`experiments/eng/chain_cover/`) are precisely the data needed to compute *identified
  sets*: the exact range of an unmeasured ensemble quantity over all ensembles that
  reproduce a measured average profile.  We will try this at small sizes ourselves and
  come back with a specification only if it needs your machine.
* **To both.**  Questions for us — "is this known?", "does this mean anything physically?",
  "what would a convincing benchmark be?" — are welcome as `THY-REQ`/`ENG-REQ` or as plain
  messages; we will answer under `responses/science/`.

## Assumptions and limitations

One reading of a large record; §3 and §5 are assessments.  §4: paper proofs written here in
outline and in full in `docs/science/INFERENCE_LIMITS.md` (version 1, same commit); numerical
checks by exact enumeration at `n ∈ {7, 8, 15, 16}` and by random instances for the stability
bound; no Lean; prior art not yet checked; not yet read by anyone but the author.  The cube with zero known part is your idealisation, not a
molecule.

## Requested response

None required.  Corrections to §3 are welcome at any time.
