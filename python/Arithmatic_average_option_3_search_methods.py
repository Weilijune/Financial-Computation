# arithmatic average call
# compare 3 methods to locate positions of Au and Ad in terms of computation time
## note: the third method is most popular

import numpy as np
from math import log, sqrt, exp
import time

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

# binomial tree
dt = T_t / n
u = exp(sigma * sqrt(dt))
d = 1 / u
p = (exp((R - q) * dt) - d) / (u - d)  # prob_of_up

# way 1: sequential search
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
start1 = time.time()
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
                    Cu = w * call[ku, j, i + 1] + (1-w) * call[ku - 1, j, i + 1]
                    Cu_AM = w * AMcall[ku, j, i + 1] + (1-w) * AMcall[ku - 1, j, i + 1]

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
                    Cd = w * call[kd, j + 1, i + 1] + (1-w) * call[kd - 1, j + 1, i + 1]
                    Cd_AM = w * AMcall[kd, j + 1, i + 1] + (1 - w) * AMcall[kd - 1, j + 1, i + 1]

                # get European call[k,j,i]
                call[k, j, i] = (p * Cu + (1-p) * Cd) * exp(-R*dt)

                # get American call[k,j,i]
                payoff_if_HTM = (p * Cu_AM + (1-p) * Cd_AM) * exp(-R*dt)
                payoff_if_early_exercise = s_ave[k, j, i] - K
                AMcall[k, j, i] = max(payoff_if_HTM, payoff_if_early_exercise)
end1 = time.time()
# output
print("Sequential search:")
print(str("European Arithmatic average call = ") + str(round(call[0, 0, 0], 4)))
print(str("American Arithmatic average call = ") + str(round(AMcall[0, 0, 0], 4)))
print(str("The time used to execute backward induction:") + str(end1 - start1))

# way 2: binary search
# step 1: payoff at maturity (build Save list)
# 三維矩陣：[層數 , row, column]
s_ave2 = np.zeros([M+1, n+1, n+1])
call2 = np.zeros([M+1, n+1, n+1])
AMcall2 = np.zeros([M+1, n+1, n+1])

for i in range(n + 1):      # i = col
    for j in range(n + 1):  # j = row
        if j <= i:          # since it's tree, we only care about upper-triangle
            Amax = (Save_t * ((t-0)/dt + 1) + St * (u * (1 - u ** (i - j)) / (1-u)) + St * ((u ** (i - j)) * d * (1-d**j)/(1-d))) / (i + (t-0)/dt + 1)
            Amin = (Save_t * ((t-0)/dt + 1) + St * (d * (1 - d ** j) / (1-d)) + St * ((d ** j) * u * (1 - u ** (i - j)) / (1-u))) / (i + (t-0)/dt + 1)
            for k in range(M + 1):
                s_ave2[k, j, i] = ((M - k)/M) * Amax + (k/M) * Amin
                if i == n:
                    call2[k, j, n] = max(s_ave2[k, j, i] - K, 0)
                    AMcall2[k, j, n] = max(s_ave2[k, j, i] - K, 0)

