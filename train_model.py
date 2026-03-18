"""
Train the productivity prediction model
Run this script to train the model before deployment
"""

import sys
from pathlib import Path

# Add ml-engine to path
ml_engine_path = Path(__file__).parent / "ml-engine"
sys.path.insert(0, str(ml_engine_path))

from models.productivity_predictor import ProductivityPredictor

print("="*60)
print("Training Productivity Prediction Model")
print("="*60)

# Initialize predictor
predictor = ProductivityPredictor()

# Train on the sample dataset
print("\nLoading training data...")
print("Building and training model...")
print("(This may take 30-60 seconds...)\n")

try:
    metrics = predictor.train()

    print("\n" + "="*60)
    print("MODEL TRAINING COMPLETE!")
    print("="*60)

    print(f"\nPerformance Metrics:")
    print(f"   R2 Score (Train): {metrics.get('train_r2', 0):.4f}")
    print(f"   R2 Score (Test):  {metrics.get('test_r2', 0):.4f}")
    print(f"   MAE (Test):       {metrics.get('test_mae', 0):.4f}")
    print(f"   CV R2 Score:      {metrics.get('cv_r2_mean', 0):.4f} +/- {metrics.get('cv_r2_std', 0):.4f}")

    print(f"\nModel saved to: ml-engine/saved_models/productivity_model.pkl")

    print("\nRunning test prediction...")
    test_result = predictor.predict(
        study_hours_per_day=6.0,
        sleep_hours=7.5,
        stress_level=5,
        focus_score=75
    )
    print(f"   Test input: 6h study, 7.5h sleep, stress=5, focus=75")
    print(f"   Predicted productivity: {test_result['predicted_score']:.1f}/100")

    print("\n" + "="*60)
    print("Ready for deployment!")
    print("="*60)
    print("\nNext steps:")
    print("1. Commit and push the trained model to GitHub")
    print("2. Deploy to Render (it will use the trained model)")

except Exception as e:
    print(f"\nTraining failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
