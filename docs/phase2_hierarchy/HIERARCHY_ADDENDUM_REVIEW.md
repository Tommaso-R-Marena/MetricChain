# Review of `HIERARCHY_ADDENDUM.md` (hidden partitions: Theorem P, Theorem H6)

*Adversarial referee report, written 2026-11-28 by an AI session that did not write the addendum, following
`HIERARCHY_ADDENDUM_review_brief.md`.  Nothing here has been read by a human expert.  Scripts and outputs:
`experiments/phase2_hierarchy/review_addendum/` (own code; nothing imported from the author's scripts).
No file outside that directory and this report was written; nothing was committed.*

---

## 0. Verdict

| claim | verdict | basis |
|---|---|---|
| **Theorem P** (§A2) | **Correct as stated; I could not break it.**  Every line of the proof checks. | algebra, line by line (§1); own re-evaluation of every intermediate claim on 12 000 instances; direct maximisation; own brute-force extremal profiles under the theorem's exact hypotheses, about 420 cases (§2) |
| **Theorem H6** (§A4) | **Correct, given the archive's lower bound.**  Every step of the proof checks. | reading and algebra (§3); steps (S), (U), (B), (1), (2) and step (e) carried out literally at finite `n` with exact binomials |
| Corollary H7, H8, Remark 1 of §A4 | Follow from H6 and the quoted archive results. | reading; arithmetic of the "large `n`" conditions |
| Remark 4 of §A2 (sharpness) | **False as stated** (does not affect any theorem). | proof and computation (§1.4) |
| §A3, second bullet (brute force) | Numbers reproduced, but it **tests a weaker statement than Theorem P**. | own solver reproduces 8 printed numbers to 2 decimals; comparison (§2.4) |

Findings: **0 CRITICAL, 0 MAJOR, 12 MINOR** (§5).  What was not checked: §6.

---

## 1. Theorem P — the proof, line by line

Notation as in §A1.  "A" = verified by algebra (by hand, reproduced below where not obvious), "C" = verified by
computation (`p1_chain.py`, output `out/p1_chain.txt`), "R" = by reading.

### 1.1 Facts (C1)–(C4)

| fact | status | how |
|---|---|---|
| `cost_𝒢 = r − r∘avg_𝒢 = Σ φ_c KL(z_c ‖ mean)` | true | A: `Σ_{c∈g} φ_c[z_c ln q + (1−z_c) ln(1−q)] = φ_g[q ln q + (1−q) ln(1−q)]` at `q` = cell mean |
| (C1) chain rule, `cost_{𝒢′} ≤ cost_𝒢`, `r(avg z) ≤ r(z)` | true | A (`avg_𝒢 avg_{𝒢′} = avg_𝒢` for a refinement); C: defect `≤ 3·10⁻¹⁵` on 8 000 random nested partitions incl. entries `0`, `1` |
| (C2) | true, **never used** in §A2 or §A4 | A; C |
| (C3) `χ ≥ 0`, `χ(p_u) = 0`, `χ(κ) = h`, monotone on `[0,p_u]`, `[p_u,½]`, symmetric, `p_u < κ < ½`, step identity | true | A: `χ′ = ln(t/(1−t)) + u` on `[0,½]`; `f(p_u) + u p_u = ln 2 − ln(1+e^u) + u = Λ₁`; `χ(0) = ln(1+e^{−u})` is finite, so the boundary values are harmless.  C: 11 slopes `0.01…40`, defect `≤ 1.1·10⁻¹⁴` |
| (C4) `λ ↦ T_g(max(z, λ))` nonincreasing (and the mirror statement) | true | A: `T_g = min_q Σ φ_c KL(z_c‖q)`; for `λ < λ′ ≤ μ(λ)` the moved classes approach `μ(λ)` from below, `KL(·‖q)` is decreasing on `[0,q]`; `μ(λ) − λ` is nonincreasing, so local monotonicity to the right holds at every `λ < max z_c`, and a continuous function with that property is nonincreasing.  Nothing in the argument refers to `½`, so cells with classes on both sides of `½` are covered.  C: 8 000 random cells of 2–8 classes, weights down to `10⁻⁶`, more than 40 levels each: largest increase `9·10⁻¹⁵` |

### 1.2 Steps 1–5

| step | claim | status | how |
|---|---|---|---|
| 1 | `Φ` continuous, `Φ(0) ≥ T(y) > θ` | true | R (`r` is continuous on `[0,1]^C`; `e(0) = y`) |
| 1 | `Φ(1) = cost₁(clip_κ y) ≤ r ≤ h ≤ θ` | true | A (`m(1) ∈ 𝒦` by convexity, so `m′ = m`, and (C1)).  This is the **only** place where `θ ≥ h` is used (see §1.4) |
| 1 | an `s` with `Φ(s) = θ` exists | true | intermediate value theorem; C: bisection residual `≤ 2·10⁻¹² h` |
| 1 | the levels `λ_g ≤ κ` (resp. `≥ 1−κ`) exist | true | A (mean of `max(e,λ)` is continuous, nondecreasing, `= m_g` for small `λ`, `≥ κ` at `λ = κ`); C |
| 1 | `avg₂ e′ = m′` | true | A; C (`≤ 7·10⁻¹³ h`) |
| 1 | `‖e − e′‖ = ‖m − m′‖` | true | A (inside a cell all classes move in one direction, so the weighted `ℓ¹` move equals `φ_g` times the move of the mean); C |
| 1 | `T(e′) ≤ T(e)` | true | (C4) cell by cell, from `λ = 0` (where `max(e,λ) = e`) to `λ_g`; C: largest value of `T(e′) − T(e)` is `+3·10⁻¹³ h` (rounding) |
| 2 | `cost₁(e′) = T(e′) + Q(m′) ≤ θ` | true | A: (C1) at `e′` and `avg₂ e′ = m′`; `m′` is constant on cells of `𝒢₂`, so `Q(m′) = cost₁(m′)`; C |
| 2 | (H2) is applied at `e′` with `cost₁(e′) ≤ θ`; (H1) at `m′ ∈ 𝒦`; `ν_𝒦` at `p = avg₁ m′ ∈ 𝒦` | each hypothesis is used exactly where it is assumed | R; C (`m′, p ∈ 𝒦` to `5·10⁻¹³`) |
| 3 | the chain and its bookkeeping, `r(e) − r(m) = T(e)`, `r(m′) − r(p) = Q(m′)` | true | A; C (identity to `7·10⁻¹³ h`) |
| 4 | clipped classes pay `φ_c[χ(ℓ) − χ(y_c)] ≤ φ_c c_ℓ`, `0 ≤ c_ℓ ≤ h` | true | A: for `ℓ ≥ p_u` use `χ ≥ 0` and `ℓ ≤ κ`; for `ℓ < p_u`, `y_c < ℓ < p_u` and `χ` is nonincreasing there; the upper side by symmetry |
| 4 | central cell: `A_g ≤ μ_g c_ℓ ≤ φ_g h` | true | A |
| 4 | deep cell (`m_g < κ`): `ℓ ≤ m_g < κ`, price `φ_g[h − χ(m_g)]`, `c_ℓ ≤ χ(m_g)`, hence `A_g ≤ φ_g h`; mirror case | true | A (`m_g ≥ ℓ` because all classes of `e` are `≥ ℓ`; monotonicity of `χ` on `[p_u, ½]`, or `c_ℓ = 0`).  A cell with classes on both sides of `½` falls under one of the three cases according to its mean; nothing else is needed.  C: `max_g (A_g − φ_g h) ≤ 3·10⁻¹³ h` |
| 5 | `Π₁ + Π₂ ≤ h` and the conclusion | true | C: on 12 000 random hidden instances `B := r(p) − r(y) + u‖y − e′‖ − (h − θ) ≤ −2.0·10⁻⁴ h` |

The 12 000 instances of part A of `p1_chain.py` were drawn from structures the author did not try (three
classes in one cell; a cell split into three by `𝒢₂`; weights down to `10⁻⁶`; slopes `0.1 … 10`; types with
entries `0`, `1`, `p_u`, `κ`, cells straddling `½`, deep cells).  Direct maximisation of `B` over `y`
(Nelder–Mead, 8 structures × 2 slopes × 2 budgets) gives `sup B = 0` up to `3·10⁻¹⁵ h`, attained, never exceeded.

**I found no gap in the proof.**  It is short because (C4) and the choice of `s` do all the work; both are sound.

### 1.3 Consistency with the known lower bounds (attempts to derive a contradiction)

* *One round (`a`).*  A full cone around a hidden centre violates (H1): the type `(κ, 1−κ) ∈ 𝒦` has a different
  value from the diagonal type with the same mean.  The theorem is silent, as it must be.
* *Hinted lower bound (`h`).*  With one cell and `θ = h` the plain dip of radius `κ` is admissible and attains the
  bound (`0`).  So the theorem cannot be used to go below `e^{nh}`; equality, no contradiction.
* *Two rounds (`c_2 > h`).*  A two-round algorithm would need the conclusion for `{cost₁ > θ}` from (H1) alone.
  Taking `𝒢₂ = 𝒢₁` in Theorem P does not give this: (H2) then says that the second batch saw nothing finer than
  `𝒢₁` on `{cost₁ ≤ θ}`, which fails for the twins of Theorem 11.86 (the second batch sees the rim of the dip).
  Skipping round 1 (`𝒢₁ = {C}`) needs `F` to be a function of `|x|` on `𝒦`, which the flat histogram of the twins
  violates.  Numerically (§2.3, control iv) the two-round analogue has hidden gain `≈ 0` up to `Θ ≈ 1.3 nh` at
  `u = 2` — the archive's `θ₂*/h = 1.33` — while under the hypotheses of Theorem P the gain follows `nh − Θ`.
* *Below `h`.*  The inequality of the theorem in fact holds for every `θ ≥ 0` (§1.4).  This does not contradict
  the lower bound `h`: for `θ < h` the bound `ν_𝒦 + h − θ` exceeds `ν_𝒦`, and a blind batch of `e^{nθ}` points
  cannot establish (H1) on `𝒦`.

I could not derive a contradiction with any known bound.

### 1.4 Two facts the addendum does not state, and one remark that is wrong

**(a) The hypothesis `θ ≥ h` is superfluous for the stated inequality.**  If `Φ(1) ≤ θ` the proof applies
verbatim.  If `Φ(1) > θ`, take `s = 1`: `e = clip_κ(y) ∈ 𝒦`, so by (H1) alone `F(e) = F(avg₁ e)`, and

    −F(y) − r(y) ≤ ν_𝒦 + [r(e) − r(y) + u‖y − e‖] − [r(e) − r(avg₁ e)] ≤ ν_𝒦 + h − cost₁(e) < ν_𝒦 + h − θ,

because `Π₁ ≤ h` and `cost₁(e) = Φ(1) > θ`.  Checked on 4 000 random instances with `θ ∈ (0.05h, h)` (part L:
largest value of bound `− (h − θ)` is `−5·10⁻³ h`) and by brute force (`Θ = 0.7nh`, excess `≤ 0`, §2.3).

**(b) Remark 4 of §A2 is wrong as stated** ("So `h` cannot be lowered").  For `θ < h` the plain dip has radius
`f^{−1}(θ) > κ`; its cone contains the type `(κ, 1−κ) ∈ 𝒦`, so it violates (H1) and is not an instance of the
theorem.  By (a) no instance violates the inequality below `h`.  What the example shows is something else: if
(H1) is known only on what a blind batch of `e^{nθ}` points sees (`{r ≤ θ}`, the version the author's script
states and tests), then `θ ≥ h` is needed.  My solver reproduces the dip there quantitatively: excess per
coordinate `+0.0400` (`n = 960`) against `D(θ) − (h − θ) = +0.0398` at `u = 2`, and `+0.1324` against `+0.1293`
at `u = 4` (`out/p2b_controls2.txt`).  The threshold `h` enters Theorem P through the definition of `𝒦`, not
through `θ ≥ h`.

**(c) The bound is attained for `θ > h` too** (the last sentence of Remark 4 is true of "this example" only).
One cell, two classes with weights `(w, 1−w)`.  Let `−G(μ) := f(μ)` on `[κ, 1−κ]`, continued with slope `u`
outside, and let `U := −F` be the largest `u`-Lipschitz function equal to `−G(mean)` on `{cost ≤ θ}` (McShane
extension; `−G∘mean` is `u`-Lipschitz because `|f′| < u` on `[κ, 1−κ]`).  Then (H1), (H2) hold, `ν_𝒦 = 0`, and
for hidden `y` with mean `p_u` and `cost(y) ↓ θ`:  `U(y) − r(y) → h + u(κ − p_u) − f(p_u) − θ = h − θ`.  Such
types exist for `θ` up to `8.1h` (`u = 1`, `w = ½`) and `1.98h` (`u = 2`, `w = ¼`), not for `u = 4`.  Brute
force agrees: for two classes in proportion 1:3, `n = 1921`, `u = 2`, the hidden maximum is `−37.6` against the
bound `−37.4` at `Θ = 1.2nh` and `−93.6` against `−93.4` at `1.5nh`.  In these extremal profiles the *visible* mass exponent is
`ν_𝒦 + h` (at the diagonal type of mean `p_u`), so sharpness of Theorem P relative to `ν_𝒦` says nothing about
slack in H6.

---

## 2. Numerical falsification of Theorem P (own code)

### 2.1 Method

`p2_extremal.py`.  On the lattice of types of `n` coordinates in 2–5 classes I compute the pointwise largest
`U = −nF` with unit steps `≤ u`, `U ≤ R` on the lattice points of `𝒦`, equal values on lattice points of `𝒦`
with equal `𝒢₁`-cell counts, and equal values on lattice points of `{n·cost₁ ≤ Θ}` with equal `𝒢₂`-cell counts.
Every `F` satisfying the hypotheses of Theorem P restricts to such a function, so

    excess := max over lattice types with n·cost₂ > Θ of (U − R)  −  (nh − Θ)

is an upper bound for a violation: `≤ 0` confirms the theorem at these types, `O(u)` is inconclusive (lattice),
linear growth in `n` would refute it.  This is the exact optimum over *all* admissible `F` at once (difference
constraints), not a search.  The solver alternates an exact `ℓ¹` inf-convolution with group minima; it agrees
with scipy's Dijkstra on the explicit graph to `4·10⁻¹²` (5 lattices × 5 variants × 2 identification modes ×
2 slopes × 3 budgets, `out/p2_validate.txt`).

