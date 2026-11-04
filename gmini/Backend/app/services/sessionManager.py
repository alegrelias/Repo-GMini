from typing import List, Optional
from app.core.observer import IObservable, IObserver
from app.models.user import User
from app.models.token import Token

"""Notifica a la GUI cuando cambia el usuario"""
class SessionManager(IObservable):
    _instance: Optional['SessionManager'] = None

    def __new__(cls) -> 'SessionManager':
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
            cls._instance._current_user: Optional[User] = None
            cls._instance._advanced_mode_active: bool = False
            cls._instance._active_token: Optional[Token] = None
            cls._instance._observers: List[IObserver] = []
        return cls._instance

    # --- Getters y Setters ---
    def get_current_user(self) -> Optional[User]:
        return self._current_user

    def set_current_user(self, user: Optional[User]) -> None:
        self._current_user = user
        self.notify("USER_CHANGED")

    def get_active_mode(self) -> bool:
        return self._advanced_mode_active

    def set_active_mode(self, mode: bool) -> None:
        self._advanced_mode_active = mode
        self.notify("MODE_CHANGED")

    def switch_user_mode(self) -> None:
        """Alterna entre Modo Basico (False) y Modo experto (True)"""
        self._advanced_mode_active = not self._advanced_mode_active
        self.notify("MODE_CHANGED")

    def get_active_token(self) -> Optional[Token]:
        return self._active_token

    def set_active_token(self, token: Optional[Token]) -> None:
        self._active_token = token

    #Patron Observer
    def attach(self, observer: IObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: IObserver) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event_info: str = "") -> None:
        for observer in self._observers:
            observer.update(self, event_info)