# MetricChain Phase II — Division 9: certified statistical thermodynamics (multistate free-energy estimation)

Consolidated archive of the division's work, built by `experiments/mbar/build_zip.sh` from one commit
of the branch `research/phase2-certified-mbar` of the MetricChain repository.  The commit is stored in
the archive comment (`unzip -z <archive>.zip`).  The directory layout is that of the repository, so
every path quoted in the documents is valid from here.

Everything in this archive was produced and reviewed by AI sessions; no human has read it, and
nothing in it has been compared with an experiment.

**Start at** `docs/mbar/README.md` (index and reproduction commands), then
`docs/mbar/FINAL_REPORT.md` (the ten deliverables of the directive, limits, recommendations).

| path | content |
|---|---|
| `docs/mbar/` | final report, mathematics note (statements and proofs), internal adversarial review and the response, validation note and generated tables, cross-divisional synthesis, negative results and our own errors, prior-art matrix, Lean correspondence, provenance, research log |
| `docs/collaboration/` | the division's mailbox: two messages to the other Phase II divisions, one computational proposal (not authorised, not run), status, digest |
| `experiments/mbar/src`, `tests`, `bench` | implementation, unit tests, benchmark scripts, table generator |
| `experiments/mbar/results` | stored outputs of every run quoted in the documents, including superseded and invalid runs kept for the record |
| `experiments/mbar/lean` | standalone Lean 4 project (sources, pins, audit script, build and axiom logs) |
| `experiments/mbar/review` | the internal referee's scripts and outputs |
| `experiments/mbar/data` | the public data set used in the validation (MIT licence; provenance in its README) |
| `experiments/mbar/handoff` | the strengthened MBAR package as received, byte for byte |

Verify the contents (every file except the manifest itself and this copy of the README):

```bash
sha256sum -c experiments/mbar/ZIP_MANIFEST.sha256
```

Not included: the Mathlib build cache (`lake exe cache get` fetches it; pins in
`experiments/mbar/lean/lake-manifest.json`) and the rest of the MetricChain repository (other
divisions' work is cited by branch and commit in `docs/mbar/SYNTHESIS.md`).
