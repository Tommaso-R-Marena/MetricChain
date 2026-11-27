# Results of the Structural & Computational Biology division

Every entry names its kind of evidence (exploratory / development / validation / held-out /
adversarial / replication), its label, its commit and how to reproduce it.  Unfavourable
results are entries like any other.  Nothing here is a statement about a protein: every
certified number is a property of published integer tables (label [M]).

Labels: [V] machine-checked in Lean (declaration named); [CK] accepted by an exact checker whose
rule semantics are [V] and whose implementation is tested; [N] numerical evidence; [E] timing
or size observed on a named machine; [H] uncertified estimate.  The session machine is a
4-core x86-64 virtual machine with 15 GB of memory, Python 3.13, numpy 2.5.5.

---

## R-1 — Certified global minima on six public structures (development evidence)

*Kind:* development (the six structures were used while the software was written).
*Experiment:* SB-X-001, `experiments/structbio/gmec_dev/run.py`, software commit `c128625`,
rows and certificates at `c3aa6f9`.  *Reproduce:* `python experiments/structbio/gmec_dev/run.py --check`.

**Read with R-8 and R-9 (added 2026-11-27).**  This table is on **model v1 with seed 0**.  The
tables of v1 depend on the seed of its hydrogen placement by tens of kcal/mol (R-8), so each
number below is a property of the seed-0 tables and of nothing more general; the same
experiment on the deterministic model v2 is R-9.  The six structures are **four proteins**:
5PTI and 1BPI are the same protein (bovine pancreatic trypsin inhibitor, identical 58-residue
sequences, two crystal forms), and 1PGA and 2IGD are two immunoglobulin-binding domains of
streptococcal protein G with 51 of 56 residues identical (sequences read from the SEQRES
records of the files).

| PDB | flexible sites | states | pair tables | certified minimum (kcal/mol) [CK] | certified gap | tables (s) | toulbar2 (s) | certificate produced (s) | checked (s) | eliminations / leaves / branchings | certificate (bytes) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1CRN | 26 | 380 | 325 | −36.476240 | 0 | 1.0 | 0.013 | 0.33 | 0.04 | 344 / 1 / 0 | 38 154 |
| 5PTI | 36 | 1 152 | 630 | −130.228328 | 0 | 8.9 | 0.26 | 2.2 | 0.24 | 1 076 / 1 / 0 | 131 152 |
| 1BPI | 36 | 1 152 | 630 | −138.259854 | 0 | 8.4 | 0.27 | 1.9 | 0.25 | 1 089 / 1 / 0 | 126 948 |
| 1PGA | 46 | 967 | 1 035 | −13.874580 | 0 | 4.6 | 0.50 | 4.7 | 0.18 | 823 / 1 / 0 | 179 063 |
| 2IGD | 49 | 1 027 | 1 176 | −38.123699 | 0 | 5.0 | 0.25 | 4.5 | 0.24 | 861 / 1 / 0 | 208 986 |
| 1UBQ | 65 | 1 763 | 2 080 | −88.695941 | 0 | 14.7 | 1.85 | 24.4 | 0.72 | 1 280 / 3 / 1 | 1 730 543 |

(Minima are shown rounded to six decimals; the exact rationals are in `results.jsonl`.  Times
[E], one core.)

What it shows.  (1) For this model on these structures the exact global minimum can be
certified: every certificate is accepted by the independent checker and the witness energy
equals the certified bound.  (2) The uncertified exact solver toulbar2 returns the same
optimum on the identical integer instance in every case.  (3) Checking costs 3 to 13 % of
production.

What it does not show, and what is unfavourable.  (a) toulbar2 is 7 to 25 times faster than
our producer on every structure, and on none of them does the certificate change the answer.
(b) These are development instances; no held-out structure has been run.  (c) The certified
configuration is not the deposited one: on ubiquitin it uses a library state rather than the
deposited state at 37 of 65 sites and lies 139.1 kcal/mol below the deposited configuration in
model energy (1PGA: 26 of 46 sites, 37.9 kcal/mol below).  *(Wording corrected 2026-11-27,
correction RC-1 below: the count is of sites whose chosen state is a library state; a library
state can lie a few degrees from the deposited conformation, and how many of these sites are in
another rotamer well was not counted on v1.  On v2 it is counted: R-9.)*  That is a property of
an in-vacuo model with rigid rotamers, and it is the reason nothing here is called a prediction.  (d) The re-run reproduces the instances bit
for bit on the same machine; other machines are untested.

Four-line error budget.  (i) Certified width 0 (integer tables).  (ii) Discretisation: not
quantified.  (iii) Energy model: at least 1.1–4.4 `kT` per residue between refits of one
force-field lineage (science division, SCI-MSG-0034 §2.3); larger for a vacuum model.
(iv) Evaluation: tables agree with an independent OpenMM system to `≤ 4·10⁻¹¹` kcal/mol on
low-energy configurations (R-4); rounding to `2⁻²⁰` kcal/mol moves a configuration's energy by
at most `1.0·10⁻³` kcal/mol on ubiquitin.

## R-2 — The checker agrees with the theory division's reference checker (validation, tiny instances)

*Kind:* validation/adversarial on enumerable instances.  `tests/structbio/test_mincert.py`,
commit `c128625`.  24 random instances (2–6 sites, 2–4 states): zero-gap certificates equal the
enumerated minimum in all 24 [CK + enumeration]; of 288 randomly mutated certificates, 275 are
expressible in `metricchain-cert/1` and both checkers give the same verdict on every one (49
accepted, 226 rejected), 13 are malformed in our format and rejected by ours; every accepted
bound is at most the enumerated minimum.  A count, not a proof: with zero disagreements in 275
trials the exact 95 % upper limit on the disagreement rate is about 1.1 %.

## R-3 — Why certified partition functions are hard on these instances (exploratory)

