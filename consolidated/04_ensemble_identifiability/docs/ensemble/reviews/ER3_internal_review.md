# ER3 — internal adversarial review of `ENSEMBLE_REPORT.md`, Part VI (§4c: E18–E21)

**Kind of review.**  Internal review by an independent AI session acting as an adversarial
referee.  It is not academic peer review.  Date: 2026-11-26.

**Object.**  Commit `8d42f60`, `docs/ensemble/ENSEMBLE_REPORT.md` lines 1267–1660 (§4c up to
§5): Theorem E18 with its table and Remarks 1–3, Proposition E18′, Theorem E19 (a)–(f), the
"Reading", Conjecture C3, Theorem E20, the sentence on `K = c + 1`, the torus Corollary,
Propositions E20′, E20″, E21 with Remarks 1–3, the paragraph on SCI-RES-0029, the table of
§4c.5; the Lean files `proofs/Ensemble/TwoStateCertificate.lean`, `PermanentCertificate.lean`
and four witnesses of `proofs/AxiomAudit.lean`; the scripts `lifted_checks.py`,
`kbody_capacity.py` and their stored outputs.  Line numbers are those of `8d42f60`.
The division kept working during the review and committed `527bf02` (follow-ups of ER2)
before it ended.  In `527bf02` §4c is byte-identical to `8d42f60` and sits at lines
1724–2117 (add 457 to the line numbers below); the two Lean files, `lifted_checks.py`,
`kbody_capacity.py`, the block L1–L7 of `output.txt` and the `kbody_capacity` blocks of
`output_threshold.txt` are unchanged (twenty lines of a new run for §4.2 were appended to
the latter).  This review and its scripts are not part of that commit.  E1, E10, E11(a)
were taken as given.

**Method.**  Every proof re-derived by hand.  Every statement attacked with my own code
(numpy/scipy; exhaustive where the size allows; the zeros of the projector certificate on
tori obtained from all complex solutions of the polynomial systems, not by minimisation).
Both Lean files and the four witnesses type-checked (`lake env lean`, exit 0, no output),
axioms printed, four instances of my own compiled.
Five sources read in the original text (§4).  `lifted_checks.py` and five of the nine
`kbody_capacity.py` runs re-run: identical to the stored outputs.

---

## 0. Bottom line

* **No CRITICAL finding.**  No numbered statement of Part VI is false.  No script found a
  counterexample to E18, E18′, E19(b)–(d), E20, E20′, E20″(a)–(c), E21(a)–(c).
* **Two MAJOR findings.**
  F1: the "count of double-point conditions" of Remark 3 to E21 (and of the table and O10) is
  false — three double points impose eight conditions on the nine-dimensional span, for every
  triple.  The conclusion drawn from it is true for another reason, and for *every* triple
  (proof and explicit twin below); the value `(3^r − 1)/(r+1)` it suggests is not the
  threshold (`r = 3`: six generic states are not identified; explicit twins in 10 of 10
  instances).
  F2: "for *every* flat-isolated support of 6 or 7 conformers that is not a face" is
  attributed to check L3, which samples nine supports and finds three.  The sentence is true:
  I verified it exhaustively (2 416 + 6 240 supports).
* **Nine MINOR findings** (F3–F11): numbers of E19(e),(f) that no script prints and one that
  my re-estimate moves (`152 → 149 ± 2`); what the Gaussian control does and does not show; a
  statement left as "computed instances" that is a theorem; constants of E20″ (one
  misleading sentence, one improvable order); prior art that makes E21 on finite product
  spaces weaker than a published theorem; an unstated hypothesis in E18(i); checks that
  check less than the text says; Lean coverage; wording.
* Beyond the review: the torus row of the table can be filled for `r = 2` (exactly 2 states)
  and, numerically, for `r = 3` (exactly 5 generic states) — §2 F1, F5 and §7.

---

## 1. Verdict per statement

