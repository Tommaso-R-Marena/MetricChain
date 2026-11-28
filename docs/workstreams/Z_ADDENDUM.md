# Workstream Z, addendum — the envelope sequence: the assembly from the non-adaptive base, without a restart

*Coordinator, 2026-11-26 (written while `Z_REPORT.md` was with its referee, and kept in a file of
its own for that reason).  Paper proofs; the numerics are floating point on grids [N] unless
they are called certified.  **Refereed internally** (an AI referee, not external peer review):
`docs/workstreams/Z_ADDENDUM_REVIEW.md`, with its own code in
`experiments/workstreams/Z/review_addendum/` — "no error of substance; every numbered statement
is correct as stated or correct after a repair of wording"; its ten findings are applied
below and listed in the note that follows.  **Sections A6a, A6b and A9a were added after that
review; they have since had a referee of their own** (`docs/workstreams/Z_A6_REVIEW.md`, own code in
`experiments/workstreams/Z/review_a6/`): *one statement wrong as first stated — the closed form of the second
level for the cube, which holds for `u ≤ 4.6535` only; everything else correct as stated or after a repair of
wording or of a citation; the script is a sound certificate.*  Its findings are applied in the text and
listed in the second note below.  Notation and the quoted
statements are those of `Z_REPORT.md` §1 and of `R_REPORT.md` (`θ = θ_na` satisfying (H0), (H1) there;
`a = θ(0+)`, `h` the fixed point, `Σ` the slope map, `p_j` the orbit curves, `M_{W,b}`, `𝓔(W, b)`).*

> **Coordinator's note after the review (2026-11-26).**  The referee re-derived every step
> and replicated the numerics with code that shares nothing with ours (the envelope
> sequence for the cube at three slopes and the Gaussian pair; the comparison with the
> fixed-rate sequence and a cut chain; Lemma A1 on envelope curves; the second and third
> level of the recursion by brute force; the geometric convergence of A9; two rows of the
> table of A8).  Applied in place: **(1)** the sentence after Theorem Z′ "the envelope
> schedule has the smaller `b_k` at every `k`" was wrong — Corollary A4 compares sequences
> from the same start (A7); **(2)** "`b_j = τ_j`" is not an open question: it holds at `j = 2`
> and fails at `j = 3` — now section A6a, with a proof of the first and a computation of
> the second that was made here independently; **(3)** the factors `3.5, 7, 21` of A8 were
> against Theorem A of Q2, not "every earlier bound"; **(4)** a grid artefact in the
> quoted ratios, and "approached from below" is specific to the pair; **(5)** the
> constant of Theorem Z″: the proof gives `1/g²`, the heuristic `1/g`; **(6)** Lemma A1 needs
> `W₀ ≡ 0`; **(7)** Theorem Z″ is for `0 < g < ε*`; **(8)**–**(10)** two rounded numbers and
> three points of wording in proofs.  Not checked by the referee: the finite-`n`
> statements that Theorems Z′, Z″ are conditional on (read, not re-derived), the one-level
> test and the nests in envelope mode (not re-run), pairs with a finite slope at zero (by
> hand only); nothing of the referee's is certified.

