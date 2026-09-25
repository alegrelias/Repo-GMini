NOTA: hay una regla de seguridad inquebrantable para aplicaciones locales: las contraseñas nunca deben guardarse en texto plano en la base de datos. Debés aplicar una función de hash (como _bcrypt_) antes de guardarlas en SQLite. De esta forma, si el archivo `.db` de la aplicación se copia o transfiere, las credenciales de los miembros del laboratorio permanecen protegidas.
# Patrones a mirar
- Builder
- Strategy
- Decorator
- Facade
- Proxy
- Memento
- Template
- State
# Clases Identificadas

+ Usuario (Abstracto)
	+ Operador
	+ Experto
+ Medicion (Abstracto) la `Medicion` representa la acción de medir
	+ Espectroscopia
	+ Monofrecuencia
	+ Multifrecuencia
+ SetupMedicion (Abstracto) El `SetupMedicion` tiene los parámetros (frecuencias, retardos)
	+ SetupEspectroscopia
	+ SetupMonofrecuencia
	+ SetupMultifrecuencia
+ SetupCalibracion
+ Placa
+ ResultadoMedicion `ResultadosMedicion` tiene los números crudos.
+ TipoConexion (Interfaz)
	+ Alambrica
	+ Inalambrica
+ ServicioMedicion
+ ServicioCalibracion
+ ServicioConexion
+ ServicioPersistencia
+ ServicioAutenticacion
+ EstadoMedicion
	+ EstadoPendiente
	+ EstadoEjecutando
	+ EstadoCompletado
	+ EstadoError
+ EstadoConexion
	+ EstadoConectado
	+ EstadoDesconectado
	+ EstadoErrorDeConeccion
+ EstadoPlaca
	+ EstadoPlacaLIbre
	+ EstadoCalibrando
	+ EstadoMidiendo
	+ EstadoError

```mermaid
classDiagram
direction LR

%% jerarquias
User <|-- Expert
User <|-- Operator

MeasureSetup <|-- SpecMeasureSetup
MeasureSetup <|-- SingleMeasureSetup
MeasureSetup <|-- MultiMeasureSetup

ConnectionType <|-- Wire
ConnectionType <|-- WireLess

MeasureState <|-- PendingState
MeasureState <|-- ExecutingState
MeasureState <|-- CompleteState
MeasureState <|-- ErrorState

ConnectionState <|-- ConnectedState
ConnectionState <|-- DisconnectedState
ConnectionState <|-- ConnectionErrorState

DeviceState <|-- FreeDeviceState
DeviceState <|-- CalibratingState
DeviceState <|-- MeasuringState
DeviceState <|-- DeviceErrorState

%% clases

class User {
	<<abstract>>
	- user_id : int
	- user_name : str
	- email : str
	- password : str
	+ has_permission(action : str)
}

class Operator{

}
class Expert{

}

class Measure {
	- measureSetup : MeasureSetup
	- date : DateTime
	- state : MeasureState
	- device_temp : float
	- result : MeasureResult
	+ set_state(new_state : MeasureState)
	+ get_state() : MeasureState
}

class MeasureSetup {
		<<abstract>>
		- exitation_voltage : float
		- gain : float
		- rfbvalue : float
		- settcycles : int
		- mux_channel : [0, 1, 2, 3]
		+ get_command() : str
}
class SpecMeasureSetup{
	- startfreq : float
	- incfreq : float
	- steps : int
	- repeat : int
}
class SingleMeasureSetup{
	- freq : float
	- delay : int
	- count : int
}
class MultiMeasureSetup{
	- freq_list :[float]
}

class CalibrationSetup{
	- channel : ["RCAL1":0, "RCAL2":1, "Other":2/3]
	- z_calc_value_real : float
	- z_calc_value_imag : float
	+ get_command() : str
}

class Device{
	- device_id : int
	- connection_type : ConnectionType
	- device_state : DeviceState
	+ set_state(new_state : DeviceState)
	+ get_state() : DeviceState
}

class MeasureResult{
	- frequencies : [float]
	- amplitudes : [float]
	- phases : [float]
	- impedances : [complex]
	+ measure_mean() : [float]
	+ measure_std() : [float]
}

class ConnectionType {
	<<abstract>>
	- connection_state : ConnectionState
	+ connect(device)
	+ disconnect()
	+ send(data : str)
	+ receive() : str
	+ set_state(new_state : ConnectionState)
	+ get_state() : ConnectionState
}
class Wire{
	- baudrate : int
	- port_name : str
	- timeout : int
}
class WireLess{
	- protocol : str
}

%% servicios

class MeasureService{
	+ execute_measure(measure : Measure) : MeasureResult
}
class PersistanceService{
	- db_root : str
	+ save_measure(result : Measure)
	+ import_result() : MeasureResult
	+ save_calibration_setup(cal_setup : CalibrationSetup)
	+ import_calibration_setup() : CalibrationSetup
	+ save_measure_setup(m_setup : MeasureSetup)
	+ import_measure_setup() : MeasureSetup
}
class AuthService{
	+ login(user_name, email, password) : Token
	+ logout()
	+ register(user_name, email, password) : Token
	
}
class ConnectionService{
	+ connect(device : Device, connection_type : ConnectionType)
	+ disconnect()
}
class CalibrationService{
	+ calibrate_device(device : Device, cal_setup : CalibrationSetup)
}

%% state patern

class DeviceState{
		<<abstract>>
	}
	class FreeDeviceState
	class CalibratingState
	class MeasuringState
	class DeviceErrorState
	
class ConnectionState{
		<<abstract>>
	}
	class ConnectedState
	class DisconnectedState
	class ConnectionErrorState
	
class MeasureState{
	 <<abstract>>
}
class PendingState
class ExecutingState
class CompleteState
class ErrorState
	    
%% relaciones 

```

