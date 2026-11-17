from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QTextEdit, QDialogButtonBox, QLabel
from PyQt6.QtCore import Qt

class NewSessionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Crear Nueva Sesión Experimental")
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: #1e1e2e; color: #cdd6f4; font-size: 14px;")
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Etiqueta de título
        lbl_title = QLabel("Definir Parámetros de la Sesión")
        lbl_title.setStyleSheet("font-weight: bold; font-size: 16px; color: #89b4fa;")
        
        # Campo para el nombre
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre de la sesión (ej. Campaña Músculo Porcino)")
        self.name_input.setStyleSheet("background-color: #45475a; border: 1px solid #5a6b7d; border-radius: 5px; padding: 5px;")
        
        # Campo para las observaciones
        self.obs_input = QTextEdit()
        self.obs_input.setPlaceholderText("Observaciones o notas del experimento (opcional)...")
        self.obs_input.setStyleSheet("background-color: #45475a; border: 1px solid #5a6b7d; border-radius: 5px; padding: 5px;")
        
        # Botones de Aceptar y Cancelar
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.setStyleSheet("""
            QPushButton {
                background-color: #313244; 
                border: 1px solid #5a6b7d; 
                border-radius: 5px; 
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #45475a;
            }
        """)
        
        # Conectar botones a las acciones nativas del QDialog
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        
        # Ensamblar el layout
        layout.addWidget(lbl_title)
        layout.addWidget(self.name_input)
        layout.addWidget(self.obs_input)
        layout.addStretch()
        layout.addWidget(self.button_box)

    def get_data(self):
        """Retorna una tupla con (nombre, observaciones) limpios de espacios extra."""
        return self.name_input.text().strip(), self.obs_input.toPlainText().strip()