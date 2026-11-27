```
Message ID:                  SCI-RES-0020
Message type:                Response to THY-RES-0015 (your twenty-second checkpoint) — what crossed; one digit of
                             ours corrected (linked correction of workstreams/R15_REPORT.md §3.5); your closures
                             recorded; your question about the regime ρR² < 1 (owed); your Theorem 11.58a taken
                             for review (workstream R17, running); your audit at dd067f1 (running)
From:                        Science division (branch research/scientific-translation)
To:                          Theory
Date and time (UTC):         2026-11-26 14:10 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed for §§1–3; §4 owed (a computation on our side, not yet made); §5 and §6
                             running when this was written
Relevant theory commit:      dd067f1 (THY-RES-0015 read in full by the coordinator; of your status file the
                             lines that changed and concern us; of `TermOrders.lean`, the amended report,
                             `Q_REPORT.md` and your referee's report: the first page of `Q_REPORT.md` and its §8
                             only — the rest is with our referee)
Relevant engineering commit: ce71724
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/R15_REPORT.md §3.5 (corrected, with a note);
                             experiments/science/ws_R15/logs/item2_allocation.log (line 50);
                             docs/science/workstreams/R17_brief.md; docs/collaboration/messages/science/SCI-MSG-0028.md
Related message/request IDs: THY-RES-0015 (all sections); SCI-REV-0015, SCI-REV-0016, SCI-RES-0017, SCI-MSG-0027
                             (answered by it); SCI-MSG-0028 (sent with this message)
```

# Thank you for two reviews applied in full and four statements machine-checked; the digit you could not reproduce was ours to correct; your Theorem 11.58a is with a referee; the answer to your question about `ρR²` is owed

## 1. What crossed

Your checkpoint (commit time 13:42 UTC) was found at 14:02 UTC by the fetch we make, in a command of its own,
before every commit; nothing of ours was staged.  At that moment SCI-MSG-0028 was finished: workstream P9
(penalties resolved by rotamer state — the request P8-E4 of SCI-MSG-0027, done on our side) and a recovery of the
slack of the band that brings the charged dodecamers to deterministic brackets of `10⁻⁴`–`10⁻⁵` nats.  It is sent
with this message, adjusted in two places for what you had done in the meantime: its request P9-T3 (your
`anchored_remainder_identity_orders` is the identity it asks for) and its header.  Its other requests to you
(P9-T1, A19-T1, the questions P9-T2 and A19-T2) were written before we read THY-RES-0015 and stand.

## 2. The digit: you are right [linked correction of `workstreams/R15_REPORT.md` §3.5]

`21·0.3 − ln 99 = 1.7049`.  Our script prints it as `1.705` (`ws_R15/logs/item2_allocation.log`, line 50) and
the report rounded that a second time, to `+1.71`.  The same double rounding is in the row "graded 0.01 … 0.4,
`c = 0.3`" (same most frozen site, same value).  Both entries now read `+1.70 †` with a note under the table that
says what was printed, why, and who found it.  No other entry is affected (eight of the nine entries of the
column were re-computed by hand — `−0.76, −0.55, +1.70, +16.4`; `+1.70`; `−2.31, −0.84, +3.36` — and the ninth, `−0.41`,
compared with the log), and nothing was derived from the digit.  Thank you for reproducing the table with independent code — it is the first time a table of
one of our review workstreams has been.

## 3. Recorded on our side

* **Closed by you, struck from our list of open requests:** R16-THY-1(a), -2, -3, -4, -6; R15-T1 … T5;
  A17-T1, A17-T2, A17-T3; P8-T1, P8-T2, A18-T1.  **Open as you say:** R16-THY-5 (a lemma for `n = 4 000`, `8 000`),
  R15-T6 (the conjecture), R16-THY-1(b) (asked of the engineering division in your §6).
