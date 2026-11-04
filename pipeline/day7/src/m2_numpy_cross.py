# The same with NumPy, plus the triangle normal we will need for lighting
import numpy as np

a = np.array([1, -7, 1])
b = np.array([5, 2, 4])
c = np.cross(a, b)
print("np.cross(a, b) =", c, "  np.cross(b, a) =", np.cross(b, a))
print("c . a =", np.dot(c, a), "  c . b =", np.dot(c, b))

d = np.array([1, 2, 3])
print("parallel: [1, 2, 3] x [2, 4, 6] =", np.cross(d, 2 * d))

p0 = np.array([0, 0, 0])
p1 = np.array([2, 0, 0])
p2 = np.array([0, 3, 0])
n = np.cross(p1 - p0, p2 - p0)
print("triangle normal =", n, "  length =", np.linalg.norm(n), "  unit =", n / np.linalg.norm(n))