> **Coordinator's note after the review of A6a, A6b, A9a (2026-11-27; `Z_A6_REVIEW.md`).**  That referee
> re-derived every statement of the three sections, verified the *output* of `z6_certified_tops.py` line by
> line with an independent verifier (31 946 lines, among them the first eight levels of the published run;
> its own integer interval arithmetic, no mpmath), built an independent certified sequence, and tried to break
> each statement on random inputs and twelve pairs.  **Verdicts:** Proposition A12(a), (b), (d), Lemma A9′,
> Proposition A11′ correct as stated; Theorem Z‴ correct as stated, conditionally as Theorem Z′; the script is a
> sound certificate.  **Applied in place:** **(1)** *wrong as first stated* — "for the cube `τ₂ = b₂ = a²/(a + x*)`":
> true exactly for `u ≤ 4.6535196` (A6a; theory report Theorem 11.58e(e)); no proof used it.  **(2)** The
> nine-digit table of A6b prints certified doubles rounded *to nearest*: a rigorous reading adds one unit in the
> last printed place (the six-digit table of the theory report is rounded up and valid).  **(3)** A citation that
> did not carry the claim: `τ₂ = b₂` and A12(d) use `sup T_{k+1} = τ(T_k)`, which the theory report's remark only
> *defines*; it is Lemma R0 of the review (§1.1, ten lines, confirmed by brute force).  **(4)** Two numbers of the
> table of A6a (`τ₃` is `5·10⁻⁶·a` high; `τ(M_{W₂,b₂})` equals `b₃`).  **(5)** Proposition A13: the cap line is below the
> *maximum* of such lines and the zero line; "nondecreasing" follows from convexity, nonnegativity and the value
> zero at zero; the restriction "pair with infinite slope at zero" is not needed in A12(b), (c) or A13; "by Lemma
> A1 and Proposition A8" needs Corollary A4 or the base case of A8 read for a start on `[0, ā]`.  **(6)** mpmath's
> interval logarithm is not a proved enclosure in its last bit — harmless here (the four-ulp rounding of the
> coefficients leaves a proved headroom of one double ulp; `ā ≥ a` verified independently at six slopes); one more
> `nextafter` would remove the dependence (not changed: the script is the audited one).  **(7)** "at 80 levels" is
> at 78; the range in A10.  **Not checked by that referee:** Proposition U and the finite-`n` statements (read,
> not re-derived); the published runs beyond level eight of `u = 1` and the runs at `u = 2`, `u = ½` and to 400
> levels (compared with its own tops and brackets only); nothing of its is machine-checked.

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
level they bound the level recursion from the first level on, `τ_j ≤ b_j` (A6) — with equality
at the second level and, numerically, a strict inequality from the third (A6a); certified
values of such bounds are in A6b.  Theorem Z then
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
`Z_REPORT.md` hold for every admissible sequence with `W₀ ≡ 0` and `b₀ ≤ a` over every base family of
flat type `b₀` with least accuracy at most one (a flat type `b₀` is the type of the grid family of
`W₀` only if `W₀` vanishes at the top — the referee's repair; both sequences below have `W₀ ≡ 0`); and at
the exponent level, if `T ≤ M_{W_j, b_j}` for a nonincreasing `T ≥ 0`, then `min(T, R[T]) ≤ M_{W_{j+1}, b_{j+1}}`.*
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
`(B, W_{j−1}(B))` stay regular a little beyond `h`: `W_{j−1}(h) ≤ L < 1 − h/a` and `W_{j−1}` is continuous
(`L < 1 − h/a` is consequence (ii) of (H1) in `R_REPORT.md` — the one place where (H1) enters; (P2) is `p_j(h) ≤ L`).  ∎

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
*From then on they converge to `h`.*  Let `c_{j₀} ≤ c⁎` (`j₀` exists by the previous step; it is not explicit).  For `j ≥ j₀`, `G_j = 1` and `V_{j+1} = (V_j + B/h − 1)₊ ≥ V_j + (B/h − 1)`,
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
`−Σ(B, 0)`; where `θ` is affine near zero the supremum is a limit `B ↑ a`); and `W₁ ≤ min(1, Σ(·, 0))`, `b₁ = a`, so
`B − Σ(B, 0)x ≤ B − W₁(B)x ≤ M_{W₁, a}(x)`.  Step: Lemma A1.  ∎

So the tops of the envelope sequence are upper bounds for the exponent of `j` nested
levels **for every `j`**, where the proof of Theorem R gave an upper bound only beyond an
unquantified restart level.  In floating point (`experiments/workstreams/Z/z4_env.py`, cube,
`u = 1`; grid of 4 000 and 8 000 points per curve, the tops agree to `10⁻⁷·a`):

| `j` | 1 | 2 | 3 | 4 | 5 | 6 | 8 | 10 | 20 | 40 |
|---|---|---|---|---|---|---|---|---|---|---|
| `b_j/a` | 1 | 0.5004 | 0.3633 | 0.3128 | 0.2914 | 0.2813 | 0.2728 | 0.2691 | 0.2642 | 0.2630 |
| `j²(b_j − h)/c_*²` | 1.15 | 1.48 | 1.41 | 1.25 | 1.12 | 1.05 | 1.008 | 1.001 | 0.996 | 0.996 |

(`h/a = 0.2626`.)  The recursion itself has `τ_k/a = 0.5004, 0.361, 0.311, 0.290, 0.280` at `k = 2, …, 6`
(theory report §11.19): **the bound is an equality at `k = 2` and is `0.5` to `0.6` per cent above
from `k = 3` on** — section A6a has the proof of the first and the computation of the second.
The envelope sequence is the best *admissible* sequence (Corollary A4), i.e. the best that
the line-by-line step of Proposition U can give; it is not the recursion.  (An earlier
version of this paragraph said "within `0.1` per cent" at `k = 2` — the rounding of a quoted
`0.500` — and left `b_j = τ_j` open; the referee and a computation of ours made at the same
time settle it.)  **The numbers of this table are floating point** (a convex envelope of grid
values is not a minorant between the grid points, and the grid errs downwards, by about
`10⁻⁷·a` at `k = 80` — the referee); certified upper bounds are in section A6b.

## A6a. Where the envelope step is exact, and where it is not  *(added after the first review; refereed since — `Z_A6_REVIEW.md`, second note at the head)*

For a nonincreasing `T ≥ 0` on `[0, ∞)` let

    τ(T) := inf_{0<φ<1} sup_{γ≥0} [ min(γ, φa) + (1 − φ)·T(γ/(1 − φ)) ]

