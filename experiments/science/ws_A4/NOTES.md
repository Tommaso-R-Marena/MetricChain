# Workstream A4 — notes (prior-art search for a global n^2 stability bound for chains from sequence-local distances)

Internal review by an AI agent (not external peer review).  Notes are kept from the first minute and
updated after every step.  Every time below is read from the clock (`date -u`) when the line was written.

## 0. Start

* 2026-11-26 20:31 UTC — read COMMON.md, A4_brief.md, and the three read-only copies
  (LOCAL_DATA_STABILITY.md in full, GEOMETRY-MSG-0007.md in full, PRIOR_ART.md in full).
* Directory `experiments/science/ws_A4/` created 20:31 UTC.  Files: `NOTES.md` (this), `search_log.md`
  (every query and every address opened), later `docs/science/workstreams/A4_REPORT.md`.
* Rules I work under (binding): generic queries/addresses only; no fabricated citation / number / quotation;
  a reading level for every source; write only here and in the report file; no state-changing git; no subagents;
  if a tool declines an action I do not work around it.

## 1. The statement, as I understand it (my own words; nothing of this goes into a query)

Points x_1..x_n in R^3; data = squared distances between points whose index difference is <= 4
(the 4th power of a path graph; a 4-lateration ("trilateration" in 3D) ordering in which every point is
attached to its 4 immediate predecessors).  Hypothesis on X: every window of 4 consecutive points is a
uniformly non-degenerate simplex (smallest singular value of the edge matrix >= tau, largest <= D).
Conclusion: every Y whose local squared distances are pointwise within tau^4/(73 D^2) of those of X is,
after an isometry, within C (b/tau^2) n^2 ||eta||_2 of X in Frobenius norm (eta = squared-distance errors of
separation <= 3).  Global (no closeness of Y to X assumed), threshold independent of n.
Mechanism: per-window polar decomposition -> window rotation R_i; consecutive windows share 3 points ->
R_{i+1} ~ R_i up to a reflection, excluded by the separation-4 distance; rotation errors telescope additively;
bond vectors summed (lever arm).  Scaling: frame error over i windows <= sqrt(i) * l2 norm; lever arm factor i;
l2 over points -> n^2.
Lower bound (their Theorem K(c)): for points in a thin tube (helix), the 7th singular value of the rigidity
matrix is <= C/n^2 (test field = bent rod), so the infinitesimal constant is >= c n^2.

Scaling dictionary to continuum elasticity (my own check, by hand): strain ~ eta/b^2; with tau ~ b ~ h,
bound = h n^2 ||strain||_2 = (L^2/h) ||strain||_2 for the displacement, i.e. (L/h) for the gradient:
the rod scaling of the geometric rigidity constant.

## 2. Keywords under which it would be found (candidate list, to be extended)

lateration / trilateration graph, sequential localisation, error propagation / accumulation, noisy distances,
stability of stress minimisation / MDS, band graph, power of a path, k-tree, chordal EDM completion,
discretizable (molecular) distance geometry, geometric build-up, branch-and-prune, patch registration,
synchronisation over O(d)/SE(d) on a path, connection Laplacian Cheeger inequality, quantitative rigidity,
rigidity eigenvalue / stiffness matrix eigenvalue, d-dimensional algebraic connectivity, geometric rigidity
estimate (Friesecke-James-Mueller), thin rods, Korn inequality in thin domains, discrete/atomistic rods,
Cramer-Rao bound for relative localisation, dead-reckoning / odometry error growth.

## 3. Log of steps

### 3.1 Arias-Castro & Vishwanath, arXiv 2310.10900v3 (8 Dec 2024) — READ IN FULL (PDF text, all 6 sections + references) [20:36 UTC]

Reading level: **opened in full** (direct download of the arXiv PDF v3, text extraction read line by line; the HTML
rendering v3 opened only to compare equation numbers).  A SIAM journal record exists (DOI 10.1137/24M1661790) — not
yet opened; everything below is the arXiv v3 text.

What it proves (their notation: p = dimension, n points, graph (V,E), noise model d_ij^2 = |x_i-x_j|^2 + eps_ij (1.2)):
* **Theorem 2.1** (p. 4): lateration graph + latent configuration in general position => "there are sigma > 0 and
  A > 0, continuous in (|x_i - x_j| : (i,j) in E), such that, if sum eps_ij^2 <= sigma^2, sequential lateration
  outputs an embedding y_1..y_n satisfying  min_g sum_i |y_i - g(x_i)|^2 <= A sum_{(i,j) in E} eps_ij^2  (2.1)".
* The explicit constant, end of the proof (PDF numbering **(2.6)**; the arXiv HTML rendering numbers the same
  display **(2.30)**):  A_n <= (1 + C_2 alpha)^{n-p-1} / ((p+1) omega^2) * max{ C_1 alpha, C_2/(1 + C_2 alpha) },
  with alpha := max_k (rho_k/omega_k)^2, omega := min_k omega_k, rho_k / omega_k the diameter / width of the landmark
  set {x_i : i in I_k} of step k; C_1, C_2 >= 1 the absolute constants of two lemmas quoted from
  Arias-Castro–Javanmard–Pelletier 2020 (their [6], "Corollary 2" and "Corollary 3").
* The admissible noise level, PDF **(2.7)** = HTML **(2.33)**:
  eta^4 <= min{ (p+1)^2/C_1^4 , (p+1) / ( C_2^2 (1 + C_2 alpha)^{n-p-2} max{C_1 alpha, C_2/(1+C_2 alpha)} ) } omega^4,
  eta^4 := sum eps_ij^2.  So the threshold shrinks like (1 + C_2 alpha)^{-(n-p-2)}.
* The sentence on the chain-like case (p. 8, right after the proof): "The bound in Theorem 2.1 takes into account the
  worst case scenario where, for every k > p+1, each node v_k is connected to precisely the preceding p + 1 nodes
  {v_{k-1}, ..., v_{k-p-1}}. [...] This is the most restrictive scenario, which necessitates performing n - p - 1
  rounds of classical lateration to embed all the nodes, and is reflected in the multiplicative growth in the
  constant A_n in (2.6)."
* **Theorem 3.1** (p. 10): same hypotheses => any minimiser of the s-stress (1.1) satisfies the same kind of bound;
  "(As it turns out, the proof below shows that we can use the same sigma and a small multiple of the constant A of
  Theorem 2.1.)" — the proof gives 6 A_0(x).  So the stress-minimiser bound inherits the exponential constant.
* The sentence on tightness (p. 11, after the proof of Thm 3.1): "While the constant was obtained in a worst-case
  scenario and is unlikely to be tight in more friendly (and less contrived) settings, it is natural to ask whether
  the perturbation bound in Theorem 3.1 has the right dependency in the errors eps_ij."  And in the Discussion (p. 16):
  "our analysis can only be accurate, if at all, in the very worst case, and is not representative of situations
  such as that of a random geometric graph".
  => NUANCE the Geometry division's wording misses: the authors say the constant is unlikely to be tight in
  *friendlier* settings; about the worst (chain-like) case they say only "accurate, if at all" — they do not claim
  the exponential is an artefact there, and they do not claim it is real.
* **Proposition 3.2** (p. 11): a lower bound min_g sum |y*_i - g(x_i)|^2 >= a sum eps^2 for suitable data, "a > 0 is a
  constant depending only on the graph (V,E)"; the proof takes a dilation and gets a = 1/(8 delta), delta the maximum
  degree.  (For a band graph delta is bounded, so a does not depend on n.)
