"""
Configuration settings and filesystem path resolvers for FastBox.
"""

from pathlib import Path

# Project root directory (2 levels up from src/fastbox)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Standard Directory Layout
SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "data"
TESTS_DIR = PROJECT_ROOT / "tests"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
WEB_DIR = PROJECT_ROOT / "web"
TEMPLATES_DIR = WEB_DIR / "templates"
OFFICIAL_TC_DIR = DATA_DIR / "official_test_cases"

# Fallback official test cases directory if located at root
FALLBACK_TC_DIR = PROJECT_ROOT / "Python Assignment(Delivery System Test Cases)"

# Default file paths
DEFAULT_INPUT_FILE = PROJECT_ROOT / "data.json"
DEFAULT_JSON_REPORT = OUTPUTS_DIR / "report.json"
DEFAULT_CSV_REPORT = OUTPUTS_DIR / "best_agent.csv"
DEFAULT_DASHBOARD_HTML = OUTPUTS_DIR / "dashboard.html"
DEFAULT_TEMPLATE_HTML = TEMPLATES_DIR / "dashboard.html"

# Precision settings
DECIMAL_PLACES = 2

