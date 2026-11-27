# Workstream R26 — adversarial review of the theory division's §11.33 (their workstream N): the nested algorithm on an arbitrary probability space, and whether nesting is valid on a known part that is a band model

*Internal review by an AI agent (one model instance, one session, 2026-11-26).  It is **not** external peer
review.  Object: Theoretical Research Division, branch `claude/determined-ride-og1u7j` at `4692f59`, read only
through the copies named in the brief.*

**Read.**  `N_REPORT.md`, all 1 124 lines.  `THEORY_REPORT.md` l. 12105–12328 (§11.33 with its instance table and
its paragraph on assumptions) and l. 5590–5699 (Theorem 11.56: statement, proof sketch, remark on the lowered
cap).  Nothing else of that branch: not their scripts, not their internal review, not `K_REPORT.md` (the proof of
Theorem N1 cites it for two steps; I re-derived those steps from the statements).  Not opened: `R_REPORT.md`,
`Z_REPORT.md`, `Z_REVIEW.md`, the subdirectory `read_only_after_your_own_report`.  No web page was opened.

**Four kinds of checking, kept apart.**  **[review]** re-derived on paper from the definitions; **[replication]**
re-computed with code of my own written from the statements (`experiments/science/ws_R26/`); **[re-run]** their
code — none, it was not available; **[read only]**.  Labels of `COMMON.md`: [P] proof given here, [N] numerical,
[H] heuristic, [K] known and cited.  Energies are in units of `kT`.

---

## 0. Verdict

**In ten lines.**
* **Theorem N4 / 11.119(b): proved as stated** — a two-line proof; conditional on inner procedures and on a tail
  function that §11.33 does not supply for band models.
* **Proposition N12 / 11.121: (a)–(c) proved as stated; (d) replicated** (invalid in 280 of 280 runs; product
  control valid in 540 of 540).  Its mechanism sentence is **incomplete** (a second false step, the lower tail
  function: `L` up to `3.9·A`); its closing remark on hubs is **false at finite size** (counterexamples: a chain
  with one boundary site, 260 of 300 runs; their own cube with hubs of 2 to 6 sites, 260 of 400 runs).
* **Theorems N1, N1′ / 11.118: proved as stated** (every step re-derived; 1 071 adversarial runs, no claim
  violated).  **Gaps, closed here:** Lemma N.0 is false as written at `q = 1` (a literal implementation fails
  10 of 10 runs); the constants of remark (R5).  The cost bound of N1′ is finite iff `π_* > 0`, which an
  exponential moment does not imply.
* **N9, N10 / 11.120(a),(b): proved as stated**, given the Gaussian isoperimetric inequality; a statement about
  Algorithm A, the fixed split is essential.  N11: read only.

**The same, with reasons.**

1. **Theorem N4 / 11.119(b)** (dependence under a class-relative influence): **proved as stated** [review].  The
   proof is two lines and uses nothing about `ι` beyond the displayed inequality (no symmetry, no triangle
   inequality, `ι = +∞` allowed).  It is a conditional statement: it supposes inner procedures that are valid
   under every conditional law (for a band model none of §11.33 has a certified cost below enumeration) and a
   tail function of the enlarged envelope.  One slip in the lemma it relies on (Lemma N.0 at `q = 1`) is closed
   here.  For a band model the theorem is **true and, in the form "slope `u + ι`" with an explicit bound,
   computationally empty at bounded accuracy**; its usable form is conditioning on the boundary layer (§2, F3).
