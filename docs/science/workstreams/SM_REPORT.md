# SM_REPORT — Workstream M: prior art for the measurement side

*What do ensemble-averaged data determine?  Prior art, read at the level of statements, for the
science division's direction "experimental data as information" (questions Q1–Q3 of
`M_brief.md`).*

Researcher: workstream M (independent).  Date: 2026-11-25.  Working directory:
`experiments/science/ws_M/` (`NOTES.md` = complete step and search log S1–S50;
`check_statements.py`, `check_q2_decomposition.py` = the numerics of §3).  No theory was
developed here beyond three one-line remarks that are labelled **[P]**; everything else is a
comparison of published statements with the division's sketches.

**Reading-level tags (rule 5).**  `[full text]` = I downloaded the PDF, extracted the text and read
the passages quoted (sections named).  `[full text via fetch tool]` = a page-fetching tool (a small
model) read the page and returned extracts; I did not see the raw text, the tool truncated long
pages at 100 000 characters and capped quotations at about 125 characters.  `[abstract]` = abstract
only (PubMed / arXiv / publisher record).  `[search snippet]` = only what a search engine returned.
`[from memory — unverified]` = my recollection, not checked in this session.  Bibliographic details
that I did not see in a tool result are marked "(ref. from memory)".  Records marked *(PubMed)* were
retrieved from PubMed; their DOIs are given as links.

**Epistemic labels (rule 6).**  **[K]** known and cited; **[P]** short paper argument given here;
**[N]** numerical evidence only; **[C]** conjecture / open; **[H]** heuristic.  Nothing here is
machine-checked.

---

## 1. Verdicts in one paragraph

