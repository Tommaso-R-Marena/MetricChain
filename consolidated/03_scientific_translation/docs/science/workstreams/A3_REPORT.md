# Workstream A3 — prior art: certifying a free energy by sampling from a model (box classes, floors, Rényi balls)

Science division, independent workstream A3.  Started 2026-11-25 23:33 UTC; this version written
2026-11-26 between 00:25 and 01:05 UTC (machine clock).
Statements positioned: **T1–T4** (theory division, forthcoming theory report §11.30; read in
`THY-RES-0007.md` §4 and in the theory `RESEARCH_LOG.md`, "Resume here (cycle 10, fourteenth
checkpoint)", item 1 (a)–(e), export `thy_ro_658b77f`) and **O1–O2** (ours: addendum A17 of
`docs/science/INFERENCE_LIMITS_ADDENDA.md`, statements A17.1–A17.6, which the coordinator declared
the authoritative version while this workstream was running; A17.4 and A17.5 are positioned too).
Working files: `experiments/science/ws_A3/` (`NOTES.md` = step-by-step log with the complete search
log; `check_math.py` / `check_math.out` = numerical checks; `getpdf.sh`, `arxiv_q.py`,
`arxiv_batch.py` = the download helpers).  Downloaded papers are kept outside the repository
(scratchpad `a3_dl/`, text in `a3_txt/`) and are identified below by arXiv number, DOI or PMC id.

**Reading levels** (COMMON rule 5): `[full text]` — I had the paper's own text (a PDF converted with
`pdftotext`, a scanned PDF read as page images, or the PMC full text) and read the passages named;
`[abstract]`; `[fetch-tool]` — an automatic reading of a web page, quotations short and not checked
against the page by me; `[search snippet]` — only what a search engine returned; `[record]` — a
bibliographic record only (Crossref / arXiv listing); `[from memory — unverified]`.
**Epistemic labels** (rule 6): **[V]** machine-checked, **[P]** paper proof given here, **[K]** known and
cited, **[N]** numerical evidence only, **[C]** conjecture, **[H]** heuristic.
**Classification scheme of the brief:** **(1)** in print as stated; **(2)** a known special case or a
direct corollary; **(3)** folklore without a locatable statement; **(4)** not found after the searches
listed.  "Not found" never means "new".  Items retrieved through PubMed are introduced by "according
to PubMed" and carry DOI links.

## How far I got

**Done.**  All six statements are classified (§1, §4), each with the closest statement in print side
by side and a sentence to write.  About 93 sources were located; 47 were read in the passages that
matter at `[full text]` level (§4.10), among them the three that decide the verdicts: Hoeffding's
1963 paper (scanned pages), the differential-privacy papers that contain T1's constant and the
sharpening of O2, and a February 2026 preprint (Block–Shetty) that contains O1 in unhinted form.
Three statements of my own came out of the comparison and were checked numerically (§2, §3):
a sharpening of A17.6 by the factor `p/(p−1)`; the fact that at the centre of a constant box the
hint is worth nothing; and that T1's bound is weaker than the inequality in Hoeffding's own proof
whenever the mean is known.  **No error was found in T1–T4 or O1–O2**; three of their sentences
say more than the literature allows (§4.8).  Two additions of the coordinator were taken up while
the work was running: the three leads on variational inference and flows (§4.5(f),(g), §4.7), and the
positioning of A17.7 and of the non-product extension of A17.6 (§4.11): the attributions "Bennett 1962 /
Hoeffding 1963" and "Efron–Stein" are confirmed against sources read in full, and a certified second-order
bound in free-energy perturbation was not found (one candidate paper, Decoster 2004, could not be opened).

**Not done.**  The original of Dagum–Karp–Luby–Ross could not be opened (eight routes tried); it is
positioned through three papers that restate its theorems.  Zwanzig (1954), Specht (1960),
Bahadur–Savage (1956), Lu–Kofke I (2001), Dagum–Luby (1997), Lilien et al. (2005) and the later K\*
papers were not read beyond abstracts or records.  The property-testing / interactive-proof
literature on "verification is cheaper than estimation" was searched once, not read.  The proofs
of the theory division's §11.30 do not exist in the export, so T3's lower bound was compared as a
statement, not as a proof.  For the second addition, Bennett (1962), Decoster (2004), Külske (2003) and
Marton's papers were not opened.  The complete list is at the end ("What I could not access").

---

## 1. Verdicts

**In one paragraph.**  No mathematical statement among the six is contradicted by the literature; one
slogan is (T4's "the floor is the one assumption sampling cannot replace" — by the heavy-tail
literature and by our own O1); and nearly everything is already in the literature.  **T1** is in print as stated: the upper half *before* the maximisation over
the mean is inequality (4.12)–(4.13) of Hoeffding's 1963 paper — with the same letter `L` — and its
maximum over the mean is the logarithm of **Specht's ratio** (the sharp reverse arithmetic–geometric
mean inequality, 1960), which is also the "maxkl" of bounded-range mechanisms in differential
privacy (2020), where the two laws are Gibbs measures.  **T2** is the stopping criterion of the K\*
family of provable partition-function algorithms (2005/2008) specialised to a constant floor; the
closed form `q*` is two lines.  **T3** was not found as a theorem about hinted query complexity, but
its framework is Aaronson's randomised certificate complexity (2002), its cost quantity `Z(lo)/Z(g)`
is the sample-size parameter of "probabilistic variational bounds" for graphical models (Liu–Fisher–
Ihler 2015) and the `1/(εμ)` term of the optimal stopping-rule theorem (Dagum–Karp–Luby–Ross 2000, read
through restatements), and its count is that of the one-sided guarantee "no mass was missed" in
Block–Shetty (2026, Theorem 6) — where it is obtained **without a hint**; at the centre of a constant
box a hint saves nothing (A3.3).  **T4** is, sentence by sentence, in print: the cheap side is
Jensen/Markov (stated for partition functions by Grosse–Ghahramani–Adams 2015 and by Gogate–Bidyuk–
Dechter, arXiv:1206.5242), the bracket "width from the sample variance, validity from the bound on the weights" is
Corollary 3.2 of Liu–Fisher–Ihler, and "sampling cannot replace an a-priori bound" is the
Bahadur–Savage theorem (1956; not opened) — but the literal "the floor is the *one* assumption"
is contradicted by the heavy-tailed mean-estimation literature, which is exactly the content of
our **O1**.  And **O1 is in print in its unhinted form**: Block & Shetty, *Partition Function Estimation
under Bounded f-Divergence*, arXiv:2602.23535 (26 February 2026), prove `n ≍ γ_f(D_f/ε)/ε ∨ χ²/ε²` with
matching lower bounds (their Theorems 5 and 8, Propositions 1–2; constants and logarithms omitted) —
`e^{D_p}ε^{−p/(p−1)}` for Rényi order `1 < p ≤ 2`, `ε^{−2}` beyond, `exp(Θ(D_KL/ε))/ε` for Kullback–Leibler,
impossibility for total variation — and a one-sided estimator whose cost is
A17's "with a hint" column for every `p > 1`; earlier, Kunsch–Novak–Rudolf (2019) have the same
exponents `max{2, q/(q−1)}` with lower bounds for all randomised algorithms using function values.
**O2** is a two-line corollary of two statements of the differential-privacy literature and can be
improved from `p²K/(8(p−1))` to `(p−1)K/8 + Σ_i L(c_i) ≤ pK/8` (so `D_2 ≤ K/4`).

| # | statement | classification | most important source (reading level) | what is *not* in print, as far as read |
|---|---|---|---|---|
| T1 | `−E_π r ≤ ln Z(g) − ln Z(ĝ) ≤ −E_π r + L(w)`, two-point law extremal, `L ≤ w²/8` | **(1) in print as stated** | Hoeffding 1963, eqs. (4.12)–(4.15) `[full text, scanned]`; Specht's ratio as quoted by Fujii–Lee–Seo 2002 `[full text]`; `maxkl` in Dong–Durfee–Rogers, arXiv:1909.13830 `[full text]` | nothing; the name "Specht's ratio" and the sharper mean-dependent bound are missing from our texts |
| T2 | range of `ln Z` after evaluating `Q`; `q*` at the centre | **(2) known special case** (bracket and stopping rule); necessity half **(3)** | Georgiev–Lilien–Donald 2008, Proposition 3 `[full text, PMC]` | the closed form `q*` with a ceiling; the statement that less coverage certifies nothing (elementary) |
| T3 | hinted cost `Θ((Z(lo)/Z(g) − 1)/ε)`; dip/bump-weighted spot check; packing lower bound; centre `Θ((e^{ρ₋}−1)/ε)` | **(2) direct corollary** for the cost law and both mechanisms; **(4) not found** as a theorem on hinted query complexity of a box class | Liu–Fisher–Ihler 2015, Prop. 3.1, Cor. 3.2 `[full text]`; Aaronson, arXiv:quant-ph/0210020, Def. 3, Lemma 5 `[full text]`; Block–Shetty, arXiv:2602.23535, Thm 6, Thm 8 `[full text]` | instance-wise two-sided statement with a hint in the query model; the factor `(1 − μ′)`; the dip-weighted sampler |
| T4 | lower bound = a mean, `w² ln(1/δ)/(2ε²)`; upper bound `e^{ρ₋}`; "the floor is the one assumption sampling cannot replace"; unhinted bracket | **(2)**; the unhinted bracket **(1)**; the slogan **(3)** and too strong | Liu–Fisher–Ihler 2015, Cor. 3.2 `[full text]`; Grosse–Ghahramani–Adams, arXiv:1511.02543, §4 `[full text]`; Bahadur–Savage 1956 via Wang–Ramdas `[full text of the secondary source]` | a query-complexity statement of the asymmetry for free energies |
| O1 | Rényi balls: hinted cost `Θ(e^{κ}/ε^{p/(p−1)})`; without a hint `ε^{−max(2, p/(p−1))}`; KL: `exp(Θ(κ/ε))`; moments of `r` useless | A17.3, A17.4: **(1) in print** (unhinted, sampling model); A17.2 (hinted): **(2) direct corollary**; A17.5(ii): **(3)** | Block–Shetty, arXiv:2602.23535, Thms 5, 6, 8, Props 1–2 `[full text]`; Kunsch–Novak–Rudolf, arXiv:1805.08637, Thms 3.9, 3.10, Cor. 3.14 `[full text]` | reading the one-sided cost as a *verification* cost; finite spaces with atoms; explicit constants |
| O2 | product reference: `D_p ≤ p²K/(8(p−1))`, `D_2 ≤ K/2` | **(2) direct corollary**, and improvable to `pK/8` | Cesar–Rogers, arXiv:2004.07223, Lemma 3.2 `[full text]`; Bun–Steinke, arXiv:1605.02065, Lemma 2.2 `[full text]` | the application to remainders of a force field |
| A17.7 | Bennett bracket: floor `b` below the mean and variance `σ²` ⇒ Jensen gap `≤ ln[(b²e^{−σ²/b} + σ²e^b)/(b²+σ²)] ≤ (σ²/b²)(e^b − 1 − b)`; `Var ≤ ¼Σc_i²` | the inequality, its extremal law and both attributions: **(1) in print as stated**; its use as a certified second-order bound in free-energy perturbation: **(4) not found** | Hoeffding 1963, Thm 3, (2.8)–(2.10) `[full text, scanned]`; Fan–Grama–Liu, arXiv:1109.4359, eq. (3), Lemma 3.1 `[full text]`; van Handel's lecture notes, Thm 2.3, Cor. 2.4 `[full text]` | a rigorous second-order bound from the reference ensemble alone, in the sources retrieved (Delle Site–Hartmann 2024 `[full text]`: the second-order truncation is no bound); Decoster 2004, which claims rigorous higher-order bounds, was not accessible |
| A17.6, non-product reference | (asked for: one citable statement with its constant) | **(2)**: `D_p ≤ p²‖D‖²K/(8(p−1))` follows from a theorem in print | Chazottes–Collet–Külske–Redig, arXiv:math/0503483, Thm 1 with (9)–(10) `[full text]`; Kontorovich–Ramanan (Ann. Probab. 2008), Thm 1.2 `[full text]` | the sharp constant `p/8` (needs the conditional free energy of the remainder) |

Additional items of A17: the direction of the divergence ("every row is `D(π_g‖π)`") is **(1) in
print** — Jarzynski 2006, eq. (45), as an estimate; Chatterjee–Diaconis 2018, Theorem 1.1, as a
theorem at one instance; Minka 2005 for "exclusive divergences exclude parts of the target".

---

## 2. Precise statements, with proofs or counterexamples

Notation of A17: `X` finite, `π ∝ e^{−ĝ}`, `r = g − ĝ`, `Y = e^{−r}`, `μ = E_π Y = Z(g)/Z(ĝ)`, `π_g = πY/μ`;
`w = osc(r)`; `L(w) = ln((e^w − 1)/w) − 1 + w/(e^w − 1)`.  Statements A3.1–A3.4 are mine; none is deep, and
A3.1, A3.2, A3.4 are corollaries of results in print (the sources are named in each).  Nothing here is
machine-checked.  **No counterexample to T1–T4 or O1–O2 was found.**

### A3.1 T1's constant, in four equal forms; a sharper bound when the mean is known  [P; checked numerically, C1–C3, C8]

For `w > 0`:

    L(w)  =  max_{0≤t≤1} [ ln(1 − t + t e^w) − t w ]          (two-point law; maximiser t = 1/w − 1/(e^w − 1))
          =  ln S(e^w),     S(h) = (h − 1) h^{1/(h−1)} / (e ln h)        (Specht's ratio)
          =  a − 1 − ln a,  a = w/(1 − e^{−w})                           (bounded-range form)
          =  sup { KL(P‖Q) : osc ln(dP/dQ) ≤ w }  =  sup { KL(Q‖P) : osc ln(dP/dQ) ≤ w }.

*Proof.*  The first line is calculus (set the derivative `(e^w − 1)/(1 + t(e^w − 1)) − w` to zero).  For the
second, `ln S(e^w) = ln(e^w − 1) + w/(e^w − 1) − 1 − ln w`.  For the third, `w/(e^w − 1) = a − w` and
`ln((e^w − 1)/w) = w − ln a`.  For the last, `KL(Q‖P) = ln E_Q e^{Y} − E_Q Y` with `Y = ln(dP/dQ)` up to a
constant, which is the Jensen gap of a variable of range `w`; and `KL(P‖Q)` is the same expression with
the roles of `P`, `Q` exchanged (`Q` is the tilt of `P` by `−Y`).  ∎

*Consequences.*  (a) Our own addendum A5 (`KL(μ‖ν) ≤ w²/8`) holds with `L(w)` in place of `w²/8`;
`L(w) = w − 1 − ln w + o(1)` for large `w`, so the improvement is from quadratic to linear
(`L(8) = 4.92` against `8`; `L(20) = 16.0` against `50`).  (b) **A sharper bound than T1 is in Hoeffding's
proof**: for a law of `−r` on an interval of length `w` with mean position `p = (max r − E_π r)/w`,

    ln Z(g) − ln Z(ĝ) + E_π r  ≤  −w p + ln(1 − p + p e^w)   ≤  L(w)   ≤  w²/8,

the first inequality being Hoeffding's (4.12)–(4.13) (Lemma 1, the chord bound), the second the
maximisation over `p`, the third his (4.15).  Since `E_π r` is estimated anyway and `max r ≤ hi` is known
on a box, the first bound is available at no cost; on random laws its median is `0.77·L(w)` (C8).

### A3.2 A17.6 sharpened: on a product reference `D_p(π_g‖π) ≤ (p − 1)K/8 + Σ_i L(c_i) ≤ pK/8`  [P; checked numerically, C4–C5]

Let `π = ⊗_i π_i` be a product measure, `r` with one-site oscillations `c_i`, `K = Σ_i c_i²`.  Then for every
`p > 1`

    D_p(π_g ‖ π)  ≤  Σ_i [ (p − 1) c_i²/8 + L(c_i) ]  ≤  p K / 8 ,       and      KL(π_g‖π) ≤ Σ_i L(c_i) ≤ K/8 .

In particular `D_2 ≤ K/4` (A17.6 has `K/2`), and the factor between A17.6's bound `p²K/(8(p−1))` and this one is
`p/(p − 1)`: 2 at `p = 2`, unbounded as `p → 1`, where A17.6 diverges and this bound tends to the classical
`K/8`.  It is asymptotically attained (`K → 0`) by additive remainders on the uniform cube, where A17.6
notes `D_2 ≈ K/4`.

*Proof.*  (i) *One site.*  If `P = Q e^{−ρ}/E_Q e^{−ρ}` with `osc ρ ≤ c`, then `Λ := ln(dP/dQ)` has range `≤ c`, so
by Hoeffding's lemma under `P`, `ln E_P e^{(p−1)(Λ − E_P Λ)} ≤ (p−1)²c²/8`, and `E_P Λ = KL(P‖Q) ≤ L(c)` by A3.1.
Hence `D_p(P‖Q) = (p−1)^{−1} ln E_P e^{(p−1)Λ} ≤ (p−1)c²/8 + L(c)`.  (ii) *Conditionals are one-site tilts.*
`π_g(x_i | x_{<i}) ∝ π_i(x_i) ψ_i(x_{≤i})` with `ψ_i = E_{π_{>i}} e^{−r(x_{≤i}, ·)}`, and `ψ_i(x_{<i}, a)/ψ_i(x_{<i}, b) ∈ [e^{−c_i}, e^{c_i}]`
because `r` changes by at most `c_i` when `x_i` changes with the other coordinates fixed.  (iii) *Chain rule.*
`E_π (dπ_g/dπ)^p = E_π Π_i ρ_i^p` with `ρ_i` the conditional density ratios; integrating out the last
coordinate first, `E_{π_n}[ρ_n^p | x_{<n}] ≤ exp((p−1)[(p−1)c_n²/8 + L(c_n)])` for every `x_{<n}`, and induction gives
the sum.  ∎

*Where it is in print.*  Step (i) is "an α-bounded-range mechanism is `(ξ, α²/8)`-zCDP with
`ξ = α/(e^α−1) − 1 − ln(α/(e^α−1)) − α²/8 ≤ 0`" (Cesar–Rogers, arXiv:2004.07223, Lemma 3.2 and the sentence
after Lemma 3.4 `[full text]`); step (iii) is the composition property of Rényi divergence,
`D_α(P‖Q) ≤ D_α(P′‖Q′) + max_x D_α(P′_x‖Q′_x)` (Bun–Steinke, arXiv:1605.02065, Lemma 2.2 `[full text]`, who refer
to van Erven–Harremoës for the proof).  Step (ii) is the dictionary: *the conditional law of site `i`
in the true ensemble, given the earlier sites, is a `c_i`-bounded-range "mechanism" relative to the
model*.  (The Kullback–Leibler chain rule with conditionals of bounded range is also the first step of
our Proposition A1.1, workstream A1.)

