```
Message ID:                  SCI-MSG-0019
Message type:                Formal verification delivered — the file you asked for (THY-RES-0008 §7 item 3):
                             the compensation lemma, Lemmas 0–2 and Theorem A of our workstream F — your
                             Theorem 11.109a (a)–(c) — are machine-checked in Lean, with nothing taken on
                             trust; Lemma A16.5 given Harper's theorem; Proposition A1.1 (your 11.61a),
                             items 1–2
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering (nothing is asked of it)
Date and time (UTC):         2026-11-26 01:26 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed for the items listed; Theorem B, the corollaries and Harper's theorem
                             are not formal (§4)
Relevant theory commit:      b2d3e9c (theory report §11.29: Theorem 11.109a, Proposition 11.109b;
                             proofs/Frontiers/QueryLowerBound.lean and NonAdaptive.lean as compiled in our
                             tree, which is built on 5ed4072 — the two files are imported, not rebuilt)
Relevant engineering commit: a2f6dc7
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             experiments/science/ws_L3/ (Compensation.lean, TheoremA.lean,
                             A16Rearrangement.lean, ChainRuleCube.lean, check_all.sh, sanity_numerics.py);
                             docs/science/workstreams/L3_REPORT.md; docs/science/workstreams/SF_REPORT.md
                             §2.0–§2.2 (two notes added); addendum A16, Lemma A16.5; A1_REPORT.md §2.5
Related message/request IDs: THY-RES-0008 §7 item 3 (answered); SCI-RES-0006 (workstream F; F-T2);
                             SCI-MSG-0016 (T-R8-1); SCI-MSG-0014 (the earlier Lean file you adopted)
```

# Theorem 11.109a (a)–(c) is machine-checked: the compensation lemma, the window, the excess of a dip, indistinguishability with an oracle, and the lower bound for adaptive algorithms at every `n` — the files, what they state, and three small improvements of the statement

## 1. What is formal

Lean 4.31.0 with the repository's pinned Mathlib; four files in
`experiments/science/ws_L3/`, written by workstream L3.  **Re-compiled by the coordinator,
one file at a time, with `lake env lean <absolute path>` (never `lake build`): four exit
codes 0, no error, no warning, no `sorry`, `admit`, `native_decide`, `axiom`, `unsafe`;
91 `#print axioms` lines, 90 of them `[propext, Classical.choice, Quot.sound]` and one
`[propext, Quot.sound]`.**  The coordinator read the definitions and nine headline
statements in the files against our report (`theoremA_fin`, `theoremA_group_sharp`,
`theoremA_fin_Cm`, `lemma1a`, `lemma0_window_lipH`, `lemma2_mass`, `lemma2_dens`,
`densW_coneW`, `A16.lemmaA16_5_of_harper`); the rest is the workstream's reading.

| your statement (§11.29) / ours | Lean declaration | file |
|---|---|---|
| Theorem 11.109a (a), compensation lemma (our Lemma 3 (i), (ii)) | `lemma3_i`, `lemma3_compensation`, `lemma3_compensation_bernoulli`; the linear equation alone, at one site, with no sign condition and no invariance: `oneW_compensated` | `Compensation.lean` (Mathlib only) |
| the window (your Proposition 11.109 (a); our Lemma 0), for marginals and for every conditional law given any pattern on any other sites; the additive instances fill it; rigidity at a cone | `lemma0_window_lipH`, `condMarg_mem_window_lipH`, `lemma0_additive_fill`, `lemma0_rigidity_lipH` | `Compensation.lean` |
| Theorem 11.109a (b), the excess of a dip sits on the cone law (our Lemma 2): `e^r − 1 ≤ E_{k,r} ≤ e^r`, `|c_{k,r} − c₀(k/n)| ≤ 1/(e^r − 1)` | `lemma2_mass`, `lemma2_dens`, `densW_coneW`, `massW_densW_dipW_of_wt_eq` | `Compensation.lean` |
| indistinguishability with an oracle (our Lemma 1 (a), (b)): your `expected_queries_ge_packing` and `nonadaptive_expected_queries_ge` with an arbitrary oracle, class and target | `lemma1a`, `lemma1b` (three lines each on top of your two theorems) | `TheoremA.lean` (imports your `QueryLowerBound`, `NonAdaptive`) |
| **Theorem 11.109a (c), first display:** `E|Q(ψ₀)| ≥ (1 − 2δ)/(n·H_{k,r})` | **`theoremA_fin`** (sites `Fin n`, cyclic shifts); `theoremA_group` (sites = any finite group acting on itself) | `TheoremA.lean` |
| (c), second display: `≥ (1 − 2δ)e^{−tr}ρ_t(m;γ)^{−n}/(n(n+1))` for every `t ≥ 0` | `Hkr_le_chernoff`, `theoremA_fin_chernoff` | `TheoremA.lean` |
| (c), last display, with `C_m = 1 + 2/min(m, 1−m) + 2/ω_m` | `theoremA_fin_Cm` | `TheoremA.lean` |
| our Lemma A16.5 (addendum A16), **given** Harper's inequality and the level — the rearrangement step that our referee's file lacked (T-R8-1 of SCI-MSG-0016) | `A16.sum_comp_le_of_card_le`, `A16.lemmaA16_5_of_harper` | `A16Rearrangement.lean` (Mathlib only) |
| your Proposition 11.61a (our A1.1), item 1 (every conditional one-site law is in the window) and item 2 (`KL(ν_ψ‖Bern(r)ⁿ) ≤ n·max{KL(a₀‖r), KL(a₁‖r)}`, attained at the cones, greatest over the class) | `condMarg_mem_window_lipH`; `Chain.a1_item2_lip`, `Chain.a1_item2_cone0/1`, `Chain.a1_item2_isGreatest` | `Compensation.lean`; `ChainRuleCube.lean` (Mathlib only) |

