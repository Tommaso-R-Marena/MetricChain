"""Strict loading, structural validation and text encoding of "shares at the leaves" certificates.

The format is the one of the science division's workstream P7 (``docs/science/workstreams/P7_REPORT.md``
§5.1 at commit ``2b4ccdf`` of ``research/scientific-translation``; files ``p7_02_cert*.json``).  This module
was written from that text and from the nine files, not from their code.  Three things live here:

``parse_json_strict``
    JSON text -> Python object.  Duplicate keys, numbers with a fraction or an exponent, ``NaN`` and
    ``Infinity``, invalid UTF-8 and trailing data are errors.

``validate``
    object -> :class:`Cert` (the certificate in a normal form).  Every departure from the format is a
    :class:`FormatError` with a reason; nothing is repaired, completed or ignored.  The rules:

    * top level: an object with the keys ``H``, ``J``, ``L``, ``tree``, ``leaves``; optionally ``shape``
      (redundant, must agree with ``H``) and the annotation keys of :data:`TOP_ANNOTATIONS`.  Any other
      key is an error.
    * ``H``: a list of ``n >= 1`` lists; ``H[i]`` has ``k_i >= 1`` integers (``k_i`` is the number of states
      of site ``i``; the domain certified is the whole product of the alphabets ``{0..k_i-1}``).
    * ``J``: an object with exactly the keys ``"i,j"`` for ``0 <= i < j < n``; ``J["i,j"]`` is a list of
      ``k_i`` rows of ``k_j`` integers, ``J["i,j"][a][b] = J_ij(a, b)`` (``a`` a state of ``i``).
    * ``L``: an integer, the bound to certify.
    * ``leaves``: a non-empty list of objects with the keys ``U`` (``n`` integers), ``P2`` (object with
      exactly the keys ``"i,j"``, ``i < j``, integer values) and ``m`` (object with exactly the keys
      ``"i,j"`` for all ordered pairs ``i != j``; ``m["i,j"]`` is a list of ``k_i`` integers,
      ``m["i,j"][a] = m_ij(a)``), optionally the annotation keys of :data:`LEAF_ANNOTATIONS`.
    * ``tree``: ``{"leaf": t}`` with ``0 <= t < len(leaves)``, or ``{"site": i, "children": {...}}`` with
      ``0 <= i < n``, ``i`` not branched on by an ancestor, and ``children`` an object whose keys are exactly
      the decimal strings ``"0" .. str(k_i - 1)`` (missing and extra children are both errors).
    * every leaf certificate is referenced by at least one node of the tree.
    * an integer is a JSON number without fraction or exponent (Python ``int``, not ``bool``).

    Annotation keys are *not* part of the certificate: their values never influence a verdict and are not
    validated here (see :func:`annotation_findings` for consistency checks of the ones the nine files carry).

``encode``
    :class:`Cert` -> the text read by ``leafcert.c`` (grammar in the header of that file).  The encoder is a
    plain transcription; the C checker re-validates everything it reads.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass

TOP_REQUIRED = ("H", "J", "L", "tree", "leaves")
TOP_OPTIONAL = ("shape",)
TOP_ANNOTATIONS = ("label", "variant", "instance", "tag", "tau", "split", "order", "unit_log2", "ref",
                   "n_leaf_certificates", "n_leaf_boxes", "depth", "note")
LEAF_REQUIRED = ("U", "P2", "m")
LEAF_ANNOTATIONS = ("kind", "box", "LB", "bf_min", "nstates")


class FormatError(ValueError):
    """The input is not a well-formed certificate (the reason is the message)."""


@dataclass(frozen=True)
class Leaf:
    U: tuple      # U[i], n integers
    P2: tuple     # P2 of the pairs i < j in lexicographic order, n(n-1)/2 integers
    m: tuple      # m[q] = (m_ij(0), ..., m_ij(k_i - 1)) for the ordered pairs (i, j), i != j, in lexicographic order


@dataclass(frozen=True)
class Cert:
    """Normal form of a certificate.  ``tree`` is ``("L", t)`` or ``("B", site, ((state, subtree), ...))``
    with the children in increasing order of the state."""
    shape: tuple  # k_i
    L: int
    H: tuple      # H[i] = (H_i(0), ..., H_i(k_i - 1))
    J: tuple      # J[p] = row-major (a outer, b inner) table of the p-th pair i < j in lexicographic order
    leaves: tuple
    tree: tuple


# ----------------------------------------------------------------------------------------------- JSON
def _no_duplicate_keys(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise FormatError(f"duplicate key {key!r} in a JSON object")
        out[key] = value
    return out


def _reject_float(text):
    raise FormatError(f"number {text!r} is not an integer (fraction or exponent)")


def _reject_constant(text):
    raise FormatError(f"{text} is not an integer")


def parse_json_strict(data):
    """Parse JSON text (``bytes`` in UTF-8, or ``str``) strictly; see the module docstring."""
    if isinstance(data, (bytes, bytearray, memoryview)):
        try:
            text = bytes(data).decode("utf-8")
        except UnicodeDecodeError as exc:
            raise FormatError(f"not UTF-8: {exc}") from None
    elif isinstance(data, str):
        text = data
    else:
        raise TypeError("parse_json_strict needs bytes or str")
    try:
        return json.loads(text, object_pairs_hook=_no_duplicate_keys, parse_float=_reject_float,
                          parse_constant=_reject_constant)
    except FormatError:
        raise
    except RecursionError:
        raise FormatError("JSON nesting too deep") from None
    except ValueError as exc:          # json.JSONDecodeError, and the interpreter's limit on integer digits
        raise FormatError(f"not valid JSON: {exc}") from None


def load(path_or_obj):
    """A path (``str`` or ``os.PathLike``), JSON text as ``bytes``, or an already parsed object -> the object.
    A ``dict`` is returned as it is (duplicate keys can no longer be detected in it)."""
    if isinstance(path_or_obj, dict):
        return path_or_obj
    if isinstance(path_or_obj, (bytes, bytearray, memoryview)):
        return parse_json_strict(path_or_obj)
    if isinstance(path_or_obj, (str, os.PathLike)):
        with open(path_or_obj, "rb") as handle:
            return parse_json_strict(handle.read())
    raise TypeError("expected a path, JSON bytes or a parsed JSON object")


# ----------------------------------------------------------------------------------------------- validation
def _kind(x):
    return {dict: "an object", list: "a list", str: "a string", int: "an integer", bool: "a boolean",
            float: "a non-integer number", type(None): "null"}.get(type(x), type(x).__name__)


def _ints(x, length, where):
    if type(x) is not list:
        raise FormatError(f"{where}: expected a list of {length} integers, found {_kind(x)}")
    if len(x) != length:
        raise FormatError(f"{where}: expected {length} integers, found {len(x)}")
    if x and set(map(type, x)) != {int}:
        for pos, v in enumerate(x):
            if type(v) is not int:
                raise FormatError(f"{where}[{pos}]: expected an integer, found {_kind(v)}")
    return tuple(x)


def _keys(x, required, optional, where):
    if type(x) is not dict:
        raise FormatError(f"{where}: expected an object, found {_kind(x)}")
    for key in x:
        if type(key) is not str:
            raise FormatError(f"{where}: key {key!r} is not a string")
    missing = [key for key in required if key not in x]
    if missing:
        raise FormatError(f"{where}: missing key(s) {missing[:6]}{' ...' if len(missing) > 6 else ''}")
    allowed = set(required) | set(optional)
    extra = [key for key in x if key not in allowed]
    if extra:
        raise FormatError(f"{where}: unexpected key(s) {extra[:6]}{' ...' if len(extra) > 6 else ''}")


def _exact_keys(x, keys, keyset, where):
    """``x`` is an object with exactly the keys ``keys`` (``keyset`` is the same as a set)."""
    if type(x) is not dict or x.keys() != keyset:
        _keys(x, keys, (), where)


def _validate_tree(tree, shape, nleaves):
    """The tree in normal form.  Every branch is on a site that no ancestor fixed and has exactly one child
    per state of that site; every leaf index is in range; every leaf certificate is used.  Iterative, so
    that no input can exhaust the interpreter's stack."""
    n = len(shape)
    states = [[str(a) for a in range(k)] for k in shape]
    root = [None]
    stack = [(tree, (), root, 0)]          # (JSON node, path of (site, state) pairs, list to fill, position in it)
    order, used = [], set()
    while stack:
        node, path, slot, pos = stack.pop()
        if type(node) is not dict or not (("leaf" in node and len(node) == 1)
                                          or ("site" in node and "children" in node and len(node) == 2)):
            where = "tree" + "".join(f".children[{a}]" for _, a in path)
            if type(node) is not dict:
                raise FormatError(f"{where}: expected an object, found {_kind(node)}")
            _keys(node, ("leaf",) if "leaf" in node else ("site", "children"), (), where)
        if "leaf" in node:
            t = node["leaf"]
            if type(t) is not int or not 0 <= t < nleaves:
                where = "tree" + "".join(f".children[{a}]" for _, a in path)
                if type(t) is not int:
                    raise FormatError(f"{where}.leaf: expected an integer, found {_kind(t)}")
                raise FormatError(f"{where}.leaf: index {t} is outside 0..{nleaves - 1}")
            used.add(t)
            slot[pos] = ("L", t)
            continue
        site, children = node["site"], node["children"]
        if type(site) is not int or not 0 <= site < n or any(site == s for s, _ in path):
            where = "tree" + "".join(f".children[{a}]" for _, a in path)
            if type(site) is not int:
                raise FormatError(f"{where}.site: expected an integer, found {_kind(site)}")
            if not 0 <= site < n:
                raise FormatError(f"{where}.site: site {site} is outside 0..{n - 1}")
            raise FormatError(f"{where}.site: branch on site {site}, which an ancestor has already fixed")
        k = shape[site]
        if type(children) is not dict or len(children) != k or not all(key in children for key in states[site]):
            where = "tree" + "".join(f".children[{a}]" for _, a in path)
            _keys(children, states[site], (), f"{where}.children (states 0..{k - 1} of site {site})")
        kids = [None] * k
        slot[pos] = ["B", site, kids]
        order.append(slot[pos])
        for a in range(k - 1, -1, -1):
            stack.append((children[states[site][a]], path + ((site, a),), kids, a))
    missing = [t for t in range(nleaves) if t not in used]
    if missing:
        raise FormatError(f"leaves: leaf certificate(s) {missing[:6]}{' ...' if len(missing) > 6 else ''} "
                          f"not referenced by the tree")
    for branch in reversed(order):         # children before parents: lists -> tuples of (state, subtree)
        branch[2] = tuple((a, tuple(kid) if type(kid) is list else kid) for a, kid in enumerate(branch[2]))
    return tuple(root[0])


