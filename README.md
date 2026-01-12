# Watt-About-It

Prédire la satisfaction client à partir de données d’enquête.

---

## Équipe & Rôles

| Rôle                 | Nom                  |
| -------------------- | -------------------- |
| **Lead Data**        | DIBLEU Joël          |
| **Lead MLOps**       | BACHABI Rochdyath    |
| **Développeur API**  | DAOUDI Mohamed       |
| **Responsable RGPD** | FALIGANT Marc-Alfred |

---

## Jeu de données

Le jeu de données analysé contient des indicateurs énergétiques par ville :

| Colonne                        | Description                    |
| ------------------------------ | ------------------------------ |
| pays                           | Pays de la ville               |
| ville                          | Ville analysée                 |
| cout_energie_eurp_mwh          | Coût moyen de l’énergie        |
| part_bas_carbone_pourcent      | Mix électrique bas carbone (%) |
| intensite_co2_g_kwh            | Intensité carbone CO₂          |
| fiabilite_reseau_indice        | Fiabilité du réseau (0–1)      |
| potentiel_solaire_kwh_kwp_an   | Potentiel solaire              |
| indice_potentiel_eolien        | Indice éolien                  |
| indice_risque_politique        | Stabilité politique            |
| indice_dependance_importations | Dépendance énergétique         |
| temperature_moy_c              | Température moyenne            |
| incitations_fiscales_euro_mwh  | Incitations fiscales           |

---

## Structure du projet

```
├── data/                     # Jeux de données et fichiers bruts
│   └── samples/              # Échantillons pour tests ETL
│
├── etl/                      # Scripts d’ingestion et transformation
│   ├── ingest_data.py
│   ├── upload_s3.py
│   └── main.py
│
├── training/                 # Scripts & notebooks ML
│
├── serving/                  # API FastAPI + Docker
│
├── docker/                   # Dockerfiles & CI/CD
│
├── docs/                     # Documentation (RGPD, ETL, architecture…)
│   └── etl.md
│
├── logs/                     # Fichiers de logs ETL & API
│
└── README.md
```

---

## Plan de travail initial

### **1. Mise en place du dépôt et de la structure projet**

* Création du dépôt Git
* Structuration complète
* Documentation et guide d’onboarding

### **2. Développement ETL**

* **Ingestion** du CSV depuis `data/samples/`
* **Validation du schéma** et des types
* **Logging détaillé**
* **Upload des données validées** vers AWS S3 (Data Lake)
* **Gestion des versions** par date

### **3. Entraînement & Suivi MLflow**

* Préparation des features
* Entraînement du modèle
* Tracking avec MLflow
* Gestion du versioning ML

### **4. Déploiement via FastAPI + Docker**

* Création d’une API prédictive
* Conteneurisation Docker
* Tests et première exécution sur EC2

### **5. CI/CD & Monitoring**

* GitHub Actions
* Monitoring : logs, métriques, dérive du modèle

---

## Mise en perspective RGPD

Le projet prévoit :
* Analyse des risques (Data Protection Impact Assessment)
* Identification des données personnelles (→ ici : aucune)
* Mise en place d’un registre de traitements
* Traçabilité complète de l’ETL (logs, versioning)
* Sécurisation Cloud : IAM, clés dans `.env`, policy S3 restreinte

