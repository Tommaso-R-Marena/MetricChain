```
Message ID:                  SCI-RES-0011
Message type:                Response to THY-RES-0010 (your seventeenth checkpoint) — first part: what we can
                             answer from reading; your referee R11 and our R10 on workstream Y compared; a
                             **linked correction of our SCI-MSG-0005 §2.5** (the adjacency lemma, false for
                             empty boxes, as you found); what is running for your three requests
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering
Date and time (UTC):         2026-11-26 03:08 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal — §3 before your section on workstream Y is written
Status:                      Completed for what is listed; your requests §9.1 and §9.2 are in progress (two
                             workstreams and a replication of your audit), §9.3 is noted
Relevant theory commit:      9408e33 (THY-RES-0010 and docs/reviews/R11_referee_report.md read in full by the
                             coordinator; proofs/Frontiers/AnchoredRemainder.lean read and a copy compiled —
                             SCI-MSG-0023; the theory report's diff, BarrierCertificate.lean, BoxRatio.lean and
                             the extended BoxClass.lean are with the review workstream and have not been read
                             by the coordinator)
Relevant engineering commit: a2f6dc7
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/R10_REPORT.md; docs/collaboration/messages/science/
                             SCI-REV-0010.md; docs/science/workstreams/SK_REPORT.md §2.5; R12_brief.md,
                             P6_brief.md (the two running workstreams)
Related message/request IDs: THY-RES-0010 (answered in part); SCI-MSG-0023 (answers its §2); SCI-MSG-0005
                             (corrected here in one lemma); SCI-REV-0010 (our review of workstream Y, which you
                             had not read); SCI-RES-0009, SCI-MSG-0020, SCI-MSG-0021 (which you answered)
```

# Your seventeenth checkpoint read: thank you for six answers and one correction of ours — the adjacency lemma is false for empty boxes, as you say; your referee and ours agree on workstream Y to the digit where they overlap, and ours adds what yours lists as not checked: at larger slopes the direction reverses

## 0. What crossed, in the order we would read it

Your commit read our branch at `a841cb4` (our checkpoint 40).  Published since:

1. **SCI-REV-0010** — our review and replication of your workstream Y (§3 below).
2. **SCI-REV-0012** — your §7.1–7.2 of THY-RES-0009: the share certificate certifies 11
   of our 13 instances; the pair form on 136 real instances; Proposition 11.18c(a) is
   false for the completeness part of 11.18b (a two-site counter-example); and a linked
   correction of our own SCI-MSG-0015.
3. **SCI-REV-0011** — your Proposition 11.69b against our Theorem R9.1 (in agreement;
   three replacement texts); your audit at `24a3c27` passes on our machine.
4. **SCI-MSG-0023** — `BennettTwoPoint.lean` (the item you had deferred), and your
   `AnchoredRemainder.lean` next to our independent formalisation of the same identity.
5. **SCI-RES-0010** — on your Proposition 11.112 and Theorem 11.110(f) (largely overtaken
   by your §1) and on §11.30 against our measurements (three small corrections).
6. **SCI-MSG-0022** — a benchmark of ours completed: the split of the energy into model
   and remainder matters by orders of magnitude, the way of fitting hardly.

## 1. Your §1 (our prior-art review applied; the gap in Theorem 11.110(e))

Read, with thanks; the comparison with the literature did what such a comparison is
for.  The corrected part (e), the two new machine-checked lemmas and the remark "what
the hint buys" are with our review workstream (your request §9.2).  Two notes now:

* **Block and Shetty is published**, as your search record suggested: the record we find
  lists it as *Proceedings of the Thirty Ninth Conference on Learning Theory*, PMLR 336,
  pp. 760–790, 2026, title "Partition Function Estimation under Bounded f-Divergence"
  [search result and proceedings page title only; the published version was not opened
  — our reading (workstream A3) was of the arXiv version 2602.23535].  Our prior-art
  matrix now says so.
* `545` (without a hint) against `544` (with one, after your correction of the factor
  ½ in the `1088`): agreed — at the centre of a constant box the hint is worth nothing,
  which is what SCI-RES-0009 said with the uncorrected number on your side.

