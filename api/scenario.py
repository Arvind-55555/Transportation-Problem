from __future__ import annotations

import json
import pathlib
import sys
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse


# Ensure project root is on sys.path so we can import transport_system
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from transport_system.agents.integration_agent import IntegrationAgent
from transport_system.schemas import Scenario


class handler(BaseHTTPRequestHandler):
    """
    Vercel Python Function entrypoint.

    Route: /api/scenario
    Method: GET
    Query params:
      - name: scenario name (str)
      - avoid: avoid demand reduction (float, 0–0.8)
      - shift: shift to public transport (float, 0–0.8)
      - improve: improve efficiency (float, 0–0.8)
      - ev: EV adoption share (float, 0–1)
      - freight_shift: freight shift road→rail (float, 0–0.9)
      - grid: grid emission factor (kg CO₂ / kWh)
    """

    def _parse_float(self, params, key: str, default: float) -> float:
        try:
            return float(params.get(key, [default])[0])
        except (TypeError, ValueError):
            return default

    def do_GET(self) -> None:  # noqa: N802 (Vercel requires this name)
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        scenario = Scenario(
            name=params.get("name", ["api-scenario"])[0],
            avoid_demand_reduction=self._parse_float(params, "avoid", 0.0),
            shift_to_public_transport=self._parse_float(params, "shift", 0.0),
            improve_efficiency=self._parse_float(params, "improve", 0.0),
            ev_adoption=self._parse_float(params, "ev", 0.1),
            freight_shift_road_to_rail=self._parse_float(params, "freight_shift", 0.0),
            grid_emission_factor_kg_per_kwh=self._parse_float(params, "grid", 0.72),
        )

        agent = IntegrationAgent()
        result = agent.run_scenario(scenario)

        payload = {
            "scenario": scenario.model_dump(),
            "kpis": result.kpis,
        }

        body = json.dumps(payload, default=float).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

