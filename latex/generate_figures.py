#!/usr/bin/env python3
"""Generate physics figures for the storage physics book. Output: PDF."""
import matplotlib
matplotlib.use('PDF')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from scipy.special import erfc
import os, warnings
warnings.filterwarnings('ignore')

# Use SimSun for CJK
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['SimSun', 'SimHei', 'Microsoft YaHei', 'DejaVu Sans'],
    'font.size': 11,
    'axes.labelsize': 13,
    'axes.titlesize': 14,
    'legend.fontsize': 9,
    'figure.dpi': 150,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
    'mathtext.fontset': 'stix',
})

outdir = 'figures'
os.makedirs(outdir, exist_ok=True)

# ============================================================
# Fig 1: Hysteresis loop
# ============================================================
def fig_hysteresis():
    fig, ax = plt.subplots(figsize=(7, 5))
    H = np.linspace(-25, 25, 500)
    Hc, Mr, Ms = 8, 0.85, 1.0
    M_up = Ms * np.tanh(2.5 * (H + Hc) / Hc)
    M_down = Ms * np.tanh(2.5 * (H - Hc) / Hc)
    M = np.where(H >= -0.5, M_up, M_down)
    ax.plot(H, M, 'b-', linewidth=2, label=r'M-H hysteresis')
    ax.axhline(y=Mr, color='red', linestyle='--', alpha=0.7, label=f'$M_r = {Mr}M_s$')
    ax.axhline(y=-Mr, color='red', linestyle='--', alpha=0.7)
    ax.axvline(x=Hc, color='green', linestyle=':', alpha=0.7, label=f'$H_c = {Hc}$ kOe')
    ax.axvline(x=-Hc, color='green', linestyle=':', alpha=0.7)
    ax.axhline(y=Ms, color='gray', linestyle='-', alpha=0.3)
    ax.axhline(y=-Ms, color='gray', linestyle='-', alpha=0.3)
    ax.set_xlabel(r'$H$ [kOe]')
    ax.set_ylabel(r'$M / M_s$')
    ax.set_title(r'Hysteresis Loop of Ferromagnetic Material')
    ax.legend(loc='lower right')
    ax.set_xlim(-22, 22)
    ax.set_ylim(-1.15, 1.15)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(f'{outdir}/fig-hysteresis.pdf')
    plt.close(fig)

# ============================================================
# Fig 2: Stoner-Wohlfarth Astroid
# ============================================================
def fig_astroid():
    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    t = np.linspace(0, 2*np.pi, 500)
    x_astroid = np.cos(t)**3
    y_astroid = np.sin(t)**3
    ax.plot(x_astroid, y_astroid, 'b-', linewidth=2.5, label=r'$h_x^{2/3} + h_z^{2/3} = 1$')
    ax.fill(x_astroid, y_astroid, alpha=0.1, color='blue')
    ax.text(0, -0.3, 'Bistable\n(2 stable states)', ha='center', fontsize=10, color='blue')
    ax.text(1.1, 0.8, 'Monostable', fontsize=10, color='red')
    ax.plot([-1.5, 1.5], [0, 0], 'k-', linewidth=0.5)
    ax.plot([0, 0], [-1.5, 1.5], 'k-', linewidth=0.5)
    ax.annotate(r'$H_c^{\max}=H_K$', xy=(0, -1), xytext=(0.3, -1.15), fontsize=10,
                arrowprops=dict(arrowstyle='->', lw=1.2), ha='center')
    ax.set_xlabel(r'$h_x = H_x / H_K$')
    ax.set_ylabel(r'$h_z = H_z / H_K$')
    ax.set_title("Stoner-Wohlfarth Astroid")
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(f'{outdir}/fig-astroid.pdf')
    plt.close(fig)