*Remark (general reference measure) [P; checked numerically, C5, last block].*  Only step (ii) uses the
product structure.  For an arbitrary model `π` on a product space, with sites taken in any fixed order,
the same proof gives

    D_p(π_g ‖ π)  ≤  Σ_i [ (p − 1) c̃_i²/8 + L(c̃_i) ],      c̃_i := sup_{x_<i} osc_{x_i} F_i(x_≤i),   F_i := −ln E_π[ e^{−r} | x_≤i ],

where `F_i` is the conditional free energy of the remainder given the first `i` sites.  For a product `π`,
`c̃_i ≤ c_i`; for a model with interactions `c̃_i` also contains the influence of site `i` on the later sites and
is not bounded by `c_i` (§5, item 6).

*Consequence for A17.6's reading.*  The certified-reweighting cost becomes `e^{K/4}/(δ s_ε²)` instead of
`e^{K/2}/(δ s_ε²)`: "`c_i ≈ 1 k_BT` is not within reach beyond about 30 sites (`e^{15}`)" becomes about 60
sites for the same budget.  The qualitative conclusion (polynomial iff `K` bounded) is unchanged.

### A3.3 At the centre of a constant box the hint is worth nothing; in general it removes exactly the variance term  [P for (a); K (through restatements) for (b); checked numerically, C6–C7]

(a) Let the class be the box `−ρ₋ ≤ r ≤ ρ₊` and fix the detection threshold `η`.  *Rule:* draw points from
`π`, evaluate `r`; let `v` be the first value; if the first `N(v) := ⌈ln(1/δ)/q(v)⌉ + 1` values all equal `v`,
with `q(v) := min{(e^η − 1)/(e^{ρ₋+v} − 1), 1 − e^{−η}}`, output `ln(Z(g)/Z(ĝ)) = −v`.  Then **for every member of
the box** the probability that the rule outputs a value off by more than `η` is at most `δ`; at the
centre `r ≡ 0` it stops after `N(0) = ⌈ln(1/δ)(e^{ρ₋} − 1)/(e^η − 1)⌉ + 1` evaluations (when `e^{ρ₋} ≥ 1 + e^η`;
in `q(v)` the first term is read as `+∞` at `v = −ρ₋`).
*Proof.*  Let `p_v = π{r = v}`.  If `ln μ + v > η` then `(1 − p_v)(e^{ρ₋} − e^{−v}) > (e^η − 1)e^{−v}`; if
`ln μ + v < −η` then `1 − p_v > 1 − e^{−η}`.  So for a value `v` at which the output would be wrong,
`1 − p_v > q(v)`, and the rule outputs `−v` with probability `p_v·p_v^{N(v)−1} ≤ p_v δ`.  Sum over `v`.  ∎
With the theory division's own numbers (`ρ₋ = ρ₊ = 3`, `ε = 0.2` i.e. `η = 0.1`, `δ = 0.05`): **545 evaluations
without a hint**, against the 1088 they quote for the hinted spot check (their count carries a factor
2 from mixing the dip and the bump sampler half and half; at the centre both are `π`).

(b) In general, sample the floor measure `π_lo ∝ e^{−ĝ−lo}` and put `X = e^{−(r−lo)} ∈ (0, 1]`, so that
`E X = μ′ = Z(g)/Z(lo)`.  The optimal stopping-rule theorem for `[0,1]`-valued variables (Dagum–Karp–Luby–
Ross; statement as restated by Mnih–Szepesvári–Audibert 2008, §3 `[full text of the restatement]`) gives an
`(ε, δ)` estimate from `C·max(σ_X², εμ′)·ln(2/δ)/(εμ′)²` samples and shows that no stopping rule does
better up to a constant, for every such variable.  T3's hinted cost is `(1 − μ′)/(εμ′)`.  Hence

    hinted (T3):   (1 − μ′)/(ε μ′)        unhinted, sampling model:   max(σ_X², ε μ′)/(ε μ′)²     (constants, ln(1/δ) omitted)

and the two agree up to a constant exactly when `σ_X² ≲ εμ′` — at the centre `σ_X = 0` — while in the
worst case `σ_X² = μ′(1 − μ′)` (two-valued remainder) the ratio is `1/ε` (C6).  **So "with a hint" in T3
is needed only where the remainder varies on the bulk of the floor ensemble, and what the hint buys
is the variance term of a known theorem.**

### A3.4 Dictionaries (no new mathematics)  [K]

(a) *T3 as a randomised certificate complexity.*  In Aaronson's Definition 3 a "randomized verifier for
input X" accepts `X` with probability 1 and rejects every `Y` with `f(Y) ≠ f(X)` with probability `≥ ½`;
`RC^X(f)` is its least expected number of queries; by his Lemma 5 non-adaptive verifiers that query
coordinate `i` with probability `λ_i` and reject on a disagreement achieve `Θ(RC^X)` with cost `Σλ_i`.
With coordinates = states, input = the remainder, `f` = "`ln Z` up to `ε`", the sensitive blocks at `r`
are the sets `D` whose dip weight exceeds `(e^ε − 1)Z` or whose bump weight exceeds `(1 − e^{−ε})Z`; the
covering programme `min Σλ_x` s.t. `Σ_{x∈D} λ_x ≥ 1` for all sensitive `D` has the feasible point
`λ_x = dip(x)/((e^ε−1)Z) + bump(x)/((1−e^{−ε})Z)` of cost `U/((e^ε−1)Z) + V/((1−e^{−ε})Z)`, and disjoint blocks of dip
weight in `((e^ε−1)Z, 2(e^ε−1)Z]` give the matching packing when no state is that heavy.  This is T3 with its
sampler; "with a hint" *is* the randomised verifier, and the theory division's own prior-art note L7
already names fractional block sensitivity for its general lower bound (at search-summary level; the
definition and Lemma 5 are now read in full).  *Remark on wording:* the feasible point shows that the
cost is `Θ((Z(lo)/Z − 1)/ε + (1 − Z(hi)/Z)/ε)`; the headline `Θ((Z(lo)/Z − 1)/ε)` drops the bump term, which is
at most `1/(1−e^{−ε})` but is the whole cost near the floor (at `r = lo` the headline reads 0).

(b) *A17 against Block–Shetty.*  `μ ↔ π`, `ν ↔ π_g`, `λ ↔ Y`, `Z ↔ μ`; `D_f` with `f(t) = t^p − pt + p − 1` is
`e^{(p−1)D_p} − 1` (my computation); `γ_f(M) ≍ M^{1/(p−1)}`.  Their two-sided cost `γ_f(D_f/ε)/ε ∨ χ²/ε²` is A17's column "without a
hint"; their one-sided cost (Theorem 6: `(1−ε)Z ≤ Ẑ ≤ M·Z` from `log(1/δ)·γ_f(6D_f/ε)/ε` samples) is A17's column
"with a hint", `e^{D_p}ε^{−p/(p−1)}`, for every `p > 1`; the lower-bound instance of their Theorem 8 (density
ratio `1 − ε` off a set of mass `p`, `1 + ε(1/p − 1)` on it, against the constant ratio 1) is the alternative of
A17.2(ii)/A17.4(ii) at the centre.  *What the hint means in their terms:* it replaces their loose upper
tail `Ẑ ≤ M·Z` by the claimed value, so that the one-sided cost becomes the whole cost.

(c) *Certification against approximate sampling.*  The same extremal pair (a set of base mass `q`
carrying target mass `≈ ε`) costs `1/q` to *detect* and `ε/q` to *select with the right frequency*; hence
"cost of certifying `ln Z`" `= ε^{−1} ×` "cost of an `ε`-approximate sample", for Rényi orders
(`e^{D_p}ε^{−p/(p−1)}` against `e^{D_p}ε^{−1/(p−1)}`, Block–Polyanskiy 2023, Example 7) — in print as Block–Shetty's
§3.3 ("at least an ε⁻¹ factor … 'counting' … is strictly harder than … 'sampling'").

---

## 3. Numerics

One script, `experiments/science/ws_A3/check_math.py` (numpy + mpmath; under a minute; run
`python3 -W error check_math.py > check_math.out`).  It checks only the identities and inequalities of §2;
it is not evidence about the literature.

| check | what | size | result |
|---|---|---|---|
| C1 | four forms of `L(w)`; `ln cosh(w/2) ≤ L(w) ≤ w²/8`; large-`w` asymptote | `w ∈ [0.01, 30]` and a grid of 6 000 points to 60 | forms agree to `1.3·10⁻⁹` (one of them is a grid maximum); inequalities hold; `L(w) − (w − 1 − ln w) = 3·10⁻¹²` at `w = 30` |
| C2 | `ln E e^Y − E Y ≤ L(w)` | 40 000 random laws, 2–8 atoms | largest ratio 1.000000; the two-point law with mass `1/w − 1/(e^w−1)` attains it to 12 digits |
| C3 | both Kullback–Leibler divergences between a law and its tilt `≤ L(w)` | 40 000 random pairs | largest ratios 1.000000 and 1.000000 |
| C4 | tilt lemma `D_α ≤ αw²/8` | 60 000 random tilts, `α ∈ {1, 1.01, 1.5, 2, 3, 5, 10}` | largest ratio 0.9994; numerical two-point suprema tabulated (e.g. `α = 2`, `w = 3`: 0.76 of the bound) |
| C5 | A3.2 on product measures: `D_p ≤ (p−1)K/8 + Σ L(c_i) ≤ pK/8`, against A17.6's `p²K/(8(p−1))` | 1 200 members (additive, inf-convolution, hockey-stick, distance functions) on `{0,1}^n`, `n ≤ 8`, and `{0,1,2}^n`, `n ≤ 5`, random product measures, exact enumeration; 7 hill-climbs | largest `D_p/(pK/8)`: 0.989 (`p = 1`), 0.976 (`p = 2`), 0.947 (`p = 6`); refined bound: 0.993, 0.977, 0.948; A17.6's bound: 0.0098 (`p = 1.01`), 0.488 (`p = 2`), 0.789 (`p = 6`); hill-climbs approach 1 from below (0.99995), confirmed with 50 digits |
| C5, last block | the remark after A3.2: `D_p ≤ Σ_i[(p−1)c̃_i²/8 + L(c̃_i)]` for a **non-product** reference | 240 random pairs (`π`, `r`) on `{0,1}^n`, `n = 3…6`, exact enumeration | largest ratio 0.74 (never violated) |
| C6 | T3's count is `ε` × the largest variance term of a `[0,1]` variable with the same mean | 4 parameter pairs | exact |
| C7 | A3.3(a): exact worst-case failure probability of the no-hint rule over two- and three-level alternatives; the theory division's example | 3 parameter triples; `2001 × 41` alternatives each | failure probabilities 0.048, 0.029, 0.006 (`≤ δ`); **545** evaluations without a hint against **1088** quoted for the hinted spot check |
| C8 | Hoeffding's mean-dependent bound | 19 467 random laws (533 nearly degenerate ones skipped) | never violated; median 0.77 of `L(w)` |
| C9 | §4.11: for a two-state Markov-chain reference with contraction `θ`: `ln E e^{λ(r−Er)} ≤ λ²K/(8(1−θ)²)`, `D_p ≤ p²K/(8(p−1)(1−θ)²)`, `Var ≤ K/(1−θ)²`; and Bennett's sharp two-point bound `W(b, σ²)` of A17.7 | 120 random chains (`n = 5, 7, 9`) with random `r`, exact enumeration; 20 000 random laws | never violated (largest ratios 0.10, 0.06, 0.02 — loose for random `r`); Bennett: largest gap/`W` = 1.000000, attained; `W ≤ ln(1 + (σ²/b²)(e^b − 1 − b)) ≤ (σ²/b²)(e^b − 1 − b)` always; with a floor and a variance bound that are not tight, gap/`W` ≤ 0.990; the lower half of §4.11(c′): largest ratio 0.99998 |

*Two lessons recorded.*  The first version of the hill-climb in C5 "found" ratios up to 1.16 and the
first version of C8 a ratio 1.001: both were rounding noise at scales where `D_p` (a difference of
nearly equal numbers) is of the order `10⁻¹³`; sixty-digit arithmetic gave ratios `0.9999…`.  The script now
refuses `K < 10⁻³`, skips nearly degenerate laws, and re-evaluates the best point of each climb with 50
digits.  A violation reported by a floating-point search of an inequality that is tight at zero is
not a counterexample until it survives high precision.

---

## 4. Prior art, statement by statement

For each statement: the statement; the closest statements in print, quoted or paraphrased closely
with the reading level; the comparison of hypotheses, quantifiers and conclusions; the classification;
and the sentence to write.

### 4.1 T1 — the Jensen bracket with the sharp constant

*Statement.*  For `r = g − ĝ` with oscillation `w`: `−E_π r ≤ ln Z(g) − ln Z(ĝ) ≤ −E_π r + L(w)`,
`L(w) = ln((e^w − 1)/w) − 1 + w/(e^w − 1) ≤ w²/8`; the two-point law is extremal.

*In print.*

(a) **Hoeffding, "Probability inequalities for sums of bounded random variables", American Statistical
Association Journal, March 1963** (Crossref record: J. Amer. Statist. Assoc. 58(301), 13–30)
`[full text: pp. 13–14, 20–22, scanned]`.  "Lemma 1. If X is a random variable such that a ≤ X ≤ b, then for
any real number h, `E e^{hX} ≤ ((b − EX)/(b − a)) e^{ha} + ((EX − a)/(b − a)) e^{hb}`" (4.2); and in the proof of
Theorem 2: "`E e^{h(X_i − μ_i)} ≤ e^{−hμ_i}(…) = e^{L(h_i)}` (4.12), where `L(h_i) = −h_i p_i + ln(1 − p_i + p_i e^{h_i})` (4.13),
`h_i = h(b_i − a_i)`, `p_i = (μ_i − a_i)/(b_i − a_i)` (4.14) … `L″(h_i) ≤ ¼`.  Therefore by Taylor's formula
`L(h_i) ≤ … = ⅛h²(b_i − a_i)²` (4.15)".  With `X = −r`, `h = 1` this is the upper half of T1 with the *mean-dependent*
constant `−wp + ln(1 − p + pe^w)`, whose maximum over `p` is `L(w)` (A3.1).  Even the letter is the same.

(b) **Specht's ratio.**  Fujii, Lee, Seo, "An application of the Mond–Pečarić method to operator convex
functions", RIMS Kôkyûroku 1259 (2002) 1–10 `[full text: pp. 1–2]`: "In 1960 as a converse of the
arithmetic-geometric mean inequality, W. Specht [11] estimated the upper bound of the arithmetic mean by
the geometric one for positive numbers: For `x_1, …, x_n ∈ [m, M]` with `M ≥ m > 0`,
`(x_1⋯x_n)^{1/n} ≤ (x_1 + ⋯ + x_n)/n ≤ M_h(1)(x_1⋯x_n)^{1/n}`, where `h = M/m` … and the Specht ratio `M_h(1)` is defined
for `h ≥ 1` as `M_h(1) = (h − 1)h^{1/(h−1)}/(e log h)`"; and "J.I. Fujii, S. Izumino and Y. Seo [1] showed an
operator version of Specht's theorem (1): Let A be a positive operator on a Hilbert space H satisfying
`0 < m ≤ A ≤ M` … Then `(Ax, x) ≤ M_h(1) exp(log A x, x)` holds for every unit vector x".  For a diagonal `A`
with entries `e^{−r(s)}` and `x = √π` this reads `E_π e^{−r} ≤ S(e^w)·exp(−E_π r)` for **every** `π` — T1's upper
half, word for word, with `ln S(e^w) = L(w)` (C1).  Also Furuichi, arXiv:1004.0581v3 `[full text: p. 1,
Lemma 2.1]`: the two-point weighted form `S(a/b)·a^{1−ν}b^ν ≥ (1 − ν)a + νb`, attributed to Tominaga, Sci. Math.
Japon. 55 (2002) 583–588, with `S(h) = S(1/h) > 1`.  Specht's own paper (Math. Z. 74(1), 91–98, 1960, per the
Crossref record) was not opened.

