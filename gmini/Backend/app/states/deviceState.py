from abc import ABC, abstractmethod

"""Determina si el hardware esta en condiciones de iniciar una nueva medicionbasado en su estado actual"""
class DeviceState(ABC):
    @abstractmethod
    def can_measure(self) -> bool:
        pass

class UncalibratedState(DeviceState):
    def can_measure(self) -> bool:
        return False

class CalibratedState(DeviceState):
    def can_measure(self) -> bool:
        return True

class FreeDeviceState(DeviceState):
    def can_measure(self) -> bool:
        return False

class MeasuringState(DeviceState):
    def can_measure(self) -> bool:
        return False

class DeviceErrorState(DeviceState):
    def can_measure(self) -> bool:
        return False