| statement | verdict | what was checked; remarks |
|---|---|---|
| E18 | **correct with a correction** | Proof re-derived (real span: take real parts; `∫f_S dν = 0` forces the support; entries are affine in the data).  3 000 random finite instances (`q = 1, 2`; real and complex lifts): hypothesis holds in 1 393, LP confirms identification in 1 393.  Case (i) needs `v(x) ≠ 0` on `S`: F8 |
| E18, table | **correct** (rows 1–3) | Row 4 is a citation from memory; row 5 belongs to another division (the quoted sentence is in GEOMETRY-RES-0001, item 1; nothing else of that row checked) |
| E18 Remark 1 | **correct** | Every step re-derived (dependency ⇒ `|a| = |b| + |c|`; two patterns ⇒ a constant pair product; four equations ⇒ `±e_i`; three ⇒ one more).  Exhaustive, `n = 3…7` (4, 56, 560, 4 960, 41 664 triples): independent; at least three patterns; at most one extra sign vector, present exactly when three patterns occur (4, 48, 400, 2 880, 19 264 triples) and equal to minus the combination with the missing pattern as coefficients; `xxᵀ` independent on `Z_S`; LP: ensembles on the three, on any two and on the four points of `Z_S` identified (all triples for `n ≤ 6`; 1 953 through a fixed vertex for `n = 7`) |
| E18 Remarks 2, 3 | **correct** | Remark 2 holds for every positive semidefinite form in the lift that vanishes on `S`: its zero set contains `Z_S`, so the projector is the best one |
| E18′ | **correct** | Proof re-derived.  Exhaustive on the cube, `n = 4` and `n = 5`, every support of every size (by orbits), every competing support: no flat-isolated non-face has a twin with at most `K` atoms for random weights (`n = 5`: 49 orbits, 25 394 supports, three weight vectors each) and no flat-isolated face has one for any weights; where flat isolation fails, twins for all sampled weights; where affine independence fails, a twin on the same support.  1 500 random instances with non-injective integer features: same.  Injectivity of `Φ` off `S` is not needed |
| paragraph after E18′ | **true; the cited check does not establish it** | F2 |
| E19(a) | **quoted correctly** | Baldi–Vershynin read (§4).  Ranges of `t`, `m`, the probability, the lift with the constant coordinate, the passage to `z_j = x_1x_j` with `n − 1` variables: right.  The hypothesis on `t` is empty below `n ≈ 1 150` (`d = 1`), `2 340` (`d = 2`): the numerics at `n ≤ 12` are independent evidence, not instances |
| E19(b) | **correct**, given (a) | The entries of `ξ_dξ_dᵀ` are exactly the `x_A`, `|A|` even `≤ 2d` |
| E19(c) | **correct**, given (a) | `ξ_2 = (1, Φ)`; lift isolation = flat isolation.  `n = 12`: lift-isolated with frequency `1.000, 1.000, 1.000, 0.993, 0.960` at `K = 24, 33, 49, 54, 66` (300 supports each; the report: `…, 0.995, 0.955`); exact arithmetic modulo a prime agrees with the floating-point test on 600 supports.  `n = 6`, `K = 13, 14` (eight flat-isolated supports, random weights): of 3 200 sampled vertices of the fibre polytope none but the ensemble itself has `≤ K` atoms (fewest: `K + 1`) |
| E19(d) | **correct** | Flip difference, `D_odd`, strictness on the event "no two of `±S` adjacent": right.  Cover's bound holds for points in arbitrary position (central arrangements; brute force over all labellings of 15 point sets of the kind used in (d): the count is below the bound by at least 138 in each).  Labels `−x_v` are independent of the points if the conformers are uniform in `{±1}ⁿ` (or `v ≠ 1` in the normalised form) |
| E19(e) | **[N]; decisions sound; numbers** | Cutting-plane decision against two certificates of my own: 765 supports, no disagreement (§6).  Numbers: F3 |
| E19(f) | **[N]; fair as a same-size comparison** | F3, F4 |
| Reading, C3 | conjecture; **evidence overstated** | F4, F11 |
| E20 | **correct**, given the lemma | Chiantini–Coppens read (§4); induction step re-derived.  Wording: F11 |
| "At `K = c + 1` …" | **correct** as a conditional | The hypothesis is automatic for `r = 3` and fails on a set of positive measure for `r = 4`: F5 |
| torus Corollary | **correct**; one part understated | `r = 3`: `K = 4`: `det M(z₃)` has degree 4 and its roots are the four given `z₃` (2 000 tuples); `K = 5`: six solutions, all on the torus, in 5 000 of 5 000 tuples, sixth point with `||z_k| − 1| ≤ 2·10⁻¹¹`; `K = 6`: a curve.  `r = 4`: `K = 10, 11`: no zero but the states (12 tuples each); `K = 12`: 24 complex solutions, 16 to 24 on the torus; `K = 13`: a curve.  F5 |
| E20′ | **correct** | Zero set; `|D| = 1` (first Fourier coefficient in the open disc).  LP on a `12³` grid: pairs differing in 2 or 3 angles identified by the products over at most two angles (24/24), in one angle not identified by all 26 (12/12, non-neighbouring values) |
| E20″(a) | **correct**; constant conservative | Both cases and the passage to `E` re-derived.  No violation in 129 pairs on dense grids and 300 pairs with shared angles, gaps down to `10⁻³` rad (`β` down to `10⁻⁶`).  F6 |
| E20″(b) | **correct** | Expansion and `Λ` checked (`Λ = 17.5…65.8` against the stated `38.6…115.9`).  LP on refined grids: `sup ∫min(d²)dν` is `0.14` to `0.42` of `Λτ/c*` |
| E20″(c) | **correct**; order not optimal | LP: `sup|ν(N_q) − w_q|` is `0.003` to `0.06` of the bound and linear in `τ`: F6 |
| "What this adds" | one sentence **misleading** | F6 |
| E21(a), (b) | **correct** | `{0..q−1}^r`, 14 cases with `q ≤ 4`, `r ≤ 6`, `K ≤ 4` (12 exhaustive, 2 sampled; about 275 000 families): permanent zero ⇔ deficient set, always; Hall ⇒ zero set = states, always; predicted sub-product in the zero set, always |
| E21(c) | **correct** | The distinct representatives exist (Hall applied to `J ∪ {i}` gives `≥ |J| + 1` coordinates): confirmed in every Hall family of the exhaustive runs; `g_i` uses `K − 1` distinct angles.  Torus, pairs sharing angles but Hall holding: no zero off the states (8 families, `90³` grid and polishing) |
| E21, numerical paragraph | numbers **reproduced** | `30 720 / 10 944 / 960` also follow by counting: a triple fails iff it contains an edge of the 6-cube (`192·62 − 960`), and has an extra zero iff it lies in a square (`15·16·4`) |
| E21 Remarks 1, 2 | **correct** | Remark 2 is weaker than a published theorem: F7 |
| E21 Remark 3 | first two sentences **correct**; third: **false count, true conclusion** | F1 |
| SCI-RES-0029 paragraph | **accurate** | The document was read on `origin/research/scientific-translation`: its §3 (a), (b), (c) say what the paragraph says ("rank 9", "the referee is asked to decide it by a linear programme") |
| table §4c.5 | rows 1–3 consistent with the text; torus row: F1, F5 | Last sentence ("strictly larger"): for the torus with `r = 2, 3` the two ranges coincide (F1) |

---

## 2. Findings

### F1 — MAJOR.  Remark 3 to E21, the torus row of §4c.5, Problem O10: the count of double-point conditions is false; the conclusion holds for another reason, and for every triple

**Where.**  Lines 1625–1627: "for three states that differ in two angles only, the count of
conditions (**three double points impose nine conditions on the nine-dimensional span**)
indicates that it fails generically".  Line 1650: "not known (a count of double-point
conditions suggests `(3^r − 1)/(r+1)`)".  §9 O10: "or to the count `⌊(3^r − 1)/(r+1)⌋`".

**Why.**
1. *The nine conditions are never independent.*  For three points of `𝕋²` take `u ≠ 0`
   orthogonal to the three lifted vectors in `ℂ⁴`.  `g = |⟨u, v(φ)⟩|²` is in the span, is not
   zero, is non-negative and vanishes at the three points, so its gradient vanishes there
   too.  The `9 × 9` matrix (value and gradient of the nine products at three points) has
   rank at most 8.  Example: states `(0.3, 1.1), (1.7, 2.9), (4.0, 5.2)`: singular values
   `2.37, 2.04, 2.01, 1.76, 1.50, 1.40, 1.33, 1.03, 0.00`.  2 000 random triples: smallest
   relative singular value `≤ 1.5·10⁻¹⁶`, second smallest `≥ 8·10⁻⁶`.  The same objection applies to every `K < 2^r`
   on `𝕋^r` (all `|⟨u, v⟩|²` with `u` orthogonal to the lifted states).  Read with the right
   rank, the count would "indicate" that a certificate exists — the opposite conclusion.
2. *The conclusion is true, for every triple, by a different argument.*  If two of the
   states share an angle, E20′ (`|D| = 1`) applies to that pair.  Otherwise let
   `B = u₀ + u₁z₁ + u₂z₂ + u₃z₁z₂` be the bilinear form through the three states.  Every `ν`
   with the data of `μ` has `∫|B|²dν = 0`, so it lives on `Γ = {B = 0} ∩ 𝕋²`.  `B` is not a
   product (the zero set of a product contains no three points pairwise different in both
   angles), so `Γ` is the graph of a Möbius map `z₂ = M(z₁)`; `M` maps three points of the
   unit circle into it, hence the circle onto itself, and after `z₂ ↦ z̄₂` if necessary
   `M(z) = c(z − a)/(1 − āz)`, `|a| < 1`.  On `Γ`, with `z₁ = e^{iθ}`,
   `z₂ = c(z₁ − 2a + a²z̄₁)/|z₁ − a|²`, so each of the nine products is `T(θ)/|e^{iθ} − a|²`
   with `T` a trigonometric polynomial of degree at most 2.  Hence `ν` has the data of `μ`
   as soon as `ν/|e^{iθ} − a|²` and `μ/|e^{iθ} − a|²` have the same Fourier coefficients of
   order `≤ 2`.  A positive measure with three atoms has a positive definite `3 × 3` Toeplitz
   matrix, hence infinitely many such partners (Carathéodory–Toeplitz).  **No ensemble with
   three states on `𝕋²` is determined by the bilinear data; so no three states that differ
   in two angles only, on any `𝕋^r`.**
   *Explicit twin.*  The uniform ensembles on `{(0,0), (2π/3, 2π/3), (4π/3, 4π/3)}` and on
   `{(π/3, π/3), (π, π), (5π/3, 5π/3)}` have the same data (`E cos φ₁cos φ₂ =
   E sin φ₁sin φ₂ = ½`, the other six non-constant means `0`; here `B = z₂ − z₁`; the three
   states differ pairwise in both angles).  Random triples: an LP over
   measures on 3 000 points of `Γ` finds a twin with *all* its mass off the three states and
   the same nine data to `4·10⁻¹⁵`, in 20 of 20 triples.
