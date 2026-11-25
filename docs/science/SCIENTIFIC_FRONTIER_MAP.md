# Scientific frontier map

*Science division.  Version 1 (2026-11-25).  A map of what the science of molecular
conformations cannot reliably establish today, why, and what precise problem each
limitation turns into.  It starts from the science, not from what MetricChain can prove.
Entries marked "pending" wait for a workstream of ours; they will be revised, not silently
replaced.  Labels as in `docs/collaboration/SCIENCE_TO_ALL.md`; **[H]** marks our reading of
a field's practice, which the prior-art workstreams (A1, A2, M) are checking.*

Theory commit referred to: `5ed4072`.  Engineering: `db56d05`.

---

## 1. The four bottlenecks

Every limitation below is one of four kinds, and it matters which, because they call for
different remedies:

| kind | the conclusion is limited by | remedy | not a remedy |
|---|---|---|---|
| **information** | what the available knowledge (model class, computed energies, measurements) determines | a different *kind* of information; or an honest set-valued answer | more computation |
| **computation** | the cost of extracting what the information determines | algorithms, structure (low treewidth, funnels), certificates that separate search from checking | more data |
| **representation** | the variables in which the problem is posed (a guarantee that is cheap in one representation and exponential in another) | change of variables / features / class | more of either |
| **meaning** | the target is not a physical observable, or a guarantee is relative to inputs nobody can supply | a different target; a different class | a sharper theorem about the same target |

The theory division's central negative result (`DEAD_ENDS.md` D28) is, in these terms, an
*information* bottleneck proved with full rigour: in a first-order class, point evaluations
do not determine `min E` or `ln Z` at sub-exponential cost.  Its lever-arm result (D42) is a
*representation* bottleneck.  Its own table "what each kind of knowledge about the residual
costs" (theory report §10) is the information axis for one kind of information.  This map
adds the other kinds, and the question of meaning.

## 2. The map

| # | what cannot be established today | kind | current practice **[H]** | the precise problem it becomes | where the programme stands |
|---|---|---|---|---|---|
| F1 | **That a computed ensemble or free energy is converged** — that no unvisited region matters | computation, with no certificate | sampling with statistical error bars that assume the relevant states were visited | two-sided certified bounds on ratios of restricted partition functions of a stated model, at realistic size; structural conditions (treewidth, funnels) under which the certificate is polynomial | verified `(+,×)` kernel with cut and elimination rules (**[V]**); no instance at realistic size (engineering E-2) |
| F2 | **Whether a disagreement between simulation and experiment is model error or sampling error** | information + meaning | goodness-of-fit and reweighting statistics computed from the same finite sample | a lower bound on the divergence of the model from *every* ensemble consistent with the data, certified independently of sampling | **new here**: `INFERENCE_LIMITS.md` Theorem 8 — data certify a lower bound on `KL(truth‖model)` and on the envelope constant; certificates are tilted partition functions (kernel-checkable); numbers on the lattice chain; prior art pending (M) |
| F3 | **What ensemble-averaged data determine about a flexible molecule's ensemble** | information | one refined ensemble (maximum entropy, Bayesian, minimal-ensemble); different methods give different ensembles | the *identified set*: the exact range of an unmeasured ensemble quantity over all ensembles consistent with data and prior class; its dual certificates; its asymptotics for chains | **new here**: exact identified sets by linear programming (model-free; with an envelope class); the theory division's limit shape (§11.22) is the asymptotic model-free identified set; widths at 15–27 beads computed; prior art pending (M) |
| F4 | **Conformational entropy from experiment** | information | entropy from per-site order parameters or low-order expansions | how well do `k`-body marginals determine the entropy, under which assumption on the energy? | **new here**: in a first-order class, not at all (Theorem 2); with interaction order `≤ k`, exactly (classical); with a high-order remainder of oscillation `ω`, to `(βω)²/4` (Theorem 7).  The assumption doing the work in practice is *low interaction order*, not smoothness |
| F5 | **Whether the observed state is the only one** (hidden or "excited" states) | information | low-population states are found when a technique happens to be sensitive to them | detectability thresholds of a hidden basin, by kind of data | **new here**: local `k`-body data bound each basin's population polynomially and not its number (Theorems 2, 3); a mean-energy datum excludes deeper hidden states and cannot exclude a hidden twin (Theorem 5, Proposition 5b) |
| F6 | **That a predicted structure is globally optimal for the stated energy** | computation, then meaning | heuristic search; learned predictors with learned confidence scores; provable discrete algorithms for pairwise rotamer models in floating point | (a) a machine-checkable certificate of optimality; (b) with model uncertainty of the order of the gaps, the meaningful object is the set of *possibly optimal* conformations, and its size | (a) verified `(min,+)` kernels, envelope duality (**[V]**; novelty of the kernels vs proof logging: pending A2); (b) contact-set theorem (**[V]**, known in substance); how many sites of a real system are sharp: pending (P) |
| F7 | **Rates and barriers with any guarantee that a faster pathway does not exist** | computation, with no certificate | pathway sampling; transition-state searches from guessed endpoints | barrier lower bounds as cut certificates; rate bounds from variational principles as partition-function certificates | absent from both branches; pending (K) |
| F8 | **Which uncertainty class a physical residual lives in** — the input of every guarantee | meaning | not asked; model error is assessed by benchmark statistics | measured bounded-difference constants along a chain, second differences, remainder of the best pair-additive fit, for real force-field terms | theory: "hypothetical until one instance is certified" (§8, §12); engineering E-3 planned on synthetic and learned residuals; a real force field: pending (P) |
| F9 | **Whether a worst-case class is the right model of ignorance at all** | meaning | — | average-case and weighted formulations with honest guarantees; tractability theorems | pending (X) |
| F10 | **Checkable justification for learned structure predictors** | meaning + computation | confidence scores calibrated on a benchmark population | proof-carrying prediction: an untrusted predictor proposes, a small kernel checks a stated property against a stated model and class | the separation of search from checking is the programme's design (**[V]** kernels); no interface to a learned proposer; the checked property is only as meaningful as F8 allows |
| F11 | **Guarantees for continuous, articulated geometry** | representation | discretise (rotamers, voxels) and ignore the remainder, or bound it heuristically | representations in which the known part is low-treewidth *and* the residual has bounded per-variable constants; for chains: local frames, pair distances, multi-scale coordinates | voxel enclosures for pairwise torsion energies (**[V]**); the lever arm destroys per-torsion constants (D42); profile classes repair it for a narrow class (§11.17); a positive tractability theorem for a physically plausible class: pending (X) |
| F12 | **Free-energy differences between structural states** (the observable free energies) | information + computation | alchemical and path methods with statistical error bars | the exact robust interval of a *ratio* of restricted partition functions over a class, with tractable dual certificates | the programme's target is the *total* `ln Z`, which a caloric curve determines without any model (Proposition 9) and whose difference to the model's is not an observable; for ratios the monotonicity argument fails and the extremal residual is not constant on either state (`INFERENCE_LIMITS.md` §7); theory report Theorem 11.35 shows averages are harder than `ln Z` |

