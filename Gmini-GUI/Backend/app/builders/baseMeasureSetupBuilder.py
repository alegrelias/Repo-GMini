from abc import ABC, abstractmethod
#Constructor abstracto para configuraciones de medicion (limpio de calibracion)
class BaseMeasureSetupBuilder(ABC):
    def __init__(self):
        self._observations: str = ""

    def with_observations(self, obs: str) -> 'BaseMeasureSetupBuilder':
        self._observations = obs
        return self

    @abstractmethod
    def build(self):
        pass