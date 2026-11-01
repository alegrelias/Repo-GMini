import uuid
from datetime import datetime
from typing import Optional, Literal
from app.models.measureSetup import MeasureSetup
from app.models.measureResult import MeasureResult

class Measure:
    """
    Entidad central que representa una sesión de medición individual.
    Vincula el setup utilizado, los resultados obtenidos y los metadatos de la ejecución.
    """
    def __init__(self, measure_setup: MeasureSetup, device_id: int):
        self._measure_id: Optional[int] = None
        self._measure_setup: MeasureSetup = measure_setup
        self._date: datetime = datetime.now()
        self._file_name: str = ""
        self._state: Literal['EXECUTING', 'COMPLETE', 'ERROR', 'PENDING'] = 'PENDING'
        self._device_id: int = device_id
        self._device_temp: float = 0.0
        self._result: Optional[MeasureResult] = None
        self._observations: str = ""
        
        # Identificador único para agrupar mediciones en bucle
        self._loop_group_id: str = uuid.uuid4().hex 
        self._iteration_number: int = 1

    # Getters
    def get_id(self) -> Optional[int]:
        return self._measure_id

    def get_measure_setup(self) -> MeasureSetup:
        return self._measure_setup

    def get_date(self) -> datetime:
        return self._date

    def get_file_name(self) -> str:
        return self._file_name

    def get_state(self) -> str:
        return self._state

    def get_device_id(self) -> int:
        return self._device_id

    def get_device_temp(self) -> float:
        return self._device_temp

    def get_measure_result(self) -> Optional[MeasureResult]:
        return self._result

    def get_observations(self) -> str:
        return self._observations

    def get_loop_group_id(self) -> str:
        return self._loop_group_id

    def get_iteration_number(self) -> int:
        return self._iteration_number

    # Setters y métodos de estado
    def set_id(self, measure_id: int) -> None:
        self._measure_id = measure_id

    def set_file_name(self, new_name: str) -> None:
        self._file_name = new_name

    def set_observations(self, obs: str) -> None:
        self._observations = obs

    def set_state(self, new_state: Literal['EXECUTING', 'COMPLETE', 'ERROR', 'PENDING']) -> None:
        self._state = new_state

    def set_result(self, result: MeasureResult) -> None:
        self._result = result

    def set_device_temp(self, temp: float) -> None:
        self._device_temp = temp

    def set_iteration_number(self, iteration: int) -> None:
        self._iteration_number = iteration

    def set_default_name(self) -> None:
        """Genera un nombre por defecto basado en la fecha ISO 8601 si el usuario no especifica uno."""
        self._file_name = f"MED_{self._date.strftime('%Y%m%dT%H%M%S')}"