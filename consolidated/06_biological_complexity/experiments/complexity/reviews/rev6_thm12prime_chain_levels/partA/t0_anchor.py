# anchor: the network N* of section 6 of the note, its printed NANUQ matrix and Theorem 9(a),(b)
import numpy as np
from rn import Net, alphas, kalmanson_search, brute_kalmanson, is_kalmanson
ch = {"rho": ["w1", "w3"], "w1": ["a1", "w2"], "w2": ["a2", "p1"], "p1": ["b", "h1"],
      "w3": ["d", "q1"], "q1": ["h1", "q2"], "q2": ["h2", "c"], "h1": ["u"], "u": ["x", "h2"], "h2": ["y"]}
N = Net(ch)
print("valid", N.valid(), "level", N.level(), "hyb", N.hyb)
L = ["a1", "a2", "b", "x", "y", "c", "d"]
D6 = N.nanuq6(L)
assert np.all(D6 % 6 == 0)
D = D6 // 6
print(D)
printed = np.array([[0,21,23,26,26,23,21],[21,0,17,24,26,27,25],[23,17,0,20,24,29,27],[26,24,20,0,20,24,26],
                    [26,26,24,20,0,20,24],[23,27,29,24,20,0,17],[21,25,27,26,24,17,0]])
print("matches the matrix printed in the note:", np.array_equal(D, printed))
po = N.planar_order()
print("planar order from embedding:", po)
al = alphas(D, list(range(7)))
print("negative alphas for order a1,a2,b,x,y,c,d:", {k: v for k, v in al.items() if v < 0})
print("brute force over 360 orders:", len(brute_kalmanson(D)), " backtracking:", kalmanson_search(D))
