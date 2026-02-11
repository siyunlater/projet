# scaling_single.py
import openmc
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

N_BATCH = np.array([100, 200, 500, 1000])
N_PARTICLE = 10000

BASE_DIR = Path(__file__).resolve().parent

sizes = []
fission_rel_sigma = []
heating_rel_sigma = []

for n_batch in N_BATCH:

    SIZE = n_batch * N_PARTICLE
    run_dir = BASE_DIR / f"N={SIZE}" / "runs" / "run_001"

    sp_file = list(run_dir.glob("statepoint.*.h5"))[0]
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

sizes = np.array(sizes)
fission_rel_sigma = np.array(fission_rel_sigma)

coef = np.polyfit(np.log10(sizes), np.log10(fission_rel_sigma), 1)
slope = coef[0]

print(f"Single-run slope ≈ {slope:.2f}")

plt.figure(figsize=(7,5))
plt.loglog(sizes, fission_rel_sigma, 'o-', label="Single-run fission σ")
plt.loglog(sizes, heating_rel_sigma, 's--', label="Single-run heating σ")

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
plt.savefig("sigma_vs_N_single.png", dpi=300)
plt.show()
