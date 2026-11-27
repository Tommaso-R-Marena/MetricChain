# Workstream M — NOTES (prior art for the measurement side)

Started 2026-11-25.  Researcher: workstream M (independent).  Writable: this directory and
`docs/science/workstreams/SM_REPORT.md` only.  No git state changes.

Reading-level tags used throughout: `[full text]`, `[abstract]`, `[search snippet]`,
`[from memory — unverified]`.  Epistemic labels: [V] [P] [K] [N] [C] [H].

## Step log

### Step 0 (start) — orientation
* Read `docs/science/workstreams/COMMON.md` in full.
* Read `docs/science/workstreams/M_brief.md` in full.
* Created this directory and this file.
* Next: THEORY_REPORT §11.6 (Thm 11.12 + remark on weights), §11.13 (Thm 11.35), §11.17;
  `docs/prior_art/L5` items P5–P6; `docs/prior_art/L8`.

### Step 1 — internal reading (what the theory division already checked)
* THEORY_REPORT §11.6 read (lines 1741–1880).  Thm 11.12 (thermal contact, [V]): range of a
  single Gibbs probability over the envelope class is a closed interval, ends attained by
  `g = −d(x,·)` and `g = d(·,x)`; **remark on weights**: in `w = e^{−βg}` the class is the
  polyhedral cone `w(y) ≤ e^{βd(x,y)} w(x)`; robust Boltzmann averages of any observable are
  linear-fractional programmes with optima at polytrope vertices; closed form special to
  single states.  Thm 11.14 (transport–entropy duality, cites Gozlan–Léonard 2007,
  Bobkov–Houdré–Tetali 2006).
* §11.13 read (lines 2819–2890).  Thm 11.35 [P]: range of mean magnetisation over the cube
  class has half-width `½ tanh(u/2)`, and most of it is uncertifiable by evaluations.
  => The theory division already has an "a-priori range of a Boltzmann average over the
  envelope class" (no data).  Q1 adds *moment constraints from data* to this.
* §11.17 read (lines 3203–3526).  Thm 11.47 (linear-in-features classes; prior art: optimal
  recovery Smolyak/Micchelli–Rivlin; set-membership Milanese–Vicino; Soyster), Thm 11.48
  (pair-additive residual is linear in cumulative pair-distance profile; `d_P` = W1 between
  truncated squared-distance multisets), Prop 11.49–11.50.  Nothing about scattering or any
  experimental observable.  Henderson's theorem is "context only" there (L8), not read.
* L5 items P5–P6 (and P7) read in full; L8 read in full.  What they already checked:
  - density-ratio classes: DeRobertis–Hartigan 1981 `[abstract only there]`, Wasserman 1992
    `[abstract]`, Lavine 1991 `[abstract]`, Walley 1997 bounded-derivative model `[abstract]`,
    Smith–Rigat 2012 `[full, working paper]`, Sergeev–Schneider–Butkovič 2009 `[full]`,
    Kairouz–Oh–Viswanath `[full]`, Bordenabe et al. `[full]`, Zhao–Small–Bhattacharya 2019
    `[full]` (Charnes–Cooper), Rebeschini–van Handel `[full]`.
  - L5 verdict P6: "PARTIALLY KNOWN"; **nobody there looked at moment-constrained
    density-ratio classes, at data, at KL balls, at OUQ, or at structural-biology methods**.
  - L8: Henderson, Smolyak, Micchelli–Rivlin etc. "not read by anyone in this project".
* So my searches must not duplicate P5–P6 but must cover: moment constraints *added to* such
  classes; and everything on the experimental side.

### Plan of literature blocks (search log follows, numbered S1, S2, …)
A. MaxOcc / maxOR / extremal ensembles in NMR-SAXS (highest priority: closest to Q1).
B. MaxEnt / Bayesian ensemble refinement (statements about uniqueness, minimal perturbation).
C. Generalised moment problems, OUQ, Bertsimas–Popescu, Lasserre, Winkler, Rogosinski.
D. Partial identification (Manski, Tamer, Molchanov–Molinari, Kaido–Molinari–Stoye, …).
E. Divergence-ball DRO with moment constraints; information-inequality UQ (Dupuis et al.).
F. Robust Bayes density-ratio classes with moment constraints.
G. k-wise independence, entropy from marginals, inverse Ising/Potts, Henderson/CCL.
H. Scattering identifiability (homometry, Shannon channels, Boutin–Kemper).
I. Value of information / experimental design in the worst-case sense (Q3).

### Access check (tools)
* `curl` through the session proxy: arXiv API and arXiv PDFs reachable (downloaded
  arXiv:1009.0679 = OUQ, 90 pp.); Europe PMC REST timed out (60 s).  `pdftotext` available.
  => "[full text]" below means: PDF downloaded, text extracted with pdftotext, and the
  passages quoted were read by me in the extracted text.  "[full text via fetch tool]" means
  a page-fetching tool (small model) read the page and returned extracts/quotes to me; I
  did not see the raw text.  PubMed MCP `get_full_text_article` returned empty for PMC5347631.

## Search log

**S1** PubMed: `"maximum occurrence" AND (conformations OR conformational) AND (NMR OR SAXS OR paramagnetic)` → 12 hits.
**S2** PubMed: `(Bertini I OR Luchinat C OR Parigi G)[Author] AND (MaxOcc OR "maximum allowed probability" OR "maximum occurrence" OR maxOR OR "minimum occurrence")` → 13 hits.
Abstracts read (all `[abstract]`, PubMed):
* Bertini, Gupta, Luchinat, Parigi, Peana, Sgheri, Yuan, JACS 129:12786 (2007),
  doi:10.1021/ja0726613 — "maximum allowed probabilities (MAPs) of conformations in protein
  domains not rigidly connected"; "innovative analytical/computational approach"; pcs + rdc
  from lanthanides in calmodulin.  **First MAP paper; Sgheri (mathematician, IAC-CNR) is a
  co-author → look for the Inverse Problems papers behind it.**
* Bertini, Giachetti, Luchinat, Parigi, Petoukhov, Pierattelli, Ravera, Svergun, JACS
  132:13553 (2010), doi:10.1021/ja1063923 — "The concept of maximum occurrence (MO), i.e.,
  the maximum percent of time that flexible proteins can spend in any given conformation, is
  introduced, and a rigorous method is developed to extensively sample the conformational
  space and to construct MO maps from experimental data" (SAXS + pcs + rdc); crystal
  conformations of CaM have MO 5 % and 15 %, extended ones up to 35 %.
* Bertini, Ferella, Luchinat, Parigi, Petoukhov, Ravera, Rosato, Svergun, J Biomol NMR
  53:271 (2012), doi:10.1007/s10858-012-9638-1 (MaxOcc web portal) — **verbatim**: "Whatever
  the real ensemble of conformations sampled by a protein, the weight of any conformation
  cannot exceed the calculated corresponding Maximum Occurrence value."  (= an upper end of
  an identified set for a point mass, prior-free.)
* Luchinat, Nagulapalli, Parigi, Sgheri, J Magn Reson 215:85 (2012),
  doi:10.1016/j.jmr.2011.12.016 — MO = "the maximum weight that such conformations can have
  independently of the real structural ensemble, in agreement with the provided restraints";
  "the quantity of independent information ... is larger when all metals are bound in the
  same domain" (a **design** statement → Q3).
* Dasgupta et al., J Biomol NMR 51:253 (2011), doi:10.1007/s10858-011-9532-2 — adding a
  lanthanide tag on the second domain "reduces the MO of the conformations to different
  extents" (value of an added data set, empirical → Q3).
* Gigli et al., PCCP 20:27429 (2018), doi:10.1039/c8cp06195e — **verbatim**: "Since the
  available conformations largely outnumber the (independent) available experimental data,
  the latter can be equally well reproduced by a variety of ensembles.  We have proposed the
  Maximum Occurrence (MaxOcc) approach to provide an upper bound of the statistical weight of
  each conformation.  This method is expected to converge towards the true statistical
  weights by increasing the number of independent experimental datasets."; DEER data "impose
  a sizeable reduction of the conformational space described by high MaxOcc conformations"
  (→ Q3, empirical).
* Andrałojć, Hiruma, Liu, Ravera, Nojiri, Parigi, Luchinat, Ubbink, PNAS 114:E1840 (2017),
  doi:10.1073/pnas.1616813114 — "Maximum Occurrence of Regions methodology" (maxOR); "the
  location and maximal spatial extent of the additional states needed to fully explain the
  NMR data"; then "under the assumption of sparsity".
* Andrałojć, Ravera, Salmon, Parigi, Al-Hashimi, Luchinat, PCCP 18:5743 (2016),
  doi:10.1039/c5cp03993b (PMC6589165) — MaxOcc on HIV-1 TAR RNA from 4 RDC sets, compared
  with MD and sample-and-select.
* Ravera, Sgheri, Parigi, Luchinat, PCCP 18:5686 (2016), doi:10.1039/c5cp04077a — "A
  critical assessment of methods to recover information from averaged data": two families
  (maximum entropy; restricted number of conformations); "The upper limits for
  conformational probabilities (MaxOcc) can also be calculated".  **Must read in full.**
* Medeiros Selegato, Bracco, Giannelli, Parigi, Luchinat, Sgheri, Ravera, ChemPhysChem
  22:127 (2021), doi:10.1002/cphc.202000714 — compares Maximum Entropy, Maximum Parsimony,
  Maximum Occurrence on the same data.
* Leung, Bignucolo, Aregger, Dames, Mazur, Bernèche, Grzesiek, JCTC 12:383 (2016),
  doi:10.1021/acs.jctc.5b00759 (COPER) — MaxEnt reweighting as convex optimisation with a
  unique global solution; **"the reduction of entropy due to the experimental constraints
  ... provides a robust measure of the information content of the experimental data relative
  to the simulated ensemble"** (→ Q3, average-case notion); notes "the maximum occurrence
  method" also has convex targets and constraints.
