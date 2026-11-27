# Referee report on workstream G — "envelopes from the geometry of articulated chains"

Reviewed: `<session scratch>/ws/G/REPORT.md`
(with its scripts `e*.py`, outputs `out_*.txt`, `lean/*.lean`); brief `docs/workstreams/G_brief.md`.
Context read: theory report §4.4 and §11 (as of about 21:40 UTC, 24 Nov 2026; the file was edited by another
process later, the theorem numbers used here were unchanged at 22:21), `DEAD_ENDS.md` D31, `prior_art/L3` §C13,
and the Lean statements `partition_bound`, `partition_bound_hamming`, `expected_queries_ge_exp_weights_min`,
`thermal_expected_queries_ge`, `softGap`, `slack`, `dipWeight`, `sum_dipWeight_eq`,
`residual_torsion_move_min_in`, `residualLowerClass_of_invariant_lipschitz` (statements only, not their proofs).

Referee scratch directory (all my code and outputs):
`<session scratch>/referee_G/`
(`reflib.py` = own chain builder, Kabsch distance by Horn's quaternion method instead of an SVD, exact-integer
diamond-lattice builder; `r1…r12*.py`; `out_r*.txt`; `lean/typecheck.log`).  Nothing in the repository was
touched.  The author's scripts were read to see what was computed; none of them was run or imported.

Abbreviations in the tables: **D** = re-derived line by line, **N** = recomputed with my own code,
**L** = scratch Lean file type-checked by me and compared with the prose, **R** = read only.

---

## 0. Summary

**No critical error.**  Every headline statement that I could test survived, and every table entry that I
recomputed (about 150 numbers, including the exact small-chain covering brackets) agrees with the report to
the printed digits.  The three scratch Lean files type-check (no `sorry`, axioms `propext`,
`Classical.choice`, `Quot.sound`) and state what the prose says.

What is a proof and what is numerical:

| headline | status after review |
|---|---|
| 1. lever-arm law `c_i = Θ(Λ b m_i^{3/2})` | Upper constant: proved (triangle inequality); `c^ver_i/(Λ b m_i^{3/2})` decreases from 1.73 (`m = 1`) to 0.824 (`m → ∞`) and is `≥ 0.824` for every `m`.  Lower constant 0.186: numerical; I confirm it for all `m ≤ 240` and at `m = 500 … 10⁵` (value − limit `≈ +0.28/m`, limit 0.18634).  A rigorous `Ω(m^{3/2})` with a smaller constant (`≈ 0.087`) follows from an elementary pairing inequality that the report does not use. |
| 2. Theorem G3 | Correct.  A direct corollary of Theorem 11.6(c) (`partition_bound`, one slope `t` for all sites, unequal constants allowed, so no conflict with D31), of 11.23(b) and of 11.24(b).  Closed form re-derived; tables reproduced. |
| 3. Theorem G8 | (a) correct, a complete proof; the cover is a certificate in the repository's sense **for the zero residual**.  (b) correct as a parametrised inequality, conditional on the number `Δ_s`, which is a floating-point Kabsch distance of two explicit block shapes; the closed form `0.0506 √(λN)` is asymptotic and is **not** implied by the proof on the stated range of `λ`.  Small-chain brackets reproduced exactly (`n = 6, 7`, all `L`; `n = 8`, `L = 4`: 723–961, 452–649, 26–31). |
| 4. zipper bound G4 | (i) one line; (ii) hairpin witness verified in exact integer arithmetic for every `n ≤ 80` (and 8 larger `n`) and every torsion `i`; upper bound `2m_i+1` and exhaustive values reproduced for `n ≤ 11`. |
| 5. finite temperature (G9) | Identity and cover bound: machine-checked, statements match; chain bound: correct paper proof. |
| 6. remaining statements | G2(b) (extensive `L` on the diamond lattice) and G11 (rank `P+1`) verified; G10(a) Lean-checked, G10(c) re-derived, G10(d) reproduced at `n = 6, 7`. |

Things in the report's summary that are stronger than what is proved are listed in §2 (M1 and m1–m5): the
word "certifiable" and "the whole exponential price … is the ℓ¹ chain rule"; the constant and range of the
G8 lower bound; "0.186 for all `m`"; "exactly / iff sequence-local"; "Theorem G9, machine-checked".

