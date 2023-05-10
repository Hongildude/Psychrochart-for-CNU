import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
# from CoolProp.CoolProp import PropsSI
# import psychrochart
# import psychrolib

K = 273.15

def secant(fun, x1, tol=1.0e-6, kmax=100):
    """ root finding f(x) = 0 by secant method """
    x2 = 1.1 * x1
    f1, f2 = fun(x1), fun(x2)
    for k in range(kmax):
        if f1 == f2:
            x2 += 1e-6
            f2 = fun(x2)
        x3 = x2 - f2 * (x1 - x2) / (f1 - f2)
        f3 = fun(x3)
        if abs(x1 - x3) < tol * max(1.0, abs(x3)):
            return x3
        x1, f1 = x2, f2
        x2, f2 = x3, f3

def hg_sat(T):
    t = T - K
    hg = (2501 + 1.805*t)*1000 # [J/kg]
    return hg

def Psat_water(T):
    C = np.array([-5.8002206e3, 1.3914993, -4.8640239e-2,
                  4.1764768e-5, -1.4452093e-8, 6.5459673])
    x = np.array([1/T, 1, T, T**2, T**3, np.log(T)])
    Psat = np.exp(np.dot(C, x)) # [Pa]
    return Psat

def Ps_TR(T, R, P=101325):
    """partial pressure of water vapor"""
    # Psat = PropsSI('P', 'T', T, 'Q', 0, 'water')
    Psat = Psat_water(T)
    Ps = R * Psat
    return Ps

def W_TR(T, R, P=101325):
    """specific humidity"""
    # Ra, Rs = 287.055, 461.520  # gas constant of air and water vapor
    Ps = Ps_TR(T, R, P)
    W = 0.62198 * Ps / (P - Ps)
    return W

def D_TR(T, R, P=101325):
    W = W_TR(T, R, P)

    def fun(D):
        return W_TR(D, 1, P) - W

    D0 = T - (1 - R) / 0.05
    D = secant(fun, D0)
    return D

def H_TR(T, R, P=101325):
    """enthalpy"""
    W = W_TR(T, R, P)
    t = T - K
    ha = 1006 * t
    hg = hg_sat(T)  # (2501 + 1.805*t)*1000
    h = ha + W * hg
    return h

def H_TW(T,W):
    R = R_TW(T, W)
    H = H_TR(T, R)

    return H

def R_TW(T, W, P=101325):
    return secant(lambda R: W_TR(T, R, P) - W, 0.8)

def B_TW(T, W):
    R = R_TW(T, W)
    B = B_TR(T, R)

    return B

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

T_array = np.linspace(273.15, 35 + 273.15, 100)
W_array = np.linspace(0, 30e-3, 100)

# Create 2D arrays for T and W values
T_grid, W_grid = np.meshgrid(T_array, W_array)

# Calculate relative humidity grid
RH_grid = np.zeros_like(T_grid)
for i, T in enumerate(T_array):
    for j, W in enumerate(W_array):
        RH_grid[j, i] = R_TW(T, W) * 100  # Convert to percentage

# Calculate enthalpy grid
H_grid = np.zeros_like(T_grid)
for i, T in enumerate(T_array):
    for j, W in enumerate(W_array):
        RH = R_TW(T, W) * 100  # Calculate relative humidity
        if RH <= 800:          # 여기 수정하면 된다.
            H_grid[j, i] = H_TW(T, W)
        else:
            H_grid[j, i] = np.nan

# Calculate wet-bulb temperature grid
B_grid = np.zeros_like(T_grid)
for i, T in enumerate(T_array):
    for j, W in enumerate(W_array):
        try:
            B_grid[j, i] = B_TW(T,W)  # Convert to Celsius
        except:
            B_grid[j, i] = np.nan

# Plot relative humidity contours
fig, ax = plt.subplots(figsize=(10, 6))

# Create contour plot for all levels except 100%
contour_levels_without_100 = np.arange(0, 100, 10)  # Define contour levels from 0 to 90
contour_plot_without_100 = ax.contour(T_grid - 273.15, W_grid , RH_grid, levels=contour_levels_without_100, colors='g', linewidths = 0.7)

# Create contour plot for 100% level only
contour_levels_100 = [100]  # Define contour level for 100% only
contour_plot_100 = ax.contour(T_grid - 273.15, W_grid , RH_grid, levels=contour_levels_100, colors='k', linewidths=2)

# Add contour labels for all levels
manual_locations = [(27, 0.0028), (26.5, 0.0038), (26, 0.0068), (25.5, 0.0078), (25, 0.01), (24.5,0.012), (24,0.0135), (23.5,0.0140), (23,0.0155)]
ax.clabel(contour_plot_without_100, colors='k', fontsize=8, fmt="%1.0f%%", manual = manual_locations)

# Plot enthalpy contours
enthalpy_levels = np.arange(0, 100, 5) * 1e3
enthalpy_plot = ax.contour(T_grid - 273.15, W_grid, H_grid, levels=enthalpy_levels, colors='k', linewidths=0.8)

# Plot wet-bulb temperature contours (습구 온도 그리드를 점선 스타일로 그리기)
wet_bulb_levels = np.arange(5+ 273.15, 31+273.15, 2)
wet_bulb_plot = ax.contour(T_grid - 273.15, W_grid, B_grid, levels=wet_bulb_levels, colors='k', linewidths=0.8, linestyles='dashed')

# Move y-axis to the right
ax.yaxis.tick_right()
ax.yaxis.set_label_position("right")

# Set y-axis ticks to be displayed every 0.001
ax.set_yticks(np.arange(0, W_array[-1] + 0.001, 0.001))

# Set x-axis ticks to be displayed every 5 and gridlines every 1
ax.set_xticks(np.arange(T_array[0] - 273.15, T_array[-1] - 273.15 + 5, 5))
ax.set_xticks(np.arange(T_array[0] - 273.15, T_array[-1] - 273.15 + 1, 1), minor=True)
ax.grid(which='minor', alpha=0.2)
ax.grid(which='major', alpha=0.5)

ax.set_xlabel("Temperature [°C]")
ax.set_ylabel("Absolute Humidity, W [kg/kg dry air]")
ax.set_title("Psychrometric Chart")
plt.show()
