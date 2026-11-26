# Workstream R9 — running notes

(started 2026-11-25 23:33 UTC; one entry per step; newest at the bottom.  Clock times are given only where I read
the clock — `date -u` or `uptime` — at that step; an earlier version of this file carried times for steps 6–10 that I
had estimated without looking, about an hour too late; they are replaced by step numbers.)

## Conventions

* EXPORT = `/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_658b77f`
  (theory tree at `658b77f`, read-only).
* OURS = `/home/user/MetricChain` (science branch, built on theory `5ed4072`).
* Labels: **re-derived** (I did the mathematics myself), **re-computed** (my own code),
  **re-ran** (someone else's code, named), **read** (only read).

## Log

### 23:33 — start
* Read `COMMON.md` and `R9_brief.md` in full.
* Created `experiments/science/ws_R9/`.  No state-changing git command will be used.

### about 23:35 — first reading (read only)
* Read in full: EXPORT `docs/collaboration/responses/theory/THY-RES-0007.md`, `THY-MSG-0013.md`;
  OURS `SCI-REV-0003.md`; EXPORT `docs/THEORY_REPORT.md` §11.24 (lines 6402–6784) and §11.22
  (lines 5099–5735); EXPORT `experiments/coordinator_checks/limit_shape_review/{README.md,
  t4_semigroup.py, out_t4_semigroup.txt, mylat.py, concat_check.py, concat_check2.py}`;
  OURS `A2_REPORT.md` §§A2.2, A2.3, 4.6–7 (lines 120–230, 566–767), `ws_R2/README.md`, `r2_enum.c`.
* §11.24, Lemma 11.85 for `r` rounds (rewritten for m3): **re-derived**, the new proof is right
  (the event `Ẽ_1∩…∩Ẽ_{t−1}∩Ẽ_t^c` is contained in {virtual batch `t` has ≤ `M_t` points} ∩ `Ẽ_t^c`,
  and the virtual batch `t` is a function of coins and `s¹..s^{t−1}`, so the union bound is legitimate).
* §11.22, Prop 11.69a: **re-derived** line by line; first display correct (some `k_i ≥ 1` because
  some `λ_i ≥ 1/(d+1)` and `M ≥ (d+1)m`); second display correct with `m = ⌈√(βM/A)⌉`,
  `A = (d+1)(β′+R)`: `β/m + A m/M ≤ 2√(βA)/√M + A/M`.  `c = 2√(60·5·64) = 277.13`.  Their statement
  is ours (A2.2) with the rounding made explicit (ours said "up to rounding") — slightly sharper.
* §11.22 packing condition `L‖p_k−p_l‖_c > e(g_k+g_l) + 2ε₁ + max(L,e)(d_k+d_l)`: **re-derived**, sufficient.
* §11.22: four exact points on the hyperplane `g = 9p₃ − 3p₈ + p₁₁`: checked by hand; dual norm of
  that functional w.r.t. `‖·‖_c+|g|` is 2.4, so the "uncertainty 0.02" = 2.4·168/22354 = 0.018 ✓.

### about 23:40 — item 4: definition of "clean" extracted from their script; own code written
* Their test `in_S(x)` (t4_semigroup.py): `dg == 0` (b′ up) and `A_part == 0` and `B_part == 0`,
  where A/B are the cross counts of the three linker sites above / below against the bridge **minus
  the chain neighbours** (1 bond, 2 second neighbours).  THY-RES-0007's wording "no pair within the
  cutoff between the three linker sites … and the chain" read literally is never satisfied (the
  linker site is bonded to the end bead) — the definition needs "at chain separation ≥ 3".
* Wrote `r9_semi.c` (own code, from the Setting paragraph + statement of Lemma 11.68; R2's
  `r2_concat.c` not opened).  Precise definition in the header comment of the file.
