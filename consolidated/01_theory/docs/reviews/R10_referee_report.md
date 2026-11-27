> **Repository note (added by the coordinator).**  Report of the independent referee R10 on
> workstream T (`docs/workstreams/T_REPORT.md`) and on theory report §11.23 (brief:
> `docs/reviews/R10_brief.md`), as delivered on 25 November 2026.  `<scratch>` is the session's
> scratch directory; the referee's scripts are in `experiments/reviews/R10/` (libraries
> `r10lib.py`, `r10search.py`, `r10slp.py`, `r10tab.py`, `r10fin.py`; tests `t00_…` – `t24_…`; queues
> `queue1.sh` … `queue6.sh`, `run_de_e0.sh`; run from that directory as in §9 of the report),
> their outputs in `experiments/reviews/R10/out/`.  Not copied: the directory `parts/` (the
> sections of this file), the referee's extracts of §11.23 (`sec1123_*.txt`, copies of the
> theory report at three commits) and two backup files.  Line numbers of the workstream's
> report refer to it as delivered (see the errata note at the head of `T_REPORT.md`); line
> numbers of the theory report refer to commit `89ac710` and have moved since.
> **What was done with the findings** (twelfth checkpoint of cycle 10): theory report §11.23 —
> status paragraph; M1 in Proposition 11.81(b) (rewritten), finding 4 of the section head,
> Corollary 11.91(iii), the consequence of Conjecture 11.94, §8, §10 (G25), §12; M2 in
> Proposition 11.82(e), Theorem 11.79(c) and Conjecture 11.83 (O5); m1–m15 at the places they
> concern (m10, m12, m13 are numbers in Proposition 11.82; m3, m4, m5, m7, m8, m14, m15 are in
> the proofs of Theorems 11.78–11.80 and Proposition 11.81(a); m2, m6 in the setting; m1, m9,
> m11 concern the workstream's report only and are in its errata); D1 (the argument for
> `R̄_H = R̂` at all accuracies) in Theorem 11.80(c); D4, D9, D10 reworded; D13 (conventions
> for a non-symmetric envelope) in the remark after Theorem 11.76; **the referee's
> completion of T12 is now the proof of Proposition 11.81(c)** (checked by the coordinator;
> not refereed in turn); the new data points (seven-atom profile at `e = 0.05`; the free
> block with a field) in Proposition 11.82; the harness has the documented refutation
> DEAD.25 for M1 (the coordinator's own re-computation of the referee's first
> counterexample) with two mutations; `docs/DEAD_ENDS.md` D53 records the lessons;
> `docs/collaboration/messages/theory/THY-MSG-0012.md` carries the linked correction of
> THY-MSG-0009.  The note at the end of §8 of the report is accurate: the eleventh
> checkpoint cited finding M1 from the referee's draft before the report was handed in
> (D53 item 7).

# R10 — Referee report on workstream T: "known parts with interactions, first case: a function of the type (mean-field models)"

Object reviewed: `<scratch>/ws/T/T_report.md` (final version, 1271 lines; **line numbers below refer to it**; the copy
`docs/workstreams/T_REPORT.md` is identical after a repository note of 22 lines), and its rendering in
`docs/THEORY_REPORT.md` §11.23 (Theorems 11.76–11.80, Propositions 11.81–11.82, Conjecture 11.83).  Context read:
`F_REPORT.md` §§2–3.4 with its errata, `A_REPORT.md` §§2.0–2.3, `R9_referee_report.md`, theory report §11.10 (Theorem
11.22), §11.16 (Theorem 11.45), §11.20 (Theorems 11.63–11.64, Proposition 11.65), the structure `GameFunction` of
`proofs/Frontiers/GamePair.lean` and the statements of `SymmetricSampling.lean`, `TypeQuantiles.lean`, `GroupSampling.lean`.

**The theory report moved while I worked.**  I first read §11.23 in the working tree on HEAD `63efc69` (about 15:10 UTC;
then lines 5068–5514).  Commit `e4351b9` (15:49) contains the section with — as far as I can reconstruct the earlier,
uncommitted state — one addition of substance: a *Remark (an arbitrary symmetry group)* after Theorem 11.76, with a
sentence about it in the status paragraph and in "Extensions" (and one more documented refutation in the harness
paragraph).  Since then the section has not changed: it is identical in `e4351b9`, in `5ed4072` (17:16) and in `89ac710` (18:33; HEAD when I
finished; file sha256 `d62f9900…a102`; my extracts are in `out/sec1123_*.txt`).  I re-read that version in full; every finding below
applies to it, and **theory-report line numbers below refer to it (§11.23 = lines 5112–5593)**.  The remark is treated in
§8 (D13).  Sections 11.24–11.27, which appeared or grew in the meantime, are outside the brief and were not reviewed.