# ============================================================
# Fig 3: Arrhenius retention
# ============================================================
def fig_retention():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8))
    T = np.linspace(280, 400, 100)
    tau0, kB = 1e-10, 1.38e-23
    for KV_kBT300 in [40, 50, 60, 70, 80]:
        tau = tau0 * np.exp(KV_kBT300 * 300 / T)
        ax1.semilogy(1000/T, tau/3.15e7, linewidth=1.8, label=f'$K_u V / k_B T_{{300}} = {KV_kBT300}$')
    ax1.axhline(y=10, color='red', linestyle='--', alpha=0.7, label='10 yr requirement')
    ax1.axvline(x=1000/300, color='gray', linestyle=':', alpha=0.5, label='T = 300 K')
    ax1.set_xlabel(r'$1000 / T$ [K$^{-1}$]')
    ax1.set_ylabel('Retention Time [yr]')
    ax1.set_title(r'Arrhenius: $\tau = \tau_0 \exp(K_u V / k_B T)$')
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)

    d = np.linspace(4, 15, 100)
    V = np.pi/6 * d**3 * 1e-27
    for Ku_label, Ku_val in [(r'CoCrPt ($3\times10^5$ J/m$^3$)', 3e5),
                               (r'FePt $L1_0$ ($7\times10^6$ J/m$^3$)', 7e6)]:
        barrier = Ku_val * V / (kB * 300)
        ax2.plot(d, barrier, linewidth=2, label=Ku_label)
    ax2.axhline(y=60, color='red', linestyle='--', alpha=0.7, label=r'$\tau = 10$ yr threshold')
    ax2.set_xlabel(r'Grain Diameter $d$ [nm]')
    ax2.set_ylabel(r'$K_u V / k_B T$')
    ax2.set_title('Energy Barrier vs Grain Size')
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 200)
    fig.tight_layout()
    fig.savefig(f'{outdir}/fig-retention.pdf')
    plt.close(fig)

# ============================================================
# Fig 4: FN tunneling
# ============================================================
def fig_fn_tunneling():
    fig, ax = plt.subplots(figsize=(7.5, 5))
    Eox = np.linspace(0.3e9, 1.5e9, 300)
    A_FN, B_FN = 1.2e-6, 2.35e10
    J = A_FN * Eox**2 * np.exp(-B_FN / Eox)
    ax.semilogy(Eox/1e9, J/1e4, 'b-', linewidth=2.5)
    ax.set_xlabel(r'Oxide Field $E_{ox}$ [GV/m]')
    ax.set_ylabel(r'Current Density $J$ [A/cm$^2$]')
    ax.set_title(r'Fowler-Nordheim Tunneling: $J = A E^2 \exp(-B/E)$')
    ax.axvline(x=0.8, color='green', linestyle='--', alpha=0.5)
    ax.axvline(x=1.1, color='green', linestyle='--', alpha=0.5)
    ax.annotate('Program\n(~100 us)', xy=(1.05, 1e4), fontsize=10, color='green', ha='center',
                bbox=dict(boxstyle='round', fc='green', alpha=0.1))
    ax.annotate('Zero bias\nJ -> 0\n(>10 yr retention)', xy=(0.4, 1e-23), fontsize=10, color='red', ha='center',
                bbox=dict(boxstyle='round', fc='red', alpha=0.1))
    ax.set_ylim(1e-25, 1e7)
    ax.grid(True, alpha=0.3, which='both')
    fig.tight_layout()
    fig.savefig(f'{outdir}/fig-fn-tunneling.pdf')
    plt.close(fig)