* Small run (`out/semi_small.txt`, N ≤ 11, all pairs N₁,N₂ ≤ 9): my counts of clean bridges per N
  (first two bonds fixed) 1, 2, 4, 10, 24, 64, 159, 420 = theirs/4 (4, 8, 16, 40, 96, 256, 636, 1680) ✓;
  class counts 1,2,3,5,8,16,28,43,64 = R2's tables ✓; 69 696 ordered pairs: additive, clean, bridge ✓.
* Launched (background): `r9_semi 22 0 20 out` (per-bridge tests, class tables N ≤ 22) and
  `r9_semi 13 13 0 out 0 2` (all pairs N₁,N₂ ≤ 13, part 0 of 2).

### about 23:52 — §11.25 (slices) read in full in the export (lines 6785–7280); SCI-REV-0001 read in full
* Remark after Lemma 11.89 (our four-line proof as they wrote it): **re-derived**.  `S = d₊/g₊² + d₋/g₋²`
  with `d₊+d₋ = 1`; `(d₊+d₋)(d₊/g₊²+d₋/g₋²) ≥ 8 + 4(g₊/g₋+g₋/g₊) = 16cosh²(ω/4)` ✓; `F′ = s`, `F″ = S/4`,
  `Ψ″ = 4/S ≤ ¼ sech²(s/2)` ✓ (c = ℓ/2 checked against the four cells).
* Theorem 11.90(a) at negative accuracies (M2 repair as written, lines 7003–7023): **re-derived**.
  Chain: strong duality for a profile with `e + MI(μ) > 0` (Slater point `ν = μ`); for fixed `(t, ξ)` the
  linear functional on the polytope {laws on supp ρ, mean κ, `E KL ≥ −e`} is maximal at a vertex; vertex
  has ≤ 3 atoms, 3 only if the inequality is active ⇒ budget 0 ⇒ `r = −e`; weak duality at the vertex;
  ⇒ `r_μ(e) ≤ max(R^{κ,(2)}(e), −e)`; `R^{κ,(2)}(e) ≥ −e` by the shell `F = −e` of the centre `m = κ`
  (`F(ℓ_max) = h(κ)` there, checked).  No gap found.  `MI ≤ h(κ)` ⇒ no feasible profile for `e < −h(κ)` ✓.
  For `N^κ`, `X ≥ 0`: all profiles feasible; at `X = 0` Slater can fail but the value function is closed
  convex on a compact domain, so no duality gap ("read sup for max") ✓.
* Theorem 11.90(b) for `e < 0` (m4): re-derived (value `−e` for `e ≤ −F(ℓ*)`; game form max at `t = 1`) ✓.
* Theorem 11.90(c) strictness (m6): re-derived ✓ (both sides `−e` on `−h(κ) ≤ e ≤ −K(u/2)`).
* Corollary 11.91 proof at `e′ = e + (I−λ)(κ)`: the case "feasible at e′ but not at e" handled
  (`r ≤ MI(μ) < −e ≤ R^κ(e)`) ✓.
