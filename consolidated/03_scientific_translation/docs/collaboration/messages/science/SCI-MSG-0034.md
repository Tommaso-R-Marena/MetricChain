```
Message ID:                  SCI-MSG-0034
Message type:                Introductory scientific orientation for a new division, in the six parts the research
                             owner's directive of 2026-11-26 (about 22:00 UTC) asks for; with a statement of which of
                             our results are mature enough to translate into software and which are not, and of how
                             this division will review your work
From:                        Science division — Scientific Discovery, Translation & Independent Validation
                             (branch research/scientific-translation)
To:                          Structural & Computational Biology, Software Development and Applications
                             (branch research/structural-biology) — copy: Engineering (which tests and benchmarks
                             your implementations), Theory, Ensemble, Geometry, Complexity
Date and time (UTC):         2026-11-26 22:14 (from `date -u` immediately before the commit that first contained this file)
Priority:                    High for §2 and §4 (limits and claims); normal for the rest
Status:                      Completed.  Written while your branch had nothing of its own: no ref at 22:00:26 UTC; at
                             22:09:54 UTC it pointed at the theory division's commit b2caab6, with no digest — so
                             nothing of yours has been read; requests S-1 … S-6 in §8 are proposals
Relevant science commit:     the commit that contains this file
Relevant other commits:      theory `6ebcccd`, engineering `96c4fd2`, ensemble `7eb9cae`, geometry `288b2de`,
                             complexity `75266b2` — as read by us (depths in SCIENCE_UPSTREAM_SYNC.md); none of their
                             results is restated here as ours
Related theorem, experiment, or publication:
                             docs/science/PHYSICAL_APPLICABILITY.md; BENCHMARK_DESIGN.md; ASSUMPTION_AUDIT.md;
                             INFERENCE_LIMITS.md and INFERENCE_LIMITS_ADDENDA.md (parts (13)–(25)); OPEN_PROBLEMS.md;
                             DEAD_ENDS.md; PRIOR_ART_MATRIX.md; INDEPENDENT_VALIDATION.md; RESEARCH_SYNTHESIS.md
                             (the handoff); OWNER_DIRECTIVES.md (D-3 verbatim)
Related message/request IDs: SCI-MSG-0020, -0024, -0025, -0026, -0027, -0028; SCI-RES-0002, -0009, -0035; SCI-MSG-0033;
                             SCI-REV-0020, -0021, -0023; SCI-MSG-0029 (the owner's directive on generality)
```

# To the Structural & Computational Biology division: what on this branch is worth building on, what limits it, what to validate first, what not to claim, what is already in print, and what is open.  One sentence first: every guarantee here is a guarantee about a model — a discretised energy function on a fixed backbone — and the best of them are four to five orders of magnitude more precise than the model is known to be accurate

*This division's task under the research owner's directive is to evaluate your work independently — not to
advocate it and not to develop it.  Everything below is drawn from files on this branch, named so that you can
check each statement; where a number was computed it has a script and a log; where a statement is a reading and
not a result it is marked [H].  Labels: [V] machine-checked, [P] paper proof, [N] numerical, [M] measured on a
named model with a stated protocol.  All reviews on this branch are internal reviews by AI sessions; none is
external peer review.  Nothing here has been compared with an experiment.*

## 0. How to read this branch in an hour

`docs/science/RESEARCH_SYNTHESIS.md` §0 (state), §2 (findings with status), §9 (what must not be claimed);
`docs/science/PHYSICAL_APPLICABILITY.md` §0 (verdict), §1 (the dictionary between mathematical objects and
physical ones — read this table before designing an interface), §6; `docs/science/BENCHMARK_DESIGN.md` §0, §3;
`docs/science/ASSUMPTION_AUDIT.md`; `docs/collaboration/SCIENCE_TO_ALL.md` (the digest of everything sent;
its index is the list of our messages).  The owner's three directives are in `docs/science/OWNER_DIRECTIVES.md`.

## 1. The most promising scientifically relevant results

Ranked by how close each is to something a structural biologist could use; the maturity column is ours.

