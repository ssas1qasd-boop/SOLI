import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

house = np.array([[0, 0], [2, 0], [2, 2], [1, 3], [0, 2], [0, 0]], dtype=float)
move = np.array([[3, 1]] * 6, dtype=float)
moved = house + move
print("house:", house.shape, " move:", move.shape)
print("corner 3 (the roof):", house[3], "->", moved[3])
print("moved - move == house:", np.array_equal(moved - move, house))
print("moved - house, every row:", np.unique(moved - house, axis=0).tolist())

squash = np.zeros((6, 2))
squash[3] = [0, -1.5]
flat = house + squash
print("squash only changes row 3: roof", house[3], "->", flat[3])

frames = [house + k * move / 3 for k in range(4)]
for k, P in enumerate(frames):
    print("frame", k, "corner 0 =", P[0])

fig, ax = plt.subplots(figsize=(6, 4))
for k, P in enumerate(frames):
    ax.plot(P[:, 0], P[:, 1], color="#c2410c", alpha=0.3 + 0.2 * k, lw=2)
ax.plot(flat[:, 0], flat[:, 1], color="#2563eb", lw=2, ls="--")
ax.set_aspect("equal")
ax.grid(alpha=0.3)
plt.savefig("moves.png", dpi=110)
print("saved moves.png")
