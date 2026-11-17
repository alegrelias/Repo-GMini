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
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
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
        title_label = QLabel("GMini GUI - Historial de Mediciones")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #D8DEE9;")
        
        self.label_leab = QLabel("LEAB")
        self.label_leab.setMinimumWidth(70)
        self.label_leab.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.label_leab.setStyleSheet("font-size: 20px; font-weight: bold; color: #D8DEE9;")

        top_layout.addWidget(title_label)
        top_layout.addStretch()
        top_layout.addWidget(self.label_leab)
        main_layout.addLayout(top_layout)

        # Pestañas de Historial
        self.tabs = QTabWidget()
        
        self.tab_mediciones = self.crear_tabla_mediciones()
        self.tab_setup_calibraciones = self.crear_tabla_calibraciones()
        self.tab_setup_mediciones = self.crear_tabla_setups_medicion()

        self.tabs.addTab(self.tab_mediciones, "Mediciones Realizadas")
        self.tabs.addTab(self.tab_setup_calibraciones, "Setup Calibraciones")
        self.tabs.addTab(self.tab_setup_mediciones, "Setup Mediciones")

        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)
        self.show()

    def crear_tabla_mediciones(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.table_mediciones = QTableWidget()
        self.table_mediciones.setColumnCount(4)
        self.table_mediciones.setHorizontalHeaderLabels(["Nombre / Descripción", "Fecha de ejecución", "Estado", "Acciones"])
        
        header = self.table_mediciones.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

        self.cargar_datos_mediciones()

        layout.addWidget(self.table_mediciones)
        return widget

    def cargar_datos_mediciones(self):
        """Recupera las mediciones guardadas desde la lista temporal o la actual de la MainWindow"""
        mediciones_guardadas = []
        if self.main_window:
            # Consultamos directamente la lista temporal de respaldo de la MainWindow
            if hasattr(self.main_window, "temp_measures_list"):
                mediciones_guardadas = self.main_window.temp_measures_list
            
            # Si está vacía pero hay una medición actual, la añadimos
            if not mediciones_guardadas and getattr(self.main_window, "current_measure", None):
                mediciones_guardadas = [self.main_window.current_measure]

        self.table_mediciones.setRowCount(len(mediciones_guardadas))
        
        if not mediciones_guardadas:
            return

        for row_idx, medida in enumerate(mediciones_guardadas):
            nombre = f"Medición #{row_idx + 1} - Ejecutada con Mock"
            fecha = "Sesión actual"
            estado = "Completado"

            self.table_mediciones.setItem(row_idx, 0, QTableWidgetItem(nombre))
            self.table_mediciones.setItem(row_idx, 1, QTableWidgetItem(fecha))
            self.table_mediciones.setItem(row_idx, 2, QTableWidgetItem(estado))
            
            # Botones de acción funcional por fila (Abrir / Borrar)
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setContentsMargins(4, 2, 4, 2)
            
            btn_load = QPushButton("📁")
            btn_load.setToolTip("Abrir y ver gráfico en el Main")
            btn_load.clicked.connect(lambda checked, m=medida: self.abrir_medicion_en_main(m))
            
            btn_delete = QPushButton("🗑")
            btn_delete.setToolTip("Eliminar medición")
            btn_delete.clicked.connect(lambda checked, idx=row_idx, m=medida: self.eliminar_medicion(idx, m))
            
            btn_layout.addWidget(btn_load)
            btn_layout.addWidget(btn_delete)
            btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.table_mediciones.setCellWidget(row_idx, 3, btn_widget)

    def abrir_medicion_en_main(self, medida):
        """Carga la medición seleccionada de vuelta en la MainWindow y plotea su gráfico"""
        if self.main_window:
            self.main_window.current_measure = medida
            resultado = medida.get_measure_result()
            if resultado:
                resultado_real = resultado.get_impedances()
                self.main_window.results_tabs.show()
                self.main_window.analytics_service.plot_debye(resultado_real, self.main_window.plot_widget)
                self.main_window._actualizar_tabla_datos(resultado_real)
                self.main_window._show_status("Medición del historial cargada correctamente.")
                self.close()

    def eliminar_medicion(self, row_idx, medida):
        """Borra la medición de la lista de respaldo y actualiza la tabla"""
        if self.main_window and hasattr(self.main_window, "temp_measures_list"):
            try:
                self.main_window.temp_measures_list.remove(medida)
            except ValueError:
                pass
            if getattr(self.main_window, "current_measure", None) == medida:
                self.main_window.current_measure = None
                
        self.table_mediciones.removeRow(row_idx)

    def crear_tabla_calibraciones(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Configuración Calibración", "Canal", "Estado"])
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(table)
        return widget

    def crear_tabla_setups_medicion(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Nombre Setup", "Tipo", "Parámetros"])
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(table)
        return widget