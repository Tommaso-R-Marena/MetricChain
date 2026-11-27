#!/usr/bin/env python3
"""R24, item 6: the tables of addendum items 86 and 90 (= the tables of SCI-MSG-0031, SCI-MSG-0032, SCI-RES-0032 section 5) and
the table of SCI-RES-0032 section 2, typed by the referee from the texts, against the committed logs (parsed).
A typed number agrees if it equals the log's number rounded to the typed number of decimals (half a unit of the last place).
Control: one typed number per table changed in its last digit must be reported.
(The table of item 88 is checked in r24_item3.py.)
Run: python3 -B r24_numbers.py > r24_numbers.log
"""
import os, re, resource
HERE = os.path.dirname(os.path.abspath(__file__)); PI = os.path.normpath(os.path.join(HERE, "..", "pi_inference")); EC = os.path.normpath(os.path.join(HERE, "..", "ensemble_checks"))


def agree(typed, logv):
    s = str(typed); dec = len(s.split(".")[1]) if "." in s else 0
    return abs(float(typed) - logv) <= 0.5 * 10 ** (-dec) * (1 + 1e-9) + 1e-12


def fl(pat, txt, grp=1):
    m = re.search(pat, txt, re.S); assert m, pat; return float(m.group(grp))


def table86():
    typed = {"K12_m4_w4": ("15.324", "15.284", "15.497", "1.011", 10, "6.21", "96.2", "1.07", "15.298", 3559, 1138),
             "K12_m4_w7": ("18.805", "18.847", "19.093", "1.015", 11, "5.36", "102.3", "1.55", "18.871", 3614, 1508),
             "K12_m3_w7": ("1.3176", "1.3349", "1.3556", "1.029", 10, "64.0", "86.8", "2.43", "1.3296", 3907, 1746),
             "LKSEc12_m3_w7": ("0.19835", "0.19937", "0.20486", "1.033", 12, "647.6", "132.7", "4.22", "0.20046", 3972, 3401)}
    out = []
    for tag, tp in typed.items():
        t = open(os.path.join(PI, f"floor_ground_state_{tag}.log")).read(); done = "ALL DONE" in t.strip().split("\n")[-1]
        logv = (fl(r"measured lambda_c there ([0-9.]+)", t), fl(r"\(c\) lambda_kink in \[([0-9.]+), ([0-9.]+)\]", t, 1), fl(r"least ([0-9.]+) against", t), fl(r"lambda_gs / measured lambda_c = ([0-9.]+)", t),
                fl(r"minimiser with (\d+) of", t), fl(r"penalty b\* = ([0-9.]+) kT", t), fl(r"cost c\* = ([0-9.]+);", t), fl(r"\(lambda_gs - lambda_c\) b\* = ([0-9.]+) nats", t),
                fl(r"equal weights predicted at lambda_gs - \(S_d - reference growth\) / b\* = ([0-9.]+)", t), fl(r"ratio c/b of (\d+) exact samples", t), fl(r"below 1.05 c\*/b\*: (\d+)", t))
        hi_k = fl(r"\(c\) lambda_kink in \[([0-9.]+), ([0-9.]+)\]", t, 2)
        for q, (a, b) in enumerate(zip(tp, logv)):
            ok = agree(a, b) or (q == 1 and agree(a, hi_k))
            out.append((f"86 {tag} col {q}", a, b, ok, done))
    return out


