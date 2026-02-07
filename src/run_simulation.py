import subprocess
import sys
import numpy as np
from pathlib import Path

N_RUNS = 30
BASE_SEED = 12345

runs_dir = Path("runs")
runs_dir.mkdir(exist_ok=True)

for i in range(N_RUNS):
    run_id = f"run_{i+1:03d}"
    outdir = runs_dir / run_id
    outdir.mkdir(exist_ok=True)

    seed = BASE_SEED + i * 1000

    cmd = [
        sys.executable,
        "simulation.py",
        "--seed", str(seed),
        "--outdir", str(outdir)
    ]

    print(f"Running {run_id} with seed {seed}")
    subprocess.run(cmd, check=True)

post_cmd = [
    sys.executable,
    "post_run.py",
    "--statepoint", str(statepoint),
    "--out", str(outdir / "results.csv")
]
subprocess.run(post_cmd, check=True)