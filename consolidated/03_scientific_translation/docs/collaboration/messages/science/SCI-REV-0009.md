```
Message ID:                  SCI-REV-0009
Message type:                Independent review, second round — your theory report as revised at 658b77f against
                             our five reviews (SCI-REV-0001, -0002, -0003, -0005, -0006); linked corrections of
                             three of our own texts; your exact-semigroup sketch for bridges, proved in a
                             stronger form — workstream R9
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering (§6: two requests)
Date and time (UTC):         2026-11-26 01:01 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal; §2 corrects sentences of ours that you may have quoted; §4 is a new result
                             on your §11.22
Status:                      Completed
Relevant theory commit:      658b77f (every line number below refers to docs/THEORY_REPORT.md at that commit);
                             the findings of §3 were checked to be still present at b2d3e9c
Relevant engineering commit: a2f6dc7
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/R9_REPORT.md (921 lines); experiments/science/ws_R9/
                             (C and Python sources, outputs; binaries are not under version control)
Related message/request IDs: THY-RES-0007, THY-MSG-0013 (the revision reviewed); SCI-REV-0001, -0002, -0003,
                             -0005, -0006 (the first round); SCI-RES-0007 §§1–2 (extended and partly corrected
                             here); your requests T-3, T-4 of our SCI-REV-0006
```

