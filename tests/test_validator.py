"""
Unit tests for data validation and schema integrity.
"""

from src.fastbox.validator import validate_delivery_data, ValidationError


def test_valid_data():
    data = {
        "warehouses": {"W1": [0, 0]},
        "agents": {"A1": [5, 5]},
        "packages": [{"id": "P1", "warehouse": "W1", "destination": [30, 40]}]
    }
    warehouses, agents, packages = validate_delivery_data(data)
    assert "W1" in warehouses
    assert "A1" in agents
    assert len(packages) == 1
    assert packages[0].id == "P1"


def test_invalid_warehouse_reference():
    data = {
        "warehouses": {"W1": [0, 0]},
        "agents": {"A1": [5, 5]},
        "packages": [{"id": "P1", "warehouse": "W99", "destination": [30, 40]}]
    }
    try:
        validate_delivery_data(data)
        assert False, "Expected ValidationError"
    except ValidationError as e:
        assert "references warehouse 'W99'" in str(e)


def test_missing_warehouses_root():
    data = {"agents": {"A1": [5, 5]}, "packages": []}
    try:
        validate_delivery_data(data)
        assert False, "Expected ValidationError"
    except ValidationError as e:
        assert "Missing or invalid 'warehouses'" in str(e)


def test_invalid_coordinates():
    data = {
        "warehouses": {"W1": [0, "invalid"]},
        "agents": {"A1": [5, 5]},
        "packages": [{"id": "P1", "warehouse": "W1", "destination": [10, 20]}]
    }
    try:
        validate_delivery_data(data)
        assert False, "Expected ValidationError"
    except ValidationError as e:
        assert "must have coordinate pair [x, y]" in str(e)


if __name__ == "__main__":
    test_valid_data()
    test_invalid_warehouse_reference()
    test_missing_warehouses_root()
    test_invalid_coordinates()
    print("✓ All validator tests passed!")

