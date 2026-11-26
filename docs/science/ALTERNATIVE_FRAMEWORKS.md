# Alternative frameworks: is a worst-case first-order envelope the right model of ignorance?

*Science division.  **Version 2** (2026-11-26, after checkpoint 43; version 1 was of
2026-11-25, checkpoint 20).  New in version 2: two rows of §1 (a higher-order envelope
with values on a Hamming ball; a divergence bound against a model that can be sampled),
§4b (what the measurements and certificates since version 1 decided), §5b (a cooperative
known part), and §8 marked with what was done.  §§2, 3, 5, 6 are unchanged.  A synthesis
for a reader who has not followed the session.  Sources: workstream X (`workstreams/SX_REPORT.md`; paper proofs, each tested
numerically, nothing machine-checked; one script re-run by the coordinator, four
arguments re-derived, see §9), workstream P (`workstreams/SP_REPORT.md`, measurements),
workstream K, `INFERENCE_LIMITS.md` with its addenda, and the theory report at `89ac710`.
Labels as in `SCIENCE_TO_ALL.md`.*

## 0. The answer in one paragraph

**The exponential price of the theory division's programme comes from the geometry of the
first-order class, not from the worst-case quantifier.**  A first-order class is a Lipschitz
polytope: what an evaluation at `a` says about `x` is a bound through the envelope distance,
and information from several evaluations combines by a *minimum*.  Replace the polytope by
an *ellipsoid* — the ball of a reproducing-kernel Hilbert space, or, read probabilistically,
a Gaussian prior — and information combines *linearly*: the uncertainty left at `x` after
evaluating a set `A` is `B_A·P_A(x)`, the distance of `x` to the span of the evaluated
representers.  On the cube, an ellipsoid whose spectrum sits on interaction orders up to `m`
costs about `n^m` evaluations, deterministically, in the worst case over the ball, for the
minimum and for `ln Z`; with orders up to `αn` the cost is exponential again, with exponent
the binary entropy `h(α)`.  So "worst case against Bayesian" is not the distinction that
matters most; "which interaction orders, how much" is.  And no cheaper paradigm can remain
valid on a first-order class: the assumption that replaces the envelope **cannot be
verified from polynomially many evaluations** (nor, by our own theorems, from averaged
data); it has to come from physics.  What physics says, in our one pilot: a continuum
solvent term is close to a pair-additive class in typical norm and several `k_BT` away from
it in supremum norm.  **Recommendation: combine** — envelopes where the known part is
sharp; a linear-information class for the rest; a supremum-norm floor, stated and accepted,
for what is outside — not a first-order envelope on the remainder, which brings the
exponential price back below the accuracy threshold its constant sets, however small that
constant is.

**What the work since version 1 decided (details in §4b).**  The recommendation was
tested on a production force field, in the variables where it can work — side-chain
rotamers on a fixed backbone.  There the known part is *exactly* pairwise, the solvent
term is pairwise up to third-order constants of `0.003–0.2 kcal/mol` for neutral side
chains, and **the combination certifies**: a low-order model fixed by evaluations on a
Hamming ball, a *proved* bound on what is left, and — for `ln Z` — either nothing more
(`ln Z` of a twenty-residue peptide, `3.5·10⁹` states, within 0.06 nats from 87 441
evaluations) or a sampled mean on top of a certified floor and variance (within 0.005).
Two things were not foreseen.  First, **for `ln Z` the supremum norm is the wrong
coordinate**: a remainder `11–12 k_BT` wide in supremum norm costs almost nothing when
the true ensemble is close to the model's in Rényi divergence (`D_2 ≤ 0.18`), a
remainder whose root-mean-square error *improves* under a fit can become more
expensive (serine on a helix: `1.66 → 1.20 k_BT` while the exponent `D_2` of the cost
goes from 16 to 45), and *nothing estimated from samples certifies which case one is
in* — the two-standard-error bar covers in 5–82 % of repetitions in the bad cases.  Second, **what fails in a compact geometry is
not accuracy but certifiability**: on a helix a fitted chain model is as accurate as on
a strand (`0.002–0.004 k_BT`), and every bound that treats atom pairs one at a time is
250–800 times too large, because the solvent term's self and cross parts cancel to one
per cent.  The open problem of this document is no longer "which model of ignorance"
but "a certified bound that sees a cancellation" (`OPEN_PROBLEMS.md` D6; workstream P5).

