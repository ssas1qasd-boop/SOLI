import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

F = np.array([[0, 0], [0, 3], [2, 3], [2, 2.5], [0.5, 2.5], [0.5, 1.7], [1.5, 1.7], [1.5, 1.2], [0.5, 1.2], [0.5, 0], [0, 0]])


def matrix(Te1, Te2):
    return np.column_stack([Te1, Te2])


transforms = {
    "scale x2": matrix([2, 0], [0, 1]),
    "rotate 90": matrix([0, 1], [-1, 0]),
    "shear": matrix([1, 0], [1, 1]),
    "mirror": matrix([-1, 0], [0, 1]),
}

fig, axes = plt.subplots(1, 4, figsize=(12, 3.4))
for ax, (name, A) in zip(axes, transforms.items()):
    moved = (A @ F.T).T
    print(f"{name:9s} A = {A.tolist()}   corner (2, 3) -> {(A @ np.array([2, 3])).tolist()}")
    ax.plot(F[:, 0], F[:, 1], color="#9ca3af", lw=1.5)
    ax.plot(moved[:, 0], moved[:, 1], color="#c2410c", lw=2.5)
    ax.arrow(0, 0, A[0, 0], A[1, 0], color="#2563eb", width=0.05, length_includes_head=True)
    ax.arrow(0, 0, A[0, 1], A[1, 1], color="#0d9488", width=0.05, length_includes_head=True)
    ax.set_title(name)
    ax.set_aspect("equal")
    ax.set_xlim(-4, 5)
    ax.set_ylim(-2.5, 4)
    ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig("shapes.png", dpi=110)
print("saved shapes.png")
