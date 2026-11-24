# Referee report on workstream B — "chain-structured known parts"

Report reviewed: `<session scratch>/ws/B/REPORT.md`
(identical, up to one path line, to `docs/workstreams/B_REPORT.md`).
Referee scratch directory (all scripts `r*.py`, all outputs `out_*.txt`):
`<session scratch>/referee_B/`

All numerics below were produced by my own code (none of the author's scripts was run or imported).
The author ran no Lean and left no Lean files, so there was nothing to type-check.
The web-search budget of the session was exhausted before my first query (0 searches possible); the
literature check is therefore limited to direct fetches of known addresses (§4).

---

## 0. Summary

**Verified** (proof re-derived line by line *and* independent numerics):

* **Theorem B.12** (sharp hint-free accuracy threshold for identical two-state sites, `ε₁* = max_θ G(θ)`),
  with **B.11** (tilted sandwich, exact width `n·max(D(c;θ), D(−c;θ))` for product references) and
  **B.10** for independent sites.  The tilted sandwich was tested on *all* vertices of the Lipschitz
  polytope of `Q_n` for `n ≤ 4` (11 200 parameter/tilt cases) and `n = 5` (36 cases × 395 094 vertices):
  worst-case width `= n·max(D(±c;θ))` to `4·10⁻¹⁴`.  It is the two-state case of Theorem 11.28(d) of the
  current theory report (I checked the reduction).
* **Theorem B.1** (droplet criterion; Ising `τ = 2h` for every `J ≥ 0`): 4 000 random inhomogeneous chains
  (`k ∈ {2,3}`, `n ≤ 7`), exact `N_cov = 1` test, zero mismatches.
* **Theorem B.5** (vacuous window `2h < c ≤ 2(J+h)`): proof correct; 4 000 random `(J,h,c)`; exact covering
  numbers in the window grow (table 3.1 reproduced exactly, `n = 4…10`, all ten rows).
* **Theorem B.6** (a) proof correct, LP check on 135 decisive instances; (b) the closed form
  `cosh(ct/2) ≥ e^{2Jt}cosh(ht)` is confirmed numerically and is sharp to `10⁻³` in `x²`, but its proof is
  only sketched; at `h = 0` it is Gray's critical distortion (formula confirmed in a source).
* **Theorem B.2** (exact exponent `R* = sup_ν R_ν(e(ν))`): I found **no gap**.  Every step holds under the
  stated hypotheses, including `ε = 0`; the two cited textbook lemmas are used within their hypotheses (§2, B.2).
* Proposition **B.4** (block brackets; `0.21508 ≤ R* ≤ 0.24167` at `c = 4J`, `L = 12`, recomputed with my own
  LP; also `L = 6, 8, 10`), Proposition **B.8** (soft-gap identities), Corollary B.7 constants, and every
  table entry I recomputed (about 140 numbers) agree with the report to within one unit of the last printed digit.

**False**

* **Conjecture B.13 is false as stated**, in three independent ways (explicit witnesses, verified in
  50–60-digit arithmetic by a standalone script):
  (Z1) `θ = 0`, an antiferromagnetic complete graph on 4 sites with fields, `βc = 1.5`: a non-additive vertex
  gives `1.00985 > 0.99202 =` best additive value;
  (Z2) `θ = 0`, a **tree** (star `K_{1,3}`): margin `4.4·10⁻⁵`;
  (T1) tilt `θ = 0.95c`, a **homogeneous antiferromagnetic open chain of 3 sites**: `7.9642 > 7.5134`.
  The author's evidence (6 100 random models, Nelder–Mead) had no power: violations sit in strongly coupled,
  tuned regimes of relative volume `≲ 10⁻⁴`.  What survives my search: all laws on `{0,1}²`; open chains
  (paths) at `θ = 0` (`n = 4`: 0 violations in 9.4 million tuned models); homogeneous chains at the specific
  tilt `θ*`; ferromagnetic homogeneous chains with any tilt (the last two by random sampling only).

**Wrong or overstated**

* The sentence after B.12, "for chains … `W(θ*) = ε₁*` iff additive residuals are extremal", is false for
  antiferromagnetic chains (the best *additive* residual is staggered: `0.255` per site against
  `ε₁* = 0.0465` at `(J,h,c,β) = (−½,0,1,1)`), and the uniform chord gap is then not the class threshold.
* Several sentences of the verdict paragraph are stronger than what is proved (list in §2, MAJOR-3).

**Unproved in the report / not verified by me**: tightness half of B.3, rows 2–3 of B.9, the analytic step
of B.6(b) for `h ≠ 0`, Remark B.2″ (heuristic), the "not finitely correlated" claim (numerical).

---

## 1. Verdict per statement

| statement | correct? | how checked | depth | novelty | remark |
|---|---|---|---|---|---|
| **B.12(a)** bounded cost above `ε₁*` on every instance | **yes** | re-derived (tensorisation, convexity in the increment, Bregman identity, McDiarmid); exhaustive vertex enumeration `n ≤ 5` (`r2_B12.py`) | short | closed form new in the project; two-state case of Thm 11.28(d) | sample size `N ≥ 2β²(c+|θ*|)² ln(2/δ)/(n(ε₁−ε₁*)²)`, decreasing in `n` |
| **B.12(b)** exponential below `ε₁*` at `θ*M` | **yes** | re-derived from Thm 11.24(b) of the theory report (taken as given: machine-checked there); single-site game `= G(θ)` on 1 000 random cases; exact dip-packing numbers `n ≤ 800` (`r2b_dips.py`, `r2c_game.py`) | short | as above | exponent small near the threshold (`0.0068` at `ε₁ = ½ε₁*`) |
| **B.11** tilted sandwich | **yes** (product case exact; general lower bound `W_n ≥ nD − O(1)` by `g = ±cM`) | as B.12(a) | short | routine | the constant `c+|θ|` in the Hoeffding/McDiarmid bound is right (range of `g−θM` is `≤ n(c+|θ|)`) |
| **B.10**, independent sites | **yes** | algebra re-derived (`Λ₁(0) = P(θ)−P(c)`, `Λ₁(1) = β(c+θ)+P(θ)−P(−c)`, maximum at `μ* = (c−θ)/2c`) | short | new in the project | — |
| **B.10**, chains (lower bound) | **yes**, tag [T*] fair | block formula for `Λ̄` checked numerically (`L = 5…320`, `O(1/L)` convergence, `r6_B8.py`); thresholds table of §2.6 reproduced (7 rows) | short | new in the project | "exactly where the dip bound stops" for ferromagnetic chains is numerical (not re-checked) |
| **B.1(a),(d)** droplet criterion, `τ_n = 2h` | **yes** | re-derived; brute force (`r3_B1.py`) | elementary | routine, apparently new in this form | holds for *every* admissible residual: `N_cov(g) = 1` iff the criterion (checked on random non-additive `g`) |
| **B.1(b)** ratio cycle, `τ = 0` for degenerate ground states | plausible | Ising cases only | elementary | routine | not checked for general chains |
| **B.1(c)** dichotomy bound | **yes for the zero residual** | re-derived | elementary | routine | statement does not say "zero residual" (MINOR-1) |
| **B.2** exact exponent | **yes** (paper proof; no gap found) | re-derived step by step incl. Lemma C.1; one-shot ring values recomputed (7 rows of table 3.2) | moderate, standard tools (blocking, type covering, Fano) | apparently new statement; method classical | valid for `0 ≤ ε_n = o(n)` incl. `ε = 0`; needs `κ < 1` |
| **B.2′** `0.007/ρ ≤ R* ≤ ln2/Δ_max` | **yes** | arithmetic re-done; grid covers by brute force (`r9_gridcover.py`) | elementary | routine | "valid *exactly* when the criterion holds" is too strong (MINOR-4) |
| **B.2″** quadratic vanishing | heuristic | not checked | — | — | labelled [H] |
| **B.3** bound | **yes** | direct from Thm 11.6(b); own run-length-limited certificates with own JSR bounds (`r8b_jsr.py`) | one step | routine | tightness: sketch, not checked; table values not reproduced to the last digits (MINOR-7) |
| **B.4** block brackets | **yes** | re-derived; own orbit-reduced LP, `L = 6,8,10,12` (`r5_B4.py`, `r5b_L12.py`) | short | routine | `[0.21508, 0.24167]` at `c = 4J` (report: `0.21507, 0.24166`) |
| **B.5** vacuous window | **yes** | proof re-done (factorisation `A(w−1)(Aw−1)/w`); random scan (`r4_B5.py`); exact `N_cov` (`r4c_ncov.py`) | elementary | new observation | — |
| **B.6(a)** `V = B` iff `K⁻¹b ≥ 0` | **yes** | LP duality re-derived; 135 decisive LP instances (`r4b_B6.py`) | one step | known (tight Shannon lower bound ⇔ backward channel) | — |
| **B.6(b)** closed form | **yes numerically**; proof incomplete | 600 random + 53 boundary parameter sets (`r4b_B6.py`, `r4d_boundary.py`); `tr`, `det` of `D₀TD₁T` re-derived | short | `h = 0`: Gray (1970); `h ≠ 0`: not found in what I could read | invariant-interval step only asserted (MINOR-5) |
| **B.6(c)** | **yes** | re-derived | elementary | — | — |
| **B.7** | (i) **yes** (proof re-done); constants `ρ_pos = 0.243073`, `ρ₁ = 0.220366`, `c_pos(h)` reproduced | `r4_B5.py` | short | new | (iii) strictness "rigorous" only up to floating-point LP |
| **B.8** soft gap identities | **yes** | brute force vs matrix products (`r6_B8.py`), `10⁻¹⁴` | definitional | known in substance (HMM / random-field chain) | "(iv) … there is none" is an unproved impossibility claim (MINOR-6) |
| **B.9** three budgets for chains | rows 2–3 **not proved** (author: sketch) | entropy, `R_β` bound, `U_β` of 5 table rows reproduced (`r6b_table25.py`) | — | — | verdict paragraph overstates (MAJOR-3) |
| zero-temperature limit of `E_π e^Λ` | fixed-`n` limit **yes**; counts 4096, 324, 92, 62 reproduced | `r8_misc.py` | elementary | routine | exchange of the limits `β→∞`, `n→∞` not shown |
| **Conjecture B.13** | **FALSE** | explicit counterexamples (`r7w_standalone.py`, `r7t_verify_theta0.py`, `r7s_verify_tilt.py`) | — | — | see MAJOR-1 |
| "for chains `W(θ*) = ε₁*` iff additive extremality" | **false for antiferromagnets** | `r7q_additive_patterns.py` | — | — | see MAJOR-2 |

---

## 2. Errors and gaps

### CRITICAL
None in any statement claimed as a theorem.

### MAJOR-1.  Conjecture B.13 is false (§2.6; §1 last sentences; §5 item 4; §6 step 1)

Notation of the report: `π ∝ exp(Σ_{i<j} J_ij s_i s_j + Σ_i h_i s_i)`, `s_i = 1 − 2y_i`,
`Φ(g) = ln E_π exp(−β(g − θM − E_π[g − θM]))`; tables below list `g/c` at the index `v = Σ_i y_i 2^{i−1}`.

* **(Z1) `θ = 0`, complete graph, `n = 4`, `β = 1`, `c = 1.5`.**
  `J₁₂ = −4.1`, `J₁₃ = J₁₄ = J₂₃ = J₂₄ = −4.6`, `J₃₄ = −7.5`, `h = (1.3, 1.3, 4.65, 4.65)`
  (`π`: 0.625 on `1100`, 0.0935 on each of `1010, 0110, 1001, 0101`).
  `max over the 16 additive g = 0.992017900733…`;
  witness `g/c = [0,1,1,2,−1,0,0,1,1,0,2,1,0,−1,1,0]` (c-Lipschitz, not additive): `Φ = 1.009850633840…`.
  52 of the 974 non-additive vertices beat every additive one.
* **(Z2) `θ = 0`, a tree: star with centre 1, `n = 4`, `β = 1`, `c = 1.66247`.**
  `J₁₂ = 1.1365`, `J₁₃ = −1.1483`, `J₁₄ = −5.9594`, `h = (5.9918, 2.3558, −2.3785, 6.1628)`.
  Best additive `0.344347818…`; witness `[0,1,1,2,1,2,0,1,−1,0,0,1,0,1,−1,0]`: `0.344391590…` (margin `4.38·10⁻⁵`).
  (This also answers the question left open in `DEAD_ENDS.md` D25 for binary Markov *trees*: additivity fails.
  By the gauge `y_i → 1−y_i` on leaves 3 and 4, the same example is a ferromagnetic star with non-uniform fields
  (checked: same margin), so "ferromagnetic" alone does not rescue the conjecture; uniform fields on a chain might.)
* **(T1) tilt `θ = 0.95c`, homogeneous antiferromagnetic open chain, `n = 3`, `β = 1`, `c = 6`.**
  `J₁₂ = J₂₃ = −2`, `h_i = −0.5`.  Best additive `7.513426478…`; witness `[0,−1,−1,−2,−1,0,−2,−1]`
  (`= −M + 2·[y₁ = y₃ = 1]`): `7.964184638…`.
  Further tilted examples (`r7s_verify_tilt.py`): antiferromagnetic triangle (`θ = 0.75c`, margin `0.0027`),
  a `±J` model on 4 sites (`θ = −0.96c`, `0.270`), homogeneous antiferromagnetic ring of 4 (`θ = −0.999c`, `0.600`),
  `J = −1.5`, `c = 4` open chain of 3 (`0.217`).

*Mechanism.*  (i) Any probability vector on the weight-2 slice of `Q_n` (the edges of `K_n`) is a limit of
pairwise measures (`E = L(M−2)² + Σ K_ij y_i y_j`, `L → ∞`), and on the slice two-valued "splits" that are not
restrictions of additive functions can be closer to the optimal two-point proportion: at `θ = 0`, 1 333 of
600 000 random slice measures for `n = 4` and 4 103 of 600 000 for `n = 5` violate the conjecture, and the
largest margin over slice measures is positive at every `βc` I tried (`2·10⁻⁴, 0.011, 0.028, 0.097, 0.53` at
`βc = 0.25, 1, 1.5, 2, 4`; `r7l_slice_opt.py`).  It is the "union of dips" phenomenon of D34.  (ii) With a tilt,
`Φ` is a two-measure functional (`ln E_{π'} e^{−βg} + βE_π g`, `π' ∝ π e^{βθM}`); two nearly degenerate
states of `π` plus weight of `π'` on a third state favour a maximum of two cones.

*Why the author's evidence missed it.*  Random sampling of couplings of order one has essentially no power:
with general random pairwise models I found 0 violations in 120 000 at `θ = 0` (`n = 3, 4`), and only a
sampler tuned to strongly coupled, nearly degenerate models finds them (rates `2·10⁻⁵` for stars, `4·10⁻⁵` for
`K₄`).  Nelder–Mead from random starts (I reproduced it: 300 + 200 starts, `n = 2, 3`) converges to degenerate
limits with margin `0⁻` and misses the violations that exist.

*What survives* (no counterexample; sizes of my search, exhaustive over all vertices unless stated):

| family | tilt | size | violations |
|---|---|---|---|
| all laws on `{0,1}²` | `|θ| ≤ 1.5c` | 14.0 million (law, `βc`, `θ`) triples (grid + log-scale) | 0 |
| open chains (paths), any couplings and fields, `n = 4` | 0 | 9.37 million tuned + 15 000 random | 0 |
| open chains, `n = 5` | 0 | 16 000 tuned | 0 (low power) |
| rings, `n = 4` | 0 | 2.12 million tuned | 0 |
| homogeneous chains/rings, both signs of `J`, at `θ = θ*_n` | `θ*` | `n = 3`: 79 461; `n = 4`: 15 870; `n = 5` (ferro): 493 | 0 |
| ferromagnetic couplings (chains, rings, complete, random graphs), random fields | `|θ| ≤ 2c` | `n = 3`: 400 000; `n = 4`: 60 000; `n = 5`: 5 120 (random sampling, **low power**: the gauge image of (Z2), a ferromagnetic star with `J = (1.1365, 1.1483, 5.9594)`, `h = (5.9918, 2.3558, 2.3785, −6.1628)`, violates at `θ = 0` with the same margin — `r7x_gauge.py` — and was not found by this sampling) | 0 |

*Counter-statement / fix.*  Replace B.13 by two separate open questions: (a) `θ = 0`, binary Markov **chains**
(paths) only — the theory report's open item 5; (b) homogeneous **ferromagnetic** chains with the pair
`(π_θ, θ)`, `|θ| ≤ c` — what the threshold on chains needs.  "Any signs, any graph, every θ", trees included,
is refuted; §6 step 1 ("… for chains (and trees)") and the evidence paragraph must be rewritten.

### MAJOR-2.  "For chains: … `W(θ*) = ε₁*` iff additive residuals are extremal" (after Theorem B.12; §1)

False in the "if" direction for antiferromagnetic chains: additive extremality would give
`W_n = max_ε Φ(cΣε_i y_i)`, and for `J < 0` the maximising sign pattern is staggered, not uniform.
`(J,h,c,β) = (−½,0,1,1)`: `ε₁* = G(0) = 0.04654`, staggered additive residual `0.25516` per site (ring of 12);
`(−1,½,2,1)`: `0.0817` against `0.858` (`r7q_additive_patterns.py`; in 96 % of 47 900 random antiferromagnetic
models at `n = 3, 4` the best additive vertex is not `±cM`).  Moreover the Hamming-Lipschitz class is invariant
under flipping a sublattice, so the zero-field antiferromagnetic class is isomorphic to the ferromagnetic one
and its true worst-case threshold is at least `0.25517`: the uniform chord gap `ε₁*` is a valid but far from
sharp lower threshold there.  *Fix:* state the chain corollary for **ferromagnetic** chains, with the two
hypotheses "non-additive residuals do not beat additive ones under `π_{θ*}`" and "uniform sign patterns are
the best additive ones" (the second holds in all my tests for `J ≥ 0`: excess `0` on rings, `O(1)` boundary
effects on open chains); for other signs take the chord gap over non-uniform additive instances.

