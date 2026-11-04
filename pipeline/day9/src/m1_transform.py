def T(v):
    x1, x2, x3 = v
    return (x1 + 2 * x2, 3 * x3)


print("T(1, 1, 1) =", T((1, 1, 1)))
print("T(2, 4, 1) =", T((2, 4, 1)))
print("input has", len((1, 1, 1)), "numbers (R3), output has", len(T((1, 1, 1))), "numbers (R2)")

A = [[1, 2, 0],
     [0, 0, 3]]


def times(A, v):
    return tuple(sum(A[r][c] * v[c] for c in range(len(v))) for r in range(len(A)))


for v in [(1, 1, 1), (2, 4, 1), (0, 0, 0)]:
    print("T", v, "=", T(v), "   A times", v, "=", times(A, v))


def S(v):
    x1, x2, x3 = v
    return (x1 * x1, x2 + 1)


print("S(0, 0, 0) =", S((0, 0, 0)), " -> the origin moved, so S is not linear")
print("S(2, 0, 0) =", S((2, 0, 0)), " but 2 * S(1, 0, 0) =", tuple(2 * c for c in S((1, 0, 0))))
