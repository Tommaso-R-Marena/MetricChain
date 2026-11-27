#!/usr/bin/env python3
"""Run one command, report wall time and peak resident memory, and kill it if it grows too large.

Stand-in for `/usr/bin/time -v` (not installed on the experiment machine).  The numbers come from
`os.wait4`, i.e. from the same kernel accounting (`ru_maxrss`) that GNU time prints as
"Maximum resident set size".  In addition the resident set size of the whole process group is
polled from /proc while the command runs; when it exceeds `--rss-kill-kb` the group is killed
(the machine is shared, and `ulimit -v` alone cannot be set tightly: `lean` reserves about 6.6 GB
of address space before it has allocated anything, see README.md).

usage: measure.py [--rss-kill-kb N] [--poll SECONDS] -- command [args...]
All report lines go to stderr and start with "MEASURE ".
"""
import os
import signal
import sys
import time


def group_rss_kb(pgid):
    """Sum of VmRSS (kB) over all processes whose process group or session is `pgid`."""
    total = 0
    for name in os.listdir('/proc'):
        if not name.isdigit():
            continue
        try:
            with open('/proc/%s/stat' % name) as fh:
                stat = fh.read()
            # fields after the command name (which may contain spaces): state ppid pgrp session ...
            rest = stat[stat.rindex(')') + 2:].split()
            if int(rest[2]) != pgid and int(rest[3]) != pgid:
                continue
            with open('/proc/%s/status' % name) as fh:
                for line in fh:
                    if line.startswith('VmRSS:'):
                        total += int(line.split()[1])
                        break
        except (OSError, ValueError, IndexError):
            continue
    return total


def kill_session(pid):
    for name in os.listdir('/proc'):
        if not name.isdigit():
            continue
        try:
            with open('/proc/%s/stat' % name) as fh:
                stat = fh.read()
            rest = stat[stat.rindex(')') + 2:].split()
            if int(rest[3]) == pid or int(rest[2]) == pid:
                os.kill(int(name), signal.SIGKILL)
        except (OSError, ValueError, IndexError):
            continue


def main(argv):
    rss_kill_kb = None
    poll = 0.05
    args = argv[1:]
    while args and args[0] != '--':
        if args[0] == '--rss-kill-kb':
            rss_kill_kb = int(args[1])
            args = args[2:]
        elif args[0] == '--poll':
            poll = float(args[1])
            args = args[2:]
        else:
            sys.stderr.write(__doc__)
            return 2
    cmd = args[1:]
    if not cmd:
        sys.stderr.write(__doc__)
        return 2

    t0 = time.monotonic()
    pid = os.fork()
    if pid == 0:
        os.setsid()                       # own session: everything it starts can be found and killed
        try:
            os.execvp(cmd[0], cmd)
        except OSError as exc:
            sys.stderr.write('MEASURE exec failed: %s\n' % exc)
            os._exit(127)

    killed_for_rss = False
    polled_peak_kb = 0
    while True:
        wpid, status, ru = os.wait4(pid, os.WNOHANG)
        if wpid == pid:
            break
        rss = group_rss_kb(pid)
        polled_peak_kb = max(polled_peak_kb, rss)
        if rss_kill_kb is not None and rss > rss_kill_kb and not killed_for_rss:
            killed_for_rss = True
            kill_session(pid)
        time.sleep(poll)
    wall = time.monotonic() - t0

    if os.WIFEXITED(status):
        code = os.WEXITSTATUS(status)
        how = 'exit status %d' % code
    else:
        code = 128 + os.WTERMSIG(status)
        how = 'killed by signal %d' % os.WTERMSIG(status)
    err = sys.stderr
    err.write('MEASURE command: %s\n' % ' '.join(cmd))
    err.write('MEASURE wall_seconds: %.2f\n' % wall)
    err.write('MEASURE user_seconds: %.2f\n' % ru.ru_utime)
    err.write('MEASURE sys_seconds: %.2f\n' % ru.ru_stime)
    err.write('MEASURE max_rss_kb: %d\n' % ru.ru_maxrss)
    err.write('MEASURE polled_peak_rss_kb: %d\n' % polled_peak_kb)
    err.write('MEASURE rss_watchdog_killed: %s\n' % ('yes' if killed_for_rss else 'no'))
    err.write('MEASURE result: %s\n' % how)
    return code


if __name__ == '__main__':
    sys.exit(main(sys.argv))
