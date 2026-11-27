# R9 addendum — Proposition 11.69b of the theory report (theory commit `24a3c27`) against Theorem R9.1

Reviewer of workstream R9, 26 November 2026.  A bounded follow-up to `R9_REPORT.md` (§4, Theorem
R9.1).  Object, all read in full from the read-only export of `24a3c27`: `docs/THEORY_REPORT.md`
lines 5590–5648 (Proposition 11.69b) with the passages that lean on it (5555–5588, 6044–6056,
9407–9410, row G24); `THY-RES-0009.md` §2; `t4_head_tail.py`, `t4_lattice_index.py` and their
outputs; harness test XVIII.7 (the 70 lines of the test, its result line, its five mutations).

Who found what.  The observation — bridges with clean ends concatenate exactly — is the theory
division's (THY-RES-0007 §1.3 and `t4_semigroup.py` at `658b77f`); R9 was asked to prove or break
it and proved it as Theorem R9.1.  Proposition 11.69b was written without that theorem, and R9.1
without their proof.  So 11.69b(a), (b) and R9.1(b), (c) are **two independent proofs of the same
two statements (up to the length of the head), and they agree.**

Reading levels used below: **re-derived** (by me, on paper); **own code** (`r9_lat.py`,
`r9_semi.c`, `r9_cobound.c` — written by me, the first from the Setting paragraph of §11.22 and
the statement of Lemma 11.68); **their code re-run** (their scripts, unchanged); **read**.
Labels `[P]`, `[N]`, `[K]` as in `COMMON.md`.

## Verdict table

| # | question | verdict | basis |
|---|---|---|---|
| 1 | their "clean" against mine | **The same set.**  Counts for 3–10 beads from my enumerator: `1, 2, 4, 10, 24, 64, 159, 420` with the first two bonds fixed, `4, 8, 16, 40, 96, 256, 636, 1680` without — theirs, all eight. | re-derived (§1); own code and their membership test side by side on all 24 484 bridges with 3–12 beads: no disagreement |
| 2 | exact additivity, 11.69b(a) | **Correct; no counterexample.**  It is R9.1(b), the case `A = B = 0` of the coboundary identity R9.1(a). | re-derived; own code, real concatenations: all 176 400 ordered pairs with at most 8 beads (this follow-up, their normalisation), all 160 326 244 with at most 13 beads (first round) |
| 3 | "head and tail of three beads", 11.69b(b); constants | **True, not minimal, and its constant is not sharp.**  Head 2 + tail 3 always suffices and neither number can be lowered; the change of `(h, g)` is *exactly* `A + B`, of norm at most `60` (attained), not only at most `168`.  Their side remark that two beads at either end suffice "(not proved)" holds up to 11 beads and **fails from 12 beads on**.  Rates: they keep `168/(N+3)` one-sided, R9.1(d) has `108/(N+3)`; in the interior both give `1/M`, with constants of different kinds (§3.3). | re-derived; own code (§3) |
| 4 | the lattice is `ℤ⁵`, from clean bridges with at most 10 beads | **Correct, and 10 is the least such number** (rank 4 up to 9 beads). | own enumeration and row reduction; two `5×5` minors with gcd 1; five vectors with determinant 1 (§4) |
| 5 | what each has; anything false or overstated | **Nothing in Proposition 11.69b is false.**  It says *less* than is true in three places, one remark invites a false generalisation, and the sentence just before it (lines 5556–5558) is still the false parenthesis C1 of `R9_REPORT.md`.  Theirs has an elementary interior estimate valid for every `M`; R9.1 has the coboundary for all bridges, `108/(N+3)`, the sharp cleaning, the saturation proved without the citation, a rate with a universal constant, the counting statement and `vol 𝒦 ≥ 1.6313` (§5). | re-derived; read |
| 6 | the two scripts | **Both do what the text says**; my re-runs reproduce their published outputs byte for byte (§6). | their code re-run |

No correction of `R9_REPORT.md` is owed.  One constant of mine can be improved (not an error):
in R9.1(f) the `7.5` may be `5` (§3.3).

---

## 1. "Clean": the same set **[P, re-derived; N]**

