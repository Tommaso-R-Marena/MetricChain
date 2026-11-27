# An independent checker of the structural-biology division's partition-function certificates, and what it found (experiment X-018)

**Status of this report (Computational Research Division, 2026-11-27, written during the consolidation ordered by the
research owner).**  The work below was done by a subagent of this division for STRUCTBIO-REQ-0004 (items 1 and 2); the
report under the line is its own, unedited.  It was told to stop at the step in progress when the consolidation
directive arrived, which is why §7 lists campaigns that were written and not run.  **What the coordinator checked:**
finding F1 was reproduced by a direct call of the structural-biology division's checker written by the coordinator
(`f1_direct.py`; output at their commit `41fa668` in `results/f1_direct_41fa668.txt`; the same at `0544ff4`): the float
tier with `exp_bits` 990 or 991 accepts and returns an interval 0.31 nats below the true `ln Z`; the exact tier and the
float tier at the default 64 bits contain it.  The test file passes here (10 passed, 3 expected failures that stand for
F1, F2 and F4), and `report_numbers.py` prints the numbers of §§1 and 4 from the stored result files.  **What the
coordinator did not do:** read the independent checker (`indep_zcheck.py`, 982 lines), re-run the campaigns, or
confirm findings F2–F9 individually (F2 and F4 are exercised by the test file).  The independent checker is therefore
itself unreviewed code; where it and the structural-biology checker both accept, and both intervals contain a truth
computed by enumeration in ball arithmetic, three things would have to be wrong in the same direction for the
agreement to mislead.

---

# Independent verification of `structbio-zcert/1` (STRUCTBIO-REQ-0004, their commit 0544ff4) — hand-back at wind-down

All numbers below are printed by `experiments/eng/sb_zcheck/report_numbers.py` from the stored JSON files, except where marked "(terminal)".

## 0. First: one acceptance that misses an exactly computed value (their float tier, non-default `exp_bits`)

