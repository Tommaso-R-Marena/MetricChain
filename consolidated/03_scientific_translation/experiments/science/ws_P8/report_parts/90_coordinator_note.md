---

## Coordinator's note (added 2026-11-26 after the hand-back; not part of the workstream's report)

*Written by the coordinator of the science division.  Everything above this line is workstream
P8's text, unchanged (this file is `report_parts/90_coordinator_note.md`; `mk_report.py` without it
reproduces the report as handed back, byte for byte).  Scripts and logs of the checks below:
`experiments/science/p8_verification/`.  Kinds of check are kept apart: **review** (re-derived on
paper), **own code** (written by the coordinator, P8's code not imported), **re-run** (P8's code,
in a scratch copy), **read only**.*

### What was checked before this report was published

1. **Read in full** (1 695 lines), tables included where a number is quoted elsewhere.

2. **Theorem AH — review.**  Re-derived; the proof is sound.  Step (a): the remainder identity
   uses the order of the sites only to name "the `m` largest elements" of a set, so it holds for
   every total order, and `I_{m−1}` does not depend on the order.  Step (b): with the hosts of a
   term last, a host `l ∉ T` could precede `min T` only if all of `T` sat among the hosts after `l`;
   a term has at most two hosts and `|T| = m ≥ 3`.  Lemma T (P3's Theorem 3 per term) was re-read
   against P3's Lemma 2 and Corollary L1, which the coordinator re-derived when P3 was adopted.
   **One sharpening:** the hypothesis of request P8-T1, "a set `H_τ` of at most `m − 1` sites
   last", can be `|H_τ| ≤ m`, and that is sharp (item 3).

3. **Theorem AH — own code, a family built to break it**
   (`p8_verification/ah_synthetic_test.py`, log `ah_synthetic_test.log`).  The statement in the
   form the proof gives — for *any* function `τ` on a product with a host set `H`, `|H| ≤ m`:
   `|τ(x) − I_{m−1}τ(x)| ≤ Σ_{T ⊆ S(x), |T| = m} max{|Δ_T τ(z; x_T)| : z_l = x⁰_l for the hosts l ∉ T}` —
   was tested at every state with the **exact** restricted maxima (the smallest constants the
   theorem allows) on two grids (108 and 144 states), `m = 2, 3, 4`, every admissible number of
   hosts.  On sums of random products `c·∏_{i∈U}[x_i ≠ x⁰_i]` whose first factor contains all hosts
   (9 900 functions): **no violation in 1 166 400 (function, state) checks, and the inequality
   is attained with ratio exactly 1** at states with more than `m` sites off the anchor.  Three
   deliberately wrong versions all fail on the same family: the anchor context only (control A),
   one host more than the hypothesis allows, `|H| = m + 1` (control B — so `|H| ≤ m` is sharp),
   and the roles of hosts and non-hosts exchanged (control C).  *A warning kept in the log:* on
   i.i.d. Gaussian tables — the family of my first version — eleven of these controls do **not**
   fail (a sum of many maxima against one number is a weak test); a test on that family alone
   would have "confirmed" false statements.

4. **The hypothesis the certificate needs, at every state — own code for the left side**
   (`p8_verification/lys_enum_check.py`; logs `lys_enum_check_K4.log`, `_K5.log`, `_LKSEc5.log`).
   `|g(x) − I_{m−1}g(x)| ≤ Σ_{T ⊆ S(x), |T| = m} ĉ_T` with P8's constants 'Sb' and 'SAb', `g`
   evaluated here at every state and `I_{m−1}g` by a grid recursion of mine: Lys₄ (16 464
   states), Lys₅ (115 248), LKSE:5 (14 508), orders 3 to `n`: **no violation**; smallest ratio
   bound/remainder 12.1 (Lys₅, order 3) to 132 (LKSE:5, order 5).  P8's stored enumerations of
   `g` equal mine to `3·10⁻¹²` kcal/mol.  The same logs give the Boltzmann means under the true
   ensemble: the bound is 9 000 to 430 000 times the remainder there ('SAb': 9 000 to 420 000) — the room P8's §2.3
   describes.

5. **Request P8-E1 — done: the twelve-residue certificate re-run with another driver**
   (`p8_verification/lys12_rerun.py`; logs `lys12_rerun_K12_m5_w7.log`, `_m5_w6.log`, `_m4_w7.log`).
   Constants read from P8's files; site, pair and in-window triple sums formed by my own
   summation; the ball taken from P8's cache after its states were compared row by row with
   `pwmodel.ball_states` and 3 000 random values were re-evaluated (largest deviation 0).
   **All nine brackets of table T10 that were re-run are reproduced to every printed digit**
   (differences `0.0e+00` at both ends): order 5, band 7: `[516.847299, 517.444904]`,
   `[517.018944, 517.239333]`, `[517.032204, 517.223832]` (site / banded pair / banded triple:
   0.598 / 0.220 / 0.192 nats); order 5, band 6: 0.812 / 0.470 / 0.446; order 4, band 7:
   10.7 / 3.27 / 1.56.  The sandwich holds at 960 Gibbs states of a sample of mine (another
   seed), at 2 000 exact samples of the floor, and at the random states of item 6.
   Also checked there: P8's per-subset decomposition of P3's closed form (variant 'P3') against
   the closed-form sums as my driver computes them (totals over exclusion sets): `Γ₅`, every
   site sum and every pair sum agree to `3·10⁻¹⁴` relative.

6. **A check P8 did not make: uniformly random states at twelve residues** (same script).
   P8 checked the sandwich at Gibbs states and at samples of the floor — low-energy states.
   Here: 250 uniformly random states for each number `s = m … 12` of sites off the anchor
   (2 000 states at order 5, 2 250 at order 4), `I_{m−1}g` by my own formula from the raw ball
   values (self-tested against the grid recursion, `1.4·10⁻¹⁴`).  **No violation** for 'P3',
   'Sb', 'SAb'.  At order 5 the true remainder `|g − I₄g|` is at most `8.3·10⁻⁴` kcal/mol even
   with all twelve side chains off the anchor, and the 'SAb' bound is 73 to 1 700 times above it
   (smallest ratio per `s`); at order 4: at most `0.067` kcal/mol, ratios 39 to 330.

7. **Re-run of P8's own validation chain for Lys₄** in a scratch copy of its directory
   (`p8_01_measure`, `p8_01b_restricted`, `p8_03_sr_validate`, `p8_03c_blockcheck`,
   `p8_10_order_identity`): the five logs equal P8's line by line after timings are removed,
   except that check B4 ran on two charge systems instead of four (I did not re-run the sign
   search that supplies the other two).

### What rests on what — to be read with the numbers above

* **Most of the gain is workstream P3's own theorem, evaluated without the merging step**
  (Proposition S; variant 'Sb'), as P8's "what is whose" says.  With 'Sb' alone the Lys₁₂
  brackets are, by my re-run: order 5, band 7: 0.623 / 0.226 / 0.196 nats; band 6:
  0.838 / 0.478 / 0.453.  Theorem AH ('SAb') adds 2–4 % there.  **At order 4 it adds a factor
  two**: 12.1 / 4.83 / 3.25 nats with 'Sb' against 10.7 / 3.27 / 1.56 with 'SAb' (band 7) —
  constants 7 % smaller, bracket halved, because at order 4 the floor is in the exponential
  regime.
* **The constants themselves were not recomputed by anyone but P8.**  Items 3–7 are a review
  of the theorem, necessary conditions at every state of three small instances and at 4 250
  random states of the large one, and re-runs.  P3's interval enclosures and per-state
  ingredients are inherited unexamined, as in every certificate of the division.

### Not checked by the coordinator

§1 and §2 of the report (the measurement of exact constants, the distance law) beyond reading;
the (LKSE)₃ run of table T10 (not re-run); the validation tables of §3.4 for instances other
than Lys₄; the first-order estimates of §4.1(ii); the timings.  Prior art outside our own
reports was not searched by P8 and not by me: nothing here is claimed as new beyond "not in
workstreams P3, P5, P6".

### What of this workstream is in the repository

Scripts, notes, logs, JSON files, `out/tables.md` and the report parts.  The division's
`.gitignore` excludes every `.npz` of a workstream as regenerable (§6 of the report says how);
the one exception, added on purpose, is the result itself: the per-subset constants
`out/g12_*.npz` and `out/g12b_*.npz` (24 files, 0.7 MB).  The balls and enumerations in `cache/`
and `out/` (2 GB) are not committed.  `logs/superseded/` — eighteen logs of killed or superseded
runs, which §6 of the report mentions and nothing cites — was not committed either (rule of the
division: a log is committed only from a run that reached its last line).

### What changed after this report (see addendum A17 (18) of `INFERENCE_LIMITS_ADDENDA.md`)

Two sentences of §4 are overtaken by work done on top of this report, and are left as written:
"at order 5 the certificate of Lys₁₂ is limited by the band" (§4.1) — the band's part comes
almost entirely from the way pairs beyond the band were split, and a split around the anchor
removes most of it; and the sampler arithmetic of §4.2(d), which is for the plain sampler —
the nested sampler needs no evaluation for most of the bracket.  Numbers: the addendum.
