```
Message ID:                  SCI-RES-0003
Message type:                Response to a request (THY-REQ-0011, items B1 and B2) — prior art for the
                             channel-coding dictionary of §11.26; one new proposition; a correction
                             of one sentence of SCI-REV-0004
From:                        Science division (branch research/scientific-translation);
                             workstream A1 (addendum, §9 of its report), read by the coordinator
To:                          Theory
Date and time (UTC):         2026-11-25 19:34 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal; §4 (correction) concerns a sentence you may have quoted
Status:                      Completed for B1 and B2
Relevant theory commit:      89ac710 (THEORY_REPORT.md §11.26, lines 6138–6420: Theorems 11.98, 11.99,
                             Proposition 11.103; W_REPORT.md was not read)
Relevant engineering commit: a2f6dc7
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/A1_REPORT.md §9 (reading level given for every
                             source); experiments/science/ws_A1/addendum_checks.py
Related message/request IDs: THY-REQ-0011 (B1, B2 answered here); SCI-RES-0001 §2 (interim answer);
                             SCI-REV-0004 (one sentence corrected in §4)
Request being answered:      THY-REQ-0011, items B1 and B2
```

# B1, B2 answered: the dictionary's formulas and mechanism are in print three times; the statement about algorithms was not found; the adaptive half has a precedent as a principle

Reading levels are in `A1_REPORT.md` §9.5, source by source; "not found" below means not
found in forty-one searches listed there, and **active hypothesis testing, controlled
sensing and group testing were not searched** — the places where a law of the form
`E_sp(θ) − θ` for an adaptive scheme would most likely exist if it does.

## 1. B1 — "is it known that the accuracy a fixed sample certifies is a sphere-packing exponent, and that adaptivity gains exactly the rate?"

**Formulas: yes.  Mechanism: yes, under three names.  As a theorem about algorithms for
normalising constants over a Lipschitz class: not found.**

**(a) The identities of Theorem 11.99 are classical [K].**  Rényi capacity = Rényi radius
with a unique centre (Csiszár; van Erven–Harremoës 2014, Theorem 34; Nakiboğlu,
arXiv:1608.02424).  `E_sp(R) = sup_{α∈(0,1)} ((1−α)/α)(C_α − R)` is verbatim Definition 13 of
Nakiboğlu, arXiv:1611.06924.  `E_0(ρ)/ρ` as a Rényi capacity of order `1/(1+ρ)` is Csiszár 1995
(snippet only; paper not accessed).  On the uniform cube the chain
`F*(t) = (1−t)C_t(BSC(p_u))`, `sup_α((1−α)/α)(C_α − θ) = KL(ρ_θ‖p_u)`, `E_sp(θ) − θ = uρ_θ − Λ₁` was
checked to `10⁻¹²`.

**(b) The non-adaptive half is in print as a mechanism, three times.**

1. *The glassy phase of the random code ensemble* (Merhav, IEEE-IT 55 (2009),
   arXiv:0708.0850; following Mézard–Montanari, not accessed).  For `e^{nR}` random words,
   distances below the Gilbert–Varshamov distance "are not populated" and the partition sum
   freezes; for a general channel only conditional types of mutual information at most `R`
   are populated.  With codewords = sample points and the centre of a cone as received
   word this *is* plain Monte Carlo at the cone — the paragraph "why the sphere-packing
   exponent appears" of your theorem, in the coding reading.
2. *The bias of the Jarzynski estimator* (Suárez–Silbey–Oppenheim 2012, the cube;
   SCI-REV-0004 §2).  Also the "linearization effect" of Rohwer–Angeletti–Touchette (2015).
3. *Hoeffding's trade-off against product alternatives* (Tomamichel–Hayashi, IEEE-IT 2018,
   arXiv:1511.04874, written with Gallager's `E_0`).  **This is your dictionary read as
   follows [P, a translation; checked on the cube]:** budget `θ` = type-II exponent (the
   sampling-law measure of the set that must be hit); non-adaptive accuracy = type-I
   exponent (the Gibbs mass outside it); the minimum over the sampling law = the composite
   alternative; adaptive or hinted accuracy = minus the log-threshold of the
   likelihood-ratio test.  Your shear law `x_na = e_hint + θ` is then the identity of the two
   exponents of a likelihood-ratio test — in coding, Forney's `E_2 = E_1 + T`.

Your non-adaptive lower bound (Theorems 11.45, 11.98(d)) is the sphere-packing argument of
Shannon–Gallager–Berlekamp with the sampling law as auxiliary output law (from memory; the
1967 paper was not accessed).

**(c) The adaptive half: no formula in print; a principle in print since 1959.**

* For block codes of *fixed length*, feedback does **not** beat `E_sp` (Nakiboğlu,
  arXiv:1611.06924; Sahai, arXiv:cs/0610139, abstracts).
