from __future__ import annotations

from typing import Dict

from transport_system.config import IndiaDefaults
from transport_system.utils.math_models import co2_from_energy


class EnergySystemAgent:
    """Estimates energy use and CO₂ for ICE vs EV under different EV adoption rates."""

    def __init__(self, defaults: IndiaDefaults | None = None) -> None:
        self.defaults = defaults or IndiaDefaults()

    def evaluate(
        self,
        passenger_vehicle_km: float,
        ev_share: float,
        grid_emission_factor_kg_per_kwh: float | None = None,
    ) -> Dict[str, float]:
        grid_factor = grid_emission_factor_kg_per_kwh or self.defaults.grid_emission_factor_kg_per_kwh

        # Simple energy intensities (kWh per vehicle-km)
        ice_kwh_per_vkm = (self.defaults.petrol_mj_per_vkm / self.defaults.mj_per_kwh)
        ev_kwh_per_vkm = 0.18  # typical EV car consumption ~ 0.15–0.2 kWh/km

        ev_vkm = passenger_vehicle_km * ev_share
        ice_vkm = passenger_vehicle_km * (1.0 - ev_share)

        ice_energy_kwh = ice_vkm * ice_kwh_per_vkm
        ev_energy_kwh = ev_vkm * ev_kwh_per_vkm

        ice_co2_kg = co2_from_energy(ice_energy_kwh, emission_factor=0.25)  # tank-to-wheel approx
        ev_co2_kg = co2_from_energy(ev_energy_kwh, emission_factor=grid_factor)

        return {
            "ice_energy_kwh": float(ice_energy_kwh),
            "ev_energy_kwh": float(ev_energy_kwh),
            "total_energy_kwh": float(ice_energy_kwh + ev_energy_kwh),
            "ice_co2_kg": float(ice_co2_kg),
            "ev_co2_kg": float(ev_co2_kg),
            "total_co2_kg": float(ice_co2_kg + ev_co2_kg),
        }

