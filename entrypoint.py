import os
import boto3
import logging
from botocore.exceptions import NoCredentialsError, ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
DATA_DIR = "data/preprocessed"

def download_s3_assets():
    """Download the required assets from s3 before the app boots."""

    if not BUCKET_NAME:
        logger.error("S3_BUCKET_NAME environment variable is not set, skipping asset download (Assuming local dev).")
        return
    
    os.makedirs(DATA_DIR, exist_ok=True)

    s3 = boto3.client('s3')

    assets = [
        "clean_dataset.csv",
        "plot_embeddings.npy"
    ]

    for asset in assets:
        local_path = os.path.join(DATA_DIR, asset)

        s3_key = f"preprocessed/{asset}"

        if not os.path.exists(local_path):
            logger.info(f"Downloading {s3_key} from S3 bucket {BUCKET_NAME} to {local_path}...")
            try:
                s3.download_file(BUCKET_NAME, s3_key, local_path)
                logger.info(f"Successfully downloaded {asset}")
            except ClientError as e:
                logger.error(f"Failed to download {asset}: {e}")
                raise
        else:
            logger.info(f"{asset} already exists locally, skipping download.")


if __name__ == "__main__":
    download_s3_assets()

    logger.info("Assets ready. Booting Gunicorn Server...")
    os.execvp("gunicorn", ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "web.app:app"])