##### Subsistema 1: Comunicación e Interacción con el Hardware

##### Módulo 1: Conectividad y Estado

```mermaid
classDiagram

%% jerarquias

User <|-- Operator
User <|-- Expert

ConnectionType <|-- Wire
ConnectionType <|-- WireLess

DeviceState <|-- FreeDeviceState
DeviceState <|-- CalibratingState
DeviceState <|-- MeasuringState
DeviceState <|-- DeviceErrorState

ConnectionState <|-- ConnectedState
ConnectionState <|-- DisconnectedState
ConnectionState <|-- ConnectionErrorState

%% clases

class ConnectionType {
	<<abstract>>
	- connection_state : ConnectionState
	+ connect(device)
	+ disconnect()
	+ send(data : str)
	+ receive() : str
	+ set_state(new_state : ConnectionState)
	+ get_state() : ConnectionState
}
class Wire{
	- baudrate : int
	- port_name : str
	- timeout : int
}
class WireLess{
	- protocol : str
}

class User {
        <<abstract>>
        - user_id : int
        - user_name : str
        - email : str
        - password : str
        + has_permission(action : str)
    }
    
class Operator{

}
class Expert{

}

class Device{
	- device_id : int
	- connection_type : ConnectionType
	- device_state : DeviceState
	+ set_state(new_state : DeviceState)
	+ get_state() : DeviceState
}

class ConnectionService{
	+ connect(device : Device, connection_type : ConnectionType)
	+ disconnect()
}

class DeviceState{
		<<abstract>>
	}
class FreeDeviceState
class CalibratingState
class MeasuringState
class DeviceErrorState
	
class ConnectionState{
		<<abstract>>
	}
class ConnectedState
class DisconnectedState
class ConnectionErrorState

%% relaciones

User "1"-->"1" Device : conecta

Device "1" o-- "1" ConnectionType
Device "1" *-- "1" DeviceState

ConnectionService "1" ..> "1" Device

ConnectionType "1" *-- "1" ConnectionState
```


##### Módulo 2: Calibración del Dispositivo
```mermaid
classDiagram

%% jerarquias
User <|-- Expert
User <|-- Operator

%% clases
class User {
        <<abstract>>
        - user_id : int
        - user_name : str
        - email : str
        - password : str
        + has_permission(action : str)
    }
    
class Operator{

}
class Expert{

}

class CalibrationSetup{
	- channel : ["RCAL1":0, "RCAL2":1, "Other":2/3]
	- z_calc_value_real : float
	- z_calc_value_imag : float
	+ get_command() : str
}

class Device{
	- device_id : int
	- connection_type : ConnectionType
	- device_state : DeviceState
	+ set_state(new_state : DeviceState)
	+ get_state() : DeviceState
}

class CalibrationService{
	+ calibrate_device(device : Device, cal_setup : CalibrationSetup)
}

class PersistanceService{
	- db_root : str
	+ save_measure(result : Measure)
	+ import_result() : MeasureResult
	+ save_calibration_setup(cal_setup : CalibrationSetup)
	+ import_calibration_setup() : CalibrationSetup
	+ save_measure_setup(m_setup : MeasureSetup)
	+ import_measure_setup() : MeasureSetup
}

%% relaciones
User "1"-->"1" Device : calibra

PersistanceService "1"..>"1" CalibrationSetup

CalibrationService "1"..>"1" Device
CalibrationService "1"..>"1" CalibrationSetup
```

#### Subsistema 2: Configuración y Toma de Mediciones
##### Módulo 1: Tipos y Estrategias de Medición

