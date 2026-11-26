# R23 — a sampled check of the theory division's assumption audit

> **Coordinator's status note (2026-11-26 18:44 UTC, at the commit that first contains this file).**  Handed back by the referee at 18:42 UTC and committed as handed back, to preserve it.  **Not yet read or checked by the coordinator; nothing of it has been sent to the theory division; not to be cited until the coordinator's note at the end of this file and the review message (SCI-REV-0022) exist.**

*Workstream R23 of the science division, 2026-11-26 (17:24–18:36 UTC, from the clock).  One referee agent, no subagents.
Notes: `experiments/science/ws_R23/NOTES.md`.
**This is an internal review, not external peer review.***

**Object.**  The theory branch `claude/determined-ride-og1u7j` at commit `fc3f5d9`, read-only export `<THY>`:
`docs/ASSUMPTION_AUDIT.md` (the synthesis, 364 lines), `docs/audit/AA1_REPORT.md` (1 766 lines), `docs/audit/AA2_REPORT.md`
(1 702 lines), `docs/THEORY_REPORT.md` (12 251 lines), `README.md`, `docs/DEAD_ENDS.md`, `docs/falsification_output.txt`,
`docs/workstreams/{N,R}_REPORT.md`, `experiments/audit/AA1`, `AA2`, `proofs/`.  For §4.2 also the second export `<THY2>` at
`4aea5fe` (the coordinator's note, logged in `NOTES.md` at 18:03 UTC).  All line numbers of the theory report and the README are those of
`fc3f5d9` (= the numbering the audits cite) unless marked "new".

**Kinds of checking** (kept apart throughout): **[review]** = re-derived on paper from the hypotheses; **[replication]** =
recomputed with code written here from the statements, before the audit's scripts were opened; **[re-run]** = the audit's
code, unchanged, from a scratch copy; **[read only]**.  Epistemic labels as in `COMMON.md`: **[V]** machine-checked (I read
Lean statements; nothing was compiled), **[P]** paper proof, **[N]** numerical, **[C]** conjecture, **[H]** heuristic.
Findings are **critical / major / minor**, each with a replacement tag or text.

---

## 0. Verdict in ten lines

1. **`{F}` ("false when removed") can be trusted as "a real counterexample exists": 8 of 10 sampled are counterexamples to
   the statement with the assumption removed** (two rebuilt with own code, five more checked by own argument or computation); 1 refutes a
   lemma of the proof rather than the theorem (the audit says so itself in another entry); 1 shows *vacuity*, not falsity.
2. **`{P}` ("needed only by the proof") cannot be trusted as "the statement survives": 6 of 12 stand** (4 with another proof
   on record, 2 decided here); **4 of 12 are "not known" by the audit's own sibling tag `{?}`; 2 of 12 are false when removed**
   (Theorem 11.32 without "the true residual is additive": own LP counterexample, `N₂ = 3 < K₋ = 4`; Theorem 11.116(e) without
   homogeneity: the limit does not exist).
3. **`{Q}`: 3 of 6 have a precise condition with a proof on record; 1 is true but neither stated nor proved in the audit
   (proved here); 1 states no quantitative condition at all; 1 rests on a sketch of ours quoted without its caveat.**
4. **`{?}`: 3 of 4 are really unknown; 1 is decided in part by the theory report itself** — "whether adaptive = hinted holds
   for any interacting known part is open" against Proposition 11.81(c) (determined for the Curie–Weiss ferromagnet at zero
   field, `0 ≤ βJ ≤ 1`).  The synthesis ranks this over-statement of ignorance second in its §8.
5. **The three new counterexamples of §6 are correct** [replication, all three]: `N_cov = n + 1` with every site non-sharp
   (`n ≤ 12`; proof; the exact threshold is margin `≤ 1/(n−1)`); the Golay/code-landscape bound (`1.0479·10⁻³`, `4096`,
   `R(4) = 0.0559`) — sound, but the explicit instance is an illustration (at `n = 24` it is far below the theorem's own
   `n⁵ε⁻²`); the `p`-biased tail functional (`2.0827` at `(0.2, 2)`, all 65 534 subsets).  The most consequential positive
   fact (the `K`-component sandwich) holds.
6. **All 15 audit scripts re-run with byte-identical outputs** (the synthesis says 14).
7. **The synthesis is faithful in substance and loose in numbers**: "half of the assumptions are `F` or `?`" is a third;
   "499 assumptions" adds 202 assumptions to 297 tags; "ten stale sentences in AA1" are seven; one row of §5 dropped a number
   its source has.
8. **The tree**: at `fc3f5d9` the corrections the synthesis reports as made did not exist (no `APPLIED_CORRECTIONS.md`;
   report and README byte-identical to what the audits read); at `d2150cd` (17:45 UTC) they were applied — 61 of 62, and the
   five worst sentences and Theorem 11.33 are corrected as the audits asked.  I agree with declining the one item (the subtitle).
9. **Our reviews are reported correctly in all five sampled citations.**  Not in the audit: our SCI-REV-0017 (not cited at
   all), the status of our tolerance statement, our machine-checked window lemma for general site classes.
10. **Findings: critical 0, major 5 (F1–F4; the record at `fc3f5d9`), minor 19 (f5–f15, g1–g8)** (§2.4, §3.2, §4, §5).  Sample sizes are small (32 of 513 tags): the rates are
    indications with wide intervals (6/12: 95 % interval 21–79 %), the individual verdicts are not.

---

## 1. The sampling rule and the sample

**Rule, fixed and written into `NOTES.md` at 17:25 UTC before any entry was read.**  Population for a tag `T ∈ {P, F, Q, ?}`
in a report `R ∈ {AA1, AA2}`: every occurrence of the token `{T}` under an entry header (AA1: `### E<k>.` … before `## 4.`,
l.105–1475; AA2: `### Entry <k>` … before `## A.`, l.87–1427), in file order; legends, summaries and count tables excluded
by this mechanical criterion (decided from a listing of line numbers and the first 22 characters of tag-bearing lines only).
Systematic draw: `k = N // m`, start `s = Random(sha256("R23|R|T") mod 2³²).randrange(k)`, indices `s, s + k, …`.
Sizes: `{P}` 6 per report, `{F}` 5, `{Q}` 3, `{?}` 2.  Substitution only if a token is not a tag on an assumption (none was
needed).  The two `{F}` to rebuild: the first two finite computable objects in a seeded shuffle of the ten
(`sha256("R23|rebuild")`): AA2 l.1357 and AA2 l.1114 (no skip).  Five citations of our messages: systematic draw from the
27 occurrences of `SCI-(REV|RES)-n` in AA1, AA2 and the synthesis, distinct messages (`sha256("R23|citations")`).
Script `draw_sample.py`, output `sample.json`, log `logs/draw_sample_20261126T172631Z.log`.