### MAJOR-3.  Verdict paragraph (§1) stronger than what is proved

1. "the cost is exponential (Theorem B.1)": proved for the zero residual (and, with the obvious changes, additive
   ones), not for every residual.
2. "the exponent is positive for every `c > 0` and is `Θ(c/J)`" for *every* chain with degenerate ground state:
   `Θ(c/J)` is proved only for the zero-field Ising chain (Cor. B.2′).
3. "it is exact **only when** … iff `cosh(ct/2) ≥ e^{2Jt}cosh(ht)` at the optimal slope": at the level of the
   exponent neither direction is proved in general — sufficiency only for `c ≥ 9.08J` (`h = 0`), necessity
   only as floating-point LP brackets at `c/J = 6, 4, 3` (and `(1,¼,4.5)`); `V_n(t*) > B_n(t*)` for long rings
   does not by itself give `R* > max B`.
4. "the optimal dual weights are *not* finitely correlated": numerical observation at `n = 10, 12`.
5. "the three budgets of the report extend to chains by the same blocking argument": rows 2 and 3 of B.9 are
   not proved (the deterministic upper bound is "sketch only"; the third row is asserted).
6. "`E_π e^Λ` has no transfer-matrix closed form": no impossibility is proved; "its zero-temperature limit is
   the entropy of run-length-limited sequences": proved for fixed `n`, the exchange of limits is not.
