# Predictions written before the runs of this directory

Written before `export_cert.py`, `check_cert.py` and `controls.py` were run for the first time (neither the
exporter nor the checker had been executed when this file was written; the file is committed with them).
Outcomes are appended below each prediction after the run, with the clock time of the run.

## P-1.  Ace-Val₆-NMe, strand backbone, order 4, band 5 (every pair in the band)

1. The exporter's integer certificate is **accepted** by the checker.
2. The claimed ends lie within `1e-5` nats of the floating-point pipeline's values of SCI-MSG-0025 §8
   (`ln Z(m₊) = 198.067925`, `ln Z(m₋) = 198.068096`), and the bracket is not narrower than the floating-point
   one by more than `1e-6` nats at either end (the integer penalties are the smallest that satisfy the
   inequalities for the published intervals, so they may be slightly smaller or slightly larger than the
   floating-point ones: smaller where our code's absolute allowance `5e-9·Γ` exceeds the interval slack, larger
   where the interval slack of the double-counting identity enters the site numbers).
3. Enumeration of the 729 states: `m_lower ≤ E ≤ m_upper` at every state (0 violations); the exact
   `ln Z(E) = 198.068008` lies inside the claimed bracket.
4. Integer penalties differ from the floating-point ones by less than `1e-6` kcal/mol (site and pair).

## P-2.  Ace-Val₂₀-NMe, polyproline II, order 5, band 8

1. **Accepted.**
2. Claimed bracket within `1e-4` nats of `[518.255189, 518.271430]` at both ends.  Less sure than P-1: here the
   floating-point pipeline had every out-of-band pair sum available and added them directly, whereas the
   certificate carries only the in-band pair sums and bounds the out-of-band ones by the double-counting
   identity with interval ends; the site numbers therefore carry the slack of up to
   `(m − 1)·3e-9·Γ + 16·6e-9·Γ` per site, divided by `2·C(5,2) = 20`.  If `Γ` is of order 10³ kcal/mol or more this
   is visible in the fifth decimal of the bracket; if it is of order 1–10 it is not.  (I do not remember `Γ` for
   this instance; the run prints it.)
3. Checker time: 20–40 s for the two transfer matrices in interval arithmetic (`3⁸` tails × 3 states × 20 sites
   ≈ 4·10⁵ interval exponentials per model at ≈ 30 µs each).

## P-3.  Controls (every mutation of an accepted file must be rejected, for the stated reason)

A pair number lowered by one unit → B1; a site number lowered by one unit → B2; the constant lowered by one unit
→ B3; each of these with the tables `m_∓` left unchanged → B1/B2/B3 (the covering check comes first), and with
the tables made consistent with the lowered penalty → still B1/B2/B3; a table entry of `m_lower` raised by one
unit → D; a table entry of `A_lower` raised by one unit with `m_lower` unchanged → D; the claimed lower end
raised, or the upper end lowered, by `1e-6` → E; an interval of step A with `lo > up` → malformed; a duplicate
key → malformed; a floating-point literal → malformed; a step-A upper end raised by a few units (which makes the
right side of B1 larger) → B1.  **One control I expect to be accepted, and it must be:** a penalty *raised* by
one unit with the tables made consistent and the claims unchanged is still a valid certificate unless the claimed
bracket was tight to within the effect of one unit (`2⁻⁴⁰` kcal/mol ≈ `1.5e-12` nats — far below the `5e-9`
widening), so it is accepted; a checker that rejected it would be checking equality with our producer, not
validity.

---

# Outcomes (appended after the runs; times from the logs)

**P-1 (Val₆; exporter 00:34:24 UTC, checker 00:34:31 UTC on 27 November 2026).**  1 — accepted: **as
predicted.**  2 — claimed ends `198.067925225`, `198.068095790`: within `6.1e-9` nats of the floating-point
values, and the integer bracket is *wider* than the floating-point one by `9.4e-11` / `9.6e-11` nats before the
widening of the claim: **as predicted** (the alternative "slightly narrower" did not occur).  3 — 0 violations
in 729 states, smallest margins `1.000e-07` kcal/mol at both sides; exact `ln Z = 198.068008142` inside: **as
predicted.**  4 — largest differences `8.0e-10` (site), `3.8e-10` (pair) kcal/mol: **as predicted.**

**P-2 (Val₂₀; exporter 00:34:45 UTC, checker 00:35:36 UTC).**  1 — accepted: **as predicted.**  2 — claimed
bracket `[518.255189142, 518.271429999]`, within `6.1e-9` nats of the floating-point values; `Γ = 0.0822`
kcal/mol, so the slack of the double-counting bound is invisible: **as predicted**, in the branch "of order
1–10 or less".  3 — checker time **10.4 s** on the first run, 9.5 s later, against a predicted 20–40 s:
**missed, by a factor of two to four**.  Both factors of the estimate were too high, as a timing made after
the run shows: the recursion has `12·3⁹ + 3⁸ + … + 3 = 246 036` terms per model, not `20·3⁹ ≈ 3.9·10⁵` (the
last eight sites have shorter tails — I counted every site as a full one), and a term costs about 21 µs at 30
digits (16.6 µs for the exponential, 4 µs for the product and sum), not 30 µs.  `2 × 246 036 × 21 µs ≈ 10 s`.

**P-3 (controls; first complete run 00:42:29 UTC, 50.9 s; last run with test vectors 00:48:59 UTC, 51.6 s).**
85 of 85 behaved as expected, including the mutated files that had to be accepted.  Three things to record
against the prediction as written above.  (a) The list above was written before the consistency checks A0
existed; they were added after the first acceptance of the two files and before the controls were written,
and the controls on them (data of another order, exchanged tables, inward rounding) were predicted only in
the controls script itself, not here.  (b) One expectation in the first draft of the controls script was wrong
and was corrected by reasoning **before** the first run: for "unit changed to `2⁻³⁹` with the integers
unchanged" I had written the label B; halving the unit makes every covering inequality easier, and the file
fails only at E.  (c) The interval-arithmetic comparison of the first draft of the checker relied on the
comparison operators of `mpmath` intervals; it was replaced by an exact comparison of rational end points
before the controls were run.  No control failed at any run.
