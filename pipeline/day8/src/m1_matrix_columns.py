def apply(M, v):
    x, y = v
    col1 = [M[0][0], M[1][0]]
    col2 = [M[0][1], M[1][1]]
    return [x * col1[0] + y * col2[0], x * col1[1] + y * col2[1]]


def show(name, M, v):
    print(name, "M =", M, " v =", v, "-> M v =", apply(M, v))


i_hat = [1, 0]
j_hat = [0, 1]

M = [[1, 3],
     [-2, 0]]
print("i lands on", apply(M, i_hat), "  j lands on", apply(M, j_hat))
show("3Blue1Brown example:", M, [-1, 2])
print("by hand: -1 * [1, -2] + 2 * [3, 0] =", [-1 * 1 + 2 * 3, -1 * -2 + 2 * 0])

rotate = [[0, -1],
          [1, 0]]
show("rotate 90:", rotate, [1, 0])
show("rotate 90:", rotate, [2, 1])

shear = [[1, 1],
         [0, 1]]
show("shear:    ", shear, [0, 1])
show("shear:    ", shear, [2, 1])

squash = [[2, -2],
          [1, -1]]
for v in ([1, 0], [0, 1], [3, 5], [-2, 4]):
    show("squash:   ", squash, v)
