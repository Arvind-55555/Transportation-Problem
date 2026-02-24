from __future__ import annotations

import pathlib
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from transport_system.agents.integration_agent import IntegrationAgent
from transport_system.schemas import Scenario


def run_dashboard() -> None:
    st.set_page_config(
        page_title="India Transport System Digital Twin",
        layout="wide",
    )

    st.title("India Transport System — Digital Twin & Scenario Explorer")
    st.markdown(
        """
This dashboard provides a **conceptual digital twin** of an Indian urban transport system.

Use the controls in the sidebar to explore **Avoid–Shift–Improve (ASI)** and technology scenarios,
and see their impact on:

- Emissions (passenger + freight + energy system)
- Congestion and travel times
- Energy consumption
- Sustainability index
"""
    )

    st.sidebar.header("Scenario controls")
    name = st.sidebar.text_input("Scenario name", value="baseline")

    st.sidebar.subheader("ASI policy levers")
    avoid = st.sidebar.slider("Avoid: demand reduction", 0.0, 0.8, 0.0, 0.05)
    shift = st.sidebar.slider("Shift: to public / non-motorised", 0.0, 0.8, 0.0, 0.05)
    improve = st.sidebar.slider("Improve: system efficiency", 0.0, 0.8, 0.0, 0.05)

    st.sidebar.subheader("Technology transitions")
    ev_share = st.sidebar.slider("EV adoption (passenger)", 0.0, 1.0, 0.1, 0.05)
    freight_shift = st.sidebar.slider("Freight shift road → rail", 0.0, 0.9, 0.0, 0.05)

    st.sidebar.subheader("Power system")
    grid_factor = st.sidebar.slider(
        "Grid emission factor (kg CO₂ / kWh)",
        0.3,
        1.2,
        0.72,
        0.02,
    )

    scenario = Scenario(
        name=name,
        avoid_demand_reduction=avoid,
        shift_to_public_transport=shift,
        improve_efficiency=improve,
        ev_adoption=ev_share,
        freight_shift_road_to_rail=freight_shift,
        grid_emission_factor_kg_per_kwh=grid_factor,
    )

    agent = IntegrationAgent()
    result = agent.run_scenario(scenario)
    kpis = result.kpis

    st.subheader("Key indicators")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("System CO₂ (kt)", f"{kpis['system_total_co2_kg'] / 1e3:,.1f}")
    col2.metric("Avg travel time (min)", f"{kpis['avg_travel_time_min']:.1f}")
    col3.metric("Congestion index", f"{kpis['congestion_index']:.2f}")
    col4.metric("Sustainability index", f"{kpis['sustainability_index']:.2f}")

    st.markdown("### Emissions breakdown")
    emis_df = pd.DataFrame(
        [
            {"component": "Passenger (direct)", "co2_kg": kpis["passenger_co2_kg"]},
            {"component": "Freight (road + rail)", "co2_kg": kpis["freight_total_co2_kg"]},
            {"component": "Vehicle + grid energy", "co2_kg": kpis["total_co2_kg"]},
        ]
    )
    fig_emis = px.bar(
        emis_df,
        x="component",
        y="co2_kg",
        labels={"co2_kg": "CO₂ (kg)", "component": "Component"},
        title="Emissions components",
    )
    st.plotly_chart(fig_emis, use_container_width=True)

    st.markdown("### Transport performance")
    perf_cols = ["avg_travel_time_min", "avg_speed_kmph", "congestion_index", "transport_efficiency"]
    perf_df = pd.DataFrame(
        [{"metric": m, "value": kpis[m]} for m in perf_cols],
    )
    fig_perf = px.bar(
        perf_df,
        x="metric",
        y="value",
        title="Transport performance metrics",
    )
    st.plotly_chart(fig_perf, use_container_width=True)

    st.markdown("### Policy narrative")
    st.write(result.tables["policy"]["policy_summary"].iloc[0])

    with st.expander("Scenario table (digital twin snapshot)"):
        st.dataframe(result.tables["scenario_summary"].T, use_container_width=True)

    with st.expander("Input datasets"):
        st.write("Traffic links")
        st.dataframe(result.tables["traffic_links"], use_container_width=True)
        st.write("Passenger OD demand")
        st.dataframe(result.tables["passenger_demand"], use_container_width=True)
        st.write("Freight shipments")
        st.dataframe(result.tables["freight_shipments"], use_container_width=True)


if __name__ == "__main__":
    run_dashboard()