*Kind:* exploratory (a throwaway script; reproduced by SB-X-003 when capability C2 exists).
Model as in R-1, `RT = 0.593` kcal/mol.  Thermal dead-end elimination with margin 12 kcal/mol
(sum of `e^{−margin/RT}` over eliminations: `7.6·10⁻¹⁰` for crambin, `6.9·10⁻⁹` for
ubiquitin), then for each pair the residual of a row-plus-column additive fit on the
surviving states.

| structure | states left (min / median / max per site) | pairs with residual oscillation > 1 / > 0.1 / > 0.01 / > 0.001 kcal/mol | threshold θ (kcal/mol) | pairs kept exact | first-order loss of the rest (nats) | width of the min-fill order | largest table |
|---|---|---|---|---|---|---|---|
| 1CRN | 147 (1 / 4 / 20) | 21 / 40 / 90 / 146 of 325 | 1.0 | 21 | 13.8 | 3 | `8.6·10³` |
| | | | 0.1 | 40 | 3.4 | 4 | `1.9·10⁵` |
| | | | 0.03 | 59 | 1.36 | 5 | `1.9·10⁶` |
| | | | 0.01 | 90 | 0.45 | 9 | `1.3·10⁹` |
| | | | 0.001 | 146 | 0.048 | 11 | `2.1·10¹⁰` |
| 1UBQ | 756 (2 / 7 / 55) | 165 / 327 / 837 / 1 401 of 2 080 | 1.0 | 165 | 113 | 10 | `8.6·10¹²` |
| | | | 0.1 | 327 | 34.8 | 22 | beyond `10¹⁸` |
| | | | 0.01 | 837 | 4.0 | 35 | beyond `10¹⁸` |

Reading.  On crambin an enclosure of `ln Z` of width 1.4 nats is within reach of exact
elimination on this machine, and 0.05 nats would need tables of `2·10¹⁰` entries.  On
ubiquitin nothing useful is: the strong pairs alone need a table of `10¹³` entries, and the
weak pairs are worth tens of nats at first order.  The widths are those of one heuristic
order (upper bounds on the treewidth); the additive fit is not the best sup-norm fit; one
pruning margin was tried.  Requests that follow from this: STRUCTBIO-REQ-0003 (R-1 … R-4,
Q-5).  [N, exploratory.]

## R-4 — The tables are the stated energy function (validation, numerical)

*Kind:* validation.  `tests/structbio/test_molecular.py`; details in
`intake/MOLECULAR_LAYER_REPORT.md` §3.  For six structures, 21 random and 21 low-energy
configurations each: energy differences from the all-native configuration computed from the
tables and from an independently assembled OpenMM system agree to `≤ 3.6·10⁻¹¹` kcal/mol
(low-energy) and `≤ 4.6·10⁻¹³` relative (random, energies up to `6·10²⁰` kcal/mol because of
clashes).  A wrong dielectric constant (8 instead of 4) or omitted 1–4 terms is detected
(1.95 and 4.79 kcal/mol).  [N]: agreement in double precision; no enclosure of the
floating-point error of a table entry exists.

## R-5 — Synthetic instances: the producer is far slower than toulbar2 where couplings are frustrated, and hypothesis H2b fails (validation)

*Kind:* validation on synthetic models.  SB-X-002, `experiments/structbio/gmec_synth/run.py
--quick --time-limit 120`, commit `5c241bd`; rows in `experiments/structbio/gmec_synth/results.jsonl`
(the run was in progress when this was written; the table is completed in the next entry
of the research log).  First rows, "contact" generator (random couplings of standard deviation
4 units on a lattice contact graph inside a dense weak graph):

| n, kmax | seeds | outcome | certificate produced (s) | toulbar2 (s) | branch-and-bound nodes |
|---|---|---|---|---|---|
| 15, 6 | 0–2 | certified, zero gap, agrees with toulbar2 | 0.14–1.06 | 0.002–0.009 | 1–10 |
| 25, 8 | 0–2 | certified, zero gap, agrees with toulbar2 | 32–45 | 0.03–0.05 | 119–201 |
| 40, 8 | 0–2 | **abstained** at the 120 s limit (both accuracies) | > 120 | 0.6–6.7 | — |
| 60, 10 | 0 (others pending) | **abstained** at the 120 s limit | > 120 | 194 | — |

