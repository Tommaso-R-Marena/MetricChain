# Workstream H — algorithms without a hint on the cube: is adaptivity enough?

Read `COMMON.md` first (it describes the state before cycle 9; the theory report at commit
`59e6761` is current — read §11.10, Theorems 11.22–11.28, and §12 item 2(d)).
Your directory: `<session scratch>/ws/H/` (absolute path given in the launch message).

## Setting
Cube `Q_n = {0,1}^n`, Hamming distance `d`.  Class `L_u`: all `psi : Q_n -> R` with
`|psi(x) - psi(y)| <= u d(x,y)` (`psi = beta g`, `u = beta c`).  Target `ln A(psi)`,
`A = 2^{-n} sum_x e^{-psi(x)}`.  An algorithm queries `psi` at points of its choice (randomised,
adaptive unless stated) and must output a number within `eps/2` of `ln A(psi)` with probability
at least `1 - delta`, **for every** `psi` in the class (no hint, no promise).  Cost = number of
queries; exponent = `lim n^{-1} ln cost` at `eps = n eps1`.  Notation: `h` binary entropy (nats),
`KL(a||b)` binary relative entropy, `p_u = 1/(1+e^u)`, `Lambda1 = ln(2/(1+e^{-u}))`,
threshold `eps1* = ln cosh(u/2) = KL(1/2 || p_u)`.

