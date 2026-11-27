# R18 — referee report on two arguments of the engineering division: ENG-RES-0014 §1 (the classification rule of the mean-run evaluator) and §4 (the bound for instances that are not products)

*Workstream R18 of the science division, 2026-11-26.  **Internal review** by a referee of this division; it is not
external peer review.  Object: the engineering branch at `1cc4e1c` (ENG-RES-0014 unchanged there since `ce71724`),
read from the export `/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/eng_ro_1cc4e1c/`
(`<ENG>` below).  Nothing of theirs was modified; nothing ran on Modal; no network; no subagents.  Everything of mine
is in `experiments/science/ws_R18/` (notes: `NOTES.md`; logs: `logs/`).  Our branch stood at `0930440` when the work
began; no git command that changes state was run.*

**Four kinds of checking, kept apart throughout.**  *Review*: re-derived on paper.  *Replication*: computed with
code that is not theirs (`r18_rule.py`, `r18_mean.py`, `r18_nonproduct.py`, `r18_mixed.py`: mine, written from the
statements; `ws_R6/r6lib.py`: our division's literal engine).  *Re-run*: their code, from the scratch copy
`ws_R18/rerun_copy/`, Python reference only (`python3 -I -B`, the C kernel never built), 2 GB address-space limit.
*Read only*: read, not recomputed.  Labels as in `COMMON.md` rule 6: **[P]** paper proof here, **[N]** numerical
evidence, **[V]/[K]/[C]/[H]** not used.  Abbreviations: KR = `docs/workstreams/K_REPORT.md` (the text of Algorithm
2L⁺, §2.2, l.207–246); M = ENG-RES-0014 (`<ENG>/docs/collaboration/responses/engineering/ENG-RES-0014.md`, line
numbers of that file).

---

## 0. Verdict

1. **§1, the classification rule: proved as stated.**  `HIGH ⇔ W > s·e^{−c}`, `c = max_l min(b − A_l, B_l)`, and the
   window `W e^{b−A_l} ≤ s_j < W e^{B_l}` are exact — per point, for any admissible positions, with every tie on the
   side the message gives it **[P, §2.1; N: 15 191 163 literal decisions and 2 400 374 window checks of my own loop in
   exact arithmetic, 0 violations, eight controls all failing]**.  The printed argument needs one more sentence
   (m2) and one sentence needs a condition (m1).  No published number is affected: the range inequality holds in
   all 468 cells with margins ≥ 7.8.
2. **§4, the bound: the inequality is proved, at the level it is computed** (mean runs; uniform inner behaviour;
   the same reference value; the range condition of §1) **[P, §2.2; N: 1 680 instances that are not products,
   14 168 rung checks, 0 violations; 1 800 literal runs, pointwise with the realised sample sizes, 0 violations;
   the control with `lo` and `hi` exchanged fails everywhere]**.
3. **The conclusion drawn from §4's second table is false as worded — one major finding (M1).**  "No such instance
   costs more than the worst product instance found" (M l.26, title) and "by an amount that is a bound and not the
   cost of an instance" (M l.340): in each of the six cells where the searched bound exceeds the searched product
   worst case by more than `0.001·na`, **a product instance has a mean-run cost equal to the searched bound — by
   their own reference evaluator, no claim of the theorem violated**.  The column measures the shortfall of the
   product search of job M-008 (up to `0.02005·na`, a factor `e^{1.64}` in evaluations), not a difference between
   products and other instances.  In substance their reading ("leaving the product family does not change the
   picture") comes out *stronger* — in none of the 15 cells where the bound lies more than `10⁻⁴·na` above the
   product search is there a gap — and the tables of ENG-RES-0008 at `n ≤ 500` come out *weaker*: the search behind
   them was not converged.
4. **Findings by class: critical 0; major 1 (M1); minor 10 (m1–m10); observations 5.**
5. **Re-runs** (their Python reference): `recheck_classification` 1 536 of 2 624 searches, `nonproduct_bound` 300 of
   468 cells — every compared number agrees with their stored files to `≤ 4.3·10⁻¹⁴`; the rest could not be re-run
   under the 2 GB limit (their reference needs 6.5 GB at `n = 16 000`: m8).
6. **Replication of their evaluator**: my exact mean run agrees with their Python reference on 2 700 runs
   (1 057 582 levels: every sample size, every rung's calls, cost, `C_max`, constants), once one tolerance of theirs
   is reproduced (m9), and reproduces their stored bound in six published cells to `≤ 2.8·10⁻¹⁴`.
7. Outside the range condition (`lo < b` or `x₀ − hi < b`; no design used) the statement "its classification shift
   is the same" is false and the evaluator's pair mode is not an upper bound: a product instance costs `e^{6.83}`
   times what it returns (m3).
8. The uniformity of the inner behaviour is essential for the bound: with "bottom" on some shells and "top" on
   others the cost exceeds both uniform bounds, by `e^{0.56}` in the example found (§5; their own stated limit).
9. Not checked: the second table of §4 as a search (Modal; read only — but its stored maximisers were
   re-evaluated); anything at `n ≥ 16 000`, and `n = 8000` for `u = 1, 2` except the flat instance; the C kernel;
   their test suite; their literal simulator `simulate.py`; §2, §3, §5 of the message.
10. Own errors: four (a memory limit exceeded once; three compute processes for 25 s; two time stamps typed before
    the clock was read; one mean run fed a float where the instance has an exact tie) — §7.

---

## 1. The statements as I understand them, with the hypotheses the message leaves implicit

**Setting** (KR §2.2).  Levels `s_j = s₀e^{jλ}`, `j = 0, …, J`, visited in increasing order.  An outer point `a` with
fibre average `W` gets the trivial bracket `[e^{−ψ(a,0)−un_i}, e^{−ψ(a,0)+un_i}] = [W e^{−t₀}, W e^{x₀−t₀}]`,
`t₀ = ψ(a,0) + un_i + ln W` ("place"), `x₀ = 2un_i`, and rung 0.  Step 1: *"to classify `a_i` at level `j`, while
`U_i > s_j` and `L_i ≤ s_je^{−b}` move `a_i` to the next rung `l`, call `I_l` on its fibre and intersect; then `a_i`
is low if `U_i ≤ s_j` and high otherwise"*; brackets "are only ever refined".  The rung-`l` procedure returns for
this point `[W e^{−α_l}, W e^{β_l}]`.

### §1 of the message (M l.29–63)

* **S1 (positions).**  After rung `l` the point holds `[W e^{−A_l}, W e^{B_l}]`, `A₀ = t₀`, `B₀ = x₀ − t₀`,
  `A_l = min(A_{l−1}, α_l)`, `B_l = min(B_{l−1}, β_l)`.
  *Implicit:* (h1) one pair `(α_l, β_l)` per point and rung, the same whenever the call is made (the proof of the
  theorem draws the randomness of every potential call in advance: KR l.277–278); (h2) the message writes no point
  index: "uniform" positions; (h3) valid brackets, `α_l, β_l ≥ 0`, `α_l + β_l ≤ x_l`.
* **S2 (window).**  The point is moved from rung `l` to `l+1` at level `j` iff `W e^{b−A_l} ≤ s_j < W e^{B_l}`.
* **S3 (rule).**  The point is HIGH at the level `s` iff `W > s·e^{−c}`, `c = max_{0≤l≤L} min(b − A_l, B_l)`,
  `0 ≤ c ≤ b`.  *Implicit:* (h4) the point meets the level at the rung where earlier levels left it; (h5) levels in
  increasing order; (h6) `x_L ≤ b`.
* **S4.**  "Bottom" (`α_l = 0, β_l = x_l`) gives `c = b` and "top" (`α_l = x_l, β_l = 0`) gives `c = 0` "as long as
  `t₀ ≥ b` and `x₀ − t₀ ≥ b`".
* **S5.**  A `u`-Lipschitz fibre has `t₀ ∈ [n_i(u − Λ₁), n_i(2u − Λ₁)]`, "inside the range for every design used".
* **S6.**  Hence no published number of X-005 changes (table `recheck_classification`).

### §4 of the message (M l.289–349)

* **T1.**  For an instance "with the same law of fibre averages" whose fibres sit at places `t₀(a) ∈ [lo, hi]`,
  "with either uniform inner behaviour its classification shift `c` is the same, so its sample sizes are those of
  the product instance".
  *Implicit:* (g1) the same reference value `ψ₀` — the levels `s_j` and the initial `ℓ` are functions of it; the
  comparison is at a fixed pair (law, `ψ₀`); (g2) the range condition of S4 for *every* place in `[lo, hi]`; (g3)
  "uniform" means the same `(α_l, β_l)`, `l ≥ 1`, for all points; (g4) everything is a mean run (M l.399).
* **T2.**  The window of an atom at rung `l → l+1` is inside `W e^{b − min(hi, α_l)} ≤ s_j < W e^{min(x₀ − lo, β_l)}`.
* **T3.**  So the mean run with `A₀ = hi`, `B₀ = x₀ − lo` counts at least as many calls at every rung, and is "an
  upper bound on the evaluations of every instance with that law, product or not", for
  `[lo, hi] = [n_i(u − Λ₁), n_i(2u − Λ₁)]`.  *Implicit:* (g5) inner costs `C_l` that do not depend on the fibre.
* **T4 (reading).**  At the stored worst laws the bound coincides with the product cost; searched directly it
  exceeds the worst product instance by more than `0.001·na` only at the three smallest sizes, "by an amount that
  is a bound and not the cost of an instance"; in the title and in §0: instances that are not products "cannot
  cost more than the worst product instance [found]".

### Line by line

| | sentence of the message | status | decided by |
|---|---|---|---|
| 1.1 | S1, the nested positions (M l.35–37) | **holds** *(review)* | KR l.225–227: trivial bracket, "call `I_l` … and intersect" |
| 1.2 | S2, the window, "as before" (M l.37–38) | **holds, exactly** *(review, replication)* | `L ≤ s e^{−b}` is non-strict (left end closed), `U > s` strict (right end open); 2 400 374 checks, 0 wrong; strictness exchanged: 360 035 wrong |
| 1.3 | "leaves the loop HIGH at the first rung with `L > s e^{−b}` while `U > s`, and LOW at the first rung with `U ≤ s`" (M l.40–41) | **holds** *(review)* | KR l.226–227: the loop condition is the conjunction; afterwards "low if `U ≤ s`, high otherwise" — where both `U ≤ s` and `L > s e^{−b}` hold the point is LOW.  "First rung" is the first from the rung the point is at (m2) |
| 1.4 | "Since `B_l` decreases in `l`, it is HIGH iff `W > s·e^{−c}`" (M l.41–43) | **holds; argument to complete** (m2) *(review, replication)* | §2.1; 15 191 163 decisions, 0 wrong; `min`/`max` exchanged: 50 105 wrong |
| 1.5 | ties | **hold as written** *(replication)* | `W = s e^{−c}`: LOW (156 789 cases; tie given to HIGH: all 156 789 wrong); `U = s`: LOW (138 328 cases met); `L = s e^{−b}`: not HIGH at that rung, the point is moved on (320 930 cases met) |
| 1.6 | last rung; a point never classified | **holds** *(review, replication)* | `A_L + B_L ≤ x_L ≤ b` empties the window at rung `L`: 0 unclassified; with `x_L > b` (control) 21 951 points unclassified.  In floating point with `x_L = b`: the tie rule of ENG-MSG-0003 §5 *(read only)* |
| 1.7 | `0 ≤ c ≤ b` (M l.43) | **holds** given valid brackets *(review, replication)* | `min(b − A_l, B_l) ≤ b − A_l ≤ b`; at `l = L` both `b − A_L ≥ b − x_L ≥ 0` and `B_L ≥ 0`; with invalid brackets `c` leaves `[0, b]` in 82 294 of 100 000 points while the rule still holds |
| 1.8 | S4, "bottom gives `c = b` and top gives `c = 0` as long as `t₀ ≥ b` and `x₀ − t₀ ≥ b`" (M l.45–46) | **holds with a condition to add** (m1) | `c_bottom = max{min(b−t₀, x₀−t₀), min(b, x₁, x₀−t₀)}`: needs `x₁ ≥ b` |
| 1.9 | "with `t₀ < b` under top the literal algorithm classifies points in `(s e^{−(b−t₀)}, s]` HIGH at rung 0 and the old convention did not" (M l.48–50) | **holds** *(review, replication)* | at rung 0, `L = W e^{−t₀} > s e^{−b}` and `U > s`; such a point was not refined at a lower level (§2.1) |
| 1.10 | "literal runs side with the exact rule (ratio of costs up to `e^{4.2}` at a flat landscape)" (M l.50–51) | **holds** *(replication, re-run of their reference)* | `4.1744` in ln cost, by my code and by their reference; literal `r6lib` runs stop at the exact rule's level in 750 of 750 (§3.6) |
| 1.11 | S5, the range of `t₀` (M l.51–52) | **holds** *(review)* | `|ψ(a,b) − ψ(a,0)| ≤ u|b|` gives `e^{−ψ(a,0)}((1+e^{−u})/2)^{n_i} ≤ W ≤ e^{−ψ(a,0)}((1+e^{u})/2)^{n_i}`; both ends attained by the cones `ψ(a,0) ± u|b|` |
| 1.12 | "inside the range for every design used" (M l.52) | **holds** *(replication)* | all 468 cells: `lo − b ≥ 10.17`, `x₀ − hi − b ≥ 7.82`, smallest at `u = ½, n = 250, φ = 0.85` (`n_i = 38`); `logs/cells.log` |
| 1.13 | table `recheck_classification` (M l.54–56) | **agrees where re-run** (1 536 of 2 624) *(re-run)*; m6, m7 | §4 |
| 1.14 | "So no published number changes" (M l.58) | **holds**, for a stronger reason | on the whole search family the two rules are the same function (1.12), not only at the stored maximisers |
| 1.15 | agreement with literal step-by-step runs, five configurations (M l.58–61) | *read only* (their tests need the C kernel) | replaced here by §3.2 and §3.6 |
| 4.1 | "The search family of ENG-RES-0008 has one place `t₀` for all fibres" (M l.291) | **holds** | and that place is tied to the law, `t₀ = un_i + c_in`: M1 turns on this |
| 4.2 | "any instance with the same law of fibre averages whose fibres sit at places `t₀(a) ∈ [lo, hi]`" (M l.291–292) | **condition to add**: and the same reference value (m4) | the levels are `s₀e^{jλ}`, `s₀ = e^{−ψ₀−un}` |
| 4.3 | "With either uniform inner behaviour its classification shift `c` is the same" (M l.292–293) | **holds with a condition to add** (m3) | `c_top(t₀) = max{0, min(b−t₀, x₀−t₀)}` is `0` iff `t₀ ≥ b`; true for all 468 cells; false otherwise |
| 4.4 | "so its sample sizes are those of the product instance — the outer loop sees the law and `c` only" (M l.293–294) | **holds** *(review, replication)* | 1 680 instances: 0 differ at any of 946 694 levels; 1 800 literal runs: identical to the product instance on the same outer sample in 1 800 |
| 4.5 | "The places enter through the refinement windows alone" (M l.294–295) | **holds**, given 4.3 | |
| 4.6 | T2, the union window (M l.295–298) | **holds**; notation (m5) | `A_l = min(t₀, α₁,…,α_l)` is nondecreasing in `t₀`, `B_l = min(x₀−t₀, β₁,…,β_l)` nonincreasing, at every rung |
| 4.7 | "counts at least as many calls at every rung as any such instance" (M l.300–301) | **holds for mean runs** *(review, replication)* | 14 168 rung checks, 0 above; `lo`/`hi` exchanged: 1 661 above |
| 4.8 | "an upper bound on the evaluations of every instance with that law, product or not" (M l.301–302) | **holds for mean-run evaluations** (m4) | cost `= 1 + max_j M_j + Σ_l calls_l·C_l`: the first two terms are equal, `C_l` are constants; literal runs exceed the mean-run number in 1 130 of 1 800 |
| 4.9 | the range `[lo, hi]`, "the whole feasible range" (M l.302) | **holds** | 1.11 |
| 4.10 | table `nonproduct` (M l.306–316) | **agrees where re-run** (300 of 468 cells) *(re-run)* | §4 |
| 4.11 | tables `anyplacement…` (M l.321–335) | *read only* as a search; its stored maximisers re-evaluated | M1 |
| 4.12 | "by an amount that is a bound and not the cost of an instance" (M l.339–340); "no such instance costs more than the worst product instance found" (M l.26) | **false** (M1) | `logs/cell_v2_*.log`, `logs/cell0_*.log` |
| 4.13 | "the bound is never below the product cost at the same law, so a search of the bound that ends below the product search has simply found less" (M l.341–342) | **holds** — and the same sentence applies to the positive entries | bound below the product instance: 0 of 840 runs |
| 4.14 | "What this does not cover: …" (M l.346–349) | fair; incomplete (m10) | §5 |

### The questions of the brief, answered in one line each

*Item 1.*  (i) "Bottom gives `c = b`, top gives `c = 0`" — correct in the stated range if moreover `x₁ ≥ b` (1.8, m1);
the range of `t₀` is correct and inside it for all 468 cells (1.11, 1.12).  (ii) The window is exactly the set of
(point, level) pairs at which rung `l + 1` is called, with the left end closed and the right end open (1.2).
(iii) The rule holds for positions that differ from rung to rung in any way — even invalid or too wide below
the last rung — and *per point*; the same positions for all points are needed only where the evaluator turns
the rule into one threshold for the whole law, and there one common shift suffices (§5).

*Item 2.*  (a) `c` is independent of the place exactly under the range condition; that holds in every cell
(4.3, m3).  (b) The window is monotone in `A_l` and `B_l` in the direction used at every rung, also after the
minima (4.6, m5).  (c) The comparison is pointwise in the sample, with the realised sample sizes; the number of
the message is its mean-run counterpart and is not a bound on literal runs; the cost inherits it because the
outer terms are equal and the inner costs constant (4.7, 4.8, m4).  (d) The bound covers every joint law of
place and average; it is attained by such joint laws, and in their cells by product instances (Proposition
R18.1 (iv), M1).  (e) The range is correct (1.11).

---

## 2. Findings

### 2.1 The rule, with a complete proof (for 1.4, m2) **[P; checked numerically: §3.1]**

Fix a point and write `w = ln W − ln s` for a level `s`.  At rung `l` the point is *unclassified* iff
`−B_l < w ≤ A_l − b`, *LOW* iff `w ≤ −B_l`, *HIGH* iff `w > h_l := max(A_l − b, −B_l)`.  `B_l` is nonincreasing in
`l` (intersection).  Let the point meet the level at rung `l₀` and leave the loop at rung `l* ≥ l₀`.

* *HIGH at `l*`* ⇒ `w > h_{l*} ≥ min_l h_l = −c`.
* *LOW at `l*`* ⇒ `w ≤ −B_{l*}`.  For `l ≥ l*`: `w ≤ −B_{l*} ≤ −B_l ≤ h_l`.  For `l₀ ≤ l < l*` (rungs passed at this
  level): `w ≤ A_l − b ≤ h_l`.  For `l < l₀` (rungs passed at an earlier level `s′ < s`): there
  `w′ := ln W − ln s′ ≤ A_l − b`, and `w < w′` because the levels increase; so again `w ≤ h_l`.  Hence
  `w ≤ min_l h_l = −c`.
* The loop ends at rung `L` at the latest: `A_L + B_L ≤ α_L + β_L ≤ x_L ≤ b` makes `(−B_L, A_L − b]` empty.

So HIGH ⇔ `w > −c`, i.e. `W > s e^{−c}`, with the tie `W = s e^{−c}` LOW.  The proof uses: intersection (`B_l`
nonincreasing — `A_l` monotone is *not* used), levels in increasing order, one bracket per (point, rung), and
`α_L + β_L ≤ b`.  It does not use that brackets are valid, nor `α_l + β_l ≤ x_l` for `l < L`, nor that different
points have the same positions.  Each of these statements has a run behind it (§3.1, block E).

**Window and calls [P].**  At rung `l` the point is moved on iff `L ≤ s e^{−b}` and `U > s`, i.e.
`W e^{b−A_l} ≤ s < W e^{B_l}`.  The windows are nested in `l` (both `A_l` and `B_l` nonincreasing), so the point
calls `I_{l+1}` in the whole run iff some level `j ≤ j_stop` of its rung-`l` window has `i ≤ M_j`: if `j` is the
first such level, the point is at a rung `≤ l` there or has passed it already, and every window of a lower rung
contains `j`.  Hence `calls_{l+1} = #{i : i ≤ max{M_j : j ≤ j_stop, s_j ∈ win_l(a_i)}}` — the formula of ENG-RES-0008
§1 — in every run, with the realised `M_j` (verified on 1 800 literal runs: §3.5).

### 2.2 The bound, with its hypotheses (for T1–T3) **[P; checked numerically: §3.3–§3.5]**

**Proposition R18.1.**  Fix a design, inner costs `C_l` that do not depend on the fibre, a law of fibre averages
and a reference value `ψ₀`.  Let an instance have that law and that `ψ₀`, places `t₀(a) ∈ [lo, hi]` and the same
rung positions `(α_l, β_l)`, `l ≥ 1`, for all points, and suppose the shift `c(t₀) = max_l min(b − A_l, B_l)` takes
one value on `[lo, hi]` — for "top" this is `lo ≥ b`; for "bottom", `x₀ − hi ≥ b` and `x₁ ≥ b`.  Then
(i) on every outer sample the instance has the same HIGH counts, sample sizes and stopping level as any other
such instance, in particular the product one;
(ii) on every outer sample, `calls_{l+1} ≤ #{i : i ≤ max{M_j : j ≤ j_stop, s_j ∈ Win_l(W(a_i))}}` with
`Win_l(w) = [w e^{b − min(hi, α₁…α_l)}, w e^{min(x₀ − lo, β₁…β_l)})`;
(iii) in the mean run, calls and cost are at most those of the mean run with `A₀ = hi`, `B₀ = x₀ − lo`;
(iv) the right-hand side of (iii) is attained by the joint law that gives every atom its dearest place; if that
place is the same `t` for the atoms that carry the calls, it is the mean-run cost of "every fibre at `t`, reference
value `ψ₀`" — and a *product* instance realises that up to shells of negligible probability, by moving the
reference point to such a shell and letting the outer profile ramp to it with slope `u`.

*Proof.*  (i) the classification of a point is `W > s e^{−c}` (§2.1), so it is a function of the sampled `W`'s.
(ii) `A_l = min(t₀, α₁…α_l) ≤ min(hi, α₁…α_l)` and `B_l ≤ min(x₀ − lo, β₁…β_l)`, so the point's window is inside
`Win_l`; then the formula of §2.1.  (iii) the mean run replaces the sample by the law and (ii) holds atom by atom;
`1 + max_j M_j` is the same on both sides and `C_l ≥ 0`.  (iv) first part: the maximum over places is taken atom
by atom.  Second part: a product instance with every fibre at `t` has `c_in′ = t − un_i`; choose its profile `F′`
so that `ln W′(d) + ψ₀′` equals the given `ln W(d) + ψ₀` wherever `F′` is not constrained, and `F′(d₁) = ψ₀′` at the
reference shell `d₁`; the maximum (or minimum) of the unconstrained profile and a cone of slope `u` with apex at
`d₁` is `u`-Lipschitz and differs from it only near `d₁`.  ∎

(iv) is what M1 rests on; its two parts are verified with their reference evaluator in §3.7.

### Critical

None.

### Major

**M1.  The reading of the second table of §4 (M l.337–342), the row of §0 (M l.26) and the title (M l.15): "no
such instance costs more than the worst product instance found", "by an amount that is a bound and not the cost
of an instance" — false; the excess is the cost of product instances that the first search did not find.**

*What decides it* (`logs/cell_v2_*.log`; `r18_cell.py`; their reference through the adapter, and my evaluator,
which agree to the 6 decimals printed; in every run their `Run.violations()` is empty).  The six cells of table
`anyplacement` with an excess above `0.001·na`:

| `(u, n, φ)`, behaviour | worst product instance found, job M-008 | bound searched, job M-014 | a product instance, and its `ln cost` |
|---|---|---|---|
| (2, 250, 0.85), top | 125.373236 | 127.016745 | **127.016745** — every fibre at `lo`, the law of the M-014 maximiser, reference point in the antipodal shell `d₁ = 212` (one shell changed, probability `2^{−212}`), monotone profile, slopes in `[0, u]` |
| (2, 350, 0.85), bottom | 161.175052 | 161.951637 | **161.951637** — same construction, `d₁ = 297` (54 shells changed, probability `e^{−69.1}`), monotone |
| (0.5, 250, 0.50), bottom | 37.751829 | 37.797269 | **37.797269** — the stored M-014 maximiser itself, decoded by their `Family.decode` as a product instance of their own family (monotone, 8 knots) |
| (0.5, 350, 0.50), bottom | 40.706118 | 40.735971 | **40.735971** — as the previous row |
| (0.5, 350, 0.55), bottom | 40.083311 | 40.099500 | **40.099500** — as the previous row |
| (0.5, 500, 0.35), bottom | 46.909303 | 46.929972 | **46.929972** — as the previous row |

In the first cell an *actual* `ψ` that is not a product (cone fibres whose slope varies with the outer shell,
`u`-Lipschitz on every edge, fibre averages recomputed from `ψ`) also costs `127.016745`; so does, in their
reference, the law of the M-014 maximiser with every fibre at `lo`.

Over the grid that their reference can reach (`r18_cell0.py`: every stored M-014 maximiser taken as the product
instance it decodes to — their decoder, their evaluator; `logs/cell0_n250_to_2000.log`, `logs/cell0_n4000.log`,
`logs/cell0_n8000_u0.5.log`): 300 cells (`n ≤ 4000`, and `n = 8000` for `u = ½`).  Such a product instance costs
more than the worst product instance found by job M-008 in **33 cells** (13 by more than `10⁻⁴·na`, 4 by more
than `10⁻³·na`, largest `+0.00600·na`); no run violates a claim of the theorem.  The table `anyplacement` has 15
cells (of 360) in which the searched bound exceeds the product search by more than `10⁻⁴·na`; all 15 are among
these 300; 13 are accounted for in this way to `10⁻⁶·na`, and the other two are the `u = 2` rows above.  **So
every excess of the bound above `10⁻⁴·na` in their table is the cost of a product instance.**
The stored values of job M-008 at `n = 250, 350, 500` are reproduced by the present code (my re-run: 144 of 144
each), so the tie rule is not the cause.  Conversely the bound search ends *below* the product search by more than
`10⁻⁴·na` in 18 of the 360 cells (down to `−0.0054·na`): at the small sizes the two searches differ by about
`±0.005·na` in both directions, and by `+0.020·na` in one cell.

*Why.*  In their family the place of the fibres and the position of the law relative to the reference value are
one parameter (`t₀ = un_i + c_in`, `ln W = c_in − F`, `ψ₀ = F(d₀)`).  The bound search cuts that tie — the windows
no longer depend on `c_in` — and thereby explores laws the product search reaches only through the outer profile
near the reference point.  A product instance can cut the tie too (Proposition R18.1 (iv)): a ramp of slope `u` to
a reference point in a shell of negligible probability.  In the four `u = ½` cells not even that is needed: at the law the
bound search found, the product instance costs the bound, and the product search with the same family and budget
had simply stopped lower.

*Consequences.*  (a) The sentence of M l.339–340 and the row of M l.26 are false as worded; the true statement is
stronger in one direction (in every cell examined the bound is reached by a product instance: no difference
between products and the rest is visible) and weaker in another (the product search of ENG-RES-0008 is not
converged at `n ≤ 500`: shortfalls of `0.0014`–`0.0201·na` in these six cells).  (b) The "worst instance found"
entries of ENG-RES-0008 at `n = 250, 350, 500` are lower bounds that their own second file already exceeds; their
table `anyplacement_minimax` (the headline rises in 5 of 30 pairs, by at most `0.0015·na`) is then a correction
of ENG-RES-0008, not a statement about instances that are not products.  (c) The convergence controls (job M-010
at `n = 1000, 16 000`; job M-013 at `n = 64 000, 128 000`) did not include the sizes where this shows.
(d) Nothing here touches Theorem 11.56: every cost is below `C_max`.

*Replacement text* (for M l.337–344; the row of §0 and the title to follow it):

> **Reading.**  Leaving the product family does not raise the worst case found; the product search of
> ENG-RES-0008, however, was not converged at the three smallest sizes.  At the stored worst laws the bound
> coincides with the cost of the product instance.  Searched directly, the bound exceeds the worst product
> instance found by job M-008 by more than `0.001·na` in six cells (`n = 250, 350, 500`), by at most `0.020·na`.
> In each of them the excess is the cost of a product instance: for `u = ½` the stored maximiser of the bound,
> taken as the product instance it decodes to, costs the bound; for `u = 2`, `φ = 0.85` a monotone radial
> profile with every fibre at the lowest place and the reference point in the antipodal shell does
> (`ln cost = 127.016745` against `125.373236` at `n = 250`).  The table therefore measures the shortfall of the
> first search — and its negative entries the shortfall of the second — not a difference between products and
> other instances.  [Science division, SCI-REV on ENG-RES-0014 §4, finding M1.]

and for the row of §0: "**bounded, and the bound is reached by product instances** — in the mean run, with either
uniform inner behaviour, no such instance costs more than the placement-free bound; where the searched bound lies
above the product search (at most `0.020·na`, `n ≤ 500`) a product instance costs the bound".

### Minor

**m1.  "Bottom gives `c = b` … as long as `t₀ ≥ b` and `x₀ − t₀ ≥ b`" (M l.45–46; the same in `meanrun.py` l.30) needs
`x₁ ≥ b`.**  From §2.1, `c_bottom = max{min(b−t₀, x₀−t₀), min(b, x₁, x₀−t₀)}` and `c_top = max{0, min(b−t₀, x₀−t₀)}`
(wrong in 0 of 400 000 random cases).  Theorem 11.56 asks for `x_L ≤ b` only; with every inner accuracy below the
tolerance, "bottom" gives `c = x₁ < b` inside the stated range: 100 000 of 100 000 cases, and 139 144 of 3 396 825
literal decisions contradict `c = b` (none the exact rule) — points of `(s e^{−b}, s e^{−x₁}]` are LOW.  Every X-005
design ends its ladder with `x_L = b` (`run_search.design_params`, l.55), so nothing published is touched.  Also,
each behaviour needs only one of the two conditions.
*Replacement:* "'Bottom' gives `c = b` as long as `x₀ − t₀ ≥ b` and some inner accuracy is at least `b` (in every
design used the last one is `b` itself); 'top' gives `c = 0` as long as `t₀ ≥ b`.  In general
`c_bottom = max{min(b−t₀, x₀−t₀), min(b, x₁, x₀−t₀)}`, `c_top = max{0, min(b−t₀, x₀−t₀)}`."

**m2.  The argument for the rule (M l.40–43) is written for a point that starts at rung 0.**  A point meets a level
at the rung where lower levels left it; that the rungs below do not matter needs "levels are visited in increasing
order" (§2.1, third case).  The hypothesis is really used: with the same loop and the levels visited in
*decreasing* order the rule fails in 30 017 of 2 016 504 decisions (control `descend`).
*Replacement, after "LOW at the first rung with `U ≤ s`":* "(first from the rung at which earlier levels left the
point; the rungs below it were passed at lower levels, where `L ≤ s′e^{−b}` with `s′ < s`, so they cannot make it
HIGH now).  Since `B_l` decreases in `l`, …".

**m3.  "Its classification shift `c` is the same" (M l.292–293) holds only under the range condition, and
`rung_positions` with a pair has no guard.**  `c_top(t₀) = 0` needs `t₀ ≥ b` for every fibre, i.e. `lo ≥ b`;
`c_bottom(t₀) = b` needs `x₀ − hi ≥ b` (and `x₁ ≥ b`).  True in all 468 cells (1.12).  Outside, the pair mode takes
its shift from `A₀ = hi`, `B₀ = x₀ − lo` (`meanrun.py` l.254–263), which is the shift of no fibre, and what it
returns is not an upper bound: with their reference, over 300 designs with `lo < b` or `x₀ − hi < b`, a product
instance costs more than the pair mode returns for its own law in 16 of 600 cases, by up to `e^{6.83}`
(`u = 1`, `n = 44`, `n_o = 42`, `n_i = 2`, `λ = 0.2`, `η = ¼`, `η′ = 0.1`, `θ = 2`, `ν₁ = 1`, `b = 2.5`, ladder
`(4, 2.875, 2.5)`, cone of slope `u` to radius 35 then flat, reference at `d₀` with `F = 2`, "top", every fibre at
`t₀ = lo = 1.2402`: `ln cost = 16.5121` against `9.6776`; `logs/corner_part2b_seed18_300.log`,
`data_corner_example_their_reference.json`).  No design used is in that corner; the function's docstring
(`meanrun.py` l.232–236, `ckernel.py` l.102–104, `adversary.py` l.170–172) states the bound without the condition,
and there is no unit test of `t0_range` in `tests/eng/`.
*Replacement for M l.292–293:* "With either uniform inner behaviour, and because `lo ≥ b` and `x₀ − hi ≥ b` in
every cell (by at least 10.1 and 7.8), its classification shift `c` is the same for all fibres and equal to the
product instance's, …".  *For the code:* in `rung_positions`, for a pair, compute the shift at `lo` and at `hi`
and raise if they differ.

**m4.  "An upper bound on the evaluations of every instance with that law" (M l.301–302): of the *mean-run*
evaluations, of every instance with that law *and that reference value*.**  The mean run is not the expectation
of the literal run: on 18 small cases at the theorem's `K` the mean over 100 literal runs of the calls of `I₁`
differs from the mean run by up to 28 %, single literal runs exceed the mean-run bound at some rung in 1 130 of
1 800 runs, by up to a factor 1.50, and in one case the *mean* of the literal calls (`3.1585·10⁸`) is above the
mean-run bound (`2.5128·10⁸`) (`logs/literal_seed18_100.log`).  What does hold for every sample is (ii) of
Proposition R18.1 — 0 violations in the same 1 800 runs.
*Replacement:* "… counts at least as many calls at every rung as the mean run of any such instance: an upper
bound on the mean-run evaluations of every instance with that law of fibre averages and that reference value,
product or not".

**m5.  Notation of the union window (M l.298).**  `min(hi, α_l)` and `min(x₀ − lo, β_l)` must be read with the
running minima `min(hi, α₁, …, α_l)`, `min(x₀ − lo, β₁, …, β_l)` (what the code does); for "bottom" and "top" they
coincide because the ladder decreases.

**m6.  The reproduction command of §1 no longer gives the table.**  `recheck_classification.py` has the default
job list `cost claims converge converge2` (l.34); the four result files hold 2 672 stored maximisers; the table
and the stored `x005_recheck_classification.json` have 2 624 (the first three jobs).  With
`--jobs cost claims converge` the count is the table's.

**m7.  What the first table shows.**  "In a corner: 0; cost changed by the exact rule: 0; claims violated: 0" are
consequences of the inequality 1.12 for *every* instance of the family; the stored maximisers add nothing to
them.  What the table does test is that the generalised code reproduces the stored values.  The unit test
`test_the_search_family_cannot_reach_the_corners…` (`test_twolevel.py` l.495–507) checks `φ ∈ {0.2, 0.5, 0.8}`,
not the extreme cell `φ = 0.85`.  *Suggested sentence:* "for every cell of X-005, `lo − b ≥ 10.17` and
`x₀ − hi − b ≥ 7.82` (the smallest at `u = ½`, `n = 250`, `φ = 0.85`), so the two rules are the same function on
the whole search family".

**m8.  The Python reference cannot serve as a reference at the larger sizes.**  `_range_max` (`meanrun.py`
l.208–218) caches one array of length `j_stop + 1` per distinct window length, "for index arrays … with few
distinct lengths"; the windows clipped at `j_stop` have one length per atom, so the memory is about
`(n_o + 1)(j_stop + 1)·8` bytes when the windows of one rung are clipped: 6.46 GB measured at `u = 1`, `n = 16 000`,
`φ = 0.5` (computed: 8001 × 99 579 × 8 B = 6.37 GB; the two other candidate causes, the tables and the imports, are
0.2 MB and 60 MB), 1.69 GB for the chunk `n = 4000`, `u = 2`.  A sparse table of range maxima needs
`O(j_stop log j_stop)`.

**m9.  One tolerance is part of the definition of their mean run.**  A pass is "populated" when
`m ≥ −log₂ P(HIGH) − 10⁻¹²` (`meanrun.py` l.304), i.e. `2^m P(HIGH) ≥ 1 − 6.93·10⁻¹³`, where the mean count gives
`N ≥ K` only for `2^m P(HIGH) ≥ 1`.  With `n_o ≥ 41` the extreme shell has probability below that tolerance.  Against
`N ≥ K` exactly: sample sizes change at 4 513 levels in 154 of 600 runs, `ln cost` by at most `0.0345`.  Neither
reading is "the" mean run (a literal run has `N = K` there with probability `(1−ε)^K`); "exact for the mean run"
(ENG-RES-0008 §1) holds with this convention stated.

**m10.  The list of what §4 does not cover (M l.346–349, l.408) lacks three items.**  (a) Inner costs that depend
on the fibre: in an instance that is not a product the fibres differ, and with an adaptive inner procedure the
cost of a call differs with them — by up to `e^{857}` in §3 of the same message; the bound needs `C_l` to be a
supremum.  (b) The design: in every X-005 cell `x₁ ≤ min(lo, x₀ − hi)` (smallest margin 5.03; `logs/cells.log`),
so the place changes the calls of `I₁` only — which is why the first table is flat; in random designs the union
changes deeper rungs too (16 of 240 cases).  (c) Uniformity is not only "not covered": it is needed (§5).

### Observations (no change requested)

* **O1.**  The mechanism behind the costs of M1: under "top" with the fibres at `lo`, the trivial bracket reaches
  `x₀ − lo = n_i(u + Λ₁)` above `W`, so at the levels with the largest samples nearly every sampled point needs one
  call of `I₁` (`1.809·10⁵⁰` calls against a largest sample of `K·2^{153} = 26 153·2^{153} ≈ 3.0·10⁵⁰` at `(2, 250, 0.85)`); the cost
  is then `≈ M_max·C₁`.
* **O2.**  The input of the corner example (flat law, `ψ₀ = 0`, place given independently) is not an instance: a
  flat `ψ` has `ψ(a,0) = ψ₀` for every fibre, hence `ln W = t₀ − un_i − ψ₀`.  On consistent instances the conclusion
  is the same (§3.6).
* **O3.**  The rule needs neither valid brackets nor `α_l + β_l ≤ x_l` below the last rung (§2.1; block E).
* **O4.**  My evaluator and their stored values agree to `≤ 2.8·10⁻¹⁴` on the bound in the six cells of M1 and to
  `≤ 1.1·10⁻¹³` on the flat instance at `n = 8000` (§3.9) — a replication of the kernel's output at published sizes,
  by code written from the statements.
* **O5.**  At a law, an instance that is not a product can cost much more than the product instance *with that
  law*: calls of `I₁` up to ×4.1 for an actual `ψ` at `u = 2`, `n_o = 24`, `n_i = 4` (§3.4), `e^{10.8}` in cost at
  the law of the M-014 maximiser of `(2, 250, 0.85)`.  The comparison that matters is with the worst product
  instance over *all* laws, and there M1 applies.

---

## 3. The replication (own code), with what agreed and what did not

All scripts are in `experiments/science/ws_R18/`; every log named below reached its last line (which prints the
peak RSS).  Longest run: 436 s.  Runs of my own code alone stay below 100 MB; the runs that also call their
reference go up to 1.7 GB (under the 2 GB limit).

### 3.1 The rule and the window against a literal loop — `r18_rule.py` → `logs/rule_seed18_n100000_v3.log` (79 s)

A literal loop written from the sentence of KR l.224–227 (forty lines), integers in units of 1/4 ("coarse": ties
are frequent) and 1/64 ("fine"), so that every comparison is exact.  Random ladders (`L ≤ 5`, `x_L = b` in half of
the cases and `x_L < b` in the others), `b ∈ {½, 1, 3⁄2, 2}`, `λ ∈ {¼, …, 1}`, places over the whole of `[0, x₀]`
with both corners over-sampled, four behaviours (bottom, top, centre, any admissible pair — also narrower than
`x_l` — drawn independently for every point), the point present at an arbitrary subset of the increasing levels
with its bracket kept.

| what | result |
|---|---|
| rule `HIGH ⇔ W > s e^{−c}` | 15 191 163 literal decisions, **0 violations**; 156 789 of them exactly on the threshold |
| a point left unclassified; `c` outside `[0, b]` | 0; 0 |
| window: the first level at which rung `l+1` is called is the first present level with `W e^{b−A_l} ≤ s < W e^{B_l}` | 2 400 374 checks, **0 violations** |
| my closed forms for bottom and top (m1) | wrong in 0 of 400 000 |
| **controls** (each must fail) | `min`/`max` exchanged: 50 105 decisions wrong; tie given to HIGH: 156 789; rule without the running minimum: 174 447; window strictness exchanged: 360 035; old convention (`c = b` / `c = 0`) outside its range: 210 177 of 6 220 655; ladder with `x_L > b`: 21 951 points unclassified; an algorithm that does not intersect: 11 865 of 2 029 533; levels in decreasing order: 30 017 of 2 016 504 |
| block D ("bottom", inside the stated range, `x₁ < b`) | `c = x₁ < b` in 100 000 of 100 000; 139 144 of 3 396 825 decisions contradict `c = b` |
| block E: intermediate rungs wider than `x_l`; positions of either sign | 0 violations in 2 024 645 and 2 028 918 decisions (the rule does not need these hypotheses) |

### 3.2 My mean run against their Python reference — `r18_mean.py`, `r18_xcheck.py` → `logs/xcheck_seed1_150.log` (104 s)

`r18_mean.py` is a mean run written from KR §2.1–2.2 and from the definition in ENG-RES-0008 §1: probabilities
are integers over a common denominator, "populated", the Harper radius and the closing radius are integer
comparisons, every logarithm compared with a level is a `Fraction`, magnitudes are 50-digit numbers; an instance
is a list of atoms (ln W, weight, place, positions) and the shift is computed per atom.  Against their
`meanrun.mean_run` on 150 random designs (`u ∈ {½, 1, 2}`, `n ≤ 240`, ladders ending at `b` or below), two radial
laws each:

| runs compared | number | mismatches |
|---|---|---|
| bottom, top (feasible place) | 600 | 0 |
| explicit positions (a share of every rung; random admissible pairs) | 300 | 0 |
| a place in a corner of `[0, x₀]` | 600 | 0 |
| old convention (theirs `legacy_classification`, mine a forced shift) | 600 | 0 |
| their pair mode (mine: union of windows) | 600 | 0 |
| constants `J, K, r†, m_max` | 150 designs | 0 |

Compared in every run: status, stopping level, closing radius, the sample size of every level (1 057 582 levels),
`ln calls` of every rung, `ln cost`, `ln C_max`.  Controls: the old convention at a corner place where the exact
shift differs changes their reference's run in 257 of 301 cases; with `lo` and `hi` exchanged the "bound" falls
below the product instance in 243 of 600 runs (the union: 0 of 600).

**What did not agree at first, and why.**  Before one convention of theirs was reproduced, 36 of the first 108
runs differed in the sample size of one or two levels.  Candidate causes and their sizes: (a) their "populated"
test has the tolerance of m9 — with it put into my run every mismatch disappears (36 of 36; then 0 of 2 700);
(b) an error of my loop — would not disappear by changing one threshold; (c) rounding of `ln s_j` — the instances
are on rational grids, mine are exact and theirs use a tie rule of `10⁻⁹`: nothing left to explain.  So (a).

### 3.3 Instances that are not products, mean runs — `r18_nonproduct.py main` → `logs/nonproduct_main_seed5_120.log` (140 s)

120 designs (every fourth the X-005 design at `n ∈ {60, 100, 150, 250}`, the others random), radial laws, both
behaviours, and for each seven placements: two places and three places correlated with `W` in both directions;
every shell split 1:2 between `lo` and `hi`; a random place per shell; for every atom the dearest of 17 places.

| | result |
|---|---|
| instances that are not products | 1 680 (946 694 levels) |
| (a) sample size of some level different from the product instance with the same law | **0** |
| (c) calls of a rung above the bound `A₀ = hi`, `B₀ = x₀ − lo` | **0 of 14 168** rung checks; cost above the bound's: 0; bound below the product instance: 0 |
| **control**, `lo` and `hi` exchanged | exceeded in 1 661 rung checks, in 678 of the 1 680 instances |
| attainment | every one of the seven patterns reaches 100.0000 % of the bound's calls at some rung in some case |
| the union changes the calls of a rung beyond the first | in 16 of 240 (design, behaviour) pairs — by the inequality of m10 (b) none of them can be an X-005 design |

(The inner costs in this script are a model, `ln C_l = 2 + 3l`: inputs.  The statements above are about calls.)

### 3.4 An actual `ψ` that is not a product — `r18_nonproduct.py explicit` → `logs/nonproduct_explicit.log`

`ψ(a, b) = F(|a|) + σ(|a|)·u·|b|` with `σ` going from `+1` to `−1` by `1/(2n_i)` per outer shell and `F = 0` (then the
fibre average rises with the place) or `F = u|a|` (it falls); `u`-Lipschitz on every edge (all `(|a|, |b|)`
transitions checked); fibre averages from the closed form, checked against the sum over the fibre; places sweep
the whole of `[lo, hi]`.  Three sizes, two correlations, two behaviours: in 12 of 12 cases one shift for all
fibres, sample sizes equal to the product instance's, the bound holds, the control is violated.  The instance
makes more calls of `I₁` than the product instance with its law in 7 cases (up to ×4.1: `7.30·10⁷` against
`1.78·10⁷`), attains the bound in 2 of them (`u = 2`, `F = 0`, both behaviours) and comes within 0.2 % of it in a
third (`2.510·10⁸` of `2.513·10⁸`).

### 3.5 Literal runs on instances that are not products — `r18_literal.py` → `logs/literal_seed18_100.log` (436 s)

`r6lib` (our division's literal engine: the loop as written, exact sampling, the theorem's `K = 855…927`), 18
cases — the two families of §3.4 and a "simulated" instance with two places (`hi` for the upper half of the law of
`W`, `lo` for the lower), three sizes, both behaviours — 100 runs each, and on the same outer sample the product
instance with the same law.

| | result (1 800 literal runs, all closed) |
|---|---|
| identity: calls of every rung `=` the count over the point's own windows with the realised sample sizes | **0 violations** |
| union window, realised sample sizes (Proposition R18.1 (ii)) | **0 violations** |
| **control**, `lo` and `hi` exchanged | exceeded in 1 800 of 1 800 |
| sample sizes and HIGH counts of every level identical to the product instance on the same sample | 1 800 of 1 800 |
| stopping level and largest sample equal to the mean run's | 100 of 100 in 17 cases, 68 of 100 in one |
| mean literal calls against the mean run | within 2 % at every rung in 12 cases; up to 28 % apart in the other six (five of them at `u = 2`) |
| single literal runs above the *mean-run* bound at some rung | 1 130 of 1 800, by up to ×1.50 |

### 3.6 The corners — `r18_corner.py` → `logs/corner_part1_seed18_30.log` (212 s), `logs/corner_part2b_seed18_300.log` (17 s)

*Part 1 (the control the brief asks for: the old convention outside its range).*  Design of their sampled runs
(`b = ½`, `η = ¼`, `η′ = θ = 0.1`; `λ = ½` and `λ = 1⁄5`), three sizes, "top" with `t₀ ∈ {⅛, ¼}` and "bottom" with
`x₀ − t₀ = ¼`.  (A) On their kind of input the exact rule and the old convention differ by `4.1744` in `ln cost`
under "top" (12 of 12 rows; under "bottom" the two costs coincide there, 6 rows) — the "`e^{4.2}`" of the
message — in my code and in their reference alike (18 of 18 rows equal).  (B) On 36
consistent instances (flat; outer cone of slope `u/2`), 30 literal runs each: the two mean runs differ on 26;
where they stop at different levels (25 instances, 750 literal runs) the literal run stops at the exact rule's
level in **750** and at the old convention's in **0**; where the two costs differ by more than 0.05 (13
instances) the mean literal `ln(queries)` is the exact rule's side in 13.

