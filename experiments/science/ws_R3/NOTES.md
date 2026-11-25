# Workstream R3 — adversarial referee of `docs/science/INFERENCE_LIMITS.md` (v2) — running notes

Started 2026-11-25 18:12 UTC.  Rules read (COMMON.md, R3_brief.md).  I write only here and in
`docs/science/workstreams/R3_REPORT.md`.  No git state changes.  No subagents.

## Step log

* 18:12 — created directory; read COMMON.md and R3_brief.md.  Next: read the note itself
  (statements first; attempt proofs independently before reading the author's proofs).
* 18:25 — read the note (v2, 544 lines), SCI-MSG-0001, SCIENCE_TO_ALL, experiments/science/README,
  theory report §11.6 (Thm 11.12 + remark), §11.10 (11.22–11.26), §11.16 (11.43–11.46),
  §11.18 (11.51–11.54), §11.19 (11.55–11.58 statements + table), §11.22 (11.67–11.75).
  Author's scripts NOT yet opened (own code first).

## First-pass independent derivations (before re-reading the given proofs line by line)

(Notation: sigma = 1/(1+e^-b), tau = tanh(b/2) = 2 sigma - 1, t = floor(k/2).)

* Lemma 1: re-derived (coset decomposition; projection of a linear code is onto F_2^S iff no
  dual word supported in S).  Correct.  Codes paragraph: BCH(2^m-1, designed 2t+1) dimension
  >= n'-mt [K]; dual of a punctured code = shortened dual, a subcode of C^perp, so dual distance
  survives restriction to ANY coordinate subset; 2^m <= 2n for m = ceil(log2(n+1)).  Degenerate
  case 2t+1 > n' (BCH = {0}, C = everything): bound 2^{n'} <= 2^{mt} still holds.  So
  |C| <= (2n)^{ceil(k/2)} is right for all n >= 1, k >= 0.  NOT optimal for odd k (extended BCH
  gives 2(2n)^{(k-1)/2}); to check numerically.
