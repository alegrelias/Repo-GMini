import random
import json

class MockWire:
    def __init__(self):
        super().__init__()
        self.connected = False
        self.last_command = ""

    def connect(self):
        print("Mock: Simulando conexión exitosa al ESP32...")
        self.connected = True
        
    def disconnect(self):
        print("Mock: Simulando desconexión.")
        self.connected = False
        
    def send(self, data: str):
        print(f"Mock TX ---> Placa recibe: {data.strip()}")
        self.last_command = data
        
    def receive(self) -> str:
        # Simulamos el prompt por defecto de la placa Guanaco Mini
        response = "ad5933> " 
        
        if "singlefreq" in self.last_command:
            real_val = -15610 + random.randint(-500, 500)
            imag_val = -1335 + random.randint(-150, 150)
            response = f"{real_val} {imag_val}j\nad5933> "
            
        elif "sweep" in self.last_command:
            # Puntos base de una curva de Debye (Módulo y Fase / Real e Imag)
            base_magnitudes = [
                [185, -1830], 
                [634, -1717], 
                [1022, -1512], 
                [1348, -1222], 
                [1591, -861]
            ]
            
            # Le sumamos un ruido aleatorio de +/- 50 a cada coordenada de cada punto
            dynamic_magnitudes = [
                [
                    punto[0] + random.randint(-50, 50), 
                    punto[1] + random.randint(-50, 50)
                ] for punto in base_magnitudes
            ]
            
            # Construimos la respuesta respetando la estructura JSON de la placa
            sweep_data = {
                "sweep": {
                    "result": {
                        "magnitude": dynamic_magnitudes,
                        "frequency": [10000, 30000, 50000, 70000, 90000]
                    }
                }
            }
            
            # Convertimos el diccionario a string JSON y anexamos el prompt
            response = json.dumps(sweep_data) + "\nad5933> "
            
        elif "calibrate" in self.last_command:
            # Asumimos que la calibración no devuelve JSON, solo el prompt si hay éxito
            response = "ad5933> " 
            
        print(f"Mock RX <--- Placa responde: {response.strip()}")
        return response