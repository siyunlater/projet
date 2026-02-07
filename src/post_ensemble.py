# post_ensemble.py
import pandas as pd
import numpy as np
from pathlib import Path

runs_dir = Path("runs")

fission_vals = []
heating_vals = []

for run in sorted(runs_dir.glob("run_*")):
    csv_file = run / "results.csv"
    if not csv_file.exists():
        print(f"Skipping {run}, no results.csv")
        continue

    df = pd.read_csv(csv_file)
    fission_vals.append(df["fission_total"].iloc[0])
    heating_vals.append(df["heating_total"].iloc[0])

fission_vals = np.array(fission_vals)
heating_vals = np.array(heating_vals)

def stats(x):
    mean = np.mean(x)
    std = np.std(x, ddof=1)
    sem = std / np.sqrt(len(x))
    return mean, std, sem

f_mean, f_std, f_sem = stats(fission_vals)
h_mean, h_std, h_sem = stats(heating_vals)

print("FISSION:")
print(f" mean = {f_mean:.4e}")
print(f" std  = {f_std:.4e}")
print(f" SEM  = {f_sem:.4e}")

print("HEATING:")
print(f" mean = {h_mean:.4e}")
print(f" std  = {h_std:.4e}")
print(f" SEM  = {h_sem:.4e}")

# Ensemble size validation
print("\nEnsemble size validation (fission std):")
for N in [5, 10, 20, 30]:
    if len(fission_vals) >= N:
        _, std, _ = stats(fission_vals[:N])
        print(f"N={N:2d} → std = {std:.4e}")
