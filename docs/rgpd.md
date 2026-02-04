# Documentation de conformité RGPD, traçabilité et gouvernance

**Projet IA – Watt about it**

---

## 1. Présentation générale du système IA

### 1.1 Description du service

Le projet *Watt about it* est un service d’aide à la décision basé sur un modèle de machine learning.
Il fournit un **score de pertinence** pour l’implantation de datacenters, à partir de critères énergétiques, environnementaux et géopolitiques.

* **Type de service** : API REST
* **Endpoint principal** : `/predict`
* **Type de modèle** : Random Forest Regressor
* **Versions** : v1 (POC), v2 (production)

---

## 2. Conformité RGPD

### 2.1 Identification des données traitées

| Catégorie     | Donnée                              | Nature                   |
| ------------- | ----------------------------------- | ------------------------ |
| Énergie       | coût énergie, part bas carbone      | Données agrégées         |
| Environnement | intensité CO₂, température          | Données publiques        |
| Politique     | indice de risque, dépendance import | Indicateurs synthétiques |
| Sortie IA     | score de suitability                | Décision automatisée     |

➡ **Aucune donnée personnelle directe ou indirecte n’est traitée**
➡ Le projet ne traite **ni nom, ni email, ni IP persistée**

---

### 2.2 Qualification RGPD

* Pas de données à caractère personnel
* Pas de profilage individuel
* Pas de décision automatisée à impact juridique

**Le RGPD s’applique uniquement de manière indirecte** (principe de bonne gouvernance et traçabilité).

---

### 2.3 Principe de finalité

Les données sont utilisées **exclusivement** pour :

* évaluer des zones géographiques
* fournir un score d’aide à la décision

**Aucune réutilisation commerciale ou secondaire** n’est effectuée.

---

### 2.4 Principe de minimisation

* seules les features strictement nécessaires sont utilisées
* aucune donnée utilisateur n’est stockée
* les logs sont limités aux éléments techniques

*Justification* :

> « Le système collecte uniquement ce qui est nécessaire à l’objectif métier. »

---

## 3. Traçabilité des décisions automatisées

### 3.1 Journalisation des prédictions

Chaque requête `/predict` génère un log structuré contenant :

* timestamp UTC
* version du modèle
* features d’entrée
* score de sortie
* métadonnées techniques (IP, user-agent)

**Objectif** :

* audit
* analyse a posteriori
* supervision de dérive

---

### 3.2 Stockage des logs

* logs sérialisés en JSON
* envoyés vers un stockage S3
* organisation par date

---

### 3.3 Traçabilité des modèles

Chaque modèle est :

* versionné
* stocké dans S3
* lié à un run d’entraînement MLflow

Exemple :

```
s3://wai-data/models/datacenter_suitability/v1/datacenter_model_20260203.joblib
```

---

## 4. Explicabilité et auditabilité

### 4.1 Limites connues

* modèle de type Random Forest → explicabilité partielle
* le score est **indicatif**, pas prescriptif

---

### 4.2 Mesures mises en place

* conservation des features utilisées
* conservation des prédictions
* possibilité d’analyse post-hoc (feature importance)

*Positionnement clair* :

> « Le modèle assiste la décision humaine, il ne la remplace pas. »

---

## 5. Gouvernance de l’IA

### 5.1 Rôles et responsabilités

| Rôle           | Responsabilité                    |
| -------------- | --------------------------------- |
| Équipe Data    | Entraînement, qualité des données |
| MLOps / IT     | Déploiement, sécurité, monitoring |
| Métier         | Interprétation du score           |
| Responsable IA | Validation finale, conformité     |

**Aucune décision n’est prise sans validation humaine.**

---

### 5.2 Cycle de vie du modèle

1. Collecte de nouvelles données
2. Retraining via pipeline
3. Création d’une nouvelle version (v2)
4. Tests (shadow / A/B)
5. Validation métier
6. Déploiement contrôlé
7. Possibilité de rollback immédiat

---

### 5.3 Gestion des incidents IA

#### Types d’incidents identifiés

* dérive de performance
* usage abusif de l’API
* incohérence métier

#### Procédure

1. Détection via logs
2. Désactivation ou gel du modèle
3. Analyse
4. Correction ou retour version précédente

---

## 6. Responsabilité et décision humaine

* Le score IA **n’est pas une décision finale**
* La responsabilité reste **humaine et organisationnelle**
* Le modèle peut être désactivé à tout moment

---

## 7. Synthèse conformité

✔ Pas de données personnelles
✔ Traçabilité complète
✔ Décision humaine finale
✔ Gouvernance claire
✔ Modèle versionné et réversible

---

## Message clé pour la soutenance

> « Notre IA est conforme par conception : elle est traçable, explicable dans ses limites, gouvernée, et ne remplace jamais la décision humaine. »
