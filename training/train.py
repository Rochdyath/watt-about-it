from pathlib import Path
import joblib
import pandas as pd
from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score

import mlflow
import mlflow.sklearn
import os

import boto3

from dotenv import load_dotenv
load_dotenv()

MODEL_VERSION = "v1"
TIMESTAMP = datetime.utcnow().strftime("%Y%m%d-%H%M%S")

S3_MODEL_KEY = (
    f"models/datacenter_suitability/{MODEL_VERSION}/"
    f"datacenter_model_{TIMESTAMP}.joblib"
)

# =========================
# Définition des chemins
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"
MODEL_DIR = BASE_DIR / "models"

MODEL_DIR.mkdir(exist_ok=True)

# # =========================
# # Récupération des données
# # =========================

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

def get_latest_data_key(bucket, prefix, filename):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

    response = s3.list_objects_v2(
        Bucket=bucket,
        Prefix=prefix,
        Delimiter="/"
    )

    folders = [
        cp["Prefix"]
        for cp in response.get("CommonPrefixes", [])
    ]

    if not folders:
        raise ValueError("Aucun dossier trouvé dans S3")

    # Trier les dossiers (YYYY-MM-DD)
    latest_folder = sorted(folders)[-1]

    data_key = f"{latest_folder}{filename}"

    return data_key, latest_folder


def download_from_s3(bucket, key, local_path):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    s3.download_file(bucket, key, local_path)
    print(f"Dataset téléchargé depuis s3://{bucket}/{key}")

S3_BUCKET = os.getenv("S3_BUCKET_NAME")
S3_PREFIX = os.getenv("S3_DATA_PREFIX")
S3_FILENAME = os.getenv("S3_DATA_FILENAME")

data_key, data_folder = get_latest_data_key(
    bucket=S3_BUCKET,
    prefix=S3_PREFIX,
    filename=S3_FILENAME
)

download_from_s3(
    bucket=S3_BUCKET,
    key=data_key,
    local_path=str(DATA_DIR / "datacenter_dataset_complet.csv")
)

# docker run --rm --env-file .env filrouge-train:1.0


data_path = DATA_DIR / "datacenter_dataset_complet.csv"

# =========================
# Charger les données
# =========================
df = pd.read_csv(data_path, sep=";", encoding="utf-8")

# =========================
# Features / Target
# =========================
features = [
    'cout_energie_eurp_mwh',
    'part_bas_carbone_pourcent',
    'intensite_co2_g_kwh',
    'fiabilite_reseau_indice',
    'potentiel_solaire_kwh_kwp_an',
    'indice_potentiel_eolien',
    'indice_risque_politique',
    'indice_dependance_importations',
    'temperature_moy_c',
    'incitations_fiscales_euro_mwh'
]

target = 'score_suitabilite_datacenter'

X = df[features]
y = df[target]

# =========================
# Train / Test split
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# Pipeline (Scaler + Model)
# =========================
model = Pipeline(steps=[
    ("scaler", StandardScaler()),
    ("rf", RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    ))
])

# =========================
# MLflow setup
# =========================
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))
mlflow.set_experiment("datacenter_suitability")

with mlflow.start_run():

    # =========================
    # Entraînement
    # =========================
    model.fit(X_train, y_train)

    # =========================
    # Évaluation
    # =========================
    y_pred = model.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"RMSE : {rmse:.2f}")
    print(f"R²   : {r2:.2f}")

    # Log des métriques
    mlflow.log_metrics({
        "rmse": rmse,
        "r2": r2
    })

    # Log des paramètres
    rf = model.named_steps["rf"]
    mlflow.log_params({
        "model_type": "RandomForestRegressor",
        "n_estimators": rf.n_estimators,
        "random_state": rf.random_state,
        "test_size": 0.2,
        "training_data": f"s3://{S3_BUCKET}/{data_key}"
    })

    # =========================
    # Sauvegarde du modèle
    # =========================
    # En local
    joblib.dump(model, MODEL_DIR / "datacenter_suitability_model.joblib")

    # Sur MLflow 
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="datacenter_suitability_model"
    )

    # Sur S3
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    s3.upload_file(
        Filename=str(MODEL_DIR / "datacenter_suitability_model.joblib"),
        Bucket=S3_BUCKET,
        Key=S3_MODEL_KEY
    )

    mlflow.log_param("model_version", MODEL_VERSION)
    mlflow.log_param("s3_model_path", f"s3://{S3_BUCKET}/{S3_MODEL_KEY}")
    

print("Modèle final sauvegardé et logs enregistrés dans MLflow")
