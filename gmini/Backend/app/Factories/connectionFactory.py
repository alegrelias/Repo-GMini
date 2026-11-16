from gmini.Backend.app.core.connectionType import ConnectionType, Wire, WireLess

class ConnectionFactory:
    @staticmethod
    def create_connection(type: str) -> ConnectionType:
        type_upper = type.upper().strip()
        
        if type_upper in ["WIRE", "USB", "SERIAL"]:
            return Wire(baudrate=9600, port_name="COM3", timeout=1)
            
        elif type_upper in ["WIRELESS", "BLUETOOTH", "WIFI"]:
            return WireLess(protocol="Bluetooth")
            
        else:
            raise ValueError(f"Tipo de conexión no soportado: {type}")