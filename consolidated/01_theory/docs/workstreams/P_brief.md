# Workstream P — chains: envelopes from pair-distance profiles (transport envelopes)

Read `COMMON.md` first (state before cycle 9), then theory report §11.14 (lever-arm law: the
per-torsion weighted-Hamming format cannot certify long chains; `DEAD_ENDS.md` D42) and §12
item 9.  Your directory: `<session scratch>/ws/P/` (absolute path in the launch message).

## The question
§11.14 ended negatively: Cartesian- or RMSD-Lipschitz residuals give torsion-space constants
that grow with the lever arm, and certificates in that format are exponential in the chain
length.  It named three ways out without proving anything.  This workstream develops one:
**residual classes whose uncertainty is correlated through pair-distance statistics.**

## Setting
A fixed-sequence chain with `N` beads, bead types `tau(p)` in a finite alphabet, a finite set
`X_N` of conformations (e.g. rotamer chains: fixed bond length and bond angle, `k` torsion
states per bond; with or without excluded volume).  Squared pair distances `s_pq(x)`.  Known
part `f` arbitrary.  Residual class `P_L` (**pair-additive with unknown radial functions**):

    g(x) = sum_{p<q} phi_{tau(p) tau(q)}(s_pq(x)),   phi_ab L-Lipschitz on [0, S_c], phi_ab(s) = 0 for s >= S_c

(a centre `phi_bar` can be absorbed into `f`).  Let `N^x_ab(s)` = number of pairs of types `(a,b)`
with `s_pq(x) <= s`, `s < S_c` (the cumulative pair-count profile).

## Claims of this cycle (mine, not refereed — first try to break them, numerically and on paper)
* **P1 (linearity).**  `g(x) = - sum_ab int_0^{S_c} phi_ab'(s) N^x_ab(s) ds`: the class is the image of
  the `L^infty` ball of radius `L` under a linear map; the features are the profiles `N^x`.
* **P2 (envelope).**  `sup_{g in P_L} (g(x) - g(y)) = L sum_ab || N^x_ab - N^y_ab ||_{L^1[0,S_c]} =: d_P(x,y)`
  — a transport (Wasserstein-1 type, with free boundary at the cutoff) distance between
  pair-distance distributions; a pseudometric, invariant under rigid motions and mirror
  images; no superposition is needed.
* **P3 (conditioning; correlated uncertainty).**  Given evaluations `g(x_i) = v_i`:
  `sup{ g(y) } = min_lambda [ lambda.v + L sum_ab || N^y_ab - sum_i lambda_i N^{x_i}_ab ||_{L^1} ]`
  (LP duality; the bracket half-width is the `L^1` distance from the profile of `y` to the
  *span* of the evaluated profiles — McShane is the special case `lambda = e_i`).  This is the
  optimal-recovery formula (Smolyak) for this class.
* **P4 (no growth with chain length at extensive accuracy).**  With at most `z` neighbours per
  bead inside the cutoff, profiles divided by `N` are monotone functions bounded by `z/2` on
  `[0,S_c]`; the `L^1` metric entropy of monotone functions gives, for the first-order class
  `{g : g(x) - g(y) <= d_P(x,y)}` (not necessarily pair-additive),
  `ln N_cov(eps1 N) <= C (z L S_c/eps1) ln(z L S_c/eps1)` per type pair, **independent of `N`**;
  for the pair-additive class the span certificate of P3 needs only polynomially many
  evaluations in `z L S_c/eps1` (greedy/reduced-basis argument), again independent of `N`.
  At fixed absolute accuracy the first-order class is exponential in `N`, the span
  certificate polynomial.
* **P5 (what is not covered).**  Pair-specific residuals (every pair its own type) fall back to
  a weighted `l^1` metric on distance matrices and are exponential; so the governing quantity
  is the number of pair types with many pairs, not the chain length.

## Tasks
1. **Verify or refute P1–P3 exactly on small chains** (brute force: all conformations of a
   rotamer chain with `n <= 10` torsions, `k = 3`; discretise `phi` on the finite set of
   occurring squared distances; solve the LPs with `scipy.optimize.linprog`; compare primal
   and dual; check exactness of the bracket).  Use squared distances so that everything is
   rational for a rational bond geometry if you want exact arithmetic.
2. **Measure P4**: packing/covering numbers of the profile set in the normalised `L^1` metric
   for `N` from 8 to as large as you can (exhaustive for small `N`, sampled conformations
   beyond: random, compact, extended, helical families) — does the entropy at fixed relative
   scale saturate with `N`?  Greedy reduced-basis widths `sigma_m`, singular values of the
   profile matrix, and the size `||lambda||_1` of the coefficients (it controls stability under a
   remainder).  Report the dependence on alphabet size (homopolymer, 2 types, 4 types).
3. **Certificates on the same instances in three formats**: weighted torsion-Hamming with valid
   per-torsion constants, the profile envelope `d_P` (covering by slack balls, greedy cover as an
   upper bound, an LP/packing lower bound), and span certificates (P3).  Take a simple known
   part (e.g. a contact energy or a torsional term) and report sizes for the minimum and for
   `ln Z` at several accuracies.  This is the constructive counterpart of D42.
4. **Lower bounds** for the pair-additive class: with `m` evaluations, how large can the
   bracket of `g(y)` remain (Gelfand-width argument)?  When is the span certificate optimal?
5. **Robustness**: `g = pair-additive + r` with `r` a small remainder in a first-order class
   (say `|r(x) - r(y)| <= eta d_0(x,y)`): the bracket becomes
   `lambda.v + L||.||_1 + sup_r [ r(y) - sum_i lambda_i r(x_i) ]`; the last term is a
   Kantorovich–Rubinstein norm of the signed measure `delta_y - sum lambda_i delta_{x_i}` (needs
   `sum lambda_i = 1`).  Work out a usable bound and check it numerically.
6. **Three-body and higher terms** (optional): what replaces the profile for a residual that is
   a sum of unknown Lipschitz functions of triangles?  Does the complexity depend on the body
   order and not on `N`?
7. **Prior art** (search log; say what you read): optimal recovery of linear functionals
   (Smolyak; Micchelli–Rivlin; Gelfand/Kolmogorov widths); metric entropy of monotone functions;
   reduced-basis greedy algorithms in Banach spaces (Binev–Cohen–Dahmen–DeVore–Petrova–
   Wojtaszczyk; DeVore–Petrova–Wojtaszczyk); Wasserstein or `L^1` distances between radial
   distribution functions as structural similarity measures; active learning with
   D-optimality/MaxVol for potentials that are linear in features (extrapolation grade);
   linear-programming contact potentials (Maiorov–Crippen); robust LP with box uncertainty.
   Which of P1–P5 is a known statement in other words?  Be precise and unsentimental.

Scope reminder: synthetic chains and mathematics only; no real biological sequences, no
design or optimisation of sequences.

## Deliverable
`REPORT.md` in your directory, organised as in `COMMON.md` rule 5, with every script and the
exact sizes you ran.  Mark each statement **proved**, **numerical**, or **conjecture**.  Use at
most 3 GB of memory (`ulimit -v 3000000` before heavy runs) and never more than 2 cores.
