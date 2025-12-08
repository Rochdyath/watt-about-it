import os
from ingest_data import ingest_csv
from upload_data import upload_to_s3

def main():
    print("Lancement du pipeline ETL")

    # Chemin du fichier échantillon
    sample_path = os.path.join("data", "samples", "sample_energy_data.csv")
    if not os.path.exists(sample_path):
        print(f"ERREUR : fichier {sample_path} introuvable")
        return

    # ------------------------
    # Étape 1 : Ingestion
    # ------------------------
    print("Étape 1 : Ingestion")
    ingest_csv(sample_path)

    # ------------------------
    # Étape 2 : Upload S3
    # ------------------------
    print("\nÉtape 2 : Stockage dans le Data Lake (AWS S3)")
    bucket_name = "wai-data"  # Remplacer par ton bucket
    prefix = "samples"             # Préfixe dans le bucket
    upload_to_s3(sample_path, bucket_name, prefix=prefix)

    print("\nPipeline ETL terminé !")

if __name__ == "__main__":
    main()
