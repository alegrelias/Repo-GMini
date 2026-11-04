from typing import Optional
from app.states.deviceState import DeviceState, UncalibratedState

class Device:
    def __init__(self, device_id: int, device_name: str = "Guanaco Mini"):
        self.device_id: int = device_id
        self._device_name: str = device_name
        self._device_state: DeviceState = UncalibratedState()

    def get_id(self) -> int:
        return self.device_id

    def get_name(self) -> str:
        return self._device_name

    def get_state(self) -> DeviceState:
        return self._device_state

    def set_state(self, new_state: DeviceState) -> None:
        self._device_state = new_state

    def can_measure(self) -> bool:
        return self._device_state.can_measure()