import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

square = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=float)
A = np.array([[2.0, 1.0], [0.0, 1.0]])
image = (A @ square.T).T
print("corners of the unit square:", square.tolist())
print("image under A:", image.tolist())


def area(poly):
    x, y = poly[:, 0], poly[:, 1]
    return 0.5 * abs(np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y))


print("area before =", area(square), " area after =", area(image), " det(A) =", round(np.linalg.det(A), 6))

B = np.array([[1.0, 2.0], [2.0, 4.0]])
flat = (B @ square.T).T
print("B =", B.tolist(), " image:", flat.tolist())
print("area after B =", area(flat), " det(B) =", round(np.linalg.det(B), 6), " -> the square became a line")

fig, axes = plt.subplots(1, 2, figsize=(8, 3.6))
for ax, (name, img) in zip(axes, [("A (det 2)", image), ("B (det 0)", flat)]):
    ax.fill(square[:, 0], square[:, 1], color="#9ca3af", alpha=0.4)
    ax.fill(img[:, 0], img[:, 1], color="#c2410c", alpha=0.5)
    ax.plot(np.append(img[:, 0], img[0, 0]), np.append(img[:, 1], img[0, 1]), color="#c2410c", lw=2)
    ax.set_title(name)
    ax.set_aspect("equal")
    ax.set_xlim(-0.5, 3.5)
    ax.set_ylim(-0.5, 6.5)
    ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("image_area.png", dpi=110)
print("saved image_area.png")
