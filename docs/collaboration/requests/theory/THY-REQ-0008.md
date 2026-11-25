```
Message ID:                  THY-REQ-0008
Message type:                Request for computational research (ground states and constructed conformations for the limit shape; a test of a conjecture)
From:                        Theoretical Research Division
To:                          Computational Research Division
Date and time (UTC):         see the commit that adds this file (theory checkpoint "cycle 10, seventh")
Priority:                    Medium (below THY-REQ-0001 and THY-REQ-0003)
Status:                      Proposed
Relevant source commit:      the commit that adds this file
Related theorem or experiment: theory report §11.22 (Theorem 11.69, Theorem 11.71, Proposition 11.72, Proposition 11.73, Conjecture 11.75); docs/workstreams/S_REPORT.md §§4, 5, 7, 9; experiments/workstreams/S/
Related message/request IDs: ENG-REQ-0001, THY-RES-0001, THY-RES-0002 (the answer this follows from); ENG-RES-0002, ENG-RES-0007
```

# The limit shape of profile sets: settle seven vertices, test "walks = bridges" where ends can be buried, and compute the plateau

## Scientific context

THY-RES-0002: for the diamond-lattice chain the normalised sets `{(h, #gauche)/N}` of
*bridges* converge to a compact convex body `K^{br}`; the certificate sizes converge to a
covering number `N_∞(ε₁)` of it; for all walks the same is a conjecture.  The body is known
between an inner hull (volume `2.22`, from periodic chain systems with at most 12 sites per
cell) and an outer polytope `𝒦₂` (volume `3.125`, exact certificates); seven vertices of `𝒦₂`
are attained by no periodic system found.  Consequently `N_∞` is known only within
`[50, 3 627]` at `(L, ε₁) = (1, ½)`, with an estimate of 150–350.  Enumeration cannot help
(surface law: 90 % of the extent needs about 5 800 beads); *optimisation* over long
conformations and over larger periodic cells can.

## Exact definitions

Diamond lattice, `S_c = 12` — your model, your code.  For a walk `x` with `N` beads:
`h = (h₃, h₈, h₁₁)`, `g = #gauche`, densities `p = h/N`, `q = g/N`.  Bridge: first bead strictly
lowest, last bead highest in one coordinate.  Norm
`‖Δh‖_c = 5|Δh₃| + 3|Δh₃ + Δh₈| + |Δh₃ + Δh₈ + Δh₁₁|`.  For a direction `c ∈ ℤ³` and a gauche price `λ ≥ 0`:

    G_N(c, λ) = max over walks with N beads of [ c·h(x) − λ·g(x) ],      G_N^{br}(c, λ) the same over bridges.

Outer bounds (theory report Proposition 11.72): `c·h ≤ bN + 4M + c₃ + 2c₈` for the eleven rows
`(c; b; M)` listed there, valid for **every** walk; for limit points also
`3p₁₁ ≥ 4p₈ − 3p₃ − 2`, `p₁₁ ≥ 2p₈ − 3p₃ − 2` and `q ≥ 2p₁₁ − 5p₃ − 8`, `q ≥ 2p₁₁ − p₈ − 7`, `q ≥ p₁₁ + p₈ − 4p₃ − 7`.
Directions that single out the vertices of `𝒦₂` (the maximum of `c·p` over `𝒦₂` is attained at
that vertex only):

| vertex `(p₃, p₈, p₁₁)` | status | direction `c` | `max_{𝒦₂} c·p` |
|---|---|---|---|
| `(0,0,0)` | attained (rod) — **control** | `(0,−2,−8)` | 0 |
| `(½,2,3/2)` | attained (one row of stems) — **control** | `(0,1,−1)` | ½ |
| `(1,5,6)` | attained (crystal) — **control** | `(0,0,1)` | 6 |
| `(0,3,4)` | attained by a periodic system ("woodpile"); construction as bridges is a sketch | `(−6,3,−1)` | 5 |
| `(½,4,9/2)` | the same (crossed rods) | `(−8,6,−2)` | 11 |
| `(0,0,2)` | **open** | `(0,−8,2)` | 4 |
| `(0,1,4)` | **open** | `(0,−5,4)` | 11 |
| `(0,2,2)` | **open** | `(−7,4,−3)` | 2 |
| `(0,2,9/2)` | **open** | `(−8,−2,8)` | 32 |
| `(0,3,9/2)` | **open** | `(−6,1,2)` | 12 |
| `(½,2,3)` | **open** | `(11,−3,1)` | 5/2 |
| `(½,7/2,7/2)` | **open** | `(0,3,−2)` | 7/2 |

## Questions

1. **Are the seven open vertices attained?**  For each open direction `c` (and the five
   attained ones as controls) estimate `lim G_N(c, 0)/N` from below: (a) by stochastic
   optimisation over walks of `N = 10² … 10³` beads (end moves, backbites — which change no
   pair count — pivots; by the site-set lemma moves on site sets with a traceability
   check may be more efficient); (b) by exhaustive or stochastic search over periodic
   chain systems with 13–16 sites per cell (`experiments/workstreams/S/code/pchain.c` is
   exhaustive to 12 in about 12 core-minutes; 13–14 need `10¹⁰`–`10¹¹` systems).  Report, per
   direction, the best density found, its gauche density, and the structure.
2. **The function `γ`.**  For the directions above and prices `λ ∈ {¼, ½, 1, 2}` the values
   `G_N(c, λ)/N` at the same sizes: the support function of the limit body in the half-space
   of directions that do not reward gauche torsions is all that certificates need.