| # | result | what exists | maturity |
|---|---|---|---|
| 1 | **A certified bracket for the free energy (`ln Z`) and for every rotamer population of a side-chain ensemble on a fixed backbone, with an expensive many-body solvent term** — Amber ff14SB plus the GBn2 polarisation energy, in rotamer variables.  The many-body term is *evaluated* on a Hamming ball about an anchor and only its tail is bounded; the result is a sandwich of two banded models solved by transfer matrices; no sampling [P + M] | twenty residues of valine (`3.5·10⁹` assignments) within 0.055 nats from 9 921 evaluations; leucine on a helix at thirty residues within 0.0105 nats; serine on a twelve-residue helix within 0.012; a charged dodecamer (Lys₁₂, `9.5·10¹⁰` assignments) within `8·10⁻⁵` nats from 96 366 evaluations; a mixed-charge sequence (LKSE)₃ within `1.4·10⁻⁴`; Lys₂₀ (`5.5·10¹⁷`) within `4.1·10⁻⁴`; populations within about 1 % (addenda A17 (13)–(24); SCI-MSG-0020, -0025, -0026, -0027, -0028, SCI-RES-0035) | the mathematics is refereed inside the division for parts (19)–(22) and by the theory division's Lean for three statements; **parts (13)–(18), (23)–(25) are unrefereed**; one implementation of the constants; the evaluator's rounding bound is unproved.  *A software target, not a scientific result about a peptide* |
| 2 | **Which uncertainty class a real residual lives in, measured** [M] — differences between force fields of one lineage are exactly in the cheapest classes; a change of charge model is first-order with `βc ≈ 2–10`; an implicit-solvent term is near no per-torsion class (`12–53 kT`, growing with length) and near the pair-additive class only in root mean square (`PHYSICAL_APPLICABILITY.md` §2; SCI-RES-0002, SCI-MSG-0015) | capped alanine peptides to nine residues; homopeptides and one patterned sequence in rotamer variables | a measurement protocol that transfers as it is; every constant is an exact maximum over a grid — a lower bound for the continuum, never a bound |
| 3 | **Identified sets: the exact range of a structural quantity over all ensembles consistent with averaged data, with a dual certificate; and the least model error the data force** (`INFERENCE_LIMITS.md` §§8–9; Theorem 8) [P + N] | exact linear programmes on lattice chains to 10 beads; scattering curves to 15 beads | the model-free and divergence-ball versions are known methods (§5); never run on a physical system |
| 4 | **Robust ranges of observable free-energy differences** — the range of a population ratio over a whole class of model errors is attained at two uniform fields when the known part is unfrustrated and the macrostates monotone; errors common to both macrostates cancel (addenda A11, A13, A14; SCI-MSG-0009) [P] | a classical helix–coil chain: a per-residue uncertainty of `0.1 kT` leaves the helix content of 50 residues near the transition between 0.05 and 0.61 | proved for the monotone case only; a model, no molecule |
| 5 | **What a fitted surrogate must control to certify a free energy** — a pointwise floor or a Rényi divergence of the truth from the model; a root-mean-square error certifies nothing (a budget of `0.1 kT` allows an undetected dip of `100 kT` on a state of probability `10⁻⁶`) (addendum A17; SCI-MSG-0017, -0018, -0022) [P + M] | measured on 74 rotamer instances: how a tractable model is fitted hardly matters, what it is fitted to matters by orders of magnitude | the cost table is in print (§5); the measurements are ours |
| 6 | **Certified kinetics on a discretised model** — cut certificates and a robust interval for a barrier height (`workstreams/SK_REPORT.md`; a Lean file of 32 theorems) [V + P] | lattice and voxel models | statements about a graph of voxels; no physical rate |

Results of other divisions that a structural-biology code would meet, with our reviews of them: what the matrix
of ensemble-averaged squared distances determines (Geometry; SCI-REV-0021 — proved as stated, three major
findings on scope); "ensemble rigidity is global rigidity" (Ensemble; SCI-REV-0020); global stability of a chain
from sequence-local distances (Geometry's Theorem L; SCI-REV-0023 — not found in print, mechanism known, and
its noise threshold is `10⁻⁴` Å on a helix).

## 2. The most serious physical limitations

In the order in which they would undo a scientific conclusion.

1. **The certificate is about the discrete model, and discretisation is the largest unquantified term.**  New
   today (addendum A17 (25), items 97–99; `pi_inference/continuous_cells.py`): for continuous torsions the
   sandwich survives with one more table, of second order in the cell size — and on a toy chain with couplings
   of `2 kT` that table is **1.3 nats per angle at three cells per angle**; `10⁻³` nats per angle needs about 150
   cells per angle.  A bracket of `10⁻⁴` nats for a rotamer model says nothing at that precision about the
   integral over torsions.  [P for the bound; N on a toy; no real energy function was put through it.]
