# Workstream A3 — prior art, full text where accessible: certifying a free energy by sampling from a model (box classes, floors, Rényi balls)

*Brief written by the coordinator after checkpoint 33 (2026-11-25).  Read `COMMON.md`
first (its commit pins are out of date: theory is at `658b77f`; read-only export at
`/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_658b77f`).*

## Why

The theory division will publish, as its theory report §11.30, a result on **sup-norm
(box) classes around a known function whose Gibbs measure can be sampled exactly**, and
asks us for "prior art and criticism" (THY-RES-0007 §4 and §6.1, in
`docs/collaboration/responses/theory/THY-RES-0007.md` of the export; the statements
(a)–(e) are listed in `docs/RESEARCH_LOG.md` of the export, section "Resume here (cycle
10, fourteenth checkpoint)", item 1).  It names what it knows "from memory": Zwanzig's
perturbation formula; the one-sidedness of exponential averaging; Dagum, Karp, Luby and
Ross for the sampling model.  The coordinator is writing the criticism and a
generalisation (a draft will appear as addendum A17 in
`docs/science/INFERENCE_LIMITS_ADDENDA.md`; if it is not there when you start, the
statements are in the last section of this brief).  **Your job is the literature**, at
the standard of our earlier originality reviews (`docs/science/workstreams/A1_REPORT.md`,
`A2_REPORT.md` — read their classification scheme and their search logs first).

## The statements to position (theirs, then ours)

T1. *Jensen bracket with the sharp constant*: for `r = g − ĝ` with oscillation `w`,
    `−E_π r ≤ ln Z(g) − ln Z(ĝ) ≤ −E_π r + L(w)`, `L(w) = ln((e^w − 1)/w) − 1 + w/(e^w − 1) ≤ w²/8`
    (the two-point law is extremal).  [Our own Theorem 7 / addendum on Barron–Sheu is
    related: `docs/science/INFERENCE_LIMITS.md` §7 and SCI-MSG-0003.]
T2. *Deterministic certificates on a box*: after evaluating a set `Q` the range of `ln Z`
    is "ceiling off `Q`" to "floor off `Q`"; at the centre of a constant box a certificate
    must cover all but `q* = (e^ε − 1)/(e^{ρ₋} − e^{ε−ρ₊} + e^ε − 1)` of the mass of `π`.
T3. *Hinted (verification) cost*: with a hint, `Θ((Z(lo)/Z(g) − 1)/ε)` evaluations certify
    `ln Z` within `ε` — sampling proportionally to the "dip weight" `w(e^{−lo} − e^{−r})` and
    the "bump weight"; matching lower bound for every randomised algorithm by packing
    disjoint sets; at the centre of a constant box `Θ((e^{ρ₋} − 1)/ε)`, independent of the
    size of the system.
T4. *Asymmetry*: the lower bound on `ln Z` (Gibbs–Bogoliubov, a mean) costs
    `w² ln(1/δ)/(2ε²)`; the upper bound costs `e^{ρ₋}`; "the floor is the one assumption
    sampling cannot replace"; without a hint the same samples give a bracket whose width
    is set by the sample variance and whose validity is paid for by the floor.
O1. (ours, addendum A17) *Rényi balls*: for the class `‖e^{−r}‖_{L^p(π)} ≤ B` (`p > 1`) the
    hinted certification cost is `Θ((B/(εμ))^{p/(p−1)})`, `μ = Z(g)/Z(ĝ)`, i.e.
    `e^{D_p}/ε^{p/(p−1)}` with `D_p` the a-priori bound on the Rényi divergence of order `p`
    between the true ensemble and the model; `p = ∞` is T3, `p = 2` is `(1 + χ²)/ε²`; a bound
    on the mean or the variance of `r` itself gives no finite cost.