Theirs: (i) the bond before the last is an up-bond; (ii) the linker of Lemma 11.68 above `x` has
no pair within the cutoff with `x` beyond its chain neighbours; (iii) the same for the zigzag that
continues the first two bonds backwards.  Mine (`R9_REPORT.md` §4.1): `b′` up, `A(x, b′) = 0`,
`B(x) = 0`, where `A`, `B` count the pairs at chain separation at least 3 and squared distance
3, 8, 11 between `x` and `t₁, t₂, t₃` above, `s₁, s₂, s₃` below.  The sites are the same sites.
"Beyond its chain neighbours" and "at chain separation at least 3" select the same pairs once (i)
holds: the pairs at separation 1 and 2 are at squared distances 3 and 8 and are not counted by
the profile, and the three pairs at separation exactly 3 across the junction lie across the
torsions `(b′, b, c₁)`, `(b, c₁, b)`, `(c₁, b, c₁)` with `c₁ = b′`, all trans, squared distance 19.  (The
wording of THY-RES-0007, which no bridge satisfied if read literally — `R9_REPORT.md` §4.1 — is
repaired in the report.)  Their second implementation defines clean by "a three-bead bridge
concatenated above, or below, changes `(h, g)` by nothing"; that is the same set by the first
line of R9.1(a) with `x²`, respectively `x¹`, the rod.

Numbers (`out/r9b_check.txt` part A; first two rows `r9_semi.c`, first round):

| beads | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|
| bridges, first two bonds fixed (mine) | 1 | 2 | 5 | 12 | 29 | 78 | 201 | 536 | 1 433 | 3 824 |
| clean among them (mine) | 1 | 2 | 4 | 10 | 24 | 64 | 159 | 420 | 1 115 | 2 938 |
| bridges from the origin, bonds not fixed (mine) | 4 | 8 | 20 | 48 | 116 | 312 | 804 | 2 144 | 5 732 | 15 296 |
| with (i) | 4 | 8 | 16 | 40 | 96 | 264 | 688 | 1 832 | 4 944 | 13 192 |
| clean: my test = their `in_S` = rod test | 4 | 8 | 16 | 40 | 96 | 256 | 636 | 1 680 | 4 460 | 11 752 |
| clean, published by them | 4 | 8 | 16 | 40 | 96 | 256 | 636 | 1 680 | — | — |
| (i) holds, (ii) fails | 0 | 0 | 0 | 0 | 0 | 0 | 16 | 88 | 248 | 768 |
| (i) holds, (iii) fails | 0 | 0 | 0 | 0 | 0 | 8 | 40 | 88 | 288 | 736 |

The three tests — mine; their `in_S`, their code evaluated on my enumeration; the rod test
written with my code — agree on every one of the 24 484 bridges.  Their sentence "up to 7 beads
a bridge is clean iff (i) holds, from 8 beads on (ii) or (iii) can fail (8 of the 264 …)" is
right; more precisely (iii) fails from 8 beads on and (ii) from 9.  "(both implementations)":
their published outputs show the eight counts for one implementation and the totals 508 and 420
for 3–8 beads for the other; a driver of mine on their harness helpers gives the same eight
numbers, and 4 460 of 5 732 at 11 beads (`r9b_harness_counts.py`, their code).

## 2. Exact additivity: correct **[P, re-derived; N exhaustive]**

Their proof is right in every step: the error of Lemma 11.68 is (pairs linker–`x¹`) +
(pairs linker–`φ(x²)`) + `[b′` down`]`; the linker above the concatenation is the `φ`-image of the
linker above `x²` and lies at least 4 height units above the first linker and `x¹`; the one
below sees `x¹` only.  The same three sentences, read without assuming clean ends, are the
identities of R9.1(a) — error `= A(x¹, c₁) + B(x²)`, `B(x¹ ∘ x²) = B(x¹)`, `A(x¹ ∘ x², φ(c)) = A(x², c)` —
which hold for **all** bridges; their own text states the first one in the remark after
Lemma 11.68 (lines 5506–5510) and does not draw the consequence (§5.2).  `0 ∈ 𝒮_M` for `M ≥ 6`:
right, the zigzag.

Own code, real concatenations built from coordinates:

* all 176 400 ordered pairs of the 420 clean bridges with 3–8 beads, first two bonds not fixed
  (their normalisation): self-avoiding bridge with `N₁ + N₂ + 3` beads, `(h, g)` exactly additive,
  clean — no failure (`out/r9b_check.txt` B1);
* first round: all 160 326 244 ordered pairs of the 12 662 clean bridges with at most 13 beads
  (first two bonds fixed, which loses nothing: the construction maps `x²` by a symmetry and is
  equivariant in `x¹`) — no failure (`out/semi_pairs13_part{0,1}.txt`);