— the level formula at vanishing accuracy (theory report §11.19, remark (1): `τ_{k+1} = τ(T_k)`) — and
`T^♯(x) := sup_{0≤y≤x} (y + T(y)) − x`, the least function above `T` all of whose slopes are at least `−1`.

**Proposition A12 [P].**
(a) *`τ(T) = inf_{x>0} a·(x + T^♯(x))/(a + x) = τ(T^♯)`: at vanishing accuracy a level sees the family below it only
through `T^♯`; slopes steeper than one are worth nothing to the next level.*
(b) *For a family `(W, b)`: `M_{W,b}^♯ = M_{W,b}`; `M_{env f, b} = M_{f, b}` for every `f : [0, b] → [0, 1]` (the convex
envelope loses nothing); and `τ(M_{W,b}) = max_{0≤B≤b} min(B, (1 − W(B))·a)`, which is `b⁺(W, b)` for a pair with
infinite slope at zero.  So **the envelope step is exact at vanishing accuracy**: `b_{j+1} = τ(M_{W_j, b_j})`.*
(c) *`θ^♯ = max(θ, a − ·) = M_{W₁, a}`.  Hence `τ₂ = b₂` for every pair with infinite slope at zero.*
(d) *In general `τ_{j+1} = τ(T_j^♯) ≤ τ(M_{W_j, b_j}) = b_{j+1}`, with equality as long as `T_j^♯ = M_{W_j, b_j}`.*

*Proof.*  (a) With `y = γ/(1 − φ)`, `x = φa/(1 − φ)` the bracket is `(1 − φ)[min(y, x) + T(y)]`; for `y ≥ x` it is at most
its value at `y = x` (`T` is nonincreasing), so the supremum is `(1 − φ)·sup_{y≤x}(y + T(y)) = (1 − φ)(x + T^♯(x))`, and
`1 − φ = a/(a + x)`.  `y + T^♯(y) = sup_{z≤y}(z + T(z))` is nondecreasing, so `(T^♯)^♯ = T^♯`.
(b) The slopes of `M_{W,b}` lie in `[−1, 0]`.  For `x > 0`, `sup_B (B − x·f(B))` is `x` times the conjugate of `f` at `1/x`,
and a function and its lower convex envelope have the same conjugate.  By (a),
`τ(M_{W,b}) = inf_φ [φa + (1 − φ)M_{W,b}(x)] = inf_φ max_B [(1 − φ)B + (1 − W(B))φa]`; the bracket is linear in `φ` and
concave in `B`, so by the minimax theorem this is `max_B inf_φ = max_B min(B, (1 − W(B))a)`.  For infinite slope at
zero `Σ(B, W(B)) < ∞` iff `B < (1 − W(B))a` (or `B = 0`), and `B` increases while `(1 − W(B))a` decreases.
(c) `y + θ(y)` is convex with the value `a` at `0`, so `sup_{y≤x}(y + θ(y)) = max(a, x + θ(x))`.  By (b),
`M_{W₁, a}(x) = sup_B (B − x·min(1, Σ(B, 0)))`: the lines with `Σ(B, 0) ≤ 1` are the tangent lines of `θ` with slopes
in `[−1, 0]`, whose supremum is `θ(x)` where `θ′(x) ≥ −1` and is below `a − x` before; the others give `sup B − x = a − x`.
Then `τ₂ = τ(θ) = τ(θ^♯) = τ(M_{W₁, a}) = b₂`.  (d) `T_j ≤ M_{W_j, b_j}` (Proposition A8) and `τ` is monotone.  ∎
(*The identity `τ_{k+1} := sup T_{k+1} = τ(T_k)` used in (c), (d)* is not in the theory report's remark, which defines the
bounded-accuracy sequence by the formula and proves "at most"; it is Lemma R0 of `Z_A6_REVIEW.md` §1.1.  The
restriction "infinite slope at zero" in (b), (c) is not needed.)

For the cube `x + θ(x) − a` changes sign once, at `x* > 0`, and `τ₂ = b₂ = a²/(a + x*)` **for `u ≤ u₀ = 4.6535196`** —
exactly when `|θ′(x*)|·(a + x*) ≤ x*`, i.e. when the top lies on the cap line of `W₁`.  For larger slopes the minimum
of `a·max(a, x + θ(x))/(a + x)` is beyond the kink, `τ₂ = b₂` is the root of `B = (1 − Σ(B, 0))·a` on the uncapped curve
and is *smaller* than `a²/(a + x*)` (`0.602893·a` against `0.604053·a` at `u = 5`; `0.7139·a` against `0.7874·a` at `u = 8`).
(The first version stated the closed form for every slope: found by the referee of this section, its §1.5; no
proof uses the closed form, and the numbers quoted at `u = ½, 1, 2` are right.)