* **Theorem 4.1**: random geometric graphs are lateration graphs w.h.p. (irrelevant here).
* NO polynomial constant is stated for any special case; no remark on chains beyond the "worst case" sentence; no
  notion of depth of the lateration order (only: "The accumulation of error can be avoided in some situations by
  minimizing the number of rounds of classical lateration", best case = landmark MDS).
* Their own survey of prior art (p. 3): "Only a few perturbation bounds exists in the MDS literature. [...] Moore et
  al. [58] [...] carry out a very limited mathematical analysis, restricting themselves to analyzing the probability
  of a gross error or 'flip' in one trilateration step. We are not aware of any other results."  And they recover
  "a result of Anderson et al. [3] in the special case of a lateration graph" (Anderson–Shames–Mao–Fidan 2010:
  dimension 2, with anchors, generically globally rigid: error of the constrained stress minimiser bounded by a
  constant multiple of the noise amplitude — constant not explicit, per A-C&V's description).
* The single-window dependence: their Lemma 2.2 ("Corollary 2 in [6]"): classical scaling on m points of diameter rho
  and width omega: min_g sum |y_i - g(x_i)|^2 <= C_1 rho^2/(m omega^4) * eta^4 — i.e. error <= sqrt(C_1/m) (rho/omega^2)
  * ||eps||_2: the same rho/omega^2 as the b/tau^2 of the statement under review (one window).  To be read at the
  source (JMLR 2020).

Verdict on the Geometry division's reading of this paper: CONFIRMED in substance (exponential constant
(1 + C_2 alpha)^{n-p-1}, exponentially shrinking threshold, chain-like case called "the worst case scenario",
no polynomial bound), with three corrections: (i) equation numbers (2.30),(2.33) are those of the arXiv HTML
rendering; in the PDF — and in the paper's own cross-references — they are (2.6),(2.7); (ii) "they state that the
bound is unlikely to be tight" should carry the authors' qualifier "in more friendly (and less contrived)
settings"; (iii) there is a published journal version (SIAM), to be identified.

### 3.2 Publication data and citing papers of Arias-Castro–Vishwanath [20:38 UTC]

* Journal version: SIAM Journal on Mathematics of Data Science 7(3), 1077-1097 (online 15 July 2025) — from the
  Crossref record [bibliographic record only]; the publisher's page returned HTTP 403: **journal version not read**.
  All statement numbers I quote are those of arXiv v3 (8 Dec 2024).
* arXiv 2207.07218 (Arias-Castro & Chau, tuning parameters for patch-stitching): abstract only; its theory "removed
  to a separate paper (arXiv:2310.10900)" per the revision comment.
* Citing papers found (Semantic Scholar API: 3; OpenAlex: 2; Crossref count: 1): Arias-Castro–Berenfeld–Kane
  (ordinal MDS theory, arXiv 2310.00211; SIAM 2025), Arias-Castro–Chau 2022, Damrich–Kobak (arXiv 2611.28985,
  21 Nov 2026).  From titles/abstracts none is about the size of the constant for chain-like lateration graphs.
  [abstract pages only for 2207.07218 and 2611.28985; title only for 2310.00211 so far]
  => As of today no citing paper found that improves the exponential constant.  Thin: citation indices lag.

### 3.3 Javanmard & Montanari, "Localization from incomplete noisy distance measurements", arXiv 1103.1417v4 (Found. Comput. Math. 13 (2013) per A-C&V's reference list) [20:38 UTC]

Reading level: **opened in full for the main text** (abstract, §§1-7 incl. 6.1, 6.1.1, 7, 7.1; appendices A-N not read).
* Setting: n points uniform in the cube [-0.5,0.5]^d, edges between points at distance <= r (random geometric graph),
  errors z_ij on *squared* distances, arbitrary with |z_ij| <= Delta; estimator = an SDP (trace minimisation), then
  rank-d truncation.  Error metric d(X,Xhat) = n^{-2} || L X X^T L - L Xhat Xhat^T L ||_1.
* Theorem 1.1: w.h.p. d(X,Xhat) <= C_1 (n r^d)^5 Delta / r^4 (3); "Conversely, w.h.p., there exist adversarial
  measurement errors such that d(X,Xhat) >= C_2 min{Delta/r^4, 1}" (4).  Constants depend only on d.
  -> polynomial in 1/r: a GLOBAL polynomial stability bound for an SDP estimator on *bulk* geometric graphs.
* §3: "it is immediate to see that under the worst case model for the measurement errors, no algorithm can perform
  better than C Delta/r^2" (dilation argument) — the same dilation as A-C&V Prop. 3.2.
* §7 (lower bound): "Consider the 'bending' map T : [-0.5,0.5]^d -> R^{d+1}, T(t_1..t_d) = (R sin(t_1/R), t_2, ..,
  t_d, R(1 - cos(t_1/R)))", R = max{1, r^2 Delta^{-1/2}}; the squared distances of edges change by at most
  r^4/(2R^2) <= Delta; "The crucial point is that the SDP in the first step of the algorithm is oblivious of
  dimension d".  So their Delta/r^4 = (strain Delta/r^2) x (domain size / r)^2 is a BENDING lower bound — the same
  mechanism as the rod lower bound under review, but for the SDP relaxation (bending into the extra dimension),
  not an estimator-independent bound in the true dimension.
* Lemma 6.2 (chains): "Let G_ij be the chain between nodes i and j as described above. There exists a constant
  C = C(d), such that |<x_i - x_j, y_i - y_j>| <= C r^{-1} sum_{(l,k) in E(G_ij)} |<x_l - x_k, y_l - y_k>|".
  A chain = sequence of subgraphs H_1..H_k, each isomorphic to the hypercube graph with diagonals of faces
  (M_d^{(2)}), consecutive ones sharing a facet, built along the straight segment from x_i to x_j.  Proof: a
  self-stress ("spring constants" lambda_lk, |lambda| <= C r^{-1}) transmitting a force along the chain
  ("force equilibrium", "torque equilibrium").  This is a quantitative *infinitesimal* rigidity estimate for a
  chain of overlapping cells — for ONE scalar (the first-order change of the end-to-end squared distance) on a
  *straight* chain, with a factor ~ (length / r) = number of cells; it does not see bending (transverse
  displacement is second order in the end-to-end distance).
* Distance from the statement under review: different graph family (bulk random geometric graph in a cube, not a
  band graph / thin chain); the estimator is an SDP, not "any configuration consistent with the data"; the chain
  lemma is first-order and scalar.  NOT a statement of which the chain bound is a corollary.  But: (i) polynomial
  global bounds for local-distance data exist in print since 2011-13 for bulk geometric graphs; (ii) the (L/r)^2
  bending law is printed there as a lower bound for the SDP.

### 3.4 Component-based localisation (arXiv 1807.00108) [20:41 UTC] — keyword scan only
"Robust Component-based Network Localization with Noisy Range Measurements" (corresponding author Yongcai Wang, per the
first page).  Engineering paper; speaks of "error accumulation in sequential localization" qualitatively and uses the
condition number of a linearised "ranging sensitivity matrix" (its Theorem 1 is a rank statement).  No bound as a
function of the number of nodes.  Reading level: keyword scan + the theorem statement.  Not relevant beyond vocabulary.

