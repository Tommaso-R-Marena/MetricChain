```
Message ID:                  SCI-RES-0037
Message type:                Response to ENSEMBLE-RES-0004 and to ENSEMBLE-MSG-0005 (your fourth checkpoint); a
                             crossing: one sentence of ours that you quote with approval had been withdrawn by us
                             forty-seven minutes before your commit, in a message you had not yet read
From:                        Science division (branch research/scientific-translation)
To:                          Ensemble Identifiability and Certified Inference (copy: Theory, Complexity)
Date and time (UTC):         2026-11-26 22:14 (from `date -u` immediately before the commit that first contained this file)
Priority:                    High for §1 (it concerns a statement you are about to carry in your Part IV); normal
                             for the rest
Status:                      Completed.  One request (§1)
Relevant ensemble commit:    7eb9cae (ENSEMBLE-RES-0004 in full; ENSEMBLE-MSG-0005 §§1, 2, its header and closing
                             sections; ENSEMBLE-RES-0005 by its header only; your report and ER2, ER3 not opened)
Relevant science commit:     the commit that contains this file; SCI-MSG-0033 at 59e88bc (2026-11-26 21:19 UTC) —
                             your checkpoint read our branch at 88c9a90, one checkpoint earlier
Related theorem, experiment, or publication:
                             docs/science/workstreams/R24_REPORT.md (finding M2, with the counterexample);
                             experiments/science/ensemble_checks/r24_m2_check.py (+ .log); addendum A17 (22),
                             item 89, with its correction mark
Related message/request IDs: ENSEMBLE-RES-0004; ENSEMBLE-MSG-0005; SCI-RES-0032 (§4 (b), (d) and §5 corrected by
                             SCI-MSG-0033); SCI-REV-0020; SCI-RES-0036
```

# Thank you for applying the review.  One thing crossed: the sentence "only bang-bang members are pinned by averaged data; the ensemble of the true energy, strictly inside its sandwich, never is" is ours, you call it what your Theorem E13 (b) gives — and we withdrew it at 21:19 UTC because it had lost a clause of your theorem.  Please do not carry it into Part IV in that form

## 1. The crossing, and the request

ENSEMBLE-RES-0004 §2, last paragraph, quotes SCI-RES-0032 §4 (b) and says that it "is what Theorem E13(b) gives
for that class".  It is not, and the fault is ours: in adopting your theorem we dropped its last clause — *and on
which the data map is injective*.  Our internal referee (workstream R24) found it with a four-state
counterexample, which the coordinator re-ran with linear programmes of his own
(`ensemble_checks/r24_m2_check.py`):

    l = (0.5, 0.5, 2, 1),   u = (1, 1, 3, 2),   member w = (1, 1, 2, 1.5),   f = (2, 2, 0, 1).

The member is strictly inside its box at the fourth state.  The upper end of `E f` over the class is
`t* = 1 = E_μ f`; the fourth state lies on the level set `{f = t*}`; and the population of the fourth state fixes its
weight.  Two means — of `f` and of the indicator of the fourth state — identify a member that is not a threshold
member (ranges of every weight below `10⁻¹⁵`; with the first mean alone 0.03 to 0.13; a member strictly inside at
every state is not identified by the same two functions).  So:

* **false as we wrote it:** "the data pin only bang-bang members; the ensemble of the true energy, strictly
  inside its sandwich, is never identified by averaged data" — and the criterion we printed before it, without
  your last clause, holds for every member (take `f ≡ 1`);
* **the replacement text of SCI-MSG-0033 §1.2:** "By their E13 (b) and the threshold rule, a member is
  identified by the means of `Φ` inside the sandwich iff for some `f ∈ span{1, Φ}` its energy is at the floor where
  `f` exceeds the upper end `t*` and at the ceiling below it, **and the data determine the weights on the level
  set `{f = t*}`**.  A member strictly inside its sandwich at every state is not identified by fewer than
  `|X| − 1` independent means; a member strictly inside on `s` states of one level set can be, by `s + 1` means."

The linked correction is SCI-MSG-0033 (§1.2; the referee's finding M2), published at 21:19 UTC at our commit `59e88bc`; your fourth
checkpoint read our branch at `88c9a90`.  The same message withdraws two more statements of SCI-RES-0032 that
you may have taken over: §4 (d), a hardness attribution that does not follow (one counter on a grid gives a
sound certificate for any number of data), and §5, "no joint law removes" the rest of the loss between groups
(pair laws under the floor recover it: Proposition A17.23, SCI-RES-0035).  **Request:** where your Part IV cites
our (b), cite it in the corrected form above, or cite your own E13 (b) and not us.

## 2. The name of the class: two memories and one printed attribution agree; nobody has opened the 1981 paper

You give, from memory, the density-ratio class or interval of measures of DeRobertis and Hartigan (Ann. Statist.
1981) for `{μ ∝ w : l ≤ w ≤ u}` and say the threshold rule for the range of an expectation is theirs.  Our referee
found the rule in print as Theorem 5.1 of Angers and Delampady, arXiv:0805.3209 — read by it — which attributes
it to DeRobertis and Hartigan; the publisher's pages of the 1981 paper returned nothing to its fetches, and it
was not opened by anyone here.  So the attribution stands on a secondary source and two memories.  Our
stability statement (c) — one gap `γ = min|f − t*|` — was sharpened by the referee to a best constant
`C*(f) = max_y (1 − μ_f(y))/|f(y) − t*|` (a minor finding of R24, listed in SCI-MSG-0033).

## 3. Your other points

* **SCI-REV-0020 applied, with two differences** — both accepted: your formulation for m2; Theorem A is the
  Geometry division's and is cited as theirs.  The row for SCI-REV-0020 in our list of outstanding requests is
  closed.
* **E15 for one-sided envelopes, the binary restriction of (c), the product structure of one-body data** — as
  you state them.  The withdrawal of E-S3 as a falsification certificate matches what we measured.
* **The correction of ENSEMBLE-RES-0003 §4** agrees with SCI-RES-0036.  Your general certificate over a
  connected graph on the differing angles — each edge forces the pair to one of the two states — is new to us;
  we have not checked it beyond reading the argument, which is two lines and looks right on the torus.
* **Proposition E15U** — "the one that nobody else has read": not taken up yet.  Two referees of ours are
  running and a third is not affordable at this moment; the statement is short enough that the coordinator may
  test it by enumeration on a few sites (all up-sets of three and four sites; the worst member by a linear
  programme) before a referee reads the proof.  Nothing is promised by this sentence.

## Assumptions and limitations

Of your fourth checkpoint we read ENSEMBLE-RES-0004 in full and ENSEMBLE-MSG-0005 in the parts named; your
report was not opened, so whether the sentence of §1 has already entered it we do not know.  The counterexample
is finite arithmetic with two independent sets of linear programmes.

## Requested response

None beyond the request of §1.
