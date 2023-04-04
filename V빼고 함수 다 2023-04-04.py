"""
Psychrometric property calculation
ed. 2022-09-26
    T, R, Ps, W, H, V, B, D
    주의 사항 : 모든것 대분자 사용
"""

import numpy as np
# from CoolProp.CoolProp import PropsSI
from scipy.optimize import fsolve

# 열역학 교과서 예제 14-3

t = 25 # [℃]
b = 15
K = 273.15 # [K]
T = t + K # [℃]
B = b + K
P = 101325 # [Pa]
W = 0.00653 # [kg/kg']
R = 0.332
D = 7.72
H = 4.175e4
V = 0.8533

def secant(fun, x1, tol=1.0e-6, kmax=100):
    """ root finding f(x) = 0 by secant method """
    x2 = 1.1 * x1
    f1, f2 = fun(x1), fun(x2)
    for k in range(kmax):
        x3 = x2 - f2 * (x1 - x2) / (f1 - f2)
        f3 = fun(x3)
        if abs(x1 - x3) < tol * max(1.0, abs(x3)):
            return x3
        x1, f1 = x2, f2
        x2, f2 = x3, f3


def Psat_water(T):
    """
    saturation pressure over liquid water 0 to 200 C
    T = absolute temperature, K
    Psat = saturation pressure, Pa
    """
    C = np.array([-5.8002206e3, 1.3914993, -4.8640239e-2,
                  4.1764768e-5, -1.4452093e-8, 6.5459673])
    x = np.array([1 / T, 1, T, T ** 2, T ** 3, np.log(T)])
    Psat = np.exp(np.dot(C, x))
    return Psat


def hg_sat(T):
    """enthalpy of saturated water vapor at T (K)"""
    t = T - K
    hg = (2501 + 1.805 * t) * 1000
    return hg


def Ps_TR(T, R, P=101325):
    """partial pressure of water vapor"""
    # Psat = PropsSI('P', 'T', T, 'Q', 0, 'water')
    Psat = Psat_water(T)
    Ps = R * Psat
    return Ps

# TR
def W_TR(T, R, P=101325):
    """specific humidity"""
    # Ra, Rs = 287.055, 461.520  # gas constant of air and water vapor
    Ps = Ps_TR(T, R, P)
    W = 0.62198 * Ps / (P - Ps)
    return W


def H_TR(T, R, P=101325):
    """enthalpy"""
    W = W_TR(T, R, P)
    t = T - K
    ha = 1006 * t
    hg = hg_sat(T)  # (2501 + 1.805*t)*1000
    h = ha + W * hg
    return h


def V_TR(T, R, P=101325):
    """specific volume"""
    Ra = 287
    Ps = Ps_TR(T, R, P)
    v = Ra * T / (P - Ps)
    return v


def B_TR(T, R, P=101325):
    """ wet-bulb temperature """
    h1 = H_TR(T, R, P)
    W1 = W_TR(T, R, P)

    def fun(B):
        # hf = PropsSI('H', 'T', B, 'Q', 0, 'water')
        hf = 4186.0 * (B - K)
        h2 = H_TR(B, 1, P)
        W2 = W_TR(B, 1, P)
        h11 = h2 - (W2 - W1) * hf
        return h1 - h11

    B = secant(fun, T)
    return B


def D_TR(T, R, P=101325):
    """ dew-point temperature """
    W = W_TR(T, R, P)

    def fun(D):
        return W_TR(D, 1, P) - W

    D0 = T - (1 - R) / 0.05
    D = secant(fun, D0)
    return D

# TB
def R_TB(T, B, P=101325):
    return secant(lambda R: B_TR(T, R, P) - B, 0.8)

def H_TB(T, B):
    R = R_TB(T, B)
    H = H_TR(T, R)

    return H

def D_TB(T, B):
    R = R_TB(T, B)
    D = D_TR(T, R)

    return D

def W_TB(T, B):
    R = R_TB(T, B)
    W = W_TR(T, R)

    return  W

def V_TB(T, B):
    R = R_TB(T, B)
    V = V_TR(T, R)

    return V

# TH
def R_TH(T, H, P=101325):
    return secant(lambda R: H_TR(T, R, P) - H, 0.8)

def B_TH(T, H):
    R = R_TH(T, H)
    B = B_TR(T, R)

    return B

def D_TH(T, H):
    R = R_TH(T, H)
    D = D_TR(T, R)

    return D

def W_TH(T, H):
    R = R_TH(T, H)
    W = W_TR(T, R)

    return W

def V_TH(T, H):
    R = R_TH(T, H)
    V = V_TR(T, R)

    return V

# TD
def R_TD(T, D, P=101325):
    return secant(lambda R: D_TR(T, R, P) - D, 0.8)

def B_TD(T, D):
    R = R_TD(T, D)
    B = B_TR(T,R)

    return B

def H_TD(T, D):
    R = R_TD(T, D)
    H = H_TR(T, R)

    return H

def W_TD(T,D):
    R = R_TD(T, D)
    W = W_TR(T, R)

    return W

