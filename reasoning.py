from models import EnvironmentalState


def assess(state: EnvironmentalState) -> list[dict]:
    risks = []

    if (
        state.organic_carbon is not None
        and state.rainfall_mm is not None
        and state.organic_carbon < 0.5
        and state.rainfall_mm < 700
    ):
        risks.append({
            "id": "soil_water_stress",
            "metrics": [
                "organic_carbon",
                "rainfall_mm",
                "moisture",
            ],
            "reason": (
                "Low soil organic carbon combined with limited "
                "rainfall can reduce soil water resilience."
            ),
        })

    if (
        state.land_use
        and state.species_richness is not None
        and state.land_use.lower() == "monoculture"
        and state.species_richness < 20
    ):
        risks.append({
            "id": "habitat_diversity_loss",
            "metrics": [
                "land_use",
                "species_richness",
                "habitat_diversity",
            ],
            "reason": (
                "Monoculture combined with low species richness "
                "can indicate limited habitat diversity."
            ),
        })

    if (
        state.deforestation
        and state.species_richness is not None
        and state.deforestation.lower() in {"medium", "high"}
        and state.species_richness < 20
    ):
        risks.append({
            "id": "habitat_fragmentation",
            "metrics": [
                "deforestation",
                "species_richness",
            ],
            "reason": (
                "Habitat loss combined with low species richness "
                "can increase biodiversity pressure."
            ),
        })

    return risks