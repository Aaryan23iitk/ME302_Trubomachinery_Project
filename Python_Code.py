import pandas as pd
import numpy as np
from scipy.optimize import fsolve

# --- Constants ---
R = 287.05
gamma = 1.4
mu = 1.83e-5
T01 = 293
Re_target = 3.0e6
l_proto = 0.2
D_pipe = 0.6
A_pipe = np.pi * (D_pipe / 2)**2

# --- Mach Number calculation ---
def solve_mach(mdot, p0, T0, A):
    target = (mdot * np.sqrt(R * T0)) / (p0 * 1000 * A * np.sqrt(gamma))

    def func(M):
        return M * (1 + 0.2 * M**2)**-3 - target

    try:
        M = fsolve(func, 0.2)[0]
        if M < 0 or M > 5:
            return np.nan
        return M
    except:
        return np.nan


# --- Static Temperature calculation---
def static_temp(T0, M):
    if np.isnan(M):
        return np.nan
    return T0 / (1 + 0.2 * M**2)


# --- Load Excel ---
file_path = 'Compressor_operation_map.xlsx'
df = pd.read_excel(file_path)

results = []

for idx, row in df.iterrows():
    try:
        mdot_ref = row['mdot_ref(kg/s)']
        T_ratio = row['T0 ratio']
        P_ratio = row['P0 ratio']

        # --- Stagnation Temperatures ---
        T02 = T01 * T_ratio
        T03 = T02
        T04 = T02
        T05 = T01

        # --- Diffuser temperature (using given relation) ---
        M4 = 0.5
        T4 = T04 / (1 + 0.2 * M4**2)

        # --- Velocity at 4 ---
        C4 = 0.5 * np.sqrt(gamma * R * T4)

        # --- Scaling ---
        K1 = (Re_target * mu * np.pi * 101.325 * 0.985 * P_ratio) / mdot_ref
        K2 = (Re_target * mu * R * T4 * (1.05**3.5)) / (C4 * 1000)

        l_m = np.sqrt(K2 / K1)
        scale = l_m / l_proto

        # --- Mass Flow ---
        mdot = Re_target * mu * np.pi * l_m

        # --- Pressures ---
        p01 = (mdot * 101.325) / mdot_ref
        p02 = p01 * P_ratio
        p03 = 0.985 * p02
        p04 = p03
        p05 = 0.95 * p04

        # --- Mach Numbers ---
        M1 = solve_mach(mdot, p01, T01, A_pipe)
        M2 = solve_mach(mdot, p02, T02, A_pipe)
        M3 = solve_mach(mdot, p03, T03, A_pipe)
        M5 = solve_mach(mdot, p05, T05, A_pipe)

        # --- Static Temperatures ---
        T1 = static_temp(T01, M1)
        T2 = static_temp(T02, M2)
        T3 = static_temp(T03, M3)
        T5 = static_temp(T05, M5)

        # --- Static Pressures ---
        def static_pressure(p0, M):
            if np.isnan(M):
                return np.nan
            return p0 * (1 + 0.2 * M**2)**-3.5

        p1 = static_pressure(p01, M1)
        p2 = static_pressure(p02, M2)
        p3 = static_pressure(p03, M3)
        p4 = p04 * (1.05)**-3.5
        p5 = static_pressure(p05, M5)

        # --- Store Results ---
        results.append({
            # Scaling
            'Scale_s': scale,
            'Mass_Flow_kg_s': mdot,

            # Stagnation Temperatures
            'T01_K': T01,
            'T02_K': T02,
            'T03_K': T03,
            'T04_K': T04,
            'T05_K': T05,

            # Static Temperatures
            'T1_K': T1,
            'T2_K': T2,
            'T3_K': T3,
            'T4_K': T4,
            'T5_K': T5,

            # Pressures
            'p01_kPa': p01,
            'p02_kPa': p02,
            'p03_kPa': p03,
            'p04_kPa': p04,
            'p05_kPa': p05,

            'p1_kPa': p1,
            'p2_kPa': p2,
            'p3_kPa': p3,
            'p4_kPa': p4,
            'p5_kPa': p5,

            # Mach
            'M1': M1,
            'M2': M2,
            'M3': M3,
            'M4': M4,
            'M5': M5
        })

    except Exception as e:
        print(f"Error in row {idx}: {e}")
        continue


# --- Export ---
results_df = pd.DataFrame(results)
output_df = pd.concat([df, results_df], axis=1)

output_df.to_excel('Scaling_Results.xlsx', index=False)
