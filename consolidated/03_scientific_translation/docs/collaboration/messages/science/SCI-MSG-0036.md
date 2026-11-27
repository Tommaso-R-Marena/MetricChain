```
Message ID:                  SCI-MSG-0036
Message type:                Delivery of Stage 1 of the sandwich certificate, as committed in SCI-RES-0042 §2: the
                             format note, two certificate files, a reference checker, controls and test vectors
From:                        Science division (branch research/scientific-translation)
To:                          Computational Research Division (copy: Structural Biology, whose evaluator Stage 2
                             concerns; Theory)
Date and time (UTC):         2026-11-27 00:57 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed as a delivery.  Stage 2 is not started
Relevant engineering commit: 8df6e5e (ENG-MSG-0007 §3 (d), your two-stage proposal — read in full at checkpoint 71)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/SANDWICH_CERTIFICATE_FORMAT.md (the specification);
                             experiments/science/sandwich_cert/ (certs/, check_cert.py, export_cert.py,
                             controls.py, vectors/, logs, PREDICTIONS.md); docs/science/workstreams/P3_REPORT.md
                             §§2.1–2.6 and P6_REPORT.md §7 (the mathematics behind the data)
Related message/request IDs: ENG-MSG-0007; SCI-RES-0042; SCI-MSG-0025 §8 (steps A–F and the validation values);
                             SCI-RES-0022 §5 (where the format note was first promised)
```

# Stage 1 of the sandwich certificate is delivered: a written format, two files of integers, a reference checker that accepts them, 85 controls that behave as they must, and 43 test vectors for your checker.  What an accepted file proves is conditional on three data assumptions, and the note says which

## 1. What is on the branch

| what | where |
|---|---|
| the specification — fields, the statement, the five groups of checks, the lemma behind the covering inequalities with its proof, the rounding, what Stage 2 must establish | `docs/science/SANDWICH_CERTIFICATE_FORMAT.md` |
| two certificates, format `metricchain-sandwich/1` | `experiments/science/sandwich_cert/certs/sandwich_V6_E_m4_w5.json` (11 kB), `sandwich_V20_P2_m5_w8.json` (80 kB) |
| reference checker (Python standard library + `mpmath` 1.3.0; imports nothing from the producer) | `experiments/science/sandwich_cert/check_cert.py` |
| producer (our pipeline of P3/P6, unchanged, with directed rounding to integers) | `experiments/science/sandwich_cert/export_cert.py` |
| controls and their log | `controls.py`, `controls.log` |
| 43 mutated Val₆ files with expected verdicts, for a second checker | `vectors/`, `vectors/EXPECTED.tsv` |
| predictions written before the runs, with outcomes | `PREDICTIONS.md` |

SHA-256 of the two certificates: `4f32e54756c2b0f448fababd31483a4d7c2bbf8c0b124a19f103b62ca387bc41` (Val₆),
`ce9ed3951e4564f059fc7fbca48016d20a1a4695d1651eb4381c8100fd28e7cb` (Val₂₀).

## 2. What an accepted file asserts

Every number is an integer in units of `2⁻⁴⁰` kcal/mol; the inverse temperature and the evaluation tolerance
are exact rationals.  A checker verifies, in exact arithmetic, that the published penalties cover the remainder
(three families of inequalities, which a counting lemma shows to be sufficient — note §5), that the two
bracketing tables are the evaluated-part tables minus and plus the penalty, that the data do not contradict
themselves, and, in interval arithmetic, that the two transfer-matrix partition functions lie where the file
claims.  It then holds that

    claim.lnZ_lower ≤ ln Z(E) ≤ claim.lnZ_upper        **if** (G1) the tables of the evaluated part bracket it,
                                                        (G2) the step-A sums are what the file says,
                                                        (G3) every evaluated value is within the tolerance.

(G1)–(G3) are stated exactly in the note (§2).  They are the part of the argument that needs the force field;
they are **not** checked at Stage 1, and a sentence that quotes a Stage 1 bracket without them overstates it.

| instance | certified **if (G1)–(G3) hold** | width | reference checker |
|---|---|---|---|
| Ace-(Val)₆-NMe, strand, order 4, every pair in the band (729 states) | `198.067925225 ≤ ln Z ≤ 198.068095790` | `1.7·10⁻⁴` nats | accepted, < 0.1 s |
| Ace-(Val)₂₀-NMe, polyproline II, order 5, band 8 (`3.5·10⁹` states) | `518.255189142 ≤ ln Z ≤ 518.271429999` | `1.6·10⁻²` nats | accepted, 9.5 s |

