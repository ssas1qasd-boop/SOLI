import numpy as np

A = np.array([[1, -1, 2], [0, -2, 1]])
B = np.array([[1, 0, 1, 1], [2, 0, 1, -1], [3, 1, 0, 2]])
print("A is", A.shape, " B is", B.shape, " -> A @ B is", (A.shape[0], B.shape[1]))

columns = []
for k in range(B.shape[1]):
    b_k = B[:, k]
    columns.append(A @ b_k)
    print("A @ b" + str(k + 1) + " =", A @ b_k)
AB = np.column_stack(columns)
print("AB =")
print(AB)
print("same as A @ B:", np.array_equal(AB, A @ B))

try:
    B @ A
except ValueError as err:
    print("B @ A:", str(err).split(" (")[0])

x = np.array([1, 0, 2, -1])
print("T then S: A @ (B @ x) =", A @ (B @ x), " (AB) @ x =", AB @ x)
print("x lives in R4, B @ x in R3, A @ (B @ x) in R2")
