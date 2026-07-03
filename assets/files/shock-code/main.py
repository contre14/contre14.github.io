import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

from rh_jump import compute_rh_jump_hot, R_N2
from simulate import rhs, Mmix_from_YN2, R_UNIV, M_N2, N_AVOGADRO


def main():
    # Pre-shock conditions (region 1)
    P1 = 5.0       # Pa
    T1 = 200.0     # K
    Tv1 = T1       # K, upstream vibrational temperature
    US = 7000.0    # m/s, shock speed (upstream velocity in shock-fixed frame)

    # Upstream composition: pure N2
    Y_N2_1 = 1.0
    Y_N_1  = 0.0

    # Upstream density (pure N2 -> R_mix = R_N2)
    rho1 = P1 / (R_N2 * T1)  # kg/m^3
    U1 = US                  # m/s

    # Rankine–Hugoniot jump (region 2, just behind shock)
    y_upstream = np.array([Y_N2_1, Y_N_1])
    rh = compute_rh_jump_hot(y_upstream, P1, T1, US)

    P2 = rh["P2"]
    T2 = rh["T2"]
    U2 = rh["U2"]
    Y_N2_2 = rh["y"][0]   # still 1.0 for frozen chemistry
    Y_N_2  = 1.0 - Y_N2_2
    Tv2 = Tv1             # vibrationally frozen across the thin shock

    rho2 = P2 / (R_N2 * T2)  # kg/m^3

    # Mass flux G = rho * u (constant)
    G = rho2 * U2

    # IVP initial condition at x = 0+
    # State vector y = [Y_N2, u, T, Tv]
    y0 = np.array([Y_N2_2, U2, T2, Tv2], dtype=float)

    # Integration domain
    x_max = 2.5
    x_span = (0.0, x_max)
    x_eval = np.linspace(0.0, x_max, 1000)

    # Integrate shock-layer ODE system
    sol = solve_ivp(
        fun=lambda x, y: rhs(x, y, G),
        t_span=x_span,
        y0=y0,
        method="RK45",
        t_eval=x_eval,
        rtol=1.0e-6,
        atol=1.0e-9,
    )

    if not sol.success:
        print("Integration failed:", sol.message)
        return

    x    = sol.t
    Y_N2 = sol.y[0, :]
    u    = sol.y[1, :]
    T    = sol.y[2, :]
    Tv   = sol.y[3, :]

    # Post-processing: rho(x), p(x), Y_N(x)
    Y_N = 1.0 - Y_N2

    # Mixture molar mass & gas constant
    M_mix = Mmix_from_YN2(Y_N2)      # kg/mol
    R_mix = R_UNIV / M_mix           # J/(kg·K)

    rho = G / u                      # kg/m^3
    p   = rho * R_mix * T            # Pa

    # Auto-detect equilibrium location x_eq: first x where T, Tv, Y_N2 are all
    # within a relative tolerance of their end-of-domain (equilibrium) values.
    eq_tol = 4.0e-3
    dT  = np.abs(T  - T[-1])  / abs(T[-1])
    dTv = np.abs(Tv - Tv[-1]) / abs(Tv[-1])
    dY  = np.abs(Y_N2 - Y_N2[-1]) / abs(Y_N2[-1])
    within = (dT < eq_tol) & (dTv < eq_tol) & (dY < eq_tol)
    idx_eq = len(x) - 1
    for i in range(len(x)):
        if within[i:].all():
            idx_eq = i
            break
    x_eq = x[idx_eq]

    # Approximate equilibrium state at x = x_max
    Y_N2_eq = Y_N2[-1]
    Y_N_eq  = Y_N[-1]
    u_eq    = u[-1]
    T_eq    = T[-1]
    Tv_eq   = Tv[-1]
    rho_eq  = rho[-1]
    p_eq    = p[-1]

    # Print pre-shock, post-shock, and approximate equilibrium states
    print("===== Pre-shock state (region 1) =====")
    print(f"P1    = {P1:.6e} Pa")
    print(f"rho1  = {rho1:.6e} kg/m^3")
    print(f"U1    = {U1:.6e} m/s")
    print(f"T1    = {T1:.6e} K")
    print(f"Tv1   = {Tv1:.6e} K")
    print(f"Y_N2_1= {Y_N2_1:.6e}")
    print(f"Y_N_1 = {Y_N_1:.6e}")
    print()

    print("===== Post-shock state (x = 0+) (region 2 initial) =====")
    print(f"P2    = {P2:.6e} Pa")
    print(f"rho2  = {rho2:.6e} kg/m^3")
    print(f"U2    = {U2:.6e} m/s")
    print(f"T2    = {T2:.6e} K")
    print(f"Tv2   = {Tv2:.6e} K")
    print(f"Y_N2_2= {Y_N2_2:.6e}")
    print(f"Y_N_2 = {Y_N_2:.6e}")
    print()

    print(f"===== Detected equilibrium state (x = {x_eq:.3f} m) =====")
    print(f"p_eq    = {p[idx_eq]:.6e} Pa")
    print(f"rho_eq  = {rho[idx_eq]:.6e} kg/m^3")
    print(f"u_eq    = {u[idx_eq]:.6e} m/s")
    print(f"T_eq    = {T[idx_eq]:.6e} K")
    print(f"Tv_eq   = {Tv[idx_eq]:.6e} K")
    print(f"Y_N2_eq = {Y_N2[idx_eq]:.6e}")
    print(f"Y_N_eq  = {Y_N[idx_eq]:.6e}")
    print()

    print(f"===== Downstream boundary (x = {x_max:.3f} m) =====")
    print(f"p_eq      = {p_eq:.6e} Pa")
    print(f"rho_eq    = {rho_eq:.6e} kg/m^3")
    print(f"u_eq      = {u_eq:.6e} m/s")
    print(f"T_eq      = {T_eq:.6e} K")
    print(f"Tv_eq     = {Tv_eq:.6e} K")
    print(f"Y_N2_eq   = {Y_N2_eq:.6e}")
    print(f"Y_N_eq    = {Y_N_eq:.6e}")
    print()

    # Macroscopic fields: 2x2 subplots
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    # 1) Pressure vs x
    ax = axes[0, 0]
    ax.plot(x, p)
    ax.set_xlabel("x [m]")
    ax.set_ylabel("p [Pa]")
    ax.set_title("Pressure vs x")
    ax.grid(True)

    # 2) Density vs x
    ax = axes[0, 1]
    ax.plot(x, rho)
    ax.set_xlabel("x [m]")
    ax.set_ylabel(r"$\rho$ [kg/m$^3$]")
    ax.set_title("Density vs x")
    ax.grid(True)

    # 3) T and Tv vs x
    ax = axes[1, 0]
    ax.plot(x, T,  label="T")
    ax.plot(x, Tv, label="Tv", linestyle="--")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("Temperature [K]")
    ax.set_title("T and Tv vs x")
    ax.legend()
    ax.grid(True)

    # 4) Y_N2 and Y_N vs x
    ax = axes[1, 1]
    ax.plot(x, Y_N2, label="Y_N2")
    ax.plot(x, Y_N,  label="Y_N", linestyle="--")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("Mass fraction")
    ax.set_title("Y_N2 and Y_N vs x")
    ax.legend()
    ax.grid(True)

    plt.tight_layout()

    # Rotational / vibrational / electronic distributions
    # x locations: pre-shock + selected downstream positions
    x_targets = ["pre", 0.0, 0.005, 0.01, 0.1]

    # Constants for level energies
    B_e_cm   = 1.998            # N2 rotational constant [cm^-1]
    hc_eV_cm = 1.239841984e-4   # eV·cm
    k_B_eV   = 8.617333262e-5   # eV/K

    # Rotational quantum numbers J and degeneracy
    J_max = 50
    J = np.arange(0, J_max + 1)
    g_J = 2 * J + 1

    # Rotational energies [eV]
    E_rot_eV = hc_eV_cm * B_e_cm * J * (J + 1)

    # Vibrational levels (harmonic oscillator)
    THETA_V = 3390.0  # K
    v_max = 10
    v = np.arange(0, v_max + 1)
    E_vib_eV = k_B_eV * THETA_V * (v + 0.5)
    g_v = np.ones_like(v)

    # Simple electronic levels for N2 [eV]
    E_elec_eV = np.array([0.0, 6.17, 7.35, 8.16])
    g_e = np.ones_like(E_elec_eV)

    fig_dist, ax_dist = plt.subplots(1, 3, figsize=(15, 4))

    for xt in x_targets:
        if xt == "pre":
            T_loc    = T1
            Tv_loc   = Tv1
            rho_loc  = rho1
            Y_N2_loc = Y_N2_1
            label_str = f"pre-shock, T ≈ {T_loc:.0f} K"
        else:
            idx = np.argmin(np.abs(x - xt))
            T_loc    = T[idx]
            Tv_loc   = Tv[idx]
            rho_loc  = rho[idx]
            Y_N2_loc = Y_N2[idx]
            label_str = f"x = {xt:.3f} m, T ≈ {T_loc:.0f} K"

        # Total N2 number density [molecules/m^3]
        rho_N2 = rho_loc * Y_N2_loc          # kg/m^3
        C_N2   = rho_N2 / M_N2               # mol/m^3
        n_tot  = C_N2 * N_AVOGADRO           # molecules/m^3

        # Rotational distribution (Boltzmann)
        exponent_rot = -E_rot_eV / (k_B_eV * T_loc)
        f_J = g_J * np.exp(exponent_rot)
        Q_rot = np.sum(f_J)
        n_J = n_tot * f_J / Q_rot
        y_ln_rot = np.log(n_J / g_J)

        ax = ax_dist[0]
        ax.plot(E_rot_eV, y_ln_rot, marker='o', linestyle='-',
                label=label_str)

        # Vibrational distribution (using Tv)
        exponent_vib = -E_vib_eV / (k_B_eV * Tv_loc)
        f_v = g_v * np.exp(exponent_vib)
        Q_vib = np.sum(f_v)
        n_v = n_tot * f_v / Q_vib
        y_ln_vib = np.log(n_v)

        ax = ax_dist[1]
        ax.plot(E_vib_eV, y_ln_vib, marker='o', linestyle='-',
                label=label_str)

        # Electronic distribution (using T_loc)
        exponent_elec = -E_elec_eV / (k_B_eV * T_loc)
        f_e = g_e * np.exp(exponent_elec)
        Q_elec = np.sum(f_e)
        n_e = n_tot * f_e / Q_elec
        y_ln_elec = np.log(n_e / g_e)

        ax = ax_dist[2]
        ax.plot(E_elec_eV, y_ln_elec, marker='o', linestyle='-',
                label=label_str)

    # Format distribution plots
    ax = ax_dist[0]
    ax.set_xlabel("Rotational energy $E_J$ [eV]")
    ax.set_ylabel(r"$\ln(n_J / g_J)$")
    ax.set_title("Rotational Boltzmann plot")
    ax.grid(True)
    ax.legend()

    ax = ax_dist[1]
    ax.set_xlabel("Vibrational energy $E_v$ [eV]")
    ax.set_ylabel(r"$\ln(n_v)$")
    ax.set_title("Vibrational distribution")
    ax.grid(True)
    ax.legend()

    ax = ax_dist[2]
    ax.set_xlabel("Electronic energy $E_e$ [eV]")
    ax.set_ylabel(r"$\ln(n_e / g_e)$")
    ax.set_title("Electronic distribution")
    ax.grid(True)
    ax.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
