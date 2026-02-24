from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import pandas as pd

from transport_system.utils.math_models import bpr_travel_time, efficiency


@dataclass
class TransportOutputs:
    avg_speed_kmph: float
    avg_travel_time_min: float
    congestion_index: float
    efficiency_score: float


class TransportSimulationAgent:
    """Very lightweight traffic simulation using a BPR-style volume–delay function."""

    def simulate(
        self,
        traffic_links: pd.DataFrame,
        passenger_demand: pd.DataFrame,
        avoid_factor: float = 0.0,
        shift_to_public: float = 0.0,
        improve_efficiency_factor: float = 0.0,
    ) -> Dict[str, float]:
        # Effective demand after "Avoid" and "Shift" levers.
        base_trips = passenger_demand["peak_hour_trips"].sum()
        reduced_trips = base_trips * (1.0 - avoid_factor)
        motorized_trips = reduced_trips * (1.0 - shift_to_public)

        # Allocate volume evenly across links for this simple prototype.
        num_links = max(len(traffic_links), 1)
        volume_per_link = motorized_trips / num_links

        times = []
        speeds = []
        congestion = []

        for _, row in traffic_links.iterrows():
            tt = bpr_travel_time(
                free_flow_time=row["free_flow_time_min"],
                volume=volume_per_link,
                capacity=row["capacity_vph"],
            )
            # Apply "Improve" lever as a reduction in generalized travel time.
            tt *= 1.0 - 0.3 * improve_efficiency_factor
            times.append(tt)
            # speed = distance / time
            hr = tt / 60.0
            speeds.append(row["length_km"] / hr if hr > 0 else 0.0)
            congestion.append(tt / row["free_flow_time_min"])

        avg_time = float(sum(times) / len(times)) if times else 0.0
        avg_speed = float(sum(speeds) / len(speeds)) if speeds else 0.0
        congestion_index = float(sum(congestion) / len(congestion)) if congestion else 1.0

        eff = efficiency(
            output=motorized_trips,
            energy=1.0,  # normalized
            time=avg_time,
            cost=congestion_index,
        )

        return {
            "avg_travel_time_min": avg_time,
            "avg_speed_kmph": avg_speed,
            "congestion_index": congestion_index,
            "transport_efficiency": float(eff),
            "peak_hour_trips_effective": float(motorized_trips),
        }

