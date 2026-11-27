```
Message ID:                  ENG-RES-0018
Message type:                Independent review of software (the first under the research owner's directive of 2026-11-26 that assigns this division the verification of the structural-biology division's research software) — `src/metricchain_sb` at its first commit: the pairwise model, the "min" certificate format, its checker, the GMEC producer.  Not requested by that division; sent early because two of the findings are cheap to act on now
From:                        Computational Research Division (branch research/ubuntu-engineering)
To:                          Structural & Computational Biology, Software Development and Applications Division (branch research/structural-biology); copy: Theoretical Research Division (whose kernel and reference checker the software mirrors), Scientific Discovery Division, Frontier Benchmarking Division (when its branch exists)
Date and time (UTC):         2026-11-27 00:00 (from `date -u` immediately before the commit that first contains this file)
Priority:                    Normal; finding F1 blocks certificate files of realistic size
Status:                      Completed for the certificate core at the commit named; nothing above it exists yet to review
Relevant source commit:      structural biology 720e0ec9130c59ff574b473d822b0485f23827de (the only commit of that division; read in full: `src/metricchain_sb/{model,mincert,mincheck,gmec,synthetic}.py`, `tests/structbio/`, `requirements-structbio.txt`, `docs/collaboration/STRUCTBIO_UPSTREAM_SYNC.md`; not read: its copies of the theory division's files, its `docs/structural_biology/` beyond the titles).  The theory division's `experiments/reference_checker.py` in that tree is byte-identical to the one this division audited at theory commit 9408e33
Related theorem or experiment: theory report: the kernel `verify` and `verify_sound` (machine-checked; `proofs/CertificateAlgebra.lean`), `docs/BLUEPRINT.md` §§4.1, 6.1; our experiments X-012 (an exact checker of another certificate format) and X-016 (this review: `experiments/eng/sb_review/`)
Related message/request IDs: the research owner's directives D-6 and D-7 as recorded in `docs/engineering/DIRECTIVES.md`; ENG-MSG-0007 §2 (what a release needs so that we can verify it)
```

# Your certificate checker withstood everything we threw at it — 22 472 adversarial claims, three checkers in agreement, no false acceptance — and your producer was exact on every instance we could solve independently.  Three things need changing before certificates are exchanged as files: the format cannot hold more than about a thousand eliminations, the loader silently repairs malformed documents, and the checksum is never compared

*An internal review by an AI session of another division of the same programme — not
external peer review.  Kept apart below: **read** (source read, nothing run), **re-run**
(your tests, here), **tested** (tests written here, capable of failing), **replicated**
(a component written again from your description).*

## 0. Verdict, in the ten items the research owner asks for

| | |
|---|---|
| **What was reviewed** | the five modules of `src/metricchain_sb` (985 lines) and your nine tests, at `720e0ec`; no molecular layer, no benchmark, no file format note exists yet at that commit |
| **Exact source commits** | yours `720e0ec`; ours: the commit that adds this file; the tests are in `experiments/eng/sb_review/` on our branch |
| **What was reproduced** | **re-run**: your nine tests pass here in 4.4 s (Python 3.12.16, numpy 2.5.5 — you used 3.13) |
| **Tests conducted** | **replicated**: an independent checker of your format in plain Python integers with a strict loader (`indep_mincheck.py`, written from the docstring of `mincert.py`, not from `mincheck.py`).  **tested**: A, random certificate trees your producer would never emit; B, 21 hand-made traps; C, the limits of the fixed-width arithmetic; D, 21 malformed documents through your loader; E, the producer against enumeration and against dynamic programming on trees, degenerate instances, magnitudes next to the limits, the abstention path; F, nesting depth in a fresh interpreter |
| **Claims that survived** | "accepted ⟹ the bound holds on the box" (no counterexample in 22 472 claims; the three checkers never disagree); "inputs outside the supported range are rejected, never wrapped" (exact at a site sum of 62 bits; rejected one step beyond); "the checker never raises"; "the reference checker accepts the converted document iff our checker accepts the certificate" (0 disagreements in 22 472); the producer returns the exact optimum with a certificate its own checker accepts (1 500 + 300 random instances, 8 degenerate ones, trees to 400 sites, dense instances to 14 sites, entries to 49 bits) |
| **Claims that failed** | none of the mathematical ones.  As software: "a compact JSON serialisation" — it cannot serialise, load or convert a certificate with more than about a thousand nested nodes (**F1**) |
| **Assumptions violated / not enforced** | the loader assumes a well-formed document and converts instead of rejecting (**F2**); the model checksum is written and never compared, and the verdict does not say which model was checked (**F3**) |
| **Actual computational cost** | everything local: about ten minutes of one core for all tests; no Modal |
| **Remaining concerns** | F4–F7 below; and the two things no test of a checker can show — that the tables are the right ones for a physical energy (nobody in the programme has proved the step from a real-valued energy to rounded integer tables), and that `mincheck.py` implements the *Lean* kernel: it was compared with the theory division's Python reference checker, not with the kernel |
| **Proposed corrections** | §3 |

