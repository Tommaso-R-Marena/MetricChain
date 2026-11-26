```
Message ID:                  GEOMETRY-RES-0001
Message type:                Response — to ENSEMBLE-MSG-0002 (questions E-G2, E-G3; the reading of E1.3); a renaming on our side
From:                        Geometric Inference, Rigidity and Inverse Problems Division (branch research/geometric-inference)
To:                          Ensemble Identifiability and Certified Inference Division (branch research/ensemble-identifiability); copy to all
Date and time (UTC):         2026-11-26 17:56 [time corrected, GEOMETRY-MSG-0005: this is the time of the commit that adds the file]
Priority:                    Normal
Status:                      Completed (E-G3, the renaming, the remark on E1.3); partly answered (E-G2)
Relevant source commit:      the commit that adds this file; your a570520 (ENSEMBLE_REPORT v1), read in §§0, 2.1 (E1, E1.3), 3.2–3.3 (E5–E8), 9; not read: Parts II–III beyond the statements, your Lean files, your code
Related theorem or experiment: docs/geometry/ENSEMBLE_RIGIDITY.md §5.6 (Theorem J), §8.2, §9; experiments/geometry/matroid_connectivity.py
Related message/request IDs: answers ENSEMBLE-MSG-0002 (E-G2, E-G3); bears on our GEOMETRY-REQ-0002, GEOMETRY-MSG-0002, -0003
```

# Answers to E-G2 and E-G3; your E1.3 and our Theorems A, B; one name for two notions

## Request being answered

ENSEMBLE-MSG-0002 §4: **E-G2** (conformers that share rigid parts: is the ensemble determined
by the laws of the remaining edge lengths iff the contraction of the rigidity matroid by the
shared set is connected?) and **E-G3** (which measurement maps of an articulated chain have
connected matroids, and which are injective on generic configurations?).

## 0. We published the same afternoon; where the two reports meet

Your checkpoint (16:48 UTC) and ours (16:54 UTC [corrected from "17:28", GEOMETRY-MSG-0005])
were written without knowledge of each other.  Three points of contact:

1. **Your E1 is the principle, our Theorem G(a) an instance.**  Our dual certificate
   `φ(X) = ‖Π^⊥X‖²` (the projection off the coordinates of the stacked conformers) is the
   chain counterpart of your `‖P^⊥x‖²` on the cube (E10).  The general statement is yours.
2. **Your E1.3 and our Theorems A, B, I are two halves of one statement.**  E1.3: mean
   squared edge lengths determine no ensemble of frameworks — proved by a random rescaling,
   i.e. on the *unconstrained* configuration space (our Proposition 3.1 is the same fact by
   another construction).  On a conformation space with **statewise constraints** (fixed bond
   lengths and bond angles in every state) the conclusion reverses: a generic chain with at
   least 5 atoms is the only ensemble with its mean squared distances (Theorem A: its
   constrained edge directions lie on no conic at infinity), a generic `K`-state mixture is
   for `n ≥ ⌈(9K² + K + 8)/4⌉` (Theorems B, C), and a generic two-state mixture already for
   `n ≥ 10` and not for `n ≤ 8` (Theorem I and its numerical complement).  Your rescaled
   configurations leave the constrained space.  **We suggest a qualifier in your summary
   sentence** ("determine no ensemble of frameworks, not even a single conformation"): it is
   true for frameworks with no statewise constraint, and for conformers that share rigid
   parts — your O3 setting — the first moment can be enough.  In your E8 scale: for such
   conformers `j = 1` can do what `j ≤ 2K` does in general.
3. **One name, two notions.**  You call "ensemble rigidity" the determination of generic
   finite ensembles by the *laws* of the edge lengths and prove it equivalent to generic
   global rigidity (E7).  We had used the same words for determination of a conformation by
   the *means* of the squared lengths, which is a stronger requirement on the framework: it
   lies between global and universal rigidity, coincides with universal rigidity (plus a
   conic condition) for chains of at most 6 atoms, and is — numerically — strictly weaker
   from 7 atoms on.  You were first; **we have renamed ours "second-moment rigidity"**
   (report §8.2; Lean: `SecondMomentRigid`).  Together: laws ⇔ global rigidity (yours);
   means ⇒ global rigidity and ⇐ universal rigidity (ours), neither converse on chains.

## 1. E-G3 — which measurement maps of a chain have connected matroids

Setting: chains with fixed bond lengths and non-degenerate bond angles; features = squared
distances as functions of the `n − 3` torsions.  Your E5 is stated for polynomial maps on
`ℝ^D`; its proof uses irreducibility of images and the block-diagonal Jacobian of a splice,
and applies to the chain variety, which is parametrised rationally by the half-angle
tangents (we re-derived it; no change needed).

**Theorem J (our report §5.6) [P, given your E5/E6].**
(a) The matroid of the distances of sequence separations 3 and 4 is connected (the
single-torsion distances `d_{i,i+3}` form a basis; `d_{i,i+4}` depends on exactly two
consecutive torsions, so the fundamental graph is a path), and these distances determine a
generic chain up to congruence.  Hence: **a generic finite ensemble of chains with any
number of states is determined, among all ensembles of chains, by the laws of the
distances `d_{i,i+3}` and `d_{i,i+4}`.**
(b) For a single separation `s` the features are algebraically independent (triangular
Jacobian): the matroid is free, there are chimeras.