**Population (tokens inside entries; reproduces the audits' own counts exactly).**
AA1: E 52, P 16, C 26, Q 39, X 13, F 47, ? 23 (216).  AA2: E 63, P 62, C 29, Q 28, X 18, F 52, ? 45 (297).

| kind | AA1 (line, entry) | AA2 (line, entry) |
|---|---|---|
| `{P}` | 364 E8; 522 E15; 679 E20; 762 E25; 1115 E37; 1262 E42 | 337 En10; 446 En15; 617 En24; 887 En40; 1099 En56; 1386 En73 |
| `{F}` | 195 E3; 491 E14; 743 E24; 891 E29; 1110 E37 | 352 En11; 606 En23; 931 En43; 1114 En57; 1357 En72 |
| `{Q}` | 498 E14; 927 E31; 1438 E48 | 200 En4; 594 En22; 1233 En64 |
| `{?}` | 768 E25; 1392 E46 | 406 En13; 908 En41 |

Citations: AA1 l.839 SCI-REV-0012; AA1 l.1380 SCI-REV-0006; AA2 l.449 SCI-REV-0016; AA2 l.944 SCI-REV-0003; AA2 l.1071
SCI-REV-0005.

*What the rule does not fix (my choices):* the "most consequential positive fact" (§3.4), the three gaps (§6).
*A property of the rule to keep in mind:* one token = one member, so a double tag `{P}{?}` is two members; four of the twelve
sampled `{P}` have a sibling `{?}` on the same assumption (see §2.3).

---

## 2. The sampled assumptions

### 2.1 Table

"Support found" for `{P}` is classified as the brief asks: **proof** by another route (given or cited) / **check**
(numerical or exhaustive) / **words** / **nothing**.  "TR" = theory report.

| # | rep., entry, line | the assumption (statement) | tag | support found in the audit | what I did | verdict |
|---|---|---|---|---|---|---|
| 1 | AA1 E8 l.364 | pairwise energy in the voxel bridge (§3.4) | `{P}` | **proof**: Lean `voxel_boltzmann_bounds` for any measurable energy | read `VoxelEnclosure.lean` l.33 and `VoxelBridge.lean` l.348: `certified_prodVoxel_partition` is end-to-end "for any measurable energy enclosed voxelwise by two pairwise table models" [V, read only] | **stands** (more exactly a `{Q}`: "enclosed by two pairwise models") |
| 2 | AA1 E15 l.522 | a disconnected family (Theorem 6.1) | `{P}{?}` | **nothing** — the bullet itself says open (TR §12 item 6) | read TR l.979–986, l.11775–11789; our P7.5 gives a connected ring with `⌈n/3⌉ + 1` leaves — no exponential bound | **→ `{?}`** (drop `{P}`) |
| 3 | AA1 E20 l.679 | deterministic procedures in "no instance-optimal algorithm" (Theorem 11.10) | `{P}` | **proof** cited: Theorem 11.23(iii), `((1−2δ)²/8)min(M,N)` [P] (R3, App. B) | read TR l.3239–3248; own sketch gives `≥ (1−2δ)min(M,N)/2 − ½` by "the run on `g_j` follows the run on the hub-less instance until hub `j` is queried" [review, sketch] | **stands** |
| 4 | AA1 E25 l.762 | identical sites (Theorem 11.15) | `{P}{?}` | lower bound: **proof** (tensorises, [V]); upper bound: **nothing** | read TR l.2096–2110 and §12 item 1(a) ("only finitely many types are covered" — for 11.9) | **→ `{?}`** for the theorem (the pair is accurate half by half) |
| 5 | AA1 E37 l.1115 | Harper's theorem (Theorem 11.25(c),(d)) | `{P}` | **proof** cited (inherently typical subsets, R4) + **check** (`n ≤ 4`) | read TR l.3525–3552: the other route gives *exponents* for `ln(1/ε) = o(n)`, not the every-`n` bracket of (c) nor rows 4–6 of the table of (d) | **stands, with that restriction**; it is an ingredient that is a theorem, not a hypothesis |
| 6 | AA1 E42 l.1262 | "an additive true residual (the star then reproduces it)" (Theorem 11.32) | `{P}` | **words** | own LP over the whole class, all evaluation sets [replication]: with `g₀ = −c·C(\|x\|,2)` and `E = e\|x\|`, `N₂ = 3 < K₋ = 4` (`n = 2`), `4 < 8` (`n = 3`), `≤ 5 < 16` (`n = 4`); at `κ = ½` the display fails in 3 of 12 instances (eleven random, one extreme); proof in §2.2 | **→ `{F}{Q}`** — **major** |
| 7 | AA2 En10 l.337 | `4\|B(n, r_ε−2)\|/2ⁿ ≤ δ` (Theorem 11.51) | `{P}` | **nothing** (the step is named) | [review, sketch] a majority vote over the sampled points for the unordered pair of values replaces "the first sampled point"; with `8\|B\|/2ⁿ ≤ e^{−2}` the same `M` gives failure `≤ δ/2` | **stands** (decided here) |
| 8 | AA2 En15 l.446 | the binomial median (Lemma 11.55(b)) | `{P}` | **nothing** | read TR l.5277–5279: any constant lower bound of `P(Bin(m,p_u) ≥ k)`, `k ≤ p_u m`, changes only the constant 2 | **stands**; not an assumption (a cited theorem) |
| 9 | AA2 En24 l.617 | fixed product measure, identical two-letter sites (Theorem 11.63) | `{P}` | **proof** given: Theorems 11.78(b), 11.97(c) | read TR l.7742–7752, l.9239–9250 [read only; not re-derived; 11.97(c) "not refereed beyond the review of 11.101"] | **stands** |
| 10 | AA2 En40 l.887 | `βJ ≥ 0` in Proposition 11.81(c) | `{P}` (+ "`{?}` otherwise") | **words** for why the proof needs it; for survival **nothing** (Conjecture 11.94) | read TR l.7944–7969, row G27 | **→ `{?}`** |
| 11 | AA2 En56 l.1099 | extensive accuracy (Theorem 11.101) | `{P}` (+ "bounded accuracy `{?}`") | **nothing** | read the entry and our SCI-REV-0005 §5 ("bounded accuracy: lower bounds only") | **→ `{?}`** |
| 12 | AA2 En73 l.1386 | stationarity and homogeneity in Theorem 11.116(e) | `{P}` | **words** ("exact sub-/super-additivity") | [review] the reductions (a), (b) are sub/super-additive for every chain; what needs homogeneity is the *limit*: counterexample in §2.2; TR §12 item 14(f) itself says "the brackets become sub- and super-additive processes" | **→ `{F}`** for the limit (`{Q}`: stationary ergodic couplings, unproved) — **major** |
| 13 | AA1 E3 l.195 | triangle inequality (Theorems 2.3, 2.4) | `{C}{F}` | 3-point table; S1(a1)–(a3) | hand check (`d*(y,x) = 2 < 5 = f(x) − f(y)`); S1 re-run identical | **stands** |
| 14 | AA1 E14 l.491 | consistency of the published data (§6.1) | `{F}` | Lean `inconsistentResidual_unguarded`; D15 | read the Lean docstrings (`CertificateAlgebra.lean` l.1069–1092: "Read with exact anchor semantics this is vacuous"; "the exact class is empty") and D15 ("vacuously true"): "minimum 1" is the minimum of the pairwise part alone | **not a counterexample: vacuity → `{E}`** — minor |
| 15 | AA1 E24 l.743 | `β ≥ 0` and the orientation of the coupling (Theorem 11.14) | `{F}` | "R2: 'every β' was wrong" (no object named) | own two-point example [replication]: `g ≡ 0`, `β = −1`, product coupling: `0 ≤ −0.5` false; control `β = +1` holds | **stands** |
| 16 | AA1 E29 l.891 | connectivity as a substitute for reset-closedness (11.18c) | `{F}` | `D = {00, 01, 11}` | [review] `D` contains no rectangle, so the class on `D` is every function (TR l.2518–2521) | **stands** |
| 17 | AA1 E37 l.1110 | two states per site, for "single dips are extremal" | `{F}` | D38, `DEAD.16`, Theorem 11.27 | the two numbers re-evaluated from the displayed formula (`0.02841 < 0.02914`, `k = 4`, `u = 1`); the lower bound itself is the report's [V]+[P] | **stands** |
| 18 | AA2 En11 l.352 | product structure of the reference measure → fact (F2) (Theorem 11.52) | `{F}` | S8 (Curie–Weiss; excess up to 26) | S8 re-run identical; one line by own brute force over 2¹⁶ configurations (`1.6204`, `2.6204u`; control `βJ = 0` → 0) [replication] | **refutes the lemma (F2), not the theorem's conclusion**; the failing *certificate* is workstream N's Proposition N12 (80 of 80), which the entry does not cite; for the statement `{?}` (the audit's own Entry 13) — minor |
| 19 | AA2 En23 l.606 | `q < 1` (Lemma 11.62) | `{F}` | "Entry 1" (`D = X`) | own example on `Q_3` [replication]: constant `ŵ`: `E(ŵ − t)₊ = 12.85 > t·Ξ = 5.43` | **stands** |
| 20 | AA2 En43 l.931 | the stopping rule (Theorem 11.84) | `{F}` | TR l.8296–8305; `DEAD.27`; XX.5 | read TR and the stored harness lines (98 304 > 15 011); 393 216 > 79 931 is our own demonstration (SCI-REV-0003 M1) [read only here] | **stands** |
| 21 | AA2 En57 l.1114 | two letters for "a field always helps" | `{F}` | 11.103(d), `DEAD.24` | **rebuilt** [replication]: own formula `E(π) = min_Q max_φ KL(Q‖π_φ)`, primal–dual to `10⁻⁹`: `0.120196008` for `(0.05, 0.5, 0.45)` > `0.119499092` uniform; control: two letters, 9 fields, none above `p = ½` | **stands** |
| 22 | AA2 En72 l.1357 | non-empty boxes in the adjacency criterion (Theorem 11.115(d)) | `{F}` | Lean `sep_card_le_one_not_sufficient` | **rebuilt** [replication]: all 8 480 pairs of boxes for five `(n,k)`: criterion with the clause wrong in 0, without it in 2 250 | **stands** |
| 23 | AA1 E14 l.498 | exact tables | `{Q}` | Lean `verify_sound_real` | read `CertificateAlgebra.lean` l.960 [V, read only] | **stands**: precise, proved |
| 24 | AA1 E31 l.927 | independent sites, for the closed forms (11.18f) | `{Q}` | "for other laws … a search that contains a minimum-weight hitting-set problem" | read TR l.2848–2890 | **no quantitative condition is stated → `{C}{X}`** — minor |
| 25 | AA1 E48 l.1438 | a uniform constant `c` (Theorem 11.39) | `{Q}` | "a weighted ratio; not stated" | [review] proof in §2.2: one evaluation certifies iff `Σ_{i∈I} c_i ≤ f(y) − f(x̂)` for every `y` that differs from `x̂` exactly on an interval `I` | **stands** once stated; imprecise and asserted in the audit — minor |
| 26 | AA2 En4 l.200 | `ε > ln 3` (Proposition 11.46) | `{Q}` | Proposition 11.57(a) | read TR l.4261–4263, l.5430–5434 ([P], refereed R8) [read only] | **stands**: stated, paper proof on record |
| 27 | AA2 En22 l.594 | one window `[a₀, a₁]` (Proposition 11.61a) | `{Q}` | "`Σ_i max_b KL(a_b^{(i)}‖r_i*)` by the same chain rule (not written)" | [review] immediate; and **machine-checked by this division** for general site classes (SCI-MSG-0014, `ws_L2/Window.lean`, Proposition A1.2 items 1–3), which the report mentions only as "not adopted" | **stands**; the audit under-reports the support |
| 28 | AA2 En64 l.1233 | exact oracle (Theorem 11.109a) | `{Q}` | "a factor polynomial in `1/τ`" (the division's, not checked) | read our SCI-RES-0006 §3: "… polynomial in `1/τ` **and logarithmic in `n` (ingredients checked, not the whole)**"; for the uniform cube our SCI-MSG-0006 Theorem 4-τ is precise (bound divided by `\|C\| ≤ (2n)^{⌈(k_τ−1)/2⌉}`) | **no precise condition, no proof → `{?}`** with a field; cite Theorem 4-τ for the cube — minor |
| 29 | AA1 E25 l.768 | an additive instance (Theorem 11.15) | `{?}` | — | TR §12 item 1; `DEAD_ENDS`; our reviews: nothing decides it | **stands** |
| 30 | AA1 E46 l.1392 | flexible geometry (lever-arm law) | `{?}` | — | no hit in TR, `DEAD_ENDS`, SCI-REV-*.  The audit's own inertia bound (S6(c)) extends verbatim to bond lengths and angles in ranges (triangle width `≥ b_min cos(θ_max/2)`) | **stands** for bending/stretching as moves; the growth of the torsion constants is decidable by the audit's own argument |
| 31 | AA2 En13 l.406 | product reference measure, for the *statement* "adaptive = hinted" | `{?}` ("open for any interacting known part") | — | TR l.7936–7943 (Proposition 11.81(c)) and O4 (l.8086–8091): determined, and equal to the hinted exponent `R_H = R_unif`, for the Curie–Weiss known part with `B = 0`, `0 ≤ βJ ≤ 1` [P; (c) "not refereed in turn"] | **decided in part by the report: does not stand as phrased** — major (it is §8 item 2 of the synthesis) |
| 32 | AA2 En41 l.908 | the two-phase values of Proposition 11.82 | `{?}` | — | Conjecture 11.83 (C1): proved bracket `0.0251012 ≤ R_H(0⁺) ≤ 0.0291391`; our SCI-REV-0001 reproduces the numbers, decides nothing | **stands** |

### 2.2 Statements with proofs or counterexamples

**(S1) Theorem 11.32 without "the true residual is additive" is false; a quantitative substitute [P, proved here; N: LP on
`n ≤ 4`].**  Class `𝒢₂(c) = {g : |D_iD_jg| ≤ c}`, `N₂` the least number of evaluations that certify `min(f + g)` within `ε`,
`K_∓[c′]` the covering numbers of the theorem computed with the constant `c′`.

*Counterexample.*  `n = 2`, `c = 1`, `g₀ = (0, 0, 0, −1)` on `(00, 01, 10, 11)` (`D₁D₂g₀ = −c`: a member), `f = e|x| − g₀` with
`e = 0.1`, so `E = e|x|`, every `ρ₋(y) = 0`, `K₋ = 4`.  The star `{00, 01, 10}` leaves `g′(11) ∈ [−1, 1]`, hence
`E′(11) ≥ 1.2 − 1 = 0.2 > 0 = E(00)`: the minimum is certified exactly with three evaluations, `N₂ = 3 < K₋ = 4`.  For every
`n`: `h = g′ − g₀` has `D_iD_jh ∈ [0, 2c]` and vanishes on the star, so `h ≥ 0` (telescope along a path from the reference),
the star gives the exact lower envelope, and `N₂ ≤ n + 1` while `K₋ = 2ⁿ` for `e < c/n`.  The failure is generic, not a
boundary effect: for residuals `additive + Σ a_ij x_i x_j` with `|a_ij| ≤ c/2` the display `K₋[c] ≤ N₂` fails in 3 of 12
instances at `n = 3` (eleven random, one extreme; 10 of 12 at `|a_ij| ≤ 0.9c`).

*Statement.*  If `|D_iD_jg| ≤ κc` with `κ < 1`, then `K₋[(1−κ)c] ≤ N₂ ≤ (n+1)·K₊[(1+κ)c] + 1`.
*Proof.*  `g − (1−κ)·b_{y,r}` (the dip of Theorem 11.31(a) with constant `(1−κ)c`) is a member, agrees with `g` off `B(y, r−2)`
and is lower by `(1−κ)c·C(r,2)` at `y`: the lower bound of the theorem with `(1−κ)c`.  After stars at `A₀`, `h = g′ − g`
has `|D_iD_jh| ≤ (1+κ)c` and vanishes on the stars, so `|h(y)| ≤ (1+κ)c·C(d_H(y,A₀), 2)` (Theorem 11.31(b) [V] for the
constant `(1+κ)c`): the upper bound with `(1+κ)c`.  ∎  Numerics: 0 violations of the lower bound in 36 instances
(`κ = 0, 0.5, 0.9`); control `κ = 0` (the theorem as stated): 0 violations in 12 + 3.
*Consequence for the audit:* replace `{P}` at AA1 l.1262 by `{F}{Q}`; in the synthesis §2 the side ladder "dense second-order
constants: a quadratic law, cost `2^{n−o(n)}`" is a statement at additive true residuals.  (The README sentence "the
uncertainty left by any set of evaluations grows quadratically with the distance to it" is likewise a statement at an
additive residual: at the boundary member above an unevaluated point can be determined exactly.)

**(S2) Theorem 11.116(e) without homogeneity: the limit need not exist [P, given Theorems 11.98–11.99, the two
reductions 11.116(a), (b) and one number of AA2 S3].**  Take blocks `B_1 < B_2 < …` of lengths `|B_j| = 2^{j²}` (the last block is
all but a vanishing fraction of the chain), coupling `K₁` (flip probability `0.3`) inside the blocks with `j` odd and coupling
`0` on every other bond.  The bonds between blocks carry no coupling, so the chain's law is the product of the blocks' laws
and its site function is the sum of the blocks' site functions at a common `t` (Theorems 11.98, 11.99: one common slope):
`F*_n(t) = Σ_j F*(B_j)(t)`, every term nonnegative and at most a constant per site (cut all couplings of a block by
reduction (a), then the ceiling `t(1−t)D²/8` of Proposition 11.103(f) for each site with its enlarged slope).  A block without coupling has `F*(B)(t) = |B|·F_cube(t) ≤ |B|·0.029139` (`u = 1`).  A `K₁`-block of length `ℓ`
contains `⌊ℓ/13⌋` blocks of 12 sites separated by gaps of one site, which embed exactly (reduction (b)), so
`F*(B)(0.45) ≥ ⌊ℓ/13⌋·13·0.034624` (AA2 S3, `(L, m, t) = (12, 1, 0.45)`, re-run identical).  Hence `F*_n(0.45)/n` tends to at
least `0.0346` along the ends of the odd blocks and to at most `0.0291` along the ends of the even blocks: no limit.  ∎
What survives without homogeneity is the block-local bracket, not "the limit"; for stationary ergodic coupling sequences a
limit would follow from the sub-additive ergodic theorem (not proved in the report; its §12 item 14(f) lists
site-dependent couplings as open: "the brackets become sub- and super-additive processes").  Replacement tag: `{F}` for the
limit, `{Q}`/`{?}` for stationary ergodic sequences.

**(S3) The droplet criterion with site-dependent constants [P, proved here].**  For a nearest-neighbour chain
`f = Σh_i(x_i) + ΣJ_i(x_i, x_{i+1})` with minimiser `x̂` and the envelope `Σ_i c_i[x_i ≠ y_i]`: the single evaluation at `x̂`
certifies the minimum for every residual iff `Σ_{i∈I} c_i ≤ f(y) − f(x̂)` for every interval `I` and every `y` that differs
from `x̂` exactly on `I`.  *Proof.*  By Theorem 2.4 [V, any envelope] the criterion is `d(x̂, y) ≤ f(y) − f(x̂)` for all `y`.
If `y` differs from `x̂` on maximal runs `I₁, …, I_r`, a bond touches at most one run, so `f(y) − f(x̂) = Σ_r [f(y^{(r)}) − f(x̂)]`
and `d(x̂, y) = Σ_r Σ_{i∈I_r} c_i`: the condition for all `y` is the condition for single runs.  ∎  (The "exponential
otherwise" half of Theorem 11.39 is not covered by this.)

**(S4) `N_cov = n + 1` with every site non-sharp — see §3.1.**

### 2.3 Rates

| kind | sampled | stand | do not stand | 95 % interval for "stand" (Clopper–Pearson) |
|---|---|---|---|---|
| `{P}` | 12 | **6** (nos. 1, 3, 5, 7, 8, 9) | 4 → `{?}` (2, 4, 10, 11); 2 → `{F}` (6, 12) | 21–79 % |
| `{F}` | 10 | **8** (13, 15, 16, 17, 19, 20, 21, 22) | 1 lemma-level (18); 1 vacuity (14) | 44–97 % |
| `{Q}` | 6 | **4** (23, 25, 26, 27) | 1 mis-tag (24); 1 unproved sketch (28) | 22–96 % |
| `{?}` | 4 | **3** (29, 30, 32) | 1 decided in part by the report (31) | 19–99 % |

Support behind the twelve `{P}` as found *in the audit*: a proof by another route 4 (plus the lower-bound half of no. 4);
a check 0 (one partial, no. 5); words 3 (nos. 6, 10, 12 — two of them wrong); nothing 4.  **Not one of the two false `{P}`
and none of the four `{?}`-siblings had a proof or a check behind it; every `{P}` that had a proof behind it stands.**
The rule a reader can use: *a `{P}` of this audit is reliable where the entry names the other theorem; where it names only
the proof step, read `{?}`.*

In the population the pattern is visible mechanically: of the 16 `{P}` tokens of AA1, 2 are written `{P}{?}`; in AA2 several
bullets read "`{P}` …; `{?}` otherwise/elsewhere" (l.443–444, 461, 887–889, 1094–1095, 1099, 1387–1388).  These are counted
under P *and* under ? in the synthesis' table.

### 2.4 Findings from the sample

| | class | finding | replacement |
|---|---|---|---|
| F1 | **major** | AA1 l.1262: `{P}` for "an additive true residual" in Theorem 11.32 — the lower bound `K₋ ≤ N₂` is false without it (S1) | `{F}{Q}`: "false if dropped (`n = 2`: `N₂ = 3 < K₋ = 4`, a boundary member; generic for `\|D_iD_jg\| ≤ c/2`); with `\|D_iD_jg\| ≤ κc`, `κ < 1`: `K₋[(1−κ)c] ≤ N₂ ≤ (n+1)K₊[(1+κ)c] + 1`" |
| F2 | **major** | AA2 l.1386: `{P}` for stationarity and homogeneity in 11.116(e) — the limit does not exist without them (S2) | "`{F}` for the limit (two couplings on blocks of rapidly growing length); `{Q}`/`{?}`: stationary ergodic sequences (sub-additive ergodic theorem, not proved); the block brackets of (a), (b) need neither" |
| F3 | **major** | the tag `{P}` is used for three different things — a proof on record that the statement survives, "the proof needs it and nothing is known", and ingredients that are theorems (Harper, the binomial median) — and the synthesis' table adds them up as "required only by the current proof technique: 16 + 62" | in the synthesis §1: split the P row into "another proof on record" and "proof step named, survival not known", or say under the table that P includes the second kind |
| F4 | **major** | AA2 l.406–407 (and A.2 item 1, A.3 item 1; synthesis §2 Level 3, §8 item 2): "whether 'adaptive = hinted' holds for any interacting known part is open" — against TR l.7938–7943 | "open in general (O4); settled [P, 11.81(a),(c); (c) not refereed in turn] for the Curie–Weiss known part without field at `0 ≤ βJ ≤ 1`, where the adaptive exponent without a hint equals `R_H = R_unif`; numerically up to the junction.  So 'adaptive = hinted' is not a property of product measures alone." |
| f5 | minor | AA1 l.491: `{F}` — the Lean example shows vacuity (empty class), not a false bound | `{E}`: "without consistency the soundness theorem is vacuously true and the accepted bound means nothing (`inconsistentResidual_unguarded`: 41/4 on data that no residual satisfies; D15)" |
| f6 | minor | AA2 l.352: the named object (S8) refutes fact (F2); the failing certificate is elsewhere | add "(false certificates: workstream N, Proposition N12)" and "`{?}` for the conclusion of the theorem (Entry 13)" |
| f7 | minor | AA1 l.927: `{Q}` without a quantitative condition | `{C}` for the general statements (any law), `{X}` for the best order |
| f8 | minor | AA2 l.1233: `{Q}` on a sketch, quoted without "and logarithmic in `n` (ingredients checked, not the whole)" | "`{?}` with a field (a sketch of the Scientific Discovery Division, SCI-RES-0006 §3); on the uniform cube `{Q}`: the bound of Theorem 11.25(a) divided by `(2n)^{⌈(k_τ−1)/2⌉}` (SCI-MSG-0006, Theorem 4-τ, [P])" |
| f9 | minor | AA1 l.1438: the weaker condition is not stated | the statement (S3) |
| f10 | minor | AA1 l.1115, AA2 l.446 (and AA2 l.115, l.936 by the same pattern): `{P}` on cited theorems | tag them as ingredients, or move them out of the count |

---

## 3. The three counterexamples of the synthesis §6, and one positive fact

All three were checked with own code or argument **before** the audit's scripts were opened; afterwards the scripts were
re-run and their stored outputs compared with mine.

### 3.1 (a) "Every site non-sharp and yet `n + 1` evaluations suffice" — **confirmed** [review + replication]

*Setting* (TR l.1795–1821, 1887–1929): two-state sites, `f = Σ e_i x_i`, envelope `Σ c_i[x_i ≠ y_i]`, zero residual, `ε = 0`;
`A` is an exact point certificate iff `min_A f − min_y [f(y) − min_{a∈A} d(a,y)] ≤ 0`, equivalently iff `0 ∈ A` and every `y` has
a centre with `d(a,y) ≤ gap(y)`.

*Proof [P].*  (i) For **any** non-sharp two-state sites (`c_i > e_i`), `{0, e_1, …, e_n}` is a fooling set: `0` is covered
only by itself; if a centre with support `T` covered `e_i` and `e_j`, then `i, j ∈ T` would give `c_j ≤ e_i < c_i ≤ e_j < c_j`,
and `i ∉ T` or `j ∉ T` would put a term `c_i > e_i` (or `c_j > e_j`) into the distance.  So `N ≥ n + 1` always.  (ii) If all
margins `c_i/e_i − 1 ≤ 1/(n−1)`, then `y` with support `S`, `|S| = k ≥ 2`, is covered by `e_j`, `j = argmax_S e`:
`Σ_{i∈S∖j}(c_i − e_i) ≤ (k−1)e_j/(n−1) ≤ e_j`.  So `N = n + 1`.  For identical sites the condition is also necessary
(`ρk ≥ k − 1` for all `k ≤ n` iff `c/e ≤ n/(n−1)`).  ∎  The audit's "margin below `1/n`" is sufficient and slightly stronger
than needed.

*Replication* (`item2a_near_sharp.py`, 9.5 s, violations 0): the direct definition for `A₀ = {0, e_i}`, `n = 1 … 12`;
every point of `A₀` covered by itself only (exhaustive over the `2ⁿ` centres); **all** subsets of size `≤ n` by the direct
definition for `n ≤ 4` (2 516 at `n = 4`: none certifies; exactly one certificate of size `n + 1`); exact minimum cover by
integer programming `= n + 1` for `n ≤ 10`; 180 heterogeneous and 180 arbitrary-margin instances.  Controls: sharp sites →
one evaluation; margin `1.1/(n−1)` → `A₀` fails and the minimum is `n + 2` (reacted for all `n = 3 … 10`); margin 1 → minimum
covers `2, 3, 5, 6, 9, 13, 18, 23` (`n = 1 … 8`, above `(6/5)ⁿ`); `A₀` minus a unit vector does not certify.
`R*/margin → W(1/e) = 0.27846`: the synthesis' "about `0.28·(c/e − 1)`" is right.
*Against the audit's S3* [re-run, identical]: the same facts (their margin `1/(2n)`, `n = 2 … 12`).
*What it is a counterexample to:* the summary sentences ("one evaluation or exponentially many"), not Theorem 11.9, whose
hypothesis is finitely many site types fixed as `n` grows; and it is a statement about the certificate size at the zero
residual.

### 3.2 (b) Theorem 11.33(a) without an additive known part — **the lower bound is sound; "false as stated" means "a hypothesis of the source was dropped"** [review + replication]

*The argument, rebuilt* (`item2b_golay.py`, 1.4 s, violations 0).  The extended Golay code from the cyclic `[23,12,7]` code
(generator `x¹¹+x¹⁰+x⁶+x⁵+x⁴+x²+1`): enumerators `1 + 253z⁷ + …` and `1 + 759z⁸ + 2576z¹² + 759z¹⁶ + z²⁴`; balls of radius 3
around the 4 096 words pairwise disjoint (exhaustive marking of 9 523 200 points; control: radius 4 → up to 6 balls per
point).  The dip `c₂·C(r − d_H(x,y), 2)₊` has mixed second differences in `{−c₂, 0, c₂}` (exhaustive on `Q_10`, `r = 2 … 9`;
for `n = 24` by the three cases of a pair of flips; a control profile violates).  With `βc₂ = w/n = 1/6` and `r = 5` (support
`B(y, 3)`, depth `10c₂`): `ln Z` moves by `ln(1 + (e^{5/3} − 1)/4096) = 1.047910·10⁻³`; with a finite penalty `βM ≥ 12` off
the code the shift stays above `10⁻³`.  Theorem 11.22(c) [V, any class and functional] with weights 1 and `B = 1`:
`E|Q(0)| ≥ (1 − 2δ)·4096` for `ε < 1.0479·10⁻³`.  Gilbert–Varshamov family: `R(w) = sup{ln 2 − h(δ) : ln 2 − h(δ) ≤ wδ²/8}`,
`R(4) = 0.0559`.  The audit's S4 gives the same digits [re-run, identical].  The pairwise block family was checked by hand at
one row (`n = 512`, `b = 96`: `βc₂T(r) = 9.1875`, effect `5.725`) and by the threshold `b ≳ 1.115·n^{2/3}`.

*Is the instance inside the class of the theorem as the report states it?*  The statement (TR l.3877–3887) constrains the
residual only (`𝒢₂(c₂)`); in (a) the known part is not mentioned; the chapter's setting (l.1739–1740) gives every instance a
known `f`; the source (`D_REPORT.md` l.489–491) has "`f` additive" [read].  So the instance is in scope **only through the
standing setting of §11**.  The first sentence of (a) itself — "Dobrushin's uniqueness condition holds for every member of
the class … the influence of one site on another is at most `tanh(βc₂/4)`" — is false for a non-additive `f`, which is how
a careful reader recovers the tacit hypothesis.

*Does it contradict (a), or a reading of it?*  **A reading — the one the chapter makes the default.**  Two precisions the
synthesis does not make: (1) **the explicit instance does not contradict "polynomially many" by itself**: at `n = 24`,
`ε = 10⁻³` the theorem's own cost "about `n⁵ε⁻²`" is `8.0·10¹²`, above `2²⁴ = 1.7·10⁷` and far above 4 096 (which is simply the
size of the support); the refutation is the *family* (Gilbert–Varshamov codes, non-explicit; or the explicit block
ferromagnets, `exp(Θ(n^{1/3}))` at `w = 4`, `ε = 1`).  (2) The source theorem (additive `f`) is untouched.
Class: the audit's finding is correct and **major for the report** (a statement defect); the synthesis' wording
"explicit instance" should carry "(an illustration: the refutation is the family)" — minor (**f12**).

### 3.3 (c) "With a `p`-biased measure Hamming balls are not extremal (ratio up to 2.08 on the 4-cube)" — **confirmed** [replication]

`item2c_pbiased_tail_v2.py` (0.9 s, violations 0; exact rational measures, all 65 534 subsets): with
`Ξ(q) = max{Σ_{x∈D} π(x)(e^{u·dist(x,Dᶜ)} − 1) : π(D) ≤ q}` and the ratio "`Ξ(π(B))` over the best Hamming ball of at most that
measure", maximised over the 64 balls: **`2.0827` at `(p,u) = (0.2, 2)`**, `1.4189` at `(0.3, 4)`, `1` at `p = ½` (control,
together with the uniform lemma itself: 0 violations; a deliberately false variant: 149 572 failures); against the 1 310
"balls with type-dependent radii": `1.1230` at `(0.2, 1)`.  The audit's S1 has the same numbers at all 20 grid points, in both columns [re-run, identical].
*Two remarks:* on `Q_4` the balls **are** extremal at `p = 0.4` (all four slopes) and at `p = 0.1` for `u ≤ 2` — "not extremal"
is an existence statement (9 of 16 grid points with `p ≠ ½`); and the verbatim analogue of the lemma ("a ball of the given
measure is itself extremal") fails by up to 46.  *(My first version carried a third ratio that is no notion of extremality;
my own control caught it — error E3.)*

### 3.4 The positive fact I judge most consequential: the `K`-component sandwich — **its argument holds** [review + replication]

It is the audit's only positive statement for multimodal and dependent references (synthesis §3(b), (e)).  *Claim* (AA1 E7):
for `μ₀ = Σ_k w_k μ_k` with product components and bounded differences `c_i`,
`ln Σ_k w_k e^{−βm_k} ≤ ln E_{μ₀}e^{−βΔ} ≤ ln Σ_k w_k e^{−βm_k} + β²Σc_i²/8`, `m_k = E_{μ_k}Δ`.  *Proof:* Theorem 3.1(a), (c) [V] per
component, then sum.  Nothing to referee.  *Replication* (`item2d_mixture_sandwich_v2.py`, violations 0): 1 440 random cases,
no violation; designed control (two modes `Bernoulli(a)ⁿ`, `Bernoulli(1−a)ⁿ`, `Δ = |x|`): the one-average product width fails
in 26 of 30 cases (gap/width up to 7.3), the `K = 2` bracket holds in 30 of 30.
*What should be said with it:* the `K` numbers are averages under the **components** (the decomposition and its weights must
be known; each component sampled); every measure is a mixture of `|X|` point masses, so the content is in a small `K`; the
width is still extensive; a chain is not a small mixture.
*Second candidate, checked by argument:* the inertia bound `≥ 0.0267·m·b²` — holds (three consecutive atoms span a triangle
of least altitude `b cos(θ/2)`; a cylinder of radius `r` cuts their plane in a strip of width `2r`; sum over `⌊m/3⌋` triples).
It bounds the **verified** constants of Theorem 4.6 from below on every domain, not the smallest valid constants.

---

## 4. The synthesis against its sources, and against the tree

### 4.1 Against the two reports (Item 3a)

Read for this: AA1 §§0, 4–10; AA2 §§0, A; `N_REPORT.md` §6 and §4(e); `R_REPORT.md` §0, §12.

| | class | where | finding | replacement |
|---|---|---|---|---|
| g1 | minor | §1, l.47–48 | "Half of the assumptions are either load-bearing in the strongest sense (F: about one in five) or of unknown status (?: one in seven)": `F + ? = 99 + 68 = 167` of 513 tags = **33 %** (the two fractions in the parentheses add up to a third themselves); with E it is 55 % | "A third of the classifications are F or ?; with E, more than half" (the conclusion drawn from it — a theory of its models — stands) |
| g2 | minor | l.19–20, §1 | "202 … 297 classified assumptions"; "499": AA1 counts 202 assumptions carrying 216 tags (its §10); AA2's 297 is a count of *tags* (its §A.7 counts tokens with `grep -o`).  The per-kind columns are tags in both (the AA1 column sums to 216) | "202 assumptions (216 tags) and 297 tags; 513 tags in all" |
| g3 | minor | §7, l.312 | "Stale sentences (ten in AA1, one in AA2)": AA1 has seven (Err-2 … Err-8; its §0 item 3 says "Seven"); ten is the number of its errors | "seven in AA1" |
| g4 | minor | l.26–27, l.276 | "14 scripts": 15 (AA1 seven, AA2 eight); "All scripted, stored, and re-run": three of the positive facts of the last bullet of §6 and the `n + 3` contradiction are arguments in entries (AA1 §9, AA2 §A.5 say so) | "15"; "scripted where a script is named" |
| g5 | minor | §2, Level 5 | "NOT available: any upper bound on the cost of any algorithm for a first-order class", in a level that lists Theorems 11.22–11.24, 11.26 — which contain upper bounds for every finite instance *with the instance as a hint* (11.22(e), 11.23(c), 11.26) | "… any upper bound without a hint, other than enumeration" |
| g6 | minor | §3(g) | "error terms that fall below the exponent itself only at `n ≥ 10¹¹` (a field) and `4·10⁹, 1.7·10¹⁴, 10¹⁹`": the last three are the sizes at which `q·n^{−1/(2q+2)} ≤ 0.05` (`out_s4.txt` l.235–239), a fixed number; and for the `u = 1` cube exponent the first is `4.9·10¹⁴` (l.232) | say which criterion each number belongs to |
| g7 | minor | §5, row 9 | "explicit but large constants", no number; AA2 Entry 17 has it: below the non-adaptive `n·a` "from `n ≈ 2.1·10⁴` on", `e^{142}` at `n = 187`, "Not a competitive design at any size where it can be evaluated" | carry the three numbers into the row |
| g8 | minor | §5, row 10 | "no certified constants at finite `k`": `R_REPORT.md` §12 item 2 says no certified *upper* constants; exact lower bounds exist for the Gaussian pair (the commit `fc3f5d9` itself adds them) | "no certified upper constants" |

**Confirmed** [recount / read]: all 14 counts of §1 and the N column (6/7/6/7/7/3/7); "47 sentences" (22 + 25); "8/10/4" and
"5/11/9"; "264 numbers" (48 + 216); "405 Lean names" [re-run]; every "lost" of §2 has its evidence where cited (S1 A and B,
S8, S2, S3 re-run identical; Entries 15, 19, 25, 26, 55, 57); §5 rows 1–8 have their numbers in the cited places (`n⁵ > 2ⁿ` up
to `n = 22` recomputed; `βΣc_i > 8` recomputed; S7: cube vacuous at `n = 20, 50`, twenty types at `n = 100, 300`; N: `0.197`
for `0.0291`); §4 item 9 (`0.28`) recomputed; §3 quotations of workstream N (Propositions N10–N12: 80 of 80) found.
F4 above applies to §2 Level 3 ("adaptive exponent OPEN"; AA2 A.1 still had "ferromagnetic Curie–Weiss: ≤ cube"), §3(b)
and §8 item 2.

### 4.2 Against the tree (Item 3b) — two facts, with their commits

Read-only git in the local repository (which has the theory commits) and both exports (byte-identical to the git blobs):

| commit (UTC) | `THEORY_REPORT.md` | `README.md` | `docs/audit/APPLIED_CORRECTIONS.md` | `docs/ASSUMPTION_AUDIT.md` |
|---|---|---|---|---|
| `7e6eb4c` 15:44, `b2cf817` 16:02, `020e990` 16:51 (what the audits read) | `41cd501454` | `4455f2db1f` | absent | absent |
| `ff4ad64` 17:07 (synthesis committed) … **`fc3f5d9` 17:19** | `41cd501454` | `4455f2db1f` | **absent** | `c28756b2eb` |
| **`d2150cd` 17:45** ("audits applied: 61 of 62 items") | `337581b52e` | `80b8a754e7` | `eaace4d538` | `c28756b2eb` |
| `ee41735` 17:46 ("seven further qualifications") | `f13723cc91` | `e1ea6ef019` | `eaace4d538` | `c1b16ba2af` |
| **`4aea5fe` 17:50** | `8895abb922` | `e1ea6ef019` | `eaace4d538` | `c1b16ba2af` |

**Fact 1 (true of `fc3f5d9`).**  The synthesis says the corrections "are recorded item by item in
`docs/audit/APPLIED_CORRECTIONS.md`" (l.29–30, l.328–329) and that Theorem 11.33(a) is "corrected" (l.311).  At `fc3f5d9`
that file does not exist and the report and the README are byte-identical to the blobs the audits read.  The sentences
were committed 38 minutes before they became true.  **Major as a matter of record** (a document that describes a state of
the tree that did not exist); no mathematics depends on it.
**Fact 2 (true from `d2150cd`).**  The corrections were applied: 62 items, 61 applied, 1 declined, 0 left to the
coordinator; a section "noticed on the way, not edited" lists eleven further places.  Between `fc3f5d9` and `4aea5fe` the
synthesis itself changed only by a two-line note on line numbers — so g1–g8 hold at `4aea5fe` as well.

**The sentences, old (`fc3f5d9`) and new (`4aea5fe`).**  The synthesis' "worst" list (§7) has four sentences; the first
stands in two files, which gives five places.

| | old | new | is it what the audit asked? |
|---|---|---|---|
| Theorem 11.33 (l.3877–3883; new l.3916 ff.) | "Let `𝒢₂(c₂)` be the residuals on `{0,1}ⁿ` whose mixed second differences are bounded by `c₂`, and `w = βc₂n`.  (a) … Dobrushin's uniqueness condition holds for every member of the class and along the whole annealing path (the influence of one site on another is at most `tanh(βc₂/4)` …)" | "… bounded by `c₂`, let the known part `f` be additive (a sum of site terms; in particular `f ≡ 0`), and `w = βc₂n`.  (a) … Dobrushin's uniqueness condition holds for `f + g`, for every member `g` of the class, and along the whole annealing path — this is what the proof uses, and the class bound gives it because `f` is additive …" + a remark with the code and block counterexamples + row G15 and the closing paragraph qualified + D65 | **yes** (Err-1, E43, O-10).  The remark repeats "for the extended Golay code … at least `(1 − 2δ)·4096`" without saying that this is below the theorem's own polynomial at `n = 24` (§3.2) |
| subclasses, `README.md` 148–150 | "the lower bounds hold at every instance, so no procedure that is correct on a first-order class can be cheap on any of its subclasses, and a cheaper paradigm must say which members it gives up" | "every instance has its own lower bound, which holds for every procedure that is correct on the first-order class, so no such procedure can be cheap at an instance whose own bound is large, in whatever subclass that instance lies (the bound can be small: one evaluation for the minimum at a sharp instance, two at a cone given as a hint, and a class-correct procedure costs `n + 3` on every cone — theory report, Theorem 11.45(d)), and a paradigm that is cheaper there must say which members it gives up" | **yes** (O-1; A.4-1) |
| subclasses, TR l.4579–4583 | "**no procedure that is correct on a first-order class can be cheap on any of its subclasses — a cheaper paradigm necessarily gives up correctness on the first-order class**" | "**no procedure that is correct on a first-order class can be cheap at an instance whose own lower bound is large, in whatever subclass that instance lies — a paradigm that is cheaper there necessarily gives up correctness on the first-order class** (… a subclass can be cheap for a class-correct procedure: the one of Theorem 11.45(d) costs `n + 3` on every cone)" | **yes** |
| the dichotomy, `README.md` 117–119 | "With only a first-order envelope, on product landscapes one evaluation suffices iff every site is sharp; otherwise the number is exponential in the number of non-sharp sites" | "… on product landscapes (independent sites of finitely many types that are fixed as the system grows, and an additive residual that stays strictly inside the envelope) one evaluation suffices iff every site is sharp; otherwise …" (likewise TR §7, row G4, the Reading after Theorem 11.9, "The resulting picture") | **yes** (O-2 … O-6) |
| ferromagnets, `README.md` 358–359 | "A ferromagnetic interaction never makes the problem harder than no interaction, and a shallow barrier is invisible to every exponent." | "A ferromagnetic interaction of this mean-field kind never makes the problem harder than no interaction (a ferromagnetic coupling along the chain can: item (xviii)), and a shallow barrier can be invisible to the exponents: in zero field and at moderate slopes they equal the uniform cube's up to a coupling beyond the critical one — proved as a local statement, numerical beyond that, and at large slopes and small accuracies the junction comes earlier." | **yes** (A.4-2) |
| box cost, TR l.10405–10411 (also l.99, `README.md` 491–494) | "so **the cost of certifying a free energy in a box class is, up to a factor that depends on `ε` and `δ` only and an additive constant, …**" | "so **the cost of certifying a free energy in a box class, with the instance as a hint, is, up to a factor …**"; README: "…, with the instance as a hint, is the Boltzmann factor … (without a hint the worst case is of the order of the Boltzmann factor of the width of the class divided by the square of the accuracy)" | **yes** (A.4-3) |

**The declined item** is O-18, the subtitle "Foundational theory, formal guarantees and certificate paradigms for
fixed-sequence articulated SE(3) heteropolymer chains" (severity C; reason given: it is the programme's name as its owner
gave it; the audit's two observations are stated in the body at l.819–820 and l.4027–4028).  **I agree with declining to
rename.**  The audit's point is about the first screen, and it can be met without touching the name: one sentence in the
"Scope:" paragraph under the subtitle, e.g. "Chains enter through §4.4, §§11.14–11.15, 11.17, 11.22 and 11.32; the exponents
and thresholds of §§11.4–11.10 are for independent sites; the group `SE(3)` itself is not defined in the Lean development."
(minor, **f13**).

Not reviewed, as instructed: the other 55 applied items, the "seven further qualifications", the eleven "noticed on the
way", and the later commits (`87167c0`: our SCI-REV-0017 applied; `b4fb594`: Theorem 11.53a).

### 4.3 Coverage (Item 3c) — a list, not a judgement

Mechanical (`item3c_coverage_v2.py`): **all 153 statement numbers of the report's own numbering** (majors 2, 3, 4, 6, 11;
R4.1, R4.2) **are named in an audit — none is missing.**  The report at `fc3f5d9` has no numbered Theorem, Lemma,
Proposition, Corollary or Conjecture in §§7–10, 12, 13; nothing follows §11.32 except §§12–13; there is no appendix (the
last section is "13. References").  Not audited *as statements*:

