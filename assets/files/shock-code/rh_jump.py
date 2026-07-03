import math

# Thermodynamic constants for pure N2 (translational + rotational only)
R_UNIVERSAL = 8.31446261815324      # J/(mol·K)
M_N2        = 28.0134e-3            # kg/mol
R_N2        = R_UNIVERSAL / M_N2    # J/(kg·K)
CP_N2       = 3.5 * R_N2            # Cp = 7/2 R (no vibration)


def residual_mass(rho1: float, US: float, rho2: float, U2: float) -> float:
    return (rho1 * US - rho2 * U2) / (rho1 * US)


def residual_momentum(P1: float, rho1: float, US: float,
                      P2: float, rho2: float, U2: float) -> float:
    return (P1 + rho1 * US**2 - (P2 + rho2 * U2**2)) / (P1 + rho1 * US**2)


def residual_energy(H1: float, US: float, H2: float, U2: float) -> float:
    return (H1 + 0.5 * US**2 - (H2 + 0.5 * U2**2)) / (H1 + 0.5 * US**2)


def compute_rh_jump_hot(
    y,
    P1: float,
    T1: float,
    US: float,
    tol: float = 1.0e-14,
    max_iter: int = 1000,
):
    # Pre-shock density from ideal gas EOS
    rho1 = P1 / (R_N2 * T1)

    # Upstream static enthalpy (tr+rot only): h1 = Cp*T1
    H1 = CP_N2 * T1

    # Initial guess from perfect-gas normal shock
    gamma = CP_N2 / (CP_N2 - R_N2)
    a1 = math.sqrt(gamma * R_N2 * T1)
    M1 = US / a1

    if M1 <= 1.0:
        raise ValueError("Upstream Mach number M1 <= 1: no normal shock solution.")

    P2_P1     = 1.0 + 2.0 * gamma / (gamma + 1.0) * (M1**2 - 1.0)
    rho2_rho1 = ((gamma + 1.0) * M1**2) / (2.0 + (gamma - 1.0) * M1**2)
    T2_T1     = P2_P1 / rho2_rho1

    T2 = T2_T1 * T1
    P2 = P2_P1 * P1

    # Iterative Rankine–Hugoniot solution
    for _ in range(max_iter):
        rho2 = P2 / (R_N2 * T2)
        U2 = rho1 * US / rho2

        P2 = P1 + rho1 * US**2 * (1.0 - rho1 / rho2)

        H2 = CP_N2 * T2
        energy_residual = H2 - H1 - 0.5 * US**2 * (1.0 - (rho1 / rho2)**2)
        T2 = T2 - energy_residual / CP_N2

        rho2 = P2 / (R_N2 * T2)
        U2   = rho1 * US / rho2
        H2   = CP_N2 * T2

        R1 = residual_mass(rho1, US, rho2, U2)
        R2 = residual_momentum(P1, rho1, US, P2, rho2, U2)
        R3 = residual_energy(H1, US, H2, U2)

        if max(abs(R1), abs(R2), abs(R3)) < tol:
            break
    else:
        print(
            "Warning: RH iteration did not converge within "
            f"max_iter={max_iter}. "
            f"Residuals: R1={R1:.3e}, R2={R2:.3e}, R3={R3:.3e}"
        )

    return {
        "P2": P2,
        "T2": T2,
        "U2": U2,
        "y": y,
    }
