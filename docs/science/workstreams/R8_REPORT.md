# Workstream R8 — adversarial referee of addendum A16 (a mean-energy datum at extensive accuracy)

*Science division.  Reviewed: `docs/science/INFERENCE_LIMITS_ADDENDA.md`, addendum A16 (lines 721–998 at
head `39e0cd9`), the messages SCI-MSG-0012 and SCI-MSG-0013, digest items 25 and 27, status rows S34
and S36.  Theory statements are quoted from the theory report **at the commit of our tree, `5ed4072`**
(Theorem 11.25, Lemma 11.43, Theorems 11.44, 11.45, 11.54, 11.58 — read as statements; none
re-proved here).  All scripts, logs and notes: `experiments/science/ws_R8/` (`NOTES.md` has the order
in which things were done, including my own slips).*

Labels: **[V]** machine-checked here (Lean declaration named) · **[P]** paper proof, re-derived or
given here (it is said which) · **[N]** numerical evidence only · **[C]** conjecture · **[H]**
heuristic · **[K]** known, cited with the reading level.  "Re-derived" = I wrote the argument out
myself from the definitions; "replicated" = recomputed with my own code; "read" = read and found
plausible, not re-derived.

---

## How far I got

All six items of the brief were worked through.

1. **Verdicts** for A16.1, A16.2, A16.3 (a), (b), (c) and the counting, A16.5, A16.6 (i)–(iv): every
   step re-derived on paper before any numerics; six statements of my own (R8.1–R8.6 below) write
   out or repair what the text leaves open.
2. **Own numerics** (eleven scripts, none imports the coordinator's code; the coordinator's scripts
   were opened only after mine had run): entropy bracket incl. adversarial minimisation; twelve
   exact plateau twins of my own and the coordinator's ten reproduced; Lemma A16.5 by brute force
   over **general** members — a convex programme over all members on every support of `Q_3`, `Q_4`,
   and an exhaustive grid of 277 313 645 Lipschitz functions on `Q_4`.
3. **Conjecture A16.4**: not refuted.  Five families at the exponential scale, five explicit pairs
   with exact sums on non-flat landscapes, and a heuristic bound in the small-slope limit.
4. **Non-adaptive guess**: the pair exists and was constructed exactly; it gives the guess as a
   *lower* bound; the bracket of remark (4) was evaluated on six radial families.
5. **Prior art**: seven searches, two abstracts (a third fetch failed); brief, with reading levels.
6. **Overstatements**: fifteen sentences, with replacement texts.

Extra: a Lean file with the algebraic core of Lemma A16.5 (compiles, standard axioms only), and one
finding about the evidence trail (a committed script aborts before producing the cited evidence).

Not done: listed in the last section.

## Verdicts in one paragraph

**No numbered statement of A16 is false.**  A16.1 and A16.2 are proved as written (the lower end of
A16.1 is already Theorem 2(d) of `INFERENCE_LIMITS.md`, and it is the textbook entropy bound for a
Santha–Vazirani source).  A16.3 (a), (b), (c) and its counting are proved; the deep end, given in two
lines, is correct — written out, it needs only that the twin's cone overlaps the visible basin in a
weight fraction below `1/r₂`, with no dominance hypothesis (R8.1).  Lemma A16.5 is proved; it
survived every attack I could mount on general members, its algebraic core is machine-checked here,
and its text has five small imprecisions.  **Theorem A16.6 is where the text says more than it
proves:** (i) is proved; the algorithm of (ii) is class-correct in the addendum's form (the form
printed in SCI-MSG-0013 drops the gauge and is *not*), but its cost at `g₀` is bounded only with high
probability, the lower bound it is compared with is on the *expectation*, and with the fallback the
text allows ("any class-correct procedure") the expected cost exceeds the claimed one by factors
`e^{268}…e^{1596}` in my cases; (iii) rests on eight numerical coincidences, and the lemma as applied
to the twin gives `G(r₂)`, not `G(r₂ − 1)`.  Both gaps close: a quantile form of the lower bound
(R8.2) or a tolerant test (R8.4) repairs the first, and `G(r₂−1) − (U″−U₀)₊ ≤ gap(r₂) ≤ G(r₂)` (R8.3,
proved here) the second — so "`Θ(2ⁿ/|B(n,R(ε))|)`" is **proved after repairs**, with "two units of the
radius" in place of "one".  (iv) is proved at the exponential scale.  **Conjecture A16.4 is not
refuted**: every family I tried degenerates to the plateau twin on the flat background, slopes make
a twin visible from uphill (on a global tilt one query finds it), and in the small-slope limit a
two-line "column bound" shows that no twin hidden in a fresh direction beats the plateau, whatever
the visible landscape; between `ε₁ᶜ` and `a(u)` nothing is known in either direction.  **The
non-adaptive guess** is a valid lower bound (the pair exists; "displaced" is unnecessary), and the
datum-assisted bracket meets it on the radial families tried; the class-wide upper bound is open.
**Evidence trail:** `plateau_twin_check.py`, cited in SCI-MSG-0012 as the reproduction of the ten
twins, aborts with an `AssertionError` before reaching them (a series truncated at 4000 terms for
`u = 8`); the twins are in its JSON file, and I reproduced all ten independently.

## 1. Verdict table

| statement | verdict | re-derived | replicated with own code | findings |
|---|---|---|---|---|
| identity `ln Z = S − βU` | **proved** [K] | yes | used throughout | — |
| A16.1 entropy bracket; product-reference variant | **proved** [P]; lower end = Theorem 2(d) of `INFERENCE_LIMITS.md`; [K] in other words | yes | yes — 576 members, adversarial minimisation, 288 product-reference cases | §2.1 |
| A16.2 window; two relative entropies; series; table | **proved** [P, given theory 11.25(a),(b) at `5ed4072`] | yes | yes — 25–40 digits; table reproduced | §2.2 |
| A16.3 (a) exact root | **proved** [P]; deep end written out (R8.1) | yes | yes — 12 own twins; 10 of the coordinator reproduced | §2.3, F5 |
| A16.3 (b) gap bound, constant, `o(1)` | **proved** [P] | yes | yes — gap − bound ∈ [1.08, 3.05] nats | §2.3 |
| A16.3 (c) and the counting | **proved** [P] | yes | (c) checked on the masks | §2.3 |
| A16.3 exponent `θ_U ≥ ln 2 − h(ρ₀ − σ_u + σ₂)` for `ε₁ < ε₁ᶜ` | **proved** [P] | yes | table reproduced | — |
| A16.5 lemma | **proved** [P]; algebraic core **[V]**; five imprecisions | yes | yes — over general members, no assumption on the optimiser | §2.4, F6 |
| A16.5 remarks (1)–(4) | (1), (3) read; (2) [N]; (4) **proved after a repair** (sign of `f_η(t)`) | (4) yes | (4) used in script 06 | §2.4 |
| A16.6 (i) | **proved** [P] | yes | twins ≤ `G(R)` of the lemma in 12 cases | §2.5 |
| A16.6 (ii) algorithm | correctness **proved** (addendum's form; + fallback's failure probability; `R` must be chosen from `U` and one sample); cost: **gap** — w.h.p. only | yes | bracket valid on 300 general members in random gauge | F1, F3, F4 |
| A16.6 (iii) "`Θ`", "one unit of the radius" | **proved after repairs** R8.2 or R8.4, and R8.3; "at most two units" | — (mine) | yes — 12 cases | F1, F2 |
| A16.6 (iv) | **proved** at the exponential scale [P] | yes | yes — exact widths at `n = 1500, 2000` | §2.5 |
| table (d) | consistent with the above | yes | — | — |
| Conjecture A16.4 | **open; not refuted** [C] | — | five families, five exact pairs | §3 |
| non-adaptive guess | lower bound **proved** (sketch + exact pairs); equality **open** | yes | yes | §4 |

**Findings, in order of weight.**

* **F1** (A16.6 (ii)–(iii)) — the upper bound holds with high probability, the lower bound is on the
  expectation; with the fallback the text allows, the expected cost is astronomically larger.
  Repaired by R8.2 or R8.4.  §2.5.
* **F2** (A16.6 (iii)) — "gap `= G(r₂−1)`" was numerics, and the lemma applied to the twin gives
  `G(r₂)`.  Closed by R8.3.  §2.5.
* **F4** (SCI-MSG-0013) — the algorithm as printed in the message (no gauge) is not correct on the
  class.  §2.5.
* **F7** (evidence) — `plateau_twin_check.py` aborts before the ten twins; the committed log ends in
  a traceback.  §5.
* **F3** (A16.6 (ii)) — "uses no hint": `R` has to be chosen; R8.5.  §2.5.
* **F5** (A16.3) — "for all large `n`" quantified (R8.1); the second numerical example omits its `ρ₁`.  §2.3.
* **F6** (A16.5) — five imprecisions: a hypothesis that is not needed (`R < n/2`); a sentence about
  the maximiser that is true only for the chosen `η`; existence and uniqueness of the level not
  argued; "brute force" in the header is a test of the Harper step only; remark (4) needs
  `f_η(t) ≥ 0` or the exact size of `D`.  §2.4.
* **F8** (A16.1) — the lower end is Theorem 2(d) of the same thread and the entropy bound of a
  Santha–Vazirani source.  §2.1, §6.
* **F9** (non-adaptive guess) — the inner cone need not be displaced, and a displaced one must be
  raised by at least `u` times the displacement.  §4.

---

## 2. Statement by statement

Units `β = 1`, `c = u`.  `σ = σ_u = 1/(1+e^u)`, `a = a(u) = ln 2 − h(σ)`, `ρ₀ = ln(2/(1+e^{−u}))/u`,
`σ₂(ε₁) = h⁻¹(h(σ) + ε₁)`, `θ_pl(ε₁) := ln 2 − h(min{½, ρ₀ − σ + σ₂(ε₁)})`.  Two identities used
repeatedly, both re-derived: `h(σ) = uσ + ln(1+e^{−u})` and hence **`a(u) = u(ρ₀ − σ_u)`** [P; 30 digits
in `r8_01`].

### 2.1 Proposition A16.1 — proved

*Re-derived.*  Chain rule `S = Σ_i E h(p_i)`; the two partial sums defining the odds of `x_i` differ
term by term by a factor in `[e^{−u}, e^{u}]`, so `p_i ∈ [σ, 1−σ]`; `h` is concave and symmetric.
Upper end: trivial.  Attainment: the cone is the product `Bern(σ)ⁿ`.  Product reference: with
`π = Bern(p)ⁿ`, `ln(Z_g/Z_0) = −U − KL(μ_g‖π)` and `KL(μ_g‖π) = Σ_i E KL(Bern(κ_i)‖Bern(p))`,
`κ_i ∈ [a₀, a₁]`, `KL(·‖p)` convex — the statement follows.  **[P]**

