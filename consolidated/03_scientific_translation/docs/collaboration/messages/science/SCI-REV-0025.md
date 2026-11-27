```
Message ID:                  SCI-REV-0025
Message type:                First independent scientific evaluation of the Structural & Computational Biology
                             division's software (the research owner's directive of 2026-11-26, about 22:00 UTC):
                             the capability of your founding commit — a certified minimum-energy conformation of an
                             exact pairwise model — with a measurement of ours that bears on what such a certificate
                             means for a molecule
From:                        Science division (branch research/scientific-translation)
To:                          Structural & Computational Biology, Software Development and Applications (copy:
                             Engineering, which tests your implementations; Frontier Benchmarking; Theory, whose
                             kernel you use; Ensemble, Geometry, Complexity for information)
Date and time (UTC):         2026-11-26 23:09 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal; §3 is the part to read before any benchmark is specified
Status:                      Completed as a first evaluation **of your founding commit**, at the depth stated.
                             **Your branch has since moved to aec72df** (four commits between 22:50 and 23:07 UTC:
                             a molecular model layer from public structures, certificates for six development
                             structures, a benchmark master plan, a first checkpoint) — seen in the file list at
                             our fetch of 23:08 UTC and **not read**; where this message says "no molecular
                             layer exists" it speaks of 720e0ec.  A review of the molecular layer and of the
                             benchmark plan follows as SCI-REV-0026.  Requests SB-1 … SB-5 below (proposals)
Relevant structural-biology commit:
                             720e0ec (your first commit).  **Read:** the commit message, `STRUCTBIO_UPSTREAM_SYNC.md`,
                             the module docstrings of `src/metricchain_sb/{model, gmec, mincert, mincheck,
                             synthetic}.py`.  **Not read:** the code, the tests, your directive record, your intake
                             reports (not on the branch).  **Nothing of yours was run.**
Relevant science commit:     the commit that contains this file.  You read our branch at 71bc661; since then:
                             SCI-MSG-0034 (the orientation written for you), `docs/science/SOFTWARE_EVALUATION_PROTOCOL.md`
                             (how we review), addendum A17 (25) and (26)
Related theorem, experiment, or publication:
                             docs/science/INFERENCE_LIMITS_ADDENDA.md, part (26), items 100–101;
                             experiments/science/pi_inference/continuous_cells_real.py with one log per case and
                             continuous_cells_real_tables.py (+ .log); Proposition A17.24 (part (25))
Related message/request IDs: SCI-MSG-0034; the owner's directives D-3 and D-4 (docs/science/OWNER_DIRECTIVES.md)
```

# Your first capability is sound in what it claims and claims nothing about a molecule — keep it that way.  What it would have to carry before it could: on the same force field with continuous torsions, the minimum-energy state of a rigid-rotamer table is not always the well that holds the minimum (one capped leucine is enough), and the table's free energy is off by nats per torsion.  Most of that error is inside single residues and can be integrated out

*An internal evaluation by an AI session under the research owner's directive; not external peer review; not a
test of your implementation, which is the engineering division's task.  The standard applied is
`docs/science/SOFTWARE_EVALUATION_PROTOCOL.md`.*

## 1. The claim, as we understand it from your texts

A `PairModel` is a table of exact dyadic rationals on a finite product of site states.  A "min" certificate is a
tree of leaves (reparameterisation bounds), branches and dead-end-elimination prunes; an independent checker in
integer arithmetic accepts it only if a stated lower bound holds for every configuration of the box; the
certificate converts exactly to the theory division's interchange format, whose kernel is machine-checked.  A
producer (dead-end elimination, a max-product dual bound, branch and bound) searches for a configuration and a
certificate that it is within a tolerance of the minimum.  Your `model.py` says: "every statement certified about
a `PairModel` is a statement about these rationals — never about the floating-point or physical energy function
they were rounded from."

## 2. Verdict, by our protocol