# step 2: backward induction
start2 = time.time()
for i in range(n - 1, -1, -1): # i = col counts for n-1, n-2,...,0
    for j in range(n + 1):     # j = row counts for 0, 1, ..., n
        if j <= i:             # since it's tree, we only care about upper-triangle
            for k in range(M + 1):
                Au = ((i + (t-0)/dt + 1) * s_ave2[k, j, i] + St * (u ** (i + 1 - j)) * (d ** j)) / (i + (t-0)/dt + 2)
                Ad = ((i + (t-0)/dt + 1) * s_ave2[k, j, i] + St * (u ** (i + 1 - (j+1))) * (d ** (j+1))) / (i + (t-0)/dt + 2)

                # find Au in s_ave[:, j, i + 1] >> linear interpolation get Cu
                # initial guess
                upper = M  # index 越大，s ave越小
                lower = 0
                index_u = int((lower + upper)/2)
                while not (Au < s_ave2[index_u, j, i + 1] and Au > s_ave2[index_u + 1, j, i + 1]):
                    if Au == s_ave2[index_u, j, i + 1] or s_ave2[0, j, i + 1] == s_ave2[M, j, i + 1]:
                        Cu = call2[index_u, j, i + 1]
                        Cu_AM = AMcall2[index_u, j, i + 1]
                        break
                    elif Au == s_ave2[index_u + 1, j, i + 1]:
                        Cu = call2[index_u + 1, j, i + 1]
                        Cu_AM = AMcall2[index_u + 1, j, i + 1]
                        break
                    elif Au < s_ave2[M, j, i + 1]:
                        Cu = call2[M, j, i + 1]
                        Cu_AM = AMcall2[M, j, i + 1]
                        break
                    elif Au > s_ave2[0, j, i + 1]:
                        Cu = call2[0, j, i + 1]
                        Cu_AM = AMcall2[0, j, i + 1]
                        break

                    elif Au > s_ave2[index_u, j, i + 1]:
                        upper = index_u
                    else:
                        lower = index_u

                    index_u = int((lower + upper) / 2)
                    if lower == upper:
                        Cu = call2[index_u, j, i + 1]
                        Cu_AM = AMcall2[index_u, j, i + 1]
                        break

                if Au < s_ave2[index_u, j, i + 1] and Au > s_ave2[index_u + 1, j, i + 1]:
                    w = (s_ave2[index_u, j, i + 1] - Au) / (s_ave2[index_u, j, i + 1] - s_ave2[index_u + 1, j, i + 1])
                    Cu = w * call2[index_u + 1, j, i + 1] + (1-w) * call2[index_u, j, i + 1]
                    Cu_AM = w * AMcall2[index_u + 1, j, i + 1] + (1-w) * AMcall2[index_u, j, i + 1]

                # find Ad in s_ave[:, j + 1, i + 1] >> linear interpolation get Cd
                # initial guess
                upper_d = M
                lower_d = 0
                index_d = int((lower_d + upper_d) / 2)
                while not (Ad < s_ave2[index_d, j + 1, i + 1] and Ad > s_ave2[index_d + 1, j + 1, i + 1]):
                    a = s_ave2[index_d, j + 1, i + 1]
                    b = s_ave2[index_d + 1, j + 1, i + 1]
                    if Ad == s_ave2[index_d, j + 1, i + 1] or s_ave2[0, j + 1, i + 1] == s_ave2[M, j + 1, i + 1]:
                        Cd = call2[index_d, j + 1, i + 1]
                        Cd_AM = AMcall2[index_d, j + 1, i + 1]
                        break
                    elif Ad == s_ave2[index_d + 1, j + 1, i + 1]:
                        Cd = call2[index_d + 1, j + 1, i + 1]
                        Cd_AM = AMcall2[index_d + 1, j + 1, i + 1]
                        break
                    elif Ad < s_ave2[M, j + 1, i + 1]:
                        Cd = call2[M, j + 1, i + 1]
                        Cd_AM = AMcall2[M, j + 1, i + 1]
                        break
                    elif Ad > s_ave2[0, j + 1, i + 1]:
                        Cd = call2[0, j + 1, i + 1]
                        Cd_AM = AMcall2[0, j + 1, i + 1]
                        break
                    elif Ad > s_ave2[index_d, j + 1, i + 1]:
                        upper_d = index_d
                    else:
                        lower_d = index_d

                    index_d = int((lower_d + upper_d) / 2)
                    if lower_d == upper_d:
                        Cd = call2[index_d, j + 1, i + 1]
                        Cd_AM = AMcall2[index_d, j + 1, i + 1]
                        break

                if Ad < s_ave2[index_d, j + 1, i + 1] and Ad > s_ave2[index_d + 1, j + 1, i + 1]:
                    w = (s_ave2[index_d, j + 1, i + 1] - Ad) / (s_ave2[index_d, j + 1, i + 1] - s_ave2[index_d + 1, j + 1, i + 1])
                    Cd = w * call2[index_d + 1, j + 1, i + 1] + (1-w) * call2[index_d, j + 1, i + 1]
                    Cd_AM = w * AMcall2[index_d + 1, j + 1, i + 1] + (1 - w) * AMcall2[index_d, j + 1, i + 1]

                # get European call[k,j,i]
                call2[k, j, i] = (p * Cu + (1-p) * Cd) * exp(-R*dt)

                # get American call[k,j,i]
                payoff_if_HTM = (p * Cu_AM + (1-p) * Cd_AM) * exp(-R*dt)
                payoff_if_early_exercise = s_ave2[k, j, i] - K
                AMcall2[k, j, i] = max(payoff_if_HTM, payoff_if_early_exercise)
end2 = time.time()
# output
print("Binary search:")
print(str("European Arithmatic average call = ") + str(round(call2[0, 0, 0], 4)))
print(str("American Arithmatic average call = ") + str(round(AMcall2[0, 0, 0], 4)))
print(str("The time used to execute backward induction:") + str(end2 - start2))

# way3: linear interpolation
# step 1: payoff at maturity (build Save list)
# 三維矩陣：[層數 , row, column]
s_ave3 = np.zeros([M+1, n+1, n+1])
call3 = np.zeros([M+1, n+1, n+1])
AMcall3 = np.zeros([M+1, n+1, n+1])

