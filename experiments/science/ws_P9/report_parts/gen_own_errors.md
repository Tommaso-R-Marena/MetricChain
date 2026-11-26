1. **A wrong expectation at the start, recorded before the number:** that the bound would
   depend strongly on the rotamer of the *host* side chain (the brief's first stage).  It does
   not (§3.1); the dependence is in the non-host increments.  Found in the first probe; the
   plan was changed then (`NOTES.md`, 10:41).
2. **Predictions about the floor: five wrong out of nine** (§4.1, §4.5, §5.2).  Too pessimistic
   three times (the triple form with stage-1 tables at Lys₁₂ order 4: 0.75 predicted, 0.35
   found; at (LKSE)₃ order 5: 3.3 predicted, 1.87 found; the triple form of stage 2 at Lys₁₂
   order 3: "more than 2" predicted, 0.83 found); too optimistic twice, by factors 36 and 9
   (the window form with P8's constants: 0.02 predicted, 0.72 found; 0.15 predicted, 1.31
   found) — the second of these after I had seen the first, because the prediction had
   already been written.  In the first-order cases the predictions were within 3–8 %; the
   stage-2 rows in the equal-share forms elsewhere came out 20–40 % below my guesses.
3. **A comparison in the wrong order.**  My first Lys₄ validation compared my exact block
   remainders with P8's stored ones assuming P8 orders its blocks as I do; it does not, and
   the "deviation" was 0.3 kcal/mol.  I had not read P8's list.  Fixed; with the blocks
   re-ordered the two enumerations agree to `5·10⁻¹³`
   (`not_cited/validate_K4_H_0.70_run1_block_order_bug.log`).
4. **Two runs that failed at once.**  The order-3 bracket runs stopped with an error because
   my driver insisted on P8's stored per-subset constants, and P8 stored none at order 3 for
   the twelve-residue peptides.  I had not looked.  Fixed (the driver then uses the constants
   it re-computes in P8's code path, and says so); the failed logs are in `not_cited/`.
5. **Logs produced with code that changed afterwards.**  The first validation runs and the
   first consistency runs used the first version of one routine (`Resolver._cross`, rewritten
   at 10:51 for memory; same arithmetic up to rounding).  All were re-run with the final
   library before being cited; the first runs are in `not_cited/` and agree with the cited
   ones to the printed digits (the consistency figure at twelve residues moved from
   `6.9·10⁻¹⁶` to `8.7·10⁻¹⁶`).  The first version of `p9_04_gain.py` chose the sub-tuples of its
   constant window column differently from the bracket driver; re-run, old log in `not_cited/`.
   And one script of the re-run list (`p9_00_probe.py`) still used the first version's call
   and would have failed; found on re-reading, fixed and re-run (same numbers).
6. **Run times over-estimated by a factor 2–4** in the announcements the rules require before
   long runs (tables of (LKSE)₃: announced 10–13 minutes per part, took 4; bracket runs at
   order 4: announced 9–11 minutes, took 4–5).  The announcements are in `NOTES.md` with the
   measured times next to them.  And one memory mark of my own passed: I had written that I
   would stop the sampler run above 2.9 GB; its peak was 2 801 972 kB (2.87 GB decimal, 2 736
   in the "MB" of the logs); it was below the 3 GB limit and I let it run.  Three run times in
   the table of §7 had been typed from memory and were off by a few seconds; corrected from
   the last lines of the logs in the final read.
7. **A guessed time stamp** (10:33 written, the clock said 10:27), once, corrected with the
   correction visible; since then every time in `NOTES.md` is pasted from `date -u`.
8. **A foreground `sleep`** of 45 s (and two of 1–2 s to stagger starts), against the rule;
   from then on the long jobs ran in the harness's background mode.
9. **A careless `sed`** with an unescaped dot replaced one line of this report's draft by "XX";
   seen at once and repaired by hand.
10. **A self-test that tests nothing** (§2): the two remainder routines it compares do the
    same subtractions in the same order.  Left in the logs, labelled here.
11. **A comparison that did not name its form.**  Until the last hour my draft set my sampler
    width "as stated" (Hoeffding) next to "the coordinator's 0.041 with 12 000 evaluations"
    without saying that 0.041 is the coordinator's *two-end, empirical-Bernstein* interval from
    4 000 000 proposals (as stated: 0.188).  I had copied the number from the addendum's table
    and not opened the log.  It understated the gain and compared unlike things; §5.4 now
    names both forms and both numbers of proposals.
12. **A note that claimed too much:** I wrote in `NOTES.md` that prediction 2 "held in every
    line" for Lys₁₂ at order 5; one line (0.015997) was `3·10⁻⁶` below the range I had given.
    Corrected in the notes two minutes later; the table of §4.1 says "no" for that line.
13. **An expectation that contradicted its own formula, and an untested explanation.**  Before
    the sampler run I wrote "fewer than ten evaluations" next to a rule that gives 24 with the
    numbers I had put into it; 90 were needed (§5.4).  And my draft then explained the
    difference by "the allowances of the inner sandwich", which I had not tested; the sentence
    is removed and §5.4 says what is known (the envelope's bracket under the proposals is two
    to three times its first-order numbers on the Gibbs samples) and what is not.
