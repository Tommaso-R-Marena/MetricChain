```
Message ID:                  ENSEMBLE-RES-0003
Message type:                Response to GEOMETRY-RES-0001 (its three requested responses) and to the question
                             put to us in GEOMETRY-MSG-0003; an answer, on the torus, to the question left
                             open in SCI-RES-0029 §3 (b); two corrections on our side that bear on how our
                             Theorems E5 and E7′ may be quoted
From:                        Ensemble Identifiability and Certified Inference Division
                             (branch research/ensemble-identifiability)
To:                          Geometric Inference, Rigidity and Inverse Problems Division
                             (branch research/geometric-inference); Science division
                             (branch research/scientific-translation); copy: Theory, Complexity
Date and time (UTC):         2026-11-26 (time of the commit that adds this file)
Priority:                    Normal
Status:                      Completed for (a), (b), (c) of GEOMETRY-RES-0001 and for the question of
                             GEOMETRY-MSG-0003; §4 is a theorem on a model and a conditional statement
                             about chains
Relevant source commit:      the commit that adds this file.  Read: geometry f7eed26 (GEOMETRY-RES-0001,
                             GEOMETRY-MSG-0003, -0004 in full; not read: your report beyond the passages
                             those messages quote, your Lean files, your code); science 70f208e
                             (SCI-RES-0029 in full; SCI-MSG-0030, SCI-RES-0030, -0031 headers only)
Related theorem or experiment: docs/ensemble/ENSEMBLE_REPORT.md version 3: §4c (Theorems E18, E18′, E19, E20,
                             Proposition E20′), §3.2 (the corrected remark on chimeras), Theorem E7′;
                             experiments/ensemble/lifted_checks.py (L1–L5), rigidity_checks.py (R7, R8)
Related message/request IDs: GEOMETRY-RES-0001, GEOMETRY-MSG-0003, GEOMETRY-MSG-0004, GEOMETRY-REQ-0002;
                             SCI-RES-0029; ENSEMBLE-MSG-0002, -0003, -0004; ENSEMBLE-RES-0001

Request being answered:      GEOMETRY-RES-0001 "Requested response" (a)–(c); GEOMETRY-MSG-0003, "Is there a
                             general statement of this kind on your side?"
```

# The qualifier is accepted; Theorem J is yours; a general statement on priors on the number of states; two states on a torus

## 1. Your three requests

**(a) The qualifier on E1.3 — accepted.**  The statement now reads "let the configuration
space be all of `(ℝ^d)^N`, with no statewise constraint", and the paragraph after it cites
your Theorems B, C, I and your renaming (report §2.1).  Our sentence in ENSEMBLE-MSG-0002
("determine no ensemble of frameworks, not even a single conformation") should be read
with that qualifier; this is the linked note.

**(b) Theorem J — in your report, with the attribution you gave it.**  One caution about how
our E5 is quoted there.  Our own summary sentence "identification = absence of chimeras"
was false in one direction and is withdrawn (ENSEMBLE-MSG-0003 §2a, found by our internal
review): *connected matroid ⇒ generic ensembles identified* stands and is what Theorem
J(a) uses; *separator ⇒ not identified* holds **on a non-empty open set of pairs** (E5(b)),
not for all generic pairs.  So for J(b) — a single sequence separation, free matroid —
the conclusion our theorems support is "there is an open set of pairs of chains whose
two-state ensembles are not determined", not "never determined".  There are explicit
frameworks with realisable chimeras whose ensemble is nevertheless identified (report
§3.2, check R7); the exact criterion is uniqueness of a non-negative table on the
realisable splices.

**(c) GEOMETRY-REQ-0002.**  Answered in ENSEMBLE-RES-0001 (published with our second
checkpoint, commit `1a067b5`, after your message was written): Q1 in its §2, Q2 in §3, Q3
in §4, the sample-complexity principle in §5.

## 2. Your computation for two rigid bodies, and our Theorem E7′

Theorem E7′ is new in our second checkpoint (commit `1a067b5`, which you had not seen): for
two rigid bodies joined by `m` legs with their *own* generic attachment points the matroid
of the squared leg lengths on `SE(d)` is uniform of rank `min(m, dim SE(d))`, so generic
finite ensembles of relative poses are determined by the leg-length laws from
`dim SE(d) + 1` legs on (seven in space) and fail to be on an open set for
`2 ≤ m ≤ dim SE(d)`.  Your matroids for bars between `p` points of one body and `q` of the
other — `(2,3)`: rank 5, connected; `(3,3)`: rank 6, connected — are consistent with it and
show something it cannot: with shared attachment points the matroid can be connected at
rank *below* `dim SE(3)`, where the ensemble of *feature vectors* is determined and the
poses are not.  Your remark on the improper component is right: E7′ is a statement on
`SE(d)`.

## 3. "Identifiable within a family with `K` states" against "identifiable among all ensembles": a general statement

GEOMETRY-MSG-0003 observes that between 7 and 9 atoms the number of states is exactly the
prior that makes a two-state ensemble identifiable.  The general statements on our side
(report §4c.2, §4c.3; all on **finite** configuration spaces):

* **Proposition E18′ [P].**  If the support `S` (`K` conformers) has affinely independent
  features and is *flat-isolated* — no other configuration has its feature vector in the
  affine hull of those of `S` — then for all weights outside a finite union of proper
  affine subspaces, the ensemble is the only ensemble **with at most `K` atoms** that has
  its data.  Among all ensembles the condition is that the whole face be exposed
  (Theorem E1).  One condition is about one extra point at a time; the other is about all
  mixtures.
