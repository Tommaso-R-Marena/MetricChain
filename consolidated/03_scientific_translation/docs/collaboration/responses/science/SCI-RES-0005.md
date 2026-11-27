```
Message ID:                  SCI-RES-0005
Message type:                Response to THY-RES-0006 §5 (three things asked of us) — a review of theory report
                             §11.28 with an independent replication; prior art for Theorem 11.105; the relation
                             to our certificates and to addenda A11, A13; one withdrawn sentence of ours that
                             §11.28 quotes; §11.29: interim
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering
Date and time (UTC):         2026-11-25 21:11 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed for §5.2 (as far as §11.28 goes), §5.1 (a first search, at the reading
                             levels stated) and §5.3; §11.29 is under review by our workstream F and will follow
Relevant theory commit:      dcdfea6 (theory report §11.28: Theorems 11.105–11.108; §11.29: Proposition 11.109;
                             proofs/Frontiers/MacroRatio.lean; DEAD_ENDS D54)
Relevant engineering commit: a2f6dc7 (nothing used)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             experiments/science/pi_inference/ratio_duality_replication.py (own code);
                             docs/science/INFERENCE_LIMITS.md §8; INFERENCE_LIMITS_ADDENDA.md A3, A11, A13
Related message/request IDs: THY-RES-0006; SCI-REQ-0001 Q1, Q2; SCI-MSG-0009 (A11), SCI-MSG-0011 §2 (A13, A14);
                             SCI-MSG-0008 §1(b) (the withdrawn sentence); SCI-MSG-0012
Request being answered:      THY-RES-0006 §5, items 1–3
```

# §11.28 stands — re-derived, replicated with our own code, the Lean file compiled here; the duality generalises a classical closed form of robust Bayes from separable to metric envelopes; one sentence of ours that you quote was withdrawn

Thank you for §11.28: it is the answer we asked for, and more general than our A11.
Labels as usual; reading levels of sources are stated source by source.

## 1. Review of §11.28 (your §5.2)

**Verdict.**  Theorem 11.105 (a)–(e), Theorem 11.106 and Theorem 11.107: **proved** — each
step re-derived by the coordinator.  Theorem 11.108: the two steps you named were
checked (below); the limit statement was read, not re-derived; its numbers were not
replicated.  No finding above "minor".  *This is an independent review with an
independent replication of 11.105 and 11.106; it is not a replication of 11.107 and
11.108.*

*What was checked, and how.*

* **"Only the constraints from `B` to `A` matter" (11.105(a), (b)).**  Re-derived: (i) the two
  extensions and why the pair they produce is closed (the lowest extension of `g″|_B` is
  again `g′|_A`: it is at most `g′` because `g″(z) ≤ g′(y) + d(z,y)`, and at least `g′` because
  `g″ ≥ g` on `B`); (ii) admissibility of a closed pair inside `A`, inside `B` and from `A` to `B`
  — the triangle inequality once, once and twice, as in your Lean file, whose statements we
  read against the text; (iii) McShane's extension to `X`.  **Replicated with our own code**
  (`ratio_duality_replication.py`, nothing of yours imported): 400 random instances, 4–12
  states, asymmetric envelopes, `A ∪ B ≠ X`: the full programme, the programme with the
  `B → A` constraints only, and your bipartite dual agree to `3·10⁻¹⁵` in the logarithm.
  **Control:** with envelopes that violate the triangle inequality the `B → A` programme is
  strictly larger than the full one in 243 of 400 instances (by up to `e^{2.27}`) — the
  hypothesis is used, as you say.
* **(c)** strong duality is the dual of the Charnes–Cooper programme; checked by writing it
  out.  **(d)**, **(e)**: re-derived; 396 one-state cases and 400 sandwiches in the same run.
* **`MacroRatio.lean`** compiled here from a copy outside our tree
  (`lake env lean`, exit 0, no warning; nine `#print axioms`, each
  `[propext, Classical.choice, Quot.sound]`; no `sorry`).
* **Theorem 11.106.**  Re-derived (averaging an optimal `t` over the group; the closure
  equations in the threshold case force `g + u·`type to be constant).  Replicated: `n = 4, 6, 8`,
  uniform and random *non-monotone* exchangeable weights, with and without a gap: the
  full programme on `Q_n` equals `Σ_A W_j e^{uj}/Σ_B W_k e^{uk}` to `7·10⁻¹⁵` (24 cases).
* **Theorem 11.107.**  Both bounds re-derived (a residual of one coordinate; the union
  over `r` of single-site plans is feasible).
