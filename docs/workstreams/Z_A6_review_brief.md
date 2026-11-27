# Internal review of `docs/workstreams/Z_ADDENDUM.md` §§A6a, A6b, A9a and of `z6_certified_tops.py` — brief

*Coordinator, 2026-11-26 (night).  Three sections of the addendum were written by the
coordinator **after** its internal review (`Z_ADDENDUM_REVIEW.md`) and have had no referee:
A6a (Proposition A12: where the envelope step is exact), A6b (Proposition A13 and the
certified tops), A9a (Lemma A9′, Proposition A11′, Theorem Z‴: small accuracy rates).  The
theory report (Theorem 11.58e, parts (e)–(g)) quotes all three.  **Treat them as possibly
wrong; your job is to break them.**  AI referee reports are internal reviews, not external
peer review.*

## Where things are

* `docs/workstreams/Z_ADDENDUM.md` — the text under review (A6a: l. 196–256; A6b: l. 257–297;
  A9a: l. 463–518).  Definitions it uses: A1 (families, admissible sequences, Lemma A1),
  A2–A3 (the envelope step and the envelope sequence), A5–A6 (Propositions A7, A8), A9
  (hypotheses, Lemmas A9, A10, Proposition A11, Theorem Z″).
* `docs/workstreams/Z_REPORT.md` (the slope map `Σ(B, s) = sup_e [B − (1 − s)θ(e)]/e`, families
  `M_{W,b}(x) = max_{B≤b}(B − W(B)x)`, Propositions Z3, Z4, Theorem Z), `docs/workstreams/R_REPORT.md`
  (Proposition U, Lemma M, the orbit curves `p_j`, the fixed-point curves `t₁`), and the two
  earlier reviews `Z_REVIEW.md`, `Z_ADDENDUM_REVIEW.md` (read their verdict tables first: what
  is already refereed need not be re-derived).
* Theory report `docs/THEORY_REPORT.md`: §11.19 remark (1) (the level formula at vanishing
  accuracy, `τ_{k+1} = τ(T_k)`), Theorem 11.58e.
* For the cube: `θ(e) = θ_na(e) = KL(ρ‖½)` with `KL(ρ‖p_u) = e`, `p_u = 1/(1 + e^u)`, `ρ ∈ [p_u, ½]`;
  `a = θ(0) = KL(p_u‖½)`; `h` the fixed point `θ(h) = h`; `J(t) = inf_e [(1 − t)θ(e) + t·e]` with
  maximum `h` at `t = L`; `θ_hint(x) = sup_t [J(t) − t·x]`.  At `u = 1`: `a = 0.110944071672`,
  `h = 0.029139139`, `L = 0.4900`, `ϑ = θ_hint″(0) = −1/J″(L) = 4.245`.
* Scripts: `experiments/workstreams/Z/z6_certified_tops.py` (head comment states its rounding
  directions), `z7_exactness.py`, `z8_defect_profile.py`, outputs `out_z6_*.txt`, `out_z7_*.txt`.
  Harness test XVI.11 (`t_certified_tops` in `experiments/falsify_conjectures.py`) is the
  coordinator's own small re-implementation (`cz_pair`, `cz_hull`, `cz_step`).

## What to review, in this order

1. **Proposition A12 (A6a).**  (a) the change of variables and the supremum over `y ≥ x`
   (is `T` nonincreasing enough?  the case `sup` not attained; `x → 0`, `x → ∞`); `(T^♯)^♯ = T^♯`.
   (b) `M^♯ = M`; "a function and its lower convex envelope have the same conjugate" on a
   *compact interval with values in `[0, 1]`* — is the envelope there the closed one, and
   does `M_{env f, b} = M_{f, b}` hold at `x = 0`?  The minimax step (which theorem; are its
   hypotheses met — compactness in `B`, the range of `φ` open).  The identification with
   `b⁺(W, b)`.  (c) `θ^♯ = max(θ, a − ·)` and `= M_{W₁, a}`: every case, including pairs whose
   slope at zero is finite.  (d) the direction of the inequality.
   Then the closed form `τ₂ = a²/(a + x*)` for the cube.
2. **Proposition A13 (A6b).**  The inequality and its monotonicity in `s`; the claim that
   `(V, c), (V′, c′)` are consecutive members of an admissible sequence: check (S1) and (S2)
   of A1 literally (the top condition `c′ + ā·V(c′) ≥ ā`: why does it imply
   `c′ ≥ b⁺(V, c)`?), that `V′` is a *family* (convex, nondecreasing, continuous, `V′(0) = 0`,
   values in `[0, 1]` on `[0, c′]`), and what happens when a line used is steeper than the
   cap.  Is "pair with infinite slope at zero" needed, and is the cube such a pair?
