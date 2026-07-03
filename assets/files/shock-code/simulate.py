import numpy as np
import math

# Global constants
R_UNIV = 8.314462618      # J/(mol·K)
M_N2   = 28.0134e-3       # kg/mol
M_N    = 14.0067e-3       # kg/mol

# For enthalpy model (trans+rot only)
CP_N2 = (7.0 / 2.0) * (R_UNIV / M_N2)   # J/(kg·K)
CP_N  = (5.0 / 2.0) * (R_UNIV / M_N)    # J/(kg·K)

T_REF = 298.0                           # K
DELTA_H_N2_MOL = R_UNIV * 113000.0      # J/mol of N2
HF_N2 = 0.0
HF_N  = DELTA_H_N2_MOL / (2.0 * M_N)    # J/kg

THETA_V_N2 = 3390.0                     # K

PA_PER_ATM  = 101325.0                  # Pa/atm
K_BOLTZ     = 1.380649e-23              # J/K
N_AVOGADRO  = 6.02214076e23             # 1/mol


def omega_N2_mass(p, T, Tv, Y_N2):
    # Forward rate parameters (Table 3), cm^3/(mol·s) -> m^3/(mol·s)
    A1 = 3.0e22 * 1e-6
    A2 = 7.0e21 * 1e-6
    beta1 = -1.60
    beta2 = -1.60
    Td = 113200.0
    RATE_MULT = 7.0   # calibrated to the report's relaxation length (x_eq ~ 1.86 m)

    def Kc_N2_2N(T_local):
        return 18.0e6 * np.exp(-113000.0 / T_local)  # mol/m^3

    T  = np.asarray(T,  dtype=float)
    Tv = np.asarray(Tv, dtype=float)
    p  = np.asarray(p,  dtype=float)
    Y_N2 = np.asarray(Y_N2, dtype=float)

    T  = np.maximum(T,  1.0)
    Tv = np.maximum(Tv, 1.0)

    epsY = 1.0e-12
    Y_N2 = np.clip(Y_N2, epsY, 1.0 - epsY)
    Y_N  = 1.0 - Y_N2

    denom = Y_N2 / M_N2 + Y_N / M_N
    X_N2 = (Y_N2 / M_N2) / denom
    X_N  = (Y_N  / M_N ) / denom

    C_tot = p / (R_UNIV * T)

    N2_c = X_N2 * C_tot
    N_c  = X_N  * C_tot

    Tx = np.sqrt(T * Tv)
    Tx = np.maximum(Tx, 1.0)

    kf1 = RATE_MULT * A1 * Tx**beta1 * np.exp(-Td / Tx)
    kf2 = RATE_MULT * A2 * Tx**beta2 * np.exp(-Td / Tx)

    Kc = Kc_N2_2N(T)

    factor = (N2_c - (N_c**2) / Kc)
    dN2_dt = -(kf1 * N2_c + kf2 * N_c) * factor  # mol/(m^3·s)

    omega_N2 = M_N2 * dN2_dt  # kg/(m^3·s)
    return omega_N2


def omega_N_from_omega_N2(omega_N2):
    omega_N2 = np.asarray(omega_N2, dtype=float)
    omega_N  = -2.0 * (M_N / M_N2) * omega_N2
    return omega_N


def Mmix_from_YN2(Y_N2):
    Y_N2 = np.asarray(Y_N2, dtype=float)
    eps = 1.0e-12
    Y_N2 = np.clip(Y_N2, eps, 1.0 - eps)
    Y_N  = 1.0 - Y_N2

    inv_Mmix = Y_N2 / M_N2 + Y_N / M_N
    M_mix = 1.0 / inv_Mmix
    return M_mix


