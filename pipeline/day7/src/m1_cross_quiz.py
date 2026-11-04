# Test yourself: the cross product by hand (Khan Academy), no libraries
def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0]]


def dot(a, b):
    total = 0
    for i in range(len(a)):
        total += a[i] * b[i]
    return total


def check(question, got, expected):
    print(question, "=", got, "  PASS" if got == expected else "  FAIL")


a = [1, -7, 1]
b = [5, 2, 4]
c = cross(a, b)
check("[1, -7, 1] x [5, 2, 4]", c, [-30, 1, 37])
check("(a x b) . a", dot(c, a), 0)
check("(a x b) . b", dot(c, b), 0)

i = [1, 0, 0]
j = [0, 1, 0]
k = [0, 0, 1]
check("i x j", cross(i, j), k)
check("j x i", cross(j, i), [0, 0, -1])
check("b x a", cross(b, a), [30, -1, -37])
check("a x a", cross(a, a), [0, 0, 0])
