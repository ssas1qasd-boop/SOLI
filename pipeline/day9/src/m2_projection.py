import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

P = np.array([[0.9, 0.45, 0.0],
              [0.0, 0.35, 0.9]])
print("P has shape", P.shape, "-> takes R3, gives R2")

cube = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
                 [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]], dtype=float)
centered = cube - 0.5
screen = (P @ centered.T).T
print("corner 5 (1, 0, 1) lands on", screen[5].round(3))

v = centered[5]
by_hand = (v[0] * 0.9 + v[1] * 0.45, v[2] * 0.9 + v[1] * 0.35)
print("yesterday's formula gives", np.round(by_hand, 3))

a, b = centered[1], centered[3]
print("T(a + b) =", (P @ (a + b)).round(3), "  T(a) + T(b) =", (P @ a + P @ b).round(3))

edges = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
fig, ax = plt.subplots(figsize=(4, 3.2))
for i, j in edges:
    ax.plot([screen[i, 0], screen[j, 0]], [screen[i, 1], screen[j, 1]], color="#475569")
ax.scatter(screen[:, 0], screen[:, 1], color="#2563eb", zorder=3)
for k, (x, y) in enumerate(screen):
    ax.annotate(str(k), (x, y), textcoords="offset points", xytext=(5, 5))
ax.set_aspect("equal")
ax.set_title("cube after P (R3 -> R2)")
fig.tight_layout()
fig.savefig("projection.png", dpi=110)
print("saved projection.png")
