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
# construct A_explicit method
A_ = np.zeros([m - 1, m + 1])
for row in range(m - 2, -1, -1):  # row-St
    j = (m-1) - row   # 由於j是由下而上漸漸變大排序(j = 2, ..., m-2) ；但row是由下而上漸漸變小排序(row = m-3, m-4, ..., 1)
    col = row + 2     # 由於row = m-2, m-3, ..., 1 這樣排序，a(j)出現位置由最右邊開始，即column排序為 m, m-1, ..., 3
    A_[row, col] = (-0.5 * (r-q) * j * dt + 0.5 * (sigma**2) * (j**2) * dt) / (1 + r*dt)     # a(j)
    A_[row, col - 1] = (1 - (sigma ** 2) * (j ** 2) * dt) / (1 + r*dt)                       # b(j)
    A_[row, col - 2] = (0.5 * (r-q) * j * dt + 0.5 * (sigma**2) * (j**2) * dt) / (1 + r*dt)  # c(j)


# European call
def Explicit_Eurcall(S0, K, r, q, sigma, T, Smin, Smax, m, n):
    # boundary condition
    f_max = max(m * dS - K, 0)
    f_min = max(0 * dS - K, 0)

    # option value at maturity (known)
    b = np.zeros([m+1, 1])
    for row in range(m+1):
        j = m - row    # 由於j是由下而上漸漸變大排序(j = 0,1,..., m) ；但row是由下而上漸漸變小排序(row = m, m-1, ..., 0)
        b[row, 0] = max(j*dS - K, 0)

    # solve Ab = x
    for i in range(n):
        x = np.dot(A_, b)       # nrow * ncol = (m-1)*1
        b = np.zeros([m+1, 1])  # nrow * ncol = (m-1)*1

        # 求出的x做為下一輪迴圈的b
        for b_rows in range(m+1):
            if b_rows == 0:
                b[b_rows, 0] = f_max
            elif b_rows == m:
                b[b_rows, 0] = f_min
            else:
                b[b_rows, 0] = x[b_rows - 1, 0] # b為(m+1,1)；x為(m-1,1) 而x由上而下為 0,1,...,m-2；b為1,2,...,m-1 (因b的最頭和最尾是boundary condition)

    j = int(S0 / dS)
    call_price = x[(m-1)-j, 0] # 由於x中row由上而下排序為0,1,...,m-2；j的排序由上而下為 m-1, m-2,...,1； 故row = (m-1) - j
    return call_price

# European put
def Explicit_Eurput(S0, K, r, q, sigma, T, Smin, Smax, m, n):
    # boundary condition
    f_max = max(K - m * dS, 0)
    f_min = max(K - 0 * dS, 0)

    # option value at maturity (known)
    b = np.zeros([m+1, 1])
    for row in range(m+1):
        j = m - row    # 由於j是由下而上漸漸變大排序(j = 0,1,..., m) ；但row是由下而上漸漸變小排序(row = m, m-1, ..., 0)
        b[row, 0] = max(K - j*dS, 0)

    # solve Ab = x
    for i in range(n):
        x = np.dot(A_, b)       # nrow * ncol = (m-1)*1
        b = np.zeros([m+1, 1])  # nrow * ncol = (m-1)*1

        # 求出的x做為下一輪迴圈的b
        for b_rows in range(m+1):
            if b_rows == 0:
                b[b_rows, 0] = f_max
            elif b_rows == m:
                b[b_rows, 0] = f_min
            else:
                b[b_rows, 0] = x[b_rows - 1, 0] # b為(m+1,1)；x為(m-1,1) 而x由上而下為 0,1,...,m-2；b為1,2,...,m-1 (因b的最頭和最尾是boundary condition)

    j = int(S0 / dS)
    put_price = x[(m-1)-j, 0] # 由於x中row由上而下排序為0,1,...,m-2；j的排序由上而下為 m-1, m-2,...,1； 故row = (m-1) - j
    return put_price