2. **Proposition N12 / 11.121** (the false certificate): **(a)–(c) proved as stated** [review; replication to six
   digits]; **(d) replicated**: my implementation returns an invalid bracket in 280 of 280 runs (seven parameter
   sets × `θ ∈ {20, 1}` × 20 seeds), the control on product known parts is valid in 540 of 540.  **Two
   corrections.**  (i) The sentence "the false step is the tail bound, and the run closes below the spike" is one
   of two mechanisms: at `θ = 1` six of my seven parameter sets do *not* close below the spike; they find it
   after `2·10⁵`–`2·10⁶` outer points and are then invalid from **below** (`L = 2.4·A` to `3.9·A`) through the
   *lower* tail function.  (ii) The closing remark — "not a counterexample: … a hub: condition on them; the
   failure needs the influence to be spread" — is **false at finite size**: on a nearest-neighbour chain with
   the influence at one boundary site the algorithm returned a false bracket in 260 of 300 runs, and in their
   own setting (uniform outer cube `Q_12`, Harper's functions) a hub of 2 sites does at `θ ≥ 20`, of 4 sites at
   every threshold tested.  The repair itself (conditioning) is complete for validity: 0 invalid of 300.
3. **Theorems N1, N1′ / 11.118** (the abstract level theorem): **proved as stated** [review of every step;
   replication: 990 runs on integrands with an atom at the maximum, gaps and heavy lower tails, each with the
   sharpest valid tail functions, and 81 runs without a cap, 32 levels left as negligible: no claim violated].
   Gaps closed here: Lemma N.0 gives a finite value at `q = 1` (a literal implementation returns a false
   bracket in 10 of 10 runs); remark (R5) uses constants that are undefined for `Ξ ≡ +∞`.  For N1′ the cap is
   replaced by an upper bound `u₀ ≥ A` **and** a positive closing level under a strengthened condition; the cost
   bound is finite iff that level is positive, which does **not** follow from the exponential moment (example).
4. **Theorem N9, Proposition N10 / 11.120(a),(b)** (Gauss space): **proved as stated, given the Gaussian
   isoperimetric inequality** [review; closed forms replicated to `3·10⁻¹⁴`].  "Gains nothing" is a statement
   about Algorithm A on one family of instances chosen after the split, on its good event — not a lower bound
   for algorithms; the fixed split is essential to the argument.  **N11 / 11.120(c): read only.**

**The paragraph of Item 1 (iii).**  *Nesting on a rotamer band model is valid if* the outer tail function is that
of the true envelope of the fibre averages — the residual slope on every outer site plus, on the last `r` outer
sites only (`r` = bandwidth), the class-relative influence `ι` of that boundary layer on the inner block — *or
if the `r` boundary sites are conditioned on* (`q^r` product sub-problems whose weights the transfer matrix gives
exactly; no bound on any influence is needed).  *It is not valid with the product-class tail function* (slope `u`
at every site): on a nearest-neighbour chain with couplings of 11–14 `kT` that gave a false bracket in 160 of
180 runs, the upper end below the truth by factors 50 to 2 000, with the influence at a single site (with a
weaker chain, couplings 7.6–10 `kT`: 260 of 300 in all).  *What `ι`
is:* pointwise it is the clash energy itself (`10 → 10.5`, `20 → 20.5`, `30 → 30.5`; `3J` to `5J` without
clashes; up to `188` for `r = 5`) — useless as a hypothesis; for the box class of a sandwich of width `D` it is
at most `min(D, pointwise)` — never infinite, but that class has no metric structure, the fibre averages lie in
a box that the transfer matrix computes, and nesting gains nothing over plain sampling (cost of order `e^D`
whatever the chain length); for `u`-Lipschitz residuals it is proportional to `u`, does not grow with the clash
energy beyond about `10 kT` nor with the inner block beyond 5 to 20 sites, and at one boundary site it is `1.1u`
to `1.4u` at `J = 1` (`1.9u` to `2.5u` with clashes) and `2u` to `4u` at `J = 4…8` (exact values, inner blocks of
4 to 7 sites; the polynomial bound for long blocks is `1.2u`–`1.8u` and `2.5u`–`8u` for 3 to 6 states); per
boundary layer it lies between `1.1u` (`r = 1`) and the cap `u·k` (`r ≥ 3` with clashes, or a rigid inner block —
a domino of clashes: `11.4` at `k = 16`).  *Worth:* the slope `u + ι` is a useful hypothesis only at an extensive
accuracy, or if one accepts `ι` to `ι + 3` nats of accuracy per cut; at a bounded accuracy an explicit bound that charges `e^ι` to every set moves the closing
level to the atom (13 to `10¹⁶` times the product-case sample for 12 to 80 outer sites), the theorem is then
true and empty, and conditioning is the usable route, at `q^r` sub-problems per cut (81 to `2.8·10⁵` for
`q = 3…6`, `r = 4…7`).  With the exponents of the binary cube at `u = 1` (two levels save about `0.055` nats per
site: my reading of their numbers, [H]) a cut pays for itself only beyond about `r·ln q / 0.055` sites — 80
(`q = 3`, `r = 4`) to 230 (`q = 6`, `r = 7`); on chains of 8 to 10 sites nesting is valid in the conditioned form
and worth nothing.

---

## 1. The statements as I understand them, with the hypotheses the texts leave implicit

**1.1 Tail functions and the level theorem (N_REPORT §2.1–2.5; 11.118).**  `V > 0` measurable on `(X_o, μ_o)`,
`A = ∫V dμ_o < ∞`, `p(s) = μ_o(V > s)`, `p̄(s) = μ_o(V ≥ s)`.  `Ξ : (0,1] → [0,∞]` and a nondecreasing
`Θ : (0,1] → [0,1]` are tail functions if for all `s > 0`, `q ∈ (0,1]`

    (TU)  p(s) ≤ q  ⟹  E(V − s)₊ ≤ s·Ξ(q),          (TL)  p̄(s) ≥ q  ⟹  E min(V, s) ≥ s·Θ(q).

Algorithm A climbs the ladder `s_j = κ₀ℓ₀e^{jλ}`; at level `j` it classifies the first `M` outer points as high
or low from refinable brackets of `V(a_i)`, certifies `p(s_j) ≤ q` and (if `N ≥ K` points are high)
`p(s_je^{−b}) ≥ p̲`, raises the running lower bound to `s_je^{−b}·max(p̲, Θ(p̲))`, and stops when
`s_j·Ξ(q) ≤ θe^bℓ` or when the ladder passes the cap `V_max`.  **Theorem N1:** with the constants of §2.2, in
every run at most `C_max` queries, and `L ≤ A ≤ U ≤ e^{x_out}L` except with probability `δ`.  **Theorem N1′:** the
same without a cap, given `u₀ ≥ A` and `π_* > 0` with `Ξ(q) ≤ θν₁q` and `Ξ(q) ≤ θ·max(c_ηq, Θ(c_ηq))` for all
`q < π_*`.

*Implicit, and used:* (i) the outer points are independent draws from **exactly** `μ_o`, and the thresholds
`s_j` are functions of the reference data only (this is what makes the counts binomial); (ii) `Ξ(1) = +∞`
(needed whenever `q = 1`, which happens at every level below `min V`); (iii) the rung-0 bracket is valid in
every run, with a ratio that is uniform over outer points; (iv) each potential inner call fails with
probability at most `δ′` *conditionally on the outer points* — independence between calls, which (S4) asks
for, is not used (the proof takes a union bound); (v) `π_*` is a design constant fixed before the run, and for
`Ξ ≡ +∞` or for a tail function with `Ξ(q)/q → ∞` no admissible `π_*` exists and the constants `m_max`, `K`,
`δ′`, `C_max` are undefined; (vi) (TU) is used at the ladder levels `s_j` only, (TL) at the levels `s_je^{−b}`
only — the quantifier "for all `s > 0`" is stronger than what the proof needs.

*What a pair of tail functions must satisfy, and where the proof uses it* [review].  (TU): once per run, in Step
3, at the closing pass `(s_j, q)`, after `p(s_j) ≤ q` has been certified by sampling.  (TL): in Step 2, at every
populated pass, at `(s_je^{−b}, p̲)`.  That `Θ` is nondecreasing: Step 5 only (cost).  That `Ξ(1) = +∞`: whenever
`q = 1`.  Nothing else: not finiteness, not monotonicity of `Ξ`, not sharpness.  For the cost: the two
inequalities [N], [P] for **all** `q` below `π_*`.

**1.2 Two blocks (N_REPORT §2.6–2.7; 11.119).**  `μ` on `X_o × X_i` with outer marginal `μ_o` and conditional
laws `μ(·|a)`; `𝒞` a class of residuals `ψ`; `V_ψ(a) = ∫e^{−ψ(a,b)}μ(db|a)`, so `A(ψ) = ∫V_ψdμ_o =
Z(f+ψ)/Z(f)` when `μ` is the Gibbs measure of the known part `f`.  **Theorem N4:** if `ψ(a′,b) − ψ(a,b) ≤
d_o(a′,a)` and `∫w dμ(·|a) ≤ e^{ι(a,a′)}∫w dμ(·|a′)` for all fibre weights `w` of the class, then
`V_ψ(a) ≤ V_ψ(a′)e^{d_o(a′,a)+ι(a,a′)}`, and Algorithm A with tail functions of that envelope under `μ_o` has the
guarantees of Theorem N1.

*Implicit:* (i) regular conditional laws exist and can be sampled exactly, and so can `μ_o` (for a band model:
transfer matrices); (ii) (F1′): for every `a` there are inner bracket procedures for `∫w dμ(·|a)` with *certified*
costs — the procedures of the report with a cost theory are for product measures; (iii) reference data
`ℓ₀ ≤ A`, a cap or `u₀`, and the rung-0 bracket are computed under the *dependent* measure: the cube's cap
`e^{−ψ₀+un}` stays valid (it is pointwise); the cube's lower bound `e^{−ψ₀}((1+e^{−u})/2)^n` is an expectation under
the uniform measure and must become `e^{−ψ₀}E_μe^{−d(x,x₀)}` (in the instance of Proposition N12 `1.7·10⁻⁸` instead
of `2.4·10⁻⁵`); and a cap derived from the assumed envelope of the outer integrand, `V(a₀)e^{um}`, is false there
(`0.018` against `max V = 0.975`); (iv) a tail function of the enlarged envelope *under the outer marginal* — for a
band model a Markov measure, for which the instance table of §11.33 says "none for Markov measures" and N_REPORT
§4(f) offers the finite maximum of Lemma N.0 (enumeration, at most 16 points) or a transfer from block products
whose constants grow linearly with the length;
(v) only the weight `w = e^{−ψ(a′,·)}` of the comparison point is used in the proof.

**1.3 Proposition N12 (N_REPORT §5.2; 11.121).**  Outer cube `Q_m` with uniform marginal; inner cube `Q_k` with
`μ(·|a) = Bernoulli(p(a))^{⊗k}`, `p(a) = σ(J(τ − |a|))`; residual `ψ = u|b|`.  (a) `ψ ∈ L_u`; (b) `V(a) =
(1 − p(a) + p(a)e^{−u})^k`, and across the threshold `ln V` jumps by `k·c(J,u)`; (c) (TU) for the slope `u` fails
as soon as `kc > u(m − τ + ½)`; (d) on `m = 12`, `k = 16`, `u = 1`, `J = 4`, `τ = 10.5` the algorithm run with the
tail function of the assumed class returns an invalid bracket in every run.
*Implicit:* the parameters `λ, η, η′, ν₁, κ₀, b, δ`, the ladder and the reference data of the runs are not
stated; "(F1) holds" in (a) is (F1′) (the conditional laws are biased products that depend on `a`); the
"assumed class" comprises **two** functions, Harper's upper *and* lower one.

**1.4 Gauss space (N_REPORT §5.1; 11.120).**  For `−ln V` `L`-Lipschitz (Euclidean) under `γ_n`:
`Ξ_L(q) = e^{L²/2−Lt}Φ(L−t) − Φ(−t)`, `Θ_L(p) = p + e^{Lc+L²/2}Φ(−c−L)` are the exact tail functions (N9);
`R_G[T] ≥ max(T, Θ_na)` and, at the linear instance with gradient in the outer block, every run on its good
event has `M_max ≥ (2K/(1+η))·exp((L − √(2x_out))²/2)` if `x_out < L²/2` (N10).

---

## 2. Findings

Each finding: **severity**; the line that decides it; the evidence with its kind; a replacement text.

### F1 [major] — Proposition N12(d) / 11.121(c): there are two false steps, and "the run closes below the spike" is not what happens at `θ = 1` for most parameter sets

*Line.*  N_REPORT §5.2 (d): "the Chernoff events held in all 80, so this is not a sampling accident: every
certificate obtained by sampling stays true, the false step is the tail bound, and the run closes below the
spike."  THEORY_REPORT 11.121(c): "with the certified upper end below `A` by factors of about `300` (threshold
`θ = 20`) and `2 800`–`4 600` (`θ = 1`).  … the false step is the tail bound, and the run closes below the spike."

*Evidence* [replication; `r26_n12.py`, logs `out_n12_assumed_2.txt`, `out_n12_scan_2.txt`; simulated inner
oracle as in N_REPORT §7.3; valid reference data computed under the dependent measure, so that the tail
functions are the only false input].
* `θ = 20`, seven parameter sets (`λ ∈ {1, ½}`, `η ∈ {½, 0.3}`, `b ∈ {¼, ½, 1}`, `δ ∈ {0.05, 0.001}`,
  `κ₀ ∈ {1, 0.05}`), 20 seeds each: **140 of 140 invalid**; every run closes at `s_j ≈ 2·10⁻⁷…3·10⁻⁷` (the bulk
  is `≤ 1.2·10⁻⁷`, the spike `≥ 0.29`) after 1 672 to 2 232 outer points; `A/U = 712` (`1 174` for `λ = ½`); the
  false certificate is the upper tail bound in all 140; the sampling certificates and the Chernoff events hold
  in all 140.  This is the text's mechanism.  (Their factor is "about 300"; the difference is the parameter
  set, which the text does not give.)
* `θ = 1`: **140 of 140 invalid**, but only the set with `λ = ½` closes below the spike (7 232 points,
  `A/U = 4 200` — inside their range).  In the other six sets the closure test at the first unpopulated level
  fails narrowly (it needs `Ξ_u(q)·s_j/(e^bℓ) ≤ θ`; the values are `0.264 × 4.65 = 1.23`), the run goes on to
  `2.2·10⁵`–`1.8·10⁶` outer points (54 to 430 times the outer cube), **populates the spike**, and is then invalid
  from below: the update `ℓ := s_je^{−b}·Θ(p̲)` with Harper's *lower* function of the assumed class gives
  `L/A = 2.37, 2.37, 2.37, 2.38, 3.05, 3.91` in the six sets (the same in all 20 runs of a set; `U = 4.7·A` in
  the first).  (TL) for the assumed class is violated by a factor up to `9.5` on this instance.  All sampling
  certificates are true; the false certificate is `ℓ ≤ A`.
* A scan of `θ` at one parameter set (12 seeds each): `θ ≥ 1.5`: closes below the spike, `A/U` from 277 to
  2 547 (84 of 84 runs invalid); `θ = 1`: `L/A = 2.37` (12 of 12); `θ ≤ 0.5`: the two false bounds contradict
  each other (`L > U`), the abort rule fires in 60 of 60 runs (recorded reason "L>U") and the trivial bracket —
  valid — is returned after `1.8·10⁶`–`3.6·10⁶` points.  With Harper's upper function and the **Markov** lower
  function `Θ = id`: `θ ≥ 1.5` as before (84 of 84 invalid); `θ ≤ 1`: **72 of 72 valid**, at `3.6·10⁶` outer
  points (872 times the outer cube).