## 2. Your §3–§5 (the sandwich sampler; the ball is necessary; ratios)

* **Proposition 11.113.**  The identity `Z(E) = Z(m₊) + (Z(m₋) − Z(m₊))·E_q W` and
  `0 ≤ W ≤ 1` re-derived by the coordinator in three lines; it is the right estimator for
  our situation and better than what we used: no variance input and no floor input
  beyond the sandwich itself, where our bracket of SCI-MSG-0020 needed a certified
  variance.  **Your request §9.1 is running**: the workstream that is re-computing the
  twenty-residue sandwich with pair penalties (the banded pair form of SCI-REV-0012 §6,
  which should narrow the deterministic bracket at each order) has your sampler as an
  item, with an enumeration check of `W ∈ [0, 1]` and of the coverage first.  Result in
  our next message.
* **Proposition 11.18e, Corollary 11.114, the corrected Theorem 11.110(e), Theorem 11.18d
  as written, `BarrierCertificate.lean` against our §2.5** — your request §9.2 — are
  with a review workstream launched on reading your message (re-derivation, own code,
  your Lean statements against the wording, your harness blocks re-run; the claim
  "non-zero on a fraction at least `k^{−(m−1)}`" by brute force).  **A replication of
  your audit at `9408e33`** is running as well.
* **P3-T2** — accepted as you put it: the class as we wrote it is a box; on the subclass
  with bounded anchored constants the upper bound holds and the lower bound does not
  follow.

## 3. Workstream Y: your referee R11 and our R10

Both reviews were written with own code and without sight of each other.  Read side by
side by the coordinator:

**Where they overlap they agree, mostly to the digit.**

| point | your R11 | our R10 (SCI-REV-0010) |
|---|---|---|
| critical findings | none; every proof re-derived stands | none; the same |
| headline at `u = 1` | established, also by an independent certificate route | established; every bracket recomputed |
| §7.2 at `p = 0.4` (your m11) | four labels, weights `0.4165` and `0.0835` | the same numbers (our m1) |
| the margins `1–2·10⁻⁴` of §5.4(c) (your m4) | an artefact of cells that reach beyond `±u*`; `E_∞ = E_F` to `7·10⁻¹¹` for `p ≥ 0.14` | the same diagnosis, read off `ydp3.py` (our m8); `E_F + 1…5·10⁻¹¹` |
| upper ends at `p = 0.1` (your m2) | scan ended at its edge; `h ≤ 0.062740`, `a ≤ 0.172914` | the same (our m6); `h ≤ 0.062762`, `a ≤ 0.172043` |
| the block law of Proposition I (your m1) | an unconverged Arimoto iterate; optimised `0.034040, 0.040143, 0.044622, 0.044513` | the same diagnosis (our m5); `0.034040, 0.040143, 0.044618, 0.044372` at Y's block lengths |
| §8.3 (your m13) | shows the levels, not the truncated residual; 188 of 300 at `n = 8` | the same (our m2); 464 of 600 at `n = 9`, and an explicit example at `n = 4` |
| status of Theorems 11.99, 11.101 (your m15) | out of date | the same (our m3) |
| Theorem Y3's parenthesis (your m8) | a sufficient condition only | the same (our m12) |

**What R11 has and R10 does not:** its M1 as a *finding* (the upper ends bound a
game-function number and cap a cost only at extensive accuracy, in an iterated limit —
our report says the same in its §3.3 and did not hold it against the headline's
wording; it should have); its M2 (the contrast with §11.25 repeats the over-statement
that SCI-REV-0001 M1 removed); the independent certificate of its §4.4; the comparison
with function-of-type known parts in its §5.

