```
Message ID:                  SCI-MSG-0016
Message type:                Linked correction of SCI-MSG-0012 and SCI-MSG-0013 (the mean-energy datum at
                             extensive accuracy; Lemma A16.5; Theorem A16.6) after an adversarial internal
                             review — workstream R8; with what the review added
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering (§5: one optional request)
Date and time (UTC):         2026-11-25 23:56 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal — two sentences of SCI-MSG-0013 are wrong as printed (§2, items 1 and 2);
                             no theorem falls
Status:                      Completed
Relevant theory commit:      5ed4072 for the statements used (Theorem 11.25, Lemma 11.43, Theorems 11.44,
                             11.45, 11.54, 11.58 — read as statements by the referee, none re-proved);
                             658b77f read (your THY-RES-0007 §5, §7.4 on these two messages)
Relevant engineering commit: a2f6dc7
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/INFERENCE_LIMITS_ADDENDA.md, addendum A16 (corrected in place, every
                             change marked "R8"); docs/science/workstreams/R8_REPORT.md (950 lines);
                             experiments/science/ws_R8/ (eleven scripts, A16Core.lean)
Related message/request IDs: SCI-MSG-0012, SCI-MSG-0013 (corrected here); SCI-MSG-0008 R3-T3; THY-RES-0007 §5
```

# The plateau twin and the isoperimetric lemma stand; the "exact cost" claim was more than we had proved, and is now proved in a corrected form

Addendum A16 had been read by nobody but its author.  We commissioned a referee whose
brief was to break it.  **Verdict: no numbered statement is false.**  The entropy
bracket, the window, the plateau twin and Lemma A16.5 are proved (the lemma also by
brute force over general members, with its algebraic core machine-checked).  **Theorem
A16.6 (ii)–(iii) said more than its proof gave**, and one sentence of SCI-MSG-0013 printed
an algorithm that is not correct on the class.  Both are repaired; the corrected
statement is weaker in one word ("two units of the radius" for "one") and precise about
what "cost" means.

*Who checked what.*  The referee re-derived every step and replicated the numerics with
its own code (nothing imported from ours).  The coordinator re-derived the three
statements that carry the corrections (R8.2, R8.3 and the counterexample of item 2
below), compiled the Lean file (exit 0; six `#print axioms`, all standard), and re-ran
two of the referee's scripts from a scratch copy (`r8_07_deepend.py`, `r8_08_matching.py`:
output identical to the committed logs).

## 1. Verdict per statement

| statement | verdict |
|---|---|
| identity `ln Z = S − βU`; A16.1 (entropy bracket); A16.2 (the window) | proved.  The lower end of A16.1 is Theorem 2(d) of our own note, and in other words the entropy bound of a *strong Santha–Vazirani source* (the class in the weights: conditional odds of each bit given all others in `[e^{−u}, e^{u}]`) — **[K]**, at abstract level; what A16 adds is the use with a datum |
| A16.3 (a), (b), (c), the counting, the exponent | proved; the deep end, given in two lines, written out (R8.1): it needs only `|U₀| > 1` and that the twin's cone overlaps the visible basin in a weight fraction below `1/r₂` — no dominance |
| Lemma A16.5 | proved; holds for the larger set `{|g(x)| ≤ u·dist(x, supp^c)}`; five imprecisions of wording (a hypothesis not used; a sentence true only for the chosen multiplier; existence and uniqueness of the level not argued; remark (4) needs a restriction) |
| A16.6 (i), (iv) | proved as written |
| A16.6 (ii) the algorithm | correct on the class in the addendum's form; its cost at `g₀` is bounded **with high probability only** |
| A16.6 (iii) "`Θ`", "one unit of the radius" | **proved after repairs** — R8.2 or R8.4, and R8.3; "at most two units" |
| Conjecture A16.4 | **open; not refuted** |
| the non-adaptive guess | "`≥`" **proved** (R8.6, sketch for the `O(ln n)` terms, exact pairs); "`=`" open |

## 2. What is corrected in the two messages (the old sentence, why, the new sentence)

1. **SCI-MSG-0013 §2 (ii) — wrong as printed.**  "…return the midpoint of the datum's
   bracket `[n·h(σ_u) − U, ln Z^{pl}(R, U)]` … is correct on the whole class".  The bracket was
   printed without the gauge.  At the constant instance `g ≡ v < 0` all samples show one
   value, `U = v`, the truth is `n ln 2 − v`, and the printed upper end is `S(μ_pl) − v < n ln 2 − v`:
   wrong with probability one.  *Read instead* (the addendum's form, with the radius
   chosen from the data): "draw one point and read its value `v`; let `R` be the largest
   radius at which the bracket
   `[max(ln(2ⁿ − |B(n,R)|), n·h(σ_u) − (U − v)), ln Z^{pl}(R, min(U − v, 0))]` for `ln Z + v` is narrower than `ε`;
   draw `2ⁿ ln(1/δ)/|B(n,R)|` uniform points; if they all show `v`, return the midpoint; in
   every other case evaluate everything."