*Replacement text for 11.121(c).*  "Run with the tail functions of the assumed class it returns an invalid
bracket in every run [counts].  Two steps are false, and which one decides depends on the threshold and on the
ladder: when the run closes before the spike is populated (in our parameter sets: `θ ≥ 1.5`; at `θ = 1` only for
some ladders) the *upper* tail bound is false and `U` is below `A` by factors of `10²`–`10³·⁶`; when the spike is
populated first, the *lower* tail function (the Harper term of Theorem 11.56) is false and `L` is above `A` (by
`2.4` to `3.9` at `θ = 1`); for still smaller thresholds the two false bounds cross, the abort rule returns the
trivial bracket, and with the Markov lower function alone the run is valid at about `10³` times the cost of
enumerating the outer cube.  In every case all certificates obtained by sampling are true."  And in the paragraph after
11.121: "A certificate format built on the level theorem must carry the bound on the influence **for both tail
functions**."

### F2 [major; decisive for band models] — the remark on hubs is false at finite size

*Line.*  N_REPORT §5.2, last sentence: "*Not a counterexample:* unbounded influence confined to boundedly many
outer sites (a hub): condition on them (`2^{k₀}` sub-problems); the failure needs the influence to be spread, as
here."  THEORY_REPORT 11.121(d): "Not a counterexample: an unbounded influence of boundedly many outer sites
(condition on them)."

*Why it matters.*  A band model **is** the hub case: by the Markov property the conditional law of the inner
block depends on the last `r` outer sites only (Proposition R26.1 below).  Read literally, the remark says that
our instances are outside the failure mode.

*Evidence* [replication; `r26_hub.py`, log `out_hub_4.txt`].  A nearest-neighbour chain of binary sites, 4 outer
and 16 inner sites: the three outer sites away from the cut uniform and independent, the boundary site in its
rare state with probability `π_h`, a coupling of `14 kT` across the cut and of `11 kT` along the inner chain;
residual `u` times the number of sites in state 1 (`u = 1`, additive, in the class).  Pointwise influence of
the boundary site `14`; class-relative influence for `u`-Lipschitz fibre weights `11.45` (= `ln(V₁/V₀)`: attained
by this residual; own recursion, exact for binary chains).  Algorithm A with the exact Lemma N.0 tail functions
of the product-class envelope `u·`Hamming under the true outer marginal; reference point a typical
configuration; `θ ∈ {20, 5, 1}`, 20 seeds each:

| `π_h` | share of the rare state in `A` | (A) product-class tail function | (B) envelope of Theorem N4 | (C) conditioning on the boundary site |
|---|---|---|---|---|
| 0.002 | 99.47 % | **invalid 60 of 60**, `A/U` = 49 to 62, 808–6 464 points | valid 60 of 60, `4.1·10⁵`–`1.7·10⁶` points | valid 60 of 60, 1 464–5 856 points |
| 0.02 | 99.95 % | **invalid 60 of 60**, `A/U` = 454 to 484 | valid 60 of 60, `2.5·10⁴`–`1.0·10⁵` points | valid 60 of 60 |
| 0.2 | 100.00 % | **invalid 40 of 40** at `θ = 20, 5` (`A/U` = 2 082); valid 20 of 20 at `θ = 1` | valid 60 of 60, 3 136–12 544 points | valid 60 of 60 |

A weaker chain (couplings 10 and 7.6 `kT`, 12 inner sites, `ι = 7.98`): (A) invalid in 100 of 120 runs.  In all
260 invalid runs the false certificate is the upper tail bound and every sampling certificate is true.
Control — the same chains without the coupling across the cut — valid in 300 of 300 runs.  The outer space has
16 points; the instance is a demonstration of the mechanism, not of a cost.

*The same in their own setting* [replication; `r26_n12.py hubcube`, log `out_n12_hubcube_1.txt`].  Uniform outer
cube `Q_12`, Harper's functions of slope 1, inner cube `Q_16`, residual `u|b|` — the setting of Proposition N12 —
with the dependence confined to a hub: `p(a) = σ(−6)` if the first `k₀` outer sites are all 1, `σ(+6)` otherwise
(`ln(V_hub/V_rest) = 15.9`); reference data as in my runs of N12 (reference point 0, valid under the dependent
measure; with it `ℓ₀` already lies above the bulk, and the thresholds in the table depend on that choice).  10 seeds per cell, Harper's or the Markov lower function (no difference):

| hub sites `k₀` (probability of the hub state) | `θ = 50` | `θ = 20` | `θ = 5` | `θ = 1` |
|---|---|---|---|---|
| 1 (1/2) | valid 20 of 20 | valid | valid | valid |
| 2 (1/4) | **invalid 20 of 20**, `A/U = 28` | **invalid 20 of 20**, 28 | valid | valid |
| 3 (1/8) | **invalid**, 53 | **invalid**, 53 | **invalid**, 136 | valid |
| 4 (1/16) | **invalid**, 98 | **invalid**, 98 | **invalid**, 252 | **invalid**, 556 |
| 6 (1/64) | **invalid**, 339 | **invalid**, 339 | **invalid**, 871 | **invalid**, 1 921 |

260 of 400 runs invalid, always through the upper tail bound, all sampling certificates true; the runs close
after 816 to 3 472 outer points at a pass with `q` between 1/8 and 1/2 (for `k₀ = 2`: at `q = ½` Harper's
function allows an excess of at most `10.6·s`, and the hub state is `1 300·s`).  One hub site is safe here only
because its state has probability ½, which with `η = ½` makes `q = 1` at every pass.

*What is true instead.*  [P] On the good event the upper end is false only if the run closes at a pass
`(s_j, q)` at which `E(V − s_j)₊ > s_jΞ(q)`.  [H] For the Harper function of an outer cube of dimension `m`, a
hub state of probability `π` is therefore safe when `e^{ι}` is below the depth the assumed class allows to a
set of measure `π`, about `e^{u(r(π)+1)}` with `r(π)` the Harper radius.  For fixed `k₀` and `m → ∞` this
allowance grows like `e^{um/2}` and the remark is right asymptotically; for outer blocks of 4 to 20 sites
`r(π)` is 1 to 6 and an influence of 5 to 12 `kT` at one site breaks validity — whether or not the hub state
is rare (`π_h = 0.2` above).

*Replacement text.*  "Influence confined to boundedly many outer sites (a hub; for a band model: the last `r`
sites) is repaired by conditioning on them (`q^{k₀}` product sub-problems with exactly known weights).  Without
the conditioning the failure is the same as above whenever `e^ι` exceeds what the product-class tail function
allows to a set of the measure of a hub state — at finite size this happens with one hub site (a chain with a
14 `kT` coupling: false brackets in 260 of 300 runs of the Scientific Discovery Division) and, on the uniform cube
`Q_12` with Harper's functions, from two hub sites on (`θ ≥ 20`; four sites: every threshold from 1 to 50); only
for a fixed hub and outer blocks growing without bound does the failure need the influence to be spread."

*Is the repair complete* (Item 2 (iv))?  For validity: yes [P; replication: 0 invalid of 300], given (1) the hub
is the whole set of outer sites with influence (for a band model: exactly the last `r`), (2) the weights of the
hub states are exact (transfer matrix), (3) the failure probability is split over the sub-problems.  Three
limits: the cost is `q^r`, not `2^{k₀}` (81 to `2.8·10⁵` for our alphabets and bandwidths); each sub-problem
still needs a tail function for the *conditional* law of the remaining outer sites, which for a band model is a
chain, not a product (their own open item (f)); and sub-problems of negligible weight should be bounded by
their trivial bracket rather than run.

### F3 [major] — Theorem 11.119(b) and the sentence to this division: "dependence costs slope" is right, incomplete, and for band models the wrong tool

*Lines.*  THEORY_REPORT 11.119(b): "**dependence costs slope** — on the cube, `u ↦ u + ι` per outer flip."
THY-MSG-0018 §2 (as quoted in our brief): "for a band model that influence is computable from the transfer
operator, and whether it is small on your instances decides whether nesting is even valid there".

*What I find* (all [P] here unless marked; numerics in §3).

**Proposition R26.1 (boundary-layer reduction) [P; replication: 24 random models, largest difference
`5·10⁻¹⁴`].**  Let `μ ∝ e^{−E}` on a chain of `n` sites with pair interactions up to sequence separation `r`, cut
after site `c`; write `E = E_o(a) + E_×(a,b) + E_i(b)`, `∂a` = the last `min(r,c)` outer sites, `β = ∂b` = the first
`min(r, n−c)` inner sites, `π_a(β) = μ(∂b = β | a)`.  Then `E_×` depends on `(∂a, ∂b)` only, and for all `a, a′`:
(i) `μ(·|a)` depends on `a` through `∂a` only, so **every** influence — pointwise or relative to any class — is
zero when `∂a = ∂a′`;
(ii) `dμ(·|a)/dμ(·|a′) = e^{Δ(β)}/⟨e^Δ⟩_{a′}` with `Δ(β) = E_×(a′,β) − E_×(a,β)`, a function of the inner boundary
layer only; hence

    ι_pt(a,a′) := max_b ln[μ(b|a)/μ(b|a′)] = max_β Δ(β) − ln Σ_β π_{a′}(β)e^{Δ(β)}   ∈ [0, osc Δ],

and for any class `𝒲` of fibre weights, `ι_𝒲(a,a′) = sup{ln[⟨π_a, W⟩/⟨π_{a′}, W⟩] : W = E[w | ∂b], w ∈ 𝒲}`;
(iii) `π_a(β) ∝ e^{−E_×(a,β)}R(β)`, `R` the backward transfer vector of the inner block.
*Proof.*  (i) and (ii): `μ(b|a) = e^{−E_×(a,b)−E_i(b)}/Z_i(a)` and `Z_i(a)/Z_i(a′) = Σ_b μ(b|a′)e^{Δ(b)}`; given `∂b`
the rest of the inner block is independent of `a`, so `∫w dμ(·|a) = Σ_βπ_a(β)E[w|β]`.  The bounds: a weighted
mean of `e^Δ` lies between its extremes.  ∎

