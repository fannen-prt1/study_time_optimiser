"""
Deployment verification script for ML model.
Run this after deployment to verify the ML model loads correctly.
"""
import sys
from pathlib import Path

# Add ml-engine to path
ml_engine_dir = Path(__file__).resolve().parent / "ml-engine"
sys.path.insert(0, str(ml_engine_dir))

print("=" * 60)
print("ML Model Deployment Verification")
print("=" * 60)

# Check 1: ML dependencies
print("\n[1/4] Checking ML dependencies...")
try:
    import numpy
    import pandas
    import sklearn
    import joblib
    print(f"  [OK] numpy version: {numpy.__version__}")
    print(f"  [OK] pandas version: {pandas.__version__}")
    print(f"  [OK] scikit-learn version: {sklearn.__version__}")
    print(f"  [OK] joblib version: {joblib.__version__}")
except ImportError as e:
    print(f"  [ERROR] Missing dependency: {e}")
    sys.exit(1)

# Check 2: Model file exists
print("\n[2/4] Checking model file...")
from config import PRODUCTIVITY_MODEL_PATH
if PRODUCTIVITY_MODEL_PATH.exists():
    size_mb = PRODUCTIVITY_MODEL_PATH.stat().st_size / (1024 * 1024)
    print(f"  [OK] Model file exists: {PRODUCTIVITY_MODEL_PATH}")
    print(f"  [OK] Model size: {size_mb:.1f} MB")
else:
    print(f"  [ERROR] Model file not found: {PRODUCTIVITY_MODEL_PATH}")
    sys.exit(1)

# Check 3: Load model
print("\n[3/4] Loading model...")
try:
    from models.productivity_predictor import ProductivityPredictor
    predictor = ProductivityPredictor()
    loaded = predictor.load()
    if loaded:
        print("  [OK] Model loaded successfully")
    else:
        print("  [ERROR] Model failed to load")
        sys.exit(1)
except Exception as e:
    print(f"  [ERROR] Exception loading model: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Check 4: Test prediction
print("\n[4/4] Testing prediction...")
try:
    result = predictor.predict(
        study_hours_per_day=5.0,
        sleep_hours=7.0,
        stress_level=5,
        focus_score=60
    )
    print(f"  [OK] Test prediction: {result['predicted_score']}")
    print(f"  [OK] Confidence: {result['confidence']}")
    print(f"  [OK] Recommendation: {result['recommendation'][:50]}...")
except Exception as e:
    print(f"  [ERROR] Prediction failed: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("[SUCCESS] ML model deployment verification passed!")
print("=" * 60)
