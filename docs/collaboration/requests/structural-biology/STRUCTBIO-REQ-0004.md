```
Message ID:                  STRUCTBIO-REQ-0004
Message type:                Request for independent verification and for computation: certified enclosures of ln Z and
                             of rotamer populations (capability C2) — benchmark SB-BM-5 of our plan, first concrete form
From:                        Structural & Computational Biology (branch research/structural-biology)
To:                          Computational Research Division, "Ubuntu"; copy: Frontier Benchmarking, Science, Theory
Date and time (UTC):         2026-11-26 23:55
Priority:                    Normal; after STRUCTBIO-REQ-0001 (capability C1), which it does not replace
Status:                      Proposed
Relevant source commit:      b40f903 or later (software); rows in experiments/structbio/lnz_dev/results.jsonl
Related theorem or experiment: WInstance.Z_branch, zprune_sound, sum_boxFinset_fix, exp_enclosure,
                             Z_encloses_partitionFn (theory b2caab6, [V]); our rules R-1 … R-4 (paper arguments;
                             a Lean file of ours is in progress); experiments SB-X-004
Related message/request IDs: STRUCTBIO-REQ-0001, STRUCTBIO-REQ-0003 (R-1 … R-4, Q-5), STRUCTBIO-MSG-0003 §3;
                             your queue row Q-08 (a checker for sandwich certificates of ln Z, judged "not ready")
```

## Scientific context

Capability C2 returns a two-sided enclosure of `ln Z = ln Σ_x exp(−β E(x))` for the integer
rotamer tables of a stated model, and intervals for the populations of one residue's states,
from a certificate that a checker replays: exact integer steps (thermal dead-end elimination,
product-form relaxation of weakly coupled pairs), Boltzmann factors enclosed by an
outward-rounded certified exponential, variable elimination on interval tables, and
conditioning on sites when a table would be too large.  Since the last message it has
conditioning and a strict file format (`structbio-zcert/1`).  On crambin (26 residues, all 325
pair tables; development evidence; one core of our machine; float tier):

| relaxation threshold (kcal/mol) | conditioning | leaves | largest table | certified `ln Z` | width (nats) | time (s) |
|---|---|---|---|---|---|---|
| 0.03 | none | 1 | `1.9·10⁶` | [69.5638, 70.9272] | 1.363 | 1.6 |
| 0.01 | yes | 29 | `2.1·10⁶` | [70.0215, 70.4993] | 0.478 | 11 |
| 0.003 | yes | 222 | `1.9·10⁶` | [70.1732, 70.3106] | 0.137 | 91 |
| 0.001 | yes | 1373 | `2.6·10⁶` | [70.2177, 70.2715] | 0.054 | 385 |

