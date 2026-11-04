import numpy as np

a = np.array([1, 2, 3])
b = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
print("a =", a)
print("b =", b.tolist())

print("ndim:", a.ndim, b.ndim)
print("shape:", a.shape, b.shape)
print("dtype:", a.dtype, b.dtype)
print("itemsize:", a.itemsize, "bytes, nbytes:", a.nbytes, "bytes")

print("b[1, 2] =", b[1, 2])
print("row 0 =", b[0, :])
print("column 1 =", b[:, 1])

print("a + 2 =", a + 2)
print("a * 2 =", a * 2)
print("a ** 2 =", a ** 2)

c = a
c[0] = 100
print("after c = a and c[0] = 100: a =", a)

a = np.array([1, 2, 3])
d = a.copy()
d[0] = 100
print("after d = a.copy() and d[0] = 100: a =", a, "d =", d)
