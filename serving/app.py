from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
import joblib
from pathlib import Path
from serving.schemas import PredictionInput
import logging
import json
from datetime import datetime
import boto3
import os
from dotenv import load_dotenv

# =========================
# Chargement des variables d'environnement
# =========================
load_dotenv()
APP_DIR = Path(__file__).resolve().parent
MODEL_DIR = APP_DIR / "models"
MODEL_PATH = MODEL_DIR / "datacenter_suitability_model.joblib"

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
LOG_PREFIX = os.getenv("S3_API_LOGS_PREFIX")

API_KEY = os.getenv("API_KEY")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# =========================
# Logger standard
# =========================
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("api_logger")

# =========================
# Handler personnalisé pour logger sur S3
# =========================
class S3LoggingHandler(logging.Handler):
    def __init__(self, bucket_name: str, prefix: str):
        super().__init__()
        self.bucket_name = bucket_name
        self.prefix = prefix
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

    def emit(self, record):
        try:
            msg = self.format(record)
            timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S-%fZ")
            key = f"{self.prefix}{timestamp}.json"
            self.s3.put_object(Bucket=self.bucket_name, Key=key, Body=msg.encode("utf-8"))
        except Exception as e:
            print(f"Erreur S3LoggingHandler: {e}")

# Ajout du handler S3 au logger
s3_handler = S3LoggingHandler(bucket_name=BUCKET_NAME, prefix=LOG_PREFIX)
s3_handler.setLevel(logging.INFO)
s3_handler.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(s3_handler)

# =========================
# Sécurité : clé API
# =========================
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: invalid API key")
    return api_key

# =========================
# FastAPI
# =========================
app = FastAPI(title="Fil Rouge – API IA Datacenter")

# # =========================
# # Téléchargement et chargement du modèle
# # =========================
# download_latest_model(BUCKET_NAME, MODEL_PREFIX, MODEL_PATH)
model = joblib.load(MODEL_PATH)

# =========================
# Endpoint /predict sécurisé
# =========================
@app.post("/predict")
def predict(data: PredictionInput, request: Request, api_key: str = Depends(verify_api_key)):
    X = [[
        data.cout_energie_eurp_mwh,
        data.part_bas_carbone_pourcent,
        data.intensite_co2_g_kwh,
        data.fiabilite_reseau_indice,
        data.potentiel_solaire_kwh_kwp_an,
        data.indice_potentiel_eolien,
        data.indice_risque_politique,
        data.indice_dependance_importations,
        data.temperature_moy_c,
        data.incitations_fiscales_euro_mwh
    ]]

    prediction = model.predict(X)[0]

    # Log JSON structuré
    log_event = {
        "timestamp": datetime.utcnow().isoformat(),
        "endpoint": "/predict",
        "client_ip": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent"),
        "features": X[0],
        "prediction": float(prediction),
        "model_version": "v1"
    }

    logger.info(json.dumps(log_event))

    return {
        "score_suitabilite_datacenter": float(prediction)
    }

