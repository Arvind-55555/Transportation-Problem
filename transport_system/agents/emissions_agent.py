from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import pandas as pd

from transport_system.utils.math_models import emissions, freight_emissions


@dataclass
class EmissionFactors:
    # Rough, illustrative factors (g per vehicle-km or per tonne-km)
    passenger_road_g_per_vkm: float = 180.0
    freight_road_g_per_tkm: float = 90.0
    freight_rail_g_per_tkm: float = 25.0


class EmissionsAgent:
    """Computes operational emissions for passenger and freight flows."""

    def __init__(self, factors: EmissionFactors | None = None) -> None:
        self.factors = factors or EmissionFactors()

    def passenger_emissions(self, passenger_demand: pd.DataFrame, avg_occupancy: float = 1.6) -> Dict[str, float]:
        # Approximate vehicle-km from trips and average trip length / occupancy
        total_trips = passenger_demand["peak_hour_trips"].sum()
        avg_trip_km = passenger_demand["avg_trip_km"].mean()
        vehicle_km = (total_trips * avg_trip_km) / max(avg_occupancy, 0.1)

        co2_kg = emissions(
            activity=vehicle_km,
            emission_factor=self.factors.passenger_road_g_per_vkm / 1000.0,
        )

        return {
            "passenger_vehicle_km": float(vehicle_km),
            "passenger_co2_kg": float(co2_kg),
        }

    def freight_emissions(
        self,
        freight_shipments: pd.DataFrame,
        road_share: float = 1.0,
    ) -> Dict[str, float]:
        # Split tonnage between road and rail
        total_tonne_km = (freight_shipments["tonnes"] * 300.0).sum()  # assume average 300 km
        road_tkm = total_tonne_km * road_share
        rail_tkm = total_tonne_km * (1.0 - road_share)

        road_co2_kg = freight_emissions(
            volume_tonnes=1.0,
            distance_km=road_tkm,
            energy_intensity_mj_per_tkm=1.0,
            carbon_intensity_kg_per_mj=self.factors.freight_road_g_per_tkm / 1000.0,
        )
        rail_co2_kg = freight_emissions(
            volume_tonnes=1.0,
            distance_km=rail_tkm,
            energy_intensity_mj_per_tkm=1.0,
            carbon_intensity_kg_per_mj=self.factors.freight_rail_g_per_tkm / 1000.0,
        )

        return {
            "freight_tonne_km": float(total_tonne_km),
            "freight_road_co2_kg": float(road_co2_kg),
            "freight_rail_co2_kg": float(rail_co2_kg),
            "freight_total_co2_kg": float(road_co2_kg + rail_co2_kg),
        }

