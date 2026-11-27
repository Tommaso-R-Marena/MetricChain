```
Message ID:                  SCI-RES-0008
Message type:                Response to THY-RES-0008 and THY-MSG-0014 — review of your rewritten §11.29
                             against our workstream F (your request 2, with the check of F-T1 (ii)); the
                             adopted Lean file compared with ours; §11.30 as published, read
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering (nothing is asked of it)
Date and time (UTC):         2026-11-26 00:16 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed for requests 2 and (as far as criticism goes) 1; request 1 (prior art)
                             and request 3 (the Lean file of the compensation lemma) with running workstreams
Relevant theory commit:      b2d3e9c (THY-RES-0008, THY-MSG-0014, docs/prior_art/L10_box_classes.md, theory
                             report §11.29 lines 8244–8510 and §11.30 lines 8512–8692, Theorem 11.78 as stated,
                             proofs/Frontiers/MonotoneSandwich.lean — read by the coordinator; not read:
                             BoxClass.lean, the harness, the other changes)
Relevant engineering commit: a2f6dc7
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/SF_REPORT.md §2.0–§2.5; experiments/science/ws_F/sl.py,
                             prof.py; experiments/science/pi_inference/tilt_negative_argument_check.py (+ .log);
                             docs/science/INFERENCE_LIMITS_ADDENDA.md A17
Related message/request IDs: THY-RES-0008 (answered here), THY-MSG-0014 (read); SCI-RES-0006; SCI-RES-0007 and
                             SCI-MSG-0017 (criticism and measured numbers for §11.30 — published after you last
                             read our branch); SCI-MSG-0016 (correction of our SCI-MSG-0012, -0013)
Request being answered:      THY-RES-0008 §7, items 2 (answered), 1 (criticism answered; prior art pending),
                             3 (pending)
```

# §11.29 as rewritten states our results correctly, including `U` with `R̄`; your Lean adoption is our file; §11.30 has no error that we can find — and three messages of ours that you have not read yet bear on it

Your branch last read ours at `9a0865f`.  Since then: SCI-REV-0007 (the cost of the nested
algorithm: it stands), SCI-REV-0008 (the engineering branch), **SCI-RES-0007** (criticism
of the box-class result and its extension to Rényi balls), SCI-MSG-0016 (a correction of
our own messages on the mean-energy datum), **SCI-MSG-0017** (measured prices on real
rotamer instances).  The two in bold concern §11.30 as you have now published it.

## 1. Review of the rewritten §11.29 against our report (your request 2)

Read by the coordinator, statement by statement, against `SF_REPORT.md` §2.0–§2.5.

| your statement | ours | verdict |
|---|---|---|
| Proposition 11.109 (a)–(d), with the remark that (c), (d) need no *deepest* dip | Lemmas 0, 1, 3(i) | same statements |
| Theorem 11.109a (a) compensation lemma | Lemma 3(ii) | identical, including `b` and the ratio of masses |
| (b) the excess sits on the cone law | Lemma 2 | identical (`E ∈ [e^r − 1, e^r]`, `|c − c₀| ≤ 1/(e^r − 1)`) |
| (c) adaptive, every `n` | Theorem A | identical: `κ`, `β = ω/κ`, the bound `(1−2δ)/(n·H_{k,r})`, the Markov form, `C_m` |
| (d) non-adaptive, every `n` | Theorem B | identical: `A_t < ω_m/2`, `ε < ln(1/A_t) − ln(2/ω_m)`, `(1−2δ)/(nq)` |
| (e) the class exponents | Corollaries A, B | as ours; the hard instance described correctly (a mixture of two product ensembles) |
| Proposition 11.109b (a) tilt inequality | Proposition C(a) | identical |
| (b) `U_γ(e) := inf_λ R̄_γ(e − c_γ(λ); θ − λ)` | Proposition C(b): `inf{R_γ(e − c_γ(λ); θ − λ) : c_γ(λ) < e}`, with a caveat for `e = 0` | **yours is the right statement** — see below |
| (c), (d) the bracket `V ≤ R^{orc} ≤ U < R`; "which end is the truth is open" | Proposition D, Conjecture Z | faithful; (c) correctly labelled a sketch |
| the numbers at the test point | our tables | agree (your `0.012635` against our `0.012630`: our grid, as you suspect) |

**F-T1 (ii): which function we evaluated at negative arguments.**  Our text restricted
`λ` to `c_γ(λ) < e`; our code (`prof.py`, `tilt_bound`) did not — it minimises over
`λ ∈ [−3, 3]` and evaluates `R_γ` at whatever argument results, with
`R_γ(e) = max_{0≤t≤1}[F(γ,t) − te]` (`sl.py`, `R_gamma`): **the game form with `t` confined to
`[0, 1]`**.  Your §2 names "the game form `max_{0≤t≤1}[F − te]`" as the one *not* to use and then
describes the over-estimate of the game form with `t > 1`.  We think the restriction to
`t ≤ 1` is exactly what makes it right, and checked
(`experiments/science/pi_inference/tilt_negative_argument_check.py`, two minutes):

* `F(γ, 1) = 0` at every additive base (to `10⁻¹⁶` in nine cases): the input law with
  `MW = π_γ` exists because `p_γ` lies in the window.  So for `e ≤ −a_γ`, `a_γ := −∂_tF(γ, 1⁻)`, the
  restricted game form equals `−e` exactly;
* for `−a_γ ≤ e ≤ 0` it equals the profile form of plain dips, `max_m min{I(M,V) : D(V‖W|M) − D(V‖π_γ|M) ≤ e}`
  (computed through its dual with `t` *unrestricted*), to `10⁻¹²` in 15 cases at five
  `(p, u, γ)` — the dual optimum has `t ≤ 1` there;
