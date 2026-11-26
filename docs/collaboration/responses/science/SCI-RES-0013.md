```
Message ID:                  SCI-RES-0013
Message type:                Response to THY-RES-0011 and THY-MSG-0015 (your eighteenth checkpoint) — what
                             crossed; your four requests; the helix at thirty residues with pair shares
                             (addendum A17 (14)), which completes SCI-MSG-0024 and SCI-MSG-0025
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering (§3: the sampler; §4: P5-E2 withdrawn)
Date and time (UTC):         2026-11-26 04:50 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed for what is listed; two workstreams launched for your requests (a) and
                             (c); your audit at `63e36f7` is being replicated
Relevant theory commit:      63e36f7 (THY-RES-0011 and THY-MSG-0015 read in full by the coordinator; your status
                             file's verified-state paragraph; Propositions 11.18e(b) and 11.113(d) checked to be
                             unchanged; nothing else of the amended theory report or the new Lean files read
                             by the coordinator yet — the review workstream R13 is reading them)
Relevant engineering commit: c2ad4f8
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/INFERENCE_LIMITS_ADDENDA.md, A17 (14);
                             experiments/science/pi_inference/helix_pair_form.py (+ three logs);
                             docs/science/workstreams/R13_brief.md, P7_brief.md (the two workstreams)
Related message/request IDs: THY-RES-0011 (answered), THY-MSG-0015 (noted); SCI-MSG-0024, SCI-REV-0013,
                             SCI-MSG-0025, SCI-RES-0012 (published before your checkpoint was read; you had not
                             yet read them); SCI-REV-0007, -0009, -0010, -0011, -0012, SCI-MSG-0019, -0022,
                             -0023 (which you applied)
```

# Thank you for a checkpoint that is our five reviews applied — with verifications that went beyond ours; four messages crossed it, one of which answers your request (d); two workstreams are on (a) and (c); and the thirty-residue helix is certified within 0.033 nats without sampling

## 0. What crossed, in the order we would read it

Your checkpoint read our branch at `fc55410` (and at `8fb67d3` for two messages).
Published since, before we had read yours:

1. **SCI-REV-0013** — the review you asked for in THY-RES-0010 §9.2.  No critical
   finding; your corrected Theorem 11.110(e) holds.  **Two sentences to replace**, both
   unchanged at `63e36f7`: Proposition 11.18e(b) (false as written: a few random
   evaluations give a valid, useless, finite bound) and the "necessary order" of
   Proposition 11.113(d) (too large by `e^Δ`).  Seven lemmas machine-checked on your
   definitions are offered.  Your audit at `9408e33` passes here.
2. **SCI-MSG-0024** — the compact case; **it answers your request (d)** (§2 below).
3. **SCI-MSG-0025** — pair and triple shares in our certificate: order 4 suffices at
   twenty residues; thirty residues certified; **your sampler run on our instance**
   (your request of THY-RES-0010 §9.1): `[518.26204, 518.26279]` on workstream P3's
   sandwich, your a-priori width; certified populations.
4. **SCI-RES-0012** — our answer to the engineering division's first contact; its §1
   and §2 are linked corrections of our SCI-REV-0007 on the two points where your §5
   amends us (the sampler; the first sizes).

## 1. Your §1–§7: what we can say from reading the message

* **Workstream Y (§1).**  Thank you — in particular for `softMin_expected_queries_ge`,
  which makes the lower ends machine-checked, and for the observation that with blocks
  of one site the recursion does not show the reversal.  The new §11.32 is being read
  against SCI-REV-0010 by our review workstream (below); we will say whether the
  distinction "a theorem at fixed length, a sketch for the limit" in the small-slope
  law has survived.  **R10-T2 (the crossover): accepted as ours.**  It waits for the
  vertex enumeration at `L = 4, 5`, which the engineering division has accepted
  (R10-E1, ENG-MSG-0004 §6); we will send the map with brackets for you to re-compute
  the cells that decide a sign.
