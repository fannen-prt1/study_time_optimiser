"""
Productivity Predictor Model
Stacking ensemble trained on student productivity dataset.
Input:  study_hours_per_day, sleep_hours, stress_level (1-10), focus_score (1-100)
Output: productivity_score (0-100)

Training, evaluation, and data processing logic live in separate modules:
    - data.preprocessing   : load CSV, polynomial features, train/test split
    - training.trainer     : build model, fit, save/load artifacts
    - training.evaluator   : MAE, R², cross-val, feature importances
"""

import numpy as np
from pathlib import Path
from sklearn.preprocessing import PolynomialFeatures

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import PRODUCTIVITY_FEATURES

from data.preprocessing import prepare_training_data, build_polynomial_features
from training.trainer import train_and_save, load_artifact
from training.evaluator import full_evaluation

# The 4 features the user provides
USER_FEATURES = PRODUCTIVITY_FEATURES


class ProductivityPredictor:
    """Stacking ensemble model to predict productivity score."""

    def __init__(self):
        self.model = None
        self.poly: PolynomialFeatures | None = None
        self.is_loaded = False

    def train(self, csv_path: str | Path | None = None) -> dict:
        """Train the model on the dataset CSV. Returns metrics dict."""
        # 1. Data processing
        data = prepare_training_data(csv_path)

        # 2. Training
        self.model = train_and_save(data["X_train"], data["y_train"], data["poly"])
        self.poly = data["poly"]
        self.is_loaded = True

        # 3. Evaluation
        metrics = full_evaluation(
            model=self.model,
            poly=self.poly,
            X_train=data["X_train"],
            X_test=data["X_test"],
            y_test=data["y_test"],
            X_poly=data["X_poly"],
            y=data["y"],
        )
        return metrics

    def load(self) -> bool:
        """Load the trained model from disk."""
        artifact = load_artifact()
        if artifact is None:
            return False
        self.model = artifact["model"]
        self.poly = artifact["poly"]
        self.is_loaded = True
        return True

    def predict(
        self,
        study_hours_per_day: float,
        sleep_hours: float,
        stress_level: int,
        focus_score: int,
    ) -> dict:
        """
        Predict productivity score.
        Returns dict with predicted_score, confidence, top_factors, recommendation.
        """
        if not self.is_loaded or self.model is None:
            raise RuntimeError("Model not loaded. Call load() or train() first.")

        raw = np.array([[study_hours_per_day, sleep_hours, stress_level, focus_score]])

        if self.poly is not None:
            features = self.poly.transform(raw)
        else:
            features = raw

        predicted = float(self.model.predict(features)[0])
        predicted = max(0.0, min(100.0, round(predicted, 1)))

        # Confidence from sub-model agreement
        if hasattr(self.model, "estimators_"):
            sub_preds = [est.predict(features)[0] for est in self.model.estimators_]
            spread = max(sub_preds) - min(sub_preds)
            confidence = max(0.3, min(0.99, 1.0 - spread / 60.0))
        else:
            confidence = 0.8

        # Top factors
        input_vals = {
            "study_hours_per_day": study_hours_per_day,
            "sleep_hours": sleep_hours,
            "stress_level": stress_level,
            "focus_score": focus_score,
        }
        factor_labels = {
            "study_hours_per_day": "Study Hours",
            "sleep_hours": "Sleep",
            "stress_level": "Stress",
            "focus_score": "Focus",
        }
        impact_weights = {
            "study_hours_per_day": 0.73,
            "focus_score": 0.41,
            "sleep_hours": 0.34,
            "stress_level": 0.20,
        }
        good_thresholds = {
            "study_hours_per_day": (3.0, True),
            "sleep_hours": (7.0, True),
            "stress_level": (5.0, False),
            "focus_score": (60.0, True),
        }

        sorted_factors = sorted(impact_weights.items(), key=lambda x: x[1], reverse=True)
        top_factors = []
        for feat, _weight in sorted_factors:
            threshold, higher_is_better = good_thresholds[feat]
            val = input_vals[feat]
            if higher_is_better:
                impact = "positive" if val >= threshold else "negative"
            else:
                impact = "positive" if val <= threshold else "negative"
            top_factors.append(
                {
                    "factor": factor_labels[feat],
                    "impact": impact,
                    "value": round(val, 1),
                }
            )

        recommendation = self._build_recommendation(input_vals, predicted)

        return {
            "predicted_score": predicted,
            "confidence": round(confidence, 2),
            "top_factors": top_factors,
            "recommendation": recommendation,
        }

    @staticmethod
    def _build_recommendation(inputs: dict, predicted: float) -> str:
        tips = []
        if inputs["sleep_hours"] < 7:
            tips.append("get more sleep (aim for 7-8 hours)")
        if inputs["stress_level"] > 6:
            tips.append("find ways to reduce stress")
        if inputs["focus_score"] < 50:
            tips.append("try techniques to improve focus (pomodoro, breaks)")
        if inputs["study_hours_per_day"] < 2:
            tips.append("increase daily study time gradually")
        elif inputs["study_hours_per_day"] > 8:
            tips.append("avoid burnout - consider shorter, focused sessions")

        if not tips:
            if predicted >= 70:
                return "Great job! Your habits are well-balanced for high productivity."
            return "You're doing well. Keep up consistent study habits."

        return "To boost productivity, try to " + " and ".join(tips) + "."


if __name__ == "__main__":
    predictor = ProductivityPredictor()
    metrics = predictor.train()
    print("\n--- Training Complete ---")
    print(metrics)

    # Test predictions across the spectrum
    print("\n--- Test Predictions ---")
    test_cases = [
        (1, 4, 9, 20, "Poor habits"),
        (3, 6, 7, 40, "Below average"),
        (5, 7, 5, 50, "Average"),
        (7, 8, 3, 70, "Good habits"),
        (9, 8, 2, 90, "Excellent habits"),
    ]
    for sh, sl, st, fs, label in test_cases:
        r = predictor.predict(
            study_hours_per_day=sh, sleep_hours=sl, stress_level=st, focus_score=fs
        )
        print(f"  {label:20s} => score={r['predicted_score']:5.1f}  conf={r['confidence']:.2f}")
