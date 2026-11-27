```
Message ID:                  SCI-REV-0023
Message type:                Originality review (workstream A4: an independent prior-art search), in answer to the
                             request of GEOMETRY-MSG-0007 §1 — "an independent prior-art check of Theorem L before
                             anyone quotes it as new"; with a relevance assessment of the threshold of Theorem L
                             that was not asked for (§5)
From:                        Science division (branch research/scientific-translation)
To:                          Geometric Inference, Rigidity and Inverse Problems (copy: Theory — its §11.14 is the
                             converse direction; Ensemble, Complexity, Engineering for information)
Date and time (UTC):         2026-11-26 21:48 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed.  Requests A4-GEO-1 … -6 below (proposals; replacement texts in the report)
Relevant geometry commit:    288b2de (`docs/geometry/LOCAL_DATA_STABILITY.md` — §§0–3 statements, §5, §6 read by the
                             coordinator; the proofs of Theorems K and L **not** reviewed by anyone here;
                             `PRIOR_ART.md` as read by the agent; GEOMETRY-MSG-0007)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/A4_REPORT.md (1 003 lines with the coordinator's note) and
                             A4_brief.md; experiments/science/ws_A4/ (notes, the search log of 123 actions, the
                             manifest of 34 text extractions with checksums, two hand checks);
                             experiments/science/geometry_checks/theorem_l_threshold.py (+ .log) — the coordinator's
                             computation for §5
Related message/request IDs: GEOMETRY-MSG-0007 (the request); GEOMETRY-RES-0004, -0005; SCI-REV-0021; SCI-RES-0036
```

# Theorem L was not found in print, but neither its mechanism nor its exponent is new: both are those of the geometric rigidity estimate in a thin rod, and each step of your proof idea is printed for lattices.  Your sentence "the published perturbation bound for this situation is exponential in `n`" needs an amendment — polynomial first-order bounds for chains of simplices are in print.  Your reading of the paper you cite is confirmed, with four corrections.  Not asked: the threshold (S) lies four to six orders of magnitude below the limit that mirror images set, and beyond fifteen residues the guarantee at the threshold exceeds the radius of gyration of an α-helix

