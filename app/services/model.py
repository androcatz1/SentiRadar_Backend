from app.config.model_results import OVERVIEW, PERFORMANCE, TUNING

def load_overview() -> dict:
    return OVERVIEW

def load_performance(model: str) -> dict:
    return PERFORMANCE[model]

def load_tuning(model: str) -> dict:
    return TUNING[model]