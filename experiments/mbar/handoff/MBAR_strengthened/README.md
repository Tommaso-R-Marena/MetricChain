# MBAR strengthened handoff — v2

This package is an independent mathematical strengthening of the recovered Gemini MBAR programme. The nested original_handoff.zip is unchanged. Read proofs/MAIN_RESULTS.md first. Do not submit the original manuscript; it contains obsolete claims. The new note replaces central theorems with explicit assumptions, derivations, and limitations; it is not a polished journal article or formal verification certificate.

## Most important results
- A1/A2: true i.i.d. MBAR asymptotic variance is convex in positive sample weights, with exact gradient as negative within-state variance. Perspective representation, cost-aware KKT, group-norm formulation E2. This generalizes a known two-state convexity result; multistate novelty still to be checked.
- B3/B4: corrected finite-sample constants and explicit contrast remainder, leading exact stratified variance. B5: corrected Berry–Esseen with observable support-based fallback.
- C1: entirely observable no-split cut-score confidence certificate. C2: independent-pilot bridge KL intervals + graph closure. C3: simple anytime-valid extension.
- D1/D2: arbitrary graph, arbitrary sample-ratio low-overlap minimax hard family, including rigorous randomized finite support coordinate-observation extension.
- E1: data-based optimizer existence criterion; E3: deterministic energy/statistical error composition interface.
- G1: explicit conservative stationary Markov-chain result and observable cut certificate with known spectral contraction; G2: full bounded observable/PMF confidence intervals.

## Reproduction
Run `OPENBLAS_NUM_THREADS=1 python software/test_and_benchmark.py` with Python 3, NumPy 2.3.5 and SciPy 1.17.0. Output is in results/; `software/test_minimax_only.py` is an independent construction check. The original recovered code is preserved inside original_handoff.zip; use the new fail-closed reference implementation instead. All benchmarks use synthetic finite-support populations; no real biomolecular dataset, no certified floating-point arithmetic, no kernel-checked Lean proof. The independent pilot in the toy coverage test is a noisy reference based on known ground truth, chosen independently of the validation sample, not a practical trained pilot. Confidence tests include abstentions; widths are reported and are often conservative. Earlier failed runs are retained. The original Lean files remain uncompiled; no Lean/Lake installed here.

## Fable priorities
See FABLE_TASK.md. Verify every derivation independently and compare with prior literature. Extend to real sampling and proof assistants; do not merge conclusions into MetricChain until independently established. The most novel candidates are A1/A2/E2, C1/C2 and D1/D2. G1/G2 are newly derived extensions, not yet tested. No claimed priority or journal readiness.
