# Pipeline d'ingestion des données

## Objectif
Assurer que chaque fichier CSV validé est chargé depuis `data/samples/`, contrôlé, journalisé puis envoyé vers le Data Lake cloud AWS S3 avec une organisation par date et un versioning temporel.

## Source des données
- **Sample local** : `data/samples/sample_energy_consumption.csv`
- **Description** : mesures de consommation énergétique par compteur (kWh) avec tarif appliqué et indicateur de période de pointe.
- **Usage** : ce fichier est destiné aux tests locaux. Les données complètes doivent résider dans `data/raw/` (non versionné) ou être récupérées depuis la source métier.

## Structure attendue du CSV
| Colonne           | Type attendu | Description                                        |
|-------------------|--------------|----------------------------------------------------|
| `record_id`       | string       | Identifiant unique de la mesure                    |
| `customer_id`     | string       | Client ou site associé au compteur                 |
| `meter_id`        | string       | Référence du compteur physique                     |
| `reading_ts`      | datetime UTC | Horodatage ISO 8601 de la mesure                   |
| `consumption_kwh` | float        | Consommation électrique en kWh                     |
| `tariff_eur_kwh`  | float        | Tarif appliqué pour 1 kWh                          |
| `is_peak`         | bool         | `true` si la mesure est prise en période de pointe |

Toute colonne manquante provoque l'arrêt du script. Les colonnes supplémentaires sont conservées mais signalées dans les logs.

## Commande d'exécution
```bash
python -m etl.ingest_data --bucket your-data-lake-bucket --prefix watt-about-it/raw
```
Options utiles :
- `--source` : chemin d'un autre CSV local.
- `--region` : région AWS (sinon chaîne de configuration par défaut).
- `--dry-run` : valide et journalise sans pousser dans le cloud.

Variables d'environnement supportées :
- `DATA_LAKE_BUCKET`
- `DATA_LAKE_PREFIX`
- `AWS_REGION`

## Exemple de sortie de logs
```
2025-01-08T09:30:02Z [INFO] Starting ingestion run 20250108T093002Z
2025-01-08T09:30:02Z [INFO] Loading source file: C:\\repo\\data\\samples\\sample_energy_consumption.csv
2025-01-08T09:30:02Z [INFO] Dataset shape: 5 rows x 7 columns
2025-01-08T09:30:02Z [INFO] Schema validation successful for columns: ['record_id', ...]
2025-01-08T09:30:03Z [INFO] Uploading ... to s3://watt-about-it-data/watt-about-it/raw/2025/01/08/sample_energy_consumption_20250108T093002Z_093003.csv
2025-01-08T09:30:04Z [INFO] Ingestion successful. Cloud destination: s3://watt-about-it-data/watt-about-it/raw/2025/01/08/sample_energy_consumption_20250108T093002Z_093003.csv
```
Le fichier complet des logs est généré sous `logs/ingestion_<run_id>.log` et n'est pas versionné.

## Emplacement final dans le Data Lake
```
s3://<bucket>/<prefix>/<YYYY>/<MM>/<DD>/<nom_source>_<run_id>_<HHMMSS>.csv
```
- `bucket` : valeur de `--bucket` ou `DATA_LAKE_BUCKET`.
- `prefix` : valeur de `--prefix` ou `DATA_LAKE_PREFIX`.
- Les sous-dossiers `YYYY/MM/DD` assurent l'organisation temporelle.
- Le suffixe `<run_id>_<HHMMSS>` garantit le versioning.

Avec les paramètres par défaut, un run réussi produira par exemple :
`s3://watt-about-it-data/watt-about-it/raw/2025/01/08/sample_energy_consumption_20250108T093002Z_093003.csv`.
