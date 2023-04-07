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
    x = np.array([1/T, 1, T, T**2, T**3, np.log(T)])
    Psat = np.exp(np.dot(C, x)) # [Pa]
    return Psat

def hg_sat(T):
    t = T - K
    hg = (2501 + 1.805*t)*1000 # [J/kg]
    return hg

def w2(B):
    pg2 = Psat_water(B)
    w2_value = 0.622*pg2/(P-pg2) # [kg/kg']
    return w2_value

def w1_TB(T,B):
    hg1 = hg_sat(T) # [J/kg]
    hf2 = 4186*(B - K) # [J/kg]
    hfg2 = hg_sat(B) - hf2 # [J/kg]
    w2_value = w2(B)

    w1 = (1005*(B-T) + w2_value*hfg2) / (hg1-hf2) # [kg/kg']
    return w1

def h_TB(T,B):
    w1_value = w1_TB(T,B)
    enthalpy = 1005*(T-K) + w1_value*hg_sat(T)
    return enthalpy

def R_TB(T,B):
    w1_value = w1_TB(T, B)
    Pg1 = Psat_water(T)

    R_TB = (w1_value*P) / ( (0.622 + w1_value) * Pg1)
    return R_TB

def Pv(T, B):
    Pv = R_TB(T,B)*Psat_water(T) # [Pa]

    return Pv

def D_TB(T,B):
    # Interpolate the temperature at a given pressure
    pressure_value = Pv(T, B)
    interpolated_temperature = np.interp(pressure_value, pressure_array, temperature_array)

    return interpolated_temperature

def T_RD(R,D):
    Pv = Psat_water(D + K)
    Pgat = Pv/R # [Pa]
    Pgat = Pgat/1000 # [kPa]
    interpolated_temperature2 = np.interp(Pgat, pressure_array2, temperature_array2)

    return interpolated_temperature2

def D_W(W):
    Pv = (W*P)/(0.622+W)
    D = np.interp(Pv, pressure_array, temperature_array)

    return D

def T_WR(W, R):
    D = D_W(W)
    T = T_RD(R,D)

    return T

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
    V = Ra * T / (P - Ps)
    return V

def T_RV(R, V, P=101325, T0=25 + K):
    def fun(T):
        V_calc = V_TR(T, R)
        return V - V_calc

    T = secant(fun, T0)
    return T

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

# TV
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

def D_W(W):
    Pv = (W*P)/(0.622+W)
    D = np.interp(Pv, pressure_array, temperature_array)

    return D

def w2(B):
    pg2 = Psat_water(B)
    w2_value = 0.622*pg2/(P-pg2) # [kg/kg']
    return w2_value

def w1_TB(T,B):
    hg1 = hg_sat(T) # [J/kg]
    hf2 = 4186*(B - K) # [J/kg]
    hfg2 = hg_sat(B) - hf2 # [J/kg]
    w2_value = w2(B)

    w1 = (1005*(B-T) + w2_value*hfg2) / (hg1-hf2) # [kg/kg']
    return w1

def h_TB(T,B):
    w1_value = w1_TB(T,B)
    enthalpy = 1005*(T-K) + w1_value*hg_sat(T)
    return enthalpy

def R_TB(T,B):
    w1_value = w1_TB(T, B)
    Pg1 = Psat_water(T)

    R_TB = (w1_value*P) / ( (0.622 + w1_value) * Pg1)
    return R_TB

def Pv(T, B):
    Pv = R_TB(T,B)*Psat_water(T) # [Pa]

    return Pv

def D_TB(T,B):
    # Interpolate the temperature at a given pressure
    pressure_value = Pv(T, B)
    interpolated_temperature = np.interp(pressure_value, pressure_array, temperature_array)

    return interpolated_temperature


def D_W(W):
    Pv = (W*P)/(0.622+W)
    D = np.interp(Pv, pressure_array, temperature_array)

    return D

# RW
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

# RV
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

def T_BV(B, V):
    T, R = TR_BV(B, V)
    return T

def R_BV(B, V):
    T, R = TR_BV(B, V)

    return R

def TR_BV(B, V, T0=25 + K, R0=0.6):
    def fun(x):
        T, R = x
        BB = B_TR(T, R)
        VV = V_TR(T, R)
        return [B - BB, V - VV]

    T, R = fsolve(fun, [T0, R0])
    return T, R

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

# HV
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

# DV
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

# WV
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

## T_RB로 변경함
def T_BR(B, R, P=101325):
    return secant(lambda T: B_TR(T, R, P) - B, 0.8)

# T_RH로 변경함
def T_HR(H, R, P=101325):
    return secant(lambda T: H_TR(T, R, P) - H, 0.8)



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

    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))

# (6) TV 만들어야함
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


    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))

# (9) RD 단위 뭐지
if __name__ == "__main__":
    K = 273.15
    P = 101325

    D = 7.72  # [℃]
    R = 0.332

    T= T_RD(R, D)
    Ps = Ps_TR(T + K, R, P)
    V = V_TR(T+ K, R, P)
    W = W_TR(T + K,R,P)
    B = B_TR(T + K,R,P)



    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T , R, Ps, W, H, V, B - K, D ))

# (10) RW 단위 뭐지
if __name__ == "__main__":
    K = 273.15
    P = 101325

    R = 0.332
    W = 0.00653  # [kg/kg']

    T = T_RW(R, W)
    Ps = Ps_TR( T + K, R, P)
    V = V_TR(T + K, R, P)
    W = W_TR(T + K, R, P)
    B = B_TR(T + K , R, P)

    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T, R, Ps, W, H, V, B - K, D ))


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

    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))

# (12) BH 만들어야함 / 불가능

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

    fmt = "{:>12s}" * 8
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'v', 'B', 'D'))
    fmt = "{:12.4g}" * 8
    print(fmt.format(T - K, R, Ps, W, H, V, B - K, D - K))
