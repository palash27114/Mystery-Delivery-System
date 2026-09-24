# FastBox Mystery Delivery System 🚚📦

A production-grade algorithmic delivery dispatch and fleet efficiency simulation engine built for **FastBox**.

---

## 🌟 Implemented Features & Capabilities

### 1. ⚙️ Core Delivery Algorithm
- **Dynamic Nearest-Agent Dispatch**: For every package, finds the optimal delivery agent based on Euclidean distance from the agent's **current dynamic location** to the package's pickup warehouse.
- **Euclidean Distance Engine**:
  $$\text{distance} = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$$
- **Full Day Lifecycle Simulation**:
  - Agent travels from their current location to the pickup warehouse.
  - Agent picks up package (with traffic/processing delay).
  - Agent travels from warehouse to the delivery destination.
  - Agent's location dynamically updates to the package's destination coordinate.
- **Efficiency Scoring**:
  $$\text{efficiency} = \frac{\text{total\_distance}}{\text{packages\_delivered}}$$
  - **Lower is better** (represents shorter travel distance per package).
  - Identifies the top-performing `best_agent` with the lowest efficiency rating.
  - **Zero-Division Safe**: Handles agents with zero deliveries gracefully without runtime exceptions.
- **Strict Schema & Constraint Validation**: Validates coordinate pairs, data types, and ensures all packages reference valid, existing warehouses.
- **Automated JSON & CSV Reporting**: Generates standardized `report.json` and `best_agent.csv`.

---

### 2. 🎁 Assignment Bonus Features
- **⏱️ Random Delivery Delays**: Simulates realistic real-world transit and loading delays (1–15 minutes per package).
- **🗺️ Terminal ASCII Route Visualization**: Renders an ASCII coordinate grid ($60 \times 25$) mapping warehouses, agents, and package destinations directly in the terminal.
- **👥 Mid-Day Agent Onboarding**: Supports dynamic fleet expansion allowing new agents to join midway through the day.
- **📊 Top-Agent CSV Export**: Generates `best_agent.csv` recording the best performing agent's efficiency and delivery count.

---

### 3. 🖥️ Interactive Web Dashboard & Visualizer (`dashboard.py`)
- **🎬 60 FPS Real-time Canvas Animation**:
  - Animated delivery vehicles traveling smoothly between agent bases, warehouses, and destinations.
  - Glowing vehicle trails, pickup ripple bursts at warehouses, and delivery completion bursts at destinations.
  - Completed delivery paths remain subtly mapped in the background to visualize the daily delivery network.
- **🎮 Full Playback Controls**:
  - `▶ Play` / `⏸ Pause` / `⏮ Prev Step` / `⏭ Next Step` / `↻ Reset`.
  - **Speed Selector**: Toggle playback speeds at `0.5x`, `1x`, `2x`, and `4x`.
- **📡 Live Status HUD & Auto-Scrolling Log**:
  - Live ticker updating vehicle actions in real time (*"🚚 A1 driving to W1 to pick up P1"*).
  - Overall progress bar tracking daily delivery completion percentage.
  - Active table row highlighting and automatic scrolling in the dispatch log.
- **🗂️ Multi-Testcase Selector**: Dropdown to switch seamlessly between **Base Case** and all **10 Official Test Cases** without page reloads.
- **📁 Custom JSON Upload with "Perfect JSON" Validator**:
  - Upload custom `.json` test cases directly in the browser.
  - Rejection modal providing the exact failure reason and format template for malformed inputs.
  - Instantly evaluates valid uploads and adds them to the live dashboard.
- **📥 1-Click CSV Report Extraction**: Download complete fleet performance and delivery dispatch logs directly from the browser.

---

### 4. 🧪 Automated Testing & Production Architecture
- **Unified Test Runner (`run_tests.py`)**:
  - **Unit Tests**: Distance math, coordinate validations, and zero-delivery edge cases.
  - **Integration Tests**: Automatically verifies all **10 official assignment test cases** (99 / 99 packages delivered with 100% pass rate).
- **Modular Python Architecture**: Clean separation between models, validation, analytics, simulation, and reporting in `src/fastbox/`.
- **🐳 Docker & Docker Compose**: Pre-configured containerized services for simulation, testing, and web visualizer.
- **Zero External Core Dependencies**: Uses 100% Python Standard Library (`math`, `json`, `csv`, `dataclasses`, `pathlib`).

---

## 🏗️ Project Architecture & Directory Layout

