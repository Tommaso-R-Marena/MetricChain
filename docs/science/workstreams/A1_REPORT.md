# Workstream A1 — prior art and originality of the query-complexity cluster

Science division, independent workstream.  Read at theory head `5ed4072`.
Working files: `experiments/science/ws_A1/` (`NOTES.md` is the step-by-step log; scripts and outputs
are listed in §3).  Downloaded papers were kept outside the repository (scratchpad) and are
identified below by arXiv number / DOI.

**Labels** (COMMON rule 6): **[V]** machine-checked, **[P]** paper proof given here, **[K]** known and
cited, **[N]** numerical evidence only, **[C]** conjecture, **[H]** heuristic.
**Reading levels** (COMMON rule 5): `[full text]` — I downloaded the PDF and read the stated parts
myself in the extracted text; `[abstract]`; `[search snippet]` — only what a search engine returned;
`[from memory — unverified]`.  Where I read only part of a paper the part is named.
*Independent review* = I read and re-derived; *independent replication* = I re-computed with my own
code.  Both are used below and only where done.

---

## 1. Verdicts

**In one paragraph.**  Of the eight claims, one is established prior art, three are best described
as known special cases or reformulations with a new minimax wrapper, two are plausibly original
theorems, one is a plausibly original generalisation, and one is a new combination (one half of
claim 5 is left unresolved).  (i) The
odds-ratio lemma (Lemma 11.89, G27) **is in print**: Hasenclever & Scholz, *Comparing measures of
association in 2×2 probability tables*, Open Stat. Probab. J. 7 (2016) 20–35 (arXiv:1302.6161, 2013),
Proposition 8(a) — with a five-line proof that is shorter than the report's; I re-derived it and
checked it numerically.  (ii) The non-adaptive exponent function `θ_na` of G18 and the threshold
constant `n ln cosh(βc/2)` of G11 are, at the extremal instance (the cone), **the published
"freezing" formulas of the discrete random energy model for the Jarzynski free-energy estimator**
(Suárez, Silbey, Oppenheim, Phys. Rev. E 85, 051108 (2012), eqs. (39)–(46)) and, at bounded accuracy,
Chatterjee–Diaconis' Theorem 3.4; I verified the coincidence of the formulas to `4·10⁻¹⁵`.  What the
theory division adds is the *minimax* statement (all non-adaptive algorithms, the whole Lipschitz
class), by Mathé–Novak's method and Harper's theorem.  (iii) The statement "adaptivity replaces the
hint" with exact exponents (G20/G21) **was not found** in any of the literatures opened (information-
based complexity, normalising constants, importance sampling, pure-exploration bandits, sampling-
oracle counting, nested simulation); its concept has clear precedents (Mathé–Novak 2007: adaption
breaks an exponential barrier of non-adaptive Monte Carlo for a log-concave class; Karnin 2016 and
Chernoff-type sequential design: identification is asymptotically as cheap as verification), and in
the units of information-based complexity it says something quite classical-looking: **the adaption
gain in the (multiplicative) error equals the cardinality `N`** — a linear functional on a
non-symmetric convex cone, relative error, function values.  (iv) The flat-histogram statements
(G22, G25) are the classical capacity / universal-mixture phenomenon plus the invariance principle
of design theory; the new content is the asymptotic isoperimetric theorem for the type-uniform
reference and the two-phase "shell" numerics, neither of which I could settle from the literature.
(v) The round hierarchy (G26) was not found; rounds of adaptivity for partition-function estimation
are a 2026 topic in the *sampling-oracle* model, where one round suffices.  (vi) One new statement
came out of the comparison with the importance-sampling literature (Proposition A1.1, §2.5): for a
product reference measure the class-wide non-adaptive upper bound at bounded accuracy follows from
the chain rule and the Chatterjee–Diaconis truncation, with `exp(na + O(√n))` samples from a
*product* measure, for every `n` — no Harper, no types; with a field it supplies an upper bound the
theory report lists as missing and shows that the flat histogram is not needed at bounded accuracy.

| # | claim (theory report) | classification | one-line reason |
|---|---|---|---|
| 1 | G20/G21, Thms 11.54, 11.58: adaptive exponent = hinted exponent | **(6) plausibly original theorem** | not found after full-text reading of the closest sources; concept has precedents; proof status is the theory division's (paper proof, internally refereed) |
| 2 | G18, Thms 11.44–11.45: Monte Carlo exponent-optimal among non-adaptive algorithms | **(3) known special case exists** | the exponent function is the published REM/Jarzynski bias curve at the cone (S–S–O 2012) and the Chatterjee–Diaconis threshold; lower-bound method is Mathé–Novak's; new = minimaxity over class and algorithms |
| 3 | G22, Thms 11.59–11.64: field; flat histogram; additive hardest instance; isoperimetry for the type-uniform reference | **(4) plausibly original generalisation** | sampler statement = capacity-achieving output law / universal mixture (known); Thm 11.63 is a new variant of Ahlswede–Zhang/Yu by their method |
| 4 | G23: shear law, game-function pair theorem | **(2) reformulation of a known result** | the shear law is the exponential change of measure `KL(ρ‖p_u) = KL(ρ‖½) + uρ − Λ₁`, in print as the REM form "`ln M` + frozen energy"; Thm 11.66 is Gallager-type restricted Legendre duality packaged for G20 |
| 5a | G25, Thm 11.76: type-stratified sampling optimal among fixed samples by symmetry | **(2) reformulation of a known result** | invariance principle (invariant designs are optimal; Kiefer) + Bakhvalov averaging over the group; one small new lemma (type-wise quantile truncation is Lipschitz) |
| 5b | G25, Prop. 11.82: shells in the barrier class | **(9) unresolved** | numerical statement; no literature found, not checked by me |
| 6 | G26, Thms 11.84–11.86: two rounds strictly between | **(6) plausibly original theorem** | not found; conditional on #1; unrefereed; method (virtual-run coupling) is standard round elimination |
| 7 | G27, Lemma 11.89: odds-ratio lemma | **(1) established prior art** | Hasenclever–Scholz 2013/2016, Prop. 8(a), statement and uniqueness of the maximiser |
| 8 | G11, Thm 11.25: threshold `n ln cosh(βc/2)`, soft gap | **(5) new combination** | the constant is the maximal bias of the one-sample estimator (S–S–O eq. (44)) / the two-point Jensen gap; its role as a sharp complexity threshold (hidden Lipschitz dips below it) was not found |

**What would survive a hostile referee** is §8.

*Changes since the first complete version of this report* (18:20 UTC, from which the coordinator's
message `SCI-REV-0004` was drawn; listed so that the message can be brought up to date):
(1) **Proposition A1.1 (§2.5) is new** — the class-wide upper bound for the product sampler
`Bern(r*)ⁿ` at bounded accuracy, which the first version called "not proved", is now proved (chain
rule; checked by enumeration), so request T4 changed from "decide whether" to "check and adopt";
(2) the sentence that the nested algorithm "answers the question Mathé and Novak leave open" was
too strong — neither their paper nor the Novak–Rudolf survey poses the non-log-concave question
(§8, §4.10); (3) "the strict inequality … cannot hold at `0⁺`" was made precise: the two sides
coincide *in the limit* `ε₁ → 0⁺` (§2.3); (4) §2.4 now contains a proof that in *absolute* error the
adaption gain disappears; (5) the two headline numbers of G26 were re-computed (§3, §4.6);
(6) the theory division's own earlier mention of the Suárez–Silbey–Oppenheim paper (by title) is
recorded (§2.2); (7) search log: 25 queries; seven scripts; (8) **§9 is an addendum** written on a
later request: questions B1 and B2 of the theory division's THY-REQ-0011 (the channel-coding
dictionary of their new Theorem 11.99), with Proposition A1.2 — the generalisation of Proposition
A1.1 to their heteropolymer setting — ten more searches and an eighth script.
*State at 19:10 UTC:* (1) has since been taken up by the coordinator (`SCI-RES-0001` §2), and
`SCI-REV-0004` already has the wording of (3); **only (2) still affects `SCI-REV-0004` as it stands**
(the sentence "answers, on a model class, the question Mathé and Novak leave open").

---

## 2. Precise statements, with proofs

### 2.1 The odds-ratio lemma is Hasenclever–Scholz Proposition 8(a) — and has a five-line proof

*Statement in the theory report* (§11.25, Lemma 11.89).  For a pair `(B, X)` of binary variables with
positive probabilities `P_{bx}` and `ln[P₁₁P₀₀/(P₁₀P₀₁)] = 2s ≥ 0`:
`I(B;X) ≤ ln 2 − h(σ(s))`, `σ(s) = 1/(1+e^{−s})`, with equality iff `s = 0` or both marginals are uniform.

*Statement in print* **[K, full text]**.  Hasenclever & Scholz use the coordinates
`(x, y, z) = (ln√(p₀₀p₁₁/p₀₁p₁₀), ln√(p₀₀p₀₁/p₁₀p₁₁), ln√(p₀₀p₁₀/p₀₁p₁₁))` on the manifold of positive
2×2 tables; `x = s` is half the log odds ratio, the planes `x = const` are the orbits of the "margin
transformations" (multiplying rows and columns by positive numbers), and `(y, z) = (0, 0)` is the
table with diagonal symmetry, i.e. uniform margins.  Their Proposition 8 reads: "For all
`x ∈ ℝ∖{0}`: a) `sMutInf_x` has exactly one maximum at the origin `(y, z) = (0, 0)`. b)
`lim_{‖(y,z)‖→∞} sMutInf_x = 0`", where `sMutInf = sign(D)·`(mutual information in bits) and the
subscript is the restriction to a fixed odds ratio (for `x < 0` the signed quantity has its unique
*extremum*, a minimum, there; the case `x > 0` is the one stated).  This is Lemma 11.89 with its
equality case.
The value at the origin, `(√λ/(1+√λ)) log √λ − log(1+√λ) + log 2` with `λ = e^{2s}`, is written out in
Williams (Neural Computation 34 (2022), eq. (10)) **[K, full text]**, who also observes on Yule's
smallpox table that "the MI is lowest in the original (unbalanced) table, and increases as the
marginals are balanced".  The report's "equivalently: among binary-input binary-output channels with
a given odds ratio the symmetric one has the largest capacity" is an immediate corollary (capacity
is a maximum over one margin); I did not find the capacity phrasing in the information-theory
literature (three searches).

*A short proof* **[P; independent review of the Hasenclever–Scholz argument, which I re-derived and
completed to a global statement; every step checked numerically, §3 T2–T3]**.
Let `P` be a positive table with odds ratio `λ ≠ 1`, `ι = ln[P/(P_B ⊗ P_X)]`, `I = E_P ι > 0`.

1. *Diagonal flow.*  `P_t ∝ (e^{t}p₀₀, p₀₁; p₁₀, e^{−t}p₁₁)` has the odds ratio `λ` for every `t`.
   It is an exponential tilt by `φ = 1_{00} − 1_{11}`, and the three scores have mean zero, so
   `dI/dt = Cov(ι, φ) = (p₁₁ − p₀₀)·I + p₀₀ι₀₀ − p₁₁ι₁₁`.
2. `(p₀₀+p₀₁)(p₀₀+p₁₀) = p₀₀(1 − p₁₁) + p₀₁p₁₀ = p₀₀(1 − c·p₁₁)` with `c = 1 − 1/λ`; hence
   `ι₀₀ = −ln(1 − c p₁₁)`, `ι₁₁ = −ln(1 − c p₀₀)`, and
   `dI/dt = (p₁₁ − p₀₀)·I + p₀₀p₁₁·[g(p₀₀) − g(p₁₁)]`,  `g(x) = ln(1 − cx)/x`.
3. `x ↦ ln(1 − cx)` is strictly concave and vanishes at `0`, so its chord slope `g` is strictly
   decreasing (for `c ∈ (0,1)` and for `c < 0`).  Both terms therefore have the sign of `p₁₁ − p₀₀`.
4. Since `p₀₀(t)/p₁₁(t) = e^{2t}p₀₀/p₁₁` is strictly increasing, `I(P_t)` increases strictly up to the
   unique `t*` with `p₀₀ = p₁₁` and decreases strictly afterwards: `I(P) ≤ I(P_{t*})`, with equality
   iff `p₀₀ = p₁₁`.
5. *Off-diagonal flow.*  Swap the columns (odds ratio `1/λ ≠ 1`, same `I`) and repeat: `I` is
   maximal exactly where `p₀₁ = p₁₀`; this flow keeps `p₀₀ = p₁₁`.  The end point has uniform margins
   and the odds ratio `λ`: it is the canonical table, whose mutual information is `ln 2 − h(σ(s))`.  ∎

So the lemma is a consequence of one named fact — *concavity of the logarithm* (the chord slope of
`ln(1 − cx)` decreases) — and of the covariance formula for derivatives along an exponential tilt.
The report's own proof (Ising parametrisation, six steps, the kernel inequality (4)) is correct as
far as I can tell — I checked its gradient formula, `T < 0`, the kernel inequality with its closed
form, the location of the maximiser and the monotonicity of the capacity numerically
(`odds_ratio_report_proof_check.py`) — but it is not needed.

*Two side remarks* **[K/P]**.  (a) The capacity of a binary-input binary-output channel with output
laws `Bern(a)`, `Bern(b)` is the largest chord gap of the binary entropy between `a` and `b` (the
Jensen gap; textbook), equivalently a Bregman information radius of the two natural parameters for
the cumulant `ln cosh`; in these terms the lemma says that this radius, at a fixed distance of the
natural parameters, is largest for the pair that is symmetric about `0` (checked, §3 T4).  The same
"chord gap of the pressure" is the theory report's hint-free threshold for two-state sites
(Theorem 11.28(e)).  (b) The lemma is a 2×2 fact: for a three-letter Potts pair at slope `0.3`,
`I = 0.010582` with uniform weights on three letters against `0.011125` on two letters (§3 T7), in
agreement with the report's remark after Corollary 11.91.

