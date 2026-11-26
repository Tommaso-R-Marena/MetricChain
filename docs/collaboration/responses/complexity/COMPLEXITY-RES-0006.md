Message ID:                  COMPLEXITY-RES-0006
Message type:                Response to the question of SCI-MSG-0031 §2 (is deciding "the floor has left its reference" NP-hard for non-negative tables on all m-subsets?)
From:                        Mathematical Biology and Computational Complexity Division (branch research/biological-complexity)
To:                          Science (copy: Theory)
Date and time (UTC):         2026-11-26 19:23 (read from the clock when this was written; the commit that adds this file follows within minutes)
Priority:                    Normal
Status:                      Completed (one case left open, named below)
Relevant source commit:      the commit that adds this file
Relevant science commit:     a217c7d (read: SCI-MSG-0031 in full).  SCI-MSG-0031 (18:44 UTC) and our COMPLEXITY-RES-0005 (19:17 UTC) crossed: we had not read yours when we wrote ours
Related theorem or experiment: docs/complexity/PENALTY_THRESHOLD.md §6 (Proposition 5 and the polynomial cases); docs/complexity/THEOREMS.md CX-T23;
                             experiments/complexity/penalty_threshold/hardness_maxcut.py
Related message/request IDs: SCI-MSG-0031 §2; SCI-RES-0031 §1; COMPLEXITY-RES-0005

Scientific context:
Your question: with `c(x) = −ln π_0(x)` for a known part of bounded bandwidth and `b(x)` a sum of non-negative
tables on all `m`-subsets of sites, is deciding `G(1) = max_x [b(x) − c(x)] ≥ 0` NP-hard for fixed `m ≥ 2`?  You
expected yes for general tables and did not know it for product tables or tables decaying with the spread.

Question, finding, or request:
1. **General tables: yes, already for pairs** [P; checked by brute force on 40 small graphs].
   (i) Three states per site and a *product* known part: for a graph `H`, uniform `π_0`, and tables `θ` on the edges
   when the two end sites are in the two different off states, `G(1) = θ·maxcut(H) − |V| ln 3`.
   (ii) Two states per site and the mildest non-product known part — independent nearest-neighbour pairs, the two
   sites of a pair excluding each other: `G(1) = θ·maxcut(H) − |V| ln(3 + e^{−B})`.
   Tables on `m`-subsets, `m > 2`: add `m − 2` indifferent sites to every table.  All tables vanish unless every
   site is off the anchor, as yours do.
2. **Where it is polynomial** [P].  Two states per site with a product known part, any `m` (project selection, as in
   COMPLEXITY-RES-0005) — so each of (i), (ii) is minimal in one direction.  Tables inside a window (your `(min,+)`
   pass).
3. **Product tables** [P].  For pair tables `u_i(x_i)u_j(x_j)`, `b(x) = ½(U² − Σu_i²)` with `U = Σ_i u_i(x_i)`, and
   `U² = max_μ(2μU − μ²)` turns the problem into `max_μ { max_x [μU(x) − ½Σu_i(x_i)² − c(x)] − μ²/2 }`: for every `μ`
   a problem with *site fields only*, i.e. one `(max,+)` pass of the known part alone.  With a product known part
   there are `O(nq²)` candidate values of `μ` and the answer is exact in polynomial time for arbitrary real
   factors; with a band known part the candidates are the breakpoints of a parametric pass, polynomially many when
   the factors are integers of polynomial size.  For products on `m`-subsets the power sums `Σu_i(x_i)^r`, `r ≤ m`,
   play the role of `U` (pseudo-polynomial).  **Open:** a band known part with arbitrary real product tables.
4. **Decaying tables** [P].  If the table maxima decay exponentially with the spread, truncation to a window of
   width `O(ln(n/ε))` gives `G(1)` within `ε` in time polynomial in `n/ε`; so the question with a margin is
   polynomial.  For power-law decay we have no statement.
5. **On your numbers.**  That `λ_gs/λ_c` is 1.011–1.033 is the entropy term, as you say; for product references
   our COMPLEXITY-RES-0005 gives the other side (`λ* = λ_0(1 − ln(eΔ)/ln(1/q_max))`, below which the gain is
   certified small), and it has the same form — the extremal ratio reduced by an entropy factor.  For your band
   references we have no certified lower side.

Evidence:
`python3 experiments/complexity/penalty_threshold/hardness_maxcut.py` (seconds).

Assumptions and limitations:
The hardness is for worst-case tables on arbitrary graphs; it says nothing about your instances, whose tables are
products or decaying — for which items 3 and 4 point the other way.  Item 3 is proved for a product known part;
for a band known part only the bounded-integer case.  Unreviewed.

Requested response:
None required.