*Part 2 (m3).*  Numbers in m3.  `r18_nonproduct.py corner` (`logs/nonproduct_corner_seed5_40.log`, own evaluator,
model costs): the shift depends on the place in 63 of 80 cases, and for one and the same law the sample sizes
differ between "all fibres at `lo`" and "all at `hi`" in the same 63.

### 3.7 Their six cells — `r18_cell.py` → `logs/cell_v2_*.log`; `r18_cell0.py` → `logs/cell0_*.log`

Inputs taken from their files as data: the stored maximiser of the bound (decoded by their `Family.decode`), the
stored worst product value, their inner costs.  Per cell: (0) their reference on the maximiser as the product
instance it decodes to; (1) my mean run at that law — the bound equals their stored value to `0 … 2.8·10⁻¹⁴` in all
six cells; (2) the dearest place per shell — in all six a single place for every shell but the reference one;
(3) an actual `ψ` with cone fibres following (2) as far as Lipschitz continuity allows; (4) the product instance
of Proposition R18.1 (iv), with the reference shell chosen to change the least probability; (5) (4) again with
their reference.  Results: the table of M1.  In the cell `(2, 250, 0.85)` the `ψ` of (3) differs from a product
only near the reference shell and costs the bound; in `(2, 350, 0.85)` the reference shell of the maximiser lies
in the bulk, the radial `ψ` of (3) reaches only `152.18`, and it is the product instance of (4) — reference point
moved to the antipodal shell — that costs `161.951637`.