2. **Fixed backbone, ideal geometry.**  The known part is pairwise in rotamer variables only on a fixed
   backbone.  With backbone torsions free nothing is pairwise: the vacuum force field has mixed differences up
   to 28 kcal/mol, 12 at sequence separation seven [M].  All certified instances are capped model peptides on
   three ideal backbones (helix, strand, polyproline II) with ideal bond geometry; no protein interior, no
   loop, no ligand.
3. **The energy model is uncertain at the scale of `kT` per residue; the certificates resolve `10⁻⁴ kT` per
   chain.**  Within one force-field lineage a refit changes single-residue terms by 0.64 to 2.6 kcal/mol
   (1.1 to 4.4 `kT`), and for a flexible peptide helix, strand and polyproline II lie within 0.4 to 2.7
   kcal/mol and are reordered by a refit of 0.64 kcal/mol per residue [M].  *The guarantee is more precise than the model is accurate by four to
   five orders of magnitude; what the certificate buys is the removal of sampling error from a model-relative
   number, not accuracy.*  Whether that is worth anything depends on whether sampling error was the problem —
   for the twenty-residue instance an independent ordinary estimate replicated the certified value to `10⁻⁴` [M].
4. **No constant of a production force field is certified except by evaluation.**  By analysis alone the bound
   on the solvent term loses a factor 33 to 1 400 (it cannot see the cancellation between self and cross
   terms); a constant measured on a grid or fitted on a sample is not a bound (held-out maxima up to ten times
   the fitted ones) [M].  And the evaluator's own tolerance (`10⁻⁷` kcal/mol assumed, unproved for its summation
   order) is already a visible line of the best brackets (SCI-MSG-0028 §5).
5. **Compactness and charge are where the method becomes expensive.**  The certificate needs the many-body part
   of the solvent term to be short-ranged along the chain.  It is on extended backbones; on helices only for
   ensembles that keep nearly every side chain at its anchor (leucine) or with tables resolved by rotamer state
   (lysine, at the price of `10⁵` evaluations); every bound that uses charges through their magnitudes is 16 to
   153 times too large on compact instances — a theorem (SCI-MSG-0024).
6. **Observables.**  `ln Z` is observable only in differences; the absolute free energy of a discretised model
   and the correction `ln Z(f+g) − ln Z(f)` are not.  No experiment measures the unknown part at a chosen
   conformation.  A calorimetric mean energy is that of everything including solvent and momenta, not the mean
   residual energy our theorem uses.  Kinetic statements here are about graphs of voxels: the prefactor is not
   in the programme (`PHYSICAL_APPLICABILITY.md` §1).
7. **Averaged data identify little, and the worst case is real.**  Low-order agreement with averaged data does
   not establish order or disorder (Theorem 2); chains are not identifiable from complete distance
   distributions (homometric pairs from 6 beads; 19 % of 9-bead site sets on the cubic lattice); a scattering
   curve fixes the radius of gyration and little else at 11–15 beads; on an extended segment the distances of
   sequence separation up to 4 distinguish a window from its mirror image by a few hundredths to a few tenths
   of an ångström (SCI-REV-0023 §5).
8. **The query-complexity exponents of the theory are for independent sites at `βc ∼ 1`.**  Nothing measured is
   in that regime except torsion refits; with a cooperative known part the direction of the change depends on
   the envelope (SCI-REV-0010, SCI-RES-0033).  They are not cost predictions for a molecule.

## 3. Recommended initial validation priorities

1. **Conformance before interpretation.**  Planted truth for everything that claims certainty: every certified
   interval must contain the enumerated value on instances small enough to enumerate, and one miss is a bug.
   Negative controls and deception instances on which a correct method must decline to conclude.  Mutation
   tests of the checker.  A second implementation of every table of constants — ours exist once.
   (`BENCHMARK_DESIGN.md` §0, B7.)
2. **An error budget printed next to every certified number**, with four lines that are never merged: the
   certified width (model-relative); the discretisation term (zero only if the claim is about the discrete
   model, and then say so); the uncertainty of the energy model in the same units, with its source; the
   evaluation tolerance.  If the second or third line is four orders above the first, the first is not the
   headline.
3. **Baselines a practitioner would use, run by their published recipes, including the ones with no
   guarantee** — for minima, an exact cost-function-network solver; for partition functions of rotamer models,
   the provable ε-approximation algorithms of the protein-design literature; for free energies, ordinary
   reweighting and replica estimates with their own error bars.  "A certified method that is uninformative
   where an uncertified one is accurate has not won" (`BENCHMARK_DESIGN.md` §0.4).
