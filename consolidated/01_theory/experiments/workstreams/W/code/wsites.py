"""wsites.py -- the example sites and chains of the worked example (W5), in one place.

Envelopes are multiples of a common unit so that all transport costs at finite n lie on a lattice.
"""
import numpy as np

from wlib import Site, Chain, binary_site


def path_site():
    """three states on a path 0 - 1 - 2 with unequal steps 0.8 and 1.6; non-uniform site law"""
    a, b = 0.8, 1.6
    d = [[0, a, a + b], [a, 0, b], [a + b, b, 0]]
    return Site([0.5, 0.3, 0.2], d, "path(0.8,1.6)")


def tri_site():
    """three states, triangle with unequal sides d01 = 1.0, d12 = 1.5, d02 = 2.0 (all triangle inequalities strict)"""
    d = [[0, 1.0, 2.0], [1.0, 0, 1.5], [2.0, 1.5, 0]]
    return Site([0.2, 0.5, 0.3], d, "tri(1,1.5,2)")


def asym_site():
    """three states, asymmetric envelope that is not 'metric + gradient' (the antisymmetric part is not exact)"""
    d = [[0, 1.0, 2.0], [0.5, 0, 1.5], [1.0, 0.5, 0]]
    return Site([0.5, 0.3, 0.2], d, "asym")


def bin_site():
    return binary_site(0.3, 1.0, "bin(0.3,1)")


def chains():
    P, T, A, B = path_site(), tri_site(), asym_site(), bin_site()
    return {
        "path": Chain([P], [1.0], "path"),
        "tri": Chain([T], [1.0], "tri"),
        "asym": Chain([A], [1.0], "asym"),
        "bin": Chain([B], [1.0], "bin"),
        "mix": Chain([B, P], [0.5, 0.5], "mix(bin,path)"),
        "mix2": Chain([B, T], [0.4, 0.6], "mix(bin,tri)"),
    }