### 2.2 A lattice effect that had to be separated

The lattice core starts at `⌈κ n_c⌉`, the anchor of the proof sits at `κ n_c`.  Each class can cost up to
`(u − |f′(κ)|)·d_c` nats, `d_c = ⌈κ n_c⌉ − κ n_c`.  Four equal classes of size `N`, one cell split into two
pairs, `u = 2`, `Θ = nh` (`out/p2b_align.txt`; "outer" = smallest lattice box *containing* `𝒦`):

| `N` | 36 | 46 | 49 | 53 | 60 | 67 |
|---|---|---|---|---|---|---|
| `d` | 0.81 | 0.98 | 0.13 | 1.00 | 0.01 | 0.03 |
| excess (inner core), units of `u` | +1.44 | +1.87 | +0.53 | **+2.14** | +0.05 | +0.14 |
| excess (outer core), units of `u` | −0.78 | −0.14 | −1.88 | −0.02 | −2.32 | −2.19 |

The excess follows `d`, not `n`; the predicted maximum `4·1.071·d` nats is `2.13u` at `N = 53`.  All later runs
use "aligned" sizes (`d_c` small).

### 2.3 Results under the theorem's exact hypotheses

*Scaling* (`out/p2b_scaleA1–3.txt`; 166 cases with hidden types; `u ∈ {2, 4}`, `Θ/nh ∈ {1, 1.2, 1.5}`).
Excess in units of `u` along increasing `n`:

