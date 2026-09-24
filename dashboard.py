"""
FastBox Interactive Web Dashboard Launcher
==========================================
Builds the animated delivery visualizer and opens it in the browser.

Usage:
    python dashboard.py
"""

import sys
import webbrowser
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from web.builder import generate_dashboard_file
from src.fastbox.config import DEFAULT_DASHBOARD_HTML


def main():
    print("=" * 60)
    print("  FastBox Live Animated Dashboard Builder")
    print("=" * 60)

    print("\n[1] Discovering test cases and compiling simulation payloads...")
    dashboard_path = generate_dashboard_file(DEFAULT_DASHBOARD_HTML)

    print(f"[2] Dashboard built successfully: {dashboard_path}")
    print("[3] Launching in default web browser...")

    url = "file:///" + str(dashboard_path).replace("\\", "/")
    webbrowser.open(url)
    print("[OK] Done!\n")


if __name__ == "__main__":
    main()