* Carlon et al., Biophys J 117:1948 (2019); Cerofolini et al., JBC 288:30659 (2013)
  (MMP-1: crystal conformation "MO ~20 %, which represents the upper limit for the presence
  of this conformation in the ensemble"); Nagulapalli et al., Structure 20:522 (2012);
  Fields 2014 (review) — applications.
Consequence: **the special case ψ = indicator of one conformation (or of a region), prior-free
(no KL ball / envelope), upper end only (later also "minOR"), is an established method in
paramagnetic NMR/SAXS since 2007.**  To check in full text: how it is computed (exact LP or
heuristic minimisation?), whether exactness/duality/certificates are stated, whether a prior
appears, whether lower bounds and general ψ appear.

**S3** Web: `Ravera Sgheri Parigi Luchinat "A critical assessment of methods to recover information from averaged data" PCCP 2016 pdf` → RSC author-version link (curl got HTTP 403; to try with fetch tool).
**S4** Web: `Gardner Longinetti Sgheri "Reconstruction of orientations of a moving protein domain from paramagnetic data" Inverse Problems 2005` → open copy at flore.unifi.it (downloaded), plus arXiv:0712.3777 (Longinetti–Sgheri–Sottile) and arXiv:1602.05953 (Clarelli–Sgheri).
**S5** Web: `Sgheri "maximal probability" orientations ... "most favoured orientations"` → nothing new (Longinetti–Luchinat–Parigi–Sgheri 2006 not located yet).

#### Read in full text (pdftotext, passages read by me)
* **Gardner, Longinetti, Sgheri, Inverse Problems 21 (2005) 879–898**, doi:10.1088/0266-5611/21/3/006
  `[full text: abstract, §1, §3 (Lemma 3.2, Thm 3.3, Cor 3.4, Thm 3.5, Thm 3.8 with proof), §4 (Prop 4.5, Thm 4.6, Cor 4.7), §7]`.
  Setting: unknown probability measure `p` on SO(3); data = mean paramagnetic tensor
  `χ̄ = ∫ R*χR dp(R)` (5 numbers per metal ion; RDCs are linear in it).  Statements:
  - "knowledge of the five distinct entries of the symmetric matrix χ̄ does not allow exact
    reconstruction of the probability measure p" (p. 881).
  - Thm 3.3: the set `V` of attainable mean tensors (= convex hull of the orbit) is the set of
    symmetric traceless matrices with eigenvalues in `[μ_min, μ_max]`.  Thm 3.5: every mean
    tensor is realised by **at most three rotations** (Carathéodory number 3; minimal).
  - **Thm 3.8 ("an optimal estimate")**: `p_max(R0) = sup{0 ≤ t < 1 : (χ̄ − t R0*χ_d R0)/(1−t) ∈ V}`
    — the *exact* largest mass any measure consistent with the data can put on the
    orientation `R0`, as a ray-shooting (gauge) formula in the moment set.  Thm 4.6: same for
    a compatible pair of tensors (two metals) under "assumption A"; Thm 4.2: ≤ 10 rotations
    suffice; Cor 4.7: `p_max ≤ min_k` single-metal bound.  "The value p_max is very hard to
    compute, because it is not easy to check whether a given pair ... belongs to V^{1,2}."
  - §7: in practice p_max is found by a **non-convex fit** (10 rotations with free
    probabilities, simulated annealing, bisection on p0) — "a reasonable estimate (from
    below) of p_max".  The theorem is exact; the computation is heuristic.
  - Uses the Curto–Fialkow quadratic complex moment problem for the coaxial case — i.e. the
    authors themselves place the question inside the moment-problem literature.
* **Longinetti, Sgheri, Sottile, Discrete Comput. Geom. 43 (2010) 54–77**, arXiv:0712.3777
  `[full text: abstract, introduction, §1 (to eq. 1.3 and the paragraph after)]`.  Facial
  structure and Carathéodory number (≤ 8) of the convex hull of an SO(3)-orbit of a pair of
  tensors.  Verbatim: "The availability of N distinct mean susceptibility tensors ... increases
  the information about p for N up to 5 ... However, even the exact knowledge of 5 mean tensors
  (i.e. 25 real numbers) does not allow the exact reconstruction of the probability measure p."
  and "define p_max(R) as the maximal fraction of time that the C-terminal can stay in a
  particular orientation R, yet still produce the measured mean tensors."  Cites [12] =
  Longinetti, Luchinat, Parigi, Sgheri (Inverse Problems 2006) for the geometric algorithm.
* **Clarelli, Sgheri, arXiv:1602.05953 (2016)** `[full text: §1–§3.4]`.  Verbatim: "The
  recovery of this probability distribution is an under-determined ill-posed problem ...";
  "there are two limit cases for the solutions" (MEP/Kullback–Leibler vs MAP); **"The Maximal
  Allowable Probability (MAP) is the largest weight of a given state in a probability
  distribution which is a solution.  As a function of the state, the MAP is not a solution but
  a sharp bound from above."**; "the rigorous mathematical definition of the MAP has been given
  in [14 = Gardner et al.]"; Prop 2.2: "The maximal number of independent mean RDC measurements
  is 25"; Prop 2.1: at most 5 independent metal ions; Prop 3.1: by Carathéodory every data
  vector is realised by ≤ n_meas + 1 conformers; §3.2–3.3: `p_max` by ray-shooting to the
  boundary of the convex moment set `V`, found by an iterative "simplex algorithm" that
  replaces vertices by conformers lying beyond the current supporting hyperplane.
  => **the geometry is exactly the generalised moment problem (moment set, Carathéodory
  reduction, supporting hyperplane = dual multiplier, finding a conformer beyond the hyperplane
  = the "pricing" global optimisation `max_x λ·φ(x)`), but no LP duality, no certificate of
  optimality and no prior measure are stated.**

#### Vocabulary note (to verify): the "maximal mass at a point compatible with given moments"
is the classical Christoffel-function / Chebyshev–Markov–Stieltjes object of the truncated
moment problem (`[from memory — unverified]`; search below).

**S6** Web: `flore.unifi.it "critical assessment of methods to recover information from averaged data"` → nothing.  Ravera et al. PCCP 2016 full text NOT accessed (RSC author PDF: HTTP 403 for curl and for the fetch tool).  `[abstract only]`.
**S7** Web (extended): `"maximum occurrence" OR "MaxOcc" ... "linear programming" OR "convex optimization" OR "upper bound"` → flore copy of Gigli et al. 2018; PMC8921464 (review of anisotropic paramagnetic restraints), PMC7018990.
**S8** PubMed: `Andralojc W[Author] AND Luchinat C[Author] AND (regions OR "information content")` → PMID 25144917 (JPCB 2014, maxOR/minOR), 26044033 (J Biomol NMR 2015, information content).
**S9** Web: three searches for the JPCB 2014 paper, Longinetti–Luchinat–Parigi–Sgheri 2006 and Sgheri 2010 → flore copy of W. Andrałojć's PhD thesis (Univ. Florence) which reprints the JPCB 2014 article; IAC-CNR abstract page for "Conformational freedom of proteins and the maximal probability of sets of orientations" (Inverse Problems 2010); the 2006 paper only as a reference (Inverse Probl. 22(4), 1485–1502).

#### Read
* **Gigli et al., PCCP 20 (2018) 27429** `[full text, author version from flore.unifi.it; read intro, calculation section, results paragraph, conclusions]`.
  Verbatim: "Ensemble reconstruction is an ill-posed inverse problem: infinite different ensembles
  can reproduce the experimental results equally well."; MaxOcc "provides an upper bound of the
  conformation's statistical weight and converges (decreases) towards the true statistical
  weight by increasing the number of independent experimental restraints.  As such the MaxOcc
  method does not yield a single ensemble solution to the problem."  **Computation (their
  eq. 1): `argmin_w [‖Pw − d‖² + ξ1(‖w‖₁ − 1)² − ξ2 w_c]`, `w ≥ 0`, multipliers "adjusted by an
  L-curve-like approach"** — a penalised non-negative least-squares problem on a finite pool
  (1000 conformers here); not an LP with a certified dual; the "bound" depends on the
  misfit threshold.  Table 2: number of conformers (of 1000) with MaxOcc ≥ 25 % drops from 396
  (NMR only) when DEER/SAXS are added (→ empirical value of information).
* **Andrałojć, Ravera, Salmon, Parigi, Al-Hashimi, Luchinat, PCCP 18 (2016) 5743** (PMC6589165)
  `[full text via fetch tool; quotes ≤125 chars as returned]`: MaxOcc computed by penalised
  NNLS with fixed weight of the conformer, pool of 37 005 inter-helical orientations (5° grid),
  target Q-factor, threshold "20% higher than the lowest Q"; "recovering an ensemble from
  experimental data remains an under-determined problem"; a conformer "whose high MaxOcc value
  arises from inherent degeneracy of the RDC data"; no lower bounds, no maximum entropy.
