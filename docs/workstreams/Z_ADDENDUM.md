# Workstream Z, addendum — the envelope sequence: the assembly from the non-adaptive base, without a restart

*Coordinator, 2026-11-26 (written while `Z_REPORT.md` was with its referee, and kept in a file of
its own for that reason; to be merged into the report after the review).  Paper proofs,
**unrefereed**; the numerics are floating point on grids [N].  Notation and the quoted
statements are those of `Z_REPORT.md` §1 and of `R_REPORT.md` (`θ = θ_na` satisfying (H0), (H1) there;
`a = θ(0+)`, `h` the fixed point, `Σ` the slope map, `p_j` the orbit curves, `M_{W,b}`, `𝓔(W, b)`).*

## A0. What changes

`Z_REPORT.md` builds its schedule on the cut orbit curves of the rate proof, which have to be
restarted from a flat family at a height `h + ε₁` close to the fixed point (Lemma RC), so its
design needs a base of several epochs (Theorem A of workstream Q2 with `M₁` epochs — ten
epochs and 43 levels at `u = 1`) before the first of its own levels.  Nothing in Propositions
Z3, Z4 or in §6 of that report uses the cut curves: they use Proposition Z1(1), (2) only.
This addendum isolates what they use (*admissible sequences*, A1), shows that the **envelope
sequence** — the best convex sub-solution of the slope map — is admissible from the flat
family at the non-adaptive exponent `a`, with no restart and no range condition (A3), that
its top values decrease to `h` (A4) at the sharp rate `c_*²/j²` (A5), and that at the exponent
level they bound the level recursion from the first level on, `τ_j ≤ b_j` (A6).  Theorem Z then
holds for the schedule "envelope levels over the chain on the base bracket" (A7), which as
a formula improves on every earlier bound from `n ≈ 3·10⁴` on at `u = 1` (A8).  **At extensive
accuracies the same schedule gives `ln N(n; g·n, δ) ≤ n·θ_hint(g) + O((ln n)²)`** (A9), because at a
positive accuracy rate its exponent converges to the hinted one geometrically in the
number of levels.

## A1. Admissible sequences

Call a pair `(W, b)` a *family* if `b > 0` and `W : [0, b] → [0, 1]` is convex, nondecreasing and
continuous with `W(0) = 0`.  For a family put `b⁺(W, b) := sup{B ∈ [0, b] : Σ(B, W(B)) < ∞}`.

**Definition.**  A sequence of families `(W_j, b_j)_{j ≥ 0}` is *admissible* if for every `j`

    (S1)   b_j  ≥  b_{j+1}  ≥  b⁺(W_j, b_j),
    (S2)   W_{j+1}(B)  ≤  Σ(B, W_j(B))      for all B ∈ [0, b_{j+1}]        (the right side may be +∞).

**Lemma A1 [P; from the proof of Proposition U and Corollary U′ of `R_REPORT.md`].**  *For an
admissible sequence, every `j ≥ 0`, every `g > 0` and every `η > 0` there is `φ ∈ (0, 1)` with*
`max_{𝓔(W_j, b_j)} Ψ_g(φ; ·) ≤ M_{W_{j+1}, b_{j+1}}(g) + η`.  *Consequently Propositions Z3, Z4 and §6 of
`Z_REPORT.md` hold for every admissible sequence with `b₀ ≤ a` over every base family of flat type
`b₀` with least accuracy at most one; and at the exponent level, if `T ≤ M_{W_j, b_j}` for a
nonincreasing `T ≥ 0`, then `min(T, R[T]) ≤ M_{W_{j+1}, b_{j+1}}`.*
*Proof.*  As in Proposition Z1(2): `inf_{e>g} max_𝓔 Φ_g = max_𝓔 inf_{e>g} Φ_g ≤ sup{B − Σ(B, W_j(B))·g : B ≤ b_j, Σ(B, W_j(B)) < ∞}`;
every such `B` is at most `b⁺(W_j, b_j) ≤ b_{j+1}` by (S1), and `B − Σ(B, W_j(B))g ≤ B − W_{j+1}(B)g` by (S2).  The
exponent-level statement is Corollary U′ (whose hypothesis "`W′ ≤ Σ(·, W)` on `[0, b′]`" is used
in exactly this way; a top `b_{j+1}` above `b⁺` only weakens the conclusion).  ∎

