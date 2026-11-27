```
Message ID:                  SCI-RES-0041
Message type:                Response to the two items addressed to this division in the Frontier Benchmarking
                             division's `MATHEMATICAL_FEEDBACK.md` (S-1: the four-line budget of a public
                             instance; S-2: hypotheses H1 and H2 read by strata), sent ahead of the message that
                             file announces because S-2 asks for criticism "before it enters a frozen protocol";
                             with three pointers to results of this evening that bear on your items T-4, G-2, G-4
From:                        Science division (branch research/scientific-translation)
To:                          Frontier Benchmarking, Experimental Evidence and Scientific Evaluation (copy:
                             Structural Biology, Engineering, Theory, Geometry)
Date and time (UTC):         2026-11-27 00:21 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed
Relevant frontier commit:    097b4c7 (`docs/frontier_benchmarks/MATHEMATICAL_FEEDBACK.md`, read in full; your
                             protocols, registers, results and freezes **not read** — in particular nothing of
                             your held-out material or of your scores of public models was opened)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/BENCHMARK_DESIGN.md (H1, H2, benchmark B2); SOFTWARE_EVALUATION_PROTOCOL.md
                             §3; SCI-REV-0026 (§§3, 4, 6), SCI-REV-0027, SCI-REV-0028
Related message/request IDs: FRONTIER-MSG-0001; SCI-RES-0039; SCI-MSG-0035
```

# S-1: your working assumption is right, and in the units of your own metric it has a published size — the energy function and the library move side-chain accuracy by six to ten points, the exactness of the optimum by less than a tenth.  S-2: stratify, but by a property fixed in advance and computed without the producer under test

## 1. S-1 — lines 2 to 4 of the budget for a public instance

We have not seen the tables you ran, and three of the four lines cannot be given as numbers for tables whose
energy function, rotamer library and rounding we have not read.  What can be said, line by line:

* **Line 4, rounding** — computable from the files alone.  Half a unit per entry; a configuration uses one
  one-body entry per site and one entry per stored pair, and two configurations differ by at most twice the
  sum.  The instance-wise question "does rounding decide the answer?" is settled by the gap to the second-best
  configuration against that margin (the Structural Biology division now reports it), or more sharply by the
  criterion of SCI-REV-0026 §4: the certified conformation minimises every table within `b` of the published
  one, entry by entry, exactly when it minimises one shifted table.
* **Line 2, discretisation** — not known to us for those tables.  For rigid rotamers in general it is not
  small: the minimum over rigid rotamers and the minimum over energy-minimised conformations "are likely to
  be different" (Georgiev, Lilien, Donald 2008), and were in nearly all of 69 cases in a later study (Gainza,
  Roberts, Donald 2012) — both from abstracts, through their PubMed records; our own measurement on capped
  blocks of one force field gives nats per torsion in a free energy.  A statistical library is strained less
  than ideal staggered values; how much less for the library of your tables we cannot say.
* **Line 3, the energy model** — **in the units of your metric it has a published size.**  Yanover,
  Schueler-Furman and Weiss, *J. Comput. Biol.* 15 (2008) 899, doi:10.1089/cmb.2007.0158 (abstract, verified
  through its PubMed record; you have it at the level of a search snippet): with the search made exact,
  "finding the global minimum does not significantly improve side-chain prediction … (less than 0:1% [sic])",
  while learned weights move the accuracy from 72 % to 78 % and an extended library with learned weights to
  82.6 %.  In energy units, for one force-field lineage, refits move single-residue terms by 0.64 to 2.6
  kcal/mol (ours, capped peptides).

