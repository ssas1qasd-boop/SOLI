import numpy as np

rotation = np.array([[0, -1], [1, 0]])
shear = np.array([[1, 1], [0, 1]])
i_hat = np.array([1, 0])
j_hat = np.array([0, 1])

print("rotation then shear, one vector at a time:")
print("  i-hat -> shear @ (rotation @ i-hat) =", shear @ (rotation @ i_hat))
print("  j-hat -> shear @ (rotation @ j-hat) =", shear @ (rotation @ j_hat))
composition = shear @ rotation
print("composition = shear @ rotation =")
print(composition)

M1 = np.array([[1, -2], [1, 0]])
M2 = np.array([[0, 2], [1, 0]])
first_column = M2 @ M1[:, 0]
second_column = M2 @ M1[:, 1]
print("M2 @ (first column of M1) =", first_column, " M2 @ (second column of M1) =", second_column)
by_columns = np.column_stack([first_column, second_column])
print("by columns:")
print(by_columns)
print("M2 @ M1 =")
print(M2 @ M1)

print("shear @ rotation:")
print(shear @ rotation)
print("rotation @ shear:")
print(rotation @ shear)
print("same? ", np.array_equal(shear @ rotation, rotation @ shear))

A = np.array([[2, 1], [0, 1]])
B = np.array([[1, 0], [3, 1]])
C = np.array([[0, 1], [-1, 0]])
print("(A @ B) @ C =", ((A @ B) @ C).tolist(), " A @ (B @ C) =", (A @ (B @ C)).tolist())
