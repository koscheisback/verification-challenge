# Review Sentiment Microservice

This repository contains a lightweight Python service for classifying product review sentiment into Positive, Neutral, or Negative.

## Features
- FastAPI-based REST API with `/predict`, `/health`, and `/metrics`
- CPU-friendly scikit-learn classifier packaged with joblib
- Unit tests covering inference and API behavior
- Docker-ready container image

## Project structure
- `src/api.py` – FastAPI routes
- `src/model.py` – model training and inference logic
- `tests/test_inference.py` – unit tests
- `data/reviews.csv` – sample review dataset

## Run locally
```bash
python -m pip install -r requirements.txt
python -m pytest -q
python -m uvicorn src.api:app --host 0.0.0.0 --port 8000
```

## Docker
```bash
docker build -t review-sentiment .
docker run -p 8000:8000 review-sentiment
```

## Example request
```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H 'Content-Type: application/json' \
  -d '{"review_text": "I loved this product"}'
```
