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

fission.std_dev.shape = (100, 100)
fission.mean.shape = (100, 100)
heating.std_dev.shape = (100, 100)
heating.mean.shape = (100, 100)

fig = plt.subplot(121)
fig.imshow(fission.mean)
fig2 = plt.subplot(122)
fig2.imshow(heating.mean)
plt.savefig('figures.png', dpi=300)


# Pandas data frame
df_fission = fission.get_pandas_dataframe(nuclides=False)
df_heating = heating.get_pandas_dataframe(nuclides=False)

pd.options.display.float_format = '{:.2e}'.format

df = pd.concat([df_fission, df_heating], ignore_index=True)
df.to_csv('data_fission_and_heating.csv', index=False)

## =================================================================
## 3. Graph 
## =================================================================
#
#fission.mean.shape = (100, 100)
#fission.std_dev.shape = (100, 100)
#heating.mean.shape = (100, 100)
#heating.std_dev.shape = (100, 100)
#
#fig = plt.subplot(121)
#fig.imshow(fission.mean)
#fig2 = plt.subplot(122)
#fig2.imshow(heating.mean)
#
## Determine relative error
#relative_error = np.zeros_like(fission.std_dev)
#nonzero = fission.mean > 0
#relative_error[nonzero] = fission.std_dev / fission.mean
#
## distribution of relative errors
#ret = plt.hist(relative_error[nonzero], bins=50)