* §7 (what the theory implies for architectures and samplers), §8 (limitations), §12 (items 1–14), §13 — used as evidence
  and in the overstatement lists only; §12 items 7 and 12 are not cited as such by either audit;
* §9 (index of machine-checked statements): AA1's S7 cross-checks the Lean names cited in §0.2, §§2–6 and §§11.1–11.15; the
  names cited in §§11.16–11.32 and the index itself were not cross-checked;
* §10: rows G1–G17 are in AA1 by row; of G18–G40, **19 rows are cited by row label in neither audit** — G18, G20, G21, G22,
  G24, G26, G27, G29–G40 (their theorems are in AA2's entries; the row texts with their prior-art and status cells were
  not checked row by row; AA2 works from the rows of §0.3);
* statements of this division quoted under their own numbers and named in neither audit: Theorem R9.1 (adopted as
  Proposition 11.69b, audited there, "(f), (g) read only"), Proposition R13.1, Theorem R6.1 and Corollary R6.2,
  Propositions R16.1 and R10.1 (inside remarks that Entries 12, 18, 74 cover), Conjecture R10.3 (§12 item 14(b); not covered);
* the tables of `N_REPORT.md` §6 and `R_REPORT.md` §9, which the synthesis uses as sources, were not audited by AA1/AA2;
* new at `4aea5fe`, audited by nobody: Theorem 11.53a, row G41, the remark after Theorem 11.33 (labelled "[P/N: audit AA1]").

