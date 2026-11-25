# Workstream A1 — running notes (prior art & originality of the query-complexity cluster)

Started 2026-11-25 17:40 UTC.  Writable: this directory + docs/science/workstreams/A1_REPORT.md.
Rules: no git state changes; never fabricate; reading-level tags [full text]/[abstract]/[search snippet]/[from memory — unverified].

## Step log

### Step 0 (17:40 UTC) — orientation
- Read COMMON.md and A1_brief.md in full.
- Created experiments/science/ws_A1/.
- Listed THEORY_REPORT headings (569 kB; §11.10, 11.16–11.21, 11.23–11.25 are the relevant sections; §10 = G-table; §13 = references).
- Next: read README, §10 rows G11, G18–G27, then the sections, then L7_query_complexity.md.

### Step 1 (≈17:55 UTC) — read theory statements (README status; §10 rows G11, G18–G27; §11.10; §11.16; §11.18; §11.19)
Exact claims as the report has them (my condensed restatement, to be compared against sources):
- **Model**: X finite; class L_u = {g : |g(x)-g(y)| ≤ c d_H(x,y)} on {0,1}^n, u = βc. Algorithms query g(x) exactly (noise-free oracle),
  randomised = finite mixture of deterministic adaptive query algorithms; (ε/2, δ)-correct for ln Z = ln Σ e^{-βg} on EVERY class member.
  Cost = E|Q(g)| at an instance (lower bounds) / worst case over the class.
