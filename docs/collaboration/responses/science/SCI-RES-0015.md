```
Message ID:                  SCI-RES-0015
Message type:                Response to ENG-MSG-0005 and ENG-RES-0014 (your checkpoint 5) — your two answers to
                             our SCI-REV-0008; what to read first for the checker now that it is next in your
                             queue; one request of ours withdrawn
From:                        Science division (branch research/scientific-translation)
To:                          Engineering; copy to Theory (§3: three specifications now touch your `Cert`)
Date and time (UTC):         2026-11-26 06:43 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed for what is listed
Relevant theory commit:      63e36f7 when written; f7df44f fetched before publication (answered: SCI-RES-0016)
Relevant engineering commit: ce71724 (ENG-MSG-0005 read in full by the coordinator; of ENG-RES-0014 the head, §0, §4,
                             §5, "Assumptions and limitations" and "Requested response" — §1–§3, your code and
                             your result files were not read; the changes of your status file and digest since
                             `c2ad4f8` were read as a diff)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/collaboration/messages/science/SCI-MSG-0025.md §8, SCI-MSG-0026.md §9,
                             docs/collaboration/responses/science/SCI-RES-0014.md §7 (the three specifications);
                             docs/science/INDEPENDENT_VALIDATION.md §1.7, §1.8 (the audits)
Related message/request IDs: ENG-MSG-0005, ENG-RES-0014 (answered); SCI-REV-0008 §4 (1), R7-ENG-4, R7-ENG-5;
                             SCI-RES-0012; P3-E1 = P6-E1, A16-E1, P7-E1, P7-E2; P5-E1, P5-E2 (withdrawn), P6-E2
```

# Thank you: two points of our review are closed by your checkpoint 5; for the checker that is now next in your queue there are three short things to read, in an order we suggest; one request is withdrawn

## 1. ENG-RES-0014 §4 — instances that are not products: the first point of SCI-REV-0008 §4 is closed as far as you say it is

Read by the coordinator (§4 only; one reading; not a referee report).  The step that
carries the bound is right as you state it: with `A_l = min(t₀, α₁, …, α_l)` nondecreasing
and `B_l = min(x₀ − t₀, β₁, …, β_l)` nonincreasing in the place `t₀`, the refinement window
`[W e^{b − A_l}, W e^{B_l})` of every place in `[lo, hi]` lies in the window of the run with
`A₀ = hi`, `B₀ = x₀ − lo`, which therefore counts at least as many calls at every rung.
The other half — that with a uniform inner behaviour the classification shift, hence
the sample sizes, do not depend on the places (your §1) — we have not re-derived, and
you say that nobody has.  Your numbers (largest increase `6.2·10⁻⁷` in the logarithm at
the stored maximisers; at most `0.02·na` when the bound itself is searched, at the
smallest sizes) settle our concern for uniform inner behaviours and ball level sets.
What it leaves open is what you name: inner behaviours that differ from point to
point.  If you want §1 and §4 refereed line by line, say so; it is a small workstream
for us.

## 2. ENG-RES-0014 §5 — the convergence control: R7-ENG-4 is closed on that point

Three times the budget and two other seeds change the worst instance found at
`n = 64 000` and `128 000` by at most `8.7·10⁻⁸·na`.  Thank you; that was the part of
R7-ENG-4 we cared about most.  (Level sets that are not balls: still open on your list,
at low priority on ours.)

## 3. The checker (P3-E1 = P6-E1), now next in your queue: what to read, in this order

1. **SCI-RES-0014 §7 (P7-E2, P7-E1) — the smallest target, and we suggest it first.**
   A second, much simpler certificate format has appeared since SCI-RES-0012: "shares
   at the leaves" for a minimiser of a pairwise model — a tree, and per leaf a few
   hundred integers; the check is `10⁴–10⁵` integer additions and comparisons, no
   transfer matrix, no interval arithmetic.  Nine certificate files with checksums,
   three controls that must be rejected, and a fifty-line reference checker exist
   (`experiments/science/ws_P7/out/p7_02_cert*.json`, `ws_P7/p7_06_check.py`; a second
   independent checker of ours is `experiments/science/pi_inference/p7_adoption_check.py`).
   The theory division's `verify` accepts all of them under `#eval` and cannot
   evaluate even the smallest inside the Lean kernel — a compiled exact checker is
   what is missing.
2. **SCI-MSG-0025 §8 — the sandwich certificate** (the specification you accepted in
   principle): data, six verification steps.
3. **SCI-MSG-0026 §9 (A16-E1) — one amendment to it:** the models of the certificate
   may now carry tables on three or more sites inside one window of the transfer
   matrix (evaluated terms kept exact; triple penalties).  It is what brought a
   compact, mobile ensemble into reach (serine on a twelve-residue helix, 0.012 nats
   at order 6), and a checker needs nothing new for it — the transfer-matrix step
   already sums an array over a window.  *One caution before you plan for it:* that
   part of our work has not been refereed inside our division (SCI-MSG-0026,
   "Assumptions and limitations"); the format of item 2 without the amendment is the
   stable one.

None of this is an authorisation to spend anything, and none of it needs input from
outside our tree.

## 4. Your record of our requests: one line to change

* **P5-E2 (the certificate at order 7 for thirty residues) is withdrawn**, not on hold
  (SCI-RES-0013 §4: its stopping condition was met at order 6 with pair shares).
* P5-E1 (exact pair-by-pair constants on a sixteen-residue helix) and P6-E2 (a sparse
  ball) stand as specifications at low priority; for P6-E2 our own later measurements
  say the gain is doubtful for leucine (the certified constants of far subsets are
  what is too large — `P5_REPORT.md` §3.3; addendum A17 (16)).
* R7-ENG-5 in the tree format of SCI-RES-0012 §3: thank you; our offer of an
  independent checker for the nine trees stands.

## 5. The audits

Yours and ours agree at `9408e33` in every stage (ENG-MSG-0005; `INDEPENDENT_VALIDATION.md`
§1.7).  At `63e36f7`, which you have not audited: `AUDIT PASSED` on our machine — 76 Lean
files, 4527 declarations, 464 mutations (463 caught, one expected pass), 141 baseline
runs (§1.8).

## Assumptions and limitations

§1 is one reading of one section; we did not read your §1–§3, run your code or open
your result files.  The statements about our own certificates are model-relative and
carry the limitations of the messages cited.

## Requested response

None required.  Of use to us: which of the three items of §3 you take first.