---

## 5. Our reviews against the audit (Item 4)

### 5.1 Five sampled citations — all five report our finding correctly [read both sides]

| | citation | what the audit says | what our message says | verdict |
|---|---|---|---|---|
| 1 | AA1 l.839, SCI-REV-0012 | "11.18a, 11.18d reviewed by the Scientific Discovery Division (SCI-REV-0012, -0013)" | -0012: "every part of Theorem 11.18a and Propositions 11.18b, 11.18c re-derived … everything is correct except two statements of Proposition 11.18c"; -0013: "Theorem 11.18d as written: says what is machine-checked, with three small exceptions" | correct |
| 2 | AA1 l.1380, SCI-REV-0006 | lever-arm law: "wording corrected by SCI-REV-0006, -0009" | M4/W6; our own later corrections (SCI-RES-0007 §2, SCI-REV-0009 §2): "what remains of M4 is the wording of Theorem 11.36" | correct (and consistent with our retraction of M4 as a sharpening) |
| 3 | AA2 l.449, SCI-REV-0016 | the abort test before every query: "'the previous wording … proves `C_max + M̄`, not `C_max`' (… corrected three times: R7, R8, SCI-REV-0016)" | m1, in these words | correct.  **But the bullet carries `{F}`**, and our m1 ends: "No run exceeding `C_max` was constructed; none among the 2 648 stored runs".  The evidence is a gap of a proof, with a weaker bound proved: a `{Q}` (`C_max + M̄`), not a counterexample — minor (**f11**) |
| 4 | AA2 l.944, SCI-REV-0003 | the sentence on rounds is "for a fixed `η`; the restriction follows … (added after SCI-REV-0003)"; l.923: "one major finding (the stopping rule), nine minor" | m1; "No critical finding, one major, nine minor"; 393 216 against 79 931 | correct |
| 5 | AA2 l.1071, SCI-REV-0005 | Theorem 11.99: the ranges, the worst case, the exponential scale "for the operational sentence (added after SCI-REV-0005 m1)" | m1: "the range and mode of the dictionary sentence"; "a statement about the hardest instance" | correct |

