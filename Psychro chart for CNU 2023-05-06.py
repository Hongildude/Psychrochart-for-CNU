"""
Psychrometric property calculation
ed. 2022-09-26
    T, R, Ps, W, H, V, B, D
    주의 사항 : 모든것 대분자 사용
"""

import numpy as np
# from CoolProp.CoolProp import PropsSI
from scipy.optimize import fsolve

# 열역학 교과서 Table5 Saturated water - Pressure table
pressure_array = np.array([1e3, 1.5e3, 2e3, 2.5e3, 3e3, 4e3, 5e3, 7.5e3, 10e3, 15e3])
temperature_array = np.array([6.97, 13.02, 17.5, 21.08, 24.08, 28.96, 32.87, 40.29, 45.81, 53.97])

# 열역학 교과서 Table4 Saturated water - Temperature Table
pressure_array2 = np.array([0.6117, 0.8725, 1.2281, 1.7057, 2.3392, 3.1698, 4.2469, 5.6291, 7.3851, 9.5953, 12.352, 15.763, 19.947, 25.043, 31.202])
temperature_array2 = np.array([0.01, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70])

# 열역학 교과서 예제 14-3

K = 273.15
R = 0.332
t = 25 # [℃]
b = 15 # [℃]
d = 7.72 # [℃]
D = d + K # [K]
T = t + K # [K]
B = b + K # [K]
P = 101325 # [Pa]
W = 0.00653 # [kg/kg']
H = 4.175e4 # [J]
V = 0.8533 # [m3/kg]


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
    x = np.array([1 / T, 1, T, T ** 2, T ** 3, np.log(T)]) if T > 0 else np.array([1 / T, 1, T, T ** 2, T ** 3, 0])
    Psat = np.exp(np.dot(C, x))
    return Psat

def w1_TB(T,B):
    hg1 = hg_sat(T) # [J/kg]
    hf2 = 4186*(B - K) # [J/kg]
    hfg2 = hg_sat(B) - hf2 # [J/kg]
    w2_value = w2(B)

    w1 = (1005*(B-T) + w2_value*hfg2) / (hg1-hf2) # [kg/kg']
    return w1


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

def Ps_W(W):
    Ps = (W*P)/(W+0.622)

    return Ps

def D_W(W):
    Pv = (W*P)/(0.622+W)
    D = np.interp(Pv, pressure_array, temperature_array)

    return D + K

# (1) TR
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

def H_TR(T, R, P=101325):
    """enthalpy"""
    W = W_TR(T, R, P)
    ha = 1006 * (T - 273.15)
    hg = hg_sat(T)  # (2501 + 1.805*t)*1000
    h = ha + W * hg
    return h

def D_TR(T, R, P=101325):
    """ dew-point temperature """
    W = W_TR(T, R, P)

    def fun(D):
        return W_TR(D, 1, P) - W

    D0 = T - (1 - R) / 0.05
    D = secant(fun, D0)
    return D

def W_TR(T, R, P=101325):
    """specific humidity"""
    # Ra, Rs = 287.055, 461.520  # gas constant of air and water vapor
    Ps = Ps_TR(T, R, P)
    W = 0.62198 * Ps / (P - Ps)
    return W

def V_TR(T, R, P=101325):
    """specific volume"""
    Ra = 287
    Ps = Ps_TR(T, R, P)
    V = Ra * T / (P - Ps)
    return V

# (2) TB
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

# (3) TH
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

# (4) TD
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

# (5) TW
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

# (6) TV
def R_TV(T, V, P=101325):
    """Relative humidity given temperature and specific volume"""

    def fun(R):
        return V_TR(T, R, P) - V

    R0 = 0.6  # initial guess for relative humidity
    R = secant(fun, R0)
    return R

def B_TV(T, V):
    R = R_TV(T, V)
    B = B_TR(T, R)
    return B

def H_TV(T, V):
    R = R_TV(T, V)
    H = H_TR(T, R)
    return H

def D_TV(T, V, P=101325):
    R = R_TV(T, V)
    D = D_TR(T, R, P)
    return D

def W_TV(T, V, P=101325):
    R = R_TV(T, V)
    W = W_TR(T, R, P)
    return W

# (7) RB
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

# (8) RH
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

# (9) RD
def T_RD(R,D):
    Pv = Psat_water(D)
    Pgat = Pv/R # [Pa]
    Pgat = Pgat/1000 # [kPa]
    interpolated_temperature2 = np.interp(Pgat, pressure_array2, temperature_array2)

    return interpolated_temperature2 + K

def B_RD(R, D):
    T = T_RD(R, D)
    B = B_TR(T, R)

    return B

def H_RD(R,D):
    T = T_RD(R, D)
    H = H_TR(T, R)

    return H

def W_RD(R,D):
    T = T_RD(R, D)
    W = W_TR(T, R)

    return W

def V_RD(R,D):
    T = T_RD(R, D)
    V = V_TR(T, R)

    return V

