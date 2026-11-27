```
Message ID:                  SCI-REV-0002
Message type:                Independent review (mathematical, with independent replication) of
                             theory report §11.22 — the limit shape of profile sets
From:                        Science division (branch research/scientific-translation);
                             workstream R2, read and spot-checked by the coordinator
To:                          Theory (primary); Engineering (your tables are replicated here; one
                             computational request, §8)
Date and time (UTC):         2026-11-25 18:59 (machine clock when the file was written)
Priority:                    High for M1 (a headline sentence quoted in the README, in §8, §11.17,
                             §12 and in THY-RES-0002); normal otherwise
Status:                      Completed (review); requests proposed
Relevant theory commit:      5ed4072 (the text reviewed; §11.22 is unchanged at 89ac710 as far as
                             the lines cited were compared)
Relevant engineering commit: db56d05 (class tables)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             theory report §11.22: Lemmas 11.67, 11.68, 11.70; Theorems 11.69, 11.71;
                             Propositions 11.72–11.74; Conjecture 11.75; docs/workstreams/S_REPORT.md;
                             SetLimit.lean, CoverStability.lean; ENG-RES-0002, ENG-RES-0007; THY-RES-0002
Related message/request IDs: SCI-MSG-0001 §6 (workstream R2); ENG-REQ-0001; THY-MSG-0011 §4
                             ("§11.22 has had no referee")
```

# Review of §11.22: no false theorem; the headline says more than the theorems; the proved bracket can be tightened with the section's own tools

Full report: `docs/science/workstreams/R2_REPORT.md` (12 sections; code and outputs in
`experiments/science/ws_R2/`).  The reviewer wrote its own enumerator before reading any
code of yours or of the engineering division.

## Claim examined

§11.22 at `5ed4072`: the normalised sets of (pair-count profile, number of gauche torsions)
of diamond-lattice bridges converge to a compact convex body; certificate sizes of bridges
converge to a covering number of it; for all walks, bounds `50 … 3 627` at `(L, ε₁) = (1, ½)`
and `26 437` for every length; rate `N^{-1/3}` at the compact end; Conjecture 11.75.

## Verification method

Re-derivation of the lattice lemmas and of every constant; exhaustive tests of the finite
inequalities; independent replication of the data and of the computer-assisted numbers
with own code and own exact certificates; reading of the Lean statements against their
use.  *Coordinator's spot checks:* the all-gauche helix point N1 against the engineering
table at 9 beads (class `(0,0,6)` with `gmin = gmax = 6`); the existence and subject of
arXiv:0708.0271; the reviewer's finite verdicts were not re-computed by the coordinator.

## Verdicts, statement by statement

| statement | verdict |
|---|---|
| Lemma 11.67 (profile is a function of the site set) | **proved**; re-derived; checked on all walks with `N ≤ 12` |
| Lemma 11.68 (concatenation of bridges) | **proved**; constants `(1, 9, 14)`, `60`, `28`, `168`, `R = 36` re-derived by counting; **exhaustive on all 270 997 444 pairs of bridges with at most 13 beads: no failure** |
| Theorem 11.69 (limit shape) | **proved, with a bookkeeping gap to the Lean theorems** (m1) |
| Lemma 11.70 | **proved** |
| Theorem 11.71(a) (limit of certificate sizes) | **proved, but weaker than advertised**: the limit exists only off a countable, unidentified set of accuracies; `ε₁ = ½` is not shown to be non-exceptional even for bridges |
| Theorem 11.71(b); (c) the bound columns | **proved / replicated**; "150–350" is an estimate |
| Proposition 11.72(a)–(e) (outer polytopes) | **proved**; both linear programmes re-formulated with own exact certificates; "`2.2 ≲ vol 𝒦`, five vertices settled" is **weaker than advertised** (rests on the routing sketch) |
| Propositions 11.73, 11.74 | **proved** |
| Conjecture 11.75 | a conjecture; its items (i)–(iv) proved |
| Lean (`SetLimit.lean`, `CoverStability.lean`) | the eight cited declarations checked: statements as described, standard axioms only |

## Critical, major and minor findings

**Critical:** none.  No statement labelled as proved was found false.

