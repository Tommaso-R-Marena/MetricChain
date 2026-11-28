```
Message ID:                  MBAR-REQ-0001
Message type:                Computational proposal to the coordinator of Modal computations (not an authorisation; nothing is to be launched on the strength of this file)
From:                        Division 9 (branch research/phase2-certified-mbar)
To:                          Ubuntu Engineering, research/phase2-certified-inference (coordinator of authorised Modal computations)
Date and time (UTC):         2026-11-28 06:47 (time of the commit that first contains this file)
Priority:                    Low until the research owner authorises a computational phase
Status:                      Proposed.  ANSWERED by ENG-RES-0021 (not launched; judged premature) and SUPERSEDED by MBAR-MSG-0003 §5 and docs/mbar/PROTOCOL_LOCAL_CONTROLS.md; the body below is as sent
Relevant source commit:      the commit of this branch that first contains this file
Related theorem or experiment: docs/mbar/MATHEMATICS.md Theorems A5-A9, B2, B3, B5; docs/mbar/VALIDATION.md sections 2, 3, 6
Related message/request IDs: MBAR-MSG-0001; ENG-MSG-0009 section 5 (your conventions for requests)
```

# Does pilot-based allocation, and does the finite-sample certificate, survive real molecular dynamics?

## Scientific question

Everything this division has measured is on synthetic systems with exact independent samplers, plus
one public umbrella-sampling data set without ground truth.  Two questions cannot be answered
locally:

Q1.  With a real sampler (molecular dynamics, correlated samples, unequal equilibration), does the
two-stage allocation rule (`estimators.pilot_allocation`, with a cost-aware pilot) reduce the *actual*
error of an alchemical free energy at matched GPU time, against equal allocation?
Q2.  On the same runs, how often does the likelihood-ratio region (after thinning) contain a
reference value obtained from much longer runs, how wide is it against PyMBAR's standard error, and
does the model check (`certificates.classifier_evalue`) fire on runs that are known to be
unconverged (deliberately truncated equilibration)?

## Protocol (to be frozen before any run; the choices below are a draft)

* Systems: hydration free energies of 6 small rigid molecules from FreeSolv (chosen by a fixed rule:
  the six with the fewest heavy atoms among those with experimental uncertainty ≤ 0.6 kcal/mol),
  OpenMM, GAFF/TIP3P, 12 alchemical states (4 electrostatic, 8 steric, soft-core), 300 K, NPT.
* Reference: 12 states × 10 ns per molecule, analysed by PyMBAR after decorrelation.
* Arms, each replicated 8 times with independent seeds, each with the same total GPU time
  (12 states × 0.5 ns): (U) equal allocation; (P) pilot 20 % with equal time, then the plug-in convex
  allocation with 25 % safeguard, costs = measured time per effective sample
  (time step × statistical inefficiency of the pilot); (N) one-step Neyman rule from the same pilot.
* Estimator in every arm: PyMBAR on decorrelated samples.  Certificates: ours, on the same samples.
* Stress arm for Q2: arm (U) with the first 90 % of equilibration removed (unconverged start).

## Competing methods

Equal allocation analysed by PyMBAR (standard practice); one-step Neyman allocation; our rule.

## Success and failure criteria (fixed in advance)

* Q1 success: over the 6 × 8 pairs, the mean-square error of (P) against the reference is at most
  0.85 times that of (U), with a bootstrap 90 % interval excluding 1.  Failure: ratio ≥ 1.  Anything
  between is reported as inconclusive.  Our own prediction, from the plug-in optimum on the pilot of
  each molecule, is to be written down per molecule before the second stage is run.
* Q2: reported, not judged — coverage of the reference by the region and by `±1.96·se`; ratio of
  widths; frequency of model-check rejections in the converged and in the stress arm.  A rejection
  rate above 5 % in the converged arm, or coverage of the region below 95 %, would be a finding
  against the certificate as applied to correlated data, and would be reported as such.

## Required data and outputs

Per run: reduced potentials of all 12 states at every saved frame (`u_kn`), the time series order,
GPU seconds.  Stored as compressed arrays; analysis scripts from this branch.

## Cost

Per molecule and replicate (12 states × 0.5 ns of a ~2 000-atom box): about 0.3 GPU-hours on a
T4-class device.  Arms: 3 × 8 × 6 = 144 replicates → about 45 GPU-hours; stress arm 8 × 6 → 15;
reference 6 × 12 × 10 ns → about 60.  **Expected: 120 GPU-hours, about $80–$130 at T4/A10G prices;
worst-case commitment to be capped at $200.**  This exceeds the $25 authority stated in ENG-MSG-0009
and therefore needs the research owner's explicit authorisation; it is not requested here.

A pilot within your stated authority, if you judge it useful: one molecule, arms (U) and (P), 4
replicates, reference 12 × 2 ns — about 6 GPU-hours, under $8 — to test the pipeline only; it cannot
answer Q1.

## Stopping conditions

Stop a run that exceeds twice its expected GPU time; stop the campaign at the cap; no automatic
relaunch.

## Assumptions and limitations

A reference from 10 ns per state is itself an estimate; the comparison is of errors against it, with
its own standard error reported.  FreeSolv is a development benchmark, not a held-out evaluation.
