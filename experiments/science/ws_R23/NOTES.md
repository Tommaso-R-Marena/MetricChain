# R23 — NOTES (running log; times are UTC read from `date -u`)

Workstream R23: sampled adversarial check of the theory division's assumption audit.
Object: `<THY>` = `/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_fc3f5d9/` (read-only export of theory branch at `fc3f5d9`).
Write area: this directory and `docs/science/workstreams/R23_REPORT.md` only.

## 2026-11-26T17:24:50Z — start
* Read `COMMON.md` and `R23_brief.md` in full.
* Created `ws_R23/` with `rerun_copy/`, `not_cited/`, `logs/`.
* Nothing of the audit has been opened yet (only `ls` and `wc -l` of `<THY>`).

## 2026-11-26T17:25Z — SAMPLING RULE, FIXED BEFORE READING ANY ENTRY (pre-registration)

Written before any `grep`/`Read` of `ASSUMPTION_AUDIT.md`, `AA1_REPORT.md`, `AA2_REPORT.md`.

**Population.** For a tag `T ∈ {P, F, Q, ?}` and a report `R ∈ {AA1, AA2}`: all occurrences of the literal
token `{T}` in `<THY>/docs/audit/R_REPORT.md`, in file order (line, then column), *that tag an assumption of a
statement entry*.  Occurrences in the legend, in count tables / summaries, and in prose that refers to a tag
generically are excluded by a mechanical criterion that I determine from the *shape* of lines only (leading
characters, section headers), before reading any mathematics, and that I record below once determined.

**Draw (systematic with seeded start).** `N` = population size, `m` = sample size, `k = N // m`,
`rng = random.Random(seed)`, `seed = int(sha256(f"R23|{R}|{T}".encode()).hexdigest(), 16) % 2**32`,
start `s = rng.randrange(k)`; the sample is the occurrences with 0-based indices `s, s+k, …, s+(m−1)k`.
If `N ≤ m`, take all and say so.

**Sizes.** `{P}`: 6 per report (12).  `{F}`: 5 per report (10).  `{Q}`: 3 per report (6).  `{?}`: 2 per report (4).

**Substitution.** If a drawn occurrence turns out not to be a tag on an assumption (e.g. a tag quoted in prose
that the mechanical criterion missed), take the next occurrence in file order (index + 1, wrapping) and record
the substitution.  No other substitution — in particular none for "too hard".

**The two `{F}` rebuilt with own code.** `rng = random.Random(int(sha256(b"R23|rebuild").hexdigest(),16) % 2**32)`;
shuffle the ten sampled `{F}` (order: AA1's five then AA2's five); take in shuffled order the first two whose
named counterexample is a finite object computable under the resource limits (≤ 20 min, ≤ 2 GB); record every
one skipped and why.

**Item 4, five citations of our reviews.** Population: all occurrences of the regex `SCI-(REV|RES)-[0-9]+` in
`AA1_REPORT.md`, then `AA2_REPORT.md`, then `ASSUMPTION_AUDIT.md`, in file order.  Systematic sample of 5 with
seed `sha256("R23|citations")`, same formula.  If a drawn occurrence cites a message already drawn, take the
next occurrence in file order that cites a different message (so five distinct messages if there are five).

**What the rule does not fix** (free choices, to be reported as such): the three counterexamples of Item 2 are
prescribed by the brief; "the most consequential positive fact" of §6 is my judgement; the three gaps of Item 5
are my judgement.

## 2026-11-26T17:26Z — shape reconnaissance (no entry read), mechanical population criterion
(heading first written as "17:31Z" from an estimate, not from the clock — own error E1, corrected at 17:26:38Z from `ls --time-style=full-iso`: `shape_recon.py` 17:25:43Z, this section and `draw_sample.py` 17:26:31Z)

* `shape_recon.py` (prints only line numbers, enclosing header index, the first 22 characters of tag-bearing lines).
  Token counts per file (all occurrences): AA1 `{E}`58 `{P}`19 `{C}`28 `{Q}`44 `{X}`19 `{F}`56 `{?}`27 (=251);
  AA2 `{E}`65 `{P}`64 `{C}`31 `{Q}`30 `{X}`20 `{F}`54 `{?}`47 (=311); the synthesis `ASSUMPTION_AUDIT.md` has no tag token.
* Read so far: AA1 lines 1–104 (preamble, conventions, one-page result — no entry); headers of AA1 and AA2.
* **Mechanical criterion (fixed now):** an occurrence is in the population iff it lies under an entry header —
  AA1: after the first `### E<k>.` header and before `## 4.` (lines 105–1475);
  AA2: after the first `### Entry <k>` header and before `## A. Synthesis` (lines 87–1427).
  Everything else (legends, AA1 §§0, 4–10; AA2 §0 and §A) is excluded.  Mid-line tags inside entries count
  (one token = one member of the population).  The substitution rule covers tokens that turn out to be prose.
* Sampler: `draw_sample.py` (next step) — writes `sample.json` and `logs/draw_sample_<time>.log`.

## 2026-11-26T17:26:31Z — the sample is drawn (`logs/draw_sample_20261126T172631Z.log`, `sample.json`)

