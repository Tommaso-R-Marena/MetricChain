#!/usr/bin/env python3
"""R1: what does "the capacity-achieving input of an asymmetric channel leans against the channel's bias"
(parenthesis in Lemma 11.89) mean, and is it true?  Channel in Ising form: X | B=b ~ spin with field h2 + J b.
For h2 > 0 the channel is biased towards X = +1.  We maximise I over the input law w = P(B=+1) and report
 (i)  the joint-law field h1* of the optimal input (the authors' proof, step 5, claims -h2 < h1* < 0),
 (ii) the sign of E[B] at the optimum (input marginal),
 (iii) the sign of E[X] at the optimum (output marginal)."""
import mpmath as mp
mp.mp.dps = 40

def opt_input(J, h2):
    a, b = mp.tanh(h2 + J), mp.tanh(h2 - J)           # E[X|B=+1], E[X|B=-1]
    Hb = lambda m: -((1+m)/2)*mp.log((1+m)/2) - ((1-m)/2)*mp.log((1-m)/2)
    I = lambda w: Hb(w*a + (1-w)*b) - w*Hb(a) - (1-w)*Hb(b)
    dI = lambda w: mp.diff(I, w)
    w = mp.findroot(dI, mp.mpf('0.5'))
    # joint field h1: P_B(+)/P_B(-) = e^{2 h1} cosh(h2+J)/cosh(h2-J)
    h1 = (mp.log(w/(1-w)) - mp.log(mp.cosh(h2+J)/mp.cosh(h2-J)))/2
    return w, h1, 2*w-1, w*a+(1-w)*b, I(w)

print(f"{'J':>5} {'h2':>6} {'w*=P(B=+1)':>12} {'h1*':>10} {'E[B]':>10} {'E[X]':>10} {'C':>10}  -h2<h1*<0  sign E[B]")
viol = 0
import itertools
for J, h2 in itertools.product((0.1, 0.5, 1.0, 2.0, 4.0), (0.05, 0.3, 1.0, 2.0, 4.0, 8.0)):
    w, h1, EB, EX, C = opt_input(mp.mpf(J), mp.mpf(h2))
    ok = (-h2 < h1 < 0)
    viol += (not ok)
    print(f"{J:5.2f} {h2:6.2f} {mp.nstr(w,8):>12} {mp.nstr(h1,6):>10} {mp.nstr(EB,6):>10} {mp.nstr(EX,6):>10} {mp.nstr(C,6):>10}  {str(bool(ok)):>9}  {'+' if EB>0 else '-'}")
print("violations of -h2 < h1* < 0:", viol)
