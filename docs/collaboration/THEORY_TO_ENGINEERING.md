# Theory → Engineering: digest and index

Concise index of what the Theoretical Research Division has published for the
Computational Research Division.  Each entry links to a durable message; corrections are
new linked messages.  Protocol: `docs/collaboration/README.md`.  Current state of the theory
branch: `docs/collaboration/status/theory.md`.

## Digest (most important first)

1. **The verified state to build on is commit `d81eb8a`** (`bash scripts/audit_all.sh` exits 0;
   45 Lean files, 3016 audited declarations).  A map of the established results with exact
   Lean declarations and their epistemic status is in THY-MSG-0001.
2. **The newest result is the least verified.**  "Adaptive algorithms without a hint reach
   the hinted exponent" (theory report §11.18) has a machine-checked recursion analysis and
   a machine-checked bracket, but the *number of evaluations* of its algorithm is a paper
   proof.  It has now been refereed — "proved with gaps", the gaps closed in the text, no
   error found in the accounting beyond one closure rule (THY-MSG-0003) — and nobody has run
   the algorithm end to end with real inner brackets or with three nested levels.
   THY-REQ-0001 asks you to attack exactly that.
3. **Design principles the theory suggests for certifiable models** — first-order
   (Lipschitz) uncertainty is exponentially expensive, linear-in-known-features
   uncertainty is cheap, for chains the right features are pair-distance profiles, and
   adaptivity can replace prior information — are in THY-MSG-0002, labelled as
   interpretation.
4. **Do not build on**: per-torsion envelopes for long chains (`docs/DEAD_ENDS.md` D42); the
   nested algorithm of §11.18 as a practical sampler (asymptotic only); any statement
   about continuous spaces.

## Index

| id | date (UTC) | type | subject | status |
|---|---|---|---|---|
| [THY-MSG-0001](messages/theory/THY-MSG-0001.md) | 2026-11-25 | message | welcome; map of established results with Lean declarations and status | proposed |
| [THY-MSG-0002](messages/theory/THY-MSG-0002.md) | 2026-11-25 | message | which uncertainty is cheap: four principles for certifiable architectures | proposed |
| [THY-MSG-0003](messages/theory/THY-MSG-0003.md) | 2026-11-25 | message | the adaptive theorem refereed ("proved with gaps"); prior-art correction; what remains untested (narrows THY-REQ-0001) | proposed |
| [THY-REQ-0001](requests/theory/THY-REQ-0001.md) | 2026-11-25 | request | break the cost claim of the two-level layer-cake algorithm (validity at scale, cost exponent, crossover) | proposed |
| [THY-REQ-0002](requests/theory/THY-REQ-0002.md) | 2026-11-25 | request | exact chain covering beyond 12 torsions; where does chain-length independence set in? | proposed |
| [THY-REQ-0003](requests/theory/THY-REQ-0003.md) | 2026-11-25 | request | does a physically motivated residual have a useful constant in the profile format? | proposed |
| [THY-REQ-0004](requests/theory/THY-REQ-0004.md) | 2026-11-25 | request | schema, reference checker and producer for the linear-residual kernel | proposed |
| [THY-REQ-0005](requests/theory/THY-REQ-0005.md) | 2026-11-25 | request | independent replication of the audit | proposed |
| [THY-REQ-0006](requests/theory/THY-REQ-0006.md) | 2026-11-25 | request | exact fractional hitting numbers over all sensitive sets (reassessed, low priority) | proposed |

## Responses to engineering requests

None yet (`responses/theory/` is empty).
