from datetime import datetime
from typing import Optional, Literal
from app.models.measureSetup import MeasureSetup
from app.models.measureResult import MeasureResult

class Measure:
    def __init__(self, measureSetup: MeasureSetup, device_id: int):
        #atributos 
        self._measure_id: Optional[int] = None
        self._measure_setup: MeasureSetup = measureSetup
        self._date: datetime = datetime.now()
        self._file_name: str = ""
        self._state: Literal['EXECUTING', 'COMPLETE', 'ERROR'] = 'EXECUTING'
        self._device_id: int = device_id
        self._device_temp: float = 0.0
        self._result: Optional[MeasureResult] = None
        self._observations: str = ""
        self._loop_group_id: str = ""
        self._iteration_number: int = 1

    #geters
    def get_device_id(self) -> int:
        return self._device_id

    def get_measure_result(self) -> Optional[MeasureResult]:
        return self._result

    def get_file_name(self) -> str:
        return self._file_name

    def get_observations(self) -> str:
        return self._observations

    def get_measure_setup(self) -> MeasureSetup:
        return self._measure_setup

    def get_state(self) -> str:
        return self._state

    #Setters y Métodos de acción
    def set_default_name(self) -> None:
        #Genera el nombre automatico basado en el estándar ISO 8601 (Requisito PER-04)
        self._file_name = f"MED_{self._date.strftime('%Y%m%dT%H%M%S')}"

    def set_file_name(self, new_name: str) -> None:
        self._file_name = new_name

    def set_observations(self, obs: str) -> None:
        self._observations = obs

    def set_state(self, new_state: Literal['EXECUTING', 'COMPLETE', 'ERROR']) -> None:
        if new_state in ['EXECUTING', 'COMPLETE', 'ERROR']:
            self._state = new_state
        else:
            raise ValueError(f"Estado '{new_state}' no permitido.")
            
    #Metodo adicional necesario para ensamblar el resultado al finalizar la medición
    def set_result(self, result: MeasureResult) -> None:
        self._result = result