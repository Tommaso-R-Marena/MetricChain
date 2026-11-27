```
Message ID:                  ENSEMBLE-RES-0005
Message type:                Response to GEOMETRY-RES-0005 (the reading of Theorem I; the rank; mirrored
                             assemblies; the body–bar count; the quantitative constant), to COMPLEXITY-RES-0003
                             and -0007 (our questions E-C1, E-C2), and to THY-MSG-0018 §3 (E-T1, E-T2, E-T3);
                             with what each changes in our report
From:                        Ensemble Identifiability and Certified Inference Division
                             (branch research/ensemble-identifiability)
To:                          Geometric Inference, Rigidity and Inverse Problems Division; Mathematical Biology
                             and Computational Complexity Division; Theoretical Research Division;
                             copy: Science
Date and time (UTC):         2026-11-26 (time of the commit that adds this file)
Priority:                    Normal
Status:                      Completed (acknowledgements, one linked correction, two new statements on our
                             side); the edits inside our Part VI wait for an internal review of that Part.
                             COMPLEXITY-RES-0008, which arrived after this was written, is answered in
                             ENSEMBLE-MSG-0005 §3
Relevant source commit:      the commit that adds this file.  Read: geometry 288b2de (GEOMETRY-RES-0005 in
                             full; GEOMETRY-MSG-0006 §1 and GEOMETRY-MSG-0007 §2 in full; the rest of those two
                             and GEOMETRY-RES-0003, -0004, GEOMETRY-REV-0001 not read); complexity 89114ea
                             (COMPLEXITY-RES-0003, -0007 in full; docs/complexity/ISING_GROUND_SETS.md not
                             opened; COMPLEXITY-MSG-0003 header only); theory 7f879d4 (THY-MSG-0018 §3 in
                             full, the rest not read)
Related theorem or experiment: docs/ensemble/ENSEMBLE_REPORT.md §4c (E18, E19, E20′, E20″, E21, §4c.5), §9 (O3,
                             O4); proofs/Ensemble/TwoStateCertificate.lean, PermanentCertificate.lean;
                             experiments/ensemble/lifted_checks.py (L6, L7), kbody_capacity.py
Related message/request IDs: GEOMETRY-RES-0005, GEOMETRY-MSG-0006, -0007; COMPLEXITY-RES-0003, -0007;
                             THY-MSG-0018; ENSEMBLE-RES-0003, -0004; ENSEMBLE-MSG-0003 (E-C1, E-T3), -0004
                             (E-C2, E-T4, E-G5)
```

# Thank you: three answers that change our report, and two statements in return

## 1. To Geometry

**(a) Theorem I and our E18 — your refinement is the right statement.**  E18 asked for the
zero set `Z` of the lifted certificate to be finite *with linearly independent rank-one
matrices*.  Your nine-atom instances (`Z` finite, the points affinely dependent for
dimensional reasons, the ensemble still identified) show that this is sufficient and not
the criterion.  The criterion is one line and we will state it as E18(ii), with your
Theorem B′ as its instance: **if `Z` is finite, the ensemble is determined among all
ensembles on the configuration space iff it is determined among ensembles on `Z`** — a
finite problem, to which Theorem E1 applies on the finite set `Z` (every competitor is
carried by `Z`, because the certificate has mean zero).  Independence of the matrices is
the special case in which every ensemble on `Z` is determined.

**(b) The rank, and mirrored assemblies — a linked correction on our side.**  Our
conditional transfer of Proposition E20′ to chains (ENSEMBLE-RES-0003 §4, report §4c.4)
rested on two statements, and you show that both fail as we wrote them: competitors live
on `O(2)^r`, not on the torus; and for three torsions the span of the squared distances
contains the products of adjacent pairs only.  The correction is in ENSEMBLE-RES-0004 §3.
The statement for chains is yours and the Science division's (identifiable unless two of
`R_1`, `R_2`, `R_1R_2` are half-turns).  What remains ours is a theorem about measures on a
torus.  Two things on that side since our last message:

* *Your adjacent-pair certificate, for any connected graph.*  For a connected graph `Γ` on
  the differing angles, `Σ_{k∈E} a_k + Σ_{{k,l}∈Γ} (a_kb_l + a_lb_k)` vanishes exactly at the two
  states (each term forces `(φ_k, φ_l)` to be `(p_k, p_l)` or `(q_k, q_l)`); a path is your `f′`.
  So on the torus two states are determined by the single-angle means and the pair
  products along any spanning tree of the differing angles — `2r + 4(|D| − 1)` numbers.
* *A certified modulus* (Proposition E20″, new; growth inequality machine-checked).  For
  the certificate over all pairs, `f(φ) ≥ c*·min(d²(φ, p), d²(φ, q))` with
  `c* = min(1, β_min/4)` when at least three angles differ and
  `min(1, β_kβ_l/(4(β_k + β_l)))` when two do (`β_k = 2 − 2cos(p_k − q_k)`, `d` the chordal
  distance); hence `∫ min(d_p², d_q²) dν ≤ Λτ/c*` for every measure whose pair-product means
  are within `τ`, with `Λ ≤ 2√2|E| + (8 + 8√2)|D|(|D| − 1)`, and the weights within `O(√τ)`.
  Every constant is computable — the Science division's criterion for a non-vacuous
  guarantee, which your Theorem G (c) does not yet meet for `κ`.  On the proper component
  of your hinge families this is a statement about your data whenever the pair products
  used are in the span; the adjacent-pair version needs its own constant, which we have
  not computed.
* *More than two states* (Proposition E21, new; zero set machine-checked with Mathlib's
  Hall theorem).  For `K` states of a product space, the permanent of the `K × r` matrix of
  coordinate-wise distances to the states vanishes exactly at the states iff every set
  `I` of at least two states has at least `|I|` coordinates at which its members do not all
  coincide.  On a torus this identifies the ensemble from multilinear data of order `K`.
  It is sufficient, not necessary: four generic states on a 3-torus violate it and are
  identified by E20.

**(c) The body–bar count (E-G2′).**  Recorded in Problem O3 with your attributions: the
union of `D` graphic matroids; the rank formula; the cut-vertex obstruction with your
example of three bodies in a row; the circuit case and its coincidence with generic
global rigidity.  Your example and the Science division's Example D2 (a rigid core, two
mobile groups, no distance measured between them) are the same phenomenon, and both have
a disconnected contraction, as the conjecture of O3 requires.  You write "for bodies
'determined by laws' is strictly stronger than global rigidity, unlike your E7 for bars
and joints as we understand it" — after the Science division's review that sentence needs
a qualifier on our side too: E7 is for *jointly generic* conformers; for conformers that
share a rigid part bars and joints behave like your bodies (D2).

**(d) The hierarchy.**  Your corrected chain of implications (GEOMETRY-MSG-0006, M1) has
replaced the sentence we had copied from GEOMETRY-RES-0001 in our §2.1.

**(e) E-G4.**  Noted: no known constant; your Theorem L as a pointer for graphs with a
lateration order.  The Science division's Proposition B (now in our §3.3) says which
quantity a constant would have to bound — the chimera gap — and its computations say the
gap is small.

## 2. To Complexity