def validate(obj):
    """The object of a certificate file -> :class:`Cert`; raises :class:`FormatError` with the reason."""
    _keys(obj, TOP_REQUIRED, TOP_OPTIONAL + TOP_ANNOTATIONS, "top level")
    # instance
    H_in = obj["H"]
    if type(H_in) is not list:
        raise FormatError(f"H: expected a list, found {_kind(H_in)}")
    n = len(H_in)
    if n == 0:
        raise FormatError("H: no site")
    H = []
    for i, row in enumerate(H_in):
        if type(row) is not list:
            raise FormatError(f"H[{i}]: expected a list of integers, found {_kind(row)}")
        if len(row) == 0:
            raise FormatError(f"H[{i}]: site {i} has no state (empty domain)")
        H.append(_ints(row, len(row), f"H[{i}]"))
    shape = tuple(len(row) for row in H)
    if "shape" in obj:
        declared = obj["shape"]
        if type(declared) is not list or any(type(v) is not int for v in declared):
            raise FormatError("shape: expected a list of integers")
        if tuple(declared) != shape:
            raise FormatError(f"shape: {declared} disagrees with the lengths of the rows of H, {list(shape)}")
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    ordered = [(i, j) for i in range(n) for j in range(n) if i != j]
    pair_keys = [f"{i},{j}" for i, j in pairs]
    ordered_keys = [f"{i},{j}" for i, j in ordered]
    pair_set, ordered_set = set(pair_keys), set(ordered_keys)
    _exact_keys(obj["J"], pair_keys, pair_set, "J")
    J = []
    for (i, j), key in zip(pairs, pair_keys):
        table = obj["J"][key]
        if type(table) is not list:
            raise FormatError(f"J[{key!r}]: expected a list of {shape[i]} rows, found {_kind(table)}")
        if len(table) != shape[i]:
            raise FormatError(f"J[{key!r}]: expected {shape[i]} rows (states of site {i}), found {len(table)}")
        flat = []
        for a, row in enumerate(table):
            flat.extend(_ints(row, shape[j], f"J[{key!r}][{a}]"))
        J.append(tuple(flat))
    L = obj["L"]
    if type(L) is not int:
        raise FormatError(f"L: expected an integer, found {_kind(L)}")
    # leaf certificates
    leaves_in = obj["leaves"]
    if type(leaves_in) is not list:
        raise FormatError(f"leaves: expected a list, found {_kind(leaves_in)}")
    if not leaves_in:
        raise FormatError("leaves: no leaf certificate")
    leaves = []
    for t, leaf in enumerate(leaves_in):
        where = f"leaves[{t}]"
        _keys(leaf, LEAF_REQUIRED, LEAF_ANNOTATIONS, where)
        U = _ints(leaf["U"], n, f"{where}.U")
        _exact_keys(leaf["P2"], pair_keys, pair_set, f"{where}.P2")
        P2 = [leaf["P2"][key] for key in pair_keys]
        if P2 and set(map(type, P2)) != {int}:
            for key, v in zip(pair_keys, P2):
                if type(v) is not int:
                    raise FormatError(f"{where}.P2[{key!r}]: expected an integer, found {_kind(v)}")
        _exact_keys(leaf["m"], ordered_keys, ordered_set, f"{where}.m")
        m = tuple(_ints(leaf["m"][key], shape[i], f"{where}.m[{key!r}]") for (i, _), key in zip(ordered, ordered_keys))
        leaves.append(Leaf(U=U, P2=tuple(P2), m=m))
    tree = _validate_tree(obj["tree"], shape, len(leaves))
    return Cert(shape=shape, L=L, H=tuple(H), J=tuple(J), leaves=tuple(leaves), tree=tree)