def V_TD(T,D):
    R = R_TD(T, D)
    V = V_TR(T, R)

    return V

# TW
def R_TW(T, W, P=101325):
    return secant(lambda R: W_TR(T, R, P) - W, 0.8)

def B_TW(T, W):
    R = R_TW(T, W)
    B = B_TR(T, R)

    return B

def H_TW(T,W):
    R = R_TW(T, W)
    H = H_TR(T, R)

    return H

def D_TW(T,W):
    R = R_TW(T, W)
    D = D_TR(T, R)

    return D

def V_TW(T,W):
    R = R_TW(T, W)
    V = V_TR(T, R)

    return V

# RB
def T_RB(R, B, P=101325):
    return secant(lambda T: B_TR(T, R, P) - B, 0.8)

def H_RB(R, B):
    T = T_RB(R, B)
    H = H_TR(T, R)

    return H

def D_RB(R, B):
    T = T_RB(R, B)
    D = D_TR(T, R)

    return D

def W_RB(R, B):
    T = T_RB(R, B)
    W = W_TR(T, R)

    return W

def V_RB(R, B):
    T = T_RB(R, B)
    V = V_TR(T, R)

    return V

# RH
def T_RH(R, H, P=101325):
    return secant(lambda T: H_TR(T, R, P) - H, 0.8)

def B_RH(R, H):
    T = T_RH(R, H)
    B = B_TR(T, R)

    return B

def D_RH(R, H):
    T = T_RH(R, H)
    D = D_TR(T, R)

    return D

def W_RH(R, H):
    T = T_RH(R, H)
    W = W_TR(T, R)

    return W

def V_RH(R, H):
    T = T_RH(R, H)
    V = V_TR(T, R)

    return V

# RD
def T_RD(R, D, P=101325):
    return secant(lambda T: D_TR(T, R, P) - D, 10)

def B_RD(R, D):
    T = T_RD(R, D)
    B = B_TR(T, R)

    return B

def H_RD(R, D):
    T = T_RD(R, D)
    H = H_TR(T, R)

    return H

def W_RD(R, D):
    T = T_RD(R, D)
    W = W_TR(T, R)

    return W

def V_RD(R,D):
    T = T_RD(R, D)
    V = V_TR(T, R)

    return V

# BD
def TR_BD(B, D, T0=25 + K, R0=0.6):
    def fun(x):
        T, R = x
        BB = B_TR(T, R)
        DD = D_TR(T, R)
        return [B - BB, D - DD]

    T, R = fsolve(fun, [T0, R0])
    return T, R

def T_BD(B, D):
    T, R = TR_BD(B,D)

    return T

def R_BD(B, D):
    T, R = TR_BD(B, D)

    return R

def H_BD(B, D):
    T, R = TR_BD(B, D)
    H = H_TR(T, R)

    return H

def W_BD(B,D):
    T, R = TR_BD(B, D)
    W = W_TR(T, R)

    return W

def V_BD(B, D):
    T, R = TR_BD(B, D)
    V = V_TR(T, R)

    return V

# BW
def TR_BW(B, W, T0=25 + K, R0=0.6):
    def fun(x):
        T, R = x
        BB = B_TR(T, R)
        WW = W_TR(T, R)
        return [B - BB, W - WW]

    T, R = fsolve(fun, [T0, R0])
    return T, R

def T_BW(B,W):
    T, R = TR_BW(B, W)

    return T

def R_BW(B,W):
    T, R = TR_BW(B, W)

    return R

def H_BW(B, W):
    T, R = TR_BW(B, W)
    H = H_TR(T, R)

    return H

def D_BW(B,W):
    T, R = TR_BW(B, W)
    D = D_TR(T,R)

    return D

def V_BW(B,W):
    T, R = TR_BW(B, W)
    V = V_TR(T, R)

    return V

# HD
def TR_HD(H, D, T0=25 + K, R0=0.6):
    def fun(x):
        T, R = x
        hh = H_TR(T, R)
        DD = D_TR(T, R)
        return [H - hh, D - DD]

    T, R = fsolve(fun, [T0, R0])
    return T, R

def T_HD(H, D):
    T, R = TR_HD(H, D)

    return T


def R_HD(H, D):
    T, R = TR_HD(H, D)

    return R

def B_HD(H, D):
    T, R = TR_HD(H, D)
    B = B_TR(T, R)

    return B

def W_HD(H, D):
    T, R = TR_HD(H, D)
    W = W_TR(T, R)

    return W

def V_HD(H,D):
    T, R = TR_HD(H, D)
    V = V_TR(T, R)

    return V

# HW
def TR_HW(H, W, T0=25 + K, R0=0.6):
    def fun(x):
        T, R = x
        hh = H_TR(T, R)
        WW = W_TR(T, R)
        return [H - hh, W - WW]

    T, R = fsolve(fun, [T0, R0])
    return T, R

def T_HW(H,W):
    T, R = TR_HW(H, W)

    return T

def R_HW(H,W):
    T, R = TR_HW(H, W)

    return R

def B_HW(H, W):
    T, R = TR_HW(H, W)
    B = B_TR(T, R)

    return B

