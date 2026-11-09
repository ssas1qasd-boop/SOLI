import numpy as np

v = np.array([2.0, 1.0])
x = np.array([1.0, 3.0])

proj = (x @ v) / (v @ v) * v
print("Proj_L(x) = (x . v / v . v) v =", proj)

P = np.outer(v, v) / (v @ v)
print("P = v v^T / (v . v) =")
print(P)
print("P @ x =", P @ x)
print("P[:, 0] = Proj(e1) =", P[:, 0], " P[:, 1] = Proj(e2) =", P[:, 1])

print("P @ P == P:", np.allclose(P @ P, P), "(projecting twice changes nothing)")
rest = x - proj
print("x - Proj(x) =", rest, " dot with v =", round(rest @ v, 10), "(perpendicular)")
print("det P =", round(np.linalg.det(P), 10), "(the plane is flattened onto a line)")
