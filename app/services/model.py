from app.config.model_results import OVERVIEW, PERFORMANCE, TUNING

def load_overview() -> dict:
    return OVERVIEW

def load_performance(dataset: str, model: str) -> dict:
    key = f"{dataset}_{model}"
    return PERFORMANCE[key]

def load_tuning(model: str) -> dict:
    return TUNING[model]