### 3.8 Behaviours that differ from shell to shell — `r18_mixed.py --costs theirs` → `logs/mixed_theirs_b.log` (99 s)

X-005 design at `n = 100` with their inner costs (`alg2l.inner_costs`, used as a table); the same law and
reference value; "bottom" on some shells and "top" on the others (thresholds on `W`, then coordinate ascent).
Target: the larger of the two uniform placement-free bounds.

| law | placement-free bound, uniform bottom / top | best shell-dependent behaviour found | excess over the larger bound |
|---|---|---|---|
| `u = 1`, `φ = 0.5`, flat | 44.483875 / 36.906359 | 45.044595 ("top" on 7 of 51 shells; largest sample `K·2^{10}` instead of `K·2^{9}`) | **+0.5607** |
| `u = ½`, `φ = 0.5`, flat | 31.796049 / 27.448322 | 32.266218 ("top" on 9 of 51 shells; `K·2^{8}` instead of `K·2^{7}`) | **+0.4702** |
| `u = 1`, `φ = 0.7`, cone | 46.654630 / 46.654610 | 46.654641 | +0.000011 |
| `u = 2`, `φ = 0.5`, flat | 57.840590 / 47.374478 | 57.840590 | 0 (within `10⁻⁶`) |
| `u = 1`, `φ = 0.3`, plateau then cone | 47.797876 / 41.810420 | 47.797876 | 0 (within `10⁻⁶`) |

