# Cross-divisional dependencies

*Written for the archive on 2026-11-27.  This file records relationships that the divisions themselves
documented — who used, reviewed, corrected or replicated what — and the points on which their records
disagree or were never reconciled.  It adds no inference of its own and resolves nothing.  Every entry
names the documents it is taken from; paths are relative to `consolidated/`.*

Files in this directory:

| file | content |
|---|---|
| `README.md` | this file |
| [`MAILBOX_INDEX.md`](MAILBOX_INDEX.md) | generated: every message, request, response and review of the eight divisions with date, addressee and title; a table of who cites whom |
| [`CROSS_REFERENCES.json`](CROSS_REFERENCES.json) | generated: for every mailbox identifier, the file that defines it and every imported Markdown file that cites it |

The communications themselves stay with their authors: `<NN_division>/docs/collaboration/{messages,requests,responses}/<division>/`.
Each division also keeps a digest for the others (`docs/collaboration/*_TO_ALL.md`, `THEORY_TO_ENGINEERING.md`,
`ENGINEERING_TO_THEORY.md`), a status file (`docs/collaboration/status/<division>.md`) that lists what it
read of every other branch and at which commit, and — except theory — a synchronisation log
(`docs/collaboration/*UPSTREAM_SYNC.md`).  The mailbox rules are `docs/collaboration/README.md` in every
division directory (each division edited its own copy).

## 1. Roles, as the research owner's directives recorded by the divisions give them

| division | role | where the directives are recorded |
|---|---|---|
| theory | the mathematics: certificate kernels and the query-complexity theory | `01_theory/docs/RESEARCH_LOG.md`; `01_theory/docs/collaboration/status/theory.md` |
| engineering | computation, independent replication, adversarial testing; coordinator of shared Modal compute; verifier of the structural-biology software | `02_engineering/docs/engineering/DIRECTIVES.md` (D-1 … D-8, the owner's words quoted) |
| science | independent validation with replication; translation to physical applicability; prior art | `03_scientific_translation/docs/science/OWNER_DIRECTIVES.md` |
| ensemble | when averaged data determine an ensemble, and what can be certified when they do not | `04_ensemble_identifiability/docs/ensemble/README.md`, `RESEARCH_LOG.md` |
| geometry | rigidity and inverse problems for averaged distance data | `05_geometric_inference/docs/geometry/RESEARCH_LOG.md` |
| complexity | complexity classifications; answers to the other divisions' complexity questions | `06_biological_complexity/docs/complexity/README.md` |
| structural biology | research software built on the mathematics | `07_structural_biology/docs/structural_biology/OWNER_DIRECTIVES.md` |
| frontier | evaluation design, benchmark integrity, CASP17 feasibility | `08_frontier_benchmarking/docs/frontier_benchmarks/OWNER_DIRECTIVES.md` |

## 2. Documented relationships

"A → B" reads "work of A is used, reviewed or answered by B".  Sources are the consolidation reports
(`…/docs/collaboration/consolidation/<division>.md`, cited as "report") and the mailbox items named.

### 2.1 Mathematics that another division builds on

| from → to | relationship | sources |
|---|---|---|
| theory → science | The certified free-energy brackets of science rest on theory's remainder inequality (Theorem 11.18) and its share and sandwich lemmas; theory calls them "the lemmas under the science division's certified free energies"; theory machine-checked one inequality of science's Proposition A17.23 | theory report §B3; science report §B1 ("the remainder inequality with class constants is the theory division's Theorem 11.18") |
| science → theory | `proofs/Frontiers/RateFull.lean` (the rate `O(1/k)` of the level recursion) was written by science and adopted by theory unchanged; science's monotone-macrostate range was adopted by theory, "which solved the general (non-monotone) problem as a transport problem (its §11.28)"; theory report §§11.27–11.29 answer questions put by science | header of `01_theory/proofs/Frontiers/RateFull.lean`; science report §B5; headings of `01_theory/docs/THEORY_REPORT.md` §§11.27–11.29; `SCI-REV-0014` |
| theory → structural biology | The C1 checker has "the theory kernel's semantics" (`verify_sound`); theory's orientation `THY-MSG-0020` says what is ready to implement and what is not; structural biology's 19 Lean theorems extend the kernel's rules and are "not reviewed by the theory division; not in its audited tree" | structural-biology report §A, §B3, §B4; `01_theory/docs/collaboration/messages/theory/THY-MSG-0020.md` |
| theory → engineering | Engineering evaluates theory's nested adaptive algorithm (Algorithm 2L⁺, Theorem 11.56) at finite size, replicated theory's audit at four of its heads, and reproduced Proposition 11.121 (false certificates) with a third implementation | engineering report §A, §B2, §B4(d); theory report §B1 "Validation" |
| ensemble → complexity | The ensemble division's question "are `K` given spin configurations exactly the ground states of some pair energy?" is complexity's B4; open for `K ≫ log n` | complexity report §B4; ensemble report §C |
| ensemble ↔ geometry | For *distributions* of distances the ensemble theorems give identifiability where geometry's second moments do not (`ENSEMBLE-RES-0008` §3); ensemble's Problem O4 needs a stability modulus for generic global rigidity | geometry report §B4 "Limitations"; ensemble report §E2 |
| complexity → structural biology, frontier, theory | Which regime no certificate format can cover (CX-T36; `COMPLEXITY-RES-0010`); "a second-order certified bound for many weak pair terms loses at first order beyond a constant oscillation per site" | complexity report §D; structural-biology report §C item 6; theory report §C |
| science → structural biology | Structural biology's certificate of optimality under entrywise table error "uses its [science's] construction"; "states as cells with their own free energy" (science's construction) is proposed for the discretisation question, not implemented | structural-biology report §B2, §E3; science report §E1 |
| ensemble → structural biology | Software cards for certified intervals were sent; "not verified by us whether implemented"; structural biology lists ensemble identification (C3) as not started | ensemble report §D; structural-biology report §C item 8 |

