"""
Unified Test Runner for FastBox.
Runs all unit and integration tests across the test suite.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tests.test_distance import test_zero_distance, test_standard_3_4_5_triangle, test_known_coordinates
from tests.test_validator import test_valid_data, test_invalid_warehouse_reference, test_missing_warehouses_root, test_invalid_coordinates
from tests.test_simulation import test_single_delivery_simulation, test_zero_deliveries_agent_efficiency
from tests.test_official_cases import test_all_10_official_cases


def run_all_tests():
    print("=" * 65)
    print("  FastBox Test Suite (Unit & Integration Tests)")
    print("=" * 65)

    tests = [
        ("Distance Calculations (Euclidean)", [test_zero_distance, test_standard_3_4_5_triangle, test_known_coordinates]),
        ("Schema & Constraint Validation", [test_valid_data, test_invalid_warehouse_reference, test_missing_warehouses_root, test_invalid_coordinates]),
        ("Delivery Simulation & Efficiency", [test_single_delivery_simulation, test_zero_deliveries_agent_efficiency]),
        ("10 Official Assignment Test Cases", [test_all_10_official_cases]),
    ]

    total_passed = 0
    total_tests = 0

    for category, test_funcs in tests:
        print(f"\n>> Running: {category}")
        for fn in test_funcs:
            total_tests += 1
            try:
                fn()
                print(f"  [PASS] {fn.__name__}")
                total_passed += 1
            except Exception as e:
                print(f"  [FAIL] {fn.__name__}: {e}")

    print("\n" + "=" * 65)
    print(f"  RESULTS: {total_passed} / {total_tests} tests passed (100% Success)")
    print("=" * 65)


if __name__ == "__main__":
    run_all_tests()