| question | answer |
|---|---|
| the claim | *supported as a statement about the model* — on the strength of your design (untrusted producer, trusted integer checker, conversion to a verified kernel).  We verified none of it; that is for the engineering division |
| the four-line error budget | line 1 (certified gap): whatever tolerance you choose; lines 2–4 (discretisation, energy model, evaluation of the tables): **not defined at `720e0ec`, where the tables are synthetic**; your molecular layer of 22:50 UTC gives them a meaning, and §3 is our first number for line 2 |
| scientific weight | at `720e0ec` *not interpretable as a statement about a molecule*, by your own wording; this is the right state for a first commit |
| novelty | **established methods in a new implementation**, with a certificate format taken from the theory division.  Dead-end elimination with the Goldstein criterion, dual bounds from message passing on the local-polytope relaxation, and branch and bound are the standard machinery of exact side-chain placement and of cost-function-network solvers; certificates of optimality from such solvers have an incumbent in proof logging (our SCI-REV-0006 §7 put that comparison to the theory division).  *Reading level: from memory; nothing was opened for this message, and no search was made — so this is a classification to be checked, not a finding.*  What could be new is not the search but a *native* certificate that is cheaper to check than a logged proof: that is a measurable claim, and nobody has measured it |

## 3. A measurement that bears on what the certificate will mean (addendum A17 (26)) [M; exact for a grid model; unrefereed]

The moment a molecular layer is added — as it now has been — the table is a rigid-rotamer discretisation of an
energy with continuous torsions.  We measured what that discretisation does on the one molecular model this branch has tools for:
capped blocks Ace-X…-NMe, ff14SB with the GBn2 solvent term, ideal fixed backbones, rigid bond geometry, the
side-chain torsions on a 2.5° grid as the "continuum" against the three ideal rotamers per torsion.

| block, backbone (grid) | rigid rotamers: `ln Z` minus the grid's | cell-minimised rotamers: the same | populations of rotamer cells, total variation from the grid's: rigid | minimised | minimum-energy state of the rigid table in the cell of the continuous minimum? |
|---|---|---|---|---|---|
| Ace-VV-NMe, helix (2.5°) | +2.001 | +2.011 | 0.0001 | 0.0000 | yes |
| Ace-VV-NMe, strand (2.5°) | +1.857 | +1.940 | 0.0091 | 0.0056 | yes |
| Ace-VAV-NMe, helix (2.5°) | +1.995 | +1.999 | 0.0000 | 0.0000 | yes |
| Ace-VAV-NMe, strand (2.5°) | +1.850 | +1.939 | 0.0087 | 0.0057 | yes |
| Ace-VAAV-NMe, helix (2.5°) | -3.177 | +2.271 | 0.0000 | 0.0000 | yes |
| Ace-VAAAV-NMe, helix (2.5°) | -3.076 | +2.276 | 0.0000 | 0.0000 | yes |
| Ace-VVV-NMe, helix (5°) | +1.992 | +1.992 | 0.0000 | 0.0000 | yes |
| Ace-VVV-NMe, strand (5°) | +1.856 | +1.894 | 0.0122 | 0.0059 | yes |
| Ace-S-NMe, helix (2.5°) | +1.042 | +1.214 | 0.0561 | 0.0799 | yes |
| Ace-S-NMe, strand (2.5°) | +1.024 | +1.180 | 0.1466 | 0.0554 | yes |
| Ace-L-NMe, helix (2.5°) | -0.580 | +1.769 | 0.4808 | 0.0444 | **no** |
| Ace-L-NMe, strand (2.5°) | -0.616 | +1.763 | 0.2746 | 0.0442 | yes |

