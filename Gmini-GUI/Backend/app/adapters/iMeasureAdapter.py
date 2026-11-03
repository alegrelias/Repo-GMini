from abc import ABC, abstractmethod
from app.models.measureSetup import MeasureSetup
from app.models.measureResult import MeasureResult

#Interfaz para los adaptadores de medicion
class IMeasureAdapter(ABC):
    @abstractmethod
    def encode_execution(self, setup: MeasureSetup) -> str:
        pass

    @abstractmethod
    def decode(self, response: str) -> MeasureResult:
        pass