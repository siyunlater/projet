# scaling_ensemble.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

N_BATCH = np.array([100, 200, 500, 1000])
N_PARTICLE = 10000

BASE_DIR = Path(__file__).resolve().parent

sizes = []
fission_rel_sigma = []
heating_rel_sigma = []

def stats(x):
    mean = np.mean(x)
    std = np.std(x, ddof=1)
    return mean, std

for n_batch in N_BATCH:

    SIZE = n_batch * N_PARTICLE
    runs_dir = BASE_DIR / f"N={SIZE}" / "runs"

    fission_vals = []
    heating_vals = []

    for run in sorted(runs_dir.glob("run_*")):
        csv_file = run / "results.csv"
        if not csv_file.exists():
            continue

        df = pd.read_csv(csv_file)
        fission_vals.append(df["fission_total"].iloc[0])
        heating_vals.append(df["heating_total"].iloc[0])

    if len(fission_vals) < 2:
        print(f"Skipping N={SIZE}, not enough runs")
        continue

    f_mean, f_std = stats(fission_vals)
    h_mean, h_std = stats(heating_vals)

    sizes.append(SIZE)
    fission_rel_sigma.append(f_std / f_mean)
    heating_rel_sigma.append(h_std / h_mean)

sizes = np.array(sizes)
fission_rel_sigma = np.array(fission_rel_sigma)

coef = np.polyfit(np.log10(sizes), np.log10(fission_rel_sigma), 1)
slope = coef[0]

print(f"Ensemble slope ≈ {slope:.2f}")

plt.figure(figsize=(7,5))
plt.loglog(sizes, fission_rel_sigma, 'o-', label="Ensemble fission σ")
plt.loglog(sizes, heating_rel_sigma, 's--', label="Ensemble heating σ")

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
plt.savefig("results/sigma_vs_N_ensemble.png", dpi=300)
plt.show()
