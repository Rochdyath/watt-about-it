from pathlib import Path

import joblib

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

# =========================
# Définition des chemins
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"
MODEL_DIR = BASE_DIR / "models"

data_path = f"{DATA_DIR}/datacenter_dataset_complet.csv"

# -----------------------------
# 1️⃣ Charger les données
# -----------------------------
df = pd.read_csv(data_path, sep=';', encoding='utf-8')


# -----------------------------
# 2️⃣ Préparer les features et la target
# -----------------------------
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

# -----------------------------
# 3️⃣ Séparer en train/test
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# 4️⃣ Normaliser les features
# -----------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# -----------------------------
# 5️⃣ Entraîner Random Forest
# -----------------------------
rf = RandomForestRegressor(
    n_estimators=200,  # nombre d'arbres
    random_state=42
)
rf.fit(X_train_scaled, y_train)

# -----------------------------
# 6️⃣ Évaluer le modèle
# -----------------------------
y_pred = rf.predict(X_test_scaled)

rmse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"RMSE : {rmse:.2f}")
print(f"R² : {r2:.2f}")

# Enregistrer le modèle Random Forest
joblib.dump(rf, f'{MODEL_DIR}/random_forest_datacenter_model.pkl')

# Enregistrer scaler pour pouvoir normaliser les nouvelles données
joblib.dump(scaler, f'{MODEL_DIR}/scaler_datacenter.pkl')