# American call
def Explicit_AMcall(S0, K, r, q, sigma, T, Smin, Smax, m, n):
    # boundary condition
    f_max = max(m * dS - K, 0)
    f_min = max(0 * dS - K, 0)

    # option value at maturity (known)
    b = np.zeros([m+1, 1])
    for row in range(m+1):
        j = m - row    # 由於j是由下而上漸漸變大排序(j = 0,1,..., m) ；但row是由下而上漸漸變小排序(row = m, m-1, ..., 0)
        b[row, 0] = max(j*dS - K, 0)

    # solve Ab = x
    for i in range(n):
        x = np.dot(A_, b)       # nrow * ncol = (m-1)*1
        b = np.zeros([m+1, 1])  # nrow * ncol = (m-1)*1

        # decide whether keep holding to maturity is better or early exercise is better one?
        for row in range(m - 1):
            price_if_HTM = x[row, 0]
            price_if_early_exercise = max(((m - 1) - row) * dS - K, 0)
            if price_if_early_exercise > price_if_HTM:
                x[row, 0] = price_if_early_exercise
            else:
                continue

        # 求出的x做為下一輪迴圈的b
        for b_rows in range(m+1):
            if b_rows == 0:
                b[b_rows, 0] = f_max
            elif b_rows == m:
                b[b_rows, 0] = f_min
            else:
                b[b_rows, 0] = x[b_rows - 1, 0] # b為(m+1,1)；x為(m-1,1) 而x由上而下為 0,1,...,m-2；b為1,2,...,m-1 (因b的最頭和最尾是boundary condition)

    j = int(S0 / dS)
    call_price = x[(m-1)-j, 0] # 由於x中row由上而下排序為0,1,...,m-2；j的排序由上而下為 m-1, m-2,...,1； 故row = (m-1) - j
    return call_price


# American put
def Explicit_AMput(S0, K, r, q, sigma, T, Smin, Smax, m, n):
    # boundary condition
    f_max = max(K - m * dS, 0)
    f_min = max(K - 0 * dS, 0)

    # option value at maturity (known)
    b = np.zeros([m + 1, 1])
    for row in range(m + 1):
        j = m - row  # 由於j是由下而上漸漸變大排序(j = 0,1,..., m) ；但row是由下而上漸漸變小排序(row = m, m-1, ..., 0)
        b[row, 0] = max(K - j * dS, 0)

    # solve Ab = x
    for i in range(n):
        x = np.dot(A_, b)  # nrow * ncol = (m-1)*1
        b = np.zeros([m + 1, 1])  # nrow * ncol = (m-1)*1

        # decide whether keep holding to maturity is better or early exercise is better one?
        for row in range(m - 1):
            price_if_HTM = x[row, 0]
            price_if_early_exercise = max(K - ((m - 1) - row) * dS, 0)
            if price_if_early_exercise > price_if_HTM:
                x[row, 0] = price_if_early_exercise
            else:
                continue

        # 求出的x做為下一輪迴圈的b
        for b_rows in range(m + 1):
            if b_rows == 0:
                b[b_rows, 0] = f_max
            elif b_rows == m:
                b[b_rows, 0] = f_min
            else:
                b[b_rows, 0] = x[
                    b_rows - 1, 0]  # b為(m+1,1)；x為(m-1,1) 而x由上而下為 0,1,...,m-2；b為1,2,...,m-1 (因b的最頭和最尾是boundary condition)

    j = int(S0 / dS)
    put_price = x[(m - 1) - j, 0]  # 由於x中row由上而下排序為0,1,...,m-2；j的排序由上而下為 m-1, m-2,...,1； 故row = (m-1) - j
    return put_price

print(str("European call_explicit method = ") + str(Explicit_Eurcall(S0, K, r, q, sigma, T, Smin, Smax, m, n)))
print(str("European put_explicit method = ") + str(Explicit_Eurput(S0, K, r, q, sigma, T, Smin, Smax, m, n)))
print(str("American call_explicit method = ") + str(Explicit_AMcall(S0, K, r, q, sigma, T, Smin, Smax, m, n)))
print(str("American put_explicit method = ") + str(Explicit_AMput(S0, K, r, q, sigma, T, Smin, Smax, m, n)))
