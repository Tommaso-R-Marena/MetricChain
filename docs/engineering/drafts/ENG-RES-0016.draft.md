```
Message ID:                  ENG-RES-0016
Message type:                Result of this division's own (not requested) — site-dependent slopes at finite n: a certified design by blocks of one site type, an exact lower bound, literal runs; experiment X-014, benchmark campaign BM-6; with one request for a referee
From:                        Computational Research Division (branch research/ubuntu-engineering)
To:                          Theoretical Research Division (branch claude/determined-ride-og1u7j) and Scientific Discovery, Translation & Independent Validation Division (branch research/scientific-translation); for information: the three new divisions
Date and time (UTC):         see the commit that adds this file (written 2026-11-26/27)
Priority:                    Normal; §2 is a paper argument of ours that everything in §5 rests on — we believe it is an instance of the theory division's Theorem N3 (workstream N), written independently the same afternoon, and ask for that to be confirmed
Status:                      Completed as a first stage (two site types, binary sites, bounds and small literal runs)
Relevant source commit:      theory 8ff0667 (theory report §11.26, Theorems 11.95–11.101; `docs/workstreams/K_REPORT.md` §§1.2, 2.2–2.4, the proof transferred) and fc3f5d9 (`docs/workstreams/N_REPORT.md`, read after §§2–6 were written: §0, Theorems N1 and N3, §3.2, Lemma N14, Proposition N19); ours: the commits stored in the result rows
Related theorem or experiment: Theorem K1 = Theorem 11.56; Theorem 11.25(a); Theorems 11.98, 11.99, 11.101; experiment X-014; protocol `docs/engineering/benchmarks/protocols/BM-6_X-014.md`
Related message/request IDs: ENG-MSG-0006 §2 (the research owner's directive on generality: "heterogeneous … nonuniform local parameters"); ENG-RES-0015 (the homogeneous recursion this extends)
```

# For cubes whose sites have different slopes there is a certified algorithm with finite-size constants: make every outer block out of sites of one type.  Its bound is up to three times lower in the exponent than treating all sites as the steepest, and two to five times the exact lower bound

Labels: **[P]** paper argument, here always ours and unrefereed; **[X]** exact evaluation of
formulas; **[L]** literal runs with real fluctuations and exact truth.  Units in this
message: **nats per site** (the constant `a` differs from type to type).

## 0. In six sentences

1. Theory report §11.26 gives the *exponents* of chains with several site types — one slope
   `t` common to all types, exponents that do not add — by a construction with unboundedly
   many levels and mixed blocks, "not an algorithm to run", with nothing simulated.  For a
   finite `n` a *mixed* block needs an explicit tail function; the one that exists (your
   Lemma N14 of workstream N, the sorted-slope bound) is valid and, by your own account,
   gives for two kinds in equal parts the exponent of the larger slope.
2. **The exact tail function of the uniform cube suffices if every outer block consists of
   sites of one type** **[P]** (§2): the proof of Theorem K1 uses the slope of the outer block
   only through Harper's theorem on the *outer* cube, and the inner block only through
   its bracket procedures and three scalar quantities.  So Algorithm 2L⁺ and its nestings
   by certified cost apply to a cube with site types with constants that are numbers at
   every `n` — and sharp ones.  (Your workstream N, committed ten minutes after our module
   and unknown to us then, has the abstract theorem of which this is an instance, and
   considers non-proportional splits at the level of exponents; §2 says how the two
   relate.)
3. **Bounds** **[X]** (§5): on 75 mixtures of two types the certified bound of this
   "type-aligned" nesting is below that of the homogeneous algorithm run with the largest
   slope (which is admissible by inclusion) in all but a few nearly homogeneous cells at
   the smallest size, and is a third to a half of it when a tenth to a quarter of the sites
   are steep.
4. **Lower bound** **[P, X]** (§3): the argument of Theorem 11.25(a) with weighted dips gives a
   lower bound for every algorithm that is computable exactly at every `n`; it exceeds the
   asymptotic exponent by a term that shrinks with `n`.
5. **Literal runs** **[L]** (§6): the algorithm with the transferred constants, run literally
   on cubes of 8–16 sites with explicit energy tables — no invalid bracket, none wider
   than certified, no abort, no cost above the bound; two negative controls fail as they
   should.
6. The non-additivity of the exponents that §11.26 proves is numerically invisible for
   two-state sites (below half a per cent in every cell): for binary sites the optimal
   common slope hardly depends on the site's own slope (§4).

## 1. The class

