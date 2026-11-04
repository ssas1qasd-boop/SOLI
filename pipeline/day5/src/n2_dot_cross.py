import numpy as np

a = np.array([1, -7, 1])
b = np.array([5, 2, 4])
print("a =", a, "  b =", b)

d = np.dot(a, b)
print("np.dot(a, b) =", d)
print("by hand      =", a[0] * b[0] + a[1] * b[1] + a[2] * b[2])
print("sum(a * b)   =", np.sum(a * b))

c = np.cross(a, b)
print("np.cross(a, b) =", c)
print("check: c . a =", np.dot(c, a), "  c . b =", np.dot(c, b))
print("np.cross(b, a) =", np.cross(b, a))

u = np.array([3.0, 4.0])
v = np.array([4.0, 3.0])
length = np.linalg.norm(u)
cos_angle = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
angle = np.degrees(np.arccos(cos_angle))
print("|u| =", length, "  angle(u, v) =", round(angle, 2), "degrees")

x = np.array([1, 0, 0])
y = np.array([0, 1, 0])
print("x cross y =", np.cross(x, y), "  y cross x =", np.cross(y, x))

P = np.array([[1, 0, 0], [1, -7, 1], [1, 2, 3]])
Q = np.array([[0, 1, 0], [5, 2, 4], [4, 5, 6]])
print("3 cross products at once:")
print(np.cross(P, Q))
print("3 dot products at once:", np.sum(P * Q, axis=1))
