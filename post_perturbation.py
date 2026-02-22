import openmc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
runs_dir = BASE_DIR / "runs"

density = np.array([0.99, 0.995, 1.0, 1.005, 1.01])

f_means_ref = []
f_sigmas_ref = []
h_means_ref = []
h_sigmas_ref = []

ref_dir = runs_dir / "dens_003"
for run in sorted(ref_dir.glob("run_*")):
    sp_ref_file = run / "statepoint.100.h5"
    sp_ref = openmc.StatePoint(sp_ref_file)
    f_tally_ref = sp_ref.get_tally(scores=["fission"])
    h_tally_ref = sp_ref.get_tally(scores=["heating"])

    f_mean_ref = f_tally_ref.mean.sum()
    f_std_ref = f_tally_ref.std_dev.sum()
    h_mean_ref = h_tally_ref.mean.sum()
    h_std_ref = h_tally_ref.std_dev.sum()

    f_means_ref.append(f_mean_ref)
    f_sigmas_ref.append(f_std_ref)
    h_means_ref.append(h_mean_ref)
    h_sigmas_ref.append(h_std_ref)

f_mean_ref = np.mean(f_means_ref)
f_sigma_ref = np.mean(f_sigmas_ref)
h_mean_ref = np.mean(h_means_ref)
h_sigma_ref = np.mean(h_sigmas_ref)

f_deltas = []
f_detects = []
h_deltas = []
h_detects = []

for dens_dir in sorted(runs_dir.glob("dens_*")):
    f_means = []
    f_sigmas = []
    h_means = []
    h_sigmas = []

    for run in sorted(dens_dir.glob("run_*")):
        csv_file = run / "results.csv"
        sp_file = run / "statepoint.100.h5"
        df = pd.read_csv(csv_file)
        sp = openmc.StatePoint(sp_file)
        f_tally = sp.get_tally(scores=["fission"])
        h_tally = sp.get_tally(scores=["heating"])

        f_mean = f_tally.mean.sum()
        f_std = np.sqrt((f_tally.std_dev**2).sum())
        h_mean = h_tally.mean.sum()
        h_std = np.sqrt((h_tally.std_dev**2).sum())

        f_means.append(f_mean)
        f_sigmas.append(f_std)
        h_means.append(h_mean)
        h_sigmas.append(h_std)

    f_mean_pert = np.mean(f_means)
    f_sigma_pert = np.mean(f_sigmas)
    h_mean_pert = np.mean(h_means)
    h_sigma_pert = np.mean(h_sigmas)

    f_sigma_mc = np.sqrt(f_sigma_ref**2 + f_sigma_pert**2)
    h_sigma_mc = np.sqrt(h_sigma_ref**2 + h_sigma_pert**2)

    f_delta_phys = abs(f_mean_pert - f_mean_ref)
    f_deltas.append(f_delta_phys)
    h_delta_phys = abs(h_mean_pert - h_mean_ref)
    h_deltas.append(h_delta_phys)

    f_detect = f_delta_phys / f_sigma_pert
    f_detects.append(f_detect)
    h_detect = h_delta_phys / h_sigma_pert
    h_detects.append(h_detect)

delta_rho = density - 1.0
mask = delta_rho != 0

f_deltas = np.array(f_deltas)
f_detects = np.array(f_detects)
h_deltas = np.array(h_deltas)
h_detects = np.array(h_detects)

fig1, ax1 = plt.subplots(figsize=(10, 6))

# First y-axis (left) - for fission
color1 = 'tab:blue'
ax1.set_xlabel('Density perturbation')
ax1.set_ylabel('Delta - perturbation', color=color1)
ax1.plot(delta_rho[mask], f_deltas[mask], 'o-', label='delta')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.grid(True, alpha=0.3)

# Second y-axis (right) - for detectability
ax2 = ax1.twinx()
color2 = 'tab:red'
ax2.set_ylabel('Detectability', color=color2)
ax2.plot(delta_rho[mask], f_detects[mask], 's-', color=color2, label='Detectability')
ax2.tick_params(axis='y', labelcolor=color2)

# Combine legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

plt.tight_layout()
plt.savefig("results/density_perturbation_fission.png", dpi=300)
plt.show()

fig2, ax3 = plt.subplots(figsize=(10, 6))
# First y-axis (left) - for heating
color1 = 'tab:blue'
ax3.set_xlabel('Density perturbation')
ax3.set_ylabel('Delta - perturbation', color=color1)
ax3.plot(delta_rho[mask], h_deltas[mask], 'o-', label='delta')
ax3.tick_params(axis='y', labelcolor=color1)
ax3.grid(True, alpha=0.3)

# Second y-axis (right) - for detectability
ax4 = ax3.twinx()
color2 = 'tab:red'
ax4.set_ylabel('Detectability', color=color2)
ax4.plot(delta_rho[mask], h_detects[mask], 's-', color=color2, label='Detectability')
ax4.tick_params(axis='y', labelcolor=color2)

# Combine legends
lines1, labels1 = ax3.get_legend_handles_labels()
lines2, labels2 = ax4.get_legend_handles_labels()
ax3.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

plt.tight_layout()
plt.savefig("results/density_perturbation_heating.png", dpi=300)
plt.show()
