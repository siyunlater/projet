import openmc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


N_RUNS = 20  # M
N_BATCH = np.array([100, 200, 500, 1000])
N_PARTICLE = 10000 #np.array([10000, 50000, 100000, 500000])

BASE_DIR = Path(__file__).resolve().parent

values = []
times = []

all_results = []

VAL = 'fission_total' # or heating 

for n_batch in N_BATCH:
    size = N_PARTICLE * n_batch
    runs_dir = Path(f"N={size}" + "/runs")

    for run in runs_dir.glob("run_*"):
        df = pd.read_csv(run / "results.csv")
        values.append(df[VAL].iloc[0])

        # --- time from OpenMC ---
        sp = openmc.StatePoint(run / "statepoint.100.h5")
        sim_time = sp.runtime["simulation"]
        times.append(sim_time)

    #values = np.array(values)
    #times = np.array(times)

    # --- ensemble statistics ---
    mean = np.mean(values)
    std = np.std(values, ddof=1)
    rel_std = std / mean

    # --- average simulation time ---
    T = np.mean(times)

    # --- Figure of Merit ---
    FoM = 1.0 / (rel_std**2 * T)

    results = {
        "N" : size,
        "batch": N_BATCH,
        "particle": n_particle,
        "Mean value": mean,
        "Std ensemble": std,
        "Relative std": rel_std,
        "Mean time": T,
        "FoM": FoM
    }
    all_results.append(results)

df = pd.DataFrame(all_results)
df.to_csv("results/Figure_of_Merit.csv", index=False)

# --- Plot for ensemble ---
# Extract data for plotting (remove NaN values)
plot_df = df[df['FoM'].notna()]
sizes = plot_df['N'].values
figure_of_merit = plot_df['FoM'].values

if len(sizes) > 1:    
    plt.figure(figsize=(7, 5))
    plt.loglog(sizes, figure_of_merit, 'o-', label="Ensemble fission σ")
    plt.xlabel("Total number of histories (N)")
    plt.ylabel("Figure of Merit")
    plt.grid(True, which="both", ls="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig("results/FoM_vs_N_ensemble.png", dpi=300)
    plt.show()
else:
    print("Not enough data points for plotting")