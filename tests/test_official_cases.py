"""
Integration tests executing all 10 official assignment test cases.
"""

import json
from pathlib import Path
from src.fastbox.validator import validate_delivery_data
from src.fastbox.simulator import simulate_day
from src.fastbox.config import OFFICIAL_TC_DIR, FALLBACK_TC_DIR


def test_all_10_official_cases():
    tc_dir = OFFICIAL_TC_DIR if OFFICIAL_TC_DIR.exists() else FALLBACK_TC_DIR
    assert tc_dir.exists(), f"Test cases directory not found at {tc_dir}"

    expected_best_agents = {
        1: "A1",
        2: "A2",
        3: "A3",
        4: "A3",
        5: "A3",
        6: "A3",
        7: "A3",
        8: "A2",
        9: "A2",
        10: "A4",
    }

    total_packages_count = 0
    total_delivered_count = 0

    for i in range(1, 11):
        file_path = tc_dir / f"test_case_{i}.json"
        assert file_path.exists(), f"Missing {file_path}"

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        warehouses, agents, packages = validate_delivery_data(data)
        report = simulate_day(warehouses, agents, packages)

        assert report.total_delivered == len(packages), f"TC {i} did not deliver all packages!"
        assert report.best_agent == expected_best_agents[i], f"TC {i} best agent mismatch: expected {expected_best_agents[i]}, got {report.best_agent}"

        total_packages_count += len(packages)
        total_delivered_count += report.total_delivered

    assert total_packages_count == 99
    assert total_delivered_count == 99


if __name__ == "__main__":
    test_all_10_official_cases()
    print("✓ All 10 official assignment test cases passed with 100% success!")