def table90():
    typed = {"K5_m4_w2_enum": (6, "0.19", "0.026", "0.025", "0.140", "0.104", "0.441", "0.166", "0.129", "0.275"), "K5_m4_w3_enum": (2, "0.06", "0.028", "0.028", "0.066", "0.019", "0.224", "0.094", "0.047", "0.130"),
             "K5_m5_w3_enum": (2, "0.06", "0.241", "0.241", "0.525", "0.148", "0.779", "0.766", "0.389", "0.013"), "LKSEc5_m4_w2_enum": (6, "0.39", "0.001", "0.001", "0.022", "0.021", "0.475", "0.022", "0.021", "0.452"),
             "K12_m4_w4": (56, "1.07", "0.169", "0.168", "0.475", "0.446", "0.708", "0.644", "0.614", "0.064"), "K12_m4_w7": (20, "0.60", "0.038", "0.038", "0.208", "0.205", "0.346", "0.246", "0.243", "0.100")}
    out = []
    for tag, tp in typed.items():
        t = open(os.path.join(PI, f"group_coupling_{tag}.log")).read(); done = "ALL DONE" in t.strip().split("\n")[-1]
        six = t[t.index("(6) the loss"):]
        logv = (fl(r"\(0\) (\d+) groups", t), fl(r"sum_g P\(S\+_g > 0\) = ([0-9.]+)\*\*", t), fl(r"the exact joint law of the groups: ln <prod \(1 \+ y_g\)> \| [^|]+\| \*\*\+([0-9.]+)\*\*", t),
                fl(r"\+ pair terms sum_\(g<h\) <y_g y_h> \(joint laws of pairs of groups\) \| [^|]+\| \*\*\+([0-9.]+)\*\*", t), fl(r"the exact joint law of all groups under the ceiling, same route \| [0-9.]+ \| \*\*([0-9.]+)\*\*", t),
                fl(r"\+ pair terms \(joint laws of pairs of groups under the ceiling\) \| [0-9.]+ \| \*\*([0-9.]+)\*\*", t), fl(r"= \*\*([0-9.]+)\*\*", six), fl(r"same inequalities: [0-9.]+ \+ [0-9.]+ = \*\*([0-9.]+)\*\*", six),
                fl(r"pair terms alone: [0-9.]+ \+ [0-9.]+ = ([0-9.]+)\*\*", six), fl(r"the rest, ([0-9.]+)", six))
        for q, (a, b) in enumerate(zip(tp, logv)): out.append((f"90 {tag} col {q}", a, b, agree(a, b), done))
    return out


def table_res32():
    typed = {"K5": {"symmetric": ("17.9", "0.020", "0.764", "0.536", "0.08", "0.07"), "one-sided": ("17.9", "0.020", "0.652", "0.428", "0.39", "0.38")},
             "LKSEc5": {"symmetric": ("22.8", "0.038", "0.978", "0.637", "0.34", "0.22"), "one-sided": ("22.8", "0.038", "0.895", "0.637", "0.41", "0.22")}}
    out = []
    for tag, d in typed.items():
        t = open(os.path.join(EC, f"thermal_union_bound_{tag}.log")).read(); done = "ALL DONE" in t.strip().split("\n")[-1]; gm = fl(r"Gibbs mean of \|g\| ([0-9.]+)", t)
        for nm, tp in d.items():
            blk = t[t.index(f"--- {nm} envelope, centre"):]
            logv = (fl(r"largest delta_i\(s, t\) over all pairs ([0-9.]+)", blk), gm, fl(r"\*\*sum tau = ([0-9.]+)\*\*", blk), fl(r"\*\*TV\(mu, mu\*_a\) = ([0-9.]+)\*\*", blk),
                    fl(r"one-site ratio test certifies b >= \*\*([0-9.]+)\*\*", blk), fl(r"the caps of \(a\), any centre: b >= ([0-9.]+)", blk))
            for q, (a, b) in enumerate(zip(tp, logv)): out.append((f"RES-0032 s2 {tag} {nm} col {q}", a, b, agree(a, b), done))
    return out


def main():
    tot = 0; bad = []
    for name, rows in (("item 86 / SCI-MSG-0031", table86()), ("item 90 / SCI-MSG-0032 / SCI-RES-0032 s5", table90()), ("SCI-RES-0032 s2 / item 87 (d)", table_res32())):
        b = [r for r in rows if not r[3]]; undone = sorted({r[0].split(" col")[0] for r in rows if not r[4]})
        # control: change the last digit of the first typed number and compare again
        a0 = str(rows[0][1]); wrong = a0[:-1] + str((int(a0[-1]) + 3) % 10); ctrl = not agree(wrong, rows[0][2])
        print(f"{name}: {len(rows)} numbers typed from the texts against the logs: {len(b)} disagree {[(r[0], r[1], r[2]) for r in b] if b else ''}; logs that did not reach their last line: {undone if undone else 'none'}; "
              f"control (first number {a0} typed as {wrong}): reported: {ctrl} (must be True)")
        tot += len(rows); bad += b
    print(f"in all {tot} numbers, {len(bad)} disagreements")
    print(f"ALL DONE; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")


if __name__ == "__main__":
    main()
