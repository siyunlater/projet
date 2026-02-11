import openmc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

N_RUNS = 20
N_BATCH = 100
N_PARTICLE = np.array([10000, 50000, 100000, 500000])

BASE_DIR = Path(__file__).resolve().parent

sizes = []
fission_vals = []
heating_vals = []
fission_rel_sigma = []
heating_rel_sigma = []

for n_particle in N_PARTICLE:
    SIZE = N_BATCH * n_particle
    size_dir = BASE_DIR / f"N={SIZE}"
    runs_dir = size_dir / "runs"

    # single run statepoint
#    sp = openmc.StatePoint(runs_dir / "run_001/statepoint.100.h5")
#
#    fission = sp.get_tally(scores=["fission"])
#
#    mean = fission.mean.sum()
#    std = fission.std_dev.sum()
#
#    rel_sigma = std / mean
#
#    sizes.append(SIZE)
#    fission_rel_sigma.append(rel_sigma)

    # ensemble stats
    for run in sorted(runs_dir.glob("run_*")):
        csv_file = run / "results.csv"
        if not csv_file.exists():
            print(f"Skipping {run}, no results.csv")
            continue

        df = pd.read_csv(csv_file)
        fission_vals.append(df["fission_total"].iloc[0])
        heating_vals.append(df["heating_total"].iloc[0])

    size = SIZE
    fission_vals = np.array(fission_vals)
    heating_vals = np.array(heating_vals)

    def stats(x):
        mean = np.mean(x)
        std = np.std(x, ddof=1)
        sem = std / np.sqrt(len(x))
        return mean, std, sem

    f_mean, f_std, f_sem = stats(fission_vals)
    h_mean, h_std, h_sem = stats(heating_vals)

    fission_rel_sigma.append(f_sem / f_mean)
    heating_rel_sigma.append(h_sem / h_mean)

    df = pd.DataFrame({
        "fission_mean": [f_mean],
        "fission_std": [f_std],
        "fission_sem": [f_sem],
        "heating_mean": [h_mean],
        "heating_std": [h_std],
        "heating_sem": [h_sem]
    })

# --- plot single run ---

#coef = np.polyfit(np.log10(sizes), np.log10(fission_rel_sigma), 1)
#print(f"Slope ≈ {coef[0]:.2f}")
#
#slope = coef[0]
#
#plt.figure(figsize=(7,5))
#plt.loglog(sizes, fission_rel_sigma, 'o-', label="Single-run fission σ")
#plt.xlabel("Total number of histories (N)")
#plt.ylabel("Relative statistical uncertainty σ")
#plt.grid(True, which="both", ls="--", alpha=0.6)
#plt.text(
#    0.05, 0.95,
#    rf"Slope = {slope:.2f}",
#    transform=plt.gca().transAxes,
#    fontsize=11,
#    verticalalignment="top",
#    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
#)
#plt.legend()
#plt.tight_layout()
#plt.savefig("sigma_vs_N_single_run.png", dpi=300)

# --- Plot for ensemble ---
coef = np.polyfit(np.log10(sizes), np.log10(fission_rel_sigma), 1)
print(f"Slope ≈ {coef[0]:.2f}")
slope = coef[0]

plt.figure(figsize=(7,5))
plt.loglog(sizes, fission_rel_sigma, 'o-', label="Ensemble fission σ")
plt.xlabel("Total number of histories (N)")
plt.ylabel("Relative statistical uncertainty σ")
plt.grid(True, which="both", ls="--", alpha=0.6)
plt.text(
    0.05, 0.95,
    rf"Slope = {slope:.2f}",
    transform=plt.gca().transAxes,
    fontsize=11,
    verticalalignment="top",
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
)
plt.legend()
plt.tight_layout()
plt.savefig("sigma_vs_N_ensemble.png", dpi=300)