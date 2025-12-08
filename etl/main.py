import os
from ingest_data import ingest_csv

def main():
    print("Lancement de l'ETL — étape 1 : ingestion des données")

    # Chemin du fichier à ingérer
    sample_path = os.path.join("data", "samples", "sample_energy_data.csv")

    # Vérification de l'existence du fichier
    if not os.path.exists(sample_path):
        print(f"ERREUR : le fichier {sample_path} est introuvable.")
        return

    # Exécution de l’ingestion
    ingest_csv(sample_path)

    print("\nPipeline ETL terminé ! (Étape 1 Ingestion)")


if __name__ == "__main__":
    main()