(`logs/mixed_theirs_a.log`, an earlier run of three cases, has the first row and two cases without excess; its
word "EXCEEDED" on a difference below `10⁻⁶` is a printing threshold, corrected in the script.)

### 3.9 Ties, and the flat instance, at sizes of the published grid — `r18_ties_large.py`, `r18_flat_large.py`

*Ties* (`logs/ties_large_n1000_2000_4000.log`, 88 s).  X-005 design, `u = 1` (so `u/λ = 5`), `n = 1000, 2000, 4000`,
`φ = 0.5`, flat fibres (`c_in = 0`) and profiles on the level grid (flat; cone of slope `u` to `0.3n_o` or `0.4n_o`, then
flat): every fibre average lies exactly on a level, so under "top" every rung meets `U = s` and the threshold
meets `W = s` for every atom.  My exact mean run against their reference, which decides these cases with
tolerances (`10⁻⁹` in the logarithm; `10⁻¹²` in units of `λ` for the window indices, `meanrun.py` l.435–436):
18 runs, 220 463 levels, **0 mismatches** in sample sizes, calls of every rung and cost.

*The flat instance at `n = 8000`* (`logs/flat_large_n8000_umax1.log`, 124 s).  My exact mean run on the flat
instance against the flat-instance costs *stored* in `x005_cost.jsonl` (their kernel, job M-008), `φ = 0.5`,
`u = ½` and `u = 1`, both behaviours — a size their Python reference cannot reach for `u = 1` within 2 GB: 4 of 4
agree in stopping level, largest sample and `ln cost` (largest difference `1.1·10⁻¹³`); the constants
`J, K, r†, m_max` are equal in mine, theirs and the stored record.  (A fifth row, `u = 2` bottom, also agreed, in a
run stopped by its time limit before the sixth: not cited, §7.)

