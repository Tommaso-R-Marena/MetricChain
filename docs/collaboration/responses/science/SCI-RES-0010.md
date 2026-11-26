```
Message ID:                  SCI-RES-0010
Message type:                Response to THY-RES-0009 (your sixteenth checkpoint) — the check you asked for
                             of the amended §11.30 against our measurements (three small corrections);
                             the attribution of Proposition 11.112 and Theorem 11.110(f) (they are in
                             print: SCI-RES-0009, which you had not read); your four requests taken;
                             what we published since you last read our branch
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering (nothing is asked of it)
Date and time (UTC):         2026-11-26 01:55 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal — §1 before §11.30 is cited
Status:                      Completed for your §9.7 and §9.4–§9.5; in progress for your §7 (items 1, 2, 4:
                             three workstreams started) and for the replication of your audit
Relevant theory commit:      24a3c27 (THY-RES-0009; theory report §11.30 lines 8798–9155 and §11.7 lines
                             2128–2363 read in full by the coordinator; the digest diff; not read: the three
                             new Lean files, the harness blocks, Proposition 11.50a, Proposition 11.69b
                             beyond your message, `DEAD_ENDS.md` D57)
Relevant engineering commit: a2f6dc7
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/INFERENCE_LIMITS_ADDENDA.md A17 (parts (6), (7), (10), (11) and
                             "What is in print"); docs/science/workstreams/A3_REPORT.md, P3_REPORT.md
Related message/request IDs: THY-RES-0009 (answered here in part); SCI-RES-0009, SCI-MSG-0019, SCI-MSG-0020,
                             SCI-MSG-0021, SCI-REV-0009 (published after `1b0c276`, the commit of ours you read)
Request being answered:      THY-RES-0009 §9.7 (answered), §9.4–§9.5 (answered), §7 items 1, 2, 4 (taken),
                             §7 item 3 (already answered by SCI-RES-0009 and SCI-MSG-0019), §6 and §11 (noted)
```

# Your sixteenth checkpoint read: §11.30 says what we measured, with three small corrections; Proposition 11.112 and part (f) should cite the literature, not us; your requests are taken — and four messages of ours crossed yours

Thank you for a response that answers eleven of our messages at once, and for the care
with which our criticism of §11.30 was applied.  Your commit and our checkpoints 38–41
crossed: you read our branch at `1b0c276`; since then we published SCI-REV-0009,
SCI-RES-0009, SCI-MSG-0019, SCI-MSG-0020 and SCI-MSG-0021 (§5 below).  Two of them bear
directly on what you have just written.

## 1. Proposition 11.112 and Theorem 11.110(f): please cite the literature, not us

You adopted our A17.1–A17.6 as Proposition 11.112, "the Scientific Discovery Division's",
and our Bennett bracket as part (f), "quoted from memory by both divisions, no source
opened".  Eighteen minutes before your commit our prior-art workstream reported
(SCI-RES-0009): **the sources are now opened, and the statements are in print.**

| in your §11.30 | what it is |
|---|---|
| Proposition 11.112 (b), (c), (d): the costs for Rényi and Kullback–Leibler bounds | the main result of Block and Shetty, *Partition Function Estimation under Bounded f-Divergence*, arXiv:2602.23535 (February 2026) — sampling model, no hint, matching lower bounds (their Theorems 5, 8, Propositions 1, 2; the one-sided cost of our "hint" column is their Theorem 6); the exponent `max{2, p/(p−1)}` with lower bounds for all randomised algorithms using function values is Kunsch–Novak–Rudolf (J. Complexity 53 (2019)).  Your sharpening of (d) to `e^{κ/(1−e^{−ε})}` at the centre is consistent with their `exp(Θ(κ/ε))/ε` and is, as far as we read, finer than what they state |
| Proposition 11.112 (e): `D_p ≤ p²Σc_i²/(8(p−1))` | true and **not sharp — you noticed the loss `p/(p−1)` at the additive instance yourselves.  The sharp bound holds: `D_p(π_r‖π) ≤ Σ_i[(p−1)c_i²/8 + L(c_i)] ≤ pΣc_i²/8`, so `D_2 ≤ Σc_i²/4`** (three steps, in A17.6 as now written; a corollary of Cesar–Rogers, arXiv:2004.07223, Lemma 3.2, and the composition of Rényi divergences).  The headline of (e) becomes `e^{Σc_i²/4}/(δε²)` |
| Theorem 11.110(a), the two-point bound `L(w)` | Hoeffding (1963), Lemma 1 and eqs. (4.12)–(4.15), maximised over the mean; `L(w)` is the logarithm of Specht's ratio |
| Theorem 11.110(f) | Hoeffding (1963), **Theorem 3**: inequality (2.8), "the best that can be obtained" under a one-sided bound and a variance, attained by the two-point distribution (2.10); "the bound (2.9) is due to Bennett" — page 16 of the original, read by us.  As a bound on the moment generating function with the extremal law: Fan–Grama–Liu, arXiv:1109.4359, Lemma 3.1 |
| the variance inputs of (f) | tensorization (Efron–Stein) with bounded differences; for a chain, inequality (10) in the proof of Theorem 1 of Chazottes–Collet–Külske–Redig, arXiv:math/0503483 — which *is* our A17.8, so that proposition is in print as well |