**Q1 (identified sets).**  The mathematics is known in full generality and under several names;
the application to conformational ensembles is known only in a special case and without
guarantees.  (i) The exact range of `∫ψ dμ` given averages `∫φ dμ = m` is the generalised moment
problem (Isii, Kemperman, Karlin–Studden; de Finetti's "fundamental theorem of prevision"; OUQ),
a linear programme whose dual is the semi-infinite "hard-max" problem
`inf_λ [max_x (ψ − λ·φ)(x) + λ·m]`.  (ii) For `ψ` = indicator of a conformation or region this is
an **established experimental-NMR method** — MAP (2007), Maximum Occurrence / MaxOcc (2010–),
maxOR and minOR (2014) of the Florence group — resting on a **theorem** of Gardner, Longinetti
and Sgheri (2005); the same object is the *maximal mass function* of moment theory, with an
exact conic dual (Schmüdgen 2015, not read; di Dio–Schmüdgen 2018, read).  In the texts I read
the two literatures do not cite each other.  (iii) Adding a KL (φ-divergence) ball around a reference measure gives the dual
`inf_{η>0,λ} [η ln E_{μ0} e^{(ψ−λ·φ)/η} + ηρ + λ·m]`, with convergence to the prior-free sharp
bounds as `ρ → ∞`: **this is Proposition 2.1 and Theorem 2.1 of Christensen & Connault
(Econometrica 2023; numbering of arXiv v4)**, in econometrics.  **Not found**: any of this for molecular ensembles with a
physical prior neighbourhood; general `ψ` in structural biology; dual certificates for the
numbers that are published (MaxOcc is computed by penalised least squares on a finite pool with
a heuristic misfit threshold); moment constraints on a density-ratio or metric ("envelope")
class; a KL-UQ bound evaluated with rigorous partition-function bounds.
**Q2 (non-identifiability).**  The positive half (interaction order `≤ m` ⇒ identified by
`≤ m`-marginals) is textbook (minimal exponential families; Griffiths–Ruelle; Henderson) and is
computationally hard in general (Bresler–Gamarnik–Shah).  The negative mechanism is also known:
there are `k`-wise independent distributions (uniform on linear codes of dual distance `> k`)
with entropy `O(k log n)` (Alon–Babai–Itai lineage; entropy bounds: Gavinsky–Pudlák,
Bhangale–Potukuchi), and Albanna et al. (2017) conclude, for `k = 2, 3` in the unrestricted
class, that the range of entropies consistent with means and pairwise correlations is nearly
the whole interval unless a further structural property is known (my paraphrase; their words
are quoted in K9).  **Not found**: the statement restricted to a
*Gibbs class with bounded single-site energy differences* (where the minimum entropy is
extensive), for every `k`, and its reading for single-site NMR proxies of entropy.  The
construction (a code-supported measure smoothed into a regular one) appeared three weeks ago in
a different theorem (Arnese–Lacker, arXiv:2611.07460); in its convolution form it is a random
codeword seen through a binary symmetric channel, for which the no-go has a three-line proof
(K10(f)) and for which a lower bound on entropy from marginals of *linear* order is published
(Samorodnitsky, arXiv:1508.01464).
**Q3 (value of information).**  The worst-case formulation — choose the experiment minimising the
largest possible width of the optimal bounds after its outcome — is **equation (2.8) of the OUQ
paper** (Owhadi et al., SIAM Review 2013), with "campaigns of experiments" as a game; no structure
theorems are given there.  In structural biology only empirical or average-case notions were
found (MaxOcc decreases when data are added; entropy reduction of a reweighted ensemble; FRET/DEER
label selection).  **Not found**: theorems on how much one more averaged observable shrinks an
identified set of a conformational ensemble, or on adaptivity for such problems.
**Most important negative finding for the division:** "exact range over all ensembles consistent
with averaged data" must not be claimed as new, neither mathematically nor in NMR; and the
KL-ball dual must be attributed to Christensen–Connault (and the divergence-ball lineage).

---

## 2. Precise statements, with comparison

Notation of the brief: `X` configuration space, `μ` the ensemble, data `m_k = ∫φ_k dμ`
(`k = 1..K`), target `∫ψ dμ`, reference `μ0 ∝ e^{−βf}`, weights `w = dμ/dμ0`.

### 2.1 Q1 — identified sets

**K1 [K] (generalised moment problem).**  For `M(m) = {μ ≥ 0 : ∫dμ = 1, ∫φ dμ = m}` the set
`{∫ψ dμ : μ ∈ M(m)}` is an interval `[L, U]`;
`U = inf{λ0 + λ·m : λ0 + λ·φ(x) ≥ ψ(x) ∀x}` under a constraint qualification; extreme points of
`M(m)` have at most `K + 1` atoms.
*Sources.*  Isii 1959/1960/1962; Karlin–Studden 1966 (Markov–Krein); Mulholland–Rogers 1958; Karr
1983; von Weizsäcker–Winkler 1979/80; Winkler 1988 — bibliographic entries read in the reference
list of OUQ, originals **not read**.  Owhadi, Scovel, Sullivan, McKerns, Ortiz, "Optimal
Uncertainty Quantification", arXiv:1009.0679v3 (SIAM Rev. 55(2):271–345, 2013,
[doi:10.1137/10080782X](https://doi.org/10.1137/10080782X); journal version not read)
`[full text: abstract, §2.2, §4 Thm 4.1, Remarks 4.2–4.3]`: Theorem 4.1 — with `n'` generalised
moment constraints on a product of Suslin spaces and `n_i` on factor `i`, the supremum of `E_μ[r]`
is attained on products of convex combinations of `n_i + n' + 1` Dirac masses, with no assumption
on the functions.  Kemperman 1971/1983/1987 duality and the *linear semi-infinite programme*
`U* = inf{Σβ_iη_i : Σβ_i h_i(s) ≥ u(s) ∀s}` in robust Bayes: Betrò, Bodini, Guglielmi,
"Generalized moment theory and Bayesian robustness analysis for hierarchical mixture models"
(author preprint `aism2005.pdf` read; a search result lists the article as
doi:10.1007/s10463-006-0046-8, Ann. Inst. Statist. Math.)
`[full text: abstract, §1, eq. (3.2), references]`.  De Finetti's fundamental theorem as an LP for
general quantities with interval inputs and outputs: Lad, Dickey, Rahman, Statistica 50(1):19–38
(1990), [doi:10.6092/issn.1973-2201/822](https://doi.org/10.6092/issn.1973-2201/822)
`[abstract via fetch tool, paraphrased]`.  SDP hierarchies: Bertsimas–Popescu, SIAM J. Optim.
15(3):780–804 (2005) `[search snippet]`.  Decision analysis with moment information: Smith, Oper.
Res. 43(5):807–825 (1995), [doi:10.1287/opre.43.5.807](https://doi.org/10.1287/opre.43.5.807)
`[search snippet]`.  Chemical-physics precedent (spectral measures): Gordon, J. Math. Phys.
9(5):655–663 and 9(7):1087–1092 (1968) — bounds "both rigorous and optimal" on thermodynamic
properties and responses from finitely many moments `[search snippet; author from memory]`.
*Comparison with Q1.*  Identical object when no prior neighbourhood is imposed.  The brief's
remark "the dual is a global optimisation `max_x[ψ(x) − λ·φ(x)]`" is the feasibility test of the
semi-infinite dual; it is the pricing step of column generation in probabilistic satisfiability
(Jaumard, Hansen, Poggi de Aragão, ORSA J. Comput. 3(2):135, 1991 `[search snippet]`; that the
pricing problem is a nonlinear 0–1 programme: `[from memory — unverified]`) and the inner problem
of Betrò–Guglielmi's algorithm, which per a search snippet "combines interval analysis with
semi-infinite linear programming" — i.e. **a rigorous global optimiser inside the dual of a
moment problem already exists in robust Bayes** `[search snippet]` (to be read by the coordinator).

**K2 [K] (maximal mass at a point = MaxOcc).**
(a) Gardner, Longinetti, Sgheri, Inverse Problems 21 (2005) 879–898,
[doi:10.1088/0266-5611/21/3/006](https://doi.org/10.1088/0266-5611/21/3/006)
`[full text: abstract, §1, §3, §4 statements, §7]`.  Unknown probability measure `p` on SO(3);
data = mean paramagnetic tensor `χ̄ = ∫R*χR dp(R)` (RDCs are linear in it).  "knowledge of the
five distinct entries of the symmetric matrix χ̄ does not allow exact reconstruction of the
probability measure p".  Thm 3.3: the set `V` of attainable data is the set of symmetric traceless
matrices with eigenvalues in `[μ_min, μ_max]`.  Thm 3.5: three rotations always suffice.
**Thm 3.8** ("an optimal estimate"):
`p_max(R0) = sup{0 ≤ t < 1 : (χ̄ − t R0*χ_d R0)/(1 − t) ∈ V}`.  Thm 4.6: the same for two metals
(≤ 10 rotations suffice, Thm 4.2).  "The value p_max is very hard to compute"; in practice it is
obtained by a non-convex fit with simulated annealing and bisection, "a reasonable estimate (from
below)".
(b) di Dio & Schmüdgen, "The multidimensional truncated moment problem: the moment cone",
arXiv:1809.00584v1 `[full text: abstract, introduction, §10 Def. 74, Prop. 75 with proof]`.  For
measurable functions `A = {a_1..a_m}` on `X`, moment sequence `s`, moment cone `S_A`:
*maximal mass function* `ρ_s(x) := sup{μ(A_x) : μ ∈ M_A(s)}` and
**Prop. 75**: `ρ_s(x) = sup{c ≥ 0 : s − c·s_A(x) ∈ S_A} ≤ κ_s(x) := inf{L_s(p) : p ∈ Pos(A), p(x) = 1}`,
with equality and attainment if `S_A` is closed and pointed (continuous functions on a compact
space, a positive element in the span).  "Determining the maximal mass at a given atom leads to a
convex optimization problem [Sm15]" (= Schmüdgen, Methods Funct. Anal. Topology 21 (2015) 266–281,
**not read**).  In one variable with polynomial moments `ρ` is the Christoffel function
`[search snippet]`.
*Comparison.*  (a) is the first formula of (b) for one family of functions; (b) adds the exact
dual: a certificate of `MaxOcc(x0) ≤ κ` is a function `p = λ0 + λ·φ` with `p(x0) = 1`, **`p ≥ 0` on
all of `X`** (a global minimisation over conformations), and value `λ0 + λ·m`.  Neither paper cites
the other's literature (grep of both texts and of the 2005 reference list).  I checked the three
formulas against each other on 120 random finite instances: agreement to `1.1e-7` **[N]** (§3, N1).

**K3 [K] (MaxOcc, maxOR, minOR as practised).**  All from the group of Bertini, Luchinat, Parigi,
Ravera, Sgheri and co-workers; *(PubMed)* for the abstracts.
* Bertini et al., JACS 129 (2007) 12786, [doi:10.1021/ja0726613](https://doi.org/10.1021/ja0726613)
  `[abstract]`: "maximum allowed probabilities (MAPs) of conformations".
* Bertini et al., JACS 132 (2010) 13553, [doi:10.1021/ja1063923](https://doi.org/10.1021/ja1063923)
  `[abstract]`: "The concept of maximum occurrence (MO), i.e., the maximum percent of time that
  flexible proteins can spend in any given conformation, is introduced" (SAXS + PCS + RDC).
* Bertini et al., J. Biomol. NMR 53 (2012) 271,
  [doi:10.1007/s10858-012-9638-1](https://doi.org/10.1007/s10858-012-9638-1) `[abstract]`:
  "Whatever the real ensemble of conformations sampled by a protein, the weight of any conformation
  cannot exceed the calculated corresponding Maximum Occurrence value."
* **Andrałojć, Luchinat, Parigi, Ravera, J. Phys. Chem. B 118 (2014) 10576**,
  [doi:10.1021/jp504820w](https://doi.org/10.1021/jp504820w) `[abstract; full text of
  Introduction, Methods and start of Results as reprinted in W. Andrałojć's PhD thesis, Univ. of
  Florence, flore.unifi.it handle 2158/1072773]`: "The method explores subregions of the
  conformational space and provides both upper and lower bounds of probability for the system to
  be in each subregion"; maxOR/minOR = "the largest and smallest weight ... that all conformations
  belonging to such region must have to provide averaged data in agreement with the experimental
  data, once complemented by other conformations outside this region"; "the minimum occurrence of
  a region (minOR) can be immediately obtained from the difference between 1 and the maxOR of the
  complementary region".  Computation: regularised non-negative least squares with the region's
  weight fixed, pool of 50 000 conformers, bound = largest/smallest weight whose fit quality `Q` is
  within 1.2 × the best `Q`.
* Gigli et al., PCCP 20 (2018) 27429, [doi:10.1039/c8cp06195e](https://doi.org/10.1039/c8cp06195e)
  `[full text, author version]`: "Ensemble reconstruction is an ill-posed inverse problem: infinite
  different ensembles can reproduce the experimental results equally well"; MaxOcc "provides an
  upper bound of the conformation's statistical weight and converges (decreases) towards the true
  statistical weight by increasing the number of independent experimental restraints"; computed as
  `argmin_w [‖Pw − d‖² + ξ1(‖w‖₁ − 1)² − ξ2 w_c]`, `w ≥ 0`, multipliers from an L-curve.
* Clarelli & Sgheri, arXiv:1602.05953 `[full text: §1–§3.4]`: "The Maximal Allowable Probability
  (MAP) is the largest weight of a given state in a probability distribution which is a solution.
  As a function of the state, the MAP is not a solution but a sharp bound from above"; MEP
  (maximum entropy / Kullback–Leibler) and MAP as "two limit cases"; an iterative "simplex
  algorithm" in the convex moment set `V` (Carathéodory: `≤ n_meas + 1` conformers).
* Sgheri, Inverse Problems 26 (2010) 035003,
  [doi:10.1088/0266-5611/26/3/035003](https://doi.org/10.1088/0266-5611/26/3/035003)
  `[abstract via fetch tool, paraphrased]`: maximal probability of any measurable set of
  orientations.  Longinetti, Sgheri, Sottile, Discrete Comput. Geom. 43 (2010) 54, arXiv:0712.3777
  `[full text: intro, §1]` (facial structure, Carathéodory number ≤ 8 for two tensors).
* Reviews: Ravera, Sgheri, Parigi, Luchinat, PCCP 18 (2016) 5686,
  [doi:10.1039/c5cp04077a](https://doi.org/10.1039/c5cp04077a) `[abstract only — full text not
  accessible]`: maximum entropy shows "the features that are common to all the infinite solutions
  satisfying the experimental data", large-weight methods "the conformational regions where a
  large probability can be placed", and "The upper limits for conformational probabilities
  (MaxOcc) can also be calculated".  Hou & Tochio, Biophys. Rev. 14 (2022) 55,
  [doi:10.1007/s12551-021-00916-4](https://doi.org/10.1007/s12551-021-00916-4)
  `[full text via fetch tool]`: "MaxOcc does not guarantee minimum occurrence"; no newer
  range-type method is described.
* Earlier: Nikiforovich, Vesterman, Betins, Podins, J. Biomol. Struct. Dyn. 4 (1987) 1119,
  [doi:10.1080/07391102.1987.10507702](https://doi.org/10.1080/07391102.1987.10507702)
  `[abstract]`: "it appears possible to confine the entire region of all w_i values only by those
  points (w_i) that provide a reasonable agreement between the results of calculations and the
  experimental data" — a feasible-region treatment of conformer weights for peptide NMR.
*Comparison with Q1.*  Same quantifier ("whatever the real ensemble"), same data model
(population-weighted averages), `ψ` = indicator of a conformer or region, both ends for regions.
Differences: (1) **no prior measure** — only a pool of sterically allowed conformers (the case
`ρ = ∞`); (2) no other `ψ` (an unmeasured observable, a distance moment) in what I read; (3) the
published numbers are optimal values of a penalised least-squares problem with a tolerance fixed
relative to the best fit, on a finite pool: **no dual bound, no statement of how far the number is
from the supremum over the continuous space** (the thesis notes that a wrong value at zero weight
"would actually point towards an under-sampling"); (4) the exact results are confined to RDC
tensors.  The identity `minOR(A) = 1 − maxOR(Aᶜ)` is checked in §3 (N1).

**K4 [K] (divergence ball plus moment constraints).**  Christensen & Connault, "Counterfactual
Sensitivity and Robustness", arXiv:1904.00989v4 (Econometrica 91(1):263–298, 2023,
[doi:10.3982/ECTA17232](https://doi.org/10.3982/ECTA17232); journal version not read)
`[full text: abstract, §1, §2.2, Assumption Φ, Prop. 2.1, eqs. (13)–(16), Thm 2.1, Remark 2.7,
Appendix B Lemmas B.1–B.3]`.  With `N_δ = {F : D_φ(F‖F*) ≤ δ}` and moment (in)equalities
`E_F[g] ⋚ P`:
* **Prop. 2.1**: `sup{E_F[k] : F ∈ N_δ, moments} = inf_{η>0, ζ, λ} η E_{F*}[φ*((k − ζ − λ'g)/η)] + ηδ + ζ + λ'P`;
  for KL: `inf_{η>0, λ} η ln E_{F*} e^{(k − λ'g)/η} + ηδ + λ'P`; the value is `−∞` iff the ball
  contains no distribution satisfying the moments.
* eqs. (15)–(16): the smallest divergence compatible with the moments and its dual (the
  I-projection).
* **Thm 2.1**: as `δ → ∞` the bounds converge to "the sharp nonparametric bounds".
* **Lemma B.3 / Remark 2.7**: the nonparametric bound equals
  `inf_λ (ess sup_u (k − λ'g)(u) + λ'P)`; "setting δ < ∞ replaces a 'hard-max' (an optimization
  over u) with a 'soft-max' (a convex expectation)".
*Comparison with Q1.*  This **is** the Q1 statement for the KL-ball neighbourhood, with the same
dual, the same limit and the same observation about the global optimisation; hypotheses: `k`, `g`
in an Orlicz class of `F*` (exponential moments for KL), a relative-interior condition.  Context:
the distribution of latent variables in structural econometric models; the reference is a
parametric family, not a Boltzmann measure; the soft-max is evaluated by quadrature or
simulation, with statistical inference for estimated moments (§6 there) but no certified bound.
Checked numerically on 12 finite instances × 2 radii: direct optimisation = dual to `4.9e-10`;
at `ρ = 60` the dual equals the prior-free LP value **[N]** (§3, N2).
*Lineage.*  Divergence balls without data constraints: Chowdhary–Dupuis 2013; Dupuis, Katsoulakis,
Pantazis, Plecháč 2016; Gourgoulias, Katsoulakis, Rey-Bellet, Wang 2020 (Thm 2: tight on
`{Q : R(Q‖P) ≤ η²}`, attained by exponential tilts `[full text of Thm 1–2]`); Katsoulakis,
Rey-Bellet, Wang 2017 (Gibbs measures, phase diagrams) `[abstract]`; Breuer–Csiszár,
arXiv:1301.4832 `[abstract + one section]` (worst case over relative-entropy/Bregman/f-divergence
balls, tied to a moment problem); Lam, arXiv:1303.0326 `[abstract]`.  These were already read by
the theory division (`prior_art/L6`, items with DOIs).  Birmpa, Feng, Katsoulakis, Rey-Bellet,
arXiv:2107.08179 `[abstract + grep]`: KL ambiguity sets per component of a Bayesian network with
physico-chemical examples; no averaged-data constraints.  Glasserman & Xu, Quantitative Finance
14(1):29–58 (2014): relative-entropy worst case with "expectation constraints" — known to me only
from the table of contents of X. Xu's thesis `[search snippet]` and memory.

**K5 [K] + [P] (maximum entropy / Bayesian refinement gives one point and the frontier).**
Maximum-entropy reweighting is the I-projection of `μ0` on `M(m)`; BioEn maximises
`−θ·S_KL − χ²/2` and recommends "the kink of the S_KL-versus-χ² curve" for choosing `θ`.  Hummer & Köfinger, J. Chem. Phys. 143 (2015) 243150,
[doi:10.1063/1.4937786](https://doi.org/10.1063/1.4937786), arXiv:1509.04447
`[full text: abstract, conclusions; whole text searched for unique/underdetermined/bound]`;
Cesari, Reißer, Bussi, Computation 6 (2018) 15, arXiv:1801.05247 `[full text: intro, discussion]`
("as close as possible to the prior distribution ... different priors are in principle expected
to lead to different posteriors"); Pitera & Chodera, JCTC 8 (2012) 3445 (ref. from memory)
`[full text, passage]` ("in underdetermined cases, there may be many distributions whose ensemble
averages satisfy experimental constraints"; MaxEnt is "the unique minimally biased choice");
Bonomi et al., Sci. Adv. 2016 (metainference), arXiv:1509.05684 `[whole text searched]`; Bonomi,
Heller, Camilloni, Vendruscolo, Curr. Opin. Struct. Biol. 42 (2017) 106–116 `[full text, author
copy]`: the inverse problem "is an ill-defined problem, in the sense that it allows multiple
solutions ... As long as different structural ensembles generate the same observable average
quantities, and thus result in similar predictions for the system properties, they should be
considered equivalent".  Posterior (typical-case) uncertainty of the weights is what Bayesian
weighting and BICePs provide — Fisher, Ullman, Stultz, Pac. Symp. Biocomput. 2012:82–93 `[abstract]`
*(PubMed)*: "models that contain more structures than the available experimental restraints are
problematic as the large number of degrees of freedom in the ensemble leads to considerable
uncertainty in the final model"; Raddi et al. 2026 (BICePs, J. Chem. Phys.) `[abstract, via
Consensus]`.  None of these texts states a range, a bound or the set of all solutions.
Köfinger & Hummer, J. Chem. Phys. 160 (2024),
[doi:10.1063/5.0189901](https://doi.org/10.1063/5.0189901) `[abstract]`: the balance of data and
model "Viewed as a Pareto optimization problem"; "By relating the variance of this energy
difference to the Kullback-Leibler divergence ... one can encode prior knowledge about energy
uncertainties, i.e., force-field errors, in the exchange rate".
*Remark [P] (one line, not checked numerically beyond N2).*  For hard constraints the set
`{μ : KL(μ‖μ0) ≤ ρ, ∫φ dμ = m}` is non-empty iff `ρ ≥ D*(m) := min{KL(μ‖μ0) : ∫φ dμ = m}`, the
value of the maximum-entropy problem; with a misfit tolerance `χ² ≤ c` it is non-empty iff
`(c, ρ)` lies on or above the BioEn `S_KL`–`χ²` curve.  So the curve that BioEn users plot to
choose `θ` is the feasibility frontier of Q1, and Q1 asks for the spread of `∫ψ dμ` above it.
The step from "the same observable average quantities" to "similar predictions for the system
properties" (Bonomi et al., quoted above) is precisely the inference that an identified-set
computation tests.

**K6 [K]/[not found] (density-ratio and envelope classes).**  `prior_art/L5` (items P5–P7) already
established: density-ratio classes (DeRobertis–Hartigan; Wasserman), Walley's bounded-derivative
model, the linear-fractional-to-linear reduction (Lavine; Zhao–Small–Bhattacharya), and "no match"
for a metric-governed class.  Added here: (i) generalised-moment classes of priors are standard in
robust Bayes and lead to linear semi-infinite programmes (Betrò et al., K1); (ii) two searches for
a density-ratio or density-band class **with** moment constraints (S27, S43 in the log) returned
nothing — Perone Pacifico–Salinetti–Tardella's "constrained density band classes" is
`[from memory — unverified]`; (iii) dilation, the phenomenon that conditioning can widen every
probability interval, is treated by Seidenfeld & Wasserman, Ann. Statist. 21(3):1139–1154 (1993)
`[search snippet]`; it cannot occur in Q1 because data enter as intersections with moment sets
(**[P]**, trivial: intersecting can only shrink a range).
*Remark [P] (checked, §3 N4).*  With normalisation written as `Σμ0 w = 1`, the range of `Σμ0 wψ`
over `{w ≥ 0 : w(y) ≤ e^{βd(x,y)}w(x), Σμ0 w = 1, Σμ0 wφ = m}` is one LP per end; no
Charnes–Cooper step is needed.  I found this statement nowhere, and it is immediate.

**What appears to be missing for Q1** (not found in S1–S50; absence of a keyword match was not
used — the nearest statements above were compared):
1. Identified sets `[L, U]` of an unmeasured observable of a *molecular* ensemble over a
   neighbourhood of a physical model (KL ball, or envelope/density-ratio class) intersected with
   experimental averages.  Mathematics: known (K1, K4).  Molecular instance: only MaxOcc/minOR
   (no prior, indicator `ψ`).
2. Guaranteed numbers: a dual certificate (K2(b), K4) evaluated with a rigorous global optimiser
   or a rigorous partition-function bound.  Search S37 (provable partition functions × model
   uncertainty) found no combination; the Betrò–Guglielmi algorithm (interval analysis inside a
   semi-infinite LP) is the nearest precedent, in robust Bayes `[search snippet]`.
3. The envelope cone with moment constraints, and any closed form extending Theorem 11.12 of
   the theory report to one moment constraint.
4. A translation between the three communities: MaxOcc = maximal mass function = upper
   probability / natural extension of an indicator = sharp bound of partial identification.

### 2.2 Q2 — non-identifiability

**K7 [K] (the identified half).**  "For graphical models representing a minimal exponential
family, the canonical parameters are uniquely determined by the mean parameters ... no algorithm
can learn the canonical parameters of a generic pair-wise binary graphical model from the mean
parameters in time bounded by a polynomial in the number of variables (unless RP = NP)" — Bresler,
Gamarnik, Shah, arXiv:1409.3836 `[abstract]`.  Lattice: uniqueness of the pair potential "has
already been settled by Griffiths and Ruelle"; continuum: Henderson 1974 for the canonical
ensemble, with a gap in the thermodynamic limit closed for a class of superstable potentials —
Frommer, Hanke, Jansen, arXiv:1903.03317 `[full text: abstract, §1]`; "The general existence
problem is widely open".  One-body version: Chayes–Chayes–Lieb, Commun. Math. Phys. 93 (1984)
57–121 `[search snippet]`.  Henderson, Griffiths–Ruelle: **not read**.
*Comparison.*  The brief's "energies of interaction order ≤ m are identified by ≤ m-site
marginals" is this statement; nothing to claim.  Two caveats to carry: identification is not
recovery (hardness above), and realizability of given marginals is itself open in general.

**K8 [K] (non-uniqueness given low-order data).**
* Kuna, Lebowitz, Speer, J. Stat. Phys. 129 (2007), arXiv:math-ph/0612075 `[abstract, §1]`:
  realizability of `(ρ1, ρ2)` is "an infinite dimensional version of the standard truncated
  moment problem"; "Typically if any realizing process exists there will be many (even an
  uncountable number)"; on a finite set there is "a realizing Gibbs measure with k body
  potentials which maximizes the entropy among all realizing measures".
* Schneidman, Still, Berry, Bialek, arXiv:physics/0307072 (Phys. Rev. Lett. 2003, ref. from
  memory) `[passages]`: "connected information of order k"; the XOR example in which pairwise
  marginals carry nothing.
* RDCs: "up to 25 motionally averaged Wigner rotation elements ... can be determined
  experimentally from multialignment RDCs" — Fisher, Zhang, Stelzer, Al-Hashimi, J. Phys. Chem. B
  112 (2008) 16815, [doi:10.1021/jp806188j](https://doi.org/10.1021/jp806188j) `[abstract]`
  *(PubMed)*; "even the exact knowledge of 5 mean tensors (i.e. 25 real numbers) does not allow
  the exact reconstruction of the probability measure p" — Longinetti–Sgheri–Sottile
  `[full text]`; Clarelli–Sgheri Prop. 2.2 `[full text]`.
* Jardetzky, Biochim. Biophys. Acta 621 (1980) 227,
  [doi:10.1016/0005-2795(80)90174-9](https://doi.org/10.1016/0005-2795(80)90174-9) `[abstract]`
  *(PubMed)*: the average structure "represents a virtual structure devoid of physical meaning".
* FRET: Song, Gomes, Shi, Gradinaru, Chan, Biophys. J. 113 (2017) 1012,
  [doi:10.1016/j.bpj.2017.07.023](https://doi.org/10.1016/j.bpj.2017.07.023)
  `[abstract; full text via fetch tool]` *(PubMed)*: "a single value of average transfer
  efficiency ⟨E⟩ ... is generally consistent with highly diverse, multiple values of the average
  radius of gyration ⟨Rg⟩"; the quantification is a conditional distribution `P(Rg² | ⟨E⟩)` under
  the model's sampling measure, **not a minimum–maximum range**.  Fuertes et al., PNAS 114 (2017)
  E6342, [doi:10.1073/pnas.1704692114](https://doi.org/10.1073/pnas.1704692114) `[abstract]`.
* General theorems of the same flavour in UQ: Owhadi, Scovel, Sullivan, "Brittleness of Bayesian
  Inference Under Finite Information in a Continuous World", Electron. J. Stat. 9 (2015) 1–79,
  [doi:10.1214/15-EJS989](https://doi.org/10.1214/15-EJS989), arXiv:1304.6772 `[abstract]`:
  "optimal lower and upper bounds on posterior values obtained from Bayesian models that exactly
  capture an arbitrarily large number of finite-dimensional marginals of the data-generating
  distribution ... such models may still make the largest possible prediction error"; and "On the
  Brittleness of Bayesian Inference", SIAM Rev. 57(4):566–582 (2015),
  [doi:10.1137/130938633](https://doi.org/10.1137/130938633), arXiv:1308.6306 `[abstract]`
  (closeness "in terms of the total variation metric or the matching of a finite system of
  generalized moments" does not prevent opposite posterior conclusions).

**K9 [K] (entropy against marginals).**
* Upper bounds from marginals are standard; in molecular simulation MIST "is also guaranteed to
  bound the entropy" — King, Silver, Tidor, J. Phys. Chem. B 116 (2012) 2891,
  [doi:10.1021/jp2068123](https://doi.org/10.1021/jp2068123) `[abstract]` *(PubMed)*; the mutual
  information expansion is a truncated expansion, not a bound — Killian, Kravitz, Gilson, J. Chem.
  Phys. 127 (2007) 024107, [doi:10.1063/1.2746329](https://doi.org/10.1063/1.2746329) `[abstract]`.
* **Albanna, Hillar, Sohl-Dickstein, DeWeese, Entropy 19 (2017)** (article number from memory),
  arXiv:1209.3744v4 `[full text: abstract, §1, §2, discussion]`: "Given a set of observed mean
  firing rates and pairwise correlations between neurons, what are the possible entropies for the
  system?"; `log2(N/(1+(N−1)ᾱ)) ≤ S̃_2 ≤ log2(1 + N(N+1)/2)` for the minimum entropy; "The range of
  possible entropies ... for many cases, the gap grows linearly with the system size N, up to a
  logarithmic correction"; "measuring pairwise or even triplet-wise correlations ... is
  insufficient to provide a useful floor on the information rate, no matter what values are
  empirically observed.  However, knowing the extent to which other statistical properties are
  obeyed can yield strong guarantees" (exchangeability).
* Bhangale & Potukuchi, arXiv:1709.00752v2 `[full text: abstract, §1, Thm 1.1–1.2]`: the uniform
  law on `yᵀM` (`M` a parity-check matrix of a code of distance `d`) is `(d−1)`-wise independent;
  BCH codes give support `O(n^{k/2})`; it attributes to Gavinsky and Pudlák the lower bound
  `log C(n, k/2)` on the entropy of `k`-wise independent variables for small `k`; Thm 1.1: `(k−1)`-wise independent unbiased bits have
  `H ≥ n − n·H(1/2 − sqrt((k/n)(1 − k/n))) − o(n)`.  Gavinsky & Pudlák, arXiv:1503.08154
  `[abstract]`: "How low can the joint entropy of n d-wise independent (for d ≥ 2) discrete random
  variables be, subject to given constraints on the individual distributions ...?  This question
  has been posed and partially answered in a recent work of Babai"; tight lower bounds for
  pairwise and three-wise independent balanced binary variables.  (Babai, Alon–Babai–Itai, Chor
  et al.: **not read**.)
* Arnese & Lacker, arXiv:2611.07460 (5 Nov 2026) `[abstract, Prop. 2.7, Remark 6.1]`: "most
  k-dimensional coordinate marginals are close to product measures" for broad classes; the
  sharpness example is a strength-2 orthogonal array (the `q`-ary simplex code) "with the
  continuous uniform blurring".
* Positive counterpart under weak dependence: entropy factorisation under spectral/entropic
  independence (Jain et al. 2026; Blanca et al. 2026) `[abstract, via Consensus]`.

**K10 — the brief's sketch in exact form, and what the literature covers.**  Class `𝒢_c`: Gibbs
measures `μ ∝ e^{−βE}` on `{0,1}ⁿ` with `|E(x) − E(x ⊕ e_i)| ≤ c`; `u = βc`, `p_u = 1/(1+e^u)`,
`h` the binary entropy (nats).
(a) **[P]** (standard) `H(μ) ≥ Σ_i H(X_i | X_{−i}) ≥ n·h(p_u)` for `μ ∈ 𝒢_c` (conditioning reduces
entropy; conditional odds lie in `[e^{−u}, e^u]`); equality for the product measure
`E = c·|x|`.
(b) **[P]** For a linear code `C`, `μ_C ∝ e^{−u·dist(x,C)}` is in `𝒢_c` and is invariant under
translation by `C`, so its Fourier coefficients vanish off `C^⊥` and all marginals on fewer than
`d(C^⊥)` sites are exactly uniform.  (This is the classical fact of K9 applied to a
`C`-invariant measure.)
(c) **[P]** `x ↦ (coset, codeword)` gives `μ_C = (uniform on C) ⊗ ν`, `ν(coset) ∝ e^{−u·w(coset)}`
with `w` the coset-leader weight; hence **`H(μ_C) = ln|C| + H(ν)` exactly**.
(d) **[N]** In the 16 cases computed (§3, N3) `0.249·ln|C| ≤ H(μ_C) − n·h(p_u) ≤ ln|C|`, the upper
inequality being an equality to four digits for `u = 8` and within 2 % for `u = 4`.  **[C]** `H(μ_C) ≤ n·h(p_u) + ln|C|` in general.
(e) **[H]** With dual-BCH codes, `ln|C| = O(k ln n)`, so for each fixed `k` the entropy per site of
a `k`-wise uniform member of `𝒢_c` tends to the class minimum, while the uniform measure (also in
`𝒢_c`, same `≤ k`-marginals) has `ln 2`.  The excess `ln|C| ≈ (k/2)·ln n` has the size of the
Gavinsky–Pudlák lower bound for *unrestricted* `k`-wise independent laws; whether
`n·h(p_u) + Ω(k ln n)` is necessary inside `𝒢_c` I did not find and did not try to prove.
(f) **[P]** (a variant that needs no conjecture; checked numerically, §3 N3b).  Let `Y` be uniform
on `C`, `E` i.i.d. Bernoulli(`p_u`) independent of `Y`, `X = Y ⊕ E` with law `m` — a uniformly
random codeword seen through a binary symmetric channel.  Then (i) `m ∈ 𝒢_c`:
`m(x) = |C|⁻¹ Σ_c π(x ⊕ c)` and each term changes by a factor in `[e^{−u}, e^{u}]` under one flip;
(ii) `m` is `C`-invariant, so all marginals on fewer than `d(C^⊥)` sites are uniform;
(iii) `H(m) = H(X|Y) + I(X;Y) = n·h(p_u) + I(X;Y)` with `0 ≤ I(X;Y) ≤ ln|C|`.  Hence
**`n·h(p_u) ≤ H(m) ≤ n·h(p_u) + ln|C|`**, the excess being the mutual information across the
channel.  With the support size `O(n^{k/2})` of BCH-based `k`-wise independent spaces (quoted
in Bhangale–Potukuchi) this proves: *for every fixed `k` the class `𝒢_c` contains measures with
exactly uniform `≤ k`-site marginals and entropy at most `n·h(p_u) + O(k ln n)`, while the uniform
measure, with the same marginals, has entropy `n ln 2`.*
(g) **[K]** A published inequality of the opposite kind exists for exactly this smoothed family.
Samorodnitsky, "On the entropy of a noisy function", arXiv:1508.01464 `[abstract]`: for a random
binary vector `X` and binary-symmetric noise `Z` of crossover `ε`, with `v = (1 − 2ε)²·n`,
`H(X ⊕ Z) ≥ n·H(ε + (1 − 2ε)·H⁻¹(E_{|B|=v} H(X_B)/v))` up to lower-order terms — a strengthening
of Mrs. Gerber's lemma that lower-bounds the entropy of a noise-smoothed measure by the average
entropy of the *marginals of order `v`* of its un-smoothed part.  My reading **[H]** (from the
abstract only): with `ε = p_u`, marginals that are uniform up to order `v = tanh²(u/2)·n` force
the smoothed measure to have nearly maximal entropy; so inside the noisy-codeword family the
order of marginals at which entropy becomes constrained is *linear in `n`*, consistent with (f)
("no fixed order suffices") and with Bhangale–Potukuchi's Theorem 1.1 for the un-smoothed case.
Related: Samorodnitsky & Sberlo, arXiv:2008.07236 `[abstract]` (low-rate doubly transitive codes
decode errors on BSC(`p`) with high probability, i.e. `I(X;Y) ≈ ln|C|` there).
*Literature coverage.*  (b) and the small-support mechanism: known (K9).  The conclusion — the
identified set of the entropy is almost the whole a-priori interval, and a structural assumption
rescues it — is known for `k ≤ 3` in the unrestricted class (Albanna et al.), where the minimum
entropy is `O(log N)` and the low-entropy measures have tiny support.  Entropy of noisy
codewords and lower bounds from marginals of linear order: known (item (g)).  **Not found**: the
statement inside a class of everywhere-positive Gibbs measures with bounded energy differences —
the a-priori interval is `[n·h(p_u), n·ln 2]` and uniform `≤ k`-marginals are compatible with
both `n·h(p_u) + O(k ln n)` and `n ln 2` for every fixed `k` — as a statement about what
low-order averaged data determine; the decomposition (c); the dichotomy with K7 in one theorem.
Every ingredient of (f) is textbook, so the statement should be presented as an observation with
the attributions of K9 and (g), not as a new technique.
*Physical reading and its prior art.*  The NMR "entropy meter" converts single-site order
parameters into conformational entropy by a linear calibration.  Wand & Sharp, Annu. Rev. Biophys.
47 (2018) 41,
[doi:10.1146/annurev-biophys-060414-034042](https://doi.org/10.1146/annurev-biophys-060414-034042)
`[abstract; full text via fetch tool]` *(PubMed)*: the relation is introduced "By postulate";
"motions of different NMR probes may be correlated"; "the objections that might be made against
the oscillator inventory approach are subsumed into this empirical parameter"; in simulations the
coupling acts as "a linear scaling" of about 17 %.  Caro et al., PNAS 114 (2017) 6563,
[doi:10.1073/pnas.1621154114](https://doi.org/10.1073/pnas.1621154114) `[abstract]`: "the
generality of this relationship has not been shown" (then shown empirically on 28 complexes).
Hoffmann, Mulder, Schäfer, J. Phys. Chem. B 126 (2022) 54,
[doi:10.1021/acs.jpcb.1c07786](https://doi.org/10.1021/acs.jpcb.1c07786) `[abstract]` asks "How
Much Entropy Is Contained in NMR Relaxation Parameters?" with respect to *time scales*.  I found
no proved statement that site-wise averaged data cannot bound entropy within a stated energy
class; K10 would be that statement, **model-relative**: it says that the calibration's validity is
a property of proteins (weak, regular coupling), not of the measurement.

### 2.3 Q3 — value of information

**K11 [K] (worst-case formulation).**  OUQ `[full text, §2.2]`: experiments determine functionals
`Φ_i(G, P)` such as `E_P[G]` or `P[X ∈ A]`; with `A_{E,c}` the scenarios compatible with outcome
`c` of experiment `E`, "An experiment E* that is most predictive, even in the worst case, is
defined by a minmax criterion": `E* ∈ argmin_E sup_c (U(A_{E,c}) − L(A_{E,c}))` (their eq. 2.8);
"Planning of campaigns of experiments ... a min max game 'played against the Universe'"; Example
2.5 chooses sequentially between measuring means and variances.  "This aspect calls for more
investigation."  Sullivan et al., ESAIM M2AN 47(6):1657–1689 (2013),
[doi:10.1051/m2an/2013083](https://doi.org/10.1051/m2an/2013083), arXiv:1202.1928 `[abstract]`:
for Lipschitz functions with legacy data "the bounds are determined by just 2 out of 32 data
points, and the remainder carry no information"; "natural methods for selecting optimal (maximally
informative) next experiments".
*Comparison.*  This is Q3's definition.  What is not there: any theorem on the size of the
minimax width, on the gain from adaptivity, or on complexity.
**K12 [K] (neighbouring theories).**  Information-based complexity: adaptive information is no
better than twice for convex symmetric classes and can be much better for convex non-symmetric
ones `[search snippet]` (the identified sets of Q1 are convex and not symmetric; the theory
division's `prior_art/L7`, `L8` cover this literature).  Bayesian optimal experimental design
(expected information gain; goal-oriented variants): Huan, Jagalur, Marzouk, Acta Numerica 2024;
Zhong et al. 2026 `[abstract, via Consensus]`.  Partial identification as a decision problem:
Dominitz & Manski, Rev. Econ. Stud. 84(4):1583–1605 (2017),
[doi:10.1093/restud/rdx005](https://doi.org/10.1093/restud/rdx005) `[search snippet]` (minimax
regret allocation between more data and better data).
**K13 [K] (structural biology: empirical or average-case).**  *(PubMed abstracts unless stated.)*
"the quantity of independent information ... is larger when all metals are bound in the same
domain" — Luchinat, Nagulapalli, Parigi, Sgheri, J. Magn. Reson. 215 (2012) 85,
[doi:10.1016/j.jmr.2011.12.016](https://doi.org/10.1016/j.jmr.2011.12.016); of 1000 calmodulin
conformers, 396 have MaxOcc ≥ 25 % with the NMR data alone, 161 with SAXS added, 68 with DEER
added and 50 with both — Gigli et al. 2018 `[full text]`; "how much information is contained in these averaged data" answered by singular
values and synthetic recovery — Andrałojć et al., J. Biomol. NMR 62 (2015) 353,
[doi:10.1007/s10858-015-9951-6](https://doi.org/10.1007/s10858-015-9951-6)
`[full text via fetch tool]`; "the reduction of entropy due to the experimental constraints ...
provides a robust measure of the information content of the experimental data relative to the
simulated ensemble" — Leung et al. (COPER), JCTC 12 (2016) 383,
[doi:10.1021/acs.jctc.5b00759](https://doi.org/10.1021/acs.jctc.5b00759); design of FRET pairs
"to minimize the uncertainty" — Dimura et al., Nat. Commun. 11 (2020) 5394,
[doi:10.1038/s41467-020-19023-1](https://doi.org/10.1038/s41467-020-19023-1); DEER label choice —
Mittal & Shukla, J. Phys. Chem. B 121 (2017) 9761,
[doi:10.1021/acs.jpcb.7b04785](https://doi.org/10.1021/acs.jpcb.7b04785); SAXS: Shannon channels
`N_S = q_max D_max/π` (Moore 1980 `[search snippet]`; Konarev & Svergun, IUCrJ 2 (2015) 352,
[doi:10.1107/S2052252515005163](https://doi.org/10.1107/S2052252515005163)); "the information
content is not uniform and reaches its maximum in the intermediate q range" — Spill & Nilges,
PLoS One 12 (2017) e0177309,
[doi:10.1371/journal.pone.0177309](https://doi.org/10.1371/journal.pone.0177309); cryo-EM images:
representatives chosen "by maximizing mutual information between ensemble weights and images" —
Mattingly, Evans, Cossio, arXiv:2606.14449 `[abstract]`.  A PubMed query combining "experimental
design" with "conformational ensemble / ensemble refinement" and NMR/FRET/DEER/SAXS returned no
record (S44).
**What appears to be missing for Q3.**  Worst-case value of an averaged observable for an
identified set of a conformational ensemble (how `U − L` for a given `ψ` changes when `φ_{K+1}` is
added, uniformly over its possible outcomes); any theorem about it.  The formulation itself is
OUQ's and must be cited as such.

---

## 3. Numerics (checks of the statements compared above; not new results)

Purpose: to make sure that the formulas quoted from different literatures are the same object
before saying so.  Independent re-computation with my own code; no code of the cited papers was
used.

| id | what | sizes | result |
|---|---|---|---|
| N1 | primal LP for the largest mass at a point; hard-max dual; ray-shooting formula (Gardner–Longinetti–Sgheri Thm 3.8); conic dual `κ` (di Dio–Schmüdgen eq. 32) | 120 instances, `|X|` 12–59, 1–5 observables | all four agree to `1.1e-7` (bisection tolerance); true weight never exceeds the bound |
| N1 | `minOR(A) = 1 − maxOR(Aᶜ)` | 40 instances | agreement to `9e-15` |
| N2 | KL ball + moments: direct convex optimisation (SLSQP) against the dual of Christensen–Connault Prop. 2.1 | 12 instances × 2 radii, `|X|` 8–24, 1–2 moments | agreement to `4.9e-10`; at `ρ = 60` the dual equals the prior-free LP value to 5 digits |
| N3 | `μ_C ∝ e^{−u·dist(x,C)}`: marginals and entropy | simplex [7,3], RM(1,3) [8,4], simplex [15,4], RM(1,4) [16,5]; `u` = 1, 2, 4, 8 | all marginals on fewer than `d(C^⊥)` sites uniform to `1e-13`; those on `d(C^⊥)` sites deviate by `2–7e-2`; `H(μ_C) = ln|C| + H(ν)` to `1e-9`; `(H − n·h(p_u))/ln|C|` between 0.249 (`u = 1`) and 1.000 (`u = 8`) |
| N3b | noisy-codeword variant `X = Y ⊕ E` (K10(f)): single-site log-ratio, marginals, entropy | same four codes; `u` = 1, 2, 4 | `max|Δ ln m|/u ≤ 1.0000`; marginals on `d(C^⊥) − 1` sites uniform to `2e-14`, on `d(C^⊥)` sites not (`3e-3`–`1e-1`); `(H − n·h(p_u))/ln|C|` between 0.316 and 1.000, as proved |
| N4 | envelope cone ∩ moment constraints as an LP in the weights | 4 instances, `|X| = 14`, 2 moments, `ℓ¹`-type metric | interval nested in the moments-only and in the cone-only intervals; truth inside |

Entropy per site in N3 at `u = 4` (class minimum `h(p_u) = 0.0901`, uniform `ln 2 = 0.6931`):
0.3818, 0.4297, 0.2749, 0.3066 for the four codes.  **The sketch's "minimum entropy the class
allows" is therefore an asymptotic statement** (it needs `ln|C|/n → 0`); at every size that can be
enumerated the entropy per site of the code ensemble is two to four times the class minimum.

Re-run: `python3 experiments/science/ws_M/check_statements.py` (seed 20261125; about 2 min CPU,
6.5 min wall on the shared machine; output `check_statements.out`) and
`python3 experiments/science/ws_M/check_q2_decomposition.py` and
`python3 experiments/science/ws_M/check_q2_bsc_variant.py` (seconds each; outputs `*.out`).  Nothing else in this report rests on computation.

---

## 4. Prior art: matrix, vocabulary, reading list, search log

### 4.1 Matrix  (question × literature → known / partial / not found / n.a.)

Columns: **ER** maximum-entropy and Bayesian ensemble refinement; **MO** MaxOcc and other
extremal-ensemble work in NMR/SAXS; **GMP** generalised moment problems and OUQ; **PI** partial
identification; **DRO** divergence-ball robust optimisation and information-inequality UQ; **RB**
robust Bayes / imprecise probability; **KW** k-wise independence, entropy-from-marginals, inverse
statistical mechanics; **SC** scattering/FRET-specific identifiability.

| question | ER | MO | GMP | PI | DRO | RB | KW | SC |
|---|---|---|---|---|---|---|---|---|
| Q1a exact range of `∫ψdμ` given averages, no prior | not found (non-uniqueness acknowledged) | partial (`ψ` = indicator only) | **known** | **known** (sharp bounds, LP) | n.a. | **known** (fundamental theorem of prevision; LSIP) | n.a. | partial (prior-weighted `P(Rg | ⟨E⟩)`, not a range) |
| Q1b largest / smallest population of a state or region | not found | **known** (MAP, MaxOcc, maxOR, minOR; theorem for RDC) | **known** (maximal mass function, conic dual) | known in form | n.a. | known in form (upper/lower probability) | n.a. | counted analogue for shapes (AMBIMETER) |
| Q1c KL ball ∩ moment constraints, dual, `ρ → ∞` limit | partial (one point: MaxEnt; frontier: `S_KL`–`χ²` curve) | not found | partial | **known** (Christensen–Connault 2023) | **known** without data constraints; with expectation constraints: Glasserman–Xu `[unverified]` | partial | n.a. | not found |
| Q1d envelope / density-ratio class ∩ moment constraints | not found | not found | not found | partial (constant density-ratio bounds in sensitivity analysis, cited in `L5` P6; whether they carry moment constraints: from memory, not read here) | not found | not found (class itself: `L5` P6) | n.a. | not found |
| Q1e guaranteed numerical value (dual certificate, rigorous global optimisation or partition-function bound) | not found | not found (penalised NNLS, heuristic threshold) | partial (SDP hierarchies; OUQ uses heuristics) | partial (inference theory for estimated moments) | not found | partial (interval analysis in LSIP, `[search snippet]`) | n.a. | not found |
| Q2a order ≤ m energy identified by ≤ m marginals | used implicitly (MaxEnt form) | n.a. | n.a. | n.a. | n.a. | n.a. | **known** (exponential families; Griffiths–Ruelle; Henderson), hard to compute | n.a. |
| Q2b many ensembles share the low-order data | acknowledged, not quantified | **known** (5/25 tensor parameters; Carathéodory numbers) | **known** (brittleness; realizability) | n.a. | n.a. | known | **known** (XOR, codes) | **known** (Shannon channels; ⟨E⟩ vs Rg; pair-statistics degeneracy) |
| Q2c range of entropy given ≤ k marginals, unrestricted class | not found | not found | n.a. | n.a. | n.a. | n.a. | **known** (Albanna et al. k ≤ 3; Gavinsky–Pudlák, Bhangale–Potukuchi any k) | not found |
| Q2d the same inside Gibbs classes with bounded energy differences; reading for entropy proxies | not found | not found | n.a. | n.a. | not found | n.a. | partial: statement **not found**; ingredients known; blurred-code example in Arnese–Lacker 2026; lower bound from marginals of linear order for noise-smoothed measures in Samorodnitsky 2016 | not found (entropy meter is an empirical calibration) |
| Q3a minimax choice of the next averaged observable: formulation | not found | partial (empirical: MaxOcc falls as data are added) | **known** (OUQ eq. 2.8, campaigns) | partial (minimax-regret data collection) | not found | partial | n.a. | partial (Shannon channels; FRET/DEER label selection, average-case) |
| Q3b theorems (shrinkage, adaptivity, complexity) for identified sets of ensembles | not found | not found | not found in OUQ; general IBC results exist (`L7`, `L8`) | not found | not found | not found | n.a. | not found |

"Not found" means: not in the sources opened under S1–S50, compared statement by statement; it is
not a claim of novelty.  The cells I regard as most likely to be overturned by a specialist:
Q1c/DRO (Glasserman–Xu and the finance literature were not read), Q1e/RB (Betrò–Guglielmi not
read), Q2d/KW (the property-testing and pseudorandomness literature is large).

### 4.2 Vocabulary the division should adopt

| the division's term | moment theory / UQ | NMR–SAXS | econometrics / statistics | imprecise probability, OR | TCS / information theory |
|---|---|---|---|---|---|
| set of ensembles consistent with the data | representing measures of a moment sequence; admissible set `A` (OUQ) | "the infinite solutions"; underdetermined, ill-posed, degenerate | observationally equivalent distributions | credal set; ambiguity set | — |
| exact range `[L, U]` of `∫ψdμ` | optimal bounds; generalised Chebyshev bounds | (for populations) minOR, MaxOcc / maxOR | **identified set**, sharp bounds | lower/upper prevision, natural extension; worst-case expectation | — |
| largest population of a state | **maximal mass function** `ρ_s(x)`; Christoffel function | **MaxOcc**, MAP | sharp upper bound | upper probability | — |
| number of states needed | Carathéodory number; Richter/Tchakaloff | minimal ensemble, sparse ensemble selection | — | — | support size |
| prior neighbourhood | — | (reference ensemble, prior) | nonparametric neighbourhood of a parametric specification | φ-divergence ball; density-ratio class | — |
| KL radius from force-field error | — | "exchange rate" `θ`, gentle refinement (Köfinger–Hummer) | neighbourhood size `δ` | radius `ρ`, tolerance `η` | — |
| dual multiplier with a positivity check | positive functional `p ∈ Pos(A)`; LSIP | — | Lagrange multipliers; hard-max vs soft-max | pricing / separation oracle | — |
| low-order data do not fix the joint | brittleness; realizability | 5 / 25 independent parameters; virtual structure | partial identification | — | k-wise independence (uniformity), orthogonal array of strength k, dual distance; connected information |
| worst-case value of an experiment | most predictive experiment (minimax), campaign | "information content" (singular values, entropy reduction) | minimax regret; identification power | — | radius of information, adaption (IBC) |

Two practical points.  (1) The word "identifiability" is essentially absent from the
ensemble-refinement literature (PubMed query S38: 0 records); "underdetermined", "ill-posed",
"degenerate" are used.  A paper for that community should say "what the data determine, with
bounds" and name MaxOcc in the first paragraph.  (2) "Sharp" has a fixed meaning in partial
identification (the bound is attained by some admissible distribution); the MaxOcc literature
says "sharp bound from above" (Clarelli–Sgheri) in the same sense.

### 4.3 The five papers the coordinator must read in full before writing

1. **Christensen & Connault, "Counterfactual Sensitivity and Robustness", Econometrica 91(1):263–298
   (2023), arXiv:1904.00989** — it contains the Q1 theorem for the KL neighbourhood (Prop. 2.1),
   the `ρ → ∞` limit (Thm 2.1), the hard-max/soft-max remark, and an inference theory for
   estimated moments that the division would otherwise have to rebuild.
2. **Gardner, Longinetti, Sgheri, Inverse Problems 21 (2005) 879–898** (open copy at
   flore.unifi.it), together with §10 of di Dio & Schmüdgen, arXiv:1809.00584 — the theorem behind
   MaxOcc and its exact conic dual; the two are the same statement in two literatures that do not
   cite each other.
3. **Andrałojć, Luchinat, Parigi, Ravera, J. Phys. Chem. B 118 (2014) 10576** (reprinted in
   Andrałojć's thesis, flore.unifi.it 2158/1072773) — the two-sided identified set of a region
   population as it is actually computed and used on experimental data, with its tolerance
   convention; this is what an NMR referee will compare any new claim with.
4. **Owhadi, Scovel, Sullivan, McKerns, Ortiz, "Optimal Uncertainty Quantification", SIAM Review
   55 (2013) 271–345, arXiv:1009.0679** (§2.2 and §4) — the reduction theorems and the minimax
   definition of the most predictive experiment and of campaigns: Q3 is formulated there.
5. **Albanna, Hillar, Sohl-Dickstein, DeWeese, Entropy 19 (2017), arXiv:1209.3744** — "what are
   the possible entropies" given low-order statistics, with the same conclusion as the Q2 sketch
   for `k ≤ 3` in the unrestricted class, and the remark that a structural assumption restores a
   linear floor.
Also to be read, in this order, if time allows: Ravera, Sgheri, Parigi, Luchinat, PCCP 18 (2016)
5686 (the field's own assessment; I could not obtain the full text); Köfinger & Hummer, J. Chem.
Phys. 160 (2024) (how the refinement community sets the KL scale from force-field error); Bhangale
& Potukuchi, arXiv:1709.00752 with Gavinsky–Pudlák (entropy of k-wise independent variables);
Betrò & Guglielmi on numerical robust Bayes under generalised moment conditions (interval
analysis inside the semi-infinite LP).

### 4.4 Search log (condensed; the full log with every query string is `NOTES.md`, S1–S50)

| # | tool | query (abridged) | outcome |
|---|---|---|---|
| S1–S2 | PubMed | "maximum occurrence" + conformations + NMR/SAXS; Bertini/Luchinat/Parigi + MaxOcc/MAP/maxOR | 12 + 13 records: the MaxOcc corpus 2007–2021 |
| S3–S9 | web | Ravera 2016; Gardner–Longinetti–Sgheri; Sgheri papers; maxOR/minOR; MaxOcc + "linear programming" | open copies of GLS 2005, Gigli 2018, Andrałojć thesis; arXiv:0712.3777, 1602.05953 |
| S8 | PubMed | Andrałojć + Luchinat + regions / "information content" | JPCB 2014 (maxOR/minOR), J Biomol NMR 2015 |
| S10 | arXiv API | titles: OUQ, Christensen–Connault, Lam, Dupuis et al., Katsoulakis et al., Chowdhary–Dupuis, Birmpa et al., Breuer–Csiszár | 9 papers downloaded |
| S11–S14 | web | information inequalities + moment/experimental constraints; KL ball + moment constraints DRO; Glasserman–Xu; "maximum entropy" reweighting + bounds/range/worst-case | no molecular KL-ball-with-data work; Glasserman–Xu only as a record |
| S15 | arXiv API | ensemble refinement + identifiability/bounds (several phrasings) | nothing relevant (arXiv indexes this field poorly) |
| S16–S18 | arXiv API, web | entropy/marginals titles; k-wise independence + codes; Gibbs measure + k-wise uniform + low entropy | Albanna, Schneidman, Kuna–Lebowitz–Speer, Frommer–Hanke–Jansen, Jiao–Stillinger–Torquato, Gommes et al., Boutin–Kemper, Bhangale–Potukuchi, Bazzi, Arnese–Lacker; no direct hit for Q2d |
| S19–S23 | PubMed | SAXS information content; SES; FRET vs SAXS; Song–Chan | 15 records |
| S24–S25 | PubMed | entropy meter; Prompers–Brüschweiler; RDC parameter count; Jardetzky; Nikiforovich; NAMFIS | 14 records |
| S26–S30 | web, arXiv | fundamental theorem of prevision; robust Bayes generalised moments; Bertsimas–Popescu; Smith 1995; journal refs | records and abstracts |
| S31–S37 | web | repositories for Ravera 2016 and Medeiros Selegato 2021; dilation; adaption (IBC); Dominitz–Manski; LP bounds for conformer populations; provable partition functions × model uncertainty | two full texts unobtainable; no LP-bounds method in small-molecule NMR; no K*/DRO combination |
| S38 | PubMed | MIE/MIST; ensemble refinement + bounds; + identifiability | MIST bound; 2 irrelevant; 0 |
| S39–S43 | web | Chayes–Chayes–Lieb; Moore 1980; Christoffel function / maximal mass; Gordon 1968; density-ratio class + moment constraints | Schmüdgen / di Dio–Schmüdgen found and read; nothing for moment-constrained density-ratio classes |
| S44–S46 | PubMed, arXiv, web | experimental design for ensembles; inverse Ising hardness; PSAT column generation | Dimura 2020, Mittal–Shukla; Bresler–Gamarnik–Shah; Jaumard et al. 1991 |
| S47–S50 | Consensus | four semantic queries (bounds over all consistent ensembles; range of unmeasured observables; minimax experiment choice; entropy vs low-order marginals in Gibbs measures) | [1] Ravera et al. 2016 is the top hit for the first; OED surveys for the third; Arnese–Lacker and entropy-factorisation papers for the fourth |

Consensus hits used (as returned): [A critical assessment of methods to recover information from averaged data](https://consensus.app/papers/details/w:071ba0ad-8c19-44ce-9ec1-34a51a7e3724/?utm_source=claude_code) (Ravera et al., 2016, PCCP);
[Conformational Ensembles of an Intrinsically Disordered Protein Consistent with NMR, SAXS, and Single-Molecule FRET](https://consensus.app/papers/details/w:08a1c040-751d-4647-856f-c82c5cb99bef/?utm_source=claude_code) (Gomes et al., 2020, JACS);
[Quantitative Description of Intrinsically Disordered Proteins Using Single-Molecule FRET, NMR, and SAXS](https://consensus.app/papers/details/w:2cfb37d3-5db6-4deb-9b53-dce16e0af8bb/?utm_source=claude_code) (Naudi-Fabra et al., 2021, JACS);
[Optimal experimental design: Formulations and computations](https://consensus.app/papers/details/w:0f2bc6ee-2425-497b-9bb2-241a2e4f2852/?utm_source=claude_code) (Huan et al., 2024, Acta Numerica);
[Goal-Oriented Bayesian Optimal Experimental Design for Nonlinear Models Using Markov Chain Monte Carlo](https://consensus.app/papers/details/w:cc90102b-64d4-4728-961d-b7b90e726ee8/?utm_source=claude_code) (Zhong et al., 2026, SIAM/ASA JUQ);
[Entropic independence via sparse localization](https://consensus.app/papers/details/w:38ade3cd-3729-4a7d-a0e1-d8a88d8a6ebe/?utm_source=claude_code) (Jain et al., 2026, EJP);
[Approximate independence of typical marginals of high-dimensional probability measures](https://consensus.app/papers/details/w:033ad4bd-0629-443f-b176-f98dfda15338/?utm_source=claude_code) (Arnese et al., 2026, arXiv);
[Rapid Mixing of Global Markov Chains via Spectral Independence: The Unbounded Degree Case](https://consensus.app/papers/details/w:36b7fa1b-cfaa-485d-b6f1-3cffafb32eed/?utm_source=claude_code) (Blanca et al., 2026, Algorithmica).
Create or connect a free Consensus account to return more than 3 results per search in Claude Code.: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code

---

## 5. What I did not settle, and what I could not access

**Not accessed (stated per rule 5).**
* Full texts behind publisher walls or bot challenges: Ravera et al. 2016 (RSC: HTTP 403 for the
  author PDF and the HTML; repository records without file); Medeiros Selegato et al.,
  ChemPhysChem 22 (2021) 127; Bertini et al. 2007 and 2010 (JACS); Longinetti, Luchinat, Parigi,
  Sgheri, Inverse Problems 22 (2006) 1485 (cited for "at most 25 independent RDC"); Sgheri 2010
  (abstract paraphrase only); Glasserman–Xu 2014 and X. Xu's thesis (CORE: HTTP 403); Smith 1995;
  Bertsimas–Popescu 2005; Lad–Dickey–Rahman 1990 (abstract paraphrase only); Betrò–Ruggeri–Męczarski
  1994 and Betrò–Guglielmi; Schmüdgen 2015; Henderson 1974; Griffiths–Ruelle 1971;
  Chayes–Chayes–Lieb 1984 (Project Euclid returned an HTML shell); Gavinsky–Pudlák 2016;
  Alon–Babai–Itai 1986; Moore 1980; Seidenfeld–Wasserman 1993; Dominitz–Manski 2017; Gordon 1968;
  Jardetzky 1980 and Nikiforovich et al. 1987 (abstracts only); the journal versions of every
  arXiv paper cited.
* Truncated by the fetch tool at 100 000 characters (final part unread): PMC4782772 (Andrałojć et
  al. 2015), PMC5658725 (Song et al. 2017), PMC7071556 (Wand & Sharp 2018), PMC8921464 (Hou &
  Tochio 2022); for these and PMC6589165 I saw tool extracts, not the text.
* Tools: Europe PMC REST API timed out; the PubMed MCP full-text call returned empty for
  PMC5347631; the arXiv API answered multi-term abstract queries unreliably.
* Not searched at all: MathSciNet/zbMATH/Web of Science (so no forward-citation chasing of
  Gardner–Longinetti–Sgheri from the moment-problem side, nor of Schmüdgen from the applied side);
  Russian-language peptide-NMR literature of the 1980s (Nikiforovich's group published there);
  patents; theses other than two; the cryo-EM heterogeneity literature beyond one 2026 preprint;
  the quantum analogue (reduced density matrices, quantum codes); crystallographic ensemble
  refinement; hydrogen-exchange and mass-spectrometry data.

**Not settled.**
1. Whether Glasserman–Xu (2014) or the DRO literature already states the KL-ball dual with
   moment constraints before Christensen–Connault (2019/2023).  Attribution should say
   "see also" until someone reads them.
2. Whether Betrò–Guglielmi's interval-analysis algorithm delivers verified enclosures of the
   optimal value (which would make "certified dual of a moment problem" known in robust Bayes).
3. Whether any paper computes a minimum–maximum range of `⟨Rg⟩` (or another unmeasured
   observable) given FRET or SAXS averages.  Song et al. compute a conditional distribution; I
   did not read the final quarter of that paper nor its follow-ups.
4. Q2d: whether the lower bound `n·h(p_u) + Ω(k ln n)` holds for `k`-wise uniform members of the
   bounded-difference class (so that the code construction is optimal up to constants); whether
   `H(ν) ≤ n·h(p_u)` in K10(c) holds in general (**[C]**; true in 16 computed cases; not needed
   for the variant K10(f)); and the exact statement and hypotheses of Samorodnitsky's inequality
   (read as an abstract only), which decides at what order of marginals the entropy of a
   smoothed measure becomes constrained.
5. Whether the envelope cone with one moment constraint has a closed-form range for a single
   state, extending Theorem 11.12 of the theory report.
6. How the tolerance convention of MaxOcc (fit quality within 1.2–1.3 × the best fit) relates to a
   statistical confidence statement; the partial-identification literature has the tools
   (inference for projections of identified sets) and I did not open it beyond Molinari's review
   abstract (arXiv:2004.11751).

---

## 6. The three most promising next steps

1. **Replicate MaxOcc with certificates on public data, then add a prior.**  Take a published
   MaxOcc case with deposited restraints (calmodulin PCS/RDC; the pool can be regenerated),
   recompute maxOR/minOR as linear programmes with explicit dual solutions `(λ0, λ)`, report the
   duality gap and the dependence on the pool, and then show how the interval changes when the
   pool is weighted by a physical model and a KL radius is imposed (Christensen–Connault dual,
   with the radius set from an energy-error scale as in Köfinger–Hummer).  This is in scope
   (public fixed-sequence data, no experiment), speaks to an existing community in its own
   terms, and its novelty claim is narrow and defensible: *guaranteed* bounds, *general*
   observables, *with* a prior neighbourhood.
2. **State Q2 as one theorem with honest attribution, and test its physical reading.**
   Dichotomy: order `≤ m` ⇒ identified (textbook, hard to compute) versus bounded differences ⇒
   the entropy interval `[n·h(p_u) + O(k ln n), n ln 2]` is entirely compatible with uniform
   `≤ k`-marginals (ingredients: K9; three-line proof K10(f); Samorodnitsky's inequality as the
   complementary positive statement at linear order).  The scientific content is the
   reading: site-resolved averaged observables cannot bound conformational entropy without an
   assumption on the order or range of the energy; the entropy meter works to the extent that
   proteins satisfy such an assumption.  The decisive check is numerical and model-relative: on
   an exactly enumerable chain model of the engineering division, compute the range of entropy
   over ensembles sharing all single-site and pair marginals with the Boltzmann ensemble, within
   an envelope class of given constants.
3. **Pose Q3 inside the theory division's own framework.**  For the linear-in-features classes of
   §11.17 (pair-distance profiles), a SAXS curve is a linear functional of exactly those features.
   The worst-case value of `K` Shannon channels for an unmeasured linear functional of the
   profile is then a width problem of the kind already treated in §11.17 (distance to a span in a
   dual norm), with the experiment in the place of the evaluations.  This would give the first
   theorem on Q3 for ensembles, with OUQ's eq. (2.8) as the definition.

---

## 7. Requests (precise enough to be sent as they are)

**To the theory division.**
* T-M1.  Is weak duality for Q1 already a corollary of the machine-checked kernels?  Statement
  wanted: *for finite `X`, observables `φ: X → ℝ^K`, `ψ: X → ℝ`, data `m`, and any `(λ0, λ)` such
  that the minimisation kernel certifies `min_x [λ0 + λ·φ(x) − ψ(x)] ≥ 0`, every probability
  vector `μ` with `Σμφ = m` satisfies `Σμψ ≤ λ0 + λ·m`.*  If `φ, ψ` are pairwise tables in rotamer
  variables this is a certificate of the existing pairwise kernel (cf. Proposition 11.50).
  Please state whether a Lean declaration of this form exists or what is missing.
* T-M2.  The KL version needs a certified *upper* bound on a tilted log-partition function:
  `Σμψ ≤ η·ln Z_β(f − (ψ − λ·φ)/(βη)) − η·ln Z_β(f) + ηρ + λ·m` for all `μ` with `KL(μ‖μ0) ≤ ρ`,
  `Σμφ = m`.  Does the partition-function kernel (§3.4, §11.8) certify an upper bound on the
  first `ln Z` term and a lower bound on the second, for a tilt `(ψ − λ·φ)/(βη)` that is pairwise
  in the rotamer variables?  A yes/no with the name of the declaration suffices.
* T-M3.  For the envelope class of Theorem 11.12, is there a closed form for the range of a
  single Gibbs probability under one additional linear constraint `Σμφ = m`?  (L5 notes that the
  closed form is special to single states; with a constraint the extremal residual is presumably
  a two-piece McShane function.)
* T-M4.  Please check K10(a)–(c) of this report (three lines each) and say whether
  `H(ν) ≤ n·h(p_u)` for the coset-leader measure follows from results you already have.

**To the engineering division.**
* E-M1 (specification).  *Motivation*: measure how fast an identified set shrinks with
  scattering information on exactly enumerated chains.  *Formulation*: for a chain model with
  complete enumeration (`experiments/eng`, lattice and off-lattice), let `X` be the set of
  conformations, `μ0 ∝ e^{−βf}` the known part, `φ_k(x) = Σ_{p<q} sin(q_k r_pq)/(q_k r_pq)` the
  Debye intensity at `q_k = kπ/D_max`, `k = 1..K`, data `m = Σμ*φ` for a "true" ensemble `μ*`
  drawn from the envelope class.  Compute for `ψ ∈ {Rg², one contact indicator, end-to-end
  distance²}` the intervals `[L, U]` (a) with moments only, (b) with the envelope cone, (c) with a
  KL ball of radius `ρ ∈ {0.1, 1, 10}`, for `K = 0..12`.  *Inputs*: enumerations already produced
  (no new sampling).  *Outputs*: table of interval widths against `K`; dual solutions `(λ0, λ, η)`
  for each end; time and memory.  *Validation*: `μ*`'s value inside every interval; (a) ⊇ (b), (a)
  ⊇ (c); primal–dual gap below `1e-8`; agreement with `check_statements.py` on a 14-state toy
  instance.  *Stopping*: sizes up to the largest enumeration that fits an LP with `|X|` columns in
  6 GB; otherwise column generation with the existing minimiser as pricing oracle.  *Resources*:
  hours on 4 cores.
* E-M2.  For the same enumerations, the entropy range of step 2 of §6: minimum and maximum of
  `H(μ)` over ensembles in the envelope cone sharing all one- and two-site (torsion) marginals
  with `μ0`.  The maximum is a convex programme; the minimum is a concave minimisation over a
  polytope, so report vertex-enumeration results for small sizes and best-found values with
  certified lower bounds otherwise.

---

*Statement of independence.*  I read the sources listed, re-derived the three remarks marked
**[P]**, and re-computed N1–N4 with my own code (independent replication of the formulas, not of
any published data set).  I did not review or replicate the coordinator's theory beyond the
sketch printed in `M_brief.md`.
