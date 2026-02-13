import openmc
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
runs_dir = BASE_DIR / "runs"

sp_ref_file = runs_dir / "temp_001/statepoint.100.h5"
sp_file = runs_dir / "temp_002/statepoint.100.h5"

sp_ref = openmc.StatePoint(sp_ref_file)
sp = openmc.StatePoint(sp_file)

tally_ref = sp_ref.get_tally(scores=["fission"])
tally_pert = sp.get_tally(scores=["fission"])

mean_ref = tally_ref.mean.sum()
std_ref = tally_ref.std_dev.sum()
rel_std_ref = std_ref / mean_ref

mean_pert = tally_pert.mean.sum()
std_pert = tally_pert.std_dev.sum()
rel_std_pert = std_pert / mean_pert

delta_phys = abs(mean_pert - mean_ref)

print(delta_phys)