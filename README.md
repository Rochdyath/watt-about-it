# watt-about-it

## Objectif
Prédire la satisfaction client à partir de données d’enquête.

## Équipe
- Lead Data : DIBLEU Joël  
- Lead MLOps : BACHABI Rochdyath  
- API : DAOUDI Mohamed  
- RGPD : FALIGANT Marc-Alfred  

## Jeu de données et KPI
| Colonne                          | Description                                                         | Exemple |
| -------------------------------- | ------------------------------------------------------------------- | ------- |
| **country**                      | Pays de la ville                                                    | France  |
| **city**                         | Ville analysée                                                      | Lyon    |
| **energy_cost_usd_mwh**          | Coût moyen de l’énergie (USD/MWh)                                   | 55.20   |
| **low_carbon_mix_percent**       | Part du mix électrique bas-carbone (%)                              | 72      |
| **co2_intensity_g_per_kwh**      | Intensité carbone du réseau (gCO₂/kWh)                              | 180     |
| **grid_reliability_index**       | Fiabilité du réseau (0 à 1)                                         | 0.85    |
| **solar_potential_kwh_kwp_year** | Potentiel solaire (kWh/kWc/an)                                      | 1850    |
| **wind_potential_index**         | Potentiel éolien (0 à 1)                                            | 0.58    |
| **political_risk_index**         | Stabilité politique (0 = risque élevé, 1 = très stable)             | 0.91    |
| **import_dependence_index**      | Dépendance énergétique (0 = indépendant, 1 = entièrement dépendant) | 0.45    |
| **avg_temperature_c**            | Température moyenne annuelle (°C)                                   | 17.5    |
| **fiscal_incentives_usd_mwh**    | Incitations fiscales (USD/MWh)                                      | 4       |


## Plan de travail initial
1. Mise en place du dépôt Git et de la structure projet  
2. Développement ETL pour préparation des données  
3. Entraînement et suivi avec MLflow  
4. Déploiement via FastAPI + Docker  
5. Mise en place de CI/CD et monitoring  

---

## Mise en perspective
Ce dépôt Git sera la colonne vertébrale du projet.  
Toutes les prochaines séances s’appuieront dessus : ajout des scripts ETL, suivi MLflow, CI/CD, API, puis monitoring.  

**Prochaine étape :** test FastAPI et premières exécutions en conteneur.
