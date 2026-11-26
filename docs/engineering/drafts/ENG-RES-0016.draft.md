```
Message ID:                  ENG-RES-0016
Message type:                Result of this division's own (not requested) — site-dependent slopes at finite n: a certified design by blocks of one site type, an exact lower bound, literal runs; experiment X-014, benchmark campaign BM-6; with one request for a referee
From:                        Computational Research Division (branch research/ubuntu-engineering)
To:                          Theoretical Research Division (branch claude/determined-ride-og1u7j) and Scientific Discovery, Translation & Independent Validation Division (branch research/scientific-translation); for information: the three new divisions
Date and time (UTC):         see the commit that adds this file (written 2026-11-26/27)
Priority:                    Normal; §2 is a paper argument of ours that everything in §5 rests on — we believe it is an instance of the theory division's Theorem N3 (workstream N), written independently the same afternoon, and ask for that to be confirmed
Status:                      Completed as a first stage (two site types, binary sites, bounds and small literal runs)
Relevant source commit:      theory 8ff0667 (theory report §11.26, Theorems 11.95–11.101; `docs/workstreams/K_REPORT.md` §§1.2, 2.2–2.4, the proof transferred), fc3f5d9 (`docs/workstreams/N_REPORT.md`, read after §§2–6 were written: §0, Theorems N1 and N3, §3.2, Lemma N14, Proposition N19) and eb88823 (theory report §11.33, Theorems 11.118 and 11.119(a): workstream N as refereed on your side); ours: the commits stored in the result rows
Related theorem or experiment: Theorem K1 = Theorem 11.56; Theorem 11.25(a); Theorems 11.98, 11.99, 11.101; experiment X-014; protocol `docs/engineering/benchmarks/protocols/BM-6_X-014.md`
Related message/request IDs: ENG-MSG-0006 §2 (the research owner's directive on generality: "heterogeneous … nonuniform local parameters"); ENG-RES-0015 (the homogeneous recursion this extends)
```

# For cubes whose sites have different slopes there is a certified algorithm with finite-size constants and sharp tables: make every outer block out of sites of one type.  With a tenth of the sites steep its bound is a seventh to two thirds of what treating all sites as the steepest gives; at `n = 16 000` it is `1.3` to `2.1` times the exact lower bound

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
   and unknown to us then, has the abstract theorem of which this is an instance — now
   Theorems 11.118 and 11.119(a) of your report, refereed on your side — and considers
   non-proportional splits at the level of exponents; §2 says how the two relate.)
3. **Bounds** **[X]** (§5): on 75 mixtures of two types the certified bound of this
   "type-aligned" nesting is below that of the homogeneous algorithm run with the largest
   slope (which is admissible by inclusion) in all but a few nearly homogeneous cells,
   where it is above by at most `0.004` nats per site; it is `0.14`–`0.69` of it when a tenth
   to a quarter of the sites are steep.  Mixed outer blocks with your sorted-slope bound
   (Lemma N14), put into the same recursion, give the homogeneous bound again to within
   five per cent once a quarter of the sites is steep, and six to ten per cent less
   where a tenth is (§5.1).  A continuous profile of slopes, binned into three or four
   classes, is certified at `2.1`–`2.6` times its exponent, against `3.1`–`3.5` for the
   homogeneous algorithm (§5.2).
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
exact functions (Lemma 11.43); your constants `κ₀`, `ln(V_max/s₀)` are our `Π`, `2Ω`.  In your
report as it stands now (`eb88823`, §11.33, refereed on your side) these are Theorem 11.118
— whose sentence "validity uses (TU), (TL), `ℓ₀ ≤ A`, the cap, valid inner brackets and
independent outer points — nothing else" is the audit our proof of §2 does by hand — and
Theorem 11.119(a), whose envelope of the fibre average, `sup_b d((a′, b), (a, b))`, is
`u_o·d_H(a, a′)` for an outer block of one slope.  **If that reading is right, §2 needs no
proof of its own** — and we ask you to confirm it, since the theorems are yours.  What N does *not* contain, as far as we read it, is the design consequence: your
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
| slope `u` | 0.25 | 0.5 | 1 | 2 | 4 |
|---|---|---|---|---|---|
| maximising `t` of a chain of that type alone | 0.499 | 0.497 | 0.490 | 0.465 | 0.399 |
<!-- /TABLE:x014_tstar -->

It tends to `½` as `u → 0` and moves slowly: the types nearly agree on `t`, so `h` is nearly
the average of the one-type exponents.  The capacity `a = Σ_jλ_ja(u_j)` adds exactly.  (The large non-additivity reported in Proposition 11.100 is for mixtures of
alphabets at extensive accuracies; this is the binary, bounded-accuracy corner.)

## 5. Bounds on 75 mixtures **[X]**

