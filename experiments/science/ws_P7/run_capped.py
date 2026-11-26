"""
Run a command with caps on memory (the machine is shared; written after the incident of 05:26 UTC, NOTES.md).

Two protections:
  * `ulimit -v` (RLIMIT_AS, option VLIMIT_MB): the address space of every process of the command is limited,
    so an allocation beyond it fails inside the process instead of exhausting the shared memory cgroup;
  * a poller: every 0.25 s the ANONYMOUS resident memory (RssAnon of /proc/<pid>/status, summed over the
    process group) is compared with CAP_MB; above it the whole group is killed.
Reported: peak anonymous resident memory, peak file-backed resident memory (memory-mapped files such as the
compiled Mathlib modules: page cache, reclaimable), largest VmPeak of a process.

usage: python3 -B run_capped.py CAP_ANON_MB TIMEOUT_S VLIMIT_MB -- command args ...     (VLIMIT_MB = 0: no ulimit -v)
       exit status: that of the command; 99 if killed for memory; 98 if timed out.
importable: run(cmd, cap_mb, timeout_s, vlimit_mb=0, cwd=None, env=None)
            -> dict(returncode, stdout, stderr, peak_anon_mb, peak_file_mb, vmpeak_mb, killed, seconds)
"""
import os, sys, time, signal, subprocess, threading, resource


def _group_mem(pgid):
    anon = filem = 0.0
    vmpeak = 0.0
    for d in os.listdir("/proc"):
        if not d.isdigit():
            continue
        try:
            with open(f"/proc/{d}/stat") as f:
                st = f.read()
            if int(st[st.rindex(")") + 2:].split()[2]) != pgid:
                continue
            with open(f"/proc/{d}/status") as f:
                for ln in f:
                    if ln.startswith("RssAnon:"):
                        anon += int(ln.split()[1]) / 1024.0
                    elif ln.startswith("RssFile:") or ln.startswith("RssShmem:"):
                        filem += int(ln.split()[1]) / 1024.0
                    elif ln.startswith("VmPeak:"):
                        vmpeak = max(vmpeak, int(ln.split()[1]) / 1024.0)
        except (OSError, ValueError, IndexError):
            continue
    return anon, filem, vmpeak


def run(cmd, cap_mb, timeout_s, vlimit_mb=0, cwd=None, env=None):
    t0 = time.time()

    def pre():
        os.setsid()
        if vlimit_mb:
            b = int(vlimit_mb * 1024 * 1024)
            resource.setrlimit(resource.RLIMIT_AS, (b, b))
    p = subprocess.Popen(cmd, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, preexec_fn=pre)
    peak_a = peak_f = peak_v = 0.0
    killed = None
    out = {}

    def reader():
        out["o"], out["e"] = p.communicate()
    th = threading.Thread(target=reader)
    th.start()
    while th.is_alive():
        a, f, v = _group_mem(p.pid)
        peak_a = max(peak_a, a); peak_f = max(peak_f, f); peak_v = max(peak_v, v)
        if a > cap_mb:
            killed = "memory"
        elif time.time() - t0 > timeout_s:
            killed = "timeout"
        if killed:
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            break
        time.sleep(0.25)
    th.join()
    return dict(returncode=(99 if killed == "memory" else 98 if killed == "timeout" else p.returncode), stdout=out.get("o", ""), stderr=out.get("e", ""),
                peak_anon_mb=peak_a, peak_file_mb=peak_f, vmpeak_mb=peak_v, killed=killed, seconds=time.time() - t0)


def summary(r, cap, vlimit):
    return (f"[run_capped] peak anonymous resident memory {r['peak_anon_mb']:.0f} MB (cap {cap:.0f} MB); peak file-backed resident memory {r['peak_file_mb']:.0f} MB; "
            f"largest VmPeak {r['vmpeak_mb']:.0f} MB (ulimit -v {('%.0f MB' % vlimit) if vlimit else 'not set'}); {r['seconds']:.1f} s; "
            + (f"KILLED: {r['killed']}" if r["killed"] else f"exit {r['returncode']}"))


if __name__ == "__main__":
    cap = float(sys.argv[1]); lim = float(sys.argv[2]); vl = float(sys.argv[3])
    cmd = sys.argv[sys.argv.index("--") + 1:]
    r = run(cmd, cap, lim, vl)
    sys.stdout.write(r["stdout"])
    sys.stderr.write(r["stderr"])
    print(summary(r, cap, vl))
    sys.exit(r["returncode"])
