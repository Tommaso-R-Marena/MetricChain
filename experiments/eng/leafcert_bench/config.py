"""The fixed protocol of the certificate benchmark, as data (the text is ``PROTOCOL.txt``).

Nothing here was changed after the first run on the test seeds; ``PROTOCOL.txt`` has a section
"Deviations" for anything that was.
"""
from __future__ import annotations

PROTOCOL_VERSION = 1
MASTER = "leafcert-bench-v1"            # master string of the test seeds (development used "leafprod-dev")
INSTANCES = 10                          # instances per cell
TIME_LIMIT = 60.0                       # seconds, every time-limited run of the main pass
LONG_TIME_LIMIT = 600.0                 # seconds, the second pass
CPUS = (5, 7)                           # the two workers are pinned to these logical CPUs (different cores)

# the producer of the main pass
MAIN = {"bound": "mp", "branching": "strong", "order": "best", "seed": 0}
CAPS = {"max_leaves": 10 ** 6, "max_cert_integers": 2 * 10 ** 6, "max_check_ops": 2 * 10 ** 7}
LONG_CAPS = {"max_leaves": 10 ** 6, "max_cert_integers": 10 ** 7, "max_check_ops": 10 ** 8}

# baselines
BRUTE_MAX_STATES = 1 << 24
DP_MAX_TABLE = 1 << 23
GENERAL_INSTANCES = 2                   # CP-SAT and MILP are run on the instances 0 and 1 of a cell ...
GENERAL_K5_FAMILIES = ("chain", "grid", "complete")     # ... of the ladders with k in {2, 3}, and with k = 5 of these
GENERAL_HITS_TO_STOP = 1                # ... and leave a ladder after their first time-limit hit
EXTENSION_INSTANCES = 3                 # cells after the producer has stopped on a ladder: instances 0 .. 2
HITS_TO_STOP = 2                        # the search without certificate stops in a cell after two limit hits
PLAIN_UNCERTIFIED = 3                   # ... and is run on the first three instances the producer did not certify
ROOT_LP_TIME_LIMIT = 20.0

ALPHABETS = (2, 3, 5, 10, "mixed")
SIZES = {
    "chain": (6, 12, 25, 50, 100),
    "tree": (6, 12, 25, 50, 100),
    "potts": (6, 12, 25, 49, 100),
    "grid": (6, 12, 25, 49, 100),
    "cubic": (6, 12, 24, 50, 100),
    "band2": (6, 12, 25, 50, 100),
    "band3": (6, 12, 25, 50, 100),
    "complete": (6, 8, 10, 12, 16, 20, 24, 28, 32, 36),
}
FAMILY_ORDER = ("chain", "tree", "potts", "grid", "cubic", "band2", "band3", "complete")

# wall-clock budgets in minutes: no new cell of a phase is started after its budget (a started cell is finished)
BUDGET_MIN = {"main": 64.0, "compare": 20.0, "long": 16.0}

# the comparison pass: searches without certificate on the instances of the main pass.
# branching rules (bound mp), all 10 instances of each cell:
COMPARE_RULE_CELLS = [("band3", 3, 50), ("band3", 5, 50), ("band2", 5, 50), ("grid", 5, 49), ("cubic", 5, 50),
                      ("complete", 2, 20), ("complete", 3, 12), ("complete", 5, 10), ("complete", 10, 8),
                      ("complete", "mixed", 12), ("grid", "mixed", 49), ("band3", 2, 50), ("band2", 3, 50),
                      ("grid", 3, 49), ("grid", 10, 49), ("cubic", 3, 50), ("potts", 5, 49)]
COMPARE_RULES = (("mp", "strong"), ("mp", "maxdeg"), ("mp", "margin"), ("mp", "maxdom"))
# leaf-bound methods, instances 0 .. 4 of each cell (smaller sizes: the linear programme is slow):
COMPARE_LP_CELLS = [("complete", 2, 20), ("complete", 3, 12), ("complete", 5, 8), ("band3", 3, 25), ("band3", 5, 25),
                    ("band2", 5, 25), ("grid", 5, 25), ("grid", 10, 25), ("cubic", 5, 24)]
COMPARE_BOUNDS = (("mp", "strong"), ("lp", "strong"), ("hybrid", "strong"), ("lp", "frac"))
COMPARE_LP_INSTANCES = 5
COMPARE_CERTIFIED = (("lp", "strong"), ("hybrid", "strong"))     # instances 0 and 1: certificate built and checked
COMPARE_CERTIFIED_INSTANCES = 2
# order of the comparison cells (the budget rule cuts from the end)
COMPARE_CELLS = COMPARE_LP_CELLS + [cell for cell in COMPARE_RULE_CELLS if cell not in COMPARE_LP_CELLS]

# the second pass (600 s; size caps LONG_CAPS for the producer): for each entry, in this order, the first cell
# of the ladder in which the solver missed an instance in the main pass, and the first two instances it missed
LONG_ORDER = (("complete", 2, "plain"), ("complete", 2, "producer"), ("band3", 3, "producer"),
              ("complete", 2, "milp"), ("complete", 2, "cpsat"), ("complete", 5, "producer"),
              ("complete", 5, "plain"), ("grid", 5, "producer"))

WORKER_ADDRESS_SPACE = 3 << 30          # bytes of address space per worker (a guard; the caps keep the use far below)


def ladders():
    """The ladders ``(family, k, sizes)`` in the fixed order."""
    return [(family, k, SIZES[family]) for family in FAMILY_ORDER for k in ALPHABETS]


def general_ladder(family, k):
    """Whether CP-SAT and MILP are run on the ladder."""
    return k in (2, 3) or (k == 5 and family in GENERAL_K5_FAMILIES)


def cell_name(family, k, n):
    return f"{family}__k{k}__n{n}"
