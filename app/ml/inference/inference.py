import joblib
import numpy as np

from app.config.model_results import LABEL_MAP

# For ETL Prediction, returns simple sentiment labels--------------------------
vectorizer = joblib.load("app/ml/vectorizers/vectorizer_merged.joblib")
model = joblib.load("app/ml/classifiers/classifier_merged.joblib")

def predict(text_processed):
    text_vectorized = vectorizer.transform(text_processed)
    predictions = model.predict(text_vectorized)
    return predictions
# -----------------------------------------------------------------------------

# For Dashboard text-level prediction, with full details
def predict_sentiment(text: str, model_key: str, models: dict) -> dict:
    """
    Run inference on a single text input.

    Args:
        text:      Raw input string.
        model_key: One of 'malaya', 'heuristic', 'merged'.
        models:    Dict returned by load_models().

    Returns:
        Dict with predicted class, probabilities, and top contributing words.

    Raises:
        ValueError: If model_key is not recognised.
    """
    if model_key not in models:
        raise ValueError(f"Unknown model '{model_key}'. Choose from: {list(models.keys())}")

    vectorizer = models[model_key]["vectorizer"]
    classifier = models[model_key]["classifier"]

    # ── inference ──────────────────────────────────────────────
    X               = vectorizer.transform([text])
    predicted_label = int(classifier.predict(X)[0])
    probs           = classifier.predict_proba(X)[0]   # shape (3,)

    # ── top contributing words ─────────────────────────────────
    feature_names  = np.array(vectorizer.get_feature_names_out())
    input_features = X.toarray()[0]
    nonzero_idx    = np.where(input_features > 0)[0]

    coefs         = classifier.coef_[predicted_label]
    contributions = coefs[nonzero_idx] * input_features[nonzero_idx]

    top_n     = min(10, len(nonzero_idx))
    top_idx   = np.argsort(np.abs(contributions))[::-1][:top_n]

    top_words = [
        {
            "word":      feature_names[nonzero_idx[i]],
            "weight":    round(float(contributions[i]), 4),
            "direction": LABEL_MAP[predicted_label] if contributions[i] > 0 else "against"
        }
        for i in top_idx
    ]

    return {
        "model":                  model_key,
        "processed_text":         text,
        "predicted_class":        LABEL_MAP[predicted_label],
        "predicted_label":        predicted_label,
        "probabilities":          {LABEL_MAP[i]: round(float(probs[i]), 4) for i in range(3)},
        "top_contributing_words": top_words,
    }