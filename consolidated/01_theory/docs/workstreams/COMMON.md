# MetricChain — shared context for independent research workstreams

You are an independent researcher on one workstream of a larger program.  Read this file first,
then your own brief.  You have real intellectual freedom inside your workstream: if you find a
more important question than the ones listed, pursue it and say why.

## Program and scope
MetricChain: foundational mathematics, formal guarantees and computational paradigms for
fixed-sequence articulated chain molecules (certified energy minimisation, certified partition
functions, realizability).  **Scope: foundational mathematics, theoretical physics,
general-purpose computational methods, fixed-sequence structural characterisation, synthetic
mathematical evaluation.  Out of scope: biological sequence engineering, target-specific
functional optimisation, experimental execution** — do not go there.

Repository (read-only for you): /home/user/MetricChain
* `docs/THEORY_REPORT.md` — the results.  The part relevant to you is §§10–12 ("certification
  geometry"), especially §11.2–11.6 and §11.10, and §12 (open questions).
* `docs/DEAD_ENDS.md` — refuted conjectures and withdrawn claims (D21–D34 are recent).
* `docs/reviews/R1_referee_report.md`, `R2_referee_report.md` — two independent referee reports.
* `docs/prior_art/L4…L7` — literature checks with search logs.
* `proofs/Frontiers/*.lean` — Lean 4 + Mathlib formalisation (e.g. `CertificationGeometry.lean`,
  `ExponentialWeights.lean`, `ProductRates.lean`, `QueryLowerBound.lean`, `SoftGapBounds.lean`).
* `experiments/` — Python falsification harness and benchmarks.

## Setting and notation (certification under envelope uncertainty)
* `X` finite configuration space; energy `E = f + g`: `f` known ("white box"), `g` an unknown
  residual, known only to lie in the **admissible class** `{g : g(x) − g(y) ≤ d(x,y) ∀x,y}` for a
  known **envelope** `d` (a quasi-metric: zero diagonal, triangle inequality, possibly
  asymmetric).  An algorithm may evaluate `g` at points of its choice; cost = number of
  evaluations.  On product spaces `X = ∏ σ_i` the standard envelope is weighted Hamming,
  `d(x,y) = Σ_i c_i [x_i ≠ y_i]`.
* **Slack** `s(a,y) = d(a,y) − g(a) + g(y) ≥ 0` (a quasi-metric).  `gap(y) = E(y) − min E`.
  After evaluating `g` on `A`: lower/upper McShane envelopes `L_A = g − s(A,·)`, `U_A = g + s(·,A)`.
* **Certificates = coverings.**  `A` certifies `min E` to within `ε` iff every `y` has an
  evaluated point within slack radius `gap(y) + ε` (plus a minimiser).  `N_cov` = least size.
  The same number is the instance-wise cost of the best deterministic algorithm that is correct
  on the whole class (machine-checked).
* **Lower bounds** (LP duality / exponential weights):
  `e^{−tε} Σ_y v(y) ≤ |A| · max_a Σ_y v(y) e^{−t(s(a,y) − gap(y))}` for all `t ≥ 0`, `v ≥ 0`.
  Every randomised algorithm with error probability `δ` pays `(1 − 2δ)` times each such bound.
* **Product landscapes** (`f`, `g` additive over sites, `|γ_i(a) − γ_i(b)| ≤ κ c_i`, `κ < 1`): one
  evaluation suffices iff every site is *sharp* (`c_i ≤` every excitation energy of the known
  part); otherwise `N_cov = exp(n R* + o(n))`, `R* = max_P R(P; s, E_P[gap])` (a rate–distortion
  function, via type covering).  Binary site with excitation `e < c`, `ρ = e/c`:
  `R* = max_μ [h(μ) − h(ρμ)]` (0.1882 at ρ = 1/2).
* **Finite temperature** (`π` = Gibbs measure of `E` at inverse temperature `β`):
  deterministic certificates of `ln Z` are quantisers of `π`; exponent
  `R_β = max_Q R(Q; s, KL(Q‖π)/β)` for accuracies that are not exponentially small (a corollary
  of Merhav 2011).
* **Dips and soft gaps** (newest results).  A *dip* of depth `c` at `y`:
  `a ↦ min(g(a), g(y) − c + d(a,y))`; it is admissible and differs from `g` exactly on the open
  slack ball `{a : s(a,y) < c}`.  It multiplies `Z` by `E_π e^{β(c − s(Y,y))₊} ≥ e^{βc − Λ(y)}` with the
  **soft gap** `Λ(y) = ln Z(f+g) − ln Z(f+U_y)`, `U_y(x) = g(y) + d(x,y)` (so
  `e^{−Λ(y)} = E_{a∼π} e^{−β s(a,y)}`; `0 ≤ Λ(y) ≤ −ln π(y)`; `Λ` is `βs`-Lipschitz).
  - *Lower bound, every algorithm* (also randomised): queries must reach within slack
    `(Λ(y)+ε)/β` of every `y` (packing form; on product spaces exponent
    `R^rand_β(ε₁) = max_P R(P; s, (E_P[Λ₁]+ε₁)/β)`, `Λ₁(b) = −ln Σ_a π(a) e^{−βs(a,b)}`).
  - *Upper bound, randomised with a hint* ("spot-check": sample points from a distribution `q`,
    compare the residual with a claimed model): with `q = ½π + ½·w/W`,
    `w(z) = π(z)((1+η)e^{Λ(z)} − 1)`, `η = e^{ε/2} − 1`: `N ≈ 2 ln(1/δ) E_π[e^{Λ}]/(1 − e^{−ε/2})`
    evaluations suffice (machine-checked; exponent on product spaces
    `U_β = ln Σ_b π(b) e^{Λ₁(b)}`).
  - *Cube* (`X = {0,1}ⁿ`, `f = 0`, `d = c·`Hamming, `u = βc`): deterministic cost `≈ 2ⁿ`;
    randomised lower bound exponent `ln 2 − h(ρ₀)`, `ρ₀ = ln(2/(1+e^{−u}))/u` (attained with a
    hint, by Harper's theorem); sharp accuracy threshold `ε = n ln cosh(u/2)`: above it a bounded
    number of random evaluations suffices, below it every algorithm is exponential.
  - *Open (the main conjecture)*: on product spaces, are single dips extremal at the exponential
    scale, i.e. is the randomised exponent exactly `R^rand_β`?  Known: true for the uniform cube;
    false for general finite instances (unions of shallow dips; `DEAD_ENDS.md` D34); the proved
    bracket is `R^rand_β ≤ exponent ≤ min(R_β, U_β)`.
* **Other results**: minimal certificates contain minimum dominating sets (NP-hard); best-first
  (Piyavskii–Shubert) search needs at most `|C|+1` evaluations for every cover `C` at radii shrunk
  by `θ = (1−κ)/(4(1+κ))` (no instance-optimality without shrinking: "hub" family); second-order
  classes (bounded mixed second differences `c_ij`): a star of `n(k−1)+1` evaluations gives the
  exact pairwise envelope `g_star ∓ Σ_{i<j changed} c_ij`, useful only under weak coupling.
* Two referees judged the cluster "a coherent note, not a theorem-driven paper": tools are
  standard (type covering, Chernoff/Hölder, LP duality), proofs short.  We are looking for
  what would make it deeper — or for a different, better direction.

## Rules (hard)
1. **Do not modify anything inside /home/user/MetricChain.**  Work only in your own directory
   (given in your brief) under
   <session scratch>/ws/ .
2. Do not run `lake build`, `lake update`, `lake clean`, `scripts/audit_all.sh`, or any git
   command that changes state.  Lean is optional for you; if you want to machine-check a lemma,
   put a scratch file in your directory and run
   `export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH"; cd /home/user/MetricChain; lake env lean <absolute path>`
   (it competes for 4 CPU cores with other workstreams — use sparingly; mathematics and Python
   numerics come first).
3. **Do not spawn further agents.**  Web search/fetch is allowed and encouraged for prior art;
   keep a short search log and say what you actually read (abstract / full text / summary).
4. Standards: falsify numerically before you believe (own Python code; numpy/scipy available);
   state hypotheses precisely; give proofs or explicit counterexamples; **negative results are
   welcome and must be reported**; distinguish clearly *known* (cite), *routine*, *apparently
   new*.  No forced claims.  Record dead ends.
5. Keep all scripts and outputs in your directory.  Write your full findings to `REPORT.md`
   there (as long as needed, well organised: 1. verdicts in one paragraph; 2. precise
   statements with proofs/counterexamples; 3. numerics (what, sizes, results); 4. prior art with
   search log; 5. what you did not settle; 6. the three most promising next steps).
6. Your **final message** must be short (at most about 600 words): the headline verdicts, the
   strongest new statement (precisely), the most important negative finding, and the absolute
   path of `REPORT.md`.  Details stay in the file.