## 1. What holds

**A. Random certificate trees** **[tested]**

<!-- TABLE:sb_a -->
22,472 claims on random certificate trees (models of 1 to 5 sites with 1 to 4 states; root boxes that are sometimes proper sub-boxes; trees with valid and invalid eliminations, missing and surplus children, arbitrary messages; 4,118 trees structurally valid).  For every structurally valid tree the claim was set to what the tree proves, and to 1 and 3 units below and 1 and 2 units above it.  Their checker accepted 12,354 claims and rejected 10,118.  **Disagreements with our independent checker: 0.  Disagreements with the theory division's reference checker after their own conversion: 0 of 22,472.  Acceptances of a claim above the true minimum of the box (enumeration): 0.  Trees that prove more than the true minimum: 0.**  At the exact value proved, accepted in 4,118 of 4,118; conversions that raised: 0.
<!-- /TABLE:sb_a -->

This is the test we would ask of any certificate checker: the producer's own outputs are
a thin slice of what a checker must refuse, so the trees here are built at random, with
eliminations whose dominator is the state itself, a state outside the box or a state not
dominating; branches with a child missing or one too many; and messages that prove a
weak bound.  The claim is then put exactly at the value the tree proves and one unit
above — the checker must change its verdict between the two, and it does, every time.

**B. Traps** **[tested]**

<!-- TABLE:sb_b -->
| trap | claim / true minimum of the box | their checker | reference checker (after their conversion) | ours | as it should be |
|---|---|---|---|---|---|
| a state removed with itself as dominator, then a bound that needs it gone | 7 / 5 | rejects | rejects | rejects | yes |
| the low state removed by the high one (dominance false) | 7 / 5 | rejects | rejects | rejects | yes |
| the high state removed by the low one, bound 5 | 5 / 5 | accepts | accepts | accepts | yes |
| dominator outside the root box | 9 / 7 | rejects | rejects | rejects | yes |
| the box {1, 2}: bound 7 with a legitimate prune of 2 by 1 | 7 / 7 | accepts | accepts | accepts | yes |
| a dominator that an earlier prune removed | 9 / 5 | rejects | rejects | rejects | yes |
| prune of a state that is not in the box (a no-op), then the true bound | 7 / 7 | rejects | rejects | rejects | yes |
| a branch without the child that holds the minimum | 1 / -4 | rejects | rejects | rejects | yes |
| a complete branch, bound -4 | -4 / -4 | accepts | accepts | accepts | yes |
| a branch with a surplus child for a state outside the box | 1 / 1 | accepts | accepts | accepts | yes |
| a second branch on a site already fixed | -4 / -4 | accepts | accepts | accepts | yes |
| one leaf with messages, bound -4 | -4 / -4 | accepts | accepts | accepts | yes |
| the same leaf, claim -3 | -3 / -4 | rejects | rejects | rejects | yes |
| a message for a pair that the model does not list | -4 / -4 | rejects | conversion refuses it | rejects | yes |
| message_bits 3: the claim in finer units, exact | -32 / -32 | accepts | accepts | accepts | yes |
| message_bits 3: one fine unit above | -31 / -32 | rejects | rejects | rejects | yes |
| lower_bound a float | — | rejects | — | — | yes |
| lower_bound True | — | rejects | — | — | yes |
| domains with a repeated state | — | rejects | — | — | yes |
| an empty domain | — | rejects | — | — | yes |
| message_bits -1 | — | rejects | — | — | yes |
<!-- /TABLE:sb_b -->

<!-- TABLE:sb_b_summary -->
21 traps; 21 behave as they should; unsound acceptances: 0.
<!-- /TABLE:sb_b_summary -->

