import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

M = np.array([[1, 3],
              [-2, 0]])
v = np.array([-1, 2])
print("M @ v =", M @ v)
print("columns of M:", M[:, 0], M[:, 1])

points = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
print("unit square corners after M:")
print((M @ points.T).T)

shear = np.array([[1, 1],
                  [0, 1]])
rotate = np.array([[0, -1],
                   [1, 0]])
print("shear then rotate (one matrix):")
print(rotate @ shear)


def draw(ax, A, title):
    for k in range(-3, 4):
        line = np.array([[k, t] for t in np.linspace(-3, 3, 2)])
        ax.plot(*(A @ line.T), color="#9ca3af", lw=0.8)
        line = np.array([[t, k] for t in np.linspace(-3, 3, 2)])
        ax.plot(*(A @ line.T), color="#9ca3af", lw=0.8)
    ax.arrow(0, 0, *A[:, 0], color="#16a34a", width=0.06, length_includes_head=True)
    ax.arrow(0, 0, *A[:, 1], color="#dc2626", width=0.06, length_includes_head=True)
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.set_aspect("equal")
    ax.set_title(title)


fig, axes = plt.subplots(1, 4, figsize=(12, 3.2))
draw(axes[0], np.eye(2), "before")
draw(axes[1], rotate, "rotate 90")
draw(axes[2], shear, "shear")
draw(axes[3], M, "M = [[1, 3], [-2, 0]]")
fig.tight_layout()
fig.savefig("grids.png", dpi=110)
print("saved grids.png")
