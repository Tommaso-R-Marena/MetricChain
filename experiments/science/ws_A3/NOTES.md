# Workstream A3 — NOTES (prior art: certifying a free energy by sampling from a model)

Started 2026-11-25 23:33 UTC.  Rules read: `docs/science/workstreams/COMMON.md`, `A3_brief.md`.
Write-scope: this directory and `docs/science/workstreams/A3_REPORT.md` only.  No state-changing git.

Reading-level tags used everywhere: `[full text]`, `[abstract]`, `[search snippet]`,
`[from memory — unverified]`.

## Log (chronological)

*Times are UTC from the machine clock (`date -u`); a first version of this log carried guessed
times that ran ahead of the clock — corrected at 23:50 on 2026-11-25.*

### 23:33 — setup
* Created `experiments/science/ws_A3/`, this file.
* Next: read A1/A2 reports (classification scheme, search logs), THY-RES-0007, the theory
  RESEARCH_LOG "Resume here (cycle 10, fourteenth checkpoint)" item 1, addendum A17 (if present),
  P2 report §4, INFERENCE_LIMITS §7.

### step 1 (23:33–23:38) — internal reading (no web yet)
Read: `A1_REPORT.md` §1, §4.1–4.2, §4.7–4.10 (scheme, search log, sources table); `A2_REPORT.md` §1 and
table; theory export `thy_ro_658b77f`: `THY-RES-0007.md` (whole; §4.2 = the announcement, §6.1 = the
request), `docs/RESEARCH_LOG.md` "Resume here (cycle 10, fourteenth checkpoint)" item 1 (statements
(a)–(e)), `docs/prior_art/L7_query_complexity.md` (whole); ours: `INFERENCE_LIMITS.md` Theorem 7,
`INFERENCE_LIMITS_ADDENDA.md` A5 (sharp form `KL ≤ w²/8`), `SCI-MSG-0003`, `P2_REPORT.md` §4.
* Addendum **A17 is not in `INFERENCE_LIMITS_ADDENDA.md`** at ≈23:36 (last addendum is A16) → O1, O2 taken from
  the brief.  (Re-check later.)
* The theory division's own L7 already attributes its *general* randomised lower bound (Thm 11.22(b,c):
  fractional packing of sensitive blocks) to fractional block sensitivity / randomised certificate
  complexity (Aaronson; Tal; Gilmer–Saks–Srinivasan; Kulkarni–Tal) at "search summaries" level, and lists
  DKLR at "search summaries only", Chatterjee–Diaconis from memory.  So for T3 the *method* attribution
  exists; my job is full text + the statement-level comparison.
* Earlier workstreams downloaded PDFs with `curl` through the proxy and read `pdftotext` output; A1 has
  Chatterjee–Diaconis (`a1_dl/is/cd.txt`) and Mathé–Novak in the scratchpad — I will re-read them myself
  where I cite them.

### step 2 (≈23:38) — first mathematical observations (before any search; to be verified numerically and in sources)
(M1) **T1's constant is Specht's ratio.**  With `h = e^w`: `ln S(h)`, `S(h) = (h−1)h^{1/(h−1)}/(e ln h)`, equals
  `ln(e^w−1) + w/(e^w−1) − 1 − ln w = L(w)`.  Specht's theorem (1960) is the sharp reverse AM–GM
  inequality `A ≤ S(M/m)·G` for numbers in `[m, M]`; with weights and `x = e^{−r}` this *is* the upper half of
  T1.  → verify the formula of `S` in a source I can open; look for the weighted/probabilistic form; look for
  the same statement in statistical-mechanics clothing.   [from memory — unverified at this point]
(M2) **T1 in divergence language**: `ln Z(g) − ln Z(ĝ) + E_π r = KL(π‖μ_g)`; so T1 says
  `0 ≤ KL(π‖μ_g) ≤ L(osc r)`; by symmetry also `KL(μ_g‖π) ≤ L(w)`, which sharpens our own A5 (`w²/8`).
