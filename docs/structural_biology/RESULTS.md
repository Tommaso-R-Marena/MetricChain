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
conformation is not close to the deposited one: on ubiquitin it differs from the deposited
state at 37 of 65 residues and lies 139.1 kcal/mol below it in model energy (1PGA: 26 of 46,
37.9 kcal/mol below).  That is a property of an in-vacuo model with rigid rotamers, and it is
the reason nothing here is called a prediction.  (d) The re-run reproduces the instances bit
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

## R-5 — Synthetic instances: the producer is far slower than toulbar2 where couplings are frustrated (validation, in progress)

*Kind:* validation on synthetic models.  SB-X-002, `experiments/structbio/gmec_synth/run.py
--quick --time-limit 120`, commit `5c241bd`; rows in `experiments/structbio/gmec_synth/results.jsonl`
(the run was in progress when this was written; the table is completed in the next entry
of the research log).  First rows, "contact" generator (random couplings of standard deviation
4 units on a lattice contact graph inside a dense weak graph):

| n, kmax | seeds | outcome | certificate produced (s) | toulbar2 (s) | branch-and-bound nodes |
|---|---|---|---|---|---|
| 15, 6 | 0–2 | certified, zero gap, agrees with toulbar2 | 0.14–1.06 | 0.002–0.009 | 1–10 |
| 25, 8 | 0–1 | certified, zero gap, agrees with toulbar2 | 32–45 | 0.03–0.05 | 119–201 |

Reading.  Where strong couplings are random (frustrated), the plain pairwise dual bound is
loose and our depth-first search needs hundreds of nodes at 25 sites: 600 to 1 700 times
slower than toulbar2, whose bounds and heuristics are far stronger.  The real structures of
R-1 behave differently (one node, or four): there dead-end elimination and the dual bound
nearly close the problem.  Certified optimality at toulbar2's speed on hard instances would
need its search with proof logging, which does not exist (`PRIOR_ART.md` §B).

---

## Withdrawn or corrected statements

None yet.  Corrections will be entries here that name the statement, the commit that made it
and the commit that corrects it; the original text stays.
