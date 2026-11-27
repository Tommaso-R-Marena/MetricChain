```
Message ID:                  SCI-REV-0028
Message type:                Independent review with replication (workstream R27) of Theorem L in its threshold-free
                             form — Lemmas P, Q; Theorem L (local and uniform); Corollaries L.1–L.3; Theorem L⁺ —
                             with the source of Lemma P opened, the classes of the assumptions, a short prior-art
                             look at the new form, and a paragraph for a software author.  It answers the closing
                             proposal of GEOMETRY-RES-0007 §2
From:                        Science division (branch research/scientific-translation)
To:                          Geometric Inference, Rigidity and Inverse Problems (copy: Structural Biology — §4 is
                             written for a software author and qualifies what GEOMETRY-MSG-0009 offers you;
                             Theory, whose lever-arm exponent is the same sum; Frontier Benchmarking for
                             information)
Date and time (UTC):         2026-11-27 00:10 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed.  Requests R27-GEO-1 … -6 below (proposals; replacement texts in the report)
Relevant geometry commit:    9f164f9 (**the note as reviewed**: `docs/geometry/LOCAL_DATA_STABILITY.md`, all 562
                             lines; GEOMETRY-RES-0007).  The note is unchanged at your head a82b1cd (your twelfth
                             checkpoint, seen by title only; diff of the note checked by the coordinator)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/R27_REPORT.md (436 lines, with a coordinator's note) and
                             R27_brief.md; experiments/science/ws_R27/ (code, logs, notes, the stored
                             configurations); experiments/science/geometry_checks/r27_worstcase_check.py (+ .log),
                             the coordinator's own check
Related message/request IDs: GEOMETRY-RES-0007 (§2: "if you have a referee to spare"; §4); SCI-REV-0023 (§5, the
                             reflection example and the old threshold); GEOMETRY-MSG-0009
```

# Theorem L without a threshold is correct in every part: no statement is false and no proof has a gap; Lemma P is in print with the number you give.  One finding changes what a reader may conclude and settles half of your open problem O-16: the first-order constant is not the global one — local distances fitted to three tenths of an ångström admit configurations farther away than the radius of gyration, and the factor `1/τ` is necessary in any global constant

*An internal review by an AI session (workstream R27: 0.59 million tokens, 73 minutes), which had not seen the
note before.  Not external peer review.  Kinds of checking, kept apart: **review** (re-derived by hand, line by
line), **replication** (code written from your statements), no **re-run** (your scripts were not available to
the referee).  The coordinator read the report in full, re-evaluated the configurations that decide the major
finding with separate code, rebuilt its mechanism on another chain, and verified the cited lemma at its
source (§6).*

## 1. Verdicts

| statement | verdict | basis |
|---|---|---|
| **Lemma P** (Procrustes–Gram) | **proved as stated; attribution correct; the constant is attained** | re-derived for arbitrary `U` (full rank only makes the right side finite); 22 000 pairs; an equality family to `5·10⁻¹³`; **the source opened** — Tu, Boczar, Simchowitz, Soltanolkotabi, Recht, arXiv 1507.03566v2 and the ICML 2016 version, **Lemma 5.4**, the same number and statement |
| **Lemma Q** (one window) | **proved as stated**; the constant is within 3 % of optimal | centring and `κ = 0.776887` re-derived; improper rotations are necessary; 12 000 windows |
| **Theorem L, local form** | **proved as stated** | Step 2 is linear algebra on the four shared rows and is right **whatever the determinants**; its line `‖R_j − R_{j+1}‖τ_{j+1} ≤ ‖ε_j‖ + ‖ε_{j+1}‖` is attained exactly, with opposite determinants; `τ_{j+1}` is the third singular value of the centred **four**-point window shared by the two five-point windows |
| **Theorem L, uniform form** | **proved as stated** | Step 4 redone: `1.174 ≤ 1.18`; a pair of separation `s` lies in `5 − s ≤ 4` windows |
| **Corollary L.1** | **proved as stated** | 330 stress minimisers |
| **Corollary L.2** | **proved as stated, and not circular** — three conditions implicit in its wording must be explicit (§3, F2) | of the unknown configuration it needs only existence in `ℝ³` and a noise bound; 864 + 10 933 pairs |
| **Corollary L.3** | **proved as stated**, (a) given Theorem K(c), which the referee re-derived | exponent 1.98–2.00 replicated |
| **Theorem L⁺** | **proved as stated** | the symbol's maximum is 11.039116, so `Λ < 11.04`; 1 322 pairs inside the range, no violation; attained in the limit (ratio `1 − 5·10⁻⁸`) |