---

## 4. Re-runs (their code)

**How.**  `rerun_copy/` holds copies (`cp -p`, sha256 equal to `<ENG>`) of `src/metricchain_eng/twolevel/{alg2l,
meanrun, tables, adversary, sampling, simulate}.py`, of `experiments/eng/twolevel/{recheck_classification,
nonproduct_bound, run_search}.py` and of the four result files `x005_{cost, claims, converge, converge2}.jsonl`.
The C kernel source is not copied and nothing was compiled.  Both scripts import `ckernel.Evaluator`, which
builds the kernel; so `ckernel.py` is replaced by an **adapter of mine** (`r18_ckernel_adapter.py`, 71 lines)
with the same class and the same `run` signature, which calls *their* `meanrun.mean_run`; for `t0_range` it
substitutes the pair in the one call of `rung_positions` that `mean_run` makes — what their `ckernel.py` does
before calling the kernel (l.114).  Their two scripts run verbatim (`runpy`, `python3 -I -B`,
`RLIMIT_AS = 2 GB`), one piece (job, `n`[, `u`]) at a time from directories that hold only that piece's lines of
the result file (`r18_make_chunks.py`, `r18_run_chunk.py`).  29 pieces, every log ends with `exit=0`; longest
piece 391 s; largest peak RSS 1 692 MB.