* **Andrałojć, Berlin, Fushman, Luchinat, Parigi, Ravera, Sgheri, J Biomol NMR 62 (2015) 353**
  (PMC4782772) `[abstract; full text via fetch tool, first 100 000 of 170 219 characters]`:
  "The question addressed here is how much information is contained in these averaged data."
  Information content is operational: singular-value spectrum of the prediction matrix ("directly
  provides an upper bound on the number of independent conformers we can hope to extract"),
  rank 10 for steric-alignment RDCs with two domains, rank 5 for paramagnetic RDCs per metal,
  PCS not low-rank; column correlations; recovery error in synthetic tests; SES vs MaxOcc/MaxOR.
  Recovering weights "is an ill-posed problem, having an infinite number of solutions".  **No
  theorem on how much an added observable shrinks the bounds.**
* **Andrałojć, Luchinat, Parigi, Ravera, J. Phys. Chem. B 118 (2014) 10576**,
  doi:10.1021/jp504820w `[abstract (PubMed); full text of Introduction, Methods, start of
  Results as reprinted in W. Andrałojć's PhD thesis, flore.unifi.it handle 2158/1072773]`.
  Verbatim: "The method explores subregions of the conformational space and provides both upper
  and lower bounds of probability for the system to be in each subregion."; "it is possible to
  calculate both the upper and lower occurrence limits for that region (maxOR and minOR) as the
  largest and smallest weight, respectively, that all conformations belonging to such region
  must have to provide averaged data in agreement with the experimental data, once
  complemented by other conformations outside this region"; **"the minimum occurrence of a
  region (minOR) can be immediately obtained from the difference between 1 and the maxOR of the
  complementary region"**; "ill-conditioned and ill-posed inverse problems and, as such, present
  an infinite number of solutions".  Computation (their eq. 3): regularised NNLS with the
  region's total weight fixed, pool of M = 50 000 RanCh conformers, 194 PCS + 134 RDC, bound =
  largest/smallest fixed weight with Q ≤ 1.2 × best Q.
* **W. Andrałojć, PhD thesis (Univ. Florence)** `[full text of §1.2–1.4, §2.4]`: "an infinite
  number of conformational ensembles, often not having a single structure in common, can
  reproduce the gathered ensemble averaged data with similar quality and there is no way to
  distinguish the actually sampled ensemble from the other ones"; MaxOcc "constitutes an upper
  bound that the experimental data impose on the weight of that structure in the real
  conformational ensemble.  The Maximum Occurrence values would converge to the actual weights
  in the limiting case of sufficiently many independent observables (and no experimental
  noise)"; MaxOR "one can ... quantify the smallest amount of mobility that has to be present in
  the system in order to explain the experimental observations"; with PRE data a region near
  the probe has minOR > 0.

**Interim verdict for Q1 × structural biology (to be refined):** the two-sided identified set
`[minOR, MaxOR]` of the probability of a *region* (ψ = indicator), over all ensembles on a finite
pool reproducing the averaged data within a misfit threshold, exists as a named, published
method (2007 MAP → 2010 MO → 2012 MaxOcc portal → 2014 maxOR/minOR → 2017 PNAS application),
with a rigorous mathematical core for the RDC case (Gardner–Longinetti–Sgheri 2005, Thm 3.8/4.6).
Absent there (in what I read): a prior measure / KL ball / density-ratio neighbourhood; general
observables ψ; LP duality, dual certificates or any guarantee for the numerical value; error
model beyond a χ²/Q threshold; continuous spaces except through the convex-hull geometry.

### Step 3 — OUQ and divergence-ball literatures (arXiv full texts)
**S10** arXiv API (title searches) → IDs: 1009.0679 (OUQ), 1904.00989 (Christensen–Connault),
1303.0326 (Lam), 1503.05136 (Dupuis–Katsoulakis–Pantazis–Plecháč), 1605.04184 (Katsoulakis–
Rey-Bellet–Wang), 1706.10260 (Gourgoulias et al.), 1103.1861 (Chowdhary–Dupuis), 2107.08179
(Birmpa–Feng–Katsoulakis–Rey-Bellet), 1301.4832 (Breuer–Csiszár).  Title searches for
Glasserman–Xu "Robust risk measurement and model risk" gave no arXiv hit.

* **Owhadi, Scovel, Sullivan, McKerns, Ortiz, "Optimal Uncertainty Quantification"**,
  arXiv:1009.0679v3 (published SIAM Review 55 (2013) 271–345 — journal version not read)
  `[full text: abstract, §2.2 "Experimental design and selection of the most decisive
  experiment", "Selection of the most predictive experiment", "Planning of campaigns of
  experiments", Example 2.5; §4 Theorem 4.1 and Remarks 4.2–4.3]`.
  - Optimal bounds = values of optimisation problems over all scenarios (function, measure)
    compatible with the information set A.
  - Thm 4.1 (reduction): with n' generalised-moment constraints on the product space and n_i on
    each factor, sup of `E_μ[r]` over the moment class is attained on products of convex
    combinations of ≤ n_i + n' + 1 Dirac masses (via Winkler; von Weizsäcker–Winkler; Karr for
    the compact case).  Remark 4.3: extends to sets of measures with known extreme points
    (Dynkin): invariant measures, stationary distributions, ...
  - **Experiment selection (their eq. 2.8), verbatim**: "An experiment E* that is most
    predictive, even in the worst case, is defined by a minmax criterion: we seek
    `E* ∈ argmin_{experiments E} sup_{outcomes c} ( U(A_{E,c}) − L(A_{E,c}) )`"; experiments are
    functionals `Φ_i(G, P)` such as `E_P[G]` or `P[X ∈ A]`; "we identify as the optimal next
    experiment the one that is most informative in the minimax sense"; "Planning of campaigns
    of experiments ... a min max game 'played against the Universe'"; Example 2.5 chooses
    sequentially among measuring the mean or variance of three inputs.
  => **Q3 in the worst-case / set-membership sense is formulated, named and illustrated in OUQ
  (2010/2013).**  No structure theorem (e.g. on adaptivity, on rates of shrinkage) is given
  there; "This aspect calls for more investigation".

* **Christensen & Connault, "Counterfactual Sensitivity and Robustness"**, arXiv:1904.00989v4
  (Econometrica 2023 — journal version not read) `[full text: abstract, §1, §2.2, Assumption Φ,
  Prop 2.1, eqs (13)–(16), Thm 2.1, Remark 2.7, Appendix B Lemmas B.1–B.3]`.
  - Object: `κ̄_δ = sup { E_F[k] : D_φ(F‖F*) ≤ δ, E_F[g_1] ≤ P_1, E_F[g_2] = P_2, ... }` and the
    infimum — the exact range of an expectation over a φ-divergence ball around a reference
    distribution intersected with finitely many moment (in)equalities.
  - **Prop 2.1 (dual)**: `K̄_δ = inf_{η>0, ζ, λ} η E_{F*}[φ*((k − ζ − λ'g)/η)] + ηδ + ζ + λ'P`; for
    KL: `inf_{η>0, λ} η log E_{F*} e^{(k − λ'g)/η} + ηδ + λ'P`; the value is ∓∞ iff no
    distribution in the ball satisfies the moments.  Eq. (15)–(16): minimum divergence subject
    to the moments (I-projection) and its dual.
  - **Thm 2.1**: as δ → ∞ the bounds converge to "the sharp nonparametric bounds".
  - **Lemma B.3 / Remark 2.7**: the nonparametric bound has the dual
    `inf_λ ( ess sup_u (k(u) − λ'g(u)) + λ'P )`, "min-max and max-min problems which involve an
    inner optimization over u ... setting δ < ∞ replaces a 'hard-max' (an optimization over u)
    with a 'soft-max' (a convex expectation)".
  => **This is the Q1 skeleton for the KL-ball neighbourhood, including the hard-max (global
  optimisation) dual of the prior-free problem.**  Context: latent-variable distributions in
  structural econometric models; nothing molecular; no certified evaluation of the soft-max.

* **Breuer & Csiszár, "Measuring distribution model risk"**, arXiv:1301.4832v1 (Math. Finance
  2016 — not read) `[abstract; §"Relation of the model risk problem and the moment problem"]`:
  worst-case expected loss over relative-entropy / Bregman / f-divergence balls, explicit worst
  case distribution (exponential family), linked to minimising entropy functionals under a
  moment constraint (Csiszár–Matúš 2012).  No additional data constraints in what I read.
* **Chowdhary & Dupuis**, arXiv:1103.1861v2 (ESAIM M2AN 47 (2013) 635) `[abstract, list of
  results]`: "explicit bounds on standard performance measures ... over families of
  distributions whose distance from a nominal distribution is measured by relative entropy",
  via the duality between risk-sensitive integrals and relative entropy.
* **Gourgoulias, Katsoulakis, Rey-Bellet, Wang**, arXiv:1706.10260v1 (IEEE Trans. IT 2020 — not
  read) `[abstract; Thm 1–2 statements and surrounding text]`: goal-oriented divergence bounds
  on `E_Q f − E_P f` in terms of `R(Q‖P)` and the MGF under `P`; Thm 2: tight on
  `Q_η = {Q : R(Q‖P) ≤ η²}`, attained by exponentially tilted measures `P^c`.
* **Katsoulakis, Rey-Bellet, Wang**, arXiv:1605.04184v1 (J. Comput. Phys. 2017 — not read)
  `[abstract]`: scalable information inequalities for high-dimensional models; "robust
  uncertainty quantification bounds for phase diagrams in statistical mechanics models".
* **Birmpa, Feng, Katsoulakis, Rey-Bellet**, arXiv:2107.08179v1 `[abstract; grep for
  "constraint"]`: KL ambiguity sets on components of Bayesian networks, "correctability";
  physico-chemical examples; the only constraints are KL radii per conditional — **no
  ensemble-average (moment) constraints from experiment in the ambiguity set**.
  => In the Dupuis–Katsoulakis line as far as read: KL (and Rényi) balls, tightness, scalability,
  Gibbs measures — yes; adding experimental moment constraints to the ball, or evaluating the
  tilted partition function with *rigorous* bounds — not seen (to be searched further).