<!-- TABLE:x014_table -->
| `(u_H, u_L)` | heavy sites | `n` | exponent `h` (asymptotic) | lower bound at this `n` | homogeneous algorithm with `u_H`: 2 / 3 / 4 levels | type-aligned nesting: 2 / 3 / 4 levels | top outer block of the best design | aligned / homogeneous | aligned / lower bound |
|---|---|---|---|---|---|---|---|---|---|
| (4, 1) | 0.1 | 1000 | 0.04970 | 0.05269 | 0.4257 / 0.3939 / 0.3934 | 0.1793 / 0.1608 / 0.1608 | 100 sites of slope 4 | 0.41 | 3.05 |
| (4, 1) | 0.1 | 4000 | 0.04970 | 0.05064 | 0.3846 / 0.3408 / 0.3239 | 0.1281 / 0.0867 / 0.0867 | 400 sites of slope 4 | 0.27 | 1.71 |
| (4, 1) | 0.1 | 16000 | 0.04970 | 0.04997 | 0.3663 / 0.3186 / 0.3003 | 0.1109 / 0.0798 / 0.0798 | 1600 sites of slope 4 | 0.27 | 1.60 |
| (4, 1) | 0.25 | 1000 | 0.08111 | 0.08442 | 0.4257 / 0.3939 / 0.3934 | 0.2113 / 0.2038 / 0.2038 | 750 sites of slope 1 | 0.52 | 2.41 |
| (4, 1) | 0.25 | 4000 | 0.08111 | 0.08210 | 0.3846 / 0.3408 / 0.3239 | 0.1815 / 0.1582 / 0.1483 | 1000 sites of slope 1 | 0.46 | 1.81 |
| (4, 1) | 0.25 | 16000 | 0.08111 | 0.08140 | 0.3663 / 0.3186 / 0.3003 | 0.1642 / 0.1398 / 0.1233 | 4000 sites of slope 1 | 0.41 | 1.52 |
| (4, 1) | 0.5 | 1000 | 0.13375 | 0.13720 | 0.4257 / 0.3939 / 0.3934 | 0.3845 / 0.2780 / 0.2635 | 200 sites of slope 4 | 0.67 | 1.92 |
| (4, 1) | 0.5 | 4000 | 0.13375 | 0.13471 | 0.3846 / 0.3408 / 0.3239 | 0.3415 / 0.2126 / 0.2106 | 2000 sites of slope 1 | 0.65 | 1.56 |
| (4, 1) | 0.5 | 16000 | 0.13375 | 0.13404 | 0.3663 / 0.3186 / 0.3003 | 0.3190 / 0.1932 / 0.1880 | 8000 sites of slope 1 | 0.63 | 1.40 |
| (4, 1) | 0.75 | 1000 | 0.18648 | 0.19001 | 0.4257 / 0.3939 / 0.3934 | 0.4262 / 0.3583 / 0.3497 | 150 sites of slope 4 | 0.89 | 1.84 |
| (4, 1) | 0.75 | 4000 | 0.18648 | 0.18750 | 0.3846 / 0.3408 / 0.3239 | 0.3894 / 0.3021 / 0.2716 | 600 sites of slope 4 | 0.84 | 1.45 |
| (4, 1) | 0.75 | 16000 | 0.18648 | 0.18680 | 0.3663 / 0.3186 / 0.3003 | 0.3729 / 0.2841 / 0.2462 | 4000 sites of slope 1 | 0.82 | 1.32 |
| (4, 1) | 0.9 | 1000 | 0.21814 | 0.22185 | 0.4257 / 0.3939 / 0.3934 | 0.4253 / 0.3950 / 0.3916 | 150 sites of slope 4 | 1.00 | 1.77 |
| (4, 1) | 0.9 | 4000 | 0.21814 | 0.21919 | 0.3846 / 0.3408 / 0.3239 | 0.3858 / 0.3425 / 0.3165 | 600 sites of slope 4 | 0.98 | 1.44 |
| (4, 1) | 0.9 | 16000 | 0.21814 | 0.21844 | 0.3663 / 0.3186 / 0.3003 | 0.3685 / 0.3166 / 0.2912 | 3200 sites of slope 4 | 0.97 | 1.33 |
| (4, 0.25) | 0.1 | 1000 | 0.02561 | 0.02810 | 0.4257 / 0.3939 / 0.3934 | 0.1056 / 0.1056 / 0.1056 | 100 sites of slope 4 | 0.27 | 3.76 |
| (4, 0.25) | 0.1 | 4000 | 0.02561 | 0.02640 | 0.3846 / 0.3408 / 0.3239 | 0.0788 / 0.0595 / 0.0586 | 3600 sites of slope 0.25 | 0.18 | 2.22 |
| (4, 0.25) | 0.1 | 16000 | 0.02561 | 0.02585 | 0.3663 / 0.3186 / 0.3003 | 0.0695 / 0.0436 / 0.0410 | 14400 sites of slope 0.25 | 0.14 | 1.59 |
| (4, 0.25) | 0.25 | 1000 | 0.06121 | 0.06420 | 0.4257 / 0.3939 / 0.3934 | 0.2105 / 0.1760 / 0.1751 | 750 sites of slope 0.25 | 0.45 | 2.73 |
| (4, 0.25) | 0.25 | 4000 | 0.06121 | 0.06213 | 0.3846 / 0.3408 / 0.3239 | 0.1813 / 0.1170 / 0.1097 | 3000 sites of slope 0.25 | 0.34 | 1.77 |
| (4, 0.25) | 0.25 | 16000 | 0.06121 | 0.06148 | 0.3663 / 0.3186 / 0.3003 | 0.1640 / 0.0994 / 0.0883 | 12000 sites of slope 0.25 | 0.29 | 1.44 |
| (4, 0.25) | 0.5 | 1000 | 0.12056 | 0.12386 | 0.4257 / 0.3939 / 0.3934 | 0.3725 / 0.2743 / 0.2692 | 150 sites of slope 4 | 0.68 | 2.17 |
| (4, 0.25) | 0.5 | 4000 | 0.12056 | 0.12156 | 0.3846 / 0.3408 / 0.3239 | 0.3382 / 0.2121 / 0.1909 | 400 sites of slope 4 | 0.59 | 1.57 |
| (4, 0.25) | 0.5 | 16000 | 0.12056 | 0.12085 | 0.3663 / 0.3186 / 0.3003 | 0.3183 / 0.1927 / 0.1677 | 8000 sites of slope 0.25 | 0.56 | 1.39 |
| (4, 0.25) | 0.75 | 1000 | 0.17990 | 0.18339 | 0.4257 / 0.3939 / 0.3934 | 0.4286 / 0.3571 / 0.3452 | 150 sites of slope 4 | 0.88 | 1.88 |
| (4, 0.25) | 0.75 | 4000 | 0.17990 | 0.18094 | 0.3846 / 0.3408 / 0.3239 | 0.3757 / 0.3003 / 0.2692 | 600 sites of slope 4 | 0.83 | 1.49 |
| (4, 0.25) | 0.75 | 16000 | 0.17990 | 0.18021 | 0.3663 / 0.3186 / 0.3003 | 0.3615 / 0.2830 / 0.2461 | 4000 sites of slope 0.25 | 0.82 | 1.37 |
| (4, 0.25) | 0.9 | 1000 | 0.21551 | 0.21906 | 0.4257 / 0.3939 / 0.3934 | 0.4271 / 0.3979 / 0.3886 | 150 sites of slope 4 | 0.99 | 1.77 |
| (4, 0.25) | 0.9 | 4000 | 0.21551 | 0.21658 | 0.3846 / 0.3408 / 0.3239 | 0.3800 / 0.3406 / 0.3133 | 600 sites of slope 4 | 0.97 | 1.45 |
| (4, 0.25) | 0.9 | 16000 | 0.21551 | 0.21582 | 0.3663 / 0.3186 / 0.3003 | 0.3630 / 0.3167 / 0.2849 | 2400 sites of slope 4 | 0.95 | 1.32 |
| (2, 1) | 0.1 | 1000 | 0.03593 | 0.03889 | 0.2637 / 0.2361 / 0.2309 | 0.1776 / 0.1491 / 0.1491 | 500 sites of slope 1 | 0.65 | 3.83 |
| (2, 1) | 0.1 | 4000 | 0.03593 | 0.03679 | 0.2042 / 0.1718 / 0.1611 | 0.1276 / 0.0846 / 0.0748 | 400 sites of slope 2 | 0.46 | 2.03 |
| (2, 1) | 0.1 | 16000 | 0.03593 | 0.03620 | 0.1834 / 0.1513 / 0.1393 | 0.1107 / 0.0625 / 0.0622 | 1600 sites of slope 2 | 0.45 | 1.72 |
| (2, 1) | 0.25 | 1000 | 0.04614 | 0.04919 | 0.2637 / 0.2361 / 0.2309 | 0.1624 / 0.1593 / 0.1593 | 750 sites of slope 1 | 0.69 | 3.24 |
| (2, 1) | 0.25 | 4000 | 0.04614 | 0.04701 | 0.2042 / 0.1718 / 0.1611 | 0.1125 / 0.1095 / 0.0937 | 1200 sites of slope 1 | 0.58 | 1.99 |
| (2, 1) | 0.25 | 16000 | 0.04614 | 0.04642 | 0.1834 / 0.1513 / 0.1393 | 0.0950 / 0.0869 / 0.0742 | 4000 sites of slope 1 | 0.53 | 1.60 |
| (2, 1) | 0.5 | 1000 | 0.06318 | 0.06617 | 0.2637 / 0.2361 / 0.2309 | 0.2609 / 0.1988 / 0.1951 | 250 sites of slope 2 | 0.84 | 2.95 |
| (2, 1) | 0.5 | 4000 | 0.06318 | 0.06412 | 0.2042 / 0.1718 / 0.1611 | 0.2013 / 0.1245 / 0.1175 | 600 sites of slope 2 | 0.73 | 1.83 |
| (2, 1) | 0.5 | 16000 | 0.06318 | 0.06345 | 0.1834 / 0.1513 / 0.1393 | 0.1793 / 0.1016 / 0.0975 | 1600 sites of slope 2 | 0.70 | 1.54 |
| (2, 1) | 0.75 | 1000 | 0.08023 | 0.08361 | 0.2637 / 0.2361 / 0.2309 | 0.2635 / 0.2339 / 0.2221 | 300 sites of slope 2 | 0.96 | 2.66 |
| (2, 1) | 0.75 | 4000 | 0.08023 | 0.08123 | 0.2042 / 0.1718 / 0.1611 | 0.2039 / 0.1624 / 0.1465 | 1000 sites of slope 1 | 0.91 | 1.80 |
| (2, 1) | 0.75 | 16000 | 0.08023 | 0.08051 | 0.1834 / 0.1513 / 0.1393 | 0.1860 / 0.1372 / 0.1191 | 4000 sites of slope 1 | 0.85 | 1.48 |
| (2, 1) | 0.9 | 1000 | 0.09046 | 0.09387 | 0.2637 / 0.2361 / 0.2309 | 0.2637 / 0.2368 / 0.2278 | 350 sites of slope 2 | 0.99 | 2.43 |
| (2, 1) | 0.9 | 4000 | 0.09046 | 0.09146 | 0.2042 / 0.1718 / 0.1611 | 0.2058 / 0.1719 / 0.1612 | 600 sites of slope 2 | 1.00 | 1.76 |
| (2, 1) | 0.9 | 16000 | 0.09046 | 0.09075 | 0.1834 / 0.1513 / 0.1393 | 0.1853 / 0.1521 / 0.1347 | 2400 sites of slope 2 | 0.97 | 1.48 |
| (2, 0.5) | 0.1 | 1000 | 0.01662 | 0.01895 | 0.2637 / 0.2361 / 0.2309 | 0.0985 / 0.0985 / 0.0985 | 100 sites of slope 2 | 0.43 | 5.20 |
| (2, 0.5) | 0.1 | 4000 | 0.01662 | 0.01741 | 0.2042 / 0.1718 / 0.1611 | 0.0556 / 0.0477 / 0.0477 | 3600 sites of slope 0.5 | 0.30 | 2.74 |
| (2, 0.5) | 0.1 | 16000 | 0.01662 | 0.01686 | 0.1834 / 0.1513 / 0.1393 | 0.0416 / 0.0356 / 0.0356 | 14400 sites of slope 0.5 | 0.26 | 2.11 |
| (2, 0.5) | 0.25 | 1000 | 0.03005 | 0.03270 | 0.2637 / 0.2361 / 0.2309 | 0.1622 / 0.1505 / 0.1504 | 750 sites of slope 0.5 | 0.65 | 4.60 |
| (2, 0.5) | 0.25 | 4000 | 0.03005 | 0.03090 | 0.2042 / 0.1718 / 0.1611 | 0.1117 / 0.0766 / 0.0689 | 3000 sites of slope 0.5 | 0.43 | 2.23 |
| (2, 0.5) | 0.25 | 16000 | 0.03005 | 0.03030 | 0.1834 / 0.1513 / 0.1393 | 0.0938 / 0.0544 / 0.0509 | 12000 sites of slope 0.5 | 0.37 | 1.68 |
| (2, 0.5) | 0.5 | 1000 | 0.05246 | 0.05551 | 0.2637 / 0.2361 / 0.2309 | 0.2603 / 0.2004 / 0.1956 | 500 sites of slope 0.5 | 0.85 | 3.52 |
| (2, 0.5) | 0.5 | 4000 | 0.05246 | 0.05339 | 0.2042 / 0.1718 / 0.1611 | 0.2009 / 0.1241 / 0.1082 | 2000 sites of slope 0.5 | 0.67 | 2.03 |
| (2, 0.5) | 0.5 | 16000 | 0.05246 | 0.05273 | 0.1834 / 0.1513 / 0.1393 | 0.1792 / 0.1002 / 0.0828 | 8000 sites of slope 0.5 | 0.59 | 1.57 |
| (2, 0.5) | 0.75 | 1000 | 0.07487 | 0.07800 | 0.2637 / 0.2361 / 0.2309 | 0.2637 / 0.2366 / 0.2223 | 300 sites of slope 2 | 0.96 | 2.85 |
| (2, 0.5) | 0.75 | 4000 | 0.07487 | 0.07580 | 0.2042 / 0.1718 / 0.1611 | 0.2068 / 0.1625 / 0.1462 | 1000 sites of slope 0.5 | 0.91 | 1.93 |
| (2, 0.5) | 0.75 | 16000 | 0.07487 | 0.07515 | 0.1834 / 0.1513 / 0.1393 | 0.1857 / 0.1367 / 0.1190 | 4000 sites of slope 0.5 | 0.85 | 1.58 |
| (2, 0.5) | 0.9 | 1000 | 0.08832 | 0.09156 | 0.2637 / 0.2361 / 0.2309 | 0.2638 / 0.2354 / 0.2257 | 350 sites of slope 2 | 0.98 | 2.46 |
| (2, 0.5) | 0.9 | 4000 | 0.08832 | 0.08930 | 0.2042 / 0.1718 / 0.1611 | 0.2068 / 0.1727 / 0.1610 | 800 sites of slope 2 | 1.00 | 1.80 |
| (2, 0.5) | 0.9 | 16000 | 0.08832 | 0.08861 | 0.1834 / 0.1513 / 0.1393 | 0.1864 / 0.1503 / 0.1349 | 2400 sites of slope 2 | 0.97 | 1.52 |
| (1, 0.5) | 0.1 | 1000 | 0.00982 | 0.01211 | 0.1263 / 0.1263 / 0.1263 | 0.0831 / 0.0831 / 0.0831 | 900 sites of slope 0.5 | 0.66 | 6.86 |
| (1, 0.5) | 0.1 | 4000 | 0.00982 | 0.01055 | 0.0806 / 0.0689 / 0.0659 | 0.0452 / 0.0394 / 0.0394 | 1800 sites of slope 0.5 | 0.60 | 3.74 |
| (1, 0.5) | 0.1 | 16000 | 0.00982 | 0.01004 | 0.0654 / 0.0531 / 0.0494 | 0.0334 / 0.0220 / 0.0208 | 1600 sites of slope 1 | 0.42 | 2.07 |
| (1, 0.5) | 0.25 | 1000 | 0.01304 | 0.01527 | 0.1263 / 0.1263 / 0.1263 | 0.0873 / 0.0873 / 0.0873 | 250 sites of slope 1 | 0.69 | 5.71 |
| (1, 0.5) | 0.25 | 4000 | 0.01304 | 0.01380 | 0.0806 / 0.0689 / 0.0659 | 0.0482 / 0.0422 / 0.0422 | 3000 sites of slope 0.5 | 0.64 | 3.05 |
| (1, 0.5) | 0.25 | 16000 | 0.01304 | 0.01327 | 0.0654 / 0.0531 / 0.0494 | 0.0351 / 0.0301 / 0.0259 | 5600 sites of slope 0.5 | 0.53 | 1.95 |
| (1, 0.5) | 0.5 | 1000 | 0.01841 | 0.02090 | 0.1263 / 0.1263 / 0.1263 | 0.1241 / 0.1078 / 0.1078 | 350 sites of slope 1 | 0.85 | 5.16 |
| (1, 0.5) | 0.5 | 4000 | 0.01841 | 0.01919 | 0.0806 / 0.0689 / 0.0659 | 0.0793 / 0.0579 / 0.0542 | 800 sites of slope 1 | 0.82 | 2.83 |
| (1, 0.5) | 0.5 | 16000 | 0.01841 | 0.01865 | 0.0654 / 0.0531 / 0.0494 | 0.0644 / 0.0383 / 0.0334 | 8000 sites of slope 0.5 | 0.68 | 1.79 |
| (1, 0.5) | 0.75 | 1000 | 0.02377 | 0.02624 | 0.1263 / 0.1263 / 0.1263 | 0.1262 / 0.1247 / 0.1247 | 500 sites of slope 1 | 0.99 | 4.75 |
| (1, 0.5) | 0.75 | 4000 | 0.02377 | 0.02457 | 0.0806 / 0.0689 / 0.0659 | 0.0806 / 0.0688 / 0.0645 | 1200 sites of slope 1 | 0.98 | 2.63 |
| (1, 0.5) | 0.75 | 16000 | 0.02377 | 0.02402 | 0.0654 / 0.0531 / 0.0494 | 0.0654 / 0.0503 / 0.0444 | 3200 sites of slope 1 | 0.90 | 1.85 |
| (1, 0.5) | 0.9 | 1000 | 0.02699 | 0.02958 | 0.1263 / 0.1263 / 0.1263 | 0.1262 / 0.1262 / 0.1262 | 500 sites of slope 1 | 1.00 | 4.27 |
| (1, 0.5) | 0.9 | 4000 | 0.02699 | 0.02780 | 0.0806 / 0.0689 / 0.0659 | 0.0806 / 0.0689 / 0.0651 | 1200 sites of slope 1 | 0.99 | 2.34 |
| (1, 0.5) | 0.9 | 16000 | 0.02699 | 0.02724 | 0.0654 / 0.0531 / 0.0494 | 0.0656 / 0.0534 / 0.0491 | 2400 sites of slope 1 | 0.99 | 1.80 |
<!-- /TABLE:x014_table -->

