# Earlier, stopped attempts to verify the 400-level run (`u = 1`, `K = 4000`) with the independent checker

*Phase II, 2026-11-28.  Kept as evidence for `docs/phase2/R29_RESOLUTION.md` §4.2: two limitations of the
checker `review_a6/a6_02_verify_z6_output.py` at `K = 4000`.  Every file here is a log of a run that was
**stopped by hand before it finished**; none of them is a verification.  The verification that counts is
`../out_verify_z6_u1_K4000_levels_*.txt` with its summary `../out_verify_z6_u1_K4000_summary.txt`.*

| files | what was run | levels checked before the stop | what it shows |
|---|---|---|---|
| `run0_…` | the checker, unmodified, on all 400 levels in one process | 15 | 4 levels had a line the checker could not match to a parent; its cap test (C) failed at all 4: levels 7, 9 (the lowest line of the level, slack `−8·10⁻¹¹`) and 14, 15 (the cap line, slack `−10⁻⁵ … −2·10⁻⁴`) |
| `run1_…` (three ranges) | `verify_z6_chunk.py` with the loop range as its only change | 66 | 22 cap tests, **all 22 failed**: 17 on the cap line, 5 on the lowest line (levels 7, 9, 152, 153, 154) |
| `run2_…` (three ranges) | the same with the refinement loop for the cap test | 51 | 18 cap tests: the 14 on a cap line **pass after one round of refinement** (least slack about `+10⁻⁵`); the 4 on the lowest line still fail, by `−10⁻¹⁵` (levels 7, 9, 152, 153) |

The two causes, both in the checker and neither in the certificate:

1. **Cap test.**  The checker compares the cap line with lines of its own at sample points chosen on the
   assumption that the cap becomes active at a vertex of the hull of the other lines.  At `K = 4000` it becomes
   active inside the last linear piece; the sample degenerates and the (sufficient) comparison fails although
   the checker's own line through the failing vertex lies above the cap.  More of the checker's own lines
   near the vertex of least slack settle it.
2. **Search for the parent of a line.**  For each stored line the checker ranks all lines of the previous
   level by a floating-point margin and tries to *prove* the six best.  For the lowest line of a level the
   margins of the true parent and its neighbours are all of the order of `10⁻¹⁷`; the true parent was seventh.
   With the true parent the checker's own exact test proves the pair (level 7: witness
   `ρ = 0.49998406577536852469`).  Trying 60 candidates settles it.

Both changes are made in memory by `../verify_z6_chunk.py`; the acceptance criteria of the checker are
unchanged (an exact comparison at every vertex; an exact identity and a proved pair).