* Thm 2 (a)-(e): re-derived; all correct.  nu_{C,b'} in class b for b' <= b: yes (cone monotone in b).
  Caveat: (e) is vacuous unless n(ln2 - h(sigma(b))) > ln|C| (e.g. b^2 n/8 > (k/2) ln 2n).
* Thm 3: re-derived via E f^2 = M_t and Markov.  Correct.  "F_t>0 on [0,r]" is not needed for the
  inequality.  It is the 2t-th-moment tail bound for sums of k-wise independent signs with a
  better polynomial (constant t! instead of (2t-1)!!).  EXACT value is a Krawtchouk LP in the
  distance distribution (n+1 variables) -> compute.
* Thm 4: re-derived; correct (zero known part essential; alternatives all in class; oracle
  answers deterministic functions of g).  Accuracy convention differs from theory report by 2.
* Thm 5 + Corollary: correct (McDiarmid constant right, one-sided).  At g=0 even ONE evaluation
  + datum gives width O(b sqrt n).
* Prop 5b: mechanism right; exact root needed; adversary may tune s per centre.  ONLY bounded
  accuracy (eps < (1/2) ln 2).  Summary table of §0 drops this.  Idea: exact identity
  sign(U'-U0) = sign(D_s/E_s - U0); for disjoint supports the root exists in (-1,0) as soon as
  W/2^n > e^u r1 -> full proof when rho_0 < 1/4, i.e. u > ~2.46.  To verify numerically.
* Prop 6: correct [K].  Thm 7: correct; SHARPER: TV <= tanh(beta omega/4) using the sharp
  Jeffreys-vs-TV inequality J >= 2 TV ln((1+TV)/(1-TV)); exactly attained with no feature.
* §7 example: correct but trivial (B is a single state, where g = -d(y,.) is the closed form).
* §8 third format: re-derived from Farkas; signs correct.  Thm 8 (a)-(c) correct.
* Prop 9: correct mathematically; physical reading (start at beta=0, "how absolute entropies are
  measured") is off: absolute entropies are measured from T -> 0 (third law), not from T = infinity.
* §11.3: conv is 1-Lipschitz for Hausdorff distance, sections converge at interior points of the
  projection (epi-convergence of convex functions) IF int(K-projection) nonempty; statement is
  for BRIDGES; for walks conditional on Conj. 11.75; bold sentence drops both qualifiers.
* Overstatements spotted so far: §0 row 1 ("nothing about the entropy" - only at uniform data);
  Thm 3 reading "populations ... identified up to polynomial factors" (false: only the upper end);
  §0 row "I1+I3 worst-case exponent unchanged" (bounded accuracy only, root [N]);
  SCI-MSG §4 title and "Why it matters" ("in a first-order class").
* Candidate "theorem within reach": (A) theta_na unchanged by the k-body oracle (C-symmetrised
  cones; drop >= D_R when balls disjoint: two-line proof); (B) joint oracle I1+I2(k)+I3 at
  bounded accuracy via C-symmetrised visible basin + C-symmetrised twin.

## Numerics log

* 18:40 `r3_codes.py` (own GF(2)/BCH code; output `r3_codes.out`).  For every n <= 31, every
  k <= n, two coordinate choices (first n; random n-subset of 2^m-1): dual of BCH(t=ceil(k/2))
  punctured to n coordinates has EXACT dual distance > k (brute force / MacWilliams) and
  |C| <= (2n)^ceil(k/2); 0 failures; max of ln|C| - ceil(k/2) ln 2n is exactly 0 (n = 2^(m-1)).
  => the "Codes" paragraph is right, also for k odd, k near n, tiny n.  Extended-BCH duals:
  dual distance 2t+2 at size 2(2^m)^t, so for odd k the bound can be improved by a factor ~n:
  |C| <= 2 (2n)^((k-1)/2).  Puncturing can destroy the MINIMUM distance of C itself
  (simplex[15,4,8] on 8 well-chosen coordinates has a word of weight 1) - harmless for the
  note (d_min(C) is never used), relevant for any sharpening.
* 18:55 `r3_thm2.py` (output `r3_thm2.out`): Theorem 2 replicated exactly on codes the author did
  not use: [15,8,4] = dual of BCH(15,2) (k=4) and extended Golay [24,12,8] (k=7), b in
  {0.5,1,2,4} resp. {1,2,4}; both nu_{C,b} and the variant exp(-b d(x,C)); full-cube
  Walsh-Hadamard transform: every Fourier coefficient of order 1..k is 0 (exactly), order k+1
  equals tau^(k+1) for the mixture; all single-flip ratios <= e^b; entropies inside (c);
  (d) on 3200 random class members + adversarial descent: min of S - n h = -3e-15.
  OBSERVATION (matters for the reading): the upper end of (c), n h + ln|C|, EXCEEDS n ln 2 in
  many of these cases (Golay b=1: 22.29 > 16.64; b=2: 17.09 > 16.64), so there the check is
  vacuous and the "ordered" ensemble is in fact almost uniform (Golay, b=1: n ln2 - S = 0.0014).
  By the same arithmetic 9 of the author's 16 cases ([7,3],[15,4],RM(1,3),RM(1,4) at b=0.5,1 and
  RM(1,3) at b=2) test an inequality implied by S <= n ln 2.  The theorem has content only when
  n (ln 2 - h(sigma(b))) > ln|C|.
* Idea worked out on paper (to be checked numerically): for MIXTURES nu_pi = sum pi(a) P_a with
  pi k-wise uniform, S(nu_pi) - n h(sigma) = I(Z;X) >= -ln E kappa^{d(Z,Z')}, kappa = 1/cosh(b/2)
  (variational decoder bound + Jensen), and E kappa^{d(a,Z')} <= pi(B(a,r)) + kappa^(r+1)
  <= M_t/min F_t^2 + kappa^(r+1) by Theorem 3 applied to pi.  Hence
  S >= n h(sigma) + t ln n - ln t! - o(1): Theorem 2 is sharp (even k: up to O_k(1)) within
  mixtures of polarised basins.  Full cone class: open.
* 19:20 `r3_thm3.py` (output `r3_thm3.out`).  Theorem 3 replicated and placed: (i) exact-integer
  identities E_unif F_t^2 = M_t, deg = 2t, F_t(d) = K_t^(n-1)(d-1) hold; E_mu f^2 = M_t checked on
  a 4-wise uniform measure that is NOT invariant under a single code (mixture of cosets of two
  permuted [15,8] codes): 1e-14.  (ii) EXACT optimum (Krawtchouk LP in the distance
  distribution; own formulation) vs the bound vs attained, on [15,8,4] k=4, Golay24 k=7,
  [31,10,12] k=4, [31,15,8] k=6, RM(1,5) k=3: attained <= LP <= bound in every row; all centres
  (all cosets) for [15,8] and Golay.  (iii) bound * n^t (1-2rho)^{2t}/t! -> 1 (n = 1e2..1e5) -
  the asymptotic claim is right; at finite n the hypothesis F_t > 0 on [0,r] fails close to n/2
  (first non-positive radius is n/2 - 4, -8, -11 for t = 2,3,4 at n=100) and the constant is far
  from 1 there (t=2, rho=0.45, n=100: 20.9x).  (iv) LP/bound -> 1 as n grows (0.98-0.995 at
  n=400): among ALL k-wise uniform measures the bound is asymptotically exact (Christoffel-function
  reading: f = reproducing kernel of polynomials of degree <= t).  (v) the plain 2t-th moment
  bound is weaker at small r by (2t-1)!!/t! but BETTER than Theorem 3 near the first root
  (Golay r=8: moment 0.727 vs Thm-3 5.27; exact LP 0.186).  (vi) odd k: Golay attains 1/4096 = LP
  optimum at r=0 while the note's bound gives 1/2325 (Rao's odd-strength bound 2 M_t(n-1) is
  what is tight); RM(1,m) attains 1/(2n) for k=3 against 1/(n+1): "attained up to constants" is
  true for odd k only with the extended code, not with the note's (2n)^ceil(k/2) code.
* 19:35 `r3_prop5b.py` (output `r3_prop5b.out`).  Prop 5b: own exact sums over the joint law of
  the two distances (log domain; root of D_s - U0 E_s).  With INTEGER r1 = round(rho1 n) the
  note's numbers are reproduced: n=1000: s* = -0.00490, ln Z'-ln Z0 = 0.6907; n=5000:
  s* = -0.0393, 0.6737; independent of the distance of the hidden centre (0.3n, 0.45n, 0.5n) to
  all digits shown; equal mean energies to 1e-16 relative.  (With real r1 = rho1 n: -0.00549,
  -0.0256.)  "cost exponent 0.0281" is the asymptotic ln 2 - h(rho1); the finite-n value
  ln 2 - ln V(n, r1+1)/n is 0.0289.  s -> U'(s) - U0 is monotone (81-point grid), root unique.
  Root exists iff roughly B0 > |U0| (n >= 400 at rho1 = rho0+0.01, i.e. ln B0 >= 4): the note's
  "ln B0 <~ 2" is not the right criterion (it is ln B0 <~ ln(|U0|) ~ ln n).
  Referee's disjoint-support lemma verified (u = 2.6, 3, 4): U'(0) < U0 always; U'(-1) > U0
  whenever W/2^n > e^u r1; then root in (-1,0) and ln Z'-ln Z0 -> ln 2.
  JOINT ORACLE example, exact on the cosets of the Golay code (n=24, k=7): visible
  g0 = -u(r1 - d(x,C))_+, twin around a deep hole a'+C; u=5, r1=3: s* = -0.005574, U' = U0 to
  machine precision, ln Z' - ln Z0 = 0.678, all marginals of order <= 7 uniform for both.
