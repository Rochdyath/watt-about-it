from fastapi import FastAPI
import joblib
from pathlib import Path

from serving.schemas import PredictionInput

app = FastAPI(title="Fil Rouge – API IA Datacenter")

# =========================
# Chargement du modèle
# =========================
APP_DIR = Path(__file__).resolve().parent
MODEL_PATH = APP_DIR / "../models" / "datacenter_suitability_model.joblib"
model = joblib.load(MODEL_PATH)

@app.post("/predict")
def predict(data: PredictionInput):
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

    prediction = model.predict(X)

    return {
        "score_suitabilite_datacenter": float(prediction[0])
    }

