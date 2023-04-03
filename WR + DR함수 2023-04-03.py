import numpy as np
from CoolProp.HumidAirProp import HAPropsSI
from scipy.optimize import fsolve

# 열역학 교과서 Table5 Saturated water - Pressure table
pressure_array = np.array([1e3, 1.5e3, 2e3, 2.5e3, 3e3, 4e3, 5e3, 7.5e3, 10e3, 15e3])
temperature_array = np.array([6.97, 13.02, 17.5, 21.08, 24.08, 28.96, 32.87, 40.29, 45.81, 53.97])

# 열역학 교과서 Table4 Saturated water - Temperature Table
pressure_array2 = np.array([0.6117, 0.8725, 1.2281, 1.7057, 2.3392, 3.1698, 4.2469, 5.6291, 7.3851, 9.5953, 12.352, 15.763, 19.947, 25.043, 31.202])
temperature_array2 = np.array([0.01, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70])


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
import numpy as np
from CoolProp.HumidAirProp import HAPropsSI
from scipy.optimize import fsolve

# 열역학 교과서 Table5 Saturated water - Pressure table
pressure_array = np.array([1e3, 1.5e3, 2e3, 2.5e3, 3e3, 4e3, 5e3, 7.5e3, 10e3, 15e3])
temperature_array = np.array([6.97, 13.02, 17.5, 21.08, 24.08, 28.96, 32.87, 40.29, 45.81, 53.97])


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


if __name__ == "__main__":
    K = 273.15
    P = 101325

    T = 25 + K
    B = 15 + K

    Ps = Psat_water(T)
    W = w1_TB(T, B)
    h = h_TB(T, B)
    R = R_TB(T, B)
    D = D_TB(T, B)

    fmt = "{:>12s}" * 7
    print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'B', 'D'))
    fmt = "{:12.4g}" * 7
    print(fmt.format(T - K, R, Ps, W, h, B - K, D ))



    W = HAPropsSI('W', 'T', T, 'B', B, 'P', P)
    h = HAPropsSI('H', 'T', T, 'B', B, 'P', P)
    R = HAPropsSI('R', 'T', T, 'B', B, 'P', P)
    D = HAPropsSI('D', 'T', T, 'B', B, 'P', P)
    print(fmt.format(T - K, R, Ps, W, h, B - K, D - K ))

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

def T_DR(D,R):
    Pv = Psat_water(D+K)
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
    T = T_DR(D,R)

    return T


# if __name__ == "__main__":
#     K = 273.15
#     P = 101325
#
#     T = 25 + K
#     B = 15 + K
#
#     Ps = Psat_water(T)
#     W = w1_TB(T, B)
#     h = h_TB(T, B)
#     R = R_TB(T, B)
#     D = D_TB(T, B)
#
#     fmt = "{:>12s}" * 7
#     print(fmt.format('T', 'R', 'Ps', 'W', 'h', 'B', 'D'))
#     fmt = "{:12.4g}" * 7
#     print(fmt.format(T - K, R, Ps, W, h, B - K, D ))
#
#
#
#     W = HAPropsSI('W', 'T', T, 'B', B, 'P', P)
#     h = HAPropsSI('H', 'T', T, 'B', B, 'P', P)
#     R = HAPropsSI('R', 'T', T, 'B', B, 'P', P)
#     D = HAPropsSI('D', 'T', T, 'B', B, 'P', P)
#     print(fmt.format(T - K, R, Ps, W, h, B - K, D - K ))

# 교과서 예제 14-4 건구온도 정답 35℃
print(T_DR(19.4, 0.4))
print(T_WR(0.0142, 0.4))



