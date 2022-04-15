# closed form solution for option strategy
# to create the option strategy, which shape like___/一一\___

from math import log, sqrt, exp
from scipy.stats import norm
import numpy as np
from numpy.random import normal

# np.random.seed(10)

S0 = float(input("S0 = "))
r = float(input("r = "))
q = float(input("q = "))
sigma = float(input("sigma = "))
T = float(input("T = "))
K1 = float(input("K1 = "))
K2 = float(input("K2 = "))
K3 = float(input("K3 = "))
K4 = float(input("K4 = "))

def d1(S,K,T,r,q,sigma):
    return(log(S / K)+(r - q + sigma**2 / 2.) * T)/(sigma * sqrt(T))
def d2(S,K,T,r,q,sigma):
    return(log(S / K)+(r - q - sigma**2 / 2.) * T)/(sigma * sqrt(T))
# def bs_call(S,K,T,r,q,sigma):
#     return S*exp(-q*T)*norm.cdf(d1(S,K,T,r,q,sigma))-K*exp(-r*T)*norm.cdf(d2(S,K,T,r,q,sigma))
#
# option_price = bs_call(S0,K1,T,r,q,sigma) - bs_call(S0,K2,T,r,q,sigma) - bs_call(S0,K3,T,r,q,sigma) + bs_call(S0,K4,T,r,q,sigma)

part1 = K1*exp(-r*T)*norm.cdf(-d2(S0,K1,T,r,q,sigma)) - S0*exp(-q*T)*norm.cdf(-d1(S0,K1,T,r,q,sigma))
part2 = K2*exp(-r*T)*norm.cdf(-d2(S0,K2,T,r,q,sigma)) - S0*exp(-q*T)*norm.cdf(-d1(S0,K2,T,r,q,sigma))
part3 = ((K2-K1)+((K2-K1)*K4/(K3-K4)))*exp(-r*T)*norm.cdf(-d2(S0,K3,T,r,q,sigma)) - ((K2-K1)/(K3-K4))*S0*exp(-q*T)*norm.cdf(-d1(S0,K3,T,r,q,sigma))
part4 = ((K2-K1)/(K3-K4))*(K4*exp(-r*T)*norm.cdf(-d2(S0,K4,T,r,q,sigma)) - S0*exp(-q*T)*norm.cdf(-d1(S0,K4,T,r,q,sigma)))
price = part1 - part2 + part3 - part4
# print(option_price)
print(str("Closed-form solution = ") + str(price))


## Monte Carlo simulation
simulated_price = []

for simulation in range(20):
    payoff = []
    rand = normal(0, 1, size = 10000)
    for i in range(len(rand)):
        ln_ST = (log(S0) + (r - q - sigma**2 / 2.) * T) + sigma * sqrt(T) * rand[i]
        ST = exp(ln_ST)
        payoff_at_T = 0
        if ST >= K1 and ST < K2:
            payoff_at_T = ST - K1
        elif ST >= K2 and ST < K3:
            payoff_at_T = K2 - K1
        elif ST >= K3 and ST < K4:
            payoff_at_T = ((K2 - K1)/(K3 - K4)) * (ST - K4)
        payoff.append(payoff_at_T)
    price = exp(-r* T) * np.array(payoff).mean()
    simulated_price.append(price)

upper_bound = np.array(simulated_price).mean() + 2 * np.array(simulated_price).std()
lower_bound = np.array(simulated_price).mean() - 2 * np.array(simulated_price).std()
print(str("95% CI for option value = [") + str(lower_bound) + str(", ") + str(upper_bound) + str("]"))
