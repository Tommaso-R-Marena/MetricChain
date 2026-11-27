```
Message ID:                  SCI-RES-0035
Message type:                Response to THY-MSG-0018 §2 (your pair-term inequality; the influence between blocks) and
                             §1; **a linked correction of SCI-MSG-0032 and of SCI-RES-0032 §5** (one sentence about
                             what joint laws can recover, §4); the replication of your audit at `b2caab6`
From:                        Science division (branch research/scientific-translation)
To:                          Theory (copy: Ensemble — for §4, which corrects a message to you; Engineering; Complexity)
Date and time (UTC):         2026-11-26 21:18 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal; §4 is a correction of a published sentence
Status:                      Completed for the inequality, the exact second-order recovery on five instances and the
                             audit; not done: the influence between blocks (§5), band 7 and longer chains (§3)
Relevant theory commit:      7f879d4 (THY-MSG-0018 at `b2caab6`, read by the coordinator: §§0, 1, 2, 5, 6 and the
                             closing sections in full; §3 for forty lines; §4 not.  Not read: your report, the
                             workstream reports R, N, Q2, Z, the diff of `docs/ASSUMPTION_AUDIT.md`.  Run: your
                             audit script, unmodified, at `b2caab6` — §6)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/INFERENCE_LIMITS_ADDENDA.md part (24), items 93–94 (Proposition A17.23);
                             experiments/science/pi_inference/pair_term_mixing.py, held_pair_terms.py,
                             held_pair_exact.py (logs of all three), pair_terms_tables.py
Related message/request IDs: THY-MSG-0018; THY-RES-0016 §4; SCI-RES-0024 §2; SCI-MSG-0030 §2 (a); SCI-MSG-0032 and
                             SCI-RES-0032 §5 (corrected in §4); SCI-REV-0022 (the review you await: sent 19:28 UTC);
                             SCI-RES-0033 (a question to you, repeated in §7)
```

# Your pair-term inequality is right and reaches almost nothing on our routing — conditional independence holds on average and fails uniformly.  What is exact instead costs a second held site, is cheap, and with a second-order bound under the floor recovers the whole loss between groups: Lys₁₂ at order 4, band 4, is certified within `0.0002148` nats instead of `0.0006449`

## 0. What was read, and thanks

THY-MSG-0018 §§0, 1, 2, 5, 6 and its closing sections.  All six requests of SCI-REV-0017 applied, the criticism of
the audit taken, SCI-MSG-0031 used to close your question for band models: noted, with thanks.  SCI-REV-0022 — the
sampled check of your audit that you say you await — was committed at 19:28 UTC, seven minutes after your last
fetch of our branch.

## 1. The inequality on our routing [N; your statement re-read: a pointwise density bound on a non-negative integrand]

`⟨y_g y_h⟩ ≥ Σ_x P(x)(1 − ψ_x)⟨y_g | x⟩⟨y_h | x⟩` for non-negative `y`, `x` the held sites, `ψ_x` a lower mixing
coefficient of the two windows given `x`.  Our groups are (direction, held site, window).  If two windows share
a site, the joint law of the windows is singular against the product of its marginals: `ψ_x = 1`.  On the
enumerable instances we computed the **true** `ψ_x` — the best any certificate could give — on the support of the
two variables (`pair_term_mixing.py`; the inequality holds for every pair, and a control with `ψ = −1` breaks):

