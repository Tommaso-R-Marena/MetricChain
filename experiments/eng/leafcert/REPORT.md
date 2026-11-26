# An exact checker for "shares at the leaves" certificates (X-012)

Computational Research Division, 2026-11-26.  Answer to request **P7-E2** of the Scientific
Discovery Division ("a compiled exact checker of that format: what runs where the Lean kernel
cannot"); their report `docs/science/workstreams/P7_REPORT.md` at commit `2b4ccdf` of
`research/scientific-translation`.

**How this was made.**  The checker, its tests and the body of this report were written by an
independent subagent of this division from the text of that report (§5.1–5.4, and §2.1 for the
mathematics) and from the nine certificate files, their checksum file and their logs.  No code
of that branch was opened before the checker and its tests were frozen; §9 says what the
comparison with their reference checker showed afterwards.  Everything of that branch was
treated as data: read with `git show`, parsed strictly, never executed.  **Checked by the
division's coordinator before publication:** the vector script and the 182 tests re-run; the
core of both engines read; a third, thirty-line checker written by the coordinator from §5.1–5.2
agrees with both engines on the nine files, on the nine files with the bound raised by one,
and on 4 000 random small certificates (726 accepted, none with a false bound by enumeration);
the finding of §9 item 1 confirmed by reading the reference checker.

Code: `src/metricchain_eng/leafcert/` (`leafcert.c`, `ckernel.py`, `pycheck.py`, `loader.py`,
`__init__.py`, `__main__.py`).  Tests: `tests/eng/test_leafcert.py`.  Here: `run_vectors.py`,
`results/vectors.json`.

## 1. Result

1. **All nine files are accepted** by both engines — `leafcert.c` (C11, 64-bit input, 128-bit
   sums, no floating point: it compiles with `-mgeneral-regs-only`) and `pycheck.py` (Python
   integers) — with identical results; the sha256 of every file equals the one in
   `logs/run1/cert_sha256.txt` of the same commit.
2. **All 27 controls are rejected by both engines, each on an inequality** (not on a format
   error), at the same inequality in both.  All 472 possible exchanges of two different
   children, at every branch node of every file, are rejected too.
3. **Our counts equal the table of §5.2 in every cell** for all nine files: depth, leaf
   certificates, leaf boxes, integers, additions, comparisons, states of the domain, and the two
   columns "with a domain-split rule" (`4 585 / 2 126`, `6 246 / 3 120`, `9 318 / 4 353`).
4. **Enumeration confirms the bound for all nine files** (18 270 to 531 441 states): the minimum
   of the published instance is `0 = L`, attained only at the state `ref` of the file.
5. **No unsound acceptance** in 24 092 certificates of 2 000 random small instances (246 842 of
   20 000 in the long run), nor in 26 865 single-integer mutants (287 208) of accepted
   certificates; the two engines never disagreed; a third evaluator in the test file predicted
   every verdict and every first failing inequality.
6. Deliberately broken copies of both checkers (23 of the C source, 18 of the Python source) are
   all detected by the test corpus; each of the 32 that are too lax by a bound it accepts and
   enumeration refutes.

What this does **not** establish: §3.2 and §8 — in particular nothing here concerns the
relation between the published integer tables and the real-valued model they were rounded from.

## 2. What the checker checks

**Data.**  A JSON object with `H` (a list of `n ≥ 1` lists of integers, `H[i][a] = H_i(a)`; site `i`
has the states `0 … k_i − 1`; the domain is the whole product `X`), `J` (exactly the keys `"i,j"`,
`i < j`; `J["i,j"][a][b] = J_ij(a, b)`), `L` (the bound), `leaves` (leaf certificates, each with `U`
(`n` integers), `P2` (keys `"i,j"`, `i < j`) and `m` (keys `"i,j"` for all ordered pairs `i ≠ j`,
`m["i,j"][a] = m_ij(a)`, a vector over all states of `i`)), and `tree` (a node is `{"leaf": t}` or
`{"site": i, "children": {state: node}}`).  `E(x) = Σ_i H_i(x_i) + Σ_{i<j} J_ij(x_i, x_j)`.  The other
keys the nine files carry are annotations and never influence a verdict.

**Well-formedness, checked before any arithmetic** (a file is rejected with `kind = "format"` and
a reason; nothing is repaired or ignored): valid JSON without duplicate keys; every number a
JSON integer; exactly the keys, lengths and index sets stated; every leaf index in range and
every leaf certificate named by some node; every branch on a site that no ancestor branches
on, with exactly the children `"0" … str(k_i − 1)`.

**The inequalities.**  Every node `v` has a box `D(v)`: `D_i(v) = {a}` if the path from the root to `v`
passes through the child `a` of a branch on site `i`, else all states of `i`.  For every leaf node
`v`, with `(U, P2, m)` the certificate it names and `D = D(v)`:

    (S)   for every site i and every a ∈ D_i:                    U_i    ≤  H_i(a) + Σ_{j ≠ i} m_ij(a)
    (P)   for every pair i < j, every a ∈ D_i, every b ∈ D_j:    P2_ij  ≤  J_ij(a, b) − m_ij(a) − m_ji(b)
    (T)                                                          L      ≤  Σ_i U_i + Σ_{i<j} P2_ij

Accepted iff well formed and (S), (P), (T) hold at every leaf node.  Only additions,
subtractions and comparisons of integers; nothing is minimised and the domain is not
enumerated.  The first failing inequality (depth first, states ascending; (S), then (P) in
lexicographic order, then (T)) is reported with its location and both sides.

**Cost convention** (the one that reproduces the table of §5.2): a term of (S) is `n − 1`
additions and one comparison; a term of (P) two additions and one comparison; (T) is
`n + n(n−1)/2 − 1` additions and one comparison.

**Arithmetic.**  Every integer of the input must fit in 64 bits (otherwise the C engine rejects
with `kind = "range"`; it never computes with a truncated number, and the Python engine
decides); sums are accumulated in `__int128` through the compiler's overflow check.

## 3. What acceptance implies, and what it does not

### 3.1 Acceptance implies `E(x) ≥ L` for every `x` of the product of the alphabets

(a) *The boxes of the leaf nodes cover `X`.*  The box of the root is `X`.  A branch `v` on site `i`
is on a site no ancestor fixed, so `D_i(v)` is the whole alphabet; it has a child `c_a` for every
state `a`, and `D(c_a) = {x ∈ D(v) : x_i = a}`: `D(v)` is the union of the boxes of its children.  By
induction from the root every `x` lies in the box of a leaf node.
(b) *At a leaf node, (S), (P), (T) give the bound on its box.*  For `x ∈ D(v)`, add (S) at `(i, x_i)`
for all `i` and (P) at `(i, j, x_i, x_j)` for all `i < j`:

    Σ_i U_i + Σ_{i<j} P2_ij  ≤  Σ_i [H_i(x_i) + Σ_{j≠i} m_ij(x_i)] + Σ_{i<j} [J_ij(x_i, x_j) − m_ij(x_i) − m_ji(x_j)]  =  E(x),

because every `m_ij(x_i)`, `i ≠ j`, occurs once with `+` (site `i`) and once with `−` (pair `{i, j}`).
With (T): `L ≤ E(x)`.  ∎

This is the argument of Propositions P7.1(a), P7.2 of the science report and of `leaf_sound`,
`verify_sound` of `proofs/CertificateAlgebra.lean` (with `u = U`, `p_ij = p_ji = P2_ij/2` and each pair
table stored once, `LeafOK` is (S), (P), (T) literally — compared by reading; Lean was not run).

### 3.2 What acceptance does not imply

* **Nothing about where the tables come from**: that `H`, `J` are the lower model of a real-valued
  energy in difference form, rounded *down* to `2⁻⁴⁰` kcal/mol, with correct class constants, is
  not checkable from the file.  The step from "the published instance is `≥ 0`" to a statement
  about a model (their Lemma P7.7 and `pairwise_sandwich_of_class`) is outside.
* Not that `L` is attained, nor that `ref` is a minimiser (for the nine files it is, by
  enumeration; that is not part of "accepted").
* Nothing about a domain other than the full product of the alphabets (a restricted,
  clash-free domain cannot be expressed in this format), nor about other certificate formats
  (the triplet / `sum` certificates): a file with other keys is rejected as malformed.
* Not that the certificate is tight or minimal: message entries for states outside every box on
  which a leaf is used are read by no inequality (360 of the 2 619 integers of the Ser₆
  one-leaf-per-state file).
* The compiler, the C library, the interpreter and the hardware are trusted; the checker is
  tested, not verified.

## 4. Where this checker is stricter than the rule as stated

The rule of §5.2 and the Lean `verify` are total; this checker also rejects files that are not
in canonical form.  None of these can turn a rejection of the rule into an acceptance.

| this checker rejects | the Lean `verify` | reason |
|---|---|---|
| a branch on a site an ancestor already fixed | checks only the child of the fixed state | such a branch carries dead children |
| a branch with a child missing, or with a child that is not a state | (children are a total function); ignores | "the child must exist"; no dead data |
| a site without states | accepts: every bound holds on the empty box | a vacuous acceptance must not look like a certified bound |
| a leaf certificate that no node names; unknown keys | — | no dead data; an unknown key might change the meaning |

## 5. Ambiguities in the specification and the files (the reading adopted)

1. **Direction of the comparisons**: §5.2 says "the comparison with `U_i`" without a direction.
   Taken from the rule quoted in §5.3 and the `note` field of the files: `U_i ≤ …`, `P2_ij ≤ …`.
2. **The bound**: §5.2 writes "finally `0 ≤ ΣU + ΣP2`"; the files carry `L` (0 in all nine).  (T)
   uses the `L` of the file; control (i) is the same file with `L + 1`.
3. **The domain** is not stated: taken as the product of the alphabets (`shape` agrees, and the
   column "states of the domain" equals `∏ k_i`).
4. **The JSON encoding** is not described in §5.1; inferred from the files (the unequal
   alphabets of Lys₃ — 30, 29, 21 — and LKSE:6 leave no other choice).
5. **Eighteen keys** of the files are not mentioned in §5.1; treated as annotations; under the
   inferred meaning all nine files are consistent (per leaf `LB = ΣU + ΣP2 ≤ bf_min`, `kind = "R"`
   exactly for the leaf whose box contains `ref`, …).
6. **The cost convention** is not stated; the one of §2 reproduces every number.
7. **Control (ii)**, "the first leaf alone on the whole domain": built as the single leaf node
   with `leaves` reduced to its first element (leaving the others would be rejected as
   malformed — a rejection for the wrong reason; every control is required to fail on an
   inequality).  **Control (iii)**, "the children of two states exchanged", does not say which:
   taken at the root, the two smallest states whose subtrees differ; and all 472 exchanges
   were tried.
8. **Nine files, seven certificates**: the two Ser₆ files at `tau 0.70` differ from those at
   `tau 0.60` only in `label` and `tau` — every integer is the same (and `tag` reads `…t0.60` in
   both).  This agrees with §0 of the report ("the same domain at both clash thresholds").
9. No discrepancy between the files and the table of §5.2.

## 6. Tests (default run; in brackets the long run `LEAFCERT_FUZZ=10`)

| test | numbers | outcome |
|---|---|---|
| the nine files, both engines, checksums | 9 | accepted; counts equal the table |
| the three controls; all exchanges of children | 27; 472 | rejected on an inequality, same location in both engines |
| enumeration of the nine domains | 18 270 … 531 441 states | minimum `0 = L`, only at `ref` |
| malformed objects / JSON texts / C encodings | 94 / 29 / 70 | each rejected with the expected kind and reason |
| soundness fuzz: random instances (2–5 sites, 1–4 states, all pairs, chains, trees, frustrated rings), certificates from an own producer and adversarial variants | 2 000 [20 000] instances; 24 092 [246 842] certificates; 10 663 [108 639] accepted, 5 960 [61 489] of them tight; 9 097 [94 707] false claims | **0 accepted bounds refuted by enumeration; 0 disagreements between engines** |
| every certificate with seven numbers in `{−1, 0, 1}` on two binary sites | 26 244 [85 293] | verdict and first failure as defined |
| integer mutants (±1, large, edges of the slack) of accepted certificates | 26 865 [287 208]; 60.1 % of the small ones and 73.5 % of Leu₁₆'s caught | every verdict predicted from the slacks; every accepted mutant confirmed by enumeration and belongs to one of eight sound classes (a table entry raised; lowered within slack; `U_i`, `P2_ij` lowered within the slack of (T); `L` lowered, or raised within slack; a message changed within slack; a message entry no inequality reads) |
| structural mutants (children exchanged, deleted, duplicated; branches removed or inserted; leaf indices changed) | 2 501 [20 877] small; 110 [4 838] real | accepted ones are the same certificate, an inserted branch, or another valid certificate (confirmed) |
| broken copies of the checkers | 23 (C) + 18 (Python) | all detected |
| corrupted encodings for the C parser against an independent decoder; sanitizer build | 3 000 [30 000]; 3 036 [30 036] inputs | agree; no report |
| 64-bit limit | 1 500 [15 000] certificates at the edges of the range | arithmetic modulo `2⁶⁴` would have accepted 235 [2 222] false bounds that both engines reject |

## 7. How to reproduce

    python experiments/eng/leafcert/run_vectors.py                          # 3 s; writes results/vectors.json
    python -m pytest tests/eng/test_leafcert.py -q                          # 182 tests, under a minute
    LEAFCERT_FUZZ=10 python -m pytest tests/eng/test_leafcert.py -q -s      # 188 tests, 9 min on one thread
    PYTHONPATH=src python -m metricchain_eng.leafcert FILE.json             # one file, both engines

The compiled checker alone, without Python at run time:

    cc -std=c11 -O2 -DLEAFCERT_MAIN -o build/leafcert src/metricchain_eng/leafcert/leafcert.c
    PYTHONPATH=src python -m metricchain_eng.leafcert --encode FILE.json > FILE.txt
    build/leafcert FILE.txt          # exit status 0: accepted; 1: rejected; 2: cannot read

The tests that need the nine files read them with `git show 2b4ccdf:<path>` and are skipped with
a message if that commit is not in the clone.  A real file takes 0.05–0.3 ms in `leafcert.c`,
0.7–3 ms through `check(…, "c")` (JSON parsing dominates) and 1.3–5.2 ms in the Python engine.

## 8. Limitations; what was not tested

* The link to the model (§3.2) — not examined at all.
* Not a proof; no formal link to the Lean `verify`.
* The stand-alone C program reads our text encoding, not the JSON; the transcription
  (`loader.encode`) is cross-checked on every test against the Python engine, which reads the
  JSON directly, and against a second encoder in the test file.
* gcc 15.2 on x86-64 Linux only (`__int128`, `__builtin_add_overflow` are compiler extensions).
* Largest inputs: the nine files, a 200-site instance and a 40-site chain; the size limits of
  the C checker (`n ≤ 4096`, `k_i ≤ 2²⁰`, `2²⁶` integers) are tested only as rejections.
* Fuzz instances are small (at most 5 sites × 4 states), because enumeration needs that.
* The producer, enumerator, third evaluator and decoder of the test file were written by the
  same author as the two engines; an error of understanding common to all of them would be
  exposed only by the nine files and their controls (and by the coordinator's third checker).
* No producer on this branch: nothing here says what a certificate costs to make.

## 9. Comparison with the reference checker `p7_06_check.py` (read last, as text; not executed)

**Same** on well-formed input: the three inequalities and their directions, the order, the root
domain, `L` from the file, one child per state, the cost convention line for line — which is why
every count agrees.

**Different only on input that is not well formed**, which the reference does not validate:

1. **It can return True for a false bound on malformed input.**  Its total is
   `sum(U) + sum(P2.values())` over *everything* in `U` and `P2`, while (S) and (P) look only at
   `U[0..n−1]` and the pairs `i < j < n`.  An extra entry appended to `U`, or an extra key in `P2`
   (for instance `"1,0"`), is added to the total without being bounded by any inequality.
   Example: one site, `H = [[5, 7]]`, `U = [5, 100]`, no pairs, `L = 100`: (S) holds for `U[0]`, the
   total is `105 ≥ 100`, the minimum is 5.  **This does not touch the nine files** (they are well
   formed) and cannot occur on the Lean route (a `Cert` term has no room for extra entries).
2. No check of types: `json.load` accepts duplicate keys, fractions, exponents and `NaN`; with
   non-integer numbers the sums are floating-point sums.
3. Negative indices mean "the last one" in Python; a missing key or a short list ends in an
   exception, not a verdict.
4. Keys are parsed with `int(…)`, so `"0, 1"`, `"+0,1"` and `"00,1"` are all the pair `(0, 1)` and
   overwrite each other silently.
5. Lenient where ours is strict (§4); `shape` defines the domain there (with a `shape` smaller
   than a row of `H` it certifies the smaller box without saying so).
