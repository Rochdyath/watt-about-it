from pydantic import BaseModel

class PredictionInput(BaseModel):
    cout_energie_eurp_mwh: float
    part_bas_carbone_pourcent: float
    intensite_co2_g_kwh: float
    fiabilite_reseau_indice: float
    potentiel_solaire_kwh_kwp_an: float
    indice_potentiel_eolien: float
    indice_risque_politique: float
    indice_dependance_importations: float
    temperature_moy_c: float
    incitations_fiscales_euro_mwh: float
