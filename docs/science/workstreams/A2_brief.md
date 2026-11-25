# Workstream A2 — prior art and originality: certificate kernels, certification geometry, chains

Read `docs/science/workstreams/COMMON.md` first.  Your directory:
`experiments/science/ws_A2/`; your report: `docs/science/workstreams/A2_REPORT.md`.

## Why this workstream exists

Workstream A1 covers the query-complexity theorems for `ln Z`.  You cover the rest of what the
programme might want to publish or build on: (i) the **machine-checked certificate kernels**
and what exists in provable molecular modelling and in proof-logging for discrete
optimisation; (ii) the **certification-geometry** results for minima (certificates are
coverings in a slack quasi-metric; rate–distortion exponents; hardness; best-first search);
(iii) everything about **chains**: the lever-arm law, pair-distance-profile classes, and the
limit shape.  The theory division's own literature checks (`docs/prior_art/L1…L8`) are
thorough for the first phase but several later rows say "no literature search was possible
in the review" or "abstracts only".

## Claims to test (read the exact statements first: theory report §0.2 table, §10 table)

1. **E1 / D3 / D4 (kernels).**  "No *native* verified checker for cost-function-network / MAP /
   dead-end-elimination certificates found"; a verified checker for two-sided partition
   function bounds with leaf / branch / thermal-prune / cut / elimination rules; rigorous
   voxel-*integral* enclosures inside a provable algorithm.  Compare with: VeriPB and
   pseudo-Boolean proof logging (Gocht, Nordström, McCreesh, Bogaerts et al.), CakePB;
   certified MaxSAT; proof logging for cost function networks / toulbar2 (search for recent
   work on certificates for WCSP / soft arc consistency; there is 2023–2026 activity);
   verified model counters and their proof formats (MICE, CPOG, Fichte–Hecher–Roland);
   certified weighted model counting / partition functions; verified branch-and-bound;
   OSPREY's K*, BBK*, MARK*, "provable" bounds on partition functions in protein design
   (Donald lab) and what "provable" means there (ε-approximation given the model, with
   floating point?); interval methods for conformational energies.
2. **G1, G4, G7** — minimal certificates of global optimality under a Lipschitz-type class as
   coverings; the exact exponential rate on product spaces as a rate–distortion function;
   the finite-temperature analogue.  Compare with: Hansen–Jaumard–Lu; Bachoc–Cesari–
   Gerchinovitz 2021 (instance-dependent bounds for Lipschitz optimisation) and follow-ups
   (Bouttier, Cesari, Gerchinovitz, Malherbe, Vayatis; "certified" Lipschitz optimisation;
   2022–2026 follow-ups on instance-optimality); Baran–Demaine–Katz "optimally adaptive
   integration of univariate Lipschitz functions"; covering-based query lower bounds in
   metric search (Hetland); source coding / guessing (Arikan–Merhav), Merhav 2011.
3. **G13 (normal form)** — a known part is the gradient part of an asymmetric envelope
   (Johnson reweighting); is this stated in the Lipschitz-optimisation or
   potential-reduction literature?
4. **G16 (lever-arm law)** — torsion-to-RMSD Lipschitz constants grow like `m^{3/2}` with the
   distance to the chain end, and its consequence for certification.  Compare with the
   robotics / kinematics literature (Jacobian norm bounds for serial chains, "kinematic
   sensitivity", "lever arm effect" in loop closure / torsion-space refinement), and
   protein torsion-space literature (internal-coordinate MD, "torsion angle dynamics",
   concerted rotations, Go–Scheraga).
5. **G19 (profile classes)** — residual classes linear in cumulative pair-count profiles;
   the envelope is a transport (Wasserstein-1) distance between pair-distance distributions.
   Compare with: shape distributions (Osada et al.), distance-distribution descriptors,
   **the scattering literature** — the pair-distance distribution `p(r)` is exactly what
   small-angle X-ray/neutron scattering measures; Wasserstein distances between `p(r)`
   curves or radial distribution functions as structural metrics; homometric point sets and
   reconstruction from distance distributions (Patterson; Boutin–Kemper 2004; turnpike /
   partial digest problems) — which questions about *identifiability of a conformation from
   its distance profile* are already answered there?  This last point matters for our
   division's own agenda; report it carefully.
6. **G24 (limit shape)** — Hausdorff convergence of normalised (profile, #gauche) sets of
   lattice bridges to a convex body via concatenation + a set-valued Fekete lemma; the
   cluster method for outer bounds.  Compare with: set-valued subadditive ergodic theory
   (Kingman-type / Artstein–Hart, "limit shapes" via superadditivity in first-passage
   percolation — the shape theorem), Hammersley–Welsh / bridges in self-avoiding walk
   theory (Madras–Slade), *joint* limit sets of observables for SAWs or lattice polymers
   ("set of attainable densities", "ground-state energy density region", "joint numerical
   range" analogues), Radin/Kennedy-type ground-state methods ("m-potentials", the cluster /
   "method of local ground states"), and convex-hull-of-achievable-statistics results in
   symbolic dynamics (rotation sets, "ergodic optimisation": the set of ergodic averages of a
   vector-valued function is a compact convex set — is the limit shape just a rotation set
   of a subshift-like system?  If so, name the theorem).
7. **C4** — finite-angle torsion → RMSD closed form `2S − 2√(S² − 4 I_A I_B sin²(φ/2))`.

## What to deliver

Same format as A1: for each claim, exact statement and location, closest prior statements
with reading level, comparison of hypotheses and conclusions, and one classification from
{established prior art; reformulation; known special case; plausibly original
generalisation; new combination; plausibly original theorem; plausibly original algorithm;
plausibly original capability; unresolved}.  Then an explicit list: **"claims in the
repository's README or theory report whose novelty wording should be weakened"** and
**"claims that are stated too modestly"**, each with the evidence.
