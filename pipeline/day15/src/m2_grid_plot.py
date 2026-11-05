import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rotation = np.array([[0, -1], [1, 0]])
shear = np.array([[1, 1], [0, 1]])
orders = [("rotation then shear", shear @ rotation), ("shear then rotation", rotation @ shear)]

lines = []
for k in range(-3, 4):
    t = np.linspace(-3, 3, 2)
    lines.append(np.array([t, np.full(2, k)]))
    lines.append(np.array([np.full(2, k), t]))

fig, axes = plt.subplots(1, 2, figsize=(8, 4))
for ax, (name, M) in zip(axes, orders):
    for line in lines:
        moved = M @ line
        ax.plot(moved[0], moved[1], color="#93c5fd", lw=1)
    i_new, j_new = M[:, 0], M[:, 1]
    ax.arrow(0, 0, i_new[0], i_new[1], color="#16a34a", width=0.06, length_includes_head=True)
    ax.arrow(0, 0, j_new[0], j_new[1], color="#dc2626", width=0.06, length_includes_head=True)
    ax.set_title(name + "\n" + str(M.tolist()))
    ax.set_aspect("equal")
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    print(name, ": i-hat ->", i_new.tolist(), " j-hat ->", j_new.tolist())
plt.tight_layout()
plt.savefig("composition.png", dpi=110)
print("saved composition.png")