Population inside entries (tokens): AA1 E52 P16 C26 Q39 X13 F47 ?23 (216); AA2 E63 P62 C29 Q28 X18 F52 ?45 (297).
(The audits' own counts — 202 + 297 = 499 "classified assumptions" — to be compared in Item 3a.)

| kind | AA1 (line, entry) | AA2 (line, entry) |
|---|---|---|
| {P} | 364 E8; 522 E15; 679 E20; 762 E25; 1115 E37; 1262 E42 | 337 En10; 446 En15; 617 En24; 887 En40; 1099 En56; 1386 En73 |
| {F} | 195 E3; 491 E14; 743 E24; 891 E29; 1110 E37 | 352 En11; 606 En23; 931 En43; 1114 En57; 1357 En72 |
| {Q} | 498 E14; 927 E31; 1438 E48 | 200 En4; 594 En22; 1233 En64 |
| {?} | 768 E25; 1392 E46 | 406 En13; 908 En41 |

Rebuild order for the ten {F}: AA2 1357, AA2 1114, AA2 931, AA2 352, AA1 743, AA1 1110, AA2 606, AA1 491, AA1 891, AA1 195.
Citations (27 occurrences, 12 distinct messages): AA1 l.839 SCI-REV-0012; AA1 l.1380 SCI-REV-0006; AA2 l.449 SCI-REV-0016;
AA2 l.944 SCI-REV-0003; AA2 l.1071 SCI-REV-0005.

## Own errors (running list)
* E1 (17:26Z): a section heading of these notes carried a time that was estimated, not read from the clock (5 minutes off). Corrected; rule from now on: `date -u` before every heading.
* E2 (17:32Z): the same mistake a second time (heading typed as "17:40Z" in the same command that read the clock as 17:32:27Z). Corrected. From now on every heading is produced by `$(date -u …)` inside the shell command that appends it.
* E3 (17:35Z): `item2c_pbiased_tail.py` (v1) contained a third ratio, "every set against the best ball of at most its own measure", that is not a notion of extremality (it is 4 for the uniform measure: four isolated points against one point).  My own control (p = ½ must give 1) caught it: 4 violations in `logs/item2c_pbiased_tail_20261126T173538Z.log`.  v2 drops it.  The two other ratios were unaffected (identical numbers in v1 and v2).
* E4 (17:43Z): `item1_thm1132_additive.py` (v1) asserted `status == 0` on LPs that HiGHS reports as "infeasible" when they are unbounded; the run stopped (log in `not_cited/`).  v2 treats status 2/3 as unbounded after asserting that the true residual is a feasible point.
* E5 (18:10Z): in `item2d_mixture_sandwich.py` (v1) the control M2 ("the one-average bound must fail for some mixtures") was run on the same random instances as the test and could not react (0 failures: random residuals are not aligned with the modes); the log ends with "TOTAL violations: 1".  v2 has a designed two-mode family (26 of 30 failures of the one-average bound, the K = 2 bracket holds in 30 of 30).

## 2026-11-26T17:32:27Z — reading for Item 2, before any audit script is opened
* Read in full: the synthesis `ASSUMPTION_AUDIT.md` (364 lines); AA2 lines 1–206 (how-to-read and Entries 1–4; none of them a sampled line);
  theory report l.1737–1986 (§§11.1–11.4), l.3798–3943 (§§11.12–11.13 with Theorem 11.33), l.4092–4295 (§11.16), l.6440–6475, l.6287–6300;
  `docs/workstreams/D_REPORT.md` l.470–560 (the source, Theorem 13) in our repository.
* File-name listing of `<THY>/experiments/audit/`: AA1 has 7 scripts (`aa1_01 … aa1_07`), AA2 has 8 (`s1 … s8`): **15 scripts, not 14**
  as the synthesis (l.26–27) and our brief say.  To be reported under Item 3a.  No script opened yet.
* Source check for Item 2(b): D_REPORT Theorem 13 is stated with "`f` additive" (l.491–492 of D_REPORT: "(mixed second differences; no
  first-order bound), `f` additive, `w = βc₂n`"); theory report l.3877–3879 has no hypothesis on `f`.  The audit's diagnosis (hypothesis
  lost in adoption) is confirmed by reading [review].
* Own derivations done before coding (to be checked numerically):
  (a) two-state sites, zero residual, `φ_i=(0,e_i)`, `c_i>e_i`: `{0,e_1,…,e_n}` is a fooling set for the cover relation
      `d(a,y) ≤ gap(y)` (no centre covers two of them) ⇒ `N ≥ n+1` for ANY non-sharp two-state sites; and it is a cover when all margins
      `c_i/e_i − 1 ≤ 1/(n−1)` (cover `y` with support `S` by `e_j`, `j = argmax_S e`): so `N = n+1` exactly.  Homogeneous case: the condition
      `margin ≤ 1/(n−1)` is also necessary.  (The audit says "< 1/n": sufficient, slightly stronger than needed.)
  (b) Golay: with `βc₂ = w/n = 1/6` the dip of Theorem 11.31(a) with `r = 5` has depth `10c₂` and support `B(y,3)`; balls of radius 3 around
      codewords are disjoint (d_min = 8); `ln Z` moves by `ln(1 + (e^{5/3} − 1)/4096) ≈ 1.048·10⁻³`.  So "ε < 10⁻³ ⇒ (1−2δ)·4096" is the
      detection bound with disjoint difference sets.  NOTE: at `n = 24`, `ε = 10⁻³` the theorem's own cost "about `n⁵ε⁻²`" is ≈ 8·10¹² ≫ 4096:
      the explicit instance does not contradict "polynomially many" numerically; the contradiction is the asymptotic family
      (GV codes: rate `R(w) = sup{ln2 − h(δ) : ln2 − h(δ) ≤ wδ²/8}`, `R(4) ≈ 0.056` by hand).
  (c) formulation to be tested: `Ξ₀(q) = max{Σ_{x∈D} π(x)(e^{u·dist(x,Dᶜ)} − 1) : π(D) ≤ q}` against Hamming balls, all 65 534 subsets of `Q_4`.

## 2026-11-26T17:36:44Z — Item 2 done with own code (no audit script opened yet)

**(a) near-sharp sites** — `item2a_near_sharp.py`, log `logs/item2a_near_sharp_20261126T173333Z.log` (reached END; 9.5 s; total violations 0).
 * T1 direct definition `UB−LB=0` for `A0={0,e_i}`, n=1..12: 0 violations.  T2 each point of A0 covered by itself only (exhaustive over 2^n centres), n=1..12: 0.
 * T3 ALL subsets of size ≤ n by the direct definition, n=1..4 (2516 subsets at n=4): none certifies; exactly one certificate of size n+1.
 * T4 exact minimum cover by ILP = n+1, n=1..10: 0 violations.  T5 heterogeneous (180 random instances): 0; fooling set for ANY margins (180 instances): 0.
 * Controls: C1 sharp → one evaluation (0 viol.); C2 margin 1.1/(n−1) → A0 fails, min cover n+2 (reacted for all n=3..10);
   boundary margin = 1/(n−1): still n+1; C3 margin 1: min cover 2,3,5,6,9,13,18,23 for n=1..8 (≥ (6/5)^n); C4 negative control reacted.
 * `R*/margin → W(1/e) = 0.27846` — the synthesis' "about 0.28·(c/e − 1)" is right.
 * VERDICT (a): **confirmed** (proof + replication).  Refinements: (i) `N ≥ n+1` holds for every family of non-sharp two-state sites (fooling set);
   (ii) the exact homogeneous threshold is margin ≤ 1/(n−1), "< 1/n" is sufficient; (iii) the claim is about the certificate size at the zero residual.

**(b) Golay** — `item2b_golay.py`, log `logs/item2b_golay_20261126T173451Z.log` (reached END; 1.4 s; total violations 0).
 * G1 code rebuilt from the cyclic [23,12,7] code: enumerators 1+253z^7+…, extended 1+759z^8+2576z^12+759z^16+z^24.  G2 radius-3 balls pairwise disjoint
   (exhaustive; control: radius 4 → up to 6 balls per point).  G3 dips in the class (exhaustive n=10, r=2..9; profile argument for n=24; control reacted).
 * G4 `ln Z` shift of one dip r=5: **1.047910e-3** (audit: "ε < 10⁻³" ✓.); with a finite penalty `βM ≥ 12` off the code the shift stays > 10⁻³.
 * G5 the bound `(1−2δ)·4096` is Theorem 11.22(c) with B = 1.  **Sound.**
 * G6 **at n = 24, ε = 10⁻³ the theorem's own cost "about n⁵ε⁻²" is 7.96·10¹² (> 2^24 = 1.68·10⁷ > 4096)**: the explicit instance does not exceed
   the polynomial that (a) states; no finite instance can refute "polynomially many".  The refutation is the family (G7): GV codes, `R(4) = 0.0559` ✓. (audit: 0.056).
 * Reading of the statement: theory report l.3877–3879 constrains `g` only; `f` is not mentioned in (a); the chapter setting (l.1739) gives every instance a
   known `f`; the source (D_REPORT Theorem 13) has "`f` additive".  (a)'s own first sentence ("Dobrushin's uniqueness condition holds for every member of the
   class … influence at most tanh(βc₂/4)") is false for a non-additive `f` — so the text signals the tacit hypothesis.
 * VERDICT (b): the lower-bound argument is **sound**; the instance is inside the scope of (a) only through the chapter's standing setting (any known `f`);
   it contradicts (a) **under that reading**, and as a family, not at n = 24.  "False as stated" = a hypothesis of the source was dropped.  Major (statement), not a refutation of the source theorem.

