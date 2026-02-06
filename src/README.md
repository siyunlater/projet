## Analyse des fluctuations statistiques et physiques de la puissance et de l’énergie déposée dans des simulations Monte-Carlo

### 1. Introduction
Bruit de méthode Monte-Carlo vs fluctuation physique

### 2. Méthodologie

**Part A — L'analyse de la fluctuation statistique de la méthode Monte-Carlo**

- Calculs steady-state
- Comparaison entre 'single run' et 'ensemble'
- Observables : taux de fission, énergie déposée
- Résultats : mean, variance, relative fluctuation(Relative Standard Deviation)
- FoM (Figure of Merit)
- **Ordres de grandeur de la fluctuation**

**Part B - Réduire incertitude statistique**
- Augmenter le nombre de particules
- Independent runs
- Résultats attendus : fluctuation depend de carré du N

**Part C - Introduire petite pertubation physique**
- small changes in density and temperature
- Conditions statistiques indentiques
- Comparaisons : grandeur d'incertitude par le calcul MC, perturbation-induced change (Δ_phys)

**Part D - Detectabilité**
- Detectability = σMC​/Δphys
- Comparaiton entre fission et heating (énergie déposée)
- Quelle observable est plus sensible ?​​
- Heating tallies est plus sensible au bruit statistique en raison de l'incertitude de la bibliothèque de KERMA que les Fission tallies?

**Géométrie**
- Single fuel pin from OpenMC example (https://nbviewer.org/github/openmc-dev/openmc-notebooks/blob/main/pincell.ipynb)
  
**Tally**
- Énergie déposée
- Fission rate

**Statistique**

**Outil**
- OpenMC

**Limitations**
- single pin-cell géométrie
- Uniquement sur steady-state
- pad de covariance de données nucléaire 