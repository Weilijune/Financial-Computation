# arithmatic average call
# MC (only European call) and Tree method (both European and American call)

import numpy as np
from numpy.random import normal
from math import log, sqrt, exp

# input
St = float(input("St = "))
K = float(input("K = "))
R = float(input("r = "))
q = float(input("q = "))
sigma = float(input("sigma = "))
t = float(input("t = "))
T_t = float(input("T-t = "))
M = int(input("num of representative average price (M) = "))
n = int(input("time_step (n) = "))
Save_t = float(input("Save,t = "))
num_sim = int(input("num_of_simulation = "))
num_rep = int(input("num_of_repetition = "))

# binomial tree
dt = T_t / n
u = exp(sigma * sqrt(dt))
d = 1 / u
p = (exp((R - q) * dt) - d) / (u - d)  # prob_of_up

# step 1: payoff at maturity (build Save list)
# 三維矩陣：[層數 , row, column]
s_ave = np.zeros([M+1, n+1, n+1])
call = np.zeros([M+1, n+1, n+1])
AMcall = np.zeros([M+1, n+1, n+1])

for i in range(n + 1):      # i = col
    for j in range(n + 1):  # j = row
        if j <= i:          # since it's tree, we only care about upper-triangle
            Amax = (Save_t * ((t-0)/dt + 1) + St * (u * (1 - u ** (i - j)) / (1-u)) + St * ((u ** (i - j)) * d * (1-d**j)/(1-d))) / (i + (t-0)/dt + 1)
            Amin = (Save_t * ((t-0)/dt + 1) + St * (d * (1 - d ** j) / (1-d)) + St * ((d ** j) * u * (1 - u ** (i - j)) / (1-u))) / (i + (t-0)/dt + 1)
            for k in range(M + 1):
                s_ave[k, j, i] = ((M - k)/M) * Amax + (k/M) * Amin
                if i == n:
                    call[k, j, n] = max(s_ave[k, j, i] - K, 0)
                    AMcall[k, j, n] = max(s_ave[k, j, i] - K, 0)