# ----------------------------------------------------------------------------------------------- encoding
def tree_tokens(tree):
    """Preorder tokens of a tree in normal form: ``L t`` or ``B site count (state subtree)*``.  A plain
    transcription: it also writes trees that are not well formed (tests use that against the C checker)."""
    out, stack = [], [tree]
    while stack:
        cur = stack.pop()
        if type(cur) is not tuple:         # a state label waiting to be written before its subtree
            out.append(str(cur))
            continue
        if cur[0] == "L":
            out += ["L", str(cur[1])]
        else:
            out += ["B", str(cur[1]), str(len(cur[2]))]
            for state, sub in reversed(cur[2]):
                stack.append(sub)
                stack.append(state)
    return out


def encode(cert):
    """:class:`Cert` -> ASCII text for ``leafcert.c``."""
    n = len(cert.shape)
    lines = ["leafcert 1", f"sites {n}", "shape " + " ".join(map(str, cert.shape)), f"bound {cert.L}"]
    for i, row in enumerate(cert.H):
        lines.append(f"h {i} " + " ".join(map(str, row)))
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    ordered = [(i, j) for i in range(n) for j in range(n) if i != j]
    for (i, j), table in zip(pairs, cert.J):
        lines.append(f"j {i} {j} " + " ".join(map(str, table)))
    lines.append(f"leaves {len(cert.leaves)}")
    for t, leaf in enumerate(cert.leaves):
        lines.append(f"leaf {t}")
        lines.append(" ".join(["u", *map(str, leaf.U)]))
        lines.append(" ".join(["p", *map(str, leaf.P2)]))
        for (i, j), vec in zip(ordered, leaf.m):
            lines.append(f"m {i} {j} " + " ".join(map(str, vec)))
    lines.append("tree")
    lines.append(" ".join(tree_tokens(cert.tree)))
    lines.append("end")
    return ("\n".join(lines) + "\n").encode("ascii")