* control (B2): all 298 704 ordered pairs of arbitrary (bridge, `c₁`) and bridge with at most 8
  beads: the error equals `A(x¹, c₁) + B(x²)` in every case.  It vanishes for all pairs of clean
  bridges, and also for 640 of the 14 784 pairs in which *neither* bridge is clean (`8 × 80`: the
  eight 8-bead bridges with `A = 0 ≠ B` above any of the 80 bridges with `B = 0 ≠ A`).  So the
  last clause of the harness text XVIII.7, "for bridges that are not clean the concatenation
  error does not vanish", is true for some pairs, not for every pair — their own run reports
  182 of 200.  The proposition does not contain that clause.

## 3. Head and tail; constants

### 3.1 The statement (b) **[P, re-derived]**

True.  The tail of three beads is the linker `t₁, t₂, t₃`; the bond before the last of the
extended bridge is `b`, an up-bond; the sites above it are `t₄, t₅, t₆` of the same zigzag, at
least 4 height units above `x`; likewise below.  Against R9.1(c):

* **Head 2 + tail 3 suffices and is minimal [P; N].**  The third head bead `s₃` never has a
  pair with `x` (only `x₀` is within three height units of it, and that pair is trans), so their
  3 + 3 is my 2 + 3 with one inert bead: `Γ̂_M ⊂ 𝒮_{M+6}` where R9.1(c) has `Γ̂_M ⊂ Γ_{M+5}` (their `𝒮_M`
  is the level `M` of my `Γ`).  A head of
  two always works because the first bead of a bridge is *strictly* lowest; a tail of two does
  not always work because the last bead is highest but need not be the only bead at its height.
* **Their side remark.**  "A head and a tail of *two* beads already suffice for every bridge
  with at most 10 beads (not proved); of one bead they do not."  True as scoped, and true at 11
  beads; **false from 12 beads on**, so it cannot be proved: head 2 + tail 2 fails for 4 of the
  4 350 pairs (bridge, `c₁`) with 12 beads and the first two bonds fixed (16 of 17 400 in their
  normalisation, counted directly), 32 of 11 738 at 13, 92 570 of 13 527 394 at 20 (`r9_semi.c`,
  first round; the counts at 11 and 12 beads re-computed with `r9_lat.py`).  Example (`out/r9b_check.txt` part C):
  `x = (0,0,0), (1,1,1), (0,2,2), (1,3,3), (2,2,4), (3,3,5), (4,2,6), (5,1,5), (6,2,4), (5,3,3), (4,2,2), (3,3,1)`,
  `c₁ = (−1,1,1)`: after head 2 + tail 2 the first site above, `t₃ = (0,6,2)`, is at squared
  distance 11 from bead 3 of `x`, `(1,3,3)`, which is at the top height.  A head of one bead
  fails from 8 beads on.

| not clean after head `k_h` + tail `k_t` | 1+1 | 1+2 | 1+3 | 2+1 | 3+1 | 2+2 | 3+2 | 2+3 | 3+3 |
|---|---|---|---|---|---|---|---|---|---|
| 3–10 beads, 3 964 pairs (bridge, `c₁`), bonds not fixed | 132 | 80 | 80 | 56 | 56 | 0 | 0 | 0 | 0 |
| 11 beads, 1 630 pairs, first two bonds fixed | 71 | 36 | 36 | 36 | 36 | 0 | 0 | 0 | 0 |
| 12 beads, 4 350 pairs, first two bonds fixed | 197 | 104 | 100 | 100 | 100 | 4 | 4 | 0 | 0 |

(First row: theirs for `1+1`, `2+2`, `3+3` — 3 832, 3 964, 3 964 of 3 964 clean — reproduced.)

### 3.2 The cost **[P; N]**

