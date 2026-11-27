# Workstream R10 — NOTES (kept from the first minute)

Reviewer: independent reviewer R10, science division.  Started 2026-11-25.
Object: theory division's `docs/workstreams/Y_REPORT.md` at commit `658b77f`
(read-only export `/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_658b77f`).

Conventions in these notes: REVIEW = read and re-derived by me; REPL = re-computed with my
own code written from the definitions before opening their code; RERUN = their code run
from a scratch copy.

## Log

* [t0] Read COMMON.md and R10_brief.md in full.  Created this directory.  Have NOT opened
  anything under `experiments/workstreams/Y/` in the export; will not until my own code for
  items 1(a)-(d) and 2 exists and has produced numbers.
* [t0+10min] Read `Y_brief.md` (136 lines) and `Y_REPORT.md` (612 lines) in full — the report
  text only, none of the code/outputs.  Plan (own code first):
  1. r10_01: controls (cube closed form; super-site of 2,3 independent sites, own vertex
     enumeration; own Arimoto + dual certificate).
  2. r10_02: brute force of (U) Y1, (L) Y2, (L') Y3 on random inhomogeneous chains,
     asymmetric envelopes.
  3. r10_03: exact small-n F*_n, E_n, a_n (n<=4 all 990 vertices, n=5 all 395094):
     non-Markov centre, non-additive vertices at p=0.1.
  4. r10_04: E_F closed form; Prop. H (tilted Markov labels) own derivation, brute-force
     check, own moment-Lyapunov computation; Prop. I (block-wise labels).
  5. r10_05: Prop. F (Markov recursion) L=1,2,3; r10_06: Prop. G tilt-state recursion, own
     conservative discretisation.
  6. r10_07: sub/super-additivity of F+_L, F-_L.
  7. r10_08: Markov-type quantile counterexample.
  8. headline map in (p,u); refutation attempts (large u, small p); small-slope derivation
     (variance / susceptibility); second chain (Potts / NNN).
  9. prior art.
  First thoughts written down BEFORE any computation (to be checked, may be wrong):
  - F*(t) = (1-t) x Renyi capacity of order t (Sibson/Csiszar) of the channel
    label -> Gibbs law; max_phi over the class is attained at extreme rays of the convex
    cone {v=e^{-phi}: v(y) <= e^{d(x,y)} v(x)} = vertices of the Lipschitz polytope.
  - Second order in the slope: (1-t)D_t(pi(1+a)||pi(1+b)) ~ t(1-t)/2 ||a-b||^2_pi, hence
    F*_n(t) ~ t(1-t)/2 * max_{phi in C_d} Var_pi(phi) for symmetric envelopes (centre 0 by
    symmetry).  So the small-slope factor relative to the cube is
    max_{phi Lip} Var_pi(phi) / (n u^2/4); for associated (ferromagnetic) spins the
    Lipschitz covariance inequality gives max Var = (u/2)^2 Var(m), i.e. the factor is
    chi = sum_k <s_0 s_k> = (1+lam)/(1-lam) = (1-p)/p.  To be tested numerically and on a
    non-ferromagnetic chain (where the factor should NOT be the k=0 structure factor).
  - Large slopes: F(t) <= (1-t) ln 2 for every reference measure (Q uniform), both cube and
    chain tend to it; heuristically the chain's "channel" is noisier (error rate
    e^{-2h}cosh^2(2K') > e^{-2h}), so the direction for h may REVERSE at large u.  The
    report leaves u>=2 undecided; an upper bound below the cube would refute "raises".
* [r10_01_controls.py, 14 s] REPL of Y section 2 (controls), own code `r10lib.py`
  (own vertex enumeration: integer height functions by a down-set recursion; own Arimoto /
  Blahut-Arimoto / exponentiated-gradient solvers, each with a duality bracket):
  cube u=1: h=0.0291391 (t*=0.4900), a=0.1109441, E=0.1201145 (closed forms AND solver);
  super-site of 2 (3) independent sites, 6 (38) vertices: same per-site values to 1e-7,
  weight on the 2 (30) non-additive vertices 3e-10; additive only: identical; non-additive
  only: h 0.0145696 (0.0194261), a 0.0554720 (0.0763123), E 0.0600573 (0.0800763) -- all
  match Y's table (0.01457 (0.01943), 0.0555 (0.0763), 0.0601 (0.0801)); field control
  (0.7,0.3): 0.0250335, 0.0953005, 0.1031310 -- match.  Vertex counts 2, 6, 38, 990,
  395094 for n=1..5 -- match; weighted cube (1.847,1,1.847): 120 vertices -- match.
  REVIEW: "vertices for one slope = integer height functions" re-derived (parity argument
  is correct: connected tight graph => f(x)-f(y) = dist mod 2 => every edge tight).
* [r10_02_reductions.py, 7 s] REPL (brute force, own code) of Theorems Y1 (U), Y2 (L),
  Y3 (L') on 40 random inhomogeneous chains: 8, 9, 10 binary sites; 6 ternary; mixed
  (2,3,2,3,2,3,2) and (3,2,2,3,2,2,3); random fields, couplings sd 0.3/1/2.5, random
  ASYMMETRIC envelopes (closure of random matrices), random cuts/gauges/gaps (also leading
  and trailing gaps, zero gaps); members: inf-convolutions, cones d(.,y0), -d(y0,.), max,
  min, convex combinations; all pairs (x,y) checked.
  (U): pi = rho e^{-g}/Z to 9e-16; identity to 7e-15 (480 cases); psi+g in C_{d+}: largest
  violation 2e-14; d+ attained (slack left by the best cone 2e-15, for every slack site and
  ordered letter pair); control psi+g in C_d: violated 480/480.
  (L): marginal identity 5e-16; two-sided bound: 0 violations in 480.
  (L'): psi in C_d (2e-14) and A_pi(psi)=A_(x)(psi') (4e-15), 180 cases; 25 of 40 chains had
  an EMPTY d^- class (negative cycle: coupling too strong for the gap) -- consistent with
  Y's caveat; 3 chains had negative entries of d^- but a nonempty class and the statement
  held there too (the proof never uses d^- >= 0).  Control psi' in C_{d_B}: violated 178/180.
  REVIEW: proofs of Y1, Y2, Y3 re-derived line by line (see report): correct.
* [r10_03_small_n.py A: 31 s; D: 40 s] REPL of the exact small-n enumerations:
  - F*_n(0.45)/n at p=0.4, n=1..4: 0.02895 0.03280 0.03359 0.03354 (Y 4.2: identical).
  - E_n = ln Z_n(h)/Z_n(0): n<=4 at p=0.4,0.3,0.1 to 1e-15 (1e-8 at p=0.1,n=4: solver
    tolerance); n=5 at p=0.3 AND p=0.1: dual of the site-wise centre over all 395094 vertices
    equals ln Z_5(h)/Z_5(0) to 3e-9.
  - non-additive vertices: weight < 1e-10 for t=0.25,0.45,0.65 and E at n<=4, all three p.
    a_4(p=0.1) = 0.5726559 vs 0.5626014 site-wise only; weight 0.0920 on f=-min(|x|,4-|x|)
    (exactly Y 7.1).  n=5, p=0.3: site-wise centre is a certificate for t=0.45,0.65,0.85, E, a.
    n=5, p=0.1: dual value of site-wise centre 0.2500923 (t=0.65), 0.1066245 (t=0.85) vs
    site-wise optimum 0.1939640, 0.0928291 (Y: 0.25009, 0.10662, 0.19396, 0.09283).
    NEW (mine): true optimum by column generation over all vertices: F*_5(0.65)=0.1965988
    (+1.4%, weight 0.094 on non-additive), F*_5(0.85)=0.0945869 (+1.9%, weight 0.163).  So the
    effect of non-additive vertices at n=5,p=0.1 is 1-2%, not the 29% that the "dual value"
    might suggest.
  - Renyi centre not Markov: I(x1;x3|x2) = 2.904e-3, 5.730e-3, 1.150e-3 (p=0.4,0.3,0.1; n=4,
    t=0.45) -- matches Y 7.2.  Walsh norms by order at p=0.3: 0, 0.2448, 0, 0.0089; nn pair
    coefficient -0.1000 -- matches.
  - FINDING (minor): Y 7.2 says "for short chains (n=4,t=0.45) the optimal labels are the two
    uniform fields and gamma* = -(1/t) ln cosh(t h m)".  True at p=0.3 and 0.1; FALSE at
    p=0.4: the optimum has 4 labels (uniform fields 0.4165 each, the two-domain labels ++--
    and --++ 0.0835 each), max|gamma* - model| = 0.156.  Their I(x1;x3|x2) at p=0.4 is
    nevertheless the right number (it matches mine with the 4-label optimum).
* [r10_lyap.py, r10_04_lower_bounds.py, 3 s] REPL of the lower ends that need no block
  optimisation.  REVIEW: Prop. H re-derived (gauge tau = sigma*s; tilt by Z(sigma)^t cancels
  the normalisation) -- formula of Y 5.3 is correct, incl. the every-n form.  REPL:
  - moment Lyapunov exponents by two numerically independent methods of mine (exact
    enumeration over 2^21 bond patterns with Aitken; Chebyshev collocation of the transfer
    operator on z = ln(y+/y-), N = 32..96): agree to 1e-11.
  - every-n formula vs the brute-force Renyi form (definition) at n=8, 27 cases: 3e-15.
  - max over (t,c) of G_inf: p=0.4: 0.033503 (0.458,0.774); 0.3: 0.038695 (0.431,0.859);
    0.2: 0.041770 (0.402,0.861); 0.1: 0.039608 (0.364,0.833)  == Y's table 6.4, all digits.
    c=0 (i.i.d. labels): 0.028907, 0.028151, 0.026626, 0.023418 == Y.
  - E_F: 0.169127, 0.232400, 0.310766, 0.401719 == Y; also = ln lam_max(D^1/2 P D^1/2).
  - a from the Prop. H family at t=0.999: 0.116817 (p=0.4; == Y's lower end of a at p=0.4,
    so that entry is "Prop. H at t=0.999", not a limit), 0.123875, 0.122445, 0.101876.
    NOTE: at p=0.1 the Markov-label family gives a >= 0.1019 < cube 0.1109; the direction
    of `a` at p=0.1 rests entirely on Prop. I (0.116632, only 5% above the cube).
* [r10_06_markov_recursion.py, 29 s] REVIEW of Prop. F: proof re-derived, correct (also the
  block version: -ln V of a block is Lipschitz with (u,..,u,u*)).  REPL: u* = 1.2183,
  1.5261, 1.9807, 2.7497; DP bounds L=1,2,3 for h, a, E at all four p agree with Y's table
  6.3 to every printed digit (e.g. p=0.3: h<= 0.054838, 0.051796, 0.049019; a<=0.154011;
  E<= 0.234188, 0.233237, 0.232849).  Finite-n inequality vs exact F*_n (n<=4, 36 cases):
  never violated (smallest margin 5.8e-4).
* [r10_tilt.py, r10_07a, r10_07b] own implementation of the tilt-state recursion (Prop. G)
  with a CELL-based safe discretisation (feasibility of a box of cells decided by corner
  values, using that theta_+- are monotone in each argument; no Lipschitz slack).
  REVIEW: (*) re-derived; solved for theta_+- explicitly.
  - control p=1/2: safe E and a are exact (0.1201145, 0.1109441) at every G; safe Renyi value
    from above (t=0.49: 0.0307683, 0.0295474, 0.0292413 at G=101,401,1601), restricted from
    below (0.0286028, 0.0290037, 0.0291052).
  - p=0.3, t=0.43, q~=0.255: safe 0.045939, 0.045168, 0.044813, 0.044622 (G=201..1601),
    restricted 0.044054 .. 0.044357.  Y: safe(G=1601) 0.04468, restricted 0.04435.  Consistent
    (my safe value is slightly tighter: no 1.5D slack).
  - threshold, Q=pi, p=0.3: my SAFE value equals E_F=0.232400 at every G (201..1601): the
    optimal relaxed policy sits in the extreme cells where the cell-max reward is exact.
    So "E_inf = E_F up to 1.4e-4" (Y 5.4(c)) is confirmed and sharpened to the rounding of
    the computation (to be tabulated for p=0.4,0.2 and checked at p=0.1).
  - finite chains n=3,4,5, 144 cases incl. q~<p: safe >= exact max over ALL vertices in every
    case (smallest margin 1.2e-3).  The relaxation is tight for q~ >= 0.85p and NOT tight for
    q~ = 0.6p (restricted > exact by up to 0.17) -- quantifies Y's "no such test for q~<p".
* Prop. I job (r10_05, first version) killed after 28 CPU-min: Arimoto to 1e-12 inside a
  golden search was far too slow (my mistake); first line it printed: p=0.4, L=12, t=0.459,
  134 labels: G_L=0.4089032, Lambda_blk=-0.0004206 (operator N=64 = N=96 = exact increments
  k=2,3), lam_Q=1  => bound 0.034040 (Y: 0.034026).  Restructured below.
* [r10_08_sandwich.py, 185 s] REPL of Prop. D numerics and of tables 6.1, 6.2 of Y.
  F+_2-2F+_1 = -0.0415,-0.0497,-0.0420 (p=0.4; t=0.3,0.45,0.7), -0.0982,-0.1136,-0.0889 (p=0.3);
  F+_3-F+_1-F+_2 = -0.0421..-0.1150; F-_2-2F-_1 = +0.0196,+0.0229,+0.0189; F-_3-F-_1-F-_2 =
  +0.0310,+0.0351,+0.0274; (F+_3-F-_3)/(tC) = 0.096,0.069,0.035 (p=0.4)  == Y 4.2.
  Table 6.1 (U), 36 entries: largest deviation 4.9e-6 (rounding).  Table 6.2 (L'): all 19
  entries incl. the best gaps m identical.  |V| = 2, 6, 120 for the slack blocks.
  REVIEW of Prop. D (a)-(d): re-derived; correct, with the caveat already in Y that F-_L at
  m=0 needs u > K (u > 2K for L=1); (c) needs d^- >= 0 for "phi^- ignores the end letters,
  hence is in the d^- class".
* [r10_09_markov_types.py 1 s, r10_09b] REPL of the negative result 8.3.
  - Y's explicit example verified literally for n=5..9: class(x)={110..0} singleton, t(x)=3;
    class(y) has n-2 members 0^a 1 0^b, psi values {0,2}, t(y)=0 for q<1/(n-2); d(x,y)=1;
    t(x)-t(y)=3 > 1.  (In weights: e^-3 vs 1: "t_y = 1 > t_x e = e^-2" as Y writes.)
    BUT in that example the TRUNCATED residual is unchanged (psi^tr(x)-psi^tr(y) = 1 = d):
    it shows that the level function is inadmissible, not that the truncation leaves the class.
  - brute force n=9, 74 Markov-type classes (Y: 74), 200 own random residuals x 3 quantiles:
    level function inadmissible in 599/600 (Y: 598/600), largest excess 6 flips (Y: 6);
    cube type classes: 0.  NEW: the truncated residual max(psi,t) itself is inadmissible in
    464/600 (largest excess 4 flips); cube: 0.
  - NEW explicit example for the truncated residual, by hand (n=4, u=1, q=1/2):
    psi = d_H(., 0100); a=1101, class {1101, 1011}, psi = {2, 4}, level 4, psi^tr(a)=4;
    b=0101, singleton class, psi^tr(b)=1; d(a,b)=1; 4-1 = 3 > 1.
* [r10_05_block_labels.py h] Prop. I REPL (identity vs definition at n=6,9,8 with random
  asymmetric M_L: 1e-15; Lambda_blk by operator N=64/96 and exact increments k=2,3 agree to
  1e-7).  Bound at Y's (L,t): p=0.4: 0.034040 (Y 0.034026); p=0.3: 0.040143 (Y 0.040115);
  p=0.2: 0.044618 (Y 0.044599).  Mine are 1.4e-5..2.8e-5 HIGHER (both are valid lower bounds;
  to be explained after reading their code).  L=16 at p=0.3: 0.040166.
* [r10_05 h: 491 s; a: ~15 min under load] Prop. I, all four p (my M_L = over-relaxed Arimoto,
  2500 iterations; ANY M_L gives a valid bound):
  h >= at Y's (L,t): 0.034040 / 0.040143 / 0.044618 / 0.044372  (Y: 0.034026 / 0.040115 /
  0.044599 / 0.044378).  Mine higher by 1.4e-5..2.8e-5 at p=0.4,0.3,0.2 and lower by 6e-6 at
  p=0.1.  With L=16: 0.040166 (p=0.3), 0.044739 (p=0.2), 0.044732 (p=0.1): slightly better.
  a >= (t=0.999): 0.116089 (L=10) / 0.127042 (L=10) / 0.130486 (L=10) / 0.116429 (L=14)
  (Y "best of both": 0.116817 [= Prop. H, replicated exactly] / 0.126444 / 0.129797 / 0.116632).
  All twelve lower ends of Y's table 0.2 are therefore confirmed as valid lower bounds
  (replicated to <= 3e-5 for h, exactly for E_F, to <= 7e-4 for a) and all lie above the cube.
* [r10_07d_upper_ends.py 0.3 801: 233 s] own SAFE tilt recursion, p=0.3:
  E <= 0.232400 = E_F + 3e-11  (Y: 0.232538);  a <= 0.140224 (q~=0.27) (Y: 0.140860);
  h <= 0.044719 (largest grid value 0.044523 at t=0.431, q~=0.2589; interval rule with
  adaptive refinement, 62 grid points; tails t*E_up and (1-t)*a_up) (Y: 0.044995; 0.044821).
  => Y's upper ends at p=0.3 are confirmed (mine are slightly smaller, i.e. Y's are valid
  and a little conservative), and the threshold bracket closes: E_inf = E_F at p=0.3.
* [r10_07c, small p] p=0.01, t=0.15, q~=0.03: safe 0.068892, 0.067813, 0.067224 (G=401,801,
  1601; converging like the cell width to about 0.0666); the restricted-mode power iteration
  does NOT close its ratio bracket ([0.0218, 0.0666]) -- the lower ends 0.0218 (p=0.01) and
  0.0025 (p=0.001) I printed earlier in the session are unconverged and must not be quoted.
  Conclusion: at p=0.01 the relaxed value is about 0.067 per site, far above every lower
  bound I have (0.0254): the tilt-state relaxation is useless for deciding small p.
* [r10_blockfield.py] NEW lower bound of mine (Prop. I with the two uniform fields on blocks
  of ANY length L, via a DP over (first, last, magnetisation); identity checked against the
  definition, 18 cases, 6e-16).  u=1: p=0.05: h >= 0.037540 (L=6, t=0.307) = 1.288 x cube;
  p=0.02: h >= 0.029973 (L=7, t=0.256) = 1.029 x cube; p=0.01: 0.025390 (0.871 x cube).
  => "raised" is PROVED for h down to p=0.02 at u=1 (Y: undecided for p<=0.05).
* [large slopes, probes] p=0.3: u=3: safe tilt upper bound at t=0.4: 0.1821 > cube h 0.1728;
  u=4: 0.2436 (q~=0.40) vs cube 0.2392; Markov-label lower bounds 0.1596 / 0.2219 (c*=0 at
  u=4: i.i.d. labels, instance = zero residual).  Neither direction provable at u>=3.
* [r10_11_small_slope.py] small-slope law F*(t) ~ (t(1-t)/2) u^2 V, V = max Lipschitz variance:
  binary symmetric chain n<=5, ALL vertices: V_n = (1/4)Var(m) exactly for p<1/2 (maximiser =
  uniform field), = (1/4)Var(staggered m) for p=0.7; F*_4(t;u)/(u^2 t(1-t)/2) = 1.7168,
  1.7725, 1.7871, 1.7908 (u=0.4,0.2,0.1,0.05; t=0.3) -> V_4 = 1.7920.
  Frustrated chain (nn ferro, nnn antiferro), n=5: V_5 is attained by a MODULATED site-wise
  label (e.g. --+++), V_5 = 1.962 vs zero-wave-vector (1/4)Var(m) = 1.014 (J1=.5,J2=-.5);
  2.390 vs 0.530 (J1=.3,J2=-.8).  => "scales with the k=0 susceptibility" is FALSE in
  general; the right quantity is V (for ferromagnets V = chi).
  Potts q=3, n=2 (763 integer Lipschitz functions, 534 vertices): J>=0: V_2 = Var(N_a) =
  (2/9)(2+2 lam2); J=-1: V_2 = 0.563 > Var(N_a) = 0.326.  Ratio check u->0 at J=0.7:
  0.59698, 0.57909, 0.56839, 0.56267 -> 0.55670.  (n=3 enumeration ran out of memory:
  replaced by LP ascent, see below.)
* [reading THEIR code, after all of the above] `ydp3.py` (conservative tilt recursion):
  nodes mu_k, cells [mu_k - D/2, mu_k + D/2]; feasibility of a grid triple enlarged by
  eps = 1.5 D, justified because theta_+- are 1-Lipschitz in each of (lam, mu+, mu-):
  |d theta| <= D/2 (1 + A' + B') <= 1.5 D  -- CORRECT; stage factors = extremes over the
  cell -- CORRECT (tau(b,+) increasing, tau(b,-) decreasing in lam); KL reward convex ->
  cell ends -- CORRECT; Shannon reward: max of 3 points + 2 D^2 (ample: |f''| <= ~1.3, needed
  slack <= D^2/25; in fact KL(tau||q) is convex in tau(+) and tau(+) monotone, so the max is at
  a cell end and no slack is needed); W <= 0 with minimal transition weights -- CORRECT.
  => their discretisation IS on the safe side (REVIEW, plus my independent implementation
  agrees: my safe values are everywhere slightly BELOW theirs).
  Their cells overhang the tilt range [-u*, u*] by D/2; the reward at the end cell is taken
  at u* + D/2.  That overhang alone is the "margin 1.0, 1.4, 1.9e-4" of 5.4(c): with
  k'_+(u*) = 0.215, k'_-(u*) = 0.363 (p=0.3), D/2 = 4.8e-4: average excess 1.4e-4.  With
  cells inside the range the safe value IS E_F (mine: E_F + 3e-11 at p=0.3, + 1e-11 at 0.4).
  Their "grid-restricted" Renyi value 0.04435 (p=0.3,t=0.43) is the -ln(min ratio) end of a
  bracket that does not close ([0.0439975, 0.0443495] at G=1601 in their own output
  y15_dp3_controls.txt) -- it is not a certified lower bound of the relaxed value; my
  midpoint-restricted grid gives a closed bracket 0.044357, so the statement "finer grids
  would lower the h-bound to about 0.0446" stands.
  `y07_block_labels.py`: M_L from `renyi_F(..., itmax=min(40000, 300+3e8/size))` = 400
  iterations at L=14: not converged; this is why their Prop. I numbers are 1-3e-5 below mine.
  Valid either way (any M_L).  a-bounds use t <= 0.99 and L <= 10.
  `y08_validate.py` (c): tests the LEVEL function (ln t_y - ln t_x - d <= 0), as I guessed.
* Prior art searches (reading levels in the report): Rached-Alajaji-Campbell 2001 (Renyi
  divergence rate of Markov sources, Perron-Frobenius) [search snippet]; Vanneste
  arXiv:0911.2161 (generalised Lyapunov exponents) [search snippet]; Holliday-Goldsmith-Glynn
  2006 (entropies of finite-state channels = top Lyapunov exponents) [search snippet];
  Newman 1980 CMP 74 [search snippet]; Bulinski-Shabanovich 1998 Fundam. Prikl. Mat. 4(2)
  479-492 [metadata only]; Galvin 2003 Israel J. Math. 138 [search snippet].
  The Lipschitz covariance inequality needed for the small-slope law has a 3-line proof for
  binary spins (g +- f increasing with g = sum L_i s_i; association gives Cov(g+f,g-f)>=0),
  so no citation is needed.
* !!! [r10_06_markov_recursion.py 3 4 6 8] LARGE SLOPES: the Markov recursion (Prop. F) with
  L=3 (96 vertices, duality brackets 1e-12) gives upper bounds BELOW the cube:
    u=4: cube h=0.239250, a=0.603052.  h <= 0.234594 (p=0.2; x0.981), 0.227585 (p=0.1; x0.951);
         a <= 0.591982 (p=0.3; x0.982), 0.559986 (p=0.2), 0.509682 (p=0.1).
    u=3: cube h=0.172831, a=0.502282.  a <= 0.495806 (p=0.3; x0.987), 0.467509 (p=0.2),
         0.432593 (p=0.1);  h: ratios 1.018..1.046 (undecided with L=3).
    u=6: a <= 0.674273 (p=0.3, L=2) < cube 0.675836.
  => "a nearest-neighbour interaction raises all three exponents" is FALSE as a general
  statement: at slopes u >= 3 it LOWERS the capacity exponent a (p <= 0.3) and at u=4 also h
  (p <= 0.2).  E stays raised for every u (E_F > ln cosh(u/2)).  Y had said: "u >= 2
  undecided for h" and nothing about a at other slopes.  To do: rigorous sup over t
  (interval rule), a finer (p,u) map, re-run with THEIR functions as a cross-check.
  Heuristic that predicted it (written in these notes before the computation): at large u
  the labels pin configurations; the leak of a pinned site is e^{-u} r, r in
  {e^{2K},1,e^{-2K}} (prob 1/4,1/2,1/4 for uniform label laws), so
  F ~ (1-t) ln 2 - e^{-tu} cosh^2(Kt) against the cube's (1-t) ln 2 - e^{-tu}.
* [r10_07d p=0.4, 0.2, 0.1] own safe tilt recursion (G=801):
  p=0.4: E <= 0.169127 (= E_F + 1e-11); a <= 0.120996 (Y 0.121446); h <= 0.036028 (Y 0.036163).
  p=0.2: E <= 0.310766 (= E_F + 5e-11); a <= 0.161310 (Y 0.160745; my q~ scan stopped at p);
         h <= 0.054121 (Y 0.054353).
  p=0.1: E <= 0.428235 with Q=pi (Y: 0.4307 at G=801), but 0.410675 with the reference
         Markov(q~=0.11) -- BELOW Y's best upper end 0.417991 (their DP, L=3): a reference
         chain other than pi improves the threshold bound at strong coupling (Y used Q=pi only).
         h <= 0.071208 and a <= 0.201298: WEAKER than Y's 0.066765 / 0.192774 because my q~
         ranges ended at 1.02p / 1.0p while the optimum is at 1.1-1.2p.  To rerun with a wider
         range.
* r10_10_map.py crashed on formatting a None (Prop. H rejected by the N=48/96 check); fixed.
* [r10_14_rerun_their_functions.py, 593 s] RERUN of THEIR functions (ylib: lip_vertices,
  bsc_block_law_cond, ustar, capacity, h_bracket = their certified bracket over all t) at
  slopes they did not report: identical numbers to mine.  u=3: a <= 0.495806 (p=0.3, x0.9871),
  0.467509 (p=0.2), 0.432593 (p=0.1); u=4: a <= 0.591982 (x0.9816), 0.559986, 0.509682;
  h certified by their interval rule: p=0.1,u=4: h in [0.227585, 0.233073] < cube 0.239250
  (x0.9742); p=0.2,u=4: upper 0.240768 with THEIR coarse t-grid (x1.006), 0.2346 at t*.
  => the reversal at large slopes is reproduced with the theory division's own code.
* [r10_11_small_slope.py, 65 s, final] helix-coil (Zimm-Bragg) chain n=5, all 395094
  vertices: V_5 = Var(N_helix) exactly, maximiser = uniform field, for (s,sigma) =
  (1,1e-2), (1,1e-3), (1.3,1e-3), (0.7,1e-2); bulk factor (1+r)/(1-r) = 1/sqrt(sigma) at s=1.
  Potts q=3 by LP ascent (local maxima, 40 starts; a lower estimate of V_n), n=3,4:
  ferro J=0.7, 1.5: best = Var(N_a) = product value x finite-n structure-factor sum
  (1.3793, 1.9086 at n=3; 1.4507, 2.1718 at n=4; bulk 1.676, 3.321);
  antiferro J=-1: best 0.9356 (n=3), 1.3166 (n=4) against Var(N_a) = 0.461, 0.588.
* [coordinator, mid-run] "converge now": finalise the report; no new explorations; verdict
  table per statement; the wrong sentence of 7.2; small-slope law with labels and scripts;
  list of what was not checked; one re-run command per script; every cited log from a run
  that reached its last line.  May connect (without re-deriving) to addendum A17.8 (C_i,
  Var <= 1/4 sum C_i^2; CCKR math/0503483 ineq. (10); Kontorovich-Ramanan 2008 Thm 1.2) and
  A17.6 sharp form.  Read A17.6 and A17.8 statements (our own division's file) for the wording.
* Housekeeping for "complete logs": set aside r10_13_reversal.log (timed out at p=0.05),
  r10_10_map.log (crashed on a format), r10_07c log (timed out at G=3201) under
  *_superseded.log names; reruns launched: r10_13 in two chunks (a: p=0.45,0.4,0.3;
  b: p=0.2,0.1), r10_07a (now prints all three modes with brackets), r10_07b (restricted_mid,
  as in the first run), r10_09b (to a log), r10_10_map (grid reduced to what is cited:
  p in {0.3,0.05,0.02,0.01}, u in Y's slope list), r10_07c (G <= 1601).  r10_tilt.py now has
  three modes: safe, restricted (nodes incl. end points), restricted_mid (cell midpoints).
* [r10_15_large_slope_checks.py, 103 s] finite chains, all vertices: (1) block form of
  Prop. F (two blocks of 2) against exact a_4 and F*_4(0.3), F*_4(0.5) at u=1,3,4,6, p=0.3,0.1:
  24 comparisons, bound >= exact always (smallest margin 0.027).  (2) exact increments
  a_n - a_{n-1} (n=2,3,4): u=3,p=0.3: 0.4582 0.4623 0.4623 (cube 0.5023); u=4,p=0.3: 0.5704
  0.5709 0.5709 (cube 0.6031); F*_n(t_cube) increments at u=4,p=0.3: 0.2226 0.2244 0.2244
  (cube h 0.2392).  Indicative [N]: h is probably lowered at (0.3, 4) as well (proved only
  for p<=0.2).
* [r10_07e p=0.1 u=1; r10_07f] wider reference range at p=0.1: h <= 0.062762 (Y 0.066765),
  a <= 0.172043 at q~=0.16 (Y 0.192774 at the edge 1.1p of their scan), E <= 0.403619
  (G=1601, q~=0.115) (Y 0.417991).  For q~ >= 0.12 the safe threshold bound equals
  E_F + KL-rate(q~||p) to 7e-11 (relaxation tight, optimum = uniform field); for q~ < 0.117
  another relaxed policy wins.  p=0.2: a <= 0.160048 (q~=0.21) (Y 0.160745).
* [r10_07g_capacity_slopes.py 0.3, 239 s] safe tilt capacity bound, p=0.3, u=1..3: ratios to
  the cube 1.26, 1.17, 1.10, 1.04, 1.011, 1.004 -- never below 1 (as it must be: with ANY
  Markov reference the period-4 label ++-- gives at least the cube's value at large u).
* [r10_05b_propI_other_slopes.py, 5 s] Prop. I (<=2 walls) at u=1.5, 2: h >= 0.064578 /
  0.069632 / 0.070865 (u=1.5; p=0.4,0.3,0.2; x1.067, 1.151, 1.171) and 0.098573 / 0.099943 /
  0.097726 (u=2; x1.013, 1.027, 1.005): h RAISED at u=2 for p=0.4,0.3,0.2.
  a >= 0.2147/0.2148/0.2022 (u=1.5; cube 0.2181) and 0.3069/0.2978/0.2712 (u=2; cube 0.3278):
  below the cube -> a undecided at u=1.5, 2 for these p.
* [final housekeeping] Reruns complete so far: r10_07a (three modes; restricted with end
  points: bracket [0.043998, 0.044349] at G=1601 does not close, exactly as in Y's own output;
  restricted_mid closes at 0.044357; threshold: safe = restricted = E_F at every G),
  r10_07b (144 cases, safe >= exact), r10_09b (example logged), r10_10_map (121 s; slope
  table at p=0.3 identical to Y except u=0.05: 2.260 vs 2.271; small p: block fields 0.037540
  at p=0.05, 0.029973 at p=0.02; at p=0.01 the block-field values with L>2 are REJECTED by my
  N=48/96 operator check -> the earlier inline number 0.025390 is withdrawn, best checked
  lower bound there is 0.023164 from Markov labels), r10_07c (252 s; safe 0.068892,
  0.067813, 0.067224), r10_13 chunk a (570 s; identical to the earlier partial run),
  r10_05 check (27 cases, 1.2e-15), r10_16_blockfield_check (36 cases vs definition 8e-16;
  Lambda_blk vs exact increments 1e-9 at the decisive (p,L,t)).  r10_13 chunk b running.
* Report written: docs/science/workstreams/R10_REPORT.md (verdict table of 38 rows; one
  major finding M1 = slope-dependence of the direction, with proved reversal cells; twelve
  minor findings; small-slope law R10.1/R10.2 with status table; connection to A17.8/A17.6;
  re-run table; lists of what was not settled / not checked).
* Things done only inline (no log, NOT cited in the report): the first Arimoto speed test;
  a probe of the tilt upper bound for h at u=3,4 (above the cube); a probe of the tilt bound
  at p=0.01, 0.001 (safe values far above every lower bound; restricted lower ends
  unconverged); the first block-field table (superseded by r10_10_map and r10_16).
* [end] r10_13 chunk b complete (862 s); the thirteen proved-lowered cells quoted in the
  report (M1 table) verified digit by digit against r10_13_reversal_a/b.log by a script.
  No placeholder left in the report; every cited log ends with its last line.  No background
  job of mine is running.  Write scope respected: this directory and
  docs/science/workstreams/R10_REPORT.md only; no state-changing git command; their export
  untouched (a scratch copy of experiments/workstreams/Y/code was made in the session
  scratchpad for r10_14).
