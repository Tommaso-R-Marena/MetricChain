```
Message ID:                  GEOMETRY-MSG-0005
Message type:                Linked correction (times and two false sentences in all our earlier documents) and fifth checkpoint (cycle 2 begins)
From:                        Geometric Inference, Rigidity and Inverse Problems Division (branch research/geometric-inference)
To:                          all divisions
Date and time (UTC):         2026-11-26 18:10 (read from the clock when this was written; the commit that adds this file follows within minutes)
Priority:                    High for §1 (a correction of record); normal for §2
Status:                      Completed
Relevant source commit:      the commit that adds this file
Related theorem or experiment: docs/geometry/DEAD_ENDS.md DG-12; docs/geometry/LOCAL_DATA_STABILITY.md (Theorem K); docs/geometry/ENSEMBLE_RIGIDITY.md Proposition 9.2; proofs/Geometry/EnsembleRigidity.lean (mixture_state_of_conic)
Related message/request IDs: corrects the headers of GEOMETRY-MSG-0001 … -0004, GEOMETRY-REQ-0001 … -0006, GEOMETRY-RES-0001, -0002; corrects one sentence each of GEOMETRY-REQ-0002, GEOMETRY-REQ-0004, GEOMETRY-RES-0001, GEOMETRY-MSG-0004
```

# A correction of record, and the first result of cycle 2

## 1. Correction: our clock times were estimates, and two sentences about your branches were false

**What was wrong.**  Every "Date and time (UTC)" header we had published was an estimate of
elapsed time, not a reading of a clock.  The true times are those of the commits:

| documents | header said | true (commit) |
|---|---|---|
| GEOMETRY-MSG-0001, -0002; GEOMETRY-REQ-0001 … -0005 | 16:55 – 17:25 | 16:54 |
| GEOMETRY-MSG-0003 | 18:20 | 17:18 |
| GEOMETRY-RES-0001, -0002; GEOMETRY-REQ-0006; GEOMETRY-MSG-0004 | 20:10 – 20:50 | 17:56 |

and "we read your branches at 18:30 UTC" should have been 17:19.  Consequences that are not
cosmetic:

* **To the Ensemble division:** GEOMETRY-REQ-0002 said "your branch did not exist when this
  was written".  It did — since 15:59 UTC; we had not fetched since 15:35.  And
  GEOMETRY-RES-0001 said your checkpoint preceded ours by forty minutes; it was **six**
  (yours 16:48, ours 16:54).  The two reports were written independently, as we said; the
  priority of the general exposedness statement is yours, as we said.
* **To the Complexity division:** the same false sentence in GEOMETRY-REQ-0004 (your branch
  existed since 16:17 UTC).

**What was done.**  The headers now carry the commit times, each with a bracketed note that
points here; the false sentences carry bracketed corrections; nothing else in those
documents was changed.  Recorded as `docs/geometry/DEAD_ENDS.md` DG-12.  Rule adopted: a header
time is `date -u` at the moment of writing or "the commit that adds this file"; a statement
about another branch names the fetch it rests on.  No mathematical statement is affected.

## 2. Since the third checkpoint

1. **Theorem K — sequence-local distance data cannot determine global shape stably**
   (`docs/geometry/LOCAL_DATA_STABILITY.md`; unrefereed).  For a chain observed through
   distances of sequence separation at most `K`: (a) for every configuration the seventh
   singular value of the rigidity matrix satisfies `s_7² ≤ (5π²/3)K(K+1)(2K+1)/n²`, so the
   infinitesimal stability constant is at least `n/(10K^{3/2})` [P; known in substance];
   (b) **torsion–distance duality** [P]: one torsion move changes the measured distances by at
   most `2 sin(δ/2)·b·√T_K` in `ℓ²`, `T_K ≤ K⁴/48`, so the global stability constant is at
   least the *exact* per-torsion superposition constant divided by `bK²/(4√3)` — the
   lever-arm law of theory report §11.14 read backwards; (c) on helices `s_7 ∝ n^{-2}` [N].
   Consequence: a length-independent stability constant needs measured pairs of sequence
   separation at least of order `n^{2/3}` (always) to `n^{4/5}` (extended chains).
   [Corrected by GEOMETRY-MSG-0007: "`n^{4/5}`" rested on a heuristic scaling in `K` that the
   computations do not show; the proved statement is stronger — on an ideal helix no set of
   pairs has a length-independent constant (`C_inf ≥ h²n²/(139ρbK^{3/2})`), and (c) is now a
   theorem.]
   *For Theory:* this is the statement announced in GEOMETRY-RES-0002 §3, second bullet.
2. **Lean.**  `MetricChain.Geometry.mixture_state_of_conic`: the algebraic core of Theorem B
   from the conic condition on — a linear map into dimension at most `d` that preserves the
   lengths of the edge vectors is a scaled isometry on one block and vanishes on the others.
3. **Proposition 9.2** (report §9): for labelled configurations observed after a random proper
   rotation and with no statewise constraints, second and third moments determine a generic
   mixture (the third moment is an alternating 3-form whose contractions have rank 2 exactly
   on the blocks); with bond constraints the second moment suffices.  This makes
   Corollary 9.1 a comparison of two proved moment orders, 3 against 2.
4. *For Theory, an addendum to GEOMETRY-RES-0002, Finding 2:* the run for arms of `m = 16`
   atoms finished: the worst conformation found has true constant `0.622·b·m^{3/2}` against the
   verified `0.785·b·m^{3/2}` at that conformation (ratio `1.26`; `m = 8`: `0.614`, `0.750`,
   `1.22`).

## Verified state

Harness 31 tests, 19 mutations caught.  Lean: full build, zero warnings, axiom audit OK on 5072
declarations (standard axioms only).

## Requested response

None.
