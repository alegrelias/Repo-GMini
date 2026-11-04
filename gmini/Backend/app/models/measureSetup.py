from abc import ABC
from typing import Optional, List

class MeasureSetup(ABC):
    """Clase abstracta base para configuraciones de medición (sin parámetros analógicos)"""
    def __init__(self):
        self._measure_setup_id: Optional[int] = None
        self._observations: str = ""

    def get_id(self) -> Optional[int]: return self._measure_setup_id
    def set_id(self, setup_id: int) -> None: self._measure_setup_id = setup_id
    def set_observations(self, obs: str) -> None: self._observations = obs

class SingleMeasureSetup(MeasureSetup):
    """Configuración para medición de Monofrecuencia"""
    def __init__(self, freq: float, delay: int, count: int):
        super().__init__()
        self.freq: float = freq
        self.delay: int = delay
        self.count: int = count

class SpecMeasureSetup(MeasureSetup):
    """Configuración para medición por Espectroscopía"""
    def __init__(self, startfreq: float, incfreq: float, steps: int, repeat: int):
        super().__init__()
        self.startfreq: float = startfreq
        self.incfreq: float = incfreq
        self.steps: int = steps
        self.repeat: int = repeat

class MultiMeasureSetup(MeasureSetup):
    """Configuración para medición de Multifrecuencia"""
    def __init__(self, freq_list: List[float]):
        super().__init__()
        self.freq_list: List[float] = freq_list