| structure | `u` | `n` | `Θ = nh` | `Θ = 1.2nh` | `Θ = 1.5nh` |
|---|---|---|---|---|---|
| two classes 1:3, one cell | 2 | 240, 480, 957, 1921 | −0.13, −0.27, −0.04, −0.05 | −0.23, −0.27, −0.13, −0.12 | −0.22, −0.22, −0.08, −0.06 |
| three classes 1:2:3 in one cell | 2 | 123, 243, 483 | +0.16, +0.20, +0.25 | +0.08, +0.10, +0.13 | −0.00, +0.01, +0.10 |
| same | 4 | 123, 242, 474 | +0.17, +0.14, −0.00 | −1.36, −3.95, −7.33 | −4.15, −7.62, −15.83 |
| one cell → `{0},{1},{2,3}` (split into three) | 2 | 56, 112, 196, 240 | +0.08, +0.25, +0.53, +0.05 | −0.31, −0.66, −1.57, −1.62 | −0.63, −1.02, −2.71, −4.11 |
| same | 4 | 68, 140, 188, 260 | +0.25, +0.30, +0.27, +0.12 | −0.94, −2.17, −2.48, −2.77 | nothing hidden |
| one cell → two pairs | 4 | 68, 140, 188, 260 | +0.25, +0.30, +0.27, +0.12 | −0.94, −2.03, −2.48, −3.77 | −1.72, −4.52, −6.11, −8.10 |
| four classes in one cell, never split | 2 | 56, 112, 196 | +0.08, +0.25, +0.53 | −0.01, −0.01, +0.21 | −0.42, −0.06, +0.14 |
| three hidden classes left after split | 2 | 56, 112, 196 | +0.08, +0.25, +0.53 | −0.31, −0.27, −0.26 | −0.56, −0.34, −0.82 |
| nested `{0,1},{2,3}` → `{0,1},{2},{3}` | 4 | 68, 140, 188 | +0.25, +0.30, +0.27 | −0.94, −2.17, −2.48 | nothing hidden |
| five classes → `{0,1},{2,3},{4}` | 2 | 35, 70, 105, 140 | +0.23, +0.31, +0.20, −0.29 | +0.57, −0.15, −0.78, −1.14 | +0.08, −1.06, −1.25, −2.16 |
| same | 4 | 55, 85, 115, 145 | +0.53, −0.46, −0.45, −0.43 | −0.82, −1.56, −1.71, −2.69 | −1.38, −2.97, −4.10, −4.88 |
| 3 % class paired with a big one after split | 2 | 190, 388, 766 | −0.14, −0.20, −5.40 | −1.83, −1.49, nothing hidden | nothing hidden |

