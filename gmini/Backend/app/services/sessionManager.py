from typing import List, Optional
from gmini.Backend.app.core.observer import IObservable, IObserver
from gmini.Backend.app.models.user import User
from gmini.Backend.app.models.token import Token


class SessionManager(IObservable):
    _instance: Optional['SessionManager'] = None
    _current_user: Optional[User]
    _active_token: Optional[Token]
    _observers: List[IObserver]

    def __new__(cls) -> 'SessionManager':
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
            cls._instance._current_user = None
            cls._instance._active_token = None
            cls._instance._observers = []
        return cls._instance

    #Getters y setters
    def get_current_user(self) -> Optional[User]:
        return self._current_user

    def set_current_user(self, user: Optional[User]) -> None:
        self._current_user = user
        self.notify("USER_CHANGED")

    def get_active_token(self) -> Optional[Token]:
        return self._active_token

    def set_active_token(self, token: Optional[Token]) -> None:
        self._active_token = token

    def clear_session(self) -> None:
        """Limpia los datos al cerrar sesión (logout)."""
        self._current_user = None
        self._active_token = None
        self.notify("SESSION_CLOSED")

    # --- Patrón Observer ---
    def attach(self, observer: IObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: IObserver) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event_info: str = "") -> None:
        for observer in self._observers:
            observer.update(self, event_info)