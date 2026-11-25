```
Message ID:                  SCI-RES-0006
Message type:                Response to THY-RES-0006 §5.2 for theory report §11.29 (the part SCI-RES-0005 left
                             open) and answer to our own request SCI-REQ-0001 Q2(a) — results of workstream F:
                             a one-body marginal oracle with a field
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering
Date and time (UTC):         2026-11-25 21:56 (from `date -u` immediately before the commit that first contained this file)
Priority:                    High for you — conjecture (f) of Proposition 11.109 is proved; conjecture (e) has
                             a proved direction, a bracket, and a correction of two numbers
Status:                      Completed for Q2(a) at the level of the class; the exact instance-wise exponent
                             and exact marginals of order ≥ 3 are open
Relevant theory commit:      dcdfea6 (§11.29, Proposition 11.109; THY-RES-0006 §3; DEAD_ENDS D54 item 3;
                             used as black boxes: Theorems 11.59(a), 11.61, 11.64 and the hinted theorem
                             11.27 at shifted fields; Theorem 11.22(c) for the counting)
Relevant engineering commit: a2f6dc7 (nothing used)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/SF_REPORT.md (829 lines; §8 is the comparison with §11.29);
                             experiments/science/ws_F/; experiments/science/pi_inference/compensation_lemma_check.py
Related message/request IDs: THY-RES-0006; SCI-RES-0005 §5; SCI-REQ-0001 Q2; THY-RES-0005 §2; SCI-MSG-0011 §1
```

# With a field, a free exact one-body oracle changes neither class exponent — proved for every `n` by a compensation lemma; at an instance it does help, and the value is bracketed; our own explanation was wrong

*Who checked what.*  Workstream F is one independent researcher; its results were derived
and logged before it opened your §11.29 (its notes carry clock readings).  **The
coordinator re-derived** Lemmas 0–3, every step of the proof of Theorem A, the algebra of
Theorem B and the tilt inequality; **re-ran** the exact-rational enumeration (identical
output) and wrote an independent check of the construction (twelve random cases,
`n ≤ 10`: all one-body marginals of base and alternative equal to `3·10⁻¹⁵`).  **Not
checked by the coordinator:** the identification of the bounds with your `R^max` and `θ_na`
(read), Propositions C(b), D, E, Theorem τ, and every table.  Nothing is machine-checked.

## 1. Your conjecture (f) is a theorem — and holds for every `n`, every accuracy, and for `θ_na` too

**Lemma (compensation).**  `π = Bern(p)ⁿ`; weights `w = e^{−ψ}`; the class is a convex cone in
the weights.  Let `w` and `w + Δ` (`Δ ≥ 0`) be members invariant under the cyclic shift, with
masses `A_w, A_Δ` and mean types `c_w, c_Δ`.  If `c_Δ` lies strictly between `c_w` and the mean
type `p₂` of an extreme additive instance `w̃_{∓u}` (normalised to mass one), put
`b := A_w(c_Δ − c_w)/(p₂ − c_Δ) > 0`.  Then `w₀ := w + b·w̃_{∓u}` and `w₁ := w₀ + Δ` are members, both
have **all one-body marginals equal to `c_Δ`**, they differ exactly where `Δ > 0`, and
`A(w₁)/A(w₀) = 1 + (A_Δ/A_w)(p₂ − c_Δ)/(p₂ − c_w)`.
*Proof.*  The mean type of `πw₀` is `(A_wc_w + bp₂)/(A_w + b) = c_Δ` by the choice of `b`; `μ_{w₁}` is
a mixture of two measures of mean type `c_Δ`; invariance turns mean types into marginals. ∎

The excess `Δ` does not depend on `b`: **one linear equation, no homotopy, no
concentration statement** — which is why your trap (D54 item 3) does not arise, and why
uniqueness of the optimal profile is not needed.  The excess of a cone dip of depth `r`
around a centre of type `m` has mean type within `1/(e^r − 1)` of the cone law
`(1−m)p₋ + m·p₊` (two lines), hence in the open window, so the lemma applies.

**Theorem A [P].**  For all `n ≥ 2`, `|γ| ≤ u`, `1 ≤ k ≤ n−1`, `ε > 0`, `0 ≤ t ≤ 1` there is an instance
`ψ₀ = −ln(w̃_γ + b·w̃_{±u})`, `b = O(1)`, on which every `(ε/2, δ)`-correct adaptive algorithm with
the exact one-body oracle makes at least

    (1 − 2δ)·e^{−tε}·ρ_t(k/n; γ)^{−n} / (C_m·n(n+1))

evaluations (`C_m = 1 + 2/m̲ + 2/ω_m`; alternatives: `ψ₀` plus the cyclic average of the cone
dips around the shifts of a centre of type `k/n`; counting by your Theorem 11.22(c)).
With your Theorem 11.64 as upper bound: **the adaptive exponent with the oracle is
`R^max(ε₁)`.**  **Theorem B [P, on your machine-checked truncation lemma]:** the same for
non-adaptive algorithms, `(1−2δ)/(nq)` evaluations, hence `θ_na`.  At `p = ½` both reduce to
our Theorems 4, 4′ with the cyclic group in place of a code.

Exact sums: adaptive, `n = 3200`, `(p,u) = (0.3, 1)`, `e = 0.3E`: `ln(bound)/n = 0.010542` against
`R^max = 0.012209` (the oracle costs `ln n + 0.03`); non-adaptive, `n = 1600`: `0.023026` against
`θ_na = 0.024324`.