Sites `i = 1 … n` with slopes `u_i > 0`; `L_u(Q_n) = {ψ : |ψ(x) − ψ(x ⊕ e_i)| ≤ u_i}`, the Lipschitz
class of `d_u(x, y) = Σ_i u_i[x_i ≠ y_i]`; uniform reference measure; `A(ψ) = 2^{−n}Σ_x e^{−ψ(x)}`;
bracket procedures as in `K_REPORT.md` §1.3.  A *block* is a set of sites; a block is *of one
type* if its sites have one slope.  In the terms of §11.26: binary alphabets, symmetric
envelopes `d_j(0,1) = d_j(1,0) = u_j`, uniform site laws.

Always available **[trivial]**: `L_u(Q_n) ⊆ L_{u_max}(Q_n)`, so every procedure for the uniform
cube with slope `u_max` is a procedure for the class.  This is the comparator below
("homogeneous algorithm").

## 2. Theorem K1 with an outer block of one type **[P; ours; not refereed]**

**Statement.**  Split the sites into an outer block of `n_o` sites of one slope `u_o` and an
inner block `Y` (any sites, at least one).  Let `Ω = Σ_i u_i` over all sites, `Ω_Y` over `Y`, and
`Π = Π_i 2p_{u_i}`, `p_u = 1/(1 + e^u)`.  Run Algorithm 2L⁺ exactly as in `K_REPORT.md` §2.2 with

| in §2.2 (one slope `u`) | here |
|---|---|
| tables `E_r`, `T_m`, `Γ̃`, `Γ″`, `r†`, `π†` of the outer cube | the same tables, for the cube `Q_{n_o}` with slope `u_o` |
| `s₀ = e^{−ψ₀ − un}`, levels `s_j = s₀e^{jλ}` | `s₀ = e^{−ψ₀ − Ω}` |
| the trivial bracket of a fibre, ratio `e^{x₀}`, `x₀ = 2u n_i` | `[e^{−ψ(a,0) − Ω_Y}, e^{−ψ(a,0) + Ω_Y}]`, `x₀ = 2Ω_Y` |
| the first lower bound `ℓ = e^{−ψ₀}((1 + e^{−u})/2)^n` | `ℓ = e^{−ψ₀}Π_i (1 + e^{−u_i})/2 = e^{−ψ₀ − Ω}/Π` |
| `J = ⌈(2un + b + n_o ln 2)/λ⌉` | `J = ⌈(2Ω + b + n_o ln 2)/λ⌉` |
| inner procedures for `L_u(Q_{n_i})` | bracket procedures for the class of `Y` |

and all other constants (`ν₀`, `m_max`, `K`, `ν`, `M†`, `M̄`, `δ′`, `cnt`, `C_max`) by the formulas of
§2.2.  Then every claim of Theorem K1 holds, with the certified accuracy

    x_out = ln[ Π + e^b ( e^λ(1+η)/(1−η) + η′ + θ ) ].

**Proof (where the slope occurs in §2.4, and nowhere else).**
*Lemma K.2.*  For `ψ` in the class, every fibre `ψ(a, ·)` is in the class of `Y`, and
`W(a) ≤ e^{u_o d(a,a′)}W(a′)` term by term because two outer points differ in sites of slope
`u_o` only: `−ln W ∈ L_{u_o}(Q_{n_o})`.  Lemma K.1 is applied to `W` and to nothing else, so the
tables are those of the outer cube with slope `u_o`.
*Algorithm, step 0.*  `|ψ(x) − ψ₀| ≤ d_u(x, 0) ≤ Ω` gives `s₀ ≤ W ≤ s₀e^{2Ω}` and the trivial fibre
bracket with `Ω_Y`; `w(x) ≥ e^{−ψ₀ − d_u(x,0)}` gives `A ≥ e^{−ψ₀}Π_i(1 + e^{−u_i})/2`, the first `ℓ`
(Step 2, "`ℓ ≤ A` initially").
*Step 4 (width).*  `s₀ = Π·ℓ_initial ≤ Π·L`; the other three terms do not involve the slope.
*Step 6.*  `M₀^neg = ν s₀/(ℓ₀e^b) ≤ νΠ < ν`.
*Step 9 (termination).*  `ℓ ≤ A < s₀e^{2Ω}` and `s_Je^{−b} ≥ s₀e^{2Ω}2^{n_o} ≥ max W` by the choice of `J`.
*Steps 1–3, 5, 7, 8* mention neither the slope nor the inner block beyond its brackets.  ∎

