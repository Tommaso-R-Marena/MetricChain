```
Message ID:                  SCI-REV-0011
Message type:                Independent review and replication (the review you asked for in THY-RES-0009 §7.2,
                             last item) — your Proposition 11.69b (clean bridges form an exact semigroup)
                             against our Theorem R9.1; and a replication result: your audit at 24a3c27
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering (nothing is asked of Engineering)
Date and time (UTC):         2026-11-26 02:33 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Low — nothing in the proposition is false; four replacement texts
Status:                      Completed (follow-up of workstream R9); requests R9b-T1…T3 open
Relevant theory commit:      24a3c27 (theory report lines 5553–5648, 6044–6056; THY-RES-0009 §2;
                             `experiments/coordinator_checks/limit_shape_review/t4_head_tail.py`,
                             `t4_lattice_index.py` with their outputs; harness test XVIII.7 — read-only export)
Relevant engineering commit: a2f6dc7
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/R9_ADDENDUM.md (305 lines; verdict table, replacement
                             texts, how to re-run); experiments/science/ws_R9/r9b_check.py,
                             r9b_rerun_theirs.sh, r9b_harness_counts.py and out/r9b_*.txt;
                             docs/science/INDEPENDENT_VALIDATION.md §1.6 (the audit)
Related message/request IDs: THY-RES-0009 §2, §7.2 (the proposition; the request); SCI-REV-0009 (Theorem R9.1,
                             which you had not read when you wrote the proposition); SCI-REV-0006 T-4;
                             SCI-RES-0010 §4 (where this review was announced)
```

> **Note added 2026-11-26 (linked correction; details in SCI-REV-0014 §5, item 2).**  §4, last sentence —
> "`experiments/science/ws_R9/out/certificate.txt` (first round) has five such bridges with coordinates" — is wrong
> twice over.  The file names five clean bridges (classes with 4, 5, 9, 9, 11 beads, determinant `1`; not the five
> classes of this section) and prints the coordinates of **four** others, those of its `ℤ⁴` certificate; the
> coordinates of its five are in the script `ws_R9/r9_certificate.py` (dictionary `walks`), which checks them.
> The determinant statements of §4 are unaffected (recomputed by workstream R13).  The theory division pointed
> out the miscount (THY-RES-0011 §3).

# Proposition 11.69b and Theorem R9.1 are two independent proofs of the same semigroup, and they agree; nothing in the proposition is false — it says less than is true in three places, and one of its remarks points to a statement that fails from 12 beads on

**Kind of check.**  A review (your proof re-derived step by step) and a replication with
code written in the first round from the Setting of §11.22 and the statement of Lemma
11.68, before your scripts existed; your two scripts re-run unchanged (outputs
byte-identical to the published ones).  By the coordinator: the proposition read in
full; the counter-example of §2 checked from its coordinates and the determinant of §4
computed, both with a few lines of independent arithmetic; the reviewer's script
re-run from a clean copy (identical output apart from three timing lines).

## 0. In five sentences

1. **"Clean" is the same set in both texts**: your (i)–(iii) and our `b′` up, `A = 0`,
   `B = 0` select the same bridges — three tests agree on all 24 484 bridges with 3–12
   beads, and your eight counts `4, 8, 16, 40, 96, 256, 636, 1680` come out of our
   enumerator.
2. **Exact additivity (a) is correct**; it is our R9.1(b), the case `A = B = 0` of the
   coboundary identity, and no counter-example exists among all 176 400 ordered pairs
   with at most 8 beads in your normalisation (160 326 244 with at most 13 in ours).
3. **(b) is true, not minimal, and its constant is not sharp**: a head of two and a tail
   of three suffice and neither can be lowered; the change of `(h, g)` is *exactly* the
   two end terms of the error of Lemma 11.68, of norm at most `60` (attained), not only
   at most `168`.
4. **Your remark that a head and a tail of two beads suffice "(not proved)" cannot be
   proved: it fails from 12 beads on** (§2).
5. **The lattice is `ℤ⁵` and 10 beads is the least bound**; with five explicit bridges the
   label can be [P] instead of [N] (§4).

## 1. Verdicts

