
# modified simplex method

MAX_ITER = 100
INF = -1E+15
EPS = 1E-5


def multy_simplex(A, I, B, Z, look_max=True):
    # n, m
    n = len(A[0])
    m = len(I)

    # f to max
    if not look_max:
        Z = [-x for x in Z]

    # перейдём к двойственной задачи, если m<n
    if m < n:
        return 'not realized yet'

    # dx, dy
    dx = m
    dy = 0
    for i in range(m):
        if I[i] == ">=":
            dy += 1

    # main matrix
    # get A
    M = []
    for i in range(m):
        temp = [0.0 for i in range(n + dx + dy)]
        M.append(temp)
    i = j = 0
    for i in range(m):
        for j in range(n):
            M[i][j] = A[i][j]
    # get E
    for i in range(m):
        M[i][i + n] = 1.0
    # Z
    Z = Z + [0.0] * (dx + dy)

    # get y - synthetical
    temp = i = 0
    for i in range(m):
        if I[i] == ">=":
            M[i][n + dx + temp] = -1.0
            temp += 1
            Z[i + n] = INF
        if I[i] == "=":
            Z[i + n] = INF

    print("Z", Z)

    # e0, e1, ... ,em
    dopM = []
    for i in range(m):
        temp = [0.0 for i in range(1 + dx)]
        dopM.append(temp)
    for i in range(m):
        dopM[i][0] = B[i]
    for i in range(m):
        dopM[i][i + 1] = 1.0

    # basis
    Bx = []
    for i in range(m):
        Bx.append(n + i)

    numb_iter = 0
    x = dict()
    while 1:

        print("=========", numb_iter)

        # iter k
        # calc L
        # L
        L = []
        for i in range(m):
            sum = 0
            for j in range(m):
                sum += dopM[j][i + 1] * Z[Bx[j]]
            L.append(sum)

        # delta
        D = []
        for i in range(n + dx + dy):
            sum = 0
            for j in range(m):
                sum += M[j][i] * L[j]
            D.append(sum - Z[i])

        # print("L",L)
        # print("D",D)

        # Test of optimal
        if min(D) >= -EPS:
            # find optimum and go away
            for i in range(n):
                for j in range(m):
                    if Bx[j] == i:
                        x[i] = dopM[j][0]
            return x
        else:
            mind = min(D)
            for i in range(n + dx + dy):
                if abs(D[i] - mind) < 1e-5:
                    in_i = i
                    break
        # print("M",M)

        # Ak
        Ak = []
        for i in range(m):
            Ak.append(M[i][in_i])

        # Ak' = Bx * Ak
        Ak_t = []
        for i in range(m):
            sum = 0
            for j in range(m):
                sum += dopM[i][j + 1] * Ak[j]
            Ak_t.append(sum)
        Ak = Ak_t

        # print("AK", Ak)

        # out_i - out from basis
        mind = 0
        out_i = 'nosolve'
        first = True
        for i in range(m):
            if Ak[i] > 0:
                if first:
                    mind = dopM[i][0] / Ak[i]
                    out_i = i
                    first = False
                if mind > dopM[i][0] / Ak[i]:
                    mind = dopM[i][0] / Ak[i]
                    out_i = i
        # print("dopM",dopM)
        # print("mind=",mind,"out_i",out_i)
        # no solve there
        if out_i == 'nosolve':
            return None

        # enter new var to Bx
        Bx[out_i] = in_i
        # print("Bx",Bx)
        # print("dopM before",dopM)
        # Gauss
        znam = Ak[out_i]
        for i in range(m):
            if Ak[i] != 0.0 and i != out_i:
                for j in range(m + 1):
                    dopM[i][j] -= dopM[out_i][j] * Ak[i] * 1.0 / znam
        for i in range(m + 1):
            dopM[out_i][i] /= znam
        # print("dopM",dopM)

        numb_iter += 1
        if MAX_ITER < numb_iter:
            return None


def get_matrix(n, m):
    res = []
    for i in range(n):
        temp = []
        for j in range(m):
            temp.append(0.0)
        res.append(temp)
    return res


def printm(label, A):
    print(label + ":")
    for i in A:
        print(i)