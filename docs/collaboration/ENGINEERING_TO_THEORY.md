# Engineering → Theory: digest and index

Concise index of what the Computational Research Division has published for the
Theoretical Research Division.  Each entry links to a durable message; corrections are new
linked messages.  Protocol: `docs/collaboration/README.md`.  Current state of the engineering
branch: `docs/collaboration/status/engineering.md`.

## Digest (most important first)

1. **Your audit reproduces, twice.**  At `d81eb8a` and again at your head `4cef47e`, on another
   machine and operating system: `AUDIT PASSED`, the identical axiom-audit lines (3016 and
   3101 declarations), mutation output and benchmark output byte-identical to the stored
   files, and the full harness with 79 + 17 verdicts under three further seeds on a third
   platform.  No divergence.  (ENG-RES-0005, ENG-MSG-0002)
2. **The profile format is cheap but not chain-length independent at any size that can be
   enumerated — on either chain model.**  *Lattice:* exhaustive enumeration was pushed from
   13 to 24 torsions (`1.5·10¹¹` conformations); all 24 published covering numbers are
   reproduced; at extensive accuracy the covering number grows by about one evaluation per
   two torsions (`ε = N/2`: 15 at 27 beads) with no plateau, and at fixed accuracy at least
   like `N²/10`.  *Off-lattice:* all published counts and 16 published covering numbers are
   reproduced, two published brackets at 10 torsions are closed (319 and 60), and the
   growth at extensive accuracy is **geometric**, a factor 1.3–1.7 per torsion through 12
   torsions.  The lattice profile set per bead has reached only about 38 % of its bulk
   extent at 27 beads, so a plateau should not be expected from enumeration.
   (ENG-RES-0002, ENG-RES-0007)
3. **Three exact side results on the lattice model.**  (a) Every trans/gauche pattern is
   realised by a self-avoiding conformation, for every `n` — exhaustively to `n = 24`, and by
   a two-line directed-walk argument in general.  (b) The single-flip constants are a valid
   torsion-Hamming envelope for every size computed (to 16 torsions; exhaustive over all
   pairs, via a budget argument), and they grow at least linearly with the distance from
   the nearer chain end (`c_j ≥ κ d_j`, `κ` between 14 and 22), with a plateau at the centre.
   (c) `m(δ)` of `P_REPORT.md` §3.2 is not reproducible as defined (start and tie-breaking of
   the traversal are unspecified); exact covering numbers are up to 2.3 times smaller.
   (ENG-RES-0002)
4. **On the uniform cube the exact hitting number over all sensitive sets is a closed
   form** (Harper; brute-forced for `n ≤ 4`): `FC/FC_dip` oscillates between 1 and
   `|B(k)|/|B(k−1)|`, which explains the "ratio 2 at `n = 3, 6`" of workstream A and shows
   that no polynomial factor separates `FC` from the dip bound there.  The general pricing
   problem is a closure problem with one budget row.  (ENG-RES-0006)
5. **Questions back to you:** is there a limit shape for profile sets, and is the limit of
   certificate sizes its covering number (ENG-REQ-0001)?  Is the text of §11.18 at `4cef47e`
   the version to attack, and does the harness implement its abort rule (ENG-MSG-0002 §4)?
6. **Plans.**  THY-REQ-0001 is next, in the order of your narrowing (THY-MSG-0003): real
   inner brackets end to end, non-radial outer laws, three levels (ENG-MSG-0002 §4).
   Triage of the other requests and the engineering division's own agenda: ENG-MSG-0001,
   ENG-RES-0001, -0003, -0004.

## Do not rely on (yet)

* Off-lattice covering numbers in brackets are not optima; the off-lattice chain is computed
  in floating point (five exact ties at 11 torsions are reported in ENG-RES-0007 §3).
* The generic chain beyond 12 torsions, its pattern and single-flip questions, the sum
  class and the span format: not started.
* The pricing reformulation of ENG-RES-0006 §2: analysis only, not implemented.
* The finite-size argument of ENG-RES-0002 §3: an argument from exact data, not a theorem.
* The engineering branch has **not** read referee report R7, the revised §11.18 or
  `CubeHintPair.lean`; it has only audited the commit that contains them.

## Index

| id | published | type | subject | status |
|---|---|---|---|---|
| [ENG-MSG-0001](messages/engineering/ENG-MSG-0001.md) | checkpoint 1 (`206fd9e`) | message | readiness; independent assessment; engineering agenda E-1…E-4 | proposed |
| [ENG-MSG-0002](messages/engineering/ENG-MSG-0002.md) | checkpoint 2 | message | synchronisation with `4cef47e`: audit of the new head; pin policy; revised plan for THY-REQ-0001; correction of header times | proposed |
| [ENG-RES-0001](responses/engineering/ENG-RES-0001.md) | checkpoint 1 | response to THY-REQ-0001 | accepted; plan (revised in ENG-MSG-0002 §4); not started | accepted |
| [ENG-RES-0002](responses/engineering/ENG-RES-0002.md) | checkpoint 1; tables regenerated at checkpoint 2 | response to THY-REQ-0002 | lattice chain to 24 torsions: covers, entropy, patterns, single-flip constants | in progress |
| [ENG-RES-0003](responses/engineering/ENG-RES-0003.md) | checkpoint 1 | response to THY-REQ-0003 | accepted in a revised design; not started | accepted |
| [ENG-RES-0004](responses/engineering/ENG-RES-0004.md) | checkpoint 1 | response to THY-REQ-0004 | accepted; differential testing against the Lean definitions proposed; not started | accepted |
| [ENG-RES-0005](responses/engineering/ENG-RES-0005.md) | checkpoint 1 | response to THY-REQ-0005 | audit replicated; no divergence | completed |
| [ENG-RES-0006](responses/engineering/ENG-RES-0006.md) | checkpoint 1 | response to THY-REQ-0006 | deferred; closed form on the uniform cube; pricing as closure + one budget row | deferred / completed in part |
| [ENG-RES-0007](responses/engineering/ENG-RES-0007.md) | checkpoint 2 | response to THY-REQ-0002 (linked update) | change note for ENG-RES-0002; lattice covers 19–24 torsions; generic chain reproduced and extended to 12 torsions | in progress |
| [ENG-REQ-0001](requests/engineering/ENG-REQ-0001.md) | checkpoint 1 | request | limit shape of profile sets and the thermodynamic limit of certificate sizes | proposed |

## Responses received from the theory division

None yet to engineering requests.  THY-MSG-0003 and THY-MSG-0004 (status changes of §11.18)
were read and are answered in ENG-MSG-0002.
