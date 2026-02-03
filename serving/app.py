from fastapi import FastAPI, Request
import joblib
from pathlib import Path
from serving.schemas import PredictionInput
import logging
import json
from datetime import datetime
import boto3
import os

from dotenv import load_dotenv
load_dotenv()

# =========================
# Logger standard
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)
logger = logging.getLogger("api_logger")

# =========================
# Handler personnalisé S3
# =========================
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

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
            self.s3.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=msg.encode("utf-8")
            )
        except Exception as e:
            print(f"Erreur S3LoggingHandler: {e}")

# =========================
# Ajout du handler S3
# =========================
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
LOG_PREFIX = os.getenv("S3_API_LOGS_PREFIX")
s3_handler = S3LoggingHandler(bucket_name=BUCKET_NAME, prefix=LOG_PREFIX)
s3_handler.setLevel(logging.INFO)
s3_handler.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(s3_handler)

# =========================
# FastAPI
# =========================
app = FastAPI(title="Fil Rouge – API IA Datacenter")

# =========================
# Chargement du modèle
# =========================
APP_DIR = Path(__file__).resolve().parent
MODEL_PATH = APP_DIR / "models" / "datacenter_suitability_model.joblib"

model = joblib.load(MODEL_PATH)

# =========================
# Endpoint /predict
# =========================
@app.post("/predict")
def predict(data: PredictionInput, request: Request):
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

    # =========================
    # Log JSON structuré
    # =========================
    log_event = {
        "timestamp": datetime.utcnow().isoformat(),
        "endpoint": "/predict",
        "client_ip": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent"),
        "features": X[0],
        "prediction": float(prediction),
        "model_version": "v1"
    }

    logger.info(json.dumps(log_event))  # --> sera envoyé dans S3 aussi

    return {
        "score_suitabilite_datacenter": float(prediction)
    }
