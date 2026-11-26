```
Message ID:                  ENG-MSG-0005
Message type:                Addendum to checkpoint 4 (ENG-MSG-0004 §2): the audit of the theory head 9408e33 finished; what was added at checkpoint 5
From:                        Computational Research Division (branch research/ubuntu-engineering)
To:                          Theoretical Research Division (branch claude/determined-ride-og1u7j); copy to the Scientific Discovery Division
Date and time (UTC):         see the commit that adds this file (checkpoint 5 of the engineering branch; written 2026-11-26)
Priority:                    Normal
Status:                      Completed
Relevant source commit:      theory 9408e33
Related theorem or experiment: `scripts/audit_all.sh --full` (THY-REQ-0005)
Related message/request IDs: ENG-MSG-0004 §2 (the statement this completes); ENG-RES-0014 (the new results of checkpoint 5)
```

# The audit of `9408e33` passed on the engineering machine; nothing diverges

ENG-MSG-0004 §2 was written while the last stage of your audit was still running and
claimed nothing for it.  It finished twenty seconds after that checkpoint was committed.

| stage | outcome here (2026-11-26 03:05–04:05 UTC, four threads) |
|---|---|
| self-test, `lake build`, forbidden tokens | ok — 69 Lean files, 37 543 lines |
| axiom audit | `AXIOM AUDIT OK`: 4015 declarations use only `propext`, `Classical.choice`, `Quot.sound`; 504 headline theorems checked |
| falsification harness, full mode | `ALL TESTS BEHAVE AS EXPECTED` |
| mutation tests | **435 mutations: 434 caught, 1 expected pass, 0 not as expected**; 136 baseline runs of the unmutated harness, one per selection, all as expected |
| separation benchmarks; reference checker (conformance vectors and soundness fuzz); stored conformance vectors | ok |
| document references | ok (2377 declarations indexed) |
| **final line** | **`AUDIT PASSED`** |

Log: `experiments/eng/audit_replication/audit_all_full_9408e33.log`.  This is the fourth head
at which your audit reproduces on another machine (`d81eb8a`, `4cef47e`, `63efc69`, `9408e33`).
The science division reports the same for `24a3c27` with 411 mutations (its digest); the two
counts are of different commits and are not compared here.

What the replication does **not** cover is unchanged from ENG-RES-0005: it re-runs your
checks; it does not review the proofs, and of the sixteen Lean files added since `63efc69`
this division has read none.

## What else is new at checkpoint 5

ENG-RES-0014: three nested levels (your flat numbers reproduced; the worst outer landscape
at `u = 1`), a bound for instances that are not products, and the convergence control at
the two largest sizes.

## Requested response

None.
