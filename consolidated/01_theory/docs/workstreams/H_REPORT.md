# Workstream H — algorithms without a hint on the cube: is adaptivity enough?

Independent report.  Directory: `scratch:ws/H/`.
All scripts named below are in this directory and run as `python3 <script>` (numpy/scipy only, < 10 min each, < 3 GB).

Notation (brief §"Setting"): `Q_n`, class `L_u`, `w = e^{-psi}`, `A = 2^{-n} sum w`, accuracy `eps = n eps1`,
`p_u = 1/(1+e^u)`, `Lambda1 = ln(2/(1+e^{-u}))`, `eps* = ln cosh(u/2) = KL(1/2||p_u)`,
`theta_hint(e) = KL((Lambda1+e)/u || 1/2)`, `theta_na(e) = min{KL(rho||1/2) : KL(rho||p_u) <= e}` (both `0` for `e >= eps*`),
`a := theta_na(0+) = KL(p_u||1/2)`, `h := theta_hint(0+)`.
`B(n,r)` Hamming ball, `E_r(n) := sum_{j<=r} C(n,j)(e^{u(r+1-j)} - 1)` (so `e^{Delta_r} - 1 = 2^{-n} E_r`),
`Gamma_n(r) := E_r(n)/|B(n,r-1)|`.  `theta*` = worst-case exponent of adaptive randomised algorithms without a hint.

Status labels: **[proved]** = complete proof in this report (paper proof, not refereed, not machine-checked);
**[sketch]** = proof outline whose missing steps are named; **[numerical]**; **[conjecture]**; **[known]**.

---

## 1. Verdicts in one paragraph

**N1 confirmed** (proof re-derived; exhaustive check of the iterated Harper inequality on all subsets of `Q_3`, `Q_4`; equality
attained).  **N2 confirmed** as stated (fine print: needs `M >= K`; the bound is vacuous for `r = 0`; its width never falls below
`ln 2 + u`, so it is a statement about extensive or large-constant accuracy).  **N3 confirmed** (the non-adaptive exponent is exactly
`theta_na`).  **N4 confirmed in a precise form** (sample splitting, explicit failure probability, Lemma 2.4 below); the coordinator's
wording leaves `t`, `r`, `gamma` and the probability unspecified, and "tight at the hinted optimum at the flat instance" is true at
the exponential scale but, in the Chernoff form, loses a factor up to `1/eps` for `eps -> 0`.  **Main question.**  I could not
refute `theta* = theta_hint`, and I now think it is true.  Three new statements: **(H1) [proved]** on the *radial* subclass
`R_u = {psi = f(d(.,s))}` — which contains the flat instance, all dips, the cone and the flattened cones of N3 — the adaptive
exponent is exactly `theta_hint(eps1)` while the non-adaptive exponent is exactly `theta_na(eps1)`: adaptivity is worth an exponential
factor there, and the N3 instances are easy.  **(H2) [proved, unrefereed]** on the *whole* class `L_u` a two-level "layer-cake"
algorithm (uniform outer sample, plain Monte Carlo brackets inside, adaptive allocation of inner effort by one-sided tests against
a ladder of levels, tail lemma N1 only at the top of the ladder) is correct and has worst-case exponent
`T_2(eps1) = inf_{phi,beta} max_{gamma>=beta} [min(gamma, phi theta_na((eps1-beta)/phi)) + (1-phi) theta_na(gamma/(1-phi))]`,
with `T_2(0+) <= (a + theta_na(a))/2 < a` (numerically `0.505 a` for `u <= 1`, `0.513 a` for `u = 2`) and `T_2 < theta_na` for
`eps1 <~ 0.7 eps*`: **adaptivity strictly helps in the worst case over the whole class**.  **(H3) [sketch + numerical]** using the
`k`-level algorithm as the inner bracket oracle gives `theta* <= T_k`, and the recursion converges numerically to within 0–2 % of
`theta_hint` at every accuracy tested and never goes below it (a consistency test that two wrong versions of my own accounting
failed).  **Coordinator's multilevel proposal:** facts (1), (2) are correct; step (3) (a one-sided inner bound at gap `ln(t/Z_a)`
suffices) is wrong as stated and the recursion `T_{k+1} = a T_k/(a-h+T_k)` is not justified (the coordinator's own "trap" is a
counterexample to the accounting, not to the idea); the threshold ladder repairs it, and the cleanest repair needs no two-sided
inner accuracy at all (§2.6–2.8).  **Negative findings:** every lower-bound family I tried (decoy cones, plateaus with hidden dips,
populations of pits, graph-type non-product instances) costs at most `theta_hint`; among additive instances the flat one is the
hardest for hinted algorithms **[proved from the formula of Theorem 11.27]**; known stability versions of Harper's theorem are far
too weak for this problem; and at simulable sizes (`n <= 48`) the two-level algorithm is much *worse* than plain Monte Carlo —
the gain is asymptotic only.

---

## 2. Precise statements, proofs, counterexamples

### 2.1 N1 (tail lemma) — confirmed **[proved; Harper's theorem is the only external input]**

**Statement.**  `psi in L_u`, `w = e^{-psi}`, `t > 0`, `D = {w > t} != Q_n`.  Then `w(x) <= t e^{u dist(x, D^c)}` on `D`, and if
`|D| <= |B(n,r)|` then `sum_{x in D} (w(x) - t) <= t E_r(n)`.

**Proof.**  For `x in D` pick `y in D^c` at distance `dist(x,D^c)`: `w(x) <= w(y) e^{u d(x,y)} <= t e^{u dist(x,D^c)}`.  Let
`D_k = {x : dist(x,D^c) >= k}` (`D_1 = D`); `D_k` is the complement of the closed `(k-1)`-neighbourhood of `D^c`.  Harper: `|N(S)|`
is minimised, among sets of given size, by an initial segment of the simplicial order, whose neighbourhood is again an initial
segment; so the inequality iterates.  `|D^c| >= 2^n - |B(n,r)| = |B(n,n-r-1)|`, hence `|N^{k-1}(D^c)| >= |B(n,n-r+k-2)|` and
`|D_k| <= |B(n,r+1-k)|`.  Summation by parts:
`sum_D (e^{u dist} - 1) = sum_{k>=1} (e^{uk} - e^{u(k-1)}) |D_k| <= sum_{k>=1} (e^{uk} - e^{u(k-1)}) |B(n,r+1-k)| = E_r(n)`.  ∎

Equality holds for the dip `w = e^{u(r+1-d(x,s))_+}`, `t = 1`.  The same proof works on any cube, in particular on every fibre
`{a} x Q_inner` and for the fibre averages (§2.6, facts (1),(2) of the coordinator).

### 2.2 N2 (plain Monte Carlo) — confirmed **[proved]**

**Statement.**  `M >= K := 8 ln(1/delta1)` uniform samples, `Ahat` their mean of `w`, `r` = least radius with
`|B(n,r)| >= 2^n K/M`, `r >= 1`.  Then with probability `>= 1 - delta1 - delta2`:
`-ln(2(1+Gamma_n(r))) <= ln Ahat - ln A <= ln(1/delta2)`.

**Proof.**  Upper side: Markov.  Lower side: let `t*` be the `ceil(2^n K/M)`-th largest value of `w`, so
`|{w > t*}| <= 2^n K/M <= |{w >= t*}|`.  With `A_t = E min(w,t*)`: N1 gives `A - A_t <= t* 2^{-n} E_r`, and
`A_t >= t* K/M > t* |B(n,r-1)|/2^n` (minimality of `r`), so `A <= (1+Gamma_n(r)) A_t`.  `min(w,t*)/t*` is `[0,1]`-valued with
`M`·mean `>= K`; the multiplicative Chernoff bound gives `P(Ahat_t <= A_t/2) <= e^{-K/8} = delta1`, and `Ahat >= Ahat_t`.  ∎