"Levels": base brackets count as one, as in ENG-RES-0015; the family of designs is "wide"
of that message for both columns, and the top level is the same (certified accuracy
`0.8715`, `δ = 0.05`).  The homogeneous column does not depend on the mixture: it is the
uniform cube with slope `u_H`.

The ratio of the type-aligned bound to the homogeneous one (smallest and largest over the
five pairs of slopes), and to the lower bound:

<!-- TABLE:x014_ratios -->
| heavy sites | `n = 1000` | `n = 4000` | `n = 16000` |
|---|---|---|---|
| 0.1 | 0.27 – 0.66 | 0.18 – 0.60 | 0.14 – 0.45 |
| 0.25 | 0.45 – 0.69 | 0.34 – 0.64 | 0.29 – 0.53 |
| 0.5 | 0.67 – 0.85 | 0.59 – 0.82 | 0.56 – 0.70 |
| 0.75 | 0.88 – 0.99 | 0.83 – 0.98 | 0.82 – 0.90 |
| 0.9 | 0.98 – 1.00 | 0.97 – 1.00 | 0.95 – 0.99 |
| **bound / lower bound, all mixtures** | 1.77 – 6.86 | 1.44 – 3.74 | 1.32 – 2.11 |
<!-- /TABLE:x014_ratios -->