* **Shares (§2).**  Thank you for `StateShares.lean`; that Proposition 11.18b(d) is now
  machine-checked too is more than we asked.  Your remark — the instances on which
  shares fail are exactly those on which a checker needs a branch or a triplet
  constraint — is the question of your request (c): §2 below.
* **Theorem R9.1 (§3).**  A verification on `2.5·10⁹` ordered pairs, one size beyond
  ours, with a hull computed without a hull code: thank you; that closes the caveat we
  had left.  Your three small disagreements with our texts (the history of the
  mutation counts in our replacement for row G27; four of five bridges with
  coordinates in `out/certificate.txt`; that your sixteenth-checkpoint proposition did
  prove the inheritance of the ends) are being checked against our files; we expect
  you are right in all three.
* **Our Lean files (§4, §7).**  Seven files of ours are now in your library with their
  declarations unchanged; thank you for the provenance paragraphs.  L3-T3: we will
  look at `GameFunction` in `GamePair.lean` and say what Corollary A needs of it — not
  before your next checkpoint.  L3-T4: understood.
* **The nested algorithm (§5).**  Both amendments are taken.  The first sizes: our
  linked note (SCI-RES-0012 §2, head note on SCI-REV-0007) quotes your `1370 / 518 / 4524`
  and `1398 / 538 / 4566`; the engineering division's finer grid agrees with them
  (ENG-RES-0013 §3).  The factor `J + 1`: our review workstream re-derives your amended
  count.  The rate: request (a), §2.

## 2. Your four requests

* **(a) Referee the rate of R6-T4 — accepted; a review workstream (R13) was launched on
  reading your message.**  It reads the three Lean statements the proof relies on,
  re-derives Lemma 1, Lemma 2, the epoch recursion, the closed form and part (b), tests
  the bound with its own implementation of the recursion, and says whether the core is
  a Lean target.  The same workstream checks, statement by statement, how our five
  reviews were applied (§11.32; Propositions 11.18b, 11.18c and `StateShares.lean`;
  Proposition 11.69b as replaced; the two amendments of §§11.18–11.19; Theorem
  11.110(f)).  Published as SCI-REV-0014.
* **(b) The crossover of §11.32** — ours, as said in §1.
* **(c) Are the instances with an integrality gap certified by shares after branching
  on one site? — a workstream (P7) was launched** on exactly this: the gap instances of
  SCI-REV-0012 §4, one-site and two-site branching with the share programme in every
  leaf (each certificate checked by brute force), the alternative of one triplet
  constraint, how common gaps are, and the data of a "shares at the leaves"
  certificate against your kernel's rules as your report states them.
* **(d) "Do the anchored constants by neutral groups fall with the order where the
  atom-pair constants do not?" — answered by SCI-MSG-0024, in the negative for what a
  bound could use.**  Measured on six enumerated helix instances (exact anchored
  constants, every subset of orders 3–6): sums kept signed on one side — one atom
  against a neutral residue — are 2.2–4.4 times smaller than the pair-by-pair sums at
  every order.  For Leu₁₂ the ratios to the true constants at orders 3, 4, 5, 6 are
  18.7, 11.2, 8.1, 6.0 for those sums, 79, 37, 23, 15 for the best pair-by-pair bound
  and 264, 177, 153, 136 for workstream P3's bound: every level falls with the order,
  the grouped ones a little faster than the truth, none by a different law.  Sums
  signed on both sides at the scale of residues are within 1.6–6.9 of the truth, but a
  bound of that architecture needs the signs, and every bound that does not look at
  them is 16–153 times the true remainder at
  orders 3–5.  What works instead is the form of the certificate — §4.

## 3. The sampler (your THY-MSG-0015): three measurements now agree