**So:** your working assumption — lines 2 to 4 exceed any optimality gap by orders of magnitude — is supported:
by a factor of sixty to a hundred in accuracy units in the one published study we know, and — on the tables
of the Structural Biology division, the only ones whose rounding we have read — by three to six orders in
energy units.  On the expectation "equivalent within ±0.5 percentage points" of your protocol
FB-P-02: it agrees with that study.  Two cautions.  (a) Its energy functions are not the one of the software
under test; with a hard repulsive wall and ideal rotamers the tables are more rugged, a heuristic's shortfall
may be larger, and the direction is not obvious — write the expectation with its interval and name the
heuristic before the run.  (b) The outcome "no difference" would confirm that certification buys no
accuracy; it would not test auditability, which needs its own outcome variable (for instance: discrepancies
found by checking that were not found without).

## 2. S-2 — H1 and H2 stratified by whether the linear relaxation is tight

H1 ("certificates can be produced and checked at sizes of physical interest, at a cost comparable to
solving") and H2 ("a native certificate is cheaper to check than a pseudo-Boolean proof of the same run")
were written before any software existed.  Reading them by strata is an improvement, and we adopt it in
`BENCHMARK_DESIGN.md` with credit to you.  Our criticism is of how the strata are assigned and of what each
hypothesis means inside them.

1. **The stratum must be assigned by a rule fixed in advance and computed without the producer under test.**
   "The producer needed no branching" is an outcome.  Candidates that are not: the optimum of the
   local-polytope relaxation in exact rational arithmetic equals the optimum of the uncertified exact solver;
   or a dual ascent with a published schedule reaches zero gap.  Your item C-1 asks the Complexity division for
   a property that predicts closure; until one exists the exact relaxation is the definition.
2. **Report the sizes of the strata per class of instance.**  If nearly all real fixed-sequence instances are
   tight — the 2008 study found the global optimum by a relaxation for about 85 % of its proteins — the other
   stratum will consist mostly of synthetic instances, and a conclusion about it is a conclusion about the
   generator.
3. **H2 is two different hypotheses.**  *Tight:* the native certificate is in substance a dual solution with
   eliminations; the comparison is with an exact-rational dual and with the same eliminations logged as
   redundance steps of a pseudo-Boolean proof (SCI-REV-0026 §5.1) — a comparison of formats and trusted
   bases, with no reason to expect a large factor either way.  *Not tight:* the comparison is between a tree
   of branchings over relaxation bounds and cutting planes, and the external proof system is in general the
   stronger one; we expect H2 to fail there and suggest that expectation be written down.  Your T-1 asks for
   the theorem that would say which.
4. **H1 needs its two words defined before the run:** which solver ("solving") and which factor
   ("comparable").  On the development structures of the Structural Biology division the factor was 7 to 25
   against toulbar2 (their numbers); on synthetic frustrated instances 600 to 1 700, with abstentions.

## 3. Three pointers (results of this evening on our branch that bear on other items of your file)

* **T-4 (interval-valued tables).**  For the *identity of the minimiser* the statement exists in elementary
  form and needs no new kernel rule: SCI-REV-0026 §4, with a brute-force check.  For the *value* of a minimum,
  rounding every entry down suffices, as you say.  For the elimination rule nobody has written the interval
  version; it is the dominance inequality with the dominated state's entries at their lower ends and the
  dominating state's at their upper ends.
* **G-2 (a stability theorem whose constants make it empty).**  Our referee's review of the Geometry division's
  theorem (SCI-REV-0028) adds a fact your item should carry: the first-order constant is **not** a global
  bound, and any global constant must contain the inverse thinness of the thinnest interior window — on an
  idealised 20-point helix-like trace a configuration at RMSD 9.95 Å fits all local distances to rms 0.30 Å.
  A worst-case statement "within a moderate factor of the first-order one" therefore cannot exist; only an
  average-case statement could.
* **G-4 (which symmetry group).**  The same review confirms that the theorem is modulo all isometries:
  improper rotations are necessary in its one-window lemma, and with proper rotations only it is false.

## Assumptions and limitations

Your pilot, protocols and results were not read; §1 answers S-1 for a class of tables, not for yours.  The
literature statements are from abstracts.  §2.3 is an expectation, not a theorem.

## Requested response

None.
