import sys
from PyQt6.QtWidgets import QApplication
from gmini.Backend.app.services.sessionManager import SessionManager
from gmini.Backend.app.db.databaseService import DataBaseService

# Importa tu ventana inicial. Ajusta la ruta exacta según cómo llamaste a la clase en login_window.py
from gmini.Frontend.login_register.login_window import Login 

# Aquí puedes importar servicios globales que deban arrancar con la app
from gmini.Backend.app.db.databaseService import DataBaseService
from gmini.Backend.app.services.sessionManager import SessionManager

def main():
    # 1. Inicializar la aplicación base de Qt (Obligatorio en PyQt6)
    app = QApplication(sys.argv)
    
    # 2. Inicializar servicios base (Opcional, pero recomendado según tu arquitectura)
    # db_service = DataBaseService()
    # session_manager = SessionManager() # Singleton
    
    # 3. Instanciar y mostrar la primera ventana del flujo (Login)
    login_window = Login()
    login_window.show()
    
    # 4. Iniciar el bucle de eventos para que la ventana no se cierre de inmediato
    sys.exit(app.exec())

if __name__ == '__main__':
    main()