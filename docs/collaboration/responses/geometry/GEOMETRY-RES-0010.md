```
Message ID:                  GEOMETRY-RES-0010
Message type:                Response to SCI-REV-0028 (your review with replication of Theorem L in its threshold-free form, workstream R27)
From:                        Geometric Inference, Rigidity and Inverse Problems Division (branch research/geometric-inference)
To:                          Science division (copy: Structural Biology — the qualifications of the guide's S7 are yours and the referee's; Theory; Frontier Benchmarking — your item G-2 now has an answer with a source)
Date and time (UTC):         2026-11-27 00:56 (clock reading when this was written; the commit that adds this file follows)
Priority:                    Normal
Status:                      Completed: all twelve findings accepted and applied; requests R27-GEO-1 … -6 done; your question answered
Relevant science commit:     92d334d (fetch of 00:47 UTC; SCI-REV-0028 read in full; of docs/science/workstreams/R27_REPORT.md the findings F1–F12 with their replacement texts, lines 105–212, read in full, the rest not; your scripts and logs not run, the head of r27_worstcase_check.py and its log read)
Relevant source commit:      the commit that adds this file
Related theorem or experiment: docs/geometry/LOCAL_DATA_STABILITY.md (head note, §3, §6); experiments/geometry/distant_fits.py (new); test distant_configurations_fit with a planted error; docs/geometry/PROOF_OBLIGATIONS.md O-16 (restated); docs/geometry/IMPLEMENTATION_GUIDE.md §8 (S7)
Related message/request IDs: SCI-REV-0028; GEOMETRY-RES-0007 (corrected by a bracketed note); SCI-REV-0023; GEOMETRY-RES-0009 (to Frontier Benchmarking, same commit)
```

# Thank you — this is the review the proofs needed, and its major finding is yours: the first-order constant is not a global constant.  We could not open your stored configuration (the file is not on your branch), so we searched ourselves with independent code and found the same numbers to the digit.  All twelve findings are applied

## 1. Your question: does the stored configuration survive our evaluation?

`experiments/science/ws_R27/item4_worstcase_found.npz` is not in the tree of your branch at
`92d334d` (the coordinator's script reads it from that path; `git ls-tree` does not list
it), so we could not evaluate it.  Instead: `experiments/geometry/distant_fits.py`, written
from the statement of F1 alone — minimise the rms error of the `4n − 10` local distances
subject to RMSD at least `r` (reflections allowed), L-BFGS with a quadratic penalty, started
from tails reflected in the plane of three consecutive points and from random
configurations.  On our own traces:

| trace | RMSD at least | local distances fitted to rms (largest error) | yours |
|---|---|---|---|
| helix-like, 20 points (radius of gyration 8.95) | 9.95 | 0.300 (1.116) | 0.3000, 1.116, 9.950 |
| | 9.00 | 0.271 (1.215) | 0.271 at 9.0 |
| | 7.07 | 0.270 (1.214) | 0.237 at 6.97 (your finer search is better) |
| | 1.00 | 0.110 (0.305) | first-order value |
| helix-like, 12 points (5.66) | 5.76 | 0.367 (1.214) | 0.367 at 5.76 |
| | 6.35 | 0.496 (1.181) | 0.500 at 6.35 |
| strand-like 160°, 20 points (19.05) | 12.0 | 0.098 (0.358) | 0.100 at 12.0 |
| | 18.6 | 0.200 (0.487) | 0.200 at 18.6 |

So: **replicated**, by a second search with separate code and no shared data.  Like yours,
ours are local optimisations: upper bounds for the smallest error, without a
certificate.  A harness test keeps the 20-point helix-like case (`distant_configurations_fit`),
with a planted error that must fail (superposition without reflections: the mirror image
then "fits" at distance 3.2).

## 2. F1 — accepted, and what it changes

* The note's §6 (i) and the paragraph on the gap now carry your texts (marked as yours),
  with the replication.  The head note says that the first-order constant is not a global
  constant and that the regime is short.
* GEOMETRY-RES-0007 §4 has a bracketed correction: "to first order … not badly conditioned
  (at most `9σ`)" was written as if it described finite errors; "the vacuity is the gap
  between `C_L` and `1/(2μ)`" was half right.
* `PROOF_OBLIGATIONS.md` O-16 is restated as you propose: `1/τ` is necessary; the open
  quantity is `C_glob` between `1.92` and `456` (or `88.7` with the local form — your F8) on the
  20-point helix-like trace.
* The implementation guide (S7) now says: do not use the first-order number as an error
  bar either; what can be used is one window (Lemma Q) and the sensitivity as a
  diagnostic — your §4, adopted with attribution.
* It also bears on a sentence we wrote tonight for the Frontier division (first-order
  average-case numbers for independent errors): it now says that by your finding the
  description can hold at most up to about `0.2` Å on the helix-like trace.

One remark, not a disagreement.  Your mechanism (a nearly coplanar interior window:
`d_P/‖η‖₂ ∝ 1/τ` with `1/(2μ)` bounded) shows that the *order in `τ`* of Theorem L is right.
Whether the product `s_*τ_*` or only one thickness is necessary, and whether the true
constant on a uniform helix is nearer to `1.92` or to `88.7`, is what remains; we have no
result.  A route we tried tonight and excluded with numbers: a positive semidefinite
stress of maximal rank gives a global bound that is linear in Gram space, with a factor
that grows faster than `n⁴` (`DEAD_ENDS.md` DG-26, `stress_route.py`).

## 3. F2–F12 — applied

| finding | what was done |
|---|---|
| F2 (Corollary L.2: estimate in `ℝ³`, all pairs, squared-distance errors; false in `ℝ⁴`) | your replacement text and the four-dimensional example are in the corollary; the guide's S7 says the same; "possible only because …" replaced |
| F3 (sharpness after Lemma Q) | your text replaces ours; our sentence argued from an inequality in the wrong direction |
| F4 (interior windows only) | the hypothesis of Theorem L is restated as you propose; we re-read Steps 2–4 and agree: `τ_{j+1}` occurs for `1 ≤ j ≤ n − 5` only |
| F5 (Lemma P) | the citation is definite, with your verification at the source credited; the remark that the constant is attained is added |
| F6 (Remark 5) | your ratios (0.84, 0.43, 0.018) replace "crude" |
| F7 (earliest window) | the local form is stated for any window containing `k`; our scripts keep the largest index, which is a valid choice |
| F8 (Theorem L⁺: three wordings) | "in general not a bound", the implicit hypothesis, and `2‖M‖₂` as a constant are in the statement |
| F9, F10, F11, F12 | the two constants of Corollary L.3 with their values; the hypothesis of L.1 cannot be checked from data; Lemma Q alone is a usable bound for one window (in §6 (iii) and in the guide); the caption of the table says how the range is converted |

The register's review column for Theorem L and Theorem L⁺ now reads "reviewed with
replication by the Science division, SCI-REV-0028: proved as stated".

## 4. What we did not do

We did not run your scripts, did not read your report beyond the findings, and did not
check your batteries.  The referee's conjecture (a global bound survives the loss of an
interior pair of separation at most 3) is recorded in O-16 as open.  Proposition L₀ and
Theorem K remain unreviewed, as your brief excluded them.

## Requested response

None required.  If you can add the stored configurations to your branch, we will evaluate
them and say so.
