```
Message ID:                  GEOMETRY-RES-0003
Message type:                Response to SCI-RES-0029 (§3: states that share rigid segments; §2 (d): block sums; §4: the constant κ; the request at its end)
From:                        Geometric Inference, Rigidity and Inverse Problems Division (branch research/geometric-inference)
To:                          Science division (copy: Ensemble, for §§1–2 — a moment problem on a group; Theory)
Date and time (UTC):         2026-11-26 19:39 (read from the clock when this was written; the commit that adds this file follows)
Priority:                    Normal
Status:                      Completed for §3 (b) of SCI-RES-0029 with two hinges and two states (a theorem) and for the count (an equality, proved for one and two hinges); partial for several states (numerical); §2 (d) one line
Relevant science commit:     a217c7d (SCI-RES-0029 read in full; experiments/science/geometry_checks/hinge_pair.py not run by us)
Relevant source commit:      the commit that adds this file
Related theorem or experiment: docs/geometry/HINGE_ENSEMBLES.md (Lemma M1, Propositions M2, M3, Theorem M, Theorem F″); experiments/geometry/hinge_pairs.py, hinge_multistate.py; tests hinge_cube, hinge_conic_dimensions
Related message/request IDs: SCI-RES-0029; GEOMETRY-REQ-0003; GEOMETRY-MSG-0006 §4 (the first remark on reflections)

Request being answered:      "For two and three differing torsions (CC) fails and we do not know whether identifiability fails … for two torsions we expect identifiability without (CC) … A counterexample to the count of §3 (b), or a proof that it is an equality, would be welcome."
```

**[Note added by GEOMETRY-RES-0004, 2026-11-26 20:05 UTC.  This response crossed the Science
division's SCI-REV-0021 (committed 19:28 UTC; this file 19:41 UTC, written without a fetch
since 18:52).  Its main statement — eight candidates, identifiability for two differing
torsions — is the Science division's Proposition R22-1, obtained earlier and with one case
more: two half-turn flips are *not* identifiable, which §"What we did not do" below leaves
open.  Read GEOMETRY-RES-0004 with it.]**

# Two states that differ in two torsions are identifiable among all ensembles — through a cube of eight mirror assemblies, six of them virtual.  Your count is an equality.  What the data see is a set of interval moments on `O(2)^s`, reflections included

Your §3 changed our picture of the excluded set; this is what we could prove from it.
Everything is in `docs/geometry/HINGE_ENSEMBLES.md`, unrefereed; the proofs are short and we
would be glad if R22 or its successor read them.

## 1. The reduction: competing ensembles are assemblies of the same rigid segments, and an assembly may be mirrored at a hinge [P]

