#!/usr/bin/env python3
"""Collect logs/*.log of the kernel-evaluation experiment into results.tsv and results.md.

Standard library only.  Every number in the tables is read from a log written by run.sh.
"""
import glob
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
NAME_RE = re.compile(r'^(E\d+h?)_n(\d+)_k(\d+)(?:_(.*))?$')
ORDER = {'E1': 0, 'E4': 1, 'E2': 2, 'E2h': 3, 'E3': 4}


def seconds(text):
    """'396ms' / '5.31s' / '1min 2s' -> seconds."""
    m = re.match(r'^([0-9.]+)(ms|s)$', text)
    if not m:
        return None
    val = float(m.group(1))
    return val / 1000.0 if m.group(2) == 'ms' else val


def parse(path):
    name = os.path.basename(path)[:-4]
    rec = {'name': name, 'enc': '', 'n': '', 'k': '', 'variant': '', 'status': '', 'wall': '',
           'rss_mb': '', 'kernel_s': '', 'elab_s': '', 'watchdog': '', 'axioms': '', 'error': '',
           'bytes': ''}
    m = NAME_RE.match(name)
    if m:
        rec['enc'], rec['n'], rec['k'] = m.group(1), int(m.group(2)), int(m.group(3))
        rec['variant'] = m.group(4) or 'pos'
    rss, polled = 0, 0
    cumulative = False
    kernel_lines = []
    with open(path, errors='replace') as fh:
        for line in fh:
            line = line.rstrip('\n')
            if line.startswith('MEASURE wall_seconds:'):
                rec['wall'] = float(line.split(':')[1])
            elif line.startswith('MEASURE max_rss_kb:'):
                rss = int(line.split(':')[1])
            elif line.startswith('MEASURE polled_peak_rss_kb:'):
                polled = int(line.split(':')[1])
            elif line.startswith('MEASURE rss_watchdog_killed:'):
                rec['watchdog'] = line.split(':')[1].strip()
            elif line.startswith('RUN status:'):
                rec['status'] = int(line.split(':')[1])
            elif line.startswith('RUN bytes:'):
                rec['bytes'] = line.split(':')[1].strip()
            elif line.startswith('cumulative profiling times:'):
                cumulative = True
            elif cumulative and line.startswith('\t'):
                key, _, val = line.strip().rpartition(' ')
                if key == 'type checking':
                    rec['kernel_s'] = seconds(val)
                elif key == 'elaboration':
                    rec['elab_s'] = seconds(val)
            elif line.startswith('type checking took '):
                kernel_lines.append(line[len('type checking took '):])
            elif 'depend' in line and 'axioms' in line:
                rec['axioms'] = 'none' if 'does not depend on any axioms' in line else \
                    line.split('axioms:')[-1].strip()
            elif ': error:' in line and not rec['error']:
                rec['error'] = line.split(': error:', 1)[1].strip()[:110]
            elif not rec['error'] and ('terminating due to' in line or 'out of memory' in line
                                       or 'Cannot allocate memory' in line
                                       or 'Stack overflow' in line or 'deep recursion' in line):
                rec['error'] = line.strip()[:110]
    rec['rss_mb'] = round(max(rss, polled) / 1024.0)
    rec['kernel_lines'] = ', '.join(kernel_lines)
    return rec


def outcome(rec):
    if rec['variant'] == 'negL_claimtrue':
        if rec['status'] != 0 and rec['error']:
            return 'rejected, as it must be'
        return 'NOT REJECTED (bug)'
    if rec['status'] == 0 and not rec['error']:
        return 'ok'
    if rec['watchdog'] == 'yes':
        return 'FAIL: resident memory above 5 GB, killed'
    if rec['status'] == 124:
        return 'FAIL: timeout'
    if 'Cannot allocate memory' in rec['error']:
        return 'FAIL: out of memory under `ulimit -v` (%s)' % rec['error']
    if rec['error']:
        return 'FAIL: ' + rec['error']
    return 'FAIL: status %s' % rec['status']


