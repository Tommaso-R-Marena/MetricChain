# Workstream L3 — Lean: Lemmas 0–3 and Theorem A of workstream F, complete; Lemma A16.5 given Harper; Proposition A1.1, items 1–2

*Lean 4.31.0 + Mathlib (the repository's pinned version, `v4.31.0`, commit `fabf563a`).  Four files
in `experiments/science/ws_L3/`; running log `NOTES.md` (clock readings); numerics `sanity_numerics.py`;
last full check `check_log.txt` (re-run with `bash experiments/science/ws_L3/check_all.sh`).
Sources formalised: `docs/science/workstreams/SF_REPORT.md` §2.0–§2.2 (setting, Lemmas 0–3, Theorem A);
`docs/science/INFERENCE_LIMITS_ADDENDA.md`, Lemma A16.5; `docs/science/workstreams/A1_REPORT.md` §2.5
(Proposition A1.1, items 1–2).*

Labels: **[V]** machine-checked here (declaration named; the file compiled with exit code 0 in my own run)
· **[P]** paper proof (by whom is said) · **[N]** numerical only · **[K]** known.

**What [V] means in this file.**  The declaration is in the named file; the file was compiled on its own with

    export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH"; cd /home/user/MetricChain; lake env lean <absolute path>

exit code 0, no error, no warning; `#print axioms` is run at the end of each file for every headline
theorem, and no line lists an axiom other than `propext`, `Classical.choice`, `Quot.sound` (90 of the
91 lines list exactly these three; `addRight_fin_val` lists `propext`, `Quot.sound`) (§ Appendix).  No `sorry`,
`admit`, `native_decide` or `axiom` occurs in any file.  Nothing was written outside
`experiments/science/ws_L3/` and this report; no state-changing git command; `lake build`, `lake update`,
`lake clean` were never run.  All declarations are in the namespace `ScienceL3` (`ScienceL3.A16`,
`ScienceL3.Chain` for items 5 and 6).

What kind of check this is: I re-derived the paper proofs of Lemmas 0–3 and Theorem A by hand
(*independent review*), tested the **formal statements as I state them** — they are more general than
the paper's — on small instances with my own code (§3; this is not a replication of workstream F's
numerics), and then proved them in Lean.

---

## 1. Verdicts

**Lemmas 0, 1, 2, 3 and Theorem A of SF_REPORT §2.1–§2.2 are machine-checked in full — every part of
the four lemmas and all three displays of Theorem A — with no statement of the report taken as a
hypothesis, and nothing in §2.0–§2.2 was found false.**  (Not formal: side remarks only — that at a
cone "one evaluation certifies `ln A`", that `J` is exponentially small, Remarks (2), (3) of Lemma 3,
which are comments.)
(1) **Lemma 3 (compensation) is [V]**, in a form more general than the paper's: any positive reference
weight invariant under any *set* of site permutations that is transitive on the sites (no group
structure is used), any normalised invariant class member as compensator; the report's form
(Bernoulli reference, compensator `w̃_{γ₂}`) is a corollary.  The linear equation holds site by site with
no sign condition and no invariance at all (`oneW_compensated`).
(2) **Lemma 1 is [V]**, (a) and (b), in the oracle-indexed model of workstream L1, for an arbitrary
oracle, class and target, by reduction to the theory division's
`MetricChain.expected_queries_ge_packing` and `MetricChain.nonadaptive_expected_queries_ge`.
(3) **Lemma 0 is [V]**, all three sentences: the window — for marginals and, more generally, for every
conditional law given any pattern on any set of other sites (item 1 of Proposition A1.1), and for any
reference weight with Bernoulli odds at the site; the additive instances fill the window; rigidity at
a cone.
(4) **Lemma 2 is [V]** (both bounds proved, not assumed), in an abstract form — two arbitrary
probability vectors, any observable with values in `[0,1]` — and for the dips of the report, with a
site-by-site version that the report does not state.
(5) **Theorem A is [V]**: `E|Q(ψ₀)| ≥ (1 − 2δ)/(n·H_{k,r})` (`theoremA_fin`); the Chernoff form
`H_{k,r} ≤ (n+1)·e^{tr}·ρ_t(k/n;γ)ⁿ`, hence `E|Q(ψ₀)| ≥ (1 − 2δ)e^{−tr}ρ_t(k/n;γ)^{−n}/(n(n+1))` for every
`t ≥ 0` (`Hkr_le_chernoff`, `theoremA_fin_chernoff`); and the last display with `C_m`, at one instance
that does not depend on `t` (`theoremA_fin_Cm`).  All of it also for sites indexed by any finite group
acting on itself by translation (`theoremA_group…`), of which the cyclic shifts of `{0,1}ⁿ` are the case
`Fin n`.
(6) **Lemma A16.5:** workstream R8 had already machine-checked the algebraic core that the brief lists
((a)–(d)); I did not redo it.  I added the step R8's report names as missing — **the rearrangement step
with Harper's theorem as an explicit hypothesis** — and with it **Lemma A16.5 itself, conditional on
Harper's inequality and on the level** (`A16.lemmaA16_5_of_harper`), plus concavity of `f_η`, the
maximiser for every level (hills included) and the case `η = 0`.
(7) **Proposition A1.1, items 1 and 2, are [V]**: item 1 as `condMarg_mem_window`; item 2 —
`KL(ν_ψ ‖ Bern(r)ⁿ) ≤ n·max{KL(a₀‖r), KL(a₁‖r)}`, equality at the two cones, and "this is the supremum
over the class" — as `Chain.a1_item2_lip`, `Chain.a1_item2_cone0/1`, `Chain.a1_item2_isGreatest`, on top
of workstream L2's general chain rule.