7. "the dip bound … vanishes **exactly** at the chord gap" for chains: the converse half is numerical.
8. "for chains a rigorous lower threshold that is also the upper one if additive residuals are extremal": see
   MAJOR-1 and MAJOR-2.

### MINOR

1. **B.1(c)**: say "at the zero residual" (the proof uses `s = c·d_H`); the number of usable cells is
   `⌊n/ℓ'⌋ − O(1)` in general (boundary layer of the finite-chain minimiser), `−2` for the Ising chain.
   Part (a) can be strengthened for free: for every admissible `g`, `N_cov(g) = 1` iff the criterion holds
   (a covering centre must be the minimiser of `f+g`, and the criterion makes it the strict minimiser of `f`).
2. **B.2**: the parenthetical "(equivalently: stationary ergodic, or randomly-phased block-i.i.d.)" is not
   proved in the text.  The ergodic version follows from the proof; the block-i.i.d. version needs one more
   line (`σ(0)` is approached by block-i.i.d. processes with `e → 0`, and `R_ν(e) ≥ h(ν) − η(e)` by Fano).
   The claim about the one-shot values `R*_n` also deserves one line (`R*_n ≥ nR_ν(e(ν)+C/n)` with `P = ν_n`).
3. **B.2, Appendix C**: `I(Y;A|Φ) ≤ I(Y;A)` holds without the `ln L` (Markov chain `Φ − Y − A`); harmless.
4. **Cor. B.2′**: grid covers are valid *whenever* the mean-displacement criterion holds; "exactly when" is
   false at finite size (ring of 15, `c = 2J`, `Δ = 5`: criterion fails, cover valid).  Only sufficiency is used.
