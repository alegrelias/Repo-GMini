from datetime import datetime
from typing import Optional

"""Entidad que representa el token de sesión activa de un usuario en el sistema"""
class Token:
    def __init__(self, user_id: int, token_string: str, created_at: Optional[datetime] = None):
        self._user_id: int = user_id
        self._token_string: str = token_string
        self._created_at: datetime = created_at if created_at else datetime.now()

    def get_user_id(self) -> int:
        return self._user_id

    def get_token_string(self) -> str:
        return self._token_string

    def get_created_at(self) -> datetime:
        return self._created_at