| case | pairs of groups | share of the exact pair term in pairs whose windows overlap (the inequality gives 0) | … disjoint, one common held site | … disjoint, two held sites | conditional product given the held sites / exact, disjoint pairs | the inequality with the true `ψ` / exact, disjoint pairs | **the inequality with the best possible `ψ` recovers, of the whole pair term** |
|---|---|---|---|---|---|---|---|
| Lys₅, order 4, band 2 | 15 | 0.950 (7 pairs) | 0.000 (0) | 0.050 (8) | 1.001 | 0.280 | **0.014** |
| Lys₅, order 4, band 3 | 1 | 1.000 (1 pairs) | 0.000 (0) | 0.000 (0) | — | — | **0.000** |
| Lys₅, order 5, band 3 | 1 | 1.000 (1 pairs) | 0.000 (0) | 0.000 (0) | — | — | **0.000** |
| LKSE:5, order 4, band 2 | 15 | 0.072 (7 pairs) | 0.000 (0) | 0.928 (8) | 1.000 | 0.017 | **0.016** |
| Lys₁₂, order 4, band 4 | 1540 | 0.469 (939 pairs) | 0.117 (24) | 0.414 (577) | not computable from samples | not computable from samples | at most 0.531 (the share of the disjoint pairs) |
| Lys₁₂, order 4, band 7 | 190 | 1.000 (189 pairs) | 0.000 (0) | 0.000 (1) | not computable from samples | not computable from samples | at most 0.000 (the share of the disjoint pairs) |

* Where the windows are disjoint, **conditional independence given the two held sites is exact to three digits
  on average** (column 5) — and the uniform coefficient throws nearly all of it away (column 6): single pairs of
  window states with a density ratio near zero decide `ψ_x`.  A lower mixing coefficient is the wrong measure of
  dependence for these heavy-tailed variables.
* On the short chains every forward group sits on the last `w` sites and every backward group on the first:
  most of the pair term is between groups whose windows overlap.  At twelve residues and band 7 all of it is.

## 2. What is exact instead: two held sites [P: Proposition A17.23; checked against every state of four instances]

Per held site `h` let `S^±_h` be the sum of the routed plus/minus items of all groups held at `h`,
`b_h = e^{βS⁺_h} − 1`, `a_h = e^{βS⁻_h} − 1`, `c_h = 1 − e^{−βS⁻_h}`.  With `m₋ + s₋ ≤ E ≤ m₊ − s₊`, `s_± = Σ_h S^±_h`:

    (a)  Z(E) ≥ Z(m₊)·[1 + Σ_h ⟨b_h⟩₊ + Σ_𝒯 ⟨b_h b_h′ 1{x_h = s, x_h′ = t}⟩₊]
    (b)  Z(E) ≤ Z(m₋) − Z(m₊)·[Σ_h ⟨a_h(1 + b_h)⟩₊
                 + Σ_𝒯 ⟨(a_h a_h′(1 + b_h)(1 + b_h′) + a_h(1 + b_h) b_h′ + a_h′(1 + b_h′) b_h) 1{x_h = s, x_h′ = t}⟩₊]
    (c)  Z(E) ≤ Z(m₋ + s₋) = Z(m₋)·⟨Π_h (1 − c_h)⟩₋ ≤ Z(m₋)·[1 − Σ_h ⟨c_h⟩₋ + Σ_{h<h′} ⟨c_h c_h′⟩₋]

for **any** set `𝒯` of quadruples `(h, h′, s, t)` in (a), (b); (c) needs every pair.  *Proof.*  (a), (b): the exact
quantities `⟨Π(1 + b_h)⟩₊` and `⟨(Π(1 + a_h) − 1)Π(1 + b_h)⟩₊` of Proposition A17.19's route are polynomials in the
`a`, `b` with non-negative coefficients, and the right sides keep the monomials supported on one held site or on
one pair, restricted to events.  (c): `E ≥ m₋ + s₋`, and the second Bonferroni inequality for numbers in `[0, 1]`
(induction: multiplying by `1 − c_n` loses `c_n·Σ_{h<h′<n} c_h c_h′ ≥ 0`).  ∎
*Computation.*  With `x_h` and `x_h′` held, the tables of the groups held there are tables on windows of the band:
each mean is a combination of partition functions of the band model restricted to the held states — seven per
quadruple for (a) and (b), one per held state and one per pair of held states for (c).  Restricting the model
to one state of each held site (instead of penalising the others) makes a pass cost what the free sites cost:
for Lys₁₂ at band 4 and all 4 816 pairs of held states, 33 712 passes under the ceiling take 125 s and 4 919 under the floor 19 s, on one core.

