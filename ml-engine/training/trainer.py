"""
Model building, fitting, and artifact persistence for the productivity predictor.
"""

import joblib
from pathlib import Path
from sklearn.ensemble import (
    GradientBoostingRegressor,
    RandomForestRegressor,
    StackingRegressor,
)
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
import numpy as np

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import (
    PRODUCTIVITY_MODEL_PATH,
    GBR_PARAMS,
    RF_PARAMS,
    META_LEARNER_PARAMS,
    STACKING_CV,
)


def build_model() -> StackingRegressor:
    """
    Construct the stacking ensemble (GBR + RF → Ridge meta-learner).

    Returns:
        An unfitted StackingRegressor.
    """
    estimators = [
        ("gbr", GradientBoostingRegressor(**GBR_PARAMS)),
        ("rf", RandomForestRegressor(**RF_PARAMS)),
    ]
    return StackingRegressor(
        estimators=estimators,
        final_estimator=Ridge(**META_LEARNER_PARAMS),
        cv=STACKING_CV,
    )


def fit_model(
    model: StackingRegressor,
    X_train: np.ndarray,
    y_train: np.ndarray,
) -> StackingRegressor:
    """
    Fit the model on training data.

    Returns:
        The fitted model.
    """
    model.fit(X_train, y_train)
    return model


def save_artifact(
    model: StackingRegressor,
    poly: PolynomialFeatures,
    path: Path | str | None = None,
) -> Path:
    """
    Save the trained model and polynomial transformer to disk.

    Args:
        model: Fitted StackingRegressor.
        poly: Fitted PolynomialFeatures transformer.
        path: Output path. Defaults to PRODUCTIVITY_MODEL_PATH from config.

    Returns:
        The path the artifact was saved to.
    """
    path = Path(path) if path else PRODUCTIVITY_MODEL_PATH
    path.parent.mkdir(parents=True, exist_ok=True)

    artifact = {
        "model": model,
        "poly": poly,
    }
    joblib.dump(artifact, path)
    return path


def load_artifact(
    path: Path | str | None = None,
) -> dict | None:
    """
    Load a saved model artifact from disk.

    Returns:
        Dict with 'model' and 'poly' keys, or None if file doesn't exist.
    """
    path = Path(path) if path else PRODUCTIVITY_MODEL_PATH
    if not path.exists():
        return None

    artifact = joblib.load(path)

    # Handle legacy formats
    if isinstance(artifact, dict) and "poly" in artifact:
        return {"model": artifact["model"], "poly": artifact["poly"]}
    elif isinstance(artifact, dict) and "model" in artifact:
        return {"model": artifact["model"], "poly": None}
    else:
        # Very old format: bare model object
        return {"model": artifact, "poly": None}


def train_and_save(
    X_train: np.ndarray,
    y_train: np.ndarray,
    poly: PolynomialFeatures,
) -> StackingRegressor:
    """
    Convenience: build → fit → save in one call.

    Returns:
        The fitted model.
    """
    model = build_model()
    fit_model(model, X_train, y_train)
    save_artifact(model, poly)
    print(f"Model saved to {PRODUCTIVITY_MODEL_PATH}")
    return model
