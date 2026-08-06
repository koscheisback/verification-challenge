from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split

MODEL_DIR = Path(__file__).resolve().parent.parent / "model"
MODEL_PATH = MODEL_DIR / "sentiment_model.joblib"

_classifier = None


def _build_model():
    global _classifier
    if _classifier is not None:
        return _classifier

    data_path = Path(__file__).resolve().parent.parent / "data" / "reviews.csv"
    df = pd.read_csv(data_path)

    train_df, temp_df = train_test_split(df, test_size=0.2, random_state=42)
    val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42)

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    X_train = vectorizer.fit_transform(train_df["review_text"].astype(str))
    X_val = vectorizer.transform(val_df["review_text"].astype(str))

    model = LogisticRegression(max_iter=1000, solver="liblinear")
    model.fit(X_train, train_df["label"])

    val_pred = model.predict(X_val)
    f1 = f1_score(val_df["label"], val_pred, average="macro")

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump((vectorizer, model), MODEL_PATH)
    _classifier = (vectorizer, model)
    return _classifier


def _load_model():
    global _classifier
    if _classifier is None:
        if MODEL_PATH.exists():
            _classifier = joblib.load(MODEL_PATH)
        else:
            _classifier = _build_model()
    return _classifier


def predict_label(review_text: str) -> str:
    if not review_text or not str(review_text).strip():
        return "Neutral"

    vectorizer, model = _load_model()
    text = [str(review_text)]
    prediction = model.predict(vectorizer.transform(text))[0]
    return str(prediction)


def train_model():
    vectorizer, model = _build_model()
    data_path = Path(__file__).resolve().parent.parent / "data" / "reviews.csv"
    df = pd.read_csv(data_path)
    _, temp_df = train_test_split(df, test_size=0.2, random_state=42)
    _, test_df = train_test_split(temp_df, test_size=0.5, random_state=42)

    X_test = vectorizer.transform(test_df["review_text"].astype(str))
    preds = model.predict(X_test)
    f1 = f1_score(test_df["label"], preds, average="macro")
    return model, f1
