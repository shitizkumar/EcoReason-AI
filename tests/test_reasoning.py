from models import EnvironmentalState
from reasoning import assess


def test_multi_metric_soil_water_risk():
    state = EnvironmentalState(
        organic_carbon=0.3,
        rainfall_mm=500,
        land_use="monoculture",
        species_richness=12,
    )

    risks = assess(state)

    risk_ids = {risk["id"] for risk in risks}

    assert "soil_water_stress" in risk_ids
    assert "habitat_diversity_loss" in risk_ids


def test_no_risk_for_normal_conditions():
    state = EnvironmentalState(
        organic_carbon=1.5,
        rainfall_mm=1200,
        land_use="mixed farming",
        species_richness=50,
    )

    risks = assess(state)

    assert risks == []


def test_deforestation_risk():
    state = EnvironmentalState(
        deforestation="high",
        species_richness=10,
    )

    risks = assess(state)

    risk_ids = {risk["id"] for risk in risks}

    assert "habitat_fragmentation" in risk_ids