from typing import List, Optional

class MeasureResult:
    #Entidad pura que almacena los resultados crudos de una medición
    def __init__(self, frequencies: List[float], amplitudes: List[float], 
                 phases: List[float], impedances: List[complex]):
        self._m_resul_id: Optional[int] = None
        self._frequencies: List[float] = frequencies
        self._amplitudes: List[float] = amplitudes
        self._phases: List[float] = phases
        self._impedances: List[complex] = impedances

    # Getters
    def get_id(self) -> Optional[int]:
        return self._m_resul_id

    def get_frequencies(self) -> List[float]:
        return self._frequencies

    def get_amplitudes(self) -> List[float]:
        return self._amplitudes

    def get_phases(self) -> List[float]:
        return self._phases

    def get_impedances(self) -> List[complex]:
        return self._impedances

    # Setters
    def set_id(self, result_id: int) -> None:
        self._m_resul_id = result_id