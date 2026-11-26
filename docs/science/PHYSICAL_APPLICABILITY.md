# Physical applicability: what the mathematics says about molecules, and what it does not

*Science division.  Version 1 (2026-11-25).  A synthesis for a reader who has not followed
the session.  Sources: workstream P (`workstreams/SP_REPORT.md`, a pilot on a real force
field; two of its numbers re-computed by the coordinator, see §8), workstream K
(`workstreams/SK_REPORT.md`, kinetics; its Lean file re-compiled and three scripts re-run by
the coordinator), workstream A2 (`workstreams/A2_REPORT.md`), `INFERENCE_LIMITS.md` and its
addenda, and the theory report at `89ac710`.  Labels as in `SCIENCE_TO_ALL.md`; **[M]** =
measured on a named model with a stated protocol.  Units: kcal/mol; `k_BT = 0.596 kcal/mol`
at 300 K.*

## 0. Verdict

1. **The mathematics is about models, never about molecules.**  A certificate proves a
   statement about an energy function on a discretised conformation space.  Every input —
   tables, class constants, anchor values — is a modelling statement, and none of the
   constants the theory needs has ever been *certified* for a production force field,
   except for corrections with an explicit low-dimensional form (torsion refits).
2. **Which class a real residual lives in — measured for the first time in this programme
   [M].**  On capped alanine peptides with Amber ff14SB as known part:
   * a difference between force fields of one lineage is **exactly** in the cheapest
     classes (ff99SB − ff14SB: a sum of single-torsion terms, range `1.115 kcal/mol`;
     ff19SB − ff14SB: one table per residue);
   * a change of charge model (ff03, ff15ipq) is a first-order class with `βc ≈ 2–10`;
   * an implicit-solvent polarisation energy (GBn2) is **not near any per-torsion
     class**: constants of `12–53 k_BT`, growing with chain length, dense second-order
     couplings of the same size, no sharp site in any enumerated instance — and it is
     near the pair-additive ("profile") class only in root mean square
     (`0.2–0.9 k_BT`), not in supremum norm (`2–16 k_BT` from three residues on).
   **In residue-rotamer variables on a fixed backbone the picture changes (workstream
   P2, checkpoint 31) [M]:** the known part is *exactly* pairwise; the solvent term is
   pairwise up to third-order constants of `0.003–0.2 kcal/mol` for neutral side chains;
   the second-order interface certifies the minimum exactly, with tens of evaluations,
   for apolar side chains and fails for polar and charged ones because the *pair* part
   of the residual is large; the third-order interface (values on a Hamming ball of
   radius 2) certifies every enumerated instance.  First-order constants saturate for
   neutral side chains and grow for charged ones (§2a).  *Qualification (workstream P4,
   SCI-REV-0012 §5):* "certifies" is on the domain the theorems were applied to — for
   valine, leucine and serine the whole clash-free product; for phenylalanine, lysine
   and the patterned sequence a pruned sub-product which in 14 of 40 analyses does not
   contain the minimum of the clash-free domain (phenylalanine on the strand: lower by
   2–13 kcal/mol).  With the true minimiser as reference and the largest reset-closed
   domain around it the star certifies 13 of those 40 and the third-order pair model
   30 of 34.
   **And the constants can be certified, at a price (workstream P3, checkpoint 40)
   [P + M]:** by analysis alone — tables and interval enclosures, no evaluation of the
   solvent term — only with a loss of a factor 33–1 400, because the bound cannot see
   the cancellation between self and cross terms of a neutral molecule; by evaluating
   the solvent term on a Hamming ball about an anchor and bounding only the tail beyond
   it, to the point where **the free energy of a twenty-residue apolar peptide on an
   extended backbone (`3.5·10⁹` rotamer assignments) is bracketed within 0.06 nats with
   no sampling and within 0.005 with** — the first certified free energy of this
   programme at a size beyond enumeration, replicated by an independent estimate.  Not
   on the helix, and not for charged side chains (§2b).
3. **The exponents of the query-complexity theory are evaluated at `βc ∼ 1`; nothing
   measured is there.**  For the solvent term the theory is in its zero-temperature regime
   and says, correctly but uninformatively, "evaluate a fixed fraction of everything"
   (at least 19, 12 and 11 % of the conformations at 3, 4 and 5 residues, measured).  For same-lineage refits it
   says "one to three evaluations".  The regime in which exponents discriminate
   (`βc` between about 0.5 and 3) is occupied, in the pilot, only by torsion refits.
   **And the exponents are those of independent sites: with a cooperative known part
   they move in a direction that depends on the envelope (workstream R10, checkpoint
   43) [P + N, one two-state chain]:** below about one `k_BT` per site all three rise, at
   small envelopes by the structure factor at zero wave vector; at several `k_BT` per
   site the two cost exponents fall below the independent-site values and only the
   threshold stays raised (§3a).  The discriminating regime straddles the crossover, so
   no single direction may be quoted for it.
4. **The class is expensive, not the function.**  The actual solvent residual has a Jensen
   gap of 2–3 nats where its own first-order class allows 71–178.  Worst-case class
   statements are, for this residual, pessimistic by two orders of magnitude.  This is the
   strongest empirical argument for models of ignorance that are not worst-case
   (`OPEN_PROBLEMS.md` D2) and for classes with known features and a bounded remainder.
5. **Three statements could meet an experiment**, each falsifiable and each still to be
   carried out on a physical system: a certified lower bound on a rotational barrier
   (against dynamic NMR); a certified range and a certified lower bound on model error
   from ensemble-averaged data (against NMR or scattering averages); and the profile class
   as the natural class of scattering data (Debye intensities are in it with constant
   `q²/6`).  §5.