def D_HW(H, W):
    T, R = TR_HW(H, W)
    D = D_TR(T, R)

    return D

def V_HW(H, W):
    T, R = TR_HW(H, W)
    V = V_TR(T, R)

    return V


## T_RB로 변경함
# def T_BR(B, R, P=101325):
#     return secant(lambda T: B_TR(T, R, P) - B, 0.8)

# # T_RH로 변경함
# def T_HR(H, R, P=101325):
#     return secant(lambda T: H_TR(T, R, P) - H, 0.8)

# # T_RD로 변경함
# def T_DR(D, R, P=101325):
#     return secant(lambda T: D_TR(T, R, P) - D, 10)


# BD
if __name__ == "__main__":
    K = 273.15
    P = 101325

    B = 15+K
    D = 7.72+K

    T = T_BD(B, D)
    R = R_BD(B, D)
    Ps = Ps_TR(T, R, P)
    V = V_TR(T, R, P)
    W = W_TR(T,R,P)
    H = H_TR(T,R,P)

    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'H', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))

# TB
if __name__ == "__main__":
    K = 273.15
    P = 101325

    T = 25 + K
    B = 15 + K

    R = R_TB(T,B,P)
    W = W_TR(T, R, P)
    Ps = Ps_TR(T, R, P)
    H = H_TR(T, R, P)
    V = V_TR(T, R, P)
    D = D_TR(T, R, P)

    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))

# TH

if __name__ == "__main__":
    K = 273.15
    P = 101325

    T = 25 + K
    H = 41760

    R= R_TH(T,H,P)
    W = W_TR(T, R, P)
    Ps = Ps_TR(T, R, P)
    V = V_TR(T, R, P)
    D = D_TR(T, R, P)
    B = B_TR(T,R,P)

    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))

# TD
if __name__ == "__main__":
    K = 273.15
    P = 101325

    T = 25 + K
    D = 7.73 + K

    R= R_TD(T, D, P)
    W = W_TR(T, R, P)
    Ps = Ps_TR(T, R, P)
    V = V_TR(T, R, P)
    B = B_TR(T,R,P)
    H = H_TR(T,R,P)

    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))

# TR

if __name__ == "__main__":
    K = 273.15
    P = 101325

    T = 25 + K
    R = 0.332

    Ps = Ps_TR(T, R, P)
    W = W_TR(T, R, P)
    h = H_TR(T, R, P)
    v = V_TR(T, R, P)
    B = B_TR(T, R, P)
    D = D_TR(T, R, P)

    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, h, v, B - K, D - K))

# TW

if __name__ == "__main__":
    K = 273.15
    P = 101325

    T = 25 + K
    W = 0.006533

    R= R_TW(T,W,P)
    Ps = Ps_TR(T, R, P)
    V = V_TR(T, R, P)
    B = B_TR(T,R,P)
    D= D_TR(T,R,P)
    H = H_TR(T,R,P)

    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))

# BD

if __name__ == "__main__":
    K = 273.15
    P = 101325

    B = 15+K
    D = 7.72+K

    T = T_BD(B, D)
    R = R_BD(B, D)
    Ps = Ps_TR(T, R, P)
    V = V_TR(T, R, P)
    W = W_TR(T,R,P)
    H = H_TR(T,R,P)

    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))

# BR

if __name__ == "__main__":
    K = 273.15
    P = 101325

    B = 15+K
    R = 0.3316

    T = T_RB(R,B,P)
    Ps = Ps_TR(T, R, P)
    V = V_TR(T, R, P)
    W = W_TR(T,R,P)
    D = D_TR(T,R,P)
    H = H_TR(T,R,P)

    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))

# BW

if __name__ == "__main__":
    K = 273.15
    P = 101325

    B = 15+K
    W = 0.00652

    T = T_BW(B, W)
    R = R_BW(B, W)
    Ps = Ps_TR(T, R, P)
    V = V_TR(T, R, P)
    D = D_TR(T,R,P)
    H = H_TR(T,R,P)

    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))

# HD

if __name__ == "__main__":
    K = 273.15
    P = 101325

    H = 41760
    D = 7.72+K

    T = T_HD(H, D)
    R = R_HD(H, D)
    Ps = Ps_TR(T, R, P)
    V = V_TR(T, R, P)
    W = W_TR(T,R,P)
    B = B_TR(T,R,P)


    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))

# HR

if __name__ == "__main__":
    K = 273.15
    P = 101325

    H = 41760
    R = 0.332

    T= T_RH(R,H,P)
    Ps = Ps_TR(T, R, P)
    V = V_TR(T, R, P)
    W = W_TR(T,R,P)
    B = B_TR(T,R,P)
    D = D_TR(T,R,P)


    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))

# HW

if __name__ == "__main__":
    K = 273.15
    P = 101325

    H = 41760
    W = 0.00652

    T = T_HW(H, W)
    R= R_HW(H, W)
    Ps = Ps_TR(T, R, P)
    V = V_TR(T, R, P)
    B = B_TR(T,R,P)
    D= D_TR(T,R,P)

    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))

