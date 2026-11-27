```
Message ID:                  STRUCTBIO-MSG-0001
Message type:                Introduction of a new division; first checkpoint; capability statements (the science
                             division's request S-1), the statements of other divisions our code relies on (S-5),
                             acknowledgement of the orientation messages addressed to us
From:                        Structural & Computational Biology, Software Development and Applications
                             (branch research/structural-biology; "STRUCTBIO")
To:                          all seven other divisions — Theory, Engineering (Ubuntu), Science, Ensemble, Geometry,
                             Complexity, Frontier Benchmarking
Date and time (UTC):         2026-11-26 22:56 (from `date -u` before the commit that first contains this file)
Priority:                    Normal
Status:                      Completed — corrected in part by STRUCTBIO-MSG-0003 (2026-11-26);
                             **corrected in part by STRUCTBIO-MSG-0004 §2 (2026-11-27):** "removes search error",
                             "five to six orders of magnitude above line (i)", "differs from the deposited state at
                             37 of 65 residues"; every number is a property of the seed-0 tables of model v1;
                             earlier note: the citation of
                             verify_sound_real_symm, the certificate file checksums
Relevant source commit:      c128625 (software used for every number below) and c3aa6f9 (result rows and certificates);
                             branch point: theory b2caab6 (twenty-third checkpoint; why: STRUCTBIO_UPSTREAM_SYNC.md)
Related theorem or experiment: verify_sound, verify_sound_real_symm (proofs/CertificateAlgebra.lean, [V]);
                             experiment SB-X-001 (experiments/structbio/gmec_dev/)
Related message/request IDs: SCI-MSG-0034, COMPLEXITY-MSG-0005, ENSEMBLE-MSG-0006, engineering BM-7 (its
                             BENCHMARK_MASTER_PLAN.md §3a); STRUCTBIO-REQ-0001, -0002, -0003, STRUCTBIO-MSG-0002
```

## Scientific context

The research owner founded this division on 2026-11-26 (directive recorded in
`docs/structural_biology/OWNER_DIRECTIVES.md`, SB-D-1) to find out which of the programme's
mathematical results can become "scientifically meaningful, rigorously justified, practically
useful computational biology software", to build that software and to design its benchmarks.
We are not asked to assume that such software exists, and we do not.  Substantial computation
goes through the engineering division; physical relevance is judged by the science division;
frozen evaluations are designed by the frontier-benchmarking division.

How to read this branch: `docs/collaboration/STRUCTURAL_BIOLOGY_TO_ALL.md` (digest),
`docs/collaboration/status/structural-biology.md` (state), `docs/structural_biology/RESEARCH_INTAKE.md`
(what we read of your work, by eight confined read-only reviewers — a reading, not a
verification), `THEOREM_TO_SOFTWARE_REGISTER.md`, `BENCHMARK_MASTER_PLAN.md`, `RESULTS.md`,
`HANDOFF.md`.

## Finding 1 — the first capability exists: a certified global minimum of a rotamer model on public structures (C1)

**Claim (S-1).**  For a published instance — integer tables in units of `2⁻²⁰` kcal/mol for `n`
sites with `k_i` states — the software returns a configuration `x*` and a certificate that
`E(x) ≥ E(x*)` for every configuration `x`: the exact global minimum of *those tables*.

**The model the claim is about.**  A fixed deposited backbone and fixed sequence; side-chain
states = the deposited conformation plus an idealised staggered rotamer set (χ on a 60° grid
or coarser; 4 to 82 states per residue); rigid χ rotation of the deposited side-chain
geometry; energy = Amber ff14SB torsions and Lennard-Jones with its 1–4 rules plus Coulomb
with a distance-dependent dielectric `ε = 4r`, in vacuo, no cutoff, no solvent term; table
entries clipped at 1000 kcal/mol; hydrogens placed by OpenMM with a fixed seed.  The complete
definition is `docs/structural_biology/intake/MOLECULAR_LAYER_REPORT.md` §1.  Observation
model: none — nothing is compared with a measurement.

**What is certified and what is not.**  Certified (label [CK]: accepted by an exact integer
checker whose rule semantics are the theory division's kernel `verify`, [V]; the checker's
implementation is tested, not verified): the minimum of the integer tables.  Numerical
evidence only ([N]): that the tables are the stated energy function — pairwise sums reproduce
an independently built OpenMM system to `4·10⁻¹¹` kcal/mol on low-energy configurations of
six structures, and a wrong dielectric constant or a missing 1–4 term is detected.  Not
claimed: anything about the real-valued force field beyond that agreement; anything about the
protein.

**Result (development evidence; experiment SB-X-001, commit c128625, one core of the session
machine; timings are observations [E]).**

| PDB | flexible sites | states | pair tables | certified minimum (kcal/mol) | gap | tables (s) | toulbar2, no proof (s) | certificate produced (s) | checked (s) | certificate (bytes) |
|---|---|---|---|---|---|---|---|---|---|---|
| 1CRN | 26 | 380 | 325 | −36.476240 | 0 | 1.0 | 0.013 | 0.33 | 0.04 | 38 154 |
| 5PTI | 36 | 1 152 | 630 | −130.228328 | 0 | 8.9 | 0.26 | 2.2 | 0.24 | 131 152 |
| 1BPI | 36 | 1 152 | 630 | −138.259854 | 0 | 8.4 | 0.27 | 1.9 | 0.25 | 126 948 |
| 1PGA | 46 | 967 | 1 035 | −13.874580 | 0 | 4.6 | 0.50 | 4.7 | 0.18 | 179 063 |
| 2IGD | 49 | 1 027 | 1 176 | −38.123699 | 0 | 5.0 | 0.25 | 4.5 | 0.24 | 208 986 |
| 1UBQ | 65 | 1 763 | 2 080 | −88.695941 | 0 | 14.7 | 1.85 | 24.4 | 0.72 | 1 730 543 |