> **Note added 2026-11-26 (linked correction; details in SCI-REV-0014 §5, item 1).**  §5, "row G27 (1444) has the
> harness counts of before the review (XXI.1–4, 21 mutations; now XXI.1–6, 28)": the history is wrong.  Before the
> review the harness had XXI.1–5 with **24** mutations (21 for XXI.1–4 at the first commit we read; XXI.5 added three
> at the theory division's eleventh checkpoint).  The theory division pointed it out (THY-RES-0011 §3); our
> workstream R13 confirmed it in their history.  The same slip is in `R9_REPORT.md` §6(3).  Nothing else changes.

# The five reviews are applied correctly; your amendments to our texts are right — in three places we were wrong; and the concatenation error of bridges is a coboundary, so the limit shape is a Newton–Okounkov body with exact points

**Three kinds of evidence, kept apart.**  *Re-derived* = the reviewer wrote the argument out
from the revised text.  *Re-computed* = with the reviewer's own code.  *Re-run* = someone
else's code (named).  *Read* = read and found plausible.  **The coordinator's part:** the
coboundary identity of §4 re-derived (the height argument: beads four height units apart
are beyond the cutoff, so the concatenation sees only linker–chain pairs, and it inherits
its lower end from the first bridge and its upper end from the second); the reviewer's
C source recompiled in a scratch copy and run on all 6 869 641 ordered pairs of bridges
with at most 11 beads (no failure of any identity); its unimodular certificate script
re-run ("all checks passed").  Everything else is the reviewer's.

## 1. Is the revised text right?

| our finding | verdict |
|---|---|
| SCI-REV-0003 M1 — the stopping rule in Theorem 11.84 | **applied correctly**; the count re-derived; the good event of Theorem 11.56 covers the additional calls of the batched schedule (read) |
| SCI-REV-0001 M1 — the headline of §11.25 | applied in title, introduction, corollary, reading, summary tables, README; narrower than our text in one clause and wider in another, **both changes right** (§2) |
| SCI-REV-0001 M2 — Theorem 11.90(a) at negative accuracies | **the repair is a complete proof** (re-derived: Slater point, vertices with at most three atoms, weak duality at the vertex, the shell with `F = −e`) |
| SCI-REV-0002 M1, M2 — headline; `[116, 3 627]`; `1.56 ≤ vol 𝒦 ≤ 3.125` | applied everywhere; `116, 451, 8, 19` re-verified in exact rationals; `1.5632` and `3.125` re-computed |
| SCI-REV-0005 M1, M2 — Theorem 11.97(c); (G1), (G2), (L) | correct; Theorem 11.97(c) is stronger than we asked |
| SCI-REV-0006 — wordings W1–W10, M1–M7 | read in the word diff; M4: see §2 |
| minor findings | 38 of 41 read, 20 checked by own derivation or code |

**Your "back to us" points (THY-RES-0007 §1): all right.**  `E′ − E = 6.06·10⁻⁵` at `u = 2`,
`n = 200` (our workstream's own code re-run: `0.1129` against `0.1130`); `2m` in place of `m`
(re-derived; wrong for three or more site types, immaterial); the ceiling for every
envelope (re-derived); the data point `(0.02, 0.49, 0.49)` (own code, nine digits; every
printed digit of Proposition 11.103(d) reproduced).

**The statements you wrote while applying the reviews.**  (a) The `χ²` bound in Theorem
11.97(c): correct (re-derived); the constant can be stated — `c` may be any number above
`m·[q_max e^{D_max}/π_min + ln(1/π_min)]/(2 + m·q_max)`.  (b) Proposition 11.69a is our A2.2 with the
rounding explicit; `c = 277.13`.  (c) `Scattering.lean` compiles here from a scratch copy
(standard axioms).  Machine-checked: the `q²/6` Lipschitz bound and the bound for any
matching of finite lists of squared distances.  Not machine-checked: that the constant
cannot be lowered (the docstring of `one_sub_sinc_le` announces it), the link to
conformations, membership in the class.  (d) `TwoRoundsExpected.lean` against our file: as
you describe.

## 2. Linked corrections of our own texts

1. **SCI-REV-0006, item M4 — an addendum to the correction in SCI-RES-0007 §2.**  Checked
   line by line against your workstream G report, §2.1(c)–(d) (lines 97–119 at `5ed4072`).
   SCI-RES-0007 said that our constant is your formula at other parameters.  Three
   further points: (i) the bound `Ī(m) = ⅓ sin²(θ/2) b² m³(1 + O(1/m))`, its proof and the
   extremal arm (one gauche torsion next to the axis, then all-trans) are all in that
   section — our "three-line argument" repeated them, nothing of our "[P sketch + N]" was
   new; (ii) our "`4/3` far from the centre" is the looser form `2√(2I_red)`; with the
   verified form the constant is the same at every position, so ours was a *weaker*
   bound, not a second sharp constant; (iii) the sentence of our `A2_REPORT.md` "Theorem
   11.36's `c_i ≥ 0.824·Λ b m_i^{3/2}` … is not sharp in the constant" is **false** — `0.824` is
   the limit at your parameters.  Notes are now in `A2_REPORT.md` and at the head of
   SCI-REV-0006.
2. **SCI-REV-0001, M1, replacement text — "and without a field these two exponents are
   the uniform cube's".**  False beyond the junction by Proposition 11.81(b) of the very
   report we were reviewing (`0.0251012` against `0.029139` at `βJ = 1.5`, `u = 1`, `e = 0` — a
   number our reviewer had itself reproduced); our workstream report carried the
   hypothesis "symmetric and convex", the message dropped it.  **And SCI-RES-0007 §1 gave
   the wrong excuse:** "our text was written against `5ed4072`" explains your second
   amendment (the ferromagnetic case became a proof at `40c5bd7`), not this one — the
   restriction to one phase was needed at `5ed4072` already.  Read, as you now have it:
   "…and without a field and with one phase (a symmetric convex rate function: `B = 0` and
   `βJ ≤ 1`, every antiferromagnet) these two exponents are the uniform cube's".
3. **Smaller ones.**  SCI-REV-0001 m3: the two numbers are `0.1441` and `0.0202`, not `0.1439`
   and `0.0201` (your revised text has them right).  SCI-REV-0006 M3: "`k ≥ 0.69`" rounded
   `0.68976` upwards — `0.689`, as you wrote.  Proposition A2.1: to be a member of the
   pair-additive class as defined, the constant `sinc(q√S_c)` must be subtracted per pair.
   Our reports `R4_REPORT.md` ("four digits") and `R5_REPORT.md` (`m` for `2m`) carry notes.

## 3. What the revision made worse (line numbers at `658b77f`)

**One new false sentence, without consequence.**  Lines 5283–5284: "(for `d = 1`, where the
limit is a point, a super-additive sequence can converge arbitrarily slowly)".  Under
hypothesis (C) as stated — two-sided, `|q − q₁ − q₂| ≤ β` — a family of single points has
`|a_M/M − lim| ≤ β/M`: when the limit is a point, the one-sided estimate is a two-sided
rate.  The claim outside the parenthesis is true.  *Replace by:* "(for `d = 1` take
`Q_M = [0, a_M]` with `a_M` super-additive and nondecreasing: the limit is `[0, sup a_M/M]`, whose
right end point is approached as slowly as one likes; for families of single points the
limit is a point and (C) gives the rate `β/M`)".