## 3. What the map says about the programme

1. **The programme has a complete theory of the least informative corner.**  One kind of
   information (evaluations), the least structured class (first order), two targets of
   which one (`ln Z` relative to the model) is not an observable and the other (`min E`) is
   physically meaningful only where sites are sharp.  The theory is rigorous and its
   negative conclusion is, we think, correct and important.  Sharpening its exponents
   further (rounds, mean-field Potts, type classes) increases mathematical resolution
   where the scientific conclusion — "exponential; do not do this" — no longer changes.
2. **The untouched axes are the scientifically productive ones**: other kinds of
   information (F2–F5), other targets (F5, F7, F12), and the class question (F8, F9).  On
   each of them the programme's existing objects reappear with a new meaning: the weight
   cone becomes a neighbourhood of the model in which data are linear constraints; the
   kernels become dual-feasibility checkers for inference from measurements; the limit
   shape becomes an identified set; the profile class becomes the class of complete
   measurement by scattering.
3. **One physical arena closes the loop**: side-chain ensembles on a fixed backbone, where
   the known part and the standard averaged observables are single-site or pairwise in the
   rotamer variables (`INFERENCE_LIMITS.md` §12).  There a model, a class, measurements and a
   verified certificate can meet on public fixed-sequence data.  Engineering's item E-2
   already points at the same instances for a different purpose.

These three statements are our working hypotheses for prioritisation.  They will be
confronted with the reports of workstreams P (does a real residual sit near a cheap
class?), X (is there a better model of ignorance?), A1/A2/M (what is actually new?) and K.

## 4. Questions the map makes precise (candidates for requests; none sent yet)

| to | question | why it matters |
|---|---|---|
| theory | exact robust interval, extremal residuals and a tractable dual for `Z_g(A)/Z_g(B)` over an envelope class (reduction: eliminate `A` by the lower McShane extension from `B`; the rest is a linear programme in the weights on `B`) | F12: the observable free energies |
| theory | the two-oracle query model (evaluations + expectations of a restricted family of observables; + a mean-energy oracle): `θ_na` with a marginal oracle; the field case; exponents with hidden twins | F3–F5: the exchange rate between computation and measurement |
| theory | the upper boundary of the limit shape and its chord at the athermal point | F3: asymptotic identified sets for chains |
| theory | flow-with-gains certificates on product spaces checkable by a pairwise kernel | F2, F3 beyond 10 beads |
| engineering | identified sets and falsification certificates on fixed-backbone side-chain cost-function networks (the instances of E-2), first with synthetic data from a hidden truth | F2, F3 on a physical system |
| engineering | envelope constants, second differences and profile-class remainders with the protocol of our workstream P, on the residuals of E-3 | F8 |
