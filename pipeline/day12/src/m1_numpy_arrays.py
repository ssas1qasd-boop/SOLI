import numpy as np

a = np.array([1, 2, 3])
b = np.array([[9.0, 8.0, 7.0], [6.0, 5.0, 4.0]])
print("a.ndim =", a.ndim, " b.ndim =", b.ndim, " b.shape =", b.shape)
print("a.dtype =", a.dtype, " itemsize =", a.itemsize, " nbytes =", a.nbytes)
a16 = np.array([1, 2, 3], dtype="int16")
print("int16: itemsize =", a16.itemsize, " nbytes =", a16.nbytes)

m = np.array([[1, 2, 3, 4, 5, 6, 7], [8, 9, 10, 11, 12, 13, 14]])
print("m[1, 5] =", m[1, 5], " m[1, -2] =", m[1, -2])
print("m[0, :] =", m[0, :])
print("m[:, 2] =", m[:, 2])
print("m[0, 1:6:2] =", m[0, 1:6:2])
m[:, 2] = [1, 2]
print("after m[:, 2] = [1, 2]:")
print(m)

output = np.ones((5, 5))
z = np.zeros((3, 3))
z[1, 1] = 9
output[1:-1, 1:-1] = z
print("Keith's 5 x 5:")
print(output)

x = np.array([1, 2, 3])
y = x
y[0] = 100
print("y = x, then y[0] = 100 -> x =", x)
x = np.array([1, 2, 3])
y = x.copy()
y[0] = 100
print("y = x.copy(), then y[0] = 100 -> x =", x)
