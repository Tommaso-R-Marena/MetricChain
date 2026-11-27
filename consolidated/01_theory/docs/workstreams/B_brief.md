# Workstream B — beyond product landscapes: chain-structured known parts
Directory: <session scratch>/ws/B/

## Why
Both referees noted that all exponent theorems are for independent sites, "otherwise the
exponent theorems do not touch the application" (chain molecules have nearest-neighbour and
longer-range couplings in the known part `f`).  Theory report §12 item 1(c) states a conjecture.

## Question
Let `f(x) = Σ_i φ_i(x_i) + Σ_i ψ_i(x_i, x_{i+1})` (a chain; start with a homogeneous two-state
"Ising" chain), envelope weighted Hamming with constant `c`, residual zero or additive.
* Zero temperature: what is the exponent of `N_cov` (least number of evaluations certifying the
  minimum)?  Known lower bound: `max_t [p_E(t) − ln(1+(k−1)e^{−tc})]` with `p_E` the pressure of
  the gap landscape (transfer matrix) — the "Boltzmann weights" bound, which is *not* optimal in
  general even for independent sites (`DEAD_ENDS.md` D31).  Conjecture: `sup_ν R_ν(δ_ν)` over
  stationary processes.  What is the right dual (Markov weights? matrix-valued weights?) and
  the right primal (covering of Markov types)?  Compute `N_cov` or `N_frac` exactly on small
  chains (ILP/LP) and test.  When does one evaluation suffice (the "sharpness" criterion with
  interactions — the sharp-minimum condition `d(x̂,y) ≤ f(y) − f(x̂)` for all `y` is a pairwise
  minimisation; characterise it for chains)?
* Finite temperature: the soft gap `Λ(y)` is a ratio of two transfer-matrix partition functions.
  Work out the randomised lower bound (packing of slack balls of radius `(Λ(y)+ε)/β`) and the
  upper bound `E_π[e^{Λ}]` for chains: are there pressure-type closed forms?  Is there a
  threshold phenomenon as on the cube?
* Anything structural that interactions change qualitatively (e.g. frustration, long-range
  order at low temperature, domain walls as the cheap excitations that make sites non-sharp).

Deliver precise statements with proofs where you can, exact small-size computations, and a
clear list of what is conjecture.