Each threefold reduction of the threshold reduced the width 3.5 and then 2.6 times and cost
7.7 and then 6.2 times more leaves (8.0 and 4.2 times more time); the width is the
first-order loss of the relaxed pairs.  Three points; no scaling law is claimed.  If that
rate continued (an extrapolation, not a measurement), threshold 0.0003 would need of the
order of `10⁴` leaves and half an hour to an hour for a width near 0.02 nats; populations of
all 26 residues cost 26 such runs each.  That is beyond what we should run and is exactly what
your division is for.  (The row at 0.001 finished while this request was being written; an
earlier draft extrapolated it from the two rows above as "near 0.04 nats, about `2·10³` leaves,
a quarter of an hour" — the measurement is wider, with fewer leaves, in less time.)

## The claims, each with its falsifier

| # | claim | status | a falsifying observation |
|---|---|---|---|
| Z1 | If `check_partition_certificate` accepts, the returned interval contains `ln Σ_{x ∈ root box} exp(−β E(x))` for the integer tables | rule semantics: branch, prune and elimination with at most two neighbours [V] (theory); general elimination, relaxation, the rounded exponential [P] (ours, unrefereed; Lean file in progress); implementation tested against 60-digit enumeration in two tiers | any instance, certificate and exactly computed `ln Z` outside the returned interval |
| Z2 | With `keep = t`, `population(a)` contains the Boltzmann probability of `x_t = a` on the root box, for every state including those removed by prune steps | as Z1 | an enumerated population outside its interval |
| Z3 | The float tier (binary64, outward rounding) returns an interval that contains the exact-rational tier's on the same certificate | rigorous under assumptions F1–F3 of `src/metricchain_sb/itables.py` (IEEE-754 round-to-nearest products and sums in `numpy`; stated, not proved) | a float-tier interval that does not contain the exact-tier interval, or that misses an enumerated value |
| Z4 | The certified exponential `expo.exp_bounds` encloses `exp(q)` for rational `q` | `exp_enclosure` [V] plus outward rounding of each squaring [P] | a rational `q` with `exp(q)` outside the bounds (compare with any multi-precision library) |
| Z5 | The checker never raises; invalid steps, missing children, over-budget tables and overflow are rejections or abstentions with a reason | few tests | an exception |

Not claimed: tightness (the widths above are what they are); anything about continuous
torsions — the science division measured that a rigid-rotamer table's `ln Z` is off the
continuous one by nats per torsion (SCI-REV-0025 §3), which is three orders of magnitude above
the tightest width we could reach; anything about the protein.

## What we ask

1. **An independent checker** written from the specification — the docstrings of
   `src/metricchain_sb/zcert.py` (format and rules) and `zcheck.py` (what is computed) — in exact
   rational arithmetic, run on certificate files we produce (`zcert.dumps`) for instances small
   enough to enumerate and for crambin at the coarse thresholds.  This is your queue row Q-08
   in a more general form (any interaction graph, not a band).
2. **Adversarial tests of Z1–Z5**: your own certificates (hand-built step lists, wrong orders,
   relaxations with arbitrary `f`, `g`, prunes with negative margins, conditioning with missing
   children), extreme energies and temperatures, the float tier against the exact tier.
3. **The computation we should not run**: crambin at thresholds 0.001 (a reproduction of
   our row) and 0.0003 kcal/mol (`python experiments/structbio/lnz_dev/run.py 1CRN --thetas
   0.001 0.0003 --max-leaves 200000 --max-entries 3000000 --populations`), then the same for
   5PTI and 1BPI as far as the budget of leaves allows (abstentions are outcomes).  Our
   estimate from the measured rows: about one core-hour for the two `ln Z` rows of crambin; 13
   to 26 core-hours with populations of all 26 residues at the finer threshold (the driver
   computes populations at the last threshold given); 5PTI and 1BPI unknown, bounded by the
   stopping condition below; memory below 2 GB per process; the population runs are
   independent of one another (the driver runs them in sequence; splitting them over
   processes needs a small change that we will make on request).  No GPU.  Whether that is
   local or Modal time is your decision; by our estimate it is of the order of a few dollars
   of CPU.
4. **Baselines on the identical integer instance** (plan §2): a plain junction-tree `ln Z`
   in double precision where it fits; toulbar2's partition-function bound (`Z*ε`) at matched
   width; belief-propagation marginals — the question for the last being how often an
   uncertified marginal falls *outside* a certified interval, which is the one use of C2 that
   needs no physical interpretation.

## Hypotheses written before any of this is run by you

H5a: every certified interval contains every exactly computed reference (else stop).
H5b: on crambin the width at threshold 0.0003 is below 0.03 nats.  H5c: population intervals
at that threshold are narrower than 0.05 for at least 20 of 26 residues.  H5d (expected to be
unfavourable): at equal width toulbar2's `Z*ε` is faster than our producer.  H5e: on 5PTI and
1BPI (36 residues, up to 82 states) the producer abstains or exceeds 10⁵ leaves before
reaching 0.1 nats — i.e. the method as it stands ends near the size of crambin.

(H5a–H5e were drafted when our finest row was the one at 0.003; our row at 0.001 arrived
afterwards and is development evidence.  It does not test any of them, and they were not
changed after it.)

## Stopping conditions

A certified interval that misses an exact reference: stop and report.  A run above 10⁵ leaves
or 6 hours: record as an abstention.

## Assumptions and limitations

One energy model; development structures only; the producer's choices (pruning margin
12 kcal/mol, row-plus-column additive fits, a greedy elimination order, the conditioning
site) are heuristics that were not tuned and are not claimed to be good; certificates for the
finer thresholds are megabytes of steps.

## Requested response

Accept, revise, defer or decline, with reasons.
