from __future__ import annotations

from typing import Dict

from transport_system.schemas import Scenario


class PolicyAgent:
    """Maps ASI levers and technology choices into qualitative policy recommendations."""

    def recommend(self, scenario: Scenario, kpis: Dict) -> Dict[str, str]:
        recs: list[str] = []

        if scenario.avoid_demand_reduction > 0.2:
            recs.append("Strengthen transit-oriented development and promote compact mixed-use zoning.")
        if scenario.shift_to_public_transport > 0.2:
            recs.append("Expand and prioritize high-capacity public transport corridors and integrated ticketing.")
        if scenario.improve_efficiency > 0.2:
            recs.append("Deploy adaptive traffic signal control and congestion pricing in key corridors.")
        if scenario.ev_adoption > 0.3:
            recs.append("Accelerate EV charging infrastructure roll-out and targeted fiscal incentives.")
        if scenario.freight_shift_road_to_rail > 0.2:
            recs.append("Invest in multimodal logistics parks and dedicated freight corridors.")

        if not recs:
            recs.append("Baseline scenario – use this as a reference to compare low-carbon strategies.")

        return {
            "policy_summary": " | ".join(recs),
        }

