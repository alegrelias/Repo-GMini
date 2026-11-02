from app.models.device import Device
from app.models.calibrationSetup import CalibrationSetup
from app.services.sessionManager import SessionManager
from app.services.connectionService import ConnectionService
from app.adapters.iCalibrationAdapter import ICalibrationAdapter


"""Servicio encargado de orquestar la calibración electrónica del equipo"""
class CalibrationService:
    
    def __init__(self, session_manager: SessionManager, 
                 connection_service: ConnectionService, 
                 adapter: ICalibrationAdapter):
        self._session_manager = session_manager
        self._connection_service = connection_service
        self._adapter = adapter

    """Ejecuta el proceso de calibración en el hardware y actualiza el estado del dispositivo"""
    def calibrate_device(self, device: Device, cal_setup: CalibrationSetup) -> bool:
        #Validación de seguridad y permisos 
        current_user = self._session_manager.get_current_user()
        if not current_user:
            raise PermissionError("Debe iniciar sesión para calibrar el dispositivo.")
            
        if not self._session_manager.get_active_mode():
            raise PermissionError("La calibración requiere permisos de Modo Avanzado.")

        #Traducción de la configuración a comando físico usando el Adaptador
        comando_calibracion = self._adapter.encode(cal_setup)

        try:
            #Envío del comando a la placa a través del servicio de conexión
            self._connection_service.send(device, comando_calibracion)
            
            #Recepción de la respuesta cruda de la consola del hardware
            respuesta_cruda = self._connection_service.receive(device)
            
            #Delegamos al adaptador la responsabilidad de entender si fue exitoso (códigos -1 a -5)
            calibracion_exitosa = self._adapter.decode(respuesta_cruda)

            #Actualizamos el patrón State del dispositivo según el resultado
            if calibracion_exitosa:
                print("Calibración exitosa.")
                #device.set_state(CalibratedState())  # Descomentar al implementar states
            else:
                print("Fallo en la calibración reportado por la placa.")
                #device.set_state(UncalibratedState())

            return calibracion_exitosa

        except Exception as e:
            #Manejo de fallos en el puerto serie, Bluetooth, o desconexiones súbitas
            print(f"Error de comunicación I/O durante la calibración: {e}")
            #device.set_state(DeviceErrorState())
            return False