**S11** Web (extended): `Katsoulakis Rey-Bellet Dupuis "information inequalities" ... "moment constraints" OR "experimental data" ...` → only the group's known papers (1605.04184, 1911.09580 rare events / Rényi, 1812.05174 Markov processes, 1906.09282 path space, 1708.03718 sparse data in random PDE, 1805.06917); **no hit combining the KL ball with experimental moment constraints**.
**S12** Web (extended): `"Kullback-Leibler" ball "moment constraints" distributionally robust "worst-case expectation" dual "exponential tilting" ...` → Hu–Hong (Optimization Online 2012/11/3677), DRO survey arXiv:2411.02549, conic KL-DRO arXiv:2007.05966; snippets do not show the combination.
**S13** Web: `Glasserman Xu "Robust risk measurement and model risk" ... constraints on expectations` → Quantitative Finance 14(1):29–58 (2014) confirmed (RePEc); Xingbo Xu's Columbia PhD thesis (2013) lists a section "Incorporating Expectation Constraints" (§2.3.2).  Thesis PDF on CORE: HTTP 403.  **Glasserman–Xu: `[search snippet]` only; the claim that they add expectation constraints to the relative-entropy worst case rests on the thesis table of contents + my memory.**
**S14** Web (extended): `"maximum entropy" reweighting ensemble "bounds" OR "range" OR "interval" ... "worst-case" OR "extremal" OR "robust" Kullback-Leibler constraint` → MaxEnt reviews only (Cesari–Reißer–Bussi; Bottaro et al. BME; Pitera–Chodera); **no "range over all consistent ensembles within a KL ball" in molecular simulation** in the snippets; found arXiv:2606.14449 (cryo-EM, see below).
**S15** arXiv API: titles of BioEn / metainference; abstract searches `"ensemble refinement" AND reweighting`, `"ensemble-averaged" AND "conformational ensemble" AND (underdetermined OR ...)`, `"conformational ensembles" AND experimental AND bounds AND "consistent with"` → only 2212.05320 (cryo-EM reweighting), 2609.27236 (Raddi–Voelz 2026, generative MSMs with restraints), 2311.08076.  arXiv indexes this literature poorly; rely on PubMed/web.

#### Read
* **Hummer & Köfinger, J. Chem. Phys. 143 (2015) 243150**, arXiv:1509.04447v2 `[full text:
  abstract, conclusions; grep of whole text for unique/underdetermined/bound/identif]`: BioEn =
  maximise a posterior functional over distributions (`−θ·S_KL − χ²/2`); the confidence
  parameter θ; "From plots of S_KL against χ² one can make an educated choice"; minimal-ensemble
  refinement is "an orthogonal refinement approach" whose relation "is not well understood".
  **No statement about the set of all consistent ensembles or about bounds.**  Note for the
  division: the BioEn `S_KL`–`χ²` curve is exactly the feasibility frontier of
  "KL ball ∩ data misfit ≤ c": the identified set is non-empty iff the pair (ρ, c) lies above it.
* **Cesari, Reißer, Bussi, Computation 6 (2018) 15**, arXiv:1801.05247 `[full text: intro,
  discussion; grep as above]`: "by design, the maximum entropy principle provides a
  distribution that, among those satisfying the experimental constraints, is as close as
  possible to the prior distribution ... different priors are in principle expected to lead to
  different posteriors".  No bounds.
* **Bonomi, Camilloni, Cavalli, Vendruscolo, Sci. Adv. 2 (2016) e1501177**, arXiv:1509.05684
  `[grep of full text only]`: no occurrence of unique/underdetermined/degenerate/bound in the
  senses searched.
* **Mattingly, Evans, Cossio, arXiv:2606.14449 (June 2026)** `[abstract + first page]`:
  cryo-EM *single-particle images* (not ensemble averages); "because images are indirect
  measurements, they limit which features of an underlying landscape are statistically
  identifiable"; choose representative conformations "by maximizing mutual information between
  ensemble weights and images"; "the measurement process induces a maximally learnable coarse
  graining of conformation space".  Average-case (Bayesian, mutual information) identifiability /
  design of the discretisation; adjacent to Q3, different data type.

### Step 4 — Q2 literatures: entropy vs marginals, k-wise independence
**S16** arXiv API (title searches) → 1209.3744 (Albanna et al.), physics/0307072 (Schneidman et al.), math-ph/0612075 and 0910.1710 (Kuna–Lebowitz–Speer), 1903.03317 (Frommer–Hanke–Jansen), 0908.1366 / 1007.1374 (Jiao–Stillinger–Torquato I/II), 1205.3382 (Gommes–Jiao–Torquato), math/0304192 (Boutin–Kemper), 1303.3235 (Kovačević et al.).  All downloaded.
**S17** Web: `"k-wise independent" OR "k-wise uniform" ... "dual distance" ... "orthogonal array" ... Alon Babai Itai BCH` → arXiv:1709.00752 (Bhangale–Potukuchi), 1707.00552 (Bazzi), 1806.03569 (O'Donnell–Zhao), 2405.08787 (Harvey–Sahami).
**S18** Web (extended): `Gibbs measure "k-wise independent" OR "k-wise uniform" marginals "low entropy" OR "minimum entropy" Markov random field bounded interaction ... code "dual distance"` → **no direct hit**; adjacent: arXiv:2611.07460 (Arnese–Lacker, 5 Nov 2026), propagation-of-chaos papers.

#### Read
* **Albanna, Hillar, Sohl-Dickstein, DeWeese, Entropy 19 (2017) 427**, arXiv:1209.3744v4
  `[full text: abstract, §1, §2 Results (eqs 1–9), discussion paragraphs]`.  Verbatim: "the full
  space of probability distributions consistent with these constraints has not been explored";
  "Our question is: Given a set of observed mean firing rates and pairwise correlations between
  neurons, what are the possible entropies for the system?"; "The range of possible entropies
  for any given set of constraints is the gap (S_n − S̃_n) ... for many cases, the gap grows
  linearly with the system size N, up to a logarithmic correction"; bounds
  `log2(N/(1+(N−1)ᾱ)) ≤ S̃_2 ≤ log2(1 + N(N+1)/2)`; for μ=1/2, ν=1/4:
  `log2 N ≤ S̃_2 ≤ log2 N + 2`; "measuring pairwise or even triplet-wise correlations between all
  bit pairs and triplets is insufficient to provide a useful floor on the information rate, no
  matter what values are empirically observed.  However, knowing the extent to which other
  statistical properties are obeyed can yield strong guarantees ... exchangeability is one such
  constraint" (min entropy then linear in N).  Cites the derandomisation literature (pairwise
  independent sample spaces from finite fields and linear codes, Hadamard matrices).
  => **Q2 for k = 2 (and 3), in the unrestricted class of all distributions, is in print as an
  "identified set for the entropy", with the same moral (a structural assumption is needed).**
  Not there: general k; a Gibbs class with bounded energy differences (their low-entropy
  distributions have tiny support, i.e. infinite energies); the class-minimum entropy.
* **Schneidman, Still, Berry, Bialek, PRL 91 (2003) 238701**, arXiv:physics/0307072
  `[grep + passages]`: "connected information of order k" from the hierarchy of maximum entropy
  distributions consistent with k-th order marginals; the XOR example ("if a third variable is
  formed as the exclusive OR ... then all pairwise ..." marginals carry nothing); cites Amari's
  information-geometric hierarchy.
* **Bhangale & Potukuchi, arXiv:1709.00752v2** `[full text: abstract, §1, Thm 1.1–1.2]`.  Verbatim
  facts: for a code with parity-check matrix M and distance d, `yᵀM` with uniform y is
  (d−1)-wise independent; "For k = O(1), BCH codes give k-wise independent sample spaces of
  support size O(n^{k/2})"; "The study of entropy of joint distributions with bounded
  dependence was first studied by Babai"; "Gavinsky and Pudlák prove asymptotically tight lower
  bounds on the joint entropy of k-wise independent ... random variables for small values of k
  ... entropy at least log C(n, k/2)"; Thm 1.1: (k−1)-wise independent unbiased bits have
  `H ≥ n − n·H(1/2 − sqrt((k/n)(1−k/n))) − o(n)`; Thm 1.2: n/2-wise ⇒ `H ≥ n − log(n+1)`.
  => **In the unrestricted class, the exact scale of the minimum entropy compatible with uniform
  ≤k-marginals is a studied problem (Babai; Gavinsky–Pudlák 2016; Bhangale–Potukuchi 2018):
  ≈ (k/2) log n for fixed k.**  (Gavinsky–Pudlák and Babai: cited through this paper, not read.)
* **Bazzi, arXiv:1707.00552** `[abstract]`: Tietäväinen's covering-radius bound
  `R ≤ n/2 − (1/2 − o(1))·sqrt(dn)` holds for codes of dual distance d and for (d−1)-wise
  independent distributions (useful for the distance-to-code distribution in the coordinator's
  ensemble `e^{−βc·dist(x,C)}`).
* **Arnese & Lacker, arXiv:2611.07460 (5 Nov 2026)** `[abstract; Prop 2.7; Remark 6.1]`: "most
  k-dimensional coordinate marginals are close to product measures" for log-concave measures
  and for measures satisfying a variance inequality for additive functions (k below
  `2 log n / log log n`, sharp).  **Sharpness (Prop 2.7) is proved with a measure built from a
  linear orthogonal array of strength 2 (the q-ary simplex code) "with the continuous uniform
  blurring" (Owen)** — i.e. a smoothed code-supported, pairwise-independent measure used as the
  extremal example for "marginals vs joint structure".  Different statement and purpose from
  Q2, same construction idea, three weeks old.

### Step 5 — Henderson / realizability / pair statistics / SAXS / FRET
* **Frommer, Hanke, Jansen, arXiv:1903.03317** (J. Math. Phys. 2019 — journal not read) `[full
  text: abstract, §1]`: "In 1974 Henderson proved that this [pair] potential is uniquely
  determined [by the pair correlation function] in a canonical ensemble and he claimed the same
  result for the thermodynamical limit"; there is "a gap in the argument"; they prove it for a
  class of superstable (hard-core, Lennard-Jones type) potentials via Georgii's variational
  principle; "for the corresponding inverse problem on the lattice the uniqueness of the pair
  potential has already been settled by Griffiths and Ruelle"; "The general existence problem is
  widely open".  (Henderson 1974, Griffiths–Ruelle 1971, Chayes–Chayes–Lieb 1984: **not read**,
  known to me through this paper and memory.)