def fmt(x, digits=2):
    if x == '' or x is None:
        return '-'
    if isinstance(x, float):
        return ('%.' + str(digits) + 'f') % x
    return str(x)


def main():
    recs = [parse(p) for p in sorted(glob.glob(os.path.join(HERE, 'logs', '*.log')))]
    recs.sort(key=lambda r: (ORDER.get(r['enc'], 9), r['n'] if r['n'] != '' else 0,
                             r['k'] if r['k'] != '' else 0, r['variant']))
    cols = ['name', 'enc', 'n', 'k', 'variant', 'status', 'outcome', 'wall', 'kernel_s', 'elab_s',
            'rss_mb', 'axioms', 'bytes', 'error']
    with open(os.path.join(HERE, 'results.tsv'), 'w') as fh:
        fh.write('\t'.join(cols) + '\n')
        for r in recs:
            r['outcome'] = outcome(r)
            fh.write('\t'.join(fmt(r.get(c, '')) for c in cols) + '\n')

    out = []
    out.append('<!-- written by collect.py from logs/*.log -->\n')
    out.append('### Main table: `leafCheck … = true := by decide +kernel`\n')
    out.append('| encoding | n | k | n²k² | cells n(n-1)/2·k² | result | wall s | kernel s | '
               'elaboration s | peak RSS MB | axioms |')
    out.append('|---|---|---|---|---|---|---|---|---|---|---|')
    for r in recs:
        if r['variant'] != 'pos' or r['enc'] == '':
            continue
        n, k = r['n'], r['k']
        out.append('| %s | %d | %d | %d | %d | %s | %s | %s | %s | %s | %s |' % (
            r['enc'], n, k, n * n * k * k, n * (n - 1) // 2 * k * k, r['outcome'], fmt(r['wall']),
            fmt(r['kernel_s']), fmt(r['elab_s']), fmt(r['rss_mb']), r['axioms'] or '-'))
    out.append('\n### Negative controls and tactic variants\n')
    out.append('| encoding | n | k | file variant | claim / tactic | result | wall s | kernel s | '
               'peak RSS MB |')
    out.append('|---|---|---|---|---|---|---|---|---|')
    what = {'negL': '`= false`, L+1 (C fails)', 'negU': '`= false`, one u+1 (A fails)',
            'negP': '`= false`, one p+1 (B fails)',
            'negJ': '`= false`, one J entry lowered (B fails in the last cell)',
            'negJ0': '`= false`, one J entry lowered (B fails in the first cell)',
            'negL_claimtrue': '`= true` on the L+1 data (wrong claim)',
            'tac_decide': '`= true := by decide` (no `+kernel`)',
            'tac_rfl': '`= true := by rfl`'}
    for r in recs:
        if r['variant'] not in what:
            continue
        out.append('| %s | %d | %d | %s | %s | %s | %s | %s | %s |' % (
            r['enc'], r['n'], r['k'], r['variant'], what[r['variant']], r['outcome'],
            fmt(r['wall']), fmt(r['kernel_s']), fmt(r['rss_mb'])))
    out.append('\n### Side experiments\n')
    out.append('| log | result | wall s | kernel s | elaboration s | peak RSS MB | note |')
    out.append('|---|---|---|---|---|---|---|')
    for r in recs:
        if r['variant'] in what or (r['variant'] == 'pos' and r['enc'] != ''):
            continue
        out.append('| %s | %s | %s | %s | %s | %s | %s |' % (
            r['name'], r['outcome'], fmt(r['wall']), fmt(r['kernel_s']), fmt(r['elab_s']),
            fmt(r['rss_mb']), r['kernel_lines'] and ('per theorem: ' + r['kernel_lines']) or ''))
    with open(os.path.join(HERE, 'results.md'), 'w') as fh:
        fh.write('\n'.join(out) + '\n')
    print('\n'.join(out))


if __name__ == '__main__':
    main()