* **Item 2(a)**: Prop 11.81 read in the export (lines 6107–6178) and in OURS at 5ed4072 (5378–5399),
  and at 89ac710 / 40c5bd7 / dcdfea6 via `git show`.  (i) At 5ed4072 Prop 11.81(b) already says
  `R_H < R_unif` beyond the junction for `B = 0` (0.0251012 at βJ = 1.5, u = 1, e = 0) — so the clause of
  OUR replacement text for M1, "without a field these two exponents are the uniform cube's", was too
  strong: it needs "and with one phase".  **Their amendment (a) is right; the slip is ours** (R1's own
  §5.4(A) had the qualifier "If I is symmetric and convex"; the replacement text dropped it).
  (ii) Prop 11.81(c) was "a sketch" with a named missing step at 5ed4072 and 89ac710 (the two versions
  R1 reviewed) and became [P, given Thm 11.64] at 40c5bd7 (referee's completion).  So R1's "the only
  proved bounds are …" was correct for the reviewed text and outdated at 658b77f: **amendment (b) right**.
  I re-derived the completion (HS mixture; `A_y(ψ) = C_n·A_{y_j}(ψ − 2(y−y_j)|x|)` ✓; finite net ⇒
  uniform o(n) ✓); it rests on Thm 11.64 and Prop 11.65(b), which I did not check, and on the cost of
  Thm 11.64 being sub-exponential in ln(1/δ) (δ is divided by ~n² grid fields) — not stated there.

### step 6 (about 23:57, 25 Nov) — item 4 computations, first results (all **re-computed with own code** `r9_semi.c`)
* `out/semi_enum22.txt`: all bridges with 3..22 beads (first two bonds fixed; 92 121 332 at N = 22; my totals and
  class counts = R2's `enum_bridge.log`, and `r9_semigroup_analysis.py` (1): my class tables = R2's tables
  (profiles and gauche masks) for N = 3..22).
  - head 5 + tail 5 (their claim (2)): every one of the 21.5 million (bridge, c₁) with N ≤ 20 becomes clean; no failure.
  - head 2 + tail 3 already suffices (0 failures, N ≤ 20) — and is minimal: head 1 + tail 3 fails (first at N = 8,
    2 cases), head 2 + tail 2 fails (first at N = 12, 4 cases; 1308 at N = 16 — corrected in step 10, I had first written
    "first at N = 16"), head 0 fails, tail 0 fails.  Total (x, c₁) with N ≤ 20: 21 220 319.
  - cost of head+tail = A + B (asserted for every case with head ≥ 3, tail ≥ 3); componentwise maxima up to N = 20:
    (1, 8, 12, 1), norm 51 (N = 18); A-part max (1,6,10,1 | 44) at N = 21, 22; B-part max (0,3,4 | 16) (= proved bound).
  - 18.8 million from-scratch profile checks of the incremental counts; 18 364 O(n²) brute-force checks.
* `out/semi_pairs13_part{0,1}.txt`: **all 160 326 244 ordered pairs of clean bridges with N₁, N₂ ≤ 13** (12 662 clean
  bridges) concatenated from coordinates: every concatenation is a self-avoiding lattice walk, a bridge, has
  (h,g) exactly additive and is clean.  0 failures of any kind.  (Claim (1) of the sketch.)
* `out/semigroup_analysis.txt`: (2) set-level closure of the clean classes `C_{N1} + C_{N2} ⊂ C_{N1+N2+3}`: 24 913 sums,
  0 missing; the same for ALL bridges fails (79 of 47 038 sums missing; first: rod(3) + (2,7,7;6) at N = 11) — so the
  restriction to clean ends is needed for exact additivity of (h,g) itself.  (3) the clean bridges with N ≤ 10
  generate Z^5 (as (h,g;N+3)) and Z^4 (as (h;N+3)): index 1.  (4) counts: #P_N/N³ = 0.152 (N = 22), 0.170 (N = 24, R2's
  table) — against vol K ≥ 1.56; local growth exponent 4.2–4.4 at N = 21..24; holes of conv(P_N): 8–10 % of its lattice
  points, none deeper than 0.93 (Euclidean) inside the hull for any N ≤ 24.
* New observation (mine): the error of Lemma 11.68 is a **coboundary**: with c(x,c₁) = A(x,c₁) + B(x),
  δ(x¹,x²) = c(x¹) + c(x²) − c(x¹∘x²), because the concatenation inherits B from x¹ and A from x².  So
  q̂ = (h,g) + A + B is exactly additive for ALL bridges.  Wrote `r9_cobound.c`; N ≤ 9: 142 129 pairs, 0 failures;
  N ≤ 13 launched in two parts.
* Consequences worked out by hand (to be written in the report): (h,g)(x)+A+B)/(N+3) ∈ K^br exactly for every
  bridge; one-sided rate 168/(N+3) → 108/(N+3) (the two error vectors are componentwise nonnegative and enter
  with opposite signs); without coordinates every bridge has a point of K^br within 30/(N+3) of ((h,g)+m)/(N+3),
  m = (½, 9/2, 7; ½).