**(c) p-biased tail functional** — `item2c_pbiased_tail_v2.py`, log `logs/item2c_pbiased_tail_v2_20261126T173615Z.log` (reached END; 0.9 s; violations 0).
   (v1 log `logs/item2c_pbiased_tail_20261126T173538Z.log` reached END with 4 control violations of a mis-specified ratio: own error E3.)
 * all 65 534 subsets of Q_4, exact rational measures; ratio_A = max over balls B of `Ξ(π(B))`/best ball of at most that measure:
   **2.0827 at (p,u) = (0.2, 2)** ✓., **1.4189 at (0.3, 4)** ✓., 1 at p = ½ ✓. (control); type-dependent radii: **1.1230 at (0.2, 1)** ✓..
 * Not in the audit's sentence: on my grid the balls ARE extremal on Q_4 at p = 0.4 (all four slopes) and at p = 0.1 for u ≤ 2 (ratio_A = 1): 9 of 16
   grid points with p ≠ ½ show non-extremality.  The verbatim analogue of the lemma (a ball of the given measure is itself extremal, ratio_B) fails by up to 46.
 * VERDICT (c): **confirmed** (replication).  It is a statement about Q_4.

## 2026-11-26T17:42:06Z — sampled entries read in the audit (first pass, before reading the theory report passages)

Entries read in full: AA1 E3, E8, E14, E15, E20–E25, E29–E31, E37, E42, E43 (for Item 2b), E46–E50; AA2 Entries 1–4, 10–15, 19–26, 36–43, 51–57, 63–74.
What each sampled token tags (first impressions; verdicts come after checking the theory report / Lean / own computation):

AA1 {P}
 1. l.364 E8  "pairwise energy, in the voxel bridge" — support claimed: Lean lemma `voxel_boltzmann_bounds` for any measurable energy. TO CHECK in proofs/.
 2. l.522 E15 "{P}{?} a disconnected family" (Theorem 6.1) — the audit itself says open (§12 item 6). Double tag.
 3. l.679 E20 "the adversary argument is for deterministic procedures" — support: Theorem 11.23(iii) [P] (R3 App. B). TO CHECK.
 4. l.762 E25 "{P}{?} identical sites" (Theorem 11.15) — lower bound tensorises; upper bound for several types "not stated here". Double tag.
 5. l.1115 E37 "Harper's theorem" — a cited true theorem, not a hypothesis; "beyond the cube the upper bound has another proof (R4)". TO CHECK.
 6. l.1262 E42 "an additive true residual (the star then reproduces it)" (Theorem 11.32) — words only.
    **My attempt: FALSE without it.**  n = 2, c = 1, e = 0.1, true residual g0 = −c·C(|x|,2) (boundary member of the class), f = e|x| − g0:
    E = e|x|, K₋ = 4 (every ρ₋ = 0) but the star {00,01,10} certifies the minimum exactly (g'(11) ≥ −1 ⇒ E'(11) ≥ 0.2 > 0): N₂ ≤ 3 < K₋.
    Reason: the dip can be subtracted from the true residual only if the result stays in the class (true for additive g, false at the boundary).
    To be confirmed with own LP code.  Candidate replacement tag: {F}{Q}.
AA1 {F}
 7. l.195 E3 triangle inequality ({C}{F}) — 3-point table; checked by hand: closure gives d*(y,x)=2 < 5 = f(x) − f(y). Counterexample to the criterion with a non-closed table. OK.
 8. l.491 E14 "consistency of the published data, if it is not checked" — `inconsistentResidual_unguarded`, D15.  With inconsistent data the class is EMPTY, so
    "for every residual of the class" is vacuous — is this "false when removed" or "vacuous when removed"? TO CHECK in Lean/D15.
 9. l.743 E24 "β ≥ 0 and the orientation of the coupling for asymmetric envelopes" — no object named beyond "R2". Rebuild a 2-point example myself.
 10. l.891 E29 "connectivity as a substitute (D = {00,01,11})". TO CHECK against Prop 11.18c.
 11. l.1110 E37 "two states per site — for 'single dips are extremal'" (D38, DEAD.16, Theorem 11.27). TO CHECK.
AA1 {Q}
 12. l.498 E14 "exact tables: … termwise lower instances (`verify_sound_real`)". TO CHECK Lean.
 13. l.927 E31 "independent sites, for the closed forms; for other laws … a search that contains a minimum-weight hitting-set problem" — is this a weaker *quantitative* condition at all?
 14. l.1438 E48 "a uniform constant c (site-dependent constants give a weighted ratio; not stated)" — own argument: run decomposition ⇒ criterion Σ_{i∈D} c_i ≤ excitation energy of every contiguous droplet.
AA1 {?}
 15. l.768 E25 "an additive instance" (Theorem 11.15).
 16. l.1392 E46 "Flexible geometry is not treated" (lever-arm law).
AA2 {P}
 17. l.337 En10 "4|B(n,r_ε−2)|/2ⁿ ≤ δ … the second branch of the proof" (Theorem 11.51).
 18. l.446 En15 "the binomial median (Lemma 11.55(b))" — no support given; an ingredient, not a hypothesis.
 19. l.617 En24 "a fixed product measure with identical two-letter sites" (Theorem 11.63) — support: Theorems 11.78(b), 11.97(c). TO CHECK.
 20. l.887 En40 "βJ ≥ 0 in (c)" — "{?} otherwise (Conjecture 11.94)". Double tag in effect.
 21. l.1099 En56 "extensive accuracy — {P}; bounded accuracy {?}". Double tag in effect.
 22. l.1386 En73 "stationarity and homogeneity in (e) — {P} (exact sub-/super-additivity)". Suspect: without homogeneity the limit F_∞ need not exist.
