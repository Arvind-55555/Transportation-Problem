from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IndiaDefaults:
    # Approximate India grid emissions factor (kg CO2 / kWh).
    # This is a configurable default for scenario exploration.
    grid_emission_factor_kg_per_kwh: float = 0.72

    # Typical vehicle energy intensities (MJ per vehicle-km) for a coarse model.
    # For EVs, we'll use kWh/km directly in the energy agent.
    petrol_mj_per_vkm: float = 2.6
    diesel_mj_per_vkm: float = 3.0

    # Convert MJ -> kWh
    mj_per_kwh: float = 3.6


@dataclass(frozen=True)
class SustainabilityWeights:
    w_env: float = 0.35
    w_econ: float = 0.25
    w_social: float = 0.2
    w_perf: float = 0.2