## 1. The dictionary

| mathematical object | physical counterpart | valid when | what is lost | what must be measured or certified |
|---|---|---|---|---|
| finite product space `∏ D_i` | rotamers on a fixed backbone; torsion wells; voxels of torsion space; lattice walks | each state is a cell on which the energy can be enclosed, cells are products over sites, hard degrees of freedom rigid or integrated out | vibrational entropy inside a cell; bond-angle flexibility; kinetics; the product structure itself (41 % of the three-state grid of the hexapeptide is clash-free) [M] | interval enclosures of every energy term over every cell; they widen with the lever arm |
| known part, pairwise in sites | a molecular-mechanics energy **on a fixed backbone**: each atom moves with one site | fixed backbone, no many-body terms | for a flexible backbone nothing is pairwise in torsions: vacuum ff14SB has mixed differences up to 28 kcal/mol (12 at separation seven) [M] | tables with outward rounding; a statement of which terms were moved into the residual |
| residual `g` | continuum-solvent polarisation; explicit polarisation; quantum minus classical energy; a learned correction; the difference of two force fields | the split is a choice: `g` is the expensive, non-decomposable or uncertain part | all structure of the functional form, unless it is put into the class | which class, with which constants (§2) |
| envelope constants `c_i`, `c_ij`, slope `L` | an a-priori worst-case bound on the change of the correction when one degree of freedom changes: a **sup-norm** error bar | it holds for all pairs of configurations of the domain | typicality: force-field accuracy is quoted in RMS; sup/RMS is 4–8 in the pilot [M] | an *upper* bound — interval arithmetic or a proved Lipschitz property.  None exists for a production force field; a constant fitted on a sample is not a bound (held-out maxima up to ten times the fitted ones [M]) |
| anchor `(a, g(a))` | a single-point evaluation of the expensive model.  **No experiment measures `g` at a chosen conformation** | the evaluation is exact, or comes with an interval | convergence error of the expensive calculation | the number of anchors is the theory's cost |
| `min E` | the global minimum of the model | it predicts a structure only if its basin dominates and the model error is below the gap to competing basins | for a flexible peptide helix, β and PPII lie within 0.4–2.7 kcal/mol and a torsion refit of 0.64 kcal/mol per residue reorders them [M] | gaps against constants, by droplets rather than by sites |
| `ln Z` | **observable** only in differences: between macrostates of one model, between thermodynamic states, gas phase → solvent (a hydration free energy).  The absolute `ln Z` of a discretised model and `ln Z(f+g) − ln Z(f)` for a model correction are not observable | — | in a first-order class correlated errors do not cancel in differences (theory report §11.13) | the accuracy that matters is about `1.7 k_BT` on differences; the class threshold measured for the solvent term is 43–48 nats per residue [M] |
| `u = βc` | `1 kcal/mol = 1.68 k_BT` at 300 K | — | — | measured: 12–53 (solvent), 2–10 (charge models), 1.1–4.3 (one lineage) [M] |
| hint | a cheaper surrogate of the residual which expensive evaluations spot-check | the surrogate is free; correctness is demanded on the class | — | a fitted typed-pair model predicts the solvent term to 0.26 kcal/mol RMS (max 2.2) [M]: a good hint; the price of checking it is set by the class |
| product landscape, the cube | independent degrees of freedom: far-apart side chains, independent rotors, titration sites | couplings small against site gaps | cooperativity, excluded volume.  In the helix basin of the hexapeptide 8 of 12 torsions have no clash-free single flip, and the collective move to PPII costs 0.37 kcal/mol in all [M] | the exponents are properties of this idealisation |
| profile class (pair-distance features) | a pair-additive energy with unknown radial functions; **the pair-distance distribution measured by small-angle scattering** (Debye intensities are in the class with constant `q²/6`, A2.1 [P]) | typed pairs; distance-dependent slope bounds | one pair type explains nothing of an electrostatic residual (remainder = total variance) [M]; chains are not identifiable from complete distance distributions (homometric pairs from 6 beads; 19 % of 9-bead site sets on the cubic lattice, A2 [N]) | a sup-norm remainder, *bounded*, not sampled |
| evaluations of `g`; averaged observables; mean residual energy (our I1, I2, I3) | single-point calculations; NMR/scattering/FRET averages; calorimetry | I2: the forward model of the observable is known and exact | forward-model error; in the worst case of a first-order class averaged data of bounded order — and of every order at fixed absolute precision — are worth a polynomial factor only (Theorems 4, 4′, 4-τ) | error bars as *tolerances* (addenda A10) |
| identified set; extent of falsification | the range of a quantity over all ensembles (or all class members) consistent with the data; the least model error the data force | exact linear programmes on enumerable systems | — | the dual certificate; see §5 |
| barrier `B(a,b)`; trap survival | a potential-energy barrier of the model; non-equilibration of a *sampler* | on the voxel **face-adjacency** graph (K8 [P]); for every dynamics stationary for the Gibbs measure and local on the graph (K10 [V]) | physical rates: the kinetic prefactor is not in the programme; the discrete Metropolis rate is not a physical rate | wall and basin partition functions; the envelope enters as `exp(β·d(basin, wall))` |
| certificate, kernel | a proof-carrying computation about the model | always | it certifies nothing about nature | the inputs |

The full table with one more column and five more rows is in `SP_REPORT.md` §2.B.