## 1. Four models of ignorance and what each guarantees

| | what is assumed | what is delivered | what can be checked | what happens when the assumption fails |
|---|---|---|---|---|
| **W** first-order envelope (theory division) | `g(x) − g(y) ≤ d(x,y)` for all pairs; the constants | an interval valid for every admissible residual; the check is a machine-verified kernel | the certificate; the envelope can be *refuted* by two evaluations (or by averaged data: our Theorem 8), never confirmed | the bound is off by the violation times a distance: graceful |
| **H** ellipsoid | `‖g‖_K ≤ B`: a spectrum and a size | an interval for every member of the ball; `B_A·P_A` is a computation | recomputation; the ball can be refuted (`yᵀK_AA⁺y > B²`), not confirmed | a sup-norm remainder `η` costs `η(1 + Λ_A)`, amplified by the Lebesgue constant of the design; a dip costs its full depth, undetected |
| **B** Gaussian prior | `g` is a draw from a Gaussian field; hyperparameters | an interval of posterior probability `1 − δ`; for `ln Z` also contributions never observed (self-averaging) | recomputation; goodness of fit sees wrong scales, not dips | coverage can fall to near zero on the affected instances, silently (measured: 9 % on instances with a dip) |
| **C** population calibration | the new system is exchangeable with a calibration set of known truths | marginal coverage over systems | coverage on further known cases | nothing for an individual instance; fails under distribution shift |
| **W_m** higher-order envelope with values on a Hamming ball *(new in version 2; the theory division's Theorems 11.18, 11.18a; our workstreams P2, P3)* | bounds on the mixed differences of order `m` of the residual (constants `c_T`), plus its values at all states within `m − 1` changes of an anchor | a sandwich `m₋ ≤ E ≤ m₊` of pairwise models: a certified minimum, and `ln Z` between two exactly solvable partition functions when the models are banded | the certificate; **and, for one real energy term on extended backbones, the constants themselves** — by interval enclosures of derivatives plus the ball's evaluations (P3: 5.5 million state checks, no violation; paper proofs, not machine-checked) | graceful in the constants; **unavailable** where the certified constants are far above the true ones — a compact geometry: 250–800 times, by cancellation the bound cannot see |
| **D** divergence from a model that can be sampled *(new in version 2; addendum A17; the theory division's §11.30; in print: Block–Shetty 2026, Hoeffding 1963)* | a bound `κ` on a Rényi divergence `D_p` of the true ensemble from the model's (`p = ∞`: a one-sided floor of the remainder); or a floor `b` and a variance bound `σ²` | an interval for `ln Z` with probability `1 − δ` from samples of the model: `Θ(e^κ/ε^{p/(p−1)})` evaluations; with `(b, σ²)`: width `2σ/√(Nδ) + W(b, σ²)`, no exponential bill | **nothing from the samples**: a sampled floor is not a floor (exact over sampled: 2.7 to 230 on five enumerated instances), a sampled variance was 9 and 70 times too small on a helix | silently: at `D_2 = 3–45` the two-standard-error bar covers in 5–82 % of repetitions and misses by up to 6 nats (measured on 45 real instances); bounds on moments of the remainder itself (mean, root mean square) give no finite cost at all |

**W_m and D are not rivals of W, H, B: they are what the recommendation of §0 turned
into** when it met a real energy function.  W_m is "envelopes where the known part is
sharp, a low-order class for the rest" with the low-order part *evaluated* rather than
assumed; D says what must be known about the rest for `ln Z` (a divergence, not a
norm), and W_m is so far the only source of a *certified* value for it.

**W**: if the constants are right the answer is right — and for a long chain the constants
make the computation impossible.  **H**: if the residual has no component outside a stated
low-order model larger than `B`, the answer is right at polynomial cost — and whether it has
is a physical question.  **B**: right with probability 95 % *if* residuals are drawn like
this; the only paradigm that can use what it has not measured.  **C**: of systems like the
ones checked, 95 % are inside their intervals.

## 2. The statements (workstream X; all **[P]** with numerical tests unless marked)

1. **Certificate for a ball (Theorem 1).**  A set `A` certifies `min(f+g)` at the zero
   residual iff `B·P_A(x) ≤ gap_f(x) + ε` for every `x`.  This is the exact counterpart of the
   theory division's covering theorem, with the *power function* in place of the *slack
   distance*.  The band itself is the classical hypercircle inequality **[K]**.
2. **Two-sided design bound on the cube (Theorem 3).**  With `M(η)` the number of Walsh
   modes that carry all but `η²` of the spectral mass:
   `M(η) ≤ (least number of evaluations with max P_A ≤ η) ≤ 16(σ²/η²)·M(η/√8)`.  Lower bound:
   eigenvalue tail.  Upper bounds: duals of BCH codes (a spectrum on orders `≤ m` is
   determined exactly by `(2n)^m` evaluations) and random linear designs.
3. **Tractability and exponent (Corollary 4).**  Certifying the minimum over an isotropic
   ellipsoid is polynomial in `n` iff the order quantiles of the spectrum are bounded;
   otherwise the exponent is `h(α)`, `α` the limiting order fraction.  For the product
   covariance `σ²ρ^{d_H}`: exponent `h((1−ρ)/2)`; polynomial iff `ρ = 1 − O(1/n)`.
4. **`ln Z` is strictly cheaper than the minimum (Theorem 5, Proposition 5′).**  The exact
   interval of `ln Z` over the consistent members of a ball is a variational formula with a
   *Gibbs-averaged* posterior kernel.  Over an order-2 ball with a uniform reference the
   unknown pair part moves `ln Z` by at most `−½ln(1−βJ) − βJ/2` below the critical point
   `βJ = 1` of its worst member — a Curie–Weiss ferromagnet — although it moves the minimum
   by an extensive amount.
5. **A third kind of component (Proposition 7).**  Under a prior, "polynomial iff the
   spectrum decays" is *false* for the value of `ln Z`: a white (random-energy) tail costs
   `O(n)` evaluations in the annealed regime, where its contribution self-averages, and
   essentially `2ⁿ` in the frozen one.  Worst-case classes know only "learnable" and
   "frozen"; the self-averaging part is real physics and is the part of a Bayesian guarantee
   that rests most heavily on the prior — it is certified without any data about it.
6. **No free hedging (Proposition 8(c)); a corollary of the theory division's
   machine-checked instance-wise bounds.**  An algorithm that is correct on a first-order
   class pays that class's instance-wise price at every instance, whatever it assumes about
   a benign subclass.  "Assume the benign class and fall back if the data contradict it" is
   not available: the contradiction itself costs exponentially many evaluations to see.
7. **Sharpness with interacting known parts has a short proof under a checkable condition
   (Theorem 9).**  The *LP-funnel slope* `τ_LP ≤ τ`: one evaluation certifies iff the envelope
   is below the funnel slope `τ`, and a polynomial-size dual certificate of that fact,
   checkable by the existing kernel, exists iff the envelope is below `τ_LP`.  Equality on
   trees and for ferromagnetic binary known parts; a triangle with `τ = 3/2`, `τ_LP = 1/3`.
8. **The lever arm belongs to the format, not to the residual (Proposition 4″).**  An
   energy quadratic in the positions has interaction order equal to the chain length and
   per-torsion constants that grow along the chain, yet only `n(n+1)/2` Walsh modes (interval
   modes).  Residuals local along the sequence, with arbitrary position-dependent weights,
   cost a number of evaluations *linear* in the chain length (Corollary 4′).  Short-range
   contacts are not low-dimensional in any torsion-like coordinates: they need type-shared,
   body-ordered *features* (Proposition 10, a synthesis).
9. **Randomisation in an additive class (Proposition 11).**  At extensive accuracy `ε₁n`,
   `O(R²/ε₁²)` random evaluations suffice, independently of `n`, against `Θ(n)` for
   deterministic algorithms — the opposite of the first-order class.  Fills the cell
   "no lower bound known" of the theory division's summary table.

## 3. Head to head (toy problems; evaluations needed, none given the instance as a hint)

| situation | envelope (W) | ellipsoid (H) | prior (B) |
|---|---|---|---|
| sharp known part, tight constants, `n ≤ 12` | **1** | about `n` | about `n` |
| pair residual, not sharp, oracle-tight constants, `n = 12` | 336 | 57 | 70 |
| the same with a safety factor 2 on the constants | 1 423 (a third of the cube) | 79 | 70 |
| additive residual, safety factor 2, `n = 100` | at least `e^{12.5}` (machine-checked product bound) | 101 | 101 |
| lever-arm toy chain, oracle-tight constants, `n = 12` | 1 719 of 4 096 | 41–78 | — |

The envelope paradigm is the cheapest of the three when the known part is sharp and its
constants are tight; it is the only one whose cost is exponential in `n` at any fixed
slack.  With oracle-tight constants the separation is not visible at enumerable sizes.
**The slack `κ` of the certified constants over the truth decides the cost of W more than
anything else** — and a certified envelope always has slack.

## 4. What our measurements add (workstream P)

* The slack and the spectrum are now measured once.  For the GBn2 solvent term in backbone
  torsions the *exact* per-torsion constants are already `12–53 k_BT` (so W is out of reach
  with no slack at all), and low orders in *torsion* coordinates fail (all torsion pairs:
  RMS 2.1, max 13 kcal/mol at five residues) — as item 8 predicts for a residual made of
  pair distances.
* In body-ordered, type-shared *features* (36 atom-type pairs, radial functions) the same
  residual is within `0.26 kcal/mol` RMS — a linear-information class with about `10³`
  coefficients, independent of chain length in principle.  That is H or B with a good
  spectrum.
* What is outside the class is `2–9 kcal/mol` in supremum norm (`4–16 k_BT`), growing with
  the chain.  By §1, row H, that floor is *amplified* against an adversary and averaged
  down against noise.  Whether the remainder of a real many-body term behaves like an
  adversary or like noise is not a mathematical question; its structure (quadratic in the
  Born-radius fluctuations, with an analytic bound) is the lead (`OPEN_PROBLEMS.md` D4).
* The pilot's Jensen gap — 2–3 nats where the first-order class allows 71–178 — is the
  self-averaging of item 5 seen on a real residual.

## 4b. What the measurements and certificates since version 1 add  (workstreams P2, P3; addendum A17 (6)–(11); all model-relative: ff14SB as known part, GBn2 as residual, synthetic capped homopeptides and one patterned sequence, rigid backbones, 300 K)

1. **In the right variables the low-order class is real [M; P2].**  Side-chain rotamers
   on a fixed backbone: the force field's known part is exactly pairwise with one site
   per residue; the solvent term is pairwise up to third-order constants of
   `0.003–0.2 kcal/mol` for neutral side chains (`2.4–10` for lysines).  First-order
   constants saturate for neutral side chains (valine `0.4–0.8`, serine `5–9.4`) and grow
   without bound for charged ones.  The second-order interface certifies the minimum of
   apolar instances from tens of evaluations out of `10⁵–10⁶` states and fails for polar
   and charged ones (the *pair* part of the residual is large); the third-order
   interface is exact on every enumerated instance.  So item 8 of §2 — "the lever arm
   belongs to the format" — has its positive counterpart: change the format and the
   class is cheap.
2. **For `ln Z`, divergence and not width [M; A17 (6)].**  With the known part alone as
   the model, the remainder is `11–12 k_BT` wide in supremum norm for apolar side chains
   while `D_2 ≤ 0.18` (valine), `0.70` (leucine); for serine `D_2 = 3–45`.  With the
   pairwise fit as the model, `D_2 ≤ 1.3·10⁻³` and `D_∞ ≤ 3.7` in all 74 instances,
   although the remainder beyond pairwise is up to `14.8 k_BT` wide for four lysines.
   **Fit quality does not predict the price**: on the serine helix the root-mean-square
   error falls from `1.66` to `1.20 k_BT` while `D_2` rises from 16 to 45.  This is row H's
   warning ("a dip costs its full depth, undetected") measured on a real term, and the
   reason row D asks for a divergence.
3. **A floor and a variance are enough, and tight [K inequality; M sharpness; A17 (7)].**
   Hoeffding's Theorem 3 with the exact floor and variance of the remainder is within a
   median factor `1.04` of the true Jensen gap on 53 instances (true gap `≤ 6.3·10⁻⁴`
   nats); a range-only bound allows up to 11 nats.  The exponential bill of row D at
   `p = ∞` is the price of not knowing the variance.
4. **A chain is enough as the tractable model [M; A17 (9), (10)].**  One-body terms and
   pairs up to two residues apart (four on a helix) — exactly solvable and exactly
   sampleable at any length — leave a remainder of `0.002–0.007 k_BT` at 20–50 residues
   (`10⁹`–`10²⁸` states) once the tables are fitted.
5. **The combination certifies, once [P + M; P3].**  Evaluations on a Hamming ball about
   an anchor, a term-by-term bound on the tail in closed form, a sandwich of banded
   pairwise models: `ln Z ∈ [518.2332, 518.2937]` for a twenty-residue valine peptide on a
   polyproline backbone (`3.49·10⁹` states) from 87 441 evaluations with no sampling;
   `[518.2598, 518.2648]` with 50 000 samples and a certified floor and variance;
   replicated by an uncertified estimate with other code (`518.2626 ± 0.0001`).  By
   analysis alone — no evaluation of the solvent term — the same bound is 33–1 400
   times too loose.
6. **Where it stops [M; P3, A17 (10)].**  On a helix the certified constants fall by
   only 5–8 per order (21–51 on a strand) and the recipe fails at every affordable
   order, while the *true* remainder of a fitted chain model is as small as anywhere.
   The price is small and the proof is missing.  Charged side chains: the domains are
   not products and the constants grow; nothing certified.
7. **What an uncertified interval is worth [M; A17 (11)].**  On 45 instances × 3 models
   with exact laws: the two-standard-error bar covers in 92–100 % of repetitions when
   `D_2 < 1` and in 5–82 % when `D_2 = 3–45`; brackets with a guarantee (given the true
   floor, or floor and variance) never fell below 0.978 at nominal 0.95; with a good
   model the floor-and-variance bracket is narrower than the empirical-Bernstein one by
   a median factor 134, with a poor one it is wider — the floor decides, at about one
   `k_BT`.  The benchmark's own refutation criterion (a family on which the
   root-mean-square error predicts the certified cost) was not met.

**What this does to the table of §1.**  Row W is confirmed out of reach in torsion
variables and *alive at higher order in rotamer variables*.  Row H's amplification of a
supremum-norm remainder is real but, for `ln Z`, beside the point: the quantity to bound
is a divergence.  Row B's "contributions never observed" (self-averaging) is exactly
what row D certifies when a variance bound exists, and exactly what fails silently
when it does not.  Row C was not tested.

## 5. The same dichotomy for measured data (our own results)

| class geometry | evaluations | ensemble-averaged data of order `k` |
|---|---|---|
| first-order polytope | exponentially many (theory division) | worth a polynomial factor — exactly, and at every fixed precision for all orders (Theorems 4, 4′, 4-τ) |
| linear / ellipsoid of order `m` | about `n^m` | for `k ≥ m` they determine the ensemble (exponential families **[K]**); a remainder outside the span costs `TV ≤ tanh(β·osc/4)`, dimension-free (Theorem 7) |

The same codes do both jobs: a linear code of minimum distance `2m+1` makes its dual a
*design* that resolves every interaction of order `≤ m`; a code of dual distance `> k` is the
*adversary* that hides a dip from every `k`-body average.  Low-order information is complete
for low-order classes and blind for first-order ones.  And classes are refutable, never
confirmable, by either kind of information: evaluations (item 6) or data (Theorem 8: data
certify a *lower* bound on the envelope constant).

*An observation not yet examined* **[H]**: against a supremum-norm remainder, evaluation
designs lose a Lebesgue constant (up to about `√M`) while the maximum-entropy refinement
against averaged data loses none (Theorem 7 is dimension-free).  The two bounds are about
different objects (an interpolant; a Gibbs measure), so this is a question, not a finding:
is expectation data intrinsically more robust to out-of-class remainders than evaluation
data?

## 5b. A cooperative known part  (new in version 2; the theory division's workstream Y, reviewed and replicated by our workstream R10, SCI-REV-0010)

Every exponent quoted in this document is for a known part that is a product measure.
For the one interacting known part worked out — a two-state chain with a
nearest-neighbour coupling — the exponents of row W move in a direction that depends
on the per-site envelope: above the product values at one `k_BT` per site (by the
structure factor at zero wave vector for small envelopes: proved at second order),
**below** them for the two cost exponents at three to six `k_BT` per site, above them for
the threshold at every slope (`PHYSICAL_APPLICABILITY.md` §3a).  And for row D the
variance bound of a remainder under a chain reference carries the same cooperative
factor (addendum A17 (8); an equality for a uniform field on the symmetric chain).  So
"the cost with an interacting known part" has no sign in general; it has a map.

## 6. Where the theory division's results sit in tractability theory

Their exponential rows are the discrete counterparts of the curse of dimensionality for
Lipschitz and fixed-smoothness classes in an unweighted supremum norm (instances or
analogues of known theorems).  Their cheap rows are finite-dimensional linear classes
(optimal recovery).  The known part, sharp sites, the normal form, the exact
rate–distortion exponents, the thresholds for `ln Z` and the hinted/adaptive exponents are
**not** instances of information-based complexity.  The middle that tractability theory is
about — high-dimensional classes with decaying or finite-order weights — is absent from
their table, and is where a physical residual plausibly lives.  (Full table:
`SX_REPORT.md` §4.1; reading levels there are abstracts and snippets.)

## 7. What this does *not* show

* The head-to-head numbers of §3 are toy problems with oracle choices of `B`, the
  envelope constants and the priors.  What §4b reports was computed on a production
  force field, but on exposed, rigid, synthetic homopeptides (one patterned sequence),
  with one instance beyond enumeration size; no buried environment, no flexible
  backbone, no comparison with any measurement; P3's proofs are on paper and its code
  has one reader besides its author.
* For spectra of exact finite order the ball paradigm reduces to the theory division's
  own "rank-many evaluations"; what the ellipsoid adds is the treatment of the tail, the
  exponent when the order is unbounded, and a Bayesian band that does not grow with `√M`.
* Evaluation counts ignore the cost of *checking*: minimising `f + ĝ_A − B_A P_A` is hard in
  general; the bridge to the pairwise kernel covers order two with a uniform bound on `P_A`.
* Nobody certifies `B`, the spectrum or the prior.  By item 6 nobody can, from polynomially
  many evaluations.
* Prior art was read at the level of abstracts and snippets; nearly every ingredient is
  known (hypercircle inequality; Mitchell–Morris–Ylvisaker 1995 for the aliasing posterior;
  finite-order weights, Wasilkowski–Woźniakowski 2004; optimisation as hard as
  approximation; kernelised optimism; the second-moment method).  Not found in the
  workstream's searches (fourteen web searches and four page fetches, logged in its
  notes): the two-sided sup-norm design bound on `𝔽₂ⁿ`, the exponent `h((1−ρ)/2)`, the
  interval formula for `ln Z`, the LP-funnel slope.  "Not found" is not a claim of novelty.

