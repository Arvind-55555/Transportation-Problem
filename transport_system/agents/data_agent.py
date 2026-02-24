from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import pandas as pd


@dataclass
class DataBundle:
    traffic_links: pd.DataFrame
    passenger_demand: pd.DataFrame
    freight_shipments: pd.DataFrame
    opportunities: pd.DataFrame


class DataAgent:
    """Loads and preprocesses core datasets for the transport system."""

    def __init__(self, data_dir: str | Path = "data") -> None:
        self.data_dir = Path(data_dir)

    def load(self) -> DataBundle:
        traffic_links = pd.read_csv(self.data_dir / "traffic_links.csv")
        passenger_demand = pd.read_csv(self.data_dir / "passenger_demand.csv")
        freight_shipments = pd.read_csv(self.data_dir / "freight_shipments.csv")
        opportunities = pd.read_csv(self.data_dir / "opportunities.csv")

        return DataBundle(
            traffic_links=traffic_links,
            passenger_demand=passenger_demand,
            freight_shipments=freight_shipments,
            opportunities=opportunities,
        )

    def basic_stats(self, bundle: DataBundle) -> Dict[str, float]:
        return {
            "num_links": float(len(bundle.traffic_links)),
            "num_zones": float(bundle.opportunities["zone_id"].nunique()),
            "peak_hour_passenger_trips": float(bundle.passenger_demand["peak_hour_trips"].sum()),
            "daily_freight_tonnes": float(bundle.freight_shipments["tonnes"].sum()),
        }