5. **B.6(b)**: the proof asserts that an invariant interval exists iff `D₀TD₁T` has real positive eigenvalues;
   this step is not shown.  Numerically the closed form is right and sharp (53 parameter sets at
   `x² = x²_bdry(1 ± 10⁻³)`, with and without field).  Tag should be [T at `h = 0` (Gray); T* otherwise].
6. **B.8(iv)**: "there is none" → "none is known".
7. **RLL certificates (table in §2.3)**: with my own JSR bounds (all words of length 12, weighted sup norm,
   crude weight optimisation) I certify `0.199, 0.159, 0.099, 0.071, 0.034` for `c/J = 4, 3, 2, 1.5, 1`, against
   the report's `0.2015, 0.1609, 0.1046, 0.0754, 0.0413`; the latter lie below the ceilings
   `ln λ − ln JSR_lower = 0.210, 0.170, 0.118, 0.090, 0.061`, so they are plausible, but the weight vector of the
   norm should be recorded to make them reproducible.  The qualitative claim (positive certificates inside the
   vacuous window) is confirmed.
8. **B.5**: "the Boltzmann bound is zero" refers to the exponent (at `h = 0` the finite-`n` bound is `ln 2`).
9. **§2.6, B.12 text**: for strongly coupled ferromagnets the finite-size values are far from `ε₁*`
   (`(J,h,c) = (2,−3,8)`: `5.26` per site at `n = 12` against `ε₁* = 1.74`); the table remark "`n = 10` is too
   short at `J = 1`" should be generalised.