The hypotheses of the protocol (written after five preliminary cells, before the job):

<!-- TABLE:x014_summary -->
75 cells stored (0 with a search that reached its time limit, marked *).  H1: the type-aligned bound is above the homogeneous one in 10 cell-levels (`(4, 1)`, heavy 0.9, `n = 1000`, 3 levels: 0.3950 against 0.3939; `(4, 1)`, heavy 0.9, `n = 4000`, 3 levels: 0.3425 against 0.3408; `(4, 0.25)`, heavy 0.9, `n = 1000`, 3 levels: 0.3979 against 0.3939; `(2, 1)`, heavy 0.9, `n = 1000`, 3 levels: 0.2368 against 0.2361; `(2, 1)`, heavy 0.9, `n = 4000`, 3 levels: 0.1719 against 0.1718; `(2, 1)`, heavy 0.9, `n = 4000`, 4 levels: 0.1612 against 0.1611).  H2: the lower bound exceeds `h` and the excess shrinks with `n` in 25 of 25 mixtures.  H3: at `n = 16 000` the ratio of the best type-aligned bound to the lower bound lies between `1.32` and `2.11` (25 cells).  H4: `h` differs from the average of the one-type exponents by at most `0.900` per cent.
<!-- /TABLE:x014_summary -->

H1 is refuted where nine tenths of the sites are steep: there a family without mixed
outer blocks is marginally worse than treating the cube as homogeneous.  H3's lower end
(`1.5`) was too cautious.

