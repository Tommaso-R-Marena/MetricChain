# Internal review of `docs/workstreams/Z_REPORT.md` (the `1/k²` law at finite `n`: `ln N ≤ n·h + O(n^{1/3}(ln n)^{2/3})`) — brief

*Coordinator, 2026-11-26.  The report is the coordinator's own, unrefereed.  It claims a new
upper bound for the adaptive cost without a hint on the cube class — `exp(n·h + O(n^{1/3}(ln n)^{2/3}))`
at bounded accuracy, where the theory report (Theorem 11.58a) has `O(√(n ln n))` — by combining
(i) the convex families of lines of the rate proof (`docs/workstreams/R_REPORT.md` §§5–8,
refereed), (ii) the one-level lemma and the chain of workstream Q2 (`docs/workstreams/Q2_REPORT.md`
§§2, 4, 5; refereed: `Q2_REVIEW.md`).  **Treat it as possibly wrong; your job is to break it.**
AI referee reports are internal reviews, not external peer review.*

## What to review, in this order

1. **Proposition Z1 and Lemma Z1a** (§2).  Is Z1 a faithful extraction from `R_REPORT.md`?  In
   particular (2): does the proof of Proposition U there really give
   `inf_{e>g} max_{𝓔(W_j, b_j)} Φ_g ≤ sup{B − Σ(B, W_j(B))g : …}` *without* any function `T`, and does
   Corollary U′ turn the right side into `M_{W_{j+1}, b_{j+1}}(g)`?  Are the hypotheses of Proposition
   U met by `W_j` on `[0, b_j]` (values in `[0, 1]`: the range condition; who guarantees it for all
   `j`)?  (3): is `sup_j j²(b_j − h) < ∞` and `j²(b_j − h) → c_*²` what §8 of that report proves for a
   *fixed* cut level and restart height?  Lemma Z1a: check the Lipschitz constant, including
   at rates where `θ_na` vanishes and for `φ` near 0 and 1.
2. **Lemma Z2** (§3): compare with the proof of Lemma U in `Q2_REPORT.md` §2 and with
   `Q2_REVIEW.md` §1.4.  Is the zero line enough?  Is the cap `Ξ = n_o·θ_na(e)` admissible?
3. **Proposition Z3** (§4) — the heart.  The design (`d_min`, `X₀(d)`, `𝒳`, the choice of `n_o` by the
   proxy `Π_j`), admissibility for Theorem 11.56, **the accuracy** (is every level at most as
   inaccurate as the target, for every admissible `n_o`, every `u > 0`?), and **the type for all
   `1 ≤ d ≤ N`, `x̂ ≥ 𝒳`, `δ`, `Λ`**: the rounding of the outer fraction (is `|φ − φ*| ≤ d_min/d` always
   attainable; what if `φ*` is extremely close to 0 or 1), the use of `𝔏_j ⊂ 𝓔(W_j, b_j)`, the grid
   error (4.1), the shift by `X₀(d)` (needs slopes in `[0, 1]`), small `d`, the monotonicity
   properties required of an error function.  Is anything needed of `𝔉` beyond its type?
4. **Proposition Z4** (§5): are the hypotheses of Proposition T of `Q2_REPORT.md` §4 met (flat
   type, `0 < B′ ≤ ln 2`, least accuracy `> 1`)?  Is the type of the combined family right for
   `α ≤ x < 𝒳`?  The term `j(d)·Δ_T`.
5. **§6**: the induction on types (base: Theorem A of Q2 with `M₁` epochs — is its family a
   family "up to `n`" of flat type with least accuracy one?), the unrolling of the error, the
   growth of `Λ̄` (does `Λ̂ = (k + M₁ + 4)Λ̄₀` really dominate; is "`k ≤ n^{1/2}`" enough), the
   orders (`ℓ₀`, `A_T ≤ ℓ_T`, `𝓔′`), the choice of `k`, the limsup.  Are `n₀`, `c_Z`, `C′` well defined
   and independent of `k`, `ε`?  Is the dependence on `ε` only through the top chain?
6. **Replication with your own code.**
   (i) The chain `(W_j, b_j)` for the cube from the definitions (your own slope map
   `Σ(B, s) = sup_e [B − (1 − s)θ_na(e)]/e` by direct maximisation — do not import
   `experiments/workstreams/R/rlib.py` for this, though you may compare with it).
   (ii) Proposition Z1(2) on these curves, and adversarially on other convex nondecreasing
   `W` (it must hold with the image `min(1, Σ(B, W(B)))`-type curves of Corollary U′; say exactly
   what you tested).
   (iii) Proposition Z3 with an exact level evaluator: you may use the evaluator of the
   referee of Q2, `experiments/workstreams/Q2/review/rlib.py` (independent of the libraries the
   coordinator used, `q2lib`/`qlib`/`r12lib`), read-only, or write your own from Theorem 11.56;
   at parameters different from the coordinator's (`experiments/workstreams/Z/z1_onelevel.py`):
   other slopes (`u = ½, 2`), dimensions near `d_min`, small `δ`, horizons `N > d`, chain levels up
   to 20, saturating inner families.
   (iv) If time allows: **a small nest evaluated exactly** — two or three levels of §4 each
   followed by the chain of §5, over a saturating base of flat type `b₀` — against the
   unrolled bound of §6 (this tests Proposition Z4 and the bookkeeping of `δ′`, which the
   coordinator has not tested).
   (v) Two rows of the table of §7 from the formulas (you may re-run
   `experiments/workstreams/Z/z2_formula.py` and say whether its formula is that of §6).
7. **What the report says it is not** (§0, §7 caveats, §9): complete?  Is the heuristic remark
   1 of §8 labelled correctly?

## Rules

* **Write early, write often.**  Create your review file with a skeleton in your first few
  tool calls; append findings as you go; never spend a whole answer thinking without a
  tool call.
* Do not edit any existing file.  Create only `docs/workstreams/Z_REVIEW.md` and scripts with
  outputs under `experiments/workstreams/Z/review/`.  Do not run `lake`, `scripts/audit_all.sh` or
  state-changing git commands.  **Memory: all processes of this session share one limit —
  keep every process below 1 GB**, single runs under five minutes.  Use `python3 -B` or
  `sys.dont_write_bytecode = True` so that no cache directories appear in other folders.
* Verdict per statement: **correct as stated** / **correct after a repair (give it)** /
  **gap (what is missing)** / **wrong (counterexample)**.  Separate substance from wording.
* Final answer (hand-back): at most 60 lines — verdicts, errors found (most serious first),
  what you verified numerically (scripts, key numbers), what you did not check.