No excess grows with `n`.  The `+0.53` entries at `u = 2` belong to classes of size 49 (`d = 0.13`), the one at
`u = 4` to classes of size 11 (`d = 0.14`).

*Breadth* (`out/p2b_sweepA_hub.txt`): 13 structures (among them a class of weight 2–3 %, pairs of very unequal
classes, two cells hiding a pair each) × `u ∈ {1, 2, 4}` × `Θ/nh ∈ {1, 1.05, 1.2, 1.5, 2.5}`: 174 cases with
hidden types, largest excess `+0.75u` (`u = 1`, `n = 146`, where `nh` is only `4.3u`).  Identification by
exchange components instead of equal cell counts (the weaker reading; 48 cases, `out/p2b_sweepA_comp.txt`):
identical values.

*Controls* (`out/p2_controls.txt`, `out/p2b_controls2.txt`, `out/p2b_two.txt`) — the test can see violations:

* (i) below `h`, with (H1) only on `{r ≤ θ}`: the plain dip is found with the predicted size (§1.4 b);
* (iii) hypothesis (H2) dropped: hidden gain `+16…+21` nats at `u = 4`, `n = 48…144`, independent of `Θ`
  (excess `+4.1u … +6.9u`, growing);
* (iv) two rounds only (classes `A0, A1, B0, B1`, `φ_A = 0.64`, centre of `A` known, final batch on shells of
  `𝒢₁`): gain per coordinate at `u = 2`, `n = 200`: `+0.002, +0.0005, +0.0003, −0.001, −0.005, −0.016, −0.046`
  at `Θ/nh = 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.7` — zero up to about `1.3`, then linearly negative.  The archive
  gives `θ₂*/h = 1.33` at `u = 2`;
