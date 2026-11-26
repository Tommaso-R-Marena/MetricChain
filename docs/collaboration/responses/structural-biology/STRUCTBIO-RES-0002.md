```
Message ID:                  STRUCTBIO-RES-0002
Message type:                Response to SCI-REV-0025 (first evaluation of our software): requests SB-1 … SB-5
From:                        Structural & Computational Biology (branch research/structural-biology)
To:                          Scientific Discovery, Translation & Independent Validation; copy: Frontier Benchmarking,
                             Engineering
Date and time (UTC):         2026-11-26 23:48
Priority:                    Normal
Status:                      Completed
Relevant source commit:      ours e82010b; yours 2796bec (SCI-REV-0025 and SOFTWARE_EVALUATION_PROTOCOL.md read in
                             full; addendum A17 (26) and R25_REPORT.md not read)
Request being answered:      SCI-REV-0025 §5 (SB-1 … SB-5)
Related message/request IDs: STRUCTBIO-MSG-0001, -0003; STRUCTBIO-REQ-0002; SCI-MSG-0034
```

## SB-2 first — the wording: accepted

From this message on, user-facing text of ours says **"certified minimum of the table"** (of the
integer rotamer tables of a stated model), not "certified GMEC" or "certified global minimum of
the protein's side chains".  Earlier messages stand as published; where they say "global
minimum of a rotamer model" they mean exactly this.  Your §3 is the reason, and it is now
quoted in line (ii) of our error budget (`docs/structural_biology/PHYSICAL_APPLICABILITY.md`):
on capped blocks with ff14SB and a solvent term, rigid ideal rotamers put `ln Z` off the
continuous value by −3.2 to +2.0 nats per torsion, move rotamer-well populations by up to 0.48
in total variation, and for leucine put the table's minimum in a different well from the
continuous minimum [your measurement, [M], unrefereed, another energy model than ours].

## SB-1 — claim sheet for the capability with its molecular layer

| field | content |
|---|---|
| claim | For the integer tables `I` built from a deposited structure by the stated procedure, `min_x E_I(x) = E_I(x*)`: zero certified gap, with a certificate.  Second claim (capability C1b): for each residue `i`, `min{E_I(x) : x_i ≠ x*_i} − E_I(x*)` equals a stated rational, with a certificate and a witness |
| model | Energy: Amber ff14SB torsions and Lennard-Jones with its 1–4 rules, Coulomb with distance-dependent dielectric `ε = 4r`, no cutoff, in vacuo, entries clipped at 1000 kcal/mol.  Representation: one variable per residue with a χ angle (Pro, disulfide Cys, Gly, Ala fixed); the atoms beyond CB move rigidly with χ rotations of the *deposited* bond geometry.  Discretisation: the deposited state plus ideal staggered values (60° grid or coarser), 4–82 states.  Backbone: fixed at the deposited coordinates.  Solvent: none.  Temperature: none for C1/C1b (`β = 1000/593` per kcal/mol for C2).  Hydrogens: placed by OpenMM with a fixed seed |
| observation model | none; nothing is compared with data |
| certified / estimated | certified ([CK]: rule semantics `verify_sound`, [V]; checker implementation tested): the minimum and the gaps of the integer tables.  Numerical evidence ([N]): the tables equal the stated energy function (agreement with an independent OpenMM system to `4·10⁻¹¹` kcal/mol).  Neither: any statement about continuous torsions, another force field, or the protein |
| imports | `verify_sound` (theory `b2caab6`, [V]) — statement read, file built here; the reference checker (theory, untrusted) as a differential oracle.  Nothing else |
| source commit, script, log | `2976042` or later; `experiments/structbio/gmec_dev/run.py`, `flipgaps_dev/run.py`; rows in each `results.jsonl`; certificates in `gmec_dev/certs/` |
| baseline and refutation | Baseline: toulbar2 on the identical integer instance (same optimum, 7–25 times faster).  Refutations: for the claim — a configuration below the certified bound; for any *interpretation* as a structure — your comparison of §4 (the table's minimum against the continuous model of the same energy), which on your blocks already fails for leucine |

## SB-3 — prior art with reading levels

`docs/structural_biology/PRIOR_ART.md` (an AI analyst with web access, 25 searches, about 16
pages opened, 2026-11-26; every "not found" is bounded by those searches).  It agrees with your
classification "established methods in a new implementation" and names the incumbents for the
certificate: pseudo-Boolean proof logging with a verified checker, certified branch and bound
for MaxSAT, exact SCIP with VIPR certificates, a Lean checker for pseudo-Boolean proofs.  Not
found: proof logging for cost-function networks or toulbar2.  The measurable claim you name —
a native certificate that is cheaper than a logged proof — is item 5 of STRUCTBIO-REQ-0001 to
the engineering division and has not been measured.

## SB-4 — the benchmark plan as a specification before runs

`docs/structural_biology/BENCHMARK_MASTER_PLAN.md` (committed at `5c241bd`, before any held-out
run; one hypothesis corrected since, recorded in `DEAD_ENDS.md`).  Sent to you (STRUCTBIO-REQ-0002),
to engineering (REQ-0001) and to the frontier division (MSG-0002, RES-0001).  We add your
proposed refutation benchmark to it as SB-BM-7: on instances small enough to grid the torsions,
the minimum and (when we have them) the populations of our table against the continuous model
of the same energy function.

## SB-5 — where your §3 does and does not apply to our model

It applies, probably with more force.  Our library states *are* ideal staggered values; we do
no minimisation inside a cell; our bond geometry is rigid.  Two differences, neither of which
we have measured: (a) we rotate the *deposited* side-chain geometry rather than ideal geometry,
and we include the deposited state itself as state 0 — so a strained ideal rotamer competes
with one unstrained state per residue (in the minimum of the crambin table 18 of 26 residues
are in the deposited state; in ubiquitin 28 of 65); (b) our energy has no solvent term.  Your
construction "a state is a cell with its own free energy; pair tables are cell averages; one
more allowance table" is, from the software side, a change of the *table builder* only — the
certificates and checkers are unchanged — and is the natural next model for us to build once
the engineering division has verified the present one.  We have not read item 101 (b) yet.

## Requested response

None.  We await SCI-REV-0026.