3. *`(3^r − 1)/(r+1)` is not the threshold.*  `r = 3` (value `6.5`): six generic states are
   **not** identified.  Any twin lives on the zero set of the projector certificate, a real
   curve; an LP over measures on about 11 000 points of the curve finds an ensemble with
   mass `0.43` to `1.00` farther than `0.05` rad from every state and the same 26 data to
   `8·10⁻¹⁵`, in 10 of 10 random instances.  The count that does work is on the curve: the 27
   products span 12 functions there (computed: 12 in all ten instances; sections of a line
   bundle of degree 12 on a curve of genus one), and six double zeros are 12 conditions.
   With F5 (five generic states are identified) the largest identified number of generic
   states on `𝕋³` is `5 = 2^r − r`.  `r = 4` (value 16): at `K = 13` an explicit twin in 2 of
   4 instances; in the other 2 none with exact data on the discretised curve, but 2 to 6 %
   of the mass can sit far from the states under a data change of `10⁻⁶` — not settled (§7).

**Correction.**  Remark 3: replace the parenthesis by argument 2 ("…are never identified:
every measure with the same data lives on the circle where the bilinear form through the
three states vanishes, and there the data are the trigonometric moments of order `≤ 2` of a
weighted measure").  Table, torus row: "identified up to": `2` for `r = 2` (proved); `5` for
`r = 3` (F5); "not identified beyond": `2` for `r = 2` (proved), `5` for `r = 3` **[N]**;
delete the count or say that it is not valid.  O10: for `r = 2, 3` the answer is `2^r − r`.
The closing sentence of §4c.5 ("In every row where both are known, the identified range is
strictly larger than the range of the natural certificate") then has two rows in which
the ranges coincide, if E18(ii) is counted as the natural certificate.

**A warning for future checks.**  A product grid cannot test non-identification here: three
states of a `24 × 24` grid are "identified" among measures on the grid in 38 of 40 cases,
because the grid has no other point on `Γ`.  Likewise two states that differ in one angle
by *one* grid step are identified on a grid (the chord is an edge of the polygon; 4 of 4).

### F2 — MAJOR.  "for every flat-isolated support of 6 or 7 conformers that is not a face" is attributed to a check that samples nine supports

**Where.**  Lines 1353–1356: "on the cube with five sites, **for every** flat-isolated
support of 6 or 7 conformers that is not a face there are *some* weights for which another
ensemble with as many conformers has the same pair data **(L3)**".  Lines 1424–1426: "L3:
`n = 5`, exhaustive over all supports of the same size".  Docstring of `lifted_checks.py`:
"L3 Cube n = 5 …, exhaustive".

**Why.**  `test_L3` draws five supports with `K = 6` and four with `K = 7`
(`for K, trials in ((6, 5), (7, 4))`); three of the nine are flat-isolated non-faces.
"Exhaustive" is true of the competing supports `S′` only.  Stored output: "3 supports
flat-isolated but not faces …, 6 faces; … SOME weights …: 3 of 3".

**The sentence is true.**  Exhaustive (`er3_e18prime.py`; every support, every `S′`):

| `n = 5`, `K` | supports | affinely dependent | not flat-isolated | flat-isolated faces | flat-isolated non-faces | of these, twin with `≤ K` atoms for: random `w` / uniform `w` / some `w > 0` |
|---|---|---|---|---|---|---|
| 4 | 1 820 | 0 | 0 | 1 780 | 40 | 0 / 40 / 40 |
| 5 | 4 368 | 0 | 0 | 3 872 | 496 | 0 / 480 / 496 |
| 6 | 8 008 | 0 | 0 | 5 592 | 2 416 | 0 / 2 400 / **2 416** |
| 7 | 11 440 | 0 | 160 | 5 040 | 6 240 | 0 / 6 240 / **6 240** |
| 8 | 12 870 | 20 | 1 280 | 2 440 | 9 130 | 0 / 9 130 / 9 130 |
| 9 | 11 440 | 160 | 4 880 | 400 | 6 000 | 0 / 6 000 / 6 000 |
| 10 | 8 008 | 600 | 6 320 | 16 | 1 072 | 0 / 1 072 / 1 072 |

(`K = 2, 3`: all supports are faces.  `n = 4`: `K = 4, 5, 6`: 2, 8, 12 flat-isolated
non-faces, all with a twin for the uniform weights.  No flat-isolated *face* has a twin for
any weights, as it must be.)

**Also.**  The explanation "at that size `K` is more than half the number of observables"
(and O9: "at `n = 5`, where `K > m/2`, exceptional weights exist") does not account for the
table: at `K = 4, 5 ≤ m/2` every flat-isolated non-face has exceptional weights as well
(`K = 4`: the Hadamard quadruple of E9(b) on four sites, the fifth site equal up to sign to
one of them — e.g. `+++++, +++−−, ++−+−, ++−−+`; uniform weights; the twin is the quadruple
of the other parity, `++++−, +++−+, ++−++, ++−−−`).

**Correction.**  Quote the exhaustive numbers; in the docstring and in the text say that
L3 samples; replace the explanation by "in every case computed (`n = 4, 5`, every `K`)
each flat-isolated non-face has exceptional weights".

### F3 — MINOR.  E19(e),(f): the quoted thresholds and ratios are printed by no script; trial counts and errors are not stated; one number moves

**Where.**  Lines 1391–1400: "about `76`, `152`, `233`"; "`78`, `142`, `214`"; "ratios `0.97`,
`1.07`, `1.09`"; "near `K = 11` … `13` … `11.5` against `16`"; and "2.6 to 3.5".

**Why.**  `kbody_capacity.py` prints frequencies on a grid of `K` (40, 20, 20 supports per `K`
for the cube; 40, 20, 12 for the control, **one** Gaussian cloud per run).  The thresholds
are interpolations made by hand; the method is not stated.  Linear interpolation of the
stored lines gives `76.4, 154.0, 234.3` and `78.8, 142.2, 214.0` (ratios `0.970, 1.083,
1.095`).  With more supports (`er3_kbody.py`; my own full LP):

| | cube, frequency ½ at | Gaussian (several clouds) | ratio |
|---|---|---|---|
| `n = 8` | `76.2` (95 %: `75.4…76.9`; 200 per `K`) | `78.0` (`77.5…78.6`; 10 clouds; single clouds `75.7…80.3`) | `0.976` |
| `n = 10` | **`148.9`** (`147.4…151.0`; 80 per `K`) | `143.2` (`141.3…144.9`; 6 clouds; single clouds `140.4…147.0`) | **`1.040`** (`1.02…1.07`) |

`n = 12`, cube: an independent replicate with the division's own `is_face` on my supports
gives faces in `16/16, 11/16, 2/16` at `K = 228, 234, 240` (frequency ½ near `236`); with the
stored line (`234.3` by interpolation) the quoted `233` is within the error, about `±3`.
The Gaussian run at `n = 12` was not repeated; theory gives `215.2` (F4).  All other
numbers of §4c are in the stored outputs (list in §6).

Also: "the **bounds** `84, 186, 352` of (d)" are the values `2D_odd`, not bounds at these
sizes — the stored output has frequency `0.025` at `K = 85` (`n = 8`), mine `0.015` at 86 and
`0.005` at 88; (d) bounds a probability, by about `½` at `K = 2D_odd`, and its second term
exceeds one there.

**Correction.**  State trials and the interpolation; "about 76, 149, 235 (±1, ±2, ±3)";
"ratios 0.98, 1.04, 1.09"; "the values `2D_odd = 84, 186, 352` of (d)".

### F4 — MINOR.  The Gaussian control is the Donoho–Tanner curve; what it supports

**Where.**  E19(f), the "Reading" (lines 1432–1439), Conjecture C3 (lines 1444–1446).

**Why.**
1. *The control agrees with theory and need not be simulated.*  The weak threshold
   `ρ_W^+(δ)`, `δ = D/N`, computed from the statistical dimension of the descent cone
   (`er3_dt_curve.py`; it returns `0.5582` at `δ = ½`, Donoho–Tanner: `.5581`), gives
   `76.4, 142.0, 215.2` for the three four-body sizes (control: `78, 142, 214`) and
   `10.9, 11.5` for pair data at `n = 12, 14` (control: `11, 11.5`).
2. *The asymptote quoted is not the value at these sizes.*  `δ = 0.77, 0.50, 0.27`;
   `D/(2 ln(N/D)) = 183, 183, 217`; `n³/(48 ln 2) = 52` at `n = 12`.  For pair data
   `n/(4 ln 2)` is reached slowly: the Gaussian threshold is `0.91n, 0.82n, 0.67n, 0.51n,
   0.42n, 0.38n` at `n = 12, 14, 20, 40, 100, 400`.
3. *"Growing with `n`" at `n ≤ 12` is not evidence for the order.*  The Gaussian cloud
   itself has threshold / lift dimension `= 2.63, 3.09, 3.21` at `n = 8, 10, 12`, then
   `3.20, 3.22` at `n = 16, 20` and only then grows (`3.6, 4.1, 5.2` at `n = 30, 40, 60`).
4. *"Threefold" mixes an asymptote with finite sizes.*  At the sizes computed the cube
   exceeds the Gaussian cloud by `1.2` (`n = 12`) and `1.4` (`n = 14`) for pair data; the
   data say that the cube departs from a Gaussian cloud as `δ` decreases, which is the
   regime of C3.
5. "**This is a gap** between *identifiable* and *certifiable by the natural certificate*
   **that is not a constant**" (line 1436) states C3 as a fact.  The table of §4c.5 has the
   right wording ("may differ in order").

**Correction.**  Cite the curve `ρ_W^+(D/N)` as the reference and say that the control
reproduces it; write "may not be a constant (Conjecture C3)"; replace "threefold" by the
measured ratios and the asymptotic extrapolation, named as such.  The comparison itself is
fair (same `N`, same `D`, same linear programme); its limits are one cloud per run and 12
to 40 supports per `K`.

### F5 — MINOR.  `K = c + 1` on tori: for `r = 3` the hypothesis of E18(ii) is automatic (a theorem, not "computed instances"); for `r = 4` it fails on a set of positive measure

**Where.**  Lines 1479–1482: "**in the instances computed** the six rank-one matrices are
independent, so those ensembles are identified as well (**[N]**, L4)"; table: "and, in
computed instances, `r = 3`"; line 1468: "meets `𝒱` in `deg 𝒱` points".

**Why.**
1. L4 computes **one** instance with `r = 3`, `K = 5`.
2. *It is a theorem.*  Let `v₁, …, v_K` be independent and `v_{K+1} = Σ a_i v_i` with at
   least two `a_i ≠ 0`.  If `Σ h_i v_i v_i^* = 0`, the coefficient of `v_i v_j^*` (`i ≠ j ≤ K`)
   is `h_{K+1} a_i ā_j`, so `h_{K+1} = 0`, then all `h_i = 0`.  For `r = 3` the secant
   4-plane of five general points is a general 4-plane (the span map `𝒱⁵ ⇢ G(4, 7)` is
   dominant, both sides have dimension 15), so it meets the Segre threefold in `6 = deg`
   distinct points; the sixth is fixed by the involution, so it is on the torus (this part
   of the text is right), and it is not proportional to one of the five.  Hence **every
   generic ensemble of five states on `𝕋³` is identified**.  Adversarial search for a
   five-point configuration with dependent matrices: the smallest singular value tends to
   zero only where the sixth point runs into one of the five (`5.6·10⁻⁸` at distance
   `10⁻⁷`), and there `Z_S = S`.  Two states differing in one angle: the certificate
   vanishes on a curve, as it must.
3. *`r = 4`, `K = 12`.*  The 24 solutions satisfy the Euler–Jacobi identity
   `Σ g(x_i)/J(x_i) = 0` for all `g` of degree `≤ 2` in each variable (checked to `10⁻¹¹`),
   which is one linear relation among the 24 matrices `v v^*` when all 24 points are on
   the torus.  In 37 random instances the number on the torus was `16, 18, 20, 22, 24` in
   `1, 15, 12, 7, 2`; with fewer than 24 the matrices are independent (smallest singular
   value `≥ 10⁻³`), with 24 they are dependent (`3·10⁻¹⁴`) and E18(ii) does not apply.  In
   these two and in three further instances with 24 the ensemble is identified all the
   same: the relation is unique and has both signs on the twelve extra zeros (`4+/8−`,
   `6+/6−`, `4+/8−`, `9+/3−`, `7+/5−`; LP on the 24 zeros in the last three: mass 0 off the
   states).  What is needed in E18 is only that no relation is non-negative off `S` —
   Theorem E1(a) on the finite set `Z_S`.
4. "`deg 𝒱` points": counted with multiplicity.

**Correction.**  State the `r = 3` case as a proposition with the two-line proof; in E18
add "more generally it suffices that no `h ≠ 0` on `Z_S` with `Σ h(x)v(x)v(x)^* = 0` is
non-negative off `S`"; table: "`2^r − r` for `r = 2, 3`; for `r = 4` in 40 computed instances
(35 by E18(ii), 5 by the weaker criterion)".

### F6 — MINOR.  E20″: the constant, the sentence on its sharpness, the order of (c)

**Where.**  Lines 1515, 1525–1526, 1556–1560.

**Why.**
1. `c_D ≤ 1` always (`β ≤ 4`), so `c* = min(1, c_D) = c_D`: the minimum with 1 is idle.
2. "the smallest value found … is `1.25` — the constant of (a) is **within a quarter of the
   best possible** in the worst case found".  With shared angles
   `inf f/min(d²) = min(1, c_true^D)` exactly (move only a shared angle), so the ratio is
   `1/c_D` as soon as `c_true^D ≥ 1`.  The `1.25` is that: the pair of L6 with `r = 5`, two
   shared angles, `|D| = 3`, `β_min = 3.21` (`1/c* = 1.246`; `er3_l6_trace.py`).  It says
   nothing about the differing angles.  There: `|D| = 2`: `c_true/c_D ∈ [2.000, 4.0]` on 109
   pairs (2 in the limit of one small gap, 4 for antipodal states); `|D| = 3`:
   `≥ 2.13`, and `8·10⁴` for gaps `(0.01, π, π)`, `8·10⁶` for `(0.001, π, π)` — `c_D =
   min β_k/4` collapses when *one* differing angle nearly coincides, the certificate does
   not (`c_true ≈ 2`).  From the two cases of the proof, for any two differing angles:
   `F ≥ min(min(θ_k, θ_l), θ_kθ_l/(4|D|))·min(A, B)`; so
   `c_D′ = max(min_k β_k/4, β_(1)β_(2)/(64|D|))` (the two largest `β`) is also valid
   (checked on grids: `c_true/c_D′ ≥ 2.1`).
3. L6 skips 14 of its 60 pairs (`β_min < 0.05`); the text says "46 random pairs" without
   the exclusion.  My runs include gaps down to `10⁻³`: no violation.
4. *(c) is of order `√τ`; the truth is of order `τ`.*  For two differing angles `k ≠ l` put
   `h = 1 − (1 − a_k/β_k)(1 − a_l/β_l)`: in the span, `h(p) = 0`, `h(q) = 1`, both critical.
   `|h − 1| ≤ 8d_q²/(β_kβ_l)` and `|h| ≤ (β_k + β_l + 4)d_p²/(β_kβ_l)` everywhere, so
   `|ν(N_q) − w_q| ≤ 12ε/(β_kβ_l) + [2√2(1/β_k + 1/β_l) + (8 + 8√2)/(β_kβ_l)]τ`, linear in
   `τ`.  LP (five configurations, `τ = 10⁻⁴…10⁻²`): the true deviation is linear in `τ`
   (`4.7·10⁻⁴, 4.7·10⁻³, 4.0·10⁻²` in one case), below both bounds; the bound of (c) is
   16 to 330 times larger and is vacuous (`≥ 1`) at `τ = 10⁻²` in all five.

**Correction.**  Drop `min(1, ·)` or say why it is kept; replace the sentence by "the
constant is attained only in the direction of the shared angles; for the differing angles
it is conservative by a factor 2 to 4 (`|D| = 2`)"; state the exclusion in L6; optionally
add `c_D′` and the linear bound for the weights.

### F7 — MINOR.  E21 on finite product spaces is weaker than a published theorem; E9(a) and E19 lack the deterministic counterpart

**Where.**  Remark 2 to E21 (lines 1618–1621); novelty class "elementary …; not searched".

**Why.**  Kahle, "Neighborliness of marginal polytopes" (2010), Theorem 13 (read, §4): the
marginal polytope of a hierarchical model whose smallest non-face has `g` elements is
`(2^{g−1} − 1)`-neighbourly, for any finite alphabets.  With all margins of order `≤ t`:
**every** ensemble with at most `2^t − 1` atoms on a finite product space is determined by
the data of order `t` — no Hall condition.  E21 with data of order `K` reaches `K` states
under a condition.  Checked: on `{0,1}⁴`, order 3: all 11 440 sets of 7 states are simplicial
faces (the 8 even states of a 4-cube are not); 352 of the 560 triples violate the Hall
condition and are identified all the same.  For the report's own setting (even correlations
of order `≤ 2d` modulo the flip = all correlations of order `≤ 2d` in `z`): any
`2^{2d} − 1` conformers are identified — `3` for pair data (this is E9(a)), `15` for two- and
four-body data (300 random 15-sets each at `n = 6, 7, 8`: all faces; an explicit 16-set is
not).

**Correction.**  Cite the theorem in Remark 2 ("on a cube or any finite product space the
existence of such an energy is known for any `2^K − 1` states; what E21 adds there is an
explicit formula; on a torus the neighbourliness fails already for two states, E20′") and
next to E9(a)/E19 as the worst-case capacity `2^{2d} − 1`.

### F8 — MINOR.  E18(i) needs `v(x) ≠ 0` on `S`; "linearly independent" can be "affinely independent"

**Where.**  Lines 1292–1294, 1304–1306: "compress …: `h_{x₀} v(x₀)v(x₀)^* = 0`".

**Why.**  The last step gives `h_{x₀} = 0` only if `v(x₀) ≠ 0`.  `X = {x₀, x₀′, x₁}`,
`v = 0, 0, 1`, observable `|v|²`, `S = {x₀, x₀′}`: `f_S = |v|²` has zero set `S`, the column
spaces `{0}, {0}` have a direct sum, the two matrices are equal, and `δ_{x₀}`, `δ_{x₀′}`
have the same data.  No lift used in the report has a zero.  In the main statement
linear independence of the `v v^*` can be weakened to linear independence of the
`(1, v v^*)` (the total mass is known): in 167 of 1 607 random instances with linearly
dependent matrices the ensemble was identified.

**Correction.**  "…and `v(x) ≠ 0`, `x ∈ S`"; optionally "affinely independent".

### F9 — MINOR.  Checks that check less than the text says; no vacuous `or True`

* **L3**: F2.  **L6**: F6 (3); its grid (`2π/30 = 0.21`) cannot resolve the extremal
  measures at `τ = 10⁻³` (scale `√τ`): with grids refined to `10⁻³` around the states the
  ratio to the bound is up to `0.42`, not `0.30`.
* **L4(b)**: "the instances computed" is one instance per `(r, K)`.  **L7(a)** only tests
  families that differ pairwise in *every* angle, where the Hall condition is trivial (my
  runs include families at its boundary).
* **L4(a), grid test**: `ok &= not res` for a random pair that differs in one angle would
  *fail* if the two values were neighbours on the grid (F1, warning) — a false alarm, not
  a false pass; it did not occur with the stored seed.
* **L5**: `assert … set(Zs) == set(Zs2)` compares a computation with its negative and
  cannot fail.  The assertion that matters (`worst_extra ≤ 1 and dependent == 0`) is real.
* **L1**: tolerance `10⁻⁷` on the distance from the span; the smallest non-zero distance I
  met at `n = 12`, `K = 66` is `2·10⁻⁶`.  Exact arithmetic agrees on 600 supports; an
  exact test costs nothing.
* **`kbody_capacity.is_face`**: sound in the direction "face" (the energies of all states
  are checked).  In the direction "not a face" it relies on the optimum of a relaxation
  being `≤ 10⁻⁷` under `|y|_∞ ≤ 1`; the margins of my own (feasible, not optimised)
  certificates for the faces are `≥ 10⁻²`, once `2·10⁻⁴`.  One line is not sound:
  `res.status != 0` is counted as "not a face" instead of "undecided" (it never happened
  in about 1 400 LPs).
* I found no assertion ending in `or True` and no tolerance through which a false
  statement of Part VI would pass.

### F10 — MINOR.  Lean: what "(a) and (b) are **[V]**" covers

`permCert_zero_set` is the first sentence of (b).  The clause "for instance if any two
states differ in at least `K` coordinates" and the second sentence ("If the condition
fails for some `I` …") are not formalised (both are immediate from
`permCert_eq_zero_iff`).  Say "(a) and the first sentence of (b)".  Details in §3.

### F11 — MINOR.  Wording

* Line 1430: "with a prior on the number of conformers and generic weights, data of order
  `d` already reach `n^d/d!`" — for even `d` (for odd `d` the lift `ξ_d` needs order
  `d + 1`); only `d = 2` is proved in the text.