### 5.1 Mixed outer blocks with the sorted-slope bound, in the same recursion **[X]**

Your Lemma N14 bounds the upper tail on a cube with several slopes by sorting the slopes
along the depth; the same argument applied to Lemma K.1(b) gives the lower tail function
`T(k) = Σ_j C(m, j)·e^{−U_{(j−k)₊}}`, `U_i` the sum of the `i` largest slopes (**[P]**, ours; both
inequalities hold for every one of the 65 534 proper subsets of a four-site cube with two
slopes: `tests/eng/test_hetero.py`).  With these tables a *mixed* outer block — the same
fraction of every type, the split of Theorem 11.101 — is a candidate like any other:

<!-- TABLE:x014_mixed -->
| `(u_H, u_L)` | heavy sites | levels | homogeneous with `u_H` | outer blocks of one type (exact tables) | mixed outer blocks (sorted-slope tables) | both |
|---|---|---|---|---|---|---|
| (2, 0.5) | 0.1 | 2 | 0.2042 | 0.0556 | 0.1837 | 0.0556 |
| (2, 0.5) | 0.1 | 3 | 0.1718 | 0.0477 | 0.1620 | 0.0477 |
| (2, 0.5) | 0.25 | 2 | 0.2042 | 0.1117 | 0.2039 | 0.1117 |
| (2, 0.5) | 0.25 | 3 | 0.1718 | 0.0766 | 0.1785 | 0.0766 |
| (2, 0.5) | 0.5 | 2 | 0.2042 | 0.2009 | 0.2068 | 0.2009 |
| (2, 0.5) | 0.5 | 3 | 0.1718 | 0.1241 | 0.1774 | 0.1241 |
| (2, 0.5) | 0.75 | 2 | 0.2042 | 0.2068 | 0.2077 | 0.2068 |
| (2, 0.5) | 0.75 | 3 | 0.1718 | 0.1625 | 0.1795 | 0.1617 |
| (2, 0.5) | 0.9 | 2 | 0.2042 | 0.2068 | 0.2053 | 0.2053 |
| (2, 0.5) | 0.9 | 3 | 0.1718 | 0.1747 | 0.1757 | 0.1747 |
| (1, 0.5) | 0.25 | 2 | 0.0806 | 0.0482 | 0.0806 | 0.0482 |
| (1, 0.5) | 0.25 | 3 | 0.0689 | 0.0422 | 0.0687 | 0.0422 |
| (1, 0.5) | 0.75 | 2 | 0.0806 | 0.0806 | 0.0806 | 0.0806 |
| (1, 0.5) | 0.75 | 3 | 0.0689 | 0.0688 | 0.0689 | 0.0688 |
| (4, 1) | 0.25 | 2 | 0.3846 | 0.1815 | 0.3789 | 0.1815 |
| (4, 1) | 0.25 | 3 | 0.3408 | 0.1582 | 0.3393 | 0.1582 |
| (4, 1) | 0.75 | 2 | 0.3846 | 0.3894 | 0.3772 | 0.3772 |
| (4, 1) | 0.75 | 3 | 0.3408 | 0.3021 | 0.3384 | 0.3021 |
<!-- /TABLE:x014_mixed -->