```text
Nexeg_Assignment/
│
├── src/                                  # Core FastBox Python Package
│   └── fastbox/
│       ├── __init__.py                   # Package exports & versioning
│       ├── config.py                     # Centralized paths and constants
│       ├── models.py                     # Strongly typed data models (Point, Agent, Package, etc.)
│       ├── distance.py                   # Euclidean distance calculation engine
│       ├── validator.py                  # Strict schema validator & custom ValidationError
│       ├── simulator.py                  # Core dispatch & dynamic location tracking engine
│       ├── analytics.py                  # Agent efficiency scoring & best agent evaluation
│       └── reporter.py                   # JSON/CSV reporting & aligned console output
│
├── web/                                  # Interactive UI & Visualizer Assets
│   ├── templates/
│   │   └── dashboard.html                # Web dashboard template with 60 FPS Canvas animation
│   └── builder.py                        # Web dashboard compiler and multi-case preprocessor
│
├── tests/                                # Test Suite (Unit & Integration Tests)
│   ├── test_distance.py                  # Math & Euclidean formula verification
│   ├── test_validator.py                 # Schema enforcement & rejection reason verification
│   ├── test_simulation.py                # Single delivery & zero-delivery edge cases
│   └── test_official_cases.py            # Integration test for all 10 official test cases
│
├── data/                                 # Standardized Data Store
│   ├── base_case.json                    # Base problem dataset
│   ├── sample_valid.json                 # Sample valid test case for uploads
│   ├── sample_invalid.json               # Sample invalid test case for rejection checks
│   └── official_test_cases/              # Test cases 1 through 10
│       ├── test_case_1.json
│       └── ...
│
├── outputs/                              # Generated Reports & Artifacts
│   ├── report.json                       # Official JSON output
│   ├── best_agent.csv                    # Exported top-performing agent CSV
│   └── dashboard.html                    # Generated self-contained HTML dashboard
│
├── main.py                               # CLI Entry Point for simulation
├── dashboard.py                          # CLI Entry Point to launch animated web dashboard
├── run_tests.py                          # Unified CLI test runner (10/10 tests passing)
├── data.json                             # Active configuration / input dataset
├── Dockerfile                            # Production container image specification
├── docker-compose.yml                    # Multi-service container orchestration
├── .gitignore                            # Standard Python & OS ignore rules
├── .gitattributes                       # GitHub Linguist language statistics override
├── requirements.txt                      # Project dependencies
└── README.md                             # Comprehensive project documentation
```

---

## 🚀 Quick Start & Usage

### 1. Run the Delivery Simulation (CLI)
Runs the simulation on `data.json`, prints formatted dispatch tables to the console, and generates `report.json` and `best_agent.csv`:

```bash
python main.py
```

To run on a specific JSON file:
```bash
python main.py "data/official_test_cases/test_case_1.json"
```

---

### 2. Launch the Interactive Web Dashboard
Builds and opens the visual dashboard in your browser:

```bash
python dashboard.py
```

---

### 3. Run the Automated Test Suite
Executes all unit tests and verifies all 10 official assignment test cases:

```bash
python run_tests.py
```

---

## 🐳 Docker Support

Run FastBox services in containerized environments:

### Using Docker CLI:
```bash
# Build Docker image
docker build -t fastbox-delivery .

# Run delivery simulation
docker run --rm -v ${PWD}/outputs:/app/outputs fastbox-delivery

# Run test suite
docker run --rm fastbox-delivery python run_tests.py
```

### Using Docker Compose:
```bash
# 1. Run delivery simulation
docker-compose run --rm simulator

# 2. Run all unit and integration tests
docker-compose run --rm test-runner

# 3. Serve the web dashboard on http://localhost:8080
docker-compose up dashboard
```

---

## 📊 Test Case Verification Results (10/10 Passing)

| Test Case | Packages | Delivered | Best Agent | Efficiency Score | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Base Case** | 5 | 5 | **A3** | 14.14 | ✅ **PASS** |
| **TC 1** | 12 | 12 | **A1** | 18.96 | ✅ **PASS** |
| **TC 2** | 10 | 10 | **A2** | 23.33 | ✅ **PASS** |
| **TC 3** | 6 | 6 | **A3** | 20.32 | ✅ **PASS** |
| **TC 4** | 12 | 12 | **A3** | 22.96 | ✅ **PASS** |
| **TC 5** | 10 | 10 | **A3** | 21.81 | ✅ **PASS** |
| **TC 6** | 9 | 9 | **A3** | 20.64 | ✅ **PASS** |
| **TC 7** | 10 | 10 | **A3** | 17.57 | ✅ **PASS** |
| **TC 8** | 11 | 11 | **A2** | 20.29 | ✅ **PASS** |
| **TC 9** | 8 | 8 | **A2** | 19.78 | ✅ **PASS** |
| **TC 10** | 11 | 11 | **A4** | 12.93 | ✅ **PASS** |
| **TOTAL** | **99** | **99** | — | — | **100% SUCCESS** |
