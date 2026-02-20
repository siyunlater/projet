# ensemble_analysis.py
import openmc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from pathlib import Path

N_BATCH = 100
N_PARTICLE = 50000

SIZE = N_BATCH * N_PARTICLE
runs_dir = Path("Part_A_B/runs")

f_means = []
f_stds = []
h_means = []
h_stds = []
times = []

for run in sorted(runs_dir.glob("run_*")):
    df = pd.read_csv(run / "results.csv")
    f_means.append(df["fission_total_mean"].iloc[0])
    f_stds.append(df["fission_total_std"].iloc[0])
    h_means.append(df["heating_total_mean"].iloc[0])
    h_stds.append(df["heating_total_std"].iloc[0])

    sp = openmc.StatePoint(run / "statepoint.100.h5")
    times.append(sp.runtime["simulation"])

f_means = np.array(f_means)
f_stds = np.array(f_stds)
h_means = np.array(h_means)
h_stds = np.array(h_stds)
T = np.mean(times)

f_mean = np.mean(f_means)
f_std = np.mean(f_stds)
h_mean = np.mean(h_means)
h_std = np.mean(h_stds)

f_rel_sigma = f_std / f_mean
h_rel_sigma = h_std / h_mean
f_FoM = 1.0 / (f_rel_sigma**2 * T)
h_FoM = 1.0 / (h_rel_sigma**2 * T)

#print(f"N = {SIZE}")
print(f"Ensemble mean (fission rate) = {f_mean:.4e}")
print(f"Ensemble std (fission rate)  = {f_std:.4e}")
print(f"Relative σ (fission rate)    = {f_rel_sigma:.4e}")
print(f"FoM  (fission rate)          = {f_FoM:.4e}")
print(f"Ensemble mean (heating) = {h_mean:.4e}")
print(f"Ensemble std (heating)  = {h_std:.4e}")
print(f"Relative σ (heating)    = {h_rel_sigma:.4e}")
print(f"FoM  (heating)          = {h_FoM:.4e}")

# --- histogram ---
plt.figure(figsize=(7,5))
plt.hist(f_means, bins=10, density=True, alpha=0.6, label="Ensemble")

x = np.linspace(f_means.min(), f_means.max(), 200)
pdf = norm.pdf(x, f_mean, f_std)
plt.plot(x, pdf, 'r-', lw=2, label="Gaussian fit")

plt.xlabel("Fission total")
plt.ylabel("Probability density")
plt.legend()
plt.tight_layout()
plt.savefig("Part_A_B/results/ensemble_histogram.png", dpi=300)
plt.show()

# --- ensemble size validation ---
print("\nEnsemble size validation:")
for M in [5, 10, 20]:
    if len(f_means) >= M:
        subset = f_means[:M]
        std_M = np.std(subset, ddof=1)
        print(f"M={M:2d} → std = {std_M:.4e}")