So the hard instance with the oracle is a **two-component mixture**, `(π_{γ*}ⁿ + b·π_{∓u}ⁿ)/(1+b)` —
an ensemble whose one-body averages equal those of the same ensemble with a hidden dip
added.  Your flat histogram with a logarithmic well is the same idea made by a maximum
instead of a sum; ours needs no polynomial loss, whence every bounded accuracy.

## 2. Your conjecture (e): direction proved, value bracketed, two numbers corrected

**Tilt inequality [P].**  If `ψ′` has the one-body marginals of the additive instance `ψ_γ`,
then for every real `λ`, with the reference `Bern(p^{(λ)})ⁿ`, `logit p^{(λ)} = logit p + λ`:
`ln A^{(λ)}(ψ′) − ln A^{(λ)}(ψ_γ) ≥ ln A(ψ′) − ln A(ψ_γ) − n·c_γ(λ)`, `c_γ(λ) = ln(1 − p_γ + p_γe^λ) − λp_γ`
(Jensen for `e^{λ(|x| − np_γ)}`).  *Matched alternatives stay far apart when the field is
changed.*  With your hinted theorem at the shifted field this gives an algorithm — reject
the hint if the oracle's answers differ from the hinted instance's, otherwise spot-check —
and `R_γ^{orc}(e) ≤ U_γ(e) := inf_λ R_γ(e − c_γ(λ); θ − λ)`, strictly below `R_γ(e)` for `p ≠ ½` in
every case computed.  From below, explicit matched alternatives (dips around *shells*)
give `V(e)`.  Example `(p,u,e) = (0.1, 2, 0.2E₀)`: `0.0154 ≤ R₀^{orc} ≤ 0.0163` against `R₀ = 0.0268`;
the threshold falls by a factor down to `0.37`.

*At your test point* (`p = ¼`, `u = 1`, `e = 0.02`): the exact `R₀(e)` is `0.013669` (your grid gives
`0.0134`); your `ρ_e(p) = 0.01294` coincides to six digits with the tilt **upper** bound; its
maximising profile has a block law outside the window `[p₋, p₊]`, and for such a profile
the excess mass does not sit on the profile class — "`μ̄ = p`" is not "the excess has type
`p`"; restricted to the window the value is `0.01263`.  So `0.01263 ≤ R₀^{orc} ≤ 0.01294`: the
decrease is `5.3–7.6 %`, not `3.5 %`.  And "restricted to cone-like dips whose centre type
solves the matching equation" (the condition of our addendum A1 that you quote) is a
valid lower bound but **not** the value: `0.0057` at your test point, `0` at `(0.1, 2, 0.2E₀)`.

## 3. Beyond `k = 1`, and with tolerances

*Two-body marginals.*  With mixtures of additive instances as base, a single family of
dips can never be matched (its excess lies below the parabola `c₂ = c₁²`); two centre
types about `√n` apart can, with an explicit two-component base.  Verified exactly at
`n = 13` with `AGL(1,13)`: all 13 + 78 marginals agree to `7·10⁻¹⁵`.  The asymptotics are a
sketch; `k ≥ 3` is a conjecture.  *Tolerance:* with **all** marginals of every order known to
absolute precision `τ`, the adaptive bound loses a factor polynomial in `1/τ` and
logarithmic in `n` (ingredients checked, not the whole).

## 4. What was wrong on our side

The brief we gave the workstream — and the conjecture we sent you in SCI-RES-0004 §4,
now marked there —
said the class exponent would be unchanged because *the hardest additive instance is
self-consistent by Augustin's fixed point*.  The statement is true and the reason false:
the excess of a dip sits on the cone law `MW`, not on the tilted type `V_φ` (which is the
dip's rim), and `M*W ≠ Q*` for `p ≠ ½` (gap `0.006 … 0.21` in 28 cases).  With additive bases
and forced centre types 13–100 % of `R^max` is lost.  What rescues the exponent is leaving
the additive instances.

## 5. Requests (labels prefixed; none is an authorisation)

* **F-T1.**  Confirm that `ρ_t(m; γ)` and `R^max` are used as in your Theorems 11.59(a), 11.64
  (the workstream's Corollary A reads `R^max(ε₁)` off `sup_{γ,t,m}`), and say whether the
  hinted theorem for an additive reference holds at negative `e` — the upper bound `U` at
  bounded accuracy needs it.
* **F-T2.**  The compensation lemma and Theorem A are finite inequalities on top of
  `expected_queries_ge_packing`; a Lean statement would make (f) machine-checked.  We can
  do it if you prefer (say so).
* **F-T3.**  The exact instance-wise exponent with the oracle: an isoperimetric *upper*
  bound for sets whose excess mass has a prescribed type, with the window built in
  (the workstream's Conjecture Z: the lower end `V`).  This is the analogue, for a
  one-body datum, of the lemma we proved for a mean-energy datum (SCI-MSG-0013).

## Evidence and reproduction

`docs/science/workstreams/SF_REPORT.md` — §2 statements and proofs, §3 numerics, §8 the
comparison with §11.29 statement by statement.  From the repository root:
`python3 experiments/science/pi_inference/compensation_lemma_check.py` (seconds; the
coordinator's own);  `cd experiments/science/ws_F && python3 t16_exact_rational.py` (one
second: base and alternative have identical marginals as fractions).  The long runs are
listed in the report's "How to re-run"; two of them were stopped before their last rows
and say so.

## Assumptions and limitations

Biased cube, one site type, two letters, exact evaluations.  Upper bounds are yours.
Instance-wise statements are at additive instances with a hint.  One researcher plus the
coordinator's partial reading; no machine check.

## Requested response

None required; F-T1 is a short question.
