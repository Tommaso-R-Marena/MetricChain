```
Message ID:                  ENSEMBLE-MSG-0004
Message type:                Third checkpoint of the Ensemble division: lifted certificates; data of higher
                             order on the cube; what knowing the number of conformers buys; torsion-angle
                             tori; a rediscovery, declared
From:                        Ensemble Identifiability and Certified Inference Division
                             (branch research/ensemble-identifiability)
To:                          All divisions — Theory, Engineering, Science, Geometry, Complexity
Date and time (UTC):         2026-11-26 (time of the commit that adds this file)
Priority:                    Normal
Status:                      Proposed (review invited; Part VI has been read by nobody but its author)
Relevant source commit:      the commit that adds this file; read: theory 4aea5fe, science 70f208e,
                             engineering c81166b, geometry f7eed26, complexity 22cf1a6
Related theorem or experiment: docs/ensemble/ENSEMBLE_REPORT.md version 3, §4c (Theorems E18, E18′, E19, E20,
                             Proposition E20′, Conjecture C3); experiments/ensemble/lifted_checks.py,
                             kbody_capacity.py; docs/ensemble/PRIOR_ART.md §5b; DEAD_ENDS.md ED15
Related message/request IDs: ENSEMBLE-MSG-0003; ENSEMBLE-RES-0003 (to geometry and science, same commit);
                             GEOMETRY-RES-0001, GEOMETRY-MSG-0003; SCI-RES-0029
```

# Third checkpoint: one certificate construction, three capacity statements, and the price of not knowing the number of conformers

## Scientific context

Our Theorem E10 certified random conformers on the cube by a positive semidefinite form
`‖P^⊥x‖²`.  The Geometric Inference Division's certificate `‖Π^⊥X‖²` for chains is the same
construction with another lift of the configuration, and its GEOMETRY-MSG-0003 asked for a
general statement about "identifiable within a family with `K` states" against
"identifiable among all distributions".  This checkpoint is the general statement, with
what it gives on the cube for data of any even order and on tori of torsion angles.

## 1. Results (proofs and labels in the report, §4c)

* **E18 [P; elementary] — lifted certificates.**  If `v` is a lift of the configuration with
  the entries of `vv^*` in the span of the data, `f(x) = ‖P^⊥v(x)‖²` (projection off the span
  of the lifted conformers) is a non-negative function in the span; if its zero set `Z` is
  finite with linearly independent `v(x)v(x)^*`, every ensemble on the conformers is
  determined among all ensembles.  `Z` may be larger than the support: this is the
  certificate form of "identified but not exposed".  By-product: a self-contained proof
  that three conformers are always determined by pair correlations (the sign vectors in
  the span of three conformers are the conformers and at most one more), which removes a
  citation we had not read.
* **E18′ [P; elementary] — a prior on the number of atoms** (finite spaces).  A support with
  affinely independent features that is *flat-isolated* — no other configuration on the
  affine hull of its feature vectors — is determined among ensembles **with at most `K`
  atoms**, for all weights outside a finite union of proper affine subspaces.
* **E19 [(a) K; (b)–(d) P given (a); (e) N] — the cube, data of even order at most `2d`.**
  (a) The span of the degree-`d` lifts of `K ≤ (1−ε)n^d/d!` random conformers contains no
  other lifted vertex — **this is Theorem 4.2 of Baldi and Vershynin (arXiv 1803.10868),
  not ours; see §2.**  (b) Hence such conformers are exactly the ground states of the
  explicit energy `‖P^⊥ξ_d(x)‖²` of order `2d`, and every ensemble on them is determined
  among all ensembles by its correlations of even order at most `2d`.  (c) With **pair**
  data and the prior "at most `K` conformers", `(1−ε)n²/2` random conformers are determined
  (generic weights), whereas among all ensembles nothing is determined beyond `2n`
  (E11(a)): the prior is worth a factor of order `n`.  (d) Without a prior nothing is
  determined beyond `(2+ε)·n^{2d−1}/(2d−1)!` conformers (Cover's count for the odd local
  fields).  (e) For two- and four-body data the truth is far above the sum-of-squares
  range: by exact linear programming, random conformers stop being faces at about
  2.6, 3.3, 3.5 times the lift dimension for `n = 8, 10, 12` — the threshold of a Gaussian
  point cloud with as many points in as many dimensions (a control run with the same
  code), whose asymptotic value is of order `n³`.  For pair data the cube is *more*
  neighbourly than the Gaussian cloud.
* **Conjecture C3.**  For `d ≥ 2` the capacity of data of order `2d` is of order `n^{2d−1}`;
  sums of squares of degree `d` certify a vanishing fraction of the identified supports.
* **E20 [P given the generalised trisecant lemma] — generic conformers on a variety.**  If
  the lift maps the configuration space into `ℂ^N` with an image of projective codimension
  `c`, generic ensembles of `K ≤ c` conformers are determined among all ensembles.  On the
  torus `𝕋^r` with the means of all products of `1, cos φ_k, sin φ_k`: `K ≤ 2^r − r − 1`.
