# Review with NumPy: the same numbers in one line each, plus the dot product properties
import numpy as np

a = np.array([2, 5])
b = np.array([7, 1])
print("a . b =", np.dot(a, b), "  |a| =", np.linalg.norm(a))
print("|a| squared =", round(np.linalg.norm(a) ** 2, 6), "  a . a =", np.dot(a, a))

c = np.array([1, 2, 3])
d = np.array([-2, 0, 5])
e = np.array([4, -1, 2])
print("c . d =", np.dot(c, d), "  d . c =", np.dot(d, c))
print("c . (d + e) =", np.dot(c, d + e), "  c . d + c . e =", np.dot(c, d) + np.dot(c, e))
print("(3c) . d =", np.dot(3 * c, d), "  3 (c . d) =", 3 * np.dot(c, d))

u = np.array([3, 4])
print("|u| =", np.linalg.norm(u), "  unit vector =", u / np.linalg.norm(u), "  its length =", np.linalg.norm(u / np.linalg.norm(u)))
