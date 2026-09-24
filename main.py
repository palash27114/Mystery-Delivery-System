"""
Mystery Delivery System - FastBox
==================================
Production Entry Point for the FastBox Delivery Dispatch Simulator.

Usage:
    python main.py [optional_path_to_data.json]
"""

import sys
import json
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.fastbox.validator import validate_delivery_data, ValidationError
from src.fastbox.simulator import simulate_day
from src.fastbox.reporter import save_json_report, save_csv_report, print_summary_table
from src.fastbox.config import DEFAULT_INPUT_FILE, DEFAULT_JSON_REPORT, DEFAULT_CSV_REPORT


def main():
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INPUT_FILE

    print("=" * 60)
    print("  FastBox - Mystery Delivery System (Production Engine)")
    print("=" * 60)

    # 1. Load data
    print(f"\n[1] Loading data from: {input_path.name}")
    if not input_path.exists():
        print(f"    ERROR: Input file not found: {input_path}")
        sys.exit(1)

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except json.JSONDecodeError as err:
        print(f"    ERROR: Invalid JSON syntax in {input_path}: {err}")
        sys.exit(1)

    # 2. Validate
    print("[2] Validating schema and business rules...")
    try:
        warehouses, agents, packages = validate_delivery_data(raw_data)
        print(f"    [OK] Validated: {len(warehouses)} Warehouses | {len(agents)} Agents | {len(packages)} Packages")
    except ValidationError as err:
        print(f"    ERROR: Validation failed: {err}")
        sys.exit(1)

    # 3. Simulate Day
    print("\n[3] Simulating delivery dispatch...\n")
    report = simulate_day(warehouses, agents, packages, simulate_delays=True)

    for step in report.delivery_log:
        print(f"  {step.package_id}: Agent {step.agent_id} @ {step.agent_start_pos} "
              f"-> WH {step.warehouse_id}{step.warehouse_pos} -> Dest {step.destination_pos} "
              f"(Trip: {step.trip_distance:.2f}, Delay: {step.delay_minutes}m)")

    # 4. Save Outputs
    save_json_report(report, DEFAULT_JSON_REPORT)
    save_json_report(report, PROJECT_ROOT / "report.json")
    save_csv_report(report, DEFAULT_CSV_REPORT)
    save_csv_report(report, PROJECT_ROOT / "best_agent.csv")

    print(f"\n[4] Reports generated:")
    print(f"    - JSON: outputs/report.json (and report.json)")
    print(f"    - CSV:  outputs/best_agent.csv (and best_agent.csv)")

    # 5. Display Summary
    print_summary_table(report)


if __name__ == "__main__":
    main()

