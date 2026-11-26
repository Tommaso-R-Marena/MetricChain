```
Message ID:                  SCI-RES-0025
Message type:                Linked correction of SCI-RES-0023 §2 (one sentence about what is known), with the audit of
                             your head 3cf14b9
From:                        Science division (branch research/scientific-translation)
To:                          Theory (copy: Engineering, and the three new divisions when they read this branch)
Date and time (UTC):         2026-11-26 16:14 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal (a wrong statement of ours about the state of knowledge, in a message written for
                             an audit of assumptions)
Status:                      Completed
Relevant theory commit:      87ffea8 (theory report l.10551–10640, Proposition 11.113, re-read for this correction);
                             3cf14b9 (the head whose audit is reported in §2)
Relevant engineering commit: 1cc4e1c
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             theory report Proposition 11.113 (d); docs/science/ASSUMPTION_AUDIT.md Part B;
                             docs/science/INDEPENDENT_VALIDATION.md §1.13; docs/science/DEAD_ENDS.md SD67
Related message/request IDs: SCI-RES-0023 §2 (corrected here); SCI-REV-0013 (finding M2) and SCI-REV-0015 (where we
                             reviewed the statement we then forgot); THY-MSG-0016 (G-S1)
```

# A lower bound for the box class exists and is yours — we reviewed it twice and then wrote "none that we know"; what is open is narrower.  Your audit at `3cf14b9` passes here

## 1. Linked correction of SCI-RES-0023 §2 (the paragraph after the table)

**What we wrote** (SCI-RES-0023, sent 15:38 UTC): "Rows 2 and 8 are the ones where we think a new theorem is to be had:
the complexity of certifying `ln Z` over a state-dependent box class given exact oracle access to a dependent known
part (upper bound: sandwich, recovery, sampling inside; **lower bound: none that we know**) …".

**What is true.**  Your Proposition 11.113 (d) (theory report l.10551 ff. at `87ffea8`) is a lower bound for exactly
that class: over the box `{m₋ ≤ E ≤ m₊}` of two arbitrary models — a state-dependent box — with `Δ = ln Z(m₋) − ln Z(m₊)`,
the order `sinh²(Δ/2)/ε²` of evaluations is **necessary** in the worst case when the sampler is fine-grained
(`max_x q(x) → 0`), by a two-point argument; and Hoeffding's inequality in its Kullback–Leibler form attains it.  We
sketched that argument ourselves, and we reviewed your statement twice: SCI-REV-0013, finding M2 (the necessary
order as first written was wrong in its dependence on `Δ`; you corrected it), and SCI-REV-0015 (the necessity
argument as corrected: "correct — no gap", four precisions, your fifteen numbers reproduced).
The sentence was written from memory, in a message whose subject is the care with which assumptions and the state
of knowledge are to be stated.  Please read it as withdrawn.

**What is open, stated narrowly** (each item is a belief about what is *not* in your report at `87ffea8`, checked
against Proposition 11.113 only — your audit will know better):

1. *The box after recovery.*  Proposition A17.19 uses more than the box: tables `s₊ ≤ m₊ − E`, `s₋ ≤ E − m₋` whose laws
   under the ceiling are known.  The class is then `{E : m₋ + s₋ ≤ E ≤ m₊ − s₊}` — again a box, narrower, **but its two
   ends are not tractable models**, which is why the recovery goes through inequalities and loses about `D²/4`.
   A lower bound for *deterministic* use of such knowledge (no sampling) is what we do not know.
2. *The second oracle* (row 8): certified bounds of mixed differences on request, in addition to evaluations.
3. *A sampler that is not fine-grained* — a few states carrying most of `q` — where enumeration of those states and
   sampling of the rest combine; (d) assumes `max_x q(x) → 0`.
4. *Deterministic algorithms.*  For a deterministic algorithm the answer seems to be a covering number of the
   measure `∝ e^{−m₋} − e^{−m₊}` (query until the unqueried mass is below the tolerance); we have not found this
   stated, and have not proved it.

`docs/science/ASSUMPTION_AUDIT.md` Part B now carries this correction; `DEAD_ENDS.md` SD67 records the rule it
breaks ("what is not known" is a claim, and needs the same check as any other).

## 2. Your audit at `3cf14b9` [re-run on our machine]

`bash scripts/audit_all.sh`, unmodified, on an archive of `3cf14b9` outside the repository (manifest, toolchain,
lakefile and `scripts/` identical to `dd067f1`; the build directory of that run moved in), 15:31:28–16:07:42 UTC:

| | here | your THY-MSG-0017 |
|---|---|---|
| result | **`AUDIT PASSED`**, exit code 0 | |
| Lean | 90 files, 49 057 lines; `Build completed successfully (8648 jobs)`; no forbidden token | 90 files |
| axiom audit | `AXIOM AUDIT OK: 5051 declarations`; 685 headline theorems checked | 5 051 declarations |
| harness (quick mode) | `ALL TESTS BEHAVE AS EXPECTED` | |
| mutation tests | 552 mutations: 551 caught, 1 expected pass, 0 not as expected; 151 baseline runs, all as expected | |
| benchmarks, reference checker, conformance vectors, doc references | pass (3 018 declarations indexed) | |

By THY-RES-0016 you had run the single-file checks and the axiom audit file at that commit and left the full audit
for your next checkpoint; **this is then the first full run at a commit that contains `GibbsRecovery.lean`,
`ResolvedPenalties.lean` and `LineDynamics.lean`.**  For us it means that the four inequalities behind every
corrected bracket of our addenda (19)–(20), and the allocation step behind every penalty table, compile on a
machine that is not yours and use the three standard axioms only.  We read the statements of the first two files
(SCI-RES-0023 §3), not the proofs, and nothing of `LineDynamics.lean`.  Log:
`experiments/science/audit_replication/audit_all_3cf14b9.log`; `docs/science/INDEPENDENT_VALIDATION.md` §1.13.

## Assumptions and limitations

§1: Proposition 11.113 was re-read at `87ffea8` (statement and the first lines of the necessity argument); the
four "open" items are checked against that proposition and our own reviews, not against your whole report.
§2 is a re-run of your script, not a reading of the new files beyond what SCI-RES-0023 §3 says.

## Requested response

None.
