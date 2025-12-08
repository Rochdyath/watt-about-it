# Watt about it – Sécurité & RGPD

## Objectif du dépôt
Ce dépôt regroupe **toutes les exigences sécurité / conformité RGPD** du projet Watt about it. Il sert de base de travail pour :
- structurer la gouvernance des données,
- démontrer la conformité lors de la soutenance,
- centraliser les artefacts de preuve (journaux techniques, matrices, politiques),
- fournir les directives de contrôle sécurité appliquées au pipeline MLOps.

Il est conçu pour fonctionner comme un **mini-SOC RGPD** dédié au projet.

## Missions principales
- Documenter précisément le traitement : finalité, base légale, minimisation.
- Définir et maintenir les contrôles techniques : IAM, secrets, chiffrement.
- Assurer la traçabilité des actions : journaux techniques, versioning, journal d’incidents.
- Préparer des preuves concrètes pour la soutenance finale.

## Pour commencer
1. Compléter `docs/rgpd.md` avec : finalité, base légale, minimisation et sécurité.
2. Renseigner l’inventaire des données : `docs/data_inventory.csv`.
3. Définir les droits d'accès : `docs/access_matrix.csv`.
4. Activer la sécurité GitHub : secret-scanning + dépendances vulnérables.
5. Placer les preuves anonymisées dans `docs/evidence/`.

## Rôles & responsabilités
- **Security/RGPD Owner** : vous
- **Review MLOps** : un validateur technique sur l’infra
- **Review final** : équipe pédagogique (soutenance)

## Contrôles de sécurité intégrés
- IAM minimal (principe du moindre privilège)
- Stockage cloud privé (Azure Blob ou S3)
- Secrets hors code (`.env` + Secret Manager)
- Chiffrement des données en transit et au repos
- CI sécurité : gitleaks, Bandit, dépendances
- Rotation régulière des clés et audit des accès

## Workflows CI/CD
- `ci-security.yml` :
  - analyse de secrets (gitleaks),
  - SAST Python (Bandit),
  - contrôle structure RGPD (fichiers requis).
- Pré-commit recommandé : detect-secrets, black, isort.

## Documentation incluse
- `rgpd.md` : registre complet du traitement
- `risk_register.md` : risques + mesures d’atténuation
- `privacy_notice.md` : transparence pour l’utilisateur
- `retention_policy.md` : suppression et rétention des données
- `incident_response.md` : plan de réponse à incident
- `runbook_security.md` : actions immédiates en cas d’alerte

## Ingestion des données (ETL)
La première brique MLOps du projet est `etl/ingest_data.py`. Elle :
- charge un CSV d’échantillon,
- valide la structure (colonnes attendues, types),
- journalise chaque étape,
- dépose les données validées dans un Data Lake (Azure Blob ou AWS S3).

### Prérequis
- Python >= 3.9
- Dépendances : `pip install pandas boto3 python-dotenv`
- Fichier `.env` (non versionné) contenant : `DATA_LAKE_BUCKET`, `DATA_LAKE_PREFIX`, `AWS_REGION` ou équivalent Azure.

### Fichier source
- Échantillon versionné : `data/samples/sample_energy_consumption.csv`
- Fichiers bruts volumineux : `data/raw/` (ignoré par Git)

### Exécution
```bash
python -m etl.ingest_data --bucket <bucket> --prefix watt-about-it/raw
```
Options :
- `--source` : fichier CSV personnalisé
- `--dry-run` : validation sans téléversement

### Logs & destination
- Log complet créé dans `logs/ingestion_<run_id>.log` (ignoré par Git)
- Structure du dépôt cloud :
	`s3://<bucket>/<prefix>/<YYYY>/<MM>/<DD>/<nom_fichier>_<run_id>.csv`

Cette organisation garantit : versioning par date, auditabilité et conformité RGPD.

# Watt about it – Projet Analyse Énergétique

## Objectif
Déterminer l’heure optimale d’allumage d’un poêle à granulés afin d’atteindre la température cible au moindre coût énergétique.

## Contexte
Le travail consiste à bâtir un pipeline MLOps minimal viable couvrant l’ETL, la containerisation et l’exposition d’une API temps réel.

## Données
Les sources envisagées combinent météo horaire ou quotidienne, caractéristiques de logement (dont le DPE) et historiques d’allumage ou données synthétiques générées pour les tests.

## KPI
L’indicateur principal est l’erreur absolue moyenne (Mean Absolute Error, MAE) sur l’heure d’allumage prédite, assortie d’une mesure de réduction du temps de chauffe en pourcentage par rapport à une stratégie de référence fixe.

## Stack
La pile technique s’appuie sur Python, Pandas, FastAPI, Docker, GitHub Actions (à venir), ainsi que sur une machine virtuelle Azure et un stockage objet Azure Blob.

## Démarrage rapide
### Mini ETL
Lancer la version locale pour générer les conversions :
```bash
cd etl/mini_etl
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python script.py
```

### Mini ETL Docker
Construire le conteneur puis exécuter le traitement :
```bash
cd etl/mini_etl
docker build -t mini_etl .
docker run --rm mini_etl
```

### API FastAPI
Tester l’API sur la machine locale :
```bash
cd serving/hello
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### API FastAPI Docker
Utiliser la version conteneurisée de l’API :
```bash
cd serving/hello
docker build -t fastapi_hello .
docker run -d -p 8000:8000 fastapi_hello
```

## Structure
```text
├─ data
├─ etl
├─ training
├─ serving
├─ docker
├─ docs
└─ tests
```

## Rôles
Travail réalisé en solo sur les volets Données, MLOps, API et RGPD.

## Licence
MIT ou à définir.
