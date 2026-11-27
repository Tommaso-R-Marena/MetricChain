<!-- written by collect.py from logs/*.log -->

### Main table: `leafCheck … = true := by decide +kernel`

| encoding | n | k | n²k² | cells n(n-1)/2·k² | result | wall s | kernel s | elaboration s | peak RSS MB | axioms |
|---|---|---|---|---|---|---|---|---|---|---|
| E1 | 8 | 2 | 256 | 112 | ok | 0.78 | 0.12 | 0.28 | 477 | none |
| E1 | 16 | 2 | 1024 | 480 | ok | 1.61 | 0.40 | 0.66 | 525 | none |
| E1 | 16 | 4 | 4096 | 1920 | ok | 3.02 | 0.96 | 1.30 | 628 | none |
| E1 | 32 | 4 | 16384 | 7936 | ok | 12.51 | 4.48 | 5.67 | 1151 | none |
| E1 | 32 | 8 | 65536 | 31744 | ok | 42.41 | 17.50 | 17.70 | 2673 | none |
| E1 | 48 | 8 | 147456 | 72192 | FAIL: resident memory above 5 GB, killed | 78.82 | - | - | 4888 | - |
| E4 | 8 | 2 | 256 | 112 | ok | 0.68 | 0.07 | 0.21 | 469 | none |
| E4 | 16 | 2 | 1024 | 480 | ok | 1.26 | 0.26 | 0.52 | 510 | none |
| E4 | 16 | 4 | 4096 | 1920 | ok | 2.24 | 0.66 | 0.98 | 580 | none |
| E4 | 32 | 4 | 16384 | 7936 | ok | 8.90 | 2.97 | 4.00 | 942 | none |
| E4 | 32 | 8 | 65536 | 31744 | ok | 28.03 | 8.56 | 13.50 | 1913 | none |
| E4 | 48 | 8 | 147456 | 72192 | ok | 77.21 | 23.00 | 37.70 | 3760 | none |
| E2 | 8 | 2 | 256 | 112 | ok | 0.54 | 0.03 | 0.08 | 459 | none |
| E2 | 16 | 2 | 1024 | 480 | ok | 0.91 | 0.24 | 0.22 | 473 | none |
| E2 | 16 | 4 | 4096 | 1920 | ok | 1.36 | 0.51 | 0.47 | 564 | none |
| E2 | 32 | 4 | 16384 | 7936 | ok | 6.07 | 4.12 | 1.43 | 1739 | none |
| E2 | 32 | 8 | 65536 | 31744 | FAIL: out of memory under `ulimit -v` (GNU MP: Cannot allocate memory (size=198688)) | 17.48 | - | - | 3244 | - |
| E2h | 8 | 2 | 256 | 112 | ok | 0.42 | 0.03 | 0.06 | 459 | none |
| E2h | 16 | 2 | 1024 | 480 | ok | 0.57 | 0.10 | 0.15 | 471 | none |
| E2h | 16 | 4 | 4096 | 1920 | ok | 1.10 | 0.29 | 0.42 | 493 | none |
| E2h | 32 | 4 | 16384 | 7936 | ok | 3.04 | 1.34 | 1.31 | 617 | none |
| E2h | 32 | 8 | 65536 | 31744 | ok | 10.72 | 5.08 | 4.89 | 961 | none |
| E2h | 48 | 8 | 147456 | 72192 | ok | 24.98 | 13.50 | 10.40 | 1640 | none |
| E3 | 8 | 2 | 256 | 112 | ok | 4.55 | 4.02 | 0.18 | 1084 | none |
| E3 | 16 | 2 | 1024 | 480 | FAIL: resident memory above 5 GB, killed | 22.49 | - | - | 4886 | - |

### Negative controls and tactic variants

| encoding | n | k | file variant | claim / tactic | result | wall s | kernel s | peak RSS MB |
|---|---|---|---|---|---|---|---|---|
| E1 | 16 | 2 | negJ | `= false`, one J entry lowered (B fails in the last cell) | ok | 1.56 | 0.32 | 519 |
| E1 | 16 | 2 | negJ0 | `= false`, one J entry lowered (B fails in the first cell) | ok | 1.09 | 0.02 | 476 |
| E1 | 16 | 2 | negL | `= false`, L+1 (C fails) | ok | 1.41 | 0.43 | 525 |
| E1 | 16 | 2 | negL_claimtrue | `= true` on the L+1 data (wrong claim) | rejected, as it must be | 1.82 | 0.42 | 536 |
| E1 | 16 | 2 | negP | `= false`, one p+1 (B fails) | ok | 1.01 | 0.05 | 477 |
| E1 | 16 | 2 | negU | `= false`, one u+1 (A fails) | ok | 1.14 | 0.28 | 512 |
| E1 | 16 | 2 | tac_decide | `= true := by decide` (no `+kernel`) | ok | 1.76 | 0.37 | 538 |
| E1 | 16 | 2 | tac_rfl | `= true := by rfl` | ok | 1.92 | 0.39 | 537 |
| E4 | 16 | 2 | negJ | `= false`, one J entry lowered (B fails in the last cell) | ok | 1.20 | 0.28 | 506 |
| E4 | 16 | 2 | negJ0 | `= false`, one J entry lowered (B fails in the first cell) | ok | 1.09 | 0.02 | 468 |
| E4 | 16 | 2 | negL | `= false`, L+1 (C fails) | ok | 1.20 | 0.23 | 506 |
| E4 | 16 | 2 | negL_claimtrue | `= true` on the L+1 data (wrong claim) | rejected, as it must be | 1.77 | 0.34 | 517 |
| E4 | 16 | 2 | negP | `= false`, one p+1 (B fails) | ok | 0.94 | 0.04 | 470 |
| E4 | 16 | 2 | negU | `= false`, one u+1 (A fails) | ok | 0.94 | 0.18 | 496 |
| E4 | 16 | 2 | tac_decide | `= true := by decide` (no `+kernel`) | ok | 1.45 | 0.28 | 519 |
| E4 | 16 | 2 | tac_rfl | `= true := by rfl` | ok | 1.61 | 0.29 | 513 |
| E4 | 32 | 4 | tac_decide | `= true := by decide` (no `+kernel`) | ok | 11.86 | 2.72 | 985 |
| E4 | 32 | 4 | tac_rfl | `= true := by rfl` | ok | 13.76 | 3.91 | 986 |
| E2 | 16 | 2 | negJ | `= false`, one J entry lowered (B fails in the last cell) | ok | 0.47 | 0.04 | 460 |
| E2 | 16 | 2 | negJ0 | `= false`, one J entry lowered (B fails in the first cell) | ok | 0.63 | 0.12 | 470 |
| E2 | 16 | 2 | negL | `= false`, L+1 (C fails) | ok | 0.52 | 0.10 | 474 |
| E2 | 16 | 2 | negL_claimtrue | `= true` on the L+1 data (wrong claim) | rejected, as it must be | 0.78 | 0.14 | 485 |
| E2 | 16 | 2 | negP | `= false`, one p+1 (B fails) | ok | 0.47 | 0.03 | 460 |
| E2 | 16 | 2 | negU | `= false`, one u+1 (A fails) | ok | 0.41 | 0.02 | 459 |
| E2 | 16 | 2 | tac_decide | `= true := by decide` (no `+kernel`) | ok | 0.73 | 0.12 | 483 |
| E2 | 16 | 2 | tac_rfl | `= true := by rfl` | ok | 0.73 | 0.14 | 487 |
| E2 | 32 | 4 | tac_decide | `= true := by decide` (no `+kernel`) | ok | 9.41 | 3.46 | 2896 |
| E2 | 32 | 4 | tac_rfl | `= true := by rfl` | ok | 9.89 | 3.74 | 2940 |
| E2h | 16 | 2 | negJ | `= false`, one J entry lowered (B fails in the last cell) | ok | 0.47 | 0.03 | 461 |
| E2h | 16 | 2 | negJ0 | `= false`, one J entry lowered (B fails in the first cell) | ok | 0.52 | 0.09 | 469 |
| E2h | 16 | 2 | negL | `= false`, L+1 (C fails) | ok | 0.58 | 0.09 | 469 |
| E2h | 16 | 2 | negL_claimtrue | `= true` on the L+1 data (wrong claim) | rejected, as it must be | 0.58 | 0.10 | 472 |
| E2h | 16 | 2 | negP | `= false`, one p+1 (B fails) | ok | 0.47 | 0.04 | 461 |
| E2h | 16 | 2 | negU | `= false`, one u+1 (A fails) | ok | 0.42 | 0.01 | 461 |
| E2h | 16 | 2 | tac_decide | `= true := by decide` (no `+kernel`) | FAIL: maximum recursion depth has been reached | 0.47 | 0.01 | 459 |
| E2h | 16 | 2 | tac_rfl | `= true := by rfl` | FAIL: maximum recursion depth has been reached | 0.53 | 0.00 | 456 |
| E3 | 8 | 2 | negJ | `= false`, one J entry lowered (B fails in the last cell) | ok | 1.51 | 0.90 | 596 |
| E3 | 8 | 2 | negJ0 | `= false`, one J entry lowered (B fails in the first cell) | ok | 4.21 | 3.69 | 1077 |
| E3 | 8 | 2 | negL | `= false`, L+1 (C fails) | ok | 4.17 | 3.61 | 1083 |
| E3 | 8 | 2 | negL_claimtrue | `= true` on the L+1 data (wrong claim) | rejected, as it must be | 4.51 | 3.87 | 1083 |
| E3 | 8 | 2 | negP | `= false`, one p+1 (B fails) | ok | 2.45 | 1.95 | 752 |
| E3 | 8 | 2 | negU | `= false`, one u+1 (A fails) | ok | 0.94 | 0.50 | 555 |
| E3 | 8 | 2 | tac_decide | `= true := by decide` (no `+kernel`) | FAIL: maximum recursion depth has been reached | 0.68 | 0.01 | 464 |
| E3 | 8 | 2 | tac_rfl | `= true := by rfl` | FAIL: maximum recursion depth has been reached | 0.53 | 0.01 | 462 |

### Side experiments

| log | result | wall s | kernel s | elaboration s | peak RSS MB | note |
|---|---|---|---|---|---|---|
| E1_n16_k2_plainnumerals | FAIL: (deterministic) timeout at `whnf`, maximum number of heartbeats (200000) has been reached | 18.02 | 0.02 | 2.57 | 490 |  |
| E1_n16_k4_plaindef | FAIL: maximum recursion depth has been reached | 4.54 | 1.22 | 1.79 | 697 | per theorem: 1.18s |
| E1_n32_k4_randmsg | ok | 17.60 | 6.16 | 7.90 | 1201 | per theorem: 5.97s |
| E1_n32_k8_dataonly | ok | 28.70 | 0.53 | 20.20 | 1025 |  |
| E4_n32_k4_oneliteral | ok | 19.60 | 3.84 | 10.20 | 1249 | per theorem: 3.71s |
| E4_n32_k4_randmsg | ok | 10.80 | 3.28 | 4.94 | 962 | per theorem: 3.12s |
| E4_n32_k8_oneliteral | FAIL: (deterministic) timeout at `whnf`, maximum number of heartbeats (200000) has been reached | 35.12 | 0.03 | 24.90 | 1692 |  |
| E4_n48_k8_dataonly | ok | 48.31 | 0.99 | 33.30 | 1468 |  |
| E2_n16_k2_randmsg | ok | 0.58 | 0.11 | 0.14 | 476 | per theorem: 109ms |
| E2h_n16_k2_oneliteral | ok | 0.73 | 0.10 | 0.33 | 468 | per theorem: 101ms |
| E2h_n16_k4_oneliteral | ok | 3.51 | 0.38 | 2.80 | 493 | per theorem: 381ms |
| E2h_n32_k4_oneliteral | ok | 46.34 | 1.52 | 44.50 | 616 | per theorem: 1.52s |
| E2h_n32_k4_randmsg | ok | 3.07 | 1.40 | 1.28 | 616 | per theorem: 1.38s |
| E2h_n48_k8_dataonly | ok | 11.58 | 0.06 | 10.50 | 521 |  |
| E3_n8_k2_randmsg | ok | 3.99 | 3.51 | 0.15 | 1085 | per theorem: 3.5s |
| baseline_empty | ok | 0.31 | - | 0.00 | 441 |  |
| baseline_empty_ulimit6000000 | FAIL: libc++abi: terminating due to uncaught exception of type lean::exception: failed to create thread | 0.26 | - | - | 442 |  |
| pitfall_thunk_chain | ok | 24.68 | 24.30 | 0.02 | 1260 | per theorem: 2.08s, 4.61s, 17.7s |
| pitfall_thunk_forced | ok | 17.92 | 17.60 | 0.01 | 1486 | per theorem: 3.04s, 6s, 8.6s |
| pitfall_thunk_forced_4theorems_aborted | FAIL: libc++abi: terminating due to uncaught exception of type std::bad_alloc: std::bad_alloc | 21.96 | - | - | 1610 |  |
| pitfall_thunk_forced_single | ok | 9.27 | 9.01 | 0.01 | 1362 | per theorem: 9.01s |