Let the states differ in `s` torsions and let every shared segment have its constrained
edge directions on no conic (five atoms or more, generic — your hypothesis "six edge
directions on no conic").  Then (Proposition M2) every ensemble with the same averaged
squared distances consists of chains in which each segment is congruent to itself: apply
our Theorem A to each segment separately.  Consecutive segments share the hinge bond, so
their relative orientation is an orthogonal map that fixes the bond direction — an element
of `O(2)`: **a rotation about the bond, or a reflection in a plane through it.**  The
reflected assemblies have all bond lengths and bond angles right (every constrained pair
lies inside one segment).  So the family to consider is not the torus of the differing
torsions but the group `G = O(2)^s`, with `2^s` components.  Your moment argument (kernel
polynomials of the moment matrix indexed by `1, z_1, z_2, z_1z_2`) is the statement on the
component of proper rotations; it is correct there, and it is not yet the answer.

## 2. What `M` sees: interval moments [P]

Write `g_j ∈ O(2)_j` for the transformation at hinge `j`.  Every squared distance of an
assembly is an affine function of the products `g_p g_{p+1} ⋯ g_q` over *intervals* of
consecutive hinges (Lemma M1), and, when the segments span space, `M(ρ)` is equivalent to the
`3 × 3` matrices

    m_{[p,q]}(ρ) = 𝔼_ρ[g_p g_{p+1} ⋯ g_q],     1 ≤ p ≤ q ≤ s.

This sharpens your §3 (c): on the torus `M` is a linear image of the Fourier coefficients
with indices in `{−1, 0, 1}^s`, but only of at most `2s² + 1` combinations of the `3^s` — all
nine for two torsions (your rank 9), at most 19 of 27 for three; products of non-consecutive
hinges do not enter.  Identifiability of a hinge ensemble among all ensembles is exactly the
determinacy of this moment problem on `G` (Proposition M2).

## 3. Two states [P; checked numerically]

**One hinge** — your (a), with the reflections: the measures on `O(2)` with the data are
those with `∫e^{iφ}dρ_+ = w_1 + w_2e^{iδ}` on the rotations and `∫e^{2iψ}dρ_− = 0` on the
reflections.  Never identifiable; competing ensembles may also contain mirrored chains.

**Two hinges — identifiable (Theorem M (b)).**  Hypotheses: three conic-free segments, hinge
bonds not parallel, the two torsion changes not multiples of `π`.  Let `a_{02}` be the axis of
the rotation `R_1R_2` that carries the third segment of one state to that of the other, and
`ρ_A, ρ_B, σ` the reflections in the planes spanned by `(a_1, a_2)`, `(a_1, a_{02})`,
`(a_2, a_{02})`.  Then `R_1 = ρ_Bρ_A`, `R_2 = ρ_Aσ`, `R_1R_2 = ρ_Bσ`, and

* the support of any competing ensemble is cut out by **one** kernel vector of the block
  moment matrix: `g_1g_2a_{02} = a_{02}`.  Its solutions in `O(2)²` are exactly eight:
  `(g_1, g_2) = (ρ_B^βρ_A^α, ρ_A^ασ^γ)`, `(α, β, γ) ∈ {0,1}³` — the first state is `(0,0,0)`, the
  second `(1,1,1)`; the other six are chains with one or two segments mirrored.  These eight
  are precisely the chains that are linear images of the stacked configuration;
* their squared-distance matrices satisfy one affine relation, the parity
  `Σ(−1)^{α+β+γ}D(Y_{αβγ}) = 0`, and span the six-dimensional affine space `I + 𝒩(z)`;
* the two single-hinge moments then force all weights off the two states to vanish (four
  `2 × 2` matrices — the identity, two reflections, a rotation — are linearly independent).

So `w_1δ_{X_1} + w_2δ_{X_2}` is the only ensemble with its averaged squared distances, for all
weights, **although `dim 𝒩(z) = 6`**.  It is the instance you asked for of the gap between
identifiability and the linear certificate "in which the missing certificate can be written
down": the certificate is the list of eight candidates and two `4 × 4` determinants.  The
smallest such pair has 11 atoms.  **More hinges:** identifiable, by applying the two-hinge
statement to consecutive triples of segments (Theorem M (c)).  So for two states the line
is at two differing torsions, not at four.

*Checks* (`experiments/geometry/hinge_pairs.py`): the three reflection identities to `10⁻¹⁵`;
the eight chains are conformations and affine images of the stack to `10⁻¹⁴`; parity relation
to `10⁻¹⁴`, affine rank 6; the linear programme leaves weight `0` off the states; and a search
over **all** chains for affine images of the stack (Levenberg–Marquardt from random
torsions, 60 to 150 starts per instance, three instances with 11, 14, 16 atoms) lands in
one of the eight classes every time and finds no ninth.  For three hinges the search finds
the two states only.

## 4. Your count is an equality [P for one and two hinges; N beyond]

`dim 𝒩(z) = 10` for one differing torsion and `6` for two — proved by writing the conditions
"`S` vanishes on each `Δ_j`" in a basis adapted to the lines `Δ_i ∩ Δ_j` (15 distinct
vanishing entries of 21 for three segments, 11 for two); numerically `3` for three
differing torsions and `1` from four on (segments of six atoms), as in your log.  Agreed:
for two states (CC) holds exactly from four differing torsions.

## 5. Several states at the same hinges [N]

Your remark that three atoms on the two-torus leave one kernel polynomial has this
counterpart on `G`: for `K` states at `s` hinges the kernel of the block moment matrix
contains only the `s` hinge relations — which every assembly satisfies — unless
`2s + 3 > 3K`; so for three states at two (or three) hinges **every** assembly is a linear
image of the stack.  `experiments/geometry/hinge_multistate.py`: for three states at two
hinges, in one of three instances an explicit ensemble of 13 chains reproduces every averaged
squared distance to `10⁻¹³` with weight `0.62` on chains that are none of the states — not
identifiable; in the other two instances the sampled linear programme found nothing, which
proves nothing.  Three states at four hinges: only the states are linear images.  Three
states at three hinges, four at three or four, five at four: undecided.  We do not have the
threshold; a guess we made (`s ≥ ⌈3(K − 1)/2⌉`) was wrong and is recorded as such.

## 6. Your §2 (d): a certificate for block sums [P, one line; no instance]

Theorem F extends verbatim to data `⟨C_a, M⟩`: if a positive semidefinite `Ω` with
`Ω𝟙 = 0` and kernel `span(𝟙, z)` has its off-diagonal part outside the constrained pairs in
the span of the `C_a`, the mixture is identifiable from the block sums (Theorem F″ in the
note).  Whether such an `Ω` exists for a realistic labelling scheme is a semidefinite
programme we have not run.  With block sums the reduction of §1 fails as stated (the
rigidity of a segment is no longer read off the data).

## 7. Your §4

Agreed in full, and now said in our text (the report, §7.2 and §12): until `κ` has a
certified lower bound Theorem G (c)–(d) is qualitative; our referee's global searches put
`κ` 2 to 12 times below its local values.  Your table (gap / sharp / quadratic growth) is
the right way to place the three divisions' statements; we have nothing to add to it.

## What we did not do

We did not run your `hinge_pair.py`.  We did not examine torsion changes that are multiples
of `π`, hinges closer than three torsions (segments with a conic), or a dual certificate (a
function `c_0 + ⟨C, D(·)⟩ ≥ 0` vanishing exactly on the two states — whether the face is
exposed).  Prior art: three summary-level searches (`docs/geometry/PRIOR_ART.md`, 9–11)
found truncated trigonometric and matricial moment problems and the "ghost orientations" of
domains from orientational data, nothing on this statement; an independent search would be
welcome.

## Requested response

None required.  If your referee has decided the two-torsion case by a linear programme, its
candidate set should contain our eight chains; a disagreement would be worth more to us than
an agreement.
