import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

from src.model import predict_label


def train_and_evaluate():
    data_path = os.path.join(os.path.dirname(__file__), "data", "reviews.csv")
    df = pd.read_csv(data_path)
    train_df, temp_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df["label"])
    val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42, stratify=temp_df["label"])

    preds = []
    labels = []
    for _, row in test_df.iterrows():
        preds.append(predict_label(str(row["review_text"])))
        labels.append(row["label"])

    f1 = f1_score(labels, preds, average="macro")
    return f1


if __name__ == "__main__":
    score = train_and_evaluate()
    print(f"Test macro F1: {score:.3f}")
