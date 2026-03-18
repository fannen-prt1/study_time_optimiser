"""
Data loading, validation, and feature engineering for the productivity model.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import PRODUCTIVITY_FEATURES, PRODUCTIVITY_TARGET, DATA_DIR, POLY_DEGREE


def load_dataset(csv_path: str | Path | None = None) -> pd.DataFrame:
    """
    Load the productivity dataset from CSV.

    Args:
        csv_path: Path to the CSV file. Defaults to DATA_DIR/dataset.csv.
                  Also checks models/data.csv as a fallback.

    Returns:
        DataFrame with at least the feature and target columns.

    Raises:
        FileNotFoundError: If no dataset CSV is found.
        ValueError: If required columns are missing.
    """
    if csv_path is not None:
        path = Path(csv_path)
    else:
        path = DATA_DIR / "dataset.csv"
        if not path.exists():
            # Fallback to the copy inside models/
            fallback = Path(__file__).resolve().parent.parent / "models" / "data.csv"
            if fallback.exists():
                path = fallback

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at {path}")

    df = pd.read_csv(path)

    required_cols = PRODUCTIVITY_FEATURES + [PRODUCTIVITY_TARGET]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")

    return df


def extract_features_and_target(
    df: pd.DataFrame,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Extract raw feature matrix X and target vector y from the dataframe.

    Returns:
        (X, y) where X has shape (n_samples, 4) and y has shape (n_samples,).
    """
    X = df[PRODUCTIVITY_FEATURES].values
    y = df[PRODUCTIVITY_TARGET].values
    return X, y


def build_polynomial_features(
    X: np.ndarray,
    degree: int = POLY_DEGREE,
    fit: bool = True,
    poly: PolynomialFeatures | None = None,
) -> tuple[np.ndarray, PolynomialFeatures]:
    """
    Create polynomial and interaction features.

    Args:
        X: Raw feature matrix of shape (n_samples, n_features).
        degree: Polynomial degree (default 2).
        fit: If True, fit a new PolynomialFeatures transformer.
             If False, use the provided `poly` to transform only.
        poly: An already-fitted PolynomialFeatures instance (required when fit=False).

    Returns:
        (X_poly, poly_transformer)
    """
    if fit:
        poly = PolynomialFeatures(degree=degree, include_bias=False, interaction_only=False)
        X_poly = poly.fit_transform(X)
    else:
        if poly is None:
            raise ValueError("Must provide a fitted PolynomialFeatures when fit=False")
        X_poly = poly.transform(X)

    return X_poly, poly


def split_data(
    X: np.ndarray,
    y: np.ndarray,
    test_size: float = 0.2,
    random_state: int = 42,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split data into train and test sets.

    Returns:
        (X_train, X_test, y_train, y_test)
    """
    return train_test_split(X, y, test_size=test_size, random_state=random_state)


def prepare_training_data(
    csv_path: str | Path | None = None,
    poly_degree: int = POLY_DEGREE,
    test_size: float = 0.2,
) -> dict:
    """
    Full preprocessing pipeline: load → extract → polynomial features → split.

    Returns a dict with keys:
        X_train, X_test, y_train, y_test, X_poly, y, poly
    """
    df = load_dataset(csv_path)
    X_raw, y = extract_features_and_target(df)
    X_poly, poly = build_polynomial_features(X_raw, degree=poly_degree, fit=True)
    X_train, X_test, y_train, y_test = split_data(X_poly, y, test_size=test_size)

    return {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "X_poly": X_poly,
        "y": y,
        "poly": poly,
    }