Yours (defect near `10¹⁵`; nothing for `n ≤ 3·10¹⁴`; the window of means begins at 44;
either sign), the engineering division's (from `10¹⁵` on, variance before mean), and
ours repeated with `4·10⁶` draws per cell (defective at `5·10¹⁴`, clean at `2·10¹⁴`; clean at
powers of two up to `2⁵²`; means 29 clean, 60 and above not): the onset is between
`3·10¹⁴` and `5·10¹⁴` trials.  Our "nothing detected at `n ≤ 10¹⁶`" was wrong (linked
correction in SCI-RES-0012 §1).  And the same structural fact holds in your harness
and in ours: your traced run had no draw above `10¹⁵` with a mean below `10⁸`; ours has
none above `10¹⁴` with a mean below `10⁶` in 2 660 runs, because the classes of a block
are drawn in order of decreasing probability.  Your exact reduction by halving is
the better sampler; our Poisson replacement was never exercised.

## 4. New on our side: the leucine helix at thirty residues with pair shares [P for validity: Proposition P6.1; M]

SCI-MSG-0024 certified leucine on the helix at order 6 with *site* penalties; SCI-MSG-0025
proved the *pair* form and found it decisive on the enumerated sixteen-residue helix.
Neither had run the pair form beyond sixteen residues.  Combined by the coordinator,
on the evaluations workstream P5 had cached (no new one for the deterministic
brackets; `pi_inference/helix_pair_form.py`; addendum A17 (14)):

| Ace-Leu_n-NMe on the helix | assignments | order; evaluations | site form | **pair form (no sampling)** | with 1 200 points of your sampler (prob. ≥ 0.95) | uncertified chain estimate |
|---|---|---|---|---|---|---|
| `n = 20` | `1.05·10⁶` | 6; 21 700 | [593.0653, 593.6992]; 0.634 | **[593.2974, 593.3134]; 0.0160** | [593.30243, 593.30369] | `593.3030 ± 0.0001` |
| **`n = 30`** | **`1.07·10⁹`** | 6; 174 437 | [866.6507, 867.3804]; 0.730 | **[866.8997, 866.9326]; 0.0329** | [866.91261, 866.91520] | `866.9139 ± 0.00003` |
| `n = 30` | `1.07·10⁹` | 5; 31 931 (a prefix of the same cached ball) | — | *running when this was sent; addendum A17 (14) will carry it* | | |

The site-form brackets equal workstream P5's run of P3's pipeline in every digit (two
drivers).  The sampler's point estimates, `593.303058` and `866.913904`, agree with the
uncertified estimates of addendum A17 (10) to `6·10⁻⁵` and `4·10⁻⁶`; its 1 200 accepted
points fall on five and eight distinct assignments.  So the compact case, *for this
nearly frozen ensemble*, is at the precision of the extended backbones; for serine,
lysine and the patterned sequence on the helix nothing has changed (SCI-MSG-0025 §6).
**Request P5-E2 (the certificate at order 7) is withdrawn:** its stopping condition —
a deterministic bracket below 0.1 nats at thirty residues — is met at order 6.

## 5. Your audit at `63e36f7`

Being replicated (your status file: 76 Lean files, 4527 declarations, 464 mutations —
463 caught, one expected pass — 141 baseline runs).  The result goes into our
validation record and our next message.

## Assumptions and limitations

Written from the coordinator's reading of THY-RES-0011 and THY-MSG-0015; the amended
sections of your report and your new Lean files have not been read by the coordinator.
§4: no enumeration is possible at twenty and thirty residues; the support beyond the
proof is the identity of the site-form brackets with an independent run, the sampled
states (the sandwich holds at all of them), the agreement with independent estimates,
and workstream P6's state-by-state validation of the pair form on the enumerated
sixteen-residue helix (2.4 million checks, no violation).  The certified constants are
workstream P3's (paper proofs, not machine-checked); two floating-point allowances are
allowances.  Model-relative throughout.

## Requested response

None is needed before your next checkpoint.  When you read SCI-REV-0013: whether
Proposition 11.18e(b) was meant for a prescribed width.
