# R21 NOTES — adversarial review of Ensemble E5 / E7 / E8 / E1.3 / §5

Workstream R21 of the science division. Object: branch `research/ensemble-identifiability` at `a570520`,
read-only export `<ENS>` = `/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/ens_ro_a570520/`.
Write only here (`experiments/science/ws_R21/`) and `docs/science/workstreams/R21_REPORT.md`.
All times below are read from the clock (`date -u`).

## Log

* 2026-11-26T16:53Z — start. Read COMMON.md and R21_brief.md. Created this directory with `logs/` and `not_cited/`.
  Machine: 4 cores, 15 GB (7 GB available at start), Python 3.13.18.
  `<ENS>` contains: docs/ensemble/{ENSEMBLE_REPORT, PRIOR_ART, THEOREM_REGISTER, DEAD_ENDS, RESEARCH_LOG, README,
  HANDOFF, OPEN_OBLIGATIONS}.md, docs/collaboration/{ENSEMBLE_TO_ALL.md, messages/ensemble/ENSEMBLE-MSG-0001/0002.md,
  status/ensemble.md}, experiments/ensemble/{run_all.py, rigidity_checks.py, pair_capacity_checks.py,
  exposedness_checks.py, capacity_threshold.py, output.txt}, proofs/Ensemble/{Exposedness, RenyiHeppes}.lean.

## Plan (order)
1. Read ENSEMBLE-MSG-0002 §4, the report §2 (E1.3), §3.2 (E5), §3.3 (E7, E8), §5, §8; PRIOR_ART; THEOREM_REGISTER;
   SCI-RES-0026 §2. Do NOT open their scripts (`experiments/ensemble/*.py`) nor `output.txt` before my own code is final.
2. Re-derive E5, E7, E8, E1.3 on paper, hypotheses explicit.
3. Own numerics: chimera search (d=2), control that must find one; E8 certificate mean and stability.
4. Literature: the two cited theorems (open them), novelty search.
5. Re-run their `run_all.py` from `rerun_copy/` with `python3 -I -B`; compare with their `output.txt`.
6. Report.

## Tool actions declined
1. 18:46Z — the Write tool DECLINED to create `experiments/science/ws_R21/report_part_9.md` (the draft of section 9
   of the report, "Against version 2 and their internal review"). Message of the tool, verbatim: "Subagents should
   return findings as text, not write report files. Include this content in your final response instead."
   NOT worked around: I did not create that file by any other means and I did not put the text of section 9
   into `R21_REPORT.md`. As the brief prescribes for this case, the full text of section 9 is kept below in
   this file ("SECTION 9 — text kept here because the write was declined") and its findings are returned as
   text in the hand-back. Consequence: `docs/science/workstreams/R21_REPORT.md` on disk has sections 0–8 only.

## Own errors
(kept in the log below with clock times; the consolidated list of eleven is in section 8 of
`docs/science/workstreams/R21_REPORT.md`: LM smoke test with too few starts; LM threshold 1e-6 too loose on W6,
K = 3; column-generation run without cost estimate, stopped; t4b crash; t6 run 1 stopped at the time limit; four
numbers written before the tables existed; "complement needed" in m2; two clock times; estimate of the
seed-sensitivity run; Prop. A / stacking / T6(d) are a rediscovery of the Geometry division's results; my
replacement text for §5 item 2 kept "carried by".)

* 2026-11-26T16:58Z — read (in full): ENSEMBLE-MSG-0002; ENSEMBLE_REPORT.md lines 1–794 (all; object = §2.1 Cor. E1.3,
  §3.2 E5/E6, §3.3 E7/E8, §5, §8, §9); PRIOR_ART.md; THEOREM_REGISTER.md; DEAD_ENDS.md; OPEN_OBLIGATIONS.md;
  SCI-RES-0026 (so as not to repeat its §2: face criterion classical, two-line stability, smooth observables ⇒ no
  sharp minimum). NOT opened yet: `<ENS>/experiments/ensemble/*.py`, `output.txt` (only after my code is final).

### Paper review, first pass (before numerics) — review, not replication