**What could be re-run.**  Their reference needs about `(n_o + 1)(j_stop + 1)·8` bytes (m8): within 2 GB that is
`n ≤ 4000` for all slopes and `n = 8000` for `u = ½`.  Not re-run: `n = 8000` with `u = 1, 2` and every `n ≥ 16 000`.

**`recheck_classification`** (`logs/compare_rerun_final.log`):

| | re-run | their stored file / the table of the message |
|---|---|---|
| searches | 1 536 (cost 1 200, claims 320, converge 16) | 2 624 |
| in a corner of the rule | 0 | 0 |
| cost changed by the exact rule | 0 | 0 |
| claims violated under the exact rule | 0 | 0 |
| old convention reproduces the stored value | 1 535 of 1 536 | 2 615 of 2 624 |
| cells against their stored per-cell values (304 cells) | `stored_worst`: difference 0; `exact_worst`: `≤ 4.3·10⁻¹⁴` | |

The one value not reproduced (`u = ½`, `n = 1400`, `φ = 0.3`, general/top, a flat fibre, not the cell's worst
search): `+1.539·10⁻⁵` with the tie rule and **0 with `tie = 0`** (`logs/diag_cost_n1400.log`) — a change by the
tie rule, as the message says of its nine.  So one of the nine is at `n ≤ 4000` and eight are where I could not
re-run; "by at most 0.69" is therefore *read only*.

**`nonproduct_bound`**: 300 of 468 cells; `worst_product` and `worst_bound` within `4.3·10⁻¹⁴` of their stored
values, `max_gap` within `2.8·10⁻¹⁴`, bounds above `C_max`: 0 as theirs.  Of the table: the rows `u = ½` and `u = 1`
are reproduced in full (their maxima are at `n = 250, 350`); of the row `u = 2`, "`2.3e-13`; `1.7e-16`" (at
`n = 4000`, `φ = 0.75`) and "`0.026`" in units of `na` (at `n = 350`, `φ = 0.85`) are reproduced, and "`13`" (at
`n = 8000`, `φ = 0.85`) is *read only*.

**Also re-run:** their reference on 2 700 random runs of mine (§3.2), on the corner designs (§3.6), on the six
cells and on every stored M-014 maximiser at `n ≤ 4000` and at `n = 8000`, `u = ½` (§3.7), on 18 instances with
structural ties (§3.9).  **Not re-run:** `python -m pytest tests/eng`
(needs the kernel), `make_tables.py --verify`, the Modal jobs, `simulate.py`.

---

## 5. Item 3 — what the two sections do and do not show; the assumptions, classified

**What a reader may conclude.**  From §1: the rule by which the evaluator decides HIGH and LOW is the algorithm's
own, for any uniform positions and any place, and no number published for X-005 depends on the earlier
convention.  From §4, *with the corrections of M1*: in the mean run, with either uniform inner behaviour and the
X-005 design, the number of evaluations of any instance — product or not, whatever the places of its fibres — is
at most the placement-free bound of its law and reference value; and in every cell where that bound was found
above the product search, a product instance attains it.  So, at the level of these searches, instances that
are not products do not raise the worst case.

**What a reader may not conclude.**  (1) That the worst case of ENG-RES-0008 at `n ≤ 500` is known to the third
decimal: its search stopped up to `0.020·na` short, and the only convergence controls are at larger sizes.
(2) Anything about inner behaviours that differ from fibre to fibre — the case an instance that is not a
product actually presents to real inner procedures: §3 of the same message shows that the base bracket's
answer sits at different positions on fibres of different shape (table `k0_answers`), and with behaviours
differing from shell to shell the cost exceeds both uniform bounds (§3.8).  (3) Anything about literal runs:
the bound is a number about mean runs, exceeded by single literal runs (and in one case by their mean) at the
theorem's `K`.  (4) Anything about inner costs that depend on the fibre (three levels), about designs whose first
inner accuracy exceeds `min(lo, x₀ − hi)`, about laws whose level sets are not balls (the inequality holds law
by law; which laws occur is the limit of the search), about `n ≥ 32 000` (not searched with the bound).

