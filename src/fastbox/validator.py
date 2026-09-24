"""
Schema and business logic validation for input delivery data.
"""

from typing import Dict, Any, Tuple, List
from .models import Warehouse, Agent, Package


class ValidationError(ValueError):
    """Raised when the input JSON data violates schema or business rules."""
    pass


def validate_delivery_data(raw_data: Any) -> Tuple[Dict[str, Warehouse], Dict[str, Agent], List[Package]]:
    """
    Strictly validates raw parsed JSON against FastBox requirements.

    Ensures:
      1. Root is a dictionary containing 'warehouses', 'agents', and 'packages'.
      2. 'warehouses' is a non-empty mapping of ID -> [x, y].
      3. 'agents' is a non-empty mapping of ID -> [x, y].
      4. 'packages' is a non-empty list of dicts with 'id', 'warehouse', 'destination' [x, y].
      5. All coordinates are 2-element numerical lists/tuples.
      6. All package warehouse references exist in the warehouses mapping.

    Returns:
        Tuple of (warehouses_dict, agents_dict, packages_list)
    """
    if not isinstance(raw_data, dict):
        raise ValidationError("Root JSON must be a dictionary containing 'warehouses', 'agents', and 'packages'.")

    # 1. Validate Warehouses
    if "warehouses" not in raw_data or not isinstance(raw_data["warehouses"], dict):
        raise ValidationError("Missing or invalid 'warehouses' object. Expected: {\"W1\": [x, y], ...}")
    
    if len(raw_data["warehouses"]) == 0:
        raise ValidationError("'warehouses' must contain at least one warehouse.")

    warehouses: Dict[str, Warehouse] = {}
    for wid, loc in raw_data["warehouses"].items():
        if not (isinstance(loc, (list, tuple)) and len(loc) == 2 and all(isinstance(v, (int, float)) for v in loc)):
            raise ValidationError(f"Warehouse '{wid}' must have coordinate pair [x, y] with 2 numbers. Found: {loc}")
        warehouses[wid] = Warehouse(id=str(wid), location=(float(loc[0]), float(loc[1])))

    # 2. Validate Agents
    if "agents" not in raw_data or not isinstance(raw_data["agents"], dict):
        raise ValidationError("Missing or invalid 'agents' object. Expected: {\"A1\": [x, y], ...}")

    if len(raw_data["agents"]) == 0:
        raise ValidationError("'agents' must contain at least one agent.")

    agents: Dict[str, Agent] = {}
    for aid, loc in raw_data["agents"].items():
        if not (isinstance(loc, (list, tuple)) and len(loc) == 2 and all(isinstance(v, (int, float)) for v in loc)):
            raise ValidationError(f"Agent '{aid}' must have coordinate pair [x, y] with 2 numbers. Found: {loc}")
        agents[aid] = Agent(id=str(aid), location=(float(loc[0]), float(loc[1])))

    # 3. Validate Packages
    if "packages" not in raw_data or not isinstance(raw_data["packages"], list):
        raise ValidationError("Missing or invalid 'packages' list. Expected: [{\"id\": \"P1\", \"warehouse\": \"W1\", \"destination\": [x, y]}, ...]")

    if len(raw_data["packages"]) == 0:
        raise ValidationError("'packages' list must contain at least one package.")

    packages: List[Package] = []
    for idx, pkg in enumerate(raw_data["packages"]):
        if not isinstance(pkg, dict):
            raise ValidationError(f"Package item at index {idx} must be a dictionary.")

        pkg_id = pkg.get("id")
        if not pkg_id or not isinstance(pkg_id, str):
            raise ValidationError(f"Package at index {idx} is missing a valid 'id' string.")

        wh_id = pkg.get("warehouse")
        if not wh_id or not isinstance(wh_id, str):
            raise ValidationError(f"Package '{pkg_id}' is missing a valid 'warehouse' string key.")

        if wh_id not in warehouses:
            raise ValidationError(f"Package '{pkg_id}' references warehouse '{wh_id}' which does not exist in 'warehouses'.")

        dest = pkg.get("destination")
        if not (isinstance(dest, (list, tuple)) and len(dest) == 2 and all(isinstance(v, (int, float)) for v in dest)):
            raise ValidationError(f"Package '{pkg_id}' destination must be [x, y] coordinates with 2 numbers. Found: {dest}")

        packages.append(Package(
            id=pkg_id,
            warehouse_id=wh_id,
            destination=(float(dest[0]), float(dest[1]))
        ))

    return warehouses, agents, packages