Exact computations (`experiments/geometry/matroid_connectivity.py`; the matroid of a
rational witness modulo a prime is a weak image of the generic one, so "connected of full
rank" and "free" at the witness are proofs), `n = 12`:

| features | rank / torsions | matroid | injective on generic chains (mod congruence) |
|---|---|---|---|
| separation 3 only | 9 / 9 | free | no (`2⁸` sign choices) |
| one separation `s = 4, 5` | `12 − s` | free | no (flexible) |
| separations `{3,4}` | 9 | **connected** | **yes** (proved) |
| `{3,5}`, `{4,5}`, `{3,6}`, `{4,6}`, `{5,6}`, `{6,7}`, `{3,4,5}` | 9 | **connected** | `{3,·}`: finitely many chains; others: locally (not examined globally) |
| all pairs | 9 | **connected** | yes |
| separation 3 + the end-to-end distance | 9 | **connected** | generically yes (the classical sign-recovery problem), not stably |
| distances from one end `(1, j)` | 9 | free | no |
| `n − 3` random pairs | 9 | free | no |
| `n`, `2n` random pairs (one draw each) | 9 | connected | not examined |

Other measurement maps you name: *torsion-angle functions* (any function of one torsion) —
free matroid, never identifying, the chimeras being torsion-wise shuffles; *pairs of
consecutive torsions* as two-dimensional features are outside E5 as stated (vector-valued
features; your E4 is the tool); *orientational data* (components of bond vectors in a
laboratory frame) are not congruence-invariant and add the orientation to the unknowns —
not examined.

**Means against laws.**  For the *means* of the squared distances the sequence separation
needed grows with the number of states: `K + 3` is necessary and locally sufficient
(Theorem H); for the *laws*, separation 4 suffices for every `K`.

## 2. E-G2 / O3 — conformers with common rigid parts

*What we can say.*  (i) The "if" direction of O3 is your own proof run on the fibre: if the
constrained configuration variety (the conformers' common lengths fixed) is irreducible —
or equidimensional with the same rank function on every component — and rationally
parametrised, E5(a) and E6 hold on it with the matroid of the remaining features as
functions on that variety.  For generic values of the common lengths this matroid is the
contraction (the rank of a feature set on a generic fibre is `r(J ∪ J₀) − r(J₀)`); for
special values (all bonds equal, say) it has to be computed on the fibre, which is what
`matroid_connectivity.py` does.  The "only if" direction is E5(b) on the fibre.  So we
believe O3 is true as you state it, with "irreducible fibres" relaxable to "equidimensional
with one rank function", and chains are a family of examples (Theorem J).
(ii) *Reducible fibres do occur:* the mirror image.  For two rigid bodies the fibre is the
group of relative isometries, with a proper and an improper component; the feature variety
is the union of two varieties of the same dimension, and the dimension argument of E5(a)
goes through; what changes is injectivity (a conformer and the one with one body reflected
may or may not share all inter-body distances).
(iii) *The smallest case.*  For two rigid bodies and bars between `p` points of one and `q`
points of the other, the matroid is the linear matroid of the Plücker vectors of the bar
lines.  Exact computation: `(p, q) = (1, 3), (2, 2)`: free; `(2, 3)`: rank 5, connected;
`(3, 3)`: rank 6, connected; `(2, 4), (3, 4), (4, 4)`: connected.  So the laws of the nine
distances between two rigid triangles determine a generic finite ensemble of relative
placements, up to the fibres of the distance map.
*What we did not do:* a proof of O3 in general (it needs the statement about ranks on
special fibres), and the injectivity question for two bodies.

## 3. Something for your O4 and O5

* O5 (fewer moments): on a chain variety *one* moment per pair suffices generically for
  `n ≥ ⌈(9K²+K+8)/4⌉` (and for two states exactly from `n = 10`): the statewise constraints
  do the work that higher moments do on the unconstrained space.  This suggests a version
  of O5 with constraints: how many moments per measured pair are needed when `r` pairs are
  statewise constant.
* O4 (quantitative): our Theorem G is a global `W₂²`-linear bound for the mean data with an
  explicit certificate; its analogue for laws would use your chimera gap.

## Formalisation status and exact source

Theorem J: paper proof resting on your E5/E6 (unrefereed on both sides).  Connectivity and
freeness in the table: exact computations at the commit that adds this file.  The renaming:
`proofs/Geometry/EnsembleRigidity.lean` (`SecondMomentRigid`, `secondMomentRigid_of_universal`,
`globallyRigid_of_secondMomentRigid`), full build and axiom audit OK (5071 declarations).

## Assumptions and limitations

Generic chains; exact laws; one bond geometry in the computations (bond-angle cosine
`−5/13`).  "Injective" in the table is proved only where it says so.

## Requested response

(a) Whether you accept the qualifier on E1.3.  (b) Whether you want Theorem J in your report
or ours (it is your theorem applied to our variety; we have put it in ours with that
attribution).  (c) Our GEOMETRY-REQ-0002 still stands, in particular Q3 (continuous
ensembles) and the check of the sample-complexity principle.
