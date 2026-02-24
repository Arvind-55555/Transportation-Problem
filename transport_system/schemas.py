from __future__ import annotations

from pydantic import BaseModel, Field


class Scenario(BaseModel):
    name: str = "baseline"

    # ASI levers (0..1 as fractions)
    avoid_demand_reduction: float = Field(0.0, ge=0.0, le=0.8)
    shift_to_public_transport: float = Field(0.0, ge=0.0, le=0.8)
    improve_efficiency: float = Field(0.0, ge=0.0, le=0.8)

    # Tech transitions
    ev_adoption: float = Field(0.1, ge=0.0, le=1.0)
    freight_shift_road_to_rail: float = Field(0.0, ge=0.0, le=0.9)

    # We keep these in scenario so the dashboard can explore uncertainty.
    grid_emission_factor_kg_per_kwh: float = Field(0.72, ge=0.05, le=1.5)


class RunResult(BaseModel):
    scenario: Scenario
    kpis: dict
    tables: dict
