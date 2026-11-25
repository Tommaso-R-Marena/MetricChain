# Workstream K — running notes (certified kinetics: barriers, rates, third semiring)

Started 2026-11-25 17:41 UTC.  Rule: update after every step.

## Step 0 (17:41) — setup
* Read COMMON.md and K_brief.md in full.
* Created `experiments/science/ws_K/`.  Report target: `docs/science/workstreams/SK_REPORT.md`.
* Next: read THEORY_REPORT §1, §2.3, §3.1, §3.4, §6.1, §11.2, §11.6 and `proofs/CertificateAlgebra.lean`
  top-level soundness statements.

## Step 1 (17:50) — reading done; first-pass analysis (paper, before numerics)
Read: THEORY_REPORT §1, §2.3, §3.1, §3.4, §6.1, §11.1–11.3, §11.6, §11.8; CertificateAlgebra.lean
(Cert/verify/verify_sound, RProblem/verifyR/verifyR_sound, IProblem/verifyITop_sound);
PartitionCertificate.lean (WInstance, ZCert, zverify; zverify2 has cut/elim rules).
`grep` over docs: nobody in the programme has touched barriers/kinetics (only incidental words).

First-pass observations (ALL UNVERIFIED until the numerics below):
* Sketch 1 (cut certificates): soundness direction fine for outer boundary.  The "iff" as stated in the
  brief FAILS in corner cases: path graph a–b, E(a)=5,E(b)=0,t=5: B=5 but S={a} has outer boundary {b}
  with E=0.  Correct form: B(a,b) = max(E(a), max_{S∋a,S∌b} min_{∂⁺S} E)  (vertex-separator form).
  This is Edmonds–Fulkerson bottleneck duality (paths vs separators = blocking pair) — to check in prior art.
* Coordinate cuts under UNRESTRICTED single-site moves are useless: ∂⁺{x_i∈T} = whole complement, so the
  bound is ≤ E(b).  Useful cuts: boxes (outer boundary = union of n boxes), level sets of a
  site-additive statistic (wall = slab), coordinate cuts only if the site's own move graph is restricted
  (torsion voxels with nearest-neighbour moves -> "certified relaxed scan").
* Sketch 2 (robust barrier height interval): looks TRUE, 5-line proof: pinned residual g−g(a) lies
  pointwise in [−d(a,·), d(·,a)], both ends admissible, B monotone, IVT.  With anchors: replace d by the
  conditional envelope D_A (Thm 11.1) — extremal g: min(U, L(a)+d(·,a)) and max(L, U(a)−d(a,·)).
  Generalisation ("pinned monotone lemma") would contain Thm 2.3, 2.4, 11.12 as special cases.
* Query complexity: conjecture "barrier certificates = coverings of a separator (lower) and of a path
  (upper)" with radii = energy excess/deficit relative to the saddle + ε.
* Sketch 3: (i),(ii) standard Rayleigh-quotient facts; extension: survival from restricted equilibrium
  P_{π_A}(τ>t) ≥ exp(−t Q(A,A^c)/π(A)) by Jensen on the spectral measure (to test).
  (iii) Dirichlet = shorting/lumping (Nash-Williams series law with several cuts); Thomson with path
  mixtures = parallel law; tropical limit of Dirichlet/Thomson = cut/path duality.
* Complexity: barrier decision should be PSPACE-hard already for pairwise 4-state models (k-colouring
  reconfiguration, Bonsma–Cereceda) and maybe at bounded bandwidth (Wrochna) — to verify in prior art.
Plan of scripts: kcore.py (library), t1_cut_duality.py, t2_robust_barrier.py, t3_cover.py,
t4_cut_families.py, t5_rates.py, t6_robust_rates.py, t7_lattice_chain.py.

## Step 2 (~17:54, machine clock) — T1, T2 run (numerics before proofs)
* `kcore.py` written (product spaces, minimax barriers by (min,max)-Dijkstra, McShane envelopes,
  conditional envelope, random admissible residuals, reversible generators, exact spectral quantities).