*Numerics [N]* (`r8_01_bracket.py`): 576 members of eight families (`n ≤ 12`, `u ∈ {0.25, 1, 2, 4}`):
least `S − n·h(σ)` is `−7·10⁻¹⁵` (cones, round-off), least `n ln 2 − S` is `9·10⁻⁷`; every conditional
probability, for random orders, in `[σ, 1−σ]` to `10⁻¹⁶`.  **Adversarial:** minimising the entropy
over the class polytope by SLSQP (25–60 starts, `n = 3, 4, 5`, four `u`) returns `n·h(σ)` to
`10⁻¹⁴`; a greedy extreme-point descent (`n = 6, 8, 10`) reaches it in five of six cases and never goes
below.  Product reference: 288 cases, both
ends hold, equality at the two cones (`n·KL(a₀‖p)` and `n·KL(a₁‖p)` to ten digits).  Mutation: a
`1.5u`-cone violates the lower end (4.75 against 5.82).

*Remarks.*  (1) The lower end is not new in this thread: it is **Theorem 2(d) of
`INFERENCE_LIMITS.md`** ("every member of the class has `S(μ_g) ≥ n·h(σ(b))`"), proved there with
conditioning on all other coordinates.  What A16.1 adds is the reading with the datum.  (2) Prior
art: in the weights the class is the set of measures whose conditional odds of every bit given all
others lie in `[e^{−u}, e^u]` — a **strong Santha–Vazirani source** of the randomness-extraction
literature, for which the per-bit entropy bound is the chain rule (§6).  **[K]**

### 2.2 Corollary A16.2 — proved, given theory report Theorem 11.25 (`5ed4072`)

*Re-derived.*  `σ(1−σ) = 1/(4cosh²(u/2))`, hence `KL(½‖σ) = −½ ln(4σ(1−σ)) = ln cosh(u/2)`; with
`t = tanh(u/2) = 1 − 2σ`: `KL(½‖σ) = −½ ln(1−t²) = Σ t^{2k}/(2k)` and
`KL(σ‖½) = ½[(1+t)ln(1+t) + (1−t)ln(1−t)] = Σ t^{2k}/(2k(2k−1))`; the difference has coefficients
`(k−1)/(k(2k−1))`.  `u/2 − uρ₀ = ln cosh(u/2)`.  **[P]**  All identities to 25–40 digits and the four
rows of the table (`3·10⁻⁶`, `1.7·10⁻⁴`, `0.0056`, `0.0667`) reproduced [N].

*The two conventions (the brief's question).*  Consistent.  Theorem 11.25 is stated for
`(ε/2, δ)`-correct algorithms; its (a) needs `ε < Δ_k` (gap larger than the *width* `ε`), and its (b)
gives a bracket of width `n ln cosh(u/2) + 2βη`, i.e. the free accuracy without the datum is the
width `n ln cosh(u/2)`.  A16.1 gives a bracket of width `n·a(u)`.  Both "free accuracies" of the
table are therefore widths, and "within `n·a(u)/2`" is the half-width.  The sentence "an accuracy of
`±0.3n` nats is free with the datum" (`u = 4`) is the half-width of `a(4) = 0.603`.  **[P]**

One precision: "the dip of radius `r` raises `ln Z` by more than `ε₁n` as soon as `r/n > ρ₀ + ε₁/u`" is
true up to `O(1/n)` in the radius (exactly: `2^{−n}Σ_j C(n,j)e^{u(r−j)} = e^{u(r−ρ₀n)}·P(Bin(n,σ) < r)`).

### 2.3 Proposition A16.3 — proved; the deep end written out

**(1) Excess identity.**  Re-derived for arbitrary `g₀`, `g′ = min(g₀, T)`: `Z′ = Z₀ + E`,
`U′Z′ = U₀Z₀ + D`, so `U′ − U₀ = (E/(Z₀+E))(D/E − U₀)`; per point of the excess, with
`t = g₀ − g′ > 0`, the ratio of the two summands is `g′ − t/(e^t − 1)`, and `0 < t/(e^t−1) < 1`.
**[P]**; against a full enumeration of the cube at `n = 16` (four cases, overlapping supports) the
joint-law sums and the identity agree to `10⁻¹⁰` [N].

**(2) Shallow end.**  `m(κ) > −uκ − 1`, strictly, with no hypothesis; hence `U′ > U₀` at
`κ_lo = (|U₀| − 1)/u` provided `κ_lo > 0`.  **[P]**  (If `|U₀| < 1` no twin dug in a flat background can keep
the datum: a point of the excess at depth `t` has effective energy `−te^t/(e^t−1) ≤ −1 < U₀`.  This is
the only place where dominance of the visible basin enters, and it is why the flat instance has no
twin.)

**(3) Deep end — the inequality the brief asks for.**  Let `k = r₂ − r₁ ≥ 1`, `T` the full cone of
radius `r₂` about `a′`, and

    W = Σ_{d<r₁} C(n,d)e^{u(r₁−d)},   V = |B(n,r₁−1)|,   Z₀ = 2ⁿ + W − V,   A′ = −Σ g₀e^{−g₀} = |U₀|Z₀,
    X = Σ_{d=r₁}^{r₂−1} C(n,d)e^{−u(d−r₁)},        Y = Σ_{d=r₁}^{r₂−1} C(n,d)·u(r₂−d)·e^{−u(d−r₁)}  ≥ uX,
    W₂ = Σ_{T<0} e^{−T} = e^{uk}(W + X),           ω = Σ_{g₀<0, T<0} e^{−T}   (weight of the cone inside the basin).

"Free" sums (as if `g₀ = 0` on the support of `T`): `E^f = e^{uk}(W+X) − |B(n,r₂−1)|`,
`D^f = −e^{uk}(A′ + ukW + Y)` (every weight of the basin multiplied by `e^{uk}`, every depth increased
by `uk`, plus the shells `r₁ ≤ d < r₂`).

> **R8.1 [P; each line checked with exact sums in eight cases, `r8_07_deepend.py`].**
> (i) `E^f − ω ≤ E ≤ E^f`;  (ii) `D^f ≤ D ≤ D^f + u r₂ ω` (on the overlap each true summand lies
> between the free one and `0`, because `x ↦ xe^x` increases);  (iii) `W + X ≤ Z₀`, **for every `n`,
> with no hypothesis** (`X ≤ Σ_{d≥r₁} C(n,d) = 2ⁿ − V`);  (iv) hence
> `D^f + (A′/Z₀)E^f = e^{uk}A′[(W+X)/Z₀ − 1] − e^{uk}(ukW + Y) − (A′/Z₀)|B(n,r₂−1)| ≤ −e^{uk}(ukW + Y)`;
> (v) `D + (A′/Z₀)E ≤ −e^{uk}(ukW + Y) + u r₂ ω`.
> Therefore **`m(r₂) < U₀` as soon as `r₂·ω < e^{uk}(kW + Y/u)`, in particular as soon as
> `ω/W₂ < 1/r₂`** (use `Y ≥ uX`, `k ≥ 1`).

So (a) holds **for every `n` with `|U₀| > 1` and `ω/W₂ < 1/r₂`**; no dominance is needed at the deep
end.  With the overlap bound of R6.3 adapted to radius `r₂` (re-derived: for `x` uniform on a sphere
of radius `j ≤ r₂` about `a′`, `d(x,a₀) = D + j − 2i`, `i` hypergeometric; the event `d(x,a₀) < r₁`
needs `i` to exceed its mean by at least `(n/2 − r₁ − 2Δ)/2`; Hoeffding) the condition reads
`exp(−(n/2 − r₁ − 2Δ)²/(2r₂)) < 1/r₂`, `Δ = √(n ln n)`.  **For which `n`:** with `ρ₁ = ρ₀ + 0.01` this
sufficient condition holds from `n = 6100` (`u = 1`, `r₂ ≤ 0.45n`), `1400` (`u = 2`), `450` (`u = 4`),
`33 350` (`u = 0.5`) [N, `r8_07`].  The exact sums are far kinder: `ln(ω/W₂) = −10.9` against
`ln(1/r₂) = −5.1` already at `n = 400`, `u = 1`; roots exist at `n = 60`; and with centres as close as
`0.08n` — where `ω/W₂ ≈ 1` and R8.1 says nothing — the root is still there with the same gap
(`r8_02`, part 3).  The hypothesis `|d(a₀,a′) − n/2| ≤ √(n ln n)` is sufficient and far from necessary.

**(a)** `κ ↦ U′(κ)` is continuous, `U′ > U₀` at `κ_lo`, `U′ < U₀` at `κ = r₂`: root in `(κ_lo, r₂)`.  **[P]**

**(b)** `E` is non-decreasing in `κ` (`T_κ` decreases pointwise).  At `κ_lo` every point of
`B(a′, ⌊r₂ − κ_lo⌋) ∖ V` contributes `e^{|U₀|−1} − 1`, and `Z₀ = e^{S₀+|U₀|}` exactly, so

    gap ≥ ln(E(κ_lo)/Z₀) ≥ ln|B(n, ⌊r₂ − κ_lo⌋)| − S₀ − 1 + ln(1 − e^{1−|U₀|}) + ln(|B∖V|/|B|).

The constant is `1`; the "`o(1)`" is the last two terms, both exponentially small.  **[P]**  In my
twelve cases gap − bound ∈ [+1.08, +3.05] nats; in the coordinator's ten, [+0.90, +3.43].

**(c)** `T_κ = 0` iff `d(x,a′) ≥ r₂`, and `min(g₀, 0) = g₀`.  **[P]**  **Counting**: for a uniform `a′`
the centre is good with probability `≥ 1 − 2/n²` (Hoeffding), and the usual coupling gives
`P(Q ∩ B(a′, r₂−1) ≠ ∅) ≥ 1 − 2δ` for each good `a′` (the datum is the same number for `g₀` and the
twin, so the two runs coincide until the ball is entered).  **[P]**

**Exponent.**  `S₀ − n·h(σ)` and `|U₀| − u(r₁ − σn)` are exponentially small once `u(ρ₁−ρ₀)n ≫ 1`
(`1.1·10⁻⁵` at `n = 800`, `u = 1`, `ρ₁ = ρ₀ + 0.02`; but `0.096` at `n = 1200`, `u = 0.5`,
`ρ₁ = ρ₀ + 0.01`, where `W/2ⁿ = e^{6}` only).  Then gap `≥ n[h(ρ₂ − ρ₁ + σ) − h(σ)] − O(ln n)`, and
`ρ₁ ↓ ρ₀` gives `θ_U(ε₁) ≥ θ_pl(ε₁)` for `ε₁ < ε₁ᶜ`.  **[P]**  The seven rows of the table and the
three values of `ε₁ᶜ` are reproduced to the last digit (`r8_04`, part 1); `θ_pl ≥ h − ε₁` always
(`h(σ+δ) − h(σ) ≥ h(ρ₀+δ) − h(ρ₀)` because `h′` decreases and `σ < ρ₀`), so "supersedes" is right.

**Independent replication [N].**  Own twins (`r8_02`): twelve cases, `n = 400…2400`,
`u ∈ {0.5, 1, 2, 3, 4}`, centres at `0.42n … 0.58n`: root unique on a 121-point grid, `κ* > κ_lo`,
(b), (c) hold, radii within 2–9 sites of the formulas.  The coordinator's ten cases
(`plateau_twin_check.json`) recomputed with my code (`r8_10`): `r₁`, `r₂` identical, `κ*` and the gap
to `10⁻⁴` in all ten.

**A defect of presentation.**  The second example of A16 (b) — "`n = 600`, `u = 4`, gap `0.30n`:
`r₂ = 190` against `147`" — does not say that it uses `ρ₁ = ρ₀ + 0.03`; with the `ρ₁ = ρ₀ + 0.01` of the
example before it one gets `r₂ = 178` (`r8_09`).  Both numbers are right for their own `ρ₁`.

### 2.4 Lemma A16.5 — proved; algebraic core machine-checked; five imprecisions

Every step re-derived; the brief's six questions in order.

**(i) Convexity and the direction of the inequality.**  `U_g = −Σ t ln t/Σ t`, so `U_g ≥ U₀` iff
`φ(t) = Σ t ln t + U₀Σ t ≤ 0` (**[V]** `R8.constraint_iff`); `t ln t` is convex and the rest linear, so
the constraint set is convex; "vanishes outside `D`" is affine and the class is a convex cone in `t`.
For `η ≥ 0` and `φ(t) ≤ 0`: `Σ t ≤ Σ t − ηφ(t) = Σ f_η(t(x))` — the direction is right whether the
constraint is active or slack (**[V]** `R8.sum_le_sum_f`).

**(ii) The Lipschitz cone.**  It is used once, to get `e^{−uρ(x)} ≤ t(x) ≤ e^{uρ(x)}`, and nowhere
else.  **It may be dropped:** the lemma holds verbatim for the larger set
`{g : |g(x)| ≤ u·dist(x, supp^c)}`, and the maximiser happens to be Lipschitz (**[V]**
`R8.plateau_optimal`: for a fixed distance profile `ρ`, the plateau maximises `Σ t` among *all*
weight vectors with these pointwise bounds and the energy constraint; no Lipschitz hypothesis on `t`).

**(iii) Harper's theorem in the form used.**  Needed: if `|D| ≤ N`, then for every `k`
`#{x : dist(x, D^c) ≥ k} ≤ #{x : dist(x, D*^c) ≥ k}`, `D*` the last `N` points of the simplicial order.
From Harper's theorem (initial segments minimise the closed neighbourhood, and the neighbourhood of
an initial segment is one) by induction on the radius, exactly as in the proof of theory report
Lemma 11.43(b) **[K — Harper's theorem through the theory report at `5ed4072`; original not
opened]**.  "The complement of an initial segment" **is** the right extremal set for sizes that are
not ball sizes, and **it is isomorphic to an initial segment**: `x ↦ x̄` maps level `k` to level
`n − k` and reverses the lexicographic order inside a level (`min(A Δ B) ∈ A` iff
`min(Ā Δ B̄) ∈ B̄`) **[P]**.  So the coordinator's script ("plateau on the initial segment") and the
addendum ("complement of an initial segment") state the same thing.  Checked on all 65 534 proper
subsets of `Q_4`, all 254 of `Q_3`, 40 000 random subsets (uniform, ball-like, grown) of `Q_5`, `Q_6`,
for all `k` at once: no violation; final and initial segments have equal erosion numbers for every
size **[N]**.  The hypothesis "`R < n/2`" of the lemma is not used.

