from abc import ABC, abstractmethod

"""Interfaz para objetos que emiten notificaciones de cambio de estado """
class IObservable(ABC):
    @abstractmethod
    def attach(self, observer: 'IObserver') -> None:
        pass

    @abstractmethod
    def detach(self, observer: 'IObserver') -> None:
        pass

    @abstractmethod
    def notify(self, event_info: str = "") -> None:
        pass


class IObserver(ABC):
    @abstractmethod
    def update(self, observable: IObservable, event_info: str) -> None:
        pass