### 2.2 Reviews with replication, and what they changed

| reviewer → reviewed | outcome | sources |
|---|---|---|
| science → theory | Thirty reviews in all divisions; for theory: "No headline theorem of the theory division was found false, and its central cost result was re-derived from scratch with identical constants"; three sentences of the nesting section replaced and a false-certificate mechanism identified (`SCI-REV-0027`, accepted; theory's D70); two sentences on box classes replaced (`SCI-REV-0012`, `-0013`); `SCI-REV-0030` on Theorem 11.58e published incomplete | science report §A.1, §B4; theory report §B1, §B3, §B4, §C |
| science → engineering | `SCI-REV-0007`, `-0008`, `-0018`; a published conclusion of engineering withdrawn after `SCI-REV-0018` (`ENG-RES-0017`) | science report §A.1; engineering report §B2, §B4(c) |
| engineering → science | An exact checker of science's "shares at the leaves" written from the text found a defect in science's reference checker, "confirmed and repaired by it" (`SCI-RES-0030`) | engineering report §B1(c) |
| engineering → theory | The flat instance is not the worst one and theory's first cost table was too favourable (`ENG-RES-0008`); the kernel `verify` cannot be executed on realistic certificates as written, a memoised version proved equal can (`ENG-MSG-0008` §2) — see §3.2 below | engineering report §B1(d), §B2 |
| science → structural biology | "a random seed inside the Structural Biology division's energy model exposed, which their own measurement then found material on all six structures" (`SCI-REV-0026`); model v1 retired | science report §A.1; structural-biology report §A, §C item 3 |
| engineering → structural biology | `ENG-RES-0018` (first commit: three findings, repaired) and `ENG-RES-0019` (commits `0544ff4`, `41fa668`: tests, adversarial claims, independent checker, the theory kernel executed on the six stored certificates of the first model; one soundness finding at a non-default setting) — see §3.1 below | engineering report §B1; `02_engineering/docs/collaboration/responses/engineering/ENG-RES-0019.md` |
| frontier → structural biology | The certified route run unmodified on ten public instances against toulbar2: 4 certified, 6 abstained in 300 s, 17–326 times slower; diagnosis: the node rate | frontier report §B1; structural-biology report §B3 |
| science → geometry | `SCI-REV-0021` (Lemma 2.2, Theorems B, B′, G proved as stated; Theorem B for `d = 1` is Laurent–Poljak's), `SCI-REV-0023`, `SCI-REV-0028` (Theorem L correct; "shown unusable as an error bar"); the hinge theorem was obtained first by science's referee (Proposition R22-1) | geometry report §B1, §B3, "Not ranked"; science report §A.1 |
| science → ensemble | `SCI-REV-0020` (E5–E8, E1.3; contributed the stability statement "Proposition B"); E15U re-derived and replicated on 950 random measures (`SCI-RES-0038`) | ensemble report §B2, §B4 |
| science → complexity | `SCI-REV-0019` and `SCI-REV-0024`: the hardness theorems proved as stated; one hypothesis restated | complexity report §B1 |
| frontier → ensemble | Nine of twenty-five planted identification controls recomputed with independent code, all reproduced; two simple reweighting baselines each return one perfectly fitting ensemble on the non-identified controls | frontier report §B4; ensemble report §B3 "Validation" |
| engineering → geometry | Exact ranks replicated over ℚ (`ENG-MSG-0007` §5); the two-state degree computed independently; `GEOMETRY-REQ-0006` instance A certified in ball arithmetic (`ENG-MSG-0008` §4; a subagent's result, core unread by the coordinator) | geometry report §B1, §B2; engineering report §B5 |
| complexity → geometry | `COMPLEXITY-RES-0009` ("realizability of averaged chain data is NP-hard to accuracy `1/poly`") was later restated as conditional: the citation, made from memory, gives only accuracy in binary | complexity report §C |

### 2.3 Requests for computation and evaluation

Engineering's queue with the state of every request at the halt:
`02_engineering/docs/engineering/benchmarks/BENCHMARK_REGISTRY.md` (table "Status at the consolidation
halt") and `02_engineering/docs/collaboration/status/engineering.md`.  Frontier's requests:
`FRONTIER-REQ-0001` (to engineering: replication of its pilot — **not done**) and `FRONTIER-REQ-0002`
(to science — items 1(a), 1(b), 3, 5 **not started**, by science's report §G).  No division other than
engineering used Modal (each report's "state at the halt" says so).

## 3. Disagreements, unreconciled items and timing gaps

These are left exactly as the records have them.

### 3.1 Structural biology and engineering: the two verification requests

* Structural biology's report ("State at the halt") says `STRUCTBIO-REQ-0001` and `-REQ-0004` "are
  unanswered".  Engineering's reply `ENG-RES-0019` is dated 2026-11-27 01:27 UTC, after that report was
  written; **no file of any other division cites `ENG-RES-0019`** (`CROSS_REFERENCES.json`).
* `ENG-RES-0019` describes the commits `0544ff4` and `41fa668`.  Structural biology then repaired its
  checkers in commit `0e934eb` (02:42 UTC; `STRUCTBIO-MSG-0005`) and pinned `a5cc106`.  **Engineering has
  not tested anything after `41fa668`**; structural biology itself says the repaired code "has not been
  attacked again by an independent reviewer".
* Engineering's finding F1 (the floating-point tier of the partition-function checker accepts a wrong
  interval at `exp_bits` 990–991) and structural biology's own adversarial review report what appears to be
  the same defect independently: `07_structural_biology/docs/structural_biology/DEAD_ENDS.md` records
  "float tier was wrong for `exp_bits` near 1000", and the repair range-checks `exp_bits` per tier
  (`VERIFICATION_REPORT.md` §10).  Whether the repair removes engineering's reproduction has not been
  checked by anyone.
* Engineering's kernel run (the theory division's `verify`, through `verifyM`) and its independent
  checker cover the six certificates stored at the top level of
  `07_structural_biology/experiments/structbio/gmec_dev/certs/` — the first energy model ("v1"), which
  structural biology later retired because of its random seed.  Those six files are the same git objects
  at `0544ff4` and at the pinned head.  **The twelve certificates of models v2 and v2-lib
  (`certs/v2/`, `certs/v2-lib/`), on which structural biology's final results rest, were checked by that
  division's own checker only**; engineering ran neither its checker nor the kernel on them.  (The two
  certificates left out of the archive for their size are the ubiquitin certificates of v2 and v2-lib.)

### 3.2 Engineering and theory: the executable kernel

`ENG-MSG-0008` §2(a) (01:27 UTC) reports that `verify` as compiled is exponential in the length of an
elimination chain, and proposes taking memoised domains or `verifyM` with its equality proof into the
theory tree.  The theory division had halted (head 01:26 UTC); its report does not mention the finding,
and no theory file cites `ENG-MSG-0008`.  Theory's own related remark is general: "A Lean theorem about
a Lean function does not verify a production checker" (report §B2).  Also unanswered: the four numerical
discrepancies and the site outside the binary family reported in engineering's unreviewed check of the
rate theorem (`ENG-MSG-0008` §2(d); `02_engineering/experiments/eng/level_rate/REPORT.md`).

### 3.3 Science and theory: the last review

`SCI-REV-0030` (Theorem 11.58e; 01:10 UTC) was "published incomplete: the referee was wound down";
science adds that it "was wound down and re-checked by nobody".  Its header says findings F1 and F5
"concern published statements".  No theory file cites it.

### 3.4 Frontier and structural biology: the held-out list

The rule by which the sealed list was drawn "differs from the software division's plan SB-BM-3 in three
places (by that division's reading; not reconciled — register IR-14)" (frontier report §B2).  No release
of the software is frozen for the held-out evaluation; the freeze record is "not issued" (structural-biology
report §E1).

### 3.5 Frontier and engineering: two freeze procedures

Frontier: "Engineering keeps its own freeze format; one index for both was proposed and not answered"
(report §B2).  Engineering's answer — that frontier's tooling should replace its manual procedure — is in
`ENG-MSG-0008` §5, published after frontier had halted.  Frontier's request for a replication of its
pilot was not carried out.

### 3.6 Science and structural biology: model v2

"The review of model v2 owed under the owner's third directive was not started" (science report §E1, §G).
Structural biology's results on model v2 are therefore reviewed by nobody outside that division, except
for what `ENG-RES-0019` covers.

### 3.7 Originality: where a reviewing division found a claim in print

Recorded by both sides in each case; listed here so that the claims are not read without them.

| claim | finding | sources |
|---|---|---|
| theory: certification geometry; realizability and torsion-to-RMSD bounds; the cost table of sampling under a divergence bound; Theorem I3 | polytrope and tropical geometry and Lipschitz extension; classical; Block–Shetty; Marton's coupling — withdrawn | theory report §C |
| theory: query-complexity cluster | the odds-ratio lemma, non-adaptive exponent formulas at the cone, the channel-coding dictionary's identities are in print; "adaptive = hinted" with exact exponents and the two-round separation not found | science report §B4; `SCI-REV-0004` |
| geometry: Theorem B (`d = 1`), Theorem K(a), the method of §6.2, the mechanism of Theorem L | Laurent–Poljak 1996; Lew–Nevo–Peled–Raz 2023; Johnston–Lovitz–Vijayaraghavan 2023; thin-rod rigidity — "three of these were pointed out by the Science division" | geometry report §C |
| ensemble: E1(b), E19(a), E19(g); mechanism of E20b, E20d | di Dio–Schmüdgen 2018; Baldi–Vershynin 2019; Kahle 2010; di Dio–Schmüdgen Theorem 40 (found by reviewer ER4) | ensemble report §B1, §C |
| ensemble: certified population ranges | "in their nearest published form, *maximum occurrence*" | frontier report §C; ensemble report §B3 |
| complexity: partition function over all orderings; degree-2 criterion and random-state bound; hardness of the chain problem; NANUQ for galled networks | Boehmer et al.; Laurent–Poljak, Odlyzko; Kallaugher et al., Piddock; an unread third-party claim | complexity report §A, §C |
| science: cost table of certified reweighting and its bracket; necessary optimality under interval costs; the rigid-rotamer finding; cell free energies | Block–Shetty and Hoeffding; Kasperski–Zieliński; Georgiev et al., Gainza et al.; LUTE | science report §C |
| structural biology: the native certificate | "in substance … an exact LP dual with an elimination trace (Frontier N-5) — not new" | structural-biology report §B3; frontier report §C |

### 3.8 Late messages that no other division cites

Mailbox items dated from 2026-11-26 23:00 UTC that are cited by no imported file outside their own
division — a mechanical list (generated); most were published at or after the halt, when the addressees
were no longer reading.  Their content is therefore unanswered, not accepted.

<!-- GEN:unread -->
| date (UTC) | id | from | to | title |
|---|---|---|---|---|
| 2026-11-27 00:56 | [`GEOMETRY-RES-0010`](../05_geometric_inference/docs/collaboration/responses/geometry/GEOMETRY-RES-0010.md) | geometry | Science division (copy: Structural Biology — the qualifications of the guide's S7 are you… | Thank you — this is the review the proofs needed, and its major finding is yours: the first-order constant is not a global constant. We could not ope… |
| 2026-11-27 01:08 | [`GEOMETRY-MSG-0012`](../05_geometric_inference/docs/collaboration/messages/geometry/GEOMETRY-MSG-0012.md) | geometry | All divisions and the research owner | The Geometry division has consolidated and stopped. Its assessment is in `docs/collaboration/consolidation/geometry.md` |
| 2026-11-27 01:18 | [`COMPLEXITY-REV-0006`](../06_biological_complexity/docs/collaboration/messages/complexity/COMPLEXITY-REV-0006.md) | complexity | All divisions (for the record); Geometry division (the accuracy clause of the realizabili… | COMPLEXITY review 6 — Theorem 12′, chain-geometry note, higher-levels note, penalty note |
| 2026-11-27 01:21 | [`FRONTIER-MSG-0004`](../08_frontier_benchmarking/docs/collaboration/messages/frontier-benchmarks/FRONTIER-MSG-0004.md) | frontier | all seven divisions | Scientific context |
| 2026-11-27 01:23 | [`COMPLEXITY-MSG-0007`](../06_biological_complexity/docs/collaboration/messages/complexity/COMPLEXITY-MSG-0007.md) | complexity | all eight divisions; §1(a) in particular to Geometry (and to Structural Biology, Science,… | 1. Linked corrections |
| 2026-11-27 01:24 | [`ENSEMBLE-MSG-0010`](../04_ensemble_identifiability/docs/collaboration/messages/ensemble/ENSEMBLE-MSG-0010.md) | ensemble | all seven other divisions and the research owner | Halted. One review applied with four corrections you should know of; the assessment is in `consolidation/ensemble.md`; what each of you may rely on i… |
| 2026-11-27 01:24 | [`ENSEMBLE-RES-0009`](../04_ensemble_identifiability/docs/collaboration/responses/ensemble/ENSEMBLE-RES-0009.md) | ensemble | Science division (copy: Structural Biology, Frontier Benchmarking, Geometry) | Every form in your table now has a statement or an explicit "outside"; the bilinear form (one fitted tensor) has outer bounds and a finite certificat… |
| 2026-11-27 01:26 | [`THY-MSG-0022`](../01_theory/docs/collaboration/messages/theory/THY-MSG-0022.md) | theory | all seven other divisions — Engineering (§§2, 3), Frontier Benchmarking (§4), Structural … | The theory division is halted; its assessment, its audited state, and two corrections for those who build on it |
| 2026-11-27 01:27 | [`ENG-RES-0019`](../02_engineering/docs/collaboration/responses/engineering/ENG-RES-0019.md) | engineering | Structural & Computational Biology, Software Development and Applications Division (branc… | At `0544ff4` the three defects of our first report are repaired; your `min` checker and producer again survived every test we have; your six stored c… |
| 2026-11-27 02:49 | [`STRUCTBIO-MSG-0005`](../07_structural_biology/docs/collaboration/messages/structural-biology/STRUCTBIO-MSG-0005.md) | structbio | all seven other divisions; in particular Engineering (ENG-RES-0018 F3–F5) and Frontier Be… | 1. State |
<!-- /GEN:unread -->

## 4. What this file does not do

It does not judge which side of a disagreement is right, does not rank results across divisions, and does
not combine statements of different divisions into new ones.  The divisions' own proposals for
combinations are listed, as they wrote them, in `00_MASTER_INDEX.md` §11.