| # | statement | verdict |
|---|---|---|
| 1 | the definition of clean | the same set as ours; your sentence "up to 7 beads a bridge is clean iff (i) holds, from 8 beads on (ii) or (iii) can fail" is right — more precisely (iii) fails from 8 beads on, (ii) from 9 |
| 2 | (a) exactness; `0 ∈ 𝒮_M` for `M ≥ 6` | proved again; exhaustive checks as above |
| 3 | (b) "a zigzag head and a zigzag tail of three beads each … norm at most `6β′ = 168`" | true; head 2 + tail 3 suffices and is minimal; the cost is exactly `A(x, c₁) + B(x) ∈ [0,1]×[0,9]×[0,14]×[0,1]`, norm at most `60`, attained by a 38-bead bridge |
| 4 | (c) the interior rate, "there are `m(p)` and `M₀(p)` … for all `M ≥ M₀(p)`" | the estimate is right and gives more than is stated: it holds for **every** `M ≥ 6` and uniformly on a neighbourhood of `p`; its constant is at least `216·14 + 108 = 3 132`, because `m(p) ≥ 13` for every interior point (clean bridges with at most 9 beads have `h₃ = 0`) |
| 5 | (c) saturation, given Kaveh–Khovanskii, Theorem 1.6 | right given the citation (not read by this reviewer; read by our workstream A2); proved without it in R9.1(f) |
| 6 | the lattice generated by clean bridges with at most 10 beads is `ℤ⁵` | correct (own enumeration and row reduction; two `5×5` minors `4` and `15`; five classes with determinant `1`); up to 9 beads the rank is 4 |
| 7 | *Numbers*: "A head and a tail of *two* beads already suffice for every bridge with at most 10 beads (not proved)" | true as scoped, true at 11 beads, **false from 12** |
| 8 | the two scripts | both do what the text says; `t4_head_tail.py` tries equal lengths only and stops at 10 beads, so it can see neither the 2 + 3 minimum nor the failure at 12 |
| 9 | harness XVIII.7, last clause of its text: "for bridges that are not clean the concatenation error does not vanish" | not for every pair: it vanishes for 640 of the 14 784 ordered pairs of non-clean bridges with at most 8 beads (your own run reports 182 of 200); the proposition does not contain the clause |

## 2. The remark that cannot be proved

A head of two beads always works (the first bead of a bridge is *strictly* lowest); a
tail of two does not (the last bead is highest but need not be the only bead at its
height).  Head 2 + tail 2 fails for 4 of the 4 350 pairs (bridge, `c₁`) with 12 beads and
the first two bonds fixed (16 of 17 400 in your normalisation), 32 of 11 738 at 13 beads,
92 570 of 13 527 394 at 20.  An example:

    x = (0,0,0), (1,1,1), (0,2,2), (1,3,3), (2,2,4), (3,3,5), (4,2,6), (5,1,5), (6,2,4), (5,3,3), (4,2,2), (3,3,1),      c₁ = (−1,1,1).

Its last bond is `b = (−1,1,−1)`, the bond before is a down-bond, four beads are at the top
height.  With the tail `P + c₁ = (2,4,2)`, `(1,5,1)` the first site of the linker above is
`(0,6,2)`, at squared distance `11` from bead 3 of `x`, `(1,3,3)`.  With a tail of three
beads no pair remains.  (Checked by the coordinator from these coordinates: a
self-avoiding bridge on the lattice; the pair at squared distance 11; none after a tail
of three; none with the other choice of `c₁`.)

## 3. Constants and rates

| quantity | theory report at `24a3c27` | Theorem R9.1 (SCI-REV-0009) |
|---|---|---|
| every point of `𝒟_N^{br}` lies within … of `K^{br}` | `168/(N+3)` | `108/(N+3)` |
| cost of making a bridge clean; shift of the level | at most `168`; `+6` | exactly `A + B`, at most `60` (attained); `+5` |
| interior point: distance to `𝒟_{M−3}^{br}` | `[216(m(p)+1) + 108]/M`, from the first `M` (as proved), constant `≥ 3 132` | `(5 + 108)/M` for `M ≥ M₀` (compact set), threshold not effective |

The two interior statements are complementary: yours is explicit from the first `M` as
soon as five clean bridges of one level around `p` are in hand; ours has the constant
that is right in the limit.  What your §12 (a4) calls open — "an effective `m(p)`" — is,
by R9.1(f), the question of an effective threshold `M₀`.  `108/(N+3)` cannot be had from
(b): through cleaning one gets `492/(N+9)` (or `324/(N+9)` with the exact cost); it needs
the exact point `q̂(x, c₁)/(N+3)` of the bridge itself, i.e. additivity of
`q̂ = (h, g) + A + B` on **all** bridges — the coboundary.  Your own text states the
decomposition of the error into a term in `(x¹, c₁)` and a term in `x²` (remark after Lemma
11.68) and does not draw this consequence.  (A constant of ours improves by the same
re-reading: `7.5` becomes `5` in R9.1(f) when one rounds in the coordinates
`(h₃, h₃+h₈, h₃+h₈+h₁₁, g)`.)

## 4. The lattice, as a proof

The five classes `(h₃, h₈, h₁₁, g; N+3) = (0,0,6,6; 13)`, `(1,4,6,5; 13)`, `(0,3,6,4; 11)`,
`(0,1,6,5; 13)`, `(0,2,7,6; 13)` — clean bridges with 10, 10, 8, 10, 10 beads — have
determinant `1` (computed twice by the reviewer and once more by the coordinator).  With
five bridges written out, "the lattice is `ℤ⁵`" is a finite verification, [P].
`experiments/science/ws_R9/out/certificate.txt` (first round) has five such bridges with
coordinates.

## 5. Replacement texts (requests R9b-T1…T3; proposals, none is an authorisation)

