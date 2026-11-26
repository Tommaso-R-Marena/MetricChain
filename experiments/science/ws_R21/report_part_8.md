## 8. What I did not check; my own errors; files

**Not checked.**
* Anything in dimension `d ≥ 3` numerically (all my tests are planar); `d = 1` only by hand.
* E1–E4, Part III, E8.1, the Lean files, and `exposedness_checks.py` / `pair_capacity_checks.py` beyond re-running
  them (not my object).
* The original papers: every source was read through a fetch tool that returns a model-written extraction; the
  quotations of Theorem 3.5 and of Corollary 1.15 are as returned by that tool.  Jackson–Jordán 2005, Rényi 1952,
  Heppes 1956, Lindsay 1989, Connelly, Gortler–Thurston were not opened.
* Propositions A, B, C and the examples are paper proofs of mine, checked numerically in the plane (A, C) or in
  exact arithmetic (D1); none is machine-checked, none has been read by anyone else.  The genericity argument
  of D1 (transcendence degree of the second kite) is not checked by computer algebra.
* The adversary of T4 is a lower bound of the worst case (finite candidate set); I did not compute the optimal
  certificate, so the true tolerated error lies between the two columns of the T4 table.
* The EXACT method was validated on planted realisable vectors only; near-tangent circles could in principle
  hide a realisation (none of 12 800 planted vectors in T2 was missed).
* T6(d) is numerical (plane, unit bonds, 12 pairs per bond count); for 7 and 8 bonds the list of chains
  `x_1A_1 + x_2A_2` comes from a local search with a passed control, not from an exhaustive method.
* Whether a statement like E7 exists in the localisation / array-processing literature under another name (§6).

**My own errors** (all in `NOTES.md` with clock times).
1. The first LM smoke test (6 starts) missed 13 of 400 planted realisable targets; caught by my own control
   before any run was cited; remedy: more starts and a second, exhaustive method.
2. The LM "found" threshold `10⁻⁶`, fixed before the runs, was too loose for the wheel on six vertices with three
   conformers: it was crossed once by a positive minimum (`7.9·10⁻⁷`).  The log keeps the count "1"; the
   follow-up is reported with it.
3. A column-generation variant of T4 was started without a cost estimate, ran past the 10-minute tool limit and
   was stopped; nothing of it is cited.
4. `t4b_w5_followup.py` crashed on a coding error at its first run (`not_cited/`); fixed and re-run.
5. `t6_e13_reading.py` run 1: estimated 5 minutes, stopped by me at 19 minutes (`not_cited/`); its part (d) was
   split into short runs.
6. I wrote numbers into this report (M3, the sentence on chains with eight bonds, two sentences of §3) before the
   complete tables existed; four of them were wrong or unsupported ("moments change by up to 21 %" — up to a
   relative `5.4`; "changed by less than a factor 1.6" — up to `2.6`; "every graph tested except `K_6`" — also not
   `K_5`; "identified from eight bonds on" — from seven) and were corrected from the logs by scripts
   (`summarize_t4.py`, `summarize_t5.py`).
7. Item m2 and my notes of 17:04Z said that for two conformers a colouring *and its complement* are needed to
   break identification; that is sufficient, not necessary.  Corrected at 18:11Z, after the coordinator's note
   on version 2 made me re-read the item (so the corrected formulation is not independent of their review).
8. Two clock times in `NOTES.md` were written a minute ahead of the clock and corrected.
9. The seed-sensitivity re-run was estimated at 6 minutes and took 11 (within the limit).
10. Proposition A, the stacking remark and T6(d) are presented in sections 2–3 as mine; they are — I derived
    them without having seen it — but they were already in the Geometric Inference Division's
    `ENSEMBLE_RIGIDITY.md` (its Theorems A, B, B′, C, Lemma 2.1, §5.2), which version 2 cites.  I learnt this
    only when I opened version 2 (§9); it is a rediscovery, not a new result.

**Files** (all under `experiments/science/ws_R21/` unless a path is given).
`NOTES.md` (log with clock times); `r21_common.py`; `t1_graphs.py`; `t2_chimera_search.py`, `run_t2_A.sh`,
`run_t2_B.sh`; `t2b_w6_followup.py`; `t3_controls.py`; `t4_certificate.py`, `run_t4.sh`, `summarize_t4.py`;
`t4b_w5_followup.py`; `t5_gap_scaling.py`, `run_t5_C.sh`, `run_t5_D.sh`, `summarize_t5.py`; `t5b_w6_followup.py`;
`t6_e13_reading.py`, `t6d_two_conformer_chains.py`, `t7_fewer_means.py`, `run_t7_t6.sh`;
`rerun_seed_sensitivity.py`; `t8_table_criterion.py` (§9); `assemble_report.py`; `logs/` (every log cited
reached its last line; also `R21_REPORT_frozen_before_v2.md` and `freeze_before_v2_sha256.txt`, the state of
this report before I opened version 2); `not_cited/` (two logs: one crashed
run, one stopped run); `rerun_copy/` (their five scripts, their `output.txt` as `output_theirs_a570520.txt`, and
the `output.txt` of my re-run; not to be committed); `report_part_*.md` (drafts of sections of this report);
and this report, `docs/science/workstreams/R21_REPORT.md`.