### Theorem B.2 in detail (requested)

*Lower bound.*  `ln|A| ≥ I(Y;a(Y)) ≥ nR^{(n)}_ν(D_n) ≥ nR_ν(D_n)`, `D_n = e(ν) + (C+ε_n)/n`.  Uses
(L1) `R^{(n)} ≥ R = inf_n R^{(n)}` for a stationary source and a single-letter distortion (sub-additivity of
`nR^{(n)}` by product test channels; Gallager 1968, Thm 9.8.1) — hypotheses hold (`s` is site-additive);
(L2) right-continuity of `R_ν` at `e(ν)`: convexity for `e(ν) > 0`, Fano's inequality at `e(ν) = 0` — needs
`s₁ > 0` off the diagonal (`κ < 1`), which is assumed.  Holds for every `ε_n = o(n)`.

*Upper bound.*  (i) low shell `{gap ≤ θn}`: Chernoff count and the variational principle, `σ(θ) ↓ σ(0)` by upper
semicontinuity of the entropy, `σ(0) = sup{h(ν): e(ν) = 0} ≤ R*` because `R_ν(0) = h(ν)` — correct.
(ii) high shell: type covering on the block alphabet `σ^L` at level `Δ_P ≥ θL > 0` — the lemma
(Csiszár–Körner, Lemma 9.1 in the 2nd ed.) is uniform in the type and in the level for a fixed finite alphabet
and bounded distortion; `L` is fixed while `m → ∞`, and the level is bounded away from 0, so no delicate
uniformity is needed.  (iii) `R(P; s_L, LD) ≤ L·R_{ν_P}(D)` (Lemma C.1): re-derived, correct (conditioning on
the phase, independence of blocks, convexity twice).  The slope bound `|R'_ν| ≤ ln k/θ` on `[θ,∞)` and the
estimates `e(ν_P) ≤ (E_P G + ‖ψ‖)/L`, `gap_n ≥ m(E_P G − ‖ψ‖) − C'` are correct.  (iv) `(m+1)^{k^L}` types.
The construction covers within `gap_n(y)` itself, so the theorem holds for `ε = 0`.
Boundary energies cost `2‖ψ‖ ln k/(Lθ)`, which is why the order of limits is `L → ∞` first, then `θ → 0`.
Nothing is missing; what remains is that the proof is a paper proof resting on two cited lemmas.

