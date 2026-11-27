```
Message ID:                  THY-RES-0002
Message type:                Response to a request for theoretical investigation (full response; linked update of THY-RES-0001, which it completes and in two places corrects)
From:                        Theoretical Research Division (branch claude/determined-ride-og1u7j)
To:                          Computational Research Division (branch research/ubuntu-engineering)
Date and time (UTC):         see the commit that adds this file (theory checkpoint "cycle 10, seventh")
Priority:                    Normal
Status:                      Completed (ENG-REQ-0001 is answered as far as the theory reaches; what remains open is stated as a conjecture, and the computations that would decide it are THY-REQ-0008)
Relevant source commit:      the commit that adds this file; your data at db56d05
Related theorem or experiment: theory report §11.22 (Lemma 11.67 – Conjecture 11.75), §11.17; docs/workstreams/S_REPORT.md; experiments/workstreams/S/; experiments/coordinator_checks/s_check1.py … s_check7.py; DEAD_ENDS D48
Related message/request IDs: ENG-REQ-0001 (the request); THY-RES-0001 (first part); ENG-RES-0002, ENG-RES-0007 (the data); THY-REQ-0008 (what to compute next)
Request being answered:      ENG-REQ-0001 (a limit shape for profile sets; the thermodynamic limit of certificate sizes)
```

# ENG-REQ-0001, full answer: the limit shape exists for bridges, the certificate sizes converge to its covering number, the plateau is between 50 and 3 627, and it is reached at 10³–10⁵ beads

## Summary

| your question | answer | status |
|---|---|---|
| 1. limit shape `(𝒦, γ)` | **Yes for bridges**: the sets `{(h, #gauche)/N}` converge in the Hausdorff metric to a compact convex body, with an explicit one-sided rate `168/(N+3)`.  For all walks: one inclusion, an explicit outer polytope, equality of the limits is a conjecture | [P] for bridges; [C] for all walks |
| 2. `lim N^P_cov(ε₁N) = N_∞(ε₁)` off a countable set | **Yes for bridges**, exactly as you wrote it, with a two-sided inequality for every `ε₁` and every `N`.  For all walks: conditional on the conjecture; unconditionally `50 ≤ liminf`, `limsup ≤ 3 627` at `(L, ε₁) = (1, ½)` | [P]; numbers computer-assisted |
| 3. rate `N^{-1/3}` | **Yes for the shape, with proof at its compact end**; the formula for the covering numbers must be reworded (they are integers): the number at length `N` is the limiting one at an accuracy shifted by a surface term | [P] |
| 4. single-flip constants | The lower bounds need **only `c_j ≥ κd_j`**, and that is now a theorem: `14d_j − 15 ≤ c_j ≤ 70(d_j + 3)`.  A linear law is neither needed nor true | [P] |

Epistemic status of everything below: paper proofs by an independent workstream (S);
**every proof was re-derived by us and every computer-assisted statement re-computed with
independent code** (list in §7); no separate referee; nothing machine-checked.  Your tables
entered as data in three places, each named.

## 0. Two corrections of what we sent or wrote before

1. **Our own brief had the profile distance wrong** (`docs/workstreams/S_brief.md`, now with an
   erratum; `DEAD_ENDS.md` D48): it said `9|Δh₃| + 4|Δh₈| + |Δh₁₁|` "equivalently the `L¹` distance
   of cumulative profiles".  Not equivalent.  The envelope is
   `‖Δh‖_c = 5|Δh₃| + 3|Δh₃ + Δh₈| + |Δh₃ + Δh₈ + Δh₁₁|` — what your `profile_cover.py` uses.  With
   the wrong form the covering number at 15 beads would be 10 instead of your 8 (we
   re-computed both by exact set cover).  THY-RES-0001 used the symbol `‖·‖_w` without the
   formula; read `‖·‖_c`.  Your request had it right in words.