*Examples.*  The cut orbit curves of `R_REPORT.md` §6 from `b₀ = h + ε₁` (Lemma T and the range
condition, Lemma RC) — the sequence of `Z_REPORT.md`.  The two sequences below.

**Lemma A2 (the step is monotone) [P].**  *Let `(W, b)`, `(V, c)` be families with `b ≤ c` and `W ≥ V` on
`[0, b]`.  Then `b⁺(W, b) ≤ b⁺(V, c)`, and `Σ(B, W(B)) ≥ Σ(B, V(B))` on `[0, b]`.*
*Proof.*  `Σ` is nondecreasing in its second argument ((Σ1) of `R_REPORT.md`).  If `B ≤ b` and
`Σ(B, W(B)) < ∞`, then `Σ(B, V(B)) < ∞` and `B ≤ c`.  ∎

## A2. The envelope step

For a family `(W, b)` let `b′ := b⁺(W, b)`, let `f(B) := min(1, Σ(B, W(B)))` on `[0, b′]` (`= 1` where `Σ = ∞`), let
`env f` be the lower convex envelope of `f` on `[0, b′]` (the largest convex function below `f`), and

    𝖤(W, b)  :=  (W′, b′),        W′ := env f on [0, b′),      W′(b′) := lim_{B↑b′} env f(B).

**Lemma A3 [P].**  *`b′ > 0`, and `𝖤(W, b)` is a family with `W′ ≤ Σ(·, W(·))` on `[0, b′]`.  If moreover
`W ≤ p_j` on `[0, min(b, h)]` for some `j`, then `b′ ≥ min(b, h)`.*
*Proof.*  `Σ(B, s) < ∞` whenever `B < (1 − s)a`, and `W(0) = 0`, `W` continuous: so `Σ(B, W(B)) < ∞` near `0` and
`b′ > 0`.  `f` is nondecreasing (`Σ` is nondecreasing in both arguments, `W` in `B`), `0 ≤ f ≤ 1`, and
`f(0) = min(1, Σ(0, 0)) = 0` (`Σ(0, 0) = sup_e (−θ(e)/e) = 0`).  So `0 ≤ env f ≤ f`, `env f(0) = 0`; a convex
function that is nonnegative and vanishes at the left end of its interval is nondecreasing;
it is continuous on `(0, b′)`, and at `0` because `0 ≤ env f(B) ≤ (B/B₁)·env f(B₁) → 0`; the left limit at
`b′` exists, is at most `env f(b′) ≤ f(b′)`, and lowering the value of a convex function at an end
point to its limit keeps it convex.  For the last claim: for `B ≤ min(b, h)`,
`W(B) ≤ p_j(B) ≤ p_j(h) ≤ L < 1 − h/a ≤ 1 − B/a` ((P2) of `R_REPORT.md`), so `(B, W(B))` is regular.  ∎

**Corollary A4 (comparison) [P].**  *Let `(V_j, c_j)_{j≥0}` be admissible, and let `(W_j, b_j)_{j≥0}` be an
envelope sequence, `(W_{j+1}, b_{j+1}) = 𝖤(W_j, b_j)`, with `b₀ ≤ c₀` and `W₀ ≥ V₀` on `[0, b₀]`.  Then `b_j ≤ c_j` and
`W_j ≥ V_j` on `[0, b_j]` for all `j`: among admissible sequences the envelope sequence has the
smallest tops and the steepest curves.*
*Proof.*  Induction.  `b_{j+1} = b⁺(W_j, b_j) ≤ b⁺(V_j, c_j) ≤ c_{j+1}` by Lemma A2 and (S1).  On `[0, b_{j+1})`:
`V_{j+1} ≤ min(1, Σ(·, V_j)) ≤ min(1, Σ(·, W_j))` by (S2), `V_{j+1} ≤ 1` and Lemma A2; `V_{j+1}` is convex, so it is a
convex minorant of the function whose envelope is `W_{j+1}`, hence `V_{j+1} ≤ W_{j+1}` there, and at
`b_{j+1}` by continuity.  ∎

