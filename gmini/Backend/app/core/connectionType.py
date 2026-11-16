from abc import ABC, abstractmethod
from typing import List
from gmini.Backend.app.core.observer import IObservable, IObserver

class ConnectionType(IObservable, ABC):
    def __init__(self):
        self._observers: List[IObserver] = []
        self.connection_state = None  # Aca va la instancia de ConnectionState (ej. DisconnectedState)

    def attach(self, observer: IObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: IObserver) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event_info: str = "") -> None:
        for observer in self._observers:
            observer.update(self, event_info)

    def get_state(self):
        return self.connection_state

    def set_state(self, new_state) -> None:
        self.connection_state = new_state
        self.notify(f"STATE_CHANGED")

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def send(self, data: str):
        pass

    @abstractmethod
    def receive(self) -> str:
        pass


class Wire(ConnectionType):
    def __init__(self, baudrate: int = 9600, port_name: str = "COM1", timeout: int = 1):
        super().__init__()
        self.baudrate = baudrate
        self.port_name = port_name
        self.timeout = timeout

    def connect(self):
        # Lógica de conexión por cable
        pass

    def disconnect(self):
        pass

    def send(self, data: str):
        pass

    def receive(self) -> str:
        return ""


class WireLess(ConnectionType):
    def __init__(self, protocol: str = "Bluetooth"):
        super().__init__()
        self.protocol = protocol

    def connect(self):
        # Lógica de conexión inalámbrica
        pass

    def disconnect(self):
        pass

    def send(self, data: str):
        pass

    def receive(self) -> str:
        return ""