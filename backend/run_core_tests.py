"""
Quick test script - Run a subset of core tests
"""
import subprocess
import sys
from pathlib import Path

# Resolve backend directory relative to this script
_BACKEND_DIR = str(Path(__file__).resolve().parent)


def run_test(test_path):
    """Run a single test and return result"""
    print(f"\n{'='*60}")
    print(f"Testing: {test_path}")
    print('='*60)
    result = subprocess.run(
        [sys.executable, "-m", "pytest", test_path, "-v", "--tb=short"],
        cwd=_BACKEND_DIR,
        capture_output=False
    )
    return result.returncode == 0


def main():
    """Run core tests"""
    tests = [
        # Authentication tests
        "tests/test_auth.py::TestAuthentication::test_register_user",
        "tests/test_auth.py::TestAuthentication::test_login_success",
        "tests/test_auth.py::TestAuthentication::test_refresh_token",
        
        # Analytics tests
        "tests/test_analytics.py::TestAnalytics::test_get_study_time_stats",
        "tests/test_analytics.py::TestAnalytics::test_get_productivity_trends",
        
        # Edge case tests
        "tests/test_edge_cases.py::TestEdgeCases::test_invalid_email_format",
    ]
    
    print("\n🧪 Running core tests...")
    print(f"Total tests to run: {len(tests)}\n")
    
    results = {}
    for test in tests:
        passed = run_test(test)
        results[test] = "✅ PASSED" if passed else "❌ FAILED"
    
    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)
    for test, result in results.items():
        test_name = test.split("::")[-1]
        print(f"{result} - {test_name}")
    
    passed_count = sum(1 for r in results.values() if "PASSED" in r)
    total_count = len(results)
    
    print(f"\n{'='*60}")
    print(f"Passed: {passed_count}/{total_count}")
    print("="*60)


if __name__ == "__main__":
    main()
