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

f_total = fission.mean.sum()
h_total = heating.mean.sum()

df = pd.DataFrame({
    "fission_total": [f_total],
    "heating_total": [h_total]
})

Path(args.out).parent.mkdir(parents=True, exist_ok=True)
df.to_csv(args.out, index=False)