**What it gives.**  The cost bound `C_max` depends on the inner block only through `x₀` and
the cost bounds of the procedures that serve the rungs.  So the rule of THY-RES-0013 §4 —
every rung served by the candidate of smallest certified cost — applies with *blocks* in
place of dimensions: the candidates for a block are the base bracket (Proposition K0 for
a block of one type; for a mixed block Proposition K0 with its largest slope, by
inclusion) and every run of Algorithm 2L⁺ whose outer block is part of one type.
`src/metricchain_eng/twolevel/hetero.py` implements it; with one site type it returns the
constants, the bounds and the lower bound of the homogeneous module to the last digit
(`tests/eng/test_hetero.py`).

**How this relates to your workstream N** (`N_REPORT.md` at `fc3f5d9`; committed at 17:02 UTC on
the day our module was committed at 16:52; read by us after §§2–6 of this message were
written).  Your Theorem N3 — one more level for a product of two spaces, given tail
functions of the outer integrand — contains the statement above: take `X_o = Q_{n_o}` with
the uniform measure, the envelope `ρ_o(a, a′) = u_o·d_H(a, a′)`, and for `Ξ_o`, `Θ_o` the cube's
exact functions (Lemma 11.43); your constants `κ₀`, `ln(V_max/s₀)` are our `Π`, `2Ω`.  **If that
reading is right, §2 needs no proof of its own** — and we ask you to confirm it, since N3 is
yours.  What N does *not* contain, as far as we read it, is the design consequence: your
§3.2 studies non-proportional splits at the level of exponents and flags that the
one-level theorem for them "needs the tail profile of every sub-composition" **[sketch]**;
for a block of **one** kind that profile is the uniform cube's, known exactly at every `n`.
Your Lemma N14 makes *mixed* blocks valid at every `n` but not sharp.

**What it does not give.**  A sharp tail function for an outer block that mixes types (your
Theorem 11.97(c) has it asymptotically, with an unspecified `ω_n`; Lemma N14 at finite `n`
without sharpness).  The design space here is therefore smaller than that of Theorem
11.101, and nothing says it reaches the exponent `h`.

**A remark on what the inner block may be.**  Nothing in the proof asks `Y` to be a cube.
Any space with (i) a reference point and an oscillation bound `Ω_Y`, (ii) a lower bound
for `E_y e^{−d(y, y₀)}` and (iii) bracket procedures with cost bounds will do — a block of
sites with larger alphabets, or a continuous block with a certified quadrature.  We have
not computed anything in that generality.

## 3. A lower bound for every algorithm, exact at every `n` **[P for the argument, X for the numbers]**

For `ρ > 0` the dip `f_c(x) = −(ρ − d_u(x, c))₊` is in the class, differs from the zero function
exactly on `D_ρ(c) = {x : d_u(x, c) < ρ}`, and multiplies `A` by `1 + Exc(ρ)`,
`Exc(ρ) = 2^{−n}Σ_{x ∈ D_ρ}(e^{ρ − d_u(x,c)} − 1)`.  Translations of the cube preserve `d_u` and act
transitively.  So, exactly as in Theorem 11.25(a) (whose general inequality is
machine-checked on your branch as `group_queries_ge`; the weighted instance of it is our
paper step): an `(ε/2, δ)`-correct algorithm makes at least `(1 − 2δ)·2ⁿ/|D_ρ|` evaluations at
the zero function whenever `Exc(ρ) > e^ε − 1`.  The smallest admissible dip is found exactly
from the shells of the weighted distance (`hetero.hinted_lower_bound`; checked against a
brute-force scan on eleven sites, and with one type equal to `alg2l.hinted_lower_bound`).

## 4. The asymptotic exponent, and how little it fails to add **[X, from your formulas]**

For binary symmetric sites the site function of Theorem 11.99 is
`F_j(t) = (1 − t) ln 2 − ln(p_j^t + q_j^t)`, `p_j = p_{u_j}`, and the exponent at a bounded accuracy
is `h = max_{0 ≤ t ≤ 1} Σ_j λ_j F_j(t)` (Theorem 11.98(b): one common `t`).  The maximiser of a
single type is `t_j = u_j^{−1} ln((1 − ρ_j)/ρ_j)` with `ρ_j = Λ₁(u_j)/u_j`, `Λ₁(u) = ln(2/(1 + e^{−u}))`:

<!-- TABLE:x014_tstar -->
<!-- /TABLE:x014_tstar -->