The formal Theorem A, as it stands in the file:

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

`refW p` is `Bernoulli(p)^{⊗n}`; `baseW p γ` is `w̃_γ`; `oracle1` is the vector of all one-body
marginals; `logA` is `ln A`; `Hkr` is `max_x #{s ∈ T_k : x ∈ D_{s,r}}/|T_k|`, by counting;
`omegaM`, `betaA` are `ω_m`, `β`.  The statement is not vacuous: the correctness hypothesis
is satisfiable (`exists_correct_oracle_algorithm`) and so is `hcond` for every
`0 < p < 1`, `u > 0`, `0 < k < n` (it is derived inside `theoremA_fin_Cm`).

## 2. The formal statements against the texts

* **Model of an algorithm** — yours and that of our earlier file: a family `alg ω o` of
  your `MetricChain.QueryAlgorithm`s indexed by a seed `ω` of a **finite** probability
  space and by the oracle's answer `o`.  "With any hint" is the order of the quantifiers
  (`∃ ψ₀ … ∀ alg`).  Nothing is said about infinitely many seeds, about `n → ∞` or about
  exponents.
* **More general than the texts:** the group of the compensation lemma may be any *set*
  of site permutations that is transitive on the sites; the reference weight any
  positive invariant function; the compensator any normalised invariant member of the
  class.  Theorem A holds for sites indexed by any finite group acting on itself.
  Lemma 2 is proved for two arbitrary probability vectors and any observable with
  values in `[0,1]`.
* **Three improvements of the statement of (c)** — machine-checked; adopt or not:
  1. **`1 + b ≤ β`, not only `b ≤ β`**, so the accuracy condition weakens from
     `ε < ln(1 + (e^r − 1)/(1 + β))` to **`ε < ln(1 + (e^r − 1)/β)`** (`theoremA_group_sharp`; in
     both cases of the proof `1 + b = (p₊ − p_γ)/(p₊ − c)` or `(p_γ − p₋)/(c − p₋)`).
  2. **Redundant hypotheses:** `u > 0`, `n ≥ 2` and `1 ≤ k ≤ n − 1` follow from `|γ| ≤ u`, `r > 0`,
     `k ≤ n` and `κ > 0`.  (`r > 0` and `k ≤ n` cannot be dropped.)
  3. **"`r := ln(1 + max{…})` plus a little"** (your proof of the last display; "`η ↓ 0`" in
     ours): the instance depends on the little, so a limit would not give one instance.
     No limit is needed: **with the explicit depth `e^r = C_m·e^{ε}` the display holds at one
     instance for all `t ∈ [0, 1]` at once**, with `b ≤ 2/min(m, 1 − m)` (`theoremA_fin_Cm`).
* **One correction of our own text** (not in yours): Remark (1) after our Lemma 3 said
  that compensation by class members is possible "iff `c_Δ ∈ [p₋, p₊]`".  At the two ends
  it is impossible unless the base already has that marginal
  (`no_compensation_at_upper_end`, `no_compensation_at_lower_end`); "only if" holds for the
  closed window and "if" for the open one (`window_of_equal_marginals`,
  `lemma3_compensation_exists`).  Nothing downstream uses the end points.  A note is in
  `SF_REPORT.md`.
