# The Hamming ball for randomised algorithms: checks for Proposition 11.18e(b′)

Nineteenth checkpoint of cycle 10.  The Scientific Discovery Division's review SCI-REV-0013 showed that our first
claim — randomised algorithms without a hint need as many evaluations as the Hamming ball has points — is false for
a bound of unspecified width, and asked whether it holds for a bracket of prescribed width.  That is a conjecture
(theory report Proposition 11.18e(b′)(ii)).  This directory holds the exact check of the combinatorial steps of an
outline that would prove `sup_g E|Q(g)| ≥ (1 − 2δ)(n + 1) − o(1)` on the cube at order two.

| file | what it checks | run time |
|---|---|---|
| `pairing_check.py` → `out_pairing_check.txt` | in exact integer and rational arithmetic, for random affine functions with widely separated coefficient magnitudes on cubes with 2 to 7 sites and 30 evaluation sets of `n` affinely independent points each (the first is the star without its last arm): the paired instance has the same values on the evaluated set; the pairing is an involution that flips one sign; the event "the minimiser lies in the affine hull of the evaluated set" never holds for both members of a pair; when it holds for one, the two minima differ by an amount of the order of the hidden coordinate; and its frequency under the prior is at most one half within noise for every set.  72 000 draws, 41 786 with separated magnitudes, no violation | 40 s |

What is **not** here: the analytic steps of the outline (the cutoffs of the prior, outputs that are right by luck,
`ln Z` against the minimum), adaptive strategies beyond the remark that the pairing is made transcript by
transcript, orders above two, alphabets with more than two states.  The harness tests of the proved parts are
XI.20 and XI.22.
