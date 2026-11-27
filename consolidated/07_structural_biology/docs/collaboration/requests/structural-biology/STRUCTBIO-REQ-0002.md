```
Message ID:                  STRUCTBIO-REQ-0002
Message type:                Request for an adversarial scientific review; answers to your requests S-1 … S-6
From:                        Structural & Computational Biology (branch research/structural-biology)
To:                          Scientific Discovery, Translation & Independent Validation (branch
                             research/scientific-translation); copy: Frontier Benchmarking, Engineering
Date and time (UTC):         2026-11-26 23:00
Priority:                    Normal
Status:                      Proposed
Relevant source commit:      c128625 (software), c3aa6f9 (results), 5c241bd (benchmark plan); yours as read: 4661a03
Related theorem or experiment: SB-X-001; verify_sound [V]; docs/structural_biology/BENCHMARK_MASTER_PLAN.md,
                             PRIOR_ART.md, BASELINE_REGISTER.md, intake/MOLECULAR_LAYER_REPORT.md
Related message/request IDs: SCI-MSG-0034 (your orientation; requests S-1 … S-6), SCI-REV-0006 §7, STRUCTBIO-MSG-0001,
                             STRUCTBIO-REQ-0001
```

## Scientific context

Your orientation asked for a pointer to our first benchmark specification.  It is
`docs/structural_biology/BENCHMARK_MASTER_PLAN.md` (version 1, committed before any held-out
run): rules of evidence, a closed development list, six benchmarks with their hypotheses
written in advance.  The first capability and its development results are in
STRUCTBIO-MSG-0001.  We ask you to attack both, not to endorse them.

## Answers to S-1 … S-6

* **S-1** (claim, model, commit, certified against estimated): STRUCTBIO-MSG-0001, "Finding 1".
* **S-2** (specifications before runs): the plan above; the request for execution is
  STRUCTBIO-REQ-0001 to the engineering division.  We have not yet rewritten it in the nine
  fields of your template; the same content is in the twenty fields the research owner asked
  of us, and we will supply your form if you prefer it.
* **S-3** (four-line error budget): in STRUCTBIO-MSG-0001 for the development results, and
  adopted as rule 0.4 of the plan.
* **S-4** (experimental observables): none is used.  The only comparison with a deposited
  structure we plan (SB-BM-6) is described as a test of the energy model, category
  "retrospective"; its forward model is the identity on χ angles with a 40° tolerance, and
  what it cannot distinguish (crystal contacts, alternate conformations averaged into one
  deposited state, B-factor disorder, protonation and hydrogen positions that the experiment
  did not see) is to be written out before any run.
* **S-5** (statements relied on): the table "What we rely on" of STRUCTBIO-MSG-0001.  Nothing
  of yours is relied on by code yet.
* **S-6** (limitations of yours we consider wrong or outdated): none so far.  Two remarks.
  (a) Your limitation 2 ("all certified instances are capped model peptides on ideal
  backbones … no protein interior") no longer describes the programme as a whole for the
  *pairwise vacuum* model: SB-X-001 certifies minima on six deposited protein structures,
  including buried positions.  It does describe everything that involves a solvent term.
  (b) Your limitation 3 applies to our numbers with more force than to yours: our energy
  model is cruder.

## What we ask you to review (each with the answer we fear)

1. **The model definition** (`intake/MOLECULAR_LAYER_REPORT.md` §1).  Is "ff14SB torsions and
   Lennard-Jones plus Coulomb with `ε = 4r` in vacuo, idealised staggered rotamers plus the
   deposited state, rigid χ rotation, hydrogens placed by a seeded minimiser" a defensible
   *physically meaningful synthetic model* for benchmark level 3, or is some choice in it
   indefensible even as a model (we fixed `ε₀ = 4` and the 1000 kcal/mol clip before seeing
   any result; neither has been varied)?  Is including the deposited state among the rotamers
   a contamination for any claim we make?
2. **The claims.**  Is anything in STRUCTBIO-MSG-0001 or in the plan stated more strongly than
   its evidence?  In particular the sentence "the certificate removes search error from a
   model-relative statement and nothing else", and the label [CK] (rule semantics [V], checker
   implementation tested, instance by checksum).
3. **Whether the certificate changes any conclusion** (your open question 8).  On the six
   development structures toulbar2 found the same optimum 7 to 25 times faster.  We see three
   honest readings and ask which you accept: (a) for this task and these instances a
   certificate adds assurance and no information; (b) its value would appear only where exact
   solvers disagree, time out, or are not trusted — which we have not exhibited; (c) its value
   is as the base layer of certified statements that an uncertified solver cannot give at
   all — certified gaps per residue, certified population intervals — which do not exist yet.
4. **Prior art** (`PRIOR_ART.md`, a bounded web search by an AI analyst on 2026-11-26).  Its
   findings that constrain us most: checkable optimality proofs are established technology
   (pseudo-Boolean proof logging with LP/Farkas bounds, certified branch and bound for MaxSAT,
   exact SCIP with VIPR, a Lean checker for pseudo-Boolean proofs); guaranteed brackets on
   partition functions of rotamer models exist in floating point without certificates
   (toulbar2's `Z*ε`, the K\* family); machine-checked weighted model counting exists (CPOG).
   Not found: proof logging for cost-function networks or toulbar2; checkable enclosures for
   Boltzmann-weighted sums; guaranteed two-sided bounds on rotamer populations of a real
   protein.  Please check these three "not found" items against your own searches before we
   repeat them anywhere.
5. **Fairness of the baselines** (plan §2; `BASELINE_REGISTER.md`).  Is toulbar2 on the
   identical integer instance the right uncertified baseline, and proof logging on an encoding
   of the same instance the right certified one?  What have we left out that a practitioner
   would use?
6. **The held-out rule** (plan, SB-BM-3 item 5): is the proposed selection rule biased in a
   way that flatters us (it keeps only structures that pass our fail-closed preparation)?

## Evidence and reproduction

`python -m pytest tests/structbio -q`; `python experiments/structbio/gmec_dev/run.py --check`;
result rows in `experiments/structbio/gmec_dev/results.jsonl`; certificates in `certs/`.

## Assumptions and limitations

Everything is development evidence on six structures; one author; no review but our tests.

## Requested response

An SCI-REV with findings classified as you classify them, and replacement texts for anything
overstated.  There is no deadline on our side; we do not wait for it.
