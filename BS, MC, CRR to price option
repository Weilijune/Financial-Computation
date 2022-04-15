# BS、Monte Carlo、CRR binomial tree > price the European and America(CRR) option
from scipy.stats import norm
import numpy as np
from numpy.random import normal
from math import log, sqrt, exp

S0 = float(input("S0 = "))
K = float(input("K = "))
r = float(input("r = "))
q = float(input("q = "))
sigma = float(input("sigma = "))
T = float(input("T = "))
num_sim = int(input("num_of_simulation = "))
num_rep = int(input("num_of_repetition = "))
n = int(input("time_step (n) = "))

def d1(S,K,T,r,q,sigma):
    return (log(S / K)+(r - q + sigma**2 / 2.) * T)/(sigma * sqrt(T))

def d2(S,K,T,r,q,sigma):
    return (log(S / K)+(r - q - sigma**2 / 2.) * T)/(sigma * sqrt(T))

def bs_EURcall(S,K,T,r,q,sigma):
    return S*exp(-q*T)*norm.cdf(d1(S,K,T,r,q,sigma)) - K*exp(-r*T)*norm.cdf(d2(S,K,T,r,q,sigma))

def bs_EURput(S,K,T,r,q,sigma):
    return K*exp(-r*T)*norm.cdf(-1*d2(S,K,T,r,q,sigma)) - S*exp(-q*T)*norm.cdf(-1*d1(S,K,T,r,q,sigma))

def MC_EURcall(S,K,T,r,q,sigma,num_sim, num_rep):
    simulated_price = []
    for simulation in range(num_rep):
        payoff = []
        rand = normal(0, 1, size= num_sim)
        for i in range(len(rand)):
            ln_ST = (log(S0) + (r - q - sigma ** 2 / 2.) * T) + sigma * sqrt(T) * rand[i]
            ST = exp(ln_ST)
            payoff_at_T = 0
            if ST >= K:
                payoff_at_T = ST - K
            else:
                payoff_at_T = 0
            payoff.append(payoff_at_T)
        price = exp(-r * T) * np.array(payoff).mean()
        simulated_price.append(price)
    upper_bound = np.array(simulated_price).mean() + 2 * np.array(simulated_price).std()
    lower_bound = np.array(simulated_price).mean() - 2 * np.array(simulated_price).std()
    return(upper_bound, lower_bound)

def MC_EURput(S,K,T,r,q,sigma,num_sim, num_rep):
    simulated_price = []
    for simulation in range(num_rep):
        payoff = []
        rand = normal(0, 1, size= num_sim)

        for i in range(len(rand)):
            ln_ST = (log(S0) + (r - q - sigma ** 2 / 2.) * T) + sigma * sqrt(T) * rand[i]
            ST = exp(ln_ST)
            payoff_at_T = 0
            if ST >= K:
                payoff_at_T = 0
            else:
                payoff_at_T = K - ST
            payoff.append(payoff_at_T)
        price = exp(-r * T) * np.array(payoff).mean()
        simulated_price.append(price)

    upper_bound = np.array(simulated_price).mean() + 2 * np.array(simulated_price).std()
    lower_bound = np.array(simulated_price).mean() - 2 * np.array(simulated_price).std()
    return(upper_bound, lower_bound)

def CRR_EURcall(S,K,T,r,q,sigma,n):
    delta_t = T/n
    u = exp(sigma * sqrt(delta_t))
    d = exp(-1 * sigma * sqrt(delta_t))
    # prob_of_up
    p = (exp((r-q) * delta_t) - d)/(u - d)
    # Create a space；Ｎ＋１是因時間被切成n等分，由第ｎ期　倒推回　第０期　求出價格，故由０～ｎ共需要ｎ＋１的格子
    option = np.zeros([n + 1, n + 1])

    # fill the last column: the payoff of call at maturity
    for i in range(n + 1):
        ST = S * (u**(n - i)) * (d ** i)
        option[i, n] = max(ST - K, 0)

    # backward induction (已經處理完最後一欄；故迴圈次數只剩n)
    for i in range(n):
        # 由於python由零開始計算，故要再減掉1；而由於是由右往左(往回解)，故不是先處理i=0的欄位；而是(n-1)-i的欄位
        col = n - 1 - i
        j = 0
        while j <= col:
            option[j, col] = exp(-r*delta_t)*(p * option[j, col+1] + (1-p) * option[j+1, col+1])
            j += 1

    CRR_price = option[0,0]
    return(CRR_price)


