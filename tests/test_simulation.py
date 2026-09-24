"""
Unit tests for delivery dispatch simulation and efficiency analytics.
"""

from src.fastbox.validator import validate_delivery_data
from src.fastbox.simulator import simulate_day


def test_single_delivery_simulation():
    data = {
        "warehouses": {"W1": [0, 0]},
        "agents": {"A1": [0, 0]},
        "packages": [{"id": "P1", "warehouse": "W1", "destination": [3, 4]}]
    }
    warehouses, agents, packages = validate_delivery_data(data)
    report = simulate_day(warehouses, agents, packages, simulate_delays=False)

    assert report.total_delivered == 1
    assert report.best_agent == "A1"
    # Agent at (0,0) -> W1 at (0,0) = 0 dist. W1 -> Dest (3,4) = 5.0 dist.
    assert report.agent_stats["A1"].total_distance == 5.0
    assert report.agent_stats["A1"].efficiency == 5.0


def test_zero_deliveries_agent_efficiency():
    # 2 agents, but A1 is much closer to W1
    data = {
        "warehouses": {"W1": [0, 0]},
        "agents": {"A1": [0, 0], "A2": [100, 100]},
        "packages": [{"id": "P1", "warehouse": "W1", "destination": [10, 0]}]
    }
    warehouses, agents, packages = validate_delivery_data(data)
    report = simulate_day(warehouses, agents, packages, simulate_delays=False)

    assert report.agent_stats["A1"].packages_delivered == 1
    assert report.agent_stats["A2"].packages_delivered == 0
    assert report.agent_stats["A2"].efficiency == 0.0  # Safe zero division handling
    assert report.best_agent == "A1"


if __name__ == "__main__":
    test_single_delivery_simulation()
    test_zero_deliveries_agent_efficiency()
    print("✓ All simulation tests passed!")