* (ii) hypothesis (H1) dropped: **no violation appeared** in the structure tried (one cell → two pairs,
  `n ≤ 144`), although the chain of the proof without the step `F(m′) = F(p)` overshoots by up to `0.57h`
  (part A of `p1_chain.py`).  So (H1) is needed by the proof; whether it is needed by the statement in that
  structure I did not determine.

**Largest excess found: `+2.14 u`** (4.28 nats; four classes of size 53, `u = 2`, `Θ = nh`), entirely the
core-rounding effect of §2.2 (predicted `2.13u`; `−0.02u` with the outer core).  With aligned sizes the largest
is `+0.75u` (`u = 1`) and `+0.57u` for `u ∈ {2, 4}` (`n = 35`).

*Resolution.*  `nh/u` is `0.029n`, `0.049n`, `0.060n` at `u = 1, 2, 4`.  A violation smaller than about one
lattice step would not be seen: that is 1 % of `nh` for two classes (`n = 1921`), 4–7 % for three (`n ≈ 480`),
6–10 % for four (`n ≈ 250`), about 12 % for five (`n = 145`).  Slopes `u < 1` cannot be resolved at these sizes.

### 2.4 The author's brute-force check tests a weaker statement

`h11_partition_chain_check.py B` uses the blind-visible set `{R ≤ Θ}` both for the normalisation and for (H1)
(its docstring states "Theorem P" in that form, with `ν₀ = sup_{V₀}`).  For `θ ≥ h` that statement follows from
Theorem P (`𝒦 ⊂ {r ≤ θ}`) and is strictly weaker.  My solver reproduces the printed numbers in that setting and
shows what the theorem as stated gives on the same lattices (`out/p2c_reproduce_author.txt`, excess in nats):

| case | author | mine, author's setting | mine, Theorem P as stated |
|---|---|---|---|
| `u=4`, `(40,40,40,40)`, one cell → pairs, `Θ = nh` (the "0.95u") | +3.80 | +3.80 | +3.80 |
| `u=2`, same | +1.38 | +1.38 | +2.28 |
| `u=1`, `(120,120)`, `Θ = nh` | +0.82 | +0.82 | +0.82 |
| `u=2`, `(60,180)`, `Θ = 1.2nh` | −4.58 | −4.58 | −0.45 |
| `u=2`, `(480,1440)`, `Θ = 1.2nh` | −38.80 | −38.80 | **+0.05** |
| `u=4`, `(60,80,100)`, split `{0},{1,2}`, `Θ = nh` | −3.06 | −3.06 | −0.89 |
| `u=2`, `(80,80,80)`, `{0,1},{2}`, `Θ = nh` | −3.97 | −3.97 | −2.91 |
| `u=1`, `(40,40,40,40)`, `Θ = 1.2nh` | +0.14 | +0.14 | +1.69 |

So the "linear decrease" of part B2 (`−4.6, −9.8, −19.5, −38.8`) is a margin of the weaker statement; under the
stated hypotheses the same instances sit on the bound (§1.4 c).  The theorem survives, but §A3 did not test it.

---

## 3. Theorem H6 — the algorithm and the proof

"C" refers to `p3_h6_steps.py` (outputs `out/p3_h6_SIQN.txt`, `out/p3_h6_E0–4.txt`).