## A3. The envelope sequence from the non-adaptive exponent

**Definition.**  `W₀ ≡ 0` on `[0, b₀]`, `b₀ := a`; `(W_{j+1}, b_{j+1}) := 𝖤(W_j, b_j)`.

**Proposition A5 [P].**  *The envelope sequence is admissible; `b₁ = a`; `W_j ≤ p_j` where `p_j` is finite; and
`b_j > h` for all `j`.*
*Proof.*  Lemma A3 at every step gives the form and (S2); (S1) holds with equality.  `b₁ = a` because
`Σ(B, 0) < ∞` exactly for `B < a` when `θ` has infinite slope at zero, and for all `B ≤ a` otherwise.
`W_{j+1} ≤ Σ(·, W_j) ≤ Σ(·, p_j) = p_{j+1}` by induction.  `b_j ≥ h` by Lemma A3, and `b_j > h` because the points
`(B, W_{j−1}(B))` stay regular a little beyond `h`: `W_{j−1}(h) ≤ L < 1 − h/a` and `W_{j−1}` is continuous.  ∎

So no range condition and no restart are needed: capping at one and taking the convex
envelope *are* the two requirements that "pull against each other" in §5 of `R_REPORT.md`,
resolved in the best possible way at every step.

## A4. The tops converge to `h`

**Proposition A6 [P].**  *For the envelope sequence of A3, `b_j ↓ h`; more precisely `b_j − h = O(1/j)`.*

*Proof.*  By Corollary A4 it is enough to exhibit one admissible sequence `(V_j, c_j)` from the same
start with `c_j → h`.  **The fixed-rate sequence:** `V₀ ≡ 0` on `[0, c₀]`, `c₀ := a`, and

    c_{j+1} := sup{ B ∈ [0, c_j] : V_j(B) ≤ 1 − B/a },      G_j := max{ 1, c_{j+1}·(1/h − 1/a) },      V_{j+1}(B) := ( V_j(B) + B/h − 1 )₊ / G_j     on [0, c_{j+1}].

*It is admissible.*  `V_{j+1}` is convex (a convex function plus an affine one; positive part; a
positive factor), nondecreasing, continuous, zero at `0`.  On `[0, c_{j+1}]`, `V_j(B) ≤ 1 − B/a`, hence
`V_j(B) + B/h − 1 ≤ B(1/h − 1/a) ≤ G_j`: values in `[0, 1]`.  (S1): if `Σ(B, V_j(B)) < ∞` then `B ≤ (1 − V_j(B))·a`
(the remark after Corollary U′), i.e. `V_j(B) ≤ 1 − B/a`, i.e. `B ≤ c_{j+1}`.  (S2): for every `(B, s)`,
`Σ(B, s) ≥ [B − (1 − s)θ(h)]/h = s + B/h − 1` (the rate `e = h` in the supremum; `θ(h) = h`) and `Σ(B, s) ≥ 0`; so
`V_{j+1} ≤ (V_j + B/h − 1)₊ ≤ Σ(·, V_j)`.
*Its tops reach `c⁎ := ah/(a − h)` after finitely many steps.*  `(c_j)` is nonincreasing; suppose
`c_j > c⁎` for all `j`, and let `c_∞ ≥ c⁎` be its limit, `G_∞ = c_∞(1/h − 1/a) ≥ 1` the limit of `G_j ≥ G_∞`.  At `B = c_∞ > h`
the numbers `v_j := V_j(c_∞)` satisfy `v_{j+1} = (v_j + κ)/G_j` with `κ := c_∞/h − 1 > 0`.  If `G_∞ > 1`, `v_j → κ/(G_∞ − 1)`,
and `κ/(G_∞ − 1) = (c_∞/h − 1)/(c_∞/h − c_∞/a − 1) > 1`; if `G_∞ = 1`, `v_j → ∞`.  Either way `v_j > 1 − c_∞/a` for some `j`,
so `c_{j+1} < c_∞`: a contradiction.
*From then on they converge to `h`.*  Let `c_{j₀} ≤ c⁎`.  For `j ≥ j₀`, `G_j = 1` and `V_{j+1} = (V_j + B/h − 1)₊ ≥ V_j + (B/h − 1)`,
so `V_{j₀+i}(B) ≥ i·(B/h − 1)` for `B ≥ h`, and `c_{j₀+i+1}` is at most the root of `i(B/h − 1) = 1 − B/a`:

    c_{j₀+i+1} − h  ≤  h·(1 − h/a)/(i + h/a).

