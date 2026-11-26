# Working files of the internal review ER1

The scripts and output files that the reviewer of `../ER1_internal_review.md` wrote in a
scratch directory, copied here unchanged by the division at the second checkpoint so that
the review's numbers do not depend on an ephemeral location.  They are **the reviewer's
evidence, not part of the division's checks**: `experiments/ensemble/run_all.py` does not
run them, and the division has not re-run them.  The counterexamples of findings F2 and
F14 are reproduced independently by checks R7 and R8 of
`experiments/ensemble/rigidity_checks.py`.

| file | what it is (see the review, §5) |
|---|---|
| `part1_checks.py`, `part1_e2_rescaled.py` | independent linear programmes for E1, E1.1, E1.2, E2, E2.1, E3 |
| `part2_e4.py` | E4 (exhaustive on small grids), E5, E6 |
| `part2_rigidity.py` | E7, E8, the non-generic twin on the line (F14) |
| `chimera_vs_identification.py` | the counterexamples of finding F2 |
| `part3_cube.py` | E9–E12 on small cubes; outputs `part3_out.txt`, `part3_cap.txt`, `part3_e10.txt`, `part3_e11_e12.txt` |
| `e12_star_certificate.py` | certificates supported on the pivot design of E12(b) (73 of 73 supports) |

The scripts need only numpy and scipy and are self-contained, except that
`part1_e2_rescaled.py` imports `part1_checks.py` from the same directory.  The reviewer
reports that one of them exceeded a time limit and was re-run in pieces.
