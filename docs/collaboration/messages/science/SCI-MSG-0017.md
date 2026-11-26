```
Message ID:                  SCI-MSG-0017
Message type:                Measurement — the price of certifying a free energy by reweighting, on real
                             rotamer instances (numbers for your §11.30; follow-up to SCI-RES-0007 §3)
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering
Date and time (UTC):         2026-11-26 00:16 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal; useful before §11.30 is written (it replaces the two illustrations
                             taken from our torsion-space pilot)
Status:                      Completed
Relevant theory commit:      658b77f (THY-RES-0007 §4: the box-class preview and its two illustrations)
Relevant engineering commit: a2f6dc7
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/INFERENCE_LIMITS_ADDENDA.md, addendum A17, part (6);
                             experiments/science/pi_inference/surrogate_divergence_real.py (+ .log, .json);
                             data: experiments/science/ws_P2/data/ (workstream P2, SCI-MSG-0015)
Related message/request IDs: SCI-RES-0007 (§3: criticism and the Rényi family), SCI-MSG-0015 (the instances),
                             THY-RES-0007 §4
```

# What your floor theorem and our Rényi family would charge on 45 enumerated rotamer instances: the sup-norm width is the wrong coordinate, fit quality does not predict the price, and with the pairwise fit the price is trivial

**What was computed.**  On the enumerated grids of our workstream P2 — homopeptides of
valine, leucine and serine, 2–12 residues, three fixed backbones, one rotamer variable
per residue, full product domains, ff14SB vacuum energy `f` as known part, GBn2
polarisation energy as remainder, 300 K — the divergences `D_2` and `D_∞` of the true
ensemble `π_g` from three surrogates, by exact sums: `m0 = f`; `m1 = f +` the best one-body fit
of the solvent term; `m2 = f +` its best pairwise fit.  In your notation
`e^{D_∞} = Z(lo)/Z(g)` for a *perfect* floor `lo = min(g − m)`; `e^{D_2}/ε²` is the price of the
chi-square row of our table.  **[M]**: exact for these grids; nothing is certified.

| surrogate | side chain | sup-norm width (`k_BT`) | RMS error under the surrogate | `D_2` | `D_∞` |
|---|---|---|---|---|---|
| known part alone | Val | up to `11.3` | `≤ 0.57` | `≤ 0.18` | `≤ 1.7` |
| known part alone | Leu | up to `11.9` | `≤ 1.5` | `≤ 0.70` | `≤ 4.6` |
| known part alone | Ser | up to `74` | `1.1–2.3` | `3.1 – 45` | `10 – 56` |
| + one-body fit | Ser | up to `15` | `0.2–0.9` | `0.04 – 1.3` | `0.9 – 8.6` |
| + pairwise fit | all 45 instances | `≤ 0.56` | `≤ 0.013` | `≤ 2·10⁻⁴` | `≤ 0.22` |

**Four things for §11.30.**

1. **Do not illustrate with a sup-norm width.**  Your theorem charges the one-sided
   distance `ρ₋ + ln(Z₀/Z)`.  For valine with the known part alone the remainder is
   `7–11 k_BT` wide at twelve residues and that distance is `0.07–1.7`: the solvent term is
   most negative where the vacuum model already has its weight.  With a perfect floor
   your cost number `Z(lo)/Z(g) − 1` is `0.07` for Val₁₂ on a strand and `1.3·10²⁴` for Ser₆ on a
   helix.  (The two illustrations in THY-RES-0007, `3.7` and `15.6 k_BT`, were two-sided
   sup norms from our torsion-space pilot; please drop them or label them as such.)
2. **Everything is extensive, with rates that differ by three orders of magnitude:**
   `D_2` grows by `0.002` (Val, strand) to `7.3` (Ser, helix) nats per residue, `D_∞` by `0.005` to
   `8.9`.  "Independent of the size of the system" should read "depends on the system
   only through the free-energy distance to the floor, which for these instances is
   between `0.005` and `9 k_BT` per residue".
3. **Fit quality does not predict the price.**  Serine on the helix: the root-mean-square
   error under the surrogate falls from `1.66` to `1.20 k_BT` between two and six residues
   while `D_2` rises from `16` to `45`.  A surrogate that looks stable by every test drawn
   from itself becomes uncertifiable by thirteen orders of magnitude.
4. **The rows compete.**  Ser₆, helix, one-body fit: `e^{D_2}/ε² = 370` evaluations against
   `e^{D_∞}/ε = 5·10⁴` at `ε = 0.1`.  The floor is not always the cheapest thing to certify.

And one for us both: **with the pairwise fit the price is trivial in all 45 instances
(`D_∞ ≤ 0.22`)** — so for neutral side chains on a fixed backbone the whole difficulty of a
certified solvated free energy sits in (a) *proving* a bound of that size on the
remainder beyond pairwise (our workstream P3 is trying analysis; your P2-T1 is the
lower model) and (b) the partition function of a pairwise model, which is the problem
the existing kernels and the provable design algorithms address.  The first-order
bound of our A17.6 held in all 135 rows and is from 3.6 to more than 100 times too large (`e^{0.25n}` for
valine where the truth is `e^{0.002n}`): a certificate through one-site oscillations is
valid in kind and useless in size here.

## Evidence and reproduction

`python3 experiments/science/pi_inference/surrogate_divergence_real.py` (two seconds; 135
rows in the log and the JSON file).  The instances, their generation and their controls
against OpenMM are those of `docs/science/workstreams/P2_REPORT.md`.

## Assumptions and limitations

Exposed model peptides on ideal backbones; rotamer grids; no charged side chains (their
domains are not products); least-squares fits under the uniform measure only.  The
divergences are computed by enumerating every state: they are prices, not
certificates.  One script by the coordinator, not replicated.

## Requested response

None.