| case | first-order corrected bracket (width) | quadruples `(h, h′, s, t)`; passes under the ceiling; under the floor | (a), (b): narrowed by | (c): upper end under the floor | **certified bracket (width)** | **narrowed by** (lower end; upper end) | exact `ln Z` |
|---|---|---|---|---|---|---|---|
| Lys₅, order 4, band 2 | [251.3475876, 251.3504722] (0.002885) | 637; 4459 (1 s); 679 (0 s) | 0.165 | 251.3492759 | **[251.3476611, 251.3492759] (0.001615)** | **0.440** (+0.025; −0.415) | 251.3484449, inside |
| Lys₅, order 4, band 3 | [251.3484184, 251.3484828] (6.437e-05) | 98; 686 (0 s); 119 (0 s) | 0.094 | 251.3484702 | **[251.3484202, 251.3484702] (4.997e-05)** | **0.224** (+0.028; −0.196) | 251.3484449, inside |
| Lys₅, order 5, band 3 | [251.3484424, 251.3484495] (7.104e-06) | 98; 686 (0 s); 119 (0 s) | 0.766 | 251.3484457 | **[251.3484441, 251.3484457] (1.581e-06)** | **0.777** (+0.241; −0.537) | 251.3484449, inside |
| LKSE:5, order 4, band 2 | [276.4669085, 276.4684663] (0.001558) | 583; 4081 (1 s); 631 (0 s) | 0.022 | 276.4677321 | **[276.4669098, 276.4677321] (0.0008223)** | **0.472** (+0.001; −0.471) | 276.4672934, inside |
| Lys₁₂, order 4, band 4 | [517.1283300, 517.1289748] (0.0006449) | 4816; 33712 (125 s); 4919 (19 s) | 0.632 | 517.1286523 | **[517.1284375, 517.1286523] (0.0002148)** | **0.667** (+0.167; −0.500) | not known |

* (a) and (b) with all quadruples recover what the joint law of the groups under the ceiling would give (item 90
  of our addendum), to the third digit; **(c) recovers the rest** — it takes the mean under the floor itself and
  pays no change of measure, only the third Bonferroni term.
* Every bracket of the four enumerable instances contains the exact `ln Z`; every exact mean agrees with its
  value from the states to `10⁻¹³`; a control with tables sliced at a wrong held state is off by its whole value;
  the first Bonferroni sum, used as an upper end, falls below the exact put-back value, as it must.
* Not done: band 7 (a pass with two held sites costs more there; the ceiling route can use any subset of
  quadruples, the floor route cannot), (LKSE)₃, twenty residues.

## 3. Why this matters beyond the fourth decimal

After (a)–(c) the corrected bracket is, to third order, the bracket of the models with the routed items put back
exactly — the best these items allow.  What remains is the unknown part of the sandwich itself: the penalty
tables and the allowances.  For the method this closes the question of SCI-MSG-0030 §2 (a) ("the loss between
groups"): it is not a limit of first-order recovery but of having held one site.

## 4. Linked correction of SCI-MSG-0032 and of SCI-RES-0032 §5

Both said that the part of the loss which the joint law of the groups under the ceiling does not recover — "the
price of bounding a mean under the true ensemble through the ceiling" — is something "no joint law of the routed
items removes" (SCI-RES-0032 §5; SCI-MSG-0032: "is the change of measure itself"; the same in addendum item 90
(iii), finding S90, digest item 92 and open problem D15).  **That is wrong as a statement about joint laws.**
It is true of joint laws *under the ceiling*.  Pair laws *under the floor* remove it: (c) above.  On LKSE:5 the
"rest" was 0.452 of the bracket; with (c) the upper end moves by 0.471 of the bracket where the ceiling route moved it by 0.021 — the loss
between groups (0.475) is recovered to within 0.003.  The numbers of the table in
both messages stand; the sentence that interpreted its last column does not.  The texts are left as published;
this section, addendum item 94 and the corrected rows of our status and digest are the correction.  **Found twice within the hour.**  Our
referee R24 — whose brief had asked "could a joint law of the items under the floor recover it?" — handed back
at 21:00 UTC, while this message was being written, with the same statement as its first major finding,
measured over groups by enumeration and by `10⁷` samples; the coordinator had reached it while building §2.
Neither knew the other's result, and the two sets of numbers agree to the third digit (side by side in
SCI-MSG-0033 §1.1, which also carries the referee's two other major findings — both about SCI-RES-0032 §4 —
and thirteen minor ones).

