import time
import uuid
from typing import List, Optional, Any
from app.core.observer import IObservable, IObserver
from app.models.device import Device
from app.models.measure import Measure
from app.models.measureSetup import MeasureSetup
from app.models.measureResult import MeasureResult
from app.states.deviceState import MeasuringState, CalibratedState, DeviceErrorState
from app.adapters.iMeasureAdapter import IMeasureAdapter
from app.services.connectionService import ConnectionService
from app.services.sessionManager import SessionManager

"""Servicio principal para la configuración y toma de mediciones. Observa a ConnectionService para actuar 
    ante cortes bruscos y es observado por la GUI para actualizar barras de progreso y resultados intermedios"""
class MeasureService(IObservable, IObserver):
    def __init__(self, 
                 connection_service: ConnectionService,
                 adapter: IMeasureAdapter,
                 session_manager: SessionManager,
                 db_service: Optional[Any] = None): 
        self._connection_service = connection_service
        self._adapter = adapter
        self._session_manager = session_manager
        self._db_service = db_service
        self._observers: List[IObserver] = []
        self._current_measure: Optional[Measure] = None
        self._executed_results: List[MeasureResult] = []
        self._connection_service.attach(self)

    """Envia los parametros de configuracion previos a la placa"""
    def apply_setup(self, device: Device, setup: Any) -> bool:
        try:
            command = self._adapter.encode_setup(setup)
            if command:
                self._connection_service.send(device, command)
                _ = self._connection_service.receive(device)
            return True
        except Exception as e:
            device.set_state(DeviceErrorState())
            self.notify(f"SETUP_ERROR: {e}")
            return False

    """Ejecuta una medición individual verificando previamente el bloqueo por descalibración """
    def execute_measure(self, device: Device, measure: Measure) -> bool:
        #Validar sesion activa
        user = self._session_manager.get_current_user()
        if not user:
            raise PermissionError("Debe iniciar sesión para ejecutar mediciones.")

        #Bloqueo por descalibración o estado inválido
        if not device.can_measure():
            raise RuntimeError(
                "El dispositivo no puede medir en su estado actual "
                "(requiere calibración previa o se encuentra ocupado/en error)."
            )

        #Preparar estado de la medición y del dispositivo
        self._current_measure = measure
        measure.set_state('EXECUTING')
        if not measure.get_file_name():
            measure.set_default_name() 
        device.set_state(MeasuringState())
        self._update_progress("MEASURE_STARTED")

        try:
            exec_cmd = self._adapter.encode_execution(measure.get_measure_setup())
            
            self._connection_service.send(device, exec_cmd)
            raw_response = self._connection_service.receive(device)

            result = self._adapter.decode(raw_response)
            measure.set_result(result)
            measure.set_state('COMPLETE')
            self._executed_results.append(result)

            device.set_state(CalibratedState())
            self._update_progress("MEASURE_COMPLETED")
            return True

        except Exception as e:
            measure.set_state('ERROR')
            device.set_state(DeviceErrorState())
            self._emergency_save(measure) 
            self._update_progress(f"MEASURE_ERROR: {e}")
            return False
        finally:
            self._current_measure = None

    """Ejecuta mediciones continuas en bucle a través del tiempo """
    def execute_loop(self, device: Device, base_setup: MeasureSetup, 
                     iterations: int, delay: float) -> List[Measure]:
        group_id = uuid.uuid4().hex
        completed_measures: List[Measure] = []

        for i in range(1, iterations + 1):
            measure = Measure(measure_setup=base_setup, device_id=device.device_id)
            measure._loop_group_id = group_id
            measure.set_iteration_number(i)

            self._update_progress(f"LOOP_ITERATION_{i}_OF_{iterations}")
            success = self.execute_measure(device, measure)
            completed_measures.append(measure)

            #Si falla la conexion en medio del bucle, abortamos el ciclo
            if not success:
                break

            self._update_progress(f"INTERMEDIATE_RESULT_READY:{i}")

            if i < iterations and delay > 0:
                time.sleep(delay)

        return completed_measures

    def finish_measure(self) -> List[MeasureResult]:
        """Devuelve la lista de resultados recolectados y limpia el buffer temporal."""
        results = list(self._executed_results)
        self._executed_results.clear()
        return results

    def _update_progress(self, status_msg: str = "PROGRESS_UPDATED") -> None:
        """Método privado según diagrama para emitir avance a la GUI (MED-09, MED-10)."""
        self.notify(status_msg)

    def _emergency_save(self, measure: Measure) -> None:
        """Persiste los últimos datos recolectados ante un error (MED-14)."""
        user = self._session_manager.get_current_user()
        if self._db_service and user:
            try:
                self._db_service.save_measure(user.get_id(), measure)
            except Exception as db_err:
                print(f"Fallo crítico al intentar guardado de emergencia: {db_err}")

    def update(self, observable: IObservable, event_info: str) -> None:
        if "ERROR" in event_info or "DISCONNECTED" in event_info:
            if self._current_measure and self._current_measure.get_state() == 'EXECUTING':
                self._current_measure.set_state('ERROR')
                self._emergency_save(self._current_measure)
                self.notify("EMERGENCY_SAVE_TRIGGERED")

    def attach(self, observer: IObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: IObserver) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event_info: str = "") -> None:
        for observer in self._observers:
            observer.update(self, event_info)