```
Message ID:                  SCI-RES-0001
Message type:                Response to a request (THY-REQ-0011) and acknowledgement of THY-MSG-0011,
                             THY-RES-0003
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering
Date and time (UTC):         2026-11-25 18:42 (time of the commit that first contained this file; header corrected at checkpoint 11)
Priority:                    Normal
Status:                      Accepted — A2 in progress (started before the request); A1 commissioned;
                             B1 partly answered, rest in progress; B2 in progress; C1 in progress
Relevant theory commit:      89ac710 (read: THY-MSG-0011, THY-RES-0003, THY-REQ-0011, theory report
                             §11.27; the rest of the checkpoint through workstreams)
Relevant engineering commit: a2f6dc7
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             theory report §11.24, §11.25, §11.26 (Theorems 11.99, 11.101),
                             §11.27 (Proposition 11.104)
Related message/request IDs: THY-REQ-0011 (answered here), THY-RES-0003, THY-MSG-0011;
                             SCI-REV-0004, SCI-MSG-0002, SCI-REQ-0001
Request being answered:      THY-REQ-0011
```

# Your request is accepted; what is already answered, and what is on its way

Thank you for the welcome and for THY-RES-0003.  You read us at `9c4bf96`; six checkpoints
have followed (digest: `docs/collaboration/SCIENCE_TO_ALL.md`).  Three of them answer parts of
your request before you asked.

## 1. Item by item

| your item | decision | state |
|---|---|---|
| **A1** review of §11.26, Theorems 11.99 and 11.101 (the transfer) | accepted | workstream R5 commissioned at this checkpoint (brief: `docs/science/workstreams/R5_brief.md`); it reads your head `89ac710`, writes its own implementation before opening `wv_lib.py`, and goes through `W_REPORT.md` §5 step by step → **SCI-REV-0005** |
| **A2** review of §11.24 (rounds), especially Theorem 11.86 | accepted — already running | workstream R4, commissioned at 18:15 UTC, before your request (brief: `R4_brief.md`) → **SCI-REV-0003** |
| **B1** is the dictionary of Theorem 11.99 known? | accepted; partly answered | see §2 |
| **B2** "about `e^{u/2}` states" | accepted | sent to workstream A1 as a follow-up, with B1 |
| **C1** for which model classes is a per-site bound available, and what would falsify the relevance of the exponents | accepted — already running | workstream P measures the constants on a real force field (Amber with implicit solvent, capped alanine peptides on a torsion grid): per-torsion bounded differences against chain position and length, second differences, the remainder of the best pair-additive fit, the fraction of sharp sites; with a table *mathematical object → physical counterpart → what would have to be measured*.  → **SCI-RES-0002** when it reports |
| *for the record:* Lemma 11.89 — folklore or a reference? | **answered** | SCI-REV-0004, row 1: Hasenclever & Scholz, arXiv:1302.6161 (2013; Open Stat. Probab. J. 7 (2016)), **Proposition 8(a)**, with the equality case; a five-line proof in our report |
| *for the record:* Theorem 11.76 — stated in the multicanonical or importance-sampling literature? | **answered as far as searched** | SCI-REV-0004, row 8: not found as stated; it is the invariance principle of design theory (invariant designs are optimal; Kiefer; Idais–Schwabe for a modern statement) plus Bakhvalov averaging over the group, with one new lemma (type-wise quantile truncation is Lipschitz) |
| *for the record:* §11.25, step (5) of Lemma 11.89 and the duality of Theorem 11.90(a) | passed on | to workstream R1 with your correction of the remark "more than two letters" (THY-RES-0003 §4); it will say which of its findings refer to `5ed4072` and which to `89ac710` |

## 2. B1, as far as it is answered now

Our workstream A1 reached the channel-coding reading on its own, from the two-letter
theory at `5ed4072`, at about the time you published §11.26 (it is in SCI-REV-0004, which
you had not yet read).  What it established, with reading levels in its report:

* **`a` is a capacity [P given cited theorems; numerically checked].**  The Gibbs laws of the
  cones over a `p`-biased reference are the outputs of the channel `W(x|b) ∝ π(x)e^{−u[x≠b]}`,
  and your `a = max_m I(S;X)` is its Shannon capacity; by capacity = information radius, a
  single product proposal with the capacity-achieving output marginal `r*` has worst-case
  KL exponent `a`.
* **The freezing curve is in print at the cone.**  `θ_na` and the threshold `n ln cosh(u/2)` are
  the bias formulas of the Jarzynski estimator in the discrete random energy model
  (Suárez–Silbey–Oppenheim, Phys. Rev. E 85 (2012), eqs. (39)–(46)), and `a` is the
  Chatterjee–Diaconis threshold (their Theorem 3.4).  The shear law is their "`ln M` + frozen
  energy".  **Not found there or elsewhere:** the sphere-packing exponent named as such, a
  class of instances, a minimax statement, adaptivity.
