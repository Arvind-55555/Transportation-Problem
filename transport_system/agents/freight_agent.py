from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import pandas as pd


@dataclass
class FreightOutputs:
    road_share: float
    rail_share: float
    empty_trip_reduction: float


class FreightOptimizationAgent:
    """Applies simple freight decarbonization logic (Avoid–Shift–Improve for freight)."""

    def optimize(
        self,
        freight_shipments: pd.DataFrame,
        shift_road_to_rail: float = 0.0,
        efficiency_gain: float = 0.0,
    ) -> Dict[str, float]:
        total_tonnes = freight_shipments["tonnes"].sum()
        baseline_empty_trip_share = 0.25
        improved_empty_trip_share = baseline_empty_trip_share * (1.0 - efficiency_gain)

        road_share = max(1.0 - shift_road_to_rail, 0.0)
        rail_share = 1.0 - road_share

        return {
            "freight_total_tonnes": float(total_tonnes),
            "freight_road_share": float(road_share),
            "freight_rail_share": float(rail_share),
            "freight_empty_trip_share": float(improved_empty_trip_share),
        }

