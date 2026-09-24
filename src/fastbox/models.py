"""
Domain data models for FastBox entities.
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Any, Optional

Point = Tuple[float, float]


@dataclass
class Warehouse:
    id: str
    location: Point


@dataclass
class Agent:
    id: str
    location: Point


@dataclass
class Package:
    id: str
    warehouse_id: str
    destination: Point


@dataclass
class DeliveryStep:
    package_id: str
    agent_id: str
    warehouse_id: str
    agent_start_pos: Point
    warehouse_pos: Point
    destination_pos: Point
    distance_to_warehouse: float
    distance_to_destination: float
    trip_distance: float
    delay_minutes: int = 0


@dataclass
class AgentStats:
    packages_delivered: int = 0
    total_distance: float = 0.0
    efficiency: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "packages_delivered": self.packages_delivered,
            "total_distance": round(self.total_distance, 2),
            "efficiency": round(self.efficiency, 2),
        }


@dataclass
class SimulationReport:
    agent_stats: Dict[str, AgentStats]
    best_agent: Optional[str]
    delivery_log: List[DeliveryStep] = field(default_factory=list)
    total_packages: int = 0
    total_delivered: int = 0

    def to_dict(self) -> Dict[str, Any]:
        result = {aid: stats.to_dict() for aid, stats in sorted(self.agent_stats.items())}
        result["best_agent"] = self.best_agent
        return result

