"""
Consolidated Multi-Testcase Report Generator
============================================
Generates report.json containing simulation results for the Base Case
as well as all 10 official test cases (TC 1 - 10).
"""

import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.fastbox.validator import validate_delivery_data
from src.fastbox.simulator import simulate_day
from src.fastbox.config import DEFAULT_INPUT_FILE, OFFICIAL_TC_DIR, FALLBACK_TC_DIR, OUTPUTS_DIR


def generate_consolidated_report():
    consolidated = {}

    # 1. Base Case
    if DEFAULT_INPUT_FILE.exists():
        with open(DEFAULT_INPUT_FILE, "r", encoding="utf-8") as f:
            base_data = json.load(f)
        wh, ag, pk = validate_delivery_data(base_data)
        base_report = simulate_day(wh, ag, pk)
        consolidated["base_case"] = base_report.to_dict()

    # 2. Test Cases 1 through 10
    tc_dir = OFFICIAL_TC_DIR if OFFICIAL_TC_DIR.exists() else FALLBACK_TC_DIR
    for i in range(1, 11):
        tc_path = tc_dir / f"test_case_{i}.json"
        if tc_path.exists():
            with open(tc_path, "r", encoding="utf-8") as f:
                tc_data = json.load(f)
            wh, ag, pk = validate_delivery_data(tc_data)
            tc_report = simulate_day(wh, ag, pk)
            consolidated[f"test_case_{i}"] = tc_report.to_dict()

    # Also include the direct base case format at root of report for backward compatibility
    if "base_case" in consolidated:
        root_report = dict(consolidated["base_case"])
        root_report["all_test_cases"] = consolidated
    else:
        root_report = consolidated

    # Save to report.json and outputs/
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    
    with open(PROJECT_ROOT / "report.json", "w", encoding="utf-8") as f:
        json.dump(root_report, f, indent=4)

    with open(OUTPUTS_DIR / "report.json", "w", encoding="utf-8") as f:
        json.dump(root_report, f, indent=4)

    with open(OUTPUTS_DIR / "all_test_cases_report.json", "w", encoding="utf-8") as f:
        json.dump(consolidated, f, indent=4)

    print("[OK] Successfully generated consolidated report for all test cases in report.json!")


if __name__ == "__main__":
    generate_consolidated_report()
