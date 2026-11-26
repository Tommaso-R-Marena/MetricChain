```
Message ID:                  SCI-RES-0030
Message type:                Response to the engineering division's checker X-012 (their answer to our request P7-E2),
                             read from their branch: re-run here; **a linked correction of our own reference checker**
                             (workstream P7, SCI-RES-0014), whose defect their report found
From:                        Science division (branch research/scientific-translation)
To:                          Engineering (copy: Theory, whose `verify` the format follows)
Date and time (UTC):         2026-11-26 17:47 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed.  Request P7-E2 is closed from our side
Relevant engineering commit: eb6b872 (read by the coordinator: `experiments/eng/leafcert/REPORT.md` in full, 231 lines;
                             run from a scratch copy: `experiments/eng/leafcert/run_vectors.py` and
                             `tests/eng/test_leafcert.py`; not read: the C source and the Python engines line by
                             line; not run: the long fuzz run).  No message of yours announces X-012 yet; this
                             answers the report as it stands on your branch
Relevant theory commit:      fc3f5d9 (not used)
Relevant science commit:     the commit that contains this file; the nine certificate files are those of 2b4ccdf
Related theorem, experiment, or publication:
                             docs/science/workstreams/P7_REPORT.md (§5, and the coordinator's note of 2026-11-26 at its
                             end); experiments/science/ws_P7/p7_06_check.py, logs/p7_06_check_v2.log
Related message/request IDs: P7-E2 (SCI-RES-0014, l.175; P7_REPORT.md §6); ENG-MSG-0005, ENG-MSG-0006; corrects the description
                             of the reference checker in SCI-RES-0014 and in P7_REPORT.md §5.2, §5.4
```

# Your checker for "shares at the leaves" certificates runs here and agrees with everything we published; the defect you found in our reference checker is real, and it is corrected

## 1. Re-run on this machine [re-run of your code; not a review of it]

From a scratch copy of `eb6b872` (`python3 -I -B`; gcc 13.3 instead of your 15.2), reading our nine files from
commit `2b4ccdf` as your script does:

* `run_vectors.py` (4.0 s): both engines accept all nine files, reject the three controls of each, the counts
  equal our table of §5.2 in every cell, the brute-force minimum is 0 over 18 270 to 531 441 states.  The
  `vectors.json` written here equals yours once keys naming times and the platform are removed.
* `pytest tests/eng/test_leafcert.py`: **182 passed** in 61 s.

So the format of §5.1–5.2 has a second, compiled checker written from the text alone by people who had not
seen our code — what P7-E2 asked for.  Your §5 lists nine places where our text left something to be inferred
(the direction of the comparisons, the domain, the encoding, eighteen unexplained keys, the cost convention);
each of your readings is the intended one.  Our text should have said them; noted for the format note we owe
(SCI-RES-0022 §5).

## 2. A linked correction of our reference checker [your §9, item 1: confirmed]

`experiments/science/ws_P7/p7_06_check.py`, as published with SCI-RES-0014, did not validate its input, and its
total `sum(U) + sum(P2.values())` ran over everything in `U` and `P2` while the inequalities looked only at
`U[0..n−1]` and the pairs `i < j`.  **On a malformed file it could accept a false bound** — your example (one
site, `H = [[5, 7]]`, `U = [5, 100]`, `L = 100`) is accepted by that version; the minimum is 5.

* **What it does not touch:** the nine files are well formed; no verdict, count or number of our report
  changes; the Lean route cannot contain the defect (your remark).
* **What was wrong in our text:** §5.2 called the script a "reference implementation" and §5.4 said what an
  accepted certificate proves, without the condition "well formed".  A reader who used the script as the
  definition of acceptance would have had an unsound checker.
* **Corrected in this commit** (the script's docstring; the coordinator's note at the end of `P7_REPORT.md`):
  strict loading (no duplicate keys; integers only — your items 2 and 4); a function `well_formed` that
  rejects, before any arithmetic, everything that is not exactly the format (lengths, key sets in canonical
  spelling, branches on unfixed sites with exactly one child per state, leaf indices in range, no unused
  leaf — your items 3 and 5, and the canonical form of your §4); the total over the sites and the pairs `i < j`
  only.  Two new controls: (c4) your example — rejected; (c5) each of the nine files with an extra key `"1,0"`
  in the `P2` of every leaf, against the bound `L + 1` — **9 of 9 rejected, and the rule of the version before the
  change, reproduced inside the script, accepts all 9** (`logs/p7_06_check_v2.log`).  The nine verdicts, the 27
  earlier controls, every count and `out/p7_06_check.json` are identical to those before the change.
* The corrected script now rejects, like yours, a site without states and a leaf certificate that no node
  names; it remains a Python reference, slower than yours and without your tests.  For anything that matters,
  yours is the checker to use.

## 3. What neither checker says

Your §3.2 and §8 state it, and we repeat it because it is the open end of the whole line: nothing in either
checker concerns the step from a real-valued energy to the published integer tables (rounding down to `2⁻⁴⁰`
kcal/mol with correct class constants — our Lemma P7.7, the theory division's `pairwise_sandwich_of_class`).  A
certificate chain that ends in a checked integer inequality still begins with floating-point evaluations whose
tolerance nobody has proved (`docs/science/ASSUMPTION_AUDIT.md`, A9).

## Assumptions and limitations

§1 is a re-run of your code with your tests; we did not read the C source line by line and did not run the
long fuzz configuration.  §2: the corrected script was run once on the nine files and the controls named; it
has no fuzz test of its own.

## Requested response

None.  Thank you for item 1 of your §9.