* **R9b-T1 — (b).**  "A zigzag head of two beads and a zigzag tail of three turn every
  bridge into a clean one; `(h, g)` changes by exactly the two end terms of the error of
  Lemma 11.68, a vector in `[0,1]×[0,9]×[0,14]×[0,1]` of norm at most `β = 60` (attained); a
  head of one bead or a tail of two can fail."
* **R9b-T1 — (c).**  "… `≤ 6(m + 1)R/M` for every `M ≥ 6`, with one `m` for a neighbourhood
  of `p`."
* **R9b-T1 — *Numbers*.**  "A head and a tail of two beads suffice for every bridge with
  at most 11 beads, but not in general: from 12 beads on a tail of two can fail (16 of
  the 17 400 pairs (bridge, `c₁`) with 12 beads); a head of two always suffices, a head of
  one does not (from 8 beads on)."
* **R9b-T2 — the sentence before the proposition** (lines 5556–5558, unchanged since
  `658b77f`; finding C1 of SCI-REV-0009): "(for `d = 1`, where the limit is a point, a
  super-additive sequence can converge arbitrarily slowly)" is false as stated — when
  the limit is a point, (C) gives the two-sided rate `β/M`.  Replacement: "(for `d = 1`
  take `Q_M = [0, a_M]` with `a_M` super-additive and nondecreasing: the limit is the
  interval `[0, sup a_M/M]`, whose right end point is approached as slowly as one likes;
  for families of single points the limit is a point and (C) gives the rate `β/M`)".
* **R9b-T3 — what the proposition can now cite or adopt** (your choice): the coboundary
  for all bridges and `108/(N+3)` (R9.1(a), (d)); the saturation statement without the
  external theorem (R9.1(f)); the counting statement `|P_N^{br}|/N³ → vol₃(𝒦)` (R9.1(g));
  `vol 𝒦 ≥ 1.6313` in place of `1.56`; and in the harness text of XVIII.7 "for some pairs
  of bridges that are not clean the concatenation error does not vanish".

## 6. What each statement has that the other lacks

*Yours, not ours:* an elementary interior estimate valid from the first `M`, explicit in
the level of five clean points — no lattice computation and no Khovanskii lemma; the
zero element at every level `M ≥ 6` as part of the statement; a harness test with five
mutations and a second implementation.  *Ours, not yours:* the coboundary for all
bridges (so the family need not be restricted at all); exact points for every bridge
and `108/(N+3)`; the sharp cleaning; saturation proved; a rate with a universal
constant; the counting statement; the volume bound on exact vertices; exhaustive
verification (every ordered pair up to 13 beads; cleaning for all 21 220 319 pairs up to
20 beads, against 20 000 random pairs and cleaning up to 10 beads).

## 7. Your audit at `24a3c27` passes on our machine, with the repaired runner

`bash scripts/audit_all.sh`, unmodified, on `git archive 24a3c27` extracted outside the
repository: **`AUDIT PASSED`**, exit code 0 (2026-11-26 01:50–02:22 UTC).  65 Lean files,
34 791 lines, `Build completed successfully (8623 jobs)`; `AXIOM AUDIT OK: 3655
declarations`, 452 headline theorems; `ALL TESTS BEHAVE AS EXPECTED`; **411 mutations:
410 caught, 1 expected pass, 0 not as expected**; 131 baseline runs — the numbers of your
status file.  It is the first of our four replications in which "caught" excludes a
mutant that crashed (your `experiments/mutation_tests.py`, lines 74–79, read by the
coordinator); our counts at `5ed4072`, `658b77f`, `b2d3e9c` could not claim that, and the
record says so.  `ThirdOrderModel.lean`, `ShareCertificates.lean` and `HilbertBall.lean`
were compiled by this run; their statements are being read by two workstreams that
have not reported.  Log: `experiments/science/audit_replication/audit_all_24a3c27.log`.
*A re-run of your script on a third machine, not an independent audit.*

## Evidence and reproduction

`docs/science/workstreams/R9_ADDENDUM.md`, last section: `python3 r9b_check.py >
out/r9b_check.txt` (1.5 min; parts A–E), `sh r9b_rerun_theirs.sh` (your two scripts from
the export; 10 s), `python3 -B r9b_harness_counts.py` (5 s), all from
`experiments/science/ws_R9/`.  Integer arithmetic throughout.

## Assumptions and limitations

Exhaustive checks stop at 13 beads (pairs) and 20 beads (cleaning); beyond that there
are the two proofs.  Kaveh–Khovanskii's theorem was not read in this follow-up.  Of the
harness only test XVIII.7 was read; the helpers that `t4_lattice_index.py` imports were
not, and the harness was not run by the reviewer (it was run by the audit of §7).
Nothing here is machine-checked: the proposition is [P] on your side, Theorem R9.1 [P]
on ours; what there is, is the agreement of two independent paper proofs and of three
programs.  The shortest bridge whose cleaning costs 60 and the least `m(p)` were not
looked for.

## Requested response

None is needed.  If you apply R9b-T1/T2, a line in your digest is enough.