## 2. Which class do real residuals live in?  [M]

Protocol (all of it in `SP_REPORT.md` §3.1): Ace-(Ala)ₙ-NMe; rigid bond lengths and angles;
backbone torsions on a three-state grid per torsion (`n ≤ 6`, 531 441 conformations) or a
two-state grid (`n ≤ 9`); conformations with steric clashes removed; energies from OpenMM
8.6.1 parameter files; exact enumeration.  **Every constant below is an exact maximum over
a finite grid, hence a lower bound for the continuous conformation space and not an upper
bound for anything.**

| residual (known part: ff14SB vacuum) | first-order constants `c_i` | second order | best cheap class | certificate of the minimum, 5 residues (28 843 conf.) |
|---|---|---|---|---|
| ff99SB − ff14SB | 0.64 on φ, 0 on ψ, for every length (1.115 on the full circle) | exactly 0 | sum of single-φ terms, **exact** [P] | 1 evaluation |
| ff19SB − ff14SB | 1.5 (φ), 2.6 (ψ), for every length (3.7, 4.4 on the clash-free continuous map) | 2.5 inside a residue, exactly 0 otherwise | one table per residue, **exact** [P] | 2–3 |
| ff03 − ff14SB, ff15ipq − ff14SB | 2.6–6.1, slowly growing | neither sparse nor large (3.9 → 0.7 over seven torsions) | residue pairs: RMS 0.12, max 1.4 | 2–28 |
| GBn2 polarisation energy | **9.0, 14.0, 18.6, 22.9, 27.5, 31.6** for `n = 1…6` (three-state grid: `≈ 4.8 + 4.5n`); 3.7 → 19.0 for `n = 1…9` on the two-state grid, sub-linear | dense; entries up to 29; half row sums 52–89 | torsion pairs: RMS 2.1, max 13.  Typed atom pairs (36 types): RMS 0.26, max 2.2 (held out).  An explicit exactly pair-additive surrogate: RMS 0.10 → 0.52, max 0.5 → 9.3 for `n = 2 → 8` | between 3 042 and 5 357 |

Further facts of the pilot that a reader should not miss:

* The **typical** single-flip change of the solvent term does not grow with length
  (6.5 kcal/mol RMS); the growth is in the extreme pairs, i.e. in exactly what a sup-norm
  envelope must cover.
* The lever-arm prediction of the theory report (§11.14) is confirmed as growth with chain
  length, not as a law in the distance to the nearer chain end.
* Restricting the domain lowers the constants (within 20 kcal/mol of the minimum of the
  known part the largest solvent constant is 14.6 instead of 27.5) — but the envelope is
  needed to justify the restriction that would make the envelope small.
* Freezing the Born radii ("pairwise GB") is useless (RMS 5 kcal/mol); the first-order
  response in the radii, which is itself pair-additive, repairs it.  The structure
  `g = (explicit pair sum) + (explicit linear term) + (remainder quadratic in the
  Born-radius fluctuations)` suggests a class with **known features and an analytic
  remainder bound** — the most promising route to a certified envelope for a real
  many-body term (`SP_REPORT.md` §6, item 2).

## 3. What the theory's formulas give with the measured numbers (model-relative)

Product landscape with the measured single-site numbers; constants extrapolated in three
ways (`SP_REPORT.md`, Statement 7):

| chain | sharp sites | uncertifiable free-energy width `Σ ln cosh(βc_i/2)` | lower bound on the certificate of the minimum |
|---|---|---|---|
| 10 residues | 0 of 20 | 430–480 nats | `≥ 10⁵` of `10^{9.5}` conformations |
| 100 residues | 0 of 200 | `4.6·10³ – 3.1·10⁴` nats | `≥ 10^{56} – 10^{74}` |

These say what a certifier that knows only per-torsion constants must pay.  They are not
statements about the peptide: on the enumerated instances the exact Jensen gap of the
solvent term is 2.1–2.6 nats where the class allows 71–178.

## 4. Resolution statements and algorithmic statements

*Resolution statements* — what any user of the model can conclude from class membership,
whatever they compute: the sharp-minimum and contact theorems; thermal contact; the exact
free-energy sandwich; the theorem that Boltzmann averages are uncertain over most of their
range; every lower bound on the number of evaluations; on the measurement side, identified
sets and the theorems on what averaged data cannot add; in kinetics, the exact robust
interval of a barrier height (K6).  *Algorithmic statements*: the kernels, learn-then-cover,
the nested samplers, the cut and rate certificates.

The measured numbers speak to the first kind: for the solvent residual no torsion is sharp
in any enumerated instance, and the collective criterion fails by factors of 26 to 380
(`λ* = 0.038 … 0.0026` for two to six residues, where one evaluation would need `λ* ≥ 1`).

## 5. Three statements that could meet an experiment