*Hypothesis check.*  H2b of the benchmark plan ("on contact models up to `n = 60`, `kmax = 12`
at least 90 % are certified within 600 s") was written before this run; at a 120 s limit the
certified fraction is 0 of 3 at `n = 40`.  The limit differs from the hypothesis' 600 s, but
the growth from 25 to 40 sites (hundreds of nodes at 25) leaves little doubt: **H2b is
expected to fail**, and the full run of SB-BM-2 should settle it.  These synthetic instances
are also much harder for toulbar2 than the real ones (194 s at 60 sites against 1.9 s for
ubiquitin's 65), i.e. the generator is more frustrated than the proteins it was meant to
resemble (noted as a bias of SB-BM-2).

Reading.  Where strong couplings are random (frustrated), the plain pairwise dual bound is
loose and our depth-first search needs hundreds of nodes at 25 sites: 600 to 1 700 times
slower than toulbar2, whose bounds and heuristics are far stronger.  The real structures of
R-1 behave differently (one node, or four): there dead-end elimination and the dual bound
nearly close the problem.  Certified optimality at toulbar2's speed on hard instances would
need its search with proof logging, for which we found no implementation (bounded searches,
2026-11-26; `PRIOR_ART.md` §B).  *(Corrected 2026-11-27, RC-2: the earlier text said "which does
not exist"; four bounded searches by four divisions do not establish that.)*

## R-6 — Certified per-residue flip gaps: the certified minimum is unique, survives rounding, and is thermally negligible (development evidence)

*Kind:* development.  *Experiment:* SB-X-003, `experiments/structbio/flipgaps_dev/run.py`, commit
`263dd18`; one zero-gap certificate per residue on the box without that residue's state in the
minimiser (label [CK] each; [M]).  *Reproduce:* `python experiments/structbio/flipgaps_dev/run.py --check 1CRN`.

| PDB | residues | gap to the second-best configuration (kcal/mol) | rounding margin (kcal/mol) | minimiser of the float tables too | residues with gap < `RT` | < `3RT` | wall time, 4 processes (s) |
|---|---|---|---|---|---|---|---|
| 1CRN | 26 | 0.0451 | 0.00017 | yes | 14 | 21 | 4 |
| 5PTI | 36 | 0.0243 | 0.00032 | yes | 21 | 28 | 29 |
| 1BPI | 36 | 0.1102 | 0.00032 | yes | 10 | 22 | 28 |
| 1PGA | 46 | 0.0068 | 0.00052 | yes | 20 | 36 | 73 |
| 2IGD | 49 | 0.0039 | 0.00058 | yes | 26 | 33 | 80 |
| 1UBQ | 65 | 0.0050 | 0.00102 | yes | 26 | 47 | 621 |

`RT = 0.593` kcal/mol.  Crambin, per residue (largest gaps): Tyr29 55.8, Tyr44 18.3, Arg17 6.5,
Arg10 3.3, Ile35 3.1 kcal/mol; the fourteen smallest are below 0.6 (hydroxyl rotamers of Thr and
Ser lowest: 0.045, 0.057).  Ubiquitin: Lys27 14.8, Leu67 10.7, Leu15 7.3, Phe45 6.9, Tyr59 6.0,
Leu71 5.0 — the residues the model pins down are those of its hydrophobic core and its buried
lysine; the three smallest gaps are 0.005 to 0.017 (Thr55, Val5, Thr12).  The largest search
for one ubiquitin gap took 52 branch-and-bound nodes and 91 s.

What it shows.  (1) Uniqueness of the minimiser, certified.  (2) Robustness to rounding: the
gap exceeds twice the rounding margin in every structure, so the minimiser of the integer
tables is the unique minimiser of the float tables as well (a corollary tested in
`tests/structbio/test_stability.py`).  (3) The unfavourable part, and the scientifically
relevant one: the gap to the second-best configuration is a few hundredths of a kcal/mol or
less, and 61 to 81 % of the residues can change state for less than `3RT` (ubiquitin: 72 %).  The certified
global minimum of this model is one configuration among very many of nearly equal energy; it
is not a description of the model's ensemble, let alone of the protein.  These are the first
numbers here that the exact solver's answer does not already contain; an uncertified solver
could compute the same values by restricted solves, without a checkable proof.

## R-7 — A first certified enclosure of ln Z on a deposited structure, and where it stops (development evidence)

*Kind:* development.  *Experiment:* SB-X-004, `experiments/structbio/lnz_dev/run.py 1CRN
--exact-check`, commit `2976042`; rows in `experiments/structbio/lnz_dev/results.jsonl`.  Label [CP]
(rule semantics [V] for chains, paper argument beyond; checker implementation tested against
60-digit enumeration in two arithmetic tiers).  Crambin, 26 residues, all 325 pair tables,
`β = 1000/593` per kcal/mol, thermal pruning margin 12 kcal/mol (233 eliminations, total loss
below `10⁻⁹` nats):

| relaxation threshold (kcal/mol) | pairs kept exact | largest table | certified `ln Z` (float tier) | width (nats) | time (s) |
|---|---|---|---|---|---|
| 1.0 | 21 | `8.6·10³` | [63.1425, 76.9461] | 13.80 | 0.4 |
| 0.3 | 29 | `7.8·10⁴` | [66.8176, 73.3317] | 6.51 | 0.4 |
| 0.1 | 40 | `1.9·10⁵` | [68.4694, 71.8347] | 3.37 | 0.7 |
| 0.03 | 59 | `1.9·10⁶` | [69.5638, 70.9272] | 1.36 | 1.6 |
| 0.01 | — | `1.3·10⁹` needed | abstained (budget `3·10⁷` entries) | — | — |

With conditioning (branch nodes; software at `e82010b`; table budget `3·10⁶` entries):

| relaxation threshold (kcal/mol) | leaves | largest table | certified `ln Z` (float tier) | width (nats) | time (s) |
|---|---|---|---|---|---|
| 0.01 | 29 | `2.1·10⁶` | [70.0215, 70.4993] | 0.478 | 11 |
| 0.003 | 222 | `1.9·10⁶` | [70.1732, 70.3106] | 0.137 | 91 |
| 0.001 | 1373 | `2.6·10⁶` | [70.2177, 70.2715] | 0.054 | 385 |

(The three rows come from one process started at 23:39 UTC with `src` as at `e82010b`; the
`commit` field of a row is the head at the moment the row was started — `e82010b`, `e82010b`,
`11498f4` — and `src` is identical at those commits.  That a row could record a commit later
than the code in memory is defect SB-DEF-08, corrected in the driver.  Tighter thresholds and
populations of all residues: requested from the engineering division, STRUCTBIO-REQ-0004.)

Exact-rational tier at threshold 1.0: [63.14249423974886, 76.94606796481926] in 9.4 s — inside
the float tier's [63.14249423974757, 76.94606796482172].  `−β E(x*) = 61.51`.

What it shows.  The pipeline from a deposited structure to a checked two-sided bound on a
partition function runs, and its two arithmetic tiers agree.  What is unfavourable: without
conditioning the enclosure is 1.36 nats wide at the last affordable threshold — entirely
first-order loss of the 266 relaxed pairs; with conditioning, each threefold reduction of
the threshold reduced the width 3.5 and then 2.6 times and cost 7.7 and then 6.2 times more
leaves (8.0 and 4.2 times more time) — three points; no scaling law is claimed.  At that rate
populations to a few per cent for all residues are tens of core-hours even for crambin;
ubiquitin is out of reach (R-3).  No baseline has been run: toulbar2's
`Z*ε` and the K\*-family algorithms give floating-point `ε`-brackets without certificates on
such instances, and we have not compared widths or times with them.

## R-8 — The tables of model v1 depend on a random seed by tens of kcal/mol (development measurement asked for by the science division)

*Kind:* development measurement, not a benchmark.  *Experiment:* SB-X-005,
`experiments/structbio/seed_dev/run.py`; the reading and our prediction were committed in
`0544ff4` before the first run; 60 seed rows and 6 summaries in
`experiments/structbio/seed_dev/results.jsonl` (code as at `0544ff4`).  *Origin:* SCI-REV-0026,
finding F1 — model v1 places hydrogens with OpenMM's `addHydrogens`, which starts them at random
positions and runs at most 50 minimiser iterations; `seed = 0` made that reproducible, not
meaningful.  For each structure the tables were built with seeds 0 to 9 and the minimum of each
integer table was certified (zero gap, full box) and compared with toulbar2.

| PDB | sites | certified minimum over the ten seeds (kcal/mol) | range | sites whose certified state differs from seed 0 (largest over seeds) | sites whose state is not the same for all ten seeds | other seeds' minimisers, evaluated in the seed-0 table, above its minimum (largest) | spread of one-body entries over seeds: median / 90 % / 99 % | spread of pair entries: median / 99 % |
|---|---|---|---|---|---|---|---|---|
| 1CRN | 26 | −52.14 … −36.48 | 15.7 | 4 (15.4 %) | 6 | 3.0 | 4.1 / 50 / 437 | 0.0043 / 7.6 |
| 5PTI | 36 | −133.68 … −111.34 | 22.3 | 2 (5.6 %) | 5 | 1.1 | 1.4 / 16 / 303 | 0.0011 / 0.41 |
| 1BPI | 36 | −143.42 … −129.45 | 14.0 | 5 (13.9 %) | 6 | 5.1 | 2.9 / 61 / 346 | 0.0015 / 0.63 |
| 1PGA | 46 | −26.63 … −13.87 | 12.8 | 5 (10.9 %) | 7 | 4.2 | 1.6 / 32 / 259 | 0.0006 / 0.86 |
| 2IGD | 49 | −56.70 … −38.12 | 18.6 | 2 (4.1 %) | 7 | 0.6 | 1.6 / 25 / 245 | 0.0005 / 0.50 |
| 1UBQ | 65 | −93.02 … −68.47 | 24.6 | 6 (9.2 %) | 13 | 7.9 | 1.9 / 46 / 455 | 0.0009 / 0.55 |

(Energies in kcal/mol; spreads are max − min over the ten seeds of one table entry, over the
entries that are clipped for no seed.)  All 60 instances were certified with zero gap, toulbar2
returned the same optimum on each, and no minimiser uses a clipped entry.

**Reading, as committed beforehand.**  "Material if in any structure some seed changes the
certified state at more than 5 % of the sites or the certified minimum ranges over more than
1 kcal/mol."  The range criterion is met in all six structures (12.8 to 24.6 kcal/mol) and the
site criterion in five.  Our prediction (more than 5 % of sites in at least four structures;
more than 10 kcal/mol in at least four) was met: five and six.

**What it shows.**  The science division's finding F1 is confirmed on our own instances: the
seed of model v1 is a model parameter whose effect on table entries is tens of kcal/mol —
a certified minimum of a v1 table is a certified property of one draw.  Two details that
qualify it without rescuing it: (1) the *identity* of the minimiser moves less than its
*value* — the other seeds' minimisers cost at most 0.6 to 7.9 kcal/mol in the seed-0 table —
because much of the spread sits in entries that good configurations share; (2) pair entries
are affected far less than one-body entries (median spread below 0.005 kcal/mol).

**Consequences, as committed beforehand.**  (i) R-1, R-6 and R-7 are statements about the
seed-0 tables of v1 and are labelled so.  (ii) No held-out run will be made on v1.
(iii) Hydrogen placement became a deterministic function of the heavy atoms under a new model
name, v2 (`src/metricchain_sb/molecular/hydrogens.py`; its tables are identical for every seed —
tested), and development results and hypotheses are formed again on v2 (R-9, R-10).

## R-9 — Model v2 (deterministic hydrogens): certified minima with and without the deposited state (development evidence)

*Kind:* development.  *Experiment:* SB-X-001 with `--model v2` and `--model v2-lib`
(`experiments/structbio/gmec_dev/run.py`), software `87082ef`; rows in `gmec_dev/results.jsonl`
(field `model`), certificates under `gmec_dev/certs/v2/` and `certs/v2-lib/`.  Label [CK].
Model v2: hydrogens by the geometric rule of `molecular/hydrogens.py` (force-field equilibrium
bond lengths and angles, staggered methyl and ammonium groups, hydroxyl hydrogens anti; nothing
random, no minimiser); everything else as v1.  `v2` has the deposited state plus the library
at every site; `v2-lib` has library states only (SCI-REV-0026, F2).  Our expectations E1–E5 were
written in the commit message of `87082ef`, before any v2 table was certified.

| PDB | sites | `v2`: certified minimum (kcal/mol) | deposited configuration | sites at a library state | sites in another rotamer well than deposited | produce / check / toulbar2 (s) | `v2-lib`: certified minimum | sites in another well than deposited | produce / check / toulbar2 (s) |
|---|---|---|---|---|---|---|---|---|---|
| 1CRN | 26 | −42.4936 | −31.6 | 8 | 3 | 0.3 / 0.03 / 0.01 | 12.0977 | 5 | 0.3 / 0.03 / 0.01 |
| 5PTI | 36 | −121.3447 | −67.9 | 19 | 11 | 1.6 / 0.19 / 0.25 | 118.8744 | 19 | 1.8 / 0.19 / 0.24 |
| 1BPI | 36 | −123.7356 | 217.6 | 12 | 6 | 2.3 / 0.18 / 0.26 | 397.9441 | 17 | 2.1 / 0.17 / 0.26 |
| 1PGA | 46 | 4.5137 | 77.9 | 30 | 14 | 3.6 / 0.18 / 0.28 | 855.1930 | 23 | 3.1 / 0.15 / 0.22 |
| 2IGD | 49 | −21.7985 | −10.2 | 15 | 5 | 5.7 / 0.68 / 0.22 | 198.2204 | 17 | 3.3 / 0.17 / 0.24 |
| 1UBQ | 65 | −76.0937 | 658.3 | 41 | 28 | 45.4 / 2.44 / 1.68 | −1.7768 | 35 | 19.8 / 1.68 / 0.99 |

All twelve certificates have zero gap over the full state set and are accepted by the checker;
toulbar2 returns the same optimum on each identical integer instance; **no certified minimiser
uses a clipped entry**, so each is also the minimum of the unclipped integer table (clipping
only lowers entries: the check the science division asked to see with each row).  A rotamer
well is, per χ, the nearest library value (`molecular/rotamers.py`, `well_of`).

**Expectations against outcome.**  E1 (v2 certifies within ten minutes; v2-lib not on all six):
first half met, second half **wrong** — all six library-only instances certify, ubiquitin
faster than with the deposited state.  E2 (toulbar2 agrees), E3 (no clipped entry used): met.
E4 (the v2 minimum lies less far below the deposited configuration than under v1): **wrong** —
the distances are 10.8, 53.5, 341.4, 73.4, 11.6 and 734.4 kcal/mol (v1: 2.3, 32.1, 24.0, 37.9,
11.6, 139.1).  E5 (more than half of the sites keep the deposited well under v2): met (12 to
43 % of sites change well).

**Why E4 failed — a property of v2 that must be written next to its results.**  The energy of
the deposited configuration is dominated by single residues: ubiquitin's Arg72 has a one-body
entry of 534.5 kcal/mol (an ideal `HG3` 1.48 Å from the residue's own carbonyl oxygen,
`HD2`–`HH11` at 1.51 Å, `HB2`–`HE` at 1.52 Å: the deposited side chain is folded on itself) and
Glu7 of 1BPI 334.8 kcal/mol (`HG3` 1.53 Å from the carbonyl oxygen of Phe4; the residue is
deposited with two alternate conformations of occupancy 0.53 and 0.47, and the first is used).
Under v1 the 50 minimiser iterations had moved those hydrogens away (entries 29.0 and 26.1) —
which is exactly the science division's point F2 (d): in v1 the hydrogens were relaxed around
the deposited conformation, an advantage that no library state received.  v2 does not have
that bias and does not have that relief: ideal hydrogens on a strained deposited side chain
clash, and the model then prefers a library state there.

**What it shows.**  (1) Cost: certification stays cheap in all three variants (at most 45 s to
produce, 2.5 s to check); toulbar2 is 6 to 27 times faster than our producer on v2.  (2) F2 (b):
removing the deposited state did not make these six instances harder for either solver; the
hypotheses formed with the deposited state present are not contradicted by the variant without
it — on development structures only.  (3) Library-only minima are strained by hundreds of
kcal/mol (+12 to +855 where `v2` has −124 to +4.5) and put 19 to 54 % of the sites in another
well than the deposited conformation: the idealised library, rotated rigidly against an
unsoftened repulsive wall, as the science division's F5 expects.  That is development evidence
for the expected failure of SB-BM-6 and says nothing about certificates.  (4) Under v2 polar
hydrogens still do not look for partners (F3 stands); a variant with hydroxyl torsions as states
is open problem SB-OP-13.

<!-- R10-13-BEGIN (tables generated from the result rows by a script; regenerate rather than edit) -->
## R-10 — Leaving a rotamer well costs kcal/mol where leaving a state costs tenths; an entrywise table error of 0.01 kcal/mol already defeats optimality (development evidence, model v2)

*Kind:* development.  *Experiment:* SB-X-006, `experiments/structbio/wellgaps_dev/run.py`
(software `41fa668`; expectations H6a–H6d written in that commit, before any run); rows in
`wellgaps_dev/results.jsonl`.  Every number is a certified minimum of a restricted box or of a
shifted table ([CK]); the two constructions are the science division's (SCI-REV-0026 §0, §4).
Energies in kcal/mol; `RT` = 0.593.  Ubiquitin was not run (about 300 certified minimisations
of about 45 s each; not started because of the consolidation directive of 2026-11-27).

*Does the certified minimiser minimise every table whose entries lie within `b` of ours?*
("no (m; k)": a certified counterexample exists whose worst-scenario energy is `m` below the
minimiser's, with `k` sites in another well.)

| PDB | sites | b = one unit (9.5·10⁻⁷) | b = 0.001 | b = 0.01 | b = 0.1 |
|---|---|---|---|---|---|
| 1CRN | 26 | yes | yes | no (-1.71; 0) | no (-51.86; 3) |
| 5PTI | 36 | yes | no (-0.10; 0) | no (-7.20; 6) | no (-111.70; 14) |
| 1BPI | 36 | yes | no (-0.11; 1) | no (-4.54; 4) | no (-100.72; 12) |
| 1PGA | 46 | yes | no (-0.10; 0) | no (-9.30; 8) | no (-181.83; 18) |
| 2IGD | — | yes | no (-0.53; 3) | no (-14.90; 5) | no (-215.33; 9) |
| 1UBQ | — | not run | not run | not run | not run |

*Gaps at `b = 0`, and the number of sites whose well is kept by every minimiser of every table
within `b`* (a sufficient condition: comparison against the minimiser alone):

| PDB | sites | state gap: smallest / median | well gap: smallest / median | sites with well gap below RT / 3RT | wells kept in every table within b = 0.001 / 0.01 / 0.1 |
|---|---|---|---|---|---|
| 1CRN | 26 | 0.0589 / 0.80 | 0.569 / 4.74 | 1 / 6 | 26 / 20 / 6 |
| 5PTI | 36 | 0.0343 / 0.50 | 0.096 / 3.78 | 9 / 16 | 35 / 11 / 4 |
| 1BPI | 36 | 0.0023 / 1.39 | 0.033 / 4.99 | 6 / 10 | 33 / 18 / 5 |
| 1PGA | 46 | 0.0438 / 0.80 | 0.096 / 3.28 | 6 / 18 | 44 / 14 / 3 |
| 2IGD | — | not run or not finished | | | |
| 1UBQ | — | not run or not finished | | | |

No gap certificate abstained or was rejected (0 of the rows).

**Expectations against outcome.**  H6a (necessarily optimal at one table unit everywhere):
met on the five structures run.  H6b (nowhere at 0.01): met.  H6c (at 0.01 at least half of
the sites of every structure keep their well; at 0.1 fewer than half): first half **wrong**
for 5PTI and 1PGA, second half met.  H6d (median well gap above `RT` — met, 3.3 to 5.0 — while
the median state gap is below it): second half **wrong** except for 5PTI.

**What it shows.**  (1) The reading the science division proposed is borne out: the model
determines *wells* much more firmly than *states* — the median cost of leaving a well is 3.3
to 5.0 kcal/mol where the median cost of leaving a state is 0.5 to 1.4 — yet 1 to 9 sites per
structure can change well for less than `RT`.  (2) With one table unit of error (which covers
the rounding of the tables and the observed evaluation error) the certified minimiser is the
minimiser of every such table: the sentence "the published model is the rounded tables" is no
longer needed for these five instances — under an evaluation-error bound that is observed, not
proved.  (3) At `b = 0.01` kcal/mol per entry no minimiser survives and a third to a half of
the wells are no longer certified; at 0.1 almost none.  A realistic force-field error is
orders of magnitude larger.  **The certified minimiser is the minimiser of the published
integers and of nothing near them** (the science division's sentence; DEAD_ENDS SB-D-E-09).

## R-11 — On the weighted library-only table of model v2, crambin's `ln Z` is enclosed to 0.0075 nats and every residue's rotamer populations to 0.024 (development evidence)

*Kind:* development.  *Experiment:* SB-X-004 with the default `--model v2-lib` (software
`d61fc53`/`7722963`; expectations H7a–H7c written in the driver before the first run).  The
object: `Z_w = Σ_x Π_i w_i(x_i) exp(−β E(x))` over library states only, each state weighted by
its share of the residue's torsion space; `−ln Z_w / β` is a free energy relative to
non-interacting free rotors — of this table, in vacuo, with rigid idealised rotamers.
`β = 1000/593` per kcal/mol; pruning margin 12 kcal/mol.  Label [CK] (float tier: under F1–F3).

| threshold (kcal/mol) | tier | leaves | largest table | certified `ln Z_w` | width (nats) | time (s) |
|---|---|---|---|---|---|---|
| 1 | exact | 1 | `4.8e+03` | [-77.8219, -65.6855] | 12.1364 | 6.4 |
| 1 | float | 1 | `4.8e+03` | [-77.8219, -65.6855] | 12.1364 | 0.5 |
| 0.3 | float | 1 | `3.9e+04` | [-73.5510, -68.7337] | 4.8173 | 0.6 |
| 0.1 | float | 1 | `1.2e+05` | [-72.3708, -69.8253] | 2.5455 | 0.7 |
| 0.03 | float | 1 | `1.2e+05` | [-71.6339, -70.6393] | 0.9945 | 0.8 |
| 0.01 | float | 19 | `3.5e+05` | [-71.3082, -70.9936] | 0.3145 | 2.8 |
| 0.003 | float | 29 | `7.3e+05` | [-71.1844, -71.1253] | 0.0590 | 7.0 |
| 0.001 | float | 29 | `2.2e+06` | [-71.1649, -71.1408] | 0.0241 | 18.0 |
| 0.0003 | float | 145 | `2.8e+06` | [-71.1574, -71.1499] | 0.0075 | 64.8 |

(Threshold 0.0001 did not finish in the 417 s left to that command.)  The exact tier's
interval at threshold 1 lies inside the float tier's.  H7a (width below 1 nat at 0.01 and
below 0.3 at 0.003) and H7b are met; H7c: 118 of 354 states survive pruning (model v1: 147 of
380).  The library-only table is far cheaper than v1's (0.059 nats in 7 s against 0.137 nats
in 91 s) because its strained states are pruned.

**Certified populations, threshold 0.001, all 26 residues** (26 certificates,
782 s in total on one core; interval widths 0.020 to 0.024):

| residue | most populated state: certified population | deposited well: certified population | residue | most populated state | deposited well |
|---|---|---|---|---|---|
| Thr1 | [0.976, 1.000] | [0.976, 1.000] | Thr2 | [0.977, 1.000] | [0.000, 0.023] |
| Ser6 | [0.939, 0.961] | [0.939, 0.961] | Ile7 | [0.977, 0.998] | [0.977, 0.998] |
| Val8 | [0.979, 1.000] | [0.979, 1.000] | Arg10 | [0.978, 1.000] | [0.978, 1.000] |
| Ser11 | [0.905, 0.927] | [0.073, 0.095] | Asn12 | [0.970, 0.991] | [0.970, 0.991] |
| Phe13 | [0.977, 1.000] | [0.977, 1.000] | Asn14 | [0.837, 0.859] | [0.837, 0.859] |
| Val15 | [0.976, 1.000] | [0.976, 1.000] | Arg17 | [0.789, 0.812] | [0.000, 0.000] |
| Leu18 | [0.875, 0.895] | [0.875, 0.895] | Thr21 | [0.976, 1.000] | [0.976, 1.000] |
| Glu23 | [0.452, 0.474] | [0.452, 0.474] | Ile25 | [0.979, 0.999] | [0.001, 0.021] |
| Thr28 | [0.813, 0.834] | [0.813, 0.834] | Tyr29 | [0.976, 1.000] | [0.976, 1.000] |
| Thr30 | [0.976, 1.000] | [0.976, 1.000] | Ile33 | [0.979, 1.000] | [0.979, 1.000] |
| Ile34 | [0.979, 1.000] | [0.979, 1.000] | Ile35 | [0.976, 1.000] | [0.976, 1.000] |
| Thr39 | [0.980, 1.000] | [0.980, 1.000] | Asp43 | [0.648, 0.669] | [0.014, 0.036] |
| Tyr44 | [0.976, 1.000] | [0.976, 1.000] | Asn46 | [0.858, 0.879] | [0.858, 0.879] |

25 of 26 residues have one state whose population is certified above 0.5; for 20 of 26 the
deposited rotamer well is certified above 0.5; for four (Thr2, Arg17, Ile25, Asp43) the
deposited well is certified below 0.05.  **What this is:** the first complete table of
guaranteed population intervals this project has for a deposited structure — a property of
the weighted table of a vacuum model with rigid ideal rotamers.  **What it is not:** a
statement about crambin; the science division measured that a rigid-rotamer table misplaces
populations by up to 0.48 in total variation against continuous torsions of the same energy
(SCI-REV-0025 §3), twenty times the width certified here.  Known weakness of the interval
itself: its width is the same for every state (about `1 − exp(−w)`); a ratio bound that uses
per-state upper ends would shrink it to about `2w·p(1−p)` (not implemented; HANDOFF).

## R-12 — The null method: on every development instance the dual bound alone certifies the exact minimum (development evidence)

*Kind:* development; baseline asked for by the Frontier division (FRONTIER-MSG-0001 §4 (a)) and
the science division (SCI-REV-0026 §7.2).  *Experiment:* SB-X-007,
`experiments/structbio/nullmethod_dev/run.py` (software `7722963`; expectation written there
before the run: exact for at least four of six structures in each variant).  A certificate
that is **one leaf on the full box** — the exact dual bound of the pairwise relaxation, no
dead-end elimination, no search — checked by the same checker.

| PDB | sites | `v2`: one leaf certifies the exact minimum? (s) | `v2-lib` (s) |
|---|---|---|---|
| 1CRN | 26 | yes (0.3) | yes (0.4) |
| 5PTI | 36 | yes (2.0) | yes (3.2) |
| 1BPI | 36 | yes (3.5) | yes (2.0) |
| 1PGA | 46 | yes (3.8) | yes (4.0) |
| 2IGD | 49 | yes (9.1) | yes (4.4) |
| 1UBQ | 65 | yes (35.9) | yes (26.9) |

**What it shows, plainly.**  The basic linear relaxation is tight on all twelve development
instances (integrality gap zero: the number the Complexity division asked for).  On these
instances the eliminations and the search of our producer are unnecessary, and a certificate
is, in substance, one exact dual solution of a linear programme — established technology, as
the Frontier division's negative result N-5 says.  This agrees with Yanover, Schueler-Furman
and Weiss (2008): a relaxation found the optimum for about 85 % of a standard side-chain set.
It does not extend to larger instances: on the ten public instances of the Frontier pilot
(337 to 1 972 residues; their exploratory run of our software at `1756529`) the four
certificates contained 0, 1, 2 and 39 branch nodes and six runs abstained within 300 s.

## R-13 — Which regime the instances are in: the quantity that matters is `max_i β c_i`, and no threshold makes both parts tractable beyond crambin (exploratory measurement)

*Kind:* exploratory; asked for by the Complexity division (COMPLEXITY-RES-0010).
*Experiment:* SB-X-008, `experiments/structbio/regime_dev/run.py` (software `627a860`).
Weighted library-only tables of v2 after thermal pruning (margin 12 kcal/mol); a pair is
"weak" at a threshold if the oscillation `o_e` of its non-additive part is at most the
threshold; `c_i` is the sum of `o_e` over the weak pairs at site `i`.  The last-but-one column
is `(β²/8) Σ_i c_i²`: what a site-wise second-order bound would give **at best** (product
reference, unit influence) — an indicator; nothing of the kind is implemented or certified.

| PDB | sites | states after pruning (before) | threshold | weak / exact pairs | `β Σ o_e` (nats) | `max_i β c_i` | site-wise second-order indicator (nats) | largest table of the exact part (log₁₀ entries) |
|---|---|---|---|---|---|---|---|---|
| 1CRN | 26 | 118 (354) | 1 | 309 / 16 | 12.14 | 5.83 | 7.983 | 3.7 |
| 1CRN | 26 | 118 (354) | 0.1 | 294 / 31 | 2.55 | 0.55 | 0.219 | 5.1 |
| 1CRN | 26 | 118 (354) | 0.01 | 254 / 71 | 0.30 | 0.08 | 0.003 | 7.7 |
| 5PTI | 36 | 321 (1116) | 1 | 571 / 59 | 39.07 | 8.55 | 35.889 | 5.1 |
| 5PTI | 36 | 321 (1116) | 0.1 | 524 / 106 | 10.88 | 1.27 | 2.203 | 10.0 |
| 5PTI | 36 | 321 (1116) | 0.01 | 366 / 264 | 1.09 | 0.14 | 0.021 | 17.3 |
| 1BPI | 36 | 330 (1116) | 1 | 567 / 63 | 46.66 | 9.32 | 50.309 | 4.9 |
| 1BPI | 36 | 330 (1116) | 0.1 | 505 / 125 | 11.31 | 1.32 | 2.219 | 9.8 |
| 1BPI | 36 | 330 (1116) | 0.01 | 326 / 304 | 1.01 | 0.12 | 0.019 | 19.9 |
| 1PGA | 46 | 345 (921) | 1 | 961 / 74 | 68.10 | 7.13 | 70.114 | 4.1 |
| 1PGA | 46 | 345 (921) | 0.1 | 870 / 165 | 19.21 | 1.58 | 4.835 | 12.6 |
| 1PGA | 46 | 345 (921) | 0.01 | 577 / 458 | 2.28 | 0.17 | 0.067 | 22.4 |
| 2IGD | 49 | 380 (978) | 1 | 1108 / 68 | 59.22 | 7.04 | 53.406 | 6.1 |
| 2IGD | 49 | 380 (978) | 0.1 | 1019 / 157 | 15.98 | 1.70 | 3.656 | 12.5 |
| 2IGD | 49 | 380 (978) | 0.01 | 787 / 389 | 2.47 | 0.17 | 0.079 | 21.8 |
| 1UBQ | 65 | 684 (1698) | 1 | 1926 / 154 | 110.21 | 10.56 | 131.120 | 12.0 |
| 1UBQ | 65 | 684 (1698) | 0.1 | 1768 / 312 | 33.55 | 2.25 | 10.615 | 24.1 |
| 1UBQ | 65 | 684 (1698) | 0.01 | 1283 / 797 | 3.86 | 0.20 | 0.129 | 37.6 |

**Reading.**  (1) The first-order width our relaxation loses is `β Σ o_e`; a second-order
bound could replace it by something like the indicator only where `max_i β c_i` is below one
— on these tables at thresholds of 0.1 kcal/mol or less.  There the indicator is 5 to 30
times smaller than the first-order width.  (2) But at those thresholds the *exact* part needs
elimination tables of `10¹⁰` to `10³⁸` entries for everything larger than crambin.  For
ubiquitin there is no threshold at which the exact part is tractable and the weak part small:
at 1 kcal/mol the exact part needs `10¹²` entries and the weak part loses 110 nats at first
order and no less at second (`max β c_i` = 10.6).  (3) So the obstruction to certified
partition functions of whole proteins under this dense vacuum model is the width of the
strongly coupled part, not the order of the bound on the weak part (the Complexity division's
Theorem 2 says which regime no certificate format can reach).  A model with a cutoff or
screened electrostatics would have a sparser strong graph; that is a different model
(SB-OP-11) and was not tried.

<!-- R10-13-END -->

---

## Withdrawn or corrected statements

Corrections are entries here that name the statement, where it was made and what replaces it.
In living documents the text is replaced with a dated note beside it; in messages, which are
historical, the body stays and a status line points to the correcting message
(STRUCTBIO-MSG-0004).

| # | statement, and where it was made | what was wrong | replacement | origin |
|---|---|---|---|---|
| RC-1 | "it differs from the deposited state at 37 of 65 residues" (R-1 (c); PHYSICAL_APPLICABILITY §3; STRUCTBIO-MSG-0001; STRUCTBIO-RES-0001; plan SB-BM-6) | the driver counted sites whose chosen *state* is a library state; a library state can lie a few degrees from the deposited conformation | "uses a library state rather than the deposited one at 37 of 65 sites (how many lie in another rotamer well was not counted)"; on v2 the count of other-well sites is recorded with every row | SCI-REV-0026 §1 |
| RC-2 | "…proof logging, which does not exist" (R-5) | bounded searches certify nothing | "for which we found no implementation (bounded searches, 2026-11-26)" | SCI-REV-0026 §1 |
| RC-3 | "the certificate removes search error from a model-relative statement and nothing else"; "Line (iii) is five to six orders of magnitude above line (i)" (PHYSICAL_APPLICABILITY §2; ARCHITECTURE §3; STRUCTBIO-MSG-0001) | no search error was exhibited (toulbar2 found every optimum); line (i) is zero, so there is no ratio | "the certificate replaces trust in an exact solver's implementation by trust in a checker, and changes no number here"; "line (iii) is at least three orders of magnitude above the rounding bound of line (iv) and ten above its observed agreement; line (i) is zero" | SCI-REV-0026 §1 |
| RC-4 | every number of R-1, R-6, R-7 read as a property of "the model" | model v1 contains a seed whose effect on its tables is tens of kcal/mol (R-8) | each is a property of the seed-0 tables of v1; the deterministic model v2 replaces v1 for all further work (R-9, R-10) | SCI-REV-0026 F1; SB-X-005 |
| RC-5 | "six structures" as six independent cases (R-1 and elsewhere) | they are four proteins | stated in R-1 | SCI-REV-0026 §2 |
| RC-6 | "`ln Z` exceeds the minimiser's exponent by 8.1 to 9.4 nats" read as entropy of the ensemble (STRUCTBIO-MSG-0003 §3; R-7 gives `−βE(x*)` next to `ln Z`) | the sum runs over a state set with the deposited conformation as an extra state and unequal numbers of library points per well, so part of the excess is a count of library points | for C2 the state set is library-only with stated shares of torsion space (`rotamers.state_share`); R-7 stands as a statement about the v1 table only | SCI-REV-0026 §0, F2 (c) |
| RC-7 | header times of STRUCTBIO-RES-0001 (23:45), -RES-0002 (23:48) and -REQ-0004 (23:55) | written as estimates; the commits that contain them are earlier (23:39:58 and 23:52:35 UTC) — a time later than its commit was not read from the clock | header times are now read from `date -u` immediately before the commit; the three headers carry a note | SCI-REV-0026 §10; DEAD_ENDS SB-DEF-09 |