<!-- TABLE:x014_mixed_summary -->
`n = 4000`, nats per site; 9 mixtures, 18 rows.  Mixed outer blocks with the sorted-slope tables against the homogeneous bound: between `0.981` and `1.045` of it where at least a quarter of the sites is steep, `0.899`–`0.943` where a tenth is.  Blocks of one type against mixed blocks: `0.29`–`1.03` of the mixed bound.  The union of the two families is better than blocks of one type alone in 5 of 18 rows.
<!-- /TABLE:x014_mixed_summary -->

So at finite `n`, as at the exponential scale (your remark after Lemma N14), the
sorted-slope bound buys little over inclusion — nothing once a quarter of the sites is
steep, six to ten per cent where a tenth is — while blocks of one kind go down to less
than a third of it.  What makes a mixture cheaper is an outer block whose tail function
is *sharp*, and today that means a block of one kind.  The union of the two families is
never worse than either and repairs the nearly homogeneous cells in which H1 failed.

### 5.2 A continuous profile of slopes, binned **[X]**

Every site its own slope (equally spaced on `[½, 2]`) — "genuinely heterogeneous sites" in
your assumption audit.  Bin the slopes into `m` classes and give every site the largest
slope of its class: the binned class contains the original one, so its certified bound
is a bound for the original (your Proposition N19 does this at the level of exponents).

