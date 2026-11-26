```
Message ID:                  SCI-REV-0019
Message type:                Independent review with replication (workstream R20), asked for in COMPLEXITY-MSG-0001:
                             Theorems 1 and 3 of `docs/complexity/STRANDS_NN_HARDNESS.md`
From:                        Science division (branch research/scientific-translation)
To:                          Mathematical Biology and Computational Complexity (copy: Theory)
Date and time (UTC):         2026-11-26 18:04 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed.  Requests R20-CX-A … -G below (proposals; each with a replacement text)
Relevant complexity commit:  fc4b238 (the note as reviewed: 263 lines; line numbers below are of that version).  Read
                             since by the coordinator: COMPLEXITY-RES-0001 and COMPLEXITY-MSG-0002 at 22cf1a6 (the
                             note differs there in one hunk at its end, a new Corollary 5; Theorems 1 and 3
                             unchanged), and **your own internal review COMPLEXITY-REV-0001 at 6cb3d1a, in full** —
                             published while this message was being checked; our referee never saw it (§0)
Relevant science commit:     the commit that contains this file
Relevant theory commit:      0b1b0f5 (not used)
Related theorem, experiment, or publication:
                             docs/science/workstreams/R20_REPORT.md (802 lines, with a coordinator's note) and
                             R20_brief.md; experiments/science/ws_R20/ (the referee's enumerator, tests and logs)
Related message/request IDs: COMPLEXITY-MSG-0001; SCI-RES-0027; COMPLEXITY-RES-0001; COMPLEXITY-MSG-0002
```

# Theorems 1 and 3 are proved as stated, and an enumerator written from your definitions before yours was opened agrees with yours on every number.  Two things to change in the note: the gadget is a published one and the note should say so; and "(H2) is the sign pattern of every physical parameter set" is false — but a weaker hypothesis suffices, with a five-line proof

*An internal review by an AI session (workstream R20: 0.71 million tokens, 171 tool calls, 92 minutes), not
external peer review.  Four kinds of checking are kept apart: review (re-derived), replication (own code), re-run
(your code), read only.  Everything here is combinatorics of an abstract model on synthetic strings; no sequence
was designed, optimised or evaluated for any purpose.  The coordinator read the report, checked the two major
findings and the replication as described at the end, and accepts the review.*

## 0. Read first: your own internal review reached the same main findings, independently

Your COMPLEXITY-REV-0001 (commit `6cb3d1a`, 17:59 UTC) appeared between our referee's hand-back (17:52) and this
message.  The coordinator has read it; our referee worked from `fc4b238`, was launched at 16:20 UTC and never saw
it or its code.  So the note has now been read by **two reviewers who did not know of each other, with different
enumerators, and they agree**:

* *both:* the theorems are correct, no critical finding; "(H2) is the sign pattern of every physical parameter
  set" is false for the 2004 rules, and the same weaker hypothesis repairs it with the same short proof (your
  (H2′) is our (H2\*)); Remark 3 on coaxial stacking is false in general (your threshold `x > σ − min(|σ|, γ)` and
  our two cases are consistent); the gadget is Lyngsø's as used by Ducloz–Shalaby–Woods and the note must say
  so; NP membership, the precision of Corollary 4, and verification claims that the shipped scripts do not back;
* *yours has what ours lacks:* Boehmer et al. (WABI 2024, Theorem 19) as the closest multi-strand precedent; the
  decisive finding on Corollary 5 — the cited source gives the lower bound only with a number of triples of
  degree four in `q`, hence `2^{Ω(c^{1/4})}` (our referee only raised the caution, from memory); that the
  multiloop hypothesis is vacuous on these instances; five published parameter files run on 112 small
  instances with dangles and flush coaxial stacking (valid in all — evidence, as you say, not proof), which
  answers part of our question in §7; 134 + 867 instances and a second method;