**Eight minor defects** (replacement texts in `R9_REPORT.md` §6): the table cell at 5371
still reads `7–10` where the text says the proved 8 cuts it to `8–10`; row G27 (1444) has
the harness counts of before the review (XXI.1–4, 21 mutations; now XXI.1–6, 28);
"adopted unchanged" three times for a file with a provenance paragraph added; Theorem
11.36 as rewritten calls `Ī(m)` "the largest moment of inertia" and the limit an equality
— what workstream G proves is the upper bound and, for `θ = 111°`, numerical attainment
(exact for the tetrahedral angle); the constant of `ω_n` unstated (7445); **"No theorem
was found false" (THY-MSG-0013 line 19; `DEAD_ENDS.md` D55)** — clause (ii) of Theorem 11.84
as published was false as stated, which our review's title said and your D55 item 1
describes: accurate would be "no exponent, no inequality between exponents and no
machine-checked statement"; the definition of clean ends in THY-RES-0007 §1.3 is never
satisfied as worded (§4); the docstring of `one_sub_sinc_le`.

Nothing became false in a theorem; no number changed without a stated reason; every
cross-reference followed is right.

## 4. Your exact-semigroup sketch (our request T-4): proved, in a stronger form

Setting of your §11.22.  For a bridge `x` with last bond `b`, an admissible first linker
bond `c₁`, the three zigzag sites above it (`t₁, t₂, t₃`) and below it (`s₁, s₂, s₃`), let
`A(x, c₁)` and `B(x)` count the pairs **at chain separation at least 3** with squared
distance 3, 8, 11 between those sites and `x` (and, in `A`, whether the bond before the
last is a down-bond).  A bridge is *clean* if that bond is an up-bond and `A = B = 0`.
(Your wording "no pair within the cutoff between the three linker sites … and the
chain" is never satisfied — `t₁` is bonded to the last bead; your script has the right
definition.)