**From the third level on the envelope tops are strictly above the true exponents [N].**
(`experiments/workstreams/Z/z7_exactness.py` → `out_z7_exactness_u1.txt`; cube, `u = 1`; floating point.  The
referee, whose brief did not include this section, found the same independently and adds in a
postscript that (b) and (c) of Proposition A12 hold numerically to `10⁻¹⁵`, and that a first value of ours,
`0.361296·a`, was a grid of step `10⁻³` in the outer fraction sitting at a kink — corrected below.)

| | value | |
|---|---|---|
| `τ₂`, closed form `a²/(a + x*)` | `0.055517524915 = 0.500410018·a` | |
| `b₂`, envelope sequence on a grid of 8 000 / certified upper bound (A6b) | `0.055517524693` / `0.055517525617` | equal, as proved |
| `τ₃ = τ(T₂)`, with `T₂ = min(θ, R[θ])` computed by direct minimisation over `(φ, β)` at 420 rates, the outer fraction of the third level refined to `10⁻⁹` | `0.361189·a` (about `5·10⁻⁶·a` high: `0.361184·a` by two referees' independent computations) | the referee, by brute force with another mesh: `0.361184·a`; the theory report has `0.361·a` |
| `τ(M_{W₂, b₂})`, the same operator on the envelope majorant | `0.363303·a` | a discretisation value of a quantity that *equals* `b₃` by Proposition A12(b) |
| `b₃` | `0.363301·a` | `b₃ − τ₃ = 2.1·10⁻³·a` |

*Where the loss is.*  The second level `T₂` is below its envelope majorant `M₂ := M_{W₂, b₂}` at every positive
accuracy rate computed, because the true level uses a positive inner tolerance (`β/g` between `0.45` and `0.007` at
the minimiser), which the line-by-line step (`β = 0`, Lemma M of `R_REPORT.md`) does not: `M₂ − T₂` is `0.03·a` to
`0.13·a` for `g ≤ 0.2ε*`, where `T₂` falls more steeply than slope `−1` — by (a) the next level does not see
that part: there `T₂^♯ = M₂ = b₂ − g` — and `3.7·10⁻³·a`, `1.8·10⁻³·a`, `7·10⁻⁴·a` at `g = 0.4ε*, 0.5ε*, 0.6ε*`, where
`T₂^♯ = T₂ < M₂`: this part the third level sees (its optimal outer fraction `φ = 0.278` puts the inner accuracy
rate at `0.36ε*`).  Against the theory report's values of the recursion itself, `τ_k/a = 0.5004, 0.361, 0.311,
0.290, 0.280` for `k = 2, …, 6`, the envelope tops `b_k/a = 0.5004, 0.3633, 0.3128, 0.2914, 0.2813` are equal at `k = 2`
and `0.5` to `0.6` per cent above from `k = 3` on; both sequences have the same asymptotics (A5).  So the envelope
sequence is the exact solution of the recursion **restricted to families that are handed down as convex sets
of lines with the inner tolerance zero**, not of the recursion: a step that also carried the tolerance would
close the gap at the exponent level (not written; at finite `n` the tolerance is what Lemma U's finite range
and the drops of workstream Q2 are about).

## A6b. Certified tops  *(added after the first review; refereed since — `Z_A6_REVIEW.md`, second note at the head)*

The tops in the table of A6 are floating-point numbers.  Admissibility asks only for `≤` in (S2) and `≥` in (S1),
so a *lower* bound of the slope map suffices, and that needs no optimisation:

**Proposition A13 (multi-rate sequences) [P].**  *Let `(V, c)` be a family that is a maximum of the zero line and
finitely many lines `ℓ_i`, let `(e_m, ϑ_m)` be pairs with `ϑ_m ≥ θ(e_m)`, and `ā ≥ a`.  Then every line*

    [ B − ϑ_m·(1 − ℓ_i(B)) ] / e_m            *is below*  `Σ(B, V(B))`  *on*  `[0, c]`.

*Hence, if `c′ ≤ c` satisfies `c′ + ā·V(c′) ≥ ā` or `c′ = c`, and `V′` is convex with `V′(0) = 0`, `V′(c′) ≤ 1` and
`V′ ≤` the maximum of the zero line and of such lines on `[0, c′]`, then `(V, c), (V′, c′)` are two consecutive
members of an admissible sequence (pair with infinite slope at zero).*  (Wording after finding F2 of the science
division's review SCI-REV-0030: the cap line of the script is below the *maximum* of two such lines, below neither
alone — a line through `(c′, 1)` that is below the hull at all its vertices is below the hull.)
*Proof.*  `Σ(B, s) ≥ [B − (1 − s)θ(e_m)]/e_m ≥ [B − (1 − s)ϑ_m]/e_m` for `s ≤ 1`, and the right side is nondecreasing in
`s`; `ℓ_i ≤ V ≤ 1` on `[0, c]`.  (S1): `Σ(B, V(B)) < ∞` forces `B ≤ (1 − V(B))a ≤ (1 − V(B))ā`, and `B + āV(B)` is
increasing.  (S2) needs only `V′ ≤ max(0, such lines)`.  `V′` is a family: convex and zero at zero by hypothesis,
nonnegative (it is used as a maximum with the zero line), hence nondecreasing (a convex nonnegative function that
vanishes at `0` is nondecreasing).  ∎

`z6_certified_tops.py` builds such a sequence for the cube from `V₀ ≡ 0` on `[0, ā]`: `θ(e) = KL(ρ‖½)` with
`KL(ρ‖p_u) = e`, so for a floating-point `ρ` the pair "an upper bound of `KL(ρ‖p_u)`, an upper bound of `KL(ρ‖½)`" is
valid (interval arithmetic, 30 digits, rounded outwards); the lines are stored as doubles with the slope
rounded down and the intercept rounded down; which lines and rates are used is chosen in floating point (one
line per sample point, the rate by a golden-section search) and affects the quality only; the upper hull, the
tangent line from `(c′, 1)` that caps the curve at one, the values at the top and the inequality
`c′ + āV(c′) ≥ ā` are computed in exact rational arithmetic.  By Lemma A1, Corollary A4 and Proposition A8 (its base case read for a start on `[0, ā]`) its tops are
**rigorous upper bounds for the exponents of the level recursion, `τ_j ≤ c_j`** — given those statements —
and `T_j(g) ≤ max_B (B − V_j(B)g)` at every rate (the maximum is evaluated exactly at the vertices).

**What is evidence for a run, and what is not (finding F1 of SCI-REV-0030; resolved in Phase II).**  The script's
last line ("ALL CHECKS PASS") tests only that the tops are nonincreasing and above a floating-point `h`; the pairs
and the rounding of the lines are valid *by construction* and are not re-checked by the script, so that line cannot
fail for the errors a certificate must exclude.  The validity of a run is established by an **independent exact
checker**, `experiments/workstreams/Z/review_a6/a6_02_verify_z6_output.py` (written by the referee of these sections;
own integer interval arithmetic, own hull, no code shared with the script): for every stored line it exhibits a
rational pair, a parent line and a rational witness `ρ`, and it verifies the cap line, the family property and the
top exactly.  `experiments/workstreams/Z/z6_pipeline_mutations.py` measures the difference on a small instance
(`u = 1`, four levels, 40 sample points; `out_z6_pipeline_mutations.txt`): of ten *gross* mutations of the script —
rounding directions reversed by `10⁻⁶`, the two divergences exchanged, a steeper parent line, a cap with half the
tangent slope, a top lowered by `10⁻³` — the checker rejects all ten, while the script's own last line still
passes for nine (the tenth trips an assertion); of six mutations that only remove a safety margin (one or four
units in the last place, a cap flatter by `10⁻⁶`, a relaxed top test) it rejects two and accepts four, and an
accepted output *is* a valid certificate (a proved pair for every line; the script keeps four units of margin).
The science division's referee found the same with its own checker and thirty mutations, and verified the
three committed runs line by line: 278 704 generated lines at `u = 1`, no violation.  The harness test XVI.11
is a third, independent re-implementation of the construction with eleven mutations.
<!-- Z:J400 -->
The 400-level run (`K = 4000`): its independent verification is described in `docs/phase2/R29_RESOLUTION.md` §4.2.
<!-- /Z:J400 -->

| `j` | 2 | 3 | 4 | 5 | 6 | 8 | 10 | 20 | 40 | 80 | 200 | 400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| certified `c_j/a ≥ τ_j/a`, `u = 1` | `0.500410024` | `0.363300653` | `0.312791462` | `0.291376787` | `0.281323250` | `0.272750695` | `0.269065250` | `0.264243938` | `0.263047017` | `0.262747193` | `0.262663126` | `0.262651110` |
| `u = 2` | `0.505615446` | `0.383347314` | `0.341033400` | `0.323697863` | `0.315235252` | `0.307181543` | `0.303467854` | `0.298465858` | `0.297189804` | | | |
| `u = ½` | `0.500026741` | `0.358645034` | `0.305680047` | `0.282897289` | `0.272167511` | `0.263247512` | `0.259553884` | `0.254793046` | `0.253620656` | | | |

(The entries are the script's printed values of certified doubles, **rounded to nearest: a rigorous reading adds
one unit in the last printed place**; the six-digit table of the theory report is rounded up.
`h/a = 0.262647098, 0.296757, 0.253231` at `u = 1, 2, ½`; 3 000 sample points per level, 4 000 for the run to 400
levels; `out_z6_certified_*.txt`.  The referee's postscript: all thirty certified tops lie above its own
envelope tops, by at most `6·10⁻⁷·a`, as Corollary A4 requires; the script has since been refereed twice — `Z_A6_REVIEW.md` §3 and the science division's SCI-REV-0030 — and found sound on the committed runs.)  The certified tops exceed the floating-point envelope tops by `3·10⁻⁸` to
`2.5·10⁻³` of their distance to `h` (the larger figure at 78 levels; `1.7·10⁻³` at 80); at 400 levels `j²(c_j − h)/c_*² = 1.0009`.
Harness XVI.11 runs a small instance with its exact-arithmetic checks, the comparison with the closed form
for two levels, and three negative controls (eleven mutations, all caught).

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
another admissible sequence.  The two start at different heights (`a` against `h + ε₁`), so
Corollary A4 does not compare them level by level — at `u = 1`, `(s_t, ε₁) = (L + 0.05, 0.003)` the
envelope tops are `b_k − h = 2.81h, 0.905h, 0.383h, 0.191h, 0.109h` at `k = 1, …, 5` against
`b^cut_k − h = 0.103h` (the referee's counterexample to an earlier sentence here).  What A4 gives
is `b_{k₁+i} ≤ b^cut_i` for all `i`, `k₁` the first level with `b_{k₁} ≤ h + ε₁` (`k₁ = 6` at `u = 1`): `k₁ + i`
envelope levels over the bracket do at least as well as `i` cut levels over the base of
`M₁` epochs (43 levels there).  The envelope schedule needs no base beyond the bracket.  One level is spent on turning the flat
type of the base into the curve `W₁` (`b₁ = a`): typing the base bracket by the tangent lines
of `θ_na` instead (a finite-`n` form of Theorem 11.45 with a logarithmic error, not in the
repository) would save it.

## A8. Numbers [N], and one level exactly

As formulas (`z2_formula.py`, mode `env`; `u = 1`, `δ = 0.05`, `ε = 1`; entries are `ln(evaluations) − n·h` in
nats; the per-level loss is that of §7 of `Z_REPORT.md`, `31` to `50` times `ln n` over the rows of the table):

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
`n ≈ 3·10⁴` on (conservatively: the formulas cross near `1.5·10⁴`) the envelope schedule is below
the non-adaptive cost and below every earlier bound.  In the excess over `n·h` it is below
Theorem A of Q2 by the factors `1.6` at `10⁵`, `1.9` at `10⁶`–`10⁷`, `3.5` at `10^{10}`, `7` at `10^{12}`, `21` at `10^{15}`,
and below the cut-curve bound of `Z_REPORT.md` by `1.83, 1.47, 1.27, 1.15, 1.07, 1.05` at
`10⁷, 10⁸, 10⁹, 10^{10}, 10^{12}, 10^{15}` (an earlier version quoted the first list as "against every
earlier bound").  The tops `b_k` are computed for `k ≤ 80` (grid 8 000) and taken as `h + c_*²/k²` beyond.
For the cube at `u = 1` the ratio `k²(b_k − h)/c_*²` approaches its limit one from below — `0.996, 0.997,
0.998` at `k = 20, 40, 80` without a grid (the referee, who followed it to `k = 800`; our grid values
`0.9958, 0.9968, 0.9973` carry a grid artefact in the last digits; the certified upper bounds of
A6b have `0.9960, 0.9978, 0.9989` and `1.0009` at `k = 400`) — so there the extrapolation is an
upper estimate; this is specific to the pair (for the Gaussian pair the limit is
approached from above).  The caveats of §7 of `Z_REPORT.md` apply: evaluations of formulas, floating
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
`H(h) ≤ Σ(h, p_{k−1}(h)) = p_k(h) ≤ L` ((P2)).  The function enveloped is `f = min(1, H)`.  If `H ≤ 1` on the
whole of `[0, b_k]`, then `f = H` is convex and `W_k = H`: nothing to prove.  Otherwise `f` is equal to `H` up to
the point `β < b_k` where `H` reaches one, and to one beyond.  Its lower convex envelope is `H` on
`[0, B_t]` and, on `[B_t, b_k]`, the line through `(b_k, 1)` that supports `H` at `B_t`, where `B_t` is the
last point whose tangent line has a value at most one at `b_k` — at a kink "tangent" means a
supporting line, and if no point has such a line then `B_t = 0` and the envelope is the chord
from the origin (Gaussian pair, `k = 1`: `W₁(B) = B`) — (that function is convex,
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
rate `0 < g < ε*` (`ε*` the rate from which `θ_na` vanishes; for `g ≥ ε*` the statement is true and
empty — `θ_hint(g) = 0` and the non-adaptive bracket already costs `exp(O(ln n))`).  There are
`n₀ = n₀(u, δ, g)` and `C = C(u, g)` such that for all `n ≥ n₀`*

    ln N(n; g·n, δ)  ≤  n·θ_hint(g) + C·(ln n)².

*Proof.*  The family `𝔉̂_k` of the envelope schedule has, at the accuracy `x̂ = g·n ≥ 𝒳` and the
dimension `n`, a certified cost of at most `max_{𝔏_k}[n·B − σ·x̂] + Ê_k ≤ n·M_{W_k, b_k}(g) + k·c_Z·ln n + C′ln n`
(Proposition Z4; §6 of `Z_REPORT.md`).  Take `k = k₁ + ⌈ln(g·n)/ln(1/λ_η)⌉` in Proposition A11: then
`n·g·λ_η^{k − k₁} ≤ 1` and `k = O(ln n)`.  ∎

Theorem 11.54 of the theory report has `exp(n·θ_hint(g) + o(n))` at extensive accuracies; this is
`exp(n·θ_hint(g) + O((ln n)²))`, against the hinted lower bound.  *The constant.*  The proof above
gives a constant of order `c_Z·hL/η` with `η` of the order of `m ≈ ½θ_hint″(0)g²`, i.e. **of order `1/g²`**
as `g → 0` (the referee: `≈ 300·c_Z·(h/g)²` at `u = 1`); it does not track it.  The true number
of levels is smaller: at a fixed rate the defect decays like `κ_g^k`,
`κ_g = 1 − g/(J(t_g) + (1 − t_g)g)` with `J′(t_g) = g` — the contraction factor of Lemma A9 at the
intercept that matters, `B = J(t_g)` — which is `e^{−g/h}` to first order in `g` (`0.364` against
`0.368` at `g = h`, `0.116` against `0.135` at `g = 2h`; the referee) and would give `C ≈ (h/g)·c_Z`: a
constant of order `1/g` is the heuristic value (the profile of `R_REPORT.md` §8a has the defect
`≈ 2θ_hint″(0)·g²·e^{−kg/h}` for `kg/h ≫ 1`), not what is proved.  In between — accuracies `x̂` with
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

## A9a. Small rates: a constant of order `1/g`, and the accuracies between `√n` and `n`  *(added after the first review; refereed since — `Z_A6_REVIEW.md`, second note at the head)*

The proof of Proposition A11 loses in two places when `g` is small: it bounds `J′(t₁(B))` from
below by `η/L`, and it asks the geometric term to be below a third of the margin.  Neither
is needed.  *Hypotheses:* those of A9 and (H1); `ϑ := θ_hint″(0) = −1/J″(L)`.

**Lemma A9′ [P].**  *There is `η₀ > 0` such that for `0 < η ≤ η₀`, `B ≤ h − η` and `i ≥ 0`:*
`t₁(B) − p_i(B) ≤ t₁(B)·μ_η^i`, *`μ_η := h/(h + ½√(η/ϑ))`.*
*Proof.*  By (H1), `J(t) = h − (L − t)²/(2ϑ) + o((L − t)²)`: there is `r₀ > 0` with `J(t) ≤ h − (L − t)²/(4ϑ)` on
`[L − r₀, L]`; put `η₀ := h − J(L − r₀)`.  For `η ≤ η₀`, `t₁(h − η) ≥ L − r₀`, so `η ≥ (L − t₁(h − η))²/(4ϑ)`, i.e.
`L − t₁(h − η) ≤ 2√(ϑη)`.  For `B ≤ h − η`: `J′(t₁(B)) ≥ J′(t₁(h − η)) ≥ η/(L − t₁(h − η)) ≥ ½√(η/ϑ)` (`J′` is
nonincreasing; concavity).  The proof of Lemma A9 with this bound in place of `η/L`.  ∎

**Proposition A11′ [P].**  *There are `g₀ > 0` and `C₃` such that for every `0 < g ≤ g₀` there is
`k₂(g) ≤ C₃/g` with*

    M_{W_k, b_k}(g)  ≤  θ_hint(g) + g·(1 + g/(48h))^{−(k − k₂(g))}        for all k ≥ k₂(g).

*Proof.*  `m(g) := θ_hint(g) − (h − Lg) = ½ϑg² + o(g²)`; let `g₀` be such that `m(g) ≥ ϑg²/4`, `η_g := ϑg²/576 ≤ η₀`
and `g ≤ 48h` on `(0, g₀]`.  Then `(L − t₁(h − η_g))·g ≤ 2√(ϑη_g)·g = ϑg²/12 ≤ m/3`.  Let `k₂(g)` be the first `k`
with `b_k − h < η_g(1 − L)/L` and `b_k − h ≤ ϑg²/12`; since `sup_k k²(b_k − h) < ∞` (Proposition A7),
`k₂(g) ≤ C₃/g`.  For `k ≥ k₂(g)`, `i := k − k₂(g)`: Lemma A10 gives `W_k ≥ p_{i+1}` on `[0, h − η_g]`, and Lemma A9′
`p_{i+1} ≥ t₁ − μ^i`, `μ := μ_{η_g} = (1 + g/(48h))^{−1}`.  Lines with `B ≤ h − η_g`: `B − W_k(B)g ≤ θ_hint(g) + gμ^i`,
as in A11.  Lines with `h − η_g ≤ B ≤ b_k`: `B − W_k(B)g ≤ (h − Lg) + (b_k − h) + (L − t₁(h − η_g))g + gμ^i`
`≤ θ_hint(g) − m/3 + gμ^i` — below `θ_hint(g) + gμ^i` whatever the size of the last term.  ∎

**Theorem Z‴ (small rates, and the accuracies between `√n` and `n`) [P, conditional as Theorem Z′].**
*Fix `u`, `δ`.  There are `g₀ > 0`, `n₀`, `C` and `C₄` such that for all `n ≥ n₀` and all rates
`C₄·ln n/√n ≤ g ≤ g₀`*

    ln N(n; g·n, δ)  ≤  n·θ_hint(g) + (C/g)·(ln n)² ;

*equivalently, for accuracies `C₄·√n·ln n ≤ x̂ ≤ g₀·n`:  `ln N(n; x̂, δ) ≤ n·θ_hint(x̂/n) + C·(n/x̂)·(ln n)²`.*
*Proof.*  Take `k = k₂(g) + ⌈ln(g·n)/ln(1 + g/(48h))⌉` in Proposition A11′: `n·g·μ^{k − k₂} ≤ 1`, and
`ln(1 + x) ≥ x/2` on `[0, 1]` gives `k ≤ C₃/g + 96h·ln(gn)/g + 1 ≤ (C₅/g)·ln n`.  The type of the `k`-th family
at the accuracy `x̂ = g·n` (Proposition Z4 holds at every accuracy above `𝒳`, with error
functions that do not depend on the accuracy — the referee, on Theorem Z″) costs at most
`n·M_{W_k, b_k}(g) + k·c_Z·ln n + C′ ln n`, for `k ≤ n^{1/2}`: that is the lower limit on `g`.  ∎

So the constant of Theorem Z″ is of order `1/g` as `g → 0` — the order of the heuristic, with
`48h` where the profile has `h` — and **the error term is at most `n^{1/3}(ln n)^{2/3}` from
`x̂ ≈ n^{2/3}(ln n)^{4/3}` on**.  What is proved for the accuracies below that: `ln N(n; x̂, δ) ≤ ln N(n; 1, δ)`
`≤ n·θ_hint(x̂/n) + L·x̂ + O(n^{1/3}(ln n)^{2/3})` (Theorem Z′ and `h − θ_hint(g) ≤ L·g`), so the two bounds
together leave an error of up to order `√n·ln n` around `x̂ ≈ √n·ln n`.  The numerical
observation of A8′ below would remove it.

*A8′ (an observation, not proved) [N].*  For the envelope sequence of the cube,
`sup_{g ≥ 0} [M_{W_k, b_k}(g) − θ_hint(g)] = b_k − h` at every level computed (`k ≤ 60`, `u = 1, 2`;
`z8_defect_profile.py`): the defect is largest at accuracy zero.  By duality this says that
`W_k(B) ≥ t₁(B − (b_k − h))` on `[0, b_k]`: the envelope curve lies above the fixed-point curve
shifted to the right by `b_k − h`.  If it holds for all `k`, then
`ln N(n; x̂, δ) ≤ n·θ_hint(x̂/n) + O(n^{1/3}(ln n)^{2/3})` uniformly in the accuracy.  The induction
"the image of the shifted curve dominates the next shifted curve" needs
`(b_k − h)²/(ϑh²) ≥ b_k − b_{k+1}` near the top and fails from about ten levels on; the least
margin is in fact near the *bottom* of the curves (`DEAD_ENDS.md` D68 item 7).

## A10. What is not proved

* Everything listed in §9 of `Z_REPORT.md`.
* The addendum has been refereed internally (see its head); A6a and A6b were added
  afterwards and were refereed on 2026-11-27 (`Z_A6_REVIEW.md`: one closed form wrong as first stated, corrected).  The tops in the table of A6 are floating point; those
  of A6b are certified given Lemma A1 and Proposition A8.
* The envelope sequence is **not** the level recursion: `τ₂ = b₂`, and `τ_j < b_j` from the third
  level on (A6a; numerically).  A step for families that also carries the inner tolerance
  — which is what the recursion gains — is not written.
* In A9 the constant `C(u, g)` is not tracked beyond its order (A9a: `1/g` for small rates;
  refereed since); for accuracies between about `n^{1/3}(ln n)^{2/3}` and `n^{2/3}(ln n)^{4/3}` the error term is not shown to be `O(n^{1/3}(ln n)^{2/3})`
  (A9a: it would follow from the observation A8′); and the matching lower bound at
  extensive accuracies is the hinted one of the theory report (Theorems 11.25(a), 11.54),
  not re-derived here.