**Findings** (details in §2.9).  *No numbered statement is false.*  Four points where the text is not
exact: (F1) Remark (1) after Lemma 3 says compensation by class members is possible "iff
`c_Δ ∈ [p₋, p₊]`"; at the two ends it is **not** possible when `c_Δ ≠ c_w` — the correct interval is
the open one **[V]** (`no_compensation_at_upper_end`, `no_compensation_at_lower_end`; "only if" and "if on
the open window" are [V] too).  (F2) In Theorem A the proof gives `1 + b ≤ β`, not just `b ≤ β`, so the
accuracy threshold improves from `ln(1 + (e^r − 1)/(1 + β))` to `ln(1 + (e^r − 1)/β)` **[V]**
(`theoremA_group_sharp`).  (F3) The hypotheses `u > 0`, `n ≥ 2`, `1 ≤ k ≤ n − 1` of Theorem A are
redundant for its first two displays (they follow from `|γ| ≤ u`, `r > 0`, `k ≤ n` and
`(e^r − 1)ω_m > 1`); `r > 0` and `k ≤ n` are not.  (F4) In the last step of the proof of Theorem A
("`r = ln(1 + max{…}) + η`, `η ↓ 0`") the instance `ψ₀` depends on `η`, so the limit does not give the
displayed bound at one instance; the display is nevertheless true as stated, with the explicit depth
`e^r = C_m e^ε` **[V]** (`theoremA_fin_Cm`).  In Lemma A16.5 the plateau needs only `φ(t_pl) ≥ 0`, not
`= 0` **[V]**.

## 2. Statements

### 2.0 Files and imports

| file | lines | theorems | imports | content |
|---|---|---|---|---|
| `Compensation.lean` | 1 948 | 119 | **Mathlib only** | the cone `𝒲_u` and the class `L_u`; Lemma 3 (i), (ii) and its Remark (1); Lemma 0 complete, also for conditional laws (A1.1 item 1); Lemma 2 |
| `TheoremA.lean` | 3 408 | 169 | Mathlib + the theory division's `proofs.Frontiers.QueryLowerBound` and `proofs.Frontiers.NonAdaptive` (read-only: `MetricChain.QueryAlgorithm`, `expected_queries_ge_packing`, `nonadaptive_expected_queries_ge`) | Parts 1–6 = `Compensation.lean` verbatim; Part 7: Lemma 1 (a), (b); Part 8: the family of alternatives; Part 9: Theorem A, first display; Part 10: Chernoff form; Part 11: last display |
| `A16Rearrangement.lean` | 344 | 22 | **Mathlib only** | Part 0 = the needed declarations of R8's `A16Core.lean`, verbatim; Part 1 (new): rearrangement, Lemma A16.5 given Harper |
| `ChainRuleCube.lean` | 655 | 34 | **Mathlib only** | Part 0 = L2's chain rule (`ws_L2/Window.lean`, lines 69–93, 421–757), verbatim; Part 1 (new): A1.1 item 2 |

**Paper statement → Lean declaration** (details and differences in §2.2–§2.8):

| paper statement | headline declaration(s) | file |
|---|---|---|
| SF §2.0: `ψ ∈ L_u ⟺ e^{−ψ} ∈ 𝒲_u`; `𝒲_u` closed under `+`, positive multiples, max, min | `lipH_iff_inCone`; `InCone.add`, `InCone.smul`, `inCone_max`, `inCone_min` | `Compensation` |
| Lemma 0, window | `lemma0_window_lipH` (`window_of_site_odds_nonneg`) | `Compensation` |
| Lemma 0, additive instances fill the window | `lemma0_additive_fill` | `Compensation` |
| Lemma 0, rigidity at a cone | `lemma0_rigidity_lipH` | `Compensation` |
| Lemma 1 (a) | `lemma1a` (`lemma1a_weighted`, `lemma1a_div`, `oracle_packing_weights`) | `TheoremA` |
| Lemma 1 (b) | `lemma1b` (`lemma1b_weighted`) | `TheoremA` |
| Lemma 2, `e^r − 1 ≤ E_{k,r} ≤ e^r` | `lemma2_mass` (`excess_mass_bounds`) | `Compensation` |
| Lemma 2, `|c_{k,r} − c₀(k/n)| ≤ 1/(e^r − 1)` | `lemma2_dens`, `densW_coneW` (`excess_mean_bound`; site by site: `lemma2_site`) | `Compensation` |
| Lemma 2, "depend on `(k,r)` only"; the dip is in the class; `D_{s,r}` | `massW_densW_dipW_of_wt_eq`; `baseW_add_dipW_inCone`; `dipW_pos_iff` | `Compensation` |
| Lemma 3 (i) | `lemma3_i` (`margW_eq_densW`, `margW_add`) | `Compensation` |
| Lemma 3 (ii) | `lemma3_compensation`, `lemma3_compensation_bernoulli` (`oneW_compensated`, `massW_compensated`) | `Compensation` |
| Lemma 3, Remark (1) | `window_of_equal_marginals`, `lemma3_compensation_exists`, `no_compensation_at_upper_end`, `no_compensation_at_lower_end` | `Compensation` |
| Theorem A, first display | `theoremA_fin` (`theoremA_group_sharp`, `theoremA_group`, `theoremA_group_div`) | `TheoremA` |
| Theorem A, second display (`ρ_t`) | `Hkr_le_chernoff`, `theoremA_fin_chernoff` (`binomial_mode_bound`, `card_wt_eq`) | `TheoremA` |
| Theorem A, last display (`C_m`) | `theoremA_fin_Cm` (`theoremA_group_Cm`) | `TheoremA` |
| Lemma A16.5, given Harper's theorem and the level | `A16.lemmaA16_5_of_harper` (`A16.sum_comp_le_of_card_le`, `A16.tail_of_harper`, `A16.F_eq_clip`, `A16.f_concaveOn`) | `A16Rearrangement` |
| Proposition A1.1, item 1 | `condMarg_mem_window_lipH` | `Compensation` |
| Proposition A1.1, item 2 | `Chain.a1_item2_lip`, `Chain.a1_item2_cone0`, `Chain.a1_item2_cone1`, `Chain.a1_item2_isGreatest` | `ChainRuleCube` |

The files of `experiments/science/` are not in the lake library and cannot import each other; this is
why two files repeat earlier material (L1 and L2 did the same).  `TheoremA.lean` is *generated* by
`assemble.py` from `parts/TheoremA_head.txt`, the body of `Compensation.lean` and
`parts/TheoremA_tail.txt`, so the repeated part is literally the same text.  The theory division's
`.olean` files for `proofs.Frontiers.QueryLowerBound` and `NonAdaptive` were already on disk; I did not rebuild them.  The
`#print axioms` lines cover it (axioms are tracked through imports).

### 2.1 Definitions

The cube is `ι → Bool`, `ι` any finite type of sites, `n = |ι|`.  Weights, reference weights and
"measures" are plain functions `(ι → Bool) → ℝ`; positivity and invariance are hypotheses where they are
used.

| report | Lean | definition |
|---|---|---|
| `x⁽ⁱ⁾` | `flipAt x i` | `Function.update x i (!x i)` |
| `𝒲_u` | `InCone u w` | `(∀ x, 0 < w x) ∧ ∀ x i, e^{−u}·w x ≤ w (flipAt x i) ∧ w (flipAt x i) ≤ e^{u}·w x` |
| `L_u` | `LipH u ψ` | `∀ x y, |ψ x − ψ y| ≤ u · hammingDist x y` |
| `A(w)` | `massW π w` | `Σ_x π x · w x` |
| mass of `{x_i = 1}` | `oneW π w i` | `Σ_x if x i then π x · w x else 0` |
| `μ_w(x_i = 1)` | `margW π w i` | `oneW π w i / massW π w` |
| `|x|` | `wt x` | number of `i` with `x i = true` |
| `dens(w)` | `densW π w` | `(Σ_x π x · w x · |x|) / (n · massW π w)` |
| "`G`-invariant" | `Invariant G w` | `∀ σ ∈ G, ∀ x, w (x ∘ σ) = w x`, with `G : Set (Equiv.Perm ι)` |
| "`G` transitive on the sites" | `SiteTransitive G` | `∀ i j, ∃ σ ∈ G, σ i = j` |
| `π = Bern(p)^{⊗n}` | `refW p` | `∏_i (if x i then p else 1 − p)`; total mass 1 (`sum_refW`) |
| `q + pe^{−γ}` | `tiltZ p γ` | `(1 − p) + p·e^{−γ}` |
| `p_γ` | `pTilt p γ` | `p·e^{−γ} / tiltZ p γ`; `p₋ = pTilt p u`, `p₊ = pTilt p (−u)` |
| additive instance with site fields `γ_i` | `tiltW p γ`, `γ : ι → ℝ` | `∏_i e^{−γ_i x_i}/(q + p e^{−γ_i})` |
| `w̃_γ` | `baseW p γ` | `tiltW p (fun _ => γ)`; equals `e^{−γ|x|}/(q + pe^{−γ})ⁿ` (`baseW_eq` **[V]**) |
| `c̃_s` | `coneW p u s` | `tiltW p (coneField u s)`, `coneField u s i = if s i then −u else u`; equals `e^{−u·d_H(x,s)}/Z_s`, `Z_s = ∏_i z_{s_i}`, `z_0 = q + pe^{−u}`, `z_1 = qe^{−u} + p` (`coneW_eq` **[V]**) |
| `Δ_{s,r}` | `dipW p u γ r s x` | `max (e^r · coneW p u s x − baseW p γ x) 0` |
| `x ∈ D_{s,r}` | `0 < dipW p u γ r s x` | `⟺ π_γⁿ(x) < e^r π_s(x)` (`dipW_pos_iff` **[V]**) |
| `T_k` | `Tk ι k` | `{s : ι → Bool // wt s = k}` |
| `Δ̄_s` | `barW p u γ r s x` | `(Σ_{a : ι} dipW p u γ r (fun i => s (i + a)) x) / n`, `ι` an additive group |
| `ln A(ψ)` | `logA π ψ` | `log (massW π (fun x => e^{−ψ x}))` |
| `o(ψ)` | `oracle1 π ψ` | `fun i => margW π (fun x => e^{−ψ x}) i` |
| `ω, ω_m, κ, β` | `omegaW p u`, `omegaM p u k n`, `kappaA p u r k n`, `betaA p u r k n` | `p₊ − p₋`; `ω·min(k/n, 1 − k/n)`; `ω_m − 1/(e^r − 1)`; `ω/κ` |
| `H_{k,r}` | `Hkr ι p u γ r k` | `(max_x #{s : wt s = k ∧ 0 < dipW p u γ r s x}) / #{s : wt s = k}` |
| `ρ_t(m;γ)` | `rhoT p u γ t m` | `max_{a∈{1,0}} [(1 − m)·ratioS p u γ false a ^ t + m·ratioS p u γ true a ^ t]` (real powers), `ratioS p u γ b a = π_b(a)/π_γ(a)`, `π_0 = Bern(p₋)`, `π_1 = Bern(p₊)` |
| `C_m` | `CmA p u k n` | `1 + 2/min(k/n, 1 − k/n) + 2/ω_m` |
| `μ_w(x_i = 1 ∣ x_P = y_P)` | `condMarg π w P y i` | `margW (cylRef π P y) w i`, `cylRef π P y x = if ∀ j ∈ P, x j = y j then π x else 0` (`condMarg_eq` **[V]**: it is the ratio of the two cylinder masses) |

**A design decision that shortens everything:** an additive instance with *site-dependent* fields has
weight `tiltW p γ` with `π·tiltW p γ = ⊗_i π_{γ_i}`; the constant field gives `w̃_γ`, the field
`γ_i = u(1 − 2s_i)` gives the normalised cone `c̃_s`.  One set of product lemmas (`sum_prodW`,
`sum_prodW_one`, `prodW_inCone`, `prodW_perm`) then serves the base, the compensator and the cones.
That my `coneW` and `baseW` are the report's `c̃_s` and `w̃_γ` is itself machine-checked (`coneW_eq`,
`baseW_eq`).

### 2.2 The cone and the class (`Compensation.lean`, Part 1) [V]

| statement (SF §2.0) | Lean | remarks |
|---|---|---|
| `ψ ∈ L_u ⟺ e^{−ψ} ∈ 𝒲_u` | `lipH_iff_inCone`; `inCone_iff_lipH_log` (`w ∈ 𝒲_u ⟺ −ln w ∈ L_u`, for `w > 0`) | through `lipH_iff_flip`: `L_u` = "changes by at most `u` under every single flip" (induction on the Hamming distance, `sub_le_mul_hammingDist`); no sign condition on `u` |
| `L_u` is the theory division's class | `lipH_iff_sub_le` | `LipH u ψ ⟺ ∀ x y, ψ x − ψ y ≤ u·d_H(x,y)`, i.e. `MetricChain.Admissible (fun x y => u * hammingDist x y) ψ` unfolded (the form used by L1's `HammingLip` and in `Chain.a1_item2_lip`) |
| `𝒲_u` closed under sums | `InCone.add`, `InCone.sum` (finite non-empty sums) | |
| … positive multiples | `InCone.smul`; `InCone.add_smul` (`w + b·v`, `b ≥ 0`) | |
| … pointwise max and min | `inCone_max`, `inCone_min` | |
| (not in the text) | `inCone_of_upper` | the upper inequality `w(x⁽ⁱ⁾) ≤ e^u w(x)` at all points implies the lower one |

