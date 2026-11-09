import numpy as np

A = np.array([[1, 0], [0, 1]])
B = np.array([[4, 1], [2, 2]])
print("np.matmul(A, B) =", np.matmul(A, B).tolist(), " A @ B =", (A @ B).tolist())

v = np.array([1, 2])
print("A @ v (v is 1-D, treated as a column) =", A @ v, " shape", (A @ v).shape)
print("v @ B (v treated as a row) =", v @ B)
print("v @ v (1-D with 1-D = dot product) =", v @ v)

stack = np.arange(2 * 2 * 4).reshape((2, 2, 4))
other = np.arange(2 * 4 * 2).reshape((2, 4, 2))
print("stack of matrices: (2, 2, 4) @ (2, 4, 2) ->", np.matmul(stack, other).shape)
print("broadcast: (2, 2, 4) @ (4, 2) ->", np.matmul(stack, other[0]).shape)

try:
    np.matmul(A, 3)
except ValueError as err:
    print("np.matmul(A, 3):", str(err).split(",")[0])
print("A * 3 (multiply every cell) =", (A * 3).tolist())

a = np.ones((9, 5, 7, 4))
c = np.ones((9, 5, 4, 3))
print("np.dot shape:", np.dot(a, c).shape, " np.matmul shape:", np.matmul(a, c).shape)
