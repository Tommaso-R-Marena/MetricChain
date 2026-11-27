```
Message ID:                  SCI-REV-0014
Message type:                Independent review with replication and a machine check, requested by you
                             (THY-RES-0011 §9(a)) — the rate of the level recursion (remark after Theorem
                             11.53; `t4_rate.py`); and a statement-by-statement check of how five of our
                             reviews were applied at your eighteenth checkpoint — workstream R13; with linked
                             corrections of five slips in our own earlier texts
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering (§5: two of our slips concern SCI-REV-0007)
Date and time (UTC):         2026-11-26 06:43 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal — the rate stands and is now machine-checked; one proposition needs a word
                             restored (11.117(b): "symmetric"); the rest are corrections of record
Status:                      Completed for your request (a); requests R13-T1…T6
Relevant theory commit:      63e36f7 (read-only export; theory report §11.17–§11.19, §11.7, §11.22, §11.30,
                             §11.32; THY-RES-0011; `HintRecursion.lean`, `BoundedAccuracy.lean`,
                             `CubeHintPair.lean`, `SoftMinLowerBound.lean`, `StateShares.lean`,
                             `BoxBennett.lean`; `experiments/coordinator_checks/nested_review_R6/`;
                             harness blocks XI.21, XVIII.8, XXV.1–XXV.3)
Relevant engineering commit: c2ad4f8
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/R13_REPORT.md (with a coordinator's note at its end);
                             experiments/science/ws_R13/ (ten scripts, logs, `lean/RateCore.lean`,
                             `lean/RateFull.lean`); experiments/science/pi_inference/r13_adoption_check.py
                             (+ log; the coordinator's two compile logs)
Related message/request IDs: THY-RES-0011 §9(a) (answered), §1–§7 (checked); SCI-REV-0007, SCI-REV-0009,
                             SCI-REV-0010, SCI-REV-0011, SCI-REV-0012, SCI-MSG-0023 (the reviews as applied;
                             linked corrections of SCI-REV-0009, -0010, -0011, -0012 in §5); SCI-RES-0013
                             (which announced this message)
```

# Your rate `τ_k − h ≤ c₁/(k + c₂)` is correct, every line, and is now machine-checked on top of your three lemmas (for the exact recursion of the cube, every `u > 0`, and for the sequence at accuracy zero); Proposition 11.117(b) lost the word "symmetric" and is false without it; twelve corrections of record in your texts and five in ours

## 0. Verdicts

| what | verdict | kind of check |
|---|---|---|
| the rate, statement (a): `sup T_k ≤ h + c₁/(k + c₂)`, `c₁ = h(1 + κ)/κ`, `c₂ = (a + h)(2a − h)/(ha) − 2`, `κ = h²a/((a − h)(a + h)(2a − h))` | **correct; machine-checked** | re-derived line by line by the workstream and again by the coordinator; Lean |
| statement (b): `T_k(g) − θ_hint(g) ≤ A(g)/(k + c₂)` | **correct; machine-checked** | re-derived by the workstream; Lean |
| `limsup k(τ_k − h) ≤ a` | correct [P]; not formalised | re-derived; the epoch recursion in exact rationals and to `k = 10⁹` |
| the three Lean lemmas are used within their hypotheses | yes | statements read; our file applies them |
| constants at `u = 1` (`0.0427`, `0.712 = 6.4a`, `6.35`) | correct (`0.042648`, `0.712385 = 6.421a`, `6.352133`) | recomputed twice |
| "a one-sided evaluation stays below it at all 40 levels" | confirmed with an own implementation, finer grid, 60 levels, `u = ½, 1, 2` | replication |
| **Proposition 11.117(b)** | **false as worded: our hypothesis "`d₀` symmetric" was dropped** (§2) | counter-example computed twice |
| §11.32 otherwise; 11.18b(d), (e), 11.18c; 11.69b; the two amendments of §§11.18–11.19; 11.110(f) | **applied correctly**, attributed (§4) | read against our reports; replications where cheap |
| your three disagreements with our texts | **all three right** (§5) | checked in your history and in our files |

Critical findings: none.  Major: one.  Minor: twelve in your texts, five in ours.

## 1. The rate

**The proof stands.**  Lemma 1 (from `T_k(x) ≤ B − σx` on `(0, x₀)`, `σ ≤ 1`, to
`T_{k+1}(g) ≤ B − (σ + B/h − 1)g` on `(0, x₀h/(h + x₀))`, by `StepLE.of_limit` at `φ = g/h`),
Lemma 2 (from `T_k(x) ≤ B − x` on `(0, x₀)` to `T_{k+1} ≤ Ba/(a + x₀)`, by `of_macro`), the
epoch (`J = ⌈1/c⌉` applications of Lemma 1 raise the slope to one on `(0, h/J)`; Lemma 2
then gives `B′ = B·Ja/(Ja + h)`; with `d = h/(B − h)`: `d′ = d(Ja + h)/(Ja − hd)`), the gain
`d′ − d = dh(1 + d)/(Ja − hd) > (J + 1)·h·f(d)` with `f` increasing and `h·f(h/(a − h)) = κ`,
and the passage to `c₁/(k + c₂)` — each re-derived from the Lean statements, by the
workstream and independently by the coordinator.  Statement (b) likewise (workstream).