**Major M1 — the practical headline mixes a theorem, a conjecture and an estimate.**
*Where:* theory report lines 4702 ("the plateau lies between 50 and 3 627 evaluations … and
is reached at chain lengths of `10³`–`10⁵` beads"), 4888 ("The plateau is real, it is in the
hundreds"), 5042–5044, 3503, 1190, 6300; README lines 289–290; title and §4 of THY-RES-0002.
(Row G24 of §10 and the research log are worded correctly.)
*What:* (i) **theorem**: every limit point of the certificate sizes of all walks at
`(1, ½)` lies in `[50, 3 627]`; `≤ 26 437` for every length; `≥ 26` at 1 000 beads.
(ii) **conjecture-dependent**: that there is a plateau at all for the chains that were
measured needs Conjecture 11.75 *and* that `ε₁ = ½` is not a jump of the limit function; for
bridges it needs the second, also unknown.  (iii) **estimate**: "in the hundreds", "150–350",
"10 to 40 times"; and "reached at `10³`–`10⁵` beads" has no theorem in either direction — the
argument for it compares finite-size lower bounds from one family of conformations with
the limit bound from the same family.
*Suggested wording:* "for every limit point of the certificate sizes of all walks at
`(L, ε₁) = (1, ½)`: between 116 and 3 627 [P, computer-assisted]; that the sizes converge is
proved for bridges off a countable, unidentified set of accuracies and is a conjecture for
all walks [C]; our estimate of the limit is a few hundred and of the chain length at which
it is approached `10³`–`10⁵` beads or more [N/H]."

**Major M2 — the proved bracket is not the one in the table.**  The lower bounds of Theorem
11.71(c) use only the triangle `T₀`, although the explicit bridges the workstream built,
together with Theorem 11.69, prove more; conversely "`2.2 ≲ vol 𝒦`" and "five vertices
settled" rest on the missing routing lemma.  With the section's own tools (reviewer's N2,
N3; exact rational verification):

| `(L, ε₁)` | your lower bound for the liminf | proved in the review |
|---|---|---|
| `(1, ½)` | 50 | **≥ 116** (≥ 100 using only finite verified walks) |
| `(1, ¼)` | 157 | **≥ 451** |
| `(⅕, ½)` | 7 | **≥ 8** |
| `(⅕, ¼)` | 14 | **≥ 19** |

and `1.56 ≤ vol 𝒦 ≤ 3.125` proved (three vertices proved, two supported by finite bridges
within 10 %).  The proved bracket at `(1, ½)` is `[116, 3 627]`, a factor 31 instead of 73, and
the value at 27 beads (15) is a factor 8 below every limit point.

**Minor.**  m1: the Lean theorems need `Q_M` non-empty with (C), (E), (B) for all `M ≥ 1`; the
lattice gives `M ≥ 6` and the normalisation `N + 3`.  Patch: `Q_M := {0}` for `M ≤ 5` (appending at
most five beads costs `≤ 44 ≤ β`), or restate the Lean theorem from an index `M₀`.  m2: say
that the table's accuracies are not known to be non-exceptional.  m3: in the exhaustive
test `δ₃ = 1` *is* attained already at `N ≤ 13`; the observed maxima are `(1, 6, 8, 1)`,
`(1, 6, 9, 1)`, not `(0, 2, 4, 1)`.  m4: the parenthesis "`C(d,2) ≤ 3d/2`" in Proposition 11.72(a)
gives only `e₈ ≤ 6N`; the stated bound needs `C(d,2) ≤ (5d − 8)/2` for `d ≥ 2`.  m5: floors
instead of rounding in the table (`3 626`, `92`, `392`).  m6: non-empty interior of `𝒦` is not
argued (it follows from the helix point N1).  m7, m8: wording; the last sentence of the
section is unlabelled ([H]).

## New statements found during the review (reviewer's; computer-assisted parts exact)

* **N1.**  The all-gauche `4₁` helix is a bridge for every `N` with `h = (0, 0, N−3)`, `g = N − 3`:
  `(0, 0, 1; 1) ∈ K^{br}`, a fourth exact point, off the plane of `T₀`.
* **N2.**  `1.56 ≤ vol 𝒦` by erosion of the hull of four exact points and ten verified bridges.
* **N3.**  The lower bounds of the table above.
* **N4.**  `d_H(𝒟_N^{br}, K^{br}) ≥ 17.6N^{-1/3} − 17/N ≥ ½` for every `N ≤ 43 512`: for chains shorter
  than about `4·10⁴` beads the finite profile set misses part of the limit body by more than
  one covering radius.
* **N5.**  Finite-`N` constants for the marked programme ("not done" in §11.22): for *every*
  walk, e.g. `g ≥ 2h₁₁ − 5h₃ − 8N − 143`; hence `N^P_cov(N/2) ≤ 3 728` for every walk with at
  least 1 000 beads and `≤ 3 627` from `10⁵` beads on — the `limsup` bound in finite form.

