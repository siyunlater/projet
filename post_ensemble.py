# post_ensemble.py
import openmc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

N_RUNS = 20  # M
N_BATCH = np.array([100, 200, 500, 1000])
N_PARTICLE = 10000 #np.array([10000, 50000, 100000, 500000])

fission_rel_sigma = []
heating_rel_sigma = []

values = []
times = []

VAL = 'fission_total' # or heating 

all_results = []

def stats(x):
    if len(x) < 2:
        return np.mean(x), np.nan, np.nan
    mean = np.mean(x)
    std = np.std(x, ddof=1)
    sem = std / np.sqrt(len(x))
    return mean, std, sem

for n_batch in N_BATCH:
    size = N_PARTICLE * n_batch
    runs_dir = Path(f"N={size}" + "/runs")

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

        # --- time from OpenMC ---
        sp = openmc.StatePoint(run / "statepoint.100.h5")
        sim_time = sp.runtime["simulation"]
        times.append(sim_time)

    # --- average simulation time ---
    T = np.mean(times)
    # --- Figure of Merit ---
    FoM = 1.0 / (rel_std**2 * T)

    f_mean, f_std, f_sem = stats(fission_vals)
    h_mean, h_std, h_sem = stats(heating_vals)

    fission_rel_sigma.append(f_sem / f_mean)
    heating_rel_sigma.append(h_sem / h_mean)

    results = {
        "N" : size,
        "batch": n_batch,
        "particle": N_PARTICLE,
        "fission_mean": f_mean,
        "fission_std": f_std,
        "fission_sem": f_sem,
        "fission_rel_sigma": f_sem / f_mean,
        "heating_mean": h_mean,
        "heating_std": h_std,
        "heating_sem": h_sem,
        "heating_rel_sigma": h_sem / h_mean,
        "mean time": T,
        "FoM": FoM
    }
    all_results.append(results)

    print(f"\n N = {size}, FISSION:")
    print(f" mean = {f_mean:.4e}")
    if not np.isnan(f_std):
        print(f" std  = {f_std:.4e}")
        print(f" SEM  = {f_sem:.4e}")
    else:
        print(f" std  = N/A (need at least 2 runs)")
        print(f" SEM  = N/A (need at least 2 runs)")

    print(f"\n N = {size}, HEATING:")
    print(f" mean = {h_mean:.4e}")
    if not np.isnan(h_std):
        print(f" std  = {h_std:.4e}")
        print(f" SEM  = {h_sem:.4e}")
    else:
        print(f" std  = N/A (need at least 2 runs)")
        print(f" SEM  = N/A (need at least 2 runs)")

    # Create results directory if it doesn't exist
    Path("results").mkdir(exist_ok=True)

# Save main stats
combined_df = pd.DataFrame(all_results)
combined_df.to_csv("results/ensemble_stats.csv", index=False)
print(f"\nResults saved to results/ensemble_stats.csv")

# Ensemble size validation
if len(fission_vals) >= 5:
    print("\nEnsemble size (M) validation (fission std):")
    valid_dict = {}
    for M in [5, 10, 20]:
        if len(fission_vals) >= M:
            _, std, _ = stats(fission_vals[:M])
            print(f"M={M:2d} → std = {std:.4e}")
            valid_dict[f"M = {M}"] = std
        else:
            valid_dict[f"M = {M}"] = np.nan
    
    df_valid = pd.DataFrame({
        "ensemble_size": list(valid_dict.keys()),
        "fission_std": list(valid_dict.values())
    })
    df_valid.to_csv("results/ensemble_validation.csv", index=False)
else:
    print(f"\nSkipping ensemble validation (need at least 5 runs, found {len(fission_vals)})")

# --- Plot for ensemble ---
# Extract data for plotting (remove NaN values)
plot_df = combined_df[combined_df['fission_rel_sigma'].notna()]
sizes = plot_df['N'].values
fission_rel_sigma = plot_df['fission_rel_sigma'].values

if len(sizes) > 1:
    coef = np.polyfit(np.log10(sizes), np.log10(fission_rel_sigma), 1)
    slope = coef[0]
    print(f"Slope ≈ {slope:.2f}")
    
    plt.figure(figsize=(7, 5))
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
    plt.savefig("results/sigma_vs_N_ensemble.png", dpi=300)
    plt.show()
else:
    print("Not enough data points for plotting")

# --- Plot for ensemble ---
# Extract data for plotting (remove NaN values)
fom_df = df[df['FoM'].notna()]
figure_of_merit = fom_df['FoM'].values

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