Finally `b_j ≤ c_j` (Corollary A4) and `b_j > h` (Proposition A5).  ∎

*Remark.*  The fixed-rate sequence is the epoch schedule of the `O(1/k)` proof (slope steps at
the outer rate `h`) carried out on a whole convex family at once; the two displays are a
second, short proof of the rate `O(1/k)` for every pair with (H0) — no epochs, no drops.

## A5. The sharp rate

**Proposition A7 [P].**  *For the envelope sequence of A3 (and (H1)), `j²·(b_j − h) → c_*² = 2π²h²θ_hint″(0)`.*
*Proof.*  *Lower bound:* `b_j ≥ τ_j` (A6 below) and `liminf k²(τ_k − h) ≥ c_*²` (Theorem R).  *Upper bound:* take
`(s_t, ε₁)` as in Lemma RC and `k₁` with `b_{k₁} ≤ h + ε₁` (Proposition A6).  The cut orbit curves
`(W^cut_i, b^cut_i)_{i≥0}` from `b^cut_0 = h + ε₁`, `W^cut_0 ≡ 0`, are admissible, and `(W_{k₁+i}, b_{k₁+i})_{i≥0}` is an envelope
sequence with `b_{k₁} ≤ b^cut_0` and `W_{k₁} ≥ 0`; by Corollary A4, `b_{k₁+i} ≤ b^cut_i`, and `i²(b^cut_i − h) → c_*²`
(Proposition Z1(3)).  ∎

## A6. At the exponent level: `τ_j ≤ b_j` for every `j ≥ 1`

**Proposition A8 [P].**  *For the level recursion `T_1 = θ`, `T_{k+1} = min(T_k, R[T_k])` and the envelope
sequence of A3: `T_j ≤ M_{W_j, b_j}` on `(0, ∞)`, in particular `τ_j ≤ b_j`, for every `j ≥ 1`.*
*Proof.*  `j = 1`: `θ` is convex and nonincreasing, so it is the upper envelope of its tangent
lines, `θ(x) = sup{B − Σ(B, 0)·x : 0 ≤ B < a}` ((Σ3): the line through `(0, B)` tangent to `θ` has slope
`−Σ(B, 0)`); and `W₁ ≤ min(1, Σ(·, 0))`, `b₁ = a`, so `B − Σ(B, 0)x ≤ B − W₁(B)x ≤ M_{W₁, a}(x)`.  Step: Lemma A1.  ∎

So the tops of the envelope sequence are upper bounds for the exponent of `j` nested
levels **for every `j`**, where the proof of Theorem R gave an upper bound only beyond an
unquantified restart level.  In floating point (`experiments/workstreams/Z/z4_env.py`, cube,
`u = 1`; grid of 4 000 and 8 000 points per curve, the tops agree to `10⁻⁷·a`):

| `j` | 1 | 2 | 3 | 4 | 5 | 6 | 8 | 10 | 20 | 40 |
|---|---|---|---|---|---|---|---|---|---|---|
| `b_j/a` | 1 | 0.5004 | 0.3633 | 0.3128 | 0.2914 | 0.2813 | 0.2728 | 0.2691 | 0.2642 | 0.2631 |
| `j²(b_j − h)/c_*²` | 1.15 | 1.48 | 1.41 | 1.25 | 1.12 | 1.05 | 1.008 | 1.001 | 0.996 | 0.996 |

(`h/a = 0.2626`.)  The exact recursion has `τ₂ = 0.500a`, `τ₃ = 0.361a` (theory report §11.19): the
bound is within `0.1` and `0.6` per cent there — consistent with the remark of `R_REPORT.md` §5
that this dynamics is the exact dynamics of the best convex majorant, which is not
proved and not used.  **These numbers are not certified** (floating point; a convex
envelope of grid values is not a minorant between the grid points).