(M3) **T3 vs DKLR**: with `X = e^{−(r−lo)} ∈ (0,1]` under the floor measure `π_lo ∝ w e^{−lo}`, `E X = μ' = Z(r)/Z(lo)`;
  T3's cost `(Z(lo)/Z(r) − 1)/ε = (1−μ')/(εμ')`.  DKLR (from memory): `Θ(max(σ²/(εμ)², 1/(εμ))·ln(1/δ))`.
  The worst-case variance term over `[0,1]` laws with mean `μ'` is `(1−μ')/(ε²μ')` (Bernoulli) — the zero-one
  estimator theorem.  So "hinted" = the `1/(εμ)` term *with the factor (1−μ)*, "unhinted sampling" = the
  Bernoulli variance term; they differ by `1/ε`.  Model differences to check in the full text: DKLR's
  algorithm sees only i.i.d. samples of `X` (no hint, no choice of query point).
(M4) **T4's asymmetry** looks like the classical one-sidedness for means of non-negative variables
  (Bahadur–Savage 1956; lower confidence bounds exist, upper ones need a bound on the support) and, for
  importance weights, "high-confidence *lower* bounds" in off-policy evaluation.  To check in sources.
(M5) **O1**: `(B/μ)^p = e^{(p−1)D_p}`.  For `1<p≤2` the cost equals the minimax rate of heavy-tailed mean
  estimation read backwards; for `p>2` estimation saturates at the variance rate but the *hinted* cost
  keeps improving — that would be the part not in the mean-estimation literature.  Yunger Halpern &
  Jarzynski (2016, "Number of trials required to estimate a free-energy difference…") use the order-∞
  Rényi divergence for the number of trials [from memory — unverified] → must read.
(M6) **O2 can apparently be sharpened by a factor 2**: conditionals of `μ_g` under a product `π` are one-site
  tilts of oscillation `≤ c_i`; a tilt of oscillation `w` has `D_α ≤ αw²/8` (Taylor: `Λ'' ≤ w²/4`); Rényi
  divergences compose additively over worst-case conditionals ⇒ `D_α(μ_g‖π) ≤ (α/8)Σc_i²`, i.e.
  `D_2 ≤ Σc_i²/4` (O2 has `/2`).  This is the composition theorem of concentrated differential privacy
  (Bun–Steinke 2016: ε-DP ⇒ `D_α ≤ αε²/2`; composition) in other clothes [from memory — unverified].
  → numerics first (`check_o2.py`), then read Bun–Steinke.

### step 3 (≈23:39–23:43) — access to Dagum–Karp–Luby–Ross (DKLR)
Search log entries (tool `WebSearch`; S = standard, X = extended):
1. S `Dagum Karp Luby Ross "An optimal algorithm for Monte Carlo estimation" pdf` → bibliographic records only
   (DOI 10.1137/S0097539797315306, SIAM J. Comput., pp. 1484–1496 per the snippet); side hit: KLM.pdf on a CMU
   course page (Karp–Luby–Madras 1989) — **downloaded, PDF, 20 pp.** (`a3_txt/klm.txt`).
2. S `"optimal algorithm for Monte Carlo estimation" … "stopping rule theorem" "generalized zero-one estimator theorem" technical report`
   → arXiv:1302.3598 (Pradhan–Dagum, restates the theorems), arXiv:0711.2801 (X. Chen: says the proof of the
   DKLR stopping rule "is not complete"), arXiv:2210.12861 (Huber).
3. X `… "AA" "(ε, δ)-approximation" "ρ_Z" "max{σ_Z^2, εμ_Z}" lower bound theorem universal constant` → ACM/ResearchGate
   records; volume/issue 29(5) per the snippet.
4. S `… filetype:pdf "Stopping Rule Algorithm" "Υ" "4 λ ln(2/δ)/ε^2"` → nothing new.
5. X `"Lower Bound Theorem" "Let BB be any algorithm" …` → arXiv:1308.1562, 1309.5413 (Huber) as secondary sources.
Direct attempts: `epubs.siam.org/doi/pdf/…` → Cloudflare challenge page (curl) / HTTP 403 (`WebFetch`);
Semantic Scholar API: `openAccessPdf.status = CLOSED`; Unpaywall: `is_oa = false`, no repository copy;
CiteSeerX → redirect to `web.archive.org`, connection reset by the proxy (archive.org not reachable from here);
`icsi.berkeley.edu/ftp/…/tr-95-014.pdf` (a guess) → "Page not found"; ResearchGate → HTML.
**DKLR original: NOT ACCESSED so far.**  Plan: read the statements as quoted in papers I can open in full
(Pradhan–Dagum 1302.3598; Huber 2210.12861; Mnih–Szepesvári–Audibert 2008; Kunsch–Novak–Rudolf 1805.08637;
Gajek–Niemiro–Pokarowski) and say so.
Project Euclid (Bahadur–Savage 1956) → Incapsula page with curl (not a PDF).

### step 4 (≈23:44) — coordinator's addition to the brief (received mid-task); A17 now present
* `INFERENCE_LIMITS_ADDENDA.md` §A17 is now in the tree (read in full, lines 1021–1265).  **Authoritative
  statements of O1–O2 are A17.1–A17.6**: A17.1 detection lemma (Hölder: `π(D) ≥ (|μ−μ′|/B)^{p/(p−1)}`),
  A17.2 hinted cost `Θ(e^κ/ε^{p/(p−1)})`, A17.3 without a hint (`p ≥ 2`: Chebyshev bracket `μ̂ ± B/√(Nδ)`
  valid for every member; `1<p<2`: median of means; lower bound a sketch), A17.4 KL ball: cost `exp(Θ(κ/ε))`,
  A17.5 polynomial moments of `r` do not suffice, A17.6 `D_p ≤ p²K/(8(p−1))`, `K = Σc_i²` (so `D_2 ≤ K/2`),
  with the remark that the additive cube instance has `D_2 ≈ K/4`.
* Three extra leads to follow (all unverified memory of the coordinator): (1) CUBO (Dieng et al.) and Rényi
  VI (Li–Turner): is `ln Z ≤ (1/p) ln E(weight^p)` + "χ² controls weight variance" stated, with any
  certificate?  (2) flow-annealed importance sampling bootstrap (Midgley et al.): what is claimed about
  ESS versus the α=2 divergence?  (3) one citable statement of mode-seeking vs mass-covering.
* New observations triggered by A17 (to verify):
  (M7) my (M6) improves A17.6 from `p²K/(8(p−1))` to `pK/8` for every `p > 1` (ratio `p/(p−1)`: 2 at `p=2`,
       unbounded as `p → 1`, where it recovers `KL ≤ K/8`); the additive cube instance is then asymptotically
       extremal.  Numerics first.
  (M8) `L(w) = a − 1 − ln a` with `a = w/(1 − e^{−w})`.  I recall this very expression as the bound on the
       expected privacy loss (a KL divergence between two exponential-mechanism = Gibbs measures) of an
       "ε-bounded-range" mechanism in the differential-privacy literature (Durfee–Rogers; Dong–Durfee–Rogers
       2020), and "ε-bounded range ⇒ ε²/8-zCDP" (Cesar–Rogers 2021) as the tilt lemma `D_α ≤ αw²/8`
       [from memory — unverified] → read arXiv versions.
  (M9) Block–Polyanskiy (2023), sample complexity of approximate rejection sampling over the class of pairs
       with `D_f(ν‖μ) ≤ D`: TV `≈ D/f′(n)` [from memory — unverified] — would be the closest in-print analogue
       of the *family* (A17.2 + A17.4): `f = x^p` gives `n ≈ e^{D_p}ε^{−1/(p−1)}`, `f = x ln x` gives `e^{D/ε}`.

### step 5 (≈23:45–23:50) — numerics for my own observations (`check_math.py`, output `check_math.out`, 20 s)
* C1: `L(w) = ln S(e^w)` (Specht) `= a − 1 − ln a`, `a = w/(1−e^{−w})` `= max_t[ln(1−t+te^w) − tw]` — four forms agree to
  `1.3·10⁻⁹` (the last is a grid maximum) on `w ∈ [0.01, 30]`; `ln cosh(w/2) ≤ L(w) ≤ w²/8`; `L(w) = w − 1 − ln w + o(1)`.
* C2/C3: 40 000 random laws: `ln E e^Y − E Y ≤ L(w)`; both `KL(tilt‖base)` and `KL(base‖tilt)` `≤ L(w)`, attained.
* C4 (tilt lemma): 60 000 random tilts, largest `D_α/(αw²/8) = 0.9994`.
* C5 (product reference): 1 200 random members (additive, inf-convolution, hockey-stick, distance functions;
  `{0,1}^n`, `n ≤ 8`; `{0,1,2}^n`, `n ≤ 5`; random product measures): largest `D_p/(pK/8)` = 0.989 (p=1), 0.976 (p=2),
  0.947 (p=6); against A17.6's `p²K/(8(p−1))` the largest ratios are 0.0098 (p=1.01), 0.488 (p=2), 0.79 (p=6).
  Hill-climb with rescaling moves: ratio → 0.99995 from below, never above.
  **Lesson recorded:** the first hill-climb "found" ratios up to 1.16 — rounding noise at `K ~ 10⁻¹³`
  (`D_p` is a difference of nearly equal numbers); confirmed by 60-digit arithmetic (exact ratio 0.99999…);
  the script now refuses `K < 10⁻³` and re-evaluates the best point with 50 digits.
* C6: T3's `(1/m − 1)/ε` is exactly `ε` × the largest variance term `(1−m)/(ε²m)` of a `[0,1]` variable of mean `m`.
→ (M1), (M2), (M6)/(M7) survive numerics.  Proof of (M7) is three lines (written in the report §2).

### step 6 (23:51–23:57) — arXiv id look-ups, first batch of downloads, first readings
arXiv API (`arxiv_batch.py`, title queries; all ids verified by the returned titles): cond-mat/0603185 (Jarzynski
2006), 1601.02637 (Yunger Halpern–Jarzynski), 1511.01437 (Chatterjee–Diaconis), 1511.06196 (Agapiou et al.),
1209.1727 (Bubeck–Cesa-Bianchi–Lugosi), 1509.05845 (Devroye–Lerasle–Lugosi–Oliveira), 2302.04658
(Block–Polyanskiy), 1605.02065 (Bun–Steinke), 1909.13830 (Dong–Durfee–Rogers), 2004.07223 (Cesar–Rogers),
1611.00328 (Dieng et al., CUBO), 1602.02311 (Li–Turner), 2208.01893 (Midgley et al., FAB), 1511.02543 (Grosse–
Ghahramani–Adams), 1805.08637 (Kunsch–Novak–Rudolf), 0904.0625 and 0910.2858 (Hahn–Then), physics/0208015 and
physics/0201046 (Zuckerman–Woolf), 1505.06217 (Yunger Halpern–Garner–Dahlsten–Vedral), 1508.00335 (Sason–Verdú),
1805.05135 (Binette), 1004.0581 (Furuichi), quant-ph/0210020 (Aaronson), 2003.10374 (Naesseth–Lindsten–Blei),
1906.04280 (Lugosi–Mendelson), quant-ph/0105114 (Heinrich–Novak), 1302.3598 (Pradhan–Dagum), 2210.12861 (Huber),
0711.2801 (X. Chen).  No arXiv hit by title: Liu–Fisher–Ihler "Probabilistic variational bounds…", Lou–Dechter–Ihler
"Dynamic importance sampling…", Goldwasser et al., Metelli et al. "Subgaussian and differentiable importance
sampling…", Gajek–Niemiro–Pokarowski (to look for elsewhere).  All 29 PDFs downloaded and converted.
Also: Mnih–Szepesvári–Audibert, ICML 2008, from icml.cc (PDF, 8 pp.).

**DKLR — more access attempts, all failed:** academia.edu (403), OpenAlex (closed; lists a CiteSeerX record whose
source was `icsi.berkeley.edu/~luby/PAPERS/optspeedup.ps`), that URL (404/403), CiteSeerX legacy link (redirects to
archive.org → reset).  **Conclusion: the original is not accessible from this machine.**  What I could read
*about* it in full text:
* X. Chen, arXiv:0711.2801, pp. 2, 5 and Appendix D `[full text]` — reproduces, with page references to the SIAM
  paper (pp. 1486, 1489, 1490–1491), the Stopping Rule Algorithm (sample until the sum reaches
  `Υ₁ = 1 + 4(e−2)(1+ε)ln(2/δ)/ε²`, output `Υ₁/N`), the "Stopping Rule Theorem" (`Pr{|μ̂ − μ| ≤ εμ} ≥ 1 − δ`), and
  Lemma 4.6 with `λ = e − 2`, `ρ_Z = max{σ_Z², εμ_Z}`.  **Chen states that DKLR's proof of the second tail is
  incomplete** ("There exists a significant gap which cannot be patched by using their argument") while the
  claim itself is true (it follows from Chen's sharper threshold).
* Mnih, Szepesvári, Audibert, ICML 2008, §3 `[full text]` — AA is a three-step procedure; "T ≤ C·max(σ², εμ)·
  (1/(ε²μ²))·log(2/δ)" for AA and "if T is the number of samples taken by any (ε, δ)-stopping rule, then there
  exists a constant C′ such that with probability at least 1 − δ, T ≥ C′·max(σ², εμ)·(1/(ε²μ²))·log(2/δ)".
  (They phrase both with probability `1 − δ`; my memory of the original is "in expectation" — cannot check.)
* Kunsch–Novak–Rudolf, arXiv:1805.08637v2, "Historical remarks" `[full text]` — DKLR, Gajek–Niemiro–Pokarowski and
  Huber "study the complexity of approximating the expected value E Y > 0 of a random variable 0 ≤ Y ≤ 1 to within
  a prescribed relative error … the cost is roughly inversely proportional to the target value E Y".
* Pradhan–Dagum, arXiv:1302.3598 `[full text, scanned/OCR]` — restates stopping rule and AA "without proof"; no
  lower bound.

**Kunsch–Novak–Rudolf (arXiv:1805.08637v2) — much closer to A17.3 than expected.** `[full text: abstract, §1,
Thm 3.9, Thm 3.10 with proofs, Remark 3.11, §3.4 to Prop. 3.13, Cor. 3.14]`
* classes: cones `Y_{p,q,K} = {‖Y−EY‖_q ≤ K‖Y−EY‖_p}`, intersected with balls of the *central* `L_q̃` norm,
  `q̃ = min(q,2)`; absolute error ε, confidence 1−δ.
* upper bound (their (5), Thm 2.17): expected cost `≤ C_q K^{pq/(q−p)} (1 + (‖Y−EY‖₁/ε)^{max{1+1/(q−1), 2}}) log δ⁻¹`.
* lower bounds: Thm 3.9 (`q ≥ 2`): `n̄^wor ≥ (4 log 3)⁻¹ (σ/ε)² log(3/(4δ))`; Thm 3.10 (`1 < q ≤ 2`):
  `n̄^wor ≥ c_{q,K} (τ/ε)^{1+1/(q−1)} log(3/(4δ))`; **Cor. 3.14: the same lower bounds for general randomised
  algorithms using function values** (when π has no atoms; Prop. 3.13: "no general randomized algorithm is better
  than the best possible i.i.d.-based algorithm in distinguishing F(1) from F(2)").
* ⇒ A17.3 ("without a hint: `Θ(e^κ/ε^{max(2, p/(p−1))})`; variance term needed") is, in absolute error and with
  central norms, **in print** (their q = our p).  Not there: the hint (verification), relative error/
  divergence form, atoms.

**Yunger Halpern–Jarzynski, arXiv:1601.02637v2 (PRE 93, 052144 per the arXiv record)** `[full text: abstract, all of
the main text up to Theorem 2]`.  My memory was imprecise: it is the order-∞ Rényi **entropy of the work
distribution**, `H^β_∞(P) = −log(p_max/β)`, not a divergence between ensembles.  Theorem 1: the expected number of
reverse trials before one outputs a `w^δ`-dominant work value satisfies `N_δ ≥ exp(β(w^δ − ΔF) + H^β_∞(P_fwd))`
(a waiting-time bound; the tolerance `w^δ` is chosen by the user).  Theorem 2 is an "approximate error bound"
under the neglected-tail assumption.  They call Jarzynski's `N ∼ e^{β(⟨W⟩−ΔF)}` "a rough estimate" and say the
question how large W must be to count as dominant "remained open".  No class, no certificate, no minimax.

**Jarzynski, arXiv:cond-mat/0603185v1** `[full text: abstract, intro, §III, §IV, start of §V]`.  §III: "a back-of-
the-envelope estimate": `N_c^F ∼ exp(βW̄_d^R)`, `N_c^R ∼ exp(βW̄_d^F)` (34a,b); (40): `D[P^F|P^R] = βW̄_d^F`; "Eq. 40
suggests that there might be a natural information-theoretic interpretation of Eq. 34."  §IV (free-energy
perturbation): "Lower bounds N_c^A and N_c^B on the required numbers of realizations are given by analogues of
Eq. 34: ln N_c^A ∼ βW̄_d^B = D[p_B|p_A] ≥ 0; ln N_c^B ∼ βW̄_d^A = D[p_A|p_B] ≥ 0" (45a,b) — i.e. sampling the
reference A costs `exp(KL(target‖reference))`: **the direction of A17's table, stated as an estimate ("∼"), in
2006**; "Of the two perturbations, the one with larger W_d requires fewer samples"; insertion vs deletion
explained by it.  Status in the paper's own words: "heuristic insights and quantitative estimates".

### step 7 (23:57–00:00, into 26 Nov) — Block–Polyanskiy; Chatterjee–Diaconis; the differential-privacy sources; Specht
**Block & Polyanskiy, arXiv:2302.04658v3** `[full text: abstract, §1 (first two pages), §2, §3 incl. Thms 3, 5, 6,
Prop. 4 and proof sketches; App. B to Cor. 17; Lemma 27]`.
* Problem: `n` i.i.d. samples from `μ`; output one of them so that its law is within TV `ε` of `ν`; class = all pairs
  with `D_f(ν‖μ) ≤ D`.  Thm 3 (upper): `n ≥ (2/(1−ε)) log(2/ε)·(f′)⁻¹(4D_f/ε) ∨ 2` suffices.  Example 6: KL →
  `Õ(exp(D_KL(ν‖μ)/ε))`.  Example 7: Rényi-λ (`f = x^λ − λx + λ − 1`, `D_f = e^{(λ−1)D_λ}`) → `Õ(e^{D_λ}ε^{−1/(λ−1)})`;
  `λ = 2`: `Õ(χ²/ε)`; `λ → ∞` recovers plain rejection sampling.  Thm 5 (lower): for `ε ≤ 1/4`, `δ > 2f(1/2)` there is a
  pair with `D_f ≤ δ` needing `n ≥ ½(f′)⁻¹(δ/(2ε))`; proof with `μ = Ber(ε/n)`, `ν = Ber(2ε)` and the `E_γ`
  divergence.  Prop. 4: if `f′` is bounded (e.g. TV) no `n` works.  Lemma 27: `ν(dν/dμ > M) ≤ 2D_f/f′(M/2)`.
* **Comparison with A17.2/A17.4 (mine):** same classes (pairs with a bounded `f`-divergence of the target from
  the sampled measure), same extremal two-point pairs (a set of base mass `q` carrying target mass `≈ ε`), same
  tail lemma (their Lemma 27 ↔ A17.1 by Hölder).  With `q·(ε/q)^p ≈ e^{(p−1)D_p}`: `1/q = e^{D_p}ε^{−p/(p−1)}` = A17.2's
  cost (one must *hit* the set to detect it), and `ε/q = e^{D_p}ε^{−1/(p−1)}` = their cost (the output must land in
  it with probability `≈ ε`).  So the two results differ by exactly the factor `1/ε` (task: detect vs select);
  for KL both are `exp(Θ(D/ε))`.  Not a corollary either way that I can see, but the family is in print for a
  neighbouring task.
**Chatterjee & Diaconis, arXiv:1511.01437v3** `[full text: §1 to Thm 1.2 statement; Thm 2.1 and its discussion]`
(A1's copy of the PDF, re-read by me).  Thm 1.1 verbatim: with `L = D(ν‖μ)`, if `n = exp(L+t)`:
`E|I_n(f) − I(f)| ≤ ‖f‖_{L²(ν)}(e^{−t/4} + 2√(P(log ρ(Y) > L + t/2)))`; if `n = exp(L−t)`:
`P(I_n(1) ≥ 1−δ) ≤ e^{−t/2} + P(log ρ(Y) ≤ L − t/2)/(1−δ)`.  One instance, typical case; needs concentration of
`log ρ`.  **Thm 2.1 (new to our discussion):** for every `ε` there is `n ≤ ε⁻²2^{1+ε⁻³}` such that for *any* `μ, ν`
and `‖f‖_{L²(ν)} ≤ 1` the empirical-variance diagnostic satisfies `P(v_n(f) < ε) ≥ 1 − 4ε` — "using v_n(f) for
testing convergence of importance sampling is fundamentally flawed".  This is the published theorem behind
the theory division's "documented refutation (mean plus two standard errors is not a certificate)" and
behind T4's "validity is paid for by the floor".
**Dong, Durfee, Rogers, arXiv:1909.13830v2** `[full text: abstract, Def. 2.2, Cor. 2.1, Thm 1, Def. 2.4, §3.4 with
Cor. 3.1, §4 Lemma 4.1–4.2, appendix passage with "maxkl"]`.  `ε`-bounded range (BR, from Durfee–Rogers): the
log-likelihood ratio of the two output laws lies in `[t−ε, t]` for some `t ∈ [0, ε]` — oscillation `≤ ε`.  The
exponential mechanism (output `y` with probability `∝ exp(εu(x,y)/(2Δu))` — a Gibbs measure) is `ε`-BR.
Lemma 4.1: every `ε`-BR pair is a post-processing of the two-point "generalized random response" `RR_{ε,t}`.
Appendix: `KL(Bern(q_{ε,t})‖Bern(p_{ε,t})) = t − (ε/(e^ε−1))(e^t−1)`, "maximized at `t = ln((e^ε−1)/ε)`, and the
value is `maxkl(ε) := ε/(e^ε−1) − 1 − ln(ε/(e^ε−1))`"; Cor. 3.1 writes it as `ε/(1−e^{−ε}) − 1 − ln(ε/(1−e^{−ε}))`
(the two are equal).  **`maxkl(w) = L(w)` (T1's constant) — in print, with the two-point extremal law.**
**Cesar & Rogers, arXiv:2004.07223v3** `[full text: Def. 2.2, Lemma 2.1, Defs 2.6–2.7, Lemma 3.2 with proof,
sentence after Lemma 3.4]`.  Lemma 3.2: for an `α`-BR mechanism `E[exp(λX_i)|F_{i−1}] ≤ e^{λ²α²/8}` and
`E[L_i|F_{i−1}] ≤ α/(e^α−1) − 1 − ln(α/(e^α−1))`; "α-BR implies (ξ, α²/8)-zCDP, where
`ξ = α/(e^α−1) − 1 − ln(α/(e^α−1)) − α²/8 ≤ 0`", i.e. `D_λ(P‖Q) ≤ λα²/8 + L(α) − α²/8` for all `λ > 1`.  **This is my
tilt lemma (M6), in a sharper form** (`D_λ ≤ (λ−1)w²/8 + L(w)`), by Hoeffding's lemma applied to the privacy loss.
**Bun & Steinke, arXiv:1605.02065v1** `[full text: Def. 1.1, Lemma 2.2, Lemma 2.3, Prop. 3.3, Remark 3.4, start of
the proof]`.  Lemma 2.2 "Composition": `D_α(P‖Q) ≤ D_α(P′‖Q′) + max_x D_α(P′_x‖Q′_x)` (cited from van Erven–
Harremoës) — the chain rule I used in (M7).  Prop. 3.3: `D_∞(P‖Q), D_∞(Q‖P) ≤ ε ⇒ D_α(P‖Q) ≤ ½ε²α`.
⇒ **(M7) `D_p(π_g‖π) ≤ (p−1)K/8 + Σ_i L(c_i) ≤ pK/8` is a two-line corollary of statements in print**
(conditionals of `π_g` are one-site tilts of range `≤ c_i` = "c_i-BR"; adaptive composition of zCDP).
**Specht's ratio.**  WebSearch (S) `Specht 1960 "Zur Theorie der elementaren Mittel" …` → Springer record (DOI
10.1007/BF01180475; Math. Z. 74, 91–98 (1960) per the snippet), RIMS Kôkyûroku PDFs.  Downloaded:
* Fujii, Lee, Seo, "An application of the Mond–Pečarić method to operator convex functions", RIMS Kôkyûroku 1259
  (2002) 1–10 `[full text: pp. 1–2]`: "In 1960 as a converse of the arithmetic-geometric mean inequality,
  W. Specht [11] estimated the upper bound of the arithmetic mean by the geometric one for positive numbers:
  For x_1, …, x_n ∈ [m, M] with M ≥ m > 0, (x_1⋯x_n)^{1/n} ≤ (x_1+⋯+x_n)/n ≤ M_h(1)(x_1⋯x_n)^{1/n}, where
  h = M/m … M_h(1) = (h−1)h^{1/(h−1)}/(e log h)"; and "J.I. Fujii, S. Izumino and Y. Seo [1] showed an operator
  version of Specht's theorem (1): … 0 < m ≤ A ≤ M … Then (Ax, x) ≤ M_h(1) exp(log A x, x) holds for every unit
  vector x" — for diagonal `A` this is `E a ≤ S(h)·exp(E log a)` for **every** law on `[m, M]`, i.e. T1's upper
  half with `a = e^{−r}`, `h = e^w`, `ln S(e^w) = L(w)` (identity checked numerically, C1).
* Furuichi, arXiv:1004.0581v3 `[full text: p. 1, Lemma 2.1, references]`: two-point weighted form
  `S(a/b)a^{1−ν}b^ν ≥ (1−ν)a + νb` attributed to Tominaga, Sci. Math. Japon. 55 (2002) 583–588; `S(h) = S(1/h) > 1`.
* Specht's own paper: **not accessed** (Springer; only the bibliographic record in a search snippet).

### step 8 (00:00–00:03) — heavy tails; Agapiou et al.; the coordinator's three leads
**Bubeck, Cesa-Bianchi, Lugosi, arXiv:1209.1727** `[full text: abstract, Lemma 1, Lemma 2 (statements), Thm 2 statement]`.
Lemma 1 (truncated mean, *raw* moment `E|X|^{1+ε} ≤ u`): w.p. `≥ 1−δ`, `μ̂_T ≤ μ + 4u^{1/(1+ε)}(log(δ⁻¹)/n)^{ε/(1+ε)}`.
Lemma 2 (median of means, *centred* moment `v`): `μ̂_M ≤ μ + (12v)^{1/(1+ε)}(16 log(e^{1/8}δ⁻¹)/n)^{ε/(1+ε)}`.  With
`p = 1+ε`, `u = B^p`: error `≤ 4B(log(1/δ)/n)^{(p−1)/p}`, i.e. `n = log(1/δ)(4B/(εμ))^{p/(p−1)}` — A17.3(ii) with a constant.
**Devroye, Lerasle, Lugosi, Oliveira, arXiv:1509.05845v1** `[full text: p. 3 passage, Thm 3.1 and its proof §4.3]`.
Thm 3.1: `n > 5`, `M > 0`, `α ∈ (0,1]`, `δ ∈ (2e^{−n/4}, 1/2)`: for any mean estimator,
`sup_{P ∈ P^M_{1+α}} P{|Ê_n − μ_P| > (M^{1/α} ln(2/δ)/n)^{α/(1+α)}} ≥ δ` (class: `(1+α)`-th *central* moment `= M`).  Proof:
two scaled Bernoulli laws `P_±` (mass `p = (2/n)log(2/δ)` at `±c`), coupled so that the two samples coincide with
probability `≥ 2δ` — the "rare atom not seen" argument = A17.2(ii)'s packing/detection mechanism (and it is a
*two-point testing* bound: knowing both candidates, i.e. a hint, does not help in the sampling model).  Formula
(10) for the central moment of `P_±` is stated "for any α > 0".
⇒ O1 for `1 < p ≤ 2` is the minimax rate `M^{1/p}(ln(1/δ)/n)^{(p−1)/p}` read backwards (yes to the brief's question);
for `p > 2` estimation saturates at the variance rate (KNR Thm 3.9), and the hinted exponent `p/(p−1) < 2` is the
part I did not find in print.
**Agapiou, Papaspiliopoulos, Sanz-Alonso, Stuart, arXiv:1511.06196v3** ("Submitted to Statistical Science" on the
PDF) `[full text: abstract, §2.2 with Thm 2.1, §2.3.3, §2.5]`.  `ρ := π(g²)/π(g)²`; Thm 2.1: for the autonormalised
estimator, `sup_{|φ|≤1}|E[μ^N(φ) − μ(φ)]| ≤ 12ρ/N`, `sup_{|φ|≤1}E[(μ^N(φ) − μ(φ))²] ≤ 4ρ/N`; `D_χ²(μ‖π) = ρ − 1`;
`ρ ≥ e^{D_KL(μ‖π)}` (2.5); "the number of particles required for accurate importance sampling scales exponentially
with the Kullback-Leibler divergence between proposal and target and linearly with the χ² divergence".  So
`ρ = 1 + χ² = e^{D_2}`: the `p = 2` row of A17's table at one instance; no class statement, no hint.

**Lead (1) — χ / Rényi upper bounds in variational inference.**
* Dieng, Tran, Ranganath, Paisley, Blei, arXiv:1611.00328v4 (NIPS 2017 per the PDF footer) `[full text: abstract,
  §1, §2.1–2.3, App. D]`.  Eq. (2): `CUBO_n = (1/n) log E_q[(p(x,z)/q(z))^n]`; Thm 1 ("Sandwich Theorem"):
  `∀n ≥ 1: ELBO ≤ log p(x) ≤ CUBO_n`, `CUBO_n` non-decreasing in `n`.  App. D: `Var(Î) = (1/B)[E_q(w²) − p(x)²]`,
  "minimizing this variance is equivalent to minimizing … the χ²-divergence".  **No certificate:** "by Jensen's
  inequality … this is a biased estimate of CUBO_n … The objective is not guaranteed to be an upper bound if S is
  not chosen appropriately from the beginning.  This problem does not exist for lower bounds because the Monte
  Carlo approximation is still a lower bound".  ← the asymmetry of T4, stated in print for the ML setting.
* Li & Turner, arXiv:1602.02311v3 `[full text: abstract, §3, §4.1, App. D first paragraphs]`.  VR bound
  `L_α = (1/(1−α)) log E_q[(p/q)^{1−α}]`; Thm 1: `L_VI ≤ L_{α₊} ≤ L_0 ≤ L_{α₋}` for `0<α₊<1`, `α₋<0`, and `L_0 = log p(D)`
  iff `supp p ⊆ supp q` (so `α₋ = 1 − p` gives `ln Z ≤ (1/p) ln E_q w^p`).  Thm 2/Cor. 1: the Monte-Carlo estimate is
  biased towards `L_VI`; "negative alpha values can potentially be used to improve the accuracy of the
  approximation, at the cost of losing the upper-bound guarantee".  Sandwiching "we leave to future work".
  Estimator only; no finite-sample guarantee over a class.
**Lead (2) — Midgley, Stimper, Simm, Schölkopf, Hernández-Lobato, arXiv:2208.01893v3 ("Published as a conference
paper at ICLR 2023")** `[full text: abstract, §1, §2 "Alpha divergence", the evaluation paragraphs, discussion]`.
Claims: "minimize the mass-covering α-divergence with α = 2, which minimizes importance weight variance"; "When
α = 2, minimizing the α-divergence is equivalent to minimizing the variance of the importance sampling weights".
ESS is an *empirical evaluation metric* only (from 5×10⁴ flow samples); **"the ESS for the SNF, RBD and the flow
trained by minimizing KL(q_θ‖p) are spurious as these methods are missing modes"**.  No statement relating a
sample size to the divergence; no certificate.
**Lead (3) — direction of the divergence.**  Minka, MSR-TR-2005-173 (7 Dec 2005) `[full text: abstract, §2
passages]`: `α ≤ 0` divergences "are zero-forcing because p(x) = 0 forces q(x) = 0 … This causes some parts of p to
be excluded"; "(α ≥ 1) are inclusive (α < 1 are exclusive).  Inclusive divergences require q > 0 whenever p > 0,
thus avoiding 'false negatives.'  If two identical Gaussians are separated enough, an exclusive divergence
prefers to represent only one of them, while an inclusive divergence prefers to stretch across both."  Also
Li–Turner §3: "zero-forcing (α → +∞, when using uni-modal approximations it is usually called mode-seeking) and
mass-covering (α → −∞)"; FAB §2: "The α-divergence is mode-seeking for α ≤ 0 and mass-covering for α ≥ 1 (Minka,
2005)"; and, in physics, Jarzynski 2006 eq. (45) (sampling A costs `exp D[p_B|p_A]`).

### step 9 (00:03–00:11) — one-sidedness in statistics and ML; certificate complexity; class F_C; free-energy and K* literature through PubMed
**Grosse, Ghahramani, Adams, arXiv:1511.02543v1** `[full text: abstract, §4 intro, §4.1, §4.2 first page]`.  Unbiased
estimators of `Z` "are stochastic lower bounds, in two senses": Markov: `Pr(log Ẑ > log Z + b) < e^{−b}` (25); Jensen:
`E[log Ẑ] ≤ log Z` (26).  §4.2: "we would expect good upper bounds to be harder to obtain than good lower bounds.
For a lower bound on the log-ML, it suffices to exhibit regions of high posterior mass.  For an upper bound,
one would have to demonstrate the absence of any additional probability mass. … But suppose we are given a
hint in the form of an exact posterior sample."  ← T4's asymmetry, stated heuristically, and a "hint" (of a
different kind: a sample of the target).  Remark for us: (25) is a *valid* lower confidence bound on `ln Z` with
no assumption on `r` at all (slack `ln(1/δ)` nats) — the cheap side does not even need the oscillation `w` that
T4's `w² ln(1/δ)/(2ε²)` uses.
**Thomas, Theocharous, Ghavamzadeh, "High confidence off-policy evaluation" (© 2015 AAAI on the PDF)** `[full text:
abstract, "Concentration Inequality" section, Thm 1 statement]`: importance-weighted returns "are bounded from
below by zero … and may have a large upper bound … very long tail"; "removing the upper tail of a distribution
can only lower its expected value" ⇒ Thm 1: a *lower* confidence bound for the mean of non-negative variables
from `Y_i = min{X_i, c_i}`, which "removes the need to determine a tight upper bound on the largest possible
importance weighted return".
**Phan, Thomas, Learned-Miller, arXiv:2106.03163v5** `[full text: §2 passage, §4.2 passage]`: for an *upper* confidence
bound on a mean "we only need to know a superset of the support with finite upper bound"; in the "1-ended
support setting" the method "is equal to Anderson's".
**Wang & Ramdas, arXiv:2202.01250v6, §10.1** `[full text of that subsection]`: moment assumptions "are necessitated
by the results of Bahadur and Savage [1956], which immediately imply that if no upper bound on a moment is
known a priori, mean estimation is provably impossible" (reference there: Ann. Math. Statist. 27(4):1115–1122,
1956).  **Bahadur–Savage itself: not accessed** (Project Euclid: Incapsula page / empty page via WebFetch).
⇒ T4 "the floor is the one assumption sampling cannot replace" = Bahadur–Savage (nothing without an a-priori
bound) + Anderson-type one-sided bounds (an upper bound on the support of `Y = e^{−r}`, i.e. the floor, suffices
for the upper confidence bound) — **and the same literature contradicts the literal "nothing else can replace
it"**: a bound on any moment of order `p > 1` of `Y` suffices (BCL13, KNR) — which is A17's point.
**Karp, Luby, Madras, J. Algorithms 10 (1989) 429–448** `[full text: title page, theorem statement p. 3 and
appendix]`: "ZERO-ONE ESTIMATOR THEOREM. Let μ = |G|/|U|. Let ε ≤ 2. If N ≥ (1/μ)·(4 ln(2/δ)/ε²) then the Monte-Carlo
algorithm described above is an (ε, δ) approximation algorithm" (OCR reads μ as p).
**Aaronson, arXiv:quant-ph/0210020v1** `[full text: abstract, Defs 1–3, Prop. 4, Lemma 5, relations paragraph]`.
Def. 3: "A randomized verifier for input X is a randomized algorithm that, on input Y ∈ Dom(f), (i) accepts with
probability 1 if Y = X, and (ii) rejects with probability at least 1/2 if f(Y) ≠ f(X). … RC^X(f) is the minimum
expected number of queries used by a randomized verifier for X"; the verifier is given X "since any additional
information that a prover might provide, the verifier can compute for itself".  Lemma 5: non-adaptive verifiers
that query coordinate `i` with probability `λ_i` and reject iff they find a disagreement achieve `Θ(RC^X(f))`
with cost `Σλ_i`.  `RC(f) = Ω(bs(f))`.  ⇒ **"with a hint" = Aaronson's randomised verifier; the spot check =
his non-adaptive verifier; T3 is the value of `RC^X` for weighted approximate summation over a box**, where the
covering LP has the closed form `λ_x ∝` dip (bump) weight.
**Mathé & Novak, arXiv:math/0611285v2** `[full text, re-read: abstract, p. 4, class definition, Thms 1–2]`:
`F_C = {(f,ρ): ‖f‖_∞ ≤ 1, ρ(x)/ρ(y) ≤ C}`; Thm 1: every Monte Carlo method with `n` values has error
`≥ (√2/6)√(C/(2n))` (`2n ≥ C−1`); Thm 2: simple Monte Carlo `≤ 2 min{1, √(2C/n)}`; "the complexity of the problem
is linear in C".  = the class-level, no-hint, all-algorithms statement for *expectations* on the box
(`C = e^{ρ₋+ρ₊}`), dimension-free in the same sense as T3.  For `ln Z` only the floor enters — that asymmetry is
not in Mathé–Novak (they treat ratios of integrals).
**Pradhan & Dagum, arXiv:1302.3598 (pp. 446–452 of the proceedings)** `[full text, OCR]`: with the "local variance
bound" `r` of a belief network, "the Zero-One Estimator Theorem … can be rewritten N ≤ (4r^k/ε²) ln(2/δ)" — an
a-priori bound on the ratio of weights turns likelihood weighting into a certified `(ε,δ)` estimate of a
probability of evidence; attributed to Dagum & Luby (1993/1994/1997), which I did not open.
**DKLR at an instance (own remark, uses only the restatement in Mnih et al.):** under the floor measure
`X = e^{−(r−lo)} ∈ (0,1]`; at the centre of a constant box `X` is constant, `σ² = 0`, so the *unhinted* stopping
rule already costs `O(log(1/δ)/(εμ′)) = O(e^{ρ₋} log(1/δ)/ε)`: **at the centre the hint is worth nothing**; in
general unhinted sampling costs `max(σ_X², εμ′)/(εμ′)²` and the hint (plus the freedom to choose where to
evaluate) removes the `σ²` term.
**PubMed (tool `search_articles`, `get_article_metadata`, `get_full_text_article`); everything below is "according
to PubMed", reading level `[abstract]` unless stated:**
query `Kofke DA[Author] AND (free-energy perturbation OR phase-space overlap)` → 12 hits; kept:
* Lu, Adhikari, Kofke, Phys Rev E 68, 026122 (2003), doi:10.1103/PhysRevE.68.026122 — "Finite sampling in
  free-energy perturbation (FEP) calculations … leads to reproducible systematic errors, with sign shown to
  depend (in a known way) only on which system governs sampling in the simulation.  Thus the result of a FEP
  calculation can be used as a bound on the true free energy.  This inequality is of a wholly different nature
  from established forms such as the Gibbs-Bogoliubov inequality".
* Wu & Kofke, Phys Rev E 70, 066702 (2004), doi:10.1103/PhysRevE.70.066702 — asymmetric bias; neglected-tail model;
  "the bias is significantly smaller when sampling is performed on the system having a broader work
  distribution ('insertion')".
* Wu & Kofke, J Chem Phys 123, 054103 (2005), doi:10.1063/1.1992483 — two relative entropies "expressed in terms
  of the dissipated work for … FEP calculations in the A→B and B→A directions"; "The relative entropies are
  used to scale the amount of sampling to obtain a universal bias curve … a simple heuristic … we argue that it
  is fail-safe".
* Wu & Kofke, J Chem Phys 123, 084109 (2005), doi:10.1063/1.2011391 — "Stages should always be constructed such
  that work is performed only into a system that has a phase-space subset relation with the starting system."
* Lu, Kofke, Woolf, J Comput Chem 25:28–39 (2004), doi:10.1002/jcc.10369 — overlap sampling "considers the
  asymmetry of the FEP calculation".
query `Bias and error in estimates of equilibrium free-energy differences from nonequilibrium measurements` → Gore,
Ritort, Bustamante, PNAS 100:12564–9 (2003), doi:10.1073/pnas.1635159100, PMC240657 — abstract: "we derive the
large N limit for the Jarzynski estimator bias, variance, and mean square error that is correct for arbitrary
perturbations".  PMC returned no XML full text; `WebFetch` of the PMC page gave an automatic reading
(`[fetch-tool]`, formulas are images): "the number of trajectories necessary to average over to obtain a given
level of accuracy increases exponentially with W̄_dis".
query `exponential averaging Bennett acceptance ratio … Shirts Pande` → Shirts & Pande, J Chem Phys 122, 144107
(2005), doi:10.1063/1.1873592 — reviews "theoretical estimates of the bias and variance of exponential averaging
(EXP), thermodynamic integration (TI), and the Bennett acceptance ratio (BAR)"; no sample-size law in the
abstract.
queries `Donald BR[Author] AND partition function AND (K* OR …)`, `minimized dead-end elimination criterion …`,
`Lilien RH[Author] AND Donald BR[Author] AND ensemble-based scoring`, `Ojewole AA[Author] AND Donald BR[Author] AND K*`:
* Georgiev, Lilien, Donald, J Comput Chem (2008), doi:10.1002/jcc.20909, PMC3263346 — **`[full text]` §4 and
  Proposition 3**: with `q*` the partial partition function of the `m` conformations returned by A*, `n`
  conformations not yet generated (all with lower bounds above `E_t`), `k` pruned conformations with lower bound
  `E_0`, `ρ = ε/(1−ε)`: "If the lower bound B(c) on the minimized energy of the (m+1)st conformation returned by A*
  satisfies B(c) ≥ −RT(ln(q*ρ − k exp(−E_0/RT)) − ln n), then the partition function computation can be halted,
  with q* guaranteed to be an ε-approximation to the true partition function q, that is, q* ≥ (1−ε)q"; proof:
  `q = q* + q′ + p* ≤ q* + n exp(−E_t/RT) + k exp(−E_0/RT)`.  Lower bounds are "a sum of precomputed pairwise
  minimum energy terms".  = T2 with a function floor and no ceiling (one-sided certificate).
* Lilien, Stevens, Anderson, Donald, J Comput Biol 12(6):740–61 (2005), doi:10.1089/cmb.2005.12.740 — "an
  efficient deterministic approximation algorithm, capable of approximating our scoring function to arbitrary
  precision".
* Ojewole, Jou, Fowler, Donald, J Comput Biol 25(7):726–739 (2018), doi:10.1089/cmb.2017.0267 (BBK*); Jou, Holt,
  Lowegard, Donald, J Comput Biol (2020), doi:10.1089/cmb.2019.0315 (MARK*; PMC sent no full text): "provable
  ε-approximations to partition functions … by computing provable, admissible pairwise-minimized energy lower
  bounds … and using the A* enumeration algorithm"; Lowegard et al., PLoS Comput Biol 16(6):e1007447 (2020),
  doi:10.1371/journal.pcbi.1007447: "Often, reaching an ε-approximation … takes a prohibitive amount of time and
  space."
  (This literature is about sequence design, outside our scope; cited only for the certificate scheme.)
  Not in what I read: sampling with a certificate; any lower bound on the number of evaluations.

### step 10 — sampling with a certificate in graphical models; Rényi-based bounds for importance weights; IBC rates; Hoeffding read; physics abstracts; Crossref checks
(time of writing is the `date` stamp printed when this entry was appended: see end of entry)
**Liu, Fisher, Ihler, "Probabilistic variational bounds for graphical models" (NIPS 2015; PDF from
proceedings.nips.cc; pages 1432–1440 per a search snippet)** `[full text: abstract, §1, related work, §3 with
Prop. 3.1, Cor. 3.2 and discussion]`.  **Closest precedent found for T3/T4 in unhinted form.**  A convex
variational upper bound `Z_trw ≥ Z` comes with a mixture-of-trees proposal `q` that can be sampled exactly and
for which "the importance weight w(x) = f(x;θ)/q(x;θ^T) satisfies w(x) ≤ Z_trw(θ^T), ∀x" (Prop. 3.1 i);
`var(w) ≤ Z_trw·Z − Z² ≤ Z²_trw/4`.  Cor. 3.2 (empirical Bernstein, Maurer–Pontil):
`Δ = √(2·v̂ar(w)·log(2/δ)/n) + 7·Z_trw·log(2/δ)/(3(n−1))`; `Ẑ ± Δ` are upper/lower bounds of `Z` w.p. `≥ 1−δ` each.  "The
second term captures the possibility that the empirical variance is inaccurate; it depends on the
boundedness of w(x) and decays at rate 1/n."  "one can apply a stopping criterion [e.g., 5, 20] on n to guarantee
a relative error ε with probability at least 1 − δ, using the bound on w(x); roughly, the expected number of
samples will depend on Z_trw/Z, the relative accuracy of the variational bound."  Abstract: "provide
certificates of accuracy given enough samples relative to the error in the initial bound".
  Dictionary: bounding model ↔ floor `lo` (a *function* floor: a lower model whose Gibbs measure is sampled
  exactly); `Z_trw ↔ Z(lo)`; `w/Z_trw ↔ X = e^{−(r−lo)} ∈ (0,1]`; `Z_trw/Z ↔ Z(lo)/Z(g)` = T3's cost quantity; the
  Bernstein bracket = T4's last sentence, almost word for word (width: sample variance; validity: the bound
  on the weights).  Not there: a hint/verification count, the `1/ε` law, dip-weighted spot checks, lower
  bounds on the number of evaluations.  Also relevant to A17 "Reading 2" (a lower model on a graph of small
  tree-width): their §4 "Weighted Mini-bucket Importance Sampling" (not read beyond the heading).
**Gogate, Bidyuk, Dechter, arXiv:1206.5242 (UAI proceedings p. 141 ff.)** `[full text: abstract, §2.2, §3]`: "high
confidence lower bounds on probability of evidence but does not have any guarantees in terms of relative or
absolute error … uses the Markov inequality"; "[Dagum and Luby, 1997] provide an upper bound on the number of
samples N required to guarantee … relative error ε with probability at least 1 − δ"; "The independence from N
allows us to use even a single sample to derive lower bounds."  ← the cheap side, validity for free.
**Metelli, Papini, Faccio, Restelli, arXiv:1809.06098v2 (NeurIPS 2018 per the arXiv record)** `[full text: §3–4
passages]`: "exponentiated α-Rényi divergence d_α(P‖Q) = exp(D_α(P‖Q))"; `Var w = d_2(P‖Q) − 1`,
`ess sup w = d_∞(P‖Q)`; `ESS(P‖Q) = N/d_2(P‖Q)` (their (6)); Thm 4.1 (Cantelli): w.p. `≥ 1−δ`,
`E_P f ≥ (1/N)Σ w f − ‖f‖_∞ √((1−δ)d_2(P‖Q)/(δN))`.  = A17.3(i)'s bracket for `p = 2` (one-sided), with `d_2` known.
**Heinrich & Novak, arXiv:quant-ph/0105114v1** `[full text: abstract, Thm 4, summary table]`: summation of `N`
numbers in the unit ball of `L_p^N`, `n < N` queries: randomised minimal error `= (1 + √((N−1)n/(N−n)))⁻¹` for
`2 ≤ p ≤ ∞` (Mathé 1995, exact), `≍ n^{−1+1/p}` for `1 ≤ p < 2` (`N > βn`); deterministic: `1` (no rate).  = the IBC form
of A17.3 and of "deterministic certificates need (almost) everything"; mean-square criterion, uniform base
measure, no hint.
**Hoeffding, JASA 58 (1963) 13–30 (scanned PDF on a university course page; pp. 13–14 and 20–22 read as page
images)** `[full text of those pages]`.  Lemma 1 / (4.2): `E e^{hX} ≤ ((b−EX)/(b−a))e^{ha} + ((EX−a)/(b−a))e^{hb}`;
(4.12)–(4.14): `E e^{h(X_i−μ_i)} ≤ e^{L(h_i)}`, `L(h_i) = −h_i p_i + ln(1 − p_i + p_i e^{h_i})`, `h_i = h(b_i−a_i)`,
`p_i = (μ_i−a_i)/(b_i−a_i)`; `L″ ≤ ¼` ⇒ (4.15) `L(h_i) ≤ h²(b_i−a_i)²/8`.  **So the upper half of T1 *before* the
maximisation over the mean is Hoeffding's (4.12)–(4.13) — with the same letter `L` — and is sharper than T1
whenever the mean is known or estimated**: `ln E e^{Y−EY} ≤ −wp + ln(1−p+pe^w)`, `p = (EY − min Y)/w`.
**Berend & Kontorovich, arXiv:1210.3248v1** `[full text: abstract, §1, Thm 4]`: Kearns–Saul inequality
`(1−p)e^{−tp} + pe^{t(1−p)} ≤ exp((1−2p)t²/(4 log((1−p)/p)))`, "optimal in the sense that, for every p, there is a t for
which equality is achieved" — the sharp constant at fixed `p` (sup over `t`), i.e. the *other* optimisation; it
is not T1's `L(w)` (sup over `p` at fixed `t`).  Kearns–Saul's own paper (arXiv:1301.7392) and Bentkus
(arXiv:math/0410159; Ann. Probab. 32 (2004) 1650–1673 per the arXiv record) downloaded, not read.
**Binette, arXiv:1805.05135v2 (doi:10.1109/TIT.2019.2896192 on the PDF)** `[full text: abstract, Thm 1/Cor. 2
statements]`: Cor. 2: `sup_{(P,Q)∈B(m,M)} D_f(P‖Q) = ((M−1)f(m) + (1−m)f(M))/(M−m)` (likelihood ratio between `m` and
`M`).  With `f = −log` and `M/m = e^w`, maximising over `m` gives `m = w/(e^w−1)` and the value `L(w)` (my
calculus; checked numerically in C3).  A third route to T1.  Sason–Verdú (arXiv:1508.00335v7) has the
`β₁, β₂` (bounded relative information) theorems 6–11; headings read only.
**Zuckerman & Woolf, arXiv:physics/0201046v1** `[full text: abstract, introduction, "Divergent Moments Case"]`:
"the free energy is bounded according to ΔF ≤ ΔF_n, any n.  This inequality results from the convexity of the
exponential function"; for a Boltzmann factor with tail `z^{−(1+α)}`, `1 < α < 2`: `f_n − f ≈ φ_{α−1}(1/n)^{(α−1)}`
(15) — power-law convergence governed by the tail index of `e^{−w}` (the physics counterpart of the `p`-th
moment rows).
**Hahn & Then, arXiv:0904.0625v3, 0910.2858v2** `[abstracts; statement index]`: convexity of the mean-square error
of Bennett's method ("state and prove"); a convergence *measure* for the two-sided estimator, explained with
the neglected-tail model.  No sample-size theorem.
**Lu & Kofke II, J. Chem. Phys. 115, 6866–6875 (2001), doi:10.1063/1.1405449** `[fetch-tool: automatic reading of
the abstract page; the tool would not reproduce the abstract verbatim]`: the quantity `M exp(ΔS/k)` (`M`
independent samples) indicates whether a result is likely accurate — about 100 minimally, 1000 safer; exact
phrase returned: "such calculations must be performed in the 'insertion' direction".  Heuristic by title.
Lu & Kofke I (J. Chem. Phys. 114, 7303–7311, doi:10.1063/1.1359181): bibliographic record only.
**Atar, Chowdhary, Dupuis, arXiv:1310.6391v1** `[abstract; Thm 2.1 formula seen]`: variational formulas for
exponential integrals with Rényi divergence, "bounding tail properties of an intractable model in terms of
a tractable one" — the uncertainty-quantification relative of A17's classes (divergence balls around a
tractable model); no evaluation-cost statement.  Birrell et al., arXiv:1911.09580: title only.
**Sanz-Alonso, arXiv:1608.08814v1** `[abstract; statement index]` (A1's copy): "necessary conditions on the sample
size in terms of the Kullback-Leibler and χ² divergences".
**Crossref API (records only, to avoid citing bibliographic details from memory):** Zwanzig, J. Chem. Phys. 22(8),
1420–1426 (1954), doi:10.1063/1.1740409 ("High-Temperature Equation of State by a Perturbation Method. I.
Nonpolar Gases"); DKLR, SIAM J. Comput. 29(5), 1484–1496 (2000); Specht, Math. Z. 74(1), 91–98 (1960); Bahadur &
Savage, Ann. Math. Statist. 27(4), 1115–1122 (1956); Hoeffding, JASA 58(301), 13–30 (1963); Lu & Kofke I and II
(above); Kofke, Fluid Phase Equilibria 228–229, 41–48 (2005), doi:10.1016/j.fluid.2004.09.017; Dagum & Luby,
Artificial Intelligence 93(1–2), 1–27 (1997), doi:10.1016/S0004-3702(97)00013-1; Mathé, J. Complexity 11(4),
394–415 (1995); Kunsch–Novak–Rudolf, J. Complexity 53, 40–67 (2019), doi:10.1016/j.jco.2018.10.007; Anderson (1969):
only a technical-report record (doi:10.21236/ad0696676).  No Crossref match for Dong–Durfee–Rogers or
Block–Polyanskiy (cited by arXiv number).  A DOI I had guessed for Lu–Kofke II turned out to belong to another
paper — discarded.
WebSearch (X) `verifying a claimed mean or sum with an untrusted hint: O(1/ε) queries versus Θ(1/ε²) …` → nothing on
certificate complexity of approximate sums; side hit arXiv:2404.08158 ("On the Power of Interactive Proofs for
Learning"; snippet: "sample complexity of O(1/ε) for … PAC-verification") `[search snippet]`.
arXiv API: `abs:"free energy perturbation" AND abs:"confidence interval" AND abs:"rigorous"` → 0;
`abs:"partition function" AND abs:"confidence interval" AND abs:"importance sampling" AND abs:"upper bound" AND abs:"bounded"` → 0.
appended at 00:17 UTC

### step 11 — the "not found" searches, and the hit that changes the verdict on O1
WebSearch (X) `free energy perturbation exponential averaging rigorous finite-sample confidence interval "lower bound"
on energy difference bounded perturbation concentration inequality certified error bar Zwanzig estimator
non-asymptotic guarantee` → no rigorous certified error bar for exponential averaging found (summaries of
applied/heuristic treatments); side hit: Kofke's manuscript (below).
**Kofke, "On the sampling requirements for exponential-work free-energy calculations" (manuscript "For submission
to Molecular Physics, issue devoted to the Liblice 2006 conference"; PDF from the author's departmental
publication page)** `[full text: abstract, §3 passage with eqs. (11), (15)]`: "We review prior research that has
demonstrated that the necessary amount of sampling scales exponentially with the dissipated work associated
with the reverse trajectory"; relative entropies `s_F = ∫p_A ln(p_A/p_B)`, `s_R = ∫p_B ln(p_B/p_A)`; "the bias … collapsed
onto a seemingly universal curve … We took this as the basis for a heuristic … Thus we have stipulated
`M_F ≥ 1 + 2(· s_R)^{1/2} exp(s_R)`, `M_R ≥ 1 + 2(· s_F)^{1/2} exp(s_F)`" (one symbol inside the root is not legible in the
text extraction); "for instantaneously deleting a hard sphere … s … is thus literally infinite.  Correspondingly
no amount of deletion sampling is capable of rendering an accurate result"; "the heuristic … is fail-safe".
→ forward sampling of A needs `≈ exp(KL(p_B‖p_A))`: stated as a *heuristic* ("stipulated").
WebSearch (X) `"Rényi divergence" bounded class of targets importance sampling normalizing constant minimax sample
complexity lower bound … ε^{-p/(p-1)} … heavy-tailed importance weights` → **arXiv:2602.23535**.
**Block & Shetty, "Partition Function Estimation under Bounded f-Divergence", arXiv:2602.23535v1 (26 Feb 2026)**
`[full text: abstract, §§1–6, App. D.1 (proof of Thm 8); appendix A–C, E–F not read]`.
* Setting: i.i.d. samples `X_i ∼ μ` and evaluations of the unnormalised density ratio `λ = Z·dν/dμ` at the samples;
  goal `(1−ε)Z ≤ Ẑ ≤ (1+ε)Z` w.p. `1−δ`.  (= A17's setting without a hint: `μ ↔ π`, `λ ↔ Y = e^{−r}`, `Z ↔ μ`, `ν ↔ π_g`.)
* `Cov_M(ν‖μ) = ν{dν/dμ ≥ M}`, `ICov_M = ∫₀^M Cov_t dt`; `γ_f(M) = inf{t ≥ 1 : f(t)/t ≥ M}` (KL: `≍ exp(M)`; Rényi-α:
  `≍ M^{1/(α−1)}`).
* Thm 4: `n ≳ M_ε log(1/δ)/ε` with `M_ε⁻¹·ICov_{M_ε} ≤ ε/4`.  Thm 5: `n ≳ γ_f(6D_f(ν‖μ)/ε)·log(1/δ)/ε ∨ c²/ε²` — "for KL
  divergence … n ≳ exp(c·D_KL(ν‖μ)/ε)/ε samples suffice as well as for α-Renyi divergences with 1 < α ≤ 2, where
  n ≳ (ε^{−α}·D_f(ν‖μ))^{1/(α−1)} samples suffice … α-Renyi divergences with α > 2, where n ≳ 1/ε² samples suffice".
  Informal Thm 2: `n = Θ(γ_f(Θ(1)·ε⁻¹·D_f) ∨ D_χ²·ε⁻²)` "necessary and sufficient".
* **Thm 6 (one-sided):** "an asymmetric approach that is capable of improving the sample complexity scaling in ε
  for the lower tail at the cost of a significantly worse upper tail bound": if `n ≳ log(1/δ)·M/ε` with
  `Cov_M(ν‖μ) ≲ ε` then `(1−ε)Z ≤ Ẑ ≤ M·Z`; "it suffices to take M = γ_f(6·D_f(ν‖μ)/ε)"; in the superquadratic case
  "a sample complexity of estimating Z from below that is significantly smaller than the ε⁻² scaling".
  For Rényi-p this is `e^{D_p}ε^{−p/(p−1)}·log(1/δ)` for **every** `p > 1` — A17.2's "with a hint" column, as the
  cost of the guarantee "no mass was missed", without a hint.
* Lower bounds: Thm 7 (integrated coverage; "for any non-atomic μ"); Prop. 1 (bounded `f′`, e.g. TV, Hellinger:
  impossible); Thm 8 (`n ≳ γ_f(C/(2ε))/ε` on a class with `D_f ≤ C + f(1−ε)`; "holds for arbitrary f-divergences");
  Prop. 2 (`‖dν/dμ‖_∞ ≤ 4`: `n ≳ ε⁻²`).  Proof of Thm 8 (read): distinguish `ν₀ = μ` (density ratio ≡ 1 — the
  *centre*) from `ν_{p,ε}` (ratio `1−ε` w.p. `1−p`, `1+ε(1/p−1)` w.p. `p`): "one must observe at least one sample from
  the high-density region … which occurs with probability p under μ" — the rare-set detection argument at the
  centre = A17.2(ii)/A17.4(ii).
* §3.3: sampling `n ≳ M log(1/ε)` with `Cov_M ≲ ε` (Prop. 3) vs estimation: "at least an ε⁻¹ factor improvement";
  "'counting' … is strictly harder than … 'sampling' under general f-divergence or coverage constraints" —
  the factor `1/ε` I found between A17.2 and Block–Polyanskiy (step 7) is their §3.3.
* Related work as they state it: "Devroye et al. [13] … heavy-tailed mean estimation under polynomial moment
  constraints; our f-divergence [bounds] recover their results when considering Renyi divergences"; Chatterjee–
  Diaconis: "exponentially many samples in the KL divergence are necessary and sufficient … do not consider
  more general f-divergences or coverage".  Their reference list gives: Chatterjee & Diaconis, Ann. Appl. Probab.
  28(2):1099–1135 (2018); Devroye et al., Ann. Statist. 44(6):2695–2725 (2016); Block & Polyanskiy, COLT 2023, PMLR,
  pp. 228–273.
* No occurrence of "hint", "verif…", "certif…" in the text (grep).  Lemma 1 ("generalized Paley–Zygmund"):
  a non-negative variable exceeds `(1−ε)` times its mean with probability `≥ ε·exp(−O(1)·E[X log X]/(ε E X))`.
**⇒ Verdict on O1 changes:** A17.3 (no hint; three regimes; lower bounds), A17.4 (KL: `exp(Θ(κ/ε))`) and the first
half of A17.5 are **in print** (Feb 2026), in the sampling model; A17.2's hinted count equals their one-sided
count (Thm 6), and its lower bound is their Thm 8 construction.  What is left to A17: reading the one-sided
cost as the verification cost (query model, hint, finite spaces, explicit constants), A17.5(ii), A17.6.
appended at 00:20 UTC