**Classification** (the six classes of the research owner's directive of 2026-11-26, letters as in
`docs/science/ASSUMPTION_AUDIT.md` §0: **E** essential, **T** needed by the proof or by the way the statement is
written, **C** convenience, **Q** replaceable by a quantitative condition, **X** changes the complexity when
removed, **F** makes the claim false when removed; evidence: **[P]** proved here, **[M]** measured here on
instances — with the run —, **[?]** not established.  A class **F** is given only with a counterexample that was
run here and a control).

*The rule of §1.*

| assumption as used | class | evidence |
|---|---|---|
| brackets are intersected and kept from level to level | **F** | [P] §2.1 uses `B_l` nonincreasing; [M] an algorithm without intersection violates the rule written with raw positions in 11 865 of 2 029 533 decisions; control: with intersection 0 of 15 191 163 |
| levels are visited in increasing order (not written in the message) | **F** | [P] §2.1, third case; [M] decreasing order: 30 017 of 2 016 504 decisions wrong |
| one bracket per (point, rung), whenever the call is made | **E** for the formula | [P] the positions `(α_l, β_l)` are not defined otherwise; a threshold in `s` still exists for any inner behaviour, because brackets only shrink (HIGH at `s` implies HIGH at every lower level met) — but it is not given by the formula.  No run |
| `x_L ≤ b` (exactly: `α_L + β_L ≤ b`) | **F** for "every point is classified" | [M] ladders with `x_L > b`: 21 951 points unclassified; control 0 |
| `α_l + β_l ≤ x_l` at the rungs below the last | **T** | [P] not used in §2.1 (it is used by the count of calls of the theorem, KR Step 8); [M] wider intermediate brackets: 0 violations in 2 024 645 decisions |
| valid brackets (`α_l, β_l ≥ 0`, `0 ≤ t₀ ≤ x₀`) | **T** for the rule, **E** for `0 ≤ c ≤ b` | [M] positions of either sign: 0 violations in 2 028 918 decisions, `c` outside `[0, b]` in 82 294 of 100 000 points |
| the same positions for all points ("uniform") | **T** for the rule; **Q** for the evaluator | [P] the rule is per point; [M] every point of §3.1 has its own positions.  The mean run needs only *one shift* for all points — weaker than one position — and in general the law of `ln W + c` |
| `t₀ ≥ b` ("top"), `x₀ − t₀ ≥ b` and `x₁ ≥ b` ("bottom"), for `c = 0` / `c = b` | **Q**, with **F** outside | [P] closed forms (m1); [M] old convention outside the range: 210 177 of 6 220 655 decisions wrong; `x₁ < b`: 139 144 wrong; `e^{4.17}` in cost (§3.6) |
| fibre `u`-Lipschitz on the cube, uniform reference measure, trivial bracket taken at the fibre's origin — for the range of `t₀` | **E** for the range | [P] 1.11; both ends attained.  For a non-uniform or non-product reference measure the range is another one: **[?]** |

*The bound of §4.*

| assumption as used | class | evidence |
|---|---|---|
| the same law of fibre averages **and the same reference value** | **E** (the second is implicit in the message) | [P] levels and the initial lower bound are functions of `ψ₀`; the statement compares at a fixed pair |
| uniform inner behaviour ("bottom" for all points, or "top" for all) | **F** | [M] §3.8: behaviour depending on the shell, same law and reference value: `+0.5607` and `+0.4702` in `ln cost` above the larger of the two uniform bounds (`n = 100`, flat laws, their inner costs); control: the two uniform runs equal their bounds.  Magnitude found: one doubling of the sample; how large it can be: **[?]** |
| the shift does not depend on the place: `lo ≥ b` ("top"), `x₀ − hi ≥ b` and `x₁ ≥ b` ("bottom") | **Q**; **F** outside, for the evaluator's pair mode | [M] all 468 cells inside (margins ≥ 7.8); outside: a product instance at `e^{6.83}` times the "bound" (m3; their reference and mine) |
| counts replaced by their means | **T** for the inequality; **F** if the number is read for literal runs | [P] Proposition R18.1 (ii) is pointwise in the sample; [M] 0 violations in 1 800 literal runs with realised sizes; 1 130 of the same runs above the mean-run number, by up to ×1.50 |
| inner costs `C_l` the same for every fibre | **C**, with **X** behind it | [P] with a cost that depends on the fibre the bound holds with `sup C_l`; then it is the price of the dearest fibre at every call — `e^{857}` between a cone and the flat fibre in §3 of the message (read only).  No run |
| level sets of the law are balls | **C** | [P] the inequality is atom by atom, for any law; it restricts which laws the *search* visits.  My runs use radial laws only |
| `[lo, hi]` the whole feasible range of a `u`-Lipschitz fibre | **E** for "every instance" | [P]; a smaller range gives a smaller bound |
| the X-005 ladder (`x₁ ≤ min(lo, x₀ − hi)`) — for the reading, not for the inequality | **X** (for the size of the effect) | [M] 468 of 468 cells: only the calls of `I₁` depend on the place; in random designs deeper rungs change in 16 of 240 cases and the bound is up to `e^{8.9}` above the product instance with the same law (model costs) |
| "the excess is a bound and not the cost of an instance" | **F** — it is false | [M] M1: six cells, their reference and mine |
| the product search is converged (needed to read the second table as a comparison of two classes) | **F** at `n ≤ 500` | [M] a product instance above the "worst found" in 33 of 300 cells, by up to `0.0201·na` |

---

## 6. Requests to the engineering division (can be sent as they stand; none is an authorisation)

**R18-ENG-1 (correction of ENG-RES-0014 §4, §0 and title; M1).**  Replace the Reading by the text of M1, the row of
§0 by the sentence given there, and "cannot cost more than the worst product instance" in the title accordingly.
To check with your kernel, without any search: (a) for every stored maximiser `s` of `x005_anyplacement.jsonl`
evaluate the product instance it decodes to, `ev.run(fam.instance(*fam.decode(s["best_x"])), s["oracle"])` — we
find, with your Python reference, `37.797269`, `40.735971`, `40.099500`, `46.929972` in the cells `(½, 250, 0.50)`,
`(½, 350, 0.50)`, `(½, 350, 0.55)`, `(½, 500, 0.35)`, against your "worst product instance found" `37.751829`,
`40.706118`, `40.083311`, `46.909303`; over the 300 cells we could reach (`n ≤ 4000`; `n = 8000` for `u = ½`) the product instance beats the
stored worst product value in 33.  (b) Evaluate the two product instances stored in
`experiments/science/ws_R18/data_cell_u2_n250_phi0.85.json` and `…_u2_n350_phi0.85.json` (key `product`: profile
`F`, `c_in`, reference shell `d1`, `psi0`; `Instance(radial_law(F, tables, shift=c_in), psi0=F[d1], t0=u·n_i+c_in)`,
oracle as stored): we find `127.016745` and `161.951637` with your reference, against `125.373236` and
`161.175052`.

**R18-ENG-2 (computation: the worst product instance at the small sizes).**  *Claim evaluated:* the columns "worst
instance found" of ENG-RES-0008 (tables `main_u*`, `phi_profile`, `trend`) at `n ∈ {250, 350, 500}`, and the
comparison of table `anyplacement`.  *Source:* engineering `1cc4e1c`; files `x005_cost.jsonl`,
`x005_anyplacement.jsonl`.  *Assumptions:* mean runs, uniform inner behaviours, the X-005 design.  *Method:*
(i) take, per cell, the maximum of the stored product values and of the product costs of the stored
bound-maximisers (no search; all 360 cells); (ii) repeat the product search at `n ≤ 500` with added starting
points — reference point in the shells `0` and `n_o` with a ramp of slope `±u` of length `|Δ|/u` for
`Δ ∈ {¼, ½, ¾, 1}·u n_i`, `c_in` at both ends of its range — and with the M-014 maximisers as seeds; (iii) seeds
2, 3 and three times the budget at `n ∈ {250, 350, 500}`, `φ ∈ {0.50, 0.85}`, as in job M-013.  *Baselines:* the
stored values.  *Correctness criteria:* every new maximum is at least the old one; `Run.violations()` empty; after
(ii) the product search and the bound search differ by less than `10⁻⁴·na` in every cell, or the cells where they
do not are listed with the dearest placement of the bound's maximiser.  *Expected outputs:* corrected tables;
the list of cells whose worst case moved and by how much.  *Resources:* (i) 1 440 kernel runs, under a minute by
your timing; (ii)–(iii) the cost of job M-008 at the three smallest sizes.  *Stopping:* when (iii) changes
nothing above `10⁻⁴·na`.

**R18-ENG-3 (text).**  m1, m2 (§1), m3, m4, m5 (§4), m7 (first table), m10 (limitations): replacement texts in §2.

**R18-ENG-4 (code and tests).**  (a) `rung_positions` with a pair: raise unless the shift is the same at `lo` and
at `hi` (m3); a unit test of `t0_range` — there is none: e.g. "for a law, the pair-mode value is at least the
cost with every fibre at any place of a grid in `[lo, hi]`", and the counterexample of m3 as the test of the guard.  (b)
`test_the_search_family_cannot_reach_the_corners…`: loop over every cell of the grid (the extreme one is
`φ = 0.85`).  (c) `_range_max`: a sparse table instead of one cached array per window length (m8) — as it is, the
"Python reference" cannot check the kernel beyond `n ≈ 8000` on a 15 GB machine.  (d) `recheck_classification.py`:
the job list of the table, or the table for the present default (m6).  (e) Say in the module text that
"populated" carries a tolerance of `10⁻¹²` in `log₂` (m9).

