# LIVE - mystery-delivery-system.vercel.app 

# FastBox Mystery Delivery System 🚚📦

A modular, production-grade algorithmic delivery dispatch and fleet efficiency tracking system built for **FastBox**.

---

## 🏗️ Architecture & Project Structure

```text
Nexeg_Assignment/
│
├── src/                                  # Core FastBox Python Package
│   └── fastbox/
│       ├── __init__.py                   # Package exports
│       ├── config.py                     # Centralized paths and constants
│       ├── models.py                     # Domain data classes (Point, Agent, Package, etc.)
│       ├── distance.py                   # Euclidean distance calculation engine
│       ├── validator.py                  # Strict schema validator & custom ValidationError
│       ├── simulator.py                  # Core dispatch & dynamic location tracking engine
│       ├── analytics.py                  # Agent efficiency scoring & best agent evaluation
│       └── reporter.py                   # JSON/CSV reporting & aligned console output
│
├── web/                                  # Interactive UI & Visualizer
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
├── run_tests.py                          # Unified CLI test runner
├── data.json                             # Active configuration / input dataset
└── requirements.txt                      # Project dependencies
```

---

## 🚀 Quick Start & Usage

### 1. Run the Delivery Simulation (CLI)
Executes the simulation on `data.json`, prints dispatch logs to the console, and generates `report.json` and `best_agent.csv`:

```bash
python main.py
```

To run on a specific JSON file:
```bash
python main.py "data/official_test_cases/test_case_1.json"
```

---

### 2. Launch the Interactive Web Dashboard
Generates and opens the visual dashboard in your browser:

```bash
python dashboard.py
```

**Features in Dashboard:**
- 🎬 **60 FPS Live Delivery Animation**: Watch agents navigate from starting points to warehouses and destinations with delivery bursts.
- 📁 **Upload JSON with Schema Validator**: Upload custom test cases; invalid schemas are rejected with format guidance.
- 📥 **Export CSV**: 1-click download of fleet metrics and dispatch logs.
- 🎛️ **Test Case Selector**: Instantly toggle between base data and all 10 test cases.

---

### 3. Run the Test Suite
Executes all unit tests and integration tests across the 10 official assignment test cases:

```bash
python run_tests.py
```

---

## 🐳 Docker Support

You can build and run the FastBox containerized services with Docker or Docker Compose:

### Using Docker CLI:
```bash
# Build image
docker build -t fastbox-delivery .

# Run simulation
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

## 🧮 Algorithm & Efficiency Formula

1. **Euclidean Distance Formula**:
   $$\text{distance} = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$$

2. **Nearest Agent Dispatch Rule**:
   For every package, the algorithm finds the agent closest to the pickup warehouse based on the agent's **current dynamic location**.

3. **Efficiency Score**:
   $$\text{efficiency} = \frac{\text{total\_distance}}{\text{packages\_delivered}}$$
   - **Lower is better** (represents less distance traveled per delivered package).
   - Zero deliveries are handled safely without division-by-zero errors.
   - **Best Agent**: The agent with the lowest efficiency score.
