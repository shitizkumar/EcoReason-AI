from typing import Any


RECOMMENDATIONS: dict[str, dict[str, Any]] = {
    "soil_water_stress": {
        "action": "Introduce cover crops and suitable agroforestry practices.",
        "metrics": [
            "organic_carbon",
            "moisture",
            "rainfall_mm",
        ],
        "mechanism": (
            "Vegetative cover and organic inputs can improve soil "
            "structure, water retention, and soil biological activity."
        ),
        "horizon": "6–24 months",
    },
    "habitat_diversity_loss": {
        "action": "Introduce intercropping and native vegetation patches.",
        "metrics": [
            "species_richness",
            "habitat_diversity",
            "land_use",
        ],
        "mechanism": (
            "Greater vegetation diversity can provide additional "
            "habitats and ecological niches."
        ),
        "horizon": "1–3 years",
    },
    "habitat_fragmentation": {
        "action": "Restore native vegetation and connect fragmented habitats.",
        "metrics": [
            "species_richness",
            "deforestation",
        ],
        "mechanism": (
            "Connected native vegetation can improve habitat continuity "
            "and movement between suitable areas."
        ),
        "horizon": "2–5 years",
    },
}


def recommend(
    risks: list[dict],
    evidence: list[dict] | None = None,
) -> list[dict]:
    evidence = evidence or []
    evidence_map = {
        item["risk"]: item
        for item in evidence
    }

    recommendations = []

    for risk in risks:
        recommendation = RECOMMENDATIONS.get(risk["id"])

        if not recommendation:
            continue

        result = {
            "risk": risk["id"],
            **recommendation,
        }

        retrieved = evidence_map.get(risk["id"])

        if retrieved:
            result["evidence"] = retrieved.get("vector_results", [])

        recommendations.append(result)

    return recommendations