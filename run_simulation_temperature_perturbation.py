import subprocess
import sys
from pathlib import Path
import numpy as np

N_RUNS = 1 # M
BASE_SEED = 12345
N_BATCH = 100
N_PARTICLE = 50000

BASE_DIR = Path(__file__).resolve().parent
runs_dir = BASE_DIR / "runs"
runs_dir.mkdir(exist_ok=True)

temperature = np.array([293.6, 298.6, 303.6, 313.6, 318.6, 323.6])

for tp in range(len(temperature)):
    temp_id = f"temp_{tp+1:03d}"
    temp_dir = runs_dir / temp_id
    temp_dir.mkdir(exist_ok=True)

    temp = temperature[tp]

    for i in range(N_RUNS):
        run_id = f"run_{i+1:03d}"
        outdir = temp_dir / run_id
        outdir.mkdir(exist_ok=True)

        seed = BASE_SEED + i * 1000
        batch = N_BATCH
        particle = N_PARTICLE

        # 1. Run OpenMC
        sim_cmd = [
            sys.executable,
            "simulation_temperature_perturbation.py",
            "--seed", str(int(seed)),
            "--batch", str(int(batch)),
            "--particle", str(int(particle)),
            "--outdir", str(outdir),
            "--temperature", str(float(temp))
        ]
        print(f"Running {run_id} with temperature {temp}")
        print(outdir)
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