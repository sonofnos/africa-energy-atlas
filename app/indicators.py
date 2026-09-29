"""The subset of OWID's energy-data columns this platform ingests and serves.

Kept deliberately small and Africa-relevant rather than mirroring all ~90
columns in the source file -- each one maps to a real question AEF's mandate
cares about (the energy transition, not the full energy-data schema).
"""

INDICATORS: dict[str, dict[str, str]] = {
    "renewables_share_energy": {
        "label": "Renewables share of primary energy",
        "unit": "%",
    },
    "fossil_share_energy": {
        "label": "Fossil fuels share of primary energy",
        "unit": "%",
    },
    "electricity_generation": {
        "label": "Electricity generation",
        "unit": "TWh",
    },
    "per_capita_electricity": {
        "label": "Electricity generation per capita",
        "unit": "kWh",
    },
    "energy_per_capita": {
        "label": "Primary energy consumption per capita",
        "unit": "kWh",
    },
    "greenhouse_gas_emissions": {
        "label": "Greenhouse gas emissions from energy",
        "unit": "Mt CO2eq",
    },
}

SOURCE_COLUMNS = ["country", "year", "iso_code", "population", "gdp", *INDICATORS.keys()]
