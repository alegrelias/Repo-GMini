from abc import ABC, abstractmethod
from app.models.calibrationSetup import CalibrationSetup

"""Interfaz para traducir el objeto CalibrationSetup a comandos CLI de la placa y evaluar la respuesta devuelta por el hardware"""
class ICalibrationAdapter(ABC):
    @abstractmethod
    def encode(self, setup: CalibrationSetup) -> str:
        pass

    @abstractmethod
    def decode(self, response: str) -> bool:
        pass