* Line 1273: "an *exact* statement of what a prior on the number of conformers adds" —
  E18′ is a sufficient condition for generic weights.
* E19(a): `C` is both the constant and the binomial sum.
* E20, proof: "the exceptional set of the lemma is a proper closed subset" — it is
  *contained in* one; `[v]` is defined where `v ≠ 0`.
* Line 1434: "equal within a few per cent" — 2 %, 4 %, 9 % (F3).

---

## 3. Lean statements against the report

Both files type-check with no output; every declaration below depends on `propext`,
`Classical.choice`, `Quot.sound` only; no `sorry`.  The four witnesses of
`proofs/AxiomAudit.lean` (extracted from `8d42f60`) compile.

| declaration | matches the report? |
|---|---|
| `twoStateCert_eq_zero_iff` | Yes: the core of E20′ as described (non-negative `a`, `b`, never zero together, every index has another one).  `ι` is the set `D`; the terms over `E`, the trigonometry and the passage to identification are on paper, as the report says.  Not vacuous for `|ι| ≥ 2`; for empty `ι` both sides are true |
| `twoStateCert_nonneg`, `twoStateCert_unique_eq_zero` | Yes.  The second says that the *formula* is zero on one coordinate; non-identification for `|D| = 1` is on paper (the docstring of the Lean file suggests more than the theorem; the report does not) |
| `twoStateCert_growth_three` | Yes: E20″(a) on `D`, `|D| ≥ 3`, with `c ≤ θ_k` for all `k`.  Needs no sign of `θ` |
| `twoStateCert_growth_two` | Yes: `|D| = 2`, `c(θ₀ + θ₁) ≤ θ₀θ₁`, `θ > 0` |
| `permCert_nonneg`, `permCert_eq_zero_iff` | Yes: E21(a).  `offSet a i` is the set of coordinates with `a i k ≠ 0` |
| `permCert_zero_set` | Yes for the first sentence of (b), one coordinate type.  F10.  With more states than coordinates the hypothesis cannot hold and `permCert` is identically zero (my example, `Fin 3 → Fin 2`) — consistent, worth a line in the text |
| `ensemble_two_state_certificate_witness`, `…_growth_three_witness`, `ensemble_perm_certificate_witness` | Real instances; all hypotheses discharged.  The permanent witness shows one direction (non-zero at a chimera) |
| `ensemble_two_state_growth_two_witness` | A real instance of the abstract statement, but not a torus configuration: `θ = 1` means antipodal states, for which `a_k + b_k = 4`; `a = (1, 0)`, `b = (0, 1)` does not satisfy that.  A torus instance compiles: `a = (0, 4)`, `b = (4, 0)`, `θ = (1, 1)`, `c = ½` (`er3_lean_checks.lean`) |