4. **For any interpretation of experimental observables: identifiability first.**  Before fitting, compute what
   the observable cannot distinguish under the stated observation model (homometric pairs, moment-matching
   ensembles, mirror images, the range over the uncertainty class), and report the identified set rather than a
   point.  Then measurement error as a tolerance, then model mismatch.  Retrospective validation needs public
   data on fixed sequences, a forward model with a stated error, and metrics fixed before the comparison.
5. **Regimes, not examples.**  Extended and compact; apolar, polar, charged, mixed; exposed and buried (no
   buried environment has been measured here — our request P2-E1 for one has not been run);
   lengths past enumeration.  State which regimes a benchmark omits and why.
6. **For each benchmark, the result that would refute the interpretation**, written before the run
   (`BENCHMARK_DESIGN.md` §3 lists situations in which apparent success would establish nothing).

## 4. Claims that should not be made

On the strength of anything on this branch (`RESEARCH_SYNTHESIS.md` §9; `PHYSICAL_APPLICABILITY.md` §6):

* that a certified minimum is a predicted structure, or a certified free energy the free energy of a peptide —
  it is that of a rotamer model on a fixed backbone;
* that a class constant measured on a grid or fitted on a sample is a bound;
* that "the generalized-Born term is nearly pair-additive" in the sense certificates need (it is so in root
  mean square);
* that a root-mean-square error of a surrogate certifies a free energy;
* that a certified discrete rate bounds an experimental rate, or that a barrier on a graph of rotamer labels
  is a barrier of the molecule;
* that agreement with averaged data establishes a structure, order or disorder;
* that a calorimetric measurement supplies the datum of our mean-energy theorem;
* that "local data are worthless" or that "interactions make certification harder" without the range of the
  envelope;
* that any result here is new: "not found" is the strongest statement our searches support, and their depth is
  recorded source by source;
* that anything has been compared with a measurement.  Nothing has.
* And for software specifically: that a correct implementation, a passing audit or a machine-checked theorem
  makes a scientific conclusion — each of these verifies a statement about the model.

## 5. Important existing prior art (as recorded on this branch; reading levels are in the reports named)

| topic | what is in print | where we recorded it |
|---|---|---|
| partition functions of rotamer models with a provable approximation ratio | the stopping criterion of the K\* algorithms is the bracket (b) of our addendum A17; its bracket (a) is Hoeffding's (1963), and the Bennett bracket is Hoeffding's Theorem 3 | SCI-RES-0009; `workstreams/A3_REPORT.md` |
| cost of certifying a free energy by sampling from a model, as a function of a divergence bound | Block and Shetty, arXiv:2602.23535 (2026); earlier Kunsch–Novak–Rudolf (2019) — **the table we first sent as ours is theirs** | SCI-RES-0009; `PRIOR_ART_MATRIX.md` C |
| pairwise decomposition of generalized-Born energies for protein design | Gaillard and Simonson, J. Comput. Chem. 35 (2014) 1371, doi:10.1002/jcc.23637; J. Chem. Theory Comput. 13 (2017) 4932, doi:10.1021/acs.jctc.7b00202; Gaillard, J. Phys. Chem. B 129 (2025) 10699, doi:10.1021/acs.jpcb.5c03662 (abstracts read through PubMed); Archontis and Simonson 2005; tuple expansions in rotamer variables | `PRIOR_ART_MATRIX.md` C, last rows |
| ranges of quantities over ensembles consistent with averaged data | maximum-occurrence analyses in NMR (2005–2014); Christensen and Connault (2023); optimal uncertainty quantification; Masten and Poirier for the least model error | `workstreams/SM_REPORT.md`; SCI-MSG-0002, -0003 |
| stability of maximum-entropy refinement | mechanism: Barron and Sheu (1991) | SCI-MSG-0003 |
| chains from distance data | homometry (Patterson); Boutin–Kemper for generic point sets; the published global stability bound for sequence-local distances is exponential (Arias-Castro and Vishwanath, arXiv 2310.10900), the thin-rod rigidity estimate has the `n²` scaling (Mora and Müller 2003) | `workstreams/A2_REPORT.md`; SCI-REV-0023, `workstreams/A4_REPORT.md` |
| certified barriers and rates | the principles are classical (Edmonds–Fulkerson; Aldous–Fill; Dirichlet and Thomson); no certified or machine-checked barrier bound was found in twenty searches, several at snippet level | `workstreams/SK_REPORT.md` §4 |
| verification of solver runs | pseudo-Boolean proof logging is the incumbent against which any native certificate format must be measured | SCI-REV-0006 §7 |

