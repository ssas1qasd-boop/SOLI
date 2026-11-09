import numpy as np

A = np.array([[2, 1],
              [0, 1]])
triangle = np.array([[0, 0], [2, 0], [0, 1]])
image = triangle @ A.T
print("corners:", triangle.tolist(), "->", image.tolist())

p, q = triangle[1], triangle[2]
for t in (0.0, 0.25, 0.5, 1.0):
    on_edge = (1 - t) * p + t * q
    print("t =", t, ": A @ point on edge =", A @ on_edge, " same point between the new corners =", (1 - t) * (A @ p) + t * (A @ q))


def area(c):
    (x0, y0), (x1, y1), (x2, y2) = c
    return abs((x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)) / 2


print("area before =", area(triangle), " after =", area(image), " |det(A)| =", abs(round(np.linalg.det(A), 6)))