## What is known (theory report; treat as claims that were refereed)
* With a hint (the algorithm is told a candidate `psi_0` and must be correct on the whole class;
  cost counted at `psi = psi_0`), at the flat instance the exponent is
  `theta_hint(eps1) = KL((Lambda1+eps1)/u || 1/2)` for `0 < eps1 < eps1*` (Theorem 11.25: lower
  bound machine-checked, upper bound by Harper's vertex-isoperimetric theorem).  Above `eps1*` a
  bounded number of uniform samples suffices on every instance.  At additive instances
  `psi = sum_i a_i x_i` no hint is needed (learn the `n+1` coefficients, then verify).
* Without a hint the published bracket was `theta_hint <= exponent <= ln cosh u` (Chebyshev).

## New claims of this cycle (mine, NOT yet refereed — your first task is to try to break them)
Let `theta_na(eps1) = min{ KL(rho||1/2) : KL(rho||p_u) <= eps1 }` (so `theta_na(0+) = KL(p_u||1/2)`,
about `u^2/8`; `theta_hint(0+)` is about `u^2/32`; both vanish at `eps1*` with the same leading
behaviour).
* **N1 (tail lemma).**  For `psi` in `L_u`, `w = e^{-psi}`, any `t > 0`, `D = {w > t}`:
  `w(x) <= t e^{u dist(x, D^c)}` on `D`; hence, if `|D| <= |B(n,r)|` (Hamming ball), by Harper
  `sum_{x in D} (w(x) - t) <= t sum_{j<=r} C(n,j) (e^{u(r+1-j)} - 1)`.
* **N2 (plain Monte Carlo on the whole class).**  `M` uniform samples, `K = 8 ln(1/delta1)`,
  `r` = least radius with `|B(n,r)| >= 2^n K/M`,
  `Gamma_n(r) = sum_{j<=r} C(n,j)(e^{u(r+1-j)}-1) / |B(n,r-1)|`.  Then with probability at least
  `1 - delta1 - delta2`: `-ln(2(1+Gamma_n(r))) <= ln Ahat - ln A <= ln(1/delta2)`.  (Chernoff for
  `min(w, t*)/t*` with `t*` the upper `K/M`-quantile of `w`, N1 for the part above `t*`, Markov
  for the upper tail.)  So the recentred Monte Carlo estimate has exponent `theta_na(eps1)` on the
  whole class.
* **N3 (non-adaptive lower bound).**  At the cone `psi_s = u d(.,s)` the alternative
  `max(psi_s, uR)` (flattened bottom) differs from it exactly on `B(s,R-1)` and lowers `ln A` by
  about `n KL(R/n || p_u)` when `R/n > p_u`.  A non-adaptive algorithm (query set drawn before any
  answer) must hit `B(s,R-1)` with probability `>= 1-2 delta` for every `s`; averaging over `s`:
  `E|Q| >= (1-2 delta) 2^n/|B(n,R-1)|`.  Hence **the non-adaptive exponent is exactly
  `theta_na(eps1)`** and plain Monte Carlo is optimal among non-adaptive algorithms.
* **N4.**  The same sample gives a certified bracket
  `A in [Ahat_t/(1+gamma), Ahat_t/(1-gamma) + t (e^{Delta_r} - 1)]` (`Ahat_t` the mean of `min(w,t)`,
  `t` an empirical upper quantile, `Delta_r` the dip effect of Theorem 11.25), which at the flat
  instance is tight at the hinted optimum: no hint is needed there.
Scratch code: `<session scratch>/cycle10/mc_cube.py`, `tail_test.py` (read-only for you).

## The open question (your main task)
**What is the exponent `theta*(eps1)` of adaptive algorithms without a hint?**  We know
`theta_hint <= theta* <= theta_na`.  Adaptivity helps at cones (the slope reveals the centre:
`n+1` queries).  Either
  (U) design an adaptive algorithm with a correctness proof on the whole class and worst-case
      exponent below `theta_na` — ideally `theta_hint` — or
  (L) prove a lower bound above `theta_hint` for all adaptive algorithms (a prior over instances
      on which locating the critical difference set is hard even with slope information).
Partial results are welcome if they are theorems: restricted classes (minima of `m` cones;
functions of the Hamming weight around a hidden centre; monotone functions), two-round
algorithms, a stability version of Harper that turns a near-extremal profile into an
approximate cone, instance-wise bounds, the case `eps = O(1)` or exponentially small accuracy.

My heuristic exploration (not proofs; may be wrong): (i) for hidden structures built from
Hamming balls (cones, mesas with a cone on top, populations of cones, decoys) the cost of
"uniform sampling + following slopes" never exceeded `theta_hint` in my calculations —
critical depth forces width (`deep => wide => visible`), and several small structures that
matter jointly are more visible than one; (ii) junk dips that shadow the cone of a deep centre
reveal the centre by coincidences (majority vote over the junk centres found); (iii) naive
"self-hinting" (sample from the Gibbs measure of the upper McShane envelope of the data and
compare) does not descend — a hint has to be *learned* (optimisation), then verified;
(iv) the detector must be two-sided: lower alternatives of a cone have footprints of uniform
measure `>= 1/2`, upper alternatives (flattened bottoms) are the ones non-adaptive algorithms
cannot see.  I conjecture `theta* = theta_hint`, without a proof.  Try to refute it.

## Also useful
* Exact small cases: for `n <= 4` and values on a grid, is the optimal adaptive strategy
  computable (game tree) for some restricted family?  Any exact evidence on adaptive versus
  non-adaptive cost is valuable.
* Prior art (keep a search log, say what you read): adaption versus non-adaption in
  information-based complexity (Bakhvalov; Gal–Micchelli; Traub–Wasilkowski–Woźniakowski; Novak's
  examples where adaption helps); query complexity of normalising constants (Ge–Lee–Lu 2020;
  Holzmüller–Bach 2025); nested sampling / multilevel splitting with a constrained-sampling
  oracle; Chatterjee–Diaconis 2018 (sample size of importance sampling); stability of Harper's
  theorem (Keevash–Long; Przykucki–Roberts).  Is N2/N3 (Monte Carlo is exactly optimal among
  non-adaptive algorithms on a Lipschitz class of the cube, with the exponent
  `min{KL(rho||1/2): KL(rho||p_u) <= eps1}`) known?

## Deliverable
`REPORT.md` in your directory, organised as in `COMMON.md` rule 5, with every script.  Mark
each statement **proved** (full proof in the report), **numerical**, or **conjecture**.  Use at most
3 GB of memory (`ulimit -v 3000000` before heavy runs) and never more than 2 cores.