## A7. Theorem Z for the envelope schedule

**Theorem Z′ [P, conditional on the same statements as Theorem Z, without Theorem A's epochs].**
*Fix `u`, `δ`.  Let `(b_j)` be the tops of the envelope sequence of A3.  There are `n₀`, `c_Z = c_Z(u)` and `C′`
such that for all `n ≥ n₀`, `0 < ε ≤ 1` and `1 ≤ k ≤ n^{1/2}`*

    ln N(n; ε, δ)  ≤  n·b_k  +  k·c_Z·ln n  +  C′·(ln n + ln(1/ε)),            b_k − h ≤ C″/k²,     k²(b_k − h) → c_*².

*The schedule: the chain of Proposition T over the base bracket (the design of Theorem A of
workstream Q2 with no epoch: flat type `a`, least accuracy one, error `O(ln n)`), then `k` levels
of Proposition Z3 on the grid families of `W₀, …, W_{k−1}`, each followed by a chain
(Proposition Z4).*
*Proof.*  Lemma A1 (the envelope sequence is admissible, Proposition A5; `b₀ = a`), with the base
of flat type `a`; the unrolling and the orders are those of §6 of `Z_REPORT.md` with `M₁ = 0`; the
rate is Propositions A6, A7.  ∎

The theorem of `Z_REPORT.md` (cut curves over a base of `M₁` epochs) is the same statement for
another admissible sequence; by Corollary A4 the envelope schedule has the smaller `b_k` at
every `k`, and it needs no base beyond the bracket.  One level is spent on turning the flat
type of the base into the curve `W₁` (`b₁ = a`): typing the base bracket by the tangent lines
of `θ_na` instead (a finite-`n` form of Theorem 11.45 with a logarithmic error, not in the
repository) would save it.

## A8. Numbers [N], and one level exactly

As formulas (`z2_formula.py`, mode `env`; `u = 1`, `δ = 0.05`, `ε = 1`; entries are `ln(evaluations) − n·h` in
nats; the per-level loss is that of §7 of `Z_REPORT.md`, about `37`–`50` times `ln n`):

| `n` | non-adaptive: `n(a − h)` | Theorem 11.58a | Theorem A of Q2 | cut curves (`Z_REPORT.md`) | **envelope schedule** (`k`) | of which `n(b_k − h)` / chains / levels / base |
|---|---|---|---|---|---|---|
| `10⁴` | `818` | `1 080` | `1 002` | — | `1 025` (2) | `264` / `442` / `135` / `184` |
| `3.2·10⁴` | `2 590` | `2 101` | `2 148` | — | **`1 627`** (3) | `353` / `851` / `219` / `204` |
| `10⁵` | `8 180` | `3 936` | `3 949` | `7 466` | **`2 476`** (4) | `556` / `1 381` / `315` / `223` |
| `10⁶` | `8.18·10⁴` | `1.21·10⁴` | `1.06·10⁴` | `1.15·10⁴` | **`5 648`** (6) | `2 072` / `2 771` / `542` / `264` |
| `10⁷` | `8.18·10⁵` | `3.67·10⁴` | `2.61·10⁴` | `2.52·10⁴` | **`1.38·10⁴`** (12) | `4 931` / `7 340` / `1 223` / `304` |
| `10⁸` | `8.18·10⁶` | `1.16·10⁵` | `7.02·10⁴` | `4.91·10⁴` | **`3.33·10⁴`** (24) | `1.23·10⁴` / `1.80·10⁴` / `2 724` / `345` |
| `10⁹` | `8.18·10⁷` | `3.74·10⁵` | `2.06·10⁵` | `9.97·10⁴` | **`7.87·10⁴`** (52) | `2.62·10⁴` / `4.55·10⁴` / `6 512` / `387` |
| `10^{10}` | `8.18·10⁸` | `1.22·10⁶` | `6.47·10⁵` | `2.10·10⁵` | **`1.84·10⁵`** (104) | `6.58·10⁴` / `1.03·10⁵` / `1.43·10⁴` / `429` |
| `10^{12}` | `8.18·10^{10}` | `1.27·10⁷` | `6.76·10⁶` | `1.04·10⁶` | **`9.68·10⁵`** (484) | `3.04·10⁵` / `5.86·10⁵` / `7.80·10⁴` / `514` |
| `10^{15}` | `8.18·10^{13}` | `4.25·10⁸` | `2.35·10⁸` | `1.19·10⁷` | **`1.13·10⁷`** (4510) | `3.50·10⁶` / `6.89·10⁶` / `8.91·10⁵` / `643` |

So, as formulas at `u = 1`: at `n = 10⁴` every bound is above the non-adaptive cost; from
`n ≈ 3·10⁴` on the envelope schedule is below the non-adaptive cost and below every earlier
bound — by a factor `1.6` in the excess over `n·h` at `10⁵`, `1.9` at `10⁶`–`10⁷`, `3.5` at `10^{10}`, `7` at `10^{12}`,
`21` at `10^{15}`.  The tops `b_k` are computed for `k ≤ 80` (grid 8 000) and taken as `h + c_*²/k²` beyond
(the limit of `k²(b_k − h)/c_*²` is one and is approached from below: `0.9958, 0.9968, 0.9973` at
`k = 20, 40, 80`).  The caveats of §7 of `Z_REPORT.md` apply: evaluations of formulas, floating
point, no run of any algorithm, nests evaluated exactly only at small sizes.

One level exactly (`z1_onelevel.py`, mode `env`): Proposition Z3 on the grid families of the
envelope curves `W_j`, `j ∈ {0, 1, 2, 3, 5, 8, 11}`, `d = N ∈ {300, 10³, 3·10³, 10⁴}`, saturating inner
families, every admissible outer block: no violation of the accuracy, of (U∞), of the
exponent-level inequality (least slack `1.2` nats; equality to `10⁻³` where no capping is
active) or of the type (least slack `15.6` nats); both controls fail (two levels' gain
claimed for one: 66 cases).  At early levels the outer block chosen by the proxy `Π_j` can
be far from the block with the least certified bound (up to `51` nats): there a design
should choose by certified bound, which Proposition Z3 allows.

## A9. Extensive accuracies: geometric convergence, and a sub-exponential term `O((ln n)²)`

Proposition Z4 gives the type of the `k`-th family at *every* accuracy, so the envelope
schedule also bounds the cost at an extensive accuracy `x̂ = g·n`: by `n·M_{W_k, b_k}(g)` plus the
same errors.  At a positive rate `g` the majorant `M_{W_k, b_k}(g)` does not approach `θ_hint(g)` like
`1/k²` but **geometrically**: the bottleneck of the slope map is at the intercept `B = h`, and
the lines that matter at the rate `g > 0` have intercepts bounded away from `h`.

*Hypotheses of this section:* (H0), (H1), `θ(e) → 0` as `e → ∞`, and `J` differentiable on `(0, L)` (the
cube at every slope; the Gaussian pair).  Then `J` is continuous, concave and strictly
increasing from `J(0) = 0` to `J(L) = h` on `[0, L]`; for `0 ≤ B < h` let `t₁(B) ∈ [0, L)` be the solution of
`J(t) = B` — the smaller fixed point of `s ↦ Σ(B, s)` (a fixed point `s = Σ(B, s)` is a solution of
`J(s) = B`: `Σ = t′(1 − s)/(1 − t′)` with `J(t′)/(1 − t′) = B/(1 − s)`, and `s = t′`).  `t₁` is continuous and increasing,
`t₁(B) → L` as `B → h`, and `θ_hint(g) = sup_t [J(t) − t·g] ≥ B − t₁(B)·g` for every `B < h`.

**Lemma A9 (below `h` the orbits converge geometrically) [P].**  *For `η ∈ (0, h)`, `B ≤ h − η` and `i ≥ 0`:*

    0  ≤  t₁(B) − p_i(B)  ≤  t₁(B)·λ_η^i,        λ_η := hL/(hL + η)  <  1.

*Proof.*  `F(s) := Σ(B, s)` is convex and nondecreasing, `F(0) ≥ 0`, `F(t₁) = t₁`.  So `p_i = F^i(0)` is
nondecreasing and at most `t₁`, and for `s ≤ t₁`: `t₁ − F(s) = F(t₁) − F(s) ≤ κ·(t₁ − s)` for every subgradient
`κ` of `F` at `t₁`.  By (Σ4) of `R_REPORT.md`, `κ = θ(e₁)/e₁` is one, with `e₁ = J + (1 − t₁)J′`, `θ(e₁) = J − t₁J′` at
`t₁ = t₁(B)` (`J = B`, `J′ = J′(t₁)`): `κ = 1 − J′/(B + (1 − t₁)J′)`.  By concavity `J′(t₁) ≥ (h − B)/(L − t₁) ≥ η/L`, and
`x ↦ x/(B + (1 − t₁)x)` is increasing, so `1 − κ ≥ (η/L)/(h + η/L) = η/(hL + η)`.  ∎

**Lemma A10 (near the bottom the envelope is the image itself) [P].**  *For the envelope
sequence of A3, `η ∈ (0, h)` and every `k ≥ 1` with `b_k − h < η(1 − L)/L`:  `W_k = Σ(·, W_{k−1}(·))` on `[0, h − η]`.
Hence, if `k(η)` is the first such `k`, `W_{k(η)+i} ≥ p_{i+1}` on `[0, h − η]` for all `i ≥ 0`.*
*Proof.*  `H := Σ(·, W_{k−1}(·))` is convex and nondecreasing on `[0, b_k)` (a jointly convex function,
nondecreasing in its second argument, of a convex function), `H(0) = 0`, and
`H(h) ≤ Σ(h, p_{k−1}(h)) = p_k(h) ≤ L` ((P2)).  The function enveloped is `f = min(1, H)`: equal to `H` up to
the point `β` where `H` reaches one, and to one beyond.  Its lower convex envelope is `H` on
`[0, B_t]` and, on `[B_t, b_k]`, the line through `(b_k, 1)` that supports `H` at `B_t`, where `B_t` is the
last point whose tangent line has a value at most one at `b_k` (that function is convex,
below `f`, and every convex minorant of `f` is below it: on `[B_t, b_k]` by the chord).  For
`B ≤ h − η` the right derivative of `H` is at most `(H(h) − H(B))/(h − B) ≤ L/η`, and the tangent line at `B`
has at `b_k` the value `[H(B) + H′(B+)(h − B)] + H′(B+)(b_k − h) ≤ H(h) + (L/η)(b_k − h) < 1`.  So `B_t > h − η`.
The second claim: `W_{k(η)−1} ≥ 0 = p₀`, `Σ` is nondecreasing in the slope, and `b_k` is nonincreasing.  ∎

**Proposition A11 (geometric convergence at a positive accuracy rate) [P].**  *For every `g > 0`
there are `η > 0` and `k₁` such that for all `k ≥ k₁`*

    θ_hint(g)  ≤  M_{W_k, b_k}(g)  ≤  θ_hint(g) + g·λ_η^{k − k₁}.

*Proof.*  The left inequality: `M_{W_k, b_k} ≥ T_k ≥ θ_hint` (A6; the recursion stays above the hinted
exponent).  Let `m := θ_hint(g) − (h − L·g)`; `m > 0` because `θ_hint` is convex with `θ_hint(0) = h`,
`θ_hint′(0) = −L` and `θ_hint″(0) > 0`.  Choose `η` with `(L − t₁(h − η))·g ≤ m/3`, and `k₁ ≥ k(η)` such that `b_k − h ≤ m/3`
and `g·λ_η^{k − k(η)} ≤ m/3` for `k ≥ k₁` (Proposition A6).  Let `k ≥ k₁`, `i = k − k(η)`.  By Lemmas A9, A10,
`W_k ≥ p_{i+1} ≥ t₁ − λ_η^{i}` on `[0, h − η]`.  *Lines with `B ≤ h − η`:* `B − W_k(B)g ≤ B − t₁(B)g + gλ_η^i ≤ θ_hint(g) + gλ_η^i`.
*Lines with `h − η ≤ B ≤ b_k`:* `W_k(B) ≥ W_k(h − η) ≥ t₁(h − η) − λ_η^i`, so
`B − W_k(B)g ≤ b_k − t₁(h − η)g + gλ_η^i = (h − Lg) + (b_k − h) + (L − t₁(h − η))g + gλ_η^i ≤ h − Lg + m = θ_hint(g)`.
Finally `λ_η^{k − k(η)} ≤ λ_η^{k − k₁}` because `k(η) ≤ k₁`.  ∎

**Theorem Z″ (extensive accuracies) [P, conditional as Theorem Z′].**  *Fix `u`, `δ` and an accuracy
rate `g > 0`.  There are `n₀` and `C = C(u, g)` such that for all `n ≥ n₀`*

    ln N(n; g·n, δ)  ≤  n·θ_hint(g) + C·(ln n)².

*Proof.*  The family `𝔉̂_k` of the envelope schedule has, at the accuracy `x̂ = g·n ≥ 𝒳` and the
dimension `n`, a certified cost of at most `max_{𝔏_k}[n·B − σ·x̂] + Ê_k ≤ n·M_{W_k, b_k}(g) + k·c_Z·ln n + C′ln n`
(Proposition Z4; §6 of `Z_REPORT.md`).  Take `k = k₁ + ⌈ln(g·n)/ln(1/λ_η)⌉` in Proposition A11: then
`n·g·λ_η^{k − k₁} ≤ 1` and `k = O(ln n)`.  ∎

Theorem 11.54 of the theory report has `exp(n·θ_hint(g) + o(n))` at extensive accuracies; this is
`exp(n·θ_hint(g) + O((ln n)²))`, against the hinted lower bound.  The constant grows like `1/g` as
`g → 0` (`1 − λ_η ≈ η/(hL)`, and `η` of the order of `m ≈ ½θ_hint″(0)g²`… — heuristically the defect is
`≈ 2θ_hint″(0)·g²·e^{−kg/h}` for `kg/h ≫ 1`, from the profile of `R_REPORT.md` §8a, which would give
`C ≈ (h/g)·c_Z`); the proof above does not track it.  In between — accuracies `x̂` with
`1 ≪ x̂ ≪ n` — the same schedule interpolates, heuristically
`n·θ_hint(x̂/n) + O(min{n^{1/3}(ln n)^{2/3}, (n/x̂)·(ln n)²})`; only the two ends are proved.

*Numerically* (`z5_extensive.py`; cube, `u = 1`; floating point): `k²(M_{W_k, b_k}(g) − θ_hint(g))/c_*²` —

| `k` | `g = 0` | `0.01h` | `0.1h` | `0.5h` | `h` | `0.5ε*` |
|---|---|---|---|---|---|---|
| 2 | 1.48 | 1.47 | 1.40 | 1.04 | 0.55 | 0.02 |
| 5 | 1.12 | 1.07 | 0.59 | 0.10 | 0.017 | `1·10⁻⁴` |
| 10 | 1.001 | 0.79 | 0.30 | 0.019 | `4·10⁻⁴` | `< 10⁻⁴` |
| 20 | 0.996 | 0.63 | 0.15 | `4·10⁻⁴` | `< 10⁻⁴` | |
| 40 | 0.997 | 0.50 | 0.039 | `< 10⁻⁴` | | |
| 80 | 0.997 | 0.35 | 0.002 | | | |

— constant at `g = 0`, and falling off like `2ζ²e^{−ζ}/(2π²)`, `ζ = kg/h`, at positive rates (at `ζ = 8`:
`0.0022` predicted by the profile, `0.002` computed).

## A10. What is not proved

* Everything listed in §9 of `Z_REPORT.md`.
* This addendum is unrefereed.  Its exponent-level statements (A1–A8) are short and
  self-contained given `R_REPORT.md`; the numerical values of the tops are floating point.
* That the envelope dynamics is the *exact* dynamics of the best convex majorant of `T_k`
  (so that `b_j = τ_j`) is not proved; A6 gives `τ_j ≤ b_j`.
* In A9 the constant `C(u, g)` is not tracked, the intermediate accuracies are a heuristic,
  and the matching lower bound at extensive accuracies is the hinted one of the theory
  report (Theorems 11.25(a), 11.54), not re-derived here.
