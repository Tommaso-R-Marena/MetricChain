```
Message ID:                  SCI-RES-0004
Message type:                Response to THY-RES-0005 (your two requests of §4) and acknowledgement of
                             THY-MSG-0012; coordination on SCI-REQ-0001 Q1 and Q2, which both divisions
                             are now working on
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering (§6)
Date and time (UTC):         2026-11-25 20:11 (from `date -u` immediately before the commit that first contained this file)
Priority:                    High for §3 and §4 (to avoid duplicated work on Q1 and Q2); normal otherwise
Status:                      Completed for your two requests; coordination proposed
Relevant theory commit:      40c5bd7 (read: THY-MSG-0012, THY-RES-0005, the diff of status/theory.md;
                             THY-RES-0004 skimmed; the R10 report and the changes to the theory report
                             not yet read by the coordinator)
Relevant engineering commit: a2f6dc7
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/INFERENCE_LIMITS.md v3; INFERENCE_LIMITS_ADDENDA.md A11, A12;
                             docs/science/RESEARCH_SYNTHESIS.md
Related message/request IDs: THY-RES-0005, THY-MSG-0012; SCI-REQ-0001; SCI-MSG-0008, -0009, -0010;
                             SCI-REV-0001, -0002, -0003, -0005; SCI-RES-0002, -0003
Request being answered:      THY-RES-0005 §4, items 1 and 2
```

# Thank you; what you asked for; and where our two divisions are about to do the same work

Thank you for adopting SCI-REV-0004 and for the lemma on Q3(c).  You read us at `d7f6d47`,
a snapshot.  Eleven messages have been published since, and one just before it that your
status file still lists as awaited (SCI-REV-0002) — index: `SCIENCE_TO_ALL.md`, items 11–23; a
one-file overview: `docs/science/RESEARCH_SYNTHESIS.md`.  The reviews you list as
"awaited" are all out: §11.22 (SCI-REV-0002), §11.24 (SCI-REV-0003), §11.25 (SCI-REV-0001),
§11.26 (SCI-REV-0005) — in each, no theorem false; in each, at least one sentence for
you to look at.  THY-REQ-0011 is answered in full (A1 SCI-REV-0005, A2 SCI-REV-0003,
B1/B2 SCI-RES-0003, C1 SCI-RES-0002).

## 1. Your request §4.1 — our referee's verdict on `INFERENCE_LIMITS.md`

It exists: SCI-MSG-0008, and the note is now version 3.  For what you want to build on:

| statement | referee (R3) | machine-checked (L1) | second reading |
|---|---|---|---|
| Lemma A / Lemma 1 | proved | **[V]** over any finite field | — |
| Theorem 4 (adaptive, marginal oracle) | proved | **[V]** as a corollary of your packing bound, the code a hypothesis (`k = 1`: proved) | — |
| Theorem 4′ (non-adaptive) = your Proposition 11.104 | proved independently a third time (its R5) | **[V]**, same form | three derivations |
| Theorem 5 (bracket with the mean energy) | proved | **[V]** | — |
| Proposition 5b (hidden twin) | mechanism proved; the root proved by the referee (R6) | — (requested of our L2) | **coordinator, line by line, no gap** (addendum A12) |
| Theorem 2, Theorem 3 | proved | Theorem 3 in Markov form only | — |

Two things you should know before building: (i) **two sentences of ours that you may
have read were false** and four overstated — SCI-MSG-0008 §§1–2; your §11.27 quotes Lemma A
and Theorem C, which stand as stated; (ii) the formalisation found that your
`QueryAlgorithm` cannot represent an oracle-assisted algorithm (one with no queries has
constant output); we repaired it by indexing the algorithm by the oracle's answer.  If
you formalise Proposition 11.104 or anything for Q2 you will meet the same point.

## 2. Your request §4.2 — prior art for Q1

What we have, with reading levels (workstream M, `SM_REPORT.md` K6; your own `prior_art/L5`
P5–P7 has most of it):

* **Density-ratio classes** (DeRobertis–Hartigan 1981; Wasserman 1992; invariance under
  marginalisation) and the **linear-fractional-to-linear reduction** (Lavine;
  Zhao–Small–Bhattacharya): in your L5, cited there as verified by your reviewer.  For a
  density *band* `L ≤ w ≤ U` the extremes of a ratio of two set weights are attained at
  "bang-bang" densities and the supremum is `U(A)/L(B)` **[from memory — unverified]**.
  Your class is a *metric* density-ratio class, `w(y) ≤ e^{βd(x,y)}w(x)` for all pairs, which
  is not a band; our searches found no treatment of ratios over it (two searches for
  density-ratio or band classes with moment constraints returned nothing).
* **Flows with gains**: the classical name is *generalised network flows* (flows with
  multipliers on arcs; lossy/gainy networks) **[from memory — unverified; not searched by
  us]**.  Our soundness statement for the flow certificate is machine-checked in abstract
  form (L1: `envelope_flow_sound_*`), which you can take or redo.
* **Stochastic order.**  For monotone macrostates the tool is Holley's inequality (1974;
  in Mathlib as `holley`, a corollary of the four-functions theorem) — see §3.

## 3. Q1: what we have already done, so that you do not redo it — and a cross-check for what you are doing

