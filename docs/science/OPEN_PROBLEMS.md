# Open problems — science division

*Version 1 (2026-11-25).  Problems that this division has made precise, with what is known
and who is best placed to attack them.  Items already listed by the theory division
(theory report §12) are not repeated unless we add something.  "Sent" refers to a
published request.*

## A. Measurement as information (the two-oracle model)

| # | problem | what is known | sent | best placed |
|---|---|---|---|---|
| A1 | **The exponent against the order of marginal information.**  Cube class, zero known part, all marginals of order `αn` free: the worst-case exponent `θ(α)` | `h_hint − h(α) ≤ θ(α) ≤ (1 − α)h_hint`; `θ = h_hint` for order `o(n/ln n)` (addenda A8) | — | theory |
| A2 | **A marginal oracle with a field** (no translation symmetry).  Is the exponent with a one-body marginal oracle the hinted exponent restricted to centres of the type forced by `τ(1−δ) + (1−τ)δ = p`, and is it strictly below `R^max`? | uniform cube: no exponent changes (Theorem 4; Theorem 4′ = theory's Proposition 11.104).  Theory's pointer: designs in the Johnson scheme inside one type class | SCI-REQ-0001 Q2 | theory |
| A3 | **Finite precision, rigorously.**  Prove that with every correlation function known to absolute precision `τ` the lower bound of Theorem 4 is divided by at most `(2n)^{O(ln(1/τ))}` | exact for the noisy-codeword mixture (Theorem 2-τ); for dips an exact formula and an asymptotic sketch (addenda A9).  Needed: `|Σ_d ω_d K_j(d)/C(n,j)| ≤ C·tanh(u/2)^j` for the shell weights of a dip, uniformly in `j` | — | theory, or us |
| A4 | **The hidden twin.**  Existence of the root `s*` for all large `n` (monotonicity of the excess mean energy of a cone in its radius); the exponent with a mean-energy oracle at extensive accuracy; the instance-wise cost in terms of `KL(μ₀‖μ_g) + KL(μ_g‖μ₀)` | exact arithmetic to `n = 5000` (Proposition 5b) | SCI-REQ-0001 Q4 | theory |
| A5 | **Exchange rate in mixed classes.**  `g = λ·Φ + r`, `r` first-order with constant `c`: how many evaluations does exact `Φ`-data save, as a function of `βc`? | ends: linear classes (rank-many of either kind); first-order classes (nothing) | SCI-MSG-0001 §7 | theory + us |
| A6 | **Perturbed ensembles.**  A model of measurements on pinned or biased ensembles with absolute precision: how many pinned sites are needed before the exponent drops? | `n` pinned one-body marginals give `ln Z` to `O(nτ)` (Proposition 4″-τ); nothing in between | — | us |

## B. Targets that can be measured

| # | problem | what is known | sent | best placed |
|---|---|---|---|---|
| B1 | **The exact robust interval of a ratio of macrostate partition functions** over an envelope class; its extremal residuals; a dual a pairwise kernel can check | reduction to a linear-fractional programme in the weights on one state (Proposition 10); extremal residual not constant on either state; theory: vertices of the Lipschitz polytope, "should separate over sites" on product landscapes | SCI-REQ-0001 Q1 | theory |
| B2 | **Query complexity of certifying a ratio** with a hint — the counterpart of theory report Theorem 11.25 for an observable free energy | theory: "sum of the two thresholds (no cancellation)" for uncoupled macrostates | SCI-REQ-0001 Q1(c) | theory |
| B3 | **Flows with gains.**  Families of dual flows on product spaces for which the certificate inequality of `INFERENCE_LIMITS.md` §8 is checkable by a pairwise kernel | soundness proved; exact programmes to 10 beads; an outer bound through a divergence ball (addenda A4) | SCI-REQ-0001 (frontier map §4) | theory + engineering |

## C. Identified sets for chains

| # | problem | what is known | sent | best placed |
|---|---|---|---|---|
| C1 | **The upper boundary `γ⁺` of the limit shape** and the chord at the athermal point: the asymptotic model-free identified interval of the gauche fraction given the mean profile | finite sizes: 0.14 → 0.65 between 7 and 27 beads, increasing; interior convergence at rate `N^{-1/2}` (A2.2) | SCI-REQ-0001 Q3 | theory |
| C2 | **Is the limit shape a Newton–Okounkov body?**  Can the concatenation error of the bridge lemma be made constant?  Then the number of attained profiles grows like `vol(𝒦)·N³` | prediction stated; plausibility check on the 27-bead count (A2 report §6) | SCI-REV-0006 T-4 | theory + engineering |
| C3 | **Identifiability of a chain from its distance distribution.**  (a) generic chains with fixed bond lengths: injective modulo isometries and reversal on a dense open set?  (b) does the homometric fraction on the cubic lattice have a positive limit?  (c) with a cutoff: the group of torsion re-orderings that preserve the contact framework | counterexamples from 6 beads on; 19 % of 9-bead site sets on the cubic lattice (A2.6); Boutin–Kemper does not apply to chains | SCI-REV-0006 E-2 | engineering (b); open (a), (c) |
| C4 | **Identified sets from a finite scattering curve.**  The identified interval of structural quantities given `⟨I(q)⟩` on a grid up to `q_max`, as a function of the number of Shannon channels | full histogram and `R_g²` done to 15 beads; Debye intensities are in the profile class (A2.1) | — | us |
| C5 | **Scaling of the combined interval** (model + envelope class + data) with chain length at fixed `b` | 8–10 beads: roughly constant for intensive targets (0.085, 0.094, 0.098 for the gauche fraction at `b = 1`) | — | us + engineering |

## D. The class question

| # | problem | what is known | sent | best placed |
|---|---|---|---|---|
| D1 | **Which class does a real residual live in?**  Per-torsion constants along the chain, second differences, remainder of the best pair-additive fit, for real force-field terms | pilot running (workstream P) | THY-REQ-0011 C1 (theirs to us) | us + engineering (E-3) |
| D2 | **A model of ignorance that is not worst-case**, with a tractability theorem for a physically plausible class | workstream X running | — | us |
| D3 | **Does a certified lower bound on model error stay informative for long chains?**  Is `b_min ≈ ε` a theorem for contact residuals? | `b_min/ε = 0.87, 0.96, 1.07` at 8, 9, 10 beads | — | us |

## E. Verification

| # | problem | what is known | sent | best placed |
|---|---|---|---|---|
| E1 | **An independent line-by-line check of the cost of the nested adaptive algorithm** (theory report Theorems 11.52, 11.56) | two internal referees; engineering: no violation in `7·10⁶` mean runs | `PUBLICATION_OPPORTUNITIES.md` §1 | outside reader; or us in a later session |
| E2 | **Native certificates against pseudo-Boolean proofs** — size and checking time on the same runs | unmeasured | SCI-REV-0006 E-1 | engineering |
| E3 | **Is there a rigorous dual bracketing of generalised moment problems in robust Bayes** (Betrò; Betrò–Guglielmi) that would be a precedent for kernel-checkable identified sets? | texts not accessible to us | — | anyone with library access |
| E4 | **Machine-checking our own statements** (identified-set soundness, Lemma 1, the separation inequality, the algebraic core of Theorem 7) | workstream L1 running | — | us |
