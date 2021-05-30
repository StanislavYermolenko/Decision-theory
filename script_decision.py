from calculation import *
from math import sqrt

input_file = "task.dat"
output_file = "execution_result.dat"

first_GF = True

# read input
ifile = open(input_file, 'r')

# f
s = ifile.readline()
if s[:3] == "max":
    f_max = True
else:
    f_max = False
# print(1)

# A - матрица верхних границ по количеству эксп/имп
A = []
ifile.readline()
s = ifile.readline()
while s.find("C") == -1:
    try:
        A.append([float(x) for x in s.split()])
        s = ifile.readline()
    except ValueError:
        print("A contains not digits")
        exit()

# printm("A",A)
# exit()


# C - матрица цен
C = []
s = ifile.readline()
while s.find("T") == -1:
    try:
        C.append([float(x) for x in s.split()])
        s = ifile.readline()
    except ValueError:
        print("C contains not digits")
        exit()

# print(C)
# exit()
# Ti
T = []
s = ifile.readline()
while s.find("alpha") == -1:
    try:
        t = s.split()
        T.append(float(t[0]))
        s = ifile.readline()
        if s.find("alpha") != -1:
            break
        s = ifile.readline()
    except ValueError:
        print("T contains not digits")
        exit()

# alpha
try:
    s = ifile.readline()
    t = s.split()
    alpha = float(t[0])
except ValueError:
    print("Alpha contains not digits")
    exit()

ifile.close()

# print(alpha)

# main work
N = len(A)
M = len(A[0])
G = len(T) + 1 + N * M
# exit()
# get _I
# столбец знаков неравенст
_I = get_matrix(G, 1)
for i in range(len(T)):
    _I[i] = "<="
# print(_I)
_I[len(T)] = "="
for i in range(N * M):
    _I[len(T) + 1 + i] = "<="

# print(_I)
# printm("I", _I)
# exit()

# get _B
# _B - столбец свободных членов
_B = get_matrix(G, 1)
for i in range(len(T)):
    _B[i] = T[i]
_B[len(T)] = 0.0
for i in range(N * M):
    _B[len(T) + 1 + i] = A[i // M][i % M]

# print("B", _B)
# exit()


# get _Z
_Z = get_matrix(N * M, 1)
if first_GF:
    # 1
    for i in range(N * M):
        if i % M == M - 1:
            _Z[i] = 1.0
        else:
            _Z[i] = 0.0
else:
    # 2
    for i in range(N):
        _Z[i] = 1.0
        _Z[i + N] = 3.0
        _Z[i + 2 * N] = 0.0

# print(_Z)
# exit()
# printm("Z",_Z)
# print(f_max)

# exit()
is_optimist = True


# get _A
# get_C_interval
def zero_func(x):
    if x < 0:
        return 0.0
    else:
        return x


def _C(C_copy, index, alph, optimist, _first_GF):
    _M = len(C_copy[0])
    if _first_GF:
        # 1
        if optimist:
            sign_ = 1.0
        else:
            sign_ = -1.0
        c = C[index // _M][index % _M]
        if index % _M == _M - 1:
            return zero_func(c * (1 - sign_ * sqrt((1 - alph) / (2 * alph))))
        else:
            return zero_func(c * (1 + sign_ * sqrt((1 - alph) / (2 * alph))))
    else:
        # 2
        pass


_A = get_matrix(G, N * M)
for j in range(len(T)):
    for i in range(N):
        _A[j][i + N * j] = 1.0
for i in range(N * M):
    sign = 1.0
    if i % M == M - 1:
        sign = -1.0
    _A[len(T) + 1 + i][i] = 1.0
# printm("_A",_A)


step = 0.01
ar_alpha = []
opt_f_alph = []
for k in range(1, 100):
    alpha = step * k
    ar_alpha.append(alpha)
    # for Optimist:
    print("For Optimist:")
    for i in range(N * M):
        sign = 1.0
        if i % M == M - 1:
            sign = -1.0
        _A[len(T)][i] = sign * _C(C, i, 0.8, is_optimist, first_GF)
    x = multy_simplex(_A, _I, _B, _Z, look_max=f_max)
    if x is None:
        opt_f_alph.append(0)
    else:
        x = sorted(x.items())
        print("Optimal plan:", x)
        optim_plan = x

        # calc f
        opt_f = 0.0
        for i in x:
            opt_f += _Z[i[0]] * i[1]
        print("opt_f=", opt_f)
        opt_f_alph.append(opt_f)

# print(ar_alpha)
# print(opt_f_alph)
# xlabel("alpha")
# ylabel("Целевая функция для Оптимиста")
# plot(ar_alpha,opt_f_alph)
# show()


step = 0.01
ar_alpha = []
pess_f_alph = []
for k in range(1, 100):
    alpha = step * k
    ar_alpha.append(alpha)
    # for Pessimist:
    print("For Pessimist: ", i)
    is_optimist = False
    for i in range(N * M):
        sign = 1.0
        if i % M == M - 1:
            sign = -1.0
        _A[len(T)][i] = sign * _C(C, i, 0.8, is_optimist, first_GF)
    x = multy_simplex(_A, _I, _B, _Z, look_max=f_max)
    print("For Pessimist:")
    if x is None:
        pess_f_alph.append(0)
    else:
        x = sorted(x.items())
        print("Optimal plan:", x)
        pess_plan = x

        # calc f
        pess_f = 0.0
        for i in x:
            pess_f += _Z[i[0]] * i[1]
        print("pess_f=", pess_f)
        pess_f_alph.append(pess_f)

# print(ar_alpha)
# print(ar_alpha)
# print(pess_f_alph)
# xlabel("alpha")
# ylabel("Целевая функция для Пессимиста ")
# optim_plan[2] = (6, 2885)
# plot(ar_alpha,pess_f_alph)
# show()

# exit()
# Result
print("Goal function is between: " + str(pess_f) + " and " + str(opt_f))
print("X0   X1  X2  X3  X4  X5  X6  X7  X8 ")
print("X11 X12 X13 X21 X22 X23 X31 X32 X33")
print("Goal Functiom")
print(_Z)
# print("Goal Function" + Z)
print("Optimal plan for pessimist: ", pess_plan)
print("Optimal plan for optimist: ", optim_plan)

# write Results in file

ofile = open(output_file, 'w')
ofile.write("Goal function is between: " + str(pess_f) + " and " + str(opt_f) + '\n')
ofile.write("Optimal plan for pessimist: " + str(pess_plan) + '\n')
ofile.write("Optimal plan for optimist: " + str(optim_plan) + '\n')
