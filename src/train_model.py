import sys
from pathlib import Path

from src.model import train_model


if __name__ == "__main__":
    pipeline, f1_score_value = train_model()
    print(f"Trained model with macro F1: {f1_score_value:.3f}")
    print(f"Model saved to {Path(__file__).resolve().parent.parent / 'model' / 'sentiment_model.joblib'}")