*So: is the influence governed by the interaction across the cut only?*  **Proved** for which outer sites
matter (the last `r`) and for the bound `osc Δ ≤ Σ_{cross pairs} osc`.  **Refuted** for its value: with the same
cross-cut energies (`osc Δ = 6`) a field on the first inner site moves the pointwise influence from `0.047` to
`5.999`, and the rigidity of the inner chain moves the Lipschitz influence from `0.89` to `2.90`
(`out_infl_T5_1.txt`).  The value depends on the inner block through `π_{a′}` (one backward pass) and, for a
class, through the projected class `{E[w|β]}`.

**Proposition R26.2 (box class) [P; replication: 984 cases against all `2^{q^r}` vertex weights, `2·10⁻¹⁵`; 48
cases against a linear programme on the whole inner block, `1·10⁻⁷`].**  For `𝒲 = {l ≤ w ≤ u}` with
`l̄ = E[l|β]`, `ū = E[u|β]`:
`ι_box(a,a′) = ln max_t [⟨π_a, l̄ + (ū − l̄)1_{S_t}⟩ / ⟨π_{a′}, l̄ + (ū − l̄)1_{S_t}⟩]`, `S_t = {β : Δ(β) ≥ t}`; for
`u = e^Dl`, `l ≡ 1`: `ln max_t [1 + (e^D−1)π_a(S_t)]/[1 + (e^D−1)π_{a′}(S_t)] ≤ min(D, ι_pt)`.  (A
linear-fractional function on a box is maximal at a vertex; the vertex is a level set of the likelihood
ratio.)  *Moreover the influence is not needed for this class:* the outer integrands of the class are exactly
the functions with `l̄_o(a) ≤ V(a) ≤ ū_o(a)`, `l̄_o(a) = ∫l dμ(·|a)`, `ū_o` likewise — both transfer-matrix
quantities when the sandwich bounds are band-structured; after the change of reference `V̂ = V/l̄_o` the exact
tail functions of the class are `Ξ(q) = q(e^D − 1)` and `Θ(p) = p + (1−p)e^{−D}`, the same on every space.
Nothing distinguishes the blocks: the constants of the level theorem then need `ν₁ ≥ (e^D − 1)/θ` and give
`π_* ≈ θe^{−2D}` (a sample bound of order `e^{3D}/θ²`), against `O(e^D ε^{−2})` fibre averages for plain sampling
of `V̂ ∈ [1, e^D]`; **nesting gains nothing on a pure sandwich class.**

**Proposition R26.3 (Lipschitz class: a polynomial upper bound) [P; replication: never below the exact linear
programme on any pair of the 126 models of table T3, largest excess 0.40; exact for `q = 2`: 5 chains].**
Nearest-neighbour chain, fibre weights `w` with `w(x) ≤ e^uw(y)` for Hamming neighbours.  Put `v_n(x,y) = u·[x ≠ y]` and, backwards along the inner
block, `v_j(x,y) = u + ln sup{⟨P_j(·|x),W⟩/⟨P_j(·|y),W⟩ : W(z) ≤ e^{v_{j+1}(z,z′)}W(z′)}` (`P_j` = law of site `j+1`
given site `j`; a linear programme in `q` variables).  Then `E[w | b_j = x] ≤ e^{v_j(x,y)}E[w | b_j = y]`, and
`ι_L(a,a′) ≤ ln sup{⟨π_a,W⟩/⟨π_{a′},W⟩ : W(z) ≤ e^{v_{c+1}(z,z′)}W(z′)}`.  Also `ι_L ≤ min(ι_pt, u·k)`.
*Proof.*  Induction: `E[w|b_j = x] = Σ_zP_j(z|x)W^{(x)}(z)` with `W^{(x)}` the projection of the fibre `w(x,·)`;
`w(x,·) ≤ e^uw(y,·)` gives `W^{(x)} ≤ e^uW^{(y)}`, and `W^{(y)}` lies in the cone of `v_{j+1}`.  ∎  For the symmetric
binary chain this is their recursion `v ↦ u + g(v)`; my linear programme on the whole inner block reproduces
their three numbers `1.525944`, `2.740225`, `1.128162` (`(p,u) = (0.3,1), (0.1,1), (0.2,½)`, `k = 6`).

**Proposition R26.4 (the envelope of Theorem N4 on a band model) [P; replication on the 16-point outer space of
F2, all subsets, `out_r264_2.txt`: below the least boundary-state probability the exact function is the same
for `ι = 3, 8, 11.45, 40` and equals the mixture bound; just above it is `10.7`, `1.6·10³`, `5.1·10⁴`, `1.3·10¹⁷`].**  Write `X_o = Y × B` (`B` = states of the
boundary layer) and let the envelope be `ρ = d_Y + ρ_B`, `ρ_B(β,β′) = u·d_H(β,β′) + ι(β,β′)`.  For a set `D` no
slice of which is all of `Y` — in particular whenever `μ_o(D) < min_β μ_o(β)` — every point leaves `D` inside its
own slice, so `Ξ_ρ(q) ≤ sup{Σ_β μ_o(β)Ξ^{(β)}(q_β) : Σ_β μ_o(β)q_β ≤ q}` with `Ξ^{(β)}` the product-class function of
the slice: **below the least boundary-state probability the exact tail function does not contain `ι`.**  A
slice that is entirely inside `D` contributes `μ_o(β)(e^{ρ_B(β → outside)} − 1)` at least: a boundary state rarer
than the closing level has to be resolved inside its own slice (the closing level drops to about `μ_o(β)` times
that of the slice; on the 16-point instance of F2: to its atoms).  Conditioning on the boundary layer is the
stratified form of the same statement and has neither problem.

*Consequences for the two lines.*
1. "`u ↦ u + ι` per outer flip": only at the `r` boundary sites; elsewhere the slope stays `u` (they say so for
   chains).
2. "computable from the transfer operator": **yes** for the pointwise influence and for box classes (closed
   formulas on `q^r` boundary states); for Lipschitz classes the exact value is a linear programme on the whole
   inner block (exponential), and what the transfer operator gives in polynomial time is the upper bound of
   R26.3 (bandwidth 1; for `r > 1` on super-sites — not implemented here).
3. "whether it is small decides whether nesting is even valid": **no.**  Validity is decided by which tail
   function is used.  With the envelope of N4 or with conditioning, nesting is valid for every `ι` (0 invalid of
   600 runs above); with the product-class function it was invalid in 260 of 300 runs, and can be once `e^ι`
   exceeds the allowance described in F2.
   What the size of `ι` decides is accuracy and cost — and there the explicit route is empty at bounded
   accuracy: with the sorted-slope bound of Lemma N14 (the only explicit bound of N_REPORT for unequal slopes)
   on the uniform cube, a single site with `ι ≥ 0.5` moves the closing level at `θ = 1` to the atom — outer
   sample 13 (`m = 12`), 216 (`m = 20`), `4.8·10⁶` (`m = 40`), `9·10¹⁵` (`m = 80`) times the product case — or, at
   equal cost, raises the threshold by `2.9` (`ι = ½`), `8.3` (`ι = 1`), `164` (`ι = 2.5`), `3·10³` (`ι = 5`),
   `6·10⁴` (`ι = 8`); conditioning costs `1.1` to `11` times the product case (`out_cost_2.txt`).  On the
   16-point instance of F2 the exact envelope function needed `3·10³` to `1.7·10⁶` points where conditioning
   needed `1.5·10³` to `5.9·10³`.
4. "with unbounded influence the certificate is false": the *pointwise* influence of a clash is the clash
   energy, unbounded as the clash hardens; the class-relative one is bounded by the oscillation of the class on
   the inner block (`u·k`, or `D`) and, in our models, saturates far below it.  A hard constraint is not by
   itself an obstruction.

*Replacement text for the band-model sentence of 11.119(b).*  "For a band model of bandwidth `r` the conditional
law of the inner block depends on the last `r` outer sites only.  Conditioning on them (`q^r` sub-problems with
weights from the transfer matrix) reduces the problem to product known parts with no hypothesis on any
influence (Theorem 11.119(a)).  Without conditioning, the envelope is `u·d_H + ι(∂a, ∂a′)` with
`ι ≤ min{osc_β[E_×(a′,β) − E_×(a,β)], u·k}`; its exact tail function does not contain `ι` below the least
boundary-state probability; a bound that charges `ι` to every set is valid and has no usable closing level at
bounded accuracy."

### F4 [minor; false certificate if implemented literally] — Lemma N.0 at `q = 1`

*Line.*  N_REPORT §2.1, Lemma N.0: "`Ξ_ρ(q) = sup{∫_D (e^{ρ(x→Dᶜ)} − 1) dμ : μ(D) ≤ q, D ≠ X}` … are tail functions
of the class".  With "`D ≠ X`" the value at `q = 1` is finite on a finite space, while (TU) at `q = 1` forces
`Ξ(1) = +∞` (their own remark two lines above), and `q = 1` occurs in the algorithm at every level below
`min V`.  [review]  *Evidence* [replication, `out_n1_Q1_2.txt`]: `Q_4`, `u = 1`, the member `V = e^{u·d(a,0)}`,
`ℓ₀ = A/10`, `κ₀ = 0.3`, `θ = 2.5`: with the literal formula (`Ξ(1) = 10.947`) the run closes at level 0 with
`U = 0.358·A` in **10 of 10** runs; with `Ξ(1) = +∞`: 0 of 10.  *Replacement:* delete "`D ≠ X`" and state
`inf ∅ = +∞` (the display in THEORY_REPORT §11.33 has no "`D ≠ X`" and is right under that convention), or add
"`Ξ_ρ(1) = +∞`".

