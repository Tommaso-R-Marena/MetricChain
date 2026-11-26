Ser₁₂ is the opposite ensemble: every side chain is off the anchor about half of the time
(6.4 of 12 on average), nothing is frozen, and P8's state-wise constants gain only a factor
1.6–1.8 there (P8_REPORT §3.5).  Tables: `p9_03_tables.py S12 5` (197 s); first-order numbers: `p9_04_gain.py S12 5`;
random-state check: `p9_06_check12.py S12 5 --noa` (2 000 states, no violation, smallest ratio
10.3, control 3 violations); brackets: `p9_05_brackets.py S12 5 7 --pairs … --label X` (26 s,
0.36 GB).  `βΓ₅`: P8's 'SAb' 0.1381 (re-computed, equal to P8's stored values); joint maxima of
stage 2: 0.0925; sum of the medians over the states: 0.0107.

{GEN_BRACKETS_S12_M5_W7}

*Reading.*  The lever is not specific to charged, mostly frozen side chains: the equal-share
triple form falls from 0.0547 (P8's constants) to 0.0226 nats, the window form from 0.0226
to 0.0117, of which 0.0091 are the reductions.  The coordinator's published bracket for this
peptide, with workstream P3's closed-form constants, is 0.0872 nats
(`[227.325848, 227.413092]`, addendum A17 (18), item 61); every bracket of the table lies inside
it.  The gain is smaller than for lysine because a mobile ensemble visits many rotamers, not
the ones near the anchor only; all five predictions for this peptide (prediction 5 in
`NOTES.md`: 0.0091, 0.054, 0.021, 0.022, 0.011) were within 8 % — a first-order regime
throughout.
