FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app"

WORKDIR /app

# STEP 4: Install CPU-only PyTorch explicitly to dodge the 5GB GPU bloat
RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# STEP 5 & 6: Copy and install the rest of the lightweight requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# STEP 7: Pre-download the Hugging Face model so it boots instantly
RUN python -c "import logging; logging.basicConfig(level=logging.INFO); from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/msmarco-bert-base-dot-v5')"

COPY . .

EXPOSE 5000

# Run the entrypoint script to get S3 assets, then boot Gunicorn
CMD ["python", "entrypoint.py"]