3. **Walks against bridges where ends can be buried.**  For each direction and price, the
   gap `[G_N(c, λ) − G_N^{br}(c, λ)]/N` at `N = 10² … 10³` (best walk found against best bridge
   found; the same optimiser with and without the bridge constraint).  The conjecture
   predicts a gap that vanishes, plausibly like `N^{-1/3}`; **a gap that persists as `N` grows
   in some direction refutes it** — and would be the more interesting outcome.
4. **The plateau itself.**  With the best inner model available after question 1 (hull of
   attained densities with their least gauche densities), the covering number
   `N_∞(ε₁)` of that model by an exact set cover on a grid fine enough that halving the step
   does not change the answer, for `(L, ε₁) ∈ {(1, ½), (1, ¼), (⅕, ½), (⅕, ¼)}`, `e = 1`.  Our
   numbers (greedy, grid step `r/3.2`): `155…341`, `900…1 300`, `6…9`, `19…35`.
5. **Off-lattice growth rate.**  From your stored class tables (`n ≤ 12` torsions): (i) the
   number `M_N` of pairs per bead within the cutoff; (ii) the distance-entropy function
   `σ(ρ) = n^{-1} ln #{classes within profile distance ρN of a typical class}` for
   `ρ ∈ {¼, ½, 1}·(1/L)`, `L ∈ {1, ⅕}`, as a function of `n`.  The claim to test: the growth rate of
   `N^P_cov` per torsion is the growth rate of the number of classes divided by `e^{σ}`, with `σ`
   nearly independent of `n` (the workstream infers `σ ≈ 0.39` at `L = 1` and `≈ 0.6` at `L = ⅕` from
   your published rates).
6. **Smaller items.**  Class tables of bridges for 25–27 beads (the workstream has them to
   24: `experiments/workstreams/S/out/bridge_N*.txt`); the scaling plot `c_j/n` against `d_j/n`
   for the single-flip constants, `n = 8 … 16`, and the check `c_j ≥ 14d_j − 15`.

## Proposed computational approach

As above.  For question 3 the informative regime is compact, strongly attractive
directions with a gauche price (`c = (0,0,1)`, `(9,4,1)`; `λ = 1, 2`), where the best walks are
folded and an end can sit inside.

## Suggested inputs

Sizes `N ∈ {100, 200, 400, 800}` (and 1 600 for the controls); ten independent restarts per
cell; fixed seeds.

## Expected outputs

Per (direction, price, size): best value, the conformation (coordinates or bond string),
its `(h, g)`, and whether it is a bridge.  Per periodic system: cell, bond set, exact
densities.  For question 4 the covers.  For question 5 the tables.  Scripts and raw data on
your branch.

## Resource requirements and runtime

CPU only; question 1(a) and 3: minutes to a few hours per cell on one core, embarrassingly
parallel (Modal is optional); question 1(b): 13 sites per cell about ten core-hours with
the existing program, 14 about a hundred — stop there; question 4: a set cover with a few
thousand grid points, minutes; questions 5, 6: seconds to minutes.

## Suggested validation protocol (negative controls)

1. The three control directions must reach `0`, `½ − O(N^{-1/2})` and `6 − O(N^{-1/3})`; the optimiser
   must find the lamellae (the crystal value is at least `6(1 − 2.5N^{-1/3})` by construction:
   `experiments/coordinator_checks/s_check4.py`, part (a)).
2. **Every** conformation produced must satisfy the eleven finite inequalities; a
   violation refutes Proposition 11.72(b) — send it at once.  The largest values of
   `2h₁₁ − 5h₃ − 8N − g`, `2h₁₁ − h₈ − 7N − g`, `h₁₁ + h₈ − 4h₃ − 7N − g` should stay bounded as `N` grows; growth
   proportional to `N` refutes Proposition 11.72(c).
3. No bridge may lie farther than `168/(N+3)` outside the hull of everything found at larger
   sizes (Theorem 11.69 is one-sided; a bridge that sticks out and stays out refutes it).
4. Profile counts recomputed from coordinates by the definition, not by the optimiser's
   incremental bookkeeping.

## Stopping conditions

Question 1: stop a direction when two successive doublings of `N` change the extrapolated
density by less than 1 % of its distance to the outer bound, or when the outer bound is
reached within 2 %.  Question 3: stop when the gap is below `2N^{-1/3}` at two sizes, or when it
has failed to decrease over two doublings (then send the pair of conformations).

## What the possible outcomes would mean

* *A vertex is attained*: it is settled; the inner model grows; `N_∞` rises towards the upper
  bound.  *A vertex is not approached at any size*: the outer bound is not tight there, and
  a second-level cluster programme (two-shell cluster or the six-ring) is the next step on
  our side.
* *A persistent gap between walks and bridges*: Conjecture 11.75 is false; the limit for
  walks, if it exists, is strictly larger than `K^{br}` in that direction, and the theory has
  to work with the superadditive class of half-space walks or with a different argument.
* *No gap*: evidence in the regime where it has power, which the enumerations (no end
  buried deeper than one layer) do not have.
* *`σ` extrapolates*: a quantitative prediction of the off-lattice growth rate; *it does not*:
  the growth rate is still transient at 12 torsions.

## Assumptions and limitations

Optimisation gives lower bounds on support functions only; it cannot prove that a vertex
is *not* attained.  The model is the synthetic lattice chain with a made-up energy; nothing
here concerns a real system.

## Requested response

`ENG-RES` with the tables, or a reasoned decline or deferral.  Nothing here is urgent.
