# CRR binomial tree with one column vector> price the European and America(CRR) option
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
n = int(input("time_step (n) = "))


def CRR_EURcall(S,K,T,r,q,sigma,n):
    delta_t = T/n
    u = exp(sigma * sqrt(delta_t))
    d = exp(-1 * sigma * sqrt(delta_t))
    # prob_of_up
    p = (exp((r-q) * delta_t) - d)/(u - d)
    # Create a space
    option = np.zeros([n + 1, 1])

    # fill the last column: the payoff of call at maturity
    for i in range(n + 1):
        ST = S * (u**(n-i)) * (d ** i)
        option[i, 0] = max(ST - K, 0)

    # backward induction
    for i in range(n):
        # 由於python由零開始計算，故要再減掉1；而由於是由右往左(往回解)，故不是先處理i=0；而是(n-1)-i
        # 這邊由於是用 1 column vector 故col只用來作為制止while loop的功用
        col = (n - 1) - i
        j = 0
        while j <= col:
            option[j, 0] = exp(-r*delta_t)*(p * option[j, 0] + (1-p) * option[j+1, 0])
            j += 1

    CRR_price = option[0,0]
    return(CRR_price)


def CRR_EURput(S,K,T,r,q,sigma,n):
    delta_t = T/n
    u = exp(sigma * sqrt(delta_t))
    d = exp(-1 * sigma * sqrt(delta_t))
    # prob_of_up
    p = (exp((r-q) * delta_t) - d)/(u - d)
    # Create a space
    option = np.zeros([n + 1, 1])

    # fill the last column: the payoff of put at maturity
    for i in range(n + 1):
        ST = S * (u**(n - i)) * (d ** i)
        option[i, 0] = max(K - ST, 0)

    # backward induction
    for i in range(n):
        # 由於python由零開始計算，故要再減掉1；而由於是由右往左(往回解)，故不是先處理i=0；而是(n-1)-i
        # 這邊由於是用 1 column vector 故col只用來作為制止while loop的功用
        col = (n - 1) - i
        j = 0
        while j <= col:
            option[j, 0] = exp(-r*delta_t)*(p * option[j, 0] + (1-p) * option[j+1, 0])
            j += 1

    CRR_price = option[0,0]
    return(CRR_price)


def CRR_AMcall(S, K, T, r, q, sigma, n):
    delta_t = T / n
    u = exp(sigma * sqrt(delta_t))
    d = exp(-1 * sigma * sqrt(delta_t))
    # prob_of_up
    p = (exp((r - q) * delta_t) - d) / (u - d)
    # Create a space
    option = np.zeros([n + 1, 1])

    # fill the last column: the payoff of call at maturity
    for i in range(n + 1):
        ST = S * (u ** (n - i)) * (d ** i)
        option[i, 0] = max(ST - K, 0)

    # backward induction
    for i in range(n):
        # 由於python由零開始計算，故要再減掉1；而由於是由右往左(往回解)，故不是先處理i=0的欄位；而是(n-1)-i的欄位
        col = (n - 1) - i
        j = 0
        while j <= col:
            # decide whether keep holding to maturity is better or early exercise is better one?
            price_if_HTM = exp(-r * delta_t) * (p * option[j, 0] + (1 - p) * option[j + 1, 0])
            St = S * (u ** (col - j)) * (d ** j)
            price_if_early_exercise = max(St - K, 0)
            if price_if_early_exercise >= price_if_HTM:
                option[j, 0] = price_if_early_exercise
            else:
                option[j, 0] = price_if_HTM
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
    option = np.zeros([n + 1, 1])

    # fill the last column: the payoff of put at maturity
    for i in range(n + 1):
        ST = S * (u ** (n - i)) * (d ** i)
        option[i, 0] = max(K - ST, 0)

    # backward induction
    for i in range(n):
        # 由於python由零開始計算，故要再減掉1；而由於是由右往左(往回解)，故不是先處理i=0的欄位；而是(n-1)-i的欄位
        col = (n - 1) - i
        j = 0
        while j <= col:
            # decide whether keep holding to maturity is better or early exercise is better one?
            price_if_HTM = exp(-r * delta_t) * (p * option[j, 0] + (1 - p) * option[j + 1, 0])
            St = S * (u ** (col - j)) * (d ** j)
            price_if_early_exercise = max(K - St, 0)
            if price_if_early_exercise >= price_if_HTM:
                option[j, 0] = price_if_early_exercise
            else:
                option[j, 0] = price_if_HTM
            j += 1

    CRR_price = option[0, 0]
    return (CRR_price)

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
