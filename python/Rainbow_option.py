# Rainbow option pricing_MC
from scipy.stats import norm
import numpy as np
from numpy.random import normal
from math import log, sqrt, exp
import scipy.linalg as la

K = float(input("K = "))
r = float(input("r = "))
T = float(input("T = "))
num_sim = int(input("num_of_simulation = "))
num_rep = int(input("num_of_repetition = "))
n = int(input("num of assets = "))
s0 = []  # s0[0] = s0(1)... >> s0[i] = s0(i+1)
q = []   # q[i] = q(i+1)
sigma = []  # sigma[i] = sigma(i+1)

for i in range(n):
    si = float(input("S0 ("+str(i+1) + str(") = ")))
    s0.append(si)
for i in range(n):
    qi = float(input("q ("+str(i+1) + str(") = ")))
    q.append(qi)
for i in range(n):
    sigmai = float(input("Sigma ("+str(i+1) + str(") = ")))
    sigma.append(sigmai)

# Covariance matrix
C = np.ones([n, n])
# ex. n = 3 輸入順序是 corr(1,2) > corr(1,3) > corr(2,3)
for i in range(n):      # row
    for j in range(n):  # column
        C[i, j] *= T * sigma[i] * sigma[j]
        if j != 0 and i != n - 1 and i < j:
            corrij = float(input("Corr ("+str(i+1) + str(",") + str(j+1) + str(") = ")))
            C[i, j] *= corrij
            C[j, i] *= corrij
A = la.cholesky(C)

# Monte Carlo Simulation
simulated_call = []
simulated_put = []
for simulation in range(num_rep):
    rand = normal(0, 1, size=num_sim * n)
    z = rand.reshape((num_sim, n))

    ST_mat = np.dot(z, A) # ST matrix
    for j in range(n):
        for i in range(num_sim):
            ST_mat[i, j] += log(s0[j]) + (r - q[j] - sigma[j]**2 / 2.) * T
            ST_mat[i, j] = exp(ST_mat[i, j])

    payoff_call = []
    payoff_put = []
    for i in range(num_sim):
        ST = max(ST_mat[i, :])
        payoff_call_T = max(ST - K, 0)
        payoff_put_T = max(K - ST, 0)
        payoff_call.append(payoff_call_T)
        payoff_put.append(payoff_put_T)

    call_price = exp(-r * T) * np.array(payoff_call).mean()
    put_price = exp(-r * T) * np.array(payoff_put).mean()
    simulated_call.append(call_price)
    simulated_put.append(put_price)


Call = np.array(simulated_call).mean()
UB_call = np.array(simulated_call).mean() + 2 * np.array(simulated_call).std()
LB_call = np.array(simulated_call).mean() - 2 * np.array(simulated_call).std()

Put = np.array(simulated_put).mean()
UB_put = np.array(simulated_put).mean() + 2 * np.array(simulated_put).std()
LB_put = np.array(simulated_put).mean() - 2 * np.array(simulated_put).std()

print("Rainbow Call:")
print(str("1. rainbow call value = ") + str(Call))
print(str("2. 95% CI for call value = [") + str(LB_call) + str(", ") + str(UB_call) + str("]"))
print("Rainbow Put:")
print(str("1. rainbow put value = ") + str(Put))
print(str("2. 95% CI for put value = [") + str(LB_put) + str(", ") + str(UB_put) + str("]"))
