import openmc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =================================================================
# 1. Load setting & data
# =================================================================
SP_FILE = 'statepoint.100.h5'

sp = openmc.StatePoint(SP_FILE)

# =================================================================
# 2. Data processing
# =================================================================
#flux = tally.get_slice(scores=['flux'])
fission = sp.get_tally(scores=['fission'])
heating = sp.get_tally(scores=['heating'])

# Data Reshape
# mesh.dimension = [100, 100]
f_mean = fission.mean.reshape((100, 100))
f_std  = fission.std_dev.reshape((100, 100))
h_mean = heating.mean.reshape((100, 100))
h_std  = heating.std_dev.reshape((100, 100))

# Pandas data frame
df_fission = fission.get_pandas_dataframe(nuclides=False)
df_heating = heating.get_pandas_dataframe(nuclides=False)

pd.options.display.float_format = '{:.2e}'.format

df = pd.concat([df_fission, df_heating], ignore_index=True)
df.to_csv('data_fission_and_heating.csv', index=False)

# =================================================================
# 3. Graph 
# =================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Fission Rate Distribution (2D)
im1 = ax1.imshow(f_mean, cmap='viridis', origin='lower', interpolation='gaussian')
ax1.set_title("Fission Rate Distribution")
plt.colorbar(im1, ax=ax1, label='Fissions / source particle')

# Heating (Energy Deposition) Distribution (2D)
im2 = ax2.imshow(h_mean, cmap='magma', origin='lower', interpolation='gaussian')
ax2.set_title("Energy Deposition (Heating)")
plt.colorbar(im2, ax=ax2, label='eV / source particle')

plt.tight_layout()
plt.savefig('distribution.png', dpi=300)

# Radial profile (1D)
center_idx = 20 # 100/2
radial_fission = fission.mean[center_idx, :]

plt.figure()
x = np.arange(100)
y_fission = f_mean[center_idx, :].flatten()
y_error = f_std[center_idx, :].flatten()

plt.plot(x, y_fission, label='Fission Rate', color='blue')
plt.fill_between(x, 
                 y_fission - y_error, 
                 y_fission + y_error, 
                 alpha=0.3, color='blue', label='Stat. Uncertainty')

plt.xlabel('Mesh Index (X-direction)')
plt.ylabel('Reaction Rate')
plt.title('Radial Fission Rate Profile (at center Y)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.savefig('radial_profile_1d.png', dpi=300)