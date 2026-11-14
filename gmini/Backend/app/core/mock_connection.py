
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
        
        # Simulamos respuestas específicas según el comando enviado
        if "singlefreq" in self.last_command:
            # Respuesta típica de monofrecuencia
            response = "-15610 -1335j\nad5933> "
        elif "sweep" in self.last_command:
            # Respuesta truncada de sweep en formato JSON para simplificar
            response = '{"sweep": {"result": {"magnitude": [[185,-1830], [634,-1717]], "frequency": [10000,30000]}}}\nad5933> '
        elif "calibrate" in self.last_command:
            # Asumimos que la calibración no devuelve JSON, solo el prompt si hay éxito
            response = "ad5933> " 
            
        print(f"Mock RX <--- Placa responde: {response.strip()}")
        return response