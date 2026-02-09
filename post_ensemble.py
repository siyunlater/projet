# post_ensemble.py
import pandas as pd
import numpy as np
import matplotlib as plt
from pathlib import Path

N_BATCH = 100
N_PARTICLE = 10000
SIZE = N_BATCH * N_PARTICLE

size_dir = f"N={SIZE}"
runs_dir = Path(size_dir+"/runs")

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

df = pd.DataFrame({
    "fission_mean": [f_mean],
    "fission_std": [f_std],
    "fission_sem": [f_sem],
    "heating_mean": [h_mean],
    "heating_std": [h_std],
    "heating_sem": [h_sem]
})

print("FISSION:")
print(f" mean = {f_mean:.4e}")
print(f" std  = {f_std:.4e}")
print(f" SEM  = {f_sem:.4e}")

print("HEATING:")
print(f" mean = {h_mean:.4e}")
print(f" std  = {h_std:.4e}")
print(f" SEM  = {h_sem:.4e}")

# Ensemble size validation
#print("\nEnsemble size (M) validation (fission std):")
#for M in [5, 10, 20, 30]:
#    if len(fission_vals) >= M:
#        _, std, _ = stats(fission_vals[:M])
#        print(f"M={M:2d} → std = {std:.4e}")
#
#        valid_dict = {}
#for M in [5, 10, 20, 30]:
#    if len(fission_vals) >= M:
#        _, std, _ = stats(fission_vals[:M])
#        valid_dict[f"M = {M}"] = std
#    else:
#        valid_dict[f"M = {M}"] = np.nan
#
#df_valid = pd.DataFrame({
#    "ensemble_size": list(valid_dict.keys()),
#    "fission_std": list(valid_dict.values())
#})
#
# Save main stats
df.to_csv("results/ensemble_stats.csv", index=False)

# Save validation separately or append
#df_valid.to_csv("results/ensemble_validation.csv", index=False)