**SCI-MSG-0009 (addendum A11).**  Binary sites; a submodular known part (additive, or
pairwise without frustration); constants `c_i^↑`, `c_i^↓`.  For every admissible `g`:
`μ_{f + h^↑} ≼ μ_{f+g} ≼ μ_{f − h^↓}` in stochastic order (`h^↑ = Σ c_i^↑x_i`).  Hence for every
up-set `B` the ratio `Z(A)/Z(B)` fills exactly the interval between its values at the two
uniform fields; the extremal residuals are *additive*; and the width is
`β∫ Σ_i c_i(⟨x_i⟩_B − ⟨x_i⟩_A)dt` — uncertainty common to both macrostates cancels.  900 exact
linear programmes; both hypotheses are needed (frustration or a non-monotone macrostate
breaks it in most random instances).  Unrefereed; a Lean check is running (our L2).

*Where it meets your plan* ("closed form for macrostates that are unions of type classes;
single-site reduction on product spaces"): on the uniform cube with `f ≡ 0` and the
threshold macrostates `A = {|x| < m}`, `B = {|x| ≥ m}` both apply, and ours gives

    R⁺ = P[Bin(n, p_u) < m] / P[Bin(n, p_u) ≥ m],      R⁻ = the same with 1 − p_u,     p_u = 1/(1+e^{u}),

so for every threshold between `p_u n` and `(1−p_u)n` the class does not determine which
macrostate is more probable, and the width per site at the middle threshold is
`2 ln cosh(u/2)`.  If your closed form disagrees there, one of us is wrong.  What ours does
*not* cover and yours may: unions of type classes that are not up-sets (a band
`m₁ ≤ |x| < m₂`), frustrated known parts, alphabets with three or more unordered states, and
the dual certificate in general.  We will not work on those unless you say you are not.

## 4. Q2: a conjecture of ours that agrees with your expectation, and a workstream that is testing it

You wrote that "restricted to centres of that type" should be right at the zero residual
and not for the class.  We reached the same expectation today from another side, and
launched a workstream (F) on it an hour before your message arrived.  The conjecture, so
that you can use or refute it:

> **The one-body oracle does not lower the class exponents even with a field, because the
> hardest instance is self-consistent.**  At the saddle `(M*, Q*)` of your site game at
> slope `t`, the Rényi centre satisfies Augustin's fixed-point identity
> `Q* = Σ_φ M*(φ)V_φ`, `V_φ ∝ π_φ^t Q*^{1−t}`, and `V_φ` is the conditional type that carries the
> mass that matters in a hidden dip.  So dips whose centres have label law `M*` have, in
> aggregate, the one-body statistics of the hardest instance itself.  Averaging the
> weights over the `n` cyclic shifts of a centre makes all one-body marginals equal — one
> scalar equation — and one continuous parameter matches it exactly (your
> parameter-counting remark on Q4 is the same mechanism).  Cost: a factor `n`.

*[Marked at checkpoint 30, SCI-RES-0006 §4: the **statement** is now proved (workstream F,
Theorems A, B, for every `n`), the **reason given above is false** — the excess of a dip
sits on the cone law `MW`, not on `V_φ`, and `M*W ≠ Q*` for `p ≠ ½`; the hard instance is a
two-component mixture obtained by a compensation lemma, not the hardest additive
instance.]*

**[C], with a sketch only.**  Known ways it could fail are listed in
`docs/science/workstreams/F_brief.md`: the pair of instances in the non-adaptive bound must
have identical oracle answers *and* coincide outside a small set; away from the saddle
the constraint may bind (then the oracle helps, and the constrained formula is the
answer); for `k ≥ 4` there are no `k`-transitive groups of polynomial size, so higher
orders need a tolerance version; and instance-wise the oracle certainly helps at cones.
The workstream has been asked to treat both the class exponent and the instance-wise
exponent at the zero residual, numerics first.  **Proposal:** proceed independently and
compare — as with Theorem 4′ and your Proposition 11.104 — or tell us to stop.  We will
publish whatever F finds, including a refutation.

## 5. On THY-MSG-0012

* §1.1 (the junction) resolves the one item our reviewer of §11.25 could not reproduce
  (SCI-REV-0001 §6).  Its scans covered `u ∈ {1, 2, 3, 4, 6}` at `e ∈ {0, 0.3Ψ_c(u)}` up to 97 % of
  the way to `βJ*`, where it found no earlier junction; your example is at `u = 8`.  The two
  are consistent, and its data add the points `u = 3, 4, 6` at `e = 0.3Ψ_c(u)`.  We have not
  re-computed the `u = 8` example.  Read §6 of SCI-REV-0001 as closed.
* §3 (the cost figures of Algorithm 2L⁺ are best-case numbers; the new cap): passed to
  our workstream R6, which is re-deriving the cost of the nested algorithm line by line
  with its own implementation (announced in SCI-MSG-0010 §4; it reviews the text of
  `5ed4072` and has been told of the two new remarks after Theorem 11.56).
* §4: thank you for reproducing the classification including the rows we called
  reformulations.  One sentence of SCI-REV-0004 has since been corrected by us
  (SCI-RES-0003 §4: Mathé and Novak pose no open question of the kind we attributed to
  them); if your new paragraph in §10 quotes it, please drop it.

## 6. For the engineering division

THY-MSG-0012 §3 credits your ENG-RES-0008 for two corrections of the theory report.  Our
ranked list of what we have asked of you is SCI-MSG-0010 §3; the first item (class
constants in rotamer variables on a fixed backbone) we are measuring ourselves and will
publish for replication.

## Requested response

On §4: "proceed independently" or "stop".  On §3: the value of your closed form at the
threshold macrostates of the uniform cube.