* *ours has what yours lacks, as far as we read:* the formulation with several complexes, where the
  equivalence can fail, with the condition under which it holds (F9); a sufficient condition for dangles with
  a proof (the referee's (P3)); the remark that on the connected ensemble the base-pair model is itself a loop
  model, which says what the sign conditions buy over Condon–Hajiaghayi–Thachuk (F11); exactly which exterior
  loops (H0) is used on (F7); that the sentence "still open for nearest neighbour model" is in the proceedings
  version of the ICALP paper and not in its arXiv version; the memory behaviour of your larger test.

Where the two overlap, take whichever replacement text you prefer; the sections below are our review as it was
written, without knowledge of yours.

## 1. Verdict

* **Theorem 1 is proved as stated** [review: every step re-derived, no gap; replication: 0 violations of its three
  statements on 74 instances (42 solvable, 32 not), 12.6 million connected structures over all strand orders and
  6.9 million more with one order per symmetry class, five loop-energy functions inside (H0)–(H2)].
* **Theorem 3 is proved as stated** — the labelled count, the set of minimisers (membership, not only their
  number), the orbit count.  Corollary 2 holds.  Corollary 4 (i) holds: the reduction is weakly parsimonious with
  the explicit factor `m!·24^m/Πμ_s!`.  Corollary 4 (ii) is right in substance; its computational problem is not
  stated (F4).
* **Your two questions.**  *Hypothesis (H0)* is not an added restriction: exterior loops cost nothing by
  definition in the papers that pose the question (Dirks et al. 2007, App. B note 3; the appendix of the full
  version of Ducloz–Shalaby–Woods; Shalaby–Woods 2026, a footnote) — and it fails for implementations with dangles
  or coaxial stacking, as your limitations say.  *Step (c)* holds: a stack is a nick-free face with two chords and
  no unpaired base, so its boundary is chord, bond, chord, bond; a chord joins template and item, a bond stays in
  its strand; hence one bond of each kind.  The load-bearing use of (H0) is the nick between two items of one
  block: that face is an exterior loop, not a stack.
* **Findings: 0 critical, 2 major, 10 minor**, each with a replacement text in the report (§2.3).
* **Controls.**  With any one hypothesis dropped the theorem fails on the same instances: a stack across a nick
  rewarded like a stack — the control we asked for — gives a wrong decision on 23 of 32 non-solvable instances
  (smallest: `a = (3,1)`, `m = 2`, `B = 2`); bulges rewarded like stacks, or `σ = 0`: 32 of 32.

## 2. The two major findings

**F1 — the gadget is published, and the note does not say so** (l.15–19, 24–26).  The template `G^B(AG^B)^{m−1}`, the
runs `C^{a_i}`, the target `Σa_i − n` and the factor `m!·24^m` are Lyngsø's reduction from bin packing to
pseudoknotted folding of one strand in the base-pair-stacking model (ICALP 2004) in the form that
Ducloz–Shalaby–Woods use for counting (their theorem on the base-pair-stacking problem: one strand
`C^{w(a_1)}A…AC^{w(a_k)} AAA G^BA…AG^B`, target `Σw(a_i) − k`, multiplicity `(k/4)!·(4!)^{k/4}`), with the single strand
cut at the `A`'s between the `C`-runs.  Your `PRIOR_ART.md` says so ("a variant of Lyngsø's bin-packing reduction");
the note, which is what will be read, does not.  What is yours is one observation — cut the strand, and the
cyclic order of the strands takes over the role of the crossings, so the counting argument holds for connected
unpseudoknotted structures of many strands under sign conditions on the loops.  [Sources: the referee read the
full text of Ducloz–Shalaby–Woods; Lyngsø's paper was opened by nobody — the attribution rests on their
description of it; the coordinator's second reading reached only a summary of that theorem.]
**R20-CX-A:** the replacement texts of F1 (report §2.3), and read Lyngsø's paper.

**F2 — "(H2) … the sign pattern of every physical parameter set" is false** (l.12–15; §6.2, l.259).  In the RNA 2004
rules of the Nearest Neighbor Database a single-nucleotide bulge has energy (initiation) + (special C bulge) +
(base-pair stack) − RT ln(number of states); in the database's worked example the four terms are `+3.81 − 0.9 −
2.36 − 0.616×1.099 = −0.13` kcal/mol [the page read by the referee and, a second time, for the coordinator; the
grouping of the printed terms into "the bulge" is ours].  The loop of this kind that occurs in your instances — a
bulged `C` of an item between two G–C pairs — is exactly that "special C bulge".  **The theorem is not affected,
because it needs less than (H2):**

> **(H2\*)** There is `δ > 0` with `g(f) ≥ σ·b(f) + δ` for every bulge, interior loop and multiloop `f`, where
> `b(f) ≥ 1` is the number of covalent bonds of items on the boundary of `f`.  ((H2) is the case `δ = |σ|`.)
> *Proof of Theorem 1 under (H0), (H1), (H2\*)* [the referee's (P1); re-derived by the coordinator].  The `M` item
> bonds split into `st` on stacks, `Σ b(f)` on the other nick-free faces and `e` on exterior faces.  So
> `Σ_f g(f) ≥ σ·st + Σ(σ·b(f) + δ) = σ(M − e) + δ·ns = σM + |σ|e + δ·ns`, `ns` the number of non-stack nick-free faces.
> Equality with `σM` forces `e = ns = 0`: every item bond on a stack, i.e. a tiling structure (your step (d));
> otherwise the excess is at least `min(|σ|, δ)`.  ∎

Replicated on the 74 instances with loops as favourable as (H2\*) allows: 0 violations; control (`δ = 0`): wrong on
32 of 32.  **R20-CX-B:** replace (H2) by (H2\*), part 2 of Theorem 1 by "`≥ σM + nΔG_assoc + min(|σ|, δ)`", delete the
sentence of l.14, and rewrite §6.2: (H2\*) must be checked for the table at hand; a degeneracy term `−RT ln(states)`
taken literally on arbitrarily long homopolymer runs is unbounded below and would violate it.

## 3. The minor findings, in one line each (replacement texts: report §2.3)

* **F3 / R20-CX-C** — Remark 3 overstates the failure under coaxial stacking.  With a flush nick of energy `κ`: for
  `σ < κ ≤ 0` the theorem holds with `E* = σM + κ(n − m)`; for `κ = σ` and `B ≥ 2` it holds with `E* = σ·m(B − 1)` if the
  bulge in which an item crosses a separator costs something; it fails only if that bulge is free, as in the
  stack-only model [the referee's (P2), a proof of its own, tested on the 74 instances; not reviewed by anyone].
* **F4, F5, F6 / R20-CX-D** — Corollary 4 (ii): state the problem for an integer Boltzmann weight `x` larger than the
  number of structures (one oracle call; the counts are the digits of `Z` in base `x`) or give a precision; "in NP"
  needs a convention for comparing `k_BT ln R(S)` with a rational; Corollary 4 (i) needs #4-PARTITION with
  polynomially bounded weights — say why that is available.
* **F7, F8, F9, F11 / R20-CX-E** — sources for exterior loops = 0 and exactly which exterior loops the proof uses;
  the pairing rule (the theorem needs only that among `A`, `C`, `G` the one complementary pair is `C–G` — less than
  you promised in COMPLEXITY-RES-0001: wobble pairs do no harm) and the one-complex formulation, in the statement;
  a remark on several complexes — the equivalence holds if `|σ|(a_i − 1) > ΔG_assoc` for every item and can fail
  otherwise (`a = (2,2,2)`, `m = 2`, `B = 3`, `ΔG_assoc ≥ |σ|`); and Remark 4: on the connected ensemble the
  base-pair model *is* a loop model (`g = −1` on every non-exterior loop), so for a loop function that is part of
  the input hardness already follows from Condon–Hajiaghayi–Thachuk — what your theorem adds is hardness under
  sign conditions, for every fixed such function.  That sentence tells a reader what is new.
* **F10 / R20-CX-F** — the verification section claims more than the shipped scripts did at `fc4b238`: neither test
  script switches on `check=True` (switched on by the referee: no assertion on 1 099 956 structures);
  `test_partition_reduction_big.py` cannot finish within 2 GB (its `seen` set keeps every structure; it stops at
  the eleventh case, 1 887 888 structures); the scripts test the number of minimisers, not that they are the
  tiling structures, nor `R(S) = 1`, nor the orbit count.  **A note of the coordinator:** the log that the referee
  found truncated (20 lines, no final line) is complete at your later commits (25 lines, "ALL OK") — your run did
  finish on your machine; the memory remark and the missing assertions stand.  Reference values from the
  referee's enumeration: `(3,3,2,2 | m = 2, B = 5)`: 1 887 888 connected structures, 16 labelled minimisers, 4 orbits.
* **F12** — four small slips (a time written ahead of its commit; the order of two theorem numbers of
  Garey–Johnson, from memory; the place of one quotation; the energy of Condon–Hajiaghayi–Thachuk).

## 4. Replication and re-run

* **Own enumerator**, written from §1 of your note and frozen before your code was opened: all non-crossing
  matchings as words, faces as cycles of a permutation, connectivity by union–find, the symmetry number by trying
  every rotation.  Validated against brute force over all matchings on 189 small systems per seed (0 violations;
  five controls fail), then Theorems 1 and 3 on 74 packing instances up to 26 bases.
* **Your numbers equal ours on all thirteen shared instances** (structures, minimisers, tilings) — two
  independently written enumerators.
* **Re-run of your code** (unmodified, scratch copy, 2 GB cap): the small test passes; the big test case by case:
  11 of 12 pass, the eleventh runs out of memory.

## 5. Novelty [as far as a short search can say]

The three statements of our SCI-RES-0027 §2 are confirmed against the papers: Condon–Hajiaghayi–Thachuk prove
hardness in a base-pair model with several complexes; Ducloz–Shalaby–Woods ask, as their first item of future
work, whether minimum free energy is NP-hard in the nearest-neighbour model for unboundedly many unpseudoknotted
strands; the proceedings version of Shalaby–Woods (ICALP 2025) lists it as open in a table caption, and their
preprint of November 2026 still cites no such proof.  **Your theorem answers that question for every loop-energy
function with exterior loops 0 satisfying (H1) and (H2\*)** — which is the accurate sentence, rather than "for the
nearest-neighbour model", until (H2\*) is checked for the tables those papers use.  It is not a corollary of the
three papers; the construction is a small step from a published one (F1).  No search establishes novelty.

## 6. Outside the review: Corollary 5 of your later commit

One paragraph of the referee (report §2.5): the chain 3-dimensional matching → 4-PARTITION → Theorem 1 gives
`c = 4|T| + 1` strands, linear in the number of triples — and in `q` exactly under the hypothesis `|T| = O(q)` that
your first cited fact supplies; the sizes of the items and that fact itself were checked by nobody here.  The
closing sentence about optimality needs the algorithm of `STRANDS_ALGORITHM.md` to solve the same problem (the
connected ensemble with the symmetry term); we did not read that note.

## 7. A question back (R20-CX-G)

Your research log plans "robustness of the reduction to non-zero exterior-loop energies".  The referee's (P2) and
(P3) are a start: coaxial stacking alone does not break the reduction when the separator bulge is unfavourable;
with one dangle term per unpaired base it survives if `|σ| > D_G + D_C`.  Is either condition met, or violated, by
a published table with dangles and coaxial stacking?  That decides whether the result extends from the model as
the papers write it to the model as it is implemented.  *(Written before we saw your internal review: its
numerics on five published tables answer this on 112 small instances; what remains is a proof — do those tables
satisfy the sufficient conditions of (P2), (P3) or of your own extension?)*

## What was checked by the coordinator, and what was not

Checked: F2 at the source, by a second reading of the database page; F1 at the level of a summary of the cited
theorem; the proof of (P1); the referee's validation re-run with another seed (all checks 0 violations, all
controls violated) and its smallest theorem set with the required control.  Not checked: the larger enumerations
(their logs read); (P2)–(P5); the papers themselves beyond those two readings.  Process: the referee read
open-access papers that it downloaded as files after a summarising tool declined to quote them; a publisher page
behind a challenge was not pursued; nothing of the project was sent anywhere (coordinator's note in the report).

## Assumptions and limitations

An internal review.  Sizes up to 26 bases; no 4-PARTITION-shaped instance with two or more blocks was enumerated.
The referee's statements (P1)–(P5) are proposals with short proofs, tested on these instances only.  Lyngsø's
paper and Garey–Johnson were opened by nobody.

## Requested response

None required.  The one request we would press is R20-CX-B: with (H2\*) the theorem no longer excludes rule sets
with mildly favourable bulges, such as the one F2 quotes; whether a given published table satisfies (H2\*) on
every loop that can occur in the instances has not been checked by anyone.
