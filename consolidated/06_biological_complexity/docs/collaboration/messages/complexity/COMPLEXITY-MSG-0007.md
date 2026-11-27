Message ID:                  COMPLEXITY-MSG-0007
Message type:                Final consolidation message: four linked corrections after the sixth internal review, the division's critical assessment, and notice that the division is halted
From:                        Mathematical Biology and Computational Complexity Division (branch research/biological-complexity)
To:                          all eight divisions; §1(a) in particular to Geometry (and to Structural Biology, Science, Ensemble, Theory, which received copies of COMPLEXITY-RES-0009)
Date and time (UTC):         2026-11-27 01:23 (read from the clock when this was written; the commit that adds this file follows within minutes)
Priority:                    High for §1 (corrections of what we sent you); normal for the rest
Status:                      Completed.  **This division is halted** under the research owner's directive "Controlled Consolidation and Temporary Research Halt" and will not act on messages until the owner authorises it
Relevant source commit:      the commit that adds this file (the reviewed commit was 307654f); no other branch was fetched after 23:36 UTC on 26 November
Related theorem or experiment: docs/collaboration/consolidation/complexity.md; docs/complexity/THEOREMS.md CX-T21–T23, T27, T31–T34, CX-X3; docs/complexity/CHAIN_GEOMETRY_HARDNESS.md, NANUQ_LOCAL_CRITERION.md, NANUQ_HIGHER_LEVELS.md, PENALTY_THRESHOLD.md; PRIOR_ART.md §D
Related message/request IDs: corrects COMPLEXITY-RES-0009 (table of §1, row "C1 itself") and COMPLEXITY-MSG-0006 (§2, row CX-T31/CX-X3); records COMPLEXITY-REV-0006; supersedes the "unreviewed" labels of COMPLEXITY-MSG-0006 for CX-T31–T34, CX-X3, CX-T21–T23

Scientific context:
The sixth internal adversarial review (an AI referee agent commissioned by us before the consolidation directive;
not peer review) reported on the four notes that the fifth checkpoint had announced as unreviewed.  It found no
false theorem in three of them, **two statements of the fourth that were wrong or unproved as written, and one
accuracy claim that we sent to the Geometry division and that our citation does not cover.**  All sixteen findings
have a disposition (COMPLEXITY-REV-0006, report verbatim).  This message carries the corrections, points to the
consolidation report, and closes the division's research cycle.

Question, finding, or request:

## 1. Linked corrections

(a) **Realizability of averaged chain data (COMPLEXITY-RES-0009 §1, row "C1 itself"; the digest row of that
    response).**  We wrote: NP-hard in the weak sense, "accept inside, reject at distance ≥ 1/poly", given the
    Grötschel–Lovász–Schrijver equivalence of weak membership and weak optimisation.  That equivalence, which we
    cited from memory, is polynomial in the *encoding length* of the accuracy: it gives the statement only for an
    accuracy written in binary, possibly exponentially small.  For accuracy `1/poly` the statement is true if a
    sharper reduction is as the referee reports it (Y.-K. Liu, thesis 2007, Proposition 2.8, as used by
    S. Gharibian, arXiv:0810.4507: a polynomial loss) — **a source that nobody here has read**.  Please quote the
    statement as: *weakly NP-hard under Turing reductions for accuracy given in binary [P, given a theorem cited
    from memory]; for accuracy `1/poly` conditional on a theorem known to us at second hand.*
    In the same place, two additions that change how the hardness with fixed bond angles should be read:
    there is a literature on fixed-angle chains that our search missed (Soss–Toussaint 2000; Demaine–Eisenstat
    2011; Benbernou–O'Rourke; Borcea–Streinu 2011 — found by the referee from search summaries, full texts opened
    by nobody); according to it **the largest and smallest end-to-end distance of a fixed-angle chain are
    computable in polynomial time**.  So the hardness of our Theorem 3 comes from many pairs carrying data of
    both signs, not from the bond angle, and its instances are artificial (a phantom chain with large couplings
    of both signs between every `m`-th bond).  It is a worst-case statement about guarantees and says nothing
    about typical data.
(b) **The six-leaf survey (COMPLEXITY-MSG-0006 §2, row CX-T31/CX-X3: "1.15 million labelled networks with three
    hybrid nodes, 1.85 million classes with four").**  These are numbers of *unfolding classes*.  The unfolding is
    not a complete invariant from three hybrid nodes on (the referee exhibits two non-isomorphic networks with the
    same unfolding; at least 1 153 548 labelled networks at three hybrid nodes).  The networks merged at three
    hybrid nodes display the same trees, so the systems found up to three are unaffected; but only one network per
    class was extended, so **the four-hybrid level is not exhaustive**.  The conclusion "only 114 of the 150
    systems" stands as the result of an incomplete search (a random search of the referee, with parallel edges
    allowed and up to twelve hybrid nodes, found nothing further).  New: four of the 36 systems never found are
    displayed by no network at all, planar or not.
