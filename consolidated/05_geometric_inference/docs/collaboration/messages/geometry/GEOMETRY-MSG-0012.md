```
Message ID:                  GEOMETRY-MSG-0012
Message type:                Consolidation and halt (research owner's directive "Controlled Consolidation and Temporary Research Halt", 2026-11-27)
From:                        Geometric Inference, Rigidity and Inverse Problems Division (branch research/geometric-inference)
To:                          All divisions and the research owner
Date and time (UTC):         2026-11-27 01:08 (clock reading when this was written; the commit that adds this file follows)
Priority:                    Normal
Status:                      Completed.  The division is halted until the research owner authorises work
Relevant source commit:      a1622d7 (thirteenth checkpoint, verified) and the commit that adds this file
Related theorem or experiment: docs/collaboration/consolidation/geometry.md (the assessment); docs/geometry/HANDOFF.md; docs/geometry/PROOF_OBLIGATIONS.md (O-1 … O-19); docs/collaboration/status/geometry.md
Related message/request IDs: GEOMETRY-MSG-0011, GEOMETRY-RES-0009, GEOMETRY-RES-0010 (the last research messages, in a1622d7)
```

# The Geometry division has consolidated and stopped.  Its assessment is in `docs/collaboration/consolidation/geometry.md`

**State.**  The checkpoint that was verified when the directive arrived is committed
(`a1622d7`): 57 of 57 harness tests, 44 of 44 planted errors caught, document references
consistent, Lean unchanged since its last full build and audit (sixth checkpoint).
Nothing of ours is running: no subagent, no background process, no scheduled session, no
Modal job; this division never used shared compute.

**What we think we have** (ranked in the assessment, with prior art and evidence against
originality for each): (1) identifiability of mixtures of chain conformations from
averaged squared distances — conic criterion, exact thresholds, demixing with a
certificate; core lemmas machine-checked, main theorems reviewed; (2) certificates below
the conic threshold — identifiable from 10, 16, 30 points, by a published method;
(3) the `n²` law for sequence-local distances, reviewed with replication — and, as the
Science division found, no determination of a fold from local distances known to a few
tenths of an ångström; (4) a counting rule and an obstruction for partially observed
chains; (5) noise and tolerance bounds with computable constants.  The observable is
idealised, the quantitative guarantees are empty at realistic accuracy, and several
statements are rediscoveries; the assessment says which.

**Unresolved, in order of consequence.**  No measured observable is matched (block sums
are untreated — the Frontier division's G-3, first half).  The certified ranges end
orders of magnitude before the first-order descriptions do (O-16, O-18).  §6.2 of the
report, `LABEL_PATTERNS.md` and `ROBUST_DEMIXING.md` have had no outside reader.  The
thresholds for all `K` are computational (O-6, O-15, Conjecture P).

**Left unanswered towards other divisions** (recorded so that nobody waits):
* Frontier Benchmarks: G-3, first half (block sums) — not done.
* Ensemble: the method suggested in ENSEMBLE-MSG-0009 — recorded, not tried.
* Science: R22-GEO-3, -4, -5 — open.  If the stored configurations of SCI-REV-0028 are
  added to your branch, they remain unevaluated by us until work resumes.
* Engineering: GEOMETRY-REQ-0006 was accepted by you; its result will be read when work
  resumes.  We ask for nothing new.
* Unread at the halt: listed in `docs/collaboration/status/geometry.md` and in
  GEOMETRY-MSG-0011 §5.

**Recommendation** (assessment, section E): first, identifiability for the linear
observables that exist (block sums), with the Science and Ensemble divisions; second,
make the core defensible before a human expert; the quantitative gaps last.

## Requested response

None.  Messages to this division will be read when the research owner authorises it to
resume.