- **G11 / Thm 11.25**: Λ₁ = ln(2/(1+e^{-u})) "soft gap of one site"; ε = nε₁. ε₁ > ln cosh(u/2): bounded number of uniform samples suffices on every instance
  (sandwich: n ln2 − β m̂ ≤ ln Z ≤ n ln 2 − β m̂ + n ln cosh(u/2), i.e. Jensen + Hoeffding-lemma-type bound with exact two-point constant).
  ε₁ < ln cosh(u/2): every algorithm needs ≥ (1−2δ)2^n/|B(k)| at the zero residual (hidden dips: g' = min(0, -c(k+1) + c d_H(·,y)));
  exponent ln2 − h((Λ₁+ε₁)/u) = KL((Λ₁+ε₁)/u ‖ ½); matching upper bound WITH HINT (hedged spot-check; Harper's theorem).
  Accuracy diagram at zero residual down to e^{-λn}.
- **G18 / Thm 11.44–11.45**: non-adaptive exponent θ_na(ε₁) = min{KL(ρ‖½): KL(ρ‖p_u) ≤ ε₁}, p_u = 1/(1+e^u); at fixed accuracy a = KL(p_u‖½).
  Upper: plain MC (uniform samples) on the whole class via tail lemmas (Harper). Lower: cones c·d_H(·,s) vs flattened cones max(c d_H, cR) with hidden centres s,
  Bakhvalov averaging — "method of Mathé–Novak 2007".
- **G20 / Thm 11.51–11.54**: adaptive, no hint: exponent θ_hint(ε₁) = KL((Λ₁+ε₁)/u ‖ ½). Upper bound: nested "layer-cake" two-level algorithm iterated k levels
  (outer block uniform sample, inner bracket procedures refined only to resolve one-sided level tests, tail lemma to close);
  recursion R[T]; identity KL(ρ‖p_u) = KL(ρ‖½) + uρ − Λ₁  ⇒ θ_na(e + θ_hint(e)) = θ_hint(e).
- **G21 / Thm 11.56–11.58**: same at bounded accuracy: adaptive exponent h = KL(Λ₁/u‖½) vs non-adaptive a = KL(p_u‖½).
- Their own prior-art statements: Mathé–Novak 2007 (method; adaption breaks curse for log-concave class), Chatterjee–Diaconis 2018 (sample size e^{KL}),
  Holzmüller–Bach 2025 (two regimes), Ge–Lee–Lu 2020, Heinrich 2024, Kunsch–Novak–Wnuk 2024, nested sampling / multilevel splitting / nested simulation (Broadie–Du–Moallemi; Giles–Haji-Ali),
  Bobkov–Houdré–Tetali; Dzindzalieta (extremal Lipschitz functions = distance functions to Harper sets) — "abstracts / search summaries only".

### Step 2 (≈18:10 UTC) — read §11.20 (Thms 11.59–11.65), §11.21 (Thm 11.66), §11.23 (Thm 11.76 + group remark), §11.24 (Thms 11.84–11.88), §11.25 (Lemma 11.89, Thm 11.90, Cor 11.91), §13 refs, prior_art/L7 in full
- **G22**: p-biased cube. θ_na = max_m min{I(S;X): D(P_{X|S}‖π_s|P_S) ≤ ε₁}, attained by type-uniform ("flat histogram") sample; adaptive = R^max = max_γ R_γ (hardest additive instance);
  Thm 11.63 asymptotic isoperimetry for the type-uniform mixture μ_H (method of types / inherently typical subsets).
- **G23**: shear law x_na(θ) = e_hint(θ)+θ; Thm 11.66: game function F on [0,1], R(e) = max_{t≤1}[F(t) − te] (a Legendre-type transform with slope constraint), θ_na = R∘(id+R)^{-1}; level recursion converges.
- **G25 / Thm 11.76**: exchangeable π; type-stratified sample optimal among non-adaptive up to factor 8(n+1)ln(2(n+1)/δ)/(1−2δ); lower bound (1−2δ)/q via random permutations σ of pair (ψ, ψ^{tr,q});
  generalised to any finite group Γ acting with invariant envelope and π: orbit-stratified sampling optimal up to N_orb factor. ← candidate "known principle": invariance / Hunt–Stein / Kiefer invariant designs / Bakhvalov averaging over a group.
- **G26**: r-round algorithms; τ^(1)=a > τ^(2) ≥ θ₂* > h = lim τ^(r); Lemma 11.85 (virtual-run/indistinguishability for block-radial functions with hidden centres) — "pointer-chasing kind".
- **G27 / Lemma 11.89**: 2×2 table with log odds ratio 2s ≥ 0 ⇒ I(B;X) ≤ ln2 − h(σ(s)), σ(s)=1/(1+e^{-s}); equality iff s=0 or both marginals uniform.
  Proof in report: Ising-pair parametrisation, gradient computation, 6 steps (≈35 lines).
- L7 says: nobody in the project read Novak 1988, Nemirovski–Yudin, Ge–Lee–Lu, Harper, Heinrich in full; R5 read Mathé–Novak §§1–4.1, §5 in full; R3 read Holzmüller–Bach pp. 1–13.
  L7 mentions two 2026 preprints (arXiv 2609.20337 "Optimal simulated annealing for partition function estimation"; arXiv 2604.01263 lower bounds adaptive/non-adaptive schedules) — from search summaries only. I must check these.

My own first observations (before searching; [P]-level, to verify numerically):
 (O1) With w = e^{-βg}, the class {w>0 : w(x) ≤ e^{u d(x,y)} w(y)} is a CONVEX CONE and Z = Σ w is a LINEAR functional; ln-accuracy = relative error.
      So the whole cluster is "integration on a convex cone with relative error" — in IBC language adaption can help on non-symmetric convex sets. The theory report (and R5) say "ln Z is not linear so IBC adaption results do not apply"; more precise: the problem IS linear in w, the class is a cone (not symmetric), the error criterion is relative.
 (O2) θ_na formula at the cone instance = REM-type "frozen" analysis of an exponential average with e^{nθ} samples (deficit n·KL(ρ_θ‖p_u), KL(ρ_θ‖½)=θ) → check Jarzynski-estimator/REM literature (Palassini–Ritort 2011; Suárez–Silbey–Oppenheim 2012; Zuckerman–Woolf 2002; Gore–Ritort–Bustamante 2003) and Ben Arous–Bogachev–Molchanov "Limit theorems for sums of random exponentials" (2005).
 (O3) Lemma 11.89: capacity of a binary-input binary-output channel = max chord gap of k(m) = ln2 − h((1+m)/2) between the two output means = Bregman information radius of two natural parameters a,b (a−b = 2J) for λ = ln cosh. Lemma ⟺ this radius is maximal for a = −b. Candidate slick proof to try.
 (O4) "Adaptivity replaces the hint" has a conceptual precedent in sequential design of experiments (Chernoff 1959) and pure-exploration bandits (Garivier–Kaufmann 2016 Track-and-Stop; Karnin 2016 "verification based"): asymptotically the cost of identification equals the cost of verification (the oracle allocation), which a static (non-adaptive) allocation cannot attain. Different regime (noise, δ→0) — to be read and compared.
 (O5) G25 symmetry part looks like the invariance principle for minimax designs (Kiefer 1959; Hunt–Stein) — to be checked.

### Step 3 (17:45 UTC) — tooling + Mathé–Novak 2007 read in FULL TEXT
- WebFetch's small model refuses verbatim quotes >125 chars and only summarises → for "full text" I download PDFs with curl (works for arxiv.org) into scratchpad and read pdftotext output myself.
- **Mathé & Novak, "Simple Monte Carlo and the Metropolis algorithm", arXiv:math/0611285v2 (J. Complexity 23 (2007) 673–696)** [full text: §§1–5 read line by line from pdftotext; appendix (proof of Lemma 12) not read].
  * Problem: S(f,ρ) = ∫fρ dμ / ∫ρ dμ (expectation under an unnormalised density), oracle for values of f and ρ, error = worst-case root-mean-square over a class; "non-adaptive" = nodes do not depend on earlier values (IBC notion).
  * Class F_C: sup ρ/inf ρ ≤ C, ‖f‖∞ ≤ 1. **Thm 1 (ALL methods, adaptive or not)**: e(S_n,F_C) ≥ (√2/6)·sqrt(C/2n) for 2n ≥ C−1 — complexity linear in C; hidden cells where ρ = C, f = ±1 (Bakhvalov prior). **Thm 2**: simple MC ≤ 2 min(1, sqrt(2C/n)). So on F_C "no sophisticated MCMC can help".
  * Class F^α: Ω convex body in R^d, ρ log-concave, |log ρ(x) − log ρ(y)| ≤ α‖x−y‖₂, ‖f‖_{2,ρ} ≤ 1. **Thm 3 (non-adaptive only)**: e ≥ 2^{-d/2-3/2}(vol Ω/vol B^d)^{1/2} α^{d/2} n^{-1/2}/sqrt(d!), by Bakhvalov averaging over ρ_i = c_i exp(−α‖y−y_i‖) with 2n hidden centres (sphere packing, Minkowski–Hlawka) and f_i = ±c̃_i·1_{B(y_i,r)}.
    Remark 5 verbatim idea: an adaptive method identifies i from one value of ρ ("the functions ρ_i are global").
  * **Thm 5 (adaptive)**: Metropolis ball walk, lim_n sup e²·n ≤ 594700 (d+1) max(d+1, α²) on F^α(B^d); uses conductance + isoperimetry for log-concave measures (Vempala's survey [29]). Only asymptotic in n; (40) "n(ε) ≤ C ε^{-2} d max(d, α²)" stated as a belief, not proved.
  * They do NOT treat the normalising constant: p.1 says computing 1/c = ∫ρ "is often as hard as the original problem (1)".
  → Comparison with theory report Thm 11.45: same mechanism (hidden centres of cones exp(−α·dist), Bakhvalov averaging, defeated by one adaptive query). Differences: (i) target ln Z itself, pairs cone / flattened cone instead of an integrand f supported at the centre; (ii) discrete cube, growing dimension, exponent in n; (iii) a matching class-wide upper bound.  The report's attribution ("method of Mathé–Novak") is accurate.
  → For G20: Mathé–Novak's adaptive upper bound needs log-concavity; nothing there about non-log-concave Lipschitz-log classes, and nothing like "adaptive = hinted".
  → New observation: Mathé–Novak Thm 1 is the F_C analogue of the HINTED lower bound (hidden needles); on the cube class C = e^{un} but Lipschitz needles must be Hamming balls, which is what lowers e^{un} to e^{nθ_hint}.

### Step 4 (17:46 UTC) — Holzmüller–Bach read in full text for the parts that bear on G11
- **Holzmüller & Bach, "Convergence rates for non-log-concave sampling and log-partition estimation", JMLR 26 (2025) 1–71, arXiv:2303.03237v4** [full text read: abstract, §1 (incl. Lemma 3), §1.1, §1.2, §2.1, §2.2, Table 1, and in Appendix B.2 the proofs of Thm 8 and Prop 9; rest (§§3–6, other appendices) only grepped for "adaptive", "cosh", "open", "conjecture"].
  * Setting: X = [0,1]^d, d FIXED; class F_{d,m,B} = {‖f‖_{C^m} ≤ B}; L_f = log∫e^f; rates in n (evaluations) and B, constants C_{m,d} "often necessarily exponential in d" ignored.
  * Deterministic points (adaptive or not): e_n = Θ_{m,d}(B n^{-m/d}) (Thm 6) — "the same rates hold for adaptive points".
  * Stochastic points (adaptive allowed): upper bound min{B n^{-m/d}, exp(C B n^{-m/d}) B n^{-1/2-m/d}} (Thm 8: approximate f by g, then importance-sample from P_g); lower bound Ω(B n^{-m/d}) − d log(1+3B) (Prop 9: reduction to optimisation via Lemma 3 |M_f − εL_{f/ε}| ≤ εd log(1+3d^{-1/2}|f|₁/ε) and Novak 1988).
    "We leave a lower bound outside of the optimization regime as an open problem; however, we conjecture that the rate B n^{-1/2-m/d} ... cannot be improved."
  * NOT there: ln cosh; any exact threshold constant; growing dimension; a separation adaptive vs non-adaptive (none claimed: deterministic rates equal; the stochastic class is defined with adaption only); instance-wise or hinted complexity.
  * The cube case is NOT a corollary: fixed-d rates with unspecified (m,d)-constants say nothing about exponents in the dimension; class and domain differ.
  → The theory report's sentence "that randomisation helps for ln Z only above an accuracy scale is known for smoothness classes (Holzmüller–Bach 2025, §2.2)" is an accurate description of the qualitative relation. Direction check: in H–B the "optimization regime" is LARGE B n^{-m/d} (rough function/few points) where stochastic = deterministic rate; "quadrature regime" where MC gains n^{-1/2}.

### Step 5 (17:48 UTC) — ITEM 7 (Lemma 11.89): FOUND IN PRINT
Searches (WebSearch):
 S1 "mutual information 2x2 contingency table fixed odds ratio maximized uniform marginals" [standard] → hits: arXiv 2203.08089 (Williams), 1302.6161 (Hasenclever–Scholz), 2404.04343, 2601.07369 …
 S2 "odds ratio" "mutual information" … "binary asymmetric channel" "same odds ratio" [extended] → 2610.12805 (Lin, Sklar-type decomposition, Oct 2026), 2203.08089; nothing on channel capacity at fixed odds ratio.
 S3 Geenens copula discrete odds ratio margin-free mutual information [standard] → Geenens 2020 framework (copula pmf = uniform-margin table with same odds ratios), no MI statement in snippets.
Downloaded and read (pdftotext):
 * **D. Hasenclever & M. Scholz, "Comparing measures of association in 2x2 probability tables", arXiv:1302.6161v1 (22 Feb 2013)** [full text of §§1–3.3 and of the appendix proof of Prop. 8 read; rest skimmed].
   Coordinates Θ(t) = (x,y,z) = (ln√(p00p11/p01p10), ln√(p00p01/p10p11), ln√(p00p10/p01p11)); x = half log odds ratio (= s of the theory report); planes x = const are the orbits of margin transformations; origin (y,z)=(0,0) = table with diagonal symmetry = uniform margins.
   **Proposition 8(a): "For all x ∈ R∖{0}: sMutInf_x has exactly one maximum at the origin (y, z) = (0, 0)."** (sMutInf = sign(D)·mutual information; subscript x = restriction to fixed odds ratio.) Part (b): sMutInf_x → 0 as ‖(y,z)‖ → ∞.
   Proof (appendix): derivative of MI along the two one-parameter margin flows t_μ ∝ (μp00, p01; p10, p11/μ), t_ν ∝ (p00, p01/ν; νp10, p11):
     d/dμ MI|_{μ=1} = (p11−p00)·MI + p00 p11 [ log(1+p00(1/λ−1))/p00 − log(1+p11(1/λ−1))/p11 ], both terms ≥ 0 for p00 ≤ p11, λ>1, zero iff p00 = p11, because x ↦ log(1+x(1/λ−1))/x is decreasing.
   I re-derived this: (i) derivative = Cov(ι, 1[00]−1[11]) by the exponential-family formula; (ii) (p00+p01)(p00+p10) = p00[1 + p11(1/λ−1)] so ι00 = −ln(1+p11(1/λ−1)), ι11 = −ln(1+p00(1/λ−1)); (iii) ln(1+ax)/x is decreasing in x (concavity of ln). The proof is correct (the arXiv text has label typos S.x/A.x).
   ⇒ **This IS Lemma 11.89 including the uniqueness of the maximiser.** Stated for sMutInf in bits; identical content.
 * **C. K. I. Williams, "On suspicious coincidences and pointwise mutual information", Neural Computation 34(10) (2022) 2037–2046, arXiv:2203.08089v3** [full text read pp. 1–7]: defines Yule's "canonical table" (margins ½, same odds ratio λ), eq. (10): I_λ = (√λ/(1+√λ)) log √λ − log(1+√λ) + log 2 (= ln 2 − h(σ(s)), √λ = e^s — the right-hand side of Lemma 11.89), and remarks on Yule's smallpox table: "the MI is lowest in the original (unbalanced) table, and increases as the marginals are balanced" — an observation on an example, no theorem; cites "Hasenclever and Scholz (2016, p. 24)".
 * arXiv:2610.12805 (Yi-Yu Lin, Oct 2026) [abstract + grep]: uniform-margin representative ("dependence nucleus"), no MI statement.  arXiv:2404.04343, 1901.08741: downloaded, not yet read.
Verdict item 7: **(1) established prior art** (Hasenclever–Scholz 2013/2016, Prop. 8(a)); the capacity re-phrasing is an immediate corollary (capacity = max over inputs = max over one margin).
Shorter proof than the report's 35 lines: monotone margin flows + "ln(1+ax)/x decreasing" (5 lines). To verify numerically next.

### Step 6 (17:50 UTC) — numerics for Lemma 11.89 (own code: odds_ratio_check.py, output odds_ratio_check.out; 19 s)
- T1: 400 000 random 2×2 tables: max(I − bound) = −3.1e−13 (no violation); equality at uniform margins to 1e−15; strict off the origin.
- T2: dI/dt = Cov(ι, φ) = (p11−p00)I + p00p11[g(p00) − g(p11)], g(x) = ln(1−cx)/x, c = 1−1/λ: agrees with finite differences to 5e−11 on 20 000 tables, sign = sign(p11−p00); same for off-diagonal flow.
- T3: I monotone along diag flow then off-diag flow, endpoint = symmetric table, on 3000 random tables (global check of the flow proof).
- T4: capacity of binary channel = largest chord gap of the binary entropy between the two output laws (agreement 6e−16) and ≤ BSC with same odds ratio on 4000 random channels.
- T5: 25 000 tables on a grid in 40-digit arithmetic: strictly below the bound off the origin (closest −5.2e−5).
- T6: mutations (tightened bound; bound at 0.9 s; "one uniform margin suffices") all detected.  [First version of T6/T7 had two errors of test design — a mutation too weak to fail, and a random search that was required to find an optimum; fixed, recorded here.]
- T7: 3-letter Potts pair at s = 0.3: I(uniform on 3 letters) = 0.010582 < I(uniform on 2 letters) = 0.011125 — the lemma is a 2×2 fact (agrees with the theory report's remark after Cor. 11.91).
[P, checked numerically] Short proof of Lemma 11.89 (flows): see report §2.

### Step 7 (17:50 UTC) — sampling-oracle line (adaptive vs non-adaptive, rounds): two 2026 preprints read
 S4 WebSearch "Hasenclever Scholz … journal 2016" → published version: The Open Statistics & Probability Journal 7 (2016) 20–35?, DOI 10.2174/1876527001607010020 [search snippet; Bentham Open page not opened]. Williams 2022 cites it as "Hasenclever and Scholz (2016, p. 24)".
 S5 WebSearch "partition function estimation Gibbs distribution sampling oracle lower bound adaptive versus non-adaptive cooling schedule 2026 arXiv" → 2609.20337, 2604.01263, Kolmogorov COLT18, 2404.02414 (Chen–Nannicini).
 * **Guo, Liu, Yang, Yin, Zhang, "Optimal simulated annealing for partition function estimation", arXiv:2609.20337v1 (17 Sep 2026)** [full text read: abstract, §1 incl. Def 1.1, Thms 1.2–1.4, Table 1; proofs not read].
   Oracle: query β ∈ [β_min, β_max], receive H(X), X ~ μ_β (a SAMPLING oracle). "non-adaptive if all query parameters are fixed before any samples are observed"; "sampling rounds".
   Thm 1.2: non-adaptive, O(q ε^{-2} log h) calls (q ≥ log Q, h ≥ E H).  Thm 1.3 (all algorithms): Ω(min{q log h, q²} ε^{-2}).  Thm 1.4 (non-adaptive): Ω(min{q log h, e^q} ε^{-2}).
   So in that model adaptivity is worth nothing when log h ≤ q, and up to e^q/q² when h is huge (adaptive TPA O(q² ε^{-2}) vs non-adaptive e^q ε^{-2}).
   Table 1 lists "rounds of sampling" for [DFK91; BŠVV08] (1 round, q² ε^{-2} log h), [ŠVV09] (Õ(√q) rounds), [Hub15; Kol18; HK24] (Õ(q) rounds), [HKL+26] (1 or 3 rounds).
 * **Harris, Kolmogorov, Liu, Yin, Zhang, "Near-optimal parallel approximate counting via sampling", arXiv:2604.01263v2 (12 Jul 2026)** [abstract + first 2 pages read]: non-adaptive O(q ε^{-2} log² h); O(q ε^{-2} log h) "with just two additional adaptive rounds".
 → Bearing on G20/G26: adaptive-vs-non-adaptive and ROUNDS of adaptivity for partition-function estimation are an active 2026 topic, but in the sampling-oracle model, at polynomial scale, where one round is (nearly) enough. Not the value-query model on a Lipschitz class; no exponent hierarchy. Must be cited; does not anticipate.

### Step 8 (17:53 UTC) — IBC adaption literature read (PDF text)
 * **Krieg, Novak, Ullrich, "On the power of adaption and randomization", arXiv:2406.07108v2 (31 Jul 2025)** [full text read: §1 (intro, Thm 1, Table 1, Thm 2), §2 beginning, §6.1 (Table 2, examples (1)–(6), open problems), §6.3 (Thm 19 and examples); §§3–5 (proofs) not read].
   - Linear S, F convex AND symmetric, deterministic: adaption gains at most a factor 2 ([Bakhvalov; Gal–Micchelli; Traub–Woźniakowski] as cited there).
   - "For non-symmetric sets, it was proved in [47] (Novak, The adaption problem for nonsymmetric convex sets, JAT 82 (1995)) that the largest possible gap between those errors is bounded above by 4(n+1)²."
   - Thm 1: e^{det-non}_{2n−1}(S,F) ≤ 12 n^{3/2} (Π_{k<n} e^{ran}_k(S,F))^{1/n} for every convex F (linear information); n instead of n^{3/2} if Y Hilbert. Table 1/2: maximal gain in the RATE: convex+symmetric: 1 (½ if Y Hilbert); only convex: in [1, 3/2] (≤ 1 if Y Hilbert).
   - §6.1(5): for convex non-symmetric F and standard information "there are more extreme examples, where adaption yields a gain up to the order n, see again [46]" ([46] = Novak, Optimal recovery and n-widths for convex classes of functions, JAT 80 (1995) 390–408 — NOT read by me).
   - "Possibly the most interesting open problem": the same question for function values (standard information).
 * **Novak, "Optimal algorithms for numerical integration: recent results and open problems", arXiv:2307.06787v1** [Remark 1 read; grep for adapti/density/Metropolis]: nothing on unknown densities / normalising constants; Remark 1(d): Heinrich solved the adaption problem in the randomized setting ("for some classes F adaption helps a lot").
 * **Heinrich, "Randomized complexity of mean computation and the adaption problem", arXiv:2401.14100v1** [abstract + first page]: scalar-valued mean computation in mixed-norm sequence spaces; adaptive vs non-adaptive randomized n-th minimal errors differ by a power of n, "up to log factors of the order n^{1/4}".
 * **Kunsch, Novak, Wnuk, "Randomized approximation of summable sequences – adaptive and non-adaptive", arXiv:2308.01705v3** [abstract]: ℓ₁^m → ℓ∞^m, "gap of order n^{1/2}(log n)^{-1/2}"; non-adaptive complexity has a √log m term, adaptive only log log m.
 * Kunsch–Wnuk arXiv:2410.23067v2 [abstract only].
 **My reading (new, to go in the report):**
   (R1) The theory report says IBC adaption results do not apply "because ln Z is not linear". Sharper: in the weights w = e^{-βg} the solution operator Z = Σw IS linear and the class {w>0, w(x) ≤ e^{u d(x,y)} w(y)} is a convex CONE; what is non-standard is (i) the class is not symmetric, (ii) the error is RELATIVE (log-scale), (iii) standard information.
   (R2) The "shear law" x_na(θ) = e_hint(θ) + θ, with N = e^{nθ} evaluations, reads ε_na(N) = ε_ad(N) + ln N + o(n): **the multiplicative error of the best non-adaptive method exceeds that of the best adaptive one by a factor equal to the cardinality N** (at the exponential scale). I.e. G20–G23 are an instance of "adaption gains one power of n for a linear functional on a non-symmetric convex class" — the order that Novak's examples with standard information reach and that the KNU upper bounds allow (rate gain ≤ 1 for Hilbert target, linear information, absolute error).  [H] analogy, not a corollary: KNU/Novak concern absolute error; here the criterion is relative, on a cone.
   → This is the single most useful translation for an IBC audience, and it tempers "exponential separation": the separation is exponential in the dimension because the error scale is e^{n·rate}; in IBC units (error at fixed cardinality) it is a factor N^1.

### Step 9 (17:54 UTC) — importance-sampling sample size and the REM/Jarzynski line: **the non-adaptive exponent FORMULA and "ln cosh" are in print**
 S6 WebSearch "Jarzynski estimator finite sample bias random energy model …" → Suárez–Silbey–Oppenheim arXiv:1108.5783; Palassini–Ritort arXiv:1108.0605.
 S7 WebSearch "Ben Arous Bogachev Molchanov limit theorems for sums of random exponentials …" → PTRF 132 (2005) 579–612 [search snippet only; not opened].
 * **Chatterjee & Diaconis, "The sample size required in importance sampling", arXiv:1511.01437v3 (Ann. Appl. Probab. 28 (2018))** [full text read: abstract, §1 through Thm 1.1 and its discussion, §3 Thms 3.4, 3.5 with surrounding text; proofs not read].
   Thm 1.1: n = exp(L+t), L = D(ν‖μ): E|I_n(f) − I(f)| ≤ ‖f‖_{L²(ν)}(e^{-t/4} + 2 sqrt(P(log ρ(Y) > L + t/2))); n = exp(L − t): P(I_n(1) ≥ 1−δ) ≤ e^{-t/2} + P(log ρ(Y) ≤ L − t/2)/(1−δ).
   Thm 3.4 (Gibbs measures, thermodynamic limit, samples from G_{N,β₀}, n = exp(b L_N)): Ẑ/Z → 1 iff b > q(β) := p(β₀) − p(β) − (β₀−β)p′(β) (given no first-order transition); at b = q only L_N^{-1} log Ẑ → p(β).
   For the cone instance sampled uniformly (β₀ = 0, H = Hamming distance to the centre, p(β) = ln(1+e^{-β})): q(u) = KL(p_u‖½) = a.  So "a = bounded-accuracy exponent of plain MC at the cone" is exactly C–D Thm 3.4 [K].
 * **A. Suárez, R. Silbey, I. Oppenheim, "Phase transition in the Jarzynski estimator of free energy differences", arXiv:1108.5783v2 (Phys. Rev. E 85, 051108 (2012))** [full text read: abstract, §I, the section "sudden compression of an ideal gas" (eqs. 26–46), Appendix C; rest skimmed].
   Setting: n_m ~ Bin(N, ½) i.i.d., W_m = ε n_m, estimator ΔF_M = −log((1/M)Σ_m e^{-ε n_m}), M = 2^{γN}.  THIS IS plain Monte Carlo for ln Z at the cone instance u·d_H(·,s) with u = ε, N = n, M = e^{nθ}, θ = γ ln 2.
   (31) ΔF = N log(2/(1+e^{-ε})) [= nΛ₁, the theory report's "soft gap of one site"].
   (39)–(43): E[ΔF_M] = N log(2/(1+e^{-ε})) if ε ≤ ε_c(γ); = N[γ log 2 + ε/(1+e^{ε_c})] if ε > ε_c; ε_c(γ) = log((1−ρ)/ρ), ρ = h₂^{-1}(1−γ).
   (44): "For a fixed value of ε the bias is maximum for M = 1: B_max(ε) = N(ε/2 − log(2/(1+e^{-ε}))) = N log cosh(ε/2)."
   Appendix C: the "discrete random energy model" (2^K levels, binomial energies; refs Moukarzel–Parga 1991, Ogure–Kabashima 2009): E log Z_M = K log 2 + N log cosh(β/2) (β ≤ β_c), ½βN tanh(β_c/2) (β > β_c).
   **Translation (my algebra, to be checked numerically):** with ρ = h₂^{-1}(1−γ), i.e. KL(ρ‖½) = θ: bias/N = θ + uρ − Λ₁ = KL(ρ‖p_u) for ρ > p_u (identity KL(ρ‖p_u) = KL(ρ‖½) + uρ − Λ₁), and 0 for ρ ≤ p_u.
   ⇒ (i) the function θ_na(ε₁) = min{KL(ρ‖½): KL(ρ‖p_u) ≤ ε₁} of Theorem 11.44/11.45 is, in parametric form, the S–S–O bias curve (their eq. 43) — for plain MC at one instance, in expectation, in the scaling limit, by the REM correspondence;
      (ii) the threshold n ln cosh(u/2) of Theorem 11.25 is their B_max (eq. 44) — the bias of the one-sample estimate = the Jensen gap at the cone;
      (iii) their form "N γ log 2 + N ε ρ" = "ln M + (energy of the frozen level)" is the shear law at this instance: non-adaptive accuracy = ln(sample size) + (uρ − Λ₁)n.
   What S–S–O do NOT have: a class of instances, a minimax statement, lower bounds for all non-adaptive algorithms, high-probability (ε,δ) statements, adaptive algorithms. Their derivation is the physicists' REM mapping (expectation of the log, scaling limit), not a finite-n theorem.
 * Palassini & Ritort, arXiv:1108.0605v1 (PRL 107, 060601 (2011)) [abstract + first column read]: bias of the Jarzynski estimator via mapping to the REM, scaling variable (log N)/μ; "convergence … requires N ≫ exp(D_typ)".
 → For G18: formula known at one instance (K); new = minimax over the Lipschitz class + all non-adaptive algorithms (lower bound by Mathé–Novak's method) + Harper tail lemmas. Classification moves from "exponent … not found" to "(3) known special case exists / (5) new combination".

### Step 10 (17:57 UTC) — rounds; flat histogram / worst-case proposals; isoperimetric exponents; verification vs identification; nested simulation
 S8 WebSearch "Canonne Gur An Adaptivity Hierarchy Theorem for Property Testing …" → arXiv:1702.05678.
 S9 WebSearch "Bar-Yossef Kumar Sivakumar Sampling algorithms: lower bounds and applications …" → only secondary snippets (a lecture slide: "for symmetric functions, uniform sampling is the best possible"); paper NOT opened. [search snippet]
 S10 WebSearch (extended) "minimax optimal importance sampling proposal over a class … multicanonical/flat histogram … orbits symmetry" → Cérou–Héas–Rousset 2212.04292; Beh–Morio 2611.20831 (16 Nov 2026); Shakirov 2402.05653; survey 2502.07396.
 S11 WebSearch "Kiefer invariant designs … optimal design invariant under group …" → Idais–Schwabe arXiv:2011.09745 (snippet: "if the criterion is invariant under a group and convex, an optimal design can be found among invariant designs"), Pukelsheim's papers. [search snippet; PDF downloaded, passage to be located]
 S12 WebSearch "Karnin Verification Based Solution for Structured MAB Problems" → NeurIPS 2016 paper.
 S13 WebSearch "Chernoff 1959 Sequential design of experiments …" → secondary descriptions only. [search snippet]
 Read:
 * **Canonne & Gur, arXiv:1702.05678v1 (CCC 2017; Comput. Complexity 27 (2018))** [abstract + intro p.1 read]: k-round-adaptive testers; for every n and 0 ≤ k ≤ n^{0.99} a property with a k-adaptive tester of Õ(k) queries while every (k−1)-adaptive tester needs Ω(n). Constructed properties (and cycle-freeness); nothing on estimation of sums/normalising constants.
 * **Cérou, Héas, Rousset, "Entropy minimizing distributions are worst-case optimal importance proposals", arXiv:2212.04292v1** [abstract + §1 pp.2–4 read]: targets η in a convex class C; cost = Ent(η|μ) (justified by Chatterjee–Diaconis); worst-case log-cost relative to a reference π: WLC_h(μ|π) = sup_{η∈C, Ent(η|π)≤h} Ent(η|μ) − h; optimal μ = entropy minimiser within C. A minimax theory of proposals over a class of targets — criterion relative to a reference and KL-based; no (ε,δ)-certified estimation, no lower bound for all non-adaptive algorithms, no flat-histogram statement.
 * **Beh & Morio, "Optimal importance sampling densities for estimating several expectations at once", arXiv:2611.20831v1 (16 Nov 2026)** [abstract, §1, Table 1 read]: one proposal serving K quantities; for "probabilities of events, max_k C_kk/m_k²" (minimax relative variance) the optimal density is "essentially the equal mixture of the f|A_k"; histogram cells: allocation laws, equal mass in the minimax-relative-error limit. → the variance-based, finite-family form of "a flat histogram is minimax for relative error across cells". Very recent; must be cited next to Berg–Neuhaus for G22/G25.
 * **Lei Yu, "Exact exponents for concentration and isoperimetry in product Polish spaces", arXiv:2205.07596v3** [abstract + intro read; two-column text garbled by pdftotext, theorem statements only located, not studied]: variational formulas for asymptotic exponents of the isoperimetric function of PRODUCT measures (generalising Ahlswede–Zhang from finite to Polish spaces), two measures and a cost allowed. Nothing on mixtures/exchangeable references. Consistent with R9's reading that Thm 11.63 is a new variant proved by the known method.
 * **Garivier & Kaufmann, "Optimal best arm identification with fixed confidence", arXiv:1602.04589v2 (COLT 2016)** [abstract read]: tight instance-dependent lower bound; Track-and-Stop "tracks the optimal proportions of arm draws highlighted by the lower bound" and is asymptotically optimal.
 * **Karnin, "Verification based solution for structured MAB problems", NeurIPS 2016** [abstract + intro read from the proceedings PDF]: "additional structure is known in advance, causing the task of verifying the optimality of a candidate to be easier than discovering the best arm … in this high confidence regime, identifying the best arm is as easy as the task of verification"; cost H_explore + H_verify.
   → conceptual precedent for "adaptivity replaces the hint" (search = verification asymptotically): there the asymptotic parameter is δ → 0 with noisy observations; in the theory report it is the dimension n with exact evaluations and fixed δ. The pattern "query complexity ≤ learning + verification" of §11.10 is Karnin's explore–verify.
 * **Ge, Lee, Lu, arXiv:1911.03043v2 (STOC 2020)** [abstract read]: strongly log-concave, queries to f and ∇f; upper Õ(d^{4/3}κ + d^{7/6}κ^{7/6})/ε², lower bound d^{1−o(1)}/ε^{2−o(1)}. Polynomial regime; irrelevant to exponents.
 * **Giles & Haji-Ali, "Multilevel nested simulation for efficient risk estimation", arXiv:1802.05016v2** [abstract + intro p.1 read]: P[E[X|Y] ≥ 0]; "adaptively selecting the number of samples in the approximation of the inner expectation, as proposed by (Broadie et al., 2011)" — the step function does not change when the inner estimate is far from the threshold. → the algorithmic relative of the two-level algorithm (refine a fibre only as far as its distance to the level requires); mean-square analysis, no worst-case exponent.

### Step 11 (17:59 UTC) — numerics II (own code: exponent_checks.py → exponent_checks.out; 4 s)
- E1: θ_hint(0+) = 0.00767, 0.02914, 0.09728, 0.15614 at u = ½, 1, 2, ln 16; a = KL(p_u‖½) = 0.03030, 0.11094, 0.32781 at u = ½, 1, 2 — agree with every number quoted in the theory report; Λ₁ + ln cosh(u/2) = u/2; a/h → 4.
- E2: S–S–O eq. (43) (bias of the Jarzynski estimator, binomial work, M = 2^{γN}) coincides with KL(ρ_θ‖p_u), KL(ρ_θ‖½) = θ = γ ln 2, to 4e−15 on 1600 parameter pairs; θ_na is its inverse; B_max = ln cosh(u/2); γ_c ln 2 = a; Chatterjee–Diaconis q(u) = a.  ⇒ my translation in Step 9 is correct.
- E3: shear law x_na(θ) = e_hint(θ) + θ to 3e−16 (it IS the identity KL(ρ‖p_u) = KL(ρ‖½) + uρ − Λ₁).
- E4: exact finite-n lower-bound constructions (dips at zero; cone vs flattened cone), log-space binomial sums: exponents 0.0266/0.0196/0.0173/0.0169 → θ_hint = 0.0163 and 0.0465/0.0341/0.0302/0.0293 → θ_na = 0.0283 for n = 200/800/3200/6400.
  **Independent replication of the report's "0.0293 at n = 6400, u = 1, ε₁ = ¼ ln cosh ½, δ = 0.05": mine 0.02933.**
  [Two bugs of mine on the first run, recorded: expm1 overflow for large radii; I took the largest instead of the least R with D_R > ε. Both fixed.]
- E5: simulated plain MC at the cone (Poisson shell counts), M = e^{nθ}: deficit ln(A/Â)/n at n = 500/2000/8000/32000: θ = 0.25a: 0.0392, 0.0335, 0.0314, 0.0309 → 0.0306; θ = 0.5a: 0.0166, 0.0123, 0.0112, 0.0108 → 0.0106; θ = 0.75a: 0.0057, 0.0034, 0.0026, 0.0024 → 0.0022; zero above a.
- E6/E7: one-sample bias = n ln cosh(u/2); mutation of the identity detected.

### Step 12 (18:03 UTC) — published version of the odds-ratio result; capacity reading of the non-adaptive exponent; further searches
 * Downloaded the PUBLISHED Hasenclever–Scholz article (benthamopen.com/DOWNLOAD-PDF/TOSPJ-7-20): The Open Statistics & Probability Journal 7 (2016) 20–35, DOI 10.2174/1876527001607010020 [full text obtained; Prop. 8 located and read at lines 531–548 of the pdftotext output]: "Proposition 8 (Margin weighting function for sMutInf): For all x ∈ R∖{0}: a) sMutInf_x has exactly one maximum at the origin (y, z) = (0, 0)." Same statement as in arXiv v1.
 * S14 WebSearch "Novak Quadrature formulas for monotone functions adaptive Monte Carlo n^{-3/2} …" → secondary snippets (arXiv:1704.08213, 2203.00423): Novak, Proc. AMS 115 (1992) 59–68: univariate monotone functions, adaptive randomized n^{-3/2} vs non-adaptive randomized n^{-1}. [search snippet; paper not opened]
 * S15 WebSearch (extended) "integration w.r.t. unknown non-normalized density lower bound adaptive nonadaptive … log-Lipschitz without log-concavity" → nothing on the setting (general Novak curse-of-dimensionality papers).
 * S16 WebSearch (extended) "adaptive versus non-adaptive query complexity estimating partition function zeroth-order/value queries Lipschitz energy hypercube …" → nothing matching; side hits: Chen–Nannicini 2404.02414; arXiv:2610.06197 (quantum partition functions, adaptive gains n^{1/4} over non-adaptive) [search snippets].
 * S17 WebSearch "rounds of adaptivity mean estimation / sum estimation / approximate counting lower bound hierarchy" → Agarwal–Agarwal–Assadi–Khanna COLT 2017 (coin tossing; log* n rounds necessary and sufficient) [search snippet]; no round hierarchy for sum estimation found.
 * S18 WebSearch "Dagum Karp Luby Ross An optimal algorithm for Monte Carlo estimation …" → FOCS 1995 / SIAM J. Comput. 2000, DOI 10.1137/S0097539797315306; "expected number of experiments … optimal to within a constant factor for every Z" [search snippet; paper not opened].
 * S19 WebSearch "Dzindzalieta Extremal Lipschitz functions …" → arXiv:1205.6300; **read abstract + intro pp.1–2 from the PDF**: sup over 1-Lipschitz f of μ{f − E f ≥ x}; "the sup … is achieved on a family of distance functions"; equivalence with the vertex-isoperimetric problem; cube with Hamming distance among the corollaries. → precedent for the mechanism of the tail lemmas 11.43 (distance functions to Harper sets extremal).
 * Idais & Schwabe, arXiv:2011.09745 [Theorem 2 and the surrounding paragraph read]: "If Φ is invariant (with respect to G) and convex, then there exists an invariant design ξ* … Invariant designs are uniform on orbits … it remains to find the optimal orbits and the [weights]"; refers to Kiefer (1959) JRSS-B 21, 272–304. → the design-of-experiments form of G25's "by symmetry alone".
 **Own computation (capacity_check.py → capacity_check.out, 3 s):**
 - The cone laws {W^n(·|s)} are the output laws of the memoryless channel s_i → x_i, W(x|b) ∝ π(x)e^{-u[x≠b]}.  a(p,u) = max_m I(S;X) (Thm 11.59(c)) = CHANNEL CAPACITY; = information radius min_r max_b D(W_b‖Bern(r)) (verified to 1e−8 on six (p,u)); uniform cube: a = ln 2 − h(p_u) = capacity of BSC(p_u).
 - **Replication of the report's table (u = 2, θ = 0, .5, 1, 2, 3): a = .3278, .3162, .2836, .1841, .0928; plain MC = .3278, .4078, .4621, .4338, .2732 — identical to the printed values** (ratio 2.94 at θ = 3 = the "2.9").
 - NEW REMARK: by capacity = information radius, the best single PRODUCT proposal Bern(r*)^n (r* = capacity-achieving output law: .4308, .3607, .2225, .1124 at θ = .5, 1, 2, 3; r* lies between p and ½) has worst-case KL exponent EXACTLY a. So at vanishing accuracy the lower bound max(φ₀, φ₁) of Thm 11.61 minimised over r equals θ_na(0+): the strict inequality "min_r max(φ₀,φ₁) > θ_na" that the report leaves unproved CANNOT hold at ε₁ → 0+; the 0.5–3 % gaps reported are an effect of extensive accuracy (and shrink as ε₁ → 0: 1.3 % at 0.05E, 2.5 % at 0.25E for (0.1, 2)).  At bounded accuracy "flat histogram, not the Gibbs measure" should read "any proposal whose marginal is the capacity-achieving output law, e.g. the product Bern(r*)^n or the flat histogram; not π".
 - C4: exact finite-n KL(cone_{m*}‖μ_H)/n = 0.1752, 0.1675, 0.1649 (n = 200, 800, 3200) → a = 0.1637 at (0.1, 2): the flat histogram attains a too (it is the universal mixture; the report's remark (3) of §11.20 already identifies μ_H with the Shtarkov NML distribution).

### Step 13 (18:12 UTC) — first full version of A1_REPORT.md written; corrections to my own draft
- Wrote docs/science/workstreams/A1_REPORT.md (§§1–8).
- Own review of the proof in the theory report of Lemma 11.89 (odds_ratio_report_proof_check.py → .out): gradient formula, T<0, kernel inequality with closed form, maximiser location, monotone capacity — all hold numerically. So their proof is consistent; the lemma is simply known.
- arXiv API used to confirm journal refs: S–S–O DOI 10.1103/PhysRevE.85.051108; Palassini–Ritort PRL 107, 060601; KNU Forum Math. Sigma 13 (2025) e152; H–B JMLR 26(249); Dzindzalieta DOI 10.1214/ECP.v18-2814.
- Tried and failed to access: Chernoff 1959 (Project Euclid: empty/JS page via curl and WebFetch); Novak 1996 (ScienceDirect 403); Novak's publication page (404).
- S20–S23 (see report §4.9): no IT source for the capacity phrasing of the lemma; Novak JAT 80 not accessible; capacity = minimax redundancy confirmed in van Erven–Harremoës arXiv:1206.2459 ("a classical result by Gallager and Ryabko") [passage read].
- CORRECTIONS to my first draft: (i) I had written that the report's remark "fixed product measure gives the worse exponents" conflicts with §2.3 — wrong: that remark is about π, not Bern(r*). Fixed. (ii) "strict inequality … false at 0+" → precise version: the two sides coincide in the limit ε₁ → 0+; strictness at positive ε₁ is not excluded. Fixed.

### Step 14 (18:19 UTC) — NEW STATEMENT: Proposition A1.1 (class-wide bounded-accuracy non-adaptive upper bound by the chain rule)
- Idea came from asking whether Bern(r*)^n is class-wide optimal at bounded accuracy (my own next-step 2).
- For π = Bern(p)^n and ANY u-Lipschitz ψ: conditional odds of ν_ψ ∈ (p/q)[e^{-u}, e^{u}] (termwise comparison of the two sums over the remaining coordinates) ⇒ all conditional means in [a0, a1] ⇒ KL(ν_ψ‖Bern(r)^n) ≤ n max(KL(a0‖r), KL(a1‖r)); min over r = capacity a (information radius).
  Upper tail of log-density by Azuma–Hoeffding with increment range ≤ 2u: exp(−s²/(2nu²)).
  Truncation step of Chatterjee–Diaconis (f ≡ 1): E|Â/A − 1| ≤ sqrt(τ/M) + 2ν(ρ > τ).
  ⇒ M = e^{na+t} samples from the product measure Bern(r*)^n: E|Â/A − 1| ≤ e^{-t/4} + 2e^{-t²/(8nu²)} for every ψ ∈ L_u, every n.
- Consequences: (a) Theorem 11.44(ii) without Harper; (b) with a field the bounded-accuracy non-adaptive exponent is exactly a, attained by a product sampler (fills §11.20 remark (4)); (c) a(p,u) ≤ a(½,u) is Lemma 11.89 in capacity form since the cone channel has log odds ratio 2u for every p.
- Checked the theory report and workstream/referee reports (grep "chain rule", "information radius", "capacity-achieving", "Azuma"): the argument is not there.
- Numerics: chain_rule_check.py → chain_rule_check.out: 112 Lipschitz instances on cubes n = 8..14, exact enumeration: all four items hold; mutations detected.
  [Error of mine: first version had a 1.5u-Lipschitz "block-radial" test function; the script's own Lipschitz check flagged it and item (i) failed by 0.24 on it. Fixed.]
- Limitation: does NOT give the extensive-accuracy exponent θ_na(ε₁) (needs lower tail of log-density uniformly; adversarial adapted κ_i; e.g. κ ≡ ½ freezes the walk). Thought about a control/tilting argument (would need: κ ≡ p_u extremal for the lower-tail control problem) — not done; listed as next step.
- Report updated (§2.5 new, §2.3, §2.6, §3, §5, §6, §7, verdict (vi)).

### Step 15 (18:21 UTC) — Novak–Rudolf survey; search for Prop A1.1
- **Novak & Rudolf, "Computation of expectations by Markov chain Monte Carlo methods", arXiv:1311.1899v2** [full text of §3 (unknown densities, Thms 3–5) and §4 (open problems) read]: Thm 4 = Mathé–Novak Thm 1 (lower bound for all randomized algorithms on F_{C,d}); Thm 5: explicit non-asymptotic bound for the lazy Metropolis ball walk on log-concave, α-log-Lipschitz densities on B^d ("polynomially tractable"); open problems: constants, L_p, MCQMC — nothing about dropping log-concavity. → corrected my §8 wording ("leaves open" → "does not reach").
- Rudolf's thesis arXiv:1108.3201 downloaded, not read.
- S24 (extended) for Prop A1.1-like statements → nothing.
- Thought about extending Prop A1.1 to extensive accuracy: reduces to a stochastic control problem for the likelihood-ratio martingale with adapted two-point increments (κ_i ∈ [a0,a1]); constant control (cone) conjecturally extremal; freezing strategies do not improve the exponent in the cases I worked by hand (partial freezing: α x*(θ/α) increasing in α). The adapted relaxation is weaker than the Lipschitz condition (which must hold in every coordinate order), so tightness is unclear. Left as next step 2 in the report.

### Step 16 (18:37 UTC) — replication of the round-hierarchy numbers; report review pass
- rounds_numbers_check.py (3 min): T2(0)/a = 0.6196, 0.6243, 0.6412, 0.6646 at u = .5, 1, 2, 3 (report .620, .624, .641, .665); 0.6181 at u = 0.02 (golden ratio).
  θ2*/a = 0.3493, 0.3592, 0.3924(!), 0.4395 on a φ1-grid of step 0.01 (report .349, .359, .394, .440).
- The 0.3924 vs 0.394 at u = 2 looked like a discrepancy; rounds_refine.py (φ1 step 0.001, running in background): u = 1: 0.35922 at φ1 = 0.640 (constraint θ < φ2 a not binding); **u = 2: 0.39400 at φ1 = 0.606, where the constraint θ < φ2 a IS binding** — my coarse grid missed the kink by 0.002. So the report's 0.394 is right. (u = 3 pending.)
- Report review pass: fixed §-reference (2.6→2.5), a broken table, the Idais–Schwabe quote (now verbatim from the PDF), the Guo et al. sentence, the sign remark on sMutInf for x<0.
- New precise remark for §2.4: in ABSOLUTE error on the section {max w ≤ 1} of the cone there is no adaption gain at all: the section contains every function with values in [e^{-u}, 1] (any such function is u-Lipschitz because distinct points have distance ≥ 1), where mean estimation is Θ(N^{-1/2}) for adaptive and non-adaptive methods, and plain MC achieves N^{-1/2} on the section. So the adaption gain is a relative-error phenomenon.

### Step 17 (18:38 UTC) — what the other documents already say
- grep in theory docs: workstream D of the theory division (docs/workstreams/D_REPORT.md §9) lists "Suárez et al. (2012, 'phase transition in the Jarzynski estimator')" as "[titles and summaries only]" (context G15), with the remark "for a given pair of systems and a given estimator … None is a lower bound over algorithms". They did not notice the coincidence of formulas with θ_na/a/ln cosh; §11.16/G18/L7 do not cite it. Recorded in report §2.2.
- The coordinator has already drawn SCI-REV-0004 (docs/collaboration/messages/science/, 18:19–18:25 UTC) and an entry in SCIENCE_TO_ALL.md from the FIRST complete version of my report. Points there that my later work supersedes:
  (1) "A class-wide upper bound for Bern(r*)^n is not proved" → now proved (Prop A1.1);
  (2) "T4 … decide whether … (missing: a tail lemma …)" → no tail lemma needed at bounded accuracy;
  (3) "it answers … the question Mathé and Novak leave open" → too strong, corrected;
  (4) counts (23 queries / 27 sources / four scripts) → 24 / more / seven.
  I cannot edit those files (outside my write area); added a "changes since the first version" paragraph to the report and will say so in the handback.
- rounds_refine.py finished u = 2 (0.39400 at φ1 = 0.606, constraint binding); u = 3 still running in the background.

### Step 18 (18:45 UTC) — sampling-oracle classics read; FOLLOW-UP FROM THE COORDINATOR RECEIVED
- Read from arXiv PDFs [abstracts]: Štefankovič–Vempala–Vigoda cs/0612058 ("we prove any non-adaptive cooling schedule has length at least O*(ln A), and we present an algorithm to find an adaptive schedule of length O*(√ln A)" — the classical adaptive/non-adaptive separation for partition functions, in the cooling-schedule sense, sampling oracle); Kolmogorov arXiv:1608.04223 (O(q ln n ε^{-2}) calls; lower bound Ω(q ε^{-2})); Harris–Kolmogorov arXiv:2007.10824 (Õ(q/ε²), optimal up to logs); Huber arXiv:1206.2689 (TPA, O(ln Z · ln ln Z)).
- **Coordinator follow-up (mid-task):** theory checkpoint 89ac710 (read-only at scratchpad/thy_ro) has a new §11.26 (heteropolymer product landscapes; "dictionary with channel coding"): Theorem 11.99: F*_j(t) = (1−t)·C_t (Rényi capacity of the "vertex channel" φ ↦ π_φ); E_0(ρ) = ρ Σ_j λ_j C_{1/(1+ρ)}; θ_na = E_sp^{-1}; "a fixed sample of e^{nθ} points certifies E_sp(θ); adaptive/hinted: E_sp(θ) − θ". Request THY-REQ-0011: B1 (is the dictionary known?), B2 ("a site with many equivalent states behaves like one with about e^{u/2} states"; crossings e^u = k(k−1)).
  Task: append "9. Addendum: questions B1, B2 of THY-REQ-0011" to A1_REPORT.md; say how Thm 11.99 relates to my §2.3 / Prop. A1.1; final message ≤ 350 words; depth on B1.
- Read in thy_ro: THEORY_REPORT.md lines 6138–6420 (§11.26 in full) and THY-REQ-0011.md in full.
- My first analysis before searching (to be checked against sources):
  (H1) For one target ν and one sampling law μ (products), "the mass a sample of e^{nθ} points can see" is the Neyman–Pearson problem max{ν(S): μ(S) ≤ e^{-nθ}} → Hoeffding's error-exponent trade-off min{D(V‖ν): D(V‖μ) ≤ θ}; Chatterjee–Diaconis' threshold e^{KL(ν‖μ)} is the Chernoff–Stein-lemma end of that curve. Minimising over μ and maximising over a family of targets gives the Rényi radius → E_sp (Csiszár 1995; Shannon–Gallager–Berlekamp's proof of the sphere-packing bound IS this hypothesis-testing argument with an auxiliary output law).
  (H2) "adaptivity gains exactly the rate" = the textbook relation between the two error exponents of a likelihood-ratio test (they differ by the log-threshold); cf. Forney's erasure/list exponents E_2 = E_1 + T.
  (H3) The game "sampler picks Q, adversary picks a law M on inputs" with payoff (1−t)D_t is composite hypothesis testing against product laws: Sibson's α-mutual information (Tomamichel–Hayashi 2018).
  (H4) At the estimator level: freezing of exponential averages = truncated Legendre transform (Rohwer–Angeletti–Touchette 2015 in general; S–S–O 2012 binomial); REM ↔ random codes (Merhav 2009; Mézard–Montanari).
  (H5) Hitting/guessing: optimal random-guessing law ∝ P^{1/(1+ρ)} (Arikan 1996; Merhav–Cohen 2019) ↔ "Rényi centre is the hardest instance / best sampler".
  Sources to open: Nakiboğlu 1608.02424, 1611.06924; Tomamichel–Hayashi 1511.04874; Merhav 0708.0850; Rohwer et al. 1409.8531; Merhav–Cohen 1811.04363; Palaiyanur–Sahai cs/0610139; Sanz-Alonso 1608.08814; Masrani et al. 2107.00745.

### Step 19 (18:52 UTC) — B1: sources read (full text of the stated parts, from arXiv PDFs)
 * **Merhav, "Relations between random coding exponents and the statistical physics of random codes", arXiv:0708.0850 (IEEE-IT 55 (2009))** [abstract, §1, §2.2.1–2.2.2 read]: Z(β|y) = Σ_{x∈C} P^β(y|x) over a random code of e^{nR} words is a REM (after Mézard–Montanari, ch. 6); BSC: N_y(δn) ≐ e^{n[R − ln2 + h(δ)]}, distances below δ_GV(R) unpopulated, Z_e ≐ (1−p)^{βn}e^{n(R−ln2)} exp(n max_{δ∈[δ_GV,1−δ_GV]}[h(δ) − βBδ]); glassy phase for p_β ≤ δ_GV(R) with F_g = δ_GV ln(1/p) + (1−δ_GV)ln(1/(1−p)); general DMC eq. (10): only conditional types with H_Q(X|Y) ≥ ln|X| − R are populated.
   → with β = 1, B = u (p = p_u), codewords = uniform sample points, y = centre: Z_e/(M(1−p)^n) IS the plain-MC estimate at the cone; F_g − (ln2 − R) = D(δ_GV(R)‖p) = E_sp(R) of the BSC. So the "populated types ⇔ I ≤ R" mechanism of Theorem 11.99's last paragraph is Merhav's eq. (10). The paper relates the glassy free energy to the correct-decoding exponent and the paramagnetic one to Gallager's exponent; it does not name E_sp for this quantity (grep "sphere": one unrelated hit).
 * **Nakiboğlu, "The Rényi capacity and center", arXiv:1608.02424v8; "The sphere packing bound via Augustin's method", arXiv:1611.06924v8** [abstracts; Definition 13 and Lemma 13 of the second read]: "E_sp(R,W) ≜ sup_{α∈(0,1)} ((1−α)/α)(C_{α,W} − R)"; unique Rényi centre; "The reliability function of the discrete stationary product channels with feedback is bounded from above by the sphere packing exponent".
 * **Tomamichel & Hayashi, arXiv:1511.04874v3 (IEEE-IT 2018)** [abstract, §I incl. eqs. (2)–(6), eqs. (51)–(55) read]: Hoeffding's bound: if β_n ≤ e^{-nR}, R < D(P‖Q): −log α_n = n sup_{0<s<1} ((1−s)/s)(D_s(P‖Q) − R); composite alternative "X^n ~ P_X^{×n} independent of Y^n": Sibson's I_s^{↑↓}(X:Y) = min_{Q_Y} D_s(P_XY‖P_X×Q_Y) = (s/(s−1))·E_0((1−s)/s, P_X)-form with "E_0 … Gallager's error exponent function"; optimal error exponent sup_{s∈(0,1)} ((1−s)/s)(I_s^{↑↓} − R).
   → THIS is the information-theoretic statement behind "a fixed sample of e^{nθ} points certifies E_sp(θ)": type-II error e^{-nθ} = sampler-measure of the set that must be hit; type-I exponent = Gibbs mass outside it; alternative = any product sampling law (min over Q).
 * **Rohwer, Angeletti, Touchette, arXiv:1409.8531v3 (PRE 92, 052104)** [abstract, §II.B, §IV.B read]: "linearization effect" of estimators of generating functions; "sheds light on previous reports of 'phase transitions' in the statistics of free energy estimators"; M must grow exponentially with n.
 * **Yunger Halpern & Jarzynski, arXiv:1601.02637v2 (PRE 93, 052144)** [abstract]: "We bound the number of trials one should expect to perform, using the order-∞ Rényi entropy", with a tolerance parameter for "dominance".
 * **Merhav & Cohen, arXiv:1811.04363** [abstract, intro, line with Arikan's formula]: randomized (i.i.d.) guessing with a universal distribution attains the guessing exponent; Arikan: E(ρ) = max_Q[ρH_Q − D(Q‖P)] = ρH_{1/(1+ρ)}.
 * **Merhav, arXiv:0711.2501** [abstract, lines 86, 315]: Forney's erasure/list exponents: "E_2(R,T) = E_1(R,T) + T".
 * **Yagli & Cuff, arXiv:1801.00714v8** [abstract, p.1]: soft-covering lemma (R > I(P_X,P_{Y|X})), exact exponents under TV.  **He, Pradhan, Winter, arXiv:2409.18307v4** [abstract, p.1]: exact strong converse exponent of soft covering at rates BELOW mutual information — "a new two-parameter information quantity, differing from the … Rényi mutual information"; random coding not tight.
 * Sanz-Alonso arXiv:1608.08814 [abstract]: necessary sample size for IS via f-divergences (KL, χ²). Sahai cs/0610139 [abstract]: E_sp remains valid with feedback for symmetric channels (fixed block length). Masrani et al. 2107.00745 [abstract]: q-paths; intermediate densities minimise a mixture of α-divergences to the endpoints.
 Searches: S26 (extended) IS + sphere packing/Hoeffding/Neyman–Pearson/Rényi → nothing with E_sp or Hoeffding for IS (hits: Sanz-Alonso; arXiv:2312.15256 App. A "cost ≈ exp(relative entropy)"). S27 REM + random code + sphere packing (Mézard–Montanari ch. 6) → Merhav's papers. S28 Csiszár 1995 abstract (snippet: β-cutoff rates, α = (1−β)^{-1}). S29 Forney E_2 = E_1 + T → Merhav 0711.2501. S30 number of mass points → Dytso–Yagli–Poor–Shamai 1901.03264 [abstract read: O(A²) upper bound]. S31 (extended) optimal alphabet size symmetric channel/PPM → nothing exact. S32 optimal PPM order → Jarzyna et al. arXiv:1709.00030 (snippet). S33 sphere packing + soft covering below MI → He–Pradhan–Winter.
 My own derivations for the addendum (to verify numerically next):
  (D1) The window of site laws P(L_j) = {π_γ: γ ∈ L_j} = {p: π(a)p(b) ≤ e^{d(a,b)}π(b)p(a)} is a convex POLYTOPE whose vertices are the vertex laws π_φ ⇒ Prop. A1.1 generalises verbatim to §11.26: every conditional law of ν_ψ lies in the window (L_j closed under soft minima), so KL(ν_ψ‖⊗Q*_{τ(i)}) ≤ n Σ_j λ_j a_j with Q*_j the capacity-achieving output law (Rényi centre of order 1) of the vertex channel.
  (D2) B2: at L = e^u the cutoff rate R_0 = C_{1/2} of the k-ary symmetric channel with pairwise likelihood ratio L is maximal at k = √L + 1, and R_0(k) = R_0(k+1) exactly at L = k(k−1); conjecture F*_k(t) = F*_{k+1}(1−t) there.

### Step 20 (18:59 UTC) — addendum written (report §9) and checked
- addendum_checks.py → addendum_checks.out (8 s, all PASS on the first run; one check Q2d added afterwards):
  Q1 cube dictionary from textbook formulas to 1e−12 (F*_c = (1−t)C_t(BSC); E_sp = sup_a((1−a)/a)(C_a − θ) = KL(ρ_θ‖p_u) = Merhav's F_g − (ln 2 − R); E_sp − θ = uρ_θ − Λ₁).
  Q2 (B2): F*_k = (1−t)C_t of the k-ary symmetric channel with p_k = L/(L+k−1), L = e^u; **cutoff rate R_0(k) maximal at k = √L + 1**; **reflection identity F*_k(t) = F*_{k+1}(1−t) at L = k(k−1)** (4e−16; proof: L+k−1 = (k−1)(k+1), L+k = k², (L^{1−t}+k)/(L^t+k−1) = k^{1−t}/(k−1)^t); integer maximiser of R_0 and of h is the k with (k−1)(k−2) < L < k(k−1) (k ≤ 12); Shannon capacity optimum k* = (L−1)²/(L ln L − L + 1) ≈ e^u/u (different law); a₂ = a₃ at u = 0.51937 (report 0.5194); report's h_2,h_3,h_4 at u = 0.5, 1 reproduced to 6 digits.
  Q3 (Prop. A1.2): window polytope W_j = {p: π(a)p(b) ≤ e^{d(a,b)}π(b)p(a)} = conv(vertex laws); conditional laws of ν_ψ in the window (5e−15) on 36 heteropolymer instances; KL(ν_ψ‖⊗Q*) ≤ Σ a_{τ(i)} with equality for additive vertex instances; mutation detected.
- Further sources read for the addendum: van Erven–Harremoës Theorem 11 and Theorems 33–34 passage [full text of passages]; Forney's MIT notes "On exponential error bounds for random codes on the BSC" §1 [full text]: E_sp(R) = D(δ_GV(R)‖p), D(δ_GV(R)‖½) = R; Dytso–Yagli–Poor–Shamai abstract (O(A²) mass points).
- Searches S34 (cutoff rate optimal alphabet size) → only the M-ary erasure example via Arıkan cs/0508034 (snippet); S35 (extended; sums of random exponentials + Rényi/sphere packing/Hoeffding) → nothing on sampling.
- Answer to B1 in one line: formulas and mechanism known under three names (random-code REM; Jarzynski bias; Hoeffding trade-off against product laws with Gallager's E_0), lower bound = sphere-packing argument; NOT found: the complexity statement, and in particular that an adaptive algorithm attains E_sp(θ) − θ (in coding, feedback does not beat E_sp).
- Answer to B2: exact counterpart = alphabet size maximising the cutoff rate; reflection identity explains the crossings; genre classical (R_0 design criterion; finite-support capacity-achieving inputs; PPM order), exact rule not found.
- Relation to my §2.3 / Prop. A1.1: §2.3 = special case (t ↑ 1, two letters) of their Thm 11.99; Prop. A1.1 is an addition and generalises (Prop. A1.2) to all of §11.26, supplying its missing bounded-accuracy upper bound for non-adaptive algorithms with a product sampler.
- Corrections to my own addendum draft before finalising: removed quotation marks around a search-engine paraphrase; "twenty years earlier" → "since 2007–2009"; made explicit that the bounded-accuracy LOWER bound a is taken from the theory report.
