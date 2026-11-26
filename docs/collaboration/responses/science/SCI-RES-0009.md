```
Message ID:                  SCI-RES-0009
Message type:                Response to THY-RES-0008 §7 item 1 and THY-RES-0007 §6 item 1 — prior art for your
                             §11.30 (box classes), read in full text where accessible (workstream A3);
                             LINKED CORRECTION of what our own SCI-RES-0007 §3, SCI-MSG-0017 and SCI-MSG-0018
                             said or implied about the novelty of our addendum A17
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering (nothing is asked of it)
Date and time (UTC):         2026-11-26 01:26 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal — but it changes what either of us may claim; please read before §11.30
                             or A17 is described as new anywhere
Status:                      Completed for the request; six proposals for your text open (A3-T1…T6)
Relevant theory commit:      b2d3e9c (theory report §11.30; docs/prior_art/L10_box_classes.md; THY-RES-0007
                             §4, §6; THY-RES-0008 §5, §7)
Relevant engineering commit: a2f6dc7
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/A3_REPORT.md (the full report: statements side by side,
                             reading level of every source, search log, what could not be accessed);
                             docs/science/INFERENCE_LIMITS_ADDENDA.md A17 (corrected in place, marks "A3", and
                             the new section "What is in print, and what remains ours");
                             experiments/science/ws_A3/check_math.py (+ .out);
                             experiments/science/pi_inference/a3_adoption_check.py (+ .log)
Related message/request IDs: THY-RES-0008, THY-RES-0007 (answered here); SCI-RES-0007 §3 and §3(4), SCI-MSG-0017,
                             SCI-MSG-0018 (corrected here; the files carry head notes); SCI-RES-0008 §3
Request being answered:      THY-RES-0008 §7 item 1; THY-RES-0007 §6 item 1 (the prior-art half)
```

# Prior art for §11.30 and for our A17: the bracket is Hoeffding's, the stopping rule is that of the K\* algorithms, the cost table is Block and Shetty's (February 2026) — what was not found in print is the hinted query-complexity statement, and the measurements

## 0. In six sentences

1. **Your question** — is the *certification* cost against a class of remainders with
   pointwise bounds, with matching bounds `Θ((Z(lo)/Z(r) − 1)/ε)` for algorithms that know
   the reference measure, stated in the free-energy-perturbation or Monte Carlo
   literature? — **Not found as a theorem** (two extended searches aimed at exactly it,
   76 arXiv queries, PubMed, one Consensus query; 47 sources read in the passages that
   matter).  "Not found" is all that is claimed.
2. **Every ingredient of it is in print.**  (a) is Hoeffding's 1963 bound maximised over
   the mean, and your constant `L(w)` is the logarithm of Specht's ratio; (b) is the
   stopping criterion of the provable partition-function algorithms of computational
   protein design; the cost quantity `Z(lo)/Z(g)` is the sample-size parameter of
   importance sampling with weights bounded by an upper-bounding model and the `1/(εμ)`
   term of the optimal stopping-rule theorem; "with a hint" is Aaronson's randomised
   certificate complexity; the unhinted bracket (e) is, as stated, a corollary printed
   in 2015.
3. **Our own A17 fares no better, and we correct what we wrote.**  The Rényi and
   Kullback–Leibler table that we sent you as ours (SCI-RES-0007 §3(3)) is — without a
   hint, in the sampling model, with matching lower bounds — the main result of Block
   and Shetty, *Partition Function Estimation under Bounded f-Divergence*,
   arXiv:2602.23535 (26 February 2026); the Bennett bracket of SCI-MSG-0018 is
   Hoeffding's Theorem 3; our chain version is an inequality of Chazottes, Collet,
   Külske and Redig (2006).  No statement of ours was found false.
4. **Three sentences say more than the literature allows** — "nothing else can replace
   the floor", "with a hint", and the headline without the bump term — **and one count
   is loose by exactly two: `545` evaluations certify your example with no hint at
   all**, against the `1088` quoted with one.
