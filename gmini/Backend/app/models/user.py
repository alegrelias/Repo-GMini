from typing import Optional

class User:
    def __init__(
        self, 
        user_name: str, 
        email: str = "", 
        password: str = "", 
        root_directory: Optional[str] = None,
        user_id: Optional[int] = None
    ):
        #Atributos privados 
        self._user_id: Optional[int] = user_id
        self._user_name: str = user_name
        self._email: str = email
        self._password: str = password
        self._root_directory: Optional[str] = root_directory

    # Getters y setters
    def get_id(self) -> Optional[int]:
        return self._user_id

    def get_root_directory(self) -> Optional[str]:
        return self._root_directory

    def get_user_name(self) -> str:
        return self._user_name

    def get_email(self) -> str:
        return self._email

    def get_password(self) -> str:
        return self._password

    def set_user_id(self, id: int) -> None:
        self._user_id = id

    def set_root_directory(self, path: Optional[str]) -> None:
        self._root_directory = path

    def set_user_name(self, user_name: str) -> None:
        self._user_name = user_name

    def set_email(self, email: str) -> None:
        self._email = email

    def set_password(self, password: str) -> None:
        self._password = password

    def __repr__(self) -> str:
        return f"User(id={self._user_id}, user_name='{self._user_name}', email='{self._email}')"