# ============================================================
# Fig 5: MLC/TLC/QLC threshold distributions
# ============================================================
def fig_mlc_distributions():
    fig, axes = plt.subplots(3, 1, figsize=(9, 8), sharex=True)
    mu_ranges = [
        ([0.8, 3.5], [0.15, 0.20], 'SLC (2 levels)'),
        ([0.8, 1.6, 2.3, 3.0, 3.7, 4.4, 5.1, 5.8], [0.08]*4 + [0.10]*4, 'TLC (8 levels)'),
        (np.linspace(0.7, 5.5, 16), [0.04]*6 + [0.05]*5 + [0.06]*5, 'QLC (16 levels)'),
    ]
    colors = plt.cm.viridis(np.linspace(0.1, 0.9, 16))
    for ax, (mus, sigmas, title) in zip(axes, mu_ranges):
        V = np.linspace(0, 6.5, 1000)
        for i, (mu, sig) in enumerate(zip(mus, sigmas)):
            pdf = 1/(np.sqrt(2*np.pi)*sig) * np.exp(-(V-mu)**2/(2*sig**2))
            ax.plot(V, pdf, color=colors[i], linewidth=1.2)
            ax.fill_between(V, pdf, alpha=0.15, color=colors[i])
        ax.set_ylabel('PDF')
        ax.set_title(title, fontsize=12)
        ax.grid(True, alpha=0.2)
        ax.set_ylim(bottom=0)
    axes[-1].set_xlabel(r'Threshold Voltage $V_{th}$ [V]')
    axes[0].set_xlim(0.3, 6.2)
    fig.tight_layout()
    fig.savefig(f'{outdir}/fig-mlc-distributions.pdf')
    plt.close(fig)

# ============================================================
# Fig 6: Raw BER vs level spacing
# ============================================================
def fig_raw_ber():
    fig, ax = plt.subplots(figsize=(7, 5))
    delta_V = np.linspace(50, 600, 200)
    for sigma in [30, 50, 70, 100]:
        ber = 0.5 * erfc(delta_V / (2 * np.sqrt(2) * sigma))
        ax.semilogy(delta_V, ber, linewidth=2, label=rf'$\sigma = {sigma}$ mV')
    ax.axhline(y=1e-3, color='red', linestyle='--', alpha=0.5, label='Typical TLC raw BER')
    ax.axhline(y=1e-15, color='green', linestyle='--', alpha=0.5, label='User BER after ECC')
    ax.set_xlabel(r'Level Spacing $\Delta V$ [mV]')
    ax.set_ylabel('Raw Bit Error Rate')
    ax.set_title(r'BER $= \frac{1}{2}\mathrm{erfc}(\Delta V / 2\sqrt{2}\sigma)$')
    ax.legend()
    ax.grid(True, alpha=0.3, which='both')
    ax.set_ylim(1e-20, 1)
    fig.tight_layout()
    fig.savefig(f'{outdir}/fig-raw-ber.pdf')
    plt.close(fig)

# ============================================================
# Fig 7: ReRAM pinched hysteresis
# ============================================================
def fig_reram_iv():
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    t = np.linspace(0, 2*np.pi, 600)
    V = 2.0 * np.sin(t)
    I = V / 200 + 0.008 * np.sin(2*t + 0.5) + 0.012 * np.sin(3*t - 0.3) + 0.005 * np.sin(5*t)
    ax.plot(V, I*1e3, 'b-', linewidth=2)
    ax.set_xlabel(r'Voltage $V$ [V]')
    ax.set_ylabel(r'Current $I$ [mA]')
    ax.set_title('ReRAM Memristor: Pinched Hysteresis I-V')
    ax.axhline(y=0, color='gray', linewidth=0.5)
    ax.axvline(x=0, color='gray', linewidth=0.5)
    ax.annotate('HRS -> LRS\n(SET)', xy=(1.2, 4), fontsize=10, color='red', ha='center',
                bbox=dict(boxstyle='round', fc='red', alpha=0.1))
    ax.annotate('LRS -> HRS\n(RESET)', xy=(-0.9, -4), fontsize=10, color='blue', ha='center',
                bbox=dict(boxstyle='round', fc='blue', alpha=0.1))
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(f'{outdir}/fig-reram-iv.pdf')
    plt.close(fig)