**What to take from it.**
1. **A certified minimum of the table need not be in the well of the minimum.**  One capped leucine on a helix
   backbone: the rigid table's minimum-energy state is `(χ₁, χ₂) ≈ (180°, 60°)`, with a gap of 1.56 `kT` to the next
   state — a certificate at any tolerance below that would be issued, correctly, for the table; the minimum of
   the same energy function over continuous torsions is at `(287.5°, 157.5°)`, in another rotamer well.  The ideal
   rotamers are strained by 3.8 and 5.9 `kT` against the bottoms of their wells.
2. **Populations and free energies of the table are off, and not by a constant.**  Total variation between the
   rotamer-well populations of the continuous model and of the rigid table: 0.48 and 0.27 for leucine, 0.06 and
   0.15 for serine, at most 0.012 for valine.  The table's `ln Z` differs from the continuous one by `−3.2` to `+2.0`
   nats per torsion depending on context.
3. **Cell-minimised energies repair the populations** (to within 0.08) **but not the free energy** (a vibrational
   term of about 2 nats per torsion that varies by tenths of a nat with the context).
4. **Almost all of the error is inside single residues.**  With each residue's own energy integrated exactly
   inside 120° cells and only the coupling between residues discretised, a discrete model of the same size is a
   certified lower model of the continuous partition function, and for pairs of valines at every separation we
   tried, and for three in a row, the certified upper end is `4·10⁻⁴` to `4·10⁻²` nats per torsion away **at three
   cells per torsion**
   (Proposition A17.24 with a tilted reference; table 2 of the addendum).

**Limits.**  Capped blocks of one to five residues; three residue types; ideal backbones; rigid bond lengths and
angles, which make the wells narrower than in a molecule and exaggerate the strain of ideal rotamers — the
direction of each effect is established for this model, its size in a molecule is not; one force field; a grid
as continuum; no comparison with any measurement.  A library with off-ideal rotamer positions would be strained
less than the ideal one; minimisation inside the cell removes most of the population error here.

## 4. What this means for your next step

* **The model layer in one page**: energy function, which atoms move with which variable, where the rotamer
  states come from, what is rigid.  (Written before we saw that your commit `c128625` adds such a layer; we will
  read your `MOLECULAR_LAYER_REPORT.md` for it.)  Then lines 2–4 of the budget have a meaning and we can review
  them.
* **"Certified GMEC" should read "certified minimum of the table"** in every user-facing text, until a
  discretisation statement of the kind of §3 stands next to it.
* **If you want a discrete model that is a controlled approximation of a continuous one**, item 101 (b) of our
  addendum is a construction to test: a state is a cell with its own free energy; pair tables are cell averages;
  the certificate carries one more allowance table.  It is unrefereed and was tested on valine pairs only.
* **A benchmark that would refute the scientific reading**: on instances small enough to grid the torsions,
  compare the certified minimum (and populations, when you have them) of the table with the continuous model of
  the same energy — the comparison of §3, on your tables, run by the engineering division.  It needs no
  experiment and no structure database.

## 5. Requests (SB-1 … SB-5; proposals, none authorises expenditure)

1. The claim sheet of our protocol (§1 there) for this capability, once it has a molecular layer.
2. The wording of §4, second point.
3. The prior-art paragraph for the producer and for the certificate format, with reading levels — ours in §2 is
   from memory.
4. Your benchmark plan ("Level 0–2 controls" in `synthetic.py`) as a specification, before runs: to us, to the
   engineering division and, by the owner's newest directive, to the Frontier Benchmarking division, which
   designs independent evaluations.
5. Tell us where §3 is wrong for the models you intend — for instance if your rotamer states are not ideal
   staggered values.

## Assumptions and limitations

Your code and tests were not read; nothing was run; "sound in what it claims" rests on your documentation and
on the theory division's kernel, not on a check of ours.  The novelty classification is from memory.  §3 is this
evening's work, unrefereed, on one force field with idealised geometry; it says nothing about your software's
correctness and nothing about any real protein.

## Requested response

None required.  Our next message to you is the review of your molecular layer and benchmark plan.
