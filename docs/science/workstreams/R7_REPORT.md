# Workstream R7 — independent review and replication of the engineering division's results

*Status of this file: written section by section while the work ran (COMMON rule 3); sections marked
"(in progress)" are not final.*

Object reviewed: branch `research/ubuntu-engineering` at commit `a2f6dc781de05b642189a51d2ed88f94e8ed7026`
(every engineering file named below is cited by its path on that branch at that commit and can be
obtained with `git show a2f6dc7:<path>`; my working copy `experiments/science/ws_R7/eng_copy/` is
git-ignored and is re-created by `experiments/science/ws_R7/make_eng_copy.sh`).
My own code and outputs: `experiments/science/ws_R7/` (notes: `NOTES.md`).

Three kinds of evidence are kept apart throughout:

* **REPLICATED** — recomputed with my own code, written from the model definition *before* I read the
  engineering implementation of that item;
* **RE-RUN** — the engineering code, exported from the commit above, executed here;
* **READ** — read and checked for internal consistency only.

Labels of COMMON rule 6: **[V]** machine-checked, **[P]** paper proof given here, **[K]** known and
cited, **[N]** numerical evidence only, **[C]** conjecture, **[H]** heuristic.

(sections follow; in progress)

---
## DRAFT (21:04 UTC) — results so far, to be reorganised into the COMMON format

### X-004 generic chain (ENG-RES-0007, -0009): REPLICATED with own code, no numerical difference
* own enumerator (`own_gen.py`, breadth-first, no symmetry reduction, global clustering of distance values) written from
  P_REPORT §0 before reading any engineering file: conformations / classes for n = 5…14 identical
  (… 8 115/1 360, 19 559/2 908, 47 141/6 137, 113 587/13 012, 273 623/27 421);
* 12-cell cover table: all 60 cells n = 5…9 and all 12 cells n = 10 identical (two cells of n = 10 are the same brackets
  [209, 211], [119, 123] in both divisions' runs); "nearest tie" column identical for n = 5…12;
* entropy table σ(ρ), n = 5…14, six radii: identical to the three printed decimals; pairs-per-bead statistics identical;
* hard-core margins (0.078 above / 0.020 below at n = 10), "classes never closer than 0.035" (n ≤ 12): identical;
* exact ties: 5 at n = 11 (L = 1, ε = N/2), none at n ≤ 10 and n = 12: identical — and explained (they are polynomial
  identities in cos θ; see NOTES 20:50–20:59): at n = 13 there are 253 exact ties in the ε = N/2 cell and 4 in the ε = N/4 cell.

### X-003 Harper closed form (ENG-RES-0006): RE-DERIVED and REPLICATED, no difference
* own derivation, own brute force (90 cases, n ≤ 4, including an LP that does not assume the uniform sampler) and own table
  (explicit simplicial-order sets): all 52 stored rows identical; their script re-run regenerates the stored file byte for byte.

### X-002 lattice: certificates
* all 288 stored covers are valid covers of the stored class tables and have the published sizes (own exact checker);
* own enumerator (`own_dia.c`) reproduces the class tables n = 1…17 exactly (per class: count, fewest and most gauche);
* own tolerance-free LP bounds: equal to N_cov in 198 of the 216 cells with n ≤ 18; n ≥ 19 in progress.

### X-005 statistics: see NOTES 20:38–20:40 and 21:00–21:03 (refit, meaning of "7 095 840 mean runs", X-006 recount).

### Record: see NOTES 20:41–20:47 (stored rows n ≤ 18 produced by uncommitted code; second solver not run by the committed
driver; no script for the tie file; Modal-only entry point for the generic cover table).
