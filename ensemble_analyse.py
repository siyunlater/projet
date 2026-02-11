# ensemble_analysis.py
import openmc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from pathlib import Path

N_BATCH = 100
N_PARTICLE = 10000

SIZE = N_BATCH * N_PARTICLE
runs_dir = Path(f"N={SIZE}/runs")

fission_vals = []
times = []

for run in sorted(runs_dir.glob("run_*")):
    df = pd.read_csv(run / "results.csv")
    fission_vals.append(df["fission_total"].iloc[0])

    sp = openmc.StatePoint(run / "statepoint.100.h5")
    times.append(sp.runtime["simulation"])

fission_vals = np.array(fission_vals)
T = np.mean(times)

mean = np.mean(fission_vals)
std = np.std(fission_vals, ddof=1)
rel_sigma = std / mean

FoM = 1.0 / (rel_sigma**2 * T)

print(f"N = {SIZE}")
print(f"Ensemble mean = {mean:.4e}")
print(f"Ensemble std  = {std:.4e}")
print(f"Relative σ    = {rel_sigma:.4e}")
print(f"FoM           = {FoM:.4e}")

# --- histogram ---
plt.figure(figsize=(7,5))
plt.hist(fission_vals, bins=10, density=True, alpha=0.6, label="Ensemble")

x = np.linspace(fission_vals.min(), fission_vals.max(), 200)
pdf = norm.pdf(x, mean, std)
plt.plot(x, pdf, 'r-', lw=2, label="Gaussian fit")

plt.xlabel("Fission total")
plt.ylabel("Probability density")
plt.legend()
plt.tight_layout()
plt.savefig("ensemble_histogram.png", dpi=300)
plt.show()

# --- ensemble size validation ---
print("\nEnsemble size validation:")
for M in [5, 10, 20]:
    if len(fission_vals) >= M:
        subset = fission_vals[:M]
        std_M = np.std(subset, ddof=1)
        print(f"M={M:2d} → std = {std_M:.4e}")
