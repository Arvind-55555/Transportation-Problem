from __future__ import annotations

import math


def emissions(activity: float, emission_factor: float) -> float:
    # Emissions = Activity × Emission Factor
    return activity * emission_factor


def co2_from_energy(energy: float, emission_factor: float) -> float:
    # CO2 = Energy Consumption × Emission Factor
    return energy * emission_factor


def freight_emissions(
    volume_tonnes: float,
    distance_km: float,
    energy_intensity_mj_per_tkm: float,
    carbon_intensity_kg_per_mj: float,
) -> float:
    # Freight Emissions = Volume × Distance × Energy Intensity × Carbon Intensity
    return volume_tonnes * distance_km * energy_intensity_mj_per_tkm * carbon_intensity_kg_per_mj


def efficiency(output: float, energy: float, time: float, cost: float) -> float:
    # Efficiency = Output / (Energy + Time + Cost)
    denom = energy + time + cost
    return output / denom if denom > 0 else 0.0


def accessibility(opportunities, beta: float, costs) -> float:
    # Accessibility = Σ (Oj × e^(-βcij))
    # opportunities and costs are aligned iterables.
    total = 0.0
    for oj, cij in zip(opportunities, costs, strict=False):
        total += float(oj) * math.exp(-beta * float(cij))
    return total


def bpr_travel_time(
    free_flow_time: float, volume: float, capacity: float, alpha: float = 0.15, beta: float = 4.0
) -> float:
    # Classic congestion function used as a simple simulation primitive.
    if capacity <= 0:
        return float("inf")
    x = max(volume / capacity, 0.0)
    return free_flow_time * (1.0 + alpha * (x**beta))