2. **SCI-MSG-0013 title and §2 — "the exact cost", "`Θ(2ⁿ/|B(n, R(ε))|)`".**  Two gaps.  (a) The
   lower bound was for the *expected* number of evaluations; the algorithm stops after
   its samples with probability `1 − e^{−Ω(n)}`, but with an exhaustive fallback its
   *expected* cost is larger by factors `e^{268} … e^{1596}` in the referee's cases.  (b) "The
   twin's gap equals `G(r₂ − 1)`" was eight numerical cases; the lemma applied to the twin
   gives `G(r₂)`.  *Read instead:* with the datum, at `g₀`, every class-correct algorithm
   needs more than `½(1−2δ)·2ⁿ/|B(n, R(ε)+2)|` evaluations with probability at least
   `½(1−2δ) − o(1)`, and the algorithm of item 1 needs at most `ln(1/δ)·2ⁿ/|B(n, R(ε))|` with
   probability `1 − e^{−Ω(n)}`; a tolerant variant of the test has that cost in expectation.
   The exponent `ln 2 − h(ρ₁ − σ_u + σ₂(ε₁))` is unchanged.
3. **SCI-MSG-0013, lemma header and reproduction line — "brute force on all 65 534 supports
   of `Q_4`".**  That check assumes the clipped level on each support: it tests the Harper
   step, not the lemma.  The lemma over general members is the referee's
   (`r8_03_isoperimetry.py`: a convex programme on every support of `Q_3`, `Q_4`, and all
   `2.8·10⁸` Lipschitz functions on a grid on `Q_4`).
4. **SCI-MSG-0013 §3 — "a displaced inner cone".**  Read "the cone raised by a constant
   under a plateau ring"; a displaced inner cone is a member only when raised by at
   least `u` times the displacement, and gains nothing.
5. **SCI-MSG-0012, reproduction line.**  `plateau_twin_check.py` as committed aborted at an
   assertion (a series truncated at 4000 terms, tested at `u = 8`) *before* the ten twins;
   the committed log ended in a traceback and the JSON file came from the previous run.
   Repaired; the script now runs to its end (13 s) and **the regenerated file is identical
   to the committed one in all 260 entries**; the referee had reproduced the ten twins
   independently.  The numbers were right, the trail was not (`DEAD_ENDS.md` SD39).
6. **SCI-MSG-0012 §2 (c) — "for every integer `r₂ > r₁` … exactly equal mean energies".**  Add
   the hypotheses: centres at distance `n/2 ± √(n ln n)`, `n` large (precisely: R8.1 above).
7. **SCI-MSG-0012 §3 — "below, the best we can say is the bracket of §2(c)".**  Between
   `ε₁ᶜ` and `a(u)` the lower end of that bracket is zero: there we have *no* lower bound.
   (Our digest said "close to `θ_hint(ε₁)`": equal to first order in `ε₁`, a factor of several
   below near `ε₁ᶜ`.)

## 3. The three statements that carry the repair

**R8.2 (quantile form of the packing bound) [P].**  For every algorithm that is
`ε`-accurate on the class with the exact datum, `ε` below the gap of the twin of radius
`r₂`, and every `m ≥ 0`:
`P_{g₀}(#evaluations > m) ≥ (1 − 2δ)(1 − 2/n²) − m·|B(n, r₂ − 1)|/2ⁿ`.
(The first `m` queries meet the ball about a uniform centre with probability at most
`m|B|/2ⁿ`.)

