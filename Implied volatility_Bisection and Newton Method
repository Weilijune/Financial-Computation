# calculate implied volatility
from scipy.stats import norm
import numpy as np
from numpy.random import normal
from math import log, sqrt, exp

def d1(S,K,T,r,q,sigma):
    return (log(S / K)+(r - q + sigma**2 / 2.) * T)/(sigma * sqrt(T))

def d2(S,K,T,r,q,sigma):
    return (log(S / K)+(r - q - sigma**2 / 2.) * T)/(sigma * sqrt(T))

def bs_EURcall(S,K,T,r,q,sigma):
    return S*exp(-q*T)*norm.cdf(d1(S,K,T,r,q,sigma)) - K*exp(-r*T)*norm.cdf(d2(S,K,T,r,q,sigma))

def bs_EURput(S,K,T,r,q,sigma):
    return K*exp(-r*T)*norm.cdf(-1*d2(S,K,T,r,q,sigma)) - S*exp(-q*T)*norm.cdf(-1*d1(S,K,T,r,q,sigma))

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

def Bisection_BS(function, benchmark, mkt_p, S, K, T, r, q):
    # inital guess since the sigma is always between the 0-1...
    a = 0.001
    b = 3
    # 處理剛好猜到ＩＶ的情況
    if (function(S,K,T,r,q,a) - mkt_p) * (function(S,K,T,r,q,b) - mkt_p) == 0:
        if (function(S,K,T,r,q,a) - mkt_p) == 0:
            IV = a
        else:
            IV = b
    else:
        # 若挑選的上下界，並沒有包到正解（ｆ（ｘ）＝０）的部分，則繼續把上界加大，直到滿足條件
        while (function(S,K,T,r,q,a) - mkt_p) * (function(S,K,T,r,q,b) - mkt_p) > 0:
            b += 1
            a /= 10
        x = (a + b) / 2
        while (function(S,K,T,r,q,x) - mkt_p) > benchmark:
            if (function(S,K,T,r,q,x) - mkt_p) * (function(S,K,T,r,q,a) - mkt_p) > 0:
                a = x
            else:
                b = x
            x = (a + b) / 2
        IV = x
    return(IV)

def Bisection_CRR(function, benchmark, mkt_p, S, K, T, r, q, n):
    # inital guess since the sigma is always between the 0-1...
    a = 0.001
    b = 3
    # 處理剛好猜到ＩＶ的情況
    if (function(S,K,T,r,q,a,n) - mkt_p) * (function(S,K,T,r,q,b,n) - mkt_p) == 0:
        if (function(S,K,T,r,q,a,n) - mkt_p) == 0:
            IV = a
        else:
            IV = b
    else:
        # 若挑選的上下界，並沒有包到正解（ｆ（ｘ）＝０）的部分，則繼續把上界加大，直到滿足條件
        while (function(S,K,T,r,q,a,n) - mkt_p) * (function(S,K,T,r,q,b,n) - mkt_p) > 0:
            b += 1
            a /= 10
        x = (a + b) / 2
        while (function(S,K,T,r,q,x,n) - mkt_p) > benchmark:
            if (function(S,K,T,r,q,x,n) - mkt_p) * (function(S,K,T,r,q,a,n) - mkt_p) > 0:
                a = x
            else:
                b = x
            x = (a + b) / 2
        IV = x
    return(IV)

def Newton_BS(function, benchmark, mkt_p, S, K, T, r, q):
    # initial guess
    xn = 0.1
    # 處理剛好猜到ＩＶ的情況
    if (function(S, K, T, r, q, xn) - mkt_p) == 0:
        IV = xn
    else:
        # vega = f'(x); vega_call = vega_put for same K
        vega = exp(-q*T) * S * sqrt(T) * norm.pdf(d1(S,K,T,r,q,xn))
        x = xn - (function(S, K, T, r, q, xn) - mkt_p) / vega
        while abs(x - xn) > benchmark:
            xn = x
            vega = exp(-q * T) * S * sqrt(T) * norm.pdf(d1(S, K, T, r, q, xn))
            x = xn - (function(S, K, T, r, q, xn) - mkt_p) / vega
        IV = x
    return(IV)