*Exponent.*  For `r = rho n`, `p_u < rho < 1/2`: `n^{-1} ln Gamma_n(r) -> h(p_u) + u(rho - p_u) - h(rho) = KL(rho||p_u)` and
`n^{-1} ln M -> KL(rho||1/2)`; the recentred estimate (`ln Ahat + [ln(2(1+Gamma)) - ln(1/delta2)]/2`) is therefore
`(eps/2, delta1+delta2)`-correct on all of `L_u` with `exp(n theta_na(eps1) + o(n))` samples.

*Fine print (not errors).*  (i) `M >= K` is needed for `t*` to exist.  (ii) For `r = 0` the statement is vacuous
(`|B(n,-1)| = 0`).  (iii) `Gamma_n(r) >= (e^u - 1) C(n,r)/|B(n,r-1)| >= e^u - 1` for `r < n/3`: the certified width is never below
`ln 2 + u`; N2 is a statement for `eps` extensive (or a large constant).  (iv) The denominator can be sharpened to `2^n K/M`.

### 2.3 N3 (non-adaptive lower bound) — confirmed **[proved]**

`max(psi_s, uR)` is `u`-Lipschitz and differs from the cone `psi_s = u d(.,s)` exactly on `B(s,R-1)`.  If
`ln A(psi_s) - ln A(max(psi_s,uR)) > eps`, Theorem 11.22(b) at the instance `psi_s` forces `P(Q meets B(s,R-1)) >= 1 - 2 delta`;
for a non-adaptive algorithm the law of `Q` does not depend on `s`, and averaging over `s` gives
`E|Q| >= (1-2 delta) 2^n/|B(n,R-1)|`.  The drop is `n KL(R/n||p_u) + O(log n)` for `R/n > p_u` (numerics §3: `0.006306` against
`0.006136` at `n = 20000`).  With N2: **the non-adaptive exponent is exactly `theta_na(eps1)`** for `0 < eps1 < eps*` (finite-`n`
bounds bracket it from both sides, §3).  Both instances of the pair are radial — this is what §2.5 exploits.

### 2.4 N4 (certified bracket from one sample) — confirmed in the following form **[proved]**

**Lemma 2.4.**  Let `w = e^{-psi}`, `psi in L_u` on `Q_d`; `K >= 1`, `m >= 2K`.  Draw `2m` uniform points; let `t` be the `K`-th
largest value of `w` among the first `m`, `What_t` the mean of `min(w,t)` over the last `m`, `r` the least radius with
`|B(d,r)| >= 2^{d+1} K/m`.  With probability at least `1 - e^{-K/4} - e^{-K/6} - 2e^{-K/24}`

    What_t/1.5  <=  mean(w)  <=  2 What_t + t 2^{-d} E_r(d),        and        U/L <= 3 + 12 Gamma_d(r).

**Proof.**  (E1) `P(w > t) <= 2K/m`: otherwise the level `q = inf{s : P(w > s) <= 2K/m}` exceeds `t`, at most `K-1` of the first
`m` samples are `>= q` although their expected number is `>= 2K`; Chernoff: `e^{-K/4}`.  (E2) `P(w >= t) >= K/(2m)`: otherwise at
least `K` samples exceed a level whose exceedance probability is below `K/(2m)`; Chernoff: `e^{-K/6}`.  (E3) Given `t` (independent
of the second half), `min(w,t)/t in [0,1]` has `m`·mean `>= m P(w >= t) >= K/2`, so the relative error of `What_t` is at most `1/2`
outside probability `2e^{-K/24}`.  On E1–E3: `What_t/1.5 <= E min(w,t) <= mean(w)`;
`mean(w) = E min(w,t) + E(w-t)_+ <= 2 What_t + t 2^{-d} E_r` by N1 (E1 gives `|{w > t}| <= |B(d,r)|`); and
`t 2^{-d} E_r / What_t <= (4m/K) 2^{-d} E_r < 8 E_r/|B(d,r-1)|`.  ∎

So the coordinator's bracket `[Ahat_t/(1+gamma), Ahat_t/(1-gamma) + t(e^{Delta_r} - 1)]` is correct with `gamma = 1/2`, `t` the
`K`-th order statistic of an independent half and `r` computed from `2K/m`.  At the flat instance `What_t = t = 1` and the width is
`ln(3 + 1.5(e^{Delta_r} - 1))`, i.e. the hinted optimum of Theorem 11.25(c) up to constants: *no hint is needed there*, at the
exponential scale (§3: exponents `0.02160` against the hinted lower bound `0.02073`, `theta_hint = 0.02018`, at `n = 6400`).
*Caveat.*  With relative error `gamma` the width has the floor `ln((1+gamma)/(1-gamma))`; for `eps -> 0` one needs `K ~ eps^{-2}`
where the hinted cost is `~ eps^{-1}` (Theorem 11.25(d), regime `lambda_c <= lambda`).  At the flat instance all sampled values
coincide and a one-sided count bound restores `eps^{-1}`; I did not write this out.

### 2.5 Theorem H1: on radial instances adaptivity closes the whole gap **[proved; apparently new]**

**Class.**  `R_u = { psi_{s,f}(x) = f(d(x,s)) : s in Q_n, f : {0..n} -> R, |f(j+1) - f(j)| <= u } ⊂ L_u`.  It contains the flat
instance, every dip `-u(R - d(.,s))_+`, the cone and the flattened cones of N3.

**Theorem H1.**  For algorithms that are `(eps/2, delta)`-correct on `R_u`, every `n`, `eps > 0`, `delta < 1/2`:
(a) non-adaptive: `E|Q| >= (1-2 delta) 2^n/|B(n,R-1)|` for the `R` of N3, and N2 applies; exponent exactly `theta_na(eps1)`;
(b) adaptive: with `k*(eps)` the least `k` with `Delta_k > eps`,

    (1 - 2 delta) 2^n/|B(n,k*(eps))|   <=   min_alg max_{psi in R_u} E|Q(psi)|   <=   (n+1) ceil( ln(2n/delta) 2^n / C(n, r_eps) ) + 2n + 1,

where `r_eps - 2` is the largest `k` with `ln[(1 + 4(e^{Delta_k} - 1) + 8|B(n,k)|/2^n)/(1 - 4|B(n,k)|/2^n)] <= eps`
(and `4|B(n,r_eps-2)|/2^n <= delta` is assumed, which holds for every `eps <= n eps*` once `n` is large).  Since
`e^{Delta_{k+1}} - 1 >= e^u (e^{Delta_k} - 1)`, `r_eps >= k*(eps) - O(1 + 1/u)`, and the two sides agree up to a factor polynomial
in `n`: **the adaptive exponent on `R_u` is `theta_hint(eps1)`** for `0 < eps1 < eps*`, against `theta_na(eps1)` without adaptivity.

**Proof.**  (a) cone and flattened cone are in `R_u`.  (b) *Lower bound*: flat instance against the dip of radius `k*(eps)`
centred at an arbitrary `s` (both radial); on the flat instance all answers are `0` until the ball is hit, so the argument of
Theorem 11.25(a) applies verbatim.  *Upper bound*, algorithm RAD(`M`):
1. Draw `x_1..x_M` uniformly; query each `x_i` and its `n` neighbours.
2. If some `x_i` has two distinct neighbour values: the neighbours of a point at distance `j` from `s` take the value `f(j-1)` on
   the `j` coordinates where `x_i != s` and `f(j+1)` on the others; flipping one of the two value classes gives `c in {s, s-bar}`.
   Query a monotone path from `c` to its antipode (`n+1` points): `psi(x) = F(d(x,c))` for all `x`, with `F` now known; output
   `ln 2^{-n} sum_j C(n,j) e^{-F(j)}` — exact.
