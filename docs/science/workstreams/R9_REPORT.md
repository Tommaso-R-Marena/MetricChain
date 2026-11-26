# Workstream R9 — second round: the five reviews as applied in the theory report at `658b77f`

*Science division, independent reviewer of workstream R9.  Written 25–26 November 2026.
Text reviewed: the read-only export of the theory tree at `658b77f` (below: **EXPORT**;
line numbers are those of `EXPORT/docs/THEORY_REPORT.md` unless another file is named),
against our reviews SCI-REV-0001, -0002, -0003, -0005, -0006 and the reports behind them.
Everything I wrote is in `experiments/science/ws_R9/` (`NOTES.md` is the step-by-step log,
including one false alarm of my own).  Vocabulary used throughout: **re-derived** (I did
the mathematics), **re-computed** (my own code), **re-ran** (someone else's code, named),
**read** (only read).*

## How far I got

All five items of the brief were done.  Item 1: every major finding read in the revised
text and re-derived; 38 of the 41 minor findings read where they were applied, 20 of them
checked by own derivation or own computation (at least a third per review; §1.6).  Item 2: all four amendments checked; (d) line by line.
Item 3: the `χ²` step and every error term of Theorem 11.97(c) re-derived and tested;
Proposition 11.69a re-derived; `Scattering.lean` and `TwoRoundsExpected.lean` read and
compiled from scratch copies; the diff of the adopted file taken.  Item 4: the sketch is
**proved**, in a stronger form, and checked exhaustively with own code (all bridges with
at most 22 beads; all 160 326 244 ordered pairs of clean bridges and all 350 026 681
ordered pairs of arbitrary bridges with at most 13 beads; random bridges of up to 3 970
beads); its consequences are worked out and the prediction is tested on R2's tables.
Item 5: the word-level diff `dcdfea6..658b77f` of the report was read for §§11.22, 11.24,
11.25, 11.26 (new text read in full) and for every changed hunk of §§0, 4.4, 6, 8, 9, 10,
11.6, 11.11, 11.14, 11.17, 12 and the README passages; not for §§11.27–11.29.

## Verdict table

| item | verdict |
|---|---|
| **1.** SCI-REV-0003 M1 (stopping rule, Theorem 11.84) | **applied correctly**; statement and proof re-derived, no new gap |
| **1.** SCI-REV-0001 M1 (headline of §11.25) | **applied in a different form, and the difference is justified** — their two amendments are right (item 2(a)) |
| **1.** SCI-REV-0001 M2 (Theorem 11.90(a), `e < 0`) | **applied correctly**; the repair as written is a complete proof; tested by own code |
| **1.** SCI-REV-0002 M1 (headline of §11.22) | **applied correctly**, in every place the review listed |
| **1.** SCI-REV-0002 M2 (`[116, 3 627]`; `1.56 ≤ vol 𝒦 ≤ 3.125`) | **applied correctly**; the four packings re-verified in exact rationals, both volumes re-computed |
| **1.** SCI-REV-0005 M1 (Theorem 11.97(c)) | **applied correctly, in a stronger form** (an explicit rate); the new step is right (item 3(a)) |
| **1.** SCI-REV-0005 M2 ((G1), (G2), (L) in Theorem 11.101) | **applied correctly**, with one constant of ours corrected (item 2(c)(a)) |
| **1.** SCI-REV-0006 W1, W2, M1–M5 | applied; M4 not as a sharpening but as a correction of *us* (item 2(d)) |
| **1.** minor findings (38 of 41 read, 20 checked) | applied; three recommended actions not done and declared as such; two digits of ours silently corrected (they are right) |
| **2(a)** "with one phase"; ferromagnets | **both amendments right.**  The first corrects a slip of ours; the second reflects a proof added after the text we reviewed |
| **2(b)** "`E′` equals `E` to four digits" | **they are right**: `E′ − E = 6.06·10⁻⁵` at `u = 2`, `n = 200` (`0.1129` against `0.1130`) |
| **2(c)** `2m`; ceiling for every envelope; the data point | **all three right** (re-derived; re-computed to nine digits) |
| **2(d)** "M4 is not a sharpening" | **they are right, we were wrong.**  A correction was published while I worked (SCI-RES-0007 §2); it is correct and omits three things (§2.4) |
| **3(a)** `ω_n ≤ q_max·n^{−1/(2q_max+2)} + c·n^{−1/4}` | **correct**; `c` may be any number above `c_ω = m[q_max e^{D_max}/π_min + ln(1/π_min)]/(2 + m·q_max)` |
| **3(b)** Proposition 11.69a | the same statement as our A2.2, with the rounding made explicit; `c = 277.13`; correct |
| **3(c)** Theorem 11.48(d), `Scattering.lean` | statement = our A2.1 (with one imprecision of ours repaired); machine-checked: the Lipschitz constant as an upper bound and the matched bound for a list of squared distances; not machine-checked: exactness of the constant, the link to conformations and to the class |
| **3(d)** `TwoRoundsExpected.lean` | **as described**: +6 lines of provenance, −4 `#print axioms` (and a blank line); declarations byte-identical |
| **4.** exact semigroup | **proved** (Theorem R9.1), stronger than the sketch: the error of Lemma 11.68 is a coboundary.  `K^{br}` is a Newton–Okounkov body; `β` disappears (`168 → 108` for all bridges, `0` for clean ones; with exact points `vol 𝒦 ≥ 1.6313` in place of `1.5632`, and the four packings hold with zero radii); the prediction becomes a **theorem for bridges**, and stays conjecture-dependent for walks; the tables up to 24 beads are consistent with it and cannot test the constant |
| **5.** what became worse | nothing became false in a theorem.  **One new sentence is false as stated** (a parenthetical example, line 5283); eight minor defects (§5) |

**Findings, classified** (details and replacement texts in §6).  *Critical* (a published
statement is false): **one in the theory text**, of no consequence — the example in
parentheses at lines 5283–5284; **one in our own**, already corrected — SCI-REV-0006 M4.
*Major:* none in the theory text; one in ours — the clause "without a field these two
exponents are the uniform cube's" of our replacement text for M1 of SCI-REV-0001.
*Minor:* eight in the theory text, seven in ours.

---

## 1. Item 1 — is the revised text right?

### 1.1 SCI-REV-0003 M1: the stopping rule in Theorem 11.84 (lines 6476–6569)  — applied correctly

*Read and re-derived.*  The rule is in the statement ("stops and returns the trivial
bracket `[s₀, s₀e^{2un}]` if `|C_l| > N_l`", line 6487), "applied before any evaluation of
stage `l`" (6489) — the order our review asked for.  Claim B is now what it can be: a
deterministic statement under the hypothesis that every stored bracket of rung `l − 1` has
ratio at most `e^{x_{l−1}}` (6497–6500), and the proof marks the one place where the
hypothesis is used (6556–6558).  I re-derived the count: a member `i > K` with witness `j`
lies among the first `M*` points, `M* < 4νs_j/(λ_je^b)`, and is counted in `N_L(i′, M*)` for
the largest level `i′` with `s_{i′} ≤ s_je^{−x_{l−1}}` (so `i′ < j` and `s_j/s_{i′} < e^{x_{l−1}+λ}`);
the definition of `λ_j` as a maximum of empirical quantities bounds that count by
`4(1+η)c_η^{−1}e^λνe^{x_{l−1}}`; summing over `J + 1` levels and adding `K` gives `N_l`.  **[P,
re-derived]**

*The one thing I looked for as a possible new gap.*  The batched schedule calls `I_1` on
all `M_max` fibres, more calls than the sequential algorithm makes; does the good event
cover them, so that the rule cannot fire on it?  Yes: Theorem 11.56 (lines 4294,
4320–4321) takes `δ′ = δ/(4LM̄)` and its good event is "every *potential* inner call valid";
the batched calls are potential calls (`M_max ≤ M̄`).  **[read]**

*The workstream's variant* ("a stored bracket of rung `l − 1` has ratio above `e^{x_{l−1}}`")
"serves as well": correct — if it does not fire, Claim B applies.

### 1.2 SCI-REV-0001 M1 and M2 (§11.25)

**M1** is applied in the title (6785), the introduction (6792–6794), "What this covers,
and what it does not" (7079–7093), Corollary 11.91(ii) (7097–7105), the *Reading*
(7253–7262), and in §0.3, §8, §10 row G27, §12 and the README (word diff read).  The text
is narrower than our replacement text in one clause and wider in another; both changes
are right — §2.1.

**M2.**  The repair (7003–7023) is a complete proof.  **[P, re-derived]**  Chain: for a
profile with `e + MI(μ) > 0` strong duality holds (Slater point `ν = μ`); for fixed
`(t, ξ)` the functional `ρ ↦ E_ρ g_{t,ξ}` is linear on the polytope of laws on the given
support with mean `κ` and `E_ρKL(·‖κ) ≥ −e`, hence maximal at a vertex; a vertex has at
most three atoms, and three only if the inequality is active, i.e. the budget is zero and
`r = −e`; weak duality at the vertex gives `r^κ_μ(e) ≤ max(R^{κ,(2)}(e), −e)`; and
`R^{κ,(2)}(e) ≥ −e` by the shell with `F = −e` of the centre `m = κ` (`F(ℓ_max) = h(κ)` there —
checked).  `MI ≤ h(κ)` gives the range `e ≥ −h(κ)`.  For `N^κ` at `X = 0` Slater's condition
can fail; the text's "read sup for max" is right because the value function of a convex
programme on a compact set with continuous data is closed.  Corollary 11.91's proof
handles the remaining case — `μ` feasible at `e′ = e + (I−λ)(κ)` but not at `e` — by
`r^κ_μ(e′) ≤ MI(μ) < −e ≤ R^κ(e)` (7116–7119).
*Own numerics* (`r9_slices.py`): 360 random feasible profiles with 3–5 blocks at six
triples `(κ, u, e < 0)`, inner minimum by a convex solver with several starts: none
exceeds the two-block supremum; the two-block supremum at `(½, 1, −0.05)` is `0.059050`, the
report's `0.0590497` (Proposition 11.82).  **[N, re-computed]**  This is a weak test — random
profiles stay `1.7·10⁻⁴` to `5·10⁻³` below the supremum; I did not optimise over profiles as R1
did.  The verdict rests on the proof.

### 1.3 SCI-REV-0002 M1 and M2 (§11.22)

**M1.**  The headline is three labelled sentences (5114–5125); the same wording stands at
3789–3796, 5410–5420, 5654–5662, in §0.3 (line 91), §8 (1284–1295), §10 (1441, 1498–1505,
1626), §12 (8482–8495) and the README.  "The plateau is real" is withdrawn with its
reason.  **[read]**

**M2.**  *Re-computed with own code* (`r9_packing_volume.py`): the vertex list of the
packings is rebuilt from the counts `(N, h₃, h₈, h₁₁, g)` of the ten bridges as recorded by
the theory division (`wit/verified.json`) and by R2 (`witness_points_W64.json`,
`witness_big.txt`) — identical; the four weight files in the export are byte-identical
to ours; in exact rationals all pairs satisfy
`L‖p_k − p_l‖_c > e(g_k + g_l) + 2ε₁ + max(L, e)(d_k + d_l)` for 116, 451, 8, 19 points (smallest
margins `1.0·10⁻³`, `1.4·10⁻⁴`, `2.0·10⁻²`, `3.3·10⁻⁴`).  The condition itself is sufficient:
if `(p′, g′) ∈ K^{br}` is within `d` of `(p, g)` in `‖·‖_c + |·|`, then `L‖Δp‖` and `e·g` move by at
most `max(L, e)·d`.  **[P, re-derived; N exact]**  Hull volume `1.631706`, eroded by
`168/12 044`: `1.563226`; `𝒦₂` from its twelve printed vertices: `3.125000` (floating point,
own formulation of the erosion through support functions).  The arithmetic of the
revised text was re-done: `3627/116 = 31.3`; `116/15 = 7.7`; `17.6N^{−1/3} − 17/N ≥ ½` exactly up
to `N = 43 512`; `≥ ¼` up to `348 709` (text: `3.4·10⁵`, conservative); with Bezdek's constant
`≥ ½` up to `111 803`; `3(18π)^{1/3}/π = 3.66532`, `4.61802`, `24.14`, `29.4`, `k ≥ 0.68976`;
`g − 9p₃ + 3p₈ − p₁₁ = 4.306` at the 22 351-bead bridge with uncertainty `2.4·168/22 354 = 0.018`
(the dual norm of that functional is `2.4`); tetrahedron volume `1/12`.  **[N]**

### 1.4 SCI-REV-0005 M1 and M2 (§11.26)

**M1** is Theorem 11.97(c) (7390–7453) with the uniformity over compositions in the
statement; its proof is in the report now, not only in `W_REPORT.md`.  I re-derived it
step by step — §3.1.  **Applied correctly; stronger than asked** (a rate).

**M2** is the paragraph "Families indexed by compositions …" (7600–7647).  (G1) is our
definition verbatim with `2m` for `m`; (G2) is our claim with `Φ_H(D) ≤ e^{−n_oθ}e^{n_ox}/4` for
`Ξ_H(e^{−n_oθ}) ≤ …` (the same statement), and its proof is right: otherwise Theorem 11.97(c)
with `e″ = x − θ − ln 4/n_o` gives `θ ≤ R̂(e′) + ω′`, `e′ = x − θ − ω′`, so `S(e′) ≥ x − 2ω′` and
`θ_na(x − 2ω′) ≥ R̂(e′) ≥ θ − ω′`.  (L) follows from `0 ≤ F*_j(τ) ≤ a_j(1 − τ)` (the Rényi capacity
of order `τ < 1` is at most the Shannon capacity).  **[P, re-derived]**

### 1.5 SCI-REV-0006

W1 (row D3, line 55), W2 (§6.4, 1026–1066; row E1, line 63), M1 (922–924, §6.4), M2
(Proposition 11.69a), M3 (5547–5563), M5 (Theorem 11.48(d)), W3, W5, W6, W7, W8, W9, W10, M6,
M7: all in the text, each marked as resting on our reading
(`docs/prior_art/L9_review_additions.md` in the export says per source who read what).
Three attributions that looked like additions of theirs are ours: "unverified checker"
for van Doren et al. (A2_REPORT line 365), "searches thin" (line 481), `L_{H,p}` (line
487).  **No attribution to us of something we did not say was found.**  M4: §2.4.

### 1.6 Minor findings sampled

Read where applied: SCI-REV-0003 m1–m9 (9 of 9; m7 in the errata of `U_REPORT.md`);
SCI-REV-0001 m1–m12 (12 of 12); SCI-REV-0002 m1–m8 (8 of 8); SCI-REV-0005 m1–m4, m6–m10 (9 of
12; not m5, m11, m12, which went to the errata of `W_REPORT.md`).  Checked by own derivation
or own code — 4 of 9, 7 of 12, 4 of 8 and 5 of 12:

| finding | where | check | result |
|---|---|---|---|
| R4 m3 (Lemma 11.85, `r` rounds) | 6583–6606 | re-derived: `Ẽ_1 ∩ … ∩ Ẽ_{t−1} ∩ Ẽ_t^c` lies in {virtual batch `t` has at most `M_t` points} `∩ Ẽ_t^c`, and that batch is a function of the coins and `s¹..s^{t−1}` | correct |
| R4 m9 (witness for three rounds) | 6542–6544 | `r9_minor.py`: the three terms are `0.54015a`, `0.54026a`, `0.54022a` | `0.54026a` ✓ |
| R4 m5, m6 | 6427–6436, 6713–6715 | read; `h/a = 0.26265`, two rounds `0.6244a` re-computed | ✓ |
| R1 m1 (input law of the asymmetric channel) | 6833–6838 | `r9_m1_input.py`: 3 000 random `(J, h₂ > 0)` | `−h₂ < h₁ < 0` and `EB > 0` in all |
| R1 m2 (envelope step) | 6871–6874 | re-derived (`δ` maps `(0, ∞)` onto `(0, J)`; second derivative at the root) | correct |
| R1 m3 (closed form on half a ray) | 6964–6967 | `r9_minor.py` | `0.020200` and `0.144080`: **the report's `0.0202`, `0.1441` are right; our review printed `0.0201`, `0.1439`** |
| R1 m4, m5, m6 | 6955–6977, 6943–6949 | re-derived (value `−e` for `e ≤ −F(ℓ*)`; the two forms of the cube's function; where strictness holds) | correct |
| R1 m11 (table, centre types, cusp) | 6978–6988 | `r9_minor.py` | all twelve values and eleven centre types to the printed digits; `N^κ(10⁻¹²) = N^κ(0⁺) − 5.800·10⁻⁷` |
| R2 m1 (bookkeeping for the Lean form) | 5264–5278 | re-derived; costs `28, 42, 44` re-counted by height; `r9_semi.c`: appending three beads costs at most `(1, 6, 9; 1)` for `N ≤ 20` | correct |
| R2 m3 (maxima of the concatenation error) | 5225–5236 | `r9_cobound.c`, all pairs with `N ≤ 13`: `(1, 6, 8, 1)`, norm 41; `r9_semi.c`: `A`-part `(1, 5, 7, 1)`, norm 37 at `N ≤ 16`, `B`-part `(0, 3, 4)` first at 14 beads | ✓; **new:** the `A`-part reaches its proved bound `(1, 6, 10; 1)`, norm 44, at 21 beads — so the error bound `(1, 9, 14; 1)`, norm `β = 60`, of Lemma 11.68 is attained (`N₁ = 21`, `N₂ = 14`) |
| R2 m4 (the third hand inequality) | 5425–5430 | re-derived from `C(d,2) ≤ (5d − 8)/2`, `≤ 3d/2`, two end beads | `h₈ ≤ 2h₃ + 3N + 3` ✓ |
| R2 m6, N1 (helix; interior) | 5456–5465 | `r9_long.py`: helix for `N` up to 1 001 | bridge, `h = (0, 0, N−3)`, `g = N−3`; and it is *clean* (§4) |
| R5 m1 (ranges of the dictionary) | 7503–7512 | `E_sp(0.3a) − 0.3a = −0.00817` on the cube, `u = 1` | "`−0.008`" ✓ |
| R5 m3 (what is machine-checked) | 7323–7331 | the four declarations of `GroupSampling.lean` and the three of `RenyiCentre.lean` exist under the cited names | ✓ (statements not re-read; R5 read them) |
| R5 m7 (the Lean theorem for the start at complete enumeration) | 7648–7656 | read `iterates_lt_hint_add` (`HintRecursion.lean`, line 326): hypothesis `hbdd : ∃ C, ∀ x, 0 < x → T 0 x ≤ C`, conclusion `∃ k, T k g < θh g + η` for `0 < g < E`; `stepLE_exact`, `GameFunction.pair` exist | the citation is now the right one |
| R5 m10 (R10's report) | 7305–7307 | `EXPORT/docs/reviews/R10_referee_report.md` exists | ✓ |
| R5 m8 (slope jump) | 7561–7566 | `r9_minor.py`, own site code: the site is `d₀₁ = 1`, `d₁₂ = 1.5`, `d₀₂ = 2`; `E`, `a`, `h` reproduced; one-sided differences at `t_c` | `+0.0055 … +0.0057` ✓ (`+0.0056`, not `+0.0052`) |

*Not done by the theory division, and said so in the text:* witnesses for `T^{(r)}(0)`,
`r ≥ 4` (R4 m9, request 6); the exhaustive concatenation test in the harness (SCI-REV-0002,
action 5; line 5685–5689); the finite-`N` certificates N5 (not re-derived, 5490–5493).

---

## 2. Item 2 — their amendments to our texts

### 2.1 (a) THY-RES-0007 §1.2 — both amendments are right

*"Without a field these two exponents are the uniform cube's" holds with one phase
only.*  Our replacement text for M1 said it without the restriction.  The theory report
that we reviewed already contradicted that: Proposition 11.81(b) at `5ed4072` (our tree,
lines 5387–5392) has `R_H < R_unif` beyond the junction for `B = 0` — `0.0251012` against
`0.029139` at `βJ = 1.5`, `u = 1`, `e = 0`, a number R1 itself reproduced.  R1's own statement
(A) (`R1_REPORT.md` §5.4) carries the hypothesis "if `I` is symmetric and convex"; the
replacement text of the message dropped it.  **The slip is ours.**  (Beyond the junction
"`R_H < R_unif`" is a numerical statement in the theory report — the local half is proved —
so our clause was unproved and numerically false there, not refuted by a theorem.)
SCI-RES-0007 §1, published while I worked, accepts both amendments as "consequences of
your Proposition 11.81(b), (c) as corrected at `40c5bd7`; our text was written against
`5ed4072`".  That explains the second amendment, not this one: the restriction to one phase
was needed at `5ed4072` already.

*For adaptive algorithms without a hint the comparison is proved also for ferromagnetic
Curie–Weiss parts.*  At the two commits R1 reviewed (`5ed4072`, `89ac710`) Proposition
11.81(c) was "a sketch" with a named missing step (checked with `git show`); it became a
proof "given Theorem 11.64" at `40c5bd7`.  So R1's "the only proved bounds are
`R_H ≤ θ* ≤ θ_na ≤ θ_na^{cube}`" was right for the text reviewed and is out of date now.  I
re-derived the completion (6159–6178): the Hubbard–Stratonovich mixture; the identity
`A_y(ψ) = C_n(y, y_j)·A_{y_j}(ψ − 2(y − y_j)|x|)` (from `P_y(x)/P_{y_j}(x) = C_n e^{2(y−y_j)|x|}`); the
tilted residual is in `L_{u+2Δ}`; a finite net gives a uniform `o(n)`.  **[P, re-derived,
given Theorem 11.64 and Proposition 11.65(b), which I did not check]**  One thing it uses
silently: the cost of the algorithm of Theorem 11.64 must stay `e^{o(n)}` when the
confidence is divided by the number `~n²` of grid fields.

### 2.2 (b) §1.1 — "`E′` equals `E` to four digits" is too strong; they are right

*Re-ran R4's code* (`twins_exact.py`, imported read-only; `r9_Eprime.py`):

| `u` | `n` | `E` | `E′` | `E′ − E` |
|---|---|---|---|---|
| 2 | 200 | `0.1129377` | `0.1129983` | `6.06·10⁻⁵` |
| 1 | 400 | `0.0300511` | `0.0300815` | `3.04·10⁻⁵` |
| 2 | 400 | `0.1151956` | `0.1152076` | `1.19·10⁻⁵` |
| 1 | 800 | `0.0341146` | `0.0341220` | `7.4·10⁻⁶` |
| 1 | 1600 | `0.0354251` | `0.0354261` | `1.1·10⁻⁶` |
| 2 | 1600 | `0.1211719` | `0.1211727` | `8·10⁻⁷` |
| 1 | 3200 | `0.0368445` | `0.0368447` | `2·10⁻⁷` |

At `u = 2`, `n = 200` the fourth decimal differs (`0.1129` / `0.1130`); at `u = 1`, `n = 400` the
fourth significant digit differs.  Their bound `6.3·10⁻⁵` (own implementation) is
consistent with `6.06·10⁻⁵`.  The revised report makes no four-digit claim (6707–6709).
*Correction owed:* `R4_REPORT.md` line 286 — "which exceeds the printed `E` by at most
`6.1·10⁻⁵` (`u = 2`, `n = 200`: `0.1130` against `0.1129`) and by less than `10⁻⁵` from `n = 800` on".

### 2.3 (c) §1.4

**(a) `2m`, not `m`.**  With `f_j = φn_j − ⌊φn_j⌋`, `F = Σf_j < m` and `p_j = n_j/n`, the
composition `c` of the inner block (`n_i ≥ (1−φ)n` sites) satisfies
`‖c − p‖₁ = Σ_j|f_j − F·p_j|/n_i < 2F/n_i < 2m/n_i`.  It exceeds `m/n_i` for `m ≥ 3`: `p = (1 − 2ε, ε, ε)`,
`f = (0, 1⁻, 1⁻)` gives almost `4/n_i`.  For `m = 2` the sum is `2|f₁p₂ − f₂p₁| < 2`.  So R5's
`m/((1−φ)n)` is wrong for three or more site types and their `2m` is right; immaterial.
**[P, re-derived]**

**(b) The ceiling for every envelope.**  With `Q = π` in the radius form,
`(1−t)D_t(π_φ‖π) = tΛ(1) − Λ(t)`, `Λ(s) = ln E_πe^{−sφ}`; `Λ″ ≤ (osc φ)²/4` and
`osc φ ≤ max_{a,b}d(a,b) =: D` for every `φ` in the Lipschitz polytope, symmetric envelope or
not; a function that vanishes at 0 and 1 with second derivative at least `−c` is at most
`c·t(1−t)/2`.  So `F*(t) ≤ t(1−t)D²/8`.  **[P, re-derived]**  (R1's report, §5.5, already says
"for a general site envelope replace `u` by `max d`"; only the message did not.)
*Own numerics* (`r9_sites2.py`): 280 pairs (site, `t`) on 40 random sites with asymmetric
envelopes, 2–4 letters: largest ratio `0.7465`; the uniform three-letter Hamming site is
below the ceiling in `h` by `9.7 %`, `5.0 %`, `1.9 %`, `5.8 %` at `u = 0.1, 0.5, 1, 2` — the
report's `5.0`, `1.9`, `5.8` (lines 7739–7741).

**(c) The data point.**  *Own code* (`r9_sites.py`, written from the statements of
Theorems 11.98–11.99; every optimum with a duality bracket; the cube's closed forms
reproduced to ten digits).  At `u = 0.5` (cube: `h = 0.0076729`, `a = 0.0302999`, `E = 0.0309298`):

| site law | `h` | `a` | `E` | against the cube |
|---|---|---|---|---|
| `(0.02, 0.49, 0.49)` | `0.007672224` | `0.030304356` | `0.030922047` | **below in `h` and `E`, above in `a`** — as they say |
| `(0.05, 0.5, 0.45)` | `0.007675166` | `0.030321669` | `0.030931644` | above in all three (`+0.030 %` in `h`) |
| `(0.04502, 0.45679, 0.49819)` | `0.007675293` | `0.030321715` | `0.030931982` | above |
| `(0.001, 0.4995, 0.4995)` | `0.007672975` | `0.030300641` | `0.030929982` | above (`+0.0014 %`) |
| uniform | `0.007425205` | `0.030166900` | `0.029097814` | below |

Every printed digit of Proposition 11.103(d) is reproduced, also at `u = 1` (`0.119499`,
`0.120196`, `0.030654`, `0.123284`, `0.030572`, `0.122951`).  "Laws near `(½, ½, 0)` lie on both
sides of the cube" is right; the half that is a theorem (weight `½` on a set of letters)
held in 200 of 200 random cases.  **[N, re-computed]**

### 2.4 (d) "M4 is not a sharpening" — they are right, and we were wrong

*Line by line* (`docs/workstreams/G_REPORT.md` in our tree, unchanged since `5ed4072`):

| | workstream G, §2.1 (lines 97–119) | our A2 (`A2_REPORT.md` 281–288; SCI-REV-0006 M4) |
|---|---|---|
| bound | (c), line 99–101: `I_A ≤ Ī(i) = Σ_p d̄(p)²`, `Ī(m) = ⅓ sin²(θ/2) b² m³(1 + O(1/m))` | `I_arm ≤ (b² sin²(θ/2)/3)·m³(1 + o(1))` |
| argument | line 102–103: "the distance to the axis is at most the distance to the axis atom; atoms two bonds apart are at the fixed distance `2b sin(θ/2)`; triangle inequality" | "the largest end-to-end distance of `j` bonds, attained by the all-trans zigzag" |
| extremal conformation | line 106–109: "one gauche next to the axis followed by all-trans (an arm almost perpendicular to the axis)", `0.256 → 0.228` against `0.2264` | "an all-trans arm joined through one gauche torsion is perpendicular to the axis" |
| constant | (d), line 115: `c_i^ver = 2Λ sin(δ/2)√Ī(m_i) ≤ (2/√3) sin(δ/2) sin(θ/2)·Λ b m_i^{3/2}(1 + O(1/m_i))` `= 0.824…` at `θ = 111°`, `δ = 120°` | `sup 2√(2I_red) = (2√2/3)·b m^{3/2} = 0.943…` at the centre, `4/3` far from it |

`(2/√3) sin(δ/2) sin(θ/2)` is `0.824126` at `(111°, 120°)` and `0.942809 = 2√2/3` at the
tetrahedral angle with `δ = 180°` (`r9_lever.py`).  Same bound, same argument, same
extremal arm; two parameter sets.  And our `4/3` is not a second sharp constant: it is
the looser form `2√(2I_red)` of Theorem 4.6(d), a factor `√2` above the verified constant
`2√min(I_A, I_B)` when one arm is much longer — a *weaker* bound than theirs.  Own
numerics: G's `Ī(m)/m³` is nonincreasing for all `m ≤ 2·10⁵`, so "`c_i^ver ≥ 0.824…` at every
position" holds; the kinked arm at `θ = 111°` makes `88.23°` with the axis (`I/m³ → 0.22618`,
`0.1 %` below the bound; two gauche torsions reach `sin² = 0.999999`); exhaustive over the
first seven arm torsions at `m = 200`: `0.22786` (G: `0.228`).

**What was false in our texts:** (i) SCI-REV-0006 M4 and row G16 ("Sharp constant: see
M4"), T-5; (ii) `A2_REPORT.md` line 40 ("find the sharp asymptotic constant `2√2/3 = 0.943` …
(the report states `≥ 0.824`)"), lines 286–288 — in particular the sentence "Theorem
11.36's '`c_i ≥ 0.824·Λ b m_i^{3/2}` for every position' is confirmed and is **not sharp in
the constant**", which is false: at the report's parameters `0.824` is the sharp limit —,
line 645 (W6's suggested wording "sharp constant `2√2/3` at the centre of a tetrahedral
chain"), 661, 682, 739.

**The correction already published** (SCI-RES-0007 §2, commit `242f771`, while this
workstream was running; head note on SCI-REV-0006; `docs/science/DEAD_ENDS.md` SD38) is
correct.  I read it after my own check.  It does not say three things:

1. the `4/3` "far from the centre" is a looser bound than the theory division's, not a
   sharp constant;
2. the argument and the extremal conformation were in G §2.1(c) as well (the published
   text cites line 115 only), so nothing of our "[P sketch + N]" was new;
3. `A2_REPORT.md` itself carries no note, and its sentence "not sharp in the constant" is
   false.

**Text of the linked correction I would add** (to be attached to SCI-RES-0007 §2 or sent as
its addendum; also as a note at lines 40 and 281 of `A2_REPORT.md`):

> *Addendum to the linked correction of SCI-REV-0006, item M4 (workstream R9).*  Checked
> line by line against `docs/workstreams/G_REPORT.md` §2.1(c)–(d) (lines 97–119 at
> `5ed4072`).  Three further points.  (1) The bound `Ī(m) = ⅓ sin²(θ/2) b² m³(1 + O(1/m))`, its
> proof (distance to the axis atom; atoms two bonds apart at distance `2b sin(θ/2)`) and
> the extremal arm (one gauche torsion next to the axis, then all-trans) are all in that
> section; our "three-line argument" and "attained by an all-trans arm behind one gauche
> torsion" repeated them.  (2) Our "`4/3` far from the centre" is the looser form
> `2√(2I_red)` of your Theorem 4.6(d); with the verified form `2√min(I_A, I_B)` the constant
> is the same at every position, so ours was a weaker bound there, not a sharp one.
> (3) The sentence of `A2_REPORT.md` (§3) "Theorem 11.36's '`c_i ≥ 0.824·Λ b m_i^{3/2}`' … is not
> sharp in the constant" is false: `0.824 = (2/√3) sin 60° sin 55.5°` is the limit of
> `c_i^ver/(Λ b m_i^{3/2})` at your parameters, approached from above.  W6's suggested wording
> should read "(limit constant `(2/√3) sin(δ/2) sin(θ/2)`; workstream G)".  What remains of
> M4: the old tag "lower constant numerical" belonged to another constant (`0.186`).

---

## 3. Item 3 — the statements written while the reviews were applied

### 3.1 (a) The `χ²` bound and the error term of Theorem 11.97(c) — correct **[P, re-derived; N]**

*The identity.*  For a product known part `I(P) = Σ_jλ_jKL(P_j‖π_j)` and
`v(P) = min_{P′}[I(P′) + W(P′, P)]`.  By Kantorovich duality and the minimax theorem site type by
site type, `v(P) = Σ_jλ_j max_{γ∈L_j}[−ln E_{π_j}e^{−γ} − E_{P_j}γ]`, hence

    (I − v)(P) = Σ_j λ_j · min_{γ∈L_j} KL(P_j ‖ π_γ)                                  (as in line 7440).

*The bound.*  If `Q` is in the window, `Q_j = π_{γ_j}` with `γ_j ∈ L_j`, so
`min_γ KL(P_j‖π_γ) ≤ KL(P_j‖Q_j) ≤ ln(1 + χ²(P_j‖Q_j)) ≤ χ²(P_j‖Q_j)`, and `Q_j(a) ≥ π_min e^{−D_max}`
because `osc γ ≤ D_max` on `L_j`.  On the set `G` of the proof `|P_j(a) − Q_j(a)| ≤ κ₂/λ_j`, so
`λ_jχ²(P_j‖Q_j) ≤ q_maxκ₂²e^{D_max}/(λ_jπ_min) ≤ q_maxκ₂e^{D_max}/π_min` when `λ_j ≥ κ₂`; a type with
`λ_j < κ₂` contributes at most `λ_jKL(P_j‖π_j) ≤ κ₂ ln(1/π_min)`.  Summing over the `m` types gives
their `ω′ = m·κ₂·[q_max e^{D_max}/π_min + ln(1/π_min)]`, uniformly in the composition.  ✓

*The other steps* (all re-derived): Hoeffding with `κ₁ = κ/((2 + m q_max)max(D_max, 1))`
puts the exit into `D` — the realised cost and type move `v(P_{X′ⁿ}) + d/n` by at most
`κ₁D_max(1 + m q_max/2) ≤ κ/2 < 2κ` — and into `G` (`κ₁ ≤ κ₂`); the window step (`P″` minimising
`I(P″) + W(P″, P′)` has `I(P″) = v(P″) = v(P′) − W(P″, P′)`, the cost grows by at most `W(P″, P′)`,
the information does not grow); `μ_H(y) ≥ Q^⊗(y)e^{−n(I−v)(P_y)}/N_orb`; data processing on
`D ∩ G`; the evaluation step (for slopes `τ ≥ 1` the identity kernel gives `α(μ) − B′ ≤
R̂(B′ − α(μ))`, because `v ≤ I` and `R̂(e) ≥ −e`); the shallow piece (`−e + 3κ + o(1)`).

*Where the leading term comes from, and that it enters once.*  Lemma T′ (`W_REPORT.md` 362–
380) gives `α_A − q_max/M ≤ α ≤ α_Ã` and the chain-rule defect `η_{M,n} = q_max/M + Σ_jq_j(M+1)^{q_j}
ln(n+1)/n`.  In Step 2 only the right inequality is used (`I(X;U|T) ≤ α_C̃`): no `q_max/M`
there.  `q_max/M` enters in Step 5 alone, additively, through `η_{M,n}`.  With
`M = ⌈n^{1/(2q_max+2)}⌉` the remaining `M`-dependent terms are `O(n^{−(q_max+2)/(2q_max+2)} ln n)`.

*The requirements on `ω_n`:* it must be at least the shift `2κ + o₁ + o₂` of the argument,
at least the additive term of the deep case
`[η_{M,n} + ln 2/n]/(1 − p_n) + p_n ln q_max/(1 − p_n) + ω′ + n^{−1}ln N_orb`, and at least `3κ + o(1)` (shallow
case).  With `κ = n^{−1/4}` and `κ₂ = κ/(2 + m q_max)`:

    ω_n  ≤  q_max·n^{−1/(2q_max+2)} + c·n^{−1/4}    for n ≥ n₀(c),      for every   c > c_ω := m·[q_max e^{D_max}/π_min + ln(1/π_min)] / (2 + m·q_max)

(the `2κ` and `3κ` are separate requirements, dominated by the leading term for large `n`;
`c_ω < e^{D_max}/π_min + ln(1/π_min)/q_max`; for the two-letter cube with `u = 1`: `c_ω = 2.89`).
**The claimed form is right; the constant is `c_ω` plus anything.**  "Below `n₀` the
statement is trivial with `ω_n = D_max`" is right too (`Φ_H⁺(D) ≤ e^{2nD_max}μ_H(D)` and
`R̂(e′) ≥ −e′`).

*Numerics on small alphabets* (`r9_sites2.py`, `r9_chi2_check.py`):
* two letters, 400 random `(π, asymmetric d, P)`, `v` by a grid search without a solver:
  the formula for `I − v` holds to the grid resolution (`5·10⁻⁷`), `0 ≤ I − v ≤ χ²(P‖Q)` for
  every window point `Q`, largest `(I − v)/min_Q χ² = 0.80`;
* 2–4 letters, asymmetric envelopes, 120 random cases: `v` from couplings (primal) and
  from `γ ∈ L` (dual) agree to `4·10⁻¹⁵`; `0 ≤ I − v ≤ KL(P‖Q) ≤ χ²(P‖Q)` in all;
* the bound on `G`: 300 random chains with 1–3 site types, compositions with small
  fractions, `κ₂ ∈ [3·10⁻⁴, 0.1]`, adversarial `P` at the edge of the box: largest
  `(I − v)/ω′ = 0.015` — the bound holds and is far from tight.

*What this does not give:* a usable `ω_n` at any size one can compute (`q_max n^{−1/6}` is
`0.98` at `n = 72` for two letters); the true size is unknown, as the text says.

### 3.2 (b) Proposition 11.69a (lines 5288–5313) — our A2.2, slightly sharper **[P, re-derived]**

First display: with `p = Σλ_iq_i/m`, `k_i = ⌊λ_iM/m⌋` (some `k_i ≥ 1` because some
`λ_i ≥ 1/(d+1)` and `M ≥ (d+1)m`), (C) used `Σk_i − 1 < M/m` times, (E) used
`M − M′ < (d+1)m` times, and `|Σk_iq_i/M − p| ≤ (d+1)(m/M)R`: total `β/m + (d+1)(β′+R)m/M`.  ✓
Second display: with `m = ⌈√(βM/A)⌉`, `A = (d+1)(β′+R)`: `β/m + A m/M ≤ 2√(βA)·M^{−1/2} + A/M`.  ✓
Our A2.2 said "`≤ c·M^{−1/2}` up to rounding"; their `+ (d+1)(β′+R)/M` is that rounding.
`c = 2√(60·5·64) = 277.13`.  The uniformity on compact subsets of the interior follows from
a finite cover by simplices.  Same statement, constant right.

### 3.3 (c) Theorem 11.48(d) and `Scattering.lean`

*The statement* (3569–3595) is our A2.1.  One imprecision of ours is repaired: `sinc(q√s)`
does not vanish beyond a cutoff, as the class of Theorem 11.48 requires; they take the
cutoff at the largest possible squared distance and subtract the known constant
`sinc(q√S_c)` per pair (3584–3585).

*The Lean file* — a scratch copy (`experiments/science/ws_R9/lean/Scattering_copy.lean`,
the export's file plus `#check`/`#print axioms` lines) compiled with `lake env lean`: exit
0; it imports Mathlib only; the eight headline declarations depend on `propext`,
`Classical.choice`, `Quot.sound`.  **What is machine-checked:**

* `sinc_sqrt_lipschitz`: for real `q` and `s, s′ ≥ 0`,
  `|sinc(q√s) − sinc(q√s′)| ≤ (q²/6)|s − s′|` (`Real.sinc`, the unnormalised `sin t/t`);
* `debye_sum_sub_le`, `debye_sub_le`: for a finite index type `ι`, families `s, s′ : ι → ℝ` of
  nonnegative numbers and **any** permutation `σ`,
  `|debye N q s − debye N q s′| ≤ (q²/3)Σ_k|s_k − s′_{σk}|`, where
  `debye N q s := N + 2Σ_k sinc(q√(s_k))`;
* `debye_eq_of_matching`: equal multisets give equal values.

**What is not machine-checked** (and the index row at line 1385 claims none of it):
that `q²/6` is the *exact* constant (the docstring of `one_sub_sinc_le`, line 219 of the
file, is headed "non-vacuity and sharpness" but the theorem is only the inequality
`1 − sinc t ≤ t²/6`); the link between `debye` and a conformation — `N` and `ι` are unrelated
in the definition, the `s_k` are any nonnegative reals; that the sorted matching is the
transport distance; membership in the class of Theorem 11.48 (the file does not import
the module that defines it); the Debye formula as an orientational average.  **Scope as
stated by them and by us:** one conformation, kinematic scattering, `q`-independent form
factors, no cutoff, no ensemble.  The Lean statement is in fact indifferent to a cutoff —
it is about any finite list of squared distances.

### 3.4 (d) `TwoRoundsExpected.lean`

`diff experiments/science/ws_R4/lean/TwoRoundsExpected.lean EXPORT/proofs/Frontiers/TwoRoundsExpected.lean`:
six lines added (a provenance paragraph in the header comment, lines 6–11), five removed
(a blank line and the four `#print axioms` at the end).  The four commands are at lines
507–510 of `EXPORT/proofs/AxiomAudit.lean`.  `TwoRounds.lean`, which it imports, is
byte-identical to `5ed4072`.  A scratch copy compiles (exit 0; the four theorems depend
on the three standard axioms).  **THY-RES-0007's description is exact.**  The theory
report says "adopted unchanged" in three places (lines 1380, 6473, 6679); "its
declarations unchanged" would be the accurate wording.

---

## 4. Item 4 — the exact semigroup for bridges: proved

### 4.1 Definitions (precise)

Setting of §11.22: diamond lattice, height `y`, every bond changes the height by `±1`;
sites whose heights differ by 4 or more are farther apart than the cutoff (`|Δy| ≥ 4`
gives squared distance `≥ 16 > 12`).  A bridge `x = (x_0, …, x_{N−1})`, `N ≥ 3`, has its first
bead strictly lowest and its last bead highest; so `u₁ = x₁ − x₀`, `u₂ = x₂ − x₁` and the last
bond `b = x_{N−1} − x_{N−2}` are up-bonds.  Let `b′ = x_{N−2} − x_{N−3}`.

* *Admissible `c₁`:* `c₁ = b′` if `b′` is an up-bond, otherwise either of the two up-bonds out
  of `x_{N−1}`.
* *Sites above:* `t₁ = x_{N−1} + c₁`, `t₂ = t₁ + b`, `t₃ = t₂ + c₁`, regarded as beads `N, N+1, N+2`.
  *Sites below:* `s₁ = x₀ − u₂`, `s₂ = s₁ − u₁`, `s₃ = s₂ − u₂`, regarded as beads `−1, −2, −3`.
* `A(x, c₁) ∈ ℤ⁴`: the numbers of pairs `(t_j, x_p)` **at chain separation at least 3** with
  squared distance 3, 8, 11, and `[b′ is a down-bond]`.  `B(x) ∈ ℤ⁴`: the same for the pairs
  `(s_j, x_p)`, last component 0.
* `x` is **clean** if `b′` is an up-bond, `A(x, b′) = 0` and `B(x) = 0`.
* `x¹ ∘_{c₁} x²` is the concatenation of Lemma 11.68: `x¹, t₁, t₂, t₃, φ(x²)`, `φ` the
  height-preserving symmetry with `φ(x²₀) = t₃ + b` that maps `(u₁, u₂)` of `x²` to `(c₁, b)`.
* `q̂(x, c₁) := (h, g)(x) + A(x, c₁) + B(x)`.

(THY-RES-0007 says "no pair within the cutoff between the three linker sites beyond
either end and the chain".  Read literally no bridge satisfies that — `t₁` is bonded to
the last bead; the script `t4_semigroup.py` has the right definition, with the three
chain-neighbour pairs subtracted.  The words "at chain separation at least 3" are
needed.)

### 4.2 Theorem R9.1

**(a) Coboundary [P; exhaustive for `N₁, N₂ ≤ 13`].**  For all bridges `x¹, x²` with at least
three beads and admissible `c₁`, `c₁″`:

    (h, g)(x¹ ∘_{c₁} x²) = (h, g)(x¹) + (h, g)(x²) + A(x¹, c₁) + B(x²),
    B(x¹ ∘ x²) = B(x¹),        A(x¹ ∘ x², φ(c₁″)) = A(x², c₁″).

Hence `q̂(x¹ ∘_{c₁} x², φ(c₁″)) = q̂(x¹, c₁) + q̂(x², c₁″)`: **the error vector of Lemma 11.68 is the
coboundary of `c(x) = A + B`, and `q̂` is exactly additive for all bridges.**

**(b) The sketch [P; exhaustive].**  Clean bridges concatenate with exactly additive
`(h, g)` and the result is clean.  So `Γ := {((h, g)(x); N(x) + 3) : x clean} ⊂ ℤ⁴ × ℕ` is a
semigroup, and so is `Γ̂ := {(q̂(x, c₁); N(x) + 3)} ⊃ Γ`.

**(c) Cleaning [P; exhaustive for `N ≤ 20`].**  For every bridge `x` and admissible `c₁`
the walk `x̂ = (s₂, s₁, x, t₁, t₂, t₃)` — a head of **two** and a tail of **three** beads — is a
clean bridge with `N + 5` beads and `(h, g)(x̂) = q̂(x, c₁)` exactly.  So `Γ̂_M ⊂ Γ_{M+5}`.
`A ≤ (1, 6, 10; 1)` and `B ≤ (0, 3, 4; 0)` componentwise, both attained (first at 21 and at 14
beads).  Two and three are minimal: a head of one bead or a tail of two can fail.

**(d) Exact points and the one-sided rate [P].**  For every bridge and admissible `c₁`,
`q̂(x, c₁)/(N + 3) ∈ K^{br}`; for clean bridges `(h, g)(x)/(N + 3) ∈ K^{br}`.  Hence
`K^{br} = Δ(Γ) = Δ(Γ̂)`, the Newton–Okounkov convex sets of these semigroups, and

    every point of 𝒟_N^{br} lies within 108/(N+3) of K^{br}            (Theorem 11.69 has 168/(N+3)).

**(e) Full lattice [P, by five explicit bridges].**  `Γ` generates `ℤ⁵` as a group, and its
projection `Γ′ = {(h(x); N + 3)}` generates `ℤ⁴`.

**(f) Interior saturation [P].**  For every compact `A` in the interior of `K^{br}` there is
`M₀` such that for all `M ≥ M₀` every integer vector `q ∈ ℤ⁴` with `q/M ∈ A` is the `(h, g)` of a
clean bridge with `M − 3` beads.  The same in `ℤ³` for profiles and the interior of `𝒦`.
Consequently interior points are approached at rate `O(1/N)`:
`dist(p, 𝒟_N^{br}) ≤ (7.5 + 108)/(N + 3)` for large `N`, uniformly on compact subsets of the
interior (Proposition 11.69a gives `277·N^{−1/2}`).

**(g) Counting [P].**  With `P_N^{br}` the set of profiles `h(x)` and `H_N^{br}` the set of
`(h, g)(x)` of bridges with `N` beads,

    lim_N |P_N^{br}| / N³ = vol₃(𝒦),            lim_N |H_N^{br}| / N⁴ = vol₄(K^{br}),

and the same limits for clean bridges.  For all walks:
`vol(𝒦) ≤ liminf |P_N|/N³ ≤ limsup |P_N|/N³ ≤ vol(𝒦₂) = 3.125`, with equality on the left
if Conjecture 11.75 holds.

### 4.3 Proofs

*(a).*  Let `H` be the height of the last bead of `x¹`.  `x¹` lies at heights `≤ H`, the
linker at `H+1, H+2, H+3`, `φ(x²)` at heights `≥ H+4`, so no pair of a bead of `x¹` and a bead
of `φ(x²)` is within the cutoff.  The pairs of the concatenation at chain separation `≥ 3`
are therefore: those inside `x¹`; those inside `φ(x²)` (a lattice symmetry preserves
them); linker–`x¹`, which `A(x¹, c₁)` counts; linker–`φ(x²)`; none inside the linker (`t₁, t₃`
are at separation 2).  Since `φ` maps `(u₁, u₂)` to `(c₁, b)`, the linker is the `φ`-image of
the sites below `x²`: `t₃ = φ(s₁)`, `t₂ = φ(s₂)`, `t₁ = φ(s₃)`, with the same chain separations;
so the linker–`φ(x²)` pairs are counted by `B(x²)`.  The six new torsions have bond triples
`(b′, b, c₁)`, then `(b, c₁, b)` and `(c₁, b, c₁)` alternately: trans except the first, which is
gauche exactly when `b′` is a down-bond (Lemma 11.68).  That is the first line.  The sites
below the concatenation are those below `x¹`, at heights `y₀ − 1, y₀ − 2, y₀ − 3`; the linker
and `φ(x²)` are at heights `≥ H + 1 ≥ y₀ + 3`, at least 4 higher; so `B(x¹ ∘ x²) = B(x¹)`.  The
sites above the concatenation with first bond `φ(c₁″)` are the `φ`-images of the sites
above `x²`; they are at heights `≥ H₂ + 1` where `H₂ ≥ H + 6` is the top of `φ(x²)` (it has at
least three beads), at least 4 above the linker and `x¹`; and the bond before the last
is `φ(b′₂)`, an up-bond iff `b′₂` is.  So `A(x¹ ∘ x², φ(c₁″)) = A(x², c₁″)`.  Adding up gives the
additivity of `q̂`.  ∎

*(b)* is (a) with `A = B = 0`.

*(c).*  The new beads are at heights outside the range of `x`, so `x̂` is a self-avoiding
bridge.  Tail: the pairs `(t_j, x_p)` at separation `≥ 3` are `A`'s; the three new torsions
are `(b′, b, c₁)`, `(b, c₁, b)`, `(c₁, b, c₁)`.  Head: the pairs `(s_j, x_p)`, `j = 1, 2`, are `B`'s —
`s₃` never has one: it is at height `y₀ − 3`, only `x₀` is within three height units, and
`(s₃, x₀)` is at separation 3 across a trans torsion (squared distance 19); the two new
torsions `(u₁, u₂, u₁)`, `(u₂, u₁, u₂)` are trans.  Head and tail are `≥ 4` apart in height.  So
`(h, g)(x̂) = (h, g)(x) + A + B`.  Clean: the sites above `x̂` are `t₄, t₅, t₆` of the same
zigzag, at heights `≥ H + 4`; within three height units they see only `t₁, t₂, t₃`, at
squared distances 3, 8 (separation 1, 2) and 19; the bond before the last is `b`, an
up-bond.  The sites below `x̂` are at heights `≤ y₀ − 3`, and see only `s₁, s₂` and `x₀`, again
in one all-trans zigzag.  The bounds on `A` and `B` are the height counts of Lemma 11.68
(re-counted: `t₁`: `(1, 3, 6)`, `t₂`: `(0, 3, 2)`, `t₃`: `(0, 0, 2)`; `s₁`: `(0, 3, 2)`, `s₂`: `(0, 0, 2)`,
`s₃`: `0`).  ∎

*(d).*  By (a) the `k`-fold concatenation of `x` with itself (with the images of one
`c₁`) has `kN + 3(k−1)` beads and `(h, g) = k(h, g)(x) + (k−1)(A + B)`; its density tends to
`q̂(x, c₁)/(N + 3)`, and limits of densities of bridges with `N → ∞` lie in `K^{br}`.  So
`Γ̂_M/M ⊂ K^{br}`; conversely every bridge is within `O(1/N)` of a point of `Γ̂_M/M`, so
`K^{br}` is the closure of `∪_MΓ̂_M/M` (which is convex: a semigroup), and by (c) of
`∪_MΓ_M/M` as well.  For the rate: `(h, g)/N − q̂/(N+3) = [3(h, g)/N − (A + B)]/(N + 3)`, a
difference of two vectors with nonnegative components; in the cumulative coordinates
in which `‖·‖_c + |·|` is `5|a| + 3|b| + |c| + |g|` the first has `a ≤ 3`, `b ≤ 18`, `c ≤ 36`, `g ≤ 3`
(the box of §11.22, valid for `N ≥ 2` by Proposition 11.73) and the second `a ≤ 1`, `b ≤ 10`,
`c ≤ 24`, `g ≤ 1`; each coordinate of the difference is at most the larger of the two:
`15 + 54 + 36 + 3 = 108`.  ∎

*(e).*  `experiments/science/ws_R9/out/certificate.txt`: clean bridges with 4, 5, 9, 9, 11
beads and `(h₃, h₈, h₁₁, g; N+3) = (0,0,1,1; 7)`, `(0,0,1,1; 8)`, `(0,2,6,5; 12)`, `(0,3,6,4; 12)`,
`(1,6,11,7; 14)`, determinant `1` (exact); for profiles `(0,0,1; 7)`, `(0,0,1; 8)`, `(0,1,3; 10)`,
`(1,6,10; 13)`, determinant `−1`.  Coordinates are in the file; each walk is checked from
coordinates against the `O(n²)` definition.  ∎

*(f).*  (Self-contained; the general statement is Theorem 1.6 of Kaveh–Khovanskii as
read by A2.)  `∪_MΓ_M/M` is dense in `K^{br}`, which has interior points (the 9-bead
clean bridge `(0,2,6,5)` gives the exact point `(0, 1/6, 1/2, 5/12)` off the hyperplane
`g = 9p₃ − 3p₈ + p₁₁` that contains the four exact points of Proposition 11.72(d)).  Cover
`A` by finitely many open simplices with vertices in `∪_MΓ_M/M`, and let `v₁, …, v_k ∈ Γ` be
these vertices' elements together with the five of (e); `Γ₀ ⊂ Γ` the semigroup they
generate, `C₀` its cone.  *Khovanskii's lemma:* every integer point of `C₀` at distance at
least `n₀|Σv_i|` from the boundary of `C₀` is in `Γ₀`, where `n₀` bounds the absolute values of
the integer coefficients in fixed representations `z = Σn_i(z)v_i` of the finitely many
integer points `z` of the zonotope `{Σt_iv_i : 0 ≤ t_i < 1}` (they exist because the `v_i`
generate `ℤ⁵`).  Indeed `x − n₀Σv_i = Σμ_iv_i` with `μ_i ≥ 0`, and `x = Σ(n₀ + ⌊μ_i⌋ + n_i(z))v_i`
with `z = Σ{μ_i}v_i`.  Points `(q; M)` with `q/M ∈ A` are at distance `≥ cM` from the boundary
of `C₀`, `c > 0`.  The rate: the integer point nearest to `Mp` is within `7.5` of it in the
norm, and passing from `M` to `N = M − 3` costs at most `3R/M`.  ∎

*(g).*  Lower bound: (f) gives all integer points of `M·A`, about `vol(A)M^d` of them;
let `A` exhaust the interior.  Upper bound: by (c) every `(h, g)(x)` is `q − c` with
`q ∈ Γ_{N+8} ⊂ (N+8)K^{br}` and `c` in the box `[0,1]×[0,9]×[0,14]×[0,1]`, and the number of
integer points in `tK + (bounded set)` is `vol(K)t^d + O(t^{d−1})` for a convex body `K`.
For walks: bridges are walks; the outer polytope holds for every walk up to `O(1)` (the
reviewer's N5).  ∎

### 4.4 Checks (own code; `r9_semi.c`, `r9_cobound.c`, `r9_lat.py`, `r9_long.py`)

`r9_semi.c` was written from the Setting paragraph and the statement of Lemma 11.68,
before opening R2's `r2_concat.c` (which I did not open at all); I had read the theory
division's `mylat.py`, `concat_check.py`, `t4_semigroup.py`.  Profiles are counted by the
definition (all integer vectors of squared norm 3, 8, 11; pairs excluded by index, not by
a formula) and cross-checked against an `O(n²)` double loop.

| check | size | result |
|---|---|---|
| my enumeration against R2's | bridges with 3–22 beads (92 121 332 at `N = 22`) | numbers of bridges, profile classes and sets of gauche counts identical to R2's tables for every `N` |
| clean bridges per `N` against the theory division's script | `N ≤ 10` | `1, 2, 4, 10, 24, 64, 159, 420` = theirs divided by 4 (they do not fix the first two bonds) |
| (c): head 5 + tail 5 (their claim) | all 21 220 319 pairs `(x, c₁)` with `N ≤ 20`, built from coordinates | always a clean bridge; cost `= A + B`; componentwise maxima `(1, 8, 12; 1)`, norm 51 |
| (c): head 2 + tail 3 | the same | always clean; `(h, g) = q̂` exactly (asserted for `N ≤ 13`, 18 709 cases) |
| minimality | the same | head 1 + tail 3 fails from `N = 8` on (2 cases; 345 738 at `N = 20`); head 2 + tail 2 from `N = 12` on (4 cases; 92 570 at `N = 20`); head 0 or tail 0 fail |
| (b): real concatenations of clean bridges | **all 160 326 244 ordered pairs** with `N₁, N₂ ≤ 13` (12 662 clean bridges) | self-avoiding, bridge, `(h, g)` exactly additive, clean: no failure of any kind |
| (a): real concatenations of arbitrary bridges | **all 350 026 681 ordered pairs** of (bridge, `c₁`) with `N₁, N₂ ≤ 13` | error `= A(x¹, c₁) + B(x²)`; both ends inherited; `q̂` additive: no failure; error maxima `(1, 6, 8, 1)`, norm 41 = R2's |
| set level | clean classes, all `N₁ + N₂ + 3 ≤ 22` | `C_{N₁} + C_{N₂} ⊂ C_{N₁+N₂+3}`: 24 913 sums, none missing; for all bridges 79 of 47 038 sums are missing — exact additivity of `(h, g)` itself needs clean ends |
| random long bridges | 787 bridges cut out of random walks with dense ends (79 with ≥ 1 000 beads, longest 3 970); 360 clean as they stand | cleaning works for all; 1 500 concatenations (up to 7 873 beads): (a) in all, (b) in the 250 clean pairs; 25 six-fold self-concatenations: `(h, g) = 6(h, g) + 5(A + B)` |
| special bridges | rod and helix up to 1 001 beads | both are clean |

### 4.5 What follows

**Is `K^{br}` the Newton–Okounkov body of an honest graded semigroup?**  Yes, of two:
`Γ` (clean bridges, `(h, g)` itself) and `Γ̂` (all bridges, `(h, g)` plus its end
correction), graded by `N + 3`, with `Γ̂_M ⊂ Γ_{M+5}`.  The answer to A2's question is
stronger than the sketch: no restriction of the family is needed, only a change of
bookkeeping — which the theory division had half-seen ("the error is a term that depends
on `(x¹, c₁)` only plus a term that depends on `x²` only", lines 5233–5234) without noting
that the concatenation inherits its ends.

**Does `β = 60` disappear?**  For `Γ` and `Γ̂` the error is zero.  For the densities
`(h, g)/N` of arbitrary bridges the one-sided rate improves from `(β + 3R)/(N+3) = 168/(N+3)`
to `3R/(N+3) = 108/(N+3)`: what remains is the normalisation.  `β = 60` itself is sharp as a
bound on the concatenation error: it is attained with `N₁ = 21`, `N₂ = 14`, hence for all larger
sizes (a head added to `x¹` or a tail added to `x²` does not change the end that matters).  Practical gain for
the numbers of §11.22.  *Without coordinates* (`r9_inner_volume.py`): each explicit bridge
gives a point of `𝒦` within `29.5/(N+3)` of `(h + (½, 9/2, 7))/(N+3)`, so the proved inner volume
rises from `1.5632` to `1.6192`.  *With coordinates* (`r9_witness_ends.py`): I re-generated the
ten bridges with the authors' builder (`experiments/workstreams/S/code/build.py`, their
code) and verified them with mine — lattice walk, self-avoidance, bridge, the stored
counts `(N, h₃, h₈, h₁₁, g)` reproduced exactly — and computed their end corrections: **nine
of the ten are clean as built (`A = B = 0`), the W3 woodpile has `A = (0, 0, 1; 0)`**; for each,
head 2 + tail 3 is a clean bridge with `(h, g) + A + B`.  So all fourteen vertices of the
packings are *exact* points of `K^{br}` after the change `(h, g)/N → q̂/(N+3)`, and
(`r9_exact_packing.py`): **R2's four packings satisfy `L‖p_k − p_l‖_c > e(g_k + g_l) + 2ε₁` with all
radii zero** (exact rationals; smallest margins `2.2·10⁻³`, `1.3·10⁻³`, `2.5·10⁻²`, `5.6·10⁻³`,
larger than before), and **`vol 𝒦 ≥ 1.6313`** — the volume of the hull of the fourteen exact
profile points, no erosion (`1.631346`; exact rational sum over the cones of the 18 facets,
facet list from Qhull) — in place of `1.5632`.  A new search for packings on the exact
vertices should add points to 116 and 451; not run.

**Does the prediction become a theorem?**  For bridges, yes — (g): the number of
attained profiles is `vol(𝒦)·N³(1 + o(1))`, the index of the generated lattice being 1;
likewise `vol₄(K^{br})·N⁴` for `(h, g)`.  For all walks it is a theorem that
`liminf |P_N|/N³ ≥ vol(𝒦)` and `limsup ≤ 3.125`; equality with `vol(𝒦)` is Conjecture 11.75
in another guise.  The convergence in (g) carries no rate: `M₀` in (f) is not effective
as proved, and the surface law says the approach is slow.

**The test on R2's tables** (`r9_semigroup_analysis.py`; bridges with 3–24 beads; my own
tables agree with R2's for `N ≤ 22`):

| `N` | profiles | `/N³` | local exponent | lattice points of the hull | attained | deepest hole |
|---|---|---|---|---|---|---|
| 12 | 101 | 0.058 | 5.2 | 109 | 0.927 | 0.26 |
| 16 | 379 | 0.093 | 4.7 | 424 | 0.894 | 0.59 |
| 20 | 1 070 | 0.134 | 4.8 | 1 172 | 0.913 | 0.76 |
| 22 | 1 617 | 0.152 | 4.2 | 1 778 | 0.909 | 0.84 |
| 24 | 2 350 | 0.170 | 4.4 | 2 565 | 0.916 | 0.93 |

(i) `|P_N|/N³` reaches `0.17` at 24 beads against `vol 𝒦 ≥ 1.56` (now `≥ 1.63`): the count is at
most a ninth of its asymptote, the local exponent is still above 4 and falling.  **The
tables cannot test the constant**; they are consistent with convergence from below, as
the surface law (`N^{−1/3}`) predicts.  A2's own plausibility estimate said as much.
(ii) What the theorem predicts *and the tables can show*: no arithmetic obstruction (the
generated lattice has index 1 already with bridges of at most 10 beads), and
saturation — at every `N ≤ 24` every lattice point of the convex hull of the attained
profiles that lies deeper than `0.93` (Euclidean) inside it is attained; the holes — 8–10 %
of the lattice points of the hull for `N ≥ 17`, up to 15 % below — all sit in the boundary layer.  **[N]**  (iii) A
homothetic-shrinkage reading `|P_N| ≈ vol(𝒦)N³(1 − kN^{−1/3})³` with R2's `k ∈ [1.71, 1.86]` would
give `vol 𝒦 ≈ 2.5–3.8` at `N = 24`; it is a heuristic **[H]**, its upper end exceeds the proved
`3.125`, and I do not offer it as an estimate.

---

## 5. Item 5 — what became worse

Nothing became false in a theorem, no number changed without a stated reason (all
removed numeric tokens of the word diff in §§11.22–11.26 were listed with
`r9_numdiff.py` and read), and no cross-reference I followed is wrong (harness labels
XIV.5, XX.5, XXI.5, XXI.6, XXII.5, DEAD.25, DEAD.27 exist; `lower_end_any` is in
`SliceRefinement.lean`; the check directories exist).  What I found:

1. **Lines 5282–5284, false as stated (new text).**  "At the boundary the abstract
   hypotheses give no rate (for `d = 1`, where the limit is a point, a super-additive
   sequence can converge arbitrarily slowly)".  Under (C) as stated — `|q − q₁ − q₂| ≤ β`,
   two-sided — a family of single points `Q_M = {a_M}` satisfies
   `|a_{M₁+M₂} − a_{M₁} − a_{M₂}| ≤ β`, and then `|a_M/M − lim| ≤ β/M`: when the limit is a point,
   Theorem 11.69's own one-sided estimate is a two-sided rate.  The claim outside the
   parentheses is true; the example must have a limit with a boundary:
   `Q_M = [0, a_M] ⊂ ℝ` with `a_M` super-additive and nondecreasing satisfies (C), (E), (B)
   with `β = β′ = 0`, its limit is `[0, sup a_M/M]`, and the right end point is approached as
   slowly as one likes (`a_M = M − M/ln(M + 2)`).
2. **Line 5371 against 5394–5395.**  The text says the proved 8 "cuts the estimate `7–10`
   of the sixth column to `8–10`"; the cell still reads `7–10`.
3. **Line 1444 (row G27).**  "harness XXI.1–4 with 21 mutations" — the section has XXI.1–6
   with 28 (lines 6801–6802, 7275).
4. **Lines 1380, 6473, 6679.**  "adopted unchanged" — see §3.4.
5. **Lines 3120–3124 (Theorem 11.36, rewritten for M4).**  `Ī(m)` is called "the largest
   moment of inertia of an arm of `m` atoms", and the limit an equality.  What workstream
   G proves is an upper bound `Σd̄(p)²` and its asymptotic attainment numerically.  For the
   tetrahedral angle the kinked arm is exactly perpendicular to the axis and the
   equality is a proof; for `θ = 111°` the one-kink arm stays `0.1 %` below (own
   computation), and that longer prefixes close the gap is numerical.  The label "[P for
   the verified constants]" is right if `Ī` is G's bound, which is what `c_i^ver` is.
6. **Lines 7445–7449.**  "with `c` and `n₀` depending on `(m, q_max, D_max, π_min)`" — the proof
   gives `c` explicitly (§3.1); worth one line.
7. **THY-MSG-0013, line 19, and `DEAD_ENDS.md` D55, line 1605: "No theorem was found
   false."**  Clause (ii) of Theorem 11.84 as published was false as stated — our review's
   title and verdict table say so, and D55 item 1 itself describes it.  Accurate would
   be: "no exponent, no inequality between exponents and no machine-checked statement
   was found false; one clause of the statement of Theorem 11.84 was".
8. **THY-RES-0007 §1.3** (not in the report): the definition of clean ends as worded is
   never satisfied (§4.1); "a head and a tail of five beads" — two and three suffice and
   are minimal.
9. **`Scattering.lean`, line 219:** the docstring of `one_sub_sinc_le` announces sharpness;
   the theorem is the inequality only (§3.3).

---

## 6. Findings classified, with replacement texts

**Critical (a published statement is false).**

* **C1 (theory report, line 5283–5284; no consequence).**  Replace the parenthesis by:
  "(for `d = 1` take `Q_M = [0, a_M]` with `a_M` super-additive and nondecreasing: the limit
  is the interval `[0, sup a_M/M]`, whose right end point is approached as slowly as one
  likes; for families of single points the limit is a point and (C) gives the rate
  `β/M`)".
* **C2 (ours; corrected by SCI-RES-0007 §2).**  SCI-REV-0006 M4.  Addendum text: §2.4.

**Major.**

* **M1 (ours).**  The replacement text of SCI-REV-0001 M1, clause "and without a field
  these two exponents are the uniform cube's": false beyond the junction by the
  reviewed report's own Proposition 11.81(b).  Read: "and without a field and with one
  phase (a symmetric convex rate function: `B = 0` and `βJ ≤ 1`, every antiferromagnet)
  these two exponents are the uniform cube's".  The theory division has it right.

**Minor — theory text** (numbers refer to §5): 2, 3, 4, 5, 6, 7, 8, 9.  Replacement texts:

* (2) cell of line 5371: `8–10`.
* (3) row G27: "harness XXI.1–6 with 28 mutations (before the review: XXI.1–4 with 21,
  profiles with more than two blocks at nonnegative accuracies only)".
* (4) "its declarations unchanged (a provenance paragraph added to the header; the four
  `#print axioms` moved to `AxiomAudit.lean`)".
* (5) "`Ī(m) := Σ_{p≤m}d̄(p)²`, the bound of workstream G §2.1(c) for the moment of inertia
  of an arm of `m` atoms about the torsion axis — attained asymptotically; exactly so for
  the tetrahedral angle, numerically for `θ = 111°`".
* (6) add: "`c` may be any number above `m·[q_max e^{D_max}/π_min + ln(1/π_min)]/(2 + m·q_max)`".
* (7) as quoted in §5.
* (9) docstring: "the case `a = 0` of `abs_sinc_sub_le`; that the constant `1/6` cannot be
  lowered is not formalised".

**Minor — ours.**

* `R4_REPORT.md` line 286, "equals the printed `E` to four digits" — §2.2.
* `R5_REPORT.md` §4.6 (G1), `m/((1−φ)|𝐧|)` → `2m/((1−φ)|𝐧|)` — §2.3(a).
* SCI-REV-0001 m3 and `R1_REPORT.md`: "`0.1439` against `0.0201`" → "`0.1441` against `0.0202`"
  (`0.144080`, `0.020200`).
* SCI-REV-0006 M3 and `A2_REPORT.md` A2.3: "`k ≥ 0.69`" rounds `0.68976` upwards; "`k ≥ 0.689`".
* `A2_REPORT.md` A2.1: "a member of the pair-additive class … with radial function
  `sinc(q√s)`" needs "after subtracting the constant `sinc(q√S_c)` per pair, with `S_c` the
  largest possible squared distance" (the class requires `φ(s) = 0` for `s ≥ S_c`).
* `A2_REPORT.md` lines 40, 286–288, 645, 661, 739 — part of C2.
* SCI-RES-0007 §1: "our text was written against `5ed4072`" accounts for the second
  amendment of §2.1 only; the first corrects a slip that was a slip at `5ed4072` too.

---

## 7. Numerics: what, sizes, how to re-run

From `experiments/science/ws_R9/` (gcc; Python 3.13 with numpy, scipy, sympy; nothing
outside the directory is written; R4's module is imported with bytecode writing off).

| script | what | size | time |
|---|---|---|---|
| `gcc -O3 -march=native -o bin/r9_semi r9_semi.c`; `bin/r9_semi 22 0 20 out` | enumeration, clean flags, cleaning tests from coordinates, class tables `out/r9_tab_N*.txt` | 3–22 beads | 7 min |
| `bin/r9_semi 13 13 0 out 0 2`, `… 1 2` | all pairs of clean bridges | `1.6·10⁸` pairs | 2 × 3.2 min |
| `gcc … -o bin/r9_cobound r9_cobound.c`; `bin/r9_cobound 13 0 2`, `… 1 2` | all pairs of arbitrary bridges: coboundary identities | `3.5·10⁸` pairs | 2 × 6.3 min |
| `r9_semigroup_analysis.py` | tables against R2's; set-level closure; generated lattice; counts, hulls, holes | — | 1 min |
| `r9_long.py`, `r9_certificate.py`, `r9_head2.py` | long random bridges; the unimodular certificate; head 2 + tail 3 | — | 1 min, 20 s, 2 min |
| `r9_packing_volume.py`, `r9_inner_volume.py` | packings (exact), volumes, arithmetic of §11.22; improved inner volume | — | 10 s |
| `r9_witness_ends.py 64`, `r9_witness_ends.py 128 "12/5"`; `r9_exact_packing.py` | the ten explicit bridges re-generated (authors' builder), verified, end corrections; packings and hull volume on exact vertices | 12 041 – 166 199 beads | 2 min, 1.5 min, 10 s |
| `r9_Eprime.py` | `E′` against `E` with R4's `twins_exact.py` | 8 rows | 4 min |
| `r9_sites.py`, `r9_sites2.py`, `r9_chi2_check.py` | site functions with duality brackets; ceiling; `χ²` step | — | 3, 9, 1 min |
| `r9_minor.py`, `r9_slices.py`, `r9_m1_input.py`, `r9_lever.py` | sampled minor findings; Theorem 11.90(a) at `e < 0`; the lever-arm constants | — | 1–4 min each |
| `r9_diffview.py LO HI`, `r9_numdiff.py LO HI` | compact word diff of the theory report between `dcdfea6` and `658b77f` | — | seconds |
| `lean/*.lean` | scratch copies; `lake env lean <absolute path>` from the repository root | 2 files | 1–2 min |

Outputs are in `out/` (and `lean/out_*.txt`).  A false alarm of mine is recorded in
`NOTES.md` (step 9): a tolerance below the grid resolution in `r9_chi2_check.py` reported
93 "violations", all at points inside the window.

## 8. Sources and reading levels

* Kaveh–Khovanskii, *Newton–Okounkov bodies, semigroups of integral points, graded
  algebras and intersection theory*, Ann. of Math. 176 (2012): **[not read by me]**; cited
  through A2's reading (`A2_REPORT.md` §4.6: statement of Theorem 1.6 in full text).
  Theorem R9.1(f) does not depend on it: the proof in §4.3 is self-contained.
* Khovanskii's lemma for finitely generated semigroups: **[from memory — the proof is
  written out in §4.3 and is three lines]**.
* The number of lattice points of `tK + B` for a convex body: **[standard; from memory]**
  (each lattice point carries a unit cube inside `tK + B + [0,1]^d`, whose volume is a
  polynomial in `t` with leading coefficient `vol K`; a lower bound in the same way).
* Everything else is internal: the export, our five reviews and reports,
  `docs/workstreams/G_REPORT.md`, `W_REPORT.md`, `U_REPORT.md` (errata read).

No new prior-art search was made.  Whether "the concatenation error of bridges is a
coboundary" is in the literature on bridges of self-avoiding walks I do not know; the
classical concatenation arguments for bridges (Hammersley–Welsh type) are about counts,
not about an additive statistic with a cutoff **[H]**.

## 9. What I did not settle

* An effective `M₀` in (f) — hence a finite-size statement, and a rate in (g).
* Whether the interior saturation holds with a boundary layer of bounded width (the
  holes at `N ≤ 24` suggest it: depth below one lattice unit).
* Larger packings on the exact vertices (the existing ones are re-verified with zero
  radii; no new search was run), and an exact-arithmetic facet list for the hull volume
  `1.6313`.
* Walks: (g) for walks is Conjecture 11.75.
* Anything about what a proof of Theorem 11.64 needs for Proposition 11.81(c) (§2.1).

## 10. The three most promising next steps

1. **State Theorem 11.69 as a Newton–Okounkov body with exact points,** and re-run the
   packing search on the exact vertices (`out/witness_ends_W64.json`,
   `out/witness_ends_W128_only.json`): the bracket for the limit points tightens at no
   cost; `vol 𝒦 ≥ 1.6313` is already there.
2. **Make the saturation effective.**  With explicit generators (lamellae, helix, rod,
   the certificate bridges) Khovanskii's constant is computable; that would turn (f)
   into "every profile at depth `≥ D` in `(N+3)𝒦` is attained for all `N`", and with it the
   count of profiles into a two-sided bound at finite `N`.
3. **Use the semigroup for the covering numbers.**  The exceptional accuracies of
   Theorem 11.71(a) are jumps of `N_∞`; with exact points on both sides of a candidate
   jump one can try to prove that `ε₁ = ½` is not exceptional — the open item (a0) of §12.

## 11. Requests

**To the theory division.**

* **R9-T1.**  Adopt Theorem R9.1 (or refute it): the coboundary identity, the semigroups
  `Γ` and `Γ̂`, `108/(N+3)`, interior saturation, the two counting limits.  Statement and
  proofs: §4.2–4.3; the precise definition of clean ends: §4.1.  A Lean statement of (a)
  needs the lattice; the abstract half of (f), (g) (a semigroup that generates the
  lattice attains every lattice point of a compact part of the interior of its cone
  far enough out) does not, and would sit next to `SetLimit.lean`.
* **R9-T2.**  Correct line 5283–5284 (C1) and the minor points 2–7, 9 of §5.
* **R9-T3.**  In Theorem 11.97(c) state the constant of §3.1, and say that `q_max/M` enters
  through the chain-rule defect alone.
* **R9-T4.**  In Proposition 11.81(c) say what is used of Theorem 11.64 when the
  confidence is divided by the number of grid fields.

**To the engineering division** (a request is not an authorisation).

* **R9-E1 (packings on exact vertices; supersedes part (ii) of the request in
  SCI-REV-0002 §8).**  *Motivation:* §4.5 — the explicit bridges are exact points of
  `K^{br}` once their end corrections are added.  *Formulation:* (i) for the witness
  bridges in boxes of side 64, 96, 128, 160: from coordinates the vectors `A(x, c₁)`, `B(x)`
  of §4.1 and `q̂/(N+3)`; (ii) the maximum packing problem
  `L‖p_k − p_l‖_c > e(g_k + g_l) + 2ε₁` in the 4-dimensional hull of the exact points, on a grid of
  step `ε₁/(4L)`, by integer programming with a certified bound, at the four pairs `(L, ε₁)`.
  *Validation:* `experiments/science/ws_R9/r9_witness_ends.py` gives `A = B = 0` for nine of
  the ten bridges of box 64/128 and `A = (0, 0, 1; 0)` for the W3 woodpile;
  `r9_exact_packing.py` gives 116, 451, 8, 19 with R2's weights — the result must be at
  least that.  *Stop:* optimality gap below 10 % or one hour per instance.  Minutes for
  (i); (ii) as in SCI-REV-0002.
* **R9-E2 (saturation at larger sizes).**  *Motivation:* §4.5 (ii).  *Formulation:* from
  the class tables of bridges (your enumeration, or R2's up to 24 beads) the lattice
  points of the convex hull of the attained profiles that are not attained, with their
  depth inside the hull, for `N` as large as the tables go.  *Validation:*
  `r9_semigroup_analysis.py` gives 215 holes of 2 565 lattice points at 24 beads, deepest
  `0.93`.  *Stop:* the largest `N` with a table.  Minutes.

---

## What I did not check

* **Theorems taken as given:** 11.52, 11.56 (read for its good event only), 11.58, 11.64,
  11.65(b), 11.78, 11.79, 11.80, 11.98(a), (b); Lemma T′ was read with its proof
  (`W_REPORT.md` 362–380) but the proof of Theorem 11.78(b) that it serves was not
  re-derived.  My verdict on Theorem 11.97(c) is: every step that *changed* is right.
* **§§11.27–11.29** and their changed hunks (they answer SCI-RES-0005/-0006, not the
  five reviews); **the harness** (`experiments/falsify_conjectures.py`) and the mutation
  runner — I checked that the cited test labels exist, nothing more; **the theory
  division's check scripts** — read (`limit_shape_review/`), not re-run.
* **Minor findings not followed into the text:** SCI-REV-0005 m5, m11, m12 (errata of
  `W_REPORT.md`); for SCI-REV-0006 the wordings W1–W10 were read in the word diff, the
  sources behind them were not re-read.
* **The reviewer's finite-`N` certificates N5** — not re-derived by them, nor by me.
* **Exactness:** the volumes `1.5632`, `3.125`, `1.6192` are floating point (Qhull);
  the packings and the certificate determinants are exact; the lattice checks are
  integer arithmetic.  Site functions carry duality brackets of at most `10⁻¹²`.
* **The ten explicit bridges** were re-generated with the *authors'* builder (I did not
  read `build.py`); what is mine is the verification from coordinates and the end
  corrections.  The hull volume `1.6313` uses Qhull's facet list (floating point) with
  exact arithmetic on it.
* **Lean:** the two files were compiled from scratch copies with `lake env lean`
  against the oleans present in the repository (built at `5ed4072`); no `lake build`.
  I did not compile `AxiomAudit.lean` or `SliceRefinement.lean`.
* **`lake env lean` on `TwoRoundsExpected` uses the stored olean of `TwoRounds`**; that the
  olean matches the source is assumed (the source is byte-identical to `5ed4072`).
* **Prior art** for the coboundary observation: no search.
