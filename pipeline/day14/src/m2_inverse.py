import numpy as np

A = np.array([[2.0, 1.0], [0.0, 1.0]])
a, b, c, d = A[0, 0], A[0, 1], A[1, 0], A[1, 1]
det = a * d - b * c
inverse = np.array([[d, -b], [-c, a]]) / det + 0.0
print("det(A) = ad - bc =", det)
print("inverse by hand =", inverse.tolist())
print("np.linalg.inv(A) =", np.linalg.inv(A).tolist())
print("A @ inverse =", (A @ inverse).tolist())

x = np.array([1.0, 2.0])
y = A @ x
print("A @ (1, 2) =", y, " inverse @ that =", inverse @ y)

target = np.array([5.0, 3.0])
solution = inverse @ target
print("solve A x = (5, 3): x =", solution, " check A @ x =", A @ solution)
print("np.linalg.solve gives", np.linalg.solve(A, target))

B = np.array([[1.0, 2.0], [2.0, 4.0]])
print("det(B) =", np.linalg.det(B))
try:
    np.linalg.inv(B)
except np.linalg.LinAlgError as err:
    print("inv(B):", err)
print("B @ (2, 0) =", B @ np.array([2.0, 0.0]), " B @ (0, 1) =", B @ np.array([0.0, 1.0]), " -> two inputs, one output: no way back")
