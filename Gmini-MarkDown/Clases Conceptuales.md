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

Measure <|-- Spectroscopy
Measure <|-- SingleFreq
Measure <|-- MultiFreq

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
        + get_role()
    }
    
    class Operator{

    }
    class Expert{
	
    }

    class Measure {
        <<abstract>>
        - measureSetup : MeasureSetup
        - date : str
        - state : MeasureState
        - device_temp : float
    }
    class Spectroscopy
    class SingleFreq
    class MultiFreq

    class MeasureSetup {
        <<abstract>>
        - exitation_voltage : float
        - gain : float
        - rfbvalue : float
        - settcycles : int
        - mux_channel : [0, 1, 2, 3]
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
    }
    
    class Device{
		- device_id : int
		- connection_type : ConnectionType
		- device_state : DeviceState
    }
    
    class DeviceState{
	    <<abstract>>
    }
    class FreeDeviceState
    class CalibratingState
    class MeasuringState
    class DeviceErrorState
    
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
    }
    class Wire{
	    - baudrate : int
	    - port_name : str
	    - timeout : int
    }
    class WireLess{
	    - protocol : str
    }
    
    class ConnectionState{
	    <<abstract>>
    }
    class ConnectedState
    class DisconnectedState
    class ConnectionErrorState

    class MeasureService{
	    + execute_measure(setup) : MeasureResult
    }
    class PersistanceService{
	    + save_result(result : MeasureResult)
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
	    + connect(connection_type : ConnectionType)
	    + disconnect()
    }
    class CalibrationService{
	    + calibrate_device(device : Device, cal_setup : CalibrationSetup)
    }
    
    class MeasureState{
	     <<abstract>>
    }
    class PendingState
    class ExecutingState
    class CompleteState
    class ErrorState
```

##### Subsistema 1: Comunicación e Interacción con el Hardware

##### Módulo 1: Conectividad y Estado

```mermaid
classDiagram

%% jerarquias

TipoConexion <|-- Alambrica
TipoConexion <|-- Inalambrica

%% clases

class TipoConexion {
        <<interface>>
    }
    class Alambrica
    class Inalambrica

class Operador

class Placa

ServicioMedicion

%% relaciones

Operador -- ServicioMedicion
Placa -- TipoConexion
Placa -- ServicioMedicion
```

##### Módulo 2: Calibración del Dispositivo
```mermaid
classDiagram

%% jerarquias
Usuario <|-- Experto
Usuario <|-- Operador

%% clases
class Usuario {
        <<abstract>>
    }
class Experto
class Operador
class SetupCalibracion
class Placa
class ServicioMedicion
class ServicioPersistencia

%% relaciones
Usuario -- ServicioMedicion
Placa -- ServicioMedicion
ServicioMedicion -- SetupCalibracion
SetupCalibracion -- ServicioPersistencia
```

#### Subsistema 2: Configuración y Toma de Mediciones
##### Módulo 1: Tipos y Estrategias de Medición

```mermaid
classDiagram

%% jerarquias
Usuario <|-- Experto
Usuario <|-- Operador

Medicion <|-- Espectroscopia
Medicion <|-- Monofrecuencia
Medicion <|-- Multifrecuencia

SetupMedicion <|-- SetupEspectroscopia
SetupMedicion <|-- SetupMonofrecuencia
SetupMedicion <|-- SetupMultifrecuencia

%% clases
class Usuario {
        <<abstract>>
    }
class Experto
class Operador

class Medicion{
		<<abstract>>
	}
class Espectroscopia
class Monofrecuencia
class Multifrecuencia

class SetupMedicion{
		<<abstract>>
	}
class SetupEspectroscopia
class SetupMonofrecuencia
class SetupMultifrecuencia

class Placa
class ServicioMedicion
class ResultadoMedicion

%% relaciones
Usuario -- ServicioMedicion
ServicioMedicion -- Placa
ServicioMedicion -- Medicion

Medicion -- SetupMedicion
Medicion -- ResultadoMedicion
```
#### Subsistema 3: Configuración y Gestión de Perfiles (Setups)

##### Módulo 1: Perfiles de Usuario y Gestión de Setups de Medición
```mermaid
classDiagram

%% jerarquias
Usuario <|-- Experto
Usuario <|-- Operador

SetupMedicion <|-- SetupEspectroscopia
SetupMedicion <|-- SetupMonofrecuencia
SetupMedicion <|-- SetupMultifrecuencia

%% clases
class Usuario {
        <<abstract>>
    }
class Experto
class Operador

class SetupMedicion{
		<<abstract>>
	}
class SetupEspectroscopia
class SetupMonofrecuencia
class SetupMultifrecuencia

class ServicioAutenticacion
class ServicioPersistencia

%% relaciones
Usuario -- ServicioPersistencia
Usuario -- ServicioAutenticacion
SetupMedicion -- ServicioPersistencia
```

#### Subsistema 5: Persistencia

##### Módulo 1: Almacenamiento y Estructura de Datos

```mermaid
classDiagram

%% jerarquias
Medicion <|-- Espectroscopia
Medicion <|-- Monofrecuencia
Medicion <|-- Multifrecuencia

%% clases
class Usuario
class ServicioPersistencia
class ServicioMedicion

class Medicion{
		<<abstract>>
	}
class Espectroscopia
class Monofrecuencia
class Multifrecuencia

class ResultadoMedicion

%% relaciones
Usuario -- ServicioMedicion
Usuario -- ServicioPersistencia

ServicioMedicion -- Medicion
Medicion -- ResultadoMedicion

%% Nuevas relaciones clave para la persistencia
ServicioMedicion -- ServicioPersistencia
Medicion -- ServicioPersistencia
ResultadoMedicion -- ServicioPersistencia
```

