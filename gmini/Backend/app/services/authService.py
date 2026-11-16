import hashlib

class AuthService:
    def __init__(self, db_service):
        self.db = db_service

    
    def _hash_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    """Verifica las credenciales del usuario. Retorna un diccionario con los datos del usuario si es exitoso, o None si falla."""
    def login(self, username, password):
        hashed_pw = self._hash_password(password)
        user = self.db.get_user_by_username(username)
        
        #El orden devuelto por get_user_by_username es:(id, username, password, email)
        if user and user[2] == hashed_pw:
            return {"id": user[0], "username": user[1], "email": user[3]}
        return None

    """Registra un nuevo usuario si el nombre de usuario está disponible.Retorna True si fue exitoso, False si el usuario ya existe."""
    def register(self, username, password, email=""):
        if self.db.get_user_by_username(username):
            return False 
        
        hashed_pw = self._hash_password(password)
        return self.db.insert_user(username, hashed_pw, email)