Novelty (my judgement, without a web search — see §4): everything is elementary.  G1 and G3 are routine
(the repository's own prior-art note had asked for the lever-arm scaling); G8 is, as far as I know, new as a
statement but is Kolmogorov–Tikhomirov entropy of Lipschitz curves plus Chernoff counting; G9a is a one-line
identity that is not in the repository; G10(a) is the classical "necessary optimality" criterion of
interval-data optimisation and should be cited as such.

---

## 1. Verdict per statement

| statement | correct? | how checked | depth | novelty | remark |
|---|---|---|---|---|---|
| G1(a) extended chain: `I = b² sin²θ S(m)`, `S(m) = Σ⌈p/2⌉²` | yes | D, N (error `1.4·10⁻¹⁰`, `n ≤ 60`, all `i`, two bond angles) | routine | routine | |
| G1(c) uniform bound `I ≤ Ī(m) = Σ d̄(p)²`, `Ī ~ sin²(θ/2) b² m³/3` | yes (proof) | D, N (exhaustive `m ≤ 11`: `I_max ≤` zigzag form `≤ Ī`) | routine | routine | "asymptotically attained": the tested pattern reaches 0.99904 of the bound at `θ = 111°` (exactly 1 at the tetrahedral angle) — m8 |
| G1(d) `c^ver_i = 2Λ sin(δ/2) √Ī(m_i)`, limit constant 0.824 | yes | D, N; Lean statement `residual_torsion_move_min_in` read | routine | constants new | `c^ver ≥ 0.824 Λ b m^{3/2}` for every `m` (needed by G3) is true but not stated — m5 |
| G1(e) `c_i* ≥ Λ ρ^sym(m_i)`, `ρ^sym(m) ≥ 0.186 b m^{3/2}` | first inequality yes (proof); second numerical | D, N (`m ≤ 240` all; `m` up to `10⁵` sampled; thin-rod limit 0.18634 re-derived) | routine | constants new | not proved for all `m`, used up to `m = 5·10⁴` — m2 |
| G1(e) loss factor 4.4 = 1.77 × 2.05 × 1.22; exhaustive exact/verified 0.59–0.95 | yes | N (`n = 5…8`: 0.594–0.953) | routine | — | |
| G1(f) conformation-specific values | yes for extended (16.0; 39.9) and helix (18.8; 40.6); coil/compact not checked | N | — | — | |
| G2(a) `Λ ≤ ℓ√(qM)` | yes | D | routine | routine | |
| G2(b) words `ttg⁺tt`, `g⁺tg⁻tg⁺`: same end frame; `L ≥ 0.387 n e_g/b` | yes (exact on the lattice) | N, integer arithmetic (`r ≤ 400`: coincide on `3r+3` of `5r+3` atoms, max displacement `√(8/3) b`, RMSD 0.9992, 1.0244, 1.0308 at `n = 50, 200, 800`) | elementary | known in spirit (local "crankshaft" moves) | proved for the gauche count only; "extensive local residual ⇒ `L ∝ N`" in general is an upper bound plus this example |
| G3 deterministic bound and closed form `C_{k,γ}` | yes | D (algebra re-done), N (28 small products: closed ≤ pre-optimised ≤ partition bound ≤ `N_frac` ≤ greedy) | routine | closed form new relative to repo | correct lemma, common slope; D31 respected |
| G3 randomised minimum and `ln Z` | yes | D from 11.23(b), 11.24(b) as stated in Lean | routine | routine | lower bound at the zero-residual instance for algorithms correct on the class |
| G3 tables (sharp sites, LB, deficits, finite temperature `H`, `U`, randomised LB at `ε = 0`, reference rates) | yes | N (own per-site LP by vertex enumeration, cross-checked against a generic LP) | — | — | `ε_crit` and the `ε = 0.1n, n` columns not recomputed |
| G4(i) `d ≥ u₀·abs(Δ#C)` | yes | D | trivial | trivial | |
| G4(ii) `⌊(m_i−1)/2⌋ ≤ zip_i ≤ 2m_i+1` | yes ([P+N] as tagged) | N (4740 pairs `(n,i)`, exact integers; exhaustive `n ≤ 11`) | elementary | formulation new, construction textbook | extension to all `n` rests on periodicity of the all-trans arms (sound) |
| G4 corollary (`γ = 1`) | yes | D, N (`u₀ = e`, `n = 1000`: 8 sharp, LB 973.8) | routine | routine | |
| G5 counting `c_i ≤ u(w−1)(w−2)/2`, frame argument | yes | D | routine | routine | measured `D_F` maxima not recomputed; "iff" overstated — m3 |
| G6 lemma (three rigid segments); single-contact ANOVA | yes | D; N for `s = 5, 7, 9` (0.720, 0.401, 0.112) | routine | — | `c_ij` tables not recomputed |
| 2.7(a)–(d) | yes | D; N for the capped-Hamming rates | routine | (b) known, (d) inequality known | "1 +" in (b) needs a unique minimiser — m6 |
| G8(a) upper bound, explicit and simplified | yes | D (81 vectors counted; constants 4.90, floor argument, range of `λ`); N (explicit values; simplified ≥ explicit on 420/420 grid points) | elementary | apparently new | zero residual only; extends verbatim to any subdomain (excluded volume) |
| G8(b) `N_cov ≥ exp(w[ln 2 − h(ϑ)])` | yes, given `Δ_s` | D; N (brute force over all `3ⁿ` centres for three small families; superadditivity) | elementary | apparently new | `Δ_s` numerical; chain-geometry specific (`θ = 111°`, `δ = 120°`) |
| G8(b) closed form `0.0506 √(λN)` on `2/(ηN) ≤ λ ≤ 1.5N` | **not proved as stated** | N | — | — | m1 |
| G8 tables (explicit bounds; Hamming lower; small chains) | yes | N (all six rows; `n = 6, 7` all `L`; `n = 8`, `L = 4`) | — | — | `n = 8`, `L = 2, 8` not recomputed |
| G9a residual-independence identity | yes | L, D, N (400 random instances, rel. error `3.5·10⁻¹⁵`) | trivial | not in repo | |
| G9b cover bound | yes | L, D, N | routine | standard | |
| G9 chain bound `6.93√(βLbN) + 2.73βLb + 4.39` | yes | D | routine | routine | needs the hint; not machine-checked — m4 |
| G9 small-chain `U`, `W1` | yes at `n = 7` (1.75, 5.41, 5.84; 4.10, 12.9, 16.8) | N | — | — | `n = 8` rows not recomputed |
| G10(a) per-contact sharpness | yes | L, D | trivial | known (necessary optimality under interval data) | cite |
| G10(b) Gō-type thresholds | not checked | R | — | — | |
| G10(c) exponential lower bound, rates | yes | D, N (0.00200, 0.00394, 0.00765, 0.01444, 0.02600) | elementary | new, minor | phantom domain, torsion-only `f` |
| G10(d) sizes | yes at `n = 6, 7` (e.g. 359–452 against 2) | N | — | — | `n = 8, 9, 10` not recomputed |
| G11 rank `≤ P+1` | yes | D, N (rank `= P+1 = 7, 10, 13, 17, 21` for `n = 6…10`, phantom and SAW) | trivial | trivial | spanner numbers not recomputed |
| Lean files (3 files, 6 theorems) | type-check | L (15–18 s each) | — | — | statements match the prose |

**Answers to the specific questions of the brief.**

* *How `Λ` and the normalisation of RMSD enter.*  `D_K = min_g ‖X − gY‖_F` over proper motions,
  `RMSD = D_K/√N` with `N = n + 3` atoms.  `Λ`-Lipschitz in `D_K` is the same as `L`-Lipschitz in RMSD with
  `L = Λ√N`; every constant is `c_i = Λ ρ_i = L ρ_i/√N`, `ρ_i` an `ℓ²` displacement.  The report is
  consistent in this throughout (also in G8: `Θ = N(w e_max + ε)²/L²`).
* *G3: which lemma, and is the form right for unequal constants?*  Theorem 11.6(c) in the form
  `partition_bound` (`CertificationGeometry.lean`, any cover) with the product denominator of
  `partition_bound_hamming` (`CertificateComplexity.lean`, arbitrary site alphabets and constants).  It is a
  one-shot bound with a single slope `t`; nothing is optimised site by site, so the objection of D31 does not
  apply.  The tables use `max_t Σ_i max_v r_i(t; v)`, again with one `t` (I recomputed them that way).
  G3 claims a lower bound and the trivial upper bound `k^{n − n_sharp}`, not the exact exponent of
  Theorem 11.9 (which would need finitely many site types).
* *G8(a): what are the centres, and is it a certificate?*  Centres: the all-trans state and, for every
  number `w` of non-trans torsions, one conformation with exactly `w` non-trans torsions per code, the code
  being the positions of every `s_w`-th atom and of the last atom, in the common frame of the first three
  atoms (no superposition), rounded to the grid `(s_w b)ℤ³`; if `s_w = 0` the whole layer.  Radii: a
  conformation `y` of layer `w` and its centre `a` satisfy
  `L·RMSD(a, y) ≤ L(1+√3) s_w b ≤ w e_min + ε ≤ gap(y) + ε`.  With the zero residual the slack is the
  envelope, so this is a cover in the sense of Theorem 11.4 and, since it contains the minimiser, a point
  certificate.  It is an existence statement about the number of evaluations; checking it needs RMSD bounds
  that the kernel does not have (the report says so).
* *G8(b): how was `η` obtained, and is the argument a proof?*  `η_s = Δ_s/(s^{3/2} b)`, `Δ_s` the Kabsch
  distance between two explicit conformations of a block of `s` atoms (one `g⁺` at the first, respectively
  at the central internal torsion), computed in floating point for `s ≤ 640` by the author and for `s` up to
  `10⁵` by me; the limit `0.06588` is `2^{−3/2}` times the thin-rod constant of G1(e).  The chain of
  inequalities (block superadditivity, shape depends only on internal torsions, triangle inequality,
  two-letter moment bound, Chernoff) is a proof; I re-derived each step and tested the counting lemma by
  brute force.  The numerical input is the single number `Δ_s` per block length; the closed form with 0.0506
  is an asymptotic numerical estimate (m1).

---

## 2. Errors and gaps

### CRITICAL
None.

### MAJOR

**M1. The practical conclusion drawn from G8/G9 is stronger than the theorems** (summary (iv); table 2.12,
row 3 "certifiable in the query count"; §6 item 2 "the whole exponential price of the RMSD route is the ℓ¹
chain rule").  The theorems are correct; four qualifications are missing where the conclusion is drawn.

1. *Instance.*  G8(a) bounds `N_cov` at the **zero residual**, for an additive torsional known part with a
   unique all-trans ground state and `e_min > 0`.  It is not an upper bound for other admissible residuals:
   `g = −L·RMSD(x₀, ·)` is admissible and removes the funnel: at `n = 8`, `L = 4` it puts 67.7 % of the
   conformations below the all-trans state (`out_r13.txt`; equivalently the ground state alone covers
   32.3 %).  The lower bounds do transfer to every algorithm; the upper bound does not transfer to every
   instance.  (§5 item 7 of the report says this; the summary does not.)
2. *Normalisation.*  The certificate is sub-exponential only if `λ = Lb/e = o(N)`.  By the report's own
   Theorem G2 an extensive local residual has `L ∝ N`; then G8(b) gives `exp(Ω(N))` for the direct RMSD
   envelope as well (rate about `0.05 √(ℓb/e)`), and the upper rate of G8(c) is below `ln 3` only for
   `ℓb/e < ln 3/36 ≈ 0.03`.  So the exponential price is not only the chain rule.
3. *Size.*  At `n = 1000`, `λ = 1` the proved bracket is `e^{1.6} ≤ N_cov ≤ e^{235}`; at `n = 10⁵`:
   `e^{16} … e^{2937}` (recomputed).  "Certifiable" is not established at any concrete size; what is proved is
   the growth law `Θ̃(√(λN))`.
4. *Hint.*  The `exp(O(√(βLbN)))` cost of G9 is that of the spot-check, which is given the instance as a
   hint (said in 2.9, not in the summary).

*Fix.*  State: "at the zero residual, for RMSD-intensive or Frobenius-intensive `L`, the number of
evaluations of a certificate under the RMSD envelope grows like `exp(Θ̃(√(λN)))` instead of `kⁿ⁻ᵒ⁽ⁿ⁾`; for
extensive `L` both formats are exponential; no statement is made for other instances or about a kernel that
could check such a certificate."

### MINOR

**m1. G8(b): closed form, range, and the constant `η`** (2.8, statement (b); summary (iv) "0.05 √(LbN/e) ≤
ln N_cov").
* `η_s` is not "0.059…0.071 for 8 ≤ s ≤ 20": with the report's own block shapes `η_9 = 0.0533` and
  `η_11 = 0.0722` (only even `s` were printed).  `η_s` tends to `0.06588 = 2^{−3/2}·0.18634` **from below**:
  `inf_{s ≥ s₀} η_s = 0.0533, 0.0593, 0.0630, 0.0646, 0.0654, 0.0657` for `s₀ = 8, 12, 20, 30, 50, 100`
  (`s ≤ 2000`); 1987 of the 1993 values of `s ∈ [8, 2000]` are below 0.0659.
* With integer `w`, `s = ⌊N/w⌋` and exact `Δ_s`, the proof does not give `0.0506 √(λN)` on the stated range
  `2/(ηN) ≤ λ ≤ 1.5N`: at the lower end it gives nothing (`ϑ > ½` for `w = 1`); on 300 log-spaced values of
  `λ` it falls short at 22–46 % of them for `N = 200, 1003, 5000, 20000` even when the integrality of `N_cov`
  is used; worst ratio (proved)/(closed form) for `λN ≥ 200`: 0.855–0.865.  The report's own table point
  `λ = 10`, `n = 10³` is an example: the argument gives 5.05, the closed form 5.07.
* *Corrected statement.*  "For all integers `w ≥ 1`, `s ≥ 5` with `ws ≤ N`:
  `N_cov(ε) ≥ exp(w[ln 2 − h(ϑ)])`, `ϑ = 2N(w e_max + ε)²/(L² w Δ_s²) ≤ ½`.  Numerically (generic chain,
  `θ = 111°`, `δ = 120°`): `ln N_cov ≥ 0.043 √(λN)` for `32/N ≤ λ ≤ 1.5N` (what my grids support:
  `N = 200, 1003, 5000, 20000`, 300 values of `λ` each; for `32 ≤ λN ≤ 187` through `N_cov ≥ 2`), and
  `ln N_cov ≥ (0.0505 − o(1)) √(λN)` when `λN → ∞`, `λ/N → 0`."  If a fully rigorous constant is wanted,
  replace `Δ_s` by the gyration bound `D_K ≥ |‖X_c‖ − ‖Y_c‖|` (closed-form sums; costs a factor ≈ 3).

**m2. `ρ^sym(m) ≥ 0.186 b m^{3/2}` is used beyond the range where it was computed** (2.1(e): "computed for
all `m ≤ 240`"; used in Remark 1 of 2.8 for `n = 10⁵`, i.e. `m` up to `5·10⁴`, and in "`c_i = Θ(…)`").  My
values: 0.186897, 0.186617, 0.186393, 0.186351, 0.186340 at `m = 500, 10³, 5·10³, 2·10⁴, 10⁵`;
`m·(value − 0.18634) → 0.2795 > 0`; same pattern for the tetrahedral angle (limit 0.18909).  So the claim is
numerically safe, but it is not a theorem.  *Fix:* either say "numerical" wherever it is used, or prove
`Ω(m^{3/2})` by the pairing inequality
`D_K²(X,Y) ≥ ½ Σ_p (|X_{i−p} − X_{i+1+p}| − |Y_{i−p} − Y_{i+1+p}|)²` (disjoint pairs; one line from the
triangle inequality), which gives `≥ 0.0866 b m^{3/2}` asymptotically and `≥ 0.0866` at every `m` I
evaluated (`m = 2 … 3000`).

**m3. "Constants are chain-length independent iff the residual (or the metric) is local in sequence"**
(2.5 Reading; summary (iii) "exactly").  Only "if" is proved.  "Only if" is false in general: pair terms of
unbounded sequence separation `s` with oscillation `u s⁻³` give `c_i ≤ u Σ_s (s−2) s⁻³ < ∞` for every `n`.
*Fix:* "bounded window (more generally `Σ_s s·u_s < ∞`) ⇒ bounded constants; contact terms of fixed
amplitude ⇒ `c_i ≥ u₀⌊(m_i−1)/2⌋`."

**m4. "(Theorem G9, machine-checked)"** (summary (iv)).  Machine-checked are Lemmas G9a and G9b; the chain
bound (code cells of unsuperposed RMSD diameter `(1+√3)sb`) is a paper proof.  It is correct.

**m5. Which constants are "verified", and one missing line.**  (i) The tables (2.3, 2.8 "H-ver") use the
zigzag form `d(p) = b√(p² sin²(θ/2) + cos²(θ/2))` for odd `p`, which assumes that the planar zigzag
maximises every intra-chain distance (classical, not proved in the report, and said so in §5).  The
certified constants are larger by at most 3 % (`m = 3`: 5.674 against 5.518); since `N_cov` is monotone in
the envelope, every comparison keeps its direction.  (ii) G3 is applied to the verified constants with
`c₀ = 0.824 Λ b`; this needs `c^ver_i ≥ 0.824 Λ b m_i^{3/2}` for every `m`, which holds
(`d̄(p) ≥ p b sin(θ/2)`, hence `Ī(m) ≥ sin²(θ/2) b² m³/3`) but is written in 2.1(d) only as "`≤ … (1 + O(1/m))`".
(iii) "certified upper bound `0.824 Λ b m^{3/2}`" is an asymptotic equality, not an inequality: the ratio is
1.73, 1.18, 0.98, 0.86, 0.83 at `m = 1, 2, 5, 20, 100`.

**m6.** 2.7(b): `N_cov(ε) ≤ 1 + Σ_j …` assumes that one point covers all minimisers (unique minimiser);
in general replace `1` by `𝒩(X_0, ε)`.

**m7.** Table 2.12: "one evaluation iff `u₀ ≲ 2e/n`" is not an equivalence; proved are "necessary:
`u₀ ≲ 4e/n`" and "sufficient: `u₀ ≤ e/(n+2)`" (SAW pairs).  "rate `≥ 0.19/(24e/u₀ + 6)`": the derivation
gives `0.1882/(24e/u₀ + 2)`, which is smaller than the printed expression for `e/u₀ > 15.6`.

**m8.** 2.1(c) "the bound is asymptotically attained": the tested arm (one gauche next to the axis, then
all-trans) gives `I/m³ → 0.226178` against `sin²(θ/2)/3 = 0.226395` at `θ = 111°` (ratio 0.99904;
Richardson extrapolation from `m = 8000, 16000`); at the tetrahedral angle the ratio is 1.00000.  Say
"attained up to 0.1 %".

**m9.** 2.8 Remark 1: "one more torsion multiplies the Hamming certificates by ≈ 2.2" holds for H-ver; for
H-opt the step `n = 6 → 7` is ×1.45 (LP) to ×1.66 (greedy).

---

## 3. Independent numerical checks

All with my own code (`reflib.py` passed its self-tests: bond lengths, angles and dihedrals of the builder;
Horn-method Kabsch against an SVD formula and under 200 random proper motions; integer lattice builder
against the float builder with the same chirality).  Python 3 with numpy 2.5.3 and scipy 1.18.1 (HiGHS).

**Claim 1 (`r1_lever.py`, `r9_misc.py`, `r10_helix.py`, `r12_kink_limit.py`).**
* Extended chain: `max |I − sin²θ·S(m)| = 1.4·10⁻¹⁰` (`n = 5, 12, 31, 60`, all `i`).
* Arm of `m` atoms, all `3^{m−1}` conformations, `m ≤ 11`: `I_max ≤` zigzag form `≤ Ī(m)`; maximiser =
  (gauche, trans, …, trans) in every case; `I_max/m³ = 0.2584` at `m = 11`.
* `c^ver(m)/(Λ b m^{3/2}) = 1.7321, 1.1806, 0.9805, 0.8614, 0.8316, 0.8249` at `m = 1, 2, 5, 20, 100, 1000`;
  `≥ 0.8241` for all `m < 400`; centre of a long chain `0.2914 L b N`, end `1.732 L b/√N`.
* `ρ^sym(m)/m^{3/2} = 0.2171, 0.1960, 0.1911, 0.1887, 0.1875` at `m = 10, 30, 60, 120, 240` (minimum over
  `m ≤ 240`: 0.18751 at `m = 240`); larger `m` as in m2; thin-rod limit `γ = 58.750°`, 0.18634.
  All-trans chain `n = 240`: `min_i D_K(flip i)/m_i^{3/2} = 0.1899`; central RMSD 16.01 (verified bound 39.85);
  all-`g⁺` helix 18.78 (40.63).
* Tetrahedral bond angle: 0.8165 and 0.1891 in place of 0.824 and 0.186.
* All `3ⁿ` conformations, `n = 5…8`: exact single-change maxima `c*_i/Λ` (e.g. `n = 8`:
  1.541, 3.008, 4.730, 5.810, …); exact/min-inertia bound 0.594–0.953; exact/certified 0.569–0.901.
* Normalisation: `RMSD = D_K/√N` with `N = n+3` atoms; `L = Λ√N`; `c_i = Λρ_i = Lρ_i/√N` throughout.

**Claim 2 (`r2_g3.py`).**
* 28 products `[3]ⁿ`, `n = 5…8`, `c_i = c₀ m_i^γ`, `γ ∈ {1.5, 1, 0.5}`: `exp`(G3 closed form) `≤ exp`(bound
  before optimising `t`) `≤ exp`(partition bound) `≤ N_frac` (LP) `≤` greedy in every case, e.g. `n = 8`,
  `γ = 1.5`, `c₀ = 2`: `12.4 ≤ 82.2 ≤ 159.9 ≤ 712.4 ≤ 773`; exact MILP for `n ≤ 6`.  (LP not obtained in four
  `n = 8` cases; there the comparison is with the greedy value.)
* Report's table: `LB = 65.29, 910.42` (`L = 1`; `n = 100, 1000`), `1024.33` (`L = 10`), `1052.52` (`Λ = 1`),
  `93.10, 1070.36` (`L = 0.1N`); G3 deficits `62.03, 245.64, 97.79, 61.66, 24.40, 38.88`; sharp sites
  8, 20, 2, 0; all sharp iff `L ≤ 0.33629, 0.03431, 0.00343` (`n = 10, 100, 1000`).  All as printed.
* Finite temperature (`r6_tables.py`): `H, U`, randomised LB at `ε = 0` = (97.5, 98.2, 53.2), (975.3, 1071.2,
  858.5), (665.6, 1078.0, 897.4), (97.5, 109.0, 87.9), (975.3, 1098.6, 1062.0); reference rates
  0, 0.1859, 0.3119, 0.5765, 0.7722.

**Claim 3 (`r3_g8.py`, `r3b_closedform.py`, `r5_small.py`, `r8_blockfamily.py`).**
* 81 integer vectors of norm `≤ 1+√3`; in `2·10⁵` random conformations (four settings) same-cell pairs have
  atom displacement `≤ 1.63 sb` and unsuperposed RMSD `≤ 0.96 sb` (bound 2.73).
* Explicit bounds, natural logarithms, exact `Δ_s`: lower 0.51, 5.06, 1.60, 16.03, 5.05, 50.68 and upper
  83.6, 1002.0, 234.7, 2936.9, 635.8, 8458.1 for `(λ, n) = (0.1, 10³), (0.1, 10⁵), (1, 10³), (1, 10⁵),
  (10, 10³), (10, 10⁵)`; simplified upper bound above the explicit one on 420/420 grid points.
  "Hamming relaxation: lower" 324.6, 96067.7, 760.2, 104338.1, 961.6, 107658.9.
* Counting lemma of (b), brute force over **all** centres (`3⁹`, `3¹¹`, `3¹²`) for families `(w, s) = (2, 6),
  (2, 7), (3, 5)`: block costs satisfy `cost(0) + cost(1) ≥ Δ²/2` (observed minimum `≈ Δ²`), block
  superadditivity holds to `10⁻¹⁴`, and no centre covers more members than `exp(w h(ϑ))`.
* Exact covering numbers, zero residual, `ε = 0`, `f = #gauche` (LP by constraint generation / greedy /
  MILP):

  | n | L | H-ver | H-opt | R |
  |---|---|---|---|---|
  | 6 | 1 | 11 | 5 (greedy 6) | 1 |
  | 6 | 2 | 41–57 (exact 41) | 21–24 (exact 21) | 3 |
  | 6 | 4 | 153–185 (exact 169) | 137–161 (exact 145) | 16–20 (exact 16) |
  | 6 | 8 | 495–505 (exact 505) | 495–505 (exact 505) | 210–221 (exact 211) |
  | 7 | 1 | 13–17 | 7–12 | 1 |
  | 7 | 2 | 75–99 | 32–48 | 4 |
  | 7 | 4 | 327–419 | 198–268 | 21–24 |
  | 7 | 8 | 1104–1195 | 688–875 | 321–350 |
  | 8 | 4 | 723–961 | 452–649 | 26–31 |

  These are the report's brackets (my greedy differs from the author's in two cells, R at `L = 8`: 221
  against 223 and 350 against 355; most of the exact values at `n = 6` are new).

**Claim 4 (`r4_lattice.py`).**  Hairpin `t^{p₁} g⁺g⁻g⁺ t^{p₂}`: `⌊min(p₁,p₂)/2⌋ + 1` contacts with `a + b`
constant; changing the first turn torsion (to `t` or to `g⁻`) leaves 0 contacts, both conformations
self-avoiding.  For all `n ∈ [3, 80] ∪ {100, 101, 150, 151, 200, 201, 300, 301}` and all `i`: 4740 pairs,
no violation of `|Δ#C| ≥ ⌊(m_i−1)/2⌋`.  Exhaustive `n = 5…11`: SAW counts 233, 683, 2005, 5849, 17107,
49833, 145379; `zip_i`, symmetric-difference and phantom values identical to the report's; `zip_i ≤ 2m_i+1`.

**Claim 5 (`lean/typecheck.log`, `r6_tables.py`, `r9_misc.py`).**  `SoftGapIndep.lean`, `SoftGapCover.lean`,
`ChainLemmas.lean` compile with `lake env lean` (exit 0, no `sorry`).  `gibbs_mul_exp_softGap` and
`sum_gibbs_exp_softGap_indep` are stated with the repository's `softGap`, `slack`, for arbitrary `d, f, g, β`;
`sum_dipWeight_indep` rewrites the repository's `sum_dipWeight_eq`; `spotCheck_const_le_cover` needs `β ≥ 0`
and a cell map `c : X → J` with `d a y ≤ r` inside cells; `contact_sharp` and `two_letter_moment` are the
statements used in G10(a) and G8(b).  Random instances (asymmetric envelopes, McShane-type residuals): identity
to `3.5·10⁻¹⁵`, cover bound `≥ 1.29 ×` the true value.  `U` at `n = 7`: 1.75, 5.41, 5.84 (`L = 2`, `β = 1`);
3.40, 6.93, 7.11 (`L = 4`, `β = 1`); 5.23, 7.47, 7.55 (`L = 4`, `β = 2`).

**Claim 6.**  G2(b) and G11 as in the table of §1.  Generic chain: `L_eff(#gauche) = 0.782 N`, `0.774 N` at
`n = 6, 7`.  G10(d) (`r7_contact.py`): `n = 6`: 17 maps, `z = (2,4,5,5,4,2)`, H 83–103 against C 1; `n = 7`:
43 maps, `z = (3,5,6,6,6,5,3)`, H 359–452 against C 2 (`u₀ = e`), 1654–1675 against 5 (`2e`), 2187 against 14
(`4e`).  G10(c) rates (`r11_g10c.py`) as printed.  Capped Hamming: 0.1138, 0.1989, 0.4567, 0.9592 (the
report prints 0.113, 0.198, 0.456, 0.959, computed with 0.408 instead of 0.41).

---

## 4. Literature

**No web search could be run.**  The search budget shared by all agents of this session was exhausted when I
reached this step (three queries refused, none executed).  I made two direct page fetches: the arXiv
abstract page of 1608.04679 (Kipnis, Goldsmith, Eldar; read through the fetch tool's summary: the paper
exists, the abstract does not display Berger's formula) and the Wiley page of Maiorov–Crippen 1995 (HTTP 403,
nothing read).  I read §C13 of the repository's `docs/prior_art/L3_realizability_geometry.md` in full.
Everything below is therefore **from memory and unverified in this session**; the coordinator should have
the items re-checked before any of it is cited.

* *Lever arm (G1).*  The repository's own note (L3, C13, "how the claim could be sharpened", item 2) asks for
  exactly this scaling law and reports that none was found.  The law is immediate from `I ∝ m³` for a rod and
  the one-body formula `RMSD² = (4/W) sin²(α/2) I` (Popov–Grudinin 2014, already cited in the theory report).
  Per-joint Lipschitz constants proportional to the distal lever arm are standard for serial kinematic
  chains in robot motion planning.  Verdict: routine; the constants 0.824 and 0.186 are new.
* *Covering numbers of conformation space (G8).*  The report cites Reva–Finkelstein–Skolnick 1998.  Closer
  in content, and missing: Park and Levitt, "The complexity and accuracy of discrete state models of protein
  structure", J. Mol. Biol. 249 (1995) (listed in L3); Kolodny, Koehl, Guibas and Levitt, J. Mol. Biol. 323
  (2002); Sullivan and Kuntz, Proteins 42 (2001) and Biophys. J. 87 (2004); McLachlan, Biopolymers 23 (1984).
  These concern covering at a fixed RMSD radius (exponential in the length).  I know of no statement with
  gap-proportional radii, so the `√(λN)` law is plausibly new; it is an exercise once Kolmogorov–Tikhomirov
  and the gap-scaled covering picture (Bachoc–Cesari–Gerchinovitz) are in hand.
* *`RMSD² ≤ R_g(X)² + R_g(Y)²`* (2.7(d)) is known: Maiorov and Crippen, Proteins 22 (1995), and Betancourt
  and Skolnick, Biopolymers 59 (2001), normalise RMSD by this quantity.  Should be cited.
* *Triangle inequality of the optimal-superposition distance* (used in G8(b)): Kaindl–Steipe 1997,
  Steipe 2002 (already in L3).
* *G10(a).*  "`x₀` is optimal for every coefficient vector in a box iff it is optimal in the scenario that
  is worst for `x₀`" is the necessary-optimality criterion of combinatorial optimisation with interval data
  (Yaman, Karaşan and Pınar 2001; Kasperski and Zieliński).  Not new; should be cited.
* *G2(b).*  Local changes of several torsions that leave the chain trace in place are the kink-jump and
  crankshaft moves of lattice polymer simulation; that RMSD is insensitive to them is common knowledge.
* *G4.*  Tight hairpin (adjacent re-entry) folds on the tetrahedral lattice are textbook polymer physics;
  the formulation as a lower bound on envelope constants I have not seen.
* The report's own citations (Kolmogorov–Tikhomirov 1959; Berger 1970, `R(D) = 2σ²/(π²D)` nats per unit
  time; the `L²` small-ball constant `1/(8ε²)`; Munos 2011; Kleinberg–Slivkins–Upfal 2008; lDDT; the clamped
  frame-aligned error; Awerbuch–Kleinberg 2004) agree with what I remember; none is used in a proof.

The author's own search log says only result summaries were read; the novelty claims of the report
("apparently new consequences, medium confidence") are worded with appropriate caution.

---

## 5. Not checked

* Proofs of the repository theorems that G3, G8 and G9 rely on (11.6, 11.23, 11.24, 11.26): I read the Lean
  statements and did not rebuild the library.
* G1(b) for `φ₀ = 180°` (my axis construction is degenerate for the planar zigzag; the other four helices
  agree within 0.8 %); G1(f) coil and compact values; the continuous-optimisation check of zigzag maximality.
* G2: the generic-chain helix pairs (`0.53 N`); the `n = 7`, `e_g = ½` illustration (123–169).
* G3: `ε_crit` and the columns at `ε = 0.1n`, `ε = n` of the finite-temperature table.
* G5: measured maxima of the clamped frame metric.  G6: the `c_i`, `½Σ_j c_ij` table and loops of 9 and 11
  torsions.
* G8: small chains at `n = 8`, `L = 2, 8`; the layer data and the packing data of Remarks 2–3
  (`out_e6_d`, `out_e6_e`); self-avoidance of the block family.
* G9: the `n = 8` rows; the Jensen brackets; the exact-cover illustration (5.8 against 1.75).
* G10(b) entirely; G10(d) for `n = 8, 9, 10`; G11 spanner norms and ranks for `n = 11, 12`.
* The Monte Carlo of `out_e12.txt` and all statements tagged [H].
* Any prior art online (§4).
* After the container restart only two light computations were run, both under `ulimit -v 2500000`
  (`r12_kink_limit.py`; an inline check written to `out_r13.txt`); all other outputs were complete before the
  restart and were not regenerated.
