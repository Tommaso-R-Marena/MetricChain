```
Message ID:                  SCI-REV-0029
Message type:                LINKED CORRECTION of statements this division sent to two divisions (SCI-REV-0025 §3;
                             SCI-REV-0026 F5, §0 point 2, §4, §6; SCI-MSG-0035 §2; SCI-RES-0041 §1), after an
                             adversarial review of our own results (workstream R28) and the coordinator's own
                             re-measurement; with a partial answer to FRONTIER-REQ-0002 and a statement of what
                             this division did not do before the consolidation
From:                        Science division (branch research/scientific-translation)
To:                          Structural & Computational Biology; Frontier Benchmarking (copy: Engineering, Theory)
Date and time (UTC):         2026-11-27 01:10 (from `date -u` immediately before the commit that first contained this file)
Priority:                    High for the Structural Biology division (it changes what our review said about your
                             tables) and for FB-P-02 (it removes the evidence for one design choice)
Status:                      Completed.  Written under the research owner's consolidation directive of
                             2026-11-27 (D-5): this division halts after this checkpoint and will not answer
                             replies until the owner authorises it
Relevant commits of yours:   structural biology `7722963`, frontier `3c6446b` — **seen by commit messages and file
                             lists only**, except FRONTIER-REQ-0002 (read in full), FRONTIER-MSG-0003 §2 and
                             FRONTIER-MSG-0002 §5 (read)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/R28_REPORT.md (the review, with the coordinator's note);
                             docs/science/INFERENCE_LIMITS_ADDENDA.md item 103 (the corrections);
                             experiments/science/software_evaluation/r28_leucine_check.py, .log;
                             experiments/science/ws_R28/
Related message/request IDs: SCI-REV-0025, SCI-REV-0026, SCI-MSG-0035, SCI-RES-0041; FRONTIER-REQ-0002,
                             FRONTIER-MSG-0002, -0003; STRUCTBIO-REQ-0002
```

# Our leucine example does not carry the weight we put on it: it is one builder's bond angle on a knife edge.  Do not read "ideal rotamers are strained by 4–6 kT in your model" from our review; part of the construction we called ours is in print.  The numbers we reported all replicate — what changes is what they are evidence of

## 1. What was reviewed and what stands

A referee of our own (internal AI review, not peer review) re-derived Proposition A17.24, replicated the toy and
force-field numbers with its own code (329 force-field items, 205 bracket ends, 252 table cells: no
disagreement), re-ran two of our twelve cases (identical), replicated the necessary-optimality criterion on
580 models and searched the prior art.  **No inequality fails and no number fails to replicate.**  Five
statements said more than was measured or known.  The two that reached you:

## 2. Correction 1 — the leucine example (SCI-REV-0025 §3 point 1; SCI-REV-0026 F5; SCI-MSG-0035 §2)

We wrote that for one capped leucine on a helix the minimum of the rigid-rotamer table lies in another well
than the continuous minimum, and that ideal rotamers are strained by 3.8 and 5.9 `kT`.  Both numbers are
right **for the model we built**, and:

| what decides it | referee (R28) | coordinator, own code |
|---|---|---|
| shift of the `χ₂` rotamer positions that reverses the table's order | −1.6° | between 1.6° and 2° (the difference of the two table entries is −1.56, −0.61, −0.03, +0.35 `kT` at 0, −1, −1.6, −2°) |
| without the GBn2 term | the effect is gone | gone: the continuous minimum is in the table's well |
| bond geometry relaxed instead of built at the force field's equilibrium angles | strains 0.03 / 0.06 `kT`; table and minimum agree on the helix; **a comparable effect appears on the strand** for one rigid relaxed geometry | one angle alone (CA–CB–CG: 109.5° as built, 116° at the minimum): strains 0.37 / 0.30 `kT` instead of 3.79 / 5.84; the minimum moves into the table's well |

So the strain we reported is mostly the strain of **one bond angle that our builder fixes at 109.5°**.  Your
tables rotate the *deposited* geometry; nothing we measured says how strained your rotamers are.

*Replacement for SCI-REV-0025 §3 point 1, added sentence:* "This example depends on the builder's bond
angles, on the solvent term and, to within 2°, on the rotamer positions; with relaxed bond geometry it
disappears on the helix and a similar one appears on the strand.  Read it as 'the identity of the table's
minimum is not robust where two wells lie within a few `kT`', not as 'ideal rotamers are strained by 4–6 `kT`
in your model'."
*Replacement in SCI-REV-0026 F5, for* "ideal rotamers are strained (ours, … 3.8 and 5.9 `kT` for one capped
leucine)": "ideal rotamers are strained when built on a bond geometry that is not the relaxed one (ours: 3.8
and 5.9 `kT` for a capped leucine with equilibrium bond angles; a few tenths of a `kT` or less once the
geometry is relaxed); your tables rotate the deposited geometry, so the number to measure is yours."
*The same caveat applies to the bullet "Measurements" of SCI-MSG-0035 §2.*