* Scratch copies of `Scattering.lean` (exit 0; 8 declarations, axioms [propext, Classical.choice, Quot.sound]) and
  `TwoRoundsExpected.lean` checked with `lake env lean` (outputs in `lean/`).
* Item 3(d): `diff ws_R4/lean/TwoRoundsExpected.lean EXPORT/proofs/Frontiers/TwoRoundsExpected.lean` = +6 lines of
  provenance, −5 lines (a blank line and the four `#print axioms`); the four are in `AxiomAudit.lean` lines 507–510;
  `TwoRounds.lean` is byte-identical to 5ed4072.  Their description is exact.

### step 7 — item 2(d) "M4 is not a sharpening": checked line by line; **they are right, we were wrong**
* Read OURS `docs/workstreams/G_REPORT.md` (unchanged since 5ed4072) lines 53–152; `SCI-REV-0006.md` in full;
  `A2_REPORT.md` lines 262–295, 640–665; theory report Theorem 4.6 / Corollary 4.7 (5ed4072) and Theorem 11.36
  at 5ed4072 (line 2902) and 658b77f (export line 3119).
* G_REPORT §2.1(c), lines 97–110: `I_A ≤ Ī(i) = Σ d̄(p)²`, `Ī(m) = ⅓ sin²(θ/2) b² m³(1+O(1/m))`, proof = "distance to
  the axis ≤ distance to the axis atom; atoms two bonds apart at fixed distance 2b sin(θ/2); triangle inequality";
  attained asymptotically by "one gauche next to the axis followed by all-trans (an arm almost perpendicular to
  the axis)", `max I/m³ = 0.256 → 0.228` against `sin²(θ/2)/3 = 0.2264`.  §2.1(d), line 115:
  `c_i^ver = 2Λ sin(δ/2)√Ī(m_i) ≤ (2/√3) sin(δ/2) sin(θ/2)·Λ b m_i^{3/2}(1+O(1/m_i)) = 0.824…` (θ = 111°, δ = 120°).
* A2 (ours): `I_arm ≤ (b² sin²(θ/2)/3) m³(1+o(1))` by "largest end-to-end distance of j bonds"; attained by "an
  all-trans arm joined through one gauche torsion"; `sup 2√(2I_red) = 2√2/3` at the centre, `4/3` far from it.
  Same bound, same argument, same extremal conformation.  `2√2/3` = G's formula at (tetrahedral, δ = 180°);
  `0.824` = G's formula at (111°, 120°); `4/3 = √2·2√2/3` is the looser form `2√(2I_red)` of Theorem 4.6(d) where the
  verified constant uses `min(I_A, I_B)` — i.e. far from the centre our number is a *weaker* bound than theirs.
* Own numerics (`r9_lever.py`, `out/lever.txt`): 0.824126; 0.942809; G's `Ī(m)/m³` nonincreasing for all m ≤ 2·10⁵,
  `2 sin60°√Ī/m^{3/2} = 0.898, 0.832, 0.825` at m = 10, 100, 1000 (so "≥ 0.824 at every position" holds); kinked arm at
  θ = 111°: 88.23° to the axis, `I/m³ → 0.22618` (0.1 % below the bound; two gauche torsions give sin² = 0.999999);
  exhaustive over the first 7 arm torsions at m = 200: 0.22786 (G reports 0.228); tetrahedral: exactly 90°, → 2/9.
* Also false in OUR report: A2_REPORT line 287–288 "Theorem 11.36's `c_i ≥ 0.824…` … is confirmed and is not sharp in
  the constant" — for the report's parameters 0.824 IS the sharp limit.
* The coordinator published the linked correction while I was working (SCI-RES-0007 §2, commit 242f771, 23:48;
  head note on SCI-REV-0006; DEAD_ENDS SD38).  Read after my own check.  It is right.  Not covered by it:
  (i) the `4/3` (a looser bound, not a second sharp constant); (ii) that the argument and the extremal conformation
  were in G §2.1(c) too; (iii) `A2_REPORT.md` itself carries no note (lines 40, 286–288, 645 (W6's suggested wording
  "sharp constant `2√2/3` at the centre of a tetrahedral chain"), 661, 739).

