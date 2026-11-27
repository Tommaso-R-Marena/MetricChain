# Can the Lean kernel evaluate one leaf check on 10³–10⁵ table entries?

*Provenance and checks (added by the coordinator of the theory division at the twenty-first
checkpoint of cycle 10).*  This experiment was designed in a written brief by the
coordinator and carried out by a subagent; the text below is the subagent's report.  It
answers request P7-T4 of the Scientific Discovery Division (its message SCI-RES-0014) and is
quoted, as a measurement, in theory report Proposition 11.18b(e), §12 item 7, and in
THY-RES-0014 §4.  The coordinator re-ran three cases independently — the packed
hierarchical encoding at `n = 32`, `k = 8` regenerated in a scratch directory (accepted, no
axioms, `0.98` GB peak), a wrong claim (rejected, exit status 1) and the array encoding at
`n = 8`, `k = 2` (`1.1` GB peak) — and read the checker of the packed encoding against the three
conditions of the leaf check.  To keep the repository small, `generated/` holds only the
files of the smallest size for every encoding and the size `(16, 2)` with its controls for
the packed hierarchical encoding (22 files); all others regenerate byte for byte with
`gen.py` (every log records the SHA-256 of the file it ran).

Feasibility experiment, 2026-11-26. Lean 4.31.0 (commit 68218e87, x86_64 Linux), 4 cores, 16 GB,
shared machine. Every Lean file in this directory imports nothing (core Lean only); Mathlib is not
used; nothing outside this directory was edited; `lake build` was not run.

## 1. The question

A collaborating group checks certificates for lower bounds on pairwise energies with `verify`
(`proofs/CertificateAlgebra.lean`: `ℚ`, `Finset` sums, `Decidable` instances). Proving
`verify cert inst dom 0 = true` with `decide +kernel` on an instance with 16 binary sites, 3 leaves
and 512 table entries (40-bit integers in arrays) exhausted 11.9 GB. They ask:

> Is there an encoding of instance and certificate for which kernel evaluation reaches
> n²k² ≈ 10³–10⁴ table entries, or is a verified evaluator outside the kernel the intended route?

Tested here: can the kernel evaluate ONE LEAF CHECK (n sites, k states, full domain)

- (A) for all i, a: `u i ≤ h i a + Σ_{j≠i} m i j a`
- (B) for all i ≠ j, all a, b: `2 · p i j ≤ J i j a b + J j i b a − m i j a − m j i b`
- (C) `L ≤ Σ_i u i + Σ_i Σ_{j≠i} p i j`

on 10³–10⁵ entries of 40-bit integers when the checker is written for the kernel: integers only,
`Bool`-valued, structural recursion on counters and lists, no `ℚ`, no `Finset`, no `Decidable`
instances for quantifiers, proved by `decide +kernel` (never `native_decide`).

## 2. Answer

Yes, for the integer-only checkers of this directory (which are NOT `verify`, see section 7):

- **n²k² = 147456 entries** (n = 48, k = 8) were evaluated by the kernel in 13.5 s (25 s wall,
  1.6 GB peak) with tables packed into one natural number each and read hierarchically (E2h), and
  in 23 s (77 s wall, 3.8 GB) with flat lists of offset naturals read in one pass (E4).
- The target range n²k² ≈ 10³–10⁴ costs 0.1–1.3 s of kernel time and less than 0.2 GB above the
  0.44 GB that `lean` needs for an empty file (E2h; E4 and E1 are 2–4 times heavier).