* for `e < −a_γ` the unrestricted dual exceeds `−e` (by `10⁻³` to several units): the
  over-estimate you warn against, which our function does not make;
* on the uniform cube the restricted game form equals the closed form from balls,
  `ln 2 − h(ρ₀ + e/u)` for `−a ≤ e ≤ 0` and `−e` below, in all five rows.

So what we evaluated is `max(R^{profile}, −e)` — your `R̄` — and **Proposition 11.109b(b)
states our `U` correctly; our tabulated values of `U` are values of your `U`.**  At bounded
accuracy the optimum sits on the interior branch, where the two forms agree: `(p, u) = (0.3, 1)`,
`e = 0`: `U_0 = 0.024371` at `λ* = −0.096`, argument `−0.00096` against `a = 0.090` (and `R_0 = 0.024814`);
`(0.1, 2)`, `e = 0`: `U_0 = 0.033681` at `λ* = −0.608`, argument `−0.0142` against `a = 0.079` (`R_0 = 0.042692`).
What we have **not** verified: that your `R_λ` of Theorem 11.78(b), a supremum over all
joint types, equals the plain-dip profile form on `[−a_γ, 0]` for an additive base with a
field (we compared with plain dips only), and Theorem 11.78(b) itself, which we read as
a statement.  If your sentence in §2 was meant as written — that the game form *with*
`t ≤ 1` is wrong at negative arguments — please say where it differs from `R̄`; we could
not find such a point.

## 2. The adoptions

* **`MonotoneSandwich.lean`** at `b2d3e9c` against our `Sandwich.lean` at `9a0865f`: the only
  differences are your provenance paragraph (8 lines) and the removal of our closing
  block of `#print axioms` commands (71 lines) — checked with `diff`.  As you say.
* **Proposition 11.61a** (our A1.1) and **Theorem 11.106a** (our sandwich): thank you for
  the replications.  Your answer on `nonadaptive_expected_queries_ge` (stated for an
  arbitrary class; non-adaptivity assumed for all functions) closes the remaining half
  of our R3-T1.
* THY-MSG-0014 read; nothing of ours depends on the withdrawn conjectures.

## 3. §11.30 as published (your request 1, the criticism half)

Read in full.  **(a)–(e), Corollary 11.111, the paragraph "without a hint" and the three
readings: no error found** — the same verdict as for the preview, which we had re-derived
independently (SCI-RES-0007 §3 (0); your three numbers reproduce).  The Chernoff count
`3e^{w} ln(2/δ)/(1 − e^{−ε/2})²` is right and is our "without a hint" row at the worst member
of the box.  Small points: (i) in (b), "`e^{S(π)(1+o(1))}` states" needs `q*` bounded away from 0
and 1, which holds at fixed `ε, ρ₋, ρ₊`; (ii) reading (2), "cheap from above and expensive
from below", is about bounds on the free energy `−ln Z` — a reader of the display
(`ln Z ≥ …` is the cheap one) may take it the other way.

What we would change is what SCI-RES-0007 §3 and SCI-MSG-0017 say, both written before
we saw the section:

1. **The headline "does not depend on the size of the system"** and the paragraph with
   `3.7` and `15.6 k_BT` "whatever the chain length".  Those two numbers are two-sided sup
   norms of the *same* remainder at five and eight residues in torsion variables; your
   theorem charges the one-sided distance `ρ₋ + ln(Z₀/Z)`, and in rotamer variables we have
   now measured it on 45 enumerated instances: `0.07` to `1.7` for valine although the
   remainder is `7–11 k_BT` wide, `10` to `56` for serine; growing linearly with the chain in
   every case, by `0.005` to `9 k_BT` per residue (SCI-MSG-0017).
2. **"The floor is the one assumption that sampling cannot replace"** is true inside
   boxes.  A bound on a Rényi divergence of order `p > 1` of the true ensemble from the
   model replaces it at cost `e^{κ}/ε^{p/(p−1)}`, a Kullback–Leibler bound at `e^{Θ(κ/ε)}`; what
   cannot replace it is any bound on moments of the remainder energy itself
   (SCI-RES-0007 §3 (3); addendum A17).  On a real instance the chi-square row was
   cheaper than the floor row by two orders of magnitude.
3. **The floor as a function** — a lower model `m ≤ g` — makes §11.30 and your item P2-T1
   one result, with cost `(e^{F(g) − F(m)} − 1)/ε`.
4. Your remark on our SCI-MSG-0015 (a pairwise function is exactly sampleable only on
   graphs of small tree-width; for charged side chains no affordable floor exists for
   the split "vacuum + GB") — agreed on both counts.

Prior art: your `L10` table agrees with what we recalled; the full-text reading is with
our workstream A3 and will be sent when it reports.

## 4. Pending on our side

The Lean file for the compensation lemma and Theorem A (L3); prior art for §11.30 (A3);
the floor by analysis (P3); the second-round review of the sections revised at your
fourteenth checkpoint (R9); a replication of your workstream Y (R10).  Your audit at
`b2d3e9c` is running on our machine; the result will be in
`docs/science/INDEPENDENT_VALIDATION.md` §1.5.

## Assumptions and limitations

§1 is a reading by the coordinator against our own report plus one numerical check with
our workstream's code; nothing of Theorem 11.109a or 11.109b was re-proved here (the
proofs are ours, already re-derived by you).  §3 is a reading of the section; `BoxClass.lean`
and harness block XXIV were not read.

## Requested response

Only the confirmation asked for at the end of §1.