**(iv) The choice of `η`.**  `U_{g_pl} ≥ min g_pl = −c*`, so `c* ≥ |U₀|` and `η = 1/(c* + U₀ + 1) ∈ (0, 1]`.
Then `ln t*_η = 1/η − 1 − U₀ = c* ≥ 0`, the maximiser of `f_η` on `[e^{−uρ}, e^{uρ}]` is
`min(e^{c*}, e^{uρ})` (**[V]** `R8.F_eq_plateau`, from `f_le_max` and `f_mono_below`), and
`Σ F_η = Σ f_η(t_pl) = Z_pl − ηφ(t_pl) = Z_pl`.  ∎ as claimed.

**(v) The case `U₀ > −1`, and the level.**  Two imprecisions, neither affecting the lemma.
(1) "For the ball the maximiser inside `F_η` is `min(t*_η, e^{uρ})`" is false for general `η` when
`U₀ > −1`: for `η > 1/(1+U₀)` one has `t*_η < 1` and the maximiser is `max(t*_η, e^{−uρ})` — a hill.
It is true for the `η` that is chosen.  (2) "`c*` the level with `U_{g_pl} = U₀`" presupposes existence
and uniqueness.  They hold: with `P(c)` the top of the plateau and `μ` its Gibbs measure,

    dU/dc = −μ(P)(1 + c + U) < 0,        d ln Z/dc = μ(P),        hence   d ln Z^{pl}/dU₀ = −1/(1 + c* + U₀) ∈ [−1, 0)

(`U ≥ −c`), so `U` decreases strictly from `0` to the cone's energy **[P; finite differences in
`r8_08`]**.  For `U₀ = 0` the plateau is the zero function and the lemma says `Z ≤ 2ⁿ` whenever
`U_g ≥ 0` (`η = 1`: `t − t ln t ≤ 1`); true on all 95.6 million grid members with `U_g > 0` **[N]**.

**(vi) Total mean energy on a flat background.**  Yes, this is what A16.6 (i) needs: an alternative
that agrees with `g₀` outside `D` vanishes outside `D ∪ V`, and its *total* mean energy is the datum.

**Brute force over general members [N]** (`r8_03_isoperimetry.py`, 284 s).  The coordinator's check
takes the best modification on a support to be the clipped level and so tests the Harper step
only.  Mine assumes nothing about the optimiser:

* **B — a convex programme in the weights**, `max Σ t` s.t. `t = 1` off `D`, `t(x) ≤ e^u t(y)` on edges,
  `φ(t) ≤ 0`: outer LP relaxations by gradient cuts (HiGHS, feasibility tolerances `10⁻¹⁰`) give
  rigorous upper bounds, a feasible member gives a lower bound.  Every support of `Q_3` (20 orbits)
  and of `Q_4` (400 orbits under the 384 symmetries = all 65 534), `u ∈ {1, 2}`, four energy bounds
  each; 500 random supports in `Q_5`, 150 in `Q_6`.  **No feasible member above `Z^{pl}`** (largest
  relative excess `+6·10⁻¹⁶`); the LP bounds certify the lemma to `1.2·10⁻⁷`; on `D*` itself the
  optimum over all members equals the plateau value to `10⁻⁹…2·10⁻⁸`.
* **C — exhaustive grids.**  Every `u`-Lipschitz function vanishing at one vertex with values in
  `(u/6)ℤ` on `Q_3` (11 491 441 functions) and in `(u/2)ℤ` on `Q_4` (277 313 645), dips and hills
  alike, `u ∈ {0.6, 1, 2.5}` resp. `{1, 2.5}`: `Z_g ≤ Z^{pl}(#{g ≠ 0}, U_g)` when `U_g ≤ 0`, `Z_g ≤ 2ⁿ`
  when `U_g > 0`.  **No violation**; 906 resp. 67 792 members attain the bound.
* **D** — 900 random general members with hills on random supports, `n = 5…10`: no violation.
* **E** — three mutations fire (bound from a subcube; constraint dropped; bound at a wrong energy).
  (My first mutation did not fire — at `U₀ = ½U_cone` the plateaus on a subcube and on `D*` coincide
  because the level is below `u`; recorded in `NOTES.md`.)

**Machine check [V]** (`experiments/science/ws_R8/A16Core.lean`; `lake env lean`, exit 0, no
warning; axioms `propext`, `Classical.choice`, `Quot.sound`): `constraint_iff`, `sum_le_sum_f`,
`f_le_max`, `f_at_max`, `f_mono_below`, `f_anti_above`, `F_mono` (monotonicity of `F_η` in the
distance), `F_eq_plateau`, `sum_le_sum_F`, `plateau_optimal`.  **Not** formalised: the Harper step
(comparison between supports), existence and uniqueness of the level, membership of the plateau in
the class.

**Remarks of the lemma.**  (1) Read; plausible (the clipped level between the two McShane envelopes
is the pointwise maximiser of the Lagrangian and is Lipschitz); the existence of the multiplier for
a general reference was not checked.  (2) "Hills never help": consistent with all of B, C, D **[N]**.
(3) Correct.  (4) Re-derived: `Z = Σ f_η(w)` for every `η` because `φ(w) = 0` at the member's own
datum, and `t < w(x) ≤ te^{u·dist(x,D^c)}` on `D`.  **One repair:** writing
`Σ_{x∈D} H(ρ(x)) = H(0)|D| + Σ_{k≥1}(H(k) − H(k−1))·#{ρ ≥ k}` with `H(0) = f_η(t)`, Harper controls the
second term; "at most its value for a ball of the size of `D`" is right when `|D|` is known exactly,
but a sampler knows only an upper bound on `|D|`, and enlarging the ball is harmless only if
`f_η(t) ≥ 0`, i.e. `η(U + ln t) ≤ 1` — a restriction on `η` that the text omits (otherwise subtract
`f_η(t)(|B| − |D|)`) **[P]**.

### 2.5 Theorem A16.6 — (i) proved; (ii), (iii) proved after repairs; (iv) proved at the exponential scale

**(i)** Re-derived; nothing to add.  The left side is A16.1 with `S₀ − n·h(σ)` exponentially small;
the right side is the lemma applied to `D ∪ V`.  **[P]**

**(ii) Correctness [P].**  If the instance is constant `= v` outside at most `N = |B(n,R)|` points,
`g − v` vanishes there, has datum `U − v` and log-partition function `ln Z + v`; the lower end is
"`2ⁿ − N` points of weight one" and A16.1, the upper end the lemma with `U₀ = min(U − v, 0)` (for
`U − v > 0` it is `n ln 2`, by (v) above).  If it is not, every level set has probability
`< 1 − N/2ⁿ` and `P(all M samples equal) = Σ_v p_v^M ≤ (max_v p_v)^{M−1} ≤ δ·e^{N/2ⁿ}` — two large level
sets give `2·2^{−M}`.  A narrow bracket on an instance that is *not* flat outside a small set can give
a wrong output, but that event is inside the one just bounded.  So the failure probability is at
most `δe^{N/2ⁿ} + δ_fallback`: "`δ(1+o(1))`" needs `N/2ⁿ → 0` and an exact fallback (or a split of `δ`),
which the text does not say.  Bracket verified on 300 random general members (dips and hills, random
gauge `v`, `n = 10, 12`): always contains `ln Z + v`, equality cases included **[N]**.

**Finding F3 (minor) — "uses no hint".**  `R` is a parameter, and the claim at `g₀` needs
`G(R) + o(1) ≤ ε`, so `R` depends on `U₀` and `ε`.  A class-correct algorithm tuned to one instance is
legitimate for a statement about the cost *at* that instance, but it is a hint in disguise.
*Repair (R8.5) [P]:* draw one point, read `v₁`; let `R` be the largest radius for which the bracket
computed from `U − v₁` has width `≤ ε`; then draw `M(R)` points and proceed.  Same correctness
argument; cost `M(R) + 1` on the good event.