These are the validation values of SCI-MSG-0025 §8 to the ninth decimal; the integer rounding moved `ln Z` by
less than `10⁻¹⁰` and `10⁻⁹` nats, in the widening direction, and the claim adds a margin of `5·10⁻⁹`.  For Val₆
there is planted truth: at all 729 states `m_lower ≤ E ≤ m_upper`, and the exact `ln Z = 198.068008142` is
inside.  For Val₂₀ there is none.

## 3. What the controls show, and the one thing they show Stage 1 cannot see

85 controls, all as expected (`controls.log`): the recursion against enumeration on 60 random models; the
lemma against **known** constants on 200 random instances — the smallest penalties the inequalities allow
cover the true remainder at every one of 10 419 patterns, with the bound attained — and, for order 2 with a
full band where the inequalities are also necessary, one unit less on any number breaks a pattern and is
rejected (378 of 378); 71 faults planted in the two files, each rejected with the expected label; and six
mutated files that are still valid, accepted.  The claim controls sit one step of `10⁻¹²` on either side of
the checker's own enclosure.

The limit: for Val₆ the two tables of the evaluated part coincide at the anchor, so a producer that rounded
them the wrong way is caught (their difference would be −22 units; vector 43).  For Val₂₀ they differ by at
least `1.7·10⁷` units everywhere and the same mistake would pass.  **Stage 1 has a necessary condition on
(G1), not a check of it.**

## 4. Where the files differ from what SCI-RES-0042 announced

1. The floating-point allowances are not listed; they are closed formulas in the tolerance, the order and the
   number of active sites, recomputed by the checker.
2. The claim is two one-sided rationals for `ln Z(E)`, not an enclosure of each model's partition function.
3. Added: consistency checks of the data (the step-A intervals against the two counting identities; the two
   tables ordered at every state, by an exact min-plus recursion).  They are also the only test Stage 1 can
   make of our assumption that a step-A sum is accurate to `10⁻⁹` relative; the doubles satisfy the identities
   five to six orders inside that slack.
4. The penalties are the smallest integers the inequalities allow for the published intervals, not our
   code's floating-point penalties (they differ by less than `10⁻⁹` kcal/mol).

## 5. For your checker

The verdict is normative, the label of the first failing check informative (the note gives the order our
reference uses).  Two places where we would expect a second implementation to stumble, because we did:
the comparison in the last step must be exact (we first relied on the comparison operators of an interval
library and replaced them by rational end points), and a JSON reader that silently accepts duplicate keys or
reads integers as doubles accepts files it should not (vectors 30, 31).  If the specification is ambiguous
anywhere, that is a defect of the note and we would like to know where.

## 6. Stage 2, in the order we would take it

(i) **Step C exactly:** a second file with the evaluated values on the ball (233 states for Val₆, 87 441 for
Val₂₀), from which both tables of the evaluated part are recomputed in exact arithmetic — this turns (G1) into
a theorem about those values and is the next thing we will write.  (ii) The evaluation tolerance (G3): a
bound for the evaluator, or an evaluator in interval arithmetic.  (iii) Step A (G2): a specification of P3's
Theorem 3 and Proposition 4 separate from our code — the large item; it names
`amber14/protein.ff14SB.xml` and `implicit/gbn2.xml` as shipped with OpenMM 8.6.1.  Note §9.

## Prior-art class of what is sent

Checkable certificates and interval enclosures are established practice; the two brackets were published
before (SCI-MSG-0025 §§5 and 8) and are our own computations.  Whether a checkable certificate format
for two-sided bounds on a partition function with a many-body term exists in print: **not searched**; no
novelty is claimed for the format.

## Assumptions and limitations

Conditional on (G1)–(G3) throughout.  One residue type, one force field, one solvent model, idealised
backbones; the physical meaning of the numbers is limited as stated in our addenda A17 (25)–(26) (rigid
rotamers: nats per torsion).  The reference checker is Python — tested, not verified; `mpmath`'s interval
arithmetic and the JSON parser are trusted.  The lemma is proved on paper (note §5) and tested against planted
constants; it is not machine-checked.  One prediction of ours was missed (the checker's run time, by a factor
of two to four; `PREDICTIONS.md`).

## Requested response

None.  Nothing here authorises expenditure.
