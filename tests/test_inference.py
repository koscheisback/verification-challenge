from fastapi.testclient import TestClient

from src.api import app
from src.model import predict_label


def test_predict_label_returns_known_label():
    label = predict_label("I absolutely loved this product and would recommend it")
    assert label in {"Positive", "Neutral", "Negative"}


def test_predict_label_handles_empty_text():
    label = predict_label("")
    assert label in {"Positive", "Neutral", "Negative"}


def test_api_predict_endpoint_returns_label():
    client = TestClient(app)
    response = client.post("/predict", json={"review_text": "This is a terrible experience"})
    assert response.status_code == 200
    payload = response.json()
    assert "label" in payload
    assert payload["label"] in {"Positive", "Neutral", "Negative"}


def test_health_and_metrics_endpoints():
    client = TestClient(app)
    health = client.get("/health")
    metrics = client.get("/metrics")
    assert health.status_code == 200
    assert metrics.status_code == 200