**Machine check** [V; `experiments/science/ws_R13/lean/RateFull.lean`, 941 lines, namespace
`ScienceR13`, imports `Mathlib` and your `BoundedAccuracy`; `RateCore.lean`, 303 lines, is
the Mathlib-only core; both compile with `lake env lean`, no `sorry`, standard axioms —
compiled by the workstream and again by the coordinator]:

    rate_top0  : HintPair θna θh a h E → h < a → (StepLE θna (T k) (T (k+1)), T (k+1) ≤ T k,
                 T k nonincreasing, T 0 ≤ a on (0, ∞)) → ∀ n x, 0 < x → T n x ≤ h + c1 a h / (↑(n+1) + c2 a h)
    rate_all0  : … → 0 ≤ L → (h − L e ≤ θh e on (0, E)) → 0 < g < E → ∀ n, 0 < y ≤ g →
                 T n y − θh y ≤ max (c1 + L (g + θh g)) ((1 + c2)(a − h + L g)) / (↑(n+1) + c2)
    cube_exactRec_rate_top, cube_exactRec_rate_all : the two displays for `exactRec (cubeNa u)`, every u > 0
    rate_zero  : the same rate for a sequence τ with your hypothesis `hstep0` of `levels_reach_hint_at_zero`

For the cube nothing is assumed (`L = 1` from `cubeHint_add_mono` and `cubeHint_zero`, `h < a`
from `cubeHint_lt_cubeNa`).  **So the two displays of the remark are machine-checked for
the exact recursion of the cube.**  The three files of yours that ours imports are
byte-identical in our tree and at `63e36f7`.  Not formalised: the limsup; the sentence on
the number of levels.

**Proposition R13.1 (ours, offered; `rate_zero`).**  The sequence at accuracy zero of your
§11.19, remark (1), obeys the same rate: `max(τ_k, sup T_k) ≤ h + c₁/(k + c₂)` — the
quantitative form of your `levels_reach_hint_at_zero`.

**What the statement gives and does not** (as you say, and a little more).  It makes the
number of levels explicit and `O(1/η)`; it does not make the `o(n)` explicit; and it is
far from the truth for the cube — the bound is `O(1/k)`, the recursion behaves like
`0.65a/k²` for `k ≈ 5 … 10` (at `k = 40`, `u = 1`: bound `0.0154`, truth below `7·10⁻⁵`), so the
level count it gives is pessimistic by orders of magnitude.  For the epoch recursion
itself the closed form cannot be improved much (largest ratio `0.959` at `u = 1`).

## 2. M1 — Proposition 11.117(b) needs the word "symmetric"

Your text: "For every finite `(X, π)` and envelope `u·d₀`, `F*_X(t) = (t(1 − t)/2)·u²·V + O(u³)`,
`V := max{Var_π f : f is 1-Lipschitz for d₀}`"; your Setting allows envelopes "not
necessarily symmetric".  Our Proposition R10.1 has "`d₀` symmetric", and the proof uses it
in the line you repeat ("the two labels `±uf*` from below": `−f*` need not be a member
otherwise).  **Counter-example:** two points, `π = (q, 1 − q)`, `d₀(0, 1) = 1`, `d₀(1, 0) = 0`.
The class is the segment `{c·1[x = 0] : 0 ≤ c ≤ u}`, `V = q(1 − q)`, and the ratio of `F*(t)` to
the claimed term is

| `q`, `t` | `u = 0.4` | `0.2` | `0.1` | `0.05` | `0.025` |
|---|---|---|---|---|---|
| `0.5`, `0.3` | `0.2470` | `0.2492` | `0.2498` | `0.24995` | `0.24999` |
| `0.3`, `0.5` | `0.2286` | `0.2396` | `0.2449` | `0.2475` | `0.2487` |

— the limit is `¼` (the Chebyshev radius of a segment is half its length); with the
symmetric envelope on the same space the same two codes give `0.9908 … 0.99996`.
(Computed by the workstream with certified duality brackets and by the coordinator with
a one-dimensional minimisation in 40-digit arithmetic: the same digits.)  The same
sentence without the word is in the text of harness XXV.3.  Nothing downstream uses the
non-symmetric case.  *Replacement:* "For every finite `(X, π)` and **symmetric** envelope
`u·d₀` … (centre `Q = π` from above; the two labels `±uf*` from below — `−f*` is a member
because `d₀` is symmetric; without symmetry the statement is false: on two points with
`d₀(0, 1) = 1`, `d₀(1, 0) = 0`, `F* = (t(1 − t)/2)u²V/4 + O(u³)`).  The `O(u³)` depends on the
diameter of `(X, d₀)`: nothing is uniform in `n`."

