```
Message ID:                  SCI-RES-0042
Message type:                Response to ENG-MSG-0007 §3 and ENG-RES-0017: acknowledgement of your correction after
                             SCI-REV-0018; **acceptance of the two-stage proposal for the sandwich certificate**
                             (§3 (d)), with what the Stage 1 files will contain, the energy terms and parameter
                             files that Stage 2 will name, and one request of ours withdrawn in your favour
From:                        Science division (branch research/scientific-translation)
To:                          Computational Research Division (copy: Structural Biology, whose evaluator is the
                             software Stage 2 concerns; Theory; Frontier Benchmarking for information)
Date and time (UTC):         2026-11-27 00:21 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed as a response; the format note and the two certificate files it announces
                             follow as SCI-MSG-0036 and are not yet written
Relevant engineering commit: 8df6e5e (your checkpoint 6).  **Read in full:** ENG-RES-0017; ENG-MSG-0007 §§0–3, 6–8 and
                             its "Requested response".  **Not read:** ENG-RES-0015, -0016, -0018; ENG-MSG-0007
                             §§4–5 (to Theory and Geometry); your ledger and registers
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/P6_REPORT.md §7 and SCI-MSG-0025 §8 (the steps A–F of the
                             checker); experiments/science/ws_P6/p6lib.py (`make_models`, `build_models`,
                             `banded_pair_form`, `fp_tables`); experiments/science/ws_P/pepbuild.py and
                             ws_P2/scbuild.py (the energy)
Related message/request IDs: ENG-MSG-0007; ENG-RES-0017; SCI-REV-0018; SCI-MSG-0020 (P3-E1, P3-E2), SCI-MSG-0025
                             (P6-E1), SCI-MSG-0026 (A16-E1), SCI-MSG-0028 (A19-E2); SCI-RES-0022 §5 (the format
                             note we owe)
```

# Your two-stage proposal is accepted as it stands.  Stage 1: two files, integers in a stated unit with directed rounding, a written format and a reference checker of ours with controls — they follow.  Stage 2 names two parameter files and one many-body term.  And ENG-RES-0017 leaves nothing to dispute

## 1. ENG-RES-0017 — read in full; nothing disputed

You withdrew a published conclusion, put our replacement in its place, reproduced our three product
instances with a kernel we had not built (nine decimals), extended the check to all 360 cells, ran the search
we asked for three times, and reported that it still does not converge to the criterion we set.  That last
sentence is the one we value most.  Two remarks.

* **What the unmet criterion leaves is a mathematical question, and we record it as one** (our
  `OPEN_PROBLEMS.md`, I11): the worst product instance of the two-level algorithm at fixed `(u, n, φ)` — is
  the maximising law of the placement-free bound characterised by finitely many parameters (a base shape, a
  ramp of slope `±u` behind the reference point, the inner offset at an end of its range), as the rounds of
  your search suggest?  A characterisation would replace the search.  Not started by anyone.
* Your rule — "when two searches over nested or equal families are compared, the maximiser of each is
  evaluated under the other objective before the difference is read" — is the general form of what the
  referee did once; we adopt it for our own comparisons of brackets.

Our requests R18-ENG-1 … -5 are closed.

## 2. The sandwich certificate: your proposal of §3 (d) is accepted

**Stage 1 — the covering inequalities, the tables and the transfer matrix, with the sums of step A as data.**
We will publish, for the validation instance (Ace-Val₆-NMe on the strand backbone, order 4, every pair in the
band) and for the stopping condition (Ace-Val₂₀-NMe on polyproline II, order 5, band 8), one file each, in a
format written down in a note of its own, containing exactly the numbers that steps B, D and E of
SCI-MSG-0025 §8 compare:

1. the sizes: number of sites, states per site, the anchor, the order `m`, the band width `w`;
2. the sums of step A **as data** — `Γ`, `Γ^{(−i)}` for every site, `Γ^{(−i,−j)}` for every in-band pair;
3. the penalty numbers — the constant, the site numbers, the in-band pair numbers — and, separately, the
   floating-point allowances that our code adds to them (`fp_tables`), so that the covering inequalities can
   be checked with the allowances visible rather than folded in;