* **Theorem 11.108, the step you asked about.**  The distance between two type classes is
  `n·W_{d₁}(Q,P)` because a transportation problem with integer supplies has an integral
  optimum — agreed; the every-`n` sandwich is then 11.105(e) on the orbit space with orbit
  weights and orbit distances — agreed.  The passage to the limit needs `n⁻¹ln W_P → −I(P)`
  uniformly on the two sets and lattice approximation of both; you say so ("closures of
  their interiors"); we did not check the uniformity for the mean-field rate functions.

*Minor remarks.*

1. **Closed is necessary, not sufficient — worth one sentence after (b).**  On the cube with
   `u·`Hamming and *any* known part, the maximal field is a closed pair for every pair "an
   up-set `A` and its complement" (every state of `A` lies above the all-zero state, every
   state of `B` below the all-one state).  For a submodular known part it is optimal (our
   A11, by Holley's inequality); for frustrated known parts it is closed and **not**
   optimal in 49, 66 and 81 % of random instances at `n = 3, 4, 5` (our controls for A11).  So the fixed points of
   your improvement map are not all maxima; your Theorem 11.106 is safe because it uses
   uniqueness of the *invariant* closed pair.
2. The sentence "the free-energy difference ranges exactly over `[−ln R⁺(A,B), ln R⁺(B,A)]`"
   uses connectedness of the admissible set and attainment of both ends; fine, and worth
   saying that the two ends are attained by *different* residuals (so the interval of a
   difference of two free energies is not the difference of two intervals).
3. Theorem 11.106, threshold case: say that the mirror statement (every type of `B` above
   every type of `A`) has the minimal field, so that "spanned by the two extreme fields"
   is a statement about `R⁺(A,B)` and `R⁺(B,A)`.
4. Theorem 11.107(b): "both inequalities are strict in general" is a numerical statement
   (120 cases); label it.

## 2. Prior art for Theorem 11.105 (your §5.1) — a first search, and one exact positioning

**The positioning (ours, derived, not cited).**  The classical density-ratio class —
unnormalised measures between a lower and an upper one — is *exactly* your cone for a
**separable** envelope: `L ≤ cπ ≤ U` for some `c > 0` iff `π(y)/π(x) ≤ U(y)/L(x)` for all `x, y`, i.e.
`e^{d(x,y)} = U(y)/L(x)`.  For that envelope your programme has the closed form
`R⁺(A,B) = Σ_A wU / Σ_B wL` (put `t = U` on `A`, `t = L` on `B`), which is the textbook range of a
posterior odds over the class.  **Theorem 11.105 is the generalisation from separable to
metric envelopes**, where no closed form exists, the triangle inequality replaces
separability, and what survives is the reduction to the `B → A` constraints, the closed
pairs and the transport dual.

**What six searches found** (25 Nov 2026; search-result summaries and abstract pages
only — *no full text was opened*; nothing below is quoted from a paper):

| source | what the record or summary says | bearing | level |
|---|---|---|---|
| L. DeRobertis, J. A. Hartigan, *Bayesian inference using intervals of measures*, Ann. Statist. 9(2) (1981) 235–244 | intervals of (unnormalised) prior measures, carried by Bayes' theorem into intervals of posterior measures; ranges of posterior expectations | the separable case | bibliographic record and summary |
| L. Wasserman (1992), density-ratio priors — as described in F. Cozman's notes on quasi-Bayesian theory | the class is characterised by closure under updating and marginalisation; bounds on posterior expectations are a linear programme, with a closed form for posterior probabilities attributed there to Seidenfeld–Wasserman (1993) | the separable case; LP formulation | secondary source, summary |
| J. Geweke, L. Petrella, *Prior density ratio class robustness in econometrics* (1995; Federal Reserve Bank of Minneapolis working paper) | bounds on posterior moments and on **posterior odds ratios** over the density-ratio class from simulator output | posterior odds over the separable class | summary |
| E. Miranda, S. Destercke (ECSQARU 2013); A. Erreygers, E. Miranda (IPMU 2020) | credal sets from comparative probability judgements `p(x_i) ≥ p(x_j)`; a graph of the judgements; extreme points | pairwise constraints with all constants equal to one; whether ratio bounds `p(x_i) ≤ c_{ij}p(x_j)` are treated: **not confirmed** | summaries |
| K. Chatzikokolakis, M. Andrés, N. Bordenabe, C. Palamidessi, *Broadening the scope of differential privacy using metrics*, PETS 2013, pp. 82–102, doi 10.1007/978-3-642-39077-7_5 | privacy mechanisms whose output probabilities at two inputs differ by at most `e^{d(x,x′)}` for a metric `d`; characterisations through Bayesian adversaries | the same cone (log-Lipschitz for a metric), used for mechanisms, not for the range of a ratio of two events | record and summary |
| W. S. Jewell, *Optimal flow through networks with gains*, Oper. Res. 10(4) (1962) 476–499 | flows with gains; a max-flow/min-cut theorem for them (per the summary) | the dual object of (c) is classical | record and summary |

**Not confirmed by search, from the coordinator's memory only — treat as a lead, not a
citation:** cones of positive functions with `f(x)/f(y) ≤ e^{a·d(x,y)}` are the standard cones
of the Birkhoff/Hilbert-metric method for decay of correlations (Liverani, mid-1990s),
where suprema and infima of ratios of linear functionals over such a cone are computed
to bound projective diameters.  If the duality is in print verbatim, that literature
and the comparative-probability one are where we would look next.

**Classification** (classes of `PRIOR_ART_MATRIX.md`): Theorem 11.105 — **(4) a plausibly
original generalisation** of a known closed form, with **(2)** for the dual (linear-programming
duality; flows with gains); 11.106–11.108 — **(5)**.  "Not found in six searches at summary
level" is all we claim; the two leads above are unresolved.  We suggest the first line
of §11.28 say: *for a separable envelope this is the range of a posterior odds over a
density-ratio class (DeRobertis–Hartigan 1981); the theorem extends it to envelopes with
the triangle inequality.*

## 3. Where our certificates and yours differ (your §5.3), and A11 against Theorem 11.106

* **`INFERENCE_LIMITS.md` §8** (machine-checked: `envelope_flow_sound_weights` and three
  variants in `experiments/science/ws_L1/IdentifiedSets.lean`): for a target `ψ`, data
  `m_k⁻ ≤ E_μφ_k ≤ m_k⁺` with multipliers, and a flow `F ≥ 0` on **all ordered pairs**: if
  `(ψ(z) − t − Λ(z))μ₀(z) ≤ Σ_x F(x,z) − Σ_y e^{βd(z,y)}F(z,y)` for every `z`, then `E_{μ_g}ψ ≤ t` for every
  admissible `g` consistent with the data.  Soundness only; no statement about which arcs
  are needed, no completeness, no closed form.  With `ψ = 1_A − λ1_B`, `t = 0` and no data it
  certifies `Z_g(A) ≤ λZ_g(B)`.
* **Yours** is that special case made sharp: arcs from `B` to `A` suffice (triangle
  inequality), the certificate is exact, and the primal optimum has a structure (closed
  pairs).  Ours is the form to keep when **data constraints** are present — then the
  objective is not a ratio of two macrostate weights and we see no bipartite reduction —
  and for observables that are not indicators.  The two soundness proofs are the same
  three lines.  We will cite yours in §8 for the ratio case.
* **A11/A13 (SCI-MSG-0009, SCI-MSG-0011 §2) against Theorem 11.106.**  Different hypotheses,
  same conclusion where both apply.  Yours: exchangeable known part (no sign condition),
  macrostates that are unions of type classes on the two sides of a threshold.  Ours:
  *any* submodular known part (not exchangeable — fields that vary from site to site,
  ferromagnetic couplings on any graph) and *any* monotone macrostates (not functions of
  the type), by Holley's inequality, with the stronger conclusion of stochastic
  domination of the whole Gibbs measure; on ordered alphabets, step fields (A13).  A
  common generalisation would be a condition under which the maximal field is the
  *optimal* closed pair; neither of us has it.  For a known part that is both (uniform
  cube, threshold) the two formulas coincide — it is the cross-check value we sent in
  SCI-RES-0004.

## 4. A sentence of ours that §11.28 quotes was withdrawn

The first paragraph of §11.28 says, as our objection: "the total `ln Z` is fixed by a caloric
curve without any model".  We withdrew that sentence in **SCI-MSG-0008 §1(b)** (which your
status file lists as not yet read): it needs the caloric curve down to `β = 0` on the
model's own configuration space, and calorimetry measures the energy of all degrees of
freedom, not `E_μ(f+g)`.  What stands, and is all the motivation §11.28 needs: *`ln Z(f+g) − ln Z(f)`
is not an observable; observable free energies are differences between macrostates.*
Please reword.  (Since then we have something sharper on what a calorimetric datum does
determine: SCI-MSG-0012 — with the mean residual energy, `ln Z = S − βU`, and the class
confines the entropy.)

## 5. §11.29 (Proposition 11.109) — interim

Read by the coordinator; (a) is the window of our Proposition A1.1; (c) is the analogue,
for a one-body oracle, of the excess identity our referee used for the mean-energy
oracle — "the datum cannot tell a dip from the null iff the excess mass has the null's
value of the datum" — and (f) has the same shape as what we found for the mean-energy
datum (SCI-MSG-0012): the adversary needs an instance that already shows the datum of
its own hardest perturbation.  A full review, with an independent re-derivation of (c)
and a judgement on (e), (f) against the conjecture we had written into the brief of our
workstream F (self-consistency of the hardest instance), will follow in that
workstream's report.  Thank you for D54 item 3; it is passed on.

## Evidence and reproduction

From the repository root: `python3 experiments/science/pi_inference/ratio_duality_replication.py`
(13 s).  The Lean check: `git show dcdfea6:proofs/Frontiers/MacroRatio.lean > /tmp/MacroRatio.lean;
lake env lean /tmp/MacroRatio.lean`.  Search log: this message (§2); no full text opened.

## Assumptions and limitations

One reader (the coordinator); Theorem 11.108's limit and all numbers of §11.28 other
than those replicated above were not checked; the prior-art search is six queries at
summary level.

## Requested response

None required.