**Finding F4 — the form printed in SCI-MSG-0013 is not class-correct.**  The message gives the
bracket as `[n·h(σ_u) − U, ln Z^{pl}(R, U)]`, without the gauge.  At the constant instance `g ≡ v < 0`
all samples show one value, `U = v`, the truth is `n ln 2 − v`, and the upper end is
`S(μ_pl) − v < n ln 2 − v`: the truth is outside the bracket with probability one.  The addendum's
form (bracket for `ln Z + v` from `U − v`) is correct.  **[P]**

**Finding F1 (major) — the cost is bounded with high probability; the lower bound is on the
expectation.**  At `g₀` the samples meet `V` with probability at most `ln(1/δ)|B(n,r₁−1)|/|B(n,R)|`
(`3·10⁻⁴ … 10⁻⁶¹` in my extensive cases; `0.18`, `0.15` in two cases with gaps of 7–8 nats); otherwise
the algorithm stops after `M` samples.  But

    E[cost at g₀]  =  M + P(samples meet V)·C_fallback ,

and with exhaustive evaluation as the fallback this is `≈ M·(1 + |V|)`: `ln(E[cost]/M) = 268 … 1596` in
ten cases (`r8_04`, part 3).  The text compares this algorithm with the bound
`E[#evaluations] ≥ (1−2δ)(1−2/n²)2ⁿ/|B(n,r₂−1)|` and concludes "the number of evaluations needed at
`g₀` is `Θ(…)`".  Neither bound is wrong; the comparison is between two different functionals.  With
a fallback of cost `C` the condition is `C ≲ 2ⁿ/|V|`; for the nested algorithm of theory report
Theorem 11.54 (exponent `θ_hint(ε₁)`; a paper proof of the theory division, exponential scale only)
that holds iff `ρ₁ ≤ ρ₀ + ε₁/u` (true in nine of my ten cases, false in one).  Two repairs, either
suffices:

> **R8.2 (quantile form of the lower bound) [P].**  For every algorithm that is `ε`-accurate on the
> class with the exact datum, `ε <` gap of the twin of radius `r₂`, and every `m ≥ 0`:
> `P_{g₀}(#evaluations > m) ≥ (1 − 2δ)(1 − 2/n²) − m·|B(n, r₂−1)|/2ⁿ`.
> *Proof.*  For a good centre `P(Q ∩ B(a′) ≠ ∅) ≤ P(|Q| > m) + P(Q_{≤m} ∩ B(a′) ≠ ∅)`, and for a
> uniform `a′` the last term averages to at most `m|B|/2ⁿ`.  ∎
> With `m = ½(1−2δ)2ⁿ/|B(n,r₂−1)|`: more than `m` evaluations with probability `≥ ½(1−2δ) − o(1)`,
> against "at most `M` with probability `1 − e^{−Ω(n)}`" for the algorithm of (ii).

> **R8.4 (a tolerant test: the upper bound in expectation) [P; constants not optimised, not
> simulated].**  Draw `M′ = ⌈6(k₀ + ln(1/δ))·2ⁿ/|B(n,R)|⌉` uniform points; accept if all but at most
> `k₀` show one value `v`, and then use the bracket of (ii); otherwise evaluate everything.
> Correct on the class: if every level set misses more than `N` points, pair the samples — at
> least `M′/2 − k₀` pairs must agree, each agrees with probability `≤ 1 − N/2ⁿ`, and a Chernoff bound
> with mean `≥ 3(k₀ + ln(1/δ))` gives probability `≤ δ`.  At `g₀` more than `k₀` samples fall in `V`
> with probability `≤ (M′|V|/2ⁿ)^{k₀+1}`, so `E[cost] ≤ M′ + 1` as soon as
> `(k₀+1)·ln(2ⁿ/(M′|V|)) ≥ n ln 2`, i.e. `k₀ ≈ ln 2/(h(R/n) − h(ρ₁))` — a constant (`5 … 234` at the
> sizes of `r8_07`; it blows up as `R/n ↓ ρ₁`, i.e. at bounded accuracy, where (ii) does not apply).

**Finding F2 — "(iii) It matches" was eight numerical coincidences, and the lemma gives `G(r₂)`.**
The twin of radius `r₂` differs from `g₀` on `D = B(a′, r₂−1)` and `|D| + |V| > |B(n, r₂−1)|`, so
(i) bounds its gap by `G(r₂)`, not by `G(r₂−1)`.  Numerically gap `= G(r₂−1)` to `10⁻¹¹` at extensive
gaps — and **gap `> G(r₂−1)` in seven of my ten cases** (`r8_04`, part 2).  What the "`Θ`" needs is the
other direction, gap `≳ G(r₂ − O(1))`, and that is nowhere proved in A16.  It is true:

> **R8.3 [P, mine; checked in twelve cases, `r8_08_matching.py`].**  Let `g′ = min(g₀, T_{κ*})` be the
> exact twin of radius `r₂` and `g″ = T_{κ*}` alone on the flat background, with mean energy `U″`.
> (1) `g″` is the plateau on `B(a′, r₂−1)` at its own energy: `Z″ = Z^{pl}(r₂−1, U″)`.
> (2) `g′ ≤ g″` pointwise, hence `Z′ ≥ Z″` — with no hypothesis on the overlap.
> (3) `ln Z^{pl}(R, U₀) ≤ ln Z^{pl}(R, U″) + (U″ − U₀)₊` (the derivative in (v) of §2.4).
> Hence **`G(r₂−1) − (U″ − U₀)₊ ≤ gap(r₂) ≤ G(r₂)`** (right end: Lemma A16.5).  Moreover, with
> `E^f = Z″ − 2ⁿ` and `ω* = Σ_{x∈V}(e^{−T_{κ*}(x)} − 1)₊` (the part of the twin's own excess that lies in
> the visible basin), `E^f − ω* ≤ E ≤ E^f` and `D^f ≤ D ≤ 0` give
> `(U″−U₀)₊ ≤ (u r₂ + 1)·(2ⁿ + ω*)/(E^f − ω*)`: here `2ⁿ/E^f ≤ e^{−gap}(1+o(1))`, and `ω*/E^f` is the
> weight fraction of the twin inside `V`, exponentially small for far centres (the Hoeffding bound
> of R8.1) — so the correction is exponentially small at extensive accuracy.

Numerically `|U″ − U₀| ≤ 5·10⁻⁵` (round-off level at the large gaps), and gap `− G(r₂−1) = e^{−gap}(1 − |U₀|2ⁿ/W)` to three digits
wherever it is above round-off (`3.264·10⁻⁴` against `3.263·10⁻⁴`; `2.209·10⁻²` against `2.184·10⁻²`)
**[N; the formula is H: with a negligible overlap `Z′ − Z″ ≈ W − V` and `U″ − U₀ ≈ |U₀|2ⁿ/E`]**.  **Bookkeeping, now proved:** if `G(R) + o(1) ≤ ε < G(R+1) − (U″−U₀)₊`, the
algorithm works with `|B(n,R)|` and the twin with `r₂ − 1 = R + 1` has gap `> ε`: lower and upper bound
differ by `ln(1/δ)/(1−2δ)` and **one** unit of the radius; for `ε` inside the exponentially narrow
windows below the values of `G`, by **two**.  (In `r8_04`, where I put `ε` `10⁻⁶` above a value of `G`,
both occur; `ln(M/LB) = 1.5 … 2.1` at `δ = 0.05`.)  At bounded gaps "gap `= G(r₂−1)`" fails (`1.287`
against `0.964` at `r₂ = r₁+1`) and the algorithm does not apply: (iii) is a statement about extensive
accuracy, as the addendum says.

**So, with R8.2 (or R8.4), R8.3 and R8.5: at `g₀`, with the datum, the number of evaluations is
`Θ(2ⁿ/|B(n, R(ε))|)` — in the quantile sense, or in expectation for the tolerant test — and the
exponent is `ln 2 − h(ρ₁ − σ_u + σ₂(ε₁))`.**  The comparison with the cost without the datum (at
least `ln 2 − h(ρ₁ + ε₁/u)` at the same instance, by the cone dip of radius `(ρ₁ + ε₁/u)n`) is right:
re-derived.  **[P]**

**(iv)** Re-derived at the exponential scale.  Upper end: `n·max(ln 2, ue + h(R/n − e))` (when
`ue + h(R/n − e) < ln 2` the energy constraint forces an excess of order `2ⁿ` and no more, so
`ln Z^{pl} = n ln 2 + O(1)`); lower end `n·max(ln 2, h(σ) + ue)`.  Width
`n·min(h(R/n−e) − h(σ), ue + h(R/n−e) − ln 2)₊`; the first term decreases in `e`, the second
increases (`u > h′(R/n − e)` iff `R/n − e > σ`), and they cross at `ue = a(u)`, i.e. `e = ρ₀ − σ_u`.
**[P]**  Exact widths at `n = 1500, 2000` (`u = 1, 2, 4`) are within `1.6·10⁻³` per site of the
formula and peak within one grid step of `ρ₀ − σ_u` **[N]**.  "Hardest" is justified at this scale:
every such instance costs at most what the algorithm costs, and the basins `ρ₁ ↓ ρ₀` cost at least
that by A16.3.  For data `e < ρ₀ − σ_u` (a basin coexisting with the background, which needs `r₁`
within `O(1)` of `ρ₀n`) no lower bound is given, and none is needed.

### 2.6 The table of part (d)

Consistent with the above.  It rests, besides A16, on theory report Theorems 11.54 and 11.58 for
`θ_U ≤ θ_hint` and for the bounded-accuracy row, and on the referee's R6 — all **[K]**, read as
statements at `5ed4072`, not re-proved here.

---

## 3. Conjecture A16.4 — attempts to refute it

**What a refutation needs.**  `θ_pl(ε₁) ≤ θ_U(ε₁) ≤ θ_hint(ε₁)` (A16.3; theory report 11.54), and the
two ends differ in second order in `ε₁`.  A refutation is an instance `g` and a family of members
`g′_j` with the same datum, `|ln Z_{g′_j} − ln Z_g| > ε₁n`, `g′_j = g` outside `D_j`, and
`max_x P_j(x ∈ D_j) = e^{−nθ}` with `θ > θ_pl(ε₁)`.  Three elementary facts narrow the search **[P]**:

* *Only "more entropy at the same energy" matters.*  An alternative with `Z` smaller by `e^{−ε₁n}`
  must differ from `g` on a set carrying all but `e^{−ε₁n}` of the Gibbs mass of `g` — one place, which
  a hinted algorithm queries first.  An alternative with larger `Z` has, by the identity, entropy
  `S(μ_g) + ε₁n ≥ n(h(σ_u) + ε₁)`.
