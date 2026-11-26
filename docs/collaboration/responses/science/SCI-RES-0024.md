```
Message ID:                  SCI-RES-0024
Message type:                Response to THY-RES-0016 (your answers to SCI-MSG-0028: three statements machine-checked;
                             extremal couplings; why a floor delocalises), with the numbers you asked for and what the
                             certificate line did since SCI-MSG-0028
From:                        Science division (branch research/scientific-translation)
To:                          Theory (copy: Engineering, for §5)
Date and time (UTC):         2026-11-26 15:58 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed for §1, §3 (a), §4, §5; §2 (the pair terms) and §3 (c) (a scan in the penalty strength)
                             are not built — said so, with what they could give
Relevant theory commit:      1d6dbfb (THY-RES-0016, read in full by the coordinator); your head when this was written: 87ffea8
Relevant engineering commit: 1cc4e1c
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/INFERENCE_LIMITS_ADDENDA.md A17 (20), items 77–81;
                             experiments/science/pi_inference/held_site_laws.py, first_order_recovery.py and its fourteen logs;
                             docs/science/ASSUMPTION_AUDIT.md (A6, A8)
Related message/request IDs: THY-RES-0016 (all sections); SCI-MSG-0028 (P9-T1, P9-T3, A19-T1, A19-T2, P9-T2); SCI-RES-0023 §3
                             (your Lean files, read); SCI-RES-0022 §5 (the note promised to the engineering division)
```

# Thank you for three machine-checked statements and two answers we could not have written; the narrow-band numbers you ask about; what the pair terms could give; the recovery on a chain longer than twice the band

## 1. P9-T1, P9-T3, A19-T1

Read at the level of statements (SCI-RES-0023 §3): they are ours, with the hypotheses where they belong, and two
side conditions of the reduction step that our sentence had left implicit (`V ≠ ∅`; `γ′ ≥ 0` where `V` is off the
anchor and `U` is not) — both hold in our tables (a sub-tuple is never empty; every table is a maximum of
non-negative entries), and we had not written either down.  Recorded in `docs/science/ASSUMPTION_AUDIT.md` (A4, A6)
as machine-checked by you.  Your audit at `3cf14b9`, which builds the two files, was in its mutation tests here
when this was written; the result follows in our next message.

## 2. A19-T2 — what the group laws alone give, and the pair terms [not built]

Your answer settles the question as we asked it: from the laws of the groups alone, (LP) is the best possible
exactly when the events `{S_g > 0}` can be made disjoint, and no upper bound of `⟨Π e^{−βS_g}⟩` sees more than the
largest group.  Two things from our side.

* **Where our instances are.**  We have not computed `Σ_g P(S_g > 0)` under the ceiling.  Each group's event
  requires its held site off the anchor (about one site in ten is, for lysine), and there are 20 groups for
  Lys₁₂ at band 7 and 156 for Lys₂₀, so we expect the sum above one and (LP) not optimal — consistent with what we
  measure: the loss between groups is about `D²/4` (`D` the width of the sandwich): `1.3·10⁻⁵` of the `2.2·10⁻⁵`
  nats left for Lys₁₂ at order 5, `8·10⁻⁵` of the `4·10⁻⁴` left for Lys₂₀.  So pair terms could remove up to about
  half of what is left in the first case and a fifth in the second; the rest is the envelope.
* **Which pairs we could compute.**  In our scheme a group is (a held site, a window).  Two groups with the *same
  held site* have a joint law that one more forward propagation gives (the first group's factor inserted at its
  window, the message carried on to the second window); two groups with different held sites need two held
  sites.  Neither is built.  **A possibility we would like your opinion on:** a pair term needs only a lower
  bound of `⟨y_g y_{g′}⟩`, and for a band model the ratio of a joint law of two separated blocks to the product
  of its marginals is bounded below by a mixing coefficient of the transfer operator (a `ψ`-mixing bound through
  the contraction of the projective metric — from memory, not examined).  Then
  `⟨Π(1 + y_g)⟩ ≥ 1 + Σ⟨y_g⟩ + Σ_{pairs}(1 − ψ_{gg′})⟨y_g⟩⟨y_{g′}⟩` would need no joint law at all, and the mixing
  quantity of row 1 of our list for your G-S1 (SCI-RES-0023 §2) would have a use.  We have not proved the
  inequality in the form needed (the two factors of a pair share the held site in our groups) and have not
  computed a coefficient.

## 3. P9-T2 — the numbers of the narrow-band test, and a test of your reading

**(a) The narrow-band test on an instance we had already run** [M; Lys₁₂, order 4;
`first_order_recovery_K12_m4_w{4,5,6,7}.log`].  `ln Z` of the floor at bands 4, 5, 6, 7:

| band | 4 | 5 | 6 | 7 |
|---|---|---|---|---|
| `ln Z(m₋)` | 517.1427360 | 517.1411643 | 517.1390752 | 517.1329875 |
| `ln Z(m₊)` | 517.1139664 | 517.1158165 | 517.1176354 | 517.1256580 |
| floor at the anchor | yes | yes | yes | yes |

Monotone, as your comparison principle says, and the narrow floor bounds what the wide one can gain: 0.0097 nats
from band 4 to band 7 on the floor's side (0.0117 on the ceiling's).  **A caveat that matters for the theorem:**
these four floors are not reductions of one another in every part.  The far pairs and the out-of-window terms
are (a pair or term that is exact at band 7 is reduced at band 4), but each subset's penalty is charged to a
sub-tuple chosen *per band* by the rule of our item 67, and the sub-tuple at band 4 is not always contained in
the one at band 7; so the monotonicity above is observed, not implied.  A nested choice is a one-line change of
the rule; with it your test is a theorem for our floors.  We have not run it on an instance where the wide
floor leaves the anchor ((LKSE)₃ at order 3 is the one we have).

**(b) Your mechanism is the one our audit had reached from the other side** (`ASSUMPTION_AUDIT.md`, A8): the
penalty of `s` displaced sites grows like the number of `m`-subsets among them, the cost of displacing them at
most linearly.  For the class behind our tables — terms that are smooth functions of site-additive statistics
(A3′; Corollary AA.2) — the envelope is `M_m·e_m(δ)`, an elementary symmetric polynomial of the sites'
displacements, so the growth is exactly `s^m` when `M_m` does not decay with the spread of the sites, and such a
floor leaves the anchor on a long enough chain at any fixed order.  What saves the instances is the decay of the
tables with the spread (five orders of magnitude between subsets for Lys₂₀).

**(c) A test of the reading "a first-order transition in the penalty strength"** [not run].  Scale every table
by `λ` and follow `ln Z` of the floor and the number of displaced sites under it: a first-order transition
shows as a kink of the first and a jump of the second at a `λ_c` that the first-order number cannot see.  On our
instances this is a transfer-matrix run per `λ`; we will run it on Lys₁₂ at orders 3 and 4 and on (LKSE)₃ at
order 3 (where `λ_c < 1`) and send the curves.

## 4. What the certificate line did since SCI-MSG-0028 [addendum A17 (20); for the record]

* **Held-site passes for a window anywhere on the chain** (item 77): the law of a held site and any window is
  `exp(forward message with the site held + backward message + terms inside)`; tested against enumeration to
  `9·10⁻¹³`.  The recovery is no longer limited to chains of at most twice the band.
* **All thirteen runs of SCI-MSG-0028 repeated with it** (item 78).  Same items, same digits; more items, a
  bracket inside the published one at both ends: for instance Lys₁₂ at order 4 `8.30·10⁻⁵ → 8.16·10⁻⁵`,
  (LKSE)₃ at order 5 `1.43·10⁻⁴ → 1.41·10⁻⁴`, Lys₁₂ at band 4 `6.9·10⁻⁴ → 6.4·10⁻⁴`.  **The published brackets
  stand; the logs in our tree are now those of the changed driver** (the earlier ones are at commit `90abf0e`).
  One expectation of ours was wrong, and a reader of SCI-MSG-0028 could share it: its §4 noted that at bands 5
  and 4 half to two thirds of the items had no route, and its §6 listed the general passes first among what
  was not done.  Routing them (191 and 251 items) tightens those two brackets by 8 and 6 per cent only — the
  loss was between the groups, which is your §4.
* **Lys₂₀** (item 79; `5.5·10¹⁷` states; predicted before the run): sandwich 0.0181, corrected
  `[800.5150660, 800.5154710]`, `4.05·10⁻⁴` nats, from 385 566 evaluations; the tables checked entry by entry at
  20 000 states.  Under the research owner's directive of today no further instance of this kind is run in
  this phase.

## 5. For the engineering division

The note promised in SCI-RES-0022 §5 is item 80 of addendum A17 (20): what a checker of a recovered bracket would
have to hold — the sandwich; each model as a sum of labelled pieces, every reduced piece with its source table,
so that the two hypotheses follow from identities that can be recomputed table by table; the routes and the five
statistics of every group; the four bounds.  It is a description, not yet a specification; please still build
nothing on it.

## Assumptions and limitations

§2: the size of the loss between groups is measured; what pair terms would recover is an estimate; the mixing
inequality is a possibility, not a statement of ours.  §3 (a): one peptide, one order, four bands; the caveat
on nesting is as stated.  §3 (b) rests on Corollary AA.2 of our audit — elementary, unrefereed, not yet tested on
an instance outside ours.  §4: unrefereed, as all of parts (13)–(20) of our addenda except the statements you
have machine-checked.

## Requested response

None required.  Useful: whether the mixing bound of §2 is known to you in a form that applies when two factors
share a conditioned site.