# ============================================================
# Fig 8: TMR RA vs MgO thickness
# ============================================================
def fig_tmr():
    fig, ax = plt.subplots(figsize=(7, 5))
    d = np.linspace(0.6, 2.5, 100)
    kappa_d1, kappa_d5 = 2.2, 6.0  # per nm
    RA_P = 0.05 * np.exp(kappa_d1 * d)
    RA_AP = 0.05 * np.exp(kappa_d5 * d)
    ax.semilogy(d, RA_P, 'b-', linewidth=2, label=r'Parallel $R_P A$ ($\Delta_1$ symmetry)')
    ax.semilogy(d, RA_AP, 'r-', linewidth=2, label=r'Anti-Parallel $R_{AP} A$ ($\Delta_5$ symmetry)')
    ax.set_xlabel(r'MgO Thickness $d$ [nm]')
    ax.set_ylabel(r'RA Product [$\Omega\cdot\mu$m$^2$]')
    ax.set_title(r'MgO(001) MTJ: Bloch State Symmetry Filtering')
    ax.legend()
    ax.grid(True, alpha=0.3, which='both')
    ax.annotate('TMR > 600%\n(d ~ 1.2 nm)', xy=(1.2, 50), fontsize=11, ha='center',
                bbox=dict(boxstyle='round', fc='yellow', alpha=0.3))
    fig.tight_layout()
    fig.savefig(f'{outdir}/fig-tmr-ra.pdf')
    plt.close(fig)

# ============================================================
# Fig 9: Endurance degradation
# ============================================================
def fig_endurance():
    fig, ax = plt.subplots(figsize=(7.5, 5))
    cycles = np.logspace(0, 5, 100)
    Vth_erase = 0.8 + 0.015 * cycles**0.45
    Vth_prog = 3.5 - 0.010 * cycles**0.50
    ax.semilogx(cycles, Vth_erase, 'b-', linewidth=2, label=r'Erased state $V_{th}$ (drifts up)')
    ax.semilogx(cycles, Vth_prog, 'r-', linewidth=2, label=r'Programmed state $V_{th}$ (drifts down)')
    ax.fill_between(cycles, Vth_erase, Vth_prog, alpha=0.15, color='green')
    ax.set_xlabel('P/E Cycles')
    ax.set_ylabel(r'Threshold Voltage $V_{th}$ [V]')
    ax.set_title('Flash Endurance Degradation: Threshold Window Closing')
    ax.annotate('Window closes\n(no distinction)', xy=(30000, 2.15), fontsize=11, ha='center',
                bbox=dict(boxstyle='round', fc='red', alpha=0.15))
    ax.annotate('Usable window', xy=(50, 2.6), fontsize=11, color='green')
    ax.legend()
    ax.grid(True, alpha=0.3, which='both')
    ax.set_ylim(0.3, 4.5)
    fig.tight_layout()
    fig.savefig(f'{outdir}/fig-endurance.pdf')
    plt.close(fig)

# ============================================================
# Fig 10: Optical spot size vs wavelength (bubble chart)
# ============================================================
def fig_optical_evolution():
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    fmt_names = ['CD (1982)', 'DVD (1996)', 'BD (2006)', 'SIL-NFR (future)']
    wavelengths = [780, 650, 405, 405]
    NAs = [0.45, 0.60, 0.85, 1.8]
    spot_sizes = [0.61 * wl / na / 1000 for wl, na in zip(wavelengths, NAs)]
    capacities = [0.7, 4.7, 25, 200]
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#9b59b6']
    for i, (fmt, wl, na, ss, cap) in enumerate(zip(fmt_names, wavelengths, NAs, spot_sizes, capacities)):
        ax.scatter(wl, na, s=cap*35, c=colors[i], alpha=0.7, edgecolors='black', linewidth=1.5, zorder=5)
        offset = 20 if i < 2 else -30
        ax.annotate(f'{fmt}\nspot={ss:.2f}um {cap}GB', (wl, na),
                    textcoords="offset points", xytext=(15, offset), fontsize=9, ha='left')
    ax.set_xlabel(r'Wavelength $\lambda$ [nm]')
    ax.set_ylabel('Numerical Aperture NA')
    ax.set_title(r'Optical Storage Evolution: $\lambda\downarrow$, NA$\uparrow$')
    ax.set_xlim(350, 850)
    ax.set_ylim(0.3, 2.2)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(f'{outdir}/fig-optical-evolution.pdf')
    plt.close(fig)