"…and change `(h, g)` by a vector of norm at most `6β′ = 168`": true and far from sharp.  Head
and tail are at least 4 height units apart, the new torsions are trans except `(b′, b, c₁)`, so
the change is **exactly `A(x, c₁) + B(x)`** — the two end terms of the error of Lemma 11.68 — and
the cleaned bridge has `(h, g) = q̂(x, c₁)`.  Hence the change lies in `[0,1]×[0,9]×[0,14]×[0,1]`
and has norm at most `β = 60`; their own text already has the two halves (`44` for a tail of three
beads at lines 5546–5548, `(0, 3, 4)` for the lower term at line 5510).  `60` is attained: for the
38-bead bridge `z` = (the 14-bead bridge with `B = (0,3,4)`) ∘ (the 21-bead bridge with
`A = (1,6,10;1)`) the change is `(1, 9, 14; 1)`, counted by the `O(n²)` definition, with head 3 +
tail 3 and with head 2 + tail 3 (part C; by R9.1(a) the concatenation inherits `B` from below
and `A` from above).  Up to 10 beads the largest change is `(0, 2, 6; 1)`, norm 15, as they print.

### 3.3 Rate constants **[P, re-derived]**

| quantity | theory report at `24a3c27` | Theorem R9.1 |
|---|---|---|
| every point of `𝒟_N^{br}` lies within … of `K^{br}` | `168/(N+3)` (Theorem 11.69, unchanged; 11.69b states no one-sided rate) | `108/(N+3)` (d) |
| cost of making a bridge clean; level shift | at most `168`; `+6` | exactly `A + B`, at most `60` (attained); `+5` |
| interior point `p`: `dist(p, 𝒟_{M−3}^{br})` | `6(m(p)+1)R/M + O(1/M) = [216(m(p)+1) + 108]/M` | `(7.5 + 108)/M` |
| … valid for | every `M ≥ 6` (see below) | `M ≥ M₀` (compact set), not effective |
| … constant | depends on `p`; at least `216·14 + 108 = 3 132` | universal: `115.5` (`113`, see below) |

* **One-sided.**  The difference between 3 + 3 and 2 + 3 is immaterial for every rate.  What
  11.69b gives for an arbitrary bridge, through (b), is the exact point of the cleaned bridge
  at level `N + 9`: `dist ≤ (9R + 168)/(N+9) = 492/(N+9)`, or `9R/(N+9) = 324/(N+9)` with the exact cost
  and its sign — neither better than the `168/(N+3)` they keep.  `108/(N+3) = 3R/(N+3)` needs the
  exact point `q̂(x, c₁)/(N+3)` of the bridge itself, that is, additivity of `q̂` on all bridges.
* **Interior, theirs.**  The estimate is right: with `T = ⌊(M−6)/m⌋`, `|k_i m/M − λ_i| ≤ m/M + λ_i(M − mT)/M`,
  and the sum over five points is below `6(m+1)/M`.  It says less than its proof gives: it
  holds for **every** `M ≥ 6` (for `M < m + 6` the point is `0` and the bound exceeds `R`), so no
  `M₀(p)` is needed; and five points with `p` inside their simplex serve a neighbourhood of `p`,
  so the bound is uniform on compact subsets of the interior with `m = m(C)`.  The constant is large:
  **`m(p) ≥ 13` for every interior point** — clean bridges with at most 9 beads have `h₃ = 0`
  (**[N]**, part D), an interior point has `p₃ > 0`, so one of the five points of `𝒮_m` has
  `h₃ ≥ 1`, and a clean bridge with a nearest-neighbour contact has at least 10 beads: `m − 3 ≥ 10`.
* **Interior, mine.**  R9.1(f) gets the rate from saturation: for `M ≥ M₀(A)` the integer point
  nearest to `Mp` is attained.  The constant is universal, the threshold is not effective.
  Rounding in the coordinates `(h₃, h₃+h₈, h₃+h₈+h₁₁, g)`, in which the norm is `5|a| + 3|b| + |c| + |g|`,
  gives `5` where I wrote `7.5` (rounding `(h₃, h₈, h₁₁, g)`): `(5 + 108)/(N+3)`.
* The two are complementary: theirs is explicit from the first `M` as soon as five clean
  bridges of one level around `p` are in hand; mine has the constant that is right in the limit.
  What §12 (a4) of the theory report calls open, "an effective `m(p)`", is by R9.1(f) the
  question of an effective threshold `M₀(A)`.

## 4. The lattice **[N, exact integer arithmetic; own code]**

Own enumeration (first two bonds fixed), own row reduction (`out/r9b_check.txt` part D):

| at most … beads | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|
| distinct `(h₃, h₈, h₁₁, g; N+3)` of clean bridges | 1 | 3 | 6 | 10 | 16 | 28 | 45 | 82 | 146 | 255 |
| rank | 1 | 2 | 2 | 2 | 3 | 4 | 4 | 5 | 5 | 5 |
| index in `ℤ⁵` | — | — | — | — | — | — | — | 1 | 1 | 1 |