### 3.5 Shamsi–Taheri–Zhu–Ye, arXiv 1010.2262v4 [20:41 UTC] — abstract + keyword scan
"Conditions for Correct Sensor Network Localization Using SDP Relaxation".  Exact data only; the single sentence on
noise: "although our theoretical analyses are based on exact distance measurements, similar extensions of our model
(established in earlier SDP work) would be applicable to noisy distance data."  No stability bound.
(OWN ERROR, caught before use: from memory I expected a noisy-data error bound for trilateration graphs in this paper;
there is none.)

### 3.6 Chaudhury–Khoo–Singer, arXiv 1306.5226v5 (SIAM J. Optim. 25 (2015) per search summary) [20:41 UTC]
Reading level: opened; abstract, contribution list, §3 (rigidity conditions incl. "Theorem 7 ([68]). If Gamma is laterated
and the local coordinates are non-degenerate then the framework Theta is affinely rigid"), §5 statements of
Theorems 12-13 and Proposition 14, discussion item (3).  Proofs not read.
* Problem: N points, M patches (local coordinate systems); data = local coordinates of points in patches, each
  perturbed by at most eps (bounded noise (33)-(34)); estimate global coordinates.  NOT distance data.
* Theorem 13 (Stability of GRET-SDP): if rank(C_0) = (M-1)d,
  eta <= |E(Gamma)|^{1/2}/lambda_2(L) * [ 32 sqrt(2d(d+1)(2+N)|E(Gamma)|) mu_{d+1}(C_0)^{-1/2} R + sqrt(2+N+M) ] eps,
  eta = min_Theta ||Z* - Theta Z_0||_F, lambda_2(L) the second smallest eigenvalue of the Laplacian of the membership
  graph, mu_{d+1}(C_0) an eigenvalue of the clean patch-stress matrix, R the radius of the configuration.
  "The bounds are again quite loose. The main point here is that the reconstruction error for GRET-SDP is within a
  constant factor of the noise level."  Item (3) of §7: "the bounds in Theorem 13 are quite loose".
* Relevance: a *global* stability bound for stitching overlapping patches whose constant is a spectral expression
  (lambda_2 of the membership graph; a patch-stress eigenvalue).  For a chain of patches lambda_2 ~ M^{-2}, so the
  bound is polynomial in the number of patches PROVIDED mu_{d+1}(C_0) is bounded below polynomially — which the
  paper does not evaluate for any family (no chain / path example).  It concerns one algorithm's output and
  coordinate noise.  So: not the statement, not a corollary without a new spectral estimate; but it is a printed
  polynomial-type route (my estimate of the exponent it would give for a chain is far above 2 — not in the paper).

### 3.7 Moore–Leonard–Rus–Teller, SenSys 2004 (author copy) [20:41 UTC]
Reading level: opened; related work, Theorem 1 (worst-case probability of a flip in one robust quadrilateral), §4.4.
* "Error propagation during trilateration is derived in [13], but the potential for significant error due to flips
  is not considered."  [13] = Niculescu & Nath, "Error characteristics of ad hoc positioning systems"; [18] =
  Savvides, Garber, Adlakha, Moses, Srivastava (Cramér–Rao lower bound for network localisation).
* §4.4: "Cluster-based localization algorithms generally suffer from poor error propagation characteristics because
  they have no absolute reference points as constraints." — qualitative; simulation only.  No growth law in n.
  => confirms A-C&V's description ("a very limited mathematical analysis ... a gross error or 'flip' in one
  trilateration step") and the Geometry division's use of it.  Follow up: Niculescu–Nath 2004; Savvides et al. 2003.

### 3.8 The continuum analogue: geometric rigidity in thin domains and rods [20:49 UTC]

(a) **Friesecke–James–Müller, "A hierarchy of plate models ...", MPI MIS preprint 7/2005 (ARMA 180 (2006) 183-236 per
search summary).**  Reading level: opened (preprint PDF); read §3 a)-b), Theorem 9 + remarks, Theorem 10, Remark 11.
* Theorem 9 (the 2002 rigidity estimate, restated): for a bounded Lipschitz U in R^n there is C(U) with
  ||grad v - R||_{L2(U)} <= C(U) ||dist(grad v, SO(n))||_{L2(U)} for some R in SO(n); "The constant C(U) can be chosen
  uniformly for a family of domains which are Bilipschitz equivalent with controlled Lipschitz constants. The
  constant C(U) is invariant under dilations."  History: "The estimate (63) was established by John [41, 42] under
  the stronger hypothesis that v is locally Bilipschitz".
* "b) Scaled rigidity estimates in thin domains. In a thin domain Omega_h = S x (-h/2, h/2) the constant in the
  rigidity estimate degenerates as h -> 0. We show that globally the constant degenerates like h^{-2}. Locally one
  can obtain a good approximation of grad w by covering Omega_h by cubes of size h and using a constant rotation in
  each cube."
* Theorem 10 (plates, rescaled gradient grad_h): maps R : S -> SO(3) and Rtilde with ||grad_h y - R||^2 <= C E,
  ||grad Rtilde||^2 <= C E / h^2, and "Moreover there exists a constant rotation Qbar in SO(3) such that
  ||grad_h y - Qbar||^2_{L2(Omega)} <= (C/h^2) E (66)", E = int dist^2(grad_h y, SO(3)).  "Proof. The result is
  implicit in [31]" ([31] = FJM 2002).
  => the thin-domain degeneration of the constant (squared constant h^{-2}, i.e. gradient constant (size/thickness))
  IS stated in print, for plates.