3. Otherwise let `{alpha, beta}` be the value at `x_1` and the common value of its neighbours; output
   `ln A_0` (recentred), `A_0 = (e^{-alpha} + e^{-beta})/2`.
*Analysis of step 3.*  Let `r` be the least radius with `M C(n,r)/2^n >= ln(2n/delta)` (`r <= r_eps` for the `M` of the theorem).
With probability `>= 1 - delta/2` every
shell `j in [r, n-r]` contains a sampled point, so reaching step 3 means `f(j-1) = f(j+1)` for all `r <= j <= n-r`: `f` is
2-periodic on `[r-1, n-r+1]`, with values `{alpha, beta}` (`x_1` lies in that range with probability
`>= 1 - 2|B(n,r-2)|/2^n`).  The alternating sum of binomial coefficients over an interval is at most `2C(n-1,r-2)`, so the middle
part of `2^n A` is `2^n A_0 (1 ± 4|B(n,r-2)|/2^n)`; each cap is at most `e^{-min(alpha,beta)} sum_{j<r-1} C(n,j) e^{u(r-1-j)}`
`<= 2 A_0 (E_{r-2} + |B(n,r-2)|)` by the Lipschitz bound from the cap boundary.  Hence
`A/A_0 in [1 - 4B/2^n, 1 + 4(e^{Delta_{r-2}} - 1) + 8B/2^n]`, `B = |B(n,r-2)|`.  ∎

Checked by `radial_alg.py` (exhaustive cube `n = 14`, 400 random radial instances: 208/208 exact outputs correct, 192/192
brackets valid).  *Remarks.*  (i) The alternating profile `f(j) = (u/2)(-1)^j` shows that step 3 cannot be dropped: no finite
order of neighbours reveals `s`.  (ii) The algorithm is correct on `R_u` only (step 2 trusts the promise); it is a statement
about where the hardness of N3 comes from, not an algorithm for `L_u`.  (iii) The class "minima of `m <= e^{o(n)}` cones" is
*not* a good test class: a single random start followed by greedy descent finds a centre within `u kappa n` of the deepest one
with probability `>= 1 - m e^{-kappa^2 n/2}`, which determines `ln A` up to `o(n)`; and for `m = 1` even `n+1` non-adaptive
queries suffice.

### 2.6 Theorem H2: a two-level algorithm on the whole class with exponent below `theta_na` **[proved, unrefereed]**

Split the coordinates: `Q_n = Q_o x Q_i`, `n_o = phi n`, `n_i = (1-phi) n`, `psi = psi(a,b)`.
`W(a) := 2^{-n_i} sum_b e^{-psi(a,b)}`, `A = E_a W(a)`, `p(s) := P_a(W(a) > s)`.

