
# Registre RGPD – Watt about it

## Finalités

Le traitement vise à **estimer le coût énergétique d'une entreprise et recommander l'offre la plus adaptée** en fonction de son profil de consommation et de son type de bâtiment.

Aucune donnée personnelle directe n'est utilisée à des fins commerciales, publicitaires ou de profilage individuel.

## Base légale

**Intérêt légitime** :

L'analyse énergétique s'effectue dans le but d'optimiser la consommation et de guider les entreprises vers une offre plus pertinente, sans traitement de données personnelles identifiantes.

Si une donnée personnelle indirecte apparaît (adresse professionnelle, email de contact), son traitement repose alors sur le  **consentement explicite** .

## Catégories de données

Le projet traite exclusivement des catégories de données **non personnelles** :

* données de consommation énergétique (kWh, heures de pointe, saisons)
* données techniques bâtiment (surface, isolation, DPE, ancienneté)
* données météo (température, vent, humidité)
* données tarifaires du marché (prix du kWh, abonnements)
* métadonnées internes (horodatage, version de fichier, ID technique)

Les données suivantes sont **explicitement interdites** :

* nom, prénom, téléphone, email d'une personne physique
* adresse privée ou identifiant permettant de rattacher la consommation à un individu
* IP, logs utilisateur, identifiant machine personnel

## Minimisation

Le système ne conserve que les variables strictement nécessaires à la finalité :

* les identifiants sont pseudonymisés sous forme de codes techniques
* toute colonne contenant un élément pouvant indirectement identifier quelqu'un est automatiquement **supprimée ou hashée**
* les datasets d'entraînement n'incluent aucune donnée sensible ou personnelle
* les logs ne contiennent jamais de données source, uniquement des métadonnées

La logique de minimisation est appliquée **avant ingestion** et  **avant entraînement du modèle** .

## Durées de conservation

* **données brutes** : 30 jours maximum, suppression automatique après traitement
* **données transformées** : 6 mois (pour réentraînement)
* **artefacts de modèles** : 12 mois, conformément aux exigences de traçabilité MLOps
* **logs techniques** : 90 jours
* **.env et secrets** : jamais conservés en dehors du Secret Manager

En fin de projet,  **tous les buckets et jeux de données sont supprimés** .

## Droits des personnes

Si une entreprise fournit accidentellement une donnée pouvant identifier une personne physique, le processus suivant s'applique :

1. Demande adressée via l'adresse de contact du projet.
2. Accusé de réception sous  **72 heures** .
3. Suppression ou rectification dans un délai maximal de  **30 jours** .
4. Preuve de suppression fournie si nécessaire.

Conformément au principe de minimisation, aucune donnée personnelle n'est conservée volontairement.

## Journalisation

Les logs contiennent uniquement des informations techniques nécessaires à l'audit MLOps :

* horodatage des ingestions
* validation de schéma (succès/erreurs)
* versions de dataset
* versions de modèles (MLflow)
* erreurs ETL
* latence et statut des endpoints API

Aucune ligne de log ne contient de données utilisateur ou de valeurs sensibles.

## Sécurité

Les mesures suivantes s'appliquent à l'ensemble de l’infrastructure :

* **IAM minimal** : accès restreint par rôle (principe du moindre privilège)
* **Sécrets hors code** : Key Vault / Secret Manager obligatoire
* **Chiffrement** : données chiffrées au repos et en transit (TLS 1.2+)
* **Isolation des environnements** : dev ≠ staging ≠ prod
* **Bucket privé** : aucune ressource Data Lake n'est publique
* **Rotation régulière des clés**
* **CI/CD sécurisé** : variables GitHub Actions chiffrées, scans automatiques

Toute anomalie de sécurité déclenche un ticket et un audit manuel.

## Sous-traitants

Les sous-traitants techniques utilisés dans le cadre du projet sont :

* **Azure** (VM, Blob Storage, Key Vault, App Service)
  * conformité ISO 27001 / RGPD
  * stockage dans la région France ou UE
* **GitHub** (code source, CI/CD)
  * secrets chiffrés, journaux cryptés
* **Open-source libraries** (Pandas, FastAPI, scikit-learn)
  * aucune donnée personnelle transmise aux mainteneurs

Aucun transfert de données en dehors de l'UE n'est effectué.

## Contact DPD

Référent RGPD interne au projet :

**Marc-Alfred** — Responsable RGPD & Sécurité du projet.

Toute demande peut être adressée via le canal de contact dédié à l'équipe projet.
