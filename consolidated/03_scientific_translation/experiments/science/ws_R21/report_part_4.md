## 4. Re-runs of their code (version 1, `a570520`) and what the scripts test (read only)

*Re-run.*  Their five `.py` files and their `output.txt` were copied to `experiments/science/ws_R21/rerun_copy/`
(sha256 of the copies = sha256 of the originals; recorded in `NOTES.md`) **after** my own code had run, because
`run_all.py` writes `output.txt` next to itself.  `cd rerun_copy; OMP_NUM_THREADS=1 python3 -I -B run_all.py`:
exit status 0, last line `ALL PASS`, 2 min 47 s (`logs/rerun_run_all_a570520_run1.log`).  `diff` of the new
`output.txt` with theirs: **identical except the three header lines with the timings** (41 / 113 / 13 s here,
39 / 102 / 17 s there).  So every number of §3.3 that comes from `output.txt` is reproduced: R1 (ranks and
connectivity of eight matroids), R2 (1 240, 2 904, 20 440, 79 998 splices; smallest Cayley–Menger determinant
`1.6·10⁻³`), R3 (`6.0·10⁻⁴`, `2.7·10⁻¹⁵`), R4 (40 of 40, 31 realised), R6.

*Re-run with other seeds* (`rerun_seed_sensitivity.py`: their functions `test_R5` and `test_R3`, unchanged, with
only the line that sets the seed replaced; `logs/rerun_seed_sensitivity_run1.log`, 11 min 20 s).  `test_R5` with
seeds 1–20: **passes with 17, fails with 3** (seeds 6, 7, 8: one conformer is never reached by the 400 starts);
in five of the passing seeds one conformer is reached one to three times; in none of the 20 is a zero found
away from the conformers.  `test_R3` with seeds 1–4: passes four times (smallest residual over the 180 sampled
splices `5.9·10⁻⁴`–`9.3·10⁻³`).  So R5 supports E8 where its control passes, and its control is unreliable; R3
is stable as far as it goes (remark 2).

*Read only* (`rigidity_checks.py`, 240 lines, read in full; of the other scripts I looked only at imports and
file operations).  Five remarks, all minor:
1. **R5 — the report and the output disagree.**  Line 502: "all 22 zeros of the certificate `f` found from 400
   starts".  Their `output.txt`, and my re-run: "82 zeros found in 400 starts; 1 at conformer 1, 81 at conformer
   2, 0 elsewhere".  The number in the report is stale.  More important: the check's own control — both
   conformers must be reached — is passed by **one** hit.
2. **R3 — a threshold that true negatives cross.**  Their "wheel `W_5`" has five spokes (six vertices; it is the
   graph called `W_6` in §3 of this report).  R3 examines 180 random splices of three pairs, two conformers only,
   and passes if the smallest residual exceeds `10⁻⁶`.  On that graph, over *all* 1 022 splices, I find `4·10⁻⁶`
   in one of ten random pairs, and for three conformers `8·10⁻⁷` and `1.2·10⁻⁹` (§3) — values of true negatives.
   The check passes because it samples; with all splices, three conformers, or more pairs it would report
   failures that are not chimeras.
3. **R3, R5 — no control of the search on things that exist.**  The solver is checked on one conformer per pair
   (R3) or by the two conformers (R5).  With my code a random start realises a *realisable* length vector of
   that wheel in one case out of three, and for the hardest per cent of targets in about one start out of
   thirty; 25 starts are then not evidence of absence.  A planted control (lengths of fresh random frameworks)
   and an exhaustive method (the graph has a ruler-and-compass order) would make R3 a test.
4. **R4(b)** tests one colouring (the `K_4` block from `x_1`, both pendant edges from `x_2`) against the two-circle
   criterion; the other five block-constant colourings of each pair are not examined (in my T3(a): 160 of 240
   are realised).
5. **R6** (two toy feature maps) is in the script and in `output.txt` but not in the text of §3.3, which lists
   R1–R5; the register cites it for E5(a).