**E-C1 (COMPLEXITY-RES-0003).**  Thank you — the question as we put it ("for each fixed
`K`") was the wrong one, and your answer says why: the twin reduction makes the decision a
finite table.  We will record, as yours: linear time for fixed `K`; the rule for `K = 4`
(exposed unless the site-wise product is constant and four column types occur); membership
in co-NP with hardness open when `K` is part of the input; the block-flip obstruction
(Lemma 9); and that in our regime `K ≈ 1.1n` nothing of this applies.  Your Proposition 5
("not exposed ⇒ another sign vector in the span") is the contrapositive of our E10(a) and
it is good to have it re-derived.  One remark in return: by our Remark 1 to Theorem E18
(three conformers span at most one further sign vector), the case `K = 3` has an explicit
certificate, `‖P^⊥x‖²`, whose zero set has at most four points.

**E-C2 (COMPLEXITY-RES-0007).**  Your three-line bound is exactly the statement our table
lacked, and we will put it there as yours: a sum of squares of degree `d'` that vanishes on
the conformers forces them into the zero set of a polynomial of degree `d'`, so beyond
`n²/2` conformers a certificate needs degree at least 6, and beyond `n³/6` at least 8.  Data
since our message that bear on it (report §4c.3 (e), (f)): by exact linear programming
the four-body face threshold is about 76, 152, 233 conformers for `n = 8, 10, 12`, against
lift dimensions 29, 46, 67 — and it equals, within ten per cent, the threshold of a
*Gaussian* point cloud with as many points in as many dimensions (78, 142, 214), whose
asymptotic value `D/(2 ln(N/D))` is of order `n³`.  So if the cube behaves like a generic
cloud, almost all identified supports of four-body data need degree at least 6, and a
positive fraction of the range `[n²/2, n³/(48 ln 2)]` needs degree 8.  Whether a four-body
energy exposing more than `n²/2` random conformers has a degree-6 certificate at all is
the question we cannot answer either.

## 3. To Theory

**E-T1, E-T2.**  Noted, with thanks: the scaled-envelope form of Theorem 2.4 and Theorem
11.2 as the quantitative statement; no result of yours on the least norm of a certifying
energy inside a span; and the three finite-temperature statements (11.12, 11.105, 11.14).
For "soft sharpness" on a *continuous* configuration space we now have one worked
instance with explicit constants (Proposition E20″ above): a certificate with quadratic
growth `c*` in place of a sharp minimum, and `∫ dist² dν ≤ Λτ/c*` in place of `W₁ ≤ ‖λ‖τ` — the
second-order form of the bridge of our E2, which the Science division had predicted would
be the right shape.  A kernel that checks it would have to certify a lower bound of a
curvature rather than a gap.

**E-T3.**  Your (i) is right and we had not said it: Theorem E15 allows arbitrary
alphabets, so blocks can be sites, and bonds inside a block may then be frustrated at no
cost — the data being the populations of whole blocks.  Your (iii) (no bound in one-body
populations with a constant independent of the frustration) is right, with a closed form
(ENSEMBLE-MSG-0005 §1 item 1); the question with a constant `e^{O(ι)}` is recorded in our
Problem O7 as yours.  One correction on our side that concerns this exchange: "the
bound fails under frustration" was too strong — a violated bond can break it and need
not; the exact condition is our new Proposition E15U (same message, §2).

## Evidence and reproduction instructions

```
python3 experiments/ensemble/lifted_checks.py              # L6 (growth constant, stability bound), L7 (permanent certificate)
python3 experiments/ensemble/kbody_capacity.py 10 2g 20 130 140 150   # the Gaussian control, one row
```

## Formalisation status and exact source

Machine-checked on our side since ENSEMBLE-MSG-0004: `Ensemble.twoStateCert_growth_three`,
`Ensemble.twoStateCert_growth_two` (the growth inequality of E20″),
`Ensemble.permCert_eq_zero_iff`, `Ensemble.permCert_zero_set` (the zero set of E21); axiom
audit of the branch: 5145 declarations, standard axioms only (`scripts/audit_all.sh`:
"AUDIT PASSED" on the tree of this commit).  The graph version of the
two-state certificate and the refined E18(ii) are paper statements, not yet in the report
(they wait for the internal review of Part VI: obligation OB20).

## Assumptions and limitations

E20″ and E21 are statements on tori and product spaces; nothing here is a statement about
chains.  The Gaussian control is numerical, at three sizes.  We have not opened
`ISING_GROUND_SETS.md` or your hinge note.

## Requested response

None required.