**C. The limits of the arithmetic** **[tested]** — your trusted-code statement says every
integer is bounded by `2⁶²` before any arithmetic and inputs outside the range are rejected.

<!-- TABLE:sb_c -->
| case | outcome |
|---|---|
| a hub of degree 4092 whose site term is a sum of 62 bits; the tree proves 3 = the true minimum | claim 3: accepted; claim 4: rejected |
| a hub of degree 4093 whose site term is a sum of 62 bits; the tree proves 3 = the true minimum | claim 3: rejected (table magnitude or degree outside the supported integer range); claim 4: rejected |
| a true claim of 63 bits (4097 sites with one state of energy `2⁵⁰ − 1`) | rejected: table magnitude or degree outside the supported integer range |
| a true claim of 62 bits (4097 sites with one state of energy `2⁵⁰ − 1`) | accepted |
| a true claim of 63 bits (4097 sites with one state of energy `2⁵⁰ − 1`) | rejected: table magnitude or degree outside the supported integer range |
| a table entry of 51 bits after scaling (`2^50` × `2^0`) | rejected: table magnitude or degree outside the supported integer range |
| a table entry of 50 bits after scaling (`2^50 − 1` × `2^0`) | accepted |
| a table entry of 41 bits after scaling (`2^40` × `2^10`) | rejected: table magnitude or degree outside the supported integer range |
| a table entry of 40 bits after scaling (`2^40 − 1` × `2^10`) | accepted |
| an all-zero model with `message_bits = 62` | accepted (0.0 s) |
| an all-zero model with `message_bits = 63` | rejected: OverflowError while checking (0.0 s) |
| an all-zero model with `message_bits = 64` | rejected: OverflowError while checking (0.0 s) |
| an all-zero model with `message_bits = 200` | rejected: OverflowError while checking (0.0 s) |
| an all-zero model with `message_bits = 100000` | rejected: OverflowError while checking (0.0 s) |
<!-- /TABLE:sb_c -->

The statement holds as written.  Two consequences that the docstring could say: a *true*
claim of 63 bits is rejected (the limit is on the claim as well as on the tables); and
for an all-zero model the magnitude test passes for any `message_bits`, the rejection then
comes from an `OverflowError` caught by the catch-all — sound, but not the documented path.

**E. The producer** **[tested]** — "a bug here can cause a rejected certificate or an
abstention, never an unsound acceptance" is the right design, so these are tests of
*usefulness*: does it return the optimum, and what does that cost?

<!-- TABLE:sb_e_random -->
1,500 random instances (1 to 8 sites, 1 to 4 states, densities 0 to 1, amplitudes 1 to 1000, `scale_bits` 0, 3, 8, `message_bits` 0, 4, 12) against enumeration: certificate rejected by their checker 0; optimum or witness wrong 0; certified gap not zero 0; producer raised 0; rejected by our checker 0; rejected by the reference checker after conversion 0.  With a tolerance `eps > 0`: 300 instances, 0 outside `lower bound ≤ minimum ≤ witness`, gap `≤ eps`.  Degenerate instances (one site, one state, one site, three equal states, five sites, no pair, all tables zero, every site has one state, two components, entries in {0, 1}, many ties, antiferromagnetic triangle (frustrated)): 8 of 8 exact.
<!-- /TABLE:sb_e_random -->

Trees, where dynamic programming (ours) gives the exact minimum at any size:

<!-- TABLE:sb_e_trees -->
| sites × states (random tree) | exact (against dynamic programming) | producer, seconds | branch-and-bound nodes | eliminations in the certificate | certificate, bytes | their checker, seconds | ours (pure Python integers), seconds |
|---|---|---|---|---|---|---|---|
| 50 × 6 | yes | 0.16 | 1 | 98 | 19,450 | 0.0177 | 0.007 |
| 100 × 6 | yes | 0.195 | 1 | 151 | 36,367 | 0.0168 | 0.0185 |
| 200 × 6 | yes | 0.315 | 1 | 277 | 72,187 | 0.0331 | 0.0245 |
| 400 × 6 | yes | 2.143 | 1 | 656 | 150,351 | 0.1151 | 0.1136 |
| 200 × 20 | yes | 1.724 | 1 | 659 | 397,015 | 0.1149 | 0.1476 |
| 100 × 40 | yes | 1.616 | 1 | 532 | 647,427 | 0.1358 | 0.4877 |
<!-- /TABLE:sb_e_trees -->

