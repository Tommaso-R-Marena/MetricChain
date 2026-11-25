# Workstream X — working notes (updated after every step)

Question: is a worst-case (set-membership) envelope class the right representation of what is
not known about a molecular energy residual; if not, what replaces it and with which guarantees.

Labels: [V] machine-checked, [P] paper proof here, [K] known+cited (reading level), [N] numerics
only, [C] conjecture, [H] heuristic.

## Log

### 2026-11-25 17:41 UTC — start
* Read COMMON.md, X_brief.md, README.md (theory status, items (i)-(x)).
* Created this directory.  Nothing else written yet.
* Next: THEORY_REPORT §10 table, §11.2–11.4, 11.7, 11.12, 11.14, 11.17, §12; DEAD_ENDS D28, D32,
  D40, D42; docs/workstreams/README.md.

### 17:55 — reading done; plan
Read: THEORY_REPORT §10 (G1–G27 + the table "what each kind of knowledge costs" + three readings),
§11.1–11.5, §11.7, §11.10 (Thm 11.22/11.23), §11.12–11.14, §11.17, §12; DEAD_ENDS D28, D32, D40–D42;
docs/workstreams/README.md.  Sibling science briefs: A1/A2 (prior art of their clusters), K, M, P
(physical applicability of envelope classes), R1, R2 — P is the nearest neighbour; I do not duplicate
its question (do real residuals lie in the classes) but ask which *kind* of class/model.

Key observations while reading (to be tested numerically before any proof):
* O1.  Brief's product covariance k = s^2 rho^{d_H} on {0,1}^n has Walsh eigenvalues
  s^2 a^{n-|S|} b^{|S|}, a=(1+rho)/2, b=(1-rho)/2: the variance carried by interaction order m is
  Binomial(n,(1-rho)/2).  Fixed rho<1 => typical order is extensive.  Bounded order needs
  rho = 1-2*lam/n (Poisson(lam) orders).  IBC "product weights" gamma_i <-> rho_i=(1-gamma_i)/(1+gamma_i).
* O2.  GP credible band = z_delta * P_A(x); RKHS-ball worst-case band = B * P_A(x), same power
  function P_A.  So "Bayes vs worst case" is NOT the operative distinction; "ellipsoid (linear
  information) vs Lipschitz polytope (tropical information)" is.  Theory division's box-linear class is
  the l^infty sibling (l^1 span distance instead of power function).
* O3.  For linear designs A = C^perp (C a binary linear code) the posterior is explicit coset by
  coset (aliasing): P_A(x)^2 = sum_cosets 4pq/(p+q) <= 4 * (non-leader spectral mass).  With dual
  BCH codes: N <= (n+1)^m points give sup_x P_A^2 <= 4 tau_m^2 (tau_m^2 = variance beyond order m).
  Lower bound for ANY N points: avg_x P_A^2 >= sum of all but the N largest eigenvalues.
* O4.  Deterministic lower bound for min at the zero instance over the ball: error >= (B/2) max_x P_A(x).
* O5.  ln Z over a ball: exact consistent interval by Gibbs variational principle + Sion:
  U_A = sup_pi [beta B_A sqrt(pi^T K_A pi) - KL(pi||pi_hat)], L_A = inf_pi [beta B_A sqrt(..) + KL].
* O6.  Bayesian: dimension-free credible interval for ln Z from Jensen + annealed bound + Gaussian
  concentration (no union bound); min needs sqrt(2 ln|X|) (REM-like tails) — but value problems
  self-average: REM tail shows "polynomial iff spectrum decays" is FALSE for the VALUE of ln Z at
  high temperature in the Bayesian setting (prior alone predicts it).  To test.
* O7.  "No free hedging": Thm 11.22/11.23 are instance-wise, so an algorithm that is cheap on a nice
  subclass cannot be correct on the first-order class — the alternative assumption cannot be verified
  with polynomially many evaluations.
* O8.  Direction 3: sharpness certificate = MAP of f - c d_H(x*,.) (unary modification).  LP tight for
  trees and binary submodular (closed under unary changes).  Define LP-funnel slope c_LP <= tau.

Plan of numerics (each before the corresponding proof):
 N1 coset formula for P_A vs direct GP posterior;  N2 eigenvalue-tail lower bound;
 N3 ball certificate + ln Z variational interval vs brute force;  N4 Bayesian coverage;
 N5 same toy problem, cost vs n: first-order envelope (covering) vs ball vs GP;
 N6 misspecification: wrong spectrum, dips, conformal recalibration;
 N7 exponent for product covariance, fixed rho vs rho=1-2lam/n;  N8 REM tail (refutation of "iff");
 N9 LP-funnel slope vs integer funnel slope on random pairwise instances.

### 18:20 — N1/N2 done (n1_coset_formula.py -> n1_coset_formula.json)
* cube.py: FWHT, spectra (isotropic, product), linear designs (span, syndromes), BCH parity checks,
  dense posterior, coset ("aliasing") posterior.
* [N] 300 random (spectrum, linear design) pairs, n=3..8: coset posterior == dense posterior
  (max rel. diff 2e-7, all in the heavy-tailed kind: pinv truncation); structural check independent
  of conditioning (K_A vanishes on A; K-K_A in span K(.,a)) to 2.7e-14.  => formula CONFIRMED.
* [N] sup_x Var <= 4*NL in all trials; largest observed sup/NL = 3.82 (so 4 is essentially sharp).
* [N] avg_x Var >= eigenvalue tail T(N) in all trials (min ratio 1.05).
* [N] BCH designs (n,m) = (7,1),(6,1),(5,1),(15,1),(15,2),(12,2),(10,2),(7,2),(15,3): min distance
  >= 2m+1 verified by brute force; N = 8,8,8,16,256,256,256,64,1024; NL <= tau_m^2 and
  sup Var <= 4 tau_m^2 (observed sup/tau^2 about 1.4-2.0).  Exact order-m priors: Var == 0.
* Decision: Theorem A = two-sided tractability statement for min over Walsh-ellipsoids
  (deterministic), Theorem B = exact consistent interval of ln Z over a ball (variational),
  Theorem C = Bayesian twin (credible intervals, variance sandwich, second-moment certificate),
  Corollary = no free hedging, Theorem D = LP-funnel slope (direction 3).