**E5(a)** proof = dimension count: closure W_a of the splice map has dim Σ r(J_i) ≥ r(J_1)+r(J_1^c) > r = dim V,
so W_a ⊄ V, pick P_a ∈ I(V) not vanishing on im s_a. Correct. Field of definition: I(V) = ker(y_e ↦ F_e), generated
over the coefficient field (flat base change). Correct. "No F_e constant" is *redundant* in (a) for m ≥ 2 (a loop
disconnects) and vacuous for m = 1; its real role: (b) and E6 (non-trivial chimeras; B'_K proper).
**E5(b)** V ⊆ V_J × V_{J^c}, equal dims, irreducible ⇒ equal. Local realisability by constant-rank theorem. Correct.
Smallest examples: connected side m=2, D=1, F(x)=(x,x) (U_{1,2}); B_2={x_1=x_2}. Disconnected side m=2, D=2,
F(x,y)=(x,y) (U_{2,2}): every splice realisable. Loop: F(x)=(x,1): matroid disconnected, yet identification holds
(trivial chimera = a conformer) — that is why constant F_e are excluded.
**E6** correct. Weights enter in the last line through ANY single edge whose K atoms are distinct (B'_K).
  Remark: "identification = absence of chimeras" is exact only generically: for a given tuple, ONE realisable
  non-constant splice does not break identification (K=2: need a and its complement both realisable — a switching
  component). Absence of chimeras is sufficient, not necessary, tuple by tuple.
**E7** (b)⇒(a) is K=1, needs neither N ≥ d+2 nor a cited theorem (with (a) defined as "every generic p").
  (a)⇒(b): GGJ Thm 3.5 (to be opened) + E6 + "each x_i generic". GHT only needed to identify "generically globally
  rigid" (every generic p) with the usual graph property (some generic p), and to upgrade the negative side to
  "no generic ensemble is determined" (replace x_1 by an equivalent non-congruent q_1). Implicit hypotheses:
  - "generic tuple" = JOINTLY generic (all dNK coordinates alg. independent over Q). "Each conformer generic" is
    NOT enough: (i) conformers sharing a rigid part (K_5−e, shared triangle, vertices 4,5 moved independently:
    chimeras (T,P4,P5'), (T,P4',P5) ⇒ ½δ_x1+½δ_x2 and ½δ_y+½δ_y' same laws) ; (ii) even with no coincident edge
    length there are special pairs with a switching component (K_4: 12 equations, 20 effective unknowns) — to be
    exhibited numerically.
  - congruence = full Euclidean group incl. reflections, separately for every conformer (chirality of each
    conformer undetermined).
  - ν arbitrary Borel measure on the UNCONSTRAINED space (R^d)^N; μ finite, point conformers.
  - congruent conformers are excluded by genericity (equal lengths ⇒ tuple ∈ B'_K) but can be merged.
  - "generic" can be weakened to "outside a proper algebraic subset" (semi-algebraic + nowhere dense).
  - NOTE for the control of Item 3: "rigid but not globally rigid" does NOT imply chimeras. Two K_4 glued along an
    edge (N=6, plane): not 3-connected ⇒ not GGR, but R_2 is connected (2-sum of circuits) ⇒ no chimera for generic
    tuples; identification fails through the flip (K=1), not through a chimera. A control "that must find one"
    needs a DISCONNECTED matroid (K_4 + degree-2 vertex; K_4 − e; triangle) or non-generic conformers.
**E8** correct given E7: ∫f dν = ∫f dμ = 0 ⇒ every ℓ_e² ν-a.s. among the K atoms; weights by Vandermonde from moments
  0..K−1 of any one edge. The certificate mean does not see the weights at all. "2K per edge" sufficient, not
  necessary: (K=1) if (G,x) has a PSD equilibrium stress matrix of rank N−d−1 (e.g. K_N generic), then first
  moments of all edges + second moments of d(d+1)/2 edges with directions not on a conic identify δ_x among all
  ensembles: f = Σ ω_e ℓ_e² + Σ_{E_2}(ℓ_e² − ℓ_e(x)²)²; |E| + d(d+1)/2 means instead of 2|E|. And redundant edges
  need no moments: a GGR spanning subgraph suffices (2K|E'|).
  Stability: Markov with the certificate: ν(f ≥ γ) ≤ ‖c‖_1 ε/γ; meaningful iff ε ≪ γ*/‖c‖_1 with γ* the value of f
  at the best near-chimera. To be put in numbers (own code).
**E1.3(b)** proof = random scaling R² ∈ {0,2}; correct on (R^d)^N; does not need a mixture (works for δ_x). The
  coordinator's guess (affine images, Σ p_k A_k^T A_k = I) is the general mechanism; theirs is A = R·I.
  READING: the statement is about the unconstrained configuration space. With prescribed lengths on a set B of
  pairs (bonds) scaling is unavailable and the statement REVERSES: Prop. (mine, to be checked numerically):
  on X_B = {p : |p_u−p_v| = L_uv, uv∈B}, for x affinely spanning, δ_x is determined mod congruence among all
  ensembles on X_B by the mean squared distances of all pairs IFF the bond directions of x do not lie on a conic
  at infinity. (If: E Gram(p) = Gram(x), Gram(p) ⪰ 0 ⇒ range Gram(p) ⊆ range Gram(x) ⇒ p = xA+b; bonds ⇒ AAᵀ = I.
  Only if: S ≠ 0 symmetric with d_e S d_eᵀ = 0 on B; p_{±t} = x(I ± tS)^{1/2} ∈ X_B, squared distances linear in t ⇒
  ½δ_{p_t}+½δ_{p_−t} has the means of δ_x.) B = ∅ is E1.3(b). Certificate ‖P^⊥ b(p)‖² = the d ≥ 1 analogue of their
  own E10 certificate; for unit bonds in d = 1 the mean squared distances ARE the pair correlations of Part III.
  For K = 2 generic chain conformers: T = S − I/2 must vanish on generic points of the quadric |b¹|² = |b²|²
  ⇒ T ∝ diag(I,−I) ⇒ S ∈ {S_1,S_2}: identified when #bonds ≥ d(2d+1) − 1 (heuristic count, to be tested).

* 2026-11-26T17:11Z — own code: `r21_common.py` (sqlen, rigidity matrix, brute-force matroid separators, stress-rank
  test, batched LM `Realiser`, exact tests), `t1_graphs.py`. Run `logs/t1_graphs_run1.log` (reached DONE; 4 s):
  K4, K5, K5-e, W5, K6, W6, K33+e are GGR (stress rank N−3; 3-connected + redundantly rigid) with connected matroid;
  K3, K4-e, K4+deg2, K33, prism not GGR, matroid NOT connected; **2K4_edge and 2K4_2sum: not GGR (κ = 2) but matroid
  connected (0 separators)** — confirms the note on the control. 0 consistency violations.
* 17:12Z — first smoke test of the LM chimera search (W5, K=2, 6 starts): the planted control FAILED for 11/200 and
  2/200 realisable targets (per-start success only ≈ 0.65 on W5, ≈ 0.48 on K33+e, ≈ 0.998 on K5; the hardest 1 % of
  targets succeed in ≈ 5 % of starts). OWN-ERROR-AVOIDED: a local search with few starts is not a proof of absence.
  Remedy: (i) 30 starts for K=2; (ii) a second, exhaustive method `Constructor` (ruler-and-compass enumeration of all
  2^(N-3) realisations of a spanning degree-two-extension subgraph, then compare the check edges). Validation of
  the exact method (probe, not logged as evidence): 2000/2000 planted realisable targets found on each of 11 graphs,
  max defect 9e-12; perturbed targets rejected.
* 17:17Z — launching T2 batch. Cost estimate (measured 0.5 ms per LM solve): K=2 runs ≤ 3 min each; K=3 runs on
  10-edge graphs: 59 046 colourings × 10 starts ≈ 5 min per ensemble, 2 ensembles ⇒ ≈ 10 min per graph, < 1 GB.
  At most two processes at a time, OMP_NUM_THREADS=1.

* 2026-11-26T17:30Z — T2 results so far (logs reached DONE; `logs/t2_<graph>_K<K>_run1.log`), all "chimeras found = 0":
  W5 K=2 (10 ens, 2540 colourings; min LM residual 3.5e-4; min exact defect 2.3e-3; 0 control violations);
  K5-e K=2 (5100; 2.4e-3; 5.3e-3; 0); K5 K=2 (10220; 6.3e-3; 1.5e-2; 0); W6 K=2 (10220; **4.4e-6**; 1.5e-4;
  6 LM planted-control misses = 2/200 in three ensembles, per-start success 0.33); K33+e K=2 (10220; 1.0e-5; 5.2e-5;
  8 LM planted misses); W5 K=3 (19674; 3.4e-5; 1.4e-4; 2 LM planted misses); K5-e K=3 (39360; 1.3e-4; 1.2e-4; 0).
  Reading: (i) no chimera (both methods); (ii) the LM search alone misses ≈ 1 % of realisable targets on the sparse
  6-vertex graphs with 30 starts — the EXACT method misses none of 200·n_ens planted targets; (iii) the smallest
  residuals are 1e-5…1e-3 in units where squared lengths are ≈ 4: the "chimera gap" is tiny already at K=2,3.

### Literature opened so far (via WebFetch = a fetch tool that returns a model-written extraction; "quotes" are as returned by that tool)
* GGJ 2022 = Garamvölgyi, Gortler, Jordán, "Globally rigid graphs are fully reconstructible", arXiv 2105.04363
  (abs page opened: v1 10 May 2021, v2 3 June 2022, related DOI 10.1017/fms.2022.44; ar5iv full text opened, chars
  0–140k in two calls). Theorem 3.5 as returned: "Let G=(V,E) be a globally rigid graph in ℝ^d on n≥d+2 vertices.
  Then G is ℛ_d-connected." Lemma 3.1 (product for rank-additive partition), Lemma 2.13 (dim M_{d,G} = r_d(G)),
  generic = n·d coordinates algebraically independent over ℚ; globally rigid graph = "every (equivalently, if some)
  generic realization"; measurement variety over ℂ, defined over ℚ. Proof of 3.5: not ℛ_d-connected ⇒ (x1, 4x2) ∈
  M_{d,G} (lengths of p on E1, of 2p on E2) is realised by a generic q with the same stress space, not an affine
  image ⇒ contradiction with Thm 2.8 (GHT-type). **So the splice of p and 2p along a separator is already the
  engine of the published proof.** d ≤ 2 case attributed to ref [14] = Jackson–Jordán, JCTB 94 (2005) 1–29.
  Sections 4–5: nothing on several frameworks / pooled lengths / disjoint unions of copies.
* GHT 2010 = Gortler, Healy, Thurston, "Characterizing generic global rigidity", arXiv 0710.0926 (ar5iv, chars 0–100k
  of 167k): Def 1.4 generic; Thm 1.13 (Connelly), Thm 1.14 (d+2 or more vertices), Cor 1.15 "Either all generic
  frameworks in C^d(Γ) of a graph are globally rigid, or none of them are."; ≤ d+1 vertices: globally rigid iff complete.
* GTT 2019 = Gortler, Theran, Thurston, "Generic unlabeled global rigidity", arXiv 1806.08688 (ar5iv, chars 0–100k of
  111k): Thm 1.5 (one generic configuration from the unlabeled edge lengths), Thm 3.4 (M_{d,G} = M_{d,H} ⇒ G = H up to
  relabeling); nothing on several configurations.
* Yao–Peng–Tsakiris, "Unlabeled PCA", arXiv 2101.09446 (ar5iv, chars 0–100k of 162k): Thm 2: generic X* of rank
  r < min(m,n), entries permuted inside each column; unique min-rank completion up to a row permutation. No matroids.
* Dokmanić et al., PNAS 110 (2013) 12186 (PMC3725100 opened): Thm 1: microphones uniformly at random ⇒ unlabeled
  first-order echoes specify the room with probability 1; echo sorting by the EDM rank test. Genericity on the SENSORS,
  room arbitrary — the opposite quantifier to E5. (Commentary PMC3725052 by Plumbley also opened.)
* Hays, Boland, Kasson, arXiv 2010.15612 (ar5iv opened): joint conformational distributions from separately acquired
  DEER distributions; no uniqueness theorem; the rest is supplied by MD + a reference ensemble.
* Search summaries only (not opened): Boutin–Kemper math/0311004; Boutin 2111.10834; Lemke–Skiena–Smith (turnpike
  survey, DIMACS TR 2002-37); arXiv 2402.03787 (beltway over orthogonal groups); Wu–Yang 1807.07237 (2k−1 moments,
  Lindsay 1989 Thm 2A); heterogeneous MRA (Boumal et al. 1710.02590; Perry et al. 1707.00943); Gortler–Thurston
  1001.0172, Connelly–Gortler–Theran 1605.07911 (super stability, conic at infinity); uDGP surveys (Liberti et al.).
* Queries used (all generic): see the search log in the report §6.
* 17:34Z — batch A (K=2) finished; K6 K=2: 98 298 colourings (3 ens), no chimera, min LM residual 3.6e-2. K5 K=3:
  118 092 colourings, none, min LM residual 1.3e-2. Batch B (W6, K33+e with K=3) still running.
* 17:35Z — launching T3 controls (`t3_controls.py`), cost estimate ≈ 8 min, < 0.5 GB (one process; batch B is the other).

* 17:37Z — T3 (a) done inside the running log: K4+deg2, 40 generic pairs: closed-form prediction 160 chimeras (40/40 pairs
  have at least one); LM found 160/160, EXACT 160/160, 0 false positives.  => the control "must find one" is passed.

### Draft of findings (to be turned into the report; classes tentative)
No critical finding: E5, E6, E7, E8, E1.3 are proved as stated in the REPORT (definitions on lines 434–436 included).
MAJOR
 M1 E1.3 reading. True on the free space (R^d)^N only. With prescribed lengths on a set B of pairs (any molecule):
    Prop A [P]: delta_x (affinely spanning) is determined by the mean squared distances of all pairs among all
    ensembles on X_B iff the B-directions of x are not on a conic at infinity. So "mean squared distances determine
    nothing, not even a single conformation" is false for chains with fixed bond lengths; their own Part III is the
    d = 1 instance (unit bonds on a line: pair correlations of bond signs are linear in the squared distances).
 M2 "generic" = jointly generic. Counterexamples with each conformer generic: (i) K4, explicit rational pair with no
    common edge length (kites A, B with the same two values of the 6th length): 1/2(x1+x2) and 1/2(y+y') same laws;
    family of codimension 2 in pair space. (ii) K5−e (GGR), shared rigid triangle, two vertices moving independently.
    Hence GGR of G is not the right criterion for conformers that share rigid parts; §8/O3 "contraction" is a guess.
 M3 exactness. No stability statement; Prop B [P]: with a band tau on every law (sup norm on atoms, mass slack eta_e),
    nu is within tau of the conformers up to mass sum eta_e PROVIDED tau < chimera gap; numbers from T2/T5: gap
    1e-3..1e-2 (K=2), 1e-5..1e-4 (K=3 or sparse 6-vertex graphs) in units where squared lengths are ~4.
    E8: certificate not sharp (quadratic) => Hölder-1/2 at best; tolerated moment error: T4.
 M4 novelty classes: E5 "new (not found)" -> elementary dimension count; the published proof of GGJ Thm 3.5 itself
    realises a splice (lengths of p on E1, of 2p on E2) along a separator. E7 -> corollary of GGJ 3.5. E8 -> classical
    per-edge 2K-moment certificate + E7. The ensemble READING was not found in my searches either.
MINOR
 m1 "no F_e constant" redundant in E5(a) (m >= 2); needed for (b)/E6.  m2 "identification = absence of chimeras"
 only generically (one chimera does not break identification; a switching component does).  m3 (b)=>(a) needs no
 cited theorem; GHT gives the full dichotomy (not GGR => NO generic ensemble determined).  m4 congruence includes
 reflections, conformer by conformer.  m5 2K|E| sufficient, not necessary (redundant edges; K=1: |E| + d(d+1)/2 for
 super stable frameworks; (2K−1)|E| among ensembles with <= K conformers).  m6 "j <= 2 certifies a single
 conformation": only if the truth is generic — data cannot certify genericity; but a finite a-posteriori check can
 replace genericity (enumerate the K^m splices).  m7 §5 item 2 "exactly the ensembles carried by ground states":
 contradicts their Example E1.2 on continua; omits affine independence.  m8 §5 item 4: E5 is for polynomial maps on
 R^D; torsion maps need the (easy) extension to irreducible varieties, and genericity is then in torsion space.
 m9 "rigid but not globally rigid" does not give chimeras (2K4 glued: connected matroid): for d >= 2 the chimera-free
 graphs (connected matroid) are strictly more than the GGR ones; ensemble-specific content of E7 is connectivity.
 m10 "generic" can be weakened to a Zariski-open set (GHT Cor 1.15).  m11 "nothing about fluctuations": the rank of
 the mean Gram matrix exceeding d certifies that the ensemble is NOT one conformation.

### Reading for data (draft, [H] unless marked)
 * laws vs moments vs means of nonlinear functions: E7 needs exact atomic laws; E8 exact moments <l^2>..<l^{4K}>.
   One mean per edge of a homogeneous function (r^-6): scaling counterexample as in E1.3 (T6 b) on the free space.
   Per-edge certificates need a non-negative function in the span with K double zeros: >= 2K functions per edge.
 * band: gap ~ (K^m)^(-1/c), c = m − (dN − d(d+1)/2) [H, to compare with T5]; with relative band tau need
   c >~ m ln K / ln(1/tau): the graph must be redundant by a factor 1/(1 − ln K/ln(1/tau)).
 * separate samples per edge: exactly the model; but label linkers make each measured "conformer" a distribution.
 * conformers as distributions: not covered (E8.1); basin means are not edge lengths of one configuration.
 * shared rigid domains: intra-domain edges are constant (loops on the chain's configuration space); for hinge
   states the data are the marginals of the joint state distribution on the hinge sets spanned by each edge — a
   discrete marginal problem (their Part III), not E7.
 * a-posteriori certificate replaces genericity at cost K^m realisability tests.
* 17:41Z — T3 finished (`logs/t3_controls_run1.log`, reached DONE). (a) 160/160 predicted chimeras found by LM and by
  EXACT, 0 false positives; (b) K5−e with shared triangle: 320 predicted chimera colourings, EXACT 320, LM 319 (one
  miss with 12 starts), same laws to 0.0e+00, chimeras not congruent to conformers (0.218); K5 with the same
  conformers: 0 chimeras; (c) 2K4_edge / 2K4_2sum: 0 chimeras in 10 pairs × 2046 / 1022 colourings, flip changes no
  measured length (1e-14) and an unmeasured one by ≥ 0.70; (d) explicit rational K4 pair verified in exact
  arithmetic; search finds exactly the two complementary chimeras; 20/20 random members of the family.
  Total violations of predictions: 1 (the LM miss).
* 17:42Z — T4 first test (K4, K=2, 1 instance, 13 s, not logged): works. Certificate mean 9e-28; C_abs 7.7e4;
  split exponent 2.00; 0 non-conformer zeros in 6000 LM runs; Markov guarantee needs eps <= 1e-8..1e-10 while the
  plain LP adversary already puts 25 % of the mass at D >= 0.3 with relative moment error 1e-4.
* 17:43–17:53Z — OWN ERROR: started a column-generation variant of T4 in the foreground WITHOUT a cost estimate; it
  ran past the 10-minute tool limit (200 LPs with ~5000 dense columns), was moved to the background and I stopped
  it (TaskStop) at 17:53Z. Nothing from that run is cited (no log file was written). Fix: profile first, fewer
  rounds, smaller first candidate set.
* 17:54Z — batch B finished (`logs/t2_W6_K3_run1.log`, `logs/t2_K33+e_K3_run1.log`, both reached DONE).
  K33+e K=3: 118 092 colourings, 0 found, min LM residual 5.3e-6, min exact defect 1.8e-5; LM planted misses 18/400.
  **W6 K=3: the log says "chimeras found=1"**: in ensemble 0 one colouring (#56110, 2211222020) has LM residual
  7.9e-07 < my pre-set LM threshold 1e-6, while the EXACT defect of the same colouring is 2.3e-06 (> 1e-9): the two
  methods disagree at that threshold. Control violations in that run: 30 (LM missed 14 + 15 of 200 planted targets
  and one of the three conformers in ens 0 with 10 starts: LM power on W6 at 10 starts ≈ 93 %). EXACT: 0 violations.
* 17:57Z — follow-up `t2b_w6_followup.py` → `logs/t2b_w6_followup_run1.log` (reached DONE, 15 s). Same ensemble
  reproduced (same seed and draw order). The residual of that colouring is 7.9229962e-07 after 120, 1000 and 5000
  LM iterations (400 starts each; ≈ 100 starts reach the same value), gradient norm 1e-14, smallest singular value
  of the Jacobian 0.28, unchanged by 60 Gauss–Newton steps; the three conformers reach 1e-16 under the same
  procedure. => a converged POSITIVE minimum: a near-chimera at squared-length distance 7.9e-7, not a chimera.
  The threshold 1e-6 was fixed before the run and was crossed once; the count "1" stays in the log and is reported
  together with this follow-up. Realisable targets end below 1e-9 (controls), so a threshold of 1e-9 would have
  been the consistent choice; I do NOT relabel the old logs.
* 17:58Z — T4 smoke tests (not logged as evidence) OK after dropping column generation: LP over an explicit
  candidate set of two sizes, candidates with normalised moments > 30 removed, tolerances 1e-9 (achieved error = eps).
  Launching: `run_t4.sh` (K4, W5; K = 1, 2, 3; 3 instances each; ≈ 1–3 min per run) and `t6_e13_reading.py` (≈ 5 min).
* 18:05Z — T4 batch finished (`logs/t4_{K4,W5}_K{1,2,3}_run1.log`; run_t4_done). K4: K=1 Markov bound and LP adversary
  agree within a factor 2 (far mass at D>=1 ≈ 400–800·eps); K=2 adversary 200–1500·eps while the certificate's own
  bound needs eps <= 1e-8; K=3 adversary: 3 %–76 % of the mass far at eps = 1e-5, certificate bound eps <= 1e-12..1e-19.
  CONTROL VIOLATION to report: in T4 part (3) (zeros of f by LM), K4 K=3 instance 1, conformer 1 was reached by 0
  of 6000 runs (the other two by 41 and 597): the LM search for zeros of f does not find every known zero.
* 18:05Z — launching T5 driver C (`run_t5_C.sh`: K4 K=2..6, W5 K=2..4, K5-e K=2..4; 8 ensembles, 12 starts; each run
  ≈ 1–3 min, driver ≈ 20 min total, < 1 GB). T6 still running (part (d) ≈ 1.5 min per bond count).
* 18:06Z — reading the six T4 logs as a table BEFORE using them:
  (i) part (3) "non-conformer zeros of f: 0" in all 18 instances, but its control (every conformer must be reached)
      FAILS in 4 instances: K4 K=3 inst 1 reached [41, 0, 597]; W5 K=3 inst 0 [4, 5, 0], inst 1 [0, 10, 2], inst 2
      [6, 0, 11] (only 9–17 of 6000 runs reach any zero). In those four the "0" is uninformative. 14/18 pass.
  (ii) the M3 numbers I had already written into the report came from K4 only; W5 is much worse at K=2
      (14–62 % far mass at eps = 1e-5). To be rewritten per graph from the full table.
  (iii) LP: 287 entries, achieved relative error <= 1.05 eps in all; 1 LP failure (status 1, K4 K=3, r=0.3).
  (iv) W5 K=1 inst 0: positive local minimum f = 5.9e-9 at D = 0.635 — followed up.
* 18:06Z — `t4b_w5_followup.py`: first run crashed (np.cross on 2-vectors) → `not_cited/t4b_w5_followup_run1_FAILED_np_cross.log`
  (OWN ERROR, coding); fixed, `logs/t4b_w5_followup_run2.log` reached DONE. Result: same generator and draw order;
  the K=1 framework x (seed 2104, W5) is infinitesimally rigid (7 nonzero singular values, smallest 0.17) with
  stress rank 2 = N−3; the residual ||t(p) − t(x)||_2 has a second minimum 7.7071124e-05 (f = 5.94e-9) at D = 0.635,
  identical after 300 and 3000 iterations, gradient 4e-14, Jacobian min singular value 0.29, reached by ≈ 1000 of
  3000 starts (x itself by ≈ 800). => converged POSITIVE minimum: x is globally rigid, but a visibly different
  framework (vertex 4 flipped across the thin hub triangle (0,3,4), area 0.042) has all 8 squared lengths within
  7.7e-5. A "near-flip": the K = 1 analogue of the chimera gap. Explains Markov eps <= 3e-7 for that instance.
  T4 table (r = 1, larger candidate set; far mass at eps = 1e-3, 1e-4, 1e-5; three instances each):
   K4 K=1: .37/.042/.0043  .77/.081/.0083  .073/.0075/.00075      Markov eps(10%): 1.0e-4..7.6e-4
   K4 K=2: .28/.038/.0043  .92/.15/.017    .18/.021/.0022                           3.5e-9..4.6e-8
   K4 K=3: .59/.15/.027    1/1/.76         1/.58/.30                                1.8e-19..1.1e-12
   W5 K=1: .24/.028/.0030  1/.11/.013      .11/.012/.0012                           3.1e-7..9.4e-5
   W5 K=2: .81/.28/.14     1/.83/.24       1/1/.62                                  2.0e-12..8.0e-11
   W5 K=3: 1/.97/.57       .91/.51/.14     1/.78/.28                                5.6e-18..2.7e-15

* 18:11Z — COORDINATOR'S NOTE received (mid-task): the Ensemble division published checkpoint 2 (commit 1a067b5,
  18:07 UTC) with VERSION 2 of its report, to which their own internal adversarial review (ER1) has been applied.
  Instructions: (1) finish on a570520, my findings must be reached without their review; (2) only AFTER my own
  findings are written down read ENSEMBLE-MSG-0003 §2 and §2a (and the review); (3) add a section "Against version 2
  and their internal review": for each of my findings — repaired in v2 (line)? found by their review? what of mine
  is not in theirs? — and the two or three findings of theirs that I missed; (4) do not review E7', Parts IV, V
  (one sentence on whether E7' answers the shared-rigid-part limitation); (5) header: which version each part
  refers to; keep a570520 line numbers for my findings. Second read-only export:
  /tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/ens_ro_1a067b5/ (never write).
  The note itself told me three things about their review before I had frozen my findings (so these are NOT
  independent on my side from 18:11Z on): (a) "identification = absence of chimeras" and "identified exactly when
  the zero set contains nothing but the conformers" are withdrawn in v2 — my m2 says the same and was in this file
  at 17:04Z and in the report draft at 18:03Z, i.e. before the note; (b) their reviewer has an OPEN set of pairs on
  K4 + degree-2 vertex with three realisable chimeras and an identified ensemble — I did not have that; (c) the
  exact criterion is uniqueness of a non-negative table on the realisable colourings with the right marginals.
* 18:11Z — OWN ERROR found while re-reading m2 after the note: I wrote (here at 17:04Z and in the report draft)
  that for K = 2 "a colouring AND ITS COMPLEMENT" are needed to break identification. That is sufficient, not
  necessary: any non-negative weighting of realisable non-constant colourings in which every edge receives the
  same total weight of each conformer does it — e.g. three colourings whose 1-classes partition the edge set,
  with no complementary pair among them. The correct general criterion is the uniqueness of the non-negative
  table (which I had only in my head, not in writing; in writing it is THEIR formulation). To correct in the
  report (m2, Prop. B wording: g2 is a sufficient threshold for failure, not the exact one).
* 18:11Z — state of my own findings at this moment (frozen before I open anything of version 2): report sections
  1 and 2 (M1–M4, m1–m10, Props A, B, C, Examples D1, D2) written 18:03Z; T1–T4 results in; T5 (driver C) and T6
  run 1 running; T7, T6 run 2, T5 driver D, and the re-run of their a570520 script still to do.
* 18:12Z — T5 driver C finished (all 11 logs reached DONE). g1 (median over 8 ensembles; LM distance in squared-length
  units, mean squared length = 4): K4: K=2 3.2e-2, K=3 2.3e-3, K=4 2.8e-4, K=5 8.1e-5, K=6 1.7e-5 (heuristic
  1/#splices: 1.6e-2, 1.4e-3, 2.4e-4, 6.4e-5, 2.1e-5 — within a factor 2); W5: 1.1e-3, 2.4e-5, 6.8e-6; K5-e: 3.7e-2,
  3.2e-3, (K=4: see log). Switching gap g2 (K=2, complementary pairs): K4 0.22, W5 0.025, K5-e 0.24.
  Launching T5 driver D (K5 K=2..4, W6 K=2,3, K6 K=2,3; each run ≈ 2–5 min, < 1.5 GB; K5 K=4 enumerates 1 048 572
  colourings, K6 K=3 samples 2 000 000 of 14 348 904).
* 18:17Z — OWN ERROR (cost estimate): `t6_e13_reading.py` run 1 (started 17:58:06Z) was estimated at ≈ 5 min; its part
  (d) took ≈ 1.5 min per bond count and it reached 19 min with two bond counts left. Stopped by me (TaskStop) before
  the 20-minute limit; log moved to `not_cited/t6_e13_reading_run1_STOPPED_at_20min.log` and NOT cited. What it
  had printed (for my own orientation only): (a)–(c) as predicted; (d) 4–6 bonds continuum of chains x1A1 + x2A2,
  7 bonds finitely many extra chains in 19/20 instances (median 2, max 4), 8 and 9 bonds none in 20/20.
  Remedy: (a)–(c) stay in `t6_e13_reading.py` (now also prints the control "zeros congruent to x reached");
  (d) split off into `t6d_two_conformer_chains.py <n_bonds>`, one short run per bond count, with the identification
  test (LP over the solutions found: largest mass off x1, x2 with the same mean squared distances) and the control
  (x1 and x2 must be reached).
* 18:17Z — launching `run_t7_t6.sh`: T7 (≈ 2 min), T6 (a)–(c) (≈ 1 min), T6d for 4,5,6,7,8,9,10,12 bonds (12 instances,
  2000 starts; ≈ 1 min each). One process; the other is T5 driver D.
* 18:23Z — T5 driver D finished (all logs DONE). Full table: `logs/summarize_t5_run1.log` (from `summarize_t5.py`).
  One value needed a look before use: W6, K=3, ensemble 2 (seed 2105): g1 = 1.190e-09, min exact defect 5.4e-07 —
  three orders below the other five ensembles (1e-5..2e-6) and below the LM "found" threshold of T2.
* 18:24Z — follow-up `t5b_w6_followup.py` → `logs/t5b_w6_followup_run1.log` (DONE, 49 s). Random stream replayed exactly
  (replay reproduces g1 of ens 0,1,2). Colouring 2012211122 (1, 4, 5 edges from conformers 0, 1, 2). Three
  independent checks agree that the residual is POSITIVE: (i) LM: 1.1901008e-09 after 1 000 and 10 000 iterations
  from the minimiser and from 126–127 of 400 random starts, gradient 2e-14, Jacobian singular values 0.58..8.5;
  (ii) EXACT: check-edge deviation +5.387894e-07 for the nearest flip pattern (the only other feasible pattern
  within 1e-2: −2.0e-3); (iii) 40-digit arithmetic (mpmath), float targets taken as exact: the stationary point
  of ||F − t||² found by Newton lies 2.9e-15 from the float minimiser and has residual 1.19010123465522e-9.
  => a near-chimera to nine digits, not a chimera. Why so small: the hub triangle (0,4,5), all three edges from
  conformer 2, has area 1.1e-3 (three nearly collinear points in that random conformer); the hub angle is then
  ~1/area times more sensitive to the lengths, so a defect of 5.4e-7 on the check edge is absorbed by changes of
  1e-9 in the lengths of the thin triangle. A nearly degenerate conformer shrinks the gap by the area factor.
* 18:24Z — T7 done (`logs/t7_fewer_means_run1.log`, DONE, 0 violations): Prop. C on K4 and K5, 10 frameworks each:
  Omega psd of rank N−3 in 10/10, 20000/20000 minimisations reach a zero congruent to x, 0 non-congruent zeros;
  negative control (two edges in E2): 20000 non-congruent zeros. T6 (a)–(c) run 2 done
  (`logs/t6_e13_reading_run2.log`): 3, 4, 6 bonds: 8000/8000 minimisations reach a zero congruent to x, 0 others;
  2 bonds: f ≡ 0 (8000 non-congruent zeros); degenerate 3-bond conformation: explicit 50/50 mixture (errors 1e-15).
  T6d: 4 and 5 bonds: an explicit ensemble with the same mean squared distances and mass 1.000 off {x1, x2} in
  12/12 instances (NOT identified). Remaining bond counts running.
* 18:25Z — my test code is final (T1–T7, T2b, T4b, T5b, T6d written; all have run; T6d runs for 6–12 bonds still in
  progress with unchanged code). ONLY NOW opened `<ENS>/experiments/ensemble/`: `run_all.py` (24 lines) runs
  exposedness_checks.py, rigidity_checks.py, pair_capacity_checks.py through subprocess and WRITES `output.txt`
  next to itself — hence the scratch copy. Copied the five .py files and their `output.txt` (as
  `output_theirs_a570520.txt`) into `rerun_copy/` (sha256 of the copies = sha256 of the originals, see log below).
  Re-run: `cd rerun_copy && OMP_NUM_THREADS=1 python3 -I -B run_all.py`; their docstring says ≈ 10 minutes
  (cost noted here before the run; one process; < 1 GB expected).
* 18:29Z — RE-RUN of their code: `cd rerun_copy && OMP_NUM_THREADS=1 python3 -I -B run_all.py` → exit 0, "ALL PASS",
  2 min 47 s (`logs/rerun_run_all_a570520_run1.log`; their output is in `rerun_copy/output.txt`). `diff` with their
  `output.txt`: identical except the three header lines with timings (41/113/13 s here, 39/102/17 s theirs).
  READ ONLY (`rigidity_checks.py`, 240 lines, read in full; the other scripts only grepped for imports and file
  operations): (i) their "wheel W5" is the wheel with FIVE spokes on six vertices (my W6). (ii) R3 examines 180
  random splices of 3 pairs (K = 2 only) with scipy `least_squares` (trf), 25 starts, pass threshold "> 1e-6"; the
  only control of the solver is one conformer per pair. On that graph my searches have per-start success 0.33
  and the smallest residuals over ALL splices are 4e-6 (K=2, one of 10 ensembles) and 8e-7, 1e-9 (K=3): their
  threshold would be crossed by true negatives. (iii) R5: report line 502 says "all 22 zeros"; their own
  output.txt and my re-run say "82 zeros found in 400 starts; 1 at conformer 1, 81 at conformer 2": the number in
  the report is stale, and the control "both conformers are reached" passes by ONE hit. (iv) R2 uses the
  Cayley–Menger determinant (a value, not a distance) — fine as a non-vanishing test for K_{d+2}. (v) R4(b) tests
  one colouring (K4 from x1, both pendant edges from x2). (vi) R6 exists in the script and in output.txt but is
  not described in the report text (lines 492–503 list R1–R5).
* 18:30Z — launching `rerun_seed_sensitivity.py` (THEIR functions test_R5 with seeds 1..20 and test_R3 with seeds
  1..4, only the seed line changed): estimate ≈ 6 min, one process.
* 18:31Z — `run_t7_t6.sh` finished (DONE 18:30:32Z). T6d (12 pairs per bond count, 2000 starts): 4, 5, 6 bonds — a
  continuum of chains x1A1 + x2A2 and an explicit ensemble with the same mean squared distances and mass 1.000 off
  {x1, x2} in 12/12 (NOT determined); 7 bonds — 2–4 extra chains in 11/12 but the table is unique in 12/12
  (determined); 8, 9, 10, 12 bonds — no extra chain in 12/12 (determined); control (x1, x2 reached) passes in
  12/12 from 7 bonds on. For >= 9 bonds the quadrics through the bond vectors are the multiples of diag(I,−I)
  (dimension 1 in all instances) — then S ∈ {S1, S2} is a proof.
* 18:36Z — T8 (`t8_table_criterion.py`, `logs/t8_table_criterion_run1.log`, DONE, 4 s): written AFTER the coordinator's
  note; replication with my own tools of the finding of THEIR internal review that was relayed in that note.
  K4 + degree-2 vertex, 400 random pairs, weights 0.4/0.6, realisable colourings by EXACT, uniqueness of the
  non-negative table by LP: 399 pairs have a chimera; 121 of them are determined all the same (26 with one
  chimera, 29 with two, 66 with three), 278 are not. So "identification = absence of chimeras" fails on a set of
  pairs of positive measure — their finding, replicated. W5 and K5−e (connected matroid): 400/400 pairs without
  chimera, determined.
* 18:38Z — FREEZE of my own findings before opening anything of version 2 (commit 1a067b5). On disk at this moment:
  the report with sections 0–8 (copy: `logs/R21_REPORT_frozen_before_v2.md`; sha256 of the report and of the part
  files in `logs/freeze_before_v2_sha256.txt`). Findings: M1 (reading of E1.3; Prop. A; chains), M2 (jointly generic;
  D1, D2), M3 (exactness; Prop. B; gap table; E8 numbers), M4 (novelty classes), m1–m10, five remarks on their
  scripts (§4), Prop. C. Still running, started 18:30Z and independent of anything I read from now on: the
  seed-sensitivity re-run of THEIR functions R5/R3 (numbers to be added to §4 and to line 9 of §0).
  Known influence of version 2 on the frozen text, through the coordinator's note of 18:11Z only: the corrected
  wording of m2 (unique non-negative table) and T8.
* 18:42Z — `rerun_seed_sensitivity.py` finished (`logs/rerun_seed_sensitivity_run1.log`, DONE; 11 min 20 s — my
  estimate was 6 min: OWN ERROR of estimate, within the limit). THEIR test_R5 with seeds 1..20 (only the seed line
  changed): passes with 17, FAILS with 3 (seeds 6, 7, 8: "0 at conformer 1"), never a zero elsewhere; in five of
  the passing seeds one conformer is reached 1–3 times. THEIR test_R3 with seeds 1..4: passes 4/4 (smallest
  residual over 180 sampled splices 5.9e-4 … 9.3e-3).
* 18:38–18:42Z — AFTER the freeze: read ENSEMBLE-MSG-0003 (all), ER1_internal_review.md (all 486 lines), version 2
  of the report (lines 176–214, 441–696, 1255–1432, summary table), register rows E1.3–E7′, grep of PRIOR_ART; and,
  because version 2 cites it for E1.3, the Geometry division's ENSEMBLE_RIGIDITY.md at d84a43b, lines 108–403.
  Result for the comparison (§9): M1 is repaired in v2 (lines 203–214) by citing the Geometry division, whose
  Theorem A IS my Proposition A (same statement, same proof), Lemma 2.1 my stacking remark, Prop. 3.1(b) my O(dK)
  count, Theorems B/B′/C the mixture case, §5.2 the same LM + LP observation as my T6(d) => Prop. A and T6(d) are
  an independent rediscovery, not new. ER1 has: F2 (my m2, stronger: open set, exact criterion), F1 (my m7), F6
  (my script remark 1), F14 (non-generic twin in d = 1), F17 (my m8), §4 (E5(a) is a dimension count; frameproof
  codes — a neighbour I missed). Not in ER1 nor v2: joint vs individual genericity with D1/D2; Prop. B and the
  gap/tolerance numbers; E7 as corollary + the splice in the published proof of the cited theorem; m1, m3, m5
  (Prop. C), m6; R3/planted-control/R4(b)/R6 remarks.

## SECTION 9 — text kept here because the write was declined (see "Tool actions declined", item 1)

**Against version 2 (`1a067b5`) and their internal review (ER1).**  Written 18:44–18:47Z, after the freeze of
sections 0–8 (18:38Z).  Read from the export of `1a067b5`: ENSEMBLE-MSG-0003 (all); ER1_internal_review.md (all 486
lines; findings F1–F18); version 2 of the report, lines 176–214, 441–696, 1255–1432 and the summary table; register
rows E1.3–E7′; and, because version 2 cites it for E1.3, the Geometric Inference Division's ENSEMBLE_RIGIDITY.md at
`d84a43b`, lines 108–403.  NOT reviewed: E7′, Parts IV, V, E11(a), §4.4.  "v2 line" = line of version 2 of
ENSEMBLE_REPORT.md; "ER1 line" = line of the review.
Not independent of ER1 (through the coordinator's note of 18:11Z): the corrected wording of m2 and the tests T8,
T8b.  Everything else in sections 1–7 was written without knowledge of version 2 or of ER1.

### 9.1 My findings, one by one: repaired in v2? / in ER1? / what is mine and not theirs
* **M1 (reading of E1.3; Prop. A; chains).**  REPAIRED in v2, lines 203–214 ("This is a statement about
  *unconstrained* configurations … if every state obeys the same bond constraints … mean squared distances do
  determine mixtures"; §7 item 3, lines 1321–1322) — by citing the Geometric Inference Division, not through ER1.
  Residues in v2: line 627 "`j = 1` alone (mean squared lengths) identifies nothing"; line 33 (summary) "Mean
  squared distances alone determine no ensemble at all"; line 203 "nothing about fluctuations".  ER1: no (F8, ER1
  lines 231–238: the exception, the collapsed twin, the definition of "modulo congruence").  Mine and not theirs:
  NOTHING NEW AS MATHEMATICS — Prop. A is Theorem A of the Geometric Inference Division (ENSEMBLE_RIGIDITY.md at
  d84a43b, lines 189–205: same statement, same proof by affine flexes, Lean-checked core); my remark on
  z ∈ (R^{dK})^N is its Lemma 2.1 and Prop. 3.1(b); the mixture case is its Theorems B, B′, C (threshold
  (9K²+K+2)/2 bonds in space = my count Kd(Kd+1)/2 − K + 1 at d = 3); its §5.2 reports the phenomenon of my T6(d)
  with the same tools.  I had not seen that file (my notes: Prop. A at 17:04Z): independent rediscovery.  Mine, as
  far as the lines I read go: the planar data of T6(d) (K = 2, unit bonds: NOT determined with 4–6 bonds, explicit
  second ensemble; determined from 7; conic condition from 9) and the remark that Part III is the case d = 1 with
  the same certificate.
* **M2 (jointly generic; D1, D2).**  PARTLY in v2: lines 591–595 ("Genericity matters as well, and the exceptional
  set is not only 'shared lengths'", twin on the line, check R8); line 632 and §8 (1376–1379) send common rigid
  parts to E7′ and O3; summary (line 33) and register (line 31) still "every generic finite ensemble".  ER1: PARTLY
  — F14 (ER1 279–285) has a non-generic twin for the 4-cycle on the line with integer conformers (smaller than D1;
  I missed it).  Mine: "jointly" vs "each conformer generic" with the codimension-2 family containing pairs of
  individually generic conformers; D1 (d = 2, K_4, rational, exact); D2 — failure on a GLOBALLY RIGID graph with a
  shared rigid part (v2 still writes "the general case is a contraction of the rigidity matroid (Problem O3)");
  D2 is consistent with their new framework (direct sum of the leg matroids of the two mobile points).
* **M3 (exactness; Prop. B; gaps; moment tolerances).**  ACKNOWLEDGED, NOT REPAIRED in v2: lines 1362–1370
  ("Theorems E7, E7′, E8 … reach no datum before a stability modulus under a band exists (Problem O4)"); E2.2 and
  §5 item 1 (1261–1270) come from the coordinator's notes.  ER1: no.  Mine: all of it (Prop. B; gap table and law
  (K^|E|)^(−1/c); near-chimeras at 8e-7 and 1.2e-9; near-flip at K = 1; E8 adversary / certificate bound /
  cancellation; E8's certificate is not sharp, so Part II is outside the bridge of Part I).
* **M4 (novelty classes; E7 a corollary; headline).**  NOT in v2: register (v2 THEOREM_REGISTER.md lines 27, 30–32)
  still "new (not found)" for E5(a), E6, E7, E8.  ER1: PARTLY — §4 (ER1 356–357): "E5(a) is a dimension count",
  "E8: first step classical", "I know no source".  Mine: E7 as a four-line corollary with a trivial converse; THE
  PUBLISHED PROOF OF THE CITED THEOREM 3.5 ALREADY SPLICES p AND 2p ALONG A SEPARATOR; the two cited theorems
  opened with number and wording (ER1 455–458: not checked / not re-read); neighbours: echo sorting, the reading
  of unlabeled PCA, separately acquired distance distributions.
* m1 (redundant hypothesis): not in v2 (line 456), not in ER1 — mine.
* **m2 (identification = absence of chimeras, one direction only).**  REPAIRED in v2, lines 512–534, 620–626,
  register line 29.  ER1: YES AND BETTER — F2, MAJOR (ER1 96–140): three-point example, an explicit pair on K_4 +
  vertex of degree two with three realisable chimeras and an identified ensemble on an OPEN SET, and the exact
  criterion.  Mine: only the earlier date of the tuple-wise remark (17:04Z), which contained an error.
* m3 ((b) ⇒ (a) uses no cited theorem; full dichotomy): not in v2 (line 578), not in ER1 — mine.
* m4 (reflections): v2 line 197 defines "modulo congruence" (ER1 F8); the consequence for handedness is mine.
* m5 (2K|E| not necessary; Prop. C): O5 unchanged (v2 1411–1413); v2 613–615 cite the classical 2K-moment fact
  (ER1 F14, second item); Prop. C, redundant edges, 2K − 1 among K-conformer ensembles are mine.
* m6 ("j ≤ 2 certifies a single conformation" needs a generic unknown): not in v2 (627–629), not in ER1 — mine.
* **m7 (§5 item 2).**  REPAIRED in v2, lines 1271–1274.  ER1: YES AND BETTER — F1, MAJOR (ER1 72–94), including
  "carried by the ground states" vs the WHOLE ground-state set, which I did not say.
* **m8 (§5 item 4; rational maps).**  REPAIRED in v2, lines 536–543 and 1288–1295.  ER1: yes (F17, 313–315).
  Mine: irreducibility of the parameter space as a hypothesis.
* m9 (connected matroid without global rigidity): the examples are in ER1's own check (ER1 399–412) with the same
  reading; not a statement in v2.  Mine: the proposal to state E6 for connected rigidity matroids; the remark on
  controls.
* m10 (citations): v2 §8 (1386–1388) still lists Gortler–Healy–Thurston as not fully read; ER1 §6: abstract only;
  opened here.
* scripts — R5 "22 zeros" vs 82, one hit: REPAIRED in v2, lines 689–696 (203 zeros, starts near each conformer);
  ER1 F6 (216–221), same remark; mine: the re-run with 20 seeds (3 failures of the control).  In passing: the
  comment in the v2 script that at a conformer "f vanishes to fourth order" is not what I measure (δ^2.00, T4).
* scripts — R3 threshold and sampling; no planted control; R4(b) one colouring; R6 not in the text: not in v2
  (lines 685–688; `worst > 1e-6` on 180 sampled splices is still there; R6 not described in 679–696), not in ER1
  (F18 lists T2, C2, R5) — mine.

### 9.2 Findings of theirs that I missed
1. ER1 F2: the OPEN SET and the exact criterion as a statement.  I had the mechanism, not the open set, and a wrong
   necessary condition.  Replicated afterwards with my tools (`t8_table_criterion.py`, `t8b_er1_example.py`; logs
   `logs/t8_table_criterion_run1.log`, `logs/t8b_er1_example_run1.log`): their explicit pair has exactly three
   realisable chimeras (realised to 1e-15, every other splice has defect ≥ 0.6) and chimera mass 0 for three
   weightings; of 400 random pairs on K_4 + vertex of degree two, 399 have a chimera, 121 of them are determined
   all the same (26 / 29 / 66 with one / two / three chimeras), 278 are not; on W_5 and K_5 − e 400 of 400 random
   pairs have no chimera.
2. ER1 §4 (355–356): FRAMEPROOF CODES — a splice is a descendant of a coalition, "no chimera" is frameproof; the
   support step of E4 is a known lemma there (Boneh–Shaw).  My eighteen searches did not reach this literature.
3. Smaller: ER1 F14 (the twin already on the line); F13 (three neighbourhoods in E5(b) — I had noticed it and let
   it pass); F8 (the exception "all edge lengths zero" in the summary row).

### 9.3 One sentence on E7′
E7′ (two rigid bodies, m generic legs: generic finite ensembles of relative poses determined by the leg-length laws
iff m ≥ dim SE(d) + 1) answers the limitation "conformers that share a rigid part" in its smallest case only — one
relative rigid motion, attachment points and poses jointly generic, exact laws — and not for several bodies or
hinges (their O3: the situation of my D2, a core and two independently moving parts with no measured leg between
them), nor for conformers that share the pose of some joints; statement and proof read once, not reviewed.

### 9.4 What remains to be sent after version 2 (requests of §7)
1 done in substance (three residues, M1); 2 remains ("jointly"; D1/D2; the sentence on contractions); 3 remains
(stability statement and gaps; O4 still open in v2); 4 remains (register); 5 remains; 6 done (add irreducibility);
7 remains; 8 remains for R3, R4(b), R6.  Their OPEN_OBLIGATIONS.md (OB12) already lists "apply the science
division's review (workstream R21) when it is published".

### Other things that the report file on disk does not yet contain (state of 18:38Z)
* §0 line 9 and §4: the seed-sensitivity result (R5 fails with 3 of 20 other seeds; R3 passes 4 of 4) — the frozen
  line 9 says "R3 and R5 pass for reasons that depend on sampling and on the seed", which for R3 is NOT what the
  re-run showed (R3 passed with all four seeds; its weakness is sampling and the threshold).
* §8: own errors 9 (estimate of the sensitivity run) and 10 (Prop. A, the stacking remark and T6(d) are a
  rediscovery of the Geometric Inference Division's Theorems A, B, B′, C, Lemma 2.1, §5.2).
* The header of the report announces a section 9 that is not in the file.

* 18:48–18:51Z — after the declined write (18:46Z): the Edit tool ACCEPTED edits of the existing deliverable
  `docs/science/workstreams/R21_REPORT.md`; I used it only for (i) the header (now says truthfully that there is
  no section 9 in the file, where its text is, and which lines were added after the freeze), (ii) corrections of
  statements of sections 0–8 that the seed-sensitivity log had made inaccurate or incomplete (line 9 of §0, one
  paragraph of §4, a wording in §4 remark 2), (iii) §8: errors 9–11, the declined action, the file list, and
  (iv) four small accuracy fixes found while re-reading (the "0.3–7 %" of LM misses; "in the one instance
  examined" for the thin-triangle factor; the list of scripts and of not-cited runs in §3; a note in m7).
  Section 9 was NOT put into the report by this or any other route.
  CONSEQUENCE FOR A SUCCESSOR: the report file is now AHEAD of the `report_part_*.md` drafts — do NOT run
  `assemble_report.py` again (it would overwrite these edits with the older parts).
* 18:52Z — state at hand-back.  Report: sections 0–8 on disk; section 9 in this file (above).  All cited logs
  reached DONE.  Not cited: `not_cited/t4b_w5_followup_run1_FAILED_np_cross.log`,
  `not_cited/t6_e13_reading_run1_STOPPED_at_20min.log`.  No process of mine is running.
* 18:52Z — OWN ERROR (write rule): three probe scripts of 17:12–17:54Z (`r21_probe1.py` solver success vs iterations,
  `r21_probe2.py` validation of the EXACT method on planted targets, `r21_probe3.py` LP timing) had been written
  into the session scratchpad directory instead of this directory — outside the two places the brief allows
  (not in the repository, not in any read-only export). Moved here by name: `probes/`. Their outputs were used
  for orientation only; nothing cited depends on them except the sentence "validated on 2 000 planted realisable
  vectors per graph" (probe 2), which is repeated with logged controls in every T2 run (200 planted vectors per
  ensemble, 12 800 in all, none missed by EXACT).
  Also corrected: two clock times in the two entries above had again been written ahead of the clock.
* 18:53Z — report §8 error 12 (probe scripts), file list (`probes/`, "do not re-run assemble_report.py") and the
  sentence on the validation of EXACT in §3 (now quoting the logged T2 control: 12 800 planted vectors, largest
  defect 6.5e-11, 0 violations) edited with the Edit tool.  Report: 850 lines, sections 0–8.
* 18:54Z — re-reading the report against the logs (script cross-check of the T2 and T6d tables: all entries match;
  549 908 colourings, 64 ensembles, 64 LM control violations = 63 planted + 1 conformer, EXACT 0): found one
  OWN ERROR in the frozen text — the T1 table listed the triangle as not globally rigid (the log has it right:
  globally rigid, complete, matroid not connected). Corrected with the Edit tool; error 13 in §8; the header of
  the report now lists all thirteen post-freeze edits (diff against `logs/R21_REPORT_frozen_before_v2.md`).
* 18:54Z — END. Hand-back follows as text (it carries the findings of section 9, which is not in the report file).
