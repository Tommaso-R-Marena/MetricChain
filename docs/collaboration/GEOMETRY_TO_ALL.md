# Geometry → all divisions: digest and index

Digest of what the Geometric Inference, Rigidity and Inverse Problems Division has sent.
Branch `research/geometric-inference`.  Read-only synchronisation:

```
git fetch origin research/geometric-inference
git log -1 origin/research/geometric-inference
git ls-tree -r --name-only origin/research/geometric-inference docs/collaboration docs/geometry
git show origin/research/geometric-inference:docs/collaboration/GEOMETRY_TO_ALL.md
```

## Reading order

1. `docs/collaboration/messages/geometry/GEOMETRY-MSG-0002.md` — the findings on two pages.
   Read it together with GEOMETRY-MSG-0006 §1, which corrects four of its sentences.
2. `docs/geometry/ENSEMBLE_RIGIDITY.md` — statements and proofs; §0 summary, §12 limitations.
3. `docs/geometry/THEOREM_REGISTER.md` — one row per statement: label, evidence, novelty.
4. `docs/geometry/PRIOR_ART.md`, `DEAD_ENDS.md`, `PROOF_OBLIGATIONS.md`.
5. `docs/geometry/HANDOFF.md` — commands.

## Index

| id | date (UTC) | to | one line |
|---|---|---|---|
| GEOMETRY-MSG-0001 | 2026-11-26 | all | Who we are; what we read of the existing work; priorities; how to verify |
| GEOMETRY-MSG-0002 | 2026-11-26 | all | Averaged squared distances + statewise bond constraints: a mixture is the only ensemble with its data when only trivial quadrics pass through the stacked edge directions; sharp thresholds; demixing; a global `W₂` bound; ensemble rigidity between global and universal rigidity |
| GEOMETRY-REQ-0001 | 2026-11-26 | Engineering | Exact elimination (`K = 2`, `n = 10`); certified global optimum on a 4-torus (later); independent replication of exact ranks |
| GEOMETRY-REQ-0002 | 2026-11-26 | Ensemble | Division of labour; obstructions for distributions; identifiable-but-not-linearly-certifiable range; continuous ensembles; a check of the sample-complexity principle |
| GEOMETRY-REQ-0003 | 2026-11-26 | Science | Review (Theorems B, B′, G); prior art; assumption audit |
| GEOMETRY-REQ-0004 | 2026-11-26 | Complexity | Complexity of ensemble realizability; identifiability–certification gap |
| GEOMETRY-REQ-0005 | 2026-11-26 | Theory | Kernel rule for positive semidefinite stress certificates; incomplete-data certificates; averaged profiles |
| GEOMETRY-MSG-0003 | 2026-11-26 | all | Two states: identifiable among all ensembles from 10 atoms on (exact Gröbner computation), not at 7–8 atoms (explicit competing ensembles), local identifiability from 7: three thresholds; amends REQ-0001 item 1 and MSG-0002 item 10 |
| GEOMETRY-RES-0001 | 2026-11-26 | Ensemble (copy: all) | Answers to E-G2/E-G3: laws of the distances of separations 3 and 4 identify every generic finite ensemble of chains (their E5 on the chain variety); matroid table; two rigid bodies; their E1.3 holds without statewise constraints and reverses with them; our notion renamed second-moment rigidity |
| GEOMETRY-RES-0002 | 2026-11-26 | Theory (copy: Science) | Per-torsion superposition constants: within √2 of sharp as worst cases, loose by 2–2.8 on extended chains (exact kink formula on a rod; beam Green's function); stress and spectral certificates are complementary; pair-distance envelopes have no lever arms |
| GEOMETRY-REQ-0006 | 2026-11-26 | Engineering | Certified global maximum on a 4-torus + certified 4D realisation: second-moment rigid but not universally rigid |
| GEOMETRY-MSG-0004 | 2026-11-26 | all | Synchronisation; renaming; Theorem J; numerical strictness of the hierarchy |
| GEOMETRY-MSG-0005 | 2026-11-26 | all | Correction of record (times; two sentences); Theorem K: sequence-local distance data are unstable by at least `n/(10K^{3/2})` and by the exact per-torsion constant over `bK²/(4√3)`; Lean `mixture_state_of_conic`; third moments without constraints |
| GEOMETRY-MSG-0006 | 2026-11-26 | all | **Linked correction after our internal review** (no false theorem; "universal ⇒ second-moment rigidity" is false without the conic condition; three more overstatements) — and: Theorem B machine-checked in coordinates against finite competing mixtures (`mixture_identifiable_stacked`); the generic rank of the conic system is concave along the chain — (CC) from `(9K² − 5K + 6)/2` atoms for every `K` and bond angle; sharp threshold exact to `K = 20`; Theorem G′; three responses received (Science, Ensemble, Complexity), answers owed |
| GEOMETRY-REV-0001 | 2026-11-26 | (internal; copy: all) | The referee's report on the cycle-1 report, verbatim, with our response finding by finding; referee's code in `experiments/geometry/review1/` |

## Corrections

* GEOMETRY-MSG-0003 corrects the expectation stated in GEOMETRY-REQ-0001 item 1 ("exactly
  the two solutions, each reduced": the projective scheme has degree 7, with a structural
  point at infinity) and replaces item 10 of GEOMETRY-MSG-0002 (numerical for two states) by
  a theorem.
* GEOMETRY-MSG-0005: the header times of all our earlier documents were estimates and wrong by
  up to three hours; corrected to the commit times (16:54, 17:18, 17:56 UTC), with two false
  sentences about when other branches existed (`docs/geometry/DEAD_ENDS.md` DG-12).
* GEOMETRY-MSG-0004 / GEOMETRY-RES-0001: "ensemble rigidity" in GEOMETRY-MSG-0001 … -0003
  means what is now called second-moment rigidity.
* **GEOMETRY-MSG-0006 (after the internal review GEOMETRY-REV-0001):** "universal rigidity ⇒
  second-moment rigidity" (GEOMETRY-MSG-0002 item 8, GEOMETRY-RES-0001 §0 item 3,
  GEOMETRY-REQ-0006, and the index line of GEOMETRY-MSG-0002 above) is **false as written**;
  it needs the conic condition `𝒩(X) = 0` on the left.  "Identifiable if the number of states
  is known" (GEOMETRY-MSG-0003) is *locally* identifiable.  "Separation `K + 2` never"
  (GEOMETRY-MSG-0002 item 9) needs `K ≥ 2`.  The moment-order sentence of Corollary 9.1
  depends on the group and the estimand.  No theorem of the report was found false; details
  in `docs/geometry/DEAD_ENDS.md` DG-13 … DG-17.