| item | status | how |
|---|---|---|
| class `HP_m`, the two descriptions, the examples (`BR_m ⊂ HP_{2m}`, `r` centres `⊂ HP_{2^r}`) | true | R |
| coordinates of one class are never separated; "never separated for all `x`" ⇔ invariance under the transposition | true | A; C exhaustively on `Q_10` (300 random members of `HP_3`, 0 violations) |
| three rounds are three batches | true | R: the neighbours of pre-chosen points are not adaptive; `𝒢₁` depends on round 1 only, `𝒢₂` on rounds 1–2 |
| count `M(n+1) + (n+1)^m M(n+1) + (n+1)^{m²} M ≤ 3(n+1)^{m²+1} M` | true | A |
| `𝒢₁`, `𝒢₂` exist (`𝒞`, `𝒢₁ ∧ 𝒞`) | true | R |
| `E[Â | rounds 1, 2] = A` for **any** `𝒢₂` | true | A; C: shell identity on `Q_10` for arbitrary partitions, relative error `≤ 10⁻¹⁵` |
| (S), (U), (B) | true | A (`N·H(1/N) ≤ ln N + 1`; Chernoff with `δ = ½`); C: `N ≤ 800` all `a`; `N ≤ 10⁶`; grid of `(M, p)` |
| (1) | true | A; C: 6 000 random instances with exact binomials, class sizes down to 1; at most 39 % of the allowance `DL` is used |
| (2) | true | A (`ρ` applications of (U) per class, `ρ·|g|` per cell); C |
| (a) cost, Markov | true | A |
| (b) `E₁`, `E₂`, `E₃` | true | A: given its type a point is uniform among the points of that type; `i, i′` lie in different classes, so `P[x_i = x_{i′} = 0 | type] = (1 − k_c/n_c)(1 − k_{c′}/n_{c′}) ≥ n^{−2}`; `E₂` refers to `𝒞₁` only (a function of round 1) and `E₃` to `𝒞₂` (rounds 1–2), so conditioning on the earlier rounds is legitimate; union bounds `(n+1)^{m+2}`, `(n+1)^{m²+2}`, `(n+1)^D` |
| (c) (X1), (X2) | true, **no circularity** | A: `E₁`, `E₂` do not mention `𝒢₁`, `𝒢₂`; the identities are deterministic consequences for whatever partition was chosen afterwards.  The test point has `𝒞₁`-type `k⁻`, hence true type `κ(k) − e_{j′}` (its `𝒞₂`-type is irrelevant); `k⁻_c ≤ n_c − 1` and `k⁻_{c′} ≤ n_{c′} − 1` as claimed; the point and both neighbours were evaluated in the round in question; a cell of `𝒢₂` contains no pair separated in round 1 or 2 |
| (d) `Â ≥ A_vis/2` on `E₃`; `A_vis ≥ (n+1)^{−D} e^{ν₀}` | true | A (pigeonhole over the fine types of `κ*`; `P(k|b) ≥ P(k)`).  Not said: the set defining `ν₀` is nonempty for large `n` (`(n+1)^{−m} ≥ e^{−Θ+DL}`) |
| (e) `cost₂(ŷ) > θ_c ≥ h`, (4) | true | A; C |
| (e) rounding `E′`, `M″`, `P″` exists; distances `≤ 1`, `≤ ρ₀`, `≤ ρ₀` | true | A (`Σ⌊·⌋ ≤ B_g ≤ Σ⌈·⌉`; `|P″_c − n_c p_c| ≤ 1 + m²/2`); C |
| (e) path `E′ → M″`: `n cost₂ ≤ n cost₂(e′) + 4D(L+1)`, `n cost₁(k − e_{d′}) ≤ nθ_c + 8D(L+1) ≤ Θ − DL`, hypothesis of (X2) at every step | true | A (per-class convexity; use (2) with `z* = B_g/n_g` for `M″`, which gives `2D(L+1)`, and with the cell means for the `𝒢₁`-part); C |
| (e) path `M″ → P″`: hypothesis of (X1) at every step; `P(κ(P″)) ≥ e^{−Θ+DL}` | true | A; C |
| (e) assembling, constants `D(ρ₀+10)(L+1) + uD`, `(n+1)^{2D}` | true | A (`9 + ρ₀ + 1`); C |
| (f) | true | A |
| lower bound `c_r(HP_m) ≥ h` attributed to Theorem 11.25 | correctly attributed | R: `K_REPORT.md` quotes 11.25(a) as the zero function against dips on balls around a hidden point; these are functions of the distance to one centre, i.e. in `HP_2`; the exponent is `h` for every fixed accuracy, which covers the ratio `8/δ` of H6 |

*Step (e) literally.*  For `m = 2` (`n ≈ 20 000`, `60 000`) and `m = 3` (`n ≈ 110 000`), `u ∈ {1, 2, 4}`,
`η ∈ {0.1, 0.2}`, random true partitions, random `𝒢₁` cutting across them, random refinements `𝒢₂`, fine
classes of sizes down to 1: 44 hidden fine types; real-type construction, rounding, both exchange paths in
random monotone order.  At each of 221 355 + 18 326 exchanges between different true classes the hypothesis of
(X2) resp. (X1) was evaluated with exact binomial probabilities: it holds with margins `≥ 772` and `≥ 2038`
nats; every intermediate bound of the text holds; the final inequality holds with margin `≥ 1466` nats.  These
margins are large because the constants are generous; the test would catch a wrong direction or a wrong object
(e.g. the wrong type in (X2)), not a tight constant.

*"For large `n`".*  The smallest `n` for which all requirements of the proof hold (`u = 1`, `δ = 0.1`; the
binding one is always `A_hid ≤ A_vis`):

| | `η = 1` | `η = 0.1` | `η = 0.01` |
|---|---|---|---|
| `m = 2` | `2.5·10³` | `3.3·10⁴` | `4.0·10⁵` |
| `m = 3` | `1.3·10⁴` | `1.6·10⁵` | `1.9·10⁶` |
| `m = 4` | `4.5·10⁴` | `5.4·10⁵` | `6.4·10⁶` |
| `m = 6` | `2.9·10⁵` | `3.5·10⁶` | `4.0·10⁷` |

