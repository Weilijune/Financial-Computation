# least-square Monte Carlo simulation to price American option
# american vanilla put
import numpy as np
from numpy.random import normal
from math import log, sqrt, exp
import statsmodels.api as sm

# 給定參數
num_sim = 10000  # simulated 10000 paths
num_rep = 20     # conduct MC 20 times
S0 = 50
K = 50
r = 0.1
q = 0.05
sigma = 0.4
T = 0.5
n = 100       # time step

dt = T/n
simulated_price = []
for simulation in range(num_rep):
    print("running " + str(simulation + 1) + " times")
    # step 0: finish S path
    S_path = np.zeros([num_sim, n+1])
    S_path[:, 0] = S0
    # path dependent - record 10000 S(t+dt) value into S_path list
    for col in range(1, n+1):
        rand = normal(0, 1, size=num_sim)
        for row in range(num_sim):
            ln_St_dt = (log(S_path[row, col-1]) + (r - q - sigma ** 2 / 2.) * dt) + sigma * sqrt(dt) * rand[row]
            St_dt = exp(ln_St_dt)
            S_path[row, col] = St_dt

    # step 1: determine the payoff for each path at maturity
    payoff = np.zeros([num_sim, n + 1])
    for row in range(num_sim):
        payoff[row, n] = max(K - S_path[row, n], 0)

    # step 2-3: backward induction (只要backward到t=1的即可)
    for col in range(n - 1, 0, -1):
        EV = []
        HV = []
        ITM_row = []
        for row in range(num_sim):
            if K - S_path[row, col] > 0:  # In-the-money
                EV.append(K - S_path[row, col])
                HV.append(payoff[row, col + 1] * exp(-r*dt))
                ITM_row.append(row)
            else:
                payoff[row, col] = payoff[row, col + 1] * exp(-r*dt)  # Out-of-money

        # OLS
        y = np.array(HV)
        y = y.reshape(len(ITM_row), 1)
        num_regressor = 3
        regressor = np.ones([len(ITM_row), num_regressor])  # 3 regressors: constant, S, and S**2
        for index in range(len(ITM_row)):
            regressor[index, 1] = S_path[ITM_row[index], col]
            regressor[index, 2] = S_path[ITM_row[index], col] ** 2
        model = sm.OLS(y, regressor)
        results = model.fit()

        # HV >> expected HV (fitted value) and compare with EV
        for index in range(len(ITM_row)):
            #HV[index] = results.params[0] + results.params[1] * regressor[index, 1] + results.params[2] * regressor[index, 2]
            HV[index] = results.params[0]
            for j in range(1, num_regressor):
                HV[index] += results.params[j] * regressor[index, j]
            if HV[index] < EV[index]:
                payoff[ITM_row[index], col] = EV[index] # early exercise
            else:
                payoff[ITM_row[index], col] = payoff[ITM_row[index], col + 1] * exp(-r*dt)

    # step 4: option value at t = 0
    summ = 0
    for row in range(num_sim):
        summ += exp(-r*dt) * payoff[row, 1]
    price = max(summ/num_sim, K - S0)
    simulated_price.append(price)

MC_put_value = np.array(simulated_price).mean()
MC_put_ub = np.array(simulated_price).mean() + 2 * np.array(simulated_price).std()
MC_put_lb = np.array(simulated_price).mean() - 2 * np.array(simulated_price).std()

print(str("Monte Carlo American vanilla put price = ") + str(MC_put_value))
print(str("95% CI for American vanilla put = [") + str(MC_put_lb) + str(", ") + str(MC_put_ub) + str("]"))