(c) **Differential privacy.**  Dong, Durfee, Rogers, "Optimal differential privacy composition for
exponential mechanisms and the cost of adaptivity", arXiv:1909.13830v2 `[full text: Def. 2.2, Cor. 2.1,
Thm 1, Lemma 4.1, appendix]`.  A mechanism is `ε`-bounded-range if the log-ratio of the two output laws
lies in `[t − ε, t]` for some `t ∈ [0, ε]`; "The exponential mechanism is ε-DP.  Further, the exponential
mechanism is ε-BR"; every `ε`-BR pair is a post-processing of a two-point "generalized random
response" (Lemma 4.1); and "`KL(Bern(q_{ε,t})‖Bern(p_{ε,t})) = t − (ε/(e^ε − 1))(e^t − 1)`.  A bit of calculus shows
the above expression is maximized at `t = ln((e^ε − 1)/ε)`, and the value is
`maxkl(ε) := ε/(e^ε − 1) − 1 − ln(ε/(e^ε − 1))`".  `maxkl(w) = L(w)`.  The exponential mechanism samples `y` with
probability `∝ exp(εu(x, y)/(2Δu))`: two Gibbs measures whose energies differ by a function of bounded
oscillation — T1's setting exactly, in another vocabulary.

(d) **f-divergence ranges.**  Binette, arXiv:1805.05135v2 (doi:10.1109/TIT.2019.2896192 on the PDF) `[full
text: abstract, Thm 1, Cor. 2]`: "`sup_{(P,Q)∈B(m,M)} D_f(P‖Q) = ((M − 1)f(m) + (1 − m)f(M))/(M − m)`" for likelihood
ratios between `m` and `M`; with `f = −log`, `M/m = e^w`, the maximum over `m` is `L(w)` (my calculus, C3).

(e) *What it is not.*  The Kearns–Saul inequality — `(1 − p)e^{−tp} + pe^{t(1−p)} ≤ exp((1 − 2p)t²/(4 log((1 − p)/p)))`,
"optimal in the sense that, for every p, there is a t for which equality is achieved" (Berend–Kontorovich,
arXiv:1210.3248v1 `[full text: §1, Thm 4]`) — is the sharp sub-Gaussian constant at fixed `p`, the supremum
over `t`; T1's `L(w)` is the supremum over `p` at fixed `t`.  Bentkus, "On Hoeffding's inequalities"
(arXiv:math/0410159; Ann. Probab. 32 (2004) 1650–1673 per the arXiv record) concerns tail probabilities; not
read.

(f) *Lower half.*  Jensen's inequality; "Gibbs–Bogoliubov" in statistical mechanics (named in the
abstract of Lu–Adhikari–Kofke 2003, below) and "`ELBO ≤ log p(x)`" in variational inference (Dieng et al.,
arXiv:1611.00328v4, Theorem 1 `[full text]`).  I did not open a primary source for the name.

*Comparison.*  Same hypotheses (a variable with values in an interval of length `w`; no other
assumption), same quantifier (every law), same conclusion and constant, same extremal law.
**Classification: (1) in print as stated.**

*Sentence to write.*  "The left inequality is Jensen's (Gibbs–Bogoliubov).  The right one is Hoeffding's
bound on the moment generating function of a bounded variable (Hoeffding 1963, Lemma 1 and eqs.
(4.12)–(4.13)) maximised over the mean; the maximum `L(w) = ln S(e^w)` is the logarithm of Specht's ratio, the
sharp constant in the converse of the arithmetic–geometric mean inequality (Specht 1960; weighted form:
Fujii–Izumino–Seo 1998, as quoted in Fujii–Lee–Seo 2002), and equals the largest Kullback–Leibler
divergence of a bounded-range pair in differential privacy (Dong–Durfee–Rogers 2020).  When `E_π r` is
known the mean-dependent bound `−wp + ln(1 − p + pe^w)`, `p = (max r − E_π r)/w`, is sharper."

### 4.2 T2 — deterministic certificates on a box

*Statement.*  After evaluating `Q` the range of `ln Z` is from "ceiling off `Q`" to "floor off `Q`"; at the
centre of a constant box a certificate of width `ε` must cover all but
`q* = (e^ε − 1)/(e^{ρ₋} − e^{ε−ρ₊} + e^ε − 1)` of the mass of `π`.

*In print.*  According to PubMed: Georgiev, Lilien, Donald, "The minimized dead-end elimination
criterion and its application to protein redesign in a hybrid scoring and search algorithm for
computing partition functions over molecular ensembles", J Comput Chem 29(10):1527–42 (2008),
[doi:10.1002/jcc.20909](https://doi.org/10.1002/jcc.20909), PMC3263346 `[full text: §4, Proposition 3 and proof]`.
With `q*` the partial partition function of the `m` conformations enumerated so far, `n` conformations not
yet generated, all with energy lower bounds above `E_t`, `k` pruned conformations with lower bound `E_0`, and
`ρ = ε/(1 − ε)`: "Proposition 3.  If the lower bound B(c) on the minimized energy of the (m + 1)st
conformation returned by A* satisfies `B(c) ≥ −RT(ln(q*ρ − k exp(−E_0/RT)) − ln n)`, then the partition
function computation can be halted, with q* guaranteed to be an ε-approximation to the true partition
function q, that is, `q* ≥ (1 − ε)q`."  Proof: "`q = q* + q′ + p*` … `q ≤ q* + n exp(−E_t/RT) + k exp(−E_0/RT)`".  The
lower bounds are "a sum of precomputed pairwise minimum energy terms".  The algorithm it improves is, again
according to PubMed, Lilien, Stevens, Anderson, Donald, J Comput Biol 12(6):740–61 (2005),
[doi:10.1089/cmb.2005.12.740](https://doi.org/10.1089/cmb.2005.12.740) `[abstract]`: "an efficient deterministic
approximation algorithm, capable of approximating our scoring function to arbitrary precision".  Later
members of the family (according to PubMed; `[abstract]` only): Ojewole, Jou, Fowler, Donald, J Comput Biol
25(7):726–739 (2018), [doi:10.1089/cmb.2017.0267](https://doi.org/10.1089/cmb.2017.0267) (BBK\*); the MARK\* paper,
[doi:10.1089/cmb.2019.0315](https://doi.org/10.1089/cmb.2019.0315) (PMID 31855059; authors and year — Jou, Holt, Lowegard, Donald, 2020 — as in workstream P2's record of the same
entry; from the abstract retrieved by me: "provable ε-approximations to partition functions … by
computing provable, admissible pairwise-minimized energy lower bounds … and using the A* enumeration
algorithm"); Lowegard et al., PLoS Comput Biol 16(6):e1007447 (2020),
[doi:10.1371/journal.pcbi.1007447](https://doi.org/10.1371/journal.pcbi.1007447) ("Often, reaching an
ε-approximation … takes a prohibitive amount of time and space").  *(This literature is about sequence
design, which is outside our scope; it is cited only for the certificate scheme on one fixed-sequence
state, as in workstream P2.)*

*Comparison.*  Proposition 3 is T2 with a **function floor** (pairwise lower bounds `B`), **no ceiling**
(unevaluated weights are bounded below by 0), the unevaluated mass bounded by counting
(`n·e^{−E_t/RT}`), and a relative criterion `q* ≥ (1 − ε)q`.  T2 with `ρ₊ = ∞` is the same inequality:
`π(Qᶜ)e^{ρ₋} ≤ (e^ε − 1)π(Q)`.  In T2 and not in what I read of K\*: the ceiling term; the closed form at the
centre; the *necessity* ("must cover all but `q*`"), which is the elementary remark that unevaluated
points of a box are unconstrained — in information-based complexity the same fact is the entry
"deterministic: 1" (no rate) for summation over `L_p^N` balls (Heinrich–Novak, arXiv:quant-ph/0105114,
table `[full text]`).  In K\* and not in T2: the order of enumeration (A\*), pruning with a bound on the
pruned mass.  Not found in the K\* papers read: sampling with a certificate; any lower bound on the
number of evaluations.  **Classification: (2) known special case** (bracket and stopping rule); the
necessity half **(3)**.

*Sentence to write.*  "Statement (b) is the stopping criterion of provable ε-approximation algorithms
for partition functions in computational protein design (Lilien et al. 2005; Georgiev, Lilien and
Donald 2008, Proposition 3), specialised to a constant floor and completed by a ceiling; there the
floor is a pairwise lower bound of the energy and the unevaluated mass is bounded by counting."

### 4.3 T3 — the hinted (verification) cost

*Statement.*  With a hint, `Θ((Z(lo)/Z(g) − 1)/ε)` evaluations certify `ln Z` within `ε` (sampling in proportion
to the dip weight `w(e^{−lo} − e^{−r})` and the bump weight); matching lower bound for every randomised
algorithm by packing disjoint sets; at the centre of a constant box `Θ((e^{ρ₋} − 1)/ε)`, independent of the
size of the system.

*In print.*

(a) **Dagum, Karp, Luby, Ross**, SIAM J. Comput. 29(5), 1484–1496 (2000) `[record; original not accessed]`.
What I could read about it: (i) X. Chen, arXiv:0711.2801, Appendix D `[full text]`, reproduces with page
references the Stopping Rule Algorithm (sample until the sum reaches `Υ₁ = 1 + 4(e − 2)(1 + ε)ln(2/δ)/ε²`, output
`Υ₁/N`), the "Stopping Rule Theorem" (`Pr{|μ̂ − μ| ≤ εμ} ≥ 1 − δ`), and Lemma 4.6 with `ρ_Z = max{σ_Z², εμ_Z}`;
(ii) Mnih, Szepesvári, Audibert, "Empirical Bernstein stopping", ICML 2008, §3 `[full text]`: "Dagum et al.
(2000) prove that … if T is the number of samples taken by AA, then there exists a constant C such
that with probability at least 1 − δ, `T ≤ C·max(σ², εμ)·(1/(ε²μ²))·log(2/δ)`.  In addition, Dagum et al. prove
that if T is the number of samples taken by any (ε, δ)-stopping rule, then there exists a constant C′
such that with probability at least 1 − δ, `T ≥ C′·max(σ², εμ)·(1/(ε²μ²))·log(2/δ)`"; (iii) Karp, Luby, Madras,
J. Algorithms 10 (1989) 429–448 `[full text: theorem statement]`: "ZERO-ONE ESTIMATOR THEOREM.  Let
`μ = |G|/|U|`.  Let `ε ≤ 2`.  If `N ≥ (1/μ)·(4 ln(2/δ)/ε²)` then the Monte-Carlo algorithm described above is an (ε, δ)
approximation algorithm" (symbols restored by me from a poor OCR of the scan).  *The brief's question — is T3 the `1/(εμ)` term with `X = e^{−(r−lo)}` under the
floor measure?*  **Yes in value, with three qualifications** (A3.3): `E X = μ′ = Z(g)/Z(lo)` and
`1/(εμ′) = Z(lo)/(εZ(g))`, which is T3's count up to the factor `(1 − μ′)`; but (1) in the Dagum–Karp–Luby–Ross
model the algorithm sees i.i.d. copies of `X` only, has no hint, and the bound is for estimation, so it
carries the variance term as well; (2) where `σ_X² ≲ εμ′` — in particular at the centre of a constant box —
the *unhinted* stopping rule already costs `1/(εμ′)`; (3) T3 is cheaper than the sampling bound exactly
when `σ_X² ≫ εμ′`, by using the hint to replace estimation by detection.  One published caution: Chen
states that the proof of the second tail of the Stopping Rule Theorem "is not complete.  There exists a
significant gap which cannot be patched by using their argument", while the claim follows from Chen's
own sharper threshold.

(b) **Sampling with a certificate from an upper-bounding model.**  Liu, Fisher, Ihler, "Probabilistic
variational bounds for graphical models" (NeurIPS proceedings site, 2015 volume) `[full text: abstract,
§1, §3]`.  A convex variational bound `Z_trw ≥ Z` comes with a mixture-of-trees proposal that can be sampled
exactly and whose importance weights satisfy "`w(x) ≤ Z_trw(θ^T), ∀x ∈ X`" (Proposition 3.1); Corollary
3.2: with `Δ = √(2·v̂ar(w)·log(2/δ)/n) + 7·Z_trw·log(2/δ)/(3(n − 1))`, "`Ẑ₊ = Ẑ + Δ` and `Ẑ₋ = Ẑ − Δ` are upper and lower
bounds of Z with at least probability (1 − δ), respectively"; "one can apply a stopping criterion [e.g., 5,
20] on n to guarantee a relative error ε with probability at least 1 − δ, using the bound on w(x);
roughly, the expected number of samples will depend on `Z_trw/Z`, the relative accuracy of the variational
bound".  Dictionary: bounding model ↔ a *function* floor whose Gibbs measure is sampled exactly;
`Z_trw ↔ Z(lo)`; `Z_trw/Z ↔ Z(lo)/Z(g)`, T3's cost quantity.  Earlier in the same line, with a-priori bounds on
the weights of likelihood weighting ("local variance bound" `r`): "the Zero-One Estimator Theorem … can be
rewritten `N ≤ (4r^k/ε²) ln(2/δ)`" (Pradhan–Dagum, arXiv:1302.3598 `[full text, OCR]`, describing Dagum–Luby, Artificial
Intelligence 93 (1997) 1–27 `[record]`).

(c) **The one-sided count without a hint.**  Block & Shetty, arXiv:2602.23535v1, Theorem 6 `[full text]`: "there
is an estimator `Ẑ` such that for any `0 < ε < 1`, if `n ≳ log(1/δ)·M/ε` where `Cov_M(ν‖μ) ≲ ε`, it holds that with
probability at least 1 − δ that `(1 − ε)·Z ≤ Ẑ ≤ M·Z`."  For a density ratio bounded by `M₀` (a floor),
`Cov_M = 0` for `M > M₀`, so "no mass was missed up to `ε`" costs `log(1/δ)·M₀/ε` model samples — T3's count —
with no hint.  Their lower bound (Theorem 8, proof read) is the detection argument at the instance
with constant density ratio: "one must observe at least one sample from the high-density region …
which occurs with probability p under μ".

(d) **The framework of "with a hint".**  Aaronson, "Quantum certificate complexity", arXiv:quant-ph/0210020v1
`[full text: Defs 1–3, Prop. 4, Lemma 5]`: "A randomized verifier for input X is a randomized algorithm
that, on input Y ∈ Dom(f), (i) accepts with probability 1 if Y = X, and (ii) rejects with probability at
least 1/2 if f(Y) ≠ f(X) … `RC^X(f)` is the minimum expected number of queries used by a randomized verifier
for X"; Lemma 5: non-adaptive verifiers that query each coordinate with its own probability and reject
on a disagreement are optimal up to a constant; `RC(f) = Ω(bs(f))`.  T3 is the value of `RC^X` for weighted
approximate summation on a box (A3.4(a)).  The theory division's L7 cites this lineage for its general
lower bound (Theorem 11.22) at search-summary level; Tal, Gilmer–Saks–Srinivasan and Kulkarni–Tal were not
opened by me either.

(e) **The class-level, no-hint analogue.**  Mathé & Novak, arXiv:math/0611285v2 `[full text: class
definition, Thms 1–2]`: on `F_C = {(f, ρ) : ‖f‖_∞ ≤ 1, ρ(x)/ρ(y) ≤ C}`, every Monte Carlo method with `n` values has
error `≥ (√2/6)√(C/(2n))` (for `2n ≥ C − 1`) and simple Monte Carlo has error `≤ 2 min{1, √(2C/n)}`: "the
complexity of the problem is linear in C".  This is the published "exponential in the sup-norm bound,
independent of the dimension, hidden needles for the lower bound" — for expectations (ratios of
integrals), all algorithms, worst case over the class, with `C = e^{ρ₋+ρ₊}`.  For `ln Z` only the floor
enters; that one-sidedness is not in Mathé–Novak.

(f) **Physics.**  Yunger Halpern & Jarzynski, arXiv:1601.02637v2 (Phys. Rev. E 93, 052144 (2016) per the arXiv
record) `[full text]`: Theorem 1, "The number `N_δ` of reverse trials expected to be performed before one
trial outputs a `w^δ`-dominant amount `W ≥ w^δ` of work is bounded as `N_δ ≥ e^{β(w^δ − ΔF) + H^β_∞(P_fwd)}`", with
`H^β_∞(P) = −log(p_max/β)` the "thermal order-∞ Rényi entropy" of the forward work distribution — a
waiting-time bound for one rare value with a user-chosen threshold; their Theorem 2 is an "approximate
error bound" under the neglected-tail assumption.  It is the nearest physics statement to "the cost
is the inverse probability of the unseen dominant set", and it is not a statement about a class, a
certificate or a floor.  (My memory of it as an order-∞ Rényi *divergence* bound was wrong.)

*What the hint/verification counterpart is, in that literature.*  In the Dagum–Karp–Luby–Ross lineage: none
found (the restatements read contain no verification model).  In query complexity: Aaronson's
randomised verifier (d).  In machine learning: Grosse–Ghahramani–Adams (§4.4) use the word — "suppose we
are given a hint in the form of an exact posterior sample" — for a different object (a sample of the
target, which gives the *upper* bound by running the estimator in reverse).  In statistics: two-point
testing lower bounds (Devroye et al., Block–Shetty) are already "hinted" — both candidates are known —
which is why, in the sampling model, a hint cannot beat them.  In learning theory the counterpart has a
name, **PAC verification**: Goldwasser, Rothblum, Shafer, Yehudayoff, "Interactive proofs for verifying
machine learning", ECCC Report No. 58 (2020) `[abstract]`: "using a source of labeled data and interaction
with an untrusted prover, what is the complexity of verifying that a given hypothesis is 'approximately
correct'? … for a specific hypothesis class, verification is significantly cheaper than learning in terms
of the number of random samples required, even if the verifier engages with the prover only in a
single-round (NP-like) protocol … Third, we show that verification is not always more efficient"; and
Gur, Jahanara, Khodabandeh, Rajgopal, Salamatian, Shinkar, arXiv:2404.08158v1 `[abstract, Thm 1.4]`: "the
verifier uses at most O(1/ε) many random labeled examples".  A single-round protocol with an untrusted
prover is a hint in the theory division's sense (correct on every input, cheap when the hint is
right); the objects verified there are hypotheses and their losses, not sums of weights, and I read
abstracts only.  The parallel is nevertheless exact in one respect: "verification is not always more
efficient" there, and here the hint is worth nothing at flat instances (A3.3).

*Comparison.*  Known: the cost quantity `Z(lo)/Z(g)` (b); the count `M/ε` for excluding missed mass (a, c);
the verifier model and the covering/packing duality (d); needle lower bounds linear in the sup-ratio
(e).  Not found after the searches of §4.9 (queries W9, W12; arXiv API): the instance-wise two-sided
statement `Θ((Z(lo)/Z(g) − 1)/ε)` *with a hint in the query model*, the dip- and bump-weighted sampler, the
factor `(1 − μ′)`.  **Classification: (2) direct corollary** for the cost law and both mechanisms — two
lines: under the floor measure `X = e^{−(r−lo)} ∈ (0,1]` has mean `μ′`, and a set on which a member could raise
`Z` by a factor `e^ε` has floor-measure mass at least `(e^ε − 1)μ′` (dip-weighted mass at least
`(e^ε − 1)μ′/(1 − μ′)`); the hint supplies the value on what was seen, so no variance term is paid — and **(4) not found** as a theorem on hinted query complexity of box classes.

*Sentence to write.*  "With a hint the problem is the randomised certificate complexity of Aaronson
(2002), and the spot check is his non-adaptive verifier.  The cost `Z(lo)/Z(g)` — the Boltzmann factor of
the free-energy distance to the floor — is the sample-size parameter of importance sampling with
weights bounded by an upper-bounding model (Dagum–Luby 1997; Liu, Fisher and Ihler 2015, Proposition 3.1
and Corollary 3.2) and the second term of the optimal stopping-rule theorem of Dagum, Karp, Luby and
Ross (2000) applied to `e^{−(r−lo)}` under the floor measure; without a hint the same count certifies the
upper side alone (Block and Shetty 2026, Theorem 6), and at an instance where the remainder is constant
on the bulk the hint is not needed at all.  What a hint buys, in general, is the variance term.  On the
class `sup ρ/inf ρ ≤ C` the corresponding worst-case statement for expectations is Mathé and Novak (2007,
Theorems 1–2)."

### 4.4 T4 — the asymmetry

*Statement.*  The lower bound on `ln Z` (Gibbs–Bogoliubov, a mean) costs `w² ln(1/δ)/(2ε²)`; the upper bound
costs `e^{ρ₋}`; "the floor is the one assumption sampling cannot replace"; without a hint the same samples
give a bracket whose width is set by the sample variance and whose validity is paid for by the floor.

*In print — machine learning and graphical models.*

(a) Grosse, Ghahramani, Adams, "Sandwiching the marginal likelihood using bidirectional Monte Carlo",
arXiv:1511.02543v1 `[full text: §4]`.  Unbiased estimators of `Z` "are stochastic lower bounds, in two senses.
First, … Markov's inequality implies that `Pr(Ẑ > aZ) < 1/a` … `Pr(log Ẑ > log Z + b) < e^{−b}` (25) … The other
sense … follows from Jensen's inequality: `E[log Ẑ] ≤ log E[Ẑ] = log Z` (26)."  And: "Heuristically speaking,
we would expect good upper bounds to be harder to obtain than good lower bounds.  For a lower bound on
the log-ML, it suffices to exhibit regions of high posterior mass.  For an upper bound, one would have
to demonstrate the absence of any additional probability mass."
(b) Gogate, Bidyuk, Dechter, "Studies in lower bounding probability of evidence using the Markov
inequality", arXiv:1206.5242 `[full text: abstract, §2.2, §3]`: "high confidence lower bounds on probability
of evidence but does not have any guarantees in terms of relative or absolute error"; "The independence
from N allows us to use even a single sample to derive lower bounds."
(c) Dieng et al., arXiv:1611.00328v4, §2.3 `[full text]`, on the Monte-Carlo estimate of their upper bound:
"The objective is not guaranteed to be an upper bound if S is not chosen appropriately from the
beginning.  This problem does not exist for lower bounds because the Monte Carlo approximation is still
a lower bound".  Li & Turner, arXiv:1602.02311v3, §4.1 `[full text]`: negative orders "at the cost of losing
the upper-bound guarantee".
(d) **The unhinted bracket, as stated:** Liu–Fisher–Ihler, Corollary 3.2 (quoted in §4.3(b)), with their
gloss: "The quantity Δ is quite intuitive, with the first term proportional to the empirical standard
deviation and decaying at the classic `1/√n` rate.  The second term captures the possibility that the
empirical variance is inaccurate; it depends on the boundedness of w(x) and decays at rate 1/n."
(e) Off-policy evaluation.  Thomas, Theocharous, Ghavamzadeh, "High confidence off-policy evaluation"
(© 2015 AAAI on the PDF) `[full text: abstract, concentration section, Thm 1]`: importance-weighted returns
"are bounded from below by zero … and may have a large upper bound"; "removing the upper tail of a
distribution can only lower its expected value"; their Theorem 1 is a lower confidence bound that
"removes the need to determine a tight upper bound on the largest possible importance weighted
return".  Metelli et al., arXiv:1809.06098v2, Theorem 4.1 `[full text]`: with probability `≥ 1 − δ`,
`E_P f ≥ (1/N)Σ w f − ‖f‖_∞ √((1 − δ)d_2(P‖Q)/(δN))`, `d_2 = exp(D_2)`; `ESS = N/d_2(P‖Q)`.

*In print — statistics.*  (f) Wang & Ramdas, arXiv:2202.01250v6, §10.1 `[full text of the subsection]`:
moment assumptions "are necessitated by the results of Bahadur and Savage [1956], which immediately imply
that if no upper bound on a moment is known a priori, mean estimation is provably impossible".
Bahadur & Savage, Ann. Math. Statist. 27(4), 1115–1122 (1956) `[record; not accessed]`.  (g) Phan, Thomas,
Learned-Miller, arXiv:2106.03163v5 `[full text: §2, §4.2 passages]`: for an upper confidence bound on a mean
"we only need to know a superset of the support with finite upper bound"; in the "1-ended support
setting" the method "is equal to Anderson's".  For `Y = e^{−r}` the upper end of the support is `e^{−lo}`: the
floor.  (h) Chatterjee & Diaconis, arXiv:1511.01437v3, Theorem 2.1 `[full text]`: "Given any ε > 0, there
exists `n ≤ ε^{−2}2^{1+ε^{−3}}` such that the following is true.  Take any μ and ν as in Theorem 1.1, and any f …
such that `‖f‖_{L²(ν)} ≤ 1`.  Let `v_n(f)` be defined as above.  Then `P(v_n(f) < ε) ≥ 1 − 4ε`" — "using `v_n(f)` for
testing convergence of importance sampling is fundamentally flawed".  This is the published theorem
behind the theory division's documented refutation ("mean plus two standard errors is not a
certificate").  In the same vein, on molecular systems: Midgley et al., arXiv:2208.01893v3 `[full text]`: "the
ESS for the SNF, RBD and the flow trained by minimizing KL(q_θ‖p) are spurious as these methods are
missing modes."

*In print — free-energy perturbation.  What exactly is stated (the brief's question).*

| source | reading level | what it states about sample size or direction | status in its own words |
|---|---|---|---|
| Zwanzig, J. Chem. Phys. 22(8), 1420–1426 (1954), doi:10.1063/1.1740409 | `[record]` | (the perturbation identity; not read) | — |
| Jarzynski, arXiv:cond-mat/0603185v1 (Phys. Rev. E 73, 046105 (2006) as cited by Yunger Halpern–Jarzynski) | `[full text: §III, §IV]` | `N_c^F ∼ exp(βW̄_d^R)`, `N_c^R ∼ exp(βW̄_d^F)` (34); for perturbation: "`ln N_c^A ∼ βW̄_d^B = D[p_B\|p_A] ≥ 0`" (45a) — sampling `A` costs `exp(KL(target‖sampled))`; "Of the two perturbations, the one with larger `W_d` requires fewer samples" | "a back-of-the-envelope estimate"; "heuristic insights and quantitative estimates" |
| Kofke, manuscript for Molecular Physics (Liblice 2006 issue) | `[full text: abstract, §3 passage]` | `M_F ≥ 1 + 2(·s_R)^{1/2}exp(s_R)` with `s_R = ∫p_B ln(p_B/p_A)` (one symbol illegible in the extraction); deleting a hard sphere: "`s` … is thus literally infinite.  Correspondingly no amount of deletion sampling is capable of rendering an accurate result" | "a heuristic", "we have stipulated", "fail-safe" |
| Wu & Kofke, J Chem Phys 123, 054103 (2005), [doi:10.1063/1.1992483](https://doi.org/10.1063/1.1992483) — according to PubMed | `[abstract]` | two relative entropies "expressed in terms of the dissipated work"; "used to scale the amount of sampling to obtain a universal bias curve" | "a simple heuristic … we argue that it is fail-safe" |
| Wu & Kofke, J Chem Phys 123, 084109 (2005), [doi:10.1063/1.2011391](https://doi.org/10.1063/1.2011391) — according to PubMed | `[abstract]` | "Stages should always be constructed such that work is performed only into a system that has a phase-space subset relation with the starting system" | recommendation |
| Wu & Kofke, Phys Rev E 70, 066702 (2004), [doi:10.1103/PhysRevE.70.066702](https://doi.org/10.1103/PhysRevE.70.066702) — according to PubMed | `[abstract]` | "the bias is significantly smaller when sampling is performed on the system having a broader work distribution ('insertion')" | neglected-tail model, numerics |
| Lu & Kofke II, J. Chem. Phys. 115(15), 6866–6875 (2001), doi:10.1063/1.1405449 | `[fetch-tool]` | the quantity `M exp(ΔS/k)` indicates whether a result is likely accurate (about 100 minimally, 1000 safer); "such calculations must be performed in the 'insertion' direction" | "Heuristics" (title) |
| Lu & Kofke I, J. Chem. Phys. 114(17), 7303–7311 (2001), doi:10.1063/1.1359181 | `[record]` | (not read) | — |
| Lu, Adhikari, Kofke, Phys Rev E 68, 026122 (2003), [doi:10.1103/PhysRevE.68.026122](https://doi.org/10.1103/PhysRevE.68.026122) — according to PubMed | `[abstract]` | "Finite sampling … leads to reproducible systematic errors, with sign shown to depend (in a known way) only on which system governs sampling … Thus the result of a FEP calculation can be used as a bound on the true free energy.  This inequality is of a wholly different nature from … the Gibbs-Bogoliubov inequality" | a bound in the sense of the sign of the bias |
| Gore, Ritort, Bustamante, PNAS 100:12564–9 (2003), [doi:10.1073/pnas.1635159100](https://doi.org/10.1073/pnas.1635159100) — according to PubMed | `[abstract]` + `[fetch-tool]` | "the large N limit for the Jarzynski estimator bias, variance, and mean square error"; (fetch) "the number of trajectories necessary … increases exponentially with `W̄_dis`" | asymptotic (large `N`) and Gaussian near-equilibrium analysis |
| Zuckerman & Woolf, arXiv:physics/0201046v1 | `[full text]` | "`ΔF ≤ ΔF_n`, any n.  This inequality results from the convexity of the exponential function"; for a Boltzmann factor with tail `z^{−(1+α)}`, `1 < α < 2`: `f_n − f ≈ φ_{α−1}(1/n)^{(α−1)}` | exact in expectation (Jensen); asymptotic expansions |
| Shirts & Pande, J Chem Phys 122, 144107 (2005), [doi:10.1063/1.1873592](https://doi.org/10.1063/1.1873592) — according to PubMed | `[abstract]` | reviews "theoretical estimates of the bias and variance" of three estimators; no sample-size law in the abstract | — |
| Hahn & Then, arXiv:0904.0625v3, arXiv:0910.2858v2 | `[abstract]` | convexity of the mean-square error of Bennett's method ("state and prove"); a convergence measure for the two-sided estimator | theorem about Bennett's method; a diagnostic |
| Yunger Halpern & Jarzynski, arXiv:1601.02637v2 | `[full text]` | Theorem 1 (§4.3(f)): expected number of trials before one "dominant" work value; calls Jarzynski's `N ∼ e^{β(⟨W⟩−ΔF)}` "a rough estimate" | a rigorous waiting-time bound; "approximate error bound" |
| Suárez, Silbey, Oppenheim, Phys. Rev. E 85, 051108 (2012) | read by workstream A1, not re-read | exact bias of the exponential average in the discrete random energy model | exact, one model |

So: the sample size `exp(dissipated work of the reverse process) = exp(KL(target‖sampled))` is a
**heuristic or an estimate** in the free-energy literature I read, a **theorem at one instance under a
concentration hypothesis** in Chatterjee–Diaconis (Theorem 1.1, quoted in §4.5), and a **minimax theorem
over divergence balls** only in Block–Polyanskiy and Block–Shetty.  *Is the one-sidedness stated as a
theorem?*  As the sign of the bias — yes, it is Jensen's inequality (Zuckerman–Woolf; Grosse et al. (26)).
As "which direction of perturbation is reliable" — only as heuristics and recommendations (Lu–Kofke,
Wu–Kofke, Kofke, Jarzynski).  As "no valid upper confidence bound on `Z` exists without an a-priori
bound" — in statistics (Bahadur–Savage), not in the free-energy papers I read.

*Comparison.*  Each clause of T4 has a counterpart: "a mean, `w² ln(1/δ)/(2ε²)`" is Hoeffding's Theorem 2
applied to `r` (and needs the *oscillation*, i.e. the ceiling as well; Markov's inequality gives a valid
lower bound on `ln Z` with no assumption at all, at a slack of `ln(1/δ)` nats: (a), (b)); "`e^{ρ₋}`" is the bound on
the weights in (d) and §4.3; the bracket is (d).  **Classification: (2)**; the unhinted bracket **(1)**; the
slogan **(3)** — and it is too strong: see §4.8, item 2.

*Sentence to write.*  "That sampling a model bounds a partition function cheaply from below and not
from above is standard (Jensen and Markov: Grosse, Ghahramani and Adams 2015; Gogate, Bidyuk and
Dechter); a valid upper bound needs a-priori control of the weights (Bahadur and Savage 1956), and
with weights bounded by an upper-bounding model the empirical-Bernstein bracket of Liu, Fisher and
Ihler (2015, Corollary 3.2) is exactly 'width from the sample variance, validity from the bound'.  A
pointwise floor is the strongest such control, not the only one: a bound on any moment of order
`p > 1` of the Boltzmann factor of the remainder suffices (Bubeck, Cesa-Bianchi and Lugosi,
arXiv:1209.1727; Kunsch, Novak and Rudolf 2019; Block and Shetty 2026)."

### 4.5 O1 — Rényi balls (A17.1–A17.5)

*Statements.*  A17.1: members of `{‖e^{−r}‖_{L^p(π)} ≤ B}` that differ on `D` have `π(D) ≥ (|μ − μ′|/B)^{p/(p−1)}`.
A17.2: hinted cost `Θ(e^κ/ε^{p/(p−1)})`, `κ` the bound on `D_p(π_g‖π)`.  A17.3: without a hint `Θ(e^κ/ε^{max(2, p/(p−1))})`.
A17.4: Kullback–Leibler ball: `exp(Θ(κ/ε))`.  A17.5: `p = 1` gives nothing; no polynomial moment of `r` suffices.

*In print.*

(a) **Block & Shetty, "Partition Function Estimation under Bounded f-Divergence", arXiv:2602.23535v1 (26 Feb
2026)** `[full text: §§1–6, App. D.1]`.  Setting: "Given access to i.i.d. samples `X_1, …, X_n ∼ μ` and the
ability to evaluate an unnormalized density ratio λ on each sample, how large must n … be to ensure
that there exists an estimator … [with] `(1 − ε)Z ≤ Ẑ ≤ (1 + ε)Z` with probability at least 1 − δ?"  Theorem 5:
"as long as `n ≳ γ_f(6·D_f(ν‖μ)/ε)·log(1/δ)/ε ∨ c²/ε²`" with `γ_f(M) = inf{t ≥ 1 : f(t)/t ≥ M}`; "This is the case for KL
divergence where `n ≳ exp(c·D_KL(ν‖μ)/ε)/ε` samples suffice as well as for α-Renyi divergences with `1 < α ≤ 2`,
where `n ≳ (ε^{−α}·D_f(ν‖μ))^{1/(α−1)}` samples suffice … α-Renyi divergences with `α > 2`, where `n ≳ 1/ε²` samples
suffice" (the exponent `1/(α−1)` is a superscript that the text extraction displaces).  Lower bounds:
Proposition 1 (bounded `f′`: "no estimator given access to finitely many samples … is capable of
producing a `1 ± ε` approximation"); Theorem 8 ("any estimator … must use at least `n ≳ γ_f(C/(2ε))/ε` samples",
"holds for arbitrary f-divergences"); Proposition 2 (`‖dν/dμ‖_∞ ≤ 4`: `n ≳ 1/ε²`).  Theorem 6: the one-sided
estimator (§4.3(c)), with "`M = γ_f(6·D_f(ν‖μ)/ε)`" — for Rényi order `p`: `log(1/δ)·e^{D_p}ε^{−p/(p−1)}` up to constants,
for every `p > 1` ("a sample complexity of estimating Z from below that is significantly smaller than the
`ε^{−2}` scaling").  §3.3: "the sample complexity of sampling is strictly smaller than that of partition
function estimation … at least an `ε^{−1}` factor".  On earlier work, in their words: "Devroye et al. …
considers heavy-tailed mean estimation under polynomial moment constraints; our f-divergence [bounds]
recover their results when considering Renyi divergences"; "Chatterjee and Diaconis … proving that
exponentially many samples in the KL divergence are necessary and sufficient for importance sampling
to succeed, but do not consider more general f-divergences or coverage".
(b) **Kunsch, Novak, Rudolf, "Solvable integration problems and optimal sample size selection",
arXiv:1805.08637v2** (J. Complexity 53 (2019) 40–67 per the Crossref record) `[full text: §1, Thms 3.9, 3.10,
Remark 3.11, §3.4, Cor. 3.14]`.  Cones `Y_{p,q,K} = {‖Y − EY‖_q ≤ K‖Y − EY‖_p}`, absolute error `ε`.  Upper bound (their
(5)): expected cost `≤ C_q K^{pq/(q−p)}(1 + (‖Y − EY‖₁/ε)^{max{1+1/(q−1), 2}}) log δ^{−1}`.  Theorem 3.9 (`q ≥ 2`):
`n̄^{wor}(ε, δ, Y_{p,q,K} ∩ σB_2) ≥ (4 log 3)^{−1}(σ/ε)² log(3/(4δ))`.  Theorem 3.10 (`1 < q ≤ 2`):
`n̄^{wor}(ε, δ, Y_{p,q,K} ∩ τB_q) ≥ c_{q,K}(τ/ε)^{1+1/(q−1)} log(3/(4δ))`.  Corollary 3.14: the same bounds "for general
randomized algorithms" using function values (π without atoms), because "no general randomized
algorithm is better than the best possible i.i.d.-based algorithm in distinguishing `F^{(1)}` from `F^{(2)}`".
Their `q` is our `p`: the exponent `max{2, p/(p−1)}` of A17.3, with lower bounds in exactly our query model,
in absolute error and central norms.
(c) **Heavy-tailed mean estimation — the brief's question "is O1 that rate, read backwards?"  Yes, for
`1 < p ≤ 2`.**  Bubeck, Cesa-Bianchi, Lugosi, arXiv:1209.1727, Lemma 1 `[full text]`: "If `E|X|^{1+ε} ≤ u`, then with
probability at least 1 − δ, `μ̂_T ≤ μ + 4u^{1/(1+ε)}(log(δ^{−1})/n)^{ε/(1+ε)}`" (truncated mean; raw moment); Lemma 2: the
median of means with the centred moment.  Devroye, Lerasle, Lugosi, Oliveira, arXiv:1509.05845v1, Theorem
3.1 `[full text, with proof]`: for `α ∈ (0, 1]` and any estimator,
`sup_{P ∈ P^M_{1+α}} P{|Ê_n − μ_P| > (M^{1/α} ln(2/δ)/n)^{α/(1+α)}} ≥ δ`; the proof uses two laws with an atom of mass
`p = (2/n) log(2/δ)` at `±c` which the sample misses with probability `≥ 2δ`.  With `p = 1 + α`, `M^{1/p} ↔ B` and absolute
accuracy `εμ`: `n ≍ ln(1/δ)(B/(εμ))^{p/(p−1)}` — A17.2 and A17.3 for `p ≤ 2`.  The information-based-complexity form:
Heinrich & Novak, arXiv:quant-ph/0105114v1, Theorem 4 and table `[full text]`: randomised error of
summation on the unit ball of `L_p^N`: `(1 + √((N − 1)n/(N − n)))^{−1}` for `2 ≤ p ≤ ∞` (Mathé 1995), `≍ n^{−1+1/p}` for
`1 ≤ p < 2`.
(d) **`p = 2` and `p = ∞` at one instance.**  Agapiou, Papaspiliopoulos, Sanz-Alonso, Stuart, arXiv:1511.06196v3,
Theorem 2.1 `[full text]`: with `ρ = π(g²)/π(g)²`, "`sup_{|φ|≤1} E[(μ^N(φ) − μ(φ))²] ≤ (4/N)ρ`", `D_χ²(μ‖π) = ρ − 1`,
`ρ ≥ e^{D_KL(μ‖π)}`; "the number of particles required … scales exponentially with the Kullback-Leibler
divergence between proposal and target and linearly with the χ² divergence".  Metelli et al. (§4.4(e)).
Chatterjee & Diaconis, arXiv:1511.01437v3, Theorem 1.1 `[full text]`: with `L = D(ν‖μ)`, "If `n = exp(L + t)` …
`E|I_n(f) − I(f)| ≤ ‖f‖_{L²(ν)}(e^{−t/4} + 2√(P(log ρ(Y) > L + t/2)))`.  Conversely … If `n = exp(L − t)` …
`P(I_n(1) ≥ 1 − δ) ≤ e^{−t/2} + P(log ρ(Y) ≤ L − t/2)/(1 − δ)`" — typical-case, one pair, needs concentration of
`log ρ`; A17.4 is the worst case over the ball, where the price is `exp(κ/ε)`.
(e) **The neighbouring task.**  Block & Polyanskiy, arXiv:2302.04658v3, Theorems 3, 5 and Examples 6–7 `[full
text]`: to output one of `n` samples of `μ` with law within total variation `ε` of `ν`, over all pairs with
`D_f(ν‖μ) ≤ D`: `Õ(exp(D_KL(ν‖μ)/ε))` samples for Kullback–Leibler, `Õ(e^{D_λ(ν‖μ)}ε^{−1/(λ−1)})` for Rényi order `λ` (the
last formula is garbled in the text extraction; this reading agrees with their Theorem 3 by my
computation and with their remark that `λ = 2` gives `Õ(χ²/ε)`); lower
bound `n ≥ ½(f′)^{−1}(δ/(2ε))` from the pair `μ = Ber(ε/n)`, `ν = Ber(2ε)`; Lemma 27: `ν(dν/dμ > M) ≤ 2D_f/f′(M/2)` — the
analogue of A17.1.
(f) **The coordinator's lead (1): χ and Rényi upper bounds in variational inference.**  Dieng, Tran,
Ranganath, Paisley, Blei, arXiv:1611.00328v4 (NIPS 2017 per the PDF footer) `[full text: §§1–2.3, App. D]`:
"`CUBO_n = (1/n) log E_q[(p(x,z)/q(z))^n]`" (their (2)); "Theorem 1 (Sandwich Theorem) … `∀n ≥ 1`
`ELBO ≤ log p(x) ≤ CUBO_n`"; the identity `½ log(1 + D_χ²(p‖q)) = −log p(x) + ½ log E_q[(p(x,z)/q(z))²]` (A17's divergence
form at `p = 2`); Appendix D: "minimizing this variance is equivalent to minimizing … the χ²-divergence".
Li & Turner, arXiv:1602.02311v3 `[full text: §3, §4.1]`: `L_α = (1/(1 − α)) log E_q[(p/q)^{1−α}]`, Theorem 1:
`L_VI ≤ L_{α₊} ≤ L_0 ≤ L_{α₋}` for `0 < α₊ < 1`, `α₋ < 0` (so `α₋ = 1 − p` gives `ln Z ≤ (1/p) ln E_q w^p`).  **So both
statements the coordinator recalled are there.  A certificate is not:** both papers give estimators and
say that the Monte-Carlo estimate of the upper bound loses the guarantee (§4.4(c)); neither states a
finite-sample guarantee over a class.
(g) **Lead (2): flow annealed importance sampling bootstrap.**  Midgley, Stimper, Simm, Schölkopf,
Hernández-Lobato, arXiv:2208.01893v3 ("Published as a conference paper at ICLR 2023") `[full text: abstract,
§1, §2, evaluation paragraphs]`: "minimize the mass-covering α-divergence with α = 2, which minimizes
importance weight variance"; "When α = 2, minimizing the α-divergence is equivalent to minimizing the
variance of the importance sampling weights".  Effective sample size is an *evaluation metric*
computed from flow samples; no statement relates a sample size to the divergence, and no guarantee is
claimed; the paper itself warns that the metric is "spurious" when modes are missing (§4.4(h)).
(h) **Uncertainty quantification.**  Atar, Chowdhary, Dupuis, arXiv:1310.6391v1 `[abstract; Thm 2.1 formula
seen]`: a variational formula for exponential integrals with Rényi divergence, for "bounding tail
properties of an intractable model in terms of a tractable one" — the same kind of class (a divergence
ball around a tractable model), another functional, no evaluation cost.

*Comparison.*  A17.3 against (a): same information (model samples plus the Boltzmann factor of the
remainder at the samples), same accuracy (multiplicative `1 ± ε`), same classes (bounded Rényi or
Kullback–Leibler divergence of the true ensemble from the model), same three regimes and exponents,
matching lower bounds; differences: their classes are unrestricted measures, ours finite spaces; their
lower bounds are for estimators fed by i.i.d. samples (Theorem 7 "for any non-atomic μ"), ours for query
algorithms that may choose where to evaluate — for which (b) supplies the lower bound when `π` has no
atoms.  A17.4 against (a): `exp(c·D_KL/ε)/ε` sufficient, `γ_f(C/(2ε))/ε` necessary: the same law,
with one more factor `1/ε`, and without the restriction to the centre (for Kullback–Leibler `γ_f(M) ≍ exp(M)`
in their notation, so the necessary count is `exp(Θ(C/ε))/ε`).  A17.2 against (a): the count is
their Theorem 6, the lower-bound instance their Theorem 8 (A3.4(b)); the *reading* — that with a hint
the one-sided cost is the whole cost, so that verification is cheaper than estimation exactly for
`p > 2` — was not found.  A17.1 is Hölder's inequality; its analogues are Lemma 27 of (e) and the
coverage bound `Cov_M ≤ D_f/(f(M)/M)`-type lemma of (a).  A17.5(i) is Proposition 1 of (a) in spirit (a
linear `f` controls nothing); A17.5(ii) (moments of `r`) was not found stated — it is the remark that a
polynomial moment of `r` bounds no moment of `e^{−r}`, and in the sampling model it is an instance of
Bahadur–Savage.

**Classification.**  A17.3 and A17.4: **(1) in print** (sampling model; (a), with (b), (c) earlier for the
Rényi rows).  A17.2: **(2) direct corollary** — two lines: by A17.1 a member whose `ln μ` differs by more than
`ε` from the hint differs on a set of `π`-mass at least `(s_ε μ̃/B)^{p/(p−1)}`, which is the hitting probability
behind Theorem 6 of (a); the hint replaces their upper tail `Ẑ ≤ M·Z` by an exact value.  A17.5(ii):
**(3)**.  The table of A17 §(4) as a whole: its rows and its right-hand column are (a); its left-hand
column is (a)'s Theorem 6 re-read.

*Sentence to write (for A17).*  "The cost table is, in the sampling model and without a hint, the main
result of Block and Shetty (arXiv:2602.23535, 2026): `γ_f(D_f/ε)/ε ∨ χ²/ε²` samples are necessary and sufficient,
i.e. `e^{κ}ε^{−p/(p−1)}` for Rényi order `1 < p ≤ 2`, `ε^{−2}` beyond, `exp(Θ(κ/ε))/ε` for Kullback–Leibler, nothing for
total variation; for `1 < p ≤ 2` this is the minimax rate of heavy-tailed mean estimation (Bubeck, Cesa-
Bianchi and Lugosi, arXiv:1209.1727; Devroye, Lerasle, Lugosi and Oliveira 2016), and the exponent `max{2, p/(p−1)}` with
lower bounds for all randomised algorithms using function values is Kunsch, Novak and Rudolf (2019).
Their one-sided estimator (Theorem 6) has the cost of our 'with a hint' column for every `p`.  What we
add is the reading of that column as a verification cost — a hint removes the variance term and
nothing else — the finite, deterministic form, the statement that no polynomial moment of the
remainder energy suffices, and A17.6."

### 4.6 O2 — product reference measures (A17.6)

*Statement.*  `π` a product measure, one-site oscillations `c_i`, `K = Σc_i²`: `D_p(π_g‖π) ≤ p²K/(8(p − 1))`; `D_2 ≤ K/2`.

*In print.*  Cesar & Rogers, "Bounding, concentrating, and truncating: unifying privacy loss composition
for data analytics", arXiv:2004.07223v3 `[full text: Def. 2.2, Lemma 2.1, Lemma 3.2 and its proof]`: "If the
analyst selects an α-BR mechanism `M_i` given `F_{i−1}` then for all λ ∈ ℝ we have
`E[exp(λX_i) | F_{i−1}] ≤ e^{λ²α²/8}` & `E[L_i | F_{i−1}] ≤ α/(e^α − 1) − 1 − ln(α/(e^α − 1))`"; "α-BR implies
`(ξ, α²/8)`-zCDP, where `ξ = α/(e^α − 1) − 1 − ln(α/(e^α − 1)) − α²/8 ≤ 0`".  Bun & Steinke, "Concentrated
differential privacy: simplifications, extensions, and lower bounds", arXiv:1605.02065v1 `[full text: Def.
1.1, Lemma 2.2, Lemma 2.3, Prop. 3.3]`: zCDP means `D_α(M(x)‖M(x′)) ≤ ξ + ρα` for all `α ∈ (1, ∞)`; "Composition:
… `D_α(P′‖Q′) + min_x D_α(P′_x‖Q′_x) ≤ D_α(P‖Q) ≤ D_α(P′‖Q′) + max_x D_α(P′_x‖Q′_x)`"; Lemma 2.3 (adaptive composition adds
the parameters); Proposition 3.3: "`D_∞(P‖Q) ≤ ε` and `D_∞(Q‖P) ≤ ε`.  Then `D_α(P‖Q) ≤ ½ε²α` for all `α > 1`."  The
proof in A17.6 uses "McDiarmid's bound on the moment generating function"; I did not open McDiarmid
(1989) or a textbook for it.

*Comparison.*  A17.6 bounds `ln E_π e^{−p(r − E_π r)}` by the bounded-differences moment generating function
and discards `−p ln E_π e^{−(r − E_π r)} ≤ 0`; the composition route keeps it, which is where the factor
`p/(p − 1)` comes from (A3.2).  **Classification: (2) direct corollary** of the two statements quoted, in
the improved form; the form in A17.6 is a weaker corollary of a standard bound.

*Sentence to write.*  "For a product reference measure the conditional law of each site in the true
ensemble is a tilt of the model's marginal by a function of oscillation at most `c_i` (a `c_i`-bounded-range
pair in the language of differential privacy), so `D_p(π_g‖π) ≤ (p − 1)K/8 + Σ_i L(c_i) ≤ pK/8` by the bound for
bounded-range pairs (Cesar and Rogers, arXiv:2004.07223, Lemma 3.2) and the composition of Rényi
divergences (Bun and Steinke, arXiv:1605.02065, Lemma 2.2)."  *(I cite arXiv versions because I did not
see the published venues; Bun–Steinke attribute the composition property to van Erven–Harremoës, which
I did not open.)*

### 4.7 The direction of the divergence (A17 §(4), last paragraph; the coordinator's lead (3))

*Statement.*  Every row is `D(π_g‖π)`, the divergence of the true ensemble from the model; the variational
principle minimises `D_1(π‖π_g)`, the gap of the cheap side, and may ignore a basin of the true ensemble.

*In print.*  Minka, "Divergence measures and message passing", MSR-TR-2005-173 (7 December 2005) `[full
text: abstract, §2 passages]`: divergences of order `α ≤ 0` "are zero-forcing because p(x) = 0 forces
q(x) = 0 … This causes some parts of p to be excluded"; orders `α ≥ 1` "are inclusive (α < 1 are exclusive).
Inclusive divergences require q > 0 whenever p > 0, thus avoiding 'false negatives.'  If two identical
Gaussians are separated enough, an exclusive divergence prefers to represent only one of them, while
an inclusive divergence prefers to stretch across both."  Li & Turner §3: "zero-forcing (α → +∞, when
using uni-modal approximations it is usually called mode-seeking) and mass-covering (α → −∞)" (their
sign convention for α is the opposite of Minka's).  Midgley et al. §2: "The α-divergence is mode-seeking
for α ≤ 0 and mass-covering for α ≥ 1 (Minka, 2005)".  In physics: Jarzynski 2006, eq. (45) and the
insertion/deletion discussion; Kofke's hard-sphere example (§4.4 table).  As a theorem on sample size:
Chatterjee–Diaconis Theorem 1.1 (`D(ν‖μ)`, target first).  **Classification: (1) in print**; one citable
source for the slogan is Minka (2005).

### 4.8 What in these sources contradicts or sharpens our statements

1. **T1 can be sharpened for free** — Hoeffding's mean-dependent bound (A3.1(b)); and our A5 (`KL ≤ w²/8`)
   holds with `L(w)`, which is linear, not quadratic, in a large oscillation.
2. **"What must be certified is the floor, and nothing else can replace it" (THY-RES-0007 §4, (i)) is
   contradicted as a literal statement.**  Any a-priori bound on a moment of order `p > 1` of `e^{−r}` under
   the model replaces it, at the price of the exponent `p/(p−1)` (Bubeck et al., Lemma 1; Kunsch et al.;
   Block–Shetty, Theorem 5); so does a Kullback–Leibler bound, at the price `exp(Θ(κ/ε))`.  What is true —
   and is Bahadur–Savage — is that *some* a-priori control of the upper tail of the Boltzmann factor is
   indispensable.  A17 says this; the literature said it first.
3. **"With a hint" overstates what the hint does.**  At the centre of a constant box the same count is
   reached without one (A3.3(a): 545 against the quoted 1088); in general the unhinted cost is the
   Dagum–Karp–Luby–Ross bound `max(σ², εμ′)/(εμ′)²` and the hint removes the variance term only.  Block–
   Shetty's Theorem 6 gives the upper side of the certificate at the hinted cost without a hint.
4. **The headline `Θ((Z(lo)/Z(g) − 1)/ε)` drops the bump term** `(1 − Z(hi)/Z(g))/(1 − e^{−ε})`, which is the whole
   cost near the floor (A3.4(a)).  The full formula is in the theory log, item (c); the headline should
   carry it or say "for instances not close to the floor".
5. **In `ε`, the "expensive" side is the cheap one.**  Excluding missed mass costs `e^{κ}ε^{−p/(p−1)}`, i.e.
   `e^{κ}/ε` under a floor; an `ε`-tight *lower* bound on `Z` costs the variance term `χ²/ε²` (Block–Shetty,
   Theorems 5–6, Proposition 2).  T4's "the lower bound costs a mean" is the cost of the Gibbs–Bogoliubov
   bound, which is not `ε`-tight (its gap is up to `L(w)`); the two statements are about different lower
   bounds and the text should say so.
6. **A17.6 loses a factor `p/(p − 1)` in the exponent** (A3.2).
7. **A17.4 holds beyond the centre and with one more factor `1/ε`** in the sampling model (Block–Shetty,
   Theorems 5 and 8); A17's "proved at the centre only" can cite it.
8. **The sample-variance diagnostic fails provably**, not only by example: Chatterjee–Diaconis Theorem 2.1
   (§4.4(h)) — a theorem to cite next to the theory division's documented refutation.
9. **A caution on a citation.**  The proof of the stopping-rule theorem in Dagum–Karp–Luby–Ross is
   reported incomplete (Chen, arXiv:0711.2801, App. D); the statement is reported true.  Cite the theorem,
   not the proof.
10. **Nothing found contradicts** T2, the lower bound of T3, A17.1–A17.5 or the direction statement.
11. **A17.7 (second addition, §4.11) is sharpened in two small ways and contradicted in none.**  Between its
    two forms sits `ln(1 + (σ²/b²)(e^b − 1 − b))` (Liao–Berg, Theorem 1, applied to the exponential); the same theorem
    improves the *cheap* side to second order when the remainder has a ceiling `a` above its mean:
    `K ≥ ln(1 + Var_π(r)(e^{−a} − 1 + a)/a²)`.  And the one molecular-simulation paper read on bounds (Delle Site–
    Hartmann 2024) states that the second-order truncation is in general neither an upper nor a lower
    bound — the gap that A17.7 closes under a floor.

### 4.9 Search log

All searches on 2026-11-25 (from 23:33 UTC) and 2026-11-26 (to 01:00 UTC); the step-by-step record with
outcomes is `experiments/science/ws_A3/NOTES.md`.  No query contained anything identifying the project.

**`WebSearch`** (S = standard, X = extended), in order:

| # | mode | query | what came back |
|---|---|---|---|
| W1 | S | `Dagum Karp Luby Ross "An optimal algorithm for Monte Carlo estimation" pdf` | bibliographic records; side hit: Karp–Luby–Madras PDF on a university course page (downloaded) |
| W2 | S | `"optimal algorithm for Monte Carlo estimation" Dagum Karp Luby Ross "stopping rule theorem" "generalized zero-one estimator theorem" technical report` | arXiv:1302.3598, 0711.2801, 2210.12861 (restatements) |
| W3 | X | `… "AA" "(ε, δ)-approximation" "ρ_Z" "max{σ_Z^2, εμ_Z}" lower bound theorem universal constant` | records only |
| W4 | S | `… filetype:pdf "Stopping Rule Algorithm" "Υ" "4 λ ln(2/δ)/ε^2"` | nothing new |
| W5 | X | `"Lower Bound Theorem" "Let BB be any algorithm" Dagum Karp Luby Ross …` | arXiv:1308.1562, 1309.5413 as secondary sources (not opened) |
| W6 | X | `"A typical approach to estimate an unknown quantity" "design an experiment that produces a random variable Z distributed in [0,1]" … full text pdf download` | academia.edu and ResearchGate listings (both refused) |
| W7 | S | `Specht 1960 "Zur Theorie der elementaren Mittel" Math. Z. 74 91-98 Specht's theorem "arithmetic mean" "geometric mean" ratio upper bound …` | Springer record; RIMS Kôkyûroku PDFs (two downloaded) |
| W8 | S | `Liu Fisher Ihler "Probabilistic Variational Bounds for Graphical Models" NIPS 2015 pdf …` | proceedings PDF (downloaded) |
| W9 | X | `verifying a claimed mean or sum with an untrusted hint: O(1/ε) queries versus Θ(1/ε²) for estimation; "randomized certificate complexity" OR "fractional block sensitivity" of approximate counting / approximate sum; interactive proofs verifying machine learning quadratically fewer samples` | **nothing** on certificate complexity of approximate sums; arXiv:2404.08158 as a side hit (abstract read afterwards, with the ECCC report it builds on) |
| W10 | X | `free energy perturbation exponential averaging rigorous finite-sample confidence interval "lower bound" on energy difference bounded perturbation concentration inequality certified error bar Zwanzig estimator non-asymptotic guarantee` | **no** certified error bar for exponential averaging; Kofke's manuscript (downloaded) |
| W11 | X | `"Rényi divergence" bounded class of targets importance sampling normalizing constant minimax sample complexity lower bound "exp(D_" OR "e^{D_" relative accuracy ε^{-p/(p-1)} OR "ε^{-α/(α-1)}" heavy-tailed importance weights` | **arXiv:2602.23535** (Block–Shetty), Block–Polyanskiy's own page |
| W12 | X | `query complexity of verifying a claimed partition function or sum of positive weights given a pointwise upper bound on each weight: sampling proportional to the slack …, Θ((U/Z − 1)/ε) evaluations, lower bound by disjoint sets; "sum estimation" "proportional sampling" verification with advice` | **nothing** matching T3; arXiv:2602.23535 and arXiv:2404.02414 again |
| W13 | X | `rigorous upper bound on the remainder of the second-order cumulant expansion of the Zwanzig free energy perturbation formula in terms of the variance of the energy difference and a one-sided bound; "Bennett's inequality" OR "Bernstein inequality" free energy difference exponential average bound variance` | **nothing** of the kind; arXiv:2009.14321 (Greeff) and arXiv:2602.18482 as side hits (the first read at abstract level) |
| W14 | X | `rigorous second-order bound on free energy difference beyond Gibbs-Bogoliubov inequality: upper bound on the remainder using variance of the perturbation energy and a bound on the perturbation, classical statistical mechanics perturbation theory "upper and lower bounds" free energy "second order"` | **no** such bound; Delle Site–Hartmann (Molecular Physics 2024; read afterwards from arXiv:2403.10918), a review (arXiv:1507.00563) that points to Decoster 2004, arXiv:2608.07246 (not opened) |
| W15 | S | `"Sharpening Jensen's inequality" Liao Berg Jensen gap bounded by variance arXiv` | arXiv:1707.08644 (downloaded and read); arXiv:2502.03988, 2212.11429 as side hits (not opened) |

