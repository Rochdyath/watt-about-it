from pathlib import Path
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score

# =========================
# Définition des chemins
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"
MODEL_DIR = BASE_DIR / "models"

MODEL_DIR.mkdir(exist_ok=True)

data_path = DATA_DIR / "datacenter_dataset_complet.csv"

# =========================
# 1️⃣ Charger les données
# =========================
df = pd.read_csv(data_path, sep=";", encoding="utf-8")

# =========================
# 2️⃣ Features / Target
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
# 3️⃣ Train / Test split
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# 4️⃣ Pipeline (Scaler + Model)
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
# 5️⃣ Entraînement
# =========================
model.fit(X_train, y_train)

# =========================
# 6️⃣ Évaluation
# =========================
y_pred = model.predict(X_test)

rmse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"RMSE : {rmse:.2f}")
print(f"R²   : {r2:.2f}")

# =========================
# 7️⃣ Sauvegarde du modèle UNIQUE
# =========================
joblib.dump(
    model,
    MODEL_DIR / "datacenter_suitability_model.joblib"
)

print("✅ Modèle final sauvegardé dans models/datacenter_suitability_model.joblib")