### 2.3 Lemma 3 (compensation) [V]

**Paper, (i).**  `G` a group of permutations of the coordinates, transitive on the sites; `w ∈ 𝒲_u`,
`Δ ≥ 0`, `Δ ≢ 0`, `w + Δ ∈ 𝒲_u`, both `G`-invariant.  All one-body marginals of `μ_w` equal `c_w`, all
those of `μ_{w+Δ}` equal `(A_w c_w + A_Δ c_Δ)/(A_w + A_Δ)`: same oracle answer iff `c_Δ = c_w`.

**Lean** (`Compensation.lean`, Part 2):

    theorem lemma3_i [Nonempty ι] {G : Set (Equiv.Perm ι)} (hG : SiteTransitive G)
        {π w Δ : (ι → Bool) → ℝ} (hπ : ∀ x, 0 < π x) (hπG : Invariant G π)
        (hw : ∀ x, 0 < w x) (hwG : Invariant G w)
        (hΔ0 : ∀ x, 0 ≤ Δ x) (hΔ1 : ∃ x, Δ x ≠ 0) (hΔG : Invariant G Δ) :
        (∀ i, margW π w i = densW π w) ∧
        (∀ i, margW π (fun x => w x + Δ x) i =
          (massW π w * densW π w + massW π Δ * densW π Δ) / (massW π w + massW π Δ)) ∧
        ((∀ i, margW π (fun x => w x + Δ x) i = margW π w i) ↔ densW π Δ = densW π w)

with the pieces `margW_eq_densW` (invariant ⇒ every marginal is the density), `margW_add` (the marginals
of a sum are the mass-weighted averages — no invariance needed), `margW_add_eq_iff`, `oneW_perm`,
`densW_eq_avg` (the density is the average of the `n` marginals).

**Paper, (ii).**  If `|γ₂| ≤ u` and `c_Δ` lies strictly between `c_w` and `p₂ := p_{γ₂}`, then with
`b := A_w(c_Δ − c_w)/(p₂ − c_Δ) > 0` the weights `w₀ := w + b·w̃_{γ₂}`, `w₁ := w + Δ + b·w̃_{γ₂}` are in
`𝒲_u`, are `G`-invariant, have all one-body marginals equal to `c_Δ`, differ exactly on `{Δ > 0}`, and
`A(w₁)/A(w₀) = 1 + (A_Δ/A_w)·(p₂ − c_Δ)/(p₂ − c_w)`.

**Lean** (Part 3; `v` is the compensator, `densW π v` plays `p₂`):

    theorem lemma3_compensation {G : Set (Equiv.Perm ι)} (hG : SiteTransitive G)
        {π : (ι → Bool) → ℝ} (hπ : ∀ x, 0 < π x) (hπG : Invariant G π) {u : ℝ}
        {w Δ v : (ι → Bool) → ℝ} (hw : InCone u w) (hwG : Invariant G w)
        (hΔ0 : ∀ x, 0 ≤ Δ x) (hΔ1 : ∃ x, Δ x ≠ 0) (hwΔ : InCone u (fun x => w x + Δ x))
        (hΔG : Invariant G Δ) (hv : InCone u v) (hvG : Invariant G v) (hv1 : massW π v = 1)
        (hbetween : (densW π w < densW π Δ ∧ densW π Δ < densW π v) ∨
          (densW π v < densW π Δ ∧ densW π Δ < densW π w)) :
        ∃ b : ℝ, b = massW π w * (densW π Δ - densW π w) / (densW π v - densW π Δ) ∧ 0 < b ∧
          InCone u (fun x => w x + b * v x) ∧ InCone u (fun x => w x + Δ x + b * v x) ∧
          Invariant G (fun x => w x + b * v x) ∧ Invariant G (fun x => w x + Δ x + b * v x) ∧
          (∀ i, margW π (fun x => w x + b * v x) i = densW π Δ) ∧
          (∀ i, margW π (fun x => w x + Δ x + b * v x) i = densW π Δ) ∧
          (∀ x, w x + Δ x + b * v x ≠ w x + b * v x ↔ 0 < Δ x) ∧
          massW π (fun x => w x + Δ x + b * v x) / massW π (fun x => w x + b * v x) =
            1 + massW π Δ / massW π w * ((densW π v - densW π Δ) / (densW π v - densW π w))

and, with exactly the objects of the report (`π = refW p`, compensator `tiltW p (fun _ => γ₂)`,
`|γ₂| ≤ u`, `p₂ = pTilt p γ₂`): **`lemma3_compensation_bernoulli`** (Part 6), same conclusion.
Supporting facts **[V]**: `massW_tiltW` (`A(w̃_γ) = 1`), `margW_tiltW` (`μ(x_j = 1) = p_{γ_j}`),
`densW_tiltW_const` (`dens(w̃_γ) = p_γ`), `tiltW_inCone` (`|γ_i| ≤ u` ⇒ member of the class),
`refW_invariant`, `tiltW_const_invariant` (invariance under every site permutation).