My third instance: `permCert_zero_set` for three states `(0,0,0), (0,1,1), (1,0,2)` over
`Fin 3` that share coordinate values pairwise (so "any two differ in `K` coordinates"
fails) with the Hall condition discharged by `decide`.

Not machine-checked, as the report says: E18, E18′, E19, E20, the terms over `E`,
E20″(b),(c), E21(c).

---

## 4. Citations

| source | how read | verdict |
|---|---|---|
| Baldi–Vershynin, arXiv 1803.10868v3, Theorems 4.1, 4.2, Definition 3.1, Lemma 2.2 | **statements read** (PDF of v3, text extracted) | Quoted correctly in E19(a): `dn^{0.02} ≤ t ≤ 0.001n`; `m < C(n − Cn/log n − t, ≤d)`; probability "larger than `1 − 2^{−t/4}`"; `x^{≤d}` indexed by subsets of size `≤ d`, the empty one included (example `(1, x₁, x₂, x₃, x₁x₂, x₁x₃, x₂x₃)`); 4.1 = [ASW, Theorem 4.5], `m < C(n − log C(n,≤d) − t, ≤d)`, probability `1 − 2^{−t}`.  4.2 does not assert independence; the report adds 4.1, rightly.  "Whose range of `K` is larger" needs `log C(n,≤d) ≤ Cn/log n`, true in the range of 4.2 (`d ≤ 0.001n^{0.98}`) for `C ≥ 1`.  The translation to `z ∈ {±1}^{n−1}` is right.  Lemma 2.2(4) is the bound for central arrangements without general position used in E19(d).  Proofs not read |
| Chiantini–Coppens, arXiv math/0005202v1, Corollary 1.3 | **statement read** (PDF) | "If `k < r − n` and `π ∈ G_k(X)` is general, then `π ∩ X` is formed by exactly `k + 1` points."  Over `ℂ` ("We work over the complex field"); `X` irreducible ("since `X` is"); non-degenerate is in the introduction, not restated in §1; singular `X` allowed.  General `π ∈ G_k(X)` ⇔ general `(k+1)`-tuple (the span map is dominant onto `G_k(X)`).  Applicable as used: closure of the image of an irreducible variety, spanning; real points of the torus are Zariski dense.  The two-line proof (induction by projection from a general point of `X`, from the trisecant lemma) re-derived |
| Donoho–Tanner, arXiv math/0607364v2, Theorems 1.2, 1.6, §1.3 | **statements read** (PDF) | `ρ_W^+(δ) ∼ |2 log δ|^{−1}`, `δ → 0`; valid when `N/n → ∞`, `log N / n → 0` (true for the cube's sizes: `log N ∼ n`, `D ∼ n^{2d}`).  So "`K ≈ D/(2 ln(N/D))` for `D ≪ N`" is the right statement and constant for the simplex.  Theorem 1.6 as stated gives the half "below the threshold faces survive"; I did not find the converse stated outside proportional growth.  At the report's sizes the asymptote is not the relevant value (F4) |
| Cover 1965 | **read in the original** (scan on the author's archive page, OCR text) | Theorem 1: `C(N, d) = 2Σ_{k<d} C(N−1, k)` for points in general position; §III treats polynomial surfaces and states the inequality for the vertices of the cube ("with inequality instead of equality because the `2^m` vertices … are not in general position").  Used correctly in (d).  (d) is the paper's own "separating capacity = twice the number of degrees of freedom" for polynomial threshold functions |
| Kahle, arXiv 0809.0786v1, Theorem 13 | **statement read** (PDF) | "(2^t − 1)-neighbourliness" of the polytope of correlations of order `≤ t` **is a known result** (and for any finite alphabets; sharp).  F7 |
| Curto–Fialkow (flat extensions) | search summary | A positive moment matrix with a flat extension has a unique, rank-atomic representing measure, atoms on the variety of the kernel.  As in the table of E18 |
| Venkatesh–Baldi 1991; Baldi–Venkatesh 1987 | search summary | Capacity of order `n^d` for interactions of order `d`; statements not seen |
| Jiang–Sidiropoulos–ten Berge 2001 | search summary | Almost-sure identifiability of multidimensional harmonic retrieval (among models with a given number of harmonics) |

---

## 5. Novelty classes

| item | report | assessment |
|---|---|---|
| E18 | elementary; formulation | Agreed; known in substance.  Neighbours to cite: the "extremal" truncated moment problem (rank of the moment matrix = number of points of the variety of its kernel; Curto–Fialkow–Möller, from memory); `‖P^⊥v(x)‖²` is the null spectrum of MUSIC (Schmidt 1986, from memory) read as a dual certificate |
| E18 Remark 1 | "the certificate proof is ours" | Agreed as a proof; the statement is the 3-neighbourliness of the cut polytope, which is the case `t = 2` of Kahle's theorem |
| E18′ | elementary (not searched) | **Formulation.**  It is the standard argument for generic uniqueness of sparsest representations (an `s`-sparse vector with generic entries is the only `s`-sparse solution once no other support carries the same flat; Foucart–Rauhut §2.2, from memory — my search did not confirm the reference), in the non-negative setting, with "flat-isolated" as the hypothesis on the support.  The contrast with the face condition is the `ℓ⁰`/`ℓ¹` gap of sparse recovery |
| E19(b), (c) | synthesis | Agreed.  (c): the contrast `n²/2` against `2n` was not found by me either; it is E18′ + Baldi–Vershynin |
| E19(d) | synthesis | Agreed; it is Cover's separating capacity for polynomial threshold functions (Cover 1965, §III) and the capacity of higher-order associative memories (Baldi–Venkatesh; summary) read through E1.  Not a new bound |
| E19, missing | — | The deterministic capacity `2^{2d} − 1` (Kahle): **known**, not in the report (F7) |
| E19(e), (f), C3 | N; conjecture | (f) reproduces a known curve (F4).  C3: I know no source |
| E20 | synthesis | Agreed (trisecant lemma + E18).  The torus Corollary is positive multidimensional harmonic retrieval with three samples per dimension; uniqueness *among all positive measures* is the notion of Carathéodory–Toeplitz–Pisarenko in one dimension.  The count `2^r − r − 1` was not found.  The literature on identifiability of tensors of format `2×…×2` (Bocci–Chiantini 2013; summary) concerns uniqueness among decompositions of the same rank and would bear on a torus version of E18′, which the report does not state |
| torus, `K = 2^r − r` for `r = 3` | N | A two-line theorem (F5); not found |
| E20′, E20″ | elementary (not searched) | Agreed; two searches of mine found nothing.  Class: elementary, **new (not found)** as explicit statements |
| E21 | elementary (Hall / Frobenius–König); not searched | **Too generous on finite product spaces**: weaker than Kahle's theorem there; what remains is the explicit formula (F7).  On tori: not found; the permanent as a certificate was not found in one search |

---

## 6. Scripts and key outputs

All in `docs/ensemble/reviews/ER3_scripts/` (scripts `er3_*.py`, `er3_lean_checks.lean`;
outputs `out_*.txt`, `rerun_*.txt`).  numpy/scipy only; each run under ten minutes.
`er3_kbody.py` and `er3_l6_trace.py` import the division's modules read-only.  The lines
below are condensed; the numbers are verbatim.

**Numbers of §4c against the stored outputs.**  Printed and equal: `4 960`, `2 880` (L5);
`1.000, 1.000, 1.000, 0.995, 0.955` at `24, 33, 49, 54, 66`, `66` (L1); `38`, `12…24` (L2);
`29, 46, 67`, `84, 186, 352` (kbody headers); six zeros (L4); `46`, `1.25`, `0.147`, `0.297`
(L6); `15`, `1.32`, `41 664`, `30 720`, `10 944`, `960` (L7).  Not printed (interpolated by
hand): `76, 152, 233`; `78, 142, 214`; `0.97, 1.07, 1.09`; `2.6…3.5`; `11`, `13`, `11.5`, `16`
(F3).  Not what is printed: "for every … (L3)" (F2).

`rerun_lifted_checks.txt`, `rerun_kbody_capacity.txt`

    lifted_checks.py: identical to the L1-L7 block of output.txt at 8d42f60 (186 s)
    kbody_capacity.py "8 2 40 ...", "10 2 20 ...", "8 2g 40 ...", "12 1 40 ...", "12 1g 40 ...": identical to output_threshold.txt
    not re-run: "10 2g", "14 1g", "12 2", "12 2g"

`er3_e18_remark1.py`

    n = 6: 4960 triples; dependent: 0; fewer than three patterns: 0; more than one extra sign vector: 0; extra vertex present in 2880
           (wrong prediction of its presence or of y: 0); dependent x x^T on Z_S: 0; LP: 4960 triples, not identified: 0 / 0 / 0
    n = 7: 41664 triples; ... extra vertex present in 19264 ...; LP: 1953 triples, not identified: 0 / 0 / 0
    E18, 3000 random instances: hypothesis holds in 1393, identification confirmed by LP in 1393; dependent matrices on Z_S in 1607
           (full-support ensemble on Z_S then not identified in 1440)
    edge case 2: X = {x0,x0',x1}, v = 0, 0, 1, S = {x0,x0'}: zero set [0, 1] = S ...; ensemble on S identified: False

`er3_e18prime.py`: the table of F2, and

    random instances: flat-isolated and affinely independent: 356, twin for a random weight: 0
                      affinely independent, NOT flat-isolated: 859; a twin for at least one of 20 random weights in 859, for all 20 in 859
                      affinely dependent on S: 285; second ensemble on the same support in 285

`er3_e19.py`

    X. K = 66: 400 supports; lift-isolated: exact 0.978, floating point (tolerance 1e-7) 0.978; states classified differently: 0
    L. n = 12: K = 24: 1.000, K = 33: 1.000, K = 49: 1.000, K = 54: 0.993, K = 66: 0.960; smallest non-zero distance from the span: 2.10e-06
    C. n = 6, d = 1: D_odd = 5, K = 12: separable labellings minus Cover's bound 1124 (of 4096): at most -880
       n = 7, d = 1, K = 14: labels -x_1 strictly separable in 0.085 of 400 samples; bound P(Bin(K-1, 1/2) <= D_odd - 1) = 0.291
    P. K = 13: vertices that are not the ensemble: numbers of atoms {14: 1, 15: 54, 16: 345}

`er3_kbody.py` (`out_kbody.txt`, `out_kbody_V12.txt`), `er3_dt_curve.py`

    n = 8  (four-body), K = 65..90: is_face = reviewer's decision in 360 of 360; status != 0 in 0 of 360 LPs
    n = 10 (four-body), K = 140..170: 100 of 100
    n = 12 (pair), K = 10..16: 300 of 300 (878 LPs inside is_face, status != 0 in 0); n = 12 (four-body), K = 232: 5 of 5
    faces: margins of the reviewer's certificates (feasible, not optimised) >= 1.3e-02, once 2.1e-04; non-faces: Stiemke residual <= 5.4e-10
    thresholds: the table of F3
    n = 12, four-body data (er3_kbody_n12.py): K = 228: face in 16 of 16 supports; K = 234: 11 of 16; K = 240: 2 of 16
    check: rho_W^+(1/2) = 0.5582 (Donoho-Tanner: .5581)
    n = 8: theory rho_W^+ D = 76.4; control 78   | n = 10: 142.0; control 142 | n = 12: 215.2; control 214
    pair data n = 12: theory 10.9 = 0.910 n; control 11 | n = 14: 11.5; control 11.5 | n = 400: 0.380 n; n/(4 ln 2) = 0.361 n

`er3_e20_torus.py` (`T3`, `T4`), `er3_torus_range.py` (`A`, `B`, `C`, `Cprime`)

    r = 3, K = 4: 2000 random 4-tuples; det M(z3) has degree 4 and its roots are the four given z3 in all but 0 cases
    r = 3, K = 5: 5000 random 5-tuples; number on the torus: {6: 5000}; largest | |z_k| - 1 | of the sixth point: 2.3e-11
           smallest singular value of the six normalised rank-one matrices: min 4.12e-05, median 3.06e-01; smallest distance of the sixth point from the five: 7.83e-05
    r = 3, K = 6: 7128 zeros on the torus over 3600 values of z3: a curve
    r = 4, K = 12: number of solutions on the torus -> instances: {16: 1, 18: 15, 20: 12, 22: 7, 24: 2}; Euler-Jacobi residual 1.2e-11
           fewer than 24: smallest singular value min 1.17e-03; all 24: max 2.67e-14
           all 24: relations: 1; coefficients on the 12 extra zeros: 4 positive, 8 negative | 6 positive, 6 negative -> no twin
    A. six states, r = 3: dimension of the span on the curve: 12; largest mass farther than 0.05 from the states with the same data:
           1.000 1.000 0.434 1.000 1.000 1.000 1.000 1.000 1.000 0.987 (residual <= 7.8e-15)
    B. twelve states, r = 4, all 24 zeros on the torus (3 instances): relations: 1; signs on the extra zeros 4+/8-, 9+/3-, 7+/5-; LP: mass off the states 0
    C. thirteen states, r = 4: span on the curve: 36; mass far from the states: 0, 0, 1.00, 1.00
    C'. instances 1, 2 with data within tau: tau = 1e-6: 1.8e-02, 6.5e-02; tau = 1e-4: 0.42, 0.74

`er3_e20pp.py`, `er3_e20pp_improved.py`, `er3_l6_trace.py`

    |D| = 2, E empty: 109 pairs: c_true / c_D between 2.000 and 4.0; (a) violated: 0
    |D| = 3, E empty: 20 pairs: c_true / c_D between 2.130 and 80002.2; (a) violated: 0
    shared angles, r = 3..5, 300 pairs, 60000 points each: smallest f/(c* min d^2) = 1.063; violations: 0
    case 4 (r = 3, |D| = 2, |E| = 1): tau = 1e-4: sup int min(d^2) dnu = 2.092e-03, bound 6.423e-03 (ratio 0.326);
           sup |nu(N_q) - w_q| = 4.749e-04, bound (c) = 1.058e-01; reviewer's linear bound 9.030e-03
    L6 trace: pairs generated: 60; skipped because some beta < 0.05: 14; r = 5, shared = 2, |D| = 3, beta_min = 3.210, 1/c* = 1.246

`er3_e21.py`

    q = 2, r = 6, K = 3: 41664 families; (a) wrong: 0; Hall holds in 30720: zero set != states: 0, no SDR: 0;
           Hall fails in 10944: predicted sub-product not in the zero set: 0, zero set = states nevertheless: 9984
    q = 3, r = 4, K = 3: 85320 families; ... Hall holds in 61560: zero set != states: 0, no SDR: 0; Hall fails in 23760: ... zero set = states nevertheless: 0
    order t = 3: all 11440 sets of 7 = 2^t - 1 states are simplicial faces (failures: 0); ... 352 violate the Hall condition and are identified all the same
    n = 8, even correlations of order <= 4: 300 random sets of 15 conformers: not a face in 0; an explicit set of 16 ... is a face: False
    the 9 x 9 matrix of the double-point conditions: smallest relative singular value at most 1.5e-16, second smallest at least 8.0e-06: RANK 8
    20 random triples, LP on the curve: a twin with mass 1.000..1.000 off the three states and the same nine data (residual 3.9e-15)

(For ternary and larger alphabets a failure of the Hall condition always gave extra zeros
in the exhaustive runs; "possibly nothing but the states" is specific to binary
coordinates, as the text says.)

---

## 7. Not settled

* **The torus beyond `r = 3`.**  `r = 4`, `K = 12`: identified in all 40 instances computed
  (E18(ii), or the weaker criterion of F5 when all 24 zeros are real) — numerical, not a
  theorem.  `K = 13`: an explicit twin in 2 of 4 instances; in the other 2 the discretised
  curve has no twin with exact data, but the mass that can leave the states grows like
  `τ^{0.5…0.9}` with the data tolerance (`10⁻⁶ → 2…6 %`).  Whether these two are identified
  with a very small gap or not at all I could not decide.  The answer to O10 for `r ≥ 4`
  may depend on the configuration and not only on `K`.
* **`r = 3`, "not at 6".**  Ten explicit twins and a count (12 conditions on a
  12-dimensional space on a curve of genus one) — not a proof that the set of six-tuples
  with an identified ensemble is of measure zero.
* **Thresholds at `n = 12`**: the cube's was replicated with 16 supports per `K` only
  (F3); the Gaussian one was not repeated (theory: `215.2`).
* **Whether `c_true ≥ 2c_D` always for `|D| = 2`** (numerical: 109 pairs).
* **O9.**  The mechanism behind the exceptional weights of F2: if `S` is not a face there
  are `T ⊂ X ∖ S` and `c ∈ conv Φ(T) ∩ aff Φ(S)`, `c = Σ_S u_aΦ(x_a)`; if `u` has at least
  `|T|` positive entries, weights with `w_a = εu_a` on `|T|` of them have a twin with `K`
  atoms.  For random conformers with `n ≪ K ≪ n²/4` this needs `|T| > n²/2 − K` generically,
  more than the number of entries of `u`; that is a heuristic for O9, not an answer.
* **Conjecture C3** — not examined beyond F4.
* **Baldi–Vershynin's proofs; Abbe–Shpilka–Wigderson; journal versions** — not read.
  **Donoho–Tanner**: the converse half outside proportional growth.  **Venkatesh–Baldi,
  Curto–Fialkow, Jiang–Sidiropoulos–ten Berge, Bocci–Chiantini** — search summaries only.
  **Foucart–Rauhut, MUSIC, Curto–Fialkow–Möller** — from memory.
* **Chains.**  The two statements on which the last paragraph of §4c.4 rests (rigid shared
  segments; span of the pair products for three torsions) are not the division's and were
  not checked by me either.  Row 5 of the table of E18 and of §4c.5 was not checked.

---

## Sources consulted

* [Baldi–Vershynin, arXiv 1803.10868 (v3 read)](https://arxiv.org/abs/1803.10868)
* [Chiantini–Coppens, arXiv math/0005202 (read)](https://arxiv.org/abs/math/0005202)
* [Donoho–Tanner, arXiv math/0607364 (read)](https://arxiv.org/abs/math/0607364)
* [Cover 1965, scan on the author's archive page (read)](https://isl.stanford.edu/~cover/papers/paper2.pdf)
* [Kahle, "Neighborliness of marginal polytopes", arXiv 0809.0786 (read)](https://arxiv.org/abs/0809.0786)
* [Curto–Fialkow, arXiv math/0507067 (search summary)](https://arxiv.org/abs/math/0507067)
* [Venkatesh–Baldi 1991, abstract page (search summary)](https://www.bohrium.com/paper-details/programmed-interactions-in-higher-order-neural-networks-maximal-capacity/812336222931255297-832)
* [Bocci–Chiantini, J. Algebraic Geom. 22 (2013) (search summary)](https://www.ams.org/jag/2013-22-01/S1056-3911-2011-00592-4/)
* [Liu–Sidiropoulos, follow-up to Jiang–Sidiropoulos–ten Berge (search summary)](https://experts.umn.edu/en/publications/almost-sure-identifiability-of-constant-modulus-multidimensional-/)
* [Cover's theorem, Wikipedia (search summary)](https://en.wikipedia.org/wiki/Cover%27s_theorem)