Everything of mine is in `<scratch>/referee10/` (`R10_report.md`, `code/`, `out/`, `parts/` = the sections of this file).
Nothing under `/home/user/MetricChain` was modified; no state-changing git command; no `lake build`; no subagent.  Python
under `ulimit -v 4000000`, one process at a time, every run under ten minutes, fixed seeds, own code (the author's and the
coordinator's code was neither run nor reused; what I read of it is listed in §10).  25 November 2026.

## 0. Summary

**Overall verdict.**  The mathematical core of the report stands.  **No critical finding.**  Every statement labelled
[proved] is proved, some after small repairs that I give; the numbers that I recomputed (about ninety, from every table
named in the brief) agree with the report — in four places only up to the last printed digit — with two exceptions in the
third digit (`a_cone`, `e₀`).
Two statements say more than is established, and one of them is false as a general statement:

* **Theorem T3(b) — the isoperimetric theorem for the type-uniform measure, every rate function: proved.**  I went through
  Steps 1–6 against F6 and the R9 record (§3).  The one change — Lemma T applied to a subset of one type class with the
  product measure `Bernoulli(k/n)ⁿ`, which is uniform on that class — is legitimate: the lemma is a statement about an
  arbitrary set and an arbitrary product measure with constants that do not depend on the measure, `P_X` is exactly
  `Bernoulli(k/n)`, and `α = I(X;U)`.  Step 6 really is simpler than in F6.  Only cosmetic repairs (the last line needs
  `R̄_λ`, not "`R_λ` is nonincreasing"; small `n`; lattice against continuum landscape).  **Lemma T8′** (`R̄_H` is 1-Lipschitz
  for every rate function) is proved, given T3.  The consequence "hinted exponent `= R_λ(ε₁)`" follows from Theorem
  11.22(e) as claimed.  The `μ_H` version (last paragraph of §4.2) is an assertion that I could complete; it is not used.
* **The convex case (T9, T10): proved.**  Binary centres suffice — the Sion step and the envelope argument are correct,
  also at the junctions of the pieces, for degenerate `Q`, and the exchange "two block types for each `τ`" ⟹ `R_H = R_H^{(2)}`
  is harmless.  `F*` satisfies every field of `GameFunction` (the argument for `E > 0` needs a repair).  "Ferromagnets are
  never harder than the uniform cube" is proved, given Proposition 11.65(b) and Lemma SL.  The equality "cone formula =
  sup–min" (T9(d)) is numerical, as labelled; it also holds in twelve cases that are not Curie–Weiss.
* **The every-`n` statements (T1, T2, T2′, T4, T5) and the lemmas (T6, T7, T8): proved** (T8(b) after a one-line repair for
  negative accuracies); the summary display of T1 is misprinted (the extremal function is non*de*creasing in `q`; `inf`, not `sup`).
* **Two phases.**  With three inner solvers that share no approximation and three search methods (one of them new: a
  linear programme over the law of the block types) I could **not refute conjecture C1**: no profile with
  `r_μ(0) > 0.0251012` in 86 searches at `e = 0`, nor a non-binary optimum in 37 searches with a field or in 37 just below
  `e₀`.  At `e = 0.02` I find the report's profile and nothing better (`0.0161548`); at `e = 0.05` a seven-atom profile gives `0.0063875` against the report's
  `0.0063867` (a proved lower bound, `+8·10⁻⁷`); with a field `βB = 0.05` the free block appears too (`0.0160758` against the
  binary `0.0152121` at `e = 0.02`; not searched in the report).  The crossing is at `e₀ = 0.001804`.  The failure of the pair
  identity for cones around profile classes at `u = 0.30` is reproduced (`0.00184002` against `0.00226456`).
* **MAJOR M1 — the junction formula is false in general.**  "For `1 < βJ ≤ βJ*(e,u) = 1 + u·c₂/(2L)` the local minimum is
  global, so `R_H(e) = R_unif(e)`" (§6.6 (iii), summary G3(e); theory report, Proposition 11.81(b) and finding 4) is true
  where the report computed it (`u = 1`) and on my grid for `u ≤ 2`, but fails for larger `u`: e.g. at `u = 8`, `e = 0`,
  `βJ = 8.26 < βJ* = 8.34` and at `u = 4`, `e = −0.362`, `βJ = 4.958 < βJ* = 4.998` the *constant* exit at a well is feasible for
  the uniform cube's profile, whose value is `0`, and the best profile found — binary; multi-block searches give nothing
  better — is below `R_unif` (`0.3674` against `0.3985`; `0.41763` against `0.41857`).  The local statement (ii) and
  the formula for `βJ*` are correct; the junction is at `min{βJ*, βJ_w}` on my grid, `βJ_w` the coupling at which the barrier
  reaches `E_unif(u) − e`.
* **MAJOR M2 — an interval that is not proved.**  "At `u = 0.30` the non-adaptive exponent is only known to lie in
  `[0.00184, 0.00226]`" (§6.5 (4), O5; theory report, Proposition 11.82(e)): the upper end is the binary value, a *lower*
  bound of `R_H(0)`; what is proved is `[0.00184, 0.00338]`.
* **The sketch T12** is correct as far as it goes and, in my judgement, provable: the step it names as missing
  (uniformity in `p`) can be avoided by absorbing the variation of the field inside a cell of a *finite* net into the
  residual, at the price `u → u + 2Δ` (§7).  The analysis of why the nested algorithm fails is correct; I see no
  immediate obstruction to the coordinator's proposed repair, and say in §7 what it would have to supply.
* **Theory report §11.23** renders the report faithfully; twelve differences are listed in §8.  Two of them are M1 and M2
  (shared with the report); one says more than the report proves but is true (`R_H = max_t[F*(t) − te]` for all `e`, with
  `R̄_H` — I supply the argument); the rest are minor.  A thirteenth item (D13) is the remark on arbitrary symmetry groups
  that was added to the section during the review and is not in the report: its paper content is correct (checked: (a′),
  (b′), (c′) and the sampling bound; two conventions should be stated for a non-symmetric envelope); its Lean file was read,
  not compiled.

## 1. Verdict per statement

"hand" = re-derived line by line; "num" = own numerics (§§6, 9).

| statement (lines) | verdict | how checked; remarks |
|---|---|---|
| **(2.1)–(2.3)**, setting (58–117) | **proved**; (2.1) as stated needs a Lipschitz `φ` (m2) | hand; (2.3) and `A(ψ^D)/A(ψ) = 1 + Φ` by brute force, 266 cases, `1.4·10⁻¹⁵` |
| **T1(a)** quantiles are Lipschitz (129–131, 145–150) | **proved** | hand; num (108 cases) |
| **T1(b)** (i), (ii) (132–135, 151–161) | **proved** | hand: hypotheses of Theorem 11.45(a); Chernoff/Markov constants |
| **T1**, summary display (136–142) | **proved after a repair** (m1) | `ε_n^{tr}` is nondecreasing in `q`; `q* := inf{q : ε_n^{tr}(q) > ε}`; upper bound for every `q < q*`.  The bold conclusion is right |
| **T2** (167–181) | **proved** | hand: hypotheses of Theorem 11.22(c) |
| **T2′** (183–195) | **proved** | hand; my block sums against brute force, 236 cases |
| **T4** (199–207) | **proved** | hand; num: `Z_gΦ_g⁺ ≤ Z_HΦ_H⁺` never violated; a factor `Z_H/Z_g > 1` is attained (up to `2.51` in my cases), so some factor is needed; `n+1` is a bound of it |
| **T5** (211–228) | **proved** | hand (cells, quantile, no unimodality); two entries of §6.3 reproduced |
| **T6** clipping (236–246) | **proved** | hand (KKT, monotonicity); num: S2 (no clipping, `I`) = S1 at every optimum |
| **T7** `v` or `I` (248–258) | **proved** | hand (thinning, data processing) |
| **T3(a)** (264–271, 281–284) | **proved** (unstated: `D ≠ Q_n`; lattice approximation) | hand; exact sums at `n = 60, 120, 240`, 48 cases |
| **T3(b)** (272–277, 285–312) | **proved** (cosmetic repair m3: `R̄_λ` in the last line) | hand, Steps 1–6 against F6/R9 (§3); num: 402 multi-centre and centreless sets at `n = 200`, all subsets of `Q_3`, `Q_4` |
| **T3**, consequence: hinted exponent `R_λ(ε₁)` (278–280) | **proved** (at continuity points; every `ε₁ > 0` for `H`) | hand: hypotheses of Theorem 11.22(e), §3 |
| §4.2, last paragraph: the same for `μ_H` (313–315) | **proved after a repair** (it is asserted; completion in §3; "Lipschitz" → uniform continuity); **not used** | hand |
| **T8(a)** (319–323, 336–341) | **proved** | hand; num: `n_μ` against the directly truncated shell-cone |
| **T8(b)** (324–329, 342–343) | **proved after a repair** (m4: `R̄_H`, non-admissible profiles at `e < 0`) | hand |
| **T8(c)** (331–335, 344–346) | **proved**, given T3(b) in the `maxdens` form, with `Φ⁺`, all real `e`, `R̄` — which is the form stated (m5: left limit at jumps of `R̄_H^{−1}`) | hand |
| **T8′** (348–364) | **proved**, given T3 | hand (§3) |
| **T9(a)** (379–380, 406–410) | **proved** | hand (Sion twice; no Slater condition needed); num `5·10⁻¹⁰` |
| **T9(b)** (381, 411–429) | **proved** | hand (§4); num: no multi-atom profile above the binary optimum in 16 convex cases and for the zero residual with two phases |
| **T9(c)** (382–391, 430–440) | **proved after a repair** (m7: argument for `E > 0`); strengthening: `R̄_H = R̂` for all `e` | hand, field by field against `GameFunction`; num: pair identity `1.3·10⁻⁸`, convexity, slopes |
| **T9(d)** (392–394, 441–443) | "`≤`" **proved**; "`=`" **not proved** (numerical, as labelled; what is missing: the sketch of lines 427–429 written out — it can be, §4) | hand; num: equality `≤ 5·10⁻⁹` in 14 cases, 12 of them not Curie–Weiss |
| **T9(e)** (395–404, 444–452) | **proved**, given Proposition 11.65(b) and Lemma SL; the sentence on `θ_na` **after a repair** (m8) | hand; num |
| **T10** (454–459) | **proved**, given Theorem F10(c) | hand: every step of F10(c) uses exchangeability only |
| §5.3 table | reproduced (2 rows, all columns) | num |
| §6.2 (A), (B): values at given profiles | reproduced; each is a proved lower bound (T3(a)) | num, three inner solvers |
| **C1** (928–929) | **not refuted** — a conjecture, as labelled | num: §6.1 |
| "`e₀ = 0.00181`" (19, 624) | `0.001804` (m10) | num |
| "`a_cone = 0.0446`" (18, 603, 675) | `0.04435` (m12) | num |
| §6.3 exact sums | reproduced (4 entries) | num, own exact sums |
| §6.5 table and (4) | reproduced (3 rows; the failure of the pair identity at `u = 0.30`); the bracket `[0.00184, 0.00226]` is **not proved** (M2: its upper end presupposes `R_H = R^{(2)}` near `e = 0` at `u = 0.30`; proved: `[0.00184, 0.00338]`) | num; hand |
| §6.6 (i) | **proved** (= T9(e)) | hand |
| §6.6 (ii), formula for `βJ*` | **proved** (local) | hand; finite differences |
| §6.6 (iii), §0 G3(e): "for `1 < βJ ≤ βJ*(e,u)` that local minimum is global, so `R_H(e) = R_unif(e)`" | **false** as a general statement (M1).  The premise fails by an explicit feasible exit (counterexamples `u = 8`, `e = 0`, `βJ = 8.26`; `u = 4`, `e = −0.362`, `βJ = 4.958`; eight more cells); the conclusion fails on the evidence of searches (best profile found `0.3674 < 0.3985`, `0.41763 < 0.41857`).  True in the range the report computed and for `u ≤ 2` on my grid | num (two solvers for the premise; three solvers and multi-block searches for the conclusion) |
| §6.6, "continuity in general" (825–826) | **proved** | hand |
| §6.7 (i), local formula `A(λ_f)` | **proved** | hand |
| §6.7 tables | reproduced (`βJ = 1.2, 1.3, 2`; field at coexistence) | num |
| §6.7 (ii), (iii); §6.4; §7.3 | **not checked** (numerical statements of the author) | — |
| §7.2 small cubes | conclusion confirmed; the reason given is inaccurate (m11) | num |
| §8.1 (why the nested algorithm fails) | correct | hand |
| **T12** (1015–1037) | a **sketch**, as labelled; the representation is correct; provable, and the missing step is avoidable (§7) | hand; num (`t14`) |
| §9 prior art | consistent with the abstracts | web (§7) |
| theory report only: *Remark (an arbitrary symmetry group)* after Theorem 11.76 (theory report 5235–5267) | **proved** on paper — (a′), (b′), (c′) and the sampling bound — with two conventions to be stated for a non-symmetric envelope (§8, D13); the "[V]" part: statements read, not compiled | hand |

## 2. Findings by severity

### CRITICAL
None.

### MAJOR

**M1.  The junction with the uniform cube: the claim "(iii)" is false as a general statement.**
*Where:* report §6.6, Statement (iii) (lines 818–820) and the conclusion "the junction is not at the critical coupling but
at `βJ*(e,u) > 1`" (821–822); §0, row G3(e) (line 23): "for `1 < βJ ≤ βJ*(e,u) = 1 + u·c₂/(2L)` … the two-phase exponents are
*equal* to those of the uniform cube"; theory report, Proposition 11.81(b) (lines 5414–5419: "numerically it is then the
global one, so `R_H(e) = R_unif(e)` for `1 < βJ ≤ βJ*`") and finding 4 of the section head (5138–5140: "up to a coupling
`βJ*(e, u) > 1`"); inherited by Proposition 11.81(c) (5424–5425), by the harness description XIX.4 (5565–5567: "equality
with the uniform cube below it") and, in the report, by the corollary of T12 (line 1021).  The row G25 of the summary table
(line 1353: "coincide with it up to a coupling beyond the critical one") and the three regimes of §6.7 (lines 880–881;
Proposition 11.82(c), 5466–5469, both in the context `u = 1`) say less and are consistent with my grid, on which the
junction `min{βJ*, βJ_w}` is always beyond `1`.
*What is true:* (ii), the local statement and the formula for `βJ*` — re-derived and checked by finite differences; and
(iii) at the parameters of the report's table (`u = 1`; `e = 0`, `0.02`, `0.04`).  On my grid it holds for `u ≤ 2` at seven
accuracies from `0.9e_c` to `0.9E`, at `e = 0` for `u ≤ 6`, and for every `u ≤ 8` when `e ≥ 0.3E_unif`.
*What is false:* that the symmetric exit, while locally stable, is the global minimiser for all `(e,u)`.  For the uniform
cube's profile `μ* = (½; p_u, p_u)` the constant exit at a well `κ_w` has `MI = 0` and is feasible as soon as
`u·dist(κ_w𝟙, μ*) + I(κ_w) ≤ e + KL(p_u‖½) + I(½)`, i.e. as soon as the barrier `I(½)` reaches
`E_unif(u) − e + u·(p_u − κ_w)⁺` (by `u/2 − KL(p_u‖½) = ln cosh(u/2) + u·p_u`; the cheapest constant exit is in fact at the
edge of the well's contact interval, where `I′ = u`, which lowers the threshold by another `2·10⁻⁴` in the first example
below), and for large `u`, or for `e` near `e_c`, this happens below `βJ*`.
*Counterexamples* (`B = 0`; S1 and the independent S2 agree; `out/t07c_junction_grid.txt`):
`u = 8`, `e = 0`, `βJ = 8.2632 < βJ* = 8.3366`: `R_unif(0) = 0.3985436`, `r_{μ*}(0) = 0` (`u·dist + I = 4.00000 ≤ e + α = 4.12859`), best
binary profile found `0.36742`; `u = 4`, `e = 0.6e_c = −0.36183`, `βJ = 4.9578 < βJ* = 4.9978`: `R_unif = 0.4185706`, `r_{μ*} = 0`
(`2.00005 ≤ 2.02703`), best binary profile `0.41763`; also `u = 3` at `0.9e_c`, `u = 6` at `0.3e_c`, and six further cells.  In
these four the top of the barrier is still a contact point (in some of the others it is not).
*Is `R_H` itself below `R_unif` there?*  By the chain of T9(e) a profile that restores `R_unif` would have to be a type-`½`
optimal profile of the uniform cube.  In the two cells with numbers above I searched (run `t24`; 16 and 23 starts: binary,
diluted, four-atom, frozen, off-centre profiles and random splittings, alternating SLP/Nelder–Mead): nothing exceeds the
binary shell at the edge of the cliff, `0.3674161` against `R_unif = 0.3985436` and `0.4176288` against `0.4185706` (each
confirmed by three inner solvers at a profile where the constant exits are infeasible by a margin `2·10⁻⁵`; §6.4).  So the
conclusion `R_H = R_unif` is not only unsupported there but, on this evidence, false; this half is numerical, the first
half (the value of `μ*` is `0`) is an explicit feasible exit.
*Repair:* state (iii) for the range computed, or as "the junction is at `min{βJ*(e,u), βJ_w(e,u)}`", `βJ_w` the coupling at
which a constant exit becomes feasible for `μ*` (`min_c[u·dist(c𝟙, μ*) + I(c)] = e + KL(p_u‖½) + I(½)`) — which is what my grid
shows (failure exactly in the cells with `I(½)|_{βJ*} > E_unif − e`; the correction `u·(p_u − κ_w)⁺` decides no cell of the
grid), numerically.  The label [numerical] of (iii) is honest;
the generality of the sentence, of the summary and of Proposition 11.81(b) is not supported.  Nothing else in the report
depends on it (T12's corollary "for `1 < βJ ≤ βJ*(ε₁,u)` the adaptive exponent is `R_unif`", line 1021–1022, inherits the
restriction).

**M2.  "Only known to lie in `[0.00184, 0.00226]`" — the upper end is not proved.**
*Where:* report §6.5 (4) (lines 774–777), §0 row G3(d) (line 22: "the non-adaptive exponent is open there"), §7.1 O5
(936–937), §12 item 7a (1199–1200); theory report, Proposition 11.82(e) (5494–5497) and Conjecture 11.83 (O5) (5514–5516).
*What is proved:* the lower end, `N(S(0)) ≥ 0.00184002` (a shell-cone around `x = 0.45138`; reproduced three ways), and the
failure of the pair identity *for cones around binary classes* (`n_{μ*}(S(0)) = 0` at the optimal, marginal shell).
*What is not:* `θ_na(S(0)) ≤ 0.00226`.  (So the report's alternative "either functions other than cones around profile
classes do better, or the shear law fails there" omits a third possibility: `R_H(0) > R^{(2)}(0)` at `u = 0.30`.)  Theorem T8(c) bounds `θ_na(X)` by `inf{θ : θ + R̄_H^{−1}(θ) < X}` with the full supremum
`R_H`; `0.00226456 = R^{(2)}(0)` is a lower bound of `R_H(0)`.  From `R̄_H ≤ R̂_unif` (T9(e)) the proved bound is
`θ_na(S(0)) ≤ R_unif(S_unif^{−1}(0.0022646)) = 0.00337705`.  So the proved bracket is `[0.00184, 0.00338]`; `[0.00184, 0.00226]`
is conditional on `R_H = R^{(2)}` for `e ≤ 0` near `0` at `u = 0.30` (the analogue of C1; one 3-block search of the author,
24 multi-block runs of mine, `t22`, none above the binary shell).  The same remark applies, less visibly, wherever "the pair
identity holds" is said about `θ_na` rather than about `n_{μ*}`: the upper bound always needs the value of the full supremum.
The report is careful about this at `u = 1` (lines 600–601, 644–645) and not here.

### MINOR

**m1.  Theorem T1, summary display (lines 130, 136–138).**  `ε_n^{tr}(q)` is nondecreasing in `q`, not "nonincreasing";
`q*(ε)` must be `inf{q : ε_n^{tr}(q) > ε}`, not `sup` (as printed, `q* = 1` and the display is void/false); the upper bound
holds for every `q < q*` ("`q*⁻`", not "`q*⁺`").  The proofs of (a), (b) and the bold conclusion are correct.

**m2.  (2.1) (line 69) and "`Z ≤ (n+1)^{1+c_φ}`" (269)** are stated for continuous `φ` with a constant `c_φ`; for a merely
continuous `φ` the bound is `3ln(n+1)/n + ω_φ(1/n)`.  Everything that uses (2.1) needs only `o(1)`.

**m3.  T3(b), last line of the proof (310): "`R_λ` is nonincreasing".**  Not automatic for `e < 0` (admissibility).  Use:
`R̄_λ` is nonincreasing and `r_μ(x) ≤ R̄_λ(e′)` for `x ≥ e′` (non-admissible `μ` have `MI(μ) < −e′`).  Also unsaid: the trivial
`ω_n` for `n ≤ 4u⁴ln²3`.  (§3.)

**m4.  T8(b) (lines 326, 343).**  For `e < 0` the step `n_μ(X) ≤ r_μ(e)` needs `μ` admissible at `e`; otherwise
`n_μ(X) ≤ MI(μ) < −e`.  The statement is `N(X) ≤ min{R̄_H(e) : e + R̄_H(e) ≤ X}`.

**m5.  T8(c) (line 331).**  At a jump of `R̄_H^{−1}` (a flat piece of `R̄_H`) the bound is `θ + R̄_H^{−1}(θ⁻) + o(1)`; the
infimum that is used is the same.

**m6.  `ψ_H = −V_n(|x|)` against `ψ_n = −nv(|x|/n)`.**  T4, T8(c), T8′ use the lattice instance, T3 the continuum one;
`|V_n(t) − nv(t/n)| = O(log n)` uniformly, so `Φ_H⁺` changes by a polynomial factor.  Nowhere said.

**m7.  T9(c), `E > 0` (line 434).**  "Every constant `ν` is at distance `≥ η`" is not an argument for a positive Lagrangian
value; repair in §4 (`MI(ν) ≥ ½(ν₁−ν₂)²`, `dist ≥ η − ½|ν₁−ν₂|`).  And the theorem can be stated as `R̄_H = R̂` for all `e` (§4).

**m8.  T9(e), "`θ_na(x) = min{KL(ρ‖½) : KL(ρ‖p_u) ≤ x}`" and "all exponents are those of the uniform cube" (lines 401–402,
17).**  The proof compares `r_μ(e)` only; `θ_na` needs the comparison of the game functions (negative accuracies).  It holds
by the same argument applied to the Lagrangian (§4).  Also the case "not admissible for the field problem" is not
treated (one line).

**m9.  §4.2, last paragraph (lines 313–315).**  An assertion ("then Step 6 as in §11.20 gives …"), with a justification
("`I − v` Lipschitz near the contact set") that is not needed and not true for a merely continuous `φ`.  Completed in §3
with uniform continuity.  Used only in §7.1 (first bullet) and §7.2.

**m10.  `e₀ = 0.00181` (lines 19, 624, 1139; theory report 5461; the section head, 5135, has `≈ 0.0018`, which is right).**  The crossing of the two branches is at
`0.001804` (root of the difference of my two maximisations; the author's own numbers at `0.002` give the same); `0.00181`
is a linear interpolation between `0.001` and `0.002`.

**m11.  §7.2 (line 955): "`Φ_H⁺(D) < 1` for most sets".**  On `Q_3`/`Q_4`, `Φ_H⁺ > 1` for 191 of 254 and 49 151 of 65 534
subsets.  The conclusion (the test is void) is right for a sharper reason: every set with `Φ_H⁺ > 1` has `maxdens = 1`.

**m12.  `a_cone = 0.0446` (lines 18, 603, 675; theory report 5460).**  I get `0.04435` (`max_m MI` of the *global* Gibbs shell
of the cone, attained at `m = ½`, where both wells tie; `t16b`).  `0.0446` coincides with the value of the *metastable* shell (in the
other well) at `m ≈ 0.5025`; I do not know how it was obtained — no output file of the author contains the number.  Immaterial for every conclusion (`0.044` against `0.111`).

**m13.  Rounding of certified exponents (line 677; theory report 5499).**  "`(1−2δ)e^{0.02509n}`" rounds the certified
`0.025087` **up**; as a lower bound it should read `e^{0.02508n}` (or the exact `θ_n`).  Likewise the table of §6.2 (A) lists
the shell `x = 0.2762` at `e = −0.07`; the value `0.0734665` belongs to `x = 0.2770` (at `0.2762` it is `0.0734649`).

**m14.  T3(a)/T8′: unstated routine steps.**  `D ≠ Q_n`; lattice approximation of block fractions and profiles; in T8′ the
inequality is first obtained for the left limit `R̄_H(e⁻)` and for `R_H(e′ + η)` (the closing sentence of the proof does
remove both).

**m15.  T9(a): "max over `γ`"** should be "sup" (`γ ↦ V(μ,B;λ_γ)` is lower semicontinuous a priori).

### Remarks that are not findings
* **A strengthening:** `R̄_H = R̂` for every real `e` in the convex case (§4) — this is what the theory report states.
* **T9(d) "`=`" can be proved** along the report's own sketch for differentiable `φ` (§4); numerically it holds beyond
  Curie–Weiss.
* **T12 can be completed without uniformity in `p`** (§7).
* **A new data point:** with a field that keeps two wells (`βB = 0.05`) the free block appears at `e = 0.02`
  (`0.016075799` against `0.0152121`), and not at `e = 0` (37 runs).
* **A slightly better profile at `e = 0.05`** (seven atoms, `0.006387549`; §6.2).

## 3. Priority A — record of the check of Theorem T3(b), Lemma T8′ and their consequences

I went through the proof with `F_REPORT.md` §3.4 (F6, Lemma T, Lemma SL, Steps 1–6), `A_REPORT.md` §2.3 (Lemma 5 and Steps
1–7 of Theorem A(ii)) and `R9_referee_report.md` §2 A next to me.  Notation of the report: instance `ψ_n = −nλ(|x|/n)`,
`Z = A(ψ_n)`, `Φ⁺(D) = Z⁻¹Σ_{x∈D}π(x)e^{nB(x)}`, `B(x) = min_{y∉D}[λ(κ_y) + u·d(x,y)/n]`.

**Step 1 (lines 286–289).**  `B(x)` is determined by the type and the distance of a minimiser: at most `(n+1)²` values; with
the type of `x`: at most `(n+1)³` pieces.  For the piece `C ⊂ T_k` with the largest `π(C)e^{nB}`:
`e^{ne} ≤ Φ⁺(D) ≤ Z⁻¹(n+1)³π(C)e^{nB}`, `π(C) = p_k|C|/|T_k| ≤ (n+1)e^{−J_k − nα_C}` (`|T_k| ≥ e^{nh(κ)}/(n+1)`), `J_k ≥ nI(κ) − c_φln(n+1)`
by (2.1), and `Z ≥ e^{−J_{t₀}+nλ(t₀/n)} ≥ (n+1)^{−c}` at a lattice type next to a touching point of `λ` (here `n·ω_h(1/n) ≤ 1 + ln n`
enters; uniform in `λ`).  Hence `e ≤ B − I(κ) − α_C + c₁ln(n+1)/n` with `c₁ = c₁(φ)`.  ✓  (∗) holds by the definition of `B(x)`.  ✓
`k ∈ {0, n}`: `T_k` is one point, `C = T_k`, `maxdens(D) = 1`.  ✓  Nothing in this step needs `h` to be Lipschitz near the ends
of `[0,1]`: `h` enters only through `(n+1)^{−1}e^{nh} ≤ C(n,t) ≤ e^{nh}` and through (2.1).
*Cosmetic:* (2.1) is stated for continuous `φ` with a constant `c_φ`; for a merely continuous `φ` the bound is
`3ln(n+1)/n + ω_φ(1/n)` (still `o(1)`, which is all that Step 1 needs) — m2.

**Step 2 (lines 290–295) — the one change.**  Lemma 5 of `A_REPORT` (= Lemma T) is stated and proved for an arbitrary nonempty
`A ⊂ Sⁿ`, an arbitrary product measure `πⁿ` with `π` of full support, and every `m ≥ 1`; its constants
(`|𝒰| ≤ (m+1)²`, the loss `(n+1)^{−2(m+1)²}`, `η_{m,n} = 2/m + 2(m+1)²ln(n+1)/n`) do not depend on `π`.  I re-derived its proof
(quantiser `⌈mp⌉/Σ⌈mp⌉ ≥ p·m/(m+2)`; most probable joint-type class; chain rule under `πⁿ(·|Ã)`; R9 had done the same).
Applied to `C ⊂ T_k`, `0 < k < n`, with `π = Bernoulli(κ)`, `κ = k/n ∈ (0,1)`:
* `Ber(κ)ⁿ(x) = e^{−nh(κ)}` for every `x ∈ T_k`, so `−n⁻¹ln Ber(κ)ⁿ(C) = h(κ) − n⁻¹ln|C| = α_C`.  ✓
* The `X`-marginal of the joint type of `((u_i(x^{i−1}), x_i))_i` is the type of `x`, i.e. **exactly** `Ber(κ)`; the joint
  type is constant on `C̃` by construction.  ✓  Hence `α = D(P_{X|U}‖Ber(κ)|P_U) = I(X;U)` (the divergence from the own
  marginal).  ✓  `Ber(κ)ⁿ(·|C̃)` is the uniform law on `C̃`.  ✓
* `α_C − 2/m ≤ α ≤ α_{C̃} ≤ α_C + 2(m+1)²ln(n+1)/n`; `I(X_I;V|U_I) = α_{C̃} − α ≤ η_{m,n}`.  ✓
* The labels depend on the prefix `x^{i−1}`, so the "blocks" differ from point to point — irrelevant: only the joint type and
  the kernel `W(x′|x,u)` are used.  The alphabet `(m+1)²` grows with `n`, but for each `n` it is finite and
  `V(μ, B−2δ; λ) ≤ R_λ(B − 2δ − α(μ))` is the definition of the supremum over **finite** block structures with real weights; no
  uniformity in the number of blocks is needed.  ✓
* `λ(κ) ≤ B`: `B(x) ≥ min_y[λ(κ_y) + u|κ_y − κ|] ≥ λ(κ)`.  ✓

**Step 3 (lines 296–297).**  `maxdens(D) ≥ |C̃|/|T_k| ≥ e^{−nα_{C̃}}`, and in the shallow case
`α_{C̃} ≤ B − I(κ) − e + o(1) < (λ − I)(κ) + 3δ − e + o(1) ≤ −e + o(1)`.  ✓  This is where `R̄_λ ≥ −e` is needed.

**Step 4 (lines 298–301).**  A minimiser `ν` of `V(μ, B−2δ; λ)` exists (compact feasible set, nonempty because
`B − 2δ ≥ λ(κ) + δ`); the cheapest coupling of `Ber(μ_u)` and `Ber(ν_u)` gives `W` with `P(X′≠X|U=u) = |ν_u − μ_u|`,
`I(X′;U) = MI(ν)`.  Given `x ∈ C̃` the `X′_i` are independent with `E d(X′ⁿ,x) = nP(X′≠X)`, `E|X′ⁿ| = nP_{X′}(1)` (constant joint
type); Hoeffding three times; `λ(κ_{X′ⁿ}) + u·d/n ≤ λ(Q) + uδ₁ + uP(X′≠X) + uδ₁ ≤ B − 2δ + 2uδ₁ = B − δ` uses that `λ` is
`u`-Lipschitz and `δ₁ = δ/(2u)`.  Membership in `D` by (∗) for the generating `x ∈ C̃ ⊂ C`.  ✓

**Step 5 (lines 302–303).**  Verbatim A_REPORT Step 5: `X′^{i−1} — X^{i−1} — X′_i` (earlier outputs are functions of `X^{i−1}`
and independent noise), `P_{X′_I} = Q`, `V — X_I — X′_I` given `U_I`, Lemma T(4).  The only measures that occur are the
uniform law on `C̃` and the product measure `Qⁿ`; `π` does not occur.  ✓

**Step 6 (lines 304–306).**  `d(a‖b) ≥ a ln(1/b) − ln 2`; `Qⁿ(y) = Q^{|y|}(1−Q)^{n−|y|} ≤ e^{−nh(κ_y)} ≤ 1/|T_{|y|}|` for **every** `Q` and
`y`, hence `Qⁿ(D) ≤ Σ_t dens_t(D) ≤ (n+1)maxdens(D)`.  ✓  No typical set and no property of `I − v` is needed — this step is
indeed simpler than in F6.

**Bookkeeping and uniformity (lines 308–310).**  `B − α − I(κ) ≥ e − [2(m+1)² + c₁]ln(n+1)/n`.  ✓  The factor `1/(1−θ_n)`
multiplies `MI(ν) ≤ ln 2`, so the error is `O(θ_n)` for **all** real `e`, including very negative ones.  ✓  For
`n ≤ 4u⁴ln²3` (`θ_n ≥ 1`) the trivial `ω_n = ½(sup I + u) + c ln(n+1)/n` works
(`Φ⁺(D) ≤ maxdens(D)·e^{n(sup λ + u)}/Z` and `R̄(e−ω) + ω ≥ 2ω − e`); the report does not say this (cosmetic, as R9 m1(iii)).
**One sentence is not correct as written (m3):** "`R_λ` is nonincreasing".  For `e < 0` the supremum defining `R_λ(e)` runs over
the profiles that are admissible at `e` (`e + α(μ) ≥ λ(μ̄)`), a set that grows with `e`, so monotonicity of `R_λ` is not
automatic.  What the proof needs is true: *`R̄_λ` is nonincreasing, and `r_μ(x) ≤ R̄_λ(e′)` whenever `μ` is admissible at
`x ≥ e′`*.  Proof: if `μ` is admissible at `e′`, `r_μ(x) ≤ r_μ(e′) ≤ R_λ(e′)`; if not, `e′ + α(μ) < λ(μ̄) ≤ I(μ̄)`, i.e.
`MI(μ) < −e′`, and `r_μ(x) ≤ MI(μ)` (the exit `ν = μ`).  With this the last line of the proof stands with `R̄_λ`.

**Verdict on T3(b): proved** (one careful paper check; cosmetic repairs m2, m3; `ω_n` of the typical-subset kind,
`≈ 2n^{−1/8}`).  The argument is the Ahlswede–Zhang/Yu converse with the reference product law chosen after the set, and
the observation that makes it work for an arbitrary rate function is correct: inside one type class `π` *is* a product
measure, and the type-uniform measure dominates every product measure up to `n+1`.  The evaluation lemma (Lemma SL) is not
used; nothing is claimed about the value of the supremum.

**The last paragraph of §4.2 (lines 313–315; the same statement for `μ_H`).**  *Asserted, with a one-line argument that I
could complete; not used in any theorem* (it is quoted in §7.1, first bullet, and tested in §7.2).  Completion: (shallow
case) `μ_H(C̃) = π(C̃)e^{V_n(k)}/Z_H ≥ e^{−n[(I−v)(κ) + α_{C̃}] − c ln n}` and `(I−v)(κ) + α_{C̃} ≤ −e + 3δ + o(1)` because
`B < v(κ) + 3δ`; (deep case) by Lemma T7 the kernel can be chosen with `Q = P_{X′}` in the contact set, Step 4 gives
`P(X′ⁿ ∈ D ∩ 𝒯) ≥ 1 − θ_n` with `𝒯 = {|κ_y − Q| ≤ δ₁}`, and on `𝒯`: `μ_H(y) ≥ e^{−n(I−v)(κ_y) − c ln n}/|T_{|y|}| ≥ Qⁿ(y)e^{−nω_{I−v}(δ₁) − c ln n}`.
The parenthesis "with `I − v` Lipschitz near the contact set, since `|I′| ≤ u` there" is neither needed nor true for a merely
continuous `φ`; uniform continuity of `I − v` on `[0,1]` suffices (m9).

**The consequence "hinted exponent `= R_λ(ε₁)`" (lines 278–280).**  Hypotheses of Theorem 11.22(e) with the hedge
`o = ln A(ψ_n) + ε/2 − ε′`, `ε′ = min(1, ε/2)`: (i) an alternative `g′ ∈ L_u` with `ln A(g′) > ln A(ψ_n) + ε − ε′` satisfies
`g′ ≥ ψ_n^D` on `D = {g′ ≠ ψ_n}`, so `Φ⁺(D) ≥ Φ(D) ≥ e^{ε−ε′} − 1`, and T3(b) (stated with `Φ⁺ ≥ Φ`; here `e > 0`, so
`R̄ = R`) gives `maxdens(D) ≥ e^{−n[R_λ(ε₁⁻)+o(1)]}`; the type-uniform half of the sampler charges `D` with at least
`maxdens(D)/(2(n+1))`.  (ii) An alternative with `ln A(g′) < ln A(ψ_n) − ε′` differs from `ψ_n` on `μ_n`-measure `≥ 1 − e^{−ε′}`
(`E_{μ_n}e^{−(g′−ψ_n)} < e^{−ε′}`); the `μ_n` half charges it.  ✓  So the cost is `e^{nR_λ(ε₁⁻)+o(n)}` against the lower bound
`e^{nR_λ(ε₁⁺)−o(n)}`: equality at continuity points, as stated; for `H` every `ε₁ > 0` is a continuity point by Lemma T8′.

**Lemma T8′ (lines 348–364): proved, given T3.**  Checked: `maxdens(D′) ≤ N·maxdens(D)` deterministically;
`P(x ∈ ≥ k copies) ≤ C(N,k)q^k ≤ 1/k!` and the union bound `2ⁿ/(n+1)! < 1` for `n ≥ 2`; for `x ∈ σ_iD`,
`s_H(x→D′ᶜ) ≥ s_H(x→(σ_iD)ᶜ)` because `D′ᶜ ⊂ (σ_iD)ᶜ`; `max ≥ n⁻¹Σ` over the at most `n` copies containing `x`;
`Φ_H⁺(σD) = Φ_H⁺(D)`; T3(b) for the arbitrary set `D′`; `Nq ≤ 1` may be assumed because otherwise the right side of the claim
is negative and `R̄_H ≥ 0`; `D′ = Q_n` only if `Nq = 1`, where the claim is trivial.  Two things should be said in the proof:
(1) T3(a) yields sets with `Φ_H⁺ ≥ e^{ne′}` and `maxdens ≤ e^{−n r_μ(e′+η) + o(n)}` for every `η > 0` (strict admissibility, lattice
approximation of `μ`), so what the argument gives first is `R̄_H(e⁻) ≥ R_H(e″) − (e − e″)` for all `e″ < e` with a **left limit**;
the report's closing sentence ("a nonincreasing function that satisfies the inequality for left limits has no jumps") is the
correct way to remove it (apply the inequality at `e₁ ↓ e`).  (2) `Φ_H⁺` is defined with the lattice landscape `V_n`, T3 with
`nv(t/n)`; they differ by `O(log n)` uniformly (m6).  The step from "`R̄_H(e) ≥ R_H(e′) − (e−e′)`" to "1-Lipschitz" uses
`−e′ − (e − e′) = −e ≤ R̄_H(e)`.  ✓  So for every rate function `R̄_H` is nonincreasing and 1-Lipschitz, and
`θ ↦ θ + R̄_H^{−1}(θ)` is nonincreasing.

## 4. Priority B — the convex case (Theorem T9, Proposition T10)

**T9(a) (lines 379–380, proof 406–410): proved.**  `v` is convex and `u`-Lipschitz, so `v = max_{|γ|≤u}λ_γ` with
`λ_γ(κ) = −γκ − I*(−γ)` the largest affine minorant of `I` of slope `−γ` (supporting lines of `v` at interior points have
slopes in `[−u,u]`, are minorants of `I`, hence `≤ λ_γ ≤ v`).  First Sion: `(ν,τ) ↦ MI(ν) + τg(ν)` on `[0,1]^k × [0,∞)`, convex
and continuous in `ν`, linear in `τ`, the **minimising** side compact — so `min_ν sup_τ = sup_τ min_ν` without any Slater
condition, also at `B = v(μ̄)` (the supremum over `τ` need not be attained there; only the value is used).  Second Sion:
convex in `ν` (`λ_γ(ν̄)` is affine in `ν`), concave and continuous in `γ` (`I*` is finite and convex), both sets compact.  ✓
("max over `γ`" should be "sup"; `γ ↦ V(μ,B;λ_γ)` is only lower semicontinuous a priori.  Irrelevant for `R_H = sup_γ R_γ`.)

**T9(b) (line 381, proof 411–423): proved.**  I re-derived every step.
* *Reduction to the law `ρ` of the block types.*  `MI(ν) = min_Q Σλ_jKL(ν_j‖Q)`; for fixed `Q` the minimisation separates over
  blocks because `λ_γ(ν̄)` is **affine** in `ν`; `α(μ) = h(E_ρM) − E_ρh(M) + I(E_ρM)`.  The displayed identity (line 415) is
  correct.
* *Sion.*  At a fixed mean, `ρ ↦ E_ρ[G_Q + τh]` is linear and weakly continuous on the convex weakly compact set of laws on
  `[0,1]` with that mean; `Q ↦ G_Q(μ)` is convex (partial minimisation of the jointly convex `KL(ν‖Q)`) and continuous on
  `[0,1]` (finite, lower semicontinuous, convex), and `G_Q` is `τu`-Lipschitz in `μ`.  So a saddle point exists, and — a point
  the report leaves implicit — **every** maximiser of `ρ ↦ min_Q E_ρ g_Q` is the first component of a saddle point, hence a
  maximiser of `E_ρ g_{Q*}`, hence carried by the contact set of `g_{Q*}` with every supporting line of its concave envelope
  at the mean.
* *The envelope argument.*  For `Q ∈ (0,1)`, `f = KL(·‖Q) − τγ·` has `f′(0⁺) = −∞`, `f′(1⁻) = +∞`, so `0 < ν_− < ν_+ < 1`, and `G_Q`
  is `C¹` (the slopes agree at `ν_±` by definition).  `g = G_Q + τh` is `C¹` on `(0,1)`, strictly concave on the closed outer
  pieces `[0,ν_−]`, `[ν_+,1]` (`τ > 0`) and strictly convex on `[ν_−,ν_+]` (`τ < 1`).  A supporting line of the envelope cannot
  touch `g` at an interior point of the middle piece (it would be the tangent of a strictly convex `C¹` function, which lies
  strictly below `g` nearby), and touches each closed outer piece at most once (strict concavity).  So at most two contact
  points, **also at the junctions** (a contact at `ν_±` is the unique contact of its outer piece).  `Q ∈ {0,1}`: `G_Q` is
  affine, `g` strictly concave, one contact point.  `τ → 0`: nothing changes for a fixed `τ ∈ (0,1)`; the value tends to `0`.
  `τ ≥ 1`: the middle piece is concave or affine, the argument fails (for `τ = 1` a line can touch along the whole middle
  piece), and the report correctly treats `τ ≥ 1` separately: for an admissible profile the bracket is at most
  `λ_γ(μ̄) − I(μ̄) − e ≤ −e`, which is `≤ 0 = φ(0)` when `e ≥ 0`.
* *"Two block types for each `τ`" ⟹ `R_γ = R_γ^{(2)}`.*  No issue: `R_γ(e) = sup_μ sup_τ[φ_{μ,γ}(τ) − τe]` and the two suprema
  commute; for each `τ ∈ (0,1)`, `sup_μ φ_{μ,γ}(τ)` is attained by a binary profile; `τ = 0` and `τ ≥ 1` contribute at most `0`
  for `e ≥ 0`.  Then `R_H = sup_γR_γ = sup_γR_γ^{(2)} ≤ R_H^{(2)} ≤ R_H`.  ✓
* The remark (lines 424–426) "for additive instances binary centres suffice for every rate function" is correct: only the
  affinity of `λ_γ` is used.
* *Numerical test of (b)* (SLP + Nelder–Mead from random profiles with 2–6 atoms, own code): excess of the best multi-atom
  value over the binary optimum `≤ 10⁻⁹` in every case — `(βJ, βB) = (0.5, 0.3)` at `e = 0` (12 runs) and `e = 0.03` (14),
  `(1, 0.1)` (10), the antiferromagnet `(−2, 0.3)` (15), the twelve non-Curie–Weiss cases of `t17` (4–10 runs each), and
  the **zero residual with two phases** (`βJ = 1.5`, landscape `0`, non-convex `I`): binary `0.008747119`, best of 28
  multi-atom runs `0.008747119`.  T9(a): `|V(μ,B;v) − max_γV(μ,B;λ_γ)| ≤ 5·10⁻¹⁰` on random profiles (three models).
  T9(c): `n_{μ*}(e + R_H(e)) = R_H(e)` to `1.3·10⁻⁸` at eight accuracies in `[−0.04, 0.06]` for `(0.5, 0.3)`; `R_H` convex
  with slopes `−0.65 … −0.24` there.

**T9(c) (lines 382–391, proof 430–440): proved; one loosely worded step; the theorem can be strengthened.**
Against `structure GameFunction (F) (E L)` of `proofs/Frontiers/GamePair.lean` (fields `cont`, `zero0`, `zero1`, `le_lin`,
`le_E`, `E_sharp`, `E_pos`):
`cont` — `F*` is a supremum of functions that are concave with slopes bounded by `L₀ = u + sup|λ_γ| + ln 2 + sup I`, finite
(`0 ≤ F* ≤ L₀`), hence `L₀`-Lipschitz on `[0,1]`.  ✓  `zero0` — `φ(0) = min_νMI = 0`.  ✓  `zero1` — `φ(1) ≤ (λ_γ − I)(μ̄) ≤ 0` with
`ν = μ`; `= 0` for the one-block profile at a touching type of `λ_γ` (it exists: `I` is continuous on `[0,1]`).  ✓
`le_lin` — `φ(t) ≤ φ(1) + L₀(1−t)`.  ✓  `le_E`, `E_sharp` — by the definition `E := sup_{0<t≤1}F*(t)/t ≤ L₀`.  ✓
`E_pos` — the conclusion is right, the sentence "every constant `ν` is at distance `≥ η`" (line 434) is not an argument
(the minimiser of the Lagrangian is not constant).  Repair: for `μ = (κ₀+η, κ₀−η)` with equal weights and `γ = 0` (`λ_0 ≡ 0`):
`MI(ν) ≥ ½(ν₁−ν₂)²` and `dist(ν,μ) ≥ η − ½|ν₁−ν₂|`, so `φ(t) ≥ min_s[s²/2 + tu(η − s/2)] − t·O(η²) = t(uη − O(η²)) − (tu)²/8`,
whence `E ≥ uη − O(η²) > 0`.  (If the minimum of `I` is at an end point of `[0,1]` — impossible for Lipschitz `φ` — use a
one-sided pair.)  m7.
The two formulas: `R_H = R̂` on `e ≥ 0` and `R̄_H ≤ R̂` everywhere — ✓ (for `τ ≥ 1` and an admissible profile the bracket is
`≤ −e = F*(1) − e`); `n_μ(X) = sup_{τ<1}(max_γφ_{μ,γ}(τ) − τX)/(1−τ)` — ✓ (Sion for the convex programme with the convex
constraint `MI + u·dist + v`, `τ = t/(1+t)`); the supremum over `τ < 1` is attained because the quotient tends to `−∞`;
`R̂(X − θ*) = θ*`, `Ŝ(X − θ*) = X`.  ✓
*Strengthening (not in the report, needed by the theory report's wording):* **`R̄_H = R̂` for every real `e`.**  For
`e₀ > e_c` put `X = Ŝ(e₀) > 0`; then `N(X) = R̂(e₀)` by the formula just proved, and by T8(b) (in the form of m4)
`N(X) ≤ R̄_H(e)` for every `e` with `e + R̄_H(e) ≤ X`; `e = e₀` qualifies because `R̄_H ≤ R̂`.  So
`R̂(e₀) ≤ R̄_H(e₀) ≤ R̂(e₀)`.  For `e ≤ e_c`: `R̂(e) = −e ≤ R̄_H(e) ≤ R̂(e)`.

**T9(d) (lines 392–394, proof 441–443): "`≤`" proved; "`=`" is numerical in the report, as labelled.**  The text delivers
exactly that.  My numerics: equality to `≤ 5·10⁻⁹` in the two rows of §5.3 that I recomputed and in twelve cases with three convex rate
functions that are not of Curie–Weiss type (`φ = −1.5(κ−0.4)² + 0.8κ⁴`, `2|κ−0.35|^{1.5} + 0.5κ`, `−1.2(κ−½)² + 0.05 sin 6κ`;
`u = 1, 2`; `e = 0, 0.3E_unif`; run `t17`).  The sketch can be completed for differentiable `φ` (not required of the
report; recorded for the coordinator): at the saddle of T9(b) the tangency conditions are `logit M_hi = u − φ′(m̄)`,
`logit M_lo = −u − φ′(m̄)` — the stationarity conditions of the convex cone functional `MI + I + uρ` for the centre type
`m = ρ*({M_hi})` (the weight of the upper atom), for every `τ` and `γ` — and the first-order conditions of the cone Lagrangian
`MI(z) + τ(uρ(z) + λ_γ(κ_z) − Λ_m)` are `h′(ν₁) = h′(ν̄) − τ(u+γ)`, `h′(ν₀) = h′(ν̄) + τ(u−γ)`, the same as those of the two
clipping levels `ν_+`, `ν_−` of the shell problem with `Q = ν̄`; when the contacts are in the outer pieces the exit is
coordinatewise beyond the shell and the triangle inequality of "`≤`" is an equality.

**T9(e) (lines 395–404, proof 444–452): proved, given Proposition 11.65(b) and Lemma SL (both refereed by R9).**
Tangent representation: `θκ − h(κ) = KL(κ‖p_θ) − ln(1+e^{−θ})`, `logit p_θ = −θ` — ✓; `I = min_θ[KL(·‖p_θ) + c(θ)]` with equality
at a supergradient `θ ∈ ∂φ(κ)` — ✓ (continuous concave `φ` on `[0,1]`).  Inclusion of feasible sets: with `I` in both
constraints (Lemma T7, applied to `I` and to `KL(·‖p₀)`), `I(ν̄) − I(μ̄) ≤ KL(ν̄‖p₀) − KL(μ̄‖p₀)` gives
field-feasible ⟹ feasible, so `r_μ(e) ≤ r_μ^{field p₀}(e)`.  ✓  `r_μ^{field p₀}(e) ≤ R^max_{p₀}(e)`: Lemma SL with `B = e + α`,
valid for every finite `𝒰` and both signs of `e`.  ✓  If the profile is not admissible for the field problem
(`e + MI(μ) + KL(μ̄‖p₀) < v_{p₀}(μ̄)`), the chain is not defined, but then `e + MI(μ) < 0` and `r_μ(e) ≤ MI(μ) < −e ≤ R^max(e)`
(not in the report; cosmetic).  `R^max_p ≤ R^max_{½}`: Proposition 11.65(b).  ✓  Equality for symmetric convex `I`: the feasible set of
`μ* = (½; p_u, p_u)` is convex and invariant under `(ν₁,ν₀) ↦ (1−ν₀, 1−ν₁)`, `MI` is convex and invariant — a minimiser of
type `½`, where the constraint is the uniform cube's.  ✓  **Gap (m8):** the sentence "`θ_na(x) = min{KL(ρ‖½) : KL(ρ‖p_u) ≤ x}`"
(and "all exponents are those of the uniform cube") needs the comparison for the game function, i.e. for `R̂` at negative
accuracies, not only for `r_μ(e)`, `e ≥ 0`.  It holds by the same two arguments applied to the Lagrangian:
`max_γφ_{μ,γ}(t) = min_ν[MI + t(u·dist + I(ν̄) − α(μ))]` (Sion and the thinning of T7), which is `≤` the field expression,
`≤ F*_{p₀}(t) ≤ F*_{½}(t)` (Proposition 11.65(b) is a statement about `F*`), and `≥` by the reflection argument at `μ*`.
Numerically: in the equality cases (`βJ = 0.5`, `1`, `B = 0`, `u = 1`; `e = −0.04, 0, 0.03`) `r_{μ*}(e) = R_unif(e)` to `10⁻¹¹`
(S1 and S2; `t23`), and the same holds at `μ*` for the antiferromagnet `βJ = −2`; every optimised profile of §6 (two
phases, with and without a field) is below `R_unif`; 766 random profiles for seven ferromagnets and accuracies of both
signs are far below it (`t12 C` — a weak test, random profiles are far from optimal).

**Proposition T10 (lines 454–459): proved, given Theorem F10(c) (refereed).**  "Its proof uses `A = Σ_tp_tE_{T_t}w` and Theorem
T2 only" is true: the three per-class events are statements about uniform samples of a finite set; `L ≤ A ≤ U` uses the
decomposition over type classes and `w(x) ≤ t̂_{|y|}e^{u·d(x,y)}`; at a symmetric instance `Tail = A·Ξ^{md}(q)` uses that `w` is
constant on type classes and `A·μ₀(x) = π(x)w₀(x)`; the lower bound is T2.  The factor: the last unsuccessful round has
`ln(3 + 1.5Ξ^{md}(q)) > ε`, hence `ln(1 + Ξ^{md}(q)) > ε − ln 3` and every algorithm needs `(1−2δ)M/(2K)` there, against
`≤ 8(n+1)M` spent.  ✓  As in R9 (m8): "reaches the exponent `R_λ`" is an exponent statement at continuity points of `R_λ`.

## 5. Priority C — the every-`n` statements and the lemmas

**T1 (lines 129–163): proved; the display of the summary is misstated (m1).**
(a) The coupling (`X` uniform on `T_t`, flip a uniform `0`: uniform on `T_{t+1}`; `w(Y) ≤ e^uw(X)`), the choice of `τ′`, the
symmetric step, `ψ^{tr,q} = max` of two members of `L_u`, `maxdens{w > t_{|x|}} ≤ q` — ✓ (brute force: 108 random `(ψ, q)`, `n ≤ 9`,
no violation, `t10`).  (b)(i) The pairs `(ψ∘σ, ψ^{tr,q}∘σ)` meet the hypotheses of Theorem 11.45(a): members of the class,
values more than `ε` apart, a point lies in the difference set of the pair `σ` iff `σx ∈ D`, probability `dens_{|x|}(D) ≤ q`.  ✓
(ii) Constants: `S = Σ_i min(w(X_i), t_t)/t_t` is a sum of `M` independent `[0,1]`-variables with mean `≥ Mq = K`;
`P(S ≤ ½ES) ≤ e^{−ES/8} ≤ e^{−K/8} ≤ δ/(2(n+1))` for `K ≥ 8ln(2(n+1)/δ)`; union over `n+1` classes `δ/2`; Markov `δ/2`;
`ln A ∈ [ln Â − ln(2/δ), ln Â + ε^{tr} + ln 2]`, length `ε^{tr} + ln(4/δ)`, the stated output is the midpoint.  ✓
*Error in the statement:* `ε_n^{tr}(q)` is **nondecreasing** in `q` (a larger `q` lowers the thresholds `t_t` and removes more
weight), not "nonincreasing" (line 130); consequently `q*(ε)` must be `inf{q : ε_n^{tr}(q) > ε}` (the set is an up-set; with
"sup" as printed, line 136, `q* = 1` and both displayed inequalities become void or false), and the upper bound holds with every
`q < q*`, i.e. `q*⁻`, not `q*⁺` (line 138).  The bold conclusion — optimality up to `8(n+1)ln(2(n+1)/δ)/(1−2δ)` and `ln(4/δ)` —
is correct with these corrections (`ε_n^{tr}` is a right-continuous step function of `q`).  The theory report (Theorem 11.76(a))
does not reproduce the faulty display.

**T2, T2′ (lines 167–195): proved.**  `ψ_g^{σD} = ψ_g^D∘σ^{−1}`, `A(ψ∘σ) = A(ψ)`, `P_σ(x ∈ σD) = dens_{|x|}(D)`; hypotheses of Theorem
11.22(c) ✓.  Formula (2.3) and `A(ψ_g^D)/A(ψ_g) = 1 + Φ_g(D)`: 266 brute-force cases (`n ≤ 9`, five models, random symmetric
instances and random sets), worst relative error `1.4·10⁻¹⁵`, every dip in `L_u`.  The exact sums of T2′ are what my own
block-sum code computes (236 comparisons with brute force, `1.4·10⁻¹⁵`; `t10`).

**T4 (lines 199–207): proved.**  `Λ_g ≤ V_n` (a `u`-Lipschitz minorant of `J`), `Z_g ≥ 1`, `Z_H ≤ n+1`; in fact
`Z_gΦ_g⁺(D) ≤ Z_HΦ_H⁺(D)` exactly (brute force: never violated, `4·10⁻¹⁶`).  *Is the factor needed?*  A factor larger than one
is: for `g = 0` and `D = Q_n ∖ {y}`, `|y|` a minimiser of `J`, both sides are equal and `Φ_0⁺/Φ_H⁺ = Z_H/Z_0` (`2.06` at
`n = 8`, `βJ = 1.5`, `u = 1`; `2.51` at `n = 10`, `βJ = 0.5`, `βB = 0.3`, `u = 6`; `t10`).  `n+1` itself is only a bound of `Z_H/Z_g`.
The theory report's addition "the factor cannot be dropped (`Z_H/Z_g` is attained)" is correct in this sense.

**T5 (lines 211–228): proved.**  Cells: `d(x, C_μ) = ℓ¹` of the counts, constant on cells; `(n+1)^{−k}e^{−nMI} ≤ d_c ≤ (n+1)e^{−nMI}`; at
most `(n+1)^{k−1}` cells per type.  Role of the quantile: the cells with `w ≥ t_t` have total density `≥ q`, so one has
`d_{c*} ≥ q/(n+1)^{k−1}`, is "seen", and `q·t_t ≤ (n+1)^{k−1}d_{c*}w(c*)`; an unseen cell has `d_c ≤ q(n+1)^{−k}`.  (The bound
`2(n+1)^{2(k−1)}` is generous; `2(n+1)^{k−1}` suffices.)  No unimodality is used.  ✓  The passage to the exponent
`θ_shell(ε₁⁺; μ)` is right.

**T6 (lines 236–246): proved.**  KKT for maximising the strictly concave `Σλ_jh(ν_j)` over a polytope (affine constraints:
necessary and sufficient); raised blocks at `c_lo = (h′)^{−1}(η+τ)`, lowered at `c_hi = (h′)^{−1}(η−τ)`, unchanged ones in
between.  Monotonicity along the thresholds needs `λ′ ≥ −u` and `c_lo ≤ type ≤ c_hi` — both stated.  *Is the Lipschitz
hypothesis respected where the lemma is used?*  Yes: the two-parameter reduction holds for every landscape (also `I`), the
boundary-curve search only for `u`-Lipschitz ones; all landscapes of §6.4 are minima of `u`-Lipschitz functions; where `I`
itself is in the constraint (T7, T9(e), the random search `t17` of the author) only the *value* is used.  My solver S2 (dual
per exit type, `I` in the constraint, no boundary curve) agrees with the clipping solver on every optimum re-evaluated
(§9), which is a numerical confirmation of T6 together with T7.

**T7 (lines 248–258): proved.**  Thinning (`X″ = X′·B`, resp. `X′ ∨ B`): `ν̄″ = κ*`, `dist(ν″,ν) = |κ′ − κ*|`, data processing;
`v(κ*) = I(κ*)` follows from `v(κ*) ≥ v(κ′) − u|κ′−κ*| = I(κ*)`.  The versions for `n_μ` and `𝒱` are the same computation.  ✓

**T3(a) (lines 264–271, proof 281–284): proved.**  `C ⊂ D`, slack `> ln 2` on `C`, the `ℓ¹` distance of counts bounds the
Hamming distance from below, `(n+1)^{k−1}` classes per type of density `≤ (n+1)e^{−nMI}`.  Exact sums at `n = 60, 120, 240`,
two and three blocks, 48 cases: both inequalities hold; in every case `θ_D > V(μ,B;v)` already without the factor `(n+1)^k`
(`t11 A`).  Unstated: `D ≠ Q_n` is needed for the dip (true as soon as `(n+1)^ke^{−nV} < 1`); the passage to `R_λ(ε₁⁺)` needs
lattice approximations of the block fractions and of `μ` (routine).

**T8 (lines 319–346).**  (a) proved: both triangle inequalities ✓, `μ*` self-consistent ✓, T7 for `I` against `v` ✓.
(b) proved after a repair (m4): for `e < 0` the step "`n_μ(X) ≤ r_μ(e)`" needs `μ` admissible at `e`; otherwise
`n_μ(X) ≤ MI(μ) < −e`.  So the statement is `N(X) ≤ min{R̄_H(e) : e + R̄_H(e) ≤ X}`.  (c) proved, given T3(b): `A(ψ^{tr}) ≥ qT`,
`t_t ≤ Te^{V_n(t)}`, `A(ψ) − A(ψ^{tr}) ≤ T·Z_H·Φ_H⁺(D)` — ✓, no convexity.  **The form of T3(b) that (c) needs:** the `maxdens` form
(not the `μ_H` form), with `Φ⁺` (not `Φ`), for **all real `e`** — negative `e` is essential, since `R̄_H^{−1}(θ) < 0` for
`θ > R_H(0)` — and with `R̄`, not `R`.  T3(b) is stated in exactly this form.  Cosmetic (m5): at a jump of the nonincreasing
function `R̄_H^{−1}` the bound is `θ + R̄_H^{−1}(θ⁻) + o(1)`; the infimum in the conclusion is unaffected.

## 6. Priority D — two phases: own numerics, attempts at refutation

All numbers in this section are mine (scripts in `code/`, outputs in `out/`; §9).  Solvers: **S1** — two-parameter search
over clippings on the boundary curve, landscape = table of `v` (used in every search; returns a feasible exit, hence an upper
bound of the inner minimum); **S2** — for every exit type on a grid (then refined) the Lagrangian dual of "minimise `MI` at
fixed type and distance budget `(B − I(κ′))/u`", with `I` itself: by weak duality each value is a *lower* bound of the
minimum at that type; no table of `v`, no clipping lemma, no boundary curve; **S3** — multi-start SLSQP over all exit
profiles in split variables, `I` in the constraint (an upper bound).  Every optimum quoted was re-evaluated with S1 (fine
settings), S2 and S3; they agree to `≤ 2·10⁻⁹` unless stated.  Searches over profiles: (i) differential evolution over
`k`-block profiles without symmetry (`k = 3, 4, 5`), (ii) Nelder–Mead, (iii) a **sequential linear programme over the law
`ρ` of the block types** (my own device, `r10slp.py`): for a ferromagnet, each exit value `g(ρ;κ′)` is a maximum of
functionals that are linear in `ρ` (convex in `ρ`), so its linearisation at a reference law with the exact multipliers is a
global minorant; maximising the minimum of these minorants over all laws on a grid of 401–801 atoms is an LP whose optimum
is `≥` the current value.  It moves finite mass in one step (it finds the free block from the binary optimum in one step at
`e = 0.02`) and is alternated with Nelder–Mead for continuous moves.

### 6.1 Conjecture C1 (`e = 0`, `βJ = 1.5`, `B = 0`, `u = 1`): not refuted

| search | starts | best value found | where |
|---|---|---|---|
| binary centres, unrestricted Nelder–Mead | 4 | `0.025101175` | `(½; 0.29803, 0.29803)`; exits of type `0.4076`, `0.5924` tie |
| differential evolution, 3 blocks (two seeds, 20 768 evaluations each) | Sobol | `0.02510113`, `0.02510116` | the binary shell, one atom split |
| differential evolution, 4 blocks (two seeds, 25 928 evaluations each) | Sobol | `0.02510057`, `0.02510086` | the same |
| differential evolution, 5 blocks (25 928 evaluations) | Sobol | `0.02509951` | the same |
| SLP ascent + Nelder–Mead, random profiles with 2–6 atoms | 40 | `0.025101176` | binary shell (31 runs at `≥ 0.0251011`, 5 more between `0.02509` and `0.02510`, not fully polished), one run at a 4-atom point `0.02494`, 3 starts of value `0` that did not move |
| alternating SLP / Nelder–Mead, structured starts (binary, `S3`…`S6`, asymmetric, frozen coordinates) + random | 7 + 30 | `0.025101176` | binary shell (32 runs); the diluted local maximum `0.0249932` (`λ_f = 0.1397`, `x = 0.2709`; 3 runs); 2 starts of value `0` |
| the same with a field `βB = 0.05` | 7 + 30 | `0.025023242` | the binary shell `(0.4761; 0.3260, 0.2707)` of the report (34 runs); a diluted local maximum `0.024909` (2 runs) |
| the same at `e = 0.0015 < e₀` | 7 + 30 | `0.024296348` | binary shell `x = 0.29856` (32 runs); the `S3` branch `0.0242784` (4 runs) |

**No profile with `r_μ(0) > 0.0251012` was found.**  In addition the binary optimum is a *critical point of the linearised
problem over all laws*: with exact multipliers and the active exit types in the grid to `10⁻⁷`, the LP optimum over laws on
401 grid atoms is `0.02510118` against the current value `0.02510117`.  This excludes every improving direction to first
order in the space of all profile laws; it is not a proof (the exit values are convex in `ρ`, so second-order gains exist
in principle — this is how the diluted branch wins beyond `e₀`).  C1 stands as a conjecture; my evidence is independent of
the author's and of the coordinator's and of the same kind.  S1/S2/S3 at the optimum: `0.025101174` each.

### 6.2 Positive accuracies: one small improvement at `e = 0.05`, none at `e = 0.02`

| `e` | binary shell | report's best | my best | profile (atoms @ weights), re-evaluated S1 / S2 / S3 |
|---|---|---|---|---|
| `0.02` | `0.015276498` (`x = 0.30552`) | `0.0161548` | `0.016154792` | `0.27743@0.42964, 0.50010@0.14083, 0.72264@0.42953` (the report's free-block profile); all 18 runs that left the value `0` end here to `5·10⁻⁷` (7 structured + 14 random starts, 3 of the random ones had the value `0` and did not move); `0.016154792` / `…792` / `…792`; three exits tie (`0.377`, `0.500`, `0.623`) |
| `0.05` | `0.004626467` (`x = 0.31796`) | `0.0063867` (5 atoms) | **`0.006387549`** (7 atoms) | atoms `0.269505, 0.386240, 0.455329, ½, 0.544671, 0.613760, 0.730495`, weights `0.373398, 0.078576, 0.007536, 0.080980, 0.007536, 0.078576, 0.373398`; `0.006387549` / `…549` / `…549`; my 5-atom optimum: `0.006386746`; found by the alternating search from the starts `S3`, `S4`, `S5` (`0.0063875`, 19–23 grid atoms), then re-optimised in the symmetric 7-atom family (`t21`) |
| `0.02`, `βB = 0.05` | `0.0152121` | not searched | **`0.016075799`** | `0.25136@0.45677, 0.47482@0.13875, 0.69534@0.40448`; `…799` / `…799` / `…799`; exits `0.3435`, `0.4563`, `0.5891` tie |

So `R_H(0.05) ≥ 0.0063875` (proved lower bound by T3(a); `+8·10⁻⁷` over the report — within the `10⁻⁵` the author allows
for), and with a field that keeps two wells the free block appears as well (`+5.7 %` over the binary centre at `e = 0.02`,
the same as at `B = 0`).  The number of atoms grows with the accuracy (a seventh atom pays at `e = 0.05`), which supports
the report's doubt (O2) that the supremum is attained by finitely many block types.  All values respect the proved bound
`R_H ≤ R_unif` (`0.0201820`, `0.0098646`).

### 6.3 The crossing `e₀`

Binary branch and `S3` branch (my own maximisations; each value re-evaluated with S2):
`e = 0.0015`: `0.024296347` / `0.024278406`; `0.0018`: `0.024136660` / `0.024136412`; `0.002`: `0.024030440` / `0.024041930`.
Root of the difference: **`e₀ = 0.001804`**.  The report's `0.00181` is the linear interpolation between `e = 0.001` and
`0.002` (its file `out/t15_e0_bJ1.5_u1.txt`), which gives `0.001806`; the value is `0.0018` to two digits (m10).  Below `e₀`
(at `0.0015`) no multi-block profile beats the binary shell in 37 runs.

### 6.4 The junction with the uniform cube (§6.6): (ii) confirmed, (iii) **false as a general statement**

*(ii)*  Re-derived: along `(a′,b′) = (ρ̄ − t, ρ̄ + t)` the exit type is `½ + t`, `I(½+t) − I(½) = 2(1−βJ)t² + O(t⁴)`,
`ρ̄ = ρ − 2(1−βJ)t²/u`, `MI = MI₀ + t²[c₂ + 2(1−βJ)L/u] + O(t⁴)`; finite differences on the boundary curve agree with the
coefficient to `10⁻⁶` in five cases (`u = 0.5, 1, 2`).  The diluted version (§6.7 (i), `A(λ_f)`) is also correct (re-derived).
`βJ*(0,1) = 1.12498`, `βJ*(0.02,1) = 1.1029`, `βJ*(0.04,1) = 1.0815`, `βJ*(e_c,1) = 1.2716`.  ✓
*(iii)*  For `u ∈ {1, 2}` and seven accuracies between `0.9e_c` and `0.9E` (run `t07c`; also `u = 0.3` and `u = 4`, `e ≥ 0`, in run
`t07`) the value of `μ* = (½; p_u, p_u)` equals `R_unif(e)` to `10⁻⁹` relative at every coupling `1 + f(βJ* − 1)`, `f ≤ 0.99`, and
falls below it for `f = 1.02` and `1.2` — the report's claim, in a wider range than it computed.  **But the claim fails for
larger `u`** (run `t07c`, re-evaluated with S2): when the barrier
`b(βJ) = I(½)` reaches `≈ E_unif(u) − e`, the *constant* exit at a well (`MI = 0`) becomes feasible for `μ*`
(`u·dist(κ_w·𝟙, μ*) + I(κ_w) ≤ e + KL(p_u‖½) + b`), and this happens below `βJ*`:

| `u` | `e` | `βJ*(e,u)` | coupling `< βJ*` | `R_unif(e)` | `r_{μ*}(e)` | best binary profile found | top of the barrier a contact point? |
|---|---|---|---|---|---|---|---|
| `4` | `0.6e_c = −0.36183` | `4.9978` | `4.9578` | `0.4185706` | `0` (exit: constant profile at the well, `u·dist + I = 2.00005 ≤ e + α = 2.02703`) | `0.41763` at `(½; 0.0258, 0.0258)` | yes (`[0.44, 0.56]`) |
| `8` | `0` | `8.3366` | `8.2632` | `0.3985436` | `0` (`4.00000 ≤ 4.12859`) | `0.36742` at `(½; 0.0292, 0.0292)` | yes (`[0.4175, 0.5825]`) |
| `3` | `0.9e_c = −0.45205` | `4.5409` | `4.3639` | `0.4548604` | `0` (`1.50016 ≤ 1.53918`) | — | yes (`[0.4974, 0.5026]`) |
| `6` | `0.3e_c = −0.20275` | `6.8066` | `6.5163` | `0.4111654` | `0` (`3.00000 ≤ 3.03808`) | — | yes (`[0.4141, 0.5859]`) |

(further failing cells of the grid: `u = 4`, `0.9e_c`; `u = 6`, `0.6e_c`, `0.9e_c`; `u = 8`, `0.3e_c`, `0.6e_c`, `0.9e_c`.)
In every cell of the grid the failure occurs exactly when `b(βJ*) > E_unif − e`, and nowhere else; for `e ≥ 0.3E`
there is none up to `u = 8`.  So the junction is at `min{βJ*(e,u), βJ_w(e,u)}`, `βJ_w` the coupling at which the barrier is as
high as the uniform cube's remaining threshold `E_unif(u) − e` — exactly: `b ≥ E_unif(u) − e + u·(p_u − κ_w)⁺` makes the
exit at the well feasible (`u/2 − KL(p_u‖½) = ln cosh(u/2) + u·p_u`; margins `0.0272`, `0.1286`, `0.0397`, `0.0381` in the
four rows; the correction decides no cell of the grid); for `u = 1` the threshold is far
away (`b(βJ*) = 0.010` against at least `0.120`), which is why the report did not see it.

*Does another profile reach `R_unif(e)` there?*  By the chain of T9(e) such a profile would have to be of type `½` and optimal
for the uniform cube, and the one that is, `μ*`, has the value `0`.  Numerically (run `t24`, the first two rows of the table):
the best symmetric binary shell sits at the edge of a cliff — the value of `(½; x, x)` is positive only while every
constant exit (`MI = 0`) is infeasible, i.e. for `x` above a threshold (`0.02916` at `u = 8`, `0.02581` at `u = 4`; the cheapest
constant exit has the type at the edge of the well's contact interval, `1.99·10⁻⁴` and `2.8·10⁻³`), and is largest there.
Evaluated at a profile where the constant exits are infeasible by a margin `2·10⁻⁵`, the three inner solvers agree to
`10⁻¹⁰`:

| `u`, `e`, `βJ` | best binary shell | S1 = S2 = S3 | `R_unif(e)` | deficit | multi-block search |
|---|---|---|---|---|---|
| `8`, `0`, `8.26321` | `(½; 0.029164, 0.029164)` | `0.367416140` | `0.398543639` | `0.0311` | 16 starts, none above the binary shell; 3 return to it, the others end between `0.3295` and `0.3668` |
| `4`, `0.6e_c`, `4.95782` | `(½; 0.025812, 0.025812)` | `0.417628794` | `0.418570639` | `9.4·10⁻⁴` | 23 starts, none above; 18 return to the binary shell, 3 to the binary shell with one atom split (within `10⁻⁵` below), one keeps frozen coordinates (`0.41580`), one never leaves the value `0` |

The multi-block starts were adapted to the cell: asymmetric binary profiles, shells diluted by a free block
(`3 %, 8 %, 15 %`), symmetric four-atom profiles, shells with frozen coordinates, an off-centre type, and random splittings
and perturbations of all of these, each improved by alternating SLP and Nelder–Mead (the search itself runs at the
accuracy `e + 2·10⁻⁵`, which can only lose).  Almost every run ends on the cliff (`MI(μ) = 0.56132`, resp. `0.57328`, for
profiles of type `½`) at a value at most that of the binary shell.  So, on this evidence — searches, not a
proof — **`R_H(e) < R_unif(e)` at these couplings below `βJ*`**: the junction really is earlier, and not only the
argument for it fails.  (At the very edge of the cliff the solvers can fall on different sides — first run of `t24`, at the shell
`x = 0.029159`, to which a maximisation of the S1 value converges: S1 = `0.3674225`, S2 = `0.3674239`, S3 = `0`.  S3 works
with `I` itself and finds a feasible constant exit of type `≈ 2·10⁻⁴`; S1 works with a table of `v` and places the edge a
hair earlier; S2 scans exit types on a grid of spacing `8·10⁻⁴` and cannot see so narrow a window.  This is why the numbers are quoted at a margin; the supremum itself is not
attained.  The "best binary profile" values of run `t07c` quoted in the table above are S1 values at such an edge and
agree with the present ones to the digits given.)  → finding **M1**.

### 6.5 The marginal shells at `u = 0.30` (§6.5 (4)): reproduced; the bracket's upper end is not proved

Contact set `[0.0465, 0.1237] ∪ [0.4745, 0.5255] ∪ [0.8763, 0.9535]`; `u_top = 0.28153` (chord to `κ = 0.1183`; at `u = 0.2815`
the top is not a contact point, at `0.2816` it is).  `R^{(2)}(e)`, optimal shell: `0.00226456` (`x = 0.44091`) at `e = 0`;
`0.00220789` (`0.44133`), `0.00209550` (`0.44219`), `0.00192939` (`0.44350`), `0.00171284` (`0.44529`) at
`e = 10⁻⁴, 3·10⁻⁴, 6·10⁻⁴, 10⁻³`; slopes between `−0.63` and `−0.51` on `[−0.002, 0.002]` (no conflict with Lemma T8′).
For the optimal shell `r_μ(e) = 0` already at `e = 2·10⁻⁴`, so `n_{μ*}(S(0)) = 0`.  `sup` over symmetric shells of
`n_μ(S(0))`: **`0.00184002` at `x = 0.45138`** by three routes (two-parameter search over clippings; through `r_μ` and
T8(b); a full `1201²` grid of exit profiles with `I` in the constraint, refined four times); three Nelder–Mead runs over
general binary profiles: `0.00184004`.  So the pair identity does fail for cones around binary classes, as reported.
**What the report overstates (M2):** "the non-adaptive exponent at the accuracy `e + R(e)` is only known to lie in
`[0.00184, 0.00226]`".  The upper end is `R^{(2)}(0)`; T8(c) bounds `θ_na` by `inf{θ : θ + R̄_H^{−1}(θ) < X}` with the **true**
`R_H`, of which `R^{(2)}` is a lower bound.  Proved: `0.00184 ≤ θ_na(S(0)) ≤ R_unif(S_unif^{−1}(0.0022646)) = 0.00338`
(from `R̄_H ≤ R̂_unif`).  The interval `[0.00184, 0.00226]` holds *if* `R_H = R^{(2)}` on a left neighbourhood of `0` at `u = 0.30`
— the analogue of C1, supported there by one 3-block search of the author and by my run `t22`: alternating SLP /
Nelder–Mead from 12 structured starts (shells with free blocks of weight `0.05, 0.14, 0.3`) and 12 random multi-atom starts
returns the binary marginal shell `0.002264557` (S1 fine and S3; S2 `0.00226452…56`, the shell is an edge of its family) and
nothing larger.

### 6.6 Spot checks of the tables (own code; every number below is mine, the report's in brackets where it differs)

* **§5.3** (`u = 1`).  `(βJ, βB) = (0.5, 0.3)`: `R_H(0) = 0.023983` at `(m; a, b) = (0.4371; 0.1310, 0.4731)`; `max_γR_γ(0) = 0.023983` at
  `γ* = +0.2147`; cone formula `0.023983`; `R_0(0) = 0.022659`; `E_H = 0.099123`; `E_0 = 0.095345`; `a = 0.091019`.
  `(1.0, 0.1)`: `0.027964`; `γ* = +0.2000`; cone formula `0.027964`; `R_0 = 0.020271`; `E_H = 0.115250`; `E_0 = 0.090246`; `a = 0.106465`.
  All equal to the report's entries.  (`E` computed as `sup_μ{min_c[u·dist(c𝟙, μ) + λ(c)] − α(μ)}`, the accuracy beyond which a
  constant exit is feasible for every profile; `a` as `max_m MI(`Gibbs shell of the cone`)`.)
* **§6.2 (A)**.  `R^{(2)}(e)`: `0.100254660` (`e = −0.10`), `0.073466544` (`−0.07`), `0.057596058` (`−0.05`), `0.043328309` (`−0.03`),
  `0.030733644` (`−0.01`), `0.025101175` (`0`), `0.019939890` (`0.01`), `0.015276498` (`0.02`),
  `0.011143072` (`0.03`), `0.007577879` (`0.04`), `0.004626467` (`0.05`), `0.001630776` (`0.064`), shells `x` as in the report
  (except `e = −0.07`, m13); unrestricted binary
  profiles return the symmetric shell at `e = −0.05, 0, 0.03`.  Free-block family: `0.024041930` (`0.002`), `0.020381673`
  (`0.01`), `0.016154794` (`0.02`), `0.012357737` (`0.03` [`0.01235769`]), `0.009020058` (`0.04`), `0.006166950` (`0.05`).
  `n_{μ*}(e + R^{(2)}) = R^{(2)}` to `10⁻⁸` at `e = −0.05, 0, 0.02` by two routes, and the directly computed truncated shell-cone
  gives the same; the truncated cone around the centre: `0.01451496`, `0.00203789`, `0.00017719` (as reported); free-block
  optimum at `e = 0.02`: `n_μ(e + R) − R = 5·10⁻¹⁰`.  Cone formula `R_cone(0) = 0.0107007`; zero residual `0.0087471`.
  **`a_cone`: `0.04435`, not `0.0446`** (m12): the Gibbs shell of the cone around a centre of type `m` is in the well on the
  side of the centre; `MI` of the global shell is `0.044351` at `m = ½` (both wells tie), `0.043419` at `m = 0.49, 0.51`,
  `0.040215` at `0.45, 0.55`; the larger values `0.0454…0.0512` belong to the metastable shell in the other well.  No output
  file of the author contains `0.0446`; his exact sums (`0.0435` at `n = 4000`) do not discriminate.
* **§6.3** (exact sums, own block-sum code validated against brute force).  Dips of `H`, `ε = 1`, capped sets around a centre
  of type `n/2`: `θ_n = 0.025153` (`n = 250`), `0.025092` (`n = 1000`); truncated shell-cone `x = 0.298` at `ε = 0.0251012n`:
  `0.031466` (`n = 250`), `0.027977` (`n = 1000`).  All four equal to the report's entries to six digits.
* **§6.5** (`e = 0`).  `u = 0.60`: `0.00907142` [`0.00907144`], cone formula `0.00321748`; `u = 0.30`: `0.00226456`
  (`x = 0.44091`), cone formula `0.00075446`; `u = 0.25`: `0.00052346` at `(0.537; 0.9085, 0.0576)` in a well, cone formula
  `0.00052067`, no barrier shell with a positive value; contact sets as reported.
* **§6.6** (`e = 0`, `u = 1`).  `βJ = 1.12, 1.14, 1.2, 1.3, 1.75`: `0.0291391, 0.0290694, 0.0283097, 0.0271307, 0.0230260`, cone
  formula `0.0291391, 0.0290694, 0.0273828, 0.0202239, 0.0054940` — all as reported; the shell `(½; p_u, p_u)` is globally
  self-consistent at `βJ = 1.2, 1.5, 1.75, 2.0` (grid `2000²`), not self-consistent for `x = 0.24, 0.26 < p_u`, and
  `θ_shell(X; x = p_u) → KL(p_u‖½)` (`0.0490, 0.0898, 0.1044, 0.1073` at `X = 10⁻², 10⁻³, 10⁻⁴, 3·10⁻⁵`), so `a = a_unif`.
* **§6.7**.  `e = 0.02`: `βJ = 1.2`: binary `0.01895028`, cone formula `0.01769125`, free block `0.01921078` (`λ_f = 0.0339`);
  `βJ = 1.3`: `0.01759988`, `0.01088239`, `0.01812017` (`λ_f = 0.0727`).  Field at coexistence (`βB = 0.05`): `0.0250232`,
  `0.0198677`, `0.0152121` at `e = 0, 0.01, 0.02` with the report's shells; cone formula `0.0115296`; zero residual `0.0075630`,
  `0.0036644`, `0.0012178`.  `βJ = 2`: contact set as reported; `0.0213210` (`e = 0`); `0.0158308 → 0.0163911` (`e = 0.01`,
  `λ_f = 0.2712`); `0.0068041 → 0.0084996` (`e = 0.03`).  All as reported.

### 6.7 Theorem T3(b) on sets (priority A, item 4)

* **Small cubes are uninformative — confirmed, for a sharper reason than the report gives.**  All proper nonempty subsets
  of `Q_3` (254) and `Q_4` (65 534), instance `H`, `βJ = 1.5`, `u = 1`: `Φ_H⁺(D) > 1` for 191 and 49 151 of them (so the report's
  "`Φ_H⁺(D) < 1` for most sets", line 955, is not right), but **every one of these has `maxdens(D) = 1`**, and every set with
  `maxdens < 1` has `Φ_H⁺ ≤ 1` and `θ_D + e_D ≤ −0.198` (`n = 3`), `≤ −0.026` (`n = 4`): the inequality holds with `ω = 0` and tests
  nothing about exponents (m11).
* **Multi-centre and centreless families, exact sums, `n = 200` on a 4-block grid (`51⁴` cells), instance `H`.**  Sets:
  neighbourhoods of the barrier shell around one centre (control); unions of two and of three such neighbourhoods around
  centres at mutual distance `n/2`; intersections; symmetric differences; sums of two distances; unequal budgets;
  neighbourhoods of random 4-block classes and unions of two; cylinders over a free block; half-spaces in the counts.
  Reference curves: `R_ref` (binary shells and the free-block family, a lower bound of `R_H`) and the proved upper bound
  `R_unif`.  `u = 1`: 210 sets, largest `ω(D) = 0.00136 = 0.05·ln n/n` with respect to `R_ref` (a neighbourhood of a random
  4-block class at `e_D = 0.062`), `0` with respect to `R_unif`; all unions, intersections and cylinders: `ω = 0`.
  `u = 4` (exponents ten times larger, so the test has some power; there `R_ref(0) = R_unif(0) = 0.23925`): 192 sets,
  largest `ω = 0.0048 = 0.18·ln n/n` (a union with unequal budgets at `e_D = 0.69`).  No violation; unions of
  neighbourhoods around several centres gain nothing at the exponential scale.  As R9 said of F6: these tests cover sets
  that are invariant under a Young subgroup; sets without symmetry (unions of exponentially many copies, as in Lemma T8′)
  cannot be summed exactly.
* T3(a) at `n = 60, 120, 240` (2 and 3 blocks, 48 cases): both inequalities hold; `θ_D > V(μ,B;v)` in every case.

## 7. Priority E — the sketch T12, the nested algorithm, prior art

**Proposition T12 (lines 1015–1037) — the representation is correct; the statement is provable along these lines, and
the "missing step" can be avoided.**
* Hubbard–Stratonovich: `e^{(βJ/2n)M²} = √(n/2πβJ)∫e^{−ny²/(2βJ)+yM}dy` ✓; with `−f = (βJ/2n)M² + βBM`, `M = 2|x| − n`:
  `π = ∫ν(dy)Ber(p_y)^{⊗n}`, `p_y = e^{y+βB}/(2cosh(y+βB))`, `ν(dy) ∝ exp(−n[y²/(2βJ) − ln 2cosh(y+βB)])dy` — positive,
  normalisable (Gaussian tails).  Checked numerically to `6·10⁻¹⁵` (`n = 10, 40`; `t14`).  `|∂_yln A_y| = |E(M) − n tanh| ≤ 2n` ✓;
  `A_y/A_{y′} ≤ e^{un}` ✓; `ν(|y| > Y) ≤ e^{−n(u+1)}` for a fixed `Y`, so `|y| ≤ Y` suffices; a grid of mesh `n⁻²` (`O(n²)` points)
  gives the factor `1 + O(1/n)`.  ✓  The combination of brackets with the weights `ν` is valid, and
  `max_yR^max_{p_y} = R^max_{½}` (attained at `y = −βB`) by Proposition 11.65(b).
* *Is the uniformity in `p` the only missing step?*  As written, yes: the grid of fields changes with `n`, and Theorem
  11.64 is an asymptotic statement for one `p` (its `ω_n` and the number of levels depend on `p`); also needed, and available,
  are failure probabilities `δ/poly(n)` and the accuracy `ε − 1`.
* *It can be avoided.*  For `y` in a cell `|y − y_j| ≤ Δ` of a **finite** net (independent of `n`):
  `A_y(ψ) = C_n(y,y_j)·A_{y_j}(ψ − 2(y−y_j)|x|)`, and `ψ − 2(y−y_j)|x| ∈ L_{u+2Δ}` (checked on `Q_10`: identity to
  machine precision, Lipschitz constant `u + 2|y−y_j|`; `t14`).  So the algorithm of Theorem 11.64 for the field `p_{y_j}`
  and the class `L_{u+2Δ}` serves all grid fields of the cell — an evaluation of the tilted residual is an evaluation of
  `ψ`.  Only finitely many pairs `(p_{y_j}, u+2Δ)` occur, the `o(n)` is uniform over them trivially, and
  `R^max_{p,u+2Δ} ≤ R^max_{½,u+2Δ} → R^max_{½,u}` as `Δ → 0` (the closed form is continuous in `u`).  With this change I
  consider T12 **provable** (given Theorem 11.64); it remains a sketch in the report.
* "Not tight in general" and "nothing for antiferromagnets" are correct remarks.

**§8.1 (lines 986–1011) — the analysis of the failure is correct.**  `N(a′)/N(a)` is the inner-Gibbs average of
`e^{−[ψ(a′,b)−ψ(a,b)]}e^{−n[φ(κ+1/n)−φ(κ)]}`, `D(a′)/D(a)` the `π(·|a)`-average of the second factor; for `ψ(a,b) = g(|b|)` the
outer function `−ln W` changes by `≈ φ′(κ_ψ) − φ′(κ_π)` per outer flip, which is not bounded by `u` and depends on `ψ`.  So
`−ln W` is Lipschitz with `u + osc φ′` only, and (F2) of Theorem 11.52/F7 fails.  The effective inner model (coupling
`βJn_i/n`, field `βB + βJ(2|a| − n_o)/n`) is right.  (F2′): at fixed total type the inner slice changes with `|a|`, a coupling
costs one inner flip, hence `2u` across outer types.  ✓

**The coordinator's proposed repair (theory report §11.23, "a possible repair") — no immediate obstruction.**  For an
exchangeable `π`, `π(a,b) = p_{|a|+|b|}/C(n,|a|+|b|)`, so given `|b| = t_i` the inner block is uniform on its slice and
independent of `a`; `W_{t_i}(a) = mean_{b∈T_{t_i}}e^{−ψ(a,b)}` has `−ln W_{t_i} ∈ L_u(Q_o)` exactly (an average over a set that does
not depend on `a`), and `ω_{t_i}(a) = C(n_i,t_i)p_{|a|+t_i}/C(n,|a|+t_i)` is an exchangeable weight on `Q_o`.  So each of the
`n_i+1` outer problems is again of the class "exchangeable reference, `u`-Lipschitz residual", for which T1–T4 and T3(b)
hold.  What has to be supplied — none of it an obstruction that I can see, all of it real work: (1) the inner problems
live on **slices** (uniform reference on one type class, no one-flip coupling inside), so the family of problems must be
enlarged to products of slices, and the recursion is no longer scale-free: the pair `(θ_na, R_H)` becomes a family indexed
by the conditional rate functions (for Curie–Weiss: effective coupling and field, a two-parameter family) and the
machine-checked convergence theorem does not apply as it stands; (2) the accuracy must be allocated over the `n_i+1` inner
types; a tool is that `t_i ↦ W_{t_i}(a)` is itself log-`u`-Lipschitz (couple adjacent inner slices by one flip), but the
weights `ω_{t_i}` change with `t_i`; (3) the cost of an outer point is a maximum over inner types and outer instances
that need not be realisable by one residual, so the limit of the recursion may exceed `R_H` (the same looseness as in T12).
Whether it equals `R_H` is the open problem, as the theory report says.

**§9 (prior art).**  Generic queries and abstract pages only (25 Nov 2026).  Consistent with the abstracts:
Trebst–Huse–Troyer, arXiv:cond-mat/0401195 ("optimizes the statistical-mechanical ensemble … to maximize the system's rate
of round trips"; "substantially outperforms flat-histogram methods" — that the optimal ensemble puts weight at bottlenecks
via the local diffusivity is in the paper, not in the abstract); Cérou–Héas–Rousset, arXiv:2212.04292 (worst-case optimal
proposal = entropy minimiser in a convex class, cost = relative entropy; verbatim); He–Owen, arXiv:1411.3954 ("the minimax
regret arises by taking a uniform mixture of proposals"); Dayal et al., arXiv:cond-mat/0306108 (perfect flat-histogram
scheme with the exact density of states; tunnelling not `N²`; exponential for the `±J` spin glass; Wang–Landau has the same
scaling); Berg–Neuhaus, arXiv:hep-lat/9202004 (2d 10-state Potts, tunnelling time not exponential); Wang–Landau,
arXiv:cond-mat/0011174; Ge–Lee–Lu, arXiv:1911.03043 (information-theoretic lower bound `d^{1−o(1)}/ε^{2−o(1)}`, gradient
queries; "cell construction" is not in the abstract); Mathé–Novak, arXiv:math/0611285 (the abstract speaks of "certain
classes" and of adaption breaking the curse for non-adaptive methods; "Lipschitz logarithm" and "log-concave" are in the
paper, as far as I remember it, not in the abstract).  Hinrichs 2010: only the bibliographic record was found; the
description agrees with what I remember of the paper.  No statement attributed to a source is contradicted by its abstract.

## 8. Priority F — discrepancies between the report and theory report §11.23

I compared §11.23 of `docs/THEORY_REPORT.md` with the final report statement by statement — first the working tree of
about 15:10 UTC, then, in full again, the version of commit `e4351b9`, which is also that of `5ed4072` and of `89ac710`,
the HEAD when I finished (lines 5112–5593; the line numbers in this table refer to it).  Apart from the remark of D13 the section
claims nothing essential that the report does not claim; the differences:

| # | theory report | report | assessment |
|---|---|---|---|
| D1 | Theorem 11.80(c) (5385–5391): "`R_H(e) = max_t[F*(t) − te]`", "`R_H` is convex with slopes in `[−1,0]`", "`θ_na = R_H∘S^{−1}`" — no restriction on `e` | T9(c): `R_H = R̂` **for `e ≥ 0`**, `R̄_H ≤ R̂` in general; `θ_na = R̂∘Ŝ^{−1}` (§14 item 5 says this was changed on purpose) | The theory report says more than the report proves.  It is nevertheless **true** when `R_H` is read as `R̄_H`: `R̄_H = R̂` for all real `e` follows from T8(b) and the formula for `N` (§4 above).  The argument should be added; `θ_na(x)` for `x < R_H(0)` depends on it. |
| D2 | Proposition 11.81(b) (5414–5419), finding 4 of the section head (5138–5140): "numerically it is then the global one, so `R_H(e) = R_unif(e)` for `1 < βJ ≤ βJ*`", for general `(e,u)` | §6.6 (iii), §0 G3(e): the same, labelled [numerical], evidence at `u = 1`, `e ∈ {0, 0.02, 0.04}` only | **False as a general statement** in both documents (finding M1): for large `u`, or `e` near `e_c`, a far exit undercuts the symmetric one below `βJ*`.  Correct in the range computed. |
| D3 | Proposition 11.82(e) (5494–5497), (O5) (5514–5516): "the exponent of non-adaptive algorithms is known only to lie in `[0.00184, 0.00226]`" | §6.5 (4), §7.1 O5, §12 item 7a: the same | Both overstate (finding M2): `0.00226` is `R^{(2)}(0)`, a lower bound of `R_H(0)`; the proved upper end is `0.00338` (from `R_H ≤ R_unif`). |
| D4 | Proposition 11.82(e) (5492–5494): "the best cone around **any** shell certifies `0.00184`" | "over symmetric shells, over general binary profiles and over profiles with a free block alike" | The theory report generalises from three families to all shells.  As a lower bound of `N(S(0))` the number is proved; as a supremum it is numerical. |
| D5 | Proposition 11.82(b) (5459–5460): shells `(½; x, x)` are self-consistent "**exactly** for `x ≥ p_u`" | "for every `x ≥ p_u`" | The addition is right (necessity: the local condition `|logit x| ≤ u` at type `½`; my grid minimisation: not self-consistent at `x = 0.24, 0.26`, self-consistent at `p_u, 0.28, 0.298, 0.35`).  Both are numerical statements about a global minimum. |
| D6 | Theorem 11.76(c) (5215–5219): "`Z_gΦ_g⁺(D) ≤ Z_HΦ_H⁺(D)`"; "The factor cannot be dropped (`Z_H/Z_g` is attained)" | T4 has only `Φ_g⁺ ≤ (n+1)Φ_H⁺`; no statement about necessity | Both additions are correct (brute force, §5): a factor `Z_H/Z_g > 1` is attained; `n+1` is a bound of it. |
| D7 | Theorem 11.79(b) (5336–5340): "`θ_shell(X; μ₀) ≤ n_{μ*}(X) = θ_shell(X; μ*)`" | T8(a): "`≤ n_{μ*}(X) ≤ θ_shell(X; μ*)`" | The equality is correct (`𝒱(μ*) = α(μ*)` and T7). |
| D8 | Theorem 11.79(a) (5332–5335): error term "`− c_k ln(n+1)`" | T5: "`− c_k ln(n+1) − c_φ′`" | A constant dropped; immaterial. |
| D9 | Interpretation (i) (5541–5552): the ensemble "uniform inside every level set and **flat over the levels of a window**" is "the sampling law of a non-adaptive certified estimator that is optimal up to a polynomial factor for every `n`" | §9, "What the results say" (i): the stratified sample over **all** level sets; "that the levels outside the window may be dropped at the exponential scale … is not re-proved here" | The theory report drops the caveat.  What T1 proves for every `n` is the type-stratified sample over all `n+1` type classes. |
| D10 | Theorem 11.80, numbers (5397–5400): "with `B = 0` **every** coupling `−40 ≤ βJ ≤ 1` has exactly the uniform cube's values" | §5.3: computed at `βJ ∈ {−40, −8, −2, −1, 0, 0.5, 0.9, 1}`; proved for `0 ≤ βJ ≤ 1` | "every" is an extrapolation for the antiferromagnets (the parenthesis that follows says "numerical").  (§11.25, written after the report and not reviewed here, claims a proof of the equality for every antiferromagnet without a field.) |
| D11 | Proposition 11.82(b) (5460): "against `0.0446` from cones" | the same (§0, §6.2 (3), §6.3) | Both carry a number that I cannot reproduce: `max_m MI(`Gibbs shell of the cone`) = 0.04435`, attained at `m = ½` (finding m12). |
| D12 | Proposition 11.82(c) (5461): "`e₀ = 0.00181`" (section head, 5135: `≈ 0.0018`) | the same | The crossing of the two branches is at `0.001804`; `0.00181` is a linear interpolation between `0.001` and `0.002` (m10). |
| D13 | *Remark (an arbitrary symmetry group)* after Theorem 11.76 (5235–5267), with a sentence in the status paragraph (5160–5161) and in "Extensions" (5554–5556); added to the section during the review, labelled as the coordinator's | not in the report; its §10 (G5) only sketches that the every-`n` statements extend to other symmetry groups | **Correct on paper** (my check; details below the table).  Two conventions should be stated for a non-symmetric envelope, and the hypothesis "triangle inequality" should be visible.  Lean file read, not compiled. |

**D13 in detail.**  Setting of the remark: a finite space `X`, an envelope `d` (not necessarily symmetric), a finite group
`Γ` with `d(σx, σy) = d(x, y)` and `π(σx) = π(x)`; admissible means `ψ(x) − ψ(y) ≤ d(x, y)` (the orientation of
`GroupSampling.lean`); `dens_x(S) = |S ∩ Γx|/|Γx| = P_σ(σx ∈ S)`.
* *(a′)* is one line, as claimed: if `ψ(σb) < c − d(a, b)` then `ψ(σa) ≤ ψ(σb) + d(σa, σb) = ψ(σb) + d(a, b) < c`, so the set of
  group elements that send `b` into `{ψ < c − d(a,b)}` is contained in the set that sends `a` into `{ψ < c}`.  Consequence
  (mine, shorter than the route through a regularisation): the orbit-wise quantile `t(x) := max{c : dens_x{ψ < c} ≤ q}` is
  invariant and — by (a′) with `c = t(a)` — satisfies `t(a) − t(b) ≤ d(a, b)`; so `max(ψ, t)` is admissible and differs from `ψ`
  on orbit density at most `q`.  (The Lean file regularises arbitrary invariant levels, `c(x) = max_a[c₀(a) − d(a, x)]`; that
  needs the triangle inequality of `d`, which is a hypothesis of `regLevel_admissible` and is not mentioned in the remark.)
  The lower bound is the two-point argument with a uniform group element, `A(ψ∘σ) = A(ψ)` by invariance of `π`.  The
  sampling bound is the proof of T1 with `n + 1 → N_orb`: `dens_O{ψ ≤ t_O} > q`, so the orbit mean of `min(w, e^{−t_O})` is at
  least `q·e^{−t_O}` and the multiplicative Chernoff bound gives every orbit mean up to a factor 2 outside probability
  `e^{−Kq/8}`; Markov from above.  The factor `8N_orb ln(2N_orb/δ)/(1 − 2δ)` follows (up to the rounding of `K`, and with the
  loss `ln(4/δ)` in the accuracy, as in Theorem 11.76(a)).
* *(b′)* is T2 verbatim: `P_σ(x ∈ σD) = dens_x(D)`, and `A(ψ_g^{σD}) = A(ψ_g^D)` for an invariant instance.
* *(c′)* is T4 with `Z_g = Σ_O e^{−(J_O − Λ_g(O))} ∈ [1, N_orb]`: `Z_gΦ_g⁺(D) ≤ Z_HΦ_H⁺(D)` and `1 + Φ_g ≤ (N_orb + 1)(1 + Φ_H)`.  For a
  **non-symmetric** envelope two things have to be said, because the text reads as if they were as on the cube: (1) the
  deepest dip on `D` is `max_{y∉D}[ψ(y) − d(y, x)]` (this order of the arguments; it is admissible by the triangle
  inequality), so the exponent in (11.23.1) is `min_{y∉D}[d(y, x) + Λ_g(Γy)]`; (2) the landscape `Λ_g = −g + min(J + g)`
  satisfies `Λ_g(O) − Λ_g(O′) ≤ δ(O′, O)`, i.e. it is admissible for the *transposed* quotient envelope, so "`V` the largest
  `δ`-admissible minorant of `J`" must be read as `V(O) = min_{O′}[J_{O′} + δ(O′, O)]` — the largest minorant of `J` whose
  *negative* is an admissible residual; read literally, `−V` need not be admissible.  (c′) also needs the triangle
  inequality of `δ`; it holds because `Γ` acts by isometries (`δ(O, O′) = min_{y∈O′}d(x, y)` for any fixed `x ∈ O`, and then
  chain two minimisers).  With these readings the three lines of T4 go through.
* *Examples.*  The full isometry group of the uniform cube is transitive, so `N_orb = 1` and the statement is the one
  made; "empty when the number of orbits is exponential" is right.
* *Lean.*  `GroupSampling.lean` (365 lines, dated 15:23; no `sorry`, `admit` or `axiom`): the statements `lowDens_shift`,
  `regLevel_admissible`, `regLevel_lowDens_le`, `regLevel_smul`, `truncate_admissible`, `truncate_gdens_le`,
  `group_nonadaptive_queries_ge`, `group_queries_ge`, `gdens_mul_card_orbit` are the ones the remark quotes, stated for an
  arbitrary invariant class and target.  I did not compile it (no `lake build` under the brief); "[V]" rests on the
  coordinator's build.  The upper bound and (c′) are paper statements, as labelled.

**Other remarks.**  The status paragraph ("not yet refereed"; (a), (b) of Theorem 11.76 machine-checked; 11.78(b),
11.80(b), (c) "read but not re-derived") is accurate as far as I can judge; I read the docstrings and the theorem lists of
`SymmetricSampling.lean` and `TypeQuantiles.lean` (stated for every permutation-invariant class and target) and did not
check the Lean proofs.  Its sentence that the coordinator's recomputations "all agree with the workstream's numbers to
the digits printed" (5157) is about runs that I did not examine; two numbers that the section prints do not survive my
recomputation in the third digit (D11, D12), and the junction was recomputed there at `u = 1` only (D2).  The "possible
repair" for the nested algorithm is labelled [C] and discussed in §7.

**A note outside the section.**  Commit `89ac710` (18:33 UTC) carries, in §11.25 (Corollary 11.91(iii), lines 6001–6004,
outside the brief), a parenthesis that cites this referee for M1 ("the junction is at `βJ*` … for `u = 1` and, on the
referee's grid, for `u ≤ 2`; for larger slopes it comes earlier — the global half of Proposition 11.81(b) is false as a
general statement").  I had handed in nothing at that time; it must have been taken from the draft of this file in my
directory.  The finding did not change between that draft and this version, and the sentence renders it correctly, with
two precisions.  (1) On my grid the failure occurs for larger slopes **and small or negative accuracies** (`u = 8`: `e ≤ 0`;
`u = 6`: `e ≤ 0.3e_c`; `u = 4`: `e ≤ 0.6e_c`; `u = 3`: `e = 0.9e_c`); for `e ≥ 0.3E_unif` there is none up to `u = 8`, and at `e = 0`
none up to `u = 6`.  (2) What I computed is that the uniform cube's profile `μ*` loses its value below `βJ*` (it drops to
`0`: ten cells, two solvers, an explicit feasible exit); that `R_H` itself leaves `R_unif` there — "the junction comes
earlier" — rests on searches in two of these cells (binary and multi-block profiles, run `t24`, made after that draft:
`0.36742 < 0.39854`, `0.41763 < 0.41857`) and on the comparison chain of T9(e), not on a proof (§6.4).  The same corollary states a sufficient condition for the equality (the uniform cube's optimal
profile keeps its cheapest exit inside the type class `½`, and `½` is a contact type); this agrees with what my grid
shows, but I have not reviewed that section.

## 9. My numerics: scripts, commands, sizes, run times

Everything is in `<scratch>/referee10/` (`code/`, `out/`); own code (numpy/scipy; nothing imported from the workstream, the
coordinator or the repository), fixed seeds, `ulimit -v 4000000`, one process at a time (three checks of 2–5 s — `t10`, `t14`,
`t16b` — overlapped with a queued job; numpy's linear algebra used several threads inside the one process), every run under ten minutes
(`timeout 590`; one run, `t04b` at `e = 0.05`, was cut by the timeout during its final re-evaluation — its search output is
complete and its best profile was re-derived and re-evaluated by `t21`).  Commands are run in `code/` as
`python3 <script> <args>`; the queues `queue1.sh` … `queue6.sh`, `run_de_e0.sh` ran them in sequence, `out/queue.log` lists
every queued command with its return code and run time.

Libraries: `r10lib.py` (rate function, table of `v` on `4·10⁵` points, the three inner solvers S1/S2/S3 of §6),
`r10search.py` (parametrisation of profiles, Nelder–Mead), `r10slp.py` (exact solution at a fixed exit type by nested
bisection; multipliers; the linear programme over laws of block types, `scipy.optimize.linprog`/HiGHS), `r10tab.py`
(binary optima for a landscape, thresholds `E`, cone shells, cone formula, `n_μ` two ways), `r10fin.py` (exact finite-`n`
sums on a `k`-block grid with an `ℓ¹` min-plus transform; brute force on full cubes).

| script → output | what | sizes | time |
|---|---|---|---|
| `t00_control.py` → `t00_control.txt` | S1, S2, S3 against the closed form of the uniform cube (`e = 0, 0.02, −0.03`) and against each other at three two-phase profiles | — | 7 s |
| `t02_binary.py` → `t02_binary.txt` | binary optima at `e = −0.05, 0, 0.02, 0.05` (4 starts each) and the free-block family at `e = 0, 0.002, 0.02`; S1/S2/S3 | — | 119 s |
| `t03_slp_test.py` → `t03_slp_test.txt` | the SLP ascent: from the binary optimum at `e = 0.02` (finds the free block), at `e = 0` (LP optimum = current value), from an asymmetric start | 161 + zoomed exit types, 401 atoms | 5 s |
| `t04_slp_search.py 1.5 0 1 0 101 40 480` → `t04_slp_e0_seed101.txt` | C1: SLP + Nelder–Mead from 40 random profiles (2–6 atoms), seed 101 | 40 starts | 305 s |
| `t05_de.py 1.5 0 1 0 k seed pop maxiter` → `t05_de_e0_k{3,4,5}_seed*.txt` | C1: differential evolution over `k`-block profiles, Sobol initialisation, then Nelder–Mead, S1/S2/S3 | `k = 3` (seeds 11, 21), `4` (12, 22), `5` (13); 20 768–25 928 evaluations | 177–297 s each |
| `t04b_slp_alt.py bJ bB u e seed 30 520` → `t04b_*.txt` | alternating SLP / Nelder–Mead from 7 structured and up to 30 random starts; S1/S2/S3 of the best three | `e = 0` (seed 5), `0.02` (6), `0.05` (7), `0.0015` (8); `βB = 0.05`: `e = 0` (9), `0.02` (10) | 437–590 s each |
| `t21_e005.py 0.05` → `t21_e0.05.txt` | symmetric laws with 5, 7, 9 atoms at `e = 0.05`; S1/S2/S3 | — | 106 s |
| `t22_u03_multi.py` → `t22_u03_multi.txt` | `u = 0.30`, `e = 0`: multi-block search around the marginal shell | 24 starts | 209 s |
| `t06_branches.py` → `t06_branches.txt`, `t06_table.json` | binary and free-block branches at 19 accuracies, each value re-evaluated with S2; the crossing `e₀`; unrestricted binary profiles at three accuracies | — | 396 s |
| `t07_junction.py` → `t07_junction.txt` | §6.6 (ii) by finite differences (5 cases); (iii): `r_{μ*}(e)` against `R_unif(e)` with S1 and S2 | `u ∈ {0.3, 1, 2, 4}` × 5 accuracies × 5 couplings | 56 s |
| `t07c_junction_grid.py` → `t07c_junction_grid.txt` | (iii) on a grid of couplings `1 + f(βJ* − 1)`, 11 values of `f`; details of the failing cells (exit, S2, contact set, best binary profile) | `u ∈ {1, 2, 3, 4, 6, 8}` × 7 accuracies | 258 s |
| `t24_junction_multi.py 8 0 0.99 24 14 380`, `… 4 0.6ec 0.99 25 14 380` → `t24_junction_multi_u8_e0.txt`, `t24_junction_multi_u4_0.6ec.txt` | two failing cells of that grid: the best symmetric binary shell (at the edge of the cliff where a constant exit becomes feasible) and a multi-block search (structured starts adapted to the cell and random splittings; alternating SLP / Nelder–Mead at the accuracy `e + 2·10⁻⁵`); S1/S2/S3 at the accuracy `e` | 16 and 23 starts | 451 s, 329 s |
| `t07b_junction_scan.py` → `t07b_junction_scan.txt` | first version of that scan (bisection with an absolute tolerance that is too tight for large `u`: several spurious flags; **superseded by `t07c`**, kept for the record) | — | 144 s |
| `t08_tables.py 53 / 65 / 67` → `t08_tables_*.txt` | spot checks of §5.3 (two rows, all seven columns), §6.5 (`u = 0.6, 0.3, 0.25`), §6.7 (`βJ = 1.2, 1.3`; field at coexistence) | — | 135 / 159 / 187 s |
| `t19_couplings.py` → `t19_couplings.txt` | §6.6 table at five couplings; §6.7 at `βJ = 2` | — | 250 s |
| `t20_zero_field.py` → `t20_zero_field.txt` | field at coexistence: `H` and the zero residual at `e = 0, 0.01, 0.02` | — | 48 s |
| `t09_u03.py 0.30` → `t09_u03.txt` | `u = 0.30`: `R^{(2)}(e)` at nine accuracies with S2, slopes, `r_μ(e)` of two shells, best shell-cone at `S(0)` three ways, general binary profiles, the proved upper end | 400-point scans of shells | 371 s |
| `t18_pair.py` → `t18_pair.txt` | pair identity with shells (through `r_μ`; by clippings; truncated shell-cone on a `2001²` grid refined 5 times), truncated cone around the centre, free-block optimum | 3 accuracies | 17 s |
| `t16_misc.py`, `t16b_acone.py`, `t23_small.py` → `t16_misc.txt`, `t16b_acone.txt`, `t23_small.txt` | wells, barrier, `u_top`; self-consistency of shells (grid `2000²`); `θ_shell(X) → a`; `a_cone` (both wells separately, 10 centre types); cone formula; zero residual; equality cases of T9(e) | — | 20 s, 5 s, 22 s |
| `t10_brute.py` → `t10_brute.txt` | brute force on full cubes: (2.3) and `A(dip)/A = 1 + Φ` (266 cases, `n ≤ 9`), T4 (the same cases; the factor), block sums against brute force (236 cases, 2–4 blocks, `n ≤ 9`), T1(a) (108 cases) | — | 2 s |
| `t11_finite.py A` / `AB` → `t11_finite_A.txt`, `t11_finite.txt` | T3(a) by exact sums (`n = 60, 120, 240`; 48 cases; an earlier choice of budgets, 36 cases, in `t11_finite.txt`); four entries of §6.3 | up to `501²` cells | 3 s, 8 s |
| `t13_T3b_sets.py u 50 seed` → `t13_T3b_u1.txt`, `t13_T3b_u4.txt` | T3(b) on 11 families of sets, 4-block grid, `n = 200` | `51⁴ = 6.8·10⁶` cells; 210 and 192 sets | 143 s, 148 s |
| `t15_smallcubes.py` → `t15_smallcubes.txt` | all subsets of `Q_3`, `Q_4` | 254; 65 534 | 10 s |
| `t12_convex.py A 7 0,1,2`, `A 7 3,4`, `BCD 7` → `t12_convex_*.txt` | T9(b) (multi-atom searches in four convex cases and for the zero residual with two phases), T9(a), T9(e) on random profiles, T9(c) | see §4 | 272, 179, 115 s |
| `t17_convex_general.py 0 / 1 / 2` → `t17_convex_general_*.txt` | T9(b), (d) for three convex rate functions that are not Curie–Weiss | 12 cases | 210–217 s each |
| `t14_hs.py` → `t14_hs.txt` | Hubbard–Stratonovich mixture (`n = 10, 40`), the tilt identity on `Q_10`, `|∂_y ln A_y|` | — | 3 s |
| `t01_speed.py` | timing of S1 (no output file) | — | 10 s |

**Accuracy.**  S1 with default settings (used inside searches) overestimates the inner minimum by up to `2·10⁻⁹` (`10⁻⁷`
relative for values `≈ 0.4` at `u ≥ 3`); every number quoted in this report is from the fine settings and agrees with S2 and
S3 to `≤ 2·10⁻⁹`, except at the marginal shells of `u = 0.30`, where the value is discontinuous in the shell and S2 differs
from S1 by up to `8·10⁻⁷`.  The same kind of edge occurs in the cells of M1 (§6.4): a supremum that sits where a constant
exit becomes feasible is not attained, and exactly at the edge S1/S2 and S3 fall on different sides; there I quote values
at a margin `2·10⁻⁵` in the accuracy, where the three agree to `10⁻¹⁰`.  The independence of the solvers is real but each
has a blind spot of its own: S2 is a scan over exit types and can miss a feasible window narrower than its grid (it did,
at that edge); S3 is a multi-start local method; S1 relies on a table of `v`.  **Errors of mine caught on the way:** (1) entropies of types `1 + 10⁻¹⁶` returned `−∞` and
emptied the candidate list of S1 (fixed by clipping); (2) the first SLP used a quasi-Newton dual solver for the
multipliers, which failed near infeasible exit types and made the LP model inconsistent with the current value (replaced by
the exact nested bisection); the exit grid then had to be refined around the active exits (V-shaped minima) before the
model reproduced the current value to `10⁻⁸`; (3) `t06` first returned `nan` or a wrong local value for shells that are not admissible at negative
accuracies (fixed and re-run; the first output is kept as `t06_branches_first_run_void_for_negative_e.txt`); (4) the first junction scan
(`t07b`) used a tolerance below the solver accuracy at large `u` and a bisection that presupposed monotonicity — replaced
by `t07c`; (5) my first search for the zero residual with a field started outside the stable well and returned `0`
(`t08_tables_67.txt`, last line; corrected in `t20`); (6) the first version of `t24` measured the margin of the far exit at
the well itself; the cheapest constant exit is at the edge of the well's contact interval (`I′ = u`), and at the edge
profile the three solvers disagreed (corrected by the margin in the accuracy; that test run was not saved to a file, its
numbers are quoted in §6.4).

## 10. What I did not check

* **Lemma SL, Proposition 11.65(b), Theorem 11.64 and Theorem 11.22/11.45** — used as inputs (R9 refereed the first three;
  the last are machine-checked statements, read as stated).  T12 inherits whatever is open in Theorem 11.64.
* **Lean**: nothing compiled (the brief excludes it).  I read the statements of `GameFunction`, `symmetric_queries_ge`,
  `symmetric_nonadaptive_queries_ge`, `truncated_weight_queries_ge` and of `GroupSampling.lean` (§8, D13) and checked that
  the four files (`GamePair`, `SymmetricSampling`, `TypeQuantiles`, `GroupSampling`) contain no `sorry`, `admit` or `axiom`;
  the claim "[V]" for Theorem 11.76(a), (b) and for the remark after it rests on the coordinator's build, not on mine.  `HintPair`/`GameFunction` for
  `F*` is a paper statement (checked in §4).
* **T3(b) on sets without symmetry** beyond `Q_4`; rates of convergence (`ω_n`); nothing quantitative is proved and I did
  not try.  The exact sums cover 4-block-symmetric sets at `n = 200` only.
* **C1 and O2 are not decided**: my searches are evidence of the same kind as the author's (different methods, no proof);
  no upper bound of `R_H(0)` better than `R_unif(0) = 0.0291391` is known.  The values beyond `e₀` are lower bounds.
* **§6.4** (other symmetric instances; 23 landscapes): not recomputed, except the zero residual and the cone formula.
  **§6.7 (ii), (iii)** (the onset `βJ**` of the free block and its estimate): not recomputed; I checked the local formula
  `A(λ_f)` on paper, two rows of the table at `e = 0.02`, and `βJ = 2`.  **§6.3**: four entries of two rows; the rows
  "beyond one centre" and the one-phase and field rows were not recomputed.  **§7.3** (the author's seven families): replaced
  by my own families (§6.7), not reproduced.
* **§10 (G5)**: read; no check.  **T5** has no numerical check of mine beyond the two truncated shell-cone entries of §6.3.
* **(iii) of §6.6 between the grid points**: my scan has `f ∈ {0.1, …, 0.9, 0.95, 0.99}` and seven accuracies per `u`; that
  the junction is *exactly* `min{βJ*, βJ_w}` is an observation on that grid, not a theorem.  Multi-block profiles were
  searched in two of the ten failing cells only (`t24`); that `R_H < R_unif` there is the outcome of searches, not a proof.
* **The author's code** was not run and not read beyond `tfin.py` (lines 1–170, to see the definition of the capped family
  and of the truncation levels), the function lists of `tlib.py` and `tfin.py`, a `grep` for `a_cone`/`0.0446` over `code/` and
  `out/`, and one output file (`t15_e0_bJ1.5_u1.txt`, to explain `e₀`).  The coordinator's scripts were not read; I read their
  `README.md` and `out_e_threshold.txt`.
* **Theory report outside §11.23.**  Sections 11.24–11.27 appeared or grew while I worked (§11.25, "slices", builds on
  Theorems 11.78–11.79, claims the equality with the uniform cube for every antiferromagnet without a field and restates the
  junction; its text says it is not refereed).  They are outside the brief and I did not review them; of the remark on
  symmetry groups inside §11.23 I checked the paper argument only (§8, D13).  My verdicts on T3 and T8 (Theorems
  11.78, 11.79) are what such later sections can rely on; nothing else.
* **Prior art**: abstract pages and one search result only; no paper was read.
* **Floating point**: double precision, no interval arithmetic.  S2 is a weak-duality bound at each exit type on a grid
  with local refinement, not a rigorous enclosure over the continuum of exit types.

## Appendix: files in `<scratch>/referee10/`

`R10_report.md` (this file) · `parts/` (its sections) · `code/`: libraries `r10lib.py`, `r10search.py`, `r10slp.py`, `r10tab.py`,
`r10fin.py`; tests `t00_control.py` … `t24_junction_multi.py` (commands in §9); queues `run_de_e0.sh`, `queue1.sh` … `queue6.sh` ·
`out/`: one `.txt` per run (names in §9), `queue.log` (queued commands, return codes, run times), `t06_table.json`,
`sec1123_*.txt` (§11.23 of the theory report as in commits `e4351b9`, `5ed4072` and in the working tree at 18:07 UTC, which is
the file of commit `89ac710` — identical).