---

## 3. Independent numerical checks (own code; sizes; result)

| script → output | what | result |
|---|---|---|
| `r1_vertices.py` | vertices of the Lipschitz polytope of `Q_n` = homomorphisms `Q_n → ℤ`: all bases for `n = 2, 3`; backtracking and recursive counts; 300 random LPs at `n = 4` | 6, 38, 990, 395 094; equal sets |
| `r2_B12.py` | tilted sandwich, all vertices, `n = 1…4` (11 200 cases, tilts incl. `θ*`, `0`, `±c`, `|θ| > c`), `n = 5` (36 cases); 10 000 non-vertex residuals | max deviation `4·10⁻¹⁴`; `0 ≤` width `≤ nε₁*`; no tilt beats `θ*`; `0.11367 / 0.12246 / 0.11383` at `θ*/c = −0.0372` |
| `r2b_dips.py` | exact fractional packing number of exactly sensitive dips at `θ*M` (`e/c = ½`, `β = 1`), `n = 100…800` | `ε₁ = ¼, ½, 0.8 ε₁*`: `3·10⁶`, `2151`, `10.8` at `n = 800`, local slopes `0.0163, 0.0076, 0.0016` → `R^rand = 0.0154, 0.0068, 0.0011`; `ε₁ = 1.1ε₁*`: `1.73, 1.60, 1.47, 1.34` (bounded, as B.12(a) requires) |
| `r2c_game.py` | game value `= G(θ)`; product-weight dip bound positive iff `ε₁ < G(θ)` | 1 000 random cases, relative error `10⁻⁹`, no mismatch |
| `r3_B1.py` | definition = droplet criterion = min-plus test = exact `N_cov = 1`; `τ_n`; random admissible residuals | 4 000 chains (1 981 sharp), 0 mismatches; `τ_n = 2h` for 12 parameter sets, `n = 2…10`, free and ring; antiferromagnet `2h−4|J|`; 175 Ising cases |
| `r4_B5.py` | B.5 on 4 000 random `(J,h,c)`; boundary; `ρ_pos`, `ρ₁`, `c_pos(h)`, Boltzmann values | no violation; all constants as in the report |
| `r4b_B6.py`, `r4d_boundary.py` | B.6(a): 150 LP instances; (b): 600 random `(x,z,q)`, words `≤ 14`, ring and free; boundary test | (a) 0 mismatches among 135 decisive; (b) 80 true / 520 false, first negative word alternating in all 520; boundary sharp |
| `r4c_ncov.py` | exact `N_cov` (ILP) and `N_frac`, free chains `n = 4…10`, ten parameter sets | table 3.1 reproduced exactly (`(1,¼,4.5)`, `n = 9`: 29 proved optimal) |
| `r5_B4.py`, `r5b_L12.py` | block brackets at `(1,0,4)`; one-shot ring values `n = 8, 10, 12` for 7 rows | `L = 6: [0.2111, 0.2672]`, `8: [0.2131, 0.2540]`, `10: [0.2143, 0.2465]`, `12: [0.21508, 0.24167]`; increments as in table 3.2 |
| `r6_B8.py`, `r6b_table25.py` | B.8 identities; pinned free energy; two-replica matrix; thresholds table; block formula; `s(β)`, `R_β` bound, `U_β` | all to `10⁻¹⁴` / to the printed digits (`U_β` at `βJ = 1` not converged at `n = 12`: increments `0.306, 0.282` against `0.2675`) |
| `r8_misc.py`, `r8b_jsr.py`, `r9_gridcover.py` | stable configurations; run-length-limited certificates; grid covers | 4096, 324, 92, 62; see MINOR-7; MINOR-4 |
| `r7a…r7w` | Conjecture B.13 | see MAJOR-1; standalone verification `r7w_standalone.py` (decimal, 60 digits, no numpy) |

