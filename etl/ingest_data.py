import pandas as pd
import logging
import os
from typing import List, Dict

# ---------------------------
# Configuration des logs
# ---------------------------
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "ingestion.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------------------------
# Colonnes attendues
# ---------------------------
EXPECTED_COLUMNS = {
    "pays": str,
    "ville": str,
    "cout_energie_eurp_mwh": float,
    "part_bas_carbone_pourcent": int,
    "intensite_co2_g_kwh": int,
    "fiabilite_reseau_indice": float,
    "potentiel_solaire_kwh_kwp_an": int,
    "indice_potentiel_eolien": float,
    "indice_risque_politique": float,
    "indice_dependance_importations": float,
    "temperature_moy_c": float,
    "incitations_fiscales_euro_mwh": float
}

def validate_schema(df: pd.DataFrame) -> bool:
    """
    Vérifie que le DataFrame contient les colonnes attendues
    et remonte les erreurs / avertissements appropriés.
    """

    df_columns = set(df.columns)
    expected = set(EXPECTED_COLUMNS.keys())

    missing = expected - df_columns
    extra = df_columns - expected

    if missing:
        logging.error(f"Colonnes manquantes : {missing}")
        print(f"ERREUR : colonnes manquantes : {missing}")
        return False

    if extra:
        logging.warning(f"Colonnes supplémentaires détectées : {extra}")
        print(f"AVERTISSEMENT : colonnes supplémentaires : {extra}")

    return True


def ingest_csv(path: str):
    logging.info(f"Début de l’ingestion du fichier : {path}")
    print(f"Chargement du fichier : {path}")

    try:
        df = pd.read_csv(path, sep=';')
    except Exception as e:
        logging.error(f"Impossible de lire le fichier CSV : {e}")
        print(f"ERREUR : impossible de lire le fichier.")
        return

    print(f"Dimensions du dataset : {df.shape[0]} lignes — {df.shape[1]} colonnes")
    logging.info(f"Dataset chargé : {df.shape[0]} lignes, {df.shape[1]} colonnes")

    # Vérification du schéma
    if not validate_schema(df):
        logging.error("Structure invalide. Ingestion stoppée.")
        print("Ingestion annulée (structure invalide).")
        return

    logging.info("Ingestion terminée avec succès.")
    print("Ingestion réussie !")
