"""
Web Dashboard Builder and Test Case Preprocessor.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any

# Ensure project root is in path
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.fastbox.validator import validate_delivery_data
from src.fastbox.simulator import simulate_day
from src.fastbox.config import (
    DATA_DIR, OFFICIAL_TC_DIR, FALLBACK_TC_DIR,
    DEFAULT_TEMPLATE_HTML, DEFAULT_DASHBOARD_HTML, DEFAULT_INPUT_FILE
)


def discover_data_files() -> Dict[str, Path]:
    """Find base data.json and all test case files across standard and fallback paths."""
    files: Dict[str, Path] = {}

    # 1. Base input file
    if DEFAULT_INPUT_FILE.exists():
        files["Base Case (data.json)"] = DEFAULT_INPUT_FILE
    elif (DATA_DIR / "base_case.json").exists():
        files["Base Case (data.json)"] = DATA_DIR / "base_case.json"

    # 2. Test cases in data/official_test_cases or fallback
    tc_dir = OFFICIAL_TC_DIR if OFFICIAL_TC_DIR.exists() else FALLBACK_TC_DIR
    if tc_dir.exists():
        for i in range(1, 100):
            p = tc_dir / f"test_case_{i}.json"
            if p.exists():
                files[f"Test Case {i}"] = p

    # 3. Sample files
    for sample_name in ["sample_valid.json", "sample_invalid.json"]:
        p = DATA_DIR / sample_name
        if p.exists():
            files[f"Sample ({sample_name})"] = p

    return files


def build_case_payload(file_path: Path) -> Dict[str, Any]:
    """Load, validate, simulate, and format a test case payload for the web dashboard."""
    with open(file_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    warehouses, agents, packages = validate_delivery_data(raw_data)
    report = simulate_day(warehouses, agents, packages)

    return {
        "warehouses": {wid: list(w.location) for wid, w in warehouses.items()},
        "agents": {aid: list(a.location) for aid, a in agents.items()},
        "packages": [
            {"id": p.id, "warehouse": p.warehouse_id, "destination": list(p.destination)}
            for p in packages
        ],
        "stats": {aid: s.to_dict() for aid, s in report.agent_stats.items()},
        "best_agent": report.best_agent,
        "delivery_log": [
            {
                "package": step.package_id,
                "agent": step.agent_id,
                "warehouse": step.warehouse_id,
                "from": list(step.agent_start_pos),
                "warehouse_loc": list(step.warehouse_pos),
                "destination": list(step.destination_pos),
                "distance_wh": step.distance_to_warehouse,
                "distance_dest": step.distance_to_destination,
                "distance": step.trip_distance,
                "delay": step.delay_minutes,
            }
            for step in report.delivery_log
        ],
        "total_packages": report.total_packages,
        "total_delivered": report.total_delivered,
    }


def generate_dashboard_file(output_path: Path = DEFAULT_DASHBOARD_HTML) -> Path:
    """Build the final dashboard.html with embedded data."""
    files = discover_data_files()
    all_results: Dict[str, Any] = {}

    for name, path in files.items():
        try:
            all_results[name] = build_case_payload(path)
        except Exception:
            # Skip invalid sample cases from auto-embed
            continue

    # Load template
    template_path = DEFAULT_TEMPLATE_HTML
    if not template_path.exists():
        template_path = PROJECT_ROOT / "dashboard_template.html"

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # Build options HTML
    options_html = "".join(f'<option value="{name}">{name}</option>\n' for name in all_results.keys())
    data_js = f"const ALL_DATA = {json.dumps(all_results, indent=2)};"

    html = template.replace("<!-- __OPTIONS_PLACEHOLDER__ -->", options_html)
    html = html.replace("/* __DATA_PLACEHOLDER__ */", data_js)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    # Also sync copy to root dashboard.html for easy browser opening
    root_dashboard = PROJECT_ROOT / "dashboard.html"
    with open(root_dashboard, "w", encoding="utf-8") as f:
        f.write(html)
    # Sync copies for local opening and instant Vercel deployment
    for target in [
        PROJECT_ROOT / "dashboard.html",
        PROJECT_ROOT / "index.html",
        PROJECT_ROOT / "public" / "index.html",
    ]:
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            f.write(html)

    return output_path