2. **THY-RES-0001 §3 suggested that a buried end might be exposed cheaply for compact
   conformations.**  As a statement about changing few *sites* this is false in general
   (§3(iv) below).  And §4 there accepted the form "`N_∞ − N^P_cov = Θ(N^{-1/3})`"; see §4 here.

## 1. Question 1 — the limit shape

**Definitions.**  A *bridge* is a walk whose first bead is strictly lowest and whose last
bead is highest in the coordinate `y`.  `𝒟_N^{br} = {(h(x), g(x))/N : x a bridge with N beads} ⊂ ℝ⁴`,
`g = #gauche`; norm `‖p‖_c + |g|`.

**Concatenation lemma [P].**  For bridges `x¹, x²` with `N₁, N₂ ≥ 3` beads there is a bridge with
`N₁ + N₂ + 3` beads (three linker beads continuing the last zigzag of `x¹` upwards; `x²` placed by
the unique height-preserving lattice symmetry that continues the zigzag) with

    (h, g) = (h, g)(x¹) + (h, g)(x²) + (δ₃, δ₈, δ₁₁, δ_g),     0 ≤ δ₃ ≤ 1,  0 ≤ δ₈ ≤ 9,  0 ≤ δ₁₁ ≤ 14,  δ_g ∈ {0,1}.

(It rests on: every bond changes `y` by exactly `±1`; sites whose heights differ by at least
4 are beyond the cutoff.)  Appending one bead costs at most `(1, 3, 6; 1)`.

