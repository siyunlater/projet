import openmc
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

N_BATCH = 100
N_PARTICLE = np.array([1e4, 5e4, 1e5, 5e5, 1e6, 5e6], dtype=int)

BASE_DIR = Path(__file__).resolve().parent

sizes = []
fission_rel_sigma = []

for n_particle in N_PARTICLE:
    SIZE = N_BATCH * n_particle
    size_dir = BASE_DIR / f"N={SIZE}"
    runs_dir = size_dir / "runs"

    # single run statepoint
    sp = openmc.StatePoint(runs_dir / "run_001/statepoint.100.h5")

    fission = sp.get_tally(scores=["fission"])

    mean = fission.mean.sum()
    std = fission.std_dev.sum()

    rel_sigma = std / mean

    sizes.append(SIZE)
    fission_rel_sigma.append(rel_sigma)

# --- plot ---

coef = np.polyfit(np.log10(sizes), np.log10(fission_rel_sigma), 1)
print(f"Slope ≈ {coef[0]:.2f}")

slope = coef[0]

plt.figure(figsize=(7,5))
plt.loglog(sizes, fission_rel_sigma, 'o-', label="Single-run fission σ")
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
plt.savefig("sigma_vs_N_single_run.png", dpi=300)