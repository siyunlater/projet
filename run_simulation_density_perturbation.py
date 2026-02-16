import subprocess
import sys
from pathlib import Path
import numpy as np

N_RUNS = 20 # M
BASE_SEED = 12345
N_BATCH = 100
N_PARTICLE = 50000

BASE_DIR = Path(__file__).resolve().parent
runs_dir = BASE_DIR / "runs"
runs_dir.mkdir(exist_ok=True)

density = np.array([0.99, 0.995, 1.0, 1.005, 1.01])

for d in range(len(density)):
    dens_id = f"dens_{d+1:03d}"
    dens_dir = runs_dir / dens_id
    dens_dir.mkdir(exist_ok=True)

    batch = N_BATCH
    particle = N_PARTICLE
    dens = density[d]

    for i in range(N_RUNS):
        run_id = f"run_{i+1:03d}"
        outdir = dens_dir / run_id
        outdir.mkdir(exist_ok=True)

        seed = BASE_SEED + i * 1000

        # 1. Run OpenMC
        sim_cmd = [
            sys.executable,
            "simulation_density_perturbation.py",
            "--seed", str(int(seed)),
            "--batch", str(int(batch)),
            "--particle", str(int(particle)),
            "--outdir", str(outdir),
            "--density", str(float(dens))
        ]
        print(f"Running {run_id} with density {dens}")
        subprocess.run(sim_cmd, check=True)
        # 2. Find statepoint file (robust)
        statepoints = list(outdir.glob("statepoint.*.h5"))
        if len(statepoints) == 0:
            raise RuntimeError(f"No statepoint found in {outdir}")
        statepoint = statepoints[0]
        # 3. Post-process this run
        post_cmd = [
            sys.executable,
            "post_run.py",
            "--statepoint", str(statepoint),
            "--out", str(outdir / "results.csv")
        ]
        subprocess.run(post_cmd, check=True)

#for n_particle in N_PARTICLE: 
#    SIZE = N_BATCH * n_particle
#    size_dir = BASE_DIR / f"N={SIZE}"
#    size_dir.mkdir(exist_ok=True)
#    runs_dir = size_dir / "runs"
#    runs_dir.mkdir(exist_ok=True)
#
#    for i in range(N_RUNS):
#        run_id = f"run_{i+1:03d}"
#        outdir = runs_dir / run_id
#        outdir.mkdir(exist_ok=True)
#
#        seed = BASE_SEED + i * 1000
#        batch = N_BATCH
#        particle = n_particle
#
#        # 1. Run OpenMC
#        sim_cmd = [
#            sys.executable,
#            "simulation.py",
#            "--seed", str(int(seed)),
#            "--batch", str(int(batch)),
#            "--particle", str(int(particle)),
#            "--outdir", str(outdir),
#            "--temperature", str(float(temperature))
#        ]
#
#        print(f"Running {run_id} with seed {seed}, N = {SIZE}")
#        subprocess.run(sim_cmd, check=True)
#
#        # 2. Find statepoint file (robust)
#        statepoints = list(outdir.glob("statepoint.*.h5"))
#        if len(statepoints) == 0:
#            raise RuntimeError(f"No statepoint found in {outdir}")
#
#        statepoint = statepoints[0]
#
#        # 3. Post-process this run
#        post_cmd = [
#            sys.executable,
#            "post_run.py",
#            "--statepoint", str(statepoint),
#            "--out", str(outdir / "results.csv")
#        ]
#
#        subprocess.run(post_cmd, check=True)
#