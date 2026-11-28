# Predictions, written before any certificate was run

*2026-11-28 05:48 UTC (from `date -u`).  At this time the library module
`src/metricchain_eng/certinf/multistate.py` exists and has not been executed on samples; the only
computations done are exact population quantities of candidate models (overlaps of adjacent states,
the probability of the rare event), used to fix the design below.  No certificate, no interval and no
sampled quantity has been computed.*

## Design (frozen)

State space: 1000 grid points `x = (i + 1/2)/1000`.  Potential `V(x) = h ((x − 1/4)(x − 3/4)/0.0625)² + 2x`
(a double well with a barrier of height `h` at `x = 1/2`, the right well raised by 1).  State 0 (the
target) is `q_0 = e^{−V}`; states 1–6 are harmonic windows `q_j = e^{−V − κ (x − c_j)²/2}` with centres
`c = 0.30, 0.35, 0.40, 0.44, 0.47, 0.50`.

| model | `h` | `κ` | `p_0`(barrier), barrier = `[0.45, 0.55]` | total-variation distance of adjacent states |
|---|---|---|---|---|
| R10 | 10 | 1500 | 3.786·10⁻⁵ | 0.51 – 0.64 |
| R14 | 14 | 2200 | 9.435·10⁻⁷ | 0.60 – 0.73 |

Class: an energy error `|d(x)| ≤ ε` on the target state, i.e. envelope ratio `Γ = e^{2ε} ∈ {1, 3}`; no
measured averages.  Target of inference: the upper end `V⁺` of the identified interval of `E_p f`, exact by
enumeration.  Observables: `barrier` (indicator of `[0.45, 0.55]`), `right` (indicator of `x > 1/2`;
`p_0 = 0.273`), `position` (`f = x`).

Methods, all at total level 0.05, half of the draws for the pilot and half for validation:

* **T** — target only: all `N` draws from state 0; the product test of Theorem 5.1.
* **P-all** — Theorem M1: `N/7` draws from each of the seven states, all pooled; free-energy intervals at
  level 0.02 from bridge averages with shortest-path closure, product test at level 0.03.
* **P-sel** — the same on a sub-mixture chosen by the pilot: state 0 and the windows that put at least a
  quarter of their pilot draws where the score is positive.
* **G** — the interval built as in item G2 of the MBAR division's imported package (a Chernoff interval
  for the pooled average of `π_0(f_0, x) A(x)`, widened by `e^{±r}` with `r` a bound of the oscillation of
  the free-energy error), fed with the same free-energy intervals; indicators only; for `Γ > 1` its upper
  end is mapped through `μ ↦ Γμ/(1 + (Γ−1)μ)`.

Cells: `barrier` on R10 and R14, `Γ ∈ {1, 3}`, `N ∈ {4·10⁴, 2·10⁵}`; `right` and `position` on R10,
`Γ ∈ {1, 3}`, `N ∈ {4·10³, 4·10⁴}`.  200 repetitions (100 at `N = 2·10⁵`).

## Predictions

| | prediction | how it could fail |
|---|---|---|
| **Q1** validity | in every cell and for T, P-all, P-sel: the fraction of certified values below `V⁺` is at most 0.05 (expected: at most 0.01) | a miss rate above 0.05 anywhere refutes the theorem or the code |
| **Q2** rarest event (R14, `barrier`) | median of certified value / `V⁺`: P-sel at most 15 at `N = 4·10⁴` and at most 4 at `N = 2·10⁵`; T at least 100 and at least 25; so P-sel is better by a factor of at least 8 in all four cells | free-energy intervals wider than estimated (about ±2 and ±0.9 along the ladder) |
| **Q3** rare event (R10, `barrier`) | P-sel and T are within a factor 3 of each other in all four cells: the cost of certifying the ladder is about the cost of counting the event | either method winning by more than 3 |
| **Q4** common observables (`right`, `position`) | T has the smallest median excess in all eight cells; P-sel's excess is 1.5 to 5 times T's (the draws spent on windows are lost); P-all's excess is at least 3 times T's (the free-energy intervals enter at first order) | pooling helping a common observable |
| **Q5** against G | `barrier`: G's ratio is at least 5 times P-sel's in the four R14 cells (a Chernoff bound for summands known only to lie in `[0, 1]` cannot be relatively accurate); `right`: G returns a value at least twice `V⁺` at `N = 4·10⁴` because it widens by the oscillation over the whole ladder | G within a factor 2 of P-sel on R14 |
| **Q6** abstention | P-all and P-sel abstain (inconsistent or unbounded free-energy intervals, or the realised envelope above the bound declared from the pilot) in at most 2 % of the runs of every cell | more abstentions |

For the shared-error statement (Proposition M2), `shared_error.py`:

| | prediction |
|---|---|
| **Q7** | on every random pair of distributions on 10 points and every `ε ∈ {0.05, 0.3, 1, 2}` the extreme values over all `2¹⁰` sign patterns of the error equal `shared_error_extremes` to `10⁻¹²`, no interior error exceeds them, and the bound `ln(1 + (e^{2ε} − 1)·TV)` is never violated |
| **Q8** | the composed interval (bridge interval for the model's difference, widened by the bound with a certified upper bound of the total-variation distance) misses the true difference in at most 5 % of 500 repetitions with the error at its worst case, and is narrower than "bridge interval ± 2ε" for the adjacent pair tested |

Everything is reported as it comes out, including refuted predictions.