AA2 {F}
 23. l.352 En11 product structure of the reference measure → fact (F2); S8.  A counterexample to a LEMMA of the proof (the audit says so itself in Entry 13: "{?} for the statement, {F} for the proof").
 24. l.606 En23 "q < 1 — {F} at q = 1" (Lemma 11.62).  Own argument: a constant ŵ ≡ C > t gives D = X and E(ŵ−t)₊ = C − t unbounded. OK.
 25. l.931 En43 the stopping rule (Theorem 11.84): 393 216 against 79 931 (DEAD.27, XX.5). Our SCI-REV-0003's major finding.
 26. l.1114 En57 two letters for "a field always helps": 11.103(d), DEAD.24 (three letters: 0.120196 against 0.119499).
 27. l.1357 En72 non-empty boxes in the adjacency criterion (`sep_card_le_one_not_sufficient`).
AA2 {Q}
 28. l.200 En4 "ε > ln 3 — constants 1±η reach every accuracy at a factor ε⁻²; this is Proposition 11.57(a)".
 29. l.594 En22 "site-dependent windows: Σ_i max_b KL(a_b^(i)‖r_i*) by the same chain rule (not written; the division's version … 'is not adopted')".
 30. l.1233 En64 "exact oracle — precision τ … a factor polynomial in 1/τ (the division's, not checked)".
AA2 {?}
 31. l.406 En13 "product reference measure — {?} for the statement" (adaptive = hinted with interactions, O4).
 32. l.908 En41 Proposition 11.82: "none is known to be the value".

Observation for Item 3a: double tags {P}{?} / "{P} …; {?} otherwise" are counted once under P and once under ? in the audits' tables — to be quantified.

## 2026-11-26T17:43:38Z — sampled {P} no. 6 (AA1 l.1262, Theorem 11.32 "an additive true residual") decided: **{P} → {F}**
* `item1_thm1132_additive_v2.py`, log `logs/item1_thm1132_additive_v2_20261126T174317Z.log` (reached END, 5.5 s).  v1 stopped on an assertion
  (HiGHS returns "infeasible" for an unbounded LP with free variables): `not_cited/item1_thm1132_additive_20261126T174301Z.FAILED.log`; own error E4 (status handling), fixed in v2.
* LP over the whole class G2(c), exhaustive over evaluation sets: with the boundary member g0 = −c·C(|x|,2) as true residual and f = e|x| − g0 (energy e|x|, e < c/n):
  n=2: N₂ = 3 < K₋ = 4; n=3: N₂ = 4 < K₋ = 8; n=4: N₂ ≤ 5 < K₋ = 16.  Control (additive true residual, same energy): N₂ = 4, 8, 16 = K₋ — the theorem as stated holds (0 violations of 3).
* Argument: h = g' − g0 has D_iD_j h ∈ [0,2c] and vanishes on the star ⇒ h ≥ 0 (telescoping) ⇒ the star gives the exact lower envelope.  The dip of Theorem 11.31(a)
  cannot be subtracted from a boundary member.  Quantitative substitute: |D_iD_j g| ≤ κc, κ<1 ⇒ lower bound with c(1−κ), upper bound with c(1+κ).  Replacement tag: {F}{Q}.

## 2026-11-26T17:55:00Z — sampled items checked against the theory report / Lean / own code (second pass)

Own code: `item1_rebuild_F_two.py`, log `logs/item1_rebuild_F_two_20261126T175119Z.log` (reached END; 180.8 s; total violations 0).
* R1 = rebuild of AA2 l.1357 (adjacency of boxes): all pairs of boxes for (n,k) = (1,2),(2,1),(2,2),(2,3),(3,2) (8 480 pairs): criterion WITH the
  non-emptiness clause wrong in 0; WITHOUT it wrong in 2 250; the Lean example confirmed.  {F} stands (replication).
* R2 = rebuild of AA2 l.1114 (three letters): own formula `E(π) = min_Q max_φ KL(Q‖π_φ)` (the limit `F*(t)/t`, t→0, of the radius form), primal–dual certified:
  uniform 0.119499092 (= Ψ₃(1)), (0.05,0.5,0.45) 0.120196008, two-letter cube 0.120114507 — the report's 0.119499 / 0.120196 / 0.120115.  Control: two letters,
  9 fields, none above p = ½.  27 of 171 grid laws beat the uniform law.  {F} stands (replication).
