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
exact conic dual (Schmüdgen 2015; di Dio–Schmüdgen 2018).  The two literatures do not cite each
other.  (iii) Adding a KL (φ-divergence) ball around a reference measure gives the dual
`inf_{η>0,λ} [η ln E_{μ0} e^{(ψ−λ·φ)/η} + ηρ + λ·m]`, with convergence to the prior-free sharp
bounds as `ρ → ∞`: **this is Proposition 2.1 and Theorem 2.1 of Christensen & Connault
(Econometrica 2023)**, in econometrics.  **Not found**: any of this for molecular ensembles with a
physical prior neighbourhood; general `ψ` in structural biology; dual certificates for the
numbers that are published (MaxOcc is computed by penalised least squares on a finite pool with
a heuristic misfit threshold); moment constraints on a density-ratio or metric ("envelope")
class; a KL-UQ bound evaluated with rigorous partition-function bounds.
**Q2 (non-identifiability).**  The positive half (interaction order `≤ m` ⇒ identified by
`≤ m`-marginals) is textbook (minimal exponential families; Griffiths–Ruelle; Henderson) and is
computationally hard in general (Bresler–Gamarnik–Shah).  The negative mechanism is also known:
`k`-wise independent distributions on linear codes of dual distance `> k` have entropy
`O(k log n)` (Alon–Babai–Itai lineage; exact entropy bounds: Gavinsky–Pudlák, Bhangale–Potukuchi),
and "the range of entropies consistent with means and pairwise correlations is almost the whole
interval, unless a structural assumption is added" is the published conclusion of Albanna et al.
(2017) for `k = 2, 3` in the unrestricted class.  **Not found**: the statement restricted to a
*Gibbs class with bounded single-site energy differences* (where the minimum entropy is
extensive), for every `k`, and its reading for single-site NMR proxies of entropy.  The
construction (a code-supported measure smoothed into a regular one) appeared three weeks ago in
a different theorem (Arnese–Lacker, arXiv:2611.07460).
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
considered equivalent".  None of these texts states a range, a bound or the set of all solutions.
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
The phrase "same observable averages, thus similar predictions" (Bonomi et al.) is precisely the
inference that an identified-set computation tests.

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
* General theorem of the same flavour in UQ: Owhadi, Scovel, Sullivan, "On the Brittleness of
  Bayesian Inference", SIAM Rev. 57(4):566–582 (2015),
  [doi:10.1137/130938633](https://doi.org/10.1137/130938633), arXiv:1308.6306 `[abstract]`: for
  models that "exactly capture an arbitrarily large number of finite-dimensional marginals of the
  data-generating distribution", optimal bounds on posterior values span the largest possible
  range (companion: Electron. J. Stat. 9 (2015) 1–79).

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
  BCH codes give support `O(n^{k/2})`; "Gavinsky and Pudlák prove ... entropy at least
  `log C(n, k/2)`"; Thm 1.1: `(k−1)`-wise independent unbiased bits have
  `H ≥ n − n·H(1/2 − sqrt((k/n)(1 − k/n))) − o(n)`.  (Gavinsky–Pudlák, Babai, Alon–Babai–Itai,
  Chor et al.: **not read**.)
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
*Literature coverage.*  (b) and the small-support mechanism: known (K9).  The conclusion "the
identified set of the entropy is almost the whole a-priori interval, and a structural assumption
rescues it": known for `k ≤ 3` in the unrestricted class (Albanna et al.), where the minimum
entropy is `O(log N)` and the low-entropy measures have tiny support.  **Not found**: the version
inside a class of everywhere-positive Gibbs measures with bounded energy differences, where the
a-priori interval is `[n·h(p_u), n·ln 2]` and both ends are met with uniform `≤ k`-marginals; (c);
the dichotomy with K7 stated in one theorem.
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