*Consequence for the theory report.*  Row G27 and §11.25 should cite Hasenclever & Scholz for the
lemma; "may well be folklore" becomes "known".  Theorem 11.90 and Corollary 11.91 (slices are never
harder than the cube) are *applications* of the lemma and are unaffected; I did not find them in
print and did not check them.

### 2.2 The non-adaptive exponent function and "ln cosh" are published REM formulas at the cone

*Statement in the theory report* (§11.16, Theorems 11.44–11.45; §11.10, Theorem 11.25).  On
`L_u = {g : |g(x) − g(y)| ≤ c·d_H(x,y)}` (`u = βc`), with `p_u = 1/(1+e^u)`, `Λ₁ = ln(2/(1+e^{−u}))`:
non-adaptive algorithms have the exponent `θ_na(ε₁) = min{KL(ρ‖½) : KL(ρ‖p_u) ≤ ε₁}` at accuracy `ε₁n`
and `a = KL(p_u‖½)` at bounded accuracy; above `ε₁ = ln cosh(u/2)` a bounded number of evaluations
suffices.

*In print* **[K, full text of the cited section and appendix]**.  Suárez, Silbey & Oppenheim study the
Jarzynski estimator `ΔF_M = −log(M⁻¹Σ_m e^{−εn_m})` with `n_m ∼ Bin(N, ½)` i.i.d. ("sudden compression
of an ideal gas").  This *is* plain Monte Carlo for `−ln A` at the cone `u·d_H(·, s)` with `ε = u`,
`N = n`, `M = e^{nθ}` uniform samples.  With `γ = log M/(N log 2)`:

| Suárez–Silbey–Oppenheim 2012 | theory report |
|---|---|
| (31) `ΔF = N log(2/(1+e^{−ε}))` | `nΛ₁`, the "soft gap" of one site times `n` |
| (41) `ε_c(γ) = log[(1−ρ)/ρ]`, `ρ = h₂⁻¹(1−γ)` | `ρ = ρ_θ`, the radius with `KL(ρ_θ‖½) = θ = γ ln 2`; `ε > ε_c ⇔ ρ_θ > p_u` |
| (43) bias `B_M = N[γ log 2 + ε/(1+e^{ε_c}) − log(2/(1+e^{−ε}))]` for `ε > ε_c`, `0` otherwise | `n·KL(ρ_θ‖p_u)` — the accuracy rate that `e^{nθ}` non-adaptive points certify; its inverse function is `θ_na` |
| (44) "the bias is maximum for `M = 1`: `B_max = N log cosh(ε/2)`" | the threshold `n ln cosh(βc/2)` of Theorem 11.25 |
| (46) `γ_c(ε) = 1 − h₂(1/(1+e^ε))` | `a = KL(p_u‖½)` |
| the form "`N γ log 2` + (energy of the frozen level)" in (39) | the shear law: non-adaptive accuracy `=` `ln N` `+` hinted accuracy `(uρ_θ − Λ₁)n` |

The translation uses only `KL(ρ‖p_u) = KL(ρ‖½) + uρ − Λ₁` **[P; verified numerically on 1600
parameter pairs to `4·10⁻¹⁵`, §3 E2]**.  Their derivation is the physicists' mapping onto the
*discrete random energy model* (binomial energy levels; Moukarzel–Parga 1991, Ogure–Kabashima 2009,
as cited there), for the expectation of the logarithm in the scaling limit; the mathematical
background is the theory of sums of random exponentials (Ben Arous–Bogachev–Molchanov 2005
**[search snippet]**).  At bounded accuracy the same threshold is Chatterjee–Diaconis' Theorem 3.4
**[K, full text]**: with `n = e^{bL_N}` samples from `G_{β₀}`, `Ẑ/Z → 1` iff
`b > q(β) = p(β₀) − p(β) − (β₀−β)p′(β)`; for the cone sampled uniformly `q(u) = KL(p_u‖½) = a`
(§3 E2e).  I also simulated the estimator (§3 E5): the deficit `ln(A/Â)/n` at `θ = a/2`, `u = 1` is
`0.0166, 0.0123, 0.0112, 0.0108` at `n = 500 … 32 000`, limit `0.0106`.

*What the theory division already had.*  Its workstream D (`docs/workstreams/D_REPORT.md`, §9, written
for G15, before §11.16) lists "Suárez et al. (2012, 'phase transition in the Jarzynski estimator')"
among sources read as "titles and summaries only", with the correct general remark that this
literature is about "a *given* pair of systems and a *given* estimator".  The coincidence of the
*formulas* with `θ_na`, `a` and `ln cosh(u/2)` was not noticed there, and §11.16, row G18 and L7 do
not cite the paper.

*What is not in these sources:* a class of instances, a minimax statement, a lower bound for all
non-adaptive algorithms, `(ε, δ)`-statements for every `n`, adaptive algorithms.  So the sentence
of row G18, "the exponent on the cube for `ln Z` … [was] not found", should become: *the exponent
function is the known freezing curve of the Jarzynski estimator at the cone (Suárez–Silbey–Oppenheim
2012; Chatterjee–Diaconis 2018 at bounded accuracy); new is that the cone is the worst instance of
the class for plain Monte Carlo (Harper) and that no non-adaptive algorithm does better
(Mathé–Novak's averaging).*

### 2.3 The bounded-accuracy non-adaptive exponent is a channel capacity; consequence for product samplers

*Observation* **[P, given the cited theorems; numerically checked, §3 C1–C4]**.  The Gibbs laws of
the cones `u·d_H(·, s)` over a `p`-biased reference are the output laws `Wⁿ(·|s)` of the *memoryless
channel* `s_i → x_i`, `W(x|b) ∝ π(x)e^{−u[x≠b]}`.  The theory report's `a = max_m I_{π_s}(S;X)`
(Theorem 11.59(c)) is therefore the **capacity** of `W`; on the uniform cube `W` is the binary
symmetric channel with crossover `p_u` and `a = ln 2 − h(p_u) = KL(p_u‖½)`.  By the classical
identity *capacity = minimax redundancy (information radius)*,
`max_{P_S} I(S;X) = min_Q max_b D(W(·|b)‖Q)`, attained at the capacity-achieving output law `Q*` —
"a classical result by Gallager and Ryabko" in the words of van Erven & Harremoës (IEEE Trans. Inf.
Theory 60 (2014); arXiv:1206.2459, section "Channel capacity and minimax redundancy" **[K, full text
of that passage]**; the identity is also verified numerically, §3 C1) —

    min over product proposals Bern(r)ⁿ of  max_s KL(Wⁿ(·|s) ‖ Bern(r)ⁿ)/n   =   a,     attained at r = r* = Q*(1).

*Consequences.*  (a) "Plain Monte Carlo is optimal on the uniform cube" (G18) at bounded accuracy is
"the uniform law is the capacity-achieving output law of the BSC" + the `e^{KL}` rule + Mathé–Novak
averaging.  (b) With a field (G22), the optimal *product* proposal is not the Gibbs measure `π` of
the known part but `Bern(r*)ⁿ` with `r*` between `p` and `½` (`r* = 0.4308, 0.3607, 0.2225, 0.1124`
against `p = 0.3775, 0.2689, 0.1192, 0.0474` at `u = 2`); and **at vanishing accuracy this single
product measure has the same worst-case KL exponent `a` as the flat-histogram sample**.  Hence the
product-sampler lower bound `max(φ₀, φ₁)` of Theorem 11.61, minimised over `r`, tends to `θ_na(0⁺) = a`
as `ε₁ → 0⁺` (for `r` between the two cone marginals `φ_b(0⁺) = D(W(·|b)‖Bern(r))`, and the minimum
over `r` of the larger one is the information radius): the strict inequality
`min_r max(φ₀, φ₁) > θ_na`, which the report states as "not proved in general", **becomes an equality
in that limit**, so it can at best be an extensive-accuracy statement; the reported gaps of 0.5–3 %
indeed shrink with `ε₁` (1.3 % at `0.05E`, 2.5 % at `0.25E` in the report's own numbers).  That
`Bern(r*)ⁿ` really attains `a` on the *whole class* at every bounded accuracy is Proposition A1.1 of
§2.5.  (The report's remark that the isoperimetry of a fixed product measure "gives the worse
exponents" is about `π` itself, not about `Bern(r*)ⁿ`, and is not contradicted.)
(c) I reproduced the report's table of §11.20 (`u = 2`, fields `0, 0.5, 1, 2, 3`): `a = .3278, .3162,
.2836, .1841, .0928` and plain Monte Carlo `.3278, .4078, .4621, .4338, .2732` — **independent
replication, identical to the printed digits**.  The report's own remark (3) of §11.20 already
identifies `μ_H` with the Shtarkov (NML) distribution; the capacity reading and the tie with a
product measure at bounded accuracy are the additions.

### 2.4 The shear law in the units of information-based complexity: adaption gains the cardinality

*Restatement* **[P — a rewriting of Theorems 11.44/11.45/11.54 as they stand, no new mathematics]**.
Let `ε_na(N)` and `ε_ad(N)` be the best accuracies (in `ln Z`) that non-adaptive, resp. adaptive,
randomised algorithms with `N = e^{nθ}` evaluations guarantee on `L_u`.  The theory report's
`x_na(θ) = e_hint(θ) + θ` (§11.21) says

    ε_na(N)  =  ε_ad(N) + ln N + o(n)        for 0 < θ ≤ h,

and `ε_ad(N) = o(n)`, `ε_na(N) = n·x_na(θ) ≤ ln N` for `h ≤ θ ≤ a`.  In multiplicative terms: **for
budgets up to `e^{nh}` the error factor of the best non-adaptive method is `N^{1+o(1)}` times that
of the best adaptive one.**

*Why this is the right way to say it to the information-based-complexity community* **[H]**.
(1) In the weights `w = e^{−βg}` the solution operator `Z(w) = Σ_x w(x)` is *linear* and the class
`{w > 0 : w(x) ≤ e^{u d(x,y)} w(y)}` is a *convex cone*.  The theory report (and referee R5) explain
the inapplicability of "adaption does not help" by "`ln Z` is not linear"; the accurate reason is
that the class is convex but **not symmetric**, the error criterion is **relative**, and the
information is **standard** (function values).  (2) For linear problems on convex non-symmetric
classes adaption is known to help by polynomial factors in the cardinality: the gap is at most
`4(n+1)²` deterministically (Novak 1995, quoted in Krieg–Novak–Ullrich **[K, full text of the
quoting paper; Novak 1995 not accessed]**), at most a rate `3/2` (rate `1` for a Hilbert target)
for adaption and randomisation together with linear information (Krieg–Novak–Ullrich 2025, Thm 1
and Table 1 **[K, full text]**), and "for standard information … there are more extreme examples,
where adaption yields a gain up to the order `n`" (ibid. §6.1(5), citing Novak, JAT 80 (1995)
**[not accessed]**).  The cube class is one more example of this kind, with the gain *exactly* one
power of the cardinality, in the randomised setting, for relative error.  (3) The gain looks
"exponential" in the theory report only because the error scale is `e^{n·rate}`.  This is an
analogy, not a corollary: the cited bounds concern absolute error, and in absolute error the gain
disappears altogether **[P]**: the convex section `{w in the cone, max w ≤ 1}` contains every
function with values in `[e^{−u}, 1]` (distinct points are at distance `≥ 1`), on which estimating
the mean has randomised error `Θ(N^{−1/2})` for adaptive and non-adaptive methods alike (Bakhvalov;
Mathé–Novak's class `F₁`), and plain Monte Carlo has error `≤ N^{−1/2}` on the whole section.  The
adaption gain lives entirely in the small-`Z` instances that only a relative criterion sees.  (4) A contrast worth citing: on the moment-ratio cones of
Kunsch–Novak–Rudolf (2019) **[abstract]** i.i.d. nodes with an adaptive *stopping rule* are optimal
among all randomised algorithms; on the log-Lipschitz cone adaptive *nodes* gain a factor `N`
(pre-drawn points with adaptive stopping do not: Theorem 11.45(e)).

### 2.5 A new statement: the bounded-accuracy non-adaptive upper bound on the whole class, by the chain rule

The theory report proves the class-wide upper bound for plain Monte Carlo (Theorem 11.44) through
the tail lemmas and Harper's theorem, and lists the corresponding statement with a field at bounded
accuracy as missing (§11.20, remark (4): "Bounded accuracies with a field: only the lower bound `a`
for non-adaptive algorithms").  At bounded accuracy neither isoperimetry nor types are needed.

**Proposition A1.1 [P; every step checked by exact enumeration on cubes `n = 8…14`, §3
`chain_rule_check.py`].**  Let `π = Bern(p)ⁿ` (`0 < p < 1`, `q = 1 − p`), `u > 0`, `L_u` the
`u`-Lipschitz functions on `{0,1}ⁿ`, `ν_ψ ∝ π e^{−ψ}`, `A(ψ) = E_π e^{−ψ}`.  Put
`a₀ = pe^{−u}/(q + pe^{−u})`, `a₁ = pe^{u}/(q + pe^{u})` (the letter marginals of the cones around `0ⁿ`
and `1ⁿ`; `logit a₁ − logit a₀ = 2u`), `R(r) = max{KL(a₀‖r), KL(a₁‖r)}`, and let `r*` minimise `R`;
`a := R(r*)` is the capacity of the binary channel with rows `Bern(a₀)`, `Bern(a₁)`, and equals the
`a = max_m I_{π_s}(S;X)` of Theorem 11.59(c).  Then for every `n` and **every** `ψ ∈ L_u`:

1. for every order of the coordinates and every prefix, `ν_ψ(y_i = 1 | y_{<i}) ∈ [a₀, a₁]`;
2. `KL(ν_ψ ‖ Bern(r)ⁿ) ≤ n·R(r)` for every `r`, with equality for `ψ = u·d_H(·, 0ⁿ)` or `u·d_H(·, 1ⁿ)`; in
   particular `sup_{ψ∈L_u} KL(ν_ψ ‖ Bern(r*)ⁿ) = n·a`;
3. for `r ∈ [a₀, a₁]`:  `ν_ψ( ln(dν_ψ/dBern(r)ⁿ) > nR(r) + s ) ≤ exp(−s²/(2nu²))`;
4. if `Â = M⁻¹Σ_j (π/Q)(X_j)e^{−ψ(X_j)}` with `X_j` i.i.d. from `Q = Bern(r*)ⁿ` and `M ≥ e^{na+t}`, then
   `E|Â/A(ψ) − 1| ≤ e^{−t/4} + 2exp(−t²/(8nu²))`.

Hence `ln Â` is `(ε/2, δ)`-correct on all of `L_u` with `exp(na + O(u√(n ln(1/(δε)))))` **non-adaptive
evaluations drawn from a product measure**, for every fixed `ε`, every field and every `n`.

*Proof.*  (1) `ν_ψ(y_{<i}, 1)/ν_ψ(y_{<i}, 0) = (p/q)·Σ_{y_{>i}} π(y_{>i})e^{−ψ(y_{<i},1,y_{>i})} / Σ_{y_{>i}} π(y_{>i})e^{−ψ(y_{<i},0,y_{>i})}`,
and the two sums differ term by term by a factor in `[e^{−u}, e^{u}]`: the conditional odds lie in
`(p/q)[e^{−u}, e^{u}]`.  (2) Chain rule: `KL(ν_ψ‖Bern(r)ⁿ) = Σ_i E KL(Bern(κ_i)‖Bern(r))` with
`κ_i = ν_ψ(y_i = 1|y_{<i}) ∈ [a₀, a₁]`, and `KL(·‖r)` is convex.  (3) `ln(dν_ψ/dQ) = Σ_i ℓ_i`, where, given
the past, `ℓ_i` takes two values that differ by `|logit κ_i − logit r| ≤ 2u`, with conditional mean
`KL(κ_i‖r) ≤ R(r)`; Azuma–Hoeffding.  (4) With `ρ = dν_ψ/dQ` and `ρ_τ = ρ·1[ρ ≤ τ]`:
`Â/A = M⁻¹Σρ(X_j)`, `E_Q|ρ − ρ_τ| = ν_ψ(ρ > τ) = 1 − E_Qρ_τ`, `Var(M⁻¹Σρ_τ(X_j)) ≤ τ/M`; so
`E|Â/A − 1| ≤ √(τ/M) + 2ν_ψ(ρ > τ)` (this is the truncation step in the proof of Chatterjee–Diaconis'
Theorem 1.1, for `f ≡ 1`); take `τ = e^{na + t/2}` and use (3).  ∎

*What it gives.*
(a) *Uniform cube* (`p = ½`: `r* = ½`, `a = KL(p_u‖½)`): Theorem 11.44(ii) — plain Monte Carlo is
correct on the whole class at every fixed accuracy with `e^{na + O(√n)}` samples — **without
Harper's theorem**.
(b) *With a field:* together with the lower bound `a` of Theorem 11.61(b), (c), **the exponent of
non-adaptive algorithms at every bounded accuracy is exactly `a(p, u)`, and it is attained by the
single product measure `Bern(r*)ⁿ`** — the flat histogram is not needed there (it attains `a` too,
§3 C4).  This fills the gap of §11.20, remark (4), and it qualifies the headline "the right sample
is … uniform on every type class": true at extensive accuracies (numerically, by 0.5–3 %),
unnecessary at bounded ones.
(c) *"A field always helps" is the odds-ratio lemma.*  The cone channel has log odds ratio `2u` for
every `p`, so `a(p, u) ≤ a(½, u) = ln 2 − h(p_u)`, with equality iff `p = ½`, is literally Lemma 11.89
in its capacity form (Hasenclever–Scholz), and the monotonicity of `a` in the field is step (5) of
the report's proof of that lemma.  For the exponent `a` this replaces the separate proof of
Proposition 11.65(b).
*How sharp it is at finite `n`.*  Not very: the `O(√n)` term comes from Azuma's inequality with the
worst-case range `2u`.  At `n = 4000`, `u = 1`, `ε = 1`, `δ = 0.1` the proposition gives `e^{0.20n}`
samples, against `e^{0.134n}` for the report's Harper-based Theorem 11.44 and the lower bound
`e^{0.109n}` (benchmark B12, as quoted in §11.16); the exponent `a = 0.111` is reached only
asymptotically, as in the report.  (A Freedman-type inequality with the conditional variance
`κ(1−κ)(logit κ)²`, whose maximum over `κ ∈ [p_u, ½]` is attained at `κ = p_u` — the cone — for
`u ≤ 2.40`, would bring the constant of the `√n` term down to the cone's there.)
*What it does not give.*  The extensive-accuracy bound `θ_na(ε₁)` (Theorem 11.44(i)): there the
*lower* tail of the log-density under `ν_ψ` is needed uniformly over the class, the adapted
conditional means act as an adversary who can freeze the walk (`κ ≡ ½` is the flat instance), and I
did not find a chain-rule argument that replaces the tail lemma.  Nothing is claimed for reference
measures that are not products (the conditional odds of an interacting `π` do not factor).
*Novelty.*  New relative to the theory report (which has neither the capacity reading of `a` nor a
class-wide KL bound); mathematically it is two textbook steps; one extended search (§4.9, no. 24)
found nothing, which is not evidence of novelty for a statement this elementary.

### 2.6 Statements in the theory report that this workstream corrects or sharpens

1. Row G27 / §11.25 prior art: "the comparison at a fixed odds ratio was not found in two searches and
   may be folklore" → it is Proposition 8(a) of Hasenclever–Scholz (2013/2016).  **[K, full text]**
2. Row G18: "the exponent on the cube for `ln Z` … not found" → the exponent *function* is in print
   at the cone (§2.2); "not found" applies to the minimax statement.
3. Row G11: "the exact threshold … not found" → the constant is `B_max` of Suárez–Silbey–Oppenheim
   (the Jensen gap at the binomial instance); "not found" applies to its role as a complexity
   threshold with an exponential lower bound below it.
4. §11.16/§11.18 and L7 ("`ln Z` is not linear, so neither 'adaption does not help' nor these gaps
   apply") → linear functional, convex cone, relative error (§2.4).
5. Theorem 11.61, "that `min_r max(φ₀, φ₁) > θ_na` whenever `p ≠ ½` is not proved in general" →
   in the limit `ε₁ → 0⁺` the two sides coincide, by capacity = information radius (§2.3); a strict
   separation can only be an extensive-accuracy statement.  §11.20 remark (4), "bounded accuracies
   with a field: only the lower bound" → the matching upper bound is Proposition A1.1 (§2.5).
   Theorem 11.44(ii) does not need Harper's theorem (same proposition, `p = ½`).
   README item (v) "the right sample is not the Gibbs measure … but uniform on every type class"
   should say: at bounded accuracy any proposal with the capacity-achieving marginal does equally
   well at the exponential scale.
6. L7 addendum, "two 2026 preprints" (search summaries only) → read; see §4.1(e).  They do not
   anticipate G20 or G26 (different oracle, polynomial scale), but they make "adaptive versus
   non-adaptive" and "rounds" for partition functions a current topic that must be cited.

---

## 3. Numerics

All scripts are mine and share nothing with the theory division's code.  They run in seconds on
one core, except the two round-hierarchy scripts (3 minutes and about 15 minutes).

| script (in `experiments/science/ws_A1/`) | what | result |
|---|---|---|
| `odds_ratio_check.py` → `.out` (19 s) | Lemma 11.89 and the flow proof: T1 400 000 random tables; T2 derivative formula against finite differences; T3 monotonicity along both flows; T4 capacity = chord gap ≤ BSC with the same odds ratio; T5 25 000 tables in 40-digit arithmetic; T6 three mutations; T7 three letters | no violation (`max(I − bound) = −3·10⁻¹³`); formula agrees to `5·10⁻¹¹`; closest grid point `−5.2·10⁻⁵`; mutations detected; lemma fails for 3 letters as expected |
| `odds_ratio_report_proof_check.py` → `.out` | the intermediate formulas of the *report's* proof of Lemma 11.89: gradient (2), `T < 0` (3), kernel (4) with closed form, maximiser and monotone capacity (5), (6) | all hold (finite differences `5·10⁻¹¹`; 20 000 samples) |
| `exponent_checks.py` → `.out` (4 s) | E1 the report's values of `h`, `a`; E2 S–S–O formulas = `θ_na`, `ln cosh`, `a`; Chatterjee–Diaconis `q = a`; E3 shear identity; E4 exact finite-`n` lower-bound constructions; E5 simulation of plain Monte Carlo at the cone; E6, E7 | E1: `h = 0.00767, 0.02914, 0.09728, 0.15614` (`u = ½, 1, 2, ln 16`), `a = 0.03030, 0.11094, 0.32781` — all digits of the report; E2: `4·10⁻¹⁵`; **E4: `0.02933` at `n = 6400`, `u = 1`, `ε₁ = ¼ ln cosh ½`, `δ = 0.05` — replicates the report's `0.0293`** (limit `0.0283`); hinted side `0.0169 → 0.0163`; E5 as in §2.2 |
| `capacity_check.py` → `.out` (3 s) | C1 capacity = information radius for the cone channel, six `(p, u)`; C2 uniform cube; C3 plain MC from `π`; C4 exact finite-`n` KL of a cone against the flat histogram; C5 mutation | equality to `10⁻⁸`; `a(0.1, 2) = 0.16374`, `r* = 0.1975`; flat histogram: `0.1752, 0.1675, 0.1649` at `n = 200, 800, 3200` `→ 0.1637`; **replicates the table of §11.20 exactly** (§2.3(c)) |
| `chain_rule_check.py` → `.out` (5 s) | Proposition A1.1 by exact enumeration, `n = 8…14`, seven `(n, p, u)`, 16 families of Lipschitz functions each (cones, flattened cones, dips, minima/maxima of cones, McShane regularisations of random functions at four roughness scales, wells, block-radial, additive): A2 conditional means in `[a₀, a₁]`; A3 `KL ≤ na`; A4 exact upper tail against `exp(−s²/(2nu²))`; A5 Monte Carlo for item 4; A6 `a(p,u) ≤ a(½,u)`; A7 three mutations | 112 instances: largest excursion of a conditional mean `4·10⁻¹⁵`; `max KL/(na) = 1.000000`, attained at a constant cone; tail bound never violated; item 4: measured `0.227` against the bound `0.471` in the tightest case; mutations detected (a `3u`-Lipschitz function leaves the interval; proposal `π` gives `1.28·na`) |
| `rounds_numbers_check.py` → `.out` (3 min), `rounds_refine.py` → `.out` (finer grid, ≈ 15 min) | the two headline numbers of the round hierarchy, re-computed from the formulas *as printed* in Theorems 11.84(b) and 11.86 (this replicates the evaluation of the formulas, not their proofs) | upper value `T^{(2)}(0)/a = 0.6196, 0.6243, 0.6412, 0.6646` at `u = 0.5, 1, 2, 3` (report: `0.620, 0.624, 0.641, 0.665`), `0.6181` at `u = 0.02` (golden ratio `0.618`); lower value `θ₂*/a = 0.3493, 0.3592, 0.3940, 0.4396` (report: `0.349, 0.359, 0.394, 0.440`), `θ₂*/h = 1.379, 1.368, 1.328, 1.277` (report: `1.38, 1.37, 1.33, 1.28`), best `φ₁ = 0.640, 0.606, 0.560` at `u = 1, 2, 3` (report: `0.64, 0.61, 0.56`); at `u = 2` the supremum sits on the constraint `θ < φ₂a`, which a grid of step `0.01` in `φ₁` misses by `0.002` |
| `addendum_checks.py` → `.out` (8 s) — for §9 | Q1 the dictionary of Theorem 11.99 on the cube from the textbook formulas (Rényi capacity of the BSC; Nakiboğlu's definition of `E_sp`; Merhav's glassy free energy; `E_sp − θ`); Q2 the `k`-ary symmetric channel behind Proposition 11.103(e): `F*_k = (1−t)C_t`, cutoff-rate optimum, reflection identity at `e^u = k(k−1)`, integer optima for `k ≤ 12`, capacity optimum, the report's `h_k` values; Q3 Proposition A1.2 by exact enumeration (two site types, 2–3 letters, asymmetric envelopes) | all pass: Q1 `10⁻¹²`; reflection identity `4·10⁻¹⁶` (and fails by `4·10⁻³` off the crossing); `h_2, h_3, h_4` reproduced to six digits; `a₂ = a₃` at `u = 0.51937`; 36 instances: conditional laws in the window to `5·10⁻¹⁵`, `max KL/(Σa) = 1.000000` with equality at additive vertex instances; a non-admissible `ψ` leaves the window |

Re-run: `cd experiments/science/ws_A1 && python3 <script>`; the seven checking scripts exit
non-zero on a failed check (`rounds_refine.py` has no pass/fail check: it only prints the refined
values, which are compared with the report's by eye in the row above).  *Errors of mine found on the way* (recorded in `NOTES.md`): two mutation/optimiser
tests that could not fail or had to find an optimum by random search; an `expm1` overflow; taking
the largest instead of the least radius `R` with `D_R > ε` in the non-adaptive lower bound; and a
test function in `chain_rule_check.py` that was `1.5u`- instead of `u`-Lipschitz (caught by the
script's own Lipschitz check, and it did violate item 1 — the check has power).
*Not done numerically:* nothing about the adaptive algorithm (Theorems 11.52, 11.56) — its cost
accounting was outside this brief; Theorem 11.63; the finite-`n` two-round twins.

---

## 4. Prior art, claim by claim

### 4.1 Claim 1 — "adaptivity replaces the hint" (G20, G21)

*Exact statement* (§11.18 Theorem 11.54; §11.19 Theorem 11.58; with Theorems 11.25(a),(d), 11.44,
11.45).  `X = {0,1}ⁿ`, known part zero, class `L_u`.  Algorithms: randomised (finite mixtures of
deterministic adaptive query algorithms), exact evaluations of `g`, `(ε/2, δ)`-correct for
`ln Σ_x e^{−βg(x)}` on **every** member, `δ < ½` fixed.  For `0 < ε₁ < ln cosh(u/2)` the least
worst-case number of evaluations is `exp(n·KL((Λ₁+ε₁)/u‖½) + o(n))` — the cost of an algorithm that
is told the instance (a "hint") at the hardest instance `g ≡ 0` — while non-adaptive algorithms need
`exp(n·θ_na(ε₁) + o(n))`, `θ_na > θ_hint`.  At every bounded accuracy, down to `e^{−o(n)}`: `h =
KL(Λ₁/u‖½)` against `a = KL(p_u‖½)`.

*Closest prior statements.*

(a) **Mathé & Novak 2007** `[full text: §§1–5; appendix not read]`.  Integration against an unknown
density, oracle for `f` and `ρ`, worst-case root-mean-square error.  Class `F_C` (`sup ρ/inf ρ ≤ C`):
complexity linear in `C` for *all* methods, simple Monte Carlo optimal (Theorems 1, 2).  Class `F^α`
(log-concave `ρ` on a convex body in `ℝ^d`, `|log ρ(x) − log ρ(y)| ≤ α‖x−y‖`): every non-adaptive
method has error `≥ c_Ω α^{d/2} n^{−1/2}/√(d!)` (Theorem 3, Bakhvalov averaging over
`ρ_i = c_i exp(−α‖y − y_i‖)` with hidden centres and integrands `±c̃_i 1_{B(y_i, r)}`), while a
Metropolis ball walk has asymptotic error `O(√((d+1)max(d+1, α²)/n))` (Theorem 5); Remark 5: an
adaptive method identifies the centre from one value.  *Comparison.*  Same mechanism for the
non-adaptive bound and the same qualitative conclusion ("adaption breaks the curse").  Different:
the functional (an expectation, not the normalising constant, which the paper calls "often as hard
as the original problem"), the hypothesis (log-concavity, used essentially by the adaptive method),
the conclusion (polynomial in `d, α` versus a constant exponential in `d`; no exponent, no matching
lower bound for adaptive methods, no comparison with a hinted problem).  The theory report's
attribution is accurate.

(b) **Verification versus identification in sequential testing** — Karnin, NeurIPS 2016 `[full
text: abstract, §1]`: "additional structure is known in advance, causing the task of verifying the
optimality of a candidate to be easier than discovering the best arm … in this high confidence
regime, identifying the best arm is as easy as the task of verification"; cost `H_explore +
H_verify`.  Garivier & Kaufmann, COLT 2016 `[abstract]`: an instance-dependent lower bound and a
strategy that "tracks the optimal proportions of arm draws highlighted by the lower bound".
Chernoff 1959 `[from memory — unverified; Project Euclid not accessible]`.  *Comparison.*  The same
motto — an adaptive procedure attains the cost of the oracle that knows the instance — in a
different regime: noisy observations, `δ → 0`, instance-wise.  The theory report's regime is exact
evaluations, fixed `δ`, dimension `→ ∞`, worst case over the class (and the instance-wise version is
stated there as open, remark (4) of §11.18).  The pattern "query complexity ≤ learning +
verification" of §11.10 is Karnin's explore–verify and should cite it.

(c) **Adaption in information-based complexity** — Krieg, Novak, Ullrich 2025 `[full text: §1,
§6.1, §6.3]`; Heinrich 2024 `[abstract]` (gap `n^{1/4}` for scalar mean computation); Kunsch, Novak,
Wnuk 2024 `[abstract]` (gap `n^{1/2}(log n)^{−1/2}`); Novak 2023 survey `[Remark 1; keyword search]`;
Novak, Proc. AMS 1992 `[search snippet]` (monotone functions: adaptive randomised `n^{−3/2}` against
non-adaptive `n^{−1}`).  See §2.4: in these units Theorems 11.45 + 11.54 are a gain of one power of
the cardinality on a convex non-symmetric class.  Nothing there treats normalising constants,
relative error, or a growing dimension with exponents.

(d) **Algorithmic relatives** — Giles & Haji-Ali 2019 `[abstract, p. 1]`, describing Broadie, Du,
Moallemi 2011: for `P[E[X|Y] ≥ 0]` the inner sample size is adapted to the distance of the inner
estimate from the threshold.  This is the idea of the two-level algorithm ("brackets of fibre
averages refined only as far as a one-sided test requires"), with mean-square criteria and no
worst-case class.  Nested sampling and multilevel splitting `[from memory — unverified]` use the
same layer-cake identity with a *constrained sampler*, which the value-query model does not provide.

(e) **Sampling-oracle counting** — Guo, Liu, Yang, Yin, Zhang, arXiv:2609.20337 (Sep 2026) `[full
text: abstract, §1, Thms 1.2–1.4, Table 1]`: the oracle returns `H(X)`, `X ∼ μ_β`; non-adaptive
`O(q ε⁻² log h)`; all algorithms `Ω(min{q log h, q²}ε⁻²)`; non-adaptive `Ω(min{q log h, e^q}ε⁻²)`.
Harris, Kolmogorov, Liu, Yin, Zhang, arXiv:2604.01263 (2026) `[abstract, pp. 1–2]`: non-adaptive
`O(qε⁻² log² h)`, and `O(qε⁻² log h)` "with just two additional adaptive rounds".  *Comparison.*
Adaptivity and rounds for partition functions, but with Gibbs samples as the oracle, at polynomial
scale, and with the conclusion that one round is (nearly) enough; a gap that is exponential in `q`
between adaptive (`O(q²ε⁻²)`, as the paper recalls for the TPA method) and non-adaptive algorithms
appears there only in the corner where `log h` is exponentially large in `q`.

(f) **Normalising constants by value/gradient queries** — Holzmüller & Bach 2025 `[full text: §§1–2.2,
Table 1, proofs of Thm 8 and Prop. 9]` (fixed `d`, `C^m` balls, rates in `n` and `B`, constants in
`d` ignored; no adaptive/non-adaptive separation: "the same rates hold for adaptive points" for
deterministic points and the stochastic class is adaptive by definition); Ge, Lee, Lu 2020
`[abstract]` (strongly log-concave, polynomial bounds).  Neither contains exponents in the dimension.

*Searches without a relevant hit* (wording in §4.9): value-query complexity of the partition function
of a Lipschitz energy on the hypercube, adaptive versus non-adaptive; integration against an unknown
log-Lipschitz density without log-concavity.

*Classification:* **(6) plausibly original theorem.**  *Caveats a referee will raise:* the statement
is about exponents on one idealised class; the upper bound is a nested algorithm with an unquantified
`o(n)` whose cost is a paper proof with a history of repaired gaps (theory report, D45, R7); the
lower bound is the easy half (hidden Hamming-ball dips — the Lipschitz version of Mathé–Novak's
Theorem 1).

### 4.2 Claim 2 — Monte Carlo is exponent-optimal among non-adaptive algorithms (G18)

*Exact statement* (Theorems 11.44, 11.45): for every member of `L_u`, plain Monte Carlo with
`e^{nθ_na(ε₁)+o(n)}` uniform samples is `(ε₁n/2, δ)`-correct; every randomised non-adaptive algorithm
needs `(1−2δ)2ⁿ/|B(R−1)|` evaluations whenever `ε < D_R` (cone against flattened cone, hidden centre).

*Closest prior statements.*  Suárez–Silbey–Oppenheim 2012 and Chatterjee–Diaconis 2018 for the
exponent function at the cone (§2.2); Mathé–Novak 2007, Theorem 3 for the lower-bound method
(§4.1(a)); Dzindzalieta 2013 `[full text: abstract, pp. 1–2]` — the supremum over 1-Lipschitz `f` of
`μ{f − Ef ≥ x}` "is achieved on a family of distance functions", equivalent to the vertex-
isoperimetric problem, with the Hamming cube among the corollaries — for the mechanism of the tail
lemmas 11.43 (distance functions to Harper sets are extremal); Harper 1966 `[not accessed]`;
§2.3 for the capacity reading of `a`.  Bar-Yossef, Kumar, Sivakumar 2001 `[search snippet]` and
Mathé–Novak's Theorems 1–2 are the classical "adaptivity does not help" statements for *unstructured*
classes, which the Lipschitz structure breaks.

*Comparison.*  Known: the formula, for one estimator at one instance, in expectation and in the
limit; the lower-bound technique.  New: (i) the cone is the worst instance of the whole class for
plain Monte Carlo at the exponential scale (Harper + truncation + Chernoff); (ii) the pair
cone / flattened cone gives the same exponent for every non-adaptive algorithm.  The theory report
calls (i) "a routine combination" and (ii) "a known method"; I agree.
*Classification:* **(3) known special case exists.**

### 4.3 Claim 3 — a field as known part (G22)

*Exact statement* (Theorems 11.59, 11.61, 11.63, 11.64): on the `p`-biased cube,
`θ_na = max_m min{I(S;X) : D(P_{X|S}‖π_s|P_S) ≤ ε₁}`, attained by sampling uniformly on every type
class; the adaptive exponent is `R^max = max_γ R_γ`, the hinted exponent of the hardest additive
instance; Theorem 11.63: every set that is `e`-sensitive for the flat-histogram instance has
`μ_H`-measure at least `exp(−n[R^max(e) + o(1)])`.

*Closest prior statements.*  (i) Capacity = information radius; redundancy–capacity; Shtarkov's NML
distribution (the report cites the last itself) — the sampler statement is this classical
phenomenon (§2.3).  (ii) Cérou, Héas, Rousset 2022 `[full text: abstract, §1]`: worst-case optimal
importance proposals over a convex class of targets with the Chatterjee–Diaconis cost `Ent(η|μ)`,
relative to a reference; the optimum is the entropy minimiser of the class.  A minimax theory of
proposals, with a different criterion; no `(ε,δ)` estimation, no lower bound for all non-adaptive
algorithms.  (iii) Beh & Morio, arXiv:2611.20831 (16 Nov 2026) `[full text: abstract, §1, Table 1]`:
for the probabilities of several events under the minimax relative variance the optimal proposal is
"essentially the equal mixture of the `f|A_k`", and histogram cells get equal mass in the minimax
limit — the variance-based, finite-family form of "a flat histogram is minimax for relative error".
(iv) Flat-histogram methods (Berg–Neuhaus; Wang–Landau) `[from memory — unverified]`.  (v) For
Theorem 11.63: Lei Yu, arXiv:2205.07596 `[abstract, introduction; theorem statements located but the
two-column text was not studied]` — exact isoperimetric exponents for *product* measures,
generalising Ahlswede–Zhang `[not accessed]`; nothing on exchangeable mixtures.

*Comparison.*  The headline "flat histogram, not the Gibbs measure" is known in substance and, at
bounded accuracy, is not even needed (a product measure with marginal `r*` ties, §2.3).  The
adaptive exponent `R^max` and Theorem 11.63 are extensions of G20 and of the Ahlswede–Zhang/Yu
theorem; I found neither and could not check Theorem 11.63 against Yu's Theorem 5 in the time
available (the theory division's referee R9 did, and judged it not a black-box corollary).
*Classification:* **(4) plausibly original generalisation.**

### 4.4 Claim 4 — shear law and game-function pair theorem (G23)

*Exact statement* (§11.21, Theorem 11.66 [V]): `x_na(θ) = e_hint(θ) + θ`; for a game function `F`,
`R(e) = max_{0≤t≤1}[F(t) − te]` and `θ_na = R∘(id + R)⁻¹` form a pair for which the level recursion
converges to `R`.

*Prior art.*  The shear law on the cube is the identity `KL(ρ‖p_u) = KL(ρ‖½) + uρ − Λ₁`; at the cone
it is the published form of the REM bias, `ln M` + frozen energy (§2.2); as a statement about
algorithms it is Theorems 11.45 + 11.54 restated (§2.4).  The transform `max_{0≤t≤1}[F(t) − te]`, with
the constraint `t ≤ 1` producing a slope-`(−1)` regime, is the structure of Gallager's random-coding
exponent `max_{0≤ρ≤1}[E₀(ρ) − ρR]` (against the sphere-packing exponent with `ρ ≥ 0`; straight-line
portion of slope `−1` below the critical rate) `[search snippet from secondary sources; Gallager
1968 not accessed]`; `θ_na(x) = max_{τ<1}(F(τ) − τx)/(1−τ)`
is the same game after eliminating the shear.  The convergence of the level recursion is specific
to the nested algorithm and has no counterpart that I know.
*Classification:* **(2) reformulation of a known result** — useful packaging (one machine-checked
statement behind two theorems), not a contribution on its own.

### 4.5 Claim 5 — exchangeable known parts (G25)

*Exact statement* (Theorem 11.76 and the remark on an arbitrary finite group): if `ε < ε_n^{tr}(q)`
every non-adaptive algorithm needs `(1−2δ)/q` evaluations; `⌈8 ln(2(n+1)/δ)/q⌉` uniform points per
type class are `(ε/2, δ)`-correct for `ε ≥ ε_n^{tr}(q) + ln(4/δ)`; the flat-histogram instance is the
hardest symmetric instance up to `n+2`.  Proposition 11.82: with two phases the extremal
perturbations are shells in the barrier class.

*Prior art for the first half.*  The invariance principle of design theory: Idais & Schwabe 2020
`[full text: Theorem 2 and its paragraph]` — "If Φ is invariant (with respect to G) and convex, then
there exists an invariant design … which is Φ-optimal over all designs … Invariant designs are
uniform on orbits … it remains to find the optimal orbits and the corresponding optimal weights",
in the spirit of Kiefer 1959 `[not accessed]`; Bakhvalov's averaging over a
group is the same argument for lower bounds (it is how Mathé–Novak and the theory report's Theorem
11.45 proceed).  Once designs are uniform on orbits, giving every one of the `N_orb` orbits the same
number of points loses at most the factor `N_orb` — that is the theorem.  The one ingredient that
is not generic is that the weight truncated at type-wise quantiles stays in the class
(`truncate_lipschitz_insert`, the local LYM inequality).
*Classification 5a:* **(2) reformulation of a known result.**
*Second half (shells at phase coexistence).*  Numerical, by the theory division's own labels;
I found no literature and did not examine it.  *Classification 5b:* **(9) unresolved.**

### 4.6 Claim 6 — rounds of adaptivity (G26)

*Exact statement* (Theorems 11.84, 11.86, Corollary 11.87): `a = τ^{(1)} > T^{(2)}(0) ≥ τ^{(2)} ≥
θ₂*(u) > h = lim_r τ^{(r)}`; at `u = 1`, `τ^{(2)} ∈ [0.359a, 0.624a]`.

*Closest prior statements.*  Canonne & Gur 2017 `[full text: abstract, introduction]`: for every
`k ≤ n^{0.99}` a property with a `k`-round-adaptive tester of `Õ(k)` queries that needs `Ω(n)` queries
with `k − 1` rounds — constructed properties, decision problems.  Agarwal, Agarwal, Assadi, Khanna
2017 `[search snippet]`: `log* n` rounds necessary and sufficient for optimal coin identification.
Guo et al. and Harris et al. 2026 (§4.1(e)): rounds for partition functions in the sampling-oracle
model, where one round suffices.  A quantum partition-function result with an `n^{1/4}` gain of
adaptive over non-adaptive strategies (arXiv:2610.06197) `[search snippet]`.
*Comparison.*  Round hierarchies are a standard genre; none of the sources treats estimation of a
sum over a Lipschitz class by value queries, and none has "dilution of a blind batch by a flat
histogram" as the separating instance.  The lower-bound lemma (virtual run, Lemma 11.85) is the
standard coupling of round-elimination arguments.  *Independent replication of the numbers* (§3):
`T^{(2)}(0)/a` and `θ₂*/a` re-computed from the printed formulas agree with the report at four slopes
to the digits given; I did not examine the proofs.
*Classification:* **(6) plausibly original theorem**, conditional on claim 1 (its upper half is a
re-scheduling of the nested algorithm) and unrefereed; one step of a hierarchy is proved.

### 4.7 Claim 7 — the odds-ratio lemma (G27)

§2.1.  *Classification:* **(1) established prior art.**

### 4.8 Claim 8 — the threshold `n ln cosh(βc/2)` and the soft gap (G11)

*Exact statement* (Theorem 11.25): above `ε₁ = ln cosh(u/2)` a number of uniform samples independent
of `n` suffices on every instance (`0 ≤ ln E e^{−β(g−Eg)} ≤ n ln cosh(u/2)`); below it every algorithm
needs `(1−2δ)2ⁿ/|B(k)|` evaluations at `g ≡ 0` whenever `ε < Δ_k`, with exponent
`ln 2 − h((Λ₁+ε₁)/u)`; matching hinted upper bound by Harper; accuracy diagram down to `e^{−λn}`.

*Closest prior statements.*  Suárez–Silbey–Oppenheim eqs. (31), (44) (§2.2): `nΛ₁` is the free-energy
difference and `n ln cosh(u/2)` the bias of a single measurement in the binomial model.  The upper
bound `ln E e^{−β(g − Eg)} ≤ n ln cosh(u/2)` for Hamming-Lipschitz `g` on the uniform cube is the
two-point martingale argument (each martingale difference is a symmetric two-point variable); I
regard it as folklore `[from memory — unverified]` and did not look for a first source.
Holzmüller–Bach §2.2 `[full text]`: two regimes for stochastic log-partition estimation on `C^m`
balls in fixed dimension; "we leave a lower bound outside of the optimization regime as an open
problem".  Mathé–Novak Theorem 1 `[full text]`: hidden "needles" give a lower bound linear in `C`
for all algorithms on `F_C`; on the cube class `C = e^{un}`, and the Lipschitz condition forces
needles to be Hamming balls — which is what lowers `e^{un}` to `e^{nθ_hint}`.
*Is the cube case a corollary of Holzmüller–Bach?*  No: their constants depend on `(m, d)` in an
unspecified, exponential way, and their classes are balls of `C^m([0,1]^d)`.  *Is `ln cosh` there?*
No (keyword search of the full text; §2.2 read).
*Classification:* **(5) new combination** — a known constant, a folklore upper bound, a needle-type
lower bound adapted to a Lipschitz class, and Harper's theorem for tightness.

### 4.9 Search log

`WebSearch` queries, in order (S = standard, X = extended); the hits that were opened are in §4.10.

1. S `mutual information 2x2 contingency table fixed odds ratio maximized uniform marginals` → arXiv 2203.08089, 1302.6161, 2404.04343, 2601.07369.
2. X `"odds ratio" "mutual information" binary variables maximum "uniform marginals" OR "symmetric" inequality capacity "binary asymmetric channel" "same odds ratio"` → 2610.12805, 2203.08089; nothing on capacity.
3. S `Geenens "copula" discrete "odds ratio" 2x2 "margin-free" … "mutual information"` → framework only.
4. S `Hasenclever Scholz "Comparing measures of association in 2x2 probability tables" journal 2016` → DOI 10.2174/1876527001607010020.
5. S `partition function estimation Gibbs distribution sampling oracle lower bound adaptive versus non-adaptive cooling schedule 2026 arXiv` → 2609.20337, 2604.01263, 2404.02414.
6. S `Jarzynski estimator finite sample bias "random energy model" …` → 1108.5783, 1108.0605.
7. S `Ben Arous Bogachev Molchanov "limit theorems for sums of random exponentials" …` → PTRF 132 (2005) (snippet).
8. S `Canonne Gur "An Adaptivity Hierarchy Theorem for Property Testing" …` → 1702.05678.
9. S `Bar-Yossef Kumar Sivakumar "Sampling algorithms: lower bounds and applications" …` → secondary snippets only.
10. X `minimax optimal importance sampling proposal over a class of target densities worst-case "multicanonical" OR "flat histogram" optimality theorem stratified sampling orbits symmetry invariance` → 2212.04292, 2611.20831, 2402.05653, 2502.07396.
11. S `Kiefer invariant designs theorem optimal design invariant under group … Hunt-Stein …` → 2011.09745, Pukelsheim.
12. S `Karnin "Verification Based Solution for Structured MAB Problems" …` → NeurIPS 2016 PDF.
13. S `Chernoff 1959 "Sequential design of experiments" …` → secondary descriptions.
14. S `Novak "Quadrature formulas for monotone functions" adaptive Monte Carlo n^{-3/2} nonadaptive n^{-1} …` → secondary snippets.
15. X `integration with respect to unknown non-normalized density lower bound adaptive nonadaptive "curse of dimensionality" … log-Lipschitz density without log-concavity` → **nothing relevant**.
16. X `adaptive versus non-adaptive query complexity estimating partition function "zeroth-order" OR "value queries" OR "function evaluations" Lipschitz energy hypercube exponential lower bound "normalizing constant" adaptivity gap` → **nothing relevant** (2404.02414, 2610.06197 as side hits).
17. S `"rounds of adaptivity" mean estimation OR "sum estimation" OR "approximate counting" lower bound hierarchy …` → Agarwal et al. COLT 2017 (snippet); no hierarchy for sums.
18. S `Dagum Karp Luby Ross "An optimal algorithm for Monte Carlo estimation" …` → bibliographic snippets.
19. S `Dzindzalieta "Extremal Lipschitz functions in the deviation inequalities from the mean" …` → 1205.6300.
20. S `"binary asymmetric channel" capacity bound "binary symmetric channel" with same "likelihood ratio" OR "odds ratio" …` → nothing on the comparison.
21. S `Plackett distribution "mutual information" "cross-product ratio" OR "odds ratio" marginals uniform maximum copula …` → 1302.6161 and 2203.08089 again.
22. S `Novak "Optimal recovery and n-widths for convex classes of functions" Journal of Approximation Theory 80 1995 adaption gain order n function values example abstract` → index entries only; full text not found.
23. S `channel capacity equals information radius "min_Q max_x D(W(·|x)||Q)" … "redundancy-capacity theorem"` → arXiv:1206.2459 (opened), lecture notes.
24. X `importance sampling hypercube "log-Lipschitz" OR "bounded log-ratio" OR "bounded influence" density conditional probabilities bounded chain rule "Kullback" product measure worst case over class sample size exp(KL) Hamming` → **nothing relevant** to Proposition A1.1 (Chatterjee–Diaconis follow-ups only).
25. S `Gallager random coding exponent "E_r(R) = max" "0 ≤ ρ ≤ 1" "E_0(ρ) − ρR" critical rate slope −1 sphere packing exponent ρ ≥ 0` → secondary sources confirming the form (snippets only).

### 4.10 Sources and what was read

| source | read | used for |
|---|---|---|
| Hasenclever & Scholz, Open Stat. Probab. J. 7 (2016) 20–35; arXiv:1302.6161v1 | `[full text]` arXiv: §§1–3.3, appendix proof of Prop. 8; published PDF: Prop. 8 | claim 7 |
| Williams, Neural Comput. 34 (2022) 2037–2046; arXiv:2203.08089v3 | `[full text]` pp. 1–7 | claim 7 |
| Lin, arXiv:2610.12805 (2026) | `[abstract]` + keyword search | claim 7 (no MI statement) |
| Mathé & Novak, J. Complexity 23 (2007); arXiv:math/0611285v2 | `[full text]` §§1–5 | claims 1, 2, 8 |
| Holzmüller & Bach, JMLR 26 (2025); arXiv:2303.03237v4 | `[full text]` §§1–2.2, Table 1, proofs of Thm 8, Prop. 9; rest keyword-searched | claims 1, 8 |
| Chatterjee & Diaconis, AAP 28 (2018); arXiv:1511.01437v3 | `[full text]` §1 to Thm 1.1; Thms 3.4, 3.5 | claim 2 |
| Suárez, Silbey, Oppenheim, PRE 85, 051108 (2012); arXiv:1108.5783v2 | `[full text]` abstract, §I, ideal-gas section (eqs. 26–46), App. C | claims 2, 4, 8 |
| Palassini & Ritort, PRL 107, 060601 (2011); arXiv:1108.0605 | `[abstract]` + first column | claim 2 |
| Krieg, Novak, Ullrich, Forum Math. Sigma 13 (2025) e152; arXiv:2406.07108v2 | `[full text]` §1, §2 (start), §6.1, §6.3 | claims 1, 4 |
| Novak, arXiv:2307.06787 | Remark 1 + keyword search | claim 1 |
| Heinrich, arXiv:2401.14100; Kunsch–Novak–Wnuk, arXiv:2308.01705; Kunsch–Wnuk, arXiv:2410.23067; Kunsch–Novak–Rudolf, arXiv:1805.08637 | `[abstract]` (from the PDF) | claim 1 |
| Novak & Rudolf, *Computation of expectations by MCMC methods*, arXiv:1311.1899v2 | `[full text]` §3 (unknown densities: Thms 3–5) and §4 (open problems) | claim 1: restates Mathé–Novak with an explicit non-asymptotic bound for the log-concave class; the open problems do not mention non-log-concave log-Lipschitz densities |
| Guo, Liu, Yang, Yin, Zhang, arXiv:2609.20337 | `[full text]` abstract, §1, Thms 1.2–1.4, Table 1 | claims 1, 6 |
| Harris, Kolmogorov, Liu, Yin, Zhang, arXiv:2604.01263v2 | `[abstract]` + pp. 1–2 | claims 1, 6 |
| Chen & Nannicini, arXiv:2404.02414 | §1.3 (existing lower bounds) | context |
| Canonne & Gur, arXiv:1702.05678 | `[full text]` abstract, p. 1 | claim 6 |
| Cérou, Héas, Rousset, arXiv:2212.04292 | `[full text]` abstract, §1 | claims 3, 5 |
| Beh & Morio, arXiv:2611.20831 | `[full text]` abstract, §1, Table 1 | claims 3, 5 |
| Idais & Schwabe, arXiv:2011.09745 | Theorem 2 and its paragraph | claim 5 |
| van Erven & Harremoës, arXiv:1206.2459 | the passage "Channel capacity and minimax redundancy" | §2.3 |
| Lei Yu, arXiv:2205.07596v3 | `[abstract]`, introduction | claim 3 |
| Garivier & Kaufmann, arXiv:1602.04589 | `[abstract]` | claim 1 |
| Karnin, NeurIPS 2016 | `[full text]` abstract, §1 | claim 1 |
| Ge, Lee, Lu, arXiv:1911.03043 | `[abstract]` | claim 1 |
| Giles & Haji-Ali, arXiv:1802.05016 | `[abstract]`, p. 1 | claim 1 |
| Dzindzalieta, ECP 18 (2013); arXiv:1205.6300 | `[full text]` abstract, pp. 1–2 | claim 2 |

**Not accessed** (cited from the papers that quote them, from search snippets, or from memory, and
marked so in the text): Novak, *Deterministic and stochastic error bounds* (1988); Novak, JAT 80
(1995) and JAT 82 (1995); Novak, *On the power of adaption*, J. Complexity 12 (1996) — ScienceDirect
returned 403; Novak, Proc. AMS 115 (1992); Chernoff 1959 — Project Euclid returned an empty page;
Harper 1966; Kiefer 1959; Gallager 1968; Bar-Yossef–Kumar–Sivakumar 2001; Canetti–Even–Goldreich
1995; Dagum–Karp–Luby–Ross 2000; Štefankovič–Vempala–Vigoda 2009; Kolmogorov 2018;
Harris–Kolmogorov; Huber; Broadie–Du–Moallemi 2011; Skilling 2006; Cérou–Guyader and Bréhier et al.
(adaptive multilevel splitting); Berg–Neuhaus 1992; Wang–Landau 2001; Ahlswede–Zhang 1999;
Bollobás–Leader 1991; Ben Arous–Bogachev–Molchanov 2005; Moukarzel–Parga 1991; Ogure–Kabashima 2009;
Agarwal–Agarwal–Assadi–Khanna 2017; the statistical-query literature (not searched).

---

## 5. What I did not settle

1. **Whether Theorem 11.54 is true.**  This workstream compared statements, not proofs: I did not
   re-derive the cost of the nested algorithm.  "Plausibly original" is a statement about the
   literature.
2. **Theorem 11.63 against Yu's theorem.**  I read Yu's abstract and introduction only; whether the
   type-uniform reference can be reduced to the product case by a cleaner argument than the
   workstream's is open to me.
3. **Novak's 1995 examples** (JAT 80): whether one of his standard-information examples with gain of
   order `n` on a convex non-symmetric class is structurally the cube example (a cone of functions
   with a one-sided local condition).  Not accessible here.
4. **Whether the hinted exponent `ln 2 − h((Λ₁+ε₁)/u)` has a REM-type counterpart.**  The non-adaptive
   exponent is the freezing curve of an exponential average; the hinted/adaptive exponent is a
   sphere-covering (rate–distortion) exponent at the radius where a dip in a *flat* landscape starts
   to matter.  I did not find the pair of radii (`p_u` and `Λ₁/u`) side by side in print.
5. **First source of the capacity phrasing of Lemma 11.89** and of the cosh bound on the Laplace
   functional of Hamming-Lipschitz functions; and whether Proposition A1.1 (§2.5) is in print
   (one search).
6. **G25 second half, Theorem 11.90, and the proofs of G26**: not examined (for G26 only the two
   headline numbers were re-computed from the printed formulas).
7. The statistical-query lower-bound literature and the Canetti–Even–Goldreich line were not opened;
   I expect them to be about unstructured classes, like Mathé–Novak's `F_C`, but that is from memory.

## 6. Three most promising next steps

1. **Write G18 + G20/G21 for the information-based-complexity audience as one theorem about
   adaption on a cone**: "for the integration functional on the cone of log-Lipschitz weights of the
   Hamming cube, with relative error, in the randomised setting, the adaption gain equals the
   cardinality `N` up to `e^{o(n)}`, for `N ≤ e^{nh}`", with Mathé–Novak, Krieg–Novak–Ullrich,
   Suárez–Silbey–Oppenheim and Chatterjee–Diaconis as the four anchors.  Ask whether the same holds
   on `[0,1]^d` for log-Lipschitz densities *without* log-concavity (Mathé–Novak's class minus
   concavity) — that is the question their community will ask.
2. **Extend Proposition A1.1 to extensive accuracies, or show that it cannot be done without
   isoperimetry.**  At bounded accuracy the chain rule replaces Harper's theorem and the method of
   types (§2.5).  At accuracy `ε₁n` one needs, uniformly over the class, a *lower* bound on the
   lower tail of the log-density — a control problem for a two-point walk whose conditional means
   the instance chooses in `[a₀, a₁]`.  If the constant control `κ ≡ a_b` is extremal for it (which
   is what Theorem 11.44 says on the uniform cube, via Harper), the whole non-adaptive theory on
   product references would become elementary, and the exact exponent of *product* samplers with a
   field — is it the `max(φ₀, φ₁)` of Theorem 11.61? — would follow.
3. **A finite-`n` version of one row.**  The radial class (Theorem 11.51) has explicit bounds for
   every `n` on both sides; a clean every-`n` adaptive/non-adaptive separation there, with constants,
   would make the note refereeable without the nested algorithm, and the full class could be stated
   as the theorem whose proof is long.

## 7. Requests

**To the theory division.**
- T1. Replace the proof and the prior-art paragraph of Lemma 11.89 by a citation of Hasenclever &
  Scholz (2016), Prop. 8(a), optionally with the five-line flow proof of §2.1; change "may be
  folklore" in row G27, §11.25 and README item (x).
- T2. In rows G11, G18 and §11.16: cite Suárez–Silbey–Oppenheim (2012) for `θ_na` at the cone (their
  eq. (43)), for `n ln cosh(u/2)` (eq. (44)) and for `nΛ₁` (eq. (31)); cite Chatterjee–Diaconis
  Theorem 3.4 (not only 1.1) for `a`; restrict "not found" to the minimax statements.
- T3. Replace "`ln Z` is not linear" (§11.18 remark (5), L7) by the cone/relative-error formulation
  of §2.4 and cite Krieg–Novak–Ullrich (2025) and Novak (1995) for the known size of adaption gains
  on convex non-symmetric classes; state the shear law as "gain = cardinality".
- T4. Check Proposition A1.1 (§2.5) and, if it stands, add it: it gives Theorem 11.44(ii) without
  Harper, the missing bounded-accuracy upper bound with a field (attained by the product measure
  `Bern(r*)ⁿ`), and `a(p,u) ≤ a(½,u)` as a corollary of Lemma 11.89.  Record that
  `min_r max(φ₀, φ₁)(0⁺) = a` (capacity = information radius), so the separation of product samplers
  from the flat histogram is an extensive-accuracy statement; qualify README item (v) accordingly.
- T5. Cite Karnin (2016) for "learning + verification" (§11.10) and for the motto of §11.18; cite
  Guo et al. (2026) and Harris et al. (2026) next to Mathé–Novak for adaptive/non-adaptive and
  rounds in the sampling-oracle model; cite Beh & Morio (2026) and Cérou–Héas–Rousset (2022) for
  minimax proposals; cite Idais–Schwabe/Kiefer for Theorem 11.76.
- T6. Precise question: is there an instance in `L_u` at which the best non-adaptive algorithm with
  `N ≤ e^{nh}` points is better than `N` times the adaptive error — i.e. is "gain = `N`" a statement
  about the worst case only?  (At radial instances Theorem 11.51 suggests the same gain.)

**To the engineering division.**
- E1. *Motivation:* §2.3 and Proposition A1.1 say that at bounded accuracy a single product proposal
  with marginal `r*` matches the flat histogram in the exponent; the proposition is checked here only
  by enumeration up to `n = 14`.  *Formulation:* for `(p, u) = (0.1, 2)` and
  `n ∈ {200, 400, 800, 1600}`, compute by exact binomial convolution (no sampling) the smallest `M`
  such that the importance-sampling estimate of `A` at the cone of centre type `m` is within a
  factor `e^{±1}` with probability `0.9`, for the three proposals `π`, `Bern(r*)ⁿ` (`r* = 0.1975`)
  and `μ_H`, maximised over `m ∈ {0, 0.1, …, 1}`.  *Expected:* `n⁻¹ ln M → 0.408, 0.164, 0.164`.
  *Validation:* the uniform cube (`p = ½`) must give `0.3278` for all three at `u = 2`.  *Stop:* when
  the last two columns differ by less than `2 ln n/n`.  *Resources:* shell-count distributions are
  Poisson with means from two binomials; minutes on one core.
- E2. None further; nothing in this workstream needs enumeration beyond what a laptop does.

---

## 8. What would survive a hostile referee, and what the paper would have to add

**The contribution.**  One result: *the exact exponents of adaptive and of non-adaptive randomised
algorithms for the normalising constant over the log-Lipschitz cone of the Hamming cube*
(Theorems 11.44/11.45 and 11.54/11.58 together).  Neither half alone is enough: the non-adaptive
half is a known formula with a known lower-bound method, and the adaptive lower bound is the easy
direction.  What a referee cannot wave away is the **matching adaptive upper bound without
log-concavity and without a sampler** — the nested algorithm — because it treats, on a model class,
a case that the Mathé–Novak line does not reach: what adaption can do when the density is only
log-Lipschitz (their adaptive method, and its explicit version in the Novak–Rudolf survey, need
log-concavity; neither paper poses the non-log-concave question).  A second result, if its proof
survives external refereeing: *two rounds are strictly between* (Theorem 11.86), because round
hierarchies for estimation problems with a natural class are rare and the separating instance is
not of the usual nested kind.

**What the paper would have to add.**
1. A complete, self-contained proof of the cost of the nested algorithm with the `o(n)` made
   explicit at least on a sub-class, and an every-`n` statement somewhere (radial class).
2. The positioning of §2.4 (cone, relative error, gain = cardinality) and the four anchors
   (Mathé–Novak; Krieg–Novak–Ullrich/Novak; Suárez–Silbey–Oppenheim; Chatterjee–Diaconis); the
   verification-versus-identification literature (Karnin; Garivier–Kaufmann) for the motto.
3. Honest scope: exact evaluations, fixed `δ`, one Lipschitz constant, exponents only, an algorithm
   nobody would run.  The referee will ask for at least one of: product reference measures (the
   field case is there), larger alphabets, or a continuous analogue; the theory report itself says
   the Gaussian analogue fails as it stands.
4. Removal of every novelty claim on Lemma 11.89, on the formula `θ_na`, on `ln cosh(u/2)` as a
   number, and on "flat histogram, not Gibbs" as a discovery (capacity-achieving output law;
   universal mixture).

**Communities.**  The adaptive/non-adaptive theorem belongs to *information-based complexity*
(adaption problem, integration with respect to unknown densities).  The formula-level content
(freezing curves, capacity, universal mixtures, the odds-ratio lemma) is *information theory /
statistical physics of sampling* and would be read there as a clean application, not as new
inequalities.  The round hierarchy and the hinted-versus-unhinted viewpoint are closest to
*sublinear algorithms / query complexity*; a referee from that side will compare with instance
optimality and with the sampling-oracle counting literature of 2018–2026.

---

## 9. Addendum: questions B1, B2 of THY-REQ-0011

*Written after the main report, on the coordinator's request, against theory checkpoint `89ac710`
(read-only checkout; §11.26 of its `docs/THEORY_REPORT.md`, lines 6138–6420, and
`docs/collaboration/requests/theory/THY-REQ-0011.md`, both read in full; `W_REPORT.md` not read).*
Labels and reading levels as in the header.  New script: `experiments/science/ws_A1/addendum_checks.py`
(8 s; all checks pass).

### 9.1 What is asked, and the short answers

**B1.**  *Is it known that the accuracy a fixed sample certifies for a normalising constant over a
Lipschitz class is a sphere-packing exponent, and that adaptivity gains exactly the sampling rate?*
— **At the level of formulas and of the mechanism: yes, three times over, under other names; at the
level of the complexity theorem: not found.**  (i) Every identity of the dictionary of Theorem 11.99
is a classical identity of information theory.  (ii) The mechanism — a sample of `e^{nθ}` points sees
a tilted product law only on the conditional types of mutual information at most `θ`, and the Gibbs
mass of what it sees has the exponent `min{D(V‖W|P) : I(P,V) ≤ θ}` — is in print as the *glassy phase of the random
code ensemble* (Mézard–Montanari; Merhav 2009), as the *bias of the Jarzynski estimator* (§2.2), and
as *Hoeffding's error-exponent trade-off* for testing a channel law against product laws
(Tomamichel–Hayashi 2018, who write it with Gallager's `E_0`).  (iii) "Adaptivity gains exactly the
rate" is, as a formula, the textbook fact that the two error exponents of a likelihood-ratio test
differ by the log-threshold (Forney's `E_2 = E_1 + T`).  (iv) What I did not find anywhere — in
information-based complexity, Monte Carlo theory for normalising constants, the importance-sampling
literature, learning theory, or statistical physics — is the *statement about algorithms*: that these
exponents are the minimax accuracy of **every** fixed sample over a Lipschitz class, and that an
adaptive algorithm **attains** the second exponent on the whole class.  On the coding side the
adaptive half has a counterpart as a *principle* but not as a *formula* (§9.2(d); corrected at
19:20 UTC — the first version of this addendum said "no counterpart at all", which was wrong): for
block codes of fixed length feedback does not beat the sphere-packing exponent; where it does
(variable length: Burnashev; fixed delay: Sahai), the principle is "identify tentatively, then pay
for the confirmation only" — Chernoff's sequential design — and the law is a different one.

**B2.**  *"A site with many equivalent states behaves like one with about `e^{u/2}` states".* — It has
an exact counterpart that I can prove but did not find in print: **the alphabet size that maximises
the cutoff rate `R_0 = C_{1/2}` of a `k`-ary symmetric channel at a fixed pairwise likelihood ratio
`L = e^u` is `k = √L + 1`**, the integer optimum being the `k` with `(k−1)(k−2) ≤ L ≤ k(k−1)`
(checked on a grid of slopes for `k ≤ 12`); and the
crossings of `h` sit at the same places because of a reflection identity,
`F*_k(t) = F*_{k+1}(1−t)` at `L = k(k−1)` (§9.4).  The *genre* — choose the number of signalling
levels for a given signal-to-noise ratio — is classical.

### 9.2 B1 in detail

*The statement compared* (Theorem 11.99, [P], unrefereed).  For a site `(π_j, d_j)` the "vertex
channel" sends a vertex `φ` of the site's Lipschitz polytope to its Gibbs law `π_φ`;
`F*_j(t) = min_Q max_φ (1−t)D_t(π_φ‖Q) = (1−t)C_t`; with `E_0(ρ) = ρΣ_jλ_jC_{1/(1+ρ)}` and
`E_sp(θ) = sup_{ρ≥0}[E_0(ρ) − ρθ]`: `θ_na = E_sp^{−1}`, `a` = capacity, and "with a budget of `e^{nθ}`
evaluations a fixed sample certifies the accuracy rate `E_sp(θ)`; an adaptive algorithm, or one with
a hint, certifies `E_sp(θ) − θ`".

**(a) The identities** **[K]**.

| line of the dictionary | where it is in print | read |
|---|---|---|
| Rényi capacity = Rényi radius, `min_Q max_φ D_α(π_φ‖Q)`, with a unique centre | "For finite Θ, Csiszár has shown that this result in fact extends to any α ∈ (0, ∞) … the minimax redundancy … may be geometrically interpreted as the 'radius' of the family"; Theorem 34 (van Erven–Harremoës 2014, arXiv:1206.2459); Nakiboğlu, *The Rényi capacity and center* (arXiv:1608.02424) | `[full text]` of the passage / `[abstract]` |
| `E_sp(R) = sup_{α∈(0,1)} ((1−α)/α)(C_α − R)` | Nakiboğlu, *The sphere packing bound via Augustin's method* (arXiv:1611.06924), Definition 13 — verbatim this formula | `[full text]` of §II-D |
| `E_0(ρ)/ρ` is a Rényi capacity of order `1/(1+ρ)` | Csiszár, IEEE-IT 41 (1995): `β`-cutoff rates, `α = (1−β)^{−1}` | `[search snippet]`; paper not accessed |
| `E_sp(R) = D(δ_GV(R)‖p)`, `D(δ_GV(R)‖½) = R` for the BSC | Forney, *On exponential error bounds for random codes on the BSC* (MIT 6.441 notes), eqs. (1.2), (1.4) | `[full text]` of §1 |
| `F*(t) = (1−t)C_t` as the exponent of an "exponential average" | `(1−t)D_t(P‖Q) = −ln Σ P^tQ^{1−t}` is the cumulant function of the log-likelihood ratio; fractional moments of importance weights are Rényi divergences (standard; e.g. the policy-optimisation literature) | `[search snippet]` |

On the uniform cube I checked the chain `F*_c(t) = (1−t)C_t(BSC(p_u))`,
`sup_α((1−α)/α)(C_α − θ) = KL(ρ_θ‖p_u)` (which is the Suárez–Silbey–Oppenheim bias curve of §2.2 and
Forney's `D(δ_GV‖p)`), and `E_sp(θ) − θ = uρ_θ − Λ₁`, to `10⁻¹²` (`addendum_checks.py`, Q1).

**(b) The mechanism: three literatures.**

1. *Random codes as a random energy model* `[full text: abstract, §1, §2.2.1–2.2.2]`.  Merhav
   (IEEE-IT 55 (2009); arXiv:0708.0850), following Mézard–Montanari (2009, ch. 6 `[not accessed]`),
   studies `Z(β|y) = Σ_{x∈C} P^β(y|x)` over a code of `e^{nR}` random words.  For the BSC: the number
   of words at distance `δn` from `y` is `≐ e^{n[R − ln 2 + h(δ)]}`, distances below the
   Gilbert–Varshamov distance `δ_GV(R)` "are not populated", and the sum freezes ("glassy phase") at
   `F_g = δ_GV ln(1/p) + (1−δ_GV)ln(1/(1−p))`; for a general channel (his eq. (10)) only conditional
   types with `H_Q(X|Y) ≥ ln|X| − R` — mutual information at most `R` — are populated.  With
   codewords = sample points, `y` = centre of a cone and `β = 1`, `Z/(M(1−p)ⁿ)` *is* the plain
   Monte Carlo estimate at the cone, and `F_g − (ln 2 − R) = E_sp(R)` (checked, Q1).  This is the
   paragraph "Why the sphere-packing exponent appears" of Theorem 11.99, in print since 2007–2009 in
   the coding reading.  Merhav relates the glassy free energy to the *correct-decoding* exponent and
   does not name `E_sp` there.
2. *The Jarzynski estimator* — §2.2 (Suárez–Silbey–Oppenheim 2012: the binomial case, i.e. the cube);
   in addition Rohwer, Angeletti, Touchette (PRE 92 (2015); arXiv:1409.8531) `[abstract, §II.B,
   §IV.B]`: the "linearization effect" of estimators of generating functions, "our results shed
   light on previous reports of 'phase transitions' in the statistics of free energy estimators",
   sample sizes exponential in `n`; and Yunger Halpern & Jarzynski (PRE 93 (2016); arXiv:1601.02637)
   `[abstract]`: "we bound the number of trials one should expect to perform, using the order-∞ Rényi
   entropy", with a tolerance parameter for the dominant region — a one-shot hypothesis-testing
   quantity between forward and reverse work distributions.  So Rényi quantities and the sample
   size of an exponential average have met in print; the asymptotic curve with all orders (Hoeffding)
   and the name "sphere packing" have not, as far as I found.
3. *Hypothesis testing* `[full text: abstract, §I, eqs. (2)–(6), (51)–(55)]`.  Tomamichel & Hayashi
   (IEEE-IT 2018; arXiv:1511.04874): if the type-II error must be at most `e^{−nR}`, the optimal
   type-I error exponent is `sup_{0<s<1} ((1−s)/s)(D_s(P‖Q) − R)` (Hoeffding's bound); for the
   composite alternative "`Xⁿ` independent of `Yⁿ`, any law of `Yⁿ`" the exponent is
   `sup_{s∈(0,1)} ((1−s)/s)(I_s^{↑↓}(X:Y) − R)` with Sibson's Rényi mutual information
   `I_s^{↑↓} = min_{Q_Y} D_s(P_{XY}‖P_X×Q_Y)`, which they write through "`E_0` … Gallager's error exponent
   function".  **This is the dictionary, read as follows** **[P — a translation, checked on the
   cube]**: budget `θ` = type-II exponent (the sampling-law measure of the set that has to be hit);
   non-adaptive accuracy = type-I exponent (the Gibbs mass outside that set); the minimum over the
   sampling law = the composite alternative; adaptive / hinted accuracy = minus the log-threshold of
   the likelihood-ratio test.  The shear law `x_na = e_hint + θ` is then the identity
   `D(V‖P) − D(V‖Q) = −λ` on the boundary of a likelihood-ratio test with threshold `e^{nλ}` — in
   coding, Forney's erasure/list exponents `E_2(R,T) = E_1(R,T) + T` (as restated by Merhav,
   arXiv:0711.2501 `[full text of the passage]`).  And the non-adaptive lower bound of the theory
   report (Theorems 11.45, 11.98(d)) is the Shannon–Gallager–Berlekamp sphere-packing argument
   `[from memory — unverified]` with the sampling law in the role of the auxiliary output law: there,
   "some decoding region has output-measure at most `e^{−nR}`"; here, "a sample of `e^{nθ}` points
   misses a set of sampling measure `e^{−nθ}`".

**(c) Covering.**  The estimate `Â/A` at a cone with centre `s` equals, by Bayes' rule, the ratio of
the output law *induced by the sample as a codebook* to the product output law, evaluated at `s`
**[P]** — the object of the soft-covering lemma (Wyner; Han–Verdú; exact exponents above the mutual
information: Yagli & Cuff, arXiv:1801.00714 `[abstract]`).  Its regime *below* the mutual
information — the one that matters here — was settled only recently and for a different criterion
(total variation tending to one): He, Pradhan, Winter, arXiv:2409.18307 `[abstract]`, with "a new
two-parameter information quantity, differing from the … Rényi mutual information" and the remark
that random coding is not tight.  So "a fixed sample has to cover the outputs of a channel" is a
living topic, but the pointwise, worst-centre criterion of the theory report is not the one studied.

**(d) Guessing and the adaptive half.**  The hinted problem is a *hitting* problem, and its home is
guessing: Arikan's exponent `max_Q[ρH_Q − D(Q‖P)] = ρH_{1/(1+ρ)}` and guessing subject to distortion
(Arikan–Merhav 1998, already cited by the theory report for G4/G7) `[the formula as quoted in
Merhav & Cohen, arXiv:1811.04363, which I read: abstract, introduction]`; randomised i.i.d. guessing
attains the guessing exponent (ibid.) — the analogue of "sample from the Rényi centre".

In channel coding proper the picture has three parts.  *(The first version of this addendum had
only the first and concluded "not in print in any form"; that was too strong and is corrected here.)*

1. *Fixed block length: feedback does not beat `E_sp`.*  "The reliability function of the discrete
   stationary product channels with feedback is bounded from above by the sphere packing exponent"
   (Nakiboğlu, arXiv:1611.06924, abstract).  "The sphere-packing bound `E_sp(R)` bounds the
   reliability function for fixed-length block-codes.  For symmetric channels, it remains a valid
   bound even when strictly causal noiseless feedback is allowed from the decoder to the encoder.
   To beat the bound, the problem must be changed" (Sahai, arXiv:cs/0610139, abstract).
2. *Variable length: feedback does beat it, by another law, and the principle is the theory
   division's motto.*  Burnashev (1976) `[not accessed; as stated in Berlin, Nakiboğlu, Rimoldi,
   Telatar, IEEE-IT 55 (2009) 3074–3080, arXiv:cs/0610145, of which I read the abstract and §I]`:
   the reliability function of variable-length block codes with feedback is
   `E_B(R) = C_1(1 − R/C)`, `C_1 = max_{x,x'} D(p(·|x)‖p(·|x'))` (their eq. (4)).  The Yamamoto–Itoh
   scheme alternates "a communication and a confirmation phase"; in the confirmation phase "the
   decoder performs a binary hypothesis test"; and the authors' converse "suggests that a
   communication and a confirmation phase are implicit in any scheme for which the probability of
   error decreases with the largest possible exponent".  In the sequential design of experiments
   the same principle is Chernoff's (1959) `[not accessed; as described in Naghshvar & Javidi, Ann.
   Statist. 41 (2013) 2703–2738, arXiv:1203.4626, of which I read the abstract and §2.2]`: "at each
   time t, find the most likely true hypothesis, and then select an action that can discriminate
   this hypothesis the best from each and every element in the set corresponding to the
   alternative hypothesis"; this is asymptotically optimal, and "the scheme of Chernoff, if
   specialized to channel coding with feedback, coincides with the second phase of Burnashev's
   scheme".  **That is "adaptivity replaces the hint" as a principle** — identify tentatively, then
   pay only for the verification of what was identified — in print since 1959 and, on the coding
   side, since 1976.  (It is the precedent named in §4.1 for claim 1; there I had Chernoff "not
   accessed" and Karnin's verification-based bandit algorithms as the source read.)  What differs
   is the law.  In coding the resource is time, additive in `n`: the two phases share the block and
   the exponent is linear in the rate.  Here the resource is a number of evaluations, exponential
   in `n`: the two phases add as `e^{nθ₁} + e^{nθ₂}` and share nothing.  On the cube
   (`addendum_checks.py`, Q4): the adaptive rate `E_sp(θ) − θ = uρ_θ − Λ₁` falls from `ln cosh(u/2)` at
   `θ = 0⁺` to zero at the fixed point `h < a` and is strictly convex; Burnashev's line for the same
   channel `BSC(p_u)` falls from `C_1 = u·tanh(u/2)` to zero at the capacity `a`.  (They are different
   quantities — an accuracy rate and an error exponent; the comparison only shows that one law is
   not the other.)
3. *Fixed delay: feedback also beats `E_sp`* (Sahai, ibid.: "this correspondence shows that the
   fixed-delay setting also presents such an opportunity for generic channels", with a "focusing
   bound") `[abstract]` — again another law.

Closest in *form* to the question — adaptive against non-adaptive **search**, treated as channel
coding — is Kaspi, Shayevitz, Javidi, *Searching with measurement dependent noise*
(arXiv:1408.4073, arXiv:1611.08959 `[abstracts]`): "measurement dependent noise incurs a
multiplicative gap in the targeting rate between adaptive and non-adaptive search strategies", and
the adaptive strategy "attains the optimal rate-reliability tradeoff".  That is a statement about
rates; the reliability law there is of Burnashev's kind as far as the abstract shows.

The roles are transposed throughout: in coding the adaptive party chooses channel *inputs*; here it
chooses *outputs* to look at.  So the half of B1 that is **not in print, as far as I found**, is the
*formula with an algorithm*: a procedure that realises the second exponent `E_sp(θ) − θ` of the
likelihood-ratio test on a whole class without knowing the hypothesis.  The *principle* behind it
is Chernoff's and Burnashev's, and a write-up should say so.

**(e) Where it was not found** (searches 26–35 of §9.5).  Importance sampling: the Stein-lemma end
only (Chatterjee–Diaconis: sample size `e^{KL}`; the same rule of thumb in an appendix of
arXiv:2312.15256 `[search snippet]`); necessary sample sizes through `f`-divergences (Sanz-Alonso,
arXiv:1608.08814 `[abstract]`); no Hoeffding curve, no Rényi radius, no sphere packing.  Information-based complexity: nothing
(Novak's survey and the adaption papers of §4.1 contain no information-theoretic exponents).
Learning theory: not searched beyond the importance-weighting hits; the minimax-rates-via-capacity
tradition (Yang–Barron) is about estimation rates, not about normalising constants `[from memory —
unverified]`.

*Classification.*  **Theorem 11.99 (the dictionary): (2) reformulation of known results** — a correct
and useful one; the first identity is one minimax step away from Csiszár's radius theorem.  It does
not change the classifications of §1: the theorems that the dictionary decorates (non-adaptive
exponent: (3)/(4); adaptive exponent: (6)) are what is or is not new.  Two consequences for the write-up:
the non-adaptive lower bound should be *presented* as the sphere-packing argument (with the
citation), and the formula `E_sp(θ) − θ` should be introduced as the second exponent of the
Neyman–Pearson test, so that the new statement stands out: an adaptive algorithm attains it.

### 9.3 How Theorem 11.99 relates to §2.3 and Proposition A1.1 of this report

*§2.3 is a special case.*  "`a` is the capacity of the cone channel, equal to its information radius,
with the capacity-achieving output law as centre" is the limit `t ↑ 1` of Theorem 11.99 for two
letters and one site type.  The two divisions arrived at it independently; theirs is the general
statement.  What §2.3 adds to §11.26 is the *consequence for samplers*: the Shannon centre is a
product law, so a product proposal ties with the stratified sample at vanishing accuracy.

*Proposition A1.1 is an addition, and it generalises to the whole setting of §11.26.*  §11.26 lists
"upper bounds at bounded accuracy" under "not done".

**Proposition A1.2 [P; items 1–3 checked by exact enumeration on 36 instances with two site types,
two and three letters and asymmetric envelopes, `addendum_checks.py` Q3; items 4–5 are the proof of
Proposition A1.1 verbatim and were not re-simulated].**  In the setting of §11.26 (sites of types
`τ(i)`, alphabets `𝒮_j`, site laws `π_j` of full support, envelopes `d_j ≥ 0` with the triangle
inequality, not necessarily symmetric; `π = ⊗π_{τ(i)}`; class `𝒞 = {ψ : ψ(x) − ψ(y) ≤ d(x,y)}`), let the
*window* of site type `j` be `𝒲_j := {p : π_j(a)p(b) ≤ e^{d_j(a,b)}π_j(b)p(a) for all a, b}`.  Then:

1. `𝒲_j = {π_γ : γ ∈ L_j}` is a convex polytope, and its vertices are the Gibbs laws of the vertices of
   the Lipschitz polytope `L_j` (the constraints `γ(a) − γ(b) ≤ d_j(a,b)` are *linear* in `p = π_γ`);
2. for every `ψ ∈ 𝒞`, every order of the sites and every prefix, the conditional law
   `ν_ψ(y_i = · | y_{<i})` lies in `𝒲_{τ(i)}` (sum the admissibility inequality over the remaining
   coordinates — the closure of `L_j` under soft minima, `softmin_admissible` in the theory's Lean file);
3. hence, for product laws `Q = ⊗Q_{τ(i)}`: `KL(ν_ψ‖Q) ≤ Σ_i max_{φ∈𝒱_{τ(i)}} KL(π_φ‖Q_{τ(i)})`, and with the
   Shannon centres `Q*_j` (capacity-achieving output laws of the vertex channels)
   `sup_{ψ∈𝒞} KL(ν_ψ ‖ ⊗Q*_{τ(i)}) = n·Σ_jλ_ja_j = n·a`, with equality at additive instances built from
   capacity-achieving vertices;
4. `ν_ψ(ln(dν_ψ/d⊗Q*) > na + s) ≤ exp(−2s²/Σ_ic²_{τ(i)})`, `c_j` the largest oscillation of
   `ln(p/Q*_j)` over `p ∈ 𝒲_j` (`2u` for two letters);
5. `M ≥ e^{na+t}` independent samples from the **product measure** `⊗Q*_{τ(i)}` give
   `E|Â/A(ψ) − 1| ≤ e^{−t/4} + 2exp(−t²/(2Σ_ic²_{τ(i)}))` for every `ψ ∈ 𝒞` and every `n`.

So, with the lower bound of Theorem 11.98(d) (stated there for every `n`; I take from the theory
report that it gives `a` at vanishing accuracy, as in the two-letter case): **on heteropolymer
product landscapes the exponent of non-adaptive algorithms at every bounded accuracy is the Shannon
capacity `a = Σ_jλ_ja_j`, and plain Monte Carlo from the product of the Shannon centres — the limit
`t ↑ 1` of the Gibbs laws of the hardest additive instances of Theorem 11.99 — attains it**, for
every `n`, without types and without isoperimetry.  It is not a corollary
of §11.26 (which has no upper bound at bounded accuracy and no statement about product samplers);
it uses of §11.26 only the definition of the vertex channel and the fact `a = Σλ_ja_j`.

*Note on independence (added 19:10 UTC).*  The coordinator's interim answer to the theory division,
`docs/collaboration/responses/science/SCI-RES-0001.md` §2, already states this generalisation as a
remark — "not written out and not checked numerically" — with the same ingredients (a soft minimum
of admissible functions is admissible; the normalised section of the weight cone is the convex hull
of the vertex laws; `KL(·‖Q)` is convex; the least largest divergence from a vertex law is the
information radius).  I read that file only after writing this section, so the two derivations
are independent.  Proposition A1.2 should be read as the written-out form of that remark, with
items 1–3 checked by enumeration and with items 4–5 (the tail and the sample size, with constants)
added; it has been checked by nobody but its author.

*Two by-products* **[P]**.  (i) *"Vertex labels suffice"* for the radius form at every order
`t ∈ (0,1]` in one line: `D_t(·‖Q)` is convex in its first argument for `t ≤ 1` (van Erven–Harremoës,
Theorem 11 `[full text]`), and by item 1 the window is the convex hull of the vertex laws.
(ii) *Product samplers at extensive accuracies.*  For a product sampler `Qⁿ` and a centre of type
`P` the same type counting gives the certified rate `min{D(V‖W|P) : D(V‖Q|P) ≤ θ}`; since
`D(V‖Q|P) = I(P,V) + D(PV‖Q)`, minimising over `Q` *after* the centre is chosen gives `E_sp(θ, P)`, and
therefore `min_Q max_P ≥ max_P min_Q = E_sp(θ)`: **at the level of these formulas a product sampler
is never better than the stratified sample, with equality as `θ ↑ a`** (§2.3).  Strictness for
`p ≠ ½` at `θ < a` — the statement the theory report leaves "not proved in general" — is the
failure of a saddle point (one law `Q` would have to be optimal for the worst centre types of both
problems, which are the constant centres for a product sampler and a mixed type for the stratified
one); I did not prove it.

### 9.4 B2 in detail

*The statement compared* (Proposition 11.103(e), [identity P, the rest N]).  For the uniform law on
`q` letters with the Hamming envelope, single dips on `k` equally weighted groups of letters give
`h_k = max_t[tΨ_k(u) − Ψ_k(tu)]`, `Ψ_k(s) = ln((e^s + k − 1)/k) − s/k`; "exactly at `e^u = k(k−1)`,
`h_k = h_{k+1}`"; the hardest number of groups is "about `e^{u/2}`".

*What it is* **[P; verified, `addendum_checks.py` Q2, Q2a–c]**.  Grouping into `k` classes is the
`k`-ary symmetric channel with correct-letter probability `p_k = L/(L + k − 1)`, `L = e^u` — the pairwise
likelihood ratio between the right group and any wrong one is `L` whatever `k`.  With
`F*_k(t) = tΨ_k(u) − Ψ_k(tu) = (1−t)C_t = (1−t)ln k + t ln(L + k − 1) − ln(L^t + k − 1)`:

* **the cutoff rate** `R_0(k) = C_{1/2} = 2F*_k(½) = ln[k(L+k−1)/(√L + k − 1)²]` is maximal over real `k`
  **exactly at `k = √L + 1 = e^{u/2} + 1`** (the derivative vanishes iff `k(√L − 1)² = (√L − 1)(L − 1)`);
* **reflection identity: at `L = k(k−1)`, `F*_k(t) = F*_{k+1}(1−t)` for all `t`**, i.e.
  `(1−t)C_t(W_k) = t·C_{1−t}(W_{k+1})` (two lines: `L + k − 1 = (k−1)(k+1)`, `L + k = k²`, and
  `(L^{1−t} + k)/(L^t + k − 1) = k^{1−t}/(k−1)^t`).  Hence at these slopes `h_k = h_{k+1}` *and*
  `R_0(k) = R_0(k+1)`: every functional of `F*` that is symmetric under `t ↔ 1−t` switches from `k` to
  `k+1` groups at `e^u = k(k−1)` — which is the report's crossing, with its "mismatch fractions add up
  to one";
* **the Shannon capacity obeys a different law**: `a_k = ln(k/(L+k−1)) + L ln L/(L+k−1)` is maximal
  at `k = (L−1)²/(L ln L − L + 1) ≈ e^u/u` (`2.95, 4.87, 8.85, 36.5` at `u = 1, 2, 3, 5`, against
  `e^{u/2} + 1 = 2.65, 3.72, 5.48, 13.2`); the crossing `a₂ = a₃` is at `u = 0.51937` (the report's
  `0.5194`).  So "about `e^{u/2}` states" is a statement about `h` (and `R_0`), not about `a` or `E`.

I also reproduced the report's `h_2, h_3, h_4` at `u = 0.5` and `u = 1` to six digits.

*Does it ring a bell?*  **[H, with the reading levels given]**  (i) The exact counterpart is the
choice of a modulation alphabet by the **cutoff rate**, the design rule of the sequential-decoding
era (Wozencraft–Jacobs; Massey 1974) `[from memory — unverified]`; for Massey's optical model the
cutoff rate of the `M`-ary erasure channel, `log M − log[1 + (M−1)ε]`, is the standard example
`[search snippet, via Arıkan, arXiv:cs/0508034]`.  The two formulas above (`k = √L + 1`,
`L = k(k−1)`) I did not find (two searches); they are elementary.  (ii) With `L` in the role of a
signal-to-noise ratio, `k ≈ √L` is the rule of thumb "about `√(1 + SNR) = e^C` amplitude levels" for
the Gaussian channel, whose rigorous form is the finiteness of the support of the capacity-achieving
input under an amplitude constraint (Smith 1971 `[not accessed]`) with the bound `O(A²)` on the
number of mass points (Dytso, Yagli, Poor, Shamai, arXiv:1901.03264 `[abstract]`).  (iii) The channel
itself — one detection, landing in the signal slot with probability `L/(L+k−1)` — is `k`-ary pulse
position modulation with a signal-to-background ratio `L` per slot, where "the optimal order" as a
function of signal and background is a standard optimisation (e.g. Jarzyna et al.,
arXiv:1709.00030 `[search snippet]`).  None of these states the `e^{u/2}` rule for an exponent of
the present kind.  *Classification of Proposition 11.103(e):* **(5) new combination** — an
elementary computation whose closed form (the reflection identity) and whose cutoff-rate reading
are, as far as two searches go, not in print.

### 9.5 Search log and sources of the addendum

Searches (continuing §4.9): 26. X `"importance sampling" sample size "sphere packing" OR
"sphere-packing exponent" OR "error exponent" OR "Hoeffding" "hypothesis testing" Neyman-Pearson Rényi
divergence required number of samples normalizing constant` → **nothing** with these exponents for
importance sampling (Sanz-Alonso; arXiv:2312.15256 App. A; two 2026 finite-sample hypothesis-testing
preprints).  27. S `"random energy model" "random code" glassy phase free energy "sphere packing"
exponent Mézard Montanari …` → Merhav's papers.  28. S `Csiszár 1995 "Generalized cutoff rates and
Rényi's information measures" …` → abstract-level snippets.  29. S `Forney 1968 … "E_2(R,T) =
E_1(R,T) + T" …` → Merhav, arXiv:0711.2501.  30. S `capacity-achieving input distribution finite
support number of mass points …` → arXiv:1901.03264.  31. X `optimal alphabet size "q-ary symmetric
channel" OR "M-ary" capacity maximized number of inputs … "pulse position modulation" optimal order`
→ nothing exact.  32. S `optimal PPM order capacity "pulse position modulation" background noise …` →
arXiv:1709.00030 (snippet).  33. S `"sphere packing" exponent "channel resolvability" OR "soft
covering" … below mutual information …` → arXiv:2409.18307, 1801.00714.  34. S `"cutoff rate" R_0
optimal alphabet size OR "number of signals" maximize cutoff rate … "Massey" "Wozencraft" …` →
Arıkan cs/0508034 (snippet).  35. X `"sums of random exponentials" OR "exponential functionals" …
"Rényi" OR "sphere packing" OR "Hoeffding trade-off" … importance sampling exponent …` → Forney's BSC
notes; nothing on sampling.

| source | read | used for |
|---|---|---|
| Merhav, IEEE-IT 55 (2009) 83–92; arXiv:0708.0850 | `[full text]` abstract, §1, §2.2.1–2.2.2 | B1 (b)1 |
| Merhav, arXiv:0711.2501 | abstract; the two passages with `E_2 = E_1 + T` | B1 (b)3 |
| Tomamichel & Hayashi, IEEE-IT 2018; arXiv:1511.04874v3 | `[full text]` abstract, §I, eqs. (2)–(6), (51)–(55) | B1 (b)3 |
| Nakiboğlu, arXiv:1608.02424v8; arXiv:1611.06924v8 | `[abstract]`; Definition 13, Lemma 13 of the second | B1 (a), (d) |
| van Erven & Harremoës, IEEE-IT 2014; arXiv:1206.2459 | Theorem 11; section "Channel capacity and minimax redundancy" (Thms 33–34) | B1 (a), §9.3 |
| Forney, *On exponential error bounds for random codes on the BSC* (MIT 6.441 course notes) | `[full text]` §1 | B1 (a) |
| Rohwer, Angeletti, Touchette, PRE 92, 052104; arXiv:1409.8531v3 | abstract, §II.B, §IV.B | B1 (b)2 |
| Yunger Halpern & Jarzynski, PRE 93, 052144; arXiv:1601.02637v2 | `[abstract]`, first page | B1 (b)2 |
| Merhav & Cohen, arXiv:1811.04363 | abstract, introduction | B1 (d) |
| Yagli & Cuff, arXiv:1801.00714v8; He, Pradhan, Winter, arXiv:2409.18307v4 | `[abstract]`, first page | B1 (c) |
| Sahai, arXiv:cs/0610139; Sanz-Alonso, arXiv:1608.08814; Masrani et al., arXiv:2107.00745 | `[abstract]` | B1 (d), (e) |
| Dytso, Yagli, Poor, Shamai, arXiv:1901.03264v4 | `[abstract]` | B2 |

*Not accessed:* Csiszár 1995; Shannon–Gallager–Berlekamp 1967; Forney 1968; Arikan 1996;
Arikan–Merhav 1998; Mézard–Montanari 2009; Smith 1971; Wozencraft–Jacobs; Massey 1974; Hoeffding
1965; Blahut 1974; `W_REPORT.md` of the theory division (only §11.26 of the theory report was read).

### 9.6 Requests that follow (additions to §7)

- T7. In §11.26, replace "not found" for the dictionary by: *the formulas are classical; the
  mechanism is the glassy phase of the random code ensemble (Merhav 2009; Mézard–Montanari), the
  Hoeffding trade-off against product alternatives (Tomamichel–Hayashi 2018) and, on the cube, the
  Jarzynski bias curve (Suárez–Silbey–Oppenheim 2012); the non-adaptive lower bound is the
  sphere-packing argument with the sampling law as auxiliary output law; what is not in print is
  that an adaptive algorithm attains `E_sp(θ) − θ`.*  Say explicitly that feedback does **not** beat
  `E_sp` in channel coding (Nakiboğlu; Sahai), so the adaptive theorem is not a transposition of a
  coding theorem.
- T8. Check Proposition A1.2 and, if it stands, move "upper bounds at bounded accuracy" from "not
  done" to done for non-adaptive algorithms; state the sampler as "the product of the Shannon
  centres".
- T9. Proposition 11.103(e): add the reflection identity `F*_k(t) = F*_{k+1}(1−t)` at `e^u = k(k−1)` and
  the cutoff-rate optimum `k = e^{u/2} + 1`; restrict "about `e^{u/2}` states" to `h` (the capacity `a`
  follows `≈ e^u/u`).
