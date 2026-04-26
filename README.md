# COSC 430 — Flask ML Model API

A production-ready Flask REST API that serves ML model predictions, containerized with Docker and deployed to Google Cloud Run via GitHub Actions CI/CD.

## Project Structure

```
.
├── app.py                          # Flask application
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Container definition
├── .dockerignore                   # Files excluded from Docker image
├── .gitignore                      # Files excluded from git
└── .github/
    └── workflows/
        └── deploy.yml              # GitHub Actions CI/CD pipeline
```

## Quick Start — Local Development

### Run with Python directly
```bash
pip install -r requirements.txt
python app.py
```

### Run with Docker
```bash
docker build -t flask-model-api .
docker run -p 8080:8080 flask-model-api
```

### Test the API
```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"X": [[1, 2, 3], [10, 20, 30]]}'
# Expected: {"y": [6, 60]}

curl http://localhost:8080/health
# Expected: {"status": "ok"}
```

## GCP Setup (one-time)

```bash
# 1. Set your project
gcloud config set project YOUR_PROJECT_ID

# 2. Enable required APIs
gcloud services enable run.googleapis.com \
  containerregistry.googleapis.com \
  artifactregistry.googleapis.com

# 3. Create service account
gcloud iam service-accounts create github-deployer \
  --display-name "GitHub Actions Deployer"

# 4. Grant roles
for ROLE in roles/run.admin roles/storage.admin roles/iam.serviceAccountUser roles/artifactregistry.writer; do
  gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member "serviceAccount:github-deployer@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role "$ROLE"
done

# 5. Download key, then add to GitHub Secrets and DELETE locally
gcloud iam service-accounts keys create key.json \
  --iam-account github-deployer@YOUR_PROJECT_ID.iam.gserviceaccount.com
# → Add contents of key.json as GitHub Secret: GCP_SA_KEY
rm key.json

# 6. Create Artifact Registry repo
gcloud artifacts repositories create flask-model-api \
  --repository-format=docker \
  --location=us-central1 \
  --project=YOUR_PROJECT_ID
```

## GitHub Secrets & Variables

In your repo: **Settings → Secrets and variables → Actions**

| Type     | Name             | Value                    |
|----------|------------------|--------------------------|
| Secret   | `GCP_SA_KEY`     | Contents of `key.json`   |
| Variable | `GCP_PROJECT_ID` | Your GCP project ID      |

## Deploying

Push to `main` — the GitHub Actions workflow builds the Docker image, pushes it to Artifact Registry, and deploys to Cloud Run automatically.

```bash
git add .
git commit -m "Update model"
git push origin main
```

## Get the Live URL

```bash
gcloud run services describe flask-model-api \
  --region us-central1 \
  --project YOUR_PROJECT_ID \
  --format "value(status.url)"
```

## Replacing the Dummy Model

In `app.py`, swap out `DummyModel` with your real model:

```python
import joblib
MODEL = joblib.load("model.pkl")   # scikit-learn example
```

Add your model file to the `COPY` step in the Dockerfile.