Not saved to files before a container restart but recorded in `PROGRESS_NOTES.md`: the random classification
runs `r7c`, `r7g`, `r7h` (`n ≤ 4`), `r7j` and the `L = 6, 8, 10` brackets.

---

## 4. Literature

No web search could be run (budget exhausted).  Direct fetches:

* arXiv:2603.07435 (Krishnamachari 2026), abstract page and an automatic summary of the HTML: Gray's critical
  distortion of the symmetric binary Markov source with flip probability `p` is
  `D_c = ½(1 − (1 − (p/(1−p))²)^{1/2})`, cited to R. M. Gray, IEEE-IT 16(4) (1970) 412–421 and Jalali–Weissman
  (ISIT 2007, 571–575); its reference list also contains Gray, IEEE-IT 17(2) (1971) 127–134 and Berger,
  IEEE-IT 23(1) (1977) 52–59.  With `x = e^{−2Jt} = p/(1−p)` and `D = q/(1+q)` this is exactly B.6(b) at `h = 0`
  (`4D(1−D) ≤ x²`).  So the attribution to Gray and the formula quoted "from memory" are right.
* Hajek–Berger (Ann. Probab. 15 (1987) 1112–1125): the DOI `10.1214/aop/1176992084` resolves to the stated title
  and issue; the Project Euclid page and PDF returned no text (three attempts), JSTOR likewise.  I could not read
  abstract or text; the description in the report matches my recollection of the abstract (mod-2 decomposition
  with white noise; exact rate–distortion function below the noise weight) but this is **not verified**.
  Newman (ibid. 1126–1130): not fetched.  Whether the closed form with a field is in either paper is unknown.
