import numpy as np


def rotate_x(degrees):
    t = np.radians(degrees)
    return np.array([[1, 0, 0], [0, np.cos(t), -np.sin(t)], [0, np.sin(t), np.cos(t)]])


p = np.array([2.0, 1.0, 0.0])
print("rotate (2, 1, 0) around x by 90:", np.round(rotate_x(90) @ p, 6))
print("x did not change, (y, z) turned: (1, 0) -> (0, 1)")

u = np.array([2.0, 1.0])
x = np.array([2.0, 3.0])
proj = (x @ u) / (u @ u) * u
print("x . u =", x @ u, " u . u =", u @ u)
print("projection of (2, 3) on the line through (2, 1):", proj)
print("x - projection =", x - proj, " (x - projection) . u =", round((x - proj) @ u, 6))

P = np.outer(u, u) / (u @ u)
print("P = u u^T / (u . u) =")
print(P)
print("P @ x =", P @ x)
print("P @ P = P?", np.allclose(P @ P, P))
print("P @ (-1, 2) =", P @ np.array([-1.0, 2.0]), " (a vector at 90 degrees to the line goes to 0)")
