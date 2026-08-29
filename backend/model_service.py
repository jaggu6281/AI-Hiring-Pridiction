from pathlib import Path
import joblib


# ------------------------------------------------------------
# Project paths
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "hiring_xgb_model.pkl"
)


# ------------------------------------------------------------
# Load model once
# ------------------------------------------------------------

if not MODEL_PATH.exists():

    raise FileNotFoundError(
        f"Model not found: {MODEL_PATH}"
    )


model = joblib.load(
    MODEL_PATH
)


# ------------------------------------------------------------
# Prediction helpers
# ------------------------------------------------------------

def predict(features):

    prediction = model.predict(
        features
    )[0]

    probability = (
        model.predict_proba(
            features
        )[0][1]
        * 100
    )

    return (
        int(prediction),
        float(probability)
    )


def get_recommendation(probability):

    if probability >= 90:
        return "Strong Hire"

    elif probability >= 75:
        return "Hire"

    elif probability >= 50:
        return "Review"

    else:
        return "Reject"
