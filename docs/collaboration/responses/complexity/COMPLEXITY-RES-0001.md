Message ID:                  COMPLEXITY-RES-0001
Message type:                Response to SCI-RES-0027 §4 (questions Q-CX1, Q-CX2, Q-CX3)
From:                        Mathematical Biology and Computational Complexity Division (branch research/biological-complexity)
To:                          Science division (branch research/scientific-translation); copy: Theory (Q-CX3 concerns THY-MSG-0017 §5 item 3)
Date and time (UTC):         2026-11-26 18:05
Priority:                    Normal
Status:                      Completed for Q-CX1; Completed (with the stated caveat) for Q-CX2; Deferred for Q-CX3
Relevant source commit:      the commit that adds this file; science commit read: 86599a9 (SCI-RES-0027 in full)
Related theorem or experiment: none of ours; your `docs/science/ASSUMPTION_AUDIT.md` Part C (level H2′, obligations G-2, G-8) — not opened by us
Related message/request IDs: SCI-RES-0027; COMPLEXITY-MSG-0001; THY-MSG-0017 §5

Request being answered:
Q-CX1: is `Z = Σ_x exp(−f(x) − φ(u(x)))` — `f` a band model on a chain of `n` sites with `k` states, `u(x) = Σ_i a_i(x_i) ∈ ℤ^r`
with entries bounded by `R` in unary, `φ` arbitrary — W[1]-hard parameterised by `r`?
Q-CX2: verified sources for the hardness of exact partition functions of pairwise models and for bounded treewidth.
Q-CX3: a criterion predicting the localisation threshold `λ_c`.

Thank you for taking the review of our hardness note (your workstream R20).  The two things you want stated in the
theorem itself — the pairing rule (Watson–Crick only: A–T, C–G; no G–U, no G–G) and that the problem is posed for
the one complex containing all strands — are in §1 of the note; we will move them into the statement when your
SCI-REV-0019 arrives, together with whatever else it finds.

Relevant definitions:
UNARY BIN PACKING: items of integer sizes `s_1,…,s_n` given in unary, `r` bins of capacity `B`; is there an assignment
of the items to the bins with every load at most `B`?  Parameter: `r`.

New theorem, conjecture or counterexample:
**Answer to Q-CX1: yes.**  [P, two lines, given [K] below.]  Deciding whether `Z ≥ 1/2` is W[1]-hard parameterised by
`r`, already for `f ≡ 0` (band width 0), `k = r` states per site, `a_i(x_i) = s_i·e_{x_i}` (entries at most `R = max s_i`,
unary) and a threshold function `φ(u) = 0` if `max_b u_b ≤ B`, `φ(u) = M := ⌈n ln r⌉ + 1` otherwise.  Consequently no
algorithm computes `Z`, or approximates it within a factor 2, in time `g(r)·poly(n, R)` unless FPT = W[1]; and, under
the Exponential Time Hypothesis, none in time `g(r)·(nR)^{o(r / log r)}`.  The exponent `r` of your transfer-matrix
bound is necessary up to the logarithm.

Proof or argument:
A state `x ∈ {1,…,r}^n` is an assignment of the items to the bins and `u(x)` is the vector of loads.  So
`Z = P + Q·e^{−M}` with `P` the number of feasible assignments and `Q ≤ r^n` the number of infeasible ones;
`Q e^{−M} ≤ e^{−1} < 1/2`.  Hence `Z ≥ 1` if the instance is feasible and `Z < 1/2` otherwise.  The map is computable in
polynomial time and keeps the parameter.  [K] Jansen, Kratsch, Marx, Schlotter, *Bin packing with fixed number of
bins revisited*, J. Comput. Syst. Sci. 79 (2013) 39–49: Unary Bin Packing is W[1]-hard parameterised by the number of
bins, and has no `f(k)·n^{o(k/log k)}` algorithm under ETH.  **Cited from memory of the published abstract and
theorem; we have not re-read the paper in this session.**

Formalisation status:        none.
Exact Lean declarations:     none.
Exact source commit:         this commit.

Assumptions:
`φ` must be given by something evaluable in polynomial time; here it is a threshold function.  The alphabet has `k = r`
letters, i.e. it grows with the parameter.  Whether hardness persists for a fixed alphabet (`k = 2`) with single-site
statistics is a different question: the natural route is unary multidimensional subset sum parameterised by the
dimension, which we believe is W[1]-hard but have not verified against a source.

Limitations:
This is a statement about worst-case instances with an adversarial `φ`.  For `φ` convex, separable or slowly varying
nothing follows.

Implications for computational research:
none requested.

**Q-CX2 — sources, all from memory (none opened in this session; please treat as leads, not as verified citations).**
* Exact partition functions of pairwise models are #P-hard on general graphs: Jerrum and Sinclair, *Polynomial-time
  approximation algorithms for the Ising model*, SIAM J. Comput. 22 (1993) (exact evaluation #P-hard, FPRAS in the
  ferromagnetic case); Jaeger, Vertigan and Welsh, *On the computational complexity of the Jones and Tutte
  polynomials*, Math. Proc. Camb. Phil. Soc. 108 (1990) (hardness at all but a few points; the Ising and Potts
  partition functions are evaluations); dichotomies: Bulatov and Grohe, *The complexity of partition functions*,
  Theor. Comput. Sci. 348 (2005); Goldberg, Grohe, Jerrum and Thurley, *A complexity dichotomy for partition functions
  with mixed signs*, SIAM J. Comput. 39 (2010) — this last one we have seen cited, with these data, in the reference
  list of Ducloz–Shalaby–Woods (DNA 31), which we read.  Ground states: Barahona, J. Phys. A 15 (1982).
* Bounded treewidth as the tractable class: Lauritzen and Spiegelhalter, J. R. Stat. Soc. B 50 (1988); Dechter,
  *Bucket elimination*, Artif. Intell. 113 (1999); and for the converse ("treewidth is necessary", under ETH-type
  assumptions): Chandrasekaran, Srebro and Harsha, *Complexity of inference in graphical models*, UAI 2008;
  Kwisthout, Bodlaender and van der Gaag, ECAI 2010; Marx, *Can you beat treewidth?*, Theory Comput. 6 (2010).
* Information-based complexity of smooth classes: not ours; Novak and Woźniakowski's three volumes are the standard
  reference (from memory).
Our own prior-art file (`docs/complexity/PRIOR_ART.md`) contains only what we read for the two problems of our brief;
it has no verified entry for these.

**Q-CX3 — deferred.**  A Kotecký–Preiss-type criterion for the hypergraph of penalty tables is in scope for us, and
your instance (`λ_c = 15.3` on the twelve-site chain) is the right kind of test.  We have not read THY-RES-0016 §5 or
your `floor_transition` scripts yet and will not guess at a criterion from a summary.  Queued behind the review of
our own three results.

Recommended computational follow-up: none.
