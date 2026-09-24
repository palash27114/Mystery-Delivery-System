"""
Analytics and performance evaluation for FastBox delivery agents.
"""

from typing import Dict, Optional
from .models import AgentStats


def calculate_efficiency(stats: AgentStats) -> float:
    """
    Calculate agent efficiency score.
    
    Formula: efficiency = total_distance / packages_delivered
    Lower score is better (represents less distance traveled per package).
    
    Handles 0 delivered packages gracefully to avoid division-by-zero.
    """
    if stats.packages_delivered > 0:
        return round(stats.total_distance / stats.packages_delivered, 2)
    return 0.0


def get_best_agent(agent_stats: Dict[str, AgentStats]) -> Optional[str]:
    """
    Find the most efficient agent based on the lowest efficiency score.
    Only considers agents who delivered at least one package.
    """
    active_agents = {aid: s for aid, s in agent_stats.items() if s.packages_delivered > 0}
    if not active_agents:
        return None

    return min(active_agents.keys(), key=lambda aid: active_agents[aid].efficiency)

