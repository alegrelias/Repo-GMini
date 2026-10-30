from typing import Optional, List
import statistics

#Clase que almacena y procesa los datos obtenidos de una medicion
class MeasureResult:
    def __init__(self, frequencies: List[float], amplitudes: List[float], phases: List[float], impedances: List[complex]):
        #atributos
        self._m_resul_id: Optional[int] = None
        self._frequencies: List[float] = frequencies
        self._amplitudes: List[float] = amplitudes
        self._phases: List[float] = phases
        self._impedances: List[complex] = impedances

    #geters y seters
    def get_id(self) -> Optional[int]:
        return self._m_resul_id

    def set_id(self, result_id: int) -> None:
        self._m_resul_id = result_id

    def get_frequencies(self) -> List[float]:
        return self._frequencies

    def get_amplitudes(self) -> List[float]:
        return self._amplitudes

    def get_phases(self) -> List[float]:
        return self._phases

    def get_impedances(self) -> List[complex]:
        return self._impedances

    #metodos de cálculo estadistico 
    #Calcula y retorna la media (promedio) de las métricas
    def measure_mean(self) -> List[float]:
        mean_amplitude = statistics.mean(self._amplitudes) if self._amplitudes else 0.0
        mean_phase = statistics.mean(self._phases) if self._phases else 0.0
        #retorna un arreglo con las medias requeridas para graficar o mostrar
        return [mean_amplitude, mean_phase]
    #Calcula y retorna la desviacion estandar de las metricas
    def measure_std(self) -> List[float]:
        #requiere al menos 2 valores para calcular la desviacion estndar
        std_amplitude = statistics.stdev(self._amplitudes) if len(self._amplitudes) > 1 else 0.0
        std_phase = statistics.stdev(self._phases) if len(self._phases) > 1 else 0.0
        return [std_amplitude, std_phase]