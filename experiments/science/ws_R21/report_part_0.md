## 0. Verdict in ten lines (version 1, `a570520`)

1. **E5, E6, E7, E8, E1.3 are proved as stated in the report** (with its definition of "generic", lines 434–436):
   every step re-derived, no gap found.  **No critical finding.**
2. The two cited theorems exist, are quoted correctly and their hypotheses are met (opened through a fetch tool:
   Garamvölgyi–Gortler–Jordán 2022, Theorem 3.5; Gortler–Healy–Thurston 2010, Corollary 1.15).
3. *Replication* (own code, plane): 549 908 non-constant splices of 64 random ensembles of two and three
   conformers on seven globally rigid graphs — **no chimera** by an exhaustive exact method (no control violated);
   the least-squares search crossed its pre-set threshold once (`7.9·10⁻⁷`, shown to be a positive minimum) and
   missed 64 things that exist.  Controls that must find a chimera found them (160 of 160; 320 of 320; D1).
4. **M1 (major).**  The reading of E1.3 ("mean squared distances determine nothing") holds on the free
   configuration space only.  With prescribed bond lengths a conformation in general position *is* determined by
   mean squared distances (Proposition A), and two generic conformers of a planar chain from seven bonds on [N].
5. **M2 (major).**  "Generic" means *jointly* generic.  For individually generic conformers the conclusion of E7
   fails: on `K_4` with no common edge length (Example D1, exact) and on the globally rigid graph `K_5 − e` with a
   shared triangle (Example D2).
6. **M3 (major).**  Exactness in numbers: the chimera gap behaves like `(K^{|E|})^{−1/c}` — `10⁻³` of a squared
   length for two conformers, `10⁻⁵` for three, on minimally globally rigid graphs; for E8, moments accurate to
   `10⁻⁵` still leave 3–76 % (`K_4`, three conformers) or 14–62 % (wheel, two conformers) of an explicit ensemble
   far from every conformer, and the certificate's own bound needs `10⁻⁸` to `10⁻¹⁹`.
7. **M4 (major, framing).**  E5 is a dimension count, E7 a four-line corollary of the cited 2022 theorem (whose
   published proof already splices two frameworks along a separator), E8 the classical per-edge certificate; the
   *reading* as identification of mixtures was not found in eighteen searches.
8. **Minor** (m1–m10 and five remarks on their scripts): a redundant hypothesis; "identification = absence of
   chimeras" holds in one direction only; the full dichotomy; reflections; `2K|E|` is not necessary (Proposition
   C); §5 items 2 and 4; graphs with connected rigidity matroid are more than the globally rigid ones; a stale
   number ("22 zeros", their output says 82).
9. *Re-run:* their `run_all.py` reproduces their `output.txt` exactly (timings apart).  With other seeds their
   check R5 fails 3 times out of 20 (a conformer is never reached — its control, not E8); R3 passes 4 of 4 but
   samples 180 splices of two conformers on a graph where the full set contains true negatives below its
   threshold (§4).
10. *Not checked:* `d ≥ 3` numerically; E1–E4, Part III, the Lean files; the cited papers were read through a
    fetch tool's extraction, not as pages.