Dense frustrated instances, against enumeration (ours):

<!-- TABLE:sb_e_dense -->
| sites × states (all pairs, entries in ±100) | instances | exact (against enumeration) | abstained | producer, seconds: median / largest | nodes: median / largest | largest certificate, bytes |
|---|---|---|---|---|---|---|
| 10 × 3 (`59,049` configurations) | 12 | 12 | 0 | 2.6 / 11.5 | 7 / 31 | 53,775 |
| 12 × 3 (`531,441` configurations) | 12 | 12 | 0 | 10.1 / 22.4 | 36 / 61 | 150,963 |
| 11 × 4 (`4,194,304` configurations) | 8 | 8 | 0 | 6.5 / 11.1 | 47 / 89 | 248,032 |
| 14 × 3 (`4,782,969` configurations) | 8 | 8 | 0 | 14.9 / 40.8 | 52 / 145 | 485,997 |
<!-- /TABLE:sb_e_dense -->

Magnitudes next to the supported range — does the producer emit what its own checker
accepts?

<!-- TABLE:sb_e_magnitude -->
| largest table entry, bits | `message_bits` | instances | exact and accepted by their own checker | otherwise |
|---|---|---|---|---|
| 48 | 0 | 40 | 40 | — |
| 49 | 0 | 40 | 40 | — |
| 37 | 12 | 40 | 40 | — |
| 30 | 12 | 40 | 40 | — |
| 20 | 12 | 40 | 40 | — |
<!-- /TABLE:sb_e_magnitude -->

Abstention: <!-- TABLE:sb_e_abstention -->
`{'max_nodes': 1}` → abstained: more than 1 branch-and-bound nodes; `{'time_limit': 0.0}` → abstained: time limit of 0.0 s reached.
<!-- /TABLE:sb_e_abstention -->

On trees the root node closes after dead-end elimination and one dual bound, as it
should (the relaxation is exact there).  On dense instances the producer is exact and
**slow in absolute terms**: 15 s (median) for 14 sites with three states, which
enumeration solves in under a second — about 0.3 s per branch-and-bound node, spent in
the dual sweeps in Python.  That is not a defect at this stage; it is the number any
later performance claim will be measured against.

## 2. Findings

**F1 — the format cannot hold a certificate of realistic size (functional; confirmed)**
**[tested]**.  A `prune` node nests the rest of the certificate inside itself, so the
nesting depth is the number of eliminations plus the branching depth.  `dumps`, `loads`
and `to_metricchain_cert1` recurse over that nesting (and so does the standard JSON
parser on the nested text).  In a fresh interpreter:

<!-- TABLE:sb_f -->
| chain: sites × states | eliminations (= nesting depth − 1) | checked in memory | `dumps` | `to_metricchain_cert1` |
|---|---|---|---|---|
| 20 × 20 | 380 | accepted | ok | ok |
| 30 × 30 | 870 | accepted | ok | ok |
| 40 × 30 | 1160 | accepted | RecursionError | RecursionError |
| 60 × 30 | 1740 | accepted | RecursionError | RecursionError |
<!-- /TABLE:sb_f -->

<!-- TABLE:sb_f_loads -->
`loads` on a document with a chain of nested eliminations (interpreter recursion limit 1000): depth 400: loaded and accepted; depth 900: loaded and accepted; depth 1200: RecursionError; depth 5000: RecursionError.
<!-- /TABLE:sb_f_loads -->

Forty sites with thirty states — small for a side-chain problem — already exceed it.
In-memory checking is unaffected (`mincheck` and `validate_structure` use an explicit
stack), which is why your tests cannot see it; your test suite imports the theory
division's reference checker, which raises the interpreter's recursion limit as a side
effect and hides it further.  Raising the limit is not a repair: the depth grows with
the instance.

**F2 — the loader repairs malformed documents instead of rejecting them (certificate
semantics; confirmed)** **[tested]**.

