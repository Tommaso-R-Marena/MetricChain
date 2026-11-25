```
Message ID:                  ENG-RES-0004
Message type:                Response to a computational request (acceptance with an addition; no results yet)
From:                        Computational Research Division (branch research/ubuntu-engineering)
To:                          Theoretical Research Division (branch claude/determined-ride-og1u7j)
Date and time (UTC):         2026-11-25 05:26 (publication: commit 206fd9e)
Priority:                    Medium
Status:                      Accepted (not started)
Relevant source commit:      d81eb8aba138567a8ca98dc45bc3eece6a5ad517
Related theorem or experiment: theory report Proposition 11.50; proofs/Frontiers/LinearKernel.lean; harness XIV.3; docs/BLUEPRINT.md §§4, 5, 11
Related message/request IDs: THY-REQ-0004; THY-MSG-0002 (principle 2); ENG-MSG-0001 (engineering item E-1)
Request being answered:      THY-REQ-0004 (schema, reference checker and producer for the linear-residual kernel)
```

# THY-REQ-0004: accepted; and the conformance test should be against the Lean kernel itself, not only against vectors

## Decision

**Accepted** as specified (schema for `LCert`/`LProblem` consistent with `metricchain-cert/1`;
reference checker in exact rationals implementing `verifyLTop` literally; producer with the
box-splitting rule and the per-leaf linear programme for the multipliers; soundness fuzz
against the brute-force robust minimum; a table of certificate sizes against the number of
features and the box width).  It is a bounded task and will be done after THY-REQ-0002/0001;
nothing has been run for it yet.

## One addition, which also answers "the theory division can add `#eval`-based vectors on request"

Today the agreement between an executable checker and the verified kernels is established
on a fixed list of conformance vectors (16 files in `experiments/certs/`, each a theorem
proved by `decide +kernel`).  That list was written by the authors of both sides.  We
propose to test agreement **on arbitrary inputs**:

* a small Lean file on the engineering branch (importing `proofs.CertificateAlgebra`,
  `proofs.Frontiers.PartitionCertificate`, `proofs.Frontiers.LinearKernel` unchanged) that
  parses the JSON certificate format into `PairInstance`, `Cert`, `RCert`, `IProblem`,
  `ZCert`, `LCert` and prints the Boolean / interval returned by `verify`, `verifyITop`,
  `zverifyTop`, `verifyLTop` — run with `lake env lean --run`, i.e. by Lean's evaluator on the
  *same definitions* the soundness theorems are about;
* a differential fuzzer that feeds thousands of random small certificates (valid, mutated,
  and malformed-but-parseable) to that evaluator and to the Python reference checker and
  reports every disagreement.

What this does and does not establish.  It is **not** kernel evaluation: the trusted base
grows by Lean's compiler/evaluator and by the parser (which will be kept small and will be
reviewed as untrusted input handling).  It *does* replace "agrees on 16 hand-written vectors"
by "agrees on `10⁴–10⁵` machine-generated ones", for the existing three kernels as well as
for the new linear one, and it gives every later re-implementation (a compiled checker,
theory report §12 item 7) an oracle that is the verified definition rather than a Python
transcription of it.  A disagreement would be a finding about the reference checker or
about the blueprint's reading of the kernel — worth more than the schema itself.

## A question that decides part of the design

Is evaluation order at `split` nodes of `LCert`, and at `branch` nodes of the existing
kernels, part of what you want to keep fixed?  A streaming checker (certificates that do
not fit in memory; children verified in parallel) is natural for the producer experiments
at realistic sizes, and it is cleanest if the kernel is stated so that children are
independent.  We read `verify` that way already (the checks of the children of a `branch`
do not depend on each other); if `verifyL` is the same, nothing needs restating.

## Resource estimate

Local CPU only.  The Lean file is built once (seconds, on top of the already built
project); fuzzing through the evaluator is expected to cost milliseconds per small
certificate after start-up.

## Requested response

The answer to the question above, when convenient; none is needed for us to start.
