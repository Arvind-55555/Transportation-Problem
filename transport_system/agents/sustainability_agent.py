from __future__ import annotations

from typing import Dict

from transport_system.config import SustainabilityWeights
from transport_system.utils.math_models import accessibility


class SustainabilityAgent:
    """Computes a composite sustainability index from environmental, economic, social, performance KPIs."""

    def __init__(self, weights: SustainabilityWeights | None = None) -> None:
        self.weights = weights or SustainabilityWeights()

    def compute(
        self,
        *,
        total_co2_kg: float,
        congestion_index: float,
        avg_travel_time_min: float,
        opportunities,
        beta_access: float = 0.15,
    ) -> Dict[str, float]:
        # Environmental: lower emissions -> higher score
        env_score = 1.0 / (1.0 + total_co2_kg / 1e6)

        # Economic: congestion as proxy for cost
        econ_score = 1.0 / (1.0 + (congestion_index - 1.0))

        # Social: gravity-based accessibility to jobs
        opp_jobs = opportunities["jobs"].tolist()
        # Use a simple cost proxy from index
        costs = [10 + i * 5 for i in range(len(opp_jobs))]
        acc = accessibility(opp_jobs, beta=beta_access, costs=costs)
        social_score = 1.0 - 1.0 / (1.0 + acc / 1e6)

        # Performance: travel time
        perf_score = 1.0 / (1.0 + avg_travel_time_min / 60.0)

        w = self.weights
        sustainability_index = (
            w.w_env * env_score + w.w_econ * econ_score + w.w_social * social_score + w.w_perf * perf_score
        )

        return {
            "env_score": float(env_score),
            "econ_score": float(econ_score),
            "social_score": float(social_score),
            "perf_score": float(perf_score),
            "sustainability_index": float(sustainability_index),
        }

