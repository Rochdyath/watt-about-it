import pandas as pd
import logging
import os
import unicodedata
import re

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
# Colonnes attendues : données RTE France entière
# ---------------------------
EXPECTED_COLUMNS = [
    "Périmètre",
    "Nature",
    "Date",
    "Heures",
    "Consommation",
    "Prévision J-1",
    "Prévision J",
    "Fioul",
    "Charbon",
    "Gaz",
    "Nucléaire",
    "Eolien",
    "Solaire",
    "Hydraulique",
    "Pompage",
    "Bioénergies",
    "Ech. physiques",
    "Taux de Co2",
    "Ech. comm. Angleterre",
    "Ech. comm. Espagne",
    "Ech. comm. Italie",
    "Ech. comm. Suisse",
    "Ech. comm. Allemagne-Belgique",
    "Fioul - TAC",
    "Fioul - Cogén.",
    "Fioul - Autres",
    "Gaz - TAC",
    "Gaz - Cogén.",
    "Gaz - CCG",
    "Gaz - Autres",
    "Hydraulique - Lacs",
    "Hydraulique - STEP turbinage",
    "Bioénergies - Déchets",
    "Bioénergies - Biomasse",
    "Bioénergies - Biogaz",
    "Déstockage batterie",
    "Eolien terrestre",
    "Eolien offshore"
]

def validate_schema(df: pd.DataFrame) -> bool:
    """Vérifie que le DataFrame contient les colonnes requises."""

    df_columns = set(df.columns)
    expected = set(EXPECTED_COLUMNS)
    print("a", df_columns)
    missing = expected - df_columns
    extra = df_columns - expected

    if missing:
        logging.error(f"Colonnes manquantes : {missing}")
        print(f"ERREUR : colonnes manquantes : {missing}")
        return False

    if extra:
        logging.warning(f"Colonnes supplémentaires : {extra}")
        print(f"AVERTISSEMENT : colonnes supplémentaires détectées : {extra}")

    return True

def ingest_file(path: str):
    logging.info(f"Début de l’ingestion du fichier : {path}")
    print(f"Chargement du fichier : {path}")

    if not os.path.exists(path):
        logging.error(f"Fichier introuvable : {path}")
        print(f"ERREUR : fichier introuvable.")
        return None

    # Choix du loader selon l’extension
    ext = os.path.splitext(path)[1].lower()

    try:
        if ext == ".csv":
            df = pd.read_csv(path, sep="\t", encoding="latin-1")
        elif ext == ".xls":
            try:
                df = pd.read_excel(path, engine="xlrd")
            except Exception as e:
                # Si le fichier n'est PAS un vrai XLS → le lire comme CSV
                if "BOF" in str(e) or "Unsupported format" in str(e):
                    df = pd.read_csv(path, sep="\t", encoding="latin-1")
                else:
                    raise e
            # df = pd.read_excel(path, engine="xlrd")
        elif ext == ".xlsx":
            df = pd.read_excel(path, engine="openpyxl")
        else:
            logging.error(f"Extension non supportée : {ext}")
            print(f"ERREUR : format non supporté : {ext}")
            return None
    except Exception as e:
        logging.error(f"Impossible de lire le fichier ({ext}) : {e}")
        print("ERREUR : fichier illisible.")
        return None

    print(f"Dimensions du dataset : {df.shape[0]} lignes — {df.shape[1]} colonnes")
    logging.info(f"Dataset chargé : {df.shape[0]} lignes, {df.shape[1]} colonnes")

    # Vérifier le schéma
    if not validate_schema(df):
        logging.error("Structure invalide. Ingestion stoppée.")
        print("Pipeline interrompu (ingestion échouée).")
        return None

    print("Ingestion réussie !")
    return df