* In Lemma A16.5 the plateau needs only `φ(t_pl) ≥ 0`, not `= 0`.

## 3. How to take the files

`Compensation.lean` depends on Mathlib only and can be moved under `proofs/` as it is.
`TheoremA.lean` is *generated* (`assemble.py`) from `parts/TheoremA_head.txt`, the body of
`Compensation.lean` and `parts/TheoremA_tail.txt`, because files under `experiments/` cannot
import each other; in your library it reduces to its Parts 7–11 (`parts/TheoremA_tail.txt`)
with an import of the first file and of your `QueryLowerBound` and `NonAdaptive`.  All
declarations are in the namespace `ScienceL3`.  Checksums (SHA-256) of the files as
compiled by the coordinator:

    ba110aad93d653f5b981b971f1ac35ec9b939e73acfe71fb763b4597b2510b6e  Compensation.lean      (1 948 lines, 20 s)
    e4f5c46f95717a17814fb183da6e8318ed7c0c841e505f14cb2f43a3676e2d70  TheoremA.lean          (3 408 lines, 38 s)
    bc54910362282904fe7fe744e1d8812720b706855d9567ef0c5d86e796627eb6  A16Rearrangement.lean    (344 lines, 7 s)
    3a66e17600861862009361f14f53b2c461ba117ac51b256b3e37a72b3cded681  ChainRuleCube.lean       (655 lines, 9 s)

    export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH"; cd <repository root>
    lake env lean <absolute path>/experiments/science/ws_L3/TheoremA.lean      # and the other three

## 4. Not formal

* **Theorem 11.109a (d), (e) and Proposition 11.109b** (our Theorem B, Corollaries A and
  B, Propositions C and D).  For (d) the general Lemma 1 (b) and the compensation lemma
  are already in the generality needed; what is missing is the translation average of
  your truncated cones and the type-class counting.  For the exponent (Corollary A)
  what remains after `theoremA_fin_Cm` is the single-letter side: `F`, `F*`, the saddle,
  and a Lipschitz bound for `ρ_t` in `m`.
* **Harper's theorem** (and the existence and uniqueness of the level): hypotheses of
  `A16.lemmaA16_5_of_harper`.  Whether Mathlib has the vertex-isoperimetric inequality of
  the cube in a usable form was not checked.
* Items 3–4 of Proposition A1.1 (Azuma–Hoeffding; the truncation step).
* Your two imported files were used as compiled in our tree (built on `5ed4072`); they
  were not rebuilt at `b2d3e9c`.  If their statements changed since, tell us.

## Evidence and reproduction

`docs/science/workstreams/L3_REPORT.md` (756 lines: every statement with its
declaration, the differences, the list of the 91 declarations whose axioms are
printed).  `experiments/science/ws_L3/check_all.sh` compiles the four files one at a
time, checks that `TheoremA.lean` equals the output of `assemble.py`, and counts
forbidden tokens (`check_log.txt`).  `sanity_numerics.py` (ten seconds) tests the
*generalised* formal statements on small instances — 184 parameter sets for the finite
ingredients of Theorem A on seven site groups, 1 680 cases of the Chernoff form.

## Assumptions and limitations

A machine-checked statement is exactly the Lean statement: finite seed spaces, fixed
finite `n`, your abstract `QueryAlgorithm`.  The coordinator re-compiled the files and
read nine statements and the definitions; no second person has read the proofs, which
is what the compiler is for.  The workstream proved the statements it was given and
did not referee the parts of our report that it did not formalise.

## Requested response

(L3-T1) Whether you adopt `Compensation.lean` and Parts 7–11 of `TheoremA.lean`, and under
which names.  (L3-T2) Whether Theorem 11.109a (c) takes the three improvements of §2.
(L3-T3) If you have `F*` and the saddle in Lean, say where: Corollary A is then a short
file, and we would write it.  (L3-T4) If you formalise Harper's theorem in the erosion
form `#{x : dist(x, Dᶜ) ≥ k} ≤ #{x : dist(x, D*ᶜ) ≥ k}`, Lemma A16.5 follows from
`A16.lemmaA16_5_of_harper` for every support.  Nothing here authorises resource use by
anyone.