The first nine columns are their `out_t4_lattice_index.txt` exactly.  Their claim holds, and 10
beads is the least bound: up to 9 beads all clean bridges have `h₃ = 0`.  Independent of any row
reduction: two `5×5` minors of the 82 vectors are `4` and `15` (gcd 1), and the five clean classes
`(0,0,6,6; 13)`, `(1,4,6,5; 13)`, `(0,3,6,4; 11)`, `(0,1,6,5; 13)`, `(0,2,7,6; 13)` — bridges with 10, 10,
8, 10, 10 beads — have determinant `1` (my fraction-free elimination and sympy).  With such a
five-vector certificate the label of the lattice claim can be `[P]`; `out/certificate.txt` of
the first round gives five bridges with coordinates (4, 5, 9, 9, 11 beads).

## 5. What each statement has; what is false or overstated

### 5.1 In Proposition 11.69b and not in Theorem R9.1

1. **An elementary interior estimate valid for every `M ≥ 6`**, explicit in the level `m` of
   five clean points around `p` — no lattice computation, no Khovanskii lemma.  R9.1(f) has no
   bound with an explicit threshold.
2. The zero element at every level `M ≥ 6` (the zigzag) stated as part of (a) and used in place
   of the extension property (E); in R9.1 the rod appears only among the checks.
3. A test in the harness with five mutations, all reported caught (read, not run), and a
   second implementation of the lattice.

### 5.2 In Theorem R9.1 and not in Proposition 11.69b

1. **The coboundary for all bridges** (a): `q̂ = (h, g) + A + B` is exactly additive on *all*
   bridges, so the family need not be restricted at all — `Γ̂ ⊃ Γ`, with `|q̂ − (h, g)| ≤ 60`.  Their
   closing sentence in *Prior art* (lines 6054–6056), "the abstract theorem with an error term
   is needed only for the statement about all bridges at a given length", can go further: for
   that statement too an exact semigroup is available.
2. **Exact points for every bridge and `108/(N+3)`** (d), where the report keeps `168/(N+3)`.
3. **The sharp cleaning** (c): head 2 + tail 3, minimal; cost exactly `A + B`; `A ≤ (1,6,10;1)`,
   `B ≤ (0,3,4)`, both attained.
4. **Saturation proved** (f), self-contained through Khovanskii's lemma — in the report it is
   **[K]** "read by the Scientific Discovery Division, not by us" (and not by me: by A2) — and
   stated also for profiles alone (`ℤ³`, interior of `𝒦`).
5. **A rate with a universal constant**, uniform on compact subsets of the interior (§3.3).
6. **The counting statement** (g): `|P_N^{br}|/N³ → vol₃(𝒦)`, `|H_N^{br}|/N⁴ → vol₄(K^{br})`; for all walks
   `vol(𝒦) ≤ liminf |P_N|/N³ ≤ limsup ≤ 3.125`.  The report has no counting statement.
7. **Numbers**: `vol 𝒦 ≥ 1.6313` on exact vertices (the report has `1.56`, line 5843); R2's four
   packings hold with all radii zero.
8. **Size of the verification**: every ordered pair up to 13 beads (`1.6·10⁸` clean, `3.5·10⁸`
   arbitrary), cleaning for all 21 220 319 pairs (bridge, `c₁`) up to 20 beads; theirs: 20 000
   random pairs, 1 056 pairs in the harness, cleaning up to 10 beads.

### 5.3 False, or more than is proved, or less

Nothing critical or major.  In the order of the text:

| where | what | class | replacement |
|---|---|---|---|
| lines 5556–5558 (before the proposition, unchanged since `658b77f`) | "(for `d = 1`, where the limit is a point, a super-additive sequence can converge arbitrarily slowly)" — **false as stated**: when the limit is a point, (C) gives the two-sided rate `β/M` | C1 of `R9_REPORT.md` §6 (critical by its rule, no consequence) | "(for `d = 1` take `Q_M = [0, a_M]` with `a_M` super-additive and nondecreasing: the limit is the interval `[0, sup a_M/M]`, whose right end point is approached as slowly as one likes; for families of single points the limit is a point and (C) gives the rate `β/M`)" |
| (b), lines 5603–5605 | "norm at most `6β′ = 168`" — true; the change is exactly `A + B`, at most `60` | minor (weaker than true) | "A zigzag head of two beads and a zigzag tail of three turn every bridge into a clean one; `(h, g)` changes by exactly the two end terms of the error of Lemma 11.68, a vector in `[0,1]×[0,9]×[0,14]×[0,1]` of norm at most `β = 60` (attained); a head of one bead or a tail of two can fail." |
| (c), lines 5610–5612; §12 (a4); THY-RES-0009 §2 | "there are `m(p)` and `M₀(p)` … for all `M ≥ M₀(p)`", "constant that depends on the point" — true; the proof gives every `M ≥ 6` and local uniformity; `m(p) ≥ 13` | minor (weaker than proved) | "… `≤ 6(m + 1)R/M` for every `M ≥ 6`, with one `m` for a neighbourhood of `p`" |
| *Numbers*, lines 5643–5645 | "A head and a tail of *two* beads already suffice for every bridge with at most 10 beads (not proved)" — true as scoped; **the general statement it points to is false** | minor | "A head and a tail of two beads suffice for every bridge with at most 11 beads, but not in general: from 12 beads on a tail of two can fail (16 of the 17 400 pairs (bridge, `c₁`) with 12 beads); a head of two always suffices, a head of one does not (from 8 beads on)." |
| lattice claim, lines 5616–5618 | **[N]** — an exact finite computation; can be **[P]** with five explicit bridges | remark | — |
| harness XVIII.7, last clause of the text | "for bridges that are not clean the concatenation error does not vanish" — not for every pair (§2) | minor (harness text only) | "… and for some pairs of bridges that are not clean the concatenation error does not vanish" |
| `limit_shape_review/README.md`, row `t4_head_tail.py` | "two (observed) always give a clean bridge" — on bridges with 3–10 beads, as the row says | remark | add "(not beyond: fails from 12 beads on)" |

Everything else I checked in the proposition is right as written: (a); (b); "`K^{br}` is the
closure of `∪_M 𝒮_M/M`" (needs `𝒮_M/M ⊂ K^{br}`, which follows from multiples, and (b)); the estimate
of (c); the saturation statement given the cited theorem (and without it, by R9.1(f)); the
counts; "What it does not give".

## 6. The two scripts

* **`t4_head_tail.py` does what the text says**: for `k = 1, …, 4` it puts a zigzag head and a
  zigzag tail of `k` beads each on every bridge with 3–10 beads (their enumerator, all four
  choices of the first two bonds) and every admissible `c₁`, asserts a self-avoiding bridge, and
  tests membership with the same function as `t4_semigroup.py`; re-run by me, its output is
  identical to the published one (`3 832`, then three times `3 964`, of `3 964`).  Two limits, both
  visible in the code: it tries equal lengths only, and stops at 10 beads — so it can find
  neither that the head may be shorter than the tail nor that a tail of two fails (12 beads);
  "largest change" is a componentwise maximum over the results that are clean, not a norm.
* **`t4_lattice_index.py` does what the text says**: it executes the harness as a module to use
  its lattice helpers, defines clean by (i) and the rod test, collects `(h, g; N+3)` up to 11
  beads and row-reduces over the integers; re-run by me, its output is identical to the
  published one, and equal to my independent computation in the number of distinct vectors,
  the rank and the index at every size.

---

## How to re-run

From `experiments/science/ws_R9/` (Python 3 with sympy; nothing outside the directory is
written; the path of the export is at the top of each script or its first argument):

| command | what | whose code | time | output |
|---|---|---|---|---|
| `python3 r9b_check.py > out/r9b_check.txt` | parts A–E: definition, exactness, heads and tails, lattice, constants; needs `r9_lat.py` and `out/extremal_raw.txt` | mine; part A also calls their `in_S` on my enumeration | 1.5 min | `out/r9b_check.txt` |
| `sh r9b_rerun_theirs.sh` | their two scripts unchanged from the export, working directory here, bytecode off; `cmp` with their outputs | theirs | 10 s | `out/r9b_rerun_t4_head_tail.txt`, `out/r9b_rerun_t4_lattice_index.txt`, `out/r9b_rerun_compare.txt` |
| `python3 -B r9b_harness_counts.py > out/r9b_harness_counts.txt` | per-size counts of clean bridges with their harness helpers and their function `clean` | theirs, my driver | 5 s | `out/r9b_harness_counts.txt` |
| first round, cited: `bin/r9_semi 22 0 20 out`; `bin/r9_semi 13 13 0 out 0 2`, `… 1 2`; `bin/r9_cobound 13 0 2`, `… 1 2` | enumeration and cleaning up to 20 beads; all pairs up to 13 beads | mine | see `R9_REPORT.md` §7 | `out/semi_enum22.txt`, `out/semi_pairs13_part*.txt`, `out/cobound13_part*.txt` |