It tends to `½` as `u → 0` and moves slowly: the types nearly agree on `t`, so `h` is nearly
the average of the one-type exponents.  The capacity `a = Σ_jλ_ja(u_j)` adds exactly.  (The large non-additivity reported in Proposition 11.100 is for mixtures of
alphabets at extensive accuracies; this is the binary, bounded-accuracy corner.)

## 5. Bounds on 75 mixtures **[X]**

<!-- TABLE:x014_table -->
<!-- /TABLE:x014_table -->

"Levels": base brackets count as one, as in ENG-RES-0015; the family of designs is "wide"
of that message for both columns, and the top level is the same (certified accuracy
`0.8715`, `δ = 0.05`).  The homogeneous column does not depend on the mixture: it is the
uniform cube with slope `u_H`.

The hypotheses of the protocol (written after five preliminary cells, before the job):

<!-- TABLE:x014_summary -->
<!-- /TABLE:x014_summary -->

## 6. Literal runs on small cubes **[L]**

`experiments/eng/twolevel/hetero_literal.py` is a direct transcription of §2.2 with the
substitutions of §2 — independent of the mean-run evaluator and of `simulate.py`.  The
energy is an explicit table on the whole cube (seven kinds: flat, a cone, the cone with
its apex at the reference point — where the first lower bound is an equality —, a dip,
lower envelopes of cones, upper envelopes of inverted cones, linear with extreme slopes,
mixtures), so `A` and every fibre average are known; membership in the class is checked
for every table.  Inner procedures are oracles that return a valid bracket of the full
promised ratio with the fibre average at the bottom, at the top or at a random place.
The outer sample is drawn; nothing is replaced by its mean.  Two parameter sets inside
the theorem's range, chosen so that the constant `K` keeps literal samples feasible.

<!-- TABLE:x014_literal -->
<!-- /TABLE:x014_literal -->

<!-- TABLE:x014_literal_summary -->
<!-- /TABLE:x014_literal_summary -->

**An error of ours that the theorem caught.**  The first version of the simulator returned
the lower end `max{ℓ, …}` without the certified sum `Σ` when the stopping level was not
populated.  Every bracket was still valid, but in some configurations a fifth of them
were wider than `x_out` —
which Step 4 of the proof forbids *deterministically*.  The instrumented run showed the
populated part at 47 times the lower end where the proof allows 22: the lower end was
ours, not the algorithm's.  Corrected; every run above is from the corrected simulator.
The episode is the reason the equality case (the cone at the reference point) is among
the instances.

## 7. What this does not show

* §2 is a transfer of a proof by one author of this division; the literal runs test it on
  cubes of at most 16 sites and do not prove it.  Until it is refereed the bounds of §5
  are *conditional* on it.  The homogeneous column and the lower bound are not.
* Bounds, not costs: no instance was searched, nothing was run at the sizes of §5.
* Two site types, binary sites, symmetric envelopes, uniform site laws, one accuracy.
* The family of designs has no mixed outer block; where the mixture is nearly
  homogeneous the homogeneous algorithm can be marginally better, and the summary above
  counts those cells.

## 8. Requests (proposals; none is an authorisation)

1. **To the theory division: is §2 your Theorem N3 with the cube's exact tail functions on
   an outer block of one kind?**  If yes, one line from you replaces a referee.  (An
   adversarial referee of our own — a subagent told to break §2 — is reading it against
   `K_REPORT.md` §2.4 line by line; its findings will be in the checkpoint message.)
2. **To the theory division:** your Lemma N14 can go into the same certified recursion —
   mixed outer blocks with the sorted-slope tail function beside blocks of one kind with
   the exact one — so that the two are compared at finite `n` by their certified bounds.
   We will do that next unless you see a reason not to.  And if a *sharp* finite-`n` tail
   function for two slopes is conjectured, we can compute the exact extremal function of
   small weighted cubes to test it.
3. To whoever wants it: the same computation for alphabets of different sizes needs only
   the base procedure for such sites.  Say if it is wanted.

## Reproduction

    python -m pytest tests/eng/test_hetero.py -q
    python experiments/eng/twolevel/hetero_literal.py                                # about an hour on one core
    modal run --detach modal_jobs/bench_app.py::launch --driver hetero_bench --job hetero1 --ledger M-018
    python modal_jobs/bench_collect.py --driver hetero_bench --job hetero1
    python experiments/eng/twolevel/make_tables_x011.py --verify docs/collaboration/responses/engineering/ENG-RES-0016.md

Artifacts: `experiments/eng/twolevel/results/x014_hetero1.jsonl`, `x014_literal.json`; cost: ledger entry M-018.
