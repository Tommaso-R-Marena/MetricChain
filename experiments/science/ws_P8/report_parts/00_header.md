# Workstream P8 (science division) — the charged case: why the certificate stops at lysine and the patterned sequence, and which lever moves it

Report of an independent workstream of the Scientific Discovery, Translation & Independent
Validation Division.  Branch `research/scientific-translation`.  Everything is in
`experiments/science/ws_P8/` (running notes with dead ends and my own errors: `NOTES.md`; logs:
`logs/`; results: `out/`).  Written 2026-11-26, section by section while the work ran.

Labels: **[P]** proved here on paper (I say how it was checked numerically), **[M]** measured on
the named model by the named script (exact enumeration unless stated), **[N]** numerical
evidence only, **[C]** conjecture, **[H]** heuristic or physical reading, **[K]** known and cited
with the reading level.  Units: kcal/mol; `k_BT = 0.596161 kcal/mol` (300 K).  Every statement
is **model-relative**: it is about the finite function defined by OpenMM 8.6.1's GBn2 expression
on workstream P2's rigid synthetic peptides (Ace-X_n-NMe, ideal α-helix `(−57°, −47°)` unless a
strand is named, three-state grid per side-chain dihedral, P2's pruned product domain), exactly
as workstreams P3 and P5 set it up.  For lysine and the patterned sequence that product domain
is a *greedily pruned sub-product* of the clash-free domain (coordinator's note at the head of
`P3_REPORT.md`): every number below is about that sub-domain.  No sequence was varied, designed
or optimised; nothing here bears on a real peptide in water.  Numbering of statements: my
statements are called Lemma T, Proposition S, Theorem AH; P3's and P5's are quoted with their
own numbers.
