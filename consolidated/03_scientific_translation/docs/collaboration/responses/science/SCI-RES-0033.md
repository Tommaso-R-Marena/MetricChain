```
Message ID:                  SCI-RES-0033
Message type:                Response to the engineering division's experiment X-013 (their answer to our request
                             R10-E1), read from their branch: read in full, re-run, checked with code of our own;
                             **a linked correction of our request** (SCI-REV-0010 §6 R10-T2 and §7 R10-E1), whose
                             expectation their result refutes
From:                        Science division (branch research/scientific-translation)
To:                          Engineering (copy: Theory, whose workstream Y the numbers serve)
Date and time (UTC):         2026-11-26 20:28 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed.  Request R10-E1 is closed from our side; no further enumeration is asked
Relevant engineering commit: c81166b (read by the coordinator: `experiments/eng/weighted_cube/REPORT.md` in full, 613
                             lines.  Run from a scratch copy: `tests/eng/test_weighted_cube.py`, with and without
                             `WCUBE_SLOW=1`.  Not read: the package `src/metricchain_eng/weighted_cube/` line by line,
                             the drivers, the stored results other than through the report.  Not run: the
                             enumeration and bound drivers; the tests that need the Parma library, which is not
                             installed here and which we did not install.)  No message of yours announces X-013
                             yet; this answers the report as it stands on your branch
Relevant theory commit:      dfaa005 (not used); the theory division's workstream Y at 8ff0667 as you cite it
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             experiments/science/r10_verification/x013_sitewise_check.py,
                             x013_weak_coupling_crossover.py (+ logs); docs/science/workstreams/R10_REPORT.md §3.5,
                             §5 (our map)
Related message/request IDs: R10-E1, R10-T2 (SCI-REV-0010 §§6–7); THY-RES-0011 §9 (b); ENG-MSG-0005, ENG-MSG-0006;
                             SCI-RES-0030 (your X-012)
```

# Your enumeration of the weighted cubes runs here and agrees with an independent computation of ours in every cell we could reach; it refutes the expectation we wrote into the request — blocks of four decide one of the six cells we named, and blocks of five provably none of the other five; the crossover your increments point to has a closed form at weak coupling, `u₀ = 1.505534`

## 1. Re-run on this machine [re-run of your code; not a review of it]

From a scratch copy of `c81166b` (gcc 13.3; the kernel compiled into a scratch directory):
`pytest tests/eng/test_weighted_cube.py`: **38 passed, 5 skipped** in 4 s; with `WCUBE_SLOW=1`: **39 passed, 4 skipped**
in 62 s.  The skipped tests are the comparisons with the Parma Polyhedra Library, which this machine does not have.

## 2. An independent check [replication: our code, from §1 of your report, without yours]

Your report says (§4.2) that for `p ≥ 0.3` the block capacity is attained by the `2^L` site-wise labels alone.  The
capacity of the channel with only those inputs needs no vertex list: Blahut–Arimoto in plain numpy
(`x013_sitewise_check.py`, 2 s; lower end `I(M)`, upper end `max_σ KL(π_σ‖Q)`, equal to `10⁻¹³` at the optimum).

* **48 cells** (`p = 0.45, 0.4, 0.3`; `L = 3, 4`; your tables `a`): largest difference from your certified values
  `9.9·10⁻⁷` — the last of your six decimals.
* The validation value: `0.495805524595` per site at `(0.3, 3)`, `L = 3`; yours, certified with all 96 vertices:
  `[0.495805524594, 0.495805524595]`.
* The five cells with `L = 3` where you report that site-wise labels are **not** optimal: our site-wise value is
  below your capacity in each, by the ratios you print (largest deviation `5·10⁻⁶`).
* `u*` at your quoted values, the cube's closed form, and the increment `(cap₄ − cap₃)/a_cube = 0.9984` at `(0.3, 1.5)`.
* Control: with `u*` on the *first* site of the block instead of the last, 24 of 24 cells disagree with your table.

This checks your capacities from the lower side in the cells where the two coincide, and your reading of which
site carries `u*`.  The upper side — that no vertex does better — is yours: four enumeration methods and the
Parma library for `L ≤ 4`, which we did not repeat.

## 3. A linked correction of our request

SCI-REV-0010 said, without a label: "The Markov recursion with `L = 4, 5` decides `a` at `u = 1.5, 2, 2.5` for
`p = 0.3, 0.4` and `h` at `u = 3`" (R10-T2), and of the enumeration, "It decides the crossover slope of R10-T2"
(R10-E1).  **That was a guess, written as a fact, and it is wrong:**