Every log named here comes from a run that reached its last line with exit status 0.  The steps
are in `experiments/science/ws_R9/NOTES.md` ("Follow-up").  No linear programme, no floating-
point comparison: integer arithmetic throughout.  Housekeeping: the snapshot commit `f5df52b`
captured four files `out/tmp_r9b/rerun_*` of a first trial of the same two re-runs (complete,
byte-identical to `out/r9b_rerun_*.txt`); I deleted them from the working tree, so `git status`
shows them as deleted — they are superseded.

## What I did not check

* **Kaveh–Khovanskii, Theorem 1.6**: not read by me, in either round (A2 read it).  The claim
  of 11.69b(c) that rests on it is proved independently in R9.1(f); the citation itself I
  cannot vouch for.
* **The harness**: I read test XVIII.7 (lines 6792–6861), its result line and the five mutation
  entries.  I did not read the helpers `ls_enum`, `ls_concat`, `ls_profile` nor the other 10 000
  lines that `t4_lattice_index.py` executes on import, and I did not run the harness or the
  mutation runner; that the helpers are right I infer from the agreement of their outputs with
  my computation.  Whether the two implementations of the theory division are independent of
  each other I did not examine.
* **The rest of commit `24a3c27`** (third-order and share certificates, `HilbertBall.lean`,
  §11.30, the other sections of THY-RES-0009): outside this follow-up, not read.
* **Sizes.**  The exhaustive pair checks stop at 13 beads, the exhaustive cleaning at 20; beyond
  that there are the proofs and the random long bridges of the first round.  I did not look for
  the shortest bridge whose cleaning costs 60 (38 beads is an example), nor for the least `m(p)`
  (13 is a lower bound, not shown to be attained), nor for a bound on `M₀(A)`.
* **Nothing here is machine-checked**: Proposition 11.69b is `[P]` on their side, Theorem R9.1
  `[P]` on ours; the agreement of two independent paper proofs and of three programs is what
  there is.

---

## Coordinator's note (2026-11-26, before publication as SCI-REV-0011)

1. **Read in full by the coordinator at `24a3c27`:** Proposition 11.69b with its proof and its *Numbers* (theory
   report lines 5590–5648), the paragraph before it (5553–5560), Lemma 11.68 and the proof of Theorem 11.69
   (5473–5552).  The quotations of §5.3 above are as printed there.
2. **The 12-bead example of §3.1, from its coordinates, with a few lines of arithmetic that share nothing with
   `r9_lat.py`:** the twelve points form a self-avoiding walk on the diamond lattice (each step is one of the
   four bond vectors of its sublattice), the first bead is strictly lowest, the last is at the top height
   together with beads 3, 5 and 9; `b = (−1,1,−1)` is an up-bond, the bond before is a down-bond; with `c₁ = (−1,1,1)`
   and a tail of two beads the first linker site `(0,6,2)` is at squared distance 11 from bead 3; with a tail of
   three no pair between linker and bridge at chain separation `≥ 3` is within the cutoff; with the other
   up-bond `c₁ = (1,1,−1)` a tail of two is already enough.  (The head was not examined: it is below the bridge
   and cannot remove a pair above it.)
3. **The determinant of the five classes of §4** is `1` (exact rational elimination).
4. **`r9b_check.py` re-run** from a scratch copy holding only that script, `r9_lat.py` and
   `out/extremal_raw.txt` (89 s, exit 0, empty error stream): the output is identical to
   `out/r9b_check.txt` except for three timing lines.
5. **Not done by the coordinator:** re-running their two scripts or the harness driver; re-deriving the
   equivalence of the two definitions of clean, the minimality of head 2 + tail 3, or the bound `m(p) ≥ 13`;
   reading the harness test.

---

## Coordinator's correction note (2026-11-26; SCI-REV-0014 §5)

"The first round gives five bridges with coordinates (4, 5, 9, 9, 11 beads)": the output
file `ws_R9/out/certificate.txt` names those five and prints coordinates of four others;
the coordinates of the five are in the script `ws_R9/r9_certificate.py`.
