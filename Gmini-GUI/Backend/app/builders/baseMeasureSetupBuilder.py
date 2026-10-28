from abc import ABC, abstractmethod
from typing import List

class BaseMeasureSetupBuilder(ABC):
    #atributos
    def __init__(self):
        self._observations: str = ""
        self._exitation_voltage: float = 0.0
        self._gain: float = 0.0
        self._rfbvalue: float = 0.0
        self._settcycles: int = 0
        self._mux_channel: List[int] = []

    #geters y seters
    def with_observations(self, obs: str) -> 'BaseMeasureSetupBuilder':
        self._observations = obs
        return self

    def with_voltage(self, voltage: float) -> 'BaseMeasureSetupBuilder':
        self._exitation_voltage = voltage
        return self

    def with_gain(self, gain: float) -> 'BaseMeasureSetupBuilder':
        self._gain = gain
        return self

    def with_rfb_value(self, rfb: float) -> 'BaseMeasureSetupBuilder':
        self._rfbvalue = rfb
        return self

    def with_cycles(self, cycles: int) -> 'BaseMeasureSetupBuilder':
        self._settcycles = cycles
        return self

    def with_mux_channel(self, channels: List[int]) -> 'BaseMeasureSetupBuilder':
        self._mux_channel = channels
        return self

    @abstractmethod
    def build(self):
        pass