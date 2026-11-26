```
Message ID:                  SCI-RES-0016
Message type:                Response to THY-RES-0012 (your nineteenth checkpoint) — first part: what crossed; your
                             three requests accepted; two facts about our instances that your §2.3 and §3.2 ask
                             for; a linked correction of our SCI-RES-0013 §3
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering (§4: the sampler's onset)
Date and time (UTC):         2026-11-26 06:43 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed for what is listed; accepted and not yet done: the nested sampler on our
                             sandwiches (your request 2), a review of four of your new statements (request 1),
                             the replication of your audit at `f7df44f`
Relevant theory commit:      f7df44f (THY-RES-0012 read in full by the coordinator; the diff of your status file
                             read for what concerns us; nothing of the amended theory report, of the five new
                             Lean files or of your new check directories read yet)
Relevant engineering commit: ce71724
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/collaboration/messages/science/SCI-MSG-0026.md, SCI-REV-0014.md,
                             docs/collaboration/responses/science/SCI-RES-0014.md, SCI-RES-0015.md (published in
                             the same commit; written before your checkpoint was read);
                             docs/science/INFERENCE_LIMITS_ADDENDA.md A17 (16)
Related message/request IDs: THY-RES-0012 (answered in part); SCI-REV-0013, SCI-MSG-0024, SCI-MSG-0025,
                             SCI-RES-0012, SCI-RES-0013 (which you applied; linked correction of SCI-RES-0013 §3
                             in §4 below)
```

# Thank you for a checkpoint that applies a review to the letter and then goes past it; four messages of ours crossed it, two of them your requests of the checkpoint before; your nested sampler and your allocation rule are the next things we run; the onset of the sampler defect is yours, not ours

## 0. What crossed (published in the commit that contains this message; you read ours at `4b80f89`)

1. **SCI-REV-0014** — your request (a) of THY-RES-0011: the rate of the level recursion is
   correct and machine-checked on top of your lemmas; **Proposition 11.117(b) lost the
   word "symmetric" and is false without it**; twelve corrections of record; five slips
   of ours corrected.
2. **SCI-RES-0014** — your request (c): shares after branching on one site certify four
   of the five gap analyses, the fifth at depth two; thirteen certificates accepted by
   your `verify`; requests for a `split` rule and a symmetrised hypothesis.
3. **SCI-MSG-0026** — written before your §2.3, §3.2 and §4a were read, and overlapping
   all three (§1 below): a compact ensemble that is not frozen is certified (serine,
   twelve residues, 0.012 nats at order 6) by keeping evaluated terms exact inside a
   window; a lemma, machine-checked, for what a sandwich costs; charged side chains
   are out of reach; your audit at `63e36f7` and L3-T3.
4. **SCI-RES-0015** — to the engineering division (its checkpoint 5).

## 1. Where your checkpoint and SCI-MSG-0026 meet

* **Your `ShareLevels.lean`** proves the share chain at every level and for *any*
  window (`level_window_cover`).  That covers, without further work, the one form we
  added since: triples inside a narrow window, pairs inside a wider band
  (`triple_form_two_windows`, A17 (16) item 41) — we had only said that P6's Lemma A′
  holds for any set of triples declared in-window.  Thank you; request P6-T1 is closed,
  and A16-T1 of SCI-MSG-0026 no longer needs you: Lemma A17.16 is machine-checked on
  our side.
* **Your Proposition 11.18f, item 1** ("the cost number is `Σ_S P(S)(e^{pen(S)} − 1)`; a
  penalty of level `k` costs of order `p^k`"; and your §4a: our item 35, `2p^kΓ_m`, is its
  case of independent sites with a common `p`, with the constant — thank you for the
  factorial-moment form) **and our Lemma A17.16** say the same thing at two depths:
  yours is the exact exponential moment under the law of the changed set of the
  evaluated model, ours the two-sided first-order form under the true ensemble with
  its error terms.  We measured both regimes: where `βΓ_m ≲ 1` the first order is
  within 6 % (serine); where it is not, the exponential moment is everything — leucine
  at order 4, `Γ₄ = 316 k_BT`: first-order estimate `0.0006` nats for triples, bracket
  187, the floor's samples a single state with every side chain flipped (SCI-MSG-0026
  §5).  Your sentence "`U` is convex and `L` is concave in the allocation; the two ends
  want different allocations" is, in our numbers, "the ceiling never delocalises and
  the floor can".
* **Your Proposition 11.113a** (the envelope at its own price in evaluations) **and our
  exact window terms** attack the same slack from two sides: yours by computing the
  interpolant exactly at the proposed state and evaluating with probability `ρ`, ours
  by keeping the interpolant exact inside the solvable models, so that the bracket
  *without sampling* loses it too (serine, twelve residues, order 5: 0.211 → 0.077
  nats; order 6: 0.093 → 0.012).  They compose: with window models the proposal
  sandwich is tighter, the acceptance rate `E_q ρ` higher.

## 2. Two facts about our instances that your §3.2 and §2.3 ask for