# ============================================================
# Fig 11: Landauer principle - energy landscapes
# ============================================================
def fig_landauer():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))
    x = np.linspace(-2, 2, 200)
    E_before = 0.5 * (x**2 - 1.5)**2 - 0.3*x
    ax1.plot(x, E_before, 'b-', linewidth=2.5)
    ax1.set_title(r'Before Erasure: Bistable ($S_0$ or $S_1$)')
    ax1.set_xlabel('Generalized coordinate')
    ax1.set_ylabel('Free Energy')
    ax1.annotate(r'$S_0$ (bit=0)', xy=(-1.2, -0.05), fontsize=11, ha='center')
    ax1.annotate(r'$S_1$ (bit=1)', xy=(1.2, 0.15), fontsize=11, ha='center')
    ax1.grid(True, alpha=0.2)
    E_after = 0.5 * (x**2 - 1.5)**2 - 0.8*x + 1.0
    ax2.plot(x, E_after, 'r-', linewidth=2.5)
    ax2.set_title(r'After Erasure: Monostable ($\to S_0$)')
    ax2.set_xlabel('Generalized coordinate')
    ax2.set_ylabel('Free Energy')
    ax2.annotate(r'$S_0$', xy=(-1.2, 0.5), fontsize=11, ha='center')
    ax2.annotate(r'$\Delta E_{\min} = k_B T \ln 2$', xy=(0.5, 2.8), fontsize=12, ha='center',
                bbox=dict(boxstyle='round', fc='yellow', alpha=0.4))
    ax2.grid(True, alpha=0.2)
    fig.tight_layout()
    fig.savefig(f'{outdir}/fig-landauer.pdf')
    plt.close(fig)

# ============================================================
# Fig 12: PCM SET/RESET pulses
# ============================================================
def fig_pcm_pulses():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))
    t = np.linspace(0, 200, 300)
    I_reset = np.zeros_like(t); I_reset[(t > 20) & (t < 70)] = 0.8
    T_reset = np.zeros_like(t)
    mask = (t > 20) & (t < 70)
    T_reset[mask] = 300 + 900 * (1 - np.exp(-(t[mask]-20)/5))
    idx70 = np.argmax(t >= 70)
    T_reset[t >= 70] = T_reset[idx70] * np.exp(-(t[t >= 70]-70)/15)
    ax1a = ax1.twinx()
    ax1.plot(t, I_reset*1000, 'r-', linewidth=2)
    ax1a.plot(t, T_reset, 'b-', linewidth=2)
    ax1.set_xlabel('Time [ns]')
    ax1.set_ylabel('Current [mA]', color='red')
    ax1a.set_ylabel('Temperature [C]', color='blue')
    ax1.set_title('RESET (Amorphization): Short pulse + fast quench')
    ax1.set_ylim(-20, 1000); ax1a.set_ylim(200, 1400)
    ax1.grid(True, alpha=0.2)
    I_set = np.zeros_like(t); I_set[(t > 30) & (t < 130)] = 0.25
    T_set = np.zeros_like(t)
    mask2 = (t > 30) & (t < 130)
    T_set[mask2] = 300 + 400 * (1 - np.exp(-(t[mask2]-30)/15))
    idx130 = np.argmax(t >= 130)
    T_set[t >= 130] = T_set[idx130] * np.exp(-(t[t >= 130]-130)/30)
    ax2a = ax2.twinx()
    ax2.plot(t, I_set*1000, 'r-', linewidth=2)
    ax2a.plot(t, T_set, 'b-', linewidth=2)
    ax2.set_xlabel('Time [ns]')
    ax2.set_ylabel('Current [mA]', color='red')
    ax2a.set_ylabel('Temperature [C]', color='blue')
    ax2.set_title('SET (Crystallization): Long pulse + slow cool')
    ax2.set_ylim(-20, 350); ax2a.set_ylim(200, 800)
    ax2.grid(True, alpha=0.2)
    fig.tight_layout()
    fig.savefig(f'{outdir}/fig-pcm-pulses.pdf')
    plt.close(fig)

