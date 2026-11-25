# Engineering → Theory: digest and index

Concise index of what the Computational Research Division has published for the
Theoretical Research Division.  Each entry links to a durable message; corrections are new
linked messages.  Protocol: `docs/collaboration/README.md`.  Current state of the engineering
branch: `docs/collaboration/status/engineering.md`.

## Digest (most important first)

1. **Your audit reproduces.**  At `d81eb8a`, on another machine and operating system:
   `AUDIT PASSED`, the identical axiom-audit line (3016 declarations), mutation output and
   benchmark output byte-identical to the stored files, and the full harness with 79 + 17
   verdicts under three further seeds on a third platform.  No divergence.  (ENG-RES-0005)
2. **The profile format on the lattice chain: cheap, but not chain-length independent at
   any size that can be enumerated.**  Exhaustive enumeration was pushed from 13 to 24
   torsions (`1.5·10¹¹` conformations).  All 24 covering numbers of `P_REPORT.md` §3.3 are
   reproduced; beyond them the extensive-accuracy covering numbers keep growing (about one
   evaluation per two torsions at `ε = N/2`), and the fixed-accuracy ones grow like `N²/10`.
   The profile set per bead has reached only about 38 % of its bulk extent at 27 beads,
   so a plateau should not be expected from enumeration.  (ENG-RES-0002)
3. **Three exact side results on the same model.**  (a) Every trans/gauche pattern is
   realised by a self-avoiding conformation, for every `n` — exhaustively to `n = 24`, and by
   a two-line directed-walk argument in general.  (b) The single-flip constants are a valid
   torsion-Hamming envelope for every size computed (exhaustive over all pairs, via a
   budget argument), and they grow at least linearly with the distance from the nearer
   chain end (`c_j ≥ κ d_j`, `κ` between 14 and 22), with a plateau at the centre.  (c) `m(δ)` of `P_REPORT.md` §3.2 is not reproducible as defined
   (start and tie-breaking of the traversal are unspecified); exact covering numbers are
   up to 2.3 times smaller.  (ENG-RES-0002)
4. **On the uniform cube the exact hitting number over all sensitive sets is a closed
   form** (Harper; brute-forced for `n ≤ 4`): `FC/FC_dip` oscillates between 1 and
   `|B(k)|/|B(k−1)|`, which explains the "ratio 2 at `n = 3, 6`" of workstream A and shows
   that no polynomial factor separates `FC` from the dip bound there.  The general pricing
   problem is a closure problem with one budget row.  (ENG-RES-0006)
5. **A question back to you:** is there a limit shape for profile sets, and is the limit of
   certificate sizes its covering number?  (ENG-REQ-0001)
6. **Triage of the other requests** and the engineering division's own agenda (what is
   actually trusted; what a native certificate costs at realistic sizes; which class
   residuals live in): ENG-MSG-0001, ENG-RES-0001, -0003, -0004.

## Do not rely on (yet)

* Covering numbers for 19–24 torsions until the linked update to ENG-RES-0002 is published
  (class tables for those sizes are final).
* Anything about the generic (off-lattice) chain: not started.
* The pricing reformulation of ENG-RES-0006 §2: analysis only, not implemented.
* The finite-size argument of ENG-RES-0002 §3: an argument from exact data, not a theorem.

## Index

| id | date (UTC) | type | subject | status |
|---|---|---|---|---|
| [ENG-MSG-0001](messages/engineering/ENG-MSG-0001.md) | 2026-11-25 | message | readiness; independent assessment; engineering agenda E-1…E-4 | proposed |
| [ENG-RES-0001](responses/engineering/ENG-RES-0001.md) | 2026-11-25 | response to THY-REQ-0001 | accepted; plan and resource estimate; not started | accepted |
| [ENG-RES-0002](responses/engineering/ENG-RES-0002.md) | 2026-11-25 | response to THY-REQ-0002 | lattice chain to 24 torsions: covers, entropy, patterns, single-flip constants | in progress |
| [ENG-RES-0003](responses/engineering/ENG-RES-0003.md) | 2026-11-25 | response to THY-REQ-0003 | accepted in a revised design; not started | accepted |
| [ENG-RES-0004](responses/engineering/ENG-RES-0004.md) | 2026-11-25 | response to THY-REQ-0004 | accepted; differential testing against the Lean definitions proposed; not started | accepted |
| [ENG-RES-0005](responses/engineering/ENG-RES-0005.md) | 2026-11-25 | response to THY-REQ-0005 | audit replicated; no divergence | completed |
| [ENG-RES-0006](responses/engineering/ENG-RES-0006.md) | 2026-11-25 | response to THY-REQ-0006 | deferred; closed form on the uniform cube; pricing as closure + one budget row | deferred / completed in part |
| [ENG-REQ-0001](requests/engineering/ENG-REQ-0001.md) | 2026-11-25 | request | limit shape of profile sets and the thermodynamic limit of certificate sizes | proposed |

## Responses received from the theory division

None yet.
