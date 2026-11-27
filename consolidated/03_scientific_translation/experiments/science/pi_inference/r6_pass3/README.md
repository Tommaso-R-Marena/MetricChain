# Workstream R6's second-pass campaigns run again with the sampler guard lowered (coordinator, 2026-11-26)

Why: the engineering division measured the defect of numpy's binomial sampler from 1e15 trials on (ENG-RES-0013 section 1.1);
re-measured here it is present from 5e14 on (../numpy_binomial_variance_check.py).  `ws_R6/r6lib.big_binomial` switches to a
Poisson draw only above 2^50, so it has a gap.  Was any run exposed?

How: a copy of `experiments/science/ws_R6/*.py` in the session scratchpad, with `r6lib_guard.patch` applied (guard lowered to
n > 1e14, p <= 1e-8, 30 < mean < 1e6; one byte written to a per-process file for every draw that takes the branch, separately
for n <= 2^50 -- the window the old guard left to numpy -- and for n > 2^50), then `bash run_pass3.sh` (the campaigns, numbers
of runs, seeds and time limits of the workstream's `run_pass2.sh`; two streams of two processes; 13 minutes).
The workstream's own directory was not touched.  Logs of the eight campaigns: `logs/`.

| campaign (seed) | runs completed here | harness-limited | runs with a violated claim | the workstream's pass 2: runs; violations |
|---|---|---|---|---|
| A_medium_213 | 500 | 18 | 0 | 313; 0 |
| A_ties_212 | 500 | 35 | 0 | 500; 0 |
| B_invalid_215 | 400 | 10 | 0 | 400; 0 |
| B_lazy_220 | 260 | 0 | 0 | 260; 0 |
| B_lazycheap_218 | 60 | 1 | 0 | 60; 0 |
| B_reducedK_214 | 400 | 4 | 0 | 400; 0 |
| D_2L_216 | 240 | 0 | 0 | 239; 0 |
| D_2L_off_217 | 300 | 0 | 0 | 300; 0 |
| **all** | **2660** | | **0** | 2472; 0 |

**Draws that took the lowered branch (n > 1e14, 30 < mean < 1e6): 0 with n <= 2^50, 0 with n > 2^50** -- in 2660 runs,
whose largest samples reach e^57.8 points.  The corrected branch is never taken: `r6lib.Landscape.new_block` draws the classes of
a block in order of decreasing probability, so every conditional probability is at least 1/(number of classes) and a draw from
1e14 trials or more has a mean of about 1e10 or more, where numpy's sampler shows no defect.  Hence the workstream's first pass
(plain numpy) was not exposed either, and "re-run with a corrected sampler (same outcome)" (SCI-REV-0007 section 4) was true and
vacuous.  (More runs complete here than in the workstream's pass because the machine was less loaded; the time limits are the same.)
