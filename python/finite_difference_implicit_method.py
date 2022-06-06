# finite difference method - implicit method
# price European and American options (call and put)
import numpy as np
# input
S0 = float(input("S0 = "))
K = float(input("K = "))
r = float(input("r = "))
q = float(input("q = "))
sigma = float(input("sigma = "))
T = float(input("T = "))
Smin = float(input("S_min = "))
Smax = float(input("S_max = "))
m = int(input("num of partition for St = "))
n = int(input("time_step (n) = "))

dS = (Smax - Smin) / m
dt = T / n

# construct A_implicit method
A = np.zeros([m - 1, m - 1])
for row in range(m - 2, -1, -1):  # row-St
    if row == m - 2:
        j = 1
        A[row, -1] = 1 + (sigma ** 2) * (j ** 2) * dt + r * dt                     # b1 (j = 1)
        A[row, -2] = -(r - q) * 0.5 * j * dt - 0.5 * (sigma ** 2) * (j ** 2) * dt  # c1

    elif row == 0:
        j = m - 1
        A[row, 1] = (r - q) * 0.5 * j * dt - 0.5 * (sigma ** 2) * (j ** 2) * dt  # a(m-1)
        A[row, 0] = 1 + (sigma ** 2) * (j ** 2) * dt + r * dt                    # b(m-1)
    else:
        j = (m-1) - row  # 由於j是由下而上漸漸變大排序(j = 2, ..., m-2) ；但row是由下而上漸漸變小排序(row = m-3, m-4, ..., 1)
        col = row + 1    # 由於row = m-3, m-4, ..., 1 這樣排序，a(j)出現位置由最右邊開始，即column排序為 m-2, m-3, ..., 2
        A[row, col] = (r - q) * 0.5 * j * dt - 0.5 * (sigma ** 2) * (j ** 2) * dt       # a(j)
        A[row, col - 1] = 1 + (sigma ** 2) * (j ** 2) * dt + r * dt                     # b(j)
        A[row, col - 2] = -(r - q) * 0.5 * j * dt - 0.5 * (sigma ** 2) * (j ** 2) * dt  # c(j)


# European call
def Implicit_Eurcall(S0, K, r, q, sigma, T, Smin, Smax, m, n):
    # boundary condition
    f_max = max(m * dS - K, 0)
    f_min = max(0 * dS - K, 0)

    # option value at maturity (known)
    b = np.zeros([m-1, 1])
    a1 = (r - q) * 0.5 * 1 * dt - 0.5 * (sigma ** 2) * (1 ** 2) * dt                   # j=1
    c_last = -(r - q) * 0.5 * (m-1) * dt - 0.5 * (sigma ** 2) * ((m-1) ** 2) * dt      # j=m-1
    for row in range(m-1):
        if row == 0:
            b[row, 0] = max((m-1)*dS - K, 0) - c_last * f_max
        elif row == m-2:
            b[row, 0] = max(1 * dS - K, 0) - a1 * f_min
        else:
            j = (m-1) - row # 由於j是由下而上漸漸變大排序(j = 2, ..., m-2) ；但row是由下而上漸漸變小排序(row = m-3, m-4, ..., 1)
            b[row, 0] = max(j*dS - K, 0)

    # # solve Ax = b
    A_inv = np.linalg.inv(A)
    for i in range(n):
        x = np.dot(A_inv, b)
        x[0, 0] -= c_last * f_max
        x[m-2, 0] -= a1 * f_min
        b = np.zeros([m-1, 1])
        for row in range(m-1):
            b[row,0] = x[row,0] # 把b替代為下一個迴圈的x

    j = int(S0 / dS)
    call_price = x[(m-1)-j, 0]   # 由於x中row由上而下排序為0,1,...,m-2；j的排序由上而下為 m-1, m-2,...,1； 故row = (m-1) - j
    return call_price


# European put
def Implicit_Eurput(S0, K, r, q, sigma, T, Smin, Smax, m, n):
    # boundary condition
    f_max = max(K - m * dS, 0)
    f_min = max(K - 0 * dS, 0)

    # option value at maturity (known)
    b = np.zeros([m - 1, 1])
    a1 = (r - q) * 0.5 * 1 * dt - 0.5 * (sigma ** 2) * (1 ** 2) * dt  # j=1
    c_last = -(r - q) * 0.5 * (m - 1) * dt - 0.5 * (sigma ** 2) * ((m - 1) ** 2) * dt  # j=m-1
    for row in range(m - 1):
        if row == 0:
            b[row, 0] = max(K - (m - 1) * dS, 0) - c_last * f_max
        elif row == m - 2:
            b[row, 0] = max(K - 1 * dS, 0) - a1 * f_min
        else:
            j = (m - 1) - row
            b[row, 0] = max(K - j * dS, 0)

    # # solve Ax = b
    A_inv = np.linalg.inv(A)
    for i in range(n):
        x = np.dot(A_inv, b)
        x[0, 0] -= c_last * f_max
        x[m - 2, 0] -= a1 * f_min
        b = np.zeros([m - 1, 1])
        for row in range(m - 1):
            b[row, 0] = x[row, 0]

    j = int(S0 / dS)
    put_price = x[(m - 1) - j, 0]
    return put_price