* Not checked at all: Avram–Berger 1985, Kontorovich–Ramanan, Marton, Derrida–Hilhorst, Zuk–Kanter–Domany,
  Leinster; prior art for B.1, B.2, B.5, B.10–B.12 (the author's "not found" claims rest on seven searches and
  could not be re-run).

Novelty, as far as I can judge without searching: B.6 is known in substance (as the author says); B.8 is a
reformulation of standard objects; B.1, B.3, B.4, B.5 are short and routine but appear new as statements; B.2 is
a new statement proved with classical block coding; B.10–B.12 are new within this project, short, and B.12 is
now subsumed by Theorem 11.28(d) of the theory report (all alphabets), keeping the explicit chord-gap formula
as its own content.

---

## 5. Not checked

* Tightness half of Proposition B.3; rows 2–3 of Theorem B.9; Remark B.2″; the min-ratio-cycle formulation of
  `τ` for general (non-Ising) chains; the "exactly where the dip bound stops" claim for ferromagnetic chains.
* The analytic invariant-interval step of B.6(b); the primary texts of Hajek–Berger and Newman.
* The author's numerics on the structure of optimal weights (supports, Schmidt spectra), the transfer-operator
  values of `U_β` to 9 digits, the LP values of `R^rand` in the table of §2.5, the `n = 14, 16` rows of table 3.2,
  the finite-`n` game values of `f5/f6`.
* Theorem 11.24(b) of the theory report, on which B.10/B.12(b) rest, was taken as given (machine-checked there).
* Conjecture B.13 beyond the sizes in MAJOR-1: paths at `θ = 0` for `n ≥ 5` (only 16 000 models at `n = 5`),
  ferromagnetic chains with tilt for `n ≥ 6`; no proof of any of the surviving statements was attempted.
