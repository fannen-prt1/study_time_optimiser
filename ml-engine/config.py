"""
ML Engine Configuration

Central place for paths, feature definitions, and model hyper-parameters.
"""

from pathlib import Path

# ── Directories ──────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent

MODELS_DIR = BASE_DIR / "saved_models"
MODELS_DIR.mkdir(exist_ok=True)

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# ── Model Paths ──────────────────────────────────────────────
PRODUCTIVITY_MODEL_PATH = MODELS_DIR / "productivity_model.pkl"

# ── Feature / Target Names ───────────────────────────────────
PRODUCTIVITY_FEATURES = [
    "study_hours_per_day",
    "sleep_hours",
    "stress_level",
    "focus_score",
]

PRODUCTIVITY_TARGET = "productivity_score"

# ── Hyper-parameters ─────────────────────────────────────────
GBR_PARAMS = {
    "n_estimators": 300,
    "max_depth": 5,
    "learning_rate": 0.08,
    "subsample": 0.85,
    "min_samples_split": 4,
    "min_samples_leaf": 2,
    "random_state": 42,
}

RF_PARAMS = {
    "n_estimators": 300,
    "max_depth": 12,
    "min_samples_split": 3,
    "min_samples_leaf": 1,
    "random_state": 42,
}

META_LEARNER_PARAMS = {
    "alpha": 1.0,
}

STACKING_CV = 5

POLY_DEGREE = 2