# ----------------------------------------------------------------------------------------------- annotations
def annotation_findings(obj, cert=None):
    """Consistency of the annotation keys carried by the science division's files with the certificate
    itself.  Returns a list of findings (empty if everything agrees).  None of this is part of a verdict;
    the meaning of the keys is inferred from the nine files and their ``note`` (the report does not define
    them): ``n_leaf_certificates``, ``n_leaf_boxes``, ``depth``, ``ref`` (a state where the instance takes
    the value ``L``), ``order`` (2), and per leaf ``box`` (the per-site union of the boxes of the nodes that
    use the leaf), ``nstates`` (its number of states), ``LB`` (``sum U + sum P2``), ``kind`` (``"R"`` iff the
    box contains ``ref``).  ``bf_min`` needs an enumeration and is checked elsewhere."""
    cert = cert if cert is not None else validate(obj)
    n, shape = len(cert.shape), cert.shape
    out = []
    boxes = [[set() for _ in range(n)] for _ in cert.leaves]      # per leaf, per site: union of the domains
    leaf_nodes, depth = 0, 0
    stack = [(cert.tree, ())]
    while stack:
        node, path = stack.pop()
        if node[0] == "B":
            for state, sub in node[2]:
                stack.append((sub, path + ((node[1], state),)))
            continue
        leaf_nodes += 1
        depth = max(depth, len(path))
        fixed = dict(path)
        for i in range(n):
            boxes[node[1]][i].update([fixed[i]] if i in fixed else range(shape[i]))
    for key, value in (("n_leaf_certificates", len(cert.leaves)), ("n_leaf_boxes", leaf_nodes), ("depth", depth),
                       ("order", 2)):
        if key in obj and (type(obj[key]) is not int or obj[key] != value):
            out.append(f"{key} = {obj[key]!r}, the certificate gives {value}")
    ref = obj.get("ref")
    ref_ok = False
    if "ref" in obj:
        if type(ref) is not list or len(ref) != n or any(type(v) is not int or not 0 <= v < shape[i] for i, v in enumerate(ref)):
            out.append("ref is not a state of the domain")
        else:
            ref_ok = True
            energy = sum(cert.H[i][ref[i]] for i in range(n))
            p = 0
            for i in range(n):
                for j in range(i + 1, n):
                    energy += cert.J[p][ref[i] * shape[j] + ref[j]]
                    p += 1
            if energy != cert.L:
                out.append(f"the instance takes the value {energy} at ref, not the bound L = {cert.L}")
    for t, leaf in enumerate(obj["leaves"]):
        box = [sorted(s) for s in boxes[t]]
        if "box" in leaf and leaf["box"] != box:
            out.append(f"leaves[{t}].box is not the union of the boxes of the nodes that use the leaf")
        size = 1
        for dom in box:
            size *= len(dom)
        if "nstates" in leaf and (type(leaf["nstates"]) is not int or leaf["nstates"] != size):
            out.append(f"leaves[{t}].nstates = {leaf['nstates']!r}, the box has {size} states")
        total = sum(cert.leaves[t].U) + sum(cert.leaves[t].P2)
        if "LB" in leaf and (type(leaf["LB"]) is not int or leaf["LB"] != total):
            out.append(f"leaves[{t}].LB = {leaf['LB']!r}, sum U + sum P2 = {total}")
        if "kind" in leaf and ref_ok:
            expected = "R" if all(ref[i] in boxes[t][i] for i in range(n)) else "N"
            if leaf["kind"] != expected:
                out.append(f"leaves[{t}].kind = {leaf['kind']!r}, expected {expected!r} (box contains ref: {expected == 'R'})")
    return out
