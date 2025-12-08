# Watt about it RGPD

Repository focalisé sur la sécurité et la conformité RGPD pour le projet fil rouge MLOps.
Ce dépôt sert de base de travail au rôle Sécurité / RGPD.

## Objectifs
- Documenter le registre de traitements et la minimisation des données.
- Mettre en place les contrôles techniques: IAM, secrets, chiffrement, CI sécurité.
- Centraliser les preuves: captures anonymisées, journaux, matrices d’accès.
- Préparer la soutenance: runbook incident, model card, politiques.

## Démarrage
1. Compléter `docs/rgpd.md` avec votre cas d’usage et la base légale.
2. Renseigner `docs/data_inventory.csv` et `docs/access_matrix.csv`.
3. Activer les checks CI et secret scanning sur GitHub.
4. Ajouter vos captures anonymisées dans `docs/evidence/` (à créer).

## Rôles
- Security/RGPD Owner: vous
- Approvers requis: Security + Lead MLOps

## Workflows
- `ci-security.yml`: gitleaks secrets, Bandit SAST Python.
- Pré-commit recommandé avec detect-secrets.

## Liens utiles
- RGPD: registre, minimisation, rétention, DSR.
- Sécurité: IAM, Key Vault, HTTPS, logs, rotation clés.
