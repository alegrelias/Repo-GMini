import pyqtgraph as pg

class AnalyticsService:
    def plot_debye(self, result_data: list, plot_widget: pg.PlotWidget):
        """
        Recibe una lista de magnitudes [[Real, Imag], [Real, Imag]...]
        y grafica un diagrama de Nyquist/Debye (Real vs -Imag) en kOhms.
        """
        # Extraer X (Real) e Y (-Imaginario) y convertir a kOhms dividiendo por 1000
        real_values = [punto[0] / 1000.0 for punto in result_data]
        imag_values = [-punto[1] / 1000.0 for punto in result_data] # Invertimos el signo para Debye
        
        # Limpiar gráfico anterior y configurar estilo
        plot_widget.clear()
        plot_widget.setLabel('left', '-Imaginario', units='kΩ') # Unidad actualizada
        plot_widget.setLabel('bottom', 'Real', units='kΩ')      # Unidad actualizada
        plot_widget.setTitle("Gráfico de Debye (Nyquist)")
        plot_widget.showGrid(x=True, y=True)
        
        # Graficar con puntos
        plot_widget.plot(real_values, imag_values, pen='c', symbol='o', symbolBrush='b')