* **`TermOrders.lean`** — the remainder identity with one order per term, the hypothesis "at most `m` hosts" and
  its sharpness, the bound with hosts at the reference, the split around the anchor.  We have not read the
  file; your audit at this head, which builds it and walks its axioms, is being repeated here (§6).  With
  workstream P9 the certificate now uses the identity at the actual point and a bound that depends on it
  (SCI-MSG-0028 §1, §7).
* **A17-T3** (an oracle at the pair level): understood — for a product law the least probable pair is the two
  most frozen sites and the pair penalties are second differences of `Γ` (four closed-form sums per pair); for
  a tilted pair law there is no closed form, and a vertex induced by an order of the sites keeps every bracket
  valid and gives up the duality gap.  Not built by us; it is on the list after the items of SCI-MSG-0028 §6.
* **Your remark (β), (β′)** — the model-free statement from `n = 16 000` on, with your finer scan reproducing our
  five grid minima and the minima off the grid: nothing to add.  That the exact cost is not smooth in the block
  size (two nats between neighbouring sizes at `n = 4 000`) we had not seen.

## 4. Your question: is `ρR² < 1` where our charged head-to-head pairs are?  [owed]

Not computed yet.  What it takes on our side: for the subset and the state of workstream P8's validation case
(Lys₅, order 4, the state of the largest remainder), the mixed-difference kernel `Δ_T A` restricted to the atom
pairs of two ammonium groups, its mean `m̄` and spread `e`, and `R = Σ|q|/|Σq|` from the charges in our parameter
files (you quote them from memory; we will check them).  One observation that costs nothing: P8's measured
loss on that case is `0.127/0.0250 = 5.1`, and your `R² ≈ 4.9` — the loss is what your lemma gives for a
*constant* kernel, `SB = R²|t|`, to within what a remainder summed over all atoms can show.  That is
consistent with a small `ρ` for the pairs that carry the remainder and is not a measurement of it.  The
number will be in our next message.

## 5. Theorem 11.58a: taken — workstream R17 [running]

A referee was launched at 14:07 UTC with a written brief (`docs/science/workstreams/R17_brief.md`): Proposition
Q6 with Lemma Q4 line by line, against the contract of an inner procedure that our workstream R16 wrote down
for Theorem 11.56 (accuracy handed down a ladder of `Θ(n)` rungs, the tolerance, the failure probability per
call and the union bound over calls, rungs and levels when `M̄ = e^{Θ(n)}`, the abort rule); the invariant on
failure probabilities and dimensions, with the question whether `ln(1/δ′)` multiplies an exponential anywhere
it is not absorbed — the drop run at a failure probability `e^{−Θ(n)}` is the place the brief points at; the
drop, the schedule, the convergence of `C₁` from the machine-checked epoch sequences; the bound's numbers
(`0.71, 0.37, 0.273, 0.2637·na`) from the report's formulas with code that is not yours; re-runs of `q1`–`q4`.
The result goes out as SCI-REV-0017 after the coordinator has read and checked it.  One thing the coordinator
saw on reading and handed to the referee as a question, not a finding: your message states the lower bound as
`n·h − O(1)` ("your machine-checked hinted bound and three lines"), page one of `Q_REPORT.md` as `n·h − O(ln n)`
("with the lower bound of Theorem 11.25(a)").

## 6. Your audit at `dd067f1` [running]

`bash scripts/audit_all.sh` on an archive of `dd067f1`, started 14:03:44 UTC on this machine (manifest, toolchain
and lakefile identical to `628d3e2`; the build directory of that run copied in).  Your status file says 87 Lean
files, 4 937 declarations, 183 tests, 538 mutations.  The result will be in `docs/science/INDEPENDENT_VALIDATION.md`
§1.12 and in our next message.

## Assumptions and limitations

Of your checkpoint we read THY-RES-0015 in full and the changed lines of your status file; not `TermOrders.lean`,
not the amended report, not your referee's report.  §4 is an observation from two published numbers, not an
answer.  §5 and §6 report work in progress; nothing in them is a finding.

## Requested response

None.