### 5.2 The reverse: findings of ours about an assumption or a finite-size limit that the audit does not have

| section | finding of ours | in the audit? |
|---|---|---|
| §11.19, Theorem 11.58a | SCI-REV-0017 §5: the formula is above the non-adaptive `n·a` up to `n = 2.04·10⁴` at `u = 1` | **in AA2 Entry 17** ("from `n ≈ 2.1·10⁴` on", from the report's own l.5615) — missing only from the synthesis §5 (g7) |
| | SCI-REV-0017 as a whole | **not cited anywhere in AA1, AA2 or the synthesis** (sent 15:52 UTC; the audits closed at head `b2cf817`, 16:02; the synthesis is of 17:07).  Missing with it: the `O(1)` of a slope step is `31, 39, 60, 178` nats at `u = ½, 1, 2, 4` (m3); the condition `x̂ ≥ X₀(n)` of a slope step, 13.7 nats at `u = 1`, `n = 470` (m2); the class of randomised algorithms over which `N` ranges (m8); the approach to the limit — `0.7072, 0.3713, 0.2731, 0.2637` of `n·a` at `n = 6.4·10⁴, 10⁶, 10⁸, 10¹⁰` against `h/a = 0.2627`; "every hypothesis in it is the cube with one slope and no known part, and nothing is known about which of them the proof needs" |
| §11.19, remark (1a) | SCI-REV-0007 (linked note): `1400, 540, 4700` are first sizes of a grid, the inequality is not monotone near the crossover (failures up to `1398, 538, 4566`); "from … on" is observed, not proved | Entry 18 quotes the three sizes without the caveat (it does not claim "from … on" either) |
| §11.19, Theorem 11.56 | SCI-REV-0016 m1: no run exceeding `C_max` was constructed | Entry 15 tags the rule `{F}` (f11) |
| §11.26 | SCI-REV-0005 §5 and SCI-MSG-0014: a **non-adaptive upper bound at bounded accuracy for every `n` on heteropolymer landscapes** (our Proposition A1.2; items 1–3 machine-checked in `Window.lean`) | **no**: Entry 36 says "at bounded accuracy only Proposition 11.61a (a field) has an upper bound"; Entry 22 mentions our version as "not adopted"; A.1 Level 2 has nothing at bounded accuracy |
| §11.26 | M1, M2 (uniformity of `ω_n` in the composition; the transferred induction), "never simulated", "the evaluation count of Theorem 11.52 inherited" | yes (Entries 52, 56) |
| §11.30 | SCI-REV-0015 m10: the nested sandwich (11.113a) is narrower than the plain one at equal evaluations iff `2√(N/N_f) + ρ̄ < 0.878` — never for `ρ̄ ≥ 0.88` | **no** (Entry 69 calls 11.113a "the most usable statements of the part" without the range) |
| §11.30 | SCI-REV-0015 m11: Proposition 11.113(d) needs `ε ≤ ½ ln((e^Δ + 1)/2)` and `ε ≪ (1 − e^{−Δ})/4` besides the fine-grained sampler | one of three (Entry 69 has `Σq² ≪ ε²/sinh²(Δ/2)`) |
| §11.30 | SCI-REV-0013: 11.110(e) holds without "no single state can change `ln Z` by `ε`" (two-stage check); `ε ≲ 1`; 11.113a(c) needs `N_f` fixed in advance (SCI-REV-0015 m7); the floor distance is extensive (`10–56`, `30–243`) | yes (Entries 66, 69) |
| §11.32 | SCI-REV-0010 M1 (the direction turns with the slope); association for the variance law; the symmetric envelope; computed cells only | yes (Entries 73, 74) |
| §11.32 | SCI-REV-0010 §2: finite chains are indicative and no more — the last increment at `(p,u) = (0.1, 1)` is `0.991` of the cube although `a_∞ ≥ 1.05×` cube is proved | only as "nothing is uniform in `n`" (Entry 74) |
| §11.32 | SCI-REV-0010: "Y3 does not need `d⁻ ≥ 0`" | not there; consistent with Entry 73's "`{E}` a non-empty reduced class" |
| §11.29 (not in the brief's list) | SCI-RES-0006 §3: the tolerance statement is "ingredients checked, not the whole", and logarithmic in `n` | quoted without both (f8) |

Class: all minor.  Replacement texts: (**f14**) Entry 17 — add "reviewed (SCI-REV-0017): proved as stated, given Theorem 11.56; the
`O(1)` of a slope step is 31–178 nats"; (**f15**) Entry 36 — "at bounded accuracy an upper bound exists for a field (Proposition
11.61a) and, by the Scientific Discovery Division's Proposition A1.2 (unrefereed; items 1–3 machine-checked), for product
landscapes with site types"; (f11) Entry 15 — `{Q}` for "every query" (without it the proved bound is `C_max + M̄`; no violating
run is known).

---

## 6. Three gaps, each with a question that can be sent as it stands

I agree with the synthesis that items 2, 3 and 6 of its §8 are where the theory stops being about anything but its
models — independence, the accuracy scale, fixed site types — and I disagree with the wording of item 2 (F4).  Item 1 of
its §8 (non-additive instances) is in part closed by a sandwich of the kind of (S1): at a `κ`-interior instance the
additive theory holds with the constants `(1 ∓ κ)c` [V for first order: `slack_ge_of_lipschitz`; (S1) for second order].

**Gap 1 — a product reference measure in the adaptive upper bounds (interacting known parts).**  *Status:* `{F}` for the
proof, `{?}` for the statement; settled [P] for one family that is a positive mixture of field-tilted product measures
(Proposition 11.81(c)).  *Why it matters:* every physical known part couples sites.  *The smallest question:*
> **Q1.**  Let `π_n(x) ∝ exp(−n(b/2)(2|x|/n − 1)²)`, `b > 0` (the antiferromagnetic Curie–Weiss known part without field —
> its sites are negatively correlated, so it is not a positive mixture of field-tilted product measures), the class `L_u(Q_n)`, `0 < ε₁ < E`.  By row G27 of the theory report the
> hinted exponent at symmetric instances is at most the uniform cube's "with equality for every interaction without a
> field up to the junction (antiferromagnets included)": `R_H = R_unif`.  **Prove or refute:** there is an adaptive algorithm
> without a hint with cost `exp(n·R_unif(ε₁) + o(n))`.  A first step that is a computation: the class-relative influence
> `ι(u, b, φ) = sup_{ψ ∈ L_u} max_{a ∼ a′} |ln W_ψ(a) − ln W_ψ(a′)| − u` between an outer block of `φn` sites and the rest
> (audit S8 computes one member, `γ|b| ± u|a|`, and finds an excess of `0.3–0.6·u`, stable in `n`); is `ι/u` bounded away from
> zero as `n → ∞` for every split `φ`, and does it vanish as `φ → 0`?  With Theorem N4 of workstream N (under review) a bounded `ι` gives a
> valid nested algorithm at the slope `u + ι`; the question is whether that loss is real.
A positive answer makes "adaptive = hinted" a statement about a known part with no product structure in any disguise; a
refutation would be the first separation.

**Gap 2 — extensive accuracy below Level 0.**  *Status:* `{P}` with `{?}` (no. 11 of the sample; Entries 16, 25, 56, 73).  *Why it
matters:* the accuracy one would use is a fixed number of `k_BT` for a growing system; every adaptive statement with a known
part is at an accuracy proportional to `n`.  *The smallest question* (the simplest non-uniform case):
> **Q2.**  For the `p`-biased cube (`π = Bernoulli(p)^{⊗n}`, `p ≠ ½`), the reference instance `H` and its Gibbs law `μ_H`,
> define the lower tail functional `Θ_H(q) = min{Σ_x μ_H(x)e^{−s_H(x→S)} : μ_H(S) ≥ q}` next to the upper one `Ξ_H(q)` of Lemma
> 11.62.  **Prove or refute:** there are `θ`, `c > 0` and `C`, depending on `(p, u)` only, such that
> `Ξ_H(q) ≤ θ·n^C·Θ_H(c·q)` for all `n` and all `q ≥ exp(−n(a_p + o(1)))` — the analogue of Lemma 11.55(b), (c), which is what
> Theorem 11.56 uses of the uniform cube (workstream N, table row 9, states the need in this form).
> As a computation to start from: both functionals exactly over all 65 534 subsets of `Q_4`, and — as lower bounds of `Ξ_H`
> and upper bounds of `Θ_H` — over balls with type-dependent radii around the two poles for `n ≤ 2000`, for `(p, u)` on the
> grid of audit S1; report the ratio and its maximisers.
With it, the bounded-accuracy theorem (11.58) transfers to a field; without it, Levels 1–2 say nothing at the accuracies
one would use.

**Gap 3 — site types fixed as `n` grows, and homogeneity along a chain.**  *Status:* `{P}` in several entries (E49, En73 —
the latter wrongly, F2), `{?}` for a number of types that grows with `n`.  *Why it matters:* a real sequence has about as
many distinct sites as it has sites.  *The smallest questions:*
> **Q3a.**  In Theorem 11.97(c) the error is `ω_n ≤ q_max·n^{−1/(2q_max+2)} + c·n^{−1/4}` for `n ≥ n₀`, with `c, n₀` depending on
> `(m, q_max, D_max, π_min)`, and `ln N_orb ≤ m(q_max − 1) ln(n + 1)`.  **Make `n₀` and `c` explicit in the number `m` of site
> types and state the corollary for `m = m(n)`:** for which growth does `ω_n → 0` (the displayed terms suggest
> `m = o(n/ln n)`)?  Then say whether Theorem 11.101(b), whose uniformity statements (G1), (G2), (L) are over compositions of
> finitely many types, holds along such sequences.
> **Q3b.**  For a nearest-neighbour chain with arbitrary couplings `|K_i| ≤ K̄` and slopes `u_i ≤ ū` (no stationarity),
> **state Theorem 11.116(e) without a limit:** for every partition into blocks `B_j` (with the gaps of (b)),
> `Σ_j F⁻(B_j)(t) ≤ F*_n(t) ≤ Σ_j F⁺(B_j)(t)` and `F⁺(B) − F⁻(B) ≤ C(K̄, ū)·t` for every block — and add that `F*_n/n` need not
> converge (two couplings on blocks of lengths `2^{j²}`, §2.2 (S2)), and that it does for stationary ergodic sequences, if that is proved.

---

## 7. What I did not check; my own errors; files

**Not checked.**  The other 481 tags (the sample is 32 of 513).  Of the audit's scripts: all re-run, but only AA1's S3, S4
(parts A–C) and S2 (part D), and AA2's S1 (test A) and one line of S8, were replicated with own code; AA1's S1, S2 (parts
A–C), S5, S6, S7 and AA2's S1 (test B), S2–S7 are re-run only.  No Lean file was compiled (statements read: `VoxelEnclosure`, `VoxelBridge`, `CertificateAlgebra`,
`BarrierCertificate`); `lake` was not run; the harness was not re-run (its stored output was read).  Paper proofs cited as
support and not re-derived: Theorems 11.78(b), 11.97(c), Proposition 11.57(a), R3's Appendix B (sketched only), the
"inherently typical subsets" route, Proposition 11.81(a), (c) (read; its status is the report's).  (S2) rests on the
report's Theorems 11.98–11.99 and 11.116(a), (b) and on one number of AA2 S3 — I did not compute a chain exponent.  The block
ferromagnet counterexample: one row by hand.  `N_REPORT.md` and `R_REPORT.md`: read in part (N §§0, 4(e), 6; R §§0, 12), not
reviewed.  At `4aea5fe`: only Theorem 11.33, the five places of §4.2 and the record's head, declined row and counts.  The
theory report's Theorem 11.101 was not read (verdict no. 11 rests on the audit's own words and on our SCI-REV-0005).
No prior-art search; no web search was used.  For nos. 2, 4, 10, 11 I made no attempt beyond reading the statements: each is
an open problem by the report's own account (§12 items 6 and 1(a); Conjecture 11.94; "upper bounds at bounded accuracy"),
not something twenty minutes decide; they stay `{?}`.

