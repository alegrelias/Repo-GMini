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
        
        cmd = self.last_command.lower().strip()
        
        # --- NUEVOS COMANDOS DE DIAGNÓSTICO (CONSOLA) ---
        if cmd == "about":
            response = '{"name":"AD5933-GUANACO-MINI","date":"Aug 31 2026","version":"2.0"}\nad5933> '
            
        elif cmd == "temperature":
            # Simulamos el sensor de temperatura interno (ej. 24°C)
            response = '24\nad5933> '
            
        elif cmd == "help" or cmd == "?":
            response = 'Lista de comandos:\nabout\ntemperature\nreset\nsweep\nsinglefreq\ncalibrate\nmeasure\nad5933> '
            
        # --- COMANDOS EXISTENTES DE MEDICIÓN Y CALIBRACIÓN (INTACTOS) ---
        elif "singlefreq" in cmd:
            real_val = -15610 + random.randint(-500, 500)
            imag_val = -1335 + random.randint(-150, 150)
            response = f"{real_val} {imag_val}j\nad5933> "
            
        elif "calibrate" in cmd:
            # Asumimos que la calibración no devuelve JSON, solo el prompt si hay éxito
            response = "ad5933> " 
            
        else:
            # BLOQUE DE REASEGURO (SWEEP / FALLBACK):
            # Si el adaptador envía cualquier otro comando (o sweep/start), responde con el JSON completo.
            sweep_data = {
                "sweep": {
                    "result": {
                        "magnitude": [
                            [185 + random.randint(-50, 50), -1830 + random.randint(-50, 50)], 
                            [634 + random.randint(-50, 50), -1717 + random.randint(-50, 50)], 
                            [1022 + random.randint(-50, 50), -1512 + random.randint(-50, 50)], 
                            [1348 + random.randint(-50, 50), -1222 + random.randint(-50, 50)], 
                            [1591 + random.randint(-50, 50), -861 + random.randint(-50, 50)]
                        ],
                        "frequency": [10000, 30000, 50000, 70000, 90000]
                    }
                }
            }
            response = json.dumps(sweep_data) + "\nad5933> "
            
        print(f"Mock RX <--- Placa responde: {response.strip()}")
        return response