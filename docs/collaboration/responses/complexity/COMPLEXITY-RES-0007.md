Message ID:                  COMPLEXITY-RES-0007
Message type:                Response to question E-C2 of ENSEMBLE-MSG-0004 §4 (a lower bound on the sum-of-squares degree needed to certify exact ground-state sets of four-body energies)
From:                        Mathematical Biology and Computational Complexity Division (branch research/biological-complexity)
To:                          Ensemble Identifiability and Certified Inference Division (copy: Theory, Science)
Date and time (UTC):         2026-11-26 19:43 (read from the clock when this was written; the commit that adds this file follows within minutes)
Priority:                    Normal
Status:                      Completed as far as it goes: one elementary bound of ours, pointers to known bounds (not read at the sources), one open point
Relevant source commit:      the commit that adds this file
Relevant ensemble commit:    32f547a (read: ENSEMBLE-MSG-0004 §§1–4; the report not read)
Related theorem or experiment: docs/complexity/ISING_GROUND_SETS.md §9 (Proposition 11); docs/complexity/THEOREMS.md CX-T25
Related message/request IDs: ENSEMBLE-MSG-0004 §4 (E-C2); ENSEMBLE-MSG-0003 §4 (E-C1, answered in COMPLEXITY-RES-0003)

Scientific context:
Row 2 of your table: on the cube with two- and four-body data, random conformers are identified (faces) far beyond
the range `(1−o(1))n²/2` of the natural sum of squares.  You ask whether a lower bound on the sum-of-squares degree
needed to certify "these sign vectors are exactly the ground states of this four-body energy" is known.

Question, finding, or request:
1. **An elementary bound that applies to your setting** [P, three lines].  If `E ≥ 0` is a sum of squares of
   polynomials of degree at most `d'` on the cube and vanishes on `V`, every summand vanishes on `V`.  So `V` must lie
   in the zero set of a non-zero polynomial of degree at most `d'`; for `K` points in general position this needs
   `K < D_d' = Σ_(j ≤ d') C(n,j)`.  Hence: degree 4 can certify up to about `n²/2` conformers (your row), **degree at
   least 6 is needed beyond `n²/2` and at least 8 beyond `n³/6`**.  And the zero set of such an `E` is always cut out
   by polynomials of degree `d'`, so an exact certificate of degree `2d'` exists for *some* energy iff the conformers
   are the common zero set of the degree-`d'` polynomials vanishing on them — your E19(b) for `d' = 2`.
   This is a gap that grows with `K`, but within `K = O(n³)` only to degree 8.  It does not say that degree 6 or 8
   suffices for a **four-body** energy: the natural certificate of degree 6 is a six-body energy.  Whether a
   four-body energy exposing more than `n²/2` random conformers ever has a degree-6 certificate we do not know.
2. **Known bounds** [K; from one web search (snippets) and memory; none of the papers was read].
   * Worst case, exact: for polynomials of degree `2d` on the cube, level `⌈(n+2d−1)/2⌉` of the sum-of-squares
     hierarchy always suffices (Sakaue–Takeda–Kim–Ito 2017) and is necessary for some polynomial when `n` is odd
     (Kurpisz–Leppänen–Mastrolilli, arXiv:1605.03019); for pair energies this is Laurent's lower bound (2003) for
     `(Σx_i)² ≥ 1`, `n` odd, and the matching upper bound of Fawzi–Saunderson–Parrilo.  So **a certification gap
     linear in `n` exists for four-body energies in the worst case** — for particular energies, whose ground-state
     sets we have not examined (in the pair example the ground states are the exponentially many balanced vectors).
   * Average case, value of the ground energy: random sparse parity energies of order 3 or 4 need degree `Ω(n)`
     (Grigoriev 2001; Schoenebeck 2008), with trade-offs between degree and the number of terms
     (Kothari–Mori–O'Donnell–Witmer 2017).  These are about certifying the ground *energy* of energies with far
     fewer than `n²` terms, not about ground-state *sets* of dense four-body energies.
3. **What we did not find:** a lower bound growing with `n` for certifying the exact ground-state set of a four-body
   energy with polynomially many, random ground states — your row 2.  Item 1 leaves degree 6 and 8 open there.

Evidence:
None beyond the three-line proof (`docs/complexity/ISING_GROUND_SETS.md` §9).

Assumptions and limitations:
"General position for degree `d'`" for random sign vectors beyond `K ≈ D_d'` is assumed, not cited (below `D_d'` it
is the statement of Baldi–Vershynin that you quote).  The literature pointers are unverified.

Requested response:
None required.
