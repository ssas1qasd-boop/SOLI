import numpy as np


def reflect_y(x):
    return np.array([-x[0], x[1]])


def stretch_y(x):
    return np.array([x[0], 2 * x[1]])


e1, e2 = np.array([1, 0]), np.array([0, 1])
R = np.column_stack([reflect_y(e1), reflect_y(e2)])
S = np.column_stack([stretch_y(e1), stretch_y(e2)])
print("reflect across the y-axis R =", R.tolist())
print("stretch y by 2            S =", S.tolist())

C = S @ R
print("reflect first, then stretch: C = S @ R =", C.tolist())

triangle = np.array([[3, 2], [-3, 2], [3, -2]])
print("triangle corners:", triangle.tolist())
print("after C:         ", (triangle @ C.T).tolist())
print("det R =", round(np.linalg.det(R)), " det S =", round(np.linalg.det(S)), " det C =", round(np.linalg.det(C)), "(negative = mirrored)")
