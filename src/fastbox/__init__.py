"""
FastBox Mystery Delivery System
===============================
A production-grade algorithmic delivery dispatch and fleet efficiency tracking engine.
"""

from .models import Point, Warehouse, Agent, Package, DeliveryStep, AgentStats, SimulationReport
from .distance import euclidean_distance
from .validator import validate_delivery_data, ValidationError
from .simulator import simulate_day
from .analytics import calculate_efficiency, get_best_agent
from .reporter import save_json_report, save_csv_report

__version__ = "1.0.0"
__all__ = [
    "Point",
    "Warehouse",
    "Agent",
    "Package",
    "DeliveryStep",
    "AgentStats",
    "SimulationReport",
    "euclidean_distance",
    "validate_delivery_data",
    "ValidationError",
    "simulate_day",
    "calculate_efficiency",
    "get_best_agent",
    "save_json_report",
    "save_csv_report",
]