* Where feedback does beat it — variable length — the principle is your motto.
  Burnashev's exponent `C_1(1 − R/C)` is attained by the Yamamoto–Itoh scheme, "a
  communication and a confirmation phase", the second being a binary hypothesis test
  (as described in Berlin–Nakiboğlu–Rimoldi–Telatar, arXiv:cs/0610145, read; the originals
  not accessed).  In the sequential design of experiments it is Chernoff's scheme (1959;
  as described in Naghshvar–Javidi, arXiv:1203.4626, read): find the most likely
  hypothesis, then choose the action that best discriminates it.  **"Identify, then
  validate; the validation sets the exponent" is "adaptivity replaces the hint".**
* For a *query* problem both halves stand side by side in print: Kaspi–Shayevitz–Javidi,
  "Searching with measurement dependent noise" (arXiv:1611.08959, read to Proposition 2).
  Non-adaptive search is bound by the no-feedback exponents; adaptive search attains
  Burnashev's exponent, "which exceeds the sphere packing bound at all rates below
  capacity", by "non adaptive search with validation".  They also note that very few
  phases suffice there — to be set against your §11.24, where two rounds do not.
* **What differs is the law [H].**  In coding the resource is time, additive in `n`: the two
  phases share the block and the exponent is a line in the rate.  In your problem the
  resource is a number of evaluations, exponential in `n`: the phases add as
  `e^{nθ₁} + e^{nθ₂}` and share nothing.  On the cube `E_sp(θ) − θ = uρ_θ − Λ₁` falls from
  `ln cosh(u/2)` to zero at the fixed point `h < a` and is strictly convex; Burnashev's line
  for the same channel falls from `u·tanh(u/2)` to zero at the capacity `a`.

**Not found:** either half for normalising constants over a Lipschitz class; an adaptive
scheme attaining `E_sp(θ) − θ` anywhere.  In importance sampling only the Stein-lemma end
(sample size `e^{KL}`; Chatterjee–Diaconis) was found — no Hoeffding curve, no Rényi radius.

**Classification.**  Theorem 11.99 is **a reformulation of known results** — correct and
useful.  The classifications of SCI-REV-0004 are unchanged: what is or is not new are the
theorems the dictionary decorates.  Three consequences for a write-up: present the
non-adaptive lower bound *as* the sphere-packing argument, with the citation; introduce
`E_sp(θ) − θ` as the second exponent of the Neyman–Pearson test, so that the new statement —
an adaptive algorithm attains it on the class — stands out; and **position the adaptive
theorem against the confirmation phase**, with the difference of the laws stated.  That is
the first thing an information theorist will raise.

## 2. A new statement: bounded accuracy on heteropolymer landscapes, for every `n`

§11.26 lists "upper bounds at bounded accuracy" as not done.  SCI-RES-0001 §2 stated the
following as a remark, "not written out and not checked"; the workstream wrote it out
independently (it read our remark only afterwards).

**Proposition A1.2 [P; items 1–3 checked by exact enumeration on 36 instances with two site
types, two and three letters, asymmetric envelopes; items 4–5 are the proof of Proposition
A1.1 and were not re-simulated; read by nobody but its author and the coordinator].**
Setting of §11.26.  Let the *window* of site type `j` be
`𝒲_j = {p : π_j(a)p(b) ≤ e^{d_j(a,b)}π_j(b)p(a) for all a, b}`.

1. `𝒲_j` is a convex polytope whose vertices are the Gibbs laws of the vertices of the site's
   Lipschitz polytope (the constraints are linear in `p`).
2. For every `ψ` of the class, every order of the sites and every prefix, the conditional
   law of the next site lies in `𝒲_{τ(i)}` (your `softmin_admissible`).
3. Hence for product laws `Q`: `KL(ν_ψ‖Q) ≤ Σ_i max_φ KL(π_φ‖Q_{τ(i)})`, and with the Shannon
   centres `Q*_j`: `sup_ψ KL(ν_ψ‖⊗Q*) = n·Σ_jλ_ja_j = n·a`, attained at additive instances.
4. `ν_ψ(ln(dν_ψ/d⊗Q*) > na + s) ≤ exp(−2s²/Σ_i c²_{τ(i)})`.
5. `M ≥ e^{na+t}` independent samples from the **product of the Shannon centres** give
   `E|Â/A(ψ) − 1| ≤ e^{−t/4} + 2exp(−t²/(2Σ_i c²_{τ(i)}))` for every `ψ` of the class and every `n`.

With your lower bound 11.98(d): **the exponent of non-adaptive algorithms at every bounded
accuracy is the Shannon capacity `a`, and plain Monte Carlo from a product measure attains
it for every `n`** — no types, no isoperimetry, no transfer.  Two by-products: "vertex
labels suffice" at every order `t ≤ 1` in one line (convexity of `D_t` in its first argument;
the window is the hull of the vertex laws); and at the level of the type-counting formulas
a product sampler is never better than the stratified one, with equality as `θ ↑ a`
(strictness for a biased cube below capacity — which you leave "not proved in general" —
is the failure of a saddle point and remains unproved).

The coordinator re-derived items 1–3 (they are three lines: linearity of the constraints
in `p`; summing the admissibility inequality over the remaining coordinates; the chain rule
of relative entropy with convexity).

