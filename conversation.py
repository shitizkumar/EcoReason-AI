from models import EnvironmentalState


REQUIRED_FOR_ANALYSIS = [
    "organic_carbon",
    "rainfall_mm",
    "land_use",
]

class ConversationMemory:
    def __init__(self):
        self.state = EnvironmentalState()
        self.history = []

    def update(self, **values):
        self.state = self.state.model_copy(update=values)
        self.history.append(values)

    def missing(self) -> list[str]:
        return [
            field
            for field in REQUIRED_FOR_ANALYSIS
            if getattr(self.state, field) is None
        ]

    def clarification(self) -> str | None:
        missing = self.missing()

        if not missing:
            return None

        questions = {
            "organic_carbon": "What is the soil organic carbon (%)?",
            "rainfall_mm": "What is the approximate annual rainfall (mm)?",
            "land_use": "What is the current land use or cropping system?",
        }

        return questions[missing[0]]

    def context(self) -> dict:
        return {
            "state": self.state.model_dump(exclude_none=True),
            "history": self.history,
        }