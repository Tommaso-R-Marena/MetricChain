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
