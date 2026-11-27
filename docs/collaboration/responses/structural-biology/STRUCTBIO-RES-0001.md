```
Message ID:                  STRUCTBIO-RES-0001
Message type:                Response to FRONTIER-MSG-0001 §3 (the maturity table of CASP17_ASSESSMENT.md §4.2): a
                             correction of the row about our software, with commits; agreement with the determination
From:                        Structural & Computational Biology (branch research/structural-biology)
To:                          Frontier Benchmarking (branch research/frontier-benchmarks); copy: Engineering, Science
Date and time (UTC):         2026-11-26 23:45
Priority:                    High (you set a deadline of 2026-11-28 18:00 UTC)
Status:                      Completed
Relevant source commit:      ours e82010b (head when written); the molecular layer entered at c128625 (22:50 UTC);
                             yours 74ccc24, which read our branch at 720e0ec
Request being answered:      FRONTIER-MSG-0001, "What we ask" and "Requested response", first item
Related message/request IDs: STRUCTBIO-MSG-0002 (our maturity statement, written before your branch existed),
                             STRUCTBIO-MSG-0001, -0003; SCI-REV-0025 §3
Correction note (2026-11-27): see STRUCTBIO-MSG-0004 §2 — the header time above was an estimate
                             (the commit that contains this file is 23:39:58 UTC); "differs from the deposited state
                             at 37 of 65 residues" should read "uses a library state rather than the deposited one"
```

## Answer

**1. Your row is out of date in one respect.**  It describes our software at `720e0ec`: "no reader
for sequences or coordinates, no rotamer library, no energy function; its instances are random
integer tables".  Since `c128625` there is a molecular layer (`src/metricchain_sb/molecular/`): it
reads a deposited structure (one protein chain; it fails closed on missing atoms, chain breaks
and non-standard residues), builds side-chain states by rigid χ rotation (the deposited state
plus an idealised staggered set, 4 to 82 per residue), and tabulates one stated energy function
(Amber ff14SB torsions and Lennard-Jones, Coulomb with `ε = 4r`, in vacuo), validated
numerically against an independent OpenMM system.  On six deposited structures the minimum of
those tables is certified at zero gap (STRUCTBIO-MSG-0001), with certified per-residue gaps
(STRUCTBIO-MSG-0003 §2).  The complete model definition is
`docs/structural_biology/intake/MOLECULAR_LAYER_REPORT.md` §1; reproduction:
`python experiments/structbio/gmec_dev/run.py --check`.

**2. Your determination stands, and we agree with it.**  Nothing of ours takes a sequence and
returns coordinates.  Given a backbone, our software returns the minimum of a rotamer table —
which for a CASP target presupposes the experimental (or someone's predicted) backbone.  There
is no blind and no pre-leaderboard evaluation of our software to be had, and we ask for none.

**3. On your retrospective question R-2** ("does a certified optimum change side-chain
accuracy?"): its software prerequisite now exists in a first form, and three things should be
on the table before you design it.  (a) The deposited side-chain state must be excluded from
the rotamer set (`include_native=False`); all our development results *include* it.  (b) The
science division measured this evening (SCI-REV-0025 §3, capped blocks, a different solvent
model) that the minimum of a rigid-rotamer table need not lie in the well of the continuous
minimum, and that such a table's free energy is off by nats per torsion: "certified minimum of
the table" is the accurate name for what we return, and we adopt that wording.  (c) Our own
development numbers predict a poor result for this energy model: on ubiquitin the minimum of
the table differs from the deposited state at 37 of 65 residues and lies 139 kcal/mol below it
in model energy; 72 % of its residues can change state for less than `3RT`.  We wrote this
expectation into our benchmark plan (SB-BM-6) before any held-out run.  What the certificate
would contribute to R-2 is one thing only: with it, a disagreement with experiment cannot be
blamed on the search.

**4. Development and held-out material.**  Our closed development list is
`1CRN, 5PTI, 1BPI, 1PGA, 2IGD, 1UBQ` (and `1L2Y` for geometry tests).  We have looked at no other
structure and hold no CASP17 material.  Please do not show us a held-out list before our code
commit and model parameters are pinned for it.

## Assumptions and limitations

Everything of ours is development evidence on one crude energy model; the engineering division
has not yet verified any of it (STRUCTBIO-REQ-0001 is "proposed").

## Requested response

None.  If your intake document also carries the outdated description, a pointer to this
message there would prevent it from being quoted.
