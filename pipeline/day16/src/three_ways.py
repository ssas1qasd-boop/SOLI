import numpy as np

A = np.array([[1, -1, 2], [0, -2, 1]])
B = np.array([[1, 0, 1, 1], [2, 0, 1, -1], [3, 1, 0, 2]])
m, n = A.shape
n2, k = B.shape

rows_dot_columns = np.zeros((m, k), dtype=int)
for i in range(m):
    for j in range(k):
        rows_dot_columns[i, j] = A[i, :] @ B[:, j]
print("1. row i . column j:")
print(rows_dot_columns)

columns = np.column_stack([A @ B[:, j] for j in range(k)])
print("2. A times each column of B:")
print(columns)

outer_sum = np.zeros((m, k), dtype=int)
for p in range(n):
    outer_sum += np.outer(A[:, p], B[p, :])
print("3. sum of (column p of A) x (row p of B):")
print(outer_sum)

print("all equal to A @ B:", np.array_equal(rows_dot_columns, A @ B) and np.array_equal(columns, A @ B) and np.array_equal(outer_sum, A @ B))
print("multiplications:", m * k * n, "=", m, "x", k, "x", n)