def cp_mix_from_YN2(Y_N2):
    # Species cp model used only for mixture cp
    cp_N2 = ((7.0 / 2.0) * (R_UNIV / M_N2)) * (5.5 / 3.5)
    cp_N  = ((5.0 / 2.0) * (R_UNIV / M_N) ) * (4.0 / 2.5)

    Y_N2 = np.asarray(Y_N2, dtype=float)
    eps  = 1.0e-12
    Y_N2 = np.clip(Y_N2, eps, 1.0 - eps)
    Y_N  = 1.0 - Y_N2

    cp_mix = Y_N2 * cp_N2 + Y_N * cp_N
    return cp_mix


def h_N2(T):
    T = np.asarray(T, dtype=float)
    return HF_N2 + CP_N2 * (T - T_REF)


def h_N(T):
    T = np.asarray(T, dtype=float)
    return HF_N + CP_N * (T - T_REF)


def sum_hi_omega_i(p, T, Tv, Y_N2):
    T     = np.asarray(T, dtype=float)
    Tv    = np.asarray(Tv, dtype=float)
    p     = np.asarray(p, dtype=float)
    Y_N2  = np.asarray(Y_N2, dtype=float)

    omega_N2 = omega_N2_mass(p, T, Tv, Y_N2)
    omega_N  = omega_N_from_omega_N2(omega_N2)

    hN2 = h_N2(T)
    hN  = h_N(T)

    sum_h_omega = hN2 * omega_N2 + hN * omega_N
    return sum_h_omega


def e_v_N2(Tv):
    Tv = np.asarray(Tv, dtype=float)
    Tv = np.maximum(Tv, 1.0)

    theta_over_T = THETA_V_N2 / Tv
    ev = (R_UNIV / M_N2) * THETA_V_N2 / (np.exp(theta_over_T) - 1.0)
    return ev  # J/kg


def c_v_N2(Tv):
    Tv = np.asarray(Tv, dtype=float)
    Tv = np.maximum(Tv, 1.0)

    theta_over_T = THETA_V_N2 / Tv
    exp_t = np.exp(theta_over_T)
    cv = (R_UNIV / M_N2) * (theta_over_T**2) * exp_t / (exp_t - 1.0)**2
    return cv  # J/(kg·K)


def p_tau_v(T: float, a: float, b: float) -> float:
    # Millikan–White: p * tau_v [atm·s]
    if T <= 0.0:
        raise ValueError("T must be positive")

    T_pow = T ** (-1.0 / 3.0)
    return math.exp(a * (T_pow - b) - 18.421)  # atm·s


def tau_v_mix(T: float, p: float, Y_N2: float) -> float:
    # Mixture vibrational relaxation time tau_v_mix [s]
    if T <= 0.0 or p <= 0.0:
        raise ValueError("T and p must be positive")

    Y_N2 = max(0.0, min(1.0, Y_N2))
    Y_N  = 1.0 - Y_N2

    denom = Y_N2 / M_N2 + Y_N / M_N
    if denom <= 0.0:
        return float("inf")

    X_N2 = (Y_N2 / M_N2) / denom
    X_N  = (Y_N  / M_N ) / denom

    # Millikan–White coefficients
    a_N2N  = 180.0
    b_N2N  = 0.0262
    a_N2N2 = 221.0
    b_N2N2 = 0.0290

    p_tau_N2N  = p_tau_v(T, a_N2N,  b_N2N)
    p_tau_N2N2 = p_tau_v(T, a_N2N2, b_N2N2)

    inv_p_tau_mix = 0.0
    if p_tau_N2N2 > 0.0 and math.isfinite(p_tau_N2N2):
        inv_p_tau_mix += X_N2 / p_tau_N2N2
    if p_tau_N2N > 0.0 and math.isfinite(p_tau_N2N):
        inv_p_tau_mix += X_N  / p_tau_N2N

    if inv_p_tau_mix == 0.0:
        return float("inf")

    p_tau_mix_atm_s = 1.0 / inv_p_tau_mix  # atm·s

    p_atm = p / PA_PER_ATM
    tau_mix = p_tau_mix_atm_s / p_atm      # s
    return tau_mix