**I found no gap in the proof of H6.**  It is a careful finite-`n` version of the chain of §A2; the events are
defined so that the partitions can be chosen after the samples.

---

## 4. Corollaries, remarks, and the reported checks

* **Remark 1 of §A4** (`m⁵ log n = o(n)`): correct.  With `m = m(n)` the requirements are `(m²+1)L ≲ ηn/4`
  (cost), `9D(L+1) ≤ ηn/2`, `D(ρ₀+2)(L+1) + DL ≤ ηn/2` and `D(ρ₀+10)(L+1) + 2DL + uD ≤ ηn/2`; the last is
  of order `m⁵ ln n`.  Numerically the proof works up to `m = 7, 19, 46, 111` at `n = 10⁶, 10⁸, 10¹⁰, 10¹²`
  (`η = 1`), i.e. `m⁵ ln n ≈ 0.47 n`.  The sentence "uses `m` only through `D` and `ρ₀`" forgets the shell
  count `(n+1)^{m²}`; that requirement is weaker.
* **Corollary H7**: follows.  `c_1 ≥ a` from cones in `HP_2`; `c_2 > h` because `BR_2 ⊂ HP_4` as a set of
  functions and `U_REPORT.md` (Proposition U10 a) states the two-round bound for algorithms correct on `BR_2`
  ("its twins are members of `BR_2`"), for every `u` with a suitable split; `c_2 < a` from Corollary 11.87 on
  `L_u`; `c_r = h` from H6.  I read the archive statements, not their proofs.
* **Corollary H8**: a restatement of H6 plus Remark 1; nothing is claimed beyond them.  "At least like
  `(n/log n)^{1/5}`" is right up to the constant above.
* **§A5, "settled for bounded `m`"**: problems 1 and 2 of §8 of the report are as described and are covered by H6.
* **§A3, first bullet**: `out/h11_partition_chain_A.txt` says what the text says (largest defects `8·10⁻¹⁴ h`,
  bound `≤ −1.1·10⁻³ h`).  The random instances never come close to equality; equality exists (§1.2).
* **§A3, second bullet**: the 84 cases, the `0.95u`, "positive in all but one case at `0.7nh`", and the B2 row
  `+3.3, −2.0, −10.9, −28.2` are in the output; reproduced (§2.4).  The statement tested is the weaker one.
  `nh/u` lies between `4.7` and `14.4` in B1, so at `u = 1` (`nh ≈ 4.7…7` nats) the tolerance "`O(#classes·u)`"
  is as large as the quantity tested.  Two of the "seven information structures" have the same partitions
  (one cell → two pairs); none has a cell split into three or three classes left in a cell.
* **§A3, third bullet**: at `θ = 1.3h` the largest gains are `−0.371h`, `−0.484h`, `−0.715h` (`u = 1, 2, 4`), as
  stated.  "Shrink under refinement" is true of the `u = 1` rows quoted; the `u = 2` rows at `θ = h` do not
  shrink monotonically (`+0.062, +0.031, +0.037`; `+0.035, +0.021, +0.042`; `+0.028, +0.035, +0.018`).
* **§A3, fourth bullet**: `PartitionChain.lean` contains the four named theorems and no `sorry`; they are linear
  arithmetic with Step 4, (C1)–(C4) and the Lipschitz step as hypotheses, as the text says.  Not compiled by me.
* **§A6**: `out/h12_r3p_on_cubes.txt` says what the text says (18 settings, 0 failures, 17 detections,
  `|z| = 2.41` once, `|z| ≤ 2.02` for "learn nothing").  Seven of the "detections" have `|z|` between `10¹⁶` and
  `10³⁰¹`: a division by a vanishing standard error, not a z-score.  In every run the energy was constant on
  the shells of `𝒢₂`, so the test never meets a hidden type; the text admits that it tests the logic only.

---

## 5. Findings

**CRITICAL:** none.  **MAJOR:** none.

**MINOR**

1. *§A3 / table of §A0 — the brute-force evidence is for a weaker statement.*  The script uses `{r ≤ θ}`
   where the theorem has `𝒦`.  Under the theorem's hypotheses the excess reaches `+2.14u` on unaligned lattices
   (a rounding effect, §2.2), and the instances of B2 sit on the bound instead of falling linearly below it.
   Say so, or rerun with `𝒦` (done here: no violation).
2. *§A2, Remark 4 — wrong as stated* (§1.4 b, c).  Replace by: the inequality holds for all `θ ≥ 0`; the
   constant `h` in the bound is optimal and is attained for `θ ≥ h` (plain dip at `θ = h`; types with a cell
   mean `p_u` for larger `θ`); the threshold `θ ≥ h` is needed when (H1) is known only on `{r ≤ θ}`.
3. *Theorem P — `θ ≥ h` is not needed for the inequality* (§1.4 a).  Harmless; worth stating, because it shows
   that `h` enters through `𝒦`.