### step 8 — more results
* `out/cobound13_part{0,1}.txt` (**own code**, `r9_cobound.c`): all 350 026 681 ordered pairs of (bridge, admissible c₁) with
  N₁, N₂ ≤ 13 (18 709 entries), real concatenations: error = A(x¹,c₁) + B(x²) in all; B(concat) = B(x¹), A(concat) =
  A(x²) in all; q̂ exactly additive in all.  Maxima of the error vector (1,6,8,1 | 41) = R2's exhaustive maxima.
* Item 2(b) (**re-ran R4's code** `twins_exact.py`, read-only import; `r9_Eprime.py`, `out/Eprime.txt`): on the rows of the
  table, E′ − E = 6.06e-5 (u = 2, n = 200: E = 0.1129377, E′ = 0.1129983 → 0.1129 / 0.1130 at four decimals),
  3.04e-5 (u = 1, n = 400), 1.19e-5 (u = 2, n = 400), ≤ 7.4e-6 from n = 800 on.  So R4's "equals the printed E to four
  digits" fails in one row; their amendment (E′ − E ≤ 6.3e-5 at n = 200, 400) is right.
* Items 2(c)(b),(c) and data points of Prop. 11.103(d) (**own code** `r9_sites.py`, `out/sites.txt`; cube closed forms
  reproduced to 10 digits): u = 0.5: (0.02,0.49,0.49): h = 0.007672224, E = 0.030922047 (both below the cube's 0.0076729,
  0.0309298), a = 0.030304356 (above 0.0302999) ✓; (0.05,0.5,0.45): h = 0.007675166, a = 0.030321669, E = 0.030931644 ✓;
  (0.04502,0.45679,0.49819): h = 0.007675293 ✓; uniform 0.007425205 ✓; (0.001,0.4995,0.4995): 0.007672975 (above the
  cube by 0.0014 %).  u = 1: uniform E = 0.1194991, h = 0.0306536, a = 0.1232845; (0.05,0.5,0.45): E = 0.1201960;
  (0.3,0.35,0.35): h = 0.0305722, a = 0.1229515 — every printed digit of the report reproduced.
* Item 2(c)(a): re-derived.  ‖c − n⃗/n‖₁ = Σ_j|f_j − F p_j|/n_i with f_j = frac(φn_j), F = Σf_j; this is < 2m/n_i and
  exceeds m/n_i for m ≥ 3 (p = (1−2ε, ε, ε), f = (0, ~1, ~1): ≈ 4/n_i > 3/n_i); for m = 2 it is < 2/n_i = m/n_i.  Their "2m" is right.
* Item 3(a): re-derived the χ² step and all error terms of Theorem 11.97(c) (see report §3.1): correct.  The constant:
  any c > c_ω := m[q_max e^{D_max}/π_min + ln(1/π_min)]/(2 + m q_max) for n ≥ n₀(c); the q_max/M term enters once (in
  η_{M,n}, Step 5), not in "I(X;U|T) ≤ α_C + o(1)" (Lemma T′(3) gives α ≤ α_Ã without it).
* Sampled minors (**own code** `r9_minor.py`, `out/minor.txt`): R1 m3: 0.020200 / 0.144080 (the report's 0.0202 / 0.1441
  are right; OUR review printed 0.0201 / 0.1439 — last digits off); R1 m11 and the whole table of Thm 11.90 reproduced
  (centre types 0.471, 0.442, 0.383, 0.325, 0.266; cusp 5.800e-7 at X = 1e-12); R4 m9 witness: terms 0.54015a, 0.54026a,
  0.54022a ✓; R5 m8: tri = (d01, d12, d02) = (1, 1.5, 2), E, a, h reproduced, slope jump +0.0055..0.0057 by one-sided
  differences ✓ (+0.0056); R5 m1: E_sp(0.3a) − 0.3a = −0.00817 ✓.
* Long bridges (`r9_long.py`, `out/long.txt`): 787 random bridges with dense ends (79 with ≥ 1000 beads, max 3970), all
  become clean with head 2 + tail 3 and with 5 + 5; 1500 concatenations up to 7873 beads: decomposition, inherited
  ends, q̂ additivity; 250 pairs of clean ones: exact; 25 six-fold self-concatenations: (h,g) = 6(h,g) + 5(A+B).
  The helix is clean for every N tested (A = B = 0).  Five explicit clean bridges with det ±1 (coordinates in the output).
* `r9_inner_volume.py`: with the exact semigroup the proved inner volume 1.5632 becomes 1.6192 without coordinates
  (centres (h + (½, 9/2, 7))/(N+3), radius 29.5/(N+3)), about 1.6314 if A + B is computed from coordinates.
* Item 5: read the word-diff of all hunks outside §§11.22–11.26 (`r9_diffview.py`): §0, §4.4, §6, §8, §9, §10, §11.6,
  §11.11, §11.14, §11.17, §12, README passages.  Attributions checked against A2_REPORT: "unverified checker" (van Doren),
  "searches thin", `L_{H,p}` are ours.  No wrong attribution found so far.

### step 9 — false alarm of mine, recorded
* `r9_chi2_check.py` (two letters, solver-free grid computation of `v`) first reported "93 violations" of
  `0 ≤ I − v ≤ χ²(P‖Q)`.  All 93 are cases with P inside the window, where `I − v = 0` and the grid value is `−5e-7`
  (grid step 5e-7 against my tolerance 1e-7).  Outside the window the largest excess over all window points is 0.
  Tolerance set to 2e-6; no violation.  (Same kind of trap as R1's NOTES steps 4, 11.)
* `r9_sites2.py` (`out/sites2.txt`): ceiling `F*(t) ≤ t(1−t)D²/8` on 40 random asymmetric sites: largest ratio 0.7465;
  three-letter uniform site below the ceiling by 9.7 / 5.0 / 1.9 / 5.8 % at u = 0.1 / 0.5 / 1 / 2 (report: 11 % as u→0,
  5.0, 1.9, 5.8 ✓); weight-½ laws: F* ≥ F*_cube in 200 of 200; `(I − v)` formula: primal (couplings) = dual (γ ∈ L) to
  4e-15 in 120 cases, q = 2..4, asymmetric; `0 ≤ I − v ≤ KL(P‖Q) ≤ χ²(P‖Q)` in all; on the set G of the proof
  `(I − v)/ω′ ≤ 0.0147` in 300 random chains (the bound is far from tight).
* `r9_slices.py` (`out/slices.txt`): 360 random feasible profiles with 3–5 blocks at six (κ, u, e<0): none exceeds the
  two-block supremum (largest r_μ − R2 = −1.7e-4); R2(κ=½, u=1, e=−0.05) = 0.059050 = the report's 0.0590497.
* `r9_certificate.py`: five clean bridges (4, 5, 9, 9, 11 beads) with determinant 1; four with determinant −1 for the
  projection; a clean 9-bead bridge off the hyperplane g = 9p₃ − 3p₈ + p₁₁ (exact interior certificate for K^br in R⁴).
* Theorem 11.56 read (export lines 4277–4350) for the good event: δ′ = δ/(4LM̄), "every potential inner call valid" —
  so the batched schedule's extra inner calls are covered and the stopping rule cannot fire on the good event.

### step 10 (about 00:35, 26 Nov) — report written (`docs/science/workstreams/R9_REPORT.md`), then checked against the outputs
* Counts corrected after re-reading my own outputs: 38 (not 31) of 41 minor findings read, 20 checked; head 2 + tail 2
  fails from N = 12 (not 16); 21 220 319 (not "21.5 million") pairs (x, c₁) with N ≤ 20.
* Additional checks made for the report: bridge totals per N (3..22) = sums of the count column of R2's tables;
  `iterates_lt_hint_add` read in `HintRecursion.lean` (line 326; hypothesis `hbdd`); the cited declarations of
  `GroupSampling.lean`, `RenyiCentre.lean` exist; harness labels exist; `lower_end_any` exists.
* New finding while re-reading §11.22 for item 5: lines 5282–5284 — "(for d = 1, where the limit is a point, a
  super-additive sequence can converge arbitrarily slowly)" is false under (C) as stated (two-sided, |q − q₁ − q₂| ≤ β):
  for single points (C) gives |a_M/M − lim| ≤ β/M.  A correct example: Q_M = [0, a_M], a_M = M − M/ln(M+2)
  (super-additive, nondecreasing; limit [0,1]; right end approached like 1/ln M).
* SCI-RES-0007 §1 (ours, published 23:48) says our M1 text "was written against 5ed4072" — that covers the second
  amendment only; Prop 11.81(b) at 5ed4072 already had R_H < R_unif beyond the junction.
* `r9_m1_input.py`: 3000 random (J, h₂ > 0): optimal input field in (−h₂, 0), E B > 0 in all (R1 m1 as rewritten).

### step 11 (00:42, 26 Nov, read from `uptime`) — exact points from the ten explicit bridges
* `r9_witness_ends.py`: re-generated the nine box-64 bridges and the 166 199-bead bridge (box 128) with the AUTHORS'
  builder (`experiments/workstreams/S/code/build.py`, call sequence as in R2's `r2_verify_witness.py`; I did not read
  `build.py`), verified with my `r9_lat.py`: lattice walk, injective, bridge, (h,g) from coordinates = the stored counts
  in all ten.  End corrections: A = B = 0 for nine (clean as built); W3 woodpile A = (0,0,1,0), B = 0.  For each the
  extension head 2 + tail 3 is clean with (h,g) + A + B.
* `r9_exact_packing.py`: R2's weights on the exact vertex list q̂/(N+3), radii zero, exact rationals: all pairs strict
  for 116 / 451 / 8 / 19 points (smallest margins +0.002172, +0.001263, +0.024910, +0.005590).  Hull of the 14 exact
  profile points: 1.631346 (Qhull; exact rational sum over the cones of its 18 facets agrees) — so vol K ≥ 1.6313.
* Report updated (§4.5, verdict table, §9, §10, request R9-E1, "What I did not check").

### step 12 (00:47, read from `uptime`; machine load 16) — final passes
* Re-read the whole report against the outputs; corrections made: "eleven centre types" (not ten); the random-profile
  test of Thm 11.90(a) is labelled weak (random profiles stay 1.7e-4..5e-3 below the supremum; not an optimised
  search); run times in §7 taken from the outputs; duality brackets described as "closed in all printed digits";
  the Lean oleans are "present in .lake/build", I did not build them.
* `r9_sites.py` now stops after the data points unless called with `all` (the later tests are in `r9_sites2.py`);
  `out/sites.txt` regenerated from it.
* README.md written.
* Final message to the coordinator: verdict per item, findings classified, corrections owed, the semigroup result,
  what was not checked, path of the report.
* `r9_extremal.c` / `r9_extremal.py`: the first 21-bead bridge with A = (1,6,10;1) and the first 14-bead bridge with
  B = (0,3,4) from the enumeration; their real concatenation (38 beads), counted by the O(n²) definition, has the
  error vector (1, 9, 14, 1), norm 60: the constants of Lemma 11.68 are attained.

## Follow-up (coordinator's message after the first hand-back): review of the theory division's own statement

EXPORT2 = `/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_24a3c27` (theory tree at `24a3c27`, read-only).
New files of this follow-up are named `r9b_*`; the deliverable is `docs/science/workstreams/R9_ADDENDUM.md`.

### b-step 1 — start (time read from `date -u` in the command that wrote this entry)
Thu Nov 26 01:53:38 UTC 2026