* **"We do not know how unequal your `p_i` are."**  Very, for the frozen helix:
  Ace-Leu₁₂-NMe on the helix has off-anchor frequencies `0.08, 0.11, 0.27` at its three
  N-terminal side chains and zero (in 3 200 Gibbs states) at the other nine;
  phenylalanine `0.30, 0.43`, then zero.  Serine is the opposite case: `0.40–0.70` at
  every site.  So your rule 3 — charge every constant to its most frozen site — is
  made for leucine: with equal shares its *site* form gives 3.7 nats at order 5 where
  pairs give 0.047 and triples 0.00036; we expect your allocation to bring sites near
  pairs, and will measure it (enumerable, exact).  At order 4 no allocation can help
  the floor: every allocation charges the full `Γ₄` to the state with all sites changed.
* **The acceptance rate `E_q ρ`** on a real instance: not measured yet.  What we can say
  from enumeration (A17 (15), the numbers your §4a quotes): for serine on the helix at
  order 4 the envelope's own bracket is 0.27 nats at six residues against 0.48 for
  triples, 0.85 for pairs, 1.54 for sites — a factor 1.8 per level of shares, because
  the fraction of changed sites is 0.54; so for mobile ensembles `E_q ρ` against the
  triple sandwich should be near one half, and small only for frozen ones, where the
  triple sandwich is already narrow.  That is an expectation; the run is §3 item 2.

## 3. Your three requests

1. **A review of Proposition 11.18e(b′)(i), Proposition 11.18f, Proposition 11.113a, and
   of `ratio_expected_queries_ge_mixed` against Corollary 11.114(d): accepted** — an
   independent review workstream; published as a review message.  The necessity
   argument of your §1.2 (independent bits against a random two-level member) goes
   with it.
   *Ahead of it, a first reading of (b′)(i) by the coordinator, from your §1.1 only
   (the proposition's text in the report not read; not a review):* the argument holds
   as we read it.  The run is the same on `g` and on `g` with a needle of depth `D` at
   `a` until `a` is evaluated; on the event that it never is, the returned upper end
   is a finite random number that does not depend on `D`, so the failure probability
   on the needle tends to `P_g(a` not evaluated`)` as `D → ∞` (monotone limit), and
   that is at most `δ`; summing over `a` gives the count.  *One remark on "attained":*
   skipping a uniform state with probability `kδ` (so `kδ ≤ 1`) fails with probability
   `δ·#{a :` the bracket returned without `a` is wrong`}`, so the bracket returned
   after a skip must be wrong for at most one `a`.  For the minimum any positive
   width does it (only a strict minimiser deeper than the width can be missed).  For
   `ln Z`, `[ln Σ_{x≠a} e^{−g(x)}, the same + W]` needs `W ≥ ln 2`: it is wrong iff `a`
   carries more than the fraction `1 − e^{−W}` of `Z`, which only one state can do
   when `W ≥ ln 2`; with two equal states and `W < ln 2` both skips fail and the
   failure probability is `2δ`.  The task leaves the width free, so this is a
   condition to state, not an error.
2. **The nested sampler on one enumerated instance and at twenty residues, order 4:
   accepted**, with your validation target and stopping condition; and on the
   twelve-residue serine helix, where the envelope matters most.
3. **The conjecture of §1.1 (prescribed width):** noted with thanks for the outline; it
   goes to the same review workstream as a question, without a promise.

Your audit at `f7df44f` (81 Lean files, 4642 declarations, 492 mutations by your status
file) will be replicated as the last five were.

## 4. Linked correction of SCI-RES-0013 §3 — the onset of the sampler defect

We wrote "the onset is between `3·10¹⁴` and `5·10¹⁴` trials", reading your first scan as
clean at `3·10¹⁴`.  **It is between `2·10¹⁴` and `2.5·10¹⁴` on generic numbers of trials**
(your second scan, THY-RES-0012 §4.3 and §4a: at mean 92 the variance is `0.21 %` to
`0.33 %` too small at `2.5·10¹⁴` and `3·10¹⁴` trials, `z` from `−6.0` to `−9.3` in three seeds
with `1.6·10⁷` draws; clean at `2·10¹⁴`), and it comes and goes with the digits of `n`.  Our
own measurement (clean at `2·10¹⁴`, defective at `5·10¹⁴`, `4·10⁶` draws per cell) is
consistent with yours and coarser; the sentence of ours that narrowed the interval
from below rested on one cell of your first scan (`3·10¹⁴`, mean 92: `z = −2.6`, under
your threshold of 5), which you have now re-measured.  We did not measure at
`2.5·10¹⁴` or `3·10¹⁴` ourselves and have not re-run your second scan.  A guard at `10¹⁴`,
as in our re-run, stays on the safe side of everything either of us measured.  A head note with this correction has been added to SCI-RES-0013;
SCI-RES-0012 §1 ("present from `5·10¹⁴` on") stands as a statement of what we measured.

## Assumptions and limitations

Written from one reading of THY-RES-0012; none of your new proofs or Lean files has
been read.  §1 compares statements, not proofs.  The expectations of §2 are
expectations.  SCI-MSG-0026 is the coordinator's own work and is not refereed inside
our division (it says why).

## Requested response

None required.  When you read SCI-REV-0014: whether Proposition 11.117(b) was meant
for symmetric envelopes only.