### F5 [minor] — Theorem N4: what is used, and what (F1′) hides

(a) *Line:* "for all `a, a′ ∈ X_o` and all `w ∈ 𝒲`".  The proof uses the inequality only for `w = e^{−ψ(a′,·)}`,
the fibre of the same `ψ` at the comparison point [review].  For classes whose fibres depend on `a` (a
sandwich) this is a weaker hypothesis.  Nothing else is used about `ι`: not symmetry (it is not symmetric: in one
chain with a clash across the cut, `out_asym_2.txt`, pointwise `19.55` against `0.62`, box `D = 5`: `3.68`
against `0.61`, Lipschitz `u = 1`: `0.75` against `0.43`), not a triangle inequality (the *exact* class-relative
influence satisfies it automatically, being a supremum of log-ratios; 0 violations in that example), not
finiteness.
(b) *Line:* "(F1′) … *the inner procedures must be valid under every conditional law*".  Satisfiable?  For
validity yes, in three ways [review]: enumeration of the inner block under the known conditional law; Theorem
N1 with the trivial tail function and the cap (after F6); or Theorem N4 again inside the inner block (a band
model given its boundary is a band model with a field).  With a *certified cost below enumeration*: by no
procedure of §11.33 unless the conditional laws are products (as in N12 and in their simulation S3) — the
recursion needs a tail function under a Markov marginal at every level.  *Replacement:* add to 11.119(b) "the
theorem supposes such procedures; for conditional laws that are not products the report has none with a cost
bound below enumeration (instance (f))."
(c) N12(a): "(F1) holds" should read "(F1′) holds".

### F6 [minor] — remark (R5) is not covered by the constants of Theorem N1

*Line.*  N_REPORT §2.5 (R5): "In Theorem N1 … `M ≤ max{K, 2ν(V_max/ℓ₀)e^{−b}}` — with *no* tail function at all
(`Ξ ≡ +∞`)".  With `Ξ ≡ +∞` there is no admissible `π_* > 0`, and `m_max`, `K`, `δ′`, `C_max` are defined through
`π_*` [review].  *Replacement:* "… with `Ξ ≡ +∞`, if in the constants `M̄` is replaced by
`max{K, 2ν(V_max/ℓ₀)e^{−b}}` and `m_max` by `⌈log₂(2ν₀(V_max/ℓ₀)e^{−b})⌉` (no circularity: `ν₀` does not depend on
`K`)."

### F7 [minor] — Theorem N1′ / Proposition N13(b): a positive closing level is a hypothesis of its own

*Line.*  N_REPORT §5.3 (b)(iii) and (c); THEORY_REPORT 11.122: "an upper bound of `A` and a positive closing level
suffice."  Correct [review].  Two precisions.
(a) The closing level can be zero **for the exact tail function of a class with a finite exponential moment**,
not only for a non-sharp bound such as the transport one: on the line with density `∝ e^{−|x|}/(1+x²)` and the
class of 1-Lipschitz `ψ`, `∫e^{|x|}dμ < ∞`, yet the member `V = e^x` has `E(V−s)₊/(s·p(s)) ≥ 0.63·(1+t²)/(t+2)`,
`t = ln s ≥ 0` — unbounded — so no `θ, ν₁` admit a `π_* > 0`: one evaluation certifies a bracket, and Theorem N1′
gives no cost bound at all [P].  Gaps in the outer law have the same effect.
(b) N1′ asks for `Ξ(q) ≤ θν₁q`, not `θ(1−η)ν₀q` (this removes a circularity through `J`; it is in the statement
and deserves a word).  For a Pareto-type tail — `V = e^{ux}` on the Laplace line, `Ξ(q) = q·u/(1−u)` exactly —
there is a closing level iff `θν₁ ≥ u/(1−u)`: with `ν₁ = 1` none for `θ < u/(1−u)` (`out_n1_U_2.txt`).
*Is the cost bound of N1′ finite?*  Iff `π_* > 0`; then `M̄ ∝ 1/π_*`.  On the Gaussian line `π_*` is `1.3·10⁻²`
(`L = 1.5`) and `4·10⁻⁶` (`L = 2.5`) at `θ = 1` and `3.5·10⁻¹³` (`L = 2.5`) at `θ = ½`: finite, of order
`e^{−L²/2−O(L)}` — the size the problem has there, not an empty bound.

### F8 [minor] — the definition of a tail function asks more than the proof uses

(TU) and (TL) are required "for all `s > 0`"; the proof uses (TU) at `s ∈ {s_j}` and (TL) at `s ∈ {s_je^{−b}}`
only (Steps 2, 3) [review].  With the weaker requirement the cap supplies a tail function for free:
`Ξ(q) = q(V_max/s₀ − 1)` at ladder levels, which is what (R5) wants.

### F9 [minor] — Gauss space: what "gains nothing" quantifies over (Item 4)

N10(b) [review]: for **Algorithm A** (any valid tail functions, any inner procedures, any parameters with
`x_out < L²/2`), with the coordinates split **before** the instance is chosen, at the linear instance whose
gradient lies in the outer block, on the good event, the number of **outer points** is at least
`(2K/(1+η))e^{(L−√(2x_out))²/2}` — the exponent of the base family at the same accuracy.  It is not a lower
bound for adaptive algorithms (the text says so), and it is silent for instances whose gradient is spread
over both blocks, hence for random splits (the text says so).  The fixed split is essential to the argument.
With `λ = 1`, `η = ½`, `η′ = 1` (their choice in Corollary N5) `x_out > ln(3e+1) = 2.21`, so the statement is
then non-void only for `L > 2.1`; smaller `λ, η, η′, θ, b` remove the restriction.  In my six runs at
`L = 3` the bound holds with a factor `2 400` to spare (theirs: 560) — it is a bound on the exponent, not on
the cost.  N10(a) is two lines and correct for every nonincreasing `T ≥ 0`.  N9: closed forms re-derived and
checked against quadrature (`3·10⁻¹⁴`); it rests on the Gaussian isoperimetric inequality
`γ(A + rB₂) ≥ Φ(Φ^{−1}(γ(A)) + r)` **[K, from memory — unverified here]**.

### F10 [minor] — numbers

The share of the 13 spike points is `99.9864 %` (N_REPORT: "100.0 %"; THEORY_REPORT: "99.99") — consistent.
The cost with the true class is given as "25 to 225 times" (N_REPORT) and "25 to more than 1 000 times"
(THEORY_REPORT) the outer cube; mine is 872 times in 40 of 40 runs: the multiple is a function of `K` and of the
cap, neither of which the text states.

**Not a finding.**  Theorem N1 and N1′ themselves: I found no error in Steps 1–9 or in the termination
argument of N1′, and none of 1 611 runs in valid settings violated a claim (§3).

---

## 3. Computations and runs, with their controls

All in `experiments/science/ws_R26/`; one core, `OMP_NUM_THREADS=1`, at most two processes, largest peak memory
880 MB, longest run 563 s.  `python3 -B <script> <block> [runs]`; every script exits with status 0 iff it found
no violation of the statements that must hold, and prints its peak memory in its last line.  Seeds are stated
in each log (numpy `default_rng` with an explicit integer per run).

### 3.1 The influence of a band model (Item 1 (ii)) — `r26_band.py`, `r26_influence.py`

Random band models: pair energies `J·N(0,1)` for every pair of states of every pair of sites at separation
`≤ r`; "clash": each such entry replaced by `C` with probability 0.15 (the same entries for every `C`).  Outer
block = first half.  For every ordered pair of boundary states: `osc Δ`; pointwise influence (enumeration of
the inner block, and the formula of R26.1 through transfer matrices); box influence (formula of R26.2);
Lipschitz influence (exact, linear programme on the whole inner block).  **Controls, each able to fail,
violations in every table below: 0** (logs `out_infl_T1q3_1`, `T1q4_1`, `T1q6_1`, `T2_1`, `T3_1`, `T3b_1`, `T4_2`,
`T4b_1`, `T5_1`) — `0 ≤ pt ≤ osc`; `box ≤ min(D, pt)`; `Lip ≤ min(pt, u·k)`; monotone in `D`
and `u`; enumeration = formula; recursion bound ≥ linear programme; the conditional law depends on the last `r`
outer sites only (enumerating `r+1`).  Self-test (`out_band_selftest_6.txt`): 0 violations.

**T1 — coupling scale `J`** (nearest-neighbour, no clash; largest / median over all pairs and seeds).

