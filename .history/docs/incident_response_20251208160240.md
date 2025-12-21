# Incident Response – Watt about it

## Objectif

Décrire les actions à suivre en cas d'incident de sécurité ou fuite potentielle.

## Déclencheurs

- Suspicion de fuite de données
- Accès non autorisé détecté
- Anomalies dans les journaux techniques
- Comportement anormal de l'API ou de la VM

## Procédure

1. **Isoler l'incident** : couper l'accès à la ressource compromise.
2. **Collecter les preuves** : logs, horodatages, versions.
3. **Identifier la cause** : identifiants exposés, espace de stockage objet rendu public, script défaillant.
4. **Corriger immédiatement** : rotation des clés, fermeture du port concerné, suppression du fichier incriminé.
5. **Notifier le référent interne**.
6. **Documenter** dans le journal d'incident.

## Communication

Interne seulement. Aucune donnée sensible ne doit être diffusée.
