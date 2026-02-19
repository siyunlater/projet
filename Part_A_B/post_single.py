# scaling_single.py
import openmc
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

N_BATCH = 100
N_PARTICLE = np.array([1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 500000])

BASE_DIR = Path(__file__).resolve().parent

sizes = []
fission_rel_sigma = []
heating_rel_sigma = []

fission_vals = []
times = []

for n_particle in N_PARTICLE:
    SIZE = N_BATCH * n_particle
    run_dir = BASE_DIR / f"N={SIZE}" / "runs" / "run_001"

    sp_file = list(run_dir.glob("statepoint.100.h5"))[0]
    sp = openmc.StatePoint(sp_file)

    fission = sp.get_tally(scores=["fission"])
    heating = sp.get_tally(scores=["heating"])

    f_mean = fission.mean.sum()
    f_std = fission.std_dev.sum()

    h_mean = heating.mean.sum()
    h_std = heating.std_dev.sum()

    sizes.append(SIZE)

    fission_rel_sigma.append(f_std / f_mean)
    heating_rel_sigma.append(h_std / h_mean)

    times.append(sp.runtime["simulation"])

print("Fission rate mean:", f_mean)
print("Fission rate std:", f_std)
print("Heating mean:", h_mean)
print("Heating std:", h_std)

f_FoMs = []
h_FoMs = []

for i in range(len(times)):
    f_FoM = 1.0 / (fission_rel_sigma[i]**2 * times[i])
    h_FoM = 1.0 / (heating_rel_sigma[i]**2 * times[i])
    f_FoMs.append(f_FoM)
    h_FoMs.append(h_FoM)

sizes = np.array(sizes)
fission_rel_sigma = np.array(fission_rel_sigma)
heating_rel_sigma = np.array(heating_rel_sigma)

f_FoMs = np.array(f_FoMs)
h_FoMs = np.array(h_FoMs)

# For sigma vs. N
f_coef = np.polyfit(np.log10(sizes), np.log10(fission_rel_sigma), 1)
f_slope = f_coef[0]
h_coef = np.polyfit(np.log10(sizes), np.log10(heating_rel_sigma), 1)
h_slope = h_coef[0]

print(f"Single-run slope (fission rate) ≈ {f_slope:.2f}")
print(f"Single-run slope (heating) ≈ {h_slope:.2f}")

plt.figure(figsize=(7,5))
plt.loglog(sizes, fission_rel_sigma, 'o-', label="Single-run fission σ")
plt.loglog(sizes, heating_rel_sigma, 's--', label="Single-run heating σ")

plt.xlabel("Total number of histories (N)")
plt.ylabel("Relative statistical uncertainty σ")
plt.grid(True, which="both", ls="--", alpha=0.6)

plt.text(
    0.05, 0.95,
    rf"Slope (fission rate) = {f_slope:.2f}; Slope (heating) = {h_slope:.2f}",
    transform=plt.gca().transAxes,
    fontsize=11,
    verticalalignment="top",
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
)

plt.legend()
plt.tight_layout()
plt.savefig("results/sigma_vs_N_single.png", dpi=300)
plt.show()

# For FoM vs. N
plt.figure(figsize=(7,5))
plt.plot(sizes, f_FoMs, 'o-', label="single run Fission FoM (fission rate)")
plt.plot(sizes, h_FoMs, 'o-', label="single run Fission FoM (heating)")
plt.xscale('log')

plt.xlabel("Total number of histories (N)")
plt.ylabel("FoM")
plt.grid(True, which="both", ls="--", alpha=0.6)

plt.legend()
plt.tight_layout()
plt.savefig("results/FoM_vs_N_single.png", dpi=300)
plt.show()