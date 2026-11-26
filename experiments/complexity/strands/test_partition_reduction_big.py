from test_partition_reduction import run
ok = True
cases = [([2, 2, 3, 1], 2, 4), ([3, 3, 2], 2, 4), ([3, 3, 1, 1], 2, 4), ([2, 2, 2, 2], 2, 4), ([3, 2, 2, 1], 2, 4),
         ([2, 1, 2, 1, 3], 3, 3), ([2, 2, 2, 3], 3, 3), ([2, 2, 2, 2, 1], 3, 3), ([4, 4, 2], 2, 5), ([3, 3, 4], 2, 5),
         ([3, 2, 3, 2], 2, 5), ([4, 3, 3], 2, 5)]
for items, m, B in cases:
    ok &= run(items, m, B, "stack")
    ok &= run(items, m, B, "random", seed=7, sigma=3)
print("ALL OK" if ok else "SOME MISMATCH")