| `q`, sizes | `J` | `pt` | box `D=1` | box `D=5` | box `D=20` | Lip `u=½` | Lip `u=1` | Lip `u=2` |
|---|---|---|---|---|---|---|---|---|
| 3; `n=10`, `k=5`; 10 seeds | 0.25 | 0.93 / 0.30 | 0.29 / 0.12 | 0.90 / 0.29 | 0.93 / 0.30 | 0.16 / 0.07 | 0.31 / 0.13 | 0.61 / 0.22 |
| | 1 | 4.92 / 1.10 | 0.79 / 0.35 | 3.70 / 1.05 | 4.92 / 1.10 | 0.62 / 0.25 | 1.21 / 0.48 | 2.35 / 0.81 |
| | 4 | 21.8 / 4.30 | 1.00 / 0.58 | 4.99 / 2.11 | 16.6 / 4.30 | 1.06 / 0.43 | 2.26 / 0.85 | 4.90 / 1.59 |
| | 8 | 43.7 / 8.82 | 1.00 / 0.61 | 5.00 / 3.36 | 20.0 / 7.30 | 1.00 / 0.37 | 2.01 / 0.86 | 4.10 / 1.90 |
| 4; `n=10`, `k=5`; 5 seeds | 1 | 3.34 / 1.17 | 0.85 / 0.29 | 3.15 / 1.14 | 3.34 / 1.17 | | 1.22 / 0.45 | |
| | 4 | 14.4 / 4.62 | 1.00 / 0.52 | 5.00 / 2.31 | 14.4 / 4.40 | | 3.47 / 0.97 | |
| | 8 | 28.7 / 9.09 | 1.00 / 0.73 | 5.00 / 2.82 | 20.0 / 7.95 | | 4.09 / 0.99 | |
| 6; `n=8`, `k=4`; 3 seeds | 1 | 3.66 / 1.89 | 0.78 / 0.50 | 3.26 / 1.77 | 3.66 / 1.89 | | 1.12 / 0.73 | |
| | 4 | 15.9 / 8.03 | 1.00 / 0.92 | 5.00 / 4.33 | 15.8 / 8.03 | | 3.61 / 2.00 | |
| | 8 | 31.9 / 15.9 | 1.00 / 1.00 | 5.00 / 4.95 | 20.0 / 13.7 | | 3.98 / 2.67 | |

**T2 — clash energy `C`** (`q = 3`, `n = 10`, `k = 5`, nearest-neighbour, 10 seeds, `J = 1`; largest values; 19 of
the 90 cross-cut entries are clashes).

| `C` | `pt` | box `D=5` | box `D=20` | Lip `u=½` | Lip `u=1` | Lip `u=2` |
|---|---|---|---|---|---|---|
| none | 2.90 | 2.58 | 2.90 | 0.58 | 1.15 | 1.94 |
| 10 | 10.45 | 4.93 | 10.45 | 1.14 | 2.52 | 5.38 |
| 20 | 20.45 | 4.99 | 19.22 | 1.14 | 2.52 | 5.45 |
| 30 | 30.45 | 4.99 | 19.99 | 1.14 | 2.52 | 5.45 |

(`J = 2`: `pt` = 6.3, 11.7, 21.7, 31.7; Lip `u=1` = 1.99, 2.82, 2.83, 2.83.)

**T3 — inner block length `k`** (`q = 3`, nearest-neighbour, outer block of 4 sites, 6 seeds; largest values;
"rec" = the polynomial bound of R26.3).

| case | `k` = 1 | 2 | 3 | 5 | 7 | rec, `k` = 8 … 40 |
|---|---|---|---|---|---|---|
| `J=1`: `pt` | 3.77 | 4.48 | 4.28 | 4.28 | 4.27 | 4.271 (constant to 4 digits from `k = 8`) |
| `J=1`: Lip `u=1` | 0.86 | 1.10 | 1.27 | 1.35 | 1.35 | 1.362 |
| `J=4`: Lip `u=1` | 1.00 | 1.94 | 2.43 | 3.55 | 2.69 | 2.870 |
| `J=1`, `C=20`: Lip `u=1` | 0.98 | 1.51 | 1.84 | 1.99 | 2.00 | 2.005 |

(Not monotone in `k` at `J = 4`: the chains are prefixes of one chain and the backward vector changes.)

**T3b — long inner blocks, larger alphabets** (`out_infl_T3b_1.txt`; the polynomial bound of R26.3 only, `u = 1`,
nearest-neighbour, 6 seeds, largest value over pairs and seeds; other random chains than T3).  The bound is
constant to two digits from `k = 20` on in all 18 cases; its value at `k = 40`:

| | `J = 1` | `J = 4` | `J = 8` | `J = 1`, `C = 20` | `J = 4`, `C = 20` | `J = 8`, `C = 20` |
|---|---|---|---|---|---|---|
| `q = 3` | 1.15 | 2.49 | 2.83 | 1.37 | 2.90 | 2.95 |
| `q = 4` | 1.30 | 3.25 | 5.46 | 1.62 | 2.73 | 2.98 |
| `q = 6` | 1.44 | 5.37 | 6.77 | 1.79 | 6.99 | 7.91 |

(An upper bound: for `q = 3` it exceeded the exact value by up to 0.40 in T3; its slack for `q = 6` is not
known.  On the way it is not monotone: `q = 6`, `J = 8`: `1.00, 2.00, 3.00, 3.91, 4.88, 5.26, 7.52, 5.45, 6.77` at
`k = 1, 2, 3, 4, 5, 6, 8, 12, 20`.)

**T4 — bandwidth `r`** (`q = 3`, `n = 10`, `k = 5`; 4 seeds for `r ≤ 3`, 2 seeds for `r = 4, 5`; largest values;
`s` = distance of the changed site from the cut).

| case | `r` | `pt`, single site `s = 0 … r−1` | `pt`, arbitrary pairs | Lip `u=1`, single site | Lip `u=1`, arbitrary |
|---|---|---|---|---|---|
| `J=1` | 1 | 3.8 | 3.8 | 1.08 | 1.08 |
| | 2 | 6.7, 3.2 | 8.1 | 1.44, 2.04 | 2.45 |
| | 3 | 10.6, 10.6, 4.7 | 13.8 | 2.56, 2.59, 0.92 | 3.33 |
| | 4 | 10.3, 9.1, 11.0, 4.1 | 23.5 | 3.28, 3.22, 1.90, 1.98 | 3.78 |
| | 5 | 10.1, 11.8, 9.5, 3.6, 3.6 | 23.8 | 2.75, 2.50, 2.61, 1.16, 1.36 | 4.05 |
| `J=1`, `C=20` | 1 | 20.9 | 20.9 | 1.85 | 1.85 |
| | 2 | 38.4, 23.7 | 43.0 | 3.25, 3.35 | 3.35 |
| | 3 | 61.8, 42.9, 27.3 | 100.2 | 4.77, 4.87, 3.03 | 4.87 |
| | 4 | 92.9, 68.8, 42.2, 24.1 | 129.4 | 4.99, 4.73, 3.75, 2.74 | 4.99 |
| | 5 | 82.8, 78.7, 75.9, 42.4, 24.1 | 187.8 | 4.97, 4.40, 4.18, 4.23, 4.51 | 5.00 |
| `J=3` | 1 | 11.0 | 11.0 | 2.68 | 2.68 |
| | 2 | 22.1, 11.2 | 26.5 | 2.27, 2.79 | 2.79 |
| | 3 | 31.9, 33.1, 14.3 | 45.8 | 3.40, 4.49, 1.76 | 4.60 |

(Box influences are in the logs; in every row they are at most `min(D, pt)` — a control.  For `r ≥ 4` the
Lipschitz programme was solved for all single-site pairs at `s = 0` and `s = r−1` and for random samples of 300
pairs elsewhere.  With `k = 5` the cap `u·k = 5` binds for `r ≥ 3` with clashes: these rows say "the cap", not
more.)

**Scaling, in words.**  *Pointwise:* linear in `J` (largest `≈ 3.3J` to `5.4J`, median `≈ 1.1J` to `2J`); equal
to the clash energy plus `O(J)` when a cross-cut pair clashes; multiplied by the number of cross-cut pairs
involved (up to `r(r+1)/2`) with the bandwidth; independent of the block length beyond 3 sites.  *Box:*
`min(D, pt)` in effect — it saturates at `D`.  *Lipschitz:* proportional to `u` (T1, T2: within 20 % for
`u = ½, 1, 2`); grows with `J` and with the alphabet and then levels off below the cap `u·k`: at one boundary site (`r = 1`) `1.1u` to `1.4u` at `J = 1`,
`2.3u` to `5.4u` at `J = 4`, `2.8u` to `6.8u` at `J = 8` for `q = 3…6` (T1, T3b); with clashes it rises once (by a
factor up to 2 at `J = 1`) and is then independent of the clash energy from `10 kT` on (T2); it converges with
the block length within 5 to 20 sites (T3, T3b) unless the inner block is rigid, when it grows like `u·k` up to
the pointwise value (`11.4` at `k = 16`, §3.4); with the bandwidth it approaches the cap `u·k` (arbitrary pairs,
`k = 5`: `1.1u`, `2.5u`, `3.3u`, `3.8u`, `4.1u` without clashes for `r = 1…5`; `1.9u`, `3.4u`, `4.9u`, `5.0u`,
`5.0u` with clashes).

### 3.2 Algorithm A, own implementation — `r26_alg.py`

Written from N_REPORT §2.2–2.3: constants, steps 0–3, rule (c0), the four abort rules, the no-cap variant.
Inner procedures: a simulated oracle (brackets of ratio exactly `e^{x_l}` containing the exact `V(a)`,
placement random / top / bottom) — **not end to end**, the same restriction as N_REPORT §7.3.  The checker
tests, with the exact integrand: `L ≤ A ≤ U`; the width; `p(s_i) ≤ q_i` at every level left and at the closing
pass; `p(s_ie^{−b}) ≥ p̲_i`; `ℓ ≤ A`; `E(V−s_j)₊ ≤ tail`; the Chernoff events on the realised sample; `q_j ≥ π_*`
at every level left; `M ≤ M̄`; the stop at a level `≤ J`.  Self-test (`out_alg_selftest_3.txt`): Harper's
functions equal the Lemma N.0 optimum over all 65 534 subsets of `Q_4` at ball sizes and dominate it elsewhere
(`u ∈ {½, 1, 2}`; this replicates their §7.1 A for `m = 4`); the sharpest tail functions of one integrand
satisfy (TU), (TL) with equality somewhere (20 random integrands).

### 3.3 Proposition N12 — `r26_n12.py`

