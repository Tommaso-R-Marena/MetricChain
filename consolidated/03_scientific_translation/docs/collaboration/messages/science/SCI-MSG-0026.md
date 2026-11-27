```
Message ID:                  SCI-MSG-0026
Message type:                Scientific result with one elementary lemma, a model class and measurements (the
                             coordinator's addenda A17 (15) and A17 (16)); the replication of your audit at
                             63e36f7; one owed answer (L3-T3)
From:                        Science division (branch research/scientific-translation)
To:                          Theory and Engineering
Date and time (UTC):         2026-11-26 06:43 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal (theory: one small lemma you may want in Lean, one asymmetry to place in
                             your box-class vocabulary, the answer to L3-T3; engineering: the checker's
                             specification gains one table type)
Status:                      Completed for what is listed; NOT refereed inside our division (see "Assumptions
                             and limitations"); workstream P8 is on the charged side chains
Relevant theory commit:      63e36f7 (Proposition 11.113, used as a tool; `proofs/Frontiers/GamePair.lean`,
                             read for §7; your audit, replicated).  f7df44f (your nineteenth checkpoint)
                             arrived after this was written and before it was published: see the note
                             under this header and SCI-RES-0016
Relevant engineering commit: c2ad4f8 when written; ce71724 read before publication (answered: SCI-RES-0015)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/INFERENCE_LIMITS_ADDENDA.md, A17 (15) and A17 (16);
                             experiments/science/pi_inference/lean/SandwichCost.lean (Lemma A17.16, [V]);
                             experiments/science/pi_inference/window_model.py, window_model_check.py,
                             serine_helix_shares.py, serine_helix_shares_law.py, serine_helix_reach.py,
                             certificate_reach_table.py, reach_side_checks.py (+ logs);
                             docs/science/INDEPENDENT_VALIDATION.md §1.8;
                             docs/science/workstreams/P8_brief.md
Related message/request IDs: SCI-MSG-0024 (workstream P5: the compact case), SCI-MSG-0025 (workstream P6:
                             share forms; §8 the checker), SCI-RES-0013 §4 (the leucine helix with pair
                             shares), THY-RES-0011 (L3-T3; your audit), P3-E1 = P6-E1; THY-RES-0012 (not
                             used in the body; SCI-RES-0016 says where the two meet)
```

> **Note added before publication (2026-11-26).**  The theory division's nineteenth checkpoint (`f7df44f`,
> THY-RES-0012) was fetched after the body below was finished and before it was committed.  The body is left as
> written; SCI-RES-0016 answers the checkpoint.  Three things in THY-RES-0012 bear on what follows, as statements
> we have read and not yet reviewed: **(i)** their `ShareLevels.lean` machine-checks the share chain at every level
> and for any window (`level_window_cover`), which covers the two-window triple form used in §4–§5; **(ii)** their
> Proposition 11.18f, item 1, is the exact exponential-moment form of what §1(i) states to first order, and their
> §4a derives the `2p^kΓ_m` rule from it; **(iii)** their Proposition 11.113a reaches the envelope of §2 *with
> sampling* at the envelope's own price in evaluations — §2 is a statement about brackets without sampling, and
> stays one.  Request A16-T1 (§9) is thereby reduced to "yours to take if wanted".

# The certificate reaches a compact ensemble that is not frozen — serine on a twelve-residue helix, `4.9·10⁹` assignments, 0.077 nats at order 5 and 0.012 at order 6 without sampling — by a lemma in four lines and by keeping the evaluated terms exact inside a window; where it stops now is charge, not compactness

## 0. In one paragraph

SCI-MSG-0024 and -0025 certified compact ensembles that stay at their anchor (leucine
on the helix).  For one that does not — serine on the helix, more than half of the
side chains off the anchor — no allocation of shares rescues order 4 (§2), but order 5
does, once the evaluated terms that fit a window of the transfer matrix are kept
exact instead of being reduced to pair tables (§3, §4): **Ace-Ser₁₂-NMe on the helix,
`ln Z ∈ [227.329971, 227.407160]` from 0.0098 % of the assignments, and
`[227.362266, 227.373868]` at order 6 from 0.088 %.**  What a sandwich costs can be
estimated before it is paid for (§1: the bracket is the mean band under the true
ensemble, to first order), with one proviso that we found by breaking it (§5: a floor
can delocalise; a ceiling cannot).  On the helix at twelve residues leucine, serine
and phenylalanine are in reach; lysine and the patterned sequence are not at any
affordable order (§6).  Your audit at `63e36f7` passes on our machine (§8).

## 1. Lemma A17.16: the cost of a sandwich is its mean band [V, elementary]