(b) **Mora–Müller, rods (MPI MIS preprint 93/2002 = Calc. Var. PDE 18 (2003)).**  Reading level: opened; §2 read in full.
* Setting: Omega = (0,L) x S, grad_h y = (d_1 y | h^{-1} d_2 y | h^{-1} d_3 y).  Proof of Theorem 2.1: apply the
  rigidity theorem on the sets (a, a+2h) x S_h -> a piecewise constant R^{(h)} : [0,L] -> SO(3) with (2.6)-(2.7);
  compare neighbouring cells inside (a, a+4h) -> (2.8)-(2.9); "iterative applications of the estimates (2.8) and
  (2.9) yield
     int_{I'} |R^{(h)}(x_1 + xi) - R^{(h)}(x_1)|^2 dx_1 <= C (|xi|/h + 1)^2 int_Omega dist^2(grad_h y^{(h)}, SO(3)) dx
     <= C(|xi| + h)^2   (2.10)".
  "The argument follows closely the proof of Theorem 4.1 in [6]" ([6] = FJM 2002).
  => THIS IS THE MECHANISM of the statement under review, in the continuum: a rotation per cell of size h, rotations
  of overlapping cells compared, differences accumulated along the rod with the factor (number of cells), in L2.
  The first inequality of (2.10) is a rigidity estimate with constant (|xi|/h + 1), valid for every y (the energy
  bound is used only in the last step).

(c) **Mora–Müller, Ann. IHP (C) 21 (2004) 271-293 (open archive).**  Reading level: opened; Theorems 2.1, 2.2 and the
first page of the proof.  Theorem 2.2 (energy <= C h^4): piecewise constant R^{(h)}, a mollified Rtilde^{(h)} and
"constants Rbar^{(h)} in SO(3)" such that for ytilde := Rbar^T y - c: ||grad_h ytilde - R^{(h)}||_{L2} <= C h^2 (2.3),
||R^{(h)} - Id||_{L^infty(0,L)} <= C h (2.5).  With ||dist||_{L2} <= C h^2 this is: all local frames are within
(C/h) ||dist(grad_h y, SO(3))||_{L2(Omega)} of ONE rotation — the single-rotation statement with the rod scaling,
for sequences (not written as an inequality with explicit dependence on L).

(d) **Scardia, arXiv 0803.0923 (Asymptot. Anal. 47 (2006) 317-343 per arXiv).**  Reading level: opened; Thm 3.1,
Remark 3.2, Thm 3.3 + proof.  Same argument for curved rods: "apply the rigidity theorem to each small curved
cylinder with the same constant. In this way we construct a piecewise constant rotation"; "applying iteratively
estimate (3.12) in neighbouring cubes, one can prove the following difference quotient estimate" (3.14).

(e) **Harutyunyan–Rodrigues, arXiv 2608.00863 (1 Aug 2026).**  Reading level: abstract + introduction.  It says:
"In [9], employing an well-established covering technique (e.g. [2]), Conti and Zwicknagl provide a new proof of the
Geometric Rigidity Estimate with explicit constants."  [9] = Conti & Zwicknagl, "The tapering length of needles in
martensite/martensite macrotwins", ARMA 247:63 (2023).  So the Geometry division's sentence about Conti–Zwicknagl
is supported *as an attribution made by this 2026 paper* (I did not open Conti–Zwicknagl).  "Explicit" there means
explicit dependence on the Lipschitz character and diameter of the domain; thin *plates/shells* are treated, not rods.

(f) The other two addresses of the note under review: arXiv 1908.04021 (P.-F. Yao: lower bounds of optimal exponents
of the thickness in the rigidity inequality for *shells*) and arXiv 2006.08840 (Avetisyan–Harutyunyan–Hovsepyan:
*linear* geometric rigidity, i.e. Korn-type, of shallow thin domains).  [abstracts only]  Neither is about rods or
discrete chains; they support only "the constant degenerates with the thickness".

### 3.9 Discrete (atomistic) rods [20:49 UTC]

(a) **Schmidt & Zeman, arXiv 2208.04199 (Calc. Var. 2023 per search summary).**  Reading level: opened; Lemmas 2.1, 2.3,
Theorem 2.4 + proof.  Atomistic rods on a cubic lattice, cross-section of fixed lattice size ("ultrathin") or growing
("thin"); cell energies depending on the 8 atoms of a cell, with "a suitable penalty term positive in a
neighbourhood of O(3)Id \ SO(3)" (i.e. reflections of a cell are penalised).  Theorem 2.4: "there exist [...] a
sequence of piecewise constant mappings R^{(k)} : R -> SO(3)" with int |grad_k ytilde - R^{(k)}|^2 <= C h_k^2 (2.8)
and
   |R^{(k)}(i h' + 3h'/2) - R^{(k)}(i h' + h'/2)|^2 <= (C/h_k) ||dist(grad_k ytilde, SO(3))||^2_{L2((u_i,v_i) x S^ext)}  (2.9);
"It is based on a now well-known result about geometric rigidity from [FJM02] and is essentially contained in
[MM03]."  => the discrete-lattice version of steps 1-2 of the proof under review is in print (neighbouring cells'
rotations differ by at most the local strain); the summation to one rotation is not written as an inequality
(they need compactness, not a constant).

(b) **Lazzaroni–Palombaro–Schlömerkemper, arXiv 1501.07505 (DCDS-S 2017 per my memory — journal not verified).**
Reading level: opened; intro passages, Remark 2, Theorem 3.1, Lemma 3.2.  Lattices tessellated into tetrahedra and
octahedra, harmonic nearest-neighbour springs, thin wires (dimension reduction).  Lemma 3.2: "There exists C > 0
such that dist^2(F, SO(3)) <= C sum_{i=1}^6 (|F w_i| - 1)^2 for every F in GL^+(3)" (w_i the six edge vectors of the
regular tetrahedron): THE ONE-SIMPLEX STEP (energy of the six bond lengths controls the distance of the affine map
from the rotations), for orientation-preserving F.  "we always impose a non-interpenetration condition, which
ensures that the deformations of the discrete setting preserve the orientation of each cell [...] The
non-interpenetration assumption can be dropped if one takes into account interactions beyond nearest neighbours,
see the recent work [1]."  [1] = Alicandro–Lazzaroni–Palombaro.

(c) **Alicandro–Lazzaroni–Palombaro, Netw. Heterog. Media 13 (2018) 1-26.**  Reading level: ABSTRACT ONLY (publisher's
page through the fetch tool; PDF not reachable).  According to the abstract: "The lattice energy includes at least
nearest and next-to-nearest neighbour interactions: the latter have the role of penalising changes of orientation."
=> the role the separation-4 distances play in the statement under review (excluding a reflection between
neighbouring cells) is played there by next-to-nearest-neighbour bonds.  The theorem(s) of that paper NOT READ.

Assessment after 3.8-3.9: the three steps of the proof idea (a rotation per simplex/cell from its edge lengths;
neighbouring cells compared, reflections excluded by longer bonds or an orientation condition; accumulation along
the rod with the factor number-of-cells) are each in print in the rod-theory literature, continuum and lattice.
What I have NOT found in print: the same argument for an arbitrary (non-lattice) chain of simplices observed through
distances, stated as a rigidity/stability inequality with a single isometry and the n^2 constant.

### 3.10 The one-window step: Arias-Castro–Javanmard–Pelletier, arXiv 1810.09569v2 (JMLR 21 (2020) per A-C&V) [20:52 UTC]
Reading level: opened; statements of Theorem 1, Corollary 1, Corollary 2 read (proofs not).
* Theorem 1 (Procrustes): "Consider two tall matrices X and Y of same size, with X having full rank, and set
  eps^2 = ||Y Y^T - X X^T||_p. [...] if ||X^dagger|| eps <= 1/sqrt 2, then min_{Q in O} ||Y - XQ||_p <= (1 + sqrt 2)
  ||X^dagger|| eps^2."  — Gram matrices close => configurations close up to an orthogonal map, constant 1/sigma_min.
  This IS step 1 of the proof under review (their "local Procrustes lemma": ||M - R|| <= 2e/tau^2), with a better
  constant; the dependence tau^{-2} for the relative error (tau^{-1} for the absolute one) is therefore in print.