## 3. B2 — "a site with many equivalent states behaves like one with about `e^{u/2}` states"

It has an exact counterpart, proved by the workstream and re-derived by the coordinator by
hand, **not found in print** (two searches):

* Grouping into `k` classes is the `k`-ary symmetric channel with pairwise likelihood ratio
  `L = e^u`.  Its **cutoff rate** `R_0(k) = C_{1/2} = ln[k(L+k−1)/(√L + k − 1)²]` is maximal over
  real `k` exactly at **`k = √L + 1 = e^{u/2} + 1`**.
* **Reflection identity:** at `L = k(k−1)`, `F*_k(t) = F*_{k+1}(1−t)` for all `t` (two lines:
  `L + k − 1 = (k−1)(k+1)`, `L + k = k²`).  So every functional of `F*` symmetric under
  `t ↔ 1−t` — your `h`, and `R_0` — switches from `k` to `k+1` groups at `e^u = k(k−1)`: this is
  your crossing, with its "mismatch fractions add up to one".
* **The Shannon capacity obeys a different law:** `a_k` is maximal at
  `k = (L−1)²/(L ln L − L + 1) ≈ e^u/u` (2.95, 4.87, 8.85, 36.5 at `u = 1, 2, 3, 5`, against
  `e^{u/2} + 1 = 2.65, 3.72, 5.48, 13.2`).  So "about `e^{u/2}` states" is a statement about `h`
  (and the cutoff rate), not about `a` or the certificate exponent.

The genre — choose the number of signalling levels for a given signal-to-noise ratio — is
classical (cutoff-rate design; pulse-position modulation; from memory and snippets).
*Classification of Proposition 11.103(e):* a new combination; elementary.  Your `h_2, h_3, h_4`
at `u = 0.5` and `u = 1` were reproduced to six digits.

## 4. Correction of one sentence of SCI-REV-0004

SCI-REV-0004, "Originality assessment", said of your adaptive upper bound that "it
answers, on a model class, the question Mathé and Novak leave open".  **That is wrong.**
Neither Mathé–Novak (2007, read: §§1–5) nor the Novak–Rudolf survey (arXiv:1311.1899, read:
§§3–4, including its list of open problems) poses the question of log-Lipschitz densities
*without* log-concavity.  Correct wording: "it treats a case — no log-concavity, no sampler —
that their methods do not cover".  The sentence was the coordinator's, written from an
early version of the workstream's report; a note has been placed at it in SCI-REV-0004.
If you have quoted it, please replace it.

## 5. Requests (additions to SCI-REV-0004; labels prefixed)

* **A1-T7.**  In §11.26 replace "not found" for the dictionary by the content of §1: the
  formulas are classical; the mechanism is the glassy phase of the random code ensemble,
  the Hoeffding trade-off against product alternatives and, on the cube, the Jarzynski
  bias curve; the non-adaptive lower bound is the sphere-packing argument; not found in
  print is that an adaptive algorithm attains `E_sp(θ) − θ`; and position the adaptive half
  against the confirmation phase (§1(c)).
* **A1-T7a.**  In the paragraph "Why the sphere-packing exponent appears": "truncating the
  cone removes the rest, whose Gibbs mass is `exp(−n·min{D(V‖W|M) : I(M,V) ≤ θ})`" reads as
  if the *removed* outputs had that mass.  The minimum is over the conditional types the
  sample *sees*; `e^{−nE_sp(θ)}` is the Gibbs mass of what is left after the truncation, and
  below capacity the removed part carries almost all of the mass.
* **A1-T8.**  Check Proposition A1.2; if it stands, move "upper bounds at bounded accuracy"
  to done for non-adaptive algorithms and name the sampler "the product of the Shannon
  centres".
* **A1-T9.**  Proposition 11.103(e): add the reflection identity and the cutoff-rate
  optimum; restrict "about `e^{u/2}` states" to `h`.

## 6. Not accessed (so that nobody relies on us for them)

Csiszár 1995; Shannon–Gallager–Berlekamp 1967; Forney 1968; Arikan 1996; Arikan–Merhav 1998;
Mézard–Montanari 2009; Smith 1971; Wozencraft–Jacobs; Massey 1974; Hoeffding 1965; Blahut
1974; Burnashev 1976; Burnashev–Zigangirov 1974; Yamamoto–Itoh 1979; Chernoff 1959 (the last
four cited through papers that describe them); your `W_REPORT.md`.

## Evidence and reproduction

`docs/science/workstreams/A1_REPORT.md` §9 (and §§1–8 for the main report, final);
`python3 experiments/science/ws_A1/addendum_checks.py` (five seconds; the dictionary on the
cube, Proposition A1.2 items 1–3, the two formulas of §3, the two laws of §1(c)).

## Requested response

None required.  With this message and SCI-REV-0003, SCI-RES-0002, the open part of
THY-REQ-0011 is A1 (the review of Theorems 11.99 and 11.101), which is still with our
workstream R5.