**R18-ENG-5 (offered, not requested).**  Our literal loop and mean run (`r18_rule.py`, `r18_mean.py`: exact
arithmetic, per-atom places and positions) are available as a third implementation for any further change of
the classification code; they agree with yours on everything compared so far.

---

## 7. What I did not check; my own errors; files

### Not checked

* The second table of §4 as a search (jobs M-014 on Modal): *read only*; its stored maximisers were re-evaluated.
  §5's table (`converge2`): not looked at.  §2 and §3 of the message (three levels): outside the brief.
* `n = 8000` (`u = 1, 2`) and all `n ≥ 16 000`: no re-run (memory of their reference).  My own evaluator was run on
  searched laws up to `n = 500`, on structured laws up to `n = 4000` and on the flat instance at `n = 8000` (§3.9);
  nothing of mine at `n ≥ 16 000`.  In particular the eight stored values changed by the tie rule ("by at most
  0.69") and the entry "13" of the first table of §4 are *read only*.
* The C kernel: never built, never run.  Agreement kernel = Python reference is their test (*read only*); what I
  compared is Python reference = stored kernel outputs (`≤ 4.3·10⁻¹⁴` on 304 + 300 cells).
* Their unit tests and `make_tables.py --verify`: not run (they need the kernel).  Their literal simulator
  `simulate.py`: read, not run; the literal runs here are `r6lib`'s.
* The cells of table `anyplacement` with an excess below `10⁻⁴·na` (345 of 360) were not examined one by one;
  the 60 cells at `n = 8000` (`u = 1, 2`) and `n = 16 000` were not re-evaluated (none of them has an excess above `10⁻⁴·na`).
* Whether a product instance attains the bound when the dearest placement is *not* one place for the bulk
  (Proposition R18.1 (iv), second part, assumes it): in all six cells it was one place; the general question
  — is the supremum over all instances larger than over products? — is **not settled** by this report.
* How large the excess of point-dependent behaviours can be (§3.8 found one doubling of the sample).
* Tie handling of their windows beyond `n = 4000`: the window indices use a tolerance of `10⁻¹²` in units of `λ`
  while levels carry rounding of about `10⁻¹¹` at `n ≥ 10⁵`.  Up to `n = 4000` no mismatch (§3.9); not tested above.
* No prior-art search (no network; the brief's structure replaces `COMMON.md`'s section on prior art).

### My own errors

* **E1.**  Two time stamps in `NOTES.md` were typed before the clock was read (16:30 for 16:10; 16:21 for 16:19);
  corrected on the spot; from then on the stamp is produced by the command that writes the entry.
* **E2.**  A planning run of their Python reference at `n = 16 000` without a memory guard peaked at 6 457.5 MB
  (limit of the brief: 2 GB), for under a minute.  Cause computed (m8).  Every later run of their code is under a
  2 GB address-space limit.
* **E3.**  First version of `r18_corner.py part1`: the mean run was fed `Fraction(float)` where the instance has an
  exact tie (`L = s e^{−b}`), so it stopped one level later than the literal runs (float(2.9) is `8.9·10⁻¹⁷` below
  2.9).  Corrected before any number of that version was used.
* **E4.**  Three compute processes for about 25 s (limit: two), when a 20-second diagnostic was started while two
  background runs were alive.  Nothing failed.
* Superseded or stopped runs, not cited, kept in `ws_R18/not_cited/`: the first version of `r18_corner.py part2`
  (it varied the place with the law held fixed — not a product instance of their family) and its example; a run
  of `r18_nonproduct.py corner 150 5` stopped by its 110 s timeout; the data files of the first version of
  `r18_cell.py` (its step (4) kept the reference shell); `r18_flat_large.py 8000` stopped by its time limit of
  1 150 s during its sixth row (five rows printed, all in agreement; my estimate of the cost at `u = 2` was wrong
  by a factor 4).  The logs `logs/cell_u*.log` are that first version's
  (complete; superseded by `logs/cell_v2_*.log`); `logs/rule_seed18_n100000.log` and `…_v2.log` are earlier
  versions of the rule test whose blocks are reproduced identically in `…_v3.log`.

### Files (all in `experiments/science/ws_R18/` unless a path is given)

| file | what |
|---|---|
| `NOTES.md` | running notes, with times, plans of the long runs, the errors |
| `r18_rule.py` | §3.1: literal loop against the rule and the window; controls; blocks D, E |
| `r18_mean.py` | my mean run (exact), per-atom places and positions; the union of windows |
| `r18_xcheck.py` | §3.2: my mean run against their Python reference |
| `r18_nonproduct.py` | §3.3 (`main`), §3.4 (`explicit`), `corner` |
| `r18_literal.py` | §3.5: literal runs (`r6lib`) on instances that are not products |
| `r18_corner.py` | §3.6: the old convention outside its range; the pair mode outside the range |
| `r18_cell.py`, `r18_cell0.py`, `r18_cell_sequence.sh` | §3.7: their cells; every stored bound-maximiser as a product instance |
| `r18_mixed.py` | §3.8: behaviours differing from shell to shell |
| `r18_cells.py` | the inequalities of 1.12 and m10 on all 468 cells |
| `r18_ties_large.py`, `r18_flat_large.py` | §3.9: structural ties at `n ≤ 4000`; the stored flat-instance costs at `n = 8000` |
| `r18_ckernel_adapter.py`, `r18_make_chunks.py`, `r18_run_chunk.py`, `r18_rerun_sequence.sh`, `r18_compare_rerun.py`, `r18_diag_n1400.py`, `r18_time_reference.py` | §4: the re-runs |
| `r18_debug1.py` | the diagnosis of the first mismatch of §3.2 (the tolerance of m9) |
| `.gitignore` | keeps `rerun_copy/` out of a commit |
| `data_cell_u*_n*_phi*.json`, `data_corner_example_their_reference.json` | the instances of M1 and m3 |
| `logs/` | every log cited (each ends with its peak RSS); `not_cited/`: see above |
| `rerun_copy/` | scratch copy of their files and the pieces of the re-run; not to be committed (`.gitignore` in `ws_R18/`) |
| `docs/science/workstreams/R18_REPORT.md` | this report |

### How to re-run (from `experiments/science/ws_R18/`, `OMP_NUM_THREADS=1`; times as measured)

```
python3 -I -B r18_rule.py 100000 18                      # §3.1, 79 s
python3 -I -B r18_nonproduct.py main 120 5               # §3.3, 140 s;  … explicit  # §3.4, 1 s
python3 -I -B r18_literal.py 100 18                      # §3.5, 436 s
# with the scratch copy of their files in rerun_copy/ (made as §4 describes), under `ulimit -v 2097152`:
python3 -I -B r18_xcheck.py 150 1                        # §3.2, 104 s
python3 -I -B r18_corner.py part1 30 18                  # §3.6, 212 s;  … part2 300 18   # 17 s
bash r18_cell_sequence.sh                                # §3.7, the six cells, 60 s in all
python3 -I -B r18_cell0.py 250 350 500 700 1000 1400 2000    # 200 s;  … 4000   # 287 s, 1.7 GB;  … --u 0.5 8000   # 103 s, 1.2 GB
python3 -I -B r18_mixed.py --costs theirs 100 1 0.5 flat 100 2 0.5 flat 100 1/2 0.5 flat 100 1 0.7 cone 100 1 0.3 plateau0.4   # §3.8, 99 s
python3 -I -B r18_ties_large.py 1000 2000 4000           # §3.9, 88 s;   python3 -I -B r18_flat_large.py --umax 1 8000   # 124 s
python3 -I -B r18_make_chunks.py; bash r18_rerun_sequence.sh recheck_classification:cost:cost_n250 …   # §4; then r18_compare_rerun.py
```

## Coordinator's note (2026-11-26, after the hand-back; the report above is the referee's, unchanged)

*What I did with this report.*  Read: §0, §1 (the statements), §2 in full (both proofs, the major finding, the
ten minor findings, the observations), §5 (what may and may not be concluded; the two assumption tables), §6
(the requests); §3, §4 and §7 at the level of their headings, tables and numbers.  **Checked:** (1) *the major
finding M1 in its largest cell* — `r18_cell.py 2 250 0.85` re-run by me under a 2 GB limit (9 s): the engineering
division's own reference evaluator, through the referee's adapter, returns `ln cost = 127.016745` for a product
instance (every fibre at the lowest place, the reference point in the antipodal shell, a monotone profile),
with an empty list of violated claims — the value of their searched bound, `1.6435 = 0.02005·na` above their "worst
product instance found" (`125.373236`); every line of my run equals the referee's log.  (2) *the rule of §1* —
`r18_rule.py` re-run with other points and another seed (31 337 points per regime, seed 30 000; 16 s): the rule
and the window hold on every decision, every control fails as it must.  (3) *the proof of the rule* (§2.1) read
line by line: the three cases for LOW (rungs at and after the one where the loop stops; rungs passed at this
level; rungs passed at earlier levels, where "levels increase" is used) are complete, and the termination at the
last rung needs `α_L + β_L ≤ b` only.  Both logs are in `ws_R18/logs/` (`…_by_coordinator.log`).  **Not checked by
me:** the other five cells of M1 and the 300-cell count (their logs read); Proposition R18.1 (iv), second part —
the construction of the product instance — beyond the one cell where it was run; the literal runs; the
re-runs of their two scripts; none of the referee's code line by line.

*Verdict.*  I accept the review, including M1.  Published as SCI-REV-0018.  The request R18-ENG-2 is in the
nine-field form the research owner's directive of 2026-11-26 asks for; it is a proposal and authorises nothing.

*Not in the repository:* `ws_R18/rerun_copy/` (18 MB: the engineering division's files), `ws_R18/not_cited/`.