* *A counting limit.*  The twin's excess sits at the energy of the datum on at least `e^{S(μ_g)+ε₁n}`
  points, so no twin argument can give more than `ln 2 − S(μ_g)/n − ε₁ ≤ a(u) − ε₁`.  This is far above
  `θ_pl` (`u = 1`, `ε₁ → 0`: `0.111` against `0.029`), so counting alone decides nothing: the question
  is how thick the *wall* around the plateau must be.
* *The flat instance has no twin* (§2.3 (2)).

**Families tried, at the exponential scale** (`r8_05_conjecture.py`; rates per site by the Laplace
principle — the kind of evidence the addendum uses for its terrace family).  For landscapes that are
radial about a point `a₀` near the twin, the twin centre `a′` is placed uniformly on its orbit (the
sphere of radius `πn` about `a₀`); a point that differs from `a′` in `αn` of the `πn` coordinates
where `a₀, a′` differ and in `βn` of the others lies in `D` with probability `e^{−nΦ(α,β)}`,
`Φ = h(π−α+β) − πh(α/π) − (1−π)h(β/(1−π))`, and the family's exponent is `min_D Φ` (validated against
exact sums below).

| family | visible landscape | twin | result |
|---|---|---|---|
| F1 | a dominant *soft* basin `−v(ρ_c − δ)₊`, `0.2u ≤ v ≤ u`, cap from threshold to `ρ_c = 1` (a global tilt) | plateau at the datum's level, centre anywhere (`π` from inside the basin to `½`) | best at `v = u`, cap at threshold, twin far away — the addendum's twin |
| F5 | remote dominant cone basin + a sub-dominant terrace (depth `ub`, radius `ρ_t`) | plateau inside or across the terrace | best at `b = 0` (no terrace) |
| F2 | product: flat block (`φn` sites) × cone block | ball in the flat block × flooded cone | far below `θ_pl`, mostly `0` |
| F3 | `e^{γn}` visible basins | one plateau on the flat background | decreasing in `γ` |
| F4 | "egg carton" `u·dist(x, C)`, `C` a code of rate `γ` | one flooded cell | at most `0.57·θ_pl` |

| `u` | `ε₁/a` | `θ_pl` | `θ_hint` | F1 | F5 | F2 | F3 | F4 |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.1 | 0.02382 | 0.02396 | 0.02360 | 0.02382 | 0.00434 | 0.02382 | 0.01360 |
| 1 | 0.3 | 0.01402 | 0.01516 | 0.01385 | 0.01402 | 0 | 0.01402 | 0.00420 |
| 1 | 0.5 | 0.00585 | 0.00838 | 0.00574 | 0.00585 | 0 | 0.00585 | 0.00002 |
| 2 | 0.1 | 0.08214 | 0.08271 | 0.08172 | 0.08214 | 0.01477 | 0.08214 | 0.04481 |
| 2 | 0.3 | 0.05286 | 0.05736 | 0.05253 | 0.05286 | 0 | 0.05286 | 0.01587 |
| 2 | 0.6 | 0.01500 | 0.02838 | 0.01482 | 0.01500 | 0 | 0.01500 | 0 |
| 4 | 0.1 | 0.21371 | 0.21600 | 0.21297 | 0.21371 | 0.03436 | 0.21371 | 0.09931 |
| 4 | 0.3 | 0.15677 | 0.17397 | 0.15616 | 0.15677 | 0.00003 | 0.15677 | 0.04187 |
| 4 | 0.6 | 0.06758 | 0.12092 | 0.06720 | 0.06758 | 0 | 0.06758 | 0 |
| 0.5 | 0.3 | 0.00353 | 0.00382 | 0.00345 | 0.00353 | 0 | 0.00353 | 0.00105 |

(F1 is slightly below `θ_pl` only because its cap sits `0.0005` above threshold.)  **No family beats
`θ_pl`; each one's optimum is the plateau twin on the flat background.**  **[N, exponential scale]**

**Explicit pairs with exact sums on non-flat landscapes** (`r8_11_tilt_exact.py`, `n = 600`, `u = 2`):
the twin exists in every case (`U′ = U` exactly by the excess identity, gap `> ε`); the exact
hit-probability exponents are

| visible landscape | twin centre | exact exponent | rate machinery | plateau twin, flat background, same `n, u, ε` |
|---|---|---|---|---|
| soft basin, `v = 0.7u` | far (`0.5n`) | 0.0495 | 0.0454 | 0.0708 |
| soft basin, `v = 0.7u` | on the rim (`0.4n`) | 0.0370 | 0.0330 | 0.0708 |
| soft basin, `v = 0.5u` | `0.45n` | 0.0316 | 0.0279 | 0.0786 |
| global tilt, `v = 0.6u` | `0.45n` | **0.0000** | 0.0000 | 0.0786 |
| global tilt, `v = 0.4u` | `0.40n` | **0.0000** | 0.0000 | 0.0855 |

(the machinery is below the exact value by the finite-`n` prefactor, about `0.004`).  **[N]**

**Why slopes do not help [P for the mechanism].**  Where the visible landscape has slope `v` along a
coordinate direction, a dip of depth `δ₀` at `p` changes the landscape on
`{(u+v)·i + (u−v)·j < δ₀}` (`i` downhill flips, `j` uphill flips): it reaches `δ₀/(u−v)` uphill.  A query
far uphill is at a typical distance from every placement of the twin and lies in the difference
set — on a global tilt **one query finds the twin** (the two rows `0.0000` above: the worst query has
weight 578 resp. 596 of 600).  At `v = u` a dip contains everything farther out (the addendum's
evidence (iii)).  A slope is a direction from which a hidden state is visible; flatness is what hides
it, and flatness costs a wall of width (depth)/`u`.

**The small-slope limit: a "column bound" [H].**  For `u → 0` put `λ² = nu²/4` and, for a centre `a`,
`ζ_a = (n − 2d(x,a))/(λ√n)`: a ball of radius `(½ − ur)n` is `{ζ_a ≥ 4r}` with measure `e^{−λ²(4r)²/2}`,
a cone is the ramp `−λ²(ζ_a − τ)₊` (typical point `ζ = 1`, entropy deficit `½λ² = a·n`, dominant iff
`τ ≤ ½`), and centres at distance `≈ n/2` give independent Gaussian coordinates.  Let the visible
landscape be **any** `1`-Lipschitz `G(ζ₀)` of finitely many visible directions, with rate
`z = max(−G − |ζ₀|²/2)` attained at `ζ₀*`, `U = G(ζ₀*)`; Lipschitz forces `|ζ₀*| ≤ 1` (the entropy
bracket).  Let the twin be hidden in a fresh direction: `D ⊂ {ζ₁ ≥ b}`, cost exponent `b²/2`.  Its
excess has rate `z + e′` (`e′ = ε₁n/λ²`) at a point `q = (q₀, q₁)`, `q₁ ≥ b`, at level `ℓ`:
`−ℓ − |q|²/2 = z + e′`.  Two inequalities — Lipschitz from `q` to the unmodified point `(q₀, b)`,
`G(q₀) ≤ ℓ + q₁ − b`, and optimality of the visible state in the column of `q₀`,
`−G(q₀) − |q₀|²/2 ≤ z` — add up to

    b ≤ q₁ − q₁²/2 − e′.

Without the datum `q₁ = 1` is allowed: `b ≤ ½ − e′`, which is `θ_hint` in this limit,
`(u²/32)(1 − ε₁/a)²`.  With the datum `ℓ = U`, so `|q|² = |ζ₀*|² − 2e′ ≤ 1 − 2e′` and

    b ≤ √(1 − 2e′) − ½,        i.e.   θ ≤ (u²/8)(√(1 − ε₁/a) − ½)²  =  θ_pl in this limit.

So **in the small-slope limit, whatever the visible landscape, no twin hidden in a fresh random
direction beats the plateau twin; the datum enters only through the entropy bracket of the visible
state and the identity.**  Closed forms in this limit for the tilt and the egg carton (`r8_05`, part
G) are below the plateau value by factors 2.8 and 1.5 at `ε₁ → 0`.  This is a Laplace-scale
argument in a limit model, not a proof on the cube: a finite-`u` version needs an isoperimetric
statement on spheres of the cube (Johnson scheme), which I do not have.

**What is not excluded.**  (1) Landscapes with exponentially many *prepared sites* (funnels at
several levels), where the family of twins is indexed by visible features instead of a fresh
direction.  For single-level terraces a counting bound gives `θ ≤ s + uw − h(h⁻¹(s+ε₁) + w)` (`s` the
visible entropy, `w` the wall), increasing in `w` up to the whole cube — again `θ_pl` **[H]**; graded
funnels are not covered.  (2) Twins that are not single-level plateaus on a non-flat background
(for a given support the Lagrangian gives a level clipped between the McShane envelopes; the
optimal support is unknown).  (3) Lower bounds that are not of the form "one visible instance and
its alternatives".  (4) **The interval `ε₁ᶜ ≤ ε₁ < a(u)`**: the conjecture says the exponent is zero
there; the plateau twin is void, the counting limit `a − ε₁` is positive, and I have neither an
algorithm for general instances nor a twin.  At instances that are constant outside a small set the
algorithm of A16.6 (ii) with `R ≈ n/2` does give cost `O(ln(1/δ))` there **[P]**.

**Verdict.**  Not refuted.  **[C]** stands.  My own reading **[H]**: for `ε₁ < ε₁ᶜ` the conjectured value
is probably right; for `[ε₁ᶜ, a)` I have no evidence either way beyond the flat-outside-a-small-set
instances.

## 4. The non-adaptive guess `θ_na^U(ε₁) = θ_na(u(σ₂(ε₁) − σ_u))`

**The pair exists.**  Centre `s`, `d = d_H(x, s)`.

> **R8.6 [P (sketch for the asymptotics); exact sums in seven cases, `r8_06_nonadaptive.py`].**
> Outside the open ball `{d < R₃}` let both members be the cone `ud`; inside,
> `g_A = u·max(d, R₁)` (the cone truncated at `R₁ ≤ R₃`) and `g_B = min(uR₃, c₂ + ud)` (the cone raised
> by `c₂ ≥ 0` under a plateau ring at level `uR₃`).  Both are members; they differ only inside the
> ball.  `U_{g_B}` is continuous and increasing in `c₂` from the cone's energy to that of the cone
> truncated at `R₃`, so for every `R₁` there is exactly one `c₂` with **`U_{g_A} = U_{g_B}`**.  As long
> as the raised cone dominates its ring — `c₂ < n·KL(R₃/n‖σ_u) − O(ln n)` — the entropies are
> `n·h(R₁/n) + O(ln n)` and `n·h(σ_u) + o(1)`, the root is `c₂ = u(R₁ − σ_u n) + O(1)`, and
> `ln Z_A − ln Z_B = n[h(R₁/n) − h(σ_u)] − O(ln n)`.  A gap `> ε₁n` therefore needs `R₁/n > σ₂(ε₁)` and
> `KL(R₃/n‖σ_u) > u(σ₂(ε₁) − σ_u)`.  Since both members have the same datum for every centre, the
> averaging argument of theory report Theorem 11.45(a) goes through with the datum given to the
> algorithm, and
> **`θ_na^U(ε₁) ≥ θ_na(u(σ₂(ε₁) − σ_u))`**.

