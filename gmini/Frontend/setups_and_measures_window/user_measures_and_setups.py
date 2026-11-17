import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class UserMeasuresAndSetups(QWidget):
    def __init__(self):
        super().__init__()
        self.inicializar_ui()

    def inicializar_ui(self):
        self.setWindowTitle("GMini GUI - Historial y Setups")
        self.resize(900, 550)
        
        # Fondo unificado exacto (#1e2229) con el Main
        self.setStyleSheet("""
            QWidget {
                background-color: #1e2229;
                color: #ffffff;
                font-family: Arial, sans-serif;
            }
            QTabWidget::pane {
                border: 1px solid #4f5b66;
                background-color: #1e2229;
                border-radius: 6px;
            }
            QTabBar::tab {
                background-color: #282c34;
                color: #ffffff;
                padding: 10px 20px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #2f5275;
                font-weight: bold;
            }
            QTableWidget {
                background-color: #21252b;
                alternate-background-color: #282c34;
                color: #ffffff;
                gridline-color: #4f5b66;
                border: 1px solid #4f5b66;
                border-radius: 4px;
            }
            QHeaderView::section {
                background-color: #282c34;
                color: #ffffff;
                padding: 6px;
                border: 1px solid #4f5b66;
                font-weight: bold;
            }
            QPushButton {
                background-color: #3b4252;
                border: 1px solid #4f5b66;
                border-radius: 6px;
                padding: 5px 10px;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #434c5e;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Encabezado superior con título y LEAB
        top_layout = QHBoxLayout()
        title_label = QLabel("GMini GUI")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #D8DEE9;")
        
        self.label_leab = QLabel("LEAB")
        self.label_leab.setMinimumWidth(70)
        self.label_leab.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.label_leab.setStyleSheet("font-size: 20px; font-weight: bold; color: #D8DEE9;")

        top_layout.addWidget(title_label)
        top_layout.addStretch()
        top_layout.addWidget(self.label_leab)
        main_layout.addLayout(top_layout)

        # Pestañas de Historial (Mediciones, Setup Calibraciones, Setup Mediciones)
        self.tabs = QTabWidget()
        
        self.tab_mediciones = self.crear_tabla_mediciones()
        self.tab_setup_calibraciones = self.crear_tabla_calibraciones()
        self.tab_setup_mediciones = self.crear_tabla_setups_medicion()

        self.tabs.addTab(self.tab_mediciones, "Mediciones")
        self.tabs.addTab(self.tab_setup_calibraciones, "Setup Calibraciones")
        self.tabs.addTab(self.tab_setup_mediciones, "Setup Mediciones")

        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)
        self.show()

    def crear_tabla_mediciones(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Nombre / Descripción", "Fecha de creación", "Estado", "Acciones"])
        
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

        mock_mediciones = [
            {"nombre": "Medición #145 - Espectroscopia de prueba", "fecha": "08/10/2026 14:15", "estado": "Completado"},
            {"nombre": "Medición #144 - Muestra A", "fecha": "07/10/2026 18:30", "estado": "Completado"},
            {"nombre": "Medición #143 - Muestra B", "fecha": "07/10/2026 09:32", "estado": "Guardado"},
            {"nombre": "Medición #142 - Espectroscopia de calibración", "fecha": "06/10/2026 16:48", "estado": "Completado"},
            {"nombre": "Medición #141 - Muestra C", "fecha": "05/10/2026 12:10", "estado": "Completado"},
            {"nombre": "Medición #140 - Espectroscopia de prueba 2", "fecha": "05/10/2026 10:15", "estado": "Guardado"},
            {"nombre": "Medición #139 - Análisis de ruido", "fecha": "04/10/2026 15:44", "estado": "Completado"},
            {"nombre": "Medición #138 - Muestra D", "fecha": "03/10/2026 11:20", "estado": "Guardado"}
        ]

        table.setRowCount(len(mock_mediciones))
        for row_idx, item in enumerate(mock_mediciones):
            table.setItem(row_idx, 0, QTableWidgetItem(item["nombre"]))
            table.setItem(row_idx, 1, QTableWidgetItem(item["fecha"]))
            table.setItem(row_idx, 2, QTableWidgetItem(item["estado"]))
            
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setContentsMargins(4, 2, 4, 2)
            
            btn_load = QPushButton("📁")
            btn_load.setToolTip("Cargar al Workspace")
            btn_delete = QPushButton("🗑")
            btn_delete.setToolTip("Eliminar registro")
            
            btn_layout.addWidget(btn_load)
            btn_layout.addWidget(btn_delete)
            btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            table.setCellWidget(row_idx, 3, btn_widget)

        layout.addWidget(table)
        return widget

    def crear_tabla_calibraciones(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Configuración Calibración", "Fecha", "Canal / Z_Cal", "Estado"])
        
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        
        mock_calibs = [
            {"nombre": "Calibración R_CAL_1 (470 Ω)", "fecha": "08/10/2026 10:00", "canal": "R_CAL_1", "estado": "Activo"},
            {"nombre": "Calibración R_CAL_2 (1 kΩ)", "fecha": "01/10/2026 09:15", "canal": "R_CAL_2", "estado": "Guardado"},
        ]

        table.setRowCount(len(mock_calibs))
        for row_idx, item in enumerate(mock_calibs):
            table.setItem(row_idx, 0, QTableWidgetItem(item["nombre"]))
            table.setItem(row_idx, 1, QTableWidgetItem(item["fecha"]))
            table.setItem(row_idx, 2, QTableWidgetItem(item["canal"]))
            table.setItem(row_idx, 3, QTableWidgetItem(item["estado"]))

        layout.addWidget(table)
        return widget

    def crear_tabla_setups_medicion(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Nombre Setup", "Tipo", "Parámetros Principales", "Fecha"])
        
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

        mock_setups = [
            {"nombre": "Setup Espectroscopia Estándar", "tipo": "Espectroscopia", "params": "100Hz - 50kHz (Steps: 5)", "fecha": "07/10/2026"},
            {"nombre": "Setup Monofrecuencia 1kHz", "tipo": "Monofrecuencia", "params": "Freq: 1000 Hz, Delay: 1s", "fecha": "05/10/2026"},
        ]

        table.setRowCount(len(mock_setups))
        for row_idx, item in enumerate(mock_setups):
            table.setItem(row_idx, 0, QTableWidgetItem(item["nombre"]))
            table.setItem(row_idx, 1, QTableWidgetItem(item["tipo"]))
            table.setItem(row_idx, 2, QTableWidgetItem(item["params"]))
            table.setItem(row_idx, 3, QTableWidgetItem(item["fecha"]))

        layout.addWidget(table)
        return widget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UserMeasuresAndSetups()
    sys.exit(app.exec())