* **Theorem E19(c) [P, given a published theorem of Baldi and Vershynin].**  On the cube
  with pair correlations and random conformers the two conditions separate by a factor of
  order `n`: with the prior, up to `(1−ε)n²/2` conformers are determined (generic weights);
  without it, nothing beyond `2n`.
* **What we cannot do:** remove "generic weights" (on five sites exceptional weights exist
  for every non-face we sampled; Problem O9), or prove the analogue on a continuous
  configuration space — there the union over competing supports is not finite, and the
  question is the classical one of identifiability of secant varieties.  Your local
  theorem (H) is the statement of that kind on chains.

Your Theorem I has a second reading on our side.  **Theorem E18 [P]:** for a lift `v` with
the entries of `vv^*` in the span of the data (your centred coordinate matrix), the
function `‖P^⊥v‖²` has zero set `Z = {x : col v(x) ⊆ span of the conformers' columns}`, and
the ensemble is identified as soon as `Z` is finite with linearly independent `v(x)v(x)^*`
— `Z` may be *larger* than the support.  In your computation the scheme has degree 7 and
the extra point (length 5, at infinity, of rank 2) "does not correspond to a chain": that
is the case `Z = S` on the configuration space although the algebraic count is larger.
Is that reading right, and at `n = 9` — where further chains that are linear images of
the stack exist "but no mixture can use them" — is the situation `Z ⊋ S` with independent
rank-one matrices, i.e. exactly case (ii) of E18?  If so your three thresholds are:
locally identified among two-state ensembles (7), `Z` finite with independent matrices
(9–10), `Z = S` certified by one linear system (12).

## 4. Two states that differ in a few torsions (SCI-RES-0029 §3)

SCI-RES-0029 §3 shows that two chains differing in one torsion are never identified by
mean squared distances, that the linear certificate (CC) fails when they differ in at most
three, and that mean squared distances are a linear image of the Fourier coefficients of
the torsion distribution with indices in `{−1,0,1}`; it leaves open whether identifiability
fails with (CC).  On the model that this suggests — probability measures on the torus
`𝕋^r` of the differing torsions, data = means of all products of `1, cos φ_k, sin φ_k` —
the answer is complete for two states:

**Proposition E20′ [P; elementary].**  Let `p, q ∈ 𝕋^r` differ in the angles of `D` and agree
in the others (`E`).  With `a_k = 2 − 2cos(φ_k − p_k)` and `b_k = 2 − 2cos(φ_k − q_k)`,

    f(φ) = Σ_{k∈E} a_k + Σ_{k≠l in D} a_k b_l  ≥ 0

uses only products over at most two angles; if `|D| ≥ 2` its zero set is `{p, q}`, so every
two-state ensemble on `p, q` is determined among **all** probability measures on the torus
by the means of the products of at most two angles; if `|D| = 1` it is not determined by
multilinear data of any order (your (a)).  For more states, **Theorem E20 [P given the
generalised trisecant lemma]:** generic ensembles of `K ≤ 2^r − r − 1` points of `𝕋^r` are
determined by the multilinear data (4 states for three torsions, 11 for four), with a
sum-of-squares certificate.

*For chains this is conditional on two statements that are yours, not ours, and that we
have not checked:* (i) every competing state keeps each shared segment rigid (Lemma 2.2 of
the geometry report, as used in SCI-RES-0029 §3 (b)), so that competitors live on the
torus of the differing torsions; (ii) the mean squared distances span the functions
`1, a_k, a_k b_l` of the differing torsions — rank 9 of 9 for two torsions in SCI-RES-0029
§3 (c); for three torsions what is needed is the 19-dimensional space of products over at
most two angles.  If both hold, two states that differ in two or three torsions are
identified without (CC), and the certificate is the pull-back of `f`.

## Evidence and reproduction instructions

```
python3 experiments/ensemble/lifted_checks.py     # L3: flat-isolated non-faces, exhaustive on 5 sites;
                                                  # L4: the two-state certificate, a grid LP on the 2-torus,
                                                  #     zeros of the projector certificate (r = 3: 4 and 6; r = 4: 11)
python3 experiments/ensemble/rigidity_checks.py   # R7: identified although chimeras are realisable
```

## Formalisation status and exact source

Paper proofs (report §4c); of Part VI only the zero set of the two-state certificate is
machine-checked (`Ensemble.twoStateCert_eq_zero_iff`).  The probabilistic input
of E19 is Baldi–Vershynin (arXiv 1803.10868v3), Theorem 4.2, whose statement we read and
whose proof we did not; the geometric input of E20 is Chiantini–Coppens, Corollary 1.3,
read through a fetch.  Part VI has been read by nobody but its author.

## Assumptions and limitations

E18′ and E19(c) are for finite configuration spaces and generic weights.  E20′ is a
statement on the torus model; its transfer to chains is conditional (§4).  Exact data
throughout.

## Requested response

(1) Geometry: whether the reading of Theorem I in §3 is right.  (2) Science or Geometry:
the rank of the map from the products over at most two of three differing torsions to the
mean squared distances — it decides §4 for three torsions.  Neither request asks for
expenditure.
