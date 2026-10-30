from typing import Optional

#almacena los parametros de la calibracion electronica del equipo.
class CalibrationSetup:
    def __init__(self, channel: str, z_calc_value_real: float, z_calc_value_imag: float):
        self._cal_setup_id: Optional[int] = None
        self._observations: str = ""
        self._channel: str = channel 
        self._z_calc_value_real: float = z_calc_value_real
        self._z_calc_value_imag: float = z_calc_value_imag

    #getters y seters
    def get_id(self) -> Optional[int]:
        return self._cal_setup_id

    def get_channel(self) -> str:
        return self._channel

    def get_z_calc_value_real(self) -> float:
        return self._z_calc_value_real

    def get_z_calc_value_imag(self) -> float:
        return self._z_calc_value_imag

    def get_observations(self) -> str:
        return self._observations

    def set_id(self, setup_id: int) -> None:
        self._cal_setup_id = setup_id

    def set_observations(self, obs: str) -> None:
        self._observations = obs