import json, joblib

LABEL_MAP = {0: "Neutral", 1: "Positive", 2: "Negative"}

with open("app/ml/results/overview.json") as f:
    OVERVIEW = json.load(f)

PERFORMANCE = {}
for dataset in ["malaya", "heuristic", "merged"]:
    for model in ["logreg", "cnb", "lgbm"]:
        key = f"{dataset}_{model}"
        with open(f"app/ml/results/performance_{dataset}_{model}.json") as f:
            PERFORMANCE[key] = json.load(f)

TUNING = {}
for model_name in ["malaya", "heuristic", "merged"]:
    with open(f"app/ml/results/tuning_{model_name}_lr.json") as f:
        TUNING[model_name] = json.load(f)

MODELS = {
    "malaya":    {
        "vectorizer":  joblib.load("app/ml/vectorizers/vectorizer_malaya.joblib"),
        "classifier":  joblib.load("app/ml/classifiers/classifier_malaya.joblib"),
    },
    "heuristic": {
        "vectorizer":  joblib.load("app/ml/vectorizers/vectorizer_heuristic.joblib"),
        "classifier":  joblib.load("app/ml/classifiers/classifier_heuristic.joblib"),
    },
    "merged":    {
        "vectorizer":  joblib.load("app/ml/vectorizers/vectorizer_merged.joblib"),
        "classifier":  joblib.load("app/ml/classifiers/classifier_merged.joblib"),
    },
}