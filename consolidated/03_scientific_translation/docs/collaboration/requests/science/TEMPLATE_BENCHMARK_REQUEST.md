# Template — a benchmark or verification request from the science division to the engineering division

*Not a message.  The form of every request of this division for a computation that is not a few minutes on its own
machine, since the research owner's directive of 2026-11-26 ("Ubuntu will coordinate substantial shared Modal
computations and benchmarking … send Ubuntu precise benchmark and verification requests"; verbatim in
`docs/science/OWNER_DIRECTIVES.md`, D-2, section 6).  The nine numbered fields are the directive's; the header is
the mailbox's.  A request is a proposal: it authorises no spending, and the engineering division decides whether,
when and how.*

```
Message ID:                  SCI-REQ-nnnn
Message type:                Benchmark / verification request
From:                        Science division (branch research/scientific-translation)
To:                          Engineering (copy: the division whose claim is evaluated)
Date and time (UTC):         from `date -u` immediately before the commit that first contains the file
Priority:                    High / Normal / Low, with the reason
Status:                      Proposed
Relevant theory commit:      exact commit
Relevant engineering commit: exact commit
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
Related message/request IDs:
```

1. **The mathematical claim being evaluated** — one statement, with its epistemic label as its owner gives it
   ([V], [P], [K], [N], [C], [H], [M]) and whose claim it is.  If the request is an audit candidate (ENG-MSG-0006 §2,
   agreed in SCI-RES-0022): "statement S is proved under H; believed / doubted under H′".
2. **The exact source commit** — branch and commit of the claim; file, section or Lean declaration.
3. **Required assumptions** — every hypothesis the computation must respect, and which one is being relaxed.
4. **The proposed computational method** — the algorithm, the arithmetic (exact, interval, floating point with
   which allowance), the code that exists (path and commit) and what must be written.
5. **Appropriate baselines** — what the result is compared with (brute force at small size, an independent
   implementation, a known closed form), and **the control that must fail**.
6. **Correctness criteria** — what counts as agreement, as a counterexample, and as "no counterexample in the
   following range"; the smallest instance on which S under H and S under H′ differ, if known.
7. **Expected outputs** — files, formats, the numbers we expect and when they were written down (a prediction
   registered before the run is named with its commit).
8. **Resource estimates** — CPU-hours, memory, storage, wall clock; whether Modal is needed at all; what a
   pilot at one tenth of the size would cost.
9. **Stopping conditions** — the budget at which the run stops whatever its state; the first result that makes
   the rest unnecessary; what is kept if it is stopped.

*Limitations to state in every request:* what of the claim's source we have read and what not; what the request
does **not** test.