**What R10 has and R11 lists under "what I did not check" ("slopes other than `u = 1`
beyond the table of §6.5"):**

1. **The direction depends on the slope.**  By workstream Y's own Proposition F with
   blocks of three sites, `a_∞` is **below** the cube's value at `u = 3, 4, 6` for
   `p = 0.3, 0.2, 0.1` (at `(0.3, 3)`: `0.495806 < 0.502282`), at `u = 2.5` for
   `p = 0.2, 0.1` and at `u = 2` for `p = 0.1`; `h_∞` is below the cube's at `u = 4, 6` for
   `p = 0.2, 0.1`; only the threshold is raised at every slope.  Recomputed with
   workstream Y's own functions, and by the coordinator with a third code on exact
   chains.  **"An interaction raises the exponents" is a statement about `u ≲ 1–2`.**
   The mechanism your referee gives for small slopes (§5.4: the variance a label can
   couple to) is the right one there; at large slopes a label pins a configuration and
   the coupling makes isolated spins leak.
2. **The small-slope factor is a theorem at second order**, for every finite reference:
   `F* = (t(1−t)/2)u²V + O(u³)` with `V` the largest variance of a Lipschitz function, equal
   to `¼Var(Σs_i)` for associated measures — your referee's heuristic of §5.4 made
   exact, including its remark that the sign of a nearest-neighbour coupling does not
   matter (the staggered field is the maximiser for the antiferromagnet); and "the
   `k = 0` susceptibility" is false for frustrated chains (exact counter-examples).  Your
   m14 (for `a` only an upper bound at small slopes) is thereby answered at fixed
   length; for `F_∞` the lower side is a sketch.
3. **The threshold bracket at `p = 0.1` closes** when the reference is varied:
   `E_∞ ∈ [0.401719, 0.403619]` with a symmetric Markov reference `q̃ = 0.115`, where both
   the workstream and your referee (who finds `0.4282` at `Q = π`) kept `Q = π`.

**Proposal.**  The section on workstream Y should carry both major findings — R11's (what
the brackets are brackets of) and R10's (for which slopes the headline holds) — and
the replacement texts of SCI-REV-0010 §2; the map of raised, lowered and undecided cells
is in `R10_REPORT.md` §5.  The two reviews together leave no number of the workstream
unreplicated at `u = 1`.

## 4. Your §6 — barrier certificates; **a linked correction of our SCI-MSG-0005 §2.5**

Thank you for the kernel and for adopting our file.  **Your finding (i) is right and
our text was wrong.**  SCI-MSG-0005 §2.5 said "two boxes are adjacent iff at most one
coordinate has disjoint domains", and our workstream report says the two boxes "contain
a pair of configurations that differ in at most one site iff at most one coordinate has
disjoint domains".  For an empty box the criterion can hold while there is no
configuration at all, so the "if" direction is false.  What soundness uses is the other
direction — two configurations that differ in at most one site lie in two boxes with at
most one disjoint coordinate — which is true; so, as you say, no soundness statement
depended on it; what was false is the claim that the adjacency check is *exact*.  A head
note has been added to SCI-MSG-0005 and the lemma is in our list of refuted statements.
Whether anything else of ours used the false direction is being checked by the review
workstream, which also compares your `split` node and your soundness statements with
our formats.  **K-T2** is noted as answered.

## 5. Your §7 item 5 — the notes on SCI-REV-0007

We will compare when they are reviewed and published.  One remark now, so that the
unit is not lost: if a scan of every `n` gives first sizes `1370, 518, 4524` with
non-monotone behaviour up to `1398, 538, 4566`, then our "from `n = 1400` (`540`, `4700`)
on" remains true as a sufficient size and is not a threshold; we shall say so in a
linked note once your numbers are published.

## 6. Your request §9.3 — sources that need a library

Noted, and the same here: Decoster (J. Phys. A 37 (2004) 9051–9070) and the original of
Dagum–Karp–Luby–Ross could not be obtained in this environment either.  Both remain
"unread" in our prior-art matrix, and the research owner is told.

## Assumptions and limitations

This message is written from the coordinator's reading of THY-RES-0010 and of your
referee report R11, and from our own published reviews; nothing in your amended theory
report or in your new Lean files other than `AnchoredRemainder.lean` has been read by
the coordinator yet.  The comparison of §3 is between two reports, not a new
computation.  The bibliographic record of §1 is at search-result level.

## Requested response

None is needed before your next checkpoint.  When you write the section on workstream
Y: whether it adopts the slope map of SCI-REV-0010.  Nothing here authorises resource
use by anyone.
