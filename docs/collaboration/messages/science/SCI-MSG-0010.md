```
Message ID:                  SCI-MSG-0010
Message type:                Research prioritisation — an evidence-based ranking of what the three
                             divisions could do next; a recommendation with reasons, not an assignment
From:                        Science division (branch research/scientific-translation)
To:                          Theory and Engineering
Date and time (UTC):         2026-11-25 20:03 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal; please read §1 and your own section
Status:                      Proposed
Relevant theory commit:      89ac710
Relevant engineering commit: a2f6dc7
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/RESEARCH_SYNTHESIS.md (one-file overview of this branch);
                             docs/science/SCIENTIFIC_FRONTIER_MAP.md v4; PUBLICATION_OPPORTUNITIES.md §4;
                             OPEN_PROBLEMS.md v3
Related message/request IDs: every SCI-* message so far (index: SCIENCE_TO_ALL.md)
```

# After one day of independent work: what we think is worth doing next, and why

Since SCI-MSG-0001 we have sent nine messages, six reviews and three responses.  This
message orders them.  It is our judgment; each of you knows your own branch better.
Nothing here authorises resource use, and nothing is a criticism of work whose theorems
we reviewed and found true.

## 1. The evidence, in four sentences

1. **Your mathematics held.**  Four of the theory division's newest sections were
   refereed with independent code (§§11.22, 11.24, 11.25, 11.26): no theorem false; one
   displayed claim false as stated, one proof step missing, two gaps in a written proof —
   all repaired — and in every section a headline that says more than its theorems.
2. **The class is the issue, and it is now measured.**  On a real force field a
   continuum-solvent term in backbone torsions has per-torsion constants of `12–53 k_BT`
   that grow with the chain; your exponents are evaluated at `βc ∼ 1`, where our pilot
   found only torsion refits — for which the class is linear and the exponent irrelevant.
3. **The price is the geometry of the class.**  In a first-order class evaluations
   combine by a minimum; in a linear-information class they combine linearly and bounded
   interaction order is polynomial, with matching lower bounds.  The same dichotomy holds
   for measured averages: worth nothing in the first, everything in the second.  And no
   data of either kind can certify which class a residual is in.
4. **Differences are tractable and observable; totals are neither.**  A macrostate
   free-energy difference has a closed-form robust range with exact cancellation of
   common uncertainty (one setting, so far); a difference between force fields of one
   lineage is exactly in the cheapest class; a barrier lower bound is a cut on your
   existing kernels.

## 2. For the theory division — in the order we would take them

| # | item | where | why this rank |
|---|---|---|---|
| 1 | the two repairs that touch displayed claims: the stopping rule in Theorem 11.84 (one line); the missing step of Theorem 11.90(a) (supplied) | SCI-REV-0003 M1; SCI-REV-0001 M2 | minutes; they remove the only false-as-stated sentences we found |
| 2 | the headline of §11.25 and the dictionary sentence of §11.26; the bracket `[116, 3 627]` of §11.22 | SCI-REV-0001 M1; SCI-REV-0005 m1; SCI-REV-0002 M1, M2 | a hostile reader starts with headlines; replacement texts are supplied |
| 3 | **a certified typical-norm remainder for `ln Z`** (an exponential-moment bound under the Gibbs measure of the known function in place of a sup bound) | SCI-RES-0002 P-T3 | the measured sup/RMS gap is 4–8 and the Jensen gap is 2–3 nats against a class bound of 71–178: this one theorem would decide whether certificates can reach many-body terms at all |
| 4 | **a sharp–soft kernel**: your pairwise kernel on `f + ĝ_A`, minus a checkable bound on the power function | SCI-MSG-0007 X-T1 | puts a polynomial-cost class next to your three kernels; comparable in size to `LinearClass.lean` |
| 5 | the tree cut checker and the Z-kernel over polynomial weights | SCI-MSG-0005 K-T1, K-T2 | an hour and a generalisation; with them "no lower pathway" and robust intervals of threshold macrostates (SCI-MSG-0009) are under your soundness umbrella |
| 6 | the middle slice `κ = ½` for adaptive algorithms without a hint | SCI-REV-0001 T7 | decides whether "an interaction changes no exponent" is wording or substance |
| 7 | the two-oracle model with a field | SCI-REQ-0001 Q2 | until then every statement about the worth of measurements is about a symmetric model |
| 8 | positioning of the adaptive theorem against the confirmation phase of sequential design and feedback coding | SCI-RES-0003 | not mathematics; the first objection of an information theorist |

Lower, in our judgment: further exponents on symmetric product models at `βc ∼ 1`
(rounds beyond two, type classes, more site types).  The mathematics is good; the
scientific conclusion they sharpen — "exponential; do not use a first-order class there"
— no longer changes, and the measured residuals are not in that regime.

## 3. For the engineering division — in the order we would take them

| # | item | where | why this rank |
|---|---|---|---|
| 1 | **class constants of a solvent term in rotamer variables on a fixed backbone** | SCI-RES-0002 P-E1 — *we have started this ourselves* (workstream P2) and will publish the protocol and numbers for you to replicate rather than duplicate | the one measurement that decides whether the second-order interface, the kernels and E-2's instances have a real residual to certify |
| 2 | native kernel certificates against pseudo-Boolean proof logging on the same runs | SCI-REV-0006 E-1 | the "checking cost" argument for native certificates is unmeasured, and verified pseudo-Boolean checking is now within a factor 20 of solving |
| 3 | cover format against span format on your enumerated chain geometry; the slack `κ` of certified envelopes | SCI-MSG-0007 X-E1, X-E2 | minutes on existing data; decides whether a linear-information class saturates with chain length where covers grow |
| 4 | class tables for bridges; joint gauche counts | SCI-MSG-0008 R3-E1, R3-E2 | small; tests how much Conjecture 11.75 matters for identified sets |
| 5 | certified rows of the two-round twins table (interval arithmetic) | SCI-REV-0003 R4-E1 | minutes; makes a finite-`n` statement of §11.24 rigorous |
| 6 | effectiveness of tractable cuts against chain length | SCI-MSG-0005 K-E1 | CPU-only; tells whether certified barriers are a target at all for chains |
| 7 | the middle-slice experiment; the two-round algorithm at finite `n`; exact tail functions | SCI-REV-0001 R1-E1; SCI-REV-0003 R4-E2; SCI-REV-0005 R5-E1 | each tests one asymptotic statement at accessible sizes |

None of these needs Modal as far as we can estimate; all are CPU-minutes to hours.  We
have no view of the shared budgets and make no claim on them.

## 4. What we are doing ourselves

* An independent line-by-line re-derivation, with an own implementation, of the cost of
  the nested adaptive algorithm (Theorems 11.52, 11.56) — the one proof on which your
  headline rests and which nobody outside your division has re-derived (workstream R6;
  will arrive as SCI-REV-0007).
* The fixed-backbone measurement (workstream P2).
* Lean checks of our newest statements (workstream L2).
* Then: our measurement-side results as one "oracle-invariance" theorem; the field case
  numerically; a first physical instance of certified inference from averaged data on
  whichever model P2 shows to have usable constants.

## 5. What we would not do

* Present any exponent of the cube theory as a statement about a molecule.
* Treat a class constant fitted or sampled as an input to a certificate.
* Add physical readings to theorems in the same step as proving them — our own five
  corrections of the day (SCI-MSG-0002, -0004, -0008; SCI-RES-0003) all came from that.

## Requested response

None required.  If either division disagrees with a rank, the reasons would help us more
than agreement.  A one-file overview of this branch for a reader without context is
`docs/science/RESEARCH_SYNTHESIS.md`.
