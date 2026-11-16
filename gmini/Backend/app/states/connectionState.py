from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

# TYPE_CHECKING para evitar importaciones circulares cruzadas con ConnectionType
if TYPE_CHECKING:
    from gmini.Backend.app.core.connectionType import ConnectionType

class ConnectionState(ABC):
    @abstractmethod
    def connect(self, context: 'ConnectionType'):
        pass

    @abstractmethod
    def disconnect(self, context: 'ConnectionType'):
        pass

    @abstractmethod
    def send(self, context: 'ConnectionType', data: str):
        pass

    @abstractmethod
    def receive(self, context: 'ConnectionType') -> str:
        pass


class DisconnectedState(ConnectionState):
    def connect(self, context: 'ConnectionType'):
        # aca lógica real (ej. abrir puerto serie)
        # Si funca, va al nuevo estado:
        context.set_state(ConnectedState())

    def disconnect(self, context: 'ConnectionType'):
        # ya esta desconectado, no hace nada
        pass

    def send(self, context: 'ConnectionType', data: str):
        raise ConnectionError("No se puede enviar el comando: el dispositivo está desconectado.")

    def receive(self, context: 'ConnectionType') -> str:
        raise ConnectionError("No se puede recibir datos: el dispositivo está desconectado.")


class ConnectedState(ConnectionState):
    def connect(self, context: 'ConnectionType'):
        # Ya esta conectado, no hace nada
        pass

    def disconnect(self, context: 'ConnectionType'):
        # logica real para cerrar el puerto o socket
        context.set_state(DisconnectedState())

    def send(self, context: 'ConnectionType', data: str):
        # logica fisica para inyectar los bytes al hardware
        pass

    def receive(self, context: 'ConnectionType') -> str:
        # logica fisica para leer los bytes desde el hardware
        return ""


class ConnectionErrorState(ConnectionState):
    def connect(self, context: 'ConnectionType'):
        # Logica para intentar restablecer o reiniciar el enlace físico
        pass

    def disconnect(self, context: 'ConnectionType'):
        # Forzar el cierre y limpieza de buffers
        context.set_state(DisconnectedState())

    def send(self, context: 'ConnectionType', data: str):
        raise ConnectionError("Error en el enlace físico. No se pueden enviar comandos.")

    def receive(self, context: 'ConnectionType') -> str:
        raise ConnectionError("Error en el enlace físico. No se pueden leer datos.")