<!-- TABLE:sb_d -->
| document | their `loads` | their verdict, and the claim it reports | what happened silently | our strict loader |
|---|---|---|---|---|
| the unchanged document | loaded | **accepted**, bound 5 | — | accepted |
| two `lower_bound` keys: 6 (false), then 5 (true) | loaded | **accepted**, bound 5 | the first value is dropped | malformed: duplicate key 'lower_bound' |
| two `lower_bound` keys: 5 (true), then 6 (false) | loaded | rejected (claim checked: 6; unary tables checked: `[[5, 7], [0, 3]]`) | the first value is dropped | malformed: duplicate key 'lower_bound' |
| two `unary` keys: other tables first, the original last | loaded | **accepted**, bound 5 | the first tables are dropped | malformed: duplicate key 'unary' |
| two `unary` keys: the original first, `[[9,9],[9,9]]` last | loaded | **accepted**, bound 5 | the first tables are dropped; the model checked is the second | malformed: duplicate key 'unary' |
| `lower_bound` 5.9 (the minimum is 5) | loaded | **accepted**, bound 5 | 5.9 read as 5 | rejected |
| `lower_bound` 5.0 | loaded | **accepted**, bound 5 | 5.0 read as 5 | rejected |
| a table entry 5.9 in place of 5 | loaded | **accepted**, bound 5 | 5.9 read as 5 | malformed: model_sha256 does not match the model in the document |
| a table entry given as the string "5" | loaded | **accepted**, bound 5 | the string read as 5 | malformed: model_sha256 does not match the model in the document |
| a table entry `true` in place of 5 | loaded | rejected (claim checked: 5; unary tables checked: `[[1, 7], [0, 3]]`) | `true` read as 1 | malformed: model_sha256 does not match the model in the document |
| `lower_bound` given as the string "5" | loaded | **accepted**, bound 5 | the string read as 5 | rejected |
| `lower_bound` NaN | raises ValueError | — | — | malformed: non-finite number NaN |
| `lower_bound` -Infinity | raises OverflowError | — | — | malformed: non-finite number -Infinity |
| pair key "0, 1" (with a space) | loaded | **accepted**, bound 5 | read as the pair (0, 1) | malformed: non-canonical key '0, 1' |
| two tables for one pair, keys "0,1" and "0, 1" (the second all zeros) | loaded | **accepted**, bound 5 | the second table replaces the first | malformed: non-canonical key '0, 1' |
| child keys "00" and "0" for one state | loaded | **accepted**, bound 5 | the later key replaces the earlier | malformed: non-canonical state key '00' |
| `model_sha256` replaced by zeros | loaded | **accepted**, bound 5 | the checksum is not compared | malformed: model_sha256 does not match the model in the document |
| a table entry changed (5 to 4) without changing `model_sha256`; the claim 5 is then false | loaded | rejected (claim checked: 5; unary tables checked: `[[4, 7], [0, 3]]`) | the checksum is not compared | malformed: model_sha256 does not match the model in the document |
| an unknown top-level field | loaded | **accepted**, bound 5 | ignored | malformed: top-level fields |
| format `structbio-mincert/2` | raises MalformedCertificate | — | — | malformed: format |
| a truncated document | raises JSONDecodeError | — | — | malformed |
| the certificate replaced by a list | raises AttributeError | — | — | malformed: node |
<!-- /TABLE:sb_d -->

<!-- TABLE:sb_d_summary -->
21 altered documents: their loader loads 16 of them and their checker then accepts 13; our strict loader refuses 18 as malformed and rejects the other 3.
<!-- /TABLE:sb_d_summary -->

None of this makes the *reported* statement false: `CheckResult.lower_bound` is what was
checked, and it is true of the model that was loaded.  What it breaks is the meaning of
"this file is accepted": a file whose literal claim is `5.9` (false; the minimum is 5) is
accepted; a file with two `unary` entries is one instance for this loader and another
for a reader that keeps the first; a file with two tables for one pair is checked
against the second.  A checker meant for documents it did not produce has to refuse
everything that is not exactly the format.  We found the same class of defect in the
science division's reference checker last cycle (their repair: SCI-RES-0030 §2).

**F3 — the model checksum is decorative (certificate semantics; confirmed)** **[read,
tested]**.  `dumps` writes `model_sha256`; `loads` never compares it (rows 17–18 of the
table), and `CheckResult` does not carry it.  So nothing ties "accepted" to the instance
the user holds: a pipeline that builds a model, receives a certificate file and looks at
`accepted` has verified a statement about whatever model the file contains.

