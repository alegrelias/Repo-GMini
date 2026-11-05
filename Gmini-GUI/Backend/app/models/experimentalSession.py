from datetime import datetime
from typing import List, Optional
from app.models.measure import Measure


class ExperimentalSession:
    """
    Entidad que agrupa un conjunto de mediciones realizadas durante una campaña
    o sesión experimental de laboratorio.
    """
    def __init__(self, user_id: int, name: str = "", observations: str = ""):
        self._session_id: Optional[int] = None
        self._user_id: int = user_id
        self._date: datetime = datetime.now()
        self._name: str = name if name else f"Sesion_{self._date.strftime('%Y%m%dT%H%M%S')}"
        self._observations: str = observations
        self._measures: List[Measure] = []

    def add_measure(self, measure: Measure) -> None:
        if measure not in self._measures:
            self._measures.append(measure)
            if self._session_id is not None:
                measure._experimental_session_id = self._session_id

    def get_measures(self) -> List[Measure]:
        return self._measures

    def get_id(self) -> Optional[int]:
        return self._session_id

    def get_user_id(self) -> int:
        return self._user_id

    def get_name(self) -> str:
        return self._name

    def get_date(self) -> datetime:
        return self._date

    def get_observations(self) -> str:
        return self._observations

    def set_id(self, session_id: int) -> None:
        self._session_id = session_id
        for m in self._measures:
            m._experimental_session_id = session_id

    def set_name(self, new_name: str) -> None:
        self._name = new_name

    def set_observations(self, obs: str) -> None:
        self._observations = obs