* Corollary 2 (classical scaling on m points of radius rho and half-width omega): RMS error <= 3 sqrt(d) rho eta^2 /
  omega^2 under eta/omega <= 1/sqrt 2, eta^4 = m^{-2} sum (lambda_ij - delta_ij)^2.
  (A-C&V's Lemma 2.2 is this with "width" and "diameter" defined differently — their footnote 3.)

### 3.11 Synchronisation on graphs [20:52 UTC]
Bandeira–Singer–Spielman, arXiv 1204.3873: keyword scan + theorem list only.  Relates the minimal "frustration" of an
O(d) potential to eigenvalues of the connection Laplacian; "It is clear that if one wants to bound full frustration
constants, a dependency on lambda_2(L_0) is needed."  No path-graph statement (on a tree synchronisation is exact).
Not a source for the chain bound.  The spectral-gap dependence 1/lambda_2 is explicit in Chaudhury–Khoo–Singer
Theorem 13 (3.6).  MY OWN REMARK (not a citation): the n^2 of the statement under review is the product of two
discrete Poincaré constants of a path with n vertices (each of order n): one for the frames, one for the positions.

### 3.12 Discretizable distance geometry and geometric build-up [20:52 UTC]
All four at keyword-scan level plus the passages quoted:
* Liberti–Lavor–Maculan–Mucherino, "Euclidean distance geometry and applications", arXiv 1205.0349v1: "The GB is very
  sensitive to numerical errors [64]. In [226], Wu and Wu propose an updated GB algorithm where the accumulated
  errors can be controlled."  No theorem on the growth of the error with the number of points (keyword scan).
* Lavor–Liberti–Maculan–Mucherino, "Recent advances on the DMDGP" (author copy): "it is well known that floating
  point errors often accumulate, which in the long run may invalidate the solution"; "our implementation employs
  several devices in order to limit the propagation of floating point errors".  Qualitative.
* Lavor–Liberti–Mucherino, interval BP (author copy): intervals instead of exact distances; "avoiding the numerical
  instabilities due to solving linear systems".  No stability theorem found by keyword scan.
* Wu–Wu–Yuan, IMA preprint 2175 (2007): "Wu and Wu [12] later proposed an updating scheme to control the rounding
  errors accumulated in the buildup procedure"; "the potential instability of the algorithms due to error
  accumulation. Investigation along this line is underway".  Qualitative.
* NOT OPENED: Luo & Wu, J. Optim. Theory Appl. 149 (2011) ("estimate its numerical errors" per a search summary);
  Sit–Wu–Yuan, Bull. Math. Biol. 2009; Wu & Wu 2007 (updated build-up); Dong & Wu 2003.  These are the places where
  an error-accumulation estimate for build-up could be; none was accessible/opened so far.
=> For Q1 item 4: in what I opened, error accumulation in build-up / branch-and-prune is acknowledged qualitatively;
   no theorem (exponential or polynomial) on its growth with chain length was found.  Basis: keyword scans of four
   documents + search summaries — THIN.

### 3.13 Quantitative rigidity: eigenvalues of stiffness matrices; finite-perturbation statements [20:55 UTC]

(a) **d-dimensional algebraic connectivity.**  [abstracts only, via the arXiv index]
* Lew–Nevo–Peled–Raz, arXiv 2205.05530: "The d-dimensional algebraic connectivity a_d(G) of a graph G=(V,E),
  introduced by Jordán and Tanigawa, is a quantitative measure of the d-dimensional rigidity of G that is defined in
  terms of the eigenvalues of stiffness matrices"; results on complete graphs.
* Presenza–Mas–Giribet–Alvarez-Hamelin, arXiv 2209.14893: "we show that the d-dimensional algebraic connectivity of
  an arbitrary graph G is bounded above by its 1-dimensional algebraic connectivity, i.e., a_d(G) <= a_1(G)".
  => CORRECTION for the note under review: its Theorem K(a) (s_7^2 <= C K^3/n^2 for every configuration) is this
  inequality plus the spectral gap of a band graph; the inequality for arbitrary graphs should be credited to
  Presenza et al. 2022 (per its abstract), the notion to Jordán–Tanigawa (per the abstract of Lew et al.).
  Their note credits "(Jordán–Tanigawa; Lew–Nevo–Peled–Raz)" from memory.  I did not open Jordán–Tanigawa.

(b) **Daitch & Spielman, "Support-Graph Preconditioners for 2-Dimensional Trusses", arXiv cs/0703119v2 (2007).**
Reading level: opened; abstract, definitions, Lemma 3.2 statement and the start of its proof.
* Lemma 3.2 (Path Lemma): "Let T be a k-face simply-connected truss, and let e_0 be a truss element with weight
  gamma(e_0) between any pair v_p, v_q of vertices in the truss, such that in T and e_0: all truss elements have
  lengths in the range [l_min, l_max]; all angles of truss faces are in the range [theta_min, pi - theta_min];
  all weights are in the range [gamma_min, gamma_max] [...]. Then: lambda_max(A_{e_0}, A_T) = O(k^3)".  In words (their
  sentence): "a simply-connected set of faces that connects two vertices supports the matrix of an element between
  the pair of vertices proportionally to the cube of the number of faces".
  => a POLYNOMIAL quantitative *infinitesimal* rigidity estimate for a chain ("truss path") of k well-shaped triangles
  in the plane: the first-order change of the distance between any two vertices is controlled by the l2 norm of
  the first-order changes of the bar lengths.  MY OWN CONVERSION (not in the paper): with |v_p - v_q| <= k l_max this
  reads |delta d_pq| <= C k^2 ||delta d||_2 — the exponent 2 of the statement under review, in dimension 2, to first
  order, for one pair.

(c) **Kyng–Peng–Schwieterman–Zhang, "Incomplete Nested Dissection", arXiv 1805.09442v1 (2018).**
Reading level: opened; abstract, definitions, Lemma 3.3, proof outline, Lemmas 4.1/4.3/4.4 statements.
* Trusses = tetrahedral meshes that are simplicial complexes with bounded aspect ratio, edge lengths and stiffness
  coefficients ("edge-simple"), "stiffly-connected" (rigidity graph on tetrahedra sharing a face connected, and
  connected around every vertex).  Stiffness matrix = sum over bars of (gamma/length) b b^T with unit vectors b.
* Lemma 3.3: "Let T be an edge-simple and stiffly-connected 3D truss. Let n be the number of vertices of T and Delta
  be the diameter. Let M denote the associated stiffness matrix. Then, lambda_min(M) = Omega(n^{-1} Delta^{-4}) and
  rank(M) = 3n - 6."  "Such a bound is analogous to the bound on minimum eigenvalues of a path in a graph."
* On their 3D analogue of the path lemma (Lemma 4.4, a factor 2^{-Theta(h)} in the hop distance h): "our
  calculations result in an exponential factor loss depending on the 'hop distance' between the first and last
  tetrahedrons. This is due to the accumulation of rotational operators, which we need to treat as matrices
  instead of simple rotations. We are not sure whether this exponential increase is simply due to an algebraic
  artifact in our proof."  They avoid it by averaging over "centerings" (Lemma 4.3).
  => IMPORTANT for the verdict: a polynomial *infinitesimal* bound for 3D tetrahedral trusses is in print.  A chain
  of face-sharing tetrahedra that is a genuine simplicial complex with bounded shape is a stiffly-connected
  edge-simple truss, so lambda_min >= c/(n Delta^4); for a rod-like chain (Delta ~ n) this is s_7 >= c n^{-5/2},
  i.e. an infinitesimal stability constant <= C n^{5/2} [my conversion; exponent 5/2, not 2].  Not global, not for
  chains whose consecutive tetrahedra overlap, weaker exponent — but "the only published bound for this case is
  exponential" is no longer accurate as a statement about what is in print.
  The same paper documents that an exponential loss "due to the accumulation of rotational operators" was a known
  obstacle in 2018 — the obstacle the proof under review removes by comparing orthogonal frames.

(d) **Holmes-Cerfon–Theran–Gortler, "Almost-rigidity of frameworks", arXiv 1908.03802v2.**  Reading level: opened;
abstract, Theorem III (end), Corollaries 3.3-3.4.  Finite-perturbation statements with explicit radii for a general
framework: e.g. Corollary 3.3: if eps = |e(q) - e(p)| (l2 change of *squared* edge lengths) is below a threshold,
"either |q - p| < eta_max(eps), or |q - p| > eta_3"; Corollary 3.4 (first-order rigid, sigma_0 = smallest nonzero
singular value of the rigidity matrix): any other configuration with the same edge lengths is at distance at least
0.618 sigma_0/(2z)^{1/2}.  LOCAL (an annulus is excluded, nothing is said beyond eta_3) and in terms of sigma_0 —
for a chain the radii shrink like the smallest singular value (~ n^{-2}).  A relative, not the statement.

(e) Z. Zhao, arXiv 1907.06441 (withdrawn by its author; last full version v4 scanned): only the qualitative remark
"if every point is only connected to nearby points, accumulated errors may make the global structural error
significantly larger than the local errors".  Not a source.