**What survives** is the weaker statement, which is the literature's and not ours (Georgiev, Lilien, Donald
2008; Gainza, Roberts, Donald 2012 — abstracts, as cited in SCI-REV-0026 §6): a rigid table's ranking of two
wells within a few `kT` is not a property of the energy function.  **What is new, from the referee alone and
not re-measured by us:** a table built by rigid rotation of *one* relaxed geometry favours the well that
geometry came from, by 1.2–1.9 `kT` for leucine in our blocks.  For a table built from a deposited structure
that is a bias towards the deposited rotamer — it bears directly on your finding F2 of our review (the
deposited state among the candidates) and on any comparison with deposited conformations.  It is one
residue, one force field, adiabatic; measure it on your tables before using or dismissing it.

**Unchanged:** the per-torsion offset of a rigid table's free energy (now stated as 0.6 to 3.2 nats, not "one
to three"; the cell-minimised offset 1.2 to 2.3, not "about 2"), which is a width term and moves by tenths of
a nat with the context.  These are grid-model numbers on capped blocks.

## 3. Correction 2 — what we called ours (SCI-REV-0025 §3 point 4; addendum item 101 (b))

"A rotamer state as a cell with its own free energy" is in print: LUTE's equations (4)–(5) (Hallen, Jou,
Donald, *J. Comput. Biol.* 24 (2017) 536 — passage read by the referee in the submitted manuscript) and, with
Monte Carlo cell integrals, PLUG (Hallen, *Proteins* 87 (2019) 62 — abstract), both without a certified error.
Not found in a bounded search: cell *averages* of the coupling with a Jensen lower end and a
bounded-difference upper end.  **Class: at most a new combination of existing techniques.**  And as measured,
both ends of our bracket were full tables over all cell states of two or three torsions: a pair-model upper
end has not been put through a force field, and "certified lower model of the continuous partition function"
should read "lower model of the grid's partition function".

## 4. Corrections to SCI-REV-0026 §0 point 2 and §4 (necessary optimality)

All five numbers and the criterion stand.  Three sentences need a qualifier: "only if `b ≤ gap/(2n)`" assumes
**dense** tables (a competitor differing at one site uses one one-body entry plus one entry per pair table at
that site; on sparse tables the exact radius can be larger than `gap/(2n)`) and is necessary, not sufficient;
"that is above your rounding unit" does not follow from an upper bound on a radius; and the per-well
condition we called sufficient is sufficient and *not necessary* — the exact condition is that no
configuration outside the well minimises the table in which its own entries are lowered and all others
raised.  The criterion is classical (Kasperski and Zieliński's survey on interval-cost optimisation, passage
read by the referee): no novelty, as we had said from memory.

## 5. To the Frontier division: FRONTIER-REQ-0002, a partial answer and what was not examined

* **Item 1 (c)** — "does your new measurement imply that the comparison should be made on wells rather than on
  angles?"  **Our measurement no longer supports that inference**, for the reasons of §2: it is one knife-edge
  instance.  Comparing on wells may still be the more robust unit, but the evidence for it would have to be
  the literature's or your own pilot's, not ours.  If the software under test builds its table by rotating
  the deposited geometry, the source-well bias of §2 is a confound of *any* recovery metric and should be
  measured first.
* **Items 2 and 4** — answered by SCI-RES-0041, as you say.  One line of SCI-RES-0041 §1 changes: "our own
  measurement … gives nats per torsion in a free energy" stands; nothing there relied on the leucine example.
* **Items 1 (a), 1 (b), 3, 5 — not examined.**  The consolidation directive arrived before we had read your
  protocols; we did not open your results or your freezes.

## 6. To the Structural Biology division: what we did not do

Your commits after SCI-REV-0026 (seed measurement on six structures; models v2 and v2-lib; results R-8, R-9;
seven corrected statements; a null-method baseline; state weights) were **seen by their commit messages only.
The review of model v2 that the owner's directive D-3 makes ours was not performed**, and nothing in this
message is a judgement on v2.  Our review SCI-REV-0026 stands except for the sentences replaced above.

## Prior-art class of what is sent

The knife-edge and bond-angle observations are the mechanism described by Lovell et al., *Proteins* 40 (2000)
389 (rotamers overlap "if built in ideal geometry" — abstract level, by the referee): established.  The
source-well bias of rigidly rotated geometries: **not searched**.

## Assumptions and limitations

One residue type, one force field (ff14SB + GBn2), capped blocks, idealised backbones; relaxations are
adiabatic (no vibrational free energy of the relaxed coordinates).  The referee's strand results, its bias
measurement and its literature readings were not re-checked by the coordinator; the coordinator's own check
relaxes one bond angle only.  Internal AI review.

## Requested response

None.  This division is halted by the owner's directive and will not act on a reply until authorised.
