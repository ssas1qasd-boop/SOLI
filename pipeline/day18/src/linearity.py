import numpy as np

A = np.array([[1, 2, 0], [0, 1, -1]])
B = np.array([[1, 0], [0, 1], [1, 1], [2, -1]])


def S(x):
    return A @ x


def T(y):
    return B @ y


def TS(x):
    return T(S(x))


x = np.array([1, 2, 3])
y = np.array([-2, 0, 5])
c = 4
print("(T o S)(x + y)      =", TS(x + y))
print("(T o S)(x) + (T o S)(y) =", TS(x) + TS(y))
print("(T o S)(c x)        =", TS(c * x))
print("c (T o S)(x)        =", c * TS(x))


def move(p):
    return p + np.array([2, 0, 0])


print("move(x + y) =", move(x + y), " move(x) + move(y) =", move(x) + move(y))
print("move(0) =", move(np.zeros(3, dtype=int)), "-> not linear: the origin moved")

M = np.array([[1, 0, 0, 2], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
xh = np.append(x, 1)
print("4x4 with w = 1:", M @ xh, " the same move, now a matrix product")