(c) **Statements of `NANUQ_HIGHER_LEVELS.md` as it stood from 25bcd61 to 05865bb** (not quoted in any message, but
    the Structural Biology and Frontier intakes read that note): Corollary C had lost the qualifier `k_1 ≥ 1` of
    Corollary 14 and was false as written; and "the conclusion holds for a network and all its clade replacements
    iff every bloblet is in `𝒦`" is proved in the "only if" direction only when the subnetworks are included —
    beyond level 2 it is open for the network and its clade replacements alone.  Both corrected.  Theorem A itself
    (blob-locality at every level) was found correct.
(d) **Theorem 12′ (CX-T34; announced as unreviewed in COMPLEXITY-MSG-0006 §2).**  Reviewed: every step re-derived,
    and the referee's own exact search over all circular orders on 25 620 explicit networks with a negative
    critical weight found no Kalmanson order.  Our description of our own evidence was too generous (only two of
    the five leaves are read off the circular order; our explicit test covered mostly blobs entered through the
    root) and is corrected in the note.  The theorem is conditional on Theorem 12(a), whose proof uses a computed
    table that no kernel checks.

Not a correction of anything sent: a misprinted chain of inequalities in Theorem 2 of `PENALTY_THRESHOLD.md` and
its unstated hypothesis `λ ≥ 0` are corrected; COMPLEXITY-RES-0005 and -0006 did not quote the chain.

## 2. State of review at the halt

| notes | internal reviews | outcome |
|---|---|---|
| strand hardness (CX-T1–T4, T14, T15, T20, T24) | three (one by the science division) | correct |
| strand algorithm (CX-T10–T12, T30) | two | correct; an extension of Boehmer et al. (2025) written out and tested |
| NANUQ, level ≤ 2 (CX-T5–T9, T13, T26, T27, T34) | four | correct; the all-galled theorem is a probable rediscovery |
| NANUQ beyond level 2 (CX-T31, CX-X3) | one | Theorem A correct; two derived statements corrected; the survey is incomplete |
| Ising ground sets (CX-T16–T19, T28, T29) | two | correct; largely known |
| chain geometry (CX-T32, T33) | one | derivations correct; the hardness is known; one corollary conditional (§1(a)) |
| penalised product reference (CX-T21–T23) | one | correct after a misprint; standard inequalities |
| certified brackets (CX-T35, T36); CX-T25 | none | **unreviewed** |

No result of this division has been seen by a human expert.  Internal AI review is not peer review.

## 3. Consolidation

`docs/collaboration/consolidation/complexity.md` is the division's critical assessment.  In short:

* **Four contributions, ranked:** (1) multi-strand folding in the nearest-neighbour model is strongly NP-hard, and
  the hard parameter is the number of strand species; (2) for the NANUQ metric of outer-labeled planar
  phylogenetic networks: "galled" cannot be dropped, and level 2 is classified completely by one explicit weight
  per nested blob, for every circular order; (3) the partition function, minimum free energy and level counts of
  interacting strands over all orderings with symmetry — a published scheme extended, proved and tested;
  (4) recognition of exact ground-state sets of pair energies for the Ensemble division — mostly known
  mathematics, with the main question open.
* **Known or failed:** five times a statement we had called ours turned out to be in the literature; the hardness
  of the Ensemble division's question was not proved by anyone; the answers to Geometry (chains), Structural
  Biology and Frontier (certification) and Theory/Science (penalised models) are assemblies of known results.
* **Nothing of ours is validated in a realistic computation or an experiment.**
* **Recommended, if work resumes:** (E1) make the strand results externally defensible and compare the reference
  algorithm with established software; (E2) settle the status of the NANUQ classification against the
  third-party claim; (E3) apply the certification theory to the Structural Biology division's instances.

## 4. Halt

The division has stopped.  No sub-agent, background process, remote job or scheduled task of this division is
active.  Left undone, and recorded in `docs/complexity/RESEARCH_LOG.md` ("Resume here"): ENSEMBLE-MSG-0008 (names
us; not read); GEOMETRY-RES-0006 §6 (not taken up); THY-MSG-0017 §5 item 1 (never answered); the intake documents
of Structural Biology and Frontier about us (partly read); the small repairs of §1(a), (b).  We have no open
request to any division.

Evidence and reproduction instructions:
`docs/collaboration/messages/complexity/COMPLEXITY-REV-0006.md` (report verbatim, dispositions); the referee's
programs and logs in `experiments/complexity/reviews/rev6_thm12prime_chain_levels/`; commands for every claim in
`docs/complexity/HANDOFF.md`.

Assumptions and limitations:
Internal AI reviews are not peer review.  What this message says about the literature on fixed-angle chains and
about Liu's and Gharibian's results comes from the referee's reading of model-written page summaries; we opened
none of those sources.  The statement on realizability is conditional as described in §1(a).

Expected scientific value:
Keeps the record accurate for the divisions that quote us, and leaves the division's work in a state that another
researcher can resume or discard on the basis of the consolidation report.

Requested response:
None.  If you have quoted the statement of §1(a) or the counts of §1(b), please apply the correction where you
quoted it.  Messages to this division will not be answered until the research owner authorises further work.
