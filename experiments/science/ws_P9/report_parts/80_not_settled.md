## 8. Not settled; not checked; my own errors

### Not settled

1. **Nothing here is refereed or machine-checked, and no run by anyone else is part of it.**  Theorem R
   is P8's Theorem AH with its last step left out and P3's Theorem 3 with the increments it is
   stated with; Proposition P is elementary.  The brackets are outputs of the pipeline's modules
   fed with tables of mine through a driver of mine (requests P9-E1, P9-E2, P9-T1).
2. **The reductions are the bracket.**  With the window form of stage 2 the bracket of Lys₁₂ is
   the penalty-free width (0.0071 nats) plus 1–3 % at orders 4 and 5; for (LKSE)₃ likewise at
   order 5 (0.0167), and plus 14 % at order 4 (§4, §5.2).  What the band gives up — ten far pairs, the evaluated terms that do not fit a window —
   is now the whole certificate (request P9-E3).  I did not touch the reductions.
3. **When a floor delocalises** is not predicted by anything I have: first-order numbers on a
   sample of the true ensemble are right within 10 % wherever the floor stays at the anchor,
   and wrong by any factor where it does not (0.012 against 0.72; 0.07 against 1.31; 0.4
   against 659 for (LKSE)₃ at order 3).  The outcome of a model run is the only test I can
   offer (request P9-T2).  **(LKSE)₃ at order 3 is not certified** (§5.2).
4. **The slack that is left** in the resolved bound: at twelve residues it is still 8–15 times
   the exact term at its tightest state and several hundred times at the median state with
   four side chains off the anchor (§3.4); on the enumerated instances its Boltzmann mean is
   255–880 times the true remainder's (stage 1: `4·10³`–`3·10⁵`; P8's constants, by the
   coordinator's logs: `9·10³`–`4·10⁵`).  What remains is the sign-blind class (P5) and the suprema over hulls taken
   over all contexts — a context-resolved hull (the hull of `I_p` given the states of the sites
   of `T`, not over everything) is the next resolution of the same kind; not tried.
5. **Longer chains.**  No closed form over the subsets; 0.15–0.6 s per subset; the hybrid of
   request P9-E4 is not run; nothing beyond twelve residues was computed.
6. **Unequal weights beyond "one sub-tuple per subset".**  The window form puts the whole
   weight of a subset on one sub-tuple chosen by a product-of-marginals estimate from an
   uncertified sample.  The convex optimum over allocations (the coordinator's Frank–Wolfe
   at the site level, addendum A17 (17)) at the level of windows with state-dependent tables
   was not attempted.
7. **Other sequences.**  Serine (mobile, neutral): one order, six rows (§5.3); leucine not
   at all (two states per site: stage 1 has nothing to resolve there, stage 2 has).
8. **The sampler** (§5.4): one run per case, one seed; the Lys₁₂ order-3 run was not made
   (memory); a proposal costs 59 exact draws of the floor at `D = 0.017`.

### Not checked

* **No proof was machine-checked.**  I re-derived P3's Corollaries L1, L2 and Remark L3 from
  P3_REPORT §2.2 and P8's Theorem AH from P8_REPORT §3.3; I did not re-derive P3's Lemma 2
  (the multilinear interpolation argument) beyond reading it.
* **P3's interval enclosures, hulls, the table allowance `PAD_TAB` and the factor `1 + 10⁻⁹`** are
  inherited unexamined, as in every certificate of the division.  My only additions to the
  arithmetic: per-state increments (`PAD_TAB` added wherever P3's maximal increment is non-zero,
  so that the maximum over the states *is* P3's value — asserted bit for bit in the code), sums,
  products and maxima of non-negative doubles, and one more factor `1 + 10⁻⁹` on every table
  entry.  The rounding argument for that last factor is a sentence in §1, not a proof.
* **The stage-2 evaluation exists in one implementation.**  It is tied to P8's code by two
  identities (maxima of stage 1 = P8's block constants; stage 2 with maximal increments =
  stage 1, to `9·10⁻¹⁶`), validated block by block at every state of three enumerated instances
  (smallest ratio 1.0034), and at twelve residues by necessary conditions only (§3.4): every
  state with exactly three or four side chains off the anchor (orders 3, 4), 20 000 random
  states with exactly five (order 5, where no ball of radius 5 exists), and 2 000–2 500
  uniformly random states per peptide and order.
* **The sandwiches at twelve residues** were checked at 960 Gibbs states of the true ensemble
  and, for the forms named in the tables of §4, at 2 000 exact samples of the floor — not at
  every state.  On Lys₅ and LKSE:5 every sandwich was checked at every state, with the exact
  `ln Z` inside (87 sandwiches).  The probability statements of §5.4 are "given the two
  sandwiches", as in the coordinator's runs; the sampler's code is the coordinator's and I
  read only its docstring, `Envelope`, `inner_bounds`, `draw_q` and `main`.
* **The whole-function check has no power for stage 1** (§2): a stage-1 table wrong by a
  factor two would pass it.  Stage 1 rests on the block-level check and on "envelope ≤ table".
* **The "self-test" of my remainder routine is not independent** (§2).
* **The Gibbs samples are uncertified**; they guide the reductions of the models (as in the
  coordinator's runs, same seeds) and my choice of sub-tuples in the window form.  Validity
  does not depend on them; the numbers do.  16 chains in all, 120 sweeps each.
* **My chains with state-independent constants equal the coordinator's forms** to every printed
  digit of the brackets on Lys₅ (three runs).  At twelve residues only the coordinator's recipe
  itself was run as a model for P8's constants (rows "ref"); my chain was compared with it
  there as a penalty *function* at 5 000 random states per case (§4, agreement to `2.5·10⁻¹⁰`
  relative), not through a model, and the brackets of the rows "joint maxima of stage 2" have
  no second driver behind them.
* **One anchor per instance, the helix, P2's pruned domain, band 7, two twelve-residue
  peptides** (plus Ser₁₂ at order 5).  No other band, backbone or sequence.
* **At order 3 "P8's constants" are P8's code path run by me**; P8 stored no per-subset
  constants at that order for twelve residues, so there is nothing of P8's to compare with.
* **Scripts were extended between runs** (options added to `p9_05_brackets.py` — an explicit list
  of pairs, a fallback when P8 stored no constants — and a third check to `p9_06_check12.py`).
  The runs made before those edits were not repeated with the final scripts; the code they
  exercised did not change.  The library `p9lib.py`: its bound and table code was last changed
  at 10:54 (session record), before every table run; at 11:00 two functions were appended
  (`off_frequencies`, `window_form_const`: the window form with constants, used by the gain and
  bracket scripts only) — the table runs of Lys₁₂ at orders 4 and 5 and of (LKSE)₃ at order 5
  were started before that append and were not repeated after it; every bracket run was made
  after it; the validations and consistency runs were repeated with the final file.
* **Timings and memory** are single runs on a shared machine.
* **Prior art outside our own reports was not searched.**  Searched: P3 (`gfbound.py` line 110,
  `termwise.py` line 128), P5, P6, P8 (`p8sr.py`, `p8lib.py`, `x01_ff_proto.py`) for an evaluation
  with the actual increments — all take the maximum over the states of the non-host site; and
  addendum A17 (17), (18) for the allocation.  I claim nothing as new beyond "not in those".
* **Physical meaning.**  Everything is relative to the GBn2 model function on P2's rigid
  synthetic peptides; nothing here bears on water or on a real peptide.

### My own errors

{OWN_ERRORS}
