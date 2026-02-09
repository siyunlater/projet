**Single run**
- one single simulation
- observable: **mean**, **std** (std_dev in OpenMC)
- = uncertainty in one simulation, but cannot be sure if the observables are for the **real mean and std**

**Ensemble (independent runs)**
- Repetition of simulations
- To observe the **distribution** of estimators
- Ensemble uncertainty (run-to-run fluctuation) : 
  $$ \bar x = \frac{1}{N}\sum x_i $$
  $$ \sigma_{ensemble}=\sqrt{\frac{1}{N-1}\sum (x_i-\bar x)^2}$$
- std of mean (SEM) : to see how precisely we know the mean
  $$ \sigma_{\bar x}=\frac{\sigma}{\sqrt{N}}$$


### Comparison of $\sigma_{single}$ and $\sigma_{ensemble}$
- similaire - good statistical confidence in MC
- different - lack of batch/particle, problem in correlation