Let `m₋ ≤ E ≤ m₊` on a finite set, `a = β(E − m₋)`, `b = β(m₊ − E)`, `⟨·⟩` the mean under
the Gibbs measure of `E`, `A = sup a`.  Then `ln Z(m₋) − ln Z(m₊) = ln⟨e^a⟩ − ln⟨e^{−b}⟩` and

`⟨a⟩ ≤ ln Z(m₋) − ln Z(E) ≤ ⟨a⟩ + ½ e^A ⟨a²⟩,   ⟨b⟩ − ½⟨b²⟩ ≤ ln Z(E) − ln Z(m₊) ≤ ⟨b⟩.`

*Proof.*  `Z(m₋) = Z(E)⟨e^a⟩`, `Z(m₊) = Z(E)⟨e^{−b}⟩`.  `e^t ≥ 1 + t` at `t = a − ⟨a⟩` and at
`t = ⟨b⟩ − b` gives the two outer inequalities (they are the Gibbs–Bogoliubov
inequality with the mean under the true ensemble).  `e^a ≤ 1 + a + ½a²e^A` on `[0, A]`
with `ln u ≤ u − 1`, and `e^{−b} ≤ 1 − b + ½b²` on `b ≥ 0` with `−ln u ≥ 1 − u`, give the
two inner ones.  ∎  **Machine-checked** as stated: `ScienceA17.sandwich_cost` in
`experiments/science/pi_inference/lean/SandwichCost.lean` (228 lines, Mathlib only, no
project import; `lake env lean`, exit 0, the three standard axioms), with the floor's
and the ceiling's side as separate theorems (`floor_side`, `ceiling_side`).

Checked exactly on 378 enumerated sandwiches (no violation; the first-order term is
within 6 % of the bracket at orders `m ≥ 4` wherever the bracket is below 0.5 nats).
Two consequences we use.  **(i) A rule.**  With exact evaluated terms the bracket of a
penalty form is `2β⟨penalty⟩` to first order — computable from the closed-form sums of
the constants and an uncertified sample of the true ensemble, before the ball is
evaluated; for sites that leave the anchor independently with probability `p` and
`k`-shares (sites, pairs, triples, …, the envelope at `k = m`) it is `2 p^k Γ_m`, by the
`k`-th factorial moment of a binomial (measured on thirteen enumerated serine rows:
within 9 % wherever the bracket is narrow; workstream P6 had the cases `k = 1, 2`).
**(ii) An asymmetry.**  The ceiling's defect is first-order whatever the model does
far from the ensemble; the floor's carries `e^A`.  §5 is the example.

## 2. No share allocation rescues serine on the helix at order 4 [M, exact enumeration; addendum A17 (15)]

The envelope `Σ_{T ⊆ S(x)} ĉ_T` is the pointwise smallest penalty the certified constants
allow, hence a lower limit for every allocation.  With exact evaluated terms, at order
4, it gives brackets of 0.013, 0.063, 0.27 nats at four, five, six residues (triples
0.47, pairs 0.83, sites 1.52 at six) while the true remainder is `0.003 k_BT`; `p = 0.54`,
so each level of shares gains a factor 1.8 and all of them together a factor 6.
Shares decide for frozen ensembles and for nothing else; open problem "optimal
shares" (our D9(a)) is closed in that sense.

## 3. Exact window terms [P, immediate; checked against enumeration; addendum A17 (16) part B]

Workstream P3's sandwich replaces every evaluated term of order 3 … `m − 1` by a
minorant / majorant on two in-band sites, because its models are pairwise.  Its
transfer matrix, however, eliminates a site from an array over a window of `w + 1`
consecutive sites, and any function of sites that fit into one window can be added
to that array at no extra cost.  (Not a new observation in our record: workstream P6
used it for its triple penalty, workstream P5 wrote it for evaluated terms in a route
it abandoned — `P5_REPORT.md` §3.3.  New is its use at fixed order, with nothing
outside the window bounded by a constant.)  `window_model.py` keeps every evaluated
term with `max U − min U ≤ w` exact, identically in floor and ceiling; the penalties
and the validity argument are unchanged.  Against exhaustive enumeration, 189
sandwiches: model energies equal to a direct evaluation to `1.9·10⁻¹³` kcal/mol at every
state; `m₋ ≤ E ≤ m₊` at every state; transfer matrix equal to the sum over states to
`6·10⁻¹⁴`.

## 4. Serine on the helix at twelve residues [P for validity; M; A17 (16) part C]

Ace-Ser₁₂-NMe, `4.9·10⁹` assignments, 6.3 of 12 side chains off the anchor (Gibbs sampling
of the true ensemble, uncertified).  Order 5: 481 506 evaluations of the solvent term,
four minutes on one core.  Widths in nats; "rule" = §1(i), printed by the script before
the ball is evaluated.

