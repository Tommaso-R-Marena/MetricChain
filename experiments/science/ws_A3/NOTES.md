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