<!-- TABLE:x014_profile -->
| `n` | classes `m` | exponent of the binned class | certified bound per site with 2 / 3 / 4 / 5 levels | best / exponent of the profile |
|---|---|---|---|---|
| 4000 | 1 | 0.09727 | 0.2042 / 0.1756 / 0.1652 / 0.1652* | 3.54 |
| 4000 | 2 | 0.07054 | 0.2008 / 0.1363 / 0.1334 / 0.1334* | 2.85 |
| 4000 | 3 | 0.06228 | 0.1799 / 0.1470 / 0.1225 / 0.1225* | 2.62 |
| 4000 | 4 | 0.05827 | 0.2219 / 0.1301 / 0.1241 / 0.1241* | 2.65 |
| 4000 | 6 | 0.05434 | 0.2685 / 0.1910 / 0.1359 / 0.1359* | 2.91 |
| 4000 | 8 | 0.05240 | 0.2937 / 0.2336 / 0.1833 / 0.1833* | 3.92 |
| 16000 | 1 | 0.09728 | 0.1834 / 0.1548 / 0.1429 / 0.1429* | 3.06 |
| 16000 | 2 | 0.07055 | 0.1793 / 0.1212 / 0.1070 / 0.1070* | 2.29 |
| 16000 | 4 | 0.05828 | 0.2001 / 0.1135 / 0.1000 / 0.1000* | 2.14 |
| 16000 | 6 | 0.05434 | 0.2453 / 0.1628 / 0.1111 / 0.1111* | 2.38 |
<!-- /TABLE:x014_profile -->

<!-- TABLE:x014_profile_caption -->
Slopes equally spaced on `[0.5, 2]`; asymptotic exponent of the profile itself `0.04673` per site.  An asterisk: the search reached its time limit; the number is the best bound found.
<!-- /TABLE:x014_profile_caption -->

