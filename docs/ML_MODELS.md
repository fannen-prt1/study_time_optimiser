# Machine Learning Models Documentation

## Overview

The Study Time Optimizer includes one trained ML model — the **Productivity Predictor** — which uses a stacking ensemble to predict a student's productivity score based on four lifestyle/study inputs.

The model is implemented in `ml-engine/models/productivity_predictor.py`, trained on `ml-engine/data/dataset.csv`, and served via the backend's `/api/v1/ai` endpoints.

---

## Productivity Predictor

### Purpose

Predict how productive a student will be based on their daily study hours, sleep, stress, and focus levels.

### Algorithm

**Stacking Ensemble** (scikit-learn `StackingRegressor`):

| Layer | Algorithm | Key Hyperparameters |
|-------|-----------|-------------------|
| Base Estimator 1 | `GradientBoostingRegressor` | n_estimators=300, max_depth=5, learning_rate=0.08, subsample=0.85, min_samples_split=4, min_samples_leaf=2 |
| Base Estimator 2 | `RandomForestRegressor` | n_estimators=300, max_depth=12, min_samples_split=3, min_samples_leaf=1, n_jobs=-1 |
| Meta-Learner | `Ridge` | alpha=1.0 |
| Cross-Validation | 5-fold | — |

### Feature Engineering

Input features are expanded using `PolynomialFeatures(degree=2, include_bias=False)` before being fed into the stacking model. This creates interaction and squared terms from the 4 raw features, producing 14 polynomial features.

### Input Features

| Feature | Type | Range | Description |
|---------|------|-------|-------------|
| study_hours_per_day | float | 0–24 | Daily study hours |
| sleep_hours | float | 0–24 | Hours of sleep |
| stress_level | int | 1–10 | Self-reported stress |
| focus_score | int | 1–100 | Self-reported focus |

### Output

| Field | Type | Description |
|-------|------|-------------|
| predicted_score | float | Productivity score (0–100) |
| confidence | float | Model confidence (0.3–0.99), based on sub-model agreement |
| top_factors | list | Ranked impact of each input factor (positive/negative) |
| recommendation | string | Actionable text tip based on inputs |

### Impact Weights (hard-coded for factor ranking)

| Feature | Weight | Threshold | Direction |
|---------|--------|-----------|-----------|
| study_hours_per_day | 0.73 | ≥ 3.0 hours | higher is better |
| focus_score | 0.41 | ≥ 60 | higher is better |
| sleep_hours | 0.34 | ≥ 7.0 hours | higher is better |
| stress_level | 0.20 | ≤ 5 | lower is better |

### Confidence Calculation

Confidence is derived from the spread between sub-model predictions:

```
confidence = max(0.3, min(0.99, 1.0 - spread / 60.0))
```

Where `spread = max(sub_predictions) - min(sub_predictions)`.

### Recommendation Logic

The model generates a text recommendation based on input values:

- `sleep_hours < 7` → "get more sleep (aim for 7-8 hours)"
- `stress_level > 6` → "find ways to reduce stress"
- `focus_score < 50` → "try techniques to improve focus (pomodoro, breaks)"
- `study_hours_per_day < 2` → "increase daily study time gradually"
- `study_hours_per_day > 8` → "avoid burnout - consider shorter, focused sessions"
- If all inputs are healthy and score ≥ 70 → "Great job! Your habits are well-balanced."

---

## Training

### Dataset

Training data is stored at `ml-engine/data/dataset.csv` with columns matching the 4 input features plus the target `productivity_score`.

### Training Process

```bash
cd ml-engine
python models/productivity_predictor.py
```

This:
1. Loads `data.csv`
2. Creates degree-2 polynomial features
3. Splits 80/20 train/test
4. Fits the StackingRegressor (GBR + RF → Ridge)
5. Evaluates MAE, R², and 5-fold cross-validation R²
6. Saves model + polynomial transformer to `ml-engine/saved_models/productivity_model.pkl`

### Saved Artifact Format

```python
{
    "model": StackingRegressor,  # the fitted ensemble
    "poly": PolynomialFeatures   # the fitted feature transformer
}
```

### Training Metrics (reported on last run)

| Metric | Value |
|--------|-------|
| MAE | ~3–5 points |
| R² | ~0.90+ |
| CV R² | ~0.88 ± 0.02 |
| Polynomial features | 14 |

### Test Predictions (from built-in test cases)

| Label | study_hours | sleep | stress | focus | Predicted Score |
|-------|-------------|-------|--------|-------|----------------|
| Poor habits | 1 | 4 | 9 | 20 | Low |
| Below average | 3 | 6 | 7 | 40 | Below avg |
| Average | 5 | 7 | 5 | 50 | Mid-range |
| Good habits | 7 | 8 | 3 | 70 | High |
| Excellent habits | 9 | 8 | 2 | 90 | Very high |

---

## Model Persistence

### File Location

```
ml-engine/saved_models/productivity_model.pkl
```

### Loading

```python
from ml_engine.models.productivity_predictor import ProductivityPredictor

predictor = ProductivityPredictor()
predictor.load()  # returns True if saved model found
```

### Lazy Loading in Backend

The backend's `ai.py` router lazy-loads the model on first request via `_get_predictor()`. The `ml-engine` directory is added to `sys.path` at runtime.

---

## API Integration

The model is exposed through two endpoints:

### POST `/api/v1/ai/predict-productivity` 🔒

Accepts 4 input features, returns prediction with confidence, factors, and recommendation.

### GET `/api/v1/ai/peak-hours` 🔒

Analyzes the user's completed study sessions (from the database) to find which hours of day yield the highest average productivity. This does not use the ML model — it computes averages from historical session data.

Requires at least 3 completed sessions with productivity scores.

---

## Configuration

ML engine configuration lives in `ml-engine/config.py`:

| Setting | Value |
|---------|-------|
| PRODUCTIVITY_MODEL_PATH | `ml-engine/saved_models/productivity_model.pkl` |
| PRODUCTIVITY_FEATURES | `['study_hours_per_day', 'sleep_hours', 'stress_level', 'focus_score']` |
| PRODUCTIVITY_TARGET | `'productivity_score'` |
| MIN_SESSIONS_FOR_TRAINING | 50 |

---

## Limitations

- **Cold start:** New users have no data for per-user peak-hours analysis. The productivity predictor works for all users (it doesn't use personal history).
- **Static weights:** Factor impact weights and thresholds are hard-coded, not learned per-user.
- **Single model:** Only one ML model (productivity prediction) is implemented. The config references `OPTIMAL_TIME_MODEL_PATH` and `DURATION_MODEL_PATH` but those models are not yet built.

---

## Future Improvements

- **Optimal Time Finder** — clustering model to identify high-productivity time slots
- **Session Duration Optimizer** — regression model to suggest optimal session length
- **Per-user retraining** — train on individual user data once they have 50+ sessions
- **Online learning** — incremental model updates as new data arrives
