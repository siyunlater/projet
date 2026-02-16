import openmc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
runs_dir = BASE_DIR / "runs"

density = np.array([0.99, 0.995, 1.0, 1.005, 1.01])

means_ref = []
sigmas_ref = []

ref_dir = runs_dir / "dens_003"
for run in sorted(ref_dir.glob("run_*")):
    sp_ref_file = run / "statepoint.100.h5"
    sp_ref = openmc.StatePoint(sp_ref_file)
    tally_ref = sp_ref.get_tally(scores=["fission"])

    mean_ref = tally_ref.mean.sum()
    std_ref = tally_ref.std_dev.sum()

    means_ref.append(mean_ref)
    sigmas_ref.append(std_ref)

mean_ref = np.mean(means_ref)
sigma_ref = np.mean(sigmas_ref)

deltas = []
detects = []

for dens_dir in sorted(runs_dir.glob("dens_*")):
    means = []
    sigmas = []

    for run in sorted(dens_dir.glob("run_*")):
        csv_file = run / "results.csv"
        sp_file = run / "statepoint.100.h5"
        df = pd.read_csv(csv_file)
        sp = openmc.StatePoint(sp_file)
        tally = sp.get_tally(scores=["fission"])

        mean = tally.mean.sum()
        std = np.sqrt((tally.std_dev**2).sum())

        means.append(mean)
        sigmas.append(std)

    mean_pert = np.mean(means)
    sigma_pert = np.mean(sigmas)

    sigma_mc = np.sqrt(sigma_ref**2 + sigma_pert**2)

    delta_phys = abs(mean_pert - mean_ref)
    deltas.append(delta_phys)

    detect = delta_phys / sigma_pert
    detects.append(detect)

delta_rho = density - 1.0
mask = delta_rho != 0

deltas = np.array(deltas)
detects = np.array(detects)

fig, ax1 = plt.subplots(figsize=(10, 6))

# First y-axis (left) - for fission
color1 = 'tab:blue'
ax1.set_xlabel('Density perturbation')
ax1.set_ylabel('Delta - perturbation', color=color1)
ax1.plot(delta_rho[mask], deltas[mask], 'o-', label='delta')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.grid(True, alpha=0.3)

# Second y-axis (right) - for heating
ax2 = ax1.twinx()
color2 = 'tab:red'
ax2.set_ylabel('Detectability', color=color2)
ax2.plot(delta_rho[mask], detects[mask], 's-', color=color2, label='Detectability')
ax2.tick_params(axis='y', labelcolor=color2)

# Combine legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

plt.tight_layout()
plt.savefig("results/density_perturbation.png", dpi=300)
plt.show()
