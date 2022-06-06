# lookback put_binomial tree
# Tree and MC method

import numpy as np
from numpy.random import normal
from math import log, sqrt, exp

# 輸入
St = float(input("St = "))
R = float(input("r = "))
q = float(input("q = "))
sigma = float(input("sigma = "))
t = float(input("t = "))
T = float(input("T = "))
Smax_t = float(input("Smax,t = "))
n = int(input("time_step (n) = "))
num_sim = int(input("num_of_simulation = "))
num_rep = int(input("num_of_repetition = "))

# Binomial Tree_European
dt = (T-t)/n
u = exp(sigma * sqrt(dt))
d = 1 / u
# prob_of_up
p = (exp((R - q) * dt) - d) / (u - d)

S = np.zeros([n+1, n+1])
# step1: 求路徑上所有的股價，先求出最後一期、倒數第二期的股價可能，然後再讓其他同層的價格與其相等，避免無法recombine Q
# 最後一期
for j in range(n + 1):
    ST = St * (u ** (n - j)) * (d ** j)
    S[j, n] = ST
    #　同層者（ｕ和ｄ的次方數相減相同者　＝　(i-j) - j = i- 2j >> 故即往上一格，往右兩格的格子，若為存在的格子，則值相同），價格相同
    row = j - 1
    col = n - 2
    while row >= 0 and col >= 0 and row <= col:  # row <= col的概念是CRR只處理上三角的格子
        S[row, col] = ST
        row -= 1
        col -= 2
# 倒數第二期
for j in range(n):
    ST = St * (u ** (n - 1 - j)) * (d ** j)
    S[j, n-1] = ST
    #　同層者（ｕ和ｄ的次方數相減相同者　＝　(i-j) - j = i- 2j >> 故即往上一格，往右兩格的格子，若為存在的格子，則值相同），價格相同
    row = j - 1
    col = (n-1) - 2
    while row >= 0 and col >= 0 and row <= col:
        S[row, col] = ST
        row -= 1
        col -= 2

# step2: build S_max list
# 三維矩陣：[層數 , row, column]
s_max = np.zeros([(n+1)+n+1, n+1, n+1])
num_Smax = np.zeros([n+1, n+1])

for c in range(n + 1):
    for r in range(n + 1):
        if r <= c and c == 0:
            s_max[0, 0, 0] = max(S[0,0], Smax_t) # S[0,0] = St
            num_Smax[0, 0] = 1
        elif r <= c:
            smax_list = []    # 自己的s_max
            parent_smax = []  # 看父母親的s_max有哪些
            if r-1 >= 0 and c-1 >= 0 and r-1 <= c-1: # 父親
                num = int(num_Smax[r-1, c-1])
                for slice in range(num):
                    parent_smax.append(s_max[slice, r-1, c-1])
            if r >= 0 and c-1 >= 0 and r <= c-1: # 母親
                num = int(num_Smax[r, c - 1])
                for slice in range(num):
                    parent_smax.append(s_max[slice, r, c-1])
            # 繼承
            for k in range(len(parent_smax)):
                if parent_smax[k] >= S[r, c] and parent_smax[k] not in smax_list:
                    smax_list.append(parent_smax[k])
                elif parent_smax[k] < S[r, c] and S[r, c] not in smax_list:
                    smax_list.append(S[r, c])

            for slice in range(len(smax_list)):
                s_max[slice, r, c] = smax_list[slice]
            num_Smax[r, c] = len(smax_list)

# step 3: payoff at T
EURput = np.zeros([(n+1)+n+1, n+1, n+1])
for r in range(n + 1):
    num = int(num_Smax[r, n])
    for slice in range(num):
        EURput[slice, r, n] = max(s_max[slice, r, n] - S[r, n], 0)