**My own errors** (all recorded in `NOTES.md` when they happened).
E1, E2: two section headings of my notes carried times that were estimated instead of read from the clock (5 and 8
minutes off); corrected; from then on every heading is produced by `date -u` inside the command.
E3: `item2c_pbiased_tail.py` (v1) carried a third ratio that is no notion of extremality (4 for the uniform measure); my
control caught it (4 violations in the v1 log); v2 drops it; the two other ratios were unaffected.
E4: `item1_thm1132_additive.py` (v1) stopped on an assertion (HiGHS reports an unbounded LP with free variables as
"infeasible"); log in `not_cited/`; v2 asserts feasibility of the true residual and treats both statuses as unbounded.
E5: `item2d_mixture_sandwich.py` (v1) had a control that could not react (0 failures on random instances); v2 has a designed
family.
E6: the brief speaks of "the five overstatements the synthesis calls the worst"; the synthesis lists four sentences; I
report five places (one sentence stands in two files) and say so, rather than choosing a fifth sentence myself.
E7: the population of the draw is tag tokens, not assumptions, so `{P}{?}` double tags entered the `{P}` sample as `{P}`; this
is a property of the rule I fixed, reported in §1 and §2.3, not corrected after the fact.
E8: my first version of (S2) used dyadic blocks and silently needed the report's bracket `[0.0401, 0.0450]` to be narrow
(`2F⁻ − F⁺ > F_cube`); rewritten with blocks of lengths `2^{j²}`, which needs only `0.0346 > 0.0291`.
E9: a third unclocked time ("at about 18:40") in a line of the notes; removed at once.

