"""
Model evaluation: metrics computation, cross-validation, and feature importance.
"""

import numpy as np
from sklearn.ensemble import StackingRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import PolynomialFeatures

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import PRODUCTIVITY_FEATURES


def compute_test_metrics(
    model: StackingRegressor,
    X_test: np.ndarray,
    y_test: np.ndarray,
) -> dict:
    """
    Compute MAE and R² on the held-out test set.

    Returns:
        {"mae": float, "r2": float, "y_pred": ndarray}
    """
    y_pred = model.predict(X_test)
    return {
        "mae": round(mean_absolute_error(y_test, y_pred), 4),
        "r2": round(r2_score(y_test, y_pred), 4),
        "y_pred": y_pred,
    }


def cross_validate(
    model: StackingRegressor,
    X: np.ndarray,
    y: np.ndarray,
    cv: int = 5,
) -> dict:
    """
    Run k-fold cross-validation and return R² summary.

    Returns:
        {"cv_r2_mean": float, "cv_r2_std": float, "cv_scores": ndarray}
    """
    scores = cross_val_score(model, X, y, cv=cv, scoring="r2")
    return {
        "cv_r2_mean": round(scores.mean(), 4),
        "cv_r2_std": round(scores.std(), 4),
        "cv_scores": scores,
    }


def get_feature_importances(
    model: StackingRegressor,
    poly: PolynomialFeatures,
    top_n: int = 8,
) -> dict:
    """
    Extract feature importances from the GBR sub-model.

    Args:
        model: Fitted StackingRegressor.
        poly: Fitted PolynomialFeatures transformer.
        top_n: Number of top features to return.

    Returns:
        Dict of feature_name → importance (float), sorted descending,
        limited to top_n entries.
    """
    gbr_model = model.named_estimators_["gbr"]
    poly_names = poly.get_feature_names_out(PRODUCTIVITY_FEATURES)
    importances = dict(zip(poly_names, gbr_model.feature_importances_))

    sorted_imp = sorted(importances.items(), key=lambda x: x[1], reverse=True)
    return {k: round(v, 4) for k, v in sorted_imp[:top_n]}


def full_evaluation(
    model: StackingRegressor,
    poly: PolynomialFeatures,
    X_train: np.ndarray,
    X_test: np.ndarray,
    y_test: np.ndarray,
    X_poly: np.ndarray,
    y: np.ndarray,
) -> dict:
    """
    Run the complete evaluation suite and return a single metrics dict.

    Returns:
        {
            "mae", "r2",
            "cv_r2_mean", "cv_r2_std",
            "train_samples", "test_samples", "poly_features",
            "top_features": {...}
        }
    """
    test_metrics = compute_test_metrics(model, X_test, y_test)
    cv_metrics = cross_validate(model, X_poly, y)
    top_features = get_feature_importances(model, poly)
    poly_names = poly.get_feature_names_out(PRODUCTIVITY_FEATURES)

    metrics = {
        "mae": test_metrics["mae"],
        "r2": test_metrics["r2"],
        "cv_r2_mean": cv_metrics["cv_r2_mean"],
        "cv_r2_std": cv_metrics["cv_r2_std"],
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "poly_features": len(poly_names),
        "top_features": top_features,
    }

    # Print summary
    print(f"MAE: {metrics['mae']:.4f}, R²: {metrics['r2']:.4f}")
    print(f"CV R²: {metrics['cv_r2_mean']:.4f} +/- {metrics['cv_r2_std']:.4f}")
    print(f"Poly features: {metrics['poly_features']}")
    print(f"Top features: {metrics['top_features']}")

    return metrics
