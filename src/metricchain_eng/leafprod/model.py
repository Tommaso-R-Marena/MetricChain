"""The instance in the sparse form the producer computes with.

An instance is given as in a certificate file: ``H[i][a]`` (site ``i``, state ``a``) and ``J["i,j"][a][b]`` for
pairs ``i < j``.  The certificate format is dense (a table for every pair); here a pair is an *edge* only if
its table is not identically zero, and messages exist on edges only.  A pair without an edge gets zero
messages and ``P2 = 0`` in every leaf certificate, which loses nothing: a zero table adds no constraint to
the pairwise relaxation.  ``J`` may omit pairs; they are zero tables (the certificate writes them out).
"""
from __future__ import annotations

import ctypes as ct

import numpy as np

MAX_ABS = 1 << 56            # largest absolute value of a table entry the producer accepts at all
MAX_SITES = 4096             # the limit of the C engine of the checker
SAFE = 1 << 62               # every int64 sum the kernel forms must stay below this in absolute value

_I64P = ct.POINTER(ct.c_int64)


class InstanceError(ValueError):
    """The instance is not one the producer can work with (the message says why)."""


class CModel(ct.Structure):
    """``lp_model`` of ``kernel.c``."""
    _fields_ = ([(name, ct.c_int64) for name in ("n", "ne", "S", "M")]
                + [(name, _I64P) for name in ("k", "koff", "H", "eu", "ev", "joff", "J", "moff", "aoff", "aedge")])


def _int_rows(table, rows, cols, where):
    if type(table) not in (list, tuple) or len(table) != rows:
        raise InstanceError(f"{where}: expected {rows} row(s)")
    out = np.empty((rows, cols), dtype=np.int64)
    for a, row in enumerate(table):
        if type(row) not in (list, tuple) or len(row) != cols:
            raise InstanceError(f"{where}[{a}]: expected a list of {cols} integers")
        for v in row:
            if type(v) is not int:
                raise InstanceError(f"{where}[{a}]: {v!r} is not an integer")
            if not -MAX_ABS <= v <= MAX_ABS:
                raise InstanceError(f"{where}[{a}]: |{v}| exceeds 2^56, the range this producer supports")
        out[a] = row
    return out


