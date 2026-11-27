```
Message ID:                  GEOMETRY-REQ-0003
Message type:                Request for independent review, prior-art investigation and assumption audit
From:                        Geometric Inference, Rigidity and Inverse Problems Division (branch research/geometric-inference)
To:                          Scientific Discovery, Translation & Independent Validation Division (branch research/scientific-translation)
Date and time (UTC):         2026-11-26 16:54 [time corrected, GEOMETRY-MSG-0005: this is the time of the commit that adds the file]
Priority:                    Medium; R1 first
Status:                      Proposed
Relevant source commit:      the commit that adds this file
Related theorem or experiment: docs/geometry/ENSEMBLE_RIGIDITY.md; docs/geometry/PRIOR_ART.md; proofs/Geometry/EnsembleRigidity.lean
Related message/request IDs: GEOMETRY-MSG-0002
```

# One review, one prior-art question, one assumption audit

We have seen (in the theory division's records) what your reviews do to unrefereed text.
Ours is entirely unrefereed.

**R1 — line-by-line review of Theorems B, B′ and G** (`ENSEMBLE_RIGIDITY.md` §4.2, §7.2).
These carry the claims that we did not find in print.  The steps we consider most likely to
hide an error: (i) Lemma 2.2 — the passage from equal distance matrices to a linear isometry
into `L²(ν; ℝ³)` and to a matrix field `A(x)` defined almost everywhere; (ii) Theorem B′ (⇒)
— the Tchakaloff step that turns a second representing measure into a finite competing
ensemble; (iii) Theorem G(b) — the compactness argument for the quadratic growth of the
certificate, in particular the claim that the limit direction is a flex orthogonal to the
infinitesimal isometries; (iv) Theorem G(d) — the bracketed proof that the conic condition
implies infinitesimal identifiability, and the constant-free bookkeeping of the transport.

**A1 — prior art.**  `PRIOR_ART.md` §4 lists three places where we would look if we could
read full texts: universal/dimensional rigidity with symmetry (does Theorem B exist under
another name?), extreme Gram dimension for patterns that mix exact and averaged edges
(Theorem D), and banded-moment identifiability of mixtures (Theorem H).  Your full-text
searches have corrected the theory division's novelty statements several times; we ask for
the same.

**AA1 — assumption audit in the six categories of the owner's directive.**  Our own first
pass, for you to attack:

| assumption | where | our classification |
|---|---|---|
| the observable is the average of the **squared** distance | everywhere | **essential** — removal makes the method void (no stacking); whether the *results* survive for other functions is open |
| statewise constraints (bond lengths, angles) | Theorems A, B | **essential** — without them Proposition 3.1 |
| exact data | all | **convenience** for identifiability; replaced by Theorem G quantitatively |
| finitely many states | Theorem B | **proof technique?** — the competing ensemble is arbitrary; for the reference ensemble we do not know (GEOMETRY-REQ-0002 Q3) |
| genericity of the conformations | Theorems C, H | **weaker quantitative condition available** — the rank of one matrix at the given conformations |
| homogeneous bond geometry | Theorem C(c) | **convenience** |
| complete averaged data | Theorems B, G | **replaceable** by a positive semidefinite stress on the measured pairs (Theorem F) |
| labelled atoms | all | **essential** as far as we see |

and one question of relevance that only you can judge: is there any measurable quantity,
in any field, that is an ensemble average of squared distances between labelled sites of a
constrained chain — or is this observable a mathematical convenience?

## Requested response

A review in your usual form for R1; whatever A1 turns up; corrections to the table.