| statement | what would be computed | what would be compared | how it could fail | state |
|---|---|---|---|---|
| **A certified relaxed torsion scan** (K2(b) with K8): "for this force field every pathway that takes torsion `i` from conformer `a` to conformer `b` crosses potential energy at least `L` above `a`" | interval tables on torsion voxels with nearest-voxel adjacency; `k` certified wall minimisations | a measured activation energy or exchange rate of a hindered rotation (dynamic NMR) | a measured barrier *below* the certified lower bound — after the entropic and kinetic prefactors are accounted for — falsifies the energy model, independently of any sampling | proposal; no physical system treated; the real obstacle is that the energy is not pairwise in torsions |
| **A certified range and a certified lower bound on model error** from averaged data (`INFERENCE_LIMITS.md` §8, §9) | the identified interval of a structural quantity over the model's envelope class given the data, with a dual certificate; the least envelope constant consistent with the data | NMR or scattering averages of a fixed-sequence system with a public ensemble | an empty identified set at the assumed constant is a certified falsification of (model + class); sampling cannot change it | exact on lattice chains to 10 beads; on a physical instance not done; the model-free and divergence-ball versions are known methods (maximum occurrence; Christensen–Connault) |
| **The profile class is the class of scattering data** (A2.1) | Debye intensities as linear functionals of the pair-distance profile, constant `q²/6` | a scattering curve on a finite grid of `q` | — (a statement of structure, not a prediction); its limits are homometric chains | proved; identified sets from scattering curves computed to 15 beads |

Also observable in principle and untouched: hydration free energies (`ln Z(f+g) − ln Z(f)`
with `f` the gas-phase energy and `g` a solvation potential of mean force).

**A fourth, added at checkpoint 23: robust ranges of observable free-energy differences**
(addenda A11, A13, A14; SCI-MSG-0009).  For binary (or ordered) sites, a known part without
frustration and macrostates monotone in the site variables, the range of a population
ratio over the *whole* envelope class is attained at two uniform fields and is computed by
ordinary partition functions; uncertainty common to both macrostates cancels.  Worked on
a classical helix–coil chain (`σ = 10⁻³`; a model, no molecule): a per-residue uncertainty of
`0.1 k_BT` leaves the helix content of a 50-residue chain near the transition undetermined
between 0.05 and 0.61, and the log odds of one residue's state uncertain by `2c` times a
cooperative length of 5–25 residues — neither `2c` nor `2cn`.  *How it could meet an
experiment:* helix contents and their temperature dependence are measured (circular
dichroism); a model with stated per-residue uncertainty either brackets the measurement
or is falsified by it, whatever non-additive form its error has.  Not done.

**What the measurement-side theorems of checkpoints 26–30 say, in physical terms [H —
readings of theorems about an idealised class; none has met a measurement].**

1. *Calorimetry turns a free-energy problem into an entropy problem* (addendum A16).
   With a mean energy known, `ln Z = S − βU`, and a bound on how much one local change can
   alter the energy bounds how ordered the ensemble can be.  Reading: a thermodynamic
   datum fixes the free energy up to an entropy uncertainty that is set by the class
   alone — per site, the relative entropy between a fair coin and a coin biased by one
   envelope constant.  For weak residuals (`βc ≲ 1`) that is about `(βc)²/8` per site and the
   datum adds almost nothing to what cheap sampling already gives; for strong ones it is
   decisive.  **Caveat that matters physically:** the theorem's datum is the mean
   *residual* energy `E_μ g`, which no instrument measures; the measurable mean energy is
   that of the whole system including solvent and momenta.  With a known part that has
   interactions the entropy bound is not available in this form (not proved).
2. *A hidden state compatible with a calorimetric datum must be as deep as the visible
   one and exponentially wider* (A16, plateau twin).  Reading: calorimetry cannot exclude
   a second basin of the same depth (already in §5 of the note), and what it does
   exclude at coarse accuracy are *narrow deep* hidden states; the hidden states that
   survive are broad, hence easier to find by search — in the model, by a computable
   factor.
3. *Local averages with a bias do not rescue the worst case, and do help at the model
   one believes in* (workstream F; theory report §11.29).  With a field, exact one-body
   averages leave both class exponents unchanged: there is an ensemble — a mixture of
   two product ensembles — whose one-body averages equal those of the same ensemble with
   a hidden state added.  At the unperturbed model, however, the same averages exclude
   part of the hidden states: the cost exponent falls by at least 2–17 % in a weak field
   (`p = 0.3`, `u = 1`) and by at least 21–100 % in a strong one (`p = 0.1`, `u = 2`), and to
   zero in a window of accuracies.  Reading: order parameters and chemical-shift-like
   one-site averages are informative *relative to a trusted model* (how much depends on
   the strength of the field) and uninformative as
   a guarantee over a class — the instance-wise statement is the meaningful one, as the
   theory division also concludes.
4. *The uncertainty of an observable free-energy difference is a transport problem*
   (theory report §11.28; our A11, A13).  The largest shift of the free-energy difference
   between two macrostates that a class of model errors allows is attained by moving
   weight from one macrostate to the other along the cheapest routes of the envelope;
   for a threshold of an order parameter the extremal error is a uniform field.  This is
   the quantity an alchemical or conformational free-energy calculation should quote as
   its model-error bar, and it is computable with ordinary partition functions in the
   monotone case.

## 6. What must not be claimed

* That a certified minimum is a predicted structure.
* That a class constant measured on a grid, or fitted on a sample, is a bound.
* That exponents computed at `βc ∼ 1` describe the cost for a solvent or quantum residual.
* That "GB is nearly pair-additive" in the sense certificates need (it is so in RMS).
* That a certified discrete rate bounds an experimental rate, or that a barrier certified
  on the Hamming graph of rotamer labels is a barrier of the molecule.
* That low-order agreement with averaged data establishes order or disorder (Theorem 2),
  or that a profile match establishes a structure (homometry).
* That a calorimetric measurement supplies the datum of addendum A16 (it supplies the
  mean energy of everything, not the mean residual energy of a model).
* That "local data are worthless" — the theorem is about the worst member of a class;
  at a trusted model they exclude a part of the hidden states that is small in a weak
  field and large in a strong one (workstream F).
