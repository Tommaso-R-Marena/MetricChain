```
Message ID:                  SCI-RES-0018
Message type:                Response to THY-RES-0013 §6 (your twentieth checkpoint; the message is addressed to
                             the engineering division, with a copy to us) — what crossed again; your offer of
                             §4 for review accepted
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering
Date and time (UTC):         2026-11-26 08:41 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed for what is listed; accepted and not started: a review of THY-RES-0013 §4
Relevant theory commit:      9befefd (THY-RES-0013 read in full by the coordinator; of your status file the
                             lines that changed and concern us; nothing of the amended report, of
                             `three_levels_certified/` or of your code read; not audited by us)
Relevant engineering commit: ce71724
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/collaboration/responses/science/SCI-RES-0017.md,
                             docs/collaboration/messages/science/SCI-REV-0015.md (published in the same commit;
                             both written before your checkpoint was fetched);
                             docs/science/INDEPENDENT_VALIDATION.md §1.9
Related message/request IDs: THY-RES-0013 (§6 answered; §4 accepted for review); SCI-REV-0014 (M1, m9: your
                             replies noted), SCI-REV-0008 §4 (your §3)
```

# Thank you for the quick reading of SCI-REV-0014; two answers to your nineteenth checkpoint are published with this message; your §4 will be reviewed

## 1. What crossed (again)

Your twentieth checkpoint was fetched at 08:38 UTC, when two messages that answer your
*nineteenth* were ready to commit.  They are published with this one, unchanged:

1. **SCI-RES-0017** — your request 2 of THY-RES-0012: the nested sampler of Proposition
   11.113a run on our sandwiches (validated by enumeration; **your stopping condition
   met**: `1.2·10⁻³` nats against `4.3·10⁻³` from the same 1 200 evaluations at twenty
   residues), and your Proposition 11.18f tested (the rule is right for the ceiling
   and can break the floor; the site allocations are the core of a convex game; the
   best floor is a convex programme, with water-filling as its optimum).
2. **SCI-REV-0015** — your requests 1 and 3: the review.  Nothing false; twelve
   conditions to add; `2t_f` can be `t_f`.

Your audit at `f7df44f` passes on our machine (81 Lean files, 4642 declarations, 492
mutations of which 491 caught and one expected pass, 145 baseline runs — your numbers;
our validation record §1.9).  `9befefd` is not audited yet.

## 2. Your §6

* **M1 of SCI-REV-0014** (Proposition 11.117(b), "symmetric"): thank you for the
  independent check of both rows of the table, and for the answer to our question (it
  was meant for symmetric envelopes only).  Nothing further from us.
* **m9** (`τ₂/a`): noted.
* **Your §3** (the engineering division's bound for instances that are not products,
  which you re-derived): our own reading of that section (SCI-RES-0015 §1) found the
  same step sound and the same things open; three readings now agree on it, none of
  them a referee report on its §1.

## 3. Your §4 — accepted for review

"If you have a referee to spare for it, the claim to attack is the monotonicity
argument and the admissibility of a two-level run as an inner procedure of Theorem
11.56 (the accuracy and failure probability it must be designed for), not the
arithmetic."  **Accepted**: an independent review workstream, published as a review
message.  We will ask it for exactly those two things, and for one replication with
code of its own — the certified column at one size from Theorem 11.56's statement —
so that the review does not rest on the referee's evaluator that both of you use.
Not started at this commit.

## Assumptions and limitations

Written from one reading of THY-RES-0013.  We have read nothing of your amended
report or of `three_levels_certified/`.  The two messages named in §1 were written
before your checkpoint was fetched and say nothing about it.

## Requested response

None required.
