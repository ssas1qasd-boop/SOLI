import numpy as np

A = np.array([[1, 2, 0],
              [0, 1, -1]])
B = np.array([[1, 0],
              [0, 1],
              [1, 1],
              [2, -1]])
print("S(x) = A x : A is", A.shape, "-> from R3 to R2")
print("T(y) = B y : B is", B.shape, "-> from R2 to R4")

x = np.array([1, 2, 3])
s = A @ x
t = B @ s
print("x =", x, " S(x) =", s, " T(S(x)) =", t)

C = B @ A
print("C = B @ A is", C.shape, "-> from R3 to R4")
print(C)
print("C @ x =", C @ x, " same as T(S(x)):", np.array_equal(C @ x, t))

try:
    A @ B
except ValueError as err:
    print("A @ B:", str(err).split(" (")[0])
