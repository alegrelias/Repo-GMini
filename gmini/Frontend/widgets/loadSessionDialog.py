from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QListWidget, QListWidgetItem, 
    QDialogButtonBox, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt
from gmini.Backend.app.models.experimentalSession import ExperimentalSession

class LoadSessionDialog(QDialog):
    def __init__(self, db_service, user_id, parent=None):
        super().__init__(parent)
        self.db_service = db_service
        self.user_id = user_id
        self.selected_session = None
        
        self.setWindowTitle("Cargar Sesión Experimental")
        self.setFixedSize(500, 400)
        self.setStyleSheet("background-color: #1e1e2e; color: #cdd6f4; font-size: 14px;")
        
        self.setup_ui()
        self.load_sessions_from_db()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        lbl_title = QLabel("Seleccione una sesión para cargar:")
        lbl_title.setStyleSheet("font-weight: bold; font-size: 16px; color: #89b4fa;")
        
        self.session_list = QListWidget()
        self.session_list.setStyleSheet("""
            QListWidget {
                background-color: #313244;
                border: 1px solid #45475a;
                border-radius: 5px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #45475a;
            }
            QListWidget::item:selected {
                background-color: #45475a;
                color: #a6e3a1;
            }
        """)
        self.session_list.itemDoubleClicked.connect(self.accept_selection)
        
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
        self.button_box.accepted.connect(self.accept_selection)
        self.button_box.rejected.connect(self.reject)
        
        layout.addWidget(lbl_title)
        layout.addWidget(self.session_list)
        layout.addWidget(self.button_box)

    def load_sessions_from_db(self):
        """Consulta la BD y puebla la lista visual."""
        try:
            sessions = self.db_service.get_sessions_by_user(self.user_id)
            
            if not sessions:
                item = QListWidgetItem("No se encontraron sesiones guardadas.")
                item.setFlags(Qt.ItemFlag.NoItemFlags) # No seleccionable
                self.session_list.addItem(item)
                self.button_box.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)
                return

            for session in sessions:
                # Formateamos la información visual
                date_str = session.get_date().strftime("%Y-%m-%d %H:%M") if hasattr(session.get_date(), 'strftime') else session.get_date()
                display_text = f"[{date_str}] {session.get_name()}"
                
                item = QListWidgetItem(display_text)
                # Almacenamos el objeto de sesión dentro del item visual para recuperarlo fácilmente
                item.setData(Qt.ItemDataRole.UserRole, session)
                self.session_list.addItem(item)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fallo al cargar sesiones desde la BD:\n{str(e)}")

    def accept_selection(self):
        """Se ejecuta al presionar Ok o hacer doble clic en un ítem."""
        current_item = self.session_list.currentItem()
        if current_item and current_item.flags() & Qt.ItemFlag.ItemIsSelectable:
            # Recuperamos el objeto de sesión almacenado en el ítem
            self.selected_session = current_item.data(Qt.ItemDataRole.UserRole)
            self.accept()
        else:
            QMessageBox.warning(self, "Atención", "Debe seleccionar una sesión válida.")

    def get_selected_session(self) -> ExperimentalSession:
        return self.selected_session