**F1 (critical by the task's definition).** Their checker in the float tier, called with `exp_bits=990` (or 991), ACCEPTS a certificate with no steps and returns `ln Z in [-677.000000000615, -676.999995836222]`; the enumerated truth is `ln Z = -676.68673831248177717` (0.31 nats above their upper bound). Smallest input:

- instance: 2 sites, `unary = [[0, 678], [0]]`, `pair = {(0,1): [[677], [0]]}`, `scale_bits = 0` (two configurations, energies 677 and 678), `beta = 1/1`, full box;
- certificate: `{"format":"structbio-zcert/1","model_sha256":"c93c651da1c591813d468f9e7016567b0ff08d906dfa92c6b0085c390ff51560","beta":"1/1","domains":[[0,1],[0]],"keep":null,"claim":{},"root":{"steps":[],"order":[1,0]},"meta":"{}"}`;
- call: `check_partition_certificate(cert, arithmetic="float", exp_bits=990)`.

Same certificate: float tier with `exp_bits` in {64, 500, 900, 950, 960, 965, 970-973, 975, 980, 985} contains the truth; 992 abstains; 993 and 1000 reject ("int too large to convert to float"); their exact tier contains the truth at every one of the 18 values tried; `indep_zcheck` contains it. Cause (read after the freeze): `FloatTables._ldexp_up` returns `1e-300` whenever the scaled exponent is below -2000, which is only a valid upper bound if the mantissa has fewer than about 1004 bits; mantissas have `exp_bits + k + 16` bits. **Scope:** it needs `exp_bits` near 990, never the default 64; it does not touch any number in their request. The docstring of `exp_bounds_me` says more bits "only cost time". Regression test: `test_finding_f1_float_tier_with_large_exp_bits` (xfail while present).

No other acceptance by either checker missed an enumerated value.

## 1. Verdict (three sentences)

On 96,559 certificates over 3,000 small instances, their exact tier accepted 19,437 and their float tier (default `exp_bits`) 19,408, and every accepted `ln Z` interval and every population interval (23,791 and 23,751) contained the 400-bit enumerated truth; `exp_bounds`/`log_bounds` were confirmed on 20,000 + 2,000 inputs with no violation. Claim Z3 as literally stated is false (the float interval failed to contain the exact-tier interval in 8,158 of 19,408 cases, by at most 2.09e-13 relative, both still containing the truth), and Z1 fails for the float tier at `exp_bits` 990-991 (F1). Z5 was NOT tested by a fuzz campaign (written, never run), and the Z3 magnitude and rounding-mode experiments were not run.

## 2. What was read, and the freeze

Before the freeze: the request; module docstrings, signatures and docstrings (via `ast`, no bodies) of `zcert`, `zcheck`, `expo`, `itables`, `model`, `modelio`; `mincert.py` lines 405-425 and 278-284 (bodies of `model_sha256`/`_model_to_json`, needed because no docstring defines the checksum; 16 unrelated lines of the other format's loader were on screen); the output of `zcert.dumps` on three hand-built objects (file layout by example). Frozen **2026-11-27 00:33:34 UTC**, sha256 `0a9d17a19c0ff2a7...` (982 lines); the file is unchanged since (a test asserts it). After the freeze I read the bodies of `zcert`, `zcheck`, `expo`, `itables`, `model`, `partition` to aim attacks. Nothing was written in their checkout (its `git status` is clean, no bytecode cache).

## 3. Specification gaps (15 recorded before the freeze) and the reading adopted

1. File layout in no docstring -> learnt from `dumps` output; exactly 8 top-level keys, unknown/missing keys are errors.
2. "Canonical rational" undefined -> `p/q`, lowest terms, `q>=1`, no `+`, no `-0`.
3. Checksum defined only as "canonical JSON" -> read from the body.
4. Keys of `children` -> canonical decimal strings.
5. Length of `f`, `g` -> one integer per state of the site.
6. Leaf `order` under conditioning -> all sites but `keep`, conditioned ones included (theirs agrees).
7. Prune validity -> `r`, `t` distinct states of the working domain; any margin sign (theirs agrees).
8. Admissible `beta` -> `beta >= 0` (theirs agrees).
9. Empty/unsorted/duplicate `domains` -> strictly increasing, non-empty. **Theirs accepts unsorted domains.**
10. Relax of an unlisted, reversed or already relaxed pair -> pair must be present, either orientation. **Theirs accepts only the listed orientation.**
11. The returned interval is implementation-defined, so claim acceptance depends on the checker and tier.
12. `populations` structure / states outside the root box -> all root states reported; `(0,0)` outside.
13. Branch on a one-state site allowed; surplus children are errors. **Theirs ignores children for states outside the working domain.**
14. `meta`, optional keys, key order, whitespace -> `meta` an uninterpreted string; all keys required. **Theirs requires `meta` to be JSON text, and accepts files without `keep` or `meta`.**
15. Limits (depth, integer size, table budget) unstated -> abstentions.

Also: the docstring states the prune factor `1 + exp(-beta m)`; the implementation uses `exp(exp(-beta m))` (sound, looser).

## 4. Campaigns actually run

| campaign | cases | their accept / reject | agreement with ours | unsound acceptances | exceptions |
|---|---|---|---|---|---|
| Z1/Z2 differential, seeds 101+102 (3,000 instances, 655 s) | 96,559 certificates | 19,437 / 75,534; their checker not run on 1,587; 1 call no return in 30 s | both accept 16,525; both reject 73,688; only theirs 2,912; only ours 1,846 | 0 (`ln Z` 19,437 yes; populations 23,791 yes; none "no", none undecided) | 0 checker, 0 loader |
| - their producer | 2,766 (222 with conditioning; producer abstained on 234 instances) | 2,764 / 0 (2 not run) | 2,764 both accept | 0 | 0 |
| - `gen` producer (trees theirs would never emit) | 6,000 | 5,910 / 0 (90 not run) | 5,910 both accept | 0 | 0 |
| - adversarial variants (about 47 kinds) | 87,793 | 10,763 / 75,534 | 7,851 / 73,688; 2,912 only theirs; 1,846 only ours | 0 | 0 |
| float tier, claim removed, default `exp_bits` | 34,648 | both tiers accept 19,408; both reject 15,211; only exact accepts 29 | float contains exact: 11,250 of 19,408 | 0 (19,408 and 23,751 yes) | 0 |
| Z4 exponential (72.2 s) | 20,000 `q` x 12 `bits` values | - | lower and upper bound confirmed 20,000 / 20,000 by both references | 0 violated, 0 undecided | 0 |
| Z4 `log_bounds` | 2,000 | - | 2,000 / 2,000 confirmed both sides | 0 | 0 |
| loader cases (`findings_repro.py`) | 35 files | loaded 15, refused 13, raised 7 | 8 loaded by theirs and refused by ours | - | 7 non-`Malformed` exceptions |

- Ours: accepted 18,924 (155 of them in rounded mode); all contain the truth (populations 22,304); 0 internal errors.
- All 4,758 verdict disagreements fall in three reading classes: unsorted domain 2,576 and surplus child 336 (theirs accepts); reversed relax pair 1,488 + 358 (ours accepts). The accepting side contained the truth every time.
- Relation where both accept (16,525): the rules prove an "ideal" interval; ours encloses each end of it to better than 1e-60, so theirs must satisfy `their_lo <= ideal_lo` and `ideal_hi <= their_hi`. Held 16,525 / 16,525, and ours lay inside theirs 16,525 / 16,525 (populations 17,608 / 17,608). Their distance from the ideal, relative: lower end at most 1.086e-12, upper end without prunes at most 1.123e-12 (2^-40 = 9.095e-13, their logarithm slack), upper end with prunes up to 9.3e4.
- "Not run on 1,587": a pre-screen withheld their checker where a prune factor `exp(q)` had `q > 14` or an exponent exceeded 30,000 (see F3).

## 5. Findings

**Critical:** F1 above.

**Major**
- **F2 — Z3 as stated is false.** Float interval not a superset of the exact-tier interval in 8,158 of 19,408 cases (lower end above in 5,291, upper end below in 3,914; at most 2.09e-13 relative). Mechanism: the final `log_bounds` is not monotone (471 of 2,000 pairs `z1 < z2` gave `lo(z1) > lo(z2)`, worst 2.17e-15 relative). Both intervals contained the truth every time. Reproduction: `test_finding_f2_...`.
- **F3 — a prune with a negative margin.** One-site, 258-byte certificate, `unary=[[0,x]]`, prune state 0 by state 1: at margin -10 kT theirs returns upper bound 22016.465794 where the rule proves 0.000045 (truth 4.54e-5); at -15 kT 3269002.37 and 0.19 s. Ad-hoc probe, not re-run, under a 2 GB limit: -30 kT took 9.7 s and ended "rejected: MemoryError while checking"; -100 to -10,000 kT 8-19 s likewise; -20,000 kT no return in 30 s; 1.6 GB resident seen. Cause: `exp(rho)` is materialised as an exact rational. Not tested without a memory limit.

**Minor**
- **F4 — loader exception types.** `ValueError` for `beta` `"--5/3"`, a superscript digit, 5,000 digits, claim `"--1/1"`; `RecursionError` for 100,000 nested brackets inside `meta` and for conditioning nested 1,000 or 2,000 deep (990 loads, checks and dumps; 5,000 is refused properly).
- **F5 — loader laxness.** Loaded and accepted: `-0`, one-sided claim, unknown field in a step or node (silently dropped), a leaf with `children`, missing `keep`, missing `meta`, unsorted domain.
- **F6** — a model with no site (`ln Z = 0`) is "rejected: IndexError while checking".
- **F7** — 1,851 of 2,764 certificates carrying their own producer's exact-tier claim are rejected by their float tier ("claimed interval is narrower").
- **F8** — `exp_bounds_me` width at `bits=64`: median 2^-78 for ordinary `q`, but max 2^-56 at |q| about 1e9, 2^-29.6 near 2^64, and useless near 2^200 (always sound).
- **F9** — 29 cases where the float tier abstains ("lower bound ... not positive") and the exact tier accepts.

## 6. Cost (two small dense instances only; their producer's certificate without steps)

| instance (largest table) | their exact | their float | ours exact | ours rounded-128 |
|---|---|---|---|---|
| 6 sites x 3 states (729) | 0.054 s, 0.54 MB | 0.015 s, 0.08 MB | 0.037 s, 0.24 MB | 0.025 s, 0.16 MB |
| 8 sites x 3 states (6,561) | 0.705 s, 4.99 MB | 0.016 s, 0.47 MB | 0.318 s, 2.04 MB | 0.300 s, 1.16 MB |

Memory is the `tracemalloc` peak. Interval widths: theirs about 2e-11, ours 2e-85 to 4e-85 (exact) and 2e-37 to 3.5e-37 (rounded). Their `exp_bounds_me` costs 180-430 microseconds per call for ordinary `q`.

## 7. NOT done or not finished

- **Z5 fuzz campaign: `campaign_z5.py` is written and was never executed** (banner in its docstring; no result file; possibly buggy). Z5 evidence is only: 0 escaping exceptions in the differential and float-tier calls on well-formed JSON, plus the 35 loader cases. No malformed-object fuzz, no cyclic or shared nodes, no odd-parameter fuzz.
- **Z3 targeted attacks not run:** near overflow/underflow, long sums, subnormals, cancellation, huge `beta*E`.
- **Rounding-mode experiment (`fesetround` upward/downward) not run.** From reading alone I expect the outward `nextafter` steps to cover directed rounding; untested.
- The `exp_bits` window of F1 is stored for one instance only (990, 991); it depends on the energies and was not mapped.
- Seeds 103 and 104 of the differential were queued and stopped by me before starting.
- No megabyte-size certificate timing; `dumps` not tested beyond depth 990; no crambin-scale run; items 3 and 4 of the request untouched.
- In my own code, never executed: the command-line entry and `model_from_json` of `indep_zcheck.py`; `truth.mp_ln_z` (so the enumerated truth rests on Arb balls only, not cross-checked with mpmath in a campaign). The Taylor exponential path was exercised in the test file only.
- Pre-freeze self-test scripts were scratch and are not kept; their substance is in the test file. `gen.py` was extended after the freeze (margin-aware producer, `temper`, `hazard`); it is test infrastructure, not the checker.

## 8. Files and commands

Everything is in `experiments/eng/sb_zcheck/` plus one test file; no absolute paths, user names or addresses in any of them (grep clean). Nothing committed, git untouched. The checkout path comes from `$SB_CHECKOUT`, default `MetricChain-sb-0544ff4` beside the repository.

- `indep_zcheck.py` — the frozen checker
- `truth.py` — enumeration with Arb balls
- `gen.py` — instances, producer, variants, hazard estimate
- `sb_bridge.py` — imports their package, records every exception
- `campaign_z12.py`, `campaign_z4.py`, `findings_repro.py`, `report_numbers.py`
- `campaign_z5.py` — NOT RUN
- `results/freeze.json`, `z12_seed101.json`, `z12_seed102.json`, `z4.json`, `findings.json`
- `tests/eng/test_sb_zcheck.py`

Commands (each script sets a 3 GB address-space limit itself):

```
python experiments/eng/sb_zcheck/campaign_z12.py --seed 101 --instances 1500   # 370 s; seed 102: 285 s
python experiments/eng/sb_zcheck/campaign_z4.py --seed 1 --cases 20000         # 72 s
python experiments/eng/sb_zcheck/findings_repro.py                             # about 14 s (terminal)
python experiments/eng/sb_zcheck/report_numbers.py                             # prints every number above
(ulimit -v 3000000; python -m pytest tests/eng/test_sb_zcheck.py -q -rx)
```

Test result (terminal): 10 passed, 3 xfailed (F1, F2, F4 still present) in 10.4 s; without the checkout 8 passed, 5 skipped in 4.1 s.

