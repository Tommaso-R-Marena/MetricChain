"""
P7 item 5, an attempt: is the acceptance of a certificate also provable INSIDE Lean's kernel?

Takes lean/P7_<label>.lean (written by p7_07_lean.py), replaces its `#eval` lines by
    theorem accepted : verify cert inst dom 0 = true := by decide +kernel
    theorem lower_bound (x : Config n k) (hx : InBox dom x) : 0 ≤ inst.energy x :=
      verify_sound cert inst dom 0 accepted x hx                       -- THEIR soundness theorem
    theorem attained : inst.energy ref = 0 := by decide +kernel
    #print axioms lower_bound
writes lean/P7K_<label>.lean and runs `lake env lean` on it with a time limit (no `lake build`).
A time-out or an error is reported as such: it is a statement about kernel evaluation of this encoding
(arrays of integers), not about the certificate, which `#eval` accepts.

usage: python3 -B p7_09_kernel.py LABEL [TIMEOUT_SECONDS] > logs/p7_09_kernel_LABEL.log   (last line "DONE p7_09_kernel")
"""
import sys, os, re, time, subprocess
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
lab = sys.argv[1]
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 900
src = open(os.path.join(HERE, "lean", f"P7_{lab}.lean")).read()
m = re.search(r"def cert : Cert (\d+) (\d+)", src)
n, k = m.group(1), m.group(2)
head = src[:src.index("#eval verify cert inst dom 0")]
head = head.replace("Nothing in this file is a theorem.", "This copy asks Lean's KERNEL to evaluate `verify` (`decide +kernel`).")
tail = f"""theorem accepted : verify cert inst dom 0 = true := by decide +kernel

/-- the theory division's Master Soundness Theorem applied to the accepted certificate -/
theorem lower_bound (x : Config {n} {k}) (hx : InBox dom x) : 0 ≤ inst.energy x :=
  verify_sound cert inst dom 0 accepted x hx

theorem attained : inst.energy ref = 0 := by decide +kernel

#print axioms lower_bound
#print axioms attained

end P7.{lab}
"""
fname = os.path.join(HERE, "lean", f"P7K_{lab}.lean")
open(fname, "w").write(head + tail)
print(f"p7_09_kernel  started {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
print(f"wrote lean/P7K_{lab}.lean; running `lake env lean` with a limit of {limit} s", flush=True)
env = dict(os.environ)
env["PATH"] = os.path.expanduser("~/.lean/lean-4.31.0-linux/bin") + ":" + env["PATH"]
t0 = time.time()
# WARNING.  The one logged run of this script (05:25 UTC, logs/p7_09_kernel_cert_L16_P2_tau0_60_ff99SB.log) was made
# with a plain subprocess call and NO memory limit: Lean's kernel grew to 11.9 GB of anonymous memory in 78 s, the
# shared memory cgroup was exhausted and the out-of-memory killer killed it AND a process of another job (NOTES.md).
# The launch below was changed afterwards (address space 16 GB, anonymous memory capped at 1.5 GB); with these
# limits the attempt can only fail faster.  It has not been re-run and should not be.
import run_capped
r_ = run_capped.run(["lake", "env", "lean", fname], cap_mb=1500, timeout_s=limit, vlimit_mb=16000, cwd=ROOT, env=env)
print(f"exit {r_['returncode']} after {r_['seconds']:.1f} s")
print("--- stdout ---"); print(r_["stdout"][-6000:])
if r_["stderr"].strip():
    print("--- stderr ---"); print(r_["stderr"][-3000:])
print(run_capped.summary(r_, 1500, 16000))
print("RESULT:", "kernel-checked" if r_["returncode"] == 0 and "error" not in r_["stdout"] else "NOT kernel-checked (see output)")
print("DONE p7_09_kernel")
