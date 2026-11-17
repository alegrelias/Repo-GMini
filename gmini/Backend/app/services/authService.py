import hashlib
import secrets
from datetime import datetime
from typing import Optional

from app.models.user import User
from app.models.token import Token
from app.db.databaseService import DataBaseService
from app.services.sessionManager import SessionManager
from app.services.localServices import LocalService


class AuthService:
    """
    Servicio de autenticación y gestión de sesiones de usuario (Subsistema 3).
    Conecta la interfaz de Login/Registro con DataBaseService, SessionManager y LocalService.
    """
    def __init__(self,
                 db_service: Optional[DataBaseService] = None,
                 session_manager: Optional[SessionManager] = None,
                 local_service: Optional[LocalService] = None,
                 user_token_file_path: str = "./session_token.json"):
        self.user_token_file_path: str = user_token_file_path
        self._db_service: DataBaseService = db_service or DataBaseService()
        self._session_manager: SessionManager = session_manager or SessionManager()
        self._local_service: LocalService = local_service or LocalService()
        self._current_checked_user: Optional[User] = None

    def register(self, user_name: str, email: str, password: str) -> bool:
        """
        Caso de Uso: Crear Perfil de Usuario (SET-02, SET-03).
        Valida que el usuario y email no existan, hashea la contraseña y persiste en BD.
        """
        clean_user = user_name.strip()
        clean_email = email.strip()

        if not clean_user or not clean_email or not password:
            return False

        if self._db_service.get_user_by_name(clean_user) is not None:
            return False
        if self._db_service.get_user_by_email(clean_email) is not None:
            return False

        hashed_password = self._rehash_password(password)

        try:
            new_user = User(clean_user, clean_email, hashed_password, None)
        except TypeError:
            new_user = User(None, clean_user)
            new_user._email = clean_email
            new_user._password = hashed_password

        return bool(self._db_service.save_user(new_user))

    def login(self, user_name: str, password: str) -> Optional[Token]:
        """
        Caso de Uso: Iniciar Sesión (SET-04).
        Verifica credenciales en BD local, asigna el usuario en SessionManager y guarda el Token.
        """
        clean_user = user_name.strip()
        if not clean_user or not password:
            return None

        user = self._db_service.get_user_by_name(clean_user)
        if user is None:
            return None

        self._current_checked_user = user
        if not self.verify_password(password):
            return None

        self._session_manager.set_current_user(user)
        token_string = self.generate_token()
        user_id = user.get_id() if hasattr(user, "get_id") else getattr(user, "_user_id", 1)

        token = Token(user_id=user_id, token_string=token_string, created_at=datetime.now())
        self._session_manager.set_active_token(token)

        if hasattr(self._local_service, "export_user_token"):
            self._local_service.export_user_token(self.user_token_file_path, token)

        return token

    def logout(self) -> bool:
        """
        Caso de Uso: Cerrar Sesión (SET-05).
        Elimina el token persistido y limpia el SessionManager.
        """
        if hasattr(self._local_service, "delete_token"):
            try:
                self._local_service.delete_token(self.user_token_file_path)
            except TypeError:
                self._local_service.delete_token()

        self._session_manager.set_active_token(None)
        self._session_manager.set_current_user(None)
        return True

    def restore_session(self, token_str: Optional[str] = None) -> bool:
        """
        Caso de Uso: Inicializar entorno de trabajo (SET-01, SET-15).
        Recupera la sesión activa si existe un token válido guardado localmente.
        """
        if not hasattr(self._local_service, "load_user_token"):
            return False

        token_obj = self._local_service.load_user_token(self.user_token_file_path)
        if token_obj is None:
            return False

        if token_str and token_obj.get_token_string() != token_str:
            return False

        user = self._db_service.get_user_by_id(token_obj.get_user_id())
        if user is None:
            return False

        self._session_manager.set_current_user(user)
        self._session_manager.set_active_token(token_obj)
        return True

    def verify_password(self, password: str) -> bool:
        if self._current_checked_user is None:
            return False
        stored_pw = getattr(
            self._current_checked_user, "_password",
            getattr(self._current_checked_user, "password", "")
        )
        hashed_input = self._rehash_password(password)
        return stored_pw == hashed_input or stored_pw == password

    def generate_token(self) -> str:
        return secrets.token_hex(32)

    def _rehash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()