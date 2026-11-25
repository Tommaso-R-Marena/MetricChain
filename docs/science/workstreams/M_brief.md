# Workstream M — prior art for the measurement side: what do ensemble-averaged data determine?

Read `docs/science/workstreams/COMMON.md` first.  Your directory:
`experiments/science/ws_M/`; your report: `docs/science/workstreams/SM_REPORT.md`
(named `SM` because the theory division already has an `M_REPORT.md`).

## Context

The science division's own research direction (developed by the coordinator in parallel
with you) treats **experimental data as information**, next to the model and to computed
energy evaluations.  The unknown is the conformational ensemble `μ` (a probability measure
on a finite or continuous configuration space `X`); the data are **ensemble averages**
`m_k = ∫ φ_k dμ` (± error) of known forward models `φ_k` — NMR chemical shifts, scalar
couplings, NOE `⟨r^{-6}⟩`, residual dipolar couplings, paramagnetic relaxation enhancement,
FRET efficiencies, DEER distance distributions, and small-angle scattering, whose intensity
is a linear functional of the **pair-distance distribution** — the same object the theory
division uses as "pair-distance profile" features (theory report §11.17).  The questions:

* **(Q1) Identified sets.**  Given the data (and possibly a prior model `μ₀ ∝ e^{−βf}` with a
  neighbourhood: a KL ball, or the theory division's envelope class, which in the weights
  `w = dμ/dμ₀` is the polyhedral cone `w(y) ≤ e^{βd(x,y)} w(x)` — theory report Theorem 11.12
  and `docs/prior_art/L5`, item P6), what is the *exact range* of another ensemble quantity
  `∫ψ dμ` (a population, a contact probability, a distance moment) over all ensembles
  consistent with everything known?  This is a generalised moment problem / linear(-fractional)
  programme; its dual is a global optimisation `max_x [ψ(x) − λ·φ(x)]`, i.e. exactly what a
  certified minimisation kernel checks.
* **(Q2) Non-identifiability theorems.**  E.g. the coordinator's sketch: in the class of Gibbs
  measures on `{±1}ⁿ` whose energy has single-site bounded differences `c`, for every fixed `k`
  there are ensembles whose `≤k`-site marginals are all exactly uniform but whose entropy per
  site is the minimum the class allows (`μ ∝ e^{−βc·dist(x, C)}`, `C` a linear code of dual
  distance `> k`): no finite order of local ensemble-averaged measurements bounds the
  conformational entropy better than the a-priori class bound; whereas for energies of
  interaction order `≤ m` the `≤m`-site marginals determine the ensemble (exponential-family
  identifiability).
* **(Q3) Value of information.**  How much does one more averaged observable shrink an
  identified set; which observable should be measured next (optimal experimental design in
  the worst-case / set-membership sense)?

You do **not** have to develop this theory.  Your job is the prior art, read at the level of
statements, so that the division claims nothing that is known.

## Literatures to open and compare (find more)

1. **Ensemble refinement in structural biology**: maximum-entropy reweighting (Jaynes;
   Pitera–Chodera 2012; Roux–Weare 2013; Cavalli–Camilloni–Vendruscolo replica-averaging;
   Boomsma et al. 2014; Hummer–Köfinger BioEn 2015; Bonomi et al. metainference 2016;
   Bottaro–Lindorff-Larsen reviews; Köfinger et al. 2019), minimal-ensemble and
   sample-and-select methods (EOM: Bernadó–Svergun 2007; ASTEROIDS; ENSEMBLE; Sparse Ensemble
   Selection; "Occam" approaches), and above all anything that computes **extremal** rather
   than typical ensembles: **Maximum Occurrence / MaxOcc / maxOR** (Bertini, Luchinat, Parigi
   and co-workers, 2007–2014: the largest weight a conformation can have in any ensemble that
   reproduces the averaged data), "minimum occurrence", "probability bounds", and any
   statement of the form "the data cannot distinguish…" that is proved rather than
   illustrated.  Identifiability/degeneracy discussions for IDP ensembles (e.g. how many
   independent parameters SAXS data contain — Shannon channels: Moore 1980; Svergun–Koch).
2. **Generalised moment problems and optimal uncertainty quantification**: Isii; Kemperman;
   Karlin–Studden; Bertsimas–Popescu ("Optimal inequalities in probability theory: a convex
   optimization approach"); Lasserre; Owhadi–Scovel–Sullivan–McKerns–Ortiz "Optimal
   Uncertainty Quantification" (SIAM Review 2013) and Sullivan et al. on OUQ with
   legacy data; Han et al.; reduction theorems (Winkler; Rogosinski).
3. **Partial identification** (Manski; Tamer; Molchanov–Molinari "Random Sets in
   Econometrics"): the identified-set language; moment-inequality models.
4. **Distributionally robust optimisation with divergence balls and moment constraints**
   (Ben-Tal et al. 2013; Hu–Hong; Breuer–Csiszár "Measuring distribution model risk";
   Lam; Duchi–Namkoong), and **information-inequality UQ for Gibbs measures and molecular
   models** (Chowdhary–Dupuis 2013; Dupuis–Katsoulakis–Pantazis–Plecháč 2016;
   Katsoulakis–Rey-Bellet–Wang; Gourgoulias et al. 2020 "How biased is your model?"): the
   Donsker–Varadhan bound `sup_{KL(μ‖μ₀)≤ρ} E_μψ = inf_η [ηρ + η ln E_{μ₀} e^{ψ/η}]` — these
   are *exactly* model-form UQ bounds whose evaluation needs a (certified) tilted partition
   function; has anyone combined them with rigorous partition-function bounds, or with
   experimental constraints?
5. **Robust Bayes / imprecise probability**: density-ratio classes (DeRobertis–Hartigan 1981;
   Wasserman 1992; Berger's surveys), "intervals of measures", lower previsions (Walley), and
   whether *moment-constrained* density-ratio classes appear.
6. **Marginal information vs joint structure**: `k`-wise independent distributions with small
   support / low entropy (Alon–Babai–Itai; orthogonal arrays; Rao bound); "local
   indistinguishability"; the marginal problem; entropy bounds from marginals (maximum
   entropy given `k`-marginals as an *upper* bound — and what is known about *lower* bounds
   under structural constraints: e.g. for Markov random fields with bounded interaction
   strength; Shearer / Han inequalities; "mutual information expansion" and "maximum
   information spanning tree" entropy estimators in biomolecular simulation: Killian–Kravitz–
   Gilson 2007; King–Tidor 2009; Wand's NMR "entropy meter"); the inverse Ising / inverse
   Potts identifiability and its conditioning (Santhanam–Wainwright; Bresler; Montanari–
   Pereira); Henderson's theorem and its extensions (pair potential ↔ pair distribution;
   Chayes–Chayes–Lieb 1984 for the general inverse problem of statistical mechanics).
7. **Scattering-specific identifiability**: homometric structures; reconstruction from
   distance distributions (Boutin–Kemper); information content of SAXS curves; ensembles
   with identical scattering.

## Deliverable

For each of Q1, Q2, Q3: (i) the closest existing statements with reading level and an honest
comparison; (ii) what, if anything, appears to be missing in the literature; (iii) the
vocabulary the division should adopt so that each community recognises its own results
(e.g. "identified set" vs "MaxOcc" vs "OUQ" vs "ambiguity set").  A matrix *question ×
literature → known / partially known / not found*.  A list of the five papers the
coordinator must read in full before writing anything, with one-sentence reasons.  Be
explicit about anything you could not access.