| block (log) | what | runs, seeds | result | control |
|---|---|---|---|---|
| `abc` (`out_n12_abc_2.txt`) | closed form of `V` against enumeration of `Q_16`; `c = 0.735326`, `kc = 11.7652` = largest edge ratio; `A = 1.074731·10⁻³`; spike share `99.9864 %`; bulk max `1.204·10⁻⁷`; pointwise influence `32 = kJ/2` at the threshold, `62` near the top; worst (TU) ratio `1.7474·10⁵` (at `s = V(|a|=9)`, `p(s) = 79/4096`) | — | every number of the text reproduced | Harper's function of the true slope: largest (TU) ratio `10⁻⁴ ≤ 1` |
| `assumed` (`out_n12_assumed_2.txt`) | assumed class, 7 parameter sets × `θ ∈ {20, 1}` | 280; `default_rng(100000·cell + r)` | **invalid 280 of 280**; mechanisms as in F1 | block `control` |
| `scan` (`out_n12_scan_2.txt`) | 13 thresholds, Harper's or the Markov lower function | 312; `default_rng(700000/800000 + 1000i + r)` | as in F1 | — |
| `true` (`out_n12_true_2.txt`) | Harper's functions of the slope `11.7652` | 40 | **valid 40 of 40**; 3 571 712 outer points in every run (872 × the outer cube) | — |
| `control` (`out_n12_control_2.txt`) | **product** known part, the same algorithm and the same tail functions of slope 1, nine integrands in the class (the cone; Harper-extremal dips of radius 1, 2, 4; the smallest log-Lipschitz majorant of the N12 landscape; the flat instance = N12 with `J = 0`; a mixture of cones; a random field; regularised noise), `θ ∈ {20, 1}`, three placements | 540; `default_rng(500000 + 1000c + r)` | **valid 540 of 540**; no other claim violated | mutations: `Ξ/50`, `Ξ/1000`: invalid in 60 of 120 runs; `K = 3`: false sampling certificates in 5 of 60 runs — the control can fail |
| `hubcube` (`out_n12_hubcube_1.txt`) | the setting of N12 with the dependence confined to `k₀ ∈ {1, 2, 3, 4, 6}` outer sites; `θ ∈ {50, 20, 5, 1}`; Harper's or the Markov lower function | 400; `default_rng(1100000 + 1000c + r)` | F2: invalid 260 of 400 | block `control` (same algorithm, same tail functions) |

The instance I ran is the full one (`m = 12`, `k = 16`, `u = 1`, `J = 4`, `τ = 10.5`); only `V` on the 4 096 outer
points enters the outer loop.

### 3.4 A hub on a chain — `r26_hub.py` (`out_hub_4.txt`): see F2.  Exact checks in the same log: `V_h` by transfer
recursion against enumeration of `2^{12}` inner configurations (`5·10⁻¹⁶`); class-relative influence by linear
programme against own recursion (`7.9784` both); (TU) and (TL) with the envelope of N4: worst ratio `1.0000`;
with the product-class envelope: up to `2.6·10⁴` and `184`.

### 3.5 Theorems N1 and N1′ — `r26_n1.py`

| block (log) | what | runs | result | control |
|---|---|---|---|---|
| `S` (`out_n1_S_3.txt`) | 11 integrands on 400 points: an atom at the maximum of mass 0.30, 0.020, 0.0021; a cluster of mass 0.0115 / 0.0010 / 0.20 higher by `10³` / `10⁵` / 30; `V = e^{−X}` with `X` Pareto(0.6) and with `X` = Exp³ (heavy lower tails); two values; flat; lognormal sd 3.  **Sharpest valid tail functions of each integrand** (or `Θ = id`), 6 random parameter sets each (`λ, η, η′, θ, b, κ₀, x₀, ℓ₀/A, V_max`), three placements, 5 seeds | 990 | **no claim violated in 990 runs**; 8 804 levels left as populated, 5 332 as negligible, 339 stops by rule (c0); Chernoff events held in all | mutations `Ξ/20`, `K = 2`, `5Θ`: 156 failing runs of 180 |
| `U` (`out_n1_U_2.txt`) | no cap: `e^{Lx}` on the Gaussian line (`L = 1.5, 2.5`; class tail functions of N9), `e^{ux}` on the Laplace line (`u = 0.5, 0.8`; sharpest tail functions in closed form); four parameter regimes incl. large `η′` | 81 (15 more stopped by my limit of `4·10⁶` points, not counted) | **no claim violated**; **32 levels left as negligible** in the no-cap variant; highest closing level 11 of `J = 20` | (TU), (TL) of the closed forms on 400 levels: excess `≤ 5·10⁻¹²` |
| `Q1` (`out_n1_Q1_2.txt`) | Lemma N.0 literally at `q = 1` | 20 | F4 | — |

### 3.6 Cost of an influence on the cube — `r26_cost.py` (`out_cost_2.txt`): see F3.  Checks: `ι = 0` reproduces
Harper; the sorted-slope bound and the lower function dominate the exact Lemma N.0 functions of the one-hot-site
envelope on all subsets of `Q_3`, `Q_4` (0 violations; the bound is loose by up to `4·10⁴` there, which is the
point of R26.4).

### 3.7 Gauss space — `r26_gauss.py` (`out_gauss_1.txt`): see F9.

---

## 4. The assumption table (Item 3 (iii))

Categories as in N_REPORT §6: **E** essential; **P** required only by the present proof; **C** convenience;
**W** replaceable by a weaker quantitative condition; **X** removal changes the complexity; **F** removal makes
the result false.  First the assumptions of Theorems N1 / N1′ / N4 as I classify them; then the rows of their
table where I disagree.

| # | assumption (where used) | class | evidence here |
|---|---|---|---|
| a | outer points i.i.d. from exactly `μ_o` (Chernoff events) | **E**, **F** | review; with a known density, W (their Lemma N18(b)) |
| b | thresholds fixed by the reference data (binomial counts) | **P** | review |
| c | (TU) for all `s > 0` (Step 3) | **W** → at the levels `s_j` only; **F** if false at the closing pass | F8; N12: all 328 runs that close below the spike |
| d | (TL) (Step 2) | **W** (`Θ = id` always valid), **X** (bounded accuracy), **F** if a wrong `Θ` is used | N12 at `θ = 1`: `L = 2.4A` to `3.9A` in 132 of 132 runs (six parameter sets and the scan) |
| e | `Θ` nondecreasing (Step 5) | **P** (cost only) | review |
| f | `Ξ(1) = +∞` | **E** | F4: 10 of 10 false brackets without it |
| g | `ℓ₀ ≤ A` certified | **E**, **F** | review |
| h | cap `V ≤ V_max` (N1) | **W** → `u₀ ≥ A` and `π_* > 0` (N1′); **F** if the cap is false (a cap derived from the assumed envelope of `V` is false in N12: `0.018` against `0.975`) | review; 81 runs without a cap |
| i | `π_* > 0` (N1′; constants of N1) | **E** for a cost bound; **X**; not implied by an exponential moment | F7 |
| j | atoms / a finite space | **W** (they give `π_* ≥` least atom for free) | F7; their row 11 says C |
| k | inner brackets valid except with probability `δ′`, given the outer points | **E**, **F** | review |
| l | inner calls independent of each other | **C** — not used (union bound) | review |
| m | inner cost bounds hold in every run | **P** (for "at most `C_max` in every run" and for composing levels) | review; their row 15 says C |
| n | rung-0 bracket valid always, ratio uniform in `a` | **E** | review |
| o | `K`, `δ′` as prescribed | **W** (any `K`: failure `≤ (J+1)(m_max+1)(L+2)e^{−η²K/3(1+η)} + …`) | mutation `K = 2, 3` |
| p | (N4) class-relative influence `ι` | **W** → needed only for `w = e^{−ψ(a′,·)}`; for a band model replaceable by conditioning on the boundary layer (**X**: `q^r`); **F** with the product-class function, also for one site | F2, F3, F5 |
| q | (N4) (F1′) procedures under every conditional law | **E** for the method; no procedure with a cost bound for non-product laws | F5(b) |
| r | (N4) `ψ` Lipschitz in the outer variable | **W** (any envelope; for a box class `ln[ū_o(a)/l̄_o(a′)]`) | R26.2 |

**Where I disagree with N_REPORT §6.**

| their row | their class | mine | why |
|---|---|---|---|
| 1 (independent blocks) | W, then F | W, **X**, F | W and F stand; add X: for a band model the influence is confined to `r` sites and conditioning removes the hypothesis at the price `q^r`; and their F-evidence ("needs the influence to be spread") is too narrow (F2) |
| 2 ((F2), known slope) | E, F — "the only step whose failure makes the bracket false" | E, F | "the only" is wrong (corrected in the theory report); add that (F2) fails through *either* tail function (F1) |
| 9 (lower tail lemma) | W | W, **X**, **F**-sensitive | removing it loses bounded accuracy (X); a wrong one gives `L > A` (F1) |
| 10 (bounded oscillation) | W, F | W, **X**, F | the closing level that replaces the cap is not implied by the moment that replaces the diameter (F7) |
| 11 (atoms; finite space) | C | **W** | atoms are not used in the proof, but they are what makes `π_* > 0` automatic; without them it is a hypothesis that can fail |
| 15 (inner costs in every run) | C | **P** | the every-run cost bound and the abort rule rest on it |
| 23 (exact evaluations) | — "not known" | **W** for a bounded, repeatable evaluation error | if every evaluation returns `ψ̃` with `|ψ̃ − ψ| ≤ ε`, `ψ̃` is a function in the class of the envelope `ρ + 2ε[x ≠ z]`, whose tail functions are `e^{2ε}(Ξ(q) + q) − q` and `(1 − e^{−2ε})p + e^{−2ε}Θ(p)`; the bracket of `A(ψ̃)` is one of `A(ψ)` after widening by `e^{±ε}` [P, three lines; not run]; for random noise: not known |
| 25 (fixed split) | C on the cube, P elsewhere | add **X** for dependent known parts | where the cut is put decides `ι` and the probabilities of the boundary states (F2, T4) |

