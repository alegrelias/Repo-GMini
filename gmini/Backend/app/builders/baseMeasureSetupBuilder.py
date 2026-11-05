from abc import ABC, abstractmethod
from app.models.measureSetup import MeasureSetup

class BaseMeasureSetupBuilder(ABC):
    def __init__(self):
        self._observations: str = ""

    def with_observations(self, obs: str):
        self._observations = obs
        return self

    @abstractmethod
    def build(self) -> MeasureSetup:
        pass