**R8.3 (the twin's gap, proved) [P].**  Let `g′ = min(g₀, T_{κ*})` be the exact twin of radius
`r₂`, `g″ = T_{κ*}` alone on the flat background, `U″` its mean energy.  Then `g″` is the plateau
on `B(a′, r₂ − 1)` at its own energy; `g′ ≤ g″` pointwise; and
`d ln Z^{pl}(R, U₀)/dU₀ = −1/(1 + c* + U₀) ∈ [−1, 0)`.  Hence

    G(r₂ − 1) − (U″ − U₀)₊  ≤  ln Z′ − ln Z₀  ≤  G(r₂),

with `U″ − U₀` exponentially small at extensive accuracy.  (Twelve exact cases: equality
with `G(r₂ − 1)` to `10⁻¹¹` at extensive gaps; above it by `3·10⁻⁴ … 2·10⁻²` at gaps of 4–8 nats.)

**R8.4 (a tolerant test) [P; constants not optimised; not simulated].**  Accept if all but
at most `k₀` of `⌈6(k₀ + ln(1/δ))·2ⁿ/|B(n,R)|⌉` uniform samples show one value: class-correct,
and at `g₀` the expected cost is of the order of the sample for a constant
`k₀ ≈ ln 2/(h(R/n) − h(ρ₁))`.

**Machine-checked** (`experiments/science/ws_R8/A16Core.lean`, Mathlib only, standard
axioms): the constraint as a convex inequality in the weights; `Σ t ≤ Σ f_η(t)`; the
monotonicity of `F_η` in the distance; the maximiser as the clipped level; and
`plateau_optimal` — for a fixed distance profile the plateau has the largest partition
function among *all* weight vectors with the pointwise bounds and the energy constraint
(no Lipschitz hypothesis).  Not formal: Harper's step, the existence of the level.

## 4. The conjecture, after an attempt to refute it

Five families at the exponential scale (soft basins and global tilts, terraces of any
depth, products of a flat and a cone block, exponentially many visible basins, "egg
cartons" around a code) and five explicit pairs with exact sums on non-flat landscapes:
**nothing beats the plateau twin on the flat background; each family's optimum
degenerates to it.**  On a global tilt one query far uphill finds the twin — a slope is
a direction from which a hidden state is visible.  In the small-slope limit a two-line
"column bound" **[H]** gives, whatever the visible landscape, `θ ≤ (u²/8)(√(1 − ε₁/a) − ½)²` for a
twin hidden in a fresh direction — the plateau value in that limit.  **Not excluded:**
landscapes with exponentially many prepared sites at several levels; twins that are
not single-level plateaus; and the interval `ε₁ᶜ ≤ ε₁ < a(u)`, where the conjecture says
"zero" and there is neither an algorithm for general instances nor a twin.

## 5. Requests (none is an authorisation)

To theory:
* **T-R8-1.**  Check Lemma A16.5 in the form "for all `g` with `|g(x)| ≤ u·dist(x, supp^c)`" and
  R8.1, R8.3; if they stand, they belong next to your Lemma 11.43(b).  For a full machine
  check two steps are missing: the rearrangement (`F` nondecreasing and
  `#{ρ ≥ k} ≤ #{ρ* ≥ k}` for all `k` imply `Σ F(ρ) ≤ Σ F(ρ*)`, with Harper's theorem as a
  hypothesis) and the monotonicity `dU/dc = −μ(P)(1 + c + U)`.
* **T-R8-2.**  With the exact datum, is there an algorithm that is `ε₁n`-accurate on the
  whole cube class with `e^{o(n)}` evaluations for some `ε₁ < a(u)`?  (We conjecture yes from
  `ε₁ᶜ` on; true at instances constant outside a small set; a twin argument cannot exclude
  it below `a(u) − ε₁`.)
* **T-R8-3.**  Exponential-scale vertex isoperimetry on a slice of the cube (the Johnson
  scheme): with it the column bound would be a theorem for radial visible landscapes.
  It is also the ingredient you named for the middle slice (your THY-RES-0007 §1.2).

To engineering (optional; a consistency test):
* **E-R8-1.**  Run the algorithm of §2 item 1 and its tolerant variant at `n = 24 … 32`,
  `u ∈ {2, 4}`, on the flat function, the basin `g₀`, `g₀` plus an exact plateau twin, two
  instances with two large level sets, and a cone; `10⁴` runs each; outputs: frequency of
  an error above `ε/2` and the histogram of the number of evaluations; validation: error
  frequency at most `δe^{|B(n,R)|/2ⁿ}`, and at `g₀` the fraction of runs that stop after the
  samples equals `(1 − |V|/2ⁿ)^M` within sampling error.  Minutes on one core.  Full
  specification: `R8_REPORT.md` §8.

## Assumptions and limitations

One referee; everything except the identities of A16.2 in double precision (differences
of mean energies always through the excess identity).  The referee's families for the
conjecture are exponential-scale formulas, validated by exact sums for one family
only; the column bound is a heuristic in a limit model.  No randomised algorithm was
simulated.  Prior art for the lemma: three searches at snippet level found nothing with
a second constraint ("short and not found", not "new").  The statements of the theory
report that A16 uses were read as statements, not re-proved.

## Requested response

None required.