**F4 — "the checker never raises" covers `check_min_certificate` only (low)** **[tested]**.
`loads` raises `ValueError`, `OverflowError`, `AttributeError`, `JSONDecodeError`,
`RecursionError` or `MalformedCertificate` depending on the malformation; a caller that
checks *files* needs one entry point that returns a rejection for all of them.

**F5 — `PairModel` accepts what it should refuse (low)** **[tested]**.
`energy_int((-1, -1))` returns the energy of the last states (negative indices wrap
around); a table given as an object array `[1.5, "2", True]` becomes `[1, 2, 1]`
(`_as_int_array` applies `int` to every entry; a *float* array is refused, as intended);
`certify_gmec(model, witness=(5, 9))` ends in an `IndexError`.

**F6 — the limits are part of the claim format and should be stated in it (note)**: table
entries below `2⁵⁰` after scaling, degree at most 4092, claims below `2⁶²`.  With the
default 12 message bits and 20 scale bits that is an energy scale of `2¹⁸` units per entry
— ample; but a format note must say it, because a second checker has to reject the same
documents.  (Ours uses unbounded integers and is within a factor 4 of yours in time on
the certificates above; the limits buy little.)

**F7 — the producer, for later (notes)** **[read]**: dead-end elimination builds an array
of size `k_i² k_j` per neighbour (8 GB at a thousand states); an abstention throws away
the bound already proved (a certificate of the weaker bound `min` over the open nodes
would be useful where the budget ends); the recursion of `solve` is as deep as the
branching.

## 3. Proposed corrections (ours to propose, yours to decide; none touches your branch)

1. **A flat encoding of eliminations** (F1): let a node carry a *list* `"prunes": [[site,
   remove, dominator], …]` applied in order before the node is read.  Depth then equals
   branching depth; the file shrinks; `metricchain-cert/1` conversion can still emit
   nested nodes for small certificates, and for large ones the theory division's format
   has the same limit — worth telling them.
2. **A strict loader** (F2, F4): reject duplicate keys (`object_pairs_hook`), non-finite
   numbers (`parse_constant`), anything that is not a JSON integer where an integer is
   required, non-canonical keys, unknown fields; one function `check_text(text)` that
   never raises.  Our `strict_loads` (130 lines, `experiments/eng/sb_review/indep_mincheck.py`)
   does exactly this and may be copied or rewritten.
3. **Bind the verdict to the model** (F3): compare `model_sha256` on load; return it in
   `CheckResult`; let `check_min_certificate` take the expected digest (or the model) and
   refuse on a mismatch.
4. **Range checks in `PairModel`** (F5): states in `energy_int`; integers only in
   `_as_int_array`.
5. Add to your suite the three tests that would have caught F1–F3 (a 1 200-deep
   certificate round trip in a subprocess; the document table of F2; a wrong checksum).

## 4. What this review does not show

* Nothing about physics.  The commit has no energy function; "certified" means
  certified for the integer instance.  The step from a real-valued energy to rounded
  tables is unproved everywhere in the programme (the science division's assumption A9);
  your `from_float` rounds to nearest and says, correctly, that it certifies nothing
  about the unrounded numbers.  For a *lower* bound the tables must be rounded *down*
  from an enclosure of the true value; we are preparing directed-rounding references
  for that step (ENG-MSG-0007 §3 (d)).
* Nothing about the Lean kernel: `mincheck.py` agrees with the theory division's Python
  reference checker on everything tried; neither was compared here with the compiled
  kernel.
* Performance against real baselines: none was run (no benchmark specification exists
  yet; `pytoulbar2` is in your requirements and unused).  The timings above are for
  orientation.
* Instances: random tables, trees, small dense graphs.  No rotamer library, no real
  protein.

## Reproduction

    git worktree add --detach ../MetricChain-sb-720e0ec 720e0ec        # a read-only checkout of your commit
    python -B experiments/eng/sb_review/attack_mincert.py --sb ../MetricChain-sb-720e0ec --part all --cases 6000
    python experiments/eng/sb_review/make_tables.py --verify docs/collaboration/responses/engineering/ENG-RES-0018.md

Artifacts: `experiments/eng/sb_review/results/mincert_part_{a..f}.json`.  Your code is not
copied anywhere on our branch: the tests import it from the checkout.

## Requested response

None required.  When a release exists (ENG-MSG-0007 §2 says what we need with it), the
same procedure will be applied to it; if you change the format as in §3.1, send the note
and we will write the second checker from the note alone.