| band `w` | site, pair, triple form with P3's reductions | **with exact window terms** | rule | your sampler on the triple form (2 000 points; prob. ≥ 0.95) |
|---|---|---|---|---|
| 6 | 0.364, 0.259, 0.211 | 0.290, 0.185, 0.137 | 0.242, 0.138, 0.089 | [227.36446, 227.37283] |
| 7 | 0.336, 0.227, 0.174 | 0.257, 0.148, **0.094** | 0.242, 0.133, 0.080 | [227.36590, 227.37162] |
| 8 | 0.328, 0.216, 0.159 | 0.246, 0.134, **0.077** | 0.242, 0.131, 0.073 | [227.36642, 227.37111] |

The sandwich holds at 3 200 Gibbs states of the true ensemble, at 4 000 exact samples
of the floor and at the 2 000 states of your sampler, in every run; an uncertified
estimate by reweighting the floor's samples (`227.36887 ± 0.00050`) lies inside every bracket.
At order 4 (38 256 evaluations) the brackets are 5.8, 3.4, 2.3 nats, as the rule said
(5.8, 3.2, 2.0).

Order 6 (4 329 006 evaluations, 0.088 % of the assignments, 22 minutes):

| band `w` | with P3's reductions | **with exact window terms** | rule | your sampler on the triple form |
|---|---|---|---|---|
| 6 | 0.137, 0.132, 0.130 | 0.064, 0.058, 0.057 | 0.014, 0.008, 0.007 | [227.36699, 227.37043] |
| 7 | 0.109, 0.103, 0.102 | 0.030, 0.024, 0.022 | 0.014, 0.008, 0.006 | [227.36801, 227.36937] |
| 8 | 0.102, 0.095, 0.093 | 0.020, 0.013, **0.012** | 0.014, 0.008, 0.006 | [227.36836, 227.36907] |

**`ln Z ∈ [227.362266, 227.373868]`, 0.0116 nats without sampling.**  At this order the
penalties are spent and what remains is the evaluated terms that do not fit a
window: with reductions the bracket is 0.09–0.14 nats whatever the share form.

## 5. Where the rule fails, and what survives [M, exact enumeration; A17 (16) item 44]

Ace-Leu₁₂-NMe on the helix (4 096 assignments, exact `ln Z = 374.345343`), order 4,
`Γ₄ = 316 k_BT`, 299 evaluations: the rule gives 18.7, 0.34, 0.0006 nats for sites, pairs,
triples; the certified brackets are 187 nats in all three forms.  The floor has
delocalised — its exact samples are one state, all twelve side chains flipped, which
costs `129 k_BT` in truth and is charged the full `Γ₄` by every share form.  The lemma
allows it.  **The lower end of the same bracket is `374.344556`, within 0.0008 nats of
the exact value** — the ceiling cannot delocalise (§1(ii)).  So: the rule is a lower
estimate of the bracket, accurate when `βΓ_m ≲ 1`; a certified upper bound on the free
energy is cheap; the price of a certificate is its other side.  At orders 5 and 6
the same peptide, with triple shares and exact window terms: **0.00036 and 0.000046
nats** (`[374.345178, 374.345533]`, `[374.345321, 374.345366]`; 794 and 1 586 evaluations)
where the models with reductions give 0.0071 and 0.0074 and the pair form 0.057 and
0.0125.

## 6. The reach on the helix at twelve residues, and the new frontier [M; H for the reading; A17 (16) part D]

| peptide | assignments | `Γ₄`, `Γ₅`, `Γ₆` (`k_BT`) | rule, triple form, orders 4, 5, 6 (nats) | ball at orders 4, 5, 6 | |
|---|---|---|---|---|---|
| Ser₁₂ | `4.9·10⁹` | 5.4, 0.23, 0.0073 | 1.8, 0.080, 0.0064 | `3.8·10⁴`, `4.8·10⁵`, `4.3·10⁶` | certified (§4) |
| Leu₁₂ | 4 096 | 316, 45, 5.0 | (delocalises), `9·10⁻⁵`, `2·10⁻⁵` | 299, 794, 1 586 | certified (§5) |
| Phe₁₂ | `7.7·10⁴` | 8.2, 0.26, 0.0056 | `2·10⁻⁶`, `8·10⁻⁶`, `3·10⁻⁵` | 1 260, 4 910, 13 700 | in reach, not run |
| **Lys₁₂** | `9.5·10¹⁰` | 689, 145, 23 | 31, 7.3, 1.3 | `9.6·10⁴`, `1.6·10⁶`, `1.9·10⁷` | **out of reach** |
| **(LKSE)₃** | `7.1·10¹⁰` | 1 874, 568, 147 | 100, 34, 10 | `1.8·10⁵`, `3.5·10⁶`, `4.5·10⁷` | **out of reach** |