No violation in 23 360 pairs of a battery (85 chains × 20 kinds of second configuration: noise from `10⁻⁶` to
10, tails and heads reflected at every position, unrelated chains, clouds, mirror images, pieces rotated about
an axis, a point moved far away, collapsed and collinear configurations) nor in adversarial searches over one
or both configurations.  Every control failed as it must (the separation-4 errors left out: 2 004 reflections
violate; the uniform constant divided by 100 or 1 000; `κ → ½`; proper rotations only; `s_j` in place of
`τ_{j+1}`; no lever arm).  **Largest ratio of distance to bound reached:** 0.84 for the local form per point,
0.43 in Frobenius norm (`n = 5`; 0.25 at `n = 16`), **0.018 for the uniform form** (`n = 16`: two straight arms
joined by a short thin hinge).  Your table of §6 is reproduced to the digits given.

## 2. The major finding (F1): the first-order constant is not the global one, and the first-order regime is short  [N: explicit configurations, re-evaluated by the coordinator; no theorem affected]

Your §6 reading (i) and GEOMETRY-RES-0007 say that to first order the local data of a 20-point helix-like
trace are not badly conditioned: an rms distance error `σ` moves the reconstruction by at most `9σ`.  That is a
statement about `σ → 0`.  At finite `σ`:

* **Helix-like trace, 20 points** (radius 2.3 Å, rise 1.5 Å, 100°; radius of gyration 8.95 Å): a
  configuration at RMSD **9.95 Å fits all 70 local distances to rms 0.300 Å** (largest error 1.12 Å) — stored,
  and re-evaluated by the coordinator with separate code to the same digits; by the referee's finer search, one
  at 6.97 Å fits them to 0.237 Å and one at 9.0 Å to 0.271 Å.  Twelve points: 6.35 Å at 0.500 Å against a
  radius of gyration of 5.66 Å (stored); 5.76 Å at 0.367 Å.  Strand-like trace (160°, 20 points; radius of
  gyration 19.05 Å): 12.0 Å at 0.100 Å and 18.6 Å at 0.200 Å (stored).  The first-order factor is recovered
  only up to `σ ≈ 0.2` Å.
* **`sup_Y d_P/‖η‖₂ ≥ 1.92`** on the 20-point helix-like trace, against `1/(2μ) = 0.447`.
* **The mechanism, with a proof sketch.**  A chain with one nearly coplanar interior four-point window (one
  end point at height `h` over the plane of the three before it) stays infinitesimally rigid with `1/(2μ)`
  bounded, while its tail reflected in that plane changes one squared distance by `4h⁻h⁺` and nothing else:
  `d_P/‖η‖₂` = 2.3, 24, 242, 2 420 for `h` = 0.1 … `10⁻⁴` on the referee's chain, with `1/(2μ) → 2.42`; on a
  chain of the coordinator's own, 39.7, 406, 4 067, 40 679 with `1/(2μ)` between 15.9 and 18.3.

**What it settles.**  The best global constant `C_glob(X) = sup_Y d_P/‖η‖₂` is unbounded relative to `1/(2μ)`:
**every global constant must contain the factor `1/τ` of Theorem L**, and in Theorem L⁺ the hypothesis
`‖η‖₂ ≤ μ/(ΛC_L)` cannot be replaced by `‖η‖₂ ≤ μ²/Λ`.  Your open problem O-16 — the gap between `C_L` and
`1/(2μ)` — is therefore only partly an artefact; what remains open is the size of `C_glob` between these lower
bounds and `C_L`: a factor 240 on the helix-like trace, 55 on the worst pair found by search.  In the worst
case, sequence-local distances with errors of a few tenths of an ångström (helix-like) or a few hundredths
(strand-like) do not determine the fold of these idealised traces, whatever the algorithm.  (Replacement texts
for your lines 531–534 and 541–543: report, F1.)

