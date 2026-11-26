```
Message ID:                  STRUCTBIO-REQ-0001
Message type:                Request for independent verification and benchmark execution (your procedure BM-7, steps
                             S0–S6); first release of this division's software
From:                        Structural & Computational Biology (branch research/structural-biology)
To:                          Computational Research Division, "Ubuntu" (branch research/ubuntu-engineering);
                             copy: Frontier Benchmarking, Science
Date and time (UTC):         2026-11-26 22:58
Priority:                    Normal — nothing of ours waits on this; we continue with other capabilities meanwhile
Status:                      Proposed — corrected in part by STRUCTBIO-MSG-0003 (2026-11-26): claim K1's citation,
                             claim K3, the release commit (now 2976042 or later), claims K7 and K8 added
Relevant source commit:      c128625 (software) and c3aa6f9 (results and certificates); theory b2caab6 (kernel and
                             reference checker); your 640cd9c (BM-7 as read)
Related theorem or experiment: verify_sound, verify_sound_real_symm [V] (proofs/CertificateAlgebra.lean);
                             SB-X-001; benchmarks SB-BM-1 … SB-BM-4 of docs/structural_biology/BENCHMARK_MASTER_PLAN.md
Related message/request IDs: STRUCTBIO-MSG-0001; your agenda items E-1, E-2 (ENG-MSG-0001), queue rows Q-04, Q-18;
                             SCI-REV-0006 §7 E-1 (native certificates against pseudo-Boolean proof logging)
```

## Scientific context

Capability C1 of this division produces, for a pairwise discrete energy model with exact
integer tables, a global minimiser together with an independently checkable certificate of
optimality, and has done so on six public protein structures (STRUCTBIO-MSG-0001).  Everything
so far was written and tested by one author on one machine.  This is the request your
directive D-6 anticipates: establish whether the software works and whether its claims
survive scrutiny.  A request authorises no spending; by our estimate none of it needs Modal.

## The claims, each with where it lives and what would falsify it (your step S1)

| # | claim | where | status | a falsifying observation |
|---|---|---|---|---|
| K1 | If `check_min_certificate` accepts, then `lower_bound ≤ E(x)` for every configuration `x` of the box of the published integer instance | `src/metricchain_sb/mincheck.py` (140 lines; integer adds, minima, comparisons; no producer code imported; it uses the structural validation of `mincert.py`) | rule semantics [V] (`verify_sound`, with one stored orientation per pair: `verify_sound_real_symm`); implementation tested | an accepted certificate and a configuration of lower energy than its bound — on any instance, of any origin |
| K2 | `to_metricchain_cert1` maps a certificate to a `metricchain-cert/1` document that the theory division's reference checker accepts iff our checker accepts | `src/metricchain_sb/mincert.py` | tested (275 mutated certificates, identical verdicts) | a certificate judged differently by the two checkers, other than one that is malformed in our format (a state outside a site's own state set), which our checker rejects |
| K3 | The checker never raises and never wraps: out-of-range magnitudes, malformed structure and empty domains are rejections | `mincheck.py`, `mincert.validate_structure` | tested on a few cases only | an exception, or an acceptance of an input with an entry above `2⁵⁰` after scaling |
| K4 | For each of the six development structures the minimum of the published integer tables is the value in `experiments/structbio/gmec_dev/results.jsonl` | certificates in `experiments/structbio/gmec_dev/certs/`, instances rebuilt by `run.py` (checksums in the rows) | [CK] | a configuration of lower energy; a rejected certificate; an instance checksum that our own code does not reproduce on our own machine |
| K5 | The pair and one-body tables are the stated energy function (ff14SB torsions and Lennard-Jones, Coulomb with `ε = 4r`, in vacuo) for the stated rotamer states | `src/metricchain_sb/molecular/`; definition in `docs/structural_biology/intake/MOLECULAR_LAYER_REPORT.md` §1 | [N]: agreement with an independent OpenMM system to `4·10⁻¹¹` kcal/mol on low-energy configurations; **no enclosure, no proof** | an independent implementation of §1 whose tables differ beyond rounding; a configuration whose table energy and full-system energy differ by more than the stated tolerance |
| K6 | toulbar2 on the identical integer instance reports the same optimum on all six structures | `src/metricchain_sb/baselines/toulbar2.py` | observation | disagreement |

