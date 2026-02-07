import openmc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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

df.to_csv(args.out, index=False) # for each single run


runs_dir = Path("runs")

fission_vals = []
heating_vals = []

for run in runs_dir.glob("run_*"):
    df = pd.read_csv(run / "results.csv")
    fission_vals.append(df["fission_total"].iloc[0])
    heating_vals.append(df["heating_total"].iloc[0])

fission_vals = np.array(fission_vals)
heating_vals = np.array(heating_vals)

def stats(x):
    mean = np.mean(x)
    std = np.std(x, ddof=1)
    sem = std / np.sqrt(len(x))
    return mean, std, sem

f_mean, f_std, f_sem = stats(fission_vals)
h_mean, h_std, h_sem = stats(heating_vals)

print("FISSION:")
print(f" mean = {f_mean:.4e}")
print(f" std  = {f_std:.4e}")
print(f" SEM  = {f_sem:.4e}")

print("HEATING:")
print(f" mean = {h_mean:.4e}")
print(f" std  = {h_std:.4e}")
print(f" SEM  = {h_sem:.4e}")

for N in [5, 10, 20, 30]: # ensemble size validation
    subset = fission_vals[:N]
    mean, std, sem = stats(subset)
    print(N, std)