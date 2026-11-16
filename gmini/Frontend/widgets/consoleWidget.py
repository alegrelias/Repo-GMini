from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QHBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QTimer

# Importamos las interfaces y estados de tu propia arquitectura
from gmini.Backend.app.core.observer import IObserver, IObservable
from gmini.Backend.app.states.deviceState import MeasuringState
from gmini.Backend.app.models.device import Device
from gmini.Backend.app.services.connectionService import ConnectionService

class ConsoleWidget(QWidget, IObserver):
    def __init__(self, connection_service: ConnectionService, device: Device, parent=None):
        super().__init__(parent)
        self.connection_service = connection_service
        self.device = device
        self.setup_ui()
        self.check_device_state()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # area de historial (lectura)
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setFont(QFont("Courier", 10))
        # Ajusta colores al tema oscuro
        self.output_area.setStyleSheet("background-color: #1e1e2e; color: #cdd6f4; border: 1px solid #45475a;")
        
        # Entrada de comandos
        self.input_layout = QHBoxLayout()
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Ingrese comando crudo (ej. about, temperature)...")
        self.input_line.setStyleSheet("background-color: #45475a; color: #cdd6f4;")
        
        self.send_button = QPushButton("Enviar")
        self.send_button.setFixedWidth(80)
        self.send_button.setStyleSheet("background-color: #313244; color: white;")
        
        self.input_layout.addWidget(self.input_line)
        self.input_layout.addWidget(self.send_button)
        
        self.layout.addWidget(self.output_area)
        self.layout.addLayout(self.input_layout)
        
        # Eventos UI
        self.send_button.clicked.connect(self.handle_send_command)
        self.input_line.returnPressed.connect(self.handle_send_command)

    def handle_send_command(self):
        command = self.input_line.text().strip()
        if not command:
            return
            
        # Reflejar el comando enviado (Color azul claro)
        self.output_area.append(f"<span style='color: #89b4fa;'>&gt; {command}</span>")
        self.input_line.clear()
        
        # Bloquear preventivamente para evitar spam de clics
        self.input_line.setEnabled(False)
        self.send_button.setEnabled(False)
        
        try:
            response = self.connection_service.send_console_command(self.device, command)
            if response:
                # Reemplaza \n por <br> para que QTextEdit respete los saltos de linea del hardware
                formatted_response = response.replace('\n', '<br>')
                self.output_area.append(f"<span style='color: #a6adc8;'>{formatted_response}</span>")
            else:
                self.output_area.append("<span style='color: #7f849c;'><i>(Sin respuesta / Timeout)</i></span>")
        except Exception as e:
            # Color rojo para errores
            self.output_area.append(f"<span style='color: #f38ba8;'><b>Error:</b> {str(e)}</span>")
        finally:
            self.check_device_state()
            
        # Forzar el scroll hacia la ultima línea
        scrollbar = self.output_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def update(self, observable: IObservable, event_info: str) -> None:
        """
        Implementación de IObserver. Reacciona a los eventos del MeasureService y ConnectionService.
        """
        # QTimer asegura que la UI se actualice en el hilo principal
        QTimer.singleShot(0, self.check_device_state)

    def check_device_state(self):
        """
        Verifica el estado del hardware inyectado y bloquea la interfaz si está operando.
        """
        current_state = self.device.get_state() if hasattr(self.device, 'get_state') else None
        
        # Valida contra la clase de estado real (Patrón State)
        if isinstance(current_state, MeasuringState):
            self.input_line.setEnabled(False)
            self.send_button.setEnabled(False)
            self.input_line.setPlaceholderText("Hardware ocupado...")
        else:
            self.input_line.setEnabled(True)
            self.send_button.setEnabled(True)
            self.input_line.setPlaceholderText("Ingrese comando crudo (ej. about, temperature)...")