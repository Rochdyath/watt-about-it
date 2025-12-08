import os
import boto3
from dotenv import load_dotenv
from datetime import datetime
import logging

# Charger le fichier .env
load_dotenv()

# Récupérer les secrets
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Configuration logging
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "s3_upload.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def upload_to_s3(local_file_path: str, bucket_name: str, prefix: str = "data"):
    """Upload vers S3 avec organisation par date."""
    if not os.path.exists(local_file_path):
        logging.error(f"Fichier inexistant : {local_file_path}")
        print(f"ERREUR : fichier inexistant : {local_file_path}")
        return False

    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

    date_str = datetime.now().strftime("%Y-%m-%d")
    file_name = os.path.basename(local_file_path)
    s3_key = f"{prefix}/{date_str}/{file_name}"

    try:
        s3.upload_file(local_file_path, bucket_name, s3_key)
        logging.info(f"Fichier uploadé : {local_file_path} → s3://{bucket_name}/{s3_key}")
        print(f"Fichier uploadé : s3://{bucket_name}/{s3_key}")
        return True
    except Exception as e:
        logging.error(f"Échec upload S3 : {e}")
        print(f"ERREUR upload S3 : {e}")
        return False