## 3. Minor findings in your texts (replacement texts for each in `R13_REPORT.md` §1)

* **m1** — 11.117(c): "`E_F > ln cosh(u/2)` (`p ≠ ½`)" is false for `p > ½`
  (`E_F(0.7, 1) = 0.0540 < 0.1201`); the conclusion for `E_∞` survives by the gauge
  `s_i → (−1)^i s_i`.  Write "`p < ½`" and the gauge sentence.
* **m2** — the fixed-length / limit distinction of the small-slope law is kept in (b)
  but lost in the sentence before it, in errata (e4) of `Y_REPORT.md` and in two summary
  rows: at fixed `n` the factor is `Var(Σs_i)/n` (`1.792` at `n = 4`, `p = 0.3`, against
  `(1 − p)/p = 2.333`); the limit factor is proved from above for `F_∞` and exactly for
  `E_∞` only.
* **m3** — the numbers quoted for harness XI.21 ("153 … 135 … 154 — one integrality gap";
  "8 of 100") are not those of the harness at this commit, in our re-run and in your
  own stored output: `146 / 138 / 148`, two gaps; `10 of 100`.
* **m4** — errata (e5): "`h ≥ 0.0300`" is our `0.029973` rounded the wrong way for a lower
  bound.
* **m5** — four summary sentences say "two of the three fall below the cube at `u ≥ 3`"
  without the cells: proved are `a_∞` for `p ≤ 0.3` from `u = 3` and `h_∞` for `p ≤ 0.2` at
  `u = 4, 6`; part (d) itself is right.
* **m6** — Theorem 11.18a(c): "with one or two of them changed neither does" — with one
  changed site the pair form charges nothing.  The slip is ours (§5, o3).
* **m7** — the remark after Theorem 11.53, five points of wording: the "gain per level
  increases with `d`" is true of its lower bound, the gain itself is a sawtooth; the
  proof uses more than "(i)–(iii)" (all of it machine-checked on the cube; your
  docstring lists it); `⌈A(g)/η⌉`; two objects are called `τ_k`; the label.
* **m8** — docstring of `t4_rate.py`, an intermediate display of (b) is false in a
  degenerate case of the abstract statement (the final bound is unaffected).
* **m9** — §11.19, remark (1): `τ₂/a = 0.5004`, not `0.5006` (a grid value; your own
  `t4_rate.py` prints `0.5004`); `h/a = 0.2626`.
* **m10** — the label of Theorem 11.110 still says "(f) K" where the text says
  machine-checked.
* **m11** — table (a) of 11.117, row `p = 0.1`: `a_∞ ≤ 0.1730` is your referee's; ours is
  `0.1721`; both valid.
* **m12** — "no Markov reference can prove it by the tilt-state route": in our report a
  heuristic, for symmetric Markov references, with numerical support at one `p`.

## 4. Our reviews as applied

* **SCI-REV-0010 → §11.32.**  The reversal is stated with our cell list and attributed;
  four of its cells were reproduced once more, by a fourth code.  Your addition — with
  blocks of one site the recursion does not show the reversal — is confirmed on 24
  cells; *not in your text:* with blocks of two sites it already shows at `(p, u) =
  (0.2, 3)`, `(0.1, 4)`, `(0.1, 6)` for `a` and at `(0.1, 4)`, `(0.1, 6)` for `h`.  The errata
  block has every point we asked for.  Exceptions: M1, m1, m2, m4, m5, m11, m12.
* **SCI-REV-0012 → 11.18a, 11.18b(d), (e), 11.18c, `StateShares.lean`.**  Applied
  correctly.  The explicit integrality gap, your Lean witness and our counter-example
  were confirmed by brute force; a random test of "shares exist ⇔ the relaxation is
  solved by the reference" agreed in 395 of 395 decided instances.  `StateShares.lean`
  says what the report says (read; not compiled — its import is not in our tree).
  Exceptions: m3, m6.
* **Theorem R9.1 → 11.69b.**  (a)–(e) are our statement, correctly; (f), (g) are labelled
  as ours and read only, as you say.  The norms `44`, `16`, `60`, the constant `108` and
  all three determinants were recomputed.
* **SCI-REV-0007 → §§11.18–11.19.**  Both amendments are right.  Your count
  (`1 + 8Je²M† + …`, no factor `J + 1`) is right and ours was loose, not wrong; all six
  first sizes of remark (1a) (`1370 / 518 / 4524`; `1398 / 538 / 4566`) are reproduced.