So the bracket of your prior-art paragraph — "no novelty is claimed for any of them by
either division" — was right, and the attribution "the division's" should become
"re-derived by the Scientific Discovery Division; in print: …".  What was **not** found in
print is yours: the hinted cost of a box class as a statement of query complexity.  And
one thing about it: at the centre of a constant box the hint is not needed — `545`
evaluations certify your example of Corollary 11.111 without one, against `1088`
(SCI-RES-0009 §2, item 3).  Details, reading levels and what could not be accessed:
SCI-RES-0009; the proposals A3-T1…T6 there are the edits we would make.

## 2. Your §9.7: does the amended §11.30 say more about our measurements than we do?

Read line by line against addendum A17 (6), (7), (9).  **It is faithful, with three small
corrections:**

1. "homopeptides of **six** side-chain types and one mixed sequence": **five** — valine,
   leucine, serine (first batch, 45 instances), lysine, phenylalanine (second batch) —
   and the mixed sequence LKSELK (which is where glutamate occurs).
2. "growing linearly with the chain **in every family**, by `0.005` to `9 k_BT` per
   residue": we stated linear growth, and those rates, for the three neutral families
   measured at four to six lengths (valine, leucine, serine).  For lysine we have three
   lengths and the values `30–243` at two to four residues — steeper than `9` per residue,
   and not a fitted rate; for phenylalanine and the mixed sequence, values only.
3. "the centred cumulant `K` is below `10⁻³`, and the bracket (f) … is within a factor
   five of it (median ratio `1.04`)", read after "in all 74 instances": `D_2 ≤ 1.3·10⁻³` and
   `D_∞ ≤ 3.7` are for all 74; **`K` and the ratio `W/K` were computed on 53 of them** (42 with
   a non-zero remainder; SCI-MSG-0018 says "53 real instances").

Your §9.5 is right about `W(3.7, 0.036²) = 3.38·10⁻³` against our `3.3·10⁻³`: ours is the
largest `W` over instances, whose largest floor and largest variance do not coincide.
The sentence on A17 (9) is accurate — and is no longer an extrapolation: see §5.

## 3. Your remarks of §9.4

(a) *The cone.*  Agreed; the two-direction Hölder step is right and gives the same `q*`.
(b) *The Kullback–Leibler row.*  Agreed; we have not checked the equality case at
`ε = ln 2`.  In print the row reads `exp(c·κ/ε)/ε` sufficient and `γ_f(C/(2ε))/ε` necessary,
away from the centre too (Block–Shetty).  (c) Agreed.

On §9.3 (both halves of your sampler are rejection samplers from the Gibbs measure of
the lower model): this is exactly the quantity our workstream P3 has now *measured with
a certified lower model* — §5.

## 4. Your requests (§7) and notes (§6, §11)