# step 2: backward induction
for i in range(n - 1, -1, -1): # i = col counts for n-1, n-2,...,0
    for j in range(n + 1):     # j = row counts for 0, 1, ..., n
        if j <= i:             # since it's tree, we only care about upper-triangle
            for k in range(M + 1):
                Au = ((i + (t-0)/dt + 1) * s_ave[k, j, i] + St * (u ** (i + 1 - j)) * (d ** j)) / (i + (t-0)/dt + 2)
                Ad = ((i + (t-0)/dt + 1) * s_ave[k, j, i] + St * (u ** (i + 1 - (j+1))) * (d ** (j+1))) / (i + (t-0)/dt + 2)

                # find Au in s_ave[:, j, i + 1] >> linear interpolation get Cu
                # initial guess: 由s_ave[:, j, i + 1]中的上界 開始往下找
                ku = 0
                for up in range(M + 1):
                    if Au >= s_ave[up, j, i + 1] or i == j:
                        break
                    elif Au < s_ave[up, j, i + 1]:
                        ku += 1

                # if ku = M+1(爆掉) 或 一路往下走的case
                if ku == M + 1 or (ku == 0 and i == j):
                    Cu = call[M, j, i + 1]
                    Cu_AM = AMcall[M, j, i + 1]
                # if Amax == Amin
                elif s_ave[ku - 1, j, i + 1] == s_ave[ku, j, i + 1]:
                    Cu = call[ku, j, i + 1]
                    Cu_AM = AMcall[ku, j, i + 1]
                # linear interpolation
                else:
                    w = (s_ave[ku - 1, j, i + 1] - Au) / (s_ave[ku - 1, j, i + 1] - s_ave[ku, j, i + 1])
                    Cu = w * call[ku, j, i + 1] + (1 - w) * call[ku - 1, j, i + 1]
                    Cu_AM = w * AMcall[ku, j, i + 1] + (1 - w) * AMcall[ku - 1, j, i + 1]

                # find Ad in s_ave[:, j + 1, i + 1] >> linear interpolation get Cd
                # initial guess: 由 s_ave[:, j + 1, i + 1]中的上界開始往下找
                kd = 0
                for down in range(M + 1):
                    if Ad >= s_ave[down, j + 1, i + 1] or i == j:
                        break
                    elif Ad < s_ave[down, j + 1, i + 1]:
                        kd += 1
                # if kd = M+1(爆掉) 或 一路往下走的case
                if kd == M + 1 or (i == j and kd == 0):
                    Cd = call[M, j + 1, i + 1]
                    Cd_AM = AMcall[M, j + 1, i + 1]
                # if Amax == Amin
                elif s_ave[kd - 1, j + 1, i + 1] == s_ave[kd, j + 1, i + 1]:
                    Cu = call[kd, j + 1, i + 1]
                    Cu_AM = AMcall[kd, j + 1, i + 1]
                # linear interpolation
                else:
                    w = (s_ave[kd - 1, j + 1, i + 1] - Ad) / (s_ave[kd - 1, j + 1, i + 1] - s_ave[kd, j + 1, i + 1])
                    Cd = w * call[kd, j + 1, i + 1] + (1 - w) * call[kd - 1, j + 1, i + 1]
                    Cd_AM = w * AMcall[kd, j + 1, i + 1] + (1 - w) * AMcall[kd - 1, j + 1, i + 1]

                # get European call[k,j,i]
                call[k, j, i] = (p * Cu + (1-p) * Cd) * exp(-R*dt)

                # get American call[k,j,i]
                payoff_if_HTM = (p * Cu_AM + (1-p) * Cd_AM) * exp(-R*dt)
                payoff_if_early_exercise = s_ave[k, j, i] - K
                AMcall[k, j, i] = max(payoff_if_HTM, payoff_if_early_exercise)
# output
print(str("European Arithmatic average call = ") + str(call[0, 0, 0]))
print(str("American Arithmatic average call = ") + str(AMcall[0, 0, 0]))

# MC simulation
dt = T_t / n
simulated_price = []
for simulation in range(num_rep):
    payoff = []
    # build 10000 (num_sim) 條 S path
    S_path = np.zeros([num_sim, n+1])
    S_path[:, 0] = St

    # path dependent - record 10000 S(t+dt) value into S_path list
    for col in range(1, n+1):
        rand = normal(0, 1, size= num_sim)
        for row in range(num_sim):
            ln_St_dt = (log(S_path[row, col-1]) + (R - q - sigma ** 2 / 2.) * dt) + sigma * sqrt(dt) * rand[row]
            St_dt = exp(ln_St_dt)
            S_path[row, col] = St_dt

    # payoff at maturity
    S_path[:, 0] = Save_t  # 要計算平均值了，把St替換成Save,t
    for row in range(num_sim):
        # 把這一條路徑的s path加總，加上issue date~t期的平均(n次) > 除以總數 ((n+1) + (t-0)/dt)
        Save_T = (sum(S_path[row, :]) + Save_t * (t-0)/dt) / ((n + 1) + (t-0)/dt)
        payoff_at_T = max(Save_T - K, 0)
        payoff.append(payoff_at_T)

    price = exp(-R * T_t) * np.array(payoff).mean()
    simulated_price.append(price)

MC_call_value = np.array(simulated_price).mean()
MC_call_ub = np.array(simulated_price).mean() + 2 * np.array(simulated_price).std()
MC_call_lb = np.array(simulated_price).mean() - 2 * np.array(simulated_price).std()

print(str("Monte Carlo European Arithmatic average call price = ") + str(MC_call_value))
print(str("95% CI for European Arithmatic average call = [") + str(MC_call_lb) + str(", ") + str(MC_call_ub) + str("]"))
