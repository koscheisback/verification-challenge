from fastapi import FastAPI
from pydantic import BaseModel

from src.model import predict_label

app = FastAPI(title="Review Sentiment Service")


class ReviewRequest(BaseModel):
    review_text: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/metrics")
def metrics() -> dict:
    return {"status": "ok", "service": "review-sentiment"}


@app.post("/predict")
def predict(request: ReviewRequest) -> dict:
    label = predict_label(request.review_text)
    return {"label": label}