- Flat `List Int` (E1) reached 65536 entries (2.7 GB) and exceeded 5 GB at 147456. A single big
  `Nat` read by shifting the whole table (E2) reached 16384 entries and ran out of memory at 65536.
  `Array Int` with `Array.getD` (E3, the collaborators' storage) passed 256 entries with 1.1 GB and
  exceeded 5 GB at 1024 entries.
- The limit is memory, not time: within one declaration the kernel keeps what it has reduced, so
  memory grows with the number of reduction steps (about 16 kB per cell for E2h, 33 kB for E4,
  53 kB for E1; a cell is one unordered pair with one (a, b): two table entries, two comparisons).

So the size of a leaf does not force an evaluator outside the kernel. What is missing for the
kernel route is a proof, written once, that the integer checker implies `LeafOK` for the decoded
instance (section 7); nothing of that proof exists yet.

## 3. What was built

| file | purpose |
|---|---|
| `gen.py` | generator (standard library, fixed seed 20261126): random signed 40-bit tables, zero messages, tight certificate (`u i = min_a h i a`, `p i j = ⌊min_{a,b}(J i j a b + J j i b a)/2⌋`, `L` = the sum in (C)), reference check in Python, one self-contained Lean file per encoding; negative controls; variants |
| `run.sh` | runs one `lean` process at a time under the limits, writes `logs/<name>.log` |
| `measure.py` | wall time and peak resident memory (`wait4`), kills a run above 5 GB resident |
| `collect.py` | `logs/*.log` → `results.md`, `results.tsv` |
| `generated/` | generated Lean files: the size (8, 2) for every encoding with the controls of E3, and the size (16, 2) with its controls for E2h (22 files, 0.5 MB; the subagent kept 58 files up to n = 32, k = 4, pruned by the coordinator); all others are deleted after their run and regenerate byte for byte (each log records the SHA-256 of the file it ran) |
| `logs/` | one log per run (90), plus `run_all.console.txt` |
| `pitfall_thunk_*.lean`, `baseline_empty.lean` | side experiments, written by hand |

Sizes (n, k): (16, 2), (16, 4), (32, 4), (32, 8), (48, 8), i.e. n²k² = 1024, 4096, 16384, 65536,
147456, and an extra tiny size (8, 2) = 256 because the array baseline does not get through
(16, 2).

Each generated file contains the checker, the tables as constants, and

```lean
theorem check_ok : E2h.leafCheck 48 8 off Lo hN uN pN mN jN = true := by decide +kernel
#print axioms check_ok
```

## 4. The encodings

All loops are structural recursion on a `Nat` counter (with list patterns in E1/E4); the counter
is matched in every step, so the loop variables the kernel sees are literals. Arithmetic is
spelled `Nat.add`, `Nat.mul`, `Nat.ble`, … directly (no `+`/`≤` instances to unfold).

| | tables | how an entry is reached | arithmetic |
|---|---|---|---|
| **E1** | flat `List Int`, entries in constructor form (`Int.ofNat a`, `Int.negSucc a`), in stream order | one front-to-back pass; nothing is indexed; the rest of the `J` stream is threaded through `Option (List Int)` | `Int.add`, `Int.neg`, `Int.mul`, a four-case `Bool`-valued `≤` |
| **E4** | flat `List Nat`, every entry stored as value + 2⁶², same stream order | the same pass | `Nat.add`, `Nat.mul`, `Nat.ble` |
| **E2** | ONE `Nat` per table, 64-bit fields, value + 2⁶², row-major | flat read: `(T >>> 64·t) % 2⁶⁴` with index arithmetic | `Nat` |
| **E2h** | the same packed tables | hierarchical read: the part of site i (64·n·k² bits), inside it the block of the pair (i, j) (64·k² bits), inside it the entry | `Nat` |
| **E3** | `Array Int` literals, row-major | `Array.getD` with index arithmetic | `Int` |

E2h is the fourth encoding, suggested by the results of E2; E4 was added to separate the cost of
`Int` from the cost of lists.

Stream order of E1/E4: `h`: (i, a); `u`: i; `p`: for i < j: `p i j, p j i`; `m`: for i < j:
`m i j ·, m j i ·`; `J`: for i < j, a, b: `J i j a b, J j i b a`. The two entries one cell needs
are adjacent, so (B) is a single pass; (A) is accumulated in the same pass (row sums of the
messages are carried along as lists). The `J` stream has n(n−1)k² entries (144384 for n = 48,
k = 8); the row-major tables of E2/E2h/E3 have n²k² including the unused diagonal blocks.

With offsets (`off = 2⁶²`, primes = stored values, `Lo = L + n²·off`) the conditions are
(A) `u' + (n−1)·off ≤ h' + Σ m'`, (B) `2p' + m' + m' ≤ J' + J' + 2·off`, (C) `Lo ≤ Σu' + Σp'`.
Every unordered pair is visited once and both orientations are compared (they share the
right-hand side of (B)).

## 5. Results

All numbers are read from `logs/` by `collect.py`; the complete tables are in `results.md`.
"kernel s" and "elaboration s" are the cumulative "type checking" and "elaboration" times of
`lean --profile` for the whole file; "wall s" also contains start-up (0.3 s), parsing and the
rest. "peak RSS" is the maximum resident set size of the `lean` process (MB = 1024 kB); an empty
file needs 441 MB (`logs/baseline_empty.log`). Single runs on a shared machine. Where a file had
already been run before the logged sweep, peak memory agreed to within 1 % and times differed by
up to 40 % (the earlier runs are not kept).

### 5.1 Main table: `leafCheck … = true := by decide +kernel`

| encoding | n | k | n²k² | cells n(n−1)/2·k² | result | wall s | kernel s | elaboration s | peak RSS MB | axioms |
|---|---|---|---|---|---|---|---|---|---|---|
| E1 | 8 | 2 | 256 | 112 | ok | 0.78 | 0.12 | 0.28 | 477 | none |
| E1 | 16 | 2 | 1024 | 480 | ok | 1.61 | 0.40 | 0.66 | 525 | none |
| E1 | 16 | 4 | 4096 | 1920 | ok | 3.02 | 0.96 | 1.30 | 628 | none |
| E1 | 32 | 4 | 16384 | 7936 | ok | 12.51 | 4.48 | 5.67 | 1151 | none |
| E1 | 32 | 8 | 65536 | 31744 | ok | 42.41 | 17.50 | 17.70 | 2673 | none |
| E1 | 48 | 8 | 147456 | 72192 | FAIL: resident memory above 5 GB, killed after 79 s | 78.82 | - | - | 4888 | - |
| E4 | 8 | 2 | 256 | 112 | ok | 0.68 | 0.07 | 0.21 | 469 | none |
| E4 | 16 | 2 | 1024 | 480 | ok | 1.26 | 0.26 | 0.52 | 510 | none |
| E4 | 16 | 4 | 4096 | 1920 | ok | 2.24 | 0.66 | 0.98 | 580 | none |
| E4 | 32 | 4 | 16384 | 7936 | ok | 8.90 | 2.97 | 4.00 | 942 | none |
| E4 | 32 | 8 | 65536 | 31744 | ok | 28.03 | 8.56 | 13.50 | 1913 | none |
| E4 | 48 | 8 | 147456 | 72192 | ok | 77.21 | 23.00 | 37.70 | 3760 | none |
| E2 | 8 | 2 | 256 | 112 | ok | 0.54 | 0.03 | 0.08 | 459 | none |
| E2 | 16 | 2 | 1024 | 480 | ok | 0.91 | 0.24 | 0.22 | 473 | none |
| E2 | 16 | 4 | 4096 | 1920 | ok | 1.36 | 0.51 | 0.47 | 564 | none |
| E2 | 32 | 4 | 16384 | 7936 | ok | 6.07 | 4.12 | 1.43 | 1739 | none |
| E2 | 32 | 8 | 65536 | 31744 | FAIL: out of memory under `ulimit -v` ("GNU MP: Cannot allocate memory") at 3.2 GB resident | 17.48 | - | - | 3244 | - |
| E2h | 8 | 2 | 256 | 112 | ok | 0.42 | 0.03 | 0.06 | 459 | none |
| E2h | 16 | 2 | 1024 | 480 | ok | 0.57 | 0.10 | 0.15 | 471 | none |
| E2h | 16 | 4 | 4096 | 1920 | ok | 1.10 | 0.29 | 0.42 | 493 | none |
| E2h | 32 | 4 | 16384 | 7936 | ok | 3.04 | 1.34 | 1.31 | 617 | none |
| E2h | 32 | 8 | 65536 | 31744 | ok | 10.72 | 5.08 | 4.89 | 961 | none |
| E2h | 48 | 8 | 147456 | 72192 | ok | 24.98 | 13.50 | 10.40 | 1640 | none |
| E3 | 8 | 2 | 256 | 112 | ok | 4.55 | 4.02 | 0.18 | 1084 | none |
| E3 | 16 | 2 | 1024 | 480 | FAIL: resident memory above 5 GB, killed after 22 s | 22.49 | - | - | 4886 | - |

"axioms: none" is the output `'check_ok' does not depend on any axioms`. Each encoding was
stopped at its first failure.

Cost of the kernel evaluation per cell, at the largest size that passed. Memory: the full run
minus the run of the same file without the theorem (`*_dataonly` in 5.3); for E2 and E3 minus the
empty file instead, which overestimates slightly.

| encoding | size | kernel time per cell | kernel memory per cell |
|---|---|---|---|
| E2h | n = 48, k = 8 | 0.19 ms | 15.9 kB |
| E4 | n = 48, k = 8 | 0.32 ms | 32.5 kB |
| E1 | n = 32, k = 8 | 0.55 ms | 53.2 kB |
| E2 | n = 32, k = 4 | 0.52 ms | 168 kB, growing with the table size |
| E3 | n = 8, k = 2 | 36 ms | 5900 kB, growing with the table size |

### 5.2 Negative controls and tactic variants

At n = 16, k = 2 (E3: n = 8, k = 2). Every control differs from the positive file in one number
and its theorem states `leafCheck … = false`, proved by `decide +kernel`; the generator asserts
with the Python reference check which of (A), (B), (C) fails.

| variant | change | claim | E1 | E4 | E2 | E2h | E3 |
|---|---|---|---|---|---|---|---|
| `negL` | `L + 1` ((C) fails; the control that was asked for) | `= false` | proved | proved | proved | proved | proved |
| `negU` | one `u i + 1` ((A) fails) | `= false` | proved | proved | proved | proved | proved |
| `negP` | one `p i j + 1` ((B) fails) | `= false` | proved | proved | proved | proved | proved |
| `negJ` | one `J` entry lowered: (B) fails only in the last cell of the last pair | `= false` | proved | proved | proved | proved | proved |
| `negJ0` | the same in the first cell of the first pair | `= false` | proved | proved | proved | proved | proved |
| `negL_claimtrue` | the `L + 1` data with the wrong claim | `= true` | rejected | rejected | rejected | rejected | rejected |
| `tac_decide` | positive data, `by decide` | `= true` | ok | ok | ok | FAIL | FAIL |
| `tac_rfl` | positive data, `by rfl` | `= true` | ok | ok | ok | FAIL | FAIL |

"rejected": exit status 1 and `check_ok` depends on `sorryAx`. For E1, E4, E2 the error is
`Tactic decide proved that the proposition … is false`; for E2h and E3 the tactic's failure
report itself fails (`Error pretty printing: maximum recursion depth has been reached`). That the
value is `false` is what the `negL` row proves.

Tactic variants: `decide` and `rfl` without `+kernel` first evaluate in the elaborator and then
the kernel checks the proof again. Where they work they cost both evaluations (E4, n = 32, k = 4:
tactic 2.9–3.0 s plus kernel 2.7–3.9 s, against 3.0 s of kernel time for `decide +kernel`; E2,
n = 32, k = 4: 2.9 GB against 1.7 GB), and they are subject to the elaborator's limits: for E2h
and E3 both fail with `maximum recursion depth has been reached` (for E2h after the warning
`exponent 2048 exceeds the threshold 256, exponentiation operation was not evaluated`).
`decide +kernel` spends about 1 ms in the tactic. `native_decide` was not used anywhere.

### 5.3 Side experiments

| log | what | result | wall s | kernel s | elaboration s | peak RSS MB |
|---|---|---|---|---|---|---|
| `baseline_empty` | empty file | ok | 0.31 | - | 0.00 | 441 |
| `baseline_empty_ulimit6000000` | empty file under `ulimit -v 6000000` | FAIL: `failed to create thread` | 0.26 | - | - | 442 |
| `E1_n32_k8_dataonly` | tables and checker without the theorem | ok | 28.70 | 0.53 | 20.20 | 1025 |
| `E4_n48_k8_dataonly` | same | ok | 48.31 | 0.99 | 33.30 | 1468 |
| `E2h_n48_k8_dataonly` | same | ok | 11.58 | 0.06 | 10.50 | 521 |
| `E1_n32_k4_randmsg` | random 40-bit messages instead of zero | ok | 17.60 | 6.16 | 7.90 | 1201 |
| `E4_n32_k4_randmsg` | same | ok | 10.80 | 3.28 | 4.94 | 962 |
| `E2h_n32_k4_randmsg` | same | ok | 3.07 | 1.40 | 1.28 | 616 |
| `E2_n16_k2_randmsg` | same | ok | 0.58 | 0.11 | 0.14 | 476 |
| `E3_n8_k2_randmsg` | same | ok | 3.99 | 3.51 | 0.15 | 1085 |
| `E2h_n16_k2_oneliteral` | each table ONE hexadecimal numeral (1024 fields) | ok | 0.73 | 0.10 | 0.33 | 468 |
| `E2h_n16_k4_oneliteral` | same (4096 fields) | ok | 3.51 | 0.38 | 2.80 | 493 |
| `E2h_n32_k4_oneliteral` | same (16384 fields) | ok | 46.34 | 1.52 | 44.50 | 616 |
| `E4_n32_k4_oneliteral` | each table ONE list literal (15872 entries) | ok | 19.60 | 3.84 | 10.20 | 1249 |
| `E4_n32_k8_oneliteral` | same (63488 entries) | FAIL: `(deterministic) timeout at whnf, maximum number of heartbeats (200000)` | 35.12 | 0.03 | 24.90 | 1692 |
| `E1_n16_k2_plainnumerals` | `List Int` written `[-5, 3, …]` (960 entries) | FAIL: the same heartbeat timeout | 18.02 | 0.02 | 2.57 | 490 |
| `E1_n16_k4_plaindef` | tables as plain `def` (3840 entries) | FAIL: `maximum recursion depth has been reached` (code generator; the kernel had accepted definition and theorem) | 4.54 | 1.22 | 1.79 | 697 |
| `pitfall_thunk_chain` | toy loop, accumulator never inspected: 50000 / 100000 / 120000 steps | ok: 2.1 s / 4.6 s / 17.7 s | 24.68 | 24.30 | 0.02 | 1260 |
| `pitfall_thunk_forced` | same loop, accumulator matched in every step, same three sizes | ok: 3.0 s / 6.0 s / 8.6 s | 17.92 | 17.60 | 0.01 | 1486 |
| `pitfall_thunk_forced_single` | only the 120000-step theorem of the previous file | ok: 9.0 s | 9.27 | 9.01 | 0.01 | 1362 |
| `pitfall_thunk_forced_4theorems_aborted` | the three-theorem file with a fourth theorem (200000 steps) | FAIL: `std::bad_alloc` | 21.96 | - | - | 1610 |

## 6. What failed, and what limits it

**Memory per reduction step is the limit.** Peak memory grows in proportion to the number of
cells (table 5.1), i.e. to the number of reduction steps; it is not the size of the data (the
9.4 Mbit table of E2h, n = 48, k = 8, costs 0.08 GB to elaborate, the evaluation 1.1 GB). Even a
trivial loop costs about 8 kB and 60–75 µs per step (`pitfall_thunk_forced*`). The kernel
evidently keeps the terms it has reduced until the declaration is finished and gives the memory
back afterwards: three theorems of 50000, 100000 and 120000 steps in one file peak at 1486 MB,
the last one alone at 1362 MB; the sum would be about 2500 MB. Extrapolating the measured memory
per cell linearly, the 5 GB limit is reached near 2.7·10⁵ cells for E2h, 10⁵ cells for E4 and
6·10⁴ cells for E1 (E1 did fail at 72192). The first two are extrapolations, not measurements.
Whether splitting one check into several theorems is a way around the limit was not tested.

**Reads decide between encodings.**
- E3: in the kernel an `Array` is a structure around a `List`, and `Array.getD` walks it from the
  front, so every read costs steps proportional to the index: 36 ms and 5900 kB per cell at 256
  entries, above 5 GB at 1024 entries. A blow-up of the size the collaborators saw thus already
  occurs with arrays and integer arithmetic alone; how much `ℚ`, `Finset` and `Decidable` add in
  `verify` was not measured.
- E2: a read `(T >>> 64·t) % 2⁶⁴` is two steps, but its memory grows with the table: 1.3 GB above
  the empty file at 16384 entries, 1.1 GB more than E2h on the same tables. That is what one
  expects if every shifted copy (on average half of the 131 kB table, 15872 reads) stays in
  memory. By the same count 65536 entries would need about 17 GB; the run aborted at 3.2 GB
  resident under the address-space limit.
- E2h takes out the part of a site and the block of a pair in separate steps whose results all
  cells of that site or pair share, so large intermediate numbers are few (same tables: 617 MB
  instead of 1739 MB at 16384 entries).
- E1/E4 read nothing at random. E1 pays 1.6 times the memory of E4 per cell for `Int`: the kernel
  runs `Nat` arithmetic on literals natively and has to unfold `Int.add` case by case.

**Literals fail before the kernel is reached** (all in `logs/`; the remedies are generator
defaults):
- A `List Int` of plain numerals `[-5, 3, …]` with 960 entries hits the elaborator's
  200000-heartbeat limit. Remedy: constructor form `Int.ofNat 3`, `Int.negSucc 4`.
- One list literal with 63488 entries hits the same limit, and the elaboration time of one long
  literal grows faster than linearly. Remedy: the list as a chain of 128-entry constants
  `a :: b :: … :: next_chunk` (same flat list; 4.0 s instead of 10.2 s at 15872 entries).
  Elaboration is still half of the wall time of E4 (38 s of 77 s at n = 48, k = 8).
- One numeral with 16384 64-bit fields takes 44.5 s to elaborate, 16 times the 2.8 s for 4096
  fields: decoding a numeral is quadratic. Remedy: 256-field numerals combined with
  `Nat.add lo (Nat.shiftLeft hi bits)`, which the kernel evaluates once (1.3 s at 16384 fields).
- Tables as plain `def`: Lean's code generator fails on a 3840-entry list literal with
  `maximum recursion depth has been reached`, although the kernel accepted everything. Remedy:
  `noncomputable def` for the tables (the checkers stay computable).
- `#print axioms` reported `propext` in early versions (not logged), from sources unrelated to the
  evaluation: `Nat.land` and `Nat.lor`, whose definitions in core depend on it (`Nat.mod` and
  `Nat.add` are used instead), and equation-compiler matches with overlapping catch-all patterns
  (the patterns are now disjoint). The final files depend on no axioms.

**An accumulator that is never inspected** (`pitfall_thunk_chain.lean`). An argument such as
`Nat.add acc 1` that is passed on without being the scrutinee of a `match` is not replaced by its
value; after i steps it is a nested term of depth i. The time is proportional to the number of
steps up to 100000 (2.1 s, 4.6 s) and then explodes (120000 steps: 17.7 s; in probes that were not
logged, 125000 steps did not finish in 25 s, and with `+ 2` instead of `+ 1` the slowdown set in
earlier). Matching the accumulator in every step removes the effect (8.6 s for 120000 steps). We
did not look into the kernel for the cause; collisions of its expression hashes along such a chain
would explain the dependence on the term, but that is a conjecture. The checkers here keep every
such chain shorter than 2n.

**The prescribed limit `ulimit -v 6000000` cannot be used.** Under it `lean` 4.31 aborts with
`failed to create thread` on an empty file (`logs/baseline_empty_ulimit6000000.log`). In a probe
(not logged) a running `lean` had six 1 GiB anonymous mappings and VmPeak 7.2 GB at 0.5 GB
resident; with `lean -s 65536` the virtual size was 3.2 GB, so these are thread stacks. `run.sh`
uses `ulimit -v 12000000` (about 5.3 GB of real allocations) and `measure.py` additionally kills
a run whose resident memory exceeds 5 GB. `/usr/bin/time` is not installed; `measure.py` reports
the same `ru_maxrss`. An address-space limit has a side effect: `pitfall_thunk_forced` with a
fourth theorem ran through once (peak 2.2 GB, not logged) and aborted once with `std::bad_alloc`
at 1.6 GB resident. Not investigated; the main-table files contain one theorem each.

## 7. What is NOT done

- **No proof relates these checkers to `verify`.** Each theorem here says that one integer
  function returns `true` on one set of literals. It says nothing about `LeafOK`, `verify` or any
  energy bound; no Lean file in this directory mentions them. A proof would need, per encoding,
  (i) a decoding of the tables into `I : PairInstance n k`, `u`, `p`, `m`, `L` over `ℚ` (integer
  casts; for E2/E2h/E4 the field minus `off`, and `Lo − n²·off`), and (ii) a theorem for all n, k
  and all inputs: `leafCheck … = true → LeafOK I (fullDom n k) L u p m`. That is: the loops reach
  every (i, a) and every ordered pair i ≠ j with every (a, b); each index or stream position reads
  the entry the decoding assigns to it, also when a list is too short or a field out of range; the
  offset bookkeeping is right; the integer comparisons agree with the rational ones. `verify` on
  a leaf is `decide (LeafOK …)`, so the existing soundness theorems would then apply. The proof
  is about the checker for arbitrary inputs: it needs Mathlib but no evaluation. Its difficulty
  was not assessed.
- **One leaf, full domain.** `branch`, `prune` and `sum` nodes and restricted domains are not
  covered. A certificate with several leaves needs one such evaluation per leaf, or an integer
  checker for the whole tree, which was not written.
- **The checkers are tested, not verified.** Evidence: the Python reference check on the same
  data; one positive and five single-number mutations per encoding at one small size; one
  positive with random 40-bit messages per encoding (E1, E4, E2h at n = 32, k = 4; E2 at n = 16,
  k = 2; E3 at n = 8, k = 2). The certificate is tight, so a checker that summed the wrong
  messages would be expected to reject such a positive; no mutation was run with nonzero messages.
  In the main table the messages are zero, so the message arithmetic there adds zeros (or `off`).
- **Integers only.** Rational tables would first have to be scaled to integers; not examined.
- One seed, one run per configuration, a shared machine; no repetitions.
- Nothing above 5 GB or n²k² = 147456 was tried; the ceilings of E2h and E4 are not known.
- The files import nothing. Inside the project (Mathlib imported) the baseline memory is higher;
  not measured. Lower-overhead checkers (hand-written recursors, a tree of literals) were not
  tried.

## 8. Reproduce

```sh
cd /home/user/MetricChain/experiments/coordinator_checks/kernel_eval
./run.sh all          # everything, one lean process at a time, about 14 minutes;
                      # overwrites logs/<name>.log, rebuilds results.md and results.tsv
python3 collect.py    # tables from the logs only

./run.sh size E2h 48 8          # one size of one encoding (generate, run, log)
./run.sh controls E2h 16 2      # negative controls and tactic variants of one size
./run.sh ladder E4 8,2 16,2 16,4 32,4 32,8 48,8      # sizes in order, stop at the first failure
python3 gen.py --out generated --n 48 --k 8 --enc E2h   # only generate
```

What `run.sh` executes for one file:

```sh
export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH"; cd /home/user/MetricChain
( ulimit -v 12000000
  python3 experiments/coordinator_checks/kernel_eval/measure.py --rss-kill-kb 5000000 -- \
    timeout 600 lean --profile experiments/coordinator_checks/kernel_eval/generated/E2h_n16_k2.lean
) > experiments/coordinator_checks/kernel_eval/logs/E2h_n16_k2.log 2>&1
```

The `decide` / `rfl` variants run with `timeout 120`.

How the logs in this directory came about: one sweep `./run.sh all` (console output in
`logs/run_all.console.txt`). Afterwards seven runs were added or repeated one at a time, and
`run.sh all` now contains them: `E1_n16_k2_plainnumerals`, `E2_n16_k2_randmsg`, `E3_n8_k2_randmsg`,
`baseline_empty_ulimit6000000`, `pitfall_thunk_forced_single`, `pitfall_thunk_chain` (repeated
after a correction of its header comment), and `pitfall_thunk_forced`
(repeated after its fourth theorem was removed; the log of the aborted four-theorem run is kept
as `pitfall_thunk_forced_4theorems_aborted.log`, its source is the current file plus
`theorem t200k : g 200000 0 = true := by decide +kernel`). All 84 logged runs of generated files
regenerate with the recorded SHA-256 from the final `gen.py`.