```mermaid
classDiagram

%% jerarquias
User <|-- Expert
User <|-- Operator

MeasureSetup <|-- SpecMeasureSetup
MeasureSetup <|-- SingleMeasureSetup
MeasureSetup <|-- MultiMeasureSetup

MeasureState <|-- PendingState
MeasureState <|-- ExecutingState
MeasureState <|-- CompleteState
MeasureState <|-- ErrorState

%% clases
class User {
        <<abstract>>
        - user_id : int
        - user_name : str
        - email : str
        - password : str
        + has_permission(action : str)
    }
    

    
class Operator{

}
class Expert{

}

class Measure {
	- measureSetup : MeasureSetup
	- date : DateTime
	- state : MeasureState
	- device_temp : float
	- result : MeasureResult
	+ set_state(new_state : MeasureState)
	+ get_state() : MeasureState
}

class MeasureSetup {
		<<abstract>>
		- exitation_voltage : float
		- gain : float
		- rfbvalue : float
		- settcycles : int
		- mux_channel : [0, 1, 2, 3]
		+ get_command() : str
}
class SpecMeasureSetup{
	- startfreq : float
	- incfreq : float
	- steps : int
	- repeat : int
}
class SingleMeasureSetup{
	- freq : float
	- delay : int
	- count : int
}
class MultiMeasureSetup{
	- freq_list :[float]
}

class MeasureResult{
	- frequencies : [float]
	- amplitudes : [float]
	- phases : [float]
	- impedances : [complex]
	+ measure_mean() : [float]
	+ measure_std() : [float]
}

class MeasureService{
	+ execute_measure(measure : Measure) : MeasureResult
}

class MeasureState{
	 <<abstract>>
}
class PendingState
class ExecutingState
class CompleteState
class ErrorState

%% relaciones
User "1"-->"1" Measure : mide

Measure "1"o--"1" MeasureSetup
Measure "1"*--"1" MeasureResult
Measure "1"*--"1" MeasureState

MeasureService "1"..>"1" Measure
```
#### Subsistema 3: Configuración y Gestión de Perfiles (Setups)

##### Módulo 1: Perfiles de Usuario y Gestión de Setups de Medición
```mermaid
classDiagram
direction LR

%% jerarquias
User <|-- Expert
User <|-- Operator

MeasureSetup <|-- SpecMeasureSetup
MeasureSetup <|-- SingleMeasureSetup
MeasureSetup <|-- MultiMeasureSetup

class User {
	<<abstract>>
	- user_id : int
	- user_name : str
	- email : str
	- password : str
	+ has_permission(action : str)
}

class Operator{

}
class Expert{

}

class AuthService{
	+ login(user_name, email, password) : Token
	+ logout()
	+ register(user_name, email, password) : Token
}

class PersistanceService{
	- db_root : str
	+ save_measure(result : Measure)
	+ import_result() : MeasureResult
	+ save_calibration_setup(cal_setup : CalibrationSetup)
	+ import_calibration_setup() : CalibrationSetup
	+ save_measure_setup(m_setup : MeasureSetup)
	+ import_measure_setup() : MeasureSetup
}

class MeasureSetup {
		<<abstract>>
		- exitation_voltage : float
		- gain : float
		- rfbvalue : float
		- settcycles : int
		- mux_channel : [0, 1, 2, 3]
		+ get_command() : str
}
class SpecMeasureSetup{
	- startfreq : float
	- incfreq : float
	- steps : int
	- repeat : int
}
class SingleMeasureSetup{
	- freq : float
	- delay : int
	- count : int
}
class MultiMeasureSetup{
	- freq_list :[float]
}

class CalibrationSetup{
	- channel : ["RCAL1":0, "RCAL2":1, "Other":2/3]
	- z_calc_value_real : float
	- z_calc_value_imag : float
	+ get_command() : str
}

%% relaciones

Expert "1"-->"0..*" MeasureSetup : crea
Expert "1"-->"0..*" CalibrationSetup : crea

User "1"-->"0..*" MeasureSetup : gestiona
User "1"-->"0..*" CalibrationSetup : gestiona

AuthService "1"..>"1" User

PersistanceService "1"..>"1" MeasureSetup
PersistanceService "1"..>"1" CalibrationSetup

```

#### Subsistema 5: Persistencia

##### Módulo 1: Almacenamiento y Estructura de Datos

```mermaid
classDiagram

%% jerarquias
User <|-- Expert
User <|-- Operator

%% clases
class User {
	<<abstract>>
	- user_id : int
	- user_name : str
	- email : str
	- password : str
	+ has_permission(action : str)
}

class Operator{

}
class Expert{

}

class Measure {
	- measureSetup : MeasureSetup
	- date : DateTime
	- state : MeasureState
	- device_temp : float
	- result : MeasureResult
	+ set_state(new_state : MeasureState)
	+ get_state() : MeasureState
}

class PersistanceService{
	- db_root : str
	+ save_measure(result : Measure)
	+ import_result() : MeasureResult
	+ save_calibration_setup(cal_setup : CalibrationSetup)
	+ import_calibration_setup() : CalibrationSetup
	+ save_measure_setup(m_setup : MeasureSetup)
	+ import_measure_setup() : MeasureSetup
}

%% relaciones
User "1"-->"0..*" Measure : guarda

PersistanceService "1"..>"1" Measure
```
