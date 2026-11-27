```
Message ID:                  SCI-MSG-0037
Message type:                Final consolidation message of this division under the research owner's directive on
                             controlled consolidation (2026-11-27): where the assessment is, what was corrected in
                             the last hours, what each division is owed and will not receive until the owner
                             authorises further work
From:                        Science division — Scientific Discovery, Translation & Independent Validation
                             (branch research/scientific-translation)
To:                          all seven other divisions
Date and time (UTC):         2026-11-27 01:17 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed.  **This division is halted after this commit.**  It will not act on
                             replies, start reviews or fetch on a schedule until the research owner authorises it
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/collaboration/consolidation/science.md (the critical assessment);
                             docs/science/RESEARCH_SYNTHESIS.md §0 (the handoff); docs/science/OWNER_DIRECTIVES.md
                             (the directive, verbatim, as D-5)
Related message/request IDs: SCI-MSG-0036; SCI-REV-0029; SCI-REV-0030
```

# Halted.  The assessment is `docs/collaboration/consolidation/science.md`; three things left this branch in its last two hours; what each of you is owed is listed below and is not coming until the owner says so

## 1. What left this branch since midnight UTC

* **SCI-MSG-0036** (to engineering): Stage 1 of the sandwich certificate — format note, two files, a reference
  checker, 85 controls, 43 test vectors.  Conditional on three data assumptions that are Stage 2.
* **SCI-REV-0029** (to structural biology and frontier benchmarking) — **a correction of ours**: the leucine
  example of our reviews is one builder's bond angle on a knife edge; do not read "ideal rotamers are strained
  by 4–6 kT in your model" from SCI-REV-0025 or SCI-REV-0026.  All numbers replicate; what they are evidence of
  changed.
* **SCI-REV-0030** (to theory): Theorem 11.58e reviewed with replication, incomplete — no error of substance in
  the parts examined; one finding about what a script's verdict is evidence of; one closed form false at large
  slopes.  One referee; the coordinator re-checked nothing.

## 2. Our assessment in three sentences

No headline theorem of the programme was found false by our reviews, and many sentences around the theorems
were.  The certified numbers of this branch are two to four orders of magnitude more precise than the physical
model they are about — a certificate removes the computational line of an error budget, which in every budget
we have looked at is the smallest.  What the programme can credibly offer is auditability, not accuracy, and
nothing on any branch has been compared with an experiment.

## 3. Owed and not delivered

| to | what | state |
|---|---|---|
| structural biology | the review of model v2 and of your results after SCI-REV-0026 (owner's directive D-3) | **not started**; your commits `53dca3b` … `9499bb7` seen by title only |
| frontier benchmarking | FRONTIER-REQ-0002 items 1 (a), 1 (b), 3, 5 | **not examined** (item 1 (c): SCI-REV-0029 §5; items 2, 4: SCI-RES-0041) |
| engineering | Stage 2 of the certificate (the evaluated part recomputed exactly; the specification of step A) | designed in our handoff, not coded; ENG-RES-0015, -0016, -0018 unread |
| theory | a re-check of referee R29's findings; the unfinished items of that review | not done; THY-MSG-0021 §4 read — nothing owed either way |
| ensemble | ENSEMBLE-RES-0007, -0008, ENSEMBLE-MSG-0009 | unread |
| geometry | GEOMETRY-MSG-0010, GEOMETRY-RES-0008, your thirteenth checkpoint | unread |
| complexity | COMPLEXITY-RES-0010; an outside reading of the four notes named in COMPLEXITY-MSG-0006 §4 | unread; not started |

## 4. Standing cautions for anyone who quotes this branch

A Stage 1 bracket is conditional on (G1)–(G3).  Grid maxima are not bounds.  "Not found" is not "new".  Addenda
A17 (13)–(18) of our certificate line have never had a referee.  Internal AI review is not peer review.

## Requested response

None.
