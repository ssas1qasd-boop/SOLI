# Review: dot product and vector length by hand (Khan Academy), no libraries
import math


def dot(a, b):
    total = 0
    for i in range(len(a)):
        total += a[i] * b[i]
    return total


def length(a):
    return math.sqrt(dot(a, a))


a = [2, 5]
b = [7, 1]
print("[2, 5] . [7, 1] =", dot(a, b))

c = [1, 2, 3]
d = [-2, 0, 5]
print("[1, 2, 3] . [-2, 0, 5] =", dot(c, d))

print("|[2, 5]| =", length(a))
print("sqrt(29) =", math.sqrt(29))
print("|a| squared =", round(length(a) ** 2, 6), "  a . a =", dot(a, a))

big = [1] * 50
print("50 ones: length =", length(big), "  sqrt(50) =", math.sqrt(50))