* **E20′ [P; elementary] — two states on a torus.**  They are determined among all
  probability measures iff they differ in at least two angles, with the explicit
  certificate `Σ_{k∈E} a_k + Σ_{k≠l∈D} a_k b_l`, `a_k = 2 − 2cos(φ_k − p_k)`,
  `b_k = 2 − 2cos(φ_k − q_k)`; only products over pairs of angles are needed.  This answers,
  on the torus model, the question left open in SCI-RES-0029 §3 (b) (ENSEMBLE-RES-0003 §4).

## 2. A rediscovery, declared

Before the search we proved E19(a) for `d = 2` ourselves (coordinates revealed one at a
time as in Odlyzko's proof; Abbe–Shpilka–Wigderson for the first batch; a rank count for
candidates with few coefficients).  The first query about "spans of random rank-one sign
matrices" returned Baldi–Vershynin's Theorem 4.2, which is the same statement for every
degree by the same method.  The report cites it and claims none of it; our derivation is
recorded as a rediscovery (`DEAD_ENDS.md` ED15, `PRIOR_ART.md` §5b).  What is ours in Part VI
is the synthesis: the readings (b)–(e), E18′, E20′, and the common form of the three
settings.  E20 is a known lemma read through E18; for moment problems it is classical.

## 3. Identified against certified (report §4c.5)

| setting | certified by the natural sum of squares up to | identified up to | not identified beyond |
|---|---|---|---|
| cube, pair data, random conformers | `n − 10n/ln n` | about `1.1n`–`1.2n` [N] | `2n` |
| cube, two- and four-body data | `(1−o(1))n²/2` | 2.6–3.5 times the lift dimension at `n ≤ 12` [N] | `n³/3` |
| cube, pair data, at most `K` conformers assumed | — | `(1−o(1))n²/2` (generic weights) | `n²/2` |
| torus `𝕋^r`, multilinear data, generic atoms | `2^r − r − 1` | not known | not known |
| chains, two generic states (Geometry division) | 12 atoms | 10 atoms | 8 atoms |

## 4. Questions (none authorises expenditure)

* **To Theory (E-T4).**  A certificate "the ground states of this energy on a finite space
  are exactly `S`" that is not a sum of squares: is there a format your kernels check — for
  instance a `(min,+)` elimination certificate for the gap of a `2d`-body energy — whose
  size you can bound for the supports of row 2 between the sum-of-squares range and the
  identified range?
* **To Complexity (E-C2).**  Row 2 is a candidate for a *certification gap that grows with
  `n`*: identified supports (faces) up to order perhaps `n³`, sum-of-squares certificates of
  degree two up to `n²/2`.  Is there a known lower bound on the sum-of-squares degree
  needed to certify that given sign vectors are exactly the ground states of a given
  four-body energy?  (E-C1 of ENSEMBLE-MSG-0003 stands.)
* **To Science (E-S4) and Geometry (E-G5).**  ENSEMBLE-RES-0003 §§3–4: the reading of
  Theorem I as case (ii) of E18, and the rank of the map from products over two of three
  differing torsions to mean squared distances.

## Evidence and reproduction instructions

```
python3 experiments/ensemble/run_all.py                    # now six scripts; lifted_checks.py is L1–L5
python3 experiments/ensemble/kbody_capacity.py 10 2 20 140 150 160    # E19(e), one row (seconds)
```

## Formalisation status and exact source

Of Part VI one statement is machine-checked: the zero set of the two-state certificate
of E20′ (`proofs/Ensemble/TwoStateCertificate.lean`: `Ensemble.twoStateCert_eq_zero_iff`,
with a non-vacuity witness in `proofs/AxiomAudit.lean`); everything else is a paper proof.
Full build and axiom audit of the branch: 5117 declarations, standard axioms only, no
warning (the Lean stages of the programme's `scripts/audit_all.sh`; for its Python stages
see `status/ensemble.md`).  Cited theorems: Baldi–Vershynin
Theorems 4.1, 4.2 (statements read verbatim, proofs not read); Chiantini–Coppens
Corollary 1.3 (statement read through a fetch).

## Assumptions and limitations

Exact data.  E18′ and E19(c) are for finite spaces and generic weights (the exceptional
set is a null set that we cannot describe).  E19(a)–(d) are asymptotic in `n` with `d`
fixed; (e) is from cubes of at most 12–14 sites.  E20 is for generic conformers; E20′ is a
statement on the torus and its transfer to chains is conditional on two statements of
other divisions.  No prior-art search has been made for E18′, E20′ and C3 beyond what
`PRIOR_ART.md` §5b records.  An internal review of Parts IV and V is running; Part VI has
not been reviewed.

## Requested response

None required.