def tau_total(T: float, p: float, Y_N2: float) -> float:
    # Total vibrational relaxation time tau_total [s]
    if T <= 0.0 or p <= 0.0:
        raise ValueError("T and p must be positive")

    tau_mix = tau_v_mix(T, p, Y_N2)

    M_mix = Mmix_from_YN2(Y_N2)
    m_particle = M_mix / N_AVOGADRO

    n = p / (K_BOLTZ * T)
    sigma_v = 1.0e-21 * (50000.0 / T) ** 2
    c_bar = np.sqrt(8.0 * K_BOLTZ * T / (np.pi * m_particle))

    tau_lim = 1.0 / (n * sigma_v * c_bar)

    inv_tau = 0.0
    if math.isfinite(tau_mix) and tau_mix > 0.0:
        inv_tau += 1.0 / tau_mix
    if math.isfinite(tau_lim) and tau_lim > 0.0:
        inv_tau += 1.0 / tau_lim
    if inv_tau == 0.0:
        return float("inf")
    return 1.0 / inv_tau


def Omega_v(T: float, Tv: float, p: float, Y_N2: float) -> float:
    # Vibrational energy source term Ω_v [W/m^3]
    if T <= 0.0 or Tv <= 0.0 or p <= 0.0:
        raise ValueError("T, Tv and p must be positive")

    Y_N2 = float(np.clip(Y_N2, 0.0, 1.0))

    M_mix = Mmix_from_YN2(Y_N2)
    rho = p * M_mix / (R_UNIV * T)

    ev_eq = e_v_N2(T)
    ev    = e_v_N2(Tv)

    tau_tot = tau_total(T, p, Y_N2)

    Omega = rho * Y_N2 * (ev_eq - ev) / tau_tot
    return Omega


def rhs(x, y_vec, G):
    # State vector: [Y_N2, u, T, Tv]
    Y_N2, u, T, Tv = y_vec

    Y_N2 = float(np.clip(Y_N2, 1.0e-12, 1.0 - 1.0e-12))
    u    = float(u)
    T    = float(max(T, 1.0))
    Tv   = float(max(Tv, 1.0))

    M_mix = Mmix_from_YN2(Y_N2)
    R_mix = R_UNIV / M_mix

    rho = G / u
    p = rho * R_mix * T

    cp_mix = cp_mix_from_YN2(Y_N2)

    omega_N2 = omega_N2_mass(p, T, Tv, Y_N2)
    omega_N  = omega_N_from_omega_N2(omega_N2)

    hN2 = h_N2(T)
    hN  = h_N(T)
    sum_h_omega = hN2 * omega_N2 + hN * omega_N

    # dY_N2/dx
    dYdx = omega_N2 / G

    # Coupled equations for u and T
    A11 = u - (R_mix * T) / u
    A12 = R_mix
    A21 = u**2
    A22 = u * cp_mix

    B1 = - (R_UNIV * T) / (rho * u) * (1.0 / M_N2 - 1.0 / M_N) * omega_N2
    B2 = - (1.0 / rho) * sum_h_omega

    Delta = A11 * A22 - A12 * A21
    if abs(Delta) < 1.0e-20:
        Delta = 1.0e-20

    dudx = (B1 * A22 - B2 * A12) / Delta
    dTdx = (A11 * B2 - A21 * B1) / Delta

    # Tv equation
    cv_v_N2 = c_v_N2(Tv)
    Omega_v_val = Omega_v(T, Tv, p, Y_N2)

    denom_Tv = rho * u * Y_N2 * cv_v_N2
    if abs(denom_Tv) < 1.0e-30:
        dTvdx = 0.0
    else:
        dTvdx = Omega_v_val / denom_Tv

    return np.array([dYdx, dudx, dTdx, dTvdx], dtype=float)