4. *(C2) is never used.*
5. *§A3, third bullet — selective quotation* (the `u = 2` values at `θ = h` do not shrink).
6. *§A3, second bullet — "seven information structures" are six*, and B1 has little power at `u = 1`.
7. *§A6 — the reported `|z|` of order `10²⁹⁹`* are artefacts; the test is degenerate (shell-constant energies).
8. *§A4 (d) — nonemptiness of the set defining `ν₀`* should be listed among the "large `n`" conditions.
9. *§A4, Remark 1 — "only through `D` and `ρ₀`"*: also through `(n+1)^{m²}` (weaker; the conclusion stands).
10. *§A4, Remark 4* is unclear ("the same amount in both directions along a class (a 2-periodic dependence)").
    If it means `F(k + e_j) = F(k + e_{j′})` throughout, it is a tautology; a profile that is 2-periodic in one
    class count and independent of the other *is* separated.
11. *Algorithm R3P — two silent idealisations*: choosing a partition without a separated pair inside a cell is
    a graph-colouring problem (free in the query model, not in time), and "separated" compares real numbers
    exactly.  Neither affects the theorem as stated.
12. *`h11_partition_chain_check.py`, docstring* states Theorem P in the `{r ≤ θ}` form and cites "report
    section 7.3"; it should match §A2.

---

## 6. What I believe, and what was not checked

* **Theorem P: I believe it.**  The proof is elementary and I verified each line by hand; every intermediate
  claim was re-evaluated by independent code; the exact extremal profiles under the stated hypotheses stay
  within lattice error of the bound in about 420 cases and do not grow with `n`.
* **Theorem H6: I believe it**, conditional on Theorem 11.25 of the archive for the lower bound.  The upper bound
  is self-contained and I verified each step by hand; step (e) was also executed literally.
* **H7, H8: I believe them** as corollaries, conditional on Theorems 11.44/11.45, 11.86 and Corollary 11.87.

Not checked: the proofs of the archive results (statements only, in `K_REPORT.md`, `U_REPORT.md`); the Lean file
was read, not compiled; Remark 2 of §A2 (Lemma B as a special case) and the sentence on Proposition G in §A5;
the internals of `h10_three_centres_finite_slope.py` and `h12_r3p_on_cubes.py` (outputs compared with the text
only); the author's scripts were not re-run; extremal profiles with exact binomial rates, with more than five
classes, or at slopes below 1; whether (H1) is necessary for the statement (only for the proof); runtimes of §A7.

## 7. Reproducibility

| script (in `experiments/phase2_hierarchy/review_addendum/`) | what | runtime | output (`out/`) |
|---|---|---|---|
| `p1_chain.py` | (C1)–(C4); Steps 1–5 on 12 000 instances; maximisation of `B`; `θ < h` | 2.5 min | `p1_chain.txt` |
| `p2_extremal.py validate`, `controls` | solver against Dijkstra; mutations of the hypotheses | 10 s | `p2_validate.txt`, `p2_controls.txt` |
| `p2b_runs.py align`, `controls2`, `two` | lattice effect of the core; plain dip below `h`; two-round control | 2 min, 1 s, 20 s | `p2b_align.txt`, `p2b_controls2.txt`, `p2b_two.txt` |
| `p2b_runs.py scaleA1`, `scaleA2`, `scaleA3` | scaling in `n`, aligned sizes | 55 s, 20 s, 70 s | `p2b_scaleA*.txt` |
| `p2b_runs.py sweepA hub`, `sweepA comp c3,c4,c6,c11,c12,c13 2,4` | breadth, two identification modes | 26 s, 15 s | `p2b_sweepA_*.txt` |
| inline call recorded in `out/p2c_reproduce_author.txt` | the author's printed numbers, both settings | 1 min | `p2c_reproduce_author.txt` |
| `p3_h6_steps.py SIQN`, `p3_h6_steps.py E i` (`i = 0…4`) | (S), (U), (B), (1), (2), `Q_10`, `n₀`; step (e) literally | 4 s; 2 min each | `p3_h6_SIQN.txt`, `p3_h6_E*.txt` |

## 8. Summary

1. **Theorem P:** correct as stated; no error found in the proof (verified line by line and by independent code).
2. **Theorem H6:** correct given the archive's lower bound (Theorem 11.25); no error found in the proof.
3. **Most serious finding:** no theorem is affected — §A3's brute-force check tests a weaker statement than
   Theorem P (`{r ≤ θ}` in place of `𝒦`), and Remark 4 of §A2 ("`h` cannot be lowered") is false as stated.
4. **Largest numerical excess:** `+2.14 u` (4.28 nats, four classes of size 53, `u = 2`, `Θ = nh`), fully
   accounted for by rounding of the core boundary; `+0.75 u` with aligned sizes; no growth with `n` up to
   `n = 1921 / 483 / 260 / 145` for 2 / 3 / 4 / 5 classes.
5. **Not checked:** proofs of the archive results, compilation of the Lean file, Remark 2 of §A2 and the
   Proposition G sentence, extremal profiles beyond five classes or below slope 1, the author's script internals.
