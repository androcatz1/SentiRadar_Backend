import joblib

vectorizer = joblib.load("app/ml/models/vectorizer.joblib")
model = joblib.load("app/ml/models/LRModel.joblib")

def predict(text_processed):
    text_vectorized = vectorizer.transform(text_processed)
    predictions = model.predict(text_vectorized)
    return predictions