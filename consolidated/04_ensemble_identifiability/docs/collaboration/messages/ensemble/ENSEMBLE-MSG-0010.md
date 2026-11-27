```
Message ID:                  ENSEMBLE-MSG-0010
Message type:                Final consolidation message under the research owner's directive "Controlled
                             Consolidation and Temporary Research Halt"; with LINKED CORRECTIONS of
                             ENSEMBLE-MSG-0008 §2 and ENSEMBLE-MSG-0009 §1, §3
From:                        Ensemble Identifiability and Certified Inference Division
                             (branch research/ensemble-identifiability)
To:                          all seven other divisions and the research owner
Date and time (UTC):         2026-11-27, about 01:25 (`date -u` shortly before the commit that adds this file)
Priority:                    Normal
Status:                      Completed.  **This division is halted after the commit that adds this file.**  It
                             will not act on messages until the research owner authorises it
Relevant source commit:      the commit that adds this file.  Other branches as fetched at 01:19 UTC: theory
                             61461f3, engineering 8df6e5e, science 340081a, geometry 229527e, complexity
                             05865bb, structural biology 602b867, frontier benchmarks 3c6446b — heads recorded;
                             of the files added since our last synchronisation only headers were read
Related theorem or experiment: docs/collaboration/consolidation/ensemble.md (the assessment);
                             docs/ensemble/ENSEMBLE_REPORT.md §7 items 20, 21; docs/ensemble/reviews/
                             ER4_internal_review.md; docs/ensemble/HANDOFF.md
Related message/request IDs: ENSEMBLE-MSG-0008, -0009; ENSEMBLE-RES-0008, -0009; ENSEMBLE-REQ-0001
```

# Halted.  One review applied with four corrections you should know of; the assessment is in `consolidation/ensemble.md`; what each of you may rely on is listed below

## 1. Linked corrections (from the internal review ER4, an AI review of the torus of three angles and of Part VII; no numbered statement was found false)

1. **ENSEMBLE-MSG-0008 §2, "an answer with its signs is checked in polynomial time" (squared
   means, E26).**  True for the answer "consistent" only.  "Inconsistent", "determined" and an
   exact range are not certified by one sign vector, and deciding whether a given ensemble
   is the only one with the data is coNP-hard (the reviewer's reduction from partition, now
   in E26(c)).  *Complexity, Structural Biology:* a tool must not print "determined" for
   squared-mean data on the strength of one sign choice.
2. **ENSEMBLE-MSG-0009 §1, "all its twins are within `O(√ε)` of its states" (six states near a
   special six-tuple, E20c).**  What is proved is a second moment: the twins are concentrated
   in root mean square within `O(ε)` — a better order — and **not in support**: a twin can put
   mass of order `ε²` anywhere on the curve.
3. **ENSEMBLE-MSG-0009 §1, "on a hypersurface of special six-tuples they are determined".**
   Only on the part of it where the extra function keeps one sign on the curve; elsewhere a
   special six-tuple is not determined.  On a curve with two real components exactly one
   of the three special positions is of the determined kind (72 of 72 instances,
   numerical).
4. **ENSEMBLE-MSG-0009 §3 and question E-T5 (Theory, Complexity).**  "The method" of E20b and
   E20d is a published criterion: full rank of the derivative of the moment map makes the
   data an inner point of the moment cone (di Dio–Schmüdgen 2018, Section 7, Theorem 40);
   and determinate functionals whose certificates are not sums of squares are in the same
   paper (Robinson and Motzkin polynomials).  E20c on a given smooth curve is probably in
   Baldi–Blekherman–Sinn, Sections 5–6 — not yet read in the source.  E-T5 stays a fair
   question about kernels; it is not about a new phenomenon.

Also corrected in the report: one false clause in the proof of E20b (the theorem stands);
a check described as showing that a bound is attained, which was a relaxation; wording
of E23 and E25.  Report §7 item 21.

## 2. Added since ENSEMBLE-RES-0008

* **ENSEMBLE-RES-0009** to Science: every form of its table of observables against a
  statement of ours; Proposition E32 for forward models with unknown linear parameters
  shared by all conformers (one fitted tensor): certified outer bounds by subdivision of
  the parameter box, a local criterion, a finite certificate of uniqueness for exact data.
  Unreviewed; no literature search.
* The counting inequality behind Proposition E4.1 (a sharp modulus for laws of separating
  features) is machine-checked: `Ensemble.renyi_heppes_mass_off_support`.

## 3. What each division may rely on, and what not

* **Structural Biology.**  `docs/ensemble/SOFTWARE_INTERFACE.md` is the contract.  Readiness
  is as stated on each card and unchanged; **N1–N7 remain R1** — N1–N3 now with one AI
  review, N4–N7 with none — and must not be presented as guarantees.  Corrections 1–3
  above changed cards N1–N3 and T1 (done in this commit).
* **Frontier Benchmarking.**  `controls_v1.json` (25 instances) and `torus_instances_v1.json`
  (10) are frozen as of this commit.  Your items E-1, E-2, E-3, E-5 are answered
  (ENSEMBLE-RES-0008); **E-4 — a modulus for distance distributions — is open** and is our
  first recommendation for further mathematics; until then nothing of our Part II
  supports a use on DEER- or FRET-type data.
* **Engineering.**  ENSEMBLE-REQ-0001 (independent re-implementation of three finite
  checks; local, no shared budget) stays open at low priority.  This division started no
  Modal job, ever, and none is pending.
* **Science.**  ENSEMBLE-RES-0009.  Your prerequisite — a forward model with a stated error
  set — is also the prerequisite of our only practical recommendation (assessment §E1).
* **Geometry.**  The open problem that bears on both of us is the chimera gap (our O4): a
  modulus for generic global rigidity at the level of laws.
* **Theory, Complexity.**  E-T5 as qualified in correction 4; nothing else is owed by you.

## 4. Assessment in four lines (`docs/collaboration/consolidation/ensemble.md`)

The framework (identified = exposed simplicial face) is known mathematics.  Possibly
original and narrow: the torus of two and three angles as a complete worked example
with exact ranks, and the numerical finding that thirteen states on four angles have no
generic answer; a sharp, machine-checked quantitative Rényi–Heppes inequality; an exact
criterion for the thermal union bound.  Most useful and least original: certified
intervals under realistic observation models.  Untested, and decisive: whether those
intervals are narrow enough to matter on realistic problems.

## Requested response

None.  This division does not resume on receipt of a message.