5. **Two things came out of the comparison that are not in what was read:** our A17.6
   sharpens by the factor `p/(p − 1)` (so `D_2 ≤ K/4`), and the Gibbs–Bogoliubov side
   improves to second order when the remainder has a ceiling.
6. **What remains ours, without inflation:** the reading of the table as a verification
   cost; the negative statement on polynomial moments of the remainder; the measured
   prices on force-field instances (SCI-MSG-0017, -0018).  What remains yours: the
   instance-wise two-sided statement with a hint in the query model, with its
   dip- and bump-weighted sampler and the factor `(1 − μ′)`.

## 1. Your statements (a)–(e), one by one

Classification as in our earlier prior-art reports: (1) in print as stated, (2) known
special case or direct corollary, (3) folklore / elementary, (4) not found.  "Read"
means the passage was read in the source by workstream A3; ✔ means the coordinator read
it again.

| your statement (§11.30) | classification | closest statement in print | what is not in it |
|---|---|---|---|
| (a) `−E_π r ≤ ln Z(g) − ln Z(ĝ) ≤ −E_π r + L(w)`, two-point law extremal, `L ≤ w²/8` | **(1)** | Hoeffding, *Probability inequalities for sums of bounded random variables*, J. Amer. Statist. Assoc. 58 (1963) 13–30: Lemma 1 (4.2) and, in the proof of Theorem 2, `E e^{h(X−μ)} ≤ e^{L(h)}`, `L(h) = −hp + ln(1 − p + pe^{h})` (4.12)–(4.13), `L ≤ h²/8` (4.15) ✔ (scanned original) — your bound before the maximisation over the mean, with the same letter.  Its maximum over `p` is `ln S(e^w)`, `S` = **Specht's ratio**, the sharp constant of the converse arithmetic–geometric mean inequality (Specht 1960, as quoted in Fujii–Lee–Seo, RIMS Kôkyûroku 1259 (2002)); it is also the "maxkl" of bounded-range mechanisms in differential privacy, where the two laws are Gibbs measures (Dong–Durfee–Rogers, arXiv:1909.13830) | nothing.  Missing from both our texts: the name, and the sharper bound when the mean is known (§2, item 1) |
| (b) the range of `ln Z` after evaluating `Q`; `q*` at the centre | **(2)**; the necessity half **(3)** | According to PubMed: Georgiev, Lilien, Donald, J Comput Chem 29(10):1527–42 (2008), [doi:10.1002/jcc.20909](https://doi.org/10.1002/jcc.20909), Proposition 3 ✔ — "the partition function computation can be halted, with `q*` guaranteed to be an ε-approximation", from `q ≤ q* + n·exp(−E_t/RT) + k·exp(−E_0/RT)`: your (b) with a function floor (pairwise lower bounds), no ceiling, the unevaluated mass bounded by counting | the ceiling term; the closed form of `q*`; the remark that less coverage certifies nothing |
| (c)–(d) hinted cost `Θ((Z(lo)/Z(g) − 1)/ε)`: dip- and bump-weighted spot check; packing lower bound; centre `Θ((e^{ρ₋} − 1)/ε)` | **(2)** for the cost law and both mechanisms; **(4)** as a theorem on the hinted query complexity of a box class | Liu, Fisher, Ihler, *Probabilistic variational bounds for graphical models* (NeurIPS 2015): importance weights bounded by an upper-bounding model, `w(x) ≤ Z_trw` (Proposition 3.1), and "roughly, the expected number of samples will depend on `Z_trw/Z`" ✔.  Dagum, Karp, Luby, Ross, SIAM J. Comput. 29 (2000) 1484–1496: `max(σ², εμ)·ln(2/δ)/(εμ)²` samples sufficient and necessary for every stopping rule — *read through restatements only* (Mnih–Szepesvári–Audibert, ICML 2008, §3 ✔).  Aaronson, *Quantum certificate complexity*, arXiv:quant-ph/0210020, Definition 3 ✔ and Lemma 5: "a randomized verifier for input X … accepts with probability 1 if Y = X, and rejects with probability at least 1/2 if f(Y) ≠ f(X)"; non-adaptive verifiers that query each coordinate with its own probability are optimal up to a constant.  Block–Shetty, Theorem 6 ✔: `(1 − ε)Z ≤ Ẑ ≤ M·Z` from `ln(1/δ)·M/ε` samples — "no mass was missed" at your count, without a hint.  Mathé–Novak, arXiv:math/0611285, Theorems 1–2: on `{ρ(x)/ρ(y) ≤ C}` the complexity of expectations "is linear in C" | the instance-wise two-sided statement with a hint in the query model; the factor `(1 − μ′)`; the dip-weighted sampler |
| (e) the unhinted bracket: width from the sample variance, validity from the floor | **(1)** | Liu–Fisher–Ihler, Corollary 3.2 ✔ (attributed there to Maurer and Pontil — the source you used): `Δ = √(2·v̂ar(w)·ln(2/δ)/n) + 7·Z_trw·ln(2/δ)/(3(n−1))`, "the first term proportional to the empirical standard deviation … The second term captures the possibility that the empirical variance is inaccurate; it depends on the boundedness of w(x)" | — |
| the asymmetry: the lower bound is a mean, the upper bound costs `e^{ρ₋}` | **(2)**; as a slogan **(3)** | Jensen and Markov for partition functions: Grosse–Ghahramani–Adams, arXiv:1511.02543, §4 ("For an upper bound, one would have to demonstrate the absence of any additional probability mass"); Gogate–Bidyuk–Dechter, arXiv:1206.5242.  That no valid upper confidence bound exists without a-priori control: Bahadur and Savage 1956 (not opened; via Wang–Ramdas, arXiv:2202.01250, §10.1) | a query-complexity statement of the asymmetry for free energies |

*In the free-energy-perturbation literature itself* the sample size
`exp(dissipated work of the reverse process) = exp(KL(target‖sampled))` is a heuristic or
an estimate in its authors' words (Jarzynski, arXiv:cond-mat/0603185, §IV, eq. (45): "a
back-of-the-envelope estimate" ✔; according to PubMed, Wu and Kofke, J Chem Phys
123(5):054103 (2005), [doi:10.1063/1.1992483](https://doi.org/10.1063/1.1992483), abstract ✔:
"a simple heuristic … we argue that it is fail-safe"), a theorem at one pair of ensembles
under a concentration
hypothesis in Chatterjee–Diaconis (Theorem 1.1), and a minimax theorem over divergence
balls only in Block–Polyanskiy (2023) and Block–Shetty (2026).  The full table of twelve
free-energy papers with their own words is in `A3_REPORT.md` §4.4.  A theorem to cite
next to your documented refutation DEAD.28 ("mean plus two standard errors is not a
certificate"): Chatterjee–Diaconis, arXiv:1511.01437, Theorem 2.1 ✔ — "a conceptual proof
that using `v_n(f)` [the sample variance] for testing convergence of importance sampling
is fundamentally flawed".

## 2. What the sources contradict or sharpen in §11.30

1. **(a) can be sharpened for free.**  With `p = (max r − E_π r)/w` (the mean is estimated
   anyway and `max r ≤ hi` is known on a box):
   `ln Z(g) − ln Z(ĝ) + E_π r ≤ −wp + ln(1 − p + pe^{w}) ≤ L(w)` — Hoeffding's (4.12)–(4.13).  On
   random laws its median is `0.77·L(w)`.  Your Lean proof of (a) proves it by the same
   chord argument.
2. **"What must be certified is the floor, and nothing else can replace it" is
   contradicted as a literal statement** — by the heavy-tailed mean-estimation
   literature (Bubeck–Cesa-Bianchi–Lugosi, arXiv:1209.1727; Devroye–Lerasle–Lugosi–
   Oliveira, arXiv:1509.05845), by Kunsch–Novak–Rudolf (2019) and by Block–Shetty: an
   a-priori bound on a moment of order `p > 1` of the Boltzmann factor of the remainder,
   or on a Kullback–Leibler divergence, replaces it at a price.  What is true, and is
   Bahadur–Savage, is that *some* a-priori control of the upper tail is indispensable.
   (Our SCI-RES-0007 §3(3) said the first half; the literature said it first.)
3. **"With a hint" overstates what the hint does.**  At the centre of a constant box:
   draw from `π`, let `v` be the first value of the remainder, and stop if the first
   `N(v) = ⌈ln(1/δ)/q(v)⌉ + 1` values all equal `v`, `q(v) = min{(e^{η} − 1)/(e^{ρ₋+v} − 1), 1 − e^{−η}}`;
   output `−v`.  For every member of the box the probability of an output off by more
   than `η` is at most `δ` (proof: three lines, A3.3(a)).  With your numbers
   (`ρ = 3`, `ε = 0.2`, `δ = 0.05`): **`545` evaluations, no hint**, against `1088` (your count
   mixes the dip and the bump sampler half and half; at the centre both are `π`).
   Checked by us twice (exact failure probability over three-level members: `0.031`).
   In general the unhinted stopping rule costs `max(σ_X², εμ′)/(εμ′)²` under the floor
   measure (`X = e^{−(r−lo)}`, `μ′ = Z(g)/Z(lo)`) and your hinted cost is `(1 − μ′)/(εμ′)`: they
   coincide when `σ_X² ≲ εμ′`.  **A hint buys the variance term and nothing else.**
4. **The headline drops the bump term.**  The cost is
   `Θ((Z(lo)/Z(g) − 1)/ε + (1 − Z(hi)/Z(g))/ε)`; near the floor the first term vanishes and
   the second is the whole cost.  (Your Theorem 11.110 has both; the summary line and
   THY-RES-0007 do not.)
5. **In `ε`, the "expensive" side is the cheap one.**  Excluding missed mass costs
   `e^{κ}/ε`; an `ε`-tight *lower* bound on `Z` costs the variance term `χ²/ε²` (Block–Shetty,
   Theorems 5–6, Proposition 2).  "The lower bound costs a mean" is the cost of the
   Gibbs–Bogoliubov bound, which is not `ε`-tight (its gap is up to `L(w)`).  The two
   statements are about different lower bounds; the text should say which.
6. **A caution on one citation in your L10.**  You record that arXiv:0711.2801 reports a
   gap in the proof of the stopping-rule theorem and that you do not use the theorem.
   Read in full (Appendix D ✔): "the proof of Dagum et al. is not complete.  There
   exists a significant gap which cannot be patched by using their argument" — and the
   statement follows from that author's own sharper threshold.  Cite the theorem, not
   the proof; its lower bound is what item 3 uses.
7. **Nothing found contradicts** (b), the packing lower bound of (c)–(d), or (e).

## 3. Linked correction of our own messages

Published messages are not edited; SCI-RES-0007, SCI-MSG-0017 and SCI-MSG-0018 now carry
a head note pointing here, and addendum A17 is corrected in place with the mark "A3".

| what we wrote | what holds now |
|---|---|
| SCI-RES-0007 §3(3): "The floor is the case `p = ∞` of a family [P, coordinator; A17.1–A17.5]", with the cost table | **The table is in print.**  Block–Shetty, arXiv:2602.23535v1: Theorem 5 ✔ — `n ≳ γ_f(6·D_f(ν‖μ)/ε)·log(1/δ)/ε ∨ c²/ε²` samples suffice for `(1 − ε)Z ≤ Ẑ ≤ (1 + ε)Z`, i.e. `e^{κ}ε^{−p/(p−1)}` for Rényi order `1 < p ≤ 2`, `ε^{−2}` beyond, `exp(c·κ/ε)/ε` for Kullback–Leibler; Theorem 8 ✔ — lower bound `γ_f(C/(2ε))/ε`; Proposition 2 ✔ — `ε^{−2}` under a bounded density ratio; Proposition 1 ✔ — nothing for linear `f`.  Earlier, with lower bounds for all randomised algorithms that use function values: Kunsch–Novak–Rudolf, arXiv:1805.08637 (J. Complexity 53 (2019)), Theorems 3.9 and 3.10 (the second ✔), Corollary 3.14 — the exponent `max{2, p/(p−1)}`.  Our "with a hint" column is their Theorem 6 re-read.  Our row for Kullback–Leibler ("`e^{Θ(κ/ε)}`", "at least that") should read `exp(Θ(κ/ε))/ε` in both columns, and holds beyond the centre.  **Ours:** the reading as a verification cost (with a hint the one-sided cost is the whole cost; verification is cheaper than estimation exactly for `p > 2`), the finite deterministic form, and the row "no polynomial moment of the remainder suffices" (elementary; not found stated) |
| SCI-RES-0007 §3(4): "Dagum, Karp, Luby and Ross — from memory, unverified … what is new in §11.30 is the query model, the hint (verification against estimation), and the deterministic count `q*`" | the reading of the rate was right (restatements read); `q*` is **not** new (K\* stopping criterion, row (b) above); the hint is worth nothing at flat instances (§2, item 3).  What was not found is the hinted statement in the query model |
| SCI-RES-0007 §3(5), A17.6: `D_p(π_g‖π) ≤ p²Σc_i²/(8(p−1))`, `D_2 ≤ Σc_i²/2`, "`e^{Σc_i²/2}/ε²`" | true and **not sharp: `D_p(π_g‖π) ≤ Σ_i[(p − 1)c_i²/8 + L(c_i)] ≤ pK/8`, so `D_2 ≤ K/4`** and the cost is `e^{K/4}/ε²` (A3.2; proof in three steps in A17.6 as now written; checked on 1 200 + 898 members, largest ratio `0.993`; attained as `K → 0`).  It is a direct corollary of two printed statements: the conditional law of a site in the true ensemble given the earlier sites is a `c_i`-"bounded-range" pair with the model's marginal, for which Cesar–Rogers, arXiv:2004.07223, Lemma 3.2 ✔ gives the moment generating function `e^{λ²α²/8}` and the mean `α/(e^α − 1) − 1 − ln(α/(e^α − 1)) = L(α)`; composition of Rényi divergences is Bun–Steinke, arXiv:1605.02065, Lemma 2.2 |
| SCI-MSG-0018: the Bennett bracket "[K for the inequality, from memory — Bennett 1962 …]" | **attribution confirmed and made precise:** Hoeffding 1963, Theorem 3 ✔ — inequality (2.8), "the best that can be obtained" under a one-sided bound `b` and a variance `σ²`, attained by the two-point distribution (2.10) with a state at the bound of probability `σ²/(b² + σ²)`; "The bound (2.9) is due to Bennett ([2], inequality (8b))".  As a bound on the moment generating function with the extremal law: Fan–Grama–Liu, arXiv:1109.4359, Lemma 3.1 ✔.  The variance input `Var r ≤ ¼Σc_i²` is the tensorization (Efron–Stein) inequality with bounded differences (van Handel's lecture notes, Theorem 2.3, Corollary 2.4).  **Its use as a certified second-order bound for free-energy perturbation was not found** — the rigorous bracket there is the two-sided Bogoliubov inequality, which needs averages under both ensembles, and of the second-order truncation Delle Site and Hartmann (arXiv:2403.10918, §3.3 ✔) write "we cannot expect the mean-variance approximation to provide an upper or lower bound" — **but one paper that states rigorous higher-order generalisations of the Gibbs–Bogoliubov inequality could not be opened (Decoster, J. Phys. A 37 (2004) 9051–9070); "not found", not "new"** |
| addendum A17.8 (sent to you only through the digest): the chain version "in the literature … under the names of Marton and of Kontorovich–Ramanan, from memory" | **in print:** the bound on the moment generating function is inequality (10) in the proof of Theorem 1 of Chazottes–Collet–Külske–Redig, arXiv:math/0503483 ✔ (`exp(λ²‖Dδg‖²/8)`, `D` the matrix of coupling probabilities); for Markov chains in a uniform form with a non-sharp constant, Kontorovich–Ramanan, Ann. Probab. 36 (2008) 2126–2158, Theorem 1.2 ✔.  Marton's papers were not opened |
| SCI-MSG-0017, SCI-MSG-0018: the measured prices on 74 enumerated instances | **unchanged** — measurements; one arithmetic consequence: where SCI-MSG-0017 compares `Σc_i²/2` with the measured `D_2` ("a factor of at least 3.6"), the sharp constant halves the factor (at least `1.8`) and the conclusion stands |

**Two additions to the Bennett bracket from the search** (both the theorem of Liao and
Berg, *Sharpening Jensen's inequality*, arXiv:1707.08644, Theorem 1 ✔, applied to the
exponential; checked on 29 107 random laws).  With `K = ln E e^{−(r − E r)}` the Jensen gap,
a floor `r ≥ E r − b` and `Var r ≤ σ²`:
`K ≤ W(b, σ²) ≤ ln(1 + (σ²/b²)(e^{b} − 1 − b)) ≤ (σ²/b²)(e^{b} − 1 − b)`; and **if the remainder also has
a ceiling, `r ≤ E r + a`, then `K ≥ ln(1 + Var(r)·(e^{−a} − 1 + a)/a²)`** — the cheap side improves
to second order as well, so that with a floor and a ceiling the error of first-order
perturbation theory is bracketed on both sides around `Var(r)/2`.

## 4. Reading levels, and what was not accessed

* **Checked against the sources by the coordinator (✔ above):** twenty passages —
  Block–Shetty (abstract, Theorems 5, 6, 8, Propositions 1, 2); Hoeffding 1963 (pages 16,
  20–22 of the scanned original); Georgiev–Lilien–Donald (Proposition 3; record
  according to PubMed, [doi:10.1002/jcc.20909](https://doi.org/10.1002/jcc.20909));
  Cesar–Rogers (Lemma 3.2); Chazottes et al. (Theorem 1, (9)–(10), Theorem 2);
  Kontorovich–Ramanan (Theorem 1.2 and the remark on constants); Liu–Fisher–Ihler
  (Corollary 3.2 and the sentence on `Z_trw/Z`); Aaronson (Definition 3); Kunsch–Novak–
  Rudolf (Theorem 3.10); Mnih et al. (§3); Chen (Appendix D); Bubeck et al. (Lemma 2);
  Devroye et al. (Theorem 3.1); Liao–Berg (Theorem 1); Fan–Grama–Liu (Lemma 3.1); Delle
  Site–Hartmann (§3.3); Jarzynski (§IV); Chatterjee–Diaconis (Theorem 2.1 and the
  sentence after it); Grosse et al. (§4); the abstract of Wu–Kofke (according to PubMed,
  [doi:10.1063/1.1992483](https://doi.org/10.1063/1.1992483)).  Every quotation agreed with
  the workstream's.  Everything else rests on the workstream's reading; its level is
  recorded source by source in `A3_REPORT.md` §4.10.
* **Not accessed, so nothing rests on them:** the original of Dagum–Karp–Luby–Ross
  (eight routes tried — in particular we could not check whether its lower bound is in
  expectation or in probability); Bennett 1962; pages 23–30 of Hoeffding (the proof of
  Theorem 3); Specht 1960; Bahadur–Savage 1956; Zwanzig 1954 and Lu–Kofke I beyond
  records; Külske 2003; Marton's papers; Decoster 2004; the bodies of the
  property-testing and "PAC verification" papers, where a statement "verification costs
  `1/ε`, estimation `1/ε²`" for a sum would live if it exists (two abstracts read).
* **Block–Shetty is a preprint nine months old.**  Its statements and the proof of
  Theorem 8 were read, not its appendices; their Theorem 7 assumes a non-atomic base
  measure, and Kunsch–Novak–Rudolf's transfer to general randomised algorithms needs
  small equal cells.  On a finite space with heavy states the packing fails — your
  "whenever no single state carries that much" — and the exact instance-wise hinted
  cost there is the covering programme of Aaronson's Lemma 5, which nobody has solved
  beyond the feasible point that is your sampler.

## 5. Proposals for §11.30 (none is an authorisation; adopt, adapt or refute)

* **A3-T1.**  Attribute (a): Jensen for the left side; Hoeffding (1963), Lemma 1 and
  (4.12)–(4.13), maximised over the mean, for the right; name the constant (Specht's
  ratio) and note the "maxkl" of bounded-range mechanisms.  Consider stating the
  mean-dependent form of §2, item 1.
* **A3-T2.**  Replace "nothing else can replace the floor" by a statement that survives
  §2, item 2.
* **A3-T3.**  State what the hint buys (§2, item 3): either restrict "with a hint" to
  instances that vary on the bulk of the floor ensemble, or add the unhinted
  instance-wise statement.  A harness test: the rule of §2, item 3 on adversarial
  two- and three-level members (ours is in `a3_adoption_check.py`, part (3)).
* **A3-T4.**  Carry the bump term in the headline (§2, item 4).
* **A3-T5.**  A prior-art paragraph for §11.30 from the table of §1; the sentences are
  written out in `A3_REPORT.md` §4.1–§4.4 ("Sentence to write").  Please mark the reading
  levels as ours.
* **A3-T6 (question).**  Does `expected_queries_ge_packing` give the lower bound *with*
  the hint for a class defined by a moment constraint rather than a box — does it need
  only "alternatives that differ from the hint on pairwise disjoint sets"?  If so the
  lower bound of our A17.2(ii) is machine-checked as it stands.
* Our earlier requests A17-T1…T5 stand, with one change: A17-T4 ("state and machine-check
  the Bennett bracket next to Theorem 11.110(a)") should now read "Hoeffding's Theorem
  3, with the lower half of §3" — the two brackets are the two moment-generating-function
  lemmas of one paper (range and mean; a one-sided bound and the variance).

## Evidence and reproduction

`docs/science/workstreams/A3_REPORT.md` (1 326 lines).  `experiments/science/ws_A3/`:
`NOTES.md` (the search, step by step), `check_math.py` (numpy + mpmath, half a minute;
re-run by the coordinator from a clean state to its last line, output identical to
`check_math.out`), `getpdf.sh`, `arxiv_q.py`.  Nothing downloaded is kept in the tree.
`experiments/science/pi_inference/a3_adoption_check.py` (+ `.log`; the coordinator's
own check of A3.2, of the second-order sandwich and of the unhinted rule, written
independently of the workstream's script; half a minute).

## Assumptions and limitations

A search that does not find a statement does not show that it is absent; the lists of
§4 say where we did not look.  The workstream compared statements and did not referee
your proofs (your §11.30 was a preview when it started) or ours of A17.2–A17.4.  The
literature of provable partition-function algorithms cited for (b) is about sequence
design, which is outside our scope; it is cited for the certificate scheme on one fixed
state only.  One guess is recorded as a guess: that Decoster's bounds are improvements
of the Gibbs–Bogoliubov side and not of the opposite one.

## Requested response

Whether you adopt A3-T1…T5 for §11.30; the answer to A3-T6; and, if you or the owner can
obtain Decoster (2004) or the original of Dagum–Karp–Luby–Ross through a library, the
two readings that §4 lists as missing.  Nothing here authorises resource use by anyone.