# ============================================================
# Fig 13: Technology comparison bar chart
# ============================================================
def fig_tech_comparison():
    fig, ax = plt.subplots(figsize=(9, 5.5))
    techs = ['HDD\n(PMR)', 'NAND\n(TLC)', 'STT-\nMRAM', 'ReRAM\n(VCM)', 'PCM', 'FeFET']
    metrics_data = {
        'Write Speed\n(log ns)':    [1,  0,  9,  8,  5,  7],
        'Endurance\n(log cycles)':  [9,  3,  9,  6,  6,  4],
        'Cell Area\n(inv F2)':      [0,  8,  3,  7,  7,  7],
        'Retention\n(log yr)':      [8,  8,  8,  6,  8,  6],
    }
    x = np.arange(len(techs))
    width = 0.18
    colors_bar = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12']
    for i, (metric, vals) in enumerate(metrics_data.items()):
        offset = (i - 1.5) * width
        ax.bar(x + offset, vals, width, label=metric, color=colors_bar[i], alpha=0.85, edgecolor='white')
    ax.set_xticks(x)
    ax.set_xticklabels(techs, fontsize=10)
    ax.set_ylabel('Relative Score (higher is better)')
    ax.set_title('Storage Technology Physics Comparison')
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(True, alpha=0.2, axis='y')
    ax.set_ylim(0, 11)
    fig.tight_layout()
    fig.savefig(f'{outdir}/fig-tech-comparison.pdf')
    plt.close(fig)

# ============================================================
# Fig 14: Magnetic recording trilemma illustration
# ============================================================
def fig_trilemma():
    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    theta = np.linspace(0, 2*np.pi, 300)
    r = 1 + 0.15*np.sin(3*theta)
    x, y = r*np.cos(theta), r*np.sin(theta)
    ax.plot(x, y, 'gray', linewidth=1, alpha=0.3)
    ax.fill(x, y, alpha=0.05, color='gray')
    points = {
        'Density\n(smaller grains)': (0, 1.1),
        'Stability\n(Ku*V >> kT)': (-0.95, -0.55),
        'Writability\n(H_write > H_c)': (0.95, -0.55),
    }
    for label, (px, py) in points.items():
        ax.plot(px, py, 'o', markersize=15, color='red', alpha=0.6)
        ax.annotate(label, (px, py), textcoords="offset points", xytext=(0, 15 if py > 0 else -20),
                    fontsize=12, ha='center', fontweight='bold')
    ax.text(0, 0, 'Trilemma', fontsize=14, ha='center', fontweight='bold', color='red', alpha=0.5)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Magnetic Recording Trilemma', fontsize=14)
    fig.tight_layout()
    fig.savefig(f'{outdir}/fig-trilemma.pdf')
    plt.close(fig)

if __name__ == '__main__':
    print('Generating figures...')
    for fn in [fig_hysteresis, fig_astroid, fig_retention, fig_fn_tunneling,
                fig_mlc_distributions, fig_raw_ber, fig_reram_iv, fig_tmr,
                fig_endurance, fig_optical_evolution, fig_landauer, fig_pcm_pulses,
                fig_tech_comparison, fig_trilemma]:
        try:
            fn()
            print(f'  OK: {fn.__name__}')
        except Exception as e:
            print(f'  FAIL: {fn.__name__}: {e}')
    n = len(os.listdir(outdir))
    print(f'Done! {n} figures in {outdir}/')