**The linear equation by itself** (the content of the paper's Remark (2)), division-free and at one
site, with no sign condition and no invariance:

    theorem oneW_compensated {π w v : (ι → Bool) → ℝ} {i : ι} {cw cΔ p₂ : ℝ}
        (hw : oneW π w i = cw * massW π w) (hv : oneW π v i = p₂ * massW π v)
        (hv1 : massW π v = 1) (hne : p₂ ≠ cΔ) :
        oneW π (fun x => w x + massW π w * (cΔ - cw) / (p₂ - cΔ) * v x) i =
          cΔ * massW π (fun x => w x + massW π w * (cΔ - cw) / (p₂ - cΔ) * v x)

and `massW_compensated`: `A(w₀) = A_w(p₂ − c_w)/(p₂ − c_Δ)`.

**Remark (1) of the paper** ("compensation by class members is possible iff `c_Δ ∈ [p₋, p₊]`; always
possible in the open window"), as four theorems **[V]**:
`window_of_equal_marginals` (only if: equal marginals of `w₀` and `w₀ + Δ` force the marginal of `Δ`
into the window), `lemma3_compensation_exists` (if `p₋ < c_Δ < p₊`: some `γ₂ ∈ {−u, +u}` and `b ≥ 0`
work; `b = 0` when `c_Δ = c_w`), and `no_compensation_at_upper_end`, `no_compensation_at_lower_end` (at
an end of the window a base plus a non-negative multiple of a class member can have that marginal only
if the base already has it) — see finding F1.

**Differences from the paper statement.**
1. `G` is any *set* of site permutations with the transitivity property; no group structure is used
   (numerically confirmed on "rotations without the identity", §3).
2. The reference weight is any positive `G`-invariant function in `lemma3_compensation`; the paper's
   `Bern(p)^{⊗n}` in `lemma3_compensation_bernoulli`.
3. The compensator is any `G`-invariant member `v` of the class with `A(v) = 1`; the paper's `w̃_{γ₂}`
   is the instance.
4. (i) does not use the cone: positivity of `w` and `Δ ≥ 0`, `Δ ≢ 0` suffice (the paper assumes
   `w, w + Δ ∈ 𝒲_u` for (i) and (ii) together).  The "iff" of (i) needs `n ≥ 1` (`[Nonempty ι]`).
5. "Strictly between" is the disjunction of the two orders.  "Differ exactly on `{Δ > 0}`" is
   `∀ x, w₁ x ≠ w₀ x ↔ 0 < Δ x`.  `b` is exhibited with its formula (`∃ b, b = … ∧ …`).
6. No hypothesis on the sign of `u`.

### 2.4 Lemma 0 (window) [V], and Proposition A1.1, item 1 [V]

**Paper.**  For every `ψ ∈ L_u` and every site, `μ_ψ(x_i = 1) ∈ [p₋, p₊]`; the densities of the additive
instances fill `[p₋, p₊]`.  If all `n` marginals are at ends of the window, with pattern `s`, then
`ψ = u·d(·,s) + const`.

**Lean** (`Compensation.lean`, Part 4):

    theorem lemma0_window_lipH {p u : ℝ} (hp0 : 0 < p) (hp1 : p < 1) {ψ : (ι → Bool) → ℝ}
        (hψ : LipH u ψ) (i : ι) :
        pTilt p u ≤ margW (refW p) (fun x => Real.exp (-ψ x)) i ∧
          margW (refW p) (fun x => Real.exp (-ψ x)) i ≤ pTilt p (-u)

(`lemma0_window` is the same in the weights).  More generally, `window_of_site_odds_nonneg`: for **any**
non-negative reference weight `π` with `π(x^{i←1})·(1 − p) = π(x^{i←0})·p` and positive mass.
`lemma0_additive_fill`: for `u ≥ 0` and every `c ∈ [p₋, p₊]` there is `γ ∈ [−u, u]` such that `w̃_γ` is in
the class and has all marginals equal to `c` (intermediate value theorem; `pTilt_anti`,
`pTilt_strictAnti`: `γ ↦ p_γ` is decreasing).  The third sentence:

    theorem lemma0_rigidity_lipH {p u : ℝ} (hp0 : 0 < p) (hp1 : p < 1) {ψ : (ι → Bool) → ℝ}
        (hψ : LipH u ψ) (s : ι → Bool)
        (h : ∀ i, margW (refW p) (fun x => Real.exp (-ψ x)) i =
          if s i = true then pTilt p (-u) else pTilt p u) :
        ∀ x, ψ x = ψ s + u * (hammingDist x s : ℝ)

(`lemma0_rigidity` in the weights: `w = w(s)·e^{−u·d_H(·,s)}`; through `flip_eq_of_marg_eq_upper`,
`flip_eq_of_marg_eq_lower`: a marginal at an end of the window forces every flip at that site to
change the weight by exactly `e^{±u}` — a sum of non-negative terms that vanishes.)

**Proposition A1.1, item 1** (paper: "for every order of the coordinates and every prefix,
`ν_ψ(y_i = 1 | y_{<i}) ∈ [a₀, a₁]`", `a₀ = p₋`, `a₁ = p₊`):

    theorem condMarg_mem_window_lipH {p u : ℝ} (hp0 : 0 < p) (hp1 : p < 1) {ψ : (ι → Bool) → ℝ}
        (hψ : LipH u ψ) (P : Finset ι) (y : ι → Bool) {i : ι} (hi : i ∉ P) :
        pTilt p u ≤ condMarg (refW p) (fun x => Real.exp (-ψ x)) P y i ∧
          condMarg (refW p) (fun x => Real.exp (-ψ x)) P y i ≤ pTilt p (-u)

**Differences.**  (1) The conditioning set is *any* `P ∌ i` with any pattern, which contains "every
order and every prefix" (`P` = the sites before `i`) and Lemma 0 (`P = ∅`).  (2) Connection with
workstream L2: `ScienceL2.condLaw_mem_window` (`ws_L2/Window.lean`) is the same statement for arbitrary
finite alphabets in "window" form `π(a)p(b) ≤ e^{d(a,b)}π(b)p(a)`; the present theorem is its two-letter
case with the window written as the interval `[p₋, p₊]`, proved directly (bijection `x ↦ x⁽ⁱ⁾`
between `{x_i = 0}` and `{x_i = 1}`), not derived from L2's file, which cannot be imported.  (3) Rigidity
is stated with the constant made explicit (`ψ = ψ(s) + u·d(·,s)`); the remark "one evaluation certifies
`ln A` exactly" is not a separate formal statement.  (4) No sign condition on `u` in the window and
rigidity statements (for `u < 0` and `n ≥ 1` the class is empty).

### 2.5 Lemma 2 (the excess of a dip is the cone law) [V]

**Paper.**  `|γ| ≤ u`, `s ∈ T_k`, `r > 0`, `Δ_{s,r} = (e^r c̃_s − w̃_γ)₊`; `w̃_γ + Δ_{s,r} = max(w̃_γ, e^r c̃_s) ∈ 𝒲_u`;
`E_{k,r} = A(Δ_{s,r})` and `c_{k,r} = dens(Δ_{s,r})` depend on `(k,r)` only, and
`e^r − 1 ≤ E_{k,r} ≤ e^r`, `|c_{k,r} − c₀(k/n)| ≤ 1/(e^r − 1)`.

**Lean.**  Abstract core (`Compensation.lean`, Part 5; `X` any finite type):

    theorem excess_mass_bounds {P₁ P₂ : X → ℝ} (h₁ : ∀ x, 0 ≤ P₁ x) (h₂ : ∀ x, 0 ≤ P₂ x)
        (s₁ : ∑ x, P₁ x = 1) (s₂ : ∑ x, P₂ x = 1) {R : ℝ} (hR : 0 ≤ R) :
        R - 1 ≤ ∑ x, max (R * P₁ x - P₂ x) 0 ∧ ∑ x, max (R * P₁ x - P₂ x) 0 ≤ R

    theorem excess_mean_bound {P₁ P₂ : X → ℝ} (h₁ …) (h₂ …) (s₁ …) (s₂ …) {R : ℝ} (hR : 1 < R)
        {f : X → ℝ} (hf0 : ∀ x, 0 ≤ f x) (hf1 : ∀ x, f x ≤ 1) :
        |(∑ x, max (R * P₁ x - P₂ x) 0 * f x) / (∑ x, max (R * P₁ x - P₂ x) 0) - ∑ x, P₁ x * f x|
          ≤ 1 / (R - 1)

For the dips (Part 6): `lemma2_mass` (`e^r − 1 ≤ massW (refW p) (dipW p u γ r s) ≤ e^r`, for all real
`u, γ, r`), `lemma2_dens` (`|densW (refW p) (dipW …) − densW (refW p) (coneW p u s)| ≤ 1/(e^r − 1)`,
`r > 0`), `densW_coneW` (`dens(c̃_s) = (k·p₊ + (n − k)·p₋)/n = c₀(k/n)`, `k = wt s`),
`baseW_add_dipW` and `baseW_add_dipW_inCone` (`w̃_γ + Δ_{s,r} = max(w̃_γ, e^r c̃_s) ∈ 𝒲_u` for `|γ| ≤ u`,
`u ≥ 0`), `refW_mul_dipW` (`π·Δ_{s,r} = (e^r π_s − π_γⁿ)₊`), `dipW_pos_iff`
(`D_{s,r} = {Δ_{s,r} > 0} = {π_γⁿ < e^r π_s}`), and
`massW_densW_dipW_of_wt_eq` (mass and density are the same for any two centres with the same number
of ones — through `exists_perm_of_wt_eq`: two configurations with the same number of ones differ by a
site permutation, and `dipW_perm`: `Δ_{s∘σ,r}(x∘σ) = Δ_{s,r}(x)`).

**Differences.**  (1) The two bounds hold for any two probability vectors and any `[0,1]`-valued
observable; the product structure enters only in "`π_s` and `π_γⁿ` are probability vectors" and in the
value of `c₀`.  (2) `|γ| ≤ u` is needed only for membership of the class, `r > 0` only for the density
bound.  (3) **Stronger than the paper:** `lemma2_site` — every one-body marginal of the normalised
excess is within `1/(e^r − 1)` of the corresponding marginal `π_{s_i}(1)` of the cone law, site by
site.  (4) "Depend on `(k,r)` only" is stated as equality for two centres of equal weight.

### 2.6 Lemma 1 (indistinguishability with an oracle), (a) and (b) [V]

**Paper.**  `ψ₀, ψ_j ∈ L_u` with `o(ψ_j) = o(ψ₀)`, `|ln A(ψ_j) − ln A(ψ₀)| > ε`, `D_j = {ψ_j ≠ ψ₀}`.  Every
`(ε/2, δ)`-correct oracle algorithm makes on `ψ₀` at least `(1 − 2δ)·|J| / max_x #{j : x ∈ D_j}`
evaluations in expectation.

**Lean** (`TheoremA.lean`, Part 7):

    theorem lemma1a {X Θ : Type*} {G : (X → ℝ) → Prop} {Φ : (X → ℝ) → ℝ}
        (O : (X → ℝ) → Θ) {Ω : Type*} [Fintype Ω]
        (alg : Ω → Θ → MetricChain.QueryAlgorithm X) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω)
        (hP1 : ∑ ω, P ω = 1) {ε δ : ℝ}
        (hcorr : ∀ g, G g →
          1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω (O g)).output g - Φ g| ≤ ε / 2), P ω)
        {g₀ : X → ℝ} (hg₀ : G g₀) {J : Type*} [Fintype J] (alt : J → X → ℝ)
        (halt : ∀ j, G (alt j)) (hO : ∀ j, O (alt j) = O g₀)
        (hsens : ∀ j, ε < |Φ (alt j) - Φ g₀|) {B : ℝ}
        (hcap : ∀ a, ((univ.filter fun j => alt j a ≠ g₀ a).card : ℝ) ≤ B) :
        (1 - 2 * δ) * (Fintype.card J : ℝ) ≤ (∑ ω, P ω * ((alg ω (O g₀)).queries g₀).card) * B

`lemma1a_div` is the displayed form `(1 − 2δ)|J|/B ≤ E[#evaluations]` (for `B > 0`); `lemma1a_weighted`
allows weights on the alternatives; `oracle_packing_weights` is the form used in Theorem A (class
`L_u`, target `ln A`, the one-body oracle, alternatives given by weights `w₀, w₁ j ∈ 𝒲_u` with all
one-body marginals equal to one number `c`).

**How it is proved, and what it rests on.**  It is the theory division's
`MetricChain.expected_queries_ge_packing` applied to the plain query algorithm `alg ω (O g₀)` and the
class `{g ∈ G : O g = O g₀}` — the argument of L1's `theorem4_adaptive_marginal_oracle`, isolated for an
arbitrary oracle, class and target.  L1's theorem itself could not be used (it is stated for codes and
the zero residual, and its file cannot be imported).

**Differences.**  (1) The oracle is any function `O` of the instance with values in any type; the class
any predicate; the target any functional.  (2) *Model:* an oracle algorithm is a family `alg ω o` of
`MetricChain.QueryAlgorithm`s (the theory division's abstract deterministic adaptive algorithm: a
query set and an output for every instance, consistent on instances that agree on the queried set — a
class that contains every decision tree) indexed by a seed `ω` of a **finite** probability space
`(Ω, P)` and by the oracle's answer; on `g` it runs `alg ω (O g)`.  Randomness with infinitely many
seeds is not covered (as in L1 and the theory division).  (3) Division-free conclusion; `B` is any
bound on the multiplicities, not necessarily their maximum.  (4) **Lemma 1 (b)** (paper: pairs
`(ψ_j, ψ′_j)` in `L_u`, all `2|J|` instances with the same oracle answer, `|ln A(ψ_j) − ln A(ψ′_j)| > ε`;
every non-adaptive `(ε/2, δ)`-correct oracle algorithm makes at least
`(1 − 2δ)|J|/max_x #{j : x ∈ D_j}` evaluations in expectation) is `lemma1b` (`lemma1b_weighted`), from
`MetricChain.nonadaptive_expected_queries_ge` in the same way: "non-adaptive" is
`∀ ω o g, (alg ω o).queries g = Q ω o`; the common answer is a parameter `o₀`; the conclusion is
`(1 − 2δ)·|J| ≤ (Σ_ω P ω·|Q ω o₀|)·B`.  It was not asked for and is not used in Theorem A.