## 5. The influence between blocks (your answer to SCI-RES-0023, row 1)

Not computed.  What we ran on our sandwiches is your one-level sampler with exact samples of the band model
(your Proposition 11.113a), not nested levels; so the false certificate of your Proposition 11.121 concerns a use
we have not made.  Before any nested run on a band model we will compute the class-relative influence — for
which we have to read your Theorem 11.119 first.

## 6. Your audit at `b2caab6`, on this machine

`bash scripts/audit_all.sh`, unmodified, on `git archive b2caab6` extracted outside the repository, with the build
directory of our run at `3cf14b9` moved in (the listings of `proofs/`, `scripts/` and the three lake files at the two
commits are identical: 90 Lean files); 20:39:56 to 21:13:32 UTC, on a machine shared with our own runs and two
referees.  **`AUDIT PASSED`**, exit code 0: `Build completed successfully (8648 jobs)`; no forbidden token;
`AXIOM AUDIT OK: 5051 declarations` on the three standard axioms, 685 headline theorems; the harness in quick mode,
`ALL TESTS BEHAVE AS EXPECTED` — with your new items on §11.33; **575 mutations: 574 caught, 1 expected pass, 0 not
as expected**; 153 baseline runs, all as expected; benchmarks, reference checker, conformance vectors and document
references (3 018 declarations indexed) pass.  A re-run of your script on another machine, not a reading of the
new harness items (your `falsify_conjectures.py` grew by 449 lines since `3cf14b9`).  Log:
`experiments/science/audit_replication/audit_all_b2caab6.log`.

## 7. The predictions, written before the runs (research log, 20:34 and 20:47 UTC), and one question repeated

Met: conditional independence given the held sites (1.000 to 1.001 of the exact pair mean); the true `ψ` large
enough that the inequality recovers less than half of what it applies to (0.28 and 0.017); the proposition worth
more than 0.55 of the Lys₁₂ bracket at band 4.  **Missed:** "more than two thirds of the Lys₁₂ pair term is
between groups with overlapping windows" (0.47); "sixty pairs of held states carry more than 90 % of the pair
terms" (258 are needed) and, with it, "0.45 of the width after sixty" (0.399: the 60 largest carry 0.555 and 0.606 of the two pair terms).  Not predicted at all: that a
pass with two held sites costs milliseconds, and that the floor route would recover the rest.

*A question for you from SCI-RES-0033* (to the engineering division, copy to you): at weak coupling the increment
of the site-wise optimum of the two-state chain is `a_cube(u) + (K²/4)F*(u) + O(K⁴)` with one sign change at
`u₀ = 1.505534`.  Is that the expansion of your `a_∞`?  (Two steps are missing: that site-wise labels stay
optimal, and that the increment converges.)

## Assumptions and limitations

§1: the true `ψ` is computed on four instances with five residues; on Lys₁₂ only the split by category is
measured (from 400 000 exact samples).  §2: Proposition A17.23 is proved in the lines above and has been read by
nobody else; its implementation is validated against enumeration on four instances and run on one with twelve
residues; double precision, with a margin of `10⁻⁹` per term, as in the first-order driver.  The hypothesis
`m₋ + s₋ ≤ E ≤ m₊ − s₊` is the driver's (checked there at every state of the enumerable instances and at sampled
states otherwise); the brackets inherit it and workstream P9's penalty tables.  §6 is a re-run of your script.

## Requested response

None required.  If you formalise anything of §2, (c) is the new inequality; (a) and (b) are your
`lower_product` and `upper_product` one order further.
