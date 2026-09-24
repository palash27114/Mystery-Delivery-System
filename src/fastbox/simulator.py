"""
Simulation engine for FastBox one-day delivery dispatch.
"""

import random
from typing import Dict, List, Tuple
from .models import Warehouse, Agent, Package, DeliveryStep, AgentStats, SimulationReport, Point
from .distance import euclidean_distance
from .analytics import calculate_efficiency, get_best_agent


def find_nearest_agent(warehouse_pos: Point, current_agent_positions: Dict[str, Point]) -> str:
    """
    Find the agent closest to the warehouse based on Euclidean distance.
    """
    return min(
        current_agent_positions.keys(),
        key=lambda aid: euclidean_distance(current_agent_positions[aid], warehouse_pos)
    )


def simulate_day(
    warehouses: Dict[str, Warehouse],
    agents: Dict[str, Agent],
    packages: List[Package],
    simulate_delays: bool = True
) -> SimulationReport:
    """
    Simulates one day of deliveries:
      1. For each package, finds the nearest available agent based on current position.
      2. Agent moves from current location -> warehouse (picks up package).
      3. Agent moves from warehouse -> destination (delivers package).
      4. Agent's location is updated to the destination.
      5. Calculates total distance, delivered count, and efficiency for all agents.

    Args:
        warehouses: Mapping of warehouse ID to Warehouse object.
        agents: Mapping of agent ID to initial Agent object.
        packages: Ordered list of Package objects to deliver.
        simulate_delays: Whether to generate random delivery delays (1-15 min).

    Returns:
        SimulationReport containing stats, best agent, and full delivery logs.
    """
    # Track mutable positions throughout the day
    agent_positions: Dict[str, Point] = {aid: agent.location for aid, agent in agents.items()}

    # Initialize statistics for all agents
    agent_stats: Dict[str, AgentStats] = {aid: AgentStats() for aid in agents.keys()}
    delivery_log: List[DeliveryStep] = []

    for pkg in packages:
        wh = warehouses[pkg.warehouse_id]
        nearest_agent_id = find_nearest_agent(wh.location, agent_positions)

        agent_start = agent_positions[nearest_agent_id]
        wh_pos = wh.location
        dest_pos = pkg.destination

        # Distance calculations
        d_to_warehouse = euclidean_distance(agent_start, wh_pos)
        d_to_dest = euclidean_distance(wh_pos, dest_pos)
        trip_distance = d_to_warehouse + d_to_dest

        delay = random.randint(1, 15) if simulate_delays else 0

        # Log step
        delivery_log.append(DeliveryStep(
            package_id=pkg.id,
            agent_id=nearest_agent_id,
            warehouse_id=pkg.warehouse_id,
            agent_start_pos=agent_start,
            warehouse_pos=wh_pos,
            destination_pos=dest_pos,
            distance_to_warehouse=round(d_to_warehouse, 2),
            distance_to_destination=round(d_to_dest, 2),
            trip_distance=round(trip_distance, 2),
            delay_minutes=delay
        ))

        # Update stats
        stats = agent_stats[nearest_agent_id]
        stats.packages_delivered += 1
        stats.total_distance += trip_distance

        # Agent arrives at destination
        agent_positions[nearest_agent_id] = dest_pos

    # Calculate final efficiencies and round totals
    for aid, stats in agent_stats.items():
        stats.efficiency = calculate_efficiency(stats)
        stats.total_distance = round(stats.total_distance, 2)

    best_agent = get_best_agent(agent_stats)

    return SimulationReport(
        agent_stats=agent_stats,
        best_agent=best_agent,
        delivery_log=delivery_log,
        total_packages=len(packages),
        total_delivered=len(delivery_log)
    )

