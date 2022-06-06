# least-square Monte Carlo simulation to price American option
# american arithmetic average call (asian call)

import numpy as np
from numpy.random import normal
from math import log, sqrt, exp
import statsmodels.api as sm

# 老師給定的參數
num_sim = 10000
num_rep = 20
St = 50
K = 50
r = 0.1
q = 0.05
sigma = 0.8
t = 0.25
T_t = 0.25
n = 100
Save_t = 50

dt = T_t/n
simulated_price = []
for simulation in range(num_rep):
    print("running " + str(simulation + 1) + " times")
    # step 0: finish S path
    S_path = np.zeros([num_sim, n+1])
    S_path[:, 0] = St
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
        # 把這一條路徑的s path加總，加上issue date~t期的平均(n次) > 除以總數 ((n+1) + (t-0)/dt)
        Save_T = (sum(S_path[row, :]) + Save_t * (t - 0) / dt) / ((n + 1) + (t - 0) / dt)
        payoff[row, n] = max(Save_T - K, 0)

    # step 2-3: backward induction(只要backward到t=1的即可)
    for col in range(n - 1, 0, -1):
        EV = []
        HV = []
        ITM_row = []
        for row in range(num_sim):
            # python算頭不算尾，因此smax是由0時點到今天這個col的時點的average
            Save = (sum(S_path[row, 0:col+1]) + Save_t * (t - 0) / dt) / ((col + 1) + (t - 0) / dt)
            if Save - K > 0:  # In-the-money
                EV.append(Save - K)
                HV.append(payoff[row, col + 1] * exp(-r*dt))
                ITM_row.append(row)
            else:
                payoff[row, col] = payoff[row, col + 1] * exp(-r*dt)  # Out-of-money

        # OLS
        y = np.array(HV)
        y = y.reshape(len(ITM_row), 1)
        num_regressor = 6
        regressor = np.ones([len(ITM_row), num_regressor])  # 6 regressors: constant, S, S**2, Save, Save**2, S*Save
        for index in range(len(ITM_row)):
            regressor[index, 1] = S_path[ITM_row[index], col]
            regressor[index, 2] = S_path[ITM_row[index], col] ** 2
            Save = (sum(S_path[ITM_row[index], 0:col+1]) + Save_t * (t - 0) / dt) / ((col + 1) + (t - 0) / dt)
            regressor[index, 3] = Save
            regressor[index, 4] = Save ** 2
            regressor[index, 5] = S_path[ITM_row[index], col] * Save

        model = sm.OLS(y, regressor)
        results = model.fit()

        # HV >> expected HV (fitted value) and compare with EV
        for index in range(len(ITM_row)):
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
    price = max(summ/num_sim, Save_t - K)
    simulated_price.append(price)

MC_value = np.array(simulated_price).mean()
MC_ub = np.array(simulated_price).mean() + 2 * np.array(simulated_price).std()
MC_lb = np.array(simulated_price).mean() - 2 * np.array(simulated_price).std()

print(str("Monte Carlo American arithmetic average call price = ") + str(MC_value))
print(str("95% CI for American arithmetic average call = [") + str(MC_lb) + str(", ") + str(MC_ub) + str("]"))