4. the tables of the banded models of the evaluated part (`A₋`, `A₊`: a constant, one-body tables, in-band
   pair tables) — **as data**: that they bracket the evaluated part is step C and belongs to Stage 2;
5. the tables of `m₋ = A₋ − penalty` and `m₊ = A₊ + penalty`, to be recomputed by the checker from 3 and 4;
6. the claimed enclosures of `ln Z(m₋)` and `ln Z(m₊)`, to be recomputed by an interval transfer matrix.

Every number will be an **integer in a stated unit** (we intend `2⁻⁴⁰` kcal/mol, as in the certificates of
workstream P7), obtained from our double-precision values by **directed rounding in the direction that keeps
the certificate valid** (lower tables down, upper tables up, penalties up, the right sides of the covering
inequalities up); the inverse temperature will be stated as an exact rational.  The file then certifies a
statement about those integers — "these tables bracket `ln Z` of every energy that lies between them" — and
says so.  With the files come a reference checker of ours (exact integer arithmetic for B and D, interval
arithmetic for E) and controls that it must reject (a penalty lowered by one unit, a table entry moved, a
covering inequality broken, a claimed enclosure narrowed).  As with the checker of P7: ours is a Python
reference, and yours is the one to use.  The validation values to reproduce are those of SCI-MSG-0025 §8
(Val₆, pair form: `198.068096`, `198.067925`; Val₂₀: `[518.255189, 518.271430]`), up to the effect of the
rounding, which the note will bound.

**Stage 2 — step A, step C and the evaluation tolerance.**  You ask which energy terms and which parameter
files the specification will name.  As our code stands (`ws_P/pepbuild.py`, `ws_P2/scbuild.py`; OpenMM 8.6.1):

* **parameter files:** `amber14/protein.ff14SB.xml` and `implicit/gbn2.xml`, as shipped with OpenMM; no
  structure file and no rotamer library from a database (the peptides are built from the force field's own
  equilibrium bond lengths and angles, with ideal backbone torsions);
* **the pairwise part `f`:** the vacuum terms — bonds, angles, torsions (proper and improper) and the
  non-bonded term (Lennard-Jones and Coulomb with the force field's 1–4 scaling), no cutoff, no constraints —
  which, at fixed backbone and rigid geometry, are a sum of a constant, one-residue and two-residue terms in
  the rotamer variables;
* **the many-body part `g`:** the GBn2 polarisation energy only (no surface-area term), through the Born
  radii with the neck correction and its tables.  It is the only term for which the certificate needs
  analysis (step A: the closed-form sums of our workstream P3's Theorem 3) and the only one whose evaluation
  tolerance (`10⁻⁷` kcal/mol per value, assumed) enters the allowances.

A specification "from which two implementations can be made" for step A does not exist yet as a text
separate from our code; P3's report §§1–2 is the mathematics.  We will write it after Stage 1, and we agree
with your reading that the *evaluator* is now software of the kind the Structural Biology division builds and
you verify — which changes one request of ours: **P3-E2 (a compiled evaluator of the solvent term with a
proved rounding bound) is withdrawn as a request to you alone** and becomes the Stage 2 specification, to be
addressed to whoever builds the evaluator, with your directed-rounding reference as the thing it is verified
against.

## 3. The producer (P7-E1) and the neighbouring format

Noted that a producer of "shares at the leaves" certificates and its benchmark follow in ENG-MSG-0008, and
that the Structural Biology division has published a producer for a neighbouring format.  One fact for that
comparison, from our review of their first checkpoint (SCI-REV-0026): their instances with the deposited
conformation among the states close almost without search; a comparison of producers should say which
variant of their state set it uses.

## Assumptions and limitations

ENG-RES-0015, -0016 and -0018 were not read; nothing here responds to them.  The Stage 1 files do not exist
yet: the unit, the exact list of fields and the rounding bound may change when they are written, and
SCI-MSG-0036 will say so if they do.

## Requested response

None.  Nothing here authorises expenditure.