# American call
def Implicit_AMcall(S0, K, r, q, sigma, T, Smin, Smax, m, n):
    # boundary condition
    f_max = max(m * dS - K, 0)
    f_min = max(0 * dS - K, 0)

    # option value at maturity (known)
    b = np.zeros([m - 1, 1])
    a1 = (r - q) * 0.5 * 1 * dt - 0.5 * (sigma ** 2) * (1 ** 2) * dt  # j=1
    c_last = -(r - q) * 0.5 * (m - 1) * dt - 0.5 * (sigma ** 2) * ((m - 1) ** 2) * dt  # j=m-1
    for row in range(m - 1):
        if row == 0:
            b[row, 0] = max((m - 1) * dS - K, 0) - c_last * f_max
        elif row == m - 2:
            b[row, 0] = max(1 * dS - K, 0) - a1 * f_min
        else:
            j = (m - 1) - row
            b[row, 0] = max(j * dS - K, 0)

    # # solve Ax = b
    A_inv = np.linalg.inv(A)
    for i in range(n):
        x = np.dot(A_inv, b)
        # decide whether keep holding to maturity is better or early exercise is better one?
        for row in range(m-1):
            price_if_HTM = x[row, 0]
            price_if_early_exercise = max(((m - 1) - row) * dS - K, 0)
            if price_if_early_exercise > price_if_HTM:
                x[row, 0] = price_if_early_exercise
            else:
                continue

        x[0, 0] -= c_last * f_max
        x[m - 2, 0] -= a1 * f_min
        b = np.zeros([m - 1, 1])
        for row in range(m - 1):
            b[row, 0] = x[row, 0]

    j = int(S0 / dS)
    call_price = x[(m - 1) - j, 0]
    return call_price

# American put
def Implicit_AMput(S0, K, r, q, sigma, T, Smin, Smax, m, n):
    # boundary condition
    f_max = max(K - m * dS, 0)
    f_min = max(K - 0 * dS, 0)

    # option value at maturity (known)
    b = np.zeros([m - 1, 1])
    a1 = (r - q) * 0.5 * 1 * dt - 0.5 * (sigma ** 2) * (1 ** 2) * dt  # j=1
    c_last = -(r - q) * 0.5 * (m - 1) * dt - 0.5 * (sigma ** 2) * ((m - 1) ** 2) * dt  # j=m-1
    for row in range(m - 1):
        if row == 0:
            b[row, 0] = max(K - (m - 1) * dS, 0) - c_last * f_max
        elif row == m - 2:
            b[row, 0] = max(K - 1 * dS, 0) - a1 * f_min
        else:
            j = (m - 1) - row
            b[row, 0] = max(K - j * dS, 0)

    # # solve Ax = b
    A_inv = np.linalg.inv(A)
    for i in range(n):
        x = np.dot(A_inv, b)
        # decide whether keep holding to maturity is better or early exercise is better one?
        for row in range(m-1):
            price_if_HTM = x[row, 0]
            price_if_early_exercise = max(K - ((m - 1) - row) * dS, 0)
            if price_if_early_exercise > price_if_HTM:
                x[row, 0] = price_if_early_exercise
            else:
                continue

        x[0, 0] -= c_last * f_max
        x[m - 2, 0] -= a1 * f_min
        b = np.zeros([m - 1, 1])
        for row in range(m - 1):
            b[row, 0] = x[row, 0]

    j = int(S0 / dS)
    put_price = x[(m - 1) - j, 0]
    return put_price

print(str("European call_implicit method = ") + str(Implicit_Eurcall(S0, K, r, q, sigma, T, Smin, Smax, m, n)))
print(str("European put_implicit method = ") + str(Implicit_Eurput(S0, K, r, q, sigma, T, Smin, Smax, m, n)))
print(str("American call_implicit method = ") + str(Implicit_AMcall(S0, K, r, q, sigma, T, Smin, Smax, m, n)))
print(str("American put_implicit method = ") + str(Implicit_AMput(S0, K, r, q, sigma, T, Smin, Smax, m, n)))