### 2.7 Theorem A (every `n`; adaptive algorithms with an exact one-body oracle) [V]

**Paper.**  `0 < p < 1`, `u > 0`, `n ≥ 2`, `|γ| ≤ u`, `1 ≤ k ≤ n − 1`, `m = k/n`, `ω_m = ω·min(m, 1 − m)`,
`r > 0` with `(e^r − 1)ω_m > 1`, `κ = ω_m − 1/(e^r − 1)`, `β = ω/κ`.  There are `γ₂ ∈ {−u, +u}` and
`b ∈ [0, β]` such that for `ψ₀ := −ln(w̃_γ + b·w̃_{γ₂}) ∈ L_u`: every randomised oracle algorithm (adaptive,
with any hint) that is `(ε/2, δ)`-correct for `ln A` on `L_u`, for some `ε < ln(1 + (e^r − 1)/(1 + β))`,
makes on `ψ₀` in expectation at least `(1 − 2δ)/(n·H_{k,r})` evaluations,
`H_{k,r} := max_x P_{s∼Unif(T_k)}[x ∈ D_{s,r}]`.

**Lean** (`TheoremA.lean`, Part 9), on `{0,1}ⁿ = Fin n → Bool` with the cyclic shifts:

    theorem theoremA_fin {n : ℕ} [NeZero n] {p u γ r : ℝ} (hp0 : 0 < p) (hp1 : p < 1)
        (hγ : |γ| ≤ u) (hr : 0 < r) {k : ℕ} (hk : k ≤ n)
        (hcond : 1 < (Real.exp r - 1) * omegaM p u k n) :
        ∃ γ₂ : ℝ, (γ₂ = -u ∨ γ₂ = u) ∧ ∃ b : ℝ, 0 ≤ b ∧ b ≤ betaA p u r k n ∧
          LipH u (fun x : Fin n → Bool => -Real.log (baseW p γ x + b * baseW p γ₂ x)) ∧
          ∀ (Ω : Type v) [Fintype Ω]
            (alg : Ω → (Fin n → ℝ) → MetricChain.QueryAlgorithm (Fin n → Bool)) (P : Ω → ℝ),
            (∀ ω, 0 ≤ P ω) → ∑ ω, P ω = 1 → ∀ ε δ : ℝ,
            ε < Real.log (1 + (Real.exp r - 1) / (1 + betaA p u r k n)) →
            (∀ ψ : (Fin n → Bool) → ℝ, LipH u ψ → 1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
              |(alg ω (oracle1 (refW p) ψ)).output ψ - logA (refW p) ψ| ≤ ε / 2), P ω) →
            (1 - 2 * δ) / ((n : ℝ) * Hkr (Fin n) p u γ r k) ≤
              ∑ ω, P ω * (((alg ω (oracle1 (refW p)
                  fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x))).queries
                  fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x)).card : ℝ)

Variants **[V]**: `theoremA_group` (sites = any finite additive group `ι` acting on itself by
translation, `n = |ι|`; conclusion in the division-free form `1 − 2δ ≤ E|Q(ψ₀)|·(n·H_{k,r})`);
`theoremA_group_div` (the same with the division); **`theoremA_group_sharp`** (`1 + b ≤ β` and the
larger threshold `ε < ln(1 + (e^r − 1)/β)`; the other three are corollaries of it); `Hkr_pos`
(`H_{k,r} > 0`, so the division is legitimate).

**The second display** (paper: "`(1 − 2δ)/(n·H_{k,r}) ≥ (1 − 2δ)·e^{−tr}·ρ_t(k/n;γ)^{−n}/(n(n+1))` for
every `t ≥ 0`") — Part 10:

    theorem Hkr_le_chernoff {p u γ r t : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (ht : 0 ≤ t) {k : ℕ}
        (hk0 : 0 < k) (hkn : k < Fintype.card ι) :
        Hkr ι p u γ r k ≤ ((Fintype.card ι : ℝ) + 1) *
          (Real.exp (t * r) * rhoT p u γ t ((k : ℝ) / Fintype.card ι) ^ Fintype.card ι)

and `theoremA_fin_chernoff` / `theoremA_group_chernoff`: under the hypotheses of `theoremA_fin`, with
the same `γ₂`, `b`, `ψ₀`, for every `t ≥ 0`:
`1 − 2δ ≤ E|Q(ψ₀)| · (n · ((n + 1) · (e^{t·r} · ρ_t(k/n;γ)ⁿ)))`.
Ingredients **[V]**: `one_le_of_dipW_pos` (Markov with real powers: `x ∈ D_{s,r}` ⇒
`1 ≤ e^{tr}∏_i (π_{s_i}(x_i)/π_γ(x_i))^t`), `dipCount_mul_le` (sum over all centres with the weights
`Bern(m)^{⊗n}` by `sum_prodW`; each factor is at most `ρ_t`), `refW_eq_pow`
(`Bern(m)^{⊗n}(s) = m^{|s|}(1 − m)^{n−|s|}`), `card_wt_eq` (`|T_j| = C(n,j)`), and
**`binomial_mode_bound`**: `1 ≤ (n + 1)·C(n,k)·(k/n)^k·(1 − k/n)^{n−k}` for `0 < k < n`, from `add_pow`
and `binomPmf_le_mode` (the binomial weights with parameter `k/n` increase up to `j = k` and decrease
afterwards: `binomPmf_step`, `binomPmf_le_succ`, `binomPmf_succ_le`).

**The last display** (paper: "for every `ε > 0` and `0 ≤ t ≤ 1`, choosing `r` suitably,
`E|Q(ψ₀)| ≥ (1 − 2δ)·e^{−tε}·ρ_t(k/n;γ)^{−n}/(C_m·n(n+1))`, `C_m := 1 + 2/m̲ + 2/ω_m`") — Part 11:

    theorem theoremA_fin_Cm {n : ℕ} [NeZero n] {p u γ ε : ℝ} (hp0 : 0 < p) (hp1 : p < 1)
        (hu : 0 < u) (hγ : |γ| ≤ u) (hε : 0 ≤ ε) {k : ℕ} (hk0 : 0 < k) (hkn : k < n) :
        ∃ γ₂ : ℝ, (γ₂ = -u ∨ γ₂ = u) ∧ ∃ b : ℝ, 0 ≤ b ∧
          b ≤ 2 / min ((k : ℝ) / n) (1 - (k : ℝ) / n) ∧
          LipH u (fun x : Fin n → Bool => -Real.log (baseW p γ x + b * baseW p γ₂ x)) ∧
          ∀ (Ω : Type v) [Fintype Ω]
            (alg : Ω → (Fin n → ℝ) → MetricChain.QueryAlgorithm (Fin n → Bool)) (P : Ω → ℝ),
            (∀ ω, 0 ≤ P ω) → ∑ ω, P ω = 1 → ∀ δ : ℝ,
            (∀ ψ : (Fin n → Bool) → ℝ, LipH u ψ → 1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
              |(alg ω (oracle1 (refW p) ψ)).output ψ - logA (refW p) ψ| ≤ ε / 2), P ω) →
            ∀ t : ℝ, 0 ≤ t → t ≤ 1 →
            1 - 2 * δ ≤
              (∑ ω, P ω * (((alg ω (oracle1 (refW p)
                  fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x))).queries
                  fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x)).card : ℝ)) *
                ((n : ℝ) * (((n : ℝ) + 1) *
                  (CmA p u k n * (Real.exp (t * ε) * rhoT p u γ t ((k : ℝ) / n) ^ n))))

proved with the explicit depth `r = ln C_m + ε`: then `e^r − 1 ≥ 2/m̲ + 2/ω_m`, so `(e^r − 1)ω_m > 2`,
`κ > ω_m/2`, `β < 2/m̲`; `C_m e^ε − 1 ≥ (1 + 2/m̲)(e^ε − 1)` gives `ε < ln(1 + (e^r − 1)/(1 + β))`; and
`e^{tr} = C_m^t e^{tε} ≤ C_m e^{tε}` for `t ≤ 1`.  The instance `ψ₀` depends on `ε` and not on `t`.

**How the first display is assembled** (all in `TheoremA.lean`; nothing is assumed).
(a) Family: `barW p u γ r s` (the translation average of the dip at `s`), `s ∈ T_k`.
`baseW_add_barW_inCone`: `w̃_γ + Δ̄_s ∈ 𝒲_u` (an average of `n` dips: `InCone.sum`, `InCone.smul`,
`baseW_add_dipW_inCone`).  `barW_invariant`: invariance under the translations (`barW_shift`, by
`dipW_perm` and re-indexing the sum).  `massW_barW`, `densW_barW`: `A(Δ̄_s) = A(Δ_{s,r})`,
`dens(Δ̄_s) = dens(Δ_{s,r})`.  (b) `massW_densW_dipW_of_wt_eq`: one mass `E` and one density `c` for all
`s ∈ T_k`.  (c) Lemma 2 (`lemma2_mass`, `lemma2_dens`, `densW_coneW`) and `cone_density_margin`
(`c₀(m)` is at distance `≥ ω_m` from both ends): `p₋ + κ ≤ c ≤ p₊ − κ`, `E ≥ e^r − 1`.
(d) `exists_compensator`: an end `p₂` of the window and `b ≥ 0`, `1 + b ≤ ω/κ`, with
`p_γ + b·p₂ = c·(1 + b)` — the linear equation of Lemma 3 with `A_w = 1`, including the case
`c = p_γ` (`b = 0`), which the hypothesis "strictly between" of Lemma 3 (ii) excludes.
(e) Hence `w₀ = w̃_γ + b·w̃_{γ₂}` has mass `1 + b` and all marginals `c`; `w₁^{(s)} = w₀ + Δ̄_s` has mass
`1 + b + E` and all marginals `c` (`margW_eq_densW` for the translation-invariant `Δ̄_s`); the gap is
`ln(1 + E/(1 + b)) ≥ ln(1 + (e^r − 1)/β) > ε`.  (f) `card_barW_ne_zero_le`: a point lies in
`{Δ̄_s > 0}` for at most `n·#{s ∈ T_k : x ∈ D_{s,r}}` centres (`permTk`: translations permute `T_k`).
(g) `oracle_packing_weights` (Lemma 1 (a)).