### 3.14 Band graphs ("generalized path graphs") in the literature on rigidity eigenvalues [20:59 UTC]  — IMPORTANT

(a) **Lew–Nevo–Peled–Raz, "Rigidity expander graphs", arXiv 2304.01306v1 (Combinatorica 45 (2025) per the reference
list of arXiv 2505.16015).**  Reading level: opened; abstract, statements in the introduction, §7.1 in full.
* a_d(G) := sup over configurations p of the (binom(d+1,2)+1)-th smallest eigenvalue of the stiffness matrix
  L(G,p) = R^T R with unit direction vectors (the "d-dimensional algebraic connectivity" of Jordán–Tanigawa).
* Theorem 1.6: "Let d >= 2, and let G be a graph. Then, a_d(G) <= a(G)."  "generalizing the case d = 2 proved by
  Jordán and Tanigawa in [14, Theorem 4.2]"; "Theorem 1.6 was proved recently and independently in [22]"
  ([22] = Presenza–Mas–Giribet–Alvarez-Hamelin, arXiv 2209.14893).
* §7.1: "Let P_{n,d} be the graph on vertex set [n] with edges {{i,j} : 1 <= i < j <= n, j - i <= d}. [...] It is not
  hard to check that, for n >= d+1, P_{n,d} is minimally rigid in R^d."
  Proposition 7.7: 1 - cos( (pi/2) / ceil(n/d) ) <= a_d(P_{n,d}) <= 2d - 2 sum_{k=1}^d cos(2k pi/n); "For large n
  [...] ≈ d^2 pi^2/(8 n^2). Moreover, 2d - 2 sum cos(2k pi/n) <= 2 pi^2 d(d+1)(2d+1)/(3 n^2). Therefore,
  a_d(P_{n,d}) = Theta_d(1/n^2)."  Conjecture 1.8: a_d(G) >= a_d(P_{n,d}) for every d-rigid graph on n vertices.
  The lower bound uses (proof of Thm 1.3) the configurations p_c(u) = (c x_i, u), u in A_i = {k ≡ i mod d},
  x_1..x_d the vertices of a regular simplex, c -> infinity: a straight prism whose cross-section is much larger
  than its length.
* Consequences for the note under review (my reading):
  - its Theorem K(a) (for every configuration and every pattern of range K, s_7^2 <= C K^3/n^2) is Theorem 1.6 +
    the circulant bound, IN PRINT, with a better constant (2 pi^2 K(K+1)(2K+1)/(3n^2), and pi^2 K(K+1)(2K+1)/(6 n^2)
    via arXiv 2505.16015 Prop. 13, against their 5 pi^2 K(K+1)(2K+1)/(3 n^2));
  - a *polynomial infinitesimal* rigidity bound for the band graph exists in print: at the prism configurations
    the rigidity eigenvalue is >= c_d/n^2, i.e. an infinitesimal constant of order n (not n^2) — for a different
    family of configurations (thick prisms, c -> infinity) than thin rods, and with distance errors measured
    through unit directions.  It does not contradict the n^2 lower bound on thin tubes.
  - the exact order of the stability constant *as a function of the configuration* (thin rod: n^2) is not in
    these papers; they ask for sup over configurations only.

(b) **Alvarez-Hamelin–Giribet–Mas–Presenza, arXiv 2505.16015v2 (4 Sep 2026).**  Reading level: opened; intro, Thm 4,
§4.2.1.  Theorem 4: a_d(G) <= a_1(G); "The special case d = 2 was previously proved by Jordán and Tanigawa [15, Th.
4.2]. The general case for d >= 2 was first introduced in a preliminary (unpublished) version of this work
available at [19], and was later independently proved by Lew et al. [16] using probabilistic methods."
"generalized path graph P_{n,d}" (edges |i-j| in {1..d}); Prop. 13: a_1(P_{n,d}) <= a_1(C_{2n,d}); "it is natural to
conjecture that a_d(G) >= a_d(P_{n,d}) [...] Thus, it is of interest to derive precise expressions for a_d(P_{n,d})."
Also: "Zhu and Hu [13] and Zelazo et al. [14] introduced the positive semi-definite stiffness matrix [...] The
latter is known as the rigidity eigenvalue of (G, p)".
  => supersedes my note in 3.13(a): the credit for a_d <= a_1 is: Jordán–Tanigawa (d = 2), Presenza et al. 2022
  and Lew et al. 2023 independently (general d).  The note under review names Jordán–Tanigawa and
  Lew–Nevo–Peled–Raz from memory: right authors; the paper is "Rigidity expander graphs"; Presenza et al. missing.

(c) **Väisälä, "A survey of nearisometries", arXiv math/0201098 (Report Univ. Jyväskylä 83 (2001) 305-315 per arXiv).**
Reading level: opened; §4 read.  *Complete* distance data, sup norm: a map f on A ⊂ R^n with
| |fx - fy| - |x - y| | <= s for all x, y is an s-nearisometry; A has the c-IAP if every s-nearisometry A -> R^n is
within c s of an isometry.  "The thickness of a bounded set A ⊂ R^n is the number theta(A) = inf_{|u|=1} d(pi_u A)."
Theorem 4.7: for bounded A without isolated points, "(1) A has the c-IAP, (2) theta(A) >= d(A)/c'" are
"quantitatively equivalent"; "Part (2) => (1) was proved in [ATV1, 3.3], and it is true for all bounded sets."
([ATV1] = Alestalo–Trotsenko–Väisälä, Israel J. Math. 125 (2001) — not opened; per a search summary of its
abstract the bound is c_n eps/q for a set of diameter 1 and thickness q.)  John's method (1961) for locally
(1+eps)-bilipschitz maps on balls / John domains is recalled (4.3-4.4).
  => global quantitative rigidity from ALL pairwise distances with a constant governed by diameter/thickness (the
  aspect ratio) is in print since 2001.  It is the complete-data counterpart of the statement under review and the
  natural upper bound to set against their Corollary K.1 remark on complete data on rods.  The word "thickness"
  is used there for the minimal width of the whole set (not of a window).

(d) Chang–Sahai (EURASIP J. Appl. Signal Process. 2006, author copy): keyword scan only — Cramér–Rao bounds for
anchored and anchor-free localisation, scaling in network size discussed for random networks; no chain/strip law
found by the scan.  Heng–Gao (arXiv 1305.7272), Huang–Yu–Anderson (1-D networks): abstracts only; no bending law.

(e) NASA CR 189568 (Balakrishnan 1991), abstract only: lattice trusses "with identical bays" modelled by "an
equivalent one-dimensional Timoshenko beam model" — evidence that the beam picture of a truss chain is standard;
no statement of an n^{-4} eigenvalue read.  The n^{-4} law itself (free-free beam: omega^2 ∝ EI/(rho A L^4)) I can
only give FROM MEMORY as textbook beam theory; I did not open a source that states it for a discrete truss.