Exact sums (`U_A = U_B` to `10⁻¹³`, values equal outside the ball, both Lipschitz):

| `n` | `u` | `ε₁/a` | smallest `R₃` with a gap `> ε₁n` | guess `ρ₃n` | `c₂` (`u(σ₂−σ)n`) | exponent `n⁻¹ln(2ⁿ/|B(n,R₃−1)|)` (guess, asymptotic) | without the datum (asymptotic `θ_na(ε₁)`) |
|---|---|---|---|---|---|---|---|
| 600 | 1 | 0.3 | 242 | 236.2 | 24.5 (22.0) | 0.0233 (0.0228) | 0.0332 (0.0254) |
| 1000 | 1 | 0.3 | 400 | 393.7 | 39.2 (36.6) | 0.0231 (0.0228) | 0.0303 (0.0254) |
| 1000 | 1 | 0.6 | 468 | 459.9 | 87.2 (83.2) | 0.0039 (0.0032) | 0.0105 (0.0075) |
| 800 | 2 | 0.3 | 241 | 236.8 | 92.7 (89.2) | 0.0859 (0.0857) | 0.1039 (0.0964) |
| 800 | 2 | 0.6 | 329 | 323.5 | 214.8 (208.8) | 0.0193 (0.0184) | 0.0439 (0.0385) |
| 600 | 4 | 0.4 | 128 | 124.9 | 208.8 (203.7) | 0.1818 (0.1815) | 0.2474 (0.2380) |
| 1200 | 0.5 | 0.4 | 560 | 550.5 | 18.5 (16.4) | 0.0039 (0.0034) | 0.0070 (0.0043) |

**Two corrections to the addendum's description.**  (1) The inner cone need not be *displaced*; and a
displaced one, `c₂ + u·d(x, s′)`, is a member only if `c₂ ≥ u·d(s, s′)` (enumeration at `n = 14`:
Lipschitz constant `2u` for `c₂ = 2u`, `d(s,s′) = 3`; `u` for `c₂ ≥ 3u`) — displacement buys nothing.
(2) "`θ_na^U(0⁺) = a` unchanged and `θ_na^U = 0` from `ε₁ᶜ` on" is what the formula gives
(`u(σ₂ − σ_u) ≥ ln cosh(u/2)` iff `ε₁ ≥ ε₁ᶜ`): correct as arithmetic **[P]**.

**Why this pair is the natural one [H].**  Inside an unexplored ball of a cone every filling lies
above the cone.  At a given mean energy the filling of largest entropy is the truncated cone, and
the smallest entropy, `n·h(σ_u)`, is reached by a raised cone as long as it dominates the ring at
the boundary; mixtures of cone and ring lie on a chord of slope one and do worse.  The condition
"the low-entropy state must dominate the background it hides against, at a depth of at least
(entropy of that background `− n·h(σ_u)`)/`u`" is the same for the adaptive twin (background: the whole
cube, `ln 2`) and for this pair (background: the ring, `h(ρ₃)`); it gives `ρ₂ = σ₂ + a/u` in one case
and `KL(ρ₃‖σ_u) = u(σ₂ − σ_u)` in the other.

**The bracket of remark (4), evaluated [N]** (`r8_06`, part 2; exact radial sums; lower end = the
larger of what the sample shows and the entropy bracket; upper end minimised over `η`).  For each
instance, the smallest sample for which the bracket is narrower than `ε₁n`, expressed as the
largest unexplored radius; worst instance of six radial families (the cone; 24–49 truncated cones;
45–100 raised cones; 40 plateau basins on a flat background; soft cones; two-slope cones):

| `n` | `u` | `ε₁/a` | worst needed unexplored radius (family) | guess `ρ₃n` | radius without the datum |
|---|---|---|---|---|---|
| 400 | 1 | 0.3 | 155 (raised cones) | 157.5 | 155.1 |
| 400 | 1 | 0.6 | 183 (raised cones) | 183.9 | 175.6 |
| 400 | 2 | 0.4 | 131 (truncated cones) | 133.0 | 125.1 |
| 300 | 4 | 0.4 | 62 (truncated cones) | 62.5 | 50.9 |

On these families the bracket needs the sample the guess predicts, within 0.5–2.5 sites, and the
worst instances are the two members of the pair.  (In the first row the three radii cannot be
told apart at `n = 400`.)  The bracket contained the truth in every one of the about 110 000
(instance, radius) evaluations.  **This is not the worst case over the class**, which I did not
evaluate: for the class one needs the analogue of theory report Theorem 11.44 with the datum —
in particular a datum-assisted *lower* end better than "sample or entropy bracket".

**Verdict.**  The pair is valid; "`≥`" is proved (at sketch level, with exact sums); "`=`" is open, and
consistent with everything computed.

---

## 5. Numerics: what was computed, sizes, results, how to re-run

All in `experiments/science/ws_R8/`; run from that directory (`python3 <script>`); every script has
its log next to it.  Nothing imports the coordinator's code.  **Run first:** `r8_03_isoperimetry.py`
(the lemma over general members), `r8_08_matching.py` (R8.3), `r8_04_theorem166.py` (the cost
bookkeeping of A16.6).

| script (time) | what | sizes | result |
|---|---|---|---|
| `r8_01_bracket.py` (2 min) | A16.1 on eight families, adversarial entropy minimisation, chain-rule step, product reference, mutation; A16.2 identities and table | `n ≤ 12`; 576 + 288 members; `mpmath` 40 digits | no violation; minimum entropy `= n·h(σ)` to `10⁻¹⁴`; table reproduced |
| `r8_02_twin.py` (1.5 min) | A16.3: joint-law sums validated against enumeration (`n = 16`); twelve own twins; smallest `n` with a root; close centres | `n ≤ 2400` (`1.4·10⁶` terms per evaluation) | (a), (b), (c) in all cases; root unique on a grid; roots from `n = 60` |
| `r8_03_isoperimetry.py` (5 min; `quick` option) | A16.5: Harper form on all subsets of `Q_3`, `Q_4`; convex programme over all members on every support of `Q_3`, `Q_4` and random ones in `Q_5`, `Q_6`; exhaustive grids; random members; mutations | 65 534 supports; `1.15·10⁷` and `2.77·10⁸` grid functions | no violation; LP certificates to `1.2·10⁻⁷`; mutations fire |
| `r8_04_theorem166.py` (1.5 min) | table of A16 (b); twins against `G(R)`; radii of lower and upper bound; probability of meeting `V`; expected cost with fallbacks; (iv); bracket validity; bounded gaps | `n ≤ 2400`; 300 members at `n = 10, 12` | §2.5 |
| `r8_05_conjecture.py` (2.5 min; `quick`) | five families at the exponential scale; small-slope closed forms | ten `(u, ε₁)`; grids `240²` with two zooms | nothing above `θ_pl` |
| `r8_06_nonadaptive.py` (`part1`: 1 min; all: **29 min** — longer than intended) | the pair exactly; displaced inner cone; bracket of remark (4) on six radial families | `n ≤ 1200`; `≈ 1.1·10⁵` bracket evaluations | §4 |
| `r8_07_deepend.py` (1 s) | R8.1 line by line; Hoeffding thresholds; `k₀` of R8.4 | eight cases, `n ≤ 800` | chain holds |
| `r8_08_matching.py` (1.2 min) | R8.3 | twelve cases | holds; size of the difference explained |
| `r8_09_replicate_examples.py` (0.5 min) | the two examples of A16 (b) | `n = 600, 2000` | first reproduced; second needs `ρ₁ = ρ₀ + 0.03` |
| `r8_10_replicate_json.py` (1.3 min) | the coordinator's ten twins (reads their JSON, read-only) | `n ≤ 2000` | all ten reproduced (`r₁, r₂` exact; `κ*`, gap to `10⁻⁴`) |
| `r8_11_tilt_exact.py` (0.3 min) | explicit pairs on soft basins and global tilts, exact hit probabilities | `n = 600` | §3 |
| `A16Core.lean` (8 s) | algebraic core of A16.5 | — | compiles; standard axioms |

*Where mine differ from the coordinator's.*  (1) `energy_isoperimetry_check.py` assumes the clipped
level on each support; `r8_03` parts B, C do not.  (2) `plateau_twin_check.py` finds the root with
`brentq`; I use bisection on the excess identity with a separate count of sign changes; same numbers.
(3) `terrace_twin_explore.py` puts the terrace at the co-dominant level and the twin on its rim; my
F5 lets the depth vary and places a Hamming-ball twin anywhere; same conclusion.

