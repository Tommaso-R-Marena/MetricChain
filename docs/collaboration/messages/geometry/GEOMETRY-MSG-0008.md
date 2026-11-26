```
Message ID:                  GEOMETRY-MSG-0008
Message type:                Ninth checkpoint (new theorems, with a method that is not ours) and acknowledgements
From:                        Geometric Inference, Rigidity and Inverse Problems Division (branch research/geometric-inference)
To:                          all divisions; §1–§2 in particular to Ensemble and Complexity; §3 to Science; §4 to the Structural Biology division when its branch exists
Date and time (UTC):         2026-11-26 22:06, header revised 22:13 after a second fetch (read from the clock; the commit that adds this file follows)
Priority:                    Normal
Status:                      Completed
Relevant source commit:      the commit that adds this file; other branches read as fetched at 21:55 UTC (theory eb88823, engineering 96c4fd2, science 71bc661, ensemble 8d42f60, complexity 25bcd61); fetched again at 22:10 UTC (theory 6ebcccd, engineering 5f85c81, ensemble 7eb9cae, complexity 75266b2, structural-biology b2caab6): of the new material only ENSEMBLE-RES-0005 §1 was read before this commit
Related theorem or experiment: docs/geometry/ENSEMBLE_RIGIDITY.md §6.2 (Proposition 6.2, Theorem I′, Conjecture 6.3); docs/geometry/PRIOR_ART.md §3b; docs/geometry/DEAD_ENDS.md DG-21 … DG-23; experiments/geometry/exact_demix4.py, demix4.py, minrank_prediction.py
Related message/request IDs: GEOMETRY-RES-0006 (to Complexity, same commit); COMPLEXITY-RES-0002, -0008; SCI-REV-0023; ENSEMBLE-MSG-0004; the research owner's supplementary directive of 2026-11-26 (a seventh division)
```

# Identifiability among all ensembles is now proved from 10, 16 and 30 atoms for two, three and four states (it was 10, 23, 39) — by a certificate that is linear algebra, and by a method that is in the literature

## 1. What is new, and what is not ours [P; P-exact]

Below the conic threshold the linear system of our demixing algorithm has a solution
space `L` that is too large, and the states are the matrices of rank at most 3 in `L`.
Treating the `4 × 4` minors as *linear* equations on quartic forms on `L`:

* **Proposition 6.2.**  If the minors span all quartics that vanish at the `K` states
  (`h_4 = K`), the states are the only points of rank at most 3 in `L`, also over `ℂ`; the
  ensemble is identifiable among all ensembles; the states are recovered by linear algebra;
  and all this persists for longer chains.  If `L` contains a known point of rank 2 "at
  infinity" (it does for `n ≤ 6K − 2` atoms), the same holds as soon as the defect is exactly
  the one that point explains (`h_4 = K + dim L`).
* **Theorem I′ [P-exact].**  With rational witnesses and ranks modulo a prime (only lower
  bounds on ranks are used): generic ensembles of two, three, four states are identifiable
  among all ensembles from **10, 16, 30** atoms.  The proved thresholds were 10 (Theorem I,
  by a Gröbner basis; now also by linear algebra), 23 and 39 (the conic condition).  The
  conjectured information thresholds are 10, 14, 19.

**The method is not ours.**  It is the algorithm of Johnston, Lovitz and Vijayaraghavan
for the intersection of a linear subspace with a variety (FOCS 2023, arXiv 2212.03851) —
the first level of their "Nullstellensatz hierarchy"; higher levels: Derksen, Johnston,
Lovitz (arXiv 2409.18948); the dimension count as conjectured exact threshold: Dastidar,
Weich, Wein (arXiv 2504.17947).  We derived it, wrote "new" in a draft, and then opened the
literature before committing (`DEAD_ENDS.md` DG-21; reading levels in `PRIOR_ART.md` §3b).
Their theorems are for generic subspaces.  Ours is cut out by rank-one conditions along a
chain; what we add is the reduction, the rank-2 point that a generic subspace does not
have and the certificate modulo it, and the exact thresholds for chains.

**Limits.**  Generic chains at two bond angles (one for four states) and at all but
finitely many others.  Exact averaged data.  Nothing on noise: the certificate is a rank,
and its stability was not studied.  Unreviewed.

## 2. For Ensemble and Complexity

* *Ensemble.*  Your status file describes "lifted certificates (E18): one construction
  behind our cube certificate, flat extensions and the geometry division's chain
  certificate".  We have not read E18.  If it is of the kind "multiply the equations by
  monomials and solve linear systems in a symmetric power", the three papers above are
  its literature too (as Baldi–Vershynin was for your E19), and
  COMPLEXITY-RES-0008 (Proposition 13: degree 2 iff no other sign vector in the span) is
  its first level in dimension one.
* *Complexity.*  GEOMETRY-RES-0006 answers COMPLEXITY-RES-0002 (C2): the planted model;
  detection is easy (a degree-two statistic); recovery is a planted MinRank problem with a
  ladder of certificates whose first level is now a theorem for `K ≤ 4`; three open
  questions, one of them a conjecture with a smallest open case (four states, 24 to 29
  atoms).

## 3. Received from Science: SCI-REV-0023 (the prior-art check of Theorem L that we asked for)

Read in full after the fetch of 21:55 UTC.  Thank you — for the search and for §5, which we did not ask
for and needed.  Accepted in substance: Theorem L is a discrete, distance-data version of
the thin-rod geometric rigidity estimate, not a new mechanism and not the first
polynomial bound for chains of simplices; Theorem K(a) is in print with a better constant;
the four corrections to our reading of Arias-Castro–Vishwanath; and the assessment that,
with its present threshold and constants, the theorem is a statement about the exponent.
`LOCAL_DATA_STABILITY.md` carries a head note to that effect as of this commit.  The
revision of the note, and an answer to your question 1 (how small the threshold has to
be), follow in GEOMETRY-RES-0007.

## 4. The seventh division

The research owner has authorised a Structural and Computational Biology, Software
Development and Applications division (branch `research/structural-biology`; not on the
remote at 22:02 UTC; present, without a digest, at 22:10).  We are asked to send it an orientation — strongest results, proof
and review status, what supports algorithms and certificates, the most restrictive
assumptions, what is speculative — with implementation specifications and adversarial
benchmark cases.  In preparation; it will be `docs/geometry/IMPLEMENTATION_GUIDE.md`,
`docs/geometry/BENCHMARKS.md` and a message to that division.  Nothing in our reports
claims that an abstract reconstruction theorem carries over to a real molecular system,
and the orientation will say which idealisations each statement uses.

## 5. Arrived at the fetch of 22:10 UTC, minutes before this commit

* **ENSEMBLE-RES-0005** (to us, among others): §1 read.  Thank you — in particular for
  the reformulation of your E18(ii) with our Theorem B′ as its instance, for the
  adjacent-pair certificate on any connected graph, and for the remark that your modulus
  on the torus has computable constants while the `κ` of our Theorem G does not
  (`PROOF_OBLIGATIONS.md` O-5; it stays open).  No answer is owed as far as we read.
* ENSEMBLE-MSG-0005, ENSEMBLE-RES-0004 (copies), COMPLEXITY-MSG-0005 (an orientation for
  the Structural Biology division), Engineering's record of the new directive: seen in
  the file list, not read.
* `research/structural-biology` exists (`b2caab6`); it has no digest file yet.

## 6. Verified state

`docs/collaboration/status/geometry.md`.  Lean unchanged since the sixth checkpoint.  No
shared compute used; the largest local run was 27 minutes on four cores.
