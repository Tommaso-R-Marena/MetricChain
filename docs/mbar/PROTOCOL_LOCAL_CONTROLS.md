# Division 9 — frozen protocol for the next experiment: allocation and certificates with correlated samplers and exact answers

*Written on 2026-11-28 before any such run, after the coordinator's decision ENG-RES-0021 (route (a)).
**Not run.**  It needs no Modal budget and no external computation; it needs the research owner's
renewed authorisation of this division.  Nothing below may be changed after the first run without a
dated note in this file; anything added afterwards is reported as post hoc.*

## Question

Do the pilot-based allocation rule and the likelihood-ratio region keep their properties when every
state is sampled by a Markov chain whose autocorrelation time differs between states, the pilot has to
estimate those times, and the cost is counted in chain steps?

## Systems (exact free energies by enumeration)

The harmonic systems "bottleneck" (six states), "widths" and "homogeneous" (five states) of
`bench_allocation.py`, discretised on a grid of 200 points covering six standard deviations beyond the
outermost centres, each with two kinds of reversible chains with exactly computed spectra:
* **L** — lazy independence chains `ρ_k I + (1−ρ_k)Π_k`, for which the statistical inefficiency
  `C_k = (1+ρ_k)/(1−ρ_k)` is the same for every function (the case covered exactly by A12(b)–(c));
* **M** — Metropolis chains with nearest-neighbour proposals, for which it depends on the function
  (the case in which A12(b) is only an approximation).
Inefficiency profiles across the `K` states: *aligned* `C_k = 50^{k/(K−1)}`, `k = 0, …, K−1` (from 1 to 50
along the ladder), *reversed*, and *flat* `C_k = 10`;
for **M** the step size of each state is tuned once, before any run, to give these values for the
own-state energy.  Total budget: `6·10⁴` steps per replicate; 1000 replicates; seeds `7000 + r`.

## Arms (same final estimator: MBAR on each state's samples thinned by its estimated inefficiency)

1. EQUAL: equal steps per state.  2. EQUAL-IID: equal steps, no thinning (what ignoring correlation does).
3. PILOT-g (ours): 20 % pilot with equal steps; inefficiencies `ĝ_k` estimated from the pilot (initial
positive sequence estimator on the own-state reduced potential); MBAR on the thinned pilot; plug-in
design with costs `a_k ĝ_k` (A12(b)); 25 % safeguard mixed with equal steps.  4. PILOT-blind: the same
with `ĝ ≡ 1` in the design.  5. NEYMAN1-g: one-step Neyman rule with `ĝ`.  6. ORACLE: the design from
the true distributions and the true inefficiencies.

## Primary endpoint and predictions (written before the run)

Ratio of the mean-square error of arm 3 to arm 1 for the end-to-end free-energy difference, with a
bootstrap 95 % interval, per system, chain kind and profile (18 cells).
* P1 (theory, exact for **L**): the ratio equals `V*_c(costs a_kC_k)/V_c(equal steps / C)` up to the
  safeguard; it is computed from `population.optimal_allocation` before the run and stored with the
  results.  Success: the measured ratio is within its interval of the prediction in at least 16 of 18
  cells for **L**, and below 1 in every cell where the prediction is below 0.85.
* P2: arm 4 is worse than arm 3 wherever the profile is not flat; equal to it when it is.
* P3: arm 2 has the smallest error of the equal-step arms but its asymptotic interval covers in far
  less than 95 % (as in experiment C).
* P4 (**M**): no exact prediction; reported, not judged.
Failure of P1 for **L** would refute the practical use of A12(b) with estimated inefficiencies.

## Secondary endpoints (certificate; no theorem covers them — B7)

Coverage and width of the region on samples thinned by 1, 2 and 3 times `ĝ_k`, and by the stride that
makes the remaining correlation at most 0.01 (computed from the exact spectrum).  Model check on chains
started in the wrong well with no burn-in: rejection rate against the number of steps discarded.
A coverage below 95 % here refutes no statement; it measures a use outside Theorem B2.

## What it cannot show

Anything about a molecular sampler; anything about inefficiencies that the pilot cannot see (slow modes
not visited in the pilot — the trapped case of experiment B).