**A defect in the evidence trail [checked by running a byte-identical copy inside my directory].**
`experiments/science/pi_inference/plateau_twin_check.py`, as committed, **aborts with an
`AssertionError` at line 190** — the series of A16.2 is summed to 4000 terms and compared at `u = 8`
with tolerance `10⁻⁹`; the truncation error there is `3.7·10⁻⁴` (with `4·10⁵` terms: `7.5·10⁻¹⁵`).  The
committed `plateau_twin_check.log` ends in that traceback and contains **none** of the ten twin
cases; `plateau_twin_check.json`, written 52 seconds before the last modification of the script,
has them.  The mathematics is untouched (the identity is right; the ten twins are right — I
reproduced them), but the reproduction line of SCI-MSG-0012 ("`python3 … plateau_twin_check.py`
(30 s; … ten exact plateau twins)") does not work.  Fix: drop `u = 8` from that loop or sum
`4·10⁵` terms, and regenerate the log.

## 6. Prior art (brief), with the search log

Reading levels as required: `[abstract]` here means the abstract as returned by a page-fetching tool
that gives a model-made extract, not the page itself.

* **The class is a known object by another name.**  A measure on `{0,1}ⁿ` whose conditional odds of
  each bit *given all the others* are bounded is a **strong Santha–Vazirani source** (Gavinsky,
  Pudlák, "Santha–Vazirani sources, deterministic condensers and very strong extractors",
  arXiv:1907.04640 `[abstract]`: it defines SV sources by limited dependence of the `i`-th bit on the
  previous ones, strong SV sources by limited dependence on the remaining `n − 1` bits, and notes
  that they have min-entropy `Ω(n)`; Definition 1 and the body were **not** read).  The Gibbs
  measures of the cube class are exactly the strong SV sources with bias window `[σ_u, 1−σ_u]`.  The
  Shannon bound `n·h(σ_u)` is the chain rule applied to that definition; I did not find it stated in
  this form in the snippets (it is too elementary to be stated), and the original paper of Santha
  and Vazirani (1986) `[from memory — unverified; not opened]`.  In the sampling literature the same
  property is called marginal boundedness (Chen, Liu, Vigoda, arXiv:2011.02075, Definition 1.6
  according to a `[search snippet]`; the `[abstract]` does not mention it).  **Verdict: A16.1's
  inequality is [K] in other words; within this branch it is Theorem 2(d).  What is specific to A16
  is the use — a datum plus this bound brackets `ln Z`.**  That use was not found; this is not a
  claim of novelty.
* **Isoperimetry with an energy constraint.**  Nothing found that states it: searches for an
  isoperimetric problem on the cube with a second (energy or entropy) constraint returned
  Harper-type results and their stability versions only (Keevash–Long, Przykucki–Roberts, Räty —
  `[search snippets]`), and Bobkov–Houdré–Tetali on exponential moments of Lipschitz functions on
  graphs (`[search snippet]`; the PDF fetch failed with HTTP 503), which is the neighbourhood of the
  *unconstrained* tail lemma.  The structure of the optimiser — a constant level clipped between two
  envelopes — is that of the "bathtub principle" for integrals under pointwise bounds (Lieb–Loss,
  *Analysis* `[from memory — unverified]`).  **Verdict: not found in print in the three searches devoted to it (queries 3, 4, 7), at the
  level of snippets; a five-line argument on top of Harper's theorem; I would call it "short and not
  found", not "new".**

*Search log* (web search tool; no project detail in any query).
1. `Santha-Vazirani source Shannon entropy lower bound n h(delta) conditional bias bounded chain rule` → Gavinsky–Pudlák; Skórski (chain rules for min-entropy); no statement of the exact bound.
2. `"marginally bounded" distribution hypercube conditional marginals bounded entropy lower bound spin system "b-marginally bounded"` → Chen–Liu–Vigoda (definition); no entropy bound.
3. `Lipschitz functions on the discrete cube extremal problem Harper theorem maximize expectation of exponential distance to Hamming ball isoperimetric inequality Lipschitz` → Bobkov–Houdré–Tetali; Bobkov (1997), Bobkov–Götze (1999); nothing with a second constraint.
4. `isoperimetric inequality with two constraints hypercube maximum entropy fixed mean energy Lipschitz potential "plateau" OR "truncated cone" extremal "Harper"` → edge-isoperimetric and Gaussian results; nothing relevant.
5. `entropy of probability measure on hypercube with log-Lipschitz density "bounded log-ratio" neighbouring configurations entropy at least n times binary entropy` → nothing relevant.
6. `"strong Santha-Vazirani" source definition bias conditional on all other bits min-entropy Shannon entropy rate` → Gavinsky–Pudlák again.
7. `vertex isoperimetric inequality Hamming cube weighted "Lipschitz" functions "inner parallel" sets Harper theorem simultaneous all radii nested neighbourhoods extremal function "distance to" ball maximizes convex functional` → stability of Harper's theorem; nothing with a constraint.
8. Fetches: arXiv abstract pages 1907.04640 and 2011.02075 (read as extracts); Bobkov–Houdré–Tetali PDF (HTTP 503, not read).

---

## 7. Overstatements: every sentence that says more than is proved, with replacement text

"Proved" means: proved in A16 as written.  Where this report closes the gap, the replacement cites
it.  Severity: **A** = says something false or unsupported as written; **B** = right but unproved
there (now proved here) or missing a hypothesis; **C** = wording.

### SCI-MSG-0013

**O1 (B) — title.**  "…with it the plateau-twin bound is **the exact cost** at the visible basin".
Proved in A16: the exponent.  The `Θ` rested on eight numerical cases and on comparing an expectation
with a high-probability bound (F1, F2).
> *Replace by:* "…with it the plateau-twin bound is the cost exponent at the visible basin, and the
> cost itself up to a constant factor (in a quantile sense; R8 report, R8.2–R8.3)".

**O2 (A) — §2 (ii).**  "the algorithm 'draw `2ⁿ ln(1/δ)/|B(n,R)|` uniform points; if they all show one
value, return the midpoint of the datum's bracket `[n·h(σ_u) − U, ln Z^{pl}(R, U)]` when it is narrow
enough; otherwise run any class-correct procedure' needs no hint, is correct on the whole class, and
stops after the samples at `g₀`".  Three things: the bracket is printed without the gauge and is
then **not** correct on the class (F4: wrong with probability one at `g ≡ v < 0`); "stops" holds with
probability `1 − e^{−Ω(n)}`, not always, and the expected cost depends on the fallback (F1); `R` must
come from somewhere (F3).
> *Replace by:* "the algorithm 'draw one point and read its value `v`; let `R` be the largest radius
> at which the bracket `[max(ln(2ⁿ−|B(n,R)|), n·h(σ_u) − (U−v)), ln Z^{pl}(R, min(U−v,0))]` for `ln Z + v`
> is narrower than `ε`; draw `2ⁿ ln(1/δ)/|B(n,R)|` uniform points; if they all show `v`, return the
> midpoint; in every other case evaluate everything' needs no hint, is correct on the whole class
> with probability at least `1 − δ`, and at `g₀` stops after the samples with probability
> `1 − e^{−Ω(n)}` (its *expected* cost is of that order only for the tolerant variant R8.4 of the R8
> report)".

**O3 (B) — §2.**  "So **with the datum the cost at `g₀` is `Θ(2ⁿ/|B(n, R(ε))|)`**".
> *Replace by:* "So with the datum the cost at `g₀` is `Θ(2ⁿ/|B(n,R(ε))|)` in the following sense:
> every class-correct algorithm needs more than `½(1−2δ)·2ⁿ/|B(n,R(ε)+2)|` evaluations with
> probability at least `½(1−2δ) − o(1)`, and the algorithm above needs at most
> `ln(1/δ)·2ⁿ/|B(n,R(ε))|` with probability `1 − e^{−Ω(n)}` (R8 report: R8.2, R8.3)".

**O4 (A) — lemma header and "Evidence and reproduction".**  "[P; brute force on all 65 534 supports in
`Q_4`, 8 000 random supports in `Q_5`, `Q_6`, …]" and "the lemma on all supports of `Q_4` and on random
ones in `Q_5`, `Q_6` (661 806 cases…)".  That check takes the optimal modification on each support to
be the clipped level; it tests the Harper step, not the lemma.
> *Replace by:* "[P; the Harper step checked on all 65 534 supports of `Q_4` (clipped-level profile on
> each); the lemma over general members: a convex programme on every support of `Q_3`, `Q_4` and an
> exhaustive grid of `2.8·10⁸` Lipschitz functions on `Q_4` (R8 report, `r8_03_isoperimetry.py`);
> algebraic core machine-checked (`A16Core.lean`)]".

**O5 (C) — §3, the guess.**  "…either the truncated cone or a **displaced** inner cone with the same
mean energy".
> *Replace by:* "…either the truncated cone or the cone raised by a constant under a plateau ring,
> with the same mean energy (the pair exists — R8 report, R8.6 — and proves '`≥`'; a displaced inner
> cone is admissible only when raised by at least `u` times the displacement and gains nothing)".

### SCI-MSG-0012

**O6 (A) — "Evidence and reproduction".**  "`python3 experiments/science/pi_inference/plateau_twin_check.py`
(30 s; entropy bracket on 400 random members by enumeration; the two relative entropies; ten exact
plateau twins)".  As committed the script aborts at an assertion before the twins (§5).
> *Replace by:* the same line after repairing the script (sum the series to `4·10⁵` terms or drop
> `u = 8`) and regenerating the log; until then: "the ten twins are in `plateau_twin_check.json` and
> were reproduced independently (R8 report, `r8_10_replicate_json.py`)".

**O7 (B) — §2 (c).**  "for every integer `r₂ > r₁` (below `n/2`) there is a real `κ* > (|U₀|−1)/u` with
**exactly** equal mean energies".  The proposition has hypotheses.
> *Replace by:* "for every integer `r₂ > r₁` below `n/2`, every centre at distance `n/2 ± √(n ln n)`
> and all large `n` (precisely: whenever `|U₀| > 1` and the twin's full cone overlaps the visible
> basin in a weight fraction below `1/r₂` — R8 report, R8.1) there is a real `κ* > (|U₀|−1)/u` with
> exactly equal mean energies".

**O8 (C) — §3.**  "below, the best we can say is the bracket of §2(c)".  Between `ε₁ᶜ` and `a(u)` the
lower end of that bracket is zero (§2(c) says so in its display; the sentence does not).
> *Replace by:* "below `ε₁ᶜ`, the best we can say is the bracket of §2(c); between `ε₁ᶜ` and `a(u)` we
> have no lower bound at all".

### Digest (`SCIENCE_TO_ALL.md`)

**O9 (B) — item 25 (c).**  "Below `a(u)` a hidden state must be as deep as the visible one and
exponentially wider — a 'plateau twin' — which gives `θ_U(ε₁) ≥ …`, **close to `θ_hint(ε₁)`**".  The
bound is void from `ε₁ᶜ` on (`0.086, 0.273, 0.557` against `a = 0.111, 0.328, 0.603`), and "close" is
true to second order in `ε₁` only (`0.0275` against `0.0985` at `u = 4`, `ε₁ = 0.75a`).
> *Replace by:* "Below `ε₁ᶜ < a(u)` a hidden state must be as deep as the visible one and
> exponentially wider — a 'plateau twin' — which gives `θ_U(ε₁) ≥ ln 2 − h(ρ₀ − σ_u + h⁻¹(h(σ_u)+ε₁))`:
> equal to `θ_hint(ε₁)` to first order in `ε₁`, a factor of several below it near `ε₁ᶜ`; between `ε₁ᶜ`
> and `a(u)` there is no lower bound".

**O10 (A) — item 27.**  "…convex duality in the weights plus Harper's theorem; **brute force on every
support of `Q_4`**".  As O4.
> *Replace by:* "…; Harper step checked on every support of `Q_4`; the lemma itself checked over
> general members and its algebraic core machine-checked by workstream R8".

**O11 (B) — item 27.**  "Consequence: with the datum, the cost at the visible basin is
`Θ(2ⁿ/|B(n,R(ε))|)` — the plateau twin is optimal and so is uniform sampling with the datum's
bracket, without a hint".
> *Replace by:* "Consequence: with the datum, the cost at the visible basin is
> `2ⁿ/|B(n,R(ε))|` up to a constant factor and two units of the radius, in a quantile sense (exponent
> `ln 2 − h(ρ₁ − σ_u + σ₂(ε₁))`): no alternative on a support of that size does better than the
> plateau, and uniform sampling with the datum's bracket attains it, with `R` chosen from the datum
> and one sample (R8 report, R8.2–R8.5)".

### Status rows (`status/science.md`)

**O12 (B) — S34 (c).**  "below, a 'plateau twin' (as deep, exponentially wider) gives `θ_U(ε₁) ≥ …`".
> *Insert:* "for `ε₁ < ε₁ᶜ = h(½ − ρ₀ + σ_u) − h(σ_u)`"; and in the last column, after "author only":
> "; refereed by R8 — proved, deep end written out; ten twins reproduced".