# step 4: backward induction
for c in range(n - 1, -1, -1): # c counts for n-1, n-2,...,0
    for r in range(n + 1):     # r counts for 0, 1, ..., n
        if r <= c:
            num_u = int(num_Smax[r, c + 1])
            num_d = int(num_Smax[r + 1, c + 1])
            u_smax = [] # up 的 parent: 父親 的 Smax_list ；u_smax[index] 中的index其實也代表他在第幾層(slice)，因append的順序
            d_smax = [] # down 的 parent: 母親 的 Smax_list
            for slice in range(num_u):
                u_smax.append(s_max[slice, r, c+1])
            for slice in range(num_d):
                d_smax.append(s_max[slice, r+1, c+1])

            num = int(num_Smax[r, c])
            for slice in range(num):
                payoff = 0
                # if up
                if s_max[slice, r, c] not in u_smax:
                    index = u_smax.index(S[r, c+1])  # u_smax[index] 中的index其實也代表他在第幾層(slice)，因append的順序
                    payoff += p * EURput[index, r, c+1]
                else:
                    index = u_smax.index(s_max[slice, r, c])
                    payoff += p * EURput[index, r, c + 1]
                # if down
                index_d = d_smax.index(s_max[slice, r, c])
                payoff += (1-p) * EURput[index_d, r+1, c+1]
                EURput[slice, r, c] = payoff * exp(-R * dt) # 折現

print(str("European Lookback put = ") + str(EURput[0,0,0]))

# Binomial Tree_American (從step3重作即可)
# step 3: payoff at T
AMput = np.zeros([(n+1)+n+1, n+1, n+1])
for r in range(n + 1):
    num = int(num_Smax[r, n])
    for slice in range(num):
        AMput[slice, r, n] = max(s_max[slice, r, n] - S[r, n], 0)

# step 4: backward induction
for c in range(n - 1, -1, -1): # c counts for n-1, n-2,...,0
    for r in range(n + 1):     # r counts for 0, 1, ..., n
        if r <= c:
            num_u = int(num_Smax[r, c + 1])
            num_d = int(num_Smax[r + 1, c + 1])
            u_smax = [] # up 的 parent: 父親 的 Smax_list ；u_smax[index] 中的index其實也代表他在第幾層(slice)，因append的順序
            d_smax = [] # down 的 parent: 母親 的 Smax_list
            for slice in range(num_u):
                u_smax.append(s_max[slice, r, c+1])
            for slice in range(num_d):
                d_smax.append(s_max[slice, r+1, c+1])

            num = int(num_Smax[r, c])
            for slice in range(num):
                payoff = 0
                # if up
                if s_max[slice, r, c] not in u_smax:
                    index = u_smax.index(S[r, c+1])
                    payoff += p * AMput[index, r, c+1]
                else:
                    index = u_smax.index(s_max[slice, r, c])
                    payoff += p * AMput[index, r, c + 1]
                # if down
                index_d = d_smax.index(s_max[slice, r, c])
                payoff += (1-p) * AMput[index_d, r+1, c+1]

                # decide whether early exercise is better than holding to maturity
                payoff_if_early_exercise = max(s_max[slice, r, c] - S[r, c], 0)
                payoff_if_HTM = payoff * exp(-R * dt)
                AMput[slice, r, c] = max(payoff_if_HTM, payoff_if_early_exercise)

print(str("American Lookback put = ") + str(AMput[0,0,0]))

# Monte Carlo
# Monte Carlo Simulation
original_St = St
dt = (T - t) / n
simulated_price = []
for simulation in range(num_rep):
    payoff = []
    S_path = np.zeros([num_sim, n+1])
    S_path[:, 0] = original_St

    # path dependent - record 10000 S(t+dt) value into S_path list
    for col in range(1, n+1):
        rand = normal(0, 1, size= num_sim)
        for row in range(num_sim):
            ln_St_dt = (log(S_path[row, col-1]) + (R - q - sigma ** 2 / 2.) * dt) + sigma * sqrt(dt) * rand[row]
            St_dt = exp(ln_St_dt)
            S_path[row, col] = St_dt
    # compare the maximum in each S path
    S_path[:, 0] = max(original_St, Smax_t)
    for row in range(num_sim):
        Smax = max(S_path[row,:])
        ST = S_path[row, -1]
        payoff_at_T = max(Smax - ST, 0)
        payoff.append(payoff_at_T)

    price = exp(-R * (T-t)) * np.array(payoff).mean()
    simulated_price.append(price)

MC_put_value = np.array(simulated_price).mean()
MC_put_ub = np.array(simulated_price).mean() + 2 * np.array(simulated_price).std()
MC_put_lb = np.array(simulated_price).mean() - 2 * np.array(simulated_price).std()

print(str("Monte Carlo European Lookback put price = ") + str(MC_put_value))
print(str("95% CI for European Lookback put = [") + str(MC_put_lb) + str(", ") + str(MC_put_ub) + str("]"))