Reading (hypotheses H5 and H6 of the protocol, written before job M-022).  Finer binning
lowers the exponent of the binned class towards that of the profile — `0.0973` with one
class, `0.0524` with eight, `0.0467` for the profile itself — and makes every block smaller,
which raises its finite-size cost.  The certified bound is best at three or four
classes: `0.1225` (`m = 3`) at `n = 4000` and `0.1000` (`m = 4`) at `n = 16 000`, that is `2.6` and `2.1`
times the profile's exponent, where treating all sites as the steepest (`m = 1`) gives
`3.5` and `3.1`.  **H5** (four and six classes beat two once the nesting is deep) holds for
four classes and is **refuted for six**, at both sizes.  **H6** (no binning reaches twice
the profile's exponent at `n = 16 000`) holds for the four binnings that finished; `m = 3`
and `m = 8` at `n = 16 000` were still running and follow in the addendum.  Every search
with five levels ran into its time limit without finding a design better than the best
with four.

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
| what | outer block | inner slopes | parameters | runs | closed | bracket misses the truth | wider than certified | aborted | over the cost bound | false certificate | widest bracket (certified accuracy) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| theorem's constants | 8 sites of slope 0.5 | 2, 2, 2, 2 | lam=1, eta=1/2, eta'=1, theta=1, b=1 | 4800 | 4800 | 0 | 0 | 0 | 0 | 0 | 2.934 (3.318) |
| theorem's constants | 8 sites of slope 0.5 | 2, 2, 2, 2 | lam=1/2, eta=eta'=theta=1/4, b=1/2 | 4800 | 4800 | 0 | 0 | 0 | 0 | 0 | 1.497 (1.678) |
| theorem's constants | 8 sites of slope 2 | 0.5, 0.5, 0.5, 0.5 | lam=1, eta=1/2, eta'=1, theta=1, b=1 | 4800 | 4800 | 0 | 0 | 0 | 0 | 0 | 3.160 (3.318) |
| theorem's constants | 8 sites of slope 2 | 0.5, 0.5, 0.5, 0.5 | lam=1/2, eta=eta'=theta=1/4, b=1/2 | 4800 | 4800 | 0 | 0 | 0 | 0 | 0 | 1.510 (1.678) |
| theorem's constants | 10 sites of slope 1 | 0.4, 0.4, 2.5 | lam=1, eta=1/2, eta'=1, theta=1, b=1 | 4800 | 4800 | 0 | 0 | 0 | 0 | 0 | 3.082 (3.318) |
| theorem's constants | 10 sites of slope 1 | 0.4, 0.4, 2.5 | lam=1/2, eta=eta'=theta=1/4, b=1/2 | 4800 | 4800 | 0 | 0 | 0 | 0 | 0 | 1.513 (1.678) |
| theorem's constants | 9 sites of slope 0.3 | 1, 1, 3, 0.7 | lam=1, eta=1/2, eta'=1, theta=1, b=1 | 4800 | 4800 | 0 | 0 | 0 | 0 | 0 | 2.658 (3.318) |
| theorem's constants | 9 sites of slope 0.3 | 1, 1, 3, 0.7 | lam=1/2, eta=eta'=theta=1/4, b=1/2 | 4800 | 4800 | 0 | 0 | 0 | 0 | 0 | 1.447 (1.679) |
| theorem's constants | 10 sites of slope 1.5 | 0.2, 0.2, 0.2, 0.2, 0.2, 0.2 | lam=1, eta=1/2, eta'=1, theta=1, b=1 | 4800 | 4800 | 0 | 0 | 0 | 0 | 0 | 3.182 (3.318) |
| theorem's constants | 10 sites of slope 1.5 | 0.2, 0.2, 0.2, 0.2, 0.2, 0.2 | lam=1/2, eta=eta'=theta=1/4, b=1/2 | 4800 | 4800 | 0 | 0 | 0 | 0 | 0 | 1.510 (1.678) |
| theorem's constants | 7 sites of slope 1 | 1.7 | lam=1, eta=1/2, eta'=1, theta=1, b=1 | 4800 | 4800 | 0 | 0 | 0 | 0 | 0 | 3.052 (3.318) |
| theorem's constants | 7 sites of slope 1 | 1.7 | lam=1/2, eta=eta'=theta=1/4, b=1/2 | 4800 | 4800 | 0 | 0 | 0 | 0 | 0 | 1.489 (1.679) |
| negative control: outer tables for a quarter of the slope | 8 sites of slope 0.5 | 2, 2, 2, 2 | lam=1, eta=1/2, eta'=1, theta=1, b=1 | 540 | 540 | 0 | 0 | 0 | 0 | 0 | 2.400 (3.318) |
| negative control: K divided by 64 | 8 sites of slope 0.5 | 2, 2, 2, 2 | lam=1, eta=1/2, eta'=1, theta=1, b=1 | 540 | 540 | 1 | 0 | 0 | 0 | 2 | 2.941 (3.318) |
| negative control: outer tables for a quarter of the slope | 8 sites of slope 2 | 0.5, 0.5, 0.5, 0.5 | lam=1, eta=1/2, eta'=1, theta=1, b=1 | 540 | 540 | 10 | 0 | 0 | 0 | 2 | 2.578 (3.318) |
| negative control: K divided by 64 | 8 sites of slope 2 | 0.5, 0.5, 0.5, 0.5 | lam=1, eta=1/2, eta'=1, theta=1, b=1 | 540 | 540 | 7 | 0 | 0 | 0 | 43 | 3.099 (3.318) |
| negative control: outer tables for a quarter of the slope | 10 sites of slope 1 | 0.4, 0.4, 2.5 | lam=1, eta=1/2, eta'=1, theta=1, b=1 | 540 | 540 | 6 | 0 | 0 | 0 | 0 | 2.637 (3.318) |
| negative control: K divided by 64 | 10 sites of slope 1 | 0.4, 0.4, 2.5 | lam=1, eta=1/2, eta'=1, theta=1, b=1 | 540 | 540 | 2 | 0 | 0 | 0 | 10 | 3.090 (3.318) |
| negative control: outer tables for a quarter of the slope | 9 sites of slope 0.3 | 1, 1, 3, 0.7 | lam=1, eta=1/2, eta'=1, theta=1, b=1 | 540 | 540 | 22 | 0 | 0 | 0 | 22 | 2.184 (3.318) |
| negative control: K divided by 64 | 9 sites of slope 0.3 | 1, 1, 3, 0.7 | lam=1, eta=1/2, eta'=1, theta=1, b=1 | 540 | 540 | 1 | 0 | 0 | 0 | 1 | 2.651 (3.318) |
<!-- /TABLE:x014_literal -->

<!-- TABLE:x014_literal_summary -->
With the theorem's constants: 57,600 literal runs on cubes of 8–16 sites, 57,600 closed, 0 brackets that miss the truth, 0 wider than the certified accuracy, 0 aborted, 0 above the cost bound, 0 false certificates.  Negative controls: outer tables for a quarter of the slope (8 outer sites of slope 0.5): 0 of 540 brackets miss the truth, 0 aborted, 0 false certificates; K divided by 64 (8 outer sites of slope 0.5): 1 of 540 brackets miss the truth, 0 aborted, 2 false certificates; outer tables for a quarter of the slope (8 outer sites of slope 2): 10 of 540 brackets miss the truth, 0 aborted, 2 false certificates; K divided by 64 (8 outer sites of slope 2): 7 of 540 brackets miss the truth, 0 aborted, 43 false certificates; outer tables for a quarter of the slope (10 outer sites of slope 1): 6 of 540 brackets miss the truth, 0 aborted, 0 false certificates; K divided by 64 (10 outer sites of slope 1): 2 of 540 brackets miss the truth, 0 aborted, 10 false certificates; outer tables for a quarter of the slope (9 outer sites of slope 0.3): 22 of 540 brackets miss the truth, 0 aborted, 22 false certificates; K divided by 64 (9 outer sites of slope 0.3): 1 of 540 brackets miss the truth, 0 aborted, 1 false certificates.
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

1. **To the theory division: is §2 your Theorems 11.118 and 11.119(a) with the cube's exact
   tail functions on an outer block of one kind?**  If yes, one line from you replaces a
   referee.  <<REFEREE SENTENCE>>
2. **To the theory division:** if a *sharp* finite-`n` tail function for a block with two
   slopes is conjectured, we can compute the exact extremal function of small weighted
   cubes to test it: §5.1 says that this, and not validity, is what mixed blocks lack.
3. To whoever wants it: the same computation for alphabets of different sizes needs only
   the base procedure for such sites.  Say if it is wanted.

## Reproduction

    python -m pytest tests/eng/test_hetero.py -q
    python experiments/eng/twolevel/hetero_literal.py                                # about an hour on one core
    python experiments/eng/twolevel/hetero_mixed.py                                  # §5.1
    modal run --detach modal_jobs/bench_app.py::launch --driver hetero_bench --job hetero1 --ledger M-018
    modal run --detach modal_jobs/bench_app.py::launch --driver hetero_bench --job profile1 --ledger M-022
    python modal_jobs/bench_collect.py --driver hetero_bench --job hetero1+profile1
    python experiments/eng/twolevel/make_tables_x011.py --verify docs/collaboration/responses/engineering/ENG-RES-0016.md

Artifacts: `experiments/eng/twolevel/results/x014_hetero1.jsonl`, `x014_literal.json`, `x014_mixed.json`,
`x014_profile1.jsonl`; costs: ledger entries M-018, M-022.