### 3.15 Explicit length-uniform rod estimates: Blanchard–Griso [21:05 UTC]
arXiv 1010.3614v1 ("Asymptotic behavior of structures made of straight rods").  Reading level: opened; abstract,
§3.2, Theorem 3.2, Theorem 4.1 statement.
* "any deformation v in H^1(P_delta; R^3) can be decomposed as v(s) = V(s) + R(s)(y_2 n + y_3 b) + vbar(s)" with
  R(s) in SO(3), R in H^1(0,L).  Theorem 3.2 ("The following theorem is proved in [6]", [6] = Blanchard–Griso,
  "Decomposition of deformations of thin rods. Application to nonlinear elasticity", Anal. Appl. 7 (2009) 21-71):
     ||dR/ds||_{L2(0,L)} <= (C/delta^2) ||dist(grad v, SO(3))||_{L2(P_delta)},
     ||dV/ds - R t||_{L2(0,L)} <= (C/delta) ||dist(grad v, SO(3))||_{L2(P_delta)},
     ||grad v - R||_{L2} <= C ||dist(grad v, SO(3))||_{L2(P_delta)},
  "where the constant C does not depend on delta and L_i."  Theorem 4.1 (clamped rod structures):
  ||v - I_d||_{H^1(S_delta)} <= (C/delta) ||dist(grad v, SO(3))||_{L2(S_delta)}.
* => for EVERY deformation of a thin rod (not only for sequences) there is a rotation field along the axis whose
  derivative is controlled by the strain with a constant uniform in thickness and length.  By Cauchy–Schwarz
  |R(s) - R(s')| <= |s-s'|^{1/2} (C/delta^2) ||dist||: the frame error accumulated over a length is at most the square
  root of that length times the L2 norm of the strain — the same sentence as in the proof under review.  A single
  rotation with constant C L/delta for the gradient and C L^2/delta for the displacement follows in two lines
  [my derivation; the single-rotation inequality for a free rod is not displayed in what I read].
  THE CONTINUUM COUNTERPART OF THE STATEMENT UNDER REVIEW IS IN PRINT WITH LENGTH-UNIFORM CONSTANTS.

### 3.16 The reflection step in print: Alicandro–Lazzaroni–Palombaro, arXiv 1601.05968v2 [21:05 UTC]  — IMPORTANT
"Interactions beyond nearest neighbours and rigidity of discrete energies: a compactness result and an application
to dimension reduction".  Reading level: opened; abstract, introduction, Theorem 1.1, Lemmas 1.2-1.3 (statements,
start of the proof of 1.3).  (Journal versions: Netw. Heterog. Media 13 (2018) [abstract read] and, per a search
summary, a companion in Calc. Var. 2017 — not opened; I do not know how the arXiv text was split.)
* Lattice points, Kuhn triangulation into N-simplices, pair energies of nearest and next-to-nearest neighbours,
  E_cell(u_F; T) = sum over the edges of the simplex of | |F(x_i - x_j)| - |H(x_i - x_j)| |^p.
* Lemma 1.2: dist^p(F, SO(N)H) <= C E_cell(u_F; T) for det F >= 0, and dist^p(F, (O(N)\SO(N))H) <= C E_cell(u_F; T)
  for det F <= 0.  [= step 1 of the proof under review: edge-length errors of one simplex control the distance of
  the affine map from the orthogonal group.]
* Lemma 1.3: "There exists a positive constant C_0 (depending on H) with the following property: if two
  neighbouring N-simplices S, T have different orientations in the deformed configuration, i.e.,
  det(grad u|_S) det(grad u|_T) <= 0, then E_cell(u; S ∪ T) >= C_0."  Proof idea as printed: otherwise grad u|_S is
  close to "the reflection across the facet shared by S and T", and the bond between the two vertices x_0, y_0
  opposite to the shared facet is badly violated.  [= step 2 of the proof under review: the distance between the
  two apexes of consecutive windows (their separation-4 pair) excludes a reflection.]
* Abstract: "interactions beyond nearest neighbours have the role of penalising changes of orientation and, to some
  extent, they may replace the positive-determinant constraint".
  => steps 1 and 2 are in print for lattice simplices (2016); step 3 (accumulation along the rod) is the
  Mora–Müller argument used in the second part of that paper for nanowires (not read by me in that paper).

### 3.17 "Errors of orthogonal alignments add" in a stitching paper (2026) [21:05 UTC]
Nguyen-Cong–Hy–Dinh, arXiv 2604.21094v1 (22 Apr 2026), "Spectral Embeddings Leak Graph Topology: ...".
Reading level: opened; Lemmas 17-18 and proof B.11.  Lemma 18: embeddings aligned "by propagating pairwise
Procrustes rotations from a root vertex" satisfy ||X_u - Z_u||_F <= O(depth(u) · E_align) + O(E_local); "This result
reveals a fundamental limitation of sequential stitching: alignment errors accumulate linearly with depth."
Proof: "Using the triangle inequality and norm preservation by orthogonal matrices: ||Delta R_u||_F <= ||Delta R_p||_F +
||Delta Q_pu||_F" (first order: "we dropped the second-order term").  Different problem (spectral embeddings of graph
patches, no translations, no lever arm) — but the sentence "rotation errors add because orthogonal maps preserve
norms" is in print there, in the patch-stitching literature.

### 3.18 Not accessible / not opened although relevant (to be listed in the report) [21:05 UTC]
* SIAM journal version of Arias-Castro–Vishwanath (HTTP 403).
* Anderson–Shames–Mao–Fidan, SIAM J. Discrete Math. 24 (2010) (closed; known only through A-C&V's description and a
  search summary of the abstract).
* Schrader, "Propagation of errors in schematic chains of triangles in space with measured distances", Bull. Géod.
  86 (1967) 427-432 — PAYWALLED, title only.  By its title the closest classical item (first-order error
  propagation along a spatial chain with measured distances).
* The translated Soviet report DTIC AD0650359 (triangulation vs trilateration links; HTTP 403); Bomford's "Geodesy";
  Chrzanowski–Konecny 1965 (cited by A-C&V) — not found/opened.
* Luo–Wu, JOTA 149 (2011) 580-598 ("We estimate its numerical errors") — abstract only; Sit–Wu–Yuan 2009;
  Wu–Wu 2007; Dong–Wu 2003 — not opened.
* Niculescu–Nath (MobiHoc 2004), Savvides et al. (IPSN 2003 / IEEE TMC 2005), Huang–Yu–Anderson (Signal Process.
  2011) — records/abstracts only.
* Friesecke–James–Müller, CPAM 55 (2002) — the original; known through the restatements in the 2005 preprint,
  Mora–Müller, Scardia.  Conti–Zwicknagl, ARMA 247 (2023) — not opened.  Blanchard–Griso, Anal. Appl. 2009 — the
  theorem read as restated in arXiv 1010.3614.  Alestalo–Trotsenko–Väisälä 2001 — through Väisälä's survey.
  Jordán–Tanigawa 2022 — through the citations in Lew et al. and Alvarez-Hamelin et al.
* Li–Li–Ye (alignment-matrix eigenvalue bounds, Commun. Math. Sci. 2007) — page not rendered.
* Alicandro–Lazzaroni–Palombaro, Netw. Heterog. Media 2018 — abstract only (but the arXiv text 1601.05968 read).
* John 1961 ("Rotation and strain"), Kohn 1982 — from memory only.

### 3.19 Corrections of my own notes, and two hand checks [21:09 UTC]