* That "interactions make certification harder", or that "the product-measure exponents
  are optimistic for real chains", without the range of the envelope: in the one
  interacting model worked out it is true for the threshold at every slope and for the
  cost exponents up to about one `k_BT` per site, and false for the cost exponents at
  several `k_BT` per site (§3a).  Nor that the small-slope factor is "the
  susceptibility": it is the largest variance of a Lipschitz function, which is the
  zero-wave-vector susceptibility only for ferromagnetic (associated) chains.
* That anything here has been compared with a measurement.  Nothing has.

## 7. Under which physical assumptions do the exponential lower bounds stop applying?

They are theorems about first-order classes, in which an evaluation informs about a
neighbourhood only.  They stop applying when the class is finite-dimensional in *known*
features with a small sup-norm remainder (theory report Theorem 11.47).  Assumptions that
give this, and the pilot's verdict on each [M]:

| assumption | ff99SB − ff14SB | ff19SB − ff14SB | charge models | GBn2 |
|---|---|---|---|---|
| low order in torsions | exact, order 1 | exact, order 2 in a residue | approximately | no |
| typed pair-additivity in atoms | yes | not tested | RMS 0.11, max 1.3 | RMS yes, sup norm no |
| locality along the chain | yes | yes | no | no |
| weak coupling, `Σ_j tanh(βc_ij/4) < 1` | 0 | 0.78 | 4.1 | 7.0 |

Smoothness alone does not help (the torus bound of theory report Theorem 11.34 is
exponential).  A bound in a typical norm — `L²` or an exponential moment under the Gibbs
measure of the known part — would, for `ln Z`, replace the sup-norm floor by the typical
remainder; whether such a bound can be *certified* is the question put to the theory
division as T-3 of SCI-RES-0002.

**Answered in principle at checkpoint 34 (the theory division's box-class result,
THY-RES-0007 §4, and our addendum A17) — and the sentence above was too hopeful about
`L²`.**  What certifies `ln Z` by sampling from the known part is an a-priori bound on a
divergence of the *true ensemble from the model*: a pointwise floor of the remainder
(cost `e^{floor}/ε` with a hint), a Rényi divergence of order `p > 1` (`e^{κ}/ε^{p/(p−1)}`; at
`p = 2` a chi-square bound, `(1 + χ²)/ε²`), or a Kullback–Leibler divergence (`e^{Θ(κ/ε)}`).  **An
`L²` bound on the remainder energy — the root-mean-square error that every fit reports —
certifies nothing**: a budget of `0.1 k_BT` allows an undetected dip of `100 k_BT` on a state
of probability `10⁻⁶`.  The physical reading [H]: a fitted surrogate is certified by
knowing that *the truth has no basin the surrogate misses*, in an exponential-moment
sense; knowing that the surrogate is accurate where *it* puts its weight (which is what
a variational fit optimises and what a test set drawn from the surrogate measures) is
the cheap half and is not enough.  For the one real remainder measured against a
pair-additive class (GBn2, backbone torsions) the needed floor grows from `0.8` to
`15.6 k_BT` between two and eight residues — "independent of the size of the system" is
a statement about the theorem's coordinate, not about that remainder.  Whether a floor
can be *proved* for the solvent term in rotamer variables, where the many-body part is
small, is workstream P3.

**The prices, measured in rotamer variables [M; checkpoint 36; addendum A17 (6)].**  On 45
enumerated instances of P2 (valine, leucine, serine homopeptides; 2–12 residues; three
backbones) with the vacuum force field as the model and the GBn2 term as remainder:
for the apolar side chains the solvated ensemble is within `D_2 ≤ 0.7`, `D_∞ ≤ 4.6` nats of
the vacuum ensemble although the solvent term varies by `11–12 k_BT` over the grid — its
minimum sits where the vacuum model already has its weight; for serine `D_2 = 3–45` and
`D_∞ = 10–56`, growing by several nats per residue; with the pairwise fit of the solvent
term `D_∞ ≤ 0.22` everywhere.  Physical reading [H]: adding implicit solvent to an apolar
side-chain ensemble on a fixed backbone is a *small* change of the ensemble in the
sense that matters for certification, and a large one for a hydroxyl group (whose
solvation depends on which way it points and on its neighbours); the pair terms carry
almost all of it.  The root-mean-square error of the surrogate does not show any of
this (it *falls* with chain length for serine on the helix while the certified cost
rises by thirteen orders of magnitude).  **These are prices computed by enumeration,
not certificates**; exposed model peptides, ideal backbones, no charged side chains.

**From prices to a certificate [P + M; checkpoint 40; workstream P3, SCI-MSG-0020; §2b].**
The assumption under which the exponential bill disappears *and can be checked* is now
explicit for one family: the solvent term of an apolar side-chain ensemble on an
extended backbone is, up to a remainder with a certified pointwise bound that is small
near the anchor, a banded pairwise function whose low orders are *evaluated*.  The
certificate costs `Σ_{j<m} C(n,j)(k−1)^j` evaluations (polynomial in the length at fixed
order `m`) plus a transfer matrix.  Where the assumption fails — a helix, where every
side chain has many neighbours within the range of the solvent kernel; charged groups —
the certified remainder decays too slowly with the order and nothing is certified at
affordable cost.  Physical reading [H]: what makes a solvated side-chain ensemble
certifiable is not that the solvent term is small or smooth but that its *many-body*
part is short-ranged along the chain; compactness is what breaks it.

## 8. Provenance, replication, limitations

