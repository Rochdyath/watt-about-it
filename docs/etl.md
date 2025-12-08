# Documentation du pipeline ETL — Étape 1 : Ingestion des données

## 1. Objectif
Cette étape du pipeline ETL a pour but de **charger et valider les données énergétiques** à partir d'un fichier CSV afin de préparer leur traitement ultérieur.

## 2. Structure du projet
- `main.py` : point d’entrée du pipeline ETL  
- `ingest_data.py` : contient la logique d’ingestion et de validation des données  
- `logs/ingestion.log` : fichier de logs généré pendant l’ingestion

## 3. Fonctionnement du pipeline

### 3.1 Lancement
Le pipeline est lancé via `main.py` :

```bash
python main.py

### 3.2 Ingestion des données (`ingest_csv`)
1. Le fichier CSV est chargé dans un **DataFrame pandas** avec le séparateur `;`.  
2. Affiche et enregistre dans les logs les **dimensions du dataset**.  
3. La structure du DataFrame est **validée** via `validate_schema()` :
   - Colonnes manquantes → **erreur**, ingestion stoppée  
   - Colonnes supplémentaires → **avertissement**

### 3.3 Logging
- **INFO** : début et fin de l’ingestion, dimensions du dataset  
- **WARNING** : colonnes supplémentaires détectées  
- **ERROR** : colonnes manquantes ou impossibilité de lire le CSV

## 4. Colonnes attendues

| Colonne                          | Type    |
|---------------------------------|---------|
| pays                             | str     |
| ville                            | str     |
| cout_energie_eurp_mwh            | float   |
| part_bas_carbone_pourcent        | int     |
| intensite_co2_g_kwh              | int     |
| fiabilite_reseau_indice          | float   |
| potentiel_solaire_kwh_kwp_an     | int     |
| indice_potentiel_eolien          | float   |
| indice_risque_politique          | float   |
| indice_dependance_importations   | float   |
| temperature_moy_c                | float   |
| incitations_fiscales_euro_mwh    | float   |

## 5. Messages affichés
- Chargement du fichier et dimensions du dataset  
- Avertissements ou erreurs liés au schéma  
- Confirmation de l’ingestion réussie

## 6. Conclusion
Cette première étape du pipeline ETL assure que les données énergétiques sont **chargées correctement** et que leur **structure est conforme** aux attentes avant toute transformation ou analyse.