* CORRECTION to 3.13(b) (Daitch–Spielman).  My "own conversion" there was wrong: the Path Lemma requires the element
  e_0 between v_p and v_q to have its length in [l_min, l_max] as well ("such that in T and e_0 all truss elements
  have lengths in the range [l_min, l_max]"), so I may not insert |v_p - v_q| <= k l_max.  What the lemma gives, for
  two vertices at bounded distance joined by a path of k well-shaped triangles: (first-order change of |v_p - v_q|)^2
  <= C k^3 * sum over bars of (first-order change of the bar length)^2, i.e. a factor k^{3/2} in l2 -> one distance.
  This is the exponent 3/2 of the *pointwise* estimate inside the proof under review (|y_i - g x_i| <= 3.94 b
  ||xi||_2 i^{3/2}), whose l2 sum over the points gives n^2.  So the Path Lemma is the 2D, first-order, one-pair
  counterpart of that pointwise step — with the same exponent.
* CORRECTION to 3.13(a): superseded by 3.14(b) (credit for a_d <= a_1).
* CORRECTION to 3.3 (Javanmard–Montanari, Lemma 6.2): the printed constant is C r^{-1} (unit cube); "factor ~
  length/r = number of cells" is my reading of the proof (stress bounded by C |x_m| / sigma_min with sigma_min >= C r).
* Hand check 1 (check_band_gap.py, output check_band_gap.out): for n in {12,20,40,80}, K in {3,4,6}:
  a(P_{n,K}) <= a(C_{n,K}) = 2K - 2 sum cos(2 pi k/n) <= 2 pi^2 K(K+1)(2K+1)/(3n^2), a(P_{n,K}) <= a(C_{2n,K}) <=
  pi^2 K(K+1)(2K+1)/(6 n^2), and lambda_7 of the stiffness matrix of random configurations <= a(P_{n,K}): ALL OK.
  [N; my own code, 12 cases, 3 random configurations each]
* Hand check 2 (check_prism.py, output check_prism.out): band graph |i-j| <= 3 in R^3 at the prism configurations
  of the proof of Lew et al.'s Theorem 1.3 (c = 1000): lambda_7 n^2 = 11.10 for n = 12, 24, 48, 96, equal to the
  printed lower bound 1 - cos((pi/2)/ceil(n/3)) ≈ 9 pi^2/(8 n^2) to three digits; at a thin helix (radius 1,
  rise 0.6) lambda_7 n^4 ≈ 145, 594, 1058, 1116.  So: prism-like thick configurations have an infinitesimal constant
  of order n (0.3 n), thin helices of order n^2 (≈ n^2/33) — consistent with both printed bounds and with the
  bending lower bound of the note under review.  [N; my own code]
* Cucuringu–Singer–Cowburn, arXiv 1111.3304 (keyword scan): "In general, there exist very few theoretical
  guaranties for graph localization algorithms, especially in the presence of noise. [...] a complete analysis of
  the noise propagation through the pipeline [...] is out of our reach at the moment".  No stability theorem.

### 3.20 Three late additions [21:17 UTC]

* **Aspnes, Eren, Goldenberg, Morse, Whiteley, Yang, Anderson, Belhumeur, "A Theory of Network Localization"**
  (manuscript headed "TRANSACTIONS ON MOBILE COMPUTING, DECEMBER 2005"; IEEE Trans. Mobile Comput. 5(12) (2006)
  1663-1678 per the reference list of Arias-Castro–Vishwanath).  Reading level: opened; Definition 3, Theorem 8, the
  passage after Corollary 3, Theorem 10; rest by keyword scan.  (The file came from an address that a search had
  returned without a title.)
  - Definition 3: "A trilaterative ordering in dimension d for a graph G is an ordering of the vertices 1, ..., d+1,
    d+2, ... n such that K_{d+1}, the complete graph on the initial vertices, is in G, and from every vertex j > d+1,
    there are at least d+1 edges to vertices earlier in the sequence."  Theorem 8: "Trilateration graphs in
    dimension d are generically globally rigid in dimension d."  Theorem 10: "A trilateration graph G = (V, E) with
    realizable edge weights is realizable in a polynomial number of trilaterations."
  - On errors (after Corollary 3, in the section on the hardness of realization): "What we do not know at present
    is whether these results continue to hold for solutions that have large positional errors but that give edge
    lengths close to those in the input. Our suspicion is that edge-length errors accumulate at most polynomially
    across the graph, but we have not yet carried out the error analysis necessary to prove this."  Conjecture 1
    follows (relative edge-length errors bounded by eps/n^c).
  => the founding paper of lateration graphs prints, as a *suspicion without proof* and for the graphs of its
  hardness construction (not for band lateration graphs), that edge-length errors accumulate at most polynomially.
  This is the nearest printed anticipation of a polynomial accumulation law in the localisation literature.
* Drusvyatskiy–Krislock–Voronin–Wolkowicz, arXiv 1410.6852v2 (keyword scan + one passage): facial reduction over
  cliques "is highly unstable when the distance measurements are corrupted by noise"; "even if pairs of cliques can
  robustly yield some facial information, the accumulated error compounds as the algorithm moves from clique to
  clique."  Their remedy: aggregate "dual" representations.  No growth law.
* Not accessible: the repository record of the Sit–Wu–Yuan build-up preprint (HTTP 403).  Boumal–Singer–Absil–Blondel
  (Cramér–Rao bounds for synchronisation of rotations) not found by two title queries of the arXiv index — from
  memory only, not used.

### 3.21 A correction of my own reading (prism configurations), and the state at the end [21:25 UTC]

* CORRECTION to 3.14(a) and to hand check 2 in 3.19: I concluded there that "thick chains do not attain n^2 in
  general".  Wrong as stated.  The configurations of Lew et al.'s lower bound are prisms whose cross-section exceeds
  their length (c -> infinity for fixed n; window aspect ratio D/tau ~ c).  With a FIXED window geometry a straight
  prism is a rod as soon as it is longer than wide, and Theorem K(c) of the note under review applies to it
  (order n^2).  My own numbers show the crossover: c = 10 gives lambda_7 n^2 = 10.7 for n = 12, 24, 48 and 6.9 for
  n = 96.  What the printed proposition supports: the order n of K(a) is attained over all configurations, so K(a)
  cannot be improved without an assumption on the configuration.  It does NOT decide the open end of their §6
  (compact chains of fixed window geometry).  The report says only this (§2.6, §4, §5.3 item 9).
* Report written: docs/science/workstreams/A4_REPORT.md (sections 0-6; the search log embedded in §5.1).
* Quotations: check_quotes.py — 122 quotations found verbatim in the extractions (or in the read-only copies, for
  phrases of the note under review); 77 not matched mechanically, inspected by eye (categories listed at the end of
  check_quotes.out): transcribed formulas / restored subscripts, two-column or page-break passages, titles,
  abstracts from the arXiv index or the fetch tool, my own wording, log entries.
* Method disclosure: the page-fetch tool returns summaries and at most ~125 characters verbatim, so I read the
  papers from text extractions of direct downloads of the same public addresses (as an earlier literature
  workstream of this division did).  Servers refused: epubs.siam.org (403), apps.dtic.mil (403; and an HTML page
  instead of the PDF), dept.aem.umn.edu (404), conservancy.umn.edu item page (403), two OpenAlex filter URLs (400);
  none was retried by another route.  Journal data of the SIAM paper came from the Crossref record.
* No tool action of mine was declined by the permission system.

### 3.22 Closed [21:26 UTC]
Report closed (21:26 UTC).  The 34 text extractions were removed one by one (manifest with addresses and checksums:
sources_manifest.tsv; regeneration: regen_sources.sh).  Files of this workstream: this directory and
docs/science/workstreams/A4_REPORT.md; nothing else was written, modified, moved or deleted; no state-changing git
command was run; no subagent was used.
(Addendum to 3.22: the page-fetch tool itself saved three scanned PDFs — the NASA/NTRS reports of log rows 35, 36,
90 — in the harness's own tool-results folder outside the repository; I read their first pages there and did not
touch them otherwise.)