**arXiv API** (`arxiv_q.py` / `arxiv_batch.py`; title, author or abstract queries, 76 in all; fifteen of them for
the second addition.  Six gave math/0609835, math/0503483, 0902.4058, 1109.4359 and Marton's math/0410168 (not
opened).  Nine more gave 1707.08644, 2403.10918, the three "two-sided Bogoliubov inequality" preprints
2111.10282, 2501.04564, 2608.07246 (not opened) and 2610.33786 (not opened); `ti:"thermodynamical
perturbations"` → 29 hits without Decoster's paper among those shown; and **no hit** for `abs:"free energy
perturbation" AND abs:"Bennett inequality"`, `abs:"cumulant expansion" AND abs:"free energy" AND abs:"rigorous
bound"`, `au:Decoster AND ti:"variational"`, `au:Decoster AND abs:"Bogoliubov"`).  Identifiers obtained and
verified by the returned titles: cond-mat/0603185, 1601.02637, 1511.01437, 1511.06196, 1209.1727, 1509.05845,
2302.04658, 1605.02065, 1909.13830, 2004.07223, 1611.00328, 1602.02311, 2208.01893, 1511.02543, 1805.08637,
0904.0625, 0910.2858, physics/0208015, physics/0201046, 1505.06217, 1508.00335, 1805.05135, 1004.0581,
quant-ph/0210020, 2003.10374, 1906.04280, quant-ph/0105114, 2010.09686, 2106.03163, 1905.06208, 1206.5242,
1809.06098, 1301.7392, math/0410159, 1210.3248, 1212.4663, 1702.07476, 1310.6391, 1911.09580, 1503.05136,
1608.08814.  (arXiv:2202.01250 was fetched by number after its title query was refused, and checked by
the title on the PDF; arXiv:1302.3598, 0711.2801, 2210.12861 and 2602.23535 came from `WebSearch`.)  Queries
**without a hit**: titles of Liu–Fisher–Ihler, Lou–Dechter–Ihler, Goldwasser et al.,
Metelli et al. (2021), Gajek–Niemiro–Pokarowski, Viricel et al., Cortes–Mansour–Mohri; `abs:"Specht" AND
abs:"determinant for positive operators"`; `abs:"converse of Jensen" AND abs:"Specht"`; `abs:"Bahadur" AND
abs:"Savage" AND abs:"mean"`; `au:Gore AND au:Ritort AND au:Bustamante`; **`abs:"free energy perturbation" AND
abs:"confidence interval" AND abs:"rigorous"` → 0; `abs:"partition function" AND abs:"confidence interval" AND
abs:"importance sampling" AND abs:"upper bound" AND abs:"bounded"` → 0.**  One request was refused (HTTP 429).