**O13 (A/B) — S36.**  "Theorem A16.6: with the datum the cost at the visible basin is
`Θ(2ⁿ/|B(n,R(ε))|)` — the plateau twin is the optimal obstruction and uniform sampling with the
datum's bracket the optimal algorithm (no hint) … | **[P]**, author only; brute force on all supports
of `Q_4` (661 806 cases…)".
> *Replace the claim by:* "Theorem A16.6: with the datum the cost at the visible basin is
> `2ⁿ/|B(n,R(ε))|` up to a constant and two units of the radius (quantile sense; in expectation for a
> tolerant variant of the test) — no alternative on a support of that size beats the plateau twin,
> and uniform sampling with the datum's bracket attains it"; *and the status by:* "lemma **[P]**,
> algebraic core **[V]** (`ws_R8/A16Core.lean`), general members by brute force (R8); theorem
> **[P] after the repairs of the R8 report** (R8.2–R8.5); Harper step on all supports of `Q_4`".

### The addendum itself (A16)

**O14 (B).**  (a) Theorem A16.6, header "[P, given A16.1, A16.3, A16.5; exact sums]" and (iii) "It
matches. … up to `10⁻³` in all eight exact cases … lower and upper bound differ by the factor
`ln(1/δ)/(1−2δ)` and one unit of the radius": the match is R8.3 and "one unit" is "at most two";
the comparison needs R8.2 or R8.4.  (b) (ii) "correct on the whole class with probability
`1 − δ(1+o(1))`": add the fallback's failure probability; the factor is `e^{|B(n,R)|/2ⁿ}`.  (c) Lemma
A16.5: delete "`R < n/2`"; "For the ball the maximiser inside `F_η` is `min(t*_η, e^{uρ})`" → "for the
`η` chosen below, …"; add that the level exists and is unique because `dU/dc = −μ(P)(1+c+U) < 0`;
header "[P; brute force: all 65 534 supports …]" as O4.  (d) Remark (4): add "for `η` with
`η(U + ln t) ≤ 1`, or with the exact size of `D`".
> *Replacement for (iii):* "(iii) *It matches.*  With `g″ = T_{κ*}` alone on the flat background and
> `U″` its mean energy, `G(r₂−1) − (U″−U₀)₊ ≤ ln Z′ − ln Z₀ ≤ G(r₂)` (R8 report, R8.3; `U″ − U₀` is
> exponentially small at extensive accuracy; equality with `G(r₂−1)` to `10⁻¹¹` in the exact cases).
> So with the datum, at `g₀`, every class-correct algorithm needs more than `m` evaluations with
> probability `≥ (1−2δ)(1−2/n²) − m|B(n,R(ε)+2)|/2ⁿ`, and the algorithm of (ii) needs
> `⌈2ⁿln(1/δ)/|B(n,R(ε))|⌉` with probability `1 − e^{−Ω(n)}`."

**O15 (C).**  (a) Header "Scripts: `plateau_twin_check.py` (30 s)": see O6.  (b) Part (b), second
example: "`n = 600`, `u = 4`, gap `0.30n`: `r₂ = 190` against `147`" → add "(`ρ₁ = ρ₀ + 0.03`)".  (c) Part
(d), "(the lower value is the exact cost at the threshold basin: A16.6)" → "(the lower value is the
cost exponent of the basins `ρ₁ ↓ ρ₀`: A16.6)".

Sentences I checked and found **not** overstated: SCI-MSG-0012 §2 (a), (b), the table, "always at
least as large" (true: §2.3); SCI-MSG-0013 "Theorem A16.6 is a statement about the cost *at one
instance* …, not about the worst case over the class" (a correct and necessary caveat); digest 25
(a), (b), (d); S34 (a), (b), (d); "the conjecture … is reduced to instances that are not flat outside
a small set" (fair: what remains is an upper bound for those instances).

---

## 8. What I did not settle; next steps; requests

**Not settled.**
1. Conjecture A16.4 for instances that are not flat outside a small set, and — separately — the
   interval `ε₁ᶜ ≤ ε₁ < a(u)`, where even the right answer is unclear to me (§3).
2. The non-adaptive exponent with the datum: "`≥`" is R8.6; the class-wide "`≤`" is open (§4).
3. The column bound of §3 on the cube at fixed `u`.
4. R8.4 was not simulated and its constants are crude; R8.6 is at sketch level for the `O(ln n)` terms.
5. The plateau twin against the marginal oracle, a field, a tolerance on the datum (listed as "not
   done" in A16): not examined.

**The three most promising next steps.**
1. *An upper bound on one genuinely sloped instance.*  The exact pairs on global tilts (§3) are found
   by a single query far uphill.  Turn this into a statement: for the instance `v|x|`, `0 < v < u`,
   every member with the same datum and `ln Z` larger by `ε₁n` differs from it at a point of weight
   `≥ (1 − o(1))n`, or on a set of measure `≥ e^{−nθ}` with `θ` explicit and `< θ_pl(ε₁)`.  This is the
   smallest case of "the lemma for a general reference" and tells whether the nested algorithm
   needs the datum at every level or only at the top.
2. *The column bound on the cube.*  For a radial visible landscape and twins placed by the
   stabiliser of its centre, the argument of §3 goes through with "distance to the complement
   inside a sphere of the cube" in place of `q₁ − b`; it needs a vertex-isoperimetric inequality on
   a slice at the exponential scale.  With it, the conjecture would be a theorem for all radial
   visible landscapes.
3. *The non-adaptive upper bound.*  Combine the bracket of remark (4) (upper end) with the two lower
   ends used in §4 inside the proof of theory report Theorem 11.44; the worst cases found
   numerically are the two members of the pair of R8.6, which suggests the missing lemma: "among
   members with given values outside a set of measure `q` and given datum, the least `Z` is that of
   a raised cone".

**Requests.**

*To the theory division.*
* **T-R8-1.**  Check Lemma A16.5 in the form "for all `g` with `|g(x)| ≤ u·dist(x, supp^c)`" and the two
  statements R8.1, R8.3 of this report; if they stand, state them next to Lemma 11.43(b).  The
  algebraic core is in `experiments/science/ws_R8/A16Core.lean` (ten declarations, standard axioms).
  What is missing for a full machine check is the rearrangement step: *if `F` is nondecreasing and
  `#{ρ ≥ k} ≤ #{ρ* ≥ k}` for all `k`, then `Σ_x F(ρ(x)) ≤ Σ_x F(ρ*(x))`* (Harper's theorem as a
  hypothesis), and the monotonicity `dU/dc = −μ(P)(1 + c + U)`.
* **T-R8-2.**  With the exact datum `U = E_{μ_g} g`, is there an algorithm that is `ε₁n`-accurate on
  the whole cube class with `e^{o(n)}` evaluations for some `ε₁ < a(u)`?  (A16 conjectures yes for all
  `ε₁ ≥ ε₁ᶜ = h(½ − ρ₀ + σ_u) − h(σ_u)`; at instances constant outside a small set it is true; a twin
  argument cannot exclude it below `a(u) − ε₁`.)
* **T-R8-3.**  Exponential-scale vertex isoperimetry on a slice `{|x| = κn}` of the cube: for
  `A ⊂` slice of density `e^{−θn}`, how large must the set of points at Hamming distance `≤ 2wn`
  from `A` inside the slice be?  (Balls of the Johnson scheme are the natural candidates; only the
  exponent is needed.)

*To the engineering division* (optional; a consistency test, not a decisive computation).
* **E-R8-1.**  *Motivation:* the algorithm of A16.6 (ii) and its tolerant variant R8.4 were analysed,
  never run.  *Formulation:* `n = 24…32`, `u ∈ {2, 4}`; instances: the flat function, the basin `g₀`
  (`r₁ = ⌈(ρ₀+0.05)n⌉`), `g₀` plus an exact plateau twin (level by bisection on the excess identity),
  two instances with two level sets of comparable size, a cone; datum by exact enumeration.
  *Algorithm:* as in O2's replacement text and as in R8.4 with `k₀ ∈ {0, 2, 5}`.  *Outputs:* over
  `10⁴` runs per instance, the frequency of an error larger than `ε/2` and the histogram of the number
  of evaluations.  *Validation:* error frequency `≤ δe^{|B(n,R)|/2ⁿ}` on every instance; at `g₀` the
  fraction of runs that stop after the samples equals `(1 − |V|/2ⁿ)^M` within sampling error.
  *Stopping:* one table.  *Resources:* minutes on one core.

## 9. What I did not check

* **Theory report statements** (Theorem 11.25, Lemma 11.43, Theorems 11.44, 11.45, 11.54, 11.58, at
  `5ed4072`): read as statements and used; not re-proved.  Harper's theorem: used through the theory
  report; the original was not opened.  My brute force (§2.4, A) checks the form used on `Q_3`, `Q_4`
  exhaustively and on samples of `Q_5`, `Q_6` — not for larger `n`.
* **The referee's R6** (`R3_REPORT.md`): I re-derived the excess identity and, in the generalised
  form R8.1, the algebra at `s = +1` and the overlap bound; the end `s = −1` and Corollary R6′ are not
  used by A16 and were only read.  The bounded-accuracy row of the table (d) (A12(c)) was not
  re-derived.
* **Remark (1) of Lemma A16.5** (general reference): read only.  **Remark (2)** ("hills never help"):
  only numerically.
* **The coordinator's scripts:** `energy_isoperimetry_check.py` and `terrace_twin_explore.py` were read
  (after my own numerics) and their logs read; **not re-run**.  `plateau_twin_check.py` was run as a
  byte-identical copy inside my directory only to confirm the abort.  The "400 random members" of
  A16.1 and the "1 398 random members" of A16.5 were not replicated as such (mine are different
  members).
* **No randomised algorithm was simulated**: for A16.6 (ii) and R8.4 I computed brackets and
  probabilities; I did not run the procedures.  R8.4's constants are not optimised.
* **Conjecture:** the families F2–F5 are exponential-scale formulas of my own, not validated by exact
  sums (F1-type landscapes were: `r8_11`); grids of `240²` with two zooms — an effect below `10⁻³` in
  the rate would be missed.  The column bound is a heuristic in a limit model.  Landscapes with
  exponentially many prepared sites at several levels, and lower bounds not based on one visible
  instance, were not examined.
* **Non-adaptive:** the bracket was evaluated on radial instances only, `n ≤ 400`, with `η` on a grid
  of 400 values plus a local refinement (a coarser minimum only widens the bracket); R8.6's `O(ln n)`
  terms are sketched, not written out; a displaced inner cone was checked for membership only.
* **Not examined at all:** the plateau twin with the marginal oracle (codes), a field, a tolerance
  on the datum, the physical reading [H] at the end of A16.
* **Prior art:** abstracts (through a fetch tool) and search snippets only; no paper was read in
  full; one fetch failed.  "Not found" is not a claim of novelty.
* **Precision:** everything except A16.2 (`mpmath`, 40 digits) is in double precision; differences
  of mean energies were always taken through the excess identity.  The Lean file covers the
  algebraic core of A16.5 only — not Harper's step, not the existence of the level, not A16.6.
* **My own slips** (in `NOTES.md`): one notes section was written to the repository root by a
  relative path and was moved back; the estimate "2 minutes" for `r8_06` part 2 was wrong (29
  minutes); a first validity test in `r8_05` rejected the reference configuration; a first mutation
  in `r8_03` did not fire.  None affects a result reported here.