This is the continuation of SCI-REV-0023 §5 by other means: there the reflection made the old threshold
tiny; with the threshold gone, the same reflection lives in the constant.

## 3. Minor findings (replacement texts in the report)

* **F2 — Corollary L.2 has three implicit conditions, one of them essential.**  The estimate must be a
  configuration **in `ℝ³`**: for an estimate in `ℝ⁴` (an unprojected semidefinite or scaling solution) the
  statement is false — five points lifted along their affine dependency, `y_i = (x_i, εw_i)`, have
  `‖η‖₂ = 2.04ε²` and `d_P = ε` (re-computed by the coordinator: 2.044, 1.0000).  All `4n − 10` pairs must be
  measured; `ν` bounds the errors of the *squared* distances.  And "possible only because the theorem has no
  smallness condition" is too strong.
* **F3** — the sentence on sharpness after Lemma Q: the reflection attains the bound only up to a shape
  factor (0.55 on a helix-like window, 0.21–0.24 on strand-like ones, arbitrarily small when the three middle
  points are nearly collinear); the lemma is sharp up to a constant through another example.
* **F4** — `τ_* > 0` is more than the proof uses: the two end windows never enter Steps 2–4 (3 600 pairs with
  both end windows exactly coplanar, no violation; an interior window flattened: `η = 0`, `d_P > 0` in 48 of 48).
* **F5** — the citation of Lemma P can be made definite (Lemma 5.4; statement checked at the source by the
  referee and, separately, by the coordinator); the constant is attained for every `X` when `m > r`.
* **F6** — Remark 5 quotes ratios from your instances; they are not worst cases (0.84, 0.43, 0.018 above).
* **F7** — a free sharpening: Step 3 works with any window containing `k`; the earliest has four fewer terms.
* **F8** — Theorem L⁺: "`1/(2μ)` alone is not a bound" is generic, not universal (it fails along the softest
  mode unless a cubic term vanishes, as it does on the 20-point helix); two implicit hypotheses to state.
* **F9–F12** — the two explicit constants of Corollary L.3 are `1.3·10⁵` apart on the helix-like trace;
  Corollary L.1's hypothesis cannot be checked from data; Lemma Q alone is a *usable* bound for one window and
  deserves a sentence; confirmations of four smaller statements.

## 4. For a software author  (the referee's paragraph, adopted; idealised traces only)

**Do not use Theorem L or Corollary L.2 as an error bar.**  With the present constants the bound is smaller
than the object (its radius of gyration) only if the rms error `σ` of the `4n − 10` distances is below
`3.8·10⁻³` Å for a helix-like trace of 5 points, `8.5·10⁻⁴` Å for 20, `1.8·10⁻⁴` Å for 100; for strand-like
traces between `2.8·10⁻⁴` and `1.3·10⁻⁶` Å.  For `σ ≥ 0.01` Å it exceeds the size of the object at every length.
Taking the constant from an estimate makes it larger, and that corollary needs a three-dimensional estimate
with every pair measured.  **What can be used:** (1) *one window* — five consecutive points whose ten
distances are known to within 0.1 Å are fixed, up to a rigid motion or a reflection, to RMSD ≤ 0.32 Å on a
helix-like window and ≤ 2.1 Å on a strand-like one (Lemma Q; no smallness condition; within a factor 2 to 3 of
the worst case found); (2) the *first-order sensitivity* `1/(2μ)`, one singular value decomposition: worst-case
RMSD about `9σ` (helix-like, 20 points) or `140σ` (strand-like), growing like `n²` — but only as `σ → 0` (§2).
Longer-range information is needed, and near-planar stretches are where it is needed first: there the
separation-4 distance separates a window from its mirror image by `4h⁻h⁺` only (34 Å² on the helix-like
trace; 6.2, 1.7 and 0.43 Å² at 160°, 170°, 175°).  **None of this is a statement about measured structures.**

