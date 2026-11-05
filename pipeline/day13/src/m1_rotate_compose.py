import numpy as np


def rotation(degrees):
    t = np.radians(degrees)
    return np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])


x = np.array([1.0, 0.0])
print("rotate (1, 0) by 90:", np.round(rotation(90) @ x, 6))
print("rotate (1, 0) by 30:", np.round(rotation(30) @ x, 6))
print("rotation(30) =")
print(np.round(rotation(30), 6))

print("rotation(30) @ rotation(60) = rotation(90)?", np.allclose(rotation(30) @ rotation(60), rotation(90)))

S = np.array([[2.0, 0.0], [0.0, 1.0]])
R = rotation(90)
p = np.array([1.0, 1.0])
print("first scale, then rotate: R @ (S @ p) =", np.round(R @ (S @ p), 6))
print("first rotate, then scale: S @ (R @ p) =", np.round(S @ (R @ p), 6))
print("R @ S =")
print(np.round(R @ S, 6))
print("S @ R =")
print(np.round(S @ R, 6))

back = rotation(-30) @ rotation(30) @ p
print("rotation(-30) undoes rotation(30):", np.round(back, 6))
print("rotation(30) transposed = rotation(-30)?", np.allclose(rotation(30).T, rotation(-30)))
print("length before =", np.linalg.norm(p), " after rotation(30) =", np.round(np.linalg.norm(rotation(30) @ p), 6))
