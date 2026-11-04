from typing import Dict, List, Any
from app.core.observer import IObservable, IObserver
from app.models.device import Device
from app.states.deviceState import DeviceErrorState

"""Servicio encargado de gestionar los enlaces fisicos (puerto serial / bluetooth) con los dispositivos Guanaco Mini"""
class ConnectionService(IObservable, IObserver):
    def __init__(self):
        self.active_connections: Dict[int, Any] = {}
        self._observers: List[IObserver] = []

    def connect(self, device: Device, connection_type: Any) -> bool:
        try:
            connection_type.connect()
            if isinstance(connection_type, IObservable):
                connection_type.attach(self)
            self.active_connections[device.device_id] = connection_type
            self.notify("Conectado")
            return True
        except Exception as e:
            device.set_state(DeviceErrorState())
            self.notify(f"CONNECTION_ERROR: {e}")
            return False

    def disconnect(self, device: Device) -> None:
        conn = self.active_connections.pop(device.device_id, None)
        if conn:
            conn.disconnect()
            self.notify("Desconectado")

    def send(self, device: Device, command: str) -> None:
        conn = self.active_connections.get(device.device_id)
        if not conn:
            raise ConnectionError("El dispositivo no tiene una conexión activa.")
        conn.send(command)

    def receive(self, device: Device) -> str:
        conn = self.active_connections.get(device.device_id)
        if not conn:
            raise ConnectionError("El dispositivo no tiene una conexión activa.")
        return conn.receive()

    def update(self, observable: IObservable, event_info: str) -> None:
        self.notify(event_info)

    def attach(self, observer: IObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: IObserver) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event_info: str = "") -> None:
        for observer in self._observers:
            observer.update(self, event_info)