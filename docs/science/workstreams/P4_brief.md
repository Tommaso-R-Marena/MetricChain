# Workstream P4 — the theory division's share certificates and third-order pair form, tested on our real instances; a review of its Theorem 11.18a and Propositions 11.18b, 11.18c

*Brief written by the coordinator at checkpoint 41 (2026-11-26, about 01:55 UTC).  Read
`COMMON.md` first (its commit pins are out of date; what matters is below).*

## Why

The theory division's sixteenth checkpoint (`24a3c27`, THY-RES-0009 §1, §7) answers the four
theory requests of our workstream P2 (SCI-MSG-0015) and asks two things back:

1. "Test the share certificate of Proposition 11.18b(d) on your 13 instances (and on the
   polar and charged ones where the star fails): does a split of the deficits exist?"
2. "A review of Theorem 11.18a, Propositions 11.18b, 11.18c …, at whatever depth you can
   afford; 11.18b(b) and 11.18c are paper proofs."

## Where things are

* The theory tree at `24a3c27`, **read-only**:
  `/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_24a3c27/`
  — `docs/THEORY_REPORT.md` §11.7 (search for `Theorem 11.18a`, `Proposition 11.18b`,
  `Proposition 11.18c`), `docs/collaboration/responses/theory/THY-RES-0009.md`,
  `proofs/Frontiers/ThirdOrderModel.lean`, `ShareCertificates.lean`,
  `experiments/falsify_conjectures.py` (their harness blocks XI.16–XI.18), `docs/DEAD_ENDS.md` D57.
* Our measurement: `docs/science/workstreams/P2_REPORT.md` (the 13 instances are those in
  which the row-sum condition fails and the exact second-order criterion holds — find
  them in the report and in `experiments/science/ws_P2/out/`), `experiments/science/ws_P2/`
  (`anlib.py`: `load_fb`, tables; `data/fb_*_R3_t0.60.npz`: enumerated grids; `an_main.py`
  and the other analysis scripts).  Read-only for you; import them.
* Workstream P3 (`docs/science/workstreams/P3_REPORT.md`, `experiments/science/ws_P3/`): the
  certified sandwich at order `m` with *site* penalties `γ_i = (1/m)Σ_{T∋i}ĉ_T`.
* Your directory: `experiments/science/ws_P4/` (create it); your report:
  `docs/science/workstreams/P4_REPORT.md`.  Write nowhere else.  No state-changing git.

## What to do, in order of value

1. **The test they asked for.**  Implement Proposition 11.18b(d) exactly as stated (deficits
   `w_ij := max_{a≠x₀_i, b≠x₀_j}[c_ij − T_ij(a,b)]₊`, loads at most the single-site excitation
   energies `Δ_i` of the full energy; existence of shares = a maximum-flow feasibility
   problem — implement the flow yourself or with scipy, and verify every returned
   certificate by additions).  Run it on all instances of P2 for which the needed tables
   exist; report, per instance: row-sum condition (for the deficits), share certificate,
   exact criterion (the reference minimises the lower model — by enumeration or by P2's
   numbers).  **The headline is one table: of the 13 instances, how many does the share
   certificate certify?**  Then the polar and charged instances where the star fails.
   State precisely which `c_ij` you use (P2's enumerated class constants: measured, not
   certified) and which reference.
2. **Part (c) of the same proposition, and the pair form of Theorem 11.18a, on real
   constants.**  With P2's measured third-order constants `c_T`: the lower model with the
   site form `γ_i = ⅓Σ_{T∋i}c_T` against the pair form `γ_ij = ⅓Σ_{T⊇{i,j}}c_T` — on the
   enumerated instances compare (a) whether the reference minimises each lower model,
   (b) `ln Z` of each lower model against the exact `ln Z` (the cost number
   `Z(m)/Z(E) − 1` of the theory division's box-class formula), (c) the largest gap
   `max(E − m)`.  Is the pair form tighter in practice, and by how much?  Does a mixed
   allocation (an LP over shares) do better still?  Verify the soundness inequality
   `m ≤ E` at every state of every instance you run (it is machine-checked on products;
   a violation would be a bug in your code or a domain that is not reset-closed).
3. **Review.**  Re-derive Theorem 11.18a (a)–(d), Proposition 11.18b (a)–(d) and
   Proposition 11.18c (a)–(c) from the statements.  For each part: correct / correct with
   a repair / wrong (with a counterexample) / not checked.  Read the Lean statements in
   the two files against the report's wording (do not compile in the audit copy; if you
   want to compile, use `lake env lean <absolute path>` from `/home/user/MetricChain` on a
   *copy* of the file placed in your directory, and say whether its imports resolve
   against our tree, which is built on an older theory commit — if they do not, say so
   and review by reading).  Things worth an adversarial look: the completeness claim of
   11.18b(b) (max-flow argument; is "over-dense" the exact criterion for every alphabet
   size, as claimed — "the constants do not depend on the states, so the worst state of
   a site is its cheapest one"?); 11.18b(c) ("the exact criterion … when the measured and
   the known pair terms vanish"); 11.18b(d) "sufficient, not necessary" — find an
   instance of ours where it fails although the reference minimises the lower model;
   11.18c(b) "the largest reset-closed part" and whether P2's pruned domains are of that
   kind; the counterexample of 11.18c(c).
4. If time remains: does the *pair form at order `m`* tighten workstream P3's sandwich
   (shares of `ĉ_T` among sites and pairs)?  A statement and one enumerated instance.

## Rules

* Labels as in `COMMON.md`.  Every number with the script and the command that produced
  it; logs only from runs that reached their last line.
* Distinguish *independent review* (you re-derived) from *replication* (you re-computed
  with your own code) from *re-run* (their code).
* Homopeptides and the one patterned sequence of P2 only; no new sequences; nothing is
  optimised over sequences.
* Report structure as in the other reports: how far you got; verdicts (a table); precise
  statements; numerics with how to re-run; what you did not check; requests for the
  theory division that can be sent as they are.
* Budget: aim to finish within about ninety minutes; item 1 first and completely.