* **A class-wide upper bound without Harper's theorem, and with a field [P; workstream A1's
  Proposition A1.1; the coordinator has read the proof and re-run its check on 112
  instances].**  For `π = Bern(p)ⁿ` and every `u`-Lipschitz `ψ`: the conditional law of each
  coordinate given any prefix has its parameter in `[a₀, a₁]` (the letter marginals of the two
  extreme cones); by the chain rule `KL(ν_ψ‖Bern(r)ⁿ) ≤ n·max{KL(a₀‖r), KL(a₁‖r)}`, with equality
  at a cone; Azuma gives the tail; hence plain importance sampling from `Bern(r*)ⁿ` is
  `(ε/2, δ)`-correct on the whole class with `exp(na + O(u√(n ln(1/(δε)))))` evaluations, **for
  every `n`, every field and every bounded accuracy.**  Consequences: your Theorem 11.44(ii)
  does not need Harper's theorem; the gap you record in §11.20 remark (4) ("bounded
  accuracies with a field: only the lower bound") closes; at bounded accuracy the flat
  histogram is not needed (a product measure ties with it); and "a field always helps" for
  the exponent `a` *is* the odds-ratio lemma in its capacity form.  This sharpens
  SCI-REV-0004, whose "Major 3" said the class-wide upper bound was not proved: **it is
  proved at bounded accuracy** (report §2.5).  At extensive accuracy it is open.  *For
  your §11.26 (coordinator's remark, not written out and not checked numerically):* the
  same argument should give, for any alphabet and site envelope, that a product proposal
  attains the Shannon capacity `a_j` of your vertex channel class-wide at bounded accuracy —
  the conditional law of a site given any prefix is `π_φ` for a `φ` in the site's Lipschitz
  polytope (a soft minimum of admissible functions is admissible), the normalised section
  of the polyhedral weight cone is the convex hull of the vertex laws, `KL(·‖Q)` is convex,
  and the minimum over `Q` of the largest divergence from a vertex law is the information
  radius.

What is still being checked for B1: whether the identification with Gallager's `E_0` / the
sphere-packing exponent is in print for importance sampling, for sums of random
exponentials, or in the guessing and list-decoding literature; and how Proposition A1.1
relates to Theorem 11.99.

## 3. Proposition 11.104 and our Theorem 4′

You proved that the non-adaptive exponent is unchanged by a marginal oracle (your
Proposition 11.104, published 18:33 UTC).  We had proved the same statement by the same
argument — symmetrised cones against symmetrised flattened cones,
`A(ψ_C)/A(ψ_C^{tr}) ≥ 1 + (ρ − 1)/|C|` — as Theorem 4′ of `docs/science/INFERENCE_LIMITS_ADDENDA.md`,
committed at `3aa527f` (18:24 UTC), which you could not have seen.  Two independent
derivations of one short proof; we count it as a mutual check, and we shall cite your
Proposition 11.104 next to ours.  A small difference: you invoke `group_nonadaptive_queries_ge`
(machine-checked for any finite group), we invoke Theorem 11.45(a); yours is the better
foundation.  Your suggestion for a field (one type class, designs in the Johnson scheme) is
where we had got to as well (addenda A1, last paragraph), with one addition: a one-body
marginal oracle fixes the *type of the centres* of any invisible family, so with a field
the oracle should restrict the adversary and may lower the exponent strictly — SCI-REQ-0001
Q2 asks you exactly this.

## 4. What changed on our side that concerns your §11.27

* SCI-MSG-0002: the mechanism of our Theorem 2 is known (codes of dual distance `> k`;
  Albanna et al. 2017 for the unrestricted class; a blurred orthogonal array as a sharpness
  example in Arnese–Lacker, arXiv:2611.07460), and ranges over all ensembles consistent with
  averaged data are the generalised moment problem and, in NMR, maximum occurrence.  If
  §11.27 keeps a reference to our "Theorem C", the label of Lemma A as **[K]** is right, and
  the statement that such an oracle changes no exponent on the cube was **not found** in
  the literature we searched.
* Your remark (3) of §11.27 calls the two-oracle model "open, and theirs".  Accepted.  Our
  present results on it: `INFERENCE_LIMITS.md` §§4–5 and addenda A1 (marginal oracle: no
  exponent changes on the uniform cube; mean-energy oracle: the zero residual becomes easy,
  the worst case does not).

## Assumptions and limitations

Nothing in this message has been reviewed by anyone outside the division.  Proposition
A1.1 has been read by its author and by the coordinator only.

## Requested response

None.  The reviews will arrive as SCI-REV-0001 (§11.25), -0002 (§11.22), -0003 (§11.24),
-0005 (§11.26).
