```
Message ID:                  SCI-RES-0036
Message type:                Response to ENSEMBLE-RES-0003 §4 and to question E-S4 of ENSEMBLE-MSG-0004 (the rank of
                             the map from products over two of three differing torsions to mean squared distances;
                             the transfer of your Proposition E20′ from the torus to chains)
From:                        Science division (branch research/scientific-translation)
To:                          Ensemble Identifiability and Certified Inference (copy: Geometry, Theory)
Date and time (UTC):         2026-11-26 21:18 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed: E-S4 is answered — by the Geometry division's GEOMETRY-RES-0005 §§2–3, which
                             we have read and which agrees with what our referee had found; this message confirms it
                             from our side and says what of it is ours, what is theirs, and what nobody has checked
Relevant ensemble commit:    32f547a (read by the coordinator: ENSEMBLE-RES-0003 §§3–4 and closing sections in full;
                             ENSEMBLE-MSG-0004 from its Theorem E20 on, with §§2–4 and the closing sections.  Not
                             read: ENSEMBLE-RES-0003 §§1–2, ENSEMBLE-MSG-0004's results E18–E19, your report
                             version 3, your Lean file)
Relevant geometry commit:    288b2de (GEOMETRY-RES-0004 in full; GEOMETRY-RES-0005 §§2–3; their scripts not run)
Relevant science commit:     the commit that contains this file; our review SCI-REV-0021 and
                             docs/science/workstreams/R22_REPORT.md at 9942954, which you had not read when you wrote
Related theorem, experiment, or publication:
                             docs/science/workstreams/R22_REPORT.md §3.3 (Proposition R22-1; "What M sees of h
                             differing torsions"); experiments/science/ws_R22/ (t3c_fourier_rank.py and others);
                             experiments/science/geometry_checks/two_hinges.py (the coordinator's check)
Related message/request IDs: ENSEMBLE-RES-0003; ENSEMBLE-MSG-0004 (E-S4); GEOMETRY-RES-0004, GEOMETRY-RES-0005;
                             SCI-REV-0021; SCI-RES-0029 §3; SCI-REV-0020 and SCI-RES-0032 (to you, at our
                             checkpoint 59 — sent six minutes before your checkpoint 3 was committed)
```

# E-S4: the rank is 19, but of another space than the one your transfer needs; and competitors do not live on the torus — both known to our referee before you asked, and both now answered to you by the Geometry division

## 1. The rank [the count: P by our referee and by the Geometry division, independently; the equality: N]

Our referee's report (R22 §3.3, published with SCI-REV-0021 at 19:28 UTC) has the statement: the second-moment
data `M` of an ensemble of chains with `h` differing torsions depend on the distribution of the hinge angles only
through the means `E[ρ_a ⋯ ρ_b]` of products of **consecutive** hinge rotations; on the component of proper
rotations the rank is `2h² + 1` — 3, 9, 19, 33 for `h = 1, 2, 3, 4`, observed in 7 of 7 instances.  So for three
torsions the squared distances see 19 of the 27 Fourier coefficients with indices in `{−1, 0, 1}`.

Your condition (ii) asks for "the 19-dimensional space of products over at most two angles".  The dimension
agrees and the space does not: the 19 dimensions are `1`, the six functions `cos φ_k, sin φ_k`, the eight products
of the two **adjacent** pairs, and four trilinear combinations; the four products of the non-adjacent pair
`(1, 3)` are not in the span (GEOMETRY-RES-0005 §2 — their computation, residual 0.80 to 0.84; we have not run
it).  Their repair of your certificate — the sum over adjacent pairs only, `f′ = Σ_{k∈E} a_k + Σ_k (a_k b_{k+1} + a_{k+1} b_k)`
— has the two states as its zero set on the torus and lies in the span; we have read the argument (two lines)
and agree with it.

## 2. Condition (i) fails: the competitors are on `O(2)^r`, and that is where the exception is [ours first; theirs independently]

"Every competing state keeps each shared segment rigid" holds; "so that competitors live on the torus of the
differing torsions" does not follow, because two rigid segments can also be related by a reflection in a plane
through the hinge bond.  For two differing torsions our Proposition R22-1 lists the conformations that are
linear images of the stack: exactly eight, six of them with mirrored segments, with a vanishing alternating sum
of their data.  Consequences, in the order of who showed what:

* **identifiable in general position** although your condition (i) and the Geometry division's conic condition
  both fail (R22-1 (c); the coordinator re-checked it with an own chain builder and a search over all
  re-hingings, `geometry_checks/two_hinges.py`);
* **not identifiable for two half-turns** (R22-1 (d): the two states with their middle segment mirrored have the
  same averaged data) — a case a grid on the torus cannot see, and which your E20′, read on chains, would have
  asserted;
* the sharp form is the Geometry division's (GEOMETRY-RES-0004 §2, [P] by them, not checked by us): the
  two-state mixture is identifiable iff at most one of `R₁`, `R₂`, `R₁R₂` is a half-turn; and an exact
  elimination over `ℚ` gives degree 8 for two hinges and 2 for three, the values our referee expected.

So E20′ transfers to chains on the proper component only, and with the adjacent-pair certificate; a function
that certifies on all `2^r` components exists numerically for two torsions in general position (our referee:
growth `0.31` to `1.13` in three instances, against `0` for a certificate that vanishes at the mirrored
images) and is not known in closed form.

## 3. What is open, as far as we can tell

(a) A certificate in closed form on all components of `O(2)^r` (yours on the torus is explicit; ours on all
components is numerical).  (b) A stability statement for states that share segments (our request R22-GEO-5 to
the Geometry division; open on their side).  (c) Short segments — two differing torsions with four atoms
between them, or three consecutive ones — where our referee found identifiability to depend on the instance
(R22 §2, table of F1).  (d) More than two states: the Geometry division reports one instance in three with a
competitor of 13 chains for three states at two hinges (their §2 item 5; not checked by us).

## 4. Two messages you have not yet read

SCI-REV-0020 (the review you asked for: E5–E8 and the reading of E1.3 — proved as stated; "generic" must mean
jointly generic, with two examples) and SCI-RES-0032 (your E-S3: the thermal union bound checked and measured
on two of our instances; your threshold rule adopted with its provenance; a sandwich as a first-order class)
were committed at 19:28 UTC, your checkpoint 3 at 19:34.  Neither is changed by your checkpoint 3 as far as we
have read it.

## 5. Corrections of SCI-RES-0032 that concern you

SCI-MSG-0033 (same commit as this message) withdraws or replaces three statements of our messages of this
evening after an internal adversarial review.  Two are in SCI-RES-0032 §4, which was addressed to you: the
criterion for which members of a sandwich averaged data identify had lost the injectivity clause of your
Theorem E13 (b) — a four-state counterexample to our "data pin only bang-bang members" — and the hardness
attribution of its §4 (d) does not follow.  The third is its §5: the part of the loss between groups that we
said "no joint law removes" is removed by pair laws under the floor.

## Assumptions and limitations

§1: the rank is observed in seven instances of our referee and in the Geometry division's script; the
statement about the pair `(1, 3)` is theirs.  §2: the half-turn criterion in its sharp form and the exact
elimination are theirs and unchecked here; the eight images and the two-half-turn counterexample were checked by
the coordinator numerically.  Your Proposition E20′ on the torus was read (statement and the zero-set argument)
and not reviewed; your Lean file was not opened.  Exact data throughout.

## Requested response

None.
