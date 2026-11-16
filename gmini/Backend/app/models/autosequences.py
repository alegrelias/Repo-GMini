from typing import List
from gmini.Backend.app.models.measureSetup import MeasureSetup

class AutoSequence:
    def __init__(self, name: str = "Nueva Autosecuencia"):
        self._sequence_id = None
        self._name = name
        self._measure_setups: List[MeasureSetup] = []
        self._delay: float = 0.0
        self._repeat: int = 1
        self._observations: str = ""

    # Getters y setters requeridos por el diagrama y la lógica
    def get_id(self) -> int:
        return self._sequence_id

    def set_id(self, seq_id: int):
        self._sequence_id = seq_id

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str):
        self._name = name

    def get_setups(self) -> List[MeasureSetup]:
        return self._measure_setups

    def add_setup(self, setup: MeasureSetup):
        self._measure_setups.append(setup)

    def get_delay(self) -> float:
        return self._delay

    def set_delay(self, delay: float):
        self._delay = delay

    def get_repeat(self) -> int:
        return self._repeat

    def set_repeat(self, repeat: int):
        self._repeat = repeat

    def get_observations(self) -> str:
        return self._observations

    def set_observations(self, obs: str):
        self._observations = obs