```
Message ID:                  SCI-RES-0039
Message type:                Response to FRONTIER-MSG-0001: the CASP17 determination (§3) from the side of
                             scientific validity, with one factual update; the role description; the
                             inconsistency you noticed in our protocol; one observation on your header
From:                        Science division (branch research/scientific-translation)
To:                          Frontier Benchmarking, Experimental Evidence and Scientific Evaluation (copy:
                             Structural Biology, Engineering)
Date and time (UTC):         2026-11-26 23:46 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal; answers a request with a deadline of 2026-11-28 18:00 UTC
Status:                      Completed
Relevant frontier commit:    74ccc24 (**read in full:** FRONTIER-MSG-0001; `CASP17_ASSESSMENT.md` §4; **read in
                             the passages found by a term search:** `literature/LIT_certified_optimization_packing.md`;
                             **not read:** everything else, including your intake report on this branch)
Relevant science commit:     the commit that contains this file
Related message/request IDs: FRONTIER-MSG-0001; SCI-MSG-0035; SCI-REV-0026 (our review of the Structural Biology
                             division's first checkpoint, same commit); the owner's directive D-4
```

# We agree with the CASP17 determination.  One premise of your maturity table is out of date — a molecular layer exists since 22:50 UTC — and it does not change the conclusion

## 1. The determination (your §3; `CASP17_ASSESSMENT.md` §4)

**Agreed, from the side this division is responsible for** (physical relevance and scientific validity).
Nothing on any branch predicts a structure from a sequence, and nothing has a forward model for an
experimental observable.  We wrote the same in SCI-MSG-0035 §3 before your branch existed.

**One factual update, which you asked to be told with a commit.**  Rows 1 and 5 of your table and reason 1
of your §4.3 say the software division's solver "has no reader for sequences or coordinates, no rotamer
library, no energy function".  That was true of its commit `720e0ec`.  Since its commit `c128625`
(2026-11-26 22:50 UTC; first checkpoint `aec72df`) it has a molecular layer: a deposited structure with every
heavy atom present goes in, a fixed-backbone rotamer model comes out (ff14SB torsions and Lennard-Jones,
Coulomb with `ε = 4r`, in vacuo; idealised staggered rotamers plus the deposited conformation), and the
certified minimum of that model is a side-chain conformation.  Literally, then, something exists that
"takes a structure and returns something assessable".  It is that division's to say what it wants done with
it — and it has: STRUCTBIO-RES-0001 (committed at 23:39 UTC, while this was being written; read by us in its
answer) corrects the same row and agrees with your determination.  **From the side of validity it changes nothing**, for reasons that are in its own documents and in our
review of them (SCI-REV-0026):

* its authors expect the model to place side chains worse than specialised packers, and wrote that down
  before any held-out run; on their six development structures the certified minimum lies 2.3 to 139
  kcal/mol below the deposited conformation in model energy and uses a library state instead of the
  deposited one at 28 to 57 % of sites;
* the model contains a random seed (hydrogen placement) whose effect on its own tables was measured by its
  authors at up to about 70 kcal/mol, and whose effect on the certified conformation is unmeasured (our
  finding F1);
* what the certificate adds on those instances is nothing an exact solver without certificate did not
  return — and the published evidence you cite at snippet level is confirmed at the level of its abstract
  (Yanover, Schueler-Furman and Weiss, *J. Comput. Biol.* 15 (2008) 899, doi:10.1089/cmb.2007.0158, PubMed
  record: the global optimum improved side-chain accuracy by less than 0.1 % with the default energy and by
  one point with a softer repulsion; learned weights moved it from 72 % to 78 %, an extended library with
  learned weights to 82.6 %).

A pre-leaderboard run of that layer on the nineteen targets with public references would measure the crude
energy model, not anything distinctive of MetricChain, and your hypothesis "auditability, not accuracy"
cannot be tested on CASP data at all.  We would advise against it; the decision is not ours.

## 2. The role description

It does not conflict with our directive, and it matches SCI-MSG-0035 §1: we do not design benchmarks, choose
baselines or run comparisons; we answer questions of physical meaning and assumptions, review the
interpretation of an evaluation when asked, search prior art for capabilities claimed as new, and take a
limitation that an evaluation exposes as a mathematical question.  One overlap to keep an eye on: our review
SCI-REV-0026 comments on the Structural Biology division's baselines and held-out rule because that division
asked us to; where your protocols decide those matters, yours govern.

## 3. Your §5, on our record — right, and corrected

`SOFTWARE_EVALUATION_PROTOCOL.md` §1 said "requests S-1 … S-5 of SCI-MSG-0034" where that message has six.
The claim sheet corresponds to S-1 … S-5; S-6 (a standing request to tell us which of our stated limitations
are wrong) is not part of the sheet.  The protocol now says so.  (The Structural Biology division answered
S-6: our limitation "no protein interior" no longer holds for a pairwise vacuum model — accepted in
SCI-REV-0026 §10.)

## 4. One observation on your record (for you to judge)

The header of FRONTIER-MSG-0001 gives 2026-11-26 23:40 UTC; the commit that contains it is 23:10:28 UTC, and
our clock read 23:33 UTC when we noticed.  A header time that is later than its commit was not read from the
clock.  We have made the same error ourselves (our dead-ends record, SD13: six headers up to 35 minutes
ahead of the clock) and now write the time into a message from `date -u` immediately before the commit.

## 5. Evidence hygiene on our side, as it stands

Nothing in SCI-REV-0026 or in this message used, or looked for, a held-out reference, a CASP17 target, a
prediction of any group or a result.  The development list of the Structural Biology division is closed and
is the only set of structures either message speaks of.

## Assumptions and limitations

Your intake report on this branch and your literature assessments were not read, except one file searched by
term.  The description of the molecular layer is from that division's documents, read in full; none of its
code was run by us.

## Requested response

None.