class Model:
    """Sparse integer form of an instance (numpy ``int64``, shared with the C kernel).

    ``n``, ``k[i]``, ``koff[i]`` (offset of site ``i`` in arrays over all (site, state) pairs, length ``S``),
    ``H`` (length ``S``), edges ``eu[e] < ev[e]`` with tables ``tables[e]`` (``k_u x k_v``), message vectors of
    length ``k_u + k_v`` per edge at ``moff[e]`` (total ``M``), ``nbrs[i]`` = list of ``(e, j)``.
    """

    def __init__(self, instance):
        if not isinstance(instance, dict) or "H" not in instance:
            raise InstanceError("an instance is a dict with the keys 'H' and 'J'")
        H_in = instance["H"]
        if type(H_in) not in (list, tuple) or len(H_in) == 0:
            raise InstanceError("H: expected a non-empty list (one list of integers per site)")
        n = len(H_in)
        if n > MAX_SITES:
            raise InstanceError(f"{n} sites: the checker's C engine stops at {MAX_SITES}")
        k = []
        for i, row in enumerate(H_in):
            if type(row) not in (list, tuple) or len(row) == 0:
                raise InstanceError(f"H[{i}]: expected a non-empty list of integers (a site needs a state)")
            k.append(len(row))
        self.n = n
        self.k = np.array(k, dtype=np.int64)
        self.koff = np.zeros(n + 1, dtype=np.int64)
        np.cumsum(self.k, out=self.koff[1:])
        self.S = int(self.koff[n])
        self.H = np.concatenate([_int_rows([row], 1, len(row), f"H[{i}]")[0] for i, row in enumerate(H_in)])
        J_in = instance.get("J", {})
        if not isinstance(J_in, dict):
            raise InstanceError("J: expected a dict with the keys 'i,j', i < j")
        eu, ev, tables = [], [], []
        seen = set()
        for key, table in J_in.items():
            try:
                si, sj = key.split(",")
                i, j = int(si), int(sj)
            except (AttributeError, ValueError):
                raise InstanceError(f"J: key {key!r} is not of the form 'i,j'") from None
            if key != f"{i},{j}" or not 0 <= i < j < n:
                raise InstanceError(f"J: key {key!r} is not 'i,j' with 0 <= i < j < {n} in decimal")
            seen.add((i, j))
            arr = _int_rows(table, k[i], k[j], f"J[{key!r}]")
            if arr.any():
                eu.append(i)
                ev.append(j)
                tables.append(arr)
        order = sorted(range(len(eu)), key=lambda e: (eu[e], ev[e]))
        self.eu = np.array([eu[e] for e in order], dtype=np.int64)
        self.ev = np.array([ev[e] for e in order], dtype=np.int64)
        self.tables = [np.ascontiguousarray(tables[e]) for e in order]
        self.ne = ne = len(order)
        self.joff = np.zeros(ne + 1, dtype=np.int64)
        self.moff = np.zeros(ne + 1, dtype=np.int64)
        for e in range(ne):
            ku, kv = k[self.eu[e]], k[self.ev[e]]
            self.joff[e + 1] = self.joff[e] + ku * kv
            self.moff[e + 1] = self.moff[e] + ku + kv
        self.J = (np.concatenate([t.ravel() for t in self.tables]) if ne else np.zeros(1, dtype=np.int64))
        self.M = int(self.moff[ne])
        self.nbrs = [[] for _ in range(n)]
        for e in range(ne):
            self.nbrs[int(self.eu[e])].append((e, int(self.ev[e])))
            self.nbrs[int(self.ev[e])].append((e, int(self.eu[e])))
        self.aoff = np.zeros(n + 1, dtype=np.int64)
        self.aoff[1:] = np.cumsum([len(x) for x in self.nbrs])
        self.aedge = np.array([e for x in self.nbrs for e, _ in x] or [0], dtype=np.int64)
        self.edge_index = {(int(self.eu[e]), int(self.ev[e])): e for e in range(ne)}
        self.missing_pairs = n * (n - 1) // 2 - len(seen)        # pairs absent from J (taken as zero tables)
        self.max_abs = int(max(np.abs(self.H).max(), np.abs(self.J).max()))
        # int64 safety: a site term is a table entry plus one message per neighbour.  Messages are refused
        # beyond ``max_message`` (checked after every kernel call), which keeps such sums below SAFE; the
        # tables must leave the messages room (they stay within a few sums of table entries).
        degree = max((len(x) for x in self.nbrs), default=0)
        self.max_message = SAFE // (degree + 2)
        if 8 * self.max_abs * (degree + 2) >= SAFE:
            raise InstanceError(f"entries up to {self.max_abs} with up to {degree} interacting neighbours per site: "
                                f"sums in 64-bit arithmetic would not be safe")
        # every energy is a sum of one entry per site and per edge
        self.energy_bound = (sum(int(np.abs(self.H[self.koff[i]:self.koff[i + 1]]).max()) for i in range(n))
                             + sum(int(np.abs(t).max()) for t in self.tables))
        if self.energy_bound >= SAFE:
            raise InstanceError("the energies of this instance may not fit in 64 bits")
        self._full = (self.k.copy(), np.concatenate([np.arange(x, dtype=np.int64) for x in k]))
        self.cstruct = CModel(n, ne, self.S, self.M, *[arr.ctypes.data_as(_I64P) for arr in (
            self.k, self.koff, self.H, self.eu, self.ev, self.joff, self.J, self.moff, self.aoff, self.aedge)])

    # ------------------------------------------------------------------------------------------ boxes
    def box(self, path=(), block=None):
        """The box of a tree node as ``(dlen, dom)``: the sites of ``path`` (pairs ``(site, state)``) fixed, all
        other sites free.  ``block = (site, states)`` restricts one more site to a list of states."""
        dlen, dom = self._full[0].copy(), self._full[1].copy()
        for i, a in path:
            dlen[i] = 1
            dom[self.koff[i]] = a
        if block is not None:
            i, states = block
            dlen[i] = len(states)
            dom[self.koff[i]:self.koff[i] + len(states)] = states
        return dlen, dom

    def zero_messages(self):
        return np.zeros(max(self.M, 1), dtype=np.int64)

    # ------------------------------------------------------------------------------------------ dense views
    def dense_tables(self):
        """``H`` and the dense ``J`` (every pair ``i < j``) as lists of Python integers, as the certificate
        format wants them."""
        n, k = self.n, self.k
        H = [self.H[self.koff[i]:self.koff[i + 1]].tolist() for i in range(n)]
        J = {}
        for i in range(n):
            for j in range(i + 1, n):
                e = self.edge_index.get((i, j))
                J[f"{i},{j}"] = (self.tables[e].tolist() if e is not None
                                 else [[0] * int(k[j]) for _ in range(int(k[i]))])
        return H, J

    def energy(self, x):
        """Energy of the state ``x`` with Python integers (independent of the C kernel)."""
        total = sum(int(self.H[self.koff[i] + x[i]]) for i in range(self.n))
        for e in range(self.ne):
            total += int(self.tables[e][x[int(self.eu[e])], x[int(self.ev[e])]])
        return total
