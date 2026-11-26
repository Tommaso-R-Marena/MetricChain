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