* **Kuna, Lebowitz, Speer, J. Stat. Phys. 129 (2007) 417**, arXiv:math-ph/0612075 `[abstract,
  §1]`; **Ann. Appl. Probab. 21 (2011) 1253**, arXiv:0910.1710 `[abstract]`: realizability of
  (ρ1, ρ2) by a point process "is an infinite-dimensional version of the classical 'truncated
  moment' problem"; "Typically if any realizing process exists there will be many (even an
  uncountable number); ... when X is a finite set, the existence of a realizing Gibbs measure
  with k body potentials which maximizes the entropy among all realizing measures"; "the
  realization determined by (ρ, g) alone is not unique".
  => the classical statistical-mechanics picture is exactly the Q2 dichotomy at m = 2 in
  continuum language: pair correlations determine the pair potential *inside the pair-potential
  class* (Henderson; exponential family), but uncountably many measures share them.
* **Gommes, Jiao, Torquato, PRE 85 (2012) 051140**, arXiv:1205.3382 `[abstract]`; **Jiao,
  Stillinger, Torquato, PRE 81 (2010) 011105**, arXiv:0908.1366 `[abstract, partial]`: "distinctly
  different microstructures may have the same [two-point] correlation function"; "What is the
  number of microstructures compatible with a specified correlation function? We computed this
  degeneracy, i.e., configurational entropy".  (Single configurations, not ensembles.)
* **Boutin & Kemper, Adv. Appl. Math. 32 (2004) 709**, arXiv:math/0304192 `[abstract]`: point
  configurations are determined by the distribution of mutual distances "for the vast majority
  of configurations", with counterexamples.  (Single configurations.)

**S19** PubMed (4 named-paper queries) and **S20** PubMed `(SAXS OR "small-angle scattering") AND ensemble AND (underdetermined OR "information content" OR degeneracy OR "Shannon channels" OR overfitting) AND (disordered OR flexible)` → 7 hits.  All `[abstract]` (E-utilities):
* Konarev & Svergun, IUCrJ 2 (2015) 352, doi:10.1107/S2052252515005163: "for monodisperse systems,
  the useful experimental data range is defined by the number of meaningful Shannon channels
  that can be determined from the data set".
* Petoukhov & Svergun, Acta Cryst. D71 (2015) 1051, doi:10.1107/S1399004715002576 (AMBIMETER): "a
  priori assessment of the ambiguity"; "the number of distinct shape categories compatible with
  a given data set" from a library of > 14 000 shape topologies → an "a-score".  (A counted
  identified set for single-particle shapes.)
* Rambo & Tainer, Nature 496 (2013) 477, doi:10.1038/nature12070.
* Shevchuk & Hub, PLoS Comput Biol 13 (2017) e1005800, doi:10.1371/journal.pcbi.1005800:
  refinement "is often ambiguous due to the low information content of SAXS data"; the Bayesian
  formulation "quantifies the precision or ambiguity of fitted structures and ensembles".
* Potrzebowski, Trewhella, André, PLoS Comput Biol 14 (2018) e1006641: "limited information
  content in SAS data"; model evidence selects the number of ensemble members.
* Spill & Nilges, PLoS One 12 (2017) e0177309, doi:10.1371/journal.pone.0177309: "we study the
  ensemble average and covariance of SAS profiles analytically ... the information content is
  not uniform and reaches its maximum in the intermediate q range ... for highly flexible
  systems, the SAS profile is a representation of the ensemble of conformers in solution, and
  not that of one conformer in particular".
* Schwalbe et al., Structure 22 (2014) 238: "Ensemble descriptions of IDPs are highly
  underdetermined"; validation by cross-validation.
* Bowerman et al. (BEES 2019; JCTC 2017); Chen & Hub 2014; Henriques et al. 2018 — context.
**S21** PubMed: SES → Berlin, Castañeda, Schneidman-Duhovny, Sali, Nava-Tudela, Fushman, JACS 135
(2013) 16595, doi:10.1021/ja4083717 `[abstract]`: "As the number of the ensemble degrees of
freedom generally greatly exceeds the number of independent observables, directly deconvolving
experimental data into a representative ensemble is an ill-posed problem"; sparsity
regularisation (compressive sensing).
**S22** PubMed: FRET vs SAXS → Fuertes et al., PNAS 114 (2017) E6342, doi:10.1073/pnas.1704692114
`[abstract]` ("decoupling between R_E and R_G"); Fuertes et al., Science 361 (2018) comment.
**S23** PubMed: Song, Gomes, Shi, Gradinaru, Chan, Biophys J 113 (2017) 1012,
doi:10.1016/j.bpj.2017.07.023 (PMC5658725) `[abstract; full text via fetch tool, first 100 000
of 134 792 chars]`.  Abstract verbatim: "When all possible—heterogeneous as well as
homogeneous—conformational distributions are taken into account without prejudgment, a single
value of average transfer efficiency ⟨E⟩ ... is generally consistent with highly diverse,
multiple values of the average radius of gyration ⟨Rg⟩.  Here we utilize unbiased
conformational statistics from a coarse-grained explicit-chain model to establish a general
logical framework to quantify this fundamental ambiguity in smFRET inference."  Per the fetch
tool: the quantification is a **conditional probability distribution `P(Rg² | ⟨E⟩)` under the
model's own sampling measure (subensembles, Bayes' theorem), with overlap coefficients — not a
minimum–maximum range over all distributions**; no explicit bounds.
=> In the FRET/SAXS literature the ambiguity is quantified in a prior-weighted (typical) sense;
no extremal identified set of ⟨Rg⟩ given ⟨E⟩ was found (so far).

### Step 6 — NMR-specific identifiability; early "feasible weights"; moment-problem classics
**S24** PubMed: `Hoffmann F AND Mulder FA AND Schafer LV AND entropy AND NMR relaxation`; `"entropy meter" AND NMR AND (Wand AJ OR Sharp KA)`; `Prompers JJ AND Bruschweiler R AND (entropy OR thermodynamic) AND correlations`.  All `[abstract]`:
* Hoffmann, Mulder, Schäfer, J. Phys. Chem. B 126 (2022) 54, doi:10.1021/acs.jpcb.1c07786 ("How Much
  Entropy Is Contained in NMR Relaxation Parameters?"): MD of T4 lysozyme; "the majority of the
  entropy is indeed contained in the short-time dynamics" for the backbone; slow side-chain
  dynamics beyond τ_R contribute significantly.  (About *time scales*, not about marginals vs
  correlations.)
* Kasinath, Sharp, Wand, JACS 135 (2013) 15092, doi:10.1021/ja405200u: "An empirical method that
  utilizes changes in conformational dynamics as a proxy for changes in conformational entropy".
* Caro et al., PNAS 114 (2017) 6563, doi:10.1073/pnas.1621154114: "changes in protein
  conformational entropy can be quantitatively obtained through a dynamical proxy, but the
  generality of this relationship has not been shown"; calibrated on 28 complexes.
* **Wand & Sharp, Annu. Rev. Biophys. 47 (2018) 41**, doi:10.1146/annurev-biophys-060414-034042
  (PMC7071556) `[abstract; full text via fetch tool, first 100 000 of 131 459 chars; quotes
  ≤125 chars]`: "the true nature of the potential governing motion is uncertain"; "motions of
  different NMR probes may be correlated"; "current NMR methods provide routine access to the
  dynamics of only a limited number of sites"; the linear relation is introduced "By postulate"
  and "the objections that might be made against the oscillator inventory approach are subsumed
  into this empirical parameter" (slope −4.8 ± 0.5 J mol⁻¹ K⁻¹ per unit ⟨O²⟩ change per
  residue-weighted term, 28 complexes, R = 0.85); MD: coupling "primarily manifests as a linear
  scaling", "reducing the side-chain entropy by a constant factor of about 17%".  The fetch tool
  reports **no statement that site-wise entropies are only an upper bound**.
  => the "entropy meter" is an empirical calibration of entropy against *single-site* averaged
  quantities; its validity is a property of real proteins, not a theorem.  A proved statement
  that single-site (or ≤k-site) averaged data cannot bound entropy inside a stated energy class
  would be the missing mathematical counterpart — I found none (see S18).
**S25** PubMed: RDC parameter count; Jardetzky; Nikiforovich; NAMFIS.  All `[abstract]`:
* Fisher, Zhang, Stelzer, Al-Hashimi, J. Phys. Chem. B 112 (2008) 16815, doi:10.1021/jp806188j:
  "up to 25 motionally averaged Wigner rotation elements ... can be determined experimentally
  from multialignment RDCs ... The 25 elements can also be used to fit an ensemble consisting of
  up to eight equally or six unequally populated states."  (Finite generalised-moment data:
  the rank-2 Wigner moments of the orientational distribution, and nothing else.)
* Jardetzky, Biochim. Biophys. Acta 621 (1980) 227, doi:10.1016/0005-2795(80)90174-9: "in cases
  where the individual conformers contributing to the average are not known the 'average'
  derived from spectroscopic data represents a virtual structure devoid of physical meaning."
* **Nikiforovich, Vesterman, Betins, Podins, J. Biomol. Struct. Dyn. 4 (1987) 1119**,
  doi:10.1080/07391102.1987.10507702: "the selection of statistical weights w_i for molecular
  conformers in solution by combined use of spectroscopic data and energy calculations ...
  Consequently, it appears possible to confine the entire region of all w_i values only by those
  points (w_i) that provide a reasonable agreement between the results of calculations and the
  experimental data."  **= a feasible-region (set-membership) treatment of conformer weights,
  twenty years before MAP/MaxOcc** (abstract only; they report "mean statistical weight values"
  found by random search — Nikiforovich, Vesterman, Betins, Biophys. Chem. 31 (1988) 101).
* NAMFIS (Cicero, Barbato, Bazzo, JACS 117 (1995) 1027 — `[from memory — unverified]`; PubMed
  shows later applications only): constrained least-squares deconvolution into conformer
  populations.