# (10) RW
def T_RW(R, W):
    D = D_W(W)
    T = T_RD(R,D)

    return T

def B_RW(R, W):
    T = T_RW(R,W)
    B = B_RW(R,W)

    return B

def H_RW(R,W):
    T = T_RW(R,W)
    H = H_TR(T,R)

    return H

def D_RW(R,W):
    T = T_RW(R, W)
    D = D_TR(T, R)

    return D

def V_RW(R,W):
    T = T_RW(R, W)
    V = V_TR(T, R)

    return V

# (11) RV
def T_RV(R, V, P=101325, T0=25 + K):
    def fun(T):
        V_calc = V_TR(T, R)
        return V - V_calc

    T = secant(fun, T0)
    return T

def B_RV(R,V):
    T = T_RV(R, V)
    B = B_TR(T, R)

    return B

def H_RV(R,V):
    T = T_RV(R, V)
    H = H_TR(T, R)

    return H

def D_RV(R,V):
    T = T_RV(R, V)
    D = D_TR(T, R)

    return D

def W_RV(R,V):
    T = T_RV(R, V)
    W = W_TR(T, R)

    return W

# (12) BH
def TR_BH(B, H, T0=25 + K, R0=0.9, P=P):
    def fun(x):
        T, R = x
        R1 = R_TB(T, B)
        R2 = R_TH(T, H)
        return [R1- R, R2- R]

    T, R = fsolve(fun, [T0, R0])
    return T, R


def T_BH(B, H):
    T, R = TR_BH(B,H)

    return T

def R_BH(B, H):
    T, R = TR_BH(B, H)

    return R

def D_BH(B, H):
    T, R = TR_BH(B, H)
    D = D_TR(T, R)

    return D

def W_BH(B,H):
    T, R = TR_BH(B, H)
    W = W_TR(T, R)

    return W

def V_BH(B, H):
    T, R = TR_BH(B, H)
    V = V_TR(T, R)

    return V

# (13) BD
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

# (14) BW
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

# (15) BV
def TR_BV(B, V, T0=25 + K, R0=0.6):
    def fun(x):
        T, R = x
        BB = B_TR(T, R)
        VV = V_TR(T, R)
        return [B - BB, V - VV]

    T, R = fsolve(fun, [T0, R0])
    return T, R

def T_BV(B, V):
    T, R = TR_BV(B, V)
    return T

def R_BV(B, V):
    T, R = TR_BV(B, V)

    return R

def H_BV(B, V):
    T = T_BV(B, V)
    H = H_TR(T, R)

    return H

def D_BV(B, V):
    T = T_BV(B, V)
    D = D_TR(T, R)

    return D

def W_BV(B, V):
    T = T_BV(B, V)
    W = W_TR(T, R)

    return W

# (16) HD
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

# (17) HW
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

# (18) HV
def TR_HV(H, V, T0=25 + K, R0=0.6):
    def fun(x):
        T, R = x
        hh = H_TR(T, R)
        VV = V_TR(T, R)
        return [H - hh, V - VV]

    T, R = fsolve(fun, [T0, R0])

    return T, R

def T_HV(H, V):
    T, R = TR_HV(H, V)

    return T


def R_HV(H,V):
    T, R = TR_HV(H, V)

    return R

def B_HV(H,V):
    T, R = TR_HV(H, V)
    B = B_TR(T, R)

    return B

def D_HV(H,V):
    T, R = TR_HV(H, V)
    D = D_TR(T,R)

    return D

def W_HV(H, V):
    T, R = TR_HV(H, V)
    W = W_TR(T, R)

    return W

# (19) DW 불가능

# (20) DV
def TR_DV(D, V, T0=25 + K, R0=0.6):
    def fun(x):
        T, R = x
        dd = D_TR(T, R)
        VV = V_TR(T, R)
        return [D - dd, V - VV]

    T, R = fsolve(fun, [T0, R0])
    return T , R

def T_DV(D, V):
    T, R = TR_DV(D, V)

    return T

def R_DV(D, V):
    T, R = TR_DV(D, V)

    return R

def B_DV(D, V):
    T, R = TR_DV(D, V)
    B = B_TR(T, R)

    return B

def H_DV(D, V):
    T, R = TR_DV(D, V)
    H = H_TR(T, R)

    return H

def W_DV(D, V):
    T, R = TR_DV(D, V)
    W = W_TR(T, R)

    return W

# (21) WV
def T_WV(W, V):
    Ra = 287.055
    T = ((P - Ps_W(W)) * V) / Ra

    return T

def R_WV(W, V):
    T = T_WV(W,V)
    R = R_TW(T, W)

    return R

def B_WV(W,V):
    T = T_WV(W, V)
    B = B_TW(T, W)

    return B

def H_WV(W, V):
    T = T_WV(W, V)
    H = H_TW(T, W)

    return H

def D_WV(W, V):
    T = T_WV(W, V)
    D = D_TW(T, W)

    return D


