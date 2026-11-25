# Workstream R9 — running notes

(started 2026-11-25 23:33 UTC; one entry per step; newest at the bottom)

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

### 23:35 — first reading (read only)
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

### 23:40 — item 4: definition of "clean" extracted from their script; own code written
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

### 23:55 — §11.25 (slices) read in full in the export (lines 6785–7280); SCI-REV-0001 read in full
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
