import numpy as np


def T(x):
    x1, x2 = x
    return np.array([x1 + 3 * x2, 5 * x2 - x1, 4 * x1 + x2])


e1 = np.array([1, 0])
e2 = np.array([0, 1])
print("T(e1) =", T(e1), " T(e2) =", T(e2))

A = np.column_stack([T(e1), T(e2)])
print("A = [T(e1) T(e2)] =")
print(A)
print("A is", A.shape, "-> T goes from R2 to R3")

for x in ([2, 1], [-1, 4], [0, 0]):
    x = np.array(x)
    print("x =", x, " T(x) =", T(x), " A @ x =", A @ x)


def F(x):
    x1, x2 = x
    return np.array([x1 * x2, x1 + 1])


B = np.column_stack([F(e1), F(e2)])
x = np.array([2, 3])
print("F(x) =", F(x), " but [F(e1) F(e2)] @ x =", B @ x, "-> F is not linear, no matrix works")