# (1) TR
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

    print(f" (1) TR")
    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, h, v, B - K, D - K))

# (2) TB
if __name__ == "__main__":
    K = 273.15
    P = 101325

    T = 25 + K
    B = 15 + K

    R = R_TB(T,B)
    W = W_TR(T, R, P)
    Ps = Ps_TR(T, R, P)
    H = H_TR(T, R, P)
    V = V_TR(T, R, P)
    D = D_TR(T, R, P)

    print(f" (2) TB")
    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))

# (3) TH
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

    print(f" (3) TH")
    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))

# (4) TD
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

    print(f" (4) TD")
    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))


# (5) TW
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

    print(f" (5) TW")
    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))

# (6) TV
if __name__ == "__main__":
    K = 273.15
    P = 101325

    T = 25 + K
    V = 0.8533

    R= R_TV(T,V,P)
    Ps = Ps_TR(T, R)
    W = W_TV(T, V)
    B = B_TV(T, V)
    D= D_TV(T, V)
    H = H_TV(T, V)

    print(f" (6) TV")
    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))

# (7) RB
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

    print(f" (7) RB")
    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))


# (8) RH
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

    print(f" (8) RH")
    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))

# (9) RD 단위 뭐지
if __name__ == "__main__":
    K = 273.15
    P = 101325

    D = 7.72 + K   # [K]
    R = 0.332

    T= T_RD(R, D)
    Ps = Ps_TR(T, R, P)
    V = V_TR(T, R, P)
    W = W_TR(T,R,P)
    B = B_TR(T,R,P)

    print(f" (9) RD")
    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T-K, R, Ps, W, H, V, B - K, D - K ))

# (10) RW 단위 뭐지
if __name__ == "__main__":
    K = 273.15
    P = 101325

    R = 0.332
    W = 0.00653  # [kg/kg']

    T = T_RW(R, W)
    Ps = Ps_TR(T, R, P)
    V = V_TR(T, R, P)
    W = W_TR(T, R, P)
    B = B_TR(T, R, P)

    print(f" (10) RW")
    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K  ))


# (11) RV 만들어야함 오류뜸
if __name__ == "__main__":
    K = 273.15
    P = 101325

    R = 0.332
    V = 0.8533  # [m3/kg]

    T = T_RV(R, V)
    Ps = Ps_TR(T, R, P)
    V = V_TR(T, R, P)
    W = W_TR(T, R, P)
    B = B_TR(T, R, P)

    print(f" (11) RV")
    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))

# (12) BH
if __name__ == "__main__":
    K = 273.15
    P = 101325

    B = 15+K    # [K]
    H = 4.175e4 # [J]

    T = T_BH(B, H)
    R = R_BH(B, H)
    Ps = Ps_TR(T, R, P)
    V = V_TR(T, R, P)
    W = W_TR(T,R,P)
    H = H_TR(T,R,P)

    print(f" (12) BH")
    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))

# (13) BD
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

    print(f" (13) BD")
    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))

# (14) BW
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

    print(f" (14) BW")
    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))

# (15) BV
if __name__ == "__main__":
    K = 273.15
    P = 101325

    B = 15+K
    V = 0.8533 # [m3/kg]

    T = T_BV(B, V)
    R = R_TB(T, B)
    Ps = Ps_TR(T, R, P)
    V = V_TR(T, R, P)
    D = D_TR(T,R,P)
    H = H_TR(T,R,P)

    print(f" (15) BV")
    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))

# (16) HD
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

    print(f" (16) HD")
    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))


# (17) HW
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

    print(f" (17) HW")
    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))

# (18) HV
if __name__ == "__main__":
    K = 273.15
    P = 101325

    H = 41760
    V = 0.8533 # [m3/kg]

    T = T_HV(H, V)
    R= R_TH(T, H)
    Ps = Ps_TR(T, R, P)
    V = V_TR(T, R, P)
    B = B_TR(T,R,P)
    D= D_TR(T,R,P)

    print(f" (18) HV")
    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))

# (19) DW / 불가능

# (20) DV
if __name__ == "__main__":
    K = 273.15
    P = 101325

    d = 7.72  # [℃]
    D = d + K  # [K]
    V = 0.8533 # [m3/kg]

    T = T_DV(D, V)
    R= R_TD(T, D)
    Ps = Ps_TR(T, R, P)
    V = V_TR(T, R, P)
    B = B_TR(T,R,P)
    D= D_TR(T,R,P)

    print(f" (20) DV")
    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))

# (21) WV
if __name__ == "__main__":
    K = 273.15
    P = 101325

    W = 0.00653  # [kg/kg']
    V = 0.8533 # [m3/kg]

    T = T_WV(W, V)
    R= R_TW(T, W)
    Ps = Ps_TR(T, R, P)
    V = V_TR(T, R, P)
    B = B_TR(T,R,P)
    D= D_TR(T,R,P)

    print(f" (21) WV")
    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))
