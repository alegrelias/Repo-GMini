from typing import Optional, List

#almacena los parametros de la calibracion electronica del equipo, incluyendo la configuración analógica base
class CalibrationSetup:
    def __init__(self, channel: str, z_calc_value_real: float, z_calc_value_imag: float,
                 exitation_voltage: float, gain: float, rfbvalue: float, 
                 settcycles: int, mux_channel: List[int]):
        self._cal_setup_id: Optional[int] = None
        self._observations: str = ""
        self._channel: str = channel 
        self._z_calc_value_real: float = z_calc_value_real
        self._z_calc_value_imag: float = z_calc_value_imag
        self._exitation_voltage: float = exitation_voltage
        self._gain: float = gain
        self._rfbvalue: float = rfbvalue
        self._settcycles: int = settcycles
        self._mux_channel: List[int] = mux_channel

    #geters y seters
    def get_id(self) -> Optional[int]: return self._cal_setup_id
    def get_channel(self) -> str: return self._channel
    def get_z_calc_value_real(self) -> float: return self._z_calc_value_real
    def get_z_calc_value_imag(self) -> float: return self._z_calc_value_imag
    def get_observations(self) -> str: return self._observations
    def get_exitation_voltage(self) -> float: return self._exitation_voltage
    def get_gain(self) -> float: return self._gain
    def get_rfbvalue(self) -> float: return self._rfbvalue
    def get_settcycles(self) -> int: return self._settcycles
    def get_mux_channel(self) -> List[int]: return self._mux_channel

    def set_id(self, setup_id: int) -> None:
        self._cal_setup_id = setup_id

    def set_observations(self, obs: str) -> None:
        self._observations = obs