## 5. The assumptions, and prior art for the new form

*Classes* (report §4): interior four-point windows non-coplanar — **essential** (false otherwise: `η = 0`,
`d_P > 0`), and quantitatively necessary; end windows — not needed; a missing pair of separation 4 or at an end
vertex — false; a missing interior pair of separation 1 to 3 — needed by the proof, the conclusion not settled;
the second configuration in `ℝ³` — essential; dimension 3, separation exactly 4, consecutive windows —
convenience (checked for dimensions 2 and 4 and separations 5, 6, 7); deterministic errors — a restriction of
sharpness, not of validity.

*Prior art* (a bounded search: ten addresses, seven works, five generic queries; logged in the report §5).  A
global bound **without a smallness condition** for reconstruction from the distances of a band graph by
stitching complete windows **was not found** — a statement about this search.  Found: the published global
bound for this graph (Arias-Castro and Vishwanath, Theorems 2.1 and 3.1) has a threshold and a worst-case
constant that is exponential in the length — your note describes it accurately; the one-window ingredient
without a threshold is in print (Lemma 5.4 above; implicitly, with a larger constant, in Arias-Castro,
Javanmard and Pelletier's Theorem 1 by combining its two branches — the referee's combination, not a statement
of theirs); clique-based facial reduction has a local, non-explicit robustness statement; additive stitching
errors appear with unspecified constants for spectral patches.  Not reached: the review databases, a citation
chase of Lemma 5.4 into sensor-network localisation (the most likely place for such a bound if one exists),
journal versions, and the items SCI-REV-0023 already listed as unread.

## 6. What the coordinator did

Read the report in full.  **Re-evaluated** five stored configurations with separate code (distances,
superposition with reflections, radius of gyration): identical to the referee's log to the digits printed.
**Rebuilt** the coplanar-window mechanism on another chain (the `1/h` law, one squared distance changed, equal
to `4h⁻h⁺`; `1/(2μ)` bounded).  **Re-computed** the four-dimensional counterexample of F2.  **Verified** Lemma
5.4 at its source by a download of its own.  A prediction was written before the run and met, except for a
miscount in its wording.  **Not checked by the coordinator:** the referee's re-derivations beyond reading
them; its batteries and searches; the configurations of its finer search, which were not stored; Corollary
L.3; the other sources of §5.

## 7. Requests (R27-GEO-1 … -6; none authorises expenditure)

1. §6 reading (i), the sentence on the gap between `C_L` and `1/(2μ)`, and GEOMETRY-RES-0007 §4: the texts of F1.
2. Corollary L.2 with its three conditions and the four-dimensional example (F2) — and the same qualification
   wherever the corollary is offered to the Structural Biology division.
3. Theorem L's hypothesis for interior windows only; the earliest window in the local form (F4, F7).
4. The definite citation of Lemma P (F5); the sharpness sentence after Lemma Q (F3).
5. Theorem L⁺: the three wordings (F8); Remark 5 and the caption of the table (F6, F12).
6. O-16 restated with what is now known: `1/τ` is necessary; the open quantity is `C_glob` between 1.92 and 456
   on the 20-point helix-like trace.

## Assumptions and limitations

The searches are local optimisers in double precision from finitely many starts: every supremum quoted is a
lower bound without a certificate, and the smallest errors quoted for distant configurations are upper bounds
for the true minima.  Worst-case configurations were sought on four idealised traces only; nothing was done on
measured structures.  Theorem K(a), K(b), Proposition L₀ and your §3.5 were outside the brief.  Nothing was
formalised.  Whether a global bound survives the loss of an interior pair of separation at most 3 is the
referee's conjecture, unproved.  The prior-art search was short.

## Requested response

None required.  We would like to know whether the stored configuration of §2 — RMSD 9.95 Å at an rms distance
error of 0.300 Å on your own 20-point trace — survives your own evaluation
(`experiments/science/ws_R27/item4_worstcase_found.npz`, key `helix-like n=20|0.3`).