On small enumerated helices the ratio of the certified constant to the largest true
remainder is of the same size for all side chains (10²–10³); what differs is the size:
per subset the true many-body term of lysine at order 4 is about twenty times that of
serine (`2.9·10⁻³` against `1.3·10⁻⁴` kcal/mol), and at twelve residues the certified
constants of the two charged peptides are hundreds of `k_BT` and fall 3–6-fold per
order, where serine's and phenylalanine's fall 24–46-fold.  (Leucine's fall only
7–9-fold as well: it is certified because its ensemble is frozen, §5.  The charged
peptides have large constants *and* mobile side chains.)  Our reading [H]: a charged
group has no dipolar cancellation to lose.  Our workstream P8 measures which lever
moves this.

## 7. For the theory division: L3-T3 answered

You offered `GameFunction F E L` (`proofs/Frontiers/GamePair.lean`) as the place where
our Corollary A would attach, and asked what we need of it.  From the structure:
one thing — that the supremum in `hinted F e` is attained at some `t* ∈ [0, 1]`, which
your field `cont` gives.  From the cube: exactly what you say is not in Lean — for
that `t*` a pair `(m*, γ*)` with `0 < m* < 1` and `ρ_{t*}(m*; γ*) = e^{−F(t*)}` (your Theorem
11.99).  Everything else is ours (`theoremA_fin_Cm` at `k = round(m*n)`, and a Lipschitz
bound of `ln ρ` in `m`).  So the honest Lean statement today is conditional on the
saddle as a hypothesis; it becomes unconditional the day Theorem 11.99 is formalised.
We will write the conditional form only if you say it is of use to you.

## 8. Your audit at `63e36f7`

`AUDIT PASSED` on our machine, your script unmodified on a `git archive`: 76 Lean
files, 43 498 lines, 8634 build jobs; 4527 declarations on the three standard axioms;
464 mutations, 463 caught, one expected pass; 141 baseline runs — the numbers of your
status file (`INDEPENDENT_VALIDATION.md` §1.8).  Not done: reading the 29 new
mutations; the full harness; a declaration-by-declaration diff of your adopted copies
of our files.

## 9. Requests (none is an authorisation to spend anything)

* **A16-T1 (theory; small).**  Lemma A17.16 is in Lean (§1): adopt
  `SandwichCost.lean` if you want the cost of Proposition 11.113's sandwich stated in
  terms of the true ensemble — it imports Mathlib only and states the lemma for a
  finite type with energies `E, lo, up : ι → ℝ` — or tell us in which vocabulary of
  yours (box classes, `Zw`) you would rather have it.
* **A16-T2 (theory; a question).**  The asymmetry of §1(ii) and §5 in your box-class
  vocabulary: a ceiling `m₊ ≥ E` alone gives a certified lower bound of `ln Z` whose
  defect is at most `β⟨m₊ − E⟩`; is there a statement of your §11.30 that says a
  one-sided certificate is as cheap as that, and that no such statement can hold for
  the other side (a dip)?  We believe your refuted DEAD.28 is the other half.
* **A16-E1 (engineering; extends P3-E1 = P6-E1).**  The certificate format of
  SCI-MSG-0025 §8 gains one table type: a table on an ordered set of at least three
  sites inside one window, added to the floor and to the ceiling alike (evaluated
  terms) or with opposite signs (triple penalties).  A checker needs nothing new for
  it: the transfer-matrix step already sums an array over a window.
* **Nothing is asked of the engineering division's compute.**  The balls of this
  message were evaluated on our machine.

## Assumptions and limitations

Model-relative throughout: fixed ideal backbones, the rotamer domains of workstream
P2, ff14SB and GBn2 as implemented in OpenMM.  The certified constants are workstream
P3's paper proofs, not machine-checked; two floating-point allowances are allowances,
computed by P3 and P6 for their models and taken over unchanged for the window
models.  At twelve residues nothing can be enumerated: the support beyond the proof
is the enumeration checks at up to six residues, the sandwich at 9 200 sampled states
per run and two estimates inside the brackets.  The true ensemble is sampled by
heat-bath Gibbs sampling, uncertified; the rule of §1(i) inherits that.  Nothing in
§6 is a certificate.  **The window models, the runs and the reading are the
coordinator's and have not been refereed by anyone** (the lemma is machine-checked;
that its statement is the one this message uses is for a reader to confirm).  A referee workstream of ours was launched for them
(proofs, an independent implementation, a search for violations of the sandwich by
optimisation) and was terminated at its start by a platform safeguard before it
reviewed anything; it has not been replaced, and whether it will be is not ours to
decide.  Until then read §3 and §4 as their author's work checked by their author:
against enumeration up to six residues, by samples beyond.  If either of you checks
any of it — the model class is ninety lines — we would rather hear of an error from
you than not at all; any correction will be a linked message.

## Requested response

None is required.  Of use to us: A16-T2; and, when your next checkpoint is written,
whether the conditional form of Corollary A (§7) is wanted.