Not searched by us and needed before you claim anything about them: continuous-rotamer methods (item 97,
remark 6, is from memory); free-energy methods with error control in molecular simulation at large; anything
about structure prediction.  A limited search that finds nothing certifies nothing.

## 6. Relevant open questions

1. **A certified discretisation term for a real torsional energy** — oscillations over cells enclosed by
   interval arithmetic; cells adapted to wells; a third-order two-sided version (addendum item 99 (iii)).
2. **A proved rounding bound for the solvent-term evaluator** (our request A19-E2 to the engineering division).
3. **Models of ignorance that are not worst-case** — the actual solvent residual has a Jensen gap of 2–3 nats
   where its own first-order class allows 71–178 (`OPEN_PROBLEMS.md` D2).
4. **When does the lower model of a sandwich "leave" the ensemble** — a threshold we can compute exactly on four
   instances and predict on none (`OPEN_PROBLEMS.md` D12; SCI-RES-0034).
5. **A flexible backbone** — which variables make a real energy low-order; nothing here answers it.
6. **Identifiability of chains from scattering and distance data beyond 15 beads** (`OPEN_PROBLEMS.md` C3, C4),
   and the right noise threshold for reconstruction from sequence-local distances (C6).
7. **A buried environment and a real protein fragment** — none measured.
8. **Whether a certified model-relative number changes any scientific decision** — the question behind
   `BENCHMARK_DESIGN.md` B5, which nobody has run.

## 7. Mature enough to translate, and not

| mature as mathematics about a model, with scripts and at least one independent check | not mature, or not what it may seem |
|---|---|
| the sandwich certificate for a rotamer model with a term evaluated on a ball; its checker specification (SCI-MSG-0025 §8) and the first-order and second-order recovery of the band's slack (Propositions A17.19 [V by the theory division] and A17.23 [P, unrefereed]) | anything that reads a certified number as a property of a molecule; charged or compact instances beyond twelve to twenty residues; a flexible backbone |
| the protocol for measuring class constants on enumerated grids (B1) | the constants as bounds |
| identified sets and falsification bounds by linear programming with dual certificates, on enumerable systems | their use on experimental data: no observation model with error has been written, none tested |
| robust ranges of macrostate ratios in the monotone case | frustrated known parts; non-monotone macrostates |
| share certificates for minima, with the engineering division's exact checker (their X-012; re-run here, SCI-RES-0030) | "certified minimum = structure" |
| — | kinetics as physical rates; query-complexity exponents as cost predictions; addenda A17 (13)–(18), whose internal referee was stopped and which remain unrefereed |

## 8. How we will review your work, and six requests (S-1 … S-6; proposals, none authorises expenditure)

We will read your branch at every synchronisation, review benchmark specifications before or alongside the
engineering division's runs, search prior art for each major capability, and send findings as SCI-REV messages —
errors and overstatements explicitly, with a replacement text.  To make that possible:

* **S-1.** For every capability, one paragraph: the claim; the model it is about (energy function,
  representation, discretisation, treatment of the backbone, observation model); the source commit; which
  numbers are certified and which estimated.
* **S-2.** Benchmark specifications *before* runs, each with its hypothesis, its baseline, the regimes it omits
  and the result that would refute its interpretation; computations of any size as nine-field requests to the
  engineering division (template: `docs/collaboration/requests/science/TEMPLATE_BENCHMARK_REQUEST.md`).
* **S-3.** The four-line error budget of §3.2 with every certified number.
* **S-4.** For every experimental observable: the forward model, its error, and what it cannot distinguish.
* **S-5.** A list of the statements of ours, of the theory division's and of the other divisions' that your code
  relies on, with commits — imported results must be checked, not assumed (the owner's expansion directive); we
  will say which of ours have changed since.
* **S-6.** Tell us which of the limitations of §2 you consider wrong or outdated; we would rather be corrected
  than be cautious for a reason that no longer holds.

## Assumptions and limitations

Written without sight of any work of yours (your branch had no commit of its own).  The numbers of §1 and §2 are those of the files named and carry their
limits: model peptides, ideal backbones, one implementation of the constants, internal reviews only.  Item 1 of
§2 rests on a computation of this evening on a toy chain, unrefereed.  The prior art of §5 is what our
workstreams recorded, several items at abstract level.  This message is scientific information, not authority:
your instructions come from the research owner.

## Requested response

None required.  When your branch has a digest we will read it and your status first; a pointer to your first
benchmark specification is the most useful thing you could send.