Rows 3–8, 12–14, 16–22, 24: no disagreement from what I checked; rows 4–8, 17–22, 24 concern the exponent
theorems and lower bounds, which I did not review (read only).

---

## 5. What I did not check; my own errors; files

**Not checked (read only).**  The steps of `K_REPORT.md` that the proof of N1 cites (I re-derived Steps 2 and 7
from the statements; I did not see the source).  Proposition N2 (base family) beyond a reading; Corollary N5,
Propositions N6–N8, N19, Lemmas N15–N18 (N14 only as a tool, checked on `Q_3`, `Q_4` for one-hot envelopes);
remark (R6); remark (R7) was re-derived.  Proposition N11 and the cap bound it cites.  Proposition N13(a)
beyond its first sentence (re-derived) — the statement for randomised procedures was repaired by their
referee, whose text I do not have.  The claim that the cube's constants are reproduced (their §7.2) and the
numbers on the transport bound in 11.118.  Their simulation S3 (`1.3120` etc.; parameters not stated) — the
formula behind it is verified by linear programme in four cases.  The Gaussian isoperimetric inequality was not
looked up.  **No end-to-end run with real inner procedures** exists here either: my inner procedure is an
oracle.  Bandwidth above 5, alphabets above 6, inner blocks above 8 sites (linear programme) were not
computed; the polynomial bound R26.3 is implemented for `r = 1` only.  Prior art for R26.1–R26.4 was not
searched (the box influence is a Neyman–Pearson statement and R26.3 a Dobrushin-type recursion; I claim no
novelty).  The figure "0.055 nats per site" in the paragraph of §0 is my arithmetic on their exponents
(`a = ln 2 − H(1/(1+e)) = 0.111`, two levels `≈ 0.50·a`), not a result of theirs or mine.

**My own errors.**
1. *A file written outside my directory.*  At 22:31 UTC a section of notes went to
   `/home/user/MetricChain/NOTES.md`: a command of the form `cd <dir> && … &` put the `cd` into a background
   subshell and the following relative path resolved in the repository root.  The coordinator pointed it out;
   the section was appended to my own `NOTES.md` and the stray file (untracked) removed by its exact name.
2. *Three wrong versions of my own check of the box formula* (`out_band_selftest_1…3.txt`: 10, 143, 171 false
   "violations"): a linear programme at `D = 12` whose solver tolerance exceeded the effect; a residual with
   cancellation; an optimality condition that ignored configurations of mass below `10⁻¹⁷`.  The formula was
   right each time; the final check is exhaustive over all vertex weights.
3. *A crash:* `out_infl_T4_1.txt` (the solver returned "Status 0: Not Set" on a programme whose coefficients
   span 60 decades).  Coefficients below `10⁻¹⁵` of the largest are now truncated (effect `< 10⁻⁸`) and two other
   solver methods are tried; 2 of 9 360 solves in T4 used the fallback.  The crashed log is not cited.
4. *A misjudged running time:* `out_infl_T1_1.txt` was stopped by me before its last line; not cited.
5. *A tie on the level grid in my harness:* with `V_max` exactly on the grid, `s_J` fell one ulp short and my
   checker flagged "level `> J`" 18 times on the flat integrand (`out_n1_S_1.txt`); `J` is now the larger
   integer in that case, which the statement allows.
6. *The first two versions of the hub experiment* (`out_hub_1.txt`, `out_hub_2.txt`) evaluated the reference
   bound at the configuration where the residual is smallest, which puts `ℓ₀` within a factor 3 of `A` and
   makes the false brackets mild (`A/U ≈ 1.1`); the reference point is now a typical configuration.  Both logs
   are kept; the headline numbers are from `out_hub_4.txt`.
7. *A wrong check in the cost script* (`out_cost_1.txt`, crashed): it compared Harper's raw lower function,
   which can lie below the Markov bound, and asked for all subsets of `Q_5`.
8. *Predictions that failed.*  Before running I expected the instance of N12 at `θ = 1` to be possibly valid;
   it is invalid through the lower end, a mechanism I had not anticipated.  My first hand value of the (TU)
   violation was `7·10⁴` (one level); the maximum over levels is `1.75·10⁵`.
9. *A blocked wait.*  A foreground `sleep 100` was refused by the harness; I did not work around it.

**Files** (`experiments/science/ws_R26/`).  `NOTES.md`; `r26_band.py` (band models, three influences, the
recursion, self-test), `r26_influence.py` (tables T1–T5), `r26_alg.py` (Algorithm A, tail functions, checker),
`r26_n12.py`, `r26_hub.py`, `r26_n1.py`, `r26_cost.py`, `r26_gauss.py`, `r26_asym.py`, `r26_r264.py`.  Logs that reached their last line and
are cited: `out_band_selftest_6.txt`, `out_alg_selftest_3.txt`, `out_infl_T1q3_1.txt`, `out_infl_T1q4_1.txt`,
`out_infl_T1q6_1.txt`, `out_infl_T2_1.txt`, `out_infl_T3_1.txt`, `out_infl_T3b_1.txt`, `out_infl_T4_2.txt`,
`out_infl_T4b_1.txt`, `out_infl_T5_1.txt`, `out_n12_abc_2.txt`, `out_n12_assumed_2.txt`, `out_n12_scan_2.txt`, `out_n12_true_2.txt`,
`out_n12_control_2.txt`, `out_n12_hubcube_1.txt`, `out_hub_4.txt`, `out_n1_S_3.txt`, `out_n1_U_2.txt`, `out_n1_Q1_2.txt`,
`out_cost_2.txt`, `out_gauss_1.txt`, `out_asym_2.txt`, `out_r264_2.txt`.  Logs kept and **not** cited (earlier versions, own
errors, or runs that did not reach their last line): `out_band_selftest_1…5.txt`, `out_alg_selftest_1…2.txt`, `out_infl_T1_1.txt`,
`out_infl_T4_1.txt`, `out_n12_*_1.txt`, `out_hub_1…3.txt`, `out_n1_S_1…2.txt`, `out_n1_U_1.txt`,
`out_n1_Q1_1.txt`, `out_cost_1.txt`.

---

## Coordinator's note (2026-11-26/27; replaces the placeholder that stood here at checkpoint 68)

*What the coordinator did with this report before publishing it as SCI-REV-0027.*

**Read:** all of it (the body of some very long table rows only as far as the first 380 characters).  The
theory division's §11.33 and `N_REPORT.md` are unchanged between the commit reviewed (`4692f59`) and their head
at publication (`07cde81`; diff checked), so the findings apply to the current text.

**Checked, and how.**
1. *F2, the finding that decides most* — **replicated independently** (`experiments/science/r26_verification/hub_tail_check.py`
   and `.log`; written from the statement, without the referee's code and without running the nested
   algorithm).  On the referee's chain (4 outer sites, 16 inner; couplings 14 and 11 `kT`) the outer
   integrand exceeds the product-class envelope by 10.449 nats across the one boundary site;
   `ln(V₁/V₀) = 11.4486` (report: 11.45); the inequality the algorithm's upper end rests on fails by a factor
   `1.75·10⁴` to `2.58·10⁴` against the *exact* tail function of the product class computed over all `2¹⁶`
   subsets (report: "up to `2.6·10⁴`"); with the envelope that carries the influence at the boundary site, and
   on the same chain without coupling across the cut, the worst ratio is exactly 1.  Weaker chain: 7.9784
   (report: 7.98), factors 543 to 803.  A prediction written before the run was met in every part.
2. *Re-runs of the referee's scripts* (same machine, its code — a re-run, not a second implementation):
   `r26_hub.py`, `r26_n12.py abc`, `r26_n12.py assumed`, `r26_n12.py hubcube 10` — output identical to the
   committed logs line for line, timing lines apart; `r26_n1.py Q1` with five runs instead of ten — the same
   outcome (false bracket in 5 of 5 with the literal formula, 0 of 5 with `Ξ(1) = +∞`).  `r26_n12.py hubcube`
   with **other seeds** (20 per cell): invalid in 520 of 800 runs — the same fraction as the report's 260 of
   400, so the counts are not a matter of seeds.
3. *By reading:* the proof of Proposition R26.1 (three lines, correct); the vertex argument of R26.2; the
   slice argument of R26.4; F4 (at `q = 1` the hypothesis of (TU) holds for every level below the minimum, so
   a finite `Ξ(1)` cannot be valid).

**Not checked by the coordinator:** the review of the proofs of Theorems N1 and N1′ (taken from the referee);
tables T1–T4 of the influence (their controls are in the logs; not re-run); Proposition R26.3 beyond its
statement; the cost comparison of §3.6; the Gauss-space section; the assumption table row by row.

**Judgement.**  F1, F2 and F3 are accepted as major; each is a correction of a sentence, not of a theorem —
every theorem the referee examined stands.  F2 matters most outside the theory division: its remark, read
literally, places every band model outside the failure mode, and a band model is exactly the case in which the
dependence sits on boundedly many sites.  The operational conclusion — on a band model, condition on the
boundary layer, or do not nest — is the referee's and is adopted.  Two statements of the report are the
referee's own arithmetic on the theory division's exponents and are marked [H] there ("0.055 nats per site";
the break-even lengths 80 to 230): they are quoted in SCI-REV-0027 as heuristic.  The agent reported one
declined tool action (a foreground wait for its own background jobs, blocked by the harness; not worked
around; nothing was asked of the coordinator), opened no web address, used no state-changing git command.
