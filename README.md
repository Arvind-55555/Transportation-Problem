# The Net Zero Transportation Problem — India

---

## Overview

This repository is a **technical, research-driven companion project** to the book:

> **"The Net Zero Transportation Problem: Mobility, Emissions, and the Future of Clean Movement in India"**
`https://shorturl.at/COdo7`

It presents transportation as a **complex systems problem**, integrating:

- Mobility networks
- Energy systems
- Emissions modeling
- Urban planning
- Freight logistics
- AI-driven mobility systems

---

## Objective

To build a **comprehensive, data-driven, and system-level framework** for:

- Understanding transportation inefficiencies
- Quantifying emissions and energy use
- Designing low-emission mobility systems
- Developing integrated transport solutions for India

---

## Core Concept

```Sustainable Transport = Integration × Efficiency × Clean Energy × Intelligence```

---

## Project Structure

- `transport_system/` — core Python library
  - `agents/` — Data, Emissions, Transport Simulation, Freight, Energy, Sustainability, Policy, Integration agents
  - `utils/` — mathematical models and I/O helpers
  - `config.py` — India-specific defaults and sustainability weights
  - `schemas.py` — Pydantic models for scenarios and run results  
- `data/` — small example CSVs (traffic links, passenger demand, freight shipments, opportunities)
- `dashboard/` — Streamlit digital-twin and scenario explorer
- `notebooks/` — ML notebooks
  - `emissions_regression.ipynb` — regression model for emissions vs. activity
  - `traffic_clustering.ipynb` — clustering of links by congestion and speed

---

## Setup & Installation

From the project root:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

On macOS / Linux, activate the virtualenv with:

```bash
source .venv/bin/activate
```

---

## Running the Digital Twin Dashboard

With the virtualenv activated, run:

```bash
streamlit run dashboard/app.py
```

The app will:

- Load the example transport datasets
- Run the multi-agent pipeline via the `IntegrationAgent`
- Expose ASI levers and technology parameters in the sidebar
- Visualise emissions, congestion, and a sustainability index

---

## ML Notebooks

Open the notebooks in Jupyter or VS Code:

- `notebooks/emissions_regression.ipynb` — demonstrates learning an emission factor from synthetic data.
- `notebooks/traffic_clustering.ipynb` — clusters links into groups for network analysis.

Both notebooks import utility functions from `transport_system.utils.math_models` and are designed to be self-contained teaching artifacts.

---

## High-Level Architecture

```text
Data (CSV)  →  DataAgent
                  ↓
         ┌───────────────────────────────┐
         │  Multi-Agent Core             │
         │                               │
         │  TransportSimulationAgent     │
         │  EmissionsAgent               │
         │  FreightOptimizationAgent     │
         │  EnergySystemAgent            │
         │  SustainabilityAgent          │
         │  PolicyAgent                  │
         │                               │
         │  ← IntegrationAgent (orchestrator) ← Scenario inputs (ASI + tech) │
         └───────────────────────────────┘
                              ↓
                    KPIs, tables, policy text
                              ↓
                    Dashboard / ML notebooks
```

The design emphasises a **modular, extensible, and India-focused** framework for exploring low-carbon transport futures.