def CRR_EURput(S, K, T, r, q, sigma, n):
    delta_t = T / n
    u = exp(sigma * sqrt(delta_t))
    d = exp(-1 * sigma * sqrt(delta_t))
    # prob_of_up
    p = (exp((r - q) * delta_t) - d) / (u - d)
    # Create a space
    option = np.zeros([n + 1, n + 1])

    # fill the last column: the payoff of put at maturity
    for i in range(n + 1):
        ST = S * (u ** (n - i)) * (d ** i)
        option[i, n] = max(K - ST, 0)

    # backward induction (已經處理完最後一欄；故迴圈次數只剩n)
    for i in range(n):
        # 由於python由零開始計算，故要再減掉1；而由於是由右往左(往回解)，故不是先處理i=0的欄位；而是(n-1)-i的欄位
        col = n - 1 - i
        j = 0
        while j <= col:
            option[j, col] = exp(-r * delta_t) * (p * option[j, col + 1] + (1 - p) * option[j + 1, col + 1])
            j += 1

    CRR_price = option[0, 0]
    return (CRR_price)


def CRR_AMcall(S, K, T, r, q, sigma, n):
    delta_t = T / n
    u = exp(sigma * sqrt(delta_t))
    d = exp(-1 * sigma * sqrt(delta_t))
    # prob_of_up
    p = (exp((r - q) * delta_t) - d) / (u - d)
    # Create a space
    option = np.zeros([n + 1, n + 1])

    # fill the last column: the payoff of call at maturity
    for i in range(n + 1):
        ST = S * (u ** (n - i)) * (d ** i)
        option[i, n] = max(ST - K, 0)

    # backward induction (已經處理完最後一欄；故迴圈次數只剩n)
    for i in range(n):
        # 由於python由零開始計算，故要再減掉1；而由於是由右往左(往回解)，故不是先處理i=0的欄位；而是(n-1)-i的欄位
        col = (n - 1) - i
        j = 0
        while j <= col:
            # decide whether keep holding to maturity is better or early exercise is better one?
            price_if_HTM = exp(-r * delta_t) * (p * option[j, col + 1] + (1 - p) * option[j + 1, col + 1])
            St = S * (u ** (col - j)) * (d ** j)
            price_if_early_exercise = max(St - K, 0)
            if price_if_early_exercise >= price_if_HTM:
                option[j, col] = price_if_early_exercise
            else:
                option[j, col] = price_if_HTM
            j += 1

    CRR_price = option[0, 0]
    return (CRR_price)

def CRR_AMput(S, K, T, r, q, sigma, n):
    delta_t = T / n
    u = exp(sigma * sqrt(delta_t))
    d = exp(-1 * sigma * sqrt(delta_t))
    # prob_of_up
    p = (exp((r - q) * delta_t) - d) / (u - d)
    # Create a space
    option = np.zeros([n + 1, n + 1])

    # fill the last column: the payoff of put at maturity
    for i in range(n + 1):
        ST = S * (u ** (n - i)) * (d ** i)
        option[i, n] = max(K - ST, 0)

    # backward induction (已經處理完最後一欄；故迴圈次數只剩n)
    for i in range(n):
        # 由於python由零開始計算，故要再減掉1；而由於是由右往左(往回解)，故不是先處理i=0的欄位；而是(n-1)-i的欄位
        col = (n - 1) - i
        j = 0
        while j <= col:
            # decide whether keep holding to maturity is better or early exercise is better one?
            price_if_HTM = exp(-r * delta_t) * (p * option[j, col + 1] + (1 - p) * option[j + 1, col + 1])
            St = S * (u ** (col - j)) * (d ** j)
            price_if_early_exercise = max(K - St, 0)
            if price_if_early_exercise >= price_if_HTM:
                option[j, col] = price_if_early_exercise
            else:
                option[j, col] = price_if_HTM
            j += 1

    CRR_price = option[0, 0]
    return (CRR_price)

BS_call = bs_EURcall(S0,K,T,r,q,sigma)
BS_put = bs_EURput(S0,K,T,r,q,sigma)
print(str("Black Scholes call price = ") + str(BS_call))
print(str("Black Scholes put price = ") + str(BS_put))
print("................................................................................")

MC_call_ub, MC_call_lb = MC_EURcall(S0,K,T,r,q,sigma, num_sim, num_rep)
MC_put_ub, MC_put_lb = MC_EURput(S0,K,T,r,q,sigma, num_sim, num_rep)
print(str("95% CI for European call = [") + str(MC_call_lb) + str(", ") + str(MC_call_ub) + str("]"))
print(str("95% CI for European put = [") + str(MC_put_lb) + str(", ") + str(MC_put_ub) + str("]"))
print("................................................................................")

CRR_Ecall = CRR_EURcall(S0,K,T,r,q,sigma,n)
CRR_Eput = CRR_EURput(S0,K,T,r,q,sigma,n)
print(str("CRR european call price = ") + str(CRR_Ecall))
print(str("CRR european put price = ") + str(CRR_Eput))
print("................................................................................")

CRR_Acall = CRR_AMcall(S0,K,T,r,q,sigma,n)
CRR_Aput = CRR_AMput(S0,K,T,r,q,sigma,n)
print(str("CRR american call price = ") + str(CRR_Acall))
print(str("CRR american put price = ") + str(CRR_Aput))
print("................................................................................")