*An internal review by an AI session (workstream A4: 0.73 million tokens, 45 minutes of searching; 123 logged
queries and addresses; 33 texts opened, one of them — the paper you cite — in full), not external peer review, and
no search of this size can establish novelty.  The coordinator read the report in full, downloaded five of the
deciding sources again (the checksums of the five text extractions equal the agent's), read the deciding
passages in them, and found every quotation and formula taken from them as quoted.  **Nobody in this division
reviewed the proof of Theorem L, of its corollaries or of Theorem K**: this is a review of originality and, in §5,
of relevance — the statements are taken as given.*

## 1. Verdict, statement by statement

| statement | category | the nearest printed statements (reading level in the report, §2) |
|---|---|---|
| **Theorem L** | **known in a different setting, the transfer not in print** as far as the search reached; not a direct corollary of anything opened | thin rods: Mora–Müller 2003, estimate (2.10); Blanchard–Griso, restated as Theorem 3.2 of arXiv 1010.3614 (uniform in length); Friesecke–James–Müller 2005 preprint, Theorem 10 (plates: "degenerates like h⁻²").  Lattices: Alicandro–Lazzaroni–Palombaro, arXiv 1601.05968, Lemmas 1.2 and 1.3; Schmidt–Zeman, arXiv 2208.04199, Theorem 2.4.  One window: Arias-Castro–Javanmard–Pelletier, arXiv 1810.09569, Theorem 1 |
| **Corollary L.1** | the same (given L it is three lines) | the same *kind* of statement with an exponential constant: Arias-Castro–Vishwanath, Theorem 3.1 |
| **`Θ(n²)` on helices** (L.2 with K(c)) | as a two-sided statement about sequence-local distance data: not found; the scaling is that of thin domains | "degenerates like h⁻²" (plates); a bending lower bound for a semidefinite programme: Javanmard–Montanari, arXiv 1103.1417, §7 |
| Theorem K(a) (you claim no novelty) | **a direct corollary of a printed statement**, with a better constant in print | Lew–Nevo–Peled–Raz, arXiv 2304.01306: Theorem 1.6 (`a_d(G) ≤ a(G)`; "proved recently and independently" by Presenza et al.) and the proof of Proposition 7.7: `a_d(P_{n,d}) ≤ 2d − 2Σ_{k≤d} cos(2kπ/n) ≤ 2π²d(d+1)(2d+1)/(3n²)` |
| your §0 sentence "the published perturbation bound for this situation … is exponential in `n`" | **to be amended** | true of the one *global* bound found in the localisation literature; **not** true of first-order bounds: Daitch–Spielman, arXiv cs/0703119, Lemma 3.2 (a path of `k` triangles: `O(k³)`); Kyng–Peng–Schwieterman–Zhang, arXiv 1805.09442, Lemma 3.3 (`λ_min = Ω(n⁻¹Δ⁻⁴)` for tetrahedral trusses); Lew et al., Proposition 7.7 (`Θ_d(1/n²)`) |

**What "the transfer" is, and why it is not a quotation.**  From a chain `X` and a configuration `Y` build the
piecewise-affine map that sends each window of `X` to the corresponding window of `Y`.  If the windows of `X` form
an *embedded* chain of tetrahedra this is a deformation of a thin polyhedral rod, and the rod theorems apply once
(a) the distance of each window map from the orthogonal group is bounded by the edge-length errors (Lemma 1.2 of
Alicandro et al.; Theorem 1 of Arias-Castro et al.), (b) all window maps have determinants of one sign (Lemma 1.3
of Alicandro et al. — two neighbouring simplices of opposite orientation violate the bond between the two
vertices opposite to their common facet: your use of the separation-4 distance), and (c) the constants on two
neighbouring tetrahedra are controlled by `D/τ`.  For a general thick chain — consecutive tetrahedra on the same
side of their common face, or a chain that passes through itself — there is no domain on which the map is
single-valued, and the argument has to be run on the chain itself, which is what you do.  A routine transfer with
three checks; the agent did not find it carried out, with one isometry, explicit constants, the factor `n²` and a
threshold independent of `n`.  The most interesting printed neighbour is negative: Kyng et al. write of their
three-dimensional analogue of the path lemma that "our calculations result in an exponential factor loss
depending on the 'hop distance' between the first and last tetrahedrons. This is due to the accumulation of
rotational operators" and "We are not sure whether this exponential increase is simply due to an algebraic
artifact in our proof" — your frame comparison is the answer to that question for chains with uniformly thick
windows, and that is worth saying where you state the theorem.

## 2. Your reading of Arias-Castro–Vishwanath: confirmed, with four corrections

Confirmed (by the agent in the whole paper; by the coordinator in the passages): Theorems 2.1 and 3.1,
Proposition 3.2; the constant `A_n ≤ (1 + C₂α)^{n−p−1}/((p+1)ω²) · max{C₁α, C₂/(1 + C₂α)}`; the exponentially
shrinking admissible noise; the chain-like graph — "each node v_k is connected to precisely the preceding p + 1
nodes" — named as "the worst case scenario"; no polynomial bound anywhere; their own account of prior art ends
"We are not aware of any other results."

1. **Equation numbers.**  (2.30) and (2.33) are the numbers of the arXiv *HTML* rendering, which numbers every
   line of a display.  In the PDF, and in the paper's own cross-references ("see (2.6) and (2.7)"), they are
   **(2.6) and (2.7)**.
2. **"They state that the bound is unlikely to be tight."**  The sentence is: "While the constant was obtained in
   a worst-case scenario and is unlikely to be tight in more friendly (and less contrived) settings, …".  About
   the worst (chain-like) case itself they say only that their analysis "can only be accurate, if at all, in the
   very worst case".  They neither claim nor deny that the exponential growth is real there.
3. **"their general-position hypothesis is not uniform, ours is quantitative."**  Their explicit bound *is*
   quantitative: `α` is the largest squared aspect ratio and `ω` the smallest width of a landmark set — the
   counterparts of your `(D/τ)²` and `τ`.  What you add is the polynomial dependence on `n`, not quantitativeness.
4. **Citation.**  There is a journal version: SIAM J. Math. Data Sci. 7(3) (2025) 1077–1097 (from its Crossref
   record; the publisher's page refused the request, so its statement numbers were not compared).

A remark of the coordinator on the same paper: the lower bound of their Proposition 3.2 is realised by a dilation
of the configuration (`y* = ηx`, constant `1/(8δ)`, `δ` the maximum degree).  It is linear in the noise and blind
to bending; your description "a constant that does not depend on `n`" is right for a band graph and should not be
read as a statement about the growth law.

## 3. What to cite, and where

The report's §4 is a replacement for your "Prior art" paragraph on Theorem L, written to be pasted, with the
reading level of every attribution.  The pointers that matter most:

* at **Step 1** (one window): Arias-Castro–Javanmard–Pelletier, Theorem 1; for lattice simplices Alicandro et al.,
  Lemma 1.2, and Lazzaroni–Palombaro–Schlömerkemper, arXiv 1501.07505, Lemma 3.2;
* at **Step 2** (no reflection between consecutive windows): Alicandro–Lazzaroni–Palombaro, Lemma 1.3 — whose
  abstract says that interactions beyond nearest neighbours "have the role of penalising changes of orientation
  and, to some extent, they may replace the positive-determinant constraint"; the "flips" of Moore et al. 2004
  are the same object in the localisation literature;
* at **Step 3** (rotations of overlapping cells compared and accumulated): Mora–Müller 2003, proof of Theorem 2.1,
  where "iterative applications of the estimates (2.8) and (2.9) yield" the estimate with the factor
  `(|ξ|/h + 1)²` — and they add that the argument "follows closely the proof of Theorem 4.1 in" Friesecke–James–
  Müller 2002 (not opened by us); on lattices Schmidt–Zeman, Theorem 2.4;
* for **Theorem K(a)**: Lew et al., Theorem 1.6 and Proposition 7.7 (replace "[From memory of the literature; no
  full text read.]"); the constant there, `2π²K(K+1)(2K+1)/(3n²)`, is 2.5 times better than your `5π²/3`;
* in your "Related theory": arXiv 2006.08840 and 1908.04021 concern shells and the linear estimate, not rods;
  cite Mora–Müller, Scardia (arXiv 0803.0923) and Blanchard–Griso instead; the attribution to Conti–Zwicknagl is
  supported only through the introduction of arXiv 2608.00863 (Conti–Zwicknagl itself was not opened);
* Aspnes et al. (IEEE Trans. Mobile Comput. 5 (2006)), the paper that introduced lateration graphs, prints for
  the graphs of its hardness construction the "suspicion … that edge-length errors accumulate at most
  polynomially across the graph", without proof — the nearest thing to your statement in that literature.

**What may be claimed** (the report's words, which we endorse): "a discrete, distance-data version of the
thin-rod geometric rigidity estimate, which we did not find stated; it replaces the exponential constant of the
published global bound for band lateration graphs by `n⁴` (squared error) under a uniform non-degeneracy
assumption".  Not: a new mechanism; not: the first polynomial bound of any kind for chains of simplices.

## 4. What the search did not reach — the "not found" is conditional on this

Not read although relevant: B. Schrader, "Propagation of errors in schematic chains of triangles in space with
measured distances", Bull. Géodésique 86 (1967) 427–432 (title only; behind a paywall) and the classical geodesy
of trilateration chains (first-order error propagation — where a growth law along a chain of figures would have
been printed first); Luo–Wu, J. Optim. Theory Appl. 149 (2011) (error estimates for geometric build-up; abstract
only); Anderson–Shames–Mao–Fidan, SIAM J. Discrete Math. 24 (2010); the journal version of Arias-Castro–
Vishwanath; Friesecke–James–Müller 2002 and Blanchard–Griso 2009 themselves (known through restatements).  No
search in zbMATH or MathSciNet (no access); no citation chase of Mora–Müller, Daitch–Spielman or Kyng et al. —
the most likely way to find the transfer if it exists; nothing in languages other than English.  The report's
§5.2 has the full table, §5.3 the agent's own eleven errors and disclosures.

## 5. Not asked: how far the threshold (S) is from what is necessary, and what the theorem guarantees on physical geometries [the formula: P, two lines; the numbers: N, `theorem_l_threshold.py`]

The research owner's directive asks us to say where a general statement has guarantees that are empty in
practice, and to classify assumptions.  Your §6 already says that the constants are loose by two to three orders
and that (S) is `6·10⁻⁶` for a typical random chain.  Two things can be added.

**(a) The necessary size of a threshold.**  Reflect the points beyond `x_{i+3}` in the plane of
`x_{i+1}, x_{i+2}, x_{i+3}` (your own counterexample to dropping (S)).  No squared distance of separation at most
3 changes, exactly one of separation 4 does, and

    |x′_{i+4} − x_i|² − |x_{i+4} − x_i|² = 4 h_i⁻ h_i⁺,

`h_i⁻`, `h_i⁺` the signed heights of `x_i` and `x_{i+4}` over that plane (write `a = x_{i+4} − x_{i+1}`,
`c = x_i − x_{i+1}`, `n` the unit normal: `|a − 2(n·a)n − c|² = |a − c|² + 4(n·a)(n·c)`).  For that `Y` the right-hand
side of Theorem L is zero and `Y` is not congruent to `X`.  So **every** pointwise threshold in a statement of
this form is below `G = min_i 4|h_i⁻h_i⁺|`, and `G ≥ 4τ²/√3` (because `|h_i⁻| ≥ σ_min(P_i)/√3` and
`|h_i⁺| ≥ σ_min(P_{i+1})`).  Yours is `τ⁴/(73D²)`: smaller than `G` by a factor of at least `169 (D/τ)²`.

| geometry (20 points unless said) | `τ` | `D` | (S) as a squared distance | (S) as a distance error | `G` | `G` as a distance error | `G`/(S) | `6.9 b/τ²` |
|---|---|---|---|---|---|---|---|---|
| α-helix, Cα trace (radius 2.3 Å, rise 1.5 Å, 100° per residue) | 1.58 Å | 7.31 Å | 1.6·10⁻³ Å² | 1.3·10⁻⁴ Å | 34.5 Å² | 2.8 Å | 2.1·10⁴ | 10.5 per Å |
| strand-like trace (radius 0.94 Å, rise 3.3 Å), 160° per residue | 0.73 Å | 12.5 Å | 2.5·10⁻⁵ Å² | 9·10⁻⁷ Å | 6.2 Å² | 0.23 Å | 2.5·10⁵ | 49 per Å |
| the same, 170° | 0.38 Å | 12.5 Å | 1.7·10⁻⁶ Å² | 7·10⁻⁸ Å | 1.7 Å² | 0.063 Å | 9.6·10⁵ | 186 per Å |
| the same, 175° | 0.19 Å | 12.5 Å | 1.1·10⁻⁷ Å² | 4·10⁻⁹ Å | 0.43 Å² | 0.016 Å | 3.8·10⁶ | 734 per Å |
| the same, 180° (planar: the control) | 0 | — | — | — | 0 | 0 | — | — |
| random chains, unit bonds (of 20 drawn, the instances with the smallest and the largest (S)) | 0.21–0.31 | 3.1 | 2.8·10⁻⁶ to 1.3·10⁻⁵ | 4·10⁻⁷ to 2·10⁻⁶ | 1.7–2.1 | 0.26–0.33 | 1.7·10⁵ to 6.1·10⁵ | 74–155 |

(Every window of every instance: the flipped configuration reproduces all distances of separation at most 3 to
rounding, changes the one of separation 4 by `4h⁻h⁺`, is not congruent to the original, and the two height
bounds hold — asserted in the script.  "As a distance error" divides by twice the largest measured distance.)

**(b) What the theorem guarantees at its own threshold.**  With every admitted pair error at the threshold,
`‖η‖₂ = (S)·√(3n − 6)` and the theorem gives an RMSD (the Frobenius bound divided by `√n`) of
`6.9·bτ²/(73D²)·(n+1)·√(n(3n−6)) ≈ 0.16·b(τ/D)²·n²` — on the α-helix trace `0.029 n²` Å:

| α-helix trace, `n` | RMSD guaranteed at the threshold | radius of gyration | errors at which the guarantee is 1 Å, as a fraction of (S) | the same as a distance error |
|---|---|---|---|---|
| 12 | 4.2 Å | 5.7 Å | 0.24 | 3·10⁻⁵ Å |
| 20 | 11.8 Å | 9.0 Å | 0.085 | 1.1·10⁻⁵ Å |
| 100 | 295 Å | 43 Å | 0.0034 | 4·10⁻⁷ Å |

**Reading.**  (i) Theorem L, as stated, is a theorem about the *exponent*: it shows that errors of frames add and
do not multiply.  As a guarantee for data it is empty on these geometries — it needs distance errors of `10⁻⁴` Å
or less, and from sixteen residues on its bound at that noise exceeds the radius of gyration of the helix (the
closed form above against `√(r² + rise²(n² − 1)/12)`: 7.5 Å against 7.3 Å at `n = 16`).  By the directive's wording it is "a
general theorem with computationally vacuous guarantees" in its constants, and we suggest saying so next to the
statement, not only in §6.  (ii) In the directive's classes: `τ > 0` is **essential** (four coplanar consecutive
points: `h⁻ = 0`, the mirror image has the same data at every separation up to 4); a threshold on the
separation-4 errors is **essential in kind and replaceable by a weaker quantitative condition in size** — the
necessary size is `G`, of order `τ²`, the sufficient one is of order `τ⁴/D²`.  (iii) The row "strand-like" is a
statement about the *data*, not about your proof: on an extended segment the separation-4 distances distinguish
a window from its mirror image by a few hundredths to a few tenths of an ångström only, so sequence-local
distances fix the handedness of such a segment only if they are that accurate — whatever theorem is used.

**Three questions this raises** (proposals; the first is the one we would ask a referee of the theorem):
1. Does Theorem L hold with (S) replaced by `|η_{i,i+4}| ≤ c·|h_i⁻h_i⁺|` window by window, for an absolute
   `c < 4` — a threshold of the size the reflections dictate, local rather than governed by the worst window?  Or
   is there a competitor that is not a reflection at one plane and shows that a factor `(τ/D)²` is necessary?
2. A constant in which a thin window costs locally (`Σ_i 1/τ_i²`-like) rather than through `min_i τ_i` — your own
   open end; on the strand table the constant changes by a factor of 15 between 160° and 175°.
3. What separations 5 to 7 buy on strand-like segments: the reflection at one plane changes those distances by
   products of heights of points further out, which are larger — is there a version of (S) with the gap of the
   widest measured separation?

## 6. Requests (A4-GEO-1 … -6; proposals)

1. Amend the summary sentence of your §0 as in the report's §4 ("The published *global* perturbation bound … in
   the localisation literature is exponential in `n`; for the first-order problem polynomial bounds are in
   print, and the continuum analogue — the geometric rigidity estimate in a thin rod — has exactly this
   scaling.").
2. Replace the "Prior art" paragraph on Theorem L by the text of the report's §4, or by your own with the same
   attributions; correct the four points of §2 above.
3. Theorem K(a): the references and the better constant of §3 above.
4. The row of your `PRIOR_ART.md` for Theorem L: "not found as stated; mechanism and scaling known", with the
   list of what the search did not reach.
5. Say next to Theorem L that its constants make it a statement about the exponent (§5), and state the necessary
   size `4|h⁻h⁺|` of the threshold if you agree with the two-line computation.
6. If anyone in the collaboration has library access: Schrader 1967 and Luo–Wu 2011 are the two unread items most
   likely to contain a growth law for chains (no expenditure is proposed here; this is a question to the
   research owner's side, not a request to spend).

## Assumptions and limitations

One agent, forty-five minutes, 33 texts opened, one read in full; the journal versions of several papers were not
compared with the arXiv texts read.  The category "the transfer not in print" is a statement about that search.
The scaling comparisons between the rod estimates and Theorem L (`(b/τ²)n²` "up to constants") were made by hand
by the agent and take your statements as given.  §5 takes Theorem L as stated; the proof was not read line by
line by anyone here, and the geometries of the table are idealised traces (constant radius, rise and turn), not
structures from a database.  The agent read the papers from text extractions of direct downloads of public
addresses; six addresses were refused by their servers and not retried by another route.

## Requested response

None required.  We would like to know whether question 1 of §5 is one you can answer quickly — a competitor that
forces the factor `(τ/D)²` would be as informative as a proof of the sharper threshold.
