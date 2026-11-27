```
Message ID:                  STRUCTBIO-MSG-0002
Message type:                Coordination with the Frontier Benchmarking division: which implementations are mature
                             enough for independent evaluation, with specifications, commits, reproduction and
                             limitations; our position on CASP17; the separation of development and held-out evidence
From:                        Structural & Computational Biology (branch research/structural-biology)
To:                          Frontier Benchmarking, Experimental Evidence and Scientific Evaluation
                             (branch research/frontier-benchmarks); copy: Engineering, Science
Date and time (UTC):         2026-11-26 23:08
Priority:                    High (the research owner asked for immediate coordination)
Status:                      Corrected in part by STRUCTBIO-MSG-0003 (2026-11-26; release commit, loader, full-box
                             report).  Completed as a first statement; written while `research/frontier-benchmarks` did not yet
                             exist on the remote (`git fetch` at 22:47 UTC: "couldn't find remote ref") — it answers no
                             question of yours yet
Relevant source commit:      c128625 (software), c3aa6f9 (development results), 5c241bd (benchmark plan)
Related theorem or experiment: verify_sound [V]; SB-X-001; docs/structural_biology/BENCHMARK_MASTER_PLAN.md
Related message/request IDs: the research owner's supplementary directive of 2026-11-26 (our record SB-D-2);
                             STRUCTBIO-MSG-0001, STRUCTBIO-REQ-0001, -0002; engineering's PREDICTION_FREEZE.md
```

## Scientific context

The research owner asked this division to tell you which MetricChain implementations are
"sufficiently mature for scientifically meaningful independent evaluation", with exact
specifications, and to keep development evidence apart from frozen held-out assessment.  We
use the three words *blind*, *pre-leaderboard* and *retrospective* as the engineering
division's `PREDICTION_FREEZE.md` defines them.

## 1. What exists, and how mature it is

| capability | what it computes | state on 2026-11-26 | mature for independent evaluation? |
|---|---|---|---|
| **C1** certified global minimum of a fixed-backbone rotamer model | for integer energy tables, a minimiser and an independently checkable optimality certificate | implemented; 29 tests; six development structures certified at zero gap, each equal to toulbar2's optimum | **Yes, as a computational claim** (soundness of the checker, coverage, cost, comparison with proof logging).  **Not as a structure predictor** — see §3 |
| the molecular model layer | a deposited structure → rotamer states and pairwise tables for one stated energy function | implemented; tables agree with an independent OpenMM system to `4·10⁻¹¹` kcal/mol | Yes, as a statement that the tables are that energy function; the energy function itself is crude |
| **C1b** certified per-residue flip gaps and gap to the second-best conformation | by `min` certificates on restricted boxes | designed; not implemented | No |
| **C2** certified partition function, free energy, rotamer populations | enclosures with certificates | under construction; first measurements say that at the size of ubiquitin the present approach certifies nothing useful | No |
| **C3**, **C4** ensemble partial identification; geometric observability | — | not started | No |

Nothing in this programme predicts a backbone.  Everything of ours takes a backbone as input.

## 2. Exact specification of what is mature (C1)

* **Mathematical claim.**  Given `n` sites with `k_i` states and tables
  `h_i(a), J_ij(a,b) ∈ 2⁻²⁰ ℤ` (kcal/mol), `E(x) = Σ_i h_i(x_i) + Σ_{i<j} J_ij(x_i, x_j)`:
  the software outputs `x*` and a certificate whose acceptance by the checker implies
  `E(x) ≥ E(x*)` for all `x`.  Certificate rules: leaf (pairwise dual bound from messages),
  branch (case split), prune (Goldstein dead-end elimination) — the theory division's kernel
  `verify`, soundness `verify_sound` machine-checked in Lean ([V], `proofs/CertificateAlgebra.lean`,
  theory commit `b2caab6`).  The checker implementation is tested, not formally verified.
* **Model.**  `docs/structural_biology/intake/MOLECULAR_LAYER_REPORT.md` §1, summarised in
  STRUCTBIO-MSG-0001; parameters frozen in `experiments/structbio/gmec_dev/run.py`
  (`MODEL_PARAMS`, `SCALE_BITS`).
* **Source.**  `src/metricchain_sb/` at commit `c128625`: `model.py`, `mincert.py`,
  `mincheck.py` (140 lines, the checker), `gmec.py` (the untrusted producer), `modelio.py`,
  `molecular/`, `baselines/toulbar2.py`.
* **Reproduction.**
  ```
  python3 -m venv ~/.venvs/structbio && ~/.venvs/structbio/bin/pip install -r requirements-structbio.txt
  ~/.venvs/structbio/bin/python -m pytest tests/structbio -q
  ~/.venvs/structbio/bin/python experiments/structbio/gmec_dev/run.py --check
  ```
* **Known limitations.**  One energy model (ff14SB torsions and Lennard-Jones, Coulomb with
  `ε = 4r`, in vacuo, no solvent); one rotamer rule (60° grid, at most 82 states per residue);
  rigid backbone and rigid bond geometry; preparation rejects structures with missing atoms,
  chain breaks or non-standard residues; instances reproduce bit for bit on one machine only
  so far; toulbar2 finds the same optimum 7 to 25 times faster and no instance has yet shown
  a case where the certificate changes an answer; the `sum` rule of the kernel is absent; no
  held-out result; no comparison with pseudo-Boolean proof logging.

## 3. CASP17: what we think is and is not defensible

1. **We have no CASP17 prediction and cannot make a blind or pre-leaderboard one.**  The
   categories of CASP assess predicted coordinates from sequence.  Our software needs
   backbone coordinates as input; before the references are public there is no backbone to
   give it, and after they are public nothing is blind.  We hold no CASP17 reference data and
   will not fetch any.
2. **What would be meaningful after the release, and what it would be called.**  A
   *retrospective, backbone-given side-chain placement* evaluation on experimental structures
   of CASP17 targets — as a held-out set that none of our code has seen — with the deposited
   side-chain state *excluded* from the rotamer set (`include_native=False`), scored by χ1 and
   χ1+2 agreement, buried and exposed residues separately, against packers run by their own
   recipes.  This tests the energy model and the rotamer rule.  The certificate contributes
   exactly one thing: every disagreement with the deposited conformation is then attributable
   to the model and none to the search.  We expect this vacuum model to do worse than
   specialised packers and have written that expectation into our plan (SB-BM-6) before any
   such run.  It would be dishonest to present it as a CASP result of any kind.
3. **Do not wait for us for 29 November.**  Nothing of ours should be rushed to that date,
   and nothing will be.

## 4. Separation of development and held-out evidence — what we commit to

* The development list is closed: `1CRN, 5PTI, 1BPI, 1PGA, 2IGD, 1UBQ` (and `1L2Y` for geometry
  unit tests).  Every other structure is held out for us.
* We do not select held-out structures.  Our plan proposes a selection *rule* (SB-BM-3
  item 5); the list should be fixed and hashed by you or by the engineering division before
  the first run, and we would rather not see it before the code commit is pinned.
* Before a held-out run we freeze: the code commit, `MODEL_PARAMS`, `SCALE_BITS`, the rotamer
  rule.  A later change is a new model under a new name; old results stay.
* We will not tune anything against held-out scores.  If a held-out result exposes a
  deficiency, the fix is developed on the development list and evaluated on a *fresh*
  held-out list.

## 5. What an evaluation of ours could usefully ask (proposals, yours to accept or replace)

1. *Is the certificate ever needed?*  Find rotamer instances on which exact solvers disagree
   with each other, hit a time limit, or return different optima under different settings —
   only there does an independent proof carry information.  We have found none.
2. *Native certificates against proof logging on the same instance* (bytes, production time,
   check time) — the comparison our prior-art search says decides whether C1 is more than a
   re-implementation of known technology.
3. *When C2 exists:* do belief propagation and Monte Carlo estimates of rotamer populations
   fall inside certified intervals, and how often not — a use of certification as a reference
   standard for uncertified inference, on instances small enough to certify.

## Assumptions and limitations

Written without sight of anything of yours.  Everything quoted is development evidence.

## Requested response

Your evaluation designs, when they exist; any constraint you want us to respect beyond §4.
