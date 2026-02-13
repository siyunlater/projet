import openmc
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
runs_dir = BASE_DIR / "runs"

values = []
mc_sigmas = []

for run in sorted(runs_dir.glob("run_*")):

    sp_file = run / "statepoint.100.h5"
    if not sp_file.exists():
        continue

    sp = openmc.StatePoint(sp_file)
    tally = sp.get_tally(scores=["fission"])

    mean = tally.mean.sum()
    std = np.sqrt((tally.std_dev**2).sum())
    
    values.append(mean)
    mc_sigmas.append(std)

values = np.array(values)
mc_sigmas = np.array(mc_sigmas)

M = len(values)

sigma_ensemble = np.std(values, ddof=1)
sigma_mc_mean  = np.mean(mc_sigmas)

R = sigma_ensemble / sigma_mc_mean

print(f"Number of runs: {M}")
print(f"σ_ensemble = {sigma_ensemble:.4e}")
print(f"mean σ_MC  = {sigma_mc_mean:.4e}")
print(f"R = {R:.4f}")

print(mean, std)
print(std/mean)