O2. (ours) for a product reference measure and a remainder with one-site oscillations
    `c_i`: `D_2 ≤ Σ_i c_i²/2` (McDiarmid's moment-generating-function bound), so first-order
    classes sit inside Rényi balls.

## Sources to open (full text if at all possible; say for each what you could read)

* Dagum, Karp, Luby, Ross, "An optimal algorithm for Monte Carlo estimation" (SIAM J.
  Comput., 2000; conference version FOCS 1995): the exact theorem — sample complexity
  `max(σ²/(εμ)², 1/(εμ))·ln(1/δ)` for `[0,1]`-valued variables, the lower bound and its
  model.  **Is T3 the `1/(εμ)` term with `X = e^{−(r−lo)}` under the floor measure?**  What
  is the "hint"/verification counterpart in that literature, if any?
* Karp, Luby, Madras (1989) zero-one estimator theorem; Mnih, Szepesvári, Audibert
  (2008) empirical Bernstein stopping; any "verification vs estimation" or "certificate
  complexity of estimation" statement (testing vs learning a mean).
* Zwanzig (1954) free-energy perturbation; the sample-size literature for exponential
  averaging: Jarzynski, "Rare events and the convergence of exponentially averaged work
  values" (2006); Gore, Ritort, Bustamante (2003); Lu and Kofke (2001); Wu and Kofke
  (2004/2005, phase-space overlap / relative-entropy measures); Shirts and Pande (2005);
  Hahn and Then (2009/2010).  **What exactly do they state** — a sample size `e^{W_diss}` or
  `e^{relative entropy}` as a heuristic, a theorem, an asymptotic?  Is the *one-sidedness*
  (which direction of perturbation is reliable) stated as a theorem anywhere?
* Chatterjee and Diaconis, "The sample size required in importance sampling" (2018):
  the theorem (`e^{KL}` with fluctuation terms) — typical-case, at an instance; contrast
  with a class certificate (`e^{D_∞}`).  Agapiou, Papaspiliopoulos, Sanz-Alonso, Stuart,
  "Importance sampling: intrinsic dimension and computational cost" (2017): the
  `χ²`-based bound.  Any statement of the form "sample size `e^{D_p}`" for Rényi order `p`
  (e.g. in the literature on Rényi-divergence variational inference, on tempering /
  annealed importance sampling, or on rejection sampling for `D_∞`).
* Heavy-tailed mean estimation with a bounded `p`-th moment, `1 < p ≤ 2`: the minimax
  rate `M^{1/p} N^{−(p−1)/p}` (Bubeck, Cesa-Bianchi, Lugosi 2013; Devroye, Lerasle, Lugosi,
  Oliveira 2016; earlier: von Bahr–Esseen 1965) — **is O1 that rate, read backwards?**
* Sharp Hoeffding / Kearns–Saul / Bentkus-type constants for T1 (the exact maximum of
  `ln E e^Y − E Y` over laws on an interval).
* In computational protein design: provable ε-approximation of partition functions by
  enumeration with bounds (the K* family: Georgiev, Lilien, Donald 2008; Lilien et al.
  2005; BBK*, MARK*) — T2 with a *function* floor (pairwise lower bounds) is that
  scheme.  P2's report (`docs/science/workstreams/P2_REPORT.md` §4) has part of this; say
  what in T2–T4 is already there (a stopping criterion from an upper bound on the
  unenumerated mass?) and what is not (sampling with a certificate; lower bounds on the
  number of evaluations).

## Deliverable

`docs/science/workstreams/A3_REPORT.md`: per statement T1–T4, O1, O2 a classification
— **(1)** in print as stated (where, with the exact statement side by side), **(2)** a
known special case or a direct corollary (say the two lines that connect them), **(3)**
folklore without a locatable statement, **(4)** not found after the searches listed — and
the sentence the theory division (or we) should write, with citation.  A search log
(query, tool, date, what came back).  Reading levels on every source (`[full text]`,
`[abstract]`, `[search snippet]`, `[from memory — unverified]`).  **Never a bibliographic
detail you did not see.**  Also: anything in these sources that *contradicts* T1–T4 or
O1–O2, or a sharper known result we should adopt.  Criticism of the mathematics is
welcome but secondary; if you find an error in T1–T4 or O1–O2, give the counterexample.

## Rules

Write only in `experiments/science/ws_A3/` (notes, any small check scripts) and
`docs/science/workstreams/A3_REPORT.md`.  No state-changing git command.  Keep `NOTES.md`
from the first minute.  Start the report with "How far I got" and end with "What I could
not access".