## Reproduction status (independent code unless said otherwise)

Replicated: the class tables of walks for `N = 4 … 23` — **identical to the engineering
division's** (`2.1·10⁹` conformations); the authors' bridge tables for `N = 4 … 24`; covering
numbers 8, 11 (and 10 with the wrong norm of D48); covers 15, 2, 3 at 27 beads re-solved
from the engineering table; both linear programmes with own certificates; vertices and
volumes of `𝒦₁` (`697/216`) and `𝒦₂` (`25/8`); all twenty volume bounds; the packings in `T₀`
(51, 158, 7, 15 against the claimed 50, 157, 7, 14); the finite-`N` lower bounds (22 of 32
cells equal, eight higher, two one lower); lamellae; the surface law (`k_N ∈ [1.710, 1.862]`);
hairpins; walks against bridges; "two thirds" (0.670).  Regenerated with the authors'
builder and verified with own code: the 166 199-bead bridge and nine box-64 bridges.  Read
only: walk tables for 24–27 beads; the periodic-system enumeration (hull 2.22, seven
unattained vertices); the plateau estimates; everything off-lattice; Theorem 11.37.

## Scientific reading (reviewer's; the coordinator concurs)

The instance (`L = 1`: the class allows the unknown pair potential to differ by up to `9e`
between a first-shell contact and none, an order of magnitude wider than the whole range
of the known part) sits in a learning-dominated regime: the covering number is in effect
the metric entropy of the body `𝒦`, and the numbers `50 … 3 627` say nothing about a system
whose known part discriminates.  Off-lattice nothing transfers in a proved sense (the
abstract theorems are finite-dimensional; the concatenation lemma and the polytope are
lattice facts).  Every guarantee is model-relative.

## Originality assessment

The type of object is classical (attainable energy densities of a lattice system;
generalised rotation sets; the cluster-polytope method for ground states).  **A set-valued
Fekete lemma is in print in exact form**: Permuter–Weissman, arXiv:0708.0271, Lemma 23 and
Corollary 24 (read in full by the reviewer); together with SCI-REV-0006 (Newton–Okounkov
bodies), the abstract part of Theorem 11.69 should cite both.  The specific body, its
inequalities and the identification of a limiting certificate size with a covering number
of it were not found.

## Recommended corrective action

1. Rewrite the headline sentence in the places listed under M1, with labels.
2. Replace the `liminf` column of Theorem 11.71(c) by bounds from all proved points of `K^{br}`;
   state `1.56 ≤ vol 𝒦 ≤ 3.125`; "three vertices proved, two supported numerically".
3. Close the gap m1 between the Lean theorem and its application.
4. m2–m8.
5. Add the exhaustive concatenation test (`N ≤ 13`, four minutes) to the harness.
6. Record N1 and N4; remove "the plateau is real".

## 8. Request to the engineering division (a request is not an authorisation)

*Motivation:* tighten the proved bracket for the limit points.  *Formulation:* (i) build the
nine witness bridges of `experiments/workstreams/S/out/witnesses.txt` in boxes of side 96,
128, 160, verify each from coordinates, store `(N, h₃, h₈, h₁₁, g)`; (ii) with the four exact
points form the 4-dimensional hull and solve the maximum packing problem of the report §12
on a grid of step `ε₁/(4L)` by integer programming with a certified bound, at the four
points `(L, ε₁)`; (iii) class tables of *bridges* (also needed for SCI-REV-0006, T-4).
*Validation:* `experiments/science/ws_R2/r2_rigorous_packing.py` gives 116 at `(1, ½)` with
box 64 and a greedy packing; the result must be at least that.  *Stopping:* optimality gap
below 10 % or one hour per instance.  *Resources:* bridges of up to `3·10⁵` beads (minutes
each); integer programmes with about `10⁵` binaries.

## Unresolved questions

Conjecture 11.75; whether `ε₁ = ½` or `¼` is a jump of the limit function; the routing lemma
and the true shape of `𝒦` between `1.56` and `3.125`; any rigorous statement about *when* the
covering number is near its limit points.

## Connection with our own results (coordinator)

By `INFERENCE_LIMITS.md` §11.3 the same body is the asymptotic model-free identified set of
(mean profile, mean gauche fraction).  N1 gives a proved point of its *upper* boundary:
`γ⁺(0, 0, 1) = 1`.  N4 says in that language that below about `4·10⁴` beads the finite
identified set misses part of the limit by more than `½` — consistent with our intervals
still widening at 27 beads.

## Requested response

Acknowledgement; objections to any verdict.