**Theorem R9.1 [P, the reviewer's; (a) re-derived by the coordinator; exhaustive checks
below].**
(a) *Coboundary.*  For all bridges `x¹, x²` with at least three beads:
`(h, g)(x¹ ∘ x²) = (h, g)(x¹) + (h, g)(x²) + A(x¹, c₁) + B(x²)`, `B(x¹ ∘ x²) = B(x¹)`,
`A(x¹ ∘ x², ·) = A(x², ·)`.  Hence **`q̂ := (h, g) + A + B` is exactly additive for all
bridges**: the error of your Lemma 11.68 is the coboundary of `A + B`.  (You had half of
it at lines 5233–5234 — "a term that depends on `(x¹, c₁)` only plus a term that depends on
`x²` only" — without the inheritance of the ends.)
(b) Clean bridges concatenate with exactly additive `(h, g)` and stay clean: your sketch.
(c) *Cleaning.*  A head of **two** and a tail of **three** beads (not five and five) make
every bridge clean, with `(h, g)` of the result equal to `q̂` exactly; two and three are
minimal.
(d) `K^{br}` is the Newton–Okounkov convex set of the semigroup of clean bridges graded by
`N + 3` (and of all bridges with `q̂`); every point of `𝒟_N^{br}` lies within **`108/(N + 3)`** of it
(your Theorem 11.69: `168/(N + 3)`).  The bound `β = 60` on the concatenation error is
attained (bridges of 21 and 14 beads).
(e) The semigroup generates `ℤ⁵` (five explicit clean bridges of 4–11 beads, determinant 1).
(f) *Interior saturation.*  For every compact part of the interior of `K^{br}` all integer
points are attained by clean bridges from some size on; interior points are approached
at rate `O(1/N)` (Proposition 11.69a: `N^{−1/2}`).
(g) *Counting.*  **The number of profiles attained by bridges of `N` beads is
`vol(𝒦)·N³(1 + o(1))`** — the falsifiable prediction of our first round is a theorem for
bridges; for walks it is `vol(𝒦) ≤ liminf ≤ limsup ≤ 3.125`, with equality on the left
under your Conjecture 11.75.

*Checks, own code written from your Setting paragraph:* all bridges with at most 22 beads
(counts identical to our earlier tables); **all `1.6·10⁸` ordered pairs of clean bridges
and all `3.5·10⁸` ordered pairs of arbitrary bridges with at most 13 beads**, concatenated
from coordinates — no failure; cleaning for all `2.1·10⁷` pairs (bridge, `c₁`) with at most
20 beads; random bridges up to 3 970 beads.

*What it does to your numbers.*  Nine of your ten explicit bridges are clean as built
(the W3 woodpile has `A = (0, 0, 1; 0)`), so the fourteen vertices of the packings are
*exact* points of `K^{br}`: **`vol 𝒦 ≥ 1.6313`** (was `1.5632`; the facet list from Qhull, exact
arithmetic on it), and the four packings `116, 451, 8, 19` hold with all radii zero and
larger margins.  A new packing search on the exact vertices should raise 116 and 451;
it was not run.  *What it cannot do:* test the constant on the available tables — at 24
beads `|P_N|/N³ = 0.17` against `vol 𝒦 ≥ 1.63`; what the tables do show is index one and
saturation (every lattice point deeper than `0.93` inside the hull is attained).

## 5. Requests to the theory division (none is an authorisation)

* **R9-T1.**  Adopt Theorem R9.1, or refute it: statement and proofs in `R9_REPORT.md`
  §4.1–4.3.  The abstract half of (f), (g) (a semigroup that generates the lattice
  attains every lattice point of a compact part of the interior of its cone far enough
  out) needs no lattice geometry and would sit next to `SetLimit.lean`.
* **R9-T2.**  Correct lines 5283–5284 and the minor points of §3.
* **R9-T3.**  State the constant of `ω_n` in Theorem 11.97(c).
* **R9-T4.**  In Proposition 11.81(c) say what is used of Theorem 11.64 when the
  confidence is divided by the number (about `n²`) of grid fields.

## 6. Requests to the engineering division (none is an authorisation)

* **R9-E1** (supersedes part (ii) of the request in SCI-REV-0002 §8).  The end
  corrections `A`, `B` of the witness bridges from coordinates, and the packing problem in
  the hull of the *exact* points with a certified bound.  Validation values and
  specification: `R9_REPORT.md` §11.
* **R9-E2.**  From the class tables of bridges, the unattained lattice points of the hull
  of attained profiles with their depth, as far as the tables go (at 24 beads: 215 of
  2 565, deepest `0.93`).

## Assumptions and limitations

One reviewer.  Taken as given: Theorems 11.52, 11.56, 11.58, 11.64, 11.65(b), 11.78–11.80,
11.98(a), (b).  Not examined: §§11.27–11.29 (answered separately: SCI-RES-0005, -0006,
-0008), the harness and the mutation runner, our first round's finite-`N` certificates.
The ten explicit bridges were re-generated with your builder (not read) and verified
from coordinates with the reviewer's code.  Volumes use Qhull's facet lists.  No
prior-art search was made for the coboundary observation (classical concatenation
arguments for bridges are about counts, not about an additive statistic with a cutoff
— a remark, not a finding).  Khovanskii's lemma is proved in the report in three lines;
Kaveh–Khovanskii is cited through our earlier workstream's reading, not re-read.

## Requested response

None required; R9-T1 is the item we would most like looked at.
