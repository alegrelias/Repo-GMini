from abc import ABC
from typing import Optional, List

class MeasureSetup(ABC):
    #Clase abstracta base para todas las configuraciones de medición.
    def __init__(self, exitation_voltage: float, gain: float, rfbvalue: float, settcycles: int, mux_channel: List[int]):
        self._measure_setup_id: Optional[int] = None
        self._observations: str = ""
        self._exitation_voltage: float = exitation_voltage
        self._gain: float = gain
        self._rfbvalue: float = rfbvalue
        self._settcycles: int = settcycles
        self._mux_channel: List[int] = mux_channel  

    def get_id(self) -> Optional[int]:
        return self._measure_setup_id

    def set_id(self, setup_id: int) -> None:
        self._measure_setup_id = setup_id

    def set_observations(self, obs: str) -> None:
        self._observations = obs


class SingleMeasureSetup(MeasureSetup):
    """
    Configuración para medición de Monofrecuencia.
    """
    def __init__(self, exitation_voltage: float, gain: float, rfbvalue: float, settcycles: int, mux_channel: List[int],freq: float, delay: int, count: int):
        super().__init__(exitation_voltage, gain, rfbvalue, settcycles, mux_channel)
        self.freq: float = freq
        self.delay: int = delay
        self.count: int = count


class SpecMeasureSetup(MeasureSetup):
    """
    Configuración para medición por Espectroscopía (Barrido espectral).
    """
    def __init__(self, exitation_voltage: float, gain: float, rfbvalue: float, settcycles: int, mux_channel: List[int],startfreq: float, incfreq: float, steps: int, repeat: int):
        super().__init__(exitation_voltage, gain, rfbvalue, settcycles, mux_channel)
        self.startfreq: float = startfreq
        self.incfreq: float = incfreq
        self.steps: int = steps
        self.repeat: int = repeat


class MultiMeasureSetup(MeasureSetup):
    """
    Configuración para medición de Multifrecuencia (frecuencias discretas).
    """
    def __init__(self, exitation_voltage: float, gain: float, rfbvalue: float, settcycles: int, mux_channel: List[int],freq_list: List[float]):
        super().__init__(exitation_voltage, gain, rfbvalue, settcycles, mux_channel)
        self.freq_list: List[float] = freq_list