**PubMed** (tools `search_articles`, `get_article_metadata`, `get_full_text_article`, `convert_article_ids`):
`Kofke DA[Author] AND (free-energy perturbation OR phase-space overlap)` → 12; `Bias and error in estimates of
equilibrium free-energy differences from nonequilibrium measurements` → 1; `exponential averaging Bennett
acceptance ratio thermodynamic integration efficiency bias Shirts Pande` → 1; `Donald BR[Author] AND partition
function AND (K* OR "epsilon-approximation" OR provable)` → 3; `minimized dead-end elimination criterion hybrid
scoring search algorithm partition functions molecular ensembles` → 1; `Lilien RH[Author] AND Donald BR[Author]
AND ensemble-based scoring` → 2; `Ojewole AA[Author] AND Donald BR[Author] AND K*` → 2; `BBK* branch and bound over
K* sparse residue interaction graphs` → 0; `Lu N[Author] AND Kofke DA[Author] AND accuracy free-energy
perturbation` → 1 (not the 2001 papers, which PubMed does not list).  Full text obtained for PMC3263346
only; PMC returned no text for PMC240657 and PMC7185359.  For the second addition: `free energy perturbation
cumulant expansion second-order (bound OR rigorous OR inequality)` → 0; `rigorous upper lower bounds free energy
difference molecular simulation variance fluctuation inequality` → 0; `free energy perturbation cumulant
expansion` → 9 (two kept); `"free energy" bounds "second order" Gibbs-Bogoliubov` → 0.

**Consensus** (tool `search`; one query, no filters; the plan returns three records): `rigorous upper and
lower bounds on free energy differences in free energy perturbation using the variance of the energy
difference, beyond the Gibbs-Bogoliubov inequality` →
[1] [FEAT: Free energy Estimators with Adaptive Transport *](https://consensus.app/papers/details/w:a87d6152-f99e-4a72-8356-d820b463e335/?utm_source=claude_code) (Jiajun He et al., 2026, Journal of Statistical Mechanics Theory and Experiment, 23 citations);
[2] [Computationally feasible bounds for the free energy of nonequilibrium steady states, applied to simple models of heat conduction](https://consensus.app/papers/details/w:0c4edba8-3925-443a-b80f-81b992b82a74/?utm_source=claude_code) (Luigi Delle Site et al., 2024, Molecular Physics, 6 citations);
[3] [Thermodynamic potentials from a probabilistic view on the system-environment interaction energy](https://consensus.app/papers/details/w:41f5dc3d-674a-4905-8ffa-598313a4f74c/?utm_source=claude_code) (Mohammad Rahbar et al., 2025, arXiv, 3 citations).
Used in §4.11 as "Consensus [1]–[3]"; [2] had been found by W14 and was read in full from arXiv.

**Crossref API** (records, to avoid bibliographic details from memory): seven DOI look-ups and eleven
bibliographic queries (listed in `NOTES.md`, steps 10 and 15).  One DOI I had guessed turned out to belong to
another paper and was discarded.

**`WebFetch`**: SIAM (403), academia.edu (403), Project Euclid (empty page), PMC page of Gore et al.
(automatic reading; formulas are images), the AIP abstract page of Lu–Kofke II through its DOI
(automatic reading; the tool would not reproduce the abstract verbatim); the IOP page of Decoster's paper
(automatic reading of the abstract, summarised by the tool; the PDF address returned an error page).

**Direct downloads** (`getpdf.sh`): 80 targets, 65 PDFs (63 distinct papers).  Refused or failed: SIAM (challenge page),
IOP (challenge page at both addresses of Decoster's paper; Unpaywall and Semantic Scholar list that PDF as the
only open copy, and neither they nor Crossref carry the abstract),
CiteSeerX (redirect to archive.org, connection reset), ResearchGate, the former ICSI address of the
report version of Dagum–Karp–Luby–Ross (404/403), Project Euclid (bot wall), Europe PMC, PMC and PNAS PDFs
of Gore et al. (challenge pages), one Kyoto repository address (HTML).

### 4.10 Sources and what was read

**Read at `[full text]` level in the passages named (47; the last nine for the second addition).**

| source | identifier | passages read | used for |
|---|---|---|---|
| Hoeffding, American Statistical Association Journal, March 1963 (JASA 58(301), 13–30 per Crossref) | scanned PDF on a university course page (pp. 13–22 only) | pp. 13–14, 16–17, 20–22 (page images) | T1, A17.7 |
| Fujii, Lee, Seo, RIMS Kôkyûroku 1259 (2002) 1–10 | Kyoto University RIMS PDF | pp. 1–2 | T1 (Specht) |
| Furuichi | arXiv:1004.0581v3 | p. 1, Lemma 2.1, references | T1 |
| Dong, Durfee, Rogers | arXiv:1909.13830v2 | abstract, Def. 2.2, Cor. 2.1, Thm 1, Def. 2.4, §3.4, Lemma 4.1–4.2, appendix passage | T1, O2 |
| Cesar, Rogers | arXiv:2004.07223v3 | Def. 2.2, Lemma 2.1, Defs 2.6–2.7, Lemma 3.2 with proof, text after Lemma 3.4 | O2 |
| Bun, Steinke | arXiv:1605.02065v1 | Def. 1.1, Lemma 2.2, Lemma 2.3, Prop. 3.3, Remark 3.4 | O2 |
| Binette | arXiv:1805.05135v2 | abstract, Thm 1, Cor. 2 | T1 |
| Berend, Kontorovich | arXiv:1210.3248v1 | abstract, §1, Thm 4 | T1 (Kearns–Saul) |
| Karp, Luby, Madras, J. Algorithms 10 (1989) 429–448 | PDF on a university course page | title page, theorem statement, appendix restatement | T3 |
| X. Chen | arXiv:0711.2801 | pp. 2, 5; Appendix D | T3 (Dagum et al.) |
| Mnih, Szepesvári, Audibert, Proc. 25th ICML (2008) | icml.cc PDF | abstract, §§2–3, passage after eq. (4) | T3 |
| Pradhan, Dagum (proceedings pp. 446–452) | arXiv:1302.3598 | §§2–4 (OCR) | T3 |
| Aaronson | arXiv:quant-ph/0210020v1 | abstract, Defs 1–3, Prop. 4, Lemma 5 | T3 |
| Mathé, Novak | arXiv:math/0611285v2 | abstract, p. 4, class definition, Thms 1–2 | T3 |
| Kunsch, Novak, Rudolf | arXiv:1805.08637v2 | abstract, §1, Thms 3.9–3.10, Remark 3.11, §3.4, Cor. 3.14 | O1 |
| Heinrich, Novak | arXiv:quant-ph/0105114v1 | abstract, Thm 4, table | O1, T2 |
| Bubeck, Cesa-Bianchi, Lugosi | arXiv:1209.1727 | abstract, Lemmas 1–2, Thm 2 statement | O1 |
| Devroye, Lerasle, Lugosi, Oliveira | arXiv:1509.05845v1 | p. 3 passage, Thm 3.1, §4.3 | O1 |
| Chatterjee, Diaconis | arXiv:1511.01437v3 | §1 to Thm 1.2, Thm 2.1 and discussion | O1, T4 |
| Agapiou, Papaspiliopoulos, Sanz-Alonso, Stuart | arXiv:1511.06196v3 | abstract, §2.2, §2.3.3, §2.5 | O1 |
| Block, Polyanskiy | arXiv:2302.04658v3 | abstract, §1 (part), §§2–3, App. B to Cor. 17, Lemma 27 | O1 |
| **Block, Shetty** | **arXiv:2602.23535v1** | abstract, §§1–6, App. D.1 | **O1**, T3, T4 |
| Jarzynski | arXiv:cond-mat/0603185v1 | abstract, introduction, §III, §IV, start of §V | T4, O1 |
| Yunger Halpern, Jarzynski | arXiv:1601.02637v2 | whole main text to Thm 2 | T3, T4 |
| Zuckerman, Woolf | arXiv:physics/0201046v1 | abstract, introduction, divergent-moments section | T4 |
| Kofke, manuscript for Molecular Physics | author's departmental page | abstract, §3 passage | T4 |
| Liu, Fisher, Ihler | NeurIPS proceedings site, 2015 volume | abstract, §1, related work, §3 | T3, T4 |
| Gogate, Bidyuk, Dechter | arXiv:1206.5242 | abstract, §2.2, §3 | T4 |
| Grosse, Ghahramani, Adams | arXiv:1511.02543v1 | abstract, §4 intro, §4.1, §4.2 first page | T4 |
| Dieng, Tran, Ranganath, Paisley, Blei | arXiv:1611.00328v4 | abstract, §1, §§2.1–2.3, App. D | lead (1) |
| Li, Turner | arXiv:1602.02311v3 | abstract, §3, §4.1, App. D first paragraphs | leads (1), (3) |
| Midgley, Stimper, Simm, Schölkopf, Hernández-Lobato | arXiv:2208.01893v3 | abstract, §1, §2, evaluation paragraphs, discussion | lead (2) |
| Minka | MSR-TR-2005-173 | abstract, §2 passages | lead (3) |
| Thomas, Theocharous, Ghavamzadeh (© 2015 AAAI) | author's page | abstract, concentration section, Thm 1 statement | T4 |
| Phan, Thomas, Learned-Miller | arXiv:2106.03163v5 | §2 and §4.2 passages | T4 |
| Wang, Ramdas | arXiv:2202.01250v6 | §10.1 | T4 |
| Metelli, Papini, Faccio, Restelli | arXiv:1809.06098v2 | §§3–4 passages, Thm 4.1 | T4, O1 |
| Georgiev, Lilien, Donald, J Comput Chem 29(10):1527–42 (2008) — according to PubMed | [doi:10.1002/jcc.20909](https://doi.org/10.1002/jcc.20909), PMC3263346 | §4, Proposition 3 | T2 |
| Fan, Grama, Liu (Stochastic Process. Appl. 122 (2012) 3545–3559 per the arXiv record) | arXiv:1109.4359v5 | §1, Lemma 3.1, references | A17.7 |
| Pinelis (Ann. Inst. H. Poincaré Probab. Stat. 50(1):15–27 (2014) per the arXiv record) | arXiv:0902.4058v1 | §1, first page | A17.7 |
| van Handel, "Probability in High Dimension", APC 550 lecture notes (21 Dec 2016) | Princeton web page | §2.1 (Thm 2.3, Cor. 2.4), notes to chapter 2 | A17.7, A17.6 |
| Raginsky, Sason | arXiv:1212.4663v8 | §2.2.3 (Thm 2.2.2 with proof), Thm 3.3.7 | A17.6, A17.7 |
| Kontorovich, Ramanan, Ann. Probab. 36(6) (2008) 2126–2158 (as printed on the arXiv version) | arXiv:math/0609835v2 | abstract, §1 (Thms 1.1, 1.2), Thm 2.1, Remark 2.1 | A17.6 non-product |
| Chazottes, Collet, Külske, Redig | arXiv:math/0503483v2 | abstract, introduction, §2.1–2.3 (Thms 1–2, proof of Thm 1), §3.1 | A17.6 non-product |
| Liao, Berg (The American Statistician 73(3), 278–281 per Crossref) | arXiv:1707.08644v2 | pp. 1–6 (Thm 1, Lemma 1, Example 1) | A17.7 |
| Delle Site, Hartmann (Molecular Physics 123(7–8), 2024 per Crossref) | arXiv:2403.10918v1 | abstract, Thm 3.1 and the start of its proof, §3.3 | A17.7 (use in free-energy perturbation) |
| Kuzemsky | arXiv:1507.00563v1 | abstract; one passage on pp. 29–30; reference [39] | A17.7 (pointer to Decoster) |

**`[abstract]` (the paper's own abstract; for PubMed items "according to PubMed"):** Lu–Adhikari–Kofke
([doi:10.1103/PhysRevE.68.026122](https://doi.org/10.1103/PhysRevE.68.026122)); Wu–Kofke
([doi:10.1103/PhysRevE.70.066702](https://doi.org/10.1103/PhysRevE.70.066702),
[doi:10.1063/1.1992483](https://doi.org/10.1063/1.1992483), [doi:10.1063/1.2011391](https://doi.org/10.1063/1.2011391));
Lu–Kofke–Woolf ([doi:10.1002/jcc.10369](https://doi.org/10.1002/jcc.10369)); Gore–Ritort–Bustamante
([doi:10.1073/pnas.1635159100](https://doi.org/10.1073/pnas.1635159100), plus `[fetch-tool]`); Shirts–Pande
([doi:10.1063/1.1873592](https://doi.org/10.1063/1.1873592)); Lilien et al.
([doi:10.1089/cmb.2005.12.740](https://doi.org/10.1089/cmb.2005.12.740)); Ojewole et al.
([doi:10.1089/cmb.2017.0267](https://doi.org/10.1089/cmb.2017.0267)); Jou et al.
([doi:10.1089/cmb.2019.0315](https://doi.org/10.1089/cmb.2019.0315)); Lowegard et al.
([doi:10.1371/journal.pcbi.1007447](https://doi.org/10.1371/journal.pcbi.1007447)); Hahn–Then (arXiv:0904.0625v3,
0910.2858v2); Sanz-Alonso (arXiv:1608.08814v1); Atar–Chowdhary–Dupuis (arXiv:1310.6391v1, with the formula
of Thm 2.1).
**`[fetch-tool]`:** Lu & Kofke II (doi:10.1063/1.1405449); Decoster (doi:10.1088/0305-4470/37/39/001), abstract.
**Downloaded, not read (titles checked only):** Kearns–Saul (arXiv:1301.7392), Bentkus (arXiv:math/0410159),
Mironov (arXiv:1702.07476), Lugosi–Mendelson (arXiv:1906.04280), Sason–Verdú (arXiv:1508.00335; headings
of the bounded-relative-information theorems only), Yunger Halpern et al. (arXiv:1505.06217), Zuckerman–
Woolf (arXiv:physics/0208015), Waudby-Smith–Ramdas (arXiv:2010.09686), Naesseth–Lindsten–Blei
(arXiv:2003.10374), Birrell et al. (arXiv:1911.09580), Huber (arXiv:2210.12861; first page), Hoffmann et al.
(arXiv:2602.18482; a side hit of W13, not relevant).
**`[record]` only:** see "What I could not access".
**`[abstract]`, added last:** Goldwasser–Rothblum–Shafer–Yehudayoff, ECCC Report No. 58 (2020); Gur et al.,
arXiv:2404.08158v1 (with the statement of Thm 1.4).  For the second addition: Greeff, arXiv:2009.14321; according to
PubMed, Wang–Mei–Ryde ([doi:10.1039/d4sc00140k](https://doi.org/10.1039/d4sc00140k)) and Mathis et al.
([doi:10.1088/1361-648X/aec29c](https://doi.org/10.1088/1361-648X/aec29c)); through Consensus, He et al. and Rahbar et al.
(Consensus [1], [3] of §4.9).  **`[record]`, second addition:** Reible–Hartmann–Delle Site (arXiv:2111.10282; Lett.
Math. Phys. 112, 97 (2022) per the arXiv listing), Marton (arXiv:math/0410168), Hu–Wang (arXiv:2610.33786).

### 4.11 Second addition from the coordinator: A17.7 (the Bennett bracket) and reference measures that are not products

*(Written after the rest of the report; A17 parts (6) and (7) were read in the tree.  Part (6) —
measured divergences — raises no prior-art question and is not discussed.)*

**A17.7 — statement.**  With `r ≥ E r − b` (a one-sided floor `b` below the mean) and `Var r ≤ σ²` under the
model, the Jensen gap `K = ln E e^{−(r − E r)}` satisfies
`K ≤ W(b, σ²) := ln[(b²e^{−σ²/b} + σ²e^{b})/(b² + σ²)] ≤ (σ²/b²)(e^{b} − 1 − b)`, with equality in the first inequality for
the two-point law that has a state at the floor with probability `σ²/(b² + σ²)`.

*In print.*

(a) **Hoeffding 1963, Theorem 3** `[full text: p. 16–17 and p. 20, scanned]`: "Theorem 3.  If `X_1, …, X_n` are
independent, `EX_i = 0`, `X_i ≤ b` (i = 1, …, n), then for `0 < t < b`,
`Pr{X̄ ≥ t} ≤ {(1 + bt/σ²)^{−(1+bt/σ²)σ²/(b²+σ²)}(1 − t/b)^{−(1−t/b)b²/(b²+σ²)}}^n` (2.8) `≤ e^{−(nt/b)[(1+σ²/bt)ln(1+bt/σ²) − 1]}` (2.9).
Here the summands are assumed to be bounded only from above. … Inequality (2.8) is the best that can be
obtained from (1.7) under the present assumptions.  It is the minimum with respect to h of the right-hand
side of (1.7) when the `X_i` have the distribution `Pr{X_i = −σ²/b} = b²/(b² + σ²)`, `Pr{X_i = b} = σ²/(b² + σ²)` (2.10). …
The bound (2.9) is due to Bennett ([2], inequality (8b)).  (Bennett's notation is different from mine.  His
first proof assumes `|X_i| ≤ b` (= his M), a second proof (pp. 42–3) uses only `X_i ≤ b`.)"  And p. 20: "the bound
in (2.8) is an increasing function of σ²".  **So the two-point extremal law is stated by Hoeffding, (2.10),
and the weaker exponential form is attributed by him to Bennett.**  The moment-generating-function
inequality itself is in the proof of Theorem 3, on pages my copy does not contain (it ends at p. 22).
(b) **The inequality at the level of the moment generating function, with the extremal law.**  Fan, Grama,
Liu, "Hoeffding's inequality for supermartingales", arXiv:1109.4359v5 (Stochastic Process. Appl. 122 (2012)
3545–3559 per the arXiv record) `[full text: §1, Lemma 3.1]`: "Bennett [2] and Hoeffding [18] used a more
precise estimation `φ_i(λ) ≤ (1/(1 + σ_i²)) exp{−λσ_i²} + (σ_i²/(1 + σ_i²)) exp{λ}`, `λ ≥ 0`, (3) for any `ξ_i` satisfying
`ξ_i ≤ 1`.  Bennett's estimation (3) is sharp with the equality attained when `P(ξ_i = 1) = σ_i²/(1 + σ_i²)` and
`P(ξ_i = −σ_i²) = 1/(1 + σ_i²)`"; "Lemma 3.1.  If ξ is a random variable such that `ξ ≤ 1`, `Eξ ≤ 0` and `Eξ² = σ²`,
then, for any `λ ≥ 0`, `E(e^{λξ}) ≤ (1/(1 + σ²)) exp{−λσ²} + (σ²/(1 + σ²)) exp{λ}`", "which, in the special case of
centered random variables, has been proved by Bennett [2]" — [2] being "Bennett, G., 1962.  Probability
inequalities for the sum of independent random variables, J. Amer. Statist. Assoc. 57, No. 297, 33–45."
With `ξ = −(r − E r)/b`, variance `σ²/b²` and `λ = b` this is `e^{K} ≤ (b²e^{−σ²/b} + σ²e^{b})/(b² + σ²)`: **A17.7, as stated,
with its extremal law.**  (The lemma is stated with `Eξ² = σ²`; "`≤ σ²`" follows because the right-hand side
increases with `σ²` — one line: its derivative in `s = σ²` has the sign of `e^{hb + hs/b} − (1 + hb + hs/b) ≥ 0`.)
(c) **The weaker form.**  Pinelis, "On the Bennett–Hoeffding inequality", arXiv:0902.4058v1 (Ann. Inst. H.
Poincaré Probab. Stat. 50(1):15–27 (2014) per the arXiv record) `[full text: §1, first page]`: "The
Bennett-Hoeffding inequality … is based on an upper bound on the exponential moments of S:
`E e^{λS} ≤ BH_exp(λ) := exp{((e^{λy} − 1 − λy)/y²)σ²}` for all `λ > 0`" (1.3) — at `λ = 1`, `y = b` this is
`K ≤ (σ²/b²)(e^{b} − 1 − b)`.  He adds that "exact bounds refining the Bennett-Hoeffding ones were obtained by
Pinelis and Utev" using third moments — a sharper known result if a third-moment bound were ever
available; not needed here.
(c′) **The same bound in the language of the Jensen gap.**  Liao & Berg, "Sharpening Jensen's inequality",
arXiv:1707.08644v2 (The American Statistician 73(3), 278–281, doi:10.1080/00031305.2017.1419145 per Crossref)
`[full text: pp. 1–6]`: "Theorem 1.  Let X be a one-dimensional random variable with mean µ, and P(X ∈ (a, b)) = 1
… Let ϕ(x) is a twice differentiable function on (a, b), and define function
`h(x; ν) := (ϕ(x) − ϕ(ν))/(x − ν)² − ϕ′(ν)/(x − ν)`.  Then
`inf_{x∈(a,b)}{h(x; µ)} var(X) ≤ E[ϕ(X)] − ϕ(E[X]) ≤ sup_{x∈(a,b)}{h(x; µ)} var(X)`" (2); "Lemma 1.  If ϕ′(x) is convex, then
h(x; µ) is monotonically increasing in x"; and "Example 1 (Moment Generating Function)".  With `ϕ = exp` and
`X = −r ≤ −E r + b` the supremum sits at the upper end and (2) reads `e^{K} − 1 ≤ (σ²/b²)(e^{b} − 1 − b)`: a form between
A17.7's two,

    W(b, σ²)  ≤  ln(1 + (σ²/b²)(e^{b} − 1 − b))  ≤  (σ²/b²)(e^{b} − 1 − b)        [checked: C9, and at 50 digits on a grid]

The paper mentions neither Bennett nor Hoeffding.  Its lower half sharpens the *cheap* side by the same
token [P from K; checked, C9]: if `r ≤ E r + a` everywhere, then `K ≥ ln(1 + Var_π(r)(e^{−a} − 1 + a)/a²)` — a
second-order improvement of the Gibbs–Bogoliubov bound, which needs a ceiling on the remainder and the
variance itself (not a bound on it).
(d) Bennett's own paper was not opened.

*The variance input, "`Var r ≤ ¼Σc_i²` (Efron–Stein)".*  van Handel, "Probability in High Dimension" (APC 550
lecture notes, Princeton, version of 21 December 2016) `[full text: §2.1]`: "Theorem 2.3 (Tensorization of
variance).  We have `Var[f(X_1, …, X_n)] ≤ E[Σ_i Var_i f(X_1, …, X_n)]` whenever `X_1, …, X_n` are independent";
"Corollary 2.4 (Bounded difference inequalities).  We have `Var[f(X_1, …, X_n)] ≤ ¼E[Σ_i (D_i f(X_1, …, X_n))²]`", `D_i f`
being the supremum minus the infimum over the `i`-th coordinate; and in the notes to the chapter: "The
tensorization property of the variance is classical.  It is sometimes called the Efron-Stein inequality
after [58], where it was used to investigate Tukey's jackknife estimator."  Raginsky & Sason,
arXiv:1212.4663v8 `[full text: Thm 3.3.7, Thm 2.2.2 with proof]`: "Theorem 3.3.7 (Efron–Stein–Steele
inequality) … `var[f(X^n)] ≤ Σ_i E[var(f(X^n) | X̄^i)]`"; and, for A17.6's other attribution, McDiarmid's inequality
with the step "`E[e^{tξ_k} | F_{k−1}] ≤ exp(t²d_k²/8)`" (2.2.32).  **Both attributions are correct** — the constant
`¼` is the tensorization inequality followed by "a variable with range `c_i` has variance at most `c_i²/4`".
Efron & Stein ("The jackknife estimate of variance", Ann. Statist. 9(3), 586–596 (1981), as cited by van
Handel) was not opened.

*Is "free-energy perturbation with a certified second-order bound" in the molecular-simulation
literature?*  **Not found.**  First round (§4.9: web query W13 and four PubMed queries): what came back
treats the truncation of the cumulant expansion empirically: Greeff, "Free energy perturbation theory at low
temperature", arXiv:2009.14321 `[abstract]`: the cumulant series of Zwanzig, convergence judged by "the ratio
of the third order to the second order term in the expansion is found to be ∼0.1, indicating good
convergence"; according to PubMed, Wang, Mei, Ryde, Chem Sci 15(23):8786–8799 (2024),
[doi:10.1039/d4sc00140k](https://doi.org/10.1039/d4sc00140k) `[abstract]`: "for Gaussian distributions … free energies
can be accurately approximated using a second-order cumulant expansion … distributions that are skewed
towards more negative values than a Gaussian present greater challenges in achieving convergence, making
standard criteria unreliable.  We propose a practical approach to assess the convergence"; and Mathis, Li,
Greeff, Blaschke, Rehn, J Phys Condens Matter (2026),
[doi:10.1088/1361-648X/aec29c](https://doi.org/10.1088/1361-648X/aec29c) `[abstract]`: free-energy perturbation theory
"does not improve systematically with perturbative order".  The second of these names, as the hard case,
exactly the extremal law of A17.7 (weight on rare, strongly negative energy differences).  No paper
retrieved bounds the remainder rigorously from a variance bound and a one-sided bound.

A second round (web query W14, one Consensus query, nine more arXiv-API queries; §4.9) gave three things.
(i) Delle Site & Hartmann, "Computationally feasible bounds for the free energy of nonequilibrium steady
states, applied to simple models of heat conduction", arXiv:2403.10918v1 (Molecular Physics 123(7–8), 2024,
doi:10.1080/00268976.2024.2391484 per Crossref) `[full text: abstract, Thm 3.1, §3.3]`.  The rigorous bracket there is
of first order at both ends — "Theorem 3.1 (Two-sided Bogoliubov inequality) … `E_{µne}[G] ≤ −β⁻¹ log E_{µe}[e^{−βG}] ≤ E_{µe}[G]`"
(24) — and its lower end is an average under the *other* ensemble.  Of the second order they write:
"`−β⁻¹ log E_{µe}[e^{−βG}] = E_{µe}[G] − (β/2)Var_{µe}(G) + O(β²)` (32).  Since the free energy is in general neither convex
nor concave as a function of β, we cannot expect the mean-variance approximation to provide an upper or
lower bound.  Yet, in practice, and this is empirically demonstrated below, the mean-variance approximation
turns out to be a fairly accurate approximation that resides between the upper and lower bounds."  This is
what A17.7 can be set against: a two-sided bracket exists when *both* ensembles are sampled (in A17's
notation `−E_π r ≤ ln Z(g) − ln Z(ĝ) ≤ −E_{π_g} r`, the upper end being an average under the target, with gap
`D_KL(π_g‖π)` by their eq. (26)); the second-order term computed from the reference alone is used as an
approximation and explicitly not as a bound.
(ii) Kuzemsky's review of the Bogoliubov variational principle, arXiv:1507.00563v1 `[full text: one passage,
pp. 29–30, and reference [39]]`: "A. Decoster [39] established a sequence of inequalities which generalize the
the Gibbs-Bogoliubov inequality in classical statistical mechanics and the Peierls and Bogoliubov
inequalities in quantum mechanics; they can be presented as rearrangements of perturbation expansions,
which provide exact bounds which are used in variational calculations."  The paper is Decoster, "Variational
principles and thermodynamical perturbations", J. Phys. A: Math. Gen. 37(39), 9051–9070 (2004),
doi:10.1088/0305-4470/37/39/001 (record per Crossref); its abstract `[fetch-tool]` says the same and adds an
illustration on an anharmonic oscillator.  **I could not open it** (publisher's challenge page; the fetch
tool got an error page).  It is the one source I met that claims rigorous bounds beyond first order in
thermodynamic perturbation theory.  From the two descriptions these are *variational* bounds, that is,
improvements of the Gibbs–Bogoliubov side — a guess from the abstract, not a reading — and not a bound on
the opposite side from a floor and a variance; it has to be read before the use made in A17.7 is called
new.
(iii) Consensus (one query; three records, `[abstract]` as returned by the tool; list in §4.9): He et al.,
"FEAT: Free energy Estimators with Adaptive Transport" (2026) — "variational upper and lower bounds on free
energy differences" next to estimators built on the escorted Jarzynski equality and the Crooks theorem
(Consensus [1]); Delle Site & Hartmann again (Consensus [2]); Rahbar et al., "Thermodynamic potentials from a
probabilistic view on the system-environment interaction energy" (2025) — "a general equality … from which
an inequality follows - aligned with Jensen's inequality applied to the Gibbs-Bogoliubov-Feynman bound"
(Consensus [3]).  None of the three abstracts states a second-order bound from the reference ensemble alone.

*Comparison and classification.*  The inequality of A17.7, its extremal law and its weaker form:
**(1) in print as stated** (Bennett 1962 as reported by Hoeffding and by Fan–Grama–Liu; Hoeffding 1963,
Theorem 3 and (2.10)).  The attribution in A17.7 ("Bennett 1962, Hoeffding 1963, sharp two-point form") is
right; the precise division of labour, as far as I could read: the exponential form (2.9) is Bennett's
(8b); the sharper form and the statement of the extremal two-point distribution are in Hoeffding; the
moment-generating-function lemma is credited to Bennett by Fan–Grama–Liu.  Its use as a *certificate* for
first-order perturbation theory of a free energy — a floor and a variance bound in, a bracket out — :
**(4) not found** in the sources retrieved (two extended web searches, four PubMed queries, one Consensus
query, eleven arXiv-API queries), with one paper that claims rigorous bounds beyond first order (Decoster
2004) not opened.  *Remark.*  T1 and A17.7 are the two
moment-generating-function lemmas of one paper: range and mean (Hoeffding's Theorem 2, eqs. (4.12)–(4.13))
against a one-sided bound and the variance (his Theorem 3).

*Sentence to write.*  "The bound is Bennett's inequality in the sharp form of Hoeffding (1963, Theorem 3,
inequality (2.8), with the extremal two-point distribution (2.10); the exponential form (2.9) is Bennett
1962, inequality (8b)); for a product reference the variance input is the tensorization
(Efron–Stein–Steele) inequality with bounded differences, `Var r ≤ ¼Σc_i²`.  We did not find it used as a
certified second-order bound in free-energy perturbation: there the rigorous bracket is the two-sided
Bogoliubov inequality, which needs averages under both ensembles; the second-order (mean–variance)
truncation is an approximation that is in general neither an upper nor a lower bound (Delle Site and
Hartmann 2024); and its convergence is judged empirically (e.g. Greeff 2020; Wang, Mei and Ryde 2024)."
(For us, not for the text: Decoster (2004) has to be read first — see (ii) above.)

**Reference measures that are not products — one citable statement with its constant.**

(a) **Chazottes, Collet, Külske, Redig, "Concentration inequalities for random fields via coupling",
arXiv:math/0503483v2** `[full text: abstract, introduction, §2.1–2.3 with Thms 1–2 and the proof of Thm 1, §3.1]`.
For a measure on `A^n` let `D^σ_{i,i+j} := max_{a,b} P̂^σ_{i,a,b}(σ^{(1)}_{i+j} ≠ σ^{(2)}_{i+j})` be the probability that two copies of the
future, coupled given the same past and the values `a`, `b` at site `i`, differ at site `i + j`; `D := sup_σ D^σ`;
`δ_i g` the oscillation of `g` at site `i`.  "THEOREM 1.  Let n ∈ ℕ be arbitrary.  Assume that (6) holds [`‖D‖_{ℓ²} < ∞`].
Then, for all functions `g : A^n → ℝ`, we have the inequality
`P{|g − Eg| ≥ t} ≤ 2 exp(−2t²/(‖D‖²_{ℓ²(ℕ)}‖δg‖²_{ℓ²(ℕ)}))` for all `t > 0`", proved through "(9)
`E(e^{λV_i} | F_{i−1})(σ) ≤ e^{λ²(D^σδg)_i²/8}`" and "(10) … `≤ e^{−λt} exp(λ²‖Dδg‖²_{ℓ²(ℕ)}/8)`"; "THEOREM 2. …
`E(g − Eg)² ≤ ‖D^{(2)}‖²_{ℓ²(ℕ)}‖δg‖²_{ℓ²(ℕ)}`" with `D^{(2)}_{i,j} = E[(D^σ_{i,j})²]^{1/2}`.  For a product measure `D` is the identity
and (10) is McDiarmid's bound with its sharp constant.  On Gibbs fields: "In [10], C. Külske obtained an
exponential concentration inequality for functions of Gibbs random fields in the Dobrushin uniqueness
regime"; with Dobrushin's matrix `C_{x,y}` (condition `sup_x Σ_y C_{x,y} < 1`) and `Δ := Σ_{n≥0} C^n`, "From [10, Lemma 1],
we have the estimate `|∫g(η)P(dη|σ_{<x}, +_x) − ∫g(η)P(dη|σ_{<x}, −_x)| ≤ Σ_y (1_{x,y} + Δ_{y,x})δ_y g`" — [10] being Külske, Comm.
Math. Phys. 239, 29–51 (2003), not opened.  Marton is cited next to it: "In [15], K. Marton obtained exponential
concentration results for a class of Gibbs random fields under a strong mixing condition lying between
Dobrushin-Shlosman condition and its weakening" — [15] being Studia Sci. Math. Hungar. 40 (2003) 95–113; not
opened.
(b) **Kontorovich & Ramanan, "Concentration inequalities for dependent random variables via the
martingale method", Ann. Probab. 36(6) (2008) 2126–2158, doi:10.1214/07-AOP384 (as printed on
arXiv:math/0609835v2)** `[full text: §1 with Thms 1.1, 1.2; Thm 2.1, Remark 2.1]`.  Mixing coefficients `η̄_{ij}` (the
largest total-variation distance between the laws of `X_j, …, X_n` given two pasts that differ only in
the `i`-th symbol), `‖Δ_n‖_∞ = max_i(1 + η̄_{i,i+1} + ⋯ + η̄_{i,n})`.  "Theorem 1.1. … `φ : S^n → ℝ` is a c-Lipschitz function
(with respect to the Hamming metric) … Then for any `t > 0`, `P{|φ − Eφ| ≥ t} ≤ 2 exp(−t²/(2nc²‖Δ_n‖²_∞))`."
"Theorem 1.2" (Markov chains, contraction coefficients `θ_i = sup_{x′,x″} ‖p_i(·|x′) − p_i(·|x″)‖_TV`):
"`P{|φ − Eφ| ≥ t} ≤ 2 exp(−t²/(2nc²M_n²))`", `M_n = max_i(1 + θ_i + θ_iθ_{i+1} + ⋯)`, and "`M_n ≤ 1/(1 − θ)`" when `θ_i ≤ θ < 1`.
"Theorem 2.1": the martingale differences of a 1-Lipschitz function satisfy `‖V_i(φ)‖_∞ ≤ 1 + Σ_{j>i} η̄_{ij}`.  Their own
caveat: "The constants in the exponent … are not sharp — indeed, for the independent case … a sharper bound
can be obtained by replacing n/2 by 2n."  On the lead "Marton, mid 1990s": "concentration inequalities around
the median that are qualitatively similar to the one obtained in Theorem 1.2 were obtained for strictly
contracting Markov chains in [20] (see Proposition 1) and for a class of stationary Markov processes in [21]
(see Proposition 4′)" — [20] = Marton, Ann. Probab. 24 (1996) 857–866, [21] = Probab. Theory Related Fields 110
(1998) 427–439, and their [19] is Marton, "A measure concentration inequality for contracting Markov chains",
Geom. Funct. Anal. 6, 556–571 (printed there with the year 1995).  None of Marton's papers was opened: the
lead is confirmed as a citation only.

*What follows for A17.6 and A17.7 [P from K; checked on 120 random two-state Markov chains, C9: no
violation].*  A17.6's own route (the moment generating function of `r` under the model at `λ = p`, then
Jensen) uses only (10); hence for any reference `π` with `‖D‖_{ℓ²} < ∞`

    D_p(π_g ‖ π)  ≤  p² ‖D‖² K / (8(p − 1)),        Var_π r  ≤  ‖D^{(2)}‖² K,        K = Σ_i c_i²,

i.e. **A17.6 with `K` replaced by `‖D‖²K`**, and a variance input for A17.7 with `‖D^{(2)}‖²` in place of `¼`; for a
Markov chain with contraction coefficient `θ < 1` the standard coupling gives `D_{i,i+j} ≤ θ^j` and `‖D‖ ≤ 1/(1 − θ)`.
The sharper route of A3.2 (composition, constant `p/8`) does not extend this way: it needs the oscillations
`c̃_i` of the *conditional free energy* of the remainder, an exponential functional that the coupling matrix
does not control linearly (§5, item 6).  So for interacting references the citable bound keeps the
factor `p/(p − 1)`.

*The one citable statement.*  Chazottes–Collet–Külske–Redig, Theorem 1, with its constant `2/(‖D‖²‖δg‖²)` in
the exponent (equivalently the moment-generating-function bound `exp(λ²‖D‖²‖δg‖²/8)`), reading level
`[full text]` of the arXiv version; for Gibbs fields under Dobrushin's condition the result is attributed
there to Külske (2003), which I did not open; for Markov chains Kontorovich–Ramanan, Theorem 1.2, with
`M_n ≤ 1/(1 − θ)` and a constant that is not sharp by the factor 4.

---

## 5. What I did not settle

1. **The exact theorems of Dagum–Karp–Luby–Ross.**  Everything said about them rests on three
   restatements (Chen; Mnih et al.; Kunsch et al.).  In particular I could not check whether the lower
   bound is stated in expectation or with probability `1 − δ`, nor its model of computation in the
   authors' words; A3.3(b) uses only what the restatement gives.
2. **Whether a statement of T3 with a hint exists in property testing or interactive proofs** ("proofs
   of proximity", PAC verification, annotated data streams).  One extended search; two abstracts read
   (§4.3).  This is the literature where "verification costs `1/ε`, estimation `1/ε²`" for a mean or a sum
   would be stated if it is; I did not find it there in the abstracts and did not read the bodies.
3. **Whether Block–Shetty's lower bounds extend to the query model with atoms and a hint.**  Their
   Theorem 7 assumes a non-atomic base measure; Kunsch–Novak–Rudolf's transfer to general randomised
   algorithms also needs a partition into small equal cells.  On a finite space with heavy states the
   packing fails (the theory division's "whenever no single state carries that much"); the exact
   instance-wise hinted cost there is the covering programme of A3.4(a), which I did not solve beyond
   the feasible point.
4. **Proofs.**  I compared statements; I did not referee the proofs of A17.2–A17.4 beyond re-deriving the
   lemmas I used, and the theory division's §11.30 is not written.  Block–Shetty is a preprint of
   February 2026; I read its statements and the proof of Theorem 8, not its appendices A–C, E–F.
5. **First sources.**  I did not open Specht (1960), Fujii–Izumino–Seo (1998), Tominaga (2002), Durfee–
   Rogers (the paper that introduces bounded range), McDiarmid, Anderson (1969) or a primary source for
   the name "Gibbs–Bogoliubov".
6. **A17.6 beyond product measures.**  The bound holds for any model with the ranges `c̃_i` of the
   conditional free energy of the remainder (remark after A3.2).  What I did not settle is how large
   the `c̃_i` are for a model with interactions: they are not bounded by the one-site oscillations of `r`,
   because the law of the later sites moves with `x_i`; bounding them is a question about the influence
   of one site on the rest (the mixing condition A17.6 alludes to, and the theory division's P2-T3 in
   another form).  What can be cited meanwhile is the non-sharp bound of §4.11 (`K` replaced by `‖D‖²K`, factor
   `p/(p − 1)` kept).
7. **Decoster (2004).**  The one paper met that claims rigorous bounds beyond first order in thermodynamic
   perturbation theory (§4.11) could not be opened; whether it contains a bound on the side of A17.7 is
   open.  Likewise Bennett (1962) itself and the proof pages of Hoeffding's Theorem 3.

## 6. The three most promising next steps

1. **Rewrite A17 around the Hoeffding–Dagum–Luby–Block–Shetty line and keep what is ours.**  State the
   table as known (§4.5, sentence), then the three things that are not in what I read: the verification
   reading (a hint removes the variance term — and nothing at instances that are flat on the bulk),
   the negative statement on polynomial moments of the remainder, and A17.6 in the sharp form of A3.2.
   This is an afternoon, and it changes what we may claim.
2. **Measure the ranges `c̃_i` for chain models** (§5, item 6).  For a model sampled site by site (a
   chain, or any model of small tree-width) the remark after A3.2 gives
   `D_p(π_g‖π) ≤ Σ_i[(p − 1)c̃_i²/8 + L(c̃_i)]`, a statement about sequential samplers that the product-measure
   version cannot reach; whether it is useful depends on whether the `c̃_i` stay bounded along the chain
   (the citable alternative, with the coupling matrix and a worse constant, is in §4.11).
   Numerics first: chains of 6–12 sites by transfer matrix, remainders of the kinds measured in
   workstreams P and P2.
3. **Measure which row a real remainder is in, with the estimator that matches the row.**  The
   literature gives the estimators: empirical-Bernstein bracket under a floor (Liu–Fisher–Ihler),
   median-of-means under a moment bound (Bubeck et al.; Block–Shetty), the one-sided quantile estimator
   (Block–Shetty, Theorem 6).  On the enumerated domains of workstreams P and P2 the Rényi divergences
   `D_p(π_g‖π)` of the solvent remainder from the pairwise model are computable exactly for several `p`;
   that table would say which a-priori bound is worth trying to certify by analysis.

## 7. Requests

### To the theory division (can be sent as they are)

* **A3-T1.**  In §11.30, attribute statement (a) as in §4.1: Jensen for the left side; Hoeffding (1963),
  Lemma 1 and eqs. (4.12)–(4.13), maximised over the mean, for the right side; name the constant —
  `L(w) = ln S(e^w)`, Specht's ratio — and note that it is the "maxkl" of bounded-range mechanisms (Dong,
  Durfee, Rogers, arXiv:1909.13830).  Consider stating the mean-dependent form
  `−wp + ln(1 − p + pe^w)`, `p = (max r − E_π r)/w`, which your Lean file can prove by the same chord argument.
* **A3-T2.**  Replace "(i) what must be certified is the floor, and nothing else can replace it" by a
  statement that survives the heavy-tail literature: *some* a-priori bound on the upper tail of the
  Boltzmann factor of the remainder is indispensable (Bahadur–Savage 1956); a pointwise floor is the
  strongest; a bound on a moment of order `p > 1` or on a Kullback–Leibler divergence also suffices, at
  the costs of Block–Shetty (arXiv:2602.23535, Theorems 5–8).
* **A3-T3.**  State what the hint buys.  Under the floor measure the unhinted stopping rule costs
  `max(σ_X², εμ′)/(εμ′)²` (Dagum–Karp–Luby–Ross 2000, as restated in Mnih–Szepesvári–Audibert 2008); your hinted
  cost is `(1 − μ′)/(εμ′)`; they coincide when `σ_X² ≲ εμ′`.  At the centre of a constant box the rule of our
  A3.3(a) certifies with 545 evaluations and no hint where your text quotes 1088 with one.  Either
  restrict "with a hint" to instances that vary on the bulk, or add the unhinted instance-wise
  statement.  (A harness test: the rule of A3.3(a) on adversarial two- and three-level members.)
* **A3-T4.**  Carry the bump term in the headline: `Θ((Z(lo)/Z(g) − 1)/ε + (1 − Z(hi)/Z(g))/ε)`.
* **A3-T5.**  Prior-art paragraph for §11.30: the sentences of §4.2–§4.4 (K\* stopping criterion; Aaronson's
  randomised verifier; Liu–Fisher–Ihler's bounded-weight bracket; Mathé–Novak's class `F_C`; Grosse et al.
  for the asymmetry; Chatterjee–Diaconis Theorem 2.1 next to your documented refutation of the naive
  interval).  Every reading level is in §4.10; please mark them as ours.
* **A3-T6 (question).**  Does `expected_queries_ge_packing` give the lower bound *with* the hint for a
  class defined by a moment constraint (not a box), i.e. does it need only "alternatives that differ
  from the hint on pairwise disjoint sets"?  If so the lower bound of A17.2(ii) is machine-checked as
  it stands.

### To the engineering division

* **A3-E1.**  On the enumerated rotamer and torsion domains (your tables behind workstreams P and P2):
  compute exactly, for the solvent remainder `r` against the pairwise model, (i) `D_p(π_g‖π)` for
  `p ∈ {1, 1.5, 2, 4, ∞}` at 300 K, (ii) the one-site oscillations `c_i` and `K = Σc_i²`, (iii) the variance of
  `e^{−(r − min r)}` under the floor measure.  *Motivation:* decide which row of the cost table a real
  remainder is in.  *Validation:* `D_∞ = ln max(Y/μ)`; `D_p` non-decreasing in `p`; `D_p ≤ (p − 1)K/8 + Σ_i L(c_i)`
  whenever the model is a product measure (this report, A3.2) — a violation is a bug.  *Stopping
  condition:* all enumerated domains of the two workstreams; no new enumeration.  *Resources:* seconds
  per domain.
* **A3-E2.**  Implement the three unhinted estimators named in §6, item 3, on the same domains with a
  fixed budget of `10⁴`–`10⁶` evaluations and report coverage of the certificates against the exact
  `ln Z` over 1 000 repetitions.  *Expected:* the empirical-Bernstein bracket never fails when the floor
  is the true minimum of `r` and fails at the rate predicted by Chatterjee–Diaconis Theorem 2.1 when the
  bound on the weights is dropped.

### To the coordinator

* The verdict on O1 changes what A17 may claim; §4.5 has the sentence.  A17.6 can be replaced by A3.2
  (proof in §2, check C5); A5 can be sharpened to `L(w)`.
* A17.7: both attributions hold (§4.11); the sentence to write is there.  For the non-product extension of
  A17.6 the citable theorem is Chazottes–Collet–Külske–Redig, Theorem 1 (constant `‖D‖²` in front of `K`); the
  sharp constant of A3.2 does not carry over.  "Free-energy perturbation with a certified second-order bound"
  was not found — two extended web searches, four PubMed queries, one Consensus query, eleven arXiv
  queries — so "not found", not "new"; and **Decoster, J. Phys. A 37 (2004) 9051–9070, should be obtained
  through a library before the claim is made** (it states rigorous generalisations of the Gibbs–Bogoliubov
  inequality to higher order; I could not open it).  A17.7 may add two lines from §4.11(c′): the intermediate
  form `ln(1 + (σ²/b²)(e^b − 1 − b))`, and the second-order improvement of the cheap side.
* If a second reader is assigned, the highest-value hour is on Block–Shetty's appendices (are Theorems 6
  and 8 proved as stated?) and on locating the original of Dagum–Karp–Luby–Ross through a library.

---

## What I could not access

* **Dagum, Karp, Luby, Ross**, SIAM J. Comput. 29(5), 1484–1496 (2000) (and the FOCS 1995 version): SIAM
  (challenge page with curl; HTTP 403 through the fetch tool), Semantic Scholar and Unpaywall (closed, no
  repository copy), CiteSeerX (redirect to archive.org, which is unreachable from this machine), the
  former ICSI address of the report version (404/403), academia.edu (403), ResearchGate.  Positioned
  through restatements only.
* **Zwanzig** (1954), **Lu & Kofke I** (2001), **Kofke** (Fluid Phase Equilibria 2005): records only
  (AIP / Elsevier).  **Lu & Kofke II**: abstract through an automatic reading only.
* **Specht** (1960; Springer), **Fujii–Izumino–Seo** (1998), **Tominaga** (2002): not opened; quoted from
  Fujii–Lee–Seo and Furuichi.
* **Bahadur & Savage** (1956), **Anderson** (1969), **von Bahr & Esseen** (1965), **Donoho** (1988): Project
  Euclid returns a bot wall or an empty page; the first is quoted from Wang–Ramdas, the others are not
  used.
* **Gore, Ritort, Bustamante** (2003): full text only through an automatic reading of the PMC page
  (formulas are images); PMC and PNAS refuse direct download.
* **Lilien et al.** (2005), **Ojewole et al.** (2018), **Jou et al.** (2020), **Lowegard et al.** (2020): abstracts
  only (PMC returned no text for the one tried).
* **Dagum & Luby** (1997), **Mathé** (1995), **Durfee & Rogers**, **van Erven & Harremoës**, **McDiarmid**,
  **Cortes–Mansour–Mohri** (2010), **Lou–Dechter–Ihler** (2017), **Gajek–Niemiro–Pokarowski** (2013),
  **Tal**, **Gilmer–Saks–Srinivasan**, **Kulkarni–Tal**, **Grossman–Komargodski–Naor**: not located in an open copy
  or not looked for beyond one query; none is quoted.  (Years in this list that are not supported by a
  record in §4.9 are from the brief or from memory.)
* For the second addition: **Bennett** (J. Amer. Statist. Assoc. 57 (1962) 33–45, as cited by Fan–Grama–Liu),
  **Hoeffding 1963, pp. 23–30** (the proof of Theorem 3; my scanned copy stops at p. 22), **Efron & Stein** (1981),
  **Külske** (Comm. Math. Phys. 239 (2003) 29–51, as cited by Chazottes et al.), **Marton**'s papers (1995/1996,
  1998, 2003, 2004, as cited by Kontorovich–Ramanan and by Chazottes et al.; the last is arXiv:math/0410168,
  located, not opened), **Pinelis–Utev**: not opened.  **Decoster**, J. Phys. A: Math. Gen. 37(39), 9051–9070
  (2004): IOP returns a challenge page to a direct download (two addresses) and an error page to the fetch
  tool; Unpaywall and Semantic Scholar list only the publisher's PDF, Crossref and Semantic Scholar carry no
  abstract, and three arXiv queries found no preprint; abstract through an automatic reading only.  **Reible–Hartmann–Delle
  Site** (arXiv:2111.10282) and the other "two-sided Bogoliubov inequality" preprints: located, not opened.
* **archive.org** is unreachable from this machine (connection reset by the proxy), which closed the
  usual route to old technical reports.