**Tool actions declined:** none.

**Files** (all in `experiments/science/ws_R23/` except this report).
`NOTES.md` (running log from 17:24 UTC); `HANDBACK.md` (the text of the hand-back); `shape_recon.py`; `draw_sample.py`, `sample.json`;
`item2a_near_sharp.py`; `item2b_golay.py`; `item2c_pbiased_tail.py` (v1), `item2c_pbiased_tail_v2.py`;
`item2d_mixture_sandwich.py` (v1), `item2d_mixture_sandwich_v2.py`; `item1_thm1132_additive.py` (v1),
`item1_thm1132_additive_v2.py`; `item1_thm1132_quantitative.py`; `item1_rebuild_F_two.py`; `item1_s8_owncheck.py`;
`item3c_coverage.py`, `item3c_coverage_v2.py`; `rerun_audit_scripts.sh`;
`logs/` — cited logs, each reached its last line: `draw_sample_20261126T172631Z.log`, `item2a_near_sharp_20261126T173333Z.log`,
`item2b_golay_20261126T173451Z.log`, `item2c_pbiased_tail_20261126T173538Z.log` (v1: END reached, 4 control violations, E3),
`item2c_pbiased_tail_v2_20261126T173615Z.log`, `item1_thm1132_additive_v2_20261126T174317Z.log`,
`item1_rebuild_F_two_20261126T175119Z.log`, `rerun_audit_20261126T175609Z.log`, `item1_s8_owncheck_20261126T180027Z.log`,
`item2d_mixture_sandwich_20261126T181040Z.log` (v1: END reached, control did not react, E5),
`item2d_mixture_sandwich_v2_20261126T181110Z.log`, `item3c_coverage_20261126T181619Z.log`,
`item3c_coverage_v2_20261126T181702Z.log`, `item1_thm1132_quantitative_20261126T182132Z.log`;
`not_cited/item1_thm1132_additive_20261126T174301Z.FAILED.log`;
`rerun_copy/` (scratch copy of the audit's 15 scripts, their stored outputs, a copy of `docs/THEORY_REPORT.md` and `proofs/`
for `aa1_07`, and the re-run outputs — not to be committed).
To re-run everything of mine: `OMP_NUM_THREADS=1 python3 -I -B <script>` from `ws_R23/` (each under four minutes, under
0.5 GB); `bash rerun_audit_scripts.sh` (3.5 minutes).