for i in range(n + 1):      # i = col
    for j in range(n + 1):  # j = row
        if j <= i:          # since it's tree, we only care about upper-triangle
            Amax = (Save_t * ((t-0)/dt + 1) + St * (u * (1 - u ** (i - j)) / (1-u)) + St * ((u ** (i - j)) * d * (1-d**j)/(1-d))) / (i + (t-0)/dt + 1)
            Amin = (Save_t * ((t-0)/dt + 1) + St * (d * (1 - d ** j) / (1-d)) + St * ((d ** j) * u * (1 - u ** (i - j)) / (1-u))) / (i + (t-0)/dt + 1)
            for k in range(M + 1):
                s_ave3[k, j, i] = ((M - k)/M) * Amax + (k/M) * Amin
                if i == n:
                    call3[k, j, n] = max(s_ave3[k, j, i] - K, 0)
                    AMcall3[k, j, n] = max(s_ave3[k, j, i] - K, 0)

# step 2: backward induction
start3 = time.time()
for i in range(n - 1, -1, -1): # i = col counts for n-1, n-2,...,0
    for j in range(n + 1):     # j = row counts for 0, 1, ..., n
        if j <= i:             # since it's tree, we only care about upper-triangle
            for k in range(M + 1):
                Au = ((i + (t-0)/dt + 1) * s_ave3[k, j, i] + St * (u ** (i + 1 - j)) * (d ** j)) / (i + (t-0)/dt + 2)
                Ad = ((i + (t-0)/dt + 1) * s_ave3[k, j, i] + St * (u ** (i + 1 - (j+1))) * (d ** (j+1))) / (i + (t-0)/dt + 2)

                # find Au in s_ave[:, j, i + 1] >> linear interpolation get Cu
                if s_ave3[M, j, i + 1] != s_ave3[0, j, i + 1]:
                    ku = int(M * (s_ave3[0, j, i + 1] - Au) / (s_ave3[0, j, i + 1] - s_ave3[M, j, i + 1]))
                    if ku == M or Au <= s_ave3[M, j, i + 1]:
                        Cu = call3[M, j, i + 1]
                        Cu_AM = AMcall3[M, j, i + 1]
                    elif ku == 0 or Au >= s_ave3[0, j, i + 1]:
                        Cu = call3[0, j, i + 1]
                        Cu_AM = AMcall3[0, j, i + 1]
                    else:
                        w = (s_ave3[ku, j, i + 1] - Au) / (s_ave3[ku, j, i + 1] - s_ave3[ku + 1, j, i + 1])
                        Cu = w * call3[ku + 1, j, i + 1] + (1 - w) * call3[ku, j, i + 1]
                        Cu_AM = w * AMcall3[ku + 1, j, i + 1] + (1 - w) * AMcall3[ku, j, i + 1]
                else:
                    Cu = call3[M, j, i + 1]
                    Cu_AM = AMcall3[M, j, i + 1]

                # find Ad in s_ave[:, j + 1, i + 1] >> linear interpolation get Cd
                if s_ave3[M, j + 1, i + 1] != s_ave3[0, j + 1, i + 1]:
                    kd = int(M * (s_ave3[0, j + 1, i + 1] - Ad) / (s_ave3[0, j + 1, i + 1] - s_ave3[M, j + 1, i + 1]))
                    if kd == M or Ad <= s_ave3[M, j + 1, i + 1]:
                        Cd = call3[M, j + 1, i + 1]
                        Cd_AM = AMcall3[M, j + 1, i + 1]
                    elif kd == 0 or Ad >= s_ave3[0, j + 1, i + 1]:
                        Cd = call3[0, j + 1, i + 1]
                        Cd_AM = AMcall3[0, j + 1, i + 1]
                    else:
                        w = (s_ave3[kd, j + 1, i + 1] - Ad) / (s_ave3[kd, j + 1, i + 1] - s_ave3[kd + 1, j + 1, i + 1])
                        Cd = w * call3[kd + 1, j + 1, i + 1] + (1-w) * call3[kd, j + 1, i + 1]
                        Cd_AM = w * AMcall3[kd + 1, j + 1, i + 1] + (1 - w) * AMcall3[kd, j + 1, i + 1]
                else:
                    Cd = call3[M, j + 1, i + 1]
                    Cd_AM = AMcall3[M, j + 1, i + 1]

                # get European call[k,j,i]
                call3[k, j, i] = (p * Cu + (1-p) * Cd) * exp(-R*dt)

                # get American call[k,j,i]
                payoff_if_HTM = (p * Cu_AM + (1-p) * Cd_AM) * exp(-R*dt)
                payoff_if_early_exercise = s_ave3[k, j, i] - K
                AMcall3[k, j, i] = max(payoff_if_HTM, payoff_if_early_exercise)
end3 = time.time()
# output
print("Linear interpolation:")
print(str("European Arithmatic average call = ") + str(round(call3[0, 0, 0], 4)))
print(str("American Arithmatic average call = ") + str(round(AMcall3[0, 0, 0], 4)))
print(str("The time used to execute backward induction:") + str(end3 - start3))