* **Replicated by the coordinator (same machine, the workstream's scripts):** the
  tripeptide constants `16.09 12.41 18.63 16.43 15.14 11.19` and 508 clash-free
  conformations from OpenMM's own force objects (`verify_openmm_direct.py`); the range
  1.1147 kcal/mol of ff99SB − ff14SB along φ and its independence of ψ
  (`an9_torsion_refits.py`).  Not independently replicated: everything else of the pilot.
  This is a re-run, not a second implementation.
* **Kinetics:** `KineticsCertificates.lean` re-compiled (32 theorems, standard axioms, no
  `sorry`); scripts T1, T3, T9 re-run with identical output.  Wrochna's theorem and the
  Edmonds–Fulkerson reference checked at the level of bibliographic record and abstract by
  the coordinator; read in full (pp. 1–8, 299–301) by the workstream.
### 2b. A floor by analysis, and a certified free energy beyond enumeration  [P + M; workstream P3, `workstreams/P3_REPORT.md`; SCI-MSG-0020]

*(Placed before §2a in the file for historical reasons; read §2a first.)*

Question (the theory division's, THY-RES-0007 §4.2): can the constants that P2 measured
by enumeration be *proved*?  Same model and protocol as §2a.

| route | what it certifies | verdict |
|---|---|---|
| analysis alone: tables, ranges, interval enclosures of the derivatives of the Born-radius rescaling and of the kernel; no value of the solvent term | third-order constants 33–1 400 times the measured ones (valine, leucine 200–1 400; serine 40–100; lysine 33–77) | rigorous and useless beyond serine on a strand.  **The loss is cancellation, not slack:** term by term the bound is within 1.1–6 of exact; summed over the atom pairs of a neutral molecule it is two to three orders too large (Val₆: self part −640, cross part +600, total −37 kcal/mol) |
| evaluate the solvent term on the Hamming ball of radius `m − 1` about an anchor; bound only the tail of order `m` in closed form over all subsets | a sandwich `m₋ ≤ E ≤ m₊` of banded pairwise models with exact partition functions and samplers; certified remainder constants falling by 21–51 per order (valine), 11–22 (leucine) on strand and PPII | **works on extended backbones**: Ace-Val₂₀-NMe on PPII, `3.49·10⁹` assignments — `ln Z ∈ [518.2332, 518.2937]` from 87 441 evaluations with no sampling; `[518.2598, 518.2648]` with 50 000 samples; the minimum certified.  In 160 enumerated runs (5.5 million state checks) the sandwich was never violated |
| the same on the helix | constants falling by 5–8 per order (Leu₁₆: 1 819, 370, 60, 8.0 kcal/mol at orders 3–6) | **fails at every affordable order** |
| the floor as a function (site penalties) against a constant | cost number `Z(m₋)/Z(E) − 1`: Val₁₀/strand 6.3 → 0.022; Lys₄/helix 3.2 → 0.48 | the theory division's cost formula holds on real numbers, and *the certificate must be a function, not a constant* |
| inputs of the floor-plus-variance bracket (addendum A17 (7)) from the sandwich | `b ≤ 𝔼u`, `Var ≤ 𝔼u²`, `u = β(m₊ − m₋)`, exact by transfer matrix: at twenty residues `0.061 k_BT`, `4.8·10⁻³`, `W = 2.4·10⁻³` nats | certified without sampling; 4–26 times the true gap on enumerated instances |

What "certified" means: paper proofs checked against enumeration, interval arithmetic
for every derivative bound, a stated floating-point allowance; **not machine-checked,
code not reviewed**.  Replication: the coordinator re-derived the combinatorial
statements, re-ran one enumerated instance and the evaluator's validation against
OpenMM, and measured the twenty-residue value independently with a chain model built
with other code (`518.2618 ± 0.0007` at first order; addendum A17 (10)).  Model-relative
throughout; exposed rigid peptides on ideal backbones; one large instance.  The neck
correction of GBn2 is what makes its constants large (10–70 times smaller without it);
OBC2's are 2–8 times smaller for apolar side chains.

### 2a. The same residual in rotamer variables on a fixed backbone  [M; workstream P2, `workstreams/P2_REPORT.md`; SCI-MSG-0015]

Protocol: capped homopolymers of Val, Leu, Phe, Ser, Lys and one patterned heteropolymer
on ideal helix, strand and PPII backbones; one site per residue, the rotamer (three
states per side-chain dihedral) as site variable; rigid ideal geometry; clash filter;
exact enumeration (140 models, 8.5·10⁶ assignments).  Exact maxima over finite sets, lower
bounds for anything larger.

| quantity | backbone torsions (§2) | residue rotamers, fixed backbone |
|---|---|---|
| known part pairwise in the sites? | no (`c_ij(f)` up to 28 kcal/mol) | **yes, exactly** with one site per residue; not with one site per χ |
| `max c_i` of the GBn2 term | 9 → 32 kcal/mol for 1…6 residues | neutral: saturates (Val 0.4–0.8, Leu 1.0–1.6, Phe 1.6–4.5, Ser 5.0–9.4 by backbone); charged: grows (poly-Lys 10, 37, 52, 56; ≥ 138 at 24 residues) |
| `c_ij`; half row sums against excitation energies | up to 29; 52–89 | Val, Leu 0.1–0.5; Ser 2.1–3.0 (row sums 3.5–4.9 against 0.13–1.0); Lys–Lys 18–51; Lys–Glu 78 |
| `c_ijk`; best two-site fit | RMS 2.1, max 13 | neutral 0.003–0.2 (fit max 0.002–0.2); charged up to 2.4 (10.2 at a relaxed clash threshold) |
| second-order interface (star, exact criterion) | condition fails by 1–2 orders | exact certificate for apolar side chains (25 evaluations of 531 441; 17 of 65 536); fails for polar and charged ones from three residues on |
| third-order interface (ball of radius 2) | — | exact certificate in every instance at the pilot's clash threshold (1 009 of 531 441 for Ser₆) |
| Jensen gap against the class bound | 2.3 against 178 nats | 0.99 against 20 (Ser₆); 4.6 against 146 (Lys₄) |

What a reader should not miss.  (1) **The solvent term is not far from pairwise in these
variables; what defeats the second-order interface is the size of its pair part** — the
screening cross terms that nearly cancel the vacuum Coulomb term of the known part.
Moving a pairwise term between known part and residual changes the first- and
second-order constants and leaves the third-order ones unchanged: the cost of the star
depends on the split, that of the ball does not.  (2) **Our prediction that the constants
would be bounded by the solvation of one side chain is true for neutral side chains and
false for charged ones** (an unscreened long-range charge–charge term stays in the
residual).  (3) Every certificate is conditional on constants that were obtained by
enumerating the whole domain; nobody has an a-priori bound on `c_ij` or `c_ijk` of a
generalized-Born term.  The measurement shows such bounds would not be vacuous.
(4) **No buried environment was measured**; there the third-order constants must be
expected to be larger — the literature reports that pairwise treatments of GB lose
accuracy when all side chains of a folded protein move together (abstracts only; the
report's §4).  That is the next measurement (request P2-E1).

* **Limitations of the pilot:** alanine only; rigid geometry (58 % of the dipeptide map is
  a clash); grids of basins; exact only to six and nine residues; one clash threshold with
  a sensitivity check (constants move by up to 15 %); the prior-art search is six PubMed
  abstract queries; no side chains, no Poisson–Boltzmann, quantum or learned residual; no
  certificate in the span format was run.
* ~~**The decisive missing measurement** is the same constants where the theory's known part
  exists: rotamer variables on a fixed backbone~~ — **made (workstream P2; §2a)**.  The
  decisive missing measurement is now the same third-order constants in a **buried**
  environment (request P2-E1 of SCI-MSG-0015), and the missing theorem an a-priori bound
  on them.

### 3a. A cooperative known part: optimistic below one `k_BT` per site, pessimistic above several  [P + N; the theory division's workstream Y at `658b77f`, reviewed and replicated by our workstream R10, `workstreams/R10_REPORT.md`; SCI-REV-0010]

*The model, and nothing more than the model.*  A two-state chain with a
nearest-neighbour coupling `K = ln((1−p)/p)` in units of `k_BT` and no field (neighbours
differ with probability `p`; correlation length `−1/ln(1−2p)`: `1.1`, `2.0`, `4.5` sites at
`p = 0.3, 0.2, 0.1`), and a residual of which only an envelope is known: one flip changes
it by at most `u` (in `k_BT`).  "Cost" is the number of evaluations of the residual needed
to certify `ln Z` to an accuracy proportional to the length; `E` is the accuracy below
which the cost is exponential, `h` and `a` the exponents of the adaptive and
non-adaptive cost.  The comparison is with independent sites of the same one-site
marginals and the same envelope ("the cube").  No observable occurs and nothing is
fitted to a molecule.

| regime | what is established | status |
|---|---|---|
| `u = 1`, `p ∈ {0.4, 0.3, 0.2, 0.1}` | all three exponents **above** the cube's (at `p = 0.3`: `h` +38 % to +54 %, `a` +15 % to +26 %, `E × 1.93`) | the theory division's result; proofs re-derived and every bracket recomputed with our own code (lower ends: every algorithm, every length; upper ends and the reading of `h`, `a` as exponents of algorithms: given theorems of the theory report that R10 did not re-derive) |
| small envelopes, `u·S(0) ≲ 1` | the three exponents are, to second order in `u`, those of independent sites times **the structure factor at zero wave vector**, `S(0) = (1−p)/p` — in general: times the largest variance per site of a Lipschitz function, which is `S(0)` exactly when the chain is ferromagnetic (associated) and is the dominant collective mode otherwise | **[P]** at fixed length (Propositions R10.1, R10.2; checked over all vertices to five sites); for the infinite chain the upper side is proved, the lower side is a sketch; "the susceptibility" is **false in general** (exact counter-examples: antiferromagnetic and frustrated chains) |
| large envelopes: `u = 3, 4, 6` (`p = 0.3, 0.2, 0.1`), `u = 2.5` (`p = 0.2, 0.1`), `u = 2` (`p = 0.1`) | the non-adaptive exponent `a` is **below** the cube's (by 1–16 %); at `u = 4, 6` and `p = 0.2, 0.1` so is `h` (by 1–8 %) | **[P]** given the theory division's Proposition F (a martingale recursion, re-derived by R10), evaluated with duality brackets; recomputed with the theory division's own functions (by R10 and by the coordinator) and with a third code on exact finite chains (`pi_inference/r10_reversal_check.py`) |
| every slope | the threshold `E` is **above** the cube's (`E ≥ E_F > ln cosh(u/2)`, closed form; factor `2.19 … 1.15` for `u = 0.5 … 6` at `p = 0.3`) | [P] |
| between (`a` for `1.5 ≤ u ≤ 2.5` at `p ≥ 0.3`; `h` for `2.5 ≤ u ≤ 3`); strong coupling `p ≤ 0.01` | undecided | — |

*Reading [H].*  Below about one `k_BT` per site the cheapest way for an unknown residual
to move `ln Z` is a perturbation the chain answers collectively — a field over a domain —
and cooperativity multiplies its effect: the independent-site exponents are
**optimistic**, by a factor that is the size of the cooperative unit.  At several `k_BT`
per site the residual can make a single configuration dominant, certification becomes
a search among the configurations that could have been made dominant, and the coupling
removes candidates (a pinned configuration with isolated spins leaks `e^{2K}` times
more): the independent-site values of `a` and `h` are **pessimistic**.  The threshold does
not reverse because it is governed by the cooperative perturbation at every slope.

*Helix–coil chains (Zimm–Bragg weights `s`, `σ`; second order in `u`)  [P at fixed length and second order; numbers
**[M]**, exact transfer matrices checked by enumeration, `experiments/science/pi_inference/helix_coil_structure_factor.py`].*
The Zimm–Bragg measure is associated (its pair weights have determinant `s(1 − σ) > 0`), so by
Propositions R10.1–R10.2 the game function of an `n`-residue chain is, to second order
in the single-residue envelope `u`, `(t(1−t)/2)·u²·Var(N_h)` with `N_h` the number of helical
residues: `E_n, a_n ≈ u²Var(N_h)/2`, `h_n ≈ u²Var(N_h)/8`.  Relative to independent residues
with the same one-residue helix probabilities the factor is `S_n = Var(N_h)/Σθ_i(1−θ_i)`;
for the infinite chain

    S_∞(s, σ) = (1 + s)/√((1 − s)² + 4σs)        (σ^{−1/2} at the midpoint s = 1; 17.5 at s = 1.1 and 4.9 at s = 1.5 for σ = 10⁻³)

(the structure factor at zero wave vector; the closed form checked against the transfer
matrix at 20 000 residues for five parameter pairs).  **The infinite-chain value is not
the value for a peptide:** the cooperative length `σ^{−1/2}` (32 residues for `σ = 10⁻³`,
100 for `10⁻⁴`) exceeds the length of most helical peptides, and the factor is then
limited by the length.

| `n` (`σ = 10⁻³`) | `s` at the chain's own midpoint (largest `Var(N_h)`) | helix fraction there | `Var(N_h)` | `S_n` | `Var(N_h)/(2n)` (independent residues at `θ = ½`: `0.125`) | `1/sd(N_h)` (`k_BT` per residue) |
|---|---|---|---|---|---|---|
| 10 | `1.75` | `0.45` | `16.4` | `6.9` | `0.82` | `0.25` |
| 20 | `1.24` | `0.43` | `52.1` | `11.5` | `1.30` | `0.14` |
| 30 | `1.12` | `0.42` | `100` | `15.1` | `1.67` | `0.10` |
| 50 | `1.05` | `0.42` | `219` | `20.1` | `2.19` | `0.068` |
| 100 | `1.015` | `0.43` | `575` | `25.8` | `2.88` | `0.042` |
| 1 000 | `1.001` | `0.49` | `7 665` | `31.1` | `3.83` | `0.011` |
| ∞ | `1` | `0.5` | — | `31.6` | `3.95` | `0` |

(For `σ = 10⁻⁴`: `S_n = 14.2`, `19.9`, `48.8` at 20, 30, 100 residues, against `100` for the
infinite chain.  At `s = 1` a short chain is almost all coil — helix fraction `0.07` at 20
residues for `σ = 10⁻³` — and its variance is small; the table is at each chain's own
midpoint.)  Reading [H]: for a twenty-residue peptide at its helix–coil midpoint an
unknown residual with single-residue effect `u` costs about **ten times** what it costs
for independent two-state residues, in all three second-order quantities, *as long as*
`u·sd(N_h) ≲ 1`, i.e. `u ≲ 0.14 k_BT` per residue (about `0.08 kcal/mol` at 300 K) — beyond
that the response saturates (the ensemble is nearly all-or-none: `Var(N_h) = 52` against
the largest possible `n²/4 = 100`) and nothing of the second-order statement survives;
at several `k_BT` per residue the other regime of the table above applies.  This is
the query-complexity counterpart of addendum A14(ii), and of a sensitivity the field
knows from practice: according to PubMed, Best and Hummer (J. Phys. Chem. B 113 (2009)
9004–15, [doi:10.1021/jp901540t](https://doi.org/10.1021/jp901540t)) report that force
fields "differ significantly in their alpha-helical propensities" and that "simple
backbone energy corrections" reproduce the helix fraction of short peptides [abstract
only; the size of their corrections is not in the abstract and is not quoted here].
Not established: that the residual of a real force field, as a function of helix–coil
states, has a single-residue envelope of this size — §2 and §2a measure envelopes per
torsion and per rotamer on a fixed backbone.

*Where the measured residuals sit.*  Same-lineage torsion refits (`βc ≈ 0.5–3` per
torsion; §2) straddle the crossover; charge-model changes and the solvent term
(`βc ≈ 2–53`) are on the large-envelope side, where — in this model — the
independent-site cost exponents overstate and the threshold understates.  Whether a
backbone with a helix–coil equilibrium behaves like the two-state chain here is not
established: the envelope classes measured in §2 and §2a are per torsion or per rotamer
on a *fixed* backbone, not per helix–coil state.

*Limits.*  One chain, two states, one coupling, one slope, no field; the proved
reversal cells rest on a proposition that only the theory division and one reviewer
have derived; floating-point rounding is not controlled; the crossover slope is not
located; nothing was simulated.

