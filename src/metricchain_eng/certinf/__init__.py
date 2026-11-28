"""Certified inference over classes of Boltzmann weights (Phase II).

``core``     exact identified intervals of box (density-ratio) classes: the dual of Theorem 4.1, linear programmes,
             inconsistency certificates, lumping.
``certify``  bounds certified from samples (Theorem 5.1), S3 as proposed, abstention rules.
``metric``   ratio-constrained (bounded-influence) classes; geometric stress observables.

Mathematics: docs/engineering/phase2/CERTIFIED_INFERENCE.md.
"""
from .core import *          # noqa: F401,F403
from .certify import *       # noqa: F401,F403
from .metric import *        # noqa: F401,F403
