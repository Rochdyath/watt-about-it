import os
from ingest_data import ingest_file
from upload_data import upload_to_s3

def main():
    print("Lancement du pipeline ETL")

    # Nouveau fichier brut RTE
    csv_path = os.path.join("data", "samples", "eCO2mix_RTE_Annuel-Definitif_2023.xls")

    if not os.path.exists(csv_path):
        print(f"ERREUR : fichier introuvable : {csv_path}")
        return

    print("\n=== Étape 1 : Ingestion ===")
    df = ingest_file(csv_path)

    if df is None:
        print("Pipeline interrompu (ingestion échouée).")
        return

    print("\n=== Étape 2 : Upload Cloud (AWS S3) ===")
    bucket = "wai-data"
    prefix = "samples"

    upload_to_s3(csv_path, bucket, prefix)

    print("\nPipeline ETL terminé avec succès !")

if __name__ == "__main__":
    main()
