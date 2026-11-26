# R15 — running notes (independent review of four statements of the theory division at f7df44f)

Started 2026-11-26.  Object: read-only export `<EXP>` =
`/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_f7df44f/`.
I write only in `experiments/science/ws_R15/` and `docs/science/workstreams/R15_REPORT.md`.

Conventions in these notes: **review** = re-derived by hand; **replication** = my own code from
the statement; **re-run** = their code; **read only**.

## Step 0 — set-up
* Read COMMON.md and R15_brief.md in full.
* Created this directory.  Nothing else done yet.

## Step 1 — reading (all read in full unless said otherwise)
* `<EXP>/docs/collaboration/responses/theory/THY-RES-0012.md` (518 lines) — read in full.
* `<EXP>/docs/THEORY_REPORT.md`: lines 2440–2770 (Thm 11.18d, Prop 11.18e, Prop 11.18f), 9636–10105 (§11.30 setting,
  Thm 11.110, Cor 11.111, "what the hint buys", Prop 11.113, Prop 11.113a, Cor 11.114) — read in full.
  The rest of the report: NOT read.
* `<EXP>/experiments/falsify_conjectures.py`: blocks XI.22 (l. 3844–3994), XI.23 (l. 3997–4174), XXIV.10–XXIV.12
  (l. 11274–11574) — read in full.  Not run yet.
* `<EXP>/proofs/Frontiers/BoxAdditions.lean`, `BoxRatio.lean`, `BoxClass.lean` — read in full;
  `QueryLowerBound.lean` l. 97–298 (QueryAlgorithm, prob_query_ne_ge, expected_queries_ge_packing) read; rest not.
