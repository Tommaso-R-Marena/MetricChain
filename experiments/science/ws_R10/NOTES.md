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