**S26** Web: de Finetti's fundamental theorem → **Lad, Dickey, Rahman, "The fundamental theorem of
prevision", Statistica 50(1) (1990) 19–38**, doi:10.6092/issn.1973-2201/822 `[abstract via fetch
tool, paraphrased by the tool]`: de Finetti's fundamental theorem of probability "reformulated in
the finite case as a computable linear programming problem", extended to general quantities, with
bounds and orderings on previsions as inputs and outputs.  Also seen in snippets: Walley–
Pelessoni–Vicig (coherence checking by LP), Schervish–Seidenfeld–Kadane (CMU TR 837).
**S27** Web (extended): robust Bayes with generalised moment classes → Betrò, Ruggeri, Męczarski,
"Robust Bayesian analysis under generalized moments conditions", J. Statist. Plann. Inference 41
(1994) 257 (ScienceDirect pii 0378375894900221); Betrò & Guglielmi, "Numerical robust Bayesian
analysis under generalized moment conditions" ("interval analysis with semi-infinite linear
programming"); Betrò–Bodini–Guglielmi, Ann. Inst. Statist. Math. (2006), "Generalized moment
theory and Bayesian robustness analysis for hierarchical mixture models"; van Eekelen,
arXiv:2401.00090; Salako & Muhammad, arXiv:2608.04315 (Aug 2026).  All `[search snippet]`, except
the two arXiv abstracts `[abstract]`.  **The snippet search found nothing on density-ratio or
density-band classes *with* moment constraints** (Perone Pacifico–Salinetti–Tardella "constrained
density band classes" is `[from memory — unverified]`; to be searched).
**S28** Web: Bertsimas & Popescu, SIAM J. Optim. 15(3) (2005) 780–804, doi:10.1137/S1052623401399903
`[search snippet]`: tight moment inequalities for `P(X ∈ S)` by semidefinite optimisation; MIT
Sloan WP 4083 (1999) is an open copy (not read).
**S29** Web: Smith, "Generalized Chebychev Inequalities: Theory and Applications in Decision
Analysis", Oper. Res. 43(5) (1995) 807–825, doi:10.1287/opre.43.5.807 `[search snippet]`: "given
certain 'moments' of a distribution, we can compute bounds on the expected value of an arbitrary
'objective' function"; applications include "decision analysis with incomplete information".
**S30** arXiv by ID: Christensen–Connault journal ref confirmed: **Econometrica 91(1) (2023)
263–298, doi:10.3982/ECTA17232**; Lam 1303.0326 abstract (KL-constrained worst case,
"infinitesimal approximations").

### Step 7 — closing the loop between MaxOcc and the moment-problem literature
**S31** Web: Ravera et al. 2016 in repositories → flore handle 2158/1058396 and CNR IRIS 20.500.14243/338112 have **no file attached**; RSC html also HTTP 403.  => `[abstract only]`, stated as not accessed.
**S32** Web: Medeiros Selegato et al. 2021 → no open full text found.  `[abstract only]`.
* Hou & Tochio, Biophys. Rev. 14 (2022) 55, doi:10.1007/s12551-021-00916-4 (PMC8921464) `[full
  text via fetch tool, first 100 000 of 116 328 chars]`: "MaxOcc is the maximum allowed weight for
  a conformation in any possible ensembles"; "MaxOcc does not guarantee minimum occurrence";
  "reconstruction is inherently an underdetermined problem, as there are infinite combinations
  of structures"; "No ensembles can be considered unique"; per the tool, no method newer than
  MaxOcc/maxOR that computes population ranges is described.
**S33** Web: dilation → Seidenfeld & Wasserman, Ann. Statist. 21(3) (1993) 1139–1154,
doi:10.1214/aos/1176349254 `[search snippet]`; follow-up snippet: density ratio classes "have just
the right shape to avoid dilation" (Wasserman & Seidenfeld 1994, JSPI — `[search snippet]`).
**S34** Web: adaption in information-based complexity → snippets (Osipenko, J. Complexity; Kon &
Novak, Bull. AMS 1990): "for convex but not symmetric sets adaptive information can be
significantly better than nonadaptive information"; "adaption helps at most twice" for convex
symmetric sets.  `[search snippet]`.  (The identified sets of Q1 are convex and not symmetric.)
**S35** Web: Dominitz & Manski, "More Data or Better Data? A Statistical Decision Problem", Rev.
Econ. Stud. 84(4) (2017) 1583–1605, doi:10.1093/restud/rdx005 `[search snippet]`: Wald decision
theory, minimax regret, allocation of a budget between sampling processes of different quality,
"partial identification of the true state of nature".
**S36** Web (extended): `"linear programming" bounds populations conformers "J coupling" OR NOE ...
"minimum and maximum" population` → **no LP-bounds method for conformer populations found** in
small-molecule/peptide NMR; a Beilstein J. Org. Chem. 7:20 snippet notes "a broad range of
conformer populations fitting the observed NOE restraints".
**S37** Web (extended): provable partition functions (K*, BBK*, DEE/A*) combined with model
uncertainty / relative entropy / DRO → **no combination found** (Hallen & Donald review
arXiv:1806.06064; Rasheed et al. arXiv:1508.03882 Chernoff-type bounds for input uncertainty).
**S38** PubMed: MIE / MIST; `(ensemble reweighting OR "ensemble refinement") AND ("upper bound" OR
"lower bound" OR "bounds on" OR "range of") AND (populations OR weights) AND (NMR OR SAXS OR FRET)`
→ 2 hits, neither about bounds; `... AND ("non-identifiab*" OR identifiability OR
unidentifiable) AND (conformational ensemble)` → **0 hits**.  (The vocabulary "identifiability"
is essentially absent from this literature; "underdetermined", "ill-posed", "degenerate" are
used instead.)
* Killian, Kravitz, Gilson, J. Chem. Phys. 127 (2007) 024107, doi:10.1063/1.2746329 `[abstract]`:
  entropy "as an expansion of multidimensional mutual information terms", equivalent to the
  generalised Kirkwood superposition approximation, truncated (an approximation, not a bound).
* King, Silver, Tidor, J. Phys. Chem. B 116 (2012) 2891, doi:10.1021/jp2068123 `[abstract]`: MIST
  "is also guaranteed to bound the entropy" (an *upper* bound from low-order marginals).
* Köfinger & Hummer, J. Chem. Phys. 160 (2024), doi:10.1063/5.0189901 `[abstract]`: "Viewed as a
  Pareto optimization problem, improved agreement with the experimental data comes at the
  expense of growing inconsistencies with the theoretical reference model ... By relating the
  variance of this energy difference to the Kullback-Leibler divergence between the respective
  Boltzmann distributions, one can encode prior knowledge about energy uncertainties, i.e.,
  force-field errors, in the exchange rate."  (= how large the KL neighbourhood of a force
  field should be; the natural bridge from an envelope/bounded-difference class to a KL radius.)
* Bonomi, Heller, Camilloni, Vendruscolo, Curr. Opin. Struct. Biol. 42 (2017) 106 `[full text,
  author copy; passages read]`: "(the so-called inverse problem) is an ill-defined problem, in
  the sense that it allows multiple solutions, as different structural ensembles can fit the
  same averaged data.  From a second perspective, however, ... As long as different structural
  ensembles generate the same observable average quantities, and thus result in similar
  predictions for the system properties, they should be considered equivalent"; choice between
  maximum entropy and maximum parsimony depends on the entropy of the system, and "it is not
  always easy to estimate a priori the amount of entropy".  MaxOcc is listed (Table) among the
  maximum-parsimony methods.  **Note: "same observable averages ⇒ similar predictions" is
  exactly the inference an identified-set calculation would test.**
* Pitera & Chodera, JCTC 8 (2012) 3445 `[full text, author copy; passage read]`: "in
  underdetermined cases, there may be many distributions whose ensemble averages satisfy
  experimental constraints, but which impose varying degrees of bias"; MaxEnt = "the unique
  minimally biased choice".
* Sgheri, Inverse Problems 26 (2010) 035003, doi:10.1088/0266-5611/26/3/035003 `[abstract via
  fetch tool, paraphrased]`: the maximal probability is extended "to any measurable subset of
  the rotation group"; properties are established.  (Theorem-level precursor of maxOR.)

**S39** Web: Chayes–Chayes–Lieb, Commun. Math. Phys. 93 (1984) 57–121 `[search snippet]`: "for
essentially all systems without hard core interactions, there is a unique external potential
which produces any given density"; multi-particle version: Chayes & Chayes, J. Stat. Phys. 36
(1984) ("On the validity of the inverse conjecture in classical density functional theory")
`[search snippet]`.  projecteuclid PDF not retrievable (HTML shell).
**S40** Web: Moore, J. Appl. Cryst. 13 (1980) 168–175 `[search snippet, via Konarev–Svergun 2015
and others]`: Shannon channels `q_n = nπ/D`; `N_S = q_max·D_max/π` as an estimate of the number
of independent parameters; "this value alone cannot provide an ultimate estimate, due to the fact
that the signal-to-noise ratio is not taken into account".
**S41** Web: Christoffel function / maximal mass → Schmüdgen, Methods Funct. Anal. Topology 21
(2015) 266–281; di Dio & Schmüdgen arXiv:1703.01494 (J. Math. Anal. Appl. 461 (2018) 1606) and
arXiv:1809.00584; Beckermann–Putinar–Saff–Stylianopoulos arXiv:1812.06560.
* **di Dio & Schmüdgen, "The multidimensional truncated moment problem: the moment cone"**,
  arXiv:1809.00584v1 `[full text: abstract, intro sentences, §10 Def. 74, Prop. 75 with proof,
  Def. 76–77]`.  Setting: finitely many measurable functions `A = {a_1..a_m}` on a space `X`
  ("moment sequence" `s`, "moment cone" `S_A`, Richter's theorem: each moment sequence has a
  k-atomic representing measure with k ≤ m).  **Def. 74: the *maximal mass function*
  `ρ_s(x) := sup{ μ(A_x) : μ ∈ M_A(s) }`.  Prop. 75: `ρ_s(x) = sup{c ≥ 0 : s − c·s_A(x) ∈ S_A}
  ≤ κ_s(x) := inf{ L_s(p) : p ∈ Pos(A), p(x) = 1 }`, with equality (and attainment,
  `s − ρ_s(x) s_A(x) ∈ ∂S_A`) when the moment cone is closed and pointed — e.g. continuous
  functions on a compact space.**  "Determining the maximal mass at a given atom leads to a
  convex optimization problem [Sm15], [Sm17, Section 18.4]."
  => This is **MaxOcc as a theorem with its exact conic dual**: the first formula is the
  Gardner–Longinetti–Sgheri ray-shooting formula (their Thm 3.8) in full generality; the dual
  `κ_s(x)` minimises the "measured value" `L_s(p) = λ0 + λ·m` over nonnegative combinations
  `p = λ0 + λ·φ` with `p(x) = 1`, and **checking `p ≥ 0` on X is a global minimisation over
  conformations** — the coordinator's "dual is a certified global optimisation".
  Cross-citation check (grep): di Dio–Schmüdgen do not mention Sgheri/Longinetti/Gardner/NMR;
  Gardner–Longinetti–Sgheri cite Curto–Fialkow (quadratic moment problem) but not the
  maximal-mass / Christoffel literature.  **The two literatures appear not to know each other.**
* di Dio & Schmüdgen arXiv:1703.01494 `[passage]`: "Recall from [Sch15] the maximal mass function
  `ρ_L(x) := sup{μ({x}) : μ is a representing measure of L}`"; Prop. 10(iii): the map
  `s ↦ c_s(x)` is concave and continuous on the interior of the moment cone.
* Classical references as listed in OUQ (arXiv v3 bibliography, read there): Isii, Ann. Inst.
  Statist. Math. 10 (1959) 65; 12 (1960) 119; 14 (1962/63) 185; Karlin & Studden, *Tchebycheff
  Systems* (1966) [Markov–Krein theorem]; Mulholland & Rogers, Proc. LMS 8 (1958) 177; Karr,
  Math. Oper. Res. 8 (1983) 74; von Weizsäcker & Winkler, Math. Ann. 246 (1979/80) 23; Winkler,
  Math. Oper. Res. 13 (1988) 581; Dynkin, Ann. Prob. 6 (1978) 705; Vandenberghe, Boyd, Comanor,
  SIAM Rev. 49 (2007) 52; Bertsimas & Popescu, SIAM J. Optim. 15 (2005) 780.  (Originals not
  read; Kemperman 1968, Rogosinski 1958, Richter 1957, Lasserre: `[from memory — unverified]`.)

### Step 8 — remaining searches, then numerics
**S42** Web: Gordon → "Error Bounds in Equilibrium Statistical Mechanics", J. Math. Phys. 9(5) (1968)
655–663: from the high-temperature expansion coefficients (moments) of the canonical partition
function, error bounds "both rigorous and optimal"; companion "Error Bounds in Spectroscopy and
Nonequilibrium Statistical Mechanics", J. Math. Phys. 9(7) (1968) 1087–1092: upper and lower
bounds on a response "using only ... the equilibrium moments of the spectral density".
`[search snippet]`; author (R. G. Gordon) from memory.  (Chemical-physics precedent for "optimal
bounds on unmeasured averages from finitely many known moments" — spectral measures, not
conformational ensembles.)
**S43** Web: density-ratio / likelihood-ratio class + moment constraints (Dorn–Guo, Rosenbaum,
robust Bayes) → nothing relevant returned (van Eekelen arXiv:2401.00090 again).  **No source found
for a moment-constrained density-ratio class; the L5 report's verdict on P6 ("no metric-governed
class in robust Bayes") therefore extends, as far as my searches go, to its moment-constrained
version.**
**S44** PubMed: experimental design → Dimura et al., Nat. Commun. 11 (2020) 5394,
doi:10.1038/s41467-020-19023-1 `[abstract]` ("an automated design tool for FRET experiments, which
determines how many and which FRET pairs should be used to minimize the uncertainty and maximize
the accuracy of an integrative structure"); Mittal & Shukla, J. Phys. Chem. B 121 (2017) 9761,
doi:10.1021/acs.jpcb.7b04785 and 122 (2018) 10793, doi:10.1021/acs.jpcb.8b07076 `[abstract]`
(label pairs ranked by capturing slow processes and being uncorrelated, "maximum information
gain").  Query `("optimal experimental design" OR ...) AND ("conformational ensemble" OR "ensemble
refinement" OR "structural ensemble") AND (NMR OR FRET OR DEER OR SAXS)` → **0 hits**.
**S45** arXiv: Bresler, Gamarnik, Shah, arXiv:1409.3836 `[abstract]`: "For graphical models
representing a minimal exponential family, the canonical parameters are uniquely determined by the
mean parameters ... no algorithm can learn the canonical parameters of a generic pair-wise binary
graphical model from the mean parameters in time bounded by a polynomial in the number of
variables (unless RP = NP)."  Santhanam & Wainwright, arXiv:0905.2639 `[abstract]` (sample
complexity of graph selection — a different question from population identifiability).
**S46** Web: PSAT → Jaumard, Hansen, Poggi de Aragão, "Column Generation Methods for Probabilistic
Logic", ORSA J. Comput. 3(2) (1991) 135, doi:10.1287/ijoc.3.2.135 `[search snippet]`: column
generation solves PSAT with interval probabilities exactly ("up to 140 variables and 300
clauses").  That the pricing step is a nonlinear 0–1 (global) optimisation: `[from memory —
unverified]`.  Walley's natural extension: `[from memory — unverified]` (no snippet obtained).
**S47–S50** Consensus (semantic search, 3 results each):
 (47) "rigorous upper and lower bounds on conformational state populations over all ensembles
  consistent with ensemble-averaged experimental data" → Ravera et al. 2016 (abstract sentence:
  "In the first case [maximum entropy], the solution focuses on the features that are common to
  all the infinite solutions satisfying the experimental data; in the second case, the
  reconstructed ensemble shows the conformational regions where a large probability can be
  placed.  The upper limits for conformational probabilities (MaxOcc) can also be calculated.");
  Raddi et al. 2026 (BICePs force-field optimisation, J. Chem. Phys.); Raddi & Voelz 2026 (arXiv).
 (48) "non-uniqueness ... range of predicted unmeasured observables across all consistent
  ensembles" → Gomes et al., JACS 2020 (SAXS+NMR ensembles, smFRET held out for validation);
  Naudi-Fabra et al., JACS 2021 (cross-validation); De Castro et al. 2026 (IDPForge).
 (49) "worst-case optimal choice of next experiment ... minimax experimental design" → Huan,
  Jagalur, Marzouk, Acta Numerica 2024 (OED survey: Bayesian and decision-theoretic, expected
  information gain); Kusumo et al. 2022 (CVaR-based design campaigns); Zhong et al. 2026
  (goal-oriented Bayesian OED).  Nothing on conformational ensembles.
 (50) "lower bound on entropy from low-order marginals impossible ... Gibbs measures with bounded
  interactions" → Jain et al. 2026 (entropic independence via sparse localization, EJP); Arnese &
  Lacker 2026; Blanca et al. 2026 (k-partite factorisation of entropy under spectral
  independence).  (Positive counterpart: under spectral independence / weak coupling the entropy
  *does* factorise approximately over local conditionals.)  All `[abstract]`.
 Consensus notice (must accompany results): "Create or connect a free Consensus account to return
 more than 3 results per search in Claude Code.: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code"

### Numerics (statements compared in the report; not new results)
`check_statements.py` (seed 20261125) → `check_statements.out`.  All assertions passed.
* N1: 120 point instances (|X| 12–59, 1–5 observables): primal LP = hard-max dual = ray-shooting
  formula (Gardner–Longinetti–Sgheri Thm 3.8) = conic dual κ (di Dio–Schmüdgen eq. 32) to 1.1e-7
  (bisection tolerance); 40 region instances: minOR(A) = 1 − maxOR(Aᶜ) to 9e-15.
* N2: 12 instances × 2 radii: SLSQP primal = Christensen–Connault dual (KL) to 4.9e-10; at ρ = 60
  the dual equals the prior-free LP value to 5 digits.
* N3: μ ∝ e^{−u·dist(x,C)} for simplex[7,3], RM(1,3)[8,4], simplex[15,4], RM(1,4)[16,5] (dual
  distances 3,4,3,4): ≤(d⊥−1)-site marginals uniform to 1e-13, the d⊥-site ones not (dev 2–7e-2);
  energy has single-site differences ≤ c.  Entropy per site (u=4): 0.3818, 0.4297, 0.2749,
  0.3066 against the class bound h(1/(1+e⁴)) = 0.0901 and ln 2 = 0.6931; **the excess over the
  class bound equals ln|C|/n to 4 digits at u = 4** (0.1848 for [15,4], 0.2166 for [16,5]) — so
  the sketch's "minimum entropy the class allows" is an asymptotic statement (needs
  ln|C|/n → 0, true for dual-BCH codes at fixed k) and is far from reached at enumerable n.
* N4: envelope cone ∩ moment constraints is one LP per end in the weights (normalisation as a
  linear equality); nesting cone+moments ⊂ moments-only and ⊂ cone-only verified on 4 instances.

### Step 9 — report written; last checks
* `docs/science/workstreams/SM_REPORT.md` written (sections 1–7; matrix §4.1; vocabulary §4.2;
  five papers §4.3; condensed search log §4.4; not-accessed list §5).
* `check_q2_decomposition.py` → `.out`: `H(μ_C) = ln|C| + H(ν)` holds to 1e-9 in 16 cases;
  `(H(μ_C) − n·h(p_u))/ln|C|` ranges from 0.249 (RM(1,3), u=1) to 1.000 (u=8); `H(ν)/n ≤ h(p_u)` in
  all 16 cases (conjecture [C] that this is general).
**S51** arXiv API: 5 multi-term abstract queries (force field + Kullback-Leibler + uncertainty
quantification + bounds; experimental + relative entropy + worst-case + molecular/Gibbs;
distributionally robust + molecular dynamics/Boltzmann/conformational; moment constraints +
Kullback-Leibler + ambiguity set; partial identification + protein/molecular) → nothing relevant
(the API returned unrelated DRO/conformal-prediction papers or nothing).
**S52** arXiv API: Gavinsky & Pudlák, "On the Joint Entropy of d-Wise-Independent Variables",
arXiv:1503.08154 `[abstract]` (see report K9).
**S53** PubMed: `Fisher CK AND Stultz CM AND (ensembles OR Bayesian)` → Fisher & Stultz, Curr. Opin.
Struct. Biol. 21 (2011) 426, doi:10.1016/j.sbi.2011.04.001; Fisher, Ullman, Stultz, Pac. Symp.
Biocomput. 2012:82–93 `[abstracts]`.
**S54** X. Xu's Columbia thesis via academiccommons (doi:10.7916/D8SX6MF1/download) → HTTP 404.
Glasserman–Xu stays `[search snippet]`.
* Verified against extracted text before finalising: BioEn functional `exp(−θ∫p ln(p/p0) − χ²/2)`
  and "the kink of the S_KL-versus-χ² curve" (arXiv:1509.04447); Gigli et al. Table-2 numbers
  (396 → 161 SAXS / 68 DEER / 50 both; 131 → 24 / 18 / 9).

### Step 10 — a cleaner variant of the Q2 sketch and its prior art (late find)
* While reviewing K10 I noticed that the *convolution* variant (uniform codeword `Y` plus
  i.i.d. Bernoulli(p_u) noise `E`, `X = Y ⊕ E`) has a complete three-line proof of the no-go:
  (i) in the class (each term of `m(x) = |C|⁻¹Σ_c π(x⊕c)` changes by a factor in `[e^{−u},e^{u}]`),
  (ii) C-invariant ⇒ uniform marginals below `d(C^⊥)`, (iii) `H = n·h(p_u) + I(X;Y)`,
  `0 ≤ I ≤ ln|C|`.  Labelled [P] in the report (K10(f)).
* `check_q2_bsc_variant.py` → `.out` (seconds): 12 cases (4 codes × u = 1, 2, 4): single-site
  log-ratio/u ≤ 1.0000; (d⊥−1)-marginals uniform to 2e-14; d⊥-marginals deviate 3e-3–1e-1;
  `(H − n·h)/ln|C|` ∈ [0.316, 1.000].  All assertions pass.
**S55** arXiv API (titles): Samorodnitsky & Sberlo, "On codes decoding a constant fraction of
errors on the BSC", arXiv:2008.07236 `[abstract]`; **Samorodnitsky, "On the entropy of a noisy
function", arXiv:1508.01464 `[abstract]`**: for binary `X` and BSC(ε) noise `Z`, with
`v = (1−2ε)²·n`, `H(X ⊕ Z) ≥ n·H(ε + (1−2ε)·H⁻¹(E_{|B|=v} H(X_B)/v))` "up to lower-order terms"
— "a strengthening of 'Mrs. Gerber's lemma'".  => a published *lower* bound on the entropy of a
noise-smoothed measure from marginals of order linear in n: the positive counterpart of Q2 for
the smoothed subclass; consistent with "no fixed order suffices".  Read as an abstract only;
the exact hypotheses must be checked by the coordinator.

### Final status (2026-11-25)
* Report: `docs/science/workstreams/SM_REPORT.md` (§1 verdicts; §2 K1–K13 with reading levels;
  §3 numerics N1–N4, N3b; §4 matrix, vocabulary, five papers, search log; §5 not settled / not
  accessed; §6 next steps; §7 requests T-M1..4, E-M1..2).
* Quotation audit done before closing: every passage in quotation marks in the report is either
  verbatim from a text/abstract I saw or a fetch-tool extract labelled as such; three paraphrases
  that had been set in quotation marks were rewritten (Albanna summary, Bonomi phrase,
  Gavinsky–Pudlák attribution) and the brittleness quote was re-attributed to the EJS paper.
* Files in this directory: NOTES.md; check_statements.py/.out (N1–N4);
  check_q2_decomposition.py/.out (K10(c)); check_q2_bsc_variant.py/.out (K10(f)).
* Nothing outside `experiments/science/ws_M/` and `docs/science/workstreams/SM_REPORT.md` was
  written; no git state was changed; downloaded PDFs are in the session scratchpad only.
* If resumed: (1) obtain Ravera et al. 2016 and Medeiros Selegato et al. 2021 through a library;
  (2) read Glasserman–Xu 2014 and Betrò–Guglielmi; (3) read Samorodnitsky's paper in full and
  state precisely what it implies for the noisy-codeword family; (4) forward-citation search of
  Gardner–Longinetti–Sgheri 2005 and of Schmüdgen 2015.

## Follow-up task (coordinator message, 2026-11-25): addendum S1–S4
Targets: (S1) stability of MaxEnt refinement (Thm 7, 7'); (S2) falsification: minimum relative
entropy as a certified lower bound on model error, and least envelope constant (Thm 8);
(S3) two-oracle query model (Thm 4, 4', 5, Prop 5b); (S4) read Betrò–Guglielmi; certified
MaxOcc after 2014.  Deliverable: section 8 of SM_REPORT.md + final message ≤ 350 words.
Search log for the addendum is numbered A1, A2, ...
### Step A0 — read the coordinator's statements
* Read `docs/science/INFERENCE_LIMITS.md` §4, §5, §6 (Thm 7), §9 (Thm 8) and the whole of
  `INFERENCE_LIMITS_ADDENDA.md` (Thm 4′, 7′, Prop 10, A4).
### Step A1 — S1
* Derived (R1): nu is the reverse I-projection of mu on the exponential family ⇒
  KL(mu‖nu) ≤ KL(mu‖mu_lam) ≤ (beta·omega)²/8 (Hoeffding).  Factor 2 better than Thm 7(v).
* Derived (R2): J ≥ 4·TV·artanh(TV) (data processing + one-variable minimisation) ⇒ with Thm 7(i)
  TV ≤ tanh(beta·omega/4), J ≤ beta·omega·tanh(beta·omega/4); sharp (two points, nu tilted).
* `check_addendum_s1.py` → `.out`: 3554 instances; F1 max 6e-16; KL/((bw)²/8) max 0.99993;
  TV/(bw/4) max 0.99984; J/((bw)²/4) max 0.99984; identity (i) 6e-14; Pythagoras 1e-13;
  TV/tanh(bw/4) max 0.99992; J/(4 TV artanh TV) min 1.00009; J/(bw·tanh(bw/4)) max 0.99992.
* Barron–Sheu 1991 Lemma 1 (3.2) read as quoted in Scricciolo (arXiv:0708.0175, p. with eq. 15):
  "If ‖log(f_θ'/f_θ)‖_∞ < ∞, then for any constant c, K(P_θ'‖P_θ) ≤ ½ e^{‖log(f_θ'/f_θ) − c‖_∞}
  ∫ f_θ' (log(f_θ'/f_θ) − c)² dx" ("inequality (3.2) from Lemma 1 of Barron and Sheu, pages
  1355–1356").
* Refinement literature: Stöckelmaier & Oostenbrink 2025 (PCCP 27:14704, doi:10.1039/d5cp01263e):
  no error bound; validation set; no empirical-likelihood vocabulary.  Bottaro et al. 2018: same.
### Step A2 — S2
* Christensen–Connault: δ̂ = inf_θ Δ(θ; γ̂, P̂), "the smallest value of δ for which there exists
  F ∈ N_δ consistent with the sample moment conditions" (full text).
* Masten–Poirier arXiv:1812.11598 (abstract): "falsification frontier", "extent of falsification",
  "falsification adaptive set".  arXiv:1705.04765 breakdown frontiers (snippet).
* EL/ET references (snippets; Schennach abstract).  PubMed: 0 records for EL/ET + MD.
* R3 (Jensen): E ρ̂_N ≥ ρ_min — sample-based minimum relative entropy is biased upward.
### Step A3 — S3
* Abstracts: Canonne–Rubinfeld 1402.3835 (dual access); Kolmogorov 1608.04223 and
  Harris–Kolmogorov 2007.10824 (sampling-oracle complexity of Z, lower bound Ω(q ε⁻²));
  Feldman–Perkins–Vempala 1311.4821 (distribution complexity = degree of independence);
  Lange–Qiao 2512.02279 (statistical MQ algorithms).  JVV from memory.
### Step A4 — S4
* Betrò–Guglielmi algorithm papers: NOT accessible (Academia 403, ScienceDirect 403, Springer
  login redirect, IMS LNMS not located).  Read: AISM 58 (2006) 721–738 published PDF (ism.ac.jp);
  CNR IRIS abstract of Betrò 2008; snippet of Betrò 2004 abstract; Mehrotra–Papp grep.
* Certified MaxOcc after 2014: not found in what I read; Medeiros Selegato 2021 unread.
* Section 8 appended to SM_REPORT.md with search log A1–A14.
* Quotation audit of section 8: Canonne–Rubinfeld quote corrected ("the algorithm A"); the Betrò
  2004 sentence is the search tool's wording, so the quotation marks were removed; the
  Christensen–Connault passage is in their §3.3 "Over-identification" (citation fixed).
* Final status of the follow-up: section 8 (8.1–8.5) in SM_REPORT.md; scripts
  check_addendum_s1.py/.out added here.  Open for a resumed session: obtain Betrò–Guglielmi
  (IMS LNMS 1997 pp. 3–20; Lect. Notes Stat. 152 (2000) 273–294) and Betrò 2004/2008; Barron–Sheu
  original; Csiszár 1975; Medeiros Selegato 2021; locate the sharp Jeffreys–TV inequality in print.