## 8. What we recommend, and what would decide

1. **A sharp–soft decomposition with a verified kernel:** envelopes where the known part is
   sharp (item 7 gives the proof object for interacting known parts); an ellipsoid on the
   rest; soundness of the form
   `min(f+g) ≥ (kernel-certified bound of the pairwise model f + ĝ_A) − B_A·p̄` with a checkable
   certificate for `max P_A ≤ p̄`.  Request X-T1 of SCI-MSG-0007.
2. **Measure the three numbers that decide between the paradigms on one real residual:**
   the slack of the best certifiable first-order constants; the spectrum in a body-ordered
   feature space (`M(η)`); the size and kind of what is left.  Workstream P measured the
   first and third for one residual on one amino acid; the fixed-backbone case (request
   P-E1 of SCI-RES-0002) is the decisive one.
3. **State every guarantee as what it is** — class-relative, prior-relative or
   population-relative (§1) — and never present an interval without its row.

*What became of these three (version 2).*  (1) The band of the ellipsoid is
machine-checked by the theory division (their Proposition 11.50a and `HilbertBall.lean`
at `24a3c27`: `hypercircle_band`, `ball_certificate_sound`, and soundness through the
pairwise kernel, `verify_sound_ball` — as reported in THY-RES-0009; the file was
compiled in our replication of their audit and not read by us; the "iff" of Theorem 1
and the design bounds are not formalised).  The decomposition that was actually carried to a
certificate is row W_m, not an ellipsoid.  (2) Done for rotamer variables (P2, P3,
addendum A17 (6)); the request for a buried environment (P2-E1) is unanswered.  (3)
Stands, and has a measured reason (§4b item 7).  **Added in version 2:**