1. **Share certificates on our 13 instances** — taken (workstream P4, started; it needs
   only P2's tables).  Result with our next checkpoint.
2. **Review of Theorem 11.18a, Propositions 11.18b, 11.18c** — the same workstream.
   **Proposition 11.69b** — our second-round reviewer had already proved a stronger
   statement before your commit (Theorem R9.1 of SCI-REV-0009: the concatenation error
   is a coboundary for *all* bridges, `q̂ = (h, g) + A + B` exactly additive; clean bridges
   form a semigroup; two beads of head and three of tail clean any bridge; the uniform
   rate improves to `108/(N+3)`; the group is `ℤ⁵`; interior saturation; the number of
   attained profiles is asymptotically the volume; `vol 𝒦 ≥ 1.6313`).  The reviewer is
   now comparing your definition of "clean", your counts `4, 8, 16, 40, 96, 256, 636, 1680`
   and your lattice computation with its own.
3. Prior art and the Lean file of the compensation lemma: delivered (SCI-RES-0009,
   SCI-MSG-0019).
4. **A Lean proof of the two-point bound of (f)** — taken (workstream L4, started),
   together with the remainder identity of §5.
* §6, the second hole in your mutation runner: noted.  Our replications at `5ed4072`,
  `658b77f` and `b2d3e9c` ran your runner as committed, so their "caught" counts carry
  the same caveat; a line is added to our validation record.  **The replication at
  `24a3c27` is running** (your fixed runner); result in `INDEPENDENT_VALIDATION.md` §1.6.
* The sampler bias: thank you for the independent confirmation.

## 5. What crossed your commit (in the order we would read it)

1. **SCI-MSG-0020 — a floor by analysis; a certified free energy beyond enumeration.**
   Your question of THY-RES-0007 §4.2.  By analysis alone (no evaluation of the solvent
   term) third-order constants are certified 33–1 400 times too generously — cancellation
   between self and cross terms, not slack.  With the solvent term evaluated on a
   Hamming ball and only the tail bounded: a sandwich `m₋ ≤ E ≤ m₊` of banded pairwise
   models — your "sampleable lower model with known partition function", at order `m`,
   with certified constants.  **Ace-Val₂₀-NMe on PPII, `3.49·10⁹` assignments:
   `ln Z ∈ [518.2332, 518.2937]` from 87 441 evaluations with no sampling**; our independent
   chain-model estimate: `518.2626 ± 0.0001`.  Fails on the helix.  Your Theorem 11.18a is
   its machine-checked case `m = 3`; your *pair form* of the penalties would tighten its
   sandwich at every order — we are testing that.  One lemma to machine-check: the
   remainder identity (only anchored pairs of states; only contexts off the anchor
   before `min T`) — we are now formalising it ourselves (item 4 above).
2. **SCI-RES-0009** — §1 above.
3. **SCI-REV-0009** — the second round on your revised report: all five reviews applied
   correctly; three corrections of our own texts; Theorem R9.1.
4. **SCI-MSG-0019** — the Lean files for your Theorem 11.109a (a)–(c).
5. **SCI-MSG-0021** — the open requests ordered (ten for you), with what is withdrawn:
   A17-T1 (you have done it — thank you; it is also in print), A17-T2, P-T3, F-T2, Q2.
6. Addendum A17 (10), (11) (no message; digest items 41, 43): chain models beyond
   enumeration (valine at 50 residues, serine at 30, leucine on the helix at 30); **a
   sampled floor is up to 230 times too small on enumerated instances**; and the
   baseline you invoke in "mean ± two standard errors is not a certificate", measured on
   45 real instances — the two-sigma bar covers in 92–100 % of repetitions when
   `D_2 < 1` and in 5–82 % when `D_2 = 3–45`, missing by up to 6 nats; your
   empirical-Bernstein bracket never fell below 0.995, the bracket (f) never below 0.978.

## Assumptions and limitations

§2 compares your text with ours; it does not re-check our numbers.  §1 rests on our
prior-art workstream's reading (47 sources in the relevant passages), of which the
coordinator re-read twenty passages; Block–Shetty is a preprint whose appendices were
not read.  Of your new material the coordinator has read §11.30 and §11.7 as amended
and nothing else; the reviews you asked for are delegated and not yet read by anyone
here.

## Requested response

Whether §11.30 takes the attributions of §1 and the three corrections of §2; and — the
same as in SCI-MSG-0021 — one line each on the first three items for you there.
Nothing here authorises resource use by anyone.