**Differences from the paper statement.**
1. *Sites.*  `theoremA_fin` is the paper's setting; the translations `i ↦ i + a` of `Fin n` are the
   cyclic shifts (`addRight_fin_val`: `(i + a).val = (i.val + a.val) % n`).  `theoremA_group` is more general: any group structure on the set of sites gives a
   transitive group of order `n` (e.g. `ℤ₂ × ℤ₂`, `S₃`; checked numerically, §3).
2. *Hypotheses dropped* because they follow from the others: `u > 0`, `n ≥ 2`, `1 ≤ k ≤ n − 1`
   (finding F3).  Kept: `0 < p < 1`, `|γ| ≤ u`, `r > 0`, `k ≤ n`, `(e^r − 1)ω_m > 1`; `[NeZero n]`.
3. *Constants.*  `theoremA_fin`, `theoremA_group`, `theoremA_group_div` have the paper's `b ≤ β` and
   threshold; `theoremA_group_sharp` is stronger (finding F2).
4. *Algorithm model* as in §2.6: `alg : Ω → (Fin n → ℝ) → MetricChain.QueryAlgorithm (Fin n → Bool)`,
   finite seed space; the oracle answer is the vector `oracle1 (refW p) ψ ∈ Fin n → ℝ`; correctness
   is required on `L_u` only.  "With any hint" is the order of the quantifiers (`∃ ψ₀ … ∀ alg`: the
   algorithm may depend on `ψ₀`).
5. `ε`, `δ` are arbitrary reals (for `δ ≥ ½` the bound is vacuous).  The correctness hypothesis is
   satisfiable for `ε, δ ≥ 0` (`exists_correct_oracle_algorithm`: evaluate everywhere), and the
   hypothesis `(e^r − 1)ω_m > 1` is satisfiable for every `0 < p < 1`, `u > 0`, `0 < k < n` (it is
   derived for `r = ln C_m + ε` inside `theoremA_group_Cm`): the theorem is not vacuous.
6. `H_{k,r}` is defined by counting: the maximum over `x` of `#{s : |s| = k, Δ_{s,r}(x) > 0}`, divided by
   `|T_k|` (`|T_k| = C(n,k)`: `card_wt_eq`).
7. *Second display.*  Stated division-free, `1 − 2δ ≤ E|Q(ψ₀)|·n(n+1)·e^{tr}·ρ_t(k/n;γ)ⁿ`; the powers
   `(·)^t` are real powers (`Real.rpow`) of positive numbers, `(·)ⁿ` a natural power.  The paper's chain
   "`(1 − 2δ)/(nH) ≥ (1 − 2δ)e^{−tr}ρ^{−n}/(n(n+1))`" presupposes `1 − 2δ ≥ 0`; the formal statement does
   not need it.  `Hkr_le_chernoff` needs `0 < k < n`, which in `theoremA_fin_chernoff` is derived from
   the hypotheses.
8. *Last display.*  `ε ≥ 0` instead of `ε > 0`; `u > 0` and `0 < k < n` are hypotheses here (the
   condition `(e^r − 1)ω_m > 1`, from which they followed, is now a conclusion about the chosen `r`);
   the depth is `r = ln C_m + ε`, not the paper's `ln(1 + max{2/ω_m, (1 + 2/m̲)(e^ε − 1)}) + η`
   (finding F4); `b ≤ 2/m̲` is part of the statement.
9. The proof does not call `lemma3_compensation`; it uses the same linear equation through
   `exists_compensator`, because the case `c_{k,r} = p_γ` needs `b = 0`.
10. Corollary A (the exponent `R^max`) is outside the brief and not formalised: it needs the
   single-letter optimisation (`F*`, the saddle) of the theory report on top of `theoremA_fin_Cm`.

### 2.8 Items 5 and 6

**Lemma A16.5 (`A16Rearrangement.lean`).**  R8's file has [V]: `sum_le_sum_f` ((a) as an inequality),
`f_le_max`, `f_mono_below`, `f_anti_above` ((b) as unimodality), `F_mono`, `F_eq_plateau` ((c), for a
level `t* ≥ 1`), `sum_le_sum_F` ((d)), `plateau_optimal`.  These are repeated verbatim in Part 0 and
are **not** claimed as mine.  New, all **[V]**:

| statement | Lean | remarks |
|---|---|---|
| (a) as an identity, `Σ t = Σ f_η(t) + η·φ(t)` | `A16.sum_eq_sum_f_add` | |
| (b) `f_η` concave | `A16.f_concaveOn` | on `[0, ∞)`, for `η ≥ 0` (from `Real.convexOn_mul_log`) |
| (c) "the maximiser is the clipped level", for every level | `A16.F_eq_clip` | `F_η(ρ) = f_η(max(e^{−uρ}, min(t*, e^{uρ})))` for every `t* > 0`: plateau if `t* ≥ 1`, hill if `t* < 1` (the case R8's F6 points to) |
| `η = 0` | `A16.F_zero` | `F_0(ρ) = e^{uρ}` |
| **rearrangement** (R8's T-R8-1): `H` nondecreasing and `#{ρ > k} ≤ #{ρ' > k}` for all `k` ⇒ `Σ_x H(ρ(x)) ≤ Σ_x H(ρ'(x))` | `A16.sum_comp_le_of_card_le` | `X` any finite type, `ρ, ρ' : X → ℕ` |
| **Lemma A16.5, given Harper and the level** | `A16.lemmaA16_5_of_harper`, `A16.lemmaA16_5_of_harper_ge` | below |
| the case `η = 0` (tail lemma) given Harper | `A16.tail_of_harper` | `t(x) ≤ e^{uρ(x)}` ⇒ `Σ t ≤ Σ e^{uρ'(x)}` |

    theorem lemmaA16_5_of_harper {X : Type*} [Fintype X] (t : X → ℝ) (ρ ρ' : X → ℕ)
        (η U₀ u ts : ℝ) (hη : 0 < η) (hu : 0 ≤ u) (h1 : 1 ≤ ts)
        (hstar : Real.log ts = 1 / η - 1 - U₀)
        (hφ : ∑ x, t x * Real.log (t x) + U₀ * ∑ x, t x ≤ 0)
        (hmem : ∀ x, t x ∈ Set.Icc (Real.exp (-(u * (ρ x : ℝ)))) (Real.exp (u * (ρ x : ℝ))))
        (hharper : ∀ k : ℕ,
          (univ.filter fun x => k < ρ x).card ≤ (univ.filter fun x => k < ρ' x).card)
        (hpl : 0 ≤ ∑ x, min ts (Real.exp (u * (ρ' x : ℝ))) *
            Real.log (min ts (Real.exp (u * (ρ' x : ℝ)))) +
          U₀ * ∑ x, min ts (Real.exp (u * (ρ' x : ℝ)))) :
        ∑ x, t x ≤ ∑ x, min ts (Real.exp (u * (ρ' x : ℝ)))

Reading: `t = e^{−g}` on the cube `X`; `ρ(x)` the distance from `x` to the complement of the support of
`g`; `ρ'` the same for the ball; `hharper` **is Harper's theorem, taken as a hypothesis**; `ts = e^{c*}`;
the conclusion is `Z_g ≤ Z^{pl}`.  **Differences from the addendum:** (1) Harper's theorem, the existence
and uniqueness of the level and the membership of the plateau in the class are hypotheses or absent,
exactly as said; (2) the plateau needs only `φ(t_pl) ≥ 0` (mean energy `≤ U₀`), not `= 0`; (3) as R8
observed, the Lipschitz property of `g` is not used, only the pointwise bounds; (4) `X` is any finite
type and `ρ, ρ'` any profiles.

**Proposition A1.1, items 1–2.**  Item 1: §2.4.  Item 2 (`ChainRuleCube.lean`; `klB a r` is
`KL(Bern(a)‖Bern(r))`, `klDivFin`, `gibbsLaw` are L2's):

    theorem a1_item2_lip {n : ℕ} {p r : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (hr0 : 0 < r)
        (hr1 : r < 1) {u : ℝ} (ψ : (Fin n → Bool) → ℝ)
        (hψ : ∀ x y, ψ x - ψ y ≤ u * (hammingDist x y : ℝ)) :
        klDivFin (gibbsLaw (fun x : Fin n → Bool => ∏ i, bernW p (x i)) ψ)
            (fun x => ∏ i, bernW r (x i)) ≤
          (n : ℝ) * max (klB (pTilt p u) r) (klB (pTilt p (-u)) r)

with `a1_item2_cone0`, `a1_item2_cone1` (value `n·KL(a₀‖r)` at `ψ = u|x|`, `n·KL(a₁‖r)` at
`ψ = u(n − |x|)`), `a1_item2_additive` (`n·KL(Bern(p_{γ(1)−γ(0)})‖Bern(r))` at `ψ = Σ_i γ(x_i)`) and
`a1_item2_isGreatest` (for `u ≥ 0`: `n·max{…}` is the greatest value over the class).  New ingredients:
`klB_le_max` (on `[a₀, a₁] ⊆ [0,1]` the binary relative entropy is largest at an end; from
`Real.convexOn_mul_log`), `klDivFin_bern`, `klBound_bool`.  **Differences:** (1) `r ∈ (0,1)` (the paper
says "every `r`"; outside `(0,1)` the divergence is infinite or undefined).  (2) "With equality for
`ψ = u·d_H(·,0ⁿ)` or `u·d_H(·,1ⁿ)`" is made precise: each cone gives its own term of the maximum, and the
larger one is the supremum.  (3) `a := R(r*)` and the identification with the capacity are not
formalised (definitions and a [K] fact).  **Which items of A1.1 are formal after this work:** item 1
(`Compensation.lean`: `condMarg_mem_window`, `condMarg_mem_window_lipH`; general alphabets: L2,
`condLaw_mem_window`); item 2 (`ChainRuleCube.lean`, as above; general alphabets with vertex labels:
L2, `klBound_pi_of_vertices`); items 3 (Azuma–Hoeffding) and 4 (the truncation step) are **not**
formal.

### 2.9 Discrepancies between the formal statements and the texts; findings

F1. **Remark (1) after Lemma 3: the window must be open.**  "Compensation by class members is possible
    iff `c_Δ ∈ [p₋, p₊]`".  *Only if* is right **[V]** (`window_of_equal_marginals`); *if* is right on
    the open window **[V]** (`lemma3_compensation_exists`), which is what the remark's second half
    says.  At an end, say `c_Δ = p₊ ≠ c_w`: a marginal of `w + b·v` (`b ≥ 0`, `v` any class member) is
    a weighted average of two numbers `≤ p₊` with positive weight on that of `w`, so it equals `p₊`
    only if the marginal of `w` does **[V]** (`no_compensation_at_upper_end`,
    `no_compensation_at_lower_end`).  Immaterial for Theorems A and B, where `c_Δ` is at distance `≥ κ`
    from the ends.
F2. **Theorem A: `1 + b ≤ β`.**  In both cases of the proof `1 + b = (p₊ − p_γ)/(p₊ − c)` resp.
    `(p_γ − p₋)/(c − p₋)`, which is `≤ ω/κ`.  So `b ≤ β − 1`, and the hypothesis on the accuracy can be
    weakened to `ε < ln(1 + (e^r − 1)/β)` **[V]** (`exists_compensator`, `theoremA_group_sharp`).
F3. **Theorem A: redundant hypotheses (first two displays).**  `u > 0` follows from
    `(e^r − 1)ω_m > 1` (and `u ≥ 0` from `|γ| ≤ u`); `1 ≤ k ≤ n − 1` and `n ≥ 2` follow from `(e^r − 1)ω_m > 1`, `r > 0`, `k ≤ n`.  `r > 0`
    and `k ≤ n` cannot be dropped from the formal statement: with `k > n` one has `ω_m < 0` and
    `(e^r − 1)ω_m > 1` is satisfiable by `r < 0`, while `T_k = ∅`.
F4. **Theorem A, last display, "`η ↓ 0`".**  With
    `r = ln(1 + max{2/ω_m, (1 + 2/m̲)(e^ε − 1)}) + η` the instance `ψ₀` (through `b`, `γ₂`) depends on
    `η`, and what the proof shows for each `η > 0` is the bound with an extra factor `e^{−tη}` at the
    instance `ψ₀^{(η)}`; letting `η ↓ 0` does not produce one instance with the displayed bound.  No
    limit is needed: the explicit depth `e^r = C_m e^ε` satisfies all three requirements, and the
    display holds at one instance, for all `t ∈ [0,1]` simultaneously **[V]** (`theoremA_group_Cm`,
    `theoremA_fin_Cm`).
F5. **Lemma 2 gives a closed interval.**  The proof of Theorem A says `c_{k,r} ∈ (p₋ + κ, p₊ − κ)`;
    Lemma 2 as stated (with `≤`) gives the closed interval, which is what is used and formalised.
F6. **Lemma 3 (i) does not need the cone; the linear equation needs neither signs nor invariance**
    (§2.3, differences 4 and the theorem `oneW_compensated`).
F7. **Lemma A16.5: `φ(t_pl) ≥ 0` suffices** (§2.8).
F8. **A1.1 item 2: `r ∈ (0,1)`; "equality at the cones"** means one cone per term of the maximum (§2.8).
F9. **Model of an algorithm** (Lemma 1 (a), Theorem A): finite seed space; the theory division's
    `QueryAlgorithm` (a superset of decision trees).  These are the conventions of the theory division
    and of L1, not a restriction introduced here, but they are part of the formal statement.

## 3. Numerics

`experiments/science/ws_L3/sanity_numerics.py` (own code; fixed seed; about 10 s; output in
`sanity_numerics_output.txt`).  Purpose: to try to falsify the **formal statements with their
generalised hypotheses** before proving them.  Nothing below is evidence for a theorem — the theorems
are proved.  All **[N]**:

| check | sizes | result |
|---|---|---|
| S1 Lemma 3 (i) | sites = `ℤ₂ … ℤ₆`, `ℤ₂×ℤ₂`, `S₃` acting on themselves; **non-product** invariant reference weights | worst `|marg − dens|` `2.2e−16` |
| S1′ a transitive set that is not a group | `n = 5`, the four non-trivial rotations | `0` |
| S2 Lemma 3 (ii), identities with arbitrary signs | 287 cases | marginals of `w₀, w₁` equal `c_Δ` to `1.1e−14`; mass-ratio formula to `2.3e−13` |
| S3 Lemma 0 | 200 random class members (McShane form), `n ≤ 5` | worst violation `1.1e−16` |
| S4 Lemma 2, abstract | 20 000 random pairs of probability vectors, random `f ∈ [0,1]` | never violated (slack `≥ 3.6e−2` in the density bound) |
| S5 every finite ingredient of Theorem A | 184 parameter sets, the 7 site groups above, `p ∈ {0.1, 0.3, 0.5, 0.7}`, `u ∈ {1, 1.5, 2, 3}`, all `1 ≤ k < n`, two depths | all assertions pass: one `(E, c)` per `T_k`; Lemma 2; `c ∈ [p₋+κ, p₊−κ]`; `0 ≤ b ≤ β`; `w₀`, `w₁^{(s)}` in the cone; all marginals equal `c` (`< 1e−9`); gap `≥ ln(1 + (e^r−1)/(1+β))`; counting bound |
| S6 A16.5, the new pieces | 20 000 cases | identity (a) `3.8e−15`; concavity never violated; `f` on a grid never exceeds `f` at the clipped level, for all `t* > 0` (`5.7e−16`); rearrangement on 20 000 dominated pairs: never violated (`3.6e−15`) |
| S8 Chernoff form of Theorem A | `n = 2 … 8`, 4 parameter sets, all `1 ≤ k < n`, 3 depths, `t ∈ {0, ¼, ½, 1, 2}`: 1 680 cases; exhaustive | `H_{k,r} − (n+1)e^{tr}ρ_tⁿ` never positive (the bound is very slack at these sizes); binomial mode bound holds |
| S7 A1.1 items 1–2 | 300 random members, `n ≤ 5`, all sites, **all** conditioning sets | item 1: worst violation `3.3e−16`; item 2: `max(KL − n·R(r)) = 4.4e−16`; equality at the two cones to `3.6e−15` |

For small `n` the bound of Theorem A is weak (in S5 a point typically lies in the support of every
`Δ̄_s`); the check is of the ingredients, not of the strength.

## 4. Prior art and search log

This workstream formalises statements of other workstreams; it makes no novelty claim for any proof
(all are elementary), and no literature search was made.  Facts about the library, from the local copy
(`.lake/packages/mathlib`), all **[signatures read with `#check` in a scratch file]**:
`Fintype.prod_sum` (the sum over a product type of a product is the product of the sums — the only
"product measure" fact used), `Equiv.extendSubtype` with `extendSubtype_mem`, `extendSubtype_not_mem`
(an equivalence between two subtypes of a finite type extends to a permutation — used for "two
configurations with the same number of ones differ by a site permutation"), `Fintype.equivOfCardEq`,
`Fintype.card_subtype`, `Equiv.sum_comp`, `Equiv.prod_comp`, `Fintype.sum_equiv`,
`Finset.exists_subset_card_eq`, `Finset.card_biUnion_le`, `intermediate_value_Icc'`,
`Real.convexOn_mul_log`, `Finset.sum_range_sub`, `hammingDist_eq_zero`; for the Chernoff form:
`Real.one_le_rpow`, `Real.mul_rpow`, `Real.exp_mul`, `Real.finsetProd_rpow`, `add_pow`,
`Nat.choose_succ_right_eq`, `Finset.card_powersetCard`, `Finset.prod_ite`.  I did not find (and did not
search the library for) a ready-made statement that the binomial weights are largest at the mode;
`binomPmf_le_mode` is proved here by the ratio of consecutive terms.  `Fin n` has an `AddCommGroup`
instance for `[NeZero n]` (checked with `inferInstance`).
Read in full: `SF_REPORT.md` §1–§2.4; `ws_L1/MarginalOracle.lean` (to line 920);
`proofs/Frontiers/QueryLowerBound.lean` lines 97–300; `ws_L2/Window.lean` lines 1–760;
`ws_R8/A16Core.lean`; addendum A16 part (c) (Lemma A16.5); `R8_REPORT.md` §2.4 and request T-R8-1 of
§7; `A1_REPORT.md` §2.5; `L2_REPORT.md` §1, §2.1, §2.6–§7; `proofs/Frontiers/NonAdaptive.lean`
lines 37–72.

## 5. Not done, and why

* **Corollaries A and B, Theorem B, §2.3–§2.7 of the SF report** — outside the brief.  Corollary A needs
  the single-letter optimisation of the theory report on top of `theoremA_fin_Cm`; Theorem B needs the
  theory division's truncated cones.  (Lemma 1 (b), which Theorem B uses, is done.)
* **Lemma A16.5:** Harper's theorem itself, existence and uniqueness of the level `c*`
  (`dU/dc = −μ(P)(1 + c + U)`), membership of the plateau in the class, Remark (4).  ("Sizes that are
  not ball sizes" is the same theorem with another `ρ'`.)
* **Proposition A1.1:** items 3 (Azuma–Hoeffding) and 4 (the truncation step); the capacity reading of
  `a`.
* The remark in Lemma 0 that at a cone "one evaluation certifies `ln A` exactly" is not a separate
  formal statement (it is immediate from `lemma0_rigidity_lipH`).
* The theory division's `proofs/Frontiers/QueryLowerBound.lean` and `NonAdaptive.lean` were imported
  as compiled; I did not recompile them.
* No statement here is about infinitely many seeds, about `n → ∞`, or about exponents; everything is
  for fixed finite `n`.

## 6. Three next steps

1. **Corollary A** (the adaptive exponent with the oracle is `R^max`): what remains after
   `theoremA_fin_Cm` is the single-letter side — `ρ_{t*}(k/n;γ*)ⁿ ≤ e^{L}·e^{−nF*(t*)}` for
   `k = round(m*n)` — i.e. the definitions of `F`, `F*`, the saddle and a Lipschitz bound for `ρ_t` in
   `m`.  If the theory division has `F*` in Lean, this is a short file.
2. **Theorem B (non-adaptive):** `lemma1b` and `lemma3_compensation` are already in the generality
   needed (`w = c̄_s^{tr}`, `Δ = c̄_s − c̄_s^{tr}`); what is missing is the translation average of the
   theory division's truncated cones (`truncate_lipschitz_insert`, …) and the type-class counting.
3. **Lemma A16.5 unconditionally on the cube:** Harper's theorem in the erosion form
   `#{x : dist(x, Dᶜ) ≥ k} ≤ #{x : dist(x, D*ᶜ) ≥ k}`.  Mathlib has Kruskal–Katona and related
   material under `Mathlib/Combinatorics/SetFamily/`; whether the vertex isoperimetric inequality of the
   cube is there in a usable form was **not checked**.

## 7. Requests

**To the theory division.**
(a) `experiments/science/ws_L3/Compensation.lean` depends on Mathlib only and can be moved under
`proofs/` as it is; `TheoremA.lean` then reduces to its Parts 7–11 (`parts/TheoremA_tail.txt`) with
`import` of the first file and of `proofs.Frontiers.QueryLowerBound`, `proofs.Frontiers.NonAdaptive`.  If Proposition 11.109 is
rewritten on the strength of workstream F: the formal Theorem A is `ScienceL3.theoremA_fin` (first
display), `theoremA_fin_chernoff` (second) and `theoremA_fin_Cm` (last); the sharper form
(`theoremA_group_sharp`, finding F2), the redundancy of three hypotheses (F3) and the explicit depth
`e^r = C_m e^ε` (F4) may be worth carrying over; Remark (1) of Lemma 3 should say "open window" (F1).
(b) `ScienceL3.lemma1a` and `ScienceL3.lemma1b` are `expected_queries_ge_packing` and
`nonadaptive_expected_queries_ge` with an oracle (three lines each).  If you add an oracle-indexed
algorithm to `QueryLowerBound.lean`, these two statements are the natural interface.
(c) (from R8's T-R8-1) the rearrangement step is now formal: `ScienceL3.A16.sum_comp_le_of_card_le`;
with Harper's theorem in the erosion form as a Lean statement, `A16.lemmaA16_5_of_harper` gives Lemma
A16.5 for every support.

**To the engineering division.**  None.

## Appendix: how to re-compile; axioms

    export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH"; cd /home/user/MetricChain
    lake env lean /home/user/MetricChain/experiments/science/ws_L3/Compensation.lean        # 20-50 s
    lake env lean /home/user/MetricChain/experiments/science/ws_L3/TheoremA.lean            # 50-180 s
    lake env lean /home/user/MetricChain/experiments/science/ws_L3/A16Rearrangement.lean    # 15-35 s
    lake env lean /home/user/MetricChain/experiments/science/ws_L3/ChainRuleCube.lean       # 15-45 s
    python3 experiments/science/ws_L3/assemble.py          # regenerates TheoremA.lean from its parts
    python3 experiments/science/ws_L3/sanity_numerics.py   # §3

or `bash experiments/science/ws_L3/check_all.sh` (writes `check_log.txt`; it also checks that
`TheoremA.lean` is identical to the output of `assemble.py` and counts forbidden tokens).  Each file
ends with `#print axioms` for its headline theorems (38 + 34 + 8 + 11 = 91 lines).  In the last run
(`check_log.txt`, 2026-11-26 01:13–01:15 UTC: four exit codes 0, no error, no warning) 90 lines read
`'ScienceL3.<name>' depends on axioms: [propext, Classical.choice, Quot.sound]` and one reads
`'ScienceL3.addRight_fin_val' depends on axioms: [propext, Quot.sound]`; no other axiom occurs.  The
names:

* `Compensation.lean` — `lipH_iff_sub_le`, `lipH_iff_inCone`, `inCone_iff_lipH_log`, `InCone.add`, `InCone.smul`,
  `inCone_max`, `inCone_min`, `margW_eq_densW`, `margW_add`, `lemma3_i`, `oneW_compensated`,
  `massW_compensated`, `lemma3_compensation`, `lemma3_compensation_bernoulli`,
  `window_of_equal_marginals`, `lemma3_compensation_exists`, `no_compensation_at_upper_end`,
  `no_compensation_at_lower_end`, `window_of_site_odds`, `lemma0_window`, `lemma0_window_lipH`,
  `lemma0_additive_fill`, `lemma0_rigidity`, `lemma0_rigidity_lipH`, `condMarg_eq`,
  `condMarg_mem_window`, `condMarg_mem_window_lipH`, `excess_mass_bounds`, `excess_mean_bound`,
  `baseW_eq`, `coneW_eq`, `baseW_add_dipW_inCone`, `lemma2_mass`, `lemma2_site`, `lemma2_dens`,
  `densW_coneW`, `dipW_pos_iff`, `massW_densW_dipW_of_wt_eq`.
* `TheoremA.lean` — `lemma3_i`, `lemma3_compensation`, `lemma3_compensation_bernoulli`,
  `lemma0_window_lipH`, `lemma2_mass`, `lemma2_dens`, `lemma1a_weighted`, `lemma1a`, `lemma1a_div`,
  `lemma1b_weighted`, `lemma1b`, `oracle_packing_weights`, `exists_correct_oracle_algorithm`,
  `massW_densW_dipW_of_wt_eq`, `dipW_pos_iff`, `addRight_fin_val`, `barW_invariant`, `massW_barW`, `densW_barW`,
  `baseW_add_barW_inCone`, `card_barW_ne_zero_le`, `exists_compensator`, `theoremA_group_sharp`,
  `theoremA_group`, `Hkr_pos`, `theoremA_group_div`, `theoremA_fin`, `binomial_mode_bound`,
  `card_wt_eq`, `Hkr_le_chernoff`, `theoremA_group_chernoff`, `theoremA_fin_chernoff`,
  `theoremA_group_Cm`, `theoremA_fin_Cm`.
* `A16Rearrangement.lean` — `A16.sum_eq_sum_f_add`, `A16.f_concaveOn`, `A16.F_eq_clip`, `A16.F_zero`,
  `A16.sum_comp_le_of_card_le`, `A16.lemmaA16_5_of_harper`, `A16.tail_of_harper`,
  `A16.lemmaA16_5_of_harper_ge`.
* `ChainRuleCube.lean` — `Chain.klBound_pi`, `Chain.kl_additive_pi`, `Chain.klB_le_max`,
  `Chain.klDivFin_bern`, `Chain.klBound_bool`, `Chain.a1_item2`, `Chain.a1_item2_lip`,
  `Chain.a1_item2_additive`, `Chain.a1_item2_cone0`, `Chain.a1_item2_cone1`,
  `Chain.a1_item2_isGreatest`.

| file | content |
|---|---|
| `Compensation.lean` | §2.2–§2.5; A1.1 item 1 |
| `TheoremA.lean` (generated) | §2.6, §2.7 |
| `parts/TheoremA_head.txt`, `parts/TheoremA_tail.txt`, `assemble.py` | the sources of `TheoremA.lean` |
| `A16Rearrangement.lean` | §2.8, Lemma A16.5 |
| `ChainRuleCube.lean` | §2.8, A1.1 item 2 |
| `check_all.sh`, `check_log.txt` | the check of the four files, one at a time |
| `sanity_numerics.py`, `sanity_numerics_output.txt` | §3 |
| `NOTES.md` | chronological log |
