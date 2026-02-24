from __future__ import annotations

from typing import Dict, List

import pandas as pd

from transport_system.agents.data_agent import DataAgent
from transport_system.agents.emissions_agent import EmissionsAgent
from transport_system.agents.energy_agent import EnergySystemAgent
from transport_system.agents.freight_agent import FreightOptimizationAgent
from transport_system.agents.policy_agent import PolicyAgent
from transport_system.agents.sustainability_agent import SustainabilityAgent
from transport_system.agents.transport_agent import TransportSimulationAgent
from transport_system.schemas import RunResult, Scenario


class IntegrationAgent:
    """Coordinator that runs the full multi-agent pipeline for a given scenario."""

    def __init__(self, data_agent: DataAgent | None = None) -> None:
        self.data_agent = data_agent or DataAgent()
        self.emissions_agent = EmissionsAgent()
        self.transport_agent = TransportSimulationAgent()
        self.freight_agent = FreightOptimizationAgent()
        self.energy_agent = EnergySystemAgent()
        self.sustainability_agent = SustainabilityAgent()
        self.policy_agent = PolicyAgent()

    def run_scenario(self, scenario: Scenario) -> RunResult:
        bundle = self.data_agent.load()

        # Transport simulation with ASI levers
        t_out = self.transport_agent.simulate(
            traffic_links=bundle.traffic_links,
            passenger_demand=bundle.passenger_demand,
            avoid_factor=scenario.avoid_demand_reduction,
            shift_to_public=scenario.shift_to_public_transport,
            improve_efficiency_factor=scenario.improve_efficiency,
        )

        # Freight optimization and related emissions
        freight_out = self.freight_agent.optimize(
            freight_shipments=bundle.freight_shipments,
            shift_road_to_rail=scenario.freight_shift_road_to_rail,
            efficiency_gain=scenario.improve_efficiency,
        )

        freight_emis = self.emissions_agent.freight_emissions(
            freight_shipments=bundle.freight_shipments,
            road_share=freight_out["freight_road_share"],
        )

        # Passenger emissions and energy system interaction
        pass_emis = self.emissions_agent.passenger_emissions(bundle.passenger_demand)

        energy_out = self.energy_agent.evaluate(
            passenger_vehicle_km=pass_emis["passenger_vehicle_km"],
            ev_share=scenario.ev_adoption,
            grid_emission_factor_kg_per_kwh=scenario.grid_emission_factor_kg_per_kwh,
        )

        total_co2_kg = (
            pass_emis["passenger_co2_kg"]
            + freight_emis["freight_total_co2_kg"]
            + energy_out["total_co2_kg"]
        )

        sust = self.sustainability_agent.compute(
            total_co2_kg=total_co2_kg,
            congestion_index=t_out["congestion_index"],
            avg_travel_time_min=t_out["avg_travel_time_min"],
            opportunities=bundle.opportunities,
        )

        policy = self.policy_agent.recommend(scenario=scenario, kpis={})

        kpis: Dict[str, float] = {
            # Transport
            **t_out,
            # Passenger emissions
            **pass_emis,
            # Freight
            **freight_out,
            **freight_emis,
            # Energy
            **energy_out,
            # Sustainability
            **sust,
            # Totals
            "system_total_co2_kg": float(total_co2_kg),
        }

        tables: Dict[str, pd.DataFrame] = {
            "traffic_links": bundle.traffic_links,
            "passenger_demand": bundle.passenger_demand,
            "freight_shipments": bundle.freight_shipments,
            "opportunities": bundle.opportunities,
            "scenario_summary": pd.DataFrame([kpis]),
        }

        # Attach policy text as a small single-row table to surface in dashboards.
        tables["policy"] = pd.DataFrame([policy])

        return RunResult(scenario=scenario, kpis=kpis, tables=tables)

    def compare_scenarios(self, scenarios: List[Scenario]) -> pd.DataFrame:
        rows = []
        for sc in scenarios:
            res = self.run_scenario(sc)
            row = {"scenario": sc.name} | res.kpis
            rows.append(row)
        return pd.DataFrame(rows)