* R3 (AA1 l.743): two points, g = 0, β = −1, product coupling: 0 ≤ −0.5 false; control β = +1 holds.  {F} stands (own argument).
* R4 (AA2 l.606): Q_3, constant ŵ: E(ŵ−t)₊ = 12.85 > t·Ξ = 5.43.  {F} stands (own argument).
* R5 (AA1 l.1110): 0.02841 (dips) < 0.02914 (boxes of pairs) from the formula of Theorem 11.27, k = 4, u = 1.  {F} stands (formula re-evaluated; the lower bound itself is the report's [V]+[P]).

Read-only checks so far (theory report line numbers in `<THY>`):
* #1 AA1 l.364: Lean `voxel_boltzmann_bounds` (VoxelEnclosure.lean l.33) is for any energy; moreover `certified_prodVoxel_partition` (VoxelBridge.lean l.348) is the end-to-end
  theorem "for any measurable energy enclosed voxelwise by two pairwise table models".  {P} stands — support: machine-checked statement (read, not compiled).
* #2 AA1 l.522 ({P}{?} disconnected family): report l.979–986 and §12 item 6 (l.11775–11789) call it open; our P7.5 gives a connected ring with ⌈n/3⌉+1 leaves. No support for {P}; → {?} alone.
* #3 AA1 l.679: Theorem 11.23 consequence (iii) (l.3240–3248): `max_j E|Q(g_j)| ≥ ((1−2δ)²/8)min(M,N)` [P] (R3 App. B).  Own sketch gives ≥ (1−2δ)min(M,N)/2 − ½ by the
  "run on g_j follows the run on g_∅ until hub j is queried" argument.  {P} stands (proof by another route, cited; sketched here).
* #4 AA1 l.762 ({P}{?} identical sites, Theorem 11.15): lower bound tensorises [V]; no upper bound for several types (§12 item 1(a) says only 11.9 has the finitely-many-types argument). → {?}.
* #5 AA1 l.1115 (Harper): not a hypothesis but a cited theorem; the alternative route (inherently typical subsets, Theorem 11.27 "R^gen is the exponent", l.3525–3552) gives
  exponents only, for accuracies with ln(1/ε) = o(n) — not the every-n bracket of 11.25(c) nor rows 4–6 of the table of (d).  {P} stands with that qualification.
* #7 AA1 l.195: stands (hand computation; S1 to be re-run).
* #8 AA1 l.491: Lean docstring of `inconsistentResidual_unguarded` (CertificateAlgebra.lean l.1076–1090): "Read with exact anchor semantics this is vacuous"; "the exact class is empty";
  D15's title: "Kernel soundness theorems that were vacuous on bad inputs".  "Minimum is 1" is the minimum of the pairwise part alone.  The soundness statement without consistency is
  VACUOUSLY TRUE, not false.  {F} → {E} (vacuous without it).  Minor.
* #10 AA1 l.891: report l.2518–2521 (D = {00,01,11} contains no rectangle, the class contains every function).  {F} stands (argument checked).
* #12 AA1 l.498: Lean `verify_sound_real` (CertificateAlgebra.lean l.960): termwise lower rational instance ⇒ bound for the real model.  {Q} stands; sufficiency machine-checked (read).
* #13 AA1 l.927: Proposition 11.18f (l.2848–2890): general statements hold for any law; "most frozen first" needs independent sites + exchangeable constants; otherwise "a search — it contains a
  minimum-weight hitting-set problem".  No weaker quantitative condition is stated. {Q} → {X} (or {C}{X}).  Minor.
* #14 AA1 l.1438: the audit says "a weighted ratio; not stated".  Own proof: energy difference and weighted Hamming distance both decompose over maximal runs of disagreement of a
  nearest-neighbour chain ⇒ one evaluation certifies iff Σ_{i∈I} c_i ≤ f(y) − f(x̂) for every y differing from x̂ exactly on an interval I (Theorem 2.4 [V] for any envelope).  {Q} stands; condition imprecise in the audit, sufficiency asserted there, proved here.  (The "exponential otherwise" half is not covered.)
* #15 AA1 l.768 ({?} additive instance, Theorem 11.15): §12 item 1 (l.11576–11603) leaves it open; nothing in DEAD_ENDS or our reviews. Stands.
* #16 AA1 l.1392 ({?} flexible geometry): no hit in the theory report, DEAD_ENDS, or our SCI-REV messages. Stands; note: the audit's own inertia bound (S6(c)) extends verbatim to
  bond lengths/angles in ranges (triangle width ≥ b_min·cos(θ_max/2)), so the growth of the torsion constants is decided; the theorem with bending/stretching as moves is not.
* #17 AA2 l.337: the condition is where the first sampled point is assumed to lie in the middle range (l.4755–4758).  Own sketch: a majority vote over the sampled points removes it at a
  constant factor when 2B/2ⁿ ≤ ¼.  {P} stands (support in the audit: none; decided here by a sketch).
* #18 AA2 l.446 (binomial median): an ingredient that is a theorem, not a hypothesis (proof idea of Lemma 11.55(b), l.5277–5279); any constant lower bound of the upper binomial tail would do.  {P} stands but is not an assumption.
* #19 AA2 l.617: Theorem 11.78(b) (l.7742–7752, exchangeable references; refereed R10) and Theorem 11.97(c) exist.  {P} stands (proofs by another route in the report; read only).
* #20 AA2 l.887 (βJ ≥ 0): report l.7966–7969 "nothing for antiferromagnets"; row G27 (l.1520): "otherwise Conjecture 11.94". → {?} (the audit says so in the same bullet).
* #21 AA2 l.1099 (extensive accuracy, Theorem 11.101): → {?} (same bullet says so).
* #22 AA2 l.1386 (stationarity and homogeneity in 11.116(e)): the statement is the existence of `F_∞ = lim F⁺_L/L` with brackets.  Counterexample to existence without homogeneity:
  couplings K₁ on [2^{2k+1},2^{2k+2}) and K₂ = 0 on [2^{2k},2^{2k+1}): by the report's own sub/super-additive reductions (a),(b) (valid for any chain) `F*_n/n` oscillates between
  ≈ (2/3,1/3) and (1/3,2/3) mixtures of F_∞(K₁), F_∞(0), which differ (h_∞ ≥ 0.0346 > 0.0291 at u = 1).  {P} → {F} for the limit ({Q}: stationary ergodic couplings, by Kingman — not proved).
* #25 AA2 l.931: report l.8296–8305 and harness DEAD.27 (98 304 > 15 011), XX.5.  The demonstration 393 216 > 79 931 is our own (SCI-REV-0003 M1).  {F} stands (read only here).
* #24, #26, #27: see the own-code log above.

## 2026-11-26T17:56:09Z — re-run of the audit's scripts (their code), from a scratch copy
* Copied the 15 scripts and 15 stored outputs to `rerun_copy/` (AA1: 7, AA2: 8; `rerun_copy/stored/` = stored outputs; `rerun_copy/tree/` = a copy of
  `docs/THEORY_REPORT.md` and `proofs/` in the layout `aa1_07` expects).  Nothing written into `<THY>`.
* Cost announced by the audits: seconds each, S5 of AA1 about 15 s, S4 of AA2 about two minutes, < 1 GB.  Expected total < 5 minutes; run one at a time,
  `OMP_NUM_THREADS=1`, `python3 -I -B`, timeout 1100 s each.  Runner: `rerun_audit_scripts.sh`; outputs `rerun_copy/out/`; summary log `logs/rerun_audit_<time>.log`.

## 2026-11-26T18:03:35Z — re-run of the audit's scripts done; remaining sampled items decided

* `rerun_audit_scripts.sh`, log `logs/rerun_audit_20261126T175609Z.log` (reached END): **15 of 15 outputs byte-identical to the stored ones**; times 0.0–117.5 s
  (AA2 s4 117.5 s, s5 39.7 s, s3 17.9 s, AA1 05 15.1 s).  The synthesis says "14 scripts": there are 15 (AA1: 7, AA2: 8).  [re-run, their code]
* Comparison of my Item-2 replications with their stored outputs (opened only now): S3 — N_cov = n+1 for n = 2..12 at margin 1/(2n), R*/δ → 0.2785: same facts as mine;
  S4 — 1.047910e-03, 4096, R(4) = 0.05591: identical digits; S1 test A — 1.085029, 1.205304, 1.389865, 1.418857 (p=0.3), 1.309135, 1.509678, 2.082706, 1.927748 (p=0.2),
  1.045763 at (0.1,4), 1 elsewhere, type-dependent 1.123018 at (0.2,1), families 64 / 1310: all equal to my v2 table.
* #23 AA2 l.352: S8 re-run identical; own brute force over 2^16 configurations (`item1_s8_owncheck.py`, `logs/item1_s8_owncheck_20261126T180027Z.log`): excess 1.6204 and 2.6204u, control βJ=0 → 0.
  The object refutes fact (F2) — a lemma of the proof — not the conclusion of Theorem 11.52; the audit says so itself in Entry 13 ("{?} for the statement, {F} for the proof").
* #28 AA2 l.200: report l.4261–4263 and Proposition 11.57(a) (l.5430–5434; [P], R8): stated; paper proof cited.  {Q} stands (read only).
* #29 AA2 l.594: bound Σ_i max_b KL(a_b^(i)‖r_i*) "by the same chain rule (not written)"; immediate (chain rule + convexity of KL in its first argument + site windows);
  in fact **machine-checked by this division** for general site classes: SCI-MSG-0014 (Proposition A1.2 items 1–3, `experiments/science/ws_L2/Window.lean`), which the report mentions only as "not adopted" (l.6259–6260).  {Q} stands.
* #30 AA2 l.1233: the report (l.10269–10270) quotes our SCI-RES-0006 §3 — "the adaptive bound loses a factor polynomial in 1/τ **and logarithmic in n (ingredients checked, not the whole)**" —
  without the last ten words.  For the uniform cube our SCI-MSG-0006 Theorem 4-τ is precise: the bound of 11.25(a) divided by |C| ≤ (2n)^⌈(k_τ−1)/2⌉, k_τ = ⌈ln(1/(τ−τ₀))/ln coth(u/2)⌉, i.e. a factor n^{O(ln 1/τ)};
  with a field it is a sketch of ours.  The {Q} has no precise condition and no proof: → {?} (with a field) / cite Theorem 4-τ (cube).
* #31 AA2 l.406 ({?}: "whether 'adaptive = hinted' holds for any interacting known part is open (O4)"): **decided in part by the report itself** — Proposition 11.81(c), l.7938–7943:
  "the adaptive exponent without a hint lies in [R_H, R_unif], and it equals R_unif — the first interacting known parts for which it is determined — wherever R_H = R_unif:
  for B = 0 and 0 ≤ βJ ≤ 1 (proved), and with two phases up to the junction of (b) (numerical)"; O4 itself (l.8086–8091) says "the conjecture holds wherever R_H = R_unif".
  So for the Curie–Weiss ferromagnet without field at βJ ≤ 1 (a non-product measure) adaptive = hinted is [P] (given Theorem 11.64; (c) "not refereed in turn").
  The {?} does not stand as phrased; the same over-statement of ignorance is in the synthesis §8 item 2 ("whether 'adaptive = hinted' is a property of product measures or of the problem") and §2 Level 3 ("adaptive exponent OPEN").
* #32 AA2 l.908: Conjecture 11.83 (C1): proved bracket 0.0251012 ≤ R_H(0⁺) ≤ 0.0291391; nothing in our reviews (SCI-REV-0001 reproduces the three numbers).  {?} stands.

### Tally of the sample (32)
{P} 12: stand 6 (support = proof by another route: l.364 [Lean], l.679, l.1115 (exponents only), AA2 l.617; support = nothing in the audit, decided here: AA2 l.337, l.446);
        → {?} 4 (AA1 l.522, l.762; AA2 l.887, l.1099 — each carries a sibling {?} in the audit itself); → {F} 2 (AA1 l.1262: own LP counterexample; AA2 l.1386: no limit without homogeneity).
{F} 10: stand 8 (AA1 l.195, l.743, l.891, l.1110; AA2 l.606, l.931, l.1114, l.1357); 1 is vacuity not falsity (AA1 l.491 → {E}); 1 refutes a lemma of the proof, not the theorem (AA2 l.352; the audit says so in Entry 13).
{Q} 6: condition precise and proved 3 (AA1 l.498 [Lean]; AA2 l.200 [P]; AA2 l.594 [asserted there, machine-checked by us]); imprecise, asserted, proved here 1 (AA1 l.1438);
        no quantitative condition at all 1 (AA1 l.927 → {X}); imprecise and resting on a sketch 1 (AA2 l.1233 → {?}).
{?} 4: stand 3 (AA1 l.768, l.1392; AA2 l.908); decided in part by the report itself 1 (AA2 l.406).

## 2026-11-26T18:03:51Z — coordinator's note received (mid-task): Item 3(b) has a second half
* The theory branch moved after `fc3f5d9`: at `d2150cd` (17:45 UTC; head now `4aea5fe`) the audit corrections were applied ("61 of 62 items (one declined)", recorded in
  `docs/audit/APPLIED_CORRECTIONS.md`); a further commit `ee41735` lists "seven further qualifications"; Theorem 11.33 now carries the hypothesis "the known part is additive".
* Second read-only export: `/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_4aea5fe/` (README.md, docs/ASSUMPTION_AUDIT.md,
  docs/audit/ incl. APPLIED_CORRECTIONS.md, docs/THEORY_REPORT.md).  Never write into it.  Called `<THY2>` below.
* To do, within Item 3(b), without enlarging the task: (1) state both facts with their commits; (2) for the five overstatements the synthesis calls the worst and for Theorem 11.33(a):
  the sentence at `fc3f5d9` and at `4aea5fe`, and whether the correction applied is the one the audit asked for; (3) name the one declined item and say whether I agree with declining it.
  Not to do: review the other 55 items.  The sample of Item 1 stays as drawn from `fc3f5d9`; the audit reports are cited by the old line numbering.

## 2026-11-26T18:09:30Z — Item 3(b): the state of the tree, both halves (read-only git + the two exports)

Blob identities (`git rev-parse <commit>:<path>`; the local repository has the theory commits):
| commit (time UTC) | THEORY_REPORT.md | README.md | docs/audit/APPLIED_CORRECTIONS.md | docs/ASSUMPTION_AUDIT.md |
|---|---|---|---|---|
| 7e6eb4c (15:44), b2cf817 (16:02), 020e990 (16:51) — what the audits read | 41cd501454 | 4455f2db1f | absent | absent |
| ff4ad64 (17:07) synthesis committed; fc3f5d9 (17:19) our object | 41cd501454 (unchanged) | 4455f2db1f (unchanged) | **absent** | c28756b2eb |
| d2150cd (17:45) "audits applied: 61 of 62 items (one declined)" | 337581b52e | 80b8a754e7 | eaace4d538 (created) | c28756b2eb |
| ee41735 (17:46) "seven further qualifications" | f13723cc91 | e1ea6ef019 | eaace4d538 | c1b16ba2af (+2 lines: a note on line numbers) |
| 4aea5fe (17:50) head given to me | 8895abb922 | e1ea6ef019 | eaace4d538 | c1b16ba2af |
Both exports are byte-identical to the git blobs at their commits (`git hash-object`).
* First half (true of fc3f5d9): the synthesis says the corrections "are recorded item by item in docs/audit/APPLIED_CORRECTIONS.md" (l.29–30, l.328–329) and
  that Theorem 11.33(a) is "corrected" (l.311); at fc3f5d9 the file does not exist and report and README are the blobs the audits read.  The sentences were written 38 minutes
  before the commit that made them true.
* Second half (true from d2150cd): the corrections are applied; the record has 62 items: 61 applied, 1 declined (O-18, the subtitle), 0 left to the coordinator; a section 5 lists
  eleven things "noticed on the way, not edited".  The synthesis at 4aea5fe differs from fc3f5d9 only by a two-line note on line numbers.
* Theorem 11.33 at 4aea5fe (l.3916–3962 new numbering): hypothesis "let the known part f be additive (a sum of site terms; in particular f ≡ 0)" restored; the Dobrushin sentence now
  says "for f + g … because f is additive"; a remark with the code and block counterexamples; row G15 and the closing paragraph qualified; D65 appended.  = what the audit asked (Err-1, E43, O-10).
* The four sentences the synthesis §7 calls the worst (five places), old → new: see the report §4.  All corrected in the sense the audits asked.
* Declined: O-18 (the subtitle "… for fixed-sequence articulated SE(3) heteropolymer chains"; reason: it is the programme's name as the owner gave it).

## 2026-11-26T18:11:32Z — Item 2, last part: the most consequential "positive fact" of §6 — the K-component sandwich (my choice; second: the inertia bound)
* Argument (AA1 E7): Z/Z₀ = Σ_k w_k E_{μ_k} e^{−βΔ}; Theorem 3.1(a),(c) [V] per product component; sum.  **Holds** (two lines; nothing to referee).
* Replication: `item2d_mixture_sandwich_v2.py`, log `logs/item2d_mixture_sandwich_v2_20261126T181110Z.log` (END; violations 0): 1440 random cases (n,q) ∈ {(6,2),(4,3),(8,2)},
  K ∈ {1,2,3,5}, three residual families, β ∈ {0.3,1,3}: 0 violations of either end.  Designed control (two modes Bernoulli(a)^n, Bernoulli(1−a)^n, Δ = |x|): the one-average
  product width fails in 26 of 30 cases (gap/width up to 7.3), the K = 2 bracket holds in 30 of 30.  The audit's S2(D) (re-run identical) shows the same.
* What the fact does not say: the K averages are averages under the COMPONENTS (the decomposition and its weights must be known exactly; each component sampled separately);
  every measure is a mixture of |X| point masses, so the content is in a small K; the width is still β²Σc_i²/8, extensive; a chain or an Ising model is not a small mixture.
* Second candidate, checked by argument: the inertia bound ≥ 0.0267·m·b² (AA1 E46, S6(c)): three consecutive atoms span a triangle of least altitude b·cos(θ/2); if all three were within
  r of a line they would lie in a strip of width 2r of their plane (the cylinder cuts the plane in an ellipse of minor axis 2r), so r ≥ ½·b·cos(θ/2); sum over ⌊m/3⌋ triples.  **Holds**
  (with ⌊m/3⌋ for m/3).  It bounds the VERIFIED constants of Theorem 4.6 from below on every domain, not the smallest valid constants.

## 2026-11-26T18:20:29Z — Item 3(a), 3(c), Item 4 (notes before writing the report)

### Item 3(a): the synthesis against AA1/AA2 (read: AA1 §§4–10 l.1476–1766, AA2 §A l.1428–1702, N_REPORT §6 and l.676–700, R_REPORT §0, §12)
* §1 counts: my mechanical recount inside entries reproduces all 14 numbers (AA1 52/16/26/39/13/47/23 = 216 tags; AA2 63/62/29/28/18/52/45 = 297 tags); N: 6/7/6/7/7/3/7 ✓.
  BUT units are mixed: AA1 §10 says "202 classified assumptions, 216 tags"; AA2 §A.7 says "tags … total 297" (its own sed/grep counts tokens).  The synthesis table calls both
  "classified assumptions" (202 and 297) and the per-kind AA1 column sums to 216, not 202.  "499 assumptions" = 202 assumptions + 297 tags; tags are 513; AA2's number of distinct assumptions is not stated anywhere.
* "Half of the assumptions are either load-bearing in the strongest sense (F: about one in five) or of unknown status (?: one in seven)": F = 99, ? = 68: F + ? = 167 = 32.6 % of 513 tags
  (33.5 % of 499): **a third, not half** (E + F + ? = 282 = 55 %).  "fewer than one in six is a pure convenience": C = 55 = 10.7 %: true, loose.
* "47 sentences": 22 + 25 ✓.  §7: "22 in AA1 (8/10/4)" ✓ (O-1…O-22: A = O-1,2,3,4,6,8,10,16; B = 5,7,9,11,12,13,14,15,17,19; C = 18,20,21,22); "25 in AA2 (5/11/9)" ✓.
  "Stale sentences (ten in AA1, one in AA2)": AA1 has SEVEN stale passages (Err-2…Err-8; AA1 §0 item 3 says "Seven"); ten is the number of AA1's errors Err-1…Err-10.
  "264 numbers" = 48 + 216 ✓.  "405 Lean names" ✓ (S7 re-run identical).
* "14 scripts … The coordinator re-ran all 14 scripts": there are 15 (7 + 8); my re-run: 15/15 identical.
* §6 header "All scripted, stored, and re-run by the coordinator": not true of three positive facts of the last bullet (coNP-hardness reduction, redundancy of (E), the K-level lower bound) and of
  the n+3 contradiction: AA1 §9 and AA2 §A.5 list them under "arguments written out in the entries (no script)".
* §2: every "lost" has its evidence where cited (S1 A/B, S8, S2, S3 re-run identical; Entries 15/25, 19, 26/57, 55).  Two inaccuracies: Level 3 "adaptive exponent OPEN" (the report's
  Proposition 11.81(c) determines it for B = 0, 0 ≤ βJ ≤ 1; AA2 A.1 at least had "(ferromagnetic Curie–Weiss: ≤ cube, 11.81(c))"); Level 5 "NOT available: any upper bound on the cost of any
  algorithm for a first-order class" while the same level lists Theorems 11.22–11.24, 11.26, which contain hinted upper bounds for every finite instance (11.22(e), 11.23(c), 11.26): should read "without a hint".
* §5 table: row 1 ✓ (E43: 10¹⁰/ε² at n = 100; n⁵ > 2ⁿ up to n = 22, ≈ 40 with the workstream's constants); row 2 ✓ (report l.3901–3902); row 3 ✓ (AA1 L1; β²S²/8 > βS iff βS > 8);
  row 4 ✓ (S7: cube YES at n = 20, 50, no at 100; 20 types × 3 letters vacuous at n = 100, 300); row 5 ✓ for (u = 2, θ = 1): 1.04·10¹¹ — but 4.9·10¹⁴ for the u = 1 cube exponent (out_s4 l.232–233);
  §3(g) quotes 4·10⁹, 1.7·10¹⁴, 10¹⁹ as sizes where the error "falls below the exponent itself": in out_s4 l.235–239 they are the sizes where q·n^(−1/(2q+2)) ≤ 0.05, a fixed number;
  row 6 ✓ (A.4 #24); row 7 ✓ (AA1 L5); row 8 ✓ (N_REPORT l.686: 0.197 for 0.0291; transport: no closing before the atom); row 9: no number in the synthesis, the number is in AA2 Entry 17
  ("from n ≈ 2.1·10⁴ on", L5615; "e^{142}" at n = 187; "Not a competitive design at any size where it can be evaluated"); row 10: R_REPORT §12 item 2 says "No certified UPPER constants at finite k;
  from below the bound is exact for the Gaussian pair" — the commit fc3f5d9 itself adds exact rational lower bounds at finite k.
* §8 item 2 / AA2 A.2 item 1 ("for no known part with interactions is the adaptive cost known, except 'at most the cube's' for mean-field ferromagnets") and A.3 item 1: contradicted by the report's l.7938–7943.

### Item 3(c): coverage (`item3c_coverage_v2.py`, log `logs/item3c_coverage_v2_20261126T181702Z.log`; v1 log `logs/item3c_coverage_20261126T181619Z.log`)
* 153 statement numbers of the report's own numbering (majors 2, 3, 4, 6, 11 and R4.1/R4.2): all named in an audit — none missing.
* No numbered Theorem/Lemma/Proposition/Corollary/Conjecture is stated in §§7–10, 12, 13; the report at fc3f5d9 has no appendix (last section "13. References") and nothing after §11.32 except §§12–13.
* Not audited as statements: §7 (implications), §8 (limitations), §9 (index; AA1 S7 cross-checks only names cited in §0.2, §§2–6, §§11.1–11.15), §10 rows G18, G20–G22, G24, G26, G27, G29–G40
  (19 of 40 rows are cited by row label in neither audit; their theorems are in AA2's entries), §12 items 1–14 (cited as evidence; items 7 and 12 not cited), §13.
* Statements of this division quoted under their own numbers and not named in either audit: Theorem R9.1 (adopted as 11.69b, audited there), Proposition R13.1, Theorem R6.1 / Corollary R6.2,
  Propositions R16.1, R10.1 (in remarks that the entries 12, 18, 74 cover), Conjecture R10.3 (§12 item 14(b); not covered).
* New at 4aea5fe and audited by nobody: Theorem 11.53a (commit b4fb594), row G41, the remark after Theorem 11.33 (labelled [P/N: audit AA1]).

### Item 4: five sampled citations (all five report our finding correctly)
1. AA1 l.839 SCI-REV-0012 ("11.18a, 11.18d reviewed by the Scientific Discovery Division (SCI-REV-0012, -0013)"): -0012 reviewed 11.18a, 11.18b, 11.18c ("everything is correct except two statements of 11.18c"); -0013 reviewed "Theorem 11.18d as written". Correct.
2. AA1 l.1380 SCI-REV-0006 ("wording corrected by SCI-REV-0006, -0009", lever-arm law): our M4/W6, itself corrected by SCI-RES-0007 §2 and SCI-REV-0009 §2 ("what remains of M4 is the wording"). Correct.
3. AA2 l.449 SCI-REV-0016 (abort test before every query; "proves C_max + M̄, not C_max"): our m1, verbatim. Correct — but the bullet is tagged {F}, and our m1 says "No run exceeding C_max was constructed;
   none among the 2 648 stored runs": the evidence is a gap of a proof (the proved bound becomes C_max + M̄: a {Q}), not a counterexample.
4. AA2 l.944 SCI-REV-0003 (restriction "for a fixed η" added after our review): our m1; and "one major finding (the stopping rule), nine minor" (l.923) = our verdict; 393 216 / 79 931 are our numbers. Correct.
5. AA2 l.1071 SCI-REV-0005 (operational sentence of Theorem 11.99: ranges, worst case — "added after SCI-REV-0005 m1"): our m1. Correct.
Reverse direction (findings of ours not in the audit): see the report §5.
cost note: n = 3, 48 instances x up to 256 subsets x 9 LPs; expected 2-5 minutes, < 200 MB

## 2026-11-26T18:24:30Z — the quantitative substitute for additivity in Theorem 11.32, tested
* `item1_thm1132_quantitative.py`, log `logs/item1_thm1132_quantitative_20261126T182132Z.log` (reached END; 88.7 s; violations 0): n = 3, 12 instances per κ (random f or e|x|, residual additive + pairwise with |a_ij| ≤ κc),
  N₂ exact by LP over all evaluation sets.  Statement S (K₋[(1−κ)c] ≤ N₂): 0 violations at κ = 0, 0.5, 0.9.  The theorem's display with the full constant (K₋[c] ≤ N₂) fails in 0 / 3 / 10 / 8 of 12 instances at κ = 0 / 0.5 / 0.9 / 1:
  **the failure is generic for non-additive members, not confined to the boundary.**  Replacement tag for AA1 l.1262: {F}{Q}.
* Proof of S (two lines): g − (1−κ)·b_{y,r} is a member (|D_iD_j| ≤ κc + (1−κ)c), equals g off B(y,r−2), is lower by (1−κ)c·C(r,2) at y ⇒ lower bound with (1−κ)c;
  after stars at A₀, h = g′ − g has |D_iD_jh| ≤ (1+κ)c and vanishes on the stars ⇒ |h(y)| ≤ (1+κ)c·C(d_H(y,A₀),2) (Theorem 11.31(b) [V] for the constant (1+κ)c) ⇒ upper bound with (1+κ)c.

## 2026-11-26T18:32:18Z — report drafted (`docs/science/workstreams/R23_REPORT.md`); (S2) tightened
* First draft of the full report written before this entry (file complete: sections 0–7).  [This line first read "at about 18:40" — a time not read from the clock: own error E9, the third of its kind, corrected at once.]
* (S2) rewritten so that it needs no closing of the brackets: blocks of lengths 2^{j²}, coupling K₁ in the odd blocks, 0 elsewhere; at the end of an odd block
  F*_n/n ≥ F⁻(B_last)/n → sup_L F⁻_L/L ≥ 0.0346 (AA2 S3), at the end of an even block F*_n/n ≤ F⁺(B_last)/n + o(1) → F_cube(t) ≤ 0.029139.  (My first version, with dyadic blocks,
  needed 2·F⁻_∞ − F_∞ > F_cube, i.e. the report's bracket [0.0401, 0.0450]; own error E8, corrected before hand-back.)
* Finding labels: major F1–F4, G1, and the record at fc3f5d9; minor f5–f15 and g2–g8 (18).

## 2026-11-26T18:36:33Z — closing entry
* Report complete: `docs/science/workstreams/R23_REPORT.md` (sections 0–7).  Final classification: critical 0; major 5 (F1 Theorem 11.32 {P}→{F}{Q}; F2 Theorem 11.116(e) {P}→{F};
  F3 the P row adds up three different things; F4 "adaptive = hinted is open for any interacting known part" against Proposition 11.81(c); the record at fc3f5d9); minor 19 (f5–f15, g1–g8).
  ("Half of the assumptions…" was first classed major, then minor (g1): a wrong fraction in a summary sentence, no conclusion depends on it.)
* (S2) final form: zero coupling between blocks ⇒ the chain is a product of blocks ⇒ site functions add at a common t (Theorems 11.98–11.99); K₁-blocks ≥ 0.034624 per site at t = 0.45
  (S3, blocks of 12 with gaps of 1, reduction (b)); uncoupled blocks = F_cube ≤ 0.029139 per site; per-site ceiling via reduction (a).
* Lean: the class of Theorem 11.31/11.32 is two-sided (`MixedDiffBound`, SecondOrderEnvelope.lean l.106: |…| ≤ c) — as in my LP.
* Rates: {P} 6/12, {F} 8/10, {Q} 4/6, {?} 3/4.  Tool actions declined: none.  No state-changing git command was run (read-only: cat-file, rev-parse, hash-object without -w, log, diff).
* Nothing was written outside `experiments/science/ws_R23/` and `docs/science/workstreams/R23_REPORT.md`.
* 2026-11-26T18:38:14Z: `HANDBACK.md` written (the text handed back to the coordinator, kept here in case the hand-back is lost); report file list updated.