* `<EXP>/experiments/coordinator_checks/random_ball/pairing_check.py` — read in full.
* ours: `docs/collaboration/responses/science/SCI-RES-0016.md` §3 (first reading of (b')(i)); 
  `experiments/science/pi_inference/nested_sampler.py` (docstring, `nested_brackets`, `main`) — read.

### First observations from reading (to be checked by computation below)
* XI.22(d) tests **ln Z**, width `Lw = 3.0`, needle depth 40, k = 2..6, skip probability r ~ U(0.05, 0.9) (so
  delta = r/k), two instances per k: one needle instance (N(0,1) values, one state at -40) and the flat instance
  zeros(k).  It does not test the minimum, nor a width below ln 2, nor ties at narrow width; its last check
  ("arithmetic of the one-site count") is the tautology (k - k*delta) == (1 - delta)*k.
* XI.23 breaks ties of the "most frozen site" by site index (`sorted(range(n), key=lambda i: (p[i], i))`), and `R_i` is
  "i and the sites after i in that order" — not "sites j with p_j >= p_i" (with ties the latter double-charges).
* The Lean theorem `ratio_expected_queries_ge_mixed` does not assume A, B disjoint and does not ask D_j inside a
  macrostate — only that D_j avoids the *other* one; the weights are restricted, so points outside count for nothing.

## Step 2 — Item 1 (Prop. 11.18e(b')(i)) — review + replication  [DONE]
Script `r15_item1_one_site.py`, log `logs/item1_one_site.log` (complete; last lines "ALL CHECKS PASSED", "peak RSS MB 113").

**Review (re-derived).**
1. Lower bound.  Fix g, a state a, an algorithm = a probability law over deterministic adaptive runs.  On the event
   {a not evaluated on g} the run (evaluated states, values, output) is identical on g_D := g - D 1_a for every D.
   Task "finite lower bound l for min": invalid on g_D once D > E0(a)+g(a)-l.  Task "bracket [L,U] for ln Z":
   invalid once D > U + E0(a) + g(a).  So fail(g_D) >= P(a not evaluated on g, threshold < D), which increases to
   P_g(a not evaluated) as D -> infinity PROVIDED the returned lower bound (min) / upper end (ln Z) is finite almost
   surely on that event (or a non-finite return counts as a failure).  Monotone limit (continuity from below); for
   finitely many random bits a maximum over runs does it.  Hence P_g(a not evaluated) <= delta for every a, g, and
   E|Q(g)| = sum_a P_g(a evaluated) >= (1-delta)|X| -- |Q(g)| = number of DISTINCT states evaluated; every g; every
   adaptive randomised algorithm.  The side that matters is the expensive one (lower bound of the minimum, upper end
   of ln Z); an upper bound of the minimum or a lower bound of ln Z costs one evaluation.
2. What is needed of the class: only that g - D 1_a is in the class for arbitrarily large D (downward needles at
   every state) -- e.g. a box class without a floor.  "Closed under adding every function" implies it (and then the
   class is the class of all functions: "one site" is the case n = 1 < m of "m > n"; for m = 1, n = 1 the class is
   closed under constants only and N_ball = 1).
3. "Attained".  (A) trivial mixture: with probability delta evaluate nothing, otherwise everything: count
   (1-delta)|X|, failure <= delta, every width (even zero), every delta in [0,1].  (B) the report's algorithm,
   skip one uniform state w.p. k delta: needs k delta <= 1, and failure = delta * #{a: output after skipping a
   invalid}: MIN with lower bound min_seen - w: invalid iff E(a) < min_seen - w: at most one a for EVERY w >= 0
   (w = 0 included -- the coordinator's "any positive width" can be "any width >= 0").  LNZ with bracket
   [ln Z_seen, ln Z_seen + W]: invalid iff weight fraction p_a > 1 - e^{-W}; at most one a iff W >= ln 2; for
   W < ln 2 the worst case is min(k, ceil(1/(1-e^{-W})) - 1) invalid skips (two equal states: 2 delta; k equal states
   and W < ln(k/(k-1)): k delta).  So the coordinator's first reading (SCI-RES-0016 §3) is RIGHT; add that the trivial
   mixture attains the count with no condition, so "attained" itself is unconditional.
   For k = 2 and ANY deterministic rule for the bracket after a skip with widths <= W < ln 2 some instance has both
   skips invalid (paper argument in the report, §2: the diagonal x = y is covered by two sets of diameter <= W).
4. Last sentence ("saving of (b) ... comes from evaluations outside the ball alone"): follows from the PROOF of (i),
   not from its statement: for a fixed unisolvent set B (e.g. the ball) and a in B let h_a be the function of order
   below m with h_a = 1_a on B; an algorithm that evaluates only in B has the same run on g and g + t h_a if a is not
   evaluated, and min(E0 + g + t h_a) -> -infinity as t -> -infinity (h_a(a) = 1).  So P_g(a not evaluated) <= delta
   for every a in B and E|Q| >= (1-delta) N_ball for every algorithm confined to B.  The second half ("cannot hide
   from a random point, a needle can") is interpretation.

**Replication (own code).**
* PART A: exact (integer / Fraction) number of invalid skips on grids with ties and needles, k = 2, 3, 4
  (49, 343, 2401 instances each task): MIN: worst 1 for w in {0, 1/10, 1, 3}; LNZ: worst = min(k, ceil(1/theta)-1) for
  tau = e^W - 1 in {1/20, 1/3, 1/2, 999/1000} (i.e. 2,2,2,2 for k=2; 3,3,2,2 for k=3; 4,3,2,2 for k=4) and worst 1 for
  tau in {1, 2, 19} (W = ln 2, ln 3, ln 20).  Needle instance: exactly 1 in all cases.
* PART C (new, not asked): LP over ALL randomised adaptive algorithms (sequence form) in a finite ladder model
  (levels 0 > -s > ... > -Ls, task MIN at prescribed width < s): least E|Q(g0)| subject to failure <= delta on every
  instance = k(1 - delta(L+1)/L) EXACTLY, for k = 2,3,4, L = 1,2,3,5 (k=4: L<=3), delta = 0.05, 0.2 (22 LPs, up to 8952
  variables, 256 instances); it tends to (1-delta)k as L grows.  Paper argument for the ladder bound: a run that
  leaves a unevaluated on g0 is the same on the L+1 instances differing at a only and is valid for at most one.
* XI.22(d) of their harness: ln Z, width 3.0 (>= ln 2), needle depth 40; not the minimum; no narrow width.

## Step 3 — Item 3 (Prop. 11.113a, nested sampler) — review + replication  [DONE]
Script `r15_item3_nested.py` (argument = repetitions; run with 2000), log `logs/item3_nested.log` (complete: last lines
"ALL CHECKS PASSED", "seconds 254.7", "peak RSS MB 83.4").  `logs/item3_nested_smoke.log` is a 60-repetition smoke run of
an earlier version of the script (before the sd diagnostic was added) — NOT cited.

**Review (re-derived).**
* (a) ranges and W = beta + rho W_in: one line each from e^{-m-} >= e^{-e-} >= e^{-E} >= e^{-e+} >= e^{-m+}.  OK.
* (b) Z(e+) = Z(m+) + A E_q beta, Z(e-) - Z(e+) = A E_q rho, accepted law q rho / E_q rho = inner sampler.  OK.
  E_q[rho W_in] = E_q rho * E_in W_in.
* (c) three two-sided Hoeffding events at delta/3: 2 exp(-2 n t^2) = delta/3 <=> t = sqrt(ln(6/delta)/(2n)): ln(6/delta) is
  right.  |E rho E W_in - rhobar Wbar| <= |E rho - rhobar| * E W_in + rhobar |E W_in - Wbar| <= t_f + rhobar t.  OK.
  **Sampling scheme**: Hoeffding needs deterministic sample sizes, or sizes determined by something independent of the
  averaged values.  VALID: N_f fixed in advance; the evaluated proposals selected by a rule that looks at the acceptance
  indicators only (all accepted: N ~ Bin(N_f, E rho) random; the first min(N_cap, #accepted); or an independent stream
  of N accepted draws).  Proof: conditionally on the acceptance pattern the proposals are independent and the accepted
  ones have law q_in; so Hoeffding for Wbar holds conditionally with t = t(n), n the (pattern-measurable) number
  evaluated; betabar, rhobar are unconditional means of N_f i.i.d. draws; union bound.  NOT COVERED: "propose until N
  are accepted" (N_f random: the free means are taken at a stopping time that depends on rho(x_i); rhobar is biased
  upward at order 1/N) and any stopping rule that looks at the running bracket.
* **Improvement found (new):** the term 2 t_f can be t_f at the same ln(6/delta).  The error is
  f(mu) + rhobar (mu - Wbar) with f(mu') = (E beta - betabar) + (E rho - rhobar) mu' affine on [0,1], so
  |f(mu)| <= max(|f(0)|, |f(1)|) = max(|E beta - betabar|, |E(beta + rho) - (betabar + rhobar)|) <= t_f when Hoeffding
  is applied to beta and to beta + rho (both in [0,1]) -- i.e. to the two ends Z(e+), Z(e-) of the inner bracket.
  Half-width A(t_f + rhobar t); balance N_f = N/rho^2 instead of 4N/rho^2.
* Coordinator's variant t_f(1 + |Wbar - 1/2| + t) + rhobar t: proof is RIGHT (c = beta + rho/2 in [0,1]; identity
  E_q W = E_q c + E rho (mu - 1/2); three events c-bar, rho-bar, W-bar).  It is between the theory's and the two-end
  form above: thy >= one (when t <= 1/2) >= two always.
* "The term 2 t_f cannot be dropped": TRUE in the sense that some N_f-dependent term is needed (see numbers); the
  coefficient 2 is not needed.
* (d): limit N_f -> infinity is (Z(e-) - Z(e+)) t with t = sqrt(ln(6/delta)/(2N)), NOT "that of Prop. 11.113(c)" which has
  ln(2/delta): larger by sqrt(ln(6/delta)/ln(2/delta)) = 1.139 at delta = 0.05 (1.208 at 0.5, 1.099 at 0.01) unless delta is
  split unevenly (delta_f -> 0).  Minor.  The lower bound of 11.113(d) does apply to the inner box: the algorithm of that
  argument may know everything except the member, in particular the outer models and Z(e-/+); needs the INNER sampler
  fine-grained (sum q_in^2 small against eps^2/sinh^2(Delta_in/2)).  "4/(E rho)^2 proposals per evaluation": arithmetic
  right (2 t_f = rho t).
* Nested vs plain at equal N: nested (thy) narrower iff 2 sqrt(N/N_f) + rhobar < kappa(delta) := sqrt(ln(2/delta)/ln(6/delta))
  = 0.8554 (0.1), 0.8778 (0.05), 0.9101 (0.01), 0.9347 (0.001).  So never if rho >= kappa; else iff N_f > 4N/(kappa - rho)^2
  (>= 5.19 N at delta = 0.05).  If all accepted proposals are evaluated (N = rho N_f): iff rho < (sqrt(1+kappa) - 1)^2 = 0.137.
  With the two-end form: sqrt(N/N_f) + rho < kappa (scheme B: rho < 0.316).

**Replication (own code, synthetic boxes: 4096 or 6561 states, product outer sandwich from equal site shares, envelope
inner sandwich, 7 instances incl. two-level members and members at the floor/ceiling of the inner box).**
* identities by enumeration: 11 identities per instance, largest error 6.7e-16; rho = 0 on every state with fewer than
  m changed sites; ranges OK.
* coverage, 2000 repetitions per configuration, 6 configurations x 7 instances x delta in {0.05, 0.3} = 168 000 runs:
  misses thy 0; one 8 (1 at delta 0.05, 7 at 0.3); two 12 (1 at delta 0.05, 11 at 0.3); plain 0; every configuration far
  inside its allowance.  Largest |error|/half-width: thy 0.961, one 1.116, two 1.153.  sd(err) agrees with the
  delta-method prediction in every configuration (e.g. 0.00399 vs 0.00397).
* without the free term: 24 587 misses, 20 112 of them in the 28 000 runs with N_f = 40, N = 2000 (72 %).
* scheme D (stop at the N-th acceptance): rhobar biased by +10 %..+13 % at N = 1, +1..2.5 % at N = 3, +0.3..0.9 % at N = 10,
  < 0.1 % at N = 100; no miss in 12 000 runs (the bound is conservative) -- but not covered by the proof.
* criterion nested-vs-plain agreed with the simulated mean widths in 32 of 32 configurations.
* OWN ERROR (caught in the smoke run): rho exceeded 1 by one unit in the last place on the all-changed state (env = pen
  there), numpy's binomial rejected it; fixed by clipping after a check that the excess is < 1e-12.  Also instance I2
  was first built with penalties larger than the sites' free-energy costs (outer bracket 10.6 nats); rescaled.

## Step 4 — Item 5 (necessity argument of Prop. 11.113(d)) — review + replication  [DONE]
Script `r15_item5_necessity.py`, log `logs/item5_necessity.log` (complete: "ALL CHECKS PASSED", "peak RSS MB 97.4").

**Table recomputed (delta = 0.05):** Pinsker 5.71, 56.90, 88.97, 180.67, 384.00 (theirs 5.7, 57, 89, 181, 384);
N_TV 20, 189, 289, 575, 1209 (identical); N_KL 68, 528, 815, 1634, 3455 (identical; the grid of 399 means is fine:
a grid of 19 999 gives the same integers).  N_KL/closed form 1.007..1.033; N_TV/Pinsker <= 3.502; N_KL/N_TV <= 3.40.
Plug-in exact failure: <= 0.00718 on the grid i/60 with N_KL (0.00731 on i/600 — the science division's 0.0073), >= 0.160 with
a quarter.  All their numbers reproduced.

**Review.**
(i) E_D in the box for every D: yes.  q(D): mean w, variance w(1-w) sum q^2 <= w(1-w) max q (exact, checked by enumeration)
    -> "fine-grained" alone suffices (Chebyshev).  Quantitatively the fluctuation of ln Z is sd(q(D))/(c+w), small against
    eps iff sum q^2 << eps^2/sinh^2(Delta/2): the sampler must have many more effective states than the count itself.
(ii) fresh bits: under the prior the indicators are i.i.d. over states; an evaluation at a new state reveals exactly its
    indicator (nothing if m-(x) = m+(x)); the next state is chosen from past bits and private randomness.  So the
    transcript is a kernel applied to Bern(w)^N.  Checked by exact enumeration: 80 random adaptive rules on 5..8 states,
    3..5 evaluations, deviation 1.1e-16.  Knowing m-/+ and q changes nothing.
(iii) reduction: c + w' = e^{2 eps}(c + w) exactly; with q(D) = w + o(1) the two truths are 2 eps + o(1) apart; "within eps"
    is a closed condition, so strictly one takes w' a little larger (c + w' = e^{2 eps + 3 eta}(c + w)) and lets eta -> 0:
    TV >= 1 - 2 delta - o(1).  Fine in the limit.
(iv) Pinsker TV <= sqrt(KL/2), KL additive over the N bits: N >= 2(1-2 delta)^2/KL.  Either direction of KL is allowed
    (TV symmetric); KL(w||w') is the smaller one in rows 2-5, the larger in row 1 (5.71 vs 6.77).  w* = c/(1+2c) maximises
    w(1-w)/(c+w)^2 = sinh^2(Delta/2): confirmed.  w' <= 1 needs eps <= (1/2) ln((e^Delta+1)/2) at w* (true in all five rows).
    The "~" needs eps << (1 - e^{-Delta})/4: in row 1 (eps = 0.01 against 0.0147) exact Pinsker is 0.77 of the formula;
    rows 2-5: 0.99..1.05.
(v) expected number: K = 4/(1-2 delta) gives (1-2 delta)^3/(8 KL): right; K = 6/(1-2 delta) gives 4(1-2 delta)^3/(27 KL),
    18.5 % larger.
Extra: Pinsker's bound does not grow with ln(1/delta) (saturates at 2/KL); Bretagnolle–Huber (1 - TV >= exp(-KL)/2,
[K, from memory]) gives N >= ln(1/(4 delta))/KL, and N_TV does grow: at (1, 0.05): delta = 0.05/0.01/0.001:
Pinsker 89/105/109, BH 88/177/303, N_TV 289/578/1021, N_KL 815/1170/1678.

CORRECTION to Step 3 above: the factor sqrt(ln(6/delta)/ln(2/delta)) is 1.139 at delta = 0.05 and 1.099 at 0.01 (right), but at
delta = 0.5 it is 1.339, not 1.208 as I wrote.  (Own arithmetic slip, in the notes only.)

## Step 5 — Item 2 (Prop. 11.18f) — review + replication  [DONE]
Script `r15_item2_allocation.py`, log `logs/item2_allocation.log` (complete: "ALL CHECKS PASSED", "seconds 128.2",
"peak RSS MB 64.1").  `logs/item2_allocation_try1.log` is a first run of an earlier version in which two of MY checks
failed for reasons of mine (an optimiser tolerance; a first-order check with a too large scale) — NOT cited.

**Numbers recomputed** (64 changed sets, exact): example 1 (p = .01 x4, .3 x2; c = 0.1): equal sites (0.24010, 0.18911);
most frozen site (0.02977, 0.01441); equal pairs (0.01647, 0.01423); envelope (0.00042, 0.00037).  Example 2
(p = .05, c = .5): equal sites (1.16710, 0.24841); vertex (2.98716, 0.15910); [not quoted by them:] equal pairs
(0.04776, 0.01694); envelope (0.00253, 0.00092).  All six quoted pairs agree to the digits printed; ratios 8.07 and 13.12.
Extra: in example 1 the minimum of U over ALL level-1 allocations is 0.02587 (equal split among the four TIED frozen
sites; L = 0.01577), 13 % below the vertex with ties broken by index (0.02977).

**Review.**
(a) cost number sum_S P(S)(e^{pen(S)} - 1): pen depends on S only.  Product formula for independent sites/site penalties.
    Mean penalty: E pen_k = sum_K g_K P(K in S); for independent sites with common p: = p^k sum_K g_K = p^k Gamma EXACTLY
    for every 0 <= k <= m and arbitrary constants (through the counting form: E C(Bin(m,p), k) = C(m,k) p^k).  Needs only
    P(K in S) = p^k for every k-subset.  OK.
(b) U = log-sum-exp of linear functions: convex; L concave; gradients = tilted probabilities.  KKT on the product of
    simplices: lam minimises U iff for every T with c_T > 0 the support of lam[T] is inside
    argmin_K P+_lam(K in S), THE TILTED LAW BEING THAT OF lam ITSELF (a fixed-point condition; ties allowed; not a
    recipe).  The iff is right.  Exchangeable instance: equal shares satisfy it.
    L: minimum at a vertex (concave on a polytope).  NOT every vertex is a local minimum: a vertex is a strict local
    minimum iff every constant sits on the k-subset of its T that is STRICTLY least often changed under P-_v (the
    ceiling-tilted law of the vertex itself).  Counted on n = 5, triples (59049 vertices): 1, 60, 60, 16, 17, 46, 42,
    1, 17, 4 strict local minima in ten instances.  The best vertex is always an ORDERING vertex ("every constant to
    the first k-subset of its T in one linear order of the k-subsets") — proof: L depends on lam through the charges
    g only, the set of achievable charges is the base polytope of the coverage polymatroid r(R) = sum of c_T over the T
    that meet R, its vertices are the ordering vertices (Edmonds), a concave function is least at a vertex.  10 of 10
    by exhaustive enumeration.  Without search?  In general no: with constants in {0, C}, C large, independent sites,
    L(v) -> sum over charged sites of -ln(1 - p_i): a minimum-weight hitting set (vertex cover for m = 2).  With
    independent sites and equal constants on all m-subsets YES: the frozen-first order is the global minimiser
    (rearrangement: all ordering vertices have the same charge profile, l_j - l_i is nondecreasing when p_j >= p_i);
    200 of 200 random instances.  With random constants greedy was the best vertex in 6 of 10, a strict local minimum in 8.
(c) first order: both ends -> sum lam P(K in S) (checked at scale 1e-5).  gamma_i = Gamma(R_i) - Gamma(R_i \ {i}) is the
    "most frozen site" allocation exactly IF the sites are linearly ordered (ties broken by the order) and R_i = {i and
    the sites after i}.  If R_i is read as "{j : p_j >= p_i}" and there are ties, tied sites are each charged the
    constants they share: example 1 gives gamma = (1,1,1,1,0,0), sum 4.0 against Gamma = 2.0, (U, L) = (0.068, 0.025)
    instead of (0.030, 0.014) — a valid cover, not an allocation.  With ties "its least probable sub-pattern" is not
    unique: for U the tied sites should share (0.0259 < 0.0298), for L one of them should take all.

**The coordinator's question (constants not small).**  Independent sites, level 1, f_i = ln((1-p_i)/p_i):
    U = sum_i [sp(gamma_i - f_i) - sp(-f_i)],  L = sum_i [sp(-f_i) - sp(-f_i - gamma_i)]   (checked).
  site-wise: max(p_i gamma_i, gamma_i - ln(1/p_i)) <= u_i <= p_i (e^{gamma_i} - 1);   l_i <= min(p_i gamma_i, -ln(1 - p_i)).
  * Floor end U (upper end of ln Z; "the floor's measure moves"): the vertex "most frozen site" minimises U iff in every
    T the charged site i has f_i - gamma_i >= f_j - gamma_j for the other j in T (KKT; checked: no violation of the
    iff in 595 random instances).  The minimiser equalises f - gamma among the sites that share constants (seen:
    graded family at scale 0.3: f - gamma = 0.12 at all eight sites).  First-order comparisons: (i) if at the greedy
    vertex each charged site is changed under the floor measure no more often than the average site of its T, then
    U(greedy) <= U(equal); (ii) if sum_T c_T [p+_eq(i(T)) - mean_{j in T} p+_eq(j)] >= 0 then U(greedy) >= U(equal)
    (homogeneous: equality in the bracket, so always).  No bound of U(greedy) by a multiple of U(equal): one pair with
    p_1 ~ p_2 = p, c = 2 ln(1/p): U(greedy) ~ ln(1/p), U(equal) = 2 ln(2 - p).
    Numbers: 4 frozen + 4 mobile, triples, c = 0.1: U equal 1.10, greedy 0.26, minimum 0.23; c = 0.3: 4.87, 3.19, 1.98;
    c = 1: 33.1, 36.1, 32.9.  Nearly homogeneous (p ~ 0.05): at U(equal) = 0.2: greedy 0.28 (n = 6), 0.23 (12), 0.21 (30);
    at U(equal) = 1: 2.49, 1.78, 1.27.  Random search: U(greedy)/U(equal) up to 2.5, difference up to 10 nats.
  * Ceiling end L: for ANY law, level and allocation, L(lam) <= C(m,k) L(equal) (pen_lam <= C(m,k) pen_equal pointwise,
    then Jensen).  Sharp asymptotically for m = 2: star of d pairs around a slightly more mobile centre: ratio 1.04
    (d = 4), 1.18 (d = 40), 1.895 (d = 1000), 1.984 (d = 1e5).  In 595 random instances L(greedy) > L(equal) never
    occurred.  (iii) if in every T the most frozen site also has the largest f + gamma^eq, then L(greedy) <= L(equal).
  So: the rule can hurt the FLOOR end (which the theory report calls the upper end U) without bound; it cannot hurt the
  ceiling end L by more than the factor m.  The brief says "lower end L" but describes the floor mechanism; both answered.

## Step 6 — Item 4 (Lean statement against Corollary 11.114(c), (d)) — reading only  [DONE]
* Import chain of `BoxAdditions.lean`: Mathlib, BoxRatio -> BoxClass -> QueryLowerBound -> {EnvelopeDuality,
  CertificationGeometry, CertificateNotions, CertificateComplexity, ThermalRobustness} -> ...  `diff` against our tree:
  QueryLowerBound and its five imports are IDENTICAL in our tree; **BoxClass.lean, BoxRatio.lean, BoxAdditions.lean are
  ABSENT from our tree**.  The brief's condition for compiling ("every import of the file exists unchanged in our tree")
  is therefore not met: NOTHING COMPILED.  The theorem was read, together with every lemma its proof term names.
* Statement read: hypotheses hw (w >= 0), ha/hwa, hb/hwb (a point of positive weight in each macrostate), alg/P/hP/hP1 (a
  finite mixture of abstract QueryAlgorithms), hcorr (within eps/2 of logRatio with probability >= 1 - delta on every
  member of the box), hr (r in the box), hdisj (pairwise disjoint D j), hD (each D j of one of four kinds: avoids B /
  avoids A, dips / bumps heavier than (e^eps - 1) Z_M(r) / (1 - e^{-eps}) Z_M(r), weights restricted to M).
  Conclusion: (1 - 2 delta) * card <= expected number of queries ON r.  No disjointness of A, B; D j need not lie in M.
* Where each hypothesis is used (proof term): hD -> rcases into four cases, alternatives dipAlt / bumpAlt; hr ->
  dipAlt_mem / bumpAlt_mem; hw, ha, hwa, hb, hwb + the "avoids" part + the weight part of hD -> logRatio_dipAlt_gt,
  logRatio_dipAlt_lt, logRatio_bumpAlt_lt, logRatio_bumpAlt_gt (the avoided macrostate's weight is unchanged:
  Zw_restr_*_of_disjoint); hdisj -> capacity 1 (each point differs from r in at most one alternative); hcorr, hP, hP1
  -> expected_queries_ge_packing with unit weights.  Every hypothesis is used; eps, delta carry no sign hypotheses
  (degenerate cases are vacuous or trivial).
* (c) against the theorem: faithful.  The sentence leaves out "on r" and "in expectation" (Theorem 11.110(d) has
  both); "randomised algorithm" = finite mixture, as in the whole library; the Lean statement is slightly more general
  (sets need only avoid the other macrostate; A, B need not be disjoint).  Nothing more is claimed than proved.
* (d): with a_M = W_M(lo)/W_M - 1, b_M = 1 - W_M(hi)/W_M.  Lower: greedy packings inside M give k_M >=
  max(floor(a_M/(2(e^eps - 1))), floor(b_M/(2(1 - e^{-eps})))) when no single state of M is heavy; sets in A and in B are
  disjoint, so the theorem gives the SUM k_A + k_B (their own example "(1 - 2 delta) 10, 40, 200" is 5+5, 20+20,
  100+100); inside one macrostate it gives max(dips, bumps), not their sum.  Upper: (b) gives
  N <= ln(1/delta) max(1, 4 max_M max(a_M/(e^{eps/2} - 1), b_M/(1 - e^{-eps/2}))) + 1 and needs U_M, V_M > 0 in BOTH
  macrostates (no one-sided ratio lemma in the Lean files).  For eps <= 1:
  (1 - 2 delta)(max_M (a_M + b_M)/(6.9 eps) - 2) <= cost <= 10.7 ln(1/delta) max_M (a_M + b_M)/eps + 1.  So the display with
  max is right as an order statement (sum and max differ by at most 2); it is a proof for eps <~ 1, no heavy single
  state, and U_M, V_M > 0.

## Step 7 — Item 6 (outline of the conjecture (b')(ii)) — reading + computation  [DONE]
Script `r15_item6_reflection.py`, log `logs/item6_reflection.log` (complete: "ALL CHECKS PASSED", "peak RSS MB 39.5").
* Fibre picture (mine): the instances with a given transcript are beta(t) = beta + t nu; beta_i(t) = nu_i (t - t_i),
  t_i = -beta_i/nu_i the zero crossing of coordinate i.  k = argmin |beta_i/nu_i| is the NEAREST crossing and the
  pairing is the reflection t -> 2 t_k - t.  nu.x*(t) = -sum_i |nu_i| sign(t - t_i) is strictly DECREASING in t, so S
  holds on at most ONE interval between consecutive crossings, and a point and its mirror image are never both in S --
  for every beta, no separation needed (0 of 60 000 exact draws, in all three classes).
* With r_i = |beta_i/nu_i| / |beta_k/nu_k|: signs kept except at k iff no crossing between t and its image: guaranteed
  for r_i > 2; involution guaranteed for r_i > 3.  Exact arithmetic: class r > 3: 41 359 draws, no violation of any
  claim; 2 < r <= 3: 5 743 draws, involution fails in 3 056, signs never; r <= 2: 12 898 draws, signs fail in 6 852.
* Density ratio = prod_{i != k} 1/|1 +- 2/r_i| (Jacobian 1): within e^{+-eps} outside an exceptional set of prior
  probability ~ 1 - (1 - ln(2/eps)/Lam)^d ~ d ln(2/eps)/Lam (d = |supp nu|, Lam = log of the dynamic range): measured for
  n = 7 (mean d = 4): P(|ln ratio| > 0.01) = 0.64, 0.29, 0.098, 0.020, 0.0039 at Lam = 20, 60, 200, 1000, 5000 (prediction
  0.64, 0.29, 0.099, 0.021, 0.0042); P(|ln ratio| > 1) = 0.091 ... 0.0004; beta' leaves the support with probability
  0.017 ... < 1e-5.  So "1 + o(1)" is true as Lam -> infinity, with an exceptional set that shrinks only like 1/Lam.
* P(S) under the prior depends on the signs only: it is the fraction of cube points on the hyperplane nu.x = nu.x^1,
  exactly <= 1/2 (largest over 180 random Q: 0.5000); the needed statement is the conditional one.
* ln Z = -alpha + sum |beta_i| + sum ln(1 + e^{-2|beta_i|}): the passage from ln Z to the minimum is exact and trivial.
* Real gaps: (1) integrating the exceptional set over transcripts (fine: P(S & stop) <= (1+eps) P(S^c & stop) + P(G^c));
  (2) lucky outputs off S (needs the lower cutoff far above width/slope; routine); (3) order above two and larger
  alphabets: there the pairing itself fails, not only its write-up (one site, three states: reflecting the smaller
  coefficient does not move the minimiser, so S is mapped into S).
* NOT done: P(S | transcript) by integration along fibres; any attempt to finish the proof.

## Step 8 — extras and re-run of their harness
* `r15_extras.py`, `logs/extras.log` (complete): E1 unisolvence of balls and Lagrange functions on ten (grid, m) pairs
  (Item 1, last sentence); E2 level 2: best vertex of L is an ordering vertex in 40 of 40; E3 one tied pair, c = 2 ln(1/p):
  U(vertex)/U(equal) = 1.86, 3.35, 4.99, 9.97 at p = 0.1, 0.01, 1e-3, 1e-6.
* RE-RUN (their code, read-only, `python3 -I -B <EXP>/experiments/falsify_conjectures.py --only ...`, default mode, seed
  20261124): XI.22, XI.23, XXIV.11, XXIV.12 all "survived"; `logs/rerun_their_harness.log` (complete: "RERUN COMPLETE").
  Their statistics agree with mine: greedy gains 8.066 / 13.12; worst_fail 0.00718; quarter_fail 0.1602; ratios 1.007..1.033;
  tv_over_bound 3.502; nkl_over_tv 3.4; XXIV.12: 3192 runs, 0 misses, 1268 of 1596 misses without the free term.
  Nothing was written into <EXP> (no __pycache__ there).

## Step 9 — report drafted; cross-check of every number in it against the complete logs; corrections
* Report written to `docs/science/workstreams/R15_REPORT.md`.
* CORRECTION to Step 6: the two-sided bound for the ratio is
  (1 - 2 delta)(max_M (a_M + b_M)/(6.9 eps) - 1) <= cost <= ln(1/delta)(10.7 max_M (a_M + b_M)/eps + 1) + 1
  (I had "- 2" and no "+ ln(1/delta)": k_A + k_B >= k of the larger macrostate, which already is >= (...) - 1; and the
  capped detection probability contributes ln(1/delta) at most).
* Added `r15_item4_packing.py` / `logs/item4_packing.log` (complete: "ALL CHECKS PASSED", "peak RSS MB 35.4"): numerical
  companion to the reading of the Lean theorem — 400 random boxes; 3 790 heavy sets (with points outside both macrostates)
  and 610 with overlapping macrostates all change the log-ratio by more than eps; 800 greedy packings never below the
  floors; the two-sided bound holds; in 186 boxes both macrostates contribute sets.
* Added E4 to `r15_extras.py` (the "second difference" for pairs) and the square-root form of Bretagnolle–Huber to
  `r15_item5_necessity.py`; both re-run, logs complete.
* Web search (one query) for the statement of the Bretagnolle–Huber inequality: the search summary gives
  TV <= sqrt(1 - exp(-KL)) with C. Canonne's note arXiv:2202.07198 and the Wikipedia article among the results; neither
  page was opened => reading level "search snippet".
* No tool declined any action in this workstream.  No Lean was compiled.  Nothing was written outside
  `experiments/science/ws_R15/` and `docs/science/workstreams/R15_REPORT.md`; nothing inside <EXP>.
## Step 10 — last additions
* E5 added to `r15_extras.py` (every allocation covers: 60 random allocations of levels 1..3, all changed sets; least
  pen - envelope = -3.6e-15, i.e. zero up to rounding at the full set) because the report says so; re-run, log complete.
* RE-RUN of their `pairing_check.py` (read-only, `python3 -I -B`, no output-file argument): output IDENTICAL to their
  stored `out_pairing_check.txt` (72 000 draws, 41 786 separated, no violation, "ALL CLAIMS HELD"); 13 s;
  `logs/rerun_their_pairing_check.log` complete.  A first attempt used `/usr/bin/time`, which is not installed (exit
  code 127, nothing run); `logs/_time_pairing.txt` is its stub.  Nothing was written into <EXP>.
* Report re-read in full against the complete logs; corrections applied (see Step 9 and the "Own errors" section).

## FINAL STATE (2026-11-26)
* Report: `docs/science/workstreams/R15_REPORT.md` (sections 0–11 as the brief asks).  Verdict: nothing false in the four
  statements, the necessity argument, or the Lean statement; no critical, no major finding; twelve minor findings with
  replacement texts (m1–m12); six additions (A1–A6); six requests to the theory division (R15-T1 … R15-T6).
* Cited logs (each reached its last line): `logs/item1_one_site.log`, `logs/item2_allocation.log`, `logs/item3_nested.log`,
  `logs/item4_packing.log`, `logs/item5_necessity.log`, `logs/item6_reflection.log`, `logs/extras.log`,
  `logs/rerun_their_harness.log`, `logs/rerun_their_pairing_check.log`.
* Not cited: `logs/item3_nested_smoke.log`, `logs/item2_allocation_try1.log`, `logs/_time_pairing.txt` (stub).
* Resources: largest peak RSS 113 MB (item 1, the LP); longest run 255 s (item 3); never more than two processes.
* No tool declined an action.  No Lean compiled (BoxClass/BoxRatio/BoxAdditions are absent from our tree).  No git command
  that changes state.  Nothing written outside this directory and the report file; nothing inside <EXP>.
* (after FINAL STATE) `r15_item2_allocation.py` re-run once more with counters of how often each test was non-vacuous:
  KKT-iff tested on 246 instances (independent sites, level 1; condition true in 105, false in 141; no violation);
  hypotheses of the three first-order comparisons true in 253, 37, 326 of 595.  Same random stream, same numbers;
  log complete ("ALL CHECKS PASSED", "seconds 86.2", "peak RSS MB 64.3").  Report sentence corrected accordingly (it
  had said "in the 595 random instances" for the iff).
