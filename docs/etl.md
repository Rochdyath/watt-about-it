# Documentation du pipeline ETL

## Étape 1 : Ingestion des données

### 1. Objectif
Cette étape du pipeline ETL a pour but de charger et valider les données énergétiques à partir d'un fichier CSV afin de préparer leur traitement ultérieur.

### 2. Structure du projet
```

etl/
├── main.py                # point d’entrée du pipeline ETL
├── ingest_data.py         # logique d’ingestion et validation
├── upload_data.py           # upload vers le Data Lake Cloud (AWS S3)
logs/
├── ingestion.log          # logs de l’ingestion
└── s3_upload.log          # logs des uploads S3
data/
└── samples/
└── sample_energy_data.csv
.env                        # secrets AWS (non versionné)

````

### 3. Fonctionnement du pipeline

#### 3.1 Lancement
Le pipeline est lancé via :

```bash
python etl/main.py
````

#### 3.2 Ingestion des données (`ingest_csv`)

* Le fichier CSV est chargé dans un DataFrame pandas avec le séparateur tabulation (`\t`).
* Affiche et enregistre dans les logs les dimensions du dataset.
* La structure du DataFrame est validée via `validate_schema()` :

  * **Colonnes manquantes** → erreur, ingestion stoppée
  * **Colonnes supplémentaires** → avertissement

#### 3.3 Upload vers le Cloud (`upload_to_s3`)

* Le fichier validé est envoyé vers un **bucket S3**.
* Organisation du chemin par date : `prefix/YYYY-MM-DD/nom_fichier.csv`
* Le versioning S3 doit être activé pour conserver les différentes versions du fichier.
* Logs générés :

  * **INFO** : début et fin de l’upload, chemin final dans le bucket
  * **ERROR** : échec de l’upload

#### 3.4 Logging global

Tous les événements sont consignés dans `logs/etl_pipeline.log` :

| Niveau  | Informations loggées                                                                                              |
| ------- | ----------------------------------------------------------------------------------------------------------------- |
| INFO    | Début et fin de l’ingestion, dimensions du dataset, début et fin de l’upload, chemin final S3, succès du pipeline |
| WARNING | Colonnes supplémentaires détectées                                                                                |
| ERROR   | Colonnes manquantes, impossibilité de lire le CSV, échec de l’upload                                              |

---

### 4. Colonnes attendues

| Colonne                        | Type  |
| ------------------------------ | ----- |
| pays                           | str   |
| ville                          | str   |
| cout_energie_eurp_mwh          | float |
| part_bas_carbone_pourcent      | int   |
| intensite_co2_g_kwh            | int   |
| fiabilite_reseau_indice        | float |
| potentiel_solaire_kwh_kwp_an   | int   |
| indice_potentiel_eolien        | float |
| indice_risque_politique        | float |
| indice_dependance_importations | float |
| temperature_moy_c              | float |
| incitations_fiscales_euro_mwh  | float |

---

### 5. Messages affichés à l’exécution

* Chargement du fichier et dimensions du dataset
* Avertissements ou erreurs liés au schéma
* Chemin final du fichier uploadé vers le Cloud
* Confirmation de l’ingestion et de l’upload réussis

---

### 6. Conclusion

Cette étape du pipeline ETL assure que :

1. Les données énergétiques sont **chargées correctement**.
2. La **structure est conforme aux attentes**.
3. Les fichiers validés sont **stockés dans le Data Lake Cloud** avec versioning.
4. Toutes les opérations sont **journalisées pour traçabilité et audit**, ce qui est essentiel pour un suivi MLOps et RGPD.