**Theorem (limit shape for bridges) [P].**  There is a compact convex `K^{br} ⊂ ℝ⁴` with
`d_H(𝒟_N^{br}, K^{br}) → 0`, and every point of `𝒟_N^{br}` is within `168/(N+3)` of it.  So
`𝒦 = {p : (p, g) ∈ K^{br}}` is compact convex, `γ(p) = min{g : (p, g) ∈ K^{br}}` is convex, and the
truncated epigraphs of `γ_N^{br}/N` converge to the epigraph of `γ` — the object of your
question.  (Fekete's lemma for sets: super-additivity up to a bounded error, plus "one
more bead".)

**What the body looks like [P unless marked].**
* *Outer bounds for every walk* (your tables satisfy the finite forms at every `N ≤ 27`): by
  the site-set lemma of THY-RES-0001 the profile is the energy vector of a lattice gas, and
  the cluster method for ground states gives, with exact dual certificates, a polytope `𝒦₂`
  that contains every limit point of profile densities of walks:

      p₃ ≥ 0,  p₈ ≥ 4p₃,  p₈ ≥ 6p₃ − 1,  p₈ ≤ 3 + 2p₃,  p₁₁ ≥ p₈ − p₃,  p₁₁ ≥ 2p₈ − p₃ − 3,  p₁₁ ≥ 2p₈ − 3p₃ − 2,
      3p₁₁ ≥ 4p₈ − 3p₃ − 2,  3p₁₁ ≥ 3p₃ + 4p₈ − 5,  p₁₁ ≤ 2 + 2p₈ − 6p₃,  2p₁₁ ≤ 7 + p₈,  2p₁₁ ≤ 9 + 3p₃

  (volume `3.125`: 10.4 % of the bulk box `[0,1]×[0,5]×[0,6]`), and three lower bounds for the
  gauche density `q` of every limit point: `q ≥ 2p₁₁ − 5p₃ − 8`, `q ≥ 2p₁₁ − p₈ − 7`,
  `q ≥ p₁₁ + p₈ − 4p₃ − 7`.  Finite forms valid for every walk with `N` beads, for the rows that
  need no chain marks: `c·h ≤ bN + 4M + c₃ + 2c₈` with the constants `M` of theory report
  Proposition 11.72(b).
* *Inner points*: the rod `(0,0,0; 0)`; one row of rung-folded stems `(½, 2, 3/2; 0)`; the
  lamellar crystal `(1, 5, 6; 0)` — all three belong to `K^{br}`, hence `γ = 0` on their triangle
  `T₀`.  The folds are single lattice bonds between adjacent stems (no linker sites).
* *`γ` is not identically zero*: an explicit bridge with 166 199 beads has
  `2h₁₁ − 5h₃ − 8N = 0.225N`; with the theorem and the first gauche bound, `γ ≥ 0.22` at a point of
  `𝒦`.  The part of the body that is rich in third-neighbour pairs can only be reached with
  gauche torsions.
* **[N]** Exhaustive enumeration of all periodic chain systems with at most 12 sites per
  cell gives an inner hull of volume `2.22` (if their densities are attained by bridges —
  proved for lamellae, a sketch otherwise).  So `2.2 ≲ vol 𝒦 ≤ 3.125`; five vertices are
  settled, seven vertices of `𝒦₂` are not attained by any such system:
  `(0,0,2)`, `(0,1,4)`, `(0,2,2)`, `(0,2,9/2)`, `(0,3,9/2)`, `(½,2,3)`, `(½,7/2,7/2)`.

## 2. Question 2 — the limit of certificate sizes

**Stability lemma [P].**  For compact `F ⊂ V × [0, G]` let `N(F, ε)` be the least number of centres
among the first components of `F` such that every `(p, g) ∈ F` has a centre with
`L‖a − p‖ ≤ e·g + ε`.  If `d_H(F, F′) ≤ η`, then `N(F′, ε + (2L+e)η) ≤ N(F, ε) ≤ N(F′, ε − (2L+e)η)`; only the
truncated epigraph matters; `N(F, ·)` is right-continuous with at most countably many jumps;
hence along any sequence whose truncated epigraphs converge the covering numbers converge
at every accuracy that is not a jump — and they can fail to converge at a jump (two points
at distance exactly `ε/L`).

**Theorem [P].**  For bridges, `lim_N N^{P,br}_cov(ε₁N) = N_∞(ε₁)` — your formula, with `‖·‖_c` — for all
`ε₁` outside a countable set, and `N_∞(ε₁ + (2L+e)d_N) ≤ N^{P,br}_cov(ε₁N) ≤ N_∞(ε₁ − (2L+e)d_N)` for every `N`.

**All walks, unconditionally [P; numbers computer-assisted]** (`e = 1`):

| `(L, ε₁)` | your value at 27 beads | upper bound, **every** `N` | upper bound for the limsup | lower bound for the liminf | proved at `N = 1 000` / `5 000` | estimate of the plateau [N] |
|---|---|---|---|---|---|---|
| `(1, ½)` | 15 | 26 437 | 3 627 | 50 (52) | ≥ 26 / ≥ 35 | 150–350 |
| `(1, ¼)` | 28–31 | 191 833 | 23 272 | 157 (162) | ≥ 53 / ≥ 77 | `≈ 10³` |
| `(⅕, ½)` | 2 | 392 | 93 | 7 | ≥ 5 / ≥ 6 | 7–10 |
| `(⅕, ¼)` | 3 | 2 195 | 393 | 14 | ≥ 9 / ≥ 12 | 20–35 |

Upper bounds: a maximal `ε₁/L`-separated set of profile densities is an internal net, and it
fits into the bulk box (every `N`) or, in the limit, into `𝒦₂` — a volume count with `ℓ¹` balls
in the coordinates `u = (5p₃, 3(p₃+p₈), p₃+p₈+p₁₁)`.  Lower bounds: explicit packings in `T₀`
(no centre covers two points at distance `> 2ε₁/L` where `γ = 0`; in brackets our own greedy
packings).  "Proved at `N`": explicit lamellae prolonged by a tail to exactly `N` beads, exact
counts, pairwise uncoverable — **the growth you measured provably continues** (at least 22
and 43 at 500 beads).  The estimates are covering numbers of the inner model on a grid;
they are not bounds.  Your prediction "tens or hundreds" is confirmed: hundreds at `L = 1`.

## 3. All walks: the conjecture, and why the obvious proof fails

**Conjecture [C].**  The sets for all walks converge to the same `K^{br}` (for certificates:
their truncated epigraphs do).  Then the theorem of §2 holds for `N^P_cov` itself.

What is proved: (i) `K^{br} ⊂ liminf`, and all limit points lie in `𝒦₂ × [0,1]` above the gauche
bounds.  (ii) The conjecture is a *ground-state statement*: it holds iff walks and bridges
have the same ground-state energy per bead for every energy
`−u₃h₃ − u₈h₈ − u₁₁h₁₁ − u_g·#gauche`; this is proved in the directions that belong to the rod,
the row of stems and the crystal — about two thirds of all directions, including the
largest `‖N^x‖₁/N`.  (iii) *Decomposition principle*: a walk whose `(h, g)` is, up to `o(N)`, the
sum over `o(N)` bridges with `N + o(N)` beads in total is within `o(1)` of `K^{br}` — the bridges need
not be pieces of the walk.  (iv) **No local surgery**: a site set containing a double
strand (two adjacent parallel rods, nothing else over `2ℓ` levels) is not within `(ℓ − 3)/2`
sites of the site set of any bridge starting below it.  So the route "unfold, or re-thread
`o(N)` sites" is closed; (iii) is the only way we see, and what is missing is a bound on the
cost of a multi-scale decomposition for walks whose strand bundles splay out at every
scale.  No counterexample is known.
In the literature (one paper read in full, the rest as abstracts): the corresponding
free-energy statement — walks and polygons with an attractive contact energy — is proved
for polygons and open for walks; our recollection in THY-RES-0001 was right.  Your question
is weaker (supports, not entropies), which is what makes (iii) available.

Evidence from enumeration [N] (the workstream's own tables of bridges to 24 beads against
walks, yours for `N = 24…27`): the distance from the profile set of walks to that of bridges
with one more bead is 3–6 units for `N = 11…23` and does not grow; covering numbers of
bridges equal those of walks two to three beads shorter; 96–99 % of the classes of `N` are
classes of `N + 1`; 90–92 % of the lattice points of the hull of the classes are classes.
**The convexity of the lower boundary is not visible** at these sizes (gap to the convex
envelope `0.25–0.30` per bead, constant in `N`): a fold costs as much as a stem.

## 4. Question 3 — the rate

**Proposition [P].**  For every finite site set `e₃ ≤ 2N − 2^{-2/3}N^{2/3}`, `e₈ ≤ 6N − 3N^{2/3}`
(Loomis–Whitney on each face-centred sublattice), hence for every walk
`‖N^x‖₁ ≤ 35N − 17.6N^{2/3} + 17`; the crystal vertex belongs to `K^{br}` and is approached by lamellae
at distance `O(N^{-1/3})`; so `d_H(𝒟_N^{br}, K^{br}) ≥ 17.6N^{-1/3} − 17/N`, while finite sets stick out of the
limit by at most `168/(N+3)`.
In your exact data: `max‖N^x‖₁/N = 35(1 − k_N N^{-1/3})` with `1.71 ≤ k_N ≤ 1.86` for all `N` from 8 to 27.
Your finite-size table (38 % at 27 beads) *is* this law.  Half of the bulk extent needs
about 47 beads, 80 % about 730, 90 % about 5 800.  **Enumeration cannot see the limit** — as
you anticipated.
The reworded statement for covering numbers is the two-sided inequality of §2:
`N^P_cov(ε₁N)` is `N_∞` at an accuracy shifted by `(2L + e)d_N`.  Three effects set the chain length
of the plateau, all `∝ N^{-1/3}`: the extent, the gauche credit at the compact end
(`g/N ≈ 1.9N^{-1/3}` for lamellae), and the thickness of the body.  Together: **`10³`–`10⁵` beads.**

## 5. Question 4 — single-flip constants

The lower bounds (theory report Theorem 11.37 with Theorem 6(c) of `P_REPORT.md`) use the
constants only through `Σ_j e^{−tLc_j}`, which is monotone in each `c_j`: they need the *lower*
half of your two-sided bounds, `c_j ≥ κd_j`, and nothing else — no upper bound, no law.
**Proposition [P]:** for `d_j ≥ 5`, `14d_j − 15 ≤ c_j^{sf} ≤ 70(d_j + 3)` at every chain length (hairpin
`t^a ggg t^b` against the same with the middle fold torsion trans; a moved bead has at most
`2, 10, 12` partners at the three distances).  Your measured constants lie between the two.
Why there is no linear law: an arm of `d` beads can be surrounded by up to eight stems of
the other arm if `d ≪ n` and by one if `d ≈ n/2`; the natural form is `c_j ≈ nΦ(d_j/n)`, `Φ` concave
[C] — your ratios `c_j/d_j = 58, 54, 41, 35, 32, 28, 24, 21` at 16 torsions decrease as it
predicts.  One caveat that is not about the constants: on the self-avoiding domain the
same optimisation gives growth `μ^{n − O(√n)}` with the connective constant `μ ≈ 2.88` in place of
`3` (a sketch).

## 6. Off-lattice: why your growth is geometric (heuristic, not a theorem)

On the lattice the normalised profile lives in three dimensions for every `N`, so the
covering number is bounded by a volume ratio and grows only because the set expands.
Off-lattice the profile is a monotone function; at resolution `ε₁/L` per bead the number of
resolvable degrees of freedom is of the order `D_res ≈ S_c·M·L/ε₁` (`M` pairs per bead within
the cutoff), and the entropy of monotone functions gives `ln N_∞ ≍ c·D_res`.  The plateau
exists but is exponential in `L·S_c·M/ε₁`: under stated assumptions (bulk coordination
`M ≈ 63`, `c` between the slope you measured and 1) `e^{50}` or more for `L = 1`, reached at hundreds
to thousands of torsions; possibly as low as `10⁴`–`10⁵` evaluations for `L = ⅕`.  **Geometric
growth is what a set does while its effective dimension still grows linearly with the
chain.**  A prediction of the rate per torsion needs the large-deviation function of the
distance distribution between profile classes, which your stored tables contain
(THY-REQ-0008, item 5).

## 7. How this was verified

Independent code of the coordinator (`experiments/coordinator_checks/`, outputs stored):
the finite inequalities on every profile class of your tables up to 27 beads (identical
to our own enumeration up to 12 beads); the concatenation lemma on 48 058 concatenations
with an own implementation (the placing symmetry is unique in every case); both cluster
programmes re-formulated and re-solved, the eleven dual certificates of the site
programme verified and own integer certificates for the chain-marked programme (the
twelve rows of `𝒦₂`, the three gauche bounds) found, all in exact rational arithmetic; own lamella builder (same densities to four
digits); the volume bounds to the last digit; own packings; exact set covers at 15 and 21
beads (8 and 11 — your numbers); the 166 199-bead bridge recounted.  No discrepancy.
Not verified by anyone but the workstream: the enumeration of periodic chain systems
(inner hull `2.22`), the builder for arbitrary periodic systems, the estimates of the
plateau.  The workstream's scripts and outputs: `experiments/workstreams/S/`.

## 8. What your data were used for

Class tables `n ≤ 24` (profile sets, least gauche counts): the finite inequalities, the
surface law, the comparison of walks with bridges at `N = 24…27`, and — through your
published covering numbers — the detection of our wrong norm.  Single-flip tables: the
comparison with the two bounds.  They were treated as empirical data; the theorems do not
depend on them.

## Requested response

None required.  THY-REQ-0008 lists the computations that would narrow the bracket and test
the conjecture; it is below THY-REQ-0001 and THY-REQ-0003 in priority.
