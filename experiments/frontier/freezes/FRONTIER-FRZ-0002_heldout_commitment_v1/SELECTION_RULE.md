# Held-out list v1 — the rule is public, the list is sealed

*Freeze FRONTIER-FRZ-0002.  For protocols FB-P-01 (held-out stage) and FB-P-02, and for the
structural-biology division's SB-BM-3 and SB-BM-6, whose authors asked that another division
fix and hash the held-out list and that they not see it before their code is pinned
(STRUCTBIO-MSG-0002 §4).*

## The rule

1. **Pool.**  The entries returned by the RCSB PDB search in `query.json`, executed at
   2026-11-26T23:40:28Z: X-ray entries, resolution ≤ 1.5 Å, exactly one polymer chain in the
   asymmetric unit, that chain a protein with 40–200 deposited residues, no nucleic acid,
   **first released on or after 2026-07-01**.  150 entries (their identifiers, sorted and
   joined by newlines, have the SHA-256 given in `commitment.json`, so anyone can confirm the
   pool by re-running the query — entries released later will be extra).
2. **Exclusions**, from archive metadata only: chains with a non-standard residue (4 entries);
   chains in the 30 % sequence-identity cluster of a development structure of the software
   division — 1CRN, 5PTI, 1BPI, 1PGA, 2IGD, 1UBQ, 1L2Y (2 entries).  144 remain, in 50
   clusters of which 47 survive the exclusions.
3. **Order.**  Ascending SHA-256 of (a secret 256-bit ordering salt ‖ entry identifier).
4. **Representatives.**  The first entry of each 30 % cluster in that order: **47
   structures**, ranked.  The other members of a cluster follow as its fallbacks, in order.
5. **Use.**  A run takes the representatives in rank order.  If a structure fails the
   software's preparation (missing heavy atoms, chain breaks) it is replaced by the next
   fallback of its cluster; a cluster with no usable member is recorded as a preparation
   failure.  Nothing is dropped after a result is seen.

Differences from the rule proposed in SB-BM-3: the release date (so that every structure
post-dates the declared training cut-offs of all learned packers found so far, the latest
being 2023-07-28, and the knowledge cut-off of the model that wrote the software, June 2026);
a secret salt in the ordering (their rule ordered by the plain hash of the identifier, which
anyone can compute); and a list of 47 rather than 100, because the pool after the date
criterion has 50 clusters.

## What is in the repository, and what is not

| item | where |
|---|---|
| the rule and the query | this file, `query.json` |
| a salted commitment to the exact ordered list (with its ordering salt) | `commitment.json` |
| the list itself, encrypted | `sealed_list_v1.enc` |
| the passphrase of the sealed file and the salt of the commitment | **not in the repository**: with the research owner |

## Opening

When the software division has frozen the commit, the model parameters and the rotamer rule
it wants evaluated (a freeze record of its own or one made with `metricchain_fb.freeze`), the
research owner gives the passphrase and the commitment salt to the division that runs the
evaluation (engineering):

```
openssl enc -d -aes-256-cbc -pbkdf2 -iter 600000 -in sealed_list_v1.enc -out heldout_list_v1.txt   # asks for the passphrase
python - <<'PY'
from metricchain_fb import commitment
print(commitment.open_commitment("<commitment from commitment.json>", open("heldout_list_v1.txt", "rb").read(), "<commitment salt>"))
PY
```

`True` shows the list is the one fixed on 2026-11-26.  From the moment it is opened the list
is disclosed: any later change to the software evaluated on it is a retrospective experiment
on this list, and a new sealed list is needed for a new held-out claim.

## What this does and does not guarantee

* The *membership and order* of the list were fixed before the software was pinned and cannot
  be changed afterwards without detection.
* The *pool* is public by construction: a developer who tuned on all 150 candidates would
  have seen every member.  The seal prevents tuning on the list; it does not prevent tuning on
  the pool.  The software division has stated that every structure outside its seven
  development structures is held out for it.
* The reference coordinates are public PDB entries; "held out" means held out from
  development, never blind.  Any evaluation on this list is retrospective (class A-RET) with
  a held-out evidence stage.
* If the passphrase is lost the list cannot be opened and must be redrawn; that is the cost
  of not storing a secret in a repository every division can read.
* Small, single-chain crystal structures are over-represented; chains that fail preparation
  are systematically absent.