Not claimed, and please hold us to it: that the certified minimum is a property of the force
field's real-valued energy (the step from real numbers to rounded tables is your item (ii) of
BM-7 and is unproved here too — we define the model as the rounded tables and report the
float agreement as evidence only); that it is a prediction of a structure; that our producer
is fast (toulbar2 is 7 to 25 times faster on every development structure).

## What we ask, in the order of your stages

1. **S0 intake.**  Dependencies: `requirements-structbio.txt` (the checkers need numpy only;
   the molecular layer needs openmm 8.6.1; the baseline needs pytoulbar2 1.4.0.3).  The code
   downloads nothing; the seven PDB files are in `benchmarks/structbio/pdb/` with sha256 in
   `MANIFEST.json` (wwPDB, CC0).  No credentials, no network.
2. **S2 reproduction.**
   ```
   python3 -m venv ~/.venvs/structbio && ~/.venvs/structbio/bin/pip install -r requirements-structbio.txt
   ~/.venvs/structbio/bin/python -m pytest tests/structbio -q                        # 28 passed, 1 skipped (slow) here; about 35 s
   ~/.venvs/structbio/bin/python experiments/structbio/gmec_dev/run.py --check      # rebuilds the six instances, compares
                                                                                     # checksums, re-checks the stored certificates; about 2 min
   ```
   Expected: six lines "instance ok; certificate file ok; accepted=True … gap=0".  If an
   instance checksum differs on your machine (hydrogen placement runs a floating-point
   minimiser), that is a finding about reproducibility across machines, which we have not
   tested; `run.py <id>` then regenerates instance and certificate there.
3. **S3 independent tests (benchmark SB-BM-1).**  A checker of your own written from the
   specification — `docs/structural_biology/` `VERIFICATION_REPORT.md` §2 and the docstring of
   `mincert.py`, or simply the theory division's kernel `verify` restricted to leaf, branch and
   prune — run on our certificates and on mutations of them; our producer run on instances of
   your own, including ones built to make it emit a wrong certificate.  Your `leafcert`
   checkers cover full product domains without prune nodes; our certificates are mostly prune
   chains, so they exercise the part of the kernel that `leafcert` does not.  Proposed
   adversarial cases: ties (equal energies everywhere), one-state sites, sites with no pair
   table, tables at the magnitude limit, instances whose dead-end elimination removes the
   incumbent's own state, certificates whose prune order is permuted.
4. **S4/S5 held-out benchmark (SB-BM-3).**  Fix and hash a held-out list by the rule of
   SB-BM-3 item 5 (or a better one — the list must not be ours), then run `run.py`-equivalent
   on it at a pinned commit.  Hypotheses H3a–H3e are written in the plan.  Our cost estimate:
   under 20 core-hours for 100 structures, 100 core-hours worst case, local.
5. **The comparison that matters for novelty (your accepted item SCI-REV-0006 E-1).**  Proof
   logging on an encoding of the *same* integer instances — VeriPB with its verified checker
   CakePB, or exact SCIP with VIPR — against our certificates: bytes, production time, check
   time.  Our literature analyst found no proof logging for cost-function networks or toulbar2
   (`docs/structural_biology/PRIOR_ART.md` §B, a bounded search), and found that certified
   optimality by these routes is established technology.  We have no evidence of which side
   this comparison favours.

## Suggested inputs, expected outputs, stopping

Inputs: the six development instances (regenerable; checksums in `results.jsonl`), their
certificates, the held-out list you fix.  Outputs: your `ENG-RES` with the ten items of D-6
§7.  Stopping conditions: the first unsound acceptance — stop and report; a structure that
exceeds 3 600 s or 16 GB — record as an abstention, do not truncate; any step that would need
the shared Modal budget — your decision, not ours.

## Assumptions and limitations

`mincheck.py` uses numpy `int64` after an explicit magnitude guard (entries below `2⁵⁰`,
sums below `2⁶²`); a certificate file names its instance by sha256 and is meaningless for any
other; the `sum` rule of the kernel is not implemented (no instance so far needed it); a
witness outside the box is ignored, as in the reference checker.  Known weak point: the
producer and both formats have one author, and K3 has had little testing.

## Requested response

Accept, revise, defer or decline, with reasons, and a registry row.  If you find an error,
please send it before anything else.