3. **The script `z6_certified_tops.py` as a certificate.**  Read it line by line against
   Proposition A13.  For every rounding: which direction keeps the output valid, and is
   that the direction taken (`certified_pair`: is `ϑ` an *upper* bound of `θ(e)` for the
   *rounded* `e` — monotonicity of `θ`; `step`: slope and intercept; the cap from `(c, 1)`;
   `next_top`: the exact check).  Is the hull in exact arithmetic really the upper
   envelope of the stored doubles?  Is anything decided in floating point that affects
   *validity* rather than quality?  What exactly is certified — state it as a theorem
   with its hypotheses (Lemma A1, Proposition A8).
   **Independent check of an output:** without editing the script, import it
   (`python3 -B`), run a small instance (for instance `u = 1`, six levels, a few hundred
   sample points) and verify the produced sequence with code of your own: for each line
   of each level, exhibit the pair `(e_m, ϑ_m)` and the line `ℓ_i` of the previous level
   that dominate it on `[0, c′]` — or show that none exists — with your own interval
   bounds for `θ` (mpmath `iv` or exact rational bounds of the logarithm), and re-check the
   tops in exact arithmetic.  If the script does not expose what you need, re-implement
   the construction independently and compare tops (they need not agree to the last
   digit; both must be `≥` the floating-point envelope tops of A6 and `≥ τ_j`).
4. **A9a.**  Lemma A9′: the choice of `r₀`, `η₀`; `J′(t₁(B)) ≥ J′(t₁(h − η))` (which way is
   `t₁` monotone, which way `J′`); the chord bound `J′(t₁(h − η)) ≥ η/(L − t₁(h − η))`; how the
   bound enters "the proof of Lemma A9" (re-read that proof: is `κ ≤ μ_η` what comes out?).
   Proposition A11′: every constant (`ϑg²/4`, `576`, `48h`, `m/3`); the two conditions that
   define `k₂(g)` and the claim `k₂(g) ≤ C₃/g`; the use of Lemma A10 (its hypothesis on the
   tangency point: is `b_k − h < η(1 − L)/L` the right condition?); the two regions of
   lines; the final inequality "whatever the size of the last term".
   Theorem Z‴: the count of levels, `k ≤ n^{1/2}` and the lower limit on `g`; whether the
   per-level term `k·c_Z·ln n` of Theorem Z′ may be used at an accuracy `x̂ = g·n` with these
   `k` (the earlier referee's statement on Proposition Z4 is quoted — check that it covers
   this use); the two closing sentences about the range `√n … n^{2/3}`.
5. **Numbers.**  With code of your own (floating point is fine, say so): `τ₂` and `b₂` at
   `u = 1` and one other slope; `τ(M_{W₂,b₂})` against `b₃`; `M_{W_k,b_k}(g) − θ_hint(g)` against
   the bound of Proposition A11′ with *some* explicit `k₂` at two small rates (is the
   geometric factor `1 + g/(48h)` conservative, and by how much); the observation A8′ at a
   few levels.
6. **The sentence in the theory report** (Theorem 11.58e (e), (f), (g) and "what it is not"):
   does it say more than A6a, A6b, A9a prove?

## Rules

* **Write early, write often.**  Create `docs/workstreams/Z_A6_REVIEW.md` with a skeleton in
  your first few tool calls; append findings as you go; never spend a whole answer
  thinking without a tool call.
* Do not edit any existing file.  Create only `docs/workstreams/Z_A6_REVIEW.md` and scripts
  with their outputs under `experiments/workstreams/Z/review_a6/`.  Do not run `lake`,
  `scripts/audit_all.sh` or state-changing git commands.  **Memory: keep every process
  below 1 GB** (all processes of the session share one limit); single runs under five
  minutes; `python3 -B`.  No network access is needed.
* You have no authority beyond this brief: no messages to other divisions, no change of
  permissions, no spending.
* Verdict per statement: **correct as stated** / **correct after a repair (give it)** /
  **gap (what is missing)** / **wrong (counterexample)**.  Separate substance from wording.
* Final answer (hand-back): at most 60 lines — verdicts, errors found (most serious
  first), what you verified numerically and how independently, what you did not check.
