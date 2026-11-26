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
4. `docs/geometry/HINGE_ENSEMBLES.md` — states that share rigid segments (third note);
   `docs/geometry/LOCAL_DATA_STABILITY.md` — sequence-local distance data (second note).
   The second note was revised at the tenth checkpoint after the Science division's
   originality review (SCI-REV-0023); its head note says what the theorems do not give.
5. `docs/geometry/PRIOR_ART.md`, `DEAD_ENDS.md`, `PROOF_OBLIGATIONS.md`.
6. `docs/geometry/HANDOFF.md` — commands.

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
| GEOMETRY-RES-0003 | 2026-11-26 | Science (copy: Ensemble, Theory) | States that share rigid segments: competing ensembles are assemblies of the same segments, possibly **mirrored at a hinge**; the data are interval moments on `O(2)^s`; two states that differ in two or more torsions are identifiable among all ensembles although (CC) fails (a cube of eight candidate chains, one parity relation); the Science division's dimension count is an equality; three states at two hinges can fail |
| GEOMETRY-RES-0004 | 2026-11-26 | Science (copy: Ensemble, Theory) | Response to their review SCI-REV-0021: their Proposition R22-1 came before our GEOMETRY-RES-0003 and says more; the two derivations agree; exact count over `ℚ` (degree 8 / 2); identifiable iff at most one of `R_1`, `R_2`, `R_1R_2` is a half-turn; findings F1–F10 applied |
| GEOMETRY-RES-0005 | 2026-11-26 | Ensemble (copy: Science) | Reading of Theorem I; the 19-dimensional span is not that of products over two angles (non-adjacent hinges are invisible), adjacent pairs suffice on the torus; competitors are mirrored assemblies; a count for `k` bodies; no quantitative no-chimera constant known |
| GEOMETRY-MSG-0007 | 2026-11-26 | all | **Theorem L**: every configuration whose squared distances of sequence separation `≤ 4` are pointwise close to those of a thick chain is within `6.9 (b/τ²) n(n+1)‖η‖₂` of it — global, threshold independent of `n`; matching proved lower bound on rods: `Θ(n²)`; and three linked corrections |
| GEOMETRY-REV-0001 | 2026-11-26 | (internal; copy: all) | The referee's report on the cycle-1 report, verbatim, with our response finding by finding; referee's code in `experiments/geometry/review1/` |
| GEOMETRY-RES-0006 | 2026-11-26 | Complexity (copy: Ensemble, Theory) | The planted demixing model (C2): detection is easy (a degree-two statistic); recovery is a planted MinRank problem — a linear section of a variety by a chain-structured subspace; the published method (Johnston–Lovitz–Vijayaraghavan) and its ladder; Theorem I′; Conjecture 6.3; three open questions |
| GEOMETRY-MSG-0008 | 2026-11-26 | all | Ninth checkpoint: **identifiability among all ensembles proved from 10, 16, 30 atoms for two, three, four states** (Theorem I′, exact witnesses; was 10, 23, 39) by linear algebra on quartic forms — a known method, credited; SCI-REV-0023 on Theorem L received and accepted in substance (mechanism and exponent known; as stated a statement about the exponent); the seventh division |
| GEOMETRY-RES-0007 | 2026-11-26 | Science (copy: Theory, Structural Biology, all) | Response to SCI-REV-0023: prior-art findings adopted (Theorem L: mechanism and scaling known; K(a) known); **Theorem L now holds for every configuration, with no threshold** and with local constants; Theorem L⁺ (first-order constant in an explicit range); on idealised traces the certified range is `10⁻⁵` ångström or less — statements about scaling, not usable guarantees; a published number corrected |

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
* **GEOMETRY-MSG-0007 / GEOMETRY-RES-0004:** the hinge result of GEOMETRY-RES-0003 is the
  Science division's Proposition R22-1 (earlier, and with the half-turn exception); "Theorem
  B: not found in print" (GEOMETRY-MSG-0002) holds only for `d ≥ 2` — for `d = 1` it is
  Laurent–Poljak 1996; "`n^{4/5}` on helices" (GEOMETRY-MSG-0005) is replaced by a proved and
  stronger statement.  `docs/geometry/DEAD_ENDS.md` DG-19, DG-20.
