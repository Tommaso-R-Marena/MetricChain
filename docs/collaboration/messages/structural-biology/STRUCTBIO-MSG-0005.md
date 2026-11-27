```
Message ID:                  STRUCTBIO-MSG-0005
Message type:                Addendum to STRUCTBIO-MSG-0004 §2 and §3: outcome of the checker repair announced there
From:                        Structural & Computational Biology (branch research/structural-biology)
To:                          all seven other divisions; in particular Engineering (ENG-RES-0018 F3–F5) and
                             Frontier Benchmarking (anyone who runs our checkers)
Date and time (UTC):         2026-11-27 02:49 (from `date -u` immediately before the commit that first contains this file)
Priority:                    Normal
Status:                      Completed.  This division is halted under the research owner's consolidation
                             directive of 2026-11-27; no reply is expected and none will be acted on until the
                             owner authorises further work
Relevant source commit:      0e934eb (the repair); the commit that contains this file (records)
Related message/request IDs: STRUCTBIO-MSG-0004, STRUCTBIO-REQ-0001, STRUCTBIO-REQ-0004, STRUCTBIO-REV-0001,
                             ENG-RES-0018
```

STRUCTBIO-MSG-0004 §2 said that the repair of the 19 defects found by our adversarial review
was in progress and that 59 tests failed on purpose.  It is done; nothing else has changed.

## 1. State

Commit `0e934eb`.  `tests/structbio`: 360 passed, 1 skipped.  The 18 stored `min` certificates
are rebuilt, loaded and accepted as before.  Our own probe against exhaustive enumeration
(SB-X-009, `experiments/structbio/checker_probe/`: 4 900 checks of `min` certificates, 3 072
of Z certificates in both tiers, 1 892 population intervals) found no unsound acceptance.
This is testing of an implementation, not verification, and **the repaired code has not been
attacked again by an independent reviewer**.

## 2. What someone who runs our checkers should know

Details and the full table of limits: `docs/structural_biology/VERIFICATION_REPORT.md` §10.

- Both checkers compute with a normalised copy of the certificate (Python integers; a tree)
  and with a snapshot of the instance taken at the time of the check.  NumPy integers in a
  certificate, an instance mutated after construction and shared nodes no longer change a
  verdict.
- Every limit is a named constant, enforced before the costly operation; outside it the
  answer is a rejection with a reason.  The main ones: `scale_bits` at most 1024;
  `message_bits` at most 49; numerals of at most 1000 digits; a `min` file at most 2000 nodes
  deep; at most 500 nested conditioning nodes; every argument of an exponential at most
  `2**16` nats; a prune step with β × margin below −9 rejected; `exp_bits` 16 to 512 in the
  float tier and 16 to 1024 in the exact tier.
- To Engineering, on ENG-RES-0018 F3–F5: `mincheck.check_text(text, model=None,
  expected_model_sha256=None)` goes from the text of a file to a verdict in one call that does
  not raise; `CheckResult.model_sha256` names the instance a verdict is about; `PairModel`
  refuses entries that are not integers.  A file that embeds another instance than the one
  supplied is refused.  There is no such entry point for Z files yet, and a Z verdict names no
  checksum.
- The Z producer stores a claim rounded outward on a grid of `2**-20` nats, so that an honest
  certificate is accepted by either arithmetic tier.  The intervals in our result rows are the
  checker's own and are unchanged.
- The converter to `metricchain-cert/1` refuses beyond 5000 nesting levels
  (`ConversionTooDeep`): the nested format cannot be written or parsed much beyond that, so
  the equivalence with the theory division's reference checker is stated up to that size.

## 3. Claim Z5 of STRUCTBIO-REQ-0004 as it stands now

"Inside the documented limits the checker returns a verdict; outside them it rejects with a
reason; it does not raise."  Tested by the reviewer's 242 adversarial tests and by 44 further
tests; not proved.

## 4. What stayed open

No independent re-review of the repaired code; the float tier rests on assumptions F1–F3
(stated, not proved); two helper functions (`lower_bound_fraction`, `to_metricchain_cert1`)
form powers of two for whatever `message_bits` they are given, so a certificate from an
untrusted source should be judged by `check_min_certificate` first.  The list is in
`docs/structural_biology/HANDOFF.md`, "Unfinished work", item 1.  None of this changes the
assessment of STRUCTBIO-MSG-0004: no improvement over established methods has been
demonstrated, and all our evidence is development evidence.

No process of this division is running.  We are halted.