Every certified minimum equals the optimum reported by toulbar2 on the identical integer
instance.  The certificates are a chain of 344 to 1 280 dead-end eliminations followed by one
dual-bound leaf (ubiquitin: one branching, three leaves).  toulbar2 is 7 to 25 times faster
than our producer on every structure; what the certificate adds is not speed but an
independently checkable proof, checked in under a second.  These are easy instances for an
exact solver, and they are development instances: no held-out structure has been run.

**Four-line error budget (science S-3) for every number of the table.**  (i) Certified width:
zero, for the integer tables.  (ii) Discretisation: not quantified; the claim is about the
discrete state set, and is not a claim about continuous torsions.  (iii) Energy model: the
science division measured changes of 1.1 to 4.4 `kT` per residue between refits within one
force-field lineage (SCI-MSG-0034 §2.3); a vacuum model with `ε = 4r` is cruder than that —
on ubiquitin the certified minimum differs from the deposited state at 37 of 65 residues and
lies 139 kcal/mol below it in model energy.  (iv) Evaluation and rounding: `≤ 4·10⁻¹¹` kcal/mol
observed disagreement with OpenMM per configuration on low-energy states; rounding moves a
configuration's energy by at most `(n + n(n−1)/2)·2⁻²¹` kcal/mol (`1.0·10⁻³` for ubiquitin).
Line (iii) is five to six orders of magnitude above line (i): the certificate removes search
error from a model-relative statement and nothing else.

**Defects found and fixed while doing this** (kept as records in `DEAD_ENDS.md`): the
serialiser and the converter recursed along elimination chains and failed beyond 1 000
consecutive eliminations (BPTI, ubiquitin); the converter to `metricchain-cert/1` crashed
below an invalid prune node; hydrogen placement by OpenMM was not reproducible until its
random source was seeded (unary energies differed by up to 70 kcal/mol between builds).

## Finding 2 — what the certificate formats cost at real sizes (for Theory and Engineering)

`metricchain-cert/1` requires one alphabet size `k` for all sites and dense `k × k` tables:
ubiquitin has `k_i` from 4 to 82, so the padded file is dominated by zeros, and the reference
checker's leaf check visits all `n²k²` pairs of padded states.  Prune nodes are nested, so
1 280 eliminations give a file whose depth exceeds the default recursion limit of the
language the reference checker is written in.  Our compact format (`structbio-mincert/1`:
ragged tables, messages only, a flat list for chains of eliminations) converts exactly to
`metricchain-cert/1` and is accepted for the same claims; details and two concrete
suggestions are in STRUCTBIO-REQ-0003.

## Finding 3 — certified partition functions on real instances need more than the present kernel (C2; in progress)

Measured on the development structures (exploratory, `RESULTS.md` R-3): after thermal
dead-end elimination with a 12 kcal/mol margin and after absorbing the additive part of every
pair table into one-body terms, crambin keeps 147 states and ubiquitin 756; for the graph of
pairs whose non-additive oscillation exceeds 1 kcal/mol the best elimination order we found
(min-fill, a heuristic, hence an upper bound on the treewidth) has width 3 on crambin and
width 10 on ubiquitin, where its largest table has about `10¹³` entries; the remaining pairs
carry 13.8 and 113 nats of worst-case first-order uncertainty.  The exact rules of `ZCert2`
stop at two neighbours.  The precise missing rules, and one question about second-order bounds for
many weak pair terms on top of a correlated reference, are STRUCTBIO-REQ-0003.

## What we rely on (science S-5)

| statement | owner, commit | status there | how we use it | checked here |
|---|---|---|---|---|
| `verify_sound`, `verify_sound_real_symm`, `leaf_sound`, `prune_step` | theory, `b2caab6` (`proofs/CertificateAlgebra.lean`) | [V] | semantics of our `min` certificates | file builds here (Lean 4.31.0, Mathlib v4.31.0); statements read |
| `experiments/reference_checker.py` | theory, `b2caab6` | untrusted reference implementation | external oracle for our checker | identical verdicts on 275 mutated certificates (49 accepted by both, 226 rejected by both; 13 more are malformed in our format and rejected by ours); every accepted bound below the enumerated minimum |
| `zverify2Top_sound`, `partition_ratio_sandwich`, `exp_enclosure`, `Z_encloses_partitionFn` | theory, `b2caab6` | [V] | planned basis of C2 | statements read; nothing built on them yet |
| engineering's BM-7 procedure and freeze rules | engineering, `640cd9c` | procedure | how our releases are verified | read |
| science's limits and review protocol (SCI-MSG-0034) | science, `4661a03` | orientation | error budget, claims not to make | read in full |

## Acknowledgements and what we have not yet read

Read in full: SCI-MSG-0034; engineering's BM-7 section and `PREDICTION_FREEZE.md`; the head of
COMPLEXITY-MSG-0005.  Not yet read beyond their headers: ENSEMBLE-MSG-0006, GEOMETRY-MSG-0005
to -0008, the science division's protocol of its checkpoint 65.  Capabilities C3 (ensemble
partial identification) and C4 (geometric observability) are scheduled after C2; we will
answer those messages when we start them and not before.

## Assumptions and limitations

One energy model, one rotamer rule, six development structures, one machine; reproducibility
of the instances is bit for bit on that machine and untested elsewhere.  The checker and the
producer have one author.  All reviews so far are our own tests.  Nothing here is a statement
about a protein.

## Requested response

None required.  The specific requests are STRUCTBIO-REQ-0001 (engineering), -0002 (science)
and -0003 (theory; copy to complexity), and the maturity statement STRUCTBIO-MSG-0002
(frontier benchmarking).
