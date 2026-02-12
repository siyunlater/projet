# post_run.py
import openmc
import pandas as pd
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--statepoint", type=str, required=True)
parser.add_argument("--out", type=str, required=True)
args = parser.parse_args()

sp = openmc.StatePoint(args.statepoint)

fission = sp.get_tally(scores=['fission'])
heating = sp.get_tally(scores=['heating'])

f_mean = fission.mean.sum()
h_mean = heating.mean.sum()

f_std = fission.std_dev.sum()
h_std = heating.std_dev.sum()

df = pd.DataFrame({
    "fission_total_mean": [f_mean],
    "fission_total_std": [f_std],
    "heating_total_mean": [h_mean],
    "heating_total_std": [h_std]
})

Path(args.out).parent.mkdir(parents=True, exist_ok=True)
df.to_csv(args.out, index=False)
