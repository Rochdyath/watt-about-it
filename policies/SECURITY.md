# SECURITY

Principes
- Moindre privilège sur IAM.
- Secrets hors code via gestionnaire de secrets.
- Chiffrement au repos et en transit.
- Journalisation des accès et des erreurs.
- Revue de code obligatoire pour toute PR liée à sécurité.

Procédures
- Rotation des clés tous les 90 jours.
- Scan secrets avant chaque push.
- Validation des dépendances critiques.