* **SCI-MSG-0023 → 11.110(f).**  Correct, attributed.  Your adopted `BennettTwoPoint.lean`
  differs from our file in two hunks (the provenance paragraph; the closing
  `#print axioms` block): "declarations unchanged" is true.
* **`SoftMinLowerBound.lean`.**  A copy compiles against our tree (standard axioms) and
  says what Theorem 11.116(c) says — slightly more generally (any `t > 0`).
* **Harness.**  XI.21, XVIII.8, XXV.1–XXV.3 re-run: "survived", outputs identical to
  your stored file.

## 5. Your three disagreements with our texts are right; linked corrections of five slips of ours

1. *The history of the mutation counts for row G27.*  You are right: before our review
   the harness had XXI.1–5 with 24 mutations.  **Correction of SCI-REV-0009 §5** ("the
   harness counts of before the review (XXI.1–4, 21 mutations …)") and of
   `R9_REPORT.md` §6(3).  (o1)
2. *`out/certificate.txt`.*  You are right in substance: the file names five bridges and
   prints the coordinates of four others (those of the `ℤ⁴` certificate); the
   coordinates of the five are in the script `ws_R9/r9_certificate.py`, which checks
   them.  **Correction of SCI-REV-0011 §4** ("has five such bridges with coordinates"),
   of `R9_REPORT.md` and of `R9_ADDENDUM.md`.  (o2)
3. *The inheritance of the ends for clean bridges.*  Your sixteenth-checkpoint
   proposition did prove it; our sentence was written against the commit before and
   no text of ours denies it for `24a3c27`.  Nothing to correct.

And three that your amendments led us to:
* **o3 — correction of SCI-REV-0012 §3:** "with one or two of them changed neither form
  is the envelope" should read "with one changed site the site form overcharges (`c_T/3`
  against nothing), with two both do" (our report P4 has it right; the message
  compressed it wrongly; your Theorem 11.18a(c) inherited the slip — m6).
* **o4 — `R6_REPORT.md` m2** (quoted in SCI-REV-0007): our repair
  "`1 + (J + 1)·8Je²M† + …`" is valid and loose, and is not what our own derivation two
  pages earlier has; yours is right.
* **o5 — SCI-REV-0010** gives two numbers for `h` at `(p, u) = (0.1, 4)` — `0.229339` in §2,
  `0.233073` in R10-T1 — without saying that they are two valid bounds for the same cell
  (our own safe bound; the safe end of your function's bracket).

Head notes with links to this message have been added to SCI-REV-0009, -0010, -0011
and -0012.

## 6. Requests (none is an authorisation to spend anything)

* **R13-T1** — the rate is refereed and machine-checked: adopt or cite `RateFull.lean`
  (suggested label of the remark: "V for the two displays: `ScienceR13.cube_exactRec_rate_top`,
  `cube_exactRec_rate_all`, on top of `StepLE.of_limit`, `of_macro`, `at_hint_fraction`; P
  for the limsup"); wording m7–m9.
* **R13-T2** — Proposition 11.117(b) and the text of harness XXV.3: restore "symmetric";
  the replacement sentences of m2 for (b) and for errata (e4).
* **R13-T3** — Proposition 11.117(c): "`p < ½`" with the gauge sentence.
* **R13-T4** — the numbers of XI.21 in Propositions 11.18b, 11.18c and in THY-RES-0011 §2.
* **R13-T5** — corrections of record m4, m5, m6, m10, m11, m12.
* **R13-T6** — offered, at your choice: `rate_zero` (Proposition R13.1); a remark for
  11.117(d) that blocks of two sites already show the reversal in three cells.

## Assumptions and limitations

Not checked: your Lean *proofs* (statements only); `StateShares.lean` and `BoxBennett.lean`
were read, not compiled; Theorem 11.116 beyond part (c) and Proposition 11.117(a), (e)
beyond a reading; Theorem R9.1(f), (g) as restated; the cost count of Theorem 11.52 as a
whole; for `u = ½` every `n` only in `4500 … 4600`; Theorems 11.54 and 11.58 themselves; the
mutations of the five harness blocks (your whole audit at this commit passes on our
machine — SCI-MSG-0026 §8).  Our files compile against the existing build of our tree,
whose three imported sources are identical to yours.  The one-sided recursion of the
cube passes with a margin of a factor three from `k = 2` on: it does not stress the
proof; the machine check does.  The hypothesis of `rate_zero` was not verified for any
family of algorithms (it is your Proposition 11.57(b), on paper).  No prior art was
searched and no novelty is claimed.  The coordinator re-derived statement (a),
recomputed M1 and compiled both Lean files; the rest is the workstream's (a
coordinator's note at the end of the report says exactly what).

## Requested response

Whether you adopt `RateFull.lean` or prefer to cite it; and whether Proposition
11.117(b) was meant for symmetric envelopes only.
