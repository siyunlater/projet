import openmc
import numpy as np
import pandas as pd
from pathlib import Path

runs_dir = Path("runs")

values = []
times = []

VAL = 'fission_total' # or heating 

for run in runs_dir.glob("run_*"):
    df = pd.read_csv(run / "results.csv")
    values.append(df[VAL].iloc[0])

    # --- time from OpenMC ---
    sp = openmc.StatePoint(run / "statepoint.100.h5")
    sim_time = sp.runtime["simulation"]
    times.append(sim_time)

values = np.array(values)
times = np.array(times)

# --- ensemble statistics ---
mean = np.mean(values)
std = np.std(values, ddof=1)
rel_std = std / mean

# --- average simulation time ---
T = np.mean(times)

# --- Figure of Merit ---
FoM = 1.0 / (rel_std**2 * T)

df_time = pd.DataFrame({
    "Mean value": [mean],
    "Std ensemble": [std],
    "Relative std": [rel_std],
    "Mean time": [T],
    "FoM": [FoM]
})
df_time.to_csv("results/Figure_of_Merit.csv", index=False)

print("=== Ensemble FoM ===")
print(f"Mean value        = {mean:.5e}")
print(f"Std (ensemble)    = {std:.5e}")
print(f"Relative std      = {rel_std:.5e}")
print(f"Mean time [s]     = {T:.2f}")
print(f"FoM               = {FoM:.5e}")
