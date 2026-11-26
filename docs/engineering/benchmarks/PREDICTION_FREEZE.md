# Freezing predictions: what makes a prediction artifact evidence

Authority: directive D-7 of the research owner (2026-11-26; `docs/engineering/DIRECTIVES.md`):
"Preserve independently timestamped prediction artifacts and exact computational
provenance."  "Maintain strict distinctions between genuine blind assessment,
pre-leaderboard assessment, and retrospective evaluation."  "Respect frozen predictions,
contamination controls, and separation between development and held-out evidence."

This file is the procedure of the Computational Research Division.  The *design* of an
evaluation (which targets, which metrics, which baselines, what counts as blind) belongs to
the Frontier Benchmarking division; the software to the Structural Biology division; this
file only says what we do so that a prediction can later be shown to have existed,
unchanged, before its reference was available to the programme.

## 1. Three words, used strictly

| word | meaning here | what must be shown |
|---|---|---|
| **blind** | the prediction was frozen while the reference was not public and not available to any division or to any tool the software used | (i) the freeze record of §2 dated before the public release of the reference; (ii) evidence that the reference was not public then; (iii) a contamination statement for every data source and every pretrained component (§3) |
| **pre-leaderboard** | the prediction was frozen before the *official assessment* (rankings, scores) was published, but the reference itself may already have been public or obtainable | (i) as above against the assessment's release; (ii) an explicit statement of which references were already public at the freeze |
| **retrospective** | everything else | nothing beyond reproducibility; never reported as a prediction |

A prediction whose category cannot be established is retrospective.  "We did not look" is
not evidence; "it was not available" with a source and a date is.

## 2. The freeze record

For every batch of predictions, one directory `experiments/eng/frozen/<batch>/` with:

1. `MANIFEST.sha256` — one line per artifact: SHA-256, size, relative path.  Artifacts
   are the prediction files exactly as they will be scored, the input files exactly as
   used, and the configuration.  Large artifacts need not be committed; their hashes
   must be, and the artifacts themselves are kept where the manifest says.
2. `PROVENANCE.json` — for each artifact: the commit of every repository branch whose
   code ran (the software's branch at a pinned commit, ours), the command, the random
   seeds, the container image or environment (package versions), the compute platform's
   own identifier of the run, start and end times as the platform reports them, and the
   hashes of all inputs — including every database, alignment, template set and
   pretrained weight file the software read, with its version and date.
3. `FREEZE.md` — who froze what, the category claimed (§1), the references it is to be
   compared with, when and where those references are expected to become public, and
   the contamination statement (§3).

The record is committed and **pushed to the public repository at once**.  Three clocks
that are not ours then bear on it: the hosting service's record of the push, the compute
platform's record of the run, and — if the research owner approves a service — a
timestamp of the manifest's hash from outside the programme (proposed; not used so far,
because it means sending a hash to a service the owner has not named).  The commit's own
date is *not* evidence: it is written by the machine that makes the commit.

Nothing in a frozen batch is edited afterwards.  A corrected prediction is a new batch;
the old one stays, and a comparison reports both.

## 3. Contamination statement

For each prediction: (a) every data source the pipeline read, with the date of the
snapshot, and whether it can contain the target's experimental structure or a close
homologue released after the target was announced; (b) for every pretrained component,
its training cutoff as documented by its authors, and whether the target or its
reference can have been in the training data; (c) whether any person or agent in the
programme had seen the reference, a figure of it, or scores computed from it; (d) how the
targets were chosen, and whether any target was dropped after predictions were made (the
list of dropped targets is part of the record).  Unknowns are written as unknowns.

## 4. Development and held-out evidence

Parameters are tuned on development targets only.  The held-out set is fixed and hashed
(the list of target identifiers, in `FREEZE.md` of a batch with no predictions yet)
*before* the first run on it; the software's commit is pinned before that run; one run
per target and configuration is scored, and every further run is reported as such.  A
failure to produce a prediction is a result.

## 5. What we will not do

Run an implementation that has not passed our intake (reading, tests of our own, a small
exact check) because a deadline is near — "Do not execute immature implementations merely
to meet the November 29 deadline."  Score anything ourselves against a reference in a
way that could feed back into a later freeze.  Call a result blind on the strength of a
commit date.