def Newton_CRR(function, benchmark, mkt_p, S, K, T, r, q, n):
    # initial guess
    xn = 0.1
    # 處理剛好猜到ＩＶ的情況
    if (function(S, K, T, r, q, xn, n) - mkt_p) == 0:
        IV = xn
    else:
        # f'(x) = (CRR(sigma + h) - CRR(sigma))/h
        h = 10 ** (-8)
        diff = (function(S, K, T, r, q, xn + h, n) - function(S, K, T, r, q, xn, n)) / h
        x = xn - (function(S, K, T, r, q, xn, n) - mkt_p) / diff
        while abs(x - xn) > benchmark:
            xn = x
            diff = (function(S, K, T, r, q, xn + h, n) - function(S, K, T, r, q, xn, n)) / h
            x = xn - (function(S, K, T, r, q, xn, n) - mkt_p) / diff
        IV = x
    return(IV)

S0 = float(input("S0 = "))
K = float(input("K = "))
r = float(input("r = "))
q = float(input("q = "))
T = float(input("T = "))
mkt_price = float(input("market price of option = "))
n = int(input("time step (n) = "))
accuracy = float(input("convergence criterion = "))

IV_bscall_B = Bisection_BS(bs_EURcall, accuracy, mkt_price, S0, K, T, r, q)
IV_bsput_B = Bisection_BS(bs_EURput, accuracy, mkt_price, S0, K, T, r, q)
IV_CRR_eurcall_B = Bisection_CRR(CRR_EURcall, accuracy, mkt_price, S0, K, T, r, q, n)
IV_CRR_eurput_B= Bisection_CRR(CRR_EURput, accuracy, mkt_price, S0, K, T, r, q, n)
IV_CRR_amcall_B = Bisection_CRR(CRR_AMcall, accuracy, mkt_price, S0, K, T, r, q, n)
IV_CRR_amput_B = Bisection_CRR(CRR_AMput, accuracy, mkt_price, S0, K, T, r, q, n)

IV_bscall_N = Newton_BS(bs_EURcall, accuracy, mkt_price, S0, K, T, r, q)
IV_bsput_N = Newton_BS(bs_EURput, accuracy, mkt_price, S0, K, T, r, q)
IV_CRR_eurcall_N = Newton_CRR(CRR_EURcall, accuracy, mkt_price, S0, K, T, r, q, n)
IV_CRR_eurput_N= Newton_CRR(CRR_EURput, accuracy, mkt_price, S0, K, T, r, q, n)
IV_CRR_amcall_N = Newton_CRR(CRR_AMcall, accuracy, mkt_price, S0, K, T, r, q, n)
IV_CRR_amput_N = Newton_CRR(CRR_AMput, accuracy, mkt_price, S0, K, T, r, q, n)

print(str("Black Scholes/ EURcall / Bisection = ") + str(IV_bscall_B))
print(str("Black Scholes/ EURput / Bisection = ") + str(IV_bsput_B))
print("................................................................................")
print(str("CRR/ EURcall / Bisection = ") + str(IV_CRR_eurcall_B))
print(str("CRR/ EURput / Bisection = ") + str(IV_CRR_eurput_B))
print(str("CRR/ AMcall / Bisection = ") + str(IV_CRR_amcall_B))
print(str("CRR/ AMput / Bisection = ") + str(IV_CRR_amput_B))
print("................................................................................")
print(str("Black Scholes/ EURcall / Newton = ") + str(IV_bscall_N))
print(str("Black Scholes/ EURput / Newton = ") + str(IV_bsput_N))
print("................................................................................")
print(str("CRR/ EURcall / Newton = ") + str(IV_CRR_eurcall_N))
print(str("CRR/ EURput / Newton = ") + str(IV_CRR_eurput_N))
print(str("CRR/ AMcall / Newton = ") + str(IV_CRR_amcall_N))
print(str("CRR/ AMput / Newton = ") + str(IV_CRR_amput_N))
