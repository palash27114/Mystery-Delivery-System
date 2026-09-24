"""
Reporting utilities for exporting FastBox results to JSON and CSV.
"""

import json
import csv
from pathlib import Path
from typing import Union
from .models import SimulationReport


def save_json_report(report: SimulationReport, output_path: Union[str, Path]) -> None:
    """Save the final summary report matching the exact assignment schema to JSON."""
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(report.to_dict(), f, indent=4)


def save_csv_report(report: SimulationReport, output_path: Union[str, Path]) -> None:
    """Export best agent statistics and fleet results to CSV."""
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    with open(out_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["agent_id", "packages_delivered", "total_distance", "efficiency", "is_best_agent"])
        for aid, stats in sorted(report.agent_stats.items()):
            is_best = (aid == report.best_agent)
            writer.writerow([aid, stats.packages_delivered, stats.total_distance, stats.efficiency, is_best])


def print_summary_table(report: SimulationReport) -> None:
    """Print an aligned console table of the simulation results."""
    print("\n" + "=" * 60)
    print(f"  {'Agent':<10} {'Delivered':<15} {'Total Distance':<18} {'Efficiency':<15}")
    print("-" * 60)
    for aid in sorted(report.agent_stats.keys()):
        s = report.agent_stats[aid]
        is_best_marker = " * BEST" if aid == report.best_agent else ""
        print(f"  {aid:<10} {s.packages_delivered:<15} {s.total_distance:<18} {s.efficiency:<15}{is_best_marker}")
    print("=" * 60)
    print(f"  Best Performing Agent: {report.best_agent} (Score: {report.agent_stats[report.best_agent].efficiency if report.best_agent else 'N/A'})")
    print("=" * 60 + "\n")