4. **For a free energy, compose three guarantees and say which is which:** an exactly
   solvable model (a chain or a banded pairwise model: no assumption); a *certified*
   floor and variance of the remainder (class-relative: row W_m supplies them where it
   can); a sampled mean (probability `1 − δ` over the samples).  Never put a sampled
   floor or a sampled variance in the second slot.
5. **Certify a cancellation.**  A bound on the tail of a solvent term that is within a
   small factor of the truth in a compact geometry — or a proof that no bound of a
   natural kind can be (`OPEN_PROBLEMS.md` D6; workstream P5, running at the time of
   writing).  Until then the certified route ends at extended backbones.

## 9. Provenance and checks

Workstream X: thirteen scripts in `experiments/science/ws_X/` (`NOTES.md` is its log).
Coordinator: `n1_coset_formula.py` re-run ("N1 OK"; a spectrum of exact order `m` is
recovered with zero posterior variance on the dual BCH design, and `sup P_A² ≤ 4·NL` in all
printed cases); the arguments of Theorem 3(a),(b), Proposition 5′(a) and Proposition 8(c)
re-derived by hand.  Everything else of the report was read, not re-derived.  The
measurements quoted in §4 are workstream P's (`PHYSICAL_APPLICABILITY.md` §8 for their
replication status).

*Version 2.*  §4b quotes findings S39, S43, S44, S48, S49, S50 of
`docs/collaboration/status/science.md`, where the status and the checks of each are
listed (P2: one end-to-end check re-run by the coordinator; P3: four statements
re-derived, three runs re-run, the twenty-residue value replicated with other code;
A17 (6)–(11): the coordinator's own scripts, not replicated by anyone else).  The prior
art of row D is in SCI-RES-0009 (workstream A3): its cost table and its inequality are
in print and are not ours.  §5b: `workstreams/R10_REPORT.md` with the coordinator's
note at its end.