* **T1 (`t1_cut_duality.py`, out_t1.txt)**: exhaustive over all S∋a, S∌b on 126 random integer-energy
  instances (N=8,9,12,16): B(a,b) = max(E(a), max_S min_{∂⁺S}E) holds 126/126; inner-boundary twin with
  E(b) holds 126/126; the brief's unrepaired iff fails in 43 (outer) / 54 (inner) of the 126 (exactly the
  corner cases E(a)=B or E(b)=B).  Canonical cut (component of a in {E<B}) works whenever B>E(a) (61/61).
  Coordinate cuts with complete site graph: boundary = complement (800/800), value ≤ E(b) (800/800) => useless.
  Box cuts: outer boundary = union of n one-defect boxes (186/186).
* **T2 (`t2_robust_barrier.py`, out_t2.txt)**: robust height interval [B_{f−d(a,·)}−f(a), B_{f+d(·,a)}−f(a)]:
  agrees with an INDEPENDENT exact optimisation over the polytrope (LP per separator / per simple path)
  to 2e-16 on 16 tiny instances (sym. and asym. site-additive envelopes); 0 violations in 2880 samples;
  with anchors (conditional envelope D_A; extremal g± as predicted) 0 violations in 1920; saddle energy in
  [B_{f+L},B_{f+U}] 0 violations in 1920; depth (persistence) of a: 0 violations in 2880.
  Exact interval width / sup-norm stability width: median 0.24 (min 0, max 0.85).
  Upper excursion ≤ envelope radius of the f-optimal path: always.
  => Sketch 2 TRUE (and extends to anchors and to depth).  Now write proofs; next T3 (coverings).

## Step 3 (~17:57, machine clock) — T3, T4 run
* **T3 (`t3_cover.py`, out_t3.txt)**: with slack s, W_ε(A)={y: s(A,y) ≤ E(y)−B_E+ε}, V_ε(A)={y: s(y,A) ≤ B_E+ε−E(y)}:
  "LB(A) ≥ B_E−ε ⇔ W_ε(A) separates p,q" 0 mismatches in 1280 tests (600 true);
  "UB(A) ≤ B_E+ε ⇔ V_ε(A) connects p,q" 0 mismatches in 1280 tests (537 true).
  Mean-field barrier f=φ(|x|), g=0, c=1, ε=0.5: the transition layer is a lower certificate and NO smaller
  anchor set is (n=4: exhaustive, C(4,2)=6; n=5: all layer-minus-one sets and 3000 random sets of size 9 fail).
  One monotone path (n+1 evaluations) is an exact upper certificate.  => lower bounds cost a covering of a
  separator (can be exponential), upper bounds a covering of a path.
* **T4 (`t4_cut_families.py`, out_t4.txt)**: fraction of the true height of each non-global local minimum
  (exit target = lower state with least barrier) certified by tractable cut families:
    binary n=10 chain+ (28 minima): box 0.99 (exact 93%), sphere 0.69 (50%), count 1.00 (96%)
    binary n=10 complete (36):       box 0.96 (89%), sphere 0.86 (72%), count 0.96 (92%)
    3-state n=6 chain+ (37):         box 0.90 (76%), sphere 0.82 (59%), count 0.91 (81%)
    3-state n=6 complete (50):       box 0.89 (76%), sphere 0.84 (60%), count 0.91 (78%)
  Curie–Weiss n=10: box only 1.7 of 4.5 (collective barrier), count/sphere exact.
  CAVEAT: small systems, shallow minima whose exits are 1–2 flips; no claim for long chains.
* **NEGATIVE (new to me, simple proof)**: Lagrangian relaxation of the counting constraint
  (hand E+λq to the pairwise kernel) returns the lower convex envelope of the profile m_j=min_{q=j}E at j=r,
  which is ≤ max(E(a),E(b)) — it NEVER beats the trivial bound (0% of 151 minima; mean fraction 0.00).
  A barrier top is exactly where the profile is non-convex.  Same for Chernoff tilting at finite T.
  => counting constraints must be enforced exactly (counter DP / polynomial weights / branching).

