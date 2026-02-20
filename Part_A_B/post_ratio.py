import openmc
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
runs_dir = BASE_DIR / "runs"

f_values = []
f_mc_sigmas = []
h_values = []
h_mc_sigmas = []
times = []

for run in sorted(runs_dir.glob("run_*")):

    sp_file = run / "statepoint.100.h5"
    if not sp_file.exists():
        continue

    sp = openmc.StatePoint(sp_file)
    f_tally = sp.get_tally(scores=["fission"])
    h_tally = sp.get_tally(scores=["heating"])

    f_mean = f_tally.mean.sum()
    f_std = np.sqrt((f_tally.std_dev**2).sum())
    h_mean = h_tally.mean.sum()
    h_std = np.sqrt((h_tally.std_dev**2).sum())
    
    f_values.append(f_mean)
    f_mc_sigmas.append(f_std)
    h_values.append(h_mean)
    h_mc_sigmas.append(h_std)

    times.append(sp.runtime["simulation"])

f_values = np.array(f_values)
f_mc_sigmas = np.array(f_mc_sigmas)
h_values = np.array(h_values)
h_mc_sigmas = np.array(h_mc_sigmas)

T = np.mean(times)
f_val_mean = np.mean(f_values)
f_val_std = np.std(f_values, ddof=1)
f_rel_sigma = f_val_std / f_val_mean
h_val_mean = np.mean(h_values)
h_val_std = np.std(h_values, ddof=1)
h_rel_sigma = h_val_std / h_val_mean

f_FoM = 1.0 / (f_rel_sigma**2 * T)
h_FoM = 1.0 / (h_rel_sigma**2 * T)

M = len(f_values)

f_sigma_ensemble = np.std(f_values, ddof=1)
f_sigma_mc_mean  = np.mean(f_mc_sigmas)
h_sigma_ensemble = np.std(h_values, ddof=1)
h_sigma_mc_mean  = np.mean(h_mc_sigmas)


f_R = f_sigma_ensemble / f_sigma_mc_mean
h_R = h_sigma_ensemble / h_sigma_mc_mean

print(f"Number of runs: {M}")
print(f"mean (fission rate)= {f_val_mean}")
print(f"std (fission rate)= {f_val_std}")
print(f"relative std (fission rate)= {f_rel_sigma}")
print(f"σ_ensemble (fission rate)= {f_sigma_ensemble:.4e}")
print(f"mean σ_MC (fission rate) = {f_sigma_mc_mean:.4e}")
print(f"R (fission rate)= {f_R:.4f}")
print(f"FoM (fission rate)= {f_FoM:.4f}\n")
print(f"mean (heating)= {h_val_mean}")
print(f"std (heating)= {h_val_std}")
print(f"relative std (heating)= {h_rel_sigma}")
print(f"σ_ensemble (heating)= {h_sigma_ensemble:.4e}")
print(f"mean σ_MC (heating) = {h_sigma_mc_mean:.4e}")
print(f"R (heating)= {h_R:.4f}")
print(f"FoM (heating)= {h_FoM:.4f}")