import numpy as np

A = np.array([[1, -7, 5], [0, 3, -10]])
B = np.array([[5, 0, 3], [11, -1, 7]])
print("A + B =")
print(A + B)
print("B + A == A + B:", np.array_equal(B + A, A + B))

C = np.array([[0, 1], [3, 2]])
D = np.array([[-1, 3], [0, 5]])
print("C - D =")
print(C - D)
print("C + (-1) * D =")
print(C + (-1) * D)
print("D - C =")
print(D - C)


def add(X, Y):
    if X.shape != Y.shape:
        return "undefined: " + str(X.shape) + " + " + str(Y.shape)
    out = np.zeros(X.shape, dtype=int)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            out[i, j] = X[i, j] + Y[i, j]
    return out


print("add(A, B) element by element =")
print(add(A, B))
E = np.array([[1, 0], [3, 5], [0, 1]])
F = np.array([[5, 7], [-1, 0]])
print("add(E, F):", add(E, F))
try:
    print(E + F)
except ValueError as err:
    print("numpy E + F:", err)