## Step 4 (18:10) — T5 running (machine load avg ~20 on 4 cores: other workstreams); prior art meanwhile
* T5 (`t5_rates.py`) partial output so far (Curie–Weiss n=10, Ising chain n=10): all inequalities hold;
  see out_t5.txt when finished.  Machine heavily loaded -> later scripts must use N ≤ ~500 states.
* Prior art read so far (reading level in brackets):
  - Edmonds & Fulkerson, "Bottleneck extrema", JCT 8 (1970) 299–306 [full text pp. 299–301, read as page
    images]: for any clutter R on a finite set, with blocker S=b(R): min_{R} max_{x∈R} f = max_{S} min_{x∈S} f.
    Intro cites the bottleneck path/cut duality of Fulkerson (arcs).  => sketch 1 (repaired) is this theorem
    for the clutter of vertex sets of a–b paths (blocker = minimal vertex separators, {a},{b} included).
  - Bonsma & Cereceda, TCS 410 (2009) 5215–5226 [search snippet of abstract]: k-colouring reachability under
    single-vertex recolouring is PSPACE-complete for k ≥ 4 (even bipartite), in P for k=3; shortest
    recolouring sequences can be exponential for k ≥ 4.
  - Wrochna, arXiv:1405.0847 (JCSS 2018) [abstract via fetch; search summary for the constants]: several
    reconfiguration problems (k-Coloring for some constant k, Independent Set, Shortest Path) remain
    PSPACE-complete on graphs of bounded bandwidth; tractable for bounded tree-depth.
  - Aldous & Fill, "Reversible Markov chains and random walks on graphs", Ch. 3 §3.5 [HTML page fetched;
    statements extracted by the fetch tool, not read raw]: Lemma 3.16 (CM f: exp(f'(0)t/f(0)) ≤ f(t)/f(0) ≤ … ≤ e^{−λt});
    Prop 3.21(iii): π(A^c)/Q(A,A^c) = E_{ρ_A}T_A ≤ E_{π_{A^c}}T_A = E_πT_A/π(A^c) ≤ 1/λ_A, ρ_A the ergodic
    exit distribution.  => my "Jensen survival bound" and (i) are KNOWN; the cut value is exactly the
    Kac mean sojourn time (TST rate with recrossings).
  - Maňuch, Thachuk, Stacho, Condon, Natural Computing 10 (2011) 391–405 [search snippet]: RNA energy
    barrier problem NP-complete in a simple energy model.

## Step 5 (18:20) — T5 finished (single-threaded BLAS: 44 s), T6 run
* **T5 (`t5_rates.py`, out_t5.txt; first partial run kept as out_t5_partial_first_run.txt)**: 43 (system, β)
  cases (Curie–Weiss n=10, Ising chain n=10, 9 random pairwise instances; N up to 1024; Metropolis).
  - λ_A ≤ k_cut=Q(A,A^c)/π(A): holds 43/43, ratio λ_A/k_cut ∈ [0.24, 1.00].
  - identity k_cut = Σ_j w_j λ_j, E_{π_A}τ ≥ 1/k_cut (ratio 1.00–3.86), survival P_{π_A}(τ>t) ≥ e^{−k_cut t}
    on 61 times: 43/43.
  - for A = sublevel component, k_cut = Σ_{y∈∂⁺A} deg_A(y)e^{−βE(y)}/Z(A) EXACTLY (kcert/kcut = 1.00 always).
  - gap ≤ Q/(π(A)π(A^c)): 43/43, ratio 0.14–0.66.
  - capacities a↔b: Dirichlet single cut: cap/cut ∈ [0.014, 0.67] (0.28–0.67 at β=8);
    Nash-Williams over levels of q = Hamming distance from a on the differing sites: exact for CW (lumpable),
    0.965–0.999 Ising chain, but as bad as 0.001 on a 3-state random instance (q is a poor coordinate there:
    C_m is dominated by low-energy regions unrelated to the transition) — levels are only as good as the
    coordinate; level-partition-function form (NWc) loses a further factor ≤ ~2–10.
    Thomson: one minimax path 0.001–0.98 of cap; ≤8 edge-disjoint paths 0.008–0.99 (0.81–0.99 at β=8).
  - 3 "violations" flagged, all in the float64 check of the hitting-time identity when π(A) ≤ 3e-14
    (h ~ 1e-20 unresolvable in double precision).  TO DO: redo that identity in high precision (t5b).
* **T6 (`t6_robust_rates.py`, out_t6.txt)**: robust TST bound sup_g k_TST(f+g;A) under weighted Hamming
  envelopes, exact by LP in w=e^{−βg} (N=256, 243): 33 cases, 0 violations of
  sampled k(g) ≤ K_exact ≤ min(K_gate, K_a); LP optimiser admissible and attains K_exact; λ_A(g) ≤ k(g).
  Inflation (1/β)ln(K_exact/k_nom) ∈ [0.10, 0.77] energy units for Σc ∈ [0.5, 3.6]; always ≤ d(a,y*).
  K_gate overshoots K_exact by 0.02–0.5, K_a by 0–1.0 energy units (K_a exact when |A|=1).
  Structure of the optimiser: in the instance inspected (|A|=8) g_opt = −d(a,·) EXACTLY at β=1,2 and within
  1.5% at β=4: the cone residual at the basin minimum (same extremal as for the barrier lower bound).
  New idea: K_gate is a dual-feasible "transport plan from wall to basin"; general dual certificates
  θ_y(x) give sup_g ≤ max_x Σ_y θ_y(x) n_y e^{−β(f(y)−f(x)−d(x,y))}.

## Step 6 (18:36) — T5 rerun clean, T5b, T7
* T5 patched: hitting-time identity counted only where π(a)/π_max ≥ 1e-9.  Final: 43 cases, 0 violations;
  identity defect ≤ 2.3e-9 in 38 well-conditioned cases; 5 ill-conditioned (float64 defects up to 6.5).
* **T5b (`t5b_scaling_highprec.py`, out_t5b.txt)**: (A) same identity at 60 digits (mpmath) on an n=6
  instance with π(a)=2.4e-17: defect 4.7e-61 (float64: 2.9e-8) => the T5 flags were round-off.
  (B) Curie–Weiss, exact lumped chain, A={m<m*}: single cut (TST) λ_A/k_1cut = 0.283, 0.173, 0.109, 0.076,
  0.058, 0.044 for n=10..320 at β=1.3 (≈ n^{-1/2}: recrossing); multi-cut (series/test function of q)
  λ_A/k_mcut = 0.73 → 0.9998.  Rows with λ_A<1e-10 not reported (float64 resolution).
* **T7 (`t7_chain.py`, out_t7.txt)**: RIS chain on the diamond lattice (3 torsion states, hard overlaps,
  E = 0.5·#gauche − #contacts, S_c=8), n=6,7,8 torsions (683/2005/5849 feasible states).
  Fraction of trap depth certified: box/count 1.00 (n=6, all depths 0.5), 0.55 (n=7, exact 37%),
  0.77 (n=8, exact 62%); sphere 0.48/0.63; GLOBAL contact-number level cut: 0.00 always (trap and
  target have the same/more contacts — q does not separate them); connected piece of the contact
  superlevel set: 0.24/0.89/0.49.  Rates (n=7 deepest trap, depth 3.0): λ_A/k_cut 0.75–0.87,
  cap/cut 0.22–0.30, gap/gap_cut 0.04–0.09 (that cut is not the slowest mode), 1-path Thomson 0.03–0.05.
  Robust height, c_i=0.3, n=8: exact [1.70,4.40] vs sup-norm stability [1.10,5.90].
  CAVEAT: tiny chains; non-monotone in n; no extrapolation.
