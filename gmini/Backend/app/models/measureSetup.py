from abc import ABC
from typing import List, Optional

"""Clase abstracta base para configuraciones de medición"""
class MeasureSetup(ABC):
    def __init__(self, observations: str = "", measure_setup_id: Optional[int] = None):
        self._measure_setup_id: Optional[int] = measure_setup_id
        self._observations: str = observations

    def get_id(self) -> Optional[int]:
        return self._measure_setup_id

    def get_observations(self) -> str:
        return self._observations

    def set_id(self, setup_id: int) -> None:
        self._measure_setup_id = setup_id

    def set_observations(self, obs: str) -> None:
        self._observations = obs

"""Configuración para barrido espectral / sweep"""
class SpecMeasureSetup(MeasureSetup):
    def __init__(self,
                 startfreq: float = 10000.0,
                 incfreq: float = 10000.0,
                 steps: int = 5,
                 repeat: int = 1,
                 observations: str = "",
                 measure_setup_id: Optional[int] = None):
        super().__init__(observations=observations, measure_setup_id=measure_setup_id)
        self._startfreq: float = float(startfreq)
        self._incfreq: float = float(incfreq)
        self._steps: int = int(steps)
        self._repeat: int = int(repeat)

    def get_start_freq(self) -> float: return self._startfreq
    def get_inc_freq(self) -> float: return self._incfreq
    def get_steps(self) -> int: return self._steps
    def get_repeat(self) -> int: return self._repeat

"""Configuración para monofrecuencia / singlefreq"""
class SingleMeasureSetup(MeasureSetup):
    def __init__(self,
                 freq: float = 10000.0,
                 delay: int = 0,
                 count: int = 1,
                 repeat: Optional[int] = None,
                 observations: str = "",
                 measure_setup_id: Optional[int] = None):
        super().__init__(observations=observations, measure_setup_id=measure_setup_id)
        self._freq: float = float(freq)
        self._delay: int = int(delay)
        self._count: int = int(repeat if repeat is not None else count)

    def get_freq(self) -> float: return self._freq
    def get_delay(self) -> int: return self._delay
    def get_count(self) -> int: return self._count
    def get_repeat(self) -> int: return self._count

"""Configuración para multifrecuencia"""
class MultiMeasureSetup(MeasureSetup):
    def __init__(self,
                 freq_list: Optional[List[float]] = None,
                 observations: str = "",
                 measure_setup_id: Optional[int] = None):
        super().__init__(observations=observations, measure_setup_id=measure_setup_id)
        self._freq_list: List[float] = [float(f) for f in (freq_list or [])]

    def get_freq_list(self) -> List[float]: return self._freq_list