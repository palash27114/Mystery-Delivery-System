"""
ASCII Map Visualizer for FastBox delivery routes.
"""

from typing import Dict, List
from .models import Warehouse, Agent, Package


def render_ascii_map(
    warehouses: Dict[str, Warehouse],
    agents: Dict[str, Agent],
    packages: List[Package],
    grid_width: int = 60,
    grid_height: int = 20
) -> str:
    """
    Render a 2D ASCII grid representing warehouses (W), agent starting positions (A),
    and package delivery destinations (D).
    """
    # Collect all coordinates to compute boundary box
    all_x = [w.location[0] for w in warehouses.values()] + \
            [a.location[0] for a in agents.values()] + \
            [p.destination[0] for p in packages]
    all_y = [w.location[1] for w in warehouses.values()] + \
            [a.location[1] for a in agents.values()] + \
            [p.destination[1] for p in packages]

    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)

    range_x = (max_x - min_x) if max_x != min_x else 1.0
    range_y = (max_y - min_y) if max_y != min_y else 1.0

    def to_grid(x: float, y: float):
        gx = int((x - min_x) / range_x * (grid_width - 1))
        gy = int((y - min_y) / range_y * (grid_height - 1))
        # Invert y for standard Cartesian display (top to bottom)
        return max(0, min(grid_width - 1, gx)), max(0, min(grid_height - 1, (grid_height - 1) - gy))

    # Initialize empty grid
    grid = [["." for _ in range(grid_width)] for _ in range(grid_height)]

    # Plot Destinations (D)
    for p in packages:
        gx, gy = to_grid(p.destination[0], p.destination[1])
        grid[gy][gx] = "D"

    # Plot Warehouses (W)
    for w in warehouses.values():
        gx, gy = to_grid(w.location[0], w.location[1])
        grid[gy][gx] = "W"

    # Plot Agents (A)
    for a in agents.values():
        gx, gy = to_grid(a.location[0], a.location[1])
        grid[gy][gx] = "A"

    lines = []
    lines.append("+" + "-" * grid_width + "+")
    for row in grid:
        lines.append("|" + "".join(row) + "|")
    lines.append("+" + "-" * grid_width + "+")
    lines.append("Legend: [W] Warehouse  |  [A] Agent Start  |  [D] Destination")

    return "\n".join(lines)
