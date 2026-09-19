from pydantic import BaseModel
from typing import Optional


class EnvironmentalState(BaseModel):
    ph: Optional[float] = None
    organic_carbon: Optional[float] = None
    moisture: Optional[float] = None

    rainfall_mm: Optional[float] = None
    temperature_c: Optional[float] = None

    land_use: Optional[str] = None
    crop: Optional[str] = None

    species_richness: Optional[int] = None
    habitat_diversity: Optional[float] = None

    pollution: Optional[str] = None
    deforestation: Optional[str] = None