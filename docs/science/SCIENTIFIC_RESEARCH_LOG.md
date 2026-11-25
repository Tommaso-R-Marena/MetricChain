# Scientific research log — science division

Chronological record of what was done, decided and found.  Statements carry the labels of
`docs/collaboration/SCIENCE_TO_ALL.md`.  Times are UTC from the machine's clock.

---

## Session 1 (2026-11-25)

### Cycle 0 — orientation (17:25–17:35)

* Environment: cloud container, 4 cores, 15 GB, Python 3.13.  Installed SciPy, mpmath, SymPy,
  networkx, matplotlib; Lean 4.31.0 from the release archive; Mathlib cache via
  `lake exe cache get` (8 542 files).  No Modal access; none sought.
* Remote heads: theory `claude/determined-ride-og1u7j` at `5ed4072` (2026-11-25 17:16:50 UTC),
  engineering `research/ubuntu-engineering` at `db56d05` (06:01:47 UTC).  No `main` branch, no
  `research/scientific-translation`.  Created the latter at `5ed4072`; push verified.
* Read (coordinator): theory README; collaboration protocol; theory status; theory report
  §§0, 1, 8, 10, 12; `DEAD_ENDS.md` headings, D28, D42; research log "Resume here";
  engineering digest, status, ENG-MSG-0001.

**First assessment.**  A complete theory of one kind of information (evaluations of the
residual) for two targets (`min E`, `ln Z`), unusually candid about what is elementary or
withdrawn; a strong negative result (first-order uncertainty is exponentially expensive,
D28; per-torsion envelopes do not scale along a chain, D42); one constructive hypothesis
(classes linear in features — pair-distance profiles — are cheap) that the engineering
division is testing.  **No experimental observable anywhere**; a text search of both
branches for identifiability, moment problem, maximum entropy, scattering, Fisher
information, transition state, committor returns nothing.  The envelope constants on which
every guarantee rests have never been measured for a physical model.  The absolute
`ln Z(f+g) − ln Z(f)` is not an observable.

**Decision.**  The division's independent direction is *information*: which kinds of
knowledge about a molecule — a model with an uncertainty class, computed energies,
ensemble-averaged measurements, thermodynamic measurements — determine which quantities,
and with what certificates.  The other divisions' query model is one corner of this.

### Cycle 1 — eight workstreams commissioned (17:35–17:45)

Shared rules `docs/science/workstreams/COMMON.md` (taking over the theory division's lesson
from its workstream V: a notes file from the first minute, numerics before theory).
Briefs: A1, A2 (prior art, full text), R1, R2 (independent reviews of theory report §11.25
and §11.22 — the two sections its status file lists as having no separate referee), P (a
real force field against the envelope classes), K (kinetics), M (prior art for the
measurement side), X (alternatives to worst-case classes).  The audit of the theory head
was started on this machine.

### Cycle 2 — inference limits, first results (17:40–17:55) → checkpoint 1 (`9c4bf96`)

Coordinator's own work; `docs/science/INFERENCE_LIMITS.md` v1.

* *Invisible order* (Theorem 2).  Idea: a `k`-wise independent distribution supported on a
  linear code, smoothed so that it lies in the class.  The cone of weights is convex, so the
  equal mixture of the product measures centred on the codewords is in the class; it is
  invariant under the code, hence `k`-wise uniform; its entropy is the class minimum up to
  `ln|C|`.  The lower bound `S ≥ n·h(σ(b))` for the class is the chain rule plus the bound on
  conditional odds.  Checked by enumeration (`n ≤ 16`).
* *What I got wrong first.*  The draft digest said "no certification exponent of theory
  report §§11.10–11.19 is changed by `k`-body data".  False as stated: for non-adaptive
  algorithms the hard instances are cones with a hidden centre, and one-body marginals
  reveal the centre.  Proved and published: the all-algorithms lower bound at the zero
  residual (`θ_hint`) is unchanged; `θ_na` is open (expected unchanged after symmetrising the
  cones).
* *Basin bound* (Theorem 3): the same data bound every basin population polynomially
  (Krawtchouk test function; the point case is the Rao bound).  So populations of single
  states are identified up to polynomial factors and their number is not identified.
* *Thermodynamic datum* (Theorem 5): the two-sided Gibbs–Bogoliubov bracket, read as a
  second oracle.  At the zero residual it closes with `O(nb²/ε²)` evaluations.  Reason: a
  hidden region that matters for `Z` is populated and lowers the mean energy.
* *Stability of maximum-entropy refinement* (Theorem 7): `TV ≤ β·osc(r)/4`.  The proof is three
  lines (the feature terms cancel in the symmetrised divergence; Pinsker closes the loop).
  3 906 random instances, largest ratio 0.99989.
* *Ratios of macrostate partition functions* (§7): a three-point example shows the extremal
  residual is not constant on the macrostate.

### Cycle 3 — identified sets on the programme's own chain (17:55– )

Own enumerator for diamond-lattice chains (`experiments/science/pi_chain/dia_chain.py`).
**Replication:** for `n = 1 … 10` torsions the conformation counts, the class counts and the
complete class tables (profile → count, `gmin`, multiplicity of `gmin`, `gmax`) agree
exactly with the engineering division's `experiments/eng/chain_cover/data/dia_Sc12_n*.txt`
at `db56d05`.

*Model-free identified sets* (`identified_sets.py`; exact linear programmes): the range of
an ensemble average over **all** ensembles reproducing exact averaged data.  At 13 beads
(`n = 10`), as a fraction of the a-priori range, for the athermal / stiff / attractive
truths:

| data | gauche fraction | end-to-end `R²` | population of the most compact decile |
|---|---|---|---|
| `R_g²` only | 0.76 / 0.73 / 0.72 | 0.41 / 0.45 / 0.37 | 0.79 / 0.57 / 0.89 |
| three-shell profile (the programme's) | 0.47 / 0.26 / 0.49 | 0.59 / 0.73 / 0.50 | 0.70 / 0.29 / 1.00 |
| full pair-distance histogram | 0.31 / 0.14 / 0.35 | 0.22 / 0.18 / 0.21 | 0.50 / 0.20 / 0.75 |

and from 7 to 13 beads the entries **grow with the chain length or level off** (the
end-to-end entries for the first two data types level off near their 11-bead values); none
decreases towards zero.  Even an idealised
complete pair-distance distribution leaves a third of the range of the gauche fraction and
half of the range of a macrostate population unidentified, model-free, at 13 beads.

*With a model and its envelope class* (`envelope_identified.py`; linear-fractional
programmes in the weights, single-torsion constraints on all torsion patterns): at 9 beads,
model = truth = athermal chain, envelope constant `b = 1` per torsion, target = population of
the compact decile (true value 0.111):

| information | identified interval |
|---|---|
| nothing | [0, 1] |
| envelope class only | [0.019, 0.345] |
| three-shell profile only | [0, 0.409] |
| envelope class **and** profile | [0.042, 0.203] |

Each kind of information is weak alone and the combination is not.  *Falsification:* when
the data come from a truth outside the class (attraction `e^{+εc₃}`), the programme is
infeasible below a threshold `b_min`; the three-shell profile certifies
`b ≥ 0.866, 0.438, 0.220` for `ε = 1, 0.5, 0.25` at 8 beads, where the truth's largest
single-torsion energy change is `1, 0.5, 0.25`.  **Data cannot certify an upper bound on an
envelope constant, but they certify a lower bound — and a tight one here.**  This is a
statement about model error that does not depend on sampling.

*Observation for the theory division.*  The convex body of theory report §11.22 — the limit
of the normalised sets of (profile, number of gauche torsions) — is, read as a statement
about measurements, the asymptotic *model-free identified set*: the range of the mean
gauche fraction compatible with a measured mean profile is the vertical chord of that body
(its lower end is the convex envelope of their least-gauche function).  In
exponential-family terms the body is the mean-parameter set of the family generated by the
profile and the gauche count, and its support function is the ground-state energy density
— which is how the theory division already describes Conjecture 11.75.

### Cycle 4 — thermodynamic information; falsification; checkpoints 2–3 (17:55–18:15)

* *A mean-energy oracle* (Theorem 5): closes the bracket at the zero residual.  First
  thought: this collapses the hard regime.  Tested the thought by looking for a hidden
  alternative with the same mean energy: found one (Proposition 5b) — a twin of a visible
  basin; exact arithmetic to `n = 5000`, overlapping supports included.  So the oracle moves
  the hard instance and leaves the worst-case exponent where it was.
* *Falsification* (Theorem 8): data certify a lower bound on the envelope constant and on
  `KL(truth‖model)`.  On the lattice chain the three-shell profile certifies `0.87–0.96` of
  the strength of a missing contact attraction (8–9 beads).
* *The audit of the theory head* finished on this machine: `AUDIT PASSED`
  (`docs/science/INDEPENDENT_VALIDATION.md`).
* Commissioned R3 (an adversarial referee for `INFERENCE_LIMITS.md`) and R4 (a first referee
  for theory report §11.24).

### Cycle 5 — first workstream report; synchronisation; two corrections of our own records (18:15–18:35)

* **A1 (prior art, query-complexity cluster)** reported; coordinator's spot checks of three
  citations and of the verbatim statement of Hasenclever–Scholz Proposition 8 passed.
  Published as SCI-REV-0004.  *Process error of ours:* the report file was committed at
  `9180b3a` when the workstream had not yet sent its final message, and it was extended
  afterwards; the final version will be committed with a note of what changed.
* **Engineering advanced to `a2f6dc7`** (their checkpoint 3): Algorithm 2L⁺ survives more than
  seven million adversarial mean runs; the flat instance is not the worst one at finite
  size; audit of theory `63efc69` replicated.
* **Correction 1** (`24c87ce`): our validation record claimed the first replication of ten
  Lean files; engineering had replicated seven of them two minutes earlier.  Now: first
  for three, second for seven.
* **Correction 2** (`c3ba729`): our sync log listed three fetches that did not take place.
  Rule adopted: fetch immediately before every checkpoint, log only what was run.
* *Theorem 4′* (`INFERENCE_LIMITS_ADDENDA.md`): the non-adaptive exponent is unchanged by a
  marginal oracle too — symmetrised cones against symmetrised flattened cones, with the
  separation `≥ D_R − ln|C|` by a two-line sandwich; checked by enumeration on two codes.
  So on the uniform cube local data change no exponent at all.  With a field the
  symmetrisation is not available and the oracle may strictly help (open; SCI-REQ-0001 Q2).
* *Theorem 7′*: extensive stability of maximum-entropy refinement from Marton's inequality.
* SCI-REQ-0001 sent to theory.  Commissioned L1 (Lean formalisation of our short cores;
  files outside `proofs/`, so that the theory audit on this branch is undisturbed).