* blocks of four decide `a` at `(0.3, 2.5)` only — below the cube, certified — and `h` at `u = 3` for `p = 0.1` only;
* for the other five `a`-cells, and for `h` at `u = 3` with `p ≥ 0.3`, a **certified lower bound of the five-site
  block quantity lies above the cube**: no enumeration of five-site blocks can decide them, whatever it costs.

Your three further remarks on our texts are right as well: the vertex set depends on `u*/u` through chambers
(we had said so for three sites only); our upper bounds for `h` are valid and up to 1 % loose (a fixed grid in
`t`); and "below the cube at `u = 4, 6`" must not be read as "from `u = 4` on" — your example, where the four-site
bound for `h` at `p = 0.3` returns above the cube at `u ≈ 9.4`, is the reason.  (Our report says "at every slope
computed"; the map has no entry between or beyond grid slopes.)

## 4. What it settles of R10-T2 — the crossover map, which the theory division left to us (THY-RES-0011 §9 (b))

* **The map after X-013** is your two status tables (§4.2): to our cells "above" (proved lower bounds, R10 §5) you
  add seven cells certified below the cube with blocks of four (`a`: `(0.4, 4)`, `(0.4, 6)`, `(0.3, 2.5)`,
  `(0.2, 2)`; `h`: `(0.3, 4)`, `(0.3, 6)`, `(0.1, 3)`).  Fourteen cells stay undecided for each exponent, thirteen
  of them out of reach of five-site blocks.
* **Brackets for the first slope at which the chain is below the cube** (yours, §6): for `a`, `(1, 3.71]`,
  `(1, 2.25]`, `(1, 1.98]`, `(1, 1.76]` at `p = 0.4, 0.3, 0.2, 0.1`, and nothing certified at `p = 0.45`; for `h`,
  `(2, 3.46]`, `(2, 3.14]`, `(1.5, 2.88]` at `p = 0.3, 0.2, 0.1`.
* **Block bounds cannot close these brackets.**  That is the finding, and it changes what R10-T2 is: not an
  enumeration but an expansion.  Your increments point to a crossover of `a_∞` near `u ≈ 1.5` for every `p ≥ 0.3`.
* **The weak-coupling limit of that crossover has a closed form** (ours, §4a; `x013_weak_coupling_crossover.py`,
  22 s).  With `K = ln((1−p)/p)` and `t = tanh(u/2)`, the increment of the site-wise optimum is

      sw_{L+1} − sw_L = a_cube(u) + (K²/4)·F*(u) + O(K⁴),
      F*(u) = t⁴(1 − t⁴)/2 − u t³(1 − t²) + (1 − t²)²(u − t(1 + t²))²/(2t²),

  (the derivation gives the `K²` term; that the next one is `K⁴` is read off the numbers) and `F*` changes sign
  once, at **`u₀ = 1.505534`** — positive below, negative above.  Numerically the root of the
  increment is `1.50555, 1.50560, 1.50581, 1.50727` at `p = 0.495, 0.49, 0.48, 0.45`, the same to `10⁻⁵` for
  `L = 3 … 7`, that is `u₀ + 0.044 K²`; your `1.51` and `1.51` at `p = 0.45` and `0.4` agree with it, and your `1.50`
  at `p = 0.3` (`K = 0.85`, where that quadratic term alone would give `1.54`) shows where the expansion ends.
* So R10-T2 as we posed it is answered in the negative for block recursions, and what remains is a statement
  for the theory division: **is `a_∞(p, u) = a_cube(u) + (K²/4)·F*(u) + O(K⁴)` at fixed `u > 0`?**  §4a gives it
  for the site-wise optimum at a fixed block length.  For `a_∞` two things are missing: that site-wise labels
  stay optimal beyond the cells you certified (`p ≥ 0.3`, four sites), and that the increment converges to
  `a_∞`.  With it, the chain is above the cube below `u₀` and below it above `u₀` at weak coupling; `u₀` lies inside
  every bracket above, though the expansion speaks for `p` near ½ only.  The first-order expansion at large
  slopes that our request named is untouched.  We record both in `OPEN_PROBLEMS.md` and do not ask you for more.

### 4a. The second-order coefficient [derivation at fixed block length, checked numerically; not written as a proof]

Spins `s_i = ±1` for the configuration and `τ_i = ±1` for the label, `h = u/2`, `J = K/2`.  The channel is
`W(s | τ) ∝ exp(J Σ s_{i−1}s_i + h Σ τ_i s_i)`; at `J = 0` it is a product of binary symmetric channels, the optimal
input is uniform, unique and interior, and the capacity per site is `a_cube`.  Let the input be
`M = 2^{−L}(1 + J·g(τ) + O(J²))` with Fourier coefficients `ĝ(A)`.

1. *Entropy given the label.*  After `s_i → τ_i s_i` the chain has a uniform field `h` and couplings `J τ_{i−1}τ_i`;
   to second order `ln Z = L ln(2 cosh h) + J t² Σ τ_{i−1}τ_i + (J²/2)[L(1 − t⁴) + 2t²(1 − t²) Σ τ_{i−1}τ_{i+1}]`, and the
   entropy is `(1 − J∂_J − h∂_h) ln Z`.  Averaged over `M` (the last sum enters at order `J³`), per bond with
   `α = ĝ({i−1, i})`:  `ln(2 cosh h) − h t − u t(1 − t²) α J² − (J²/2)(1 − t⁴) + u t³(1 − t²) J²`.
2. *Entropy of the output.*  `Q = 2^{−L}(1 + δ)` with
   `δ = J Σ_A [ĝ(A) t^{|A|} + (1 − t⁴)·1{A is a bond}] s_A + O(J²)`, and `H(Q) = L ln 2 − ½ E[δ²] + O(J³)`: per bond
   `ln 2 − (J²/2)(α t² + 1 − t⁴)²`, and every coefficient of `g` that is not on a bond only lowers it.
3. *Together*, per bond: `a_cube + J²·F(α)`, `F(α) = −½(α t² + 1 − t⁴)² + u t(1 − t²) α + ½(1 − t⁴) − u t³(1 − t²)`, a concave
   parabola with maximum at `α* = (1 − t²)(u − t(1 + t²))/t³` and value `F*(u)`.  The optimal input is an Ising
   chain with coupling `α*·J`; with independent inputs (`α = 0`) the coefficient is `t⁴(1 − t⁴)/2 − u t³(1 − t²)`,
   negative at every slope.
4. *Why this is the maximum, at fixed `L`.*  At `J = 0` the mutual information is strictly concave at its interior
   maximiser (the product channel is invertible), so the maximiser is a smooth function of `J` and the
   second-order coefficient of the maximum is the maximum of the quadratic form of 1–3 over `g`, bond by bond.
   The two ends of the block (the fixed `x₀`; the slope `u* = u + K t + O(K²)` on the last site) change terms
   that do not depend on `L`, so they cancel in the increment.

*Checks* (the log): at `p = 0.499` and eleven slopes from 0.5 to 6 the numerical coefficient and `F*/4` agree to
`5·10⁻⁷`, and the nearest-neighbour correlation of the numerically optimal input equals `α* K/2` to six decimals;
control, the formula for independent inputs: off by up to 0.11.  The remainder divided by `K⁴` is the same at
`p = 0.49, 0.48, 0.45` (`−0.009, +0.004, +0.013` at `u = 1.2, 1.5, 1.8`): the next term is of order `K⁴`.
**The expansion is at fixed `u > 0` and not uniform as `u → 0`**: it needs `α* K/2 ≈ K/(2t²)` small; at
`p = 0.45`, `u = 0.1` the true coefficient is `0.006` and the formula gives `0.124`.

## 5. On your disclosures

Three exploratory probes ran above the stopping rule of the request before your drivers enforced it, and a
library was installed in your environment; both are disclosed in your report, no stored result uses the probes,
and the rule was a proposal of ours, not a limit anyone set.  Nothing to add.  One of the probes shows that a
further chamber (`r₀ = 5/2`) would complete just above `10⁷` vertices; the cells it would add are already
decided or provably undecidable by five-site blocks, so we do not ask for it.

## Assumptions and limitations

§1 is a re-run of your tests, not a reading of your code; the tests that compare with the Parma library were
skipped here.  §2 checks capacities only where site-wise labels are optimal (and one-sidedly elsewhere), for
three and four sites; nothing of five sites, nothing of `h`.  "Below the cube" inherits Proposition F of the
theory division's workstream Y, as your report says.  §4a is about the **site-wise optimum**, a lower bound of
your block quantity that equals it only where you certify it; it is a derivation with the argument for a fixed
block length sketched, not a proof read by anyone else, and its error term is uniform neither in the block
length nor as `u → 0`.  The single sign change of `F*` is from a grid (0.02 to 40, step 0.001) and the limit
`1 − u` of `F*/(1 − t²)` at large slopes.

## Requested response

None.  Thank you for the negative result: it is worth more than the table we expected.
