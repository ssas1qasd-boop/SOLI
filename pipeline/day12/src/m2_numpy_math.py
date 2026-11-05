import numpy as np

a = np.array([1, 2, 3, 4])
print("a + 2 =", a + 2, " a * 2 =", a * 2, " a ** 2 =", a ** 2)
print("a + [1, 0, 1, 0] =", a + np.array([1, 0, 1, 0]))

ones = np.ones((2, 3))
twos = np.full((3, 2), 2)
print("matmul(ones 2x3, twos 3x2) =")
print(np.matmul(ones, twos))
print("ones * ones (element-wise) =")
print(ones * ones)
print("det(identity(3)) =", np.linalg.det(np.identity(3)))

stats = np.array([[1, 2, 3], [4, 5, 6]])
print("min =", np.min(stats), " max =", np.max(stats), " sum =", np.sum(stats))
print("min per row (axis=1) =", np.min(stats, axis=1), " max per column (axis=0) =", np.max(stats, axis=0))

before = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
print("reshape (4, 2) =")
print(before.reshape((4, 2)))
try:
    before.reshape((2, 3))
except ValueError as err:
    print("reshape (2, 3):", err)

v1 = np.array([1, 2, 3, 4])
v2 = np.array([5, 6, 7, 8])
print("vstack =")
print(np.vstack([v1, v2]))
print("hstack shape =", np.hstack((np.ones((2, 4)), np.zeros((2, 2)))).shape)

data = np.array([[12, 75, 40], [88, 3, 51]])
print("data > 50 =")
print(data > 50)
print("data[data > 50] =", data[data > 50])
print("any column > 50:", np.any(data > 50, axis=0), " all:", np.all(data > 50, axis=0))
