import numpy as np

I2 = np.identity(2)
I3 = np.identity(3)
print("I2 =")
print(I2)
x = np.array([7.0, -2.0, 5.0])
print("I3 @ x =", I3 @ x, " (the same x)")

e1 = np.array([1.0, 0.0])
e2 = np.array([0.0, 1.0])
print("3 * e1 + 5 * e2 =", 3 * e1 + 5 * e2)


def T(v):
    x1, x2 = v
    return np.array([x1 + 3 * x2, 5 * x2 - x1, 4 * x1 + x2])


print("T(e1) =", T(e1))
print("T(e2) =", T(e2))

A = np.column_stack([T(e1), T(e2)])
print("A = [T(e1) | T(e2)] =")
print(A)
print("A.shape =", A.shape, " (3 rows = output R3, 2 columns = input R2)")

for v in [np.array([1.0, 1.0]), np.array([2.0, -1.0]), np.array([0.0, 0.0])]:
    print("T", v, "=", T(v), "   A @", v, "=", A @ v)
