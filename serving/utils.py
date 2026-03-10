import boto3
from pathlib import Path
import os

from dotenv import load_dotenv
load_dotenv()

APP_DIR = Path(__file__).resolve().parent
MODEL_DIR = APP_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)

MODEL_PATH = MODEL_DIR / "datacenter_suitability_model.joblib"

MODEL_PREFIX = os.getenv("S3_MODEL_PREFIX")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

def download_latest_model(bucket_name: str, prefix: str, local_path: str):

    s3 = boto3.client("s3")
    
    # Lister tous les objets sous le prefix
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    if "Contents" not in response:
        raise FileNotFoundError(f"Aucun objet trouvé dans s3://{bucket_name}/{prefix}")
    
    # Trier par Key pour récupérer le dernier fichier
    files = sorted(response["Contents"], key=lambda x: x["Key"], reverse=True)
    latest_file = files[0]["Key"]
    
    s3.download_file(bucket_name, latest_file, local_path)
    print(f"Dernier modèle téléchargé depuis s3://{bucket_name}/{latest_file} -> {local_path}")
    
    return local_path

download_latest_model(BUCKET_NAME, MODEL_PREFIX, MODEL_PATH)