**Facts.**  (F1) For each `a`, `b -> psi(a,b)` is `u`-Lipschitz on `Q_i`, so Lemma 2.4 applies to every fibre.
(F2) `a -> -ln W(a)` is `u`-Lipschitz on `Q_o` (`W(a) >= e^{-u d(a,a')} W(a')` termwise), so N1 applies to `W` on `Q_o`:
if `p(s) <= |B(n_o,r)|/2^{n_o}` then `E(W - s)_+ <= s 2^{-n_o} E_r(n_o)`.  (These are the coordinator's facts (1), (2).)
(F3) *Layer cake.*  For levels `s_0 < s_1 < ... < s_j` with `s_0 <= min W`:
`s p(s) <= A` for every `s`, and `A <= s_0 + sum_{i<j} s_{i+1} p(s_i) + E(W - s_j)_+`.

**Inner oracle.**  `INNER(a,m)` = Lemma 2.4 on the fibre of `a` with `2m` queries; outputs `[L,U]` with `U/L <= e^{omega(m)}`,
`omega(m) := ln(3 + 12 max_{r' <= r_m} Gamma_{n_i}(r'))`; for `2K/m <= 2^{-n_i}` the fibre is enumerated (`L = U`).
`m*(x)` := least `m in {2K, 4K, 8K, ...}` with `omega(m) <= x`.  As in N2, `n_i^{-1} ln m*(n_i xi) -> theta_na(xi)` uniformly on
compact subsets of `(0, eps*)`, and `m*(x) = O(K)` for `x >= n_i eps* + O(log n)`.

**Algorithm 2L(`phi`, `beta`, `g`)**, `0 < beta < g`; `b := n beta`, `G := n g`, `b' := 1`, `K := ceil(24 ln(2^{n+6} n^3/delta))`,
`J := ceil(2 u n_o + n_i eps* + n_o ln 2 + 2b + 10)`.
* *Start.*  One outer point `a_ref`, `[L_ref, U_ref] = INNER(a_ref, 2K)`; `s_0 := L_ref e^{-u n_o}` (`<= W(a)` for all `a` by F2);
  `s_j := s_0 e^{j b'}`; `ell := s_0`.  Keep one list `a_1, a_2, ...` of i.i.d. uniform outer points, each with a bracket
  `[L_i, U_i]` that is only ever refined (doubling `m`, intersecting).
* *Classification of `a_i` at level `j`:* refine until `U_i <= s_j` ("LOW") or `L_i > s_j e^{-b}` ("HIGH").
* *Level `j = 0, 1, ...`:* `M := K`; repeat: classify `a_1..a_M`; `N := #HIGH`; `q := min(1, 2 max(N,K)/M)`;
  if `N >= K` put `ell := max(ell, s_j e^{-b} N/(2M))`;
  **closure test:** `r :=` least radius with `|B(n_o,r)| >= 2^{n_o} q`, `tail := s_j 2^{-n_o} E_r(n_o)` (`tail := 0` if
  `2^{n_o} q < 1`); if `tail <= e^{G} ell`, stop and return the midpoint of `[ln ell, ln Upper]`,
  `Upper := s_0 + sum_{i<j} c_i + tail`, where `c_i := s_{i+1} q_i` (`q_i` = the value of `q` when level `i` was left);
  else if `N >= K` ("populated") or `M >= M_j^neg := 2 K J e^{b'} s_j/(ell e^{b})` ("negligible") go to level `j+1`;
  else `M := 2M`.

**Theorem H2.**  For every `psi in L_u`, with probability at least `1 - delta`:
(i) `ln ell <= ln A <= ln Upper` and `ln(Upper/ell) <= n g + ln(4J+3) + 1`; so 2L is `(eps/2, delta)`-correct on `L_u` with
`eps = n g + O(log n)`;
(ii) the number of queries is at most `exp( n tau(phi,beta,g) + o(n) )`, uniformly in `psi`,

    tau(phi, beta, g) := max_{gamma >= beta} [ min( gamma, phi theta_na((g-beta)/phi) ) + (1-phi) theta_na(gamma/(1-phi)) ].

Hence `theta*(eps1) <= T_2(eps1) := inf_{phi, beta} tau(phi, beta, eps1)` (take `g` slightly below `eps1`).

**Corollary.**  `lim_{eps1 -> 0} T_2(eps1) = min_phi max( (1-phi) a , phi a + (1-phi) theta_na(phi a/(1-phi)) ) <= (a + theta_na(a))/2 < a`
(`gamma -> gamma + (1-phi) theta_na(gamma/(1-phi))` is convex, so the maximum over `[0, phi a]` is at an endpoint; `phi = 1/2`).
Numerically (grid upper bounds) `T_2(0+)/a <= 0.505, 0.505, 0.513` for `u = 0.5, 1, 2`, and `T_2(eps1) < theta_na(eps1)` on the whole grid
`eps1 <= 0.68 eps*` (ratio `0.51 -> 0.89`); for `eps1 >~ 0.8 eps*` the formula does not beat plain Monte Carlo (§3).

**Proof.**  *Good event.*  (V1) every bracket produced by `INNER` is valid; (V2) for every level `j` and every `M` in the
doubling sequence: if `M p(s_j) >= 2K` then at least `M p(s_j)/2` of `a_1..a_M` have `W > s_j`; (V3) for every `j`, `M` and every
`x in {b, b+b', ...}`: `#{i <= M : W(a_i) > s_j e^{-x}} <= max(2 M p(s_j e^{-x}), K/2)`.  Each event fails with probability at most
`4e^{-K/24}` (Lemma 2.4, Chernoff), and there are at most `2^{n+5} n^2` brackets (the algorithm aborts beyond that number, which does
not happen on the good event) and `O(n^3)` pairs/triples; the choice of `K` makes the total `<= delta`.
(The levels depend only on `a_ref`, which is independent of the list.)

*Validity.*  By V1, `W(a) > s_j` implies HIGH, and HIGH implies `W(a) > s_j e^{-b}`.  So `N >= #{W > s_j}` and V2 gives
`p(s_j) <= q`; if `N >= K`, V3 gives `p(s_j e^{-b}) >= N/(2M)`, hence `s_j e^{-b} N/(2M) <= A` by F3: `ell <= A` always.
`A <= Upper` by F3 (`c_i >= s_{i+1} p(s_i)`) and F2 (the set `{W > s_j}` has at most `2^{n_o} q <= |B(n_o,r)|` points).

*Width.*  A populated level has `c_i = s_{i+1} 2N/M = 4 e^{b+b'} (s_i e^{-b} N/(2M)) <= 4e^{b+b'} ell`; a negligible one has
`c_i <= s_{i+1} 2K/M_i^neg = e^{b} ell/J`; `s_0 <= ell`; `tail <= e^{G} ell`.  So `Upper/ell <= 1 + 4J e^{b+b'} + e^{b} + e^{G}`.

*Termination within `J` levels.*  Above `max W · e^{b} <= s_0 e^{2un_o + omega(2K) + b}` nothing is HIGH; `M_j^neg` then grows by
`e^{b'}` per level, and once `2^{n_o} · 2K/M < 1` the tail is `0`.

*Sample sizes.*  Let `r†` be the largest `r` with `Gamma_{n_o}(r') <= e^{G-b}/4` for all `1 <= r' <= r`, and
`M† := 2K 2^{n_o}/|B(n_o,r†)| = exp(n phi theta_na((g-beta)/phi) + o(n))`.  Since `2^{-n_o} E_r < q Gamma_{n_o}(r)` (minimality
of `r`): at a populated level `tail < s_j q Gamma(r) <= 4e^{b} ell Gamma(r)`, at a negligible one
`tail < e^{b} ell Gamma(r)/(J e^{b'})`; so a level that is left without stopping has `r > r†`, i.e. `q_j > 2K/M†`.
Consequently `M_j^neg <= 4J e^{2b'} M†` for every level reached: `ell` never decreases, so `M_j^neg <= e^{b'} M_{j-1}^neg`; if level
`j-1` was negligible then `M_{j-1}^neg <= M_{j-1} < M†`; if it was populated then `ell >= s_{j-1} e^{-b} q_{j-1}/4`, whence
`M_j^neg <= 8KJ e^{2b'}/q_{j-1} < 4J e^{2b'} M†`.  So every `M` used is at most `8J e^{2b'} M†`.

*How many samples are close to a level.*  For every ladder level `i < j`: `s_i p(s_i) <= s_i q_i <= 4 e^{b} ell` (populated:
`s_i q_i = 4e^{b} · s_i e^{-b} N/(2M) <= 4e^{b} ell`; negligible: `s_i q_i <= e^{b} ell/(J e^{b'})`).  For
`x >= b` let `s_i` be the largest ladder level `<= s_j e^{-x}`; then
`M_j^neg p(s_j e^{-x}) <= (2KJ e^{b'} s_j/(ell e^{b})) · 4 e^{b} ell e^{b'} e^{x}/s_j = 8KJ e^{2b'} e^{x}` — the factors `e^{b}`
cancel, which is why the same tolerance `b` is used for HIGH and for negligibility.  With V3: at most
`32 K J e^{2b'} e^{x} + 4K` of the samples used at level `j` have `W > s_j e^{-x}`.

*Cost.*  A sample with `W(a) = s_j e^{-G_a}` is classified at level `j` as soon as `omega(m) <= max(G_a, b)` (if `omega <= G_a`
then `U <= W e^{omega} <= s_j`; if `omega <= b` and `U > s_j` then `L > s_j e^{-b}`), i.e. after at most `8 m*(max(G_a,b))` queries
in total.  Summing over levels and over `x in b + b' N`:

    #queries <= sum_j sum_x min( 8J e^{2b'} M† , 32KJ e^{2b'} e^{x+b'} + 4K ) · 8 m*(x),

whose exponent is `max_{gamma >= beta} [min(gamma, phi theta_na((g-beta)/phi)) + (1-phi) theta_na(gamma/(1-phi))] + o(1)`.  ∎

**What the algorithm does, in words.**  It never estimates a mean of heavy-tailed values.  It certifies, level by level, that
few outer points lie above the level (`p(s_j) <= q_j`) — a one-sided statement whose cost per sample is governed by the *gap*
between the sample and the level — and it uses the tail lemma once, at the top, where the certified exceedance probability is
already of the order of a ball of radius `rho_na`.  On a cone the high levels are populated only near the outer centre, so the
expensive inner brackets are spent there (`max(phi,1-phi) a`); on a flat outer landscape level `sigma` above the bulk needs
`e^{n sigma}` samples but only inner width `n sigma` (`sigma + (1-phi) theta_na(sigma/(1-phi))`, again `<= a/2`); the "trap"
(flat bulk + slightly supercritical bump) is the same computation.  The lower bound of Theorem 11.25 is respected: at the flat
instance, level `sigma` hits a critical dip through outer distance `x = sqrt(sigma)` (small-`u` units) with probability of order
one, at every `sigma` simultaneously.

**Caveats.**  (1) The proof is complete as far as I can see, but it is mine alone and unrefereed; two earlier versions of
the *accounting* (not of the validity argument) were wrong — see §2.8.  (2) Constants are hopeless at small `n`: `two_level_sim.py`
(`n = 32`) confirms validity of every bracket but needs far more queries than plain Monte Carlo for a wider bracket (§3).
(3) The accuracy is `n g + O(log n)`: nothing is claimed for `eps = O(1)`.

### 2.7 Proposition H3: deeper recursion, and where it converges **[sketch + numerical]**

Define `T_1 := theta_na` and

    T_{k+1}(g) := min( T_k(g),  inf_{phi in (0,1), 0<beta<g}  max_{gamma >= beta} [ min(gamma, phi theta_na((g-beta)/phi)) + (1-phi) T_k(gamma/(1-phi)) ] ).

**Proposition H3 (claim).**  `theta*(eps1) <= T_k(eps1)` for every fixed `k`.

*Sketch.*  Run algorithm 2L with `INNER` replaced by the `k`-level algorithm on the fibre (itself a 2L-type algorithm on a split
of the inner coordinates).  The proof of H2 uses only two properties of the inner oracle: (P1) for a target width `x` it returns a
valid bracket of ratio `<= e^{x}` on **every** instance, with a failure probability that survives the union bound;
(P2) its cost for target `x` is at most `exp(n_i T_k(x/n_i) + o(n))` on every instance.  H2(i),(ii) are exactly (P1),(P2) for
`k = 2`, and the argument for level `k+1` given level `k` is the same.  The one change: the width is no longer a deterministic
function of the effort, so classification calls the oracle with targets `x_l = x_0 (1-zeta)^l` until LOW/HIGH; a sample at gap
`G_a` then costs `poly · exp(n_i T_k((1-zeta) max(G_a,b)/n_i))`, and `zeta -> 0` after `n -> infinity`.  *Not written out:* the
uniformity of the `o(n)` terms through `k` nested levels, the failure-probability budget (`K` grows by a constant factor per
level), and measurability details.  The top of each ladder is closed by the plain tail lemma on that level's outer block, which
is why `theta_na` (not `T_k`) appears in the first term.

**Numerical evaluation** (`ml_recursion.py`, grid in `eps1`, `phi`, `beta`, `gamma`; entries are `T_k/theta_na`; last row
`theta_hint/theta_na`):

| `u = 1`, `eps1/eps*` | 0 | 0.016 | 0.062 | 0.25 | 0.49 |
|---|---|---|---|---|---|
| `k = 2` | 0.505 | 0.512 | 0.542 | 0.641 | 0.763 |
| `k = 3` | 0.365 | 0.400 | 0.453 | 0.595 | 0.751 |
| `k = 4` | 0.315 | 0.363 | 0.426 | 0.586 | 0.750 |
| `k = 6` | 0.283 | 0.343 | 0.414 | 0.583 | 0.749 |
| `k = 12` | 0.268 | 0.335 | 0.409 | 0.583 | 0.749 |
| `k = 48` | 0.265 | 0.333 | 0.408 | 0.583 | 0.749 |
| `theta_hint/theta_na` | 0.263 | 0.331 | 0.406 | 0.577 | 0.733 |

(`u = 0.5`: `k = 48` row `0.256, 0.322, 0.397, 0.572, 0.742` against `0.253, 0.320, 0.395, 0.566, 0.725`; `u = 2`:
`0.299, 0.370, 0.447, 0.618, 0.775` against `0.297, 0.368, 0.445, 0.612, 0.758`.)  Two observations.
(1) **`T_k >= theta_hint` on the whole grid for every `k`** (`max(theta_hint - T_k) = 0.00000` in the output).  This is a
necessary condition for any correct scheme (flat-instance lower bound) and a sharp test of the accounting: two earlier versions
of my recursion violated it (§2.8).  (2) **The limit is within 0–2 % of `theta_hint`** (closest at small `eps1`; the residual at
larger `eps1` is of the order of the grid resolution in `beta`, and I cannot say whether it is real).

**Conjecture H4.**  `lim_k T_k = theta_hint` on `(0, eps*)`; with H3 this gives `theta* = theta_hint`: *adaptivity is enough.*
What is proved is `theta_hint <= theta* <= T_2 < theta_na` (small `eps1`).

### 2.8 Verdict on the coordinator's multilevel proposal

* **Facts (1), (2): correct** (F1, F2 above; one-line proofs).
* **Step (3) is wrong as stated.**  "An outer sample with `Z_a = t e^{-G}` needs only a one-sided inner bound at gap `G`" does
  not give the outer bracket: certificates `Z_a <= t` bound `sum_a min(Z_a,t)` only by `M t`, whereas the main term can be as
  small as `K t`.  What the single-threshold bracket needs is `sum_a (U_a - L_a) <= eta sum_a L_a`, i.e. gaps measured from the
  tolerance `eta · Ahat_t`, not from `t`; then Markov's inequality gives no bound on the number of samples at small gap.
  *Counterexample to the accounting* (the coordinator's "trap", found independently): outer landscape = flat bulk + bump of
  radius just above `rho_hint`, inner landscapes = flattened cones with plateau radius tuned to the required gap (a product
  instance `psi(a,b) = u(d(b,s_i) - R_i)_+ - u(R_o - d(a,s_o))_+`).  The single-threshold scheme pays
  `phi theta_na(eps1/phi) + (1-phi) theta_na(~2 eps1/(1-phi))`, which tends to `a` as `eps1 -> 0`: no gain, and the recursion
  `T_{k+1} = min_phi max(phi a, phi h + (1-phi) T_k)` is not justified.
* **The ladder repairs it.**  With the ladder the coordinator's count
  `min(M, M · E min(Z,t)/(t e^{-G}))` is the right Markov bound *per level*, and the resulting accounting ("CLOSE": stop at the
  first level where the outer tail lemma closes) evaluates to `T_2/theta_na = 0.58–0.60` at `eps1 -> 0` (full supremum over
  outer shapes and gaps; the coordinator's `0.571–0.625`), `0.33–0.37` at six levels.  Question (ii): at `eps1 = 0` the
  maximiser is at one of the two endpoints for `k = 2, 3, 4` — outer flat (`rho_o = rho_hint`, gap `0`) or outer cone
  (`rho_o = p_u`, all samples) — (`close_argmax.py`); the full recursion gives `0.586, 0.453, 0.391` (`u = 1`) against
  `0.576, 0.439, 0.373` from `T_{k+1} = a T_k/(a-h+T_k)`: the endpoint recursion is a good, slightly optimistic, approximation
  of the CLOSE accounting.  **I did not prove the CLOSE accounting** (it needs two-sided inner accuracy on the samples that carry
  each stratum, and the inner brackets of N2/N4 have the floor `ln 2 + u`).
* **A cleaner repair (§2.6).**  Replace "estimate the strata" by "bound the exceedance probabilities" (layer cake): at the
  exponential scale `A = max_s s · P(W > s)` up to the ladder ratio, so only one-sided classifications with a tolerance are
  needed, the tail lemma enters once, and the worst case has no supremum over outer shapes.  This is Theorem H2
  (`T_2(0+) ≈ a/2`), and its recursion has the fixed point the coordinator conjectured (`theta_hint`, numerically) although the
  recursion itself is different (`a/2, 0.36a, 0.31a, ...` instead of `a T_k/(a-h+T_k)`).
  CLOSE and CLIMB are incomparable instance by instance (at the flat instance CLOSE costs `phi h + (1-phi) T_k`, the climb costs
  more; at the trap the climb is cheaper); a scheme may dovetail both.
* **The coordinator's open items.**  (i) non-product instances: the proof of H2 uses no product structure — only Markov/layer-cake
  bounds certified at lower levels; (ii) see above; (iii) `K = O(n + ln(1/delta))` suffices for all union bounds;
  (iv) no oracle allocation is needed: "refine until LOW or HIGH", with doubling of `M` until populated/negligible, is the
  allocation; the threshold is not known in advance and need not be; (v) only the *maximum* of the tolerances (straddling/negligible
  `beta`, closure `g`) enters the width; the infinite slope of `theta_na` at `0` is harmless (it helps: the bottom term
  `(1-phi) theta_na(beta/(1-phi))` drops quickly).
* **Simulation** (`two_level_sim.py`, `n = 32`, eight instances incl. cone, flat, outer-flat × inner-cone, flattened cone, dip,
  trap, random bi-radial): all 32 brackets valid; the algorithm is far from competitive at this size (§3).
* **A warning from my own errors.**  I derived three wrong recursions before the final one: (v1) counted the samples within gap
  `gamma` as `e^{n(gamma - g_1)}` (the negligibility tolerance does not reduce that count); (v2, v4) forgot that the first
  negligible level above a bulk already needs `e^{n beta}` samples.  v2 and v4 produce `T_k < theta_hint` and are thereby refuted;
  v1 passes the test by luck.  The outputs are kept (`out_ml_recursion_v*.txt`).  Any future accounting should be run through the
  test `T_k >= theta_hint`.

### 2.9 Is the flat instance the hardest one with a hint?  (partial)

If some instance had a hinted exponent above `theta_hint(eps1)` the conjecture `theta* = theta_hint` would fail trivially.

* **Additive instances `theta |x ⊕ s|`, `|theta| <= u` [proved from the game formula of Theorem 11.27; the range `t > 1` checked
  numerically].**  For the two-state site the matrix game is `2 x 2`:
  `val(K_t) = e^{t(P(theta) - P(u))} (1 + e^{-tu})/(1 + e^{-t theta})`, `P(x) = ln(1 + e^{-x})`, so
  `R(eps1; theta) = max_{t >= 0} [ -t(P(theta) - P(u)) + P(t theta) - P(tu) - t eps1 ]`.
  The derivative of the bracket in `theta` is `t (P'(t theta) - P'(theta))`, which has the sign of `-theta` for `0 < t < 1`
  (`P` convex): for each such `t` the bracket is maximal at `theta = 0`, where it gives `theta_hint`.  `hint_additive.py`:
  `max [R(eps1;theta) - R(eps1;0)] = 0.0` over `u in {0.3..4}`, 15 accuracies, 81 slopes, with the maximiser always in `[0,1]`.
  So **among additive instances of equal slopes the flat instance is the hardest**; for mixed slopes the common-`t` lower-bound
  functional of Theorem 11.28 is also maximal at slopes `0`.
* **Ball plateaus [numerical, restricted family].**  `g = u'(d(.,0) - R')_+` with `p_{u'} < R'/n < 1/2`: the Gibbs measure is
  (nearly) uniform on a sphere and the critical dip radius drops to `(eps1 + h(r') - ln(1+e^{-u}))/u < rho_hint`; but sampling
  an inner or outer shell hits all rim-centred dips with exponent at most `0.9989 theta_hint` in all 263 parameter cases
  (`plateau_explore.py`).  The "centre advantage" and, outside the plateau, the rigidity of steep slopes more than compensate.
* Open: a proof that `sup_g theta_hint(g, eps1) = theta_hint(flat, eps1)` over all of `L_u` (it would follow from H3 + H4).

### 2.10 Attempts at a lower bound above `theta_hint` (all negative) **[heuristic computations, recorded as dead ends]**

A pair `(g_0, g_1)` at distance `> eps` must differ on a set carrying a share `1 - e^{-eps}` of the Gibbs mass of one of them;
the adversary wants that set small *and* unlocatable.  Under the Lipschitz constraint depth forces width (N1), and every family
I tried is found at cost `<= e^{n theta_hint}`:

1. *Pit of radius `T` with a flattened bottom among `N` decoys, one decoy unflattened.*  Significance against the background
   forces `u T/n > Lambda1 + eps1`; sampling finds all pits at cost `2^n/|B(T)|`, i.e. exponent `KL(T/n||1/2) < theta_hint`.
2. *Rough background* (distance to a random code with cell radius `kappa n < p_u n`): the level `-ln A` shifts but the critical
   radius of a hidden cone does not; the hidden funnel is recognisable by the fraction of downhill directions (`tau` against
   `kappa`).
3. *Low-lying plateau `W` (measure `e^{-n gamma}`) with a hidden dip `V ⊂ W`.*  The dip radius drops to `rho_hint - gamma/u`, but
   the funnel of `W` has radius `>= rho_hint` (Harper), and `|W|/|V|` has exponent
   `KL(rho_hint - gamma/u||1/2) - gamma <= theta_hint` because `h' <= u` above `p_u`.
4. *Population of `e^{n nu}` cones tiling the cube, all flattened at radius `rho n` except a fraction `e^{-n lambda}`.*  Centres
   are found by slopes at polynomial cost; the rare ones matter iff `lambda < KL(rho||p_u) - eps1`, and `nu >= lambda` with
   `nu = KL(rho||1/2)` forces `rho <= rho_hint`: the cost `e^{n lambda}` is at most `e^{n theta_hint}`, with equality exactly in
   the degenerate limit where the instance is flat with one critical dip.  (I find this coincidence the best heuristic
   evidence for the conjecture.)
5. *Non-product "graph" instances* `psi(a,b) = u d(b, iota(a))` (outer flat, inner cones with moving centres): a product
   instance over pair-sites; costs the two-level scheme `phi h + (1-phi) a` in the CLOSE accounting but is not hard in itself.
6. *Long thin valleys* (Aldous-type local-search instances): impossible here — the oscillation of `psi` is at most `un`, so a path
   of exponential length is level, and its tube is a plateau as in 3.
7. *Stability of Harper's theorem* as a tool for an algorithm ("a near-extremal tail is nearly a cone"): Keevash–Long need the
   boundary within a factor `1 + c/n` of the minimum, Przykucki–Roberts treat radii `<= log n/(3 log log n)`; the present problem
   needs stability under an *exponential* slack `e^{n zeta}`, where nothing like "close to a ball" can hold (§4).

---

## 3. Numerics: what, sizes, results (exact commands and outputs)

All commands are run from this directory.  `hlib.py` holds the shared formulas (own code; nothing imported from the
coordinator's scratch files, which I read but did not run).

**`python3 verify_N1.py`** (≈ 1.5 min) → `out_verify_N1.txt`.  Iterated Harper inequality
`|{x : dist(x,D^c) >= k}| <= |B(n,r+1-k)|` for *all* subsets of `Q_3` and `Q_4`, random/structured subsets up to `n = 10`; N1 for
every threshold of 1320 random Lipschitz functions from six generators (McShane upper/lower extensions, additive, radial walks,
bounded noise + cone, max/min of cones); equality case.

    exhaustive iterated Harper, n=3: subsets=254 violations=0
    exhaustive iterated Harper, n=4: subsets=65534 violations=0
    random/structured subsets, n=5: sets=4000 violations=0      (same for n=6, 8; n=10: sets=600 violations=0)
    N1 on random Lipschitz functions n=10 u=1.3: (thresholds, violations, max lhs/rhs, non-Lipschitz instances) = (41966, 0, 1.0000000000000038, 0)
    (n=4,u=0.7: 2414 thresholds; n=6,u=1: 7767; n=8,u=0.5: 27484; n=8,u=2: 27548 — all 0 violations, max lhs/rhs = 1.000000)
    equality case (dip of radius 3, n=10): lhs/rhs = 1.000000000000

**`python3 verify_N234.py`** (≈ 2 min) → `out_verify_N234.txt`.
*N2*, simulation at `n = 40`, `u = 1`, `K = 23.97`, 2000 repetitions × 7 radial instances × `M in {200, 2000, 20000}`:
`P_low_fail = 0.0000` in all 21 cases (claimed `<= 0.05`), `P_up_fail <= 0.0005` (claimed `<= 0.05`); e.g.
`cone M=200 r=16 bound_low=-5.029 min dev=-2.395 median=-0.546 max=2.978`.
*N3*, drop of `ln A` against `n KL(R/n||p_u)`: `u=1 n=20000 R/n=0.3190: drop/n=0.006306 KL=0.006136`;
`u=2 n=20000 R/n=0.2692: drop/n=0.083081 KL=0.082866`.
*N2/N3*, finite-`n` exponents `n^{-1} ln(#queries)` (non-adaptive lower bound | Monte Carlo upper bound):

    u=0.5 eps1=0.00773 n= 12800: lower 0.00811 (R=5600)  upper 0.00877 (r0=5579)  theta_na=0.00761  theta_hint=0.00431
    u=1.0 eps1=0.06006 n=   200: lower 0.02265 (R=84)    upper 0.06292 (r0=73)    theta_na=0.00979  theta_hint=0.00723
    u=1.0 eps1=0.06006 n= 12800: lower 0.01017 (R=5502)  upper 0.01058 (r0=5494)  theta_na=0.00979  theta_hint=0.00723
    u=2.0 eps1=0.10845 n= 12800: lower 0.08869 (R=3751)  upper 0.08936 (r0=3744)  theta_na=0.08807  theta_hint=0.05390

(both bounds approach `theta_na` from above; 36 parameter triples in the file).
*N4* (Lemma 2.4, `n = 40`, `K = 40`, 1500 repetitions): coverage `1.0000` in all 21 cases (proved failure bound `0.38` at this
`K`); widths e.g. `flat M=40000: 1.110` (floor `ln 3`), `cone M=40000: 2.401`.  *N4 at the flat instance versus the hinted
optimum:* `u=1 n=6400 eps1=0.020: hinted lower bound exponent 0.02073; N4 without hint 0.02160; theta_hint=0.02018`;
`u=2 n=6400 eps1=0.100: 0.05747; 0.05839; 0.05679`.

**`python3 radial_alg.py`** (≈ 20 s) → `out_radial_alg.txt` (Theorem H1, exhaustive cube `n = 14`, 400 random radial instances):
`{'exact': '208/208 correct', 'bracket': '192/192 correct', 'vacuous': '0/0 correct'}  median bracket width: 0.018`.

**`python3 ml_recursion.py`** (≈ 4 min) → `out_ml_recursion.txt`.  Recursion of §2.7 (CLIMB) for `k <= 48` and the
coordinator's accounting (CLOSE) for `k <= 6`, `u in {0.5, 1, 2}`, 41 accuracies.  Table of §2.7; in addition, for `k = 2`
(`T_2/theta_na` along the accuracy grid, `u = 1`):
`0.00:0.505 0.02:0.522 0.05:0.540 0.09:0.559 0.14:0.587 0.20:0.619 0.28:0.656 0.36:0.697 0.46:0.743 0.56:0.809 0.68:0.890 0.81:1.000`
and `max(theta_hint - T_k) = ±0.00000` in every CLIMB and CLOSE line.  CLOSE: `k=2: 0.586 (phi=0.56)`, `k=6: 0.342` at `eps1 = 0`,
`u = 1`.  `python3 close_argmax.py` → `out_close_argmax.txt` (location of the worst outer shape, §2.8).
The files `out_ml_recursion_v1_optimistic.txt`, `_v2_buggy.txt`, `_v3_draft.txt`, `_v4_buggy.txt`, `_v5_draft.txt` are records
of superseded accountings (§2.8) and are **not** evidence for anything.

**`python3 two_level_sim.py 16`** (≈ 9 min, `n_o = n_i = 16`, `u = 2`, `b = 3`, `b' = 1`, `K = 16`, 4 runs per instance, query
budget `1.5e8` per run) → `out_two_level_sim_16.txt`.  Implementation of algorithm 2L (a slightly earlier variant: negligibility
tolerance `1` instead of `e^{b}`, closure tested only when a level is left as negligible, the factor `J` in `M^neg` dropped —
changes that affect cost and width, not validity) on bi-radial instances
`psi = F[d_o, d_i]` (exact sampling through binomial distances, exact `ln A`).  Result: `ALL BRACKETS VALID` (32/32, including
the runs stopped by the budget, whose bracket is `[ell, +inf)`).  Three instances closed within budget:

    flat                      two-level: covered=True width= 5.86 queries=3.15e+07   plain N4 at the same number of queries (capped at 8e6): width=1.10
    outer flat x inner cone   two-level: covered=True width= 5.87 queries=1.1e+08    plain N4 ...: width=1.70
    random bi-radial          two-level: covered=True width= 6.48 queries=1.8e+08    plain N4 ...: width=1.10

and five did not (cone, outer cone × inner flat, flattened cone, dip, trap).  **Reading:** at `n = 32` the scheme is far worse
than plain Monte Carlo (ladder of ~100 levels, `K`, and the constant `e^{2u}` of the tail lemma at radius `<= 1` dominate; the
outer cube has only `65536` points while up to `2·10^6` outer samples are requested).  The simulation validates the logic of the
bracket, nothing else; the exponents of §2.6–2.7 are statements about `n -> infinity` and cannot be seen at sizes I can simulate.

**`python3 hint_additive.py`** (≈ 5 s): `max over u, eps1, theta of [R(eps1;theta) - R(eps1;0)] = 0.0 ... maximiser t always in [0,1]`.
**`python3 plateau_explore.py`** (≈ 30 s) → `out_plateau_explore.txt`: 264 parameter cases (`u in {0.5,1,2}`, four accuracies,
plateau radii `0.3..0.5`, three outside slopes); largest ratio (hitting exponent)/`theta_hint` over the non-flat cases: `0.9989`.

---

## 4. Prior art, with search log

What I actually read is marked: **[A]** abstract or search-engine summary only; **[S]** machine summary of the full text
(fetched page summarised by a tool; I did not read the source line by line); **[M]** from memory, not re-checked.

| query (web search, 25 Nov 2026) | found | read |
|---|---|---|
| adaption versus non-adaption, information-based complexity, Novak "adaption helps", Lipschitz class | Novak, *On the power of adaption* (survey); Novak, *Optimal algorithms for numerical integration: recent results and open problems* (arXiv 2307.06787); Krieg–Novak–Ullrich, *On the power of adaption and randomization* (arXiv 2406.07108) | [A] |
| Heinrich, randomized complexity, adaption, mean computation | Heinrich, *Randomized complexity of parametric integration and the role of adaption I* (J. Complexity 2024); *Randomized complexity of mean computation and the adaption problem* (arXiv 2401.14100); Kunsch–Novak–Wnuk (arXiv 2308.01705); Kunsch–Wnuk (arXiv 2410.23067) | [A] |
| Holzmüller–Bach, convergence rates for non-log-concave sampling and log-partition estimation | JMLR 26 (2025), arXiv 2303.03237 | [A] (the theory report's own reading in `prior_art/L7` is more detailed) |
| Ge–Lee–Lu, estimating normalizing constants for log-concave distributions | STOC 2020, arXiv 1911.03043 | [A] |
| stability of Harper's vertex-isoperimetric inequality | Keevash–Long (arXiv 1807.09618); Przykucki–Roberts (arXiv 1808.02572) | [S] of the ar5iv pages (main theorems) |
| Broadie–Du–Moallemi, nested sequential simulation | Management Science 57 (2011) 1172–1194; Giles–Haji-Ali, *Multilevel nested simulation for efficient risk estimation* (arXiv 1802.05016) | [A] |
| (no search) nested sampling (Skilling 2006), multilevel splitting (Kahn–Harris; Cérou–Guyader), "tootsie pop" product estimators (Huber–Schott), Chatterjee–Diaconis 2018, Aldous 1983 / Aaronson 2004 / Zhang 2006 on local search on the cube | — | [M] |

**What these say, as far as I read.**
* *Adaption in IBC.*  For linear problems on convex symmetric classes adaption does not help deterministically
  (Bakhvalov, Gal–Micchelli; [A]/[M]); in the randomised setting the question was open for decades and was settled by Heinrich:
  gaps of order `n^{1/8}`, `n^{1/4}` and, for vector-valued approximation, larger (up to order `n`, Kunsch–Novak–Wnuk) between
  adaptive and non-adaptive `n`-th minimal errors [A].  The present problem is outside that framework (the functional
  `psi -> ln mean e^{-psi}` is non-linear, the regime is "dimension to infinity, exponential cost"), and the gaps here are
  *exponential in the number of queries*: on `R_u` exactly `theta_na` against `theta_hint` (H1), on `L_u` at least `theta_na`
  against `T_2` (H2).  I found no statement of N2/N3 (plain Monte Carlo is optimal among non-adaptive algorithms on a Hamming–
  Lipschitz class, with exponent `min{KL(rho||1/2) : KL(rho||p_u) <= eps1}`) and none of H1/H2.  **This is "not found", not "new":
  I read abstracts only.**
* *Normalising constants.*  Holzmüller–Bach: worst-case rates for smoothness classes on `[0,1]^d`, optimisation regime versus
  quadrature regime [A]; Ge–Lee–Lu: algorithms and an information-theoretic lower bound of order `d^{1-o(1)} eps^{-2-o(1)}` queries
  for log-concave densities [A].  Neither treats the exponential regime of a Lipschitz class in growing dimension.
* *Stability of Harper.*  Keevash–Long: `|A| = |ball|` and vertex boundary `<= (1 + c/n)` × minimum imply
  `|A Δ ball| <= delta C(n-1,k-1)` [S]; Przykucki–Roberts: sets of size `C(n,k)`, `k <= log n/(3 log log n)`, neighbourhood within
  an additive `C(n,k) p` of the minimum [S].  Both are stability at multiplicative slack `1 + o(1)`; an algorithm built on
  "a near-extremal tail is nearly a cone" would need slack `e^{n zeta}`.  I therefore did not pursue that route.
* *Algorithmic relatives.*  The layer-cake/level-set idea is that of nested sampling and multilevel splitting, which assume a
  constrained-sampling oracle (or mixing) that the query model does not provide [M]; adaptive allocation of inner samples to
  outer scenarios near a threshold is the idea of nested sequential simulation in risk estimation (Broadie–Du–Moallemi; mean
  squared error analysis, sequential tests) [A].  What I did not find: a *certified* (worst-case, one-sided) version of either,
  the use of an isoperimetric tail lemma to close the top of the ladder, or a recursion for worst-case exponents.
* *Local search on the cube* (Aldous; Aaronson; Zhang: `2^{n/2}`-type query bounds for finding a local minimum) [M] does not
  transfer: its hard instances are long level paths, which under the constraint `osc(psi) <= un` carry no mass (§2.10, item 6).

---

## 5. What I did not settle

1. **`theta*` itself.**  Proved: `theta_hint <= theta* <= T_2`, with `T_2 < theta_na` for small `eps1` (numerically for
   `eps1 <~ 0.7 eps*`).  For `eps1` near `eps*` I have no algorithm better than plain Monte Carlo (the two exponents differ only in
   higher order there).  The value of `theta*` remains open.
2. **Proposition H3** (induction over levels) is a sketch.  The delicate points are those where I already erred twice in the
   two-level case: which tolerance enters which count.  It should be written with the same care as §2.6, or machine-checked in
   its single-letter part (the recursion).
3. **Conjecture H4** (`lim T_k = theta_hint`) is numerical (agreement 0–2 %).  I have no analytic argument; the recursion has
   `theta_hint` as a fixed point only in the limit `phi -> 0`.
4. **Theorem H2 is unrefereed.**  I re-derived every inequality after each correction and tested the bracket on 32 simulated
   runs, but the cost bound (the part that matters) is not testable at small `n`.
5. **Hinted complexity of non-additive instances.**  Is the flat instance the hardest instance with a hint on all of `L_u`?
   Proved for additive instances of equal slopes; numerical for ball plateaus.
6. **Exact small cases** (game trees for `n <= 4`): not attempted — after H1 the restricted families I would have used
   (radial values on a grid) are understood asymptotically, and for `n <= 4` every exponent statement is void.
7. **Small or constant `eps`.**  Everything new here is for `eps = n eps1`; N2/N4-type brackets have the floor `ln 2 + u`.
   Exponentially small accuracies are untouched.
8. **CLOSE accounting** (the coordinator's ladder with the tail lemma at every level): evaluated, not proved; it is
   instance-wise incomparable with the climb of §2.6.
9. Whether N2/N3/H1/H2 are known: abstracts only (§4).

## 6. The three most promising next steps

1. **Referee Theorem H2, then write Proposition H3 as a theorem.**  H2 already answers the question "does adaptivity help in the
   worst case on the whole class?" (yes, `T_2(0+) ≈ theta_na(0+)/2`).  The induction needs one clean statement of the oracle
   interface — "(P1) valid bracket of ratio `e^x` on every instance, (P2) cost `exp(n T(x/n) + o(n))` on every instance" — and a
   proof that 2L maps such an oracle to such an oracle with `T -> T'` given by the recursion.  The consistency test
   `T_k >= theta_hint` should accompany every version.  A Lean statement of the layer-cake inequality F3 and of the width bound
   would be cheap and would protect the bookkeeping.
2. **Prove (or refute) `lim_k T_k = theta_hint` analytically.**  This is a one-dimensional problem about the operator
   `T -> inf_{phi,beta} max_gamma [min(gamma, phi theta_na((g-beta)/phi)) + (1-phi) T(gamma/(1-phi))]`.  Natural route: pass to the
   continuum limit `phi -> 0` (a first-order PDE / Hamilton–Jacobi equation in the variables (remaining fraction, accuracy)) and
   identify `theta_hint` as its solution; the parametrisation `u rho = Lambda1 + g` and the identity
   `KL(rho||p_u) - KL(rho||1/2) = u rho - Lambda1` suggest that the characteristics are the lines of constant `rho`.  If the limit
   is strictly above `theta_hint` at large `eps1` (the numerics leave 2 % room), dovetailing the climb with the CLOSE strategy —
   which is optimal at the flat instance — is the candidate that removes the gap.
3. **Lower-bound side: one honest attempt with several instances at once, on a class where slopes carry no information.**
   H1 and §2.10 say that every structure built from Hamming balls is found at cost `e^{n theta_hint}`; H3/H4 say why (the
   layer-cake scheme never uses geometry).  If the conjecture is to fail, it must fail through the *accounting* of the scheme,
   i.e. through an instance on which samples at small gap from a level are more numerous than the certified bound
   `e^{gap}` allows — which the proof of H2 excludes for two levels.  So the useful version of this step is adversarial
   testing of H3 at three levels on product instances `outer × middle × inner` built from {flat, cone, flattened cone,
   critical bump}, by exact evaluation of the algorithm's cost with binomial formulas at `n ~ 10^4` (no simulation).


---

## Appendix: files in this directory

`REPORT.md` (this file); `hlib.py` (formulas); `verify_N1.py`, `verify_N234.py` (N1–N4); `radial_alg.py` (Theorem H1);
`two_level_sim.py` (algorithm 2L of Theorem H2); `ml_recursion.py`, `close_argmax.py` (recursions of §2.7–2.8);
`hint_additive.py`, `plateau_explore.py` (§2.9); outputs `out_*.txt` (the `out_ml_recursion_v*.txt` files are superseded,
see §2.8 and §3).  Nothing inside